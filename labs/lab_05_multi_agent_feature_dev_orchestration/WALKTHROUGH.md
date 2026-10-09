# Lab 05: Multi-Agent Collaboration (`feature-dev`: `code-explorer`, `code-architect`, `code-reviewer`)

## 1. Learning Objectives & Multi-Agent Architecture

Why does single-session vibe coding break down on multi-file features? Because noisy codebase searches, competing design alternatives, implementation diffs, and self-review push a single context window past the **60% context degradation wall**.

Anthropic's official **`feature-dev` plugin** (`plugins/feature-dev/README.md`) and Antigravity's **Subagent & Workflow Orchestration (`.agents/workflows/feature-dev.md`, `.agents/agents/*.md`, `/plan`)** solve this by decomposing feature development into **7 disciplined phases** powered by three context-isolated read-only subagent archetypes:

1. **Phase 1: Discovery** — Clarify the high-level goal and initialize the phase checklist.
2. **Phase 2: Codebase Exploration (`code-explorer` subagents)** — Spawn 2–3 parallel read-only `code-explorer` agents (`Glob`, `Grep`, `Read`) that trace entry points and call chains using exact `file:line` citations and return the top essential files to read.
3. **Phase 3: Clarifying Questions Gate (MANDATORY STOP)** — Surface all underspecified edge cases, integration boundaries, and failure modes discovered during Phase 2. **Never advance to Phase 4 Architecture until the human answers every Phase 3 question.**
4. **Phase 4: Architecture Design (`code-architect` subagents)** — Spawn parallel `code-architect` agents across three explicit lenses:
   - `minimal_changes` (smallest footprint, maximum reuse)
   - `clean_architecture` (maintainability & explicit abstractions)
   - `pragmatic_balance` (speed + production quality)
   Present the trade-offs and wait for explicit human approval.
5. **Phase 5: Implementation** — Implement the human-selected architecture slice by slice.
6. **Phase 6: Quality Review (`code-reviewer` subagents)** — Spawn 3 parallel `code-reviewer` agents auditing Simplicity/DRY, Functional Bugs, and `CLAUDE.md`/`GEMINI.md` Conventions, filtering out noise via a hard **`confidence >= 80`** threshold (`0–100` scale).
7. **Phase 7: Summary** — Record what was built, decisions made, and verification results.

---

## 2. Step-by-Step Implementation

1. Author the three subagent definitions in `agents/`:
   - `agents/code-explorer.md`
   - `agents/code-architect.md`
   - `agents/code-reviewer.md`
2. Implement `feature_dev_orchestrator.py` satisfying `REQ-0501` through `REQ-0506`:
   - `validate_subagent_definitions(agents_dir)`
   - `aggregate_explorer_findings(explorer_reports)`
   - `synthesize_architecture_options(proposals)`
   - `filter_review_findings(findings, min_confidence=80)`
   - `FeatureDevPipeline` enforcing `ClarificationGateError` (Phase 3 $\to$ 4) and `ArchitectureApprovalGateError` (Phase 4 $\to$ 5).

---

## 3. Verification Command

```bash
./labs/lab_05_multi_agent_feature_dev_orchestration/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. In `/plan` mode, inspect `starter/single_agent_rush.py` and invoke parallel `code-explorer` subagents (or `.agents/agents/{code-explorer,code-architect,code-reviewer}.md`) to map the 7-phase state machine.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and run the `/feature-dev` workflow to implement `work/feature_dev_orchestrator.py` and `work/agents/*.md` until `./labs/lab_05_multi_agent_feature_dev_orchestration/self_diagnose.sh work` exits `0` without modifying `adversarial_tests/` or `expected_output/`.
5. Run targetable self-diagnosis:
   ```bash
   ./labs/lab_05_multi_agent_feature_dev_orchestration/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `starter/single_agent_rush.py` and review `.claude/agents/{code-explorer,code-architect,code-reviewer}.md` and `/feature-dev`.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and invoke `/feature-dev`:
   ```text
   /feature-dev Implement labs/lab_05_multi_agent_feature_dev_orchestration/work/ until ./labs/lab_05_multi_agent_feature_dev_orchestration/self_diagnose.sh work exits 0; do not modify any file under adversarial_tests/ or expected_output/.
   ```
5. Run targetable self-diagnosis:
   ```bash
   ./labs/lab_05_multi_agent_feature_dev_orchestration/self_diagnose.sh work
   ```
