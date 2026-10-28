# R45-C2 counter — mutation probe (wave 1, seat `R45W1C2CounterMutants`)

Target: `tools/round-45/c2-counter.py`, the interpreter of claim **R45-C2** (`plans/round-45-claims.md`,
clauses 1–3: `scope_size == 6`, `unregistered == []` by **exact path equality**, `thin == []` by the
exit-code cell).

- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Freeze: `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`
- Graded rev exercised: `faa875bc0eb839d15b83c4afa6078819e5a7b381` (wave-1 tip, registry rows landed)
- Original bytes: `sha256 50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025`, 9560 bytes, 268 lines
  — re-hashed after every run, unchanged; `git -C <lane> status --porcelain -- plans/round-45-claims.md tools/round-45` empty.
- Method: copied the frozen file to scratch (`/fast/scratch/hyaku/kaidoku-r45/R45W1C2CounterMutants`),
  applied one byte patch per mutant to the **copy**, ran the same detector
  `python3 -I -B <copy> --selftest` (env `HYAKU_SCRATCH=TMPDIR=<scratch>`), never the original.

## Baseline (unmutated)

```
cmd  python3 -I -B c2-counter.pristine.py --selftest      rc=0   utc 2026-10-28T15:39:10Z
stdout sha256 aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d
C2_SELFTEST: cases=7 failures=0
green, red-unregistered, red-wrong-path-rows, red-thin-exit-cell, red-unknown-rev,
red-frozen-touched, red-scope-size all ok:true
```

Receipt: `receipts/pristine.selftest.txt`.

## Verdicts

| # | mutant | patch locus | expected detector | observed | verdict |
|---|---|---|---|---|---|
| m1 | `endswith` instead of exact path equality | `by_tool.get(path)` → suffix `lookup()` (both directions) | `red-wrong-path-rows` and/or `red-unregistered` stay red | **rc 0, `cases=7 failures=0`, stdout byte-identical to baseline** | **SURVIVED** |
| m2 | a row satisfies a path if **any** cell contains it | `by_tool.get(path)` → scan `cand["cells"]` for `path in c` | `red-wrong-path-rows` / `red-thin-exit-cell` | **rc 0, `cases=7 failures=0`, stdout byte-identical to baseline** | **SURVIVED** |
| m3 | exit-code-cell check dropped | `if len(cells)<3 or not exits_ok(cells[2]): thin.append` → `pass` | `red-thin-exit-cell` | rc 1, `red-thin-exit-cell expect 1 got 0`, `failures=1` | **KILLED** |
| m4 | scope size read as hard-coded six | `len(scope) != 6` → `6 != 6`; receipt `scope_size` → `6` | `red-scope-size` | rc 1, `red-scope-size expect 1 got 0`, `failures=1` | **KILLED** |
| m5 | frozen-path arm removed | `if changed: return 2, frozen_path_changed` → comment | `red-frozen-touched` | rc 1, `red-frozen-touched expect 2 got 0`, `failures=1` | **KILLED** |

Mutant hashes (bytes): m1 `391402f88b43356ab45847f643a56feec6c6225419488a3f52fbc8c44a44271e` (9775),
m2 `252ab71332d5c8f8a14229498dc07470b52778c28203cc96e1f647b4bd14401e` (9732),
m3 `34fd25ff9fc9196daa52f6834d1ff6ede43c2c75d6b68503058725b3666af567` (9517),
m4 `e0dee36d19cdad81562bb56176550b13ff85a6abaa8ee434e9fea19ffb6bbd7d` (9608),
m5 `93e6daa5f1fd69415cbbfa48de1031136362bb8b110d2206390676efbd05e013` (9501).
Every mutant was re-run a second time: identical rc, identical red set, identical stdout sha256
(m1/m2 second-run stdout `aea7e363e5661efc…` — the same bytes as the pristine run).

Patches: `receipts/<mutant>.patch.txt` (unified diff vs frozen). Full selftest output:
`receipts/<mutant>.selftest.txt`. Mutant bodies: `mutants/<mutant>.py`.

## The three kills, named

- **m3 → `red-thin-exit-cell`.** With the third-column check gone, `thin` is always `[]`, so the
  case's deliberately bare cell (`0` met; non-zero otherwise) is scored green where the case
  expects `1`. Killed for the right reason: `got 0`, not a crash.
- **m4 → `red-scope-size`.** With `scope_size` a constant, a five-path scope file is reported as
  `scope_size 6` and exits 0 where `red-scope-size` expects 1. Killed for the right reason.
- **m5 → `red-frozen-touched`.** With the arm deleted, the post-freeze claims-file edit exits 0
  where the case expects 2. Killed for the right reason.

## The two survivors are holes — exact bypass each enables

Both survivors emit **byte-identical** output to the pristine selftest, so no case in the frozen
seven distinguishes them. I proved each is a *false positive generator* with a fixture repo
(`git init` under scratch, freeze == HEAD, scope = the six `SCOPE_TEST` paths) where one scope path
has **no row whose first cell is that path**:

| probe | SKILL.md at the fixture | pristine | mutant |
|---|---|---|---|
| `m1` | five exact rows + row `` `tools/archive/tools/round-44/c.py` `` | rc **1**, `unregistered: ['tools/round-44/c.py']` | rc **0**, `met_target: true`, `registered: [all six]` |
| `m1_reverse` | five exact rows + row `` `tools/round-44/c.py` ``; scope path `tools/round-44/deep/tools/round-44/c.py` | rc **1**, `unregistered: ['tools/round-44/deep/tools/round-44/c.py']` | rc **0**, `met_target: true` |
| `m2` | five exact rows + row `` `tools/round-45/x.py` `` whose **gate** cell cites `` `tools/round-45/y.py` `` | rc **1**, `unregistered: ['tools/round-45/y.py']` | rc **0**, `met_target: true`, `thin: []` |

