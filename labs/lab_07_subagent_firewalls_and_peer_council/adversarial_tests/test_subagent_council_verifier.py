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

"""Immutable adversarial verifier for Lab 07 (REQ-0701 through REQ-0706)."""

from __future__ import annotations

import unittest

import subagent_council as sc


class TestLab07SubagentCouncilVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 07."""

  def test_req0701_subagent_context_firewall_saves_over_90_percent_parent_tokens(self) -> None:
    """REQ-0701: Isolate high-token child search traces and return bounded file:line summary."""
    raw_traces = ["full file read and grep dump " * 300 for _ in range(12)]
    findings = [
        "`src/auth.py:L14` verifies HMAC signature.",
        "`src/ledger.py:L88` commits integer-cent postings.",
    ]
    fw = sc.execute_subagent_context_firewall(raw_traces, findings, max_parent_tokens=600)
    self.assertGreaterEqual(fw.isolation_ratio, 0.90)
    self.assertLessEqual(fw.parent_summary_tokens_returned, 600)
    self.assertIn("`src/auth.py:L14`", fw.summary_markdown)

  def test_req0702_read_only_subagent_tool_boundary_enforcement(self) -> None:
    """REQ-0702: Enforce read-only tools (Glob, Grep, Read, LSP) on explorer, architect, reviewer."""
    ok, errs = sc.validate_subagent_tool_boundary("code-explorer", ["Glob", "Grep", "Read"])
    self.assertTrue(ok, msg=str(errs))

    bad, errs_bad = sc.validate_subagent_tool_boundary(
        "code-reviewer",
        ["Read", "Edit", "Bash"],
    )
    self.assertFalse(bad)
    self.assertTrue(any("Edit" in e or "Bash" in e for e in errs_bad))

  def test_req0703_multi_agent_pr_triage_and_confidence_filter(self) -> None:
    """REQ-0703: Bucket findings into MUST_FIX, RECOMMENDED, CONSIDER and drop confidence < 80."""
    findings = [
        sc.ReviewFinding(
            specialist="Security",
            title="SQL injection in raw query string",
            file_line="src/db.py:L42",
            confidence=95,
            tier=sc.TriageTier.MUST_FIX,
        ),
        sc.ReviewFinding(
            specialist="Performance",
            title="N+1 query in batch loader",
            file_line="src/loader.py:L19",
            confidence=85,
            tier=sc.TriageTier.RECOMMENDED,
        ),
        sc.ReviewFinding(
            specialist="Style",
            title="Subjective variable rename nitpick",
            file_line="src/loader.py:L20",
            confidence=55,
            tier=sc.TriageTier.CONSIDER,
        ),
    ]
    report = sc.synthesize_pr_triage_report(findings, min_confidence=80)
    self.assertEqual(len(report.must_fix), 1)
    self.assertEqual(len(report.recommended), 1)
    self.assertEqual(len(report.consider), 0)
    self.assertEqual(report.dropped_low_confidence_count, 1)
    self.assertTrue(report.blocks_merge)

  def test_req0704_llm_council_anonymization_and_borda_aggregation(self) -> None:
    """REQ-0704: Anonymize model identities ('Response A', ...) and aggregate Borda rankings."""
    anon, label_to_model = sc.anonymize_council_responses({
        "claude-opus-4-6": "Design with optimistic concurrency.",
        "gemini-3.1-pro": "Design with serializable ledger table.",
        "gpt-5": "Design with event queue.",
    })
    self.assertEqual(set(anon.keys()), {"Response A", "Response B", "Response C"})
    for label in anon:
      self.assertNotIn("claude", label.lower())
      self.assertNotIn("gemini", label.lower())

    ballots = [
        ["Response B", "Response A", "Response C"],
        ["Response B", "Response C", "Response A"],
        ["Response A", "Response B", "Response C"],
    ]
    result = sc.aggregate_borda_rankings(ballots, label_to_model)
    self.assertEqual(result.winning_label, "Response B")
    self.assertEqual(result.winning_model, "gemini-3.1-pro")
    self.assertEqual(result.borda_scores_by_label["Response B"], 8)

  def test_req0705_workspace_isolation_mode_selector(self) -> None:
    """REQ-0705: Select 'inherit' for read-only exploration and 'worktree' for parallel writers."""
    self.assertEqual(sc.select_workspace_isolation_mode(True, parallel_writers=0), "inherit")
    self.assertEqual(sc.select_workspace_isolation_mode(False, parallel_writers=2), "worktree")

  def test_req0706_disjoint_git_worktree_file_ownership(self) -> None:
    """REQ-0706: Verify disjoint file ownership across parallel worktrees and detect collisions."""
    clean = sc.validate_disjoint_worktree_ownership({
        "wt-auth": ["src/auth.py", "tests/test_auth.py"],
        "wt-ledger": ["src/ledger.py", "tests/test_ledger.py"],
    })
    self.assertTrue(clean.is_disjoint)
    self.assertEqual(clean.overlapping_files, ())

    collision = sc.validate_disjoint_worktree_ownership({
        "wt-auth": ["src/shared.py", "src/auth.py"],
        "wt-ledger": ["src/shared.py", "src/ledger.py"],
    })
    self.assertFalse(collision.is_disjoint)
    self.assertEqual(collision.overlapping_files, ("src/shared.py",))


if __name__ == "__main__":
  unittest.main()
