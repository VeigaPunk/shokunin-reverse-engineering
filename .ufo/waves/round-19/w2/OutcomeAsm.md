# Outcome asm — C3 raw-log audit of t1250-asm

Seat: KaidokuR19.OutcomeAsm-3 (wave 2, read-only scout, leaf). No delegation, no production
edits, no REA/MCP device, no REA `analyze`/`search`/`decompile`, no Ghidra run, no carrier
execution, no installs. Scratch files only under `/tmp` (`/tmp/asm-extract.json`,
`/tmp/asm-compare-repro.json`).

- Lane (read-only): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Contract baseline B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.
- C3 freeze commit: `a1140e76fffdc1be032d9d813dbb686157803bbc` (2026-10-20T15:57:44-03:00),
  ancestor of the tip (`git merge-base --is-ancestor a1140e7 refs/heads/main` → exit 0).
- Observed main tip at audit start: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; the tip
  advanced during the audit to `279e8b19c51658bfd05b9e31a1c0894ab2e70537`
  (16:21:51-03, wave-two fixes). Both values are recorded where they matter; the C3
  predictions and run evidence were not modified by either commit.
- Label: `t1250-asm`; carrier `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/asm`.
- Raw log: `.ufo/waves/round-19/runs/t1250-asm/logs/rea-ghidra-cWUKB0/ghidra.log`
  (227 lines, 38277 bytes, 2026-10-20 16:01:35.627 -03).

Report: .ufo/waves/round-19/w2/OutcomeAsm.md

## Verdict (short)

- **Prediction match: exact, 8/8 compared fields**, parsed from the raw `ghidra.log`,
  independent of `compare.json` [OBSERVATION]. Route `info` at `1.25.0`; no Go analysis
  failure, no `Invalid index`, no EOF read, no fallback, no bootstrap miss, no
  `Untested Go version`.
- **Frozen mechanism rule for this label (non-D, predicted silent): holds** — the log shows
  no `Go analysis failure` [OBSERVATION]. The cohort D/non-D direction also holds on raw
  logs: only `t1250-vet` fails, with `Invalid index: 13902080`, which is in the frozen
  H1-only set; the other seven labels have no failure [OBSERVATION].
- **But two rule-level caveats, both affecting calibration:**
  1. The exact full H1 read-list prediction for `vet` is **falsified**: frozen
     `[13902080, 852107777, 1801722468838924630]`, observed `[13902080]`; `compare.exit=1`.
     The frozen `confirmed` text requires only one H1-only index and no outside index, so the
     mechanism verdict survives while the stronger per-carrier list does not.
  2. The rule's **binding gate is red at the delivered revision** because
     `receipt-validate.py` was rewritten after the freeze (`70672eb3…` → `9276b198…` →
     `6afb7ef6…` as the tip advanced). The retained freeze-time validation is green. Under
     the literal rule text, zero labels are "bound" at the tip; at `a1140e7` all eight are.
     The integrated `verify.py` anticipates this red (expected exit 1 + drift-only findings),
     but `predictions/decision-rule.json` does not say so.

## 1. Binding of the raw log to the frozen prediction

```
$ sha256sum runs/t1250-asm/logs/rea-ghidra-cWUKB0/ghidra.log
c350a577d36682ca7099585481bf246344317a178abfe3349fbf4dfc3f723795; exit=0
$ wc -lc runs/t1250-asm/logs/rea-ghidra-cWUKB0/ghidra.log
227 38277; exit=0
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/asm
a7ed400a04009488ea819eb06aeb912dc3537125cceef036743641060fd797f4; exit=0
$ md5sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/asm
fc86c84363c196ce128a715ae60fc215; exit=0
$ sha256sum predictions/t1250-asm.prediction.json
ae0c3cad056061a2daf1f9f98df6a43149e947599116f13b781f60075484ce4b; exit=0
$ git hash-object predictions/t1250-asm.prediction.json
5ee2a2ce1d45b1a476187fbd094c2fb803bc6ef9; exit=0
$ git rev-parse a1140e7:.ufo/waves/round-19/predictions/t1250-asm.prediction.json
5ee2a2ce1d45b1a476187fbd094c2fb803bc6ef9; exit=0
$ git rev-parse refs/heads/main:.ufo/waves/round-19/predictions/t1250-asm.prediction.json
5ee2a2ce1d45b1a476187fbd094c2fb803bc6ef9; exit=0
$ sha256sum -c predictions/SHA256SUMS   # run in W19
predictions/t1250-asm.prediction.json: OK  (all 19 rows OK); exit=0
```

