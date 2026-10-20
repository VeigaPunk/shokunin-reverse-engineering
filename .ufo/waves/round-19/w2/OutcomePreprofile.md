# Outcome preprofile — C3 raw-log audit of t1250-preprofile

Seat: KaidokuR19.OutcomePreprofile-3 (wave 2, read-only scout). No delegation, no production
edits, no REA/MCP device, no REA `analyze`/`search`/`decompile`, no Ghidra run, no carrier
execution, no builds, no installs. All writes are this report and `/tmp/kr19-*` scratch outputs
(Ghidra source extraction, validator runs); no Git writes and no `jj` anywhere.

- Lane (read-only): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Observed tips (the lane advanced during the audit; both are recorded):
  - `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` at `2026-10-20T19:20:54Z` — tip while the log,
    observation, compare, receipt and prediction were parsed (`git rev-parse refs/heads/main`, exit 0).
  - `279e8b19c51658bfd05b9e31a1c0894ab2e70537` at `2026-10-20T19:22:41Z` (`git rev-parse
    refs/heads/main`, exit 0; committer time `2026-10-20T16:21:51-03:00`, "wave-two fixes — list
    identity, alias classifier coverage, strict replay, scope and source qualifications").
  - Relevant bytes did **not** move between the two tips: the prediction blob is
    `21d85035a04f7f6711b2361911ea19ae817db46f` at both, the worktree prediction sha256 is
    `290b04e75069f61785948f27cad45443541f8802844ea6a45e81e7f762e938bd` at both, and
    `git status --porcelain` over `predictions/` and `runs/t1250-preprofile/` was empty (exit 0).
    `receipt-validate.py` **did** move (`9276b198…` at `d0690fd` → `6afb7ef6…` at `279e8b19`);
    §5 re-runs both and gets the same finding shape.
- Contract baseline B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. C3 freeze commit
  `a1140e76fffdc1be032d9d813dbb686157803bbc` (`2026-10-20T15:57:44-03:00`), ancestor of both
  observed tips.
- Label: `t1250-preprofile`. Carrier:
  `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/preprofile`.
- Bound log: `.ufo/waves/round-19/runs/t1250-preprofile/logs/rea-ghidra-aURSDn/ghidra.log`.
- Frozen prediction: `.ufo/waves/round-19/predictions/t1250-preprofile.prediction.json`.

## Verdict (short)

- **Prediction match: exact, 8/8 compared fields, zero substantive mismatches** [OBSERVATION],
  parsed from the raw `ghidra.log` without using `compare.json` as evidence. Route `info` at
  `1.25.0`; no Go analysis failure, no `Invalid index`, no EOF read, no fallback, no bootstrap
  miss, no `Untested Go version`, no `ERROR` line of any component.
  Five fields are byte-equal; three (`fallback_to`, `snapshot_label`, `untested_version`) are
  scalar-vs-container representation differences that the frozen comparator's declared rules
  resolve as equality (§3). A byte-strict reading would call those three `DIFF`; the semantics
  do not differ.
- **Frozen mechanism rule for this label: holds** [OBSERVATION]. `t1250-preprofile` is non-D,
  predicted silent under **both** H1 and H0 (map-path and the separately merged full-walk read
  lists are all empty), and the bound log is silent. This is a successful negative prediction,
  **not** discriminating evidence for H1 over H0: a silent carrier can only fail to refute.
  The cohort sweep of my own greps agrees with the rule's literal `confirmed` clause: only
  `t1250-vet` reports `Go analysis failure`, with `Invalid index: 13902080` (an H1-only value),
  and no non-D log reports one (§4).
- **Binding gate: context-dependent, and the frozen text was not amended** [OBSERVATION +
  INFERENCE]. The run-time validation retained under `evidence/receipt-validation/` is green
  (`exit 0`, `valid: 1`); a live re-run at either wave-2 tip is red with exactly two findings
  (`sha256_mismatch`, `size_mismatch`) **on `receipt-validate.py`'s own bytes only** — a
  self-referential pin overtaken by the wave-1/wave-2 edits of that tool. No other pinned path
  is flagged (`checks_performed=360`, both findings on that one path). Under the literal text of
  `predictions/decision-rule.json:3` (`receipt-validate.py --require-mid-maps exits 0`) the
  label is **unbound at the delivered tip**; under the run-time/source-bound reading it is
  **bound and valid**. Report the label as *match with a declared binding-drift exception*;
  §5 gives both readings and the L1's existing substitution at `verify.py:108-110,674-681`.

## 1. Binding chain: carrier → prediction → log

Commands (lane-relative, from the lane root or `runs/t1250-preprofile`; all exit codes shown):

```
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/preprofile            # exit 0
eff3b19676f41d95eb598fa7520a9f44c2014db65a5a7470a2ca5c4cfa3f840b
$ sha256sum runs/t1250-preprofile/logs/rea-ghidra-aURSDn/ghidra.log                     # exit 0
4815553d653a8fc8bf126c85671405e249705d2c7ced05baadd7b9612eb99242
$ wc -l -c runs/t1250-preprofile/logs/rea-ghidra-aURSDn/ghidra.log                      # exit 0
163 15980
$ sha256sum predictions/t1250-preprofile.prediction.json                                # exit 0
290b04e75069f61785948f27cad45443541f8802844ea6a45e81e7f762e938bd
$ sha256sum -c predictions/SHA256SUMS                                                   # exit 0, 19/19 OK
$ git rev-parse a1140e7:.ufo/waves/round-19/predictions/t1250-preprofile.prediction.json        # exit 0
21d85035a04f7f6711b2361911ea19ae817db46f
$ git rev-parse 279e8b19:.ufo/waves/round-19/predictions/t1250-preprofile.prediction.json       # exit 0
21d85035a04f7f6711b2361911ea19ae817db46f
$ git cat-file blob 21d85035a04f7f6711b2361911ea19ae817db46f \
    | cmp - predictions/t1250-preprofile.prediction.json                                 # exit 0
$ sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json  # exit 0
54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252
$ stat -c '%s %n' .../typeinfo/golang/go1.25.0.json                                      # exit 0
10081618 .../typeinfo/golang/go1.25.0.json
$ ls .../typeinfo/golang/patchverdiffs/ | grep -F 1.25                                    # exit 1 (no match)
$ jq -c '{carrier, retained_logs, bound_sessions, unbound_sessions}' runs/t1250-preprofile/receipt.json  # exit 0
carrier.sha256_pre == sha256_post == eff3b19676f4…
retained_logs[0].binding == {logfile_ok: true, md5_ok: true, target_ok: true}
bound_sessions == ["/tmp/kr17-rea-lbl8xl82/rea-ghidra-aURSDn"]; unbound_sessions == []
$ jq -c '.pins_compare' runs/t1250-preprofile/receipt.json                               # exit 0
{"changed":[],"equal":true,"errors":[],"missing":[],...}   (152 pre / 152 post entries)
```

[OBSERVATION] Chain, all links exact:

1. The prediction's carrier sha256 (`…prediction.json:34`) equals the on-disk carrier digest and
   both receipt digests (`sha256_pre == sha256_post`).
2. The log itself names the carrier: `ghidra.log:59` imports
   `target-eff3b19676f4.bin` (first 12 hex of the prediction sha) with
   `?MD5=3c3de3622961b949ae8134796c2a72d4`, equal to `receipt.carrier.md5_pre`.
3. Log bytes/sha256 equal `observation.json:165,168` and `receipt.retained_logs[0].files.ghidra.log`;
   the three binding booleans are true and `unbound_sessions` is empty.
4. The prediction blob is byte-identical to the freeze-commit blob and unchanged at both wave-2
   tips; `SHA256SUMS` verifies 19/19 (exit 0).
5. The route's loaded snapshot is the frozen selection base: the installed
   `go1.25.0.json` sha256/size (`54d1016…`, `10081618`) equal
   `prediction.selection.base.sha256/size`; there is no `1.25` patch-diff file (grep exit 1),
   consistent with `selection.patch_applied=false`, `selected_patch=0`, `status=base_only`.
6. Mid-run pin `pins/mid-1.json` holds 152 entries at `2026-10-20T19:05:51.185Z`; pre/post
   entries are equal with no change, error or missing path.

[INFERENCE] These bytes are the run's Ghidra log for the predicted carrier; the binding is not
merely name-based. [LIMIT] The log is a polling copy (`receipt.log_capture_limit`), so
completeness is bounded — see §5.

## 2. The four assigned signals in the raw log

Prediction fields: `predictions/t1250-preprofile.prediction.json:20,25-30,36-46`. Exits are this
seat's greps over `L=runs/t1250-preprofile/logs/rea-ghidra-aURSDn/ghidra.log`, not
`compare.json`.

| Signal | Frozen prediction | Raw-log observation | Command exit |
|---|---|---|---|
| Go analysis failure | `c3.h1_kind=none`; `c3.h1_map_path_failure=false`; `c3.h0_map_path_failure=false`; `extra.analyzer_errors_empty=true` | no `Go analysis failure`; **zero** `ERROR` lines of any component; Go analysis ran to completion (`:106-108,113-123`, 18 s timing `:154`); `Analysis succeeded` at `:157` | `grep -n 'Go analysis failure'` = 1; `grep -n 'ERROR'` = 1 |
| Invalid index | `extra.invalid_index_reads=[]`; `c3.h0_reads_including_walk.invalid_index=[]` | no `Invalid index` token | `grep -n 'Invalid index'` = 1; `grep -n 'Invalid index: '` = 1 |
| EOF read | `extra.eof_reads=[]`; `c3.h0_reads_including_walk.eof=[]` | no `Unable to read past EOF`, no `EOF`, no `EOFException`, no `Exception` | `grep -n 'past EOF'` = 1; `grep -n 'EOF'` = 1; `grep -n 'Exception'` = 1 |
| GoApiSnapshot route | `expected.snapshot_route=info`; `snapshot_label=1.25.0`; `fallback_to=null`; `missing_bootstrap=false`; `untested_version=null` | `:104 INFO (GoApiSnapshot) Using Go API snapshot for 1.25.0`; `:105 INFO (GoRttiMapper) Using Go API snapshot for version 1.25.0`; no fallback/bootstrap/`Untested` text | `grep -n 'GoApiSnapshot'` = 0 → `:104`; `grep -n 'Using Go API snapshot'` = 0 → `:104,105`; `grep -n 'Falling back'` = 1; `grep -n 'Untested'` = 1; `grep -n 'Missing Go bootstrap'` = 1 |

Exact command block (each line's exit is the integer after `exit=`):

```
$ L=logs/rea-ghidra-aURSDn/ghidra.log
$ grep -n 'Go analysis failure' "$L"                            exit=1
$ grep -n 'Invalid index' "$L"                                  exit=1
$ grep -n 'Invalid index: ' "$L"                                exit=1
$ grep -n 'past EOF' "$L"                                       exit=1
$ grep -n 'EOF' "$L"                                            exit=1
$ grep -n 'Exception' "$L"                                      exit=1
$ grep -n 'ERROR' "$L"                                          exit=1
$ grep -n 'Falling back' "$L"                                   exit=1
$ grep -n 'Untested' "$L"                                       exit=1
$ grep -n 'Missing Go bootstrap' "$L"                           exit=1
$ grep -n 'Analysis succeeded' "$L"                             exit=0  -> :157
$ grep -n 'ANALYZING changes made by post scripts' "$L"         exit=0  -> :163
$ grep -n 'GoApiSnapshot' "$L"                                  exit=0  -> :104
$ grep -n 'Using Go API snapshot' "$L"                          exit=0  -> :104,105
$ grep -n 'WARN' "$L"                                           exit=0  -> :109-112 only
$ grep -c '' "$L"                                               exit=0  -> 163
$ wc -c < "$L"                                                  exit=0  -> 15980
```

**Parse traps, observed.** `grep -in 'invalid'` exits 0 and hits `ghidra.log:60`
`Skipping section [.gosymtab] with invalid size 0x0` — only the exact token `Invalid index`
is the `EOFException` formatter (`log-extract.py:114`). Likewise `grep -i 'failed'` hits the
four `GoTypeManager` subtype WARNs (`:109-112`), which are not failures (§6). The success
report is also not a failure-freedom signal: `t1250-vet` carries both
`ERROR … Go analysis failure` at `runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:186` and
`REPORT: Analysis succeeded` at `:276`. The negative signal is the absent `ERROR` line, not
`:157`.

**Route semantics, source-anchored.** `GoApiSnapshot.java:148-166` emits exactly one of
WARN `Falling back from A to B for Go API snapshot` (when a lower patch diff is substituted) or
INFO `Using Go API snapshot for %s` (when `patchVer == goVer`, including patch 0), and nothing
when the base JSON is missing (`:122-126`). `GoRttiMapper.java:174-181` then echoes the loaded
snapshot version at INFO only when `getVer()` is valid; `:170-171` emits
`ERROR … Untested Go version [%s]` outside `SUPPORTED_VERSIONS = "1.15-1.25"` (`:79`).
[OBSERVATION] Both INFO lines are present, the WARN/ERROR alternatives are absent, and the
loaded file's digest equals the frozen selection base. [INFERENCE] The route is the
base-only/patch-0 `info` route on the frozen `go1.25.0.json`; the GoRttiMapper line alone would
be a request echo and is corroborating, not discriminating (`log-extract.py:98-102`).

`observation.json` agrees line-for-line: `:2` `analyzer_errors: []`, `:7`
`classification: "snapshot_loaded"`, `:8` `eof_reads: []`, `:162` `invalid_index_reads: []`,
`:170` `missing_bootstrap: false`, `:171` `snapshot_fallbacks: []`, `:175`
`snapshot_route: "info"`, `:176` `symbol_analysis_failures: []`, `:177`
`untested_versions: []`, `:163` `invalid_version_strings: []`.

## 3. Exact field comparison against the frozen prediction

The table below was recomputed from the raw log (values checkable against §2) and compared to
`predictions/t1250-preprofile.prediction.json`; it is not a read of `compare.json`.

| Prediction field | Predicted | Observed (raw-log basis) | Frozen comparator rule (fields `compare.json:5-56`; rules `:57-63`) | Verdict |
|---|---|---|---|---|
| `expected.missing_bootstrap` | `false` | `false` (no `Missing Go bootstrap`; reading proceeded `:103-105`) | equality | **exact** |
| `expected.snapshot_route` | `"info"` | `"info"` (`:104` INFO; no fallback WARN) | equality | **exact** |
| `extra.analyzer_errors_empty` | `true` | `true` (0 `ERROR` lines) | derived | **exact** (and stronger than the extractor predicate, §6) |
| `extra.eof_reads` | `[]` | `[]` (no `past EOF`/`EOF`/`Exception`) | exact list | **exact** |
| `extra.invalid_index_reads` | `[]` | `[]` (no `Invalid index`) | exact list | **exact** |
| `expected.fallback_to` | `null` | `[]` (`snapshot_fallbacks` empty) | contains-or-both-empty | **semantic match** (representation differs) |
| `expected.untested_version` | `null` | `[]` (`untested_versions` empty) | contains-or-both-empty | **semantic match** (representation differs) |
| `expected.snapshot_label` | `"1.25.0"` | `["1.25.0"]` (`:104,105`) | contains-or-both-empty; rule itself labels this **non-discriminating** (request echo) | **semantic match** (representation differs) |

Result: **8/8 match, 5 byte-equal + 3 representation-normalized, 0 substantive mismatches.**
`compare.json` independently records `"all_match": true` (line 2) with all eight `"match": true`
(lines 5-56), but that file is treated here as a downstream artifact, not as the evidence.

Additional frozen `c3` fields (not columns of `compare.py`), checked against the same log:

| Field | Frozen | Observation basis | Verdict |
|---|---|---|---|
| `c3.h1_kind` | `"none"` | `symbol_analysis_failures == []` (`observation.json:176`; no `Go analysis failure`) | **match** (string↔empty-list is representational; the raw log shows no failure) |
| `c3.h1_map_path_failure` | `false` | no `Go analysis failure` | **match** |
| `c3.h0_map_path_failure` | `false` | no `Go analysis failure` | **match** |
| `c3.h0_reads_including_walk.eof` | `[]` | `[]` | **exact** |
| `c3.h0_reads_including_walk.invalid_index` | `[]` | `[]` | **exact** |
| `c3.misread_map_types` / `uncommon_map_types` | `3` / `3` | **not log-observable**; prescan `map_types=30`, `misread_map_types=3`, `uncommon_map_types=3`, `true_kind_witness={map_bucket_strings:0, map_group_strings:27}` | static-model value, consistent with the frozen prediction; do **not** score the log as confirming it (§6) |
| `c3.true_kind` | `"swiss"` | not log-observable; prescan/source-model value | same |
| `c3.diagnostic_r19` / `emulator_diagnostic_field` | `false` / `false` | D is defined by map-path booleans (`decision-rule.json:2`), not the emulator's `diagnostic` field (w1 `H0H1Semantics.md`) | consistent |

`prediction.extra_expectations` for a `none` label is generated as `analyzer_errors_empty`
(`gen-predictions.py:71-72`); `t1250-vet` instead gets `analyzer_errors_contain: "Go analysis
failure"` (`:73-74`). So the frozen comparator for this label tests absence, correctly.

## 4. Frozen mechanism rule applied

Rule text: `.ufo/waves/round-19/predictions/decision-rule.json:5` (`confirmed`), `:28`
(`refuted`), `:2` (D definition: H1 map-path true **and** H0 map-path false), `:21` (H1-only
invalid indexes), `:126` (walk indexes common to both hypotheses), `:4` (compare exit reported
per label; the mechanism verdict is decided from the bound log). This label's row is `:104`
(`d: false`, `h1: "none"`, `route: "info"`, both read lists empty); vet's is `:121`.

**Preprofile is non-D.** Its frozen prediction has `h1_map_path_failure=false` and
`h0_map_path_failure=false` (`prediction.json:26,20`), `h1_kind="none"` (`:25`), and
`invalid_index_reads_h1=[]` with `h0_reads_including_walk=[]` (`:43-46`, `:19-24`). The prescan
also shows the **full emulator walk** clean under both hypotheses — `walk.failed={h0:false,
h1:false}`, `indexed_types={h0:1104,h1:1158}`, `unindexed_types={h0:0,h1:0}` — so the label is
silent under both H1 and H0 even before the map-path booleans.

[OBSERVATION] The bound log matches: no `Go analysis failure`, no `Invalid index`, no EOF read
(§2). The rule's non-D clause ("every non-D label shows no Go analysis failure") therefore
holds for `t1250-preprofile`; the `refuted` clause ("a non-D label fails") is not triggered by
this label.

[INFERENCE] This is a **non-discriminating** success: because the emulator predicted silence
under H1 and H0 alike, silence cannot distinguish Swiss-map misbinding from the true layout.
The label's value is that it does not refute, and that its negative prediction was realized;
confirmatory weight would have to come from a D label.

**Cohort raw-log sweep (my own greps, no compare.json).** All eight bound logs, same predicates
(`grep -c -F 'Go analysis failure'`, `grep -c -F 'Invalid index'`, `grep -c -E ' (ERROR) '`):

| Label | Log lines | `Go analysis failure` | `Invalid index` | `ERROR` lines | Last log line |
|---|---:|---:|---:|---:|---|
| `t1250-asm` | 227 | 0 | 0 | 0 | `ANALYZING changes made by post scripts` |
| `t1250-cgo` | 180 | 0 | 0 | 0 | same |
| `t1250-compile` | 432 | 0 | 0 | **1** | same |
| `t1250-cover` | 250 | 0 | 0 | 0 | same |
| `t1250-go` | 576 | 0 | 0 | 0 | same |
| `t1250-gofmt` | 182 | 0 | 0 | 0 | same |
| `t1250-preprofile` | 163 | 0 | 0 | 0 | same |
| `t1250-vet` | 282 | **1** | **1** | **1** | same |

```
$ for d in t1250-*/; do L=$(ls $d/logs/*/ghidra.log|head -1); ...; done        # exit 0
$ grep -n 'Invalid index: [0-9]*' runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log   # exit 0
229:Invalid index: 13902080
```

[OBSERVATION] Vet's only reported index, `13902080` (`…/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:229`,
inside the `Go analysis failure` at `:186`), is in the frozen H1-only set
`{13902080, 852107777}` (`decision-rule.json:21`); the walk index `1801722468838924630`
(`:126`) does not appear; no index outside the frozen H1 list appears. The seven non-D logs
report no `Go analysis failure`. The literal `confirmed` text therefore holds on the raw logs.

**Calibration caveats on "holds"** [OBSERVATION + INFERENCE]:

1. `t1250-vet`'s `compare.json` mismatches the frozen full H1 list (predicted three reads,
   observed one). That is the expected-red encoded at `verify.py:112`; the mechanism rule only
   requires "at least one h1-only value and no outside index". The rule is deliberately
   lenient about the predicted-but-absent `852107777` and the walk index. Do not report the
   full-list prediction as confirmed.
