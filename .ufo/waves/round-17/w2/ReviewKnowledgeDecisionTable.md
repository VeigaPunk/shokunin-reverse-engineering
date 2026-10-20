# ReviewKnowledgeDecisionTable — r17 knowledge entry: decision-table + INFERENCE attack

Seat: `KaidokuR17.ReviewKnowledgeDecisionTable` (wave 2, leaf, read-only).
Lane revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`; baseline `b563c799d97774aae4351276fe43cb897311e349`.
Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` — every row of the decision table (`:101-107`) and both INFERENCE blocks (`:111-120`), against the installed `Base-src.zip` members (`GoApiSnapshot.java`, `GoRttiMapper.java`, `GoBuildInfo.java`, `TransientProgramProperties.java`, plus `GolangSymbolAnalyzer.java` / `GolangStringAnalyzer.java` / `ElfLoader.java` where the row needs them), the retained runs, and the lane's own prior corpus.
Method: read-only. `unzip -p | nl -ba` on the archive; `read`/`grep`/`git`/`readelf`/`pacman -Qo`; Python `-I -B`; scratch under `/tmp/r17kd`. No REA analyze/search/decompile, no Ghidra, no carrier execution. No installs or updates. `[OBSERVED]` = command output; `[INFERENCE]` = my reasoning.

## Row / inference verdicts

| Target | Verdict |
|---|---|
| R1 `:102` GoApiSnapshot `Using … for X` | held (see no-finding N1) |
| R2 `:103` `Falling back …` | held (N2) |
| R3 `:104` GoRttiMapper `Using … for version X` | **F2** |
| R4 `:105` `Untested` + no snapshot + `Missing bootstrap` | held (N4) |
| R5 `:106` only `Reading Go binary info` + `unable to get` | held (N5) |
| R6 `:107` bootstrap OK then `Go analysis failure` | **F3** |
| INFERENCE 1 `:111-116` range/base confound | claim held; **F5** missing anchors |
| INFERENCE 2 `:117-120` historical `op` 2.40.0 | **F1** |

## Findings

### F1 — HIGH (calibration): INFERENCE 2 is contradicted by the lane's own recorded Go version for `op` 2.40.0

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:117-120`.

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ sed -n '19p;66,69p;108,118p' corpus/knowledge/2026-10-13-r4-10-real-version-pair.md
| `1password-cli` 2.34.1-1 → 2.40.0-2 | `usr/bin/op` | 41,210,040 → 43,475,106 | `d24dc5d4…` → `8d029d2c…` | ELF x86-64 static, stripped Go (**go1.25.7 → go1.26.8**) |
- `op-2.34.1` (`go1.25.7`): Go analyzer fully recovered pclntab names — 33,060
  procedures, ~32,933 carrying `namespace::pkg.name` symbols (`main::main.main`,
  `runtime::runtime.mstart0`, `_rt0_amd64_linux`, protobuf type stubs).
- `op-2.40.0` (`go1.26.8`): only 11,595 procedures recovered, 11,588 of them
  …
- source: run log rows 5–9, 16; `readelf -h` entry addresses; `go version` on both
  binaries (`go1.25.7` vs `go1.26`, `go1.26.8` strings); `s234-all.json` /
  `s240-all.json` inventories in `/tmp/rea-r4`.
```

The entry makes the class conditional on "**only if** that build was go1.26.x", then says the package "is no longer installed, so its cause stays UNKNOWN". The conditional is already satisfied by the lane's own r4-10 record (`go1.26.8`, obtained from `go version` and embedded strings), and r4-10 used the Ghidra 12.1.4 provider (`r4-10:8`). "Not installed now" bounds *reproduction of the session*, not the version question; the version is not unknown. The final sentence ("the current `op` 2.41.0-1 is a different binary") is true but does not bear on the class: the historical build is also `go1.26.8`. Whether that session actually took the missing-base branch remains unobserved because its log is gone (`r14:83-90`) — a different question from the version conditional the entry leaves open.

Smallest fix — replace `:117-120` with one sentence:
> The 2.40.0 build is recorded as go1.26.8 (`r4-10:19,69,110-117`), so the missing-base class is consistent with that run; the binary and its transient log are gone, so the exact branch is not reproduced and its cause stays UNKNOWN.

### F2 — MEDIUM (calibration): row 3 says "Snapshot valid", but the line proves only that a base JSON was found and the request was echoed

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:104`.

```
$ Z=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
$ unzip -p "$Z" ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | nl -ba | sed -n '178,181p'
   178			if (!apiSnapshot.getVer().isInvalid()) {
   179				Msg.info(GoRttiMapper.class,
   180					"Using Go API snapshot for version %s".formatted(apiSnapshot.getVer()));
   181			}
