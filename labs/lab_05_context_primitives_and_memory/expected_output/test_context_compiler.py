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

"""Unit tests for Lab 05 context_compiler.py (REQ-0501 through REQ-0506)."""

from __future__ import annotations

import unittest

import context_compiler as cc


class TestContextCompiler(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 05 (REQ-0501..REQ-0506)."""

  def test_req0501_three_context_primitives_classifier(self) -> None:
    """Verifies REQ-0501: Three Context Primitives Classifier (Prompts/Slash Commands, Rules, Skills)."""
    self.assertEqual(
        cc.classify_context_primitive(True, False, False),
        cc.ContextPrimitive.PROMPT_OR_SLASH_COMMAND,
    )
    self.assertEqual(
        cc.classify_context_primitive(False, True, False),
        cc.ContextPrimitive.LAZY_LOADED_SKILL,
    )
    self.assertEqual(
        cc.classify_context_primitive(False, False, True),
        cc.ContextPrimitive.STANDING_RULE,
    )

  def test_req0502_instruction_compliance_cliff_and_60_line_map(self) -> None:
    """Verifies REQ-0502: 150-Instruction Compliance Cliff Auditor and 60-Line Root Map Compiler."""
    budget = cc.audit_instruction_compliance_budget(40, cliff_threshold=150)
    self.assertFalse(budget.exceeds_cliff)
    self.assertGreaterEqual(budget.estimated_compliance_rate, 0.90)

    root_md = cc.compile_root_context_map(
        project_name="TaskFlow",
        commands=["Test: `CI=true ./self_diagnose_all.sh`"],
        architecture_items=["`labs/`: 8 progressive hands-on labs"],
        on_demand_docs=["@docs/architecture.md", "@docs/testing-conventions.md"],
    )
    self.assertLessEqual(len(root_md.splitlines()), 60)
    self.assertIn("@docs/architecture.md", root_md)

  def test_req0503_dual_harness_scoped_rule_validator(self) -> None:
    """Verifies REQ-0503: Dual-Harness Path-Scoped Rule Validator (.agents/rules/ and .claude/rules/)."""
    ok_agy, _ = cc.validate_scoped_rule({"trigger": "always_on"}, "Use integer MoneyCents.")
    ok_claude, _ = cc.validate_scoped_rule({"paths": ["labs/**/*.py"]}, "Use integer MoneyCents.")
    self.assertTrue(ok_agy)
    self.assertTrue(ok_claude)

  def test_req0504_provenance_tagged_memory_formatter(self) -> None:
    """Verifies REQ-0504: Provenance-Tagged Memory Formatter (#direct vs. #commit/#time/#session)."""
    direct = cc.format_memory_entry(
        cc.MemoryEntry("Always run self_diagnose_all.sh", is_explicit_user_directive=True)
    )
    self.assertTrue(direct.endswith("#direct"))

    indirect = cc.format_memory_entry(
        cc.MemoryEntry(
            "TaskFlow SettlementBatch uses integer cents",
            is_explicit_user_directive=False,
            commit_sha="a1b2c3d",
        )
    )
    self.assertNotIn("#direct", indirect)
    self.assertIn("#commit:a1b2c3d", indirect)

  def test_req0505_startup_memory_cap_and_stale_commit_pruner(self) -> None:
    """Verifies REQ-0505: 200-Line Startup Memory Cap and Stale Commit Pruner."""
    entries = [
        cc.MemoryEntry("Stale fact", is_explicit_user_directive=False, commit_sha="old1"),
        cc.MemoryEntry("Durable user rule", is_explicit_user_directive=True, commit_sha="old1"),
    ]
    compacted = cc.prune_and_cap_memory(entries, superseded_commits={"old1"}, max_lines=200)
    self.assertEqual(compacted.pruned_stale_count, 1)
    self.assertEqual(len(compacted.active_lines), 1)
    self.assertIn("#direct", compacted.active_lines[0])

  def test_req0506_worktree_shared_memory_path_resolver(self) -> None:
    """Verifies REQ-0506: Git-Worktree Shared Memory Path Resolver for claude and agy."""
    paths = cc.resolve_project_memory_paths("TaskFlow")
    self.assertEqual(paths["claude"], "~/.claude/projects/TaskFlow/memory/MEMORY.md")
    self.assertEqual(paths["agy"], "~/.gemini/antigravity/knowledge/TaskFlow/KNOWLEDGE.md")


if __name__ == "__main__":
  unittest.main()
