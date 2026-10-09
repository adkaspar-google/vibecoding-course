# Speaker Notes: From Vibe Coding to Agentic Engineering (`agy` & `claude`)

Complete tripartite speaker notes (`PURPOSE`, `VERBAL SCRIPT`, `TRANSITION`) for all **36 slides** across **7 modules**, covering the foundational philosophy of code, Wittgenstein's language games, persistent project context, cross-session auto-memory, crafting `agentskills.io` skills manually ("a conciencia"), `eval-viewer` & Signal Detection Theory trigger calibration, multi-agent `feature-dev` orchestration, versioned plugins with MCP & `PreToolUse` hooks, and the graduation bridge to Spec-Driven Development (`SDD-Crash-Course`).

---

## Module 01: Foundations, Conceptual Models & Dual-Branch Architecture (Slides 01–06)

### Slide 01 — From Vibe Coding to Agentic Engineering (`agy` & `claude`)
- **PURPOSE:** Introduce the prerequisite course preceding `SDD-Crash-Course` and establish its three architectural pillars across both the `agy` (Antigravity / Gemini CLI) and `claude` (Claude Code) branches.
- **VERBAL SCRIPT:** Welcome to From Vibe Coding to Agentic Engineering. This course is designed as the foundational prerequisite right before our Spec-Driven Development course, and the repository ships with two complete, one-to-one Git branches: the `agy` branch for Antigravity and Gemini CLI, and the `claude` branch for Claude Code. Across seven modules and six self-diagnosing Python labs, we move from naive vibe coding to disciplined agentic engineering across three pillars: first, grounding code as a model of understanding and bounding agents in Wittgensteinian language games; second, engineering persistent context, cross-session auto-memory, and manually crafted skills; and third, orchestrating multi-agent feature development, versioned plugins, and the escalation bridge to Spec-Driven Development.
- **TRANSITION:** Let's begin on Slide 2 with Unmesh Joshi's foundational question, published on Martin Fowler's site: What is code in the LLM era?

### Slide 02 — Unmesh Joshi's "What Is Code?" (May 2026): Code as a Model of Understanding
- **PURPOSE:** Contrast naive "Ralph Wiggum" vibe coding and Cognitive Debt against Unmesh Joshi's thesis (published on martinfowler.com) that code is primarily an explicit model of understanding.
- **VERBAL SCRIPT:** In his landmark essay What Is Code, published on Martin Fowler's site, Unmesh Joshi explains why cheaper LLM syntax generation makes software engineering discipline more critical, not less. When developers treat an LLM as a black box and passively review diffs just to see if a demo runs, they accumulate massive Cognitive Debt: across three prompts, the agent invents conflicting synonyms like `client_id` and `cust_acct`, uses floating-point numbers for money, and silently guesses missing exchange rates. Joshi reminds us that we are not meant to be passive reviewers of generated code; the act of writing and structuring code is itself part of our thinking. Our primary job is making the conceptual model explicit and refining our Ubiquitous Language through feedback.
- **TRANSITION:** Why does shared vocabulary matter so much when collaborating with an AI? Slide 3 grounds this in Ludwig Wittgenstein's philosophy of language.

### Slide 03 — Grounding AI with Wittgenstein: From Language Games to Epistemic Honesty
- **PURPOSE:** Connect Wittgenstein's *Language Games* (*Sprachspiele*), Heidegger's *Being-in-the-world*, MaKTO (`arXiv:2501.14225`), and Marco Graziano's Epistemic Honesty (`LGDL`) to how we communicate with coding agents.
- **VERBAL SCRIPT:** Three recent research works connect Ludwig Wittgenstein's Philosophical Investigations directly to agentic coding. First, situated language-game research shows that words do not carry meaning through static dictionary lookup; meaning arises only from rule-governed use inside a community. Second, the MaKTO framework on arXiv proves that aligning multi-agent language expression with state-action values achieves a 61 percent win rate, a 23 percent relative improvement over GPT-4o, and wins 60 percent of its games against human experts. Third, Marco Graziano's Language-Game Description Language applies Wittgenstein's Private Language Argument to enforce Epistemic Honesty: when a prompt is grounded in shared vocabulary with confidence at least 0.85, the agent executes; when a term or exchange rate is missing, the agent pauses and asks coworker-style clarifying questions instead of guessing.
- **TRANSITION:** How do we structure our engineering loop around these grounded agents? Let's look at Kief Morris's Why Loop and How Loops on Slide 4.

### Slide 04 — Humans and Agents in Software Engineering Loops (Kief Morris, martinfowler.com, Mar 2026)
- **PURPOSE:** Explain Kief Morris's separation of the human-owned "Why Loop" from the nested agent "How Loops" and introduce the "On-the-Loop" Harness Flywheel.
- **VERBAL SCRIPT:** In Humans and Agents in Software Engineering Loops, Kief Morris distinguishes between being In-the-Loop, where a human bottlenecks every line of generated code, and being On-the-Loop, where the human owns the Why Loop and engineers the harness governing the agent's nested How Loops. The Human Why Loop frames business value and Ubiquitous Language. The Outer How Loop sets persistent context and auto-memory. The Middle How Loop provides curated skills and multi-agent orchestration. And the Inner How Loop runs fast TDD generation against immutable verifiers. Whenever a defect escapes the Inner Loop, we don't just patch the code line—we upgrade the harness so that entire error class never happens again.
- **TRANSITION:** Let's see on Slide 5 how those exact harness layers map one-to-one between the `claude` branch and the `agy` branch.

