# UPX-packed ELF whose `UPX!` magic words are tampered: structural magic repair (round 87, R87-C1)

status: R87-C1 measured — the magic-altered anti-UPX class is Core for the bounded class named below
iff `python3 -I -B tools/round-87/upx-tamper-battery.py --root . --repair-cmd
tools/round-87/upx-magic-repair.py --upx /usr/bin/upx --pkg <REA 6.5.0 pkg dir> --work <SCRATCH>
--json-out <OUT>` reports `recovered 8 of 8`, `controls_ok` all true and exit 0 at the measured
revision <MEASURED: rev> (SCORECARD `## 2026-11-04 — round 87`). The before state is committed with
the declaration `f0ebf61161d08279dca98841461330ad442d3023`: the do-nothing control
(`--repair-cmd identity`) scores `recovered 0 of 8`, exit 1
(`.ufo/waves/round-87/pre/c1-control-identity-at-base.json`), and the cheap rule
(`--repair-cmd naive-global`) scores `recovered 4 of 8` with N1 false, exit 1
(`.ufo/waves/round-87/pre/c1-control-naive-global-at-base.json`). At BASE
`99f8b6a8979978fe02dc3c8f674ce4fdee3ab44b` `PROVINCE.md` and `corpus/README.md` list "an anti-UPX
stub whose magic or entry is altered" as Frontier.

source: S306 — UPX v5.2.0 `src/stub/src/include/linux.h` (`struct l_info`, `struct p_info`, `struct b_info`), https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h — <QUOTE, word count, line anchor, fetched sha256: from ScribeSources row> — grounds the l_info/p_info/b_info field layout the repair reads; it says nothing about tampering.
source: S307 — UPX v5.2.0 `src/p_unix.cpp` (end-of-chain `b_info`; "sz_cpr must be h->magic"), https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp — <QUOTE, word count, line anchor, fetched sha256: from ScribeSources row> — grounds the end-of-chain sentinel as a magic-bearing structure.
verified-at: 2026-11-04 (landing receipt `<MEASURED: .ufo/waves/round-87/l1/scores/c1-at-<rev>.json>` at the measured revision)
recheck: `python3 -I -B tools/round-87/upx-magic-repair.py --selftest` -> `SELFTEST cases=9 failures=0`; `python3 -I -B tools/round-87/upx-tamper-battery.py --selftest` -> `SELFTEST cases=8 failures=0`; the counting command above -> exit 0, `recovered 8 of 8`. Counter sha256 `0f2d2bd80108ded5282dbb8cbf79044357538458143c97ee591cc78e8e5384b0` (pinned in `.ufo/waves/round-87/claims.json`), repair sha256 `f4ebd152495dc832180fff3d1ca3447937a7dad121ba63d57872003ffcc49723` (commit `b5c7a49e20647bb73117ed1ffb4f68dd69916cd8`). Source recheck: refetch both URLs, `sha256sum` against the S306/S307 rows, `grep -n` the quoted lines.

## The class

[observation] A UPX-packed ELF whose `UPX!` words are overwritten still runs: the declaration
records `jq.t1 --version` printing `jq-1.8.2` with every `UPX!` word zeroed. The packer refuses it:
`upx -t`, `upx -l` and `upx -d` answer `NotPackedException: not packed by UPX`. [inference] The stub
that decompresses at run time never consults the words; only the packer's own unpack path does, so
overwriting them is a zero-cost anti-unpack measure. The file keeps the packed shape the round-68
route detects (no section header table, high entropy, a 3-procedure REA stub inventory), but the
route's first step (`upx -l` rc 0) now fails, so the route reads "not packed" and stops on the stub.

## Three structural anchors (located by structure, never by the tampered value)

| anchor | where it is | how it is found without the magic |
|---|---|---|
| PackHeader magic | 32-byte PackHeader in the last 512 bytes | its checksum byte is the sum of bytes 4..30 mod 251 — it **excludes** the magic, so a tampered header still validates; version >= 10, little-endian non-DOS format, plausible `c_len`/`u_len`/`u_file_size` |
| `l_info.l_magic` | `l_info {l_checksum, l_magic, l_lsize, l_version, l_format}` followed by `p_info {p_progid, p_filesize, p_blocksize}` (S306) | cross-checked: `l_version`/`l_format` equal the PackHeader's version/format and `p_filesize` equals the PackHeader's `u_file_size` |
| end-of-chain `b_info.sz_cpr` | the `b_info {sz_unc, sz_cpr, method, ftid, cto8, unused}` chain after `p_info`; its last record has `sz_unc == 0` and `sz_cpr == magic` (S307) | reached by **walking** the chain from `p_info`; where the chain stops at the embedded loader, resuming at the first later offset whose own chain (same method) ends at a sentinel — the "get past the loader" step |

