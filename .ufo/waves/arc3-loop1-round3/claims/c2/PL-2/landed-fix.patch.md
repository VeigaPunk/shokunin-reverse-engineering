# landed-fix record — interim harness defect in the landed revision `73c15b84…`

Seat PL-2 · chain c2 · wave `arc3-loop1-round3` · 2026-10-19 · **record only, no
target was written by this seat**. This is the round's caught-and-fixed defect
note for the interval between EX-21's landing revisions, kept because the target
churned inside the wave (the round-2 D8 shape) and the fix pattern generalizes.

## Timeline (all UTC 2026-10-19, all snapshotted to `/var/tmp/pl2`, never `/tmp`)

| revision | first observed | selftest (measured) | note |
|---|---|---|---|
| `112d01dc…` (r2 landed, 889 lines) | HEAD baseline | `CLEAN 15/15 exit 0` | the plan's base |
| `73c15b84…` (1109 lines) | 13:12Z, two reads 2 s apart identical | **`DIRTY cases=21 passed=20 failed=1 exit=3`** | interim; defect below |
| `7cd19c3c…` (1155 lines) | 13:13Z, re-read identical | `CLEAN cases=22 passed=22 failed=0 exit 0` | defect gone, 22 case names = the plan's set |

## Defect (revision `73c15b84…`)

```
case require-paths-blocks-partial-reference     FAIL  (TypeError: _run_verify() got an unexpected keyword argument 'require_paths')
CUSTODY_PAIR_SELFTEST: DIRTY cases=21 passed=20 failed=1 exit=3
```

Reproduced **in place** and on a scratch copy (same output; the case is not
environment-dependent). Cause: the two new call sites

```
 1013:        rc_gate = _run_verify([str(rec), "--live"], out_gate, require_paths=5)
 1019:        rc_pass = _run_verify([str(rec), "--live"], out_pass, require_paths=1)
```

call the in-process harness with a keyword it did not accept —

```
 1049:def _run_verify(argv, out_path: Path) -> int:
```

— although its body already built the Namespace with `require_paths=None`
(`:1053`). The flag worked from the CLI (`--require-paths 5` measured `exit 2` +
`REFERENCE-COVERAGE`), so only the selftest's own coverage was affected: the
claim's "selftest … at exit 0" clause was unmet at that revision.

## Two fixes, both measured (applied to scratch copies of `73c15b84…` only)

- **A2 — call sites argv-style** (the harness's declared interface): replace the
  two calls with
  `_run_verify([str(rec), "--live", "--require-paths", "5"], out_gate)` /
  `… "--require-paths", "1" …`. Result: sha256 `58c92ba6…`,
  `CLEAN cases=21 passed=21 failed=0 exit=0`.
- **B — thread the argument through the signature**: `def _run_verify(argv,
  out_path: Path, require_paths=None) -> int:` plus
  `if require_paths is not None: ns.require_paths = require_paths` before the
  dispatch. Result: sha256 `a6668d30…`,
  `CLEAN cases=21 passed=21 failed=0 exit=0`.

Both were superseded 60 s later: at `7cd19c3c…` no `require_paths=` call site
remains and the selftest reads `CLEAN cases=22 passed=22 failed=0 exit=0`
(the earlier defect is not reproducible there; recorded as the D8-shape churn
note, not as a live blocker). Also closed at `7cd19c3c…`: `case_label` now uses
`TOOL_PATH` (the identity arm), so selftest case 7 measures the running bytes
instead of a sibling filename.

## Why this record stays

The failure mode generalizes: extending an in-process selftest harness with a
new argument requires threading it through **both** the call sites and the
signature; a Namespace default alone is not a contract. The wave's own
verification seats (EX-25, CR-4) were probing the same revisions — a
DIRTY-selftest revision must never be the one the receipts self-pin, which is
why the §4 coupled-landing set in `plan.md` couples the tool, README, row and
receipt identities into one commit.

## Remaining coupling gaps at `7cd19c3c…` (checked 13:14Z, not this seat's write)

- `.ufo/gates/custody-pair/README.md`: the selftest paragraph is already at
  `22 cases` (`:124-135`) but the class itself is invisible — `grep -c
  UNEVALUABLE` = **0** in the whole file; the exit table (`:87-95`) still ends at
  `| 13 | ABSENT |` with no `| 14 | UNEVALUABLE |` row, the capture paragraph
  (`:96-98`) still reads only `0`/`13`, and the precedence line (`:101-102`) is
  still `CONTENT-DRIFT > ABSENT > …` without `UNEVALUABLE`.
- `SKILL.md:390`: the `custody-pair` registry row still says `15 fixture cases`,
  its worst-finding map has no `14`, and its precedence string omits
  `UNEVALUABLE`.
- Both are items 2/3 of `plan.md` §4 and remain required for the claim's
  same-commit coupling clause (one voice per row — round-2 D10).