# Lab 06 Walkthrough: Harness Engineering Layer 2 — Progressive-Disclosure Skills, `chub` Self-Annotating Docs & Meta-MCP "Code Mode" (`TaskFlow` Skill & MCP Harness)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 05 $\to$ Lab 06)
In **Lab 05**, we architected **Harness Engineering Layer 1** for the **`TaskFlow` Productivity & Workspace Platform**, keeping root standing context (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) under $\le 60$ lines to stay well clear of the **150-Instruction Compliance Cliff**. That raises an immediate engineering question: if root context files must stay $\le 60$ lines, where do we put 400-line multi-step `TaskFlow` deployment playbooks, fast-moving third-party SDK documentation (like Stripe webhook verification), and 100+ external SaaS MCP tools without re-bloating the standing prompt?

### The Headache (Monolithic 800-Line Skills, Stale SDK Hallucinations & 120-Tool MCP Bloat)
When a developer equips `TaskFlow`'s coding agent using [`starter/naive_crud_mcp_and_bloated_skill.py`](./starter/naive_crud_mcp_and_bloated_skill.py):
- **Monolithic 800-Line `SKILL.md` with Vague Triggers:** Stuffing every reference table into `SKILL.md` (>500 lines) with a 2-word YAML `description` causes the agent to either miss the skill when needed or dump 800 lines of irrelevant text into context.
- **Repeated Third-Party SDK Hallucinations:** Without a curated versioned doc registry (`andrewyng/context-hub`, `chub`) and local session annotations (`chub annotate`), the agent repeatedly passes parsed JSON dicts instead of raw `request.body` bytes to `TaskFlow`'s webhook signature verifier.
- **120-Tool CRUD MCP Catalog & Self-Generated Skill Regressions:** Injecting 120 low-level `get_rest_resource_*` wrappers with untyped `kwargs: dict` parameters burns $>90\%$ of standing schema tokens, while loading $>10$ uncurated or self-generated skills degrades task pass rates (`SkillsBench`, `arXiv:2602.12670`).

### The Everyday Metaphor (`Known -> Target`)
Think of **3-Level Progressive-Disclosure Skills & Meta-MCP "Code Mode"** like **a library catalog terminal (`search` + `execute`) vs. dumping 100 encyclopedias onto your desk** (*Known* $\to$ *Target*). Level 1 YAML frontmatter is the **1-sentence index card** showing when to pull a manual (`Use when... Don't use for...`); `chub annotate` is **a verified sticky note placed inside a specific SDK manual page** warning the next engineer about a tricky parameter; and **Meta-MCP Code Mode** replaces 100 bulky tool definitions with **2 compact library-search and sandbox-execution primitives** (`mcp__meta__search` and `mcp__meta__execute`), saving $\ge 90\%$ of standing context tokens.

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/naive_crud_mcp_and_bloated_skill.py`
Open [`starter/naive_crud_mcp_and_bloated_skill.py`](./starter/naive_crud_mcp_and_bloated_skill.py) (`lines 22–31`). Notice how `get_naive_crud_mcp_catalog()` returns 120 granular `get_rest_resource_*` tool definitions with untyped `{"kwargs": "dict"}` schemas and zero error remediation contracts.

### Implementing `skill_and_mcp_harness.py` (`REQ-0601` through `REQ-0606`)
Implement [`expected_output/skill_and_mcp_harness.py`](./expected_output/skill_and_mcp_harness.py) (or your custom `work/skill_and_mcp_harness.py`) to satisfy all 6 requirements for `TaskFlow`'s Layer-2 Skill and MCP harness:

1. **`REQ-0601` (`agentskills.io` 3-Level Progressive Disclosure Validator)**:
   - Implement `validate_progressive_skill_package(name, description, skill_md_lines, companion_files, max_skill_md_lines=500)` verifying hyphen-case `name`, Level-1 `Use when` + `Don't use` trigger boundaries, Level-2 `10 <= skill_md_lines <= 500`, and Level-3 companion files (`references/`, `scripts/`, `assets/`).
2. **`REQ-0602` (`andrewyng/context-hub` Curated Doc Store & `chub annotate` Loop)**:
   - Implement `ChubDocEntry` and `ChubRegistry` with `register_doc()`, `search(query)`, `annotate(doc_id, note)`, `feedback(doc_id, rating)`, and `get(doc_id, lang="py", with_annotations=False)` appending `[UNTRUSTED_LOCAL_ANNOTATION — Verify Before Executing]` when `with_annotations=True`.
