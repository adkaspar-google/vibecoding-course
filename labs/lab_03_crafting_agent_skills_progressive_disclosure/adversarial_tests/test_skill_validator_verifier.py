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

"""Immutable adversarial verifier for Lab 03 (REQ-0301..REQ-0306)."""

from __future__ import annotations

import os
from pathlib import Path
import unittest
from skill_validator import (
    apply_brand_profile,
    audit_skill_quality_delta,
    compute_progressive_disclosure_budget,
    validate_skill_package,
)


class TestLab03ImmutableVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 03."""

  def _target_dir(self) -> Path:
    env_target = os.environ.get("LAB03_TARGET_DIR")
    if env_target:
      return Path(env_target)
    return Path(__file__).resolve().parent.parent / "expected_output"

  def test_req0301_and_req0302_validates_anthropic_brand_package(self) -> None:
    pkg_dir = self._target_dir() / "anthropic-brand"
    rep = validate_skill_package(pkg_dir)
    self.assertTrue(rep.is_valid, msg=rep.errors)
    for required_file in ("docs.md", "slides-deck.md", "apply_template.md"):
      self.assertIn(required_file, rep.companion_files)

  def test_req0303_progressive_disclosure_saves_tokens(self) -> None:
    pkg_dir = self._target_dir() / "anthropic-brand"
    budget = compute_progressive_disclosure_budget(pkg_dir, "docs.md")
    self.assertGreater(budget.startup_savings_ratio, 0.70)
    self.assertLess(budget.active_session_tokens, budget.eager_all_files_tokens)

  def test_req0304_catches_self_generated_skill_traps(self) -> None:
    bad_md = (
        "Always write clean, modular, well-documented code.\n"
        "Multiply all input dimensions by 1000.0 before layout.\n"
    )
    audit = audit_skill_quality_delta(bad_md, ["#141413", "WCAG"])
    self.assertEqual(audit.classification, "SELF_GENERATED_DEGRADATION_RISK")
    self.assertTrue(audit.has_unverified_speculative_trap)

  def test_req0305_applies_brand_profile_by_artifact(self) -> None:
    res = apply_brand_profile({"title": "Deck"}, "slides")
    self.assertEqual(res["reference_loaded"], "slides-deck.md")
    self.assertEqual(res["margin_pt"], 36)


if __name__ == "__main__":
  unittest.main()
