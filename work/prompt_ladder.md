# Prompt Ladder — Explaining an ML Result Without Inventing One

**Track:** FlyRank ML internship · **Author:** Kerem Özcan · **Run date:** September 8, 2026

## Task and experimental setup

Turn the current content-refresh task-framing work into a portfolio case for an Applied ML Manager. The practical test is whether a stranger can understand the problem, decisions, measured result, and limits without being sold a model that was never trained.

AI assistance was used to execute and compare six prompts. Every output below is a real, unedited response from a separate Codex CLI invocation. V0 is a deliberately weak prompt for this track, not a claimed historical message. Each next prompt was chosen after reading the preceding result. There were six successful model runs and no output-selection rerolls.

**Controls:** Same installed CLI (0.148.0), same default model selection, same read-only scratch directory outside the repo, same fixed developer instruction, fresh ephemeral session each time, and no prior outputs included. User config was ignored. No tools or repository access occurred in the runner, as checked in its event logs. Only the cumulative user prompt changed.

Fixed developer instruction, identical in all six runs:

> Respond only to the supplied prompt. Do not use tools, inspect files, browse, or ask other agents. Treat this as a standalone writing task.

**Limits:** The CLI still supplied its standard runtime instructions/skill catalog; these were not six bare API requests. V0 and V4 emitted skill-description truncation warnings but completed successfully. The saved events did not expose the resolved model ID or temperature, so this report does not claim an exact model version, deterministic replication, or a statistically established effect of each layer. One run per prompt shows observed differences, not proof that a change will always help.

The factual context added in V2 comes from saved outputs of [the ML-03 notebook](notebooks/w02_ml_task_framing.ipynb). The model received that context text, not the dataset or notebook file.

## Side-by-side comparisons

| Transition | Previous output | New output | Observed difference |
|---|---|---|---|
| V0 → V1 | “Please share the project’s README” | “I developed a machine-learning prioritization system” | More complete-looking; less trustworthy. Missing facts became invented achievements. |
| V1 → V2 | “Historical refresh outcomes were used” | “No machine-learning model was trained in the notebook.” | Real context corrected the central invented claim. |
| V2 → V3 | “I used a proxy rather than claiming true refresh benefit.” | “may instead favor high-traffic pages whose performance is comparatively stable.” | Audience targeting introduced an unsupported explanation and did not shorten the answer. |
| V3 → V4 | “whether prioritizing a page leads to measurable editorial impact.” | “a separate causal design would still be required” | Explicit constraints repaired the causal boundary. |
| V4 → V5 | Four sections: Problem / Approach / Result / What this established | Three sections: The problem / What I did and decided / What came of it | Better scan structure; shorter output; word cap slightly missed. |

## Six-run overview

| Run | Single added layer | Output words* | Verdict |
|---|---|---:|---|
| V0 | Weak baseline | 26 | Asks for missing inputs; no case |
| V1 | Clearer goal | 204 | Worse: invents achievements |
| V2 | Real context | 344 | Grounded numbers and no-model limit |
| V3 | Defined audience | 380 | Mixed: longer, speculative explanation |
| V4 | Constraints | 410 | Safer claims, but more verbose |
| V5 | Specified output format | 234 | Best observed balance; word cap slightly missed |

*Counts use whitespace splitting, including headings, Markdown tokens, and the Artifact line. Under this convention V5 is 234 words, four over the cap; other counting conventions may differ.

## V0 — Weak baseline

**Full prompt actually run:**

~~~text
Explain my ML project.
~~~

**Saved output — verbatim:**

> Please share the project’s README, code, notebook, architecture diagram, or a brief description. I’ll explain its goal, data flow, model, training/evaluation process, and key design choices.

- **What changed:** No layer yet. “Explain my ML project.” is a deliberately weak prompt for my current track, not a claimed recovered month-old message.
- **What actually improved:** No previous output exists. It usefully asked for a README or description instead of pretending it knew the project.
- **What still failed:** It produced no usable case, decision, or result. The prompt supplied neither project facts nor a clear deliverable.
- **What I would try next:** Add a clearer goal so it targets a portfolio case rather than an open-ended explanation.

