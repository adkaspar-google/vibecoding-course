# Antigravity Native Track Playbook (`agy` Branch)

This playbook documents how **Vibe-Coding-Course** runs natively in **Google Antigravity / Gemini CLI** on the `agy` branch using `GEMINI.md` & `AGENTS.md` (`@docs/*.md` on-demand references), the Antigravity Knowledge Base (`~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` with `#direct` provenance tags), `.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/workflows/`, and `.agents/plugins/vibe-engineering-kit/`.

---

## 1. Ownership & Harness Primitives

| Stage | Owner | Antigravity Interface |
| :--- | :--- | :--- |
| **Persistent project context** | Repo (`GEMINI.md` / `AGENTS.md`) | `GEMINI.md` & `AGENTS.md` ($\le 40$ lines) + `@docs/*.md` references + `.agents/rules/*.md` (`trigger: always_on \| model_decision`) |
| **Cross-session memory** | Antigravity Knowledge Base | `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md`, `topics/*.md`, `#direct`/`#commit`/`#time`/`#session` tags, `/memory` |
| **Context hygiene audit** | Antigravity / Gemini CLI | `/stats`, `/memory` (`show \| add \| refresh`), `/skills`, `/clear`, `/compress` |
| **Manual & auto skills** | `.agents/skills/` | `/anthropic-brand` (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) & `/harness-audit` |
| **Skill evaluation & SDT** | `skill-creator` | Paired `with_skill` vs `without_skill` ablation, `eval-viewer`, Signal Detection Theory (`d'`, criterion `c`, utility `U`) |
| **7-phase multi-agent flow** | `.agents/agents/` & `.agents/workflows/` | `code-explorer`, `code-architect`, and `code-reviewer` ($\text{confidence} \ge 80$) via `/feature-dev` and `/plan` |
| **Versioned plugin bundle** | `.agents/plugins/` | `.agents/plugins/vibe-engineering-kit/{plugin.json,mcp_config.json,hooks.json}` |
| **Read-only exploration** | Antigravity | `/plan` mode |
| **Locked files** | Antigravity + OS | `chmod -w` + `PreToolUse` hook blocking mutations to `adversarial_tests/` |
| **Deterministic pass/fail** | This repo | `labs/*/self_diagnose.sh`, `self_diagnose_all.sh` |

---

## 2. Learner Session Flow (`agy` Branch)

1. From the repository root on the `agy` branch, launch Antigravity:
   ```bash
   agy --workspace .
   ```
2. **Explore in `/plan` mode**: Run `/stats` and `/memory show` to inspect startup context token usage, inspect the lab's `starter/` files, and launch read-only `code-explorer` subagents. Nothing is written during exploration.
3. **Human approval checkpoint**: Verify no files were modified during exploration before implementation begins:
   ```bash
   git status --short
   ```
4. **Start a clean session for implementation**: In labs 03 through 06, start a clean session (or run `/clear`) and execute the step-by-step workflow in the lab's `## Antigravity Track` section until `./labs/<lab>/self_diagnose.sh work` exits `0`.
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

- **Hook guardrails & read-only permissions**: `adversarial_tests/` is protected both by `chmod -w` and by the `PreToolUse` command hook in `hooks.json`.
- **Deterministic authority**: The deterministic authority for pass/fail grading is always `./labs/<lab>/self_diagnose.sh` (and `./self_diagnose_all.sh` in CI).
