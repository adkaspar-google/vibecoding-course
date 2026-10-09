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

"""Unit tests for Lab 01 prompt_steerer.py."""

from __future__ import annotations

import unittest

import prompt_steerer as ps


class TestPromptSteerer(unittest.TestCase):
  """User unit tests for Lab 01."""

  def test_ubiquitous_language_and_steering(self) -> None:
    acct = ps.AccountId("ACCT-9001A")
    money = ps.MoneyCents(2500, "USD")
    self.assertEqual(acct.value, "ACCT-9001A")
    self.assertEqual(money.amount_cents, 2500)

    constraints = ps.EngineeringConstraints(
        latency_ms_p99=120,
        consistency_model="STRONG",
        reliability_strategy="IDEMPOTENCY_KEY_AND_RETRY",
        security_boundary="AUTHZ_AND_INPUT_VALIDATION",
        maintainability_contract="TYPED_INTERFACES",
    )
    report = ps.evaluate_prompt_steering(
        "Implement idempotent ledger settlement endpoint.",
        constraints=constraints,
        sample_payload={"debit_account_id": "ACCT-9001A", "amount_cents": 2500},
    )
    self.assertEqual(report.status, ps.SteeringStatus.PRODUCTION_STEERED)
    self.assertEqual(report.steering_score, 1.0)


if __name__ == "__main__":
  unittest.main()
