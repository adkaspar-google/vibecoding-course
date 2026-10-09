---
description:Guided 7-phase multi-agent feature development workflow orchestrating code-explorer, code-architect, and code-reviewer subagents.
---

# 7-Phase Multi-Agent Feature Development (`/feature-dev`)

Execute this 7-phase pipeline whenever building a non-trivial feature:

1. **Phase 1: Discovery** — Clarify the feature objective and create a 7-phase progress checklist.
2. **Phase 2: Codebase Exploration (`code-explorer`)** — Launch 2–3 parallel read-only `code-explorer` subagents (`Glob`, `Grep`, `Read`) to trace entry points and call chains (`file:line`) and identify the top essential files to read.
3. **Phase 3: Clarifying Questions Gate (MANDATORY STOP)** — Present all edge cases, error-handling questions, and boundary ambiguities discovered during exploration. **Wait for explicit user answers before proceeding to Phase 4.**
4. **Phase 4: Architecture Design (`code-architect`)** — Launch parallel `code-architect` subagents across three lenses (`minimal_changes`, `clean_architecture`, `pragmatic_balance`), present trade-offs, and **wait for user selection**.
5. **Phase 5: Implementation** — Implement the selected architecture and run `./labs/<lab>/self_diagnose.sh work`.
6. **Phase 6: Quality Review (`code-reviewer`)** — Launch 3 parallel `code-reviewer` subagents (Simplicity/DRY, Functional Bugs, and `CLAUDE.md` Conventions) and report only findings with `confidence >= 80`.
7. **Phase 7: Summary** — Summarize files modified, architectural decisions, and test verification output.
