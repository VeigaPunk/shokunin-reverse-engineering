# VZ-4 — arc3-loop1-round10 convergence verdict

Independent reconciliation of frozen C1–C3 (`claims-frozen.md:16-65`). I re-ran Command A at both measured revisions, reran the EX-4 REA probes and its ID recomputation, projected EX-12’s proposed C2 rule in memory, and tested RV-1’s patch on scratch copies. Git remained read-only. The only authorized write is this verdict artifact.

## Revision and controls

- `HEAD` = `5694506a862c32d2f7aac44935778bce4b6184f2`; work parent = `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`.
- Command A from `SCORECARD.md:88-124`, run against immutable Git objects, returned:

  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "eb5a2c4af9d910bb7a3d4fced780f4641e341a24", "rule_blocks": 15}
  ```

- `git diff --quiet -- .ufo/gates/c1-census-v10.py corpus/knowledge corpus/README.md SKILL.md PROVINCE.md SCORECARD.md LOG.md` exited `0`. The pre-existing status remained `M .ufo/waves/arc2-loop1-round10/C3.md` and `?? .ufo/waves/arc3-loop1-round10/`; neither was altered. No canonical C1/C2/C3 source change is present.

## C1 — coverage / one corpus Unknown

**REPRODUCED — EX-4’s bounded `inspect_rust_binary` ID result. UNVERIFIABLE — selected corpus/map landing and 88→89. CANDIDATE CHOICE — not converged.**

I ran four cached REA 6.7.0 calls using the `EX-4` reproduction recipe (`claims/c1/EX-4/evidence/rederive-commands.txt:1-15`): two `inspect-rust-binary /usr/bin/rustc --format json --full-output` calls, then the same operation on two byte-identical copies created under `/var/tmp`. All four exited 0. `sha256sum` returned `c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136` for `/usr/bin/rustc` and each copy; each report said 5,240 bytes. Exact IDs from this run:

```text
base1 /usr/bin/rustc: ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256
base2 /usr/bin/rustc: ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256
copyA: ev_126c383f001f4e7543da6d0b901f5129fcfe95f5fb5083fa8b6c5a8c12ef5ef4
copyB: ev_6968513dc5e4345e59dd7332c35ea6f7561e353dc65ae02bbf328efbdb61e9b8
```

The scratch copy IDs vary with their paths; the same-path reruns agreed, while same-byte copies at distinct paths differed. I also ran `node .ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids.mjs`: all four retained envelopes’ reported IDs matched recomputation; changing only `subject.name`/`subject.local_path` kept the base ID; substituting the path-bearing semantic fields reproduced the retained copyA ID (`claims/c1/EX-4/evidence/recompute-ids.mjs:14-35,48-68`). The installed package implementation agrees: `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js:159-183` hashes a semantic projection; `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js:8-25,60-76` supplies canonical SHA-256. The Rust service adds path-bearing parameters/result/location fields (`claims/c1/EX-4.md:13-16`; package version/path and hashes in `claims/c1/EX-4/evidence/identity.txt:1-13`).

This is a result for `inspect_rust_binary` in the cached 6.7.0 package, on one ELF byte identity and two alternate paths. It does not establish other REA verbs/releases, artifact formats, all Evidence fields, or runtime behavior. The frozen candidate and proposed corpus/map token are identified at `claims/c1/EX-4.md:1-5,23-30`; neither is canonicalized.

**Candidate disagreement and recommendation:** VZ-1, VZ-3, CR-6, and CN-3 support EX-3’s three-target K8 Vyper draft; CR-8 selects EX-2’s solc-viaIR candidate. VZ-2 and CN-4 independently reran EX-4 and recommend its distinct `inspect_rust_binary` Unknown; this seat also reran it. CR-5/CR-7 report no consolidated choice. These are alternatives, not additive closures. EX-3 has the broadest multi-target peer re-derivation, while EX-4 directly closes a separate verb-family gap with package-source support. VZ-4 recommends EX-4 as the single C1 entry, but this is not unanimous convergence: EX-3 and EX-2 remain supported alternatives. Whichever candidate is chosen, only one entry plus its map token satisfies C1, and Command A must then be rerun for 89 files / 89 mapped with empty missing/dangling sets.

**Locator and inventory corrections:** CR-5’s EX-8 warning (`claims/verdicts/CR-5.md:23`) is not reproduced against the current artifact. `claims/c1/EX-8.md:27-29` contains one repository-root-relative `.ufo/waves/.../EX-8/` prefix, not a duplicated prefix; I checked that both `evidence/HardforkVault.vy` and `evidence/rederive.sh` resolve from the repo root. VZ-2, VZ-3, and CN-3 independently report the locator correction (`claims/verdicts/VZ-2.md:42`; `VZ-3.md:27`; `CN-3.md:28`). VZ-2 also notes that CR-5’s C1 artifact inventory at `:21` omits the now-present EX-2, EX-6, and CR-3 reports (`VZ-2.md:42`); treat it as a stale snapshot, not a current exhaustive list.

## C2 — depth / Queue-drain rule #16

**REPRODUCED — baseline and EX-12 parser projection. UNVERIFIABLE — landed 16/16 rule.**

The exact Command A outputs above establish 15 rules / 15 citation-resolved at HEAD and the work commit. I extracted EX-12’s exact proposed bullet and projected it into HEAD’s Queue-drain section in memory, using Command A’s `^- \*\*` rule split and citation-range resolver. Output:

```json
{"source_revision":"5694506a862c32d2f7aac44935778bce4b6184f2","selected_draft":"EX-12 proposed rule text (exact one-line quote, memory only)","baseline":{"rule_blocks":15,"citation_resolved_rules":15},"in_memory_projection":{"rule_blocks":16,"citation_resolved_rules":16},"projected_text_includes_r4_F5b_label":false,"projection_only":true}
```

I recommend the majority dependency-coupled rule rather than EX-10’s pointer sensitivity or EX-14’s dispatcher-prologue topic. EX-12’s rule body is parser-compatible; its supporting evidence at `claims/c2/EX-12.md:15` calls the r4 dependency “F5b↔C1,” while EX-9 explicitly distinguishes F5b from a C1-coupled F5c variant (`claims/c2/EX-9.md:15`). The underlying record is more nuanced than a single label correction: the frozen claim and r4 cross-chain verdict use F5b (`claims-frozen.md:36-39`; `.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`); PL-2’s plan lists F5b as the “real solc/vyper-compiled bytecode untested” row and F5c as “selectors stay bare hashes” (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187`). Its optional Vyper-naming variant is explicitly labeled F5c and conditional on C1 (`:255-259`; `candidate-coupled-vyper.patch.md:217-224`). The actual r4 commit diff changes the F5b wording to name the Vyper carrier and adds the r4 corpus entry in the same commit. Thus preserve the frozen F5b provenance, recognize the separate F5c variant, and state the rule generically as “Vyper wording ↔ C1 evidence” rather than collapsing the two.