[observation] On the four carriers packed `upx --best` (scribe scratch run, 2026-11-04, not the
scored run) the anchors land at: jq `l_info 556`, `b_info_end 13992`, `packheader 14000`; xxd
`556 / 19513 / 19524`; libz `9284 / 63721 / 65544`; docker-init `556 / 357738 / 357748`; every
chain stopped at the loader and resumed (4 blocks after the resume on all four). The libz sentinel
sits about 1.8 KiB before its PackHeader (appended shared-object data), so the repair imposes no
padding rule between sentinel and PackHeader.

## The commands

| step | command |
|---|---|
| detect | `readelf -SW <f>` reports no sections, the file runs, `upx -l <f>` rc != 0 `NotPackedException`, REA `analyze` returns a stub-sized inventory |
| repair | `python3 -I -B tools/round-87/upx-magic-repair.py --in <f> --out <f.fixed> --json` — exit 0 repaired or already intact (byte-identical output when intact); exit 2 refused (not an LE ELF, no validated PackHeader, no l_info matching it, no chain sentinel), nothing written; reads only `--in`, never runs the packer |
| test | `/usr/bin/upx -t <f.fixed>` rc 0 |
| route | the packed-ELF route (`2026-11-03-r68-packed-elf-route`): `upx -d -q -o <out> <f.fixed>`, sha256 against the pin, `rea analyze --format json <out>` |
| count | `python3 -I -B tools/round-87/upx-tamper-battery.py --root . --repair-cmd tools/round-87/upx-magic-repair.py --upx /usr/bin/upx --pkg <REA 6.5.0 pkg dir> --work <SCRATCH> --json-out <OUT>` |

## The measurement

| carrier | declared original procedures | T1-zero | T2-foreign |
|---|---|---|---|
| jq | 167 | <MEASURED> | <MEASURED> |
| xxd | 99 | <MEASURED> | <MEASURED> |
| libz.so.1.3.2 | 184 | <MEASURED> | <MEASURED> |
| docker-init | 1268 | <MEASURED> | <MEASURED> |

Recovered `<MEASURED> of 8` (target 8); controls N1 refuse-plain `<MEASURED> of 4`, N2
corrupt-payload recovered `<MEASURED> of 4` (must be 0), N3 intact-idempotent `<MEASURED> of 4`;
exit `<MEASURED>`. Before: identity 0/8; naive-global 4/8 (all four T2 cases; every T1 case fails
`upx -t` with `bad e_phoff`; N1 false — it refuses nothing). [inference] The cheap rule recovers
only the class whose tamper value is itself a findable token; the zeroed class needs the
structural anchors.

## Limits (stated, never claimed covered)

- Four carriers (`jq`, `xxd`, `libz.so.1.3.2`, `docker-init`), one packer (UPX 5.2.0,
  `/usr/bin/upx` sha256 `cf2f6e7c…c969`), one mode (`--best`), little-endian ELF x86-64, two tamper
  values (zero, `KDK!`) applied to every `UPX!` word. Not covered: entry-altered or
  stub-patched files, other packers, big-endian ELF, PE/Mach-O, other UPX versions or modes,
  tampering of fields other than the magic (version, format, checksum, sizes).
- The counter scores bytes, not provenance: a "repair" that re-packed the original would emit the
  same bytes. The kill rule's "names, reads or hashes any carrier source path or pin" clause is
  checked by review of the repair source (`--in`/`--out` only), not by the counter.
- [observation] The repaired packed file is not the pristine packed file for jq and xxd: each packed
  image carries a fourth `UPX!` occurrence outside the three anchors (jq offset 10971, xxd 16499;
  scribe scratch run) that the tamper overwrites and the repair leaves alone, so `cmp` against the
  pristine packed file reports 4 differing bytes on both; libz and docker-init carry no such
  occurrence and differ by 0. [inference] The occurrence is a `cmp` immediate in the loader code;
  the unpacker does not consult it, and `upx -d` still restores the pinned original on all four.
  Equality is therefore claimed for the **unpacked** bytes only.
- Inventory equality is the declared procedure count, not semantic equality.
- [unknown] Whether a tamperer who also rewrites the PackHeader checksum, `p_filesize` or the chain
  sizes can be repaired: none was measured, and the repair refuses rather than guesses.
