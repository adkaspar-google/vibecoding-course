# Lab 02 Walkthrough: The Core Agentic Loop & Wireshark-Style Harness Wire-Trace Inspector (`TaskFlow` Harness Telemetry)

## 1. Headache-Before-Aspirin & Spiral Retrieval Bridge

### Spiral Retrieval Bridge (From Lab 01 $\to$ Lab 02)
In **Lab 01**, we replaced vague 5-word vibe prompts on the **`TaskFlow` Productivity & Workspace Platform** with **Pillar-02 Software Engineering Constraints** (`AccountId`, integer `MoneyCents`, latency/consistency/security bounds) and **4-Tier Earned Autonomy Gates**. Yet even a well-steered prompt can fail on the wire if we treat the coding agent as a magic black box rather than inspecting the actual HTTP/JSONL payload (`system_prompt`, `standing_context`, `tool_schemas`, `messages`) transmitted across the **3-Layer Agent Stack** (`Layer 1: Model API`, `Layer 2: Toolkits & MCP`, `Layer 3: Agent Harness`).

### The Headache (150-Tool Schema Bloat & Unverified Action Loops)
When a `TaskFlow` developer wires up an agent using [`starter/bloated_wire_agent.py`](./starter/bloated_wire_agent.py) without wire-level observability:
- **150-Tool CRUD Schema Bloat:** Injecting 150 granular `mcp__github__endpoint_*` REST wrappers consumes **10,000+ lines of JSONL schema definitions** for a 1-line user prompt ($>16\times$ schema-to-conversation bloat), burning $>85\%$ of the token budget before `TaskFlow` code is even read.
- **Overfitted Standing Context:** Dumping 120 vague rules (`"Rule i: obey everything"`) into the root standing context file without a single executable test command starves the model of actionable verification instructions.
- **Unverified Mutations & Infinite Retry Loops:** The agent runs `Edit` on `app.py` and immediately declares `"Done!"` without executing a `VERIFY_RESULTS` test turn, or retries the exact same failing `Bash` command 10 times in a row.

### The Everyday Metaphor (`Known -> Target`)
Think of **Wireshark-Style Wire-Trace Inspection & Swiss Army Knife Consolidation** like **weighing a backpacker's pack before a mountain climb** (*Known* $\to$ *Target*). Packing 150 single-purpose kitchen gadgets (*150 granular CRUD tool schemas*) leaves zero room for food and water (*conversation & code context*); replacing them with a single 5-blade **Swiss Army Knife** (`Bash`, `Read`, `Edit`, `Grep`, `LSP`) slashes pack weight by $>90\%$ while handling every trail task.

---

## 2. Inspecting the Flawed Baseline & Step-by-Step Implementation

### Inspecting `starter/bloated_wire_agent.py`
Open [`starter/bloated_wire_agent.py`](./starter/bloated_wire_agent.py) (`lines 22–37`). Notice how `build_bloated_wire_payload()` constructs 150 verbose `mcp__github__endpoint_*` schemas and a 120-line standing context block with zero verification commands.

### Implementing `wire_trace_inspector.py` (`REQ-0201` through `REQ-0206`)
Implement [`expected_output/wire_trace_inspector.py`](./expected_output/wire_trace_inspector.py) (or your custom `work/wire_trace_inspector.py`) to satisfy all 6 requirements for `TaskFlow`'s harness telemetry:

1. **`REQ-0201` (3-Layer Agent Stack Classifier)**:
   - Implement `AgentStackLayer` (`LAYER_1_MODEL_API`, `LAYER_2_TOOLKIT_AND_MCP`, `LAYER_3_AGENT_HARNESS`) and `classify_stack_component(component_name)`.
2. **`REQ-0202` (Core Agentic Loop Phase Classifier & Verification Auditor)**:
   - Implement `LoopPhase` (`GATHER_CONTEXT`, `TAKE_ACTION`, `VERIFY_RESULTS`), `classify_tool_call_phase(tool_name, command_or_target)`, and `audit_loop_completion(turns)` verifying that all three phases occur and every `TAKE_ACTION` mutation is followed by a `VERIFY_RESULTS` turn (`has_unverified_mutation=False`).
3. **`REQ-0203` (Wireshark-Style HTTP/JSONL Wire-Trace Inspector)**:
   - Implement `WireTracePayload` and `inspect_wire_payload(payload)` computing `system_tokens`, `standing_context_tokens`, `tool_schema_tokens`, `conversation_tokens`, `total_tokens`, and `schema_to_conversation_ratio`.
