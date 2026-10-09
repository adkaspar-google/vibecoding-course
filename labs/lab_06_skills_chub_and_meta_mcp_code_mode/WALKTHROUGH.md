# Lab 06: Harness Engineering Layer 2 — Progressive-Disclosure Skills, `chub` Self-Annotating Docs & Meta-MCP "Code Mode"

## 1. Learning Objectives & Conceptual Motivation

1. **Progressive-Disclosure Agent Skills (`agentskills.io` Open Standard)**:
   Skills package procedural domain expertise across three lazy-loaded disclosure levels:
   - **Level 1 (YAML Frontmatter)**: `name` and trigger-rich `description` (`Use when ... Don't use for ...`, ~50–100 tokens) loaded at session startup.
   - **Level 2 (`SKILL.md` Body $\le 500$ lines)**: Step-by-step workflow loaded **only** when the skill is triggered.
   - **Level 3 (`references/*.md`, `scripts/*.py`, `assets/*`)**: Deep reference tables and deterministic scripts loaded or executed on demand without bloating context.

2. **Curated Versioned Grounding & Self-Improving Annotations (`andrewyng/context-hub`, `@aisuite/chub`)**:
   To prevent LLM API hallucinations on fast-moving SDKs, Andrew Ng's `context-hub` equips agents with a `get-api-docs` skill backed by the `chub` CLI:
   - `chub search <query>` and `chub get <doc_id> --lang py` fetch curated, versioned, language-specific Markdown documentation.
   - **Self-Improving Session Loop (`chub annotate`):** When an agent discovers an API gotcha during debugging (e.g., `"Stripe webhook verification requires the raw unparsed request body"`), it saves a local note via `chub annotate stripe/webhooks "..."`. Future runs retrieve the note via `--with-annotations` (explicitly marked as untrusted local input) and report quality signals upstream via `chub feedback up|down`.

3. **Ergonomic MCP Tools & Meta-MCP "Code Mode" (`>90%` Token Reduction, Stanford CS146S Lecture 4)**:
   - **4 Rules of Ergonomic Agent Tools:** (1) Design around **outcomes**, not 1-to-1 REST CRUD endpoints; (2) Enforce **strict typed schemas** (no untyped `**kwargs` or open `dict`s); (3) Return **actionable typed errors**; and (4) Use **Meta-MCP "Code Mode" (`search` + `execute` meta-tools)**.
   - Instead of injecting 120 MCP tool schemas into every turn, **Meta-MCP Code Mode** exposes only two compact meta-tools (`mcp__meta__search` to query relevant tool schemas on demand, and `mcp__meta__execute` to run a chained script inside a sandbox), cutting standing schema tokens by **$\ge 90\%$**.

4. **Empirical Skill Science (`SkillsBench`, `arXiv:2602.12670`)**:
   Across 87 tasks and 9,396 trajectories, curated human-authored skills raise pass rates by **+16.2pp to +16.6pp**, whereas self-generated skills degrade pass rates (**-1.3pp to -11.5pp**), and loading $>10$ overlapping skills triggers severe routing confusion.

---

## 2. Inspecting the Flawed Baseline (`starter/naive_crud_mcp_and_bloated_skill.py`)

Inspect `starter/naive_crud_mcp_and_bloated_skill.py`. Notice three Layer-2 anti-patterns:
- **800-Line Monolithic `SKILL.md`**: Dumps every reference table directly into `SKILL.md` with a vague 3-word description.
- **Unannotated Stale API Calls**: Hallucinates deprecated SDK parameters because there is no `chub` doc lookup or local session annotation store.
- **120-Tool CRUD MCP Catalog**: Injects 120 low-level `get_*`/`post_*` REST wrappers with untyped `kwargs: dict` parameters directly into the standing prompt.

---

## 3. Step-by-Step Implementation (`skill_and_mcp_harness.py`)

Implement `skill_and_mcp_harness.py` satisfying `REQ-0601` through `REQ-0606`:
1. **`REQ-0601` (`agentskills.io` 3-Level Progressive Disclosure Validator)**:
   - `validate_progressive_skill_package(name, description, skill_md_lines, companion_files)`.
2. **`REQ-0602` (`andrewyng/context-hub` Curated Doc Store & `chub annotate` Loop)**:
   - `ChubRegistry` with `search(query)`, `get(doc_id, lang="py", with_annotations=False)`, `annotate(doc_id, note)`, and `feedback(doc_id, rating)`.
3. **`REQ-0603` (Ergonomic Tool Schema Auditor — CS146S Lecture 4)**:
   - `audit_tool_ergonomics(tool_spec)` flagging raw CRUD prefixes, untyped `kwargs` / missing strict properties, and missing error remediation hints.
4. **`REQ-0604` (Meta-MCP "Code Mode" `search` + `execute` Harness & $\ge 90\%$ Token Savings)**:
   - `MetaMcpCodeModeHarness` and `measure_code_mode_token_savings(raw_tool_schemas)` proving $\ge 0.90$ token reduction.
5. **`REQ-0605` (`SkillsBench` Paired Ablation Evaluator)**:
   - `evaluate_skillsbench_ablation(with_skill_scores, without_skill_scores, is_self_generated=False)`.
6. **`REQ-0606` (Skill Catalog Overload Detector)**:
   - `audit_skill_catalog_overload(active_skill_names, sweet_spot_max=3, overload_ceiling=10)`.

---

## 4. Verification Command

```bash
./labs/lab_06_skills_chub_and_meta_mcp_code_mode/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `.agents/skills/` and `starter/naive_crud_mcp_and_bloated_skill.py` in `/plan` mode, and list active skills with `/skills`.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_06_skills_chub_and_meta_mcp_code_mode/work/skill_and_mcp_harness.py` and `test_skill_and_mcp_harness.py`, then run:
   ```bash
   ./labs/lab_06_skills_chub_and_meta_mcp_code_mode/self_diagnose.sh work
   ```
