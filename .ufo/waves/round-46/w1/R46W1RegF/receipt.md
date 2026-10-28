# R46W1RegF — receipts

Seat `R46W1RegF`, round 46 wave 1, lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `31820472784284727546808acc31b3ea1e73919b`. Scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegF` (removed after these files were copied here).

## Provenance — the bytes actually read and executed

`git show <freeze>:<path> | sha256sum` and `git hash-object <path>`:

| path | freeze sha256 |
|---|---|
| `tools/round-41/fetch-vendor.py` | `1cb0a34688488160bc693369dadf21152050cdd6e1654f7d1f6c168bc8ea0e04` |
| `tools/round-42/heldout-gen-v4.py` | `c2b1641ad6beec0d8eead002520174fb596c574efe44220c4a440917be03a5e1` |
| `tools/round-45/c1-counter.py` | `2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509` |
| `tools/round-46/registry.py` | `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449` |
| `tools/round-46/census.json` | `573ec008fc3f9173da04589c013484485758e9cf1c901a254bf1d6286d62133e` |
| `plans/round-46-claims.md` | `a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01` |

`git hash-object` of the worktree copies of `tools/round-41/fetch-vendor.py`,
`tools/round-42/heldout-gen-v4.py`, `tools/round-45/c1-counter.py`,
`tools/round-42/fixtures.json` and `tools/round-39/gen-squashfs.py` equals the
`git rev-parse <freeze>:<path>` blob id for each (`git diff --stat <freeze> -- tools/round-41
tools/round-42 tools/round-45 tools/round-39/gen-squashfs.py` is empty), so every command
below ran the frozen bytes. `tools/round-46/census.json` lists 38 paths and contains all
three of this seat's paths.

## Command receipts

Environment for every run: `TMPDIR=$S HYAKU_SCRATCH=$S`, cwd `$S`, `python3 -I -B`.
`L` = the lane root. Raw stdout/stderr are in `receipts/`; the machine-readable form of the
16-case battery is `receipts/receipts.json` (sha256
`256175f0ebe4d6e4cd9a784127ca7ed6c2332ceab43c1e80dff646f697716246`).

| # | command | exit | stdout sha256 | stdout bytes | UTC (start) |
|---|---|---|---|---|---|
| 1 | `python3 -I -B $L/tools/round-41/fetch-vendor.py --selftest` | 0 | `828a9add44cff9e88dc7751bd290d981ba040eff20bb25a09666d9dad34804ec` | 1027 | 2026-10-28T16:55:05Z |
| 2 | `python3 -I -B $L/tools/round-41/fetch-vendor.py` | 2 | `e3b0c442…b855` (empty) | 0 | 2026-10-28T16:55:05Z |
| 3 | `python3 -I -B $L/tools/round-41/fetch-vendor.py --cache $S/fv/cache2` | 2 | empty | 0 | 2026-10-28T16:55:05Z |
| 4 | `python3 -I -B $L/tools/round-41/fetch-vendor.py --spec $S/fv/bad.json --cache $S/fv/cache3b` | 1 | `c5c66795163a36ad8ba9d8c6696f892213b7d58064694ba8a8c15ab398ed6181` | 302 | 2026-10-28T16:55:05Z |
| 5 | `python3 -I -B $L/tools/round-41/fetch-vendor.py --spec $S/fv/broken.json --cache $S/fv/cache4b` | 1 | empty | 0 | 2026-10-28T16:55:05Z |
| 6 | `python3 -I -B $L/tools/round-41/fetch-vendor.py --spec $S/fv/nope.json --cache $S/fv/cache5b` | 1 | empty | 0 | 2026-10-28T16:55:05Z |
| 7 | `python3 -I -B $L/tools/round-41/fetch-vendor.py --help` | 0 | `892d731f42879dd65ee19c6bffa2ce3a30df8e13809bd67419a62e5dff988729` | 378 | 2026-10-28T16:55:05Z |
| 8 | `python3 -I -B $L/tools/round-45/c1-counter.py --selftest` | 0 | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` | 650 | 2026-10-28T16:55:05Z |
| 9 | `python3 -I -B $L/tools/round-45/c1-counter.py` | 2 | `ceadf6938045a1df52a6ff56ffc4797e7a6788eec4c5b40b3c0dc79b5764bf9b` | 118 | 2026-10-28T16:55:06Z |
| 10 | `python3 -I -B $L/tools/round-45/c1-counter.py --root $L --freeze <FREEZE> --rev 000…0` | 2 | `260f72034176c55d342d21ef4e92066d7b5f006e7c7edcf9ddfd048f8d4b7b9a` | 94 | 2026-10-28T16:55:06Z |
| 11 | `python3 -I -B $L/tools/round-45/c1-counter.py --root $L --freeze <FREEZE> --rev <FREEZE> --json-out $S/c1/at-freeze.json` | 0 | `fab5652fe8eef3aaefe0578b59a9ad105fe843de5e243b27d65bf2b6a77febb6` | 495 | 2026-10-28T16:55:06Z |
| 12 | `python3 -I -B $L/tools/round-42/heldout-gen-v4.py --seed <FREEZE> --selftest --scratch $S/hg/work` | 0 | `906b9e6f2fb135290a9b2633bc55913036250ca905a27fb1ebb4ab1d39298432` | 49369 | 2026-10-28T16:55:07Z |
| 13 | `python3 -I -B $L/tools/round-42/heldout-gen-v4.py --selftest` | 2 | empty | 0 | 2026-10-28T16:55:08Z |
| 14 | `python3 -I -B $L/tools/round-42/heldout-gen-v4.py --seed zz --selftest` | 1 | empty | 0 | 2026-10-28T16:55:08Z |
| 15 | `python3 -I -B $L/tools/round-42/heldout-gen-v4.py --seed <FREEZE> --out $S/hg/out-h3b --classes nope` | 1 | empty | 0 | 2026-10-28T16:55:08Z |
| 16 | `python3 -I -B $S/check_rows.py $L/.ufo/waves/round-46/w1/R46W1RegF/rows.md` | 0 (process; scored runs inside) | `c7beba1b03bf9116dfb41be8e04813514ef99379c592439a036109eb582ae73f` | 1173 | 2026-10-28T16:55:08Z |
| 17 | `python3 -I -B $S/legacy_probe.py $S $L` (scores the existing `tools/round-45/c1-counter.py` SKILL.md row verbatim) | 0 (process; `registry.score` returned 1) | `7fc4db51d7b5b5e63f96651e13ccb17a11d4e7cbe4e32bdba51eb3d116121c80` | 354 | 2026-10-28T16:55:53Z |

