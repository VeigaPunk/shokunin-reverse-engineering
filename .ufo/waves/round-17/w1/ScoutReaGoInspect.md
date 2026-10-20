# Scout — REA `inspect-go-binary` (provider `go-build-info`): how `go_version` is derived, and why esbuild 0.27.7's is empty

Round 17 (hyaku phase 2), axes: calibration + depth. Read-only: no carrier executed, no REA
`analyze`/`search`/`decompile`, no Ghidra, no installs, no ledger/registry edits. One permitted REA
call was run (`inspect-go-binary`, explicitly allowed by the lane contract).

- `R` = `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` (rea-agents 6.5.0).
- Carrier `C` = `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.27.7/node_modules/@esbuild/linux-x64/bin/esbuild`
  — sha256 `c638273fcf95573ca74af586677800b4dd874c55f8f945adb54316d6902ba14b`, 11,120,788 bytes,
  ELF64 LSB EXEC, x86-64.

## Answer

`go_version` is not read from an ELF header/field or from any string scan. It is the compiler-version
string **inside the Go build-info blob**, copied verbatim (no normalization) after a structural decode
that mirrors Go's `debug/buildinfo`: 14-byte magic `\xff Go buildinf:`, 16-byte-aligned virtual address,
fixed 32-byte header, then either two varint-prefixed inline strings (Go >= 1.18, `flags & 2`) or a
pointer pair (pre-1.18).

For carrier `C` the blob **does not exist anywhere in the file**. esbuild 0.27.7 is built with a
deliberately patched Go 1.25.7 toolchain whose linker call `ctxt.buildinfo()` is commented out
(`Makefile` at tag `v0.27.7:60-81`), so no `go:buildinfo` symbol is created, hence no `.go.buildinfo`
section and no magic bytes. REA therefore returns `normalized_result.build_info: null` — **there is no
`go_version` key at all** (not `""`, not a guess). A consumer evaluating
`normalized_result.build_info.go_version` gets `None`/`undefined`, which prints as empty.

This is correct, honest behaviour, not a reader defect: esbuild removes the record on purpose to defeat
`go version ./esbuild`-style CVE scanners (Makefile comment, `v0.27.7:60-68`).

## REA derivation chain (observed, `R/...:line`)

| step | anchor |
|---|---|
| CLI command `inspect-go-binary` | `R/cli/goCommands.js:9-19`; name `R/cliCommandNames.js:59` |
| Service wraps result as Evidence (`normalized_result` = result) | `R/application/go/GoBinaryService.js:55-67`; `R/domain/evidence.js:284` |
| Provider reads `image.build_info`, preserves `null` | `R/go/GoBinaryProvider.js:98,116` |
| Container dispatch (`\x7fELF` → ELF reader) | `R/go/GoBinaryImage.js:114-119` |
| Candidate span 1: section named exactly `.go.buildinfo\0` | `R/go/GoElfImage.js:105-121` |
| Section checks: SHT_PROGBITS, no SHF_COMPRESSED, maps to same file offset | `R/go/GoElfImage.js:113-116,122-124` |
| Candidate span 2 (no named section): every writable PT_LOAD (`flags&3===2`) | `R/go/GoElfImage.js:77-78,137` |
| Magic constant `ff20476f…64696e663a` | `R/go/GoBinaryImage.js:7` |
| 16-byte-aligned scan, 32 bytes required, 256 MiB cumulative budget | `R/go/GoBinaryImage.js:18-33,145-165` |
| Header must agree with its virtual mapping (`verifyMapping(32)`) | `R/go/GoBinaryImage.js:43` |
| ptrSize/flags; bit0 = endianness, bit1 = inline vs pointer | `R/go/GoBinaryImage.js:45-52` |
| Inline decode: version at `header+32`, module immediately after | `R/go/GoBinaryImage.js:56-60,166-188` |
| Pointer decode (pre-1.18) | `R/go/GoBinaryImage.js:62-70,190-208` |
| **No header found** → `build_info: null` (carrier `C`) | `R/go/GoBinaryImage.js:35-36` |
| Header found, zero-length version → hard `malformed` | `R/go/GoBinaryImage.js:74-75`; surfaced as `AnalysisInputError`/`invalid_format` (`R/go/GoBinaryProvider.js:47-56`) |
| Header found, non-UTF-8 version → `go_version: null` | `R/go/GoBinaryImage.js:76,103-107`; limitation `R/go/GoBinaryProvider.js:120-126`; strict decoder `R/go/GoBinaryContainer.js:133-141` |
| Normal field output (raw bytes also base64-preserved) | `R/go/GoBinaryImage.js:76,94-97` |
| Schema: `go_version` nullable, `build_info` nullable, strict object | `R/domain/go/goBinary.js:36,56` |