## V1 — Clearer goal

**Exact addition to the previous prompt:**

~~~text
Goal: Write a portfolio case explaining the content-refresh prioritization problem, the approach taken, and the measured result.
~~~

**Full prompt actually run:**

~~~text
Explain my ML project.
Goal: Write a portfolio case explaining the content-refresh prioritization problem, the approach taken, and the measured result.
~~~

**Saved output — verbatim:**

> ## ML Content-Refresh Prioritization
>
> The project addressed a common SEO challenge: deciding which existing pages should be refreshed first. With a large content library, manually reviewing every page was slow, while prioritizing only by traffic decline overlooked pages with stronger recovery potential.
>
> I developed a machine-learning prioritization system that ranked pages according to their expected value from a refresh. The model combined signals such as traffic and ranking trends, content age, search demand, engagement, conversion value, and previous refresh performance. Historical refresh outcomes were used to estimate the likely uplift for each page, while business rules accounted for effort, strategic importance, and prediction confidence.
>
> The output was a ranked refresh queue rather than a simple “update/don’t update” classification. This made the system operationally useful: editors could focus limited capacity on pages with the highest expected return and understand the signals behind each recommendation.
>
> In the measured evaluation period, the prioritized cohort achieved **[X%] greater organic uplift**, generated **[Y] additional visits/conversions**, and reduced manual analysis time by **[Z%]** compared with the previous selection process.
>
> The project demonstrated how ML can turn content maintenance from a reactive, intuition-led workflow into a measurable allocation problem—helping teams invest editorial effort where it is most likely to produce results.

- **What changed:** Added only a clearer goal: explain the content-refresh problem, approach, and measured result as a portfolio case.
- **What actually improved:** It moved from requesting inputs to a recognizable case with a problem, ranked queue, and outcome paragraph.
- **What still failed:** This made factual reliability worse. It asserted “I developed a machine-learning prioritization system” and invented historical refresh outcomes, conversion value, and uplift modeling. [X%], [Y], and [Z%] are placeholders, not measured results.
- **What I would try next:** Supply the actual notebook facts before asking for more polish.

## V2 — Real context

**Exact addition to the previous prompt:**

~~~text
Context: This is Kerem Özcan's FlyRank internship task-framing notebook, completed with AI assistance. The starter CSV has 30,000 anonymized pages across 32 clients. One row is one content page. The task is ranking pages for editorial review, assuming 50 review slots per cycle. The eligible slice has 21,758 pages with impressions_90d >= 100 and impressions_prev_30d > 0. Binary relevance is is_declining_proxy = (trend_direction == "down"); down means a greater-than-20% impression fall between consecutive 30-day windows. There are no observed refresh-benefit outcomes. A fixed rule puts pages last updated at least 90 days ago first, then sorts by impressions_90d descending. It finds 22 proxy-positive pages in its top 50: Precision@50 = 44%. Uniform random selection from this same slice has expected Precision@50 = 60.4%. These are full-slice descriptive results, not a held-out model evaluation. No model was trained in this notebook. The notebook checks missing values and unique page IDs and saves executed outputs. Direct label fields are excluded from working signals, but retained 90-day metrics overlap the decline window. Future work is earlier feature windows, later outcomes, and held-out clients. Artifact: work/notebooks/w02_ml_task_framing.ipynb.
~~~

**Full prompt actually run:**

~~~text
Explain my ML project.
Goal: Write a portfolio case explaining the content-refresh prioritization problem, the approach taken, and the measured result.
Context: This is Kerem Özcan's FlyRank internship task-framing notebook, completed with AI assistance. The starter CSV has 30,000 anonymized pages across 32 clients. One row is one content page. The task is ranking pages for editorial review, assuming 50 review slots per cycle. The eligible slice has 21,758 pages with impressions_90d >= 100 and impressions_prev_30d > 0. Binary relevance is is_declining_proxy = (trend_direction == "down"); down means a greater-than-20% impression fall between consecutive 30-day windows. There are no observed refresh-benefit outcomes. A fixed rule puts pages last updated at least 90 days ago first, then sorts by impressions_90d descending. It finds 22 proxy-positive pages in its top 50: Precision@50 = 44%. Uniform random selection from this same slice has expected Precision@50 = 60.4%. These are full-slice descriptive results, not a held-out model evaluation. No model was trained in this notebook. The notebook checks missing values and unique page IDs and saves executed outputs. Direct label fields are excluded from working signals, but retained 90-day metrics overlap the decline window. Future work is earlier feature windows, later outcomes, and held-out clients. Artifact: work/notebooks/w02_ml_task_framing.ipynb.
~~~

