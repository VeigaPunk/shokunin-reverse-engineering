HOLDS

# W2 falsify: carrier run `s1250-noswiss-nomethods`, re-derived independently

Seat: KaidokuR18.Runs1250noswissnomethods (author-side advisory, leaf). This is a recommendation, not an admission.

- Revisions: REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, freeze F `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
- Abbreviations (relative to the lane):
  - `RUN=.ufo/waves/round-18/runs/s1250-noswiss-nomethods`
  - `LOG=$RUN/logs/rea-ghidra-9XZBsW/ghidra.log`
  - `PRED=.ufo/waves/round-18/predictions/s1250-noswiss-nomethods.prediction.json`
  - `CAR=/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-noswiss-nomethods`
  - `SRC=<ghidra_12.1.4_PUBLIC>/Ghidra/Features/Base/lib/Base-src.zip`
- Line anchors: every `$RUN` file at REV is byte-identical to disk. `git diff --stat REV -- $RUN` is empty and `git status --porcelain` is clean, so REV line numbers equal disk line numbers. `PRED` lines are cited at F; that blob is unchanged at REV.
- Scope: no REA analyze/search/decompile, no Ghidra, no carrier execution, no installs.

## Verdict per field
Observed = read from the raw REV log or bytes. Inferences are marked [INFERENCE].

| Field | Frozen (F:PRED line) | Re-derived from raw lines / bytes | Verdict |
|---|---|---|---|
| snapshot_route | `info` (:34) | Exactly 1 `(GoApiSnapshot)` record: `LOG:113` `INFO (GoApiSnapshot) Using Go API snapshot for 1.25.0`. No WARN GoApiSnapshot record, no `Falling back from`. Source: once a base JSON exists (`SRC:GoApiSnapshot.java:122-126`), patch 0 skips the loop at :153-156 and takes the INFO branch at :163. | HOLDS |
| snapshot_label | `1.25.0` (:33) | `LOG:113`, plus the GoRttiMapper echo at `LOG:114` (`GoRttiMapper.java:179-180`) | HOLDS (request echo; carries no information) |
| untested_version | null (:35) | 0 `Untested Go version` (would be ERROR, `GoRttiMapper.java:170-171`); 0 case-insensitive `untested` | HOLDS |
| fallback_to | null (:31) | 0 `Falling back from` (`GoApiSnapshot.java:159-160`) | HOLDS |
| missing_bootstrap | false (:32) | 0 `Missing Go bootstrap` (`GoRttiMapper.java:358-359`). `LOG:112` Reading Go binary info; `LOG:115-116` 9 unindexed / 799 types | HOLDS |
| `Go analysis failure` (analyzer_errors_empty) | true (:38) | 0 matches; 0 case-insensitive `analysis failure`; 0 ERROR from `Golang*` components. The success path is in the log: `LOG:5887-5892` correspond to `GolangSymbolAnalyzer.java:164-175`, inside the try block (:144-180) and before the analyzed flag is set at :178 | HOLDS |
| `Invalid index:` values | `[]` (:40) | 0 (also 0 case-insensitive; 0 `EOFException`, `IOException` or `Caused by` anywhere) | HOLDS |
| `Unable to read past EOF:` values | `[]` (:39) | 0 (also 0 case-insensitive `past eof`) | HOLDS |
| input / normalized / in_declared_range | `go1.25.0 X:noswissmap` / `1.25.0` / true (:43,:44,:42) | Buildinfo in the carrier bytes (offset 0x162000) is `go1.25.0 X:noswissmap`, with `GOEXPERIMENT=noswissmap`. `LOG:183` logs `Go version 1.25.0`; no Untested record | HOLDS |
| selection (base_only, go1.25.0.json) | sha `54d10162…6252`, 10081618 B, status base_only (:74) | `sha256sum`/`stat` of the snapshot JSON match, and it matches the `pins/mid-1.json` entry. No `patchverdiffs/go1.25.*` file is installed (glob lists go1.24.1-6 only) | HOLDS |
| c3 block | diagnostic false; h0/h1 none; true_kind old; misread 0; uncommon 0 (:16-24) | Frozen emulator re-run: all of these fields reproduce, 11 map types, all `uncommon:false`. Construction: `carriers/src/nomethods/main.go:1-2,12,21,23` (REV) has an unnamed `map[string]int` and free functions. `.symtab` has `main.main` and `main.str` and no methods (the sibling has `main.Counts.String` and `main.(*Counts).String`). The log binds to this source: `LOG:434` `main.go:23 @004998f6` is `func main()` and `LOG:5592` `main.go:21 @00499713` is `func str`. Both addresses fall inside the `.symtab` ranges of main.main (0x4998e0+394) and main.str (0x499700+475). 118 `map_noswiss.go` references and 0 `map_swiss` | HOLDS (not directly visible in the log; consistent) |
| session path | — | `LOG:2` `Using log file: /tmp/kr17-rea-5w8zvw01/rea-ghidra-9XZBsW/ghidra.log`. `LOG:40,43,45` put the project in the same dir. This equals `receipt.json:2-4` and `:1911`. `unbound_sessions` [] (:1989), leftovers [] (:1916). All 15 r18 runs use distinct `/tmp/kr17-rea-*` parents | HOLDS |
| target-\<sha12\> | — | `LOG:46,66,106,112,5931,5937` `target-e4e2f8ff8c47.bin` = sha256[:12]. It appears in no other r18 log | HOLDS |
| MD5 | — | `LOG:66` `?MD5=7aac4ef41bf8290cb2c429b3956dd91b` = `md5sum $CAR` = `receipt.json:6`; binding flags true (`receipt.json:1893-1895`) | HOLDS |
| carrier sha256 | `e4e2f8ff…0291` (:28) | Equal across all of: `sha256sum $CAR`; `receipt.json:8-9` (pre and post); `carriers/SHA256SUMS:9` (added at F, before the run); the analyze/inspect-go subject digests; and a full `go build -a` rebuild of the REV source with the `build.sh:21-24` recipe (`cmp` identical) | HOLDS |
| log integrity | — | REV blob sha256 `9a5bb6b9…bb74`, 993216 B, 5937 newline-terminated records. Equals disk, `observation.json:161` and `receipt.json:1901` | HOLDS |
| receipt-validate `--require-mid-maps` | exit 0 required (`decision-rule.json:2`) | exit 0: valid 1/1, 360 checks, `findings: []` | HOLDS |
| prediction blob frozen | — | sha256 `6014ae13…c70d` at F, at REV and on disk. `git log -- PRED` lists only F, and F is an ancestor of REV. The run started 16:27:51Z, after F was committed (13:23:55-03 = 16:23:55Z). `producer.json` branch_tip = F; pins_pre has the same sha | HOLDS |
| tool reproducibility | — | Rerunning `log-extract.py` on LOG gives canonical JSON (minus `log_path`) with sha `e9521cab…` = `observation.json`. Rerunning `compare.py` gives `1c5effb5…` = `compare.json` (minus paths), `all_match: true` | HOLDS |

Role [INFERENCE from `decision-rule.json:7,9,19`]:
- This label is a non-D synthetic control.
- Observing no failure satisfies the "no non-D synthetic label shows a failure" clause.
- It does not trigger "any noswiss synthetic label fails".
- It cannot move the H0/H1 mechanism verdict, because h0 = h1 = none by construction.

## Findings (none breaks this label)
**F1 · Low · emulator gap scan never fires. This corroborates `w2/Runs1246noswissnethttp.md` F1, here with exact flag semantics.**
- Observation:
  - The frozen emulator gives `walk.indexed_types` 790 and `unindexed_types` 0 for this carrier.
  - Ghidra logs `LOG:115` `Discovered 9 unindexed Go types` and `LOG:116` `Found 799`.
- Cause:
  - `REV:.ufo/waves/round-18/tools/swiss-misread.py:1236-1237` tests the raw GoName against `startswith("struct { ")`.
  - Ghidra first strips one `*` when ExtraStar is set (`SRC:GoBaseType.java:118`; `GoTypeFlag.java:30`, ExtraStar = 1<<1). Only then does it apply `isAnonType` (`GoSymbolName.java:237-238`).
- Counterfactual (in memory): inserting `if (tflag & 2) and name.startswith("*"): name = name[1:]` after :1236 gives these unindexed counts, each equal to Ghidra's logged count:

  | Carrier | unindexed |
  |---|---|
  | this label | 9 (total 799) |
  | s1250-noswiss-methods | 9 |
  | s1250-swiss-methods | 9 |
  | s1246-swiss-nethttp | 39 |
  | kimi | 195 |
  | aether | 188 |

- On all six carriers, `predicted_failure_kind_h0/h1`, `eof_reads_h1`, `invalid_index_reads_h1`, `misread_map_types`, `uncommon_map_types` and `diagnostic` are unchanged.
- Consequence: the docstring claim at `swiss-misread.py:17-18` ("the unindexed-closure gap scan") overstates fidelity. No verdict changes.

**F2 · Low · the single "mid-run" map is a step-start snapshot. This corroborates `w2/MidMapsRetained.md` F2.**
- Timing:
  - The analyze step started at 16:27:51.638126Z (`receipt.json:1963`) and ended at 16:28:12.228891Z (`:1929`).
  - mid-1 was taken at 16:27:51.683282Z (`:1940`), +45 ms.
  - That is before `LOG:1` (13:27:52-03:00) and at least 3.3 s before the snapshot read at `LOG:113` (13:27:55-03:00).
- Cause: `carrier-run.py:39` sets `PIN_CHECK_S = 30.0`, longer than the 20.59 s step, and `:484` fires the check on the first poll.
- Consequence: the only guard over the Ghidra window is the equality of the pre and post pin maps (`receipt.json:346-352`). The `--require-mid-maps` pass proves a map was retained, not that pins were checked during the read. No verdict changes.

**F3 · Info · `analyzer_errors_empty` is narrower than its name.**
- It is true only under `log-extract.py:243` (ERROR level and component starts with `Golang`).
- The log also contains 5700 `ERROR (GoFuncData)` "Failed to add source file mapping" records, 5 `ERROR (DWARFDataTypeImporter)` records and 3 `WARN (GoTypeManager)` records (`LOG:455-457`).
- Do not paraphrase this field as "no Go errors".

## Residual risk / verification gaps
- Log tail:
  - `LOG:5937` (`ANALYZING changes made by post scripts`) is the last line of all 15 r18 logs. The last copy was at 16:28:11.727Z (`receipt.json:1909`) and the step ended at 16:28:12.229Z; the receipt warns about tail loss at `receipt.json:24`.
  - [INFERENCE] The tail cannot hide a symbol-analysis failure. Re-analysis skips once the analyzed flag is set (`GolangSymbolAnalyzer.java:119-121,178`), and `LOG:5892` shows the try block ran past markup.
  - Reads by other components in the lost tail cannot be observed.
- Outside this label: even with the F1 fix, the emulator's type totals on the two real carriers stay below Ghidra: kimi 5700 vs 5707 (−7), aether 6112 vs 6115 (−3). The four synthetic carriers I tested match exactly (799/801/808/1713). I did not investigate the cause; predicted outcomes did not change.
- Ghidra markup of individual types was not observed (forbidden). The c3 counts rest on the emulator, the log counts and `.symtab`.
- The rebuild trusted `~/.local/opt/go-1.25.0` as installed (`go version go1.25.0 linux/amd64`). I did not re-verify the tarball hash that `build.sh:3-4` claims.
- The log binds the carrier only by sha12 + MD5. The full sha256 binding goes through the receipt's pre/post hash of the same path, plus my independent re-hash and rebuild.

## Commands (exit codes)
```text
git -C <lane> show F:PRED                                                    # 0 (frozen JSON above)
git -C <lane> log -1 --format='%H %cI %s' REV; ... F; git merge-base --is-ancestor F REV   # 0; ANCESTOR_EXIT=0
git -C <lane> diff --stat F REV -- PRED                                      # 0, empty
for c in F REV; do git show $c:PRED | sha256sum; done; sha256sum PRED; git log -- PRED   # 0; 6014ae13… ×3; only F
git -C <lane> ls-tree -r --long REV -- $RUN/; git status --porcelain -- $RUN …; git diff --stat REV -- $RUN …   # 0; 16 files; clean; empty
git show REV:$LOG | python3 -I -B -c '<regex sweep: (GoApiSnapshot)|Go analysis failure|Invalid index:|Unable to read past EOF:|Falling back from|Untested Go version|Missing Go bootstrap|binding lines>'
    # EXIT=0 0 → sha256 9a5bb6b9…, records 5937, final_nl True; route 113 INFO only;
    # counts {route:1, failure:0, invidx:0, eof:0, fallback:0, untested:0, bootstrap:0, bind:3 (LOG:2,46,66)}
