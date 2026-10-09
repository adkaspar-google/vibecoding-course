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

"""Immutable adversarial verifier for Lab 06 (REQ-0601 through REQ-0606)."""

from __future__ import annotations

import unittest

import skill_and_mcp_harness as smh


class TestLab06SkillAndMcpHarnessVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 06."""

  def test_req0601_progressive_disclosure_skill_validator(self) -> None:
    """REQ-0601: Validate agentskills.io 3-level progressive disclosure (YAML, SKILL.md <=500 lines, references/scripts)."""
    good = smh.validate_progressive_skill_package(
        name="context-hub-docs",
        description="Fetches curated versioned API docs. Use when calling external SDKs. Don't use for local math.",
        skill_md_lines=120,
        companion_files=["references/api_quirks.md", "scripts/chub_lookup.py"],
    )
    self.assertTrue(good.is_valid, msg=str(good.errors))

    bad = smh.validate_progressive_skill_package(
        name="Invalid_Name",
        description="Vague description",
        skill_md_lines=650,
        companion_files=[],
    )
    self.assertFalse(bad.is_valid)
    self.assertFalse(bad.level1_metadata_ok)
    self.assertFalse(bad.level2_body_ok)
    self.assertFalse(bad.level3_companions_ok)

  def test_req0602_context_hub_chub_curated_docs_and_annotations(self) -> None:
    """REQ-0602: Support chub search, get, self-improving annotate, and up/down feedback."""
    reg = smh.ChubRegistry()
    reg.register_doc(
        smh.ChubDocEntry(
            doc_id="openai/chat",
            lang="py",
            version="1.60.0",
            content_md="Call `client.chat.completions.create(model=..., messages=...)`.",
        )
    )
    self.assertEqual(reg.search("completions"), ["openai/chat"])
    reg.annotate("openai/chat", "Use reasoning_effort='medium' for balanced latency.")
    clean_doc = reg.get("openai/chat", lang="py", with_annotations=False)
    self.assertNotIn("UNTRUSTED_LOCAL_ANNOTATION", clean_doc)

    annotated_doc = reg.get("openai/chat", lang="py", with_annotations=True)
    self.assertIn("UNTRUSTED_LOCAL_ANNOTATION", annotated_doc)
    self.assertIn("reasoning_effort='medium'", annotated_doc)

    fb = reg.feedback("openai/chat", "up")
    self.assertEqual(fb["up"], 1)

  def test_req0603_ergonomic_tool_schema_auditor(self) -> None:
    """REQ-0603: Flag raw CRUD tool wrappers and untyped kwargs; approve outcome-based typed tools."""
    bad_crud = {
        "name": "get_user_by_id",
        "parameters": {"properties": {"kwargs": {"type": "object"}}},
    }
    bad_audit = smh.audit_tool_ergonomics(bad_crud)
    self.assertFalse(bad_audit.is_ergonomic)
    self.assertFalse(bad_audit.is_outcome_oriented)
    self.assertFalse(bad_audit.has_strict_typed_schema)

    good_outcome = {
        "name": "settle_customer_invoice",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
                "amount_cents": {"type": "integer"},
            },
            "required": ["account_id", "amount_cents"],
            "additionalProperties": False,
        },
        "error_contract": "Raises InvoiceSettlementError with remediation steps on insufficient balance.",
    }
    good_audit = smh.audit_tool_ergonomics(good_outcome)
    self.assertTrue(good_audit.is_ergonomic, msg=str(good_audit.issues))

  def test_req0604_meta_mcp_code_mode_achieves_over_90_percent_token_savings(self) -> None:
    """REQ-0604: Meta-MCP 'Code Mode' (search + execute) reduces standing schema tokens by >=90%."""
    raw_catalog = [
        {
            "name": f"mcp__saas__operation_{i}",
            "description": "Detailed enterprise SaaS endpoint schema definition " * 8,
            "parameters": {
                "type": "object",
                "properties": {"resource_id": {"type": "string"}, "payload": {"type": "string"}},
                "additionalProperties": False,
            },
        }
        for i in range(100)
    ]
    harness = smh.MetaMcpCodeModeHarness(raw_catalog)
    self.assertEqual(len(harness.standing_wire_schemas()), 2)
    found = harness.search("operation_42")
    self.assertEqual(len(found), 1)
    exec_res = harness.execute([{"tool": "mcp__saas__operation_42", "args": {"resource_id": "R1"}}])
    self.assertEqual(exec_res[0]["status"], "ok")

    savings = smh.measure_code_mode_token_savings(raw_catalog)
    self.assertGreaterEqual(savings.token_reduction_ratio, 0.90)

  def test_req0605_skillsbench_paired_ablation_evaluator(self) -> None:
    """REQ-0605: Compute paired pass-rate lift (pp) and detect self-generated skill regressions."""
    curated = smh.evaluate_skillsbench_ablation(
        with_skill_scores=[True, True, True, False, True],
        without_skill_scores=[False, True, False, False, True],
        is_self_generated=False,
    )
    self.assertEqual(curated.pass_rate_delta_pp, 40.0)
    self.assertEqual(curated.verdict, "CURATED_GAIN")

    self_gen = smh.evaluate_skillsbench_ablation(
        with_skill_scores=[False, False, True, False],
        without_skill_scores=[True, False, True, False],
        is_self_generated=True,
    )
    self.assertLess(self_gen.pass_rate_delta_pp, 0.0)
    self.assertEqual(self_gen.verdict, "SELF_GENERATED_REGRESSION")

  def test_req0606_skill_catalog_overload_detector(self) -> None:
    """REQ-0606: Confirm 2-3 skills in sweet spot and flag >10 skills as severely overloaded."""
    sweet = smh.audit_skill_catalog_overload(["context-hub-docs", "reppit-workflow", "architecture-guard"])
    self.assertTrue(sweet.in_sweet_spot)
    self.assertFalse(sweet.is_severely_overloaded)

    overloaded = smh.audit_skill_catalog_overload([f"skill-{i}" for i in range(12)])
    self.assertFalse(overloaded.in_sweet_spot)
    self.assertTrue(overloaded.is_severely_overloaded)


if __name__ == "__main__":
  unittest.main()
