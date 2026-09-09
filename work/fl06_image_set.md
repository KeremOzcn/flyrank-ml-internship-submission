# FL-06: Image Set & Rejection Note — Kill Your Darlings

**Author**: Kerem Özcan
**Date**: September 9, 2026
**Reference**: [AI Fluency Week 03 — Kill Your Darlings](https://aifluency.flyrank.ai/week-03.html)

---

## 1. Images the portfolio actually needs

Matched to the content map (4 pages, single action: inspect the notebook).

| # | Image | Page | Source | Status |
|---|---|---|---|---|
| 1 | Precision@50 result chart (44.0% vs 60.4% expectation) | Home / Hero | Real capture from executed notebook cell | **Placeholder** — needs screenshot of the actual cell output |
| 2 | Favicon / logo mark (bar chart with shortfall) | All pages (browser tab, header) | SVG, geometry — not generated | **Done** (`work/favicon.svg`) |
| 3 | Repository tree showing receipts beside claims | Work / Case Study | Real screenshot of GitHub repo file tree | **Not yet gathered** |
| 4 | Prompt iteration log excerpt | How I Work | Real screenshot or clean code block | **Not yet gathered** |

That's it. Four images. No hero photo, no abstract background, no team stock photo.

---

## 2. Images rejected (and why)

### Rejected 1: AI-generated "dashboard" hero

**What it was:** A generated image of a sleek analytics dashboard with charts, KPIs, and a dark UI — the kind of thing every ML portfolio opens with.

**Why it was cut:** It shows invented numbers. A portfolio whose entire argument is "my figures are real and measured" cannot open on a picture of fake ones. Rejected on principle, before taste. The numbers on that dashboard do not trace to any executed cell.

**The lesson:** If the image contains data, the data must be yours. Decoration that looks like evidence is worse than no decoration.

---

### Rejected 2: Abstract "neural network" graphic

**What it was:** A generated image of glowing nodes and connections — the standard "AI" visual.

**Why it was cut:** Textbook AI slop. It decorates without adding a single fact. It is the look every other ML portfolio opens with, which means it makes the site less memorable, not more. The portfolio's mood is "lab notebook" — a neural network graphic is the opposite of that.

**The lesson:** If you can't point to a specific fact the image communicates, it doesn't belong.

---

### Rejected 3: Chart of the 0.240 → 0.740 result

**What it was:** A clean bar chart showing Precision@50 improving from 0.240 (baseline) to 0.740 (random forest) — the starter repo's reference pipeline numbers.

**Why it was cut:** This would have been the best-looking image on the site, which is exactly why it needed checking. Those numbers come from the starter repo's `outputs/model_results.json`, committed before any of my work. My notebook measured 44.0% Precision@50, not 74.0%. The chart plots someone else's pipeline and would pass as mine. It nearly survived because it flattered me.

**The lesson:** The most dangerous image is the one that makes you look good. Check provenance before aesthetics.

---

## 3. Standing rule

> **Real captures outrank everything.** Both kept images are placeholders until the notebook screenshots on the gather-list exist. A screenshot of the actual executed cell carries provenance a redrawn SVG cannot. No generated image replaces a real capture of real output.

---

## 4. Consistent style for connective images

When generated images are used for connective tissue (not work proof), they must share:
- The portfolio palette: ink `#16191C`, paper `#F6F7F5`, slate teal `#2A5D63`, burnt orange `#B4552F`
- IBM Plex Mono for any labels or numbers in the image
- No gradients, no glassmorphism, no 3D — flat geometry only
- One accent per image, same discipline as the page

Currently no generated connective images are planned. If one is needed later, it follows the rule above.

---

## 5. Pass / Revise Checklist

- [x] Image list matches the content map — 4 images for 4 pages
- [x] Work shown with real captures, not AI stand-ins — all work images are screenshots of real output (or placeholders pending capture)
- [x] Rejection note shows genuine judgment — three rejections, each with a specific reason beyond "I liked this one"
- [x] Rejected image that flattered the author was caught and cut (the 0.240 → 0.740 chart)
- [x] Gather list is honest — placeholders and missing items are flagged, not hidden

---

## 6. Artifact Locations

| What | Where |
|---|---|
| This document | `work/fl06_image_set.md` |
| Identity kit (sibling deliverable) | `work/fl05_identity_kit.md` |
| Favicon SVG | `work/favicon.svg` |
| Full Week 3 file (all three assignments) | `work/week03_identity_and_content_map.md` |