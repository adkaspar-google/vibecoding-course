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

"""Lab 02 Reference Solution: Core Agentic Loop & Harness Wire-Trace Inspector.

Implements:
- REQ-0201: 3-Layer Agent Stack Classifier (andrewyng/aisuite & Skills Map 3.5).
- REQ-0202: Core Agentic Loop Phase Classifier (Gather Context -> Take Action -> Verify Results).
- REQ-0203: Wireshark-Style HTTP/JSONL Wire-Trace Inspector (Stanford CS146S Lecture 2).
- REQ-0204: Swiss Army Knife Primitive Consolidation vs. 150-Tool CRUD Schema Bloat Detector.
- REQ-0205: Standing Context Overfitting Auditor (CLAUDE.md / GEMINI.md <= 60 lines).
- REQ-0206: Runaway Tool-Failure Loop Circuit Breaker.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any


SWISS_ARMY_KNIFE_PRIMITIVES: tuple[str, ...] = (
    "Bash",
    "Read",
    "Edit",
    "Grep",
    "LSP",
)

LAYER_1_KEYWORDS = frozenset({
    "chatcompletions",
    "provider:model",
    "tokenizer",
    "sampling",
    "kv_cache",
    "reasoning_effort",
})
LAYER_2_KEYWORDS = frozenset({
    "bash",
    "read",
    "edit",
    "write",
    "grep",
    "glob",
    "lsp",
    "git",
    "mcp",
})
LAYER_3_KEYWORDS = frozenset({
    "claude.md",
    "gemini.md",
    "agents.md",
    "plan_mode",
    "skill.md",
    "subagentfirewall",
    "pretooluse",
    "posttooluse",
    "memory.md",
    "knowledge.md",
    "compaction",
})


class AgentStackLayer(str, Enum):
  """3-Layer Agent Stack (andrewyng/aisuite & OpenWorker, REQ-0201)."""

  LAYER_1_MODEL_API = "LAYER_1_MODEL_API"
  LAYER_2_TOOLKIT_AND_MCP = "LAYER_2_TOOLKIT_AND_MCP"
  LAYER_3_AGENT_HARNESS = "LAYER_3_AGENT_HARNESS"


def classify_stack_component(component_name: str) -> AgentStackLayer:
  """Classifies an architectural component into the 3-Layer Agent Stack (REQ-0201)."""
  norm = component_name.strip().lower()
  if norm.startswith("mcp__") or norm in LAYER_2_KEYWORDS:
    return AgentStackLayer.LAYER_2_TOOLKIT_AND_MCP
  if ":" in norm or norm in LAYER_1_KEYWORDS:
    return AgentStackLayer.LAYER_1_MODEL_API
  if norm in LAYER_3_KEYWORDS or norm.endswith(".md") or "hook" in norm or "harness" in norm:
    return AgentStackLayer.LAYER_3_AGENT_HARNESS
  raise ValueError(f"Unrecognized stack component: '{component_name}'")


class LoopPhase(str, Enum):
  """3-Phase Core Agentic Loop (Claude Code 101 & Antigravity CLI, REQ-0202)."""

  GATHER_CONTEXT = "GATHER_CONTEXT"
  TAKE_ACTION = "TAKE_ACTION"
  VERIFY_RESULTS = "VERIFY_RESULTS"


@dataclass(frozen=True)
class ToolTurn:
  """Single tool invocation turn inside an agent wire trace."""

  tool_name: str
  command_or_target: str = ""
  is_error: bool = False
  error_message: str = ""


def classify_tool_call_phase(tool_name: str, command_or_target: str = "") -> LoopPhase:
  """Classifies a tool call into Gather Context, Take Action, or Verify Results (REQ-0202)."""
  norm_tool = tool_name.strip()
  cmd_lower = command_or_target.strip().lower()

  if norm_tool in ("Read", "Grep", "Glob", "LSP", "view_file", "code_search"):
    return LoopPhase.GATHER_CONTEXT

  if norm_tool in ("Edit", "Write", "replace_file_content", "write_to_file"):
    return LoopPhase.TAKE_ACTION

  if norm_tool in ("Bash", "run_command", "Browser", "browser"):
    if any(
        kw in cmd_lower
        for kw in ("unittest", "pytest", "self_diagnose", "playwright", "/browser", "verify", "lint")
    ):
      return LoopPhase.VERIFY_RESULTS
    if any(
        kw in cmd_lower
        for kw in ("git status", "git diff", "git log", "cat ", "ls ", "head ")
    ):
      return LoopPhase.GATHER_CONTEXT
    return LoopPhase.TAKE_ACTION

  return LoopPhase.TAKE_ACTION


@dataclass(frozen=True)
class LoopAuditResult:
  """Verification audit of a multi-turn agentic loop (REQ-0202)."""

  phases_observed: tuple[LoopPhase, ...]
  has_unverified_mutation: bool
  is_complete_loop: bool


def audit_loop_completion(turns: list[ToolTurn]) -> LoopAuditResult:
  """Verifies that any TAKE_ACTION mutation is followed by a VERIFY_RESULTS turn (REQ-0202)."""
  phases = [classify_tool_call_phase(t.tool_name, t.command_or_target) for t in turns]
  last_action_idx = -1
  last_verify_idx = -1
  for idx, phase in enumerate(phases):
    if phase == LoopPhase.TAKE_ACTION:
      last_action_idx = idx
    elif phase == LoopPhase.VERIFY_RESULTS:
      last_verify_idx = idx

  has_unverified_mutation = last_action_idx != -1 and last_verify_idx < last_action_idx
  is_complete = (
      LoopPhase.GATHER_CONTEXT in phases
      and LoopPhase.TAKE_ACTION in phases
      and LoopPhase.VERIFY_RESULTS in phases
      and not has_unverified_mutation
  )
  return LoopAuditResult(
      phases_observed=tuple(phases),
      has_unverified_mutation=has_unverified_mutation,
      is_complete_loop=is_complete,
  )


def estimate_tokens(text_or_obj: Any) -> int:
  """Deterministic token estimator (~4 chars per token on serialized JSON/text)."""
  if isinstance(text_or_obj, str):
    raw = text_or_obj
  else:
    raw = json.dumps(text_or_obj, sort_keys=True)
  if not raw:
    return 0
  return max(1, (len(raw) + 3) // 4)


@dataclass(frozen=True)
class WireTracePayload:
  """HTTP/JSONL request payload sent by a coding agent harness on the wire (REQ-0203)."""

  system_prompt: str
  standing_context: str
  tool_schemas: list[dict[str, Any]]
  messages: list[dict[str, Any]]


@dataclass(frozen=True)
class WireInspectionReport:
  """Token breakdown across the 4 wire segments (REQ-0203)."""

  system_tokens: int
  standing_context_tokens: int
  tool_schema_tokens: int
  conversation_tokens: int
  total_tokens: int
  schema_to_conversation_ratio: float


def inspect_wire_payload(payload: WireTracePayload) -> WireInspectionReport:
  """Computes segment token distribution across an agent wire payload (REQ-0203)."""
  sys_t = estimate_tokens(payload.system_prompt)
  stand_t = estimate_tokens(payload.standing_context)
  schema_t = sum(estimate_tokens(schema) for schema in payload.tool_schemas)
  conv_t = max(1, sum(estimate_tokens(msg) for msg in payload.messages))
  total = sys_t + stand_t + schema_t + conv_t
  ratio = round(schema_t / float(conv_t), 2)
  return WireInspectionReport(
      system_tokens=sys_t,
      standing_context_tokens=stand_t,
      tool_schema_tokens=schema_t,
      conversation_tokens=conv_t,
      total_tokens=total,
      schema_to_conversation_ratio=ratio,
  )


@dataclass(frozen=True)
class ToolBloatAudit:
  """Comparison of bloated CRUD tool catalogs vs. Swiss Army Knife primitives (REQ-0204)."""

  is_bloated: bool
  tool_count: int
  schema_to_conversation_ratio: float
  original_schema_tokens: int
  consolidated_schema_tokens: int
  token_reduction_ratio: float
  recommended_primitives: tuple[str, ...]


def build_swiss_army_knife_schemas() -> list[dict[str, Any]]:
  """Returns the 5 compact Swiss Army Knife tool schemas (Bash, Read, Edit, Grep, LSP)."""
  return [
      {
          "name": name,
          "description": f"Compact general-purpose {name} primitive.",
          "parameters": {"type": "object", "properties": {"target": {"type": "string"}}},
      }
      for name in SWISS_ARMY_KNIFE_PRIMITIVES
  ]


def audit_tool_schema_bloat(
    payload: WireTracePayload,
    max_schema_to_conversation_ratio: float = 3.0,
) -> ToolBloatAudit:
  """Detects tool-schema bloat (>3x conversation tokens) and computes Swiss Army Knife savings (REQ-0204)."""
  report = inspect_wire_payload(payload)
  compact_schemas = build_swiss_army_knife_schemas()
  compact_tokens = sum(estimate_tokens(s) for s in compact_schemas)
  orig_tokens = max(1, report.tool_schema_tokens)
  reduction = round(max(0.0, (orig_tokens - compact_tokens) / float(orig_tokens)), 4)
  is_bloated = (
      report.schema_to_conversation_ratio > max_schema_to_conversation_ratio
      or len(payload.tool_schemas) > 25
  )
  return ToolBloatAudit(
      is_bloated=is_bloated,
      tool_count=len(payload.tool_schemas),
      schema_to_conversation_ratio=report.schema_to_conversation_ratio,
      original_schema_tokens=report.tool_schema_tokens,
      consolidated_schema_tokens=compact_tokens,
      token_reduction_ratio=reduction,
      recommended_primitives=SWISS_ARMY_KNIFE_PRIMITIVES,
  )


@dataclass(frozen=True)
class StandingContextAudit:
  """Audit of CLAUDE.md / GEMINI.md / AGENTS.md against overfitting (REQ-0205)."""

  line_count: int
  is_overfitted: bool
  has_test_command: bool
  issues: tuple[str, ...]


def audit_standing_context(
    standing_context_text: str,
    max_lines: int = 60,
) -> StandingContextAudit:
  """Audits CLAUDE.md / GEMINI.md for line-budget compliance and test commands (REQ-0205)."""
  lines = standing_context_text.splitlines()
  line_count = len(lines)
  lower = standing_context_text.lower()
  has_test_cmd = any(
      cmd in lower for cmd in ("unittest", "pytest", "self_diagnose", "npm test", "cargo test")
  )
  issues: list[str] = []
  if line_count > max_lines:
    issues.append(
        f"Standing context has {line_count} lines (exceeds {max_lines}-line map budget; offload details to @docs/*.md)"
    )
  if not has_test_cmd:
    issues.append("Standing context is missing an explicit test/verification command")
  return StandingContextAudit(
      line_count=line_count,
      is_overfitted=line_count > max_lines or not has_test_cmd,
      has_test_command=has_test_cmd,
      issues=tuple(issues),
  )


@dataclass(frozen=True)
class LoopCircuitBreakerStatus:
  """Runaway loop detection status across consecutive failing tool calls (REQ-0206)."""

  tripped: bool
  consecutive_failures: int
  repeated_signature: str | None


def detect_runaway_tool_loop(
    turns: list[ToolTurn],
    max_identical_failures: int = 3,
) -> LoopCircuitBreakerStatus:
  """Trips when the same (tool_name, command_or_target) fails >= max_identical_failures times in a row (REQ-0206)."""
  last_sig: str | None = None
  streak = 0
  for turn in turns:
    sig = f"{turn.tool_name}:{turn.command_or_target.strip()}"
    if turn.is_error:
      if sig == last_sig:
        streak += 1
      else:
        last_sig = sig
        streak = 1
      if streak >= max_identical_failures:
        return LoopCircuitBreakerStatus(
            tripped=True,
            consecutive_failures=streak,
            repeated_signature=sig,
        )
    else:
      last_sig = None
      streak = 0
  return LoopCircuitBreakerStatus(
      tripped=False,
      consecutive_failures=streak,
      repeated_signature=last_sig,
  )
