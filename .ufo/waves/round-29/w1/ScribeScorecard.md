# ScribeScorecard — SCORECARD round-29 section draft

Seat: `KaidokuR29.ScribeScorecard` (leaf; no subagents, no network lookups, no REA, no tool installs,
no git/jj writes anywhere). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only.
All commands below are read-only reads of the lane tree and of `.ufo/waves/round-29/`; drafting ran
2026-10-22T20:1xZ–20:25:04Z.

## Behavior

Read the round-28 section of `SCORECARD.md` (`:3133-3168`) for format, the six routed defects in
`corpus/lessons/round-28-verifier-spotcheck.md`, every receipt under `.ufo/waves/round-29/before/`
and `after/`, `.ufo/waves/round-29/claims.json`, `corpus/lessons/round-29.md`, `corpus/QUALITY.md`
rows 43–47, `corpus/SOURCES.md` S087–S088, both ledgers, and both round-29 knowledge entries. Then
wrote a full round-29 section: title, base + freeze paragraph, claims table (claim / axis / before at
`bacbe9cc` / after at `18be864a` / counting command / verdict "target met as measured"), an
owned-axes paragraph with the knowledge and SOURCES counts, width disclosures, the six-defect
hygiene list with pointers, and a planned field. Nothing was executed against the lane; no counter,
selftest, gate or check was re-run to decorate the report.

## Draft