### Slide 05 — 1-to-1 Architectural Parity: `claude` Branch vs. `agy` Branch
- **PURPOSE:** Walk through the exact file-by-file architectural correspondence between the `claude` branch (Claude Code) and the `agy` branch (Antigravity / Gemini CLI).
- **VERBAL SCRIPT:** Every concept in this course is portable across coding harnesses. On the `claude` branch, persistent project context lives in a concise 40-line `CLAUDE.md` with `@docs` imports and `.claude/rules`; auto-memory lives in `~/.claude/projects/<repo>/memory/MEMORY.md`; skills live in `.claude/skills/anthropic-brand/`; and multi-agent workflows use `.claude/agents` and `.claude-plugin/plugin.json`. On the `agy` branch, persistent context lives in `GEMINI.md`, `AGENTS.md`, and `.agents/rules`; cross-session knowledge lives in `~/.gemini/antigravity/knowledge/<project>/KNOWLEDGE.md` with `scope: workspace` and `#direct` provenance tags; and skills, subagents, workflows, and plugins live under `.agents/`. Both branches are verified by automated track tests.
- **TRANSITION:** Let's look at Slide 6 to see the six hands-on Python labs you will run and verify in under one second.

### Slide 06 — The 6 Self-Diagnosing Python Labs (`./self_diagnose_all.sh` in `< 1s`)
- **PURPOSE:** Preview the six progressive Python engineering labs and how `./self_diagnose_all.sh` grades them deterministically.
- **VERBAL SCRIPT:** Our repository includes six progressive, zero-dependency Python labs. Lab 1 builds Ubiquitous Language value objects and a Wittgensteinian epistemic confidence gate. Lab 2 builds a root context auditor and git-worktree auto-memory compiler. Lab 3 builds an `agentskills.io` validator and the multi-file `anthropic-brand` skill. Lab 4 builds a paired `eval-viewer` benchmark engine, skill overload detector, and Signal Detection Theory calibrator. Lab 5 builds the 7-phase `feature-dev` multi-agent orchestrator. And Lab 6 packages versioned plugins, MCP tools, `PreToolUse` hooks, and the escalation router to Spec-Driven Development. Running `./self_diagnose_all.sh` verifies all six labs and 54 tests in under a tenth of a second.
- **TRANSITION:** Let's dive into Module 2 on Slide 7 and walk through Lab 1 step by step.

---

## Module 02: Lab 01 Step-by-Step — Vocabulary & Bounded Language Games (Slides 07–11)

### Slide 07 — Lab 01 Problem: The "Vibe-Coded" Payments Ledger Disaster
- **PURPOSE:** Inspect the broken vibe-coded starter in `labs/lab_01_vocabulary_and_bounded_language_games/starter/domain_ledger.py` and identify its three failure modes.
- **VERBAL SCRIPT:** Let's open Lab 1. In `starter/domain_ledger.py`, an ungrounded vibe-coded script tries to settle payment batches using raw dictionaries and floats. First, it suffers from synonym soup, accepting `acct`, `client_id`, `cust_acct`, or `user_id` interchangeably with zero format validation. Second, it converts monetary amounts to IEEE-754 floats, introducing classic floating-point rounding drift across fee allocations. Third, when asked to settle a cross-currency transfer from Japanese Yen to US Dollars without a known exchange rate, it silently guesses a fallback rate of 1.0! If you run Lab 1's `self_diagnose.sh` against the starter folder, it immediately fails.
- **TRANSITION:** Let's fix the first two failure modes on Slide 8 by encoding our Ubiquitous Language into frozen value objects.

### Slide 08 — Lab 01 Step 1 (`REQ-0101..0102`): Ubiquitous Language Value Objects
- **PURPOSE:** Walk through implementing `AccountId`, `MoneyCents`, and deterministic half-up integer basis-point fee allocation (`REQ-0101` and `REQ-0102`).
- **VERBAL SCRIPT:** In Step 1 of Lab 1, we replace untyped dictionaries and floats with frozen dataclasses that enforce our Ubiquitous Language at construction time. `AccountId` validates the canonical pattern `ACCT-` followed by 4 to 12 uppercase alphanumeric characters, rejecting synonym drift with `DomainVocabularyError`. `MoneyCents` requires an exact integer `amount_cents`—explicitly rejecting both `float` and Python's `bool` subtype—alongside a validated ISO currency code. For fee calculations in `allocate_fee_bps`, we use exact integer basis-point math: `(amount_cents * fee_bps + 5000) // 10000`, guaranteeing that net amount plus fee equals the original amount to the exact cent.
- **TRANSITION:** Next, on Slide 9, let's enforce double-entry conservation across an entire settlement batch.

