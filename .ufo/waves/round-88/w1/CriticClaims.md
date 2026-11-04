# CriticClaims — round 88, kaidoku (critic seat)

Scope: falsify R88-C1 and R88-C2 as claims (cheapest cheat, axis fit, causal separability, sizing
rules). No lane file, instrument, claim or wave artifact was edited; the seat wrote only its own
report, critique, receipts and cheat scripts. No tool install or upgrade was needed (nothing was
installed; host pins re-hashed and equal).

## (a) What I ran

All commands from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless noted; scratch under
`/fast/scratch/hyaku/kaidoku-r88/CriticClaims/` (deleted after the receipts were copied here).

1. Base counter (C2), the counter's own success flag at the do-nothing state:
   `python3 tools/round-88/depth-blocks.py --root . --rev 0cf8e3243059e0bc510b90c880d13d191e78d732 --json-out <scratch>/c2-base-rev.json`
   → `{"blocks": 27, "met_target": true, "resolved": 27, "unresolved": []}`, **rc 0**.
2. C2 cheat, a one-line citation-only block inserted inside `## Queue-drain craft` in a scratch copy
   of `SKILL.md` + `corpus/`:
   `python3 tools/round-88/depth-blocks.py --root <scratch>/cheat-c2 --worktree --json-out <scratch>/cheat-c2-oneline-block.json`
   → `{"blocks": 28, "met_target": true, "resolved": 28, "unresolved": []}`, **rc 0**.
3. C1 candidate cross-check (independent tamper + repair, own population):
   pack each pinned carrier `upx --best`, zero block0 `sz_cpr`, run
   `python3 tools/round-88/upx-chain-repair.py --in <tampered> --out <out> --json`
   → derived 252 / 249 / 201 / 226, bytes equal to the packed file in all four; dinit candidates
   `136` (accounted 123,942,159 > u_len 851,288), `226` (851,288), `440` (850,696) → winner 226;
   libz single candidate 201, accounted 98,592 of 108,560.
4. C1 cheat 1 (packer oracle, no geometry):
   `python3 tools/round-88/upx-chain-battery.py --root . --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/oracle-repair-v2.py --upx /usr/bin/upx --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <scratch> --json-out <scratch>/cheat-c1-oracle-v2.json`
   → `recovered 4 of 4`, `controls_ok` all true, regression 8/8, **exit 0**.