4. **`REQ-0204` (Swiss Army Knife Consolidation vs. 150-Tool Schema Bloat Detector)**:
   - Implement `build_swiss_army_knife_schemas()` and `audit_tool_schema_bloat(payload, max_schema_to_conversation_ratio=3.0)` flagging bloated tool catalogs and computing `token_reduction_ratio` ($\ge 0.90$) when consolidating to `SWISS_ARMY_KNIFE_PRIMITIVES` (`Bash`, `Read`, `Edit`, `Grep`, `LSP`).
5. **`REQ-0205` (Standing Context Overfitting Auditor)**:
   - Implement `audit_standing_context(standing_context_text, max_lines=60)` checking that `CLAUDE.md` / `GEMINI.md` stays within 60 lines and includes an explicit test command (`unittest`, `pytest`, `self_diagnose`, etc.).
6. **`REQ-0206` (Runaway Tool-Failure Loop Circuit Breaker)**:
   - Implement `detect_runaway_tool_loop(turns, max_identical_failures=3)` tripping (`tripped=True`) when an identical `tool_name:command_or_target` signature fails $\ge 3$ consecutive times.

### Verification Commands
```bash
# Verify the reference solution
./labs/lab_02_agent_loop_and_harness_wire_trace/self_diagnose.sh

# Grade your own implementation in work/
./labs/lab_02_agent_loop_and_harness_wire_trace/self_diagnose.sh work
```

---

## 3. Common Misconception (`✕` vs. `✓`)

> **✕ Myth:** *"Giving a coding agent 150 specialized MCP tools (one for every REST API endpoint and git subcommand) makes it smarter because it never has to compose CLI commands."*
>
> **✓ Reality:** Wire-trace inspection (Stanford CS146S Lecture 2) proves the exact opposite: 150 tool schemas inject thousands of lines of JSON Schema tokens on **every single turn**, degrading attention and inflating cost by $>16\times$. Modern frontier models are heavily post-trained on `Bash`, `git`, `Read`, `Edit`, `Grep`, and `LSP`—consolidating to those 5 **Swiss Army Knife primitives** cuts schema tokens by $>90\%$ while improving tool-selection accuracy.

---

## 4. Self-Check Quiz & 3-Rung Hint Ladder

**Question (`Spot-the-Flaw`):** A `TaskFlow` agent executes the following 4-turn trajectory while fixing a bug in `ledger.py`:
```python
turns = [
    ToolTurn("Read", "ledger.py"),
    ToolTurn("Edit", "ledger.py"),
    ToolTurn("Bash", "./self_diagnose_all.sh"),
    ToolTurn("Edit", "ledger.py"),
]
```
Does `audit_loop_completion(turns)` mark `is_complete_loop` as `True` or `False`, and why?

<details>
<summary><strong>Rung 1 Hint (Spotlight — Where to Look)</strong></summary>
Inspect how `last_action_idx` and `last_verify_idx` are compared inside `audit_loop_completion()` in [`expected_output/wire_trace_inspector.py`](./expected_output/wire_trace_inspector.py) (`lines 150–172`).
</details>

<details>
<summary><strong>Rung 2 Hint (N=1 Toy Case)</strong></summary>
Compute the index of each phase in `turns`: Turn `0` (`Read`) is `GATHER_CONTEXT`, Turn `1` (`Edit`) is `TAKE_ACTION`, Turn `2` (`Bash ./self_diagnose_all.sh`) is `VERIFY_RESULTS` (`last_verify_idx = 2`), and Turn `3` (`Edit`) is `TAKE_ACTION` (`last_action_idx = 3`).
</details>

<details>
<summary><strong>Rung 3 Hint (Full Walkthrough & Answer)</strong></summary>
Even though all three `LoopPhase` values appear in `turns`, Turn `3` performs a second `Edit` (`last_action_idx = 3`) *after* the last verification run (`last_verify_idx = 2`). Because `last_verify_idx < last_action_idx`, `has_unverified_mutation` is **`True`** and `is_complete_loop` is **`False`**. Every code mutation must be followed by a fresh `VERIFY_RESULTS` step before the agent stops.
</details>

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `starter/bloated_wire_agent.py` in `/plan` mode and run `/stats` to observe live session token breakdown across system instructions, tool schemas, and messages.
3. Verify your workspace is clean before implementation:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_02_agent_loop_and_harness_wire_trace/work/wire_trace_inspector.py` and `test_wire_trace_inspector.py`, then run:
   ```bash
   ./labs/lab_02_agent_loop_and_harness_wire_trace/self_diagnose.sh work
   ```
