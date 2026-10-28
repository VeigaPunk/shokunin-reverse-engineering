# W2C2Rescore — round 49 wave 2, R49-C2 calibration (post-landing)

Seat: W2C2Rescore. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Landing `29883d4ec35a31a8393c4ffb220888c44c0bb022`. FREEZE `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`. Attack target: the C2 before→after numbers and the landed bytes that the counter reads. Counter frozen; no counter or landed text was edited (all probes are in-memory overlays or in a clean clone, `git clone --shared` checked out detached at the landing revision).

## Verdict

**Numbers reproduce exactly; the 9 → 0 is genuine for the nine atoms as the counter defines them, but three frozen clauses are under-bound.** Before (FREEZE): exit 1, `mismatches 9`. After (landing, with `--battery`): exit 0, `atoms_total 9`, `mismatches 0`, `battery.failing []`, 16 mutations each red on exactly its own atom, do-nothing red on all nine. Both printed JSONs are byte-identical to the L1's recorded receipts (`controls/ctl-c2-0-do-nothing.json`, `l1/scores/c2-at-landing.json`).

Three clauses of the plan sentence are not enforced by the frozen code (F1–F3 below). Each is a counter defect to report, not patch: the landed text satisfies the counter, and the counter would also pass text that violates the plan sentence. Two further items are disclosed limits, confirmed by run (F4, F5). One is a reading caveat on the headline (F6).

## Findings

| # | Sev | Attacks | Clause (plan sentence) | Probe | Observed | Expected per plan |
|---|---|---|---|---|---|---|
| F1 | medium | A7 `EX_USAGE` | "the teaches cell states `EX_USAGE is 64` and **no other status** for `EX_USAGE`" | S148 teaches: append "; an older mirror prints EX_USAGE=2" (or "EX_USAGE was 2 in 1994") | **exit 0, A7 green** (`attacks/attack-overlays.txt` X1, X1b) | red A7 |
| F2 | medium | A8 search log | "carries **exactly one** round-48 entry (marked `late entry`)" | insert an unmarked second `- 2026-10-28 round 48 …` line after the late entry | **exit 0, A8 green** (X2) | red A8 |
| F3 | medium | A6 locator | "locator = **the heading the quote sits under**" | S147 quote 1 replaced by a section-3 sentence ("In a word, an exception, far from “proving” a rule, conclusively refutes it.", 13 words, present in the snapshot under `3. The Problem of Demarcation`); anchor's existing parenthetical "(they precede `3. The Problem of Demarcation`)" kept | **exit 0, A6 green** (V1, `attacks/a6-locator.txt`). Same overlay with the parenthetical removed → red A6 (V2) | red A6 |
| F4 | low | A8 search log | "exactly one round-49 entry" | a second round-49 entry dated `2026-10-29` | **exit 0, A8 green** (X6): entries are matched by the literal `- 2026-10-28 round 49` prefix | red A8 (or document the date filter) |
| F5 | disclosed, confirmed | A8 | `identified` "asserted by the lane, not derivable" | `Identified 3, screened 3` → `Identified 300, screened 3` | exit 0 (X4) | green (the disclosed limit, as written) |
| F6 | disclosed, confirmed | A6/A7 | snapshots not bound to the live page | sysexits snapshot with an appended `EX_USAGE is 2` line; S148 sha pin re-computed and rewritten in the same overlay | exit 0 (`attacks/x8-forged-snapshot.txt`) | green (the disclosed limit, as written). Note the counter also does not read the snapshot's contents beyond the quote and `EX_USAGE 64`, so a contradicting line in the snapshot is invisible |

Reading caveat (not a counter defect, a headline caveat for the L1):

- **F7 — "9 → 0" measures presence and agreement of correction records, not repair of the round-48 record.** At FREEZE the nine reds are `lesson line A1..A7 absent` (seven), `round 48: 0 matching search-log entries`, `round 49: 0 …` (A8) and `SCORECARD … 0 sections` (A9): every one is an absent correcting record. The do-nothing overlay at REV gives the same nine reds (`ctl-c2-0`, byte-identical). The counter also *requires* the defective text to remain: A1 reads REV's `corpus/lessons/round-48.md` and requires its header to still name `0f06251b…` (byte-identical to base, enforced). So the count reaches 0 by documenting the defects beside the unchanged record, which is the plan's append-only design. The landed "counted and repaired" wording should not be read as "the round-48 record no longer carries the wrong statements". Measured: `corpus/lessons/round-48.md` at REV is the base blob; the header still reads `0f06251b`.

## What was run (exact commands)

