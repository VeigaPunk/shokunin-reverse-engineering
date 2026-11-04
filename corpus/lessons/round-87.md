# Round 87 — a magic-tampered UPX ELF is repaired from the packer's own structures

Base `99f8b6a8979978fe02dc3c8f674ce4fdee3ab44b`; declaration `f0ebf61161d08279dca98841461330ad442d3023`
(plan, counter, do-nothing and cheap-rule controls, census before); repair candidate
`b5c7a49e20647bb73117ed1ffb4f68dd69916cd8`; wave dispatch `1c8a76f41f340d575b707d597678efdfed0550c4`;
integration `73c3a29740884b0c134bbe50e3c9b13f141daccf` (measured revision). One v1 wave `r87-w1`,
eleven seats. The round-86 non-author spot-check (`corpus/lessons/round-86-verifier-spotcheck.md` §6)
is the input: its SHONEN-box-2 observation and V86-1 shaped the claim, V86-2 is mined below.

Claim: **R87-C1** (coverage, capability — the PROVINCE Frontier class "anti-UPX stub whose magic is
altered" moves to Core): `recovered 8 of 8`, controls 4/4, 0/4, 4/4, exit 0 at `73c3a297`
(`.ufo/waves/round-87/l1/scores/c1-at-73c3a297.json`); do-nothing 0/8 and naive-global 4/8 at the
declaration. Entry `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M87-1 | an instrument false finding: the round-84 freeze precheck's script pattern has no trailing boundary, so `.ufo/…/c1-control-identity-at-base.json` in a claim string is read as a `.js` script and reported `COUNTER_BLOB_ABSENT` | `.ufo/waves/round-87/l1/freeze-precheck-at-declaration.json` (three findings, two of them `…-at-base.js`) | none — the round-84 selftest has no `.json` path case | `tools/round-87/freeze-precheck.py` (round-84 file byte-identical): trailing `(?![A-Za-z0-9_])`; selftest cases `json-receipt-not-script`, `js-script-still-named` (13/0). Shown able to fail: on the same claim string the round-84 pattern returns `.ufo/waves/round-87/pre/c1.js`, the round-87 pattern does not; on the round-87 container the round-87 tool keeps only the genuine finding (`.ufo/waves/round-87/l1/freeze-precheck-r87-at-declaration.json`) |
| M87-2 | a registry row written with no opened document (round-86 S305, routed V86-2) | `corpus/lessons/round-86-verifier-spotcheck.md` §6 item 2; `corpus/SOURCES.md:221` | CORPUS.md §2b item 1 (prose; no check) | `tools/round-87/registry-opened-check.py` + QUALITY row 153. Shown able to fail: base `2cf0b7ff` → rev `4cc03025` exits 1 naming S305 (`.ufo/waves/round-87/l1/fixcheck-r86-red.json`); base = rev `99f8b6a8` exits 0 |
| M87-3 | an overstated failability rationale: the plan says the zeroed class "needs … a structural repair"; a chain-walk-free heuristic scores 8/8 with REA and byte-identical outputs, so the counter forces the checksum and `l_info` anchors but not the chain walk | `.ufo/waves/round-87/w1/CriticClaim/critique.md` F1; `receipts/cheap-v4-checksum-lite-rea.json` | §9 claim sizing ("build the cheapest control that skips the claimed work") — the controls built (identity, global replace) were not the cheapest variant of the claimed tool | QUALITY row 152; the knowledge entry states the limit; the frozen predicate is unchanged and still met |
| M87-4 | the declaration container named the claimed tool (`tools/round-87/upx-magic-repair.py`) inside the claim object before it existed, so the prefreeze gate reports a genuine `COUNTER_BLOB_ABSENT` (and `COUNTER_PATH_NOT_PINNED` at `b5c7a49e`) | `.ufo/waves/round-87/l1/freeze-precheck-at-candidate.json` | the round-84 gate (it fired) | routed: a capability claim's container keeps the claimed artifact outside the counter-scanned claim strings, or pins it after it lands; disclosed, not repaired in the frozen container |

## Gate

| source | decision | opened 2026-11-04 | located quote and judgment |
|---|---|---|---|
| S306 UPX v5.2.0 `src/stub/src/include/linux.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/stub/src/include/linux.h | **admit** (code, tier A, absent → mined) | HTTP 200, 19689 bytes, sha256 `5de99480…3ea9` (ScribeSources fetch; L1 fetch the same day, same byte count) | line 579: "struct l_info // 12-byte trailer in header for loader (offset 116)" (11 words). Grounds the field layout the repair reads |
| S307 UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | **admit** (absent → mined) | HTTP 200, 373743 bytes, sha256 `551fc867…d2dc` | line 8065: "if (sz_cpr != UPX_MAGIC_LE32) // sz_cpr must be h->magic" (8 tokens). The Linux ELF unpacker's own end-of-file check |
| S308 UPX v5.2.0 `src/packhead.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.cpp | **admit** (absent → mined) | HTTP 200, 13236 bytes, sha256 `41b4a51b…f37a` | lines 64-66: "assert(get_le32(buf) == UPX_MAGIC_LE32); buf += 4; blen -= 4;". The checksum skips the magic, which is why a tampered PackHeader still validates |
| UPX v5.2.0 `src/p_unix.cpp` | **reject** (no row) | HTTP 200, 24181 bytes, sha256 `bf83c413…642e` | line 671 carries the same `sz_cpr` check inside `PackUnix::unpack`, but the Linux ELF classes override `unpack` (`p_lx_elf.cpp` 7755, 9023), so the ELF claim rests on S307. Flip: a carrier class unpacked through `PackUnix::unpack` |

Status changes: S306, S307, S308 absent → mined, used-by `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`.
Recheck cadence 180d (ScribeSources draft; URLs are tag-pinned).

**Sourced claim.** R87-C1's knowledge entry cites S306–S308, opened this round (§2b item 4).

**Assimilation: none.** `merge/kaidoku/` was not consumed this round; no package entry was opened. No `considerthese/` directory exists in this lane.

## Wave attack results carried into the landing

- ReviewerRepair: sound-with-limits; provenance clause holds (imports `argparse/json/struct/sys`, I/O only
  `--in`/`--out`); `rea_recover` is entailed by `identity` (F1); N2 holds through UPX's own integrity check (F3).
- SentinelR87: decoy-sentinel steering (F1, MEDIUM) and a quadratic resume scan (F2) — both fixed before
  measurement (best-candidate selection, memoised walk); I/O contract (F3) fixed (rc 2, 256 MiB cap);
  `--out` follows symlinks (F4) stays a named limit.
- MutationR87: 22 repair mutants (10 killed, 12 survived — population-unexercised guards), 14 counter mutants
  (8 killed, 6 survived); no mutant turned the do-nothing control green.
- CriticClaim: claim survives as a predicate; rationale weakened (M87-3); out-of-population T3/T4 repaired,
  T5 (`p_filesize` zeroed) not repaired, T6 (banner removal) not a tamper of `-t`/`-d`.

## Routed to the next steered round

1. Freeze the CriticClaim v4 heuristic as a second cheap-rule control in a counter revision (M87-3).
2. Keep the claimed artifact out of the counter-scanned claim strings at declaration (M87-4).
3. Counter F5/F6 (uncaught exception → exit 1; N1 counts rc `None` as refusal) and the `--no-rea` label.
4. Repair mutation survivors (version/format cross-check, method checks, PackHeader sanity bounds) need
   population or selftest cases that exercise them.
5. Carried: V86-6 (A3 coverage pointer), V86-7 (round-86 counter false greens), R85-4, planner-seat deviation.
