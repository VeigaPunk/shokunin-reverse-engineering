# WDataflow — Dependency map of retained round-33 CHPE modules and causal separation from held R33FixtureBuilder

Reviewer/leaf seat, round 33 w1. Scope: four retained modules `tools/round-33/{chpe_profile, selftest_pegen, measure_driver, r32_oracle_adapter}.py`, their isolated parser selftest receipts under `.ufo/waves/round-33/repairs/parser/`, and retained source captures under `corpus/evidence/round-33/sources/`. Read-only lane; scratch root `/fast/scratch/hyaku/kaidoku-r33/w1/WDataflow/`. No parser runs, no fixture writes, no lane mutations other than this report.

Pinned admissible revision `d7076120e4f00c6d18aa77b8764d14861e820eb2`; base `428315a8f5674b952def862910af6e07a6c2224b`. Claim `R33-C1` remains STOPPED/unprovable (`claim-stop.json`); this report is dependency/separation evidence only and is not a replacement measurement or revived carrier claim.

## 1. Named axes
- Primary: **depth** — source-traceable structural decision table and bounded reader (the retained profile's finding-id ordering and guards).
- Secondary: **verification** — isolated instrument selftests and pinned source anchors must remain independently checkable.
- Non-axis constraint: **safety/containment** — held `R33FixtureBuilder` outputs and the original held item `U064N008Hf47eb933` are excluded; no reconstruction.

## 2. Module dependency map (static, from admitted files)

| Module | Role | Stdlib imports | Retained-module imports | External non-stdlib deps | Runtime file reads |
|---|---|---|---|---|---|
| `selftest_pegen.py` | synthetic PE32+ fixture recipe generator | `struct` | none | none | none |
| `chpe_profile.py` | CHPE structural profile classifier | `hashlib,json,os,struct,subprocess,sys,tempfile` | `selftest_pegen` **only inside `selftest()`** | none | input bytes (argv path) |
| `measure_driver.py` | generic structural-match driver | `argparse,hashlib,json,os,random,resource,secrets,shutil,signal,subprocess,sys,tempfile,time` | none | `git` binary (optional, `--repo/--rev` mode) | classifier bytes, manifest, document spec, row paths |
| `r32_oracle_adapter.py` | baseline adapter to frozen r32 oracle | `hashlib,json,os,subprocess,sys,shutil,types` | `selftest_pegen`, `measure_driver` **only inside `selftest()`** | none | `tools/round-32/arm64x_oracle.py` (pinned sha256) |

Import edges (admitted):
- `chpe_profile.selftest()` → `selftest_pegen` (lazy, `sys.path` insert of own dir).
- `r32_oracle_adapter.selftest()` → `selftest_pegen` and `measure_driver` (lazy).
- `r32_oracle_adapter.adapt()` → `round-32/arm64x_oracle.py` via `load_oracle()` (hash-guarded `exec` of verified bytes).
- `measure_driver.Source` (git mode) → `git` subprocess.
- `chpe_profile.selftest()` → subprocess to its own file for each case.

No edge points to any held/excluded path, quarantine, or builder module.

## 3. Production vs. selftest dependency closures (non-obvious separation)

Production entry points (`chpe_profile` classify-bytes/CLI, `r32_oracle_adapter adapt`, `measure_driver run`) have **smaller** closures than the modules' source imports suggest:

- `chpe_profile` production closure = stdlib only. `selftest_pegen` is imported only in `selftest()`.
- `r32_oracle_adapter` production closure = stdlib + the pinned `round-32/arm64x_oracle.py` (sha256 `17eea1f9…`). `selftest_pegen` and `measure_driver` are imported only in `selftest()`.
- `measure_driver` production closure = stdlib + optional `git` binary.
- `selftest_pegen` closure = stdlib (`struct`) only.

Consequence: the held item could not have entered the retained *production* code paths through these modules; any influence would have to be via the two retained selftest-only helpers, which are themselves stdlib-only and held-path-free (see §5). Selftest-only imports must not be reported as production dependencies.

## 4. Source captures (primary-source evidence)

Retained captures and pins (`source-pins.json`, `source-anchor-map.json`, `pe-source-capture.json`) verified byte-identical to their pins for sampled files:

| Anchor label | Retained path | Pinned sha256 | Verified |
|---|---|---|---|
| `pe-format.md` | `corpus/evidence/round-33/sources/pe-format.md` | `563f2dd9…` | yes (sampled) |
| `Object-COFF.h` | `corpus/evidence/round-33/sources/Object-COFF.h` | `214d3f4a…` | yes (sampled) |
| `BinaryFormat-COFF.h` | `corpus/evidence/round-33/sources/BinaryFormat-COFF.h` | `a44641df…` | pin recorded |
| `COFFObjectFile.cpp` | `corpus/evidence/round-33/sources/COFFObjectFile.cpp` | `444fc3fa…` | pin recorded |
| `Chunks.h` | `corpus/evidence/round-33/sources/Chunks.h` | `09e505a2…` | pin recorded |
| `Chunks.cpp` | `corpus/evidence/round-33/sources/Chunks.cpp` | `550c20df…` | pin recorded |
| `Writer.cpp` | `corpus/evidence/round-33/sources/Writer.cpp` | `229163a9…` | pin recorded |
| `arm64ec-codemap.test` | `corpus/evidence/round-33/sources/arm64ec-codemap.test` | `edf6964b…` | pin recorded |
| `COFFDumper.cpp` | `corpus/evidence/round-33/sources/COFFDumper.cpp` | `f107c5a8…` | supplementary only (not a classifier dependency) |

`chpe_profile.FINDINGS` anchor strings reference 8 of the 9 captures (all except `COFFDumper.cpp`, which `source-anchor-map.json` explicitly marks supplementary). Anchor labels are compile-time string constants in the module; no source file is read at runtime. LLVM revision scope: `0d261d1ca552c95a8f007e061c787ac7132fbcbc` (LLVM 23.1.3) only; PE spec is the negotiated Markdown capture.

## 5. Isolated original selftest receipts (instrument evidence only)

| Receipt | Module under test | sha256 (verified) | Top-level result |
|---|---|---|---|
| `repairs/parser/selftest-chpe_profile.json` | `chpe_profile` | `bb11bba0…` | `pass: true`, `cases: 107`, `finding_ids_defined: 45`, `finding_ids_produced: 45`, `finding_ids_uncovered: []`, `vocabulary_ok: true` |
| `repairs/parser/selftest-measure_driver.json` | `measure_driver` | `01287525…` | `pass: true` (all listed checks `ok: true`) |
| `repairs/parser/selftest-r32_oracle_adapter.json` | `r32_oracle_adapter` | `061ee98a…` | `pass: true` (11 results, all `pass: true`) |

Module hashes (`parser-pins.json`) verified byte-identical to current files:
- `chpe_profile.py` `b364de70…`
- `selftest_pegen.py` `aea5475c…`
- `measure_driver.py` `af5d86f1…`
- `r32_oracle_adapter.py` `4ac63bec…`

Selftest receipts are retained original instrument outputs, not production carrier measurements and not a substitute for the stopped 32-row claim. `selftest_pegen.py` has **no dedicated standalone receipt**; it is exercised only indirectly through the `chpe_profile` and `r32_oracle_adapter` selftests. This is the one direct-instrument coverage gap in the retained set.

## 6. Causal separation from the held item

Evidence used (admitted only): module source/imports, `safety-holds.json`, `quarantine-record.json`, `prep/R33ChpeParser-independent.json`, lane filesystem listing, git history.

Findings:
1. Excluded builder paths are absent from the lane: `tools/round-33/{chpe_fixture_gen,chpe_predict,chpe_driver_manifest}.py`, `.ufo/waves/round-33/{frozen,prefreeze-controls}`, `prep/{R33FixtureBuilder,R33ChpeParser}.md`, `prep/builder-count-erratum.txt` — none present (`ls` confirms).
2. Lane-wide grep for the excluded builder module names returns matches **only** inside `quarantine-record.json`'s `excluded_paths` metadata; no retained module, receipt, or prep file references them.
3. Retained module imports are stdlib + retained siblings + pinned round-32 oracle only; no import of any held/excluded path or quarantine.
4. Hold metadata records only provider error metadata and exclusion rules; no held findings were inspected or used. Original held item `U064N008Hf47eb933` remains untouched.
5. Shared schema labels (`r33-chpe-structural/1`, `r33-structural-manifest/1`, `r33-document-spec/1`, `r33-measure-driver/1`, `r32-oracle-adapter/1`) are **not** treated as dependency proof: they are string constants defined independently in the retained modules. Their possible occurrence in held materials would not establish a causal link, and held materials were not inspected.
6. Git history: all four modules and the three receipts first appear in commit `d7076120` (the stop commit), not in base `428315a8`; no commit touches them between base and the pinned revision except the stop commit. No hidden inheritance from a held builder is evidenced.

Conclusion: on admitted evidence, the four retained modules are causally separated from the held item. The separation proof is static (imports/paths/metadata) and does not claim runtime-environment isolation beyond the modules' own fixed paths and pinned hashes.

## 7. Uncertainty and limits (reported, not repaired)

- `selftest_pegen.py` has no standalone receipt; its correctness rests on indirect exercise. A future isolated receipt could close this without reviving the 32-row claim; not done here.
- `r32_oracle_adapter.selftest()` depends on `measure_driver.run` for its `common_positive_facts_match_counter` check, so that one check is not measure-driver-independent. Production `adapt()` does not use `measure_driver`.
- Selftests were **not rerun** in this wave (not assigned; safety cap on subprocess count/memory/wall time). Verification rests on retained receipts plus hash equality to pinned module bytes.
- Causal separation is limited to static imports/paths and hold metadata; runtime state (environment, cwd, filesystem) was not audited.
- The 32-row claim stays stopped: no admissible independent expected fixture manifest exists, and no replacement/reconstruction was attempted or proposed.

## 8. Proposed move (one, bounded)

**Non-obvious move:** split the reporting of dependency closure by *entry point*: treat production closures (`chpe_profile` → stdlib only; `r32_oracle_adapter` → stdlib + pinned round-32 oracle) as the admissible dependency set, and relegate `selftest_pegen`/`measure_driver` imports to a separate, explicitly-labeled "instrument-only" closure. This improves the **depth** axis (tighter, honest dependency claims for the retained profile and adapter) and the **verification** axis (a clear, auditable boundary between production and instrument code) without harming either, and it prevents future seats from inflating production dependency claims with selftest-only imports. It does not alter contract, axes, routes, or judgment, and it does not revive the stopped 32-row claim.

## 9. Risks
- If a future change adds a top-level (non-lazy) import of `selftest_pegen` or `measure_driver` into `chpe_profile`/`r32_oracle_adapter`, the production-closure claim in §3 breaks; must re-audit.
- If `round-32/arm64x_oracle.py` changes without updating `ORACLE_SHA256`, `r32_oracle_adapter` refuses (exit 2) — by design, but it blocks the adapter until the pin is consciously updated.
- Static-only separation proof could miss a runtime path that reads a held file; not evidenced, but not runtime-proven.

## 10. Verification performed
- Read modules and receipts; verified module sha256 against `parser-pins.json` (all 4 match).
- Verified receipt sha256 against `prep/R33ChpeParser-independent.json` (all 3 match).
- Verified sampled source-capture sha256 against `source-pins.json` (Object-COFF.h, pe-format.md match).
- Lane listing confirms excluded builder paths absent; grep confirms no held-path references outside quarantine metadata.
- No builds, tests, linters, formatters, or parser runs performed in this wave.

## 11. Tooling
No installs or updates performed. Only `read`, `grep`, and lane `ls`/`sha256sum` via bash were used. No pacman transactions. No lane git/jj writes.
