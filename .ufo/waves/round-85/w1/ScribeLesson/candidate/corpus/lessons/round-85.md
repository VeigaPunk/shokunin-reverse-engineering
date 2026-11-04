# Round 85 — a claim's counter is named in its predicate; a counted scope is counted, not asserted

Base `b3084c8c2036db966ce4750b4039bddaa84cc760`; declaration `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`
(`plans/round-85-claims.md`, the frozen 21-row mutant table `.ufo/waves/round-85/mutants.json`, the
pre-declaration BASE receipts commit `c7e2e8e166cf8ae3db292814f80ab5d35beec455`). One v1 wave
`r85-w1`. This lesson records what this round mined and the corrections the round-84 non-author
spot-check routed in (R2, R3, R4). The round-84 lesson and its spot-check are **not** rewritten;
the corrections below are appended text only.

Round 85 declares two claims: R85-C1 (calibration — `tools/round-85/predicate-bind.py` refuses a
claim container whose counter path appears only outside an affirmative, non-negated predicate) and
R85-C2 (depth — the frozen 21-row table closes the r84 probe's surviving mutants at declared
cases). Their verification is the L1's; this lesson does not assert either outcome.

## Gate

| item | decision | source opened 2026-11-04 | judgment |
|---|---|---|---|
| S304 Papadakis et al., "Mutation Testing Advances: An Analysis and Survey", Advances in Computers vol. 112 (2019), pp. 275-378 | admit (mined, tier **B**, scope `mutation-testing survey`) | `https://doi.org/10.1016/bs.adcom.2018.03.015` → HTTP 200, resolving to `https://linkinghub.elsevier.com/retrieve/pii/S0065245818300305`; full text read from the ORBilu author postprint archived 2019-04-29, `https://web.archive.org/web/20190429011957/http://orbilu.uni.lu/bitstream/10993/31612/1/survey.pdf` → HTTP 200 (PDF 1 129 278 B, 153 pages, sha256 `63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023`; snapshot `.ufo/waves/round-85/w1/ScribeSource/source-snapshot.txt`). ScienceDirect chapter page returned HTTP 403 and the ORBilu handle failed TLS verification; the archived postprint was the text actually read. Anchor: Section 2 "Background", postprint PDF p. 6 — “When a test distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant is 'killed' or 'detected'” (24 words) | grounds the round's sourced claim that a mutant counts as killed only by an observed difference in the test run. **Stated gap:** the survey defines the kill behaviourally and is silent on a test's *name*; the lane's declared-case-name binding is the lane's own tightening of that definition and must not be attributed to the source. Row facts and the quote's location are supplied by the ScribeSource seat (`w1/ScribeSource/report.md`); the row and its knowledge entry must land together or the registry's `used-by` check flags E11 |

Rejected this round: none. Carried forward from round 84 and unchanged here — **S303** (npm tarball
`rea-agents-6.5.0.tgz` as authority for the extraction-gap taxonomy) stays rejected: a tarball is not
an anchored document, S302 is the anchored authority; **flip:** a published REA documentation URL that
anchors the gap taxonomy. Its reason text is corrected below (C-R2) without an in-place rewrite.

Spot-check result: **pending: non-author closure**. The round-84 non-author spot-check
(`corpus/lessons/round-84-verifier-spotcheck.md`) is the last closure on record; this round's own
outside spot-check is not yet written, and no agreement or admission is claimed for round 85 here.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M85-1 | a counted scope asserted as a smaller number, and a wave pointer cited without the directory prefix that holds it | `w1/ScribeLesson/r2-r4-evidence.txt` (E1–E5) and `w1/ScribeLesson/sweep-red-before.txt` / `sweep-green-after.txt`: at `91eeb72f`, `git show 91eeb72f:corpus/SOURCES.md \| grep -n -F 'rea-agents-6.5.0.tgz'` returns **8** matching rows — S079, S080, S083, S090, S092, S119, S123 and S303 itself — of which **7 are prior rows**; and the sweep over the round-84 lesson's own `l1/waves/round-84/w1/SentinelScope/esc-receipt.json` is RED (`MISSING`) while `.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json` is GREEN (`ok`) | none — no tool, gate or reviewer caught either; both were found by the non-author spot-check reading the lesson and the registry (routed R2, R3) | the count is re-derived by command and recorded in Correction C-R2 (7 prior rows, not the "five scopes (S083/S090/S092/S119/S123)" the row states); the pointer is corrected to the `.ufo/`-prefixed path in Correction C-R3 with the red-before/green-after sweep as its proof. The lesson's own text is left as it was — the correction is appended here |

