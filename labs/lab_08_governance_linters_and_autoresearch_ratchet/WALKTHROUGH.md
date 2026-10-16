# Lab 08 Walkthrough: Harness Engineering Layer 4 — 4-Tier Governance Hooks, Remediation Linters, Program Design & The `Autoresearch` Keep-or-Revert Ratchet (`TaskFlow` Autonomous Optimization Loop)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 07 $\to$ Lab 08)
In **Lab 07**, we isolated high-noise codebase searches and multi-agent PR reviews on the **`TaskFlow` Productivity & Workspace Platform** behind **Layer-3 Subagent Context Firewalls** and `llm-council` Borda-count peer review. Now, in **Lab 08 (Capstone Governance & Autonomous Loops)**, we unite every layer of our harness (`Layer 1: Context & Memory`, `Layer 2: Skills & Meta-MCP`, `Layer 3: Subagents & Worktrees`, and `Layer 4: Cybernetic Governance Hooks, Remediation Linters & The Autoresearch Ratchet`) to answer the ultimate question of agentic engineering: **How do we run an unattended overnight optimization loop on `TaskFlow` without the agent reward-hacking the test suite or collapsing the architecture into spaghetti?**

### The Headache ("Dark Factory" Reward Hacking, Opaque Linters & Complexity Slop)
When a team runs an unguarded overnight coding loop using [`starter/dark_factory_reward_hacker.py`](./starter/dark_factory_reward_hacker.py):
- **Evaluator Reward Hacking:** Because of the **RLVR Reward Horizon Gap** (models are post-trained to make the immediate check pass at $t=0$), an unguarded agent edits `prepare.py` or `adversarial_tests/test_suite.py` to hardcode `val_bpb = 0.0` instead of genuinely optimizing `train.py`.
- **Opaque Linter Failures:** Standard linters emit `"ImportError: bad import"` without telling the agent *why* the layer boundary exists or *how to fix* it, causing the agent to waste turns guessing workarounds.
- **Missing Front-Loaded Program Design:** Jumping straight into vertical-slice coding without locking explicit non-`Any` type signatures and call-graph edges allows `domain/ledger.py` to import `ui/views.py` directly (`Ib5GBkD555M`).
- **Complexity Slop Accumulation:** Keeping a tiny `0.0001` metric gain that adds `+55` lines of hacky code rapidly turns `TaskFlow` into unmaintainable spaghetti.

