# Round 88 — a zeroed `b_info.sz_cpr` is recovered from chain geometry, and the refusal matrix routes the rest

Base `0cf8e3243059e0bc510b90c880d13d191e78d732`; declaration `7fbe16d455d52e83d42fbfe176e30c7cbb17694b` (plan,
four instruments, three base controls, census before); freeze `70d6f7dec57a874e31bb53ee7f10056cffec656d`
(claims.json, prefreeze gate CLEAN with its red control at `d190c5b5`); instrument supersession `01ffb937`
(matrix v2); wave `r88-w1` fourteen seats. The round-87 non-author spot-check
(`corpus/lessons/round-87-verifier-spotcheck.md`) is the input: its V87-1/V87-2/V87-4 routed items and the
carried M87-3 ("a chain-walk-free heuristic also scores 8/8") shaped both claims.

Claim: **R88-C1** (coverage, capability — a new corruption class enters Core): `recovered 4 of 4`,
`N1`/`N2`/`N3` true, round-87 regression 8 of 8, exit 0
(`.ufo/waves/round-88/pre/c1-candidate-at-declaration.json`); the unchanged round-87 repair scores 0 of 4 on
the same class. **R88-C2** (depth): craft rule block 28 lands, `blocks 28, resolved 28, unresolved []`
(`tools/round-88/depth-blocks.py`). Entries:
`corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`, `corpus/README.md` round-88 note,
`PROVINCE.md` `## Round-88 additions to Core`, `SKILL.md` decision-table row + block 28.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M88-1 | an instrument false positive: `field-tamper-matrix.py` v1 wrote zeros into fields that were *already* zero (`l_info.l_size` on all four carriers, `ph.filter` on the carrier with no filter) and reported `upx -t` rc 0 as `tolerated`, conflating "UPX ignores this field" with "nothing changed" | `.ufo/waves/round-88/l1/scores/c2-matrix-at-declaration.json` v1 run: `per_class` had `tolerated 8`, `noop` did not exist; v2 run on the same population: `noop 5`, `tolerated 3`, `effective_cells 63` | QUALITY row 154 (written this round from the finding; the pre-existing bar had no no-op clause) | `tools/round-88/field-tamper-matrix-v2.py` decides `noop` from the captured `was` bytes before the run and reports `effective_cells`/`noop_cells`; selftest case `vocab-closed` pins the 10-label set. Shown able to fail: v1's receipt holds 5 cells that v2 names `noop`, and the v1 classifier has no path to that label (`grep -c '"noop"' tools/round-88/field-tamper-matrix.py` → 0) |
| M88-2 | a closed vocabulary that met two real messages (`bad method 0 at 0x…` ×4, `IOException: bad seek` ×1) left 5 of 68 cells `other-refusal` instead of extending the vocabulary | v1 receipt `unclassified` had 5 entries; v2 receipt `unclassified []`, `per_class` carries `bad-method 4`, `bad-seek 1` | QUALITY row 155 (written this round) | same v2 instrument; the supersession is recorded in `claims.json` `instrument_supersessions` (`01ffb937`) with the re-taken before record, and the claim's evidence arm now states 0 unclassified |
| M88-3 | a repair rule that was right on three carriers and wrong on the fourth: "the smallest structurally reachable candidate wins" derived 136 for docker-init (true 226), because the structural bound alone leaves three candidates (136, 226, 440) | `.ufo/waves/round-88/pre/c1-candidate-at-declaration.json` first run: `recovered 3 of 4`, dinit `test_ok` false with `compressed data violation` | the round-88 do-nothing/cheap controls (they were scored before the freeze; the miss was caught by the candidate's own run, before the freeze) | the accounting bound: a candidate whose chain sums more `sz_unc` than the PackHeader's `u_len` is impossible, and the survivor accounting for the most declared bytes wins (S309). Shown able to fail: docker-init 136 accounts 123,942,159 of 851,288 and 440 accounts 850,696; only 226 accounts 851,288 — the pre-freeze receipt `c1-candidate-at-declaration.json` records `recovered 4 of 4` after the change, and the repair's selftest `geometry-records-u_len` asserts the accounting numbers |

| M88-4 | the pre-freeze control set did not include the cheapest *different technique*: a repair that runs the packer as an oracle (ascending structural candidates, `upx -t` accepts) scores `recovered 4 of 4` with the frozen counter, so the counter forces the geometry's *outcome* but not its structural derivation | `.ufo/waves/round-88/w1/ReviewerC1/report.md` §2 R7 (the run's receipt under `w1/ReviewerC1/attacks/results/`); the pre-freeze controls were `identity`, `naive-global` and `r87-anchor`, none of which runs the packer | QUALITY row 152 ("a capability claim's cheap-rule controls include a heuristic variant of the claimed tool") — the variant built was a heuristic *of the claimed rule*, not a heuristic *of another technique* | disclosed as a limit in the entry and the report, and routed: the next counter revision scores the packer-oracle rule as a declared control beside the claimed repair, and the claim's rationale is restated as "the outcome is reachable by two techniques; the structural one needs no packer". The frozen predicate is unchanged and still met |
| M88-5 | a routing row over-broad: craft block 28 routes `b_info corrupted` (8 cells, two fields) to one move, but a zeroed `sz_unc` is not recoverable (the repair refuses) and only `sz_cpr` is | `.ufo/waves/round-88/w1/ConnectorR88.md` finding 1 and `sz-unc-probe.json`: zeroed `b0-sz_unc` → `upx -t` `b_info corrupted`, repair rc 2; zeroed `b0-sz_cpr` → same `upx -t` text, repair rc 0 | QUALITY row 156 (written this round from the finding) | the block's text is **not** edited this round — the frozen C2 kill rule says "the block text changed after this declaration" kills the claim — so the correction lands as the next block revision, and the entry, PROVINCE and README now state the disambiguation. Shown able to fail: `w1/ConnectorR88/sz-unc-probe.json` holds both arms |
| M88-6 | record drift after the instrument supersession: the plan's C2 sentence still said "closed 7-label vocabulary" (the v1 set) after v2 landed 10 labels, and the entry's rule text said the candidate's chain "reaches the end-of-chain sentinel" without the loader-resume step every carrier needs | `w1/ConnectorR88.md` finding 2 (the plan sentence); `w1/ExecGeomCross/report.md` finding 1 (a contiguous-only reading yields zero candidates on all four carriers) | none — the round had no post-supersession record sweep | both sentences corrected in `plans/round-88-claims.md` and `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`; the container's predicate and kill rule are untouched (they never named the vocabulary or the resume). Shown able to fail: `python3 -I -B tools/round-88/depth-blocks.py --root . --worktree` still reports 28/28 after the entry edit (the block is byte-identical) |

