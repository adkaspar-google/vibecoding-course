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

"""Immutable adversarial verifier for Lab 01 (REQ-0101 through REQ-0106)."""

from __future__ import annotations

import unittest

import prompt_steerer as ps


class TestLab01PromptSteererVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 01."""

  def test_req0101_ubiquitous_language_and_synonym_drift(self) -> None:
    """REQ-0101: Enforce AccountId, MoneyCents integer minor units, and synonym drift detection."""
    self.assertEqual(ps.AccountId("ACCT-1024XYZ").value, "ACCT-1024XYZ")
    with self.assertRaises(ValueError):
      ps.AccountId("client_99")

    self.assertEqual(ps.MoneyCents(1050, "EUR").amount_cents, 1050)
    with self.assertRaises(TypeError):
      ps.MoneyCents(10.50, "USD")  # type: ignore[arg-type]
    with self.assertRaises(TypeError):
      ps.MoneyCents(True, "USD")  # type: ignore[arg-type]

    violations = ps.audit_ubiquitous_language({"client_id": "ACCT-1000", "tx_amt": 19.99})
    self.assertGreaterEqual(len(violations), 2)
    self.assertTrue(any("client_id" in v for v in violations))
    self.assertTrue(any("float" in v.lower() for v in violations))

  def test_req0102_software_engineering_prompt_steerer(self) -> None:
    """REQ-0102: Contrast naive vibe prompt against Pillar 02 engineering-steered prompt."""
    vibe_report = ps.evaluate_prompt_steering("Build a fast checkout endpoint")
    self.assertEqual(vibe_report.status, ps.SteeringStatus.VIBE_UNDERSPECIFIED)
    self.assertEqual(len(vibe_report.missing_dimensions), 5)
    self.assertLess(vibe_report.steering_score, 0.5)

    steered_report = ps.evaluate_prompt_steering(
        "Implement ledger transfer handler with integer cents.",
        constraints=ps.EngineeringConstraints(
            latency_ms_p99=150,
            consistency_model="STRONG",
            reliability_strategy="IDEMPOTENCY_KEY_AND_RETRY",
            security_boundary="AUTHZ_AND_INPUT_VALIDATION",
            maintainability_contract="TYPED_INTERFACES",
        ),
        sample_payload={"debit_account_id": "ACCT-1234", "amount_cents": 5000},
    )
    self.assertEqual(steered_report.status, ps.SteeringStatus.PRODUCTION_STEERED)
    self.assertEqual(steered_report.steering_score, 1.0)
    self.assertEqual(steered_report.missing_dimensions, ())
    self.assertIn("p99_latency_ms<=150", steered_report.compiled_prompt)

  def test_req0103_dual_harness_permission_mode_mapping(self) -> None:
    """REQ-0103: Map Antigravity ('agy') and Claude Code ('claude') permission modes."""
    agy_plan = ps.map_harness_permission_mode("agy", "strict")
    claude_plan = ps.map_harness_permission_mode("claude", "plan")
    self.assertEqual(agy_plan.tier, ps.AutonomyTier.TIER_1_PLAN_OR_STRICT)
    self.assertEqual(claude_plan.tier, ps.AutonomyTier.TIER_1_PLAN_OR_STRICT)
    self.assertFalse(agy_plan.can_write_files)
    self.assertFalse(claude_plan.can_write_files)

    agy_profile = ps.map_harness_permission_mode("agy", "proceed-in-sandbox")
    claude_accept = ps.map_harness_permission_mode("claude", "acceptEdits")
    self.assertEqual(agy_profile.tier, ps.AutonomyTier.TIER_3_SANDBOX_AUTO_EDIT)
    self.assertEqual(claude_accept.tier, ps.AutonomyTier.TIER_3_SANDBOX_AUTO_EDIT)
    self.assertTrue(agy_profile.auto_approves_edits)

  def test_req0104_hard_floors_block_destructive_actions_in_any_mode(self) -> None:
    """REQ-0104: Hard floors block destructive actions even in 'always-proceed' or 'auto' mode."""
    auto_profile = ps.map_harness_permission_mode("agy", "always-proceed")
    gate = ps.EarnedAutonomyGate(profile=auto_profile)

    for dangerous in (
        "rm -rf /tmp/build",
        "psql -c 'DROP TABLE accounts;'",
        "git push origin main --force",
        "vim labs/lab_01/adversarial_tests/test_prompt_steerer_verifier.py",
        "cat .env",
    ):
      entry = gate.evaluate_action(
          dangerous,
          user_explicitly_approved=True,
          reviewer_approved=True,
      )
      self.assertEqual(entry.decision, ps.GateDecision.HARD_FLOOR_BLOCKED)
      self.assertEqual(entry.provenance, "denied")
      gate.reset_circuit_breaker(human_verified=True)

  def test_req0105_reviewer_circuit_breaker_and_unattended_guard(self) -> None:
    """REQ-0105: Trip circuit breaker after 3 denials and block unattended self-approval."""
    profile = ps.map_harness_permission_mode("claude", "auto")
    gate = ps.EarnedAutonomyGate(profile=profile, max_consecutive_denials=3)

    unattended_entry = gate.evaluate_action(
        "python3 scripts/migrate_prod.py",
        unattended=True,
    )
    self.assertEqual(
        unattended_entry.decision,
        ps.GateDecision.UNATTENDED_SELF_APPROVAL_DENIED,
    )

    gate.evaluate_action("python3 scripts/op1.py", reviewer_approved=False)
    gate.evaluate_action("python3 scripts/op2.py", reviewer_approved=False)
    self.assertTrue(gate.circuit_breaker_tripped)

    halted = gate.evaluate_action("git status", user_explicitly_approved=True)
    self.assertEqual(halted.decision, ps.GateDecision.CIRCUIT_BREAKER_HALTED)

    with self.assertRaises(PermissionError):
      gate.reset_circuit_breaker(human_verified=False)
    gate.reset_circuit_breaker(human_verified=True)
    self.assertFalse(gate.circuit_breaker_tripped)

  def test_req0106_provenance_audit_trail(self) -> None:
    """REQ-0106: Every evaluated action is logged with provenance ('auto-approved', 'user-approved', 'denied')."""
    profile = ps.map_harness_permission_mode("agy", "request-review")
    gate = ps.EarnedAutonomyGate(profile=profile)

    e1 = gate.evaluate_action("python3 -m unittest discover")
    e2 = gate.evaluate_action("python3 custom_script.py", user_explicitly_approved=True)
    e3 = gate.evaluate_action("rm -rf build/")

    self.assertEqual(e1.provenance, "auto-approved")
    self.assertEqual(e2.provenance, "user-approved")
    self.assertEqual(e3.provenance, "denied")
    self.assertEqual(len(gate.audit_log), 3)


if __name__ == "__main__":
  unittest.main()
