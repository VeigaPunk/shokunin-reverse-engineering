# RevEsbuildBuildinfo — 0.27.7 has no buildinfo record; REA's null is correct

author: KaidokuR17.RevEsbuildBuildinfo-3 (revenger); 2026-10-20
scope: read-only. No REA analyze/search/decompile, no Ghidra, no carrier execution, no installs,
no subagent dispatch. Only `rea inspect-go-binary` and byte-level reads of the two carriers.
Axes: **calibration** (is REA misparsing Go 1.25?) and **depth** (why the record is absent, down to the
producer's build recipe).

## Answer

- **Observation.** The 0.27.7 ELF contains **zero** occurrences of the 14-byte `\xff Go buildinf:` magic and
  **no `.go.buildinfo` section** in its section table. REA 6.5.0 therefore takes its documented
  "no header found" path and returns `build_info: null` (rendered as empty go_version). This is not a parse
  failure: a parsed-but-empty header would raise `malformed` (`GoBinaryImage.js:75`).
- **Inference (high confidence).** esbuild's release recipe since v0.27.0 builds the shipped binaries with a
  *locally patched Go toolchain* that comments out the linker call `ctxt.buildinfo()`, so the `go:buildinfo`
  symbol is never emitted. The `runtime.buildVersion` / `runtime.modinfo` strings are still written by
  unpatched `addstrdata1` calls, so the binary still "looks Go" but has no buildinfo record to index them.
- **Net:** the 0.25.12 vs 0.27.7 difference is producer-side metadata suppression, not an REA defect and not
  a Go 1.25 format change.

## 1. REA side — null is the designed result when the magic is absent

Local REA 6.5.0 source (`$REA = ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist`):

| anchor | behavior |
|---|---|
| `go/GoElfImage.js:105-121` | selects a search window only for an allocated section named exactly `.go.buildinfo` |
| `go/GoElfImage.js:137` | with no such section, searches the `fallback` list instead |
| `go/GoElfImage.js:55,78` | `fallback` = file-backed PT_LOADs with `(flags & 3) === 2` (writable, non-exec) |
| `go/GoBinaryImage.js:7` | `MAGIC = ff20476f206275696c64696e663a` (`\xff Go buildinf:`) |
| `go/GoBinaryImage.js:19-36` | scans each window; **no match → `build_info: null`** |
| `go/GoBinaryImage.js:145-165` | `findHeader` requires the magic at a 16-byte-aligned virtual address |
| `go/GoBinaryImage.js:75` | a *parsed* empty version is `GoBinaryFormatFailure("malformed", …)` |
| `go/GoBinaryProvider.js:129` | emits the observed limitation: "No recognized Go build-info record was found …; absent metadata does not establish that the binary is not Go." |

Running the CLI (`npx -y rea-agents@6.5.0 inspect-go-binary …`) on 2026-10-20:

| carrier | REA normalized result |
|---|---|
| esbuild 0.27.7 | `build_info: null` + the limitation at `GoBinaryProvider.js:129` |
| esbuild 0.25.12 | `header_offset: 10027008` (0x990000), `encoding: inline`, `go_version: go1.23.12`, module 762 B |
| notesmd-cli (stock Go 1.25.8) | `go_version: go1.25.8`, header 4308992 (0x41c000) |
| aether (Go 1.25.14) | `go_version: go1.25.14` |
| captree (Go 1.26.1, `-X:nodwarf5`, external link) | `go_version: go1.26.1-X:nodwarf5` |

The last three refute "REA cannot parse Go ≥1.25": the same parser decodes Go 1.25.8, 1.25.14, and 1.26.1
records normally.

## 2. Carrier bytes — 0.27.7 has no record; 0.25.12 has a textbook one

Paths (abbreviated below as `E27` / `E25`):
`E27 = /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/bin/esbuild`
`E25 = /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild`

Observations (whole-file scans + ELF header parse):

| fact | E27 (0.27.7) | E25 (0.25.12) |
|---|---|---|
| size / sha256 | 11,120,788 / `c638273f…2ba14b` | 10,358,936 / `bab29b2c…ced7014` |
| `\xff Go buildinf:` hits | **0** (also 0 hits for `Go buildinf`) | 1 at file 0x990000 |
| section count | 13 | 14 |
| `.go.buildinfo` | **absent** | off 0x990000, size 0x330, WA; vaddr 0xd90000 |
| `.go.fipsinfo` | off/vaddr 0xa31000/0xe31000, size 0x78 (first RW section) | absent (Go 1.23 era) |
| `.note.go.buildid` / PT_NOTE | absent / no PT_NOTE | off 0xf9c, size 0x64; `file` prints `Go BuildID=…` |
| embedded Go version string | `go1.25.7` once at 0x758588 (.rodata) | `go1.23.12` twice: 0x6fb648 (.rodata) and 0x990021 (buildinfo) |
| module blob | hash-framed `runtime.modinfo` at 0x76b8e0 (`path\t` at 0x76b8f0) | runtime copy at 0x70cac0; buildinfo copy at 0x99002c |
| esbuild version string | `0.27.7` at 0x6769de | (not scanned) |

E25 header at 0x990000 (observed bytes):
`ff20476f206275696c64696e663a` `08` (ptrSize) `02` (flags: inline, little-endian) then 16 zero bytes;
length byte `09` at 0x990020, then `go1.23.12` at 0x990021..0x990029; `fa 05` = varint(762) at 0x99002a;
module bytes at 0x99002c..0x990325; 10 bytes zero padding to the 0x330 section end. This reproduces REA's
`header_offset`/`version_location`/`module_location` exactly (10027008 / 10027041 / 10027052).

E27's first RW PT_LOAD begins at file 0xa31000 (vaddr 0xe31000, filesz 0x69780) and its first section is
`.go.fipsinfo`. `.gopclntab` ends at vaddr 0xe30b38, so there is no hole where a buildinfo section could have
been **removed** without leaving a gap. Stock Go 1.25 layout for comparison (notesmd-cli, Go 1.25.8): the RW
LOAD starts exactly at `.go.buildinfo` (file 0x41c000 / vaddr 0x81c000, size 0x520), then `.go.fipsinfo`
(0x41c520), then `.noptrdata` (0x41c5a0). E27 has the suffix of that layout but not its first section.

Caveat (observation): E27's shstrtab still contains the literal name `.go.buildinfo` (and `.go.fuzzcntrs`,
`.elfdata`), but no section header references them. E25's shstrtab likewise contains `.elfdata` with no such
section, so these are linker-fixed names, not evidence of a removed section.

