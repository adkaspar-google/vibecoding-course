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

"""Lab 01 Reference Solution: Engineering Prompt Steering & Earned Autonomy.

Implements:
- REQ-0101: Ubiquitous Language Value Objects (AccountId, MoneyCents) & Synonym Drift Detector.
- REQ-0102: Software-Engineering Prompt Steerer (Andrew Ng's AI Engineering Skills Map Pillar 02).
- REQ-0103: Dual-Harness Permission Mode Mapper ('agy' and 'claude' -> 4 Autonomy Tiers).
- REQ-0104: Hard Floors Against Destructive Operations ('openworker' Tier 1 Invariant).
- REQ-0105: Reviewer Circuit Breaker & Unattended Self-Approval Guard.
- REQ-0106: Provenance Audit Trail ('auto-approved', 'user-approved', 'denied').
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any


ACCOUNT_ID_PATTERN = re.compile(r"^ACCT-[A-Z0-9]{4,12}$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")

SYNONYM_DRIFT_MAP: dict[str, str] = {
    "client_id": "debit_account_id",
    "cust_acct": "debit_account_id",
    "user_id": "debit_account_id",
    "acct_no": "debit_account_id",
    "tx_amt": "amount_cents",
    "amount_float": "amount_cents",
    "fee_float": "fee_cents",
    "ccy": "currency",
}

VALID_CONSISTENCY_MODELS = frozenset({
    "STRONG",
    "BOUNDED_STALENESS",
    "EVENTUAL_IDEMPOTENT",
})
VALID_RELIABILITY_STRATEGIES = frozenset({
    "IDEMPOTENCY_KEY_AND_RETRY",
    "CIRCUIT_BREAKER",
    "DEAD_LETTER_QUEUE",
})
VALID_SECURITY_BOUNDARIES = frozenset({
    "AUTHZ_AND_INPUT_VALIDATION",
    "MTLS_AND_RATE_LIMIT",
    "PARAMETERIZED_SQL",
})
VALID_MAINTAINABILITY_CONTRACTS = frozenset({
    "TYPED_INTERFACES",
    "BOUNDED_CONTEXT",
})

HARD_FLOOR_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f\b", re.IGNORECASE),
    re.compile(r"\bdrop\s+(table|database|schema)\b", re.IGNORECASE),
    re.compile(r"\bgit\s+push\s+.*--force\b", re.IGNORECASE),
    re.compile(r"\bgit\s+reset\s+--hard\b", re.IGNORECASE),
    re.compile(r"adversarial_tests", re.IGNORECASE),
    re.compile(r"(^|[\s/])\.env(\b|$)", re.IGNORECASE),
    re.compile(r"curl\s+.*\|\s*(ba)?sh\b", re.IGNORECASE),
    re.compile(r"\bchmod\s+777\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class AccountId:
  """Canonical Ubiquitous Language identifier for a ledger account (REQ-0101)."""

  value: str

  def __post_init__(self) -> None:
    if not isinstance(self.value, str) or not ACCOUNT_ID_PATTERN.match(self.value):
      raise ValueError(
          f"Invalid AccountId '{self.value}': must match ^ACCT-[A-Z0-9]{{4,12}}$"
      )


@dataclass(frozen=True)
class MoneyCents:
  """Exact integer minor-unit monetary value object (REQ-0101)."""

  amount_cents: int
  currency: str

  def __post_init__(self) -> None:
    if isinstance(self.amount_cents, bool) or not isinstance(self.amount_cents, int):
      raise TypeError("amount_cents must be an exact int (floats and bools are forbidden)")
    if self.amount_cents < 0:
      raise ValueError("amount_cents must be non-negative")
    if not isinstance(self.currency, str) or not CURRENCY_PATTERN.match(self.currency):
      raise ValueError(f"Invalid ISO currency '{self.currency}': must match ^[A-Z]{{3}}$")


def audit_ubiquitous_language(payload: dict[str, Any]) -> list[str]:
  """Detects synonym drift and float monetary fields in a request payload (REQ-0101)."""
  violations: list[str] = []
  for key, value in payload.items():
    if key in SYNONYM_DRIFT_MAP:
      canonical = SYNONYM_DRIFT_MAP[key]
      violations.append(
          f"Synonym drift on '{key}': use canonical Ubiquitous Language term '{canonical}'"
      )
    if isinstance(value, float):
      violations.append(
          f"Float monetary/numeric drift on '{key}': use exact integer minor units (MoneyCents)"
      )
  return violations


class SteeringStatus(str, Enum):
  """Classification of prompt steering readiness (REQ-0102)."""

  VIBE_UNDERSPECIFIED = "VIBE_UNDERSPECIFIED"
  PRODUCTION_STEERED = "PRODUCTION_STEERED"


@dataclass(frozen=True)
class EngineeringConstraints:
  """Explicit Pillar 02 Software Engineering constraints for steering an agent (REQ-0102)."""

  latency_ms_p99: int | None = None
  consistency_model: str | None = None
  reliability_strategy: str | None = None
  security_boundary: str | None = None
  maintainability_contract: str | None = None


@dataclass(frozen=True)
class PromptSteeringReport:
  """Result of evaluating a prompt against Pillar 02 engineering dimensions (REQ-0102)."""

  status: SteeringStatus
  steering_score: float
  missing_dimensions: tuple[str, ...]
  ubiquitous_language_violations: tuple[str, ...]
  compiled_prompt: str


def evaluate_prompt_steering(
    prompt_text: str,
    constraints: EngineeringConstraints | None = None,
    sample_payload: dict[str, Any] | None = None,
) -> PromptSteeringReport:
  """Evaluates a prompt against Andrew Ng's Pillar 02 Software Engineering dimensions (REQ-0102)."""
  if not prompt_text or not prompt_text.strip():
    raise ValueError("prompt_text must be non-empty")

  c = constraints or EngineeringConstraints()
  missing: list[str] = []

  if c.latency_ms_p99 is None or c.latency_ms_p99 <= 0:
    missing.append("latency_ms_p99")
  if c.consistency_model not in VALID_CONSISTENCY_MODELS:
    missing.append("consistency_model")
  if c.reliability_strategy not in VALID_RELIABILITY_STRATEGIES:
    missing.append("reliability_strategy")
  if c.security_boundary not in VALID_SECURITY_BOUNDARIES:
    missing.append("security_boundary")
  if c.maintainability_contract not in VALID_MAINTAINABILITY_CONTRACTS:
    missing.append("maintainability_contract")

  ul_violations = tuple(audit_ubiquitous_language(sample_payload or {}))
  satisfied_count = 5 - len(missing)
  score = round(satisfied_count / 5.0, 2)
  if ul_violations:
    score = max(0.0, round(score - 0.2 * len(ul_violations), 2))

  if not missing and not ul_violations:
    status = SteeringStatus.PRODUCTION_STEERED
    compiled = (
        f"{prompt_text.strip()}\n"
        f"[Engineering Constraints] "
        f"p99_latency_ms<={c.latency_ms_p99}; "
        f"consistency={c.consistency_model}; "
        f"reliability={c.reliability_strategy}; "
        f"security={c.security_boundary}; "
        f"maintainability={c.maintainability_contract}"
    )
  else:
    status = SteeringStatus.VIBE_UNDERSPECIFIED
    compiled = prompt_text.strip()

  return PromptSteeringReport(
      status=status,
      steering_score=score,
      missing_dimensions=tuple(missing),
      ubiquitous_language_violations=ul_violations,
      compiled_prompt=compiled,
  )


