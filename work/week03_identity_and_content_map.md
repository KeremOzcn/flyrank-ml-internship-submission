# Week 3 — Consistency, Not Talent

**Author**: Kerem Özcan
**Date**: September 9, 2026
**Presented version (submit this URL)**: https://claude.ai/code/artifact/9b06a949-5937-458d-9f07-431f547511fa

This file is the plain-text copy. Paste section 4 into the Claude Project so every build week
repeats the same choices.

---

## 1. The one-line claim

> **I measure the baseline everyone assumes works — and report it when it loses to chance.**

### What it replaced, and why

FL-02 and FL-03 both carry the claim *"…beat fixed human rules by ~3× Precision@50"* (0.240 →
0.740). **Those numbers are not mine.** `git log -- outputs/` shows `outputs/model_results.json`
arriving in commit `4929633 "Initial release — FlyRank ML Internship starter"` — the template's own
reference pipeline, committed before any of my work. `task_evidence.json` records
`model_trained: false` and `held_out_evaluation: false`.

What my executed notebook measured: the stale-first rule reached **Precision@50 = 44.0%** (22 hits
in 50 slots) against a **60.4%** random-selection expectation on the same 21,758-page eligible
slice — a 16.4pp shortfall. The rule lost to chance.

FL-04 already retired the 3× headline for this reason. The Week 3 claim descends from FL-04's
evidence, not FL-02's. **Action required: FL-02 §1 and FL-03 §1–3 still assert the 3× claim and
should be corrected before anything links to them.**

---

## 2. Content map

Single action everything ladders to: **inspect the notebook on GitHub**.

| Page | Sections, in order | Named CTA |
|---|---|---|
| **1 · Home** | Claim → measured result (44.0% vs 60.4%, charted) → what that means → case teaser | Inspect the notebook |
| **2 · Work** (lead case) | The decision → data contract → the baseline and its score → the leak I planted and removed → limits | Open the executed notebook |
| **3 · How I work** | Baseline before model → leak-hunting → receipts → where AI helped | Read the prompt iteration log |
| **4 · Contact** | One line → repo → email | Inspect the repo |

### Still need to gather

- [ ] Real screenshot — executed notebook's Precision@50 cell with outputs visible
- [ ] Real screenshot — repository tree showing receipts beside claims
- [ ] ML-04 data-contract numbers (grain probe, row span, `IS TRUE` survivors) — **blocked on the Hugging Face token**
- [ ] Deployed paper URL — `submission/paper_url.txt` is still a placeholder
- [ ] A held-out result, once a model exists — nothing to show yet; do not imply otherwise

---

## 3. Identity kit

| Role | Choice |
|---|---|
| Headings | IBM Plex Sans 600 |
| Body | IBM Plex Sans 400 |
| Numbers, labels, code | IBM Plex Mono 500 |
| Ink (text) | `#16191C` — 16.4:1 on paper |
| Paper (background) | `#F6F7F5` |
| Main (rules, links, marks) | `#2A5D63` — 6.9:1 on paper |
| Accent (flagged shortfall only) | `#B4552F` — 4.6:1 on paper |

Logo / favicon: a baseline with three bars hanging beneath it, one falling further than the others.
Legible at 32px. Source SVG lives in the artifact above.

Dark-theme steps: paper `#111417`, ink `#EDEEEC`, main `#63B3AD`, accent `#E08A5F` (7.6:1 and
7.0:1 respectively on the dark surface).

---

## 4. Style note — paste this into the Claude Project

> Fonts: IBM Plex Sans for headings and body, IBM Plex Mono for every number, label and hex code.
> Colors: ink `#16191C` on paper `#F6F7F5`; slate teal `#2A5D63` for rules, links and marks; burnt
> orange `#B4552F` used *only* to flag a measured shortfall — never decoratively.
> Mood: a lab notebook. Generous margins, hairline rules, one accent per page, nothing decorative
> competing with the figures. If a visitor remembers the design instead of the number, it failed.

---

## 5. Image set and rejection note

**Kept (2):**
- The Precision@50 chart — every value traces to an executed cell (22/50, 13,152/21,758).
- The mark — geometry, not generation.

**Cut (3):**
- *AI-generated "dashboard" hero* — shows invented numbers. A portfolio arguing its figures are real
  cannot open on a picture of fake ones. Rejected on principle, before taste.
- *Abstract "neural network" graphic* — textbook AI slop; decorates without adding a fact, and is
  the look every other ML portfolio opens with.
- *A chart of the 0.240 → 0.740 result* — would have been the best-looking image on the site, which
  is why it needed checking. It plots the starter repo's pipeline, not mine. It nearly survived
  because it flattered me.

**Standing rule:** real captures outrank all of the above. Both keepers are placeholders until the
notebook screenshots on the gather-list exist — a capture of the actual executed cell carries
provenance a redrawn SVG cannot.
