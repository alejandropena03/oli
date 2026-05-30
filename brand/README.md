# /oli Brand System

Production-ready `/brand` asset system for `/oli`, structured to compare 5 logo routes across 15 explorations and generate reusable exports, mockups, and review tooling.

## Structure

```text
/brand
  /routes
    /route-a-pragmatic-wordmark
    /route-b-command-slash
    /route-c-operator-grid
    /route-d-execution-layer
    /route-e-industrial-minimal
  /tokens
  /mockups
  /exports
  /brandbook
  /scripts
  README.md
```

## Brand direction

- Primary hypothesis: `Route B / Command Slash`
- Strong secondary: `Route C / Operator Grid`
- Safest enterprise route: `Route A / Pragmatic Wordmark`
- Best motion/app-icon behavior: `Route D / Execution Layer`
- Strongest premium restraint: `Route E / Industrial Minimal`

## Typography

- Display: `Barlow Condensed`
- UI/Body: `IBM Plex Sans`
- Mono/Command: `Space Mono`
- Fallback stack is defined in [`tokens/pragmatic-void.css`](./tokens/pragmatic-void.css)

Specimens to test:
- `/oli`
- `Hey /oli`
- `Run /oli`
- `Build with /oli`
- `No es otro chat. Es trabajo terminado.`

## Scoring rubric

Each route is scored from 1 to 5 on:

- distinctiveness
- legibility
- enterprise credibility
- consumer friendliness
- technical/operator feel
- scalability
- icon strength
- motion potential
- alignment with `/oli` values
- risk of looking generic

Open [`brandbook/logo-evaluation.html`](./brandbook/logo-evaluation.html) to review all 15 explorations.

## Export pipeline

The generator creates editable SVG source files first, then optional raster/vector exports.

### Requirements

Install Python dependencies:

```powershell
py -m pip install -r brand/scripts/requirements.txt
```

### Generate source assets

```powershell
py brand/scripts/generate_brand_system.py
```

### What the generator produces

- 15 logo explorations across 5 routes x 3 variations
- wordmark, icon, horizontal, and stacked lockups
- dark, light, monochrome, and transparent SVG variants
- HTML logo evaluation grid
- HTML brandbook
- hero mockups and landing mockup
- favicon, app icon, social icon, OG image, PNG, ICO, and PDF exports

## Usage rules

- Keep the slash structural and intentional.
- Preserve the cyan top caps that distinguish the lowercase `l`.
- Use command green only for success or execution-complete states.
- Use warning yellow only for warning/debug emphasis, never as a dominant brand color.
- Avoid distortion, excessive glow, mascot behavior, terminal clichés, and any rendering where `/oli` risks reading as `/0li`, `Ioli`, or `0li`.

## Recommendation framework

Do not select a winner based on taste alone. Compare:

- strategic truth
- product fit
- UI/system fit
- small-size behavior
- motion potential
- enterprise trust
- memorability
