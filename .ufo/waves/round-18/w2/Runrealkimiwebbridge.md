HOLDS

# Re-derivation of carrier run `real-kimi-webbridge` (wave 2, falsify)

Seat: KaidokuR18.Runrealkimiwebbridge. REV = b2aad08ceeee8dd125ce0d316056d8bd766c7f94; freeze = eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0. All cited run artifacts are committed at REV and byte-identical to the worktree (verified below), so `path:line` anchors hold at REV. Method: independent re-extraction from raw log lines with grep/sha256sum/md5sum — not via the producer's log-extract.py — then compared against the frozen prediction. No tools installed (none needed). No REA analyze/search/decompile, no Ghidra, no carrier execution; only hashing and `file` header reads.

## Commands (each with exit code)

1. Route + failure extraction (exit 0):
```
$ cd .ufo/waves/round-18/runs/real-kimi-webbridge && grep -n -E "GoApiSnapshot|Go analysis failure|Invalid index|Unable to read past EOF|Untested Go version|Using Go API snapshot" logs/rea-ghidra-ZSUHpG/ghidra.log
68:2026-10-20 13:31:12 WARN  (GoApiSnapshot) Falling back from 1.24.13 to 1.24.6 for Go API snapshot
69:2026-10-20 13:31:13 INFO  (GoRttiMapper) Using Go API snapshot for version 1.24.13
73:2026-10-20 13:31:14 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException
206:Caused by: java.io.EOFException: Invalid index: 15606016
```
2. Counts (grep -c; exit 1 for a zero count is grep's no-match status, expected):
```
"Unable to read past EOF" → 0;  "Invalid index" → 1;  "Go analysis failure" → 1;
"Untested Go version" → 0;  "GoApiSnapshot" → 1;  "EOFException" → 1 (only line 206)
```
3. Carrier hashes (exit 0):
```
$ sha256sum /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge
71067480bd99c2ba0f6d76df50a17e4911917cec8878320c107105066f8ad35d
$ md5sum /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge
605e348a7278e82d103ae8f0e1dc105f
```
4. Receipt validation (exit 0, echoed `EXIT=0`):
```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/real-kimi-webbridge/receipt.json
{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,...,
 "receipts":[{"checks_performed":366,"findings":[],"kind":"carrier","status":"valid","valid":true}],
 "require_mid_maps":true}
```
5. Prediction freeze identity (exit 0):
```
$ git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json | sha256sum
05b354d01af0481876e828730cd2e84815bc04c22b5fd6c0aed79f7d43c41756
$ sha256sum .ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json   → same digest
$ git diff --stat eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json .ufo/waves/round-18/predictions/decision-rule.json
(no output → unchanged between freeze and REV)
```
6. Log binding lines (exit 0):
```
$ grep -n -E "target-|kr17-rea" logs/rea-ghidra-ZSUHpG/ghidra.log
2:  ... Using log file: /tmp/kr17-rea-0wd781s_/rea-ghidra-ZSUHpG/ghidra.log
46: ... IMPORTING: file:///tmp/kr17-rea-0wd781s_/rea-ghidra-ZSUHpG/target-71067480bd99.bin
57: Loading file:///tmp/kr17-rea-0wd781s_/rea-ghidra-ZSUHpG/target-71067480bd99.bin?MD5=605e348a7278e82d103ae8f0e1dc105f...
```
7. Retained-log digests vs receipt (exit 0):
```
$ sha256sum logs/rea-ghidra-ZSUHpG/ghidra.log logs/rea-ghidra-ZSUHpG/script.log
fae34819b55f12f3b6b873c0dd0643e544ee442b368b3ae82e9a5bdfbcc5d051  ghidra.log
f0710f720f8aca3201ebd5d203c996cd5ea181cad02d8dc6c58607f16110a266  script.log
```
8. Committed-at-REV identity (exit 0):
```
$ git show REV:.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log | sha256sum → fae34819… (== worktree)
$ git show REV:.ufo/waves/round-18/runs/real-kimi-webbridge/receipt.json | sha256sum → a0e78bbe858035d9… (== worktree)
```

## Per-field verdicts

Prediction = `git show eb6c2668:…/predictions/real-kimi-webbridge.prediction.json` (sha256 05b354d0…, listed in predictions/SHA256SUMS at the freeze commit). Observation = raw ghidra.log lines + receipt.

| Field | Predicted | Observed (raw) | Verdict |
|---|---|---|---|
| snapshot_route | `"fallback"` | ghidra.log:68 `WARN (GoApiSnapshot) Falling back from 1.24.13 to 1.24.6` — the only GoApiSnapshot line (count 1); no INFO-level GoApiSnapshot line (observation.json `api_snapshot_info_labels: []`) | HOLDS |
| snapshot_label | `"1.24.13"` | ghidra.log:69 `INFO (GoRttiMapper) Using Go API snapshot for version 1.24.13` | HOLDS |
| fallback_to | `"1.24.6"` | ghidra.log:68, same line | HOLDS |
| untested_version | `null` | `"Untested Go version"` count 0; observation.json `untested_versions: []` | HOLDS |
| missing_bootstrap | `false` | observation.json:81 `"missing_bootstrap": false`, `bootstrap_attempts: 1` | HOLDS |
| extra.analyzer_errors_contain | `"Go analysis failure"` | ghidra.log:73 `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` (count 1) | HOLDS |
| extra.eof_reads | `[]` | `"Unable to read past EOF"` count 0; the log's only EOFException is the Invalid-index line | HOLDS |
| extra.invalid_index_reads | `[15606016]` | ghidra.log:206 `Caused by: java.io.EOFException: Invalid index: 15606016` (count 1), inside the GoName.readStructure stack under the line-73 failure | HOLDS |
| carrier.sha256 | `71067480…f8ad35d` | sha256sum identical | HOLDS |
| carrier.md5 (receipt) | `605e348a…c105f` | md5sum identical; also equals ghidra.log:57 `?MD5=` and receipt.json:6 `md5_pre` | HOLDS |

compare.json (run dir) records all eight fields `match: true`, `all_match: true`; my independent raw-line extraction agrees with it on every field (observation, cross-checked, not circular: I did not use log-extract.py).

## Log binding

- Session path: ghidra.log:2 log file `/tmp/kr17-rea-0wd781s_/rea-ghidra-ZSUHpG/ghidra.log` == receipt.json:2-4 `bound_sessions[0]` == receipt.json:1911 `session_dir` == observation.json `log_file_line`. HOLDS.
- target-\<sha12\>: ghidra.log:46 imports `target-71067480bd99.bin`; `71067480bd99` is the first 12 hex of the carrier sha256 `71067480bd99c2ba…`. HOLDS.
- MD5: ghidra.log:57 `?MD5=605e348a7278e82d103ae8f0e1dc105f` == md5sum(carrier) == receipt.json:6 `md5_pre`; receipt.json:8-9 `sha256_pre` == `sha256_post` == recomputed carrier sha256 (no drift). HOLDS.
- Retained-log integrity: receipt.json:1893-1897 binding flags `logfile_ok/md5_ok/target_ok` all true; receipt.json:1897-1906 recorded sha256 for ghidra.log (fae34819…) and script.log (f0710f72…) == recomputed digests. HOLDS.
- Receipt provenance: producer.json:5-6 `branch_tip` = eb6c2668… (the freeze commit); steps argv use `npx -y rea-agents@6.5.0` (receipt.json:1924-1931, contract-compliant); pins_compare `equal: true, changed: []` (receipt.json:348); `mid_run_drift_steps: []` (receipt.json:25); mid pin maps mid-1/mid-2, 152 entries each, `equal: true` (receipt.json:1936-1946). HOLDS.

## Receipt validation (--require-mid-maps)

Exit 0; 1 receipt, valid, 0 invalid/unreadable; 366 checks, findings []. Per receipt-validate.py:453-500, the flag requires every step `pin_checks` entry to carry `map_path`+`map_sha256` (`mid_map_missing` otherwise), the analyze step to carry ≥1 check (`mid_checks_absent`), recomputes each map digest, and re-derives the equal/changed/missing verdict via pins.compare with an entries-count cross-check (`mid_entries_mismatch`). The receipt's two mid maps satisfy this. HOLDS.

## Decision-rule application (this label only)

decision-rule.json:3 binding gate — all three conditions verified for this label: (a) validator exits 0 with --require-mid-maps; (b) bound log's carrier sha256 (target-71067480bd99 → 71067480bd99c2ba…) equals the prediction's; (c) prediction blob unchanged from the freeze commit (digest + empty diff). The table row (decision-rule.json:184-195) freezes `h1: invalid_index`, `invalid_index_reads_h1: [15606016]`, `eof_reads_h1: []`, `route: fallback`, `diagnostic: true` — identical to the prediction file. The frozen emulator output (predictions/swiss-misread/real-kimi-webbridge.json at eb6c2668, lines 3084-3098) predicts `predicted_invalid_index_reads_h0: []` vs `_h1: [15606016]` and `predicted_eof_reads: []`; the observed log shows exactly the H1 read set and no H0-compatible silence. [INFERENCE] This held-out D label therefore shows its exact H1 outcome and contributes toward the frozen rule's "confirmed" branch; the fleet-level confirmed/refuted/unresolved verdict depends on the other 14 labels and is out of this seat's scope.

Non-obvious combination the prediction got right: the log pairs label `1.24.13` (GoRttiMapper INFO echoes the requested version, per the prediction's GoApiSnapshot.java:111,122-126 basis) with route `fallback` (WARN) and an underlying go1.24.0 base + go1.24.6 diff (prediction `selection.status: fallback_diff`, `selected_patch: 6`). [INFERENCE, grounded in the prediction's basis rows]

## Residual caveats

- receipt.json:24 `log_capture_limit`: "polling copy; lines written after the final poll before REA deletes its runtime root can be missing". The retained log ends at line 263 (13:32:09 "ANALYZING changes made by post scripts") while the analyze step ended at 16:32:10.09Z (receipt.json), so headless-exit/teardown lines are plausibly absent. [INFERENCE] All extracted fields sit at lines ≤ 227, before the final poll (118 polls, last copy 16:32:09.59Z, receipt.json:1909-1910), so the disclosed truncation cannot affect them. [INFERENCE]
- compare.json rules mark `snapshot_label` "non-discriminating: request echo" — the discriminating fields here are the failure signature and the read values, both of which matched exactly. Observation.
- Carrier `file` output: statically linked stripped ELF x86-64, BuildID c5b01256… — consistent with a Go binary but not independently re-derived beyond inspect-go.json's `"go_version":"go1.24.13"` (matches prediction `input`). Observation.

## Verdict

**HOLDS** — every predicted field (snapshot_route, snapshot_label, fallback_to, untested_version, missing_bootstrap, analyzer_errors_contain, eof_reads, invalid_index_reads), the carrier sha256/MD5, all three log-binding anchors, the retained-log digests, the freeze-commit identity of the prediction, and the --require-mid-maps receipt validation reproduce exactly from raw artifacts at REV. No finding against the run; residual risk limited to the disclosed polling-copy tail truncation, which cannot affect the extracted fields.
