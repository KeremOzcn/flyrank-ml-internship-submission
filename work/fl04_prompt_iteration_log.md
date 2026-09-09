# FL-04: Prompt Iteration Log

**Phase**: Foundations
**Author**: Kerem Özcan
**Date**: September 8, 2026
**Run artifacts**: [`work/prompt_iteration_runs/`](prompt_iteration_runs/) — every prompt, every output, a receipt per call, and [`run_manifest.json`](prompt_iteration_runs/run_manifest.json)

---

## 1. The task

The task comes from **FL-01 Target Task 3 — Technical Markdown & Research Report Synthesis**
([`fl01_workflow_audit.md`](fl01_workflow_audit.md) §4). It is classified *Delegate to AI with review*
in the audit, which is exactly the class where prompt quality decides whether the review is a
skim or a rewrite.

FL-01 defines "done well" for this task as three testable conditions:

1. The report follows a technical structure (Abstract, Methodology, Results, Discussion).
2. Every numerical claim traces back exactly to committed evidence.
3. Zero unverified or hallucinated claims; limitations stated.

The concrete instance: **write a short research report on the completed FlyRank content-refresh
notebook, so a reviewer can judge whether the results justify further modeling.** The underlying
work is task framing plus one fixed-rule baseline — no trained model, no held-out evaluation, no
causal experiment. That makes it a good test case, because the most likely failure is not bad
prose. It is a model quietly upgrading a descriptive result into a modeling claim.

The evidence the prompts are allowed to use is frozen in
[`prompt_iteration_runs/task_evidence.json`](prompt_iteration_runs/task_evidence.json), extracted
from the executed notebook `work/notebooks/w02_ml_task_framing.ipynb`:

| Fact | Value |
|---|---|
| Raw pages / clients | 30,000 / 32 |
| Eligible pages (`impressions_90d >= 100`, `impressions_prev_30d > 0`) | 21,758 |
| Proxy-positive eligible pages (`trend_direction == "down"`) | 13,152 |
| Assumed review capacity | 50 pages per cycle |
| Fixed rule hits in top 50 | 22 → **Precision@50 = 44%** |
| Uniform random expectation (13,152 / 21,758) | **≈ 60.4%** |
| Model trained / held-out eval / observed refresh benefit | none / none / none |

---

## 2. How these runs were produced

Prompt experiments are worthless if the harness answers the question for the model, so the runs
are stripped down deliberately:

```bash
claude -p "$(cat vN_prompt.txt)" \
  --setting-sources "" --system-prompt "" \
  --exclude-dynamic-system-prompt-sections \
  --strict-mcp-config --tools "" \
  --model sonnet --output-format json
```

That disables tools, MCP servers, hooks, plugins, and both project and user `CLAUDE.md`. The naive
prompt costs 278 input tokens, so what reaches the model is essentially the prompt itself.
Resolved model: `claude-sonnet-5`. Each rung was run **three times** (18 runs total), because a
single sample cannot distinguish a technique effect from sampling noise, and the CLI exposes no
temperature or seed control.

**A discarded first attempt, recorded because it changes how I read the whole exercise.** The
first pass ran with tools enabled. The v1 prompt — role assignment only, no evidence whatsoever —
came back with a complete, correctly-numbered report. The model had used its file tools to read
the repository, found `task_evidence.json`, and also found the later prompt files; its reply
opened by citing "the five-heading / one-table / <350-word spec from your v5 prompt rung." It had
read ahead and answered a question I had not asked yet. Those outputs are not in this log.

The lesson generalizes past this assignment: **in an agentic harness you are not measuring your
prompt.** A weak prompt plus filesystem access can outscore a strong prompt without it, which
tells you nothing about the prompt. This is also the mechanism behind a whole class of
evaluation self-deception — a benchmark that leaves the answer key inside the agent's reachable
context measures retrieval, not capability.

---

## 3. The six versions

Each version is strictly cumulative: it is the previous prompt plus exactly one named technique,
so any difference is attributable to that one addition. Full text in
[`prompt_iteration_runs/`](prompt_iteration_runs/).

### v0 — Naive baseline (no technique)

> `Write a report about my ML results.`

**Output** ([`v0_output.md`](prompt_iteration_runs/v0_output.md)): no report. A 158-word intake
questionnaire asking for project context, dataset, models, metrics, comparisons, files, and
audience. **3/3 replicates refused** (158 / 149 / 170 words).

