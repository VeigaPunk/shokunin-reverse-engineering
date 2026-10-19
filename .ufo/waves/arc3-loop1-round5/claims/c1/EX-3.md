# EX-3 — C1 correctness sweep

Scope: the six C1 checks in `claims-frozen.md:20-27`. Every value below was re-derived in this seat from the named Git objects, gate runs, source files, or shipped-bytecode evidence; prior-round numeric results were not used as proof.

## Results

1. **Command A — REPRODUCED.** Re-ran the `SCORECARD.md:88-124` recipe against all six named Git objects. Each had empty `missing`/`dangling` sets and scores 10.0/10.0.

   | Revision | Mapped / knowledge files | Resolved / rule blocks |
   |---|---:|---:|
   | `fbbbd45` | 82/82 | 13/13 |
   | `28aa7a9` | 82/82 | 14/14 |
   | `5be4a26` | 83/83 | 14/14 |
   | `c418be0` | 83/83 | 14/14 |
   | `520341d` | 83/83 | 14/14 |
   | `40de383` | 84/84 | 14/14 |

   Git parents clarify the round shorthand: `5be4a26` is a hygiene child of `c418be0`, while `520341d` is the direct parent of `40de383`. All six objects were measured; the grouped labels in the frozen scope should not be treated as a linear round ancestry. Evidence: `EX-3/evidence/command-a.jsonl`, `EX-3/evidence/command-a-topology-and-province.txt`.

2. **Custody-pair selftest — REPRODUCED.** `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /dev/shm` ended `CLEAN cases=28 passed=28 failed=0 exit=0`. Evidence: `EX-3/evidence/custody-pair-selftest.out` and `.exit`.

3. **Citation-drift probe, default and strict — REPRODUCED.** At HEAD, default reported `findings=0 exit=0`; strict reported `clean findings=0 exit=0`. Evidence: `EX-3/evidence/citation-drift-{default,strict}.out` and matching `.exit` files.

4. **Census v10 — REPRODUCED.** `python3 .ufo/gates/c1-census-v10.py --root .` returned PASS with stale/ambiguous/undeclared/unresolved all zero; scope errors and unreadable lists were empty. It reports scoped line counts PROVINCE 162, SCORECARD 1631, SKILL 390. Evidence: `EX-3/evidence/census-v10.out` and `.exit`.

5. **PROVINCE line hold and nine stale literals — DISCREPANCY.** The current `PROVINCE.md` has 162 lines; the six tested commit objects also each have 162. Eight exact stale needles are absent (`Reserve: 91MB Godot ARM64 template`, `all 3 organic cores`, `real solc/vyper-compiled bytecode untested`, `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\``, `probe-refused since r2`, `pacman pairs beyond expac unexercised`, `absent: \`7z\``, `35 features incl. PyGhidra/BSim`). The ninth, `JEB (unprobed)`, remains at `PROVINCE.md:88`. The capability matrix records an `inspect-jeb-client` attempt and `fetch failed` at `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:99`; that does not establish a reachable JEB service, but it does contradict the required literal-absence check. Evidence: `EX-3/evidence/province-literal-scan.txt` and `EX-3/evidence/command-a-topology-and-province.txt`. Exact escaped-pattern Grep queries were used along with the persisted literal scan; shell `grep -F` was not invoked because shell grep/rg is disallowed by the tool policy.

6. **Vyper entry spot-check — DISCREPANCY.** The selector count, runtime identity, and dispatcher structure were independently checked. The ABI contains 15 function entries; two separate Keccak implementations (Python and Node), each passing canonical Ethereum test vectors, derive the same 15 selectors as planted K and the fresh REA 6.4.0/6.7.0 results. The decoded runtime is 1,562 bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`; the 3,124-byte hex carrier hashes to `e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192`. Independently decoding the prologue and following the XOR compare legs found 13 two-byte entries (26 bytes) at `0x600`; all 13 targets are JUMPDESTs, all 15 selectors reach the matching leg body, and all 15 REA offsets match.

   The wording at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:21` says the runtime copies the 13-entry table to memory. Correction: the table is stored at the runtime tail, but the dispatcher computes `0x600 + 2*(selector % 13)` and `CODECOPY`s only the selected **two-byte entry** to memory offset `0x1e` (the retained `PUSH1 0x02` supplies the copy length), then loads that entry and jumps. Four buckets contain selector chains; three are empty. The remaining spot-checked claims reproduce. Evidence: `EX-3/evidence/vyper-selector-rederive.txt` and `.exit`, `EX-3/evidence/vyper-table-independent.txt` and `.exit`, the fresh mini-EVM rerun `EX-3/evidence/vyper-dispatch-census.out` and `.exit`, and `EX-3/evidence/vyper-rea-6.4.0.json` / `.exit` plus `EX-3/evidence/vyper-rea-6.7.0.json` / `.exit`.

Static bytecode inspection only; no runtime execution, deployment identity, or reachable JEB service is claimed.