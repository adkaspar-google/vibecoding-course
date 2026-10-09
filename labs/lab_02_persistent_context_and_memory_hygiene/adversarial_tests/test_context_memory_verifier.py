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

"""Immutable adversarial verifier for Lab 02 (REQ-0201..REQ-0206)."""

from __future__ import annotations

import unittest
from context_memory_manager import (
    compile_auto_memory,
    format_memory_entry,
    resolve_project_memory_dir,
    simulate_context_command,
    validate_root_context_md,
)


class TestLab02ImmutableVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 02."""

  def test_req0201_requires_on_demand_references(self) -> None:
    md_without_refs = (
        "## Commands & Environment\n"
        "## Architecture & Directory Map\n"
        "## Core Conventions\n"
        "## On-Demand References\n"
        "No at-mentions here.\n"
    )
    res = validate_root_context_md(md_without_refs)
    self.assertFalse(res.is_valid)

  def test_req0202_worktree_parity(self) -> None:
    p1 = resolve_project_memory_dir("/a/b/wt1", "/a/repo", "claude", "/home/u")
    p2 = resolve_project_memory_dir("/a/b/wt2/sub", "/a/repo", "claude", "/home/u")
    self.assertEqual(p1, p2)

  def test_req0203_and_req0204_direct_tag_and_200_line_cap(self) -> None:
    line = format_memory_entry("Observed config in repo", "agent_discovered")
    self.assertNotIn("#direct", line)
    compiled = compile_auto_memory(
        [{"statement": f"Rule {i}", "source_type": "user_explicit"} for i in range(220)],
        max_lines=200,
    )
    self.assertLessEqual(compiled.index_line_count, 200)

  def test_req0205_detects_60_percent_degradation_wall(self) -> None:
    rep = simulate_context_command({"history": 130_000}, window_limit_tokens=200_000)
    self.assertEqual(rep.status, "CONTEXT_POLLUTION_WARNING")


if __name__ == "__main__":
  unittest.main()
