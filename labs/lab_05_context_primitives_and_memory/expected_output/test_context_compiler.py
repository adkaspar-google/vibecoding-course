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

"""Unit tests for Lab 05 context_compiler.py."""

from __future__ import annotations

import unittest

import context_compiler as cc


class TestContextCompiler(unittest.TestCase):
  """User unit tests for Lab 05."""

  def test_compile_root_map_and_memory_provenance(self) -> None:
    root_md = cc.compile_root_context_map(
        project_name="Vibe-Coding-Course",
        commands=["Test: `CI=true ./self_diagnose_all.sh`"],
        architecture_items=["`labs/`: 8 progressive hands-on labs"],
        on_demand_docs=["@docs/architecture.md", "@docs/testing-conventions.md"],
    )
    self.assertLessEqual(len(root_md.splitlines()), 60)
    self.assertIn("@docs/architecture.md", root_md)


if __name__ == "__main__":
  unittest.main()
