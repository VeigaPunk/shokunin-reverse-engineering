# R38W2Separability — reproduction

Instrument: the FIRST-FREEZE counters only (attempt 2's rule), extracted from
`e059ca9391642d5b71b6662cabcbdce0d9308719`:

| file | sha256 |
|---|---|
| `c1-frozen.py` (= `git show e059ca93:tools/round-38/c1-counter.py`) | `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` |
| `c2-frozen.py` (= `git show e059ca93:tools/round-38/c2-counter.py`) | `7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7` |

Both copies are stored beside this file (`c1-frozen.py`, `c2-frozen.py`); the C1 sha256 equals the
`a7a62b09…` digest the round-38 lesson quotes for the first-freeze counter.

## Fixture repo

Scratch root `S=/fast/scratch/hyaku/kaidoku-r38/R38W2Separability` (removed after the run; every
cited receipt was copied into this directory).

```bash
D="$(mktemp -d "$S/fx.XXXX")"; git -C "$D" init -q
git -C "$D" rev-parse --show-toplevel          # verified == $D (realpath) before any commit
git -C "$D" fetch -q --no-tags /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    refs/heads/main:refs/remotes/lane/main
# fixture identity only, per-commit: GIT_AUTHOR_* / GIT_COMMITTER_* = fixture / fixture@invalid
```

The lane repository was only read (`git show`, `git ls-tree`, `git diff`, `git fetch` from it).

Counter invocations (every run names `-C "$D"` through `--root`; `TMPDIR=$S`,
`HYAKU_SCRATCH=/fast/scratch/hyaku`):

```bash
python3 -I -B c2-frozen.py --root "$D" --rev <REV> \
  --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 --json-out <RECEIPT>
python3 -I -B c1-frozen.py --root "$D" --rev <REV> \
  --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>
```

## Fixture commit map (scratch shas; trees are what matters, parents are given)

| id | parent | edit | purpose |
|---|---|---|---|
| `landed_c2` | — | `0fc6113376a156fddc3ec385386d71c3a4a9f690` unchanged | landed tip baseline |
| `landed_c1` | — | `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` unchanged | C1 verdict revision |
| `base` | — | `77091b492cc53f8743bd0701b1e7d5e66123dd84` unchanged | before-state |
| `a0` | landed_c2 | drop `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`, its coverage-map row, `corpus/evidence/round-38/c1/**`; count left 126/126 | unrestated arithmetic coupling |
| `a1` | landed_c2 | as `a0`, count restated 126/126 → 125/125 | seat instruction, count only |
| `a1b` | landed_c2 | entry + **all three** README lines naming the stem + receipts dropped, count 125/125 | literal instruction state |
| `a2` | landed_c2 | `a1b` + SCORECARD prose de-coupled ("one entry … unblob-format-matrix") + PROVINCE line 157 reverted to base text | de-coupled green state |
| `a3` | landed_c2 | only `corpus/evidence/round-38/c1/**` dropped | receipts-independence probe |
| `a4` | landed_c2 | entry present, its coverage-map row dropped | partial C1 landing |
| `a5` | landed_c2 | C1 landed, SCORECARD count left at 124/124 | C2 restatement probe |
| `b` | landed_c1 | PROVINCE line 44 reverted to the base `evidence/doctor/` pointer | C1 landed, C2 not |
| `b2` | landed_c2 | `b` edit applied on the landed tip | same, on the final tree |

Variant `a2`'s exact diff against the landed tip is `a2-decoupled.diff` in this directory.

## Receipts

`c1-*.json`, `c2-*.json` — full counter JSON for each run (frozen counter's own output, including
`argv`). Summary table is in the seat report `../../R38W2Separability.md`.
