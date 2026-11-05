# Packed-ELF `b_info` value classes: a wrong-but-in-range `sz_cpr` recovered by the same chain law (round 89, R89-C1)

source: S311 — UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp — opened 2026-11-04, HTTP 200, 373743 bytes, sha256 `551fc8675a594937…`; line 7105 (and 7308, the 32-bit twin): "throwCantUnpack("corrupt b_info");"; lines 7096-7104 show the `unpackExtent(sz_elf_hdrs, …)` peek whose short result decides it, so the message names the *block walk*, not one field.
source: S312 — UPX v5.2.0 `src/p_unix.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.h — opened 2026-11-04, HTTP 200, 6651 bytes, sha256 `73bd992ec0fb4602…`; lines 201-204: "packed_struct(p_info) { // 12-byte packed program header / LE32 p_progid; LE32 p_filesize; LE32 p_blocksize;"; grounds why the locator finds `u_file_size` twelve bytes after `l_magic`.
source: S306 (existing, round 87) — UPX v5.2.0 `src/stub/src/include/linux.h` — the 12-byte `b_info` header the chain walk steps by.
source: S309 (existing, round 88) — UPX v5.2.0 `src/packhead.h` — the PackHeader fields the accounting bound reads (`u_len`, `c_len`, `u_file_size`).
source: S310 (existing, round 88) — UPX v5.2.0 `src/packer.cpp` — the arithmetic gate that raises `header corrupted` before any checksum.
verified-at: 2026-11-04 (round 89; measured revision and receipt in SCORECARD `## 2026-11-04 — round 89`)
recheck: 180d — `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest` (16 cases, failures 0) and the counting command below.

## The class

[observation] Round 88's limit — "a non-zero but wrong `sz_cpr` is left alone" — is a *class*, not an
edge: overwrite block 0's `sz_cpr` with any other in-range value and every bound the packer applies to
the field passes (`0 < sz_cpr <= sz_unc`, block inside the tail window). The refusal therefore moves
one stage later: `upx -t` answers `Exception: compressed data violation` (measured on all four
carriers, `.ufo/waves/round-89/pre/c1-base-r88-repair.json` `precondition.tail`), where the zeroed
value answers `CantUnpackException: b_info corrupted`. The round-88 repair cannot see it: its
round-87 anchor path reports `intact` (the `UPX!` words are in place) and its geometry gate skips any
block whose stored `sz_cpr` is non-zero, so the composed repair scores `recovered 0 of 4` with every
control true.
[inference] The class is recoverable for the same reason the zeroed class is: `sz_cpr` is redundant
with the block boundaries, so the *stored value is not an input to the derivation at all*. Reading it
only to decide `intact` versus `corrected` is the whole difference between the two classes.
[unknown] Whether a wrong value in a *later* block is recoverable the same way (this round derives
block 0 only), and whether the accounting bound stays unique when two candidates fit `u_len` on a
carrier class not measured here (32-bit ELF, LZMA-filtered shared object).

## The rule

The derivation is round 88's chain law with the stored value taken out of the gate
(`corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`): for each `l_info` candidate, `b0 = l_info +
20`, `sz_unc0 > 0`; scan `s1 > b0 + 12` for a plausible `b_info` under block 0's method (or the
PackHeader's) whose chain reaches the end-of-chain sentinel, directly or through the loader-resume
step; require `0 < s1 - (b0 + 12) <= sz_unc0`; with the derived value written, walk and sum `sz_unc`,
reject a candidate whose total exceeds the PackHeader `u_len` (S309), and among survivors take the one
accounting for the most declared bytes, ties to the smaller derived value.

Three outcomes, decided from the stored value only *after* the derivation:

| stored `sz_cpr` | class | output |
|---|---|---|
| equals the derived value | `intact` | byte-identical to the input |
| `0` | `chain-geometry` | one write at `b0+4` |
| any other value (in range or not) | `field-value` | one write at `b0+4` |

Composition, not replacement: the round-87 anchor path runs first (a magic-tampered carrier keeps its
repair, selftest case `magic-class-composed`); when that walk refuses — which a broken first block
makes it do — the derivation runs on the original bytes and the *corrected* bytes are re-validated
through the anchor path, so a correction that does not restore a plausible chain is refused rather
than written.

## Measured (R89-C1)

