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

"""Unit tests for Lab 08 autoresearch_harness.py (REQ-0801 through REQ-0806)."""

from __future__ import annotations

import unittest

import autoresearch_harness as ah


class TestAutoresearchHarness(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 08 (REQ-0801..REQ-0806)."""

  def test_req0801_cybernetic_matrix_and_pre_tool_use_exit_code_2_gate(self) -> None:
    """Verifies REQ-0801: 2x2 Cybernetic Control Matrix Classifier and PreToolUse Exit-Code-2 Gate."""
    self.assertEqual(
        ah.classify_cybernetic_control(True, True),
        ah.CyberneticQuadrant.COMPUTATIONAL_GUIDE,
    )
    blocked = ah.pre_tool_use_exit_code_gate("Edit", "prepare.py")
    allowed = ah.pre_tool_use_exit_code_gate("Edit", "train.py")
    self.assertEqual(blocked.exit_code, 2)
    self.assertEqual(allowed.exit_code, 0)

  def test_req0802_remediation_aware_structural_linter(self) -> None:
    """Verifies REQ-0802: OpenAI Remediation-Aware Structural Linter ([VIOLATION] -> [WHY] -> [HOW TO FIX])."""
    diags = ah.lint_architecture_with_remediation(
        source_file="domain/ledger.py",
        imported_modules=["infra/http_client.py"],
        allowed_layer_imports={"domain": {"domain"}},
    )
    self.assertEqual(len(diags), 1)
    self.assertIn("[VIOLATION]", diags[0])
    self.assertIn("[WHY]", diags[0])
    self.assertIn("[HOW TO FIX]", diags[0])

  def test_req0803_front_loaded_program_design_verifier(self) -> None:
    """Verifies REQ-0803: Dex Horthy's Front-Loaded Program Design Verifier (Ib5GBkD555M)."""
    aligned = ah.verify_front_loaded_program_design(
        module_type_signatures={"domain/ledger.py": "def settle(batch: Batch) -> Receipt"},
        call_graph_edges=[("service/checkout.py", "domain/ledger.py")],
        forbidden_edges={("domain/ledger.py", "ui/views.py")},
    )
    self.assertTrue(aligned.is_aligned)

  def test_req0804_autoresearch_three_file_boundary_validator(self) -> None:
    """Verifies REQ-0804: Karpathy's autoresearch 3-File Harness Boundary Validator (only train.py mutable)."""
    ok, _ = ah.validate_autoresearch_file_mutation(["train.py"])
    bad, _ = ah.validate_autoresearch_file_mutation(["train.py", "prepare.py"])
    self.assertTrue(ok)
    self.assertFalse(bad)

  def test_req0805_simplicity_criterion_and_git_keep_or_revert_ratchet(self) -> None:
    """Verifies REQ-0805: Karpathy's Simplicity Criterion and Automated Git Keep-or-Revert Ratchet."""
    keep_del = ah.evaluate_autoresearch_ratchet(0.990, 0.989, loc_delta=-8)
    self.assertEqual(keep_del.decision, ah.RatchetDecision.KEEP_SIMPLIFICATION)

    reject_bloat = ah.evaluate_autoresearch_ratchet(0.990, 0.9895, loc_delta=25)
    self.assertEqual(reject_bloat.decision, ah.RatchetDecision.REVERT_COMPLEXITY_BLOAT)

  def test_req0806_results_tsv_experiment_ledger_formatter(self) -> None:
    """Verifies REQ-0806: Untracked results.tsv Experiment Ledger Formatter."""
    row = ah.format_results_tsv_row(
        commit_sha="a1b2c3d",
        val_bpb=0.989000,
        peak_vram_mb=14200.0,
        loc_delta=-8,
        decision=ah.RatchetDecision.KEEP_SIMPLIFICATION,
    )
    cols = row.split("\t")
    self.assertEqual(len(cols), 6)
    self.assertEqual(cols[4], "keep")


if __name__ == "__main__":
  unittest.main()
