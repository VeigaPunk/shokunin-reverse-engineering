# MutCounter — R91 mutation probe (seat report)

Seat: MutCounter, wave r91-w1, lane kaidoku-shokunin. Scratch clone, lane untouched.
Commit under test: `deb2765a55fef0e4e81500a027dfe59951b69e87` (frozen declaration; verified
`git rev-parse HEAD` after clone and again at final restore).

## Verdict table

| Mutant | Target file | Change | Frozen run label (exit) | Verdict |
|---|---|---|---|---|
| M1 | tools/round-91/stop-boundary-battery.py | unsafe scoring removed; every rc 0 output → silent | `refused 8 of 8; unsafe 0; intact 4 of 4` (exit 0) | **SURVIVED** |
| M2 | tools/round-91/stop-boundary-battery.py | intact arm always `same = True` | `refused 8 of 8; unsafe 0; intact 4 of 4` (exit 0) | **SURVIVED** |
| M3 | tools/round-91/stop-boundary-battery.py | `after = sorted(os.listdir(box))` moved before the child runs | `refused 8 of 8; unsafe 0; intact 4 of 4` (exit 0) | **SURVIVED** |
| M4 | tools/round-91/upx-stop-boundary-repair.py | `if upx_test(d):` → `if True:` | `refused 0 of 8; unsafe 0; intact 4 of 4` (exit 1) | **KILLED** |
| M5 | tools/round-91/upx-stop-boundary-repair.py | refusal branch writes input to `--out` before raising | `refused 0 of 8; unsafe 0; intact 4 of 4` (exit 1; cells `rc 2` + output → class `other`) | **KILLED** |
| M6 | tools/round-91/depth-blocks-v3.py | `table_shape` returns ok=True unconditionally | primary `blocks 31, resolved 31, required-shaped 1/1` (exit 0); `--prose-proof` `control_killed false` (exit 1) | **KILLED** (by the prose control) |
| M7 | tools/round-91/depth-blocks-v3.py | `--shape-from` default 31 → 32 | `blocks 31, resolved 31, required-shaped 0/0` (exit 1) | **KILLED** |

Score: 4 KILLED / 3 SURVIVED. Per the mutation-testing contract, the survivors are coverage
findings on the counters, not grounds to touch the claims.

## Baselines (pristine clone, all required before mutant verdicts count)