Three distinct "empty" surfaces, only one silent:

1. `build_info: null` — no blob discovered (this carrier). JSON has no `go_version` key; the limitation
   "No recognized Go build-info record was found…" is attached (`R/go/GoBinaryProvider.js:128-131`).
2. `build_info.go_version: null` — blob found but version bytes are not valid UTF-8. Limitation string
   about non-UTF-8 is added (`R/go/GoBinaryProvider.js:120-126`).
3. CLI error — blob found but zero-length version; no successful JSON at all.

## Carrier evidence (observed)

- Section table (parsed independently with Python `struct`; agrees with `readelf -SW`): 13 headers at
  file offset 0x158; `.text` 0x401000/0x1000+0x58a051, `.rodata` 0x98c000/0x58c000+0x1f39f9,
  `.go.fipsinfo` 0xe31000/0xa31000+0x78, `.shstrtab` 0xa9b000+0x94. **No `.go.buildinfo`, no
  `.note.go.buildid`, no `.symtab`.**
- Whole-file byte search: `b.find(b"\xff Go buildinf:") == -1` across all 11,120,788 bytes.
- `b".go.buildinfo"` occurs only at file offset 0xa9b035, i.e. inside `.shstrtab`; **no section header
  references that name**.
- Literal `go1.25.7` at file offset 0x758588 (inside `.rodata`). A string-grep probe would report a
  version here; REA does not, because it requires the structural blob. (Inference: this is the
  runtime's toolchain-version string, not build info.)
- Permitted run:
  `npx -y rea-agents@6.5.0 inspect-go-binary "C" --format json` → exit 0, evidence
  `ev_a1e7ac95032d7b36ea1c7c1429d7c6f8a8e252c153267bfa9f5e5228fe302ea1`;
  `normalized_result`: `{format:"elf", architecture:"amd64", bits:64, byte_order:"little",
  build_info:null}`; `subject.architecture:"x86_64"`; `confidence:"observed"`,
  `authority:"shipped-artifact"`. No `go_version` anywhere in the output.

Controls in the same `node_modules` tree (same reader, blob present):

| version | size | sha256 (prefix) | magic | section |
|---|---|---|---|---|
| @esbuild/linux-x64 0.21.5 | 9,707,520 | `b567f467fdac92c6…` | 0x8f4000 | `.go.buildinfo` 0xcf4000/0x8f4000+0x220 |
| @esbuild/linux-x64 0.25.12 | 10,358,936 | `bab29b2ca7a9e89b…` | 0x990000 | `.go.buildinfo` 0xd90000/0x990000+0x330 |
| @esbuild/linux-x64 0.27.7 | 11,120,788 | `c638273fcf95573c…` | **none** | **none** |

The 0.25.12 blob is independently visible in the r17 pilot Ghidra segment dump
(`.ufo/waves/round-17/pilot/esb.json`: segment `.go.buildinfo` 0xd90000–0xd90330), so the "normal" case
behaves as expected; 0.27.7 is the outlier.

## Root cause (observed at the release tag, not inference)

- `https://raw.githubusercontent.com/evanw/esbuild/v0.27.7/go.version` = `1.25.7` — matches the literal
  embedded in `C`, so the toolchain identity survived even though the blob did not.
- `https://raw.githubusercontent.com/evanw/esbuild/v0.27.7/Makefile:60-81`, target
  `go/$(GO_VERSION)`:
  - comment `:60-68`: build a custom Go compiler that "omits buildinfo from the final executable (since
    there is no command-line option to disable this) … avoid poorly-implemented 'security' tools …
    `go version ./esbuild` … false-positive report";
  - `:80` guard `grep -qF "ctxt.buildinfo()" src/cmd/link/internal/ld/main.go`;
  - `:81` `sed "s/ctxt.buildinfo/\/\/ctxt.buildinfo/" main.go`.
- Go 1.25.7 `cmd/link/internal/ld/main.go:426-427` calls `ctxt.buildinfo()`. That function
  (`data.go:2436-2474`) creates `go:buildinfo` (`:2440`), aligns it to 16 (`:2442`), writes the magic +
  ptrSize + flags (`|=2`, `:2446-2457`) and the varint `runtime.buildVersion` / `runtime.modinfo`
  (`:2458-2459`), and a rodata reference (`:2470`).
