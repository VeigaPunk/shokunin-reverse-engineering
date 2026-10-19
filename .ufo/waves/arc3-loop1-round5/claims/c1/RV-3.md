# RV-3 — C1 calibration sweep (arc3-loop1-round5)

Seat RV-3 is assigned to C1 by `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-33,83-84`. Scope is the six listed sweep items only. All measurements below are first-hand against immutable Git objects or the landed tree at `71668ccd2c920b907672b5c40efaafe7c2e75bd1` (HEAD). No custody path or tracked project file was written.

## Verdicts

1. **Command A — REPRODUCED.** Used the recipe in `SCORECARD.md:88-124`, looping its `REV` input across the named commits and HEAD. Exact JSON output:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

All seven objects have `missing=[]`, `dangling=[]`, and 10.0/10.0 scores. The round work commits reproduce the sequence: `fbbbd45` 82/82, 13/13; `28aa7a9` 82/82, 14/14; `c418be0` 83/83, 14/14; `40de383` 84/84, 14/14. Also checked the intervening hygiene commit `5be4a26` and custody commit `520341d`, both 83/83 and 14/14. The fresh outputs, not earlier reports, are the evidence.

2. **Custody-pair selftest — DISCREPANCY in the supplied invocation; REPRODUCED under the tool's supported invocation.** Running the stated `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` returned:

```text
usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...
custody-pair.py: error: the following arguments are required: cmd
exit 2
```

The parser defines `selftest` as a positional subcommand, not `--selftest` (`.ufo/gates/custody-pair/custody-pair.py:1306-1333`). Corrected invocation `python3 .ufo/gates/custody-pair/custody-pair.py selftest` returned the exact summary:

```text
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

The cases include the tool's custody-write refusal checks; the script's selftest reports all 28 passing.

3. **Citation-drift probe — REPRODUCED in both modes.** Commands run against `HEAD`:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0

$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

4. **Census v10 — REPRODUCED.** Command: `python3 .ufo/gates/c1-census-v10.py --root .`. Landed-tree output:

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

5. **PROVINCE hold and nine stale-literal absences — REPRODUCED.** `wc -l PROVINCE.md` returned `162 PROVINCE.md`. I derived the obsolete text from `git show --format= --unified=0 40de383 -- PROVINCE.md`, then checked each exact literal against the landed `PROVINCE.md`; each fixed-literal Grep probe returned `No non-sensitive matches found` (0 matches):

```text
config.toml:3298
35 features incl. PyGhidra/BSim
1Password 423-file asar
absent: `7z`, `cabextract`
Reserve: 91MB Godot ARM64 template, ARM64X hybrids
all 3 organic cores
real solc/vyper-compiled bytecode untested
Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS
probe-refused since r2; multi-version pacman pairs beyond expac unexercised
```

The current file is `PROVINCE.md:1-162`; the round-4 same-line edits are visible in the cited Git diff. The fixed-literal searches were issued against this file only.

6. **Vyper entry spot-check — REPRODUCED.** Sources are `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:3,12,19,21-22`, the CarrierV ABI (`.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/abi.json:1`), planted set (`.../evidence/planted-K.json:23-40`), probe envelope (`.../evidence/probe/probe-6.4.0-hex.json:1`), and binary `.../out/runtime.bin`. I independently derived selectors from all ABI function signatures using the included Keccak routine (and ran its two canonical-vector selftests), then compared the resulting sets with the planted set and probe output:

```text
selftest PASS keccak256(b'') = c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
selftest PASS keccak256(b'transfer(address,uint256)') = a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b
selftest PASS (2 canonical Ethereum vectors)
ABI function entries=15; re-derived selectors=15; planted K=15; probe selectors=15
ABI==planted=True ABI==probe=True missing=[] extra=[]
dispatch abi=15/15
runtime.bin bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe decoded bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 raw==decoded=True envelope_hash_match=True
prologue24=5f3560e01c6002600d820660011b61060001601e395f5156 entry_opcode=0x5b
PUSH4-DUP2-XOR-PUSH2-JUMPI sites=15 distinct=15 selectors_equal_abi=True
table_words=0x029c,0x05e7,0x050b,0x0400,0x05ac,0x043f,0x053d,0x05e7,0x0590,0x0574,0x0382,0x05e7,0x0018
jumpdest_targets=10/10 all_target_bytes_0x5b=True sentinel_0x5e7=3
sentinel_offset=0x5e7 opcode=0x5b is_jumpdest=True
```

Thus the cited 15/15 K/K, decoded/runtime SHA-256 identity and modulo-indexed table plus XOR-comparison dispatcher shape all reproduce on the entry's own CarrierV evidence. `runtime.bin` was read-only; no compiler or probe was re-run.
