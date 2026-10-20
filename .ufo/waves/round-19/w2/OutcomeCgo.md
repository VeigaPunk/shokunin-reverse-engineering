# OutcomeCgo — C3 held-out outcome for t1250-cgo (round 19, wave 2)

Scope: attack the C3 outcome for `t1250-cgo` from the **raw retained `ghidra.log`** (not `compare.json`), against the frozen prediction `predictions/t1250-cgo.prediction.json` and the frozen rule `predictions/decision-rule.json`. Read-only; no production edits; no REA analyze / Ghidra execution; no carrier execution; no installs. LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; W19 = `LANE/.ufo/waves/round-19`.

## Verdict

1. **Prediction match: exact, 8/8 log-observable frozen fields.** `expected` (5 fields) and `extra_expectations` (3 fields) all match the raw log. No mismatch. `compare.exit` 0 / `all_match: true` is corroborated independently, not assumed.
2. **Frozen mechanism rule, non-D clause: holds for this label.** `t1250-cgo` is non-D (`diagnostic_set_D = ["t1250-vet"]`) and its log contains **zero** `Go analysis failure` lines and zero `ERROR`-severity Go lines. The rule's text for a non-D label is "shows no Go analysis failure"; that is what the log shows.
3. **Discrimination from this label: none, by design.** The prescan predicts silence under **both** H1 and H0 for cgo (`predicted_failure_h1 false`, `predicted_failure_h0 false`), so the match is a negative-control result: it supports the outcome model but cannot distinguish H1 from H0. The discriminating label is `t1250-vet`. Calling the cgo match "confirmation of H1" would be over-reading; I do not.
4. **Binding gate: passed at measurement time, not re-executable verbatim today.** The recorded `receipt-validate.py --require-mid-maps` result for this receipt is exit 0 / valid 1 (`evidence/receipt-validation/t1250-cgo.json`). Re-running it today exits 1 **solely** on a self-pin: the tool file `round-17/tools/receipt-validate.py` changed after the run (`70672eb3…` at run time -> `9276b198…` at `main` -> `6afb7ef6…` in the current dirty worktree), and the validator hashes live files. Every C3 subject pin (carrier, typeinfo snapshot, prediction blob, log digest) still matches. Detail in "Binding chain" below.

## Artifacts and identity [OBSERVED]

| Item | Value |
|---|---|
| Carrier | `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cgo`, 4413745 B, sha256 `d61f87246456ff1175d057ad663a10dd1ac503c54dc770d14aaa5ffd3309b858`, md5 `1bdce2782a6a828733dae9f99c943c6c` |
| Frozen prediction | `W19/predictions/t1250-cgo.prediction.json`, sha256 `b42a62bf61fec9b99df1c81e60d2763069e4b3bd9223dbf3ad769e6e7136aefd` |
| Freeze commit | `a1140e76fffdc1be032d9d813dbb686157803bbc` (2026-10-20 15:57:44 -0300); blob at that commit has the same sha256 |
| Retained log | `W19/runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log`, 180 lines, 18804 B, sha256 `92b560d537b3b4833c23b7a842d1a0bd2705516f4fb4c8ea4fb55431e24c9524` |
| Observation | `W19/runs/t1250-cgo/observation.json` (derived from the log; sha field `log_sha256` equals above) |
| Receipt | `W19/runs/t1250-cgo/receipt.json`; `retained_logs[0].binding = {logfile_ok: true, md5_ok: true, target_ok: true}`, `pins_compare.equal true`, `mid_run_drift_steps []` |
| Run base | producer `branch_tip a1140e7…`; analyze step started `19:01:37.047840Z`, ended `19:02:16.177824Z`, `exit 0`. The freeze commit is dated `18:57:44Z`, i.e. ~3 m 53 s before analyze start; `pins/mid-1.json` was taken `19:01:37.093664Z` (before the first Ghidra log line at `19:01:38`) and `pins/mid-2.json` at `19:02:07.168790Z`; both pin prediction `b42a62bf…` and carrier `d61f8724…`. |
| Main tip at report time | `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (2026-10-20 16:15:31 -0300) |

Log-to-carrier binding is in the log itself: line 58,
`Loading file:///tmp/kr17-rea-7tv8__gs/rea-ghidra-bdYUwH/target-d61f87246456.bin?MD5=1bdce2782a6a828733dae9f99c943c6c...`
— target name carries the carrier sha256 prefix, and `MD5=` equals the carrier md5. This is independent of `observation.json`.

