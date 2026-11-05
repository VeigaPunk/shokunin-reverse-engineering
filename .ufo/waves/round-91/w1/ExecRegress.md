# ExecRegress — R91-C1 regression arm at declaration commit

Revision: `deb2765a55fef0e4e81500a027dfe59951b69e87` (requested and recorded as measured).

## Command (run once, exit 0)

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r91/ExecRegress" && mkdir -p "$S/tmp" "$S/work" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ExecRegress" && TMPDIR="$S/tmp" python3 -I -B tools/round-90/upx-later-block-battery.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev deb2765a55fef0e4e81500a027dfe59951b69e87 --repair-cmd tools/round-91/upx-stop-boundary-repair.py --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work "$S/work" --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ExecRegress/receipt.json; echo "exit=$?"
```

- Printed label: `P1 6 of 6; P2 4 of 4; P3 4 of 4`
- Exit code: `exit=0` (battery `exit` field 0)
- Receipt: `.ufo/waves/round-91/w1/ExecRegress/receipt.json`
- Matches `--expect`: yes. `met_target`: true. `recovered`: P1 6, P2 4, P3 4.

## controls_ok (every key and value)

| control | value |
|---|---|
| N1-refuse-plain | true |
| N2-corrupt-payload | true |
| N3-intact-idempotent | true |
| carrier_blind | true |
| cheat_repack | true |
| isolation | true |
| no_work | true |
| rea | true |

All eight controls true.

## Instrument sha256 vs claims.json `instruments`

| file | computed sha256 | pinned sha256 | match |
|---|---|---|---|
| `tools/round-91/upx-stop-boundary-repair.py` | `473bb3a937a60b0b785a6c814b0e25cacc67c97b85cc1cb9704985781d829b91` | `473bb3a937a60b0b785a6c814b0e25cacc67c97b85cc1cb9704985781d829b91` | EXACT |
| `tools/round-90/upx-later-block-battery.py` | `5462ef134c680e4f811c59da5e8f17ff84159ed5a55bdd5e1fe5ad7226de3210` | `5462ef134c680e4f811c59da5e8f17ff84159ed5a55bdd5e1fe5ad7226de3210` | EXACT |

Also checked against receipt pins: `upx_sha256` `cf2f6e7c…c969` (upx 5.2.0) and `rea_pkg` path match `claims.json` pins. Receipt `pins.modules` sha256 values for round-87/88/89/90 helpers are recorded in the receipt; I did not separately hash them, and `rea_pkgjson_sha256` was not recomputed here (the receipt's `rea` control is true).

## Notes

- Shell commands were run from the fleet root with absolute paths; the battery ran from the lane root with `--root` set to the lane.
- No tool was edited. No git mutation was performed in the lane.
- The receipt's `work_root` points to a scratch directory under `/fast/scratch/hyaku/kaidoku-r91/ExecRegress/work/`. That scratch is deleted before yield, so the receipt's `work_root` path will not resolve after this seat ends.
- Tool install/update: none.

## Verdict for the regression arm

Regression arm of R91-C1 passes at `deb2765a55fef0e4e81500a027dfe59951b69e87`: label equals the frozen `--expect`, exit 0, all controls true, instrument hashes exact. The coverage arm (`stop-boundary-battery.py`, `refused 8 of 8; unsafe 0; intact 4 of 4`) was not part of this item and is not scored here.
