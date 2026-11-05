# Packed-ELF `b_info` chain geometry: a zeroed first-block `sz_cpr` recovered from the chain (round 88, R88-C1)

source: S309 — UPX v5.2.0 `src/packhead.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.h — opened 2026-11-04, HTTP 200, 3678 bytes, sha256 `6cf2b14db8ffac097529f66628a8f1224237d5dccc285c9d320b2bf08cc87672`; lines 55-59: "unsigned u_len; unsigned c_len; unsigned u_adler; unsigned c_adler; unsigned u_file_size;"; grounds the PackHeader fields the geometry bounds its derivation by, and the header checksum field at line 66.
source: S310 — UPX v5.2.0 `src/packer.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp — opened 2026-11-04, HTTP 200, 44586 bytes, sha256 `ab274d672d0985fa92d83e8c9c867d62ff30a1f31d2fb0b919e6d8826b03e040`; lines 544-546: "if (ph.c_len > ph.u_len || (ph.c_len == ph.u_len && !allow_incompressible) ||"; the next line raises "header corrupted", so a PackHeader field tamper fails before any checksum is consulted.
source: S306 (existing, round 87) — UPX v5.2.0 `src/stub/src/include/linux.h` — `struct b_info`/`struct l_info` layout: the 12-byte `b_info` header the chain walk steps by.
source: S307 (existing, round 87) — UPX v5.2.0 `src/p_lx_elf.cpp` — line 8065: "if (sz_cpr != UPX_MAGIC_LE32) // sz_cpr must be h->magic": the Linux ELF unpacker's end-of-chain check.
verified-at: 2026-11-04 (round 88; measured revision and receipt in SCORECARD `## 2026-11-04 — round 88`)
recheck: 180d — `python3 -I -B tools/round-88/upx-chain-repair.py --selftest` (11 cases, failures 0) and the counting command below.

## The class

[observation] Zeroing the `sz_cpr` word of the first `b_info` block of a packed UPX 5.2.0 little-endian
ELF is a *metadata* corruption, not a magic-word corruption: `upx -t` answers
`CantUnpackException: b_info corrupted` and `upx -d` refuses, while every `UPX!` word is still in
place. Measured on the four round-70 carriers (jq, xxd, libz, docker-init; sha256-pinned): the round-87
anchor repair refuses all four with `p_info is not followed by a plausible b_info`, because its chain
walk starts at `l_info + 20` and cannot take a first step. Do-nothing (`identity`) and the round-87
cheap rule (`naive-global`) recover 0 of 4 as well
(`.ufo/waves/round-88/pre/c1-control-{identity,naive-global,r87-anchor}-at-base.json`).
[inference] The block's length is recoverable because the chain is a *layout*: `b_info` records are
contiguous, each occupying `12 + sz_cpr` bytes, so the next block's offset fixes the previous block's
`sz_cpr` exactly. The corrupted field is redundant with the block boundaries the file still carries.
[unknown] Whether the derivation is unique on carrier classes not measured here (a 32-bit ELF, an
LZMA-filtered shared object with a non-zero `cto`, a multi-member overlay); the round's own ambiguity
data is below.

## The rule

Derive `sz_cpr` from chain geometry, bounded twice:

