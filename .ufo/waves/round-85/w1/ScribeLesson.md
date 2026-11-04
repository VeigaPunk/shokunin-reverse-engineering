# ScribeLesson — round 85 lesson and routed corrections (findings)

Seat report (draft; no commit, no lane-tree production bytes written).

**R2 (S303 scope count).** At `91eeb72f`, `grep -n -F 'rea-agents-6.5.0.tgz'` over
`corpus/SOURCES.md` returns **8** rows: S079, S080, S083, S090, S092, S119, S123 and S303 itself;
**7 are prior rows**. The URL sits in column 3 (source) of each. The row's anchor cell claims
"five scopes (S083/S090/S092/S119/S123)" — wrong; the count is seven. The text is in the **anchor**
cell (col 7), not `teaches` (col 8) as the routed defect states. The rejection and its flip are
unchanged. Count also 8 at `8ae9c8ee` and `b3084c8c`, so it was wrong when written.

**R3 (M84-5 pointer).** Sweep over the r84 lesson at `91eeb72f` is RED
(`MISSING l1/waves/round-84/w1/SentinelScope/esc-receipt.json`); the corrected
`.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json` and `…-abs.json` are GREEN (both `ok`, and
`git cat-file -e` at `91eeb72f`).

**R4 (M84-4 pointer).** `git log --oneline -S 'met = all(arms)' 91eeb72f -- tools` is **empty** — no
committed revision under `tools/` ever carried the per-run field; the first committed one
(`e0de2088`) already returns `{"depth","arms","observed"}` from `score_envelope()` with the
aggregate `"met": all(arms.values())` at line 241 (line 248 at `91eeb72f`). The removal predates
the first commit, so no diff exists. Resolvable pointer instead:
`.ufo/waves/round-84/l1/mistakes/m84-2-nested-met.json` (blob `3f25b629…`, sha256 `45e4bafa…`),
added by `b15d8083` (ancestor of `91eeb72f`); it records the mutant with `exit 0`, `failures []` —
the dead field is not re-demonstrable on current bytes. Its `"mistake": "M84-2"` cell disagrees
with the M84-4 row it supports.

**S304 gate facts** (from `w1/ScribeSource/report.md`): DOI HTTP 200; full text from the archived
ORBilu postprint HTTP 200 (ScienceDirect 403, ORBilu handle TLS failure); quote “When a test
distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant
is 'killed' or 'detected'” (24 words), Section 2 "Background", postprint p. 6; **admit, tier B,
scope `mutation-testing survey`**. The source is silent on name-matching — the lane's declared-case
binding is the lane's own tightening, not the source's wording.

**Proposed QUALITY criterion (one, for the L1 to decide; QUALITY.md not touched):** a count claimed
about a registry or directory is re-derived by command before it is written and every pointer a
lesson cites resolves as written — a scope count is stated as the ids the command returns, and each
path is checked with `test -e` at the revision it names.

**Open:** (1) correct S303's anchor cell in the registry row append-only, or only in the lesson?
(2) R4 has no diff to show; a diff-shaped artifact would need pre-commit bytes that are not in the
lane. (3) `m84-2-nested-met.json`'s `"mistake"` cell vs the M84-4 row. (4) S304 row + knowledge
entry must land together (E11). (5) `## Gate` spot-check line reads `pending: non-author closure`;
no admission for round 85 is claimed.

**Files:** `.ufo/waves/round-85/w1/ScribeLesson/candidate/corpus/lessons/round-85.md`,
`sweep-red-before.txt`, `sweep-green-after.txt`, `r2-r4-evidence.txt`, `report.md`.
**Installations:** none; no pacman transaction.