Clone: `D=/fast/scratch/hyaku/kaidoku-r49/W2C2Rescore/clone.m6J4` (`git clone --shared` of the lane, `checkout --detach 29883d4e…`, `rev-parse --show-toplevel` = `$D`; FREEZE is an ancestor; `git log FREEZE..REV` = 6 commits, none touches `tools/round-49` or the plan per the counter's own walk). Environment: `TMPDIR=HYAKU_SCRATCH=…`, `GIT_NO_REPLACE_OBJECTS=1`, `python3 -I -B`.

| Run | Command (abbrev.) | Exit | stdout sha256 | Receipt copy |
|---|---|---|---|---|
| before, clone | `python3 -I -B $D/tools/round-49/c2-mismatch.py --root $D --rev decc5697… --freeze decc5697…` | 1 | `7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4` | `receipts/c2-before-freeze.json` |
| after, clone, battery | `… --root $D --rev 29883d4e… --freeze decc5697… --battery` | 0 | `0cad6d5cfb525227be6af09d6cd6b6115818cee4436180a902a8d1847f490f86` | `receipts/c2-after-landing-battery.json` |
| after, clone, no battery | `… --rev 29883d4e… --freeze decc5697…` | 0 | `5f403b7479a9ee5a657c550079b5fbf54d53fe59c6d63d9e311dbaaec785be6c` | `receipts/c2-after-landing.json` |
| before, lane root | same as before, `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | 1 | `7aa900e1…` (identical) | `receipts/c2-before-freeze-laneroot.json` |
| after+battery, lane root | same as after+battery, lane root | 0 | `0cad6d5c…` (identical) | `receipts/c2-after-landing-battery-laneroot.json` |

Attack driver outputs (sha256 in full): `attacks/attack-overlays.txt` `50278f5cab99abdaf47797e70f80610c2e16a2ea46bef6d7053ddc70d3176f83`; `attacks/a6-locator.txt` `11c1c6c0322211f4d81be4fe070175254d15637b547781fdf0448356d16fb14f`; `attacks/x8-forged-snapshot.txt` `ae2d1e1507c9c486373f90bb96cf9679556b3dff8b8952d3c4fe3b6419db3e6f`. Drivers `attack.py`, `a6.py`, `x8.py` import the frozen counter from the clone with `importlib` (`dont_write_bytecode`), call its `Git`, `Overlay` and `score`, and write nothing to the clone. Every hash of the copied receipts is in `receipts/SHA256SUMS`; the clone itself is deleted after this report.

## Field-by-field comparison with recorded receipts

| Recorded file | sha256 | Compared with | Result |
|---|---|---|---|
| `.ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json` | `7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4` | before, clone | `cmp` equal (1208 bytes) |
| `.ufo/waves/round-49/l1/scores/c2-at-landing.json` | `0cad6d5cfb525227be6af09d6cd6b6115818cee4436180a902a8d1847f490f86` | after+battery, clone | `cmp` equal (3293 bytes) |
| `.ufo/waves/round-49/l1/scores/c2-at-3847f393.json` (intermediate landing) | `e5b2c2d87f2ae5b826521c52fc1d6495d9c2e46e7fe9582eafa8d530d6cd4620` | — | exit 1, `mismatches 2` (A6, A7: teaches did not open `supersedes S14x —`), battery `mutation set incomplete: 15 of 16` plus red-cascades; counter sha `9b80b3b0…` (unchanged) |

`counter_sha256` = `counter_sha256_at_freeze` = `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` in every receipt above; `git show FREEZE:tools/round-49/c2-mismatch.py | sha256sum` gives the same value, and the file is unchanged at REV. Freeze-integrity checks passed in every run (no exit 2).

Per-atom reasons at FREEZE (all nine red by absence, see F7): A1–A7 `lesson line Ax absent`; A8 `round 48: 0`, `round 49: 0 matching search-log entries`; A9 `0 sections`. At REV: all nine `ok: true`, `why: []`.

Battery at REV: 16 mutations, each `red == [its atom]` and `noop == []`, `ok true` (A1 swap; A2 non-commit; A3 ×4 incl. duplicate line; A4 off-by-one; A5 zeroed digest; A6 snapshot bytes, anchor section, word count; A7 snapshot bytes, second status; A8 late marker, stop rationale; A9 contradictory line). Do-nothing: 102 changed paths restored to FREEZE, red `[A1..A9]`.

## Checked and clean (no finding)

- Freeze integrity: `merge-base --is-ancestor FREEZE REV` true; no commit in FREEZE..REV touches `tools/round-49` or the plan; counter bytes equal FREEZE blob.
- A4 seat accounting re-derived by hand: 75 seats in `r48-w1-results.json`; `.md` artifacts absent for `C1Battery` (only `C1Battery-2/receipt.json`, a different name), `C1Meaning` (only `receipt.json`; `LabC1Meaning.md` is another seat), `ScribeReportNumbers` (none). The lesson's `reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers` agrees with the counter and with the round-48 closure's item 7.
- A2 dead hash `663f30ee7516942a0120e7de68fe88356e680822` is not a commit; `…751694fb0970e7de68fe88356e680822` is.
- A8 rows: `146 → 149`, round 49 included 2 (S147, S148), excluded 1 (S149 rejected); round 48 `144 → 146`, included 1, excluded 1 (S146). Consistent with the registry at base/REV.
- Landing history: `3847f393` → `188ddeea` → `b58f9b19` → `29883d4e` edited only `corpus/SOURCES.md` and `corpus/lessons/round-49.md` (non-frozen). The first landing score (`c2-at-3847f393.json`) was red (mismatches 2); the intermediate scores between that commit and `29883d4e` are not in the lane's record, so they are not counted here. The counter bytes and the frozen paths did not change across the commits. For the calibration record: the 0 at `29883d4e` follows non-frozen edits whose stated purpose was the counter's own reds (teaches opening with the `supersedes` form, corrections section moved last).

## Routing

- F1, F2, F3 are counter clauses under-binding the plan sentence. Per the freeze rule they are reported as misses; the frozen counter stays as is. A round-50 counter could bind: "no other status for EX_USAGE" over all `EX_USAGE` occurrences in the teaches cell; exactly one round-48 entry over all `2026-10-28 round 48` lines (marked or not); the quote's own locator (the heading section_of returns, equality not substring).
- F4 and F5 are the same family (search-log entries matched by a filter, and an asserted count).
- F6 is the disclosed snapshot limit, confirmed.
- F7 is for the L1's wording of the headline.

## Not run

No live web re-fetch of the SEP or man7 pages (disclosed limit; out of scope for a consistency counter). No build or test of the rest of the lane. Only the C2 counter and its overlays were executed.
