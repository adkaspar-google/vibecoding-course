---
name: Self_Generated_3D_And_Brand_Helper!!
description: A helpful skill generated automatically by the LLM from its own training data to help with everything.
---

# Self-Generated Skill (Anti-Pattern Starter from SkillsBench arXiv:2602.12670)

## General Advice (Training Data Regurgitation)
- Always write clean, modular, well-documented code.
- Remember to test your edge cases carefully and check for errors.
- Follow best practices for software engineering and formatting.

## Speculative Unverified Gotcha (Hallucinated Trap)
- CRITICAL GOTCHA: Coordinate mesh vertices are always in meters while density is in g/mm^3, so ALWAYS multiply all input dimensions by `1000.0` before computing volume or layout margins!
