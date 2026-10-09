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

"""Unit tests for Lab 05: Multi-Agent Feature-Dev Orchestration."""

from __future__ import annotations

from pathlib import Path
import unittest
from feature_dev_orchestrator import (
    ArchitectureApprovalGateError,
    ClarificationGateError,
    FeatureDevPipeline,
    aggregate_explorer_findings,
    filter_review_findings,
    synthesize_architecture_options,
    validate_subagent_definitions,
)

AGENTS_DIR = Path(__file__).resolve().parent / "agents"


class TestFeatureDevMultiAgentOrchestration(unittest.TestCase):
  """Verifies REQ-0501 through REQ-0506."""

  def test_req0501_validate_readonly_subagent_definitions(self) -> None:
    """REQ-0501: code-explorer, code-architect, and code-reviewer are valid and read-only."""
    rep = validate_subagent_definitions(AGENTS_DIR)
    self.assertTrue(rep["is_valid"], msg=rep["errors"])
    for name in ("code-explorer", "code-architect", "code-reviewer"):
      self.assertIn(name, rep["agents"])
      self.assertEqual(
          set(rep["agents"][name]["tools"]), {"Glob", "Grep", "Read"}
      )

  def test_req0502_parallel_explorer_aggregation_and_file_line_citations(self) -> None:
    """REQ-0502: Aggregates parallel code-explorer reports and enforces file:line format."""
    reports = [
        {
            "entry_points": ["src/auth/router.py:42"],
            "call_chain": ["src/auth/router.py:42", "src/auth/service.py:108"],
            "essential_files": ["src/auth/router.py", "src/auth/service.py"],
        },
        {
            "entry_points": ["src/auth/middleware.py:19"],
            "call_chain": ["src/auth/middleware.py:19", "src/auth/token_store.py:77"],
            "essential_files": ["src/auth/service.py", "src/auth/token_store.py"],
        },
    ]
    agg = aggregate_explorer_findings(reports)
    self.assertEqual(agg["explorer_count"], 2)
    self.assertEqual(len(agg["essential_files"]), 3)

    with self.assertRaises(ValueError):
      aggregate_explorer_findings([
          {"entry_points": ["invalid_citation_without_line"], "call_chain": []},
          {"entry_points": ["src/a.py:10"], "call_chain": []},
      ])

  def test_req0503_phase3_clarifying_questions_circuit_breaker(self) -> None:
    """REQ-0503: Blocks Phase 4 Architecture until all Phase 3 questions are answered."""
    pipe = FeatureDevPipeline("Add OAuthPKCE session refresh")
    pipe.complete_phase2_exploration([
        {"entry_points": ["src/auth.py:10"], "call_chain": ["src/auth.py:10"], "essential_files": ["src/auth.py"]},
        {"entry_points": ["src/db.py:20"], "call_chain": ["src/db.py:20"], "essential_files": ["src/db.py"]},
    ])
    q1 = "Should expired refresh tokens revoke the entire token family?"
    pipe.register_phase3_questions([q1])

    proposals = [
        {"lens": "minimal_changes", "summary": "In-place check", "files_to_touch": ["src/auth.py"], "tradeoffs": "Fast"},
        {"lens": "clean_architecture", "summary": "TokenFamily aggregate", "files_to_touch": ["src/domain.py"], "tradeoffs": "Clean"},
        {"lens": "pragmatic_balance", "summary": "Service-layer guard", "files_to_touch": ["src/service.py"], "tradeoffs": "Balanced"},
    ]
    with self.assertRaises(ClarificationGateError):
      pipe.advance_to_phase4_architecture(proposals)

    pipe.answer_phase3_question(q1, "Yes, revoke the entire token family on replay.")
    options = pipe.advance_to_phase4_architecture(proposals)
    self.assertEqual(len(options), 3)

  def test_req0504_phase4_trilens_synthesis_and_human_approval_gate(self) -> None:
    """REQ-0504: Requires Minimal, Clean, and Pragmatic lenses and explicit human selection."""
    with self.assertRaises(ValueError):
      synthesize_architecture_options([{"lens": "minimal_changes", "summary": "Only one"}])

    pipe = FeatureDevPipeline("Add rate limiting")
    pipe.complete_phase2_exploration([
        {"entry_points": ["src/api.py:1"], "call_chain": [], "essential_files": ["src/api.py"]},
        {"entry_points": ["src/lim.py:1"], "call_chain": [], "essential_files": ["src/lim.py"]},
    ])
    pipe.register_phase3_questions(["Per-IP or per-API-key?"])
    pipe.answer_phase3_question("Per-IP or per-API-key?", "Per-API-key.")
    pipe.advance_to_phase4_architecture([
        {"lens": "minimal_changes", "summary": "Decorator", "files_to_touch": ["src/api.py"], "tradeoffs": "Minimal"},
        {"lens": "clean_architecture", "summary": "Middleware", "files_to_touch": ["src/mw.py"], "tradeoffs": "Clean"},
        {"lens": "pragmatic_balance", "summary": "TokenBucket", "files_to_touch": ["src/tb.py"], "tradeoffs": "Balanced"},
    ])

    with self.assertRaises(ArchitectureApprovalGateError):
      pipe.approve_architecture_and_implement("non_existent_lens", ["src/tb.py"])

    res = pipe.approve_architecture_and_implement("pragmatic_balance", ["src/tb.py"])
    self.assertEqual(res["selected_architecture"], "pragmatic_balance")

  def test_req0505_phase6_reviewer_confidence_80_filter(self) -> None:
    """REQ-0505: Retains only code-reviewer findings with confidence >= 80."""
    raw_findings = [
        {
            "category": "critical_bugs",
            "confidence": 92,
            "location": "src/tb.py:44",
            "description": "Unchecked division by zero when refill_rate is 0",
            "fix_suggestion": "Validate refill_rate > 0 in __post_init__",
        },
        {
            "category": "simplicity_improvements",
            "confidence": 65,
            "location": "src/tb.py:12",
            "description": "Could rename local variable",
            "fix_suggestion": "Optional rename",
        },
        {
            "category": "convention_violations",
            "confidence": 85,
            "location": "src/tb.py:88",
            "description": "Uses float instead of MoneyCents integer",
            "fix_suggestion": "Use MoneyCents",
        },
    ]
    filtered = filter_review_findings(raw_findings, min_confidence=80)
    self.assertEqual(filtered["retained_count"], 2)
    self.assertEqual(filtered["suppressed_low_confidence_count"], 1)
    self.assertEqual(
        filtered["high_confidence_findings"][0]["confidence"], 92
    )


if __name__ == "__main__":
  unittest.main()