Identity commands re-run at report time (cwd `LANE`):

```
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cgo
d61f87246456ff1175d057ad663a10dd1ac503c54dc770d14aaa5ffd3309b858   exit 0
$ md5sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cgo
1bdce2782a6a828733dae9f99c943c6c   exit 0
$ sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json
54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252   exit 0
$ git show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-cgo.prediction.json | sha256sum
b42a62bf61fec9b99df1c81e60d2763069e4b3bd9223dbf3ad769e6e7136aefd   exit 0
$ git merge-base --is-ancestor a1140e76fffdc1be032d9d813dbb686157803bbc refs/heads/main
exit 0
```

## Raw-log parse [OBSERVED]

Commands (cwd `W19`; `grep` exit 1 below means "no matching line", not a tool failure):

```
$ wc -lc runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
180 18804
$ sha256sum runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
92b560d537b3b4833c23b7a842d1a0bd2705516f4fb4c8ea4fb55431e24c9524
$ grep -c ' INFO ' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log ; grep -c ' WARN ' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log ; grep -c ' ERROR ' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
53
3
0
$ grep -n -E 'ERROR|Exception|Invalid|EOF|End of file|past end|Traceback|Caused by' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
(no lines) exit 1
$ grep -n -E 'fall.?back|Untested Go version|untested|bootstrap|Unable to find Go|bootstrap data' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
(no lines) exit 1
$ grep -n -E 'GoApiSnapshot\) Using|GoRttiMapper\) Using|Go version 1\.25\.0|Analysis succeeded|post scripts' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
122,123,126,174,180
$ grep -n 'MD5=' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
58:Loading file:///tmp/kr17-rea-7tv8__gs/rea-ghidra-bdYUwH/target-d61f87246456.bin?MD5=1bdce2782a6a828733dae9f99c943c6c...
$ grep -c 'Go analysis failure' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
0
$ grep -c -E 'Invalid index: [0-9]+' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log ; grep -c -E 'Unable to read past EOF: [0-9]+, [0-9]+' runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
0
0
```

Relevant lines, verbatim components:

- `122: 16:01:40 INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0`
- `123: 16:01:40 INFO  (GoRttiMapper) Using Go API snapshot for version 1.25.0`
- `124: 16:01:40 INFO  (GoTypeManager) Discovered 29 unindexed Go types`
- `125: 16:01:40 INFO  (GoTypeManager) Found 2218 Go types`
- `126: 16:01:40 INFO  (GolangSymbolAnalyzer) Go version 1.25.0`
- `127-129: 16:01:47 WARN (GoTypeManager) Failed to get subtype '[...]...' in *[...]...` (3 subtype lookups; `GoTypeManager.java:417` `Msg.warn`, not a failure path)
- `136: 16:02:04 INFO  (PropagateRttiBackgroundCommand) Go RTTI callsite fixup info (total/updated/skipped): 2271/2227/0`
- `140: 16:02:13 INFO  (GoRttiMapper) Go missing type names: 5` (`GoRttiMapper.java:373`, info)
- `174: 16:02:13 INFO  (HeadlessAnalyzer) REPORT: Analysis succeeded for file: file:///.../target-d61f87246456.bin`
- `180: 16:02:15 INFO  (HeadlessAnalyzer) ANALYZING changes made by post scripts: ...` (last line)

### GoApiSnapshot route, grounded in the pinned Ghidra source

`GoApiSnapshot.getPatchVerDiffFile` emits exactly one of two component messages once the base JSON exists: WARN `Falling back from %s to %s for Go API snapshot` (`GoApiSnapshot.java:160`) or INFO `Using Go API snapshot for %s` (`:163`; the patch loop is skipped when patch == 0). The log has the INFO form at line 122 and **no** WARN form anywhere (grep exit 1). Therefore, [OBSERVED] route = `info`, base-only, no patch diff. This is corroborated by `GoRttiMapper.java:180`: the line-123 INFO is emitted only when `apiSnapshot.getVer()` is non-invalid, i.e. the snapshot was actually loaded, not `EMPTY`. The prediction's `selection = {status: base_only, selected_patch: 0, patch_applied: false, base: go1.25.0.json sha256 54d10162…}` matches the on-disk `go1.25.0.json` (sha256 `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`, re-hashed at report time).

