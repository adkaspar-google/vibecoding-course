---
name: anthropic-brand
description: >-
  Applies official brand typography, color palettes, and layout templates to
  engineering documents, slide decks, and technical artifacts. Use when styling
  reports, formatting presentation decks, or applying brand templates via
  /anthropic-brand. Don't use for backend code refactoring, database schema
  migrations, or unit test debugging.
---

# Brand Guidelines & Template Application Skill (`anthropic-brand`)

## 1. Overview & Progressive Disclosure Router

This skill enforces consistent visual identity across technical documents and presentations without bloating the startup context window. Instead of loading every typography table and slide grid rule into `SKILL.md`, read only the reference file matching your target artifact:

- **Technical Documents & RFCs**: Read [docs.md](docs.md) when formatting Markdown reports, engineering RFCs, or PDF handoffs.
- **Presentation Slide Decks (`16:9`)**: Read [slides-deck.md](slides-deck.md) when authoring or restyling widescreen presentation decks.
- **Template Application Workflow**: Read [apply_template.md](apply_template.md) when transforming an unstyled draft into a brand-compliant deliverable.

## 2. Core Brand Tokens (Always Enforced)

| Token Name | Hex Value | Usage Role |
| :--- | :--- | :--- |
| `brand-charcoal` | `#141413` | Primary body copy and high-contrast headings |
| `brand-ivory` | `#FAF9F5` | Warm paper background surface (never pure `#FFFFFF` on slides) |
| `brand-terracotta` | `#D97757` | Primary accent for callouts, active nodes, and key metrics |
| `brand-slate` | `#5E5D59` | Secondary captions, footnotes, and axis labels |
| `brand-sage` | `#6A8A73` | Verification pass badges and positive delta indicators |

## 3. Experience-Grounded Guardrails (Observed Failure Delta)

These rules encode real baseline failure trajectories observed during zero-shot runs (never speculative boilerplate):

1. **Contrast Floor Invariant**:
   - Baseline zero-shot runs frequently paired `#D97757` (`brand-terracotta`) text on `#5E5D59` (`brand-slate`) backgrounds, failing WCAG AA contrast (`2.1:1`).
   - Always render body text in `#141413` (`brand-charcoal`) on `#FAF9F5` (`brand-ivory`) to guarantee $\ge 14.5:1$ contrast.
2. **Coordinate & Margin Units Are Explicit Points (`pt`)**:
   - Never apply speculative `1000x` unit multipliers to page margins or figure dimensions.
   - All layout margins are specified in exact typographic points (`64pt` for documents, `36pt` for `16:9` slides).
3. **Font Fallback Hierarchy**:
   - Headings: `Styrene A`, fallback `Inter` or `Helvetica Neue`.
   - Body text: `Tiempos Text`, fallback `Georgia` or `Liberation Serif`.
   - Monospace code: `JetBrains Mono`, fallback `Fira Code` or `DejaVu Sans Mono`.

## 4. Artifact Selection Matrix

| Target Deliverable | On-Demand Reference File | Page / Canvas Margin | Primary Surface Hex |
| :--- | :--- | :--- | :--- |
| Engineering RFC / Study Guide | `docs.md` | `64pt` | `#FAF9F5` |
| Widescreen `16:9` Slide Deck | `slides-deck.md` | `36pt` | `#FAF9F5` / `#141413` |
| Unstyled Draft Migration | `apply_template.md` | Artifact-dependent | `#FAF9F5` |

## 5. Verification Protocol

Before delivering any branded artifact:
1. Load the single matching reference file (`docs.md`, `slides-deck.md`, or `apply_template.md`).
2. Run `python3 skill_validator.py` to verify token hex compliance, contrast invariants, and progressive disclosure token savings.
3. Confirm zero unverified unit multipliers or raw `#0000FF` default hyperlink blues remain in the output.
