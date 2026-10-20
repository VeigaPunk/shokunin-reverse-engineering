# t1250-go C3 binding review

## Axis assessment

- **Calibration:** The captured result is consistent with this label's frozen prediction: the prediction declares `h1_kind: none` and `snapshot_route: info`; the retained log records the Go 1.25.0 snapshot route and reports analysis succeeded. This assesses `t1250-go` only, not the full C3 cohort.
- **Freshness:** The run producer names freeze tip `a1140e76fffdc1be032d9d813dbb686157803bbc`. The `t1250-go` prediction blob at that commit and the current prediction both hash to `80632ede7724f0bbc635c0c54a02de14bf2bdd60d37c1987eed7041aced92ceb`. The current `main` ref is `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; the frozen-blob check, rather than the current tree, is the freshness check.
- **Depth:** Receipt validation evidence records one valid carrier receipt, 384 checks, no findings, and `require_mid_maps: true`. Independently, the bound log and all five retained mid-map hashes match the receipt. The capture-completeness caveat below limits absence-based conclusions from the log tail.

## Findings

### Low — retained log completeness through process exit is not established

**Observation:** `receipt.json:24` explicitly says the polling copy may miss lines written after its final poll and before REA deletes the runtime root. For this run, the last log-copy timestamp is `2026-10-20T18:59:59.725746+00:00` (`receipt.json:1911`), while `steps.analyze.ended_at_utc` is `2026-10-20T19:00:00.227380+00:00` (`receipt.json:1931`), about 0.502 seconds later. The retained `ghidra.log` ends at line 576 with “ANALYZING changes made by post scripts” (`runs/t1250-go/logs/rea-ghidra-AiWB8A/ghidra.log:574-576`), not a log-completion marker. The run logic's final `poller.scan()` is best-effort and occurs after `proc.wait()` (`round-17/tools/carrier-run.py:524-532`); its poller only sees extant session directories (`:214-227`).

**Inference:** The retained bytes are correctly hash-bound, but the record does not prove the log is complete through Ghidra process termination. The available bytes show the expected `info` snapshot route (`ghidra.log:516-521`) and an analysis-success line (`:570`); they do not establish that no relevant line was emitted during the unobserved tail. Keep the no-failure/silence conclusion for this non-D label qualified by this capture gap. No omitted bytes are independently recoverable from the retained artifact set.

## Binding checks — observations

- `receipt.json:2-10,1892-1913,2027` identifies one bound session (`rea-ghidra-AiWB8A`), the expected carrier path and matching pre/post SHA-256, all three log-binding flags true, and no unbound sessions. The captured `ghidra.log` basename identifies `target-b93cdfdbc72f.bin` at `ghidra.log:46,58`; receipt carrier MD5 and SHA-256 are consistent with that run identity.
- The carrier SHA-256 is `b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25` in the current carrier, `receipt.json:8-9`, and frozen prediction `t1250-go.prediction.json:32-35`. At the freeze commit, `git show … | sha256sum` returned the same prediction digest as the current file. `predictions/SHA256SUMS:7` agrees.
- The `pins/` directory contains exactly **5** files, `mid-1.json` through `mid-5.json`; no separate pre/post map files are present (pre/post snapshots are embedded in `receipt.json`). Independent SHA-256s for every mid map match `steps.analyze.pin_checks` at `receipt.json:1934-1979`; each check records 152 entries, `equal: true`, and empty changed/missing lists. `pins_compare` also records `equal: true` with empty changed/errors/missing (`receipt.json:348-355`), and `mid_run_drift_steps` is empty (`:23-25`).
  Independent SHA-256 outputs: `logs/rea-ghidra-AiWB8A/ghidra.log` `ebb305d61ad7c0e9616b8da8c472468bb06b6e5f78bbb9e28b7295e6dcaa3676`; `script.log` `13008f21f257db70cb0c18f1c075368cb158969cf2bb5ebb1e1dbb0400103460`; `mid-1` `b36d685101188d567ee982cdff4bf311e5b165a0bb81add8f5033df0da5dd52d`; `mid-2` `f4a43abd2435525a1088275204702800e3f403c19e5a8186377002757e4bd1ec`; `mid-3` `5244e1073e5c3d7efd297538362268d1173b805c9835b2aebf6a5b9b132bc2a4`; `mid-4` `65cd5f2012adf6cb74a08b828d72279f18e2dca695b2320e74e79b72c482a3be`; `mid-5` `3263b20408d4056fe3141b40ae22b336c37b264e0ce74f52274fa1465ed3b6b7`.
- Retained validation evidence (`evidence/receipt-validation/t1250-go.json:2-22`) reports exit 0, `valid: 1`, `invalid: 0`, 384 checks, no findings, and `require_mid_maps: true`. This is the retained validation result; I did not rerun the validator.
- The current `round-17/tools/receipt-validate.py` hash differs from the producer-captured hash (`producer.json:6-12`, `receipt.json:1103-1106`): captured `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`, current `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762`. Per the assignment, this is the expected forward-fix mismatch, not a receipt defect; no receipt was rewritten.
- `compare.json:2-53` reports all compared prediction fields match. The raw log, not `compare.json`, is the basis for the observed log statements above. The log also has Go subtype warnings (`ghidra.log:522-525`); these are reported as warnings, not misrepresented as an `Invalid index` failure.

## Verification commands (all exited 0)

```text
sha256sum '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/logs/rea-ghidra-AiWB8A/ghidra.log' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/logs/rea-ghidra-AiWB8A/script.log' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/pins/mid-1.json' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/pins/mid-2.json' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/pins/mid-3.json' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/pins/mid-4.json' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/pins/mid-5.json'  # exit 0
sha256sum '/home/vgpnk/.local/opt/go-1.25.0/bin/go' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/predictions/t1250-go.prediction.json' '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/predictions/decision-rule.json'  # exit 0
git -C '/home/vgpnk/Projects/shokunin/kaidoku-shokunin' rev-parse refs/heads/main  # exit 0
set -o pipefail; git -C '/home/vgpnk/Projects/shokunin/kaidoku-shokunin' show 'a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-go.prediction.json' | sha256sum  # exit 0
printf '%s\n' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-go/pins/mid-*.json | wc -l  # exit 0; output 5
sha256sum '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py'  # exit 0
```

**Verification gaps:** No LSP device was mounted (`read xd://lsp` returned “No such tool”); grep was used only to locate artifact text, not as semantic proof. No REA/Ghidra analysis, carrier execution, mutation, build, or test was run. The report is limited to `t1250-go`; it does not verify the other seven labels.
