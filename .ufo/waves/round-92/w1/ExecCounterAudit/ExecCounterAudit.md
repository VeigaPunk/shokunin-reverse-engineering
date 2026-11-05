# ExecCounterAudit — round 92 reproduction of R92-C1 control and R92-C2 controls

Seat: ExecCounterAudit (executor). Lane: kaidoku. Clone: `11f8606178dfd9e72001b31daf412c5463106a63` (equals lane HEAD; clone `git status` clean). Scratch removed after copying receipts.

Environment: `upx 5.2.0` (`/usr/bin/upx`, UCL 1.03), `python3 -I -B`, `TMPDIR` and `--work` in scratch. No host state changed, no installs, no pacman, no sysctl, no subagents.

## 1. Reproduction table (`--root <clone>`, `--rev 11f8606178dfd9e72001b31daf412c5463106a63`)

Repro receipts: `repro-<name>.json` in this seat dir. Pre receipts: `.ufo/waves/round-92/pre/<name>.json`.

| name | reproduced label | pre label | label match | met repro / pre | exit (repro) |
|---|---|---|---|---|---|
| c1-control-do-nothing-round91-repair (counter `tools/round-92/stop-boundary-repair-battery.py`, repair `tools/round-91/upx-stop-boundary-repair.py`) | repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10 | same | yes | False / False | 1 |
| c2-positive-v2-round91 (v2, round-91 refusal tool) | refused 10 of 10; typed 10; unsafe 0; intact 5 of 5 | same | yes | True / True | 0 |
| c2-counterfeit-A-v2 (v2, `cheat_carrier_read.py`) | refused 10 of 10; typed 10; unsafe 0; intact 4 of 5 | same | yes | False / False | 1 |
| c2-counterfeit-B-v2 (v2, `cheat_hash_table.py`) | refused 10 of 10; typed 10; unsafe 0; intact 4 of 5 | same | yes | False / False | 1 |
| c2-counterfeit-C-v2 (v2, `cheat_typed_only.py`) | refused 10 of 10; typed 0; unsafe 0; intact 5 of 5 | same | yes | False / False | 1 |
| c2-do-nothing-v1-counterfeit-A (v1 `tools/round-91/stop-boundary-battery.py`, `cheat_carrier_read.py`) | refused 8 of 8; unsafe 0; intact 4 of 4 | same | yes | True / True | 0 |
| c2-do-nothing-v1-counterfeit-B (v1, `cheat_hash_table.py`) | refused 8 of 8; unsafe 0; intact 4 of 4 | same | yes | True / True | 0 |
| c2-do-nothing-v1-counterfeit-C (v1, `cheat_typed_only.py`) | refused 8 of 8; unsafe 0; intact 4 of 4 | same | yes | True / True | 0 |

All eight labels, met_target values and exit codes matched. For each repro receipt the `counter_sha256` and `repair_sha256` equal the pre receipt. For the five v2 names the `carriers` block (source and packed sha256, block counts) equals the pre receipt.

Commands (abbreviated; `C` = clone, `D` = seat dir, `S` = scratch):

- `python3 -I -B $C/tools/round-92/stop-boundary-battery-v2.py --root $C --repair-cmd tools/round-91/upx-stop-boundary-repair.py --work $S/work/c2-positive-v2-round91 --rev 11f8606… --expect "refused 10 of 10; typed 10; unsafe 0; intact 5 of 5" --json-out $D/repro-c2-positive-v2-round91.json` → rc 0
- same, with `--repair-cmd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-92/controls/cheat_{carrier_read,hash_table,typed_only}.py` → rc 1 each
- `python3 -I -B $C/tools/round-91/stop-boundary-battery.py --root $C --repair-cmd <cheat path> --expect "refused 8 of 8; unsafe 0; intact 4 of 4" --json-out $D/repro-c2-do-nothing-v1-counterfeit-<A|B|C>.json` → rc 0 each
- `python3 -I -B $C/tools/round-92/stop-boundary-repair-battery.py --root $C --repair-cmd tools/round-91/upx-stop-boundary-repair.py --work $S/work/c1-control-do-nothing-round91-repair --rev 11f8606… --expect "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10" --json-out $D/repro-c1-control-do-nothing-round91-repair.json` → rc 1, label `repaired 0 of 10 …`, met False, as pinned

The runner names its receipts after the cheat stem (`carrier_read`, `hash_table`, `typed_only`); these were renamed to the pre names (A, B, C) after the run. No receipt content was edited.

## 2. Pin check

Full digests, recomputed at the clone (`sha256sum`) and, where stated, at the lane working tree.

