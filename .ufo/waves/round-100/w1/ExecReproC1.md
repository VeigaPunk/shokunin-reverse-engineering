# ExecReproC1 — independent reproduction of R100-C1 (UPX 5.2.0 PE payload-corruption refusal)

Seat: ExecReproC1 (executor) · 2026-11-05 · lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin
Revs used: A1 = a610671d7a01e1d762eb7103e6ee9f8a2be287ed; F = 8e24c29a37ca81a0bd1ff5ec73c96a949885322e;
lane tip recorded at run start = cbd224ef9b9d2271f415d823bdc4d1e70a0d281c (= A2 at that time; `tip=` line in logs/runs.log).
Scratch S=/fast/scratch/hyaku/kaidoku-r100/ExecReproC1 (402 GiB free at start; deleted after artifact copy).
Clone: `git clone --shared <lane> $S/clone`; `git rev-parse --show-toplevel` verified == $S/clone before every run (driver asserts it). No mutating git anywhere but the scratch clone.

## 1. Frozen battery runs (command per contract, run from the clone checkout)

Driver `run-battery.sh` (copied to artifacts): for each row,
`cd $S/clone && TMPDIR=$S/tmp python3 -I -B tools/round-100/pe-upx-corrupt-battery.py --root $S/clone --repair <repair> --rev <rev> --work $S/work-<name> --json-out $S/receipts/<name>.json`
(battery reads candidate bytes via `git -C root show rev:repair`, never the tree; every candidate invocation under `strace -f -qq -e trace=execve,execveat`).

| run | rev | repair | rc | label tail differing from TARGET |
|---|---|---|---|---|
| a1 | A1 | tools/round-100/upx-pe-repair.py | 0 | none — exact TARGET, `met True` |
| tip | cbd224ef (tip) | tools/round-100/upx-pe-repair.py | 0 | none — exact TARGET, `met True` |
| r99 | F | tools/round-99/upx-pe-repair.py | 1 | `corrupt 0 of 40` (rest full) |
| h4 | F | tools/round-100/forgeries/h4-oracle-alias.py | 1 | `corrupt 20 of 40; exec 0 of 1` |
| h6 | F | tools/round-100/forgeries/h6-exec-only.py | 1 | `exec 0 of 1` (rest full) |

Comparison vs frozen evidence — all five agree, zero deviations:
- a1 receipt vs L1 receipt `.ufo/waves/round-100/l1/scores/c1-at-a610671d….json`: counts identical (30/9/10/20/40/40/2/3/1/1/119), `counter_sha256` identical (`8f148d33…83183`), `repair_sha256` identical (`15ada0b0…9a37`), `met: true`, `exit: 0`, exec leg 154 invocations 0 violations.
- r99/h4/h6 labels are byte-identical to the corresponding lines of `.ufo/waves/round-100/pre/c1-controls-at-freeze.txt`, including rc 1 each (h0–h3/h5 not re-run; my assignment scoped r99 + h4/h6).
- Pre-checks: battery blob identical at F/A1/tip (`git rev-parse <rev>:tools/round-100/pe-upx-corrupt-battery.py` = `b24c2251…3390` ×3); candidate blob identical A1 vs tip (`88ff04e3…fcbd`); `upx 5.2.0`, `strace 7.2` (preflight passed inside every run).

## 2. Own probe (NOT the battery) — per-carrier Adler identity + 5 self-chosen flips

Script `adler_probe.py` (copied to artifacts; stdlib only). Per pinned carrier (the battery's ten CARRIERS, sha256 pins re-verified, all True):
pack `upx --best -q -f`; locate `UPX!` (all ten: offset 992 = UPX1 rawdataptr − 64; data start cstart = 1024);
read c_adler @ hdr+12, c_len @ hdr+20; check `zlib.adler32(pb[cstart:cstart+c_len], 1) & 0xffffffff == c_adler`;
flip 5 bytes at MY offsets in [cstart, cstart+c_len): first byte (rel 0), last byte (rel c_len−1), middle (rel c_len//2), two `os.urandom`-drawn distinct offsets; xor value `1 + urandom % 255`;
record `upx -t -q` rc vs candidate (A1 bytes extracted via `git show A1:tools/round-100/upx-pe-repair.py`) rc/message/output-absence.
Agreement := upx -t fails AND candidate rc != 0 with `checksum` in output AND no `--out` written.

| carrier | adler_ok | flips agree | intact cand_rc / upx -t(out) |
|---|---|---|---|
| t32 | True | 5/5 | 0 / 0 |
| t64 | True | 5/5 | 0 / 0 |
| w32 | True | 5/5 | 0 / 0 |
| w64 | True | 5/5 | 0 / 0 |
| winhello | True | 5/5 | 0 / 0 |
| fastlist64 | True | 5/5 | 0 / 0 |
| freeglut32dll | True | 5/5 | 0 / 0 |
| gle64dll | True | 5/5 | 0 / 0 |
| llio32dll | True | 5/5 | 0 / 0 |
| sevenzip64dll | True | 5/5 | 0 / 0 |
| **total** | **10/10** | **50/50** | 10/10 accepted |

Sample (t32, c_len 35016): rel 0 xor 23 → upx -t rc 1, cand rc 2 `checksum` ✓; rel 35015 xor 209 → 1 / 2 ✓; rel 17508 xor 31 → 1 / 2 ✓; rel 8375 xor 63 → 1 / 2 ✓; rel 20533 xor 90 → 1 / 2 ✓. Full per-flip detail: artifacts/probe.json.

## 3. Source-rule spot check

`.ufo/waves/round-100/pre/s327-packhead-v5.2.0.cpp` lines 335–338: `upx_adler32(raw_bytes(in, ph.c_len), ph.c_len, ph.saved_c_adler)` compared to `ph.c_adler`, else `throwChecksumError()` — matches the frozen rule. LE PackHeader offsets confirmed in the same copy (u_adler @ +8, c_adler @ +12; battery `ph_fields` reads c_len @ +20, data at +32) — consistent with my probe's independent parsing.

## Findings

1. F1 (reproduction): R100-C1 reproduces independently — candidate at A1 and at lane tip cbd224ef both hit the exact TARGET label with exit 0; receipt metadata (counter/candidate sha256, all counts) identical to the L1 receipt. No deviation.
2. F2 (controls): round-99 repair (`corrupt 0 of 40`), h4-oracle-alias (`corrupt 20 of 40; exec 0 of 1`), h6-exec-only (`exec 0 of 1`) at F reproduce the freeze transcript byte-for-byte, all rc 1. The two frozen claims the battery discriminates (checksum refusal + process-level exec guard) are both load-bearing in my runs.
3. F3 (attack): no attack found — on all ten pinned carriers the Adler-32 identity holds, and 50/50 self-chosen corruptions (incl. first/last byte of the compressed blob) are refused by the candidate exactly when `upx -t` fails; intact packs pass on 10/10.

## Artifacts (this directory)

`receipts/{a1,tip,r99,h4,h6}.json` (sha256: a1 d90e4d44…, tip 53009aa3…, r99 79670383…, h4 3574236e…, h6 2086b98a…), `probe.json` 7716dc1a…, `adler_probe.py`, `run-battery.sh`, `candidate-at-A1.py`, `logs/{runs.log,a1,tip,r99,h4,h6}.log`.

Environment: no tools installed/upgraded (none needed); pacman untouched; no sysctls touched; /tmp unused (all scratch under /fast). Scratch deleted after artifact copy.
