# Round 57 — the r56-closure carry-in round: eight routed defects close, and the extended M56-4 rule becomes an instrument

Lane kaidoku, round 57, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked), L1-inline on the Windows host (2026-11-01). Round base
`63413677ec0531e38722b8dbfb0b89a0bc113d04` (the r56 verifier spot-check commit);
declaration `5d5bcb92ac0476d0d2480e248eaaec3c5f030f07`; carry-in landing
`e304cb0dbfc4140de984e938be0cf794964b2759`; operative freeze
`bc261681ef89833693c039c80762aa31189bfbed` (first commit adding
`.ufo/waves/round-57/claims.json`). No wave (no dispatch surface on this host;
the kaidoku round-53 L0 question stays open and unanswered). Both claims are
offline over committed bytes; the executed instruments are the new frozen
round-57 gate, the unchanged corrections-pin, and the R29 gate.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S257 | https://git-scm.com/docs/git-ls-tree — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-57/l1/s257/` (git-ls-tree.html `2c298383476164238c6e25ba804412a335c405ab9540650bb603778e2f4f8b64`) | "--name-only List only filenames (instead of the "long" output), one per line." (OPTIONS, 11 words) | admit, tier A docs (the tool's own manual, consistent with S255/S256's tiering of git-scm.com docs), mined: grounds the listing semantics of `tools/round-57/record-receipt-audit.py` — every backtick-quoted `.ufo/waves/round-N/` path a record section names is resolved against one `git ls-tree -r --name-only REV` listing, exact match, one revision. The R56 reject-1 boundary is applied consistently: the r56 gate anchored cat-file because its verdict was existence-at-revision; this gate's verdict IS the ls-tree listing, so the anchor moves to the ls-tree manual. Used by `plans/round-57-claims.md`, `tools/round-57/record-receipt-audit.py`, this lesson. |
| R57 reject 1 | extracting the record's named paths from the WORKTREE copy of `SCORECARD.md` (an on-disk read would let a post-hoc edit satisfy the audit) | reject — the instrument reads `git show REV:RECORD`, committed bytes only; the audit's subject is the record as filed, never the desk copy | reject row |
| R57 reject 2 | running the R29 gate at the record rev before the round-57 ledger row exists and calling the run clean | reject — the gate honestly exits 1 pre-row (disclosures 31/32 exact + missing [round-57]); the receipt says so and lands with the close, one commit after the row (the r55/r56 ordering pattern, disclosed in the receipt header) | reject row |
| R57 reject 3 | repairing D6 by editing the r56 LOG freeze entry in place to insert the discarded sha | reject — LOG.md is append-only (0 deletions across the round, re-derived); the disclosure is completed by an appended correction entry naming the clause it completes, the S254 append-only-ledger form | reject row |
| census receipts | the host-adapted census command at round start and at the filing tip; start receipt `.ufo/waves/round-57/l1/census-start.txt` (exit 0, 19 standing W04, 163 rows) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing controls | `.ufo/waves/round-57/l1/scores/c1-before.txt` (all eight routed defects open at the base) and `scores/c2-before.txt` (instrument absent, 0 registry rows, 0 capability rows) | both arms red at the base, committed at the freeze | measured pre-data; a do-nothing control cannot land an erratum set, a missing receipt, printed disclosure shas, a receipted gate run, or rows |

