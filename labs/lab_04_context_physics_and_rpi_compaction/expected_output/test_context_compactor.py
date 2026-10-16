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

"""Unit tests for Lab 04 context_compactor.py (REQ-0401 through REQ-0406)."""

from __future__ import annotations

import unittest

import context_compactor as cc


class TestContextCompactor(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 04 (REQ-0401..REQ-0406)."""

  def test_req0401_context_window_physics_and_dumb_zone_classifier(self) -> None:
    """Verifies REQ-0401: Context Window Physics and 40% Dumb Zone Classifier."""
    smart = cc.profile_context_window(50_000, 200_000)
    dumb = cc.profile_context_window(95_000, 200_000)
    self.assertEqual(smart.zone, cc.ContextZone.SMART_ZONE)
    self.assertFalse(smart.requires_compaction)
    self.assertEqual(dumb.zone, cc.ContextZone.DUMB_ZONE)
    self.assertTrue(dumb.requires_compaction)

  def test_req0402_autoresearch_output_redirection_backpressure(self) -> None:
    """Verifies REQ-0402: karpathy/autoresearch Output-Redirection Backpressure (> run.log 2>&1 and metric grep)."""
    cmd = cc.rewrite_command_with_backpressure("uv run train.py | tee train.out", log_file="run.log")
    self.assertEqual(cmd, "uv run train.py > run.log 2>&1")

    raw_log = "step 1\nstep 2\nval_bpb: 0.981000\npeak_vram_mb: 12000.0\n"
    extracted = cc.extract_backpressure_summary(raw_log)
    self.assertFalse(extracted.crashed)
    self.assertEqual(extracted.extracted_lines, ("val_bpb: 0.981000", "peak_vram_mb: 12000.0"))

  def test_req0403_sandboxed_side_query_pruning(self) -> None:
    """Verifies REQ-0403: Sandboxed Side-Query Pruning (/btw pattern) leaves active_history unchanged."""
    history = [{"role": "user", "content": "Implement TaskFlow settlement"}]
    reply, after = cc.execute_sandboxed_side_query(history, "What flag runs verbose tests?", "Use -v")
    self.assertIn("-v", reply)
    self.assertEqual(after, history)

  def test_req0404_rendergit_cxml_repository_packer(self) -> None:
    """Verifies REQ-0404: karpathy/rendergit CXML Repository Packer filters __pycache__ and .venv."""
    cxml = cc.render_repo_cxml({
        "src/taskflow.py": "print('ok')\n",
        "src/__pycache__/taskflow.pyc": "binary",
    })
    self.assertIn("<source>src/taskflow.py</source>", cxml)
    self.assertNotIn("__pycache__", cxml)

  def test_req0405_frequent_intentional_compaction_rpi_engine(self) -> None:
    """Verifies REQ-0405: Frequent Intentional Compaction (RPI) Handoff Engine achieves >=80% token reduction."""
    bundle = cc.compact_exploration_to_rpi_artifacts(
        noisy_turns=["grep dump " * 200 for _ in range(20)],
        verified_findings=["`src/ledger.py:L10-L30` validates MoneyCents."],
        plan_steps=["Update `src/routes.py:L40-L55` to check idempotency key."],
        out_of_scope=["adversarial_tests/"],
    )
    self.assertGreaterEqual(bundle.compression_ratio, 0.80)
    self.assertIn("`src/ledger.py:L10-L30`", bundle.research_md)

  def test_req0406_human_leverage_pyramid_defect_amplification(self) -> None:
    """Verifies REQ-0406: Human Leverage Pyramid Defect Amplification Estimator (1000x, 100x, 1x)."""
    self.assertEqual(cc.estimate_defect_amplification("RESEARCH", 3), 3000)
    self.assertEqual(cc.estimate_defect_amplification("PLAN", 3), 300)
    self.assertEqual(cc.estimate_defect_amplification("CODE", 3), 3)


if __name__ == "__main__":
  unittest.main()
