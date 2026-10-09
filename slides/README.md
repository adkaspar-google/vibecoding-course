# `slides/` — 42-Slide Widescreen Deck & 8-Module End-to-End Video Curriculum

This directory contains the complete widescreen (`16:9`) presentation slide deck, tripartite speaker notes, and the pipeline that renders the narrated `1080p` step-by-step lecture videos for **`Vibe-Coding-Course`** (*From Vibe Coding to Agentic Harness Engineering: Antigravity (`agy`) & Claude Code (`claude`)*).

## 1. Files in `slides/`

- **[`Vibe_Coding_Course_Slides.pdf`](./Vibe_Coding_Course_Slides.pdf)**: Compiled 42-slide widescreen (`16:9`) presentation PDF covering Phase 1 (Vibe Coding Foundations & Daily Workflows, Modules 1–4, Slides 01–19) and Phase 2 (Harness Engineering & Agentic Loops, Modules 5–8, Slides 20–42) across both the `agy` and `claude` branches.
- **[`Vibe_Coding_Course_Slides.tex`](./Vibe_Coding_Course_Slides.tex)**: Editable LaTeX/TikZ source for all 42 slides.
- **[`SPEAKER_NOTES.md`](./SPEAKER_NOTES.md)**: Complete 42-slide instructor script with `PURPOSE`, `VERBAL SCRIPT`, and `TRANSITION` for every slide.
- **[`build_video.py`](./build_video.py)**: Automated parallel TTS + FFmpeg video synthesis pipeline that builds both the 8 standalone module MP4s (`modules/`) and the master full-course video `Vibe_Coding_Course_Lecture.mp4`.

> [!NOTE]
> The rendered videos (`Vibe_Coding_Course_Lecture.mp4` and the 8 module MP4s under `modules/`) are release assets (**not tracked in git**). Download them from the course's release assets, or regenerate them locally with the recipe in §3.

## 2. Step-by-Step Module Videos (`slides/modules/`)

