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
    "lab_01_vibe_coding_and_earned_autonomy",
    "lab_02_agent_loop_and_harness_wire_trace",
    "lab_03_reppit_workflow_and_reflection",
    "lab_04_context_physics_and_rpi_compaction",
    "lab_05_context_primitives_and_memory",
    "lab_06_skills_chub_and_meta_mcp_code_mode",
    "lab_07_subagent_firewalls_and_peer_council",
    "lab_08_governance_linters_and_autoresearch_ratchet",
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
          "@docs/language-and-code-foundations.md",
          "@docs/skillsbench-and-harness-guide.md",
      ):
        self.assertIn(ref, text)
        ref_path = REPO_ROOT / ref.lstrip("@")
        self.assertTrue(ref_path.is_file(), f"Missing referenced doc: {ref_path}")

  def test_req_agy_02_agents_rules_skills_subagents_and_plugins(self) -> None:
    rules_dir = REPO_ROOT / ".agents" / "rules"
    self.assertTrue((rules_dir / "ubiquitous-language.md").is_file())
    self.assertTrue((rules_dir / "skill-hygiene.md").is_file())

    skills_dir = REPO_ROOT / ".agents" / "skills"
    for skill_name in ("context-hub-docs", "reppit-workflow", "architecture-guard", "harness-audit"):
      self.assertTrue(
          (skills_dir / skill_name / "SKILL.md").is_file(),
          f"Missing .agents/skills/{skill_name}/SKILL.md",
      )

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
        "/context-hub-docs",
        "/reppit-workflow",
        "/architecture-guard",
        "/feature-dev",
        "/plan",
        "/grill-me",
        "/browser",
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
