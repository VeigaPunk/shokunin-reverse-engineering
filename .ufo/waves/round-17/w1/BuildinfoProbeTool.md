# BuildinfoProbeTool — buildinfo-probe.py

Tool: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py`
Independent stdlib-only reader of the Go build-info blob. Runs under `python3 -I`; never executes
the carrier; ELF only (other formats are sniffed and reported, not decoded).

## Verification performed

`python3 -I <tool> --selftest` → `SELFTEST: CLEAN cases=11`, exit 0.
Fixtures cover: inline via `.go.buildinfo` section; inline via writable-PT_LOAD fallback with no
section headers; pointer format LE ptr_size 8; pointer format BE ptr_size 4; no magic; misaligned
magic skipped for later aligned one; truncated header at range end; empty version string
(`found:true`, `go_version:null`, matching Go `errNotGoExe` at L259-260); MZ sniffed as pe;
tolerated extra flag bits outside Go's 0x3 mask; magic only in a non-writable segment → `found:false`.
Two real defects found and fixed before selftest pass: a Python `&`/`!=` precedence bug
(`flags & MASK != X` parses as `flags & (MASK != X)`) and a zero-length read at exact segment
end faulting inside `read` instead of returning `b""`.

## Carrier results (all exit 0)

| path | sha256 (prefix) | found | go_version | search_space | header_offset |
|---|---|---|---|---|---|
| /usr/bin/shfmt | 58f765638eed… | true | `go1.27.0-X:nodwarf5` | .go.buildinfo section | 3515584 |
| esbuild 0.25.12 | bab29b2ca7a9… | true | `go1.23.12` | .go.buildinfo section | 10027008 |
| esbuild 0.21.5 | b567f467fdac… | true | `go1.20.12` | .go.buildinfo section | 9388032 |
| esbuild 0.27.7 | c638273fcf95… | **false** | **null** | first writable non-executable PT_LOAD | null |

Independent agreement with REA `inspect-go-binary` 6.5.0 (allowed per contract): identical
`go_version` and identical `header_offset` on all three found carriers (REA evidence ids
ev_f8ef12a8… shfmt, ev_0cabcc66… esb 0.25.12, ev_5c06ecef… esb 0.21.5). On esb 0.27.7 REA's
`normalized_result.build_info` is `null` and its limitations add "No recognized Go build-info
record was found" (ev_a1e7ac95…); this probe reports `found:false` with `magic_file_offsets:[]`
— the magic occurs **nowhere** in the file, aligned or not, so the absence is total, not a
search-range artifact.

## Why REA returned empty go_version for the 0.27.7 build

**Observation** (file bytes): esb 0.27.7 is a normal Go ELF — it has `.gopclntab`,
`.gosymtab`, `.go.fipsinfo` sections and a NUL-terminated `go1.25.7` string at file offset
0x758588 — but has **no `.go.buildinfo` section** and **zero occurrences** of `\xff Go
buildinf:` anywhere in its 11120788 bytes. So REA's probe (which mirrors Go's reader: prefer
`.go.buildinfo`, else scan the writable PT_LOAD — rea-agents dist `go/GoElfImage.js:105`,
`go/GoBinaryImage.js` MAGIC + `build_info: null` return) correctly reports no record, and
`go_version` is empty/null because there is no blob to decode — not because it was out of
range or unparseable.

**Observation** (upstream source): `esbuild v0.27.7` Makefile lines 60-81
(raw.githubusercontent.com/evanw/esbuild/v0.27.7/Makefile) build releases with a custom-patched
Go toolchain: comment at L60-62 "Build a custom version of the Go compiler that omits buildinfo
from the final executable (since there is no command-line option to disable this)"; L80
`grep -qF "ctxt.buildinfo()" src/cmd/link/internal/ld/main.go`; L81
`sed "s/ctxt.buildinfo/\\/\\/ctxt.buildinfo/" main.go` comments out the linker's buildinfo
emission. `go.version` at that tag = `1.25.7`, matching the observed `go1.25.7` runtime string.

**Observation** (version bracketing): the same Makefile patch is absent at v0.25.12 and v0.26.0
(go.version 1.23.12), present at v0.27.0 (go.version 1.25.4) and v0.27.7. So the omission began
with the 0.27.x release line — consistent with 0.21.5/0.25.12 binaries carrying the blob and
0.27.7 not.

**Inference** (labeled as such): esb 0.27.7 was linked by esbuild's patched Go 1.25.7 toolchain,
which is exactly the mechanism the Makefile documents (the sed comments out `ctxt.buildinfo()`,
called at `src/cmd/link/internal/ld/main.go:427` at tag go1.25.7). Motivation per the Makefile
comment: dodge Go-version CVE false-positives from security scanners. The residual `go1.25.7`
string is the runtime's own compiled-in version string, unaffected by link-time buildinfo
suppression.

## Go source anchors cited (tag `go1.25.0`, `src/debug/buildinfo/buildinfo.go`, file sha256
332fff28ac2569b76dda2e9d4f25aacc112e12bd8888fca927db0c5156187f45)

L58 magic; L61-62 align=16/header=32; L125-130 ELF dispatch; L170-172 DataStart/errNotGoExe;
L181-188 32-byte header; L192-202 ptrSize@14, flags@15, versPtr@16, endian mask 0x1, version
mask 0x2 (ptr=0/inl=2); L218-227 inline vs pointer format comment; L228-258 decode dispatch;
L259-260 empty vers → notGoExe; L262-267 `mod[16:len-16]` framing strip; L284-318 decodeString
(uvarint L297); L335 1 MiB search chunk; L339-397 searchMagic (align-up L347, header-space check
L388-390, misaligned skip L392-402); L445-453 elfExe.DataReader (PT_LOAD filesz mapping);
L455-466 elfExe.DataStart (.go.buildinfo at L457-458, writable non-exec PT_LOAD L461-463).

Upstream quirk noted, not replicated (inference): in `searchMagic`, after `data = data[next:]`
(L399) the next `bytes.Index` result `i` is relative to the re-sliced slice, but the function
returns `start + i` (L404) and tests `remaining - i` (L388) against the unsliced remainder —
so with ≥2 misaligned matches Go's reported address would sit too early. This probe uses
absolute offsets inside the range, which is the behavior the code intends; no known linker
output produces consecutive misaligned magics.

## Limits

ELF decoding only; pointer-format headers stop at ptr decode per contract (vers/mod pointers
reported, not dereferenced). `magic_file_offsets` is an unrestricted whole-file scan offered
as stronger absence evidence than Go's scoped search. No installs or updates were made; only
network reads were the mandated upstream-source fetches (Go tag go1.25.0, esbuild tags).

Report: .ufo/waves/round-17/w1/BuildinfoProbeTool.md
