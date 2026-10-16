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

"""Unit tests for Lab 01 prompt_steerer.py (REQ-0101 through REQ-0106)."""

from __future__ import annotations

import unittest

import prompt_steerer as ps


class TestPromptSteerer(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 01 (REQ-0101..REQ-0106)."""

  def test_req0101_ubiquitous_language_and_synonym_drift(self) -> None:
    """Verifies REQ-0101: Ubiquitous Language Value Objects (AccountId, MoneyCents) and synonym drift detection."""
    acct = ps.AccountId("ACCT-9001A")
    money = ps.MoneyCents(2500, "USD")
    self.assertEqual(acct.value, "ACCT-9001A")
    self.assertEqual(money.amount_cents, 2500)
    with self.assertRaises(TypeError):
      ps.MoneyCents(25.00, "USD")  # type: ignore[arg-type]

    violations = ps.audit_ubiquitous_language({"client_id": "ACCT-9001A", "tx_amt": 25.0})
    self.assertEqual(len(violations), 3)

  def test_req0102_software_engineering_prompt_steerer(self) -> None:
    """Verifies REQ-0102: Software-Engineering Prompt Steerer across all 5 Pillar 02 dimensions."""
    unsteered = ps.evaluate_prompt_steering("Make TaskFlow checkout fast")
    self.assertEqual(unsteered.status, ps.SteeringStatus.VIBE_UNDERSPECIFIED)
    self.assertEqual(len(unsteered.missing_dimensions), 5)

    constraints = ps.EngineeringConstraints(
        latency_ms_p99=120,
        consistency_model="STRONG",
        reliability_strategy="IDEMPOTENCY_KEY_AND_RETRY",
        security_boundary="AUTHZ_AND_INPUT_VALIDATION",
        maintainability_contract="TYPED_INTERFACES",
    )
    report = ps.evaluate_prompt_steering(
        "Implement idempotent TaskFlow ledger settlement endpoint.",
        constraints=constraints,
        sample_payload={"debit_account_id": "ACCT-9001A", "amount_cents": 2500},
    )
    self.assertEqual(report.status, ps.SteeringStatus.PRODUCTION_STEERED)
    self.assertEqual(report.steering_score, 1.0)

  def test_req0103_dual_harness_permission_mode_mapper(self) -> None:
    """Verifies REQ-0103: Dual-Harness Permission Mode Mapper across 'agy' and 'claude'."""
    agy_strict = ps.map_harness_permission_mode("agy", "strict")
    claude_plan = ps.map_harness_permission_mode("claude", "plan")
    self.assertEqual(agy_strict.tier, ps.AutonomyTier.TIER_1_PLAN_OR_STRICT)
    self.assertEqual(claude_plan.tier, ps.AutonomyTier.TIER_1_PLAN_OR_STRICT)
    self.assertFalse(agy_strict.can_write_files)

    agy_sbx = ps.map_harness_permission_mode("agy", "proceed-in-sandbox")
    claude_accept = ps.map_harness_permission_mode("claude", "acceptEdits")
    self.assertEqual(agy_sbx.tier, ps.AutonomyTier.TIER_3_SANDBOX_AUTO_EDIT)
    self.assertEqual(claude_accept.tier, ps.AutonomyTier.TIER_3_SANDBOX_AUTO_EDIT)

  def test_req0104_hard_floors_against_destructive_operations(self) -> None:
    """Verifies REQ-0104: Hard Floors block destructive commands and protected targets in any mode."""
    gate = ps.EarnedAutonomyGate(profile=ps.map_harness_permission_mode("agy", "always-proceed"))
    entry = gate.evaluate_action("rm -rf /tmp/taskflow", user_explicitly_approved=True)
    self.assertEqual(entry.decision, ps.GateDecision.HARD_FLOOR_BLOCKED)
    self.assertEqual(entry.provenance, "denied")

  def test_req0105_reviewer_circuit_breaker_and_unattended_guard(self) -> None:
    """Verifies REQ-0105: Reviewer Circuit Breaker trips after 3 consecutive denials and blocks unattended unallowlisted commands."""
    gate = ps.EarnedAutonomyGate(
        profile=ps.map_harness_permission_mode("claude", "auto"),
        max_consecutive_denials=3,
    )
    unattended = gate.evaluate_action("python3 scripts/deploy.py", unattended=True)
    self.assertEqual(unattended.decision, ps.GateDecision.UNATTENDED_SELF_APPROVAL_DENIED)
    gate.evaluate_action("python3 scripts/op1.py", reviewer_approved=False)
    gate.evaluate_action("python3 scripts/op2.py", reviewer_approved=False)
    self.assertTrue(gate.circuit_breaker_tripped)

    halted = gate.evaluate_action("git status", user_explicitly_approved=True)
    self.assertEqual(halted.decision, ps.GateDecision.CIRCUIT_BREAKER_HALTED)

  def test_req0106_provenance_audit_trail(self) -> None:
    """Verifies REQ-0106: Provenance Audit Trail records 'auto-approved', 'user-approved', and 'denied' decisions."""
    gate = ps.EarnedAutonomyGate(profile=ps.map_harness_permission_mode("agy", "request-review"))
    e_auto = gate.evaluate_action("git status")
    e_user = gate.evaluate_action("python3 migrate.py", user_explicitly_approved=True)
    e_deny = gate.evaluate_action("cat .env")
    self.assertEqual(e_auto.provenance, "auto-approved")
    self.assertEqual(e_user.provenance, "user-approved")
    self.assertEqual(e_deny.provenance, "denied")
    self.assertEqual(len(gate.audit_log), 3)


if __name__ == "__main__":
  unittest.main()
