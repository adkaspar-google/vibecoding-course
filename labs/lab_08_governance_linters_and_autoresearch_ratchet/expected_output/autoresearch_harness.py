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

"""Lab 08 Reference Solution: 4-Tier Governance, Remediation Linters & Autoresearch Ratchet.

Implements:
- REQ-0801: 2x2 Cybernetic Control Matrix Classifier & PreToolUse Exit-Code-2 Gate.
- REQ-0802: OpenAI Remediation-Aware Structural Linter ([VIOLATION] -> [WHY] -> [HOW TO FIX]).
- REQ-0803: Dex Horthy's Front-Loaded Program Design Verifier (Ib5GBkD555M).
- REQ-0804: Karpathy's autoresearch 3-File Harness Boundary Validator (prepare.py / train.py / program.md).
- REQ-0805: Karpathy's Simplicity Criterion & Automated Git Keep-or-Revert Ratchet.
- REQ-0806: Untracked results.tsv Experiment Ledger Formatter.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


IMMUTABLE_HARNESS_PATHS: tuple[str, ...] = (
    "prepare.py",
    "program.md",
    "adversarial_tests",
    "self_diagnose.sh",
)
MUTATING_TOOLS: frozenset[str] = frozenset({
    "Edit",
    "Write",
    "replace_file_content",
    "write_to_file",
    "Bash",
    "run_command",
})


class CyberneticQuadrant(str, Enum):
  """2x2 Cybernetic Control Matrix (martinfowler.com — Böckeler & Morris, REQ-0801)."""

  COMPUTATIONAL_GUIDE = "COMPUTATIONAL_GUIDE"      # Feedforward + Deterministic CPU
  INFERENTIAL_GUIDE = "INFERENTIAL_GUIDE"          # Feedforward + Semantic LLM
  COMPUTATIONAL_SENSOR = "COMPUTATIONAL_SENSOR"    # Feedback + Deterministic CPU
  INFERENTIAL_SENSOR = "INFERENTIAL_SENSOR"        # Feedback + Semantic LLM


def classify_cybernetic_control(
    is_feedforward_guide: bool,
    is_computational_cpu: bool,
) -> CyberneticQuadrant:
  """Maps a harness control into the 2x2 Cybernetic Control Matrix (REQ-0801)."""
  if is_feedforward_guide and is_computational_cpu:
    return CyberneticQuadrant.COMPUTATIONAL_GUIDE
  if is_feedforward_guide and not is_computational_cpu:
    return CyberneticQuadrant.INFERENTIAL_GUIDE
  if not is_feedforward_guide and is_computational_cpu:
    return CyberneticQuadrant.COMPUTATIONAL_SENSOR
  return CyberneticQuadrant.INFERENTIAL_SENSOR


@dataclass(frozen=True)
class PreToolUseHookOutcome:
  """Exit-code result of a deterministic PreToolUse governance hook (REQ-0801)."""

  exit_code: int  # 0 = allow, 2 = hard block
  provenance: str  # "auto-approved" | "denied"
  stderr_message: str


def pre_tool_use_exit_code_gate(tool_name: str, target_path_or_cmd: str) -> PreToolUseHookOutcome:
  """Returns exit_code=2 to hard-block mutations to immutable evaluation harness files (REQ-0801)."""
  if tool_name in MUTATING_TOOLS:
    for protected in IMMUTABLE_HARNESS_PATHS:
      if protected in target_path_or_cmd:
        return PreToolUseHookOutcome(
            exit_code=2,
            provenance="denied",
            stderr_message=(
                f"[HARD_FLOOR_BLOCKED] PreToolUse exit code 2: '{target_path_or_cmd}' "
                f"touches immutable verifier/harness '{protected}'. Modify only bounded target files."
            ),
        )
  return PreToolUseHookOutcome(
      exit_code=0,
      provenance="auto-approved",
      stderr_message="",
  )


def _layer_of(module_path: str) -> str:
  parts = module_path.strip().strip("/").split("/")
  return parts[0] if parts else ""


def lint_architecture_with_remediation(
    source_file: str,
    imported_modules: list[str],
    allowed_layer_imports: dict[str, set[str]],
) -> list[str]:
  """Emits agent-actionable [VIOLATION] -> [WHY] -> [HOW TO FIX] messages on layer violations (REQ-0802)."""
  src_layer = _layer_of(source_file)
  allowed = allowed_layer_imports.get(src_layer, {src_layer})
  diagnostics: list[str] = []

  for imp in imported_modules:
    imp_layer = _layer_of(imp)
    if imp_layer and imp_layer not in allowed:
      allowed_str = ", ".join(sorted(allowed)) if allowed else "none (pure leaf layer)"
      diagnostics.append(
          f"[VIOLATION] Module '{source_file}' (layer '{src_layer}') imports '{imp}' (layer '{imp_layer}'). "
          f"[WHY] Layer '{src_layer}' is only permitted to depend on [{allowed_str}] to prevent architectural coupling and context drift. "
          f"[HOW TO FIX] Extract a typed Protocol/interface into an allowed shared contract module in [{allowed_str}] and inject the dependency."
      )
  return diagnostics


@dataclass(frozen=True)
class ProgramDesignVerification:
  """Result of Dex Horthy's Front-Loaded Program Design check (Ib5GBkD555M, REQ-0803)."""

  is_aligned: bool
  untyped_modules: tuple[str, ...]
  violated_call_edges: tuple[tuple[str, str], ...]
  errors: tuple[str, ...]


