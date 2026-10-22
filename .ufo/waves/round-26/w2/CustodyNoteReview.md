# CustodyNoteReview — Kaidoku round 26, wave 2 (falsify)

Item: the SKILL.md superseding note at the end of the round-25 custody section
(`## Superseding note — round 25 custody subject landed; the filed wording above
is superseded`), added by commit c327772653badd3b19b3954e1f8713973aa3f93e
(SKILL.md lines 834-881 there). Method: read-only git on the lane, judged at
c3277726; fleet file read directly. Every check ran 2026-10-22, exit 0 unless
stated; full raw output in scratch (sha256 below). Lane tip moved during review
(fe3eb4ed, then 003de8cc); all "tip" claims were re-verified at c3277726,
fe3eb4ed and 003de8cc and hold at all three.

## Clause-by-clause verdicts (note text -> evidence -> verdict)

1. "appended after the round 25 section above and changes no filed byte of that
   section" — `git diff --numstat c3277726^ c3277726 -- SKILL.md` = `49  0`;
   single hunk `@@ -830,3 +830,52 @@` (pure insert at EOF). Section bytes
   sha256-identical between a4ab912a and c3277726^ (both `06cda128…6754a`).
   Verdict: holds.
2. "section above was written at the claims freeze commit a4ab912a…" —
   `git log -S 'Explicit instrument-reference custody' -- SKILL.md` returns only
   `a4ab912a round-25: freeze explicit custody contract before implementation`;
   freeze-gate receipt names `"freeze": "a4ab912a…"`. Verdict: holds.
3. "when the subject tools/round-25/instrument-custody.py did not exist" —
   `ls-tree a4ab912a tools/round-25/` lists only ruler.py (blob 29a4e07d).
   Verdict: holds.
4. paraphrase "not implemented at this phase … unavailable verdict with exit 2 …
   cases therefore not observed" — SKILL.md:787-788 at c3277726: "The candidate
   `tools/round-25/instrument-custody.py` is not implemented at this phase;
   missing candidate is unavailable2 and cases are not observed." Registry exit
   map has `2 unavailable/…`. Verdict: holds (faithful paraphrase).
5. "superseded from commit fafdd283… onward" — subject blob exists from
   fafdd283 in every later tree checked. Verdict: holds.
6. "fafdd283 (parent a4ab912a) added one file … 514 lines, 21190 bytes, sha256
   54c43cdc…, blob 8a6e21f18e…, mode 100755" — `show -s` parent matches;
   stat "1 file changed, 514 insertions(+)"; blob: 21190 bytes, 514 lines,
   sha256 54c43cdc01930fcb58f14053d8099f4b28352147656a05d811574cc74e7d34fb;
   ls-tree mode 100755, blob 8a6e21f18e805c7ce44e03a9a4872e9063073c32.
   Verdict: holds.
7. "the same blob is at the current lane tip" — blob 8a6e21f… present at
   c3277726, fe3eb4ed, 003de8cc. Verdict: holds.
8. "ruler sha256 at the tip is 20fe3f3d…, cases sha256 at 62feef9c is
   6c851cd7…; ruler and 34 pairs unchanged" — ruler blob 29a4e07d identical at
   62feef9c…tip, content sha256 20fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179
   b179acb6fda99d0532; cases.json blob 99979840 identical at 62feef9c and tip,
   sha256 6c851cd7…e3e0, and contains exactly 34 cases. Verdict: holds.
9. "registry row round25-custody-ruler keeps its entry, exit map and pinned
   digests unchanged" — pure-append diff; row (SKILL.md:807) pins oracle-rev
   62feef9c… and oracle-sha256 6c851cd7…, ruler sha 20fe3f3d…, all matching the
   recomputed values. Verdict: holds.
10. "attempt 1 calibration claim R25-C1 … explicit caller selected 34 case
    custody contract … not continued, no after value" — claims.json R25-C1,
    axis calibration, "explicit caller-selected Git instrument-reference
    custody", 34 declared cases; no `after` key anywhere in the file; SCORECARD
    line 3050 and round-25.md both say not continued. Verdict: holds.
11. quote "not pursued, not as met" (corpus/lessons/round-25.md, "Attempt 3"
    heading, lines 361 to 364; SCORECARD.md line 3050) — heading is line 357;
    the quoted phrase spans lines 362-363 inside the sentence at 361-363; span
    361-364 brackets it; identical at c3277726, fe3eb4ed, 003de8cc. SCORECARD
    line 3050 reads "…was not continued and has no after value." Verdict: holds.
