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

"""Unit tests for Lab 01: Ubiquitous Language & Wittgensteinian Epistemic Gate."""

from __future__ import annotations

import unittest
from domain_ledger import (
    AccountId,
    EpistemicAction,
    LedgerPosting,
    MoneyCents,
    SettlementBatch,
    audit_vocabulary_drift,
    evaluate_language_game_move,
)


class TestDomainLedgerAndLanguageGame(unittest.TestCase):
  """Verifies REQ-0101 through REQ-0106."""

  def test_req0101_ubiquitous_language_value_objects(self) -> None:
    """REQ-0101: Canonical AccountId and MoneyCents reject floats and invalid IDs."""
    acct_a = AccountId("ACCT-1001")
    acct_b = AccountId("ACCT-2002")
    self.assertEqual(acct_a.value, "ACCT-1001")

    with self.assertRaises(ValueError):
      AccountId("client_99")

    with self.assertRaises(TypeError):
      MoneyCents(19.99, "USD")  # type: ignore[arg-type]

    m1 = MoneyCents(1250, "USD")
    m2 = MoneyCents(750, "USD")
    self.assertEqual(m1.add(m2), MoneyCents(2000, "USD"))

    posting = LedgerPosting(acct_a, acct_b, m1, "INV-2026-001")
    self.assertEqual(posting.money.amount_cents, 1250)

  def test_req0102_vocabulary_synonym_drift_detector(self) -> None:
    """REQ-0102: Detects vibe-coded synonym drift and float amounts."""
    drifted_payload = {
        "client_id": "ACCT-1001",
        "cust_acct": "ACCT-2002",
        "tx_amt": 49.95,
    }
    findings = audit_vocabulary_drift(drifted_payload)
    drifted_terms = {f["drifted_term"] for f in findings}
    self.assertIn("client_id", drifted_terms)
    self.assertIn("cust_acct", drifted_terms)
    self.assertIn("tx_amt", drifted_terms)

  def test_req0103_settlement_batch_double_entry_conservation(self) -> None:
    """REQ-0103: Enforces double-entry conservation and non-negative balances."""
    treasury = AccountId("ACCT-TREAS01")
    merchant = AccountId("ACCT-MERCH01")
    batch = SettlementBatch(batch_id="BATCH-01", base_currency="USD")
    batch.seed_balance(treasury, 50_000)
    batch.seed_balance(merchant, 10_000)

    posting = LedgerPosting(
        debit_account=treasury,
        credit_account=merchant,
        money=MoneyCents(15_000, "USD"),
        narrative="Settlement payout #101",
    )
    balances = batch.apply_postings([posting])
    self.assertEqual(balances["ACCT-TREAS01"], 35_000)
    self.assertEqual(balances["ACCT-MERCH01"], 25_000)

    # Overdraft attempt must fail without mutating state
    with self.assertRaises(ValueError):
      batch.apply_postings([
          LedgerPosting(
              debit_account=treasury,
              credit_account=merchant,
              money=MoneyCents(99_000, "USD"),
              narrative="Overdraft attempt",
          )
      ])
    self.assertEqual(batch.balances_cents["ACCT-TREAS01"], 35_000)

  def test_req0104_epistemic_confidence_gate_grounded_execution(self) -> None:
    """REQ-0104: Grounded requests execute with confidence >= 0.85."""
    req = {
        "debit_account": "ACCT-TREAS01",
        "credit_account": "ACCT-MERCH01",
        "amount_cents": 25_000,
        "currency": "EUR",
        "narrative": "EU Invoice #884",
    }
    fx_bp = {("EUR", "USD"): 10_800}  # 1 EUR = 1.0800 USD
    res = evaluate_language_game_move(req, known_fx_basis_points=fx_bp)
    self.assertEqual(res.action, EpistemicAction.GROUNDED_EXECUTE)
    self.assertGreaterEqual(res.confidence, 0.85)
    self.assertEqual(res.questions, ())
    self.assertIsNotNone(res.normalized_posting)
    assert res.normalized_posting is not None
    self.assertEqual(res.normalized_posting.money.amount_cents, 27_000)

  def test_req0105_epistemic_honesty_on_missing_fx_and_ambiguous_vocab(self) -> None:
    """REQ-0105: Missing FX rate or synonym drift returns CLARIFICATION_REQUIRED."""
    ungrounded_req = {
        "client_id": "ACCT-TREAS01",
        "debit_account": "ACCT-TREAS01",
        "credit_account": "ACCT-MERCH01",
        "amount_cents": 25_000,
        "currency": "JPY",
        "narrative": "Tokyo settlement",
    }
    res = evaluate_language_game_move(ungrounded_req, known_fx_basis_points={})
    self.assertEqual(res.action, EpistemicAction.CLARIFICATION_REQUIRED)
    self.assertLess(res.confidence, 0.85)
    self.assertGreaterEqual(len(res.questions), 2)
    self.assertIsNone(res.normalized_posting)

  def test_req0106_escalate_out_of_bounds_policy_limit(self) -> None:
    """REQ-0106: Requests exceeding autonomous policy limits trigger escalation."""
    req = {
        "debit_account": "ACCT-TREAS01",
        "credit_account": "ACCT-MERCH01",
        "amount_cents": 50_000_00,
        "currency": "USD",
        "narrative": "Large wire transfer",
    }
    res = evaluate_language_game_move(req, policy_limit_cents=10_000_00)
    self.assertEqual(res.action, EpistemicAction.ESCALATE_OUT_OF_BOUNDS)
    self.assertIsNotNone(res.escalation_reason)


if __name__ == "__main__":
  unittest.main()
