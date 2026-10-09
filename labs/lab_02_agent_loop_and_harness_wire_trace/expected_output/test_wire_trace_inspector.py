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

"""Unit tests for Lab 02 wire_trace_inspector.py."""

from __future__ import annotations

import unittest

import wire_trace_inspector as wti


class TestWireTraceInspector(unittest.TestCase):
  """User unit tests for Lab 02."""

  def test_loop_completion_and_swiss_army_consolidation(self) -> None:
    turns = [
        wti.ToolTurn("Read", "app.py"),
        wti.ToolTurn("Edit", "app.py"),
        wti.ToolTurn("Bash", "python3 -m unittest"),
    ]
    res = wti.audit_loop_completion(turns)
    self.assertTrue(res.is_complete_loop)
    self.assertFalse(res.has_unverified_mutation)


if __name__ == "__main__":
  unittest.main()
