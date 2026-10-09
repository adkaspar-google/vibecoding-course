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

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================================================"
echo "  Vibe-Coding-Course: Running Master Self-Diagnosis Across All 6 Labs"
echo "========================================================================"

LABS=(
  "lab_01_vocabulary_and_bounded_language_games"
  "lab_02_persistent_context_and_memory_hygiene"
  "lab_03_crafting_agent_skills_progressive_disclosure"
  "lab_04_skill_evaluation_and_trigger_calibration"
  "lab_05_multi_agent_feature_dev_orchestration"
  "lab_06_capstone_plugins_mcp_and_harness_flywheel"
)

PASSED=0
for lab in "${LABS[@]}"; do
  echo ""
  "${ROOT_DIR}/labs/${lab}/self_diagnose.sh"
  PASSED=$((PASSED + 1))
done

echo ""
echo "========================================================================"
echo "  [ALL PASSED] ${PASSED}/${#LABS[@]} Hands-On Vibe-Coding-Course Labs Verified!"
echo "========================================================================"