2. `t1250-compile` has one `ERROR`, at
   `runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log:347`:
   `Analysis Task: Golang RTTI Propagation (deferred) - element cannot be mapped to a null key
   java.lang.NullPointerException`. It is **not** the frozen `Go analysis failure` predicate
   (`log-extract.py:115`), and the extractor's `analyzer_errors` counts only `ERROR` records
   whose component starts with `Golang` (`log-extract.py:243-244`), whereas this component is
   `AnalysisTaskWrapper`. So the literal non-D clause holds, but "silent" is predicate-scoped:
   a Go-RTTI task did fail. That label's verdict belongs to `OutcomeCompile`, not here.
3. The rule is asymmetric: seven realized negative predictions carry little discriminative
   weight; the mechanism verdict effectively rests on `t1250-vet`.

## 5. Binding gate, liveness and freshness

**Run-time evidence (freeze-era).** `evidence/receipt-validation/t1250-preprofile.json` records
`exit: 0`, `counts {invalid:0, receipts:1, unreadable:0, valid:1}`, `checks_performed: 360`,
`findings: []`, `pins_path: /tmp/pins.py` (lines 2-20). The out-of-lane pins file is not a
divergence [OBSERVATION]:

```
$ sha256sum /tmp/pins.py                                                                # exit 0
9e9c72507de429c913891c65ffeafda9a686fee532d6a9dcfcd42b8092639fe0
$ git cat-file blob a1140e7:.ufo/waves/round-17/tools/pins.py | sha256sum               # exit 0
9e9c72507de429c913891c65ffeafda9a686fee532d6a9dcfcd42b8092639fe0
$ sha256sum .ufo/waves/round-17/tools/pins.py                                           # exit 0
9e9c72507de429c913891c65ffeafda9a686fee532d6a9dcfcd42b8092639fe0
$ git log --oneline a1140e7..279e8b19 -- .ufo/waves/round-17/tools/pins.py             # exit 0, no commits
```