**Note.** This is the honest baseline and it is not a failure of phrasing. The model had no
evidence, and declining to invent results is the correct behavior — a v0 that had produced a
confident report would have been the worse outcome. What v0 establishes is the real bottleneck:
this task is blocked on *evidence supply*, not on wording. Every later gain that looks like
"better prompting" has to be measured against that.

---

### v1 — Role assignment

> `+ Role: You are an applied ML research editor.`

**Output** ([`v1_output.md`](prompt_iteration_runs/v1_output.md)): still no report. **3/3
replicates refused** (205 / 196 / 191 words).

**Note — the most useful negative result in the ladder.** Role assignment bought a *vocabulary*,
not a deliverable. The questionnaire reorganized itself under an "Essential Information" heading
and started asking editor-shaped questions it had not asked before: train/validation/test split
methodology, baselines for comparison, and whether "Limitations" and "Reproducibility" sections
were required. It also added a "Quick Start Option" offering to work from a pasted file.

So the role changed *what the model considered relevant* — real, and visible in three of three
runs — while moving output quality exactly nowhere, because the binding constraint was still
missing evidence. Role assignment is a cheap steering technique that is often sold as a quality
technique. On this task it steered and did not lift, and +38 words of better-targeted questions
is the entire measured effect.

---

### v2 — Context and motivation

> `+ Context and motivation:` the full evidence block — what the work is, who needs it and why,
> every number from `task_evidence.json`, and the explicit non-results (no model, no held-out
> evaluation, no causal experiment), closing with *"These are the available results; unknown
> information remains unknown."*

**Output** ([`v2_output.md`](prompt_iteration_runs/v2_output.md)): the first real report, and the
single largest jump in the ladder. **3/3 produced reports with every supplied number correct.**

**Note.** This rung is where the task actually gets done, which confirms the v0 reading: supplying
evidence and motivation, not adopting a persona, is what converts refusal into output. Two effects
worth separating:

*The gain beyond restatement.* The model did not merely reformat what I gave it. It derived a
point I had not made — that because proxy prevalence in the eligible pool is ~60%, precision alone
is a weak quality signal here, and a rule has to clear a ~60% bar rather than a low one. That is a
correct and genuinely useful observation about my evaluation design.

*The costs.* Length went unmanaged and unstable: 817 / 780 / **1166** words, a 386-word spread
across identical prompts. The model invented its own eight-section skeleton, hitting at most 2 of
the 5 headings the final spec would later require, and never producing a source line in any run
(it did produce a table in 3/3, unprompted). In the longest
replicate it drifted into unrequested advice about alternative metrics (early detection, AUC/lift).

*The failure I did not predict.* All **3/3** runs printed `**Author:** keremozcan1603@gmail.com`.
I never supplied my email; it came from the runtime's identity. Given an unrequested metadata slot
("Author:"), the model filled it from whatever the environment exposed. That is the concrete
version of a rule worth keeping: **fields you don't specify get filled from context you didn't
audit** — and here the leaked value was personal data in a document destined to be public.

---

### v3 — Few-shot examples

> `+ Few-shot examples (illustrative only; these are not FlyRank observations):` two short
> input→report pairs demonstrating the hedged sentence pattern — a rule below its random baseline
> described without explaining *why*, and inspected missingness described without claiming it was
> harmless.

**Output** ([`v3_output.md`](prompt_iteration_runs/v3_output.md)): reports in 3/3, numbers correct
in 3/3, length tightening to 739 / 581 / 551 (spread 188, down from 386).

**Note.** The examples transferred, but partially and with one backfire.

*What transferred.* Hedging became systematic rather than occasional — "does not establish that",
"cannot be ruled out from this notebook alone" — and a dedicated Limitations section appeared with
five separate caveats. The email leak dropped from 3/3 to 2/3. Structural compliance did **not**
improve (0–1 of 5 headings), which makes sense: my examples demonstrated *sentences*, so the model
copied sentence-level behavior and nothing above it. Few-shot teaches the level you show it.

*The backfire.* One replicate invented a causal mechanism the evidence cannot support — that
high-impression pages may be less likely to fall 20%, and that long-stale pages may skew toward
already-stable traffic. Example A existed specifically to forbid explaining *why* the rule
underperformed. So the hedging vocabulary did not only fail to prevent speculation; it made the
speculation read as measured and careful. **A model can learn the sound of epistemic caution
without the substance of it**, and that is more dangerous than blunt overclaiming, because a
skimming reviewer scores the tone rather than the claim.

---

### v4 — Output structure

