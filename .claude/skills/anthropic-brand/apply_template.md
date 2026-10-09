# Deterministic Template Application Procedure (`apply_template.md`)

Loaded on demand from `SKILL.md` when transforming an existing unstyled draft into a brand-compliant document or slide deck.

## Step-by-Step Workflow
1. **Classify Artifact Type**: Inspect whether the target is a `doc` (`docs.md`) or `slides` (`slides-deck.md`).
2. **Map Color Palette**: Replace unbranded `#FFFFFF` backgrounds with `#FAF9F5` (`brand-ivory`), `#000000` body text with `#141413` (`brand-charcoal`), and primary highlights with `#D97757` (`brand-terracotta`).
3. **Apply Font Stack**: Bind `heading_font = "Styrene A"`, `body_font = "Tiempos Text"`, and `code_font = "JetBrains Mono"`.
4. **Verify Invariants**: Confirm `margin_pt` (`64` for `doc`, `36` for `slides`) and verify zero ungrounded unit multipliers were applied.
