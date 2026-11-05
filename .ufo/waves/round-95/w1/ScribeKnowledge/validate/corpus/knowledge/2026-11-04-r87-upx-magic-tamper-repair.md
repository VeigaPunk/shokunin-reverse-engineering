# UPX-packed ELF whose `UPX!` magic words are tampered: structural magic repair (round 87, R87-C1)

source: S306 — UPX v5.2.0 `src/stub/src/include/linux.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h — opened 2026-11-04, HTTP 200, 19689 bytes, sha256 `5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9`; line 579: "struct l_info // 12-byte trailer in header for loader (offset 116)"; grounds the `l_info`/`p_info`/`b_info` field layout the repair reads.
source: S307 — UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp — opened 2026-11-04, HTTP 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`; line 8065: "if (sz_cpr != UPX_MAGIC_LE32) // sz_cpr must be h->magic"; grounds the end-of-chain `b_info` as a magic-bearing structure the Linux ELF unpacker checks.
source: S308 — UPX v5.2.0 `src/packhead.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp — opened 2026-11-04, HTTP 200, 13236 bytes, sha256 `41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a`; lines 64-66: "assert(get_le32(buf) == UPX_MAGIC_LE32); buf += 4; blen -= 4;"; grounds that the PackHeader checksum skips the four magic bytes.
verified-at: 2026-11-04 (round 87; measured revision and receipt in SCORECARD `## 2026-11-04 — round 87`)
recheck: 180d — `python3 -I -B tools/round-87/upx-magic-repair.py --selftest` (33 cases, failures 0) and the counting command below.

## The class

[observation] A UPX-packed ELF whose `UPX!` words are overwritten still runs: the round's before-state
run (`.ufo/waves/round-87/w1/ExecReaBefore/before.json`) shows all six tampered executables
(jq, xxd, docker-init × T1-zero/T2-foreign) exit 0 and print the original version string. The packer
refuses all eight tampered files: `upx -t`, `upx -l` and `upx -d` exit 2 with
`NotPackedException: not packed by UPX`. REA 6.5.0 `analyze` is blind to the tamper: its counts on the
intact packed, T1 and T2 files are identical per carrier and show the stub (jq 3/3/3, xxd 3/3/6,
docker-init 3/3/5 procedures/segments/strings) or, for the shared object, a partial program (libz
98 of 184 procedures — UPX leaves part of a `.so` uncompressed). Nothing in the REA envelope names UPX.
[inference] The run-time stub never consults the magic words; only the packer's own unpack path does,
so overwriting them is a zero-cost anti-unpack measure, and the round-68 route's first step
(`upx -l` rc 0) reads such a file as "not packed".

## Three structural anchors (located by structure, never by the tampered value)

| anchor | where it is | how it is found without the magic |
|---|---|---|
| PackHeader magic | the 32-byte PackHeader in the last 512 bytes | its checksum byte is the byte sum mod 251 taken after the first four bytes (S308, lines 64-70), so a tampered header still validates; version >= 10, little-endian non-DOS format, plausible `u_len`/`c_len`/`u_file_size` |
| `l_info.l_magic` | `l_info {l_checksum, l_magic, l_lsize, l_version, l_format}` followed by `p_info {p_progid, p_filesize, p_blocksize}` (S306, lines 579-593) | cross-checked: `l_version`/`l_format` equal the PackHeader's version/format and `p_filesize` (12 bytes after `l_magic`) equals `u_file_size` |
| end-of-chain `b_info.sz_cpr` | the `b_info {sz_unc, sz_cpr, method, ftid, cto8, unused}` chain after `p_info`; its last record has `sz_unc == 0` and `sz_cpr == magic` (S307, line 8065) | reached by walking the chain; where it stops at the embedded loader, by resuming at the first later offset whose own chain ends at a sentinel |

