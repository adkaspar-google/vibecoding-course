---
paths:
  - "labs/**/*.py"
---

# Ubiquitous Language & Clarification Gate Rule

- Always represent monetary values as exact integer minor units (`MoneyCents`), never `float`.
- When domain terms drift (`client_id`, `tx_amt`) or required parameters are missing, ask explicit clarifying questions instead of guessing defaults.
