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

"""Immutable adversarial verifier for Lab 05 (REQ-0501..REQ-0506)."""

from __future__ import annotations

import os
from pathlib import Path
import unittest
from feature_dev_orchestrator import (
    ClarificationGateError,
    FeatureDevPipeline,
    filter_review_findings,
    validate_subagent_definitions,
)


class TestLab05ImmutableVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 05."""

  def _target_dir(self) -> Path:
    env_target = os.environ.get("LAB05_TARGET_DIR")
    if env_target:
      return Path(env_target)
    return Path(__file__).resolve().parent.parent / "expected_output"

  def test_req0501_validates_all_three_subagents(self) -> None:
    rep = validate_subagent_definitions(self._target_dir() / "agents")
    self.assertTrue(rep["is_valid"], msg=rep["errors"])

  def test_req0502_through_req0505_end_to_end_pipeline(self) -> None:
    pipe = FeatureDevPipeline("Add audit trail")
    pipe.complete_phase2_exploration([
        {"entry_points": ["a.py:1"], "call_chain": ["a.py:1"], "essential_files": ["a.py"]},
        {"entry_points": ["b.py:2"], "call_chain": ["b.py:2"], "essential_files": ["b.py"]},
    ])
    pipe.register_phase3_questions(["Retention period?"])
    with self.assertRaises(ClarificationGateError):
      pipe.advance_to_phase4_architecture([])

    pipe.answer_phase3_question("Retention period?", "90 days")
    pipe.advance_to_phase4_architecture([
        {"lens": "minimal_changes", "summary": "S1", "files_to_touch": ["a.py"], "tradeoffs": "T1"},
        {"lens": "clean_architecture", "summary": "S2", "files_to_touch": ["b.py"], "tradeoffs": "T2"},
        {"lens": "pragmatic_balance", "summary": "S3", "files_to_touch": ["c.py"], "tradeoffs": "T3"},
    ])
    pipe.approve_architecture_and_implement("clean_architecture", ["b.py"])
    summary = pipe.complete_phase6_review_and_phase7_summary([
        {"category": "critical_bugs", "confidence": 95, "location": "b.py:10", "description": "Bug", "fix_suggestion": "Fix"},
        {"category": "nit", "confidence": 50, "location": "b.py:2", "description": "Low", "fix_suggestion": "Ignore"},
    ])
    self.assertEqual(summary["phase"], 7)
    self.assertEqual(len(summary["high_confidence_review_findings"]), 1)

  def test_req0505_confidence_filter_suppresses_below_80(self) -> None:
    res = filter_review_findings(
        [{"category": "nit", "confidence": 79, "location": "x.py:1", "description": "d", "fix_suggestion": "f"}],
        min_confidence=80,
    )
    self.assertEqual(res["retained_count"], 0)


if __name__ == "__main__":
  unittest.main()