class AutonomyTier(str, Enum):
  """4-Tier Ladder of Earned Autonomy (REQ-0103)."""

  TIER_1_PLAN_OR_STRICT = "TIER_1_PLAN_OR_STRICT"
  TIER_2_MANUAL_REVIEW = "TIER_2_MANUAL_REVIEW"
  TIER_3_SANDBOX_AUTO_EDIT = "TIER_3_SANDBOX_AUTO_EDIT"
  TIER_4_GOVERNED_AUTO_LOOP = "TIER_4_GOVERNED_AUTO_LOOP"


@dataclass(frozen=True)
class HarnessPermissionProfile:
  """Normalized permission profile across Antigravity ('agy') and Claude Code ('claude')."""

  harness: str
  mode: str
  tier: AutonomyTier
  can_write_files: bool
  auto_approves_edits: bool
  requires_sandbox_for_shell: bool
  requires_reviewer_gate: bool


AGY_MODE_MAP: dict[str, HarnessPermissionProfile] = {
    "strict": HarnessPermissionProfile(
        harness="agy",
        mode="strict",
        tier=AutonomyTier.TIER_1_PLAN_OR_STRICT,
        can_write_files=False,
        auto_approves_edits=False,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=True,
    ),
    "request-review": HarnessPermissionProfile(
        harness="agy",
        mode="request-review",
        tier=AutonomyTier.TIER_2_MANUAL_REVIEW,
        can_write_files=True,
        auto_approves_edits=False,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=True,
    ),
    "proceed-in-sandbox": HarnessPermissionProfile(
        harness="agy",
        mode="proceed-in-sandbox",
        tier=AutonomyTier.TIER_3_SANDBOX_AUTO_EDIT,
        can_write_files=True,
        auto_approves_edits=True,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=False,
    ),
    "always-proceed": HarnessPermissionProfile(
        harness="agy",
        mode="always-proceed",
        tier=AutonomyTier.TIER_4_GOVERNED_AUTO_LOOP,
        can_write_files=True,
        auto_approves_edits=True,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=True,
    ),
}

