# Lab 02: The Core Agentic Loop & Wireshark-Style Harness Wire-Trace Inspector

## 1. Learning Objectives & Conceptual Motivation

1. **The 3-Layer Agent Stack (`andrewyng/aisuite` & Skills Map 3.5)**:
   A coding agent is not just an LLM chat box; it is an engineered **Harness** wrapping a model and a toolkit across three layers:
   - **Layer 1 (`LAYER_1_MODEL_API`)**: Stateless `provider:model` completion endpoints (`ChatCompletions`, tokenization, reasoning effort, KV prompt caching).
   - **Layer 2 (`LAYER_2_TOOLKIT_AND_MCP`)**: Local filesystem, Git, and shell primitives (`Read`, `Edit`, `Bash`, `Grep`, `LSP`) plus external Model Context Protocol (`mcp__*`) servers.
   - **Layer 3 (`LAYER_3_AGENT_HARNESS`)**: Standing project context (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`), Plan Mode, Skills, Subagent firewalls, Lifecycle Hooks (`PreToolUse`, `PostToolUse`), Auto-Memory, and Context Compaction.

2. **Wireshark-Style Harness Trace Inspection (Stanford CS146S Lecture 2, `themodernsoftware.dev`)**:
   When you inspect a production coding agent (`agy` or `claude`) on the wire via an HTTP/JSONL proxy, every API turn transmits four distinct payload segments:
   - `system_prompt` (~50–80 lines of core behavioral instructions)
   - `standing_context` (`CLAUDE.md` / `GEMINI.md` / `AGENTS.md` + active rules)
   - `tool_schemas` (JSON Schema definitions for native and `mcp__` tools)
   - `messages` (interleaved user prompts, thoughts, `tool_use` calls, and `tool_result` outputs)
   - **The "Swiss Army Knife" Tool Consolidation Principle:** Early MCP setups with 110–150 granular CRUD tools consumed **10,000+ lines of JSONL schema definitions** for just **600 lines of conversation** ($>16\times$ schema-to-conversation bloat). Production harnesses favor compact general-purpose primitives (`Bash`, `Read`, `Edit`, `Grep`, `LSP`) because modern models have post-trained fluency in CLI and Git mechanics.

3. **The Core Agentic Loop (`Gather Context -> Take Action -> Verify Results`)**:
   As taught in *Claude Code 101* and *Hands-on with Antigravity CLI*, every reliable engineering turn follows three phases:
   1. **Gather Context (`GATHER_CONTEXT`)**: `Read`, `Grep`, `Glob`, `LSP`, or read-only `git status`/`git diff`.
   2. **Take Action (`TAKE_ACTION`)**: `Edit`, `Write`, or mutating shell commands.
   3. **Verify Results (`VERIFY_RESULTS`)**: Running deterministic unit tests (`unittest`, `self_diagnose.sh`) or live `/browser` checks before claiming completion, while a **Loop Circuit Breaker** halts runaway retries when the same tool call fails 3 times in a row.

---

## 2. Inspecting the Flawed Baseline (`starter/bloated_wire_agent.py`)

Inspect `starter/bloated_wire_agent.py`. Notice three harness anti-patterns:
- **150-Tool CRUD Schema Bloat**: Injects 150 granular REST tool schemas into every turn, burning $>85\%$ of the wire payload before the user says a word.
- **Unverified Action Loops**: Executes `Edit` mutations and immediately returns `"Done!"` without running any `VERIFY_RESULTS` test command.
- **Infinite Retry Loop**: Retries a failing `Bash` command indefinitely with identical arguments when a test fails.

---

## 3. Step-by-Step Implementation (`wire_trace_inspector.py`)

Implement `wire_trace_inspector.py` satisfying `REQ-0201` through `REQ-0206`:
1. **`REQ-0201` (3-Layer Agent Stack Classifier)**:
   - `AgentStackLayer` (`LAYER_1_MODEL_API`, `LAYER_2_TOOLKIT_AND_MCP`, `LAYER_3_AGENT_HARNESS`) and `classify_stack_component(name)`.
2. **`REQ-0202` (Agentic Loop Phase Classifier & Verification Auditor)**:
   - `LoopPhase` (`GATHER_CONTEXT`, `TAKE_ACTION`, `VERIFY_RESULTS`), `classify_tool_call_phase(tool_name, command_arg)`, and `audit_loop_completion(turns)` ensuring every mutation is followed by a verification step.
3. **`REQ-0203` (Wireshark-Style HTTP/JSONL Wire-Trace Inspector)**:
   - `WireTracePayload` and `inspect_wire_payload(payload)` computing segment token counts (`system_tokens`, `standing_context_tokens`, `tool_schema_tokens`, `conversation_tokens`, `total_tokens`).
4. **`REQ-0204` (Swiss Army Knife Consolidation vs. Schema Bloat Detector)**:
   - `audit_tool_schema_bloat(payload, max_schema_to_conversation_ratio=3.0)` flagging bloated tool catalogs and computing token savings when consolidating to `SWISS_ARMY_KNIFE_PRIMITIVES` (`Bash`, `Read`, `Edit`, `Grep`, `LSP`).
5. **`REQ-0205` (Standing Context Overfitting Auditor)**:
   - `audit_standing_context(text, max_lines=60)` verifying concise standing context with explicit test/build commands.
6. **`REQ-0206` (Runaway Tool-Failure Circuit Breaker)**:
   - `detect_runaway_tool_loop(turns, max_identical_failures=3)` tripping when an identical `(tool_name, args_signature)` fails $\ge 3$ consecutive times.

---

## 4. Verification Command

```bash
./labs/lab_02_agent_loop_and_harness_wire_trace/self_diagnose.sh
```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, run `/context` to inspect how system prompts, `CLAUDE.md`, MCP tools, and messages consume context tokens, then read `starter/bloated_wire_agent.py`.
3. Verify no files were modified during exploration:
   ```bash
   git status --short
   ```
4. Implement `labs/lab_02_agent_loop_and_harness_wire_trace/work/wire_trace_inspector.py` and `test_wire_trace_inspector.py`, then verify:
   ```bash
   ./labs/lab_02_agent_loop_and_harness_wire_trace/self_diagnose.sh work
   ```
