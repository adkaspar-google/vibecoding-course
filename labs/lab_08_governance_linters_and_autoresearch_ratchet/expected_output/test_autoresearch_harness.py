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

"""Unit tests for Lab 08 autoresearch_harness.py."""

from __future__ import annotations

import unittest

import autoresearch_harness as ah


class TestAutoresearchHarness(unittest.TestCase):
  """User unit tests for Lab 08."""

  def test_simplicity_criterion_and_remediation_linter(self) -> None:
    keep_del = ah.evaluate_autoresearch_ratchet(0.990, 0.989, loc_delta=-8)
    self.assertEqual(keep_del.decision, ah.RatchetDecision.KEEP_SIMPLIFICATION)

    reject_bloat = ah.evaluate_autoresearch_ratchet(0.990, 0.9895, loc_delta=25)
    self.assertEqual(reject_bloat.decision, ah.RatchetDecision.REVERT_COMPLEXITY_BLOAT)


if __name__ == "__main__":
  unittest.main()
