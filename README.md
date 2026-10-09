# Vibe Coding to Agentic Engineering (`Vibe-Coding-Course`)

> **The Prerequisite Hands-On Course to `SDD-Crash-Course` (Spec-Driven Development)**
> **Dual-Branch Support:** `agy` (Antigravity / Gemini CLI) & `claude` (Claude Code)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-green.svg)](self_diagnose_all.sh)
[![Labs: 6/6 Passing](https://img.shields.io/badge/Hands--On_Labs-6%2F6_Passing-brightgreen.svg)](labs/)

As LLMs make syntax generation cheaper, the mechanical act of typing instructions becomes less central. What becomes paramount is **making the conceptual model explicit, discovering the right domain vocabulary, and refining that vocabulary through iteration, domain expertise, and feedback** (Unmesh Joshi, *What Is Code?*, martinfowler.com, May 2026).

This hands-on course bridges the gap between unstructured **"Ralph Wiggum" vibe coding** and **Spec-Driven Development (SDD)** by teaching engineers how to ground coding agents in **Wittgensteinian Language Games**, **Persistent Context (`CLAUDE.md` / `GEMINI.md`)**, **Cross-Session Auto-Memory**, **Human-Crafted `agentskills.io` Skills ("A Conciencia")**, **Paired Skill Evaluation (`eval-viewer` & Signal Detection Theory)**, **Multi-Agent Collaboration (`feature-dev`)**, and **Versioned Plugins + MCP Servers**.

---

## 1. Quickstart (`< 1s` Self-Diagnosis)

```bash
# Clone and switch to your preferred harness branch ('agy' or 'claude')
git checkout agy     # For Antigravity / Gemini CLI support
git checkout claude  # For Claude Code support

# Run the master self-diagnosis suite across all 6 labs (< 1 second, zero external deps)
./self_diagnose_all.sh

# Run the track verification suite for both 'agy' and 'claude' harnesses
CI=true python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 2. Dual-Branch Harness Architecture (`agy` vs. `claude`)

| Capability Layer | `claude` Branch (Claude Code) | `agy` Branch (Antigravity / Gemini CLI) |
| :--- | :--- | :--- |
| **1. Persistent Project Context** | [`CLAUDE.md`](CLAUDE.md) ($\le 40$ lines) with `@docs/*.md` on-demand imports + `.claude/rules/*.md` | [`GEMINI.md`](GEMINI.md) & [`AGENTS.md`](AGENTS.md) ($\le 40$ lines) with `@docs/*.md` references + `.agents/rules/*.md` (`trigger: always_on \| model_decision`) |
| **2. Cross-Session Auto-Memory** | `~/.claude/projects/<project>/memory/MEMORY.md` (derived from git repo root; shared across worktrees; 200-line / 25 KB cap) | `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` (Knowledge Items + `artifacts/*.md` with `#direct`, `#commit`, `#time`, `#session` tags) |
| **3. Context & Memory Commands** | `/context`, `/memory`, `/clear`, `/compact` | `/stats`, `/memory` (`show \| add \| refresh`), `/skills`, `/plan`, `/clear`, `/compress` |
| **4. Multi-File Agent Skills** | `.claude/skills/anthropic-brand/` (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) invoked via `/anthropic-brand` | `.agents/skills/anthropic-brand/` (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) invoked via `/anthropic-brand` |
| **5. Skill Evaluation & Trigger Tuning** | Anthropic `skill-creator` + `grading.json` + `benchmark.json` + `eval-viewer/generate_review.py` | Paired `with_skill` vs `without_skill` ablation + `eval-viewer` + Signal Detection Theory ($d'$, $c$, $U$) |
| **6. Multi-Agent Collaboration** | `.claude/agents/{code-explorer,code-architect,code-reviewer}.md` + `/feature-dev` 7-phase command | `.agents/agents/{code-explorer,code-architect,code-reviewer}.md` + `.agents/workflows/feature-dev.md` (`/feature-dev`) & `/plan` |
| **7. Versioned Plugins, Hooks & MCP** | `.claude-plugin/plugin.json` + `.mcp.json` + `hooks/hooks.json` (`PreToolUse`) | `.agents/plugins/vibe-engineering-kit/{plugin.json,mcp_config.json,hooks.json}` |

> **Branch maintenance:** `main` is the dual-harness source of truth. The `agy` and `claude` branches are derived from it (other harness's files and walkthrough track removed) by `python3 tools/specialize_branch.py agy|claude` — never edit them by hand.

---

## 3. Progressive 6-Lab Hands-On Curriculum

| Lab | Title & Core Concept | Key Deliverable (`expected_output/` / `work/`) | Requirements |
| :--- | :--- | :--- | :--- |
| **[Lab 01](labs/lab_01_vocabulary_and_bounded_language_games/WALKTHROUGH.md)** | **Ubiquitous Language & Wittgensteinian Epistemic Honesty**<br>Eliminating Cognitive Debt, synonym drift, float money bugs, and Private-Language FX hallucinations | `domain_ledger.py` (`AccountId`, `MoneyCents`, `SettlementBatch`, `evaluate_language_game_move`) | `REQ-0101` .. `REQ-0106` |
| **[Lab 02](labs/lab_02_persistent_context_and_memory_hygiene/WALKTHROUGH.md)** | **Persistent Context (`CLAUDE.md` / `GEMINI.md`) & Auto-Memory**<br>On-demand `@docs/*.md` references, git-worktree memory sharing, 200-line `MEMORY.md` cap, `#direct` discipline, and `/context` 60% degradation wall | `context_memory_manager.py` | `REQ-0201` .. `REQ-0206` |
| **[Lab 03](labs/lab_03_crafting_agent_skills_progressive_disclosure/WALKTHROUGH.md)** | **Crafting `agentskills.io` Skills Manually ("A Conciencia")**<br>3-Level Progressive Disclosure (`anthropic-brand/{SKILL.md,docs.md,slides-deck.md,apply_template.md}`) vs. SkillsBench self-generated `1000x` unit-conversion traps | `skill_validator.py` + `anthropic-brand/` | `REQ-0301` .. `REQ-0306` |
| **[Lab 04](labs/lab_04_skill_evaluation_and_trigger_calibration/WALKTHROUGH.md)** | **Skill Evaluation (`eval-viewer`) & Solving Skill Overload**<br>Paired `with_skill` vs `without_skill` (`grading.json`, `benchmark.json`, `eval-viewer` HTML), SDT $d'$ & $c$, and Reference-First consolidation from $7 \to 3$ skills | `skill_eval_engine.py` | `REQ-0401` .. `REQ-0406` |
| **[Lab 05](labs/lab_05_multi_agent_feature_dev_orchestration/WALKTHROUGH.md)** | **Multi-Agent Collaboration (`feature-dev` 7-Phase Pipeline)**<br>Parallel `code-explorer` (`file:line`), mandatory Phase 3 Clarifying Questions gate, tri-lens `code-architect` (*Minimal*, *Clean*, *Pragmatic*), and `code-reviewer` ($\ge 80$ confidence) | `feature_dev_orchestrator.py` + `agents/*.md` | `REQ-0501` .. `REQ-0506` |
| **[Lab 06](labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/WALKTHROUGH.md)** | **Capstone: Versioned Plugins, MCP Servers & The On-the-Loop Flywheel**<br>`plugin.json`, `PreToolUse` immutable-verifier hooks, JSON-RPC MCP server, Skill-vs-Plugin classifier, and escalating brownfield drift to SDD | `harness_flywheel.py` + `vibe-engineering-plugin/` | `REQ-0601` .. `REQ-0606` |

---

## 4. Literature & Empirical Foundations

- **Unmesh Joshi**, *What Is Code?* (`martinfowler.com/articles/what-is-code.html`, May 2026) — Code as a model of understanding, Ubiquitous Language, and Cognitive Debt.
- **Kief Morris**, *Humans and Agents in Software Engineering Loops* (martinfowler.com *Exploring Gen AI* series) (`martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html`, Mar 2026) — The Why Loop vs. How Loop, and *On-the-Loop* Harness Engineering.
- **Z. He**, *Wittgenstein's Language Games and Heidegger's Being-in-the-World in Human-AI Interaction* (`SciTePress IESD 2025`, Paper `139777`).
- **Ye et al.**, *Multi-Agent KTO (MaKTO): Grounding Decision-Making and Language Expression in Wittgenstein's Language Games* (`arXiv:2501.14225`, 2025) — **61% win rate** (+23.0% over GPT-4o).
- **Marco Graziano**, *Grounding AI with Wittgenstein: From Language-Games to Epistemic Honesty* (`LGDL`, 2025).
- **Li et al. (`SkillsBench`)**, *Benchmarking How Well Agent Skills Work Across Diverse Tasks* (`arXiv:2602.12670v4`, Jun 2026) — Curated human-written skills yield **+16.6 pp** average lift (`33.9% -> 50.5%`), whereas self-generated skills degrade performance (**$-8.1\text{ pp}$ to $-11.5\text{ pp}$** below baseline), and `2–3` focused skills (**+19.0 pp**) outperform `4+` skills (**+10.1 pp**).
- **Agent Skills Specification**: `https://agentskills.io/specification`
- **Anthropic `skill-creator` & `feature-dev`**: `github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md` and `github.com/anthropics/claude-code/blob/main/plugins/feature-dev/README.md`.

---

## 5. Course Deliverables in This Repository

- **13-Page Practical Coursebook PDF**: [`Coursebook_Vibe_Coding_to_Agentic_Engineering.pdf`](Coursebook_Vibe_Coding_to_Agentic_Engineering.pdf)
- **36-Slide `16:9` Widescreen Lecture Deck & Tripartite Speaker Notes**: [`slides/Vibe_Coding_Course_Slides.pdf`](slides/Vibe_Coding_Course_Slides.pdf) and [`slides/SPEAKER_NOTES.md`](slides/SPEAKER_NOTES.md)
- **Narrated `1080p` Step-by-Step Module Videos & Full-Course Master Lecture** (release assets, not tracked in git): `slides/modules/Module_01..07_*.mp4` and `slides/Vibe_Coding_Course_Lecture.mp4` — download from the release page or regenerate with [`slides/build_video.py`](slides/build_video.py) (see [`slides/README.md`](slides/README.md) §3; works with a public `GEMINI_API_KEY`)
- **Playbooks**: [`playbooks/DUAL_HARNESS_VIBE_CODING_PLAYBOOK.md`](playbooks/DUAL_HARNESS_VIBE_CODING_PLAYBOOK.md), [`playbooks/ANTIGRAVITY_PLAYBOOK.md`](playbooks/ANTIGRAVITY_PLAYBOOK.md), and [`playbooks/CLAUDE_CODE_PLAYBOOK.md`](playbooks/CLAUDE_CODE_PLAYBOOK.md)
