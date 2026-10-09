# Architecture & Two-Phase Harness Topology (`@docs/architecture.md`)

Referenced on demand from `CLAUDE.md`, `GEMINI.md`, and `AGENTS.md` so architectural details load only when needed.

## 1. Phase 1 — Vibe Coding Foundations & Daily Workflows (`labs/lab_01_*` .. `labs/lab_04_*`)

1. **Lab 01 (`lab_01_vibe_coding_and_earned_autonomy`)**:
   Ubiquitous Language value objects (`AccountId`, `MoneyCents`), Andrew Ng's *AI Engineering Skills Map* Pillar 02 prompt steering (`latency_ms_p99`, `consistency_model`, `reliability_strategy`, `security_boundary`, `maintainability_contract`), and `andrewyng/openworker` 4-Tier Earned Autonomy (`agy` and `claude` permission modes, Hard Floors, Reviewer Circuit Breaker, Provenance Audit Trail).
2. **Lab 02 (`lab_02_agent_loop_and_harness_wire_trace`)**:
   `andrewyng/aisuite` 3-Layer Agent Stack, `Gather Context -> Take Action -> Verify Results` loop verification, Stanford CS146S Wireshark-style HTTP/JSONL payload inspection, and "Swiss Army Knife" primitive consolidation (`Bash`, `Read`, `Edit`, `Grep`, `LSP`) vs. 150-tool CRUD bloat.
3. **Lab 03 (`lab_03_reppit_workflow_and_reflection`)**:
   Stanford CS146S 5-step `RePPIT` workflow (`Research -> Propose -> Plan -> Implement -> Test/Verify`), Socratic `/grill-me` clarification gate, Orthogonal Proposals + Post-Proposal Context Reset, `Out of Scope / Do NOT Touch` plan guardrails, Phase-Based Model Routing, and `andrewyng/translation-agent` reflection (`Generate -> Reflect -> Refine`).
4. **Lab 04 (`lab_04_context_physics_and_rpi_compaction`)**:
   Dex Horthy's Context Window Physics (`Smart Zone <= 40%` vs. `Dumb Zone > 40%`), `karpathy/autoresearch` output-redirection backpressure (`> run.log 2>&1`), `/btw` sandboxed side-queries, `karpathy/rendergit` CXML packing, and Frequent Intentional Compaction (`RPI`) into line-cited `research.md` and `plan.md`.

## 2. Phase 2 — Harness Engineering & Agentic Loops (`labs/lab_05_*` .. `labs/lab_08_*`)

5. **Lab 05 (`lab_05_context_primitives_and_memory`)**:
   Layer 1 Harness Engineering: Three Context Primitives (`Prompts/Slash Commands`, `Rules`, `Skills`), the 150-Instruction Compliance Cliff, the Minimalist 60-Line Root Map (`CLAUDE.md` / `GEMINI.md` / `AGENTS.md`), and cross-session memory (`MEMORY.md` / `KNOWLEDGE.md`) with `#direct` vs. `#commit`/`#time`/`#session` provenance.
6. **Lab 06 (`lab_06_skills_chub_and_meta_mcp_code_mode`)**:
   Layer 2 Harness Engineering: `agentskills.io` 3-Level Progressive Disclosure, `andrewyng/context-hub` (`@aisuite/chub`) curated versioned docs + `chub annotate` self-improving session notes, Stanford CS146S Meta-MCP "Code Mode" (`search` + `execute` meta-tools with $\ge 90\%$ token savings), and `SkillsBench` (`arXiv:2602.12670`) evaluation.
7. **Lab 07 (`lab_07_subagent_firewalls_and_peer_council`)**:
   Layer 3 Harness Engineering: Subagents as Context Firewalls (`>=90%` parent token isolation), read-only `feature-dev` subagents (`code-explorer`, `code-architect`, `code-reviewer`), CS146S Multi-Agent PR Triage (`MUST_FIX` / `RECOMMENDED` / `CONSIDER` at $\ge 80$ confidence), Karpathy's `llm-council` anonymized Borda peer review, and disjoint `git worktree` ownership.
8. **Lab 08 (`lab_08_governance_linters_and_autoresearch_ratchet`)**:
   Layer 4 Harness Engineering: 2x2 Cybernetic Control Matrix, `PreToolUse` Exit-Code-2 hard-floor hooks, OpenAI remediation-aware structural linters (`[VIOLATION] -> [WHY] -> [HOW TO FIX]`), Dex Horthy's Front-Loaded Program Design verifier (`Ib5GBkD555M`), and Karpathy's `autoresearch` (`prepare.py` / `train.py` / `program.md`) Simplicity Criterion & Git Keep-or-Revert Ratchet.
