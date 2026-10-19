# EX-4 — c1 correctness sweep

All values below were re-derived in this run from immutable Git objects, current gate executions, or the r4 CarrierV bytes/evidence. No prior seat's reported number is used as proof. Current records HEAD is `71668cc`.

## Command A — REPRODUCED

Re-ran the recipe at `SCORECARD.md:88-124` against every listed work revision, including both commits in each paired round, and the records HEAD. Output (JSON from the recipe):

```text
{"citation_resolved_rules":13,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":82,"mapped":82,"missing":[],"revision":"fbbbd45","rule_blocks":13}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":82,"mapped":82,"missing":[],"revision":"28aa7a9","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":83,"mapped":83,"missing":[],"revision":"5be4a26","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":83,"mapped":83,"missing":[],"revision":"c418be0","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"revision":"40de383","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":83,"mapped":83,"missing":[],"revision":"520341d","rule_blocks":14}
{"citation_resolved_rules":14,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":84,"mapped":84,"missing":[],"revision":"71668cc","rule_blocks":14}
```

Every tested revision has `missing=[]`, `dangling=[]`, and coverage/depth 10.0/10.0. In particular, the final work tree `40de383` is 84/84 and 14/14; `520341d` is 83/83 and 14/14. These are separate immutable tree measurements, not a quoted round summary.

## Landed-tree gates and PROVINCE — REPRODUCED

- Census command: `python3 .ufo/gates/c1-census-v10.py --root .`
  - `live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`
  - `PROVINCE.md lines=162 loci=6`; `SCORECARD.md lines=1631 loci=9`; `SKILL.md lines=390 loci=2`.
  - `G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)`
  - `SCOPE-ERRORS (marker assertions): []`; `UNREADABLE (could-not-evaluate): []`; `DECLARED FAIL CLASSES: []`; `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`.
- Citation drift default: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- Citation drift strict: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- Custody-pair selftest: the supplied spelling `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` returns argparse usage/exit 2 (`custody-pair.py` requires a `{capture,verify,selftest,paths}` subcommand; see gate `:1308-1333`). Re-ran the intended test via `CUSTODY_PAIR_SCRATCH=/var/tmp/kaidoku-ex4-r5 python3 .ufo/gates/custody-pair/custody-pair.py selftest` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. Scratch was `/var/tmp/kaidoku-ex4-r5/custody-pair-selftest-3fltd32y`.
- `wc -l PROVINCE.md; sha256sum PROVINCE.md` → `162 PROVINCE.md`; `11a5c60450cc736a5b5443fa559191dc35b246386927cbd854b5e9fef1f0bcf2  PROVINCE.md`.
- Rechecked these nine old literals against current `PROVINCE.md`; each exact-literal search returned no match. The corrected live lines are shown in parentheses: `config.toml:3298` (:18); `35 features incl. PyGhidra/BSim` (:46); `1Password 423-file asar` (:49); old absent-tools list `absent: 7z, cabextract, xxd, radare2/rizin, strace/ltrace, upx, pacman-contrib` (:62); `Reserve: 91MB Godot ARM64 template` (:83); `all 3 organic cores exceed the cap` (:84-86); `real solc/vyper-compiled bytecode untested` (:91-93); `Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to` (:143-144; the surrounding phrase is no longer present); `still probe-refused since r2; multi-version pacman pairs beyond expac unexercised` (:157-160). Searches used the dedicated Grep tool with exact literal patterns (regex metacharacters escaped), rather than shell `grep`.

## CarrierV spot check — REPRODUCED

Re-derived against `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/` and the r4 entry (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:19-22`):

- `planted-K.json:23-40` has 15 planted selectors. Fresh set comparison against its three saved probe envelopes printed:

```text
planted_K=15 runtime_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.4.0-hex.json: functions=15 matched=15/15 missing=[] extra=[] bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 agrees=True
probe-6.4.0-raw.json: functions=15 matched=15/15 missing=[] extra=[] bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 agrees=True
probe-6.7.0-hex.json: functions=15 matched=15/15 missing=[] extra=[] bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 agrees=True
```

- Fresh `sha256sum`/`wc -c` on `out/runtime.bin` gave SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`, 1,562 bytes. This agrees with `out/compile-receipt.txt:14,18` and each decoded probe bytecode identity.
- Re-ran REA itself with `TMPDIR=/var/tmp/kaidoku-ex4-r5 npm_config_cache=/var/tmp/kaidoku-ex4-r5/npm-cache npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json`. Result: Evidence `ev_d1792f577ae3611615fd8dbcb1ce2e71dae4e0346b66d72b41321f4644df963f`, 15 function objects, all `dispatch:"abi"`, decoded bytes=1562 and bytecode SHA-256 equal to the raw runtime above.
- Re-ran the byte-level `dispatch-census.py` against `runtime.hex`, planted K, and the 6.4.0 hex envelope. Exact summaries: `runtime bytes: 1562`; `assumed jump table at 0x600 (13 buckets x 2 B) -> tail 26 B`; `execution reached the leg-derived body: 15/15`; `agreement: 15/15`; `probe set == leg-chain set: True`; no extras or omissions. A separate opcode-boundary parse of `runtime.bin` confirmed prefix `5f3560e01c6002600d820660011b61060001601e395f5156`, 13 table entries all beginning at JUMPDEST, and the `0x05e7` empty sentinel 3 times. Four buckets ([5, 6, 10, 12]) contain multiple selectors; thus the entry's four “collisions” reproduces as four collision-bearing buckets (five selector sites beyond one per occupied bucket). Opcode-boundary PUSH4 parsing found the 15 planted selectors plus six `08c379a0` immediates and no `69656e74` PUSH4; the latter is a PUSH32-payload substring, not a dispatcher selector.

**Disposition:** all six scoped checks REPRODUCED; no correction is indicated. The only invocation discrepancy is that the custody gate's actual CLI uses `selftest` as a subcommand, not `--selftest`.
