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

"""Capstone: Plugin Manifest Validator, PreToolUse Hook Guard, MCP Server & Harness Flywheel.

Implements REQ-0601 through REQ-0605 for Lab 06:
- Dual-harness plugin validator (.claude-plugin/plugin.json & plugin.json)
- Deterministic PreToolUse hook blocking mutations to immutable verifier paths
- JSON-RPC 2.0 MCP tool server dispatcher with lazy vs eager schema accounting
- Skill vs. Plugin packaging decision classifier
- Kief Morris 'On-the-Loop' Harness Flywheel & SDD Escalation Router
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
KEBAB_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PROTECTED_DIRS = ("adversarial_tests/", "expected_output/")


def validate_plugin_bundle(
    plugin_dir: str | Path,
    harness: str = "claude",
) -> dict[str, Any]:
  """Validates a versioned plugin bundle for Claude Code or Antigravity (REQ-0601)."""
  root = Path(plugin_dir)
  errors: list[str] = []

  if harness == "claude":
    manifest_path = root / ".claude-plugin" / "plugin.json"
    mcp_path = root / ".mcp.json"
    hooks_path = root / "hooks" / "hooks.json"
  elif harness == "agy":
    manifest_path = root / "plugin.json"
    mcp_path = root / "mcp_config.json"
    hooks_path = root / "hooks.json"
  else:
    raise ValueError(f"Unsupported harness '{harness}'")

  if not manifest_path.is_file():
    errors.append(f"Missing plugin manifest: {manifest_path}")
    manifest: dict[str, Any] = {}
  else:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

  plugin_name = str(manifest.get("name", ""))
  version = str(manifest.get("version", ""))

  if not plugin_name or not KEBAB_PATTERN.match(plugin_name):
    errors.append(f"Invalid plugin name '{plugin_name}'; must be kebab-case")
  if not version or not SEMVER_PATTERN.match(version):
    errors.append(f"Invalid semantic version '{version}'; must match X.Y.Z")
  if not manifest.get("description"):
    errors.append("Plugin manifest missing 'description'")

  if not mcp_path.is_file():
    errors.append(f"Missing MCP configuration file: {mcp_path.name}")
  if not hooks_path.is_file():
    errors.append(f"Missing hooks configuration file: {hooks_path.name}")

  namespaced_skills: list[str] = []
  skills_dir = root / "skills"
  if skills_dir.is_dir():
    for child in sorted(skills_dir.iterdir()):
      if child.is_dir() and (child / "SKILL.md").is_file():
        namespaced_skills.append(f"/{plugin_name}:{child.name}")

  return {
      "is_valid": len(errors) == 0,
      "harness": harness,
      "plugin_name": plugin_name,
      "version": version,
      "namespaced_skills": tuple(namespaced_skills),
      "errors": tuple(errors),
  }


def evaluate_pre_tool_use_hook(event_payload: dict[str, Any]) -> dict[str, str]:
  """Evaluates a PreToolUse event and blocks edits to immutable verifiers (REQ-0602)."""
  tool_name = str(event_payload.get("tool_name", ""))
  tool_input = event_payload.get("tool_input", {}) or {}

  target_candidates = [
      str(tool_input.get("file_path", "")),
      str(tool_input.get("TargetFile", "")),
      str(tool_input.get("command", "")),
      str(tool_input.get("CommandLine", "")),
  ]

  mutating_tools = {
      "Edit",
      "Write",
      "MultiEdit",
      "replace_file_content",
      "write_to_file",
      "Bash",
      "run_command",
  }

  if tool_name in mutating_tools:
    for candidate in target_candidates:
      for protected in PROTECTED_DIRS:
        if protected in candidate:
          return {
              "decision": "block",
              "reason": (
                  f"PreToolUse guardrail blocked '{tool_name}' targeting "
                  f"immutable directory '{protected}'"
              ),
          }

  return {"decision": "allow", "reason": "Permitted by PreToolUse policy"}


class MCPHarnessServer:
  """Deterministic JSON-RPC 2.0 MCP server bundled inside the plugin (REQ-0603)."""

  TOOLS_SCHEMA = (
      {
          "name": "audit_vocabulary",
          "description": "Checks a payload for Ubiquitous Language synonym drift.",
          "inputSchema": {"type": "object", "properties": {"keys": {"type": "array"}}},
      },
      {
          "name": "check_context_budget",
          "description": "Checks whether token usage stays below the 60% degradation wall.",
          "inputSchema": {
              "type": "object",
              "properties": {"used_tokens": {"type": "integer"}, "limit_tokens": {"type": "integer"}},
          },
      },
  )

  def handle_jsonrpc(self, request: dict[str, Any]) -> dict[str, Any]:
    req_id = request.get("id", 1)
    method = str(request.get("method", ""))
    params = request.get("params", {}) or {}

    if method == "tools/list":
      return {
          "jsonrpc": "2.0",
          "id": req_id,
          "result": {"tools": list(self.TOOLS_SCHEMA)},
      }

    if method == "tools/call":
      tool_name = str(params.get("name", ""))
      args = params.get("arguments", {}) or {}
      if tool_name == "audit_vocabulary":
        keys = [str(k) for k in args.get("keys", [])]
        drifted = [k for k in keys if k in ("client_id", "tx_amt", "fee_float")]
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"drifted_keys": drifted, "is_clean": len(drifted) == 0},
        }
      if tool_name == "check_context_budget":
        used = int(args.get("used_tokens", 0))
        limit = max(1, int(args.get("limit_tokens", 200_000)))
        ratio = round(used / limit, 4)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "utilization_ratio": ratio,
                "healthy": ratio <= 0.60,
            },
        }
      return {
          "jsonrpc": "2.0",
          "id": req_id,
          "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
      }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Unsupported method: {method}"},
    }


def classify_skill_vs_plugin(requirements: dict[str, Any]) -> dict[str, str]:
  """Decides whether a capability should be packaged as a standalone Skill or a Plugin (REQ-0604)."""
  needs_mcp = bool(requirements.get("needs_mcp_server", False))
  needs_hooks = bool(requirements.get("needs_lifecycle_hooks", False))
  needs_subagents = bool(requirements.get("needs_bundled_subagents", False))
  needs_versioned_dist = bool(requirements.get("needs_versioned_distribution", False))

  if needs_mcp or needs_hooks or needs_subagents or needs_versioned_dist:
    return {
        "recommended_package": "PLUGIN",
        "rationale": (
            "Use a versioned Plugin (plugin.json) when bundling MCP servers, "
            "PreToolUse/Stop hooks, custom subagents, or cross-repo distribution."
        ),
    }
  return {
      "recommended_package": "STANDALONE_SKILL",
      "rationale": (
          "Use a standalone Skill (SKILL.md + optional references/scripts) for "
          "a self-contained procedural workflow without MCP servers or hooks."
      ),
  }


def route_harness_flywheel_improvement(failure_event: dict[str, Any]) -> dict[str, str]:
  """Routes an observed agent failure to the right On-the-Loop harness layer or SDD (REQ-0605).

  Implements Kief Morris's On-the-Loop Harness Engineering flywheel and the
  architectural boundary between Vibe Coding and Spec-Driven Development (SDD).
  """
  failure_type = str(failure_event.get("failure_type", ""))
  services_affected = int(failure_event.get("services_affected", 1))
  has_cross_service_contract_drift = bool(
      failure_event.get("has_cross_service_contract_drift", False)
  )

  if services_affected >= 3 or has_cross_service_contract_drift or failure_type == "multi_service_spec_drift":
    return {
        "target_layer": "ESCALATE_TO_SDD_SPEC",
        "artifact": "openspec/specs/<capability>/spec.md + conductor/tracks/<id>/plan.md",
        "action": (
            "Conversational vibe coding has reached its brownfield scale limit; "
            "transition to Spec-Driven Development (SDD) with persistent specs."
        ),
    }

  routing_map = {
      "wrong_test_or_build_command": (
          "ROOT_CONTEXT_RULE",
          "CLAUDE.md / GEMINI.md",
          "Add exact test/build command to root project context file.",
      ),
      "repeated_user_preference_correction": (
          "AUTO_MEMORY",
          "MEMORY.md / KNOWLEDGE.md (#direct)",
          "Persist explicit user correction in cross-session auto-memory.",
      ),
      "procedural_domain_workflow_error": (
          "CURATED_SKILL",
          ".claude/skills/<name>/SKILL.md or .agents/skills/<name>/SKILL.md",
          "Encode observed baseline failure delta into an experience-grounded skill.",
      ),
      "modified_immutable_test_file": (
          "PRE_TOOL_USE_HOOK",
          "hooks.json (PreToolUse)",
          "Enforce deterministic PreToolUse block on immutable test directories.",
      ),
      "missing_live_schema_or_telemetry_lookup": (
          "PLUGIN_MCP_TOOL",
          "plugin.json + mcp_config.json / .mcp.json",
          "Expose deterministic external lookup via a bundled MCP server tool.",
      ),
  }

  if failure_type not in routing_map:
    raise ValueError(f"Unrecognized failure_type '{failure_type}'")

  layer, artifact, action = routing_map[failure_type]
  return {
      "target_layer": layer,
      "artifact": artifact,
      "action": action,
  }
