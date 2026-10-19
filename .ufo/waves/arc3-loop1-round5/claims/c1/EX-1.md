# EX-1 — C1 correctness sweep

Seat assignment: `EX-1` → chain `c1` (`claims-frozen.md:81-85`). I re-ran the checks below against Git objects or the landed tree; results are observations from this pass, not copied prior results. No tracked or custody path was written.

## Command A — revision counts

Ran the recipe at `SCORECARD.md:88-124` against each listed object (and the records commits/HEAD for chronology). Output fields below are from those invocations; `mapped/files`, `resolved/rules`, and scores reproduce as follows:

| Revision | Direct history identity | Mapped / files | Resolved / rules | Missing, dangling | Coverage / depth | Verdict |
|---|---|---:|---:|---|---|---|
| `fbbbd45` | r1 work | 82/82 | 13/13 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `28aa7a9` | r2 work | 82/82 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `c418be0` | r3 work | 83/83 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `5be4a26` | hygiene; parent is `c418be0` | 83/83 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED at this object |
| `015e1ba` | r3 records | 83/83 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `520341d` | r4 custody work; parent is `015e1ba` | 83/83 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `40de383` | r4 Vyper work; child of `520341d` | 84/84 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `c07af80` | r2 records | 82/82 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |
| `71668cc` (`HEAD`) | r4 records | 84/84 | 14/14 | `[]`, `[]` | 10.0/10.0 | REPRODUCED |

Command output form, for example: `{"citation_resolved_rules":13,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":82,"mapped":82,"missing":[],"revision":"fbbbd45","rule_blocks":13}`; each later output had the corresponding values in the table.

**Attribution discrepancy:** the dispatch note groups `5be4a26` with r2, but `git log --all --graph --oneline` / `git show -s --format='%H %P %s'` re-derived its subject as `hygiene: drop committed pyc...` and parent as `c418be0` (r3 work). The same history shows `520341d` parent `015e1ba`, then `40de383` parent `520341d`; thus the 83→84 increase occurs from `520341d` to `40de383`, not in the reverse order. The per-object measurements all reproduce; the round grouping/order supplied for these commits does not.

## Landed-tree gates

Measured at `HEAD=71668ccd2c920b907672b5c40efaafe7c2e75bd1`:

- `python3 .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0. Output also reports `PROVINCE.md lines=162`.
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- Same command with `--strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- The named `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` invocation returns argparse usage, exit 2: this script requires a subcommand (`custody-pair.py:1308-1334`), not a `--selftest` flag. Correct invocation, `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm`, returned `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. Scratch was removed after the run. **Verdict:** 28-case selftest REPRODUCED; command spelling DISCREPANCY.

## PROVINCE line hold and nine literal checks

`wc -l PROVINCE.md` → `162 PROVINCE.md`; `git diff --quiet 40de383:PROVINCE.md HEAD:PROVINCE.md` returned 0 (same blob content from r4 Vyper work through HEAD).

I re-searched each exact needle in the live `PROVINCE.md` (literal patterns; the workspace search returned no match for eight):

- Absent: `Reserve: 91MB Godot ARM64 template`
- Absent: `all 3 organic cores`
- **Present:** `JEB (unprobed)` — `PROVINCE.md:88`
- Absent: `real solc/vyper-compiled bytecode untested`
- Absent: `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\``
- Absent: `probe-refused since r2`
- Absent: `pacman pairs beyond expac unexercised`
- Absent: `absent: \`7z\``
- Absent: `35 features incl. PyGhidra/BSim`

**DISCREPANCY:** 8/9 needles are absent, not 9/9. The remaining phrase is explicitly recorded as NO-CHANGE-with-cause at `SCORECARD.md:1605-1606`; this report flags the literal sweep mismatch without treating that adjudication as a new semantic correction.

## Vyper-entry spot check

Entry: `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:7,12,19,21` (source/evidence paths at `:5,32`). I re-derived the CarrierV claims against the shipped carrier and a fresh pinned CLI call:

- `wc -c` on `EX-04/out/runtime.bin` and `runtime.hex` → 1,562 and 3,124 bytes. `sha256sum` → runtime bytes `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; hex text `e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192`.
- Fresh command: `TMPDIR=/var/tmp/ex1-vyper-recheck npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json`. Parsed output: `functions=15 abi_dispatch=15 decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 decoded_bytes=1562 selector_set_matches_planted=True missing=0 extra=0`; the 15-selector set exactly matches the pre-recorded planted set.
- Fresh byte-level decode of `runtime.hex`: prefix begins `5f3560e01c6002600d820660011b61060001601e39`; a modulo-indexed 13-entry table begins at `0x600`, all 13 destinations are `JUMPDEST`, the `0x5e7` empty-bucket sentinel occurs 3 times, and 15 unique `DUP2/XOR` selector legs were found. Re-running the cited `dispatch-census.py` against the carrier and probe also yielded `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and `probe set == leg-chain set: True`.

**Verdict:** the 15/15 K/K, runtime SHA-256, and modulo-table/XOR dispatch-shape claims are REPRODUCED on these pinned bytes. This is static artifact analysis; it does not establish runtime contract behavior or chain identity. Entry scope remains RESULT/no Core promotion (`:30`).

## C1 disposition

All six frozen C1 facets were exercised. Command A, census, citation drift, province length, custody test (with the parser-correct command), and Vyper carrier spot-check reproduce as recorded. **Overall: DISCREPANCY** for the stale-literal 9/9 assertion (one named NO-CHANGE needle remains), the custody command spelling, and commit attribution/order as described above; no lane/corpus/PROVINCE files were modified.
