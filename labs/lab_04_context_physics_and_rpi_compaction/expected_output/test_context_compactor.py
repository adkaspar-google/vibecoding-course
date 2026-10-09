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

"""Unit tests for Lab 04 context_compactor.py."""

from __future__ import annotations

import unittest

import context_compactor as cc


class TestContextCompactor(unittest.TestCase):
  """User unit tests for Lab 04."""

  def test_smart_vs_dumb_zone_and_backpressure(self) -> None:
    smart = cc.profile_context_window(50_000, 200_000)
    dumb = cc.profile_context_window(95_000, 200_000)
    self.assertEqual(smart.zone, cc.ContextZone.SMART_ZONE)
    self.assertEqual(dumb.zone, cc.ContextZone.DUMB_ZONE)
    self.assertTrue(dumb.requires_compaction)


if __name__ == "__main__":
  unittest.main()
