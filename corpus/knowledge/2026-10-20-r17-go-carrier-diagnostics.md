source: S003 (installed Base-src.zip members `GoRttiMapper.java`, `GoApiSnapshot.java`, `GoBuildInfo.java`, `GoVer.java`), S023 (installed Go snapshot data), S024 (Go `debug/buildinfo` reader, https://go.dev/src/debug/buildinfo/buildinfo.go at go1.27.3), S025 (Go release history, https://go.dev/doc/devel/release), S026 (Go linker `X:` suffix, `src/cmd/link/internal/ld/main.go:191-198` at go1.27.3), S029 (Ghidra upstream range at tag `Ghidra_12.1.4_build` vs master) in `corpus/SOURCES.md`; retained runs under `.ufo/waves/round-17/runs/`; predictions frozen at lane commit `271167473d87ef710f07ecdd98caf0ce12091686` before any run.
verified-at: 2026-10-20 — eight REA 6.5.0 `analyze` sessions (Ghidra 12.1.4 provider), 13:47–14:00 UTC, run sequentially by the round-17 L1; author-side, not outside verification.
recheck: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/<label>/receipt.json` (digests of retained logs/outputs), then rerun one carrier with `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/run-carriers.sh <label>` and compare `observation.json` fields; carrier bytes may change on package upgrade — compare the receipt's `carrier.sha256_pre` first.

# Go carrier diagnostics: retained Ghidra analyzer logs against frozen source predictions

## Question

Rounds 14–16 held the Go RTTI bootstrap path as source reading and a source
model (r14 decision table, r15 installed inventory, r16 selection preview). No
analyzer log had ever been retained: REA deletes its Ghidra runtime root,
including `ghidra.log`, when the session closes (r4-10 recorded the bootstrap
message as "observed-not-cited"). This entry asks: on real, pinned carriers,
which Go-analysis route does the installed provider actually take, and does
the source model predict it **before** the run?

## Method (what makes this more than a re-read)

- **Capture.** `tools/carrier-run.py` gives each REA child a private `TMPDIR`
  (`/tmp/kr17-rea-*`), polls that parent every 0.5 s and copies only
  `ghidra.log` and `script.log` of new `rea-ghidra-*` roots before REA's
  close deletes them. A retained log counts only when its own bytes bind it to
  the run: `Using log file: <session>/ghidra.log` and
  `IMPORTING: file://<session>/target-<carrier sha256[:12]>.bin`. Every run
  had exactly one bound session and zero unbound sessions.
- **Pins.** 146 paths — the carrier, r16 `selection.py`, the frozen prediction
  and every file of the installed Go data dir — were hashed before, every 30 s
  during, and after each session (`tools/pins.py`). All eight pre/post compares
  are equal and no mid-run check differed. This shows identical bytes at those
  instants, not continuity between them.
- **Prediction before observation.** `tools/predict.py` strips `go`
  (`GoBuildInfo.java:488-489`), applies `GoVer.parse` (`GoVer.java:62-81`), tests
  the declared range `1.15-1.25` (`GoRttiMapper.java:79`), calls r16
  `select_snapshot`, and derives the **route** that `GoApiSnapshot` logs:
  `none` (no base JSON, `GoApiSnapshot.java:122-126`), `info` (selected patch =
  requested patch, `:162-164`) or `fallback` (WARN, `:158-161`). Predictions for
  all eight carriers were committed at `2716747` before the first run. The two
  `calib-*` carriers had been seen in the pilot. The six `pro-*` carriers had not.
  The `pro-esbuild-0.27.7` prediction was written by hand, because
  `predict.py` refuses an empty version.
- **Extraction and compare.** `tools/log-extract.py` reads route from the
  `GoApiSnapshot` component only. The `GoRttiMapper` line `Using Go API snapshot
  for version X` echoes the **requested** version (`GoRttiMapper.java:179-180`),
  so it cannot discriminate. `tools/compare.py` checks `untested_version`,
  `snapshot_label`, `missing_bootstrap`, `snapshot_route` and `fallback_to`.

## Observations (all eight runs: carrier-run exit 0, compare exit 0)

| label | carrier (package) | sha256[:16] | build-info Go | predicted route | observed GoApiSnapshot / GoRttiMapper lines | bootstrap |
|---|---|---|---|---|---|---|
| calib-shfmt | `/usr/bin/shfmt` (shfmt 3.14.1-1) | `58f765638eed5309` | `go1.27.0-X:nodwarf5` | none, untested 1.27.0 | `Untested Go version [1.27.0]`; no snapshot line; `Missing Go bootstrap type info` ×2 | missing |
| calib-esbuild-0.25.12 | kimi-code pnpm `@esbuild/linux-x64@0.25.12` | `bab29b2ca7a9e89b` | `go1.23.12` | info | `Using Go API snapshot for 1.23.12` (INFO) | loaded; 4881 types |
| pro-notesmd-cli | `~/.local/bin/notesmd-cli` (no package owner) | `412dc532d278b9e4` | `go1.25.8` | fallback → 1.25.0 | `Falling back from 1.25.8 to 1.25.0 for Go API snapshot` (WARN), then `…for version 1.25.8` | loaded; 2302 types |
| pro-aether | `/usr/bin/aether` (aether 4.32.0-2) | `06c91f55df4117e5` | `go1.25.14` | fallback → 1.25.0 | `Falling back from 1.25.14 to 1.25.0…` (WARN), then `…for version 1.25.14` | loaded; 6115 types |
| pro-esbuild-0.21.5 | pnpm `@esbuild/linux-x64@0.21.5` | `b567f467fdac92c6` | `go1.20.12` | info | `Using Go API snapshot for 1.20.12` (INFO) | loaded; 4411 types |
| pro-containerd-shim | `/usr/bin/containerd-shim-runc-v2` (containerd 2.4.2-1) | `d3aa80d720b80f70` | `go1.27.2-X:nodwarf5` | none, untested 1.27.2 | `Untested Go version [1.27.2]`; no snapshot line; missing bootstrap ×2 | missing |
| pro-op | `/usr/bin/op` (1password-cli 2.41.0-1) | `f4ac474fd0202c73` | `go1.26.8` | none, untested 1.26.8 | `Untested Go version [1.26.8]`; no snapshot line; missing bootstrap ×2 | missing |
| pro-esbuild-0.27.7 | pnpm `@esbuild/linux-x64@0.27.7` | `c638273fcf95573c` | none (`build_info: null`) | hand: none, no version lines | `Reading Go binary info` ×2 only; analyzer errors `unable to get GoRttiMapper` | no mapper |

Full SHA-256, REA `inspect-go-binary` and `analyze` Evidence IDs, step argv,
exit codes, timestamps and log digests are in each `runs/<label>/receipt.json`.
For example, the analyze ID for `calib-shfmt` is
`ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3`, and the
ID for `pro-notesmd-cli` is
`ev_4fd342dd05bcf5a5da4d3574c09501bff856245ccd336f1c6a337459c0b350d7`. All
runs report language/compiler `x86:LE:64:default:golang`.

- **OBSERVATION: the fallback WARN is real and is the only selection signal.**
  The two 1.25.x carriers (no installed 1.25 patch diffs) logged
  `Falling back from <req> to 1.25.0`. The very next line still says
  `Using Go API snapshot for version <req>`. That confirms the r16 reject at
  runtime: the requested label is not the selected data.
- **OBSERVATION: missing base means no snapshot line at all.** All three
  out-of-range carriers (1.26.8, 1.27.0, 1.27.2) logged `Untested` and then
  `Missing Go bootstrap type info` without any `GoApiSnapshot` line. The
  bootstrap attempt repeats once per Go analyzer (`bootstrap_attempts` = 2),
  because a null mapper is not cached (`TransientProgramProperties.java:107-110`).
- **OBSERVATION: absent build info is a distinct route.** esbuild 0.27.7 has
  no `\xff Go buildinf:` record (REA `build_info: null`). The independent
  `tools/buildinfo-probe.py` whole-file scan agrees. Ghidra still selected the
  golang compiler spec, which comes from section names, not build info. It
  logged no version, untested, invalid or bootstrap line, and both analyzers
  failed to get a mapper. The hand prediction matched.
- **OBSERVATION, unpredicted: in-range bootstrap is not full recovery.** On
  aether (fallback route), the mapper bootstrapped and found 6115 types. Then
  `GolangSymbolAnalyzer` logged
  `Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException`,
  caused by `java.io.EOFException: Unable to read past EOF: 17645861, 111938854`
  during interface-type markup (`runs/pro-aether/logs/*/ghidra.log:97-177`).
  Go string recovery still ran (`Go strings found: 7200`). Cause: **UNKNOWN**.
  This run does not show that the 1.25.0 fallback data caused it.
- **OBSERVATION: the REA analyze Evidence ID repeated.** `calib-shfmt`
  (`ev_2b29a1dd…`) and `calib-esbuild-0.25.12` (`ev_391dbfe6…`) reproduced
  the pilot IDs exactly, about 30 minutes apart. This is consistent with the
  r5/r9 content+params-keyed `analyze` identity (QUALITY #15). It is one
  repetition, not a determinism proof.

## Decision table (installed Ghidra 12.1.4, REA 6.5.0, Linux x86-64 ELF)

| Log signal (GoApiSnapshot / GoRttiMapper) | Means | Does not mean |
|---|---|---|
| `Using Go API snapshot for X` from **GoApiSnapshot** | Base JSON found and selected patch = requested patch (exact diff or patch 0) | Which file bytes were read, or that the patched content is correct |
| `Falling back from X to Y for Go API snapshot` | Base found and a lower patch (or the base) was used | That X's API equals Y's |
| `Using Go API snapshot for version X` from **GoRttiMapper** | Snapshot valid; X is the **request** echo | Exact selection (it appears after a fallback too) |
| `Untested Go version [X]` + no snapshot line + `Missing Go bootstrap type info` | No installed base for X's minor (this installation: 1.26.x, 1.27.x) | That the range check stopped analysis (it only logs), or that the binary layout changed |
| Only `Reading Go binary info` + analyzer `unable to get GoRttiMapper` | No build-info record (or no fallback version) | That the file is not Go |
| Bootstrap OK, then `Go analysis failure …` | Symbol markup aborted after bootstrap | That RTTI types or strings were not recovered |

## Inference (labelled)

- INFERENCE: on this host, the declared range and the installed bases cover
  the same minors (1.15–1.25), so an out-of-range carrier always lacks a base.
  These runs cannot separate the advisory range check from the missing base. The
  source can: `GoRttiMapper.java:170-172` only logs. A layout change in Go
  1.26/1.27 is neither shown nor excluded, because the failure happens in the
  constructor, before any moduledata read.
- INFERENCE: the historical `op` 2.40.0 recovery loss (r4-10, r14) belongs to
  the same missing-base class **only if** that build was go1.26.x. That package
  is no longer installed, so its cause stays UNKNOWN. The current `op`
  2.41.0-1 (go1.26.8) is a different binary.

## Not examined

- Patched-content correctness, which diff bytes Ghidra applied, and arch-bucket
  retention: none of these is logged.
- Other providers, REA versions, Ghidra versions, OS/arch or file formats: all
  eight carriers are x86-64 Linux ELF.
- Determinism beyond one run per carrier.
- Procedure-name inventories: no `search` was run. `procedure_count` /
  `string_count` from `analyze` are totals, not Go-recovery rates.
- Log completeness: polling copies can miss lines written in REA's last
  ≤0.5 s + kill window. Every Go line precedes the bridge script, so all Go
  lines were captured. Absence claims hold only up to the last retained line.
