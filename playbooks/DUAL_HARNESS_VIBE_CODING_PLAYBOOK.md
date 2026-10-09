# Dual-Harness Vibe Coding to Agentic Engineering Playbook (`agy` & `claude`)

This playbook serves as the architectural reference for **Vibe-Coding-Course**, the foundational prerequisite to **SDD-Crash-Course** (Spec-Driven Development). It maps the 1-to-1 correspondence between the **Antigravity (`agy` branch)** and **Claude Code (`claude` branch)** harnesses across six engineering layers.

---

## 1. Why Vibe Coding Precedes SDD: The 3-Tier Steering Taxonomy

| Paradigm | Human Steering Layer | Primary Harness Artifacts | Strengths | Scale Limit (Why SDD Follows) |
| :--- | :--- | :--- | :--- | :--- |
| **1. AI-Assisted Coding** | **Syntax / Line Layer** | Autocomplete + inline diffs | High precision on single functions | Human types or micromanages every file |
| **2. Disciplined Vibe Coding (This Course)** | **Intent, Vocabulary & Harness Layer** | `CLAUDE.md` / `GEMINI.md`, Auto-Memory, `SKILL.md`, `feature-dev` subagents, Plugins + Hooks | Rapid 0-to-1 features, bounded modules, interactive flow with "On-the-Loop" guardrails | Multi-service brownfield contract drift across $>3$ services requires persistent system specs |
| **3. Spec-Driven Development (Follow-On Course)** | **System Specification Layer** | `proposal.md`, `spec.md`, `design.md`, `tasks.md`, `SPEC.md` SSOT | Scales to multi-team distributed architectures & clean-room rebuilds | Higher ceremony than needed for 0-to-1 spikes |

---

## 2. Master 1-to-1 Harness Architecture Matrix (`claude` vs. `agy`)

| Layer | Claude Code (`claude` branch) | Antigravity / Gemini CLI (`agy` branch) |
| :--- | :--- | :--- |
| **1. Persistent Project Context** | `CLAUDE.md` ($\le 40$ lines) with `@docs/*.md` on-demand imports + `.claude/rules/*.md` (`paths:` globs) | `GEMINI.md` & `AGENTS.md` ($\le 40$ lines) with `@docs/*.md` on-demand references + `.agents/rules/*.md` (`trigger: always_on \| model_decision \| glob \| manual`) |
| **2. Cross-Session Auto-Memory** | `~/.claude/projects/<project>/memory/MEMORY.md` (derived from git repo root; shared across worktrees; 200-line / 25 KB startup cap) + `topics/*.md` | `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` (Knowledge Items + `topics/*.md` with epistemic tags `#direct`, `#commit:<sha>`, `#time:<date>`, `#session:<id>`) |
| **3. Context & Memory Commands** | `/context`, `/memory`, `/clear`, `/compact` | `/stats`, `/memory` (`show \| add \| refresh`), `/skills`, `/plan`, `/clear`, `/compress` |
| **4. Progressive-Disclosure Skills** | `.claude/skills/<name>/SKILL.md` (`agentskills.io` spec), invoked via `/skillname` (e.g., `/anthropic-brand` with `docs.md`, `slides-deck.md`, `apply_template.md`) | `.agents/skills/<name>/SKILL.md` (`agentskills.io` spec), invoked via `/skillname` (e.g., `/anthropic-brand` with `docs.md`, `slides-deck.md`, `apply_template.md`) |
| **5. Skill Evaluation & Trigger Tuning** | Anthropic `skill-creator` (`with_skill` vs `without_skill`), `grading.json`, `benchmark.json`, `eval-viewer/generate_review.py`, 60/40 description loop | `skill-creator` + paired ablation (`with_skill` vs `without_skill`), `eval-viewer`, Signal Detection Theory (`d'`, criterion `c`, utility `U`) |
| **6. Multi-Agent Collaboration (`feature-dev`)** | `.claude/agents/{code-explorer,code-architect,code-reviewer}.md` + `/feature-dev` 7-phase command | `.agents/agents/{code-explorer,code-architect,code-reviewer}.md` + `.agents/workflows/feature-dev.md` (`/feature-dev`) & `/plan` |
| **7. Versioned Plugins, Hooks & MCP** | `.claude-plugin/plugin.json` + `.mcp.json` + `hooks/hooks.json` (`PreToolUse`, `PostToolUse`, `Stop`) | `.agents/plugins/<name>/plugin.json` + `mcp_config.json` + `hooks.json` (`PreToolUse`, `PostToolUse`, `Stop`) |

---

## 3. Core Empirical & Conceptual Foundations

1. **Code as Conceptual Model (Unmesh Joshi, *What Is Code?*, martinfowler.com, May 2026)**:
   - Code is both machine instructions and a **model of understanding**. Passive review of generated code accumulates **Cognitive Debt** (synonym drift and ungrounded abstractions).
2. **Wittgenstein's Two Theories of Language — How Language Produces Actions & Code**:
   - **Early Wittgenstein (*Tractatus Logico-Philosophicus*, 1921) — Picture Theory of Language:** Language as a strict, formal, 1-to-1 logical picture of facts $\leftrightarrow$ traditional programming languages, type systems, and unit tests (*instructions for a machine*).
   - **Late Wittgenstein (*Philosophical Investigations*, 1953) — Meaning as Use & Language as Action:** Natural language as a collaborative toolbox used between a builder and an assistant to coordinate real actions (`Molino & Tagliabue, arXiv:2302.01570`; `Winograd & Flores, 1986`).
   - **Empirical Proof in Interactive Coding Agents (`Wang, Liang, & Manning, ACL 2016, arXiv:1606.02447`; `MaKTO arXiv:2501.14225`; `Marco Graziano LGDL`; `SciTePress 139777`):** In Stanford's `SHRDLURN` study of 100 human players instructing an AI assistant solely through natural language to perform block-building actions, task completion depended on **(a) avoiding synonyms** (consistent domain vocabulary) and **(b) compositionality** (defining reusable higher-level instructions, exactly like Skills), paired with coworker-style clarification gates (`GROUNDED_EXECUTE` vs `CLARIFICATION_REQUIRED` vs `ESCALATE_OUT_OF_BOUNDS`).
3. **Why Loop vs. How Loop & "On-the-Loop" Harness Engineering (Kief Morris, Mar 2026)**:
   - Humans own the **Why Loop**; agents execute the nested **How Loop**. When an agent errs, an **On-the-Loop** engineer upgrades the harness (`CLAUDE.md`/`GEMINI.md`, `MEMORY.md`/`KNOWLEDGE.md`, `SKILL.md`, `PreToolUse` hook, or MCP tool).
4. **Empirical Science of Skills (`SkillsBench` `arXiv:2602.12670v4`, 87 tasks, 9,396 trajectories)**:
   - **Human-Authored Skills ("A Conciencia")**: **+16.6 pp** average pass-rate lift (`33.9% -> 50.5%`; **+24.8 pp on Gemini CLI**, **+18.2 pp on Claude Code**).
   - **Self-Generated Skills Degrade Performance**: **$-8.1\text{ pp}$ on Claude Code**, **$-11.3\text{ pp}$ on Codex**, and **$-11.5\text{ pp}$ on Gemini CLI** below the No-Skills baseline due to training-data regurgitation and hallucinated unit conversions (`1000x` trap).
   - **Skill Overload Penalty**: `2–3` focused skills achieve peak lift (**+19.0 pp**), whereas `>= 4` skills drop to **+10.1 pp** due to routing collisions.
