# Antigravity Native Track Playbook (`agy` Branch)

This playbook documents how **Vibe-Coding-Course** runs natively in **Google Antigravity (`agy` CLI & Antigravity 2.0 IDE / Mission Control)** across **Phase 1 (Vibe Coding Foundations & Daily Workflows)** and **Phase 2 (Harness Engineering & Agentic Engineering Loops)**.

---

## 1. Ownership & Harness Primitives (`agy` Track)

| Stage | Owner | Antigravity Interface |
| :--- | :--- | :--- |
| **1. Permission Modes & Earned Autonomy** | `~/.gemini/antigravity-cli/settings.json` | `strict`, `request-review`, `proceed-in-sandbox`, `always-proceed` + `/config` & `!` Shell Mode |
| **2. Daily `RePPIT` & `RPI` Workflow** | Antigravity 2.0 Artifacts & Slash Commands | `/grill-me` (Socratic IoC), `/plan` (`Implementation Plan` Artifact), `/artifact`, `/browser` (`Walkthrough` Artifact), `/goal`, `/schedule` |
| **3. Context Window Physics & Compaction** | Antigravity / Gemini CLI | `/stats` (keep in `<= 40%` Smart Zone), `/compress`, `/clear`, `> run.log 2>&1` backpressure |
| **4. Persistent Project Context** | Repo (`GEMINI.md` / `AGENTS.md`) | `GEMINI.md` & `AGENTS.md` ($\le 45$ lines) + `@docs/*.md` lazy imports + `.agents/rules/*.md` (`trigger: always_on \| model_decision \| glob \| manual`) |
| **5. Cross-Session Knowledge Base** | Antigravity Knowledge Items | `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` with `#direct` vs. `#commit`/`#time`/`#session` provenance via `/memory` (`show \| add \| refresh`) |
| **6. Progressive-Disclosure Skills (`agentskills.io`)** | `.agents/skills/` | `/context-hub-docs` (`chub` grounding & annotations), `/reppit-workflow`, `/architecture-guard`, `/harness-audit`, `/skills` |
| **7. Context-Firewall Subagents & Council** | `.agents/agents/` & `.agents/workflows/` | Read-only `code-explorer`, `code-architect`, and `code-reviewer` ($\text{confidence} \ge 80$) via `/feature-dev` & Agent Manager worktrees |
| **8. Versioned Plugins, Hooks & Ratchets** | `.agents/plugins/` | `.agents/plugins/vibe-engineering-kit/{plugin.json,mcp_config.json,hooks.json}` (`PreToolUse` Exit Code `2`) |

---

## 2. Learner Session Flow (`agy` Branch)

1. From the repository root on the `agy` branch, launch Antigravity:
   ```bash
   agy --workspace .
   ```
2. **Explore in `/plan` mode (`<= 40%` Smart Zone)**: Run `/stats` and `/memory show` to inspect startup context token usage, use `/grill-me` to clarify requirements, inspect the lab's `starter/` files, and delegate broad searches to read-only `code-explorer` subagents.
3. **Human approval checkpoint**: Verify no files were modified during exploration before implementation begins:
   ```bash
   git status --short
   ```
4. **Reset context after proposal selection**: Once an architectural proposal and `Implementation Plan` Artifact (including `Out of Scope / Do NOT Touch`) are approved, run `/clear` (or `/compress`) so rejected proposal tokens do not pollute implementation.
5. **Implement & run targetable self-diagnosis**:
   ```bash
   ./labs/<lab>/self_diagnose.sh work
   ```

---

## 3. What `TARGET_DIR` (`work/`) Must Contain Per Lab

| Lab | Phase | Deliverable in `TARGET_DIR` (`work/`) | Immutable Verifier |
| :--- | :--- | :--- | :--- |
| **`01`** | Phase 1 | `prompt_steerer.py`; `test_*.py` optional | `adversarial_tests/test_prompt_steerer_verifier.py` |
| **`02`** | Phase 1 | `wire_trace_inspector.py`; `test_*.py` optional | `adversarial_tests/test_wire_trace_inspector_verifier.py` |
| **`03`** | Phase 1 | `reppit_orchestrator.py`; `test_*.py` optional | `adversarial_tests/test_reppit_orchestrator_verifier.py` |
| **`04`** | Phase 1 | `context_compactor.py`; `test_*.py` optional | `adversarial_tests/test_context_compactor_verifier.py` |
| **`05`** | Phase 2 | `context_compiler.py`; `test_*.py` optional | `adversarial_tests/test_context_compiler_verifier.py` |
| **`06`** | Phase 2 | `skill_and_mcp_harness.py`; `test_*.py` optional | `adversarial_tests/test_skill_and_mcp_harness_verifier.py` |
| **`07`** | Phase 2 | `subagent_council.py`; `test_*.py` optional | `adversarial_tests/test_subagent_council_verifier.py` |
| **`08`** | Phase 2 | `autoresearch_harness.py`; `test_*.py` optional | `adversarial_tests/test_autoresearch_harness_verifier.py` |

---

## 4. Guarantees & Verification Authority

- **Hard Floors & Exit-Code-2 Hooks**: `adversarial_tests/` is protected both by OS `chmod -w` permissions and by the `PreToolUse` Exit-Code-2 hook in `.agents/plugins/vibe-engineering-kit/hooks.json`.
- **Deterministic Authority**: Conversational completion claims are never sufficient; the deterministic authority is always `./labs/<lab>/self_diagnose.sh` (and `./self_diagnose_all.sh` across all 8 labs).
