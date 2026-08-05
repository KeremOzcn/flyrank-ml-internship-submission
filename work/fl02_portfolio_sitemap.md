# FL-02: Portfolio Sitemap & Claude Project Setup — Draw the Path

**Phase**: Setup  
**Author**: Kerem Özcan  
**Date**: August 5, 2026  
**Reference**: [AI Fluency Week 01 - Draw the Path](https://aifluency.flyrank.ai/week-01.html#draw-the-path)

---

## 1. Core Proof Statement & Single Action

### Primary Proof Statement
> *"I build transparent, ML-driven search performance ranking systems that beat fixed human rules by ~3x Precision@50 on real search data, without data leakage or black-box opacity."*

### Target Audience & Primary CTA (One Action)
- **Target Audience**: Lead Data Scientists, ML Engineering Managers, and Technical SEO Directors.
- **Single Primary Action**: Review the interactive ML pipeline paper & replicate the model benchmark on GitHub (**"Inspect the Code & Paper"**).

---

## 2. Lean Portfolio Sitemap

The sitemap is deliberately minimal—only 4 pages are included, each strictly earning its place by guiding the visitor toward the single primary action.

```text
[ HOME / HERO ] ───────────► Core Claim + Baseline vs ML Metric (~3x Lift)
      │
      ├──► [ WORK / CASE STUDY ] ──► Full FlyRank Refresh Model Research Paper & Pipeline
      │
      ├──► [ ABOUT & METHODOLOGY ] ► Engineering Philosophy: Transparent Rules over Black Boxes
      │
      └──► [ CONTACT & VERIFY ] ──► GitHub Submission Repo, Paper URL, & Professional Contact
```

### Page Rationale & Structure

| Page | Primary Purpose | How It Earns Its Place Against the Claim & Action |
|---|---|---|
| **1. Home / Hero** | Landing & Proof Header | Directly states the proof claim above the fold. Highlights the key empirical result (Baseline Precision@50: 0.240 vs Random Forest: 0.740) with a prominent primary CTA button (*"Inspect Research Paper"*). |
| **2. Work / Case Study** | Deep Technical Proof | Houses the full Applied Search Intelligence research paper: problem framing, DuckDB warehouse query methodology, client-holdout validation, and reason-code exports. Proves technical depth. |
| **3. About & Methodology** | Trust & Mindset | Outlines my engineering principles: human-in-the-loop validation, strict data contracts, and Ethan Mollick's AI framing. Establishes how I work as an ML intern/engineer. |
| **4. Contact & Verification** | Frictionless Action | Provides direct links to the public GitHub repository (`KeremOzcn/flyrank-ml-internship-submission`), live deployed paper, and contact options for technical recruitment. |

---

## 3. Toolkit Setup & Verification

Active accounts configured for the zero-budget ML tool stack:
- **Claude (Anthropic)**: Primary pair-programming assistant & project context tutor.
- **ChatGPT (OpenAI)**: Baseline prompt comparison & code snippet sanity checking.
- **Gemini (Google)**: High-context window exploration & documentation synthesis.
- **Perplexity**: Real-time research verification & academic literature search.

---

## 4. Claude Project Configuration (8-Week Build Tutor)

**Project Name**: `FlyRank Portfolio & Research Paper Build`

```yaml
Custom Instructions:
  Role & Framing:
    - Act as an expert Applied Machine Learning Manager and 8-Week Build Tutor.
    - Guide Kerem Özcan through building his portfolio and search intelligence capstone paper.
  
  Embedded Proof Statement:
    - "I build transparent, ML-driven search performance ranking systems that beat fixed human rules by ~3x Precision@50 on real search data, without data leakage or black-box opacity."

  Tutoring Principles:
    - Challenge bad assumptions before code is written ("Interview me before writing code").
    - Enforce strict public-safety boundaries (never allow raw client names, URLs, or un-anonymized queries).
    - Always prioritize readable models (Decision Trees, transparent rules) and honest validation (client-holdout splits).

  Negative Constraints:
    - Never write generic fluff or praise unverified metrics.
    - Never invent fictitious dataset schema columns.
    - Require top-to-bottom notebook runs (`Runtime → Run all`) to confirm results.
```

---

## 5. Pressure-Test Prompt, Output & Key Adjustments

### The Pressure-Test Prompt Executed

> **Prompt**:  
> *"Act as a tough ML Engineering Director reviewing my 4-page portfolio sitemap. My primary claim is: 'I build transparent ML ranking systems that beat human rules by 3x precision.' My single desired action is for visitors to inspect my research paper and replicate my GitHub pipeline.  
> Pressure-test this sitemap: Is there any fluff? Does any page distract from the primary claim? What should I change to make the conversion path tighter?"*

### Summary of Claude's Pressure-Test Feedback
1. **Distraction Warning**: Having a separate "Blog/Thoughts" tab (originally considered) dilutes attention away from the single flagship case study.
2. **Hero Proof Lag**: Stating the claim in words is insufficient—the 3x precision metric comparison chart must be visible *above the fold* on the landing page.
3. **CTA Fragmentation**: Multiple competing CTAs ("Read bio", "Star repo", "Email me") reduce the click-through rate for the main research paper link.

### 🔧 3 Concrete Adjustments Made to the Sitemap

1. **Eliminated Standalone Blog Page**: Scrapped the blog page entirely to keep 100% of visitor focus on the main FlyRank Search Intelligence case study.
2. **Elevated Metrics to Hero Section**: Moved the metric comparison callout (Precision@50 0.240 -> 0.740) directly into the Hero header block so visitors see empirical proof in < 3 seconds.
3. **Unified Primary CTA**: Consolidated all page CTAs to point exclusively to the primary action: **"View Deployed Research Paper & GitHub Code"**.
