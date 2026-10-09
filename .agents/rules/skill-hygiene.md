---
trigger: model_decision
description: Apply when creating, editing, or evaluating agent skills (SKILL.md) to enforce 3-level progressive disclosure, curated skill authoring, and the 2-3 skill sweet spot.
---

# Skill Engineering Hygiene Rule

- Author skills from observed baseline failure trajectories—never rely on unverified self-generated training-data summaries (`SkillsBench` `arXiv:2602.12670`).
- Keep `SKILL.md` between `20` and `500` lines; offload deep reference tables and scripts into Level 3 companion files (`references/*.md`, `scripts/*.py`).
- Consolidate overlapping micro-skills so each task activates at most `2–3` focused outcome skills.
