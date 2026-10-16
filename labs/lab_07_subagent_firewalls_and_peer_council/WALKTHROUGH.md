# Lab 07 Walkthrough: Harness Engineering Layer 3 — Subagents as Context Firewalls, Multi-Agent PR Triage & `llm-council` Peer Review (`TaskFlow` Multi-Agent Orchestration)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 06 $\to$ Lab 07)
In **Lab 06**, we built **Harness Engineering Layer 2** for the **`TaskFlow` Productivity & Workspace Platform**, using 3-level progressive-disclosure skills, `chub` self-annotating SDK docs, and **Meta-MCP "Code Mode"** (`search` + `execute`) to cut standing tool-schema overhead by $\ge 90\%$. Yet even with a lean standing harness, what happens when a single `TaskFlow` feature requires searching 40 repository files, reviewing a security-sensitive pull request across 5 specialist dimensions, or running parallel implementation agents across the workspace?

### The Headache (Noisy Roleplay Subagents, Unbounded Write Permissions & Worktree Collisions)
When a developer orchestrates subagents on `TaskFlow` using [`starter/noisy_roleplay_subagents.py`](./starter/noisy_roleplay_subagents.py):
- **Parent Context Dumping:** Instead of acting as a **Context Firewall**, the child subagent dumps 40,000 tokens of raw `Grep` output straight back into the parent session (`"\n".join(raw_grep_logs)`), immediately pushing the parent into the **$>40\%$ Dumb Zone**.
- **Unbounded Subagent Write Permissions:** Granting `code-explorer`, `code-architect`, or `code-reviewer` mutating tools (`Edit`, `Write`, `Bash`) allows a "review" subagent to silently modify `TaskFlow` source files mid-audit.
- **Un-Anonymized Self-Bias & Low-Confidence Review Noise:** Letting judge models see model names (`claude-opus-4-6`, `gemini-3.1-pro`) biases peer rankings toward their own model family, while emitting PR comments with `< 80` confidence floods developers with false-positive style nitpicks.
- **Overlapping Worktree Collisions:** Running two parallel write subagents in `git worktree` checkouts that both modify `src/shared.py` guarantees merge conflicts on integration.

