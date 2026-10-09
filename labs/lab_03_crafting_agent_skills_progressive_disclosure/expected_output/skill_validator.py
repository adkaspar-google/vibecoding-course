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

"""agentskills.io Validator, Progressive Disclosure Budgeter & Self-Generation Trap Auditor.

Implements REQ-0301 through REQ-0305 for Lab 03:
- agentskills.io specification frontmatter & cardinality validator
- 3-level progressive disclosure token accounting (SKILL.md + docs.md, slides-deck.md, apply_template.md)
- SkillsBench (arXiv:2602.12670) self-generated skill trap detector
- Deterministic brand template application
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any


SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
GENERIC_TRAINING_PHRASES = (
    "write clean, modular, well-documented code",
    "test your edge cases carefully",
    "follow best practices for software engineering",
    "help with everything",
)
SPECULATIVE_MULTIPLIER_PATTERN = re.compile(
    r"multiply all input dimensions by\s+`?1000(?:\.0)?`?",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SkillValidationReport:
  """Validation report for an agentskills.io skill directory (REQ-0301, REQ-0302)."""

  is_valid: bool
  name: str
  description: str
  line_count: int
  companion_files: tuple[str, ...]
  errors: tuple[str, ...]


def _parse_frontmatter(markdown_text: str) -> tuple[dict[str, str], str]:
  """Extracts simple YAML frontmatter key-values and body from SKILL.md."""
  if not markdown_text.startswith("---\n"):
    return {}, markdown_text
  end_idx = markdown_text.find("\n---\n", 4)
  if end_idx == -1:
    return {}, markdown_text
  fm_raw = markdown_text[4:end_idx]
  body = markdown_text[end_idx + 5 :]

  meta: dict[str, str] = {}
  current_key: str | None = None
  folded_lines: list[str] = []

  for line in fm_raw.splitlines():
    if line.startswith("  ") and current_key is not None:
      folded_lines.append(line.strip())
      meta[current_key] = " ".join(folded_lines).strip()
      continue
    if ":" in line:
      key, val = line.split(":", 1)
      current_key = key.strip()
      val_clean = val.strip()
      if val_clean in (">-", ">", "|"):
        folded_lines = []
        meta[current_key] = ""
      else:
        folded_lines = [val_clean.strip("\"'")]
        meta[current_key] = folded_lines[0]
  return meta, body


def validate_skill_package(
    skill_dir: str | Path,
    min_lines: int = 50,
    max_lines: int = 500,
) -> SkillValidationReport:
  """Validates a skill directory against agentskills.io & cardinality rules (REQ-0302)."""
  path = Path(skill_dir)
  errors: list[str] = []
  skill_md_path = path / "SKILL.md"
  if not skill_md_path.is_file():
    return SkillValidationReport(
        is_valid=False,
        name="",
        description="",
        line_count=0,
        companion_files=(),
        errors=("Missing SKILL.md in skill directory",),
    )

  text = skill_md_path.read_text(encoding="utf-8")
  lines = text.splitlines()
  line_count = len(lines)
  meta, _ = _parse_frontmatter(text)

  name = meta.get("name", "")
  description = meta.get("description", "")

  if not name:
    errors.append("Missing 'name' in SKILL.md YAML frontmatter")
  else:
    if len(name) > 64 or not SKILL_NAME_PATTERN.match(name):
      errors.append(
          f"Invalid skill name '{name}': must be 1-64 lowercase alphanumeric "
          "chars separated by single hyphens (^[a-z0-9]+(-[a-z0-9]+)*$)"
      )
    normalized_dir = path.name.replace("_", "-")
    if name != normalized_dir:
      errors.append(
          f"Skill name '{name}' does not match directory '{path.name}'"
      )

  if not description:
    errors.append("Missing 'description' in SKILL.md YAML frontmatter")
  else:
    if len(description) > 1024:
      errors.append(
          f"Description length ({len(description)} chars) exceeds 1024-char limit"
      )
    if "use when" not in description.lower():
      errors.append("Description must include positive trigger guidance ('Use when...')")
    if "don't use" not in description.lower() and "do not use" not in description.lower():
      errors.append("Description must include negative trigger boundary ('Don't use for...')")

  if line_count < min_lines:
    errors.append(
        f"SKILL.md has {line_count} lines (< {min_lines} micro-skill floor)"
    )
  if line_count > max_lines:
    errors.append(
        f"SKILL.md has {line_count} lines (> {max_lines} ceiling); move details to references"
    )

  companions = tuple(
      sorted(
          p.name
          for p in path.iterdir()
          if p.is_file() and p.name != "SKILL.md"
      )
  )
  return SkillValidationReport(
      is_valid=len(errors) == 0,
      name=name,
      description=description,
      line_count=line_count,
      companion_files=companions,
      errors=tuple(errors),
  )


@dataclass(frozen=True)
class ProgressiveDisclosureBudget:
  """Token budget across the 3 progressive disclosure tiers (REQ-0303)."""

  level1_metadata_tokens: int
  level2_skill_body_tokens: int
  level3_selected_ref_tokens: int
  level3_total_available_tokens: int
  eager_all_files_tokens: int
  active_session_tokens: int
  startup_savings_ratio: float


def _estimate_tokens(text: str) -> int:
  """Approximates LLM token count (~4 chars per token, min 1 for non-empty)."""
  stripped = text.strip()
  if not stripped:
    return 0
  return max(1, (len(stripped) + 3) // 4)


def compute_progressive_disclosure_budget(
    skill_dir: str | Path,
    active_reference: str | None = None,
) -> ProgressiveDisclosureBudget:
  """Computes Level 1, Level 2, and Level 3 token usage for a skill (REQ-0303)."""
  path = Path(skill_dir)
  skill_md = (path / "SKILL.md").read_text(encoding="utf-8")
  meta, body = _parse_frontmatter(skill_md)

  l1_text = f"{meta.get('name', '')}: {meta.get('description', '')}"
  l1_tokens = _estimate_tokens(l1_text)
  l2_tokens = _estimate_tokens(body)

  ref_tokens_map: dict[str, int] = {}
  for item in sorted(path.iterdir()):
    if item.is_file() and item.name != "SKILL.md":
      ref_tokens_map[item.name] = _estimate_tokens(
          item.read_text(encoding="utf-8")
      )

  l3_total = sum(ref_tokens_map.values())
  l3_selected = ref_tokens_map.get(active_reference, 0) if active_reference else 0

  eager_total = l1_tokens + l2_tokens + l3_total
  active_total = l1_tokens + l2_tokens + l3_selected
  startup_savings = (
      round(1.0 - (l1_tokens / eager_total), 4) if eager_total > 0 else 0.0
  )

  return ProgressiveDisclosureBudget(
      level1_metadata_tokens=l1_tokens,
      level2_skill_body_tokens=l2_tokens,
      level3_selected_ref_tokens=l3_selected,
      level3_total_available_tokens=l3_total,
      eager_all_files_tokens=eager_total,
      active_session_tokens=active_total,
      startup_savings_ratio=startup_savings,
  )


@dataclass(frozen=True)
class SkillQualityDeltaAudit:
  """Audit result distinguishing human 'a conciencia' skills from self-generated noise (REQ-0304)."""

  classification: str
  has_generic_pretraining_filler: bool
  has_unverified_speculative_trap: bool
  grounded_failure_matches: int
  issues: tuple[str, ...]


def audit_skill_quality_delta(
    skill_markdown: str,
    observed_baseline_failures: list[str],
) -> SkillQualityDeltaAudit:
  """Detects SkillsBench self-generated skill anti-patterns (REQ-0304).

  Per SkillsBench (arXiv:2602.12670), self-generated skills reduce pass rate by
  -8.1 to -11.5 pp because they repeat generic pretraining advice or lock in
  unverified conversion traps (e.g., multiplying dimensions by 1000.0).
  """
  lower = skill_markdown.lower()
  issues: list[str] = []

  has_filler = False
  for phrase in GENERIC_TRAINING_PHRASES:
    if phrase in lower:
      has_filler = True
      issues.append(
          f"Contains generic training-data filler phrase: '{phrase}'"
      )

  has_trap = bool(SPECULATIVE_MULTIPLIER_PATTERN.search(skill_markdown))
  if has_trap:
    issues.append(
        "Contains unverified speculative 1000x unit conversion trap "
        "(SkillsBench 3d-scan-calc failure mode)"
    )

  grounded_matches = 0
  for failure_keyword in observed_baseline_failures:
    if failure_keyword.lower() in lower:
      grounded_matches += 1

  if grounded_matches == 0:
    issues.append(
        "Zero rules grounded in observed baseline failure trajectories "
        "(violates 'Experience Before Theory')"
    )

  if has_filler or has_trap or grounded_matches == 0:
    classification = "SELF_GENERATED_DEGRADATION_RISK"
  else:
    classification = "CURATED_HIGH_SIGNAL_DELTA"

  return SkillQualityDeltaAudit(
      classification=classification,
      has_generic_pretraining_filler=has_filler,
      has_unverified_speculative_trap=has_trap,
      grounded_failure_matches=grounded_matches,
      issues=tuple(issues),
  )


def apply_brand_profile(
    draft: dict[str, Any],
    artifact_type: str = "doc",
) -> dict[str, Any]:
  """Applies deterministic brand rules from docs.md / slides-deck.md / apply_template.md (REQ-0305)."""
  if artifact_type not in ("doc", "slides"):
    raise ValueError(f"Unsupported artifact_type '{artifact_type}'; expected 'doc' or 'slides'")

  margin_pt = 64 if artifact_type == "doc" else 36
  return {
      "title": str(draft.get("title", "Untitled")),
      "artifact_type": artifact_type,
      "reference_loaded": "docs.md" if artifact_type == "doc" else "slides-deck.md",
      "background_hex": "#FAF9F5",
      "body_text_hex": "#141413",
      "accent_hex": "#D97757",
      "heading_font": "Styrene A",
      "body_font": "Tiempos Text",
      "code_font": "JetBrains Mono",
      "margin_pt": margin_pt,
  }
