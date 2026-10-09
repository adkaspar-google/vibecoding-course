# Lab 03: Crafting `agentskills.io` Skills Manually ("A Conciencia"), Progressive Disclosure & The Self-Generated Skill Trap

## 1. Learning Objectives & Empirical Grounding (`SkillsBench` `arXiv:2602.12670`)

1. **Skills Are Procedural Instruction Manuals for AI**:
   - A skill is a directory anchored by `SKILL.md` that can be invoked manually via `/skillname` (e.g., `/anthropic-brand`) or loaded automatically when the task matches its `description`.
2. **Why Human-Crafted Skills ("A Conciencia") Dramatically Outperform Self-Generated Skills (`SkillsBench`, Li et al., 2026)**:
   - Across 87 benchmark tasks and 9,396 trajectories:
     - **Human-Curated Skills**: Boost pass rate from **33.9% to 50.5% (+16.6 pp average lift; +24.8 pp on Gemini CLI, +18.2 pp on Claude Code, and up to +67.0 pp on procedural tasks)**.
     - **Self-Generated Skills Decrease Performance**: Asking an LLM to generate its own skill before solving drops pass rates **below the No-Skills baseline** (**$-8.1\text{ pp}$ on Claude Code + Opus 4.7**, **$-11.3\text{ pp}$ on Codex**, **$-11.5\text{ pp}$ on Gemini CLI + Gemini 3.1 Pro**).
   - **Root Cause**: Self-generated skills repeat generic training-data advice (`"write clean code"`) or lock in hallucinated "gotchas" (like SkillsBench's `3d-scan-calc` failure where a self-generated skill hardcoded a false `1000.0x` millimeter conversion).
   - **Experience Before Theory (`skill-creator`)**: Always run the prompt zero-shot *first*, observe real failure trajectories, and write only the **Minimal Prescriptive Delta**.
3. **3-Level Progressive Disclosure (`agentskills.io` Specification)**:
   - **Level 1 (Metadata, `~100 tokens`)**: `name` (`^[a-z0-9]+(-[a-z0-9]+)*$`) + `description` ($\le 1024$ chars, with `Use when...` and `Don't use for...`).
   - **Level 2 (`SKILL.md` body, `50–500 lines`)**: Core tokens and routing table loaded when `/anthropic-brand` is invoked.
   - **Level 3 (On-Demand References, `0 startup tokens`)**: Companion files `docs.md`, `slides-deck.md`, and `apply_template.md` loaded only when needed.

---

## 2. Step-by-Step Implementation

1. Create the multi-file skill directory `anthropic-brand/` containing:
   - `SKILL.md` (50–500 lines, compliant YAML frontmatter, core brand tokens, experience-grounded contrast & `pt`-unit guardrails, and progressive disclosure router).
   - `docs.md` (document geometry & typography rules).
   - `slides-deck.md` (`16:9` widescreen slide deck rules).
   - `apply_template.md` (deterministic step-by-step branding procedure).
2. Implement `skill_validator.py` satisfying `REQ-0301` through `REQ-0305`:
   - `validate_skill_package(skill_dir)`
   - `compute_progressive_disclosure_budget(skill_dir, active_reference)`
   - `audit_skill_quality_delta(skill_markdown, observed_baseline_failures)`
   - `apply_brand_profile(draft, artifact_type)`

---

## 3. Verification Command

```bash
./labs/lab_03_crafting_agent_skills_progressive_disclosure/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `starter/self_generated_skill/SKILL.md` in `/plan` mode and identify the `agentskills.io` frontmatter violations and the `1000.0x` hallucinated unit-conversion trap.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and run the `/feature-dev` workflow to implement `work/skill_validator.py` and `work/anthropic-brand/` until `./labs/lab_03_crafting_agent_skills_progressive_disclosure/self_diagnose.sh work` exits `0` without modifying `adversarial_tests/` or `expected_output/`.
5. Verify your deliverables in `work/`:
   ```bash
   ./labs/lab_03_crafting_agent_skills_progressive_disclosure/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `starter/self_generated_skill/SKILL.md` and plan the `anthropic-brand/` (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) directory and `skill_validator.py`.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and invoke `/feature-dev`:
   ```text
   /feature-dev Implement labs/lab_03_crafting_agent_skills_progressive_disclosure/work/ until ./labs/lab_03_crafting_agent_skills_progressive_disclosure/self_diagnose.sh work exits 0; do not modify any file under adversarial_tests/ or expected_output/.
   ```
5. Run targetable self-diagnosis:
   ```bash
   ./labs/lab_03_crafting_agent_skills_progressive_disclosure/self_diagnose.sh work
   ```
