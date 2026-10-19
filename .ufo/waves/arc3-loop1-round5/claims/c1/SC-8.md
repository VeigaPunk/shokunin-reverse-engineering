# Seat report — SC-8 (chain c1)

Assignment: C1 correctness sweep per `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-36`. Read-only audit at HEAD `71668ccd2c920b907672b5c40efaafe7c2e75bd1`; only this seat artifact was written.

## Findings

1. **Command A — REPRODUCED.** Re-ran the recipe at `SCORECARD.md:88-124` against each supplied immutable work-commit ID, plus the intermediate `520341d`. Exact outputs:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
```

The recorded round checkpoints reproduce: r1 `82/82, 13/13` (`SCORECARD.md:1389-1393`), r2 `82/82, 14/14` (`:1474-1476`), r3 `83/83, 14/14` (`:1550-1554`), and r4 `84/84, 14/14` (`:1611-1612`). All six results have no missing or dangling map tokens and scores 10.0/10.0.

2. **Custody-pair selftest — DISCREPANCY in the specified invocation; test reproduced with the CLI's actual subcommand.** The requested `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 with `custody-pair.py: error: the following arguments are required: cmd`. The parser defines positional subcommands at `.ufo/gates/custody-pair/custody-pair.py:1308-1333`; the valid form is `selftest` (not `--selftest`). Ran `CUSTODY_PAIR_SCRATCH=/dev/shm python3 .ufo/gates/custody-pair/custody-pair.py selftest`; exact final line: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. No `/tmp` scratch used.

3. **Citation-drift probe, default — REPRODUCED.** `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.

4. **Citation-drift probe, strict — REPRODUCED.** `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

5. **Census v10 — REPRODUCED.** `python3 .ufo/gates/c1-census-v10.py --root .` returned:

```text
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1631 loci=9
SKILL.md       lines=390  loci=2
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

6. **PROVINCE line hold and stale-literal sweep — DISCREPANCY.** `wc -l PROVINCE.md` → `162`. I checked each literal with `grep -nF -- <literal> PROVINCE.md`; the pre-repair blob `520341d:PROVINCE.md` independently contains all 9 needles, while current HEAD contains 1/9:

```text
Reserve: 91MB Godot ARM64 template — ABSENT (grep exit 1)
all 3 organic cores — ABSENT (grep exit 1)
JEB (unprobed) — PRESENT: PROVINCE.md:88  JEB (unprobed). Engine installs are operator-owned.
real solc/vyper-compiled bytecode untested — ABSENT (grep exit 1)
Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` — ABSENT (grep exit 1)
probe-refused since r2 — ABSENT (grep exit 1)
pacman pairs beyond expac unexercised — ABSENT (grep exit 1)
absent: `7z` — ABSENT (grep exit 1)
35 features incl. PyGhidra/BSim — ABSENT (grep exit 1)
```

Corrected observation: **8/9 absent; `JEB (unprobed)` remains** at `PROVINCE.md:87-88`. This conflicts with the frozen absence check and the round-4 statement “all nine stale literals cleared” (`SCORECARD.md:1603-1606`). Round 4 also records JEB as a no-change adjudication with cause there, but that does not make the literal absent. This seat cannot change `PROVINCE.md` under the write-scope restriction; parent disposition required.

7. **Vyper entry evidence spot-check — REPRODUCED.** The entry states the CarrierV claim at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19,21`. I parsed the entry’s own `EX-04` planted-set and all three cited probe envelopes; output:

```text
planted K=15 distinct=15
probe-6.4.0-hex.json: functions=15 unique=15 duplicates=0 missing=0 extra=0 K/K=True dispatch=['abi']
  decoded-bytes=1562 decoded-sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.4.0-raw.json: functions=15 unique=15 duplicates=0 missing=0 extra=0 K/K=True dispatch=['abi']
  decoded-bytes=1562 decoded-sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.7.0-hex.json: functions=15 unique=15 duplicates=0 missing=0 extra=0 K/K=True dispatch=['abi']
  decoded-bytes=1562 decoded-sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
```

`EX-04/out/runtime.bin` independently hashes to `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0` (1,562 bytes); decoding `runtime.hex` produces byte-identical bytes and the same SHA-256. Running the cited `EX-04/evidence/dispatch-census.py` against the committed runtime, planted set, and hex envelope reports `assumed jump table at 0x600 (13 buckets x 2 B)`, `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and `probe set == leg-chain set: True`. The runtime prefix is `5f3560e01c6002600d820660011b61060001601e`; the decoder’s chain legs are `PUSH4; DUP2; XOR; PUSH2; JUMPI`. This is a static evidence check of the recorded REA results, not a fresh REA probe or runtime execution. Evidence sources: `EX-04/evidence/planted-K.json:23-39`, `EX-04/evidence/probe/probe-{6.4.0-hex,6.4.0-raw,6.7.0-hex}.json`, `EX-04/out/runtime.bin`, and `EX-04/evidence/dispatch-census.py:7-14`.
