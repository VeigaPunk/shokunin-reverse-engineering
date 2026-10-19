# CR-4 — arc3-loop1-round7 evidence reconciliation

Seat CR-4, verdicts/convergence chain, 2026-10-19. Inspected the frozen work revision `2fba56fe7d54cfb94ca9332c11cea81667b3b289` and records HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`. The unmodified C1 gate is SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` (713 lines). This is a per-claim reconciliation, not a scalar round verdict.

## Rulings

- **C1 operability — BLIND SPOT VERIFIED; LOCATOR CORRECTED; SEEDED CATCH REPRODUCED; CLEAN-PASS ACCEPTANCE UNVERIFIABLE.** The present full pointer is `~/.kimi-code/config.toml:3546`, not the frozen `:3298`. EX-1's receipt-bound scratch variant passes clean and fails a seeded dead pointer, but its receipt proves a hash-only capture, not the contents at line 3546. I do not accept a scratch adjudication as proof that this current pointer is current-by-design. No candidate is approved to land.
- **C2 coverage — FORMULA DERIVATION REPRODUCED WITHIN SCOPE; SELECT EX-3 ONLY; LANDING PENDING.** Eight retained envelopes independently recompute to their IDs, and pinned package source defines the bounded projection. EX-3 most directly closes the frozen “formula not derived” Unknown. This does not generalize to other verbs or versions, and the projected 86/86 is not a landed measurement.
- **C3 calibration — LIVE COUNT REPRODUCED; NO-EDIT ADJUDICATION RECORDED; CURRENT-SUMMARY RESIDUAL.** Three independent enumerations found 1,350 archives, 206 below the dated 1,556 receipt. Retain the dated receipt as historical; `PROVINCE.md:50` remains misleading if read as a current count.

## C1 — `ptr_check` collection blind spot

The frozen claim names `PROVINCE.md:18`'s `:3298` pointer and requires a receipt-anchored current-by-design exception, a seeded dead-pointer failure, and preservation of G21/counters (`claims-frozen.md:14-38`). At the current source, `PROVINCE.md:18` instead contains the full `~/.kimi-code/config.toml:3546` path; `:3298` is described as a historical receipt pointer. The gate's path-bearing regex is at `.ufo/gates/c1-census-v10.py:311`; `classify()` gathers `PTR` only under `if not occ` at `:511-514`, so the pin in the same unit suppresses the pointer. Direct baseline classification has no pointer detection. Direct `ptr_check()` calls for both 3546 and 3298 return `stale`; the current source's full path is 3546, while the abbreviated 3298 is not a full `PTR` match (`PROVINCE.md:18`; first-hand details also recorded at `claims/c1/EX-1.md:8-18` and `claims/c1/EX-2.md:9-21`).

I reran the unmodified gate:

```text
python3 .ufo/gates/c1-census-v10.py --json
exit=0 verdict=PASS
counts: PROVINCE.md={lines:162,loci:6}, SCORECARD.md={lines:1757,loci:9}, SKILL.md={lines:413,loci:2}
current_ok_per_file={PROVINCE.md:17,SCORECARD.md:14,SKILL.md:3}
frontier_rows=14 frontier_errors=[] g2_ok=true stale=0 ambiguous=0 undeclared=0 unresolved=0
```

The passing baseline does not evaluate the line-18 pointer. I reran EX-1's scratch candidate (SHA-256 `cf5595e86f6deda81410d3e2eac82f205e97546ac3c114af561ace9b6e183e62`) against its clean and seeded trees; no repository gate or source was edited:

```text
python3 /var/tmp/kaidoku-c1-ex1.RB0rD3/.ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-c1-ex1.RB0rD3 --json
exit=0 verdict=PASS
current_ok_per_file={PROVINCE.md:20,SCORECARD.md:16,SKILL.md:3}
frontier_rows=14 frontier_errors=[] g2_ok=true; stale=[] unresolved=[]

python3 /var/tmp/kaidoku-c1-ex1.RB0rD3/.ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-c1-ex1-fault.2v4AfI --json
exit=1 verdict=FAIL
PROVINCE.md block 15-26, pointer line 18: UNRESOLVED — :999999 beyond EOF (4150 lines)
frontier_rows=14 frontier_errors=[] g2_ok=true
```

The candidate preserves the line/locus counts and G21, while `current_ok_per_file` increases for newly detected pointers. If “every existing counter intact” means identical numeric `current_ok_per_file` values, this condition is not met; if it means preserving the counter/output surface while counting the newly visible assertions, the recorded runs support it. This interpretation should not be silently assumed.

**Receipt limitation:** EX-1 binds the exact source locus and target to a receipt path, receipt SHA, capture timestamp, and config digest (`claims/c1/EX-1.md:26-28`). I read the referenced receipt: `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt:7-9` says it is “sha256-capture-only” and that no file contents were read; `:26-31` records only metadata and the whole-config SHA-256. The receipt hash authenticates that receipt, but does not reveal or bind the line contents at `:3546`. The source-locus table therefore supports an explicit adjudication, not first-hand proof that the stale live target contains the pin. `EX-1.md:17-18` likewise distinguishes the live stale pointer from its receipt-current-by-design treatment.

Peer reconciliation: CR-3 and VZ-1 select RV-2's narrower scratch variant (`claims/verdicts/CR-3.md:17-32`, `VZ-1.md:24-30`); VZ-2 says the clean-pass acceptance is not verified because the source/receipt mismatch remains (`VZ-2.md:25-31`); CN-2 favors PL-2's broader exact-locus receipt registration (`CN-2.md:17-23`). EX-1's receipt identity is stronger than RV-2's stamp-and-live-pin check, but the same hash-only content gap remains. PL-2 also adds a broader receipt/scope surface and different counters. The blind spot and seeded catch are verified; whether a hash-only receipt is sufficient for the frozen “receipt anchor” is unspecified and not resolved by the evidence. **C1 acceptance remains unverified; no patch is selected for landing.**

