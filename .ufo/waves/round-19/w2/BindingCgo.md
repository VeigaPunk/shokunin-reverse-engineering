# C3 binding review — `t1250-cgo`

## Findings (by severity)

### P2 — The silent/empty diagnostic result is based on a retained log whose tail is incomplete

**Observation.** The receipt declares polling-copy loss as a capture limitation (`.ufo/waves/round-19/runs/t1250-cgo/receipt.json:24`). It records the last log copy at `2026-10-20T19:02:15.677240Z` and the analyze step ending at `19:02:16.177824Z` (`receipt.json:1911-1933`), a 0.500584-second gap. The retained `ghidra.log` ends at line 180, `ANALYZING changes made by post scripts`, after it has started `ReaGhidraBridge` (`logs/rea-ghidra-bdYUwH/ghidra.log:174-180`); there is no captured post-script completion. The run-bound observation nevertheless records `invalid_index_reads: []` (`observation.json:151-161`), and the comparison reports `all_match: true` (`compare.json:1-53`). The producer's captured `carrier-run.py` digest matches the current runner, whose `LogPoller` copies on polls and makes only a final best-effort scan after process wait (`.ufo/waves/round-17/tools/carrier-run.py:44-46, 472-532`). The extractor derives `invalid_index_reads` from the retained bytes (`.ufo/waves/round-17/tools/log-extract.py:28-35, 177-190`).

**Inference / impact.** The log-to-run identity binding is intact (see below), and the observed Go-version/snapshot lines precede this tail gap. But the empty diagnostic list proves absence only in the bytes actually retained; it cannot rule out a diagnostic written after the last copy. Treat this carrier's negative/silent diagnostic result as qualified, not as complete-log confirmation. This is a capture-completeness limitation, not evidence that an omitted diagnostic actually occurred. `t1250-cgo` is predicted `h1_kind: none` (`predictions/t1250-cgo.prediction.json:15-30`), so this row is non-discriminating for H1 in any event; the frozen amendment names `t1250-vet` as the sole D carrier (`claims.json:36-40`).

## Binding checks that passed

**Observation — frozen prediction and carrier identity.** `producer.json:2-5` identifies label `t1250-cgo`, branch `main`, and tip `a1140e76fffdc1be032d9d813dbb686157803bbc`; the amendment says predictions were frozen there before analysis (`claims.json:36,40`). The prediction at that commit hashes to `b42a62bf61fec9b99df1c81e60d2763069e4b3bd9223dbf3ad769e6e7136aefd`, matching `predictions/SHA256SUMS:4`. Its carrier path and SHA are `.../pkg/tool/linux_amd64/cgo` and `d61f87246456ff1175d057ad663a10dd1ac503c54dc770d14aaa5ffd3309b858` (`predictions/t1250-cgo.prediction.json:32-35`). Independently hashing the installed carrier returned that SHA and MD5 `1bdce2782a6a828733dae9f99c943c6c`, matching both receipt pre/post SHA and its MD5 (`receipt.json:5-10`).

**Observation — one run-bound Ghidra session.** The receipt has exactly one `bound_sessions` entry (`receipt.json:2-3`), and its `retained_logs` session directory is the same (`receipt.json:1892-1914`); `unbound_sessions` is empty (`receipt.json:2000`). In the retained log, `Using log file` names that session's `ghidra.log` (line 2), `IMPORTING` names its `target-d61f87246456.bin` (line 46), and the loader MD5 is the receipt/carrier MD5 (line 58). The receipt's binding flags are all true (`receipt.json:1894-1897`). The same log reports the Ghidra 12.1.4 installation (line 1), Go API snapshot `1.25.0` (lines 121-126), and analysis succeeded before the post scripts (line 174). This establishes one canonical runtime identity for this run; no alternate-runtime or reroute is evidenced here.

**Observation — independent log/map hashes and map counts.** The retained `ghidra.log` SHA-256 independently recomputes to `92b560d537b3b4833c23b7a842d1a0bd2705516f4fb4c8ea4fb55431e24c9524`, matching `receipt.json:1900-1904` and `observation.json:158-161`. Exactly two files exist under `pins/`: `mid-1.json` and `mid-2.json`. Their recomputed hashes match the analyze-step commitments (`receipt.json:1934-1951`); each contains 152 entries and their recorded times match the map files (`pins/mid-1.json:764-765`, `pins/mid-2.json:764-765`). A direct JSON equality check found `pins_pre.entries == pins_post.entries == mid-1.entries == mid-2.entries`; the receipt also has `pins_compare.equal: true` with empty changed/errors/missing lists (`receipt.json:348-355`) and no mid-run drift steps (`receipt.json:25`).

**Observation — recorded validation and comparison.** The retained validation record reports one valid receipt, zero invalid/unreadable receipts, 366 checks, no findings, and `require_mid_maps: true` (`evidence/receipt-validation/t1250-cgo.json:2-22`). Independent checks above do not rely on that stored verdict. `compare.json` reports all fields matched, including empty EOF/invalid-index reads (`compare.json:2-53`); the prediction explicitly expects those empty values and a `1.25.0` snapshot route of `info` (`predictions/t1250-cgo.prediction.json:36-46`). This supports the recorded comparison over the captured log, subject to the tail limitation above.

## Validator digest note

**Observation.** `producer.json:11` records `receipt-validate.py` SHA-256 `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`; the current file hashes to `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762`. Per assignment, this is the expected mismatch after its forward fix, not a receipt defect. I did not rewrite any receipt or validation artifact.

## Commands and exit codes

All commands below were read-only; each reported exit 0.

```sh
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/pins/mid-1.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/pins/mid-2.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/predictions/t1250-cgo.prediction.json
# exit=0

find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/pins -maxdepth 1 -type f -name 'mid-*.json' -printf '%f\n' | sort
find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/pins -maxdepth 1 -type f -name 'mid-*.json' -printf '%f\n' | wc -l
# exit=0; names: mid-1.json, mid-2.json; count=2

set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-cgo.prediction.json | sha256sum
# exit=0

set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-cgo.prediction.json | jq -r '.carrier.sha256'
# exit=0

sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cgo
md5sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cgo
# exit=0 for the command pair

jq -c '[.pins_pre.entries == .pins_post.entries, (.pins_pre.entries|length), (.pins_post.entries|length), .pins_compare.equal, (.mid_run_drift_steps|length)]' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/receipt.json
# exit=0; result: [true,152,152,true,0]

jq -e -s '.[0].pins_pre.entries == .[0].pins_post.entries and .[1].entries == .[0].pins_pre.entries and .[2].entries == .[0].pins_pre.entries' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/receipt.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/pins/mid-1.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/pins/mid-2.json
# exit=0; result: true

jq -r '.steps.analyze.pin_checks[] | [.map_path,.map_sha256,.entries,.equal,(.changed|length),(.missing|length)] | @tsv' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-cgo/receipt.json
# exit=0

sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py
# exit=0

sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/carrier-run.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/pins.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/log-extract.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/compare.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/swiss-misread.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py
# exit=0
```

No builds, tests, installs, runtime launches, or production edits were performed. No LSP device was exposed in the mounted tools; this review was scoped to the requested retained-artifact binding.