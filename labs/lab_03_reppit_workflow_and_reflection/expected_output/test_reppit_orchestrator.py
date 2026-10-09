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

"""Unit tests for Lab 03 reppit_orchestrator.py."""

from __future__ import annotations

import unittest

import reppit_orchestrator as ro


class TestReppitOrchestrator(unittest.TestCase):
  """User unit tests for Lab 03."""

  def test_workflow_rigor_and_context_reset(self) -> None:
    self.assertEqual(ro.classify_workflow_rigor(1), ro.WorkflowRigor.VANILLA_PROMPT)
    self.assertEqual(
        ro.classify_workflow_rigor(5, has_architectural_ambiguity=True),
        ro.WorkflowRigor.REPPIT_WORKFLOW,
    )

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


if __name__ == "__main__":
  unittest.main()
