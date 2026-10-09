# Lab 07: Harness Engineering Layer 3 — Subagents as Context Firewalls, Multi-Agent PR Triage & `llm-council` Peer Review

## 1. Learning Objectives & Conceptual Motivation

1. **Subagents Are Context Firewalls, Not Roleplay Personas (Dex Horthy, `rmvDxxNubIg` & Skills Map 3.2)**:
   A common misconception is treating subagents as human organizational roleplay ("Product Manager Agent talks to QA Agent"). In reality, subagents exist for **Context Window Isolation**:
   - When an agent needs to locate where a payment webhook is validated across 40 files, running 30 `Grep` and `Read` calls in the main thread burns 50,000 tokens and pushes the parent session into the **40% Dumb Zone**.
   - Spawning a read-only `code-explorer` subagent burns those 50,000 search tokens inside an **ephemeral child context window** and returns a **500-token `file:line`-cited summary** to the parent (`>=90%` parent context savings).

2. **Anthropic's `feature-dev` Subagents & Stanford CS146S Multi-Agent PR Triage**:
   - **Read-Only Tool Boundaries**: `code-explorer`, `code-architect`, and `code-reviewer` are strictly restricted to read-only tools (`Glob`, `Grep`, `Read`, `LSP`) so they can never silently mutate files during exploration or review.
   - **Multi-Agent PR Triage (`themodernsoftware.dev` Weeks 6–7)**: Parallel specialist subagents (`Security`, `Performance`, `Architecture`, `Style`, `EdgeCases`) audit a diff; findings with `confidence < 80` are filtered out as noise, and verified findings are triaged into **`MUST_FIX` [Red]**, **`RECOMMENDED` [Yellow]**, and **`CONSIDER` [Green]**.

3. **Karpathy's `llm-council` — Anonymized Cross-Model Peer Review & Chairman Synthesis**:
   In `karpathy/llm-council`, Karpathy contrasts a weekend vibe-coded web app with a 3-stage multi-model verification protocol:
   - **Stage 1 (Independent First Opinions)**: Query multiple models in parallel.
   - **Stage 2 (Anonymized Peer Review & Ranking)**: Strip model identities (`Response A`, `Response B`, `Response C`) so models cannot bias toward their own family, then aggregate peer rankings via **Borda count**.
   - **Stage 3 (Chairman Synthesis)**: Synthesize the top-ranked analysis into the final architectural decision.

4. **Workspace Isolation & Stacked Change Management (`inherit` vs. `git worktree` vs. Colocated Jujutsu `jj`, `wavect.io` & `jj-vcs/jj`)**:
   - Read-only subagents share the parent workspace (`inherit`), whereas parallel write subagents require isolated workspaces with **strictly disjoint file ownership**.
   - **Provisioning Cost vs. Integration Cost (`wavect.io`, Kevin Riedl, 2026)**: Native `git worktree` (`claude --worktree` or Antigravity 2.0 Mission Control worktrees) paired with a shared `.git` object store or `--filter=blob:none` partial clone slashes cold-start **Provisioning Cost** while preserving Git LFS, submodules, and `.gitattributes`.
   - **Colocated Jujutsu (`jj git init --colocate` + `jj workspace add`) for Agentic Change Management**: When parallel agents continuously rewrite stacked commits or hit rebase conflicts, colocating open-source Jujutsu (`github.com/jj-vcs/jj`, `docs.jj-vcs.dev`) slashes **Integration Cost** via: (a) **Working Copy Is a Commit (`@`)** (auto-snapshotted on every command without `git add`/`stash`), (b) **Stable Change IDs (`k–z`)** that survive rewrites (`jj workspace update-stale`), (c) **First-Class Conflict Algebra** ($\Delta M = \text{Tree}(M) - \text{AutoMerge}(P_1, P_2)$) where rebases never abort mid-loop, descendants auto-rebase immediately, and N-parent integration stacks (`jj new changeA changeB`) rebase cleanly, and (d) **Transactional Time-Travel (`jj op log`, `jj undo`, `jj op restore`)** + non-interactive `jj split -m`, `jj squash --into <REV> -u`, `jj absorb`, and `jj converge --no-interactive`.

---

## 2. Inspecting the Flawed Baseline (`starter/noisy_roleplay_subagents.py`)

Inspect `starter/noisy_roleplay_subagents.py`. Notice four Layer-3 anti-patterns:
- **Parent Context Dumping**: Returns the entire 40,000-token raw grep log from the child subagent into the parent context window.
- **Unbounded Subagent Write Permissions**: Gives `code-explorer` and `code-reviewer` full `Edit` and `Bash` write access.
- **Un-anonymized Self-Bias**: Lets judge models see which model wrote each proposal during peer review.
- **Overlapping Worktree Edits**: Runs two parallel write subagents that both mutate `src/ledger.py`, causing guaranteed merge conflicts.

---

## 3. Step-by-Step Implementation (`subagent_council.py`)

Implement `subagent_council.py` satisfying `REQ-0701` through `REQ-0706`:
1. **`REQ-0701` (Subagent Context Firewall)**:
   - `execute_subagent_context_firewall(raw_search_traces, concise_findings, max_parent_tokens=600)` verifying `file:line` citations and `>= 0.90` parent token savings.
2. **`REQ-0702` (Read-Only Subagent Tool Boundary Validator)**:
   - `validate_subagent_tool_boundary(agent_role, requested_tools)` enforcing read-only tools (`Glob`, `Grep`, `Read`, `LSP`) for `code-explorer`, `code-architect`, and `code-reviewer`.
3. **`REQ-0703` (Stanford CS146S Multi-Agent PR Triage & $\ge 80$ Confidence Filter)**:
   - `ReviewFinding`, `TriageTier` (`MUST_FIX`, `RECOMMENDED`, `CONSIDER`), and `synthesize_pr_triage_report(findings, min_confidence=80)`.
4. **`REQ-0704` (Karpathy's `llm-council` Anonymizer & Borda Rank Aggregator)**:
   - `anonymize_council_responses(model_outputs)` and `aggregate_borda_rankings(ballots, label_to_model)`.
5. **`REQ-0705` (Workspace Isolation Mode Selector)**:
   - `select_workspace_isolation_mode(is_read_only_research, parallel_writers)` returning `"inherit"` or `"worktree"`.
6. **`REQ-0706` (Disjoint `git worktree` File-Ownership Validator)**:
   - `validate_disjoint_worktree_ownership(worktree_file_maps)` detecting overlapping file assignments across parallel worktrees.

---

## 4. Verification Command

```bash
./labs/lab_07_subagent_firewalls_and_peer_council/self_diagnose.sh
```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `.claude/agents/{code-explorer,code-architect,code-reviewer}.md`, `.claude/commands/feature-dev.md`, and `starter/noisy_roleplay_subagents.py`.
3. Verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_07_subagent_firewalls_and_peer_council/work/subagent_council.py` and `test_subagent_council.py`, then verify:
   ```bash
   ./labs/lab_07_subagent_firewalls_and_peer_council/self_diagnose.sh work
   ```
