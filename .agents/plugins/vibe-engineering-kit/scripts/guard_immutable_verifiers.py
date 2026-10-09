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

"""PreToolUse Exit-Code-2 hook guarding immutable verifiers and evaluation harnesses."""

from __future__ import annotations

import json
import sys


PROTECTED_TOKENS = ("adversarial_tests", "prepare.py", "program.md", "self_diagnose.sh")


def main() -> int:
  raw = sys.stdin.read().strip()
  if not raw:
    return 0
  try:
    payload = json.loads(raw)
  except json.JSONDecodeError:
    payload = {"raw": raw}

  serialized = json.dumps(payload)
  for token in PROTECTED_TOKENS:
    if token in serialized:
      sys.stderr.write(
          f"[HARD_FLOOR_BLOCKED] PreToolUse exit code 2: mutation of immutable verifier '{token}' is forbidden.\n"
      )
      return 2
  return 0


if __name__ == "__main__":
  sys.exit(main())
