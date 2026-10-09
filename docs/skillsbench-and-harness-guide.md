# Empirical Skill Science, Meta-MCP & Harness Engineering (`@docs/skillsbench-and-harness-guide.md`)

Referenced on demand from `CLAUDE.md`, `GEMINI.md`, and `AGENTS.md`.

## 1. SkillsBench Empirical Findings (`arXiv:2602.12670`, Li et al., 2026)
- Evaluated across **87 tasks**, **8 domains**, and **9,396 agent trajectories**:
  - **No-Skills Baseline**: **33.9%** pass rate.
  - **Focused Curated Skills**: **50.5%** pass rate (**+16.2pp to +16.6pp average lift**).
  - **Self-Generated Skills Degrade Accuracy**: Having an agent auto-generate its own skills without human curation drops performance (**-1.3pp to -11.5pp** below baseline) due to pretraining repetition and hallucinated unit conversions.
  - **Skill Overload Cliff**: `2–3` focused skills achieve peak lift (**+19.0pp**), whereas loading `>10` overlapping skills degrades routing precision.

## 2. Curated API Grounding (`andrewyng/context-hub`) & Meta-MCP "Code Mode" (Stanford CS146S)
- **`@aisuite/chub` (`context-hub`)**: Prevents SDK hallucinations by fetching versioned, language-specific docs (`chub search`, `chub get --lang py`) and persisting session discoveries via `chub annotate` (`--with-annotations`).
- **Meta-MCP "Code Mode" (`search` + `execute`)**: Replaces 100+ raw CRUD tool schemas with 2 compact meta-tools (`mcp__meta__search` and `mcp__meta__execute`), reducing standing schema token overhead by **$\ge 90\%$**.

## 3. Durable Execution (`Temporal`), Closed-Loop Ratchets (`karpathy/autoresearch`) & Front-Loaded Alignment (`Ib5GBkD555M`)
- **Durable Execution Frameworks (`Temporal`, `LangGraph`, `DBOS`, `Restate`, `Inngest`)**: Wrap deterministic agent orchestration inside replayable **Workflows** while executing non-deterministic LLM and MCP tool calls as fault-tolerant **Activities** with event-history replay and zero-compute Human-in-the-Loop (HITL) signals.
- **3-File `autoresearch` Separation**: Immutable evaluator (`prepare.py`), single mutable target (`train.py`), and human-authored harness spec (`program.md`) with the **Simplicity Criterion** and Git Keep-or-Revert Ratchet.
- **Why "Lights-Off" Factories Fail (`Ib5GBkD555M`)**: RLVR optimizes $t=0$ test pass rather than $t=6\text{ mo}$ maintainability; prevent architectural collapse via **Front-Loaded Program Design** (explicit types, interfaces, and call-trees before vertical slices).
