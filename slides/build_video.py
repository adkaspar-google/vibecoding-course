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
"""Builds the 7 Step-by-Step Module Videos and the Master 36-Slide Course Lecture Video.

Pipeline:
1. Parses all 36 `VERBAL SCRIPT` entries from `SPEAKER_NOTES.md`.
2. Synthesizes `audio/slide-01.wav` .. `audio/slide-36.wav` in parallel through a pluggable
   TTS backend (voice `Kore` by default):
     - `GEMINI_TTS_BIN=<cli>`  any CLI honoring `<cli> -output=<wav> tts -voice=<voice> "<text>"`
     - `GEMINI_API_KEY=<key>`  the public Gemini API (`gemini-2.5-flash-preview-tts`, REST via urllib)
   Existing `audio/*.wav` files are reused, so re-rendering slides never needs a backend.
3. Renders `segments/seg-01.mp4` .. `segments/seg-36.mp4` in parallel via `ffmpeg` (`1920x1080`).
4. Concatenates each module's slides into 7 standalone MP4 videos under `modules/`:
   - `Module_01_Foundations_and_Dual_Harnesses.mp4` (Slides 01-06)
   - `Module_02_Lab01_Vocabulary_and_Language_Games.mp4` (Slides 07-11)
   - `Module_03_Lab02_Persistent_Context_and_Auto_Memory.mp4` (Slides 12-16)
   - `Module_04_Lab03_Crafting_Skills_Manually.mp4` (Slides 17-21)
   - `Module_05_Lab04_Eval_Viewer_Overload_and_SDT.mp4` (Slides 22-26)
   - `Module_06_Lab05_Multi_Agent_Feature_Dev.mp4` (Slides 27-31)
   - `Module_07_Lab06_Plugins_MCP_and_SDD_Bridge.mp4` (Slides 32-36)
5. Concatenates all 36 segments into `Vibe_Coding_Course_Lecture.mp4`.

The rendered MP4s are release assets (not tracked in git); see `slides/README.md`.
"""

import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave

SLIDES_DIR = pathlib.Path(__file__).resolve().parent
NOTES_PATH = SLIDES_DIR / "SPEAKER_NOTES.md"
PNG_DIR = SLIDES_DIR / "png"
AUDIO_DIR = SLIDES_DIR / "audio"
SEG_DIR = SLIDES_DIR / "segments"
MODULES_DIR = SLIDES_DIR / "modules"
MASTER_VIDEO = SLIDES_DIR / "Vibe_Coding_Course_Lecture.mp4"

# --- TTS backend configuration (first configured backend wins) -----------------------------
TTS_CLI = os.environ.get("GEMINI_TTS_BIN")  # Backend A: external CLI (see contract above)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Backend B: public Gemini API key
TTS_MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
VOICE = os.environ.get("GEMINI_TTS_VOICE", "Kore")
GEMINI_TTS_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
MIN_WAV_BYTES = 10_000
NO_BACKEND_HELP = (
    "No TTS backend is configured and audio/*.wav is incomplete. Choose one:\n"
    "  A) export GEMINI_TTS_BIN=/path/to/tts-cli   "
    "# must honor: <cli> -output=<wav> tts -voice=<voice> \"<text>\"\n"
    "  B) export GEMINI_API_KEY=<your key>          "
    "# public Gemini API, no extra dependencies (https://aistudio.google.com/apikey)\n"
    "  C) skip synthesis and download the pre-rendered MP4 release assets (see slides/README.md)."
)

MODULES = [
    ("Module_01_Foundations_and_Dual_Harnesses.mp4", 1, 6),
    ("Module_02_Lab01_Vocabulary_and_Language_Games.mp4", 7, 11),
    ("Module_03_Lab02_Persistent_Context_and_Auto_Memory.mp4", 12, 16),
    ("Module_04_Lab03_Crafting_Skills_Manually.mp4", 17, 21),
    ("Module_05_Lab04_Eval_Viewer_Overload_and_SDT.mp4", 22, 26),
    ("Module_06_Lab05_Multi_Agent_Feature_Dev.mp4", 27, 31),
    ("Module_07_Lab06_Plugins_MCP_and_SDD_Bridge.mp4", 32, 36),
]


def parse_scripts(md_path: pathlib.Path) -> list[str]:
  text = md_path.read_text(encoding="utf-8")
  pattern = re.compile(r"-\s+\*\*VERBAL SCRIPT:\*\*\s*(.+)")
  scripts = [m.group(1).strip() for m in pattern.finditer(text)]
  if not scripts:
    raise RuntimeError(f"No VERBAL SCRIPT entries found in {md_path}")
  return scripts


