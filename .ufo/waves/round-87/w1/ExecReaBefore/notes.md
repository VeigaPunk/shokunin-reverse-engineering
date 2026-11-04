# ExecReaBefore — R87-C1 before/after REA evidence

Seat: ExecReaBefore (executor, leaf). Round 87, kaidoku. No production edits; no commits.
Pins observed: upx 5.2.0 sha256 cf2f6e7c…a8c969; rea-agents package.json sha256 a500302319c1…3050a6c (matches);
repair tools/round-87/upx-magic-repair.py sha256 f4ebd152495dc832180fff3d1ca3447937a7dad121ba63d57872003ffcc49723 (matches the committed candidate). All 4 carrier sha256 pins matched.

## Commands (verbatim)
Driver: `before_driver.py` in this dir (receipt). Run:

```
S=/fast/scratch/hyaku/kaidoku-r87/ExecReaBefore; W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-87/w1/ExecReaBefore; mkdir -p "$S" && cd "$S" && TMPDIR=$S/tmp HOME=$S/home python3 -I -B $W/before_driver.py "$S" "$W/before.json"
```
(rc 0, wall 428.6 s, scratch peak 6.2 MB.) Per carrier the driver runs:
- `cp -p <source> orig`; `/usr/bin/upx --best -q -o packed orig`
- T1-zero / T2-foreign = `packed.replace(b"UPX!", b"\0\0\0\0" | b"KDK!")` (identical to counter `tamper()`), mode copied from packed
- on orig/packed/T1/T2: `node /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs analyze --format json <file>` (env HOME=$S/home TMPDIR=$S/tmp LANG=C)
- on packed/T1/T2: `upx -t <f>`, `upx -l <f>`, `upx -d -q -o <f>.unpacked <f>`
- runtime (30 s timeout): `jq --version`, `xxd -v`, `docker-init --version` on orig/packed/T1/T2
- after: `python3 -I -B tools/round-87/upx-magic-repair.py --in <T> --out <T>.repaired --json`, then upx -t/-l/-d on the repaired file, REA analyze of the `upx -d` output, and the repaired binary's runtime.
Extra spot check: `rea.mjs analyze --format json jq/packed` and `jq/T1-zero` grepped for `upx` (case-insensitive): 0 mentions each.

## Before (tampered = what the runtime and REA see)
| carrier | magic words (offsets) | REA procs/segs/strings packed = T1 = T2 | orig REA | upx -t/-l/-d on T1,T2 | runtime T1,T2 |
|---|---|---|---|---|---|
| jq | 4 (556, 10971, 13992, 14000) | 3/3/3 | 167/30/190 | rc 2 NotPackedException (all three) | rc 0 `jq-1.8.2` |
| xxd | 4 (556, 16499, 19513, 19524) | 3/3/6 | 99/29/103 | rc 2 NotPackedException | rc 0 `tinyxxd 1.3.17` (stderr) |
| libz | 3 (9284, 63721, 65544) | 98/6/136 | 184/29/199 | rc 2 NotPackedException | n/a (shared lib) |
| dinit | 3 (556, 357738, 357748) | 3/3/5 | 1268/29/1111 | rc 2 NotPackedException | rc 0 `tini version 0.19.0 - git.de40ad0` |

Intact packed: upx -t rc 0 "Tested 1 file.", upx -l rc 0, upx -d rc 0 restoring the pin, for all 4.

- Tampering is runtime-invisible: all 6 tampered executables (3 carriers × T1/T2) run and print the same version as orig (rc 0).
- Tampering is packer-tool-fatal: upx -t, -l and -d all exit 2 `NotPackedException: not packed by UPX` on all 8 tampered files.
- REA is tamper-blind and packer-blind: REA counts for packed, T1 and T2 are identical per carrier; it reports the stub only (executables: 3 procedures) and no packer signal (normalized_result keys: document, image_base, procedure_count, segment_count, segments, string_count; no "upx" string anywhere in the envelope). evidence_id differs per file (content-addressed).
- Calibration caveat for "REA sees only the stub": true for jq/xxd/dinit (3 procs). For libz the packed shared object still shows 98 of 184 procedures (UPX keeps part of the .so uncompressed), so REA on the tampered libz sees a partial program, not just a stub.

## After (repair candidate f4ebd152…)
All 8 cases: repair rc 0, `upx -t` rc 0, `upx -d` sha256 == carrier pin (identity true), REA analyze of the restored bytes = declared original procedure count (jq 167, xxd 99, libz 184, dinit 1268; segment/string counts also equal orig: 30/190, 29/103, 29/199, 29/1111). Repaired jq/xxd/dinit run with rc 0 and the original version string. 8/8 on every arm this seat exercised (the counter itself was not run here).

Repair `--json` reports 3 anchors per carrier (l_info, b_info_end, packheader) and restores exactly those 3 windows.

## Findings
1. jq and xxd carry a 4th `UPX!` word (jq @10971, xxd @16499) that the repair does NOT restore: bytes there are `81 fa 55 50 58 21` = x86 `cmp edx, 'UPX!'` immediate, inside loader bytes before the payload. Consequence: repaired jq/xxd are NOT byte-identical to the intact packed file (`repaired_equals_packed: false`), while libz/dinit are (`true`). It does not affect the R87-C1 score: windows_only only constrains bytes that changed, and upx -t / -d / runtime all pass with that word left tampered. [INFERENCE] upx -t / -d check neither that loader word nor the bytes holding it, and the runtime path that executes that `cmp` does not change the outcome for these runs. Reported as a finding about what "recovered" means, not a defect in the frozen claim.
2. The before-state REA signal cannot tell intact from tampered (identical counts), so REA alone gives no tamper detection; the repair is what lifts REA from 3→declared counts (jq/xxd/dinit) and 98→184 (libz).

## Tooling
No installs or upgrades.

## Cleanup
Scratch /fast/scratch/hyaku/kaidoku-r87/ExecReaBefore removed before DONE. No packed/tampered binaries kept; sha256 of every state is in before.json.
