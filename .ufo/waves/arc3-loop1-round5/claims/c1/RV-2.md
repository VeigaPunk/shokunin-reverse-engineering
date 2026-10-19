# RV-2 — C1 calibration sweep

Seat RV-2, chain c1. Re-derived against immutable Git objects and the landed tree; no prior seat's reported result was used as a measurement. Scope follows `claims-frozen.md:17-33`.

## Results

| Check | Verdict | First-hand result / evidence |
|---|---|---|
| Command A at named work commits and landed HEAD | **REPRODUCED** | Re-ran the recipe in `SCORECARD.md:88-124` (reads Git objects with `git show` / `git ls-tree`). Exact JSON stdout: |

```text
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "fbbbd45", "rule_blocks": 13}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "28aa7a9", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "c418be0", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "5be4a26", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "520341d", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "40de383", "rule_blocks": 14}
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 84, "mapped": 84, "missing": [], "revision": "71668cc", "rule_blocks": 14}
```

`520341d` is 83/83; the subsequent `40de383` tree is 84/84. Thus the new knowledge file is present in the latter, not the former. All tested mapped/file counts and rule counts reproduce; no missing or dangling tokens.

| Check | Verdict | First-hand result / evidence |
|---|---|---|
| Custody-pair selftest | **REPRODUCED** | The frozen spelling `python3 .ufo/gates/custody-pair/custody-pair.py --selftest` is not accepted: argparse printed `usage: custody-pair.py [-h] {capture,verify,selftest,paths} ...` and exited 2 (`cmd` is required). The script's subcommand form was run with scratch outside `/tmp`: `TMPDIR=/var/tmp python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (exit 0). All 28 case lines reported PASS.
| Citation-drift probe, normal mode | **REPRODUCED** | `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; process exit 0.
| Citation-drift probe, strict mode | **REPRODUCED** | `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; process exit 0.
| Census v10 at landed HEAD | **REPRODUCED** | `TMPDIR=/var/tmp python3 .ufo/gates/c1-census-v10.py --root .` → `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; process exit 0. Live anchors re-derived as Devin 6.5.0, OMP 6.5.0, Kimi 6.7.0.
| PROVINCE line hold | **REPRODUCED** | `wc -l PROVINCE.md` → `162 PROVINCE.md`; `PROVINCE.md` has no working-tree diff.
| Nine stale-literal absences | **DISCREPANCY** | Exact-literal searches against current `PROVINCE.md`: no matches for `Reserve: 91MB Godot ARM64 template`, `all 3 organic cores`, `real solc/vyper-compiled bytecode untested`, `Next: raise \`REA_GHIDRA_STARTUP_TIMEOUT_MS\``, `probe-refused since r2`, `pacman pairs beyond expac unexercised`, `absent: \`7z\``, or `35 features incl. PyGhidra/BSim`. But `JEB (unprobed)` **does match** at `PROVINCE.md:88` (`JEB (unprobed). Engine installs are operator-owned.`), so 8/9 absences reproduce and the all-nine claim does not. Search was performed with the dedicated Grep tool using literal needles (regex metacharacters escaped), not a shell `grep -F` invocation.
| Vyper entry: 15/15 K/K | **VERIFIED** | Entry claim at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:12,19`; independent expected selectors in `.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json:23-39`. A first-hand Python parse compared the planted set to each RV-2 envelope at `.ufo/waves/arc3-loop1-round4/claims/c1/RV-2/evidence/my-probe-carrierV-{hex-6.4.0,raw-6.4.0,hex-6.7.0}.json:1`: each has 15 functions, 15 unique selectors, exact-set equality, no missing/extra selector, and 15 `dispatch: abi` results.
| Vyper runtime SHA-256 | **VERIFIED** | First-hand hash of `.../EX-04/out/runtime.bin`: 1,562 bytes, SHA-256 `57d6fd0ae0da001975a3f58ae72804757aa36267f6e373bf9f134ecc9791dae0`. Decoding `.../EX-04/out/runtime.hex` gives the same 1,562 bytes and hash. All three RV-2 envelopes' `normalized_result.bytecode.sha256` values match.
| Vyper dispatch shape | **VERIFIED** | Re-ran `python3 .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/dispatch-census.py .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json .ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json` (`dispatch-census.py:16,171-237`). Output: `assumed jump table at 0x600 (13 buckets x 2 B)`, `execution reached the leg-derived body: 15/15`, `agreement: 15/15`, `probe set == leg-chain set: True`, no probe extras or leg-only selectors. The 13 table entries point to `0x5b` JUMPDESTs; empty sentinel `0x5e7` occurs at buckets 1, 7, and 11. All 15 compare legs have `shape_ok=True` for `JUMPDEST PUSH4 DUP2 XOR PUSH2 JUMPI`; all reported offsets are the fall-through body entries, not JUMPDESTs. This supports the entry's modulo-13 table / XOR-chain description (`...vyper-leg.md:21`).

## Scope / write record

Only this seat artifact was written. Git was not mutated. The initial and final status showed the existing modification `M .ufo/waves/arc2-loop1-round10/C3.md`; `PROVINCE.md` remained unmodified. The stale-literal finding is the sole discrepancy found in this C1 pass.