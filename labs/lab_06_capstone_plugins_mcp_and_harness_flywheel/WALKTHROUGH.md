# Lab 06: Capstone — Skills vs. Plugins, MCP Servers, `PreToolUse` Hooks & The "On-the-Loop" Harness Flywheel

## 1. Learning Objectives & Architectural Synthesis

1. **Skills vs. Plugins**:
   - A **Skill** (`SKILL.md` + optional `references/` and `scripts/`) is a single procedural instruction manual.
   - A **Plugin** (`.claude-plugin/plugin.json` on `claude` / `.agents/plugins/<name>/plugin.json` on `agy`) is a **versioned, namespaced distribution unit** (`/plugin-name:skill-name`) that bundles skills (`skills/`), subagents (`agents/`), commands/rules, event hooks (`hooks.json`), and **MCP servers** (`.mcp.json` / `mcp_config.json`).
2. **Kief Morris's "On-the-Loop" Harness Flywheel (*Humans and Agents in Software Engineering Loops*, 2026)**:
   - Instead of micromanaging every generated code line (*In-the-Loop*) or blindly accepting unverified diffs (*Out-of-the-Loop*), an **On-the-Loop** engineer converts every agent failure into a permanent harness upgrade:
     - Wrong build/test command $\to$ `ROOT_CONTEXT_RULE` (`CLAUDE.md` / `GEMINI.md`)
     - Repeated user preference correction $\to$ `AUTO_MEMORY` (`MEMORY.md` / `KNOWLEDGE.md` with `#direct`)
     - Multi-step procedural error $\to$ `CURATED_SKILL` (`SKILL.md` + `references/`)
     - Unauthorized mutation of locked tests $\to$ `PRE_TOOL_USE_HOOK` (`hooks.json`)
     - Missing live schema/telemetry tool $\to$ `PLUGIN_MCP_TOOL` (`plugin.json` + MCP server)
3. **The Bridge to Spec-Driven Development (SDD)**:
   - When a change spans $\ge 3$ services or introduces cross-service contract drift, conversational vibe coding reaches its structural limit—and the flywheel routes the task to **Spec-Driven Development (`ESCALATE_TO_SDD_SPEC`)** (`openspec/specs/` + `conductor/tracks/` in the follow-on `SDD-Crash-Course`).

---

## 2. Step-by-Step Implementation

1. Create the versioned plugin bundle `vibe-engineering-plugin/` supporting both `claude` (`.claude-plugin/plugin.json`, `.mcp.json`, `hooks/hooks.json`) and `agy` (`plugin.json`, `mcp_config.json`, `hooks.json`) plus `skills/harness-audit/SKILL.md`.
2. Implement `harness_flywheel.py` satisfying `REQ-0601` through `REQ-0606`:
   - `validate_plugin_bundle(plugin_dir, harness)`
   - `evaluate_pre_tool_use_hook(event_payload)`
   - `MCPHarnessServer.handle_jsonrpc(request)`
   - `classify_skill_vs_plugin(requirements)`
   - `route_harness_flywheel_improvement(failure_event)`

---

## 3. Verification Command

```bash
./labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/self_diagnose.sh
```

---

## Antigravity Track

1. Launch Antigravity from the repository root:
   ```bash
   agy --workspace .
   ```
2. Inspect `starter/unbundled_loose_tools.json` as your only input in `/plan` mode and design the `vibe-engineering-plugin/` bundle and `harness_flywheel.py`.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and run the `/feature-dev` workflow to implement `work/harness_flywheel.py` and `work/vibe-engineering-plugin/` until `./labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/self_diagnose.sh work` exits `0` without modifying `adversarial_tests/` or `expected_output/`.
5. Run targetable self-diagnosis:
   ```bash
   ./labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/self_diagnose.sh work
   ```

---

## Claude Code Track

1. Launch Claude Code in learner mode from the repository root:
   ```bash
   claude --settings .claude/learner.settings.json
   ```
2. In `plan mode`, inspect `starter/unbundled_loose_tools.json` as your only input and plan the `.claude-plugin/plugin.json` manifest, `.mcp.json`, `hooks/hooks.json`, and `harness_flywheel.py`.
3. Run the human approval checkpoint:
   ```bash
   git status --short
   ```
4. Start a new session (or run `/clear`) and invoke `/feature-dev`:
   ```text
   /feature-dev Implement labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/work/ until ./labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/self_diagnose.sh work exits 0; do not modify any file under adversarial_tests/ or expected_output/.
   ```
5. Run targetable self-diagnosis:
   ```bash
   ./labs/lab_06_capstone_plugins_mcp_and_harness_flywheel/self_diagnose.sh work
   ```
