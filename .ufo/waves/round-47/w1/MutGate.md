# MutGate — mutation probe of `tools/round-46/gate.py` against R47-C1 clause 7

Seat `MutGate`, round 47 wave 1, mutation-tester. Read-only on the lane tree; every
receipt below was produced in a throwaway clone plus throwaway fixture repos.

**Measured revision** `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` (lane `main` at 17:59Z;
the lane advanced through `09a9f912` (18:04Z) to `b1a058f3` (18:09Z) — `git diff
31b092d..HEAD -- tools/round-47/ tools/round-46/gate.py plans/round-47-claims.md SKILL.md` is
**empty** at both tips, so every value below holds at the lane tip byte for byte).

| object | sha256 |
|---|---|
| `tools/round-46/gate.py` @ 31b092d | `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` |
| `tools/round-47/exact.py` @ 31b092d | `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5` |
| driver `w1/MutGate/mutate.py` | `929742d833ac594e9e36b34d70adaf1052bebb56c10dd0a1d9d50d007164d51d` |
| `receipts/receipts.json` | `d6938d888c8d01a485f3778195ac3b5c85b348c44001ae688e296c9845a588c8` |

`git version 2.56.0`, `python3 3.14.8`. No tool was installed.

Baseline (pristine bytes, claims' own counting command, battery on): exit **0**,
`met_target true`, `failing []`, clause-7 receipt `literal 1 / reversed 0`,
`battery {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`
(`receipts/full-command-with-battery.json`, `baseline`). A baseline failure would have made
every mutant below inconclusive; it did not.

## Why freeze = rev for these runs

`exact.py` derives its frozen set from `plans/round-47-claims.md:205-206` — `plans/round-47-claims.md`
and `tools/round-47/`. `tools/round-46/gate.py` is **not** in that set, so a gate.py mutation never
trips `frozen_path_changed`; the only clause that can see one is clause 7. That is why the probe
commits its mutants as ordinary commits on top of a clone pinned at 31b092d with
`--freeze 31b092d` and reads them at the mutant commit. (Freeze = rev = 31b092d at baseline;
freeze = 31b092d, rev = mutant thereafter.)

## The command

```sh
S=/fast/scratch/hyaku/kaidoku-r47/MutGate
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-47/w1/MutGate/receipts
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/fx"
git -C "$S/fx" checkout -q --detach 31b092d17e77f5064c919383a9bc1e6cbfd2d1ff
printf '.ufo/\n' >> "$S/fx/.git/info/exclude"
export TMPDIR="$S" HYAKU_SCRATCH="$S"
python3 -I -B .ufo/waves/round-47/w1/MutGate/mutate.py \
  --fx "$S/fx" --base 31b092d17e77f5064c919383a9bc1e6cbfd2d1ff --out "$R" --scratch "$S"
```

Per mutant the driver runs the claims' counting command shape (no battery for the sweep;
the battery is exercised separately below, because it does not change the verdict):

```sh
python3 -I -B <fx>/tools/round-47/exact.py --root <fx> \
  --freeze 31b092d… --rev <mutant rev> --no-battery --json-out <fx>/.ufo/scratch/<name>.json
```

Two out-of-band detectors, same bounds on pristine / mutant / restored bytes:

- **D2 behaviour** — `gate.history_touched` over a merge fixture whose *only* touch of
  `plans/merge-only.md` is the merge commit's first-parent diff (the R46-CL6 scenario), plus a
  touched non-ASCII path `corpus/naïve.md` (decode arm) and a commit whose subject is exactly
  `M3` (format arm). Pristine expectation (5 paths):
  `corpus/naïve.md, corpus/plain.md, plans/merge-only.md, plans/x.md, tools/y.md`.
- **D3 forgery** — base → commit that rewrites `plans/round-47-claims.md` → commit that restores
  its bytes. Net `git rev-parse HEAD:plans/round-47-claims.md` **equals** the base blob in every
  case (recorded as `net_blob_identical: true`), so `blob_changed` is empty and only
  `history_touched` can see the in-range tamper.

## Mutation table

