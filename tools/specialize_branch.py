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
"""Regenerates a single-harness branch (`agy` or `claude`) from `main`.

`main` is the dual-harness superset. This tool derives a specialized branch by:
  1. `git checkout -B <branch> main`
  2. removing the OTHER harness's files (`git rm -r`)
  3. stripping the OTHER harness's `## <X> Track` section from every lab WALKTHROUGH.md
  4. inserting a branch banner under the README title
  5. committing the result

Usage (from the repository root, with a clean working tree):
    python3 tools/specialize_branch.py agy
    python3 tools/specialize_branch.py claude
    git checkout main

Never hand-edit `agy` or `claude`: change `main`, then re-run this tool for both branches.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

HARNESSES = {
    "agy": {
        "track": "Antigravity",
        "remove": [
            ".claude", ".claude-plugin", "CLAUDE.md",
            "playbooks/CLAUDE_CODE_PLAYBOOK.md", "tests/claude_track",
        ],
        "banner": (
            "> **You are on the `agy` branch** — it ships only the Antigravity / Gemini CLI harness "
            "(`GEMINI.md`, `AGENTS.md`, `.agents/`, `playbooks/ANTIGRAVITY_PLAYBOOK.md`, "
            "`tests/agy_track/`). Switch to `claude` for the Claude Code harness, or `main` for both "
            "side by side."
        ),
        "message": "agy: Antigravity / Gemini CLI native track (removes Claude Code harness files)",
    },
    "claude": {
        "track": "Claude Code",
        "remove": [
            ".agents", "GEMINI.md", "AGENTS.md",
            "playbooks/ANTIGRAVITY_PLAYBOOK.md", "tests/agy_track",
        ],
        "banner": (
            "> **You are on the `claude` branch** — it ships only the Claude Code harness "
            "(`CLAUDE.md`, `.claude/`, `.claude-plugin/`, `playbooks/CLAUDE_CODE_PLAYBOOK.md`, "
            "`tests/claude_track/`). Switch to `agy` for the Antigravity / Gemini CLI harness, or "
            "`main` for both side by side."
        ),
        "message": "claude: Claude Code native track (removes Antigravity / Gemini CLI harness files)",
    },
}


def git(*args: str) -> str:
  return subprocess.run(
      ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
  ).stdout


def strip_track(text: str, track_name: str) -> str:
  """Removes `## <track_name> Track` (and its body) while keeping one `---` separator."""
  heading = f"## {track_name} Track"
  if heading not in text:
    raise RuntimeError(f"Heading not found: {heading}")
  pattern = re.compile(re.escape(heading) + r"\n.*?(?=(?:\n---\n\n## )|\Z)", re.S)
  out, count = pattern.subn("", text, count=1)
  if count != 1:
    raise RuntimeError(f"Could not remove section: {heading}")
  out = re.sub(r"---\n\n\n---\n\n", "---\n\n", out)  # removed a middle section
  out = re.sub(r"\n---\n\n\Z", "\n", out)  # removed the final section
  return out.rstrip("\n") + "\n"


def main(argv: list[str]) -> int:
  if len(argv) != 2 or argv[1] not in HARNESSES:
    print(__doc__)
    return 2
  keep = argv[1]
  other = "claude" if keep == "agy" else "agy"
  spec, other_spec = HARNESSES[keep], HARNESSES[other]

  if git("status", "--porcelain").strip():
    print("Working tree is not clean; commit or stash first.", file=sys.stderr)
    return 1

  git("checkout", "-q", "-B", keep, "main")
  git("rm", "-r", "-q", *spec["remove"])

  for walkthrough in sorted(REPO_ROOT.glob("labs/lab_*/WALKTHROUGH.md")):
    before = walkthrough.read_text(encoding="utf-8")
    after = strip_track(before, other_spec["track"])
    assert f"## {spec['track']} Track" in after, walkthrough
    assert f"## {other_spec['track']} Track" not in after, walkthrough
    assert "self_diagnose.sh work" in after, walkthrough
    walkthrough.write_text(after, encoding="utf-8")
    print(f"  stripped '{other_spec['track']} Track' from {walkthrough.relative_to(REPO_ROOT)}")

  readme = REPO_ROOT / "README.md"
  lines = readme.read_text(encoding="utf-8").splitlines()
  if not lines or not lines[0].startswith("# "):
    raise RuntimeError("README.md must start with an H1 title")
  lines[1:1] = ["", spec["banner"]]
  readme.write_text("\n".join(lines) + "\n", encoding="utf-8")

  git("add", "-A")
  git("commit", "-q", "-m", spec["message"])
  print(f"Branch '{keep}' regenerated from main: {git('rev-parse', '--short', 'HEAD').strip()}")
  print("Run `git checkout main` when you are done.")
  return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv))
