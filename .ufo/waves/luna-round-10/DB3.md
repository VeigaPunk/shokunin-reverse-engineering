## CLAIM
Complete lane A's timing-broken debt-ledger chain for the rounds 7-9 tranche: restore item-level coverage (D6's unfinished cross-check) and name the omissions.

## METHOD
Static reads at HEAD `c343939` (brief said `6e83a20`; current HEAD is `c343939`, +12/−0 SCORECARD conformance append, 0 deletions). Sources: reports r7-9; `SCORECARD.md:503-613`; `LOG.md:811-886`; D3-D6 (race documented at `D4.md:2`, `D6.md:5`), W7-W9, ZB4, A2/A4; `../MANIFEST.json`; `git show --numstat` on records commits `6e2ee8f`/`a280e07`/`6e83a20`; on-disk seat counts; CB7 C9 (`CB7.md:250`) plus grep of the six l7 entries. No probes, network, or writes.

## FINDINGS
- R7 append-only breach confirmed: `git show --numstat 6e2ee8f -- SCORECARD.md` → `32 1`; the single deletion is the living coverage row (72/72 `2abd30f5` → 78/78 `3395b6d`). R8/R9 records: `27 0`, `54 0` (append-only). Disclose; later appends do not cure (W7:10; R8.md:10).
- R7 report form: six headings (`kaidoku.md:6,19,35,42,58,63`) vs the four-section contract (SHONEN fourth; `templates/round-prompt.md:60-73`); R8/R9 share the six-heading shape.
- R7 CB7 C9 FAIL corroborated: C9 demands the per-entry literal `rea-agents@6.5.0` (`CB7.md:250`); it appears in l7-01..05 (10 hits) but not l7-06 (W7:9).
- R8 dispatch unproven: report claims 128 (`kaidoku.md:4`); disk now 100 seat files (52 A + 48 B), ZB4:13 91/128 with lane A never 64, FB1 52 lane-A items, no roster/backfill. R9 likewise: 121 files (66+55) vs claimed 128 (`kaidoku.md:3-4`), no roster (W9:17-26). Carry both.
- MANIFEST enum: prose rows `2846-2847` (r8) and `2860` (r9) — three of A2's six; r7's rows (`2833-2835`) are clean enums.
- D-chain omissions (answers D6 for this tranche): D3/D4/D5 carry pre-pair, SC1–SC6 convention, `:107-109`/`:77-80` staleness, r3-jq bleed, /tmp residuals; they miss the items above plus R9's VB3 straggler (`kaidoku.md:55-56`).

## THREATS
Record-based: no /tmp, REA, or sibling inspection. Counts are point-in-time lower bounds; W9's caveat stands (do not infer exactly seven undelivered seats). CB7 cited from W7's run plus my grep, not re-run. Completeness closes only rounds 7-9.

## VERDICT
FINDING: tranche ledger completed; R7 is not append-only, R7 has report-form and CB7-C9 defects, R8/R9 128-seat dispatch is unproven, and three tranche MANIFEST rows carry prose — carry all into closeout.
