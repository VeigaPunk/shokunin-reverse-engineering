HOLDS — all 21 requested selftest invocations at measured source S returned exit 0.

**Observation.** Exported `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 | tar -x -C /var/tmp/rerunself.Z7eibS` (export directory created by `mktemp -d /var/tmp/rerunself.XXXXXX`). Executed source was from this export, not the working tree. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/verify.py | sha256sum` matched `sha256sum /var/tmp/rerunself.Z7eibS/.ufo/waves/round-20/verify.py` (`95ef0217c84847dbff31b6ddb2b78249cda722e3fb150b92f01e879ab0af455e`); the same `git show`/`sha256sum` comparison for `.ufo/gates/custody-pair/custody-pair.py` matched at `d81cf5c0eb9c027a3aaadeb0c0b3cc326b36d6e8556a678a4b95e03eee47c146` (comparison command exit 0). `verify.py:42-55` lists the ten required `tools/*.py`; `verify.py:271-280` schedules those plus `measure.py`, `controls-r20.py`, `verify.py`, and `run-carriers.sh`.

For the first table, exact invocation template was `python3 -I -B "$A/<path>" --selftest` with `A=/var/tmp/rerunself.Z7eibS`, cwd `$A`; `run-carriers.sh` used `bash "$A/.ufo/waves/round-20/run-carriers.sh" --selftest`. Each wrapper recorded `EXIT=0` after the shown final test line.

| Tool | Last test line | Exit | S source anchor |
|---|---|---:|---|
| `.ufo/waves/round-20/tools/carrier-guard.py` | `SELFTEST: CLEAN cases=4` | 0 | `.ufo/waves/round-20/tools/carrier-guard.py:625` |
| `.ufo/waves/round-20/tools/compare-first-failure.py` | `SELFTEST: CLEAN cases=6` | 0 | `.ufo/waves/round-20/tools/compare-first-failure.py:156` |
| `.ufo/waves/round-20/tools/evidence-timestamps.py` | `SELFTEST: CLEAN cases=4` | 0 | `.ufo/waves/round-20/tools/evidence-timestamps.py:418` |
| `.ufo/waves/round-20/tools/final-census.py` | `SELFTEST: CLEAN cases=3` | 0 | `.ufo/waves/round-20/tools/final-census.py:308` |
| `.ufo/waves/round-20/tools/first-failure-extract.py` | `SELFTEST: CLEAN cases=4` | 0 | `.ufo/waves/round-20/tools/first-failure-extract.py:292` |
| `.ufo/waves/round-20/tools/retro-v2.py` | `SELFTEST: CLEAN cases=5` | 0 | `.ufo/waves/round-20/tools/retro-v2.py:207` |
| `.ufo/waves/round-20/tools/revexec.py` | `SELFTEST: CLEAN cases=5` | 0 | `.ufo/waves/round-20/tools/revexec.py:341` |
| `.ufo/waves/round-20/tools/routed-r19.py` | `SELFTEST: CLEAN cases=4` | 0 | `.ufo/waves/round-20/tools/routed-r19.py:1114` |
| `.ufo/waves/round-20/tools/swiss-misread-v2.py` | `SELFTEST: CLEAN cases=17` | 0 | `.ufo/waves/round-20/tools/swiss-misread-v2.py:1860` |
| `.ufo/waves/round-20/tools/verb-coverage.py` | `SELFTEST: CLEAN cases=8` | 0 | `.ufo/waves/round-20/tools/verb-coverage.py:312` |
| `.ufo/waves/round-20/measure.py` | `SELFTEST: CLEAN cases=25` | 0 | `.ufo/waves/round-20/measure.py:652` |
| `.ufo/waves/round-20/controls-r20.py` | `SELFTEST: CLEAN cases=12` | 0 | `.ufo/waves/round-20/controls-r20.py:453` |
| `.ufo/waves/round-20/verify.py` | `SELFTEST: CLEAN cases=14` | 0 | `.ufo/waves/round-20/verify.py:565` |
| `.ufo/waves/round-20/run-carriers.sh` | `SELFTEST: CLEAN cases=20` | 0 | `.ufo/waves/round-20/run-carriers.sh:192` |

The requested in-place gate invocations were `python3 -I -B "$A/<path>" --selftest`, except custody-pair, which used `python3 -I -B "$A/.ufo/gates/custody-pair/custody-pair.py" selftest --scratch /var/tmp/custody-pair-r20.LRTKHS`. That directory was made by `mktemp -d /var/tmp/custody-pair-r20.XXXXXX`; a post-run directory read was empty.

| Gate | Last test line | Exit | S source anchor |
|---|---|---:|---|
| `.ufo/gates/custody-pair/custody-pair.py` | `SELFTEST: CLEAN cases=33` | 0 | `.ufo/gates/custody-pair/custody-pair.py:1255-1268,1526` |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `CITATION_DRIFT_SELFTEST: CLEAN cases=34 passed=34 failed=0 exit=0` | 0 | `.ufo/gates/citation-drift/citation-drift-probe.py:630,762` |
| `.ufo/waves/round-17/tools/receipt-validate.py` | `SELFTEST: CLEAN cases=28` | 0 | `.ufo/waves/round-17/tools/receipt-validate.py:811,1190` |
| `.ufo/waves/round-18/tools/head-rev-lint.py` | `SELFTEST: CLEAN cases=5` | 0 | `.ufo/waves/round-18/tools/head-rev-lint.py:1204,1335` |
| `.ufo/waves/round-19/tools/wave-outcomes.py` | `SELFTEST: CLEAN cases=34` | 0 | `.ufo/waves/round-19/tools/wave-outcomes.py:396,817` |
| `.ufo/waves/round-18/tools/jj-red-before.py` | `SELFTEST: CLEAN cases=11` | 0 | `.ufo/waves/round-18/tools/jj-red-before.py:1047,1191-1237` |
| `.ufo/gates/c1-census-v10.py` | `SELFTEST: CLEAN cases=3` | 0 | `.ufo/gates/c1-census-v10.py:664,719` |

**Inference.** No requested selftest falsified its fixture-level contract. The `measure.py` fixture also printed expected unresolvable-zero-revision diagnostics before its clean summary; process exit was 0. **Residual risk / verification gap:** these are selftest results, not independent end-to-end proof of live carrier, census, or corpus behavior; no Go toolchain binary or REA/Ghidra run was invoked.