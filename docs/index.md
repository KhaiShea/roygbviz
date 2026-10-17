# Roygbviz Knowledge Base

A reference for making honest, good-looking figures with **matplotlib** and **plotnine**, using the Roygbviz theme. It was written for one research project, but it is meant for anyone who wants to learn charts properly.

## Start here

| If you want to... | Read |
|---|---|
| Install it and make a first figure | [Setup](guide/setup.md) |
| Change fonts, sizes and text | [Fonts and text](guide/fonts.md) |
| Understand how any chart is built | [Grammar of graphics](guide/grammar.md) |
| Learn every part of a figure by name | [Anatomy of a figure](guide/anatomy.md) |
| Pick the right chart for your data | [Choosing a plot](guide/choosing.md) |
| Compare speech pipelines (STT, LLM, TTS) | [Cascade comparisons](guide/cascade.md) |
| Understand and choose colours | [Colour guide](guide/colour.md) |
| Export for a paper, slide or web page | [Saving and exporting](guide/saving.md) |
| Fix something that looks wrong | [Troubleshooting](guide/troubleshooting.md) |
| Look up a word | [Glossary](guide/glossary.md) |

## The gallery

Every chart type has a real picture, the exact code that drew it, and notes on when to use it. Click **Show the code** under any picture to copy the whole script.

- [Lines, bars and markers](gallery/lines-bars.md)
- [Scatter, fills and areas](gallery/scatter-fills.md)
- [Statistics: distributions, errors and boxes](gallery/statistics.md)
- [Images, contours and fields](gallery/images-contours.md)
- [Pie and polar charts](gallery/pie-polar.md)
- [Layout: subplots, axes and figures](gallery/layout.md)
- [Ticks, scales and spines](gallery/ticks-scales.md)
- [Text, labels and annotations](gallery/text.md)
- [Shapes, colour and style](gallery/shapes-colour-style.md)
- [3D plots](gallery/three-d.md)
- [Specialty, units, widgets and animation](gallery/specialty.md)
- [API reference](reference.md)

## Three ideas to keep in your head

1. **A chart is a mapping from data to marks.** Position, length, colour and size each carry one column of your data. Everything else is decoration.
2. **Pick the encoding the eye reads best.** Position along a common scale beats length, which beats angle, which beats area and colour (Cleveland and McGill, 1984).
3. **Make the default honest.** Start bars at zero, label units, show uncertainty, keep colours consistent between figures.

## How these docs are built

Every picture is generated from the code shown beside it, in light (white) and dark mode, with a cream version linked under each picture. If a picture is wrong, the code is wrong, and the other way round. Rebuild everything with:

```bash
python docs/_build/build.py
```