**Saved output — verbatim:**

> ## Content-refresh prioritization at FlyRank
>
> During my FlyRank internship, I framed a ranking problem around a practical editorial constraint: if a team can review only 50 pages per cycle, which pages should receive attention first?
>
> The starter dataset contained 30,000 anonymized content pages across 32 clients, with one row per page. After requiring at least 100 impressions over 90 days and nonzero impressions in the previous 30-day window, 21,758 pages remained eligible.
>
> Because the dataset contained no observed outcomes showing whether refreshing a page improved its performance, I used a proxy rather than claiming true refresh benefit. A page was marked proxy-positive when its trend direction was “down,” representing an impression decline greater than 20% between consecutive 30-day windows.
>
> I evaluated a simple fixed prioritization rule:
>
> 1. Rank pages last updated at least 90 days ago ahead of newer pages.
> 2. Within that ordering, sort by 90-day impressions in descending order.
> 3. Select the first 50 pages for editorial review.
>
> The rule identified 22 declining pages in its top 50, giving a descriptive Precision@50 of 44%. However, the eligible population’s proxy-positive rate was 60.4%, so uniformly selecting 50 pages from the same slice would be expected to achieve 60.4% Precision@50. The heuristic therefore underperformed the random baseline on the chosen proxy.
>
> This is a useful negative result. It shows that combining content age with traffic volume does not necessarily prioritize pages currently exhibiting the defined decline signal. It also demonstrates why even intuitive editorial rules need explicit baselines before being treated as effective.
>
> These figures are full-slice descriptive results, not held-out model performance. No machine-learning model was trained in the notebook. Direct label fields were excluded from the working signals, but the retained 90-day metrics still overlap the period used to define decline, so the setup is not suitable for causal or deployment claims.
>
> The notebook also validates missing values and page-ID uniqueness and preserves executed outputs for reproducibility. The next step would be to construct features from earlier time windows, measure later refresh outcomes, and evaluate ranking performance on held-out clients.
>
> Artifact: `work/notebooks/w02_ml_task_framing.ipynb`

- **What changed:** Added only real context: dataset grain, eligible slice, proxy, baseline result, limitations, AI assistance, and artifact.
- **What actually improved:** The invented model disappears. It now says “No machine-learning model was trained” and reports 22/50 = 44% against a 60.4% random expectation. It recognizes the negative result and overlapping windows.
- **What still failed:** It omits AI assistance despite that fact being supplied. At 344 whitespace-delimited words, it reads like a notebook walkthrough. The intended reader is still unspecified.
- **What I would try next:** Specify an Applied ML Manager to test whether familiarity reduces introductory explanation.

## V3 — Defined audience

**Exact addition to the previous prompt:**

~~~text
Audience: An Applied ML Manager reviewing an internship portfolio who already understands ranking, proxy labels, and Precision@K.
~~~

**Full prompt actually run:**

