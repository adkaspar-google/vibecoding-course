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

"""Starter vibe-coded billing script exhibiting severe Cognitive Debt.

Anti-patterns present in this file (Unmesh Joshi / Martin Fowler, 2026;
Marco Graziano Wittgenstein LGDL, 2025):
1. Synonym drift: mixes 'client_id', 'cust_acct', 'user_id', 'tx_amt', 'fee_float'.
2. Floating-point money arithmetic causing IEEE-754 rounding drift.
3. Silent hallucination: guesses a 1.0 exchange rate when FX rate is missing
   instead of pausing to ask clarifying questions (zero epistemic honesty).
"""

from __future__ import annotations
from typing import Any


def process_vibe_payment(payload: dict[str, Any], fx_table: dict[str, float] | None = None) -> dict[str, Any]:
  """Processes a payment using ad-hoc vibe-coded heuristics (BROKEN)."""
  fx_table = fx_table or {}
  who = (
      payload.get("client_id")
      or payload.get("cust_acct")
      or payload.get("user_id")
      or "anon"
  )
  amt = float(payload.get("tx_amt") or payload.get("fee_float") or 0.0)
  ccy = payload.get("currency", "USD")
  # BUG: Silently guesses 1.0 when currency conversion rate is unknown!
  rate = fx_table.get(ccy, 1.0)
  settled_usd = amt * rate * 0.9715
  return {"account": who, "settled_usd": settled_usd, "status": "EXECUTED"}
