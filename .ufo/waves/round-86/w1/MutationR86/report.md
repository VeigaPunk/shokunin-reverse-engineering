# MutationR86: round-86 counter mutation report

Revision: `0864a7bdbf185583773d1a3f3416de76e9cab137` (committed bytes of `tools/round-86/record-agreement.py` and `tools/round-86/gate-registry.py`; no production edit, no commit).

Method: 20 single-anchor mutants from `mutants.json`. Each `find` counted in committed bytes (all = 1). One mutant at a time in a scratch copy, run as `python3 -I -B <copy> --selftest`. `killed` only when the DECLARED case appears as `FAIL <case>:` and the pristine run is green. Survivors and inconclusive rows are reported separately.

Pristine: record-agreement rc=0 `SELFTEST cases=11 failures=0`; gate-registry rc=0 `SELFTEST cases=8 failures=0`.

Counts: killed=7, survived=13, inconclusive=0 (of 20).

## Rows

| id | target | declared case | case exists | anchors | status | observed FAIL lines / crash |
|---|---|---|---|---|---|---|
| RA-01 | tools/round-86/record-agreement.py | a1-wrong-count | True | 1 | survived | FAIL genuine-agreement: expected ok=True, atoms=[False, True, True] |
| RA-02 | tools/round-86/record-agreement.py | a1-no-superseding-row | True | 1 | survived | none |
| RA-03 | tools/round-86/record-agreement.py | a3-stale-receipt-round | True | 1 | survived | none |
| RA-04 | tools/round-86/record-agreement.py | a3-no-receipt-named | True | 1 | survived | crash: ValueError: max() iterable argument is empty |
| RA-05 | tools/round-86/record-agreement.py | a2-docstring-drift | True | 1 | survived | none |
| RA-06 | tools/round-86/record-agreement.py | a2-ambiguous-sentences | True | 1 | killed | FAIL a2-ambiguous-sentences: expected ok=False, got True |
| RA-07 | tools/round-86/record-agreement.py | a1-wrong-id-set | True | 1 | killed | FAIL a1-wrong-id-set: expected ok=False, got True |
| RA-08 | tools/round-86/record-agreement.py | a1-wrong-count | True | 1 | killed | FAIL a1-wrong-count: expected ok=False, got True |
| RA-09 | tools/round-86/record-agreement.py | a3-receipt-not-revision-stamped | True | 1 | survived | none |
| RA-10 | tools/round-86/record-agreement.py | a3-receipt-not-revision-stamped | True | 1 | killed | FAIL a3-receipt-not-revision-stamped: expected ok=False, got True |
| RA-11 | tools/round-86/record-agreement.py | a3-receipt-absent-at-rev | True | 1 | killed | FAIL a3-receipt-absent-at-rev: expected ok=False, got True; FAIL a3-receipt-not-revision-stamped: expected ok=False, got True |
| GR-12 | tools/round-86/gate-registry.py | duplicate-row | True | 1 | survived | none |
| GR-13 | tools/round-86/gate-registry.py | incomplete-verdict-map | True | 1 | killed | FAIL incomplete-verdict-map: expected ok=False, mismatches=[] |
| GR-14 | tools/round-86/gate-registry.py | selftest-nonzero-exit | False | 1 | survived | none |
| GR-15 | tools/round-86/gate-registry.py | incomplete-verdict-map | True | 1 | survived | none |
| GR-16 | tools/round-86/gate-registry.py | wrong-declared-exit | True | 1 | survived | none |
| GR-17 | tools/round-86/gate-registry.py | pin-absent-at-rev | True | 1 | survived | none |
| GR-18 | tools/round-86/gate-registry.py | two-pins-one-absent | False | 1 | survived | none |
| GR-19 | tools/round-86/gate-registry.py | owner-round-mismatch | True | 1 | killed | FAIL owner-round-mismatch: expected ok=False, mismatches=[] |
| GR-20 | tools/round-86/gate-registry.py | owner-trailing-text | False | 1 | survived | none |

## Killed (named case observed)

- RA-06: `a2-ambiguous-sentences`
- RA-07: `a1-wrong-id-set`
- RA-08: `a1-wrong-count`
- RA-10: `a3-receipt-not-revision-stamped`
- RA-11: `a3-receipt-absent-at-rev`
- GR-13: `incomplete-verdict-map`
- GR-19: `owner-round-mismatch`

## Survivors: missing cases (verified by probe unless marked)

