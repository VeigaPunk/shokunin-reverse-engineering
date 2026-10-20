# C3 outcome — t1250-compile (official go1.25.0 `cmd/compile`)

Seat: `KaidokuR19.OutcomeCompile-3`. Read-only scout; no clone, no mutation, no REA
`analyze`/`search`/`decompile`, no Ghidra invocation, no carrier execution.

## Binding facts (observation)

| item | value |
|---|---|
| carrier | `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile`, 21,518,237 bytes |
| carrier sha256 | `20dbac54f9f897582aedafea7207976f0300cfd4992429814d00bccbea7a4083` — equals `predictions/t1250-compile.prediction.json` `carrier.sha256`; `receipt.json` `carrier.sha256_pre` = `sha256_post` (no run drift) |
| bound log | `runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log`, 77,180 bytes, 432 lines |
| log sha256 | `fcad067469e3470db9a03536983c2243434ba6e2fdcca4fe606616a50f6ea7f0` — equals `receipt.json:retained_logs[0].files.ghidra.log.sha256`, and equals `git show refs/heads/main:…/ghidra.log \| sha256sum` |
| frozen prediction | sha256 `651d6b125ddbbaa6a67b7da274ee525eb56c24a9f16a4d8858dae3c229f64f7f`; identical at freeze commit `a1140e7` and now |
| chronology | prediction authored 2026-10-20 15:37:18, committed 15:57:44 (`a1140e7`); run producer `branch_tip=a1140e7` at 16:02:16 -03; analyze log starts 16:02:19 — **prediction precedes analyze** |
| receipt evidence | `evidence/receipt-validation/t1250-compile.json`: exit 0, valid 1/1, 390 checks, `require_mid_maps: true`. Binding re-verification is another seat's; cited, not re-owned. (Tool digest drift for `receipt-validate.py` is the wave-2 binding item, out of scope here.) |

Emulator identity in the prediction: `round-18/tools/swiss-misread.py` sha256
`14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`; measured file sha matches
(exit 0). Prescan `evidence/prescan/kr19-sm-compile.json`: `predicted_failure_h1=false`,
`predicted_failure_h0=false`, kinds `none`/`none`, `misread_map_types=15`,
`uncommon_map_types=15`, `diagnostic=false` — matches the frozen `c3` block.

## Raw-log observations (from `ghidra.log`, not `compare.json`)

| line | level/component | text (exact) | significance |
|---|---|---|---|
| 333 | `INFO (GoApiSnapshot)` | `Using Go API snapshot for 1.25.0` | discriminating selection-route line (`GoApiSnapshot.java:158-163`); INFO = exact/patch-0, no fallback |
| 334 | `INFO (GoRttiMapper)` | `Using Go API snapshot for version 1.25.0` | requested-version echo only (`log-extract.py:98-103`) |
| 337 | `INFO (GolangSymbolAnalyzer)` | `Go version 1.25.0` | build-info version parsed without truncation |
| 338-340 | `WARN (GoTypeManager)` | `Failed to get subtype '[…]runtime.elfSym' / '[…]byte' / '[…]uint16'` | not compile-specific: the same WARN appears in 27 of the 39 retained round-17/18/19 `ghidra.log`s (26 besides this one); WARN level |
| **347** | **`ERROR (AnalysisTaskWrapper)`** | **`Analysis Task: Golang RTTI Propagation (deferred) - element cannot be mapped to a null key java.lang.NullPointerException: element cannot be mapped to a null key`** | **the only timestamp-led ERROR record in the log; a Go analysis task failed** |
| 410 | timing summary | `Golang RTTI Propagation (deferred)   0.020 secs` | task ran and aborted after 0.020 s |
| 426 | `INFO (HeadlessAnalyzer)` | `REPORT: Analysis succeeded for file: file:///tmp/kr17-rea-9nv8amxo/rea-ghidra-uEQQSP/target-20dbac54f9f8.bin` | task failure was non-fatal; the rest of auto-analysis completed |

