# Lab 05: Harness Engineering Layer 1 — The Three Context Primitives, 60-Line Map & Persistent Memory

## 1. Learning Objectives & Conceptual Motivation

1. **The Harness Equation & The Three Context Primitives (`martinfowler.com` & Skills Map 3.4)**:
   $$\text{Agent} = \text{Model} + \text{Harness}$$
   A production harness separates context into three distinct primitives based on activation frequency and token weight:
   - **Prompts & Slash Commands (`PROMPT_OR_SLASH_COMMAND`)**: Ephemeral, per-turn task intent (`/plan`, `/grill-me`, `/feature-dev`).
   - **Standing Rules (`STANDING_RULE`)**: Always-on or path-glob-scoped invariants (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`, `.claude/rules/*.md`).
   - **Lazy-Loaded Skills (`LAZY_LOADED_SKILL`)**: Multi-step procedural manuals (`SKILL.md`) whose body tokens load **only** when triggered.

2. **The 150-Instruction Compliance Cliff & The Minimalist 60-Line Map Rule (OpenAI & Stanford CS146S)**:
   Instruction-following studies show that once a prompt accumulates **>150 simultaneous rules**, model compliance drops sharply across *all* rules. Rather than stuffing 500 lines of prose into `CLAUDE.md` or `GEMINI.md`, treat root context files as a **$\le 60$-line table of contents** containing:
   - Exact build, test, and linter commands (`CI=true ./self_diagnose_all.sh`)
   - High-level directory map
   - Lazy `@docs/*.md` pointers (`@docs/architecture.md`, `@docs/testing-conventions.md`, `@docs/language-and-code-foundations.md`, `@docs/skillsbench-and-harness-guide.md`) loaded on demand.

3. **Cross-Session Memory (`MEMORY.md` & `KNOWLEDGE.md`) with Provenance Hygiene**:
   - **Claude Code Auto-Memory**: `~/.claude/projects/<project>/memory/MEMORY.md` (shared across `git worktree` checkouts, capped at 200 lines at startup).
   - **Google Antigravity Knowledge Base**: `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` (`/memory show|add|refresh`).
   - **Provenance Tagging Discipline**: Reserve `#direct` **strictly** for explicit user instructions; tag agent-observed codebase facts with `#commit:<sha>`, `#time:<YYYY-MM-DD>`, and `#session:<id>`, and prune stale entries when commits are superseded.

---

## 2. Inspecting the Flawed Baseline (`starter/monolithic_claude_md_dump.py`)

Inspect `starter/monolithic_claude_md_dump.py`. Notice three Layer-1 harness anti-patterns:
- **Monolithic 400-Line `CLAUDE.md`**: Dumps 220 conflicting rules into a single root file with zero `@docs/*.md` lazy imports.
- **Fake `#direct` Tagging**: Labels speculative agent guesses with `#direct`, permanently poisoning future sessions.
- **Unbounded `MEMORY.md` Growth**: Appends raw session logs past 500 lines without pruning superseded commits.

---

## 3. Step-by-Step Implementation (`context_compiler.py`)

Implement `context_compiler.py` satisfying `REQ-0501` through `REQ-0506`:
1. **`REQ-0501` (Three Context Primitives Classifier)**:
   - `ContextPrimitive` (`PROMPT_OR_SLASH_COMMAND`, `STANDING_RULE`, `LAZY_LOADED_SKILL`) and `classify_context_primitive(is_per_turn_intent, is_multi_step_procedure, applies_every_session)`.
2. **`REQ-0502` (150-Instruction Cliff Auditor & 60-Line Root Map Compiler)**:
   - `audit_instruction_compliance_budget(instruction_count, cliff_threshold=150)` and `compile_root_context_map(project_name, commands, architecture_items, on_demand_docs, max_lines=60)`.
3. **`REQ-0503` (Dual-Harness Scoped Rule Validator)**:
   - `validate_scoped_rule(frontmatter, body)` supporting `.agents/rules/*.md` (`trigger: always_on | model_decision | glob | manual`) and `.claude/rules/*.md` (`paths: [...]`).
4. **`REQ-0504` (Provenance-Tagged Memory Formatter)**:
   - `MemoryEntry` and `format_memory_entry(entry)` enforcing `#direct` strictly for explicit user directives and `#commit`/`#time`/`#session` for indirect observations.
5. **`REQ-0505` (200-Line Startup Cap & Stale Commit Pruner)**:
   - `prune_and_cap_memory(entries, superseded_commits, max_lines=200)`.
6. **`REQ-0506` (Worktree-Shared Memory Path Resolver)**:
   - `resolve_project_memory_paths(project_slug)` returning canonical `claude` and `agy` memory paths.

---

## 4. Verification Command

```bash
./labs/lab_05_context_primitives_and_memory/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `GEMINI.md`, `AGENTS.md`, and `.agents/rules/` alongside `starter/monolithic_claude_md_dump.py` in `/plan` mode, and check `/memory show`.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_05_context_primitives_and_memory/work/context_compiler.py` and `test_context_compiler.py`, then run:
   ```bash
   ./labs/lab_05_context_primitives_and_memory/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `CLAUDE.md` and `.claude/rules/` alongside `starter/monolithic_claude_md_dump.py`, and run `/memory` to view active memory files.
3. Verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_05_context_primitives_and_memory/work/context_compiler.py` and `test_context_compiler.py`, then verify:
   ```bash
   ./labs/lab_05_context_primitives_and_memory/self_diagnose.sh work
   ```
