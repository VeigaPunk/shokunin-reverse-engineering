# ScribeQuality — round 91 QUALITY row drafts

Draft: `.ufo/waves/round-91/w1/ScribeQuality/rows-draft.md` — rows 178, 179, 180, 181.
`corpus/QUALITY.md` not edited (`git status --short -- corpus/QUALITY.md` empty).

Base: QUALITY.md at 2135f6e1d3f69a259b32cc5167c52ccb1a261c24 ends at Row 177; declaration commit deb2765a55fef0e4e81500a027dfe59951b69e87 carries the same 177 rows.

## Rows drafted

| Row | Criterion | Evidence |
|---|---|---|
| 178 | boundary class is a typed refusal with no output file unless the packer's verdict is green | `.ufo/waves/round-91/pre/c1-base-round90-repair.json`: `refused 0 of 8; unsafe 2; intact 4 of 4`, six silent + two unsafe, all rc 0 |
| 179 | geometry-only intact/tamper separation fails when the tamper leaves the walked total unchanged | `.ufo/waves/round-91/pre/probes/probe-cls-output.json`: walked total = intact total on 6 cells (all +7, plus xxd/dinit -7), exactly the six silent cells |
| 180 | block-count predicate paired with a shape clause for every block at/after the boundary; prose control killed | `tools/round-91/depth-blocks-v3.py --prose-proof`, `.ufo/waves/round-91/pre/c2-prose-proof.json` (`control_killed: true`); base `.ufo/waves/round-91/pre/c2-depth-at-base.json` (`blocks 30`) |
| 181 | calibration record row names only receipts that exist at the row's revision and agree with it | `tools/round-91/record-cells.py`, `.ufo/waves/round-91/pre/c3-at-base.json` (`mismatches 5`, `met: false`) |

## Path check (declaration commit deb2765a55fef0e4e81500a027dfe59951b69e87)

Command: `for p in <paths>; do git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e deb2765a55fef0e4e81500a027dfe59951b69e87:$p && echo OK $p || echo MISSING $p; done`

Result: all ten cited paths OK (exit 0 each):
- `tools/round-90/upx-break-repair.py`
- `tools/round-91/stop-boundary-battery.py`
- `tools/round-91/depth-blocks-v3.py`
- `tools/round-91/record-cells.py`
- `.ufo/waves/round-91/pre/c1-base-round90-repair.json`
- `.ufo/waves/round-91/pre/probes/probe-cls-output.json`
- `.ufo/waves/round-91/pre/probes/probe-cls.py`
- `.ufo/waves/round-91/pre/c2-prose-proof.json`
- `.ufo/waves/round-91/pre/c2-depth-at-base.json`
- `.ufo/waves/round-91/pre/c3-at-base.json`

Draft structure check: `grep -o "^- \*\*Row 1[78][0-9]" rows-draft.md` → Rows 178, 179, 180, 181 (4 rows).

## Verification notes

- Row 178: c1 receipt counts `silent 6, unsafe 2, refused 0, intact 4`; every cell `rc 0`; unsafe cells carry `outside_window` bytes at jq 10094–10097 and libz 60124–60127.
- Row 179: probe `cls.total` vs `u_len` — jq +7 30800 (=intact), xxd ±7 38928 (=intact for both), libz +7 98592 (=intact), dinit ±7 851288 (=intact for both); jq -7 22585 and libz -7 87421 differ. Silent set in c1 receipt (jq+7, xxd-7, xxd+7, libz+7, dinit-7, dinit+7) equals the unchanged-total set exactly.
- Row 180: `c2-prose-proof.json` prose `v2_accepts true, v3_accepts false` (`table:rows:0<3`, `table:cells:0<4`); table `v3_accepts true`.
- Row 181: c3 detail — R89-C1 A2+A3 fail; R89-C2 A3 fail; R90-C1 A2+A3 fail; R90-C2 all pass; total mismatches 5.

## Scope and limits

- Drafting only. No counters were re-run; figures are read from the frozen receipts and the probe output above. Row 178's "candidate rule" sentence states the frozen design, not an observed `upx -t` verdict on those cells.
- No installs or tool changes. No pacman. No edits outside the seat directory and this report.
- Scratch dir `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r91/ScribeQuality` created and removed before yield.
