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

"""Skill Evaluation (eval-viewer / grading.json / benchmark.json), SDT Trigger Calibration & Overload Pruner.

Implements REQ-0401 through REQ-0405 for Lab 04:
- Anthropic skill-creator grading.json & benchmark.json paired evaluation
- Static eval-viewer HTML report generator (Outputs + Benchmark tabs)
- Signal Detection Theory (d', criterion bias c, utility U) with Hautus +0.5 smoothing
- SkillsBench (arXiv:2602.12670 Table 8) skill overload consolidator using Reference-First rule
"""

from __future__ import annotations

from dataclasses import dataclass
import html
import math
from statistics import mean, pstdev
from typing import Any


def grade_trajectory_expectations(
    output_text: str,
    expectations: list[dict[str, str]],
) -> dict[str, Any]:
  """Grades an agent output against deterministic expectations into grading.json schema (REQ-0401).

  Note: Uses exact field names 'text', 'passed', and 'evidence' required by
  Anthropic's skill-creator eval-viewer (never 'name'/'met').
  """
  graded_list: list[dict[str, Any]] = []
  passed_count = 0

  for exp in expectations:
    exp_text = str(exp["text"])
    required_token = str(exp["required_substring"])
    passed = required_token in output_text
    if passed:
      passed_count += 1
      evidence = f"Found required substring '{required_token}' in output."
    else:
      evidence = f"Missing required substring '{required_token}' in output."

    graded_list.append({
        "text": exp_text,
        "passed": passed,
        "evidence": evidence,
    })

  total = len(graded_list)
  pass_rate = round(passed_count / total, 4) if total > 0 else 0.0
  return {
      "expectations": graded_list,
      "passed_count": passed_count,
      "total_count": total,
      "pass_rate": pass_rate,
  }


def aggregate_paired_benchmark(
    with_skill_runs: list[dict[str, float]],
    without_skill_runs: list[dict[str, float]],
) -> dict[str, Any]:
  """Aggregates paired with_skill vs without_skill runs into benchmark.json schema (REQ-0402)."""
  if not with_skill_runs or not without_skill_runs:
    raise ValueError("Both with_skill_runs and without_skill_runs must be non-empty")

  ws_rates = [float(r["pass_rate"]) for r in with_skill_runs]
  wo_rates = [float(r["pass_rate"]) for r in without_skill_runs]
  ws_tokens = [float(r.get("tokens", 0.0)) for r in with_skill_runs]
  wo_tokens = [float(r.get("tokens", 0.0)) for r in without_skill_runs]

  ws_mean = round(mean(ws_rates), 4)
  wo_mean = round(mean(wo_rates), 4)
  ws_std = round(pstdev(ws_rates), 4) if len(ws_rates) > 1 else 0.0
  wo_std = round(pstdev(wo_rates), 4) if len(wo_rates) > 1 else 0.0

  net_delta = round(ws_mean - wo_mean, 4)
  token_delta = round(mean(ws_tokens) - mean(wo_tokens), 1)
  verdict = "POSITIVE_LIFT" if net_delta > 0.0 else "NOISE_OR_REGRESSION"

  return {
      "with_skill": {
          "mean_pass_rate": ws_mean,
          "stddev_pass_rate": ws_std,
          "mean_tokens": round(mean(ws_tokens), 1),
      },
      "without_skill": {
          "mean_pass_rate": wo_mean,
          "stddev_pass_rate": wo_std,
          "mean_tokens": round(mean(wo_tokens), 1),
      },
      "delta": {
          "net_pass_rate_delta": net_delta,
          "mean_token_delta": token_delta,
      },
      "verdict": verdict,
  }


def generate_eval_viewer_html(
    benchmark_summary: dict[str, Any],
    graded_cases: list[dict[str, Any]],
) -> str:
  """Generates a standalone static HTML report mirroring eval-viewer/generate_review.py (REQ-0403)."""
  ws_rate = benchmark_summary["with_skill"]["mean_pass_rate"]
  wo_rate = benchmark_summary["without_skill"]["mean_pass_rate"]
  delta = benchmark_summary["delta"]["net_pass_rate_delta"]
  verdict = html.escape(str(benchmark_summary["verdict"]))

  case_rows: list[str] = []
  for idx, case in enumerate(graded_cases, start=1):
    prompt = html.escape(str(case.get("prompt", f"Eval Case #{idx}")))
    exp_items: list[str] = []
    for exp in case.get("grading", {}).get("expectations", []):
      badge = "PASS" if exp.get("passed") else "FAIL"
      text = html.escape(str(exp.get("text", "")))
      ev = html.escape(str(exp.get("evidence", "")))
      exp_items.append(f"<li><strong>[{badge}]</strong> {text} — <em>{ev}</em></li>")
    case_rows.append(
        f"<div class='eval-case'><h3>Case {idx}: {prompt}</h3>"
        f"<ul>{''.join(exp_items)}</ul></div>"
    )

  return (
      "<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'>"
      "<title>Skill Eval-Viewer Report</title></head>\n<body>\n"
      "<h1>Skill Evaluation Viewer</h1>\n"
      "<section id='tab-outputs'><h2>Outputs Tab (Qualitative Trajectory Review)</h2>\n"
      + "\n".join(case_rows)
      + "\n</section>\n"
      "<section id='tab-benchmark'><h2>Benchmark Tab (With-Skill vs Without-Skill)</h2>\n"
      f"<p>With-Skill Mean Pass Rate: {ws_rate:.2%}</p>\n"
      f"<p>Without-Skill Mean Pass Rate: {wo_rate:.2%}</p>\n"
      f"<p>Net Lift Delta: {delta:+.2%} ({verdict})</p>\n"
      "</section>\n</body>\n</html>\n"
  )


