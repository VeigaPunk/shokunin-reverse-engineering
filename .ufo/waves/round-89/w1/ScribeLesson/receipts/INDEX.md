# ScribeLesson — receipt index (round 89)

All receipts in this directory were produced by seat `ScribeLesson` on 2026-11-04 against the
**frozen** round-89 instruments. The lane's own working tree was not modified by any of them;
the two probe scripts are copies under the seat directory and the frozen originals are untouched
(their sha256s still equal the pins in `.ufo/waves/round-89/claims.json`).

| file | what it measures | headline |
|---|---|---|
| `d3-r88-counter-at-r89-base.json` | the **superseded** round-88 depth counter at the round-89 base | `blocks 28, met_target true, exit 0` — the D3 defect, re-measured |
| `c2-v2-at-r89-base.json` | the round-89 v2 counter at the same base, target 29 | `blocks 28, met_target false, exit 1` — the D3 fix |
| `c2-v2-at-8bbb40cc.json` | the round-89 v2 counter at the block-29 landing commit | `blocks 29, resolved 29, met_target true, exit 0` |
| `cheat-r88-sibling-v2-under-r88-battery.json` | round 88's own `sibling-repair-v2.py` cheat under the **round-88** battery | `recovered 4 of 4, met_target true, exit 0`, all controls true — the D4 red arm |
| `cheat-r88-sibling-v2-under-r89-battery.json` | the **same** cheat under the **round-89** battery | `recovered 0 of 4, met_target false, exit 1` — the D4 fix |
| `cheat-sibling-under-r89-battery.json` | this seat's own sibling-copy cheat under the round-89 battery (`--no-rea`) | `recovered 0 of 4, exit 1` |
| `cheat-carrier-read-under-r89-battery.json` | ReviewerC1's `cheat-carrier-read.py`, re-run **verbatim** by this seat under the round-89 battery | `recovered 4 of 4, met_target true, exit 0` — the isolation control's blind spot (M89-9) |
| `u-len-preference-probe.json` | the frozen repair with `u_len` forced to 1 on a scratch copy (`probe-ulen.py`) | exit 0, `fits_u_len = false`, `uncompressed_accounted = 30800`, output == the intact packed carrier — the `u_len` bound is a rank key, not a filter (M89-10) |

## Scripts

- `cheat-sibling.py` — this seat's sibling-copy cheat (copies the `packed` sibling of `--in`).
- `cheat-carrier-read2.py` — this seat's carrier-read variant (re-packs a carrier source instead
  of deriving the field); it did **not** score the target (`recovered 1 of 4`), which is why the
  M89-9 row cites ReviewerC1's script, re-run verbatim.
- `probe-ulen.py` — a copy of the frozen repair with `ph["u_len"] = 1` forced in `derive()`, so
  that no candidate can satisfy the accounting bound. The frozen file was not edited.

## Reproduce

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r89/ScribeLesson; mkdir -p $S/w89 $S/w88
python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 0ec2bb40… --expect-blocks 29
python3 -I -B tools/round-88/depth-blocks.py   --root . --rev 0ec2bb40…
python3 -I -B tools/round-88/upx-chain-battery.py --root . \
  --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair-v2.py \
  --upx /usr/bin/upx --pkg <rea-agents 6.5.0 dir> --work $S/w88 --json-out $S/a.json
python3 -I -B tools/round-89/upx-field-battery.py --root . \
  --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair-v2.py \
  --upx /usr/bin/upx --pkg <rea-agents 6.5.0 dir> --work $S/w89 --json-out $S/b.json \
  --expect-recovered 4
```
