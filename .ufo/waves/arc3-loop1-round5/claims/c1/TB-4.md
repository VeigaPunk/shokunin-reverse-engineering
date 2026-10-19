# TB-4 — C1 correctness sweep

HEAD at sweep: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`.

## (a) Command A — REPRODUCED at the work revisions

I re-ran the recipe at `SCORECARD.md:88-124` against each Git tree, using its `git show`/`git ls-tree` source reads. These are the run outputs (all six also report `missing: []`, `dangling: []`, and coverage/depth scores `10.0/10.0`):

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
```

The recorded work-tree values reproduce: r1 `fbbbd45` 82/82, 13/13; r2 `28aa7a9` 82/82, 14/14; r3 `c418be0` 83/83, 14/14; r4 `40de383` 84/84, 14/14 (`SCORECARD.md:1389-1393,1474-1476,1550-1554,1611-1613`). **DISCREPANCY (revision grouping only):** the supplied grouping of `5be4a26` with r2 does not follow Git ancestry. `git show -s --format='%H %P %s' 5be4a26` reports its parent as `c418be0`; its own commit is hygiene-only (`.gitignore` and removal of a bytecode cache). Its tree therefore returns the later 83/83 state. This does not change the reproduced r2 work-commit result at `28aa7a9`.

## (b) Custody-pair selftest — DISCREPANCY in the frozen invocation; test REPRODUCED

The frozen shorthand `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2: `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` / `error: the following arguments are required: cmd`. The CLI defines `selftest` as a positional subcommand (`.ufo/gates/custody-pair/custody-pair.py:1329-1333`). Re-running with the required form:

```text
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

Thus the 28-case result reproduces; the invocation written in the frozen gate list does not.

## (c) Citation-drift probe — REPRODUCED

Commands on landed HEAD:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## (d) Census v10 — REPRODUCED

Command: `python3 .ufo/gates/c1-census-v10.py --root .`.

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

## (e) PROVINCE line hold and stale-literal scan — DISCREPANCY

First-hand `wc -l PROVINCE.md` output: `162 PROVINCE.md`; `sha256sum` output: `11a5c60450cc736a5b5443fa559191dc35b246386927cbd854b5e9fef1f0bcf2  PROVINCE.md`.

I searched the nine exact strings listed in `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:2-10` against the current file. The live literal-count output was:

```text
Reserve: 91MB Godot ARM64 template\tABSENT
all 3 organic cores\tABSENT
JEB (unprobed)\tPRESENT x1
real solc/vyper-compiled bytecode untested\tABSENT
Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`\tABSENT
probe-refused since r2\tABSENT
pacman pairs beyond expac unexercised\tABSENT
absent: `7z`\tABSENT
35 features incl. PyGhidra/BSim\tABSENT
```

Thus eight are absent, but `JEB (unprobed)` is **present once**, at `PROVINCE.md:88` (`JEB (unprobed). Engine installs are operator-owned.`). The measured result is **8/9 absent**, not 9/9. The literal is separately recorded as a NO-CHANGE ruling in `SCORECARD.md:1603-1606`; I make no corpus or PROVINCE edit under this seat's write boundary.

## (f) Vyper entry spot-check — REPRODUCED against its evidence

The entry identifies its CarrierV evidence and claims at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:7,12,19,21-22`. I compared the committed planted-selector JSON, 6.4.0 hex probe envelope, and runtime bytes directly:

```text
planted=15 probe=15 intersection=15 missing=[] extra=[] all_dispatch_abi=True
runtime.bin_bytes=1562 runtime.bin_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 runtime.hex_decoded_bytes=1562 runtime.hex_decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 byte_identical=True
prologue_hex=5f3560e01c6002600d820660011b61060001601e39 table_start=0x600 table_entries=13
```

I also ran the entry's byte-level census on those local evidence files:
`python3 .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/dispatch-census.py .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json`.
Its output reports `runtime bytes: 1562`, a 13-entry table at `0x600`, `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and `probe set == leg-chain set: True` with no extras. The decoded prologue contains `DUP3; MOD` and `PUSH2 0x0600; ... CODECOPY`; the 15 selector legs use `DUP2; XOR; PUSH2; JUMPI`. Four buckets contain multiple selector legs (indices 5, 6, 10, 12). All 15 probe offsets match the byte-derived fall-through body entries, each reported `JUMPDEST@probe=False`. This supports the entry's modulo-indexed jump-table/XOR-chain shape claim. This is a static check of the committed runtime and evidence (including the instrument's local mini-EVM), not a fresh REA probe or chain/runtime observation.