def _inverse_normal_cdf(p: float) -> float:
  """Rational approximation (Peter Acklam) to standard normal inverse CDF Phi^-1(p)."""
  if p <= 0.0 or p >= 1.0:
    raise ValueError("Probability p must be strictly in (0, 1)")

  a = (
      -3.969683028665376e01,
      2.209460984245205e02,
      -2.759285104469687e02,
      1.383577518672690e02,
      -3.066479806614716e01,
      2.506628277459239e00,
  )
  b = (
      -5.447609879822406e01,
      1.615858368580409e02,
      -1.556989798598866e02,
      6.680131188771972e01,
      -1.328068155288572e01,
  )
  c = (
      -7.784894002430293e-03,
      -3.223964580411365e-01,
      -2.400758277161838e00,
      -2.549732539343734e00,
      4.374664141464968e00,
      2.938163982698783e00,
  )
  d = (
      7.784695709041462e-03,
      3.224671290700398e-01,
      2.445134137142996e00,
      3.754408661907416e00,
  )
  p_low = 0.02425
  p_high = 1.0 - p_low

  if p < p_low:
    q = math.sqrt(-2.0 * math.log(p))
    return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
        (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
    )
  if p <= p_high:
    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
        * q
        / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
    )
  q = math.sqrt(-2.0 * math.log(1.0 - p))
  return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
      (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
  )


@dataclass(frozen=True)
class SDTTriggerMetrics:
  """Signal Detection Theory metrics for skill description routing (REQ-0404)."""

  hr_adj: float
  fa_adj: float
  d_prime: float
  criterion_c: float
  utility_u: float
  bias_regime: str


def compute_sdt_trigger_metrics(
    hits: int,
    misses: int,
    false_alarms: int,
    correct_rejections: int,
    c_target: float = 0.0,
) -> SDTTriggerMetrics:
  """Computes Hautus (+0.5) smoothed d', criterion c, and utility U (REQ-0404)."""
  hr_adj = (hits + 0.5) / (hits + misses + 1.0)
  fa_adj = (false_alarms + 0.5) / (false_alarms + correct_rejections + 1.0)

  z_hr = _inverse_normal_cdf(hr_adj)
  z_fa = _inverse_normal_cdf(fa_adj)

  d_prime = round(z_hr - z_fa, 4)
  criterion_c = round(-0.5 * (z_hr + z_fa), 4)
  utility_u = round(2.0 * d_prime - 0.5 * abs(criterion_c - c_target), 4)

  if criterion_c > 0.25:
    bias_regime = "CONSERVATIVE_UNDER_TRIGGERING"
  elif criterion_c < -0.25:
    bias_regime = "LIBERAL_FALSE_ALARM_POLLUTION"
  else:
    bias_regime = "BALANCED_CALIBRATED"

  return SDTTriggerMetrics(
      hr_adj=round(hr_adj, 4),
      fa_adj=round(fa_adj, 4),
      d_prime=d_prime,
      criterion_c=criterion_c,
      utility_u=utility_u,
      bias_regime=bias_regime,
  )


def consolidate_overloaded_skills(
    skills: list[dict[str, Any]],
    max_active_skills: int = 3,
    min_standalone_lines: int = 50,
) -> dict[str, Any]:
  """Consolidates overloaded micro-skills into 2-3 parent outcome skills with references/ (REQ-0405).

  Implements SkillsBench Table 8 defense (2-3 skills = +19.0 pp vs >=4 skills = +10.1 pp)
  and the Reference-First rule (merging sibling sub-workflows into references/*.md).
  """
  by_domain: dict[str, list[dict[str, Any]]] = {}
  for s in skills:
    domain = str(s.get("domain", "general"))
    by_domain.setdefault(domain, []).append(s)

  consolidated: list[dict[str, Any]] = []
  demoted_to_references: list[str] = []

  for domain, group in sorted(by_domain.items()):
    if len(group) == 1 and int(group[0].get("lines", 0)) >= min_standalone_lines:
      consolidated.append({
          "name": str(group[0]["name"]),
          "domain": domain,
          "references": [],
          "total_lines": int(group[0].get("lines", 0)),
      })
    else:
      # Merge domain siblings into one canonical parent skill + references/*.md
      refs: list[str] = []
      total_lines = 0
      for item in group:
        sub_name = str(item["name"])
        refs.append(f"references/{sub_name}.md")
        demoted_to_references.append(sub_name)
        total_lines += int(item.get("lines", 30))
      consolidated.append({
          "name": f"{domain}-workflow",
          "domain": domain,
          "references": refs,
          "total_lines": max(min_standalone_lines, total_lines),
      })

  return {
      "original_skill_count": len(skills),
      "consolidated_skill_count": len(consolidated),
      "is_within_sweet_spot": len(consolidated) <= max_active_skills,
      "consolidated_skills": consolidated,
      "demoted_to_references": demoted_to_references,
  }
