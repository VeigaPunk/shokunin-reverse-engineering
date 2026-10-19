# VZ-2 — reconciliation verdict (arc3-loop1-round9)

**Measured against:** `HEAD=947091d6b6f52684faf9ca53adf94ff8a0f6b006`  
**Verified at:** 2026-10-19  
**Write boundary:** this verdict only. Source files, `PROVINCE.md`, `SCORECARD.md`, gate code, corpus, receipt, and other seats' artifacts were not edited. All scratch used for this verdict was under `/var/tmp` and removed.

## Disposition

- **C1 — PARTIALLY REPRODUCED; frozen completion condition DISCREPANT.** The live pacman cache count and installed-`jq` byte equality were re-derived. The `available:true` session claim remains unverified as a current state. Most importantly, the census instrument is already `FAIL`, so the frozen “instrument still PASS” condition is not met.
- **C2 — REPRODUCED, bounded to the exact fixture and compiler pair.** I independently recompiled the EX-5 source with solc 0.8.28 and 0.8.37, re-probed both viaIR runtimes, and compared their code prefixes. This closes the tested 0.8.28 version question for this source/settings pair; it does **not** establish a different dispatcher class or generalize to other versions or sources. The corpus/map landing and post-landing Command A remain unverified.
- **C3 — TARGETED MEASUREMENT REPRODUCED; integration incomplete.** The live pointer resolves to the current Kimi pin, and an insertion-before-pin test shows the physical-line drift behavior. The whole census gate still fails on the separate SCORECARD locus. No canonical corpus/receipt landing was made by this seat.

## C1 — freshness

### Per-item findings

1. **Live archive and sidecar counts — OBSERVED; historical baseline — DATED.** `PROVINCE.md:50` still states `1556 signed archives` without a local as-of qualifier. First-hand output:

   ```text
   $ printf 'archive files: '; ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
   archive files: 1350
   $ printf 'signature files: '; ls /var/cache/pacman/pkg/*.sig | wc -l
   signature files: 1350
   $ python3 - <<'PY'
   from pathlib import Path
   root=Path('/var/cache/pacman/pkg')
   archives={p.name for p in root.glob('*.pkg.tar.zst')}
   signatures={p.name[:-4] for p in root.glob('*.pkg.tar.zst.sig')}
   print(f'archive_count={len(archives)} signature_count={len(signatures)} archives_without_adjacent_signature={len(archives-signatures)} signatures_without_archive={len(signatures-archives)}')
   PY
   archive_count=1350 signature_count=1350 archives_without_adjacent_signature=0 signatures_without_archive=0
   $ wc -l < PROVINCE.md
   162
   ```

   The arithmetic against the row's old literal is `1350 - 1556 = -206`. The retained source calls 1,556 a 2026-10-13 snapshot (`corpus/knowledge/2026-10-13-pacman-packages.md:75-83`); the current cache cannot remeasure that historical state. Sidecar presence/pairing is not cryptographic validation of every signature, so I do not independently assert that all 1,350 current archives have valid signatures.

2. **Installed `jq` byte identity — VERIFIED for this recheck.**

   ```text
   $ pacman -Q jq
   jq 1.8.2-1
   $ pacman -Qkk jq
   jq: 25 total files, 0 altered files
   $ sha256sum /usr/bin/jq
   e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
   $ tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
   e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
   ```

   This proves the installed executable matches that cached archive member; it is not a fresh cryptographic verification of the archive signature.

3. **`available:true in live session` — UNKNOWN as a 2026-10-19 live state.** `PROVINCE.md:40` dates the Core-table surface verification to 2026-10-13, so that old observation can be retained as dated. I had no attached `binary_session` to establish current provider availability. The probe name `binary_session {}` and `.MTREE` format description in `PROVINCE.md:50` are methods/capability descriptions, not additional live scalar measurements; the `.MTREE` format claim is described at `corpus/knowledge/2026-10-13-pacman-packages.md:14-16`.

