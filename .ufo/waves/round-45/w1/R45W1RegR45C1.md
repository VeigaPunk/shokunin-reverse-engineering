# R45W1RegR45C1 — registry row for `tools/round-45/c1-counter.py`, verified at the freeze

Seat `R45W1RegR45C1`, round 45 wave 1, leaf, lane `kaidoku-shokunin`. Read-only on the lane
tree; all writes are under this wave directory. Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (re-derived independently by two pathspecs, both
same). `HEAD` at run time `faa875bc`; the claims' measured revision `1f4b27f8`. Python
3.14.8, no installs or upgrades needed or made, no network.

Deliverables under `.ufo/waves/round-45/w1/R45W1RegR45C1/`:

- `row.md` — the exact 7-cell row, cell-by-cell grounding, pinned-input identities, and a
  clearly-labelled optional delta row.
- `receipt.md` — every command run, with exit code, stdout sha256 and UTC stamp; the arm and
  mutation matrices; the limits; the not-run list.

## The row

The row is **already landed at `SKILL.md:1640`** (`### Round-44/45 instrument registry`,
post-freeze commit `abfeda50`) and was verified cell by cell: no cell is wrong, so landing it
again is a no-op. sha256 of that line plus newline
`2c30eb70ea075dcf8c4c6aa02c032c7ab3314030b339a5221d45a6c354657731`, 7 cells, 529 bytes.

First cell is exactly `` `tools/round-45/c1-counter.py` ``. Exit cell names all three codes;
`2` is measured on `frozen_path_changed` (direct touch, restored touch, bulk sweep, and a
claims-file-only touch), unknown `--rev`, non-ancestor freeze, absent `SKILL.md`, and usage,
and a `2` receipt carries `verdict: could_not_evaluate` with **no** `met_target` key.

**Pinned inputs**, with identity at the freeze:

| input | identity | use |
|---|---|---|
| `plans/round-45-claims.md` | blob `f93df4c3`, sha256 `56bacf31…`, 175 lines | frozen pathspec only; prose never parsed |
| `tools/round-45/frozen-path-preflight.py` | blob `b4239827`, sha256 `633ebc05…` | extracted from `--rev`, run `--selftest` in scratch |
| `SKILL.md` `## Queue-drain craft` | not frozen (graded surface), read at `--rev` | split on the literal `"## Queue-drain craft "`; block 22 = the `<!-- freeze-integrity-table v1 -->` block |

**Selftest counts measured** on the frozen bytes (sha256 `2cfc5a48…`, 366 lines): the counter
is **9 cases**, `C1_SELFTEST: cases=9 failures=0`, exit 0, stdout sha256 `296734f2…`; the
interpreter it drives is **11 cases**, `PREFLIGHT_SELFTEST: cases=11 failures=0`, stdout
sha256 `9f03df65…`. Both stdout texts are byte-identical to `controls/c1-selftest.txt` and
`controls/preflight-selftest.txt`.

Lane behaviour reproduced exactly: the freeze do-nothing receipt **equals**
`controls/ctl-c1-0-do-nothing.json`, the base receipt **equals** `ctl-c1-0-base.json`, and the
counter exits 0 with `met_target true` at both `1f4b27f8` and `HEAD`. Freeze integrity of the
real range is clean (`touched/restored/blob_changed/dirty` all empty; zero merge commits).

## Headline finding — the frozen-path arm fails open on a merge commit

`frozen_path_changed()` is `git log --name-only` **without** `-m`/`--diff-merges`. On a merge
commit whose conflict resolution edits a frozen path, that invocation prints the commit
header and **no paths**, so the arm sees nothing and the counter continues instead of exiting
2. Measured on a fixture where both parents are clean of the frozen path:

- `c1-counter` on `F1..M2`: **exit 0**, `frozen_path_changed []`, `met_target true`,
  `failing []` — while `tools/round-45/c1-counter.py` went `4ce400b2…` → `d98d51e3…`.
- `frozen-path-preflight.py` on the same range: **exit 1**,
  `touched [{path: tools/round-45/c1-counter.py, status: M}]`.