- **RA-01** (missing), declared `a1-wrong-count`. Missing: `a1-count-binding-isolated`. Fixture `9 rows touched; corrected prior-row count 3 (S083/S090/S119)` expects ok=True. Pristine ok=True, mutant ok=False (verified). Current kill is incidental: genuine-agreement fails, the declared case does not.
- **RA-02** (missing), declared `a1-no-superseding-row`. Missing: `a1-no-superseding-row-truly`. The fixture named a1-no-superseding-row still contains a row whose teaches opens `supersedes S303` (S305), so the `if not sup` branch is never reached; the case exercises the no-count-clause path. Needed: a fixture with no such row, expect ok=False. Under the mutant that fixture would raise IndexError at `sup[-1]` [INFERENCE from source, not run].
- **RA-03** (missing), declared `a3-stale-receipt-round`. Missing: `a3-stale-receipt-blob-present`. The stale fixture's round-6 receipt is absent, so the blob read rejects it and the M>=R comparison is never the deciding check. Stale card + round-6 blob with 40-hex rev expects ok=False: pristine False, mutant True (verified).
- **RA-04** (missing), declared `a3-no-receipt-named`. Missing: `a3-no-receipt-named-isolated`. Mutant raises ValueError from max([]). The selftest only catches Unreadable, so the whole run dies with a traceback and no named FAIL line. Needs a per-case guard that reports `FAIL <case>: exception`.
- **RA-05** (missing), declared `a2-docstring-drift`. Missing: `a2-sentence-no-status-word`. The drift fixture's sentence contains the conflicting word `inconclusive`, so `not others` alone rejects it and the stem-absent path is never exercised. Sentence with no status word expects ok=False: pristine False, mutant True (verified).
- **RA-09** (missing), declared `a3-receipt-not-revision-stamped`. Missing: `a3-receipt-rev-39-hex`. Fixture rev is 6 chars (`abc123`), which 39-40 also rejects. A receipt with a 39-hex rev expects ok=False: pristine False, mutant True (verified).
- **GR-12** (missing), declared `duplicate-row`. Missing: `duplicate-row-G1-attribution`. The duplicate-row case checks only the aggregate ok. With find_row None, G2-G5 also fail, so the G1 rule is never individually observable. Per-atom assertion G1 ok=False on the duplicate fixture: pristine False, mutant True (verified).
- **GR-14** (equivalent), declared `selftest-nonzero-exit`. Missing: `-`. Equivalent on the current row: G3 runs the identical argv (`-I -B ... --selftest`, declared exit 0), so it catches the same nonzero exit and the aggregate is unchanged (verified). Not a selftest gap unless a row's self-test cell differs from --selftest.
- **GR-15** (missing), declared `incomplete-verdict-map`. Missing: `verdict-map-no-exit-2`. NO_MAP_ROW has no `0=` at all, so the partial-map path is unexercised. Verdict `0=clean; 1=flagged` expects ok=False: pristine False, mutant True (verified).
- **GR-16** (missing), declared `wrong-declared-exit`. Missing: `child-exit-mismatch-probe`. wrong-declared-exit declares 3 against got=0, so the mutant also fails it. Needed: a row declaring exit 0 on a `--probe` command that exits 2 (fixture tool needs a --probe branch): pristine False, mutant True (verified).
- **GR-17** (missing), declared `pin-absent-at-rev`. Missing: `pin-blob-absent-round-84`. BAD_PIN_ROW rewrites the pin to `round-85/absent.json`, which the claims.json regex does not match, so pins=[] and G4 fails on the empty-pin path. The absent-blob branch is never reached. Pin `round-84/claims.json` (absent): pristine False, mutant True (verified).
- **GR-18** (missing), declared `two-pins-one-absent`. Missing: `two-pins-one-absent`. Two pins, one absent: pristine False, mutant (>=1) True (verified).
- **GR-20** (missing), declared `owner-trailing-text`. Missing: `owner-trailing-text`. Owner cell `kaidoku-r85 (old)` expects ok=False: pristine False, mutant True (verified).

## Calibration notes

- Both selftests print `cases=len(cases)+1`: record-agreement prints 11 for 10 named cases; gate-registry prints 8 for 7. The summary over-counts by one.
- The gate-registry selftest asserts only the aggregate `ok`, never per-atom verdicts, so atoms G1-G5 are not individually checked.
- record-agreement's selftest loop catches only `Unreadable`; any other exception aborts the whole run with no named FAIL.

## Proposal for the L1 (not applied)

Add the verified cases above (each expect/kill pairing was probed in scratch); add per-atom assertions for gate-registry; wrap each selftest case in try/except reporting `FAIL <case>: exception`; rename `a1-no-superseding-row` to match its fixture or replace the fixture. GR-14 needs no case: it is equivalent on the current row.

Milestone: R86-C1 (record agreement, 3 atoms) and R86-C2 (gate registration, 5 atoms) selftests examined; frontier S255 (committed bytes read via `git show`) and S305 (supersession fixture) reviewed; the round-86 lesson that a case name must match its fixture is confirmed by RA-02.