- The symbol name becomes the section name: `data.go:1807-1817` rewrites a `go:` prefix to `.go.`; and
  `sym.SBUILDINFO` symbols get one section each via `allocateDataSections` (`data.go:1905-1917`).
  No symbol ⇒ nothing in the `SBUILDINFO` bucket ⇒ no `.go.buildinfo` section ⇒ no magic. That is
  exactly the observed 0.27.7 section table.
- Version line history: `v0.26.0` Makefile has no buildinfo-removal target and `go.version` = 1.23.12
  (the local 0.25.12 blob is consistent with that); `v0.27.0` already has the target and
  `go.version` = 1.25.4. The removal landed in the 0.27 line.

Why `.go.buildinfo` still appears in `C`'s `.shstrtab`: Go 1.25.7 builds the section-name string table
from a **fixed list** (`cmd/link/internal/ld/elf.go:1427-1481`), unconditionally adding
`.text .noptrdata .data .bss .noptrbss .go.fuzzcntrs .go.buildinfo .go.fipsinfo .elfdata .rodata
.typelink .itablink .gosymtab .gopclntab` and then `.shstrtab`. The observed shstrtab of `C` matches
that order byte-for-byte. **The name is not evidence that a section exists** — a name-based probe is a
false positive by construction.
Separately, `.note.go.buildid` is absent because `v0.27.7/Makefile:11` passes
`-ldflags=-s -w -buildid=` (empty build id); that is independent of the buildinfo patch. Do not infer
the patched linker from the missing note alone.

## Calibration consequences for the r17 tool contract

- `W/tools/predict.py` takes `normalized_result.build_info.go_version`; for this carrier that node is
  **null**. `build_info is None` must map to "no version observed" → exit 2 with a reason, per the
  contract's empty/unparseable rule. It must **not** become `""`, and must not fall back to the
  `go1.25.7` `.rodata` string or to the `.go.buildinfo` shstrtab name.
- `build_info: null` ≠ "not Go". `C` is unmistakably Go (`.gopclntab`, `.typelink`, `.itablink`,
  `.go.fipsinfo`, `go1.25.7` literal); REA's own limitation says absence does not establish non-Go.
- Version strings are copied verbatim, so toolchain suffixes survive; the pilot's shfmt result
  `go1.27.0-X:nodwarf5` (pilot `README.txt`) is consistent with `R/go/GoBinaryImage.js:76,94`.
- REA is stricter than Go's reader on text: Go assigns raw bytes to `BuildInfo.GoVersion`, while REA
  returns `null` for non-UTF-8 (`R/go/GoBinaryContainer.js:133-141`).
- REA's discovery is a superset of Go 1.25.7's: Go falls back to the **first** writable non-exec
  PT_LOAD (`go1.25.7 src/debug/buildinfo/buildinfo.go:455-467`), REA scans **every** writable PT_LOAD
  with file-backed ranges (`R/go/GoElfImage.js:77-78,137`). For `C` both find nothing, so readers
  agree.
- Suggested knowledge/lesson wording: "REA reports the Go build-info record, not the toolchain
  identity. A Go binary may still embed `go1.x.y` and Go runtime tables while carrying no
  `.go.buildinfo` blob (esbuild ≥0.27 strips it at link time). Treat `build_info: null` as
  deliberate-absence-compatible, never as non-Go."

## Remaining unknowns

- Whether 0.27.0–0.27.6 release binaries also lack the blob: the v0.27.0 Makefile has the same patch,
  but no such binary exists locally; only 0.27.7 was verified.
- Whether the patched toolchain leaves `runtime.Version()` reporting `go1.25.7` at runtime: not tested
  (carrier execution prohibited). The literal is present; attribution to `runtime.buildVersion` is
  inference.
- Other r17 carriers (e.g. `/usr/bin/shfmt`) were not inspected here; scope was the esbuild carrier.

## Tooling / installs

No installs or upgrades. `npx -y rea-agents@6.5.0` used the existing npx cache
(`~/.npm/_npx/ad9a3fdbcad992c6`); `readelf` (binutils) and Python 3 stdlib for byte/section parsing.
REA commands run: exactly one `inspect-go-binary` (permitted). No `analyze`, `search`, `decompile`, no
Ghidra, no carrier execution.
