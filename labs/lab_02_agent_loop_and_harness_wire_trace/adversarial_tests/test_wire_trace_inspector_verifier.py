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

"""Immutable adversarial verifier for Lab 02 (REQ-0201 through REQ-0206)."""

from __future__ import annotations

import unittest

import wire_trace_inspector as wti


class TestLab02WireTraceInspectorVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 02."""

  def test_req0201_three_layer_agent_stack_classifier(self) -> None:
    """REQ-0201: Classify components across Layer 1 (Model API), Layer 2 (Toolkits/MCP), Layer 3 (Harness)."""
    self.assertEqual(
        wti.classify_stack_component("anthropic:claude-sonnet-4-5"),
        wti.AgentStackLayer.LAYER_1_MODEL_API,
    )
    self.assertEqual(
        wti.classify_stack_component("Bash"),
        wti.AgentStackLayer.LAYER_2_TOOLKIT_AND_MCP,
    )
    self.assertEqual(
        wti.classify_stack_component("mcp__github__create_issue"),
        wti.AgentStackLayer.LAYER_2_TOOLKIT_AND_MCP,
    )
    self.assertEqual(
        wti.classify_stack_component("CLAUDE.md"),
        wti.AgentStackLayer.LAYER_3_AGENT_HARNESS,
    )
    self.assertEqual(
        wti.classify_stack_component("PreToolUse"),
        wti.AgentStackLayer.LAYER_3_AGENT_HARNESS,
    )

  def test_req0202_agentic_loop_phase_and_verification_audit(self) -> None:
    """REQ-0202: Classify Gather Context -> Take Action -> Verify Results and flag unverified edits."""
    unverified = [
        wti.ToolTurn("Grep", "def settle"),
        wti.ToolTurn("Edit", "ledger.py"),
    ]
    bad_audit = wti.audit_loop_completion(unverified)
    self.assertTrue(bad_audit.has_unverified_mutation)
    self.assertFalse(bad_audit.is_complete_loop)

    verified = [
        wti.ToolTurn("Read", "ledger.py"),
        wti.ToolTurn("Edit", "ledger.py"),
        wti.ToolTurn("Bash", "./self_diagnose_all.sh"),
    ]
    good_audit = wti.audit_loop_completion(verified)
    self.assertFalse(good_audit.has_unverified_mutation)
    self.assertTrue(good_audit.is_complete_loop)

  def test_req0203_wire_payload_token_breakdown(self) -> None:
    """REQ-0203: Inspect HTTP/JSONL wire payload across system, standing_context, tool_schemas, messages."""
    payload = wti.WireTracePayload(
        system_prompt="You are a concise coding agent.",
        standing_context="# CLAUDE.md\nRun `python3 -m unittest`",
        tool_schemas=wti.build_swiss_army_knife_schemas(),
        messages=[{"role": "user", "content": "Run the test suite and fix any failure in ledger.py"}],
    )
    report = wti.inspect_wire_payload(payload)
    self.assertGreater(report.system_tokens, 0)
    self.assertGreater(report.standing_context_tokens, 0)
    self.assertGreater(report.tool_schema_tokens, 0)
    self.assertGreater(report.conversation_tokens, 0)
    self.assertEqual(
        report.total_tokens,
        report.system_tokens
        + report.standing_context_tokens
        + report.tool_schema_tokens
        + report.conversation_tokens,
    )

  def test_req0204_swiss_army_knife_vs_150_tool_bloat(self) -> None:
    """REQ-0204: Flag 150-tool CRUD schema bloat (>3x conversation) and verify >90% consolidation savings."""
    bloated_schemas = [
        {
            "name": f"mcp__crud_tool_{i}",
            "description": "Low-level REST wrapper with verbose parameter descriptions " * 12,
            "parameters": {"type": "object", "properties": {"id": {"type": "string"}}},
        }
        for i in range(150)
    ]
    payload = wti.WireTracePayload(
        system_prompt="System prompt",
        standing_context="# GEMINI.md\nRun `python3 -m unittest`",
        tool_schemas=bloated_schemas,
        messages=[{"role": "user", "content": "Check git status."}],
    )
    audit = wti.audit_tool_schema_bloat(payload, max_schema_to_conversation_ratio=3.0)
    self.assertTrue(audit.is_bloated)
    self.assertEqual(audit.tool_count, 150)
    self.assertGreater(audit.schema_to_conversation_ratio, 3.0)
    self.assertGreaterEqual(audit.token_reduction_ratio, 0.90)
    self.assertEqual(audit.recommended_primitives, ("Bash", "Read", "Edit", "Grep", "LSP"))

  def test_req0205_standing_context_overfitting_audit(self) -> None:
    """REQ-0205: Flag standing context files that exceed 60 lines or omit test commands."""
    bloated_md = "\n".join(f"- Rule {i}: never do X" for i in range(85))
    bad = wti.audit_standing_context(bloated_md, max_lines=60)
    self.assertTrue(bad.is_overfitted)
    self.assertFalse(bad.has_test_command)

    lean_md = "# CLAUDE.md\n- Test: `CI=true python3 -m unittest`\n- Docs: @docs/architecture.md\n"
    good = wti.audit_standing_context(lean_md, max_lines=60)
    self.assertFalse(good.is_overfitted)
    self.assertTrue(good.has_test_command)

  def test_req0206_runaway_tool_failure_circuit_breaker(self) -> None:
    """REQ-0206: Trip circuit breaker when identical tool call fails 3 consecutive times."""
    turns = [
        wti.ToolTurn("Bash", "python3 -m unittest", is_error=True, error_message="ImportError"),
        wti.ToolTurn("Bash", "python3 -m unittest", is_error=True, error_message="ImportError"),
        wti.ToolTurn("Bash", "python3 -m unittest", is_error=True, error_message="ImportError"),
    ]
    status = wti.detect_runaway_tool_loop(turns, max_identical_failures=3)
    self.assertTrue(status.tripped)
    self.assertEqual(status.consecutive_failures, 3)
    self.assertEqual(status.repeated_signature, "Bash:python3 -m unittest")


if __name__ == "__main__":
  unittest.main()
