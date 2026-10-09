---
name: reppit-workflow
description: >-
  Guides the 5-step RePPIT daily engineering workflow (Research -> Propose -> Plan ->
  Implement -> Test/Verify) with Socratic clarification, 2 orthogonal architectural
  proposals, post-proposal context reset, Out-of-Scope plan guardrails, and
  Frequent Intentional Compaction (RPI). Use when building multi-file features or
  refactoring modules. Don't use for single-line typo fixes.
---

# `RePPIT` & `RPI` Intentional Compaction Skill (`reppit-workflow`)

Implements the Stanford CS146S Lecture 3 (`themodernsoftware.dev`) 5-step workflow and Dex Horthy's Frequent Intentional Compaction (`rmvDxxNubIg`).

## 5-Step Protocol
1. **Research (`research.md`)**: Strictly document *what exists today* with exact `file.py:L10` citations. Never propose solutions during Research. Resolve ambiguities via `/grill-me` (or Plan Mode questioning).
2. **Propose + Context Reset**: Draft **2 orthogonal architectural proposals** (`references/proposal_template.md`). Once the engineer selects one proposal, immediately purge the rejected proposal's tokens from context (`/clear` or `/compress`).
3. **Plan (`plan.md`)**: Specify exact `file:line` targets, verification commands, and a mandatory `## Out of Scope / Do NOT Touch` guardrail section (`references/plan_template.md`).
4. **Implement (Phase-Based Model Routing)**: Route `Research/Propose/Plan` to a frontier reasoning model (`gemini-3.1-pro` / `claude-opus-4-6`) and `Implement/Verify` to a fast model (`gemini-3-flash` / `claude-sonnet-4-6`).
5. **Verify & Reflect**: Run deterministic unit tests (`self_diagnose.sh`), `/browser` behavioral checks, and emit a verified `walkthrough.md` Run Receipt.