def _wav_is_complete(wav_path: pathlib.Path) -> bool:
  return wav_path.exists() and wav_path.stat().st_size > MIN_WAV_BYTES


def select_tts_backend() -> str:
  """Returns 'cli', 'api', or 'none' depending on the configured environment."""
  if TTS_CLI:
    return "cli"
  if GEMINI_API_KEY:
    return "api"
  return "none"


def tts_via_cli(wav_path: pathlib.Path, script: str) -> bool:
  """Backend A: any CLI honoring `<cli> -output=<wav> tts -voice=<voice> "<text>"`."""
  cmd = [TTS_CLI, f"-output={wav_path}", "tts", f"-voice={VOICE}", script]
  res = subprocess.run(cmd, capture_output=True, text=True)
  return res.returncode == 0 and _wav_is_complete(wav_path)


def _pcm_rate_from_mime(mime_type: str) -> int:
  m = re.search(r"rate=(\d+)", mime_type or "")
  return int(m.group(1)) if m else 24000


def write_pcm16_wav(wav_path: pathlib.Path, pcm_bytes: bytes, sample_rate: int) -> None:
  """Wraps raw 16-bit little-endian mono PCM into a WAV container for ffmpeg."""
  with wave.open(str(wav_path), "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(pcm_bytes)


def build_gemini_tts_request(script: str) -> tuple[str, bytes, dict[str, str]]:
  """Builds the public Gemini API `generateContent` request for one narration track."""
  url = GEMINI_TTS_ENDPOINT.format(model=TTS_MODEL)
  body = {
      "contents": [{"parts": [{"text": script}]}],
      "generationConfig": {
          "responseModalities": ["AUDIO"],
          "speechConfig": {
              "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}
          },
      },
  }
  headers = {
      "Content-Type": "application/json",
      "x-goog-api-key": GEMINI_API_KEY or "",
  }
  return url, json.dumps(body).encode("utf-8"), headers


def decode_gemini_tts_response(payload: dict) -> tuple[bytes, int]:
  """Extracts (pcm_bytes, sample_rate) from a Gemini `generateContent` AUDIO response."""
  parts = payload["candidates"][0]["content"]["parts"]
  inline = next(p["inlineData"] for p in parts if "inlineData" in p)
  return base64.b64decode(inline["data"]), _pcm_rate_from_mime(inline.get("mimeType", ""))


def tts_via_gemini_api(wav_path: pathlib.Path, script: str) -> bool:
  """Backend B: public Gemini API text-to-speech (no SDK dependency)."""
  url, data, headers = build_gemini_tts_request(script)
  req = urllib.request.Request(url, data=data, headers=headers, method="POST")
  try:
    with urllib.request.urlopen(req, timeout=180) as resp:
      payload = json.load(resp)
  except urllib.error.HTTPError as err:
    detail = err.read().decode("utf-8", errors="replace")[:300]
    print(f"  [TTS] Gemini API HTTP {err.code} for {wav_path.name}: {detail}", flush=True)
    return False
  except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as err:
    print(f"  [TTS] Gemini API transport error for {wav_path.name}: {err}", flush=True)
    return False
  try:
    pcm, rate = decode_gemini_tts_response(payload)
  except (KeyError, IndexError, StopIteration, ValueError) as err:
    print(f"  [TTS] Unexpected Gemini API payload for {wav_path.name}: {err}", flush=True)
    return False
  write_pcm16_wav(wav_path, pcm, rate)
  return _wav_is_complete(wav_path)


def synthesize_one_tts(idx: int, script: str) -> tuple[int, float]:
  wav_path = AUDIO_DIR / f"slide-{idx:02d}.wav"
  if _wav_is_complete(wav_path):
    return idx, 0.0
  backend = select_tts_backend()
  if backend == "none":
    raise RuntimeError(f"Missing {wav_path.name}. {NO_BACKEND_HELP}")
  synth = tts_via_cli if backend == "cli" else tts_via_gemini_api
  t0 = time.time()
  for attempt in range(1, 6):
    if synth(wav_path, script):
      return idx, time.time() - t0
    time.sleep(1.5 * attempt)
  raise RuntimeError(f"Failed TTS for slide {idx:02d} after 5 attempts via '{backend}' backend")


def render_one_segment(idx: int) -> tuple[int, float]:
  png_path = PNG_DIR / f"slide-{idx:02d}.png"
  wav_path = AUDIO_DIR / f"slide-{idx:02d}.wav"
  seg_path = SEG_DIR / f"seg-{idx:02d}.mp4"
  if not png_path.exists():
    raise FileNotFoundError(f"Missing slide PNG: {png_path}")
  if not wav_path.exists():
    raise FileNotFoundError(f"Missing slide WAV: {wav_path}")

  probe = subprocess.run(
      [
          "ffprobe",
          "-v",
          "error",
          "-show_entries",
          "format=duration",
          "-of",
          "default=noprint_wrappers=1:nokey=1",
          str(wav_path),
      ],
      capture_output=True,
      text=True,
      check=True,
  )
  dur = float(probe.stdout.strip()) + 0.75
  cmd = [
      "ffmpeg",
      "-y",
      "-loop",
      "1",
      "-i",
      str(png_path),
      "-i",
      str(wav_path),
      "-vf",
      "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,format=yuv420p",
      "-af",
      "apad=pad_dur=0.75",
      "-c:v",
      "libx264",
      "-preset",
      "veryfast",
      "-tune",
      "stillimage",
      "-r",
      "24",
      "-c:a",
      "aac",
      "-b:a",
      "192k",
      "-ar",
      "24000",
      "-t",
      f"{dur:.2f}",
      "-movflags",
      "+faststart",
      str(seg_path),
  ]
  subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  return idx, dur


def concat_segments(out_path: pathlib.Path, start_idx: int, end_idx: int) -> float:
  concat_file = SEG_DIR / f"concat_{start_idx:02d}_{end_idx:02d}.txt"
  lines = [f"file '{SEG_DIR / f'seg-{i:02d}.mp4'}'" for i in range(start_idx, end_idx + 1)]
  concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
  subprocess.run(
      [
          "ffmpeg",
          "-y",
          "-f",
          "concat",
          "-safe",
          "0",
          "-i",
          str(concat_file),
          "-c",
          "copy",
          "-movflags",
          "+faststart",
          str(out_path),
      ],
      check=True,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
  )
  probe = subprocess.run(
      [
          "ffprobe",
          "-v",
          "error",
          "-show_entries",
          "format=duration",
          "-of",
          "default=noprint_wrappers=1:nokey=1",
          str(out_path),
      ],
      capture_output=True,
      text=True,
      check=True,
  )
  return float(probe.stdout.strip())


def main() -> int:
  AUDIO_DIR.mkdir(parents=True, exist_ok=True)
  SEG_DIR.mkdir(parents=True, exist_ok=True)
  MODULES_DIR.mkdir(parents=True, exist_ok=True)

  scripts = parse_scripts(NOTES_PATH)
  print(f"[1/4] Parsed {len(scripts)} slide scripts from {NOTES_PATH.name}", flush=True)

  print("[2/4] Synthesizing TTS audio tracks in parallel (max_workers=4)...", flush=True)
  with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {
        pool.submit(synthesize_one_tts, i, script): i
        for i, script in enumerate(scripts, start=1)
    }
    for fut in as_completed(futures):
      idx, elapsed = fut.result()
      status = "cached" if elapsed == 0.0 else f"synthesized in {elapsed:.1f}s"
      print(f"  [TTS] Slide {idx:02d}/{len(scripts):02d}: {status}", flush=True)

  print("[3/4] Rendering 1080p MP4 slide segments in parallel (max_workers=6)...", flush=True)
  total_dur = 0.0
  with ThreadPoolExecutor(max_workers=6) as pool:
    futures = {pool.submit(render_one_segment, i): i for i in range(1, len(scripts) + 1)}
    for fut in as_completed(futures):
      idx, dur = fut.result()
      total_dur += dur
      print(f"  [SEG] Slide {idx:02d}/{len(scripts):02d}: {dur:.1f}s", flush=True)

  print("[4/4] Assembling 7 Module Videos + Master Full-Course Video...", flush=True)
  for mod_name, s_idx, e_idx in MODULES:
    mod_path = MODULES_DIR / mod_name
    dur = concat_segments(mod_path, s_idx, e_idx)
    size_mb = mod_path.stat().st_size / (1024 * 1024)
    print(
        f"  [MODULE] {mod_name} (Slides {s_idx:02d}-{e_idx:02d}): "
        f"{dur:.1f}s ({dur/60:.1f} min), {size_mb:.2f} MB",
        flush=True,
    )

  master_dur = concat_segments(MASTER_VIDEO, 1, len(scripts))
  master_mb = MASTER_VIDEO.stat().st_size / (1024 * 1024)
  print(
      f"  [MASTER] {MASTER_VIDEO.name} (Slides 01-{len(scripts):02d}): "
      f"{master_dur:.1f}s ({master_dur/60:.1f} min), {master_mb:.2f} MB",
      flush=True,
  )
  return 0


if __name__ == "__main__":
  sys.exit(main())
