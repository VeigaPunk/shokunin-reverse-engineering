# ExecSourceBind — wave r85-w1 seat report (R85-C2 depth rows)

Lane `kaidoku-shokunin`, round 85, L1 `KaidokuR85`. Declaration 91eeb72f6a7b13dc96e826117956f90ed89ae3f3;
frozen table `.ufo/waves/round-85/mutants.json` (sha256 `ef031dbe3525ff8454b1b120ed18f88a8918c981c7a4726ab626430e72e1ec41`); frozen counter `tools/round-84/mutation-closure.py` (unmodified).

## Result

Three declared kills added; three BASE kills retained; nothing in scope regressed.

| row | target | declared case | BASE | after |
|---|---|---|---|---|
| sb-emdash-optional | tools/round-83/source-bind.py | entry-cites-no-em-dash-refused | survived | **killed** |
| sb-id-substring | tools/round-83/source-bind.py | id-prefix-not-attributed | survived | **killed** |
| cg-frozen-detector-ge | tools/round-82/conjunction-gate.py | frozen-duplicate-detector-refused | survived | **killed** |
| sb-window-13th (kept) | tools/round-83/source-bind.py | late-single-header | killed | **killed** |
| sb-two-fields-first (kept) | tools/round-83/source-bind.py | duplicate | killed | **killed** |
| cg-floor-le (kept) | tools/round-82/conjunction-gate.py | genuine-synthetic-passes | killed | **killed** |

Counter receipt `after-source-bind.json` at sandbox rev f341d0e067ef01d1683a4b360ba41905c2e7bec5:
mutants 21, killed 6, survivors 15 (all `pc-*` printed-command rows, ExecPrintedCmd's scope),
inconclusive [], pristine_failed []; all three targets pristine green.

## Candidate bytes (wave dir, never the lane tree)

- `candidate/tools/round-83/source-bind.py` — `r85c_entry_cites_no_em_dash_refused()` /
  `r85c_id_prefix_not_attributed()` at end of file, each registered by one case-tuple entry
  (`FIXTURES + (…)` in the selftest loop). Each case runs the production CLI path
  (`entry_cites` via `--entry/--sid/--json-out` subprocess), asserts exact rc + finding JSON, and
  fails under its mutant (em-dash-optional regex attributes prose; substring membership attributes S2999).
- `candidate/tools/round-82/conjunction-gate.py` — `r85c_frozen_detector_ge()` at end of file,
  registered by one guarded `check("frozen-duplicate-detector-refused", …)`; asserts the production
  re-derived `frozen_killed` is False for a synthetic genuine receipt whose declared-case detector row
  is duplicated (mutant's `>= 1` accepts it).
- `candidate.diff` vs 91eeb72f: 2 files, +47/−1. No predicate, kill rule, target, `tools/round-84/`
  file, mutant table, or `pre/` fixture touched; no pre-existing case changed or weakened.

## Evidence

- `selftest-pristine.txt` (91eeb72f bytes): source-bind rc=0; conjunction-gate rc=0 (21 cases).
- `selftest-candidate.txt` (f341d0e bytes): source-bind rc=0 (10 checks, both new `ok rc=[1, 1]`);
  conjunction-gate rc=0, `SELFTEST cases=22 failures=0`.
- `per-row.md` — full table incl. kept rows and mutant-failure lists.
- Counter command run exactly as assigned, sandbox clone verified
  (`rev-parse --show-toplevel` == clone) before the throwaway-identity commit; no git writes outside
  the scratch clone; lane tree untouched outside the seat wave dir.

## Deviations / risks

- Counter `ok=false` at this revision is expected mid-wave: the 15 surviving `pc-*` rows belong to
  ExecPrintedCmd. This seat's six rows are all killed.
- Kill binding remains name-level per the frozen table (declared round limit; not remediated here).
- No tools installed (none needed); pacman paused and untouched. Blockers: none.