Absent, with exit-1 greps: `Go analysis failure`, `Invalid index`, `Unable to read past EOF`,
`EOFException`, `Untested Go version`, `Falling back from`, `Missing Go bootstrap type info`.
There is no `Invalid index` read and no EOF read anywhere in this log, and no `Go analysis
failure` record. The only case-insensitive `invalid` hit is `:59 Skipping section [.gosymtab]
with invalid size 0x0` (loader message, not a Go read failure).

Corpus census of timestamp-led ERROR records (all retained round-17/18/19 logs, exit 0):
round-19 carriers → `t1250-compile` 1 (`AnalysisTaskWrapper`), `t1250-vet` 1
(`GolangSymbolAnalyzer`), the other six 0. Round-18/17 logs never contain an
`ERROR (AnalysisTaskWrapper)` record; their `AnalysisTaskWrapper` hits are stack-trace
continuation frames inside `GolangSymbolAnalyzer` traces. **The wrapper-attributed Go task
failure is unique to this carrier in the retained corpus.**

## Prediction comparison

Eight fields are actually compared by `compare.py` for this label. Raw-log verdicts:

| # | field | predicted | observed in raw log | verdict |
|---|---|---|---|---|
| 1 | `untested_version` | `null` | no `Untested Go version` line (grep exit 1) | MATCH |
| 2 | `snapshot_label` | `1.25.0` | `:333` GoApiSnapshot label `1.25.0` | MATCH |
| 3 | `missing_bootstrap` | `false` | no bootstrap-missing line (grep exit 1) | MATCH |
| 4 | `snapshot_route` | `info` | `:333` INFO, no WARN fallback | MATCH |
| 5 | `fallback_to` | `null` | no `Falling back from` line (grep exit 1) | MATCH |
| 6 | `extra.analyzer_errors_empty` | `true` | **one Go analysis-task ERROR at `:347`** | **MISMATCH (raw log)** |
| 7 | `extra.eof_reads` | `[]` | no EOF pair (grep exit 1) | MATCH |
| 8 | `extra.invalid_index_reads` | `[]` | no `Invalid index` (grep exit 1) | MATCH |

C3-side frozen fields that are not compare fields:

- `h1_kind: none`, `h1_map_path_failure: false`, `h0_map_path_failure: false` — **consistent**
  with the log: no map-path read failure of any kind appears.
- `diagnostic_r19: false`, `emulator_diagnostic_field: false` — emulator-side; not observable
  in a log.
- `misread_map_types: 15`, `uncommon_map_types: 15`, `true_kind: swiss` — emulator-side type
  predictions; a Ghidra log cannot confirm or refute per-type layout, and none of the log's
  type counts (`:335 161 unindexed`, `:336 5851 found`, `:392 26 missing names`) is a
  map-layout oracle.

**Net: 7 of 8 compare-visible fields match the raw log; `analyzer_errors_empty` does not.**

`compare.json` reports `all_match: true` with `compare.exit 0`. That is true only relative to
the extractor's definition; see below.

## Why `compare` cannot see it (depth, source-anchored)

- `log-extract.py:243`: `if level == "ERROR" and component.startswith("Golang")` → appends
  `analyzer_errors`. Line 347's component is `AnalysisTaskWrapper`, so it is dropped.
- `log-extract.py:214` with `:122-131`: the `go_lines` allowlist also rejects
  `AnalysisTaskWrapper`; `observation.json` `go_lines` jumps from line 346 to 389, so the
  record is absent from the retained observation entirely.
- `log-extract.py:115,198`: `symbol_analysis_failures` requires the literal
  `Go analysis failure`; the wrapper message does not contain it.
- `compare.py:201-206`: `extra.analyzer_errors_empty` is derived solely from
  `observation.analyzer_errors`, hence `observed: []`, `match: true`, exit 0 (reproduced).
- `gen-predictions.py:71-72`: the frozen field was set to `true` mechanically because
  `h1_kind == "none"`. The field therefore encodes the implication *"no map-path failure ⇒
  no analyzer errors"*; compile falsifies that implication while leaving the map-path
  prediction intact.