~~~text
Explain my ML project.
Goal: Write a portfolio case explaining the content-refresh prioritization problem, the approach taken, and the measured result.
Context: This is Kerem Özcan's FlyRank internship task-framing notebook, completed with AI assistance. The starter CSV has 30,000 anonymized pages across 32 clients. One row is one content page. The task is ranking pages for editorial review, assuming 50 review slots per cycle. The eligible slice has 21,758 pages with impressions_90d >= 100 and impressions_prev_30d > 0. Binary relevance is is_declining_proxy = (trend_direction == "down"); down means a greater-than-20% impression fall between consecutive 30-day windows. There are no observed refresh-benefit outcomes. A fixed rule puts pages last updated at least 90 days ago first, then sorts by impressions_90d descending. It finds 22 proxy-positive pages in its top 50: Precision@50 = 44%. Uniform random selection from this same slice has expected Precision@50 = 60.4%. These are full-slice descriptive results, not a held-out model evaluation. No model was trained in this notebook. The notebook checks missing values and unique page IDs and saves executed outputs. Direct label fields are excluded from working signals, but retained 90-day metrics overlap the decline window. Future work is earlier feature windows, later outcomes, and held-out clients. Artifact: work/notebooks/w02_ml_task_framing.ipynb.
Audience: An Applied ML Manager reviewing an internship portfolio who already understands ranking, proxy labels, and Precision@K.
~~~

**Saved output — verbatim:**

> ## Content-refresh prioritization at FlyRank
>
> During my FlyRank internship, I framed content refresh as a ranking problem: given a limited editorial budget of 50 reviews per cycle, which pages should be reviewed first?
>
> The starter dataset contained 30,000 anonymized pages across 32 clients, with one row per content page. I restricted the analysis to 21,758 pages with at least 100 impressions over 90 days and nonzero impressions in the previous 30-day window. This removed pages with insufficient activity for a meaningful trend comparison.
>
> Because the dataset contained no observed outcomes showing whether a refresh improved performance, I could not define a true refresh-benefit target. Instead, I used a diagnostic proxy:
>
> `is_declining_proxy = (trend_direction == "down")`
>
> A page is classified as “down” when impressions fell by more than 20% between consecutive 30-day windows. This proxy identifies declining pages, not pages that would necessarily benefit from editorial intervention.
>
> I evaluated a fixed prioritization rule that:
>
> 1. Places pages last updated at least 90 days ago first.
> 2. Sorts pages within that ordering by 90-day impressions, descending.
>
> Among its top 50 pages, 22 were proxy-positive, giving a descriptive Precision@50 of 44%.
>
> For context, 60.4% of the eligible slice was proxy-positive, so uniform random selection from the same population would have an expected Precision@50 of 60.4%. The rule therefore underperformed random selection against the chosen proxy. This is still a useful result: recency and traffic alone did not concentrate declining pages and may instead favor high-traffic pages whose performance is comparatively stable.
>
> These numbers are full-slice diagnostics, not held-out model results. No model was trained in the notebook, and the exercise should not be interpreted as evidence of production ranking performance. Direct label fields were excluded from the working signals, but retained 90-day metrics overlap the period used to construct the decline proxy, so the setup is not yet suitable for leakage-safe predictive evaluation.
>
> The next step would be to convert the framing into a temporal learning problem: construct features from earlier windows, observe later outcomes such as recovery or incremental value after refresh, and evaluate on held-out clients. That would test both generalization and the decision that actually matters—whether prioritizing a page leads to measurable editorial impact.
>
> The executed analysis, including missing-value checks, page-ID uniqueness validation, and saved outputs, is documented in `work/notebooks/w02_ml_task_framing.ipynb`.

- **What changed:** Added only the audience: an Applied ML Manager who already knows ranking, proxies, and Precision@K.
- **What actually improved:** It exposes the exact proxy expression and uses the more specific phrase “leakage-safe predictive evaluation,” making the label easier to inspect.
- **What still failed:** The hoped-for brevity did not happen: 344 words became 380. It speculates that the rule may favor stable high-traffic pages without supporting analysis here, and suggests later outcomes plus held-out clients would test whether prioritization leads to editorial impact. That validation alone does not establish causal benefit. AI assistance is still omitted.
- **What I would try next:** Add factual constraints to prevent unsupported explanations and causal implications and preserve AI disclosure.

## V4 — Constraints

**Exact addition to the previous prompt:**

~~~text
Constraints: Use only the supplied facts. Do not invent model training, refresh outcomes, explanations for the rule's performance, or demonstrated business impact. Do not imply that temporal or client-held-out evaluation alone proves the causal effect of refreshing a page. Preserve the disclosure of AI assistance.
~~~

**Full prompt actually run:**

