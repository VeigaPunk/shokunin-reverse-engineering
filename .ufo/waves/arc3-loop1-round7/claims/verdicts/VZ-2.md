# VZ-2 — arc3-loop1-round7 reconciliation verdict

Seat VZ-2, verdicts/convergence chain, 2026-10-19. Direct checks used HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804` and frozen work revision `2fba56fe7d54cfb94ca9332c11cea81667b3b289`. Peer artifacts were compared against first-hand checks, not treated as evidence by themselves. I wrote only this verdict; no gate, corpus, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, or `LOG.md` was changed. Scratch, where used, remained under `/var/tmp`.

## Summary

| Claim | Ruling |
|---|---|
| C1 operability | **BLIND SPOT REPRODUCED; CLEAN-PASS CRITERION NOT VERIFIED.** The current path pointer is `:3546`, not the frozen `:3298` receipt pointer. Scratch patches catch seeded dead pointers, but the current `:3546` target is stale and its receipt-current-by-design exception is not anchored to evidence that identifies that line. No patch is landed. |
| C2 coverage | **NAMED FORMULA UNKNOWN CLOSED WITHIN PINNED SCOPE; LANDING PENDING.** EX-3's bounded `ev_` formula derivation is independently reproduced from pinned package source and eight envelopes. Recommend landing only EX-3's entry/token. Command A remains 85/85; the required post-landing 86/86 has not occurred. |
| C3 calibration | **LIVE COUNT REPRODUCED; HISTORICAL-CURRENT DISCREPANCY.** Live count is 1,350, delta −206 from 1,556. Select the frozen no-edit adjudication for the dated corpus receipt; separately flag `PROVINCE.md:50` as stale if read as current. |

No all-claims completion is justified: C1 has an unresolved acceptance defect and C2 still lacks a landed entry/map token and post-landing Command A run.

## C1 — pointer collection blind spot

### Before-state and locator correction

The gate `.ufo/gates/c1-census-v10.py` is 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`. At `:511-514`, pointer matches are appended only under `if not occ`; the pin/version scan has already populated `occ` for the current Kimi statement. My unmodified `python3 .ufo/gates/c1-census-v10.py --json` returned PASS, with counts `PROVINCE.md={162 lines, 6 loci}`, `SCORECARD.md={1757, 9}`, `SKILL.md={413, 2}`, G21 14 rows / no errors, and `current_ok_per_file={PROVINCE.md:17,SCORECARD.md:14,SKILL.md:3}`. The baseline therefore does not evaluate the pointer.

The frozen locator needs correction. `PROVINCE.md:18` contains the full active path:line `~/.kimi-code/config.toml:3546`, dated “2026-10-19 re-read.” The `:3298` text is explicitly the historical 17:55:49Z receipt pointer; it is only a suffix, not a second full path:line token matched by the gate's `PTR` regex. Direct `ptr_check()` calls for both 3298 and 3546 return `stale`; the actual `:3546` target is not the live Kimi pin.

### Candidate-patch reconciliation

The defect is agreed across PL-1/PL-2, EX-1/EX-2, and RV-1/RV-2. The scratch candidates do not agree on how to satisfy the frozen clean-tree condition:

- RV-2's final candidate (SHA-256 `1e7ee0d9b7c89074de9eef37c0da4f8684848f59450219192b329e81c6822f8c`) passes the clean copy by registering `PROVINCE.md:18`, `:3546` against the literal `2026-10-19 re-read` stamp and pin. It catches the seeded `:999999` pointer as UNRESOLVED/FAIL; G21 remains 14 rows/no errors, JSON keys remain the same 19, and G2 remains true. This demonstrates the collector/fault test, but the string stamp and pin are not a durable receipt identity and do not establish why the stale `:3546` is current-by-design.
- RV-1 and EX-2 correctly distinguish the current source from the frozen historical suffix: an honest collector that checks `:3546` fails on the unchanged current text. The old receipt records `:3298`, not a full-path `:3546` locus. EX-1's and other registry variants add receipt metadata, but the stored receipt has a whole-config digest rather than captured line content; that does not by itself prove the current line pointer.
- The variants also change positive-counter results differently (RV-2: 20/14/3; PL-1: 19/16/3; PL-2: 21/16/3). Do not combine these counts or claim one patch's semantics using another's test results. Existing field/key inventory and G21 are preserved in the candidate runs; `current_ok_per_file` necessarily changes as pointers become newly detected.

**Ruling:** the blind spot and seeded-fault catch are reproduced, but requirement (a)—current-tree PASS with an adequately receipt-anchored current-by-design pointer—is **not verified**. Resolve the `:3546` versus historical `:3298` source/receipt mismatch before landing any candidate. No gate edit was made.

