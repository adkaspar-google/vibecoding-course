# Lab 03: Directing the Daily Workflow (`Research -> Propose -> Plan -> Implement -> Verify`) & Reflection

## 1. Learning Objectives & Conceptual Motivation

1. **Task Complexity vs. Workflow Rigor Spectrum (Stanford CS146S Lecture 3 & Skills Map 3.1)**:
   Not every task needs the same ceremony. High-velocity engineers match workflow rigor to task complexity:
   - **Copy/typo tweak (`1` file, zero ambiguity)** $\to$ `VANILLA_PROMPT`
   - **Small multi-file bugfix (`2–3` files, clear design)** $\to$ `SINGLE_PLAN_MODE` (`/plan` or `Shift+Tab`)
   - **Medium feature (`3–8` files or architectural choice)** $\to$ **`REPPIT_WORKFLOW` (`Research -> Propose -> Plan -> Implement -> Test/Verify`)**
   - **Large multi-module migration (`>8` files / cross-service)** $\to$ `MULTI_SESSION_SUBAGENTS`

2. **The 5-Step `RePPIT` Daily Workflow (`themodernsoftware.dev` Lecture 3)**:
   - **Step 1 — Research (`research_codebase`)**: Strictly documents *what exists today* with exact `file.py:L10` citations—explicitly forbidden from proposing solutions—to build both the agent's compressed context and the human's mental model, paired with Socratic requirement interviewing (`/grill-me` in Antigravity or Plan Mode questioning in Claude Code).
   - **Step 2 — Propose (Orthogonal Proposals + Post-Proposal Context Reset)**: Force the agent to generate **2 orthogonal architectural proposals** (e.g., `server_side_idempotency_store` vs. `client_signed_stateless_token`) with explicit trade-offs. **Crucial Context Hygiene Rule:** *Once the engineer selects Proposal A, immediately purge Proposal B from the active context window so rejected tokens never confuse implementation.*
   - **Step 3 — Plan (`Implementation Plan` Artifact)**: Produce a file-and-line-targeted plan with a mandatory **`## Out of Scope / Do NOT Touch`** guardrail section to block scope creep.
   - **Step 4 — Implement with Phase-Based Model Routing**: Use a **frontier reasoning model** (`gemini-3.1-pro` / `claude-opus-4-6`) for *Research, Propose, and Plan*, then route *Implement and Verify* to a **fast, cost-efficient model** (`gemini-3-flash` / `claude-sonnet-4-6`) once the design is locked.
   - **Step 5 — Verify, Reflect & Commit (`andrewyng/translation-agent` + `Walkthrough` Artifact)**: Run `Generate -> Reflect -> Refine` self-critique, execute unit tests + `/browser` visual verification, and emit a verified `walkthrough.md` Run Receipt.

---

## 2. Inspecting the Flawed Baseline (`starter/impulsive_feature_coder.py`)

Inspect `starter/impulsive_feature_coder.py`. Notice three daily workflow anti-patterns:
- **Silent Assumption Syndrome**: Jumps straight from an ambiguous feature prompt into mutating files without running `Research` or `/grill-me` clarification.
- **Rejected Proposal Context Pollution**: Leaves 3,000 tokens of rejected architectural discussion inside the active chat history during code generation, causing the model to mix both designs.
- **Scope Creep**: Modifies unrelated files because the plan lacked an explicit `Out of Scope / Do NOT Touch` boundary.

---

## 3. Step-by-Step Implementation (`reppit_orchestrator.py`)

Implement `reppit_orchestrator.py` satisfying `REQ-0301` through `REQ-0306`:
1. **`REQ-0301` (Task Complexity vs. Workflow Rigor Classifier)**:
   - `WorkflowRigor` (`VANILLA_PROMPT`, `SINGLE_PLAN_MODE`, `REPPIT_WORKFLOW`, `MULTI_SESSION_SUBAGENTS`) and `classify_workflow_rigor(files_touched, has_architectural_ambiguity, is_cross_service_migration)`.
2. **`REQ-0302` (Read-Only Research Document Validator & Socratic `/grill-me` Gate)**:
   - `validate_research_document(text)` requiring `file:L<line>` citations and rejecting premature solution proposals; `evaluate_clarification_gate(unresolved_questions)` blocking progression until all questions are resolved.
3. **`REQ-0303` (Orthogonal Proposal Validator & Post-Proposal Context Reset)**:
   - `ArchitecturalProposal`, `validate_orthogonal_proposals(prop_a, prop_b)`, and `select_proposal_and_reset_context(messages, prop_a, prop_b, selected_id)` purging the rejected proposal from context.
4. **`REQ-0304` (Plan Guardrail Validator with `Out of Scope / Do NOT Touch`)**:
   - `validate_implementation_plan(plan_md)` requiring file/line targets, verification commands, and an explicit `Out of Scope / Do NOT Touch` section.
5. **`REQ-0305` (Phase-Based Model Router)**:
   - `route_model_for_reppit_phase(phase, harness)` routing `RESEARCH`, `PROPOSE`, `PLAN` to frontier reasoning models and `IMPLEMENT`, `TEST_VERIFY` to fast execution models.
6. **`REQ-0306` (`Generate -> Reflect -> Refine` & `Walkthrough` Run Receipt Validator)**:
   - `run_reflection_cycle(draft_code, checklist)` and `validate_walkthrough_receipt(receipt, do_not_touch_files)`.

---

## 4. Verification Command

```bash
./labs/lab_03_reppit_workflow_and_reflection/self_diagnose.sh
```

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
