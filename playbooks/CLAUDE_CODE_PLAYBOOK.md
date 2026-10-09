# Claude Code Native Track Playbook (`claude` Branch)

This playbook documents how **Vibe-Coding-Course** runs natively in **Claude Code** on the `claude` branch using `CLAUDE.md` (`@docs/*.md` on-demand imports), git-worktree-shared Auto-Memory (`~/.claude/projects/<project>/memory/MEMORY.md`), `.claude/skills/`, `.claude/agents/`, `/feature-dev`, `eval-viewer`, and `.claude-plugin/plugin.json`.

---

## 1. Ownership & Harness Primitives

| Stage | Owner | Claude Code Interface |
| :--- | :--- | :--- |
| **Persistent project context** | Repo (`CLAUDE.md`) | `CLAUDE.md` ($\le 40$ lines) + on-demand `@docs/*.md` references + `.claude/rules/*.md` |
| **Cross-session auto-memory** | Claude Code | `~/.claude/projects/<project>/memory/MEMORY.md` (git-repo-scoped, shared across worktrees) + `/memory` |
| **Context hygiene audit** | Claude Code | `/context`, `/clear`, `/compact` (keep utilization in the 40%–60% sweet spot) |
| **Manual & auto skills** | `.claude/skills/` | `/anthropic-brand` (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) & `/harness-audit` |
| **Skill evaluation** | `skill-creator` | Paired `with_skill` vs `without_skill` $\to$ `grading.json` $\to$ `benchmark.json` $\to$ `eval-viewer/generate_review.py` |
| **7-phase multi-agent flow** | `.claude/agents/` | `/feature-dev` orchestrating `code-explorer`, `code-architect`, and `code-reviewer` ($\text{confidence} \ge 80$) |
| **Versioned plugin bundle** | `.claude-plugin/` | `.claude-plugin/plugin.json` + `.mcp.json` + `hooks/hooks.json` (`PreToolUse`) |
| **Read-only exploration** | Claude Code | `plan mode` |
| **Multi-phase execution** | Claude Code | `/feature-dev` |
| **Locked files** | Claude Code | `permissions.deny` rules in `.claude/settings.json` & `.claude/learner.settings.json` |
| **Deterministic pass/fail** | This repo | `labs/*/self_diagnose.sh`, `self_diagnose_all.sh` |

---

## 2. Learner Session Flow (`claude` Branch)

1. From the repository root on the `claude` branch, launch learner mode:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. **Explore in `plan mode`**: Run `/context` and `/memory`, inspect the lab's `starter/` files, and delegate read-only exploration to `code-explorer` subagents. Nothing is written during exploration.
3. **Human approval checkpoint**: Verify no files were modified during exploration before implementation begins:
   ```bash
   git status --short
   ```
4. **Start a new session for implementation and run `/feature-dev`**: In labs 03 through 06, start a clean session (or run `/clear`) and run the `/feature-dev` workflow defined in the lab's `## Claude Code Track` section.
5. **Run targetable self-diagnosis**:
   ```bash
   ./labs/<lab>/self_diagnose.sh work
   ```

---

## 3. What `TARGET_DIR` (`work/`) Must Contain Per Lab

| Lab | Read from `TARGET_DIR` (`work/`) | Always read from the lab |
| :--- | :--- | :--- |
| **`01`** | `domain_ledger.py`; `test_*.py` optional | `adversarial_tests/` |
| **`02`** | `context_memory_manager.py`; `test_*.py` optional | `adversarial_tests/` |
| **`03`** | `skill_validator.py`, `anthropic-brand/{SKILL.md,docs.md,slides-deck.md,apply_template.md}`; `test_*.py` optional | `adversarial_tests/` |
| **`04`** | `skill_eval_engine.py`; `test_*.py` optional | `starter/overloaded_skill_catalog.json`, `adversarial_tests/` |
| **`05`** | `feature_dev_orchestrator.py`, `agents/{code-explorer,code-architect,code-reviewer}.md`; `test_*.py` optional | `adversarial_tests/` |
| **`06`** | `harness_flywheel.py`, `vibe-engineering-plugin/`; `test_*.py` optional | `adversarial_tests/` |

---

## 4. Guarantees & Verification Authority

- **File-tool permission rules vs. OS sandboxing**: The `permissions.deny` rules in `.claude/settings.json` (`Edit(**/adversarial_tests/**)`) and `.claude/learner.settings.json` (`Read(**/expected_output/**)` and `Edit(**/adversarial_tests/**)`) guard Claude's file tools (`Read`, `Edit`, `Write`) and are **not** an OS-level sandbox against arbitrary shell commands.
- **Agent self-assessment vs. deterministic grading**: In Claude Code, conversational completion claims are never authoritative; the deterministic authority is always `./labs/<lab>/self_diagnose.sh`.
