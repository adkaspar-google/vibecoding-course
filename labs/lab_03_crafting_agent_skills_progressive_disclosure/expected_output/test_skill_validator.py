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

"""Unit tests for Lab 03: Crafting Agent Skills & Progressive Disclosure."""

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

CURRENT_DIR = Path(__file__).resolve().parent
LAB_ROOT = Path(os.environ.get("LAB_DIR", str(CURRENT_DIR.parent)))
STARTER_DIR = LAB_ROOT / "starter" / "self_generated_skill"
BRAND_SKILL_DIR = CURRENT_DIR / "anthropic-brand"


class TestCraftingAgentSkills(unittest.TestCase):
  """Verifies REQ-0301 through REQ-0306."""

  def test_req0301_anthropic_brand_skill_directory_anatomy(self) -> None:
    """REQ-0301: anthropic-brand contains SKILL.md, docs.md, slides-deck.md, apply_template.md."""
    rep = validate_skill_package(BRAND_SKILL_DIR)
    self.assertTrue(rep.is_valid, msg=rep.errors)
    self.assertEqual(rep.name, "anthropic-brand")
    self.assertEqual(
        rep.companion_files,
        ("apply_template.md", "docs.md", "slides-deck.md"),
    )

  def test_req0302_agentskills_frontmatter_and_cardinality_validation(self) -> None:
    """REQ-0302: Rejects invalid names, missing negative triggers, and <50 line micro-skills."""
    bad = validate_skill_package(STARTER_DIR)
    self.assertFalse(bad.is_valid)
    self.assertGreaterEqual(len(bad.errors), 3)

  def test_req0303_progressive_disclosure_token_accounting(self) -> None:
    """REQ-0303: Level 1 metadata startup load saves >75% tokens over eager loading."""
    budget = compute_progressive_disclosure_budget(
        BRAND_SKILL_DIR, active_reference="slides-deck.md"
    )
    self.assertLess(budget.level1_metadata_tokens, 120)
    self.assertGreater(budget.startup_savings_ratio, 0.75)
    self.assertLess(budget.active_session_tokens, budget.eager_all_files_tokens)

  def test_req0304_self_generated_skill_trap_detection(self) -> None:
    """REQ-0304: Flags SkillsBench self-generated filler and 1000x conversion traps."""
    starter_md = (STARTER_DIR / "SKILL.md").read_text(encoding="utf-8")
    starter_audit = audit_skill_quality_delta(
        starter_md,
        observed_baseline_failures=["#D97757", "WCAG", "Styrene A"],
    )
    self.assertEqual(
        starter_audit.classification, "SELF_GENERATED_DEGRADATION_RISK"
    )
    self.assertTrue(starter_audit.has_generic_pretraining_filler)
    self.assertTrue(starter_audit.has_unverified_speculative_trap)
    self.assertEqual(starter_audit.grounded_failure_matches, 0)

    curated_md = (BRAND_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    curated_audit = audit_skill_quality_delta(
        curated_md,
        observed_baseline_failures=["#D97757", "WCAG", "Styrene A"],
    )
    self.assertEqual(
        curated_audit.classification, "CURATED_HIGH_SIGNAL_DELTA"
    )
    self.assertFalse(curated_audit.has_generic_pretraining_filler)
    self.assertFalse(curated_audit.has_unverified_speculative_trap)
    self.assertEqual(curated_audit.grounded_failure_matches, 3)

  def test_req0305_deterministic_brand_template_application(self) -> None:
    """REQ-0305: Applies doc vs slides brand profiles deterministically."""
    doc_out = apply_brand_profile({"title": "Q4 Architecture RFC"}, "doc")
    self.assertEqual(doc_out["reference_loaded"], "docs.md")
    self.assertEqual(doc_out["margin_pt"], 64)
    self.assertEqual(doc_out["background_hex"], "#FAF9F5")

    slides_out = apply_brand_profile({"title": "Vibe Coding Deck"}, "slides")
    self.assertEqual(slides_out["reference_loaded"], "slides-deck.md")
    self.assertEqual(slides_out["margin_pt"], 36)
    self.assertEqual(slides_out["accent_hex"], "#D97757")


if __name__ == "__main__":
  unittest.main()