[OBSERVATION] Chain, all links exact:

1. Carrier sha256 `a7ed400a…` equals `predictions/t1250-asm.prediction.json` `carrier.sha256`
   and `receipt.json.carrier.sha256_pre == sha256_post`; carrier md5
   `fc86c843…` equals `log:59` `?MD5=fc86c84363c196ce128a715ae60fc215` and
   `receipt.carrier.md5_pre`.
2. Log imports `target-a7ed400a0400.bin` (`log:46`, `log:163`), the first 12 hex of the
   prediction sha; `receipt.retained_logs[0].binding` is
   `{logfile_ok: true, md5_ok: true, target_ok: true}`; retained-log bytes `38277` and
   sha256 `c350a577…` equal `observation.json.log_bytes/log_sha256` and the receipt's copy.
3. The prediction file is itself a run pin: `receipt.pins_pre.entries[…t1250-asm.prediction.json]`
   = `{sha256: ae0c3cad…, size: 3101}`, identical in `pins_post`; `pins_compare.equal=true`
   with `changed=[]`. The three mid-run pin maps (`pins/mid-1..3.json`, 152 entries each)
   were taken at 19:00:33.97Z, 19:01:04.05Z, 19:01:34.13Z and are all `equal`.
4. `bound_sessions=['/tmp/kr17-rea-9r0uuou2/rea-ghidra-cWUKB0']`, `unbound_sessions=[]`;
   `session_parent` matches; no leftovers. The log's line 2 records the same `/tmp` log path
   that `observation.log_file_line` names.
5. Freeze precedes the run: commit `a1140e7` at 15:57:44-03, `producer.json.recorded_at_utc`
   `19:00:33Z` (=16:00:33-03), `runs/run-log.txt:6-7` `t1250-asm start 16:00:33 / end
   16:01:36`, analyze exit 0. `carrier-run.exit=0`, `observation.exit=0`, `compare.exit=0`.
6. Prediction and rule blobs are unchanged from the freeze through the newest observed tip:
   `a1140e7` and `refs/heads/main` both resolve `t1250-asm.prediction.json` to
   `5ee2a2ce…`, `swiss-misread/t1250-asm.json` to `809432fa…`, `decision-rule.json` to
   `09899450…`; `git log -- predictions/` lists only `a1140e7`.

## 2. The four assigned signals in the raw log

[OBSERVATION] All greps target
`runs/t1250-asm/logs/rea-ghidra-cWUKB0/ghidra.log`; `grep -c` exits 1 when the count is 0.

| Signal | Frozen prediction (file:line) | Raw log | Command / exit |
|---|---|---|---|
| Go analysis failure | `c3.h1_kind=none`; `h0/h1_map_path_failure=false`; `extra.analyzer_errors_empty=true` (`t1250-asm.prediction.json:20,25-26,44`) | absent; **zero** `ERROR` lines; `REPORT: Analysis succeeded` at `:221` | `grep -c 'Go analysis failure'` → `0`, exit 1; `grep -c 'ERROR'` → `0`, exit 1; `grep -in 'failure'` → no line, exit 1; `grep -in 'exception'` → no line, exit 1 |
| Invalid index | `extra.invalid_index_reads=[]`; `c3.h0_reads_including_walk.invalid_index=[]` (`:46`) | absent | `grep -c 'Invalid index'` → `0`, exit 1 |
| EOF read | `extra.eof_reads=[]`; `c3.h0_reads_including_walk.eof=[]` (`:45`) | absent; no `EOF`, no `EOFException` | `grep -c 'Unable to read past EOF'` → `0`, exit 1; `grep -c 'EOF'` → `0`, exit 1 |
| GoApiSnapshot route | `expected.snapshot_route=info`; `snapshot_label=1.25.0`; `fallback_to=null`; `missing_bootstrap=false`; `untested_version=null` (`:37-41`) | `:168 INFO (GoApiSnapshot) Using Go API snapshot for 1.25.0`; `:169 INFO (GoRttiMapper) Using Go API snapshot for version 1.25.0`; no fallback/untested/bootstrap text | `grep -c 'Using Go API snapshot'` → `2`, exit 0; `grep -c 'Falling back'` → `0`, exit 1; `grep -c 'Untested'` → `0`, exit 1; `grep -c 'bootstrap'` → `0`, exit 1 |