5. C1 cheat 2 (copy the counter's own `packed` sibling, window-restricted):
   same battery with `--repair-cmd …/cheats/sibling-repair-v2.py`
   → `recovered 4 of 4`, `controls_ok` all true, regression 8/8, **exit 0**.
   Crude sibling copy (any ≤4 differing bytes) is caught by N2 (`4 of 4`, N2 false).
6. Instrument selftests: `upx-chain-repair.py` 11 cases, `upx-chain-battery.py` 6,
   `field-tamper-matrix.py` 11, `depth-blocks.py` 7 — all 0 failures; `sha256sum` of the four
   instruments equals the `claims.json` pins.
7. Read-only record checks: `git log/diff/status` for the pre receipts, freeze commit, plan edits,
   measured receipts; `git cat-file -e a14f0a42:<receipt>` for the C2 block's citations.

## (b) Measured numbers

| measurement | value |
|---|---|
| C2 base counter (rev `0cf8e324`) | blocks 27, resolved 27, `met_target true`, exit 0 |
| C2 citation-only cheat | blocks 28, resolved 28, `met_target true`, exit 0 |
| C2 matrix receipt (`c2-matrix-at-declaration.json`) | 68 cells, 63 effective, 0 unclassified; 9 non-zero classes (header 35, b_info 8, corrupt b_info 4, p_info 4, compressed 4, bad-method 4, bad-seek 1, tolerated 3, noop 5) |
| C1 measured receipt (`c1-at-a14f0a42.json`) | recovered 4/4, controls true, regression 8/8, exit 0, repair sha `59ee51b0…` |
| C1 independent derivation | 252 / 249 / 201 / 226; accounted 30,800 / 38,928 / 98,592 / 851,288; byte-equal to packed 4/4 |
| dinit structural candidates | 136 (impossible, 123,942,159 > u_len), 226 (winner, 851,288), 440 (850,696) |
| C1 oracle cheat | recovered 4/4, controls true, regression 8/8, exit 0 (252 `upx -t` probes for jq, 0.54 s) |
| C1 sibling cheat (window-restricted) | recovered 4/4, controls true, regression 8/8, exit 0 (no `upx` probes) |
| pre receipts / freeze commits | pre controls `7fbe16d45` 19:58:56; freeze `70d6f7dec` 19:59:02 |

## (c) Findings that contradict the claim or the plan

1. **R88-C2's predicate is not implemented by its counter.** `depth-blocks.py` sets
   `met_target = not unresolved`; it has no `28`. At base it exits 0 with 27 blocks, and the
   pre-freeze control receipt `c2-depth-at-base.json` records `met_target: true`. The kill rule
   `resolved < 28` is prose only. The claim's label is reachable by a one-line citation-only block
   (scored, exit 0). Verdict: **falsified as a frozen predicate**; the nine-row table itself is real
   and axis-fitting.
2. **R88-C2's declared separability is contradicted by the landed block.** The plan says the block
   cites the r87 file (present at base) "so R88-C2 is verifiable without R88-C1 having landed", but
   block 28 also cites `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`, absent at base and
   committed with C1's entry at `a14f0a42`.
3. **R88-C1's frozen label is mechanism-blind.** Two non-geometry repairs score the exact label with
   all controls true: a `upx -t`/`upx -d` oracle (M88-4 already discloses this) and a copy of the
   counter's own `packed`/`n3.out`/`chain.repaired` sibling restricted to the `sz_cpr` window (not in
   M88-4, not caught by the kill rule). The plan's premise that M87-3 "defines what this round must
   not repeat" is repeated on the new class. Verdict: **weakened** — the artifact and its numbers
   hold.
4. **The battery's work-dir layout leaks the answer.** `run_root/<carrier>/` holds `packed`,
   `n3.out`, `chain.repaired` next to `chain.tampered`, the repair's `--in`; the repair can list the
   directory. Only the N2 control stops the careless copy; the window-restricted copy passes N2.
5. **The plan's C1 sentence is stale on dinit.** "The smallest offset above `block0 + 12` … yields
   `sz_cpr`" would write 136; the artifact and M88-3 write 226 by the accounting bound. The plan's
   own rule paragraph is the operative one.
6. **The frozen plan was edited after the freeze.** Worktree `M plans/round-88-claims.md` changes
   the C2 sentence from v1/7-label to v2/10-label; the container predicate is unchanged and the edit
   is disclosed as M88-6, but the plan is no longer byte-frozen.
7. **`PROVINCE.md` promotes C1 to Core as "verified" citing the declaration-time receipt**
   (`pre/c1-candidate-at-declaration.json`), not the measured `c1-at-a14f0a42.json`.
8. **The C2 block's non-knowledge citations are unenforced.** The matrix receipt path and
   `corpus/QUALITY.md` rows 154–155 are ignored by the counter's regex; only
   `corpus/knowledge/*.md[:line]` is checked.
9. **The counter does not pin the repair bytes in its met condition.** Both cheats have different
   repair shas and both score `met=True`; the predicate names the path and the container pins the
   sha, but the battery certifies any `--repair-cmd`.

## (d) Files written

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims.md` (this report)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/critique.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/c2-base-rev.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c2-oneline-block.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/c1-candidate-crosscheck.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-oracle-v2.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-oracle.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-sibling-v2.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-sibling.json`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/cheats/oracle-repair-v2.py` (sha256 `b8225a1c…`)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/cheats/oracle-repair.py` (sha256 `53bd4abd…`)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair-v2.py` (sha256 `ce58a6c4…`)
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair.py` (sha256 `dd623fb2…`)

Nothing outside the seat dir was written; no commit was made (the L1 commits the seat output).
