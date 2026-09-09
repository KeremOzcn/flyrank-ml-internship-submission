# Cross-model run of the final prompt (v5)

The final prompt is `../v5_prompt.txt` (sha256 in `../run_manifest.json`). The same bytes went to
both models, three runs each. The written comparison is §5 of `../../fl04_prompt_iteration_log.md`.

## Claude side

- Outputs: `../v5_output.md`, `../replicates/r2_v5_output.md`, `../replicates/r3_v5_output.md`
- Receipts: `../v5_receipt.json`, `../replicates/r{2,3}_v5_receipt.json`
- Model resolved: `claude-sonnet-5` via `claude` CLI 2.1.250; 2–278 input tokens per call

```bash
claude -p "$(cat v5_prompt.txt)" \
  --setting-sources "" --system-prompt "" \
  --exclude-dynamic-system-prompt-sections \
  --strict-mcp-config --tools "" \
  --model sonnet --output-format json
```

## ChatGPT side

- Outputs: `chatgpt_v5_output.md`, `chatgpt_v5_r2_output.md`, `chatgpt_v5_r3_output.md`
- Events: `codex_v5_events_final.jsonl`, `codex_v5_r2_events.jsonl`, `codex_v5_r3_events.jsonl`
- Runner: `codex-cli` 0.148.0 on ChatGPT account auth; 22,649–23,534 input tokens per call

```bash
codex exec "$(cat v5_prompt.txt)" \
  --ignore-user-config --ignore-rules --skip-git-repo-check \
  --ephemeral -s read-only -C <neutral dir outside the repo> --json \
  -o crossmodel/chatgpt_v5_output.md < /dev/null
```

**`-C <neutral dir>` is not optional.** See "Discarded run" below.

### Quota block, 2026-09-08

Three attempts between 17:44 and 17:56 (+03) returned
`You've hit your usage limit … try again at 9:27 PM`; `gpt-5.1-codex-mini` was rejected as a
fallback (`400`, not supported for ChatGPT-account auth). A watcher retried after the reset and
succeeded on its first attempt at 21:42:55. Full history: `codex_retry_log.txt`; the failed
afternoon attempt is preserved in `codex_v5_events.jsonl`.

## Discarded run

`discarded/` holds one replicate executed with the working directory *inside* the repository. It
spent **147,661 input tokens** and made **10 shell calls**, including
`rg --files -g 'w02_ml_task_framing*'` — it went looking for the source notebook rather than
working from the prompt. Codex is an agent; given repo access it will use it. That run was
quarantined and re-run from a neutral cwd. All three kept runs made zero tool calls
(`grep -c '"type":"command_execution"'` returns 0).

This is the same contamination described in §2 of the log for the Claude side. Verify tool-call
count and input-token size on any future run before trusting it.

## The asymmetry to keep disclosing

`claude` can be stripped to a near-bare model call. `codex exec` cannot — it exposes no
"no-agent-system-prompt" mode, so ~23,000 tokens of coding-agent scaffolding rides along on every
call. Differences between the two sides therefore confound the model with its wrapper. A cleaner
model-vs-model test would paste the identical prompt into chatgpt.com with custom instructions and
memory switched off; that is a different experiment and has not been run.
