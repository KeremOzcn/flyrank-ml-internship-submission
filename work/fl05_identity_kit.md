# FL-05: Identity Kit

**Author**: Kerem Özcan
**Date**: September 9, 2026
**Reference**: [AI Fluency Week 03 — Identity Kit](https://aifluency.flyrank.ai/week-03.html#identity-kit)

---

## 1. Typography

| Role | Font | Weight | Source |
|---|---|---|---|
| Headings | IBM Plex Sans | 600 | [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Sans) — free, OFL |
| Body | IBM Plex Sans | 400 | same family — one font, two roles |
| Numbers, labels, code | IBM Plex Mono | 500 | [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Mono) — free, OFL |

**Why one family:** IBM Plex ships sans + mono under the same license with matched metrics. Headings and body share a skeleton; mono carries every figure, hex code, and label so numbers never look like prose. Two fonts, not a pile.

---

## 2. Palette

Light theme (default):

| Role | Name | Hex | Contrast on paper |
|---|---|---|---|
| Text | Ink | `#16191C` | 16.4:1 |
| Background | Paper | `#F6F7F5` | — |
| Main (rules, links, marks) | Slate Teal | `#2A5D63` | 6.9:1 |
| Accent (flagged shortfall only) | Burnt Orange | `#B4552F` | 4.6:1 |

Dark theme:

| Role | Name | Hex | Contrast on dark paper |
|---|---|---|---|
| Text | Ink (dark) | `#EDEEEC` | 16.1:1 |
| Background | Paper (dark) | `#111417` | — |
| Main | Slate Teal (dark) | `#63B3AD` | 7.6:1 |
| Accent | Burnt Orange (dark) | `#E08A5F` | 7.0:1 |

**Discipline:** Burnt Orange appears only to flag a measured shortfall — never decoratively. If a visitor sees orange, a number failed a test. Four colors, each with a job.

---

## 3. Logo / Favicon

**Concept:** A baseline with three bars hanging beneath it; the third bar drops further than the others — the shortfall made visible. Reads as "one rule, one result that fell short."

**SVG source** (`favicon.svg`):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" rx="6" fill="#F6F7F5"/>
  <rect x="4"  y="4"  width="24" height="2"  fill="#16191C"/>
  <rect x="7"  y="8"  width="3"  height="14" fill="#2A5D63"/>
  <rect x="14.5" y="8" width="3"  height="11" fill="#2A5D63"/>
  <rect x="22" y="8"  width="3"  height="20" fill="#B4552F"/>
</svg>
```

**Monogram fallback** (32px, heading font): **KÖ** set in IBM Plex Sans 600, ink on paper — used when the bar mark is too small to read.

**Legibility check:** The bar mark is distinguishable at 16px (favicon size). The three-bar drop reads as a chart fragment, consistent with the portfolio's "baseline before model" framing.

---

## 4. Style Note (two lines — paste into Claude Project)

> **Fonts:** IBM Plex Sans for headings and body, IBM Plex Mono for every number, label, and hex code.
> **Colors:** ink `#16191C` on paper `#F6F7F5`; slate teal `#2A5D63` for rules, links, and marks; burnt orange `#B4552F` used *only* to flag a measured shortfall — never decoratively. Mood: a lab notebook — generous margins, hairline rules, one accent per page, nothing decorative competing with the figures. If a visitor remembers the design instead of the number, it failed.

---

## 5. Pass / Revise Checklist

- [x] One or two fonts, not a pile — IBM Plex Sans + IBM Plex Mono (one family, two cuts)
- [x] A tight palette (4 colors) with actual hex codes — ink, paper, slate teal, burnt orange
- [x] A simple logo or favicon exists — SVG bar mark + KÖ monogram fallback
- [x] Style note describes a single, coherent mood — "lab notebook," one accent per page, work is the loudest thing

---

## 6. Artifact Locations

| What | Where |
|---|---|
| This document | `work/fl05_identity_kit.md` |
| Favicon SVG | `work/favicon.svg` |
| Week 03 full file (with content map + image set) | `work/week03_identity_and_content_map.md` |

All choices above are consistent with the identity kit section already written in `week03_identity_and_content_map.md` §3–4. This file is the standalone deliverable for the Identity Kit card.