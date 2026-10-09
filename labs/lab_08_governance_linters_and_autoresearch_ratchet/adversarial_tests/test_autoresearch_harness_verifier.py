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

"""Immutable adversarial verifier for Lab 08 (REQ-0801 through REQ-0806)."""

from __future__ import annotations

import unittest

import autoresearch_harness as ah


class TestLab08AutoresearchHarnessVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 08."""

  def test_req0801_cybernetic_matrix_and_pre_tool_use_exit_code_2_gate(self) -> None:
    """REQ-0801: Classify 2x2 Cybernetic controls and return exit_code=2 on immutable harness edits."""
    self.assertEqual(
        ah.classify_cybernetic_control(True, True),
        ah.CyberneticQuadrant.COMPUTATIONAL_GUIDE,
    )
    self.assertEqual(
        ah.classify_cybernetic_control(True, False),
        ah.CyberneticQuadrant.INFERENTIAL_GUIDE,
    )
    self.assertEqual(
        ah.classify_cybernetic_control(False, True),
        ah.CyberneticQuadrant.COMPUTATIONAL_SENSOR,
    )
    self.assertEqual(
        ah.classify_cybernetic_control(False, False),
        ah.CyberneticQuadrant.INFERENTIAL_SENSOR,
    )

    blocked_prepare = ah.pre_tool_use_exit_code_gate("Edit", "prepare.py")
    self.assertEqual(blocked_prepare.exit_code, 2)
    self.assertEqual(blocked_prepare.provenance, "denied")

    blocked_tests = ah.pre_tool_use_exit_code_gate(
        "Write",
        "labs/lab_08/adversarial_tests/test_autoresearch_harness_verifier.py",
    )
    self.assertEqual(blocked_tests.exit_code, 2)

    allowed_train = ah.pre_tool_use_exit_code_gate("Edit", "train.py")
    self.assertEqual(allowed_train.exit_code, 0)
    self.assertEqual(allowed_train.provenance, "auto-approved")

  def test_req0802_remediation_aware_structural_linter(self) -> None:
    """REQ-0802: Emit [VIOLATION] ... [WHY] ... [HOW TO FIX] remediation recipes on layer violations."""
    allowed_map = {
        "domain": {"domain"},
        "service": {"domain", "service"},
    }
    diags = ah.lint_architecture_with_remediation(
        source_file="domain/ledger.py",
        imported_modules=["domain/models.py", "infra/postgres_client.py"],
        allowed_layer_imports=allowed_map,
    )
    self.assertEqual(len(diags), 1)
    msg = diags[0]
    self.assertIn("[VIOLATION]", msg)
    self.assertIn("[WHY]", msg)
    self.assertIn("[HOW TO FIX]", msg)
    self.assertIn("infra/postgres_client.py", msg)

  def test_req0803_front_loaded_program_design_verifier(self) -> None:
    """REQ-0803: Verify explicit non-Any type signatures and call-tree alignment before vertical slicing."""
    bad = ah.verify_front_loaded_program_design(
        module_type_signatures={
            "domain/ledger.py": "def settle(batch: Any) -> Any",
        },
        call_graph_edges=[("domain/ledger.py", "ui/views.py")],
        forbidden_edges={("domain/ledger.py", "ui/views.py")},
    )
    self.assertFalse(bad.is_aligned)
    self.assertEqual(bad.untyped_modules, ("domain/ledger.py",))
    self.assertEqual(len(bad.violated_call_edges), 1)

    good = ah.verify_front_loaded_program_design(
        module_type_signatures={
            "domain/ledger.py": "def settle(batch: SettlementBatch) -> SettlementReceipt",
        },
        call_graph_edges=[("service/checkout.py", "domain/ledger.py")],
        forbidden_edges={("domain/ledger.py", "ui/views.py")},
    )
    self.assertTrue(good.is_aligned, msg=str(good.errors))

  def test_req0804_autoresearch_three_file_boundary_validator(self) -> None:
    """REQ-0804: Allow mutations only to train.py; forbid prepare.py and program.md."""
    ok, errs = ah.validate_autoresearch_file_mutation(["train.py"])
    self.assertTrue(ok, msg=str(errs))

    bad, errs_bad = ah.validate_autoresearch_file_mutation(["train.py", "prepare.py"])
    self.assertFalse(bad)
    self.assertTrue(any("prepare.py" in e for e in errs_bad))

  def test_req0805_simplicity_criterion_and_git_keep_or_revert_ratchet(self) -> None:
    """REQ-0805: Enforce Simplicity Criterion (reject tiny gain with high LOC bloat; keep code deletion)."""
    # 1. Crash -> revert
    crashed = ah.evaluate_autoresearch_ratchet(0.995, 0.980, loc_delta=2, crashed=True)
    self.assertEqual(crashed.decision, ah.RatchetDecision.REVERT_GIT_RESET)
    self.assertEqual(crashed.git_action, "git reset --hard HEAD~1")

    # 2. Worse val_bpb -> revert
    regressed = ah.evaluate_autoresearch_ratchet(0.995, 0.999, loc_delta=-5)
    self.assertEqual(regressed.decision, ah.RatchetDecision.REVERT_GIT_RESET)

    # 3. Tiny gain (0.0008 < 0.002) that adds +22 LOC (>10) -> reject complexity bloat!
    bloat = ah.evaluate_autoresearch_ratchet(0.9950, 0.9942, loc_delta=22)
    self.assertEqual(bloat.decision, ah.RatchetDecision.REVERT_COMPLEXITY_BLOAT)
    self.assertEqual(bloat.git_action, "git reset --hard HEAD~1")

    # 4. Tiny gain (0.001) or equal metric that DELETES code (-12 LOC) -> keep simplification!
    simplification = ah.evaluate_autoresearch_ratchet(0.9950, 0.9940, loc_delta=-12)
    self.assertEqual(simplification.decision, ah.RatchetDecision.KEEP_SIMPLIFICATION)
    self.assertEqual(simplification.git_action, "keep_commit")

    # 5. Substantial gain (0.006 >= 0.002) with modest +6 LOC -> keep improvement!
    clean_win = ah.evaluate_autoresearch_ratchet(0.9950, 0.9890, loc_delta=6)
    self.assertEqual(clean_win.decision, ah.RatchetDecision.KEEP_IMPROVEMENT)
    self.assertEqual(clean_win.git_action, "keep_commit")

  def test_req0806_results_tsv_formatter(self) -> None:
    """REQ-0806: Format deterministic tab-separated results.tsv row."""
    row = ah.format_results_tsv_row(
        commit_sha="a1b2c3d",
        val_bpb=0.989000,
        peak_vram_mb=14200.0,
        loc_delta=-8,
        decision=ah.RatchetDecision.KEEP_SIMPLIFICATION,
    )
    cols = row.split("\t")
    self.assertEqual(len(cols), 6)
    self.assertEqual(cols[0], "a1b2c3d")
    self.assertEqual(cols[4], "keep")


if __name__ == "__main__":
  unittest.main()
