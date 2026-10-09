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

"""Verification suite for the Antigravity Native Track ('agy' branch)."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]

LAB_NAMES = [
    "lab_01_vocabulary_and_bounded_language_games",
    "lab_02_persistent_context_and_memory_hygiene",
    "lab_03_crafting_agent_skills_progressive_disclosure",
    "lab_04_skill_evaluation_and_trigger_calibration",
    "lab_05_multi_agent_feature_dev_orchestration",
    "lab_06_capstone_plugins_mcp_and_harness_flywheel",
]


class TestAntigravityTrack(unittest.TestCase):
  """Automated acceptance tests for the Antigravity ('agy') track."""

  def test_req_agy_01_gemini_and_agents_md_concise_with_refs(self) -> None:
    for fname in ("GEMINI.md", "AGENTS.md"):
      fpath = REPO_ROOT / fname
      self.assertTrue(fpath.is_file(), f"Missing {fname}")
      text = fpath.read_text(encoding="utf-8")
      self.assertLessEqual(len(text.splitlines()), 45)
      for ref in (
          "@docs/architecture.md",
          "@docs/testing-conventions.md",
          "@docs/wittgenstein-language-games.md",
          "@docs/skillsbench-empirical-guide.md",
      ):
        self.assertIn(ref, text)

  def test_req_agy_02_agents_rules_skills_subagents_and_plugins(self) -> None:
    rules_dir = REPO_ROOT / ".agents" / "rules"
    self.assertTrue((rules_dir / "ubiquitous-language.md").is_file())
    self.assertTrue((rules_dir / "skill-hygiene.md").is_file())

    brand_dir = REPO_ROOT / ".agents" / "skills" / "anthropic-brand"
    for fname in ("SKILL.md", "docs.md", "slides-deck.md", "apply_template.md"):
      self.assertTrue((brand_dir / fname).is_file(), f"Missing {fname}")

    for agent in ("code-explorer.md", "code-architect.md", "code-reviewer.md"):
      self.assertTrue((REPO_ROOT / ".agents" / "agents" / agent).is_file())
    self.assertTrue(
        (REPO_ROOT / ".agents" / "workflows" / "feature-dev.md").is_file()
    )

    plugin_dir = REPO_ROOT / ".agents" / "plugins" / "vibe-engineering-kit"
    self.assertTrue((plugin_dir / "plugin.json").is_file())
    self.assertTrue((plugin_dir / "mcp_config.json").is_file())
    self.assertTrue((plugin_dir / "hooks.json").is_file())
    manifest = json.loads((plugin_dir / "plugin.json").read_text(encoding="utf-8"))
    self.assertEqual(manifest["name"], "vibe-engineering-kit")

  def test_req_agy_03_walkthroughs_and_playbook(self) -> None:
    playbook = REPO_ROOT / "playbooks" / "ANTIGRAVITY_PLAYBOOK.md"
    self.assertTrue(playbook.is_file())
    pb_text = playbook.read_text(encoding="utf-8")
    self.assertLessEqual(len(pb_text.splitlines()), 150)
    for token in (
        "/stats",
        "/memory",
        "KNOWLEDGE.md",
        "#direct",
        "/anthropic-brand",
        "/feature-dev",
        "/plan",
    ):
      self.assertIn(token, pb_text)

    for lab in LAB_NAMES:
      wt_text = (REPO_ROOT / "labs" / lab / "WALKTHROUGH.md").read_text(
          encoding="utf-8"
      )
      self.assertIn("## Antigravity Track", wt_text)
      self.assertIn("agy --workspace .", wt_text)
      self.assertIn(f"./labs/{lab}/self_diagnose.sh work", wt_text)


if __name__ == "__main__":
  unittest.main()
