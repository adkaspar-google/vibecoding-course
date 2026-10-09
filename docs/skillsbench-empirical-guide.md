# Empirical Science of Agent Skills (`@docs/skillsbench-empirical-guide.md`)

Referenced on demand from `CLAUDE.md` and `GEMINI.md` / `AGENTS.md`.

## 1. SkillsBench Findings (`arXiv:2602.12670v4`, Li et al., 2026)
- Evaluated across **87 tasks**, **8 domains**, and **9,396 agent trajectories**:
  - **No-Skills Baseline**: **33.9%** pass rate.
  - **Curated Human-Authored Skills ("A Conciencia")**: **50.5%** pass rate (**+16.6 pp average lift**; **+24.8 pp on Gemini CLI + Gemini 3.1 Pro**, **+18.2 pp on Claude Code + Opus 4.7**, up to **+67.0 pp** on procedural workflows).
  - **Self-Generated Skills Degrade Performance**: Having an agent generate its own skills before solving drops pass rate **below the No-Skills baseline** (**$-8.1\text{ pp}$ on Claude Code**, **$-11.3\text{ pp}$ on Codex**, **$-11.5\text{ pp}$ on Gemini CLI**) due to pretraining repetition and hallucinated unit-conversion traps (`3d-scan-calc` `1000x` bug).

## 2. Skill Count Overload & Complexity Sweet Spots (Tables 8 & 9)
- **Skill Count**: `1` skill = **+18.0 pp**, `2–3` skills = **+19.0 pp** (optimal sweet spot), `>= 4` skills = **+10.1 pp** (-8.9 pp routing confusion penalty).
- **Skill Length**: `Compact` = **+19.0 pp**, `Standard` = **+21.5 pp**, `Detailed` = **+14.5 pp**, `Comprehensive/Exhaustive` = **+0.7 pp**.
