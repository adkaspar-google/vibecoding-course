# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Lab 07 Reference Solution: Subagent Context Firewalls, PR Triage & LLM Council.

Implements:
- REQ-0701: Subagent Context Firewall (isolating high-token child search traces from parent).
- REQ-0702: Read-Only Subagent Tool Boundary Validator (code-explorer, code-architect, code-reviewer).
- REQ-0703: Stanford CS146S Multi-Agent PR Triage (MUST_FIX, RECOMMENDED, CONSIDER + >=80 confidence).
- REQ-0704: Karpathy's llm-council Anonymized Peer Review & Borda Rank Aggregation.
- REQ-0705: Workspace Isolation Mode Selector (inherit vs. worktree).
- REQ-0706: Disjoint git worktree File-Ownership Validator.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


FILE_LINE_RE = re.compile(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]+:L?\d+")
READ_ONLY_TOOLS = frozenset({"Glob", "Grep", "Read", "LSP"})
READ_ONLY_SUBAGENT_ROLES = frozenset({"code-explorer", "code-architect", "code-reviewer"})


@dataclass(frozen=True)
class SubagentFirewallResult:
  """Metrics and bounded summary produced by a Subagent Context Firewall (REQ-0701)."""

  child_search_tokens_burned: int
  parent_summary_tokens_returned: int
  isolation_ratio: float
  summary_markdown: str


