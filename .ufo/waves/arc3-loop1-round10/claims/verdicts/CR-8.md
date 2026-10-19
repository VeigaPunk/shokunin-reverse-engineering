# CR-8 — arc3-loop1-round10 convergence verdict

**Seat:** verdicts/convergence (`claims-frozen.md:67-72`). This is a per-item evidence reconciliation, not an aggregate pass. It does not integrate drafts or modify the live corpus, skill, gate, or custody state.

## Revision and current baselines

- `HEAD=5694506a862c32d2f7aac44935778bce4b6184f2`.
- **REPRODUCED — Command A at HEAD.** Ran the `SCORECARD.md:88-124` source-derived recipe against immutable Git objects:

  ```json
  {"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 88, "mapped": 88, "missing": [], "revision": "5694506a862c32d2f7aac44935778bce4b6184f2", "rule_blocks": 15}
  ```

- **VERIFIED — live G21 identity and baseline.** `.ufo/gates/c1-census-v10.py` hashes to `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. `python3 .ufo/gates/c1-census-v10.py --root . --quiet` reports PROVINCE 162 lines, 14 G21 rows, no errors, `VERDICT: PASS` and exit 0. The source declares fixed spans at `:292-308`; `frontier_check()` tests those spans at `:422-444`; the final current span is `PROVINCE.md:161-162` (`claims/c3/PL-3.md:12-13`).

## C1 — coverage: select one bounded Unknown

- **VERIFIED — the candidate Unknown is open.** The frozen claim permits one untested solc version under viaIR (`claims-frozen.md:18-25`). R6 explicitly leaves versions other than 0.8.37 open (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`; candidate scope in `claims/c1/EX-2/entry-draft.md:9`).
- **REPRODUCED — selected EX-2 measurement, bounded to ViaIrVault and optimizer runs 200.** I recompiled the copied source in `/var/tmp/kaidoku-cr8-solc-check.CMz63l`, using the staged solc 0.8.28 package and the read-only local solc 0.8.37 package, repeated both 0.8.28 legs, reran REA 6.7.0 on fresh runtimes, and ran the byte-boundary census. Source SHA-256: `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe`. All 8/8 repeated artifacts (runtime, creation code, ABI and method IDs for viaIR and standard control) matched byte-for-byte. Reproduction and identities: `claims/c1/EX-2/evidence/compiler-identity.txt:7-16`, `source-identity.txt:1-3`, `rederive-output.txt:1-10`, and `dispatch-census.json:161-171,271-293,405-427`.
  - solc 0.8.28 viaIR: 1,517-byte runtime, SHA-256 `3f28f35ea804ce431cca75f3c2b6602aaeaf17938f4d4a773654e19a95f07967`; 15 selectors, 15 comparison sites (14 `EQ`, terminal `SUB`), selector set equals compiler method IDs.
  - Fresh REA result: 15 rows, selectors and decoded-bytecode digest match; Evidence ID `ev_7c4ec6c14ff0ef55efde6a1c6dcfbd51d74d8f937d5f68c21ca258df80ad647d`; `runtime_execution=not-performed`.
  - The 0.8.28 standard-pipeline control is 1,921 bytes with 18 sites (15 `EQ`, 3 `GT`) over the same 15 selectors.
- **CORRECTED — do not claim a new dispatcher class or a version-specific code-body delta.** The fresh 0.8.37 viaIR runtime is also 1,517 bytes; both metadata sections start at byte 1,464 and the pre-metadata bytes are identical (SHA-256 `34a46554c003760ddc41c3e7c2ec94cdc08b0d162a75a763d6f06c49ed03ed15`; no first differing pre-metadata byte). Full-runtime hashes differ because the metadata differs (`claims/c1/EX-2/evidence/dispatch-census.json:2-8,271-293,405-427`). The supported result is that this exact 0.8.28 fixture has been measured and matches the 0.8.37 dispatcher/code-body shape—not that the alternate compiler produced a different dispatcher.
- **VERIFIED — before-state only; UNVERIFIABLE — coverage landing.** Command A remains 88 knowledge files / 88 mapped. EX-2's proposed file and map token are only a draft (`claims/c1/EX-2/entry-draft.md:1,18`); 89/89 is not measured. This verdict selects EX-2 as the sole C1 candidate to carry forward. Other visible C1 reports are alternatives, not additional entries: Vyper target drafts overlap (for example EX-3/EX-7 Paris and EX-5/CR-4 London/Prague); EX-4 proposes a different `inspect_rust_binary` Unknown. They were not independently remeasured by this seat and are not counted alongside EX-2.