## Gate

Sources opened 2026-11-04 by the L1 (curl, HTTP status and byte count recorded; the scout seat's independent
fetch is in `w1/ScoutUpxSrc/`).

| source | decision | opened 2026-11-04 | located quote and judgment |
|---|---|---|---|
| S309 UPX v5.2.0 `src/packhead.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.h | **admit** (code, tier A, absent → mined) | HTTP 200, 3678 bytes, sha256 `6cf2b14db8ffac097529f66628a8f1224237d5dccc285c9d320b2bf08cc87672` | lines 55-59: "unsigned u_len; unsigned c_len; unsigned u_adler; unsigned c_adler; unsigned u_file_size;" (10 tokens). Grounds the accounting bound: `u_len` is the packer's own declared uncompressed total, distinct from `c_len` and `u_file_size` |
| S310 UPX v5.2.0 `src/packer.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp | **admit** (code, tier A, absent → mined) | HTTP 200, 44586 bytes, sha256 `ab274d672d0985fa92d83e8c9c867d62ff30a1f31d2fb0b919e6d8826b03e040` | line 546: "throwCantUnpack("header corrupted");" (3 tokens); lines 544-545 carry the arithmetic bounds. Grounds why every PackHeader-field tamper answers `header corrupted` before any checksum |
| UPX v5.2.0 `src/p_unix.cpp` (re-opened) | **reject — unchanged** (no row; r87's reject stands) | HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | lines 682-690 do carry `corrupt b_info` sanity checks inside `PackUnix::unpack`, but r87's flip condition ("a carrier class unpacked through `PackUnix::unpack`") is not met by any carrier this lane holds; the geometry law is grounded on S306 (`struct b_info`) and S309 instead. Flip: a carrier class whose unpack runs through the base class |
| UPX v5.2.0 `src/headers.h` | **reject** (no row) | HTTP 404, 14 bytes | the path does not exist at tag `v5.2.0`; `src/packhead.h` (S309) is where the header struct actually lives. Flip: the file appears at a later tag |

Status changes: S309, S310 absent → mined, used-by `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`.
Recheck cadence 180d (URLs are tag-pinned). Census before exit 0 (213 rows) → after exit 0 (215 rows).

**Sourced claim.** R88-C1's knowledge entry cites S309 and S310, both opened this round (§2b item 4).

**Assimilation: none.** `merge/kaidoku/` was not consumed this round (two-claim budget); no package entry was
opened. No `considerthese/` directory exists in this lane.
