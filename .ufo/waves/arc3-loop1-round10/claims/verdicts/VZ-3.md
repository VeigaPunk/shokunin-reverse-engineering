# VZ-3 — arc3-loop1-round10 reconciliation verdict

Independent reconciliation of the frozen C1–C3 claims (`claims-frozen.md:16-65`). The quantitative measurements below were re-derived for this verdict. Scratch was kept under `/var/tmp`; no corpus, map, SKILL, gate, custody, or other source file was changed. Git was read-only.

## Source-derived baseline

I ran Command A from `SCORECARD.md:88-124` against immutable `HEAD` `5694506a862c32d2f7aac44935778bce4b6184f2` and work revision `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. Both returned:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":88,"mapped":88,"missing":[],"rule_blocks":15}
```

Thus the pre-integration baselines are **88/88** coverage and **15/15** craft rules. These counts do not establish either frozen after-condition (89/89 or 16/16).

## C1 — coverage / one named Unknown

**REPRODUCED — EX-3's bounded Vyper target result. UNVERIFIABLE — corpus admission and 88→89.**

I ran `npm_config_offline=true bash .ufo/waves/arc3-loop1-round10/claims/c1/EX-3/evidence/rederive.sh` from the lane root. It exited 0; compiler scratch was `/var/tmp/kaidoku-ex3-r10.8eAgos`. The source SHA-256 was `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; the Vyper executable was `0.4.3+commit.bff19ea2`, SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`.

- Paris, Cancun, and Prague double-compiles all passed. Each setting yielded eight ABI functions, eight compiler method IDs and eight REA functions; selector sets matched 8/8 with no missing/extra selectors, `dispatch=abi`, and eight `PUSH4` selector legs.
- Paris produced 423 decoded runtime bytes, SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`. Cancun and Prague were byte-identical at 418 bytes, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`. Paris differs from Cancun/Prague; Cancun equals Prague. ABI and method-ID outputs were identical across the three settings.
- This is static evidence for one synthetic K8 source, Vyper 0.4.3, gas optimization and these compiler EVM-target settings. REA reports runtime execution was not performed; no deployment, chain, or general behavior claim follows.

EX-3 is a suitable single draft candidate: it has `source:`, `verified-at:`, and `recheck:` fields and states its narrow scope (`claims/c1/EX-3.md:3-14`). The draft/map token are not in the corpus or coverage map. The two Command A results above remain 88/88, so the frozen after-condition is **UNVERIFIABLE** pending landing both and rerunning at that commit.

Peer reconciliation: CR-2 supplies another K8 London/Prague target draft and EX-6 a broader five-target matrix; this verdict re-ran EX-3 only and does not adopt those additional measurements. The live C1 candidate disagreement is EX-3 versus EX-4: VZ-1/CN-3 recommend EX-3, while VZ-2/VZ-4/CN-1/CN-4 recommend EX-4; CR-6/CR-7 and CN-2 leave the final choice open. CR-8 selects EX-2, but the frozen C1 claim explicitly says solc 0.8.28 was already characterized at R9 for the same ViaIrVault fixture (`claims-frozen.md:18-20`); R9 EX-5 confirms that source/version comparison (`.ufo/waves/arc3-loop1-round9/claims/c2/EX-5.md:7-11`), so EX-2's recheck is not a fresh C1 Unknown for this wave. EX-4 is a distinct Rust Evidence-ID Unknown. EX-8 is a separate source fixture. CR-5 and CR-7 flag EX-8's locator; VZ-2 and CN-3 dispute that warning. In the current `.ufo/waves/arc3-loop1-round10/claims/c1/EX-8.md:27-29`, the source and recheck paths each have one repository-root-relative prefix, and both files exist; the duplicated nested forms do not. I do not reproduce a locator defect under the documented repository-root invocation.

## C2 — depth / Queue-drain rule #16

**REPRODUCED — SC-2's parser/citation projection in memory. UNVERIFIABLE — integrated rule.**

The current `SKILL.md` has 15 Queue-drain rule blocks. I appended SC-2's exact proposed “Co-land every truth dependency” bullet in memory and applied Command A's rule split and corpus citation-range check. Result: baseline `15` blocks / `15` citation-resolved; projection `16` / `16`. The projected corpus ranges resolve: r4 `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57` (63 lines) and r8 `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-6,17` (17 lines). No `SKILL.md` write was made.

The dependency examples are supported by immutable commit trees: `40de38343398eee72aeebad7429f3bb99ab0a8dd` changes PROVINCE and the coverage map while adding the r4 knowledge entry; `53fcf0caca7255f730fe1a1f17aefd00203a2978` changes the gate, receipt, PROVINCE and map while adding the r8 entry. The r4 item label varies between records: the r4 C2 verdict says F5b at `.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`, while PL-2's plan identifies the C1-dependent Vyper-naming hunk as F5c (`.ufo/waves/arc3-loop1-round4/claims/c2/PL-2/plan.md:185-187,255-259`). Keep the proposed rule generic (“Vyper statement ↔ C1 entry”) rather than embedding that disputed label.