`Untested Go version [..]` is an `Msg.error` at `GoRttiMapper.java:171`; absent. `Missing Go bootstrap type info` (`:359`) absent. So `untested_version` and `missing_bootstrap` are observed, not inferred from silence of a different level.

## Frozen prediction comparison (independent parse) [OBSERVED]

I parsed the raw log with my own line/route regexes (not `log-extract.py`, not `compare.json`) and compared to the frozen JSON. Output (exit 0):

```
FIELD fallback_to         predicted=None       observed=None       match=True
FIELD missing_bootstrap   predicted=False      observed=False      match=True
FIELD snapshot_label      predicted='1.25.0'   observed='1.25.0'   match=True
FIELD snapshot_route      predicted='info'     observed='info'     match=True
FIELD untested_version    predicted=None       observed=None       match=True
EXTRA analyzer_errors_empty  predicted=True   observed=True       match=True
EXTRA eof_reads              predicted=[]     observed=[]         match=True
EXTRA invalid_index_reads    predicted=[]     observed=[]         match=True
ALL_MATCH True
```

`analyzer_errors_empty` is a bool expectation and the extractor's list is `[]`; `compare.py:201-206` implements it as emptiness. `snapshot_label` is a **request echo** (the frozen compare rules themselves label it "non-discriminating: request echo"); it should not be counted as independent confirmation of Go version selection. The discriminating route field is `snapshot_route`, which matches.

Decision-rule table row for cgo: `{d: false, h1: "none", route: "info", fallback_to: null, eof_reads_h1: [], invalid_index_reads_h1: [], invalid_index_reads_h0_incl_walk: [], go_version: "go1.25.0"}`. All match after one normalization: the row uses build-info form `go1.25.0`, while the log prints `GoVer.toString()` = `1.25.0` (leading `go` stripped per `GoBuildInfo.java:488-489`, a basis line of the frozen prediction). A literal string compare here is a false mismatch; the normalized comparison matches. The literal `go1.25.0` does not occur in the log (grep exit 1), so the row's `go_version` is only indirectly log-checkable.

Corroboration (not substitute): re-running the pinned round-17 extractor on the raw log reproduced `observation.json` exactly — all shared keys equal, exit 0:

```
$ python3 -I -B ../round-17/tools/log-extract.py --log runs/t1250-cgo/logs/rea-ghidra-bdYUwH/ghidra.log
exit=0 ; keys_equal True ; all_shared_equal True
extract snapshot_route info classification snapshot_loaded failures [] eof [] inv [] analyzer_errors []
```

## Frozen mechanism rule [OBSERVED + INFERENCE]

Frozen rule text (`predictions/decision-rule.json`, `confirmed`): "every D label's bound ghidra.log reports a Go analysis failure whose Invalid index value(s) include at least one h1_only_invalid_indexes value and no index outside the frozen H1 list, **AND every non-D label shows no Go analysis failure**."

- cgo is non-D. Observed: 0 `Go analysis failure`, 0 `ERROR`, 0 `Invalid index`, 0 `Unable to read past EOF`, 0 `Untested Go version`. `Analysis succeeded` is present (line 174). → **cgo's clause holds.**
- The literal `Go analysis failure` has two emitters in the pinned Base source: `GolangSymbolAnalyzer.added()`'s catch (`GolangSymbolAnalyzer.java:182`, `Msg.error`) and `GolangStringAnalyzer.added()`'s catch (`GolangStringAnalyzer.java:125`, `Msg.error`). cgo's log shows the string analyzer's main run completing normally (`139: 16:02:06 INFO (GolangStringAnalyzer) Go strings found: 3118`) and no failure text from either. The 3 WARN subtype lookups and `Go missing type names: 5` are different code paths and are not failures.
- Cross-label context (outside my label, raw grep only): of the 8 retained logs, only `t1250-vet` has a failure — 1 line, and exactly 1 `Invalid index: 13902080`, which is in `h1_only_invalid_indexes[t1250-vet] = [13902080, 852107777]`; the walk index `1801722468838924630` occurs 0 times in its log. The other 6 non-D logs have 0 failures (`grep -c 'Go analysis failure'`: asm 0, compile 0, cover 0, go 0, gofmt 0, preprofile 0, cgo 0, vet 1). So the retained raw logs are consistent with the rule's `confirmed` side, but the formal verdict needs all binding/gate conditions and is the integrator's to compute; I do not pronounce it from cgo.

