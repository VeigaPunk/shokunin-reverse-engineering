# TB-1 — C1 calibration sweep

HEAD re-derived as `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. Scope follows `claims-frozen.md:17-33`; no corpus, custody, or tracked files were changed. All reported measurements below were freshly calculated or run in this seat.

## 1. Command A at work commits — REPRODUCED

Replayed the `SCORECARD.md:88-124` Git-object recipe at each named work/checkpoint commit. Exact JSON output:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
```

Each has `missing=[]`, `dangling=[]`, and 10.0/10.0 scores. Recorded work-commit values reproduce: r1 `SCORECARD.md:1389-1393`; r2 `:1474-1476`; r3 `:1550-1554`; r4 `:1611-1612`. The `5be4a26` and `520341d` values are the additional named intermediate checkpoints; `520341d` is the parent of `40de383` (`git show -s --format='%H%n%P'`).

## 2. Landed-tree gates

- **Census v10 — REPRODUCED.** Command: `python3 .ufo/gates/c1-census-v10.py --root .` (exit 0). Exact summary output:

  ```text
  live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
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

- **Citation-drift probe — REPRODUCED, both modes.** `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` returned exact final line `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`. The same command with `--strict` returned `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- **Custody-pair selftest — REPRODUCED.** Valid CLI invocation is `python3 .ufo/gates/custody-pair/custody-pair.py selftest`; exact result: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (scratch: `/dev/shm/custody-pair-selftest-qjuoq9q5`). Invocation note: the supplied `custody-pair.py --selftest` form is not accepted by this tree; it returned `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` / `error: the following arguments are required: cmd` (exit 2). The parser defines `selftest` as a subcommand at `.ufo/gates/custody-pair/custody-pair.py:1308-1339`.

## 3. PROVINCE line hold and nine literals — DISCREPANCY

`wc -l PROVINCE.md` returned exact output `162 PROVINCE.md` (also confirmed by `PROVINCE.md:1-162`). I queried each exact literal from the round-4 residual list (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:1-11`) with escaped exact-string Grep patterns; eight returned `No non-sensitive matches found`:

- `Reserve: 91MB Godot ARM64 template`
- `all 3 organic cores`
- `real solc/vyper-compiled bytecode untested`
- `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\``
- `probe-refused since r2`
- `pacman pairs beyond expac unexercised`
- `absent: \`7z\``
- `35 features incl. PyGhidra/BSim`

The ninth, `JEB (unprobed)`, **is present**: Grep returned `kaidoku-shokunin/PROVINCE.md:88:  JEB (unprobed). Engine installs are operator-owned.` Therefore the strict file-wide literal-absence assertion is **8/9, not 9/9**. This is a discrepancy against `SCORECARD.md:1603-1606` (“all nine stale literals cleared”); the hit is in the current Alternate providers row (`PROVINCE.md:87-89`) and may be an intentional no-change, so I make no proposed edit. The literal-level absence claim itself does not reproduce.

## 4. Vyper entry spot-check against its evidence — REPRODUCED

Inputs were the committed CarrierV ABI/runtime and the three cited EX-04 probe envelopes. I recomputed Ethereum Keccak selectors from `EX-04/out/abi.json:1` using the evidence's standalone Keccak implementation (canonical empty-string and `transfer(address,uint256)` vectors both PASS), then compared the result to each stored envelope. I also decoded the runtime bytes and walked the modulo table/XOR compare chains independently; no REA tool was re-run and no target/runtime execution or deployment identity is claimed.

Exact fresh selector/envelope output:

```text
probe-6.4.0-hex.json: selectors=15/15 set_equal=True missing=0 extra=0 dispatch_abi=15/15 bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.4.0-raw.json: selectors=15/15 set_equal=True missing=0 extra=0 dispatch_abi=15/15 bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.7.0-hex.json: selectors=15/15 set_equal=True missing=0 extra=0 dispatch_abi=15/15 bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
```

Fresh byte/dispatch output:

```text
keccak selftest: PASS
ABI functions=15; probe functions=15; ABI selectors == probe selectors: True; K/K=15/15; dispatch=abi 15/15
runtime.bin bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0; hex-decodes-equal=True; envelope-bytecode-sha256-match=True
prologue=5f3560e01c6002600d820660011b61060001601e395f5156; modulo-opcode-at-0x0a=0x06; table-offset=0x600; buckets=13; targets-are-JUMPDEST=True; table-sentinel-0x5e7-count=3
XOR-chain selectors=15; compare-shape=15/15; chain-set == ABI-set == probe-set: True; reported-offset == leg fall-through: 15/15; offsets-at-JUMPDEST=0/15
```

`wc -c` + `sha256sum` independently returned `1562 .../EX-04/out/runtime.bin` and `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 .../runtime.bin`. The byte-level dispatcher replay independently returned `runtime bytes: 1562`, `assumed jump table at 0x600 (13 buckets x 2 B) -> tail 26 B`, `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and `probe set == leg-chain set: True`. This supports the entry's CarrierV claims at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19-22` and its evidence pointers at `:32`; the byte-level claims are consistent with `EX-04/out/verify-report.json:5-59` and `EX-04/evidence/probe/probe-6.4.0-hex.json:1`.

## Coverage of this seat

All six frozen C1 checks were attempted. Five groups reproduce; the file-wide stale-literal check has the single named discrepancy above. C2 corpus-wide audit and C3 debt disposition are outside TB-1's c1 chain assignment.