## C2 — bounded `inspect-evm-interface` Evidence-ID formula

The frozen claim permits exactly one Unknown and names the `ev_` formula as not yet derived (`claims-frozen.md:40-53`). I reran `python3 .ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/recompute_evidence_ids.py`: all eight `claimed`/`derived` IDs matched, and all eight display-only subject-name/local-path mutations preserved the ID. The script also reported:

```text
pair=67-base1/67-base2 id_equal=True parameter_path_equal=True carrier_sha_equal=True decoded_bytecode_equal=True function_payload_equal=True
pair=67-base1/67-copyA id_equal=False parameter_path_equal=False carrier_sha_equal=True decoded_bytecode_equal=True function_payload_equal=True
pair=67-copyA/67-copyB id_equal=False parameter_path_equal=False carrier_sha_equal=True decoded_bytecode_equal=True function_payload_equal=True
pair=64-base/64-copyA id_equal=False parameter_path_equal=False carrier_sha_equal=True decoded_bytecode_equal=True function_payload_equal=True
```

The bounded formula is `ev_` + lowercase SHA-256 of UTF-8 canonical JSON over the Evidence semantic projection. Source anchors in the retained package evidence are REA 6.4.0 `dist/domain/evidence.js:129-152` and `EvmInterfaceService.js:55-65`; REA 6.7.0 `dist/domain/evidence.js:159-183`, `dist/domain/canonicalDigest.js:1-25,63-75`, and `dist/application/evm/EvmInterfaceEvidence.js:3-11` (`claims/c2/EX-3/evidence/source-contract.txt:9-29`). The 6.4.0 projection omits `relationship_coverage`; 6.7.0 includes it. Both omit `evidence_id`, `subject.name`, and `subject.local_path`. The evidence supports the two pinned versions and tested synthetic runtime/request forms only.

**Selection and disagreement:** select only EX-3's `2026-10-19-arc3-r7-evm-evidence-id-domain` entry/token. EX-6's six-call path/TMPDIR result remains useful and reproducible, but tests bounded path sensitivity rather than deriving the formula; its draft itself says the full formula remains unknown and lacks the opening `recheck:` field (`claims/c2/EX-6/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md:10-16,28-32`). CR-3/VZ-1 select EX-6; VZ-2 selects EX-3 (`VZ-2.md:35-53`). CN-2 selects a Vyper dispatcher characterization because four artifacts converge on it, while also confirming EX-3's eight recomputations (`CN-2.md:25-44`). The Vyper candidate is not disproven; EX-3 is preferred because it directly closes the specifically named formula Unknown. C2 permits one selection, not cumulative credit for competing drafts.

The EX-3 draft begins with `source:`, `verified-at:`, and `recheck:` and pins a same-path expected ID (`claims/c2/EX-3/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md:3-5`), matching the corpus contract (`~/.kimi-code/skills/shokunin/protocol/CORPUS.md:17`). Command A at frozen revision `2fba56fe7d54cfb94ca9332c11cea81667b3b289` returned:

```text
baseline: knowledge_files=85 mapped=85 missing=[] dangling=[] citation_resolved_rules=15 rule_blocks=15 coverage=10.0 depth=10.0
in-memory EX-3 stem/token projection: knowledge_files=86 mapped=86 missing=[] dangling=[] citation_resolved_rules=15 rule_blocks=15 coverage=10.0 depth=10.0
```

This is projection only: no EX-3 corpus entry or map token is landed, and no post-landing Command A run exists. Keep the candidate unlanded until the authorized integration step, then run Command A on the actual resulting revision; the frozen 85→86 acceptance remains pending (`claims/c2/EX-3.md:17-21`).

## C3 — pacman archive inventory

At `2026-10-19T14:42:32-03:00`, three read-only enumerations agreed:

```text
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' -printf 'x' | wc -c -> 1350
Python pathlib direct-child regular-file count                              -> 1350
Bash nullglob /var/cache/pacman/pkg/*.pkg.tar.zst                           -> 1350
```

The dated receipt states 1,556 archives at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` (`verified-at: 2026-10-13`); the measured difference is `1350 - 1556 = -206`. This is a path inventory only, not a signature, coverage, byte-integrity, or package-integrity recheck. The frozen claim explicitly permits an erratum or a no-edit adjudication for a retention-varying inventory (`claims-frozen.md:55-69`). Choose no corpus edit: retain 1,556 as the dated historical observation and record this ruling here. `PROVINCE.md:50` repeats 1,556 without an as-of qualifier and remains discrepant if interpreted as live; correction requires separate authorization. Peer artifacts agree on the count and delta; their erratum/no-edit preference split is not a factual disagreement (`VZ-1.md:58-60`, `VZ-2.md:55-59`, `CN-2.md:48-57`).

## Write boundary and remaining work

Only this verdict is written. No gate, corpus, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, or `LOG.md` was changed. The lane `AGENTS.md` normally requires a LOG entry, but this seat's explicit single-file write fence excludes it.

- C1 needs the integrator to resolve whether a hash-only receipt satisfies the frozen receipt-anchor condition, reconcile the frozen `:3298` with current `:3546`, and clarify whether positive-counter values may change. No patch is approved meanwhile.
- C2 has one selected candidate, EX-3; its entry/token must be landed under authorized integration scope and Command A rerun on that commit.
- C3's no-edit disposition is recorded; the live-sounding `PROVINCE.md:50` count remains a separately authorized residual.
