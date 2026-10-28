# R45W1C2CounterMutants — mutation probe of the frozen C2 counter

Seat `R45W1C2CounterMutants`, round 45 wave 1. Target: `tools/round-45/c2-counter.py` (claim **R45-C2**),
frozen at `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`. Full report, patches and per-run receipts:
`.ufo/waves/round-45/w1/R45W1C2CounterMutants/` (`report.md`, `receipts/`, `mutants/`, `probes.json`).

Target bytes `sha256 50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025`; untouched
(re-hashed after every run, `git status --porcelain -- plans/round-45-claims.md tools/round-45` empty).
Detector for every run: `python3 -I -B <copy> --selftest`, scratch under
`/fast/scratch/hyaku/kaidoku-r45/R45W1C2CounterMutants` (removed after receipts were copied).

## Unmutated selftest line

```
rc=0  utc 2026-10-28T15:39:10Z  stdout sha256 aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d
C2_SELFTEST: cases=7 failures=0
```

## Results — 3 killed, 2 survived

| mutant | expected detector | observed | verdict |
|---|---|---|---|
| m1 `endswith` instead of exact path equality | `red-wrong-path-rows` / `red-unregistered` | rc 0, `cases=7 failures=0`, stdout byte-identical to baseline | **SURVIVED** |
| m2 any cell contains the path | `red-wrong-path-rows` / `red-thin-exit-cell` | rc 0, `cases=7 failures=0`, stdout byte-identical | **SURVIVED** |
| m3 drop the exit-code-cell check | `red-thin-exit-cell` | rc 1, `red-thin-exit-cell expect 1 got 0` | KILLED |
| m4 scope size hard-coded to six | `red-scope-size` | rc 1, `red-scope-size expect 1 got 0` | KILLED |
| m5 drop the frozen-path arm | `red-frozen-touched` | rc 1, `red-frozen-touched expect 2 got 0` | KILLED |

Each killed mutant fails for the right reason (`got` is the false pass, not a crash), and each was
re-run: identical rc, red set and stdout sha256.

## The two holes, with the exact bypass demonstrated

Fixture repos (scratch `git init`, freeze == HEAD, six-path scope) in which one scope path has **no
first-cell row** — pristine 1, mutant 0:

- **m1**: five exact rows plus `` `tools/archive/tools/round-44/c.py` `` → registers
  `tools/round-44/c.py` (row is a *suffix extension* of the scope path); the reverse direction lets
  a top-level row register a **nested** scope path (`tools/round-44/c.py` →
  `tools/round-44/deep/tools/round-44/c.py`). `met_target: true`, pristine names the path.
- **m2**: a row for `` `tools/round-45/x.py` `` whose gate cell merely cites
  `` `tools/round-45/y.py` `` registers `y.py`, and its `cells[2]` is then reused as the exit-code
  cell, so `thin` is judged against the wrong row. `met_target: true`, pristine names the path.
  Live-adjacent: at `faa875bc` the preflight path is matched by both its own row and
  `tools/round-45/c1-counter.py`'s prerequisite cell; only document order keeps the receipt honest.

Neither survivor is reachable by the frozen seven because `good_rows()` only ever writes first cells,
`red-wrong-path-rows` uses disjoint names, and no case has a suffix-related row or a non-first-cell
mention. 2/5 survival = the selftest does not pin predicate clause 2.

## Bounded severity

The frozen body *is* exact equality; a mutant body could only score a rev in which it already
existed without a post-freeze touch of `tools/round-45/`, and that touch is caught: editing
`tools/round-45/c2-counter.py` after a fixture freeze gave `rc 2 frozen_path_changed:
['tools/round-45/c2-counter.py','tools/round-45/x.py']`. On the real lane pristine, m1 and m2 produce
**identical receipts** at `faa875bc` (rc 0, `scope_size 6`, `unregistered []`, `thin []`, six
registered) and identical rc 1 do-nothing receipts at the freeze. So: a regression-protection gap
for the next freeze, not a defect in this round's measurement.

## For the L1

Predicate clause 2 is implemented correctly but not pinned by the frozen selftest; the claim's kill
rule ("six rows naming other tools still report six unregistered") is narrower than the predicate —
it excludes disjoint names only, not citations or suffixes. Killing cases to add at the next freeze,
named: `red-suffix-row`, `red-nested-scope-row`, `red-cited-path-row`.

Harness note (recorded, not hidden): `freeze_arm_dir` was first run with `--freeze <rev> --rev <rev>`
by my slip (rc 0); re-run with the true freeze it is `rc 2`. The corrected receipt is
`probes.json`; the slip was mine, not the counter's.

Not run: other revs, the C1 counter and preflight bodies (other seats), `thin` semantics beyond
"names 0, 1 and 2". Installs: none. No git/jj mutation outside scratch fixtures.
