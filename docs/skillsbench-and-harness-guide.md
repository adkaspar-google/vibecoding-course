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

## 3. Multi-Agent VCS (`git worktree` vs. Jujutsu `jj`), Durable Execution (`Temporal`), Meta-Harnesses (`Databricks Omnigent`), Ratchets (`karpathy/autoresearch`) & Front-Loaded Alignment (`Ib5GBkD555M`)
- **Multi-Agent Workspace Isolation & Stacked Change Management (`git worktree` vs. Jujutsu `jj`, `wavect.io` & `jj-vcs/jj`)**:
  - **Provisioning Cost vs. Integration Cost (`wavect.io`, Riedl 2026)**: $\text{Provisioning Cost} = \text{Task Starts} \times \text{Cold-Start Min} \times \text{Runner Cost/Min}$ (reduced via `git worktree` + shared `.git` object store / `--filter=blob:none` partial clone) vs. $\text{Integration Cost} = \text{Accepted Changes} \times \text{Reviewer \& Merge Min} \times \text{Eng Cost/Min}$ (reduced via colocated **Jujutsu `jj git init --colocate`** & `jj workspace add`).
  - **Why Colocated Jujutsu (`jj`) Excels for Agentic Loops**: (1) **Working Copy Is a Commit (`@`)** — zero-ceremony auto-snapshotting on every command without `git add`/`stash`; (2) **Stable Change IDs (`k–z`) vs. Commit IDs (`0–9a–f`)** across rewrites; (3) **First-Class Conflict Algebra** ($\Delta M = \text{Tree}(M) - \text{AutoMerge}(P_1, P_2)$) — rebases never abort mid-loop on conflicts, descendants auto-rebase immediately, and N-parent integration commits (`jj new changeA changeB`) rebase cleanly; (4) **Transactional Operation Log (`jj op log`, `jj undo`, `jj op restore <OP_ID>`)** + non-interactive `jj split -m`, `jj squash --into <REV> -u`, `jj absorb`, and `jj converge --no-interactive`. (Use pure `git worktree` when repositories require Git LFS, submodules, `.gitattributes`, or `--filter=blob:none` partial clones.)
- **Durable Execution Frameworks (`Temporal`, `LangGraph`, `DBOS`, `Restate`, `Inngest`)**: Wrap deterministic agent orchestration inside replayable **Workflows** while executing non-deterministic LLM and MCP tool calls as fault-tolerant **Activities** with event-history replay and zero-compute Human-in-the-Loop (HITL) signals.
- **The Meta-Harness Layer (`Databricks Omnigent`, `omnigent.ai`, Zaharia et al., Jun 2026)**: Sits *above* individual coding harnesses (`Claude Code`, `Codex`, `agy`, `Pi`) and SDKs to **Combine** (1-line YAML harness swapping and multi-harness subagent composition), **Control** (stateful session-history security policies — e.g., escalating `git push` to require human approval after `npm install`, pausing every \$100 of LLM spend, and **Egress-Proxy Credential Injection** so the agent runtime never sees raw GitHub/cloud tokens), and **Share** (live multiplayer session URLs across terminal, web, mobile, and `Modal`/`Daytona` sandboxes).
- **3-File `autoresearch` Separation**: Immutable evaluator (`prepare.py`), single mutable target (`train.py`), and human-authored harness spec (`program.md`) with the **Simplicity Criterion** and Git Keep-or-Revert Ratchet.
- **Why "Lights-Off" Factories Fail (`Ib5GBkD555M`)**: RLVR optimizes $t=0$ test pass rather than $t=6\text{ mo}$ maintainability; prevent architectural collapse via **Front-Loaded Program Design** (explicit types, interfaces, and call-trees before vertical slices).
