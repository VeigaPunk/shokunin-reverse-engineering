# RerunC1Counter — R26-C1 counting command re-run (round 26, wave 2)

Seat `KaidokuR26.RerunC1Counter` (leaf, falsify wave). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, lane HEAD `fe3eb4edf410244eff46151a148c8f754be1ce80`
(`git rev-parse HEAD`, exit 0, 2026-10-22T13:02:09Z). Rules bound by
`.ufo/waves/round-26/claims.json` frozen at `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`.
Verdict is on committed bytes at the revs named below.

## Verdict

**Holds.** The frozen acceptance holds at every named revision: before-count
0/8 and `entry_ok` 0 at `a0639d8e` and `c27f445e` (exit 1), after-count 8/8
and `entry_ok` 1 at `ebe2cb4a` (exit 0), and it still holds at `c327772653`
after the routed fixes (exit 0). `--selftest` passes 16 of 16, exit 0. The
instrument blob, wherever it exists, equals the pinned sha256
`11c27422…18fa`. No counterexample found. (Observation.)

## Runs

Command, exactly as frozen in `claims.json` `counting_command`, run with cwd =
lane root; the instrument only reads Git objects, so the run is read-only:

`python3 -I -B tools/round-26/c1-id-identity.py --root <LANE> --rev <REV>`

| rev | utc | exit | rows_complete | entry_ok | first reasons |
|---|---|---|---|---|---|
| a0639d8e61e486e2a716ff94cddd89a73200a02c | 13:00:40Z | 1 | 0/8 | 0 | every row `table_missing`; entry `entry_missing` |
| c27f445e70cedbaf5300b2fd0a53e821d9b659a9 | 13:00:40Z | 1 | 0/8 | 0 | every row `table_missing`; entry `entry_missing` |
| ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb | 13:00:40Z | 0 | 8/8 | 1 | none; verdicts 7x `content-keyed`, `inspect-binary-layout` = `path-sensitive` |
| c327772653badd3b19b3954e1f8713973aa3f93e | 13:00:41Z | 0 | 8/8 | 1 | none; same verdict pattern as `ebe2cb4a` |

Every stderr empty (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
At the two green revs: `table.data_rows 8`, `header_ok true`, `extra_rows []`,
entry `cited_ids ["S079","S080"]`, `rows_opened_today ["S079","S080"]`,
`gate_ids ["S037","S079","S080"]`, `qualifying_ids ["S079","S080"]`, reasons
`[]`; path diagnostic `text_contains_path true` for all 24 envelopes.
(Observation; excerpts from the saved stdout files below.)

## Selftest

`python3 -I -B tools/round-26/c1-id-identity.py --selftest` at 2026-10-22T13:00:41Z,
exit 0, `cases 16`, `failures 0`. All named failure modes reproduce:
`missing_envelope`, `envelope_ok_false`, `wrong_subject_sha256`,
`id_cell_mismatch`, `wrong_verdict`, `unknown_verb`, `duplicate_verb_row`,
`table_subject_sha256_mismatch`, `entry_missing`,
`entry_source_without_table`, `sources_row_other_date`, `gate_omits_id`,
`usage_error_missing_rev` (exit 2), plus green, `gzip_envelopes`,
`no_id_verdict`. (Observation.)

## Instrument pin

`git cat-file blob <REV>:tools/round-26/c1-id-identity.py | sha256sum`
(read-only git; run 2026-10-22T13:00:42Z and 13:02:09Z):

- `a0639d8e`, `c27f445e`, `ebe2cb4a`, `46ebfd2f`: absent, git exit 128.
- `bd0c84bcb60724a16d33eb332e625ed9b767bea5`: `11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa`.
- `c327772653badd3b19b3954e1f8713973aa3f93e`: same pinned value.
- `fe3eb4edf410244eff46151a148c8f754be1ce80` (lane HEAD) and the working-tree copy: same pinned value.

`git log --format='%H %P'` shows the chain
`a0639d8e -> c27f445e -> 81f63f36 -> ebe2cb4a -> 46ebfd2f -> bd0c84bc -> c327772653 -> fe3eb4ed`,
so the instrument's first commit is `bd0c84bc`; absence before that is
expected, and the "each later commit" pin comparison applies to `bd0c84bc`,
`c327772653` and HEAD — all match, i.e. the instrument was never modified
after introduction. (Observation for the hashes; inference for "never
modified", resting on the parent chain plus the four blob comparisons.)

Note: the frozen `counting_command` executes the working-tree instrument and
takes only the data tree from `--rev`, so the `ebe2cb4a` run is the pinned
instrument bytes reading the `ebe2cb4a` tree (the instrument did not yet exist
in that tree). This is the literal frozen command; flagged so no one reads the
`ebe2cb4a` result as "that tree's own instrument". (Observation; reading.)

## Cross-seat reproduction

My outputs are byte-identical to wave 1's recorded artifacts
(`/fast/scratch/hyaku/kaidoku-r26/seats/CounterC1/out/`), independent run
environments: `a0639d8e` json `fcb49c34…363bd`, `c27f445e` json
`27906956…2cb74`, `ebe2cb4a` json `76141980…e552a`, `selftest.txt`
`208a14f3…e882b` — all four `equal=True` at 2026-10-22T13:02:09Z. (Observation.)

## Findings by severity

- Blocking: none.
- Major: none.
- Minor: none new. Wave 1's disclosed rule-level residuals on `entry_ok`
  (self-reported `opened` cells, `status` not gated, `used-by` not gated —
  D1/D6) remain latent by design of the frozen rule; this seat did not
  re-attack them, it re-ran, self-tested and pin-checked.

## Residual risk and verification gaps

- `c327772653` is new coverage (wave 1 stopped at `ebe2cb4a`); it holds, but
  later L1 commits (SCORECARD round-26 section, LOG, claim-freezes row) are
  not yet in any run I did — lane HEAD `fe3eb4ed` was not run as a rev since
  it was not in the assignment. (Unknown for HEAD; expected to hold by the
  same reasoning, inference only.)
- I did not run `--mutants` (wave-1 Evidence 3 covers it; outside assignment).

## Artifacts (under `/fast/scratch/hyaku/kaidoku-r26/seats/w2/KaidokuR26.RerunC1Counter/`)

| artifact | sha256 |
|---|---|
| out/real-a0639d8e61e486e2a716ff94cddd89a73200a02c.json | fcb49c343617f7ab88d722cca529347583d09d3949e81297c4a0bc5adb5363bd |
| out/real-a0639d8e61e486e2a716ff94cddd89a73200a02c.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| out/real-c27f445e70cedbaf5300b2fd0a53e821d9b659a9.json | 27906956ee7dcf9fd1586cc018e36bd0d40b5717ff2c1645476134720822cb74 |
| out/real-c27f445e70cedbaf5300b2fd0a53e821d9b659a9.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| out/real-ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb.json | 76141980e4553c7091a4c67d9b1390dc06bcc43cfe66b8e76d7d92c8bebe552a |
| out/real-ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| out/real-c327772653badd3b19b3954e1f8713973aa3f93e.json | 037de95a9ffb32fa398f1a3cdcf4c417e35cf9357ce8411730eb60061f6bae24 |
| out/real-c327772653badd3b19b3954e1f8713973aa3f93e.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |
| out/selftest.txt | 208a14f33b8c8872125c75a85735c8ec82a7aa24cec49796edeb22ef78ee882b |
| out/selftest.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty) |

## Tooling

No tools installed or upgraded. Lane untouched except this report file; no
lane mutation, no git or jj writes (all git use read-only: `rev-parse`,
`log`, `cat-file`).
