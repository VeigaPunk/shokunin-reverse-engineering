# ExecReproC1 — independent reproduction of R98-C1 (round 98, attempt 1)

Date: 2026-11-05. Rev under test: L = 72346895a35a74af18151b125934fa0c09fe1e3c.
Scratch S=/fast/scratch/hyaku/kaidoku-r98/ExecReproC1 (removed at end of session).
Host: /usr/bin/upx 5.2.0 (preflight-matching), python 3.14.8, 406G free on /fast.
No tools installed/upgraded; no pacman, no sysctl, no writes outside S and the w1 paths.

## 1. Setup (verified)
- `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone` exit 0.
- `git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c` exit 0;
  `rev-parse HEAD` = 72346895a35a74af18151b125934fa0c09fe1e3c.
- `rev-parse --show-toplevel` = $S/clone before any write.
- sha256(clone:tools/round-98/pe-upx-tamper-battery.py at L)
  = a34d1253e75e98d4fbb66abe139d2c374a8332f8b6ca1bc8e4afea8dbf4feee8, byte-identical to the
  `counter_sha256` recorded in both frozen pre receipts (freeze integrity holds across B→L for
  this counter).

## 2. Frozen C1 command (candidate) — PASS
- Command (cwd=$S/clone): `python3 -I -B tools/round-98/pe-upx-tamper-battery.py
  --repair-cmd tools/round-98/upx-pe-repair.py --work $S/c1 --json-out $S/c1.json
  --rev 72346895a35a74af18151b125934fa0c09fe1e3c`
- Exit 0; label: `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18`
  (`met: true`) — exact match with the frozen R98-C1 predicate.
- Receipt receipt sha256 (candidate repair at L): 2fa1102d320acd8016a05721763c9d57f15a6b92894a67821187d8c825a1dfa4.

## 3. Controls at L vs pre receipts at B — PASS (both)
| arm | my exit | my label | pre label | label/exit match | repair_sha256 vs pre |
|---|---|---|---|---|---|
| tools/round-98/controls/identity-copy.py | 1 | `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18` | same | yes/yes (1) | equal: d8b7d4de6588d394d7d172d1ed5b5a0c7577b7f89efeea812321c692e177626e |
| tools/round-87/upx-magic-repair.py | 1 | `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18` | same | yes/yes (1) | equal: 96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24 |
(1) The only receipt field differing from pre is `rev` (mine 72346895a…, pre d0aebc28) — expected:
controls were frozen at B, I re-ran them at L. All other fields (label, exit, counter_sha256,
repair_sha256, upx, tool) identical. Both controls remain do-nothing-calibrated at L.

## 4. Hand-derived oracle cells (own tamper code) — 3/3 PASS
Written from the claim text, not the battery: T1 zero the first `UPX!` word; T2 rename the first
three `UPX*` section headers positionally to `.text`/`.data`/`.rdata`; T3 both. Oracle:
sha256(`upx -d` of repaired) == sha256(`upx -d` of the untampered pack), `upx -t` gates at each
step. Carriers pin-verified before use.

| cell | carrier (pin ok) | tamper | `upx -t` tampered | repair rc | `upx -t` repaired | unpack sha == ref | verdict |
|---|---|---|---|---|---|---|---|
| t32 | distlib t32.exe | magic | non-zero (refused) | 0 | 0 | yes | recovered |
| w64 | distlib w64.exe | names | non-zero (refused) | 0 | 0 | yes | recovered |
| winhello | WinHelloCPP.exe | both | non-zero (refused) | 0 | 0 | yes | recovered |

Reference sanity: in all three cells `upx -d` of the untampered pack also reproduced the
original carrier byte-for-byte (`ref_equals_carrier: true` in hand-cells.json).

## 5. Findings
1. R98-C1 frozen predicate reproduces exactly at L: candidate label + exit 0 (Sec 2).
2. Identity-copy control reproduces the B calibration at L, byte-identical repair script
   (sha match), expected label `0/18 recovered, 6/6 intact` (Sec 3).
3. Held r87 ELF-only repair reproduces the B calibration at L: 0/18 recovered, 0/6 intact,
   2/2 refused (Sec 3).
4. Independent hand oracle (3 cells, own tamper code, repair CLI driven directly) confirms the
   battery's oracle semantics: tamper is real (upx refuses), repair restores, unpack sha
   equality holds (Sec 4).
5. No defects found; no calibration drift between B (pre receipts) and L (this run) for either
   control; counter file unchanged (sha equality, Sec 1).

## 6. Receipts (this dir)
- commands.txt — every cited command line with exit codes.
- c1.json / c1-identity.json / c1-r87.json — battery JSON receipts (sha256:
  e9c26074…, 0d83f794…, c9186898…).
- hand-cells.json + hand_cell.py — hand-derived cells and the tamper implementation
  (sha256: 8116dda2…, 7df0e9fd…).

## 7. Risks / notes
- Reproduction is single-host and single-rev (L); carriers are host-absolute paths
  (distlib, Ghidra class files, pnpm fastlist) — battery preflight pins them by sha256 and all
  six pins matched here.
- Controls were re-run at L, not B, per seat item; rev-field delta documented above.
- Scratch S removed after receipt copy (trap-delete equivalent executed manually).
