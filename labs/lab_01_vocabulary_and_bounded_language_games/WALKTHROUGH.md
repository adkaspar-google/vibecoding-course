# Lab 01: Code as Conceptual Model, Ubiquitous Language & Wittgensteinian Epistemic Honesty

## 1. Learning Objectives & Theoretical Grounding

1. **Code as a Model of Understanding (Unmesh Joshi & Martin Fowler, *What Is Code?*, 2026)**:
   As LLMs commoditize the mechanical typing of syntax, the primary role of software engineering shifts to making the **conceptual model explicit**, discovering the right **domain vocabulary**, and preventing **Cognitive Debt** (where plausible-looking LLM abstractions drift across synonyms like `client_id`, `cust_acct`, `user_id`, and `tx_amt`).
2. **Wittgenstein's Language Games & Epistemic Honesty (Z. He *SciTePress 139777*, Ye et al. *MaKTO* `arXiv:2501.14225`, Marco Graziano *LGDL*)**:
   By Wittgenstein's *Private Language Argument*, statistical next-token continuation has no internal criterion of correctness. Grounding an agent requires bounding it in an explicit **Engineering Language Game** with a **Confidence Gate**:
   - Execute (`GROUNDED_EXECUTE`) when every term and conversion rule is grounded ($\text{confidence} \ge 0.85$).
   - Ask coworker-style clarifying questions (`CLARIFICATION_REQUIRED`) when domain vocabulary drifts or parameters (such as cross-currency FX rates) are ungrounded.
   - Escalate (`ESCALATE_OUT_OF_BOUNDS`) when policy limits or invariants are violated.

---

## 2. Inspecting the Cognitive-Debt Starter (`starter/vibe_billing_blob.py`)

Inspect `starter/vibe_billing_blob.py`. Notice three classic "Ralph Wiggum" vibe-coding failure modes:
- **Synonym Drift**: Accepts `client_id`, `cust_acct`, `user_id`, `tx_amt`, and `fee_float` interchangeably.
- **Float Money Drift**: Multiplies IEEE-754 floats (`amt * rate * 0.9715`), silently losing cents.
- **Silent Hallucination**: Uses `fx_table.get(ccy, 1.0)`—silently assuming a `1.0` exchange rate when `JPY` or `EUR` rates are missing instead of asking for clarification!

---

## 3. Step-by-Step Implementation (`domain_ledger.py`)

Implement `domain_ledger.py` satisfying `REQ-0101` through `REQ-0106`:
1. **`REQ-0101` (Ubiquitous Language Value Objects)**:
   - `AccountId(value: str)` enforcing `^ACCT-[A-Z0-9]{4,12}$`.
   - `MoneyCents(amount_cents: int, currency: str)` rejecting `float` and `bool` values.
   - `LedgerPosting(debit_account, credit_account, money, narrative)`.
2. **`REQ-0102` (Synonym Drift Detector)**:
   - `audit_vocabulary_drift(payload)` flagging drifted keys (`client_id`, `cust_acct`, `tx_amt`, `fee_float`, etc.) and any `float` monetary field.
3. **`REQ-0103` (Bounded-Context Conservation Invariant)**:
   - `SettlementBatch.apply_postings(new_postings)` enforcing currency homogeneity, non-negative account balances, and double-entry conservation ($\sum \text{debits} = \sum \text{credits}$).
4. **`REQ-0104` & `REQ-0105` (Wittgensteinian Epistemic Confidence Gate)**:
   - `evaluate_language_game_move(request, known_fx_basis_points, policy_limit_cents, target_currency)` returning `LanguageGameEvaluation(action, confidence, questions, normalized_posting, escalation_reason)`.
   - Never guess missing FX rates; return `EpistemicAction.CLARIFICATION_REQUIRED` with explicit coworker-style questions.
5. **`REQ-0106` (Policy Escalation & Unit Tests)**:
   - Return `EpistemicAction.ESCALATE_OUT_OF_BOUNDS` when converted amount exceeds `policy_limit_cents` or `amount_cents <= 0`.

---

## 4. Verification Command

```bash
./labs/lab_01_vocabulary_and_bounded_language_games/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity in learner mode from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `starter/vibe_billing_blob.py` using `@labs/lab_01_vocabulary_and_bounded_language_games/starter/vibe_billing_blob.py` in read-only planning mode (`/plan`).
3. Verify your workspace state before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_01_vocabulary_and_bounded_language_games/work/domain_ledger.py` and `test_domain_ledger.py`, then run:
   ```bash
   ./labs/lab_01_vocabulary_and_bounded_language_games/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `starter/vibe_billing_blob.py` and list every synonym drift and ungrounded FX assumption.
3. Run the human approval checkpoint to verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_01_vocabulary_and_bounded_language_games/work/domain_ledger.py` and `test_domain_ledger.py`, then verify:
   ```bash
   ./labs/lab_01_vocabulary_and_bounded_language_games/self_diagnose.sh work
   ```
