# TB-3 — C1 correctness sweep

Chain: `c1` (calibration), wave `arc3-loop1-round5`. Scope: `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-33`. All measurements below were rerun from this checkout or recomputed from the cited bytes; prior report numbers were not used as measurement evidence.

## Results

### 1. Command A at the arc3 work commits — REPRODUCED

I reran the recipe at `SCORECARD.md:88-124` against Git objects. I ran every SHA in the frozen grouped list individually, including the r2 hygiene commit and r4 custody commit:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
```

Every measurement has no missing or dangling map entries; mapped counts and resolvable-rule counts reproduce. The final work commit is 84/84 mapped and 14/14 resolvable.

### 2. Custody-pair selftest — REPRODUCED; supplied CLI spelling is DISCREPANT

The frozen invocation `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` exits 2 with `error: the following arguments are required: cmd`. The actual parser has a `selftest` subcommand (`custody-pair.py:1329-1333`; usage also at `.ufo/gates/custody-pair/README.md:21-39`). Running the actual command with permitted scratch:

```text
$ python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

All 28 case lines reported `PASS`. The behavioral claim reproduces; the `--selftest` spelling does not.

### 3. Citation-drift probe, both modes — REPRODUCED

Commands: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` and the same command with `--strict`.

```text
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

### 4. Census v10 — REPRODUCED

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

### 5. PROVINCE line hold and stale-literal sweep — DISCREPANCY

`wc -l PROVINCE.md` returned `162`. I used the nine requested literal needles from the R4 residual checklist (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/evidence/residual-and-token-sweep.txt:1-10`) as test inputs, checked each was present in the pre-R4 parent `015e1bab914713568f339fd53999bc180459cc40` using `git show ... | grep -F`, and reran `grep -F` on landed `PROVINCE.md`:

```text
needle=Reserve: 91MB Godot ARM64 template | baseline=present | landed=ABSENT
needle=all 3 organic cores | baseline=present | landed=ABSENT
needle=JEB (unprobed) | baseline=present | landed=present
needle=real solc/vyper-compiled bytecode untested | baseline=present | landed=ABSENT
needle=Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` | baseline=present | landed=ABSENT
needle=probe-refused since r2 | baseline=present | landed=ABSENT
needle=pacman pairs beyond expac unexercised | baseline=present | landed=ABSENT
needle=absent: `7z` | baseline=present | landed=ABSENT
needle=35 features incl. PyGhidra/BSim | baseline=present | landed=ABSENT
```

Thus the frozen “nine stale-literal absences” does not reproduce as stated: eight needles are absent, but the exact `JEB (unprobed)` needle remains at `PROVINCE.md:87`. The R4 record at `SCORECARD.md:1605-1606` explicitly says this wording was adjudicated NO-CHANGE-with-cause (the verb was probed; no JEB installation exists). Correction: report eight absent plus one intentionally retained/adjudicated phrase, not nine absent. The line-count hold does reproduce.

### 6. Vyper entry evidence — REPRODUCED (evidence spot-check, not a new REA probe)

Scope: `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:11-24`, with CarrierV bytes/evidence under `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/`.

Fresh hash/size check on the committed runtime files:

```text
57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0  .../EX-04/out/runtime.bin
1562 .../EX-04/out/runtime.bin
3124 .../EX-04/out/runtime.hex
```

I parsed the ABI, recomputed the 15 function selectors with the local Keccak-256 implementation, and compared them with `planted-K.json` and the three retained probe envelopes. The two canonical Keccak test vectors passed. Exact recomputation summary:

```text
abi_function_entries=15 derived_signatures=15 abi_selector_map_equals_planted=True
probe-6.4.0-hex.json raw=15 normalized=15 unique=15 exact_selector_set=True all_dispatch_abi=True decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.4.0-raw.json raw=15 normalized=15 unique=15 exact_selector_set=True all_dispatch_abi=True decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
probe-6.7.0-hex.json raw=15 normalized=15 unique=15 exact_selector_set=True all_dispatch_abi=True decoded_sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
```

I freshly ran `EX-04/evidence/dispatch-census.py` against the runtime hex, planted selectors, and both-pin hex envelopes. On both runs it returned `runtime bytes: 1562`, a 13-bucket × 2-byte jump table at `0x600` (26-byte tail), 15 selector legs in XOR compare chains, `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and `probe set == leg-chain set: True`. All 15 reported offsets were not JUMPDESTs, as the entry specifies; selector discovery and dispatcher shape agree with the bytes and retained envelopes.

## Overall

Four of the six scoped checks reproduce without qualification. The custody selftest reproduces using the parser's `selftest` subcommand (the frozen `--selftest` spelling is invalid); the PROVINCE line count reproduces, but its nine-absence assertion has one retained JEB needle. No scoped item was left unchecked.