4. **Census-gate requirement — DISCREPANCY.** First-hand `python3 .ufo/gates/c1-census-v10.py --json` exited 1. Relevant output:

   ```text
   "verdict": "FAIL"
   "stale": []
   "ambiguous": []
   "undeclared": [{"file": "SCORECARD.md", "block": "1833-1839", ...
                    "line": 1834, "scope": null, "disp": "AMBIGUOUS"}]
   "unresolved": []
   "frontier_rows": 14, "frontier_errors": [], "g2_ok": true
   ```

   The offending assertion at `SCORECARD.md:1834` is beyond the gate's declared SCORECARD range ending at line 1813 (`.ufo/gates/c1-census-v10.py:276-277`). This failure is independent of the PROVINCE row; do not describe the full instrument as PASS before or after a row-only patch.

### Reconciliation

My current counts and `jq` check agree with the direction of the C1 reports. `PL-2` is the most complete row-patch proposal I reviewed: it dates the old `available:true` observation, records the current `jq` recheck, and points to the retained count erratum (`claims/c1/PL-2.md:20-34`). Its reported GPG check covers the one `jq` archive; I did not perform that cryptographic check myself and do not extend it to every archive. The patch remains proposal text, not a repair in this tree. The C1 result is therefore partial: facts support a dated count correction, but the frozen PASS condition fails at this HEAD.

## C2 — coverage

### Baseline and selected candidate

I reran Command A using the immutable Git-object recipe in `SCORECARD.md:88-124`:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

**Preferred single landing: EX-5, the alternate-solc version candidate.** This matches frozen candidate (a) (`claims-frozen.md:32-38`) and is now independently measured here, rather than relying on EX-5's reported figures. I copied the exact fixture `claims/c2/EX-5/evidence/source/ViaIrVault.sol` (SHA-256 `f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe`), used offline-cached solc 0.8.28 and the read-only solc 0.8.37 prefix, and ran the seat's `evidence/compile.js` with optimizer enabled/runs 200 and `viaIR:true`. I then called `rea-agents@6.7.0` `inspect-evm-interface <runtime.hex> hex --format json` on both fresh viaIR outputs (provider `evmole-interface` / `evmole@0.9.3`). The 0.8.28 call Evidence ID was `ev_109b30898db7be5e4b9b1d0f4dcfb0fae6846cc9a964ca51c1ecd7a36885d15f`.

First-hand parsed output:

```json
{"version":"0.8.28+commit.7893614a.Emscripten.clang","runtime_bytes":1517,"runtime_sha256":"3f28f35ea804ce431cca75f3c2b6602aaeaf17938f4d4a773654e19a95f07967","abi_functions":15,"method_identifiers":15,"rea_rows":15,"selectors_match":true,"decoded_sha256":"3f28f35ea804ce431cca75f3c2b6602aaeaf17938f4d4a773654e19a95f07967","decoded_matches_compiled":true,"confidence":"inferred","runtime_execution":"not-performed"}
{"version":"0.8.37+commit.f401782d.Emscripten.clang","runtime_bytes":1517,"runtime_sha256":"2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a","abi_functions":15,"method_identifiers":15,"rea_rows":15,"selectors_match":true,"decoded_sha256":"2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a","decoded_matches_compiled":true,"confidence":"inferred","runtime_execution":"not-performed"}
{"viair_runtimes_same_size":true,"viair_pre_metadata_bytes_equal":true,"shared_prefix_sha256":"34a46554c003760ddc41c3e7c2ec94cdc08b0d162a75a763d6f06c49ed03ed15","metadata_tails_differ":true}
repeat_compile_comparisons=PASS (runtime.bin, creation.bin, abi.json, method-identifiers.json for solc 0.8.28 and 0.8.37)
```

**Inference, bounded:** for this exact synthetic source and optimizer configuration, bytes `[0,1464)` are identical between solc 0.8.28 and 0.8.37. The runtime suffix is 53 bytes total (`1517 - 1464`); REA reports a 51-byte terminal CBOR payload at offset 1464, leaving two trailing bytes outside that payload. The suffix differs, but I do not separately characterize those two bytes. The shared code prefix means no dispatcher-class delta was observed for this version pair. This does not establish a general rule for other source shapes, solc releases, optimizer settings, or fallback/receive variants. REA reports inferred static selectors; it did not execute either runtime.

### Peer convergence and landing boundary

