# CriticGeneralization — round 17 wave 2 (author-side advisory critic)

Seat: `KaidokuR17.CriticGeneralization`. Lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da` (`git rev-parse HEAD` printed it). Axes: **calibration** and **depth**.
Targets: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (K), `SKILL.md:509-541` (S), and `corpus/README.md:35` (R). The top-level `README.md` has 24 lines at this revision (`git show da64646:README.md | wc -l` → `24`), so "README:35" is read as `corpus/README.md:35`, the Go-lineage row that holds the r17 token.
Method: I read files only. Ghidra 12.1.4 sources came from `Base-src.zip`, extracted to `/tmp/kr17-critgen`. I also ran `readelf -SW`, `go version -m`, round-17 `predict.py`, and ran `grep` over the retained logs. I did not run REA analyze/Ghidra and did not execute any carrier. I installed nothing. Tags: **OBS** = I observed it with the cited command. **INF** = inference.

Question asked of each sentence: does it state, as a general law, something the evidence supports only for this host, x86-64 ELF, one run per carrier, and Ghidra 12.1.4/REA 6.5.0?

## Findings

### F1 — MEDIUM — the "×2" bootstrap count depends on carrier and host state, not only on the analyzer count
- Sites:
  - S:522: `` `Untested Go version [X]`, no snapshot line, `Missing Go bootstrap type info` ×2 ``
  - K:56-57: "missing bootstrap ×2"
  - K:75-77: "The bootstrap attempt repeats once per Go analyzer (`bootstrap_attempts` = 2), because a null mapper is not cached"
- Counterexample (source, OBS):
  - There is a third caller of `GoRttiMapper.getSharedGoBinary`. `grep -rn getSharedGoBinary` returns `GolangStringAnalyzer.java:103`, `GolangSymbolAnalyzer.java:133` and **`GolangDWARFFunctionFixup.java:286`**.
  - The fixup calls `initGoBinaryContext` for every Go DWARF function (`GolangDWARFFunctionFixup.java:77-80`, `:283-288`). It keeps `goBinary` as an instance field, and one fixup list is built per DWARF program (`DWARFProgram.java:631` `functionFixups = DWARFFunctionFixup.findFixups()`). A null mapper is not cached (`TransientProgramProperties.java:107-110`).
  - So when DWARF loads on an out-of-range or no-build-info binary, every Go function retries the bootstrap. Each retry repeats `Reading Go binary info` / `Untested` / `Missing Go bootstrap…`. This is INF from source; it was not run.
- Why it did not appear (OBS):
  - The DWARF analyzer is enabled by default (`DWARFAnalyzer.java:57-58`), and it ran in these REA sessions. For example, `runs/calib-shfmt/logs/rea-ghidra-j5AXOZ/ghidra.log:79,81` shows `DWARF external debug information found: … filename=shfmt.debug … hash=ff9989502b95…` and then `Unable to find DWARF information, skipping DWARF analysis`.
  - The analyzer timing line `DWARF 0.004 secs` is at `:97`.
  - `readelf -SW <carrier> | grep -oE '\.(debug_[a-z]+|…)'` found **no** `.debug_*` section on any of the eight carriers.
- Host-state dependence (OBS + INF):
  - Ghidra's default debug-file providers include the user debuginfod cache (`ExternalDebugFilesService.java:123-127,171-175`; `LocalDirDebugInfoDProvider.java:88-91` → `~/.cache/debuginfod_client`).
  - On this host, `echo $DEBUGINFOD_URLS` → `https://debuginfod.archlinux.org`. `ls ~/.cache/debuginfod_client` lists two build-id dirs (`4bd539a8…`, `cc56d2fd…`). `ls ~/.cache/debuginfod_client/ff9989502b95bd930f44ff74295bbc1fb4061812` → `No such file or directory`.
  - INF: one `debuginfod-find`/gdb session on `/usr/bin/shfmt` would put the debug file there. After that, a rerun on the **same `sha256_pre`** could log many bootstrap attempts instead of 2. The recheck recipe at K:3 compares only carrier bytes, not the debug-cache state.
  - The pilot also records an `REA_GHIDRA_DISABLED_ANALYZERS` knob (`pilot/README.txt:5`), which would lower the count.
- Impacted axes: calibration (a conditional count is presented as a signal), depth (the third caller is missed).
- Smallest fix:
  - S:522: change `×2` to `≥1 (×2 here: Symbol+String analyzers, no DWARF loaded)`.
  - K:76: change "once per Go analyzer" to "once per `getSharedGoBinary` caller (Symbol, String; and per Go DWARF function via `GolangDWARFFunctionFixup.java:283-288` when DWARF loads, e.g. from `~/.cache/debuginfod_client`)".
  - K:3: add "debuginfod cache state" to the recheck preconditions.

