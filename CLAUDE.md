# Vibe-Coding-Course — Claude Code Persistent Project Context

## Commands & Environment
- Language: Python 3.11+ standard library only (zero external runtime packages).
- Test runner: `CI=true python3 -m unittest` (or `CI=true python3 -m unittest discover -s <dir> -p "test_*.py" -v`).
- Lab grader: `./labs/<lab>/self_diagnose.sh [TARGET_DIR]` (defaults to `expected_output`; pass `work` in learner mode).
- Full suite: `CI=true ./self_diagnose_all.sh`.
- Context & memory inspection: `/context` (audit token utilization) and `/memory` (inspect `~/.claude/projects/<project>/memory/MEMORY.md`).

## Architecture & Directory Map
- `labs/lab_01_*` .. `labs/lab_06_*`: 6 progressive hands-on labs from Ubiquitous Language & Epistemic Gates to Multi-Agent `feature-dev` and Plugins.
- `.claude/skills/anthropic-brand/`: Multi-file skill (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) invoked via `/anthropic-brand`.
- `.claude/agents/`: Read-only subagents (`code-explorer.md`, `code-architect.md`, `code-reviewer.md`) orchestrated via `/feature-dev`.
- `playbooks/`: Track playbooks (`CLAUDE_CODE_PLAYBOOK.md`, `ANTIGRAVITY_PLAYBOOK.md`, `DUAL_HARNESS_VIBE_CODING_PLAYBOOK.md`).

## Core Conventions
- Requirement traceability: every requirement `REQ-XXXX` MUST be verified by a unit test named `test_reqXXXX_*`.
- Immutable verifiers: `adversarial_tests/` is strictly read-only (`chmod -w` and `Edit(**/adversarial_tests/**)` denied). Never modify or weaken test assertions.
- In learner mode (`claude --settings .claude/learner.settings.json`), `expected_output/` is hidden via `Read(**/expected_output/**)` deny rules; write deliverables under `labs/<lab>/work/`.
- Maintain `2–3` focused skills per task (SkillsBench sweet spot) and author skills manually ("a conciencia") from observed baseline failure deltas.

## On-Demand References
- Pull 6-layer harness architecture on demand via @docs/architecture.md
- Pull testing and immutable verifier rules on demand via @docs/testing-conventions.md
- Pull Wittgenstein Language-Games & Fowler conceptual model notes via @docs/wittgenstein-language-games.md
- Pull SkillsBench (`arXiv:2602.12670`) empirical metrics via @docs/skillsbench-empirical-guide.md