## 3. Producer chain — esbuild patches the Go linker from v0.27.0 onward

All upstream anchors read at the named tags on 2026-10-20:

| anchor | statement |
|---|---|
| `https://github.com/evanw/esbuild/blob/v0.27.7/Makefile#L58-L82` | `go-compiler` target: "Build a custom version of the Go compiler that omits buildinfo from the final executable (since there is no command-line option to disable this)"; line 81 `sed "s/ctxt.buildinfo/\\/\\/ctxt.buildinfo/" main.go`; lines 80–82 then `make.bash` |
| `Makefile#L11` | `GO_FLAGS += "-ldflags=-s -w -buildid=" -buildvcs=false` |
| `Makefile#L359,L363-L364` | `platform-internal` builds with `$(GO_COMPILER)`; `platform-linux-x64: version-go go-compiler` |
| `https://github.com/evanw/esbuild/blob/v0.27.7/.github/workflows/publish.yml#L58,L73` | release runs `make platform-all`, then `make publish-all` |
| `https://github.com/evanw/esbuild/blob/v0.27.7/go.version` | `1.25.7` (matches the `go1.25.7` string in E27) |
| `https://github.com/evanw/esbuild/blob/v0.25.12/Makefile#L5,L336-L341` | 0.25.12 has only `-ldflags=-s -w` and plain `go build`; **no** `go-compiler` target |
| `https://github.com/evanw/esbuild/blob/v0.25.12/go.version` | `1.23.12` (matches E25's buildinfo) |
| `https://github.com/evanw/esbuild/blob/v0.27.0/CHANGELOG-2025.md#L188` | v0.27.0 updates Go 1.23.12 → 1.25.4; the `go-compiler` target first appears in the v0.27.0 Makefile (grep: v0.26.3 = 0 matches, v0.27.0 = 3) |

Go side (`go1.25.7` source):

- `src/cmd/link/internal/ld/main.go:427` calls `ctxt.buildinfo()`; the esbuild sed turns this call into a comment.
- `src/cmd/link/internal/ld/data.go:2436-2465` is `(*Link).buildinfo`: it creates `go:buildinfo`, writes the
  magic at 2444–2448, and appends the version/modinfo strings (2458–2459). With line 427 commented out, the
  symbol is never created — hence no magic and no `.go.buildinfo` section.
- The strings themselves are set independently: `main.go:192` `addstrdata1(ctxt, "runtime.buildVersion="+buildVersion)`
  and `ld.go:91` `addstrdata1(ctxt, "runtime.modinfo="+s)`. That is why `go1.25.7` and the framed modinfo blob
  survive in `.rodata` at 0x758588 / 0x76b8e0. **Inference** (supported by both source sites and the observed
  strings): the retained strings are the unpatched runtime string data, not leftover buildinfo.
- `fips140.go:501-504` documents normal placement: the FIPS info is "near the start of the data segment,
  right after go:buildinfo". E27's `.go.fipsinfo` is at the start of the data segment, consistent with the
  preceding symbol never having been emitted.

Provenance check: the local E27 file is byte-identical to the binary inside the official npm tarball
(`sha256 c638273f…` matches `tar -xzO package/bin/esbuild` streamed from
`https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.27.7.tgz`), and that tarball's sha512 equals
npm's `dist.integrity` (`hzznmADP…`). So the absence is shipped-artifact reality, not local corruption.

## 4. Counter-hypotheses tested and rejected

| hypothesis | discriminating observation |
|---|---|
| REA fails on the Go 1.25 format | same parser returns go1.25.8, go1.25.14, go1.26.1 records; Go 1.25 inline format is unchanged (flags 0x2, ptrSize 8) |
| Magic moved or was re-encoded in Go 1.25 | stock Go 1.25.8 / 1.25.14 binaries carry `.go.buildinfo` with the magic at the start of the RW segment; Go 1.25.7 source still writes it at `data.go:2444-2448` |
| A post-link `strip`/`objcopy` removed the section | no residual gap: E27's RW segment starts at `.go.fipsinfo`; a removal that preserves virtual layout would leave fipsinfo at its original vaddr (0xe31000 + buildinfo size) plus a zero gap at the segment start. E27 shows fipsinfo at the segment start, i.e. the bytes were never laid out; the Makefile documents a linker patch instead |
| `-buildid=` alone caused the absence | the buildinfo symbol is written unconditionally from `ctxt.buildinfo()` (`data.go:2436-2442`) and never consults `flagBuildid`; `-buildid=` (Makefile#L11) is a separate recipe change. E25's Makefile does not pass `-buildid=` yet its binary has both the note and buildinfo; E27's Makefile changes two independent things, and only the linker patch explains the missing buildinfo |
| Binary is non-Go / malformed | `.gopclntab` (0x2ad458), `.go.fipsinfo`, 2,339 occurrences of the `github.com/evanw/esbuild` module prefix, `go1.25.7`, and a valid Go 1.25 ELF layout; REA's own limitation says absence ≠ non-Go |
| Go 1.26 `.go.module` means buildinfo moved | `.go.module` is the moduledata section added by Go 1.26 (golang/go#76038, CL 720660); esbuild 0.28.2 (Go 1.26.5, `~/Projects/tog/node_modules/@esbuild/linux-x64/bin/esbuild`) has `.go.module` but still zero buildinfo magic, consistent with the same sed at `v0.28.2/Makefile#L58-L83` |

## 5. Consequences for this round

- `contract.md:98-104` requires `buildinfo-probe.py` to exit 0 with `found:false` when no magic exists.
  esbuild ≥0.27.0 is exactly that case; a `found:false` on E27 is **correct output**, not a tool failure.
  A tool that instead fabricates a version from the rodata string would be wrong.
- `carrier-census.py` (`contract.md:110-113`) will record `go_version: null` for E27 since it delegates to REA;
  calibrate the C2 prediction table accordingly (an in-range Go carrier can legitimately have no record).
- If Go-version attribution of esbuild ≥0.27.0 is needed, the only direct surviving version string is the
  link-time `go1.x.y` constant in `.rodata` (E27: 0x758588, a single occurrence, `main.go:188-192`), not a
  dependency/authenticity attestation; it can be stripped independently.
- REA needs no change for this input. A future parser *could* scan `.rodata` heuristically, but that would
  invent a record Go itself no longer writes; the current `null` + limitation text is the honest result.

## Confidence / falsifiers

- **Observed:** all offsets, section facts, magic counts, REA outputs, npm tarball/identity hashes.
- **Inference (high):** the sed at `Makefile#L81` is the cause of the absent record; not reproduced by building
  a patched toolchain (no Go toolchain installed; building is out of scope). Falsifier: a stock-Go 1.25.7 build
  of the same source also lacking buildinfo, or an official 0.27.7 artifact built through a non-`go-compiler`
  path — neither observed.
- **Inference (high):** retained `go1.25.7`/modinfo strings come from the unpatched `addstrdata1` calls; the
  binary has no symbol table to trace the reference directly.
- **Not verified:** the other 0.27.x platform binaries; the same tagged Makefile/provenance is inferred, only
  0.27.7 linux-x64 was byte-inspected here.