`/tmp/pins.py` is byte-identical to the freeze blob and to the current lane copy, so the
retained exit-0 validation is consistent with lane bytes of that tool.

**Live re-runs (read-only).**

```
# at d0690fd, validator 9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45 / 51075 B
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-preprofile/receipt.json                       # exit 1
counts {invalid:1, receipts:1, unreadable:0, valid:0}; checks_performed 360
findings: sha256_mismatch + size_mismatch, both path
  .ufo/waves/round-17/tools/receipt-validate.py (expected 70672eb…/46047; actual 9276b198…/51075)

# at 279e8b19, validator 6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762 / 52682 B
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-preprofile/receipt.json                       # exit 1
counts {invalid:1, receipts:1, unreadable:0, valid:0}; checks_performed 360
findings: sha256_mismatch + size_mismatch, same single path (actual 6afb7ef6…/52682)
```

[OBSERVATION] At both tips the **only** finding is the checking tool's own pin: the receipt
pins `receipt-validate.py` at the freeze blob `70672eb3…`/46047 B, and the lane has since
edited that file (wave-1 integration `4f6c73f`, then wave-2 `279e8b19`). No other pinned path
is flagged (360 checks, two findings, one path). The carrier digest, log digest, binding
booleans and mid-run maps all pass.

**How the integrated verifier treats this** [OBSERVATION]. `verify.py:108-110` records the
expected exit for `receipt-validate-*` as `1` with the comment "Live receipts correctly detect
the forward-edited producer validator; source-bound clean validations are retained separately
under evidence/". `verify.py:674-681` requires exactly two findings
(`{sha256_mismatch, size_mismatch}`) all on `.ufo/waves/round-17/tools/receipt-validate.py`,
**plus** the retained JSON with `counts {invalid:0, …, valid:1}`. My two live re-runs match that
expected shape exactly.

