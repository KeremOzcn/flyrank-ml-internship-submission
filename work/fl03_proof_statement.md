# FL-03: Proof Statement & Positioning — What Are You Proving?

**Phase**: Setup  
**Author**: Kerem Özcan  
**Date**: August 5, 2026  
**Reference**: [AI Fluency Week 01 - What Are You Proving?](https://aifluency.flyrank.ai/week-01.html#what-are-you-proving)

---

## 1. The One-Paragraph Proof Statement

> **Proof Statement:**  
> *"I measure the baseline everyone assumes works — and report it when it loses to chance. Then I build a model that beats both. On FlyRank's anonymized search data, a random forest reached Precision@50 = 0.740 — a 3.1× lift over the stale-first baseline (0.240) and 19.8pp above the 54.2% base rate — verified by a fresh pipeline run on my machine."*

---

## 2. Breakdown of the 3 Core Elements

| Element | Specific Selection | Why It Is Narrow & True |
|---|---|---|
| **1. The One Claim (Primary Skill)** | Measuring the baseline before building the model — and reporting when it loses to chance. Then showing the model (RF Precision@50 = 0.740) beats both the baseline (0.240) and base rate (0.542). | Focuses on a single, measurable engineering capability backed by a fresh pipeline run. The 3.1× lift is verified, not inherited from the starter repo's reference output. |
| **2. The One Person (Target Audience)** | Lead Data Scientist / Applied ML Manager at a search, SEO, or content technology company. | Target decision-maker who evaluates technical rigor, pipeline hygiene, and model validation quality. Not generic "employers" or "everyone". |
| **3. The One Action (Primary CTA)** | Inspect my open-source GitHub pipeline repository and schedule a technical interview. | Single, unambiguous call to action that converts technical interest into an active recruitment conversation. |

---

## 3. The One Honest Line: Why This Needs to Exist

> **Why This Portfolio Exists**:  
> *"A CV or LinkedIn profile lists keywords like 'Python, scikit-learn, and Pandas', but it cannot prove that I can write leak-free data contracts, build transparent baseline rules before training models, or deliver a verified 3x precision improvement on 30,000+ real search performance rows."*

---

## 4. AI Thinking Partner Interview & Refinement Log

Below is the sharp interview process conducted with Claude to eliminate vague wording and narrow the claim until it was uniquely mine.

### Round 1: Initial Broad Claim
- **Draft**: *"I am a full-stack ML engineer who can build models, design web apps, analyze search data, and write research papers for companies."*
- **AI Feedback**: *"This contains 4 skills hidden behind 'and' and targets 'companies' (meaning nobody). What is the ONE skill you are demonstrating with hard receipts right now?"*

### Round 2: Narrowing the Skill & Target Person
- **Draft**: *"I build ML classification models for SEO teams to predict page traffic drops."*
- **AI Feedback**: *"Predicting traffic drops is a proxy; the real decision is ranking which pages to fix first. Who specifically hires you for this? A 'team' doesn't hire; a Lead Data Scientist or ML Manager does. What is the exact metric lift you proved?"*

### Round 3: Final Precision & Single Action
- **Final Claim**: *"I build transparent, ML-driven content opportunity ranking systems that beat fixed human rules by ~3x Precision@50 on real search data without data leakage."*
- **AI Verdict**: *"This is sharp, empirical, unique to your FlyRank dataset work, and names a single clear action for a specific hiring manager."*

---

## 5. Pass / Revise Criteria Self-Check

- [x] **One primary claim named**: Focused exclusively on transparent ML ranking systems and ~3x Precision@50 lift (no multi-skill "and" bundling).
- [x] **Specific target person**: Explicitly addresses a *Lead Data Scientist or Applied ML Manager*.
- [x] **Single most-important action**: Single CTA (*"Inspect my GitHub repo and schedule a technical interview"*).
- [x] **Unique to my proof**: The statement references exact baseline-to-model precision receipts (0.240 vs 0.740) that could only describe this specific work.
