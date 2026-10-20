# ToolchainIdentity — go1.25.0 carrier identity, build info, prescan comparison

Seat: KaidokuR19.ToolchainIdentity (read-only). Baseline: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`.
Scope: sha256+size of the nine C3 carriers, Go build info via the lane's static parsers, comparison with
`W19/evidence/prescan/*.json`, and official-tarball provenance. No carrier was executed; no REA or Ghidra call was
made; nothing under `/home/vgpnk/.local/opt` or the lane was modified. The only lane write is this report.

Paths below: `GO=/home/vgpnk/.local/opt/go-1.25.0`, `W19=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19`.

## Verdict

- **OBSERVATION — carriers are pristine tarball members.** All nine C3 carriers are byte-identical (`sha256`+size)
  to their members in the official `go1.25.0.linux-amd64.tar.gz`; the whole 14,496-file tree is byte-identical to a
  fresh extract of that archive, which itself hashes to the go.dev release value
  `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613` (59,659,213 bytes).
- **OBSERVATION — 9/9 carry an inline Go build info blob reading `go1.25.0`.** The lane's Go-faithful parser
  (`W17/tools/buildinfo-probe.py`, selftest `SELFTEST: CLEAN cases=11`) finds `.go.buildinfo` in all nine, including
  `link`, with `flags=0x2` (inline), `ptr_size=8`, little-endian.
- **OBSERVATION — the prescan's `link: unparseable` is false for these bytes.** `kr19-sm-link.json:1-4` says
  `no Go build info`; `link` actually has a valid header at file offset 5,779,456 (`.go.buildinfo`, vaddr `0x983000`,
  section size `0x110`) with `version='go1.25.0'` and modinfo `path\tcmd/link`.
- **OBSERVATION — the prescan premise is a parser artifact.** The prescan emulator `W18/tools/swiss-misread.py:197`
  uses `d.find(BUILDINFO_MAGIC)` — an *unrestricted first-hit* scan. For `link` the first hit is at file offset
  3,461,224 in `.rodata` (an incidental copy of the 14-byte magic inside the linker's own data), where the header
  bytes are nonsense (`ptr_size=0x72`, `flags=0x75`), so `parse_buildinfo` returns `(None, None, None)` and
  `analyse` raises at `:1262`. Reproduced below.
- **INFERENCE — 8/9 prescan successes are file-order luck.** Only `link`'s `.rodata` copy precedes its
  `.go.buildinfo`; for the other eight the first whole-file hit happens to be the real header. Any rebuild that
  moves an incidental copy earlier in the file would flip a carrier to "unparseable" without any byte-level cause in
  the claim's terms.

## O1 — identity and build info (all nine)

`sha256` and size measured on the installed files; `off` is the `.go.buildinfo` file offset from the probe
(`header_offset`), decimal and hex; `sec` is the section size from `readelf -SW`.

| carrier (rel. `GO/`) | bytes | sha256 | off (dec / hex) | sec | ver | `path` line |
|---|---|---|---|---|---|---|
| `bin/go` | 14,939,693 | `b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25` | 13,344,768 / `0xcba000` | 0x110 | go1.25.0 | `cmd/go` |
| `bin/gofmt` | 3,000,838 | `2aa4122abbd1593ee7c9e184366feef7cb06e52ce790b5ef2119e8aee8640a80` | 2,703,360 / `0x294000` | 0x110 | go1.25.0 | `cmd/gofmt` |
| `pkg/tool/linux_amd64/asm` | 4,811,078 | `a7ed400a04009488ea819eb06aeb912dc3537125cceef036743641060fd797f4` | 4,161,536 / `0x3f8000` | 0x110 | go1.25.0 | `cmd/asm` |
| `pkg/tool/linux_amd64/cgo` | 4,413,745 | `d61f87246456ff1175d057ad663a10dd1ac503c54dc770d14aaa5ffd3309b858` | 3,952,640 / `0x3c5000` | 0x110 | go1.25.0 | `cmd/cgo` |
| `pkg/tool/linux_amd64/compile` | 21,518,237 | `20dbac54f9f897582aedafea7207976f0300cfd4992429814d00bccbea7a4083` | 18,894,848 / `0x1205000` | 0x120 | go1.25.0 | `cmd/compile` |
| `pkg/tool/linux_amd64/cover` | 5,037,210 | `64686d22f3b4055386bbcbf0aeac54249cdbff771ffd7b54c8d4abd330df8166` | 4,468,736 / `0x443000` | 0x110 | go1.25.0 | `cmd/cover` |
| `pkg/tool/linux_amd64/link` | 6,403,924 | `a4286eaff6094de7f88d55299a61a14d5aae2bfbd19687ba6d5330a730aee983` | 5,779,456 / `0x583000` | 0x110 | go1.25.0 | `cmd/link` |
| `pkg/tool/linux_amd64/preprofile` | 2,274,474 | `eff3b19676f41d95eb598fa7520a9f44c2014db65a5a7470a2ca5c4cfa3f840b` | 2,048,000 / `0x1f4000` | 0x110 | go1.25.0 | `cmd/preprofile` |
| `pkg/tool/linux_amd64/vet` | 8,082,935 | `9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7` | 7,364,608 / `0x706000` | 0x110 | go1.25.0 | `cmd/vet` |

All nine also carry `.go.fipsinfo` and `.note.go.buildid`, and share one Go section skeleton (`.text .typelink
.itablink .gopclntab .go.buildinfo .go.fipsinfo .note.go.buildid .noptrdata .data .bss` all present — section-name
census run on all nine, exit 0). `link` is not structurally distinguishable from the other eight at section level.

Per-binary modinfo differences (decoded from `.go.buildinfo`): all nine record `-buildmode=exe -compiler=gc
-gcflags=cmd/...=-dwarf=false -trimpath=true CGO_ENABLED=0 GOARCH=amd64 GOOS=linux GOAMD64=v1`; **`compile` alone
adds `-pgo=default.pgo`**, and its section is `0x120` (242-byte modinfo) against `0x110` for the rest. `compile`
also orders `GOAMD64/GOARCH/GOOS` differently (last three lines). No other differences.

## O2 — official-tarball provenance

- `https://go.dev/dl/go1.25.0.linux-amd64.tar.gz` downloaded 2026-10-20 to `/tmp/go1.25.0.linux-amd64.tar.gz`:
  `sha256 = 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`, size `59,659,213` — both equal to
  `https://go.dev/dl/?mode=json&include=all` for `go1.25.0`/`go1.25.0.linux-amd64.tar.gz` (fetched same run).
- In-lane records agree in full and in size: `W18/w1/SentinelReaEnv.md:75` and `W18/w2/ReopenS035.md:67-69`
  (`… 59659213`). `corpus/lessons/round-18-verifier-spotcheck.md:147` carries only the truncated `2852af0c…b613`
  (prefix/suffix), which cannot authenticate a download on its own — the full value is at the two W18 anchors above.
- Extraction to `/tmp/go125-official/go`, then per-file `sha256sum` over both trees: **14,496/14,496 lines
  identical** (`cmp` clean), file-name lists identical (`diff` empty), symlinks `0/0`, dirs `1,592/1,592`.
  `VERSION` = `go1.25.0` / `time 2025-08-08T19:33:32Z`.
- No local tarball or checksum file existed before this seat (`find / -xdev` for `go1.25.0*.tar*` returned nothing).

## O3 — prescan comparison (`W19/evidence/prescan/kr19-sm-*.json`)

- Eight of nine: `carrier.sha256` and `carrier.size` equal my hashes (checked programmatically, 8/8 True),
  `go_version='go1.25.0'`, `go_version_buildinfo='go1.25.0'`, `go_version_source='inline'` — all consistent with the
  probe. `snapshot_status='base_only'` for those eight, `snapshot_file=…/typeinfo/golang/go1.25.0.json`.
- `link`: the file is only `{"error": "no Go build info in …/link", "status": "unparseable"}`
  (`kr19-sm-link.json:1-4`) — **no carrier digest, no version, no evidence** binding that verdict to bytes.
- Prescan `layout` is identical on the eight (`ghidra_maptype=internal/abi.OldMapType`, `ghidra_size=88`,
  `true_kind=swiss`, `true_size=112`, `uncommon_size=16`); `vet` is the only one with `predicted_failure=true`
  (`diagnostic_detail` types `*types.valueMap`, `*types.opPredicates`, `*types.nodeSet`). Those are other seats'
  questions; I only confirm the version/identity inputs they rest on.

## O4 — the `link` counterexample, mechanism and reproduction

- OBSERVATION: `readelf -SW GO/pkg/tool/linux_amd64/link` →
  `[ 7] .go.buildinfo PROGBITS 0000000000983000 583000 000110 00 WA 0 0 16`.
- OBSERVATION: bytes at `0x583000`: `ff 20 47 6f 20 62 75 69 6c 64 69 6e 66 3a 08 02 00…` → magic, `ptr_size=8`,
  `flags=0x02`; inline varint `08` + `go1.25.0`; modinfo varint `d8 01` (216 bytes) framed by the
  `3077af0c…d8f2` sentinels, first line `path\tcmd/link`, last line `build\tGOAMD64=v1`.
- OBSERVATION: the *first* whole-file magic is at 3,461,224 (`0x34d068`), inside `.rodata`
  (section `addr=0x6cd000 off=0x2cd000 size=0x11ac61`); the bytes are
  `…e.symtab \xff Go buildinf: runtime.egcbss main..inittask go:plugin.tabs…` — the linker's own data, not a header.
  At that offset `d[magic+14]=0x72` (`ptr_size`) and `d[magic+15]=0x75` (`flags`); `flags & 2 == 0`, so
  `parse_buildinfo` takes the pointer branch and `ptr_size=114 ∉ {4,8}` → `(None,None,None)`.
- OBSERVATION (reproduced with the prescan's own code, imported read-only):
  `parse_buildinfo` on `link` → `first_magic=3461224 ptrsz=0x72 flags=0x75 parse=(None, '', None)`, while the other
  eight return `('go1.25.0', <contaminated modinfo>, 'inline')`.
- OBSERVATION (same module, search scoped to `.go.buildinfo` instead of `d.find`):
  `version='go1.25.0'`, `modinfo_first_line='path\tcmd/link'`, full flags as in O1.
- OBSERVATION: the emulator's success rule is therefore file-offset-order dependent
  (`swiss-misread.py:53,194-197,1251-1262`); the Go-faithful rule is the section/short-scan space implemented at
  `buildinfo-probe.py:162` (`elf_search_space`) + `:205` (`search_magic`, aligned 14-byte magic).
- OBSERVATION (secondary, low impact): the emulator's `modinfo` still contains the 16-byte sentinels (it does not
  strip framing the way Go does); its `GOOS`/`GOARCH` scan uses line prefixes, so the eight parsed carriers still
  report `linux/amd64` correctly. Cosmetic for predictions, but it shows emulator ≠ Go parser.
- INFERENCE: if the emulator were scoped to `.go.buildinfo`, `link` would parse to the same shape as the other eight
  and need no `--go-version` override. Whether to include `link` in C3 is not this seat's decision; the mechanism,
  the correct bytes, and the forced-version escape hatch are recorded here for `LinkNoBuildinfo`/L1.

## O5 — downstream statements resting on the false premise

`W19/claims.json:26` (C3 text: “(go, gofmt, asm, cgo, compile, cover, preprofile, vet; **link has no build info**)”),
`W19/contract.md:44` (“link unparseable (no Go build info)”), `W19/gen-wave1.py:143` (GenPredictionsR19 is told to
record `status: excluded` for link “with the emulator's unparseable cause”), `W19/gen-wave1.py:304-307`
(`LinkNoBuildinfo` prompt), `W19/w1/LogEntryDraft.md:21`, `W19/w1/LessonSkeleton.md:48`. Each is an accurate record of
the prescan artifact and an inaccurate statement about the carrier bytes.

## O6 — freshness

- OBSERVATION: the carrier is the **.0** release. `https://go.dev/dl/?mode=json&include=all` currently lists
  `go1.25.0` through `go1.25.14` (14 Linux/amd64 patch archives), so the calibration carrier is 14 patch releases
  behind the live 1.25 line; `~/.local/opt` also holds `go-1.24.6` and `go-1.27.3`.
- OBSERVATION: go1.25.0's archive is still published and its digest unchanged (2852af0c…b613), so the pinned
  provenance is reproducible, not a moving target.
- INFERENCE: conclusions about “Go 1.25” generically from these bytes are scoped to the .0 build; later patches
  could alter `.go.buildinfo` size/modinfo but were not fetched (see unknowns).

## Commands (as run; exit codes)

```
$ for f in bin/go bin/gofmt pkg/tool/linux_amd64/{asm,cgo,compile,cover,link,preprofile,vet}; do
    printf '%s\t%s\t%s\n' "$f" "$(stat -c%s GO/$f)" "$(sha256sum GO/$f | cut -d' ' -f1)"; done
# exit=0   (values in O1)

$ python3 -I -B W17/tools/buildinfo-probe.py --selftest
SELFTEST: CLEAN cases=11
# exit=0

$ for f in <the nine>; do python3 -I -B W17/tools/buildinfo-probe.py "$f"; done
# found=true, search_space=".go.buildinfo section", go_version="go1.25.0", inline=true, ptr_size=8, flags=2
# modinfo_first_line="path\tcmd/<name>"; probe_exit=0 for all nine

$ curl -sSL -m 600 -o /tmp/go1.25.0.linux-amd64.tar.gz https://go.dev/dl/go1.25.0.linux-amd64.tar.gz
$ stat -c '%s' /tmp/go1.25.0.linux-amd64.tar.gz && sha256sum /tmp/go1.25.0.linux-amd64.tar.gz
59659213
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  /tmp/go1.25.0.linux-amd64.tar.gz
# curl_exit=0, exit=0

$ curl -sSL 'https://go.dev/dl/?mode=json&include=all' -o /tmp/go-dl.json
go1.25.0 go1.25.0.linux-amd64.tar.gz 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613 59659213 archive
# exit=0

$ tar -xzf /tmp/go1.25.0.linux-amd64.tar.gz -C /tmp/go125-official
$ ( cd /tmp/go125-official/go && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > /tmp/official.tree.sha
$ ( cd GO && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > /tmp/installed.tree.sha
$ cmp -s /tmp/official.tree.sha /tmp/installed.tree.sha; echo $?
0        # TREE_IDENTICAL=yes; 14496/14496 lines; diff of name lists empty
# exit=0

$ python3 -c "<ELF section map for link>"          # off 3461224 -> .rodata; off 5779456 -> .go.buildinfo
# exit=0

$ python3 -c "<import W18/tools/swiss-misread.py; parse_buildinfo(link)>"
first_magic=3461224 ptrsz=0x72 flags=0x75 parse=(None, '', None)
# exit=0

$ python3 -c "<same module; parse starting at .go.buildinfo offset>"
ptrsz=8 flags=0x2 version='go1.25.0'  modinfo_first_line='path\tcmd/link'
# exit=0
```

No installs or upgrades were performed; no pacman transaction was attempted. Network use: two `curl` fetches
(go.dev release JSON + the 59.7 MB tarball), artifacts left in `/tmp` (`go1.25.0.linux-amd64.tar.gz`,
`go125-official/`, `go-dl.json`, `official.tree.sha`, `installed.tree.sha`).

## Residual unknowns

1. **REA 6.5.0's own buildinfo reader on `link` is untested** — the contract bars REA `analyze`/`search`/`decompile`
   on C3 carriers before the L1 freezes predictions, so whether REA would parse `link` (section-scoped like Go, or
   first-hit like the emulator) is unknown here. The prescan artifact is *not* REA output; it is
   `swiss-misread.py` (tool sha256 at B `14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`,
   worktree identical). Probe sha256 at B `94ce3c202135dddb0c068567e52802a228af12464e8a5e62f235af8c00c70f61`.
2. The prescan artifacts record no tool digest and, for `link`, no carrier digest; the verdict is not bound to bytes
   in the artifact itself (I bind it here: `a4286eaff609…aee983`, 6,403,924 bytes).
3. Whether `link` should join C3 (with or without `--go-version go1.25.0`) is `LinkNoBuildinfo`/L1's call; I did not
   run the emulator's override path or predict an outcome for it.
4. Later 1.25.x patches were not fetched, so whether `.go.buildinfo`/section layout changes across the 1.25 line is
   unverified (only go1.25.0 bytes are characterised here).
5. The full-tree digest comparison covers regular files only; both trees have 0 symlinks and equal directory counts,
   so nothing is known to be skipped, but mode/ownership differences were not compared (tar records `0/0`).
