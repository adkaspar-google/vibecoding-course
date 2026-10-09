# Lab 01: Shared Domain Vocabulary & Coworker Clarification

## 1. Learning Objectives & Conceptual Motivation

1. **Code as a Model of Understanding (Unmesh Joshi & Martin Fowler, *What Is Code?*, 2026)**:
   As LLMs commoditize the mechanical typing of syntax, the primary role of software engineering shifts to making the **conceptual model explicit**, discovering a consistent **Ubiquitous Language**, and preventing **Cognitive Debt** (where plausible-looking LLM abstractions drift across synonyms like `client_id`, `cust_acct`, `user_id`, and `tx_amt`).
2. **Wittgenstein's Two Theories of Language — How We Use Language to Produce Code & Actions**:
   - **Early Wittgenstein (*Tractatus Logico-Philosophicus*, 1921) — Picture Theory of Language:** Language as a strict, formal, 1-to-1 logical picture of facts $\leftrightarrow$ traditional code, type systems, and unit tests (*exact instructions for a machine*).
   - **Late Wittgenstein (*Philosophical Investigations*, 1953) — Meaning as Use & Language as Action:** Natural language as a collaborative toolbox used between coworkers (the Builder & Assistant in `§2`) to coordinate actions (`Molino & Tagliabue, arXiv:2302.01570`; `Winograd & Flores, 1986`).
   - **Empirical Grounding in Coding Agents (`Wang, Liang, & Manning, ACL 2016, arXiv:1606.02447`; `Ye et al. MaKTO, arXiv:2501.14225`; `Marco Graziano LGDL`; `Z. He SciTePress 139777`):** In interactive Builder–Assistant tasks where humans instruct an AI agent solely through natural language to perform actions, task completion depends on **(a) avoiding synonyms** (consistent vocabulary) and **(b) asking coworker-style clarifying questions** rather than guessing missing parameters:
     - Execute (`GROUNDED_EXECUTE`) when every domain term and conversion rule is grounded ($\text{confidence} \ge 0.85$).
     - Ask coworker-style clarifying questions (`CLARIFICATION_REQUIRED`) when domain vocabulary drifts or parameters (such as cross-currency FX rates) are ungrounded.
     - Escalate (`ESCALATE_OUT_OF_BOUNDS`) when policy limits or invariants are violated.

---

## 2. Inspecting the Cognitive-Debt Starter (`starter/vibe_billing_blob.py`)

Inspect `starter/vibe_billing_blob.py`. Notice three classic "Ralph Wiggum" vibe-coding failure modes:
- **Synonym Drift**: Accepts `client_id`, `cust_acct`, `user_id`, `tx_amt`, and `fee_float` interchangeably.
- **Float Money Drift**: Multiplies IEEE-754 floats (`amt * rate * 0.9715`), silently losing cents.
- **Silent Hallucination**: Uses `fx_table.get(ccy, 1.0)`—silently assuming a `1.0` exchange rate when `JPY` or `EUR` rates are missing instead of asking a coworker-style clarifying question!

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
4. **`REQ-0104` & `REQ-0105` (Coworker Readiness & Clarification Gate)**:
   - `evaluate_request_readiness(request, known_fx_basis_points, policy_limit_cents, target_currency)` (aliased as `evaluate_language_game_move`) returning `RequestReadinessEvaluation` / `LanguageGameEvaluation(action, confidence, questions, normalized_posting, escalation_reason)`.
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
