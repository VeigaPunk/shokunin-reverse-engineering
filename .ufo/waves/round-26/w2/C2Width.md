# Round 26 wave 2 — C2Width (critic): is R26-C2 reported wider than its counter?

Seat: KaidokuR26.C2Width. Judged commit: fe3eb4edf410244eff46151a148c8f754be1ce80 (lane HEAD, the L1 SCORECARD, LOG and claim-freezes commit).
Commands ran 2026-10-22T12:58:31Z to 12:59:57Z UTC, in the lane, read-only Git objects only. No REA calls, no tool installs, no web sources.
Scratch: /fast/scratch/hyaku/kaidoku-r26/seats/w2/C2Width/.

## Verdict

**Holds for the number, fails narrowly on wording (fixable).** The 5 to 0 result reproduces and the score delta is correctly stated as 0.
One sentence in the SCORECARD round-26 section (`SCORECARD.md:3075` at fe3eb4ed) reports more than the counter measured, and it misdescribes the wave-1 disclosure.
The LOG entry (`LOG.md:2967`, "R26-C2 5 → 0 of 6 at `46ebfd2f`") and the table row (`SCORECARD.md:3071`) are within the counter.
Impacted axis: calibration.

## Counter reproduction (observation)

Command: `python3 -I -B tools/round-26/c2-calibration.py --root . --rev <REV>` at 12:58:39Z. The instrument at fe3eb4ed has sha256 3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e, which matches the `3b0f6507…7e8e` cited in SCORECARD.
- a0639d8e: exit 1, `5 [('K1', 'mismatch'), ('K2', 'mismatch'), ('K3', 'pass'), ('K4', 'mismatch'), ('K5', 'mismatch'), ('K6', 'mismatch')]`.
- 46ebfd2f, c3277726 and fe3eb4ed: exit 0, `0 [... all 'pass']`.
- `cmp` of my outputs at a0639d8e and 46ebfd2f against the committed receipts printed `before-identical` and `after-identical`.

## What 5 to 0 supports

- Observation: the six frozen predicates K1 to K6 in claims.json fail 5 times at base and 0 times at 46ebfd2f, and they stay at 0 through HEAD.
- Observation: between c27f445e and fe3eb4ed, `git diff -U0 -- SCORECARD.md` has only two hunks, `@@ -23,3 +23,3 @@` (the three owned-axes rows) and `@@ -3061,0 +3062,20 @@` (the appended round-26 section). SHONEN changed by one line. The repair is confined as `causal_separation` says.
- Observation, outside the counter: the repair added new history statements to the rows. I checked two. "rule blocks grew from 9 to 17 in eight commits from `58116aa1` to `4072ebb3` (2026-10-18 and 2026-10-19)" holds.
  A recipe A walk over the 13 SKILL.md commits in that range gives the parent at 9 and increases at exactly 8 commits (58116aa1 10, 265e1aa5 11, 8cc81a84 12, ba06c4dd 13, 28aa7a98 14, 2fba56fe 15, 9c1d1fef 16, 4072ebb3 17). The dates are 2026-10-18 and 2026-10-19.
  `git log -1 75af886a` gives "luna-round-2: per-client REA surface calibration", which matches the row's description of it. (recipe A is the C2Cherrypick extraction, sha256 236dde1d…9b01.)
- Observation by reading, outside the counter: the new K6 pointer `PROVINCE.md:8-14` does state the configured `rea-agents@6.7.0` pins with 207/153, and the round carrier pin `rea-agents@6.5.0` ("Round carrier runs pin the CLI explicitly to the superseded client pin `rea-agents@6.5.0`").

## What 5 to 0 does not support

1. "The six fixed statements agree with the repository" (`SCORECARD.md:3075`). Counterexample: the K rules test frozen predicates, not whether a statement is true.
   - K5 tests only that the cited hex prefixes `result.json` `measured_revision`. It never runs command B.
   - K2 tests only that a substring is present.
   - K6 tests only that the word "contested" is absent and that the pointers fall inside PROVINCE's 303 lines. A false clause without that word would pass, as would a flipped box (already disclosed from MutR25Calib M6 and M9).
   The truth checks I ran above are a seat observation, not the counter's. Label: observation (the rule text in claims.json is K1 to K6).
