# CN-1 — arc3-loop1-round10 reconciliation verdict

**Disposition:** recommend EX-4 as the single C1 landing, SC-2’s dependency-coupled rule as the single C2 landing, and a G21 section walk that recognizes `-`, `*`, and `+` bullets for C3. These are integration recommendations, not landed results. I did not edit corpus, map, SKILL, gate, custody, LOG, or other-seat files, and did not mutate Git.

## Revisions and independent controls

`git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`; `git rev-parse eb5a2c4` → `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. I re-ran SCORECARD Command A (`SCORECARD.md:88-124`) over both immutable trees. Each returned:

```text
knowledge_files=88, mapped=88, missing=[], dangling=[],
rule_blocks=15, citation_resolved_rules=15
```

I also ran `python3 .ufo/gates/c1-census-v10.py --root . --quiet`: exit 0 / PASS; `PROVINCE.md` is 162 lines, G21 reports 14 rows and no errors. The live gate SHA-256 is `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`.

## C1 — one corpus Unknown

### EX-4: independently reproduced; recommended

The frozen claim allows a second `ev_` verb family (`claims-frozen.md:18-25`). I freshly ran REA 6.7.0 `inspect-rust-binary` four times, with `TMPDIR` and byte-identical copies under `/var/tmp`:

```bash
REA=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents
S=/var/tmp/kaidoku-cn1-r10-rustc-check.W1KgKL
mkdir -p "$S/copyA" "$S/copyB"
cp /usr/bin/rustc "$S/copyA/rustc"; cp /usr/bin/rustc "$S/copyB/rustc"
export TMPDIR="$S"
node "$REA/scripts/rea.mjs" --version
node "$REA/scripts/rea.mjs" inspect-rust-binary /usr/bin/rustc --format json --full-output  # twice
node "$REA/scripts/rea.mjs" inspect-rust-binary "$S/copyA/rustc" --format json --full-output
node "$REA/scripts/rea.mjs" inspect-rust-binary "$S/copyB/rustc" --format json --full-output
sha256sum /usr/bin/rustc "$S/copyA/rustc" "$S/copyB/rustc"
```

Here `$REA` was `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents`; `$S` was `/var/tmp/kaidoku-cn1-r10-rustc-check.W1KgKL`. The four raw JSON envelopes and SHA-256 listing remain in that scratch directory.

Fresh results: both `/usr/bin/rustc` calls returned `ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256`; copyA returned `ev_9a3d629a1090dd970907bb7ee344026a18181f17005dc37098591dac2788684c`; copyB returned `ev_82df3e53e4c3687fc97f0dc1cf50dd81a88dfc1de79a7e3e668609db7103890a`. All four reports identify operation `inspect_rust_binary`, the same 5,240-byte artifact SHA-256 `c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136`, and each file hash independently matched.

I recomputed the IDs from the fresh full envelopes using the package projection and canonical SHA-256: all four matched. Mutating only `subject.name` / `subject.local_path` left the base ID unchanged; changing only the semantic path fields (`parameters.path`, `normalized_result.artifact.path`, and `locations[0].path`) to copyA’s path reproduced copyA’s ID. This matches the implementation at cached REA `dist/domain/evidence.js:159-183` and `dist/domain/canonicalDigest.js:8-25,60-76`; `RustBinaryService.js:55-80` supplies those path-bearing fields. Its package source hashes match `claims/c1/EX-4/evidence/identity.txt:5-9`. `RustBinaryProvider.js:21,38-60` describes an in-process read, not target execution.

**Bound and limits:** this verifies the Evidence-ID formula and path sensitivity for this operation, REA 6.7.0, and one ELF byte identity. It does not establish a universal rule for other verbs/releases or execute the target. The EX-4 draft correctly proposes one Rust-row token (`claims/c1/EX-4.md:1,11-16,26-30`), but corpus admission and the frozen 88→89 after-state remain **UNVERIFIABLE** until one entry and token land and Command A is rerun.

### Reconcile alternatives and status discrepancies

- **CORRECTED — EX-2 is not a new Unknown.** Its source SHA-256 is `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe` (`claims/c1/EX-2/evidence/compiler-identity.txt:2-5`), the same ViaIrVault source already used by R9 EX-5. R9 EX-5 measured solc 0.8.28 viaIR and its comparison with 0.8.37 (`.ufo/waves/arc3-loop1-round9/claims/c2/EX-5.md:7-9`); R9 VZ-2 independently records that source/settings result and the matching pre-metadata region (`.ufo/waves/arc3-loop1-round9/claims/verdicts/VZ-2.md:83-94`). This is a useful reproduction, but the frozen claim itself names 0.8.28 as already characterized, so EX-2 cannot close a fresh C1 Unknown.
- **Vyper hardfork drafts overlap.** EX-3, CR-4, and EX-5 use the same K8 source hash `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; EX-7 overlaps the Paris leg, EX-6 proposes a broader fork matrix, while EX-8 is a distinct fixture. VZ-1 and CR-6 independently re-derived EX-3’s Paris/Cancun/Prague result and prefer that Vyper candidate (`claims/verdicts/VZ-1.md:7-15`; `CR-6.md:13-21`). I did not rerun those compiler/REA measurements and do not represent them as CN-1 measurements. EX-4 is a separate frozen candidate, directly measured above, and avoids merging overlapping fork drafts into one claim.
- **DISCREPANCY — stale R7 landing sentence.** The existing R7 entry says its corpus file/map token have not landed (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:26`), but that file exists and the EVM coverage row maps `2026-10-19-arc3-r7-evm-evidence-id-domain` (`corpus/README.md:38`). The status sentence is stale; it does not characterize the different Rust verb or negate EX-4’s candidate.
- C1 roster check: 11 report files are present (CR-1–CR-4 and EX-2–EX-8); `claims/c1/EX-1.md` is absent. EX-1 has an evidence directory, but not a top-level report. The missing report does not affect the measured EX-4 result.

## C2 — Queue-drain depth

**REPRODUCED — SC-2 projection, not a landed rule.** The independent immutable-tree controls above establish 15 rules / 15 citation-resolved at HEAD and `eb5a2c4`. I inserted the exact SC-2 bullet (`claims/c2/SC-2.md:9`) into HEAD’s Queue-drain text in memory and applied Command A’s rule-splitting and citation-range logic: baseline 15/15; projection 16/16. The draft references resolve: R4 `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` (63 lines), and R8 `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-6,17` (17 lines). No `SKILL.md` was written; actual 16/16 remains **UNVERIFIABLE** pending integration and a fresh Command A run.

I independently checked the two earned dependency examples against their immutable commits. Commit `40de38343398eee72aeebad7429f3bb99ab0a8dd` includes both the R4 Vyper knowledge entry and PROVINCE/map changes. Commit `53fcf0caca7255f730fe1a1f17aefd00203a2978` includes the R8 gate extension, receipt, PROVINCE/map changes, and knowledge entry. One label needs correction in the rule’s supporting prose: the R4 cross-chain verdict/frozen shorthand says F5b, but the detailed plan identifies F5b as the real-solc item and the C1-dependent Vyper-naming hunk as F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`). State the dependency generically as **R4 Vyper wording ↔ C1 corpus entry** rather than perpetuating the label conflict.

