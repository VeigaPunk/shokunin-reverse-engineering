# Round 91 — declared claims (frozen before scoring)

Lane: `kaidoku-shokunin`. Round 91, attempt 1. Base revision: `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`
(branch `main`, the tip at the start of this round). Declaration commit: the commit that adds this
file, `.ufo/waves/round-91/claims.json` and the `tools/round-91/` instruments; every scored receipt
below names that commit, and no instrument byte changes after it except as a disclosed supersession
recorded in `claims.json`.

Owned axes: coverage, depth, calibration, freshness, all at 10.0 on their finite proxies. The
lowest-axis obligation is met by any tied-lowest axis; round 90 entered a capability, so the stagnation
window has not restarted and no waiver is invoked. Claims: two, on distinct axes (coverage, depth),
causally separable: C1's artifacts are `tools/round-91/upx-stop-boundary-repair.py`,
`tools/round-91/stop-boundary-battery.py` and the coverage record; C2 reads only `SKILL.md`'s craft
section and the knowledge file it cites, which exists at the base revision.

**Pre-declaration probes.** Before this file existed, the L1 measured the round-90 repair on last-block
tampers in scratch (`/fast/scratch/hyaku/kaidoku-r91/l1/probe-t7.py`, `probe-cls.py`). Those runs are
exploratory: they set the before-state and the design, and they are copied byte-exact to
`.ufo/waves/round-91/pre/probes/`. No probe output is a scored receipt; every scored receipt is
written after this declaration.

## R91-C1 — coverage (capability: a stop-boundary class enters Core as a measured refusal)

**Class `T7-chain-stop-boundary`.** A packed UPX 5.2.0 `--best` little-endian ELF x86-64 whose *last*
`b_info` block before the chain stop carries `sz_cpr` moved by −7 or +7 (both in range,
`0 < value <= sz_unc`). Four pinned carriers (`jq`, `xxd`, `libz`, `docker-init`), two directions: eight
cells. Measured at base: the round-90 repair returns `rc 0` on all eight cells; two write bytes outside
the tampered window (`jq` −7, `libz` −7; the sentinel word, QUALITY 176), six return the broken file
unchanged (rc 0 on a file `upx -t` still rejects; QUALITY 167).

**Candidate.** `tools/round-91/upx-stop-boundary-repair.py`: identical to the round-90 repair in every
branch except the one it previously fell through. When no successor decides the walk, the repair runs
`upx -t` on its input: green → the input is returned byte-identical (`class intact`); red → a typed
refusal (`stop-boundary: …`, rc 2), no output file.