| Phase | Module | Video File | Slide Range | Topics & Lab Walkthrough |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Module 01 (Lab 01)** | `modules/Module_01_Language_Evolution_Skills_Map_and_Lab01.mp4` | Slides 01–07 | Why Language Produces Code & Actions (Unmesh Joshi/Martin Fowler, Wittgenstein's *Tractatus* vs. *Philosophical Investigations*, Andrew Ng's SE Fundamentals), Visual Feedback Loop (`Human -> Computer -> Chatbot -> Agent -> Harness -> AI Model`), Six Eras (2022–2026), All 3 SearchIntel Model-Pace Charts (`N=143`), 4-Pillar AI Engineering Skills Map, Ladder of Earned Autonomy, and **Lab 01 (`prompt_steerer.py`)** |
| **Phase 1** | **Module 02 (Lab 02)** | `modules/Module_02_Agent_Loop_Agy_Claude_101_and_Lab02.mp4` | Slides 08–11 | 3-Layer Agent Stack (`aisuite` & CS146S Lecture 2), Swiss Army Knife Primitives vs. 150-Tool Bloat, Google Antigravity (`agy`) 101, Anthropic Claude Code (`claude`) 101, and **Lab 02 (`wire_trace_inspector.py`)** |
| **Phase 1** | **Module 03 (Lab 03)** | `modules/Module_03_RePPIT_Daily_Workflow_and_Lab03.mp4` | Slides 12–15 | Task Complexity vs. Workflow Rigor, Socratic `/grill-me`, the 5-Step `RePPIT` Loop (Orthogonal Proposals + Context Reset, `Out of Scope` Guardrail, Phase Model Routing, Reflection), `agy` vs. `claude` Execution & Time-Travel, and **Lab 03 (`reppit_orchestrator.py`)** |
| **Phase 1** | **Module 04 (Lab 04)** | `modules/Module_04_Context_Physics_Dumb_Zone_and_Lab04.mp4` | Slides 16–19 | Stateless Context Physics (`NextAction = LLM(ContextWindow)`), the 40% "Dumb Zone", Output-Redirection Backpressure (`> run.log 2>&1`) & `rendergit`, Frequent Intentional Compaction (FIC) & Leverage Pyramid, and **Lab 04 (`context_compactor.py`)** |
| **Phase 2** | **Module 05 (Lab 05)** | `modules/Module_05_Context_Primitives_Memory_and_Lab05.mp4` | Slides 20–23 | Cybernetic 2x2 Control Matrix (Guidance vs. Sensors $\times$ Computational vs. Inferential), 150-Instruction Cliff (`ETH Zurich` & `IFScale`), 60-Line `CLAUDE.md`/`GEMINI.md` Map Rule, Cross-Session Memory (`MEMORY.md` vs. `KNOWLEDGE.md`), and **Lab 05 (`context_compiler.py`)** |
| **Phase 2** | **Module 06 (Lab 06)** | `modules/Module_06_Skills_Chub_Meta_MCP_and_Lab06.mp4` | Slides 24–29 | `agentskills.io` 3-Level Progressive Disclosure, Andrew Ng's `context-hub` (`chub` Feedback Loop), Ergonomic MCP Tool Design & Meta-MCP "Code Mode" (`>90%` Token Savings), `SkillsBench` Parts 1 & 2 (All 4 Charts: `+16.2pp` Curated vs. `-1.3pp` Self-Generated, Domain Gains, `2–3` Skill Sweet Spot, Cost Pareto), and **Lab 06 (`skill_and_mcp_harness.py`)** |
| **Phase 2** | **Module 07 (Lab 07)** | `modules/Module_07_Subagent_Firewalls_Council_and_Lab07.mp4` | Slides 30–34 | Subagents as Context Firewalls (`0%` Parent Exploration Bloat), 7-Phase `feature-dev` Pipeline, CS146S Actionable PR Triage (`Must Fix` / `Recommended` / `Consider`), Karpathy's `llm-council`, `git worktree` vs. Colocated Jujutsu (`jj`), and **Lab 07 (`subagent_council.py`)** |
| **Phase 2** | **Module 08 (Lab 08)** | `modules/Module_08_Governance_Linters_Autoresearch_and_Lab08.mp4` | Slides 35–42 | 4-Tier "Governed by Design" Hooks (`PreToolUse` Exit Code `2`) & `Temporal` Replay, Databricks `Omnigent` Meta-Harness, Custom Remediation Linters (`[VIOLATION] -> [WHY] -> [HOW TO FIX]`), Karpathy's `autoresearch` & `program.md` Ratchet, Why "Lights-Off" Software Factories Fail, Anthropic Recursive Self-Improvement Parts 1 & 2 (All 4 Charts), and **Lab 08 (`autoresearch_harness.py`)** |

## 3. Regenerating the Deck and Videos Locally

```bash
# 1. Slides -> PDF -> 1920x1080 PNG frames (needs pdflatex + poppler-utils)
cd slides
pdflatex -interaction=nonstopmode Vibe_Coding_Course_Slides.tex
pdflatex -interaction=nonstopmode Vibe_Coding_Course_Slides.tex
rm -rf png && mkdir -p png && pdftoppm -png -r 120 Vibe_Coding_Course_Slides.pdf png/slide

# 2. Pick ONE text-to-speech backend for the 42 narration tracks (needs ffmpeg on PATH)
export GEMINI_API_KEY=...            # Backend B: public Gemini API (gemini-2.5-flash-preview-tts), no SDK needed
# export GEMINI_TTS_BIN=/path/to/cli # Backend A: any CLI honoring `<cli> -output=<wav> tts -voice=<voice> "<text>"`
# export GEMINI_TTS_VOICE=Kore       # optional; default voice
# export GEMINI_TTS_MODEL=...        # optional; default gemini-2.5-flash-preview-tts

# 3. Synthesize audio/, render segments/, assemble modules/*.mp4 + Vibe_Coding_Course_Lecture.mp4
python3 build_video.py
```

`audio/slide-NN.wav` files are cached: delete a slide's `.wav` to re-synthesize only that narration after editing its `VERBAL SCRIPT` in `SPEAKER_NOTES.md`. Segments are always re-rendered from the current `png/` frames, so visual-only edits never need a TTS backend. The backend logic is covered offline by `tests/build_tools/test_build_video_tts.py`.
