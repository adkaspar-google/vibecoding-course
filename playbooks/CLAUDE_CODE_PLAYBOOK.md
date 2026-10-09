# Claude Code Native Track Playbook (`claude` Branch)

This playbook documents how **Vibe-Coding-Course** runs natively in **Claude Code (`claude` CLI & IDE Extensions)** across **Phase 1 (Vibe Coding Foundations & Daily Workflows)** and **Phase 2 (Harness Engineering & Agentic Engineering Loops)**.

---

## 1. Ownership & Harness Primitives (`claude` Track)

| Stage | Owner | Claude Code Interface |
| :--- | :--- | :--- |
| **1. Permission Modes & Earned Autonomy** | `.claude/settings.json` & `Shift+Tab` | `plan` (`plan mode`), `default`, `acceptEdits`, `auto` + `!` bash execution |
| **2. Daily `RePPIT` & `RPI` Workflow** | Claude Code Workflow | `Explore -> Propose (Orthogonal + /clear) -> Plan -> Implement -> Verify` + `/rewind` (`Esc+Esc`) |
| **3. Context Window Physics & Compaction** | Claude Code | `/context` (keep in `<= 40%` Smart Zone), `/btw` (sandboxed side-query), `/compact`, `/clear`, `> run.log 2>&1` backpressure |
| **4. Persistent Project Context** | Repo (`CLAUDE.md`) | `CLAUDE.md` ($\le 45$ lines) + `@docs/*.md` lazy imports + `.claude/rules/*.md` (`paths:` globs) |
| **5. Cross-Session Auto-Memory** | Claude Code Auto-Memory | `~/.claude/projects/<project>/memory/MEMORY.md` (git-repo-scoped, shared across worktrees, 200-line cap) + `/memory` |
| **6. Progressive-Disclosure Skills (`agentskills.io`)** | `.claude/skills/` | `/context-hub-docs` (`chub` grounding & annotations), `/reppit-workflow`, `/architecture-guard`, `/harness-audit` |
| **7. Context-Firewall Subagents & Council** | `.claude/agents/` & `.claude/commands/` | Read-only `code-explorer`, `code-architect`, and `code-reviewer` ($\text{confidence} \ge 80$) via `/feature-dev` & `claude --worktree` |
| **8. Versioned Plugins, Hooks & Ratchets** | `.claude-plugin/` | `.claude-plugin/plugin.json` + `PreToolUse` (Exit Code `2`), `PostToolUse` remediation linters |

---

## 2. Learner Session Flow (`claude` Branch)

1. From the repository root on the `claude` branch, launch learner mode:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. **Explore in `plan mode` (`<= 40%` Smart Zone)**: Run `/context` and `/memory`, inspect the lab's `starter/` files, use `/btw` for quick side-questions without polluting history, and delegate broad discovery to read-only `code-explorer` subagents.
3. **Human approval checkpoint**: Verify no files were modified during exploration before implementation begins:
   ```bash
   git status --short
   ```
4. **Reset context after proposal selection**: Once an architectural proposal and implementation plan (including `Out of Scope / Do NOT Touch`) are selected, run `/clear` so rejected proposal tokens do not pollute implementation.
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

- **File-Tool Deny Rules & Exit-Code-2 Hooks**: `.claude/settings.json` (`Edit(**/adversarial_tests/**)`) and `.claude/learner.settings.json` (`Read(**/expected_output/**)` and `Edit(**/adversarial_tests/**)`) combine with `chmod -w` and `PreToolUse` Exit-Code-2 hooks to guard immutable verifiers.
- **Deterministic Authority**: Conversational completion claims are never authoritative; the deterministic authority is always `./labs/<lab>/self_diagnose.sh` (and `./self_diagnose_all.sh` across all 8 labs).