| file | recomputed sha256 | pin in `claims.json` | match |
|---|---|---|---|
| tools/round-92/stop-boundary-repair-battery.py (clone and lane) | 63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc | `counter_sha256` 63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc | yes |
| tools/round-92/stop-boundary-battery-v2.py (clone and lane) | f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874 | `imports_sha256` f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874 | yes |
| tools/round-91/upx-stop-boundary-repair.py (clone and lane) | 3779d35fc8f57bc9f573b87b5b4e566e159ac58737b3942be6b840f649e3f238 | `instruments_sha256` 3779d35fc8f57bc9f573b87b5b4e566e159ac58737b3942be6b840f649e3f238 | yes |
| tools/round-91/stop-boundary-battery.py (clone and lane) | 5998b6bd878534d62ca867def69f9da21a3bd1a6139f51c7fba196dcc6893ca9 | `instruments_sha256` 5998b6bd878534d62ca867def69f9da21a3bd1a6139f51c7fba196dcc6893ca9 | yes |
| .ufo/waves/round-92/controls/cheat_carrier_read.py (lane) | 018ae7caf27b6b4ae3f927d7eb999d4d76b040992c268231a57209b9729b34a3 | 018ae7caf27b6b4ae3f927d7eb999d4d76b040992c268231a57209b9729b34a3 | yes |
| .ufo/waves/round-92/controls/cheat_hash_table.py (lane) | 4abd318b9b1512865f29bbf6ba591c85bd3b10fe30137bd4e714f3fba47a11a5 | 4abd318b9b1512865f29bbf6ba591c85bd3b10fe30137bd4e714f3fba47a11a5 | yes |
| .ufo/waves/round-92/controls/cheat_typed_only.py (lane) | 7ef7f9e01b0e4f72becc5222fb4120138febc590d91d804056ce0ef7de1d1a7a | 7ef7f9e01b0e4f72becc5222fb4120138febc590d91d804056ce0ef7de1d1a7a | yes |

Mismatches: none. The lane round-92 counters are byte-identical to the clone copies. `git diff --stat 73a882712… 11f8606… -- tools/round-91` is empty.

Host carriers (source sha256 recomputed by `sha256sum`; compared to the receipt `source_sha256`):

| carrier | host sha256 | receipt sha256 | match |
|---|---|---|---|
| /usr/bin/jq | e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 | e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 | yes |
| /usr/bin/xxd | 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 | 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65 | yes |
| /usr/lib/libz.so.1.3.2 | 6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9 | 6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9 | yes |
| /usr/bin/docker-init (`dinit`) | 0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115 | 0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115 | yes |
| /usr/bin/xz (unseen) | 24c477492f40fd8b1b6eca2d6cc020e47d4c9c11ee1bfb9ba57fb8e2f6a11bda | 24c477492f40fd8b1b6eca2d6cc020e47d4c9c11ee1bfb9ba57fb8e2f6a11bda | yes |

The counters also run `carrier pin drift` and `packer sha256 drift` checks on every run; every v2 run passed them, so the host carriers and UPX match the pins at execution time.

## 3. CHEAT-B table recomputation

Fresh `upx --best -q` of the four pinned carriers on this host (upx 5.2.0), sha256 of the packed output:

| carrier | fresh packed sha256 | in `TABLE` (cheat_hash_table.py) |
|---|---|---|
| /usr/bin/jq | e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a | yes |
| /usr/bin/xxd | 1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff | yes |
| /usr/lib/libz.so.1.3.2 | a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b | yes |
| /usr/bin/docker-init | b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7 | yes |

The set of fresh digests equals the four-element `TABLE` set exactly (no extras, none missing). The unseen `/usr/bin/xz` packs to `a7b4d929441c01673bb336d69052bb362faa0a9d10504a30b691ce0fd43a889b`, which matches the receipt pin and is not in `TABLE`. That absence is the only reason CHEAT-B scores `intact 4 of 5`.

## 4. CHEAT-A and CHEAT-C versus round-91 CriticClaims

Diffed `.ufo/waves/round-91/w1/CriticClaims/evidence/cheats/{cheat_carrier_read,cheat_typed_only}.py` against the round-92 controls:

- CHEAT-A (`cheat_carrier_read.py`): logic identical (same four carriers, same `upx --best -q` pack, same `open(outp,"rb").read() == d` comparison, same `cand.upx_test` override). Differences: the round-91 wrapper loads the tool from a round-91 CriticClaims clone (`CLONE`); the round-92 wrapper loads `tools/round-91/upx-stop-boundary-repair.py` from the lane (`ROOT`). The docstring differs. Behaviour-neutral at this commit (tool sha identical).
- CHEAT-C (`cheat_typed_only.py`): logic identical (`sys.exit(1 if rc == 2 else rc)`). Same path difference (`CLONE` → `ROOT`). Docstring differs.
- CHEAT-B: the round-91 CriticClaims hash-table file was not diffed in this item; its table was checked against fresh packs in section 3.

