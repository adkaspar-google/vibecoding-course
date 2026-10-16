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

"""Unit tests for Lab 02 wire_trace_inspector.py (REQ-0201 through REQ-0206)."""

from __future__ import annotations

import unittest

import wire_trace_inspector as wti


class TestWireTraceInspector(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 02 (REQ-0201..REQ-0206)."""

  def test_req0201_three_layer_agent_stack_classifier(self) -> None:
    """Verifies REQ-0201: 3-Layer Agent Stack Classifier across Model API, Toolkit/MCP, and Harness."""
    self.assertEqual(
        wti.classify_stack_component("anthropic:claude-sonnet-4-6"),
        wti.AgentStackLayer.LAYER_1_MODEL_API,
    )
    self.assertEqual(
        wti.classify_stack_component("Bash"),
        wti.AgentStackLayer.LAYER_2_TOOLKIT_AND_MCP,
    )
    self.assertEqual(
        wti.classify_stack_component("GEMINI.md"),
        wti.AgentStackLayer.LAYER_3_AGENT_HARNESS,
    )

  def test_req0202_agentic_loop_phase_and_verification_audit(self) -> None:
    """Verifies REQ-0202: Core Agentic Loop Phase Classifier (Gather Context -> Take Action -> Verify Results)."""
    turns = [
        wti.ToolTurn("Read", "taskflow/ledger.py"),
        wti.ToolTurn("Edit", "taskflow/ledger.py"),
        wti.ToolTurn("Bash", "python3 -m unittest"),
    ]
    res = wti.audit_loop_completion(turns)
    self.assertTrue(res.is_complete_loop)
    self.assertFalse(res.has_unverified_mutation)

  def test_req0203_wireshark_style_wire_payload_inspector(self) -> None:
    """Verifies REQ-0203: Wireshark-Style HTTP/JSONL Wire-Trace Inspector token distribution."""
    payload = wti.WireTracePayload(
        system_prompt="You are a concise TaskFlow coding agent.",
        standing_context="# GEMINI.md\nRun `python3 -m unittest`",
        tool_schemas=wti.build_swiss_army_knife_schemas(),
        messages=[{"role": "user", "content": "Verify TaskFlow settlement tests."}],
    )
    report = wti.inspect_wire_payload(payload)
    self.assertEqual(
        report.total_tokens,
        report.system_tokens
        + report.standing_context_tokens
        + report.tool_schema_tokens
        + report.conversation_tokens,
    )

  def test_req0204_swiss_army_knife_consolidation_vs_schema_bloat(self) -> None:
    """Verifies REQ-0204: Swiss Army Knife Primitive Consolidation vs. 150-Tool CRUD Schema Bloat."""
    bloated_schemas = [
        {
            "name": f"mcp__taskflow_crud_{i}",
            "description": "Verbose REST wrapper schema " * 15,
            "parameters": {"type": "object", "properties": {"id": {"type": "string"}}},
        }
        for i in range(150)
    ]
    payload = wti.WireTracePayload(
        system_prompt="System",
        standing_context="# CLAUDE.md\nRun `python3 -m unittest`",
        tool_schemas=bloated_schemas,
        messages=[{"role": "user", "content": "Fix TaskFlow bug"}],
    )
    audit = wti.audit_tool_schema_bloat(payload)
    self.assertTrue(audit.is_bloated)
    self.assertGreaterEqual(audit.token_reduction_ratio, 0.90)

  def test_req0205_standing_context_overfitting_auditor(self) -> None:
    """Verifies REQ-0205: Standing Context Overfitting Auditor enforces <=60 lines and explicit test command."""
    lean = wti.audit_standing_context("# GEMINI.md\n- Test: `./self_diagnose_all.sh`\n", max_lines=60)
    self.assertFalse(lean.is_overfitted)
    self.assertTrue(lean.has_test_command)

    overfitted = wti.audit_standing_context("\n".join(f"Rule {i}" for i in range(80)), max_lines=60)
    self.assertTrue(overfitted.is_overfitted)

  def test_req0206_runaway_tool_failure_circuit_breaker(self) -> None:
    """Verifies REQ-0206: Runaway Tool-Failure Loop Circuit Breaker trips after 3 identical failures."""
    turns = [
        wti.ToolTurn("Bash", "python3 -m unittest", is_error=True),
        wti.ToolTurn("Bash", "python3 -m unittest", is_error=True),
        wti.ToolTurn("Bash", "python3 -m unittest", is_error=True),
    ]
    cb = wti.detect_runaway_tool_loop(turns, max_identical_failures=3)
    self.assertTrue(cb.tripped)
    self.assertEqual(cb.consecutive_failures, 3)


if __name__ == "__main__":
  unittest.main()
