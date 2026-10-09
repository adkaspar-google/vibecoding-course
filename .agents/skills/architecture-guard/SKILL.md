---
name: architecture-guard
description: >-
  Runs remediation-aware structural architecture linting ([VIOLATION] -> [WHY] ->
  [HOW TO FIX]), Front-Loaded Program Design type/call-graph verification, and
  Karpathy's autoresearch Simplicity Criterion checks. Use when validating module
  boundaries, reviewing diffs, or running closed-loop ratchets. Don't use for UI
  copywriting.
---

# Remediation-Aware Architecture Guard (`architecture-guard`)

Enforces architectural boundaries (`references/layer_contracts.md`) and emits self-repair instructions directly into the agent's context window.

## Verification Steps
1. **Structural Layer Check**: Run `python3 scripts/lint_architecture.py` to verify that `domain/` modules never import `infra/` or `ui/` directly.
2. **Remediation Format**: Every violation must be formatted as `[VIOLATION] ... [WHY] ... [HOW TO FIX] ...`.
3. **Program Design & Simplicity Criterion**: Verify explicit non-`Any` type signatures before vertical-slice implementation, and reject complexity bloat in autonomous loops.
