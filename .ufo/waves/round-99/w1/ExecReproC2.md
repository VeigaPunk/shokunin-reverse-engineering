# ExecReproC2 — independent reproduction of R99-C2 (truncated UPX PE refusal)

Seat: ExecReproC2 (executor). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
Clone: /fast/scratch/hyaku/kaidoku-r99/ExecReproC2/clone, detached at L = 01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f
(`git -C <clone> rev-parse --show-toplevel` = clone path, verified). Bk = c19d57cd2e65a036478b9e78f6c5397dedfb2bcb read via `git show` (`--rev`), no checkout.
Scratch removed on exit. Receipts: `.ufo/waves/round-99/w1/ExecReproC2/` (copied from scratch; `byhand.py` is my harness).
No mutating git in the lane. No tool installs. No pacman. Labrat not used. C1 is not in this item.

## 1. Frozen C2 battery, exit and label

Command (absolute paths, `--work` in scratch, `--json-out` in wave dir):
`python3 -I -B <clone>/tools/round-99/pe-upx-trunc-battery.py --root <clone> --repair <path> --rev <rev> --work $S/w-<name> --json-out .../c2-<name>.json`

| run | rev | repair | exit | label (verbatim) | met |
|---|---|---|---|---|---|
| frozen C2 at L | L | tools/round-99/upx-pe-repair.py | 0 | recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79 | True |
| frozen C2 at Bk | Bk | tools/round-99/upx-pe-repair.py | 0 | same as L | True |

L and Bk: same label, same repair_sha256 `ac97598a94c04119…` (candidate file unchanged L→Bk), same counter_sha256 `d4ed44301f417ef6…`.

## 2. Controls at Bk vs frozen `pre/c2-*-at-freeze.json`

Exit codes in `c2-exits.txt`. All controls exit 1 as the freeze predicts. Each control's label, repair_sha256, counter_sha256 and the full 115-cell tuple list (arm, carrier, case, ok, candidate_rc) equal the freeze receipt.

| control | exit (mine / freeze) | label (mine) | label = freeze | cells = freeze |
|---|---|---|---|---|
| r98 repair (tools/round-98/upx-pe-repair.py) | 1 / 1 | recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 0 of 40; refused 2 of 2; cli 0 of 3; static 1 of 1; effective 79 of 79 | yes | yes |
| g4 fixed-992 | 1 / 1 | recovered 27 of 30; decoy 9 of 9; intact 9 of 10; overlay 18 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79 | yes | yes |
| g5 size-cache (FORGERY_CACHE built by build-size-cache.py, exit 0) | 1 / 1 | recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 10 of 20; truncated 40 of 40; refused 0 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79 | yes | yes |
| g6 lazy-anchor | 1 / 1 | recovered 30 of 30; decoy 0 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79 | yes | yes |

Disagreements with freeze: none. Note the repair_sha256 of each forgery at Bk equals the freeze value, so the forgery bytes are the frozen ones.

## 3. Own hand probe (`byhand.py`, my own PE parser and cut offsets, not the battery's)

Tool: L copy of tools/round-99/upx-pe-repair.py (repair_sha256 `ac97598a…`). Packer: `/usr/bin/upx --best -q -f` = upx 5.2.0.
Carriers (sha256 pins checked): t32.exe, w64.exe, freeglut32.vc14.dll. Sections in each pack: UPX0 (rsize 0), UPX1, .rsrc (last).
Cuts I chose (not the battery's `aligned_end-1` nor `UPX1 rptr+rsize//2`):
- UPX1 rptr+3 (byte 1027 in t32/w64/freeglut32 → 1027 in all three, UPX1 starts at 1024)
- UPX1 rptr + 3/4 rsize
- last section (.rsrc) rptr + rsize/2
Extra boundary cells: aligned end of last section (should pass) and aligned end − 1 (should fail).

18 cells (3 carriers × 6), each: `upx -t -q` rc and `upx-pe-repair.py --in --out --json` rc, output presence, reason.

| carrier | cut | file len | upx -t rc | tool rc | tool reason | out written | agree |
|---|---|---|---|---|---|---|---|
| t32 | UPX1+3 | 1027 | 1 | 2 | truncated: 1027 < 58880 | no | yes |
| t32 | UPX1 3/4 | 27904 | 1 | 2 | truncated | no | yes |
| t32 | .rsrc mid | 47872 | 1 | 2 | truncated | no | yes |
| t32 | aligned end | 58880 | 0 | 0 (intact) | — | yes, == input | yes |
| t32 | aligned end − 1 | 58879 | 1 | 2 | truncated | no | yes |
| w64 | UPX1+3 | 1027 | 1 | 2 | truncated: 1027 < 62976 | no | yes |
| w64 | UPX1 3/4 | 30976 | 1 | 2 | truncated | no | yes |
| w64 | .rsrc mid | 51968 | 1 | 2 | truncated | no | yes |
| w64 | aligned end | 62976 | 0 | 0 (intact) | — | yes, == input | yes |
| w64 | aligned end − 1 | 62975 | 1 | 2 | truncated | no | yes |
| freeglut32 | UPX1+3 | 1027 | 1 | 2 | truncated: 1027 < 80384 | no | yes |
| freeglut32 | UPX1 3/4 | 55168 | 1 | 2 | truncated | no | yes |
| freeglut32 | .rsrc mid | 76800 | 1 | 2 | truncated | no | yes |
| freeglut32 | aligned end | 80384 | 0 | 0 (intact) | — | yes, == input | yes |
| freeglut32 | aligned end − 1 | 80383 | 1 | 2 | truncated | no | yes |
| t32 / w64 / freeglut32 | uncut pack | 58880 / 62976 / 80384 | 0 | 0 (intact) | — | yes, == input | yes ×3 |

Command: `cd <scratch> && S=<scratch> CLONE=<clone> WAVE=<wave> python3 -I -B byhand.py > byhand.txt` → exit 0, "ALL AGREE".
Result: `upx -t` fails exactly where the tool returns rc 2 + `truncated`, and passes exactly where the tool returns rc 0 with an output byte-identical to the input (both directions, 18/18).

## 4. Disagreements and observations

- Rc-level disagreements: 0 (battery labels and exits; own probe 18/18 agreement).
- Message-level note (not a disagreement): for cuts inside the first ~1 KiB of UPX1 (1027 bytes), `upx -t` fails with `CantUnpackException: header corrupted`, not `OverlayException: invalid overlay size` (the packer's checkOverlay path, which is what the tool's arithmetic mirrors). The later cuts show `OverlayException`. The tool's label `truncated` is the aligned-end arithmetic, correct for all six cuts per carrier, but its word is not upx's diagnostic in the 1027-byte case. Relevant only if a reviewer wants the refusal reason tied to the packer's own message.
- The frozen C2 predicate's `effective 79 of 79` is confirmed for the battery; my probe did not reproduce the 79-count.
- Forgery controls behave exactly as the freeze says; none passes the target.

## 5. Installs

None. No pacman, no ~/.local/bin write, no sysctl.

## Verdict

R99-C2 reproduces independently: frozen predicate met at L and Bk (label, exit 0), all frozen controls reproduce label/exit/hashes/cells, and my own 3-carrier, 18-cell probe agrees with upx -t at every cut. findings: 0 disagreements.
