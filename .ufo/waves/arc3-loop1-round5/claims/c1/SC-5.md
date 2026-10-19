# SC-5 — arc3-loop1-round5 C1 correctness sweep

Seat: SC-5 · chain c1 · independent sweep of arc3 rounds 1–4. Repo HEAD read-only pin: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. Wrote only this seat artifact; all recorded measurements below were rerun from Git objects, the landed tree, or cited Vyper evidence bytes. No REA target/runtime was executed for the Vyper static check.

## Verdicts and re-derivations

### (a) Command A — REPRODUCED

Ran the exact recipe at `SCORECARD.md:88-124` using `git show` against every supplied work/hygiene hash, plus records HEAD. Exact JSON output:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

All seven outputs independently give empty `missing`/`dangling`; the mapped denominator and citation-resolved/rule counts are shown per revision. In particular, `40de383` and records HEAD produce 84/84 and 14/14; the pre-Vyper `520341d` snapshot produces 83/83 and 14/14.

### (b) Custody-pair selftest — REPRODUCED; frozen invocation syntax DISCREPANCY

The frozen command form `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2: argparse prints `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` and `error: the following arguments are required: cmd`. The landed CLI requires a subcommand (script `:1308-1339`); the actual rerun was:

```text
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

The default selftest scratch was under `/dev/shm`, not `/tmp`. Thus the 28-case selftest claim reproduces, but the frozen `--selftest` spelling does not.

### (c) Citation-drift probe — REPRODUCED

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

### (d) Census v10 — REPRODUCED

Command: `python3 .ufo/gates/c1-census-v10.py --root .`. Landed-tree output included:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1631 loci=9
SKILL.md       lines=390  loci=2
-- STALE (0) --
-- AMBIGUOUS (0) --
-- UNDECLARED (0) --
-- UNRESOLVED (0) --
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

### (e) PROVINCE line hold and nine old literals — line hold REPRODUCED; absence claim DISCREPANCY

`wc -l PROVINCE.md` → `162 PROVINCE.md`. I checked each literal on `PROVINCE.md` directly with file-scoped Grep searches (fixed phrases; regex metacharacters escaped where needed). Eight were absent, but `JEB (unprobed)` still matches `PROVINCE.md:88`:

```text
NO MATCH: Reserve: 91MB Godot ARM64 template
MATCH:    JEB \(unprobed\) -> PROVINCE.md:88
NO MATCH: all 3 organic cores
NO MATCH: real solc/vyper-compiled bytecode untested
NO MATCH: Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
NO MATCH: probe-refused since r2
NO MATCH: pacman pairs beyond expac unexercised
NO MATCH: absent: `7z`
NO MATCH: 35 features incl. PyGhidra/BSim
```

Correction supported by admitted sources: `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:99` records an `inspect-jeb-client` live probe ending `capability_unavailable`/`unsupported_provider`, “fetch failed”; `corpus/knowledge/2026-10-14-r14-01-queue-b-residual.md:140-146` re-pins the same typed refusal and states exit 1. The `unprobed` wording is therefore stale. Accurate replacement: **“JEB (client probe attempted; blocked with typed refusal, no engine)”** (or equivalent). The 162-line hold is true, but “all nine stale literals absent” is false on the landed tree: eight absent, one still present.

### (f) Vyper entry spot-check — REPRODUCED from retained evidence

Entry under test: `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12-23`. Recomputed from `EX-04/out/abi.json`, the recorded planted set, runtime bytes and three sealed probe envelopes (`EX-04/evidence/`); this is a static evidence recheck, not a fresh REA invocation or runtime observation.

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/keccak256.py --selftest
selftest PASS keccak256(b'') = c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
selftest PASS keccak256(b'transfer(address,uint256)') = a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b
selftest PASS (2 canonical Ethereum vectors)
```

My script derived canonical function signatures from the ABI function entries, hashed them with the evidence Keccak implementation, and set-compared them with planted K and each probe result:

```text
abi_functions=15 abi_derived_K=15 recorded_planted_K=15 abi_vs_planted_equal=True missing=[] extra=[]
runtime.bin_bytes=1562 runtime.bin_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 runtime.hex_chars=3124 decoded_bytes=1562 hex_decodes_to_bin=True
probe[6.4.0-hex]: functions=15 planted_K=15 K_K=True missing=[] extra=[] dispatch_abi=15/15 bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 offsets_present=15
probe[6.4.0-raw]: functions=15 planted_K=15 K_K=True missing=[] extra=[] dispatch_abi=15/15 bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 offsets_present=15
probe[6.7.0-hex]: functions=15 planted_K=15 K_K=True missing=[] extra=[] dispatch_abi=15/15 bytecode_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 offsets_present=15
dispatch: runtime_bytes=1562 prologue_match=True table_offset=0x600 buckets=13 table_bytes=26 table_heads_jumpdest=13/13 repeated_target=0x5e7 repeats=3 empty_heads=3
dispatch_chains: selectors=15 unique=15 selector_set_equals_abi=True all_compare_shape_Dup2_Xor_Push2_Jumpi=True selector_push4_legs=15
dispatch_offsets[6.4.0-hex]: matched_fallthrough_entries=15/15 all_match=True offsets_at_jumpdest=0/15
dispatch_offsets[6.4.0-raw]: matched_fallthrough_entries=15/15 all_match=True offsets_at_jumpdest=0/15
dispatch_offsets[6.7.0-hex]: matched_fallthrough_entries=15/15 all_match=True offsets_at_jumpdest=0/15
```

The runtime begins `5f3560e01c6002600d820660011b61060001601e395f5156`: after selector extraction, the bytes implement `MOD` by 13, scale by two, `CODECOPY` the 13-entry table at `0x600`, then load and jump. Static parsing finds 15 unique selector legs with `DUP2/XOR/PUSH2/JUMPI`, matching the ABI/probe sets; all 15 reported offsets are the post-`JUMPI` fall-through, not a `JUMPDEST`. Runtime SHA-256 and the 15/15 K/K claim reproduce.

## Overall

Five checks reproduce as scoped (Command A, the selftest itself, citation-drift both modes, census, Vyper evidence). The PROVINCE line count reproduces, but the nine-absence subclaim does not: `JEB (unprobed)` remains at line 88 and requires a wording correction. The supplied custody invocation is also malformed for the landed argparse interface; using its required `selftest` subcommand passes all 28 cases.
