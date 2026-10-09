# Contributing to Vibe-Coding-Course

We welcome contributions to the **Vibe Coding to Agentic Engineering** hands-on course!

## Core Principles

1. **Zero External Runtime Dependencies**: All lab scripts and unit tests must run using Python 3.11+ standard library only so learners can execute `./self_diagnose_all.sh` in under 1 second without virtualenv setup friction.
2. **Dual-Branch Parity (`agy` & `claude`)**:
   - The `agy` branch provides native **Antigravity / Gemini CLI** customizations (`GEMINI.md`, `AGENTS.md`, `.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/plugins/`).
   - The `claude` branch provides native **Claude Code** customizations (`CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, `.claude-plugin/`).
3. **Requirement Traceability**: Every lab requirement (`REQ-XXXX`) must be verified by an automated unit test (`test_reqXXXX_*`) and validated via `./labs/<lab>/self_diagnose.sh`.
4. **Immutable Verifiers**: Never modify or weaken assertions inside `adversarial_tests/` to make broken code pass.
5. **License**: All contributions are licensed under the Apache License 2.0. Include the standard Apache-2.0 header on all source and shell files.