## Corrections (append-only)

These are appended by round 85. The round-84 lesson (`corpus/lessons/round-84.md`) and the round-84
spot-check are not rewritten; where this round's wording differs from theirs, this section governs.

### Correction, round 85 — C-R2 (S303's reason says "five scopes"; the count is seven prior rows)

Routed from `corpus/lessons/round-84-verifier-spotcheck.md` §4 (Discernment spot-check, "Factual
error in the reason") and §9 (routed defect R2). The S303 row's **anchor** cell (column 7 of the
registry table; the row's `teaches` cell carries the rejection and the flip) states: "the registry
already holds this URL in five scopes (S083/S090/S092/S119/S123)". The routed defect describes it
as the row's `teaches` reason; the count claim itself sits in the anchor cell, and it is corrected
here where it actually stands.

Re-derived by count, at the declaration revision:

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 91eeb72f:corpus/SOURCES.md \
    | grep -n -F 'rea-agents-6.5.0.tgz'
85:| S079 …
86:| S080 …
89:| S083 …
96:| S090 …
98:| S092 …
125:| S119 …
129:| S123 …
219:| S303 …
$ … | grep -c -F 'rea-agents-6.5.0.tgz'
8
```

**The count is 8 rows in the registry; 7 of them precede S303.** The seven prior rows are
**S079, S080, S083, S090, S092, S119, S123** — the URL `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`
stands in column 3 (source) of every one of them. The eighth match is S303's own row, which names
the URL as the rejected candidate's source. The "five scopes (S083/S090/S092/S119/S123)" is
therefore wrong twice over: it undercounts the prior rows (5 named, 7 present) and it names only the
rows whose scope mentions the tarball, not every row that holds the URL.

The rejection decision itself is unaffected — a tarball is not an anchored document, S302 is the
anchored authority, and the flip condition is unchanged. Only the count and the row list are
corrected. The same count holds at the round-84 commits (`8ae9c8ee` = 8, `b3084c8c` = 8), so the
error was present when the row was written and was not a later regression.

Evidence: `w1/ScribeLesson/r2-r4-evidence.txt` E1–E5.

### Correction, round 85 — C-R3 (M84-5's pointer lost the `.ufo/` prefix)

Routed from `corpus/lessons/round-84-verifier-spotcheck.md` §5 and §9 (routed defect R3). The
round-84 lesson's M84-5 row cites `l1/waves/round-84/w1/SentinelScope/esc-receipt.json` (and the
`-abs` variant in the same cell). That path does not exist; the receipts live under the wave
directory's real prefix.

Corrected pointer: **`.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json`** and
**`.ufo/waves/round-84/w1/SentinelScope/esc-receipt-abs.json`**.

Resolution proof — red before the correction, green after (read-only `test -e` in the lane tree;
command outputs in `w1/ScribeLesson/sweep-red-before.txt` and `w1/ScribeLesson/sweep-green-after.txt`):

```
# RED — over the round-84 lesson's own wording, at 91eeb72f:
$ grep -o 'l1/waves/round-84[^ )`]*' round-84.md | sort -u | while read p; do test -e "$p" && echo "ok $p" || echo "MISSING $p"; done
MISSING l1/waves/round-84/w1/SentinelScope/esc-receipt.json

# GREEN — the corrected spelling:
$ test -e .ufo/waves/round-84/w1/SentinelScope/esc-receipt.json && echo ok …
ok .ufo/waves/round-84/w1/SentinelScope/esc-receipt.json
ok .ufo/waves/round-84/w1/SentinelScope/esc-receipt-abs.json
$ git cat-file -e 91eeb72f:.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json && echo 'blob ok'
blob ok
```

The `-abs` variant is cited in the round-84 lesson by bare file name, so the `l1/…` sweep finds only
the one prefixed path; it inherits the same missing prefix and resolves under the same `.ufo/` prefix.

### Correction, round 85 — C-R4 (M84-4 has no resolvable pointer; the removal predates the first commit)

Routed from `corpus/lessons/round-84-verifier-spotcheck.md` §5 and §9 (routed defect R4). The
round-84 lesson's M84-4 row gives its evidence as prose only — "the first `score_envelope()` returned
`met = all(arms)`" — with no file or commit to resolve.

The pickaxe named in the routed defect returns nothing for the tool path:

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --oneline -S 'met = all(arms)' 91eeb72f -- tools
(no output)
```

**There is no commit under `tools/` that removed the field, because no committed revision of the
tool ever carried it.** The literal string occurs only in prose: at `91eeb72f` it is in
`corpus/lessons/round-84.md` and `corpus/lessons/round-84-verifier-spotcheck.md` and nowhere else.
The same pickaxe without the path filter returns only commits that write such prose —
`8ae9c8ee` (the round-84 lesson landing) and `b3084c8c` (the round-84 spot-check), plus this
round's pre-dispatch artifacts (`.ufo/waves/round-85/r85-w1-dispatch.json`,
`.ufo/waves/round-85/r85-w1-spec.json`, `.ufo/waves/round-85/w1-briefs/ScribeLesson.md`), which
quote the routed defect. The first
committed revision of the tool — `e0de2088a7bddc16305357f90ac7e889fa0a0d11` ("round-84: freeze
claim-metadata gate, mutation-closure counter and nested-chain counter with base controls"), which
*creates* `tools/round-84/nested-sqfs.py` — already has `score_envelope()` returning
`{"depth": depth, "arms": arms, "observed": observed}` with no per-run `met`, and the aggregate
decided in `score()` at line 241 (`"met": all(arms.values()) and control["fires"]}`); at the
declaration revision `91eeb72f` the same aggregate sits at line 248. The removal therefore happened
in the working tree **before** the tool's first commit and left no commit to point at (inference
from committed bytes only: no committed revision carries the per-run field, and the first
committed one already lacks it).