~~~text
Explain my ML project.
Goal: Write a portfolio case explaining the content-refresh prioritization problem, the approach taken, and the measured result.
Context: This is Kerem Özcan's FlyRank internship task-framing notebook, completed with AI assistance. The starter CSV has 30,000 anonymized pages across 32 clients. One row is one content page. The task is ranking pages for editorial review, assuming 50 review slots per cycle. The eligible slice has 21,758 pages with impressions_90d >= 100 and impressions_prev_30d > 0. Binary relevance is is_declining_proxy = (trend_direction == "down"); down means a greater-than-20% impression fall between consecutive 30-day windows. There are no observed refresh-benefit outcomes. A fixed rule puts pages last updated at least 90 days ago first, then sorts by impressions_90d descending. It finds 22 proxy-positive pages in its top 50: Precision@50 = 44%. Uniform random selection from this same slice has expected Precision@50 = 60.4%. These are full-slice descriptive results, not a held-out model evaluation. No model was trained in this notebook. The notebook checks missing values and unique page IDs and saves executed outputs. Direct label fields are excluded from working signals, but retained 90-day metrics overlap the decline window. Future work is earlier feature windows, later outcomes, and held-out clients. Artifact: work/notebooks/w02_ml_task_framing.ipynb.
Audience: An Applied ML Manager reviewing an internship portfolio who already understands ranking, proxy labels, and Precision@K.
Constraints: Use only the supplied facts. Do not invent model training, refresh outcomes, explanations for the rule's performance, or demonstrated business impact. Do not imply that temporal or client-held-out evaluation alone proves the causal effect of refreshing a page. Preserve the disclosure of AI assistance.
~~~

**Saved output — verbatim:**

> ## Content-refresh prioritization at FlyRank
>
> During my FlyRank internship, I developed this task-framing notebook with AI assistance to examine how pages might be prioritized for editorial review.
>
> ### Problem
>
> The starter dataset contains 30,000 anonymized content pages from 32 clients, with one row per page. The operational framing assumes a review capacity of 50 pages per cycle.
>
> Because the dataset contains no observed outcomes showing whether refreshing a page improved its performance, the notebook does not train or evaluate a refresh-benefit model. Instead, it defines a descriptive ranking task using a decline proxy.
>
> The eligible population consists of 21,758 pages satisfying:
>
> - `impressions_90d >= 100`
> - `impressions_prev_30d > 0`
>
> Binary relevance is defined as:
>
> ```text
> is_declining_proxy = (trend_direction == "down")
> ```
>
> Here, `down` indicates a greater-than-20% fall in impressions between consecutive 30-day windows.
>
> ### Approach
>
> I evaluated a fixed prioritization rule that:
>
> 1. Places pages last updated at least 90 days ago first.
> 2. Sorts pages within that ordering by `impressions_90d` descending.
>
> The evaluation metric is Precision@50, matching the assumed editorial capacity. I also calculated the expected Precision@50 of uniform random selection from the same eligible slice to provide a prevalence-based reference point.
>
> The notebook checks missing values and page-ID uniqueness and saves its executed outputs. Direct label fields are excluded from the working signals. However, the retained 90-day metrics overlap the time window used to define the decline proxy, so the setup should not be interpreted as temporally clean prediction.
>
> ### Result
>
> The fixed rule identifies 22 proxy-positive pages among its first 50 recommendations:
>
> ```text
> Precision@50 = 22 / 50 = 44.0%
> ```
>
> Uniform random selection from the same eligible population has an expected Precision@50 of 60.4%.
>
> These figures are full-slice descriptive results—not held-out model performance. No model was trained, no refresh outcomes were available, and the notebook does not demonstrate business impact or the causal effect of refreshing selected pages.
>
> ### What this established
>
> The notebook turns an underspecified content-refresh request into an explicit ranking problem with a defined eligible population, review budget, proxy label, baseline rule, metric, and key validity limitations. It also shows that the proposed fixed rule does not improve on the random-selection expectation under this proxy-based framing.
>
> A stronger follow-up study would construct features from earlier windows, measure outcomes in later periods, and evaluate generalization on held-out clients. Even with temporal and client-held-out evaluation, a separate causal design would still be required to establish whether refreshing a selected page causes an improvement.
>
> Artifact: `work/notebooks/w02_ml_task_framing.ipynb`