`exit` is `exact.py --profile v3`; `c7` is the clause-7 receipt `gate_order_literal/reversed`;
`D2 history` is `history_touched` over the merge fixture. Clause 7's code is
`tools/round-47/exact.py:260-264` — `gtext.count(ORDER)` and `gtext.count(REVERSED)` on the
file's **text**, nothing else.

| # | mutation (target in `gate.py`) | exit | c7 | clause 7 | D2 history (expected 5 paths) | caught by |
|---|---|---|---|---|---|---|
| M01 | flag order → `--diff-merges=first-parent, -m` | **1** | 0/1 | **RED** | unchanged (5/5) | clause 7 — **equivalent mutant** |
| M02 | `--format=` → `--format=%s` | 0 | 1/0 | green | `['\nM', 5-1]` — gains bogus `'\nM'`, **loses `tools/y.md`** | nothing in exact.py |
| M03 | drop `-z` | 0 | 1/0 | green | `[]` (5 lost) | nothing |
| M04 | `--name-status` → `--name-only` | 0 | 1/0 | green | `[]` (5 lost) | nothing |
| M05 | drop `-m` | **1** | 0/0 | **RED** | unchanged (5/5) | clause 7 — **equivalent mutant** |
| M06 | drop the `--` separator | 0 | 1/0 | green | unchanged; **`git log failed`** on the separator fixture | nothing (latent) |
| M07 | pathspec join `*paths` → `*paths[:1]` | 0 | 1/0 | green | 2/5; separator fixture loses `tools/round-47/exact.py` | nothing |
| M08 | status regex `[ACDMRTUXB]` → `[AD]` | 0 | 1/0 | green | `['plans/merge-only.md']` (4 lost) | nothing |
| M09 | decode `utf-8/surrogateescape` → `latin-1` | 0 | 1/0 | green | `'corpus/naÃ¯ve.md'` — **wrong path** | nothing |
| M10 | `return sorted(touched), None` → `return [], None` | 0 | 1/0 | green | `[]` (5 lost) | nothing |
| M11 | append `--no-merges` (literal intact) | 0 | 1/0 | green | 3/5 — **loses `plans/merge-only.md`, `plans/x.md`** | nothing |
| M12 | rev range `{base}..{tip}` → `{tip}..{base}` | 0 | 1/0 | green | `[]` (5 lost) | nothing |
| M13 | regex `^[ACDMRTUXB][0-9]*$` → drop `$` | 0 | 1/0 | green | unchanged (5/5) | nothing — equivalent mutant |

All 13 targets occurred exactly once in the pristine file; all 13 mutants compile
(`py_compile` ok). Per-mutant commit rev, mutant-file sha256, exit, stdout sha256 and UTC are in
`receipts/receipts.json`; the full counter receipts are in `receipts/counter/M*.json`
(each file's own sha256 equals the recorded stdout sha256, because `gate.emit` writes the same
bytes it prints).

**Counts.** 10 of the 13 mutants change the arm's output (M02, M03, M04, M06, M07, M08, M09,
M10, M11, M12). **Clause 7 kills 0 of those 10.** The 3 that leave the output unchanged are
M01, M05, M13 — **clause 7 kills 2 of those 3.** Its discrimination is anti-correlated with
behaviour on this instrument.

## Full counting command (battery on) — the survivors survive it

| rev | exit | failing | battery |
|---|---|---|---|
| baseline | 0 | `[]` | 4 / 4 / 0 / 1 / 0 |
| M10 `return []` | **0** | `[]` | 4 / 4 / 0 / 1 / 0 |
| M11 `--no-merges` | **0** | `[]` | 4 / 4 / 0 / 1 / 0 |
| M12 reversed range | **0** | `[]` | 4 / 4 / 0 / 1 / 0 |
| M01 flag order | 1 | `['gate.py flag order: 0 correct, 1 reversed']` | not built (`code != 0`) |

