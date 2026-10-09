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
echo "  Vibe-Coding-Course: Running Master Self-Diagnosis Across All 8 Labs"
echo "========================================================================"

LABS=(
  "lab_01_vibe_coding_and_earned_autonomy"
  "lab_02_agent_loop_and_harness_wire_trace"
  "lab_03_reppit_workflow_and_reflection"
  "lab_04_context_physics_and_rpi_compaction"
  "lab_05_context_primitives_and_memory"
  "lab_06_skills_chub_and_meta_mcp_code_mode"
  "lab_07_subagent_firewalls_and_peer_council"
  "lab_08_governance_linters_and_autoresearch_ratchet"
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
