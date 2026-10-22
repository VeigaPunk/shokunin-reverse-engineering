# R29-C1 counter mutation probe

## Scope and detector

Target: `tools/round-29/c1-fresh-naming.py`, in the isolated clone at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC1Counter/clone` (clone HEAD `18be864a528873b2b70d8c94e31f880290249e90`). Only this cloned counter was mutated; each edit was restored before the next probe.

Bounded detector, used pristine, for each mutant, and after each restoration:

```sh
date -u +%Y-%m-%dT%H:%M:%SZ && sha256sum /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC1Counter/clone/tools/round-29/c1-fresh-naming.py && TMPDIR=/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC1Counter/tmp python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC1Counter/clone/tools/round-29/c1-fresh-naming.py --selftest; printf 'EXIT=%s\n' "$?"
```

**Observation — pristine:** 2026-10-22T20:21:16Z; counter SHA-256 `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda`; excerpt `selftest cases=22 failures=0`, `EXIT=0`. The test was therefore a usable baseline.

## Mutants

Each row records the one-line/minimal diff, mutated counter hash, UTC time, exact discriminating output excerpt and detector exit, verdict, and restored-byte check. Every restored hash was the pristine hash above; each restoration run printed `selftest cases=22 failures=0` and `EXIT=0`.

| Mutant (diff) | Mutated run: UTC, SHA-256, exact output excerpt, exit | Verdict | Restored run: UTC; SHA-256 |
|---|---|---|---|
| Drop CLAIM citation guard: `if not (s in cited and s in rows ...` → `if not (s in rows ...` | 20:22:18Z; `a3ca8d4011fc09c034749af9ff1780860e7faa515bf2a55146a44350b57f1252`; `FAIL red-entry-old-row exit=0 want=1`; `FAIL red-cites-other-new-row exit=0 want=1`; `selftest cases=22 failures=2`; `EXIT=1` | **Killed** | 20:22:29Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Accept any cited row: `s = CLAIM["row"]` → `s = sorted(cited)[0] if cited else CLAIM["row"]` | 20:22:45Z; `70bd70f88d70fa684ce4d93176ab5006395fb129ca5e93b0bb0ea5c575d0d130`; `FAIL red-cites-other-new-row exit=0 want=1`; `selftest cases=22 failures=1`; `EXIT=1` | **Killed** | 20:22:54Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Drop `s not in base`: remove `s not in brows and` from the row predicate | 20:23:03Z; `1696466b1ea050febd60bb5571aae739f99c211003acaf3c78f22f8eae7d40c0`; `selftest cases=22 failures=0`; `EXIT=0` | **Survived — coverage finding** | 20:23:11Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Off-by-one TARGET: `"runs": 16` → `"runs": 17` | 20:23:22Z; `067a601a6ddef2babd1d700055007cbda4ffbe0909162e183d32f3c02d92b457`; `selftest cases=22 failures=0`; `EXIT=0` | **Survived — coverage finding** | 20:23:30Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Drop one PINS entry: delete `RESOLVER: "4be915668ea20a643d04c9b8ae3c83bc9f5fd1b4d8821e06cabdccce36b3c23d",` | 20:23:40Z; `97ee27d4ff6cb5c55e1e7db708eec64fd5ea4f922b4f0a41a316a625a0382eaa`; `KeyError: 'tools/round-25/a2/resolve-selectors.py'`; `EXIT=1` | **Killed** (selftest aborts) | 20:23:53Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Relax run UTC boundary: `t <= counter_time` → `t < counter_time` | 20:24:11Z; `5a14a265386df92860901420fc89d5232232d1e06d89d6a34362faf67301a9b3`; `selftest cases=22 failures=0`; `EXIT=0` | **Survived — coverage finding** | 20:24:19Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Accept non-200 status 404: `m.get("status") != 200` → `m.get("status") != 200 and m.get("status") != 404` | 20:24:32Z; `59404ff586082bbf3d6282038b801a148bc5c3d6222b1982933408c843a9ae12`; `FAIL red-lookup-status exit=0 want=1`; `selftest cases=22 failures=1`; `EXIT=1` | **Killed** | 20:24:39Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |
| Drop tally-equality acceptance gate: remove `and c["tally_equal"] == 1 and` from `full` | 20:24:53Z; `427250645b48760b5935dd2941f8a0975d44ebcbd88dbdbc5ccd9ca5c1cf7154`; `selftest cases=22 failures=0`; `EXIT=0` | **Survived — coverage finding** | 20:25:14Z; `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` |

## Findings and restoration evidence

**Observation:** Four mutants were killed and four survived. The killed cases were detected by the indicated selftest assertion except the removed resolver pin, which made the test abort with the recorded `KeyError`. The four surviving mutant runs completed the detector with zero failures; these are coverage findings, not changes to the invariant.

**Inference:** The selftest sets `CLAIM["row"]` to `S002`, so its old-row citation case does not exercise a claimed row that is itself present in the base. It also resets `TARGET` to fixture counts (2 runs, 3 rows), so the production run target is bypassed. The early-UTC fixture is strictly earlier rather than exactly equal to the counter timestamp. Finally, `red-tally-edited` still returned the expected failure with the tally gate removed; the fixture also changes the entry's stated tally triple, so another validation appears to catch that case. These observations explain the survivors but do not alter the contract.

**Observation — final exact-byte check:** At 2026-10-22T20:25:44Z, `sha256sum` reported the same SHA-256 for the read-only lane counter and restored clone counter: `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda`.

Scratch artifact: restored clone counter at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC1Counter/clone/tools/round-29/c1-fresh-naming.py`, SHA-256 `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda`. No separate script or raw-output file was created; command output excerpts are captured above. No tools were installed or updated.