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

"""Immutable adversarial verifier for Lab 03 (REQ-0301 through REQ-0306)."""

from __future__ import annotations

import unittest

import reppit_orchestrator as ro


class TestLab03ReppitOrchestratorVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 03."""

  def test_req0301_task_complexity_to_workflow_rigor_classifier(self) -> None:
    """REQ-0301: Map task scope and ambiguity to Vanilla, Plan Mode, RePPIT, or Multi-Session Subagents."""
    self.assertEqual(ro.classify_workflow_rigor(1), ro.WorkflowRigor.VANILLA_PROMPT)
    self.assertEqual(ro.classify_workflow_rigor(2), ro.WorkflowRigor.SINGLE_PLAN_MODE)
    self.assertEqual(
        ro.classify_workflow_rigor(3, has_architectural_ambiguity=True),
        ro.WorkflowRigor.REPPIT_WORKFLOW,
    )
    self.assertEqual(
        ro.classify_workflow_rigor(12, is_cross_service_migration=True),
        ro.WorkflowRigor.MULTI_SESSION_SUBAGENTS,
    )

  def test_req0302_research_document_and_socratic_clarification_gate(self) -> None:
    """REQ-0302: Enforce file:line citations in Research and forbid premature solutions."""
    bad_research = "We should refactor the billing service to use event sourcing."
    bad_res = ro.validate_research_document(bad_research)
    self.assertFalse(bad_res.is_valid)
    self.assertTrue(bad_res.contains_premature_solution)

    good_research = (
        "Current request flow enters `api/routes.py:L18` and delegates to "
        "`domain/ledger.py:L64` where `SettlementBatch` validates balances."
    )
    good_res = ro.validate_research_document(good_research)
    self.assertTrue(good_res.is_valid)
    self.assertEqual(len(good_res.citations_found), 2)

    passed, remaining = ro.evaluate_clarification_gate(["Should refunds support partial cents?"])
    self.assertFalse(passed)
    self.assertEqual(len(remaining), 1)
    passed_clean, _ = ro.evaluate_clarification_gate([])
    self.assertTrue(passed_clean)

  def test_req0303_orthogonal_proposals_and_post_proposal_context_reset(self) -> None:
    """REQ-0303: Require 2 orthogonal proposals and purge rejected proposal tokens on selection."""
    p1 = ro.ArchitecturalProposal(
        proposal_id="P1",
        title="Pessimistic Row Locking",
        mechanism_axis="database_pessimistic_lock",
        summary="Use SELECT FOR UPDATE in SQLite/Postgres.",
        tradeoffs=("Zero retry waste under contention", "Higher lock wait latency"),
    )
    p2_clone = ro.ArchitecturalProposal(
        proposal_id="P2",
        title="Another Row Lock",
        mechanism_axis="database_pessimistic_lock",
        summary="Same axis.",
        tradeoffs=("Same tradeoff",),
    )
    ok_clone, _ = ro.validate_orthogonal_proposals(p1, p2_clone)
    self.assertFalse(ok_clone)

    p2_ortho = ro.ArchitecturalProposal(
        proposal_id="P2",
        title="Optimistic Version Counter",
        mechanism_axis="optimistic_concurrency_version",
        summary="Compare-and-swap on version column.",
        tradeoffs=("Lock-free reads", "Requires retry on write collision"),
    )
    ok_ortho, issues = ro.validate_orthogonal_proposals(p1, p2_ortho)
    self.assertTrue(ok_ortho, msg=str(issues))

    reset_state = ro.select_proposal_and_reset_context(
        "Current ledger is in `domain/ledger.py:L40`.",
        p1,
        p2_ortho,
        selected_id="P2",
    )
    self.assertEqual(reset_state.selected_proposal_id, "P2")
    self.assertEqual(reset_state.purged_proposal_id, "P1")
    joined = "\n".join(reset_state.compacted_messages)
    self.assertIn("Optimistic Version Counter", joined)
    self.assertNotIn("Pessimistic Row Locking", joined)
    self.assertGreater(reset_state.tokens_saved, 5)

  def test_req0304_plan_guardrail_validator_out_of_scope(self) -> None:
    """REQ-0304: Require file:line targets, verification command, and Out of Scope / Do NOT Touch section."""
    bad_plan = "# Plan\nEdit `domain/ledger.py:L40` and run `python3 -m unittest`."
    self.assertFalse(ro.validate_implementation_plan(bad_plan).is_valid)

    good_plan = (
        "# Implementation Plan\n"
        "1. Update `domain/ledger.py:L40` to check version counter.\n"
        "## Out of Scope / Do NOT Touch\n"
        "- Do not modify `legacy/auth.py` or `adversarial_tests/`.\n"
        "## Verification\n"
        "- Run `CI=true python3 -m unittest discover -v`.\n"
    )
    res = ro.validate_implementation_plan(good_plan)
    self.assertTrue(res.is_valid)
    self.assertTrue(res.has_out_of_scope_section)
    self.assertTrue(res.has_verification_command)

  def test_req0305_phase_based_model_router(self) -> None:
    """REQ-0305: Route Research/Propose/Plan to frontier reasoning models and Implement/Verify to fast models."""
    r_agy = ro.route_model_for_reppit_phase(ro.ReppitPhase.PLAN, harness="agy")
    i_agy = ro.route_model_for_reppit_phase(ro.ReppitPhase.IMPLEMENT, harness="agy")
    self.assertEqual(r_agy.tier, "frontier_reasoning")
    self.assertEqual(i_agy.tier, "fast_execution")
    self.assertNotEqual(r_agy.model_id, i_agy.model_id)

    r_claude = ro.route_model_for_reppit_phase(ro.ReppitPhase.PROPOSE, harness="claude")
    i_claude = ro.route_model_for_reppit_phase(ro.ReppitPhase.TEST_VERIFY, harness="claude")
    self.assertEqual(r_claude.tier, "frontier_reasoning")
    self.assertEqual(i_claude.tier, "fast_execution")

  def test_req0306_reflection_cycle_and_walkthrough_receipt(self) -> None:
    """REQ-0306: Execute Generate -> Reflect -> Refine and validate Walkthrough Run Receipt."""
    draft = "def calc(x):\n  try:\n    return float(x)\n  except Exception: pass\n"
    reflected = ro.run_reflection_cycle(draft)
    self.assertTrue(reflected.converged)
    self.assertGreaterEqual(len(reflected.critique_findings), 2)
    self.assertNotIn("float(", reflected.refined_code)

    good_receipt = ro.WalkthroughReceipt(
        files_modified=("domain/ledger.py", "tests/test_ledger.py"),
        test_command="CI=true python3 -m unittest",
        test_exit_code=0,
        browser_or_behavioral_check="Verified 200 OK JSON settlement response in /browser.",
    )
    ok, errs = ro.validate_walkthrough_receipt(
        good_receipt,
        do_not_touch_files=("legacy/auth.py",),
    )
    self.assertTrue(ok, msg=str(errs))

    bad_receipt = ro.WalkthroughReceipt(
        files_modified=("domain/ledger.py", "legacy/auth.py"),
        test_command="CI=true python3 -m unittest",
        test_exit_code=0,
        browser_or_behavioral_check="Checked UI",
    )
    ok_bad, errs_bad = ro.validate_walkthrough_receipt(
        bad_receipt,
        do_not_touch_files=("legacy/auth.py",),
    )
    self.assertFalse(ok_bad)
    self.assertTrue(any("Scope creep" in e for e in errs_bad))


if __name__ == "__main__":
  unittest.main()