12. "freeze ledger row FLAGGED, INSTRUMENT_ABSENT and INSTRUMENT_REVISED, the
    latter naming fafdd283 (claim-freezes.tsv line 13; receipt
    corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json)" — file has
    13 lines at c3277726; line 13 is the round-25 FLAGGED row naming both
    findings and fafdd283 (still line 13 at both later tips). Receipt present at
    c3277726; its round-25 entry: verdict FLAGGED, findings INSTRUMENT_ABSENT
    (path) and INSTRUMENT_REVISED with commits ["fafdd283…"], freeze a4ab912a,
    gate rev 1e064f9b203a012c4d3d33be87a9f3d0039d135f. Verdict: holds.
13. "outside measurement … exit 0, 34 of 34 exact, finding
    all_declared_pairs_exact, at 2026-10-22T03:28:48Z" — fleet receipt:
    exit 0, total 34, exact 34, finding all_declared_pairs_exact, at
    2026-10-22T03:28:48.373018+00:00, actual_M fafdd283…. Verdict: holds.
14. "fleet … .ufo/waves/hyaku/kaidoku25-prerequisite/parent-after-process.json,
    sha256 d15f5581…" — measured sha256
    d15f5581a6e968121cb9963a561a95421e24a871842dd5829acb994a7d64a958 at
    13:03:49Z and again in the transcript run. Verdict: holds.
15. "its own authority record states that admission is false" — sibling
    measurement-authority.json: `"owner": "Main only"`, `"admission": false`,
    same actual_M and source_sha256 54c43cdc…. Verdict: holds.
16. "'Not implemented at this phase' was true at the freeze and is false at the
    tip" — absent at a4ab912a, present from fafdd283 through 003de8cc.
    Verdict: holds.
17. "round 25 verifier spot check calls the claim abandoned" —
    round-25-verifier-spotcheck.md:185: "…while `fafdd283` landed it and the
    claim was abandoned." Verdict: holds.
18. "no committed lane record contains a retirement decision" —
    `git grep -i retir c3277726 -- corpus .ufo/waves/round-25 SCORECARD.md`
    finds only unrelated uses (axis-retired boilerplate, retired path
    assumption, census row, wall thread). No R25-C1 retirement anywhere.
    Verdict: holds (grep-scoped, see gaps).
19. "lane's committed records say not continued, reported as not pursued, not as
    met" — round-25.md:361-363, SCORECARD.md:3050, claims.json (no after key).
    Verdict: holds.

## Findings by severity

- Major: none.
- Minor: none.
- Informational: (a) clause 11's span "lines 361 to 364" contains the quoted
  sentence, but the "Attempt 3" heading itself sits at line 357, outside the
  span — the citation reads as heading-plus-span, which is accurate enough;
  (b) the exact phrase "not pursued, not as met" appears only in
  round-25.md; SCORECARD.md:3050 carries the equivalent "not continued and has
  no after value" — the note cites both as one wording, a fair summary;
  (c) the note's "no filed byte of that section" is true and stronger than
  claimed: the note commit is a pure EOF append (0 deletions in SKILL.md).

## Residual risk and verification gaps

- Clause 18 is a keyword grep over corpus/, .ufo/waves/round-25/ and
  SCORECARD.md at c3277726, not a semantic read of every committed file; the
  residual chance of an undiscovered retirement record is small but not zero.
- The fleet file was hashed in the working tree at 13:03:49Z and 13:07:46Z; it
  is outside the lane and could in principle change later. Its sha256 matched
  the note at both read times.
- "claims freeze commit" designation of a4ab912a is corroborated by the
  freeze-gate receipt and claim-freezes.tsv; the L1's own freeze ledger is the
  authority relied on, not an independent definition.

## Artifacts (scratch, sha256)

- /fast/scratch/hyaku/kaidoku-r26/seats/w2/CustodyNoteReview/evidence.sh —
  12e73a0ef65b2ca8e5caebb1811e5fba849d801cc82101636fc1f5d6ef9f20ed
- /fast/scratch/hyaku/kaidoku-r26/seats/w2/CustodyNoteReview/evidence.txt —
  477a583286c9862771c73e0f3ede71462905df3eb51deac412f97a257e901b6c
- /fast/scratch/hyaku/kaidoku-r26/seats/w2/CustodyNoteReview/tmp/ — empty

Tools installed: none. No lane file was modified; all git/jj use read-only.