The resume is a scan. UPX's own unpacker skips the loader deterministically through `e_entry` and
`l_lsize` (`p_lx_elf.cpp` lines 7948-7972, ScoutUpxLayout A13); the scan is the analogue of its
recovery peek (lines 7993-8009). Blocks may use the first block's method or the PackHeader's method:
an `--lzma` shared object begins with one NRV2B block followed by LZMA blocks (ExecRepairCases probe).

[observation] On the four carriers packed `upx --best` the anchors land at: jq `l_info 556`,
`b_info_end 13992`, `packheader 14000`; xxd `556 / 19513 / 19524`; libz `9284 / 63721 / 65544`;
docker-init `556 / 357738 / 357748`. jq and xxd carry a fourth `UPX!` word (jq 10971, xxd 16499):
the bytes `81 fa 55 50 58 21`, an x86 `cmp edx, 0x21585055` immediate in the loader. It is not an
anchor; the tamper overwrites it and the repair leaves it, so a repaired jq/xxd differs from the
untampered packed file in those 4 bytes while libz and docker-init are byte-identical to it.

## The commands

| step | command |
|---|---|
| detect | `readelf -SW <f>` reports no sections, the file runs, `upx -l <f>` exits 2 `NotPackedException`, REA `analyze` returns a stub-sized inventory |
| repair | `python3 -I -B tools/round-87/upx-magic-repair.py --in <f> --out <f.fixed> --json` — exit 0 repaired or already intact (byte-identical output when intact); exit 2 refused (not an LE ELF, no validated PackHeader, no `l_info` matching it, no chain sentinel), nothing written; reads only `--in`, never runs the packer |
| test | `/usr/bin/upx -t <f.fixed>` exit 0 |
| route | the packed-ELF route (`2026-11-03-r68-packed-elf-route`, carrier table of `2026-11-04-r70-provenance-bound-receipts`): `upx -d -q -o <out> <f.fixed>`, sha256 against the pin, `rea analyze --format json <out>` |
| count | `python3 -I -B tools/round-87/upx-tamper-battery.py --root . --repair-cmd tools/round-87/upx-magic-repair.py --upx /usr/bin/upx --pkg <REA 6.5.0 package dir> --work <scratch> --json-out <receipt>` |

## The measurement

Measured at `73c3a29740884b0c134bbe50e3c9b13f141daccf` (repair sha256 `96da7d8e…bec24`, counter sha256 `0f2d2bd8…4b0`), receipt
`.ufo/waves/round-87/l1/scores/c1-at-73c3a297.json`, REA envelopes `.ufo/waves/round-87/l1/scores/rea-73c3a297/`:

| carrier | declared original procedures | T1-zero (REA procs/segs/strings after) | T2-foreign | before (REA on tampered file) |
|---|---|---|---|---|
| jq | 167 | recovered, 167/30/190 | recovered, 167/30/190 | 3/3/3 |
| xxd | 99 | recovered, 99/29/103 | recovered, 99/29/103 | 3/3/6 |
| libz.so.1.3.2 | 184 | recovered, 184/29/199 | recovered, 184/29/199 | 98/6/136 |
| docker-init | 1268 | recovered, 1268/29/1111 | recovered, 1268/29/1111 | 3/3/5 |

`recovered 8 of 8` (target 8); controls N1 refuse-plain 4/4, N2 corrupt-payload recovered 0/4,
N3 intact-idempotent 4/4; exit 0. `repaired_equals_packed` is true for libz and docker-init and false
for jq and xxd (the loader `cmp` word, above).

Before (committed with the declaration `f0ebf61161d08279dca98841461330ad442d3023`): the do-nothing
control (`--repair-cmd identity`) scores `recovered 0 of 8`, exit 1; the cheap rule
(`--repair-cmd naive-global`, replace every copy of the word at `len-36` with `UPX!`) scores
`recovered 4 of 8` — all four T2 cases, every T1 case failing `upx -t` with `bad e_phoff` — and N1
false (it refuses nothing), exit 1. [inference] The cheap rule recovers only the class whose tamper
value is itself a findable token; the zeroed class needs the structural anchors.

