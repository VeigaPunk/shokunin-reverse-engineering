# ScoutGoExperimentSuffix — official Go source for the `-X:nodwarf5` version suffix

Author: `KaidokuR17.ScoutGoExperimentSuffix-3` (scout), 2026-10-20. Read-only.
Axes named: **calibration** (separate the semantic Go version from a producing-toolchain
marker before any snapshot/range mapping) and **depth** (linker construction → embedded
string → `runtime.Version()` → `runtime/debug.BuildInfo.GoVersion` → `go version <binary>`).

Scope: no REA analyze/search/decompile, no Ghidra, no carrier execution, no installs, no
carrier touched. I fetched the official Go 1.27.2 source tarball from `go.dev/dl` and read
tag files through `go.googlesource.com` / `raw.githubusercontent.com` (official `golang/go`
mirror). Everything below is **observation** unless marked **[INFERENCE]**.

Question: where does official Go source/doc explain the `-X:nodwarf5` suffix seen in
`runtime.Version()` / build-info `GoVersion`?

## Answer in one paragraph

Observation: the Go **linker** appends `X:<GOEXPERIMENT>` to `runtime.buildVersion` when the
linker's effective GOEXPERIMENT set differs from the platform baseline
(`src/cmd/link/internal/ld/main.go:191-199`), and `runtime.Version()` returns that string
verbatim (`src/runtime/extern.go:362-377`). Since CL 719701 (commit `9daaab3`, Go 1.26),
the separator is `-` when the base version contains no hyphen and a space otherwise, so a
release toolchain built with `GOEXPERIMENT=nodwarf5` yields `go1.27.0-X:nodwarf5`.
`nodwarf5` is the experiment-list spelling for "`Dwarf5` disabled relative to baseline"
(`expList` prefixes disabled experiments with `no`, `src/internal/buildcfg/exp.go:182-187`);
DWARF 5 became the baseline in Go 1.25 and
`GOEXPERIMENT=nodwarf5` opts out (`https://go.dev/doc/go1.25#dwarf5-support`). The marker is
meta-information about the building toolchain, not part of the semantic Go version.

## Located chain (tag `go1.27.2`; access date 2026-10-20)

| # | Link in the chain | Anchor (file:line) | Located quote (≤25 words) | Kind |
|---|---|---|---|---|
| 1 | `Dwarf5` is baseline-on except darwin/ios/aix, so `nodwarf5` is a non-default disable | `src/internal/buildcfg/exp.go:76-88`, line 79 | `dwarf5Supported := (goos != "darwin" && goos != "ios" && goos != "aix")` | observation |
| 2 | Disabled experiment names are emitted with a `no` prefix | `src/internal/buildcfg/exp.go:159-189`, line 186 | `list = append(list, "no"+name)` | observation |
| 3 | `Dwarf5` documented as the DWARF-5 switch | `src/internal/goexperiment/flags.go:103-104` | `Dwarf5 enables DWARF version 5 debug info generation.` | observation |
| 4 | Linker builds the version suffix; `-` iff base has no `-` | `src/cmd/link/internal/ld/main.go:191-199`, lines 193-197 | `buildVersion += sep + "X:" + goexperiment` (line 197); `// See go.dev/issue/75953.` (line 194) | observation |
| 5 | `runtime.buildVersion` doc states the `"X:<GOEXPERIMENT>"` inclusion | `src/runtime/extern.go:362-370`, lines 364-365 | `If any GOEXPERIMENTs are set to non-default values, it will include "X:<GOEXPERIMENT>".` | observation |
| 6 | `runtime.Version()` returns it verbatim | `src/runtime/extern.go:372-377` | `It is either the commit hash and date at the time of the build or, when possible, a release tag like "go1.3".` | observation |
| 7 | Linker embeds the same string in `go:buildinfo` | `src/cmd/link/internal/ld/data.go:2643` | `data = appendString(data, strdata["runtime.buildVersion"])` | observation |
| 8 | Blob reader assigns it to `BuildInfo.GoVersion` | `src/debug/buildinfo/buildinfo.go:97` | `bi.GoVersion = vers` | observation |
| 9 | `debug.ReadBuildInfo` injects `runtime.Version()` and documents the field | `src/runtime/debug/mod.go:35`, `:42-44` | `GoVersion is the version of the Go toolchain that built the binary (for example, "go1.19.2").` | observation |
| 10 | The Go tool itself strips the marker before use (cache salt) | `src/cmd/go/internal/cache/hash.go:46-58`, lines 51/54 | `if i := strings.Index(version, "-X:"); i >= 0 {` | observation |
| 11 | `go/version` treats the suffix as a non-standard-toolchain suffix | `src/go/version/version.go:21`; `https://go.dev/doc/toolchain#name` | `Non-standard toolchains use names of the form goV-suffix for any suffix.` | observation |
| 12 | CLI surfaces that print it | `src/cmd/go/internal/envcmd/env.go:126`; `src/cmd/go/internal/version/version.go:87,195` | `{Name: "GOVERSION", Value: runtime.Version()}`; `fmt.Printf("%s: %s\n", file, bi.GoVersion)` | observation |