sha256sum $CAR; md5sum $CAR; stat -c %s $CAR                                 # 0; e4e2f8ff…0291; 7aac4ef4…d91b; 2247294
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $RUN/receipt.json   # EXIT=0; valid 1, invalid 0, checks 360, findings []
python3 -I -B round-17/tools/log-extract.py --log $LOG | jq -S 'del(.log_path)' | sha256sum   # 0 0 0; e9521cab… == stored
python3 -I -B round-17/tools/compare.py --prediction PRED --observation $RUN/observation.json | jq -S 'del(.prediction,.observation)' | sha256sum   # 0 0 0; 1c5effb5… == stored
python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier $CAR --golang-root <ghidra>/…/typeinfo/golang   # EXIT=0; c3 fields == PRED:16-24; walk 790/0
tmp=$(mktemp -d); git clone -q --no-hardlinks --no-checkout <lane> $tmp/lane; git -C $tmp/lane remote remove origin   # remotes=0
  git -C $tmp/lane checkout -q REV -- .ufo/waves/round-18/carriers
  (cd …/carriers/src/nomethods; env -i HOME=$w/home PATH=/usr/bin:/bin GOTOOLCHAIN=local GOFLAGS= CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
     GOAMD64=v1 GOEXPERIMENT=noswissmap GOCACHE=$w/c GOPATH=$w/p GOENV=off ~/.local/opt/go-1.25.0/bin/go build -a -v -trimpath -buildvcs=false -o $w/out/… .)
  # BUILD_EXIT=0; 61 packages; sha256 e4e2f8ff…0291; cmp identical; rm -rf $tmp → CLEANED   ($w = $tmp/lane/.kr18w2, inside the clone)
