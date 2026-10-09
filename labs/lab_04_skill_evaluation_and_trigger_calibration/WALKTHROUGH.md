# Lab 04: Evaluating Skills (`skill-creator` & `eval-viewer`), Solving Skill Overload & SDT Trigger Calibration

## 1. Learning Objectives & Empirical Grounding

1. **Paired `with_skill` vs. `without_skill` Evaluation (`skill-creator` & `eval-viewer`)**:
   - A skill's true value is $\Delta\text{PassRate} = \text{PassRate}_{\text{with}} - \text{PassRate}_{\text{without}}$.
   - Anthropic's `skill-creator` workflow spawns parallel `with_skill` and `without_skill` runs, grades assertions into `grading.json` (`{"expectations": [{"text", "passed", "evidence"}]}`), aggregates statistics into `benchmark.json`, and renders a static HTML review UI via `eval-viewer/generate_review.py` (`Outputs` tab + `Benchmark` tab).
2. **Why Adding More Skills Confuses the Agent (`SkillsBench` Table 8)**:
   - Empirical result from `SkillsBench` (`arXiv:2602.12670`):
     - `1` skill = **+18.0 pp** lift
     - `2–3` focused skills = **+19.0 pp** lift (optimal sweet spot)
     - `>= 4` skills = **+10.1 pp** lift (**-8.9 pp drop!**)
   - The more skills you add, the more the router struggles to decide *which* skill to invoke, *when*, and *why*.
   - **The Reference-First Defense**: Merge micro-skills ($<50$ lines) or sibling sub-workflows into `references/<subtopic>.md` inside a parent outcome skill—adding **0 startup tokens** and **0 extra routing targets**.
3. **Signal Detection Theory (SDT) Trigger Calibration**:
   - Using Hautus (1995) $+0.5$ smoothing on Hits ($H$), Misses ($M$), False Alarms ($FA$), and Correct Rejections ($CR$):
     $$d' = \Phi^{-1}(\text{HR}_{\text{adj}}) - \Phi^{-1}(\text{FA}_{\text{adj}}), \qquad c = -0.5\left(\Phi^{-1}(\text{HR}_{\text{adj}}) + \Phi^{-1}(\text{FA}_{\text{adj}})\right), \qquad U = 2.0 d' - 0.5|c - c_{\text{target}}|$$

---

## 2. Step-by-Step Implementation (`skill_eval_engine.py`)

Implement `skill_eval_engine.py` satisfying `REQ-0401` through `REQ-0406`:
1. **`REQ-0401` (`grade_trajectory_expectations`)**: Grade trajectory outputs into `grading.json` format (`text`, `passed`, `evidence`).
2. **`REQ-0402` (`aggregate_paired_benchmark`)**: Compute `with_skill` vs `without_skill` mean/stddev pass rate, token delta, and `POSITIVE_LIFT` vs `NOISE_OR_REGRESSION`.
3. **`REQ-0403` (`generate_eval_viewer_html`)**: Render a self-contained HTML viewer with `id='tab-outputs'` and `id='tab-benchmark'`.
4. **`REQ-0404` (`compute_sdt_trigger_metrics`)**: Compute Hautus-smoothed `hr_adj`, `fa_adj`, `d_prime`, `criterion_c`, and `utility_u`.
5. **`REQ-0405` (`consolidate_overloaded_skills`)**: Consolidate the 7 colliding skills in `starter/overloaded_skill_catalog.json` down to $\le 3$ outcome skills using `references/*.md`.

---

## 3. Verification Command

```bash
./labs/lab_04_skill_evaluation_and_trigger_calibration/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `starter/overloaded_skill_catalog.json` in `/plan` mode and design the consolidation into 3 parent skills.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and run the `/feature-dev` workflow to implement `work/skill_eval_engine.py` until `./labs/lab_04_skill_evaluation_and_trigger_calibration/self_diagnose.sh work` exits `0` without modifying `adversarial_tests/` or `expected_output/`.
5. Verify your deliverables in `work/`:
   ```bash
   ./labs/lab_04_skill_evaluation_and_trigger_calibration/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `starter/overloaded_skill_catalog.json` and review the `grading.json` and `benchmark.json` schemas from `skill-creator`.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and invoke `/feature-dev`:
   ```text
   /feature-dev Implement labs/lab_04_skill_evaluation_and_trigger_calibration/work/ until ./labs/lab_04_skill_evaluation_and_trigger_calibration/self_diagnose.sh work exits 0; do not modify any file under adversarial_tests/ or expected_output/.
   ```
5. Run targetable self-diagnosis:
   ```bash
   ./labs/lab_04_skill_evaluation_and_trigger_calibration/self_diagnose.sh work
   ```
