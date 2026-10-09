---
name: harness-audit
description: >-
  Audits repository harness health across root context files, auto-memory caps,
  skill progressive disclosure, and immutable verifier hooks. Use when diagnosing
  agent drift or running /vibe-engineering-kit:harness-audit. Don't use for
  application business logic implementation.
---

# Harness Audit Skill (`harness-audit`)

Invoked as `/vibe-engineering-kit:harness-audit` when packaged inside the `vibe-engineering-kit` plugin.

## Audit Checklist
1. Root context (`CLAUDE.md` / `GEMINI.md` / `AGENTS.md`) is $\le 120$ lines with `@path` references.
2. Auto-memory (`MEMORY.md` / `KNOWLEDGE.md`) is $\le 200$ lines and uses `#direct` discipline.
3. Active workspace skills stay within the `2–3` focused outcome sweet spot.
4. `PreToolUse` hooks block mutations to `adversarial_tests/`.
