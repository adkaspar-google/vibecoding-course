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

"""Immutable adversarial verifier for Lab 01 (REQ-0101..REQ-0106)."""

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


class TestLab01ImmutableVerifier(unittest.TestCase):
  """Adversarial verification suite for Lab 01."""

  def test_req0101_rejects_boolean_and_float_money(self) -> None:
    with self.assertRaises(TypeError):
      MoneyCents(True, "USD")  # type: ignore[arg-type]
    with self.assertRaises(TypeError):
      MoneyCents(10.5, "USD")  # type: ignore[arg-type]

  def test_req0102_detects_all_drifted_keys(self) -> None:
    findings = audit_vocabulary_drift({"user_id": "ACCT-1111", "usd_float": 1.5})
    self.assertGreaterEqual(len(findings), 2)

  def test_req0103_double_entry_sum_conserved(self) -> None:
    batch = SettlementBatch("B-99", "USD")
    a1 = AccountId("ACCT-AAAA")
    a2 = AccountId("ACCT-BBBB")
    batch.seed_balance(a1, 1000)
    batch.seed_balance(a2, 500)
    batch.apply_postings([LedgerPosting(a1, a2, MoneyCents(400, "USD"), "Ref-1")])
    self.assertEqual(sum(batch.balances_cents.values()), 1500)

  def test_req0104_and_req0105_never_guesses_fx_rate(self) -> None:
    res = evaluate_language_game_move(
        {
            "debit_account": "ACCT-AAAA",
            "credit_account": "ACCT-BBBB",
            "amount_cents": 5000,
            "currency": "GBP",
            "narrative": "Cross-border invoice",
        },
        known_fx_basis_points={},
    )
    self.assertEqual(res.action, EpistemicAction.CLARIFICATION_REQUIRED)
    self.assertTrue(any("GBP->USD" in q for q in res.questions))


if __name__ == "__main__":
  unittest.main()
