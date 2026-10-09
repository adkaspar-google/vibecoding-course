# Lab 01: Vibe Coding vs. Software-Engineering Steering & The Ladder of Earned Autonomy

## 1. Learning Objectives & Conceptual Motivation

1. **Why Natural Language Coordinates Code & Action (Opening Conceptual Foundation)**:
   Why can a software engineer type natural-language English into a terminal agent and produce working software? Two complementary perspectives explain the bridge between human intent and executable code:
   - **Wittgenstein's Two Theories of Language:** Early Wittgenstein (*Tractatus Logico-Philosophicus*, 1921) modeled language as a strict, formal, 1-to-1 logical picture of facts—mirroring how compilers, static type systems, and deterministic unit tests evaluate formal source code. Late Wittgenstein (*Philosophical Investigations*, 1953) recognized that everyday human language is not a static logical calculus, but an active toolbox used between collaborators (the Builder and Assistant in `§2`) to coordinate actions within shared rules.
   - **Code as an Externalized Conceptual Model (Unmesh Joshi & Martin Fowler, *What Is Code?*, 2026):** As LLMs commoditize the mechanical typing of syntax, code remains critical because it simultaneously instructs the machine and captures the team's **Ubiquitous Language**. When engineers passively accept "Ralph Wiggum" vibe-coded output without enforcing consistent domain vocabulary, codebases accumulate **Cognitive Debt** (synonym drift across `client_id`, `cust_acct`, `user_id`, and `tx_amt`, or IEEE-754 `float` money errors).

2. **Andrew Ng's Core Insight on Vibe Coding (*The AI Engineering Skills Map*, Pillar 02)**:
   In DeepLearning.AI's *AI Engineering Skills Map* (synthesized from over 10,000 AI engineering roles), **Pillar 02 (Software Engineering Fundamentals)** sits alongside **Pillar 03 (Using Coding Agents)**. A novice who vibe codes with a vague prompt (`"build a fast payment endpoint"`) forces the coding agent to silently guess architectural tradeoffs across **latency**, **consistency**, **reliability**, **security**, and **maintainability**. An engineer who knows software fundamentals steers the agent with explicit constraints (`p99 <= 150ms`, `STRONG` consistency with integer cents, idempotency keys, parameterized queries, and typed domain interfaces).

3. **The Autonomy Slider & 4-Tier "Governed by Design" Harness (`andrewyng/openworker` & Karpathy's *Software 3.0*)**:
   - **Orchestration Over Automation ("The Conductor Mindset"):** Engineers calibrate agent autonomy along a spectrum from interactive diff review to bounded autonomous loops:
     - **Google Antigravity (`agy`) Permission Modes** (`~/.gemini/antigravity-cli/settings.json`): `strict`, `request-review`, `proceed-in-sandbox`, `always-proceed`.
     - **Claude Code (`claude`) Permission Modes** (`.claude/settings.json` / `Shift+Tab`): `default`, `plan`, `acceptEdits`, `auto`.
   - **4-Tier Governance (`openworker`):**
     1. **Hard Floors:** Destructive or irreversible actions (`rm -rf`, `DROP TABLE`, `git push --force`, mutating `adversarial_tests/`, reading `.env` secrets) are blocked even in `always-proceed` or `auto` mode (*"the fixer is never the only checker"*).
     2. **Ladder of Earned Autonomy:** Routine safe commands graduate to allowlists, while a **Reviewer Circuit Breaker** trips after repeated denials (`>= 3`) and unattended runs never self-approve unverified shell actions.
     3. **Audit Trail with Provenance:** Every tool call is recorded with `auto-approved`, `user-approved`, or `denied` plus reviewer reasoning.

---

## 2. Inspecting the Flawed Baseline (`starter/vibe_prompt_and_autonomy_blob.py`)

Inspect `starter/vibe_prompt_and_autonomy_blob.py`. Notice three critical failure modes:
- **Synonym & Float Money Drift**: Accepts `client_id`, `cust_acct`, `tx_amt`, and IEEE-754 `float` amounts interchangeably.
- **Unsteered Vibe Prompts**: Passes raw 5-word prompts (`"make checkout work fast"`) directly to execution with zero latency, consistency, reliability, security, or maintainability constraints.
- **Ungoverned Auto-Approve**: Setting `auto_approve=True` blindly executes `rm -rf /`, `DROP TABLE ledger`, or modifications to `adversarial_tests/` with no hard floors, no circuit breaker, and no provenance audit log.

---

## 3. Step-by-Step Implementation (`prompt_steerer.py`)

Implement `prompt_steerer.py` satisfying `REQ-0101` through `REQ-0106`:
1. **`REQ-0101` (Ubiquitous Language Value Objects & Synonym Drift Detector)**:
   - `AccountId(value: str)` enforcing `^ACCT-[A-Z0-9]{4,12}$`.
   - `MoneyCents(amount_cents: int, currency: str)` rejecting `float` and `bool` values and enforcing 3-letter uppercase ISO currency codes.
   - `audit_ubiquitous_language(payload)` flagging drifted keys (`client_id`, `cust_acct`, `user_id`, `tx_amt`, `fee_float`) and any `float` monetary field.
2. **`REQ-0102` (Software-Engineering Prompt Steerer — Skills Map Pillar 02)**:
   - `EngineeringConstraints(latency_ms_p99, consistency_model, reliability_strategy, security_boundary, maintainability_contract)` and `evaluate_prompt_steering(prompt_text, constraints)` returning `PromptSteeringReport(status, steering_score, missing_dimensions, compiled_prompt)`.
3. **`REQ-0103` (Dual-Harness Permission Mode Mapper)**:
   - `map_harness_permission_mode(harness, mode)` mapping `agy` (`strict`, `request-review`, `proceed-in-sandbox`, `always-proceed`) and `claude` (`default`, `plan`, `acceptEdits`, `auto`) modes to `AutonomyTier` and governance flags.
4. **`REQ-0104` (Hard Floors Against Destructive Operations)**:
   - `is_hard_floor_violation(command_or_target)` and `EarnedAutonomyGate.evaluate_action(...)` returning `HARD_FLOOR_BLOCKED` on destructive shell commands, secret access, force pushes, or mutations to `adversarial_tests/` regardless of permission mode.
5. **`REQ-0105` (Reviewer Circuit Breaker & Unattended Self-Approval Guard)**:
   - Trip `circuit_breaker_tripped = True` after `max_consecutive_denials` (`3`) denials, halting subsequent calls with `CIRCUIT_BREAKER_HALTED`, and block unallowlisted shell commands when `unattended=True` (`UNATTENDED_SELF_APPROVAL_DENIED`).
6. **`REQ-0106` (Provenance Audit Trail)**:
   - Record every decision in `gate.audit_log` with `provenance` in `{"auto-approved", "user-approved", "denied"}`.

---

## 4. Verification Command

```bash
./labs/lab_01_vibe_coding_and_earned_autonomy/self_diagnose.sh
```

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
