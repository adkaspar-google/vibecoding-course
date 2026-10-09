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

"""Lab 05 Reference Solution: Context Primitives, 60-Line Map & Persistent Memory.

Implements:
- REQ-0501: Three Context Primitives Classifier (Prompts/Slash Commands, Rules, Skills).
- REQ-0502: 150-Instruction Compliance Cliff Auditor & 60-Line Root Map Compiler.
- REQ-0503: Dual-Harness Path-Scoped Rule Validator (.agents/rules/ & .claude/rules/).
- REQ-0504: Provenance-Tagged Memory Formatter (#direct vs. #commit/#time/#session).
- REQ-0505: 200-Line Startup Memory Cap & Stale Commit Pruner.
- REQ-0506: Git-Worktree Shared Memory Path Resolver.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


VALID_AGY_RULE_TRIGGERS = frozenset({"always_on", "model_decision", "glob", "manual"})


class ContextPrimitive(str, Enum):
  """The Three Context Primitives in Harness Engineering Layer 1 (REQ-0501)."""

  PROMPT_OR_SLASH_COMMAND = "PROMPT_OR_SLASH_COMMAND"
  STANDING_RULE = "STANDING_RULE"
  LAZY_LOADED_SKILL = "LAZY_LOADED_SKILL"


def classify_context_primitive(
    is_per_turn_intent: bool,
    is_multi_step_procedure: bool,
    applies_every_session: bool,
) -> ContextPrimitive:
  """Classifies an instruction artifact into Prompt/Command, Standing Rule, or Skill (REQ-0501)."""
  if is_per_turn_intent and not applies_every_session:
    return ContextPrimitive.PROMPT_OR_SLASH_COMMAND
  if is_multi_step_procedure:
    return ContextPrimitive.LAZY_LOADED_SKILL
  return ContextPrimitive.STANDING_RULE


@dataclass(frozen=True)
class InstructionBudgetAudit:
  """Audit of standing instruction count against the 150-instruction compliance cliff (REQ-0502)."""

  instruction_count: int
  cliff_threshold: int
  exceeds_cliff: bool
  estimated_compliance_rate: float


def audit_instruction_compliance_budget(
    instruction_count: int,
    cliff_threshold: int = 150,
) -> InstructionBudgetAudit:
  """Evaluates standing instructions against the 150-instruction compliance cliff (REQ-0502)."""
  if instruction_count < 0:
    raise ValueError("instruction_count must be non-negative")
  exceeds = instruction_count > cliff_threshold
  if not exceeds:
    rate = round(max(0.88, 1.0 - (instruction_count / float(cliff_threshold)) * 0.10), 4)
  else:
    overflow = instruction_count - cliff_threshold
    rate = round(max(0.35, 0.85 - (overflow / 100.0) * 0.25), 4)
  return InstructionBudgetAudit(
      instruction_count=instruction_count,
      cliff_threshold=cliff_threshold,
      exceeds_cliff=exceeds,
      estimated_compliance_rate=rate,
  )


def compile_root_context_map(
    project_name: str,
    commands: list[str],
    architecture_items: list[str],
    on_demand_docs: list[str],
    max_lines: int = 60,
) -> str:
  """Compiles a concise <=60-line CLAUDE.md / GEMINI.md / AGENTS.md map with @docs/*.md imports (REQ-0502)."""
  if not on_demand_docs:
    raise ValueError("on_demand_docs must contain at least one @docs/*.md lazy reference")

  lines: list[str] = [f"# {project_name} — Persistent Project Context", "", "## Commands & Environment"]
  lines.extend(f"- {cmd.strip()}" for cmd in commands)
  lines.extend(["", "## Architecture & Directory Map"])
  lines.extend(f"- {item.strip()}" for item in architecture_items)
  lines.extend(["", "## On-Demand References"])
  for doc in on_demand_docs:
    ref = doc.strip() if doc.strip().startswith("@") else f"@{doc.strip()}"
    lines.append(f"- Reference {ref}")

  if len(lines) > max_lines:
    raise ValueError(f"Compiled root context has {len(lines)} lines, exceeding max_lines={max_lines}")
  return "\n".join(lines) + "\n"


def validate_scoped_rule(frontmatter: dict[str, Any], body: str) -> tuple[bool, list[str]]:
  """Validates .agents/rules/*.md ('trigger') and .claude/rules/*.md ('paths') scoped rules (REQ-0503)."""
  errors: list[str] = []
  if not body or not body.strip():
    errors.append("Rule body must be non-empty")

  has_agy_trigger = "trigger" in frontmatter
  has_claude_paths = "paths" in frontmatter

  if not has_agy_trigger and not has_claude_paths:
    errors.append("Rule frontmatter must define either 'trigger' (.agents/rules) or 'paths' (.claude/rules)")

  if has_agy_trigger:
    trig = frontmatter["trigger"]
    if trig not in VALID_AGY_RULE_TRIGGERS:
      errors.append(f"Invalid Antigravity rule trigger '{trig}'")
    if trig == "glob" and not frontmatter.get("globs"):
      errors.append("Antigravity rule with trigger='glob' must specify 'globs'")

  if has_claude_paths:
    paths = frontmatter["paths"]
    if not isinstance(paths, list) or not paths or not all(isinstance(p, str) and p.strip() for p in paths):
      errors.append("Claude Code rule 'paths' must be a non-empty list of glob strings")

  return (len(errors) == 0, errors)


@dataclass(frozen=True)
class MemoryEntry:
  """Structured cross-session memory observation (REQ-0504)."""

  statement: str
  is_explicit_user_directive: bool = False
  commit_sha: str | None = None
  date_str: str | None = None
  session_id: str | None = None


def format_memory_entry(entry: MemoryEntry) -> str:
  """Formats a memory bullet enforcing #direct strictly for user directives and #commit/#time/#session for indirect facts (REQ-0504)."""
  stmt = entry.statement.strip()
  if not stmt:
    raise ValueError("Memory statement must be non-empty")
  if "#direct" in stmt and not entry.is_explicit_user_directive:
    raise ValueError("Indirect agent observations must never contain '#direct'")

  tags: list[str] = []
  if entry.is_explicit_user_directive:
    tags.append("#direct")
  if entry.commit_sha:
    tags.append(f"#commit:{entry.commit_sha}")
  if entry.date_str:
    tags.append(f"#time:{entry.date_str}")
  if entry.session_id:
    tags.append(f"#session:{entry.session_id}")

  if not entry.is_explicit_user_directive and not tags:
    raise ValueError("Indirect codebase observations must include at least one relativity tag (#commit, #time, or #session)")

  suffix = (" " + " ".join(tags)) if tags else ""
  return f"- {stmt}{suffix}"


@dataclass(frozen=True)
class MemoryCompactionResult:
  """Result of pruning stale commits and capping MEMORY.md / KNOWLEDGE.md at 200 lines (REQ-0505)."""

  active_lines: tuple[str, ...]
  overflow_topic_lines: tuple[str, ...]
  pruned_stale_count: int


def prune_and_cap_memory(
    entries: list[MemoryEntry],
    superseded_commits: set[str] | None = None,
    max_lines: int = 200,
) -> MemoryCompactionResult:
  """Prunes entries tied to superseded commits and caps startup memory at max_lines (REQ-0505)."""
  stale_set = superseded_commits or set()
  formatted_kept: list[str] = []
  pruned = 0

  for entry in entries:
    if entry.commit_sha and entry.commit_sha in stale_set and not entry.is_explicit_user_directive:
      pruned += 1
      continue
    formatted_kept.append(format_memory_entry(entry))

  active = tuple(formatted_kept[:max_lines])
  overflow = tuple(formatted_kept[max_lines:])
  return MemoryCompactionResult(
      active_lines=active,
      overflow_topic_lines=overflow,
      pruned_stale_count=pruned,
  )


def resolve_project_memory_paths(project_slug: str) -> dict[str, str]:
  """Returns canonical worktree-shared memory file paths for Claude Code and Antigravity (REQ-0506)."""
  slug = project_slug.strip().strip("/")
  if not slug:
    raise ValueError("project_slug must be non-empty")
  return {
      "claude": f"~/.claude/projects/{slug}/memory/MEMORY.md",
      "agy": f"~/.gemini/antigravity/knowledge/{slug}/KNOWLEDGE.md",
  }
