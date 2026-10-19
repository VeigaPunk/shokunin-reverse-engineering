# VZ-2 — arc3-loop1-round10 reconciliation verdict

**Measured against:** records `HEAD=5694506a862c32d2f7aac44935778bce4b6184f2`; work revision `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`.  
**Verified:** 2026-10-19.  
**Write boundary:** this verdict only. Gate, custody paths, corpus, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, and peer artifacts were not edited. All new scratch was under `/var/tmp` and removed; Git was read-only.

## Disposition

**Integration HOLD; judge the claims separately.** C1's distinct `inspect_rust_binary` Unknown is reproduced on the measured REA 6.7.0 operation, but no corpus entry or map token landed, so the frozen 88→89 condition is not met. C2 has a parser-compatible rule-16 draft and a 16/16 in-memory projection, but the live craft section remains 15/15. C3's proposed guard catches the dash and star line-163 probes on scratch, but silently accepts a valid plus-marker bullet; the broad append-past-register claim is therefore only partially reproduced. The live gate remains PASS and unchanged. These findings are not a scalar pass.

## Revision and source-derived baseline

I reran Command A from `SCORECARD.md:88-124` against both immutable Git trees. Exact outputs:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
```

A fresh `python3 .ufo/gates/c1-census-v10.py --quiet` at `HEAD` returned `PROVINCE.md lines=162`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS`, exit 0. The gate SHA-256 is `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`.

## C1 — coverage / one named corpus Unknown