## 5. Attack results (ways pins and receipts can agree while the counter is wrong)

1. **The v2 calibration label admits five-entry counterfeits.** Two scratch probes, scored with the frozen v2 counter at 11f8606 and the frozen expect:
   - `probes/cheat_hash_table_plus_xz.py`: CHEAT-B with the xz packed sha256 `a7b4d929441c01673bb336d69052bb362faa0a9d10504a30b691ce0fd43a889b` added to `TABLE` → `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5`, met True, rc 0 (`attack-probe-table-plus-xz-v2.json`).
   - `probes/cheat_carrier_read_plus_xz.py`: CHEAT-A with `/usr/bin/xz` appended to `CARRIERS` → same label, met True, rc 0 (`attack-probe-carrier-read-plus-xz-v2.json`).
   The three declared counterfeits are refused as the claim states. The two extended ones are not, because the counter's five-carrier list is exactly the list a counterfeit needs. The claim's declared limits name "an unseen-carrier table" as out of scope, so this is not a contradiction of the frozen claim. It does mean the R92-C2 verdict covers the three named counterfeits, not the calibration class. Route to L1 for the knowledge entry.
2. **Receipts and reproduction share code and host.** Counter and tool bytes are identical at base 73a88 and declaration 11f86 (repair sha 3779… in both). Agreement shows determinism on this host, not correctness. UPX is the only independent oracle, and it is the same oracle the counter uses.
3. **Attribution gap in receipts.** Each receipt records `repair_sha256` as the sha of the `--repair-cmd` file. For the cheat wrappers that is the wrapper (018ae7…, 4abd…, 7ef7…), not the round-91 tool the wrapper imports; the imported tool's bytes are not recorded. The wrappers hard-code the lane's `tools/round-91` path (`ROOT`), not `--root`, so a lane edit would change what the CHEATs test without the receipt showing it. Current content matches (sha equal), so no effect now.
4. **Untracked pre receipt.** Lane `git status` at 11f86 reports `?? .ufo/waves/round-92/pre/regress-base-round91-repair.json`. The declaration commit does not pin its bytes. It is outside this item's comparison; flagged.
5. **Intact arm is weak.** The v2 intact check is `rc == 0 and output == packed`; it never calls the packer on the output. A candidate that echoes its input passes intact by construction. The repair arm of the C1 counter does discriminate (output must differ only in the window and be green), so this is a limit of the calibration counter, not of R92-C1.
6. The C1 do-nothing control and the C2 positive control score as frozen. The C1 candidate repair tool is not measured in this seat.

## 6. Verdict for this item

- Reproduction: 8 of 8 receipts reproduce label, met_target and exit exactly. Pins: no mismatch. CHEAT-B table: exact set equality with fresh packs. CHEAT-A and CHEAT-C: logic identical to round-91; only the path differs.
- The R92-C2 count (0 of 3 named counterfeits admitted) reproduces. The frozen label does not exclude a counterfeit that carries all five pinned carrier packs or packs all five carriers at run time; this sits inside the claim's declared limits but must be stated in the knowledge entry.

## Receipts written (seat dir `.ufo/waves/round-92/w1/ExecCounterAudit/`)

- `repro-c1-control-do-nothing-round91-repair.json`
- `repro-c2-positive-v2-round91.json`
- `repro-c2-counterfeit-A-v2.json`, `repro-c2-counterfeit-B-v2.json`, `repro-c2-counterfeit-C-v2.json`
- `repro-c2-do-nothing-v1-counterfeit-A.json`, `repro-c2-do-nothing-v1-counterfeit-B.json`, `repro-c2-do-nothing-v1-counterfeit-C.json`
- `attack-probe-table-plus-xz-v2.json`, `attack-probe-carrier-read-plus-xz-v2.json`
- `probes/cheat_hash_table_plus_xz.py`, `probes/cheat_carrier_read_plus_xz.py` (scratch attack wrappers; not lane tools)
- `ExecCounterAudit.md` (this file); copy at `.ufo/waves/round-92/w1/ExecCounterAudit.md`

Installs/updates: none. Host changes: none. Subagents dispatched: none.

Checks for the main agent: none required from this seat; the reproduction above is this seat's measured evidence, and verification remains with main.
