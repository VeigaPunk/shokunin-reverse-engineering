# Round 54 — the routed-record repair round: ten routed defects close with receipts

Lane kaidoku, round 54, fresh-start round, L1-inline on the Windows host (2026-11-01).
Round base `45c6878634c16caa8e3e63472b30e439581b3a0d` (the r53 spot-check commit);
declaration `9dc73005…`; freeze `85843f2e…`. No wave (no dispatch surface on this host;
the kaidoku round-53 L0 question stays open and unanswered). Both claims are offline
over committed bytes; the only executed instrument is the frozen
`tools/round-53/r53-record.py` (bytes unchanged since round 53).

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S254 | https://www.rfc-editor.org/rfc/rfc6962.txt — fetched read-only with curl 2026-11-01 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-54/l1/s254/` (rfc6962.txt `08fdf31c10b9f20872a65c027a9fe8cee27280f930120784241a57de744752af`); a first fetch of the datatracker `.txt` URL returned the HTML rendering and was replaced by the rfc-editor origin (both recorded in the session scratch, the snapshot is the rfc-editor bytes) | "violating its append-only property by presenting two different, conflicting views of the Merkle Tree" (§7.3, 21 words) | admit, tier A spec (the IETF's own published text — primary for the append-only log model), mined: the form of the freeze-ledger correction convention (QUALITY row 100) — a ledger is corrected by appended entries that name what they correct, never by editing filed rows into a conflicting view. It grounds a record-keeping form, not any REA surface; no CT log was operated. Used by `corpus/QUALITY.md` row 100, `corpus/claim-freezes-corrections.tsv`, `plans/round-54-claims.md`. |
| R54 reject 1 | grounding the correction convention in git's own object/ref documentation instead of S254 | reject — the lane's plumbing-only rule already rests on git practice; S254 names the append-only property itself as the guarantee being borrowed, which is the thing the convention needs | reject row (LEARNING.md Gate format) |
| R54 reject 2 | appending the round-53 correction row directly into `corpus/claim-freezes-v2.tsv` | reject — the gate's `--disclosures` agreement counts any ledger row without a matching audited freeze as stray and exits 1 (r53 receipt: 28/28 exact, no strays); a correction row there would break every later gate run, so the convention puts corrections in the companion ledger | reject row |
| R54 reject 3 | regenerating the D6 broad sweep and asserting the original 390 hits | reject — not reproducible: the working copies changed after round 53 (regenerated count 272, fleet root 0); the listing commits the regenerated output with the drift disclosed inside, never a claimed-equal count | reject row |
| census receipts | `scripts/sources-census.sh validate --root <fleet> <explicit lane dir>` at round start and at the filing tip; start receipt `.ufo/waves/round-54/l1/census-start.txt` (exit 0, 19 standing W04) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here); W04 stays debt |
| do-nothing controls | `.ufo/waves/round-54/l1/scores/c1-before.txt` (nine routed-record closures absent at the base) and `scores/c2-before.txt` (the drifted block-27 clause present once; the v6 clean row's census cell `*`) | both arms red at the base, committed at the freeze | measured pre-data; a do-nothing control cannot land receipts, conventions or corrections |

Assimilation: none — `considerthese/` does not exist in this lane (measured at round
start); the shokuknow register is unreachable from this host; the report carries
`Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M54-1 | reconstruction-order (registry rows must land inside the Registry table) | first E11-reproduction run emitted `E12 S253 row outside Registry section` and never reached the target `E11 S253 missing used-by corpus/lessons/round-53.md`: the reproduced SOURCES.md appended the S253 row at end-of-file, after the prose section (`scratch/kaidoku-r54` transcript, first run) | this round's L1; the census's own E12 check (it fired, the reproducer had not consulted it) | the reproduction inserts the row after the last `| S` row of the Registry table; the committed `records/census-e11-repro.txt` is the corrected run (exit 1, exact E11 line). Rule: a reproduced registry carries appended rows inside the table, or the census grades the reconstruction, not the target failure |
| M54-2 | fixture-root confusion (stale constants across contexts) | the first three control-battery arms exited 2 with `merge-base failed: Not a valid commit name 6ead6f1b…`/`6697518f…`: the scratch driver passed the LANE's freeze/base hashes to runs against the scratch FIXTURE repo, whose freeze/base are its own commits (`records/c2-control-battery.txt` records only the corrected final run; the failed first run is disclosed here) | this round's L1; QUALITY 83 (dry-run end to end before trusting an instrument run) | the driver passes the fixture-scoped hashes; all three arms then score red on exactly their atom. Rule: hashes are scoped to the repo they name; a reused constant is checked against the repo it is aimed at |
| M54-3 | stale-docstring-on-a-frozen-instrument (erratum, no byte touched) | `tools/round-53/r53-record.py`'s docstring says `--selftest` "runs the battery over this directory's committed mutation fixtures under `.ufo/waves/round-53/l1/record-mutations/` when present; offline hosts … exit 2", but the implementation builds the miniature fixture inline and never reads that directory (no such tree is committed); found while wiring `records/c2-selftest-receipt.json` | this round's L1 | the frozen bytes stay untouched (the r53 container pins them); the receipt records what the code does (32 inline cases, pass 32, fail 0), not what the docstring says; this row is the erratum of record |
| M54-5 | receipt-authoring (an edit dropped a line the receipt was supposed to carry) | the E11 receipt `.ufo/waves/round-54/l1/records/census-e11-repro.txt` carries the reproduced exit=1 and the exact `E11 S253 missing used-by corpus/lessons/round-53.md` line but no `verdict:` line: the scratch driver's verdict-append was lost while fixing the ok-check, and the receipt landed without it (first after-arm run: checker FAIL, then checker corrected to test what the receipt actually contains) | this round's L1, by the after-arm content check | the landed receipt stays as landed (no in-place receipt rewrite); the verdict (exit 1 + exact E11 line) is derived by `scores/c1-after.txt` D10 checks; the checker, not the receipt, asserts the verdict — disclosed rather than re-landed |
| M54-4 | helper-mechanics (directory arguments are not expanded) | the freeze commit `5f768669…` carried only LOG.md: `treecommit.py` treats a directory argument as a path that is not a file on disk and removes it from the tree (a no-op here); the wave files landed in the follow-up commit `85843f2e…` | this round's L1, at verification (`git ls-tree` count 0) | pass explicit file paths to the helper (the freeze receipt list in SCORECARD names every file); the ordering defect is disclosed here and in LOG — all freeze receipts still precede the first repair-data commit |

## Claim disposition (filled at the record commits)

C1 (calibration, the nine routed-record closures D1,D2,D4,D5,D6,D7,D8,D9,D10): before
0/9 at the base (`scores/c1-before.txt`), after 9/9 content-checked at the landing
(`scores/c1-after.txt`, committed with the record). C2 (depth, block-27 prose/table
agreement): before the drifted clause present once (`scores/c2-before.txt`), after the
clause count 0 with the table bytes between the v6 markers byte-identical and the
frozen `tools/round-53/sqfs-triage-v6.py` re-run green at the landing
(`scores/c1-v6-at-landing.json`, `scores/c2-after.txt`). Verdicts in SCORECARD's
round-54 section and LOG.

## Freeze

First commit adding the container `.ufo/waves/round-54/claims.json` (and `l1/FREEZE`):
`85843f2ec7feef3f44c285df455233cb865202f9`. The freeze commit `5f768669…` carried only
the LOG entry (M54-4); the wave files landed with the container at `85843f2e…` and
still precede every repair-data commit. No amendments; the operative freeze for every
after-command is `85843f2e…`; the frozen oracle's bytes and pin are unchanged from the
r53 container (`c9fd8c68…`).

## Corrections (round 55)

Appended by round 55 (nothing above this block is edited). Corrections to this
lesson's claims, per the protocol's correction rule:

- **Correction 1 — "the only executed instrument".** The header sentence above
  ("the only executed instrument is the frozen `tools/round-53/r53-record.py`") is
  superseded: TWO frozen instruments were executed in round 54 —
  `tools/round-53/r53-record.py` (the selftest, control-battery and tip-reproduction
  receipts) AND `tools/round-53/sqfs-triage-v6.py` (the landing re-score, receipt
  `.ufo/waves/round-54/l1/scores/c1-v6-at-landing.json`, pin `5902a008…`, bytes
  verified unchanged by the round-54 closure). Both were frozen, which is what the
  sentence was trying to assert. Routed defect 2 of
  `corpus/lessons/round-54-verifier-spotcheck.md` §5; the same correction is carried
  by the round-55 LOG declaration entry and the round-55 report.
- **Correction 2 — the v6-table digest.** The receipt line `table sha256
  base=b340ed2b48facca7 landing=b340ed2b48facca7` (scores/c2-after.txt) names no
  extraction command and the value was not reproducible (routed defect 3, spot-check
  §5). Round 55 supersedes the value with the extraction of record —
  `python -X utf8 -I -B tools/round-55/v6-block-digest.py --root . --rev <REV>` —
  whose full digest `946e535947ba6d17da9f4b1ca7993af285e66103547a5c2107b253e5dd204bcc`
  is identical at the round-53 base, the round-54 landing, the round-54 close tip
  and the round-55 base (receipt `.ufo/waves/round-55/l1/records/v6-digest-repro.txt`,
  which also transcribes the ~100-boundary sweep that failed to reproduce
  `b340ed2b48facca7`). The byte-identity claim this receipt supported is unchanged
  and now re-derivable.
- **Correction 3 — the tip gate run.** The no-harm section's "freeze gate at the
  tip: exit 0, disclosures 29/29 exact" (spot-check §5 item 1: the assertion shipped
  no artifact) is now receipted:
  `.ufo/waves/round-54/l1/scores/freeze-gate-tip-90f3a9b9.json` — the gate executed
  by round 55 at rev `90f3a9b9d3970ae87173787521a821132c10c66c`, exit 0, disclosures
  exact 29 of 29, stray [], round-54 row CLEAN.