- **What changed:** Added one constraints layer governing claim fidelity: supplied facts only, no invented achievements or explanations, no causal implication from holdouts, and retain AI disclosure.
- **What actually improved:** “With AI assistance” returns. The speculative stable-page explanation disappears. It explicitly says a separate causal design is required to establish refresh effects and keeps the baseline comparison.
- **What still failed:** It grows to 410 words with an introduction and four sections. Accuracy improves, but it is too long for the short case I need.
- **What I would try next:** Specify three headings and a 180–230-word budget as one output-shape layer.

## V5 — Specified output format

**Exact addition to the previous prompt:**

~~~text
Output format: Use exactly three headings—The problem; What I did and decided; What came of it—with one paragraph under each, followed by one Artifact line. Keep the whole response between 180 and 230 words.
~~~

**Full prompt actually run:**

~~~text
Explain my ML project.
Goal: Write a portfolio case explaining the content-refresh prioritization problem, the approach taken, and the measured result.
Context: This is Kerem Özcan's FlyRank internship task-framing notebook, completed with AI assistance. The starter CSV has 30,000 anonymized pages across 32 clients. One row is one content page. The task is ranking pages for editorial review, assuming 50 review slots per cycle. The eligible slice has 21,758 pages with impressions_90d >= 100 and impressions_prev_30d > 0. Binary relevance is is_declining_proxy = (trend_direction == "down"); down means a greater-than-20% impression fall between consecutive 30-day windows. There are no observed refresh-benefit outcomes. A fixed rule puts pages last updated at least 90 days ago first, then sorts by impressions_90d descending. It finds 22 proxy-positive pages in its top 50: Precision@50 = 44%. Uniform random selection from this same slice has expected Precision@50 = 60.4%. These are full-slice descriptive results, not a held-out model evaluation. No model was trained in this notebook. The notebook checks missing values and unique page IDs and saves executed outputs. Direct label fields are excluded from working signals, but retained 90-day metrics overlap the decline window. Future work is earlier feature windows, later outcomes, and held-out clients. Artifact: work/notebooks/w02_ml_task_framing.ipynb.
Audience: An Applied ML Manager reviewing an internship portfolio who already understands ranking, proxy labels, and Precision@K.
Constraints: Use only the supplied facts. Do not invent model training, refresh outcomes, explanations for the rule's performance, or demonstrated business impact. Do not imply that temporal or client-held-out evaluation alone proves the causal effect of refreshing a page. Preserve the disclosure of AI assistance.
Output format: Use exactly three headings—The problem; What I did and decided; What came of it—with one paragraph under each, followed by one Artifact line. Keep the whole response between 180 and 230 words.
~~~

**Saved output — verbatim:**

> ## The problem
>
> During my FlyRank internship, I framed content-refresh prioritization as a ranking problem: choose 50 pages per review cycle from 30,000 anonymized pages across 32 clients. The eligible slice contained 21,758 pages with `impressions_90d >= 100` and `impressions_prev_30d > 0`. Because no observed refresh-benefit outcomes were available, I used a binary proxy: `is_declining_proxy = (trend_direction == "down")`, where “down” means impressions fell by more than 20% between consecutive 30-day windows.
>
> ## What I did and decided
>
> With AI assistance, I built an executed task-framing notebook that checks missing values and page-ID uniqueness, defines the eligible population and proxy label, and evaluates a fixed prioritization rule. The rule ranks pages last updated at least 90 days ago first, then sorts by `impressions_90d` descending. Direct label fields were excluded from working signals, while documenting that retained 90-day metrics overlap the decline window. No model was trained.
>
> ## What came of it
>
> The rule returned 22 proxy-positive pages in its top 50, giving Precision@50 of 44%. Uniform random selection from the same eligible slice has expected Precision@50 of 60.4%. These are full-slice descriptive results, not held-out model evaluation, and they neither measure refresh benefit nor demonstrate business impact. The result establishes a transparent baseline and exposes the need for better study design: earlier feature windows, later outcomes, and held-out clients—without treating temporal or client-held-out evaluation alone as causal evidence that refreshing improves performance.
>
> Artifact: `work/notebooks/w02_ml_task_framing.ipynb`

