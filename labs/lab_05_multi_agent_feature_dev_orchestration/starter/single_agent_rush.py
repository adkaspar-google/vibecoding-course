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

"""Anti-pattern starter: jumping straight from vague prompt to code (Phase 1 -> Phase 5).

Skips codebase exploration (code-explorer), skips clarifying questions (Phase 3 gate),
skips architectural trade-off comparison (code-architect), and skips confidence-filtered
review (code-reviewer).
"""

from __future__ import annotations


def run_unguarded_feature_build(user_prompt: str) -> dict[str, str]:
  return {
      "prompt": user_prompt,
      "status": "WROTE_CODE_WITHOUT_EXPLORATION_OR_CLARIFICATION",
  }