**REPRODUCED — bounded second-verb Evidence-ID result. UNVERIFIABLE — selected corpus/map landing and 88→89 after-count.** The frozen claim allows the `ev_` ID domain for a different verb family (`claims-frozen.md:16-29`). The prior EVM record explicitly limits its formula to `inspect-evm-interface` and says other operations are outside scope (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9,11,26`).

I freshly ran the cached REA CLI (`6.7.0`) with `inspect-rust-binary <path> --format json --full-output` twice on `/usr/bin/rustc`, then on two same-byte copies in `/var/tmp`. Every input hashed to `c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136` (5,240 bytes). Each returned ID matched an independent recomputation of the complete Evidence envelope's semantic projection:

```text
REA_VERSION=6.7.0
base1 /usr/bin/rustc  ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256  recomputed=match
base2 /usr/bin/rustc  ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256  recomputed=match
copyA same SHA-256    ev_f366ab8fbc8d4cdf6d3f10428e696ea52c6fcbeddfd0fa30ac9a66fdd8c7dfea  recomputed=match
copyB same SHA-256    ev_a51a49014f91511fbf9d5452fbf78b675a9fe95f344ae79e60da143dd2e3981e  recomputed=match
display_fields_mutation_preserves_id=true
path_fields_only_mutation_matches_copyA=true
```

The fresh copy IDs differ from EX-4's retained IDs because the copied paths differ; the package includes semantic path fields. This is not a conflict: `dist/domain/evidence.js:159-183` projects the evidence, `dist/domain/canonicalDigest.js:8-25,60-76` hashes compact canonical JSON, and `dist/application/rust/RustBinaryService.js:55-80` places the selected artifact path in parameters, normalized results, and locations. This establishes the formula for this `inspect_rust_binary` case on cached REA 6.7.0—not all REA operations or versions, formats, failures, or field variations. The binary was statically inspected, not executed.

**Candidate selection:** I recommend EX-4's single proposed entry `2026-10-19-arc3-r10-rust-evidence-id-domain.md` and matching Rust-row token (`claims/c1/EX-4.md:1,11-15,19-24`; map location `corpus/README.md:63`). EX-4 addresses the frozen different-verb candidate and supplies package-source inspection plus recomputed IDs. VZ-1 instead recommends EX-3's bounded K8 Paris/Cancun/Prague Vyper entry (`claims/verdicts/VZ-1.md:7-15`); that is a viable but different Unknown, not evidence against EX-4. Select one C1 entry and one token; do not combine the overlapping drafts. I did not re-run the peer Vyper compiler matrices and do not adopt their numeric results as my measurements.

At the refreshed inventory, C1 has 10 top-level seat reports: EX-2..EX-8, CR-1, CR-3, and CR-4; no top-level EX-1.md or CR-2.md report was present (their evidence directories exist). C2 and C3 each have 12 reports. CR-5's C1 list at `claims/verdicts/CR-5.md:21` omits the now-present EX-2, EX-6, and CR-3, so it is not a current exhaustive inventory. Its EX-8 locator objection at `:23` also does not match the current `claims/c1/EX-8.md:27,29`: those lines contain one repository-root-relative path each, and both referenced evidence files exist.

## C2 — depth / Queue-drain rule #16

**REPRODUCED — starting baseline and in-memory projection. UNVERIFIABLE — landed rule and 16/16 committed after-state.** Command A above confirms 15 rule blocks and 15 citation-resolved rules at both revisions. The 12 C2 reports mostly converge on dependency-coupled landing (10/12); EX-16 states the complete-set/consumer-check rule at `claims/c2/EX-16.md:5-9`, and SC-1 provides a concrete rule and citation list at `claims/c2/SC-1.md:26-38`. EX-10 proposes a distinct perishable-pointer rule (`claims/c2/EX-10.md:5-18`); EX-14 proposes following a full dispatcher and terminal miss path (`claims/c2/EX-14.md:27-38`). These are alternatives, not changes already in `SKILL.md`.

I projected SC-1's exact proposed bullet into the immutable HEAD Queue-drain craft text in memory, then used Command A's rule split and citation-range resolver. Output:

```json
{"before":{"citation_resolved_rules":15,"rule_blocks":15},"in_memory_projection":{"citation_resolved_rules":16,"rule_blocks":16},"new_rule_citations_resolve":true,"new_rule_refs":[{"lines":63,"path":"2026-10-19-arc3-r4-evm-vyper-leg.md","range":[30,30],"valid":true},{"lines":63,"path":"2026-10-19-arc3-r4-evm-vyper-leg.md","range":[34,57],"valid":true},{"lines":17,"path":"2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md","range":[17,17],"valid":true},{"lines":76,"path":"2026-10-13-ghidra-install.md","range":[71,76],"valid":true}],"source_revision":"5694506a862c32d2f7aac44935778bce4b6184f2"}
```

The r4 example's label is inconsistent across records: the frozen shorthand says “F5b↔C1” (`claims-frozen.md:37-38`); the r4 plan labels the specifically Vyper-dependent patch `candidate-coupled-vyper` under the F5c split (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`); the cross-chain verdict calls the dependency F5b (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`). State the underlying Vyper-scope dependency, not an unqualified F5 label. The coupled commit contents independently rechecked with `git diff-tree` were:

```text
r4 40de38343398eee72aeebad7429f3bb99ab0a8dd:
M PROVINCE.md
M corpus/README.md
A corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md
r8 53fcf0caca7255f730fe1a1f17aefd00203a2978:
M .ufo/gates/c1-census-v10.py
A .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt
M PROVINCE.md
M corpus/README.md
A corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md
```

Use one dependency-coupled rule draft (SC-1 or EX-16), resolve the r4 label in prose, and rerun Command A on the actual landing revision. The projection above is not a committed after-measurement.

## C3 — operability / G21 append-past-register guard

**PARTIALLY REPRODUCED — the dash/star tail case; residual remains for plus bullets.** The frozen condition is an appended Frontier bullet beyond line 162 being flagged rather than silently accepted (`claims-frozen.md:51-65`). The current 14-row register ends at `PROVINCE.md:161-162` (`.ufo/gates/c1-census-v10.py:292-308`); its existing `BULLET` regex is `^\s*[-*] ` at `:318`. I copied the three inputs and gate to `/var/tmp`, applied PL-3's proposed patch only to scratch, and ran `python3 <scratch-gate> --root <scratch-root> --quiet` after appending each marker at physical line 163. Exact decisive output:

```text
source/clean: line_count=162 exit=0; FRONTIER register (G21): 14 rows asserted, errors: []; DECLARED FAIL CLASSES: []; VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
source/dash: line_count=163 exit=0; FRONTIER register (G21): 14 rows asserted, errors: []; DECLARED FAIL CLASSES: []; VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
source/star: line_count=163 exit=0; FRONTIER register (G21): 14 rows asserted, errors: []; DECLARED FAIL CLASSES: []; VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
source/plus: line_count=163 exit=0; FRONTIER register (G21): 14 rows asserted, errors: []; DECLARED FAIL CLASSES: []; VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
patched/clean: line_count=162 exit=0; FRONTIER register (G21): 14 rows asserted, errors: []; DECLARED FAIL CLASSES: []; VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
patched/dash: line_count=163 exit=1; FRONTIER register (G21): 14 rows asserted, errors: ["PROVINCE.md:163 unregistered bullet in '### Round-4 frontier (post-unlock)' (FRONTIER-UNEVALUABLE)"]; DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']; VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
patched/star: line_count=163 exit=1; FRONTIER register (G21): 14 rows asserted, errors: ["PROVINCE.md:163 unregistered bullet in '### Round-4 frontier (post-unlock)' (FRONTIER-UNEVALUABLE)"]; DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']; VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
patched/plus: line_count=163 exit=0; FRONTIER register (G21): 14 rows asserted, errors: []; DECLARED FAIL CLASSES: []; VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

PL-3's scan calls `BULLET.match` (`claims/c3/PL-3.md:104-108`), so `+` is missed by the shared `[-*]` expression. VZ-1 independently identified this plus-marker bypass (`claims/verdicts/VZ-1.md:27-35`); the scratch matrix above confirms it on PL-3 itself. Keep PL-3's fail-closed heading and exact registered-start approach as a candidate, but extend its matcher to include `+` and rerun clean, dash, star, and plus seeds before accepting the broad bullet-coverage claim. No patched gate, live gate, or custody path was changed.

## Integration boundary

No C1 entry/map token, C2 rule, or C3 instrument fix is present in the measured source tree. Do not report 89/89, 16/16, or a live G21 repair. The only durable deliverable from this seat is this verdict; no LOG or other seat file was changed.