```
$ for f in runs/t1250-*/logs/*/ghidra.log; do echo "$(echo $f|cut -d/ -f2) fail=$(grep -c 'Go analysis failure' $f) inv=$(grep -c -E 'Invalid index: [0-9]+' $f)"; done
t1250-asm fail=0 inv=0
t1250-cgo fail=0 inv=0
t1250-compile fail=0 inv=0
t1250-cover fail=0 inv=0
t1250-go fail=0 inv=0
t1250-gofmt fail=0 inv=0
t1250-preprofile fail=0 inv=0
t1250-vet fail=1 inv=1
exit 0
```
- **Positive mechanism is not observable in cgo's log.** `c3.true_kind swiss`, `misread_map_types 2`, `uncommon_map_types 2`, `h0/h1_map_path_failure false` come from the source-model prescan, not from Ghidra output. The log verifies the predicted *outcome silence* only. [INFERENCE] The mechanism can be present and non-fatal when the misread name offset still lands in mapped memory; vet's layout is where it does not. That inference is anchored in the vet stack (`GoName.readStructure` -> `MemoryByteProvider.ensureBounds` -> `Invalid index: 13902080`), not directly in the cgo log.
- Because cgo is predicted silent under both H1 and H0, this label cannot refute either hypothesis. It is a correct negative control, not positive confirmation.

### Capture-tail gap and why it does not hide a cgo failure [INFERENCE, source-anchored]

All 8 retained logs end at the same phase — `ANALYZING changes made by post scripts` — because capture is a polling copy: `receipt.json` `log_capture_limit` says "polling copy; lines written after the final poll before REA deletes its runtime root can be missing". For cgo: last copy `19:02:15.677240Z`, analyze process ended `19:02:16.177824Z`, so at most ~0.5 s of shutdown/post-script lines are absent; the log's last line is `16:02:15 -0300`.

For the **symbol analyzer — the path that emits vet's mechanism failure** — the gap cannot hide a re-emitted failure: it emits `Go analysis failure` only inside `added()`, which returns early on the same transaction (`GolangSymbolAnalyzer.java:113`) and on `isAlreadyAnalyzed(program)` (`:119-120`, message "Go analysis already performed, skipping."); the analyzed flag is set at `:178` only after the main run succeeds, and cgo's main run did succeed (`Analysis succeeded`, line 174). A post-script re-run therefore skips Go markup rather than re-emitting a failure. The skip message itself is in the uncaptured tail, so this closure is inference from the pinned source plus the observed success line, not a direct observation.

The **string analyzer** has no such guard (`GolangStringAnalyzer.added()` carries no `lastTxId`/`isAlreadyAnalyzed` early return); a scoped post-script re-run could in principle emit `Go analysis failure` inside the uncaptured tail. Its full-program run completed normally at line 139 (`Go strings found: 3118`; the analysis summary attributes 1.166 s to `Golang Strings`), and the tail is ~0.5 s, so a re-run inside that window is possible but unsupported by any evidence. This is a residual of the capture, not of the H1 mechanism, and it does not affect the symbol-analyzer closure above.

## Binding chain and the self-pin finding [OBSERVED]

