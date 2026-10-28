# W2C2Log — round 49 wave 2: falsification of landed lesson atoms A3, A4, A5 (+ adjacent A2 prose)

Seat `W2C2Log`, lane `kaidoku`, round 49. Landing revision `29883d4ec35a31a8393c4ffb220888c44c0bb022`. Numbers re-derived at round-48 base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` from git objects (`git show <base>:<path>`, `git ls-tree`, `git rev-parse`, `git merge-base --is-ancestor`). No counter imported; no `tools/round-49/` code run. Read-only throughout; the lane tree was not touched.

## Verdict

**Numbers: confirmed. Prose: three sentences misstate their sources, one of them materially (the ScribeReportNumbers cause).**

Every number on lesson lines A3, A4 and A5 reproduces from the base: the LOG.md line sets for `2e785632`, `33f65a91`, `c093e798`; the unnamed set `577a02a5`, `8847042a`, `7fe11332`; 75 seats, 72 report artifacts, missing `C1Battery`, `C1Meaning`, `ScribeReportNumbers`; both raw and final-LF-stripped digests of both round-48 receipts. The defects are in the words around them: (F1) the lesson says the ScribeReportNumbers cause is unknown, but the committed results registry it cites records the cause; (F2) the lesson says the closure cited `2e785632` at 3445 "alone", which the closure does not say; (F3) "newline-stripped" is ambiguous and the verified transform is strip-one-final-LF.

## Findings

| # | Atom / line | Severity | Lesson text (landed, `corpus/lessons/round-49.md:56`) | What the evidence says | Command / receipt |
|---|---|---|---|---|---|
| F1 | A4 | **medium** (misstated cause in a wave-accounting correction) | "`ScribeReportNumbers` has nothing — cause unknown beyond that, no seat transcript was reopened." | The committed registry the lesson cites, `.ufo/waves/round-48/r48-w1-results.json` (base), entry `ScribeReportNumbers`: `"aborted": true`, `"error": "Assignment is to draft measurements/trends from receipts, but available receipt files only establish freeze controls/pre-landing … No report written because doing so would invent numbers, receipts, or evidence."` LOG.md:3446 (base) says the same: "ScribeReportNumbers (aborted because only freeze controls existed when it drafted)". The cause is recorded in two committed places; the sentence says it is unknown and that no transcript was consulted, so the reader is told the cause is absent when it is on the page. Fix: state the cause from the registry (seat aborted by design: pre-landing controls only, no post-landing receipts, report declined to avoid inventing numbers). | `python3 attack-a345.py` key `A4.results_entries.ScribeReportNumbers`; `git show e4f2cfa5…:.ufo/waves/round-48/r48-w1-results.json` (sha256 `8eec161e…2c7`); `git show e4f2cfa5…:LOG.md | sed -n 3446p` |
| F2 | A3 | low (misattribution) | "the closure cited `2e785632` at `LOG.md:3445` alone" | `corpus/lessons/round-48-verifier-spotcheck.md` (base) line 18 says the *fleet report* cited the range 3442–3444 and that "the `2e785632` commit is at LOG.md:3445, outside the cited 3442–3444". The closure does not say "alone", does not present 3445 as its citation, and does not mention 3440/3441 — which is exactly the lesson's new finding. The fleet report's own pointer is `LOG.md:3442-3444` (fleet report, `7b845bef…:.ufo/reports/round-48/kaidoku.md` line 22). Fix: "the fleet report cited `LOG.md:3442-3444`; the closure located it at 3445; LOG.md also names it at 3440 and 3441." | closure line 18; fleet report line 22 (`attack-a345.json` `closure_pointer_lines`) |
| F3 | A5 | low (ambiguous definition) | "the report's `3cc2d72d…` and `c30628ae…` are the newline-stripped digests" | Verified transform is **final LF stripped** (remove one trailing `\n`): `c1` → `3cc2d72d8f65…8f77`, `c2` → `c30628ae7c43…e1ce8`. "Newline-stripped" read as "strip all LF" gives `c1` `03be967d302a…8bae` and `c2` `a6052ef4a7e4…37dc8`, which are not the report's digests. Fix: say "final LF stripped (`sha256(bytes[:-1])`)". The closure line 75/99 uses the right wording ("final newline stripped"). | `attack-a345.json` `A5.c1.final_lf_stripped`, `A5.c1.all_lf_stripped` (same for `c2`) |
| F4 | A4 (omission) | low | A4 correction does not state that LOG.md:3446 itself misnames the no-report seats. | LOG.md:3446 (base) names "no-report seats: C1Battery-2 … and ScribeReportNumbers" and omits C1Meaning. `C1Battery-2/` is a receipt directory (not a seat, as the lesson says); C1Meaning, which has no `.md`, is absent from the LOG list. LOG is append-only so the lesson is the only place the correction lives; it should say that LOG.md:3446 is wrong on both counts. | `attack-a345.json` `A4.LOG_3446_names_no_report_seats: true`; `git show e4f2cfa5…:LOG.md \| sed -n 3446p` |
| F5 | A2 (adjacent, line 56, outside assignment) | low | "the two share exactly 8 hex" | The dead `663f30ee7516942a0120e7de68fe88356e680822` and the real `663f30ee751694fb0970e7de68fe88356e680822` share a **14**-hex leading prefix (`663f30ee751694`) and agree at **36 of 40** positions. "Exactly 8" is false under any reading; the true sentence is that the 8-hex abbreviations match. | `attack-a345.json` `A2_prefix_len: 14`, `A2_positional_equal: 36` |

## Re-derivations that held (no finding)

| Atom | Quantity | Re-derived value at base `e4f2cfa5` | Lesson value | Match |
|---|---|---|---|---|
| A3 | LOG.md lines naming `2e785632` | 3440, 3441, 3445 | 3440, 3441, 3445 | yes |
| A3 | LOG.md lines naming `33f65a91` | 3440, 3441, 3444 | 3440, 3441, 3444 | yes |
| A3 | LOG.md lines naming `c093e798` | 3440, 3441, 3445 | 3440, 3441, 3445 | yes |
| A3 | unnamed (zero hits, case-insensitive, 8-char and 7-char prefixes) | `577a02a5`, `8847042a`, `7fe1133` absent | `577a02a5`, `8847042a`, `7fe11332` | yes |
| A3 | all six are ancestors of base (`merge-base --is-ancestor`) | `2e785632863f043a985f7953775b6aca191f1169`, `33f65a913cfd21a4491a4f8b7ccc8f00069f058d`, `c093e798106eba7e5372f63108ec32748bdc115f`, `577a02a52b68b02d33374e8a3f9a913a257fee7d`, `8847042a140b044dbf335210c965bf7b06b09b4f`, `7fe11332781356ec3d5b0b314698de27dd25b50d` (all exist) | ancestors | yes |
| A4 | seats (`results` length, unique names, `seats` field) | 75 / 75 / 75 | 75 | yes |
| A4 | seats with a `.md` at `w1/<seat>.md` or `w1/<seat>/**.md` | 72 | 72 | yes |
| A4 | seats without | `C1Meaning` (dir has only `receipt.json`), `C1Battery` (no file; `C1Battery-2/receipt.json` is a receipt dir), `ScribeReportNumbers` (no artifact) | same three | yes |
| A4 | zero-byte report artifacts among the 72 | none | — | n/a |
| A4 | role mix (`agent` field) | executor 22, scribe 16, reviewer 9, scout 9, critic 6, mutation-tester 6, connector 2, revenger 2, simplifier 2, sentinel 1 (sum 75) | not stated in lesson; matches LOG.md:3446 and fleet report line 14 | yes |
| A4 | `C1Meaning` cause | results: `status blocked`, `reason=frozen_worktree_dirty` (receipt `dirty: tools/round-48/meanings.py`) | "the closure records frozen_worktree_dirty" | yes |
| A5 | `c1-final-33f65a91.json` raw | `6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e` (2589 B, ends in LF) | `6320c5d2…` | yes |
| A5 | `c1` final-LF-stripped | `3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77` | `3cc2d72d…` (report digest, fleet report line 34) | yes |
| A5 | `c2-final-33f65a91.json` raw | `d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914` (2710 B) | `d1bb87d8…` | yes |
| A5 | `c2` final-LF-stripped | `c30628ae7c439754f570476d570ed57db3361c1a3b5178ecb1c97f065c1e1ce8` | `c30628ae…` (fleet report line 35) | yes |
| A4 (cross-check) | "73 seats produced reports" | fleet report line 14 and LOG.md:3446 say 73; closure line 136 and the lesson say 72 | lesson correct | yes |

## Commands run (all exit 0)

```
export GIT_NO_REPLACE_OBJECTS=1
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; B=e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9
git -C $R show $B:LOG.md                                              # exit 0; 3449 lines
git -C $R show $B:.ufo/waves/round-48/r48-w1-results.json             # exit 0; sha256 8eec161e5e250d6747d1127b104b10dfab7469492cc62813b3651e376fd2b2c7
git -C $R show $B:corpus/lessons/round-48-verifier-spotcheck.md       # exit 0; sha256 a46da21f264b5c6fd23f2fe6c0ab6cadc7dad2788d5093dfc7a776131aac13e8
git -C $R ls-tree -r --name-only $B .ufo/waves/round-48/w1/          # exit 0; 494 paths
git -C $R show $B:.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json   # exit 0; sha256 6320c5d2…ced86e (raw)
git -C $R show $B:.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json   # exit 0; sha256 d1bb87d8…a23914 (raw)
git -C $R rev-parse --verify -q <h>^{commit}; git -C $R merge-base --is-ancestor <full> $B   # for the six commits: all exit 0
git -C /home/vgpnk/Projects/shokunin show 7b845bef80a797b7b90944c6ab2752dbbc9afaa9:.ufo/reports/round-48/kaidoku.md   # read-only, fleet repo; exit 0; sha256 a6895609b910ec8f4511f0783f18f7151c86934bf04495018a503a1e5749914b
git -C $R show 29883d4ec35a31a8393c4ffb220888c44c0bb022:corpus/lessons/round-49.md   # landed lesson; sha256 8df4089f479e8e6cbbdde10cd4193159bc4f6512331f5e7a3846b13dfdefb6fc
GIT_NO_REPLACE_OBJECTS=1 python3 -I -B .ufo/waves/round-49/w2/W2C2Log/attack-a345.py > .ufo/waves/round-49/w2/W2C2Log/attack-a345.json   # exit 0
```

Artifacts (in `.ufo/waves/round-49/w2/W2C2Log/`):
- `attack-a345.py` sha256 `ece73335c294651784285babddb7a1b4fb1f54e79e81cc19b3cd76aa451de3cd` — my own derivation, stdlib + git only, no import from `tools/`.
- `attack-a345.json` sha256 `9ab8f6cdf82e77f59f69d0b216c1ba7e3e399adb27ad52c5e938313fe59d7ff5` — its output (all A2–A5 quantities above).
- `fleet-report-7b845bef.md` sha256 `a6895609b910ec8f4511f0783f18f7151c86934bf04495018a503a1e5749914b` — copy of the fleet report read from the fleet repo commit `7b845bef` (the lane repo does not contain that commit).

Other pinned inputs (sha256 of base blobs, not copied): `c1-final-33f65a91.json` raw `6320c5d2…ced86e`; `c2-final-33f65a91.json` raw `d1bb87d8…a23914`; `C1Meaning/receipt.json` `0a3e7cd5de47880fcfb29b18c84c161137b0443b04b112536defe9263c952226`; `LOG.md` (base) `cd855f88a7a0af65261e59b2a7bd294ad206a6ef2f21cb59b3bb8764346e7b10`; closure (base) `a46da21f…aac13e8`.

## Not run / limits

- The round-48 seats' transcripts were not reopened (the lesson says the same); F1 is decided from the committed registry and LOG.md, not from transcripts.
- `stdout` of the round-48 counters was not regenerated; the "newline-stripped" digests are checked as `sha256(file[:-1])` equal to the fleet report's values. The equality of counter stdout to the receipt file is the closure's claim, not re-run here.
- Snapshot/live-page checks, A1, A6–A9 and the counters themselves are out of this seat's scope and not run.
- The fleet report commit `7b845bef` is absent from the lane object store; it was read from the fleet repo read-only.
- Remaining A3 prose attributions (`7fe11332` "cited with LOG.md:3436-3439") were checked only for the fact of the citation (fleet report line 21), not for LOG.md lines 3436–3439 naming other freeze hashes.

## Actions for the L1 (non-frozen text only)

1. Replace the ScribeReportNumbers sentence in `corpus/lessons/round-49.md` line 56 with the committed cause (F1).
2. Reword the closure attribution for `2e785632` (F2) and the digest definition to "final LF stripped" (F3).
3. Add to the A4 correction that LOG.md:3446 misnames `C1Battery-2` and omits `C1Meaning` (F4).
4. Fix "share exactly 8 hex" to "match in their 8-hex abbreviations" or the 14-hex prefix (F5).
5. The counters were not run by this seat and nothing here is a counter defect; no frozen path is implicated.