1. **Structural bound.** For each `l_info` candidate (found by its own `u_file_size`/version/format
   cross-check, round 87's locator), let `b0 = l_info + 20` and require `sz_cpr0 == 0` and
   `sz_unc0 > 0`. Scan `s1 > b0 + 12` for bytes that form a plausible `b_info` under block0's method
   (or the PackHeader's) whose own chain reaches the end-of-chain sentinel — directly, or through
   the round-87 loader-resume step (on every measured carrier the contiguous chain stops at the
   embedded loader: jq stops at 10097 with the sentinel at 13988 and the resumed chain at 13228, so
   a contiguous-only reading yields zero candidates); require `0 < s1 - (b0 + 12) <= sz_unc0`.
2. **Accounting bound.** With the derived value written, walk the chain from `b0` (and its resumed
   segment past the embedded loader) and sum the blocks' `sz_unc`. A candidate whose total exceeds the
   PackHeader's `u_len` (S309) is impossible; among the survivors the one accounting for the most
   declared bytes wins, ties broken by the smaller derived value.

Measured effect of the accounting bound on docker-init: three candidates survive the structural bound
(derived 136, 226, 440; true value 226). 136 accounts for 123,942,159 bytes against `u_len` 851,288 and
is impossible; 440 accounts for 850,696; 226 accounts for exactly 851,288 and wins. On the shared
object the chain accounts for 98,592 of 108,560 (its appended data is not chain data), so the single
structural candidate is accepted — a named limit, not a claim of exactness.

## Measured (R88-C1)

`python3 -I -B tools/round-88/upx-chain-battery.py --root . --repair-cmd tools/round-88/upx-chain-repair.py --pkg <rea 6.5.0> --work <scratch> --json-out <receipt>`:

| arm | observed |
|---|---|
| real repair | `recovered 4 of 4`, `controls_ok` all true, round-87 regression `recovered 8 of 8`, exit 0 (`.ufo/waves/round-88/pre/c1-candidate-at-declaration.json`) |
| derived `sz_cpr` per carrier | jq 252 (accounts 30,800/30,800), xxd 249 (38,928/38,928), libz 201 (98,592/108,560), dinit 226 (851,288/851,288) |
| `identity` | `recovered 0 of 4`, exit 1 |
| `naive-global` | `recovered 0 of 4`, exit 1 |
| round-87 repair, unchanged (base state) | `recovered 0 of 4`, all controls true, exit 1 |

Each recovered case passes five arms: the repair exits 0, the only changed bytes lie inside block 0's
four-byte `sz_cpr` window, `upx -t` exits 0, `upx -d` restores the carrier pin, and REA 6.5.0 reports
the declared round-70 procedure count (jq 167, xxd 99, libz 184, docker-init 1268).

## Refusal-signature matrix (round-88 evidence, R88-C2)

`tools/round-88/field-tamper-matrix-v2.py` over 4 carriers × 17 single-field tampers: 68 cells, 63
effective, 0 unclassified (`.ufo/waves/round-88/l1/scores/c2-matrix-at-declaration.json`). Per class:
`header-corrupted` 35, `b_info corrupted` 8, `corrupt b_info` 4, `p_info corrupted` 4,
`compressed data violation` 4, `bad method` 4, `bad seek` 1, `tolerated` 3, `noop` 5.
[observation] `l_info.l_checksum` is tolerated on the three executables (`upx -t` rc 0, `upx -d`
identity true) and fatal on the shared object (`IOException: bad seek`); `l_info.l_size` and the
absent `ph.filter` are no-ops (the bytes were already zero), never "tolerated fields".

## Limits

- The repair does not decompress the block it repaired; the counter's `upx -t`/`upx -d` arms, not the
  repair, refuse a wrong derivation.
- One field on four carriers. `p_blocksize`, `p_filesize`, adler and other PackHeader-field tampers are
  measured by the matrix but are not repaired this round.
- A non-zero but wrong `sz_cpr` is left alone by the composed repair (selftest case
  `szcpr-nonzero-not-derived`): the class is a *zeroed* length, not an arbitrary one.
- The counter scores bytes, not provenance: a repair that read the carrier and re-packed it would score
  the same.
- The class is the *compressed* length. `upx -t` answers `b_info corrupted` for a zeroed `sz_unc`
  too (4 of the 8 `b_info corrupted` matrix cells) and there is no redundancy for the uncompressed
  length: the repair refuses (`sz_unc0 == 0` guard). A packer-as-oracle repair (ascending
  candidates, `upx -t` accepts) reaches the same 4 of 4 on this population — disclosed as a limit,
  not claimed away (`w1/ReviewerC1/report.md` §2, R7).

## Counting command

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-88/upx-chain-battery.py --root . \
  --repair-cmd tools/round-88/upx-chain-repair.py \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r88/recheck --json-out /fast/scratch/hyaku/kaidoku-r88/recheck.json
```