- Recorded gate result at measurement time: `W19/evidence/receipt-validation/t1250-cgo.json` — `exit 0`, `valid 1`, `require_mid_maps true` (all 8 labels' recorded files show exit 0 / valid 1).
- Subject pins still match live: carrier sha256 = prediction carrier sha256 (`d61f8724…`); typeinfo `go1.25.0.json` sha256 = prediction `selection.base.sha256` (`54d10162…`); prediction blob = freeze-commit blob (`b42a62bf…`, `git show a1140e7:… | sha256sum`); retained log sha256 = observation + receipt (`92b560d5…`); `pins/mid-1.json` and `pins/mid-2.json` both pin prediction `b42a62bf…` and carrier `d61f8724…`; `pins_pre`/`pins_post` compare equal; `mid_run_drift_steps []`. `pins.py` sha256 is unchanged from the run (`9e9c7250…`).
- Re-running `receipt-validate.py --require-mid-maps` today exits 1 with exactly two findings (one file, two codes) — both on the validator itself:

```
$ python3 -I -B ../round-17/tools/receipt-validate.py --require-mid-maps runs/t1250-cgo/receipt.json
exit 1
$ git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:.ufo/waves/round-17/tools/receipt-validate.py > /tmp/receipt-validate-B.py
$ python3 -I -B /tmp/receipt-validate-B.py --require-mid-maps runs/t1250-cgo/receipt.json
exit 1
findings:
sha256_mismatch  expected 70672eb3…  actual 6afb7ef6…  path .../round-17/tools/receipt-validate.py
size_mismatch    expected 46047      actual 52682      same path
```

366 checks ran; no other file was flagged. The same result occurs when running the frozen `8a8da7e` blob of the validator (`70672eb3…`), because it hashes the **live working tree**, not a revision.
- Cause: the integration commit `4f6c73f8` changed `receipt-validate.py` (`8a8da7e`/`a1140e7` blob `70672eb3…` -> `main` blob `9276b198…`, 51075 B), and the lane worktree currently carries an uncommitted edit (`git status --porcelain` -> ` M .ufo/waves/round-17/tools/receipt-validate.py`, +33/-5 vs `main`, live sha `6afb7ef6…`, 52682 B). The dirty file is not mine and I did not modify it.
- Consequence for calibration: the gate as frozen ("receipt-validate.py --require-mid-maps exits 0 on its receipt") is **tool-version sensitive and not reproducible verbatim after any edit to the validator**, for every label. The run-time result stands as recorded, and every subject pin still verifies; a re-evaluation should run the pinned tool content with revision-scoped reads, or exclude self-pins. This is a tooling-freshness finding, not drift in the cgo evidence.

## Freshness rechecks at report time [OBSERVED]

- Carrier and Ghidra typeinfo digests re-hashed now: both match the frozen prediction/pins.
- Prediction blob equals freeze commit; `predictions/decision-rule.json` unchanged between `a1140e7` and `main` (`git diff --stat a1140e7..main -- predictions claims.json contract.md` -> only `claims.json`, +12/-2, i.e. the declared C3 amendment including the count `0 -> 8`).
- C3 run artifacts were added in `4f6c73f8` (16:09:17 -0300) and are unchanged afterward (`git diff --stat 4f6c73f8..main -- runs evidence predictions tools` -> only C1/C2 evidence files and `tools/routed-r18.py`).
- Main tip has advanced past the run base to `d0690fd4`; nothing in the C3 evidence chain references the newer tip.

## Residual unknowns

- The mechanism (Swiss map layout bound to `internal/abi.OldMapType`) is not directly observable in a Ghidra log; only its outcome is. cgo's silence would also be produced by H0, so it is non-discriminating.
- The retained log is a polling snapshot with a ~0.5 s uncaptured tail; the symbol-analyzer closure is source-anchored inference (guard + observed success), not an observed skip line, and a string-analyzer re-run inside that tail is not excluded (see capture-tail section).
- `snapshot_label` is a request echo and is non-discriminating by the frozen compare rule; `go_version` in the rule table needs the documented `go`-prefix normalization.
- Type-count cross-check (depth note, not part of the prediction): cgo's log `Found 2218` equals prescan `h1 indexed 2189 + discovered unindexed 29`, but that identity fails for 5 of the other 7 labels (compile -6, cover -1, go -3, gofmt -3, vet -1; asm and preprofile match), so it is a coincidence here, not a law; the prescan's `walk.unindexed_types = 0` does not model Ghidra's `Discovered 22-242 unindexed` lines. [INFERENCE] No predictive weight should be assigned to the cgo arithmetic match.
- No installs, no production edits, no delegation. Only this report was written.

Report: .ufo/waves/round-19/w2/OutcomeCgo.md