### Slide 09 — Lab 01 Step 2 (`REQ-0103`): Bounded-Context Double-Entry Conservation
- **PURPOSE:** Explain how `LedgerPosting` and `SettlementBatch.apply_postings()` enforce double-entry conservation and prevent overdrafts without mutating caller state (`REQ-0103`).
- **VERBAL SCRIPT:** In Step 2, we model valid moves inside our bounded context using `LedgerPosting` and `SettlementBatch`. Every `LedgerPosting` requires distinct debit and credit `AccountId` instances, a strictly positive `MoneyCents` amount, and a non-empty audit narrative. When `SettlementBatch.apply_postings` executes, it works on a copy of the account balances, verifies that every posting matches the batch currency, checks that no debit causes a negative balance, and asserts that total integer cents before the batch equal total integer cents after the batch. If any invariant fails, it raises `LedgerConservationError` without mutating the caller's dictionary.
- **TRANSITION:** What if the user's natural-language request is ambiguous or missing an exchange rate? Slide 10 implements our Wittgensteinian Epistemic Gate.

### Slide 10 — Lab 01 Step 3 (`REQ-0104..0105`): Wittgensteinian Epistemic Confidence Gate
- **PURPOSE:** Show how `evaluate_language_game_move()` computes grounding confidence and routes between `GROUNDED_EXECUTE`, `CLARIFICATION_REQUIRED`, and `ESCALATE_OUT_OF_BOUNDS`.
- **VERBAL SCRIPT:** In Step 3, we implement Marco Graziano's Wittgensteinian Epistemic Confidence Gate in `evaluate_language_game_move`. First, if a request attempts a prohibited policy action like `override_audit` or `bypass_conservation`, confidence drops to zero and the gate returns `ESCALATE_OUT_OF_BOUNDS`. Second, if the request uses ungrounded synonym keys like `client_id` or `tx_amt`, passes a float amount, or requests a cross-currency settlement whose currency pair is missing from `known_fx_basis_points`, confidence drops below the 0.85 threshold and the gate returns `CLARIFICATION_REQUIRED` with explicit coworker-style questions. Only fully grounded requests with confidence at least 0.85 return `GROUNDED_EXECUTE`.
- **TRANSITION:** Let's run Lab 1's self-diagnosis script on Slide 11 to verify our implementation against both unit and adversarial tests.

### Slide 11 — Lab 01 Step 4 (`REQ-0106`): Self-Diagnosis & Adversarial Verification
- **PURPOSE:** Demonstrate running `./labs/lab_01.../self_diagnose.sh` and explain what the read-only `adversarial_tests/` suite verifies.
- **VERBAL SCRIPT:** In Step 4, we run `./labs/lab_01_vocabulary_and_bounded_language_games/self_diagnose.sh`. The script runs two verification stages: first, our six unit tests in `test_domain_ledger.py`, and second, the locked adversarial verifier in `adversarial_tests/test_domain_ledger_verifier.py`. Notice what the adversarial suite catches: it tests whether passing `True` as `amount_cents` sneaks past `isinstance(x, int)`, verifies that failed settlement batches never mutate the caller's input balances dictionary, and confirms that cross-currency JPY-to-USD transfers never guess a 1.0 exchange rate. All nine test suites pass in under 20 milliseconds.
- **TRANSITION:** With Lab 1 complete, let's move to Module 3 on Slide 12 and tackle persistent context and cross-session auto-memory in Lab 2.

---

## Module 03: Lab 02 Step-by-Step — Persistent Context & Auto-Memory (Slides 12–16)

### Slide 12 — Lab 02 Problem: Fresh Context Windows, Monolithic Bloat & Memory Poisoning
- **PURPOSE:** Introduce the fresh-context-window problem and the three failure modes in `labs/lab_02_persistent_context_and_memory_hygiene/starter/context_memory_manager.py`.
- **VERBAL SCRIPT:** Every Claude Code or Antigravity session begins with a completely fresh context window. Two mechanisms carry knowledge across sessions: human-authored root context files (`CLAUDE.md` or `GEMINI.md`) and agent-authored auto-memory (`MEMORY.md` or `KNOWLEDGE.md`). In Lab 2's starter file, we see three common anti-patterns: first, a 500-line monolithic root context file that wastes thousands of tokens on every turn; second, deriving the memory directory from `os.getcwd()` instead of the git root, which fragments memory across git worktrees; and third, tagging unverified agent guesses with `#direct`, poisoning future sessions.
- **TRANSITION:** Let's fix the root context bloat first in Step 1 on Slide 13 using a 40-line cap and `@docs/*.md` on-demand imports.

### Slide 13 — Lab 02 Step 1 (`REQ-0201..0202`): Concise Root Context & `@path` Imports
- **PURPOSE:** Walk through `audit_root_context_file()` and `resolve_on_demand_references()` in `context_memory_manager.py`.
- **VERBAL SCRIPT:** In Step 1 of Lab 2, `audit_root_context_file` enforces a strict 40-line budget on `CLAUDE.md` and `GEMINI.md` and verifies that three onboarding sections are present: Commands and Environment, Architecture and Directory Map, and Core Conventions. Instead of pasting long architecture docs inline, we reference them using `@docs/architecture.md` and `@docs/testing-conventions.md`. Then `resolve_on_demand_references` pulls only the `@docs` files matching the active task topics—and validates `candidate.relative_to(root)` to block any path-traversal attacks like `@../../etc/passwd.md`. This cuts startup context token overhead by more than 80 percent.
- **TRANSITION:** Now let's see on Slide 14 how Auto-Memory paths are resolved across git worktrees and subdirectories.

