# Lab 04 Walkthrough: Context Window Physics, The 40% "Dumb Zone" & Frequent Intentional Compaction (`TaskFlow` `RPI` Compaction Engine)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 03 $\to$ Lab 04)
In **Lab 03**, we structured `TaskFlow` feature development around the **5-Step `RePPIT` Workflow (`Research -> Propose -> Plan -> Implement -> Verify`)** and learned to purge rejected proposals so their tokens never pollute implementation. Now we generalize that insight into the fundamental law of **Context Window Physics**: because an LLM is a stateless function ($\text{NextAction} = \text{LLM}(\text{ContextWindow})$), what happens when noisy grep dumps, full file reads, and 5,000-line test logs push a `TaskFlow` coding session past **40% context utilization**?

### The Headache (Context Rot in the >40% "Dumb Zone" & Unbounded Stdout Flooding)
When a developer runs a long `TaskFlow` debugging session using [`starter/dumb_zone_session_accumulator.py`](./starter/dumb_zone_session_accumulator.py):
- **Unbounded Stdout Flooding:** Running test or training scripts with `| tee` dumps thousands of lines of progress bars directly into `history` instead of redirecting output to `run.log` (`> run.log 2>&1`) and grepping only the 2 summary metric lines.
- **Operating Deep in the >40% Dumb Zone:** Although frontier models advertise 200k–1M token windows, attention dilution pushes sessions past **40% utilization** from the **Smart Zone (`<= 40%`)** into the **Dumb Zone (`> 40%`)**, where the agent starts hallucinating `TaskFlow` function signatures and forgetting standing rules.
- **Citationless Auto-Compaction:** Waiting until 95% capacity triggers emergency summarization that strips exact `file.py:L10-L25` line citations, forcing the next session to re-grep the entire repository from scratch.

### The Everyday Metaphor (`Known -> Target`)
Think of **The 40% Dumb Zone & Frequent Intentional Compaction (`RPI`)** like **working at a physical desk covered in open reference books, sticky notes, and crumpled scratch paper** (*Known* $\to$ *Target*). Once more than 40% of your desk is buried under scratch paper (*Dumb Zone*), you spend all your mental energy hunting for the right page and making mistakes. **Frequent Intentional Compaction** means writing your verified measurements onto one clean index card with exact page numbers (`research.md` + `plan.md` with `file:L10-L25` citations) and sweeping the desk completely clear (`/clear` / `/compress`) before building the next part.

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/dumb_zone_session_accumulator.py`
Open [`starter/dumb_zone_session_accumulator.py`](./starter/dumb_zone_session_accumulator.py) (`lines 20–23`). Notice how `run_noisy_session()` blindly appends raw multi-thousand-line `raw_stdout` strings directly into `history` with zero backpressure or compaction.

### Implementing `context_compactor.py` (`REQ-0401` through `REQ-0406`)
Implement [`expected_output/context_compactor.py`](./expected_output/context_compactor.py) (or your custom `work/context_compactor.py`) to satisfy all 6 requirements for `TaskFlow`'s context compaction engine:

1. **`REQ-0401` (Context Window Profiler & 40% Dumb Zone Classifier)**:
   - Implement `ContextZone` (`SMART_ZONE`, `DUMB_ZONE`) and `profile_context_window(used_tokens, max_window_tokens=200_000, smart_zone_ceiling=0.40)` returning `ContextWindowProfile` with `requires_compaction = (utilization_ratio > smart_zone_ceiling)`.
2. **`REQ-0402` (`karpathy/autoresearch` Output-Redirection Backpressure)**:
   - Implement `rewrite_command_with_backpressure(command, log_file="run.log")` stripping `| tee ...` and appending `> run.log 2>&1`, plus `extract_backpressure_summary(raw_log_text, metric_prefixes, tail_lines_on_crash=20)` returning only matched metric lines on success or the last `tail_lines_on_crash` lines on crash.
3. **`REQ-0403` (Sandboxed Side-Query Pruning — `/btw` Pattern)**:
   - Implement `execute_sandboxed_side_query(active_history, question, answer)` returning the formatted side-query answer alongside an unchanged copy of `active_history` (zero token growth).
4. **`REQ-0404` (`karpathy/rendergit` CXML Repository Packer)**:
   - Implement `render_repo_cxml(files_dict)` packing source files into `<documents><document index="..."><source>...</source><document_content>...</document_content></document></documents>` while skipping ignored noise paths (`__pycache__`, `.git`, `node_modules`, `.venv`, `.pytest_cache`).
5. **`REQ-0405` (Frequent Intentional Compaction `RPI` Handoff Engine)**:
   - Implement `compact_exploration_to_rpi_artifacts(noisy_turns, verified_findings, plan_steps, out_of_scope)` validating that every finding and plan step carries a `file:L<line>` citation and producing `RpiHandoffBundle` with `compression_ratio >= 0.80`.
6. **`REQ-0406` (Human Leverage Pyramid Defect Amplification Estimator)**:
   - Implement `estimate_defect_amplification(stage, defective_lines)` quantifying downstream broken-code blast radius (`RESEARCH` = `1000x`, `PLAN` = `100x`, `CODE` = `1x`).

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_04_context_physics_and_rpi_compaction/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_04_context_physics_and_rpi_compaction/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"Because my model supports a 200,000-token context window, I don't need to compact or clear the session until the context meter hits 90%–95%."*
>
> **✓ Reality:** Dex Horthy's empirical harness analysis (`rmvDxxNubIg`) demonstrates that reasoning quality and instruction adherence degrade sharply once noisy tool outputs push utilization past **~40% (the "Dumb Zone")**. By practicing **Frequent Intentional Compaction (`RPI`)**—distilling findings into line-cited `research.md` and `plan.md` artifacts and resetting the session—you keep the agent operating inside the `< 40%` **Smart Zone** at all times.

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Predict-the-Outcome`):** Suppose a `TaskFlow` engineer introduces **2 defective lines** in `research.md` (misidentifying which module validates workspace permissions) versus **2 defective lines** in `plan.md` versus **2 defective lines** in final Python `CODE`. According to `estimate_defect_amplification(stage, defective_lines)`, how many downstream defective lines of code does each mistake produce, and why does `compact_exploration_to_rpi_artifacts()` raise a `ValueError` if a finding omits `:L<line>`?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect `LEVERAGE_MULTIPLIERS` and `CITATION_PATTERN` in [`expected_output/context_compactor.py`](./expected_output/context_compactor.py) (`lines 33` and `215–229`).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Multiply `defective_lines = 2` by each multiplier in `LEVERAGE_MULTIPLIERS`: `RESEARCH` (`1000`), `PLAN` (`100`), and `CODE` (`1`). Then check what `CITATION_PATTERN` (`[A-Za-z0-9_./-]+\.[A-Za-z0-9]+:L\d+`) requires on every item in `verified_findings + plan_steps`.
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
`estimate_defect_amplification` returns **`2000`** for `RESEARCH` (`2 * 1000`), **`200`** for `PLAN` (`2 * 100`), and **`2`** for `CODE` (`2 * 1`). Because `research.md` and `plan.md` carry `100x–1000x` leverage, `compact_exploration_to_rpi_artifacts()` strictly requires every finding and plan step to include a verifiable `file.ext:L<line>` citation (`CITATION_PATTERN`) so the fresh post-compaction agent can jump straight to the exact lines without re-searching the repo.
</details>

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
