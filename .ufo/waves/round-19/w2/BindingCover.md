# W2 review — C3 binding, t1250-cover (BindingCover-3)

Scope: `.ufo/waves/round-19/runs/t1250-cover/` — receipt, producer, pins, bound log, retained
validation evidence. Axes: calibration, freshness, depth. All git reads against the frozen tip
`a1140e76fffdc1be032d9d813dbb686157803bbc` by full hash; no git writes; no receipts rewritten;
no carrier executed (hashed only); no REA/Ghidra invocation. Mutation tests: none run (no code
change proposed by this review; nothing to mutate).

**Verdict: the t1250-cover C3 binding holds. No falsifying defect found in scope.**
Two findings below are observations that bound how the binding evidence must be read today
(F-1 expected and briefed; F-2 is a mid-review tree movement, also non-defective but easy to
misread).

## Verified binding chain (all Observation unless marked)

### 1. Carrier SHA matches the frozen prediction

```
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cover
64686d22f3b4055386bbcbf0aeac54249cdbff771ffd7b54c8d4abd330df8166  ... (exit 0)
$ md5sum <same path>
4b81886d22d4bbb7cc47fc6605d9601b  ... (exit 0)
```

- Prediction at freeze: `predictions/t1250-cover.prediction.json` `carrier.sha256` = `64686d22…` (read of file).
- Receipt `carrier.sha256_pre` = `carrier.sha256_post` = `64686d22…`, `md5_pre` = `4b81886d…` (`runs/t1250-cover/receipt.json:2-17`).
- Pin maps: all four snapshots (`pins_pre`, `pins/mid-1.json`, `pins/mid-2.json`, `pins_post`) carry the same carrier entry `{'sha256': '64686d22…', 'size': 5037210}` — python equality check printed `pre==mid1: True`, `mid1==mid2: True`, `mid2==post: True`, 152 entries each (exit 0).
- Bound target name embeds the digest prefix: log line `2026-10-20 16:05:11 INFO (GoRttiMapper) Reading Go binary info: target-64686d22f3b4.bin` (`logs/rea-ghidra-XVD7qp/ghidra.log:191`, echoed in observation.json `go_lines` and in the log tail's `ANALYZING changes made by post scripts: …/target-64686d22f3b4.bin`).

### 2. Bound log re-hash matches receipt and observation

```
$ sha256sum .ufo/waves/round-19/runs/t1250-cover/logs/rea-ghidra-XVD7qp/ghidra.log
630a40d4d5d45258cfa45c4720672dc671c088106cecaa5fdbcfe221427df5ad  ... (exit 0)
$ wc -c <same> → 31862 (exit 0)
$ sha256sum .../script.log → a443790bd911c86b4f46458be2db91ee763dca1af922a9eb9e89f3f6780202b9, 106 bytes (exit 0)
```

Matches `receipt.steps.analyze.retained_logs[0].files` (both files, `logfile_ok/md5_ok/target_ok` true),
`retained_logs[0].files` at receipt top level, and `observation.json` `log_sha256`/`log_bytes`.

### 3. Prediction and decision rule unchanged from the freeze

```
$ git show a1140e76…:.ufo/waves/round-19/predictions/t1250-cover.prediction.json | sha256sum
0e14f0a8bfecd3e6a8c6931905c036c715d2d6637e5b278941e5a157a17f0603  -   (exit 0)
$ diff <(git show a1140e76…:…t1250-cover.prediction.json) predictions/t1250-cover.prediction.json
IDENTICAL, diffexit=0
$ git show a1140e76…:.ufo/waves/round-19/predictions/decision-rule.json | sha256sum
3d94a7c0fc92d9af71fd3d670349acd18ce4b9ad6ccfa161b406a23d6620c8f8  -   (exit 0)
$ sha256sum predictions/decision-rule.json → 3d94a7c0… (identical)
$ git show a1140e76…:.ufo/waves/round-19/predictions/SHA256SUMS | grep -E 't1250-cover|decision-rule'
3d94a7c0…  predictions/decision-rule.json
0e14f0a8…  predictions/t1250-cover.prediction.json
40b3b54c…  predictions/swiss-misread/t1250-cover.json
```

The run-time pin of the prediction in every pin map is `0e14f0a8…` — so run-time pinned bytes =
freeze-commit bytes = working-tree bytes today. The frozen emulator blob
`predictions/swiss-misread/t1250-cover.json` is also unchanged (`40b3b54c…` at freeze = working
tree) and predicts for cover: `predicted_failure_h0/h1: false`, all `predicted_invalid_index_reads*
: []`, `predicted_eof_reads*: []`, `misread_map_types: 4` (read of file) — cover is a silent
non-D label. The emulator itself is unchanged: `sha256sum .ufo/waves/round-18/tools/swiss-misread.py`
= `14924bd6…` (exit 0) = the run-time pin = `prediction.c3.emulator_sha256`.

### 4. Freeze ordering (freshness)

```
$ git show -s --format='%H%n%ci%n%s%n%P' a1140e76…
a1140e76fffdc1be032d9d813dbb686157803bbc
2026-10-20 15:57:44 -0300
round-19: frozen C3 predictions and decision rule (go1.25.0 toolchain held-out, D={t1250-vet}), runner (pre-run)
85589ac757f9ca3cb25efcd702d0963e25c9c4df
$ git merge-base --is-ancestor a1140e76… refs/heads/main → yes (exit 0)
```

Freeze committer instant 18:57:44Z precedes the first run (`runs/run-log.txt` first entry
`2026-10-20T15:57:51-03:00`, t1250-go) and the cover analyze window
`started_at_utc 2026-10-20T19:05:07.575585+00:00` → `ended_at_utc 19:05:50.211565+00:00`
(`receipt.json` `steps.analyze`). "Frozen before any REA analyze" holds for this run.
Timezone coherence: the Ghidra log's local stamps 16:05:08–16:05:49 (-03:00) equal 19:05:08–19:05:49Z,
inside the pin window pre 19:05:06.86Z → post 19:05:50.26Z (`receipt.pins_compare`), with mid-1 at
19:05:07.62Z and mid-2 at 19:05:37.69Z. `producer.json` `branch_tip` = `a1140e76…`,
`recorded_at_utc 2026-10-20T19:05:06Z`.

### 5. Mid maps count and drift

- Count: **2** mid maps (`pins/mid-1.json`, `pins/mid-2.json`), **152 pinned entries each**; my re-hash: `28a5f3f59b6c…` / `bc97c0fd79b2…` (exit 0), equal to `receipt.steps.analyze.pin_checks[].map_sha256` with `equal: true`, `changed: []`, `missing: []`.
- Entry sets identical across pre/mid-1/mid-2/post (python dict equality, exit 0). `mid_run_drift_steps: []`, `pins_compare.equal: true`.
- `receipt-validate.py --require-mid-maps` on this receipt exited **0** at validation time:
  `evidence/receipt-validation/t1250-cover.json`: `exit 0`, `status valid`, `checks_performed 366`,
  `findings []`, `pins_available true`, `require_mid_maps true` (validator run from the pinned copy,
  `pins_path: /tmp/pins.py`).

### 6. Outcome vs frozen decision rule for cover (non-D)

Decision rule (identical at freeze and today): `D_definition` map-path booleans,
`diagnostic_set_D: ["t1250-vet"]`, `count_rule` = labels with a bound retained log and a compare.json,
`binding_gate` = validator exit 0 + carrier sha equality + unchanged prediction blob — all three gate
conditions verified above.

Observed for cover: `observation.json` `classification snapshot_loaded`, `invalid_index_reads []`,
`eof_reads []`, `analyzer_errors []`, `snapshot_route info`, `snapshot_labels ["1.25.0"]`,
`missing_bootstrap false`; log has `Using Go API snapshot for 1.25.0` at `ghidra.log:192-193` and
`Go version 1.25.0` at `:196` (INFO, no WARN fallback); `grep -c "Invalid index" ghidra.log` → **0**
(exit 1 = zero matches). `compare.json` `all_match: true` over all 8 fields; `compare.exit 0`,
`observation.exit 0`, `carrier-run.exit 0`; all three stderr files 0 bytes and the receipt records the
empty-string sha `e3b0c442…` for both step stderr paths (consistent). A silent non-D label exactly as
predicted — the failure-free half of the frozen `confirmed` condition.

## Findings by severity

### F-1 [Expected, observed] Current validator exits 1 on all 8 receipts — self-digest drift only

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-cover/receipt.json ; echo exit=$?
exit=1
findings (both on the validator's own path):
  sha256_mismatch  expected 70672eb3…145  actual 6afb7ef6…762
  size_mismatch    expected 46047         actual 52682
```

Same two findings, on no other path, for all of go/gofmt/asm/cgo/compile/cover/preprofile/vet
(8/8 receipts, `counts: {invalid: 1, receipts: 1}`). This is the briefed expected post-fix state:
the run pinned the then-current validator (`70672eb3…`, also in `producer.json tool_sha256` and every
pin map); the forward fix (commit `4f6c73f`, `+102/-8`, the R18-MIDMAP-LISTSTEP analyze-step-identity
tightening) replaced the file. **Not a receipt defect; receipts correctly left untouched.** Notably the
strictest current validator re-checked the other 364 checks per receipt and found nothing — an
independent re-confirmation of every carrier/prediction/log/emulator/typeinfo pin.
Consequence to keep in view: the `binding_gate` as literally written ("receipt-validate.py
--require-mid-maps exits 0 on its receipt") is time-indexed — re-evaluated *today* it fails 8/8 on the
self-pin. The record of gate passage is the retained `evidence/receipt-validation/*.json`, which is the
correct artifact; no action needed, but any fresh aggregate gate re-run must read those retained
verdicts, not re-execute.

### F-2 [Observed, non-defective] Main advanced mid-review; validator grew again

Start of review: `refs/heads/main = d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, validator blob
`9276b198…` (51075 B at `4f6c73f`). During review main moved to `279e8b19c51658bfd05b9e31a1c0894ab2e70537`
with validator blob `cae3ec84…` (52682 B), working tree clean against it (`git diff --stat` empty,
diffexit 0; file mtime 16:19:33 -03:00). All conclusions here are pinned to `a1140e76…` and to immutable
run artifacts, so the tree movement does not affect them. Flagged only so wave-2 readers do not misread
the two different "current validator" digests seen in various w2 outputs.

### F-3 [Observation, cross-label support] k = 8 confirmed; vet's compare mismatch is the designed non-gating path

All 8 labels have a bound retained `ghidra.log`, a `compare.json`, and a retained
`evidence/receipt-validation/<label>.json` (per-label sweep, exit 0) — the C3 count 0 → 8 holds.
7/8 `compare.json all_match: true`. `t1250-vet` is `all_match: false` on exactly one field:
`extra.invalid_index_reads` predicted `[13902080, 852107777, 1801722468838924630]` (full frozen H1
list) vs observed `[13902080]` — `runs/run-log.txt` aggregate `exit=1` comes solely from this vet
compare exit, exactly as the frozen `compare_note` ("its exit is reported per label; the mechanism
verdict … is decided from the bound log") anticipates. Mechanism side, independently swept:
`grep -c "Invalid index"` = 0 in all seven non-D logs and 1 in vet's
(`t1250-vet/logs/*/ghidra.log:229`: `Caused by: java.io.EOFException: Invalid index: 13902080`).
`13902080` is in the frozen `h1_only_invalid_indexes` set `{13902080, 852107777}` and no observed
index falls outside the frozen H1 list, and every non-D label is silent — the frozen rule's `confirmed`
conditions are satisfied on my independent observation. [Inference, flagged as such: whether the
round-18 Go-1.24-only limit "moves to confirmed" is the claimant's declaration under its own rule; the
rule-satisfaction facts above are observations. Note `h0_consistent` (walk-index-only, non-discriminating)
does *not* apply to vet as run — the observed index is H1-only, i.e. discriminating.]

## Residual risk and verification gaps

- Archive provenance (S038): I did not re-download the go1.25.0 linux-amd64 archive or re-derive
  `cover`'s member digest from it; carrier identity rests on the frozen decision-rule `held_out`
  note, the live binary hash, and the pre/post/mid pin equality. Extraction was judged out of scope
  for a binding review (the binding chain does not pass through the archive).
- `carrier-run.stdout` is a verbatim copy of `receipt.json` (2002 vs 2001 lines, trailing newline) —
  informational only, no digest is recorded against it.
- F-1's time-indexed gate (above) is the only durable caveat on re-running the binding gate.
- No mutation testing performed: this review proposes no code change; the mutation seats
  (MutDigest/MutStrict/…) own validator-side mutations.

Commands were run read-only in LANE (`sha256sum`, `md5sum`, `wc`, `stat`, `grep -c`, `python3 -I -B`
json readers, `git --no-optional-locks show/rev-parse/merge-base/diff/cat-file/ls-tree/log`); validator
reruns wrote only `/tmp/rv-<label>.out`. Exit codes pasted inline above.