> `+ Output structure:` exactly five headings (Abstract; Methodology; Results; Discussion; Next
> steps), one compact table in Results with method / positives at 50 / Precision@50, prose under
> 350 words, ending with a Source line.

**Output** ([`v4_output.md`](prompt_iteration_runs/v4_output.md)): **5/5 headings in 3/3 runs**,
table in 3/3, source line in 3/3, at 334 / 363 / 347 words — a 29-word spread, down from 188.

**Note.** The largest *quality-per-token* gain in the ladder, and it worked by subtraction.

*What structure fixed for free.* Output fell 44% from v3's average (624 → 348 words) with no
supplied number lost. The email/author hallucination went to **0/3** — not because I forbade it, but because the
five prescribed headings left no metadata slot to fill. Same for the invented mechanism: it
disappeared in 3/3. Constraining shape turned out to be a more reliable way of suppressing
fabrication than instructing against it, because a fabrication needs somewhere to live.

*A gain I did not ask for.* All 3/3 computed the expected positives at 50 (~30.2 = 13,152/21,758 ×
50), a derived figure absent from my prompt and arithmetically correct. Asking for a table with a
"positives at 50" column forced the comparator into the same units as the rule, and the model did
the conversion. **Structure requests can induce correct computation, because a shape can imply an
obligation that prose does not.**

*What structure did not fix.* **0/3** stated the size of the gap between 44% and 60.4%. The
headline comparison of the entire report was left for the reader to subtract. And in 1/3 the
phrase "As in prior work, a rule underperforming a random baseline…" appeared — treating my
illustrative few-shot examples as though they were prior FlyRank findings, despite being labeled
"illustrative only; these are not FlyRank observations." That label protected the *numbers* but
not the *framing*: examples leak into voice even when explicitly fenced off.

---

### v5 — Step decomposition (final)

> `+ Step decomposition:` complete four stages in order before returning — (1) extract supplied
> facts, assumptions and unknowns including the AI-assistance disclosure; (2) check 22/50,
> 13,152/21,758, expected positives at 50, and the percentage-point gap; (3) draft the five
> sections; (4) audit every claim against supplied evidence and check headings and length,
> correcting unsupported explanations or lost assumptions. Return only the report.

**Output** ([`v5_output.md`](prompt_iteration_runs/v5_output.md)): 5/5 headings, table and source
line in 3/3, at 351 / 355 / 345 words — a **10-word spread**, the tightest in the ladder.

**Note.** v5 costs 17 more words of output and $0.002 more than v4. It looks nearly identical. The
difference is entirely in what it stopped losing.

*Stage 2 recovered the headline.* **3/3** now state the gap explicitly — "roughly 16.4 percentage
points" (60.4467 − 44 = 16.45, correct) — against **0/3** at v4. Naming an arithmetic check as its
own step is what put the report's most important number into the report.

*Stage 4 removed the imported framing.* The "as in prior work" leak went to 0/3, and the leakage
caveat sharpened from a vague warning into one accurate sentence: agreement between rule and proxy
may partly reflect the 90-day metrics overlapping the decline window rather than an independent
effect.

*Stage 1 protected the disclosure.* Naming the AI-assistance disclosure as an extraction target
kept it in the Abstract in 3/3 — the kind of clause that silently vanishes under a word cap,
because compression drops whatever no step is accountable for.

*The real lesson.* Decomposition did not make the writing better. It made it **stop losing
things** — and the 10-word spread across three runs says the same thing quantitatively: this rung
buys *consistency*, which is what actually matters for a task I intend to delegate repeatedly.
A one-shot demo cannot see this gain, because at n=1 v4 and v5 look like the same document.

---

## 4. What the 18 runs measured

Every cell is 3 runs of the identical prompt. Sources: [`run_manifest.json`](prompt_iteration_runs/run_manifest.json) and [`replicates/`](prompt_iteration_runs/replicates/).