### Slide 14 — Lab 02 Step 2 (`REQ-0203`): Git-Worktree Auto-Memory Resolution
- **PURPOSE:** Explain `derive_claude_memory_dir()` and how git worktrees share one unified memory directory in Claude Code and Antigravity.
- **VERBAL SCRIPT:** In Step 2, we implement `derive_claude_memory_dir`. In Claude Code, each project gets its own memory directory at `~/.claude/projects/<project>/memory/`. Crucially, the `<project>` slug is derived from the canonical git repository root, not the current subdirectory or worktree path. That means whether you are working in the main checkout, a subdirectory like `src/api`, or a parallel git worktree at `/worktrees/feature-a`, `derive_claude_memory_dir` resolves all of them to the exact same shared `memory/` directory. Outside a git repository, it cleanly falls back to the resolved working directory.
- **TRANSITION:** Once we have the shared memory directory, how do we prevent memory poisoning and bloat? Let's look at Step 3 on Slide 15.

### Slide 15 — Lab 02 Step 3 (`REQ-0204..0205`): Provenance Tags & The 200-Line Memory Cap
- **PURPOSE:** Detail epistemic provenance validation (`#direct` vs. `#commit`/`#time`/`#session`) and the 200-line / 25 KB `MEMORY.md` cap with `topics/*.md` overflow routing.
- **VERBAL SCRIPT:** Step 3 enforces two critical memory hygiene invariants. First, in `validate_and_format_memory_entry`, the `#direct` tag is reserved strictly for explicit user statements where `is_explicit_user_statement` is `True`. If an agent tries to spoof `#direct` on an indirect code observation, or fails to provide a `#commit`, `#time`, or `#session` relativity tag, the validator raises `MemoryProvenanceError`. Second, because Claude Code only auto-loads the first 200 lines or 25 kilobytes of `MEMORY.md` at startup, `compile_memory_index` keeps `MEMORY.md` under that cap and routes detailed or overflow entries into `topics/<topic>.md` with clean markdown links.
- **TRANSITION:** Let's review the interactive `/context`, `/memory`, and `/clear` commands and verify Lab 2 on Slide 16.

### Slide 16 — Lab 02 Step 4 (`REQ-0206`): `/context`, `/memory`, `/clear` & Verification
- **PURPOSE:** Connect Lab 2's code to live `/context`, `/memory`, and `/clear` CLI commands and run `./labs/lab_02.../self_diagnose.sh`.
- **VERBAL SCRIPT:** In your daily workflow, you pair these hygiene rules with built-in slash commands: run `/context` in Claude Code or `/stats` in Gemini CLI to inspect live token utilization across system prompts, context files, MCP servers, and skills; run `/memory` in Claude Code or `/memory show | add | refresh` in Gemini CLI to review and prune cross-session memories; and run `/clear` or `/compact` to keep active context below the 60 percent degradation threshold. Running `./labs/lab_02_persistent_context_and_memory_hygiene/self_diagnose.sh` executes all unit and adversarial tests—verifying worktree sharing, path-traversal blocking, `#direct` provenance, and the 200-line cap.
- **TRANSITION:** Next, let's move to Module 4 on Slide 17 and learn how to craft high-signal `agentskills.io` skills manually in Lab 3.

---

## Module 04: Lab 03 Step-by-Step — Crafting Agent Skills Manually (Slides 17–21)

### Slide 17 — Lab 03 Problem & Empirical Proof (`SkillsBench arXiv:2602.12670`)
- **PURPOSE:** Present the `SkillsBench` (`arXiv:2602.12670`) empirical benchmark across 87 tasks and 9,396 trajectories proving that human-crafted skills add `+16.6 pp` while self-generated skills hurt pass rates by `-8.1 to -11.5 pp`.
- **VERBAL SCRIPT:** Skills are procedural instruction manuals for AI. But a crucial finding from the 2026 SkillsBench paper on arXiv—spanning 87 tasks and 9,396 trajectories—is that how a skill is written determines whether it helps or hurts. When engineers write skills manually and thoughtfully—a conciencia—from real failure trajectories, pass rates jump by 16.6 percentage points on average, including plus 24.8 points on Gemini CLI and plus 18.2 points on Claude Code. Conversely, when an LLM is asked to self-generate its own skill before solving a task, pass rates drop below the no-skill baseline by 8.1 to 11.5 percentage points because the model repeats training-data platitudes or locks in hallucinated rules.
- **TRANSITION:** Let's examine the open `agentskills.io` specification and 3-level progressive disclosure architecture on Slide 18.

### Slide 18 — Lab 03 Step 1 (`REQ-0301..0302`): `agentskills.io` Spec & Progressive Disclosure
- **PURPOSE:** Explain the 3-level progressive disclosure model and YAML frontmatter validation rules implemented in `skill_validator.py`.
- **VERBAL SCRIPT:** To prevent skills from bloating the context window, the `agentskills.io` specification uses three-level progressive disclosure. At Level 1, only the YAML frontmatter `name` and `description`—roughly 100 tokens per skill—are loaded at session startup. In Step 1 of Lab 3, `validate_skill_frontmatter` verifies that `name` is 1 to 64 lowercase hyphenated characters matching the parent directory name, and that `description` states both positive `Use when...` triggers and negative `Don't use for...` boundaries. At Level 2, when invoked via `/skillname` or matched by the router, the agent reads `SKILL.md`. And at Level 3, companion reference files cost zero tokens until selectively loaded.
- **TRANSITION:** Let's inspect our concrete multi-file skill directory, `anthropic-brand/`, on Slide 19.

