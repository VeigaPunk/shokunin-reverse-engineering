# CN-4 — arc3-loop1-round10 convergence verdict

**Chain:** verdicts/convergence (`claims-frozen.md:67-72`). I re-derived the measurements below from immutable source revisions, pinned package code, and scratch runs under `/var/tmp`; peer measurements are not used as evidence. I wrote only this artifact. No Git mutation was performed.

## Revision controls

I ran SCORECARD Command A (`SCORECARD.md:88-124`) against the frozen records HEAD and the named work revision, using their Git objects:

```json
{"revision":"5694506a862c32d2f7aac44935778bce4b6184f2","knowledge_files":88,"mapped":88,"missing":[],"dangling":[],"rule_blocks":15,"citation_resolved_rules":15}
{"revision":"eb5a2c4af9d910bb7a3d4fced780f4641e341a24","knowledge_files":88,"mapped":88,"missing":[],"dangling":[],"rule_blocks":15,"citation_resolved_rules":15}
```

These are before-state controls, not after-landing results. The protected source paths (gate, corpus/map, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`) match HEAD; no claim landing is present.

## C1 — coverage / one corpus Unknown

**REPRODUCED — bounded `inspect_rust_binary` Evidence-ID result. UNVERIFIABLE — selected corpus/map landing and 88→89 after-state.**

I recommend EX-4’s distinct-verb-family candidate over merging the overlapping Vyper variants. The existing r7 Evidence-ID draft scopes its formula to `inspect-evm-interface` (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9,26`); the existing Rust entry documents `.dep-v0`/compiler-path findings, not this operation’s ID formula (`corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:7-10`). This makes EX-4 a separate, bounded Unknown rather than a second measurement of the same EVM claim.

I independently ran cached `rea-agents` CLI 6.7.0 `inspect-rust-binary /usr/bin/rustc --format json --full-output` twice, then ran it on two byte copies under separate `/var/tmp` paths. All three files hashed to `c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136` (5,240 bytes). Both same-path calls returned `ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256`; copyA and copyB returned respectively `ev_a256865748212808e167c2ddbe49f6ccd1b8ff9b45c10dec0d86b64741894288` and `ev_14b0ea3c8f97d23ce5cb58abec0f2d2301294f45a2c3b5c1e53f9eb761223004`. Each full returned Evidence envelope reported `confidence=observed`, `authority=shipped-artifact`.

I recomputed all four IDs from their full envelopes using the package’s semantic projection and canonical JSON/SHA-256 behavior: all four matched. Mutating only `subject.name` and `subject.local_path` left the base ID unchanged; substituting only `parameters.path`, `normalized_result.artifact.path`, and the `artifact-path` location reproduced copyA’s ID. The host package source hashes were independently checked: `evidence.js` `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` (`:159-183`), `canonicalDigest.js` `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` (`:8-25,60-76`), and `RustBinaryService.js` `81c34f68609df323124f1c27f2525fc80ae2fcf4dccc02e711b7f477ce189c5d` (`:55-80`). Those sources show the scoped projection and path-bearing semantic fields; the probe did not execute the target. The observed absence of `.dep-v0` does not establish absence of dependencies.

The frozen after-condition remains **UNVERIFIABLE**: no corpus entry or Rust-row map token is landed, and both immutable revisions still measure 88 files / 88 mapped. Integrate only one C1 draft and its map token together, then require Command A to report 89 files, 89 mapped, and empty missing/dangling sets.

## C2 — depth / queue-drain rule #16

**REPRODUCED — baseline and in-memory projection. UNVERIFIABLE — landed rule.**

I extracted SC-2’s exact proposed “Co-land every truth dependency” bullet, inserted it in memory into HEAD’s Queue-drain craft section, and applied Command A’s rule split and citation-range resolver. The before result was 15 rule blocks / 15 resolved; the projection was 16 / 16. The new references resolve within the immutable files: `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` (63 lines), `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-6` and `:17` (17 lines). No `SKILL.md` edit was made; 16/16 is a projection only.

I also checked the coupling examples directly: the r4 landing diff contains the PROVINCE/map changes and added r4 entry (`40de383`); the r8 diff contains the gate, receipt, PROVINCE/map changes and added r8 entry (`53fcf0c`). Correct SC-2’s r4 shorthand before integration: the r4 plan labels the Vyper split variant under F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187`), while the r4 verdict says the F5b wording depends on C1’s corpus landing (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`). Use “Vyper-dependent Frontier wording” rather than treating either hunk label as unambiguous. The dependency principle is supported; the actual rule remains draft-only. After landing, require Command A to report 16 blocks and 16 citation-resolved rules.

## C3 — operability / G21 append-past-register gap

**REPRODUCED — current gap and scratch candidate behavior. RESIDUAL — `+` bullet bypass.**

The current gate SHA-256 is `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`; `PROVINCE.md` ends at line 162, and the G21 register’s final span is `:161-162` (`.ufo/gates/c1-census-v10.py:292-308`, `PROVINCE.md:161-162`). `frontier_check()` checks only declared spans (`gate:422-444`), and the current gate bullet matcher excludes `+` (`gate:318`). On clean scratch input the source gate returned exit 0 / PASS, 14 rows, no frontier errors. I then appended an unregistered Markdown bullet at line 163, separately using each marker `-`, `*`, and `+`; all three source-gate cases still returned exit 0 / PASS with no errors.

I applied RV-1’s patch text only to scratch (`claims/c3/RV-1/evidence/g21-frontier-coverage.patch`; `patch --batch -p1` exit 0). Its clean control remained PASS; seeded `-` and `*` cases each failed at line 163 with `FRONTIER-UNEVALUABLE`, exit 1. The seeded `+` case still passed silently, exit 0. The patched gate passed `py_compile`. I also extracted and applied PL-4’s fenced patch only in scratch (`patch --batch -p0` exit 0; `py_compile` exit 0); it has the same `+` bypass. Thus the tested dash case is closed, but neither patch as written satisfies the full Markdown-bullet scope. This agrees with VZ-1’s identified residual and narrows the positive evidence to the exact seeded cases I ran.

**Recommendation:** revise RV-1’s guard to recognize all three Markdown markers (`[-*+]`), retain its missing/duplicate-heading failure behavior, and update the now-stale residual statement at gate lines 113-116 in the same integration. Re-run clean plus line-163 `-`, `*`, and `+` scratch cases; accept only if clean stays PASS and all three seeds fail as unevaluable. The present tests do not establish coverage for prose or claims inserted inside a registered span. No live gate or custody source was changed.

## Reconciliation and one integration recommendation

The peer artifacts offer competing drafts, not landed outcomes: VZ-1 recommends a K8 Vyper candidate for C1 and identifies the C3 marker residual; CR-5 correctly distinguishes current baselines from after-states and flags EX-8’s duplicated locator (`claims/c1/EX-8.md:27,29`). I independently re-derived the figures above and do not use peer-reported numbers. My single integration recommendation is: select EX-4 as the one C1 Unknown and land its entry/map token together; use SC-2’s dependency-coupled rule after neutralizing its r4 label; and integrate a revised RV-1 guard only after the `+` case and stale gate text are fixed. Then measure Command A at the landing revision (89/89 coverage and 16/16 depth) and record the scratch G21 marker matrix alongside the gate change.

Every scratch tree created for the re-runs described above was under `/var/tmp` and removed after its run. No corpus, map, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, gate, custody path, LOG, or peer artifact was changed.