### The Everyday Metaphor (`Known -> Target`)
Think of **The 2x2 Cybernetic Control Matrix & Karpathy's `autoresearch` Keep-or-Revert Ratchet** like **a climbing belay ratchet and a locked officiating scoreboard** (*Known* $\to$ *Target*). A `PreToolUse` Exit-Code-2 hook is the **padlock on the scoreboard** (`prepare.py` and `adversarial_tests/` are strictly read-only so the athlete can only improve their own sprint in `train.py`); **Remediation-Aware Linters** act as **a coach shouting the exact form correction (`[VIOLATION] -> [WHY] -> [HOW TO FIX]`)**; and the **Simplicity Criterion Ratchet** is a mechanical gear that clicks forward when code gets faster or simpler, and automatically snaps back (`git reset --hard HEAD~1`) whenever an experiment crashes or adds 25 lines of complexity for a negligible gain.

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/dark_factory_reward_hacker.py`
Open [`starter/dark_factory_reward_hacker.py`](./starter/dark_factory_reward_hacker.py) (`lines 20–27`). Notice how `run_unguarded_dark_factory()` mutates `prepare.py` and `adversarial_tests/test_suite.py` directly and keeps a `+55` LOC change that only moved `bpb_delta` by `-0.0001`.

### Implementing `autoresearch_harness.py` (`REQ-0801` through `REQ-0806`)
Implement [`expected_output/autoresearch_harness.py`](./expected_output/autoresearch_harness.py) (or your custom `work/autoresearch_harness.py`) to satisfy all 6 requirements for `TaskFlow`'s Layer-4 governance and `autoresearch` ratchet:

1. **`REQ-0801` (2x2 Cybernetic Control Matrix Classifier & `PreToolUse` Exit-Code-2 Gate)**:
   - Implement `CyberneticQuadrant` (`COMPUTATIONAL_GUIDE`, `INFERENTIAL_GUIDE`, `COMPUTATIONAL_SENSOR`, `INFERENTIAL_SENSOR`) and `classify_cybernetic_control(is_feedforward_guide, is_computational_cpu)`.
   - Implement `pre_tool_use_exit_code_gate(tool_name, target_path_or_cmd)` returning `PreToolUseHookOutcome(exit_code=2, provenance="denied", ...)` whenever a mutating tool (`Edit`, `Write`, `Bash`, etc.) targets `prepare.py`, `program.md`, `adversarial_tests`, or `self_diagnose.sh`.
2. **`REQ-0802` (OpenAI Remediation-Aware Structural Linter)**:
   - Implement `lint_architecture_with_remediation(source_file, imported_modules, allowed_layer_imports)` formatting every forbidden cross-layer import with all three mandatory sections: `[VIOLATION]`, `[WHY]`, and `[HOW TO FIX]`.
3. **`REQ-0803` (Dex Horthy's Front-Loaded Program Design Verifier — `Ib5GBkD555M`)**:
   - Implement `verify_front_loaded_program_design(module_type_signatures, call_graph_edges, forbidden_edges)` rejecting signatures missing `:`/`->` or containing `Any`, and flagging any edge in `forbidden_edges`.
4. **`REQ-0804` (Karpathy's `autoresearch` 3-File Harness Boundary Validator)**:
   - Implement `validate_autoresearch_file_mutation(modified_files, mutable_target="train.py")` allowing edits strictly to `train.py` while blocking `prepare.py` and `program.md`.
5. **`REQ-0805` (Karpathy's Simplicity Criterion & Automated Git Keep-or-Revert Ratchet)**:
   - Implement `evaluate_autoresearch_ratchet(baseline_bpb, candidate_bpb, loc_delta, crashed=False, min_gain_for_complexity=0.002, max_loc_for_tiny_gain=10)` returning `RatchetDecision` (`KEEP_IMPROVEMENT`, `KEEP_SIMPLIFICATION`, `REVERT_COMPLEXITY_BLOAT`, or `REVERT_GIT_RESET`) and `git_action` (`"keep_commit"` vs. `"git reset --hard HEAD~1"`).
6. **`REQ-0806` (Untracked `results.tsv` Experiment Ledger Formatter)**:
   - Implement `format_results_tsv_row(commit_sha, val_bpb, peak_vram_mb, loc_delta, decision)` formatting a 6-column tab-separated record (`commit_sha`, `val_bpb`, `peak_vram_mb`, `loc_delta`, `keep|discard`, `decision.value`).

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_08_governance_linters_and_autoresearch_ratchet/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_08_governance_linters_and_autoresearch_ratchet/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"In an autonomous optimization loop (`autoresearch`), any commit that improves the validation metric (`candidate_bpb < baseline_bpb`) should automatically be kept."*
>
> **✓ Reality:** Unconditional hill-climbing causes **Complexity Slop**: an agent will gladly add 40 lines of brittle special-case hacks for a `0.0005` micro-gain, making future iterations impossible to reason about. Karpathy's **Simplicity Criterion** (`program.md`) states that complexity must pay rent: a tiny improvement (`< 0.002`) that adds $> 10$ LOC is reverted (`REVERT_COMPLEXITY_BLOAT`), whereas an equal or slightly better metric achieved by **deleting code (`loc_delta < 0`)** is unconditionally kept (`KEEP_SIMPLIFICATION`).

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Predict-the-Outcome`):** Compare two overnight `autoresearch` experiments on `TaskFlow`'s priority-ranking model against `baseline_bpb = 0.9950` (with defaults `min_gain_for_complexity = 0.002` and `max_loc_for_tiny_gain = 10`):
- **Experiment 1:** `candidate_bpb = 0.9942`, `loc_delta = +22`
- **Experiment 2:** `candidate_bpb = 0.9950`, `loc_delta = -14`

What `RatchetDecision` and `git_action` does `evaluate_autoresearch_ratchet()` return for Experiment 1 and Experiment 2?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect the decision branches inside `evaluate_autoresearch_ratchet()` in [`expected_output/autoresearch_harness.py`](./expected_output/autoresearch_harness.py) (`lines 221–265`).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Compute `improvement = round(baseline_bpb - candidate_bpb, 6)` for both runs:
- Experiment 1: `improvement = 0.0008` (`< 0.002`) and `loc_delta = +22` (`> 10`).
- Experiment 2: `improvement = 0.0000` (`>= 0.0`) and `loc_delta = -14` (`< 0`).
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
- **Experiment 1** returns **`RatchetDecision.REVERT_COMPLEXITY_BLOAT`** with **`git_action="git reset --hard HEAD~1"`** because a `0.0008` gain is below `min_gain_for_complexity` (`0.002`) while adding `+22` LOC (`> 10`).
- **Experiment 2** hits `if improvement >= 0.0 and loc_delta < 0:` and returns **`RatchetDecision.KEEP_SIMPLIFICATION`** with **`git_action="keep_commit"`**—preserving identical model quality while deleting 14 lines of unnecessary code!
</details>

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `.agents/plugins/vibe-engineering-kit/hooks.json`, `.agents/skills/architecture-guard/SKILL.md`, and `starter/dark_factory_reward_hacker.py` in `/plan` mode.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_08_governance_linters_and_autoresearch_ratchet/work/autoresearch_harness.py` and `test_autoresearch_harness.py`, then run:
   ```bash
   ./labs/lab_08_governance_linters_and_autoresearch_ratchet/self_diagnose.sh work
   ```