The `rea_recover` arm is entailed by the `identity` arm (wave review F1): once `upx -d` restores the
pinned bytes, REA's count follows from the pin. The REA-level signal that the repair adds is the
before → after contrast above: the stub count on the tampered file versus the declared count after.

## Out-of-population probe (not scored, not Core)

ExecRepairCases (`.ufo/waves/round-87/w1/ExecRepairCases/receipts/probe-after-fix.json`) packed the
four carriers with `-1`, `--lzma` and `--best --brute`, tampered T1/T2 and repaired: every case passes
`upx -t`, restores the pinned sha256 through `upx -d` and the executables run like the original. The
reviewer's probe on the committed pre-integration repair refused libz `--lzma` (single-method chain
walk); the integrated repair accepts the PackHeader's method for later blocks.

## Hardening after the wave (integrated before measurement)

SentinelR87 showed that a 25-byte decoy chain planted in loader bytes steered the first-hit resume
scan to a wrong sentinel (jq/docker-init: rc 0, output still failing `upx -t`; intact+decoy: 4 loader
bytes mutated), and that the resume scan was quadratic on crafted chains. The integrated repair scores
every resume candidate (a sentinel already reading `UPX!` wins, else the one nearest the PackHeader),
memoises walk ends, and refuses non-regular or > 256 MiB input with rc 2. Re-run of the seat's decoy
probe on the integrated repair: all four decoy cases restore the real sentinel (`upx -t` 0;
intact+decoy unchanged) — `.ufo/waves/round-87/l1/decoy-probe-after-hardening.txt`. A decoy placed
between the real sentinel and the PackHeader (room exists only in a shared object's appended data,
1815 bytes on libz) is not excluded.

CriticClaim built a chain-walk-free repair (checksum PackHeader, version/format `l_info`, zero-surround
sentinel) that also scores `recovered 8 of 8` with REA and byte-identical outputs
(`.ufo/waves/round-87/w1/CriticClaim/receipts/cheap-v4-checksum-lite-rea.json`): the frozen counter
forces the checksum and `l_info` anchors but not the chain walk. The plan's sentence "only a
structural repair reaches" the zeroed class holds only in that sense; the chain walk is a robustness
choice the counter does not discriminate.

## Limits (stated, never claimed covered)

- Core scope: four carriers (`jq`, `xxd`, `libz.so.1.3.2`, `docker-init`), UPX 5.2.0 (`/usr/bin/upx`
  sha256 `cf2f6e7c…c969`), `--best`, little-endian ELF x86-64, two tamper values (zero, `KDK!`)
  applied to every `UPX!` word. Not covered: entry-altered or stub-patched files, tampering of fields
  other than the magic (version, format, checksum, sizes, `p_filesize`), other packers or UPX
  versions, big-endian ELF, PE/Mach-O, i386/ARM.
- The counter scores bytes, not provenance; the kill rule's "reads no carrier path or pin" clause is
  checked by review (ReviewerRepair: imports `argparse`, `json`, `struct`, `sys` only; the only I/O is
  `--in`/`--out`).
- N2 (corrupted payload never recovered) holds through UPX's own integrity check; the repair itself
  does not verify the PackHeader adlers.
- Mutation probe (MutationR87): no mutant turned the do-nothing control green; guard mutants that the
  four-carrier population never exercises (PackHeader sanity bounds, `l_info` version/format
  cross-check, method checks) survive the frozen counter — they are defences against plain-ELF false
  matches, covered in part by the integrated selftest's chance-window cases, not by the population.
- Measured negative (CriticClaim T5): T2 plus `p_info.p_filesize` zeroed — the repair exits 0 but `upx -t`
  still fails; tampering of fields beyond the magic is not repaired. Whether a tamperer who also rewrites
  the PackHeader checksum or chain sizes can be repaired was not measured.