- **What changed:** Added only the specified output format: three named headings, one paragraph each, an Artifact line, and a word budget.
- **What actually improved:** It follows the headings and paragraph structure, preserves the 44% versus 60.4% comparison, says no model was trained, and retains AI assistance and the causal limitation. It drops from 410 to 234 words.
- **What still failed:** It slightly exceeds the 230-word cap under the counting convention below. The first paragraph remains dense, and the 50-slot assumption reads like a fixed budget. It is the best observed balance, not a perfect result.
- **What I would try next:** Next experiment, not run here: add a verification layer that checks the word count and preserves the assumed status of the review budget before returning the answer.

## Final reusable prompt

V5 is the best observed version: it retains the factual safeguards and gives a usable three-part case. The cleaned template below removes the weak opening and replaces project-specific facts with explicit input fields. It is a reusable adaptation of V5, **not a seventh tested run**. The tested, fully populated V5 is preserved above.

**How to use:** Start a fresh conversation. Fill the fact block from your own notebook or report; do not copy FlyRank's numbers into another project. Use “unknown” for missing evidence. Replace the audience if needed, then paste the completed prompt.

~~~text
Goal: Write a portfolio case explaining my applied ML problem, the approach taken,
and the measured result.

Context:
- Project and artifact link: [name; notebook or report URL]
- My contribution and AI assistance: [what I did; what AI helped with]
- Business decision: [who acts and what they decide]
- Assumed capacity or other assumptions: [state assumptions explicitly]
- Data and unit of analysis: [source; row count; groups; one row = one what]
- Eligible slice: [filters and remaining row count]
- Target or proxy: [exact definition; observed outcome or rule-derived proxy]
- Missing outcome evidence: [what the data cannot establish]
- Method actually completed: [rule/model; completed work versus plans]
- Measured result: [metric; numerator/denominator; evaluated population]
- Comparison: [baseline on the same population; observed or expected]
- Validation status: [descriptive, held out, temporal; leakage/overlap]
- Checks and artifact status: [checks actually run; saved outputs]
- Next work: [planned work, not achievements]

Audience: An Applied ML Manager reviewing an internship portfolio who already
understands ranking, proxy labels, and Precision@K.

Constraints: Use only the supplied facts. Do not invent model training, outcomes,
explanations for performance, or demonstrated business impact. Do not imply that
temporal or client-held-out evaluation alone proves a causal intervention effect.
Preserve the disclosure of AI assistance.

Output format: Use exactly three headings—The problem; What I did and decided;
What came of it—with one paragraph under each, followed by one Artifact line.
Keep the whole response between 180 and 230 words.
~~~

## What earned its place

Real context made the largest visible correction: the answer stopped claiming a trained refresh-benefit model. Constraints repaired unsupported explanations and restored AI disclosure. Format improved scanability, although it did not strictly enforce the word cap under the stated counting convention. Audience targeting had mixed value: it exposed the proxy expression but did not shorten the answer and introduced speculation.

The failure worth remembering is V1. A clearer goal made an unsupported answer sound more finished. Specificity about the desired deliverable did not substitute for evidence about the project.

## Evidence and checks

- Six complete prompts and raw outputs: [prompt_ladder_runs/](prompt_ladder_runs/).
- [Run manifest](prompt_ladder_runs/run_manifest.json): separate session IDs, completion usage, runtime warnings, word counts, and SHA-256 hashes of every prompt/output.
- Each V1–V5 prompt preserves the previous prompt byte-for-byte and appends one named layer. The constraints layer contains related factual boundaries; the format layer contains related output-shape requirements.
- Saved output text was checked against each CLI completion event; no model output was edited for presentation.
- The final template is self-contained and names the evidence a different ML intern must supply.
- No claim is made that all five additions helped, or that the final output met every instruction.