- REA's own `analyze.json` `normalized_result` exposes only
  `document, image_base, segments, segment_count, procedure_count, string_count` — no
  analyzer-error surface. The failure exists only in the raw log.

## Mechanism of the observed failure (inference, grounded in source)

- `GolangSymbolAnalyzer.java:1207-1208` builds `CallSiteInfo` with
  `funcMgr.getFunctionContaining(ref.getFromAddress())` as `callingFunc`; that call returns
  `null` for a call reference whose from-address is not inside an analyzed function.
- `GolangSymbolAnalyzer.java:1181-1183` then does
  `.collect(groupingBy(csi -> csi.callingFunc))`. JDK `Collectors.groupingBy` rejects null
  keys with exactly `element cannot be mapped to a null key` (the logged NPE), aborting the
  whole deferred RTTI-propagation task before any callsite can be fixed up.
- This is a containment/navigation gap, not a map-layout read: no `Invalid index`, no EOF,
  and the failure occurs in the RTTI callsite grouping path, not the type-markup walk that
  produces `go1.24/1.25` Swiss-map `Invalid index` EOFs (`GolangSymbolAnalyzer.java:182`,
  which is the message vet emits). Alternative chain — an H1-corrupted RTTI function making
  a non-function call reference enter the stream — is possible in principle but has no
  evidence here and is not needed to explain the NPE; confidence: high for the direct source
  cause, low for any H1 linkage.
- Effect: RTTI propagation contributed nothing for this carrier (`:410`, 0.020 s) while the
  rest of analysis and the post-scripts ran normally (`:426`). This is a partial, non-fatal
  analyzer failure.

## Frozen mechanism rule — does it hold for this label?

Rule text: `predictions/decision-rule.json:5` (confirmed), `:28` (refuted), `:125`
(unresolved), and `:2` (verdict decided **from the bound log**). Compile is non-D:
`decision-rule.json` table row `t1250-compile d=false`, prescan `h1=false/h0=false`.

- **Literal reading.** The rule's failure predicate is the Ghidra message
  `Go analysis failure` (emitted at `GolangSymbolAnalyzer.java:182`; round-18's rule words the
  same predicate as "analyzer_errors contain 'Go analysis failure'"). Compile's log contains
  no such message (grep exit 1), so the "every non-D label shows no Go analysis failure"
  arm is satisfied. Under this reading the rule is not refuted, but it is also not a clean
  demonstration: the label is "silent" only because the rule names one diagnostic string.
- **Substantive reading.** Line 347 is a failed *Golang* analysis task
  (`Golang RTTI Propagation (deferred)`), so "a non-D label fails" (`:28`) is true and the
  cohort's confirmed claim is refuted for this label.
- **Coverage gap.** `:28` never defines "fails", and `:125` enumerates only route mismatch,
  unbound log and timeout — an abortive Go background analyzer with no `Invalid index`/EOF is
  in no clause. The rule cannot classify compile without an added definition.

