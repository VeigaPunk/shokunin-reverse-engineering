# R45W2PreflightReal — the sweep-contamination fix attacked on real history (scoped findings)

Full report, every receipt and the drivers: `.ufo/waves/round-45/w2/R45W2PreflightReal/report.md`
+ `receipts.json` (`exits.tsv` + per-run stdout/stderr). Lane tree read-only; no installs.
Frozen bytes verified: the interpreter I ran hashes `633ebc05…` and equals the frozen blob
`b4239827…` at `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`.

## Verdicts on the three assigned attacks

- **A1 (r44 sweep, `--pathspec` + `--require-pathspec`) — holds.** Exit 1, `touched` = exactly
  **8** (all `M`, all `c86ea508`), **zero** non-fixture records, `blob_changed` = the dir tree oid
  + the eight. My receipt is identical on every semantic field to the lane's own
  `.ufo/waves/round-45/l1/preflight-c86ea508.json`. The eight are 5 `after.json` + 2
  `manifest.json` + 1 knowledge `.md`; `c86ea508` is 432 paths (400 A / 32 M) with those 8 `M`.
- **A2 (r45 `f762b727..f59565b7`) — `clean`, exit 0, but the certificate is under-scoped.**
  Byte-identical stdout with and without `--require-pathspec`; also `clean` at the measured
  revision `1f4b27f8` and at HEAD (`0ee50aaf`). The freeze genuinely held (`git log
  f762b727..HEAD -- plans/round-45-claims.md tools/round-45/` empty; blobs `f93df4c3…` /
  tree `8cb6fa80…` unchanged). **But** the command names only `tools/round-45`, while the
  freeze has two paths; block 22 (R45-CL10) requires
  `--pathspec tools/round-45/ --pathspec plans/round-45-claims.md` with both `--freeze-path`
  values. Fixture pair: the one-pathspec shape exits **0 `clean`** after a commit that edits a
  frozen file it did not declare, while the two-pathspec form exits 1 on the same history.
  The certifying run is `b1` (two pathspecs, exit 0 `clean`). The lane's own receipts use the
  one-pathspec form too — record rule and record receipts disagree.
- **A3 (whole-tree scan, no `--pathspec`, no `--require-pathspec`) — falsified as a "catch".**
  Exit 1, `touched` = **542 records / 536 distinct** (the eight are inside it), `blob_changed`
  = `["tools/round-44/control-fixtures"]` only. Control: the same scan with a frozen path that
  is **byte-identical across the range** also exits 1 with `blob_changed []`. A red that is
  invariant to the frozen path is not evidence about it: the scan **drowns** the eight
  (8 of 542), it does not identify them. Row 5's exit-2 refusal happens only when the caller
  passes `--require-pathspec`; without it you get row-6 red at 542 records.

## Calibration cross-checks (all measured)

Selftest 11/0 with exactly the seven named red cases. Base interpreter (4008 B) has zero hits
for `check-dirty`/`require-pathspec`/`restored`/`selftest` — the "gains four arms" clause is
literal. Block 22's `--dirty-pathspec` false-clean reproduced exactly (narrowed → `clean` on a
dirty frozen file). The guard fails closed on a sibling-prefix pathspec and on `:(exclude)`
magic (both exit 2). Not in place: fleet wiring — `grep -r frozen-path-preflight
/home/vgpnk/Projects/shokunin/scripts` → 0 matches, so the M44-2 vector (non-author sweep) is
still un-prevented.

## Open routes for the L1

1. Cite `b1`, not the one-pathspec run, for the round's freeze; label the l1 receipts as
   `tools/round-45/`-only.
2. Row 2 of block 22 states the restore trigger unconditionally; the arm only fires inside the
   declared pathspec — say "within the declared pathspec".
3. `touched` counts records (542) not paths (536) and the receipt has no field reconciling it
   with `git show`'s 432; a reader cannot tell a sweep from a range without recomputing.
4. Placement in the fleet sweep/pre-push path remains an operator request (block 22 says so);
   it is the only thing that would have stopped `c86ea508`.
