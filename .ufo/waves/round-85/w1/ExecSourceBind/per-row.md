# ExecSourceBind — R85-C2 per-row measurement (wave r85-w1)

Frozen counter: `tools/round-84/mutation-closure.py` (lane bytes, unmodified), invoked exactly as
assigned:
`python3 -I -B <lane>/tools/round-84/mutation-closure.py --root $D --rev f341d0e067ef01d1683a4b360ba41905c2e7bec5 --mutants <lane>/.ufo/waves/round-85/mutants.json --work $S/c2 --json-out after-source-bind.json`

- Sandbox: `$S/clone.qwy0`, branch `r85-c2` = declaration 91eeb72f6a7b13dc96e826117956f90ed89ae3f3 +
  candidate commit f341d0e067ef01d1683a4b360ba41905c2e7bec5 (only the two target files changed, +47/−1);
  `git rev-parse --show-toplevel` verified equal to the clone before the commit.
- Mutant table sha256 `ef031dbe3525ff8454b1b120ed18f88a8918c981c7a4726ab626430e72e1ec41` (frozen bytes, untouched).
- BASE column = `.ufo/waves/round-85/pre/c2/base-mutation-closure.json` (do-nothing control at 91eeb72f).

| row | target | declared case | BASE (91eeb72f) | after (f341d0e) | declared case under mutant | anchor |
|---|---|---|---|---|---|---|
| sb-emdash-optional | tools/round-83/source-bind.py | entry-cites-no-em-dash-refused | survived (declared-case-absent) | **killed** | failures=[entry-cites-no-em-dash-refused] | 1 |
| sb-id-substring | tools/round-83/source-bind.py | id-prefix-not-attributed | survived (declared-case-absent) | **killed** | failures=[id-prefix-not-attributed] | 1 |
| cg-frozen-detector-ge | tools/round-82/conjunction-gate.py | frozen-duplicate-detector-refused | survived (declared-case-absent) | **killed** | failures=[frozen-duplicate-detector-refused] | 1 |
| sb-window-13th (kept) | tools/round-83/source-bind.py | late-single-header | killed | **killed** (unchanged) | failures=[late-single-header] | 1 |
| sb-two-fields-first (kept) | tools/round-83/source-bind.py | duplicate | killed | **killed** (unchanged) | failures=[duplicate, duplicate-after-window] | 1 |
| cg-floor-le (kept) | tools/round-82/conjunction-gate.py | genuine-synthetic-passes | killed | **killed** (unchanged) | failures=[genuine-synthetic-passes] | 1 |

Counter receipt totals at f341d0e (`after-source-bind.json`): mutants 21, killed 6, survivors 15
(all `pc-*` printed-command rows — ExecPrintedCmd scope), inconclusive [], pristine_failed [].

Pristine selftests as measured by the counter (candidate rev): `tools/round-83/source-bind.py` exit 0
green (10 cases, incl. both new), `tools/round-82/conjunction-gate.py` exit 0 green (22 cases, incl. new),
`tools/round-82/printed-command.py` exit 0 green (22 cases, untouched).

Selftest receipts (run as `python3 -I -B <tool>.py --selftest` from a work dir, `TMPDIR=$S`):

- `selftest-pristine.txt` — declaration bytes 91eeb72f: source-bind rc=0 (8 checks), conjunction-gate rc=0
  (21 cases, `SELFTEST cases=21 failures=0`).
- `selftest-candidate.txt` — candidate bytes f341d0e: source-bind rc=0 (10 checks; new cases
  `entry-cites-no-em-dash-refused: ok rc=[1, 1]`, `id-prefix-not-attributed: ok rc=[1, 1]`),
  conjunction-gate rc=0 (`SELFTEST cases=22 failures=0`).

Changes to pre-existing cases: **none**. The only touches of existing code are (a) the source-bind
selftest loop now iterates `FIXTURES + (r85c_entry_cites_no_em_dash_refused(), r85c_id_prefix_not_attributed())`
— two added case-tuple entries, existing tuples byte-identical; (b) one added guarded
`check("frozen-duplicate-detector-refused", r85c_frozen_detector_ge())` line in the conjunction-gate
selftest. Full diff: `candidate.diff`. No tool installs were needed; pacman untouched.
