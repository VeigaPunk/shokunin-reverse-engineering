# Round 86 — CriticClaims report (critic, read-only)

Full per-clause table, fixtures and residuals: `.ufo/waves/round-86/w1/CriticClaims/critique.md`. Receipts: `.ufo/waves/round-86/w1/CriticClaims/receipts/` (`base-rerun/`, `fixtures/`, recipe `fixtures/recipe-fx.py`). No production edit, no commit.

## Verdicts

| claim | verdict | receipts that decide it |
|---|---|---|
| R86-C1 (calibration, 3 record atoms) | **falsified** (measurement) | `c1-a2-survivor`, `c1-a2-surviving` (A2 green on non-status words); `c1-a3-history-removed-r85` (A3 green on a 40-zero rev after 22 history rows deleted); `c1-a3-round-rewrite-0` (A3 green, round cell rewritten 85→0); `c1-a1-s079-rewrite` (A1 green on a rewritten registry) |
| R86-C2 (operability, 5 gate atoms) | **falsified** (measurement) | `c2-worktree-green` (rev-stamped green from a committed tool that exits 2; G2/G3 run the working tree); `c2-foreign-cmd`, `c2-gate-registry-cmd` (G3 green on a command that is not the registered tool); `c2-dup-malformed` (G1 green with two rows); `c2-map-substring` (G2 green on `10=`) |

## What survives

- Do-nothing controls reproduce at BASE exactly (C1 `0/3`, C2 `0/5`, exit 1); both cheap-rule controls accept BASE as declared.
- Causal separability holds in both directions (`sep-*` fixtures: C1 unchanged across the C2-only commit; C2 unchanged across the C1-edit commit).
- Honest reachability: A1 (`c1-a1-genuine`), A2 (`c1-a2-survived`) and the whole of C2 (`c2-genuine`, 5/5) reach green with honest edits.
- Instrument freeze: pinned sha256s match HEAD; no post-declaration change to counters, plan or claims.

## Blocking findings

- **C1 A3 is not honestly reachable under the frozen rule.** The `| coverage |` selector matches 23 rows; the target needs 22 historical rows deleted or renamed and a new `round-85` `l1/scores` receipt. The plan's stated BASE cause for A3 ("names only a round-67 receipt") is false: the row names rounds 84/76/75/68/67.
- **C2 measures the working tree at `--rev`.** G2/G3 run `cwd=root`, so a receipt stamped with a rev can be green on bytes that rev does not contain.
- **Frontier:** the S255 row is inherited (`fetched 2026-11-01`, round is 2026-11-04); its "never from a mutable worktree" teaches is not in the snapshot; the round-86 lesson and its quote format do not exist yet.

## Other observations

- Lane working tree has `M SKILL.md` (one inserted line) on the production path during the wave; not written by this seat; for the L1.
- Three `pre/*-at-declaration.json` files added after declaration; additive, not referenced by `claims.json`.
- Tools installed: none. Lane git commands were read-only; fixture commits were in scratch only, each asserted to its own toplevel.