- **m1 bypass (`endswith`).** A registry row for a *longer* path that ends with the scope path
  registers it (`` `tools/archive/tools/round-44/c.py` `` → `tools/round-44/c.py`), and a row for a
  *shorter* path registers a nested scope path (`` `tools/round-44/c.py` `` → the nested
  `tools/round-44/deep/tools/round-44/c.py`). This is precisely the provenance the claim forbids
  ("path equality, never 'names a path'").
- **m2 bypass (any cell).** A row naming a **different** tool registers a scope path whenever any
  of its other cells mentions it — and, because the row's `cells[2]` is then reused as the
  exit-code cell, `thin` is also judged against the *wrong* row. This is live-adjacent today:
  in the real `SKILL.md` at `faa875bc`, `tools/round-45/frozen-path-preflight.py` is matched by
  **two** rows — its own (row 42) and `tools/round-45/c1-counter.py` (row 43), whose prerequisite
  cell carries that path. Document order currently masks it (42 is exact and comes first), so
  deleting the preflight's own row would leave m2 reporting `met_target: true`.

Why the frozen seven cannot see either: `good_rows()` puts every path in the first cell and nothing
in the other cells; `red-wrong-path-rows` uses *disjoint* names (`tools/round-40/c0..c5.py`), which
are neither suffixes nor citations of the scope paths; `red-unregistered` swaps one first cell for
another disjoint name; `red-thin-exit-cell` edits only the exit cell. Zero of the seven cases
exercises (a) a non-first-cell mention of a scope path, or (b) a suffix-related row. 2/5 mutants
survive on exactly those two gaps.

Minimal cases that would kill them, named for a future freeze (the frozen file may not be edited
now): **`red-suffix-row`** (five exact rows + `` `tools/archive/tools/round-44/c.py` ``, expect 1),
**`red-nested-scope-row`** (scope path nested, only the parent row, expect 1), and
**`red-cited-path-row`** (a row for another tool citing the missing path in its gate cell, expect 1).

## Bound on the damage — the survivors are latent, not live

The instrument body as frozen **is** exact equality (`by_tool.get(path)`), and a mutant body can
only be the one scoring if it exists at `--rev` without any commit in `FREEZE..REV` touching
`tools/round-45/`. The directory freeze arm closes that: I committed an edit to
`tools/round-45/c2-counter.py` and `tools/round-45/x.py` after a fixture freeze and the pristine
counter on the **mutant** body's behalf returned `rc 2 frozen_path_changed:
['tools/round-45/c2-counter.py','tools/round-45/x.py']` (probe `freeze_arm_dir`). So m1/m2 are a
regression-protection gap (a future freeze could land an equality-relaxing counter with a green
selftest), not a defect in this round's measurement: on the real lane, pristine, m1 and m2 produce
**identical receipts** at `faa875bc` — `rc 0`, `scope_size 6`, `unregistered []`, `thin []`,
`registered` all six — and identical `rc 1` do-nothing receipts at the freeze (all six unregistered).

Consequence for the claim text, stated for the L1: predicate clause 2 ("first cell is exactly that
path") is implemented correctly by the frozen bytes but **not pinned** by the frozen selftest. The
claim's kill rule ("Six rows naming other tools still report six unregistered") is strictly narrower
than the predicate: it covers disjoint names only, and says nothing about citations or suffixes.

## Harness correction (recorded, not hidden)

Probe `freeze_arm_dir` was first invoked with `--freeze <rev> --rev <rev>` by a harness slip and
printed `rc 0`, which reads as an arm failure. Re-invoked with the true fixture freeze
(`b07cdc02… → 8a73c4a5…`) it printed `rc 2 frozen_path_changed`. The first output was my error, not
the counter's; the corrected receipt is the one in `probes.json`.

## Receipts and integrity

- `receipts/pristine.selftest.txt`, `receipts/<m1..m5>.selftest.txt`, `receipts/<m1..m5>.patch.txt`,
  `receipts/summary.json` (mutant hashes, determinism re-runs, probe pointer), `receipts/detail.json`
  (per-red-case `expect`/`got`), `receipts/table.json`, `probes.json` (fixture repos + verdicts),
  `mutants/` (pristine and the five bodies).
- Restoration evidence: originals never mutated (same sha256 before/after, clean `git status` on the
  frozen paths); the mutate-then-restore cycle in scratch returned `93e6daa5…` rc 1 → overwritten
  with pristine bytes → `50212d0f…` rc 0, byte-identical to the frozen file.
- Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1C2CounterMutants` removed after the receipts were
  copied here.
- Installs: none (python3 stdlib only). No git/jj mutation anywhere; every git call named `-C <dir>`
  and the only `commit`s were in scratch fixtures under `/fast/scratch`.

## Not run

- The counter was not evaluated at revs other than the freeze and `faa875bc`, and the C1 counter /
  preflight were not mutated (other seats own them).
- No claim was re-derived from `plans/round-45-claims.md` beyond the C2 clauses read there; the
  `thin` semantics beyond "cell names 0, 1 and 2" were not probed.