| | v0 naive | v1 role | v2 context | v3 few-shot | v4 structure | v5 decomposition |
|---|---|---|---|---|---|---|
| Produced a report | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Supplied numbers correct | — | — | 3/3 | 3/3 | 3/3 | 3/3 |
| Output words | 158/149/170 | 205/196/191 | 817/780/1166 | 739/581/551 | 334/363/347 | 351/355/345 |
| Spread (max − min) | 21 | 14 | **386** | 188 | 29 | **10** |
| Required headings (of 5) | 0 | 0 | 0–2 | 0–1 | **5/5 ×3** | **5/5 ×3** |
| Table present | 0/3 | 0/3 | 3/3 | 1/3 | 3/3 | 3/3 |
| Source line present | 0/3 | 0/3 | 0/3 | 2/3 | 3/3 | 3/3 |
| Leaked my email as "Author" | 0/3 | 0/3 | **3/3** | 2/3 | 0/3 | 0/3 |
| Invented a causal mechanism | — | — | 0/3 | **1/3** | 0/3 | 0/3 |
| Treated examples as prior work | — | — | 0/3 | 0/3 | **1/3** | 0/3 |
| Derived expected positives (~30.2) | — | — | 0/3 | 0/3 | 3/3 | 3/3 |
| Stated the 16.4pp gap | — | — | 3/3 | 1/3 | **0/3** | **3/3** |

Word counts are whole-document whitespace tokens (headings and table cells included), computed in
the receipts — not prose-only counts, so they run slightly above the figure the v4/v5 prose cap
governs. Cost of one full six-rung pass: **$0.1035**.

Three things this table says that a single run could not:

1. **The whole quality jump is v1 → v2.** Everything after it is control, not capability. Ranking
   the techniques by measured effect on *this* task: context ≫ structure > decomposition >
   few-shot > role. The technique with the best reputation-to-effect ratio was role assignment.
2. **Nothing monotonically improves.** v3 lost the 16.4pp gap that v2 had stated in 3/3, and v4 did
   not recover it. Adding a technique can silently delete a behavior an earlier rung produced, so
   "each version is better" is an assumption to test, not a property of ladders.
3. **The last two rungs bought variance reduction.** A 386-word spread became 10. For a task I
   plan to run repeatedly and review quickly, predictability is worth more than the marginal
   sentence.

---

## 5. Cross-model comparison

Identical prompt bytes (`v5_prompt.txt`) to both models, **3 runs each**.

| | Claude | ChatGPT |
|---|---|---|
| Model / runner | `claude-sonnet-5`, `claude` CLI 2.1.250 | `codex exec`, `codex-cli` 0.148.0 (ChatGPT account auth) |
| Harness input tokens per call | 2–278 | 22,649–23,534 |
| Tool calls made | 0/3 (tools disabled) | 0/3 (after one contaminated run was discarded) |

The ChatGPT side was blocked all afternoon on an account usage limit (`try again at 9:27 PM`); a
watcher retried at 21:42 and succeeded on the first attempt. Log:
[`crossmodel/codex_retry_log.txt`](prompt_iteration_runs/crossmodel/codex_retry_log.txt).

**One Codex replicate was discarded, for the same reason as §2.** I first ran the replicates with
the working directory *inside* the repo. One of them spent 147,661 input tokens and executed 10
shell commands — including `rg --files -g 'w02_ml_task_framing*'`, hunting for the source notebook.
Codex is an agent and I had handed it the evidence. It is quarantined in
[`crossmodel/discarded/`](prompt_iteration_runs/crossmodel/discarded/) and was re-run with
`-C <neutral dir>`. All three kept runs made zero tool calls. **The same trap caught me twice in
one afternoon, on two different CLIs.**

### Compliance: the prompt dominates the model

| Criterion (3 runs each) | Claude | ChatGPT |
|---|---|---|
| All 5 required headings | 3/3 | 3/3 |
| Table with requested columns | 3/3 | 3/3 |
| Source line | 3/3 | 3/3 |
| All supplied numbers correct | 3/3 | 3/3 |
| Derived ~30.2 expected positives | 3/3 | 3/3 |
| Stated the 16.4pp gap | 3/3 | 3/3 |
| AI-assistance disclosure kept | 3/3 | 3/3 |
| Fabricated any metric | 0/3 | 0/3 |
| Words (whole document) | 345 / 351 / 355 | 346 / 364 / 367 |

**That is the headline, and it is not the one I expected.** On every criterion the assignment
cares about, the two models are indistinguishable. A prompt engineered to this level made the
model choice nearly irrelevant for this task — which is a much stronger argument for prompt
engineering than any single-model before/after could be. Where v0 and v5 differ enormously, Claude
and ChatGPT at v5 differ barely at all.

### Where they actually differ

**Tone — the one systematic difference.** ChatGPT delivers a *verdict*; Claude reports a *finding*.
ChatGPT closed with a judgment in **3/3** runs — "the available results do not justify claiming
predictive value or refresh benefit", "Results do not justify the current rule over random
selection". Claude did so in **1/3**, otherwise stopping at the description and leaving the
inference to the reader. My prompt asked for a report that helps a reviewer *judge*, so ChatGPT is
arguably answering the brief more directly. But it is doing more of the reader's thinking, and for
a document whose entire purpose is to avoid overclaiming, I prefer the version that hands me the
gap and lets me draw the conclusion.