Separator history (depth):

- `go1.25.4`, `go1.25.5` and `go1.25.14` still do `buildVersion += " X:" + goexperiment`
  (space) at `src/cmd/link/internal/ld/main.go:190` (checked at all three tags: no 1.25
  backport of CL 719701).
- `go1.26.0` has the fixed `sep := " "` / `if !strings.Contains(buildVersion, "-") { sep = "-" }`
  logic at `src/cmd/link/internal/ld/main.go:190-195` at tag `go1.26.0`; `go1.27.0` and
  `go1.27.2` are identical at `:191-199`.
- Change text, commit `9daaab305c4d1dede9e4f6efdc5e1268a69327e6` (CL 719701, Fixes #75953):
  "always put the X: part into the suffix, resulting in, for example, go1.25.0-X:foo."
  (13 words). Issue: `https://go.dev/issue/75953` (redirects to
  `https://github.com/golang/go/issues/75953`); milestone Go1.26.

So: **`-X:` implies the fixing linker (Go ≥ 1.26); the older ` X:` form implies a linker
before CL 719701** — **[INFERENCE]**, modulo a distro backport (issue comment
`https://github.com/golang/go/issues/75953#issuecomment-3507842163` records Fedora shipping
`go1.25.4 X:nodwarf5 linux/amd64`, the space form).

## Calibration points for round-17

1. **Three distinct strings, never merge them**: semantic version `go1.27.0`; producing
   toolchain marker `-X:nodwarf5`; build setting `GOEXPERIMENT=nodwarf5` (observed in the
   carrier's build settings by the r17 `inspect-go-binary` run cited in
   `ScoutGoReleaseHistory.md`). Only the first feeds `M.m.p` selection.
2. **The “explanation” is source-level, not exported API prose**: `pkg.go.dev/runtime?tab=doc`
   has **0** occurrences of `GOEXPERIMENT` / `X:` at access (grep), and `pkg.go.dev/debug/buildinfo`
   documents no `GoVersion` field text. Citing `pkg.go.dev/runtime#Version` for the suffix
   would be citation drift; cite `runtime/extern.go:362-370` at the tag (source comment on
   the unexported `buildVersion`) plus the linker construction site.
3. **`-X:` here is not the linker's `-X name=value` flag**: it is the version-suffix
   separator chosen by `main.go:193-196`; the actual `-X` flag rejects non-string vars at
   `cmd/link/internal/ld/data.go:1264`. Do not describe the suffix as an ldflag.
4. **Go itself strips the marker before semantics**: `cache/hash.go:46-58` strips both
   `" X:"` and `"-X:"`; `go/version` cuts at the first `-`. Any normalizer should reproduce
   that strip, keep the raw string as evidence, and never feed the suffix to snapshot
   selection; whether Ghidra's `GoVer.parse` already does so is the GoVer lane's question
   (pilot log shows `1.27.0`, consistent with stripping).
5. **Contract example vs pilot observation**: `contract.md:64` uses `go1.27.2-X:nodwarf5`
   illustratively; the pinned carrier `/usr/bin/shfmt` reports `go1.27.0-X:nodwarf5`
   (`pilot/README.txt:7`). Use the observed string in prediction tables, not the example.
6. **The suffix is behavioral evidence, not decoration**: the same `buildcfg.Experiment.Dwarf5`
   value that the linker reports in the suffix also selects DWARF-5 emission
   (`src/cmd/link/internal/ld/dwarf.go` has 16 such sites, e.g. `:1172`, `:1219`, `:2359`;
   `src/cmd/compile/internal/ssa/debug.go:1476`). So `-X:nodwarf5` corroborates DWARF-4
   output for that link, unless DWARF was stripped (`-ldflags=-w`) or a nonstandard link
   path applies — **[INFERENCE]** on those caveats; the peer lane observed the matching
   `GOEXPERIMENT=nodwarf5` build setting.
7. **Ghidra already normalizes it**: pilot `shfmt-log/ghidra.log:83,87` logs
   `Untested Go version [1.27.0]`, i.e. the `-X:nodwarf5` suffix did not reach the range
   gate. That is an observation for the Ghidra-side lanes (GoVer lane owns the parser
   source); my source chain explains why the toolchain string can carry it.

## Provenance (access date 2026-10-20)

| Target | URL | Note |
|---|---|---|
| Go 1.27.2 source tarball | `https://go.dev/dl/go1.27.2.src.tar.gz` | 35,134,614 B; SHA-256 `03495da2ba64894d40f5c4992e49454fa78b50690604ff92b6afff5081b76e62`; line anchors above verified in the extracted tree |
| Canonical tag files | `https://go.googlesource.com/go/+/refs/tags/go1.27.2/src/runtime/extern.go#362`, `.../src/cmd/link/internal/ld/main.go#191`, `.../src/internal/buildcfg/exp.go#79`, `.../src/internal/goexperiment/flags.go#103`, `.../src/runtime/debug/mod.go#35`, `.../src/cmd/go/internal/cache/hash.go#46`, `.../src/go/version/version.go#21`, `.../src/cmd/link/internal/ld/data.go#2643`, `.../src/debug/buildinfo/buildinfo.go#97` | official repository; `?format=TEXT` serves base64 when a raw fetch is needed |
| Source browser (unversioned, master) | `https://go.dev/src/runtime/extern.go#L362`, `https://go.dev/src/internal/buildcfg/exp.go#L79` | read support only; page names no revision, and master line numbers differ (quote at `L368-369` on master) |
| Go 1.25 release notes | `https://go.dev/doc/go1.25#dwarf5-support` | quote: `DWARF 5 generation can be disabled by setting the environment variable GOEXPERIMENT=nodwarf5 at build time` (17 words) |
| Toolchain naming doc | `https://go.dev/doc/toolchain#name` | quote: `Non-standard toolchains use names of the form goV-suffix for any suffix.` (13 words) |
| Issue / fix | `https://go.dev/issue/75953`, `https://github.com/golang/go/commit/9daaab305c4d1dede9e4f6efdc5e1268a69327e6` | issue body shows the pre-fix `go1.25.3 X:nodwarf5`; commit message quote above |

Tag corroboration: `go1.27.0` raw tag has the same code at
`src/cmd/link/internal/ld/main.go:191-199`, `src/runtime/extern.go:365,370,375`,
`src/internal/buildcfg/exp.go:79,84` — the carrier's own toolchain train already contains
the `-X:` form.

## Draft SOURCES row (11 columns; id to be assigned by L1)

Baseline `corpus/SOURCES.md` ends at S023; two sibling scouts also proposed `S024`, so L1
must assign the id. Status `queued` now; flip to `mined` only when
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` cites it (same rule the
`ScoutGoBuildinfoDocs` draft states).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | Go 1.27.2 source — https://go.googlesource.com/go/+/refs/tags/go1.27.2/src/runtime/extern.go#362 | code | A | Official Go definition and linker construction of the GOEXPERIMENT marker appended to `runtime.Version()` / `BuildInfo.GoVersion`, not the semantic Go version | tag `go1.27.2` (src tarball SHA-256 `03495da2ba64894d40f5c4992e49454fa78b50690604ff92b6afff5081b76e62`); `src/runtime/extern.go:362-370`; `src/cmd/link/internal/ld/main.go:191-199`; `src/internal/buildcfg/exp.go:79,84,167-189`; commit `9daaab3` (CL 719701) | Treat `-X:<experiment>` (pre-1.26: ` X:`) as a producing-toolchain marker to strip before version parsing; `nodwarf5` records `Dwarf5` disabled relative to baseline. | queued | 2026-10-20 | on-release | — |

If L1 prefers code and documentation separable, the release-note/toolchain-doc pair can be
a second `docs` row; one `code` row is the minimum that grounds the construction.

## Search log line for `corpus/SOURCES.md` (optional, for L1)

2026-10-20 — Question: which official Go source or doc explains the `-X:nodwarf5` suffix in
`runtime.Version()` / build-info `GoVersion`? Opened `go.dev/src` (`runtime/extern.go`,
`internal/buildcfg/exp.go`), tag files at `go1.25.4`/`go1.26.0`/`go1.27.0`/`go1.27.2`/`master`,
`go.dev/doc/go1.25#dwarf5-support`, `go.dev/doc/toolchain#name`, issue 75953, and commit
`9daaab3`; downloaded and hashed the `go1.27.2` source tarball. Screened 2 candidate anchors,
included 1 source (Go 1.27.2 source tree, which states both the inclusion rule and the
separator construction), excluded `pkg.go.dev/runtime` (0 occurrences of `GOEXPERIMENT`/`X:`;
exported doc does not state the suffix). Stop: construction, spelling, separator history, and
downstream `GoVersion` propagation are anchored at tag lines.

## Limits / remaining unknowns

- `go.dev/src` renders an unversioned master snapshot; anchors here are tag-`go1.27.2` line
  numbers from the official tarball, not master line numbers.
- `raw.githubusercontent.com` is a mirror of `golang/go`; I did not verify commit signatures.
  The tarball itself came from `go.dev/dl` and is hashed above.
- Issue 75953 and the commit page are tracker/history, not normative documentation; they are
  cited for the separator change only, with the tag source as the authoritative anchor.
- No local Go toolchain exists on this host (`go` is not installed), so I could not run
  `go version`/`go env` myself; the carrier string is taken from `pilot/README.txt:7` and the
  peer lane's `inspect-go-binary` evidence, not re-run here.
- I did not inspect Ghidra's `GoVer.parse`; the `1.27.0` log normalization is cited as an
  observation only (the GoVer lane owns that source).
- The pilot's `shfmt.json` is REA `analyze` output and has no `build_info` key; the
  `go_version` string in `pilot/README.txt` comes from a separate `inspect-go-binary` call
  (peer evidence `ev_f8ef12a8…`), which I did not re-execute.

Installs/updates: none.
