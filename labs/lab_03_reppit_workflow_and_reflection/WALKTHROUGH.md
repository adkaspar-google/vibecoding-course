# Lab 03 Walkthrough: Directing the Daily Workflow (`Research -> Propose -> Plan -> Implement -> Verify`) & Reflection (`TaskFlow` Feature Delivery)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 02 $\to$ Lab 03)
In **Lab 02**, we inspected the **3-Layer Agent Stack** on the wire for the **`TaskFlow` Productivity & Workspace Platform**, consolidating 150 bloated CRUD tool schemas into 5 **Swiss Army Knife primitives** (`Bash`, `Read`, `Edit`, `Grep`, `LSP`) and enforcing the 3-phase **Core Agentic Loop (`Gather Context -> Take Action -> Verify Results`)**. Now that each individual turn is lean and verified on the wire, how should an engineer orchestrate a **multi-file `TaskFlow` feature** across an entire daily coding session without the agent guessing architecture or polluting its own context window?

### The Headache (Impulsive Coding, Rejected Proposal Pollution & Scope Creep)
When a developer uses [`starter/impulsive_feature_coder.py`](./starter/impulsive_feature_coder.py) to build a multi-file `TaskFlow` idempotent invoice settlement feature in a single unstructured chat session:
- **Silent Assumption Syndrome:** The agent jumps straight from a vague feature request into mutating files without first documenting *what exists today* (`file.py:L10` citations) or asking Socratic clarification questions (`/grill-me` / Plan Mode).
- **Rejected Proposal Context Pollution:** After the agent brainstorms two competing designs (*Option A: Server-Side SQLite Idempotency Store* vs. *Option B: Client-Signed Stateless HMAC Token*) and the engineer selects Option A, leaving Option B's 3,000 tokens in the chat history causes the model to accidentally blend stateless HMAC logic into the SQLite implementation.
- **Unbounded Scope Creep:** Because the implementation plan lacked an explicit **`## Out of Scope / Do NOT Touch`** boundary, the agent "helpfully" refactors `legacy/auth.py` and breaks unrelated `TaskFlow` login flows.

