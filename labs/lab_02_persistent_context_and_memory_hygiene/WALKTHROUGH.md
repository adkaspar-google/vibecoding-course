# Lab 02: Persistent Project Context (`CLAUDE.md` / `GEMINI.md`), On-Demand `@path` Imports & Cross-Session Auto-Memory

## 1. Learning Objectives & Architectural Grounding

Every coding agent session begins with a **fresh context window**. Two distinct mechanisms carry knowledge across sessions:
1. **Human-Authored Persistent Project Context (`CLAUDE.md` on `claude` / `GEMINI.md` & `AGENTS.md` on `agy`)**:
   - Captures project onboarding info, directory structure, architectural invariants, and exact verification commands.
   - Uses **on-demand `@path/to/file.md` references** (e.g., `@docs/architecture.md`, `@docs/testing-conventions.md`) so detailed reference documents are pulled only when relevant—saving startup tokens just like progressive disclosure in skills.
2. **Agent-Authored Cross-Session Auto-Memory (`~/.claude/projects/<project>/memory/MEMORY.md` on `claude` / `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` on `agy`)**:
   - In **Claude Code**, each project gets its own memory directory at `~/.claude/projects/<project>/memory/` derived from the **git repository root**, so all git worktrees and subdirectories share one auto-memory store (falling back to the project root outside git). Only the first **200 lines / 25 KB** of `MEMORY.md` load at startup; detailed notes belong in linked `topics/*.md` files.
   - In **Antigravity (`agy`)**, project Knowledge Items live under `~/.gemini/antigravity/knowledge/<project>/` (`KNOWLEDGE.md` + `artifacts/*.md`), and factual claims carry epistemic provenance tags (`#direct` strictly for explicit user instructions, `#commit:<sha>`, `#time:<YYYY-MM-DD>`, `#session:<id>`).
3. **Context Inspection (`/context` & `/memory`)**:
   - Because $\text{Output} = f(\text{Context})$, exceeding **60% context utilization** triggers attention dilution and reasoning degradation (`CONTEXT_POLLUTION_WARNING`).

---

## 2. Step-by-Step Implementation (`context_memory_manager.py`)

Implement `context_memory_manager.py` satisfying `REQ-0201` through `REQ-0206`:
1. **`REQ-0201` (`validate_root_context_md`)**: Enforce `max_lines`, verify the 4 core onboarding headings (`Commands & Environment`, `Architecture & Directory Map`, `Core Conventions`, `On-Demand References`), and extract `@path/to/file.md` references.
2. **`REQ-0202` (`resolve_project_memory_dir`)**: Resolve `~/.claude/projects/<project>/memory` (or `~/.gemini/antigravity/knowledge/<repo>` on `agy`) from `git_repo_root` so all worktrees and subdirectories map to the exact same directory.
3. **`REQ-0203` (`compile_auto_memory`)**: Enforce the 200-line / 25 KB limit on `MEMORY.md` / `KNOWLEDGE.md`, routing overflow and topic-scoped notes into `topics/<slug>.md`.
4. **`REQ-0204` (`format_memory_entry`)**: Attach `#direct` **strictly** when `source_type == "user_explicit"`, never on agent-inferred observations.
5. **`REQ-0205` (`simulate_context_command`)**: Compute token utilization, progressive `@path` token savings, and flag `CONTEXT_POLLUTION_WARNING` above `0.60`.

---

## 3. Verification Command

```bash
./labs/lab_02_persistent_context_and_memory_hygiene/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Run `/stats` and `/memory show` to inspect startup context token usage across `System prompt`, `Rules`, `Skills`, and `Free space`, and inspect `starter/BLOATED_CONTEXT.md` in `/plan` mode.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_02_persistent_context_and_memory_hygiene/work/context_memory_manager.py` and `test_context_memory_manager.py` (using `/memory refresh` to reload context rules), then run:
   ```bash
   ./labs/lab_02_persistent_context_and_memory_hygiene/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, run `/context` and `/memory` to inspect startup token usage and the git-repo-scoped auto-memory path, and inspect `starter/BLOATED_CONTEXT.md` using subagents.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_02_persistent_context_and_memory_hygiene/work/context_memory_manager.py` and `test_context_memory_manager.py`, then verify:
   ```bash
   ./labs/lab_02_persistent_context_and_memory_hygiene/self_diagnose.sh work
   ```