### The Everyday Metaphor (`Known -> Target`)
Think of **Subagent Context Firewalls & `llm-council` Anonymized Peer Review** like **an appellate judge's law clerk and a double-blind academic peer review** (*Known* $\to$ *Target*). You never wheel 50 boxes of raw trial transcripts onto the judge's bench (*dumping raw grep logs into the parent context*); the law clerk reads all 50 boxes in a separate back room (*ephemeral child context window*) and hands the judge a **1-page memo with exact page-and-line citations** (`>= 90%` parent token savings), while double-blind review strips author names (`Response A`, `Response B`) before Borda-count ranking.

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/noisy_roleplay_subagents.py`
Open [`starter/noisy_roleplay_subagents.py`](./starter/noisy_roleplay_subagents.py) (`lines 20–22`). Notice how `run_leaky_subagent()` returns `"\n".join(raw_grep_logs)` directly to the caller without token bounds, `file:line` citations, or read-only tool enforcement.

### Implementing `subagent_council.py` (`REQ-0701` through `REQ-0706`)
Implement [`expected_output/subagent_council.py`](./expected_output/subagent_council.py) (or your custom `work/subagent_council.py`) to satisfy all 6 requirements for `TaskFlow`'s Layer-3 subagent and council harness:

1. **`REQ-0701` (Subagent Context Firewall)**:
   - Implement `execute_subagent_context_firewall(raw_search_traces, concise_findings, max_parent_tokens=600)` verifying that every finding includes a `file:L<line>` citation, `parent_summary_tokens_returned <= max_parent_tokens`, and `isolation_ratio >= 0.90`.
2. **`REQ-0702` (Read-Only Subagent Tool Boundary Validator)**:
   - Implement `validate_subagent_tool_boundary(agent_role, requested_tools)` restricting `code-explorer`, `code-architect`, and `code-reviewer` strictly to `READ_ONLY_TOOLS` (`{"Glob", "Grep", "Read", "LSP"}`).
3. **`REQ-0703` (Stanford CS146S Multi-Agent PR Triage & $\ge 80$ Confidence Filter)**:
   - Implement `ReviewFinding`, `TriageTier` (`MUST_FIX`, `RECOMMENDED`, `CONSIDER`), and `synthesize_pr_triage_report(findings, min_confidence=80)` dropping findings with `confidence < 80`, enforcing `file:line` citations, and setting `blocks_merge = (len(must_fix) > 0)`.
4. **`REQ-0704` (Karpathy's `llm-council` Anonymizer & Borda Rank Aggregator)**:
   - Implement `anonymize_council_responses(model_outputs)` mapping sorted models to `"Response A"`, `"Response B"`, ..., and `aggregate_borda_rankings(ballots, label_to_model)` scoring 1st place = $N$ points down to last place = $1$ point.
5. **`REQ-0705` (Workspace Isolation Mode Selector)**:
   - Implement `select_workspace_isolation_mode(is_read_only_research, parallel_writers)` returning `"inherit"` for read-only subagents (`parallel_writers == 0`) and `"worktree"` for parallel writers (or colocated Jujutsu `jj workspace add` workflows).
6. **`REQ-0706` (Disjoint `git worktree` File-Ownership Validator)**:
   - Implement `validate_disjoint_worktree_ownership(worktree_file_maps)` detecting any overlapping file paths across parallel worktrees.

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_07_subagent_firewalls_and_peer_council/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_07_subagent_firewalls_and_peer_council/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"Subagents should be designed around human job titles ('Product Manager Agent', 'UX Designer Agent', 'Frontend Engineer Agent') chatting back and forth in a shared conversation thread."*
>
> **✓ Reality:** Anthropomorphic roleplay in a shared thread multiplies token consumption and accelerates **Context Rot**. In production harness engineering (Dex Horthy & Anthropic `feature-dev`), a subagent is a **Context Firewall**: it runs high-noise search or specialist review inside an isolated child context window with strict tool permissions (`Read`/`Grep`/`Glob`/`LSP`) and returns only a compact, `file:line`-cited digest to the parent orchestrator.

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Predict-the-Outcome`):** Three models (`claude-opus-4-6`, `gemini-3.1-pro`, `gpt-5`) propose architectures for `TaskFlow`'s webhook queue and are anonymized via `anonymize_council_responses()` into `"Response A"`, `"Response B"`, and `"Response C"`. Three peer-review ballots are cast:
- Ballot 1: `["Response B", "Response A", "Response C"]`
- Ballot 2: `["Response B", "Response C", "Response A"]`
- Ballot 3: `["Response A", "Response B", "Response C"]`

What is the exact Borda count score for `"Response B"`, and which model wins in `aggregate_borda_rankings()`?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect how `anonymize_council_responses()` sorts `model_outputs.items()` (`lines 173–176`) and how `points = n_candidates - rank_idx` is accumulated in `aggregate_borda_rankings()` (`lines 203–205`) of [`expected_output/subagent_council.py`](./expected_output/subagent_council.py).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
With `n_candidates = 3`, rank index `0` (1st place) earns `3 - 0 = 3` points, rank index `1` (2nd place) earns `3 - 1 = 2` points, and rank index `2` (3rd place) earns `3 - 2 = 1` point. Sum the points for `"Response B"` across Ballots 1, 2, and 3.
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
Sorting model keys alphabetically maps `"claude-opus-4-6"` $\to$ `"Response A"`, `"gemini-3.1-pro"` $\to$ `"Response B"`, and `"gpt-5"` $\to$ `"Response C"`. Across the 3 ballots, `"Response B"` places 1st (`3` pts), 1st (`3` pts), and 2nd (`2` pts) for a total of **`8` Borda points** (vs. `6` for `"Response A"` and `4` for `"Response C"`), making **`"Response B"` (`"gemini-3.1-pro"`)** the winner.
</details>

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `.agents/agents/{code-explorer,code-architect,code-reviewer}.md`, `.agents/workflows/feature-dev.md`, and `starter/noisy_roleplay_subagents.py` in `/plan` mode.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_07_subagent_firewalls_and_peer_council/work/subagent_council.py` and `test_subagent_council.py`, then run:
   ```bash
   ./labs/lab_07_subagent_firewalls_and_peer_council/self_diagnose.sh work
   ```
