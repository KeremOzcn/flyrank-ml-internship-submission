# FL-07: The Through-Line — Map Content & CTAs

**Author**: Kerem Özcan
**Date**: September 9, 2026
**Reference**: [AI Fluency Week 03 — The Through-Line](https://aifluency.flyrank.ai/week-03.html)

---

## 1. The one-line claim

> **I measure the baseline everyone assumes works — and report it when it loses to chance.**

### Why this claim, and not the earlier one

FL-02 and FL-03 carried *"beat fixed human rules by ~3× Precision@50"* (0.240 → 0.740). Those numbers are the starter repo's reference pipeline — `git log -- outputs/` shows `model_results.json` arriving in the initial commit, before any of my work. `task_evidence.json` records `model_trained: false` and `held_out_evaluation: false`.

What my executed notebook actually measured: the stale-first rule reached **Precision@50 = 44.0%** (22 hits in 50 slots) against a **60.4%** random-selection expectation on the same 21,758-page eligible slice. The rule lost to chance by 16.4 percentage points.

The claim follows the evidence, not the other way around. It is one sentence, and it is the only sentence a visitor needs to remember.

---

## 2. Content map

**Single action everything ladders to:** Inspect the notebook on GitHub.

| Page | Sections, in order | Named CTA |
|---|---|---|
| **1 · Home** | Claim → measured result (44.0% vs 60.4%, charted) → what that means → case teaser | Inspect the notebook |
| **2 · Work** (lead case) | The decision → data contract → the baseline and its score → the leak I planted and removed → limits | Open the executed notebook |
| **3 · How I work** | Baseline before model → leak-hunting → receipts → where AI helped | Read the prompt iteration log |
| **4 · Contact** | One line → repo → email | Inspect the repo |

### Page-by-page rationale

**Home:** The claim is the first thing. Below it, the measured result with a chart — not a headline number from someone else's pipeline. Then one sentence on what it means (the easy rule is worse than random for this task). The case teaser links to Work.

**Work:** The lead (and only) case is the FlyRank content-refresh framing. Sections follow the analytical order: what I decided to do, what data I used, what the baseline scored, what I caught (a leakage proxy I planted and removed), and where the result stops being conclusive. The CTA opens the executed notebook — not a paper that doesn't exist yet.

**How I work:** Four short sections explaining the method: baseline before model, leak-hunting as a habit, receipts beside claims, and where AI assisted. The CTA points to the prompt iteration log, which shows the actual back-and-forth.

**Contact:** One line, the repo, an email. No form, no social links, no "let's connect" — just the action.

### CTA ladder

```
Home ──"Inspect the notebook"──► Work
Work ──"Open the executed notebook"──► GitHub notebook
How I Work ──"Read the prompt iteration log"──► GitHub log
Contact ──"Inspect the repo"──► GitHub repo
```

Every CTA points to the same place: the evidence. No CTA sends a visitor to a bio, a blog, or a deployed paper that doesn't exist.

---

## 3. Still need to gather

Honest list — the build week cannot start if these are hidden.

- [ ] **Real screenshot** — executed notebook's Precision@50 cell with outputs visible
- [ ] **Real screenshot** — repository tree showing receipts beside claims
- [ ] **ML-04 data-contract numbers** (grain probe, row span, `IS TRUE` survivors) — blocked on the Hugging Face token
- [ ] **Deployed paper URL** — `submission/paper_url.txt` is still a placeholder
- [ ] **A held-out result**, once a model exists — nothing to show yet; do not imply otherwise

---

## 4. Pass / Revise Checklist

- [x] The claim is single and memorable — one sentence, not a paragraph
- [x] Every page has ordered sections and a named CTA, laddering up to one action
- [x] The gather-list is honest — missing items are flagged, not hidden
- [x] The lead case is the strongest case — only one case, placed first on Work
- [x] No page exists without earning its place against the claim and action

---

## 5. Artifact Locations

| What | Where |
|---|---|
| This document | `work/fl07_content_map.md` |
| Identity kit (sibling deliverable) | `work/fl05_identity_kit.md` |
| Image set & rejection note (sibling deliverable) | `work/fl06_image_set.md` |
| Full Week 3 file (all three assignments combined) | `work/week03_identity_and_content_map.md` |