`python3 -I -B tools/round-89/upx-field-battery.py --root . --repair-cmd tools/round-89/upx-field-value-repair.py --pkg <rea 6.5.0> --work <scratch> --json-out <receipt> --expect-recovered 4`:

| arm | observed |
|---|---|
| real repair | `recovered 4 of 4`, `controls_ok` all true (`N1-refuse-plain`, `N2-corrupt-payload`, `N3-intact-idempotent`, `isolation`), round-88 class regression `recovered 4 of 4`, exit 0 (`.ufo/waves/round-89/pre/c1-candidate-at-declaration.json`) |
| tamper per carrier | jq 252→244, xxd 249→241, libz 201→193, dinit 226→218 (stored `true - 8`); derived values equal round 88's |
| round-88 repair, unchanged (before) | `recovered 0 of 4`, all controls true, exit 1 (`.ufo/waves/round-89/pre/c1-base-r88-repair.json`) |
| `identity` | `recovered 0 of 4`, exit 1 |
| `naive-global` | `recovered 0 of 4`, exit 1 |

Each recovered case passes five arms: the repair exits 0, the only changed bytes lie inside block 0's
four-byte `sz_cpr` window, `upx -t` exits 0, `upx -d` restores the carrier pin, and REA 6.5.0 reports
the declared round-70 procedure count (jq 167, xxd 99, libz 184, docker-init 1268). The counter runs
every repair invocation in a private directory that holds the single input file, and the `isolation`
control records the directory listing each invocation saw (round-88 M88-8 / QUALITY 158).

## Refusal signatures by field class (2-carrier probe, round-89)

`.ufo/waves/round-89/l1/scores/block29-cells.json` — jq and xxd, one field per cell, `upx -t` after the
tamper:

| class | `upx -t` | reading |
|---|---|---|
| `b0.sz_unc := 0` | rc 1 `CantUnpackException: b_info corrupted` | no redundancy for the uncompressed length: refuse |
| `b0.sz_cpr := 0` | rc 1 `CantUnpackException: b_info corrupted` | recoverable (chain geometry) |
| `b0.sz_cpr := stored - 8` | rc 1 `Exception: compressed data violation` | recoverable; the only class reaching the payload stage |
| `b0.sz_cpr := 0xFFFFFFF0` | rc 1 `CantUnpackException: b_info corrupted` | recoverable; the gate fires early, the field is still redundant |
| `b0.sz_cpr := sz_unc + 1` | rc 1 `CantUnpackException: header corrupted` | the arithmetic gate, one stage earlier than `b_info` |
| `b0.method ^= 0xFF` | rc 1 `CantUnpackException: bad method 0xfd at 0x240` | the offset names the block; no redundancy: refuse |
| `l_info.version ^= 0xFF` | rc 0 `Tested 1 file.` | tolerated by `upx -t`, but it breaks this lane's locator: refuse |
| `l_info.format ^= 0xFF` | rc 0 `Tested 1 file.` | same |
| PackHeader `u_len := 0` | rc 1 `CantUnpackException: header corrupted 3` | the PackHeader arithmetic gate (S310) |

[observation] The message does not name the field: `b_info corrupted` covers `sz_unc` and `sz_cpr`
alike (QUALITY 156), and `sz_cpr = sz_unc + 1` answers `header corrupted` instead, because that value
fails a header-level comparison before the block walk starts.

## Limits

- The repair does not decompress what it repairs; the counter's `upx -t`/`upx -d` arms are the guard,
  and a payload corruption is invisible to the structural walk (selftest case
  `corrupt-payload-not-structural`).
- One field on four carriers, block 0 only; later-block values and `p_filesize`/`p_blocksize` stay
  Frontier.
- The counter scores bytes, not provenance; a repair that ran the packer as an oracle is a disclosed
  cheap rule (round 88's M88-4), not excluded by construction.
- The candidate scan keeps round 88's cost profile (QUALITY 160; measured 1.02 s / 14.22 s / 221.85 s
  at 800 / 3,200 / 12,800 crafted candidates) — no new bound is claimed.

## Counting command

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-89/upx-field-battery.py --root . \
  --repair-cmd tools/round-89/upx-field-value-repair.py \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r89/recheck \
  --json-out /fast/scratch/hyaku/kaidoku-r89/recheck.json --expect-recovered 4
```
