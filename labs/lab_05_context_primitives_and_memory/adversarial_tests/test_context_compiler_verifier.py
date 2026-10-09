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

"""Immutable adversarial verifier for Lab 05 (REQ-0501 through REQ-0506)."""

from __future__ import annotations

import unittest

import context_compiler as cc


class TestLab05ContextCompilerVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 05."""

  def test_req0501_three_context_primitives_classifier(self) -> None:
    """REQ-0501: Classify items into Prompts/Slash Commands, Standing Rules, and Lazy-Loaded Skills."""
    self.assertEqual(
        cc.classify_context_primitive(
            is_per_turn_intent=True,
            is_multi_step_procedure=False,
            applies_every_session=False,
        ),
        cc.ContextPrimitive.PROMPT_OR_SLASH_COMMAND,
    )
    self.assertEqual(
        cc.classify_context_primitive(
            is_per_turn_intent=False,
            is_multi_step_procedure=True,
            applies_every_session=False,
        ),
        cc.ContextPrimitive.LAZY_LOADED_SKILL,
    )
    self.assertEqual(
        cc.classify_context_primitive(
            is_per_turn_intent=False,
            is_multi_step_procedure=False,
            applies_every_session=True,
        ),
        cc.ContextPrimitive.STANDING_RULE,
    )

  def test_req0502_150_instruction_cliff_and_60_line_map(self) -> None:
    """REQ-0502: Audit the 150-instruction compliance cliff and compile <=60-line root map."""
    safe_budget = cc.audit_instruction_compliance_budget(45, cliff_threshold=150)
    self.assertFalse(safe_budget.exceeds_cliff)
    self.assertGreaterEqual(safe_budget.estimated_compliance_rate, 0.90)

    cliff_budget = cc.audit_instruction_compliance_budget(260, cliff_threshold=150)
    self.assertTrue(cliff_budget.exceeds_cliff)
    self.assertLess(cliff_budget.estimated_compliance_rate, 0.70)

    compiled = cc.compile_root_context_map(
        project_name="Vibe-Coding-Course",
        commands=["Run `CI=true ./self_diagnose_all.sh`"],
        architecture_items=["`labs/`: 8 hands-on labs"],
        on_demand_docs=["docs/architecture.md", "@docs/testing-conventions.md"],
        max_lines=60,
    )
    self.assertLessEqual(len(compiled.splitlines()), 60)
    self.assertIn("@docs/architecture.md", compiled)

    with self.assertRaises(ValueError):
      cc.compile_root_context_map(
          project_name="Overflow",
          commands=[f"cmd {i}" for i in range(70)],
          architecture_items=["arch"],
          on_demand_docs=["@docs/architecture.md"],
          max_lines=60,
      )

  def test_req0503_dual_harness_scoped_rules_validator(self) -> None:
    """REQ-0503: Validate .agents/rules/ ('trigger') and .claude/rules/ ('paths') frontmatter."""
    ok_agy, errs_agy = cc.validate_scoped_rule(
        {"trigger": "always_on", "description": "Ubiquitous language"},
        "Use integer MoneyCents.",
    )
    self.assertTrue(ok_agy, msg=str(errs_agy))

    ok_claude, errs_claude = cc.validate_scoped_rule(
        {"paths": ["labs/**/*.py"]},
        "Use integer MoneyCents.",
    )
    self.assertTrue(ok_claude, msg=str(errs_claude))

    bad_glob, _ = cc.validate_scoped_rule({"trigger": "glob"}, "Missing globs key")
    self.assertFalse(bad_glob)

  def test_req0504_provenance_tagging_discipline(self) -> None:
    """REQ-0504: Reserve #direct strictly for explicit user directives; require relativity tags for indirect facts."""
    direct_line = cc.format_memory_entry(
        cc.MemoryEntry(
            statement="Always run self_diagnose_all.sh before committing",
            is_explicit_user_directive=True,
        )
    )
    self.assertTrue(direct_line.endswith("#direct"))

    indirect_line = cc.format_memory_entry(
        cc.MemoryEntry(
            statement="SettlementBatch validates double-entry balance",
            is_explicit_user_directive=False,
            commit_sha="a1b2c3d",
            date_str="2026-10-09",
        )
    )
    self.assertNotIn("#direct", indirect_line)
    self.assertIn("#commit:a1b2c3d", indirect_line)
    self.assertIn("#time:2026-10-09", indirect_line)

    with self.assertRaises(ValueError):
      cc.format_memory_entry(
          cc.MemoryEntry(
              statement="Untagged indirect observation",
              is_explicit_user_directive=False,
          )
      )

  def test_req0505_prune_superseded_commits_and_200_line_cap(self) -> None:
    """REQ-0505: Prune stale commit observations and offload lines >200 to overflow topic lines."""
    entries = [
        cc.MemoryEntry(
            statement="Old schema observation",
            is_explicit_user_directive=False,
            commit_sha="old111",
        ),
        cc.MemoryEntry(
            statement="User rule survives commit pruning",
            is_explicit_user_directive=True,
            commit_sha="old111",
        ),
    ] + [
        cc.MemoryEntry(
            statement=f"Active observation {i}",
            is_explicit_user_directive=False,
            commit_sha="head999",
        )
        for i in range(205)
    ]
    res = cc.prune_and_cap_memory(entries, superseded_commits={"old111"}, max_lines=200)
    self.assertEqual(res.pruned_stale_count, 1)
    self.assertEqual(len(res.active_lines), 200)
    self.assertEqual(len(res.overflow_topic_lines), 6)
    self.assertIn("User rule survives commit pruning #direct", res.active_lines[0])

  def test_req0506_worktree_shared_memory_paths(self) -> None:
    """REQ-0506: Resolve canonical worktree-shared memory paths for claude and agy."""
    paths = cc.resolve_project_memory_paths("Vibe-Coding-Course")
    self.assertEqual(
        paths["claude"],
        "~/.claude/projects/Vibe-Coding-Course/memory/MEMORY.md",
    )
    self.assertEqual(
        paths["agy"],
        "~/.gemini/antigravity/knowledge/Vibe-Coding-Course/KNOWLEDGE.md",
    )


if __name__ == "__main__":
  unittest.main()