git show REV:.ufo/waves/round-18/tools/swiss-misread.py | python3 -I -B -c '<exec in memory; optional insert after :1236:
    if (candidate[machine.header_offsets["TFlag"]] & 2) and name.startswith("*"): name = name[1:]>' <carrier> <golang-root> frozen|fix
    # EXIT=0 0 each; this label frozen 790/0 → fix 799/9; s1246-swiss-nethttp 1674/0 → 1713/39, inv_h1 [22386945] both
for r in runs/*/receipt.json; do jq -r '[label, analyze start/end, pin_checks count/instants]'; done   # EXIT=0; this run: 1 map at +45 ms
```
- Run in-process, read-only, so there are no shell exit codes:
  - Python `zipfile` reads of SRC members (GoApiSnapshot, GoRttiMapper, GolangSymbolAnalyzer, MemoryByteProvider, GoTypeManager, GoBaseType, GoSymbolName, GoTypeFlag).
  - Parsing of buildinfo and `.symtab` from carrier bytes.
  - Normalized diff of the nomethods and methods sibling logs: 41 diff lines, covering DWARF sizes, 799 vs 801 types, method-info 132 vs 134, and main.go:23/21 vs :26/:24.
  - A python3 `-I -B` subprocess for the counterfactual over 6 carriers.
- The read-only grep tool collected the cross-log `Discovered/Found` counts.

## Housekeeping
- Writes: this report, plus two mkdtemp clones (`/tmp/r18w2-s1250nn.C9CcJT` and `.EdwxE6`) with origin removed. Build HOME, GOCACHE and GOPATH were all inside each clone, and both clones were deleted.
- No jj and no git writes in the lane.
- No tools were installed or updated (git, jq, python3 and go1.25.0 were already present). pacman was not touched.
