# Draft SOURCES rows S024–S029 — round 17 (DraftSourcesRows)

Draft only. Not written to `corpus/SOURCES.md`. Contract v1 cell order (11 columns). Every row below was opened by this author on 2026-10-20 (UTC). New rows are `queued` because no knowledge entry or lesson cites them yet; L1 changes `status` to `mined` and fills `used-by` when a citing path exists (CORPUS.md rule 2; census awk at CORPUS.md:145-147).

Byte pins for the line anchors (sha256 of the bytes this author read):
- Go 1.27.3 toolchain tarball `https://go.dev/dl/go1.27.3.linux-amd64.tar.gz` — `65efbc80fdc1fa2cd2631cad5b481777a68e8725f34e89f50fc6ac714e379b40` (equals the `go.dev/dl/?mode=json` value; extracted to `/home/vgpnk/.local/opt/go-1.27.3`).
- `https://go.dev/doc/devel/release` HTML snapshot — `d9a4b0ebb8eed5e50b092d5360d811b6dd89a21cb2518f5953bcc12f744d8968` (line numbers below are snapshot lines).
- `https://go.dev/doc/go1.27` HTML snapshot — `a4c56ba584ac26614537ac40bf07aa638314decdacf32ea96acb60dbfe57393e` (snapshot lines).
- Ghidra `GoRttiMapper.java` at tag `Ghidra_12.1.4_build` — `2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95`; at `master` — `0712837a21754b42d3b2deb19ef5e37d829ea5ea87dd59a4232445f67d7c36cd`.
- GP-6528 commit patch `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch` — `f44945bc879d46f2e16624f7823246416d625229e57930db13a040862c170538`.
- Ghidra releases feed `https://github.com/NationalSecurityAgency/ghidra/releases.atom` — `bc07390b13fe108dd8c15db5df6896545af8ab2c3f3f2b0890ab18b2231b9a03`.

## Rows

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S024 | Go `debug/buildinfo` reader — https://go.dev/src/debug/buildinfo/buildinfo.go (master view; same line numbers in pinned go1.27.3 `src/debug/buildinfo/buildinfo.go`) | code | A | How Go's own stdlib reader finds and decodes the build-info blob: magic, flags, inline version and modinfo strings, and the version it returns | go1.27.3 `buildinfo.go:58` magic; `:97` `bi.GoVersion = vers`; `:200-202` flag constants; `:224-227` inline-format comment; `:229-237` inline decode; `:262-268` modinfo framing | Gives the reference decoder to check a version-string reader against: the version is returned raw, including any `X:` experiment token; the stdlib does not strip it. | queued | 2026-10-20 | on-release | — |
| S025 | Go Release History — https://go.dev/doc/devel/release | docs | A | Official stable Go toolchain names, release dates, and the support rule, for dating a carrier's toolchain against the release train | snapshot `go-release.html` (sha256 d9a4b0eb…): `:464` support policy; `:474` `go1.27.0 (released 2026-08-19)`; `:525-527` `go1.27.3 (released 2026-10-19)`; `:750-751` `go1.26.10 (released 2026-10-19)` | Places 1.27.0 as the first 1.27 minor (2026-08-19) with 1.27.x and 1.26.x patches shipping after it; a carrier built with any 1.27.x is outside Ghidra 12.1.4's declared range (S029). | queued | 2026-10-20 | on-release | — |
| S026 | Go linker build-version suffix — `src/cmd/link/internal/ld/main.go:191-198` and `src/internal/buildcfg/exp.go:79-84, 157-161` (go1.27.3 tarball) | code | A | How a toolchain built with non-default GOEXPERIMENT writes `X:<exp>` into `runtime.buildVersion`, the separator it uses, and which flags are listed | `main.go:191-197` `buildVersion += sep + "X:" + goexperiment`; `main.go:193-196` dash separator when the version has no `-`, citing go.dev/issue/75953; `exp.go:157-160` `String()` elides baseline flags; `exp.go:79-84` baseline `Dwarf5` default | Explains `go1.27.0-X:nodwarf5` as the baseline-relative experiment list after a dash: an `X:` token marks a non-default toolchain build and is not part of the release number. | queued | 2026-10-20 | on-release | — |
| S027 | golang/go issue #75953, "go/version: does not support the `X:` suffix from `go env GOVERSION`" — https://github.com/golang/go/issues/75953 (accessed 2026-10-20; closed; milestone Go1.26) | docs | B | Maintainer discussion of why the space-separated `X:` form breaks `go/version`, and the dash-separator proposal; rationale only, not normative | issue Description section; comment by dmitshur, 2025-10-17 (activity item 6): proposal to use `go1.25.3-X:nodwarf5` | Records that the space form is the defect and the dash form is the chosen repair; shipped behavior is taken from S026 source. Tier B because it is a tracker thread, not a spec. | queued | 2026-10-20 | 365d | — |
| S028 | Go 1.27 Release Notes — https://go.dev/doc/go1.27 | docs | A | Official GOEXPERIMENT opt-out names and experiment removals announced in 1.27, the flag names that can appear as `X:` tokens | snapshot `go-1.27.html` (sha256 a4c56ba5…): `:584` `GOEXPERIMENT=nosizespecializedmalloc` opt-out; `:610` `goroutineleakprofile` experiment deleted; `:684-685` `GOEXPERIMENT=nojsonv2` opt-out. Case-insensitive `dwarf` search of the snapshot: zero matches | Documents two 1.27 opt-outs with announced removal, and shows the release notes do not document `nodwarf5`, so a `nodwarf5` token must be matched to S026 source rather than to a published flag. | queued | 2026-10-20 | on-release | — |
| S029 | Ghidra upstream Go version range — `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` at tag `Ghidra_12.1.4_build` (`GoVerRange.parse("1.15-1.25")`) and at `master` (`"1.15-1.26"`); releases feed https://github.com/NationalSecurityAgency/ghidra/releases.atom | code | A | Which Ghidra release declares Go 1.26 support versus master only, so release-status claims about Go 1.26/1.27 recovery stay separate from upstream commits | tag `:79` `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`; master `:79` `"1.15-1.26"`; GP-6528 patch lines 150-151 (`-…"1.15-1.25"` / `+…"1.15-1.26"`); releases feed newest entry `Ghidra 12.1.4`, 2026-09-21T17:38:59Z | The only release observed (12.1.4, 2026-09-21) declares 1.15–1.25, so the GP-6528 1.26 range is master-only as of 2026-10-20; no Ghidra release observed declares 1.27. | queued | 2026-10-20 | on-release | — |