There is **no single C2 candidate consensus**; the nominations are alternatives, not evidence for one another. `CN-2` preferred EX-11 when EX-5 was not yet in its report snapshot (`claims/verdicts/CN-2.md:62-79,114-116`), while `CN-1`, `VZ-3`, and `CR-7` prefer EX-8; `CN-3` prefers CR-1; `CN-4`, `VZ-4`, and `CR-6` prefer EX-10; `VZ-1` focuses on the Vyper creation-bytecode residual (`claims/verdicts/CN-1.md:46-48`, `VZ-3.md:36-48`, `CR-7.md:62`, `CN-3.md:19-25`, `CN-4.md:61-83`, `VZ-4.md:59-83`, `CR-6.md:67-69`, `VZ-1.md:44-68`). `EX-12` now also has a delivered report for the alternate-solc family (`claims/c2/EX-12.md:5-19`); I did not independently rederive its result. The measured EX-5 result directly tests frozen candidate (a), so I prefer it for the one-entry C2 move; this is my bounded recommendation, not peer consensus.

The runtime alias equivalence already recorded at `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:11` does not by itself close the creation-bytecode or broader output-format residuals discussed by `VZ-1`, `CR-8`, and `EX-10` (`claims/verdicts/CR-8.md:82-110`, `claims/c2/EX-10.md:7-10`). Those are legitimate alternative C2 scopes, not a basis for treating every Vyper report as a duplicate. Only one entry and matching map token should be integrated.

The EX-5 corpus entry and map token are still draft-only; no post-landing Command A exists. Before landing, make the source path satisfy `corpus/QUALITY.md:14` (the draft currently names the source by a repository-relative path plus SHA at `claims/c2/EX-5/entry-draft.md:5,10`) and ensure the recheck is a stable regenerating recipe, not only a prior scratch-path capture (`corpus/QUALITY.md:16`; `claims/c2/EX-5/evidence/reproduction.txt:12-17`). After exactly one entry and map token are integrated, rerun Command A at the landing revision; `87 → 88` remains a projection, not a measured result.

## C3 — calibration / pin-line drift

### Present pointer and drift behavior

**OBSERVATION:** the live config search found exactly one `rea-agents@` occurrence; content search returned:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

I imported the checked-in gate, ran its live-anchor derivation, and called its own `ptr_check()` on the actual pointer and on a minimal scratch config under `/var/tmp`:

```text
live_anchors={'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
actual_pointer_4126=('ok', 'pins 6.7.0')
scratch_before_line2=('ok', 'pins 6.7.0')
scratch_after_old_line2=('stale', "line holds no rea-agents pin: '# inert drift probe'")
scratch_after_reanchor_line3=('ok', 'pins 6.7.0')
```

The gate maps `ptr_check()` state `ok` to `current-ok` (`.ufo/gates/c1-census-v10.py:466-482,538-544`), so the pointed-to line itself is current-ok. The frozen pointer is `PROVINCE.md:18`. Inserting a line before the pin makes the old physical line stale; re-anchoring to the shifted line restores `ok`. **INFERENCE:** this pointer is path-plus-line based, not stanza-identity based. This test establishes the drift mechanism, not the historical cause or exact chronology of every earlier line change; behavior after duplicate matches is also untested.

**Instrument-wide status — DISCREPANCY:** the same first-hand gate run above is `FAIL` because of `SCORECARD.md:1834`, not the PROVINCE pointer. The targeted pointer result does not turn the census into a PASS. The C3 peer reports `EX-15` and `SC-4` reach the same qualitative separation between a current pointer and a red whole-gate verdict (`claims/c3/EX-15.md:7-9`, `claims/c3/SC-4.md:50-70`); their numbers are not used as my evidence. The characterization is in seat artifacts only at this snapshot; no canonical corpus erratum or receipt update was made, so that integration part remains for the parent.

## Final integration actions

1. Keep the C1 row's 1,556 as a dated historical value, add the measured live delta and date the `jq` result; do not claim the full instrument passes until the separate out-of-scope SCORECARD locus is resolved by an authorized change.
2. If integrating one C2 entry, prefer EX-5 after the source-path/recheck quality fixes above, then measure Command A at the actual landing commit.
3. Preserve C3 as “pointer check current-ok; pointer is line-sensitive; full gate FAIL” and land the characterization in the authorized canonical note/receipt separately.

Only this VZ-2 verdict is this seat's deliverable. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` and all peer artifacts were left untouched.