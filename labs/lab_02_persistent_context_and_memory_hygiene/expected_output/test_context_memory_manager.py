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

"""Unit tests for Lab 02: Persistent Context & Auto-Memory Hygiene."""

from __future__ import annotations

import unittest
from context_memory_manager import (
    compile_auto_memory,
    format_memory_entry,
    resolve_project_memory_dir,
    simulate_context_command,
    validate_root_context_md,
)


VALID_ROOT_CONTEXT = """# Payments Ledger Service — Persistent Project Context

## Commands & Environment
- Run tests: `CI=true python3 -m unittest discover -v`
- Run linter: `python3 -m py_compile domain_ledger.py`

## Architecture & Directory Map
- `src/domain/`: Ubiquitous Language value objects (`AccountId`, `MoneyCents`).
- `src/gate/`: Wittgensteinian epistemic confidence gate.

## Core Conventions
- Monetary amounts MUST use integer minor units (`MoneyCents`), never floats.
- Ambiguous currency conversions must return `CLARIFICATION_REQUIRED`.

## On-Demand References
- Pull architecture deep-dive on demand via @docs/architecture.md
- Pull ledger test invariants on demand via @docs/testing-conventions.md
"""


class TestContextAndMemoryHygiene(unittest.TestCase):
  """Verifies REQ-0201 through REQ-0206."""

  def test_req0201_validate_root_context_and_on_demand_refs(self) -> None:
    """REQ-0201: Validates concise root CLAUDE.md/GEMINI.md and extracts @path refs."""
    res = validate_root_context_md(VALID_ROOT_CONTEXT, max_lines=60)
    self.assertTrue(res.is_valid, msg=res.errors)
    self.assertEqual(res.missing_sections, ())
    self.assertEqual(
        res.on_demand_refs,
        ("docs/architecture.md", "docs/testing-conventions.md"),
    )

    bloated = "\n".join(["# Line"] * 150)
    bad = validate_root_context_md(bloated, max_lines=60)
    self.assertFalse(bad.is_valid)
    self.assertEqual(len(bad.missing_sections), 4)

  def test_req0202_git_worktree_shared_memory_path_resolution(self) -> None:
    """REQ-0202: Subdirectories and git worktrees share one git-derived memory dir."""
    wt1 = resolve_project_memory_dir(
        current_working_dir="/Users/alice/worktrees/feature-fx/src/api",
        git_repo_root="/Users/alice/repos/payments-ledger",
        harness="claude",
        home_dir="/Users/alice",
    )
    wt2 = resolve_project_memory_dir(
        current_working_dir="/Users/alice/worktrees/hotfix-01",
        git_repo_root="/Users/alice/repos/payments-ledger",
        harness="claude",
        home_dir="/Users/alice",
    )
    self.assertEqual(wt1, wt2)
    self.assertEqual(
        wt1,
        "/Users/alice/.claude/projects/-Users-alice-repos-payments-ledger/memory",
    )

    # Outside git repo, falls back to project root
    non_git = resolve_project_memory_dir(
        current_working_dir="/tmp/scratch_proto",
        git_repo_root=None,
        harness="claude",
        home_dir="/Users/alice",
    )
    self.assertEqual(
        non_git,
        "/Users/alice/.claude/projects/-tmp-scratch_proto/memory",
    )

    # Antigravity Knowledge Base path resolution
    agy_dir = resolve_project_memory_dir(
        current_working_dir="/workspace/payments-ledger/sub",
        git_repo_root="/workspace/payments-ledger",
        harness="agy",
        home_dir="/Users/alice",
    )
    self.assertEqual(
        agy_dir,
        "/Users/alice/.gemini/antigravity/knowledge/payments-ledger",
    )

  def test_req0203_auto_memory_compiler_respects_200_line_ceiling(self) -> None:
    """REQ-0203: MEMORY.md stays <= 200 lines and routes topic notes to topic files."""
    entries = [
        {
            "statement": f"Core preference #{i}: run unittest before commit",
            "source_type": "user_explicit",
            "core": True,
        }
        for i in range(240)
    ]
    entries.append({
        "statement": "Deadlock traced to retry lock order in batch worker",
        "source_type": "agent_discovered",
        "topic": "debugging",
        "date_str": "2026-10-08",
        "session_id": "a1b2c3d4",
    })
    compiled = compile_auto_memory(entries, harness="claude", max_lines=200)
    self.assertLessEqual(compiled.index_line_count, 200)
    self.assertLessEqual(compiled.index_byte_count, 25_000)
    self.assertIn("topics/debugging.md", compiled.topic_files)
    self.assertIn("topics/overflow.md", compiled.topic_files)

    # Antigravity Knowledge Base frontmatter check
    agy_compiled = compile_auto_memory(entries[:5], harness="agy", max_lines=200)
    self.assertIn("scope: workspace", agy_compiled.index_markdown)

  def test_req0204_epistemic_provenance_direct_tag_discipline(self) -> None:
    """REQ-0204: #direct is reserved strictly for explicit user statements."""
    user_line = format_memory_entry(
        "Always use MoneyCents integer arithmetic",
        source_type="user_explicit",
        date_str="2026-10-08",
    )
    self.assertIn("#direct", user_line)

    agent_line = format_memory_entry(
        "Batch settlement worker uses SQLite WAL mode",
        source_type="codebase_observed",
        commit_sha="654321a",
        session_id="deadbeef",
    )
    self.assertNotIn("#direct", agent_line)
    self.assertIn("#commit:654321a", agent_line)
    self.assertIn("#session:deadbeef", agent_line)

  def test_req0205_context_command_budget_and_60pct_threshold(self) -> None:
    """REQ-0205: Simulates /context utilization and flags >60% pollution."""
    healthy = simulate_context_command(
        {
            "system_prompt": 8_000,
            "root_context_md": 1_200,
            "auto_memory": 1_500,
            "skills_level1_metadata": 900,
            "conversation_history": 82_000,
        },
        deferred_reference_tokens=28_000,
        window_limit_tokens=200_000,
    )
    self.assertEqual(healthy.status, "OPTIMAL_SWEET_SPOT")
    self.assertEqual(healthy.progressive_savings_tokens, 28_000)

    polluted = simulate_context_command(
        {
            "system_prompt": 10_000,
            "bloated_context_dump": 45_000,
            "raw_grep_outputs": 85_000,
        },
        window_limit_tokens=200_000,
    )
    self.assertEqual(polluted.status, "CONTEXT_POLLUTION_WARNING")
    self.assertGreater(polluted.utilization_ratio, 0.60)


if __name__ == "__main__":
  unittest.main()