## Gate — located quotes (≤25 words each; for the round-17 lesson `## Gate`)

| id | URL | access date | located quote (≤25 words) | location |
|---|---|---|---|---|
| S024 | https://go.dev/src/debug/buildinfo/buildinfo.go | 2026-10-20 | `var buildInfoMagic = []byte("\xff Go buildinf:")` | buildinfo.go:58 |
| S024 | https://go.dev/src/debug/buildinfo/buildinfo.go | 2026-10-20 | Since 1.18, the flags version bit is flagsVersionInl. In this case, | buildinfo.go:224 (comment) |
| S024 | https://go.dev/src/debug/buildinfo/buildinfo.go | 2026-10-20 | `bi.GoVersion = vers` | buildinfo.go:97 |
| S025 | https://go.dev/doc/devel/release | 2026-10-20 | go1.27.0 (released 2026-08-19) | snapshot line 474 (`id="go1.27.0"`) |
| S025 | https://go.dev/doc/devel/release | 2026-10-20 | go1.27.3 (released 2026-10-19) | snapshot lines 525-527 |
| S025 | https://go.dev/doc/devel/release | 2026-10-20 | Each major Go release is supported until there are two newer major releases. | snapshot line 464 (Release Policy) |
| S026 | https://go.dev/src/cmd/link/internal/ld/main.go (tarball go1.27.3) | 2026-10-20 | `buildVersion += sep + "X:" + goexperiment` | main.go:197 |
| S026 | https://go.dev/src/cmd/link/internal/ld/main.go (tarball go1.27.3) | 2026-10-20 | `if !strings.Contains(buildVersion, "-") { // See go.dev/issue/75953.` | main.go:194 |
| S026 | https://go.dev/src/internal/buildcfg/exp.go (tarball go1.27.3) | 2026-10-20 | (Experiments in the same state as in the baseline are elided.) | exp.go:158 |
| S027 | https://github.com/golang/go/issues/75953 | 2026-10-20 | However, the `X:` suffix form is not supported by `go/version` | issue Description section |
| S027 | https://github.com/golang/go/issues/75953 | 2026-10-20 | A simple change might be to replace the space with a dash, like "go1.25.3-X:nodwarf5". | comment by dmitshur, 2025-10-17 (activity item 6) |
| S028 | https://go.dev/doc/go1.27 | 2026-10-20 | You may set GOEXPERIMENT=nosizespecializedmalloc at build time to disable | snapshot line 584 (Faster memory allocation) |
| S028 | https://go.dev/doc/go1.27 | 2026-10-20 | may disable it by setting GOEXPERIMENT=nojsonv2 at build time, | snapshot lines 684-685 (encoding/json/v2) |
| S029 | https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/Ghidra_12.1.4_build/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | 2026-10-20 | public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25"); | line 79 (tag) |
| S029 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch | 2026-10-20 | +	public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26"); | patch line 151 (GP-6528, 2026-03-03) |

## Notes for L1

- S004 (already in SOURCES) is the GP-6528 commit itself; S029 adds the release-status question. Do not treat S004 as release evidence.
- Installed `Base-src.zip` (S003) and installed 12.1.4 `docs/ChangeHistory.md` (S007) contain no Go 1.26 entry (`grep` for `1\.26|1\.27` returned none); installed `data/typeinfo/golang/` holds only `go1.25.0.json` among 1.25–1.27 files. These are S003/S007/S023 facts, not new rows.
- Range consequence for C2 carriers: with Ghidra 12.1.4's declared `1.15-1.25`, an in-range carrier must be built with Go ≤1.25.x. The pilot esbuild (go1.23.12) is in range; the pilot shfmt (go1.27.0) is out of range.
- Quote-to-row check: each quote above is copied verbatim from the snapshot or source file named in its location column; the snapshot files are in `/tmp/kr17-ghidra/` and `/tmp/kr17-src/` (not committed).