2. "11 further self-assessment statements ... that disagree with the repository". The wave-1 report labels three of them as partly inference.
   - Item 1: "reading it as a current claim is my inference".
   - Item 8: "calling it a mismatch rather than append-only design is inference".
   - Item 9: "inference that this is stale".
   Observed disagreements: 8. Statements whose staleness is the seat's inference: 3. Label: observation of the report's own labels.
3. The parenthetical "(round-1 sections, capabilities pointers, the round-25 planned field)" misdescribes the 11.
   - C2Cherrypick says "All capability evidence pointers at :619-622 are present". Its capability items 7 to 9 are a missing citation-drift row, a section undercount and a stale saturation sentence, not pointers.
   - The grouping also omits the header lines (:12 lowest-axis, :14 `AXES.md:33-39`), `## Open gaps` (:78-80), the Domain frontier (:81-83) and the planned field at :152-154.
   Label: observation.
4. "They stay open". This holds for the text: all 11 anchors are found at the same lines at fe3eb4ed (12, 14, 46, 55, 80, 82, 152, 615, 631, 907, 3061), and the lines before 3062 changed only at 23-25.
   But item 11's departure is now disclosed in SCORECARD itself at :3066, so "open" there means the text is unchanged and its departure is disclosed. Label: observation.
5. A calibration-axis gain or "the card is calibrated". The text correctly does not claim either; "finite proxy 10 → 10, delta 0" is right. Recorded here only so that later wording does not drift into it.

## Smallest safe correction (wording the report must use)

Replace the first sentences of `SCORECARD.md:3075` with:

> What R26-C2 shows: the six fixed items K1–K6 pass their frozen claims.json rules at `46ebfd2f` (and still at `fe3eb4ed`); 5 of the 6 failed at `a0639d8e`. The rules check counts, revisions, a substring and the absence of the word "contested". They do not check whether each statement is true; K5 does not run command B. It is not a full audit. Wave-1 critic `.ufo/waves/round-26/w1/C2Cherrypick.md` lists 11 further SCORECARD statements left unchanged: 8 observed disagreements and 3 where staleness is the seat's inference (items 1, 8, 9). They are at `:12`, `:14`, `:46`, `:55`, `:78-83` (two), `:152-154`, `:615-624`, `:631-632`, `:907` and `:3061`. Item 11's order departure is disclosed above.

Keep the existing sentence about K6 not reading the box mark. The LOG line, the table row and the planned field need no change.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/w2/C2Width/)

- c2-at-a0639d8e.json bc5cf07b67f3f15354f932568dc5e57a87de2dbf63c84a96dab6970c72974a51
- c2-at-46ebfd2f.json d53f2d2142fbd4fdb5897016299dd662cd2eadc6876ff5d1dc60030cc353f0ae
- c2-at-c3277726.json a977e5ec2b5c19702af171399eeb5b9a4588cba843cd8c47b94b9bec69a04345
- c2-at-fe3eb4ed.json 369c5272f3b7fc2c3f63f755f630c0496f81a332c9ef028c7ed94f2efb2de4a4
- SCORECARD.fe3eb4ed.md 10ae7acf0b46392ab9b194f4a21c08688b539ff71ca5db747ad9e8a1e83ec74b
- LOG.fe3eb4ed.md 421347688dd7924b792a3d821bc1819f14e8dceafa6c912d8e9ad7e3ba17fc5e
- skill-commits.txt ac32e895dd63adbc431f3d9213cd50675798f8b4989248a9d96ec41b77cd4d19
- rule-blocks-walk.txt 5330674047961b30dca5769b3fe3482a3df4614ca1fa047db6fb9150880c55d7

Tool installs: none. Sources: local lane Git objects only.
