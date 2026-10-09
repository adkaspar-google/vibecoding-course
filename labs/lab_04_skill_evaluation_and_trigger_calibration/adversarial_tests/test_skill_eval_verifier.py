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

"""Immutable adversarial verifier for Lab 04 (REQ-0401..REQ-0406)."""

from __future__ import annotations

import unittest
from skill_eval_engine import (
    aggregate_paired_benchmark,
    compute_sdt_trigger_metrics,
    consolidate_overloaded_skills,
    generate_eval_viewer_html,
    grade_trajectory_expectations,
)


class TestLab04ImmutableVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 04."""

  def test_req0401_and_req0402_paired_delta(self) -> None:
    g = grade_trajectory_expectations(
        "hello world", [{"text": "has world", "required_substring": "world"}]
    )
    self.assertEqual(g["pass_rate"], 1.0)
    b = aggregate_paired_benchmark([{"pass_rate": 0.2}], [{"pass_rate": 0.6}])
    self.assertEqual(b["verdict"], "NOISE_OR_REGRESSION")

  def test_req0403_html_viewer_sections(self) -> None:
    b = aggregate_paired_benchmark([{"pass_rate": 0.8}], [{"pass_rate": 0.4}])
    html_str = generate_eval_viewer_html(b, [])
    self.assertIn("tab-outputs", html_str)
    self.assertIn("tab-benchmark", html_str)

  def test_req0404_sdt_hautus_smoothing_handles_zeros(self) -> None:
    # Even with 0 misses and 0 false alarms, Hautus smoothing keeps d' finite
    m = compute_sdt_trigger_metrics(hits=10, misses=0, false_alarms=0, correct_rejections=10)
    self.assertGreater(m.d_prime, 2.0)
    self.assertLess(m.d_prime, 10.0)

  def test_req0405_reference_first_consolidation(self) -> None:
    skills = [
        {"name": f"micro-{i}", "domain": "testing", "lines": 20}
        for i in range(5)
    ]
    out = consolidate_overloaded_skills(skills, max_active_skills=3)
    self.assertEqual(out["consolidated_skill_count"], 1)
    self.assertEqual(len(out["consolidated_skills"][0]["references"]), 5)


if __name__ == "__main__":
  unittest.main()