def verify_front_loaded_program_design(
    module_type_signatures: dict[str, str],
    call_graph_edges: list[tuple[str, str]],
    forbidden_edges: set[tuple[str, str]],
) -> ProgramDesignVerification:
  """Verifies explicit type signatures and call-tree alignment before vertical-slice coding (REQ-0803)."""
  untyped: list[str] = []
  for mod, sig in sorted(module_type_signatures.items()):
    if "->" not in sig or ":" not in sig or "Any" in sig:
      untyped.append(mod)

  bad_edges: list[tuple[str, str]] = [
      edge for edge in call_graph_edges if edge in forbidden_edges
  ]

  errors: list[str] = []
  if untyped:
    errors.append(f"Program Design requires explicit non-Any type signatures; failed modules: {untyped}")
  if bad_edges:
    errors.append(f"Call-graph contains forbidden cross-layer edges: {bad_edges}")

  return ProgramDesignVerification(
      is_aligned=not errors,
      untyped_modules=tuple(untyped),
      violated_call_edges=tuple(bad_edges),
      errors=tuple(errors),
  )


def validate_autoresearch_file_mutation(
    modified_files: list[str],
    mutable_target: str = "train.py",
) -> tuple[bool, list[str]]:
  """Enforces karpathy/autoresearch 3-file separation: only train.py is mutable by the agent (REQ-0804)."""
  errors: list[str] = []
  if not modified_files:
    errors.append("Experiment must modify the bounded target file")
  for fpath in modified_files:
    norm = fpath.strip()
    if norm != mutable_target:
      errors.append(
          f"Forbidden file mutation '{norm}': autonomous loop may only edit '{mutable_target}' (prepare.py and program.md are read-only)"
      )
  return (len(errors) == 0, errors)


class RatchetDecision(str, Enum):
  """Decision of the Karpathy autoresearch Keep-or-Revert Ratchet (REQ-0805)."""

  KEEP_IMPROVEMENT = "KEEP_IMPROVEMENT"
  KEEP_SIMPLIFICATION = "KEEP_SIMPLIFICATION"
  REVERT_COMPLEXITY_BLOAT = "REVERT_COMPLEXITY_BLOAT"
  REVERT_GIT_RESET = "REVERT_GIT_RESET"


