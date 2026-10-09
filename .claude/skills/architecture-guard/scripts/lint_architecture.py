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

"""Remediation-aware structural linter helper for architecture-guard skill."""

from __future__ import annotations

import sys


def format_violation(source_file: str, forbidden_import: str) -> str:
  return (
      f"[VIOLATION] '{source_file}' imports forbidden module '{forbidden_import}'. "
      "[WHY] Domain modules must remain pure and isolated from infrastructure I/O. "
      "[HOW TO FIX] Inject a typing.Protocol port defined in 'domain/ports.py'."
  )


if __name__ == "__main__":
  if len(sys.argv) == 3:
    print(format_violation(sys.argv[1], sys.argv[2]))
  sys.exit(0)
