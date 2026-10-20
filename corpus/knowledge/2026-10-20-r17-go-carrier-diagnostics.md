source: S003 (installed Base-src.zip members `GoRttiMapper.java`, `GoApiSnapshot.java`, `GoBuildInfo.java`, `GoVer.java`, `TransientProgramProperties.java`), S023 (installed Go snapshot data), S024 (Go `debug/buildinfo` reader, https://go.dev/src/debug/buildinfo/buildinfo.go at go1.27.3), S025 (Go release history, https://go.dev/doc/devel/release), S026 (Go linker `X:` suffix, `src/cmd/link/internal/ld/main.go:191-198` at go1.27.3), S029 (Ghidra upstream range at tag `Ghidra_12.1.4_build` vs master), S031 (Go 1.25 notes, `#dwarf5-support`), S032 (Ghidra PR #9348, tier B lead) in `corpus/SOURCES.md`; retained runs under `.ufo/waves/round-17/runs/` (second pass) and at lane commit `da64646adcb19c1ede7537b799b8c7d283fe43da` (first pass); predictions frozen at lane commit `271167473d87ef710f07ecdd98caf0ce12091686` before any measured run.
verified-at: 2026-10-20 — two sequential passes of eight REA 6.5.0 `analyze` sessions (Ghidra 12.1.4 provider): first pass 13:47–14:00 UTC, second pass 14:27–14:40 UTC with the hardened capture tool; author-side, not outside verification.
recheck: read-only first — `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/<label>/receipt.json` (exit 0 = digests, pins, log binding and mid-run checks consistent); then a non-destructive rerun `RUNS_DIR=/tmp/r17-recheck bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/run-carriers.sh <label>` and compare its `observation.json` route/version/bootstrap fields (not paths or timestamps) with the retained one. Compare `carrier.sha256_pre` first: package upgrades change carrier bytes.

# Go carrier diagnostics: retained Ghidra analyzer logs against frozen source predictions

## Question

Rounds 14–16 held the Go RTTI bootstrap path as source reading and a source
model: the r14 decision table, the r15 installed inventory and the r16
selection preview. No analyzer log had ever been retained. REA deletes its
Ghidra runtime root, including `ghidra.log`, when the session closes, and
r4-10 recorded the bootstrap message only as "observed-not-cited". This entry
asks two things. On real, pinned carriers, which Go-analysis route does the
installed provider take? And does the source model predict that route
**before** the run?

## Method

- **Capture.** `tools/carrier-run.py` gives each REA child a private
  `TMPDIR` (`/tmp/kr17-rea-*`) and an allowlisted environment
  (`NODE_DISABLE_COMPILE_CACHE=1`, no tokens). It polls that parent every
  0.5 s and copies only `ghidra.log` and `script.log` of new `rea-ghidra-*`
  roots before REA's close deletes them. A retained log counts only when its
  own bytes bind it to the run: `Using log file: <session>/ghidra.log` and
  `IMPORTING: file://<session>/target-<carrier sha256[:12]>.bin`. Every run
  in both passes had exactly one bound session and zero unbound sessions.
- **Pins.** Each run pins 146 paths: the carrier, r16 `selection.py`, the
  frozen prediction, and all 143 installed Go data files. In the second pass
  each pin map is retained with its UTC instant: pre, every 30 s during
  analyze (2–8 checks per run, `steps.analyze.pin_checks`), and post. All
  maps are equal. They show identical bytes **at those instants** only
  (QUALITY #19). The first-pass receipts kept only pre/post maps.
- **Prediction before observation.** `tools/predict.py` reproduces Ghidra's
  parse:
  - strip one `go` (`GoBuildInfo.java:488-489`);
  - `GoVer.parse` (`GoVer.java:62-81`), checked against the real Java on 366
    strings with 0 disagreements (`.ufo/waves/round-17/w2/predict-java-diff/`);
  - the declared range `1.15-1.25` (`GoRttiMapper.java:79`);
  - r16 `select_snapshot`.

  From these it derives the **route** that `GoApiSnapshot` logs:
  - `none`: no base JSON, `GoApiSnapshot.java:122-126`;
  - `info`: selected patch = requested patch, `:162-164`;
  - `fallback`: WARN, `:158-161`.

  All eight predictions were committed at `2711674` before the first
  measured run. The two `calib-*` carriers had already been seen in the
  pilot (10:17–10:19 -03), so they are calibration, not prediction. Of the
  six `pro-*` carriers, three test routes no run had shown before the freeze:
  `pro-notesmd-cli` and `pro-aether` (fallback) and `pro-esbuild-0.27.7` (no
  build info). The other three repeat pilot-seen routes: containerd-shim and
  op (`none`), esbuild 0.21.5 (`info`). The `pro-esbuild-0.27.7` prediction
  was written by hand because `predict.py` refuses an empty version. Its
  extra expectations are now compared mechanically (`compare.py`
  `extra.*` fields).
- **Extraction and compare.** `tools/log-extract.py` reads route only from the
  `GoApiSnapshot` component. The `GoRttiMapper` line `Using Go API snapshot
  for version X` echoes the **requested** version
  (`GoRttiMapper.java:179-180`), so it cannot discriminate. Of the compared
  fields, `snapshot_label` and `untested_version` are near-tautological on
  this host. The discriminating fields are `snapshot_route` and `fallback_to`.

## Observations (both passes: carrier-run exit 0, compare exit 0, 8/8)

| label | carrier (package) | sha256[:16] | build-info Go | route predicted = observed | key retained lines | bootstrap |
|---|---|---|---|---|---|---|
| calib-shfmt | `/usr/bin/shfmt` (shfmt 3.14.1-1) | `58f765638eed5309` | `go1.27.0-X:nodwarf5` | none | `Untested Go version [1.27.0]`; no snapshot line; `Missing Go bootstrap type info` ×2 | missing |
| calib-esbuild-0.25.12 | `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild` | `bab29b2ca7a9e89b` | `go1.23.12` | info | `GoApiSnapshot` INFO `Using Go API snapshot for 1.23.12` | loaded; 4881 types |
| pro-notesmd-cli | `/home/vgpnk/.local/bin/notesmd-cli` (no package owner) | `412dc532d278b9e4` | `go1.25.8` | fallback → 1.25.0 | WARN `Falling back from 1.25.8 to 1.25.0 for Go API snapshot`, then `…for version 1.25.8` | loaded; 2302 types |
| pro-aether | `/usr/bin/aether` (aether 4.32.0-2) | `06c91f55df4117e5` | `go1.25.14` | fallback → 1.25.0 | WARN `Falling back from 1.25.14 to 1.25.0…`, then `…for version 1.25.14` | loaded; 6115 types; symbol markup then fails |
| pro-esbuild-0.21.5 | `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.21.5/node_modules/@esbuild/linux-x64/bin/esbuild` | `b567f467fdac92c6` | `go1.20.12` | info | INFO `Using Go API snapshot for 1.20.12` | loaded; 4411 types |
| pro-containerd-shim | `/usr/bin/containerd-shim-runc-v2` (containerd 2.4.2-1) | `d3aa80d720b80f70` | `go1.27.2-X:nodwarf5` | none | `Untested Go version [1.27.2]`; no snapshot line; missing bootstrap ×2 | missing |
| pro-op | `/usr/bin/op` (1password-cli 2.41.0-1) | `f4ac474fd0202c73` | `go1.26.8` | none | `Untested Go version [1.26.8]`; no snapshot line; missing bootstrap ×2 | missing |
| pro-esbuild-0.27.7 | `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/bin/esbuild` | `c638273fcf95573c` | none (`build_info: null`) | none (hand) | `Reading Go binary info` ×2 only; both analyzers `unable to get GoRttiMapper` | no mapper |

Full carrier SHA-256, step argv, exit codes, timestamps, log digests and the
analyze Evidence IDs are in each `runs/<label>/receipt.json`. The
`inspect-go-binary` Evidence IDs are in `runs/<label>/inspect-go.json`. All
runs report language/compiler `x86:LE:64:default:golang`. `pro-op` ran with
`REA_GHIDRA_STARTUP_TIMEOUT_MS=900000`, recorded in its receipt, because of
its 47 MB size.

- **OBSERVATION: the fallback WARN is the route signal; the mapper line is an
  echo.** The two 1.25.x carriers (no installed 1.25 patch diffs) logged
  `Falling back from <req> to 1.25.0`. The next line still says
  `Using Go API snapshot for version <req>`. That confirms the r16 reject at
  runtime: the requested label is not the selected data.
- **OBSERVATION: missing base means no `GoApiSnapshot` line at all.** All
  three out-of-range carriers (1.26.8, 1.27.0, 1.27.2) logged `Untested`,
  then `Missing Go bootstrap type info`, with no snapshot line.
  `bootstrap_attempts` (cache-miss calls that log `Reading Go binary info`)
  is 2 in each case. A null mapper is not cached
  (`TransientProgramProperties.java:107-110`), so the Symbol and String
  analyzers each retry. The count is 2 **here** only because no DWARF loaded.
  `GolangDWARFFunctionFixup.java:286` is a further caller per imported
  function.
- **OBSERVATION: absent build info is a distinct route.** esbuild 0.27.7 has
  no `\xff Go buildinf:` record. Three readers agree:
  - REA `build_info: null`;
  - `tools/buildinfo-probe.py` whole-file scan;
  - the official go1.27.3 `go version -m`, which reports `not a Go
    executable`, i.e. S024's `errNotGoExe`, `buildinfo.go:411`.

  Ghidra still chose the golang compiler spec, which on ELF comes from
  section names (`ElfLoader.java:188-200`; INFERENCE from source). It logged
  no version, untested, invalid or bootstrap line.
- **OBSERVATION, unpredicted: bootstrap is not full recovery.** On aether,
  the mapper bootstrapped and found 6115 types. Then `GolangSymbolAnalyzer`
  logged `Go analysis failure java.io.IOException:
  java.lang.reflect.InvocationTargetException`, caused by
  `java.io.EOFException: Unable to read past EOF: 17645861, 111938854`
  (`runs/pro-aether/logs/*/ghidra.log:97-177`). Go string recovery still ran
  (`Go strings found: 7200`). The same EOF numbers reproduced in the second
  pass, as frozen in `predictions/replicate-expectations.json`.
- **OBSERVATION: Evidence IDs repeat except aether.** 7/8 analyze Evidence IDs
  were identical across the two passes, and `calib-*` also matched the pilot.
  This is consistent with the content-keyed `analyze` id (QUALITY #15). The
  aether id differed (`ev_ae9f7086…` → `ev_247261e8…`) because
  `string_count` went 29118 → 29117. The frozen "id equals first pass"
  expectation is therefore **falsified for aether**: one Ghidra string-count
  difference between identical-byte runs.

## Decision table (installed Ghidra 12.1.4, REA 6.5.0, x86-64 Linux ELF)

| Log signal | Means | Does not mean |
|---|---|---|
| `GoApiSnapshot` INFO `Using Go API snapshot for X` (X = the normalized version; rc/beta and `X:` suffixes are dropped by `GoVer.parse`) | Base JSON found and selected patch = X's patch (exact diff or patch 0) | Which bytes were read, that patched content is correct, or that X was the toolchain's full version string |
| `GoApiSnapshot` WARN `Falling back from X to Y for Go API snapshot` | Base found; a lower patch was used. Only fallback to the base (Y = M.m.0) was observed | That X's API equals Y's; fallback to an intermediate diff was never observed |
| `GoRttiMapper` `Using Go API snapshot for version X` | Base JSON found; X is the **request** echo | The selection route, or usable arch data (`isInvalid()` tests arches separately) |
| `Untested Go version [X]` + no snapshot line + `Missing Go bootstrap type info` | No installed base for X's minor (this installation: 1.26.x, 1.27.x) | That the range check stopped analysis (it only logs, `GoRttiMapper.java:170-172`), or that the binary layout changed |
| `Invalid Go version string [S]` (WARN, `GoRttiMapper.java:166-169`) | A build-info version was found but did not parse | Absence of build info (no carrier exercised this line) |
| Only `Reading Go binary info` + `unable to get GoRttiMapper` | No build-info record and no fallback version | That the file is not Go |
| Bootstrap OK, then `GolangSymbolAnalyzer` `Go analysis failure …` | Symbol markup aborted after bootstrap (strings may still be recovered) | That the snapshot fallback caused it |

## Inference (labelled)

- INFERENCE: on this host the declared range and the installed bases cover
  the same minors (1.15–1.25). An out-of-range carrier therefore always lacks
  a base, and these runs cannot separate the advisory range check from the
  missing base; the source can. The failure is thrown in the mapper
  constructor (`GoRttiMapper.java:348,351-360`) before `init()` reads any
  moduledata (`:444`). A Go 1.26/1.27 layout change is neither shown nor
  excluded.
- INFERENCE, aether cause:
  - Installed `go1.25.0.json` maps `runtime.maptype` to
    `internal/abi.OldMapType` (0x58 bytes), and Ghidra's `GoMapType` has no
    Swiss-map binding. aether's maps use the Swiss layout (0x70 bytes).
  - A static byte trace of `/usr/bin/aether` follows a misread map-type
    method-info field into a name record at 0x10d4120. That record's varint
    length is 111938854, read at 0x10d4125 = 17645861: exactly the logged
    pair of address and length.
  - The same mechanism is described by the open, unmerged upstream PR #9348
    (S032, tier B).
  - The base JSON is identical for notesmd-cli. notesmd-cli has no map types
    with method info, so it does not reach this path; the 1.25.14→1.25.0 patch
    fallback is not the cause.
  - These are seat byte traces (`.ufo/waves/round-17/w2/CriticAetherUnknown.md`,
    `RevAetherEOF.md`), not a Ghidra replay with instrumentation. The exact
    invoking record is unresolved.
  - Corollary, also INFERENCE: the same binding would silently misread the
    size fields of every Swiss map type in any 1.24/1.25 carrier
    (notesmd-cli has 63 map types) without a log line. "No error" in the
    table therefore does not mean that map types were laid out correctly.
- INFERENCE, version strings:
  - The `-X:nodwarf5` suffix is the linker's record of a non-default
    link-time experiment configuration: S026 `main.go:191-198`, and S031,
    under which DWARF 5 is disabled at build time.
  - `GoVer.parse` truncates at `-`, so such a carrier is analysed as the
    plain release (here 1.27.0/1.27.2).
  - S025 dates go1.27.0 to 2026-08-19, so 1.27.x carriers are plausible on
    2026-10-20. A release date is a lower bound for a build, not its date.
  - S029: no released Ghidra declares 1.26 or 1.27; master declares 1.26
    only. The missing-base route is expected to persist on 12.1.x.
- INFERENCE, historical op pair: r4-10 recorded `op` 2.40.0 as go1.26.8
  (`2026-10-13-r4-10-real-version-pair.md:19,69`), which by version falls in
  this missing-base class. Its log was never retained and the package is
  gone, so that run's actual route stays unobserved. The current `op`
  2.41.0-1 (go1.26.8) is a different binary that does show the route.

## Not examined

- Patched-content correctness, which diff bytes Ghidra applied, and
  arch-bucket retention: none of these is logged.
- Fallback to an intermediate patch diff (e.g. 1.24.7+ → 1.24.6): no host
  carrier exercises it. The base-present but arch-empty route, a parse-failing
  version string, and DWARF-loaded failing carriers are source-only.
- Other providers, REA/Ghidra versions, OS/arch or file formats (all x86-64
  ELF). The golang-cspec rule above is ELF-specific; PE uses build ID or
  build-info bytes.
- Determinism beyond two passes per carrier. Procedure-name inventories: no
  `search` was run. `procedure_count`/`string_count` are totals, not Go
  recovery rates.
- Log completeness: the retained log is a polling prefix. All 16 retained
  logs reach `REPORT: Analysis succeeded`, and every Go line precedes the
  bridge script. Absence claims hold only up to the last retained line.
- The Python model vs Gson/Java behaviour, and the S003 source archive vs
  the loaded classes: not authenticated.