### Slide 19 — Lab 03 Step 2 (`REQ-0303..0304`): The Multi-File `anthropic-brand/` Skill
- **PURPOSE:** Walk through the 4-file `anthropic-brand/` skill directory (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`) and one-level-deep link validation.
- **VERBAL SCRIPT:** In Step 2, we inspect the `anthropic-brand` skill directory included on both branches and in Lab 3. Instead of cramming document typography, slide grids, and retrofit checklists into one giant file, `SKILL.md` acts as a concise 60-line Level 2 router. It defines the core hex palette tokens, highlights a real experience-grounded gotcha—never pairing Terracotta `#D97757` text directly on Muted Stone `#5E5D59` backgrounds because its 2.1-to-1 contrast fails WCAG AA—and routes to three one-level-deep companion files: `docs.md` for reports, `slides-deck.md` for 16-by-9 decks, and `apply_template.md` for retrofitting existing drafts.
- **TRANSITION:** How do we automatically catch and reject low-signal self-generated skills? Let's look at Step 3 on Slide 20.

### Slide 20 — Lab 03 Step 3 (`REQ-0305`): Rejecting Self-Generated Filler vs. High-Signal Rules
- **PURPOSE:** Show how `audit_skill_signal_quality()` differentiates `starter/bad_self_generated_skill/` from the curated `anthropic-brand/` skill.
- **VERBAL SCRIPT:** Compare `starter/bad_self_generated_skill/SKILL.md` with our curated `anthropic-brand/SKILL.md`. The self-generated skill is full of vague pretraining platitudes: write clean, modular code, follow industry best practices, make sure there are no bugs, and handle edge cases appropriately. It contains zero hex codes, zero terminal commands, and zero real gotchas. In Step 3 of Lab 3, `audit_skill_signal_quality` enforces the Experience Before Theory standard: it checks line bounds, scans for generic self-generated filler phrases, verifies at least three concrete hex tokens, file paths, or fenced commands, and requires an explicit Gotcha or Trap section.
- **TRANSITION:** Let's see on Slide 21 how selective Level 3 reference loading saves over 75 percent of tokens and run Lab 3's verifier.

### Slide 21 — Lab 03 Step 4 (`REQ-0306`): Selective Artifact Loading & Lab 03 Verification
- **PURPOSE:** Walk through `select_references_for_artifact()` and run `./labs/lab_03.../self_diagnose.sh`.
- **VERBAL SCRIPT:** In Step 4, `select_references_for_artifact` implements selective Level 3 loading: when the user asks to format a document, the agent loads only `SKILL.md` and `docs.md`, skipping `slides-deck.md` and `apply_template.md`. When building a presentation, it loads only `SKILL.md` and `slides-deck.md`. Only when retrofitting an existing document does it load `apply_template.md`. Running `./labs/lab_03_crafting_agent_skills_progressive_disclosure/self_diagnose.sh` verifies our frontmatter rules, catches broken or chained multi-hop links, rejects the self-generated skill, and passes all unit and adversarial tests.
- **TRANSITION:** Now that we can author a skill, what happens when a team adds too many skills, or how do we prove a skill works? Let's enter Module 5 and Lab 4 on Slide 22.

---

## Module 05: Lab 04 Step-by-Step — `eval-viewer`, Skill Overload & SDT (Slides 22–26)

### Slide 22 — Lab 04 Problem: Skill Catalog Overload & Uncalibrated Trigger Descriptions
- **PURPOSE:** Explain `SkillsBench` Table 8 (`2–3` skills sweet spot vs. `>= 4` skills degradation) and the trigger "Trade-Off Trap."
- **VERBAL SCRIPT:** As teams adopt Claude Code and Antigravity, they quickly hit a second trap: the more skills you add, the more confused the agent gets about which skill to use, how, and when. SkillsBench Table 8 proves this quantitatively: one skill gives plus 18.0 percentage points of lift, and two to three skills hit the peak sweet spot of plus 19.0 percentage points. But at four or more skills, lift plunges to plus 10.1 points—an 8.9 percentage-point collapse! At the same time, broadening a skill's description to get a 100 percent Hit Rate causes False Alarms to jump to 40 percent. Lab 4 solves both problems mathematically.
- **TRANSITION:** Let's start with Step 1 on Slide 23: paired `with_skill` versus `without_skill` benchmarking and the `11/11` zero-flake rule.

### Slide 23 — Lab 04 Step 1 (`REQ-0401..0402`): Paired `with_skill` vs. `without_skill` Benchmarking
- **PURPOSE:** Detail `compute_paired_benchmark()`, regression detection, and the binomial reliability math behind the `11/11` zero-flake gate.
- **VERBAL SCRIPT:** Anthropic built `skill-creator` and `eval-viewer` to measure whether a skill genuinely helps across paired evaluation runs. In Lab 4's broken starter, the evaluator only averaged `with_skill` runs, ignoring the baseline entirely. In Step 1, `compute_paired_benchmark` compares paired `with_skill` and `without_skill` trajectories on the exact same prompts, computes per-prompt pass-rate deltas, and counts any baseline assertions that regressed. Furthermore, by binomial reliability math, 3 out of 3 passes gives only 34 percent confidence that true reliability is at least 90 percent, whereas 11 out of 11 consecutive passes achieves 72 percent confidence.
- **TRANSITION:** Next, on Slide 24, let's implement the catalog overload auditor and Reference-First consolidation.

### Slide 24 — Lab 04 Step 2 (`REQ-0403..0404`): Auditing Skill Catalog Overload
- **PURPOSE:** Show how `audit_skill_catalog_overload()` detects `> 3` active skills, `< 50`-line micro-skills, and high lexical Jaccard overlap.
- **VERBAL SCRIPT:** In Step 2 of Lab 4, `audit_skill_catalog_overload` audits your workspace's active skill catalog against three rules. First, if active skill count exceeds three, it flags `overload_detected = True`. Second, any standalone micro-skill under 50 lines—such as separate 20-line skills for `git-commit`, `git-branch`, `git-pr`, and `git-rebase`—is flagged for Reference-First consolidation. Third, it computes pairwise token Jaccard similarity across skill descriptions and flags any pair with overlap at or above 0.35. Consolidating those four git micro-skills into `references/*.md` under one `git-workflow` parent skill cuts startup metadata by 60 percent and restores the plus 19.0 point sweet spot.
- **TRANSITION:** How do we tune the parent skill's description so it triggers on positive requests without false-alarming on near-misses? Slide 25 introduces Signal Detection Theory.

### Slide 25 — Lab 04 Step 3 (`REQ-0405`): Signal Detection Theory ($d'$, Criterion Bias $c$, Utility $U$)
- **PURPOSE:** Walk through `compute_sdt_metrics()` using Hautus (1995) $+0.5$ smoothing, sensitivity $d'$, criterion bias $c$, and utility $U$.
- **VERBAL SCRIPT:** In Step 3, we replace naive Hit Rate tuning with Signal Detection Theory in `compute_sdt_metrics`. Given Hits, Misses, False Alarms, and Correct Rejections on a 60/40 train/test split of positive and near-miss negative queries, we apply Hautus 0.5 smoothing so 100 percent hit rates or 0 percent false alarm rates never produce infinite z-scores. Sensitivity $d'$ equals the inverse normal of adjusted Hit Rate minus the inverse normal of adjusted False Alarm Rate, measuring true discriminability ($d' > 2.0$ is strong). Criterion bias $c$ measures whether the trigger is too conservative ($c > +0.25$), too liberal ($c < -0.25$), or balanced ($|c| \le 0.25$).
- **TRANSITION:** Let's render the self-contained `eval-viewer` HTML report and verify Lab 4 on Slide 26.

