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

"""Unit tests for Lab 04: Skill Evaluation (eval-viewer) & SDT Trigger Calibration."""

from __future__ import annotations

import json
import os
from pathlib import Path
import unittest
from skill_eval_engine import (
    aggregate_paired_benchmark,
    compute_sdt_trigger_metrics,
    consolidate_overloaded_skills,
    generate_eval_viewer_html,
    grade_trajectory_expectations,
)

LAB_ROOT = Path(
    os.environ.get("LAB_DIR", str(Path(__file__).resolve().parent.parent))
)
STARTER_CATALOG = LAB_ROOT / "starter" / "overloaded_skill_catalog.json"


class TestSkillEvalAndTriggerCalibration(unittest.TestCase):
  """Verifies REQ-0401 through REQ-0406."""

  def test_req0401_grading_json_schema_exact_keys(self) -> None:
    """REQ-0401: Produces grading.json schema with 'text', 'passed', and 'evidence'."""
    output = "Applied #FAF9F5 background with Styrene A heading and 64pt margin."
    expectations = [
        {"text": "Uses brand-ivory #FAF9F5", "required_substring": "#FAF9F5"},
        {"text": "Uses Styrene A font", "required_substring": "Styrene A"},
        {"text": "Uses 36pt slide margin", "required_substring": "36pt"},
    ]
    graded = grade_trajectory_expectations(output, expectations)
    self.assertEqual(graded["passed_count"], 2)
    self.assertEqual(graded["total_count"], 3)
    self.assertAlmostEqual(graded["pass_rate"], 0.6667, places=4)
    first = graded["expectations"][0]
    self.assertEqual(set(first.keys()), {"text", "passed", "evidence"})

  def test_req0402_paired_with_vs_without_skill_benchmark(self) -> None:
    """REQ-0402: Aggregates paired runs into benchmark.json and computes net lift."""
    with_skill = [
        {"pass_rate": 0.90, "tokens": 1800},
        {"pass_rate": 0.85, "tokens": 1750},
        {"pass_rate": 0.95, "tokens": 1850},
    ]
    without_skill = [
        {"pass_rate": 0.40, "tokens": 2400},
        {"pass_rate": 0.35, "tokens": 2600},
        {"pass_rate": 0.45, "tokens": 2500},
    ]
    bench = aggregate_paired_benchmark(with_skill, without_skill)
    self.assertEqual(bench["verdict"], "POSITIVE_LIFT")
    self.assertAlmostEqual(bench["delta"]["net_pass_rate_delta"], 0.50, places=4)
    self.assertLess(bench["delta"]["mean_token_delta"], 0.0)

  def test_req0403_eval_viewer_html_contains_outputs_and_benchmark_tabs(self) -> None:
    """REQ-0403: Generates static eval-viewer HTML with Outputs and Benchmark tabs."""
    bench = aggregate_paired_benchmark(
        [{"pass_rate": 0.90, "tokens": 1500}],
        [{"pass_rate": 0.40, "tokens": 2100}],
    )
    grading = grade_trajectory_expectations(
        "Found #FAF9F5",
        [{"text": "Check #FAF9F5", "required_substring": "#FAF9F5"}],
    )
    html_report = generate_eval_viewer_html(
        bench, [{"prompt": "Brand the RFC doc", "grading": grading}]
    )
    self.assertIn("id='tab-outputs'", html_report)
    self.assertIn("id='tab-benchmark'", html_report)
    self.assertIn("POSITIVE_LIFT", html_report)

  def test_req0404_sdt_trigger_calibration_d_prime_and_bias_c(self) -> None:
    """REQ-0404: Computes Hautus-smoothed d' and criterion bias c."""
    # Calibrated description: 19 hits, 1 miss, 1 false alarm, 19 correct rejections
    calibrated = compute_sdt_trigger_metrics(
        hits=19, misses=1, false_alarms=1, correct_rejections=19
    )
    self.assertGreater(calibrated.d_prime, 2.5)
    self.assertAlmostEqual(calibrated.criterion_c, 0.0, places=2)
    self.assertEqual(calibrated.bias_regime, "BALANCED_CALIBRATED")

    # Over-broad description ("Trade-Off Trap"): 20 hits, 0 misses, 12 false alarms, 8 CR
    over_liberal = compute_sdt_trigger_metrics(
        hits=20, misses=0, false_alarms=12, correct_rejections=8
    )
    self.assertEqual(over_liberal.bias_regime, "LIBERAL_FALSE_ALARM_POLLUTION")
    self.assertGreater(calibrated.utility_u, over_liberal.utility_u)

  def test_req0405_consolidate_overloaded_skills_to_sweet_spot(self) -> None:
    """REQ-0405: Consolidates 7 colliding skills into 3 domain skills + references/."""
    raw = json.loads(STARTER_CATALOG.read_text(encoding="utf-8"))
    res = consolidate_overloaded_skills(raw["skills"], max_active_skills=3)
    self.assertEqual(res["original_skill_count"], 7)
    self.assertEqual(res["consolidated_skill_count"], 3)
    self.assertTrue(res["is_within_sweet_spot"])
    self.assertGreaterEqual(len(res["demoted_to_references"]), 6)


if __name__ == "__main__":
  unittest.main()
