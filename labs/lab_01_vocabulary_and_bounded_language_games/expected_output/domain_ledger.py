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

"""Ubiquitous Language domain model & Wittgensteinian Epistemic Honesty Gate.

Implements REQ-0101 through REQ-0105 for Lab 01:
- Explicit conceptual model & Ubiquitous Language (Unmesh Joshi & Martin Fowler,
  'What Is Code?', 2026)
- Language-Game grounding & Epistemic Honesty (Wittgenstein Philosophical
  Investigations; MaKTO arXiv:2501.14225; Marco Graziano LGDL; SciTePress 139777)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any


ACCOUNT_ID_PATTERN = re.compile(r"^ACCT-[A-Z0-9]{4,12}$")
SUPPORTED_CURRENCIES = frozenset({"USD", "EUR", "GBP", "JPY"})

# Mapping of vibe-coded synonym drift terms to canonical Ubiquitous Language terms
SYNONYM_DRIFT_MAP: dict[str, str] = {
    "client_id": "account_id",
    "cust_acct": "account_id",
    "customer_id": "account_id",
    "user_id": "account_id",
    "tx_amt": "amount_cents",
    "charge_cents": "amount_cents",
    "fee_float": "amount_cents",
    "usd_float": "amount_cents",
    "ccy": "currency",
    "curr": "currency",
}


class EpistemicAction(str, Enum):
  """Decision state in a bounded engineering language game."""

  GROUNDED_EXECUTE = "GROUNDED_EXECUTE"
  CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
  ESCALATE_OUT_OF_BOUNDS = "ESCALATE_OUT_OF_BOUNDS"


@dataclass(frozen=True)
class AccountId:
  """Canonical identifier for a ledger account (REQ-0101)."""

  value: str

  def __post_init__(self) -> None:
    if not isinstance(self.value, str) or not ACCOUNT_ID_PATTERN.match(self.value):
      raise ValueError(
          f"Invalid AccountId '{self.value}': must match ACCT-[A-Z0-9]{{4,12}}"
      )


@dataclass(frozen=True)
class MoneyCents:
  """Exact integer-minor-unit monetary value forbidding float drift (REQ-0101)."""

  amount_cents: int
  currency: str = "USD"

  def __post_init__(self) -> None:
    if isinstance(self.amount_cents, bool) or not isinstance(self.amount_cents, int):
      raise TypeError("MoneyCents.amount_cents must be an exact int (never float)")
    if self.currency not in SUPPORTED_CURRENCIES:
      raise ValueError(f"Unsupported currency '{self.currency}'")

  def add(self, other: MoneyCents) -> MoneyCents:
    if self.currency != other.currency:
      raise ValueError(
          f"Currency mismatch in MoneyCents.add: {self.currency} vs {other.currency}"
      )
    return MoneyCents(self.amount_cents + other.amount_cents, self.currency)


@dataclass(frozen=True)
class LedgerPosting:
  """Single immutable debit or credit entry in the bounded ledger context (REQ-0101)."""

  debit_account: AccountId
  credit_account: AccountId
  money: MoneyCents
  narrative: str

  def __post_init__(self) -> None:
    if self.debit_account == self.credit_account:
      raise ValueError("debit_account and credit_account must be distinct")
    if self.money.amount_cents <= 0:
      raise ValueError("LedgerPosting money.amount_cents must be strictly positive")
    if not self.narrative or not self.narrative.strip():
      raise ValueError("LedgerPosting requires a non-empty domain narrative")


@dataclass
class SettlementBatch:
  """Bounded-context aggregate enforcing double-entry conservation (REQ-0103)."""

  batch_id: str
  base_currency: str = "USD"
  postings: list[LedgerPosting] = field(default_factory=list)
  balances_cents: dict[str, int] = field(default_factory=dict)

  def seed_balance(self, account: AccountId, amount_cents: int) -> None:
    if amount_cents < 0:
      raise ValueError("Initial seed balance cannot be negative")
    self.balances_cents[account.value] = amount_cents

  def apply_postings(self, new_postings: list[LedgerPosting]) -> dict[str, int]:
    """Applies a batch of postings atomically while preserving ledger invariants."""
    if not new_postings:
      raise ValueError("SettlementBatch requires at least one LedgerPosting")

    working = dict(self.balances_cents)
    total_debits = 0
    total_credits = 0

    for posting in new_postings:
      if posting.money.currency != self.base_currency:
        raise ValueError(
            f"Posting currency {posting.money.currency} does not match batch "
            f"base_currency {self.base_currency}"
        )
      debit_key = posting.debit_account.value
      credit_key = posting.credit_account.value
      debit_bal = working.get(debit_key, 0) - posting.money.amount_cents
      if debit_bal < 0:
        raise ValueError(
            f"Insufficient funds in {debit_key}: balance would become {debit_bal}"
        )
      working[debit_key] = debit_bal
      working[credit_key] = working.get(credit_key, 0) + posting.money.amount_cents
      total_debits += posting.money.amount_cents
      total_credits += posting.money.amount_cents

    if total_debits != total_credits:
      raise ValueError("Double-entry conservation invariant violated")

    self.postings.extend(new_postings)
    self.balances_cents = working
    return dict(self.balances_cents)


def audit_vocabulary_drift(payload: dict[str, Any]) -> list[dict[str, str]]:
  """Detects unmapped synonym keys that cause Cognitive Debt (REQ-0102)."""
  findings: list[dict[str, str]] = []
  for key, val in payload.items():
    if key in SYNONYM_DRIFT_MAP:
      findings.append({
          "drifted_term": key,
          "canonical_term": SYNONYM_DRIFT_MAP[key],
          "reason": (
              f"Replace ambiguous term '{key}' with Ubiquitous Language "
              f"identifier '{SYNONYM_DRIFT_MAP[key]}'"
          ),
      })
    if isinstance(val, float):
      findings.append({
          "drifted_term": key,
          "canonical_term": "amount_cents (int)",
          "reason": f"Field '{key}' uses float ({val}); monetary amounts must be int cents",
      })
  return findings


@dataclass(frozen=True)
class LanguageGameEvaluation:
  """Result of evaluating a request through the Wittgensteinian Epistemic Gate."""

  action: EpistemicAction
  confidence: float
  questions: tuple[str, ...]
  normalized_posting: LedgerPosting | None = None
  escalation_reason: str | None = None


def evaluate_language_game_move(
    request: dict[str, Any],
    known_fx_basis_points: dict[tuple[str, str], int] | None = None,
    policy_limit_cents: int = 10_000_00,
    target_currency: str = "USD",
) -> LanguageGameEvaluation:
  """Evaluates a settlement instruction with epistemic honesty (REQ-0104, REQ-0105).

  Instead of guessing missing parameters (Private Language fallacy), this gate
  checks whether every term is grounded in the shared Language Game:
  - Returns ESCALATE_OUT_OF_BOUNDS if policy limits or structural invariants fail.
  - Returns CLARIFICATION_REQUIRED with coworker-style questions if vocabulary
    drifts, fields are ambiguous, or FX conversion rates are ungrounded.
  - Returns GROUNDED_EXECUTE only when confidence >= 0.85 and all domain
    invariants hold.
  """
  known_fx_basis_points = known_fx_basis_points or {}
  questions: list[str] = []
  confidence = 1.0

  drift_findings = audit_vocabulary_drift(request)
  if drift_findings:
    confidence -= 0.35
    for item in drift_findings:
      questions.append(
          f"Clarify vocabulary: '{item['drifted_term']}' is not in the ledger "
          f"Ubiquitous Language. Should this map to '{item['canonical_term']}'?"
      )

  debit_raw = request.get("debit_account")
  credit_raw = request.get("credit_account")
  amount_raw = request.get("amount_cents")
  currency = request.get("currency", target_currency)
  narrative = request.get("narrative", "")

  if not debit_raw or not credit_raw:
    confidence -= 0.40
    questions.append(
        "Which canonical AccountId (ACCT-XXXX) should be debited and credited?"
    )

  if not isinstance(amount_raw, int) or isinstance(amount_raw, bool):
    confidence -= 0.40
    questions.append(
        "What is the exact integer amount in minor units (amount_cents)?"
    )
  elif amount_raw <= 0:
    return LanguageGameEvaluation(
        action=EpistemicAction.ESCALATE_OUT_OF_BOUNDS,
        confidence=0.0,
        questions=(),
        escalation_reason="amount_cents must be strictly positive",
    )

  if not narrative or not str(narrative).strip():
    confidence -= 0.25
    questions.append(
        "What is the business settlement narrative/invoice reference for this posting?"
    )

  converted_cents = amount_raw if isinstance(amount_raw, int) else 0
  if currency != target_currency:
    pair = (currency, target_currency)
    if pair not in known_fx_basis_points:
      confidence = min(confidence, 0.50)
      questions.append(
          f"Missing grounded FX rate for {currency}->{target_currency}. "
          "What authoritative basis-point rate should be applied?"
      )
    elif isinstance(amount_raw, int):
      # Basis points: 10000 bp = 1.0000x
      converted_cents = (amount_raw * known_fx_basis_points[pair]) // 10_000

  if isinstance(converted_cents, int) and converted_cents > policy_limit_cents:
    return LanguageGameEvaluation(
        action=EpistemicAction.ESCALATE_OUT_OF_BOUNDS,
        confidence=round(max(0.0, confidence), 2),
        questions=tuple(questions),
        escalation_reason=(
            f"Converted amount {converted_cents} cents exceeds autonomous policy "
            f"limit of {policy_limit_cents} cents"
        ),
    )

  confidence = round(max(0.40 if questions else 0.0, min(1.0, confidence)), 2)
  if questions or confidence < 0.85:
    return LanguageGameEvaluation(
        action=EpistemicAction.CLARIFICATION_REQUIRED,
        confidence=min(confidence, 0.75),
        questions=tuple(questions),
        normalized_posting=None,
    )

  posting = LedgerPosting(
      debit_account=AccountId(str(debit_raw)),
      credit_account=AccountId(str(credit_raw)),
      money=MoneyCents(converted_cents, target_currency),
      narrative=str(narrative).strip(),
  )
  return LanguageGameEvaluation(
      action=EpistemicAction.GROUNDED_EXECUTE,
      confidence=confidence,
      questions=(),
      normalized_posting=posting,
  )
