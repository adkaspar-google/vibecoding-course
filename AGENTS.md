# Vibe-Coding-Course — Antigravity / Gemini CLI Persistent Project Context

## Commands & Environment
- Language: Python 3.11+ standard library only (zero external runtime packages).
- Test runner: `CI=true python3 -m unittest` (or `CI=true python3 -m unittest discover -s <dir> -p "test_*.py" -v`).
- Lab grader: `./labs/<lab>/self_diagnose.sh [TARGET_DIR]` (defaults to `expected_output`; pass `work` in learner mode).
- Full suite: `CI=true ./self_diagnose_all.sh`.
- Context & memory inspection: `/stats` (session token usage), `/memory` (`/memory show`, `/memory add`, `/memory refresh`), and Antigravity Knowledge Items (`~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md`).

## Architecture & Directory Map
- `labs/lab_01_*` .. `labs/lab_06_*`: 6 progressive hands-on labs from Ubiquitous Language & Epistemic Gates to Multi-Agent `feature-dev` and Plugins.
- `.agents/skills/anthropic-brand/`: Multi-file `agentskills.io` skill (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) invoked via `/anthropic-brand`.
- `.agents/agents/`: Read-only subagents (`code-explorer.md`, `code-architect.md`, `code-reviewer.md`) orchestrated via Antigravity Agent Manager, `/feature-dev`, or `/plan`.
- `.agents/plugins/vibe-engineering-kit/`: Versioned plugin bundle (`plugin.json`, `mcp_config.json`, `hooks.json`).

## Core Conventions
- Requirement traceability: every requirement `REQ-XXXX` MUST be verified by a unit test named `test_reqXXXX_*`.
- Immutable verifiers: `adversarial_tests/` is strictly read-only (`chmod -w` and `PreToolUse` hook guarded). Never modify or weaken test assertions.
- Epistemic provenance: in Knowledge Items (`KNOWLEDGE.md`), reserve `#direct` strictly for explicit user instructions; anchor codebase observations with `#commit`, `#time`, and `#session`.
- Maintain `2–3` focused skills per task (SkillsBench sweet spot) and author skills manually ("a conciencia") from observed baseline failure deltas.

## On-Demand References
- Pull 6-layer harness architecture on demand via @docs/architecture.md
- Pull testing and immutable verifier rules on demand via @docs/testing-conventions.md
- Pull Wittgenstein Language-Games & Fowler conceptual model notes via @docs/wittgenstein-language-games.md
- Pull SkillsBench (`arXiv:2602.12670`) empirical metrics via @docs/skillsbench-empirical-guide.md