- Battery × candidate repair, `--expect 'refused 8 of 8; unsafe 0; intact 4 of 4'` → label exact, met True, exit 0 (1.03 s).
- Depth primary, `--rev deb2765…`, `--expect-blocks 31 --expect 'blocks 31, resolved 31, required-shaped 1/1'` → met=True, exit 0.
- Depth `--prose-proof` → `control_killed true`, exit 0.
- Regression `tools/round-90/upx-later-block-battery.py --repair-cmd tools/round-91/upx-stop-boundary-repair.py --expect 'P1 6 of 6; P2 4 of 4; P3 4 of 4'` → label exact, all 8 controls true (`N1, N2, N3, carrier_blind, cheat_repack, isolation, no_work, rea`), exit 0 (212 s). Notes: this counter resolves `--repair-cmd` against the process CWD, requires a pre-existing `--work` and `--rev`; REA arm passed via `--pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (the pinned `rea_package_dir`; its `package.json` sha256 matches the `rea_pkgjson_sha256` pin).
- Do-nothing control: battery × round-90 repair, `--expect 'refused 0 of 8; unsafe 2; intact 4 of 4'` → label exact (reproduces `pre/c1-base-round90-repair.json`), met False exit 1 as the before-state should.

## Survivor findings (one-line reasons)

- **M1 SURVIVED** — the frozen predicate is scored against a candidate that never emits an rc 0
  output, so the `unsafe` arm is dead code under the accepted run; the label and counts are
  identical with the arm deleted. Secondary detection exists: under M1 the do-nothing run labels
  `refused 0 of 8; unsafe 0; intact 4 of 4` (exit 1 vs the before receipt's `unsafe 2`), i.e. the
  before-receipt reproduction run would catch this mutant even though the frozen candidate run
  cannot (`mutant-M1-battery-round90repair.json`).
- **M2 SURVIVED** — the accepted candidate genuinely passes the intact arm 4 of 4, so forcing
  `identity true` is indistinguishable under the frozen run; the arm only discriminates repairs
  that corrupt intact inputs, and the frozen predicate never exercises such a repair.
- **M3 SURVIVED** — `box_after` is recorded in every cell and intact arm but never gated: under M3
  every receipt row shows `box_after ['in']` (including the 4 intact arms where the child wrote
  `out`), the QUALITY 170 evidence is silently corrupted, yet label/counts/exit are unchanged.
  Common root: the frozen predicate gates only label equality + the four counts; evidence arms
  (`box_after`) and arms that discriminate non-accepted repairs (`unsafe`, `intact` against a
  failing repair) have no gate in the scored run.

## Kill-path notes

- M4/M5: the regression arm stays green under both repair mutants (`P1 6 of 6; P2 4 of 4; P3 4 of 4`,
  all controls true, exit 0 — successors decide every P1–P3 cell, so the stop-boundary branch is
  unreached there). The kill comes solely from the R91-C1 class battery.
- M6: the primary depth run passes under M6 (block 31 is a genuine table), so the frozen
  `--prose-proof` control is the only detector — it fired (`control_killed false`, exit 1).
  The R91-C2 predicate is safe only while `--prose-proof` stays part of the scored command.
- M7: killed by the primary label alone (`required-shaped 0/0`); the canonical C2 command omits
  `--shape-from`, so the default is load-bearing.

## Hash evidence (mutated → restored; pins from claims.json)

| File | pin (pristine) | mutated under | restored |
|---|---|---|---|
| stop-boundary-battery.py | `5998b6bd…93ca9` | M1 `d1140d8b…eef1`, M2 `876b7546…bb3d0`, M3 `203c05cf…1c9937` | `5998b6bd878534d62ca867def69f9da21a3bd1a6139f51c7fba196dcc6893ca9` ✓ |
| upx-stop-boundary-repair.py | `473bb3a9…29b91` | M4 `f880adc1…72c1a7`, M5 `9bfcfb02…47aab` | `473bb3a937a60b0b785a6c814b0e25cacc67c97b85cc1cb9704985781d829b91` ✓ |
| depth-blocks-v3.py | `bcf6c4ea…eb052f` | M6 `a76c2107…7e60`, M7 `cd2002bc…1d990` | `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f` ✓ |

Final state: clone `git status --porcelain` = 0 entries; HEAD = `deb2765a55fef0e4e81500a027dfe59951b69e87`;
all three instruments `cmp`-byte-identical to the pristine snapshots taken before the first mutant.
Host pins verified before runs: `/usr/bin/upx` = `cf2f6e7c…8c969` (`upx 5.2.0`), all four carriers
match their CARRIERS pins. No tools installed or upgraded (nothing needed).

## Command lines (all runs used the scratch clone, `TMPDIR=$S/tmp`, `--work` under `$S/work`)

Battery (candidate): `python3 $S/clone/tools/round-91/stop-boundary-battery.py --root $S/clone
--repair-cmd tools/round-91/upx-stop-boundary-repair.py --work $S/work/<run> --rev deb2765a55fef0e4e81500a027dfe59951b69e87
--expect 'refused 8 of 8; unsafe 0; intact 4 of 4' --json-out <receipt>`
Battery (do-nothing): same with `--repair-cmd tools/round-90/upx-break-repair.py --expect 'refused 0 of 8; unsafe 2; intact 4 of 4'`
Regression (run from `$S/clone` cwd): `python3 tools/round-90/upx-later-block-battery.py --root . --rev deb2765a55fef0e4e81500a027dfe59951b69e87
--repair-cmd tools/round-91/upx-stop-boundary-repair.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
--work $S/work/<run> --expect 'P1 6 of 6; P2 4 of 4; P3 4 of 4' --json-out <receipt>`
Depth primary: `python3 $S/clone/tools/round-91/depth-blocks-v3.py --root $S/clone --rev deb2765a55fef0e4e81500a027dfe59951b69e87
--expect-blocks 31 --expect 'blocks 31, resolved 31, required-shaped 1/1' --json-out <receipt>`
Depth control: same counter with `--prose-proof --json-out <receipt>`
Exit codes are quoted per run in the transcript and reflected in the table above.

## Files written (all under the seat directory)

Receipts (JSON, one per run): `baseline-battery-candidate.json`, `baseline-depth-primary.json`,
`baseline-depth-proseproof.json`, `baseline-regression.json`, `baseline-battery-round90repair.json`,
`mutant-M1-battery-candidate.json`, `mutant-M1-battery-round90repair.json`,
`mutant-M2-battery-candidate.json`, `mutant-M3-battery-candidate.json`,
`mutant-M4-battery-candidate.json`, `mutant-M4-regression.json`, `mutant-M5-battery-candidate.json`,
`mutant-M5-regression.json`, `mutant-M6-depth-primary.json`, `mutant-M6-depth-proseproof.json`,
`mutant-M7-depth-primary.json`, `mutant-M7-depth-proseproof.json`; plus this `MutCounter.md`.
Scratch dir `/fast/scratch/hyaku/kaidoku-r91/MutCounter` deleted after this report.
