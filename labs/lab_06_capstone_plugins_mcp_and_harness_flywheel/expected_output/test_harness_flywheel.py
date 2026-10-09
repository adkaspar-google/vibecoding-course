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

"""Unit tests for Lab 06: Plugins, MCP Servers, Hooks & The On-the-Loop Harness Flywheel."""

from __future__ import annotations

from pathlib import Path
import unittest
from harness_flywheel import (
    MCPHarnessServer,
    classify_skill_vs_plugin,
    evaluate_pre_tool_use_hook,
    route_harness_flywheel_improvement,
    validate_plugin_bundle,
)

PLUGIN_DIR = Path(__file__).resolve().parent / "vibe-engineering-plugin"


class TestPluginsMcpAndHarnessFlywheel(unittest.TestCase):
  """Verifies REQ-0601 through REQ-0606."""

  def test_req0601_validate_dual_harness_plugin_manifests(self) -> None:
    """REQ-0601: Validates plugin bundle on both 'claude' and 'agy' harnesses."""
    claude_rep = validate_plugin_bundle(PLUGIN_DIR, harness="claude")
    self.assertTrue(claude_rep["is_valid"], msg=claude_rep["errors"])
    self.assertEqual(claude_rep["plugin_name"], "vibe-engineering-kit")
    self.assertEqual(claude_rep["version"], "1.2.0")
    self.assertIn(
        "/vibe-engineering-kit:harness-audit", claude_rep["namespaced_skills"]
    )

    agy_rep = validate_plugin_bundle(PLUGIN_DIR, harness="agy")
    self.assertTrue(agy_rep["is_valid"], msg=agy_rep["errors"])
    self.assertEqual(agy_rep["plugin_name"], "vibe-engineering-kit")

  def test_req0602_pre_tool_use_hook_blocks_immutable_verifiers(self) -> None:
    """REQ-0602: PreToolUse hook blocks edits to adversarial_tests/ and expected_output/."""
    blocked = evaluate_pre_tool_use_hook({
        "tool_name": "Edit",
        "tool_input": {"file_path": "labs/lab_01/adversarial_tests/test_x.py"},
    })
    self.assertEqual(blocked["decision"], "block")
    self.assertIn("adversarial_tests/", blocked["reason"])

    allowed = evaluate_pre_tool_use_hook({
        "tool_name": "Edit",
        "tool_input": {"file_path": "labs/lab_01/work/domain_ledger.py"},
    })
    self.assertEqual(allowed["decision"], "allow")

  def test_req0603_mcp_harness_server_jsonrpc_tools(self) -> None:
    """REQ-0603: Bundled MCP server handles tools/list and tools/call deterministically."""
    srv = MCPHarnessServer()
    listed = srv.handle_jsonrpc({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    tool_names = {t["name"] for t in listed["result"]["tools"]}
    self.assertEqual(tool_names, {"audit_vocabulary", "check_context_budget"})

    vocab_res = srv.handle_jsonrpc({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "audit_vocabulary",
            "arguments": {"keys": ["account_id", "tx_amt"]},
        },
    })
    self.assertFalse(vocab_res["result"]["is_clean"])
    self.assertEqual(vocab_res["result"]["drifted_keys"], ["tx_amt"])

  def test_req0604_skill_vs_plugin_packaging_decision(self) -> None:
    """REQ-0604: Distinguishes standalone Skill from versioned Plugin bundle."""
    skill_only = classify_skill_vs_plugin({
        "needs_mcp_server": False,
        "needs_lifecycle_hooks": False,
        "needs_bundled_subagents": False,
    })
    self.assertEqual(skill_only["recommended_package"], "STANDALONE_SKILL")

    plugin_pkg = classify_skill_vs_plugin({
        "needs_mcp_server": True,
        "needs_lifecycle_hooks": True,
    })
    self.assertEqual(plugin_pkg["recommended_package"], "PLUGIN")

  def test_req0605_on_the_loop_flywheel_and_sdd_escalation(self) -> None:
    """REQ-0605: Routes failures to Harness layers and escalates brownfield drift to SDD."""
    r_rule = route_harness_flywheel_improvement(
        {"failure_type": "wrong_test_or_build_command"}
    )
    self.assertEqual(r_rule["target_layer"], "ROOT_CONTEXT_RULE")

    r_mem = route_harness_flywheel_improvement(
        {"failure_type": "repeated_user_preference_correction"}
    )
    self.assertEqual(r_mem["target_layer"], "AUTO_MEMORY")

    r_skill = route_harness_flywheel_improvement(
        {"failure_type": "procedural_domain_workflow_error"}
    )
    self.assertEqual(r_skill["target_layer"], "CURATED_SKILL")

    r_hook = route_harness_flywheel_improvement(
        {"failure_type": "modified_immutable_test_file"}
    )
    self.assertEqual(r_hook["target_layer"], "PRE_TOOL_USE_HOOK")

    r_sdd = route_harness_flywheel_improvement({
        "failure_type": "multi_service_spec_drift",
        "services_affected": 4,
        "has_cross_service_contract_drift": True,
    })
    self.assertEqual(r_sdd["target_layer"], "ESCALATE_TO_SDD_SPEC")


if __name__ == "__main__":
  unittest.main()