### Slide 26 — Lab 04 Step 4 (`REQ-0406`): Rendering `eval-viewer` HTML & Lab 04 Verification
- **PURPOSE:** Demonstrate `render_eval_viewer_html()` and run `./labs/lab_04.../self_diagnose.sh`.
- **VERBAL SCRIPT:** In Step 4, `render_eval_viewer_html` generates a self-contained HTML evaluation viewer modeled on Anthropic's `eval-viewer/generate_review.py`. It includes both an `Outputs` tab—showing side-by-side `with_skill` and `without_skill` outputs and assertion evidence—and a `Benchmark` tab displaying mean pass-rate lift, token delta, regression count, SDT sensitivity $d'$, criterion bias $c$, and the promotion verdict badge. Running `./labs/lab_04_skill_evaluation_and_trigger_calibration/self_diagnose.sh` verifies all paired benchmark, overload consolidation, SDT math, and HTML rendering tests.
- **TRANSITION:** Now let's move to Module 6 on Slide 27 and scale from single-agent skills to multi-agent collaboration with `feature-dev` in Lab 5.

---

## Module 06: Lab 05 Step-by-Step — Multi-Agent `feature-dev` Collaboration (Slides 27–31)

### Slide 27 — Lab 05 Problem: Why Single-Window Vibe Coding Fails on Multi-File Features
- **PURPOSE:** Contrast single-window context pollution and confirmation bias against the 7-phase `feature-dev` multi-agent architecture.
- **VERBAL SCRIPT:** Why does single-window vibe coding fall apart on multi-file features? First, running 25 raw grep searches in the main thread fills 40,000 tokens of noise, pushing the session past the 60 percent degradation wall before coding even starts. Second, without an explicit clarifying-questions gate, the agent guesses ambiguous edge cases. Third, an agent reviewing its own diff in the same context window suffers from confirmation bias. Both Anthropic's official `feature-dev` plugin and Antigravity's subagent architecture solve this by delegating exploration, architecture, and review to isolated, read-only subagents across a disciplined 7-phase pipeline.
- **TRANSITION:** Let's examine Phases 1 and 2 on Slide 28: validating subagent frontmatter and aggregating parallel `code-explorer` traces.

