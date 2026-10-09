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

"""Unit tests for Lab 06 skill_and_mcp_harness.py."""

from __future__ import annotations

import unittest

import skill_and_mcp_harness as smh


class TestSkillAndMcpHarness(unittest.TestCase):
  """User unit tests for Lab 06."""

  def test_chub_and_code_mode_savings(self) -> None:
    reg = smh.ChubRegistry()
    reg.register_doc(
        smh.ChubDocEntry(
            doc_id="stripe/webhooks",
            lang="py",
            version="2026.1",
            content_md="Use `Webhook.construct_event(payload, sig_header, secret)`.",
        )
    )
    reg.annotate("stripe/webhooks", "Pass raw request.body bytes, never parsed JSON dict.")
    doc = reg.get("stripe/webhooks", lang="py", with_annotations=True)
    self.assertIn("UNTRUSTED_LOCAL_ANNOTATION", doc)
    self.assertIn("raw request.body bytes", doc)


if __name__ == "__main__":
  unittest.main()
