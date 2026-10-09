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

"""Flawed starter for Lab 07: Dumps raw child search logs into parent & allows write tools in explorer."""

from __future__ import annotations


def run_leaky_subagent(raw_grep_logs: list[str]) -> str:
  """Anti-pattern: returns entire raw grep dump to parent instead of bounded summary."""
  return "\n".join(raw_grep_logs)
