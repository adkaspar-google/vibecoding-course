#!/bin/bash
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_RAW="${1:-expected_output}"
if [[ "${TARGET_RAW}" = /* ]]; then
  TARGET_DIR="${TARGET_RAW}"
else
  TARGET_DIR="${LAB_DIR}/${TARGET_RAW}"
fi

echo "=== Lab 06: Capstone — Plugins, MCP Servers & Harness Flywheel (${TARGET_RAW}) ==="

if [[ ! -f "${TARGET_DIR}/harness_flywheel.py" ]]; then
  echo "[FAIL] Missing required deliverable: ${TARGET_DIR}/harness_flywheel.py"
  exit 1
fi

if [[ ! -d "${TARGET_DIR}/vibe-engineering-plugin" ]]; then
  echo "[FAIL] Missing required plugin bundle: ${TARGET_DIR}/vibe-engineering-plugin"
  exit 1
fi

LAB06_TARGET_DIR="${TARGET_DIR}" PYTHONPATH="${TARGET_DIR}" python3 -m unittest discover -s "${LAB_DIR}/adversarial_tests" -p "test_*.py" -v
if compgen -G "${TARGET_DIR}/test_*.py" > /dev/null; then
  LAB06_TARGET_DIR="${TARGET_DIR}" PYTHONPATH="${TARGET_DIR}" python3 -m unittest discover -s "${TARGET_DIR}" -p "test_*.py" -v
else
  echo "[SKIP] No user test_*.py found in ${TARGET_DIR}; ran immutable adversarial_tests only."
fi

echo "[PASS] Lab 06 verified: Plugins, MCP Servers & Harness Flywheel passed!"