**Accuracy — one soft overreach, from ChatGPT.** One run concluded "the current baseline does not
justify **deployment**." Deployment is nowhere in the evidence and nowhere in the prompt; there is
no system, no rollout, no decision about shipping anything. It is a reasonable-sounding sentence
about a question that was never asked. Everything checkable was correct on both sides — this is
scope creep, not a wrong number, and it is exactly the kind of drift that survives a skim.

**Structure — a formatting inconsistency on the ChatGPT side.** It varied its heading level between
runs: `##` in 2/3, `#` (H1) in 1/3. Claude used `##` in 3/3. Irrelevant standalone, and a real
nuisance if you paste the output into a larger document with its own heading hierarchy.

**Length stability.** ChatGPT's spread was 21 words to Claude's 10 — both well inside spec, and too
small a difference at n=3 to claim as a model property.

**Failure points, side by side.** ChatGPT echoed my own instruction sentence — "Unknown information
remains unknown." — verbatim into the body of the report in 1/3 runs, turning a directive to the
model into a line addressed to the reader. Claude never did (0/3). Claude's failures were all at
earlier rungs and all *metadata and framing* rather than arithmetic: the email-as-author leak
(v2–v3), the few-shot examples leaking into voice as "prior work" (v4). At v5, neither model failed
on anything the FL-01 criteria measure.

### The confound, stated plainly

These are not equivalent calls. Claude ran stripped to near-bare (2–278 input tokens); the Codex
CLI exposes no "no-agent-system-prompt" mode and carried ~23,000 tokens of coding-agent scaffolding
into every call. So every difference above confounds model with wrapper, and the tonal difference
in particular — a coding agent is built to end on a recommendation — may well be the harness
talking rather than the model. The honest reading is that **this comparison bounds how much the
model choice mattered (very little) without cleanly attributing the small residue.** Settling that
needs the same prompt in chatgpt.com with no custom instructions and no memory, which is a
different experiment than the one I ran.

### One correction to my own measurement

Before this run existed, I had scored an *earlier, differently-specified* Codex ladder
([`prompt_ladder_runs/`](prompt_ladder_runs/)) as missing its word cap — 234 words against a stated
180–230. That was the whole-document count including headings and the artifact line; the prose it
actually governs is 218, inside the cap. The constraint was met and the claim is withdrawn. I had a
tidy cross-model difference and it evaporated on recount, which is why the comparison above is
built only from runs of the identical prompt.

---

## 6. The reusable template

Distilled from the ladder, ordered by measured effect. Nothing in it refers to FlyRank, to me, or
to this dataset — fill the brackets and it applies to any "turn my evidence into a structured
document" task.

```text
[TASK]
<One sentence: the artifact you want and the decision it has to support.>

[ROLE]
You are a <specific practitioner, not "expert">: <the discipline whose judgment
you want applied>.

[CONTEXT AND MOTIVATION]
Who reads this and what they will decide with it: <reader, decision>.
What the work actually is: <method, and explicitly what it is NOT>.
Evidence you may use — these are the only facts available:
  <fact: value>
  <fact: value>
What does NOT exist: <no trained model / no held-out eval / no causal test /
no observed outcome — list every absent thing a reader might assume is present>.
Unknown information remains unknown. Do not fill gaps by inference.

[EXAMPLES]  (illustrative only; not observations about this work)
Input: <a situation structurally like yours>
Good output: "<one or two sentences in the exact epistemic register you want —
show the level you care about; the model copies the level you demonstrate>"
Input: <a second situation, covering a different failure you want avoided>
Good output: "<...>"

[OUTPUT STRUCTURE]
Return <format> with exactly these headings: <H1; H2; H3; H4; H5>.
Include <one table with these columns: ...>, so comparisons are forced into
common units.
Keep prose under <N> words. End with <a source/provenance line>.
Do not add sections, metadata fields, author lines, or dates.

[STEPS]  (complete in order before answering; return only the final artifact)
1. Extract the supplied facts, assumptions, unknowns, and any required
   disclosures.
2. Verify the arithmetic: <name each figure and comparison explicitly,
   including any difference or gap you want stated>.
3. Draft the requested sections.
4. Audit every claim against the supplied evidence. Remove explanations of
   WHY something happened unless the evidence establishes it. Confirm the
   headings, the length, and that no required disclosure was dropped.
```

