# Lab 01 Walkthrough: Vibe Coding vs. Software-Engineering Steering & The Ladder of Earned Autonomy (`TaskFlow` Billing & Workspace Platform)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Opening Conceptual Foundation: Why Natural Language Coordinates Code & Action
Welcome to **Lab 01** of our journey building and governing the **`TaskFlow` Productivity & Workspace Platform**! Why can a software engineer type natural-language English into a terminal coding agent (`agy` or `claude`) and produce working production software? Three foundational insights explain how natural language coordinates code and action:

1. **Wittgenstein's Two Theories of Language:** Early Wittgenstein (*Tractatus Logico-Philosophicus*, 1921) modeled language as a strict, formal, 1-to-1 logical picture of facts—mirroring how compilers, static type systems, and deterministic unit tests evaluate formal Python source code. Late Wittgenstein (*Philosophical Investigations*, 1953) recognized that everyday human language is not a static logical calculus, but an active toolbox used between collaborators (the human Builder and the AI Coding Agent) to coordinate actions within shared rules.
2. **Code as an Externalized Conceptual Model (Unmesh Joshi & Martin Fowler, *What Is Code?*, 2026):** As LLMs commoditize the mechanical typing of syntax, code remains critical because it simultaneously instructs the machine and captures the team's **Ubiquitous Language**. When engineers passively accept unreviewed "Ralph Wiggum" vibe-coded output, the `TaskFlow` codebase rapidly accumulates **Cognitive Debt**—synonym drift across `client_id`, `cust_acct`, `user_id`, and `tx_amt`, or IEEE-754 `float` rounding errors on subscription billing amounts.
3. **Andrew Ng's Core Insight on Vibe Coding (*The AI Engineering Skills Map*, Pillar 02):** In DeepLearning.AI's *AI Engineering Skills Map* (synthesized from over 10,000 AI engineering roles), **Pillar 02 (Software Engineering Fundamentals)** sits directly alongside **Pillar 03 (Using Coding Agents)**. A novice who vibe-codes a `TaskFlow` workspace billing feature with a 5-word prompt (`"make checkout work fast"`) forces the LLM to silently guess architectural trade-offs across **latency**, **consistency**, **reliability**, **security**, and **maintainability**. An engineer who knows software fundamentals steers the agent with explicit constraints (`p99 <= 150ms`, `STRONG` consistency with exact integer cents, idempotency keys, parameterized queries, and typed domain interfaces) and governs execution along the **4-Tier Ladder of Earned Autonomy** (`andrewyng/openworker` & Karpathy's *Software 3.0*).

### The Headache (Unsteered Vibe Coding & Ungoverned Auto-Approve)
When a developer vibe-codes `TaskFlow`'s workspace billing settlement endpoint as shown in [`starter/vibe_prompt_and_autonomy_blob.py`](./starter/vibe_prompt_and_autonomy_blob.py) without domain steering or permission guardrails:
- **Synonym & Float Money Drift:** The function accepts `client_id`, `cust_acct`, `user_id`, and `tx_amt` interchangeably and multiplies IEEE-754 `float` amounts (`raw_amount * 0.9715`), silently losing pennies on workspace invoices.
- **Unsteered 5-Word Prompts:** Prompts like `"make checkout work fast"` omit all 5 Pillar-02 engineering dimensions (`latency_ms_p99`, `consistency_model`, `reliability_strategy`, `security_boundary`, `maintainability_contract`).
- **Blind Auto-Approve (`auto_approve=True`):** Setting `auto_approve=True` blindly executes `rm -rf /`, `DROP TABLE ledger`, `git push --force`, or edits to `adversarial_tests/` with zero hard floors, zero circuit breakers, and zero provenance audit logs.

### The Everyday Metaphor (`Known -> Target`)
Think of **Software-Engineering Prompt Steering & Earned Autonomy** like **programming an commercial airliner's autopilot with a flight plan and hard flight-envelope protections** (*Known* $\to$ *Target*). Telling an autopilot *"fly to Chicago fast"* (*vibe prompt*) invites disaster; a pilot enters exact altitude, airspeed, and routing constraints (*Pillar 02 steering*), while hard-wired envelope protections (*OpenWorker Tier-1 Hard Floors*) physically prevent the plane from stalling or diving even when autopilot is engaged (`always-proceed` / `auto`).

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/vibe_prompt_and_autonomy_blob.py`
Open [`starter/vibe_prompt_and_autonomy_blob.py`](./starter/vibe_prompt_and_autonomy_blob.py) (`lines 30–39`). Notice how `run_vibe_checkout()` chains untyped dictionary lookups (`payload.get("client_id") or payload.get("cust_acct")`), casts monetary fees to `float`, and executes arbitrary shell strings whenever `auto_approve=True`.

### Implementing `prompt_steerer.py` (`REQ-0101` through `REQ-0106`)
Implement [`expected_output/prompt_steerer.py`](./expected_output/prompt_steerer.py) (or your custom `work/prompt_steerer.py`) to satisfy all 6 verifiable requirements for the `TaskFlow` platform:

1. **`REQ-0101` (Ubiquitous Language Value Objects & Synonym Drift Detector)**:
   - Implement `AccountId(value: str)` enforcing `^ACCT-[A-Z0-9]{4,12}$`.
   - Implement `MoneyCents(amount_cents: int, currency: str)` rejecting `float` and `bool` values (`TypeError`) and enforcing 3-letter uppercase ISO currency codes (`^[A-Z]{3}$`).
   - Implement `audit_ubiquitous_language(payload)` flagging drifted keys in `SYNONYM_DRIFT_MAP` (`client_id`, `cust_acct`, `user_id`, `acct_no`, `tx_amt`, `amount_float`, `fee_float`, `ccy`) and any `float` numeric value.
2. **`REQ-0102` (Software-Engineering Prompt Steerer — Skills Map Pillar 02)**:
   - Implement `EngineeringConstraints(latency_ms_p99, consistency_model, reliability_strategy, security_boundary, maintainability_contract)` and `evaluate_prompt_steering(prompt_text, constraints, sample_payload)` returning `PromptSteeringReport(status, steering_score, missing_dimensions, ubiquitous_language_violations, compiled_prompt)`.
3. **`REQ-0103` (Dual-Harness Permission Mode Mapper)**:
   - Implement `map_harness_permission_mode(harness, mode)` mapping Google Antigravity (`agy`: `strict`, `request-review`, `proceed-in-sandbox`, `always-proceed`) and Claude Code (`claude`: `plan`, `default`, `acceptEdits`, `auto`) modes to `AutonomyTier` (`TIER_1_PLAN_OR_STRICT` through `TIER_4_GOVERNED_AUTO_LOOP`) and `HarnessPermissionProfile`.
4. **`REQ-0104` (Hard Floors Against Destructive Operations)**:
   - Implement `is_hard_floor_violation(command_or_target)` and `EarnedAutonomyGate.evaluate_action(...)` returning `GateDecision.HARD_FLOOR_BLOCKED` on destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`, `git reset --hard`, `chmod a+rwx`, `curl ... | sh`), `.env` secret reads, or mutations to `adversarial_tests/` regardless of permission mode or human approval.
