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

"""Unit tests for Lab 03 reppit_orchestrator.py (REQ-0301 through REQ-0306)."""

from __future__ import annotations

import unittest

import reppit_orchestrator as ro


class TestReppitOrchestrator(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 03 (REQ-0301..REQ-0306)."""

  def test_req0301_task_complexity_to_workflow_rigor_classifier(self) -> None:
    """Verifies REQ-0301: Task Complexity vs. Workflow Rigor Classifier across all 4 tiers."""
    self.assertEqual(ro.classify_workflow_rigor(1), ro.WorkflowRigor.VANILLA_PROMPT)
    self.assertEqual(ro.classify_workflow_rigor(2), ro.WorkflowRigor.SINGLE_PLAN_MODE)
    self.assertEqual(
        ro.classify_workflow_rigor(5, has_architectural_ambiguity=True),
        ro.WorkflowRigor.REPPIT_WORKFLOW,
    )
    self.assertEqual(
        ro.classify_workflow_rigor(10, is_cross_service_migration=True),
        ro.WorkflowRigor.MULTI_SESSION_SUBAGENTS,
    )

  def test_req0302_research_document_and_socratic_clarification_gate(self) -> None:
    """Verifies REQ-0302: Read-Only Research Validator and Socratic Clarification Gate (/grill-me)."""
    res = ro.validate_research_document(
        "TaskFlow invoice routing enters `api/routes.py:L18` and settles in `domain/ledger.py:L64`."
    )
    self.assertTrue(res.is_valid)
    self.assertEqual(len(res.citations_found), 2)

    passed, remaining = ro.evaluate_clarification_gate(["Should TaskFlow support partial refunds?"])
    self.assertFalse(passed)
    self.assertEqual(len(remaining), 1)

  def test_req0303_orthogonal_proposals_and_post_proposal_context_reset(self) -> None:
    """Verifies REQ-0303: Orthogonal Proposal Validator and Post-Proposal Context Reset."""
    pa = ro.ArchitecturalProposal(
        proposal_id="A",
        title="Server-Side Idempotency Table",
        mechanism_axis="server_side_storage",
        summary="Persist idempotency keys in SQLite.",
        tradeoffs=("Requires DB write lock", "Strong replay protection"),
    )
    pb = ro.ArchitecturalProposal(
        proposal_id="B",
        title="Client-Signed Stateless Nonce",
        mechanism_axis="client_stateless_hmac",
        summary="Validate HMAC timestamp token at edge.",
        tradeoffs=("Zero DB reads", "Susceptible to replay within clock skew window"),
    )
    state = ro.select_proposal_and_reset_context("ledger.py:L14 settles batches.", pa, pb, "A")
    self.assertEqual(state.selected_proposal_id, "A")
    self.assertEqual(state.purged_proposal_id, "B")
    self.assertNotIn("Client-Signed Stateless Nonce", "\n".join(state.compacted_messages))

  def test_req0304_plan_guardrail_validator_with_out_of_scope(self) -> None:
    """Verifies REQ-0304: Plan Guardrail Validator requiring file:line targets and Out of Scope section."""
    plan_md = (
        "# TaskFlow Plan\n"
        "1. Update `domain/ledger.py:L40`.\n"
        "## Out of Scope / Do NOT Touch\n"
        "- Do not modify `legacy/auth.py`.\n"
        "## Verification\n"
        "- Run `python3 -m unittest`.\n"
    )
    res = ro.validate_implementation_plan(plan_md)
    self.assertTrue(res.is_valid)
    self.assertTrue(res.has_out_of_scope_section)
    self.assertTrue(res.has_verification_command)

  def test_req0305_phase_based_model_router(self) -> None:
    """Verifies REQ-0305: Phase-Based Model Router selects frontier models for planning and fast models for implementation."""
    plan_route = ro.route_model_for_reppit_phase(ro.ReppitPhase.PLAN, harness="agy")
    impl_route = ro.route_model_for_reppit_phase(ro.ReppitPhase.IMPLEMENT, harness="agy")
    self.assertEqual(plan_route.tier, "frontier_reasoning")
    self.assertEqual(impl_route.tier, "fast_execution")

  def test_req0306_reflection_cycle_and_walkthrough_receipt_verifier(self) -> None:
    """Verifies REQ-0306: Generate -> Reflect -> Refine cycle and Walkthrough Receipt Verifier."""
    reflected = ro.run_reflection_cycle("def calc(x):\n  return float(x)\n")
    self.assertTrue(reflected.converged)
    self.assertNotIn("float(", reflected.refined_code)

    receipt = ro.WalkthroughReceipt(
        files_modified=("domain/ledger.py",),
        test_command="python3 -m unittest",
        test_exit_code=0,
        browser_or_behavioral_check="Verified 200 OK settlement response.",
    )
    ok, errs = ro.validate_walkthrough_receipt(receipt, do_not_touch_files=("legacy/auth.py",))
    self.assertTrue(ok, msg=str(errs))


if __name__ == "__main__":
  unittest.main()
