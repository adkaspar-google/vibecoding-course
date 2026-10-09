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

"""7-Phase Multi-Agent Feature-Dev Orchestrator (code-explorer, code-architect, code-reviewer).

Implements REQ-0501 through REQ-0505 for Lab 05:
- Read-only subagent frontmatter validator (code-explorer, code-architect, code-reviewer)
- Phase 2 parallel code-explorer file:line citation aggregator
- Phase 3 mandatory Clarifying Questions circuit breaker before Phase 4 Architecture
- Phase 4 tri-lens code-architect synthesizer (minimal_changes, clean_architecture, pragmatic_balance)
- Phase 6 confidence-filtered (confidence >= 80) code-reviewer aggregator
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any


FILE_LINE_PATTERN = re.compile(r"^[A-Za-z0-9_./-]+:\d+$")
ALLOWED_READONLY_TOOLS = frozenset({"Glob", "Grep", "Read"})
REQUIRED_ARCHITECT_LENSES = frozenset({
    "minimal_changes",
    "clean_architecture",
    "pragmatic_balance",
})


class ClarificationGateError(RuntimeError):
  """Raised when Phase 4 Architecture is attempted with unanswered Phase 3 questions."""


class ArchitectureApprovalGateError(RuntimeError):
  """Raised when Phase 5 Implementation is attempted without human architecture selection."""


def _parse_agent_frontmatter(markdown_text: str) -> dict[str, str]:
  if not markdown_text.startswith("---\n"):
    return {}
  end_idx = markdown_text.find("\n---\n", 4)
  if end_idx == -1:
    return {}
  fm_raw = markdown_text[4:end_idx]
  meta: dict[str, str] = {}
  current_key: str | None = None
  folded: list[str] = []
  for line in fm_raw.splitlines():
    if line.startswith("  ") and current_key is not None:
      folded.append(line.strip())
      meta[current_key] = " ".join(folded).strip()
      continue
    if ":" in line:
      k, v = line.split(":", 1)
      current_key = k.strip()
      v_clean = v.strip()
      if v_clean in (">-", ">", "|"):
        folded = []
        meta[current_key] = ""
      else:
        folded = [v_clean]
        meta[current_key] = v_clean
  return meta


def validate_subagent_definitions(agents_dir: str | Path) -> dict[str, Any]:
  """Validates code-explorer, code-architect, and code-reviewer definitions (REQ-0501)."""
  base = Path(agents_dir)
  required_names = ("code-explorer", "code-architect", "code-reviewer")
  errors: list[str] = []
  validated: dict[str, dict[str, Any]] = {}

  for agent_name in required_names:
    md_file = base / f"{agent_name}.md"
    if not md_file.is_file():
      errors.append(f"Missing required subagent file: {md_file.name}")
      continue
    meta = _parse_agent_frontmatter(md_file.read_text(encoding="utf-8"))
    if meta.get("name") != agent_name:
      errors.append(f"Subagent {md_file.name} has mismatched name='{meta.get('name')}'")
    if not meta.get("description"):
      errors.append(f"Subagent {md_file.name} missing description")

    tools_raw = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
    if not tools_raw:
      errors.append(f"Subagent {md_file.name} missing tools list")
    else:
      disallowed = set(tools_raw) - ALLOWED_READONLY_TOOLS
      if disallowed:
        errors.append(
            f"Subagent {md_file.name} grants write/exec tools {sorted(disallowed)}; "
            "explorer/architect/reviewer subagents must remain read-only (Glob, Grep, Read)"
        )
    validated[agent_name] = {
        "name": agent_name,
        "tools": tuple(tools_raw),
        "model": meta.get("model", "inherit"),
    }

  return {
      "is_valid": len(errors) == 0,
      "agents": validated,
      "errors": tuple(errors),
  }


def aggregate_explorer_findings(
    explorer_reports: list[dict[str, Any]],
) -> dict[str, Any]:
  """Aggregates parallel Phase 2 code-explorer outputs and verifies file:line citations (REQ-0502)."""
  if len(explorer_reports) < 2:
    raise ValueError(
        "Phase 2 requires at least 2 parallel code-explorer reports (e.g., surface + depth)"
    )

  entry_points: list[str] = []
  call_chain_hops: list[str] = []
  essential_files: list[str] = []

  for rep in explorer_reports:
    for ep in rep.get("entry_points", []):
      ep_str = str(ep)
      if not FILE_LINE_PATTERN.match(ep_str):
        raise ValueError(
            f"Invalid entry_point citation '{ep_str}': must match path/to/file.ext:line"
        )
      if ep_str not in entry_points:
        entry_points.append(ep_str)

    for hop in rep.get("call_chain", []):
      hop_str = str(hop)
      if not FILE_LINE_PATTERN.match(hop_str):
        raise ValueError(
            f"Invalid call_chain citation '{hop_str}': must match path/to/file.ext:line"
        )
      call_chain_hops.append(hop_str)

    for fpath in rep.get("essential_files", []):
      f_str = str(fpath)
      if f_str not in essential_files:
        essential_files.append(f_str)

  return {
      "explorer_count": len(explorer_reports),
      "entry_points": tuple(entry_points),
      "call_chain": tuple(call_chain_hops),
      "essential_files": tuple(essential_files),
  }


def synthesize_architecture_options(
    proposals: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
  """Synthesizes Phase 4 code-architect proposals across the 3 required lenses (REQ-0504)."""
  by_lens: dict[str, dict[str, Any]] = {}
  for prop in proposals:
    lens = str(prop.get("lens", ""))
    if lens in REQUIRED_ARCHITECT_LENSES:
      by_lens[lens] = {
          "lens": lens,
          "summary": str(prop.get("summary", "")),
          "files_to_touch": tuple(prop.get("files_to_touch", [])),
          "tradeoffs": str(prop.get("tradeoffs", "")),
      }

  missing = REQUIRED_ARCHITECT_LENSES - set(by_lens.keys())
  if missing:
    raise ValueError(
        f"Phase 4 code-architect synthesis missing required lenses: {sorted(missing)}"
    )
  return by_lens


def filter_review_findings(
    findings: list[dict[str, Any]],
    min_confidence: int = 80,
) -> dict[str, Any]:
  """Filters Phase 6 code-reviewer outputs by confidence >= 80 (REQ-0505)."""
  retained: list[dict[str, Any]] = []
  suppressed_count = 0

  for item in findings:
    conf = int(item.get("confidence", 0))
    if conf < min_confidence:
      suppressed_count += 1
      continue
    loc = str(item.get("location", ""))
    if not FILE_LINE_PATTERN.match(loc):
      raise ValueError(
          f"Reviewer finding location '{loc}' must use exact file:line format"
      )
    retained.append({
        "category": str(item.get("category", "critical_bugs")),
        "confidence": conf,
        "location": loc,
        "description": str(item.get("description", "")),
        "fix_suggestion": str(item.get("fix_suggestion", "")),
    })

  retained.sort(key=lambda x: -int(x["confidence"]))
  return {
      "min_confidence_threshold": min_confidence,
      "retained_count": len(retained),
      "suppressed_low_confidence_count": suppressed_count,
      "high_confidence_findings": tuple(retained),
  }


@dataclass
class FeatureDevPipeline:
  """Stateful 7-phase feature-dev orchestrator with hard Phase 3 and Phase 4 gates (REQ-0503, REQ-0504)."""

  feature_request: str
  current_phase: int = 1
  explorer_summary: dict[str, Any] | None = None
  open_questions: dict[str, str | None] = field(default_factory=dict)
  architecture_options: dict[str, dict[str, Any]] = field(default_factory=dict)
  selected_architecture: str | None = None
  implemented_files: list[str] = field(default_factory=list)
  review_summary: dict[str, Any] | None = None

  def complete_phase2_exploration(self, explorer_reports: list[dict[str, Any]]) -> dict[str, Any]:
    self.explorer_summary = aggregate_explorer_findings(explorer_reports)
    self.current_phase = 2
    return self.explorer_summary

  def register_phase3_questions(self, questions: list[str]) -> None:
    if self.current_phase < 2:
      raise RuntimeError("Cannot enter Phase 3 before Phase 2 exploration completes")
    if not questions:
      raise ValueError("Phase 3 requires at least one clarifying question on underspecified edge cases")
    for q in questions:
      self.open_questions[q] = None
    self.current_phase = 3

  def answer_phase3_question(self, question: str, answer: str) -> None:
    if question not in self.open_questions:
      raise KeyError(f"Unknown clarifying question: {question}")
    if not answer or not answer.strip():
      raise ValueError("Clarifying answer cannot be empty")
    self.open_questions[question] = answer.strip()

  def advance_to_phase4_architecture(
      self, proposals: list[dict[str, Any]]
  ) -> dict[str, dict[str, Any]]:
    """Enforces the mandatory Phase 3 Clarifying Questions gate before Phase 4 (REQ-0503)."""
    unanswered = [q for q, ans in self.open_questions.items() if not ans]
    if not self.open_questions or unanswered:
      raise ClarificationGateError(
          f"BLOCKED_AWAITING_CLARIFICATION: {len(unanswered)} Phase 3 question(s) "
          "must be answered by the user before Phase 4 Architecture Design."
      )
    self.architecture_options = synthesize_architecture_options(proposals)
    self.current_phase = 4
    return self.architecture_options

  def approve_architecture_and_implement(
      self, selected_lens: str, modified_files: list[str]
  ) -> dict[str, Any]:
    """Enforces explicit human architecture approval before Phase 5 implementation (REQ-0504)."""
    if self.current_phase < 4 or not self.architecture_options:
      raise ArchitectureApprovalGateError(
          "Cannot enter Phase 5 Implementation before Phase 4 Architecture Design"
      )
    if selected_lens not in self.architecture_options:
      raise ArchitectureApprovalGateError(
          f"Selected architecture '{selected_lens}' is not among synthesized options"
      )
    self.selected_architecture = selected_lens
    self.implemented_files = list(modified_files)
    self.current_phase = 5
    return {
        "phase": 5,
        "selected_architecture": self.selected_architecture,
        "implemented_files": tuple(self.implemented_files),
    }

  def complete_phase6_review_and_phase7_summary(
      self, raw_findings: list[dict[str, Any]], min_confidence: int = 80
  ) -> dict[str, Any]:
    if self.current_phase < 5:
      raise RuntimeError("Cannot run Phase 6 review before Phase 5 implementation")
    self.review_summary = filter_review_findings(raw_findings, min_confidence=min_confidence)
    self.current_phase = 7
    return {
        "phase": 7,
        "feature_request": self.feature_request,
        "essential_files_explored": self.explorer_summary["essential_files"]
        if self.explorer_summary
        else (),
        "clarifications_resolved": len(self.open_questions),
        "selected_architecture": self.selected_architecture,
        "implemented_files": tuple(self.implemented_files),
        "high_confidence_review_findings": self.review_summary[
            "high_confidence_findings"
        ],
    }