def execute_subagent_context_firewall(
    raw_search_traces: list[str],
    concise_findings: list[str],
    max_parent_tokens: int = 600,
) -> SubagentFirewallResult:
  """Isolates noisy child search trajectories and returns a bounded file:line summary to parent (REQ-0701)."""
  if not raw_search_traces or not concise_findings:
    raise ValueError("raw_search_traces and concise_findings must be non-empty")

  for finding in concise_findings:
    if not FILE_LINE_RE.search(finding):
      raise ValueError(f"Subagent summary finding must include a file:line citation: '{finding}'")

  summary_lines = ["## Subagent Context-Firewall Summary"]
  summary_lines.extend(f"- {f.strip()}" for f in concise_findings)
  summary_md = "\n".join(summary_lines)

  child_chars = sum(len(t) for t in raw_search_traces)
  parent_chars = len(summary_md)
  child_tokens = max(1, (child_chars + 3) // 4)
  parent_tokens = max(1, (parent_chars + 3) // 4)

  if parent_tokens > max_parent_tokens:
    raise ValueError(
        f"Subagent summary ({parent_tokens} tokens) exceeds max_parent_tokens={max_parent_tokens}"
    )

  isolation = round(max(0.0, (child_tokens - parent_tokens) / float(child_tokens)), 4)
  return SubagentFirewallResult(
      child_search_tokens_burned=child_tokens,
      parent_summary_tokens_returned=parent_tokens,
      isolation_ratio=isolation,
      summary_markdown=summary_md,
  )


def validate_subagent_tool_boundary(
    agent_role: str,
    requested_tools: list[str],
) -> tuple[bool, list[str]]:
  """Enforces strict read-only tool boundaries on explorer, architect, and reviewer subagents (REQ-0702)."""
  role = agent_role.strip()
  violations: list[str] = []
  if not requested_tools:
    violations.append(f"Subagent '{role}' must declare at least one tool")
  if role in READ_ONLY_SUBAGENT_ROLES:
    forbidden = [t for t in requested_tools if t not in READ_ONLY_TOOLS]
    if forbidden:
      violations.append(
          f"Read-only subagent '{role}' cannot be granted mutating/shell tools: {forbidden}"
      )
  return (len(violations) == 0, violations)


class TriageTier(str, Enum):
  """Stanford CS146S Multi-Agent PR Triage severity buckets (REQ-0703)."""

  MUST_FIX = "MUST_FIX"        # Red: Security vulnerabilities, data corruption, broken invariants
  RECOMMENDED = "RECOMMENDED"  # Yellow: Performance bottlenecks, architectural boundary leaks
  CONSIDER = "CONSIDER"        # Green: Minor style or readability improvements


@dataclass(frozen=True)
class ReviewFinding:
  """Single finding emitted by a specialist review subagent (REQ-0703)."""

  specialist: str  # "Security" | "Performance" | "Architecture" | "Style" | "EdgeCases"
  title: str
  file_line: str
  confidence: int  # 0..100
  tier: TriageTier


@dataclass(frozen=True)
class PrTriageReport:
  """Synthesized multi-agent PR review report with confidence filtering (REQ-0703)."""

  must_fix: tuple[ReviewFinding, ...]
  recommended: tuple[ReviewFinding, ...]
  consider: tuple[ReviewFinding, ...]
  dropped_low_confidence_count: int
  blocks_merge: bool


def synthesize_pr_triage_report(
    findings: list[ReviewFinding],
    min_confidence: int = 80,
) -> PrTriageReport:
  """Filters out findings with confidence < min_confidence and buckets into MUST_FIX / RECOMMENDED / CONSIDER (REQ-0703)."""
  must_fix: list[ReviewFinding] = []
  recommended: list[ReviewFinding] = []
  consider: list[ReviewFinding] = []
  dropped = 0

  for f in findings:
    if f.confidence < min_confidence:
      dropped += 1
      continue
    if not FILE_LINE_RE.search(f.file_line):
      raise ValueError(f"ReviewFinding must have a valid file:line citation, got '{f.file_line}'")
    if f.tier == TriageTier.MUST_FIX:
      must_fix.append(f)
    elif f.tier == TriageTier.RECOMMENDED:
      recommended.append(f)
    else:
      consider.append(f)

  return PrTriageReport(
      must_fix=tuple(must_fix),
      recommended=tuple(recommended),
      consider=tuple(consider),
      dropped_low_confidence_count=dropped,
      blocks_merge=len(must_fix) > 0,
  )


def anonymize_council_responses(
    model_outputs: dict[str, str],
) -> tuple[dict[str, str], dict[str, str]]:
  """Replaces model identifiers with anonymous labels ('Response A', 'Response B', ...) (karpathy/llm-council, REQ-0704)."""
  if len(model_outputs) < 2:
    raise ValueError("llm-council requires at least 2 distinct model outputs")

  anon_payload: dict[str, str] = {}
  label_to_model: dict[str, str] = {}
  for idx, (model_name, text) in enumerate(sorted(model_outputs.items())):
    label = f"Response {chr(ord('A') + idx)}"
    anon_payload[label] = text
    label_to_model[label] = model_name
  return (anon_payload, label_to_model)


@dataclass(frozen=True)
class CouncilSynthesisResult:
  """Result of Borda count rank aggregation across anonymized peer reviews (REQ-0704)."""

  winning_label: str
  winning_model: str
  borda_scores_by_label: dict[str, int]
  borda_scores_by_model: dict[str, int]


def aggregate_borda_rankings(
    ballots: list[list[str]],
    label_to_model: dict[str, str],
) -> CouncilSynthesisResult:
  """Aggregates ranked ballots using Borda count (1st place = N points, ..., last = 1 point) (REQ-0704)."""
  if not ballots:
    raise ValueError("ballots must be non-empty")
  n_candidates = len(label_to_model)
  scores_by_label: dict[str, int] = {label: 0 for label in label_to_model}

  for ballot in ballots:
    if set(ballot) != set(label_to_model.keys()) or len(ballot) != n_candidates:
      raise ValueError(f"Invalid ballot {ballot}: must rank every candidate exactly once")
    for rank_idx, label in enumerate(ballot):
      points = n_candidates - rank_idx
      scores_by_label[label] += points

  winning_label = sorted(
      scores_by_label.keys(),
      key=lambda lbl: (-scores_by_label[lbl], lbl),
  )[0]
  scores_by_model = {
      label_to_model[lbl]: score for lbl, score in scores_by_label.items()
  }
  return CouncilSynthesisResult(
      winning_label=winning_label,
      winning_model=label_to_model[winning_label],
      borda_scores_by_label=scores_by_label,
      borda_scores_by_model=scores_by_model,
  )


def select_workspace_isolation_mode(
    is_read_only_research: bool,
    parallel_writers: int = 0,
) -> str:
  """Selects 'inherit' for read-only subagents and 'worktree' for parallel writers (REQ-0705)."""
  if is_read_only_research and parallel_writers == 0:
    return "inherit"
  return "worktree"


@dataclass(frozen=True)
class WorktreeOwnershipAudit:
  """Validation of disjoint file ownership across parallel git worktrees (REQ-0706)."""

  is_disjoint: bool
  overlapping_files: tuple[str, ...]


def validate_disjoint_worktree_ownership(
    worktree_file_maps: dict[str, list[str]],
) -> WorktreeOwnershipAudit:
  """Ensures no two parallel worktree subagents modify the same file (REQ-0706)."""
  seen: dict[str, str] = {}
  overlaps: set[str] = set()
  for wt_name, files in sorted(worktree_file_maps.items()):
    for fpath in files:
      norm = fpath.strip()
      if norm in seen and seen[norm] != wt_name:
        overlaps.add(norm)
      else:
        seen[norm] = wt_name
  sorted_overlaps = tuple(sorted(overlaps))
  return WorktreeOwnershipAudit(
      is_disjoint=len(sorted_overlaps) == 0,
      overlapping_files=sorted_overlaps,
  )
