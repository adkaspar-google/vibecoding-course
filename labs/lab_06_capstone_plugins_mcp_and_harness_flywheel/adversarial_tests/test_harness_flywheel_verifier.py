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

"""Immutable adversarial verifier for Lab 06 (REQ-0601..REQ-0606)."""

from __future__ import annotations

import os
from pathlib import Path
import unittest
from harness_flywheel import (
    MCPHarnessServer,
    classify_skill_vs_plugin,
    evaluate_pre_tool_use_hook,
    route_harness_flywheel_improvement,
    validate_plugin_bundle,
)


class TestLab06ImmutableVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 06."""

  def _target_dir(self) -> Path:
    env_target = os.environ.get("LAB06_TARGET_DIR")
    if env_target:
      return Path(env_target)
    return Path(__file__).resolve().parent.parent / "expected_output"

  def test_req0601_validates_both_claude_and_agy_plugin_layouts(self) -> None:
    pdir = self._target_dir() / "vibe-engineering-plugin"
    self.assertTrue(validate_plugin_bundle(pdir, "claude")["is_valid"])
    self.assertTrue(validate_plugin_bundle(pdir, "agy")["is_valid"])

  def test_req0602_blocks_shell_and_file_mutations_on_adversarial_tests(self) -> None:
    res = evaluate_pre_tool_use_hook({
        "tool_name": "run_command",
        "tool_input": {"CommandLine": "rm -rf labs/lab_06/adversarial_tests/"},
    })
    self.assertEqual(res["decision"], "block")

  def test_req0603_and_req0604_mcp_and_packaging_classifier(self) -> None:
    srv = MCPHarnessServer()
    out = srv.handle_jsonrpc({
        "jsonrpc": "2.0",
        "id": 9,
        "method": "tools/call",
        "params": {
            "name": "check_context_budget",
            "arguments": {"used_tokens": 90_000, "limit_tokens": 200_000},
        },
    })
    self.assertTrue(out["result"]["healthy"])
    self.assertEqual(
        classify_skill_vs_plugin({"needs_mcp_server": True})["recommended_package"],
        "PLUGIN",
    )

  def test_req0605_routes_multi_service_drift_to_sdd(self) -> None:
    r = route_harness_flywheel_improvement(
        {"failure_type": "multi_service_spec_drift", "services_affected": 3}
    )
    self.assertEqual(r["target_layer"], "ESCALATE_TO_SDD_SPEC")


if __name__ == "__main__":
  unittest.main()
