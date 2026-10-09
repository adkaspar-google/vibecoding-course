# Architecture & Harness Topology (`@docs/architecture.md`)

This document is referenced on demand from `CLAUDE.md` and `GEMINI.md` / `AGENTS.md` so its tokens are loaded only when architectural context is needed.

## 1. The 6-Layer Agentic Harness Stack

1. **Ubiquitous Language & Bounded Contexts (`labs/lab_01_*`)**:
   Domain value objects (`AccountId`, `MoneyCents`, `LedgerPosting`) and the Wittgensteinian `EpistemicConfidenceGate` (`GROUNDED_EXECUTE`, `CLARIFICATION_REQUIRED`, `ESCALATE_OUT_OF_BOUNDS`).
2. **Persistent Project Context & Auto-Memory (`labs/lab_02_*`)**:
   Concise root context (`CLAUDE.md` / `GEMINI.md` $\le 40$ lines) with `@docs/*.md` on-demand imports plus git-repo-scoped cross-session auto-memory (`~/.claude/projects/<project>/memory/MEMORY.md` vs `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md`).
3. **Progressive-Disclosure Agent Skills (`labs/lab_03_*`)**:
   `agentskills.io` compliant skill directories (`anthropic-brand/` with `SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) authored manually from observed baseline failure deltas ("Experience Before Theory").
4. **Empirical Skill Evaluation & Trigger Calibration (`labs/lab_04_*`)**:
   Paired `with_skill` vs `without_skill` grading (`grading.json`, `benchmark.json`, `eval-viewer` HTML) and Signal Detection Theory ($d'$, criterion bias $c$, Reference-First consolidation to $\le 3$ skills).
5. **7-Phase Multi-Agent Collaboration (`labs/lab_05_*`)**:
   `feature-dev` workflow orchestrating read-only `code-explorer`, `code-architect` (`minimal_changes`, `clean_architecture`, `pragmatic_balance`), and `code-reviewer` (`confidence >= 80`) subagents.
6. **Versioned Plugins, MCP Servers & The On-the-Loop Flywheel (`labs/lab_06_*`)**:
   Bundling skills, subagents, `PreToolUse` hooks, and JSON-RPC MCP tools into `vibe-engineering-kit`, and escalating multi-service brownfield drift to Spec-Driven Development (SDD).
