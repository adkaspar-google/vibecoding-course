---
trigger: always_on
description: Enforces Ubiquitous Language integer-cent money invariants and Wittgensteinian epistemic honesty gates across all labs.
---

# Ubiquitous Language & Epistemic Honesty Rule

- Always represent monetary values as exact integer minor units (`MoneyCents`), never `float`.
- When domain terms drift (`client_id`, `tx_amt`) or required FX rates are missing, return `CLARIFICATION_REQUIRED` with explicit coworker-style clarifying questions instead of guessing defaults.
