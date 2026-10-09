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

"""Lab 03 Reference Solution: RePPIT Workflow Orchestrator & Reflection Engine.

Implements:
- REQ-0301: Task Complexity vs. Workflow Rigor Classifier (Stanford CS146S Lecture 3).
- REQ-0302: Read-Only Research Validator & Socratic Clarification Gate (/grill-me).
- REQ-0303: Orthogonal Proposal Validator & Post-Proposal Context Reset.
- REQ-0304: Plan Guardrail Validator requiring file:line targets & 'Out of Scope / Do NOT Touch'.
- REQ-0305: Phase-Based Model Router (Frontier model for Research/Propose/Plan -> Fast model for Implement/Verify).
- REQ-0306: Generate -> Reflect -> Refine (andrewyng/translation-agent) & Walkthrough Receipt Verifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


FILE_LINE_CITATION_RE = re.compile(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]+:(?:L?\d+)")
PREMATURE_SOLUTION_PHRASES: tuple[str, ...] = (
    "we should refactor",
    "i propose we rewrite",
    "recommended solution:",
    "implementation plan:",
)


class WorkflowRigor(str, Enum):
  """Task Complexity vs. Workflow Rigor Spectrum (CS146S Lecture 3, REQ-0301)."""

  VANILLA_PROMPT = "VANILLA_PROMPT"
  SINGLE_PLAN_MODE = "SINGLE_PLAN_MODE"
  REPPIT_WORKFLOW = "REPPIT_WORKFLOW"
  MULTI_SESSION_SUBAGENTS = "MULTI_SESSION_SUBAGENTS"


def classify_workflow_rigor(
    files_touched: int,
    has_architectural_ambiguity: bool = False,
    is_cross_service_migration: bool = False,
) -> WorkflowRigor:
  """Maps task scope and ambiguity to the appropriate workflow rigor tier (REQ-0301)."""
  if files_touched <= 0:
    raise ValueError("files_touched must be >= 1")
  if is_cross_service_migration or files_touched > 8:
    return WorkflowRigor.MULTI_SESSION_SUBAGENTS
  if has_architectural_ambiguity or files_touched >= 4:
    return WorkflowRigor.REPPIT_WORKFLOW
  if files_touched >= 2:
    return WorkflowRigor.SINGLE_PLAN_MODE
  return WorkflowRigor.VANILLA_PROMPT


@dataclass(frozen=True)
class ResearchValidationResult:
  """Validation result for a Step 1 Research document (REQ-0302)."""

  is_valid: bool
  citations_found: tuple[str, ...]
  contains_premature_solution: bool
  errors: tuple[str, ...]


def validate_research_document(research_markdown: str) -> ResearchValidationResult:
  """Validates that Research documents 'what exists today' with file:line citations only (REQ-0302)."""
  citations = tuple(FILE_LINE_CITATION_RE.findall(research_markdown))
  lower = research_markdown.lower()
  has_premature = any(phrase in lower for phrase in PREMATURE_SOLUTION_PHRASES)
  errors: list[str] = []
  if not citations:
    errors.append("Research document must include exact file:line citations (e.g. 'service.py:L42')")
  if has_premature:
    errors.append("Research document must strictly describe what exists today without proposing solutions")
  return ResearchValidationResult(
      is_valid=not errors,
      citations_found=citations,
      contains_premature_solution=has_premature,
      errors=tuple(errors),
  )


def evaluate_clarification_gate(unresolved_questions: list[str]) -> tuple[bool, list[str]]:
  """Socratic /grill-me gate: blocks transition to Propose/Plan while questions remain unanswered (REQ-0302)."""
  cleaned = [q.strip() for q in unresolved_questions if q and q.strip()]
  return (len(cleaned) == 0, cleaned)


@dataclass(frozen=True)
class ArchitecturalProposal:
  """Single architectural proposal in Step 2 of RePPIT (REQ-0303)."""

  proposal_id: str
  title: str
  mechanism_axis: str
  summary: str
  tradeoffs: tuple[str, ...]
  open_questions: tuple[str, ...] = ()


def validate_orthogonal_proposals(
    prop_a: ArchitecturalProposal,
    prop_b: ArchitecturalProposal,
) -> tuple[bool, list[str]]:
  """Verifies that two proposals represent genuinely orthogonal architectural axes with explicit trade-offs (REQ-0303)."""
  issues: list[str] = []
  if prop_a.proposal_id == prop_b.proposal_id:
    issues.append("Proposals must have distinct proposal_id values")
  if prop_a.mechanism_axis.strip().lower() == prop_b.mechanism_axis.strip().lower():
    issues.append(
        f"Proposals are not orthogonal: both use mechanism_axis='{prop_a.mechanism_axis}'"
    )
  if not prop_a.tradeoffs or not prop_b.tradeoffs:
    issues.append("Both proposals must list explicit engineering trade-offs")
  return (len(issues) == 0, issues)


@dataclass(frozen=True)
class PostProposalContextState:
  """Compacted context state after selecting one proposal and purging the rejected one (REQ-0303)."""

  selected_proposal_id: str
  purged_proposal_id: str
  compacted_messages: tuple[str, ...]
  tokens_saved: int


def select_proposal_and_reset_context(
    research_summary: str,
    prop_a: ArchitecturalProposal,
    prop_b: ArchitecturalProposal,
    selected_id: str,
) -> PostProposalContextState:
  """Selects one orthogonal proposal and wipes the rejected proposal's tokens from context (REQ-0303)."""
  is_ortho, issues = validate_orthogonal_proposals(prop_a, prop_b)
  if not is_ortho:
    raise ValueError(f"Cannot select from non-orthogonal proposals: {'; '.join(issues)}")

  if selected_id == prop_a.proposal_id:
    chosen, rejected = prop_a, prop_b
  elif selected_id == prop_b.proposal_id:
    chosen, rejected = prop_b, prop_a
  else:
    raise ValueError(f"Unknown proposal_id '{selected_id}'")

  rejected_blob = f"{rejected.title} {rejected.summary} {' '.join(rejected.tradeoffs)}"
  tokens_saved = max(1, (len(rejected_blob) + 3) // 4)

  compacted = (
      f"[Verified Research] {research_summary.strip()}",
      f"[Selected Proposal {chosen.proposal_id}: {chosen.title}] "
      f"axis={chosen.mechanism_axis}; summary={chosen.summary}; "
      f"tradeoffs={', '.join(chosen.tradeoffs)}",
  )
  return PostProposalContextState(
      selected_proposal_id=chosen.proposal_id,
      purged_proposal_id=rejected.proposal_id,
      compacted_messages=compacted,
      tokens_saved=tokens_saved,
  )


@dataclass(frozen=True)
class PlanValidationResult:
  """Validation report for a Step 3 Implementation Plan artifact (REQ-0304)."""

  is_valid: bool
  file_targets: tuple[str, ...]
  has_out_of_scope_section: bool
  has_verification_command: bool
  errors: tuple[str, ...]


def validate_implementation_plan(plan_markdown: str) -> PlanValidationResult:
  """Validates that an implementation plan contains file:line targets, Out of Scope guardrails, and test commands (REQ-0304)."""
  targets = tuple(FILE_LINE_CITATION_RE.findall(plan_markdown))
  lower = plan_markdown.lower()
  has_out_of_scope = "out of scope" in lower or "do not touch" in lower
  has_verify = any(
      cmd in lower for cmd in ("unittest", "pytest", "self_diagnose", "/browser", "playwright")
  )
  errors: list[str] = []
  if not targets:
    errors.append("Plan must specify exact file:line targets (e.g. 'handlers/checkout.py:L20')")
  if not has_out_of_scope:
    errors.append("Plan must include an explicit 'Out of Scope / Do NOT Touch' guardrail section")
  if not has_verify:
    errors.append("Plan must include a deterministic verification command")
  return PlanValidationResult(
      is_valid=not errors,
      file_targets=targets,
      has_out_of_scope_section=has_out_of_scope,
      has_verification_command=has_verify,
      errors=tuple(errors),
  )


class ReppitPhase(str, Enum):
  """5 phases of the RePPIT workflow (REQ-0305)."""

  RESEARCH = "RESEARCH"
  PROPOSE = "PROPOSE"
  PLAN = "PLAN"
  IMPLEMENT = "IMPLEMENT"
  TEST_VERIFY = "TEST_VERIFY"


@dataclass(frozen=True)
class ModelRouteDecision:
  """Model selection decision for a given RePPIT phase and harness (REQ-0305)."""

  phase: ReppitPhase
  harness: str
  model_id: str
  tier: str  # "frontier_reasoning" | "fast_execution"


def route_model_for_reppit_phase(phase: ReppitPhase, harness: str = "agy") -> ModelRouteDecision:
  """Routes Research/Propose/Plan to a frontier reasoning model and Implement/Verify to a fast model (REQ-0305)."""
  norm_harness = harness.strip().lower()
  if norm_harness not in ("agy", "claude"):
    raise ValueError(f"Unsupported harness '{harness}': expected 'agy' or 'claude'")

  if phase in (ReppitPhase.RESEARCH, ReppitPhase.PROPOSE, ReppitPhase.PLAN):
    model_id = "gemini-3.1-pro" if norm_harness == "agy" else "claude-opus-4-6"
    return ModelRouteDecision(
        phase=phase,
        harness=norm_harness,
        model_id=model_id,
        tier="frontier_reasoning",
    )

  model_id = "gemini-3-flash" if norm_harness == "agy" else "claude-sonnet-4-6"
  return ModelRouteDecision(
      phase=phase,
      harness=norm_harness,
      model_id=model_id,
      tier="fast_execution",
  )


@dataclass(frozen=True)
class ReflectionResult:
  """Outcome of an Andrew Ng 'Generate -> Reflect -> Refine' cycle (REQ-0306)."""

  initial_draft: str
  critique_findings: tuple[str, ...]
  refined_code: str
  converged: bool


def run_reflection_cycle(draft_code: str) -> ReflectionResult:
  """Executes a deterministic Generate -> Reflect -> Refine pass over draft code (REQ-0306)."""
  findings: list[str] = []
  refined = draft_code

  if "float(" in refined:
    findings.append("Replace float() monetary conversion with integer minor units (int)")
    refined = refined.replace("float(", "int(")

  if "except Exception: pass" in refined or "except:\n    pass" in refined:
    findings.append("Replace silent bare exception swallowing with explicit ValueError propagation")
    refined = refined.replace("except Exception: pass", "except ValueError as exc: raise exc")

  if "TODO" in refined:
    findings.append("Resolve leftover TODO placeholder before completion")
    refined = refined.replace("TODO", "VERIFIED_COMPLETE")

  return ReflectionResult(
      initial_draft=draft_code,
      critique_findings=tuple(findings),
      refined_code=refined,
      converged="float(" not in refined and "except Exception: pass" not in refined,
  )


@dataclass(frozen=True)
class WalkthroughReceipt:
  """Step 5 Walkthrough / Run Receipt artifact (REQ-0306)."""

  files_modified: tuple[str, ...]
  test_command: str
  test_exit_code: int
  browser_or_behavioral_check: str


def validate_walkthrough_receipt(
    receipt: WalkthroughReceipt,
    do_not_touch_files: tuple[str, ...] = (),
) -> tuple[bool, list[str]]:
  """Verifies a Walkthrough Run Receipt against test exit code, behavioral evidence, and Do-Not-Touch boundaries (REQ-0306)."""
  errors: list[str] = []
  if receipt.test_exit_code != 0:
    errors.append(f"Verification command failed with exit code {receipt.test_exit_code}")
  if not receipt.test_command.strip():
    errors.append("Walkthrough receipt must record the exact test command executed")
  if not receipt.browser_or_behavioral_check.strip():
    errors.append("Walkthrough receipt must include behavioral or /browser verification evidence")

  forbidden_set = set(do_not_touch_files)
  touched_forbidden = [f for f in receipt.files_modified if f in forbidden_set]
  if touched_forbidden:
    errors.append(
        f"Scope creep detected: modified Out-of-Scope files {touched_forbidden}"
    )
  return (len(errors) == 0, errors)