**Frozen predicate (the same sentence in this plan, the counter's code, the label and the container):**

`refused 8 of 8; unsafe 0; intact 4 of 4` from `tools/round-91/stop-boundary-battery.py --repair-cmd
tools/round-91/upx-stop-boundary-repair.py`, exit 0, AND the regression arm
`tools/round-90/upx-later-block-battery.py --repair-cmd tools/round-91/upx-stop-boundary-repair.py
--expect "P1 6 of 6; P2 4 of 4; P3 4 of 4"` exit 0 (the round-90 interior and block-0 classes keep their
repairs, QUALITY 161).

- `refused` — rc ≠ 0 and no output file; `unsafe` — rc 0 with bytes outside the window or a length change;
  `intact` — rc 0 and byte-identical output on the intact carrier.
- The label must equal the `--expect` string exactly; any control false, any counter or repair sha256
  differing from the container pins, or any carrier pin drift is a failure.

**Before (do-nothing control, the round-90 repair under the same frozen counter):**
`refused 0 of 8; unsafe 2; intact 4 of 4` — `.ufo/waves/round-91/pre/c1-base-round90-repair.json`
at `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`. The base cannot reach the target, so the target is not a
do-nothing outcome.

**Named cheap rules (must score below target; declared before data):**
- *blanket refusal* (refuse every last-block input): `refused 8 of 8` but `intact 0 of 4` → fails.
- *geometry-only refusal* (refuse when the walked total is below `u_len`): the chain total cannot see a
  `+7` tamper (its total still equals `u_len`), so it does not refuse all eight cells, and it refuses the
  intact `libz` (its total is below `u_len` on the intact file too) → fails. Scored by ExecCandidate in
  wave `r91-w1`; the receipt is the measured count, not the predicted one.

**Kill rule.** Any label differing from the frozen predicate; `unsafe` > 0; `intact` < 4; the regression
label differing from `--expect`; a counter or repair sha256 differing from the pins; a receipt taken at a
revision other than the measured one; the target narrowed after any scoring.

**Limits declared before data.** The class is refused, not repaired: no successor and no decompression
decides the last block (the geometry leaves `sz_cpr` under-determined). The intact arm depends on
`upx -t` as the packer's verdict on the input. The repair reads no carrier path, but that is an
audit-level claim, not a counter arm (QUALITY 168 is carried by the round-90 battery's `carrier_blind`
arm, which the regression run includes).

## R91-C2 — depth (craft rule block 31: a stop-boundary refusal table)

**Claim.** `SKILL.md`'s `## Queue-drain craft` section gains block 31: a decision table routing the three
measured base classes of the stop-boundary tamper to the guard that answers each, each row citing a
`QUALITY.md` criterion present at the base revision. Blocks 1–30 are not retrofitted (history is measured,
not rewritten); the shape clause applies from block 31 (`--shape-from 31`).

**Counter.** `tools/round-91/depth-blocks-v3.py --root . --rev <D> --expect-blocks 31 --expect
"blocks 31, resolved 31, required-shaped 1/1"`, exit 0. v3 is v2 (citation resolution, 25-word and
two-span floor) plus a decision-table clause (header, separator, ≥3 body rows of ≥4 cells) for every
block at or after `--shape-from`. `--prose-proof` runs v2 and v3 on the same prose and table fixtures
and must report `control_killed true`.

**Before:** base `2135f6e1d…`: `blocks 30, resolved 30, required-shaped 0/0`, met false —
`.ufo/waves/round-91/pre/c2-depth-at-base.json`. The shape-blind predecessor (`tools/round-89/depth-blocks-v2.py`)
accepts a prose block that v3 refuses (`.ufo/waves/round-91/pre/c2-prose-proof.json`), so the shape clause is
not a no-op.

**Kill rule.** `blocks != 31`; `resolved != 31`; block 31 citing a path absent at the base revision
(QUALITY 159); block 31's text changed after declaration; the prose control not killed.

**Limits declared before data.** v3 measures the table's shape and its citations, not that its routing is
correct (QUALITY 175 names this). Block 31 describes behaviour measured at base, so it verifies without
C1 landing.

## Calibration sweep (not claimed)

`tools/round-91/record-cells.py` re-derives the claim rows of rounds 89–90 in `SCORECARD.md` from
committed bytes (the QUALITY 173 and round-90 D-3/D-5 class: a receipt named in a row must exist at the
row's revision, and a revision the receipt names must agree with the row's). Base `2135f6e1d`: 5 mismatches on
4 rows (`.ufo/waves/round-91/pre/c3-at-base.json`). It is reported as a measured calibration defect in
`corpus/lessons/round-91.md` `## Mistakes`; it is not a claim, its score is not moved, and the round-90
records are corrected by new rows, never rewritten (CORPUS.md rule: corrections are new entries).

## Frontier step (CORPUS.md §SOURCES, contract v1)

- The sourced claim: C1's knowledge entry rests on S313 (`src/p_unix.cpp`, UPX v5.2.0), re-opened this
  round (2026-11-05, HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e`,
  line 496 `if (sz_cpr > sz_unc || sz_unc > (int)blocksize)`).
- Mistakes mined: M91-1 (the round-90 repair's rc-0 unsafe and silent writes were known as QUALITY 176/167 but
  had no counter arm); M91-2 (record cells of rounds 89–90 name artifacts that do not resolve, the calibration
  sweep above).
- Assimilation: none — no `merge/kaidoku/` package and no `considerthese/` directory exist in this lane.
