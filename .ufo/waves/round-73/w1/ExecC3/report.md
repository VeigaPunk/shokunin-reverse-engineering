# ExecC3 — independent R73-C3 re-derivation

## Result: frozen declaration does not establish R73-C3

Axes: independent seam fidelity; named-case discrimination; target-pin enforcement; scope/secret safety.

All inputs came from read-only `git show`, not working-tree instrument bytes. Base: `05bf065684e52d72ea25aad95f7acb71fcd7874c`; declaration: `da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b`.

| Source | Independent mutation | rc | Cases | Complete failed list |
|---|---|---:|---:|---|
| base r72 | pristine | 0 | 35 | [] |
| base r72 | a: git reader env=None | 0 | 35 | [] |
| base r72 | b: checker readelf env removed | 0 | 35 | [] |
| base r72 | c: implicit derivation deleted | 0 | 35 | [] |
| declaration r73 | pristine | 0 | 38 | [] |
| declaration r73 | a: git reader env=None | 1 | 38 | [checker-readelf-allowlisted-exec] |
| declaration r73 | b: readelf helper env removed | 1 | 38 | [checker-readelf-allowlisted-exec] |
| declaration r73 | c: implicit helper derivation deleted | 1 | 38 | [implicit-capsule-polluted-raw-log] |

The independent defects were reconstructed using AST-located source surgery, without importing or using the battery patch table. Original committed MutReaders a/b/c patches are retained verbatim. Patch c predates base hardening, so its semantic deletion was mapped to the complete implicit-capsule `elif` at base and the extracted resolver body at declaration. Six independent unified diffs are retained.

## Causal findings

- **a is killed by the wrong declared case.** Declaration uses one shared `seam_seen` file for git and readelf. Both shims append the same PATH. Dropping git's env means git no longer selects its shim; readelf's single remaining record occupies slot zero. Consequently the git case (`seam_paths[:1]`) passes, while the readelf case (`seam_paths[1:2]`) fails. This is an attribution defect, not an import failure. Working-tree source viewed during research already has separate logs; that repair is not in the frozen declaration and was not substituted into these measurements.
- **Independent b is killed by its named case**, by removing env from `readelf_header` itself. The frozen battery instead mutates the `check_receipt` caller (`rh = readelf_header(row["source"], ...)`). Selftest invokes the helper directly with its own env; therefore the frozen battery's b survives. The independent mutation and battery mutation are intentionally distinguished, not conflated.
- **c is killed by its named case.** Removing implicit resolution leaves the empty result/path; the case requires the polluted fixture's real path plus an audit failure mentioning canary. It therefore fails rather than silently accepting the synthetic polluted capsule.
- Every independent selftest produced its complete JSON result (35 or 38 cases), with no stderr/import traceback. Both pristines passed. Thus the observed failures are named assertion failures, not missing-module or missing-fixture exits. The shared-log source explains a's wrong attribution; real frozen `capsule_audit.py` dependencies were provided to every copy.

## Frozen battery, both directions

Executed frozen `mutation-check.py` with `python3 -I -B`, `--rev <declaration>`, explicit absolute `--root` and scratch `--work`, and each requested tool/patch-set. r73 additionally used `--min-pristine-cases 38`. Each direction was measured with correct and deliberately wrong `--expect-target-sha256`.

| Patch set | Pin | rc | survivor_count | Outcome |
|---|---|---:|---:|---|
| r73 | correct | 1 | 1 | a killed_wrong_case; b survived; c killed |
| r73 | wrong | 1 | 1 | same mutation outcomes; target_pin.matched=false and explicit mismatch defect |
| r73base | correct | 2 | unavailable | implicit_capsule_dropped patch site matched 0 times |
| r73base | wrong | 2 | unavailable | same patch-site failure; no scored pin receipt |

The declaration's r73base c anchor still expects `if capsule_path is None ...`, but the frozen r72 target has the hardened explicit/implicit `if`/`elif` structure. The requested frozen base battery is unevaluable, not survivor_count=3. Independently reconstructed base mutants do all survive, as shown above.

Target pin enforcement is observed for r73: matching pin yields matched=true; a wrong 64-zero pin yields matched=false, an explicit defect, and ok=false. Both already exit 1 for mutation defects, so the exit code alone is not discriminating. For r73base, pin enforcement cannot be established from its output because the unmatched patch aborts receipt production; do not claim a scored base pin test.

## Retained evidence and reproducibility

All paths below are relative to this report's directory:

- `summary.json`: source/mutant/patch hashes, eight independent results, four battery summaries, dependency comparison, axes and limitations.
- `r72-{pristine,a,b,c}.json`, `r73-{pristine,a,b,c}.json`: exact argv, rc, stdout, stderr, counts and failed lists.
- `original-{a,b,c}.patch`: committed original defect patches.
- `r72-{a,b,c}.patch`, `r73-{a,b,c}.patch`: independent actual source edits.
- `battery-{r73,r73base}-{correct,wrong}.json`: exact argv, rc and complete stdout/stderr/receipt.
- `rederive.py`: reproducible driver, semantic mutation construction and unconditional scratch cleanup. Existing individual receipts are reused on restart; remove receipts only in a separately authorized fresh reproduction if fresh runs are desired.

Source hashes: r72 `330ecf89debe550ca2e3799f0a1643728604d24d95924e6d8053433d6e32bab6`; r73 `e184cf118427e4678dbbf2647eb615948cffc8ecf59783b13850046d0a9970b1`; frozen battery `06a26a1384e14eae849b90db4735ce3e8faf9e52bfb84aa8895628afd7da9360`.

The battery copies capsule modules from the working tree, but both round modules were hash-compared to the declaration and are byte-identical (`b05e70072bd9c58ee172ccf705926f926f8bd6cfbf0940d2903333894aa593de`). No frozen instrument or implementation file was modified.

## Operational notes / limits

An initial driver assumed battery JSON always appeared on stdout, stopped at JSON decoding of the base battery's stderr-only exit-2 result, and cleaned scratch in finally. Eight individual receipts had already been retained. The driver was corrected to retain raw results first and parse either channel; individual selftests were reused rather than rerun. Four final battery receipts are complete. No inference of success is made from the driver process exit code.

One scratch root `/fast/scratch/hyaku/kaidoku-r73/ExecC3` was used and removed by `finally` before return. All retained writes are confined to the assigned lane report directory and sibling ExecC3.md. No git mutations, installs, package transactions, raw environment dumps, credential reads, UPX executions or REA executions occurred. UPX-copy/--expect-upx is not applicable to these selftest/battery interfaces, which do not accept that argument. Child runs used a constructed nonsecret environment; no inherited environment values were retained. LSP is unavailable: no LSP tool is mounted; AST and source inspection were used instead.

Risks/blockers: named-case attribution a, uncovered frozen caller mutation b, and stale r73base c anchor block the requested frozen 0/3 battery claim. These are measured scoped findings, not permission to modify declaration bytes. Parent owns any landing-version integration gates.

Self-evaluation: accuracy 4/5 (measured frozen results, no claim about repaired landing); completeness 4/5 (all requested runs retained, base battery cannot score); clarity 4/5 (independent-helper and battery-caller b distinguished); actionability 4/5 (exact failing seams and receipts supplied; no out-of-scope repair); conciseness 4/5 (full evidence detail reserved here). Overall 4.0. Improvement: parent should compare any authorized landing bytes with these frozen defects without relabeling declaration evidence as landing evidence. User agreement is expected on the measured limitations, not on the originally claimed 0/3 result.
