# Vibe-Coding-Course — Claude Code Persistent Project Context

## Commands & Environment
- Language: Python 3.11+ standard library only (zero external runtime packages).
- Test runner: `CI=true python3 -m unittest` (or `CI=true python3 -m unittest discover -s <dir> -p "test_*.py" -v`).
- Lab grader: `./labs/<lab>/self_diagnose.sh [TARGET_DIR]` (defaults to `expected_output`; pass `work` in learner mode).
- Full 8-lab suite: `CI=true ./self_diagnose_all.sh`.
- Context & memory inspection: `/context` (audit token utilization against the 40% Dumb Zone), `/btw` (sandboxed side-query), `/clear`, `/rewind`, and `/memory` (`~/.claude/projects/<project>/memory/MEMORY.md`).

## Architecture & Directory Map
- `labs/lab_01_*` .. `labs/lab_04_*`: Phase 1 Labs (Engineering Steering & Earned Autonomy, Wire-Trace Inspector, `RePPIT` Workflow & Reflection, 40% Dumb Zone & `RPI` Compaction).
- `labs/lab_05_*` .. `labs/lab_08_*`: Phase 2 Labs (60-Line Context Map & Memory, Progressive Skills + `chub` + Meta-MCP Code Mode, Subagent Firewalls & `llm-council`, 4-Tier Governance + Remediation Linters + `Autoresearch` Ratchet).
- `.claude/skills/`: Curated progressive-disclosure skills (`context-hub-docs/`, `reppit-workflow/`, `architecture-guard/`, `harness-audit/`).
- `.claude/agents/`: Read-only subagents (`code-explorer.md`, `code-architect.md`, `code-reviewer.md`) orchestrated via `/feature-dev`.
- `playbooks/`: Track playbooks (`CLAUDE_CODE_PLAYBOOK.md`, `ANTIGRAVITY_PLAYBOOK.md`, `DUAL_HARNESS_VIBE_CODING_PLAYBOOK.md`).

## Core Conventions
- Requirement traceability: every requirement `REQ-XXXX` (`REQ-0101`..`REQ-0806`) MUST be verified by a unit test named `test_reqXXXX_*`.
- Immutable verifiers: `adversarial_tests/` is strictly read-only (`chmod -w` and `Edit(**/adversarial_tests/**)` denied). Never modify or weaken test assertions.
- In learner mode (`claude --settings .claude/learner.settings.json`), `expected_output/` is hidden via `Read(**/expected_output/**)` deny rules; write deliverables under `labs/<lab>/work/`.
- Maintain `2–3` focused curated skills per task (`SkillsBench` sweet spot) and keep context utilization in the `<= 40%` Smart Zone via Frequent Intentional Compaction (`RPI`).

## On-Demand References
- Pull Two-Phase 8-lab harness architecture on demand via @docs/architecture.md
- Pull testing and immutable verifier rules on demand via @docs/testing-conventions.md
- Pull language, Ubiquitous Language, and AI Engineering Skills Map notes via @docs/language-and-code-foundations.md
- Pull SkillsBench (`arXiv:2602.12670`), `chub`, Meta-MCP, and `autoresearch` guide via @docs/skillsbench-and-harness-guide.md