Parse trap [OBSERVATION]: `grep -n 'invalid'` **does** hit `ghidra.log:60`,
`Skipping section [.gosymtab] with invalid size 0x0` (import "Additional info", exit 0). Only
the exact token `Invalid index` (the `EOFException` formatter at
`Base-src.zip:ghidra/app/util/bin/MemoryByteProvider.java:302`) is the H1 signal. The lower
case `invalid size` is a loader note, not an analyzer read.

Source grounding for the route [OBSERVATION, from `Base-src.zip`]:
`ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:148-166` logs
`Using Go API snapshot for %s` (INFO) only when no patch-diff fallback occurs, and
`Falling back from %s to %s for Go API snapshot` (WARN) otherwise. A missing base file returns
`GoApiSnapshot.EMPTY` with no INFO line. The observed INFO therefore means the `go1.25.0.json`
base snapshot was selected, not a fallback; its pinned sha256
`54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` (`receipt.pins_pre`,
10081618 B) equals `prediction.selection.base.sha256/size`.

Independent reproduction [OBSERVATION]: the run-pinned extractor bytes are unchanged from the
producer pin (`sha256sum round-17/tools/log-extract.py` = `eb8f2c78…`, equal to
`receipt.pins_pre`). Running it on the bound log returned exit 0, and every extracted key —
`analyzer_errors`, `symbol_analysis_failures`, `mapper_errors`, `invalid_index_reads`,
`eof_reads`, `snapshot_route`, `snapshot_labels`, `snapshot_fallbacks`, `missing_bootstrap`,
`untested_versions`, `go_version_logged`, `api_snapshot_info_labels`, `bootstrap_attempts`,
`classification`, `go_lines` — equals `observation.json` byte-for-value:
`python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log <L> > /tmp/asm-extract.json` →
exit 0; key-by-key comparison printed `SAME` for all 17 checked keys.
`compare.py` (sha256 `582a77f3…`, equal to its producer pin) is likewise unchanged; re-running it on
the frozen prediction + observation reproduced `compare.json`'s `all_match=true` and all eight
field records exactly (exit 0). Cross-check only: the verdict here rests on the raw log.

## 3. Exact match computation

| Field (prediction path) | Predicted | Observed from raw log | Match / strength |
|---|---|---|---|
| `expected.snapshot_label` | `1.25.0` | `:168`, `:169` | yes (rule: contains-or-both-empty; **non-discriminating — request echo**) |
| `expected.snapshot_route` | `info` | `:168 INFO (GoApiSnapshot)`; no WARN/fallback | yes (**discriminating**) |
| `expected.fallback_to` | `null` | `snapshot_fallbacks=[]` | yes (both-empty rule; non-discriminating when empty) |
| `expected.missing_bootstrap` | `false` | no bootstrap text; `bootstrap_attempts=1` (the `Reading Go binary info` line, `:167`) | yes (equality) |
| `expected.untested_version` | `null` | no `Untested Go version` | yes (both-empty rule; non-discriminating when empty) |
| `extra.analyzer_errors_empty` | `true` | `analyzer_errors=[]` (zero ERROR lines) | yes (boolean vs empty list) |
| `extra.eof_reads` | `[]` | `eof_reads=[]` | yes (exact list) |
| `extra.invalid_index_reads` | `[]` | `invalid_index_reads=[]` | yes (exact list) |

