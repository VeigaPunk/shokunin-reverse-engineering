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

| M88-7 | a counter whose `met_target` does not encode the claim's target: `depth-blocks.py` sets `met_target = not unresolved`, so at base it reports `met_target true`, exit 0 with 27 blocks; the claim's 28 lived only in prose and in the receipt | `.ufo/waves/round-88/w1/CriticClaims/receipts/c2-base-rev.json` (base: blocks 27, met_target true, exit 0) and `cheat-c2-oneline-block.json` (a one-line citation-only block: blocks 28, resolved 28, exit 0) | QUALITY row 157 (written this round) | not repaired this round: the instrument is frozen and the claim is judged on its frozen counter. Routed: `--expect-blocks N` as a required argument, so `met_target` is `blocks == N and resolved == N and not unresolved`, with the base arm and the citation-only stub as red controls |
| M88-8 | a counter that hands the answer to the repair: the battery writes `packed`, `n3.out` and `chain.repaired` into the same directory as the repair's `--in`, so a repair that copies the sibling `packed` file scores `recovered 4 of 4` with 0 packer probes | `.ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-sibling-v2.json` (4 of 4, all controls) and `cheats/sibling-repair-v2.py` | QUALITY row 158 (written this round) | not repaired this round (frozen counter). Routed: one private directory per repair invocation, containing only the tampered input, with the sibling-copy cheat as a red control |
| M88-9 | a depth block that cites a document the other claim creates, while the plan declares the claim verifiable without it: block 28's Refs line names `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`, absent at base | `.ufo/waves/round-88/w1/CriticClaims/critique.md` §separability; `depth-blocks.py --rev 0cf8e324` resolves 27 of 27 (the block does not exist at base) | QUALITY row 159 (written this round) | disclosed in the report and the SCORECARD section; the block's text is frozen for this round, so the correction (cite only base-present documents) lands with the next block revision |

| M88-10 | a cost bound asserted instead of measured: the plan called the candidate scan "O(window) per l_info candidate … a hostile file may still cost a linear scan"; the crafted worst case is quadratic in the candidate count and takes minutes at sub-megabyte sizes | `l1/scores/c1-candidate-scan-scaling.json` (L1 probe): 800 candidates / 25,760 bytes → 1.02 s, 3,200 / 102,560 → 14.22 s, 12,800 / 409,760 → 221.85 s, each refusing rc 2 only after the scan; the seat that first reported it (SentinelR88) wrote no report, so its claim was unverified until this probe | QUALITY row 160 (written this round) | measured and stated as a limit in the entry and the report; routed: cap the candidate count (or the total scanned offsets) and refuse with a typed error, with this receipt as the red control |

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

## Wave `r88-w1` — seat results and what the round carried

Fourteen seats in one v1 wave (`r88-w1`, dispatch `20:00`, results `r88-w1-results.json`). Seven delivered a
report: ExecGeomCross, ExecMutation, ExecR87Regress, ReviewerC1, ReviewerC2, CriticClaims, ConnectorR88.
Seven settled with only a partial transcript and no report (provider failure; the wave's results file
records each seat's final text verbatim): ExecMatrix (only `matrix.json`, which reproduces the v1
instrument's 68 cells and its 5 unclassified — an independent confirmation of M88-2), ScoutUpxSrc,
ScoutHostClasses, ScribeEntry, ScribeSources, MutationR88, SentinelR88. Per-seat cause: the results file
carries no per-seat error field (`agent`/`note` only), so the cause for those seven is `unknown` beyond
the truncated transcript — the last text of each is quoted in the round report.

What the delivered seats established:

- **ExecGeomCross** (independent, from-scratch derivation): agreement 4/4 with the committed repair
  (252/249/201/226), derived values equal the intact pre-tamper values, 445,684 offsets scanned;
  docker-init is the only carrier with more than one candidate and the accounting bound is load-bearing
  there (ablation: smallest-derived-only and largest-total-only both pick 136, wrong). Finding: the rule
  as *worded* ("next plausible b_info whose chain reaches the sentinel") yields zero candidates
  contiguously — the loader-resume step is required (M88-6).
- **ExecMutation** (13-row declared-case table over the two C1 instruments): the claimed repair and
  counter still score `recovered 4 of 4` with all controls and the 8/8 regression after every single-edit
  copy; **two survivors** — `R01` (dropping the `derived <= sz_unc0` bound) and `R02` (dropping the
  sentinel-reach test) are not killed by any selftest case, because no fixture exercises those guards;
  `R03`/`R04` (removing the `fits_u_len` preference / the accounting key) are killed on docker-init by
  `geometry-records-u_len`. Routed: selftest cases for the two surviving guards.
- **ExecR87Regress** (no-harm): the frozen round-87 counter with the new repair `recovered 8 of 8`,
  controls true, exit 0 (139.87 s); `--no-rea` 0 of 4 (the `rea_recover` arm is the only difference,
  90.01 s vs 154.95 s); the repair refuses plain originals (rc 2, `no validated PackHeader`) and a
  non-ELF (`not a little-endian ELF`); both counters' selftests green.
- **ReviewerC1** (attack): the frozen predicate reproduces independently (196.9 s). Eight cheaper rules
  scored: R1 smallest-candidate, R2 contiguous-u_len, R3 sentinel-only, R4 `p_blocksize`, R5
  `c_len - 12*blocks`, R6 global fill all fail (0–3 of 4); **R7 packer-as-oracle scores 4 of 4** (M88-4).
- **ReviewerC2** (attack): the depth counter resolves a content-free block that cites a one-line
  knowledge file (the floor is existence+range, never meaning); latent parser defects (`_`/uppercase
  names, nested paths, a fenced example line becomes a phantom block) with no live false negative in the
  170-file corpus; the v1 instrument's 8 "tolerated" cells include 5 no-ops (M88-1/M88-2 confirmed
  independently).
- **CriticClaims** (falsification): C1 "weakened", C2 "falsified as a frozen predicate". Measured
  contradictions: (a) `depth-blocks.py` sets `met_target = not unresolved`, so it reports `met_target
  true` and exit 0 at base with 27 blocks — the claim's 28 lives only in prose and in the receipt
  (M88-7); (b) a one-line citation-only block scores `blocks 28, resolved 28, exit 0` (the counter cannot
  tell a table from a stub); (c) the landed block cites the C1 knowledge entry, absent at base, so C2 is
  not verifiable without C1 (M88-9); (d) the battery leaves `packed`/`n3.out` in the repair's own input
  directory, so a repair that copies the sibling `packed` file scores `recovered 4 of 4` with 0 packer
  probes (M88-8); (e) the battery's `met` does not pin the repair bytes, so two different repair sha256s
  both score met; (f) `PROVINCE.md` cited the declaration-time receipt rather than the measured one.
- **ConnectorR88**: `b_info corrupted` covers both `sz_unc` and `sz_cpr`; the repair refuses the first
  and repairs the second (M88-5, verified independently in `l1/scores/c1-szunc-vs-szcpr.json`); the
  plan's "7-label vocabulary" was stale after the supersession (M88-6). No sibling lane holds this
  ground.

Unverified partial findings carried into the routed list, not admitted: SentinelR88's transcript reports
a crafted "decoy" input making the repair exit 0 while patching a wrong offset and writing a fabricated
`UPX!` into the ELF header, and a clean quadratic in the candidate scan; the seat wrote no report, so
neither is evidence here. The L1's own candidate-scan scaling probe is
`l1/scores/c1-candidate-scan-scaling.json` (the round's measured answer to the DoS question).