CLAUDE_MODE_MAP: dict[str, HarnessPermissionProfile] = {
    "plan": HarnessPermissionProfile(
        harness="claude",
        mode="plan",
        tier=AutonomyTier.TIER_1_PLAN_OR_STRICT,
        can_write_files=False,
        auto_approves_edits=False,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=True,
    ),
    "default": HarnessPermissionProfile(
        harness="claude",
        mode="default",
        tier=AutonomyTier.TIER_2_MANUAL_REVIEW,
        can_write_files=True,
        auto_approves_edits=False,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=True,
    ),
    "acceptEdits": HarnessPermissionProfile(
        harness="claude",
        mode="acceptEdits",
        tier=AutonomyTier.TIER_3_SANDBOX_AUTO_EDIT,
        can_write_files=True,
        auto_approves_edits=True,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=False,
    ),
    "auto": HarnessPermissionProfile(
        harness="claude",
        mode="auto",
        tier=AutonomyTier.TIER_4_GOVERNED_AUTO_LOOP,
        can_write_files=True,
        auto_approves_edits=True,
        requires_sandbox_for_shell=True,
        requires_reviewer_gate=True,
    ),
}


def map_harness_permission_mode(harness: str, mode: str) -> HarnessPermissionProfile:
  """Maps an 'agy' or 'claude' permission mode to its canonical AutonomyTier profile (REQ-0103)."""
  norm_harness = harness.strip().lower()
  if norm_harness == "agy":
    if mode not in AGY_MODE_MAP:
      raise ValueError(f"Unsupported agy permission mode: '{mode}'")
    return AGY_MODE_MAP[mode]
  if norm_harness == "claude":
    if mode not in CLAUDE_MODE_MAP:
      raise ValueError(f"Unsupported claude permission mode: '{mode}'")
    return CLAUDE_MODE_MAP[mode]
  raise ValueError(f"Unsupported harness '{harness}': expected 'agy' or 'claude'")


def is_hard_floor_violation(command_or_target: str) -> bool:
  """Returns True if the command or file target violates a non-negotiable Hard Floor (REQ-0104)."""
  return any(pattern.search(command_or_target) for pattern in HARD_FLOOR_PATTERNS)


class GateDecision(str, Enum):
  """Outcome of evaluating a tool action through the EarnedAutonomyGate."""

  APPROVED = "APPROVED"
  HARD_FLOOR_BLOCKED = "HARD_FLOOR_BLOCKED"
  CIRCUIT_BREAKER_HALTED = "CIRCUIT_BREAKER_HALTED"
  UNATTENDED_SELF_APPROVAL_DENIED = "UNATTENDED_SELF_APPROVAL_DENIED"
  REVIEWER_DENIED = "REVIEWER_DENIED"
  PLAN_MODE_READ_ONLY_DENIED = "PLAN_MODE_READ_ONLY_DENIED"


@dataclass(frozen=True)
class AuditLogEntry:
  """Provenance-tagged audit record for every tool invocation (REQ-0106)."""

  action: str
  decision: GateDecision
  provenance: str  # "auto-approved" | "user-approved" | "denied"
  reason: str