### The Everyday Metaphor (`Known -> Target`)
Think of **The 5-Step `RePPIT` Workflow & Post-Proposal Context Reset** like **an architect designing a bridge renovation** (*Known* $\to$ *Target*). First you survey the existing piers with exact measurements (*Read-Only Research*), then you sketch two genuinely different bridge designs (*Orthogonal Proposals*). **Crucially, once the city approves the suspension bridge, you take the rejected truss-bridge blueprints off the drafting table before handing the final plan to the construction crew** (*Post-Proposal Context Reset*), and you put yellow caution tape around historic buildings the crew must not touch (*`Out of Scope / Do NOT Touch`*).

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/impulsive_feature_coder.py`
Open [`starter/impulsive_feature_coder.py`](./starter/impulsive_feature_coder.py) (`lines 20–27`). Notice how `impulsive_implement()` concatenates both `proposal_a` and `proposal_b` into `combined_context`, modifies `legacy_billing.py` without an out-of-scope guardrail, and marks `"verified": "assumed_working"`.

### Implementing `reppit_orchestrator.py` (`REQ-0301` through `REQ-0306`)
Implement [`expected_output/reppit_orchestrator.py`](./expected_output/reppit_orchestrator.py) (or your custom `work/reppit_orchestrator.py`) to satisfy all 6 requirements for `TaskFlow`'s daily feature delivery workflow:

1. **`REQ-0301` (Task Complexity vs. Workflow Rigor Classifier)**:
   - Implement `WorkflowRigor` (`VANILLA_PROMPT`, `SINGLE_PLAN_MODE`, `REPPIT_WORKFLOW`, `MULTI_SESSION_SUBAGENTS`) and `classify_workflow_rigor(files_touched, has_architectural_ambiguity, is_cross_service_migration)`.
2. **`REQ-0302` (Read-Only Research Validator & Socratic `/grill-me` Gate)**:
   - Implement `validate_research_document(research_markdown)` requiring exact `file:L<line>` citations and rejecting premature solution proposals (`"we should refactor"`, `"i propose we rewrite"`, etc.), plus `evaluate_clarification_gate(unresolved_questions)` blocking progression until all Socratic questions are answered.
3. **`REQ-0303` (Orthogonal Proposal Validator & Post-Proposal Context Reset)**:
   - Implement `ArchitecturalProposal`, `validate_orthogonal_proposals(prop_a, prop_b)` enforcing distinct `mechanism_axis` values and explicit `tradeoffs`, and `select_proposal_and_reset_context(research_summary, prop_a, prop_b, selected_id)` purging the rejected proposal's tokens from `compacted_messages`.
4. **`REQ-0304` (Plan Guardrail Validator with `Out of Scope / Do NOT Touch`)**:
   - Implement `validate_implementation_plan(plan_markdown)` requiring `file:line` targets, a deterministic verification command, and an explicit `Out of Scope / Do NOT Touch` section.
5. **`REQ-0305` (Phase-Based Model Router)**:
   - Implement `route_model_for_reppit_phase(phase, harness)` routing `RESEARCH`, `PROPOSE`, and `PLAN` to `frontier_reasoning` models (`gemini-3.1-pro` / `claude-opus-4-6`) and `IMPLEMENT` and `TEST_VERIFY` to `fast_execution` models (`gemini-3-flash` / `claude-sonnet-4-6`).
6. **`REQ-0306` (`Generate -> Reflect -> Refine` & `Walkthrough` Run Receipt Validator)**:
   - Implement `run_reflection_cycle(draft_code)` (`andrewyng/translation-agent` self-critique pattern) and `validate_walkthrough_receipt(receipt, do_not_touch_files)` verifying exit code `0`, behavioral evidence, and zero modifications to `do_not_touch_files`.

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_03_reppit_workflow_and_reflection/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_03_reppit_workflow_and_reflection/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"During Step 1 (`Research`), a good coding agent should go ahead and recommend how to refactor `TaskFlow`'s code so we save a step."*
>
> **✓ Reality:** Mixing **Research (*what exists today*)** with **Proposal (*how to change it*)** causes premature architectural lock-in before the agent has mapped all callers and invariants. In Stanford CS146S's `RePPIT` workflow, `Research` is strictly read-only and factual (`file.py:L42` citations only), and after Step 2 (`Propose`), the rejected proposal MUST be purged from the context window so its tokens never contaminate Step 4 (`Implement`).

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Spot-the-Flaw`):** An engineer asks the agent for two architectural proposals (`prop_a` and `prop_b`) to handle concurrent `TaskFlow` workspace task updates:
- `prop_a`: `proposal_id="P1"`, `title="Postgres Row Lock"`, `mechanism_axis="database_pessimistic_lock"`, `tradeoffs=("No retries", "Higher lock wait")`
- `prop_b`: `proposal_id="P2"`, `title="SQLite Row Lock"`, `mechanism_axis="database_pessimistic_lock"`, `tradeoffs=("Simple setup", "Table-level writer contention")`

Why does `validate_orthogonal_proposals(prop_a, prop_b)` reject this pair even though `proposal_id`, `title`, and `tradeoffs` are all different?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect how `mechanism_axis` is compared in `validate_orthogonal_proposals()` inside [`expected_output/reppit_orchestrator.py`](./expected_output/reppit_orchestrator.py) (`lines 114–129`).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Compare `prop_a.mechanism_axis.strip().lower()` (`"database_pessimistic_lock"`) against `prop_b.mechanism_axis.strip().lower()` (`"database_pessimistic_lock"`). Are these two proposals exploring genuinely different concurrency mechanisms, or just two minor variations of pessimistic locking?
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
Both proposals share the exact same `mechanism_axis="database_pessimistic_lock"`. In Step 2 of `RePPIT`, proposals must be **genuinely orthogonal** across architectural axes (e.g., `database_pessimistic_lock` vs. `optimistic_concurrency_version`) so the engineer compares real design trade-offs rather than superficial variations of the same idea.
</details>

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Use `/grill-me` and `/plan` to inspect `starter/impulsive_feature_coder.py` and draft an `Implementation Plan` Artifact with an `Out of Scope / Do NOT Touch` section.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_03_reppit_workflow_and_reflection/work/reppit_orchestrator.py` and `test_reppit_orchestrator.py`, then run:
   ```bash
   ./labs/lab_03_reppit_workflow_and_reflection/self_diagnose.sh work
   ```