**Consequence for the frozen text** [OBSERVATION + INFERENCE]. `decision-rule.json:3` says a
label counts only if the validator "exits 0 on its receipt" — with no substitution for a
forward-edited checker. At the delivered revision that literal test fails, so `t1250-preprofile`
is *unbound* under the written gate; under the run-time validation (exit 0, retained) it is
*bound and valid*, and the red is a self-pin, not carrier evidence. `claims.json:40` phrases
the count as "labels with a bound retained log and compare.json" and does not mention the
validator self-pin, so the amendment does not resolve the conflict. This report states both
readings; choosing or amending is the L1's, and no production edit is made here. Reporting the
label as *match with a declared binding-drift exception* is the only formulation that does not
silently drop either fact.

**Freshness anchors.** `2026-10-20T19:20:54Z` and `19:22:41Z` tips above; run artifact mtimes
`2026-10-20 16:06:14.20` (log), `16:06:14.78` (observation), `16:06:14.80` (compare),
`16:07:56.36` (receipt-validation evidence), local `-03`. The log's first analysis line is
`16:05:54` (`:103-104`), inside the recorded pin window
`19:05:50.42Z`–`19:06:14.75Z`; the prediction was frozen at `15:57:44-03` (≈8 min before the
run's `19:05:50Z` start). Prediction blob unchanged at both tips; `SHA256SUMS` 19/19; no
uncommitted changes under `predictions/` or `runs/t1250-preprofile/`. Tip re-checked after this
report was written: at `2026-10-20T19:31:13Z` `refs/heads/main` was still
`279e8b19c51658bfd05b9e31a1c0894ab2e70537` (exit 0).

**Truncation, bounded.** The polling copy ends at `:163`
`ANALYZING changes made by post scripts` (`grep` exit 0). All eight retained logs end on that
same line, so it is harness-wide, not label-specific. The Go-analysis window is fully inside
the retained bytes: `:103` reading info → `:104-108` snapshot/version/types → `:109-123` markup
and fixups → `:124-155` timing (18 s) → `:157` analysis succeeded → `:158-163` post scripts.
[INFERENCE] The failure class sought here is emitted inside the main analysis (vet: `:186`,
before its `:276` success), so this tail truncation cannot hide a preprofile failure. The log's
mtime `19:06:14.206Z` is 0.545 s before the post-pin snapshot `19:06:14.751Z`; [INFERENCE] that
residual gap covers only HeadlessAnalyzer completion chatter, not the Go analysis window.

## 6. Depth and calibration findings (preprofile-scoped)

1. **"Silent" is not literal silence.** The log carries four `GoTypeManager` WARNs at
   `ghidra.log:109-112` (`Failed to get subtype … runtime.elfSym`, `byte`, `uint16`,
   `time.Timer`). No frozen prediction field enumerates WARNs, and the strings are **not**
   mechanism evidence: the same class appears in 7/8 carriers (my sweep: `subtypes=3-4` in
   asm/cgo/compile/cover/go/gofmt/preprofile, `0` in vet because it fails earlier) and in a
   round-18 silent application, `.ufo/waves/round-18/runs/calib-notesmd-cli/logs/rea-ghidra-tpzD5t/ghidra.log`
   (3 subtype WARNs, 0 `ERROR`). A naive `grep -i failed` returns four hits; the frozen
   predicate does not.
2. **Static vs observed must not be conflated.** `misread_map_types=3`, `uncommon_map_types=3`,
   `true_kind="swiss"` (`prediction.json:28-30`) are emulator/source-model values; the Ghidra
   log prints no map-type names. The log confirms only the predicted *outcome* (silence). Any
   report that says the log "confirms three Swiss maps were misread" is overclaiming.
3. **`snapshot_label` is a request echo.** The comparator itself labels it
   "non-discriminating: request echo" (`compare.json:14-17`); `GoRttiMapper.java:179-180` prints
   the requested version. The discriminating evidence is the `GoApiSnapshot` INFO route plus
   the loaded typeinfo identity (`54d1016…`, `10081618 B`). Matching the label alone would be
   nearly vacuous.
4. **`analyzer_errors_empty` is component-scoped.** `log-extract.py:243-244` counts only
   `ERROR` records whose component starts with `Golang`; a `GoRttiMapper` `ERROR` (e.g.
   `Untested Go version`, source `:170-171`) would not populate it, though `untested_versions`
   and route checks could. For preprofile this narrowness is moot — zero `ERROR` lines of any
   component — but the field name overstates its breadth in general.
5. **The mid pin is not mid-analysis.** `pins/mid-1.json` was taken at `19:05:51.185Z`, 1.6 s
   after `pins_pre` and before the log's first line (`19:05:52Z`); the Go analysis runs
   `19:05:54`–`19:06:12Z`. Drift coverage comes from full pre/post equality (152 entries, zero
   changed/errors/missing, `receipt.pins_compare`), which brackets the whole run; the "mid"
   label adds no sample inside the analysis window.
6. **Success ≠ no failure.** `vet` proves an `ERROR … Go analysis failure` and
   `REPORT: Analysis succeeded` coexist (`:186`, `:276`). For any future negative prediction,
   the absence of the `ERROR` record is the signal; the success report is not.

## 7. Limits

- [LIMIT] Read-only audit. No REA/Ghidra command, no MCP device, no carrier execution, no
  build/test/format run, no install or update (nothing to record under the tooling directive).
  No delegation (leaf seat).
- [LIMIT] `compare.py` was **not** re-run: the assignment requires the raw log, and
  `compare.json` is reported only as a downstream artifact (`exit 0`, `all_match: true`).
- [LIMIT] The source-bound exit-0 was not reproduced by checking out `a1140e7` (that would need
  rewriting absolute pin paths or a lane write). Instead: the retained green JSON, the
  byte-identical `/tmp/pins.py` vs freeze blob, the 360-check re-runs with no non-self finding,
  and `verify.py`'s own expected-red contract are reported separately (§5).
- [LIMIT] Cohort statements cover only the four assigned signals in the eight retained raw
  logs; detailed verdicts for the other labels belong to their seats. The `.gosymtab` line
  (`:60`) and the four subtype WARNs are reported as non-signals, not suppressed.
- [LIMIT] No LSP device is exposed in this harness; the evidence targets are logs, JSON, Git
  blobs and Java source in a zip, so all anchors are text/line references rather than symbol
  references.

Report: .ufo/waves/round-19/w2/OutcomePreprofile.md
