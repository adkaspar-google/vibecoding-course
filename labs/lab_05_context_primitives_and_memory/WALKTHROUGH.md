# Lab 05 Walkthrough: Harness Engineering Layer 1 — The Three Context Primitives, 60-Line Map & Persistent Memory (`TaskFlow` Standing Context & Memory Compiler)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 04 $\to$ Lab 05)
In **Lab 04**, we kept individual `TaskFlow` coding sessions inside the **$\le 40\%$ Smart Zone** by applying output-redirection backpressure (`> run.log 2>&1`) and **Frequent Intentional Compaction (`RPI`: `research.md` + `plan.md`)**. However, `research.md` and `plan.md` are ephemeral task artifacts. How do we architect **Harness Engineering Layer 1** ($\text{Agent} = \text{Model} + \text{Harness}$) so durable `TaskFlow` project conventions (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) and cross-session memory (`MEMORY.md`, `KNOWLEDGE.md`) persist across hundreds of sessions without triggering the **150-Instruction Compliance Cliff**?

### The Headache (Monolithic 250-Rule Instruction Dumps & Unverified Memory Poisoning)
When a team maintains `TaskFlow`'s project context using [`starter/monolithic_claude_md_dump.py`](./starter/monolithic_claude_md_dump.py):
- **The 150-Instruction Compliance Cliff:** Dumping 250 inline rules into a single monolithic `CLAUDE.md` or `GEMINI.md` file causes LLM instruction compliance to plummet across *all* rules (including critical `TaskFlow` integer-cent billing invariants).
- **Fake `#direct` Provenance Poisoning:** Allowing an agent to tag its own speculative codebase guesses with `#direct` permanently elevates transient hypotheses to the same authority as explicit human architecture directives.
- **Unbounded Memory Growth & Stale Commits:** Appending raw session observations past 200 lines without pruning entries tied to superseded Git commits pollutes startup context with obsolete `TaskFlow` schema facts.

### The Everyday Metaphor (`Known -> Target`)
Think of **The 60-Line Root Context Map & Provenance-Tagged Memory** like **an emergency cockpit quick-reference laminated card vs. a 500-page aircraft maintenance binder** (*Known* $\to$ *Target*). If you tape all 500 pages onto the windshield (*monolithic 250-rule `CLAUDE.md`*), the pilot cannot see the runway; instead, the laminated card holds only the **$\le 60$-line essential checklist and tab pointers** (`@docs/architecture.md`, `@docs/testing-conventions.md`) that open the exact binder section on demand.

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/monolithic_claude_md_dump.py`
Open [`starter/monolithic_claude_md_dump.py`](./starter/monolithic_claude_md_dump.py) (`lines 20–22`). Notice how `generate_bloated_claude_md()` emits 250 inline rules in a single string (`>150` cliff threshold) with zero `@docs/*.md` lazy references or scoped rule frontmatter.

### Implementing `context_compiler.py` (`REQ-0501` through `REQ-0506`)
Implement [`expected_output/context_compiler.py`](./expected_output/context_compiler.py) (or your custom `work/context_compiler.py`) to satisfy all 6 requirements for `TaskFlow`'s Layer-1 context and memory compiler:

1. **`REQ-0501` (Three Context Primitives Classifier)**:
   - Implement `ContextPrimitive` (`PROMPT_OR_SLASH_COMMAND`, `STANDING_RULE`, `LAZY_LOADED_SKILL`) and `classify_context_primitive(is_per_turn_intent, is_multi_step_procedure, applies_every_session)`.
2. **`REQ-0502` (150-Instruction Compliance Cliff Auditor & 60-Line Root Map Compiler)**:
   - Implement `audit_instruction_compliance_budget(instruction_count, cliff_threshold=150)` and `compile_root_context_map(project_name, commands, architecture_items, on_demand_docs, max_lines=60)` enforcing $\le 60$ lines and `@docs/*.md` lazy references.
3. **`REQ-0503` (Dual-Harness Path-Scoped Rule Validator)**:
   - Implement `validate_scoped_rule(frontmatter, body)` validating both Antigravity `.agents/rules/*.md` (`trigger: always_on | model_decision | glob | manual`, requiring `globs` when `trigger == "glob"`) and Claude Code `.claude/rules/*.md` (`paths: [...]`).
4. **`REQ-0504` (Provenance-Tagged Memory Formatter)**:
   - Implement `MemoryEntry` and `format_memory_entry(entry)` reserving `#direct` strictly for `is_explicit_user_directive=True` and requiring at least one relativity tag (`#commit:<sha>`, `#time:<YYYY-MM-DD>`, or `#session:<id>`) on indirect agent observations.
5. **`REQ-0505` (200-Line Startup Memory Cap & Stale Commit Pruner)**:
   - Implement `prune_and_cap_memory(entries, superseded_commits, max_lines=200)` pruning indirect observations whose `commit_sha` is in `superseded_commits` (while preserving `#direct` user directives) and splitting lines beyond `max_lines=200` into `overflow_topic_lines`.
6. **`REQ-0506` (Worktree-Shared Memory Path Resolver)**:
   - Implement `resolve_project_memory_paths(project_slug)` returning canonical memory paths for `claude` (`~/.claude/projects/<slug>/memory/MEMORY.md`) and `agy` (`~/.gemini/antigravity/knowledge/<slug>/KNOWLEDGE.md`).

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_05_context_primitives_and_memory/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_05_context_primitives_and_memory/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"Every time the coding agent discovers a useful fact about `TaskFlow`'s codebase, it should append that fact to `CLAUDE.md` / `GEMINI.md` or tag it with `#direct` in memory so future sessions never forget it."*
>
> **✓ Reality:** Appending every observation to root context files rapidly pushes the harness over the **150-instruction compliance cliff** and >60-line budget. Worse, tagging agent-inferred codebase observations with `#direct` prevents automatic pruning when a commit is superseded. Only explicit human statements earn `#direct`; codebase observations belong in `MEMORY.md` / `KNOWLEDGE.md` anchored with `#commit:<sha>` so stale facts are pruned automatically when code evolves.

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Predict-the-Outcome`):** Suppose `prune_and_cap_memory(entries, superseded_commits={"old111"}, max_lines=200)` is called with two entries that both reference `commit_sha="old111"`:
1. `MemoryEntry("SettlementBatch uses legacy v1 table", is_explicit_user_directive=False, commit_sha="old111")`
2. `MemoryEntry("Never use float for TaskFlow currency", is_explicit_user_directive=True, commit_sha="old111")`

Which of these two entries is pruned, which survives into `active_lines`, and why?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect the `if` condition inside the `for entry in entries:` loop of `prune_and_cap_memory()` in [`expected_output/context_compiler.py`](./expected_output/context_compiler.py) (`lines 195–199`).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Evaluate `entry.commit_sha and entry.commit_sha in stale_set and not entry.is_explicit_user_directive` for Entry 1 (`is_explicit_user_directive=False`) and Entry 2 (`is_explicit_user_directive=True`).
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
**Entry 1 is pruned** (`pruned_stale_count = 1`) because it is an indirect codebase observation (`is_explicit_user_directive=False`) anchored to superseded commit `"old111"`. **Entry 2 survives** in `active_lines` (`"- Never use float for TaskFlow currency #direct #commit:old111"`) because explicit user directives (`#direct`) represent durable human policy that outlives individual code commits.
</details>

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