## C2 — corpus Unknown and competing drafts

### Re-derived candidate: `inspect-evm-interface` Evidence IDs

I independently ran `python3 .ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/recompute_evidence_ids.py`. All eight envelopes recomputed to their claimed IDs; all eight display-only subject-name/local-path mutations retained the ID. The retained same-byte copy pairs have equal carrier/decoded-bytecode SHA and function payload, but changed IDs as path fields in the semantic record change. For example, 6.7.0 base `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052` differs from copyA `ev_6cbe1e3dfd0c345004eacb4369fef8f580f8766cd2b25ea0e629b1bf1c9a2917`; `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` differ while the decoded runtime and normalized functions remain the same.

I also inspected the cached package implementations directly. In 6.7.0, `dist/domain/evidence.js:159-183` defines the semantic projection and `dist/domain/canonicalDigest.js:1-25,60-75` emits sorted compact JSON and SHA-256; `dist/application/evm/EvmInterfaceEvidence.js:3-11` binds it to `inspect_evm_interface`. The 6.4.0 implementation has the same projection shape except it lacks `relationship_coverage` (`dist/domain/evidence.js:129-152` and `EvmInterfaceService.js:55-65`). Thus the bounded formula is `ev_` + lowercase SHA-256 of UTF-8 canonical JSON over that semantic projection—not a universal formula for every REA verb/version. EX-3's fixture is a synthetic 28-byte runtime, and the entry properly limits its claim to the two pinned package versions and tested request forms.

EX-6's six live path/TMPDIR probes are also reproducible and useful: one 1,517-byte carrier consistently yields the same ID at the same resolved path, while basename/parent-path changes mint other IDs; relative spelling of the same path and alternate TMPDIR do not change it. But its draft's statement that the complete formula remains unknown is superseded for the tested versions by EX-3's source derivation and 8/8 independent recomputation. I therefore disagree with VZ-1's choice of EX-6 as the C2 landing candidate: EX-3 more directly closes the named “formula not derived” Unknown, and its draft already opens with `source:`, `verified-at:`, and `recheck:` fields.

The Vyper `--no-optimize` / `-O codesize` candidate is independently strong and fits frozen option (a): I recompiled K8 with Vyper 0.4.3, finding no-opt 617 B (SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`) with eight PUSH4/EQ comparison legs, and codesize 360 B (`bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`) with a packed selector table and no PUSH4. Fresh REA calls recovered the eight compiler selectors in both. EX-4/EX-5/CR-1/CR-2 provide convergent additional byte-level evidence. This remains a valid alternative Unknown, not a second C2 landing.

### Coverage measurement and decision

I ran Command A from `SCORECARD.md:88-124` against work revision `2fba56f`:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":85,"mapped":85,"missing":[],"revision":"2fba56f","rule_blocks":15}
```

No arc3-r7 token is present in the current corpus map, and no candidate entry is landed. The 86/86 results in peer artifacts are overlay projections, not post-landing measurements. **Select exactly EX-3's `2026-10-19-arc3-r7-evm-evidence-id-domain` entry/token** as the recommended C2 closure; defer EX-6 and the competing Vyper entry. Then land the one entry and token under the authorized integration scope and run Command A on that actual revision. Until that happens, C2's evidence is verified but its frozen landing/85→86 acceptance remains **PENDING**.

## C3 — pacman archive inventory

A fresh Python regular-file enumeration and independent Bash nullglob count both returned **1,350** direct-child `*.pkg.tar.zst` files in `/var/cache/pacman/pkg`. The historical receipt at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` records **1,556**, so the re-derived delta is `1350 - 1556 = -206`. This measures paths/count only; it does not recheck signatures, integrity, or total bytes.

C3 peers agree on 1,350/−206; EX-7/RV-3 prefer an append-only erratum while SC-1/SC-2/EX-8/EX-9 prefer no edit. The frozen claim permits either disposition. I select **recorded no-edit adjudication**: preserve 1,556 as the explicitly dated 2026-10-13 snapshot because cache inventory is retention-varying, not a capability assertion. Residual: `PROVINCE.md:50` repeats 1,556 without an as-of qualifier; it is discrepant if interpreted as current inventory. That source was not changed under this seat's write fence.

## Integration boundary

This verdict is evidence reconciliation only. C1 still needs a defensible pointer/receipt reconciliation before a gate patch is accepted. C2 needs exactly one selected entry/token landed and a fresh Command A 86/86 measurement; the recommendation above is EX-3. C3 records the allowed no-edit adjudication and does not certify the historical entry's signature or integrity claims. No other tracked or custody path was changed.
