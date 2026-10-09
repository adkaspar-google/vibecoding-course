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

"""Lab 04 Reference Solution: Context Window Physics & RPI Compaction Engine.

Implements:
- REQ-0401: Context Window Physics & 40% Dumb Zone Classifier (Dex Horthy rmvDxxNubIg).
- REQ-0402: karpathy/autoresearch Output-Redirection Backpressure (> run.log 2>&1 & metric grep).
- REQ-0403: Sandboxed Side-Query Pruning (/btw pattern).
- REQ-0404: karpathy/rendergit CXML Repository Packer.
- REQ-0405: Frequent Intentional Compaction (RPI: Research -> Plan -> Implement) Handoff Engine.
- REQ-0406: Human Leverage Pyramid Defect Amplification Estimator (1000x Research, 100x Plan, 1x Code).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


CITATION_PATTERN = re.compile(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]+:L\d+(?:-L?\d+)?")
IGNORED_PATH_PARTS = ("__pycache__", ".git", "node_modules", ".venv", ".pytest_cache")


class ContextZone(str, Enum):
  """Context window operating zone (Dex Horthy rmvDxxNubIg, REQ-0401)."""

  SMART_ZONE = "SMART_ZONE"
  DUMB_ZONE = "DUMB_ZONE"


@dataclass(frozen=True)
class ContextWindowProfile:
  """Snapshot of context window utilization and zone classification (REQ-0401)."""

  used_tokens: int
  max_window_tokens: int
  utilization_ratio: float
  zone: ContextZone
  requires_compaction: bool


def profile_context_window(
    used_tokens: int,
    max_window_tokens: int = 200_000,
    smart_zone_ceiling: float = 0.40,
) -> ContextWindowProfile:
  """Computes context utilization ratio and classifies Smart Zone (<=0.40) vs. Dumb Zone (>0.40) (REQ-0401)."""
  if max_window_tokens <= 0:
    raise ValueError("max_window_tokens must be positive")
  if used_tokens < 0:
    raise ValueError("used_tokens must be non-negative")

  ratio = round(used_tokens / float(max_window_tokens), 4)
  in_dumb_zone = ratio > smart_zone_ceiling
  zone = ContextZone.DUMB_ZONE if in_dumb_zone else ContextZone.SMART_ZONE
  return ContextWindowProfile(
      used_tokens=used_tokens,
      max_window_tokens=max_window_tokens,
      utilization_ratio=ratio,
      zone=zone,
      requires_compaction=in_dumb_zone,
  )


def rewrite_command_with_backpressure(command: str, log_file: str = "run.log") -> str:
  """Rewrites a noisy command to redirect stdout/stderr to a log file (karpathy/autoresearch, REQ-0402)."""
  cleaned = command.strip()
  if not cleaned:
    raise ValueError("command must be non-empty")
  if "| tee" in cleaned:
    cleaned = cleaned.split("| tee")[0].strip()
  if f"> {log_file}" in cleaned:
    return cleaned
  return f"{cleaned} > {log_file} 2>&1"


@dataclass(frozen=True)
class BackpressureExtraction:
  """Compact summary extracted from a redirected log file (REQ-0402)."""

  crashed: bool
  extracted_lines: tuple[str, ...]
  raw_line_count: int
  extracted_line_count: int


def extract_backpressure_summary(
    raw_log_text: str,
    metric_prefixes: tuple[str, ...] = ("val_bpb:", "peak_vram_mb:", "PASSED", "OK"),
    tail_lines_on_crash: int = 20,
) -> BackpressureExtraction:
  """Extracts only key metric lines on success or tail lines on crash (REQ-0402)."""
  lines = raw_log_text.splitlines()
  crashed = any(
      marker in raw_log_text
      for marker in ("Traceback (most recent call last):", "RuntimeError:", "FAIL:", "ERROR:")
  )
  if crashed:
    tail = tuple(lines[-tail_lines_on_crash:]) if lines else ()
    return BackpressureExtraction(
        crashed=True,
        extracted_lines=tail,
        raw_line_count=len(lines),
        extracted_line_count=len(tail),
    )

  matched = tuple(
      line.strip()
      for line in lines
      if any(line.strip().startswith(prefix) for prefix in metric_prefixes)
  )
  return BackpressureExtraction(
      crashed=False,
      extracted_lines=matched,
      raw_line_count=len(lines),
      extracted_line_count=len(matched),
  )


def execute_sandboxed_side_query(
    active_history: list[dict[str, str]],
    question: str,
    answer: str,
) -> tuple[str, list[dict[str, str]]]:
  """Executes a /btw sandboxed side-query without polluting active_history (REQ-0403)."""
  snapshot = [dict(turn) for turn in active_history]
  formatted_reply = f"[btw side-query] Q: {question.strip()} -> A: {answer.strip()}"
  return (formatted_reply, snapshot)


def render_repo_cxml(files_dict: dict[str, str]) -> str:
  """Packs repository source files into karpathy/rendergit CXML format while skipping noise (REQ-0404)."""
  out: list[str] = ["<documents>"]
  doc_idx = 1
  for path in sorted(files_dict.keys()):
    if any(part in path for part in IGNORED_PATH_PARTS):
      continue
    content = files_dict[path]
    out.append(f'  <document index="{doc_idx}">')
    out.append(f"    <source>{path}</source>")
    out.append("    <document_content>")
    out.append(content.rstrip("\n"))
    out.append("    </document_content>")
    out.append("  </document>")
    doc_idx += 1
  out.append("</documents>")
  return "\n".join(out)


@dataclass(frozen=True)
class RpiHandoffBundle:
  """Compacted Research -> Plan -> Implement handoff artifacts (REQ-0405)."""

  research_md: str
  plan_md: str
  pre_compaction_tokens: int
  post_compaction_tokens: int
  compression_ratio: float


def compact_exploration_to_rpi_artifacts(
    noisy_turns: list[str],
    verified_findings: list[str],
    plan_steps: list[str],
    out_of_scope: list[str],
) -> RpiHandoffBundle:
  """Compacts noisy exploration turns into line-referenced research.md and plan.md artifacts (REQ-0405)."""
  if not verified_findings or not plan_steps:
    raise ValueError("verified_findings and plan_steps must be non-empty")

  for item in verified_findings + plan_steps:
    if not CITATION_PATTERN.search(item):
      raise ValueError(
          f"Every RPI finding and plan step must include an exact file:L<line> citation: '{item}'"
      )

  research_lines = ["# Research Artifact (`research.md`)", "", "## Verified Codebase Findings"]
  research_lines.extend(f"- {finding.strip()}" for finding in verified_findings)
  research_md = "\n".join(research_lines) + "\n"

  plan_lines = ["# Implementation Plan (`plan.md`)", "", "## Targeted Changes"]
  plan_lines.extend(f"{idx}. {step.strip()}" for idx, step in enumerate(plan_steps, start=1))
  plan_lines.extend(["", "## Out of Scope / Do NOT Touch"])
  plan_lines.extend(f"- {guard.strip()}" for guard in (out_of_scope or ["adversarial_tests/"]))
  plan_md = "\n".join(plan_lines) + "\n"

  pre_chars = sum(len(t) for t in noisy_turns) + len(research_md) + len(plan_md)
  post_chars = len(research_md) + len(plan_md)
  pre_tokens = max(1, (pre_chars + 3) // 4)
  post_tokens = max(1, (post_chars + 3) // 4)
  compression = round(max(0.0, (pre_tokens - post_tokens) / float(pre_tokens)), 4)

  return RpiHandoffBundle(
      research_md=research_md,
      plan_md=plan_md,
      pre_compaction_tokens=pre_tokens,
      post_compaction_tokens=post_tokens,
      compression_ratio=compression,
  )


LEVERAGE_MULTIPLIERS: dict[str, int] = {
    "RESEARCH": 1000,
    "PLAN": 100,
    "CODE": 1,
}


def estimate_defect_amplification(stage: str, defective_lines: int) -> int:
  """Computes downstream broken-code amplification across the Human Leverage Pyramid (REQ-0406)."""
  norm = stage.strip().upper()
  if norm not in LEVERAGE_MULTIPLIERS:
    raise ValueError(f"Unsupported stage '{stage}': expected RESEARCH, PLAN, or CODE")
  if defective_lines < 0:
    raise ValueError("defective_lines must be non-negative")
  return defective_lines * LEVERAGE_MULTIPLIERS[norm]
