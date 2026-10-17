# RB3 — reviewer of SB1–5, SHONEN bar discipline (lane B)

## CLAIM
Review seats SB1–SB5 under the SHONEN promotion bar: every retained `[~]`, claimed defect, and closed-gate conclusion must reproduce against primaries; no `[x]`/promotion leakage anywhere.

## METHOD
Read all five SB seats; re-ran SCORECARD command A (`SCORECARD.md:92-123`) and command B (`:132-142`) at HEAD `c343939`; python/jq on `evidence/round-1-2026-10-15/{rea-bundle,result}.json`; `sed`/`grep` on SKILL.md; `sha256sum` on libjq//bin/true/jq; `objdump 0x17070`; LOG anchors `:464-468`, `:784`, `:835`; `git log/show` on SHONEN.md/PROVINCE.md. Read-only.

## FINDINGS
- Command A (mine): 79/79, 9/9, 10.0/10.0; command B 0→10 — reproduces SB1/SB3/SB5.
- SB2 raw values reproduce: bundle `records:1 [inspect_native_instruction]`, `scenarios:0`, `captures:0`; result `reviewer:"L1-author"`, `outside_spot_check:false`, `owned_session_closed:true`, `target_executed:false`.
- SB3 pins reproduce: libjq `7e8bccc6…5e8b6b`, /bin/true `8bc9a73a…`, jq `e8156675…7806`; `17070: f3 0f 1e fa endbr64`.
- SB1's drift+linkage stand (nuances): at correction commit `c265db9`, `SKILL.md:77` was the `## Queue-drain craft` header, so `77-191` was exact then; at HEAD the section is `:81-195`, so the pointer now starts in error patterns and truncates rule 9 (`:187-196`). Decision table/checklists hold no resolvable in-repo citation; sole path-shaped token `GhidraClient.js:607` (`:76`) is external/unpinned. Nit: 21 data rows, not 25.
- SB4 verifies: PROVINCE blob `8a1cec88` unchanged since `7125dd4`; box-4 range `PROVINCE.md:88-109` excludes safety refusal `:114-116`; bleed loci match (`r2-jq-shadow-verdict.md:217,236-237`; `r3-jq-provenance.md:60,136`).
- Discipline intact: 4×`[~]` in all five seats; no `[x]` claim; each seat disclaims verifier eligibility; SB5's S2-citation correction verified (round-6 header `LOG.md:784`, not `:467-501`). Pre-luna `[x]` self-attestations were corrected at `c265db9` (`LOG.md:445-450`); HEAD `c343939` additive-only (+16 LOG/+12 SCORECARD, 0 deletions).

## THREATS
No live probes; host hashes valid today only; REA bundle schema semantics unverified (SB2's "prose past decode" is artifact-level inference); verifier-absence scoped to reviewed artifacts; SB seats landed mid-review — late edits unguarded.

## VERDICT
FINDING: SB1–5 bar discipline holds — 4×`[~]`, no `[x]`, defect claims reproduce; fold SB1's linkage gap and both pointer-drift claims into the final SHONEN text.
