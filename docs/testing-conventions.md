# Testing Conventions & Immutable Verifiers (`@docs/testing-conventions.md`)

Referenced on demand from `CLAUDE.md`, `GEMINI.md`, and `AGENTS.md`.

## 1. Requirement Traceability (`REQ-XXXX`)
- Every lab requirement `REQ-XXXX` (`REQ-0101` through `REQ-0806`) MUST be verified by an automated unit test named `test_reqXXXX_*`.
- All tests use Python 3.11+ standard library `unittest` with zero external runtime dependencies.

## 2. Targetable Lab Graders (`self_diagnose.sh`)
- Run a single lab against reference output: `./labs/<lab>/self_diagnose.sh`
- Run a single lab against learner workspace `work/`: `./labs/<lab>/self_diagnose.sh work`
- Run all 8 labs end-to-end in `<1s`: `CI=true ./self_diagnose_all.sh`

## 3. Immutable Adversarial Verifiers (`adversarial_tests/`)
- Every lab contains `labs/<lab>/adversarial_tests/test_*_verifier.py` locked read-only (`chmod -w`) and protected by `Edit(**/adversarial_tests/**)` deny rules and `PreToolUse` Exit-Code-2 hooks.
- Never weaken, delete, or bypass test assertions (`"the fixer is never the only checker"`).
