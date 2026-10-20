# Scout — Go `debug/buildinfo` docs and source (r17 w1)

Question: ground a SOURCES row for Go's build-info blob and `GoVersion` that can carry
C2's carrier-diagnostics claims, with a durable revision, access date, a ≤25-word quote,
and a learner benefit. Tier per corpus contract v1 (`/home/vgpnk/Projects/shokunin/CORPUS.md:66`,
tier definitions `:93-97`). Read-only; no carrier executed, no REA analysis, no installs.

## Opened (observation, access date 2026-10-20, fetch 13:33 UTC)

| target | URL | HTTP | bytes | identity observed |
|---|---|---|---|---|
| package docs | https://pkg.go.dev/debug/buildinfo | 200 | 50,986 | page declares `Version: go1.27.3`; renders Overview, `type BuildInfo`, `Read`, `ReadFile`; **0** occurrences of `GoVersion` |
| source browser | https://go.dev/src/debug/buildinfo/buildinfo.go | 200 | 78,364 | page declares no version; source line ids 1–586 plus empty `L587` |
| pinned source | https://raw.githubusercontent.com/golang/go/go1.27.3/src/debug/buildinfo/buildinfo.go | 200 | 16,658 | 586 lines, SHA-256 `5e4064efa60e5fb768ffbf49f44bb6dd037fe35d3245ba9573881adef2f9c097` |
| patch tag | https://raw.githubusercontent.com/golang/go/go1.27.2/src/debug/buildinfo/buildinfo.go | 200 | 16,658 | same SHA-256 as go1.27.3 (byte-identical file) |
| dev tip | https://raw.githubusercontent.com/golang/go/master/src/debug/buildinfo/buildinfo.go | 200 | 16,658 | same SHA-256 at access (no drift) |
| canonical blob page | https://github.com/golang/go/blob/go1.27.3/src/debug/buildinfo/buildinfo.go | 200 | — | human-viewable pin for the row |

At every cited line the `go.dev/src` render matched the tag: `:55-58` magic comment/literal,
`:60-63` consts, `:70` `errors.AsType`, `:191-203` offsets/flags, `:224-230` inline branch,
`:337-401` `searchMagic`, `:586` final line. This is anchor-level agreement, not a full-file
diff of the HTML render.

## Recommended SOURCES row (S024 at baseline; L1 assigns if siblings also propose rows)

Baseline `corpus/SOURCES.md` ends at S023. Row text, ready to paste:

| S024 | Go 1.27.3 `debug/buildinfo` source — https://github.com/golang/go/blob/go1.27.3/src/debug/buildinfo/buildinfo.go | code | A | The on-disk build-info blob format in Go 1.27.3: magic, fixed header, flag bits, and version extraction | Tag `go1.27.3`; file SHA-256 `5e4064efa60e5fb768ffbf49f44bb6dd037fe35d3245ba9573881adef2f9c097`; `src/debug/buildinfo/buildinfo.go:55-58`, `:60-63`, `:191-203`, `:224-230` | A reader must accept only 16-byte-aligned magic, then decode a fixed 32-byte header before the varint version string. | queued | 2026-10-20 | on-release | — |

Field notes:

- `kind: code`, `tier: A` — source code is named primary/authoritative for its scope in
  `CORPUS.md:93-97`; the scope cell limits it to the blob format, not to REA, Ghidra, or
  any carrier's provenance. No `community` inflation risk.
