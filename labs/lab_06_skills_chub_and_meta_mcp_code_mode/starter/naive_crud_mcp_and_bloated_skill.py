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

"""Flawed starter for Lab 06: 120 raw CRUD tools with untyped kwargs and 800-line SKILL.md."""

from __future__ import annotations

from typing import Any


def get_naive_crud_mcp_catalog() -> list[dict[str, Any]]:
  """Anti-pattern: 120 low-level CRUD tools with untyped kwargs dict."""
  return [
      {
          "name": f"get_rest_resource_{i}",
          "description": "Low-level REST GET wrapper " * 15,
          "parameters": {"kwargs": "dict"},
      }
      for i in range(120)
  ]
