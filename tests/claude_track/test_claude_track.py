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

"""Verification suite for the Claude Code Native Track ('claude' branch)."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
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


class TestClaudeCodeTrack(unittest.TestCase):
  """Automated acceptance tests for the Claude Code ('claude') track."""

  def test_req_claude_01_all_labs_self_diagnose(self) -> None:
    proc = subprocess.run(
        [str(REPO_ROOT / "self_diagnose_all.sh")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    self.assertEqual(proc.returncode, 0, msg=proc.stdout + "\n" + proc.stderr)
    self.assertIn("[ALL PASSED] 8/8", proc.stdout)

  def test_req_claude_02_empty_target_fails(self) -> None:
    for lab in LAB_NAMES:
      script = REPO_ROOT / "labs" / lab / "self_diagnose.sh"
      with tempfile.TemporaryDirectory() as tmpdir:
        proc = subprocess.run(
            [str(script), tmpdir],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(proc.returncode, 0, msg=f"{lab} passed on empty dir")
        self.assertIn("[FAIL]", proc.stdout + proc.stderr)

  def test_req_claude_03_copied_expected_output_passes(self) -> None:
    for lab in LAB_NAMES:
      lab_dir = REPO_ROOT / "labs" / lab
      script = lab_dir / "self_diagnose.sh"
      with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree(lab_dir / "expected_output", tmpdir, dirs_exist_ok=True)
        proc = subprocess.run(
            [str(script), tmpdir],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode, 0, msg=f"{lab} failed: {proc.stdout}\n{proc.stderr}"
        )

  def test_req_claude_04_claude_md_concise_and_has_on_demand_refs(self) -> None:
    claude_md = REPO_ROOT / "CLAUDE.md"
    self.assertTrue(claude_md.is_file())
    text = claude_md.read_text(encoding="utf-8")
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

  def test_req_claude_05_skills_agents_and_plugin_present(self) -> None:
    skills_dir = REPO_ROOT / ".claude" / "skills"
    for skill_name in ("context-hub-docs", "reppit-workflow", "architecture-guard", "harness-audit"):
      self.assertTrue(
          (skills_dir / skill_name / "SKILL.md").is_file(),
          f"Missing .claude/skills/{skill_name}/SKILL.md",
      )

    for agent in ("code-explorer.md", "code-architect.md", "code-reviewer.md"):
      self.assertTrue((REPO_ROOT / ".claude" / "agents" / agent).is_file())

    self.assertTrue(
        (REPO_ROOT / ".claude" / "commands" / "feature-dev.md").is_file()
    )
    self.assertTrue(
        (REPO_ROOT / ".claude-plugin" / "plugin.json").is_file()
    )

  def test_req_claude_06_settings_and_learner_deny_rules(self) -> None:
    settings = json.loads(
        (REPO_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    self.assertIn(
        "Edit(**/adversarial_tests/**)",
        settings.get("permissions", {}).get("deny", []),
    )
    learner = json.loads(
        (REPO_ROOT / ".claude" / "learner.settings.json").read_text(
            encoding="utf-8"
        )
    )
    deny = learner.get("permissions", {}).get("deny", [])
    self.assertIn("Read(**/expected_output/**)", deny)
    self.assertIn("Edit(**/adversarial_tests/**)", deny)

  def test_req_claude_07_walkthroughs_and_playbook(self) -> None:
    playbook = REPO_ROOT / "playbooks" / "CLAUDE_CODE_PLAYBOOK.md"
    self.assertTrue(playbook.is_file())
    pb_text = playbook.read_text(encoding="utf-8")
    self.assertLessEqual(len(pb_text.splitlines()), 150)
    for token in (
        "/context",
        "/memory",
        "/btw",
        "/rewind",
        "/context-hub-docs",
        "/reppit-workflow",
        "/architecture-guard",
        "/feature-dev",
        "plan mode",
        "/clear",
    ):
      self.assertIn(token, pb_text)

    for lab in LAB_NAMES:
      wt_text = (REPO_ROOT / "labs" / lab / "WALKTHROUGH.md").read_text(
          encoding="utf-8"
      )
      self.assertIn("## Claude Code Track", wt_text)
      self.assertIn("claude --settings .claude/learner.settings.json", wt_text)
      self.assertIn(f"./labs/{lab}/self_diagnose.sh work", wt_text)


if __name__ == "__main__":
  unittest.main()
