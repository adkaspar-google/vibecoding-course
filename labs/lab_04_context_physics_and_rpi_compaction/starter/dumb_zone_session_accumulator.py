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

"""Flawed starter for Lab 04: Floods context into the Dumb Zone (>40%) without backpressure."""

from __future__ import annotations


def run_noisy_session(history: list[str], raw_stdout: str) -> list[str]:
  """Anti-pattern: dumps entire multi-thousand-line stdout into context without compaction."""
  history.append(raw_stdout)
  return history
