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

"""Unit tests for Lab 07 subagent_council.py."""

from __future__ import annotations

import unittest

import subagent_council as sc


class TestSubagentCouncil(unittest.TestCase):
  """User unit tests for Lab 07."""

  def test_firewall_and_council_ranking(self) -> None:
    res = sc.execute_subagent_context_firewall(
        raw_search_traces=["grep dump " * 500 for _ in range(10)],
        concise_findings=["`src/ledger.py:L25` enforces double-entry balance."],
    )
    self.assertGreaterEqual(res.isolation_ratio, 0.90)


if __name__ == "__main__":
  unittest.main()