(`receipts/full-command-with-battery.json`.) The four forgeries score
`('substring-arm', 0, 1), ('duplicate-routed-id', 0, 1), ('stale-mutations-digest', 0, 1),
('flag-order-drift', 0, 1)` in every one of those runs — the battery is uniform because it is
built from the same mutated `gate.py` it is supposed to police.

## Findings

### F1 — clause 7 is a text count; its two "kills" are equivalent mutants

`exact.py:260` counts the literal `"-m", "--diff-merges=first-parent"` and its reverse in
`gate.py`'s bytes. M05 drops `-m` (behaviour identical: `--diff-merges=first-parent` alone
already yields first-parent diffs) and clause 7 goes red on `0 correct, 0 reversed`. M01 swaps
the order: raw `git log` bytes grow 39 → 52 and `plans/x.md` is printed **four** times instead of
three (`diff --diff-merges=first-parent -m` ≡ `-m`), but `history_touched` is set-valued
(`gate.py:99-114`) so the graded output is identical. Clause 7 therefore accepts or rejects on
spelling. This is the R46-CL2 hole (`blobberish` satisfies `blob` — containment instead of
meaning, `plans/round-47-claims.md:54`) one level up: the clause binds the *spelling* of an
argument pair, not the property the pair is meant to guarantee.

### F2 — the R46-CL6 blindness is reachable with the literal intact: M11

`gate.py:99` gains `--no-merges` **after** the pinned pair. The pinned literal still occurs
exactly once, the reversed pair zero times, so clause 7 is green; the merge commit's
first-parent resolution stops being reported (D2 loses `plans/merge-only.md` and `plans/x.md`),
and the whole counter exits **0** — with the battery nominal. The one mutation that reproduces
the routed defect in its own vocabulary is the one clause 7 cannot see. Repro: apply
`M11` from `w1/MutGate/mutate.py` to a copy of `gate.py`, then run the counting command; the
receipt prints `gate_order_literal 1, gate_order_reversed 0, failing []`.

### F3 — the frozen-instrument arm is unpinned; a commit-and-revert of the claimed file scores green

D3 builds `base → tamper plans/round-47-claims.md → restore its bytes`; the claims blob at tip
equals the claims blob at base in all four branches (`net_blob_identical: true`).

| gate.py at rev | exit | failing | `frozen_path_changed` |
|---|---|---|---|
| pristine | **2** | `[]` | `['plans/round-47-claims.md']` |
| M10 `return []` | **0** | `[]` | `[]` |
| M12 reversed range | **0** | `[]` | `[]` |
| M11 `--no-merges` | 2 | `[]` | `['plans/round-47-claims.md']` |

(`receipts/counter/forgery-*.json`.) One flipped return or one reversed rev range turns the
frozen-path arm off, and no clause of `exact.py` reads that return. `frozen_path_changed` is the
only thing standing between the lane and an in-range rewrite of the frozen counter; it is
computed by code that is itself outside the frozen set.

### F4 — an *uncommitted* `gate.py` edit is invisible, and the receipt is byte-identical

With `M10` written into the clone's worktree and **not committed**:

| phase | exit | stdout sha256 |
|---|---|---|
| before (pristine) | 0 | `3f351726bd25200fe8589eceee6d81dd366bb1d2c29e815c6fd387e9d8c967fa` |
| while dirty (`M tools/round-46/gate.py`) | **0** | `3f351726bd25200fe8589eceee6d81dd366bb1d2c29e815c6fd387e9d8c967fa` |
| restored | 0 | `3f351726bd25200fe8589eceee6d81dd366bb1d2c29e815c6fd387e9d8c967fa` |

(`receipts/dirty-worktree-m10.json`.) `gate.freeze_state` refuses a dirty worktree only under the
frozen pathspecs (`gate.py:173,187-191`), and gate.py is not one. `exact.py` executes the library from
the worktree (`exact.py:23-24`) while grading committed bytes — so the F3 guard covers the claimed
instrument and not the shared library it imports.

### F5 — the flag-order harm, measured

Same conflicting-merge fixture, five argument shapes, raw `git log … --name-status -z --format=`
output:

| flags | bytes | `plans/x.md` occurrences | `history_touched` |
|---|---|---|---|
| `-m --diff-merges=first-parent` (canonical) | 39 | 3 | `['plans/x.md']` |
| `--diff-merges=first-parent -m` (swapped) | 52 | 4 | `['plans/x.md']` |
| `--diff-merges=first-parent` | 39 | 3 | `['plans/x.md']` |
| `-m` | 52 | 4 | `['plans/x.md']` |
| `-m --diff-merges=first-parent --no-merges` | 26 | 2 | merge diff gone entirely |

`SKILL.md:639` says the reordered pair "prints a merge twice and blinds the arm". The first half
is true (3 → 4 occurrences). The second half is **false at the consumer**: `touched` is a set, so
duplicates are idempotent and the graded output is identical. The blindness in that table row is
produced by `-m` *alone* (or by `--no-merges`), not by the order — and clause 7 pins the order.

## Restoration evidence

- `gate.py` rewritten to the pristine bytes and checked by sha256:
  `c3ba6b93…` = pristine (`restore.equals_pristine: true`).
- `git -C <fx> status --porcelain -- tools/round-46/gate.py` → **empty**.
- Counter re-run at the base rev after restore: exit **0**, stdout sha256
  `3f351726…`, identical to the pre-mutation baseline.
- D2 re-run on the restored bytes: identical to pristine on all three fixtures
  (`behaviour_matches_pristine: true`).
- The scratch clone, its fixtures and `$S` were removed after the receipts were copied into
  `w1/MutGate/receipts/`. Nothing was written to `tools/`, `plans/`, `SKILL.md`, `SCORECARD.md`,
  `LOG.md` or the fleet repo; no git mutation ran outside a fixture repo whose
  `rev-parse --show-toplevel` was asserted equal to the fixture path.

## Calibration notes (harness bugs found and fixed, discarded runs)

1. First harness read the claims blob with `stdout.strip()`, which stripped the trailing newline;
   the "restore" commit then differed by one byte and the forgery scored exit 2 for the wrong
   reason. Fixed to raw bytes; the discarded run's receipts were overwritten.
2. First harness pinned a hard-coded base while the lane was committing (`07d2894` → A7), so
   `freeze..rev` silently spanned two amendment commits and `frozen_path_changed` fired for
   `tools/round-47/`. Every later run pins the base to the clone's own HEAD and **asserts**
   `--show-toplevel`.
3. The merge fixture first gave `plans/x.md` a non-merge touch on the main branch, which masked
   `--no-merges`; it was rebuilt so the merge commit is the only toucher. The earlier
   `M11 survived` row was therefore a fixture defect, not a result — it is now `M11 blinds`.
4. `M09`'s target had to be widened to a two-line unique string: `r.stdout.decode("utf-8",
   "surrogateescape")` occurs twice in `gate.py` (`history_touched` and `dirty`).

**Not run.** R47-C2 (`record.py`) — out of this seat's scope, not touched. `--profile v2`
sampled on M01/M05/M10/M11/M12 and the baseline only (`receipts/profiles-v2-v3.json`: v2 green on
all five, v3 red only on M01/M05). The four battery forgeries were not re-scored per mutant rev
beyond the aggregate fields in `full-command-with-battery.json`. The separator hazard (M06) is
latent at the measured rev: `git for-each-ref` shows no ref named like a frozen path, and the
hazard needs exactly one such ref (`refs/heads/plans/round-47-claims.md`) plus the file existing —
both reproduced in `fixture-separator`, where M06 returns `('git log failed')`.

## What this means for the landing (report only — frozen bytes untouched)

Clause 7 as written cannot fail on any gate.py defect except a change in the spelling of one
adjacent argument pair, and it fails on two changes that leave the arm's output unchanged. If the
L1 wants R47-C1 to bind R46-CL6, the clause has to bind the arm's *output* over a fixture where a
merge commit is the only toucher of a path (the `history` fixture in `w1/MutGate/mutate.py`,
`build_history_fixture`), not the library's text — and the library itself has to be inside the
frozen set, otherwise F3 and F4 hold whatever the clause says.