The 12 C2 reports mostly converge on this dependency-coupled rule; EX-10’s pointer-specific rule and EX-14’s dispatcher-prologue rule are distinct alternatives. Recommend one generalized SC-2-style bullet only. The parser projection does not establish an integrated SKILL improvement.

## C3 — G21 operability

**REPRODUCED — current append-past-register gap.** The live gate fixes 14 Frontier rows (`.ufo/gates/c1-census-v10.py:292-308`) and `frontier_check()` tests only those declared spans (`:422-444`); the final span ends at PROVINCE lines 161-162. In a `/var/tmp` scratch copy I appended a new Markdown bullet at line 163. The unchanged gate returned PASS / exit 0 with no Frontier errors for each of `-`, `*`, and `+` markers.

**REPRODUCED — improved candidate on scratch only.** I tested a scratch-only gate variant that keeps the fixed-span checks, requires each exact named Frontier heading to occur once, scans those sections for unregistered bullets using `[-*+]`, and reports through `FRONTIER-UNEVALUABLE`. Results:

```text
case       unchanged gate       scratch candidate
clean      PASS / 0              PASS / 0
line 163 - PASS / 0              FAIL / 1 FRONTIER-UNEVALUABLE
line 163 * PASS / 0              FAIL / 1 FRONTIER-UNEVALUABLE
line 163 + PASS / 0              FAIL / 1 FRONTIER-UNEVALUABLE
```

Scratch inputs and the candidate are under `/var/tmp/kaidoku-cn1-r10-g21.jryfWW`. This is not a landed patch or a test of any peer patch. In particular, VZ-1 found that the RV-1 / PL-4 candidate expression only recognizes `-` and `*`, so `+` still passes (`claims/verdicts/VZ-1.md:27-35`); my three-marker matrix confirms the need to handle it in the integrated candidate. Keep the explicit-heading and unique-heading checks, include `+`, and rerun the clean and three-marker matrix after integration.

**Boundary:** this tested append case does not establish detection of an additional bullet inserted inside an already-registered physical span, non-bullet claim text, or renamed Frontier sections. All 12 C3 report files are present, but the overlapping proposed patches are not a live gate change.

## Integration acceptance

- **C1:** land only EX-4’s bounded Rust entry plus its README token; then require Command A at that exact commit to return 89 knowledge files, 89 mapped, and empty missing/dangling sets.
- **C2:** integrate one corrected, generic dependency-coupled rule; then require Command A at the landing commit to return 16 rule blocks and 16 citation-resolved rules.
- **C3:** integrate a reviewed section scanner that includes `+` and rejects missing/duplicate named headings; rerun clean, dash, star, and plus cases against the landing gate.

Until those checks run on the actual integration tree, all three frozen after-states remain pending. The only repository write by CN-1 is this verdict file.
