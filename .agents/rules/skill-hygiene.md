---
trigger: model_decision
description: Apply when creating, editing, or evaluating agent skills (SKILL.md) to enforce progressive disclosure, Experience Before Theory, and the 2-3 skill sweet spot.
---

# Skill Engineering Hygiene Rule

- Author skills manually ("a conciencia") from observed baseline failure trajectories—never use self-generated training-data summaries (`SkillsBench` `arXiv:2602.12670`).
- Keep `SKILL.md` between `50` and `500` lines; offload deep reference tables into companion files (`docs.md`, `slides-deck.md`, `apply_template.md`, or `references/*.md`).
- Consolidate overlapping micro-skills so each task activates at most `2–3` focused outcome skills.