### Slide 28 — Lab 05 Step 1 (`REQ-0501..0502`): Subagent Frontmatter & `code-explorer`
- **PURPOSE:** Walk through `parse_agent_definition()` and `aggregate_exploration_reports()` in `feature_dev_orchestrator.py`.
- **VERBAL SCRIPT:** In Step 1 of Lab 5, `parse_agent_definition` parses `.claude/agents/*.md` and `.agents/agents/*.md` definitions for `code-explorer`, `code-architect`, and `code-reviewer`. Crucially, it enforces least-privilege tool isolation: if any read-only subagent requests `Write`, `Edit`, or `Bash`, validation fails with `SubagentSpecError`. During Phase 2, we spawn two to three parallel `code-explorer` subagents that trace entry points and call chains in isolated context windows. `aggregate_exploration_reports` verifies that every trace entry includes an exact `file:line` citation like `src/ledger/batch.py:42` and returns a deduplicated list of key files to read.
- **TRANSITION:** Once Phase 2 exploration completes, we hit the most important gate in the entire 7-phase workflow on Slide 29: Phase 3 Clarifying Questions.

### Slide 29 — Lab 05 Step 2 (`REQ-0503`): Phase 3 Mandatory Clarifying Questions Gate
- **PURPOSE:** Explain why Phase 3 is a mandatory hard stop (`ClarificationGateError`) in `FeatureDevSession` before Phase 4 Architecture or Phase 5 Implementation.
- **VERBAL SCRIPT:** Look at Phase 3 in Anthropic's official `feature-dev` specification: CRITICAL—this is one of the most important phases; DO NOT SKIP; wait for user answers before proceeding to architecture design. In Lab 5's broken starter, the orchestrator jumped straight from exploration to writing code while questions were still unanswered. In Step 2, `FeatureDevSession` enforces a deterministic state machine: calling `run_phase4_architecture` or `run_phase5_implementation` while any question in `pending_questions` lacks a non-empty answer in `clarification_answers` immediately raises `ClarificationGateError`. In Antigravity, Phase 3 pauses in `/plan` mode or `/feature-dev` for explicit human sign-off on the Implementation Plan artifact before writing code.
- **TRANSITION:** Once the human answers every clarifying question, Slide 30 walks through Phase 4 Tri-Lens Architecture and Phase 5 Implementation.

### Slide 30 — Lab 05 Step 3 (`REQ-0504..0505`): Tri-Lens `code-architect` & Implementation
- **PURPOSE:** Compare the three `code-architect` lenses (`minimal_changes`, `clean_architecture`, `pragmatic_balance`) and the Phase 5 implementation gate.
- **VERBAL SCRIPT:** In Phase 4, instead of settling for the first design that comes to mind, we spawn parallel `code-architect` subagents across three distinct engineering lenses: `minimal_changes` for the smallest diff and fastest reuse; `clean_architecture` for decoupled port-and-adapter abstractions; and `pragmatic_balance`, which balances delivery speed with clean testability. `run_phase4_architecture` verifies that all three lenses are presented with explicit trade-offs and component-level `file:line` targets. The orchestrator then waits for explicit human selection via `select_architecture_lens` before unlocking Phase 5 implementation and test verification.
- **TRANSITION:** After implementation passes unit tests, Slide 31 covers Phase 6 confidence-filtered review and Phase 7 summary generation.

### Slide 31 — Lab 05 Step 4 (`REQ-0506`): `code-reviewer` (`confidence >= 80`) & Verification
- **PURPOSE:** Show how `filter_review_findings()` suppresses low-confidence nitpicks (`< 80`) and verify Lab 5 via `./labs/lab_05.../self_diagnose.sh`.
- **VERBAL SCRIPT:** In Phase 6, we spawn three parallel `code-reviewer` subagents auditing Simplicity and DRY, Functional Correctness, and `CLAUDE.md` or `GEMINI.md` Convention Compliance. Automated reviews often fail by flooding developers with noisy, speculative nitpicks. To prevent alert fatigue, `filter_review_findings` enforces Anthropic's strict confidence threshold: every finding is scored from 0 to 100, and only findings with `confidence >= 80` are surfaced, sorted by severity and confidence descending. Running `./labs/lab_05_multi_agent_feature_dev_orchestration/self_diagnose.sh` verifies all seven phases and passes both unit and adversarial verifiers.
- **TRANSITION:** Finally, let's enter Module 7 on Slide 32 for our Lab 6 Capstone: packaging plugins, MCP servers, `PreToolUse` hooks, and the bridge to Spec-Driven Development.

---

## Module 07: Lab 06 Step-by-Step — Plugins, MCP & The SDD Bridge (Slides 32–36)

### Slide 32 — Lab 06 Problem: Skills vs. Versioned Plugins (`plugin.json` + MCP + Hooks)
- **PURPOSE:** Distinguish standalone skills from versioned plugins (`.claude-plugin/plugin.json` and `.agents/plugins/<name>/plugin.json`) and inspect the `vibe-engineering-kit` bundle.
- **VERBAL SCRIPT:** What is the difference between a Skill and a Plugin? A Skill is a single Markdown instruction manual (`SKILL.md` plus optional reference files). A Plugin is a versioned, namespaced distribution package—configured via `.claude-plugin/plugin.json` on the `claude` branch and `.agents/plugins/<name>/plugin.json` on the `agy` branch—that bundles skills, custom subagents, slash commands or rules, deterministic lifecycle hooks, and Model Context Protocol (MCP) tool servers. MCP servers give the agent deterministic hands and eyes to query live schemas, while bundled skills give the agent the procedural brain explaining when and how to use those tools.
- **TRANSITION:** Let's look at Step 1 of Lab 6 on Slide 33: validating the plugin manifest and bundled MCP server.

