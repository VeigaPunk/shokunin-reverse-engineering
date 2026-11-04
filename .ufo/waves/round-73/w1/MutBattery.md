# MutBattery — round-73 battery honesty

Axes: named-case specificity, inventory integrity, expectation/target binding, exact restoration. No source changes or installations.

## Findings

- **Survivor:** manually applying `readelf_env_dropped` to the observed landing bytes leaves `--selftest` green: rc 0, 38 cases, failed `[]`. Git-reader and implicit-capsule mutants each exit 1 naming their declared case. Landing battery scoring is false, survivor_count 1, not the claimed 0.
- **False positive kill:** the git-reader mutant additionally breaking the readelf case fails both `git-reader-allowlisted-exec` and `checker-readelf-allowlisted-exec`. The battery labels it `killed`, returns `ok: true` (main's exit mapping 0), rather than the requested `killed_wrong_case`. Its predicate checks membership, not exclusivity.
- **Inventory defenses hold:** deleting the git-reader `cases.append` block alone yields rc 1, 37 cases, failed `["case-inventory"]`; deleting only its registry line yields rc 1, 38 cases, the same failure. `--min-pristine-cases 37` cannot bless the dropped case: scoring raises Unevaluable because pristine is not green.
- **Expectation attacks rejected:** a zero-expectation patch aimed at the git site but declaring the readelf case is `killed_wrong_case`, `ok: false` (main exit mapping 1). Applying r73 to the declaration's round-72 route raises Unevaluable: readelf patch matches zero sites (mapping 2). A zero-filled incorrect target SHA yields `target_pin.matched: false`, `ok: false` (mapping 1; this run also has the independent readelf survivor).
- Declaration comparison: pristine declaration bytes are green, but its battery scores false: git-reader mutation fails the readelf case instead (`killed_wrong_case`), readelf survives, implicit capsule is killed.

## Evidence and limits

`MutBattery/manual-selftests.json` records actual subprocess rc/output and mutation/restoration hashes. `MutBattery/battery-attacks.json` records actual `check()` outputs/errors. Battery attacks import the declaration battery, inject captured target bytes via its `git_blob` seam (avoiding git writes), and use explicit scratch work; artificial patch sets are in-memory only. Recorded scoring rc is the existing main function's mapping, not a separately executed CLI process exit. Manual selftests use `/usr/bin/python3 -I -B ... --selftest`.

Landing source SHA256: `ed3e26fab2ace12e94956704bab68940443fe093bd10aa2c70c75aa9c3284c1b`.
Declaration source SHA256: `e184cf118427e4678dbbf2647eb615948cffc8ecf59783b13850046d0a9970b1`.
Declaration battery SHA256: `06a26a1384e14eae849b90db4735ce3e8faf9e52bfb84aa8895628afd7da9360`.

All landing mutation copies were restored byte-for-byte to the landing hash and rerun green. The declaration pristine comparator was subsequently overwritten with landing bytes for its green restoration control; it was not a declaration mutation/restoration claim. No original route bytes changed. An initial anchor assertion failed before detectors ran because declaration and landing selftest bodies differ; scratch was cleaned, then recreated at the same assigned location for the completed experiment. Final cleanup removed `/fast/scratch/hyaku/kaidoku-r73/MutBattery` in a finally block before reporting. No environment values were persisted by this seat's receipts; selftest fixture files remained in scratch and were deleted.

Risks: C3's zero-survivor claim is contradicted for the recorded landing hash; extra unrelated failures are accepted as valid kills. This report does not modify the contract or repair the battery.

Report: .ufo/waves/round-73/w1/MutBattery.md
