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

"""Unit tests for Lab 07 subagent_council.py (REQ-0701 through REQ-0706)."""

from __future__ import annotations

import unittest

import subagent_council as sc


class TestSubagentCouncil(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 07 (REQ-0701..REQ-0706)."""

  def test_req0701_subagent_context_firewall(self) -> None:
    """Verifies REQ-0701: Subagent Context Firewall isolates noisy child search traces with >=90% token savings."""
    res = sc.execute_subagent_context_firewall(
        raw_search_traces=["grep dump " * 500 for _ in range(10)],
        concise_findings=["`src/ledger.py:L25` enforces TaskFlow double-entry balance."],
    )
    self.assertGreaterEqual(res.isolation_ratio, 0.90)
    self.assertLessEqual(res.parent_summary_tokens_returned, 600)

  def test_req0702_read_only_subagent_tool_boundary_validator(self) -> None:
    """Verifies REQ-0702: Read-Only Subagent Tool Boundary Validator blocks Edit/Bash on explorer/architect/reviewer."""
    ok, _ = sc.validate_subagent_tool_boundary("code-explorer", ["Glob", "Grep", "Read"])
    bad, _ = sc.validate_subagent_tool_boundary("code-reviewer", ["Read", "Edit"])
    self.assertTrue(ok)
    self.assertFalse(bad)

  def test_req0703_multi_agent_pr_triage_and_confidence_filter(self) -> None:
    """Verifies REQ-0703: Multi-Agent PR Triage buckets MUST_FIX/RECOMMENDED/CONSIDER and filters confidence < 80."""
    findings = [
        sc.ReviewFinding("Security", "SQL injection", "src/db.py:L42", 95, sc.TriageTier.MUST_FIX),
        sc.ReviewFinding("Style", "Nitpick rename", "src/db.py:L10", 50, sc.TriageTier.CONSIDER),
    ]
    report = sc.synthesize_pr_triage_report(findings, min_confidence=80)
    self.assertEqual(len(report.must_fix), 1)
    self.assertEqual(report.dropped_low_confidence_count, 1)
    self.assertTrue(report.blocks_merge)

  def test_req0704_llm_council_anonymizer_and_borda_rank_aggregator(self) -> None:
    """Verifies REQ-0704: Karpathy's llm-council Anonymized Peer Review and Borda Rank Aggregation."""
    anon, label_to_model = sc.anonymize_council_responses({
        "claude-opus-4-6": "Optimistic concurrency",
        "gemini-3.1-pro": "Serializable ledger",
    })
    self.assertEqual(set(anon.keys()), {"Response A", "Response B"})
    res = sc.aggregate_borda_rankings(
        [["Response B", "Response A"], ["Response B", "Response A"]],
        label_to_model,
    )
    self.assertEqual(res.winning_label, "Response B")
    self.assertEqual(res.winning_model, "gemini-3.1-pro")

  def test_req0705_workspace_isolation_mode_selector(self) -> None:
    """Verifies REQ-0705: Workspace Isolation Mode Selector ('inherit' vs. 'worktree')."""
    self.assertEqual(sc.select_workspace_isolation_mode(True, parallel_writers=0), "inherit")
    self.assertEqual(sc.select_workspace_isolation_mode(False, parallel_writers=2), "worktree")

  def test_req0706_disjoint_git_worktree_file_ownership_validator(self) -> None:
    """Verifies REQ-0706: Disjoint git worktree File-Ownership Validator detects overlapping files."""
    clean = sc.validate_disjoint_worktree_ownership({
        "wt-1": ["src/auth.py"],
        "wt-2": ["src/ledger.py"],
    })
    overlap = sc.validate_disjoint_worktree_ownership({
        "wt-1": ["src/shared.py"],
        "wt-2": ["src/shared.py"],
    })
    self.assertTrue(clean.is_disjoint)
    self.assertFalse(overlap.is_disjoint)
    self.assertEqual(overlap.overlapping_files, ("src/shared.py",))


if __name__ == "__main__":
  unittest.main()