## C2 — depth: rule #16 remains a draft

- **REPRODUCED — baseline.** Command A above measures `rule_blocks=15` and `citation_resolved_rules=15`; EX-9 and SC-1 independently report the same pre-change counts (`claims/c2/EX-9.md:7-13`; `claims/c2/SC-1.md:7-14`).
- **VERIFIED — draft consensus, not integration.** Most current C2 proposals converge on declaring and co-landing truth-dependent artifacts, then rerunning the owning check on the combined commit (EX-9 `:47-49`, SC-1 `:26-38`, EX-16 `:5-9`). EX-14 instead proposes completing the byte walk through the terminal dispatcher miss path (`claims/c2/EX-14.md:27-38`). These are alternative rule drafts; none changes `SKILL.md`.
- **CORRECTED — the r4 dependency label is F5c↔C1, not F5b↔C1.** `claims-frozen.md:36-39` uses the F5b shorthand. In the r4 plan, F5b is the real solc/Vyper bytecode debt, while the Vyper-specific split is F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187`). The variant that is true only if the C1 Vyper entry lands in the same commit is explicitly F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:255-259`; `.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/candidate-coupled-vyper.patch.md:217-224`). Use F5c↔C1 when citing that coupling; do not repeat the frozen shorthand.
- **UNVERIFIABLE — actual 16/16 after-state.** Some seats report in-memory 16/16 projections, including CR-5's SC-2 projection (`claims/verdicts/CR-5.md:29-37`), but the live skill remains at 15 rules. Projection is not a committed measurement. No rule was integrated and no post-change Command A result exists.

## C3 — operability: G21 append-past-162 gap and scratch candidates

- **REPRODUCED — live instrument gap.** On copies under `/var/tmp/kaidoku-cr8-c3verify.4cUE9y`, I appended one synthetic Frontier bullet at line 163. The unchanged gate returned PASS/0 with `14 rows asserted, errors: []`; the clean unchanged gate also returned PASS/0. This reproduces the blind spot described by PL-3 (`claims/c3/PL-3.md:12-13,35-50`) and RV-1 (`claims/c3/RV-1.md:9-11`).
- **REPRODUCED — PL-3 candidate on scratch only.** Extracted the diff in `claims/c3/PL-3.md:68-109` and applied it to clean and seeded copies with `patch --batch -p1`. Clean candidate: PASS/0, empty G21 errors. Seeded candidate: FAIL/1, `PROVINCE.md:163 unregistered bullet in '### Round-4 frontier (post-unlock)' (FRONTIER-UNEVALUABLE)`. It also reports absent or duplicate named section headings unevaluable; no such heading fault was part of this seeded test.
- **REPRODUCED — current RV-1 candidate on scratch only.** The current patch (`claims/c3/RV-1/evidence/g21-frontier-coverage.patch:1-7`) has SHA-256 `c0e9e9ca69031e973b872e70ac68548697117eaec7dd7b2ad5e1118b21f4493c`; it applies with `patch --batch -p1`. Clean candidate: PASS/0. Seeded candidate: FAIL/1, `PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)`. This agrees with the current patch measurement in `claims/verdicts/CR-5.md:49-55`. An earlier scratch note referenced a hunk at line 439; that un-hashed version is not the current patch (current hunk starts at 441) and the failure does not reproduce against the current bytes.
- **UNVERIFIABLE — live gate closure.** Both PL-3 and RV-1 remain proposals. The live gate still has the baseline hash and returns PASS on the seeded line-163 copy. These two patches address the same residual; integrate one, not both. PL-3 is the broader option for this narrow gate case because it also rejects missing/duplicate named headings, but that preference is not a live instrument result. Neither candidate's scratch test covers unregistered text inserted inside an already-registered span or non-bullet prose.

## Boundary and disposition

Only this verdict artifact is written in the repository. Compiler and gate-test outputs were confined to `/var/tmp`; no `/tmp`, Git mutation, corpus/map, `SKILL.md`, gate, custody, PROVINCE, SCORECARD, or LOG write was made. The unrelated pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification remains untouched. C1's canonical entry/map integration, C2's selected and measured rule #16, and C3's live patch remain open for the integrator.
