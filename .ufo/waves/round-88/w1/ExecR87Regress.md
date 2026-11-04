# ExecR87Regress — R88-C1 independent no-harm evidence (round 88, wave r88-w1)

Seat: executor, leaf. Lane HEAD `a14f0a426`. Full report with commands, tables and receipts:
`.ufo/waves/round-88/w1/ExecR87Regress/report.md`. Receipts in `.ufo/waves/round-88/w1/ExecR87Regress/`.

Pins re-verified: `upx 5.2.0` `cf2f6e7c…aa8c969`, rea-agents `package.json` `a5003023…050a6c`,
repair `59ee51b0…a0b46`, r88 counter `a01ed622…37160`, r87 counter `0f2d2bd8…4b0`, r87 module
`96da7d8e…bec24`, carriers jq/xxd/libz/dinit all as pinned. No install, no pacman, no git/jj write.

## What I ran and what it measured

1. `python3 -I -B tools/round-87/upx-tamper-battery.py --root <lane> --repair-cmd <lane>/tools/round-88/upx-chain-repair.py --pkg <rea pkg> --work <scratch> --json-out …/r87-with-r88-repair.json --evidence-dir …/rea-r87-with-r88-repair`
   → **recovered 8 of 8**, controls all true, met, **exit 0**, wall 139.87 s; REA counts 167/99/184/1268 = `DECLARED_ORIG`.
2. `tools/round-88/upx-chain-battery.py … --no-rea` → recovered **0 of 4** (target 4), controls true, regression 8/8 met, **exit 1**, wall **90.01 s**; same command with REA → recovered **4 of 4**, controls true, regression 8/8 met, **exit 0**, wall **154.95 s**. Agreement on non-REA arms: **0 disagreements** (16/16 arms, all hashes, all block0 offsets); only `recovered` differs. The REA receipt is identical, case for case, to `pre/c1-candidate-at-declaration.json`.
3. Selftests: r87 counter **8 cases / 0 failures**, r88 counter **6 / 0**, repair **11 / 0**; all exit 0.
4. Repair on the four plain originals: **rc 2, no output** on each; non-ELF (MZ stub, random bytes) **rc 2** `refused: not a little-endian ELF`; directory **rc 2** `--in is not a regular file`. All refuse as required.
5. Extra, independent of the counter: derived `sz_cpr` equals ground truth on **4/4** carriers (252/249/201/226), repaired output equals the untampered packed bytes, `upx -t` on the zeroed file says `CantUnpackException: b_info corrupted` (rc 1); the round-87 repair alone refuses with `p_info is not followed by a plausible b_info` (rc 2).
6. Extra: candidate space re-enumerated — jq/xxd/libz have **1** structural candidate each; dinit has **3** (one over-claiming 123,942,159 > `u_len` 851,288, then 851,288 vs 850,696) and the declared tiebreak picks the true one. `strace` over `--no-rea`: **8** `node rea.mjs analyze` execs, all in the regression arm; the repair opens only `--in`, `--out` and the round-87 module.

## Findings (qualify, do not contradict, the claim)

- **F1** R88-C1's predicate reproduces exactly: 4 of 4, controls true, regression 8 of 8, exit 0; and the frozen round-87 counter is 8 of 8 with the new repair. No recovery used a byte outside the `sz_cpr` window.
- **F2** On a plain original the refusal message repeats one clause: `…no validated PackHeader in the tail window; no validated PackHeader in the tail window` — `repair()` concatenates the anchor refusal with a geometry refusal that fails at the same `find_packheader`. Behaviour correct, message misleading.
- **F3** `--no-rea` is not transitive: the embedded round-87 regression arm still forwards `--pkg` without `--no-rea`, so 8 REA calls run (measured) and `--no-rea` can never report `met_target`. It is a partial-instrumentation mode, not a REA-free one.
- **F4** The `fits_u_len`/largest-accounted tiebreak is exercised by 1 of 4 carriers (dinit); the other three are single-candidate recoveries. Limit of the evidence, consistent with named limit 1.
- **F5** libz accounts 98,592 of `u_len` 108,560 and is accepted on its single candidate — named limit 1 confirmed verbatim.
- **F6** The repair exits 0 on the `N2-corrupt-payload` files (no integrity check); the control holds only through `upx -t`/`-d`.
- **F7** REA `analyze` ≈ 5.3–5.6 s per call and forks java + the Ghidra decompiler; explains 154.95 s vs 90.01 s.
- **F8** `claims.json` supersedes the C2 matrix instrument with a v2; no C1 pin is affected (all four C1-relevant hashes match).

## Risks / blockers

None blocking. Risk carried to the reviewers: F3 (a reader may treat `--no-rea` as REA-free) and F4
(the rule's discriminating power rests on one carrier). No mutation, no commit, no spawn, no
`agent://all`; scratch deleted after receipts were copied out.

Lane revision note: HEAD was `a14f0a426` at run start and advanced to `1a72fdef4` during the seat;
all four C1-relevant instrument hashes re-checked unchanged and `tools/` clean, so the numbers above
hold at the current revision.
