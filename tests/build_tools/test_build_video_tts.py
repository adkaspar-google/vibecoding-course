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

"""Offline tests for the pluggable TTS backend in `slides/build_video.py` (no network)."""

from __future__ import annotations

import base64
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import wave

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD_VIDEO_PATH = REPO_ROOT / "slides" / "build_video.py"


def _load_build_video():
  spec = importlib.util.spec_from_file_location("build_video_under_test", BUILD_VIDEO_PATH)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


class _FakeHttpResponse(io.BytesIO):
  """Minimal context-manager stand-in for `urllib.request.urlopen(...)`."""

  def __enter__(self):
    return self

  def __exit__(self, *exc):
    self.close()
    return False


class TestBuildVideoTtsBackends(unittest.TestCase):
  """Backend selection, Gemini API request/response handling, and WAV output."""

  def setUp(self) -> None:
    self.bv = _load_build_video()

  def test_speaker_notes_yield_36_verbal_scripts(self) -> None:
    scripts = self.bv.parse_scripts(REPO_ROOT / "slides" / "SPEAKER_NOTES.md")
    self.assertEqual(len(scripts), 42)
    self.assertTrue(all(len(s) > 40 for s in scripts))

  def test_backend_selection_prefers_cli_then_api_then_none(self) -> None:
    bv = self.bv
    bv.TTS_CLI, bv.GEMINI_API_KEY = "/usr/bin/some-tts", None
    self.assertEqual(bv.select_tts_backend(), "cli")
    bv.TTS_CLI, bv.GEMINI_API_KEY = "/usr/bin/some-tts", "key"
    self.assertEqual(bv.select_tts_backend(), "cli")
    bv.TTS_CLI, bv.GEMINI_API_KEY = None, "key"
    self.assertEqual(bv.select_tts_backend(), "api")
    bv.TTS_CLI, bv.GEMINI_API_KEY = None, None
    self.assertEqual(bv.select_tts_backend(), "none")

  def test_missing_backend_raises_actionable_error(self) -> None:
    bv = self.bv
    bv.TTS_CLI, bv.GEMINI_API_KEY = None, None
    with tempfile.TemporaryDirectory() as tmpdir:
      bv.AUDIO_DIR = Path(tmpdir)
      with self.assertRaises(RuntimeError) as ctx:
        bv.synthesize_one_tts(7, "Narration for slide seven.")
    message = str(ctx.exception)
    self.assertIn("GEMINI_TTS_BIN", message)
    self.assertIn("GEMINI_API_KEY", message)
    self.assertIn("slide-07.wav", message)

  def test_cached_wav_short_circuits_without_any_backend(self) -> None:
    bv = self.bv
    bv.TTS_CLI, bv.GEMINI_API_KEY = None, None
    with tempfile.TemporaryDirectory() as tmpdir:
      bv.AUDIO_DIR = Path(tmpdir)
      (bv.AUDIO_DIR / "slide-03.wav").write_bytes(b"\0" * (bv.MIN_WAV_BYTES + 1))
      self.assertEqual(bv.synthesize_one_tts(3, "ignored"), (3, 0.0))

  def test_gemini_request_shape_matches_public_tts_api(self) -> None:
    bv = self.bv
    bv.TTS_CLI, bv.GEMINI_API_KEY, bv.VOICE = None, "test-key", "Kore"
    url, data, headers = bv.build_gemini_tts_request("Hello, learners.")
    self.assertTrue(url.startswith("https://generativelanguage.googleapis.com/v1beta/models/"))
    self.assertTrue(url.endswith(":generateContent"))
    self.assertEqual(headers["x-goog-api-key"], "test-key")
    body = json.loads(data)
    self.assertEqual(body["contents"][0]["parts"][0]["text"], "Hello, learners.")
    cfg = body["generationConfig"]
    self.assertEqual(cfg["responseModalities"], ["AUDIO"])
    self.assertEqual(
        cfg["speechConfig"]["voiceConfig"]["prebuiltVoiceConfig"]["voiceName"], "Kore"
    )

  def test_gemini_api_backend_writes_valid_pcm16_wav(self) -> None:
    bv = self.bv
    bv.TTS_CLI, bv.GEMINI_API_KEY = None, "test-key"
    pcm = bytes(48_000)  # 1 second of 24 kHz 16-bit mono silence (> MIN_WAV_BYTES)
    payload = {
        "candidates": [{
            "content": {
                "parts": [{
                    "inlineData": {
                        "mimeType": "audio/L16;codec=pcm;rate=24000",
                        "data": base64.b64encode(pcm).decode("ascii"),
                    }
                }]
            }
        }]
    }
    fake = _FakeHttpResponse(json.dumps(payload).encode("utf-8"))
    with tempfile.TemporaryDirectory() as tmpdir:
      wav_path = Path(tmpdir) / "slide-01.wav"
      with mock.patch.object(bv.urllib.request, "urlopen", return_value=fake) as urlopen:
        self.assertTrue(bv.tts_via_gemini_api(wav_path, "Welcome to the course."))
      req = urlopen.call_args.args[0]
      self.assertEqual(req.get_method(), "POST")
      self.assertEqual(req.get_header("X-goog-api-key"), "test-key")
      with wave.open(str(wav_path), "rb") as wf:
        self.assertEqual(wf.getnchannels(), 1)
        self.assertEqual(wf.getsampwidth(), 2)
        self.assertEqual(wf.getframerate(), 24000)
        self.assertEqual(wf.getnframes(), 24000)

  def test_gemini_api_backend_reports_malformed_payload_without_raising(self) -> None:
    bv = self.bv
    bv.TTS_CLI, bv.GEMINI_API_KEY = None, "test-key"
    fake = _FakeHttpResponse(json.dumps({"candidates": []}).encode("utf-8"))
    with tempfile.TemporaryDirectory() as tmpdir:
      wav_path = Path(tmpdir) / "slide-02.wav"
      with mock.patch.object(bv.urllib.request, "urlopen", return_value=fake):
        self.assertFalse(bv.tts_via_gemini_api(wav_path, "x"))
      self.assertFalse(wav_path.exists())


if __name__ == "__main__":
  unittest.main()
