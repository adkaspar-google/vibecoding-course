# `slides/` — 36-Slide Widescreen Deck & 7-Module End-to-End Video Curriculum

This directory contains the complete widescreen (`16:9`) presentation slide deck, tripartite speaker notes, and the pipeline that renders the narrated `1080p` step-by-step lecture videos for **`Vibe-Coding-Course`** (*From Vibe Coding to Agentic Engineering: Antigravity (`agy`) & Claude Code (`claude`)*).

## 1. Files in `slides/`

- **[`Vibe_Coding_Course_Slides.pdf`](./Vibe_Coding_Course_Slides.pdf)**: Compiled 36-slide widescreen (`16:9`) presentation PDF covering Foundations + Labs 01–06 step-by-step across both the `agy` and `claude` tracks.
- **[`Vibe_Coding_Course_Slides.tex`](./Vibe_Coding_Course_Slides.tex)**: Editable LaTeX/TikZ source for all 36 slides.
- **[`SPEAKER_NOTES.md`](./SPEAKER_NOTES.md)**: Complete 36-slide instructor script with `PURPOSE`, `VERBAL SCRIPT`, and `TRANSITION` for every slide.
- **[`build_video.py`](./build_video.py)**: Automated parallel TTS + FFmpeg video synthesis pipeline that builds both the 7 standalone module MP4s (`modules/`) and the master full-course video `Vibe_Coding_Course_Lecture.mp4`.

> [!NOTE]
> The rendered videos (`Vibe_Coding_Course_Lecture.mp4`, 30 min / ≈47 MB, and the 7 module MP4s, ≈6–9 MB each) are **not tracked in git**. Download them from the course's release assets, or regenerate them locally with the recipe in §3.

## 2. Step-by-Step Module Videos (`slides/modules/`)

| Module | Video File | Slide Range | Topics & Lab Walkthrough |
| :--- | :--- | :--- | :--- |
| **Module 01** | `modules/Module_01_Foundations_and_Dual_Harnesses.mp4` | Slides 01–06 | Why Pure Vibe Coding Collapses, Joshi's Code as a Model of Understanding, Wittgenstein's Two Theories of Language (*Early Picture Theory* vs. *Late Meaning-as-Use / Language as Action*), Kief Morris's Why/How Loops, `agy` vs. `claude` Architecture Mapping, and `self_diagnose_all.sh` |
| **Module 02 (Lab 01)** | `modules/Module_02_Lab01_Domain_Vocabulary_and_Language_Games.mp4` | Slides 07–11 | **Lab 01 Step-by-Step**: Shared Domain Vocabulary & Coworker Clarification in `domain_ledger.py` (`REQ-0101..0106`), replacing float dicts with frozen `AccountId` & `MoneyCents`, double-entry `SettlementBatch`, `evaluate_request_readiness()`, and `./self_diagnose.sh` |
| **Module 03 (Lab 02)** | `modules/Module_03_Lab02_Persistent_Context_and_Auto_Memory.mp4` | Slides 12–16 | **Lab 02 Step-by-Step**: Persistent Context (`CLAUDE.md` with `@docs/*.md` vs. `GEMINI.md` + `.agents/rules/*.md`), Auto Memory (`MEMORY.md` 200-line/25KB cap vs. `KNOWLEDGE.md` Knowledge Items), `/context` (Claude Code) / `/stats` (Gemini CLI) & `/memory`, and `./self_diagnose.sh` |
| **Module 04 (Lab 03)** | `modules/Module_04_Lab03_Crafting_Skills_Manually.mp4` | Slides 17–21 | **Lab 03 Step-by-Step**: Skillsbench Empirical Proof (`+16.6 pp` curated vs. `-8.1` to `-11.5 pp` self-generated), `agentskills.io` 3-Level Progressive Disclosure, Building `anthropic-brand` (`SKILL.md`, `docs.md`, `slides-deck.md`, `apply_template.md`), and `./self_diagnose.sh` |
| **Module 05 (Lab 04)** | `modules/Module_05_Lab04_Eval_Viewer_Overload_and_SDT.mp4` | Slides 22–26 | **Lab 04 Step-by-Step**: Skill Catalog Overload & Trigger Confusion, Signal Detection Theory (`d'` Sensitivity & Criterion Bias `c`), `eval-viewer` With-Skill vs. Without-Skill Ablation (`delta_pass_rate`, `token_efficiency_ratio`), Pruning Redundant Skills, and `./self_diagnose.sh` |
| **Module 06 (Lab 05)** | `modules/Module_06_Lab05_Multi_Agent_Feature_Dev.mp4` | Slides 27–31 | **Lab 05 Step-by-Step**: Anthropic's 7-Phase `feature-dev` Pipeline, Phase-Gated Context Isolation (`code-explorer`, `code-architect`, `code-reviewer`), Phase 3 Clarifying Gate & Phase 6 Confidence-Scored Review (`>= 80`), and `./self_diagnose.sh` |
| **Module 07 (Lab 06)** | `modules/Module_07_Lab06_Plugins_MCP_and_SDD_Bridge.mp4` | Slides 32–36 | **Lab 06 Capstone Step-by-Step**: Skills vs. Plugins Decision Matrix, Cross-Branch Plugin Manifest (`plugin.json` + `mcp_config.json` + `hooks.json`), Bridging Vibe Coding to SDD (`VibeSpecBridge` -> 8-Section `SPEC.md`), and `./self_diagnose_all.sh` |

## 3. Regenerating the Deck and Videos Locally

```bash
# 1. Slides -> PDF -> 150 DPI PNG frames (needs pdflatex + poppler-utils)
cd slides
pdflatex -interaction=nonstopmode Vibe_Coding_Course_Slides.tex
pdflatex -interaction=nonstopmode Vibe_Coding_Course_Slides.tex
rm -rf png && mkdir -p png && pdftoppm -png -r 150 Vibe_Coding_Course_Slides.pdf png/slide

# 2. Pick ONE text-to-speech backend for the 36 narration tracks (needs ffmpeg on PATH)
export GEMINI_API_KEY=...            # Backend B: public Gemini API (gemini-2.5-flash-preview-tts), no SDK needed
# export GEMINI_TTS_BIN=/path/to/cli # Backend A: any CLI honoring `<cli> -output=<wav> tts -voice=<voice> "<text>"`
# export GEMINI_TTS_VOICE=Kore       # optional; default voice
# export GEMINI_TTS_MODEL=...        # optional; default gemini-2.5-flash-preview-tts

# 3. Synthesize audio/, render segments/, assemble modules/*.mp4 + Vibe_Coding_Course_Lecture.mp4
python3 build_video.py
```

`audio/slide-NN.wav` files are cached: delete a slide's `.wav` to re-synthesize only that narration after editing its `VERBAL SCRIPT` in `SPEAKER_NOTES.md`. Segments are always re-rendered from the current `png/` frames, so visual-only edits never need a TTS backend. The backend logic is covered offline by `tests/build_tools/test_build_video_tts.py`.
