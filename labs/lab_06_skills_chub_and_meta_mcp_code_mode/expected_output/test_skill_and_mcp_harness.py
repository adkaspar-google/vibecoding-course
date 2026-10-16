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

"""Unit tests for Lab 06 skill_and_mcp_harness.py (REQ-0601 through REQ-0606)."""

from __future__ import annotations

import unittest

import skill_and_mcp_harness as smh


class TestSkillAndMcpHarness(unittest.TestCase):
  """Requirement-traceable unit tests for Lab 06 (REQ-0601..REQ-0606)."""

  def test_req0601_progressive_disclosure_skill_validator(self) -> None:
    """Verifies REQ-0601: agentskills.io 3-Level Progressive Disclosure Validator."""
    res = smh.validate_progressive_skill_package(
        name="context-hub-docs",
        description="Fetches curated API docs. Use when calling external SDKs. Don't use for local math.",
        skill_md_lines=110,
        companion_files=["references/api_quirks.md", "scripts/chub_lookup.py"],
    )
    self.assertTrue(res.is_valid)
    self.assertTrue(res.level1_metadata_ok)
    self.assertTrue(res.level2_body_ok)
    self.assertTrue(res.level3_companions_ok)

  def test_req0602_context_hub_chub_doc_store_and_annotations(self) -> None:
    """Verifies REQ-0602: andrewyng/context-hub (@aisuite/chub) Curated Doc Store and Self-Annotating Loop."""
    reg = smh.ChubRegistry()
    reg.register_doc(
        smh.ChubDocEntry(
            doc_id="stripe/webhooks",
            lang="py",
            version="2026.1",
            content_md="Use `Webhook.construct_event(payload, sig_header, secret)`.",
        )
    )
    reg.annotate("stripe/webhooks", "Pass raw request.body bytes, never parsed JSON dict.")
    doc = reg.get("stripe/webhooks", lang="py", with_annotations=True)
    self.assertIn("UNTRUSTED_LOCAL_ANNOTATION", doc)
    self.assertIn("raw request.body bytes", doc)

  def test_req0603_ergonomic_tool_schema_auditor(self) -> None:
    """Verifies REQ-0603: Ergonomic Tool Schema Auditor enforces outcome naming, strict types, and error remediation."""
    good_tool = {
        "name": "settle_taskflow_invoice",
        "parameters": {
            "type": "object",
            "properties": {"account_id": {"type": "string"}, "amount_cents": {"type": "integer"}},
            "required": ["account_id", "amount_cents"],
            "additionalProperties": False,
        },
        "error_contract": "Raises InvoiceSettlementError with remediation steps on insufficient funds.",
    }
    audit = smh.audit_tool_ergonomics(good_tool)
    self.assertTrue(audit.is_ergonomic)

  def test_req0604_meta_mcp_code_mode_token_savings(self) -> None:
    """Verifies REQ-0604: Meta-MCP 'Code Mode' (search + execute meta-tools) achieves >=90% token savings."""
    raw_catalog = [
        {
            "name": f"mcp__taskflow__op_{i}",
            "description": "Enterprise SaaS endpoint schema definition " * 8,
            "parameters": {
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "additionalProperties": False,
            },
        }
        for i in range(80)
    ]
    savings = smh.measure_code_mode_token_savings(raw_catalog)
    self.assertGreaterEqual(savings.token_reduction_ratio, 0.90)

  def test_req0605_skillsbench_paired_ablation_evaluator(self) -> None:
    """Verifies REQ-0605: SkillsBench Paired Ablation Evaluator detects curated gains vs. self-generated regressions."""
    curated = smh.evaluate_skillsbench_ablation(
        with_skill_scores=[True, True, True, False],
        without_skill_scores=[False, True, False, False],
        is_self_generated=False,
    )
    self.assertEqual(curated.verdict, "CURATED_GAIN")
    self.assertEqual(curated.pass_rate_delta_pp, 50.0)

  def test_req0606_skill_catalog_overload_detector(self) -> None:
    """Verifies REQ-0606: Skill Catalog Overload Detector enforces 2-3 sweet spot vs. >10 overload cliff."""
    sweet = smh.audit_skill_catalog_overload(["context-hub-docs", "reppit-workflow"])
    overloaded = smh.audit_skill_catalog_overload([f"skill-{i}" for i in range(12)])
    self.assertTrue(sweet.in_sweet_spot)
    self.assertTrue(overloaded.is_severely_overloaded)


if __name__ == "__main__":
  unittest.main()
