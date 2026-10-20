# VerifyR20

## Axes and change

- **Calibration:** fixed B at `14f0260ad319ecc26994381b2415d5a999003375`; strict routed counts expect 1 at B and 0 at SOURCE, matching the claims contract (`.ufo/waves/round-20/contract.md:4`; `claims.json:17-18`).
- **Coverage:** the pass plans both-revision verb coverage, both-revision measure, controls, SOURCE timestamp checking, final census, and selftests for every source `tools/*.py` plus the assigned required tools. Per-command argv, expected/actual exit and stdout/stderr SHA-256 are retained in `verification.json`, with output files under `verify/` (`gen-wave1.py:285-292`; Python runner pattern `.ufo/waves/round-19/verify.py:192-236`).
- **Depth:** the final-census receipt is checked against SOURCE and its retained stdout digest; evidence/selftest scratch is not placed in the lane. The contract requires external `tempfile.mkdtemp()` scratch and the final census receipt shape (`contract.md:23-34,:55`; `gen-wave1.py:161-167`).

**Observation:** Created `/tmp/kr20-VerifyR20-2/.ufo/waves/round-20/verify.py`; observed clone base was `14f0260ad319ecc26994381b2415d5a999003375`. Patch: `.ufo/waves/round-20/w1/patches/VerifyR20-2.patch` (stat: `1 file changed, 582 insertions(+)`). No other clone file was staged. No install/update was needed.

**Observation:** The selftest passed exactly once. Exact final line: `SELFTEST: CLEAN cases=14`; exit 0. The dry-run used SOURCE=B and returned exit 0. Its table reports `source_present=false` for every new W20 source path; therefore it planned but did not execute the full counting pass or write `verification.json`. No integrated SOURCE revision was available in the B clone. The parent must run the full pass after integration; the verifier refuses to count absent/mismatched source tools as successful.

## Dry-run command table

`CLONE=/tmp/kr20-VerifyR20-2`; `B=SOURCE=14f0260ad319ecc26994381b2415d5a999003375`. These are planned commands, not executed commands; the last column is the recorded expected exit.

| Label | Planned argv | Expected |
|---|---|---:|
| selftest-verify | `python3 -I -B $CLONE/.ufo/waves/round-20/verify.py --selftest` | 0 |
| selftest-carrier-guard | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/carrier-guard.py --selftest` | 0 |
| selftest-compare-first-failure | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/compare-first-failure.py --selftest` | 0 |
| selftest-evidence-timestamps | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/evidence-timestamps.py --selftest` | 0 |
| selftest-final-census | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/final-census.py --selftest` | 0 |
| selftest-first-failure-extract | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/first-failure-extract.py --selftest` | 0 |
| selftest-retro-v2 | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/retro-v2.py --selftest` | 0 |
| selftest-revexec | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/revexec.py --selftest` | 0 |
| selftest-routed-r19 | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/routed-r19.py --selftest` | 0 |
| selftest-swiss-misread-v2 | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/swiss-misread-v2.py --selftest` | 0 |
| selftest-verb-coverage | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/verb-coverage.py --selftest` | 0 |
| selftest-measure | `python3 -I -B $CLONE/.ufo/waves/round-20/measure.py --selftest` | 0 |
| selftest-controls-r20 | `python3 -I -B $CLONE/.ufo/waves/round-20/controls-r20.py --selftest` | 0 |
| selftest-run-carriers | `bash $CLONE/.ufo/waves/round-20/run-carriers.sh --selftest` | 0 |
| routed-r19-baseline-strict | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/routed-r19.py --root $CLONE --rev $B --strict` | 1 |
| routed-r19-source-strict | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/routed-r19.py --root $CLONE --rev $B --strict` | 0 |
| verb-coverage-baseline | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/verb-coverage.py --root $CLONE --rev $B` | 0 |
| verb-coverage-source | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/verb-coverage.py --root $CLONE --rev $B` | 0 |
| measure-baseline | `python3 -I -B $CLONE/.ufo/waves/round-20/measure.py $B` | 0 |
| measure-source | `python3 -I -B $CLONE/.ufo/waves/round-20/measure.py $B` | 0 |
| controls-r20 | `python3 -I -B $CLONE/.ufo/waves/round-20/controls-r20.py $B $B` | 0 |
| evidence-timestamps-source | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/evidence-timestamps.py --root $CLONE --rev $B --path .ufo/waves/round-20 --strict` | 0 |
| final-census-tool | `python3 -I -B $CLONE/.ufo/waves/round-20/tools/final-census.py --root $CLONE --out-dir $CLONE/.ufo/waves/round-20/verify` | 0 |

## Commands run (each exit shown)

```text
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-VerifyR20-2 && git -C /tmp/kr20-VerifyR20-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-VerifyR20-2 rev-parse HEAD
-> 14f0260ad319ecc26994381b2415d5a999003375; exit 0

python3 -I -B .ufo/waves/round-20/verify.py --selftest
-> SELFTEST: CLEAN cases=14; exit 0

python3 -I -B .ufo/waves/round-20/verify.py --dry-run 14f0260ad319ecc26994381b2415d5a999003375
-> command table above; exit 0

git -C /tmp/kr20-VerifyR20-2 add --all -- .ufo/waves/round-20/verify.py && mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-VerifyR20-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/VerifyR20-2.patch && git -C /tmp/kr20-VerifyR20-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375
-> .ufo/waves/round-20/verify.py | 582 ++++++++++++++++++++++++++++++++++++++++++; 1 file changed, 582 insertions(+); exit 0
```

**Observation:** No LSP tool/provider is exposed in this seat's tool inventory, so LSP definitions/references were unavailable. No build, lint, formatter, or other verification was run.

Report: .ufo/waves/round-20/w1/VerifyR20.md