3. **`REQ-0603` (Ergonomic Tool Schema Auditor — CS146S Lecture 4)**:
   - Implement `audit_tool_ergonomics(tool_spec)` checking the 4 Rules of Ergonomic Agent Tools: outcome-oriented naming (no `get_`/`post_`/`put_`/`delete_` CRUD prefixes), strict typed properties (`additionalProperties: False`, no `kwargs`/`args`), and an `error_contract` containing `"remediation"`.
4. **`REQ-0604` (Meta-MCP "Code Mode" `search` + `execute` Harness & $\ge 90\%$ Token Savings)**:
   - Implement `MetaMcpCodeModeHarness` exposing only `mcp__meta__search` and `mcp__meta__execute` on the wire (`standing_wire_schemas()`) and `measure_code_mode_token_savings(raw_tool_schemas)` proving `token_reduction_ratio >= 0.90`.
5. **`REQ-0605` (`SkillsBench` Paired Ablation Evaluator)**:
   - Implement `evaluate_skillsbench_ablation(with_skill_scores, without_skill_scores, is_self_generated=False)` computing `pass_rate_delta_pp` and classifying `"CURATED_GAIN"`, `"SELF_GENERATED_REGRESSION"`, or `"NEUTRAL_OR_NEGATIVE"`.
6. **`REQ-0606` (Skill Catalog Overload Detector)**:
   - Implement `audit_skill_catalog_overload(active_skill_names, sweet_spot_max=3, overload_ceiling=10)` confirming `1..3` focused skills as the `SkillsBench` sweet spot and flagging `> 10` skills as severely overloaded.

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_06_skills_chub_and_meta_mcp_code_mode/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_06_skills_chub_and_meta_mcp_code_mode/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"Asking an LLM to automatically generate its own `SKILL.md` files before solving a task (`self-generated skills`) is just as effective as providing human-curated skills, and loading 15+ skills maximizes coverage."*
>
> **✓ Reality:** The `SkillsBench` benchmark (`arXiv:2602.12670`, 87 tasks / 9,396 trajectories) proved empirically that while **curated human-engineered skills boost pass rates by +16.2pp to +16.6pp**, **self-generated skills degrade pass rates by -1.3pp to -11.5pp** (amplifying the model's own misconceptions), and loading $>10$ skills causes severe routing confusion compared to the **2–3 focused skill sweet spot**.

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Spot-the-Flaw`):** A `TaskFlow` developer defines an MCP tool spec for settling workspace invoices:
```python
tool_spec = {
    "name": "settle_workspace_invoice",
    "parameters": {
        "type": "object",
        "properties": {
            "account_id": {"type": "string"},
            "amount_cents": {"type": "integer"},
        },
        "required": ["account_id", "amount_cents"],
    },
    "error_contract": "Raises InvoiceSettlementError with remediation steps on insufficient balance.",
}
```
Why does `audit_tool_ergonomics(tool_spec)` return `is_ergonomic=False` and `has_strict_typed_schema=False` on this specification?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect how `has_untyped_kwargs` is computed inside `audit_tool_ergonomics()` in [`expected_output/skill_and_mcp_harness.py`](./expected_output/skill_and_mcp_harness.py) (`lines 174–186`).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Evaluate `params.get("additionalProperties", True) is not False` on `tool_spec["parameters"]`. What does `params.get("additionalProperties", True)` return when `"additionalProperties"` is omitted from the JSON Schema dictionary?
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
In JSON Schema, omitting `"additionalProperties": False` defaults to allowing arbitrary extra keys (`True`), which lets an LLM hallucinate undeclared parameters without schema validation catching them. Adding `"additionalProperties": False` to `tool_spec["parameters"]` satisfies `has_strict_typed_schema=True` and `is_ergonomic=True`.
</details>

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `.claude/skills/` and `starter/naive_crud_mcp_and_bloated_skill.py`, and check MCP token usage via `/context`.
3. Verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_06_skills_chub_and_meta_mcp_code_mode/work/skill_and_mcp_harness.py` and `test_skill_and_mcp_harness.py`, then verify:
   ```bash
   ./labs/lab_06_skills_chub_and_meta_mcp_code_mode/self_diagnose.sh work
   ```