SC-1 through SC-4, EX-12, and EX-16 also propose the dependency-coupled discipline; EX-10 and EX-14 offer other craft topics. Select one reviewed text, describe the r4 dependency generically instead of choosing between F5b/F5c, land it once, then rerun Command A. Until the actual tree reports 16 blocks with resolved citations, C2 is **UNVERIFIABLE as an integrated improvement**.

## C3 — operability / G21 append guard

**REPRODUCED — live append gap and a corrected PL-3 scan-local candidate on scratch. UNVERIFIABLE — the delivered peer patches miss `+`, and no corrected patch is in the live gate.**

The gate SHA-256 is `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. A fresh `python3 .ufo/gates/c1-census-v10.py --json` exited 0 with `PROVINCE.md` at 162 lines, 14 Frontier rows, `frontier_errors=[]`, and verdict `PASS`. The fixed register is at `.ufo/gates/c1-census-v10.py:292-308`; its check covers declared spans at `:422-444`, and the source itself names the appended-bullet residual at `:114-116`.

I copied the gate inputs to `/var/tmp/vz3-g21-final-daeku0o8`, appended a synthetic dash bullet at line 163, and ran the original gate and an exact scratch application of `claims/c3/RV-1/evidence/g21-frontier-coverage.patch`:

```text
before-clean   exit=0 lines=162 errors=[] classes=[] verdict=PASS
before-seeded  exit=0 lines=163 errors=[] classes=[] verdict=PASS
patch_exit=0
patched-clean  exit=0 lines=162 errors=[] classes=[] verdict=PASS
patched-seeded exit=1 lines=163 errors=['PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)'] classes=['FRONTIER-UNEVALUABLE'] verdict=FAIL
```

In `/var/tmp/vz3-g21-plus-nssmsqmg`, I appended `+ **VZ-3 seeded plus-marker Frontier bullet** — boundary fault.` at line 163 and ran both the original and patched gate. **Both returned exit 0 / PASS with `frontier_errors=[]`.** The reason is `.ufo/gates/c1-census-v10.py:318`: the shared `BULLET` matcher is `r"^\s*[-*] "`, which does not recognize `+`; RV-1's patch reuses it.

I also extracted and applied PL-3's exact diff under `/var/tmp/vz3-pl3-check-pshtmrjm`. As delivered, its clean fixture stayed PASS, dash and star seeds at line 163 returned FAIL with `FRONTIER-UNEVALUABLE`, and the plus seed stayed PASS/0. PL-3 requires bullet starts to match registered row starts and checks for missing/duplicate named headings, while RV-1 accepts any bullet within a registered span.

In a second scratch copy `/var/tmp/vz3-pl3-plus-fix-mhnsmxn_`, I changed only PL-3's scan predicate from `if BULLET.match(lines[i]) and (f, i + 1) not in registered_starts:` to `if re.match(r"^\s*[-*+]\s+", lines[i]) and (f, i + 1) not in registered_starts:`; the shared `BULLET` matcher and other checks were untouched. Patch application succeeded; clean stayed PASS/0 and each line-163 `-`, `*`, and `+` seed returned FAIL/1 with `FRONTIER-UNEVALUABLE`. This reproduces the corrected scan behavior on scratch, but the peer patch text still needs that amendment and the live gate remains unchanged. This verdict directly tested RV-1 and PL-3 only; other variants are not proof.

The corrected PL-3 scan is **REPRODUCED on scratch only**: clean stays PASS and `-`, `*`, and `+` line-163 seeds fail as `FRONTIER-UNEVALUABLE`. **UNVERIFIABLE — live gate change:** the peer patch artifact still lacks the `+` matcher update, and the tracked gate remains unchanged. Do not claim the instrument itself is fixed until an amended patch is integrated and checked at its landing revision.

## Integration disposition

- **C1:** resolve the EX-3/EX-4 disagreement (EX-3 is the only candidate re-run by this verdict; frozen C1 excludes EX-2's already-characterized 0.8.28 fixture), land one bounded entry and its map token together, and require Command A to show 89 knowledge files / 89 mapped with no missing or dangling entries.
- **C2:** integrate one generic dependency-coupled rule, describe the r4 dependency without choosing the disputed F5 label, and require Command A to show 16 rule blocks with resolving citations at the integration revision.
- **C3:** amend the PL-3 patch text with the scratch-tested `[-*+]` scan predicate, update the gate's residual note, and rerun clean plus `-`, `*`, and `+` controls against the integrated revision. Do not claim a live instrument fix before that landing.

No corpus, coverage-map, `SKILL.md`, gate, custody, PROVINCE, SCORECARD, LOG, or peer file was changed for this verdict. No Git mutation was performed.