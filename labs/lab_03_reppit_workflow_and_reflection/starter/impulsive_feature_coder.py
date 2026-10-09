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

"""Flawed starter for Lab 03: Impulsive feature coder without RePPIT or context reset."""

from __future__ import annotations


def impulsive_implement(feature_request: str, proposal_a: str, proposal_b: str) -> dict[str, str]:
  """Anti-pattern: keeps both conflicting proposals in context and skips Research/Plan."""
  combined_context = f"Request: {feature_request}\nOption A: {proposal_a}\nOption B: {proposal_b}"
  return {
      "context_used": combined_context,
      "files_modified": "app.py, auth.py, legacy_billing.py",
      "verified": "assumed_working",
  }
