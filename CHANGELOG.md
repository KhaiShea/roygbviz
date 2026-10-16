# Changelog

## Unreleased

- `end_labels` text is now regular weight by default (was bold), with a little more space after the dot. Pass `bold=True` for the old look, or `bold="medium"`/`"semibold"` if your font has it.

## 0.1.0 (2026-10-17)

First release.

- Twelve colours from one rainbow: nine for models, three for stages (STT, LLM, TTS).
- Light and dark modes, five lightness levels each.
- Diverging scale (cold to hot), shading helpers (`shade`, `shade_map`), and `stroke` for sizes.
- plotnine theme, direct end labels, and a 45-chart mega test.
- Colourblind-safe set not built yet.
