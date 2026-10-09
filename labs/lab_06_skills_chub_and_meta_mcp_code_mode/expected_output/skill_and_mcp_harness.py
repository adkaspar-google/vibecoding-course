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

"""Lab 06 Reference Solution: Progressive Skills, Chub Docs & Meta-MCP Code Mode.

Implements:
- REQ-0601: agentskills.io 3-Level Progressive Disclosure Validator.
- REQ-0602: andrewyng/context-hub (@aisuite/chub) Curated Doc Store & Self-Annotating Loop.
- REQ-0603: Ergonomic Tool Schema Auditor (Stanford CS146S Lecture 4).
- REQ-0604: Meta-MCP 'Code Mode' (search + execute meta-tools) with >=90% Token Savings.
- REQ-0605: SkillsBench (arXiv:2602.12670) Paired Ablation Evaluator.
- REQ-0606: Skill Catalog Overload Detector (2-3 sweet spot vs. >10 overload).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from typing import Any


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RAW_CRUD_PREFIXES = ("get_", "post_", "put_", "delete_", "patch_", "list_all_raw_")


@dataclass(frozen=True)
class SkillPackageValidation:
  """Validation report for a 3-level progressive-disclosure skill package (REQ-0601)."""

  is_valid: bool
  level1_metadata_ok: bool
  level2_body_ok: bool
  level3_companions_ok: bool
  errors: tuple[str, ...]


def validate_progressive_skill_package(
    name: str,
    description: str,
    skill_md_lines: int,
    companion_files: list[str],
    max_skill_md_lines: int = 500,
) -> SkillPackageValidation:
  """Validates a skill package against agentskills.io 3-level progressive disclosure rules (REQ-0601)."""
  errors: list[str] = []

  l1_ok = True
  if not SKILL_NAME_RE.match(name):
    l1_ok = False
    errors.append(f"Invalid skill name '{name}': must be hyphen-case ^[a-z0-9]+(-[a-z0-9]+)*$")
  desc_lower = description.lower()
  if "use when" not in desc_lower or ("don't use" not in desc_lower and "do not use" not in desc_lower):
    l1_ok = False
    errors.append("Level 1 description must include both 'Use when...' and 'Don't use...' trigger boundaries")

  l2_ok = 10 <= skill_md_lines <= max_skill_md_lines
  if not l2_ok:
    errors.append(
        f"Level 2 SKILL.md has {skill_md_lines} lines (must be between 10 and {max_skill_md_lines} lines)"
    )

  l3_ok = bool(companion_files) and all(
      f.startswith(("references/", "scripts/", "assets/")) or f.endswith(".md")
      for f in companion_files
  )
  if not l3_ok:
    errors.append("Level 3 must include at least one companion reference or script file")

  return SkillPackageValidation(
      is_valid=not errors,
      level1_metadata_ok=l1_ok,
      level2_body_ok=l2_ok,
      level3_companions_ok=l3_ok,
      errors=tuple(errors),
  )


@dataclass(frozen=True)
class ChubDocEntry:
  """Curated versioned API documentation entry in Context Hub (REQ-0602)."""

  doc_id: str
  lang: str
  version: str
  content_md: str


@dataclass
class ChubRegistry:
  """Local implementation of andrewyng/context-hub (@aisuite/chub) with self-improving annotations (REQ-0602)."""

  docs: dict[tuple[str, str], ChubDocEntry] = field(default_factory=dict)
  annotations: dict[str, list[str]] = field(default_factory=dict)
  feedback_counts: dict[str, dict[str, int]] = field(default_factory=dict)

  def register_doc(self, entry: ChubDocEntry) -> None:
    self.docs[(entry.doc_id, entry.lang)] = entry

  def search(self, query: str) -> list[str]:
    q = query.strip().lower()
    matched = [
        doc_id
        for (doc_id, _), entry in sorted(self.docs.items())
        if q in doc_id.lower() or q in entry.content_md.lower()
    ]
    return list(dict.fromkeys(matched))

  def annotate(self, doc_id: str, note: str) -> None:
    cleaned = note.strip()
    if not cleaned:
      raise ValueError("Annotation note must be non-empty")
    self.annotations.setdefault(doc_id, []).append(cleaned)

  def feedback(self, doc_id: str, rating: str) -> dict[str, int]:
    norm = rating.strip().lower()
    if norm not in ("up", "down"):
      raise ValueError("rating must be 'up' or 'down'")
    counts = self.feedback_counts.setdefault(doc_id, {"up": 0, "down": 0})
    counts[norm] += 1
    return dict(counts)

  def get(self, doc_id: str, lang: str = "py", with_annotations: bool = False) -> str:
    key = (doc_id, lang)
    if key not in self.docs:
      raise KeyError(f"Doc '{doc_id}' (lang='{lang}') not found in ChubRegistry")
    entry = self.docs[key]
    base = f"# {entry.doc_id} ({entry.lang}, v{entry.version})\n\n{entry.content_md.strip()}"
    if not with_annotations or not self.annotations.get(doc_id):
      return base
    notes = "\n".join(f"- {n}" for n in self.annotations[doc_id])
    return (
        f"{base}\n\n"
        f"## [UNTRUSTED_LOCAL_ANNOTATION — Verify Before Executing]\n"
        f"{notes}"
    )


@dataclass(frozen=True)
class ToolErgonomicsAudit:
  """Ergonomics audit of an agent tool specification (CS146S Lecture 4, REQ-0603)."""

  is_ergonomic: bool
  is_outcome_oriented: bool
  has_strict_typed_schema: bool
  has_actionable_errors: bool
  issues: tuple[str, ...]


def audit_tool_ergonomics(tool_spec: dict[str, Any]) -> ToolErgonomicsAudit:
  """Audits a tool specification against the 4 Rules of Ergonomic Agent Tools (REQ-0603)."""
  name = str(tool_spec.get("name", "")).strip()
  params = tool_spec.get("parameters", {})
  error_contract = str(tool_spec.get("error_contract", "")).strip()

  issues: list[str] = []
  is_outcome = bool(name) and not name.lower().startswith(RAW_CRUD_PREFIXES)
  if not is_outcome:
    issues.append(
        f"Tool '{name}' uses a granular CRUD verb prefix; design tools around user outcomes instead"
    )

  props = params.get("properties") if isinstance(params, dict) else None
  has_untyped_kwargs = (
      not isinstance(props, dict)
      or not props
      or "kwargs" in props
      or "args" in props
      or params.get("additionalProperties", True) is not False
  )
  has_strict_schema = not has_untyped_kwargs
  if not has_strict_schema:
    issues.append(
        f"Tool '{name}' lacks a strict typed schema (forbid untyped kwargs and set additionalProperties=False)"
    )

  has_errors = bool(error_contract) and "remediation" in error_contract.lower()
  if not has_errors:
    issues.append(f"Tool '{name}' must document typed error exceptions with remediation guidance")

  return ToolErgonomicsAudit(
      is_ergonomic=not issues,
      is_outcome_oriented=is_outcome,
      has_strict_typed_schema=has_strict_schema,
      has_actionable_errors=has_errors,
      issues=tuple(issues),
  )


META_MCP_CODE_MODE_SCHEMAS: tuple[dict[str, Any], ...] = (
    {
        "name": "mcp__meta__search",
        "description": "Search the on-demand MCP tool registry by capability keyword and return matching typed schemas.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mcp__meta__execute",
        "description": "Execute a chained Python/TypeScript tool invocation plan inside the governed sandbox.",
        "parameters": {
            "type": "object",
            "properties": {"operations": {"type": "array", "items": {"type": "object"}}},
            "required": ["operations"],
            "additionalProperties": False,
        },
    },
)


@dataclass(frozen=True)
class CodeModeTokenComparison:
  """Token comparison between raw N-tool MCP injection and Meta-MCP Code Mode (REQ-0604)."""

  raw_tool_count: int
  raw_schema_tokens: int
  code_mode_schema_tokens: int
  token_reduction_ratio: float


class MetaMcpCodeModeHarness:
  """Stanford CS146S Lecture 4 Meta-MCP 'Code Mode' (search + execute) harness (REQ-0604)."""

  def __init__(self, tool_catalog: list[dict[str, Any]]) -> None:
    self._catalog = {str(t["name"]): t for t in tool_catalog}

  def standing_wire_schemas(self) -> list[dict[str, Any]]:
    """Returns only the 2 compact meta-tools ('search' and 'execute') for the standing wire payload."""
    return list(META_MCP_CODE_MODE_SCHEMAS)

  def search(self, query: str) -> list[dict[str, Any]]:
    """On-demand discovery of relevant tool schemas without polluting every turn."""
    q = query.strip().lower()
    return [
        spec
        for name, spec in sorted(self._catalog.items())
        if q in name.lower() or q in str(spec.get("description", "")).lower()
    ]

  def execute(self, operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Executes a chained sequence of tool operations in a single sandbox round-trip."""
    results: list[dict[str, Any]] = []
    for op in operations:
      tool_name = str(op.get("tool", ""))
      if tool_name not in self._catalog:
        raise KeyError(f"Unknown tool '{tool_name}' in Meta-MCP execute chain")
      results.append({
          "tool": tool_name,
          "status": "ok",
          "args": op.get("args", {}),
      })
    return results


