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

"""Flawed vibe-coded starter for Lab 01 (anti-pattern demonstration).

Anti-patterns present in this file:
1. Synonym drift ('client_id', 'cust_acct', 'tx_amt', 'fee_float') and float money.
2. Unsteered 5-word vibe prompts with zero latency, consistency, reliability,
   security, or maintainability constraints.
3. Blind auto-approve that executes destructive commands ('rm -rf', 'DROP TABLE',
   editing 'adversarial_tests/') without hard floors, circuit breakers, or audit logs.
"""

from __future__ import annotations

from typing import Any


def run_vibe_checkout(payload: dict[str, Any], prompt: str, command: str, auto_approve: bool = True) -> dict[str, Any]:
  """Executes an unvalidated vibe checkout and shell command without guardrails."""
  acct = payload.get("client_id") or payload.get("cust_acct") or payload.get("user_id") or "anon"
  raw_amount = float(payload.get("tx_amt", 0.0)) - float(payload.get("fee_float", 0.0))
  return {
      "account": acct,
      "amount_float": raw_amount * 0.9715,
      "prompt_used": prompt,
      "command_executed": command if auto_approve else "skipped",
  }
