# EX-15 fixture measurements — before→after (chain c2 claim)

All runs 2026-10-19 by seat EX-15. Suite: 16 cases (`../cases.json`),
`hard_fail=0` in both phases. Raw per-case output and `results.json`:

| phase | instrument | sha256 | dir |
|---|---|---|---|
| before | EX-16's frozen pre-edit copy (`claims/c2/EX-16/tools/census-before.py`) | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (490 L) | `before-6f1d19ff/` |
| after | live `.ufo/gates/c1-census-v10.py` (r9 final at this seat's close) | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` (601 L) | `after-d0772ce8/` |

Commands (verbatim):

```
python3 gen_fixtures.py            # SELF-CHECK OK: 33 files, markers per parsed SCOPE, no stray gate tokens
python3 run_fixtures.py --phase before --instrument <EX-16 frozen copy> \
        --expect-sha 6f1d19ff… --json-check      # 16 cases, hard_fail=0, exit 0
python3 run_fixtures.py --phase after  --instrument .ufo/gates/c1-census-v10.py \
        --expect-sha d0772ce8… --json-check      # 16 cases, hard_fail=0, exit 0
                                                 # (same result at a4c16763 and df9ffdf9)
sha256sum -c-style manifest verify  # 33 files, 0 bad
```

Harness reuse was verified from a foreign cwd (`/var/tmp`) with the documented
command form — exit 0, same results.

## Instrument revisions inside the round (measured anew each time)

| rev | sha256 | floor semantics | this seat's measurement |
|---|---|---|---|
| v10 | `6f1d19ff…` | none (G2's vacuous second disjunct) | before-column, all H1/H3 injections silent-PASS |
| r9-v1 | `82fb807e…` | global: `current-ok > 0` | after-column (14-case v1 layout): H1/H3 all FAIL; folded-block FAIL with `current-ok loci=0, total loci=1` |
| r9-v2 | `c95a5cf3…` | per-file, blocks counted | refused on sha churn before running; PL-2 §0 records it as claim-breaking (false FAIL on HEAD) |
| r9-v3 | `df9ffdf9…` | per-file, detections counted | after-column re-run: all green; folded-block PASS `SCORECARD.md=1`; snapshot kept in `after-df9ffdf9/` |
| r9-v4 | `a4c16763…` | identical to r9-v3 (header/Usage text only) | after-column re-run; snapshot kept in `after-a4c16763/` |
| r9-v5 | `d0772ce8…` | identical to r9-v3/v4 (docstring/naming text only) | final after-column at this seat's close; snapshot kept in `after-d0772ce8/` |

## Discrimination summary (measured)

* H1 silent-PASS → declared FAIL: `miss-skill`, `miss-skill-dir`,
  `miss-skill-dangling`, `miss-skill-mode000`, `miss-province`,
  `miss-scorecard`, `miss-all`, and the H1b residual `empty-skill` —
  before PASS/FAIL via markers, after FAIL exit 1 with the declared
  `UNREADABLE (could-not-evaluate)` class naming the file.
* H3 blind-PASS → declared FAIL: `blind-nonempty` (data-side, zero loci in a
  non-empty scope), `partial-blind-skill` (per-file collapse with loud peers).
* Invariance: `ctl-head` PASS before and after; `current-ok-ctl` PASS before and
  after (`PROVINCE.md=1, SCORECARD.md=1, SKILL.md=1`).
* Readings pinned: `hist-only` = PER-FILE floor; `fold-mixed-block` =
  ASSERT-COUNT (det-counted) floor.
* Still open, measured: `h2-inline-excuse` PASS, `h5-gate-free` PASS.
