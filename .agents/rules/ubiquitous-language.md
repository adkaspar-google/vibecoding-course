---
trigger: always_on
description: Enforces Ubiquitous Language integer-cent money invariants and Socratic clarification gates across all labs.
---

# Ubiquitous Language & Clarification Gate Rule

- Always represent monetary values as exact integer minor units (`MoneyCents`), never `float`.
- When domain terms drift (`client_id`, `tx_amt`) or required parameters are missing, ask explicit clarifying questions (`/grill-me`) instead of guessing defaults.
