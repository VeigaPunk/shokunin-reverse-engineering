# RV-1 — C1 calibration correctness sweep

HEAD observed: `71668ccd2c920b907672b5c40efaafe7c2e75bd1`. Scope is the C1 checklist in `.ufo/waves/arc3-loop1-round5/claims-frozen.md:17-36`. All measurements below were freshly derived; no prior seat's number is used as measurement evidence. I changed only this artifact.

## 1. Command A — REPRODUCED

Re-ran the recipe at `SCORECARD.md:88-124` against immutable Git objects (`git show REV:path` / `git ls-tree`), separately for every named hash and HEAD. Exact JSON stdout:

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

The four round-work claims match the records: r1 82/82, 13/13 at `SCORECARD.md:1389-1391`; r2 82/82, 14/14 at `:1474-1476`; r3 83/83, 14/14 at `:1550-1554`; r4 84/84, 14/14 at `:1611-1613`. All have empty missing/dangling sets and both scores 10.0. The additional snapshots were also measured, not inferred: `5be4a26` = 83/83, `520341d` = 83/83, current HEAD = 84/84. `git show -s` identifies `5be4a26` as a hygiene commit with parent `c418be0`, and `520341d` as the parent of `40de383`; outputs are therefore attached to hashes rather than assumed round labels.

## 2. Landed-tree gates

- **Census — REPRODUCED:** `python3 .ufo/gates/c1-census-v10.py --root .` printed `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. It reported `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1631 loci=9`, `SKILL.md lines=390 loci=2`; `SCOPE-ERRORS (marker assertions): []`, `UNREADABLE (could-not-evaluate): []`, `G2 positive-assertion guard: ok`, `G7 ... []`, `G11 ... []`, `DECLARED FAIL CLASSES: []`.
- **Citation drift default — REPRODUCED:** `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`.
- **Citation drift strict — REPRODUCED:** same command with `--strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- **Custody selftest — REPRODUCED:** actual CLI form `python3 .ufo/gates/custody-pair/custody-pair.py selftest` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (scratch `/dev/shm/custody-pair-selftest-o0fyrfkg`). The prompt's spelling `custody-pair.py --selftest` is not accepted by this revision: it exits 2 with `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` / `the following arguments are required: cmd`. Source `custody-pair.py:1308-1333` defines `selftest` as a subcommand. The test itself passed using that actual subcommand.

## 3. PROVINCE line hold and stale-literal sweep

- **162-line hold — REPRODUCED:** re-read Git blobs directly: `520341d` parent = 19,498 bytes / 162 lines; `40de383` = 19,908 bytes / 162 lines; HEAD `71668cc` = 19,908 bytes / 162 lines. This verifies the line-count hold across the r4 work commit; `PROVINCE.md` itself also reads through line 162.
- Searched each of the nine required literal substrings individually against current `PROVINCE.md` using exact literal queries (the dedicated Grep tool; regex metacharacters escaped, fixed-substring semantics):

| Literal | Result |
|---|---|
| `Reserve: 91MB Godot ARM64 template` | no match |
| `all 3 organic cores` | no match |
| `JEB (unprobed)` | **DISCREPANCY — match at `PROVINCE.md:88`: `JEB (unprobed). Engine installs are operator-owned.`** |
| `real solc/vyper-compiled bytecode untested` | no match |
| `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\`` | no match |
| `probe-refused since r2` | no match |
| `pacman pairs beyond expac unexercised` | no match |
| `absent: \`7z\`` | no match |
| `35 features incl. PyGhidra/BSim` | no match |

Corrected result is **8/9 absent; 1 stale literal remains**, not 9/9 absent. This contradicts the round record's “all nine stale literals cleared” at `SCORECARD.md:1603-1605`. The underlying evidence for correcting the wording is `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:99`: `inspect-jeb-client` was probed and returned typed `capability_unavailable` / `unsupported_provider` (`fetch failed`), so “unprobed” is inaccurate even though no JEB engine is available. Suggested text-only correction: `JEB (client probed: typed refusal, no engine). Engine installs are operator-owned.` No corpus or PROVINCE edits were made.

## 4. Vyper evidence spot-check — REPRODUCED

Sources re-read: corpus entry `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:3,12,19-23`; planted set `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json:23-39`; recorded probe envelopes at `.../EX-04/evidence/probe/probe-6.4.0-hex.json:1` and `probe-6.7.0-hex.json:1`; binary inputs `.../EX-04/out/runtime.bin` and `runtime.hex`. I independently parsed the saved evidence and hashed the local carrier; I did not claim a new REA invocation or target execution.

Fresh calculation output:

```text
planted selectors: 15 unique=True
runtime binary: bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0
hex-decoded runtime: bytes=1562 sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 exact_binary_match=True
6.4.0: functions=15 unique=15 recovered=15/15 missing=[] extra=[] dispatch=['abi'] sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 sha_matches_runtime=True
6.7.0: functions=15 unique=15 recovered=15/15 missing=[] extra=[] dispatch=['abi'] sha256=57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0 sha_matches_runtime=True
```

Independently ran `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/dispatch-census.py` against the checked-in runtime, planted set and 6.4.0 envelope. Its output: `runtime bytes: 1562`; table at `0x600` (`13 buckets x 2 B`, 26-byte tail); `leg chains (17 legs)`; `execution reached the leg-derived body: 15/15`; probe/derived offset `agreement: 15/15`; `probe set == leg-chain set: True`; no probe extras or leg-chain-only selectors. The byte prologue begins `5f3560e01c6002600d820660011b61060001601e395f5156`, consistent with selector modulo 13 and a copied jump table. Every one of the 15 reported offsets is not a JUMPDEST, matching the entry's fall-through-body convention (`dispatch-census.py` output; parser implementation `dispatch-census.py:176-211,222-237`; corpus statement `...vyper-leg.md:21-22`). The scanner's two raw PUSH4-byte candidates include `69656e74`; the corpus explains at `...vyper-leg.md:23` that this is a substring in a PUSH32 payload, not a selector, so I did not count it as a recovered dispatch.

## C1 disposition

All Command A counts and the three landed-tree gates reproduce. The Vyper 15/15 set, decoded runtime identity and modulo-jump-table shape reproduce from the entry's evidence. **One discrepancy remains:** `JEB (unprobed)` is still present at `PROVINCE.md:88`, making the nine-literal-absence claim false at HEAD. The custody selftest passes, but its documented invocation must use the `selftest` subcommand, not `--selftest`.
