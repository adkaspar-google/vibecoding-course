# Lab 04: Context Window Physics, The 40% "Dumb Zone" & Frequent Intentional Compaction (`RPI`)

## 1. Learning Objectives & Conceptual Motivation

1. **Stateless LLM Physics & The 40% "Dumb Zone" (Dex Horthy, `rmvDxxNubIg`)**:
   At every step of an agentic loop, the model is a stateless function:
   $$\text{NextAction} = \text{LLM}(\text{ContextWindow})$$
   Although modern frontier models advertise 200k to 1M+ token context windows, **not all tokens are created equal**. As noisy grep dumps, full file reads, stack traces, and failed tool retries accumulate past **~40% context utilization**, attention dilution and conflicting historical instructions push the agent from the **Smart Zone (`0%–40%`)** into the **Dumb Zone (`>40%`)** ("Context Rot").

2. **Context Backpressure via Output Redirection (`karpathy/autoresearch` & `karpathy/rendergit`)**:
   - In `karpathy/autoresearch` (`program.md`), the agent is instructed:
     > *"Run `uv run train.py > run.log 2>&1` — redirect everything, do NOT use `tee` or let output flood your context. Read out results via `grep '^val_bpb:\|^peak_vram_mb:' run.log`."*
   - In `karpathy/rendergit`, repositories are flattened into a structured **LLM CXML View** (`<documents><document>...</document></documents>`) that strips build noise (`__pycache__`, `node_modules`, `.venv`).
   - For quick tangent questions during coding, Claude Code's `/btw` executes a **sandboxed side-query** whose tokens are immediately pruned from the main conversation history.

3. **Frequent Intentional Compaction (FIC), The `RPI` Loop & The Human Leverage Pyramid**:
   Instead of waiting for emergency auto-compaction at 95% capacity, disciplined engineers practice **Frequent Intentional Compaction** across the **RPI Loop (`Research -> Plan -> Implement`)**:
   - Distill a noisy 80,000-token exploration session into a 600-token `research.md` and `plan.md` on disk with exact `file.py:L10-L25` citations, then run `/clear` (or Antigravity `/compress` / new session) so implementation starts fresh in the **Smart Zone (`<10%` utilization)**.
   - **The Human Leverage Pyramid:** 1 bad line in `research.md` causes ~1,000 lines of broken code (`1000x` amplification); 1 bad line in `plan.md` causes ~100 lines of wasted code (`100x`); reviewing `research.md` and `plan.md` is the highest-leverage human activity in agentic engineering.

---

## 2. Inspecting the Flawed Baseline (`starter/dumb_zone_session_accumulator.py`)

Inspect `starter/dumb_zone_session_accumulator.py`. Notice three context-rot anti-patterns:
- **Unbounded Stdout Flooding**: Appends 5,000 lines of raw test/training progress bars directly into the message history (`tee`-style) instead of redirecting to `run.log`.
- **95% Auto-Compaction Waiting**: Continues generating code at 75% context utilization deep inside the Dumb Zone.
- **Citationless Summaries**: Compacts history into vague prose (`"checked some files in billing"`) that loses all `file.py:L10-L25` line numbers.

---

## 3. Step-by-Step Implementation (`context_compactor.py`)

Implement `context_compactor.py` satisfying `REQ-0401` through `REQ-0406`:
1. **`REQ-0401` (Context Window Profiler & 40% Dumb Zone Detector)**:
   - `ContextZone` (`SMART_ZONE`, `DUMB_ZONE`) and `profile_context_window(used_tokens, max_window_tokens=200_000, smart_zone_ceiling=0.40)`.
2. **`REQ-0402` (`karpathy/autoresearch` Output-Redirection Backpressure)**:
   - `rewrite_command_with_backpressure(command, log_file="run.log")` and `extract_backpressure_summary(raw_log_text, metric_prefixes, tail_lines_on_crash=20)`.
3. **`REQ-0403` (Sandboxed Side-Query Pruning — `/btw` Pattern)**:
   - `execute_sandboxed_side_query(active_history, question, answer)` returning the answer without mutating or growing `active_history`.
4. **`REQ-0404` (`karpathy/rendergit` CXML Repository Packer)**:
   - `render_repo_cxml(files_dict)` formatting source files into `<documents><document>...</document></documents>` while filtering out ignored noise paths.
5. **`REQ-0405` (Frequent Intentional Compaction `RPI` Engine)**:
   - `compact_exploration_to_rpi_artifacts(noisy_turns, verified_findings, plan_steps, out_of_scope)` producing line-cited `research_md` and `plan_md` with `>= 80%` token compression.
6. **`REQ-0406` (Human Leverage Pyramid Defect Amplification Estimator)**:
   - `estimate_defect_amplification(stage, defective_lines)` (`RESEARCH` = `1000x`, `PLAN` = `100x`, `CODE` = `1x`).

---

## 4. Verification Command

```bash
./labs/lab_04_context_physics_and_rpi_compaction/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Run `/stats` to inspect current context utilization, inspect `starter/dumb_zone_session_accumulator.py` in `/plan` mode, and practice `/compress` and `/clear`.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_04_context_physics_and_rpi_compaction/work/context_compactor.py` and `test_context_compactor.py`, then run:
   ```bash
   ./labs/lab_04_context_physics_and_rpi_compaction/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, run `/context` and `/btw` to observe how Claude Code tracks token utilization and sandboxed side-queries, then inspect `starter/dumb_zone_session_accumulator.py`.
3. Verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_04_context_physics_and_rpi_compaction/work/context_compactor.py` and `test_context_compactor.py`, then verify:
   ```bash
   ./labs/lab_04_context_physics_and_rpi_compaction/self_diagnose.sh work
   ```