`e3b0c442…b855` is sha256 of empty output. Rows 1, 8, 12 were also run once before this
battery (individual shell calls, 2026-10-28T16:5xZ) and produced the identical stdout
sha256, so the selftests are reproducible across runs.

## What each selftest actually printed

- #1 `SELFTEST cases=16 pass=16 fail=0`; 15 chain cases plus
  `nested-writes-carved-bytes`. (`receipts/fv-selftest.out`)
- #8 `C1_SELFTEST: cases=9 failures=0`; green, relabelled-block, thin-table,
  bad-citation, no-S140, interpreter-fails, bad-exit-cell, frozen-touched→2,
  unknown-rev→2. (`receipts/c1-selftest.out`)
- #11 `rule_blocks 22`, `block22_present 1`, `block22_rows 10`, `met_target true`,
  `failing []`, exit 0 — the round-45 predicate still scores at the round-46 freeze.
- #12 `all 17 selftest checks passed` (`receipts/hg-selftest.out`).

## Rows validated by the frozen C2 scorer's own code path (#16)

`check_rows.py` parses `rows.md`, builds a `<!-- instrument-registry v2 -->` section with the
exact house header and only these three rows, and feeds it to `registry.score(..., "r46",
"v2", ...)` from the frozen `tools/round-46/registry.py`, with a synthetic census holding
exactly the three parsed cell-1 paths.

| case | scorer exit | unregistered | thin | absent_at_rev |
|---|---|---|---|---|
| as written | 0 | `[]` | `[]` | `[]` |
| mutant: cell 3 replaced with `0 rows, 1 column, 2 bytes` | 1 | `[]` | `["tools/round-41/fetch-vendor.py"]` | `[]` |
| mutant: cell 1 rewritten to `see <path> (wrapper)` | 1 | `["tools/round-41/fetch-vendor.py"]` | `[]` | `[]` |
| mutant: row for `tools/round-45/c1-counter.py` deleted | 1 | `["tools/round-45/c1-counter.py"]` | `[]` | `[]` |

Per-row structural facts printed by the same run: 7 cells, `stray_backticks 0` outside cell 1,
cell 1 exactly `` `path` ``, cell 3 keys exactly `{0,1,2}`, header equals `registry.HOUSE`.

## Installs

None. Only `python3` (stdlib), `git` read commands and `sha256sum` were used; no package
was installed through any channel.

## Cleanup

`/fast/scratch/hyaku/kaidoku-r46/R46W1RegF` is removed by the seat after `receipts/` and the
two markdown files were written. Nothing was written under `/tmp`, to `SKILL.md`, to
`plans/`, to `tools/`, or to any sibling lane.