**8/8 exact under the frozen compare rules** [OBSERVATION]. Five fields carry discriminating
content (route, bootstrap, and the three extras); three are empty/echo matches. The
emptiness is the point: this label is a negative control, not positive evidence for H1.

## 4. Frozen mechanism rule: asm, cohort, and the binding clause

Rule text (`predictions/decision-rule.json:3,5,20-21`): `confirmed` needs every D label's bound
log to show a Go analysis failure whose Invalid index values include at least one H1-only value
and no index outside the frozen H1 list, **and** every non-D label to show no Go analysis
failure; `binding_gate` needs `receipt-validate.py --require-mid-maps` to exit 0, the carrier
sha to equal the prediction's, and the prediction blob to be unchanged from the freeze.

- **asm (non-D): mechanism clause holds** [OBSERVATION]. No `Go analysis failure`, no
  Invalid index, no EOF read; route info. asm's emulator H1 and H0 kinds are both `none`
  (`evidence/prescan/kr19-sm-asm.json`), so silence is the predicted outcome under either
  hypothesis. It cannot discriminate H1 from H0.
- **Cohort direction on raw logs: holds** [OBSERVATION].

```
$ for l in go gofmt asm cgo compile cover preprofile; do f=$(ls runs/t1250-$l/logs/*/ghidra.log); \
    printf '%s ' "$l"; grep -c -F 'Go analysis failure' "$f"; done
go 0 / gofmt 0 / asm 0 / cgo 0 / compile 0 / cover 0 / preprofile 0   (grep exit=1 each)
$ f=$(ls runs/t1250-vet/logs/*/ghidra.log); grep -c -F 'Go analysis failure' "$f"
1; exit=0
$ grep -n 'Go analysis failure' runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log
186:2026-10-20 16:06:20 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: ...
$ grep -n 'Invalid index' runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log
229:Caused by: java.io.EOFException: Invalid index: 13902080
$ V=$(ls runs/t1250-vet/logs/*/ghidra.log)
$ for p in '13902080' '852107777' '1801722468838924630' 'Unable to read past EOF'; do \
    printf '%s=' "$p"; grep -c -F "$p" "$V"; done
13902080=1 / 852107777=0 / 1801722468838924630=0 / Unable to read past EOF=0 (exit=1 for the zeros)
```

  Vet's only observed index is `13902080`, inside
  `h1_only_invalid_indexes.t1250-vet=[13902080, 852107777]`; no index outside the frozen H1
  list appears. Under the frozen `confirmed` predicate, that plus seven silent controls
  yields **confirmed** [OBSERVATION for the log facts; the verdict is the rule's own
  mechanical consequence].
- **Full-list prediction is falsified** [OBSERVATION]. Vet's frozen H1 list has three
  indexes; the log shows one. `runs/t1250-vet/compare.exit=1`; the only mismatched compare
  field is `extra.invalid_index_reads`. This is the "mechanism confirmed, exact list not"
  split the round-19 knowledge note records; it must not be reported as 8/8.
- **Binding clause: red at the delivered tip, green only at the freeze bytes**
  [OBSERVATION]. Retained freeze-time validation
  `evidence/receipt-validation/t1250-asm.json` = `{"counts": {"invalid": 0, "receipts": 1,
  "unreadable": 0, "valid": 1}, "exit": 0, "require_mid_maps": true}` with
  `checks_performed: 372`. The receipt pins the validator at
  `70672eb3…`/46047 B in **both** `pins_pre` and `pins_post`. The tool bytes changed after the
  freeze, twice:

```
$ for r in a1140e7 4f6c73f d0690fd 279e8b1; do printf '%s ' $r; \
    git --no-optional-locks show $r:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum; done
a1140e7 70672eb3…; 4f6c73f 9276b198…; d0690fd 9276b198…; 279e8b1 6afb7ef6…   (exit=0)
$ for r in a1140e7 4f6c73f d0690fd 279e8b1; do printf '%s ' $r; \
    git --no-optional-locks cat-file -s $r:.ufo/waves/round-17/tools/receipt-validate.py; done
a1140e7 46047; 4f6c73f 51075; d0690fd 51075; 279e8b1 52682                   (exit=0)
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-asm/receipt.json; echo $?
# excerpted from the JSON
{"counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "exit": 1,
 "pins_path": ".../.ufo/waves/round-17/tools/pins.py",
 "receipts": [{"checks_performed": 372, "status": "invalid", "valid": false,
   "findings": [
     {"code": "sha256_mismatch", "path": ".../round-17/tools/receipt-validate.py",
      "expected_sha256": "70672eb3…", "actual_sha256": "6afb7ef6…",
      "where": "pins_post.entries.…/receipt-validate.py"},
     {"code": "size_mismatch", "path": ".../round-17/tools/receipt-validate.py",
      "expected_bytes": 46047, "actual_bytes": 52682, "where": "pins_post.entries.…"}]}]}
exit=1
```

  Carrier, log, mid-map and prediction checks pass; the only findings are the two
  validator-bytes codes. The integrated verifier at the tip already encodes this expectation:
  `verify.py:110` maps `receipt-validate-` to expected exit 1; `verify.py:569-575` runs the
  live validator with `--require-mid-maps` expecting 1; `verify.py:669-683` constrains the red
  to exactly `{sha256_mismatch, size_mismatch}` on that one path and requires the retained
  `receipt-source-bound-valid-<label>` green. The frozen `decision-rule.json` contains no such
  exception, so under its literal text asm is **not bound at the delivered revision** and
  **is bound at `a1140e7`**. C3's `0 -> 8` is therefore true at the freeze revision and 0 at
  the tip under the literal gate; the L1 must amend the rule or state the frozen-revision
  reading [INFERENCE on intent; OBSERVATION on the code paths and exits].

**Answer to "does the frozen mechanism rule hold":** for asm's non-D clause, yes; for the
cohort direction, yes on raw logs (vet H1-only index + seven silent); for the rule's binding
clause, only at the freeze revision — at the observed delivered tips it is red on validator
bytes alone.

## 5. Depth: what "silent" does and does not mean

[OBSERVATION] The asm log has exactly four `WARN` lines and no `ERROR`:

```
173 WARN (GoTypeManager) Failed to get subtype '[46912496118442]runtime.elfSym' in *[46912496118442]runtime.elfSym
174 WARN (GoTypeManager) Failed to get subtype '[1125899906842623]byte' in *[1125899906842623]byte
175 WARN (GoTypeManager) Failed to get subtype '[562949953421311]uint16' in *[562949953421311]uint16
176 WARN (GoTypeManager) Failed to get subtype 'time.Timer' in *time.Timer
187 INFO (GoRttiMapper) Go missing type names: 8
```

- These are not Go analysis failures. The frozen predicate is the literal `Go analysis failure`
  `Msg.error` text emitted by `GolangSymbolAnalyzer.java:182` and
  `GolangStringAnalyzer.java:125` in `Base-src.zip`; the extractor counts only
  `level == ERROR and component.startswith("Golang")`
  (`round-17/tools/log-extract.py:113-115,244`). "Silent" therefore means *no ERROR-level
  symbol-analyzer failure*, not *no Go diagnostic* [OBSERVATION + definitional reading].
