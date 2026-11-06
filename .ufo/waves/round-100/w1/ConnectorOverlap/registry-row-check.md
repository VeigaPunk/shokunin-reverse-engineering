# Round-100 registry rows: exit maps verified against source (A2 cbd224ef; lane HEAD b0a7bb8ca)

A2 contains no `tools/round-100/*.py` row. Lane HEAD b0a7bb8ca has four. Blob sha256 match across F, A1, A2 and HEAD where the tool exists.

| tool | sha256 (row = A1 = A2 = HEAD blob) | exit map in row | verified in source (A2) |
|---|---|---|---|
| tools/round-100/pe-upx-corrupt-battery.py | 8f148d336e6f95ac60a805fc063f8e627d7c04789b138e318bb11c847fd83183 (F = A2) | 0 frozen label; 1 other label; 2 preflight | `return 0 if met else 1` :461; preflight `return 2` :278-336. Matches. |
| tools/round-100/upx-pe-repair.py | 15ada0b0e2b3732b67051ed7c49108d92889fe0d756e0b1dfd5df17334a99a37 (absent at F; A1 = A2 = HEAD) | 0 repaired or intact; 2 typed refusal | `return 0` :217; `refuse()` returns 2 :177; `sys.exit(main())` :221. Exception set caught `(Refuse, struct.error)` :199. **Row omits exit 1**; round-98 row lists `1=uncaught CLI error`. See F11. |
| tools/round-100/gen-forgeries.py | c3f3c425d53c5ab09f9cb580dea5914b99b5ce990fc76c519d2d2ebf8a2ca586 (F = A1 = A2 = HEAD) | 0 written; 1 SystemExit missing anchor | `return 0` :87. Missing-anchor path not re-run here. |
| tools/round-100/registry-selftest-truth.py | 496a4979ecd6be4e50db21fdca3fec8bc5f427aad85014acf06bc7be6fa6e1f4 (F = A2) | 0 label exact; 1 other label; 2 could-not-evaluate | `return 0 if met else 1` :288; `return 2` :246-273. `--selftest` present (:240). |

## Self-test run at A2 (command and output)
`python3 -I -B tools/round-100/registry-selftest-truth.py --selftest` in the scratch clone at cbd224ef → exit 0, last line `SELFTEST cases=22 failures=0`. Copy: `.ufo/waves/round-100/w1/ConnectorOverlap/c2-selftest-at-cbd224ef.txt`.

## Probe of pe-upx-repair exit codes (scratch inputs)
Command: `python3 -I -B tools/round-100/upx-pe-repair.py --in <f> --out <f>.out --json` for four hostile inputs:
- empty.bin → exit 2, `{"refused": "not-mz"}`
- mz2.bin (two bytes `MZ`) → exit 2, `not-mz`
- mzpe-short.bin (MZ + PE header, one section table entry) → exit 2, `sections`
- mz-badoff.bin (e_lfanew 0x7fffffff) → exit 2, `not-pe`
No `.out` file written in any case. No exit 1 observed. Uncaught classes outside `(Refuse, struct.error)` were not exercised.

## Rows the L1 must add (or confirm) at its landing revision
1. `tools/round-100/pe-upx-corrupt-battery.py` — counter, `--expect` label, `--work`, `--json-out`, no `--selftest`.
2. `tools/round-100/upx-pe-repair.py` — tool, exit map 0/2, and add `1=uncaught CLI error` unless the L1 proves the exit-1 path absent.
3. `tools/round-100/gen-forgeries.py` — generator, exit 0/1, writes `--out-dir` only.
4. `tools/round-100/registry-selftest-truth.py` — counter, exit 0/1/2, `--selftest` 22 cases (confirm the row's cell says 22).
Rule 201 (QUALITY row 201) requires every `tools/round-N/*.py` to have a row before the report. The round-99 self-assessment-audit A4 covers rounds 97-99 only, so no counter enforces this for round 100.
