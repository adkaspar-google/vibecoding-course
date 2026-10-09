# Dual-Harness Vibe Coding & Agentic Engineering Playbook (`agy` & `claude`)

This playbook serves as the architectural reference for **Vibe-Coding-Course**, mapping the 1-to-1 correspondence between the **Google Antigravity (`agy` branch)** and **Anthropic Claude Code (`claude` branch)** harnesses across **Phase 1 (Vibe Coding Foundations & Daily Workflows)** and **Phase 2 (Harness Engineering & Agentic Engineering Loops)**.

---

## 1. The 2022–2026 Architectural & Human-Interaction Evolution

| Era | Milestone & Protocol Breakthroughs | Model Paradigm Shift | Human-Agent Interaction Pattern |
| :--- | :--- | :--- | :--- |
| **Late 2022** | GitHub Copilot GA (Jun 2022), ReAct (`arXiv:2210.03629`, Oct 2022), ChatGPT (Nov 30, 2022) | Next-token code completion & single-turn RLHF chat | Ghost-text `Tab` autocomplete & copy-pasting snippets between browser and IDE |
| **2023** | Cursor launch (Mar 2023), OpenAI `Function Calling` (`gpt-4-0613`, Jun 2023), SWE-bench (Oct 2023), Parallel `tools` API (Nov 2023) | Fine-tuned JSON schema `tool_calls` emission | In-editor `@Codebase` RAG & inline `Cmd+K` diff generation |
| **2024** | Gemini 1.5 Pro 1M–2M Context (Feb 2024), SWE-agent ACI (Apr 2024), Claude 3.5 Sonnet + `.cursorrules` (Jun 2024), OpenAI `o1` RL reasoning (Sep 2024), **MCP open-sourced** (Nov 25, 2024) | Test-time RL reasoning chains + MCP universal tool bus | Multi-file IDE composers & static repository rules files |
| **Early–Mid 2025** | DeepSeek-R1 `RLVR` (Jan 2025), **Karpathy coins "Vibe Coding"** (Feb 2, 2025), **Claude Code + `CLAUDE.md`** (Feb 24, 2025), **Google A2A Protocol** (Apr 2025), Claude 4 interleaved tool thinking (May 2025), **Gemini CLI (`GEMINI.md`) + `AGENTS.md`** (Jun 2025) | RL with Verifiable Rewards (compilers/tests) & interleaved reasoning across multi-step tool loops | Conversational Vibe Coding & terminal-native agents guided by `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` |
| **Late 2025** | Claude Code Subagents & Hooks (Summer 2025), Plugins (Oct 2025), Agent Skills `SKILL.md` (Oct 2025), **Google Antigravity & Gemini 3** (Nov 18, 2025), **`agentskills.io` Standard** (Dec 18, 2025) | 3-level progressive disclosure (`YAML -> SKILL.md -> scripts/`) & subagent context firewalls | Agent-first Mission Control (`Implementation Plan` & `Walkthrough` Artifacts, Browser Subagent, Knowledge Items) |
| **2026 – NOW** | **Harness Engineering** (OpenAI, Fowler/Böckeler/Morris, `SkillsBench`), **Karpathy's `autoresearch` (`program.md`)**, **Antigravity 2.0 (`agy`)**, **Andrew Ng's *AI Skills Map*, `OpenWorker` & `context-hub` (`chub`)**, **Stanford CS146S (`RePPIT` & Meta-MCP Code Mode)**, **Anthropic *Recursive Self-Improvement*** | Long-horizon autonomous loops (METR 4-month doubling horizon to 12–16 hrs) governed by deterministic sensors & ratchets | **Harness Engineering**: 4-tier governance, remediation linters, front-loaded Program Design (types/call-trees), and closed-loop Keep-or-Revert ratchets |

---

## 2. Master 1-to-1 Dual-Harness Architecture Matrix (`claude` vs. `agy`)

| Capability Layer | Claude Code (`claude` branch) | Google Antigravity (`agy` branch) |
| :--- | :--- | :--- |
| **1. Permission Modes & Earned Autonomy** | `.claude/settings.json` (`plan`, `default`, `acceptEdits`, `auto`) + `Shift+Tab` | `~/.gemini/antigravity-cli/settings.json` (`strict`, `request-review`, `proceed-in-sandbox`, `always-proceed`) + `/config` |
| **2. Daily `RePPIT` Workflow** | `plan mode` $\to$ Orthogonal Proposals + `/clear` $\to$ Plan (`Ctrl+G`) $\to$ Implement $\to$ Verify + `/rewind` (`Esc+Esc`) | `/grill-me` $\to$ Orthogonal Proposals + `/clear` $\to$ `/plan` (`Implementation Plan` Artifact) $\to$ Implement $\to$ `/browser` + `Walkthrough` Artifact |
| **3. Context Physics (`<= 40%` Smart Zone)** | `/context`, `/btw` (sandboxed side-query), `/compact [focus]`, `/clear` | `/stats`, `/compress`, `/clear`, `> run.log 2>&1` backpressure |
| **4. Persistent Project Context Map** | `CLAUDE.md` ($\le 45$ lines) with `@docs/*.md` lazy imports + `.claude/rules/*.md` (`paths:`) | `GEMINI.md` & `AGENTS.md` ($\le 45$ lines) with `@docs/*.md` lazy imports + `.agents/rules/*.md` (`trigger:`) |
| **5. Cross-Session Memory & Provenance** | `~/.claude/projects/<project>/memory/MEMORY.md` (git-worktree-shared, 200-line cap) + `/memory` | `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` (`#direct`, `#commit`, `#time`, `#session`) + `/memory show\|add\|refresh` |
| **6. Progressive Skills & `chub` Grounding** | `.claude/skills/{context-hub-docs,reppit-workflow,architecture-guard,harness-audit}/SKILL.md` | `.agents/skills/{context-hub-docs,reppit-workflow,architecture-guard,harness-audit}/SKILL.md` + `/skills` |
| **7. Subagent Context Firewalls & Council** | `.claude/agents/{code-explorer,code-architect,code-reviewer}.md` + `/feature-dev` + `claude --worktree` | `.agents/agents/{code-explorer,code-architect,code-reviewer}.md` + `.agents/workflows/feature-dev.md` + Mission Control worktrees |
| **8. Governance Hooks & Closed-Loop Ratchets** | `.claude-plugin/plugin.json` + `PreToolUse` (Exit Code `2`) + `PostToolUse` remediation linter | `.agents/plugins/vibe-engineering-kit/{plugin.json,mcp_config.json,hooks.json}` (`PreToolUse` Exit Code `2`) |