$ unzip -p "$Z" ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java | nl -ba | sed -n '239p;503,505p'
   239			return new GoApiSnapshot(ver, results);
   503		public boolean isInvalid() {
   504			return arches.isEmpty();
   505		}
$ unzip -p "$Z" ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | nl -ba | sed -n '356p'
   356				if (apiSnapshot.isInvalid()) {
```

[OBSERVED] `GoApiSnapshot.read` stores the **requested** `GoVer` (`:239`); the mapper logs whenever that version is non-invalid (`:178-181`). `GoApiSnapshot.isInvalid()` is a *different* predicate — `arches.isEmpty()` (`:503-505`) — and is the one that selects the `Missing Go bootstrap type info` branch (`:356-360`). [INFERENCE from those source facts] A base JSON that exists but retains no applicable OS/arch record therefore logs `Using Go API snapshot for version X` and then throws missing-bootstrap; the line does not imply usable type data. The lane already documented this second cause at `r14:51-54` and qualified it at `r14:121-127` (source-level possibility, not observed for unpatched bases because every base carries the generic `all` bucket; patched results not asserted). "Snapshot valid" is therefore too strong for the cell; it is true only in the narrow sense "the requested major.minor is valid and a base file was read".

Smallest fix — replace the "Means" cell with:
> Base JSON found; X is the **request** echo; usable arch data is not implied (`GoApiSnapshot.isInvalid()` `:503-505`; see `r14:51-54`).

### F3 — LOW (calibration): row 6 attributes the message to symbol markup, but both analyzers emit the same text

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:107`.

```
$ unzip -p "$Z" ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java | nl -ba | sed -n '181,183p'
   181			catch (IOException e) {
   182				Msg.error(this, "Go analysis failure", e);
   183			}
$ unzip -p "$Z" ghidra/app/plugin/core/analysis/GolangStringAnalyzer.java | nl -ba | sed -n '124,126p'
   124			catch (IOException e) {
   125				Msg.error(this, "Go analysis failure", e);
   126			}
```

[OBSERVED] The aether line is `(GolangSymbolAnalyzer) Go analysis failure …` (`runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log:97`), so "Symbol markup aborted after bootstrap" is correct *for that run*. But the bare text `Go analysis failure` is emitted by both analyzers, and only the component tag distinguishes them; a string-analyzer catch would be described wrongly by this row. Smallest fix: qualify the row `Bootstrap OK, then (GolangSymbolAnalyzer) Go analysis failure …` (or note `GolangStringAnalyzer:125` emits the same text).

### F4 — LOW (missing caveat / completeness): the table has no row for `Invalid Go version string [X]`

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:101-107`.

```
$ unzip -p "$Z" ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | nl -ba | sed -n '166,169p'
   166			if (goVer.isInvalid()) {
   167				throw new BootstrapInfoException(
   168					"Invalid Go version string [%s]".formatted(buildInfo.getVersion()));
   169			}
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17
$ grep -n 'INVALID_VERSION_RE' tools/log-extract.py
83:INVALID_VERSION_RE = re.compile(r"Invalid Go version string \[([^\]]*)\]")
203:        iv = INVALID_VERSION_RE.search(message)
```

[OBSERVED] This is a distinct route: a version source is found (build-info record or `fallbackGoVer` option), but its text parses to `GoVer.INVALID` (`GoVer.java:62-81,105-107`), so mapper creation aborts before the range check or snapshot lookup. The entry's own extractor recognizes the message and the esbuild observation at `:84-85` says the run logged no "invalid" line, but the table gives a reader no row to interpret it; row 5 ("only `Reading Go binary info` + `unable to get`") does not match because the WARN line is present. Smallest fix — add one row:
> `Invalid Go version string [X]` | A version source was found (build-info record or `fallbackGoVer` option) but its text parses to `GoVer.INVALID`; mapper creation aborts before snapshot lookup (`GoRttiMapper:166-169`) | That no build-info record exists, or that the version is merely outside the declared range.

### F5 — LOW (missing anchor): INFERENCE 1's constructor claim is true, but the cited anchor does not establish it

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:114-116`.

```
$ unzip -p "$Z" ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | nl -ba | sed -n '110p;329p;348p;353,360p;444,445p'
   110						supplier_result.init(monitor);
   329		public GoRttiMapper(Program program, GoBuildInfo buildInfo, int ptrSize, GoVer goVer,
   348			initStructMappings();
   353				registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this);
   356				if (apiSnapshot.isInvalid()) {
   358					throw new BootstrapInfoException(
   359						"Missing Go bootstrap type info, unable to extract Go RTTI info."
   444		public void init(TaskMonitor monitor) throws IOException {
   445			GoModuledata firstModule = findFirstModuledata(monitor);
```

[OBSERVED] The claim "the failure happens in the constructor, before any moduledata read" is correct: the constructor (`:329`) ends with `initStructMappings()` (`:348`), whose empty-snapshot branch throws (`:358-360`); `init()` (`:444-445`, the `findFirstModuledata` path) is called by the supplier only after construction (`:110`). But the entry's only anchor for this INFERENCE is `:170-172`, which proves the range check *logs*, not where the failure occurs. Smallest fix: append `(constructor :329,348; throw :353-365; moduledata search in init() :444-445, called at :110)`.

## Bounded no-findings (checked; held)

- **N1 R1 `:102`.** `GoApiSnapshot.getPatchVerDiffFile` (`:148-166`) logs the INFO exactly in the `else` of `patchVer.getPatch() != goVer.getPatch()`, after the base lookup at `:122-126`; "base JSON found and selected patch = requested patch (exact diff or patch 0)" is the right meaning, and the observed INFO rows match (calib 0.25.12 `ghidra.log:63`; 0.21.5 `:62`). Caveat, not a row defect: the INFO precedes the JSON parse/application, so "found" is not "parsed"; a failure would add `Failed to read Go info`.
- **N2 R2 `:103`.** The WARN branch (`:158-161`) and "lower patch (or the base)" match the loop at `:153-156`; observed aether `:92` and notesmd `:68`. Same parse caveat as N1. "Does not mean X's API equals Y's" is correct.
- **N4 R4 `:105`.** The conjunction pins base-missing here: `GoApiSnapshot:118-126` returns null before the diff search, `GoRttiMapper:176-181` logs nothing for `EMPTY`, and `:356-360` throws. Observed shfmt `:82-84`, containerd `:240-242`, op `:68-70`; all three also show `Untested` (independent of the base check) and zero `GoApiSnapshot` lines. The "this installation" scoping keeps the row sound. Minor caveat: the "Means" omits "and no fallback version was supplied" (`GolangSymbolAnalyzer:129-131`; option default `""` at `:1345`); all eight runs had it empty.
- **N5 R5 `:106`.** `buildInfo == null` after `fromProgram` + `fromFallbackInfo` returns null (`GoRttiMapper:150-163`; `GoBuildInfo:188-200`); observed esbuild 0.27.7 `ghidra.log:63-69` (`Reading` then `unable to get`, no version/untested/invalid/bootstrap). "Does not mean not Go" matches `GoRttiMapper:160-162` ("probably not a Go binary") and REA's own limitation text.
- **INFERENCE 1 `:111-116`.** Verified true: installed bases are exactly `go1.15.0.json`…`go1.25.0.json` (143 files = 20 top-level + 123 patch diffs; `run-carriers.sh` adds carrier + r16 `selection.py` + prediction → 146 pins, and all eight receipts report `pins_compare.equal: true` with 146 entries); `SUPPORTED_VERSIONS` is `1.15-1.25` (`GoRttiMapper:79`); `:170-172` only logs. Only the anchors are missing (F5).
- **Observations table `:51-58`.** All eight carrier hashes, package owners (`pacman -Qo`: shfmt 3.14.1-1, aether 4.32.0-2, 1password-cli 2.41.0-1, containerd 2.4.2-1; notesmd-cli unowned), routes (`info` / `fallback` / `none`), type counts (4881/2302/6115/4411), `bootstrap_attempts` (2 for shfmt/containerd/op/esbuild-0.27.7, 1 for the four snapshot-loaded runs), `language_compiler` (`x86:LE:64:default:golang`), and `bound_sessions`=1 / `unbound_sessions`=0 match the receipts, observations and logs. `go1.27.0-X:nodwarf5` / `go1.27.2-X:nodwarf5` match `inspect-go.json`.
- **esbuild 0.27.7 cspec claim `:80`.** [OBSERVED] true: `ElfLoader:109-112` calls `detectCompilerName`, and `:196-198` selects `golang` when `GoRttiMapper.hasGolangSections` (`:201-210`) sees `.gopclntab`; `readelf -SW` shows `.gopclntab` and no `.go.buildinfo`. The entry gives no anchor; adding `ElfLoader.java:196-198` would improve auditability (not raised as a finding).
- **Method anchors `:34-37`.** `GoBuildInfo:488-489`, `GoVer:62-81`, `GoRttiMapper:79,170-172,179-180`, `GoApiSnapshot:122-126`, `TransientProgramProperties:107-110` all say what the entry claims. The `GoRttiMapper` request-echo is correct but needs `GoApiSnapshot:239` as the second anchor (not raised as a finding).
- **Pilot/prospective split `:37-40`.** [OBSERVED] `pilot/` contains only shfmt and esbuild 0.25.12 (`shfmt.json`, `esb.json`, logs); the six `pro-*` labels are absent. `pro-esbuild-0.27.7.prediction.json` is the hand-written one ("author: L1 … hand-derived … predict.py exits 2 on an empty version").
- **Evidence-ID repeat `:94-97`.** [OBSERVED] `runs/calib-shfmt/analyze.json` and `runs/calib-esbuild-0.25.12/analyze.json` equal `pilot/shfmt.json` / `pilot/esb.json` (`ev_2b29a1dd…`, `ev_391dbfe6…`); the "one repetition, not a determinism proof" wording is calibrated.

## Cross-surface (outside the assigned table/inference scope; independently reported by sibling w2 seats)

These are in the same entry's header and recheck, so I verified them; they are not my primary surface and other w2 seats cover them in detail.

- **S1 — HIGH: the advertised `recheck:` (`:3`) is red on every retained receipt.** `python3 -I -B tools/receipt-validate.py runs/calib-shfmt/receipt.json` → exit 1, `{"counts":{"invalid":1,"receipts":1,"unreadable":0,"valid":0}}`, `"findings":[{"code":"unrecognized_shape","where":"$","detail":"receipt matches neither retain nor carrier shape"}]`, `"status":"invalid"`; same for `pro-aether`. Root cause: `receipt-validate.py:95-99` requires `steps` to be a **list**, while `carrier-run.py:275,349` writes it as a **dict** keyed by step; the validator's selftest fixture uses a list (`:470`), so `--selftest` is CLEAN cases=5 without covering the real shape. Proof the shape is the sole blocker: a `/tmp` copy of the same receipt with `steps` rewritten to a list of its values validates → exit 0, 336 checks, no findings. Smallest fix: accept `dict` in `classify`, iterate `steps.values()` in `check_required` (keep the key in `where`), and add a dict-shaped selftest fixture mirroring `carrier-run.py:275,349`.
- **S2 — MEDIUM: `:37` cites an unresolvable commit.** `git cat-file -t 2716747` → `fatal: Not a valid object name 2716747`; `git log -1 --format='%H %cI' 2711674` → `271167473d87ef710f07ecdd98caf0ce12091686 2026-10-20T10:46:45-03:00`. The correct full hash is already on `:1`; `run-carriers.sh:2` repeats the typo. Smallest fix: replace `2716747` with `2711674` in both files.
- **S3 — LOW: the recheck's rerun clause destroys the evidence it says to compare.** `:3` says "then rerun one carrier with `bash …/run-carriers.sh <label>` and compare `observation.json` fields"; at HEAD `run-carriers.sh:14-15` is `out="runs/$label"` then `rm -rf "$out"; mkdir -p "$out"`, so `runs/<label>/` (receipt, logs, observation, compare) is deleted before the rerun. The worktree's `RUNS_DIR` mitigation is uncommitted (`git status --porcelain .ufo/waves/round-17/run-carriers.sh` → ` M …`) and not at `da64646`. Smallest fix: state "copy `runs/<label>` aside (or run with `RUNS_DIR=/tmp/…`) first; the script deletes `runs/<label>`."

## Residual risk / verification gaps

- Read-only seat: no REA analyze/search/decompile, no Ghidra, no carrier execution; all observations are the retained logs/JSON. I did not reproduce a session.
- F2's arch-empty route is source-level only. `r14:121-127` (the r15 qualification) says it is not observed for unpatched bases and patched results are unasserted; I did not craft a patched snapshot to exercise it.
- I did not verify the upstream Ghidra range (S029) or the Go 1.26/1.27 layout question; outside this seat. The aether "Cause: UNKNOWN" (`:90`) is separately attacked by `w2/ScoutGhidraEOFIssue.md` (upstream PR #9348); I did not independently verify that upstream claim, so I assert no cause and no negation here. F3 stands independently of that cause.
- The `:3` rerun clause was read, not executed (it would delete or modify retained evidence).
- No tool installs or updates were made.
