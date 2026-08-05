# FL-01: Workflow Audit & Tooling Setup

**Phase**: Setup  
**Author**: Kerem Özcan  
**Date**: August 5, 2026  
**Framework Basis**: Ethan Mollick's *On-boarding your AI Intern* & Anthropic Academy's *AI Fluency: Framework & Foundations*

---

## 1. Weekly Workflow Audit Table

The following audit maps 12 recurring tasks from my weekly workflow across machine learning coursework, software development, and project management.

| Task # | Task Description | Classification | One-Line Rationale |
|---|---|---|---|
| 1 | Setting overall machine learning problem framing and core business goals | **Just me** | Requires subjective business judgment, alignment with stakeholders, and accountability that cannot be outsourced. |
| 2 | High-stakes code reviews and pull request approvals for core architecture | **Just me** | Code ownership, safety criticalities, and long-term architectural integrity require final human decision-making. |
| 3 | Writing boilerplate data preprocessing and Pandas cleaning scripts | **Delegate to AI with review** | Deterministic pandas operations are easily drafted by AI, but require human review for edge cases like NaNs or type casting. |
| 4 | Drafting docstrings, function comments, and API documentation | **Delegate to AI with review** | AI generates clear standard docstrings quickly, requiring brief human verification for domain correctness. |
| 5 | Initial Exploratory Data Analysis (EDA) & signal distribution tests | **Collaborate with AI** | Human guides the diagnostic hypothesis while AI rapidly executes statistical summaries and plot code. |
| 6 | Refactoring complex functions into modular, clean Python components | **Collaborate with AI** | Iterative pair programming balances AI's speed with human design choices and maintainability. |
| 7 | Debugging obscure Python/PyTorch runtime tracebacks and errors | **Collaborate with AI** | AI identifies root cause possibilities while human tests hypothesis against runtime context. |
| 8 | Formatting Markdown tables, lists, and LaTeX equations in reports | **Delegate to AI with review** | Repetitive syntax formatting is ideal for AI delegation, with human checking layout alignment. |
| 9 | Running daily smoke tests and standard unit test suites | **Fully automate** | Deterministic test executions run via shell scripts or CI workflows without requiring active human prompt engineering. |
| 10 | Generating initial synthetic data / mock data for unit tests | **Fully automate** | Scripted schema-based dummy data generation is fully automated without human intervention. |
| 11 | Drafting weekly research paper summaries and literature outlines | **Collaborate with AI** | AI helps outline key sections, while human ensures technical accuracy and synthesis of findings. |
| 12 | Conducting retrospective self-evaluation of model performance & errors | **Just me** | Honest critical reflection on model trade-offs and business impact requires human domain intuition. |

---

## 2. Free Toolkit Setup & Learning Evidence

### Tool Accounts Configured
- **Claude (Anthropic)**: Configured with Claude Projects for structured context management.
- **ChatGPT (OpenAI)**: Active account for cross-checking reasoning and prompt baseline comparisons.
- **Anthropic Academy**: Enrolled in *AI Fluency: Framework & Foundations*.

### Anthropic Academy Summary (Module 1: Foundations)
- **Key Takeaway 1 (The AI Intern Mental Model)**: Treat LLMs like capable but inexperienced interns—give explicit context, constraints, and instructions, but verify outputs rigorously.
- **Key Takeaway 2 (Prompt Precision)**: Use explicit role framing, target outputs, step-by-step reasoning requests, and negative constraints ("never do X").
- **Key Takeaway 3 (Human-in-the-Loop)**: Maintain active oversight on high-stakes tasks, auditing logic rather than blindly trusting plausible-sounding outputs.

---

## 3. Configured Claude Project

**Project Name**: `FlyRank ML Internship`  
**Purpose**: Central workspace for ML pipeline development, data auditing, and capstone research paper drafting.

```yaml
Custom Instructions:
  Identity & Role:
    - You are pair-programming with Kerem Özcan on the FlyRank ML Internship track.
    - Kerem is an ML intern working on search performance ranking, content refresh models, and DuckDB warehouse analytics.
  Tone & Style:
    - Professional, direct, concise, and technical.
    - Prefer clean code over long prose.
    - Avoid sycophancy or generic filler ("Sure, I can help!").
  Current Goals:
    - Build honest, transparent baseline models and machine learning classifiers.
    - Avoid data leakage (e.g. trend_pct or client ID leakage).
    - Maintain clean Git hygiene (no datasets committed to git).
  Strict Guardrails:
    - Always search the codebase before assuming a helper function or feature is missing.
    - Never invent fictitious dataset columns or fake API methods.
    - Always recommend verifying code with top-to-bottom notebook execution.
```

---

## 4. Target Audit Tasks & Success Definitions (For FL-02 to FL-04)

The following three tasks have been selected from the workflow audit for reuse in assignments FL-02 through FL-04:

### Target Task 1: Exploratory Data Analysis & Anomaly Detection (FL-02)
- **Description**: Analyzing search performance datasets to uncover non-intuitive relationships (e.g., search volume vs. impressions, CTR decay by position tier) and identifying data anomalies.
- **Measurable "Done Well" Definition**:
  1. Computes exact correlation matrices and group aggregations on clean datasets.
  2. Flags at least 2 non-obvious data gotchas (e.g., zero-filled GA4 metrics or CTR percentages exceeding 100%).
  3. Outputs clean visualization scripts (Matplotlib/Seaborn) that render without errors.

### Target Task 2: Baseline Model & Feature Pipeline Scripting (FL-03)
- **Description**: Building transparent, human-readable baseline rules and feature engineering pipelines for ranking declining pages.
- **Measurable "Done Well" Definition**:
  1. Implements a human-explainable baseline rule with explicit reason codes.
  2. Calculates exact Precision@K (e.g., Precision@50) and compares against base rate.
  3. Guarantees zero label leakage (verifies target label derives from non-feature columns).

### Target Task 3: Technical Markdown & Research Report Synthesis (FL-04)
- **Description**: Drafting structured research reports, methodology sections, and PDF summaries of ML model benchmark results.
- **Measurable "Done Well" Definition**:
  1. Report adheres to academic/technical structure (Abstract, Methodology, Results, Discussion).
  2. All numerical claims in text trace back exactly to committed JSON metrics files (`outputs/model_results.json`).
  3. Zero unverified or hallucinated claims; all limitations clearly stated.