The immutable tree checks confirm coupled examples: commit `40de38343398eee72aeebad7429f3bb99ab0a8dd` changes `PROVINCE.md` and `corpus/README.md` while adding the r4 Vyper entry; `53fcf0caca7255f730fe1a1f17aefd00203a2978` changes the gate, receipt, `PROVINCE.md`, and README while adding the r8 entry. The r8 corpus text still calls its entry/map and after-count pending (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-17`); historical co-landing is evidence for the rule, not a current 16-rule result. No `SKILL.md` edit landed. **UNVERIFIABLE:** accept rule #16 only after one selected rule lands and Command A returns 16 blocks with all citations resolved at that commit.

## C3 — operability / G21 appended-Frontier guard

**REPRODUCED — existing line-163 gap and RV-1 dash/star closure on scratch. PARTIAL — plus-marker bypass. UNVERIFIABLE — live gate change.**

The live gate has 14 fixed rows (`.ufo/gates/c1-census-v10.py:292-308`); the last declared span is `PROVINCE.md:161-162`. `frontier_check()` tests those registered spans (`:422-444`), and current `BULLET` is `re.compile(r"^\s*[-*] ")` (`:318`). I applied RV-1’s exact patch (SHA-256 `c0e9e9ca69031e973b872e70ac68548697117eaec7dd7b2ad5e1118b21f4493c`) only to copies under `/var/tmp`, then ran clean and line-163 marker cases:

```json
{"case":"source-clean","exit_code":0,"verdict":"PASS","frontier_rows":14,"frontier_errors":[],"declared_fail_classes":[]}
{"case":"source-dash","exit_code":0,"verdict":"PASS","frontier_rows":14,"frontier_errors":[],"declared_fail_classes":[]}
{"case":"candidate-clean","exit_code":0,"verdict":"PASS","frontier_rows":14,"frontier_errors":[],"declared_fail_classes":[]}
{"case":"candidate-dash","exit_code":1,"verdict":"FAIL","frontier_rows":14,"frontier_errors":["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"],"declared_fail_classes":["FRONTIER-UNEVALUABLE"]}
{"case":"candidate-star","exit_code":1,"verdict":"FAIL","frontier_rows":14,"frontier_errors":["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"],"declared_fail_classes":["FRONTIER-UNEVALUABLE"]}
{"case":"candidate-plus","exit_code":0,"verdict":"PASS","frontier_rows":14,"frontier_errors":[],"declared_fail_classes":[]}
```

This confirms RV-1 closes the tested `-` and `*` cases while a valid Markdown `+` bullet escapes because the patch reuses the `[-*]` matcher. Add `+` recognition and rerun the clean / `-` / `*` / `+` matrix before accepting the generic frozen “new Frontier bullet” claim. The patch also tests range membership, not exact registered bullet starts; insertion inside a registered span and non-bullet text were not tested here (`claims/verdicts/CR-5.md:57`; RV-1 patch at `claims/c3/RV-1/evidence/g21-frontier-coverage.patch:24-27`). Other drafts are not substituted for my tested patch; CR-8 separately reports PL-3’s dash case only (`claims/verdicts/CR-8.md:36-38`). No live gate change is claimed.

## Per-item disposition

- **C1:** EX-4’s narrow ID behavior **REPRODUCED**; C1 candidate selection **NOT CONVERGED**; 89/89 coverage after-state **UNVERIFIABLE** until a single corpus entry and map token land.
- **C2:** baseline and EX-12 in-memory projection **REPRODUCED**; r4/r8 coupling evidence **VERIFIED** with the F5b/F5c distinction above; integrated rule #16 **UNVERIFIABLE**.
- **C3:** append-past-register gap **REPRODUCED**; RV-1 patch closure for `-`/`*` **REPRODUCED on scratch**; `+` bypass **REPRODUCED**; full closure and live gate change **UNVERIFIABLE**.

The record remains incomplete: no canonical C1 or C2 after-state and no live C3 patch is present. No source, corpus, map, gate, custody, `PROVINCE.md`, `SCORECARD.md`, or `LOG.md` file was changed by VZ-4; scratch was confined to `/var/tmp` and removed after testing.