- The same three subtype strings appear in **7/7 non-D labels** (`go`, `gofmt`, `asm`, `cgo`,
  `compile`, `cover`, `preprofile`) with a fourth `time.Timer`/`time.Ticker` warning in four;
  **vet has 0** WARNs, consistent with its failure aborting the same `GoTypeManager.markupGoTypes`
  phase before the warnings are reached (INFERENCE from vet's stack). Their identity across
  carriers with very different map counts (asm 1 misread, compile 15) argues against an
  asm-specific map cause; the cause is unresolved and no frozen field binds it
  [OBSERVATION + INFERENCE].
- Unlike `t1250-compile`, asm has **no** `ERROR (AnalysisTaskWrapper)` / `NullPointer`
  line (both greps exit 1), so asm's silence is not hiding a Go-task error outside the
  extractor's scope. This is a real difference between the two labels, not an assumption.
- The predicted mechanism state for asm — `misread_map_types: 1`, `true_kind: "swiss"`,
  `uncommon_map_types: 1` (`t1250-asm.prediction.json:28-30`) — is **not observable** in a
  provider log. It is a structural claim from the emulator over the carrier bytes. The
  emulator's `per_type` entry is the uncommon map
  `*go.shape.map[string]cmd/internal/objabi.PkgSpecial` (addr 6490944, slot 24, `uncommon:
  true`): H0 puts its uncommon data at 6491056 with `pkg_path 9430`; H1 at 6491032 with
  `pkg_path 24`; **both outcomes are `silent`, detail/eof null**
  (`evidence/prescan/kr19-sm-asm.json`). The emulator's walk also fails under both
  hypotheses at index 20 / type 6395840, `unmapped at 0x14` — a non-discriminating
  structural miss, not an analyzer `Invalid index` and deliberately outside the D rule
  (`w1/H0H1Semantics.md`). The log's silence is exactly what this predicts; it neither
  confirms nor refutes the misread count [OBSERVATION for prescan values; INFERENCE for the
  descriptor-to-log non-link].
- The compare never checks the `c3` block: `compare.json` fields are the five `expected`
  items plus the three `extra_expectations` items only. asm's `8/8` therefore does not test
  `misread_map_types`; the mechanism test lives in the D/non-D rule and vet's failure.
- Emulator determinism/freshness: prescan `evidence/prescan/kr19-sm-asm.json`
  (sha256 `f63d97a5…`, 20142 B) and frozen
  `predictions/swiss-misread/t1250-asm.json` (sha256 `8fd17eab…`, 20141 B) are **semantically
  identical** (canonical JSON sha256 both `7676d14f…`); the byte difference is one missing
  trailing newline in the frozen copy. The prediction's `c3` block reproduces the prescan
  values field-for-field (12/12 checks), and the frozen emulator digest `14924bd6…` equals
  `receipt.pins_pre[swiss-misread.py]` and the current file [OBSERVATION].
- Retention bound: `receipt.log_capture_limit` warns that lines written after the final poll
  can be missing. The final copy was at 19:01:35.627Z, 0.5 s before the step end
  (19:01:36.128Z); the last line (`:227`) is
  `ANALYZING changes made by post scripts`, i.e. the retained bytes include the whole Go
  phase through `Analysis succeeded` (`:221`). The four signals are inside the retained
  prefix; "no failure after post scripts" is not asserted [OBSERVATION + bounded INFERENCE].

## 6. Remaining unknowns

1. Cause of the cohort-wide `Failed to get subtype` WARNs and of `Go missing type names: 8`
   for asm. No frozen field or emulator table binds them; this seat did not decode carrier
   RTTI (no REA/execution lane). The three bit-pattern lengths are all-ones-ish
   (`0x2aaaaaaaaaaa`, `0x3ffffffffffff`, `0x1ffffffffffff`) and consistent with misread
   length fields, but that is unproven and not used by the match.
2. Whether the one misread map type is among the eight missing type names. The emulator
   names the descriptor, the log does not enumerate missing names; linking them requires
   decoding the carrier, which this lane forbids.
3. Up to 0.5 s of post-script lines may be absent from every retained log
   (`receipt.json.log_capture_limit`); the four assigned signals are unaffected.
4. The lane tip moved during the audit (`d0690fd` → `279e8b19`, 16:21:51-03) and may move
   again. The C3 predictions and run evidence did not change, but the validator bytes did;
   the literal binding-gate status depends on the final delivered revision or an append-only
   rule amendment.
