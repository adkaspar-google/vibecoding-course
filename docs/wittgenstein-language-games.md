# Philosophy of Code & Wittgensteinian Language Games (`@docs/wittgenstein-language-games.md`)

Referenced on demand from `CLAUDE.md` and `GEMINI.md` / `AGENTS.md`.

## 1. Code as Conceptual Model (Unmesh Joshi & Martin Fowler, 2026)
- Source: *What Is Code?* (`martinfowler.com/articles/what-is-code.html`).
- As LLMs reduce the cost of generating syntax, the primary bottleneck shifts to making the **conceptual model explicit**, discovering the right **domain vocabulary**, and preventing **Cognitive Debt** (synonym drift and ungrounded abstractions).

## 2. Wittgenstein's Language Games & Epistemic Honesty
- **SciTePress IESD 2025 (Paper 139777, Z. He)**: Synthesizes Wittgenstein's *Language Games* (meaning is use within shared engineering rules) and Heidegger's *Being-in-the-world* (situated tool understanding).
- **MaKTO (`arXiv:2501.14225`, Ye et al., 2025)**: Multi-agent KTO grounded in Wittgenstein's *Philosophical Investigations*, achieving a **61% win rate** (**+23.0% over GPT-4o**, **+10.9% over two-stage RL**, **49% Turing blind rate**).
- **Marco Graziano (`LGDL`, 2025)**: By Wittgenstein's *Private Language Argument*, statistical token continuation lacks an internal criterion of correctness. Bounding agents in explicit Language-Games with confidence thresholds enforces **Epistemic Honesty** (`GROUNDED_EXECUTE` vs `CLARIFICATION_REQUIRED` vs `ESCALATE_OUT_OF_BOUNDS`).
- **Coworker Communication Principle**: Talk to AI the same way we talk to human coworkers—onboarding them with shared domain vocabulary, progressive context, and explicit clarification gates.
