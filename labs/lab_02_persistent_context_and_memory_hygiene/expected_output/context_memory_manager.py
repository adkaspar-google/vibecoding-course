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

"""Persistent Context (CLAUDE.md / GEMINI.md) & Auto-Memory Hygiene Engine.

Implements REQ-0201 through REQ-0205 for Lab 02:
- Root context validation with on-demand @path progressive reference extraction
- Git-worktree-aware project memory path resolution (~/.claude/projects/<project>/memory/ and ~/.gemini/antigravity/knowledge/<project>/)
- 200-line / 25 KB MEMORY.md & KNOWLEDGE.md compiler with topic overflow
- Epistemic provenance tagging (#direct strictly for explicit user statements)
- /context token budget & 60% degradation threshold auditor
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
from typing import Any


REQUIRED_CONTEXT_SECTIONS = (
    "Commands & Environment",
    "Architecture & Directory Map",
    "Core Conventions",
    "On-Demand References",
)

AT_REF_PATTERN = re.compile(r"(?:^|\s)@([A-Za-z0-9_./-]+\.md)\b")


@dataclass(frozen=True)
class RootContextValidationResult:
  """Validation report for CLAUDE.md or GEMINI.md / AGENTS.md (REQ-0201)."""

  is_valid: bool
  line_count: int
  missing_sections: tuple[str, ...]
  on_demand_refs: tuple[str, ...]
  errors: tuple[str, ...]


def validate_root_context_md(
    markdown_text: str,
    max_lines: int = 120,
) -> RootContextValidationResult:
  """Validates a root CLAUDE.md or GEMINI.md / AGENTS.md file (REQ-0201)."""
  lines = markdown_text.splitlines()
  line_count = len(lines)
  errors: list[str] = []

  if line_count == 0:
    errors.append("Context markdown file cannot be empty")
  if line_count > max_lines:
    errors.append(
        f"Context file has {line_count} lines, exceeding max_lines={max_lines}. "
        "Move detailed docs into @docs/*.md on-demand references."
    )

  missing: list[str] = []
  for section in REQUIRED_CONTEXT_SECTIONS:
    pattern = re.compile(rf"^##+\s+.*{re.escape(section)}", re.MULTILINE)
    if not pattern.search(markdown_text):
      missing.append(section)
      errors.append(f"Missing required section heading: '{section}'")

  refs = tuple(dict.fromkeys(AT_REF_PATTERN.findall(markdown_text)))
  if not refs:
    errors.append(
        "No on-demand @path/to/file.md references found; root context should "
        "delegate deep reference docs on demand to save startup tokens."
    )

  return RootContextValidationResult(
      is_valid=len(errors) == 0,
      line_count=line_count,
      missing_sections=tuple(missing),
      on_demand_refs=refs,
      errors=tuple(errors),
  )


def resolve_project_memory_dir(
    current_working_dir: str,
    git_repo_root: str | None = None,
    harness: str = "claude",
    home_dir: str = "/home/dev",
) -> str:
  """Resolves the shared cross-session auto-memory directory (REQ-0202).

  In Claude Code, each project gets ~/.claude/projects/<project>/memory/ where
  <project> is derived from the canonical git repository root so all git
  worktrees and subdirectories share one auto-memory directory. Outside a git
  repository, the current project root path is used instead.
  In Antigravity ('agy'), Knowledge Items are stored under
  ~/.gemini/antigravity/knowledge/<slug>.
  """
  anchor_raw = git_repo_root if git_repo_root else current_working_dir
  posix_anchor = PurePosixPath(anchor_raw)

  # Normalize path into deterministic project slug (e.g., /workspace/payments-api/worktrees/feat-a -> repo root)
  parts = [p for p in posix_anchor.parts if p not in ("/", "")]
  if not parts:
    project_slug = "root"
  else:
    project_slug = "-" + "-".join(parts)

  home_posix = PurePosixPath(home_dir)
  if harness == "claude":
    return str(home_posix / ".claude" / "projects" / project_slug / "memory")
  if harness == "agy":
    repo_name = parts[-1] if parts else "default"
    return str(home_posix / ".gemini" / "antigravity" / "knowledge" / repo_name)
  raise ValueError(f"Unsupported harness '{harness}'; expected 'claude' or 'agy'")


def format_memory_entry(
    statement: str,
    source_type: str,
    commit_sha: str | None = None,
    date_str: str | None = None,
    session_id: str | None = None,
) -> str:
  """Formats a durable memory bullet with epistemic provenance tags (REQ-0204).

  Reserve #direct strictly for statements explicitly given by the user
  (source_type == 'user_explicit'). Observations inferred by the agent from
  code, tests, or environment MUST NOT carry #direct.
  """
  clean = statement.strip().lstrip("-").strip()
  if not clean:
    raise ValueError("Memory statement cannot be empty")

  tags: list[str] = []
  if source_type == "user_explicit":
    tags.append("#direct")
  elif source_type not in ("agent_discovered", "codebase_observed", "test_verified"):
    raise ValueError(
        f"Invalid source_type '{source_type}'; expected 'user_explicit' or "
        "'agent_discovered'/'codebase_observed'/'test_verified'"
    )

  if commit_sha is not None:
    tags.append(f"#commit:{commit_sha}")
  if date_str is not None:
    tags.append(f"#time:{date_str}")
  if session_id is not None:
    tags.append(f"#session:{session_id}")

  suffix = (" " + " ".join(tags)) if tags else ""
  return f"- {clean}{suffix}"


@dataclass(frozen=True)
class CompiledAutoMemory:
  """Result of compiling MEMORY.md / KNOWLEDGE.md and overflow topic files (REQ-0203)."""

  index_markdown: str
  topic_files: dict[str, str]
  index_line_count: int
  index_byte_count: int


def compile_auto_memory(
    entries: list[dict[str, Any]],
    harness: str = "claude",
    max_lines: int = 200,
    max_bytes: int = 25_000,
) -> CompiledAutoMemory:
  """Compiles cross-session memory respecting the 200-line / 25 KB startup cap (REQ-0203)."""
  header_lines: list[str] = []
  if harness == "agy":
    header_lines.extend([
        "---",
        "description: Persistent cross-session Knowledge Item index and engineering conventions",
        "scope: workspace",
        "---",
        "",
        "# Antigravity Knowledge Base Index (KNOWLEDGE.md)",
        "",
    ])
  else:
    header_lines.extend([
        "# Project Auto-Memory Index (MEMORY.md)",
        "",
    ])

  core_bullets: list[str] = []
  topic_buckets: dict[str, list[str]] = {}

  for item in entries:
    formatted = format_memory_entry(
        statement=str(item["statement"]),
        source_type=str(item.get("source_type", "agent_discovered")),
        commit_sha=item.get("commit_sha"),
        date_str=item.get("date_str"),
        session_id=item.get("session_id"),
    )
    topic = item.get("topic")
    is_core = bool(item.get("core", topic is None))
    if is_core and not topic:
      core_bullets.append(formatted)
    else:
      topic_slug = str(topic or "general").lower().replace(" ", "-")
      topic_buckets.setdefault(topic_slug, []).append(formatted)

  topic_files: dict[str, str] = {}
  topic_links: list[str] = []
  for slug, bullets in sorted(topic_buckets.items()):
    rel_path = f"topics/{slug}.md"
    topic_files[rel_path] = (
        f"---\ndescription: Detailed memory notes for {slug}\n---\n\n"
        + "\n".join(bullets)
        + "\n"
    )
    topic_links.append(
        f"- [{slug}]({rel_path}) — {len(bullets)} entries (loaded on demand)"
    )

  body_lines = list(header_lines)
  body_lines.append("## Core Workspace Rules & Preferences")
  # Reserve room for topic links section (including potential overflow link) at the bottom of MEMORY.md
  reserved_footer_lines = len(topic_links) + 4
  for bullet in core_bullets:
    if len(body_lines) + reserved_footer_lines >= max_lines:
      topic_buckets.setdefault("overflow", []).append(bullet)
      continue
    candidate = "\n".join(body_lines + [bullet])
    if len(candidate.encode("utf-8")) + 512 > max_bytes:
      topic_buckets.setdefault("overflow", []).append(bullet)
      continue
    body_lines.append(bullet)

  if "overflow" in topic_buckets and "topics/overflow.md" not in topic_files:
    overflow_bullets = topic_buckets["overflow"]
    topic_files["topics/overflow.md"] = (
        "---\ndescription: Overflow memory notes\n---\n\n"
        + "\n".join(overflow_bullets)
        + "\n"
    )
    topic_links.append(
        f"- [overflow](topics/overflow.md) — {len(overflow_bullets)} entries (loaded on demand)"
    )

  if topic_links:
    body_lines.append("")
    body_lines.append("## On-Demand Topic Files")
    body_lines.extend(topic_links)

  index_md = "\n".join(body_lines) + "\n"
  final_lines = len(index_md.splitlines())
  final_bytes = len(index_md.encode("utf-8"))
  return CompiledAutoMemory(
      index_markdown=index_md,
      topic_files=topic_files,
      index_line_count=final_lines,
      index_byte_count=final_bytes,
  )


@dataclass(frozen=True)
class ContextAuditReport:
  """Simulated output of /context command and progressive loading audit (REQ-0205)."""

  total_used_tokens: int
  window_limit_tokens: int
  free_tokens: int
  utilization_ratio: float
  status: str
  progressive_savings_tokens: int
  category_breakdown: dict[str, int]


def simulate_context_command(
    category_tokens: dict[str, int],
    deferred_reference_tokens: int = 0,
    window_limit_tokens: int = 200_000,
) -> ContextAuditReport:
  """Simulates /context inspection and checks the 60% degradation threshold (REQ-0205)."""
  if window_limit_tokens <= 0:
    raise ValueError("window_limit_tokens must be positive")

  used = sum(max(0, int(v)) for v in category_tokens.values())
  free = max(0, window_limit_tokens - used)
  ratio = round(used / window_limit_tokens, 4)

  if ratio > 0.60:
    status = "CONTEXT_POLLUTION_WARNING"
  elif ratio >= 0.40:
    status = "OPTIMAL_SWEET_SPOT"
  else:
    status = "HEALTHY_HEADROOM"

  return ContextAuditReport(
      total_used_tokens=used,
      window_limit_tokens=window_limit_tokens,
      free_tokens=free,
      utilization_ratio=ratio,
      status=status,
      progressive_savings_tokens=max(0, deferred_reference_tokens),
      category_breakdown=dict(category_tokens),
  )
