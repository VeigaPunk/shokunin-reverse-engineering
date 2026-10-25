# R35Audit09 — C1 coverage-axis fit: evidence and first falsifications

## Scope and axis

Read-only assessment of frozen C1 (`P35-c1`) for the `.jsc` → source mapping frontier. C1 is an assimilation/admission claim, not a claim that source acquisition, analysis, or an upstream mapper implementation occurred during this wave. The declared target is specific: two knowledge entries, S125/S129 registry rows, PROVINCE frontier table entries, and README coverage entries. No lane production files, counters, claims, plans, corpus, receipts, VCS state, or external source trees were changed. Only this report was written.

## Evidence: frontier/source fit

- At the declared base `aa04633a686d49756763b1feed4be6830d5bb479`, `PROVINCE.md` already declares the `.jsc` → source mapping frontier: `.jsc` Ignition disassembly is held and a View8/jsc2js-style mapper is next (HEAD line 147). `corpus/README.md` also notes the existing `.jsc` boundary (coverage-map/history lines 23–24, 224). This supports topical fit, while distinguishing the new mapper-contract/inventory records from prior bytecode-disassembly records.
- Prep captures exist at the canonical freeze tree: `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md`, `releases-page1.json`, and `releases-page7.json`. The captured README says jsc2js reverses V8-generated JSC bytecode to readable JavaScript; it describes patched d8/loadjsc as the bytecode-printing layer and a View8-derived tool as the reconstruction layer (capture lines 9–13), and says to choose d8 matching the target V8 version (line 22). This is relevant source evidence for documenting a mapper/toolchain contract and release inventory. Presence of captures does not itself establish a running tool, a validated mapping result, or a completed source reconstruction.
- The C1 counter fixes the claimed entry paths/rows in `ENTRIES` (lines 16–19), parses SOURCES as eleven-column rows (21–25), and checks entry existence, trio fields, row citation, mined status, current-round opened date, used-by, PROVINCE stems, and README filenames (98–140). It tests presence/linkage and minimal provenance shape, not the truth or quality of the knowledge prose, correctness of source interpretation, actual mapper execution, or complete source-to-output fidelity. The selftest's positive fixture is synthetic, with `example.test` provenance and simplified documentation tables (42–95); its red mutation removes the trio from entry one. The stated pass is therefore limited to the encoded structural contract.

## First falsifications / control evidence

- Reproduced the frozen C1 do-nothing score using:

  `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B tools/round-35/c1-coverage-counter.py --root . --rev aa04633a686d49756763b1feed4be6830d5bb479 --freeze 2323d197456f1328459d9420aff025cffbcb3e27 --json-out /tmp/r35-c1-donothing.json`

  Output: `C1_FAIL: entry_missing:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md; entry_missing:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md; registry_row_missing:S125; registry_row_missing:S129; province_missing:2026-10-25-r35-jsc2js-mapper-contract; province_missing:2026-10-25-r35-jsc2js-release-inventory; readme_missing:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md; readme_missing:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md`; `EXIT=1`.
- Compared `/tmp/r35-c1-donothing.json` to committed `.ufo/waves/round-35/controls/c1-do-nothing.json`: revision, freeze, failing list, pass value, predicate, and instrument all matched; failing list equality was true. This demonstrates discrimination from do-nothing at base for this instrument and revision pair.
- Ran the explicitly read-only counter selftest: `python3 -I -B tools/round-35/c1-coverage-counter.py --selftest --root .`; output `C1_SELFTEST: ok`, `green=0 red=1`, `EXIT=0`. It supports the counter's synthetic green/red behavior only.
- Base SOURCES census from frozen census receipt: `rows=106`, `EXIT=0`, with nine W04 duplicate-URL warnings. `S125` and `S129` are absent as registry IDs in base SOURCES; the base only contains same-number strings in unrelated contexts (e.g. round-18 `S1250...` and round-34 staged IDs), so exact row IDs remain the relevant distinction.
- C1 freeze inputs are present at `2323d197456f1328459d9420aff025cffbcb3e27`; recomputed hashes there match canonical JSON pins exactly: C1 `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220`, C2 `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94`, plan `45b644a44851b8302dd0a3699e09220ca3b39aad8685ffeb3ae1b6aca9167138`. This confirms the canonical freeze snapshot's hashes, not clean custody under the separate round-34 gate.

## Material limit / instrument-custody caveat

`.ufo/waves/round-35/freeze-status.md` records that `freeze-integrity.py` failed at `f1ea3a6d` (`pins=4 changed=2 freeze=13d7a815`), because final counter bytes changed after the first frozen claims object; later canonical claims contain final hashes but the gate discovers the first-added claims file and rejects. The report states `INSTRUMENT_REVISED` debt and that C1/C2 were not scored before the final freeze; it allows only falsification, not re-freeze. `corpus/claim-freezes.tsv` likewise has a round-35 `FLAGGED` row with `INSTRUMENT_ABSENT,INSTRUMENT_REVISED`. Thus a clean frozen-instrument custody verdict is not supported even though canonical JSON pins equal the bytes at the later canonical revision and the do-nothing control reproduces. Do not present those as curing the disclosed setup-order defect.

## Commands and limits

Commands exercised are quoted above; additional read-only evidence came from `git show`, `git ls-tree`, `git grep`, commit-history inspection, SHA-256, and direct reads of the plan, canonical claims, counters, freeze-status, controls, census receipt, source captures, and claim-freezes ledger. No score was run on a data revision or on any post-freeze C1 entries. No source fetch, live mapper execution, builds, tests beyond the counter's explicit selftest, lint, or verification gate was run. No LSP-backed symbol work was needed for this advisory assessment. No nested delegation, background jobs, installs, or VCS mutation occurred.

## Conclusion

C1 fits the named coverage axis and the existing frontier as a narrow admission/assimilation measurement; existing captures provide relevant external-source basis for the specified records. At base, its do-nothing control fails as intended and the counter selftest distinguishes its synthetic green/red fixtures. However, the round-35 freeze-integrity/setup-order defect remains material: these observations do not establish clean instrument custody, actual mapping capability, source-to-output correctness, or a passing measured C1 claim. The frozen kill rule and no-re-freeze instruction remain controlling.
