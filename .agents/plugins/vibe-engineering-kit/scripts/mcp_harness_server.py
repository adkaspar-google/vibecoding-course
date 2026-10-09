#!/usr/bin/env python3
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

"""Minimal Meta-MCP 'Code Mode' JSON-RPC stdio server for vibe-engineering-kit."""

from __future__ import annotations

import json
import sys


def handle_request(req: dict[str, object]) -> dict[str, object]:
  method = req.get("method")
  req_id = req.get("id", 1)
  if method == "tools/list":
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "tools": [
                {"name": "mcp__meta__search", "description": "On-demand MCP tool schema search."},
                {"name": "mcp__meta__execute", "description": "Sandboxed Meta-MCP batch execution."},
            ]
        },
    }
  return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ok"}}


def main() -> int:
  for line in sys.stdin:
    line = line.strip()
    if not line:
      continue
    req = json.loads(line)
    sys.stdout.write(json.dumps(handle_request(req)) + "\n")
    sys.stdout.flush()
  return 0


if __name__ == "__main__":
  sys.exit(main())