@dataclass(frozen=True)
class RatchetEvaluation:
  """Outcome of evaluating an experiment against val_bpb and the Simplicity Criterion (REQ-0805)."""

  decision: RatchetEvaluation | RatchetDecision
  bpb_improvement: float
  loc_delta: int
  git_action: str  # "keep_commit" | "git reset --hard HEAD~1"
  reason: str


def evaluate_autoresearch_ratchet(
    baseline_bpb: float,
    candidate_bpb: float,
    loc_delta: int,
    crashed: bool = False,
    min_gain_for_complexity: float = 0.002,
    max_loc_for_tiny_gain: int = 10,
) -> RatchetEvaluation:
  """Evaluates an experiment using karpathy/autoresearch val_bpb + Simplicity Criterion (REQ-0805)."""
  if crashed:
    return RatchetEvaluation(
        decision=RatchetDecision.REVERT_GIT_RESET,
        bpb_improvement=0.0,
        loc_delta=loc_delta,
        git_action="git reset --hard HEAD~1",
        reason="Experiment crashed; reverting commit.",
    )

  improvement = round(baseline_bpb - candidate_bpb, 6)

  # Regression: candidate val_bpb is worse (higher) than baseline.
  if improvement < 0.0:
    return RatchetEvaluation(
        decision=RatchetDecision.REVERT_GIT_RESET,
        bpb_improvement=improvement,
        loc_delta=loc_delta,
        git_action="git reset --hard HEAD~1",
        reason=f"val_bpb regressed by {abs(improvement):.6f}; reverting commit.",
    )

  # Equal or better val_bpb while deleting code -> ALWAYS KEEP (Simplicity Criterion!).
  if improvement >= 0.0 and loc_delta < 0:
    return RatchetEvaluation(
        decision=RatchetDecision.KEEP_SIMPLIFICATION,
        bpb_improvement=improvement,
        loc_delta=loc_delta,
        git_action="keep_commit",
        reason=f"Simplicity win: val_bpb improved by {improvement:.6f} while deleting {abs(loc_delta)} LOC.",
    )

  # Zero improvement without deleting code -> revert.
  if improvement == 0.0:
    return RatchetEvaluation(
        decision=RatchetDecision.REVERT_GIT_RESET,
        bpb_improvement=0.0,
        loc_delta=loc_delta,
        git_action="git reset --hard HEAD~1",
        reason="Zero val_bpb improvement without code simplification; reverting.",
    )

  # Tiny gain that adds disproportionate LOC bloat -> reject per Simplicity Criterion.
  if improvement < min_gain_for_complexity and loc_delta > max_loc_for_tiny_gain:
    return RatchetEvaluation(
        decision=RatchetDecision.REVERT_COMPLEXITY_BLOAT,
        bpb_improvement=improvement,
        loc_delta=loc_delta,
        git_action="git reset --hard HEAD~1",
        reason=(
            f"Simplicity Criterion rejected tiny gain ({improvement:.6f} < {min_gain_for_complexity}) "
            f"that added +{loc_delta} LOC (>{max_loc_for_tiny_gain})."
        ),
    )

  return RatchetEvaluation(
      decision=RatchetDecision.KEEP_IMPROVEMENT,
      bpb_improvement=improvement,
      loc_delta=loc_delta,
      git_action="keep_commit",
      reason=f"Clean val_bpb improvement of {improvement:.6f} with acceptable LOC delta ({loc_delta:+d}).",
  )


def format_results_tsv_row(
    commit_sha: str,
    val_bpb: float,
    peak_vram_mb: float,
    loc_delta: int,
    decision: RatchetDecision,
) -> str:
  """Formats an untracked results.tsv experiment ledger row (REQ-0806)."""
  status = "keep" if decision in (RatchetDecision.KEEP_IMPROVEMENT, RatchetDecision.KEEP_SIMPLIFICATION) else "discard"
  return f"{commit_sha}\t{val_bpb:.6f}\t{peak_vram_mb:.1f}\t{loc_delta:+d}\t{status}\t{decision.value}"