### Slide 33 — Lab 06 Step 1 (`REQ-0601..0602`): Validating `plugin.json` & Bundled MCP Servers
- **PURPOSE:** Walk through `validate_plugin_bundle()` and the bundled zero-dependency stdio JSON-RPC MCP server (`mcp_ledger_server.py`).
- **VERBAL SCRIPT:** In Lab 6's broken starter, `validate_plugin_bundle` accepted unversioned manifests with `version: "latest"`, missing subagent files, and empty MCP configs. In Step 1, our solution validates that the plugin name is strict kebab-case, the version follows strict `MAJOR.MINOR.PATCH` Semantic Versioning (`1.2.0`), every referenced skill and subagent file exists on disk, and every MCP server in `.mcp.json` or `mcp_config.json` specifies a valid command, argument list, and tool schema. We also include a working stdio JSON-RPC 2.0 server, `mcp_ledger_server.py`, exposing `query_ubiquitous_ledger_schema` and `check_fx_rate_bps`.
- **TRANSITION:** How do we guarantee that an agent never tampers with our locked test suite? Slide 34 implements deterministic `PreToolUse` hooks.

### Slide 34 — Lab 06 Step 2 (`REQ-0603`): Deterministic `PreToolUse` Guardrail Hooks
- **PURPOSE:** Explain why prompt rules are probabilistic and how `evaluate_pre_tool_use_hook()` deterministically blocks edits to `adversarial_tests/` and `self_diagnose.sh`.
- **VERBAL SCRIPT:** Under pressure to make a failing test pass, an unconstrained agent may attempt sycophantic self-testing—weakening an assertion or running `chmod +w` on `adversarial_tests/`. Prompt instructions alone cannot enforce security boundaries because prompts are probabilistic. In Step 2 of Lab 6, `evaluate_pre_tool_use_hook` — wired into `.claude/settings.json` and `.agents/plugins/vibe-engineering-kit/hooks/hooks.json` — intercepts every `Write`, `Edit`, `Bash`, or `run_command` call before execution. If the target path touches `adversarial_tests/`, `self_diagnose.sh`, or `.git/`, it fails closed with `decision: "block"` and `exit_code: 2`.
- **TRANSITION:** Now let's bring Kief Morris's On-the-Loop Harness Flywheel together in Step 3 on Slide 35.

### Slide 35 — Lab 06 Step 3 (`REQ-0604..0605`): The "On-the-Loop" Harness Flywheel Router
- **PURPOSE:** Walk through `recommend_flywheel_upgrade()` routing observed agent failures across the six harness layers.
- **VERBAL SCRIPT:** In Step 3, `recommend_flywheel_upgrade` implements Kief Morris's On-the-Loop Harness Flywheel. Instead of manually patching agent mistakes over and over, we classify the defect and upgrade the matching harness layer: a `wrong_test_command` upgrades `ROOT_CONTEXT_RULE` in `CLAUDE.md` or `GEMINI.md`; a `repeated_user_correction` upgrades `AUTO_MEMORY` with a `#direct` tag; a `domain_procedure_error` upgrades a `CURATED_SKILL` and verifies lift in `eval-viewer`; an attempt to edit locked tests upgrades `PRE_TOOL_USE_HOOK`; a missing live schema lookup adds a `PLUGIN_MCP_TOOL`; and multi-service architectural drift triggers `ESCALATE_TO_SDD_SPEC`.
- **TRANSITION:** Let's examine that final escalation boundary on Slide 36: when to graduate from Disciplined Vibe Coding to our Spec-Driven Development course.

### Slide 36 — Lab 06 Step 4 (`REQ-0606`): The Escalation Bridge to `SDD-Crash-Course`
- **PURPOSE:** Define the exact quantitative threshold where teams transition from Disciplined Vibe Coding (`Vibe-Coding-Course`) to Spec-Driven Development (`SDD-Crash-Course`).
- **VERBAL SCRIPT:** Slide 36 completes our bridge to the Spec-Driven Development course. When you are building a bounded feature, prototype, or utility touching one or two services without breaking wire contracts, the five harnesses you mastered in this course—Ubiquitous Language types, concise root context plus Auto-Memory, manually crafted skills, `eval-viewer` calibration, and `feature-dev` subagents—give you maximum velocity and quality. The moment a change touches three or more services, introduces a breaking API or schema migration, or requires a Clean-Room Rebuild SSOT, `recommend_flywheel_upgrade` returns `ESCALATE_TO_SDD_SPEC`, handing off directly to Conductor, OpenSpec, and `SPEC.md` in `SDD-Crash-Course`. Run `./self_diagnose_all.sh` to verify all six labs, and see you in the SDD course!
- **TRANSITION:** End of presentation. Open the floor for questions and live terminal walkthroughs on both the `agy` and `claude` branches.