5. **`REQ-0105` (Reviewer Circuit Breaker & Unattended Self-Approval Guard)**:
   - Trip `circuit_breaker_tripped = True` after `max_consecutive_denials` (`3`) denials, halting subsequent actions with `GateDecision.CIRCUIT_BREAKER_HALTED` until `reset_circuit_breaker(human_verified=True)` is called, and block unallowlisted commands when `unattended=True` (`GateDecision.UNATTENDED_SELF_APPROVAL_DENIED`).
6. **`REQ-0106` (Provenance Audit Trail)**:
   - Record every evaluated action in `gate.audit_log` as an `AuditLogEntry` with `provenance` in `{"auto-approved", "user-approved", "denied"}`.

### Verification Commands
```bash
# Verify the reference solution against immutable adversarial tests + unit tests
./labs/lab_01_vibe_coding_and_earned_autonomy/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_01_vibe_coding_and_earned_autonomy/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"Enabling `always-proceed` in Antigravity or `auto` mode in Claude Code means the agent should be allowed to run any shell command or edit test files if a human passes `user_explicitly_approved=True`."*
>
> **✓ Reality:** In the 4-Tier `openworker` Governance architecture, **Tier-1 Hard Floors are non-negotiable invariants** (*"the fixer is never the only checker"*). Even in `TIER_4_GOVERNED_AUTO_LOOP` with `user_explicitly_approved=True`, destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`), `.env` secret reads, and mutations to `adversarial_tests/` MUST be blocked at the harness gate (`HARD_FLOOR_BLOCKED`) before execution.

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Predict-the-Outcome`):** Suppose an engineer configures `EarnedAutonomyGate` with `map_harness_permission_mode("claude", "auto")` and `max_consecutive_denials=3`. The agent executes two consecutive actions where `reviewer_approved=False`, followed by one unattended action `gate.evaluate_action("python3 scripts/migrate_prod.py", unattended=True)`. If the engineer then runs `gate.evaluate_action("git status", user_explicitly_approved=True)`, what `GateDecision` and `provenance` are returned, and why?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect how `_record(..., is_denial=True)` updates `self.consecutive_denials` and `self.circuit_breaker_tripped` inside `EarnedAutonomyGate.evaluate_action()` in [`expected_output/prompt_steerer.py`](./expected_output/prompt_steerer.py).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Trace the denial counter step by step: the two `reviewer_approved=False` calls return `REVIEWER_DENIED` (`consecutive_denials` becomes `1`, then `2`). The third call (`"python3 scripts/migrate_prod.py"` with `unattended=True`) is not in `allowed_command_prefixes`, so it returns `UNATTENDED_SELF_APPROVAL_DENIED` (`consecutive_denials` reaches `3`, tripping `circuit_breaker_tripped = True`).
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
Because `circuit_breaker_tripped` is checked at the very top of `evaluate_action()` (before allowlists or `user_explicitly_approved`), the fourth call (`"git status"`) immediately returns **`GateDecision.CIRCUIT_BREAKER_HALTED`** with **`provenance="denied"`**. The circuit breaker remains locked until a human explicitly calls `gate.reset_circuit_breaker(human_verified=True)`.
</details>

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `starter/vibe_prompt_and_autonomy_blob.py` using `@labs/lab_01_vibe_coding_and_earned_autonomy/starter/vibe_prompt_and_autonomy_blob.py` in `/plan` mode and check permission settings via `/config`.
3. Verify your workspace is clean before writing code:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_01_vibe_coding_and_earned_autonomy/work/prompt_steerer.py` and `test_prompt_steerer.py`, then run:
   ```bash
   ./labs/lab_01_vibe_coding_and_earned_autonomy/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode` (`Shift+Tab`), inspect `starter/vibe_prompt_and_autonomy_blob.py` and identify all missing engineering constraints and ungoverned permission paths.
3. Verify no files were mutated during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_01_vibe_coding_and_earned_autonomy/work/prompt_steerer.py` and `test_prompt_steerer.py`, then verify:
   ```bash
   ./labs/lab_01_vibe_coding_and_earned_autonomy/self_diagnose.sh work
   ```
