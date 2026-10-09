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

"""Immutable adversarial verifier for Lab 04 (REQ-0401 through REQ-0406)."""

from __future__ import annotations

import unittest

import context_compactor as cc


class TestLab04ContextCompactorVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 04."""

  def test_req0401_smart_zone_vs_40_percent_dumb_zone(self) -> None:
    """REQ-0401: Classify <=40% utilization as SMART_ZONE and >40% as DUMB_ZONE."""
    p_smart = cc.profile_context_window(80_000, max_window_tokens=200_000)
    self.assertEqual(p_smart.utilization_ratio, 0.40)
    self.assertEqual(p_smart.zone, cc.ContextZone.SMART_ZONE)
    self.assertFalse(p_smart.requires_compaction)

    p_dumb = cc.profile_context_window(82_000, max_window_tokens=200_000)
    self.assertGreater(p_dumb.utilization_ratio, 0.40)
    self.assertEqual(p_dumb.zone, cc.ContextZone.DUMB_ZONE)
    self.assertTrue(p_dumb.requires_compaction)

  def test_req0402_autoresearch_output_redirection_backpressure(self) -> None:
    """REQ-0402: Redirect noisy commands to run.log and extract only key metrics or crash tail."""
    cmd = cc.rewrite_command_with_backpressure("uv run train.py | tee train.out", log_file="run.log")
    self.assertEqual(cmd, "uv run train.py > run.log 2>&1")

    noisy_log = "\n".join(
        [f"step {i}: loss=2.{i}" for i in range(500)]
        + ["val_bpb: 0.984200", "peak_vram_mb: 14210.5"]
    )
    summary = cc.extract_backpressure_summary(noisy_log)
    self.assertFalse(summary.crashed)
    self.assertEqual(summary.raw_line_count, 502)
    self.assertEqual(summary.extracted_lines, ("val_bpb: 0.984200", "peak_vram_mb: 14210.5"))

    crash_log = "\n".join(
        [f"step {i}" for i in range(100)]
        + ["Traceback (most recent call last):", "  File 'train.py', line 92", "RuntimeError: OOM"]
    )
    crash_summary = cc.extract_backpressure_summary(crash_log, tail_lines_on_crash=5)
    self.assertTrue(crash_summary.crashed)
    self.assertEqual(crash_summary.extracted_line_count, 5)
    self.assertIn("RuntimeError: OOM", crash_summary.extracted_lines[-1])

  def test_req0403_sandboxed_side_query_does_not_pollute_history(self) -> None:
    """REQ-0403: Execute /btw side-query without adding tokens to active_history."""
    history = [{"role": "user", "content": "Implement ledger settlement"}]
    reply, after_history = cc.execute_sandboxed_side_query(
        history,
        question="What flag enables verbose unittest output?",
        answer="Use -v",
    )
    self.assertIn("-v", reply)
    self.assertEqual(len(after_history), 1)
    self.assertEqual(after_history, history)

  def test_req0404_rendergit_cxml_packer_filters_noise(self) -> None:
    """REQ-0404: Render repository into CXML <documents> while skipping __pycache__ and .venv."""
    cxml = cc.render_repo_cxml({
        "src/ledger.py": "class Ledger:\n  pass\n",
        "src/__pycache__/ledger.cpython-311.pyc": "binary_junk",
        ".venv/lib/site.py": "venv_noise",
    })
    self.assertIn("<documents>", cxml)
    self.assertIn("<source>src/ledger.py</source>", cxml)
    self.assertNotIn("__pycache__", cxml)
    self.assertNotIn(".venv", cxml)

  def test_req0405_frequent_intentional_compaction_rpi_bundle(self) -> None:
    """REQ-0405: Distill noisy exploration into line-cited research.md and plan.md with >=80% token reduction."""
    noisy_turns = ["raw grep dump line " * 200 for _ in range(25)]
    findings = [
        "`src/ledger.py:L12-L38` validates AccountId and integer MoneyCents.",
        "`src/routes.py:L45-L70` dispatches POST /settle to SettlementBatch.",
    ]
    plan_steps = [
        "Add idempotency key check in `src/routes.py:L50-L62`.",
        "Persist batch receipt in `src/ledger.py:L39-L55`.",
    ]
    bundle = cc.compact_exploration_to_rpi_artifacts(
        noisy_turns=noisy_turns,
        verified_findings=findings,
        plan_steps=plan_steps,
        out_of_scope=["adversarial_tests/"],
    )
    self.assertIn("`src/ledger.py:L12-L38`", bundle.research_md)
    self.assertIn("## Out of Scope / Do NOT Touch", bundle.plan_md)
    self.assertGreaterEqual(bundle.compression_ratio, 0.80)

    with self.assertRaises(ValueError):
      cc.compact_exploration_to_rpi_artifacts(
          noisy_turns=noisy_turns,
          verified_findings=["Uncited vague finding without file or line"],
          plan_steps=plan_steps,
          out_of_scope=[],
      )

  def test_req0406_human_leverage_pyramid_amplification(self) -> None:
    """REQ-0406: Quantify 1000x Research, 100x Plan, and 1x Code defect amplification."""
    self.assertEqual(cc.estimate_defect_amplification("RESEARCH", 2), 2000)
    self.assertEqual(cc.estimate_defect_amplification("PLAN", 2), 200)
    self.assertEqual(cc.estimate_defect_amplification("CODE", 2), 2)


if __name__ == "__main__":
  unittest.main()