@dataclass
class EarnedAutonomyGate:
  """4-Tier 'Governed by Design' execution gate with hard floors and circuit breaker (REQ-0104..0106)."""

  profile: HarnessPermissionProfile
  allowed_command_prefixes: tuple[str, ...] = (
      "python3 -m unittest",
      "./self_diagnose_all.sh",
      "./labs/",
      "git status",
      "git diff",
  )
  max_consecutive_denials: int = 3
  consecutive_denials: int = 0
  circuit_breaker_tripped: bool = False
  audit_log: list[AuditLogEntry] = field(default_factory=list)

  def _record(
      self,
      action: str,
      decision: GateDecision,
      provenance: str,
      reason: str,
      is_denial: bool,
  ) -> AuditLogEntry:
    if is_denial:
      self.consecutive_denials += 1
      if self.consecutive_denials >= self.max_consecutive_denials:
        self.circuit_breaker_tripped = True
    else:
      self.consecutive_denials = 0

    entry = AuditLogEntry(
        action=action,
        decision=decision,
        provenance=provenance,
        reason=reason,
    )
    self.audit_log.append(entry)
    return entry

  def reset_circuit_breaker(self, human_verified: bool = False) -> None:
    """Resets the circuit breaker only when explicitly confirmed by a human."""
    if not human_verified:
      raise PermissionError("Circuit breaker reset requires human_verified=True")
    self.consecutive_denials = 0
    self.circuit_breaker_tripped = False

  def evaluate_action(
      self,
      action: str,
      is_write_or_mutation: bool = False,
      user_explicitly_approved: bool = False,
      reviewer_approved: bool = True,
      unattended: bool = False,
  ) -> AuditLogEntry:
    """Evaluates a candidate tool action against 4-tier OpenWorker governance rules."""
    if self.circuit_breaker_tripped:
      return self._record(
          action=action,
          decision=GateDecision.CIRCUIT_BREAKER_HALTED,
          provenance="denied",
          reason="Reviewer circuit breaker is tripped after repeated denials; human reset required.",
          is_denial=True,
      )

    # Tier 1 Invariant: Hard floors can NEVER be bypassed, even with user or auto approval.
    if is_hard_floor_violation(action):
      return self._record(
          action=action,
          decision=GateDecision.HARD_FLOOR_BLOCKED,
          provenance="denied",
          reason=f"Hard floor violation blocked irreversible/protected action: '{action}'",
          is_denial=True,
      )

    # Plan / strict mode blocks all writes and mutations.
    if is_write_or_mutation and not self.profile.can_write_files:
      return self._record(
          action=action,
          decision=GateDecision.PLAN_MODE_READ_ONLY_DENIED,
          provenance="denied",
          reason=f"Mode '{self.profile.mode}' is read-only and forbids file/state mutations.",
          is_denial=True,
      )

    is_allowlisted = any(
        action.strip().startswith(prefix) for prefix in self.allowed_command_prefixes
    )

    # Unattended runs never self-approve unallowlisted commands.
    if unattended and not is_allowlisted:
      return self._record(
          action=action,
          decision=GateDecision.UNATTENDED_SELF_APPROVAL_DENIED,
          provenance="denied",
          reason="Unattended runs cannot self-approve commands outside the sandbox allowlist.",
          is_denial=True,
      )

    if not reviewer_approved:
      return self._record(
          action=action,
          decision=GateDecision.REVIEWER_DENIED,
          provenance="denied",
          reason="Independent reviewer check rejected the action.",
          is_denial=True,
      )

    if user_explicitly_approved:
      return self._record(
          action=action,
          decision=GateDecision.APPROVED,
          provenance="user-approved",
          reason="Explicitly approved by human engineer.",
          is_denial=False,
      )

    if is_allowlisted or self.profile.auto_approves_edits:
      return self._record(
          action=action,
          decision=GateDecision.APPROVED,
          provenance="auto-approved",
          reason=f"Auto-approved within governed tier {self.profile.tier.value}.",
          is_denial=False,
      )

    return self._record(
        action=action,
        decision=GateDecision.REVIEWER_DENIED,
        provenance="denied",
        reason=f"Mode '{self.profile.mode}' requires explicit human approval for non-allowlisted action.",
        is_denial=True,
    )
