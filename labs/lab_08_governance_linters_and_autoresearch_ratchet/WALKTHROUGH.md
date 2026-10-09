# Lab 08: Harness Engineering Layer 4 — 4-Tier Governance Hooks, Remediation Linters, Program Design & The `Autoresearch` Keep-or-Revert Ratchet

## 1. Learning Objectives & Conceptual Motivation

1. **The 2x2 Cybernetic Control Matrix (`martinfowler.com` — Böckeler & Morris)**:
   Every control in an agent harness falls along two axes: **Timing** (*Guides [Feedforward]* before action vs. *Sensors [Feedback]* after action) and **Mechanism** (*Computational [Deterministic CPU]* vs. *Inferential [Semantic LLM]*):
   - **Computational Guide**: Sandbox allowlists, `PreToolUse` Exit-Code-2 hard-floor hooks, static type definitions.
   - **Inferential Guide**: `CLAUDE.md` / `GEMINI.md`, `SKILL.md`, `program.md` ("research org code").
   - **Computational Sensor**: Unit tests (`self_diagnose.sh`), structural AST linters, `prepare.py` (`evaluate_bpb`).
   - **Inferential Sensor**: Multi-agent `code-reviewer`, `llm-council` peer review, LLM-as-a-judge.

2. **Remediation-Aware Architectural Linters (OpenAI *Harness Engineering*)**:
   Standard compiler errors tell a human *what* broke; **Remediation-Aware Linters** write error messages directly for the coding agent's context window using a 3-part contract:
   ```text
   [VIOLATION] Domain module 'domain/ledger.py' imports infrastructure module 'infra/http_client'.
   [WHY] Domain logic must remain pure and deterministic without network I/O coupling.
   [HOW TO FIX] Inject a typing.Protocol interface defined in 'domain/ports.py' instead.
   ```

3. **Why "Lights-Off" Software Factories Fail & Front-Loaded Program Design (Dex Horthy, `Ib5GBkD555M`)**:
   Why do fully autonomous "dark software factories" collapse under technical debt after ~8 weeks? Because of the **RLVR Reward Horizon Gap**: models are post-trained to make unit tests pass at $t=0$, not to preserve architectural coherence at $t=6\text{ months}$. Deterministic harnesses **raise the floor**, but humans must **raise the ceiling** via **4-Phase Front-Loaded Alignment**:
   $$\text{Product} \longrightarrow \text{Architecture} \longrightarrow \text{Program Design (Types, Interfaces, Call-Trees)} \longrightarrow \text{Vertical Slices}$$

4. **Karpathy's `autoresearch` & `program.md` Keep-or-Revert Ratchet (`github.com/karpathy/autoresearch`)**:
   In `karpathy/autoresearch`, autonomous overnight improvement works because the harness enforces a strict **3-File Separation** and **Simplicity Criterion**:
   - **`prepare.py` (Immutable Evaluation Sensor)**: Read-only ground-truth evaluator (`evaluate_bpb`). The agent is strictly forbidden from editing `prepare.py`.
   - **`train.py` (Bounded Mutable Action Space)**: The single file the agent edits per experiment.
   - **`program.md` (Human-Authored "Research Org Code")**: Defines the loop rules and the **Simplicity Criterion**:
     > *"All else being equal, simpler is better. A 0.001 val_bpb improvement that adds 20 lines of hacky code? Probably not worth it. A 0.001 val_bpb improvement from deleting code? Definitely keep."*

---

## 2. Inspecting the Flawed Baseline (`starter/dark_factory_reward_hacker.py`)

Inspect `starter/dark_factory_reward_hacker.py`. Notice four Layer-4 failure modes:
- **Reward Hacking the Evaluator**: Modifies `prepare.py` and `adversarial_tests/` to return a fake `val_bpb = 0.0` instead of improving `train.py`.
- **Opaque Linter Errors**: Emits `"ImportError: bad import"` with zero `[WHY]` or `[HOW TO FIX]` remediation instructions.
- **Unchecked Architectural Spaghetti**: Allows `domain/` modules to import `ui/` and `infra/` directly without Program Design call-graph verification.
- **Complexity Slop Accumulation**: Keeps a `0.0005` metric tweak that adds `+45` lines of brittle spaghetti code.

---

## 3. Step-by-Step Implementation (`autoresearch_harness.py`)

Implement `autoresearch_harness.py` satisfying `REQ-0801` through `REQ-0806`:
1. **`REQ-0801` (2x2 Cybernetic Matrix Classifier & `PreToolUse` Exit-Code-2 Gate)**:
   - `CyberneticQuadrant` and `classify_cybernetic_control(is_feedforward_guide, is_computational_cpu)`; `pre_tool_use_exit_code_gate(tool_name, target_path)` returning exit code `2` when an agent attempts to mutate `prepare.py`, `program.md`, or `adversarial_tests/`.
2. **`REQ-0802` (OpenAI Remediation-Aware Structural Linter)**:
   - `lint_architecture_with_remediation(source_file, imported_modules, allowed_layer_imports)` formatting violations with `[VIOLATION]`, `[WHY]`, and `[HOW TO FIX]`.
3. **`REQ-0803` (Front-Loaded Program Design Verifier — `Ib5GBkD555M`)**:
   - `verify_front_loaded_program_design(module_type_signatures, call_graph_edges, forbidden_edges)` verifying typed signatures and call-tree edges before vertical-slice coding.
4. **`REQ-0804` (`autoresearch` 3-File Harness Boundary Validator)**:
   - `validate_autoresearch_file_mutation(modified_files)` allowing mutations only to `train.py` and blocking `prepare.py` and `program.md`.
5. **`REQ-0805` (`autoresearch` Simplicity Criterion & Git Keep-or-Revert Ratchet)**:
   - `evaluate_autoresearch_ratchet(baseline_bpb, candidate_bpb, loc_delta, crashed=False, min_gain_for_complexity=0.002, max_loc_for_tiny_gain=10)` returning `KEEP_IMPROVEMENT`, `KEEP_SIMPLIFICATION`, `REVERT_COMPLEXITY_BLOAT`, or `REVERT_GIT_RESET`.
6. **`REQ-0806` (`results.tsv` Experiment Ledger Formatter)**:
   - `format_results_tsv_row(commit_sha, val_bpb, peak_vram_mb, loc_delta, decision)` formatting a deterministic tab-separated experiment record.

---

## 4. Verification Command

```bash
./labs/lab_08_governance_linters_and_autoresearch_ratchet/self_diagnose.sh
```

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

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `.claude-plugin/plugin.json`, `.claude/skills/architecture-guard/SKILL.md`, and `starter/dark_factory_reward_hacker.py`.
3. Verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_08_governance_linters_and_autoresearch_ratchet/work/autoresearch_harness.py` and `test_autoresearch_harness.py`, then verify:
   ```bash
   ./labs/lab_08_governance_linters_and_autoresearch_ratchet/self_diagnose.sh work
   ```
