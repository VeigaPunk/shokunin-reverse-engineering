# R22-C1 refusal-ancestor review

## Finding

**MEDIUM — Nested `ok: false` ancestor is counted as exercised.**

`count-c1.py:54-66` validates the outer CLI envelope (`ok is True`) and then passes only `envelope["data"]` to `r21.bind`. The retained r21 helper's `refused()` checks `error`/`errors`, selected string status/code fields, `exit_code`, and `raw_result`/`normalized_result` (`round-21/tools/verb-coverage.py:39-55`); it does not recognize `ok is False`. Its supported `records` wrapper walk propagates only that predicate (`:58-74`). Consequently, a matching record beneath a nested supported `records` ancestor with `ok:false` is bound even though that ancestor declares failure. This is within the claimed refusal-handling behavior, not the separately declared limits on source relevance or cryptographic authentication.

### Reproduction

I used the existing fixture builder `counter-fixtures.py:c1_files()` as the clean baseline (six source-linked records with the expected operation aliases), copied its declared helper/catalog dependencies into private temporary Git repositories, then committed each variant. No lane source was changed. Exact argv, stdout, and stderr for all three runs are retained in `w2/C1Refusal.json`.

- **Clean positive:** `/usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1refusal-ancestor-l72rwbky/positive-all-six-xvxnv_7q --rev c67603804d2b3befd2bf4f9ebadb988935ba9c38` → exit **0**, stdout reports `t1_exercised_count: 6`, `finding: c1_complete`; stderr empty.
- **Recognized refusal control:** same argv shape, root `/tmp/c1refusal-ancestor-l72rwbky/matching-record-under-refusal-ancestor-20e7bocs`, rev `fe2422ec04059f4fb5c70221e4df2f2204316ccc`. Each outer envelope was successful, but its `data` held `{ "error": {"code":"capability_unavailable"}, "records": [matching_record] }`. Result: exit **1**, stdout reports `t1_exercised_count: 0`, `finding: c1_incomplete`; stderr empty. This confirms ordinary error-coded ancestors are rejected.
- **Adversarial typed ancestor:** argv `/usr/bin/python -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root /tmp/c1refusal-ancestor-l72rwbky/nested-ok-false-refusal-ancestor-uet39pns --rev 69c39290fe0f95ded8813662daa530b8d0b374eb`. Each outer envelope remained `ok:true` with matching `meta.command`; its `data` was `{ "ok": false, "records": [matching_record] }`. Result: exit **0**, stdout reports `t1_exercised_count: 6`, all six verbs exercised, `finding: c1_complete`; stderr empty. The failure flag is on an ancestor of every matched record, but the refusal predicate ignores it.

The private fixture intentionally tests parser behavior; it does **not** establish that a real provider emits this nested shape. That limits likelihood, not the observed acceptance defect. Top-level failed envelopes and nested ancestors carrying a truthy `error` are correctly rejected. The counter's declared no-cryptographic-authentication limit remains separate; this finding concerns the stated local refusal/record binding semantics.

### Narrow fix

Include strict boolean `ok is False` in the refusal predicate for every supported carrier ancestor (or apply an equivalent recursive gate to the `data` tree before binding). Add a fixture where a matching record is under `records` beneath `ok:false`, expecting no exercised verbs and exit 1, while retaining the existing clean and error-coded controls.

## Residual risk and verification gaps

- LSP status/references/definition/diagnostics were unavailable in the exposed tool set; I make no semantic caller-coverage claim and used no grep output as proof.
- Only the bounded private positive/refusal probes above were run. No full selftest/build/lint suite or provider runtime was run; no tool was installed.
- The report's JSON attachment contains the exact complete stdout strings, argv arrays, exits, and stderr for each probe (including the positive and refusal controls).