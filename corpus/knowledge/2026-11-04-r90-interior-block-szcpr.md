# Packed-ELF `b_info` later-block `sz_cpr`: the interior break is a chain desynchronisation, not a field value (round 90, R90-C1)

source: S313 — UPX v5.2.0 `src/p_unix.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp — opened 2026-11-04, HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`; line 472 `// Consumes b_info header block and sz_cpr data block from input file 'fi'.`; line 485 `fi->readx(&hdr, szb_info);`; line 504 `fi->readx(ibuf+j, sz_cpr);` — the loop reads a twelve-byte header, then exactly `sz_cpr` payload bytes, so the next header's offset is a function of the stored value.
source: S312 (existing, round 89) — UPX v5.2.0 `src/p_unix.h` — the NE32 `packed_struct(b_info)` twelve-byte layout the walk steps by.
source: S311 (existing, round 89) — UPX v5.2.0 `src/p_lx_elf.cpp` — the `un_shlib_1` peek that reports a desynchronised shared object as `corrupt b_info` and the executables' range-checked `unpackExtent` calls.
source: S309 (existing, round 88) — UPX v5.2.0 `src/packhead.h` — the PackHeader `u_len` the accounting preference reads.
source: S314 — UPX v5.2.0 `src/p_lx_elf.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.h — opened 2026-11-04, HTTP 200, 31147 bytes, sha256 `895da5cd72da32bf17846ef4b8088b1ed75dc35ac2506f694098bb30c90c7d89`; line 107 `unsigned o_binfo;  // offset to first b_info` — the packer names the first block's start (`o_binfo = sz_elf_hdrs + sizeof(l_info) + sizeof(p_info)`, `src/p_lx_elf.cpp` line 4000), so the walk starts at a layout boundary rather than at an arbitrary offset.
verified-at: 2026-11-04 (round 90; the landing measurements ran 2026-11-05 03:00-05:00 UTC — receipts in `.ufo/waves/round-90/l1/scores/` and the record in SCORECARD `## 2026-11-04 — round 90`)
recheck: 180d — the counting command below and `python3 -I -B tools/round-90/upx-break-repair.py --selftest`.

## The class

[observation] Round 89's limit — "whether a wrong value in a *later* block is recoverable the same way
(this round derives block 0 only)" — is a class, not an edge. Pack a pinned carrier with `upx 5.2.0
--best`, walk its first contiguous `b_info` segment, and overwrite an **interior** block's `sz_cpr`
with a different in-range value. `upx -t` answers `Exception: compressed data violation`; the round-87
anchor path reports the file `intact` (every `UPX!` word is in place); the round-89 block-0 law finds
block 0's stored value already correct and returns the bytes unchanged. Measured on jq, xxd and
docker-init, both directions (`stored - 7`, `stored + 7`): the unchanged round-89 repair recovers
`0 of 6` with its controls true (`.ufo/waves/round-90/pre/c1-candidate-at-declaration.json`).
[inference] The tamper is not a *value* defect but a *boundary* defect: every block after the tampered
one is read from the wrong offset, so the walk stops early (usually at the embedded loader) and the
suffix is never described. That is why an accounting comparison separates it from an intact carrier:
an intact chain already walks every block it can reach, so any candidate that changes a stored value
skips blocks and accounts for less or the same.
[unknown] A carrier whose suffix self-resumes after the tampered block (no loader stop) is
structurally indistinguishable from an intact file; the tool refuses it and no carrier in this set
exercises it. 32-bit carriers and `--lzma` output are not measured.

## The rule

The derivation is round 88's chain law applied at the walk's **break point** instead of at block 0
(`corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`): take the last block the stored-value walk
could still step, scan every offset above `block + 12` for a plausible `b_info` whose own chain
reaches the end-of-chain sentinel (directly or through the loader-resume step), set `derived =
successor - (block + 12)` bounded by `0 < derived <= sz_unc`, reject `derived == stored`, write it, and
re-walk. Among survivors prefer the candidate that accounts for the most declared bytes; for this class the
PackHeader `u_len` is enforced as a **filter** inside `derive_break` (`total != require_total`
refuses, QUALITY 171 — the docstring said "preference" until the wave's critic measured the code and
the instrument was superseded, `.ufo/waves/round-90/claims.json` `instrument_supersessions`), and the
ranking key's `(total <= u_len, …)` component is inert here because every survivor accounts exactly
`u_len`; ties go to the smaller derived value.

The acceptance test is measured, not asserted: a candidate is written only when it accounts for
**strictly more** declared bytes than the stored-value chain does. Everything else returns the input
byte-identical, which is what keeps `N3-intact-idempotent` true on all four carriers.

| stored `sz_cpr` at the break point | what the suffix does | output |
|---|---|---|
| equal to the derived value | the walk reaches the sentinel on its own | byte-identical (`intact`) |
| any other in-range value | the walk stops at the loader after the tampered block | one write, `derived` |
| no candidate accounts for more | the suffix self-resumes, or the block is the last before a stop | byte-identical, refused |

S314 is what makes scanning legitimate: the packer tracks `o_binfo`, the offset to the first `b_info`, so a carrier's walk has one start and the derivation only ever searches *forward* from a block the stored walk agreed on.

## Measured (R90-C1)

`tools/round-90/upx-later-block-battery.py` scores a repair on three populations built from four
sha256-pinned carriers, each invocation in a private directory that holds the tampered input alone and,
for the blindness arm, under `bwrap` with every pinned carrier path bound to decoy bytes.

| arm | cells | after (round-90 repair) | before (round-89 repair) |
|---|---|---|---|
| `P1` interior later block, jq/xxd/docker-init x `stored - 7`/`stored + 7` | 6 | 6 of 6 | 0 of 6 |
| `P2` block 0 wrong (round-89 class), four carriers | 4 | 4 of 4 | 4 of 4 (composed) |
| `P3` block 0 zeroed (round-88 class), four carriers | 4 | 4 of 4 | 4 of 4 (composed) |
| `carrier_blind` P1 re-scored with the pinned paths blinded | 6 | 6 of 6 | — |
| controls `N1`/`N2`/`N3`/`isolation` | 4 carriers | true | true |
| `cheat_repack` (reproduces the intact packed bytes) | 1 | live unblinded, killed blinded | killed |

A cell is `recovered` only when the repair exits 0, every differing byte lies inside the tampered
four-byte window, `upx -t` answers rc 0, `upx -d` reproduces the carrier's pinned sha256 and REA 6.5.0
reports the original's own procedure/segment/string counts.

## Limits

- Interior blocks only: the *last* block before a chain stop is under-determined (every derived value
  that still leaves a stop before the resume offset accounts for the same total), and the tool refuses
  it.
- The shared object's chain accounts 98,592 of 108,560 `u_len` bytes; that gap is accepted and
  recorded, never repaired, so `libz` is a `P2`/`P3` carrier only.
- The repair does not decompress what it repairs; the counter's `upx -t` and `upx -d` arms are what
  refuse a wrong derivation.
- The derivation is a scan with one sentinel search per candidate: measured cost is reported, not
  claimed linear (`corpus/QUALITY.md` row 160's rule applies to a crafted worst case); the wave measured
  10.3 ms (jq, 13,135 offsets) to 139.5 ms (docker-init, 356,909 offsets) per repair.
- **A last-block tamper is not refused cleanly (measured this round, routed).** When the stored chain
  looks intact and no successor survives, the break-point branch falls through to the round-89 law; on a
  last-block `- 7` tamper of jq (block offset 10,094) and libz (60,124) that law writes the four-byte
  `UPX!` sentinel word, returns rc 0 and leaves `upx -t` red. The frozen counter scores interior cells
  only, so it cannot see this. Routed to round 91 with QUALITY 176.
- **The REA count arm is not perfectly stable on docker-init.** Seven runs of REA 6.5.0 on the identical
  bytes (sha `0bd49c8d…`) reported 1268 six times and 1267 once, so one seat's `P2` cell read `3 of 4`;
  the L1's landing run at `499d2183` reports `P2 4 of 4` with the REA arm required, and both runs are
  disclosed in the round-90 report rather than only the passing one.
- A packer-validated brute force over `1..sz_unc` would repair the same cells; the counter does not
  force the chain walk, so the claim is the capability, not the mechanism (QUALITY 152's standard).

## Counting command

```
python3 -I -B tools/round-90/upx-later-block-battery.py --root . --rev <REV> \
  --repair-cmd tools/round-90/upx-break-repair.py \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <scratch> --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --json-out <receipt>
```

Label `P1 6 of 6; P2 4 of 4; P3 4 of 4`, exit 0, every control true.
