# SC-7 — C1 correctness sweep

Observed HEAD: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. This report records independent re-derivations; command outputs below were produced on the immutable commit objects or current tree, not copied from prior-round reports.

## (a) Command A at named commits — REPRODUCED

Replayed the source-derived recipe at `SCORECARD.md:88-124` against each named object. Exact JSON outputs:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
```

All six named snapshots have no missing or dangling map entries; mapped count equals knowledge-file count at each. Every SHA named in the frozen scope was measured as its own snapshot rather than assuming paired revisions had identical contents.

## (b) custody-pair selftest — REPRODUCED

The frozen shorthand `custody-pair.py --selftest` is not accepted by this tree's argparse interface (it requires the `selftest` subcommand; the shorthand invocation exited 2 with “the following arguments are required: cmd”). Ran the supported command with scratch on `/dev/shm`:

```text
CUSTODY_PAIR_SCRATCH=/dev/shm python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm
CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

## (c) citation-drift default and strict — REPRODUCED

With `TMPDIR=/var/tmp` for the probe's scratch:

```text
TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_VERDICT: reported findings=0 exit=0

TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## (d) census v10 — REPRODUCED

`python3 .ufo/gates/c1-census-v10.py --root .` returned `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0; `SCOPE-ERRORS (marker assertions): []`, `UNREADABLE (could-not-evaluate): []`, and `DECLARED FAIL CLASSES: []`.

## (e) PROVINCE line hold and nine literal checks — DISCREPANCY

`wc -l < PROVINCE.md` returned `162` (line count reproduced). Re-ran fixed-string checks with `grep -F` against all nine scoped needles; eight were absent, but one remained:

```text
PROVINCE line count: 162
ABSENT  Reserve: 91MB Godot ARM64 template
ABSENT  all 3 organic cores
88:  JEB (unprobed). Engine installs are operator-owned.
ABSENT  real solc/vyper-compiled bytecode untested
ABSENT  Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`
ABSENT  probe-refused since r2
ABSENT  pacman pairs beyond expac unexercised
ABSENT  absent: `7z`
ABSENT  35 features incl. PyGhidra/BSim
```

Thus the claim that all nine exact needles are absent does not reproduce: `JEB (unprobed)` is still present at `PROVINCE.md:88`. It occurs in the current alternate-providers clause, and `SCORECARD.md:1606` records the JEB item as “NO-CHANGE-with-cause” because no JEB install exists. I did not edit that clause; the corrected mechanical result is 8/9 needles absent, with the remaining occurrence named rather than silently counted as absent.

## (f) Vyper entry spot-check — REPRODUCED

For `CarrierV`, `sha256sum out/runtime.bin` in `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04` returned:

```text
57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0  out/runtime.bin
```

A local comparison of the entry's pre-probe planted set with the three cited probe envelopes (`probe-6.4.0-hex.json`, `probe-6.4.0-raw.json`, `probe-6.7.0-hex.json`) returned, for each: `functions=15 abi=15 unique=15 matches_planted=True planted=15 missing=[] extra=[]`; all three decoded bytecode digests equal the runtime SHA-256 above.

Ran `python3 evidence/dispatch-census.py out/runtime.hex evidence/planted-K.json evidence/probe/probe-6.4.0-hex.json` from the EX-04 directory. Output included `runtime bytes: 1562`, `assumed jump table at 0x600 (13 buckets x 2 B)`, `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, and `probe set == leg-chain set: True`. `out/opcodes.txt:1` begins `PUSH0 CALLDATALOAD PUSH1 0xE0 SHR PUSH1 0x02 PUSH1 0x0D DUP3 MOD ... PUSH2 0x0600 ... CODECOPY ... JUMP`, supporting the modulo-indexed 13-bucket table and dispatcher shape. The recorded REA envelopes say `runtime_execution: not-performed`; the dispatch census's mini-EVM is a local bytecode-routing model, not evidence of deployed/on-chain execution.

Entry pointers: `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19-22`; its listed primary evidence resides under `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/`.