- Path: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeScorecard/draft.md`
- sha256: `2c90356acba06935c68d01579491ed788345f18bc5a948c26077417e7470cbae` (10 763 bytes, 27 lines;
  `sha256sum draft.md`, 2026-10-22T20:25:04Z)
- The draft has no `Report:` trailer and no lane path other than the pointers it cites; the L1 places it.

## Gates (observed, read-only)

| check | command | output excerpt | exit |
|---|---|---|---|
| the five named revisions exist | `git cat-file -t <rev>` for `bacbe9cc`, `dbd87cfa`, `4fcea978`, `7431096b`, `18be864a` | `commit` ×5 | 0 |
| freeze precedes data | `git log -1 --format='%cI %s'` | `dbd87cfa` `2026-10-22T17:03:06-03:00`; `4fcea978` `17:09:09-03:00`; `18be864a` `17:16:21-03:00` (= 20:03:06Z / 20:09:09Z / 20:16:21Z) | 0 |
| before receipts precede the freeze | read of `before/c1-at-bacbe9cc.txt`, `c2-at-bacbe9cc.txt`, `hex-screen-c1.txt`, `preseen-*.txt`, `select-heldout.txt` | utc `20:01:29Z`–`20:02:58Z`, exit 2/0/0/0/0 as quoted in the draft | – |
| after receipts | read of `after/c1-at-18be864a.txt`, `c2-at-18be864a.txt`, both `*-selftest.txt` | `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` exit 0; `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1` exit 0; `cases=22 failures=0`, `cases=19 failures=0` | – |
| knowledge / SOURCES counts | `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,} \|'` | 112 → 114; 86 → 88 at `bacbe9cc` / `18be864a` | 0 |
| README rows for both entries | `git show 18be864a:corpus/README.md \| grep -n r29` | `:79`, `:80` (map); `:175`, `:176` (index) | 0 |
| r27 patch digest | `git show 7431096b:tools/round-27/c2-xpin-check.py \| sha256sum` | `1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783` (equals the worktree file and the receipt's "patched instrument 1c8259a8") | 0 |
| PROVINCE round-29 annotation | `git show 18be864a:PROVINCE.md \| grep -n 'round 29'` | no match (`round 28` annotation only, at `:94`) | 1 |
| axis rows cited | `grep -n '17/17'`, `sed -n '18,28p' SCORECARD.md` | depth row `:24`, coverage row `:23`, both measured at `ebe2cb4a` | 0 |

## Touched surfaces

- Created (lane, my own report only): `.ufo/waves/round-29/w1/ScribeScorecard.md`.
- Created (scratch): `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeScorecard/draft.md`.
- Nothing else written in the lane; no lane file edited, no git/jj write, no install.

## Findings

- **F1 — observation: a round-29 section is already drafted in the lane working tree.** `git diff
  18be864a -- SCORECARD.md` shows `+22` lines appended after `:3168` (heading "## Round 29 — the
  round-25 EVM naming rule on fresh published-interface carriers, and openchain's `filtered` flag on
  never-fetched selectors"). It contains base, freeze, a two-row claims table, receipts, owned axes,
  width disclosures and the six hygiene items — **and no planned field**, which my draft supplies.
  It also carries numbers that no receipt under `.ufo/waves/round-29/` produces, quoted verbatim:
  `"its no-name rows come from REA inferring `uint256` for `bytes32` (24), `bytes` for `string` (3),
  and from spam ties (3)"`; `"its 38 predicted-true entries come from 19 of the 26 never-fetched
  canonical keys"`; `"the three finite proxies stay saturated at 10"`; `"written from the L1's
  knowledge of the standards (only n04 has a source row, S088)"`; and for the r27 patch `"every line
  outside selftest() is byte-identical to the frozen d8de667f"`. I did not ground any of these five:
  the 24/3/3 breakdown is also stated in `corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md:50-51`
  and `corpus/README.md:79` (pointer, not a wave receipt); "19 of the 26" appears in no receipt I
  read; "three finite proxies" is a claim about the axis table I did not measure; S088 is indeed the
  only new row behind a carrier, but `make-carriers.py` does not record which interface list each of
  the 16 carriers came from; and `d8de667f` is a blob, not a commit, so I could not re-read that
  comparison object by commit id. **Inference:** the working-tree text is the L1's own in-progress
  section, not another seat's; it is uncommitted, so both texts can be reconciled freely.
- **F2 — observation: the lane tree is not clean at drafting time.** `git status --porcelain` (read-
  only) printed ` M LOG.md`, ` M SCORECARD.md`, ` M tools/round-29/prefile-check.sh` and untracked
  `.ufo/waves/round-29/after/c1-at-18be864a.txt` (and further `after/` receipts). QUALITY row 47 and
  `tools/round-29/prefile-check.sh` require a clean tree immediately before the report commit; the
  L1 must settle and commit these, and the after receipts, before filing. Not my edit.
- **F3 — observation: PROVINCE.md carries no round-29 line at `18be864a`.** The Frontier bullet
  "EVM bytecode (extended)" stands as round 28 left it (`:94`). My draft says exactly that;
  it does **not** repeat the round-28 card's "annotated, not moved" wording, which would be false
  for round 29.
- **F4 — observation: the round-29 freeze is itself flagged.** `after/freeze-gates-v2.txt` reports
  `"flagged": [... "round-29"]` with `INSTRUMENT_UNPINNED` for `tools/round-28/c1-heldout-naming.py`
  (M29-3). The draft discloses it inside hygiene item 5 rather than presenting the gate as clean;
  `"clean": 2` in that receipt refers to rounds 24 and 28/claims-c2, not to round 29.
- **F5 — unknown: whether either claim is admitted.** Both counters meet their frozen targets at
  `18be864a` (exit 0 each), and the draft's verdict column says only "target met as measured".
  Admission, and the depth/coverage trend wording, stay with the outside reviewer; the draft asserts
  neither.
- **F6 — observation: M28-4's shape is absent this round.** `claims.json` records
  `"pre_freeze_probe": {"utc": null}`, both pre-seen screens read `overlap=0` at the base, and the
  C1 selectors were screened by name against 58 720 lane words — the evidence the draft cites for
  routed defect 4. I re-read the receipts but did not re-run `preseen.py`; the draft attributes the
  numbers to those receipts, not to a fresh run.

## Numbers I could not ground (acceptance note)

- Not in any `.ufo/waves/round-29/` receipt, therefore **left out of the draft**: the no-name
  breakdown (24 `bytes32`→`uint256`, 3 `string`→`bytes`, 3 spam ties); "38 predicted-true entries
  come from 19 of the 26 keys"; "three finite proxies stay saturated at 10"; per-carrier source-row
  coverage ("only n04 has a source row, S088"); the "every line outside selftest() is byte-identical
  to `d8de667f`" comparison.
- In the draft but measured read-only at drafting time rather than taken from a wave receipt, and
  labelled as such in the draft's own sentence: knowledge files 112 → 114, SOURCES rows 86 → 88,
  `corpus/README.md:79-80` / `:175-176`, the axis-row citations `:23-24` at `ebe2cb4a`, the r27
  instrument digest, and the three commit timestamps (20:03:06Z freeze, 20:09:09Z data, 20:16:21Z
  measured revision).
- Everything else in the table and the hygiene list is quoted from a named receipt with its exit
  code; no number was inferred from a commit message except the "16 REA runs, 304 lookups, 178
  openchain responses" sentence in the freeze paragraph, which comes from `4fcea978`'s subject line
  and is corroborated by the two entry headers I read.

## Out of scope (not done)

- Did not edit `SCORECARD.md`, `PROVINCE.md`, `LOG.md`, `SKILL.md`, `QUALITY.md`, `SOURCES.md`,
  any `corpus/` file, counter, gate or ledger; did not commit, push, or run any git/jj write.
- Did not run any counter, selftest, freeze gate, pre-file check, REA call or network lookup.
- Did not install or update any tool (nothing was needed).
- Did not judge admission, the trend verdicts or the SHONEN boxes.

## Artifacts

| path | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScribeScorecard/draft.md` | `2c90356acba06935c68d01579491ed788345f18bc5a948c26077417e7470cbae` |
| `.ufo/waves/round-29/w1/ScribeScorecard.md` (this report; the hash is of the bytes before this cell was filled in) | `021707837565261ee1f363a3c5552df9ea3401079c91275c99b7691012abce6c` |