**Five rules a stranger should carry, each earned above:**

1. **Evidence before persona.** Role assignment moved 0/3 outputs from refusal to report; supplying
   evidence moved 3/3. If output is weak, add facts before adding adjectives.
2. **Name the absences explicitly.** Listing what does *not* exist (no model, no held-out
   evaluation, no causal test) is what keeps a descriptive result from being written up as a
   modeling claim.
3. **Close every slot you don't want filled.** An unrequested "Author:" field pulled my real email
   out of the runtime in 3/3 runs. Prescribing the exact headings drove that to 0/3 without a
   single "do not" instruction. Constrain shape rather than forbidding content.
4. **Demonstrate at the level you care about.** Sentence-level examples bought sentence-level
   hedging and zero structural compliance — and taught the *sound* of caution well enough to make a
   speculative claim read as careful. Pair examples with a structure spec, never rely on them alone.
5. **Name each number you want checked as its own step.** The headline 16.4pp gap appeared in 0/3
   runs until a verification step named it, then 3/3. Anything no step is accountable for is what
   compression deletes first.

---

## 7. Limits of this experiment

- **One task, one model, one day.** Every ranking above is specific to a structured-report task
  where all evidence was supplied in the prompt. Role assignment doing nothing here is not evidence
  that role assignment does nothing generally — on a task with genuine tonal ambiguity it would
  plausibly carry much more.
- **n=3, no seed, no temperature control.** Three samples per rung supports "3/3 vs 0/3" claims
  comfortably and separates the 386-word spread from the 10-word one. It does not support fine
  distinctions, and nothing here is a significance test.
- **Cumulative, not factorial.** Each rung is previous + one technique, so I measured the marginal
  effect of each technique *in that order*. I did not test whether structure alone would beat
  few-shot alone, or whether the v3 backfire would have occurred without v2 preceding it.
- **The model never verified anything.** Every number was asserted by me from
  `task_evidence.json`. If that file were wrong, v5 would be confidently, structurally,
  well-hedged wrong — and would look exactly as trustworthy. The ladder bought faithfulness to
  supplied evidence, which is not the same as truth.
- **The cross-model comparison carries a harness confound** (§5): Claude ran near-bare, ChatGPT ran
  inside the Codex agent wrapper. It bounds the model effect as small without cleanly attributing
  the residue, and n=3 per model cannot support the 1/3-level differences as model properties.
- **Two of twenty-four runs were thrown away for contamination**, one per CLI, both caught only
  because token counts looked wrong. I have no guarantee I would have caught a subtler one.

---

## 8. Files

| Path | What it is |
|---|---|
| [`prompt_iteration_runs/v0…v5_prompt.txt`](prompt_iteration_runs/) | The six prompts, cumulative |
| [`prompt_iteration_runs/v0…v5_output.md`](prompt_iteration_runs/) | Canonical output per rung |
| [`prompt_iteration_runs/v0…v5_receipt.json`](prompt_iteration_runs/) | Per-call session id, usage, cost, sha256 |
| [`prompt_iteration_runs/replicates/`](prompt_iteration_runs/replicates/) | Replicates 2 and 3 of all six rungs |
| [`prompt_iteration_runs/run_manifest.json`](prompt_iteration_runs/run_manifest.json) | Harness, flags, and every run in one file |
| [`prompt_iteration_runs/task_evidence.json`](prompt_iteration_runs/task_evidence.json) | The frozen evidence the prompts assert |
| [`prompt_iteration_runs/tutorial/`](prompt_iteration_runs/tutorial/) | Anthropic tutorial drills (ch. 1–3) with receipts |
| [`prompt_iteration_runs/crossmodel/`](prompt_iteration_runs/crossmodel/) | ChatGPT runs ×3, event logs, retry log, and the discarded contaminated run |

**Tutorial drills.** Chapters 1–3 of the Anthropic Prompt Engineering Interactive Tutorial were
worked through against the live API rather than in the notebook, with prompts, outputs and token
receipts saved. Two of six exercises fail the tutorial's built-in keyword checker while meeting the
stated criterion — 1.2 (correct behavior, wrong keyword) and 3.1 (correct answer `x = 6`, checker
misses the capitalized "Incorrect"); see
[`tutorial/exercise_checks.json`](prompt_iteration_runs/tutorial/exercise_checks.json). Worth
recording, because a brittle string check scoring a correct answer as a failure is the same
measurement problem as the contaminated run in §2, pointed the other way.
