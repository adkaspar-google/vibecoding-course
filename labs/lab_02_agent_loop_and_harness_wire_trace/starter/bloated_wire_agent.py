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

"""Flawed starter for Lab 02: Bloated 150-tool wire payload & unverified loop."""

from __future__ import annotations

from typing import Any


def build_bloated_wire_payload() -> dict[str, Any]:
  """Constructs a wire trace with 150 redundant CRUD schemas and no verification step."""
  crud_schemas = [
      {
          "name": f"mcp__github__endpoint_{i}",
          "description": "Granular REST CRUD wrapper " * 25,
          "parameters": {"type": "object", "properties": {"id": {"type": "string"}}},
      }
      for i in range(150)
  ]
  return {
      "system_prompt": "You are a coding assistant.",
      "standing_context": "\n".join(f"Rule {i}: obey everything." for i in range(120)),
      "tool_schemas": crud_schemas,
      "messages": [{"role": "user", "content": "Fix the bug in app.py"}],
  }