The resolvable pointer that does exist is the committed mutant receipt
**`.ufo/waves/round-84/l1/mistakes/m84-2-nested-met.json`** (blob `3f25b6290496cbf802510b5b09d33b866b6265b3`,
sha256 `45e4bafa4927e11f3c13d18f3b7403f7058a9def0ac165429efd4a302160255f`), added by
`b15d8083baf4f6de420fb452bcec13a87f4bb22a` (an ancestor of `91eeb72f`; also present at
`4d110e00c6f3231aed19f823ed9b51e0328cd408`, which is not an ancestor). Its full content:

```
{
 "mistake": "M84-2",
 "mutant": "envelope met = all(mutually exclusive coverage arms)",
 "exit": 0,
 "failures": []
}
```

Read literally: the mutant that reinstates the dead per-run field is **not** killed on current
bytes (`exit 0`, no failures). That is the same finding the round-84 lesson already records for
M84-4 — the removal is a design correction, not a demonstrated fix, and a revert of the code alone
no longer fails the selftest. Two defects are visible in that receipt and are stated here rather
than silently smoothed: (a) its `mistake` cell reads **M84-2**, while the prose it supports is the
**M84-4** row, so the file name and its content cell disagree with the lesson's numbering; (b)
because the mutant survives, this receipt demonstrates the *absence* of the defect on current bytes
and cannot demonstrate the removal. The lane's own M84-4 wording — "not re-demonstrable on current
bytes" — remains accurate; what this correction adds is the resolvable pointer and the fact that
the removal is pre-commit, not a diff that a reader can inspect.

Evidence: `w1/ScribeLesson/r2-r4-evidence.txt` E6–E14.
