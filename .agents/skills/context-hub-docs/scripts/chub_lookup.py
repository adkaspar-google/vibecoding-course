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

"""Local helper script for context-hub-docs skill lookup."""

from __future__ import annotations

import sys


DOCS = {
    "stripe/webhooks": "Use raw request.body bytes with Webhook.construct_event.",
    "openai/chat": "Use strict JSON schemas with additionalProperties=False.",
}


def main(argv: list[str]) -> int:
  if len(argv) < 2:
    print("Usage: chub_lookup.py <search|get> [arg]")
    return 1
  cmd = argv[1]
  arg = argv[2] if len(argv) > 2 else ""
  if cmd == "search":
    for k, v in DOCS.items():
      if arg.lower() in k.lower() or arg.lower() in v.lower():
        print(f"{k}: {v}")
    return 0
  if cmd == "get" and arg in DOCS:
    print(f"# {arg}\n{DOCS[arg]}")
    return 0
  return 1


if __name__ == "__main__":
  sys.exit(main(sys.argv))