def measure_code_mode_token_savings(raw_tool_schemas: list[dict[str, Any]]) -> CodeModeTokenComparison:
  """Measures context token reduction of Meta-MCP Code Mode vs. raw schema injection (REQ-0604)."""
  raw_chars = len(json.dumps(raw_tool_schemas, sort_keys=True))
  meta_chars = len(json.dumps(list(META_MCP_CODE_MODE_SCHEMAS), sort_keys=True))
  raw_tokens = max(1, (raw_chars + 3) // 4)
  meta_tokens = max(1, (meta_chars + 3) // 4)
  reduction = round(max(0.0, (raw_tokens - meta_tokens) / float(raw_tokens)), 4)
  return CodeModeTokenComparison(
      raw_tool_count=len(raw_tool_schemas),
      raw_schema_tokens=raw_tokens,
      code_mode_schema_tokens=meta_tokens,
      token_reduction_ratio=reduction,
  )


@dataclass(frozen=True)
class SkillsBenchReport:
  """Paired with_skill vs. without_skill evaluation report (arXiv:2602.12670, REQ-0605)."""

  with_skill_pass_rate: float
  without_skill_pass_rate: float
  pass_rate_delta_pp: float
  is_self_generated: bool
  verdict: str  # "CURATED_GAIN" | "SELF_GENERATED_REGRESSION" | "NEUTRAL_OR_NEGATIVE"


def evaluate_skillsbench_ablation(
    with_skill_scores: list[bool],
    without_skill_scores: list[bool],
    is_self_generated: bool = False,
) -> SkillsBenchReport:
  """Computes paired pass-rate lift in percentage points and flags self-generated regressions (REQ-0605)."""
  if not with_skill_scores or len(with_skill_scores) != len(without_skill_scores):
    raise ValueError("with_skill_scores and without_skill_scores must be non-empty and equal length")

  with_rate = sum(1 for x in with_skill_scores if x) / float(len(with_skill_scores))
  without_rate = sum(1 for x in without_skill_scores if x) / float(len(without_skill_scores))
  delta_pp = round((with_rate - without_rate) * 100.0, 2)

  if is_self_generated and delta_pp <= 0.0:
    verdict = "SELF_GENERATED_REGRESSION"
  elif delta_pp > 0.0:
    verdict = "CURATED_GAIN"
  else:
    verdict = "NEUTRAL_OR_NEGATIVE"

  return SkillsBenchReport(
      with_skill_pass_rate=round(with_rate, 4),
      without_skill_pass_rate=round(without_rate, 4),
      pass_rate_delta_pp=delta_pp,
      is_self_generated=is_self_generated,
      verdict=verdict,
  )


@dataclass(frozen=True)
class SkillOverloadAudit:
  """Audit of active skill count against the 2-3 sweet spot and >10 overload cliff (REQ-0606)."""

  active_count: int
  in_sweet_spot: bool
  is_severely_overloaded: bool
  recommendation: str


def audit_skill_catalog_overload(
    active_skill_names: list[str],
    sweet_spot_max: int = 3,
    overload_ceiling: int = 10,
) -> SkillOverloadAudit:
  """Audits active skill count against SkillsBench Table 8 thresholds (REQ-0606)."""
  count = len(active_skill_names)
  in_sweet = 1 <= count <= sweet_spot_max
  severe = count > overload_ceiling
  if severe:
    rec = f"Severe skill overload ({count} > {overload_ceiling}); consolidate into 2-3 outcome skills with Level 3 references."
  elif not in_sweet:
    rec = f"Skill count ({count}) is outside the 1-{sweet_spot_max} sweet spot; prune redundant skills."
  else:
    rec = "Active skill catalog is within the optimal 2-3 focused skill sweet spot."
  return SkillOverloadAudit(
      active_count=count,
      in_sweet_spot=in_sweet,
      is_severely_overloaded=severe,
      recommendation=rec,
  )