Assimilation: none — `considerthese/` does not exist in this lane (measured at
round start); the shokuknow register is unreachable from this host; the report carries
`Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M57-1 | receipt-annotation drift (a receipt's conclusion written from the intended state, not its own observed output) | the r56 `scores/c1-after.txt` V-1/V-5 blocks each print 0 and then annotate "grep exit=1 (>=1 -> V-1/V-5 closed)" — the annotations assert the opposite of their own observed output because the probe strings do not occur in the committed correction wording; the r56 report then quoted "1 / 1 / 0 / 1" where its own receipt prints 0 / 1 / 0 / 0; no r56 check compared a receipt's annotations against its own printed outputs | the r56 non-author closure (routed D1/D2, §7); corrected this round | the erratum of record is the `## Corrections (round 57)` block in `corpus/lessons/round-56.md` (nothing above it edited); the after-arm is restated on markers that DO occur in the committed bytes (`planted empty directory trees mirroring the pathspec`, `canonical-parameter clarification`, `supersedes M55-2`) and re-run with observed outputs in `.ufo/waves/round-57/l1/scores/c1-after.txt`. The general rule is M56-1's transcription rule applied to receipt annotations: an annotation line is checked by re-deriving its predicate from the printed output before the receipt lands |
| M57-2 | gate coverage defined over one naming surface (the audit checked what the container claimed, not everything the record named) | the r56 post-close correction's pre-filing audit diffed `git ls-tree` against the two receipts the M56-4 lesson row named — the record section's 13-name receipts list was a second, unguarded surface, so a third named receipt (`records/receipt-audit-green-r56.txt`) shipped uncommitted and M56-4's "fully resolvable" sentence was falsified at the r56 tip | the r56 non-author closure (routed D4, §7); mechanized this round | `tools/round-57/record-receipt-audit.py`: EVERY backtick-quoted `.ufo/waves/round-N/` path a record section names must resolve at the named revision (section-sliced committed bytes, exact match against one `git ls-tree -r --name-only REV` listing, zero named unevaluable never vacuously clean); its red demo reproduces the D4 defect at the base (named 14, missing 1) and its green demo shows the closure at the carry-in landing (named 14, missing 0). The D4 receipt lands at `e304cb0d…`; the record resolves 13/13 from that commit on |
| M57-3 | batched LOG appends (entries written before the commits they describe) | the declaration and carry-in-landing LOG entries were appended in one batch before either commit existed, so the carry-in entry landed inside the declaration commit `5d5bcb92…` and the carry-in commit `e304cb0d…` carries the files the entry names but no LOG line of its own | this round's L1, by the post-commit diff-tree audit (each commit's contents re-derived against the LOG entry it was meant to carry) | disclosed in the round-57 freeze LOG entry (not waived, LOG deletions 0); the facts are unchanged (every named file resolves at `e304cb0d…` and at the tip). Rule: a LOG entry is appended immediately before ITS OWN commit, never batched ahead |

## Claim disposition (filled at the record commit)

C1 (calibration, the eight r56-closure routed defects D1–D8): before all-eight-open
at the base (`scores/c1-before.txt`), after all-eight-closed with committed
artifacts (the erratum + landed receipt + printed sha + receipted gate run +
corrected item list; per-defect landing commits in the SCORECARD round-57
section; after receipt `scores/c1-after.txt`, pinned at the record commit,
lands with the close — the ordering note applies, the rev field pins the commit
it measured). C2 (depth, capability acquisition — the named-path completeness
gate): before absent (`scores/c2-before.txt`), after selftest 9/0, red demo
exit 1 `NAMED_PATH_ABSENT` on the D4 defect itself at the base, green demo
exit 0 at the carry-in landing, registry row in SKILL, capability row in
SCORECARD (`records/record-audit-green-r56.txt`). Verdicts in SCORECARD's
round-57 section and LOG.

## Freeze

First commit adding the container `.ufo/waves/round-57/claims.json`:
`bc261681ef89833693c039c80762aa31189bfbed`. No amendments to the operative
freeze; the LOG ordering slip (M57-3) is disclosed, not an amendment. The
frozen instruments and pins: `tools/round-57/record-receipt-audit.py`
`3a5fff9a…d8151`, `tools/round-55/corrections-pin.py` `22f77c34…9ece81`
(unchanged since the r56 disclosed revision), `tools/round-29/freeze-gate.py`
`25b54339…93eb2` (unchanged since round 29) — bytes unchanged from the claims
commit `5d5bcb92…`.