So claim R45-C1's kill rule ("a commit in `FREEZE..REV` touching a frozen path makes the
counter exit 2 without printing `met_target`") is false for merge commits, and the arm fails
in the dangerous direction. The selftest cannot see it: `red-frozen-touched-is-exit-2` builds
a direct commit. This is the R34b class block 22 itself cites — the case set holds while the
surface is shortcut-reachable.

Scope of the damage, stated honestly: **no measured score is affected.** The round's history
has zero merges (`git rev-list --merges f762b727..HEAD` empty), the frozen-path diff is empty,
and both gates score `HEAD` clean. The preflight — the gate that blocks a landing — uses
`-m --diff-merges=first-parent` and does catch the shape. For wave 2 the options are (a) a v2
counter whose arm is `-m --diff-merges=first-parent --name-status`, (b) a non-merge
qualification in the claim's kill rule, or both. The instrument is frozen, so neither can be
done now.

## Other limits measured (all in `receipt.md`)

1. **Structural-only rows pass.** Eight `| x | y | 0 | z |` rows score `met_target: true`
   (disclosed by block 22's own prose; now measured).
2. **Citation regex is narrower than "citation".** Only `corpus/(knowledge|lessons)/*.md` and
   `plans/*.md` are counted/resolved; a `tools/…:9999` reference in the block is ignored and
   the run stays green. `block22_refs` under-counts rather than over-counts.
3. **Crash maps to `1`, not `2`.** Renaming the heading to `## Queue-drain craft(` raises
   `IndexError`; exit 1 with empty stdout. Since `SKILL.md` is not frozen, a later round can
   produce "not met" for a predicate it never evaluated.
4. **Exit-2 receipts drop `freeze`/`rev`.** Two different could-not-evaluate events
   (`A-touch`, `A-restored`) hash identically (`0db762f1…`); a `2` is auditable only from the
   command line.
5. **`frozen-path-preflight.py --selftest` leaves its fixtures** under
   `$HYAKU_SCRATCH/kaidoku-r45/preflight-selftest/` (no removal per case; 24 directories
   observed). The counter-driven path is clean because the counter removes its wrapper. That
   belongs to the preflight's row.
6. Worktree dirt is invisible to the counter by design (it reads objects); the dirty arm is
   the preflight's, and the row's write scope correctly does not claim otherwise.

## Recommendation to the L1

- **Do not add a second row.** If you adopt the delta wording (exit-2 set named, merge
  qualification disclosed, measurement basis explicit; sha256
  `dc4cf9fdd1b5aa256964f63504f52bda7293121e7805b8a33e0144817a65a08a`, 7 cells), **replace
  `SKILL.md:1640`** — the c2 counter keeps the first matching row per path.
- If you keep the landed row, read it with this caveat: its cell 3 ("including
  `frozen_path_changed`") is true only for non-merge commits. The house style already
  discloses such limits inside rows (cf. the round-38 row's "an unknown or unresolvable
  revision is not detected"), so the delta is consistent with precedent rather than novel.
- The merge failure is a **wave-2 hardening item and a claim-text truth fix**, not a wave-1
  score change.

## Agreement with sibling seats

`--selftest` stdout hashes (`296734f2…`, `9f03df65…`) match `R45W1C1CounterMutants.md` and
`R45W1C1SelftestFromFreeze.md`; the controls match their measured receipts. The mutants seat
probes the counter's *code* (two survivors: block count tested only from below, marker clause
exit-redundant); this seat probes the *SKILL surface and history*. The results are disjoint:
the surface shapes I ran against pristine code (23 blocks, duplicate marker, 7 rows, `ok`
exit cell, stripped marker) are caught exactly as `evaluate()` reads. No disagreement found.

## Not run

No corrupted object store, no shallow clone, no read-only `--json-out`, no rebase/amend/
replacement-ref history rewrites, no re-scoring of the R45-C2 or round-44 instruments, and no
network source opening (S140/S141 are the sources seats').

Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45C1` was removed after these files were
written. The lane tree was never written to; every lane git call was read-only.