- `status: queued`, `used-by: —` — the r17 knowledge entry does not exist yet. Marking
  `mined` against a planned path would trip the fleet check at `CORPUS.md:147` ("mined rows
  whose used-by paths do not exist — must print nothing"). Flip to `mined` with
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` only after that entry lands
  and cites this row.
- The anchor carries the file hash because a tag is a mutable ref; the hash pins the bytes.
  The tag alone would still be acceptable; the hash makes the row cheap to re-verify.

## Gate quote (round lesson `## Gate`)

Location: `src/debug/buildinfo/buildinfo.go:55-57`, tag `go1.27.3`, accessed 2026-10-20.

> The build info blob left by the linker is identified by a 32-byte header, consisting of buildInfoMagic (14 bytes), followed by version-dependent fields.

23 contiguous words (three comment lines joined). The literal itself is `:58`:
`var buildInfoMagic = []byte("\xff Go buildinf:")` — 14 bytes, matching the comment.

Screened but not used as the anchor: pkg.go.dev Overview ¶, 16 words —
"Package buildinfo provides access to information embedded in a Go binary about how it was
built." It grounds the API's purpose only; it says nothing about magic, header, flags, or
the `GoVersion` field (0 hits), so it cannot ground the probe.

## Source model → `W/tools/buildinfo-probe.py`

All anchors at tag `go1.27.3`; observation from the pinned file.

| Probe requirement (contract) | Anchor | Observed content |
|---|---|---|
| magic `\xff Go buildinf:` | `:55-58` | 14-byte magic; header is 32 bytes |
| 16-byte alignment constant | `:61` | `buildInfoAlign = 16` |
| fixed header size | `:62`, `:181`, `:187` | `buildInfoHeaderSize = 32`; short header → `errNotGoExe` |
| ptr size at 0-based offset 14 | `:192` | `ptrSizeOffset = 14` |
| flags at 0-based offset 15 | `:193` | `flagsOffset = 15` |
| first pointer at 0-based offset 16 | `:194` | `versPtrOffset = 16`; second pointer at 16+ptrSize |
| endianness bit 0x1 | `:196-198`, `:241-247` | little `0x0`, big `0x1` |
| inline-string bit 0x2 | `:200-202`, `:229` | `flagsVersionInl = 0x2`; branch on `flags&0x2 == 0x2` |
| Go ≥1.18 inline layout | `:205-207`, `:224-230`, `:284-318` | version string at `addr+32`, then modinfo at the returned address; each is Uvarint-length-prefixed |
| aligned search semantics | `:335`, `:347`, `:353-372`, `:384-400` | round start up to 16; 1 MiB chunks; misaligned hit is skipped, not accepted |
| header must fit after magic | `:388-390` | else `errNotGoExe` |
| pre-1.18 pointer format | `:238-257`, `:320-333` | stored pointers are target virtual addresses resolved through `DataReader`; a file-offset-only reader cannot follow them, so the contract's "report `pointer_format` and stop" is source-consistent (inference about the probe, observation of the code) |
| `GoVersion` source | `:97` | `bi.GoVersion = vers` after `debug.ParseBuildInfo(mod)`; version is the blob string, not modinfo |
| module framing strip | `:262-268` | 16-byte sentinels; comment names `modload.infoStart`/`infoEnd` |
| empty version rejected | `:259-261` | `vers == ""` → `errNotGoExe` |

Depth note cross-file: the `GoVersion` field itself is declared in
`src/runtime/debug/mod.go:42-44` at the same tag ("the version of the Go toolchain that
built the binary"), and `debug.ReadBuildInfo` injects `runtime.Version()` at `:31-35`
because the version is "stored separately" and "ParseBuildInfo does not recognize it".
That explains why a blob reader and the stdlib agree on `GoVersion` for the same file.

## Calibration notes (observation vs inference)

1. **pkg.go.dev cannot anchor the format** (observation). Its rendered text has 0
   occurrences of `GoVersion` and no magic/header/flag text; it documents only the package
   overview, `type BuildInfo`, `Read`, and `ReadFile`. A row anchored there would support
   "the API exists", not "the blob is shaped like this".
2. **`go.dev/src` is unversioned in page text** (observation). Its cited lines matched tag
   `go1.27.3` and `master` at access, but the page itself names no revision. Use it for
   reading; anchor to the tag.
3. **Line count artifact** (observation). The reader's page footer reported "617" lines
   while the file is 586 (`wc -l`) and the HTML ids stop at `L587` (empty trailer). Do not
   cite 617 as a source line count. The pinned file is 586 lines.
4. **Patch-tag stability** (observation). `go1.27.2`, `go1.27.3`, and `master` are
   byte-identical for this file (same SHA-256), so `on-release` recheck costs one hash.
5. **No normalization in this package** (inference from `:97`, `:112-270`). `Read` assigns
   the blob's `vers` verbatim and `readRawBuildInfo` contains no normalization step.
   Therefore a `-X:nodwarf5`-style suffix in REA `go_version` is consistent with a verbatim
   toolchain string; this file does not prove REA reads this field or preserves it.
6. **Scope honesty**: nothing here establishes REA 6.5.0 behavior, Ghidra's Go gate, or that
   any carrier contains this blob. It grounds only the reader-side format.

## Search log line for `corpus/SOURCES.md` (rule 5, optional for L1)

2026-10-20 — Question: which canonical, version-pinned source grounds the Go build-info
blob magic/format and `GoVersion` for a stdlib-only probe? Opened `pkg.go.dev/debug/buildinfo`,
`go.dev/src/debug/buildinfo/buildinfo.go`, raw `golang/go` at `go1.27.3`, `go1.27.2`, and
`master` for `src/debug/buildinfo/buildinfo.go`, plus `go1.27.3/src/runtime/debug/mod.go`.
Identified 7 URLs, screened 2 distinct sources, included 1 (tag `go1.27.3` source), excluded 1
(pkg.go.dev: API surface only, 0 `GoVersion` occurrences, no format text). Stop: the
reader-side format and `GoVersion` extraction are anchored; producer-side linker code and
provider behavior are out of scope.

## Limits / remaining unknowns

- No local Go toolchain: `command -v go` exited 1 with no output, so there is no GOROOT
  copy to cross-check. Verification is tag-vs-patch-tag-vs-master-vs-`go.dev` render, plus
  SHA-256.
- `pkg.go.dev` `Version: go1.27.3` is a moving "latest" declaration, not durable; the tag
  is the anchor.
- No TLS or transparency-log verification; only HTTP 200 plus content hashes.
- The producer (`cmd/link/internal/ld` buildinfo writer) and `debug.ParseBuildInfo` were not
  opened. Sentinel framing is known only from the reader's strip logic and its comment
  (`:262-268`), so the writer-side layout remains inference.

## Installs

None.