**Verdict.** The frozen mechanism rule does **not** hold as a predictive success for
`t1250-compile`. The per-carrier prediction is falsified on `analyzer_errors_empty` by the
raw log (the compare's exit 0 is a tool-scope artifact), and the amendment's statement that
"the 7 non-D labels [are] silent" (`claims.json:40`; `contract.md:43-44`) is false for
compile in substance: silent in map-path reads, **not** silent in analyzer tasks. H1's
map-path mechanism is **not** refuted by this label — route `info`, snapshot `1.25.0`,
no `Invalid index`, no EOF — so the honest classification is *unresolved/anomaly* for this
label, not `confirmed` and not an H1 refutation. Any C3 verdict of "confirmed" must either
(a) state explicitly that "Go analysis failure" means only the exact
`GolangSymbolAnalyzer.java:182` message (and then disclose this unmodeled failure class), or
(b) treat compile as an unpredicted failure and drop the "7 silent" claim for this carrier;
the extractor also needs `AnalysisTaskWrapper`-attributed Golang tasks in
`analyzer_errors` before the compare can ever catch this class.

## Residual unknowns

1. **Determinism** — one retained run only; no second `t1250-compile` run exists
   (`runs/pass2/` contains only an in-progress `t1250-go` rerun at observation time
   16:22 -03). Whether line 347 recurs on a rerun is untested.
2. **Trigger site** — the specific reference/function that produced the null `callingFunc` is
   not in the log; recovering it would need an authorized rerun with program-state inspection
   (forbidden to this seat).
3. **Causal independence from Swiss misreading** — inference from code shape, not a
   controlled comparison; no evidence either way beyond the absence of map-path failures.
4. Other carriers' outcomes and the cohort aggregate are other seats' scope.

## Commands and exits

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-compile/logs/rea-ghidra-uEQQSP
sha256sum ghidra.log script.log                                  # exit 0 → fcad0674…, ebe7a5bb…
wc -l ghidra.log                                                 # exit 0 → 432
stat -c '%s %n' /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile  # exit 0 → 21518237
sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile        # exit 0 → 20dbac54…
grep -n "Go analysis failure" ghidra.log                         # exit 1 (absent)
grep -n "Invalid index" ghidra.log                               # exit 1 (absent)
grep -nE "Unable to read past EOF|EOFException" ghidra.log       # exit 1 (absent)
grep -n -i "invalid" ghidra.log                                  # exit 0 → :59 only (loader message)
grep -nE '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9:]{8} ERROR' ghidra.log  # exit 0 → :347 (1 record)
grep -n "Golang RTTI Propagation (deferred)" ghidra.log          # exit 0 → :347, :410
grep -nE "Using Go API snapshot|Falling back from|Untested Go version|Missing Go bootstrap" ghidra.log  # exit 0 → :333, :334
grep -n "Analysis succeeded\|Analysis failed" ghidra.log         # exit 0 → :426
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log .ufo/waves/round-19/runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log > /tmp/kr19-compile-obs.json   # exit 0 → analyzer_errors []
python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction .ufo/waves/round-19/predictions/t1250-compile.prediction.json --observation /tmp/kr19-compile-obs.json > /tmp/kr19-compile-cmp.json   # exit 0, all_match true
git --no-optional-locks show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-compile.prediction.json | sha256sum   # exit 0 → 651d6b12…
git --no-optional-locks show refs/heads/main:.ufo/waves/round-19/runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log | sha256sum   # exit 0 → fcad0674…
git --no-optional-locks log --format='%H ai=%ai ci=%ci %s' -- .ufo/waves/round-19/runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log   # exit 0 → 4f6c73f, ci 16:09:17
find .ufo/waves/round-17 .ufo/waves/round-18 .ufo/waves/round-19 -name ghidra.log -print0 | xargs -0 grep -c "Failed to get subtype"   # exit 0 (per-log census)
grep -rlE '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9:]{8} ERROR +\(AnalysisTaskWrapper\)' .ufo/waves/round-17 .ufo/waves/round-18   # exit 1 → 0 files
find .ufo/waves/round-17 .ufo/waves/round-18 .ufo/waves/round-19 -name ghidra.log -print0 | xargs -0 grep -l "Failed to get subtype" | wc -l   # exit 0 → 27 of 39
python3 -I (inline JSON scans: producer.json, receipt.json, observation.json, analyze.json, prescan)   # exit 0
unzip -o -q /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip 'ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java' 'ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java'   # exit 0
```
`refs/heads/main` observed at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (16:15:31 -03). No
installs, no upgrades, no working-tree writes in LANE other than this report; no mutation
tests were needed for an outcome seat.

No `lsp` device was exposed in this seat's tool set, so source tracing used `read`/`grep`
with exact file:line anchors; that unavailability is recorded rather than presenting grep
as semantic proof.

Report: .ufo/waves/round-19/w2/OutcomeCompile.md