### F2 — MEDIUM — the INFO row's "selected patch = requested patch" hides version normalization
- Sites:
  - S:520: "Base found; selected patch = requested patch"
  - K:102: "selected patch = requested patch (exact diff or patch 0)"
- Counterexample (OBS):
  - `GoVer.parse` deletes everything from the first character that is not `[.0-9]` (`GoVer.java:63-65`). A missing patch becomes 0 (`GoVer.java:46-47,72-74`).
  - Command: `python3 -I -B .ufo/waves/round-17/tools/predict.py --go-version go1.21rc2 --golang-root <golang>`
  - Output: `"normalized": "1.21.0"`, `"snapshot_route": "info"`, `"snapshot_label": "1.21.0"`.
  - So a release-candidate binary would log the GoApiSnapshot **INFO** line for 1.21.0 release data, with no WARN. In the same way, `go1.22.8 X:rangefunc` → `"normalized": "1.22.8"`, `info`.
  - The X:<GOEXPERIMENT> suffix is dropped. Experiments that change runtime type layout would therefore get release snapshot data, and no log line would show it (INF).
  - No in-range carrier with a suffix was run. All three `-X:nodwarf5` carriers were out of range.
- Impacted axes: calibration ("requested" means the parse-normalized version, not the build's toolchain identity).
- Smallest fix: append to the Limit cell at S:520 and the "Does not mean" cell at K:102: "X is the `GoVer.parse`-normalized version; rc/beta and `X:` suffixes are dropped (`GoVer.java:63-65`), so INFO does not show the build matches the snapshot's release or experiment set."

### F3 — LOW-MEDIUM — the no-build-info row states ELF/Ghidra-reader facts as general facts
- Site: S:523: "No build-info record (check `inspect-go-binary` `build_info: null`) | Not "not Go": the golang cspec comes from section names"
- K:81 says the same without a format qualifier: "which comes from section names, not build info".
- The S table header has no ELF qualifier; K:98 has one.
- Counterexamples (OBS, source):
  - The cspec rule from section names holds for ELF (`ElfLoader.java:188-199`) and Mach-O (`MachoLoader.java:547-548`). For PE, golang is chosen from a Go build ID in `.text` **or** build-info magic in the first 512 bytes of `.data` (`PeLoader.java:1146-1171`). A PE file with neither would get no golang cspec, the Go analyzers would not run, and this row's signature would never appear.
  - Ghidra reads build info only from the `.go.buildinfo`/`go_buildinfo` section, or from the first 512 bytes of PE `data` (`GoBuildInfo.java:92-108`). It returns null on **any** `IOException` in that read (`:137-152`).
  - REA `inspect-go-binary` and `buildinfo-probe.py` are separate readers. Their `build_info: null` is a correlate of Ghidra's null, not the same test.
  - On this carrier set the readers agreed. `readelf -SW` shows `pro-esbuild-0.27.7` has only `.gopclntab`, with no `.go.buildinfo`. `go version -m` → "could not read Go build info … not a Go executable".
- Smallest fix:
  - Scope S:523 and K:81 to "ELF/Mach-O (`ElfLoader.java:196-197`); PE differs."
  - Reword S:523 to: "Ghidra found no readable `.go.buildinfo` record and no fallback version; REA `build_info: null` is an independent correlate."

### F4 — LOW — the SKILL section and the README cell drop the scope that K carries
- S:512-516: "runs real, pinned Go carriers through REA 6.5.0 … Eight of eight matched, including six prospective carriers. Use it before attributing Go symbol loss to a layout change."
- The S:518 table has no "Ghidra 12.1.4, Linux x86-64 ELF" qualifier, but K:98 has it ("Decision table (installed Ghidra 12.1.4, REA 6.5.0, Linux x86-64 ELF)").
- Every row depends on Ghidra-12.1.4-specific source: the range `1.15-1.25` at `GoRttiMapper.java:79`, the message strings, and the cspec detection.
- The lane's own lesson already rejects the general reading: `corpus/lessons/round-17.md:36` reads "8/8 matches prove the predictor generally | reject | One host, x86-64 ELF, one run per carrier, Ghidra 12.1.4 only".
- R (`corpus/README.md:35`): the r17 clause "8/8 routes matched frozen predictions incl. the 1.25.x fallback WARN" has no limit clause. The r16 clause in the same cell keeps "source-model only".
- Calibration detail: one of the six prospective predictions (`pro-esbuild-0.27.7`) was written by hand (K:39-40; `predictions/carriers.tsv`). S:513-515 says each route was "predicted from installed source".
- Smallest fix:
  - S:515: "Eight of eight matched (one run each, one host, x86-64 ELF, Ghidra 12.1.4; one hand prediction)."
  - S:518: add `(Ghidra 12.1.4 via REA 6.5.0, x86-64 Linux ELF)` to the table lead-in.
  - R:35: append "; one host, x86-64 ELF, one run each".

### F5 — LOW — the fallback row is generalized past the only fallback shape observed
- S:521 "Lower patch data used" and K:103 "a lower patch (or the base) was used" are correct as source readings.
- But the only fallback observed at runtime is **to the base** (1.25.x → 1.25.0), in a minor with **zero** installed diffs.
- OBS:
  - `ls patchverdiffs | grep '^go1\.25\.'` → count 0. The largest installed diffs per minor are 1.24:6, 1.23:12, 1.22:12, 1.21:13 and 1.20:14.
  - So neither 1.25 prediction exercised r16 `select_snapshot` choosing among diffs.
  - Fallback to a nonzero intermediate diff (for example a go1.24.7+ request → 1.24.6) was never observed. That includes the derived patched provider (`GoApiSnapshot.java:133-145`).
  - My host census found no such carrier. `go version` over `/usr/bin/*` and `~/.local/bin/*` found in-range builds only at go1.25.8 and go1.25.14. A wider find found only go1.20.12 and go1.23.12.
- R:35 correctly keeps r16 as "source-model only". The "8/8" claims (S:515, R:35) should not be read as runtime confirmation of r16's request-bounded selection.
- Smallest fix: add one bullet to K "Not examined": "Fallback to a nonzero intermediate diff (requests above the highest installed diff of a minor that has diffs, e.g. ≥1.24.7): no host carrier."

### F6 — LOW — "the only selection signal" (K:68)
- K:68 reads "the fallback WARN is real and is the only selection signal". K's own table (K:102) treats the GoApiSnapshot INFO line as selection evidence (`GoApiSnapshot.java:162-164`), so the sentence contradicts its own document.
- Smallest fix: "…is the only signal that the selected data differs from the request."

### F7 — LOW — "all Go lines were captured" (K:132-133)
- K:132-133 reads "Every Go line precedes the bridge script, so all Go lines were captured."
- OBS: all eight retained logs end exactly at `ANALYZING changes made by post scripts` (for example `runs/calib-shfmt/…/ghidra.log:125`, `runs/pro-op/…/ghidra.log:115`). That analysis pass is never retained.
- `corpus/lessons/round-17.md:37` itself says "the capture is a prefix".
- INF: the Go analyzers probably do not run again in that pass, but this is unobserved.
- The next sentence (K:133) hedges correctly, but the "so all" clause states more than the evidence.
- Smallest fix: "every retained Go line precedes the bridge script; Go lines from the killed post-script pass, if any, are unobservable."

## Checked, no finding (bounded)
- **Source anchors:**
  - Every anchor below matches the extracted 12.1.4 source: `GoApiSnapshot.java:122-126` (no base → null), `:158-161` WARN, `:162-164` INFO; `GoRttiMapper.java:79` range, `:170-172` (logs only), `:179-180` (request echo); `TransientProgramProperties.java:107-110` (null not cached).
  - The bootstrap failure happens in the constructor (`GoRttiMapper.java:346-366`). `init(monitor)`, which reads moduledata, runs only after `getGoBinary` returns (`:108-111`). So K:115-116 and the S:522 Limit cell are correct for 12.1.4.
- **K:111-112 "always lacks a base", which is scoped "on this host":** the installed bases are exactly `go1.15.0…go1.25.0.json`, and below 1.15 there is also no base. `find golang -type f | wc -l` → 143, matching S:532 "143 installed Go data files" and K:26 "146 paths" (143 + 3).
- **Hedged claims and table scope:** K:92-96 (Evidence-ID repeat: "one repetition, not a determinism proof"), K:84-91 (aether failure: cause UNKNOWN) and K:117-120 (op 2.40.0: conditional and UNKNOWN) are hedged correctly. K:98 carries the full scope qualifier. K:126-128 lists other providers, versions, OS/arch and determinism as not examined.
- **R:35 facts:** the version span "1.20–1.27, no-build-info" matches the eight `observation.json`/`compare.json` files (all `all_match: true`). `bootstrap_attempts` 1/2 per run matches K's table.

## Tooling
- No installs or updates.
- Scratch is only under `/tmp/kr17-critgen` (extracted `Base-src.zip` members).
- Every Python run used `-B`.
