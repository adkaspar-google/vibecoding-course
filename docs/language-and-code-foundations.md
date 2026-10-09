# Language, Code & Software-Engineering Steering (`@docs/language-and-code-foundations.md`)

Referenced on demand from `CLAUDE.md`, `GEMINI.md`, and `AGENTS.md` for Module 1.1 conceptual foundations.

## 1. Why Natural Language Coordinates Code & Action
- **Wittgenstein's Two Theories of Language**:
  - **Early Wittgenstein (*Tractatus Logico-Philosophicus*, 1921) — Picture Theory**: Language as a strict, formal, 1-to-1 logical picture of facts—mirroring how compilers, static type systems, and deterministic unit tests evaluate formal source code.
  - **Late Wittgenstein (*Philosophical Investigations*, 1953) — Language as Tool & Action**: Natural language as a shared toolbox used between collaborators (the Builder and Assistant in `§2`) to coordinate actions within agreed rules (`Molino & Tagliabue, arXiv:2302.01570`; `Winograd & Flores, 1986`; `Wang, Liang, & Manning, ACL 2016, arXiv:1606.02447`).
- **Code as an Externalized Conceptual Model (Unmesh Joshi & Martin Fowler, *What Is Code?*, 2026)**:
  - Source code simultaneously instructs the machine and externalizes the team's **Ubiquitous Language**. Unchecked vibe coding accumulates **Cognitive Debt** when synonyms (`client_id`, `cust_acct`, `tx_amt`) and ungrounded assumptions proliferate across modules.

## 2. Andrew Ng's *AI Engineering Skills Map* (DeepLearning.AI, 2026)
- Synthesized from **>10,000 job postings** across 4 Pillars: (1) *Building & Deploying AI Applications*, (2) *Software Engineering Fundamentals*, (3) *Using Coding Agents*, and (4) *Shaping the Build*.
- **Why Pillar 02 (Software Engineering Fundamentals) Anchors Vibe Coding**: Without software engineering fundamentals, a developer cannot steer a coding agent across latency (`p99`), consistency (`STRONG` vs. idempotent eventual), reliability (retries, circuit breakers), security (input validation, least privilege), and maintainability (typed boundaries).
