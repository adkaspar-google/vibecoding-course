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

"""Flawed starter for Lab 08: Reward-hacks prepare.py and keeps 50-line bloat for 0.0001 gain."""

from __future__ import annotations


def run_unguarded_dark_factory() -> dict[str, object]:
  """Anti-pattern: modifies prepare.py evaluator and accepts unbounded code bloat."""
  return {
      "modified_files": ["prepare.py", "adversarial_tests/test_suite.py"],
      "kept_change": True,
      "loc_added": 55,
      "bpb_delta": -0.0001,
  }
