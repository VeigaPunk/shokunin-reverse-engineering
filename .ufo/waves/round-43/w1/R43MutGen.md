# R43MutGen — design-time mutation test of the QUALITY-85 tuple refusal

**Verdict: DONE — 20 single-fault mutants of the six-field tuple check enumerated; 16 are blind to the round-42 C02 defect; a 10-case selftest suite that kills all 20 is specified and machine-readable at `.ufo/waves/round-43/w1/artifacts/R43MutGen/mutants.json`.**

Seat: R43MutGen (leaf, mutation tester). Round 43 wave 1, pre-freeze. Consumer: R43C1Gen's integrator (selftest suite for `tools/round-43/heldout-gen-v4r43.py`).

## Golden semantics under test (from the draft claim, plans/round-43-claims.md, R43-C1)

For every carrier the generator runs REA, extracts `observed_features(envelope)` restricted to the six `REQUIRED_FEATURES`, and compares against the tuple the manifest would declare (`carriers[].declared_features`, the single R41-CL1 key). Any field inequality → exit 3 `declared_tuple_unobserved`, **no manifest write**, per-carrier diff on stdout. The six fields: `handler_set`, `gap_kinds`, `gap_dependencies`, `be_argv`, `symlink_removed`, `published`.

## Subject inputs (grounded in committed round-42 evidence)

| side | source | tuple |
|---|---|---|
| C02 declared | `corpus/evidence/round-42/c2/heldout/manifest.json` `carriers[C02].declared_features` | H=`[squashfs_v4_be]`, G=`[extractor-failure, unpublished-entry]`, D=`[]`, BE=`yes`, SR=`false`, P=`nonzero` |
| C02 observed | `corpus/evidence/round-42/c2/heldout/C02/envelope.json` `normalized_result.extraction_gaps` (three gaps: extractor-failure, **depth-limited**, unpublished-entry) via `observed_features` (`tools/round-42/c2-counter.py:581`); independently in `run.json` summary | H=`[squashfs_v4_be]`, G=`[depth-limited, extractor-failure, unpublished-entry]`, D=`[]`, BE=`yes`, SR=`false`, P=`nonzero` |

Only `gap_kinds` differs — exactly the mismatch record `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` → `declared_features.mismatch[0]` (the sole mismatch, which stopped round 42 honestly at `eb8215ac`). C02's REA argv carried `--max-depth 1` (`run.json`), which is what minted `depth-limited` at the ceiling beside the failing chunk. Supporting schema facts used below: `declared_features = declared_tuple(predictor(factors))` (predictor ≡ declared by construction, `tools/round-42/heldout-gen-v4.py`); combos have `class_expected = null` and named classes carry `{label, action, reported_only}` — there is **no** `class_expected.features` key (`manifest.json` `declared_schema`).

## Axes

- **Coverage:** 20 mutants across 5 fault classes (field-drop ×7, set-semantics ×4, data-source ×4, enforcement ×3, comparison ×2). 16 accept the round-42 C02 manifest as-is.
- **Depth:** each mutant entry carries the exact C02 declared/observed inputs, the mutant's verdict on C02, and a concrete selftest with full tuples.
- **Calibration:** each selftest states expected behavior under the correct check **and** under the mutant; kill direction (under-strict vs over-strict) is labeled; one inference is flagged.

## Mutant table (abridged — full tuples in `mutants.json`)

| id | single fault | C02 passes? | selftest | kill direction |
|---|---|---|---|---|
| M01 | drop `handler_set` | **yes** | ST-HFLIP: observed H=`[squashfs_v4_le]` vs declared `[squashfs_v4_be]` | under-strict |
| M02 | compare only `gap_kinds` | no | ST-DEPS: only `gap_dependencies` differs | under-strict |
| M03 | drop `gap_dependencies` | **yes** | ST-DEPS | under-strict |
| M04 | drop `be_argv` | **yes** | ST-BEARGV: only `be_argv` differs (yes vs no) | under-strict |
| M05 | drop `symlink_removed` | **yes** | ST-SYMREMOVED: only `symlink_removed` differs (true vs false) | under-strict |
| M06 | drop `published` | **yes** | ST-PUBZERO: only `published` differs (zero vs nonzero) | under-strict |
| M07 | drop `gap_kinds` — the exact M42-2 blind spot | **yes** | ST-C02-REAL | under-strict |
| M08 | accept on subset (declared ⊆ observed) | **yes** | ST-C02-REAL — C02's lie *is* a subset relation | under-strict |
| M09 | accept on superset (observed ⊆ declared) | no | ST-OVERDECL: declared G adds `depth-limited`, observed doesn't | under-strict |
| M10 | `gap_kinds` reduced to presence boolean | **yes** | ST-KINDSWAP: `[unpublished-entry]` vs `[extractor-failure]` | under-strict |
| M11 | filter `depth-limited` out before comparing | **yes** | ST-C02-REAL — looks like normalization, hides M42-2 exactly | under-strict |
| M12 | read tuple from `class_expected.features` (None → skip every carrier) | **yes** | ST-C02-REAL + loud-refusal-on-None rule | under-strict |
| M13 | "observed" read from the manifest predictor, not the envelope (pre-run predictions; tautology) | **yes** | ST-C02-REAL | under-strict |
| M14 | skip combos entirely | **yes** | ST-C02-REAL — combos are where M42-2 lived | under-strict |
| M15 | incomplete declared tuple = vacuous pass | no | ST-INCOMPLETE: declared_features missing `published` | under-strict |
| M16 | diff printed but refusal not enforced (exit 0, manifest still written) | **yes** | ST-C02-REAL — assert exit 3 **and** no manifest file **and** diff content | under-strict |
| M17 | refuse only if ALL fields differ (any→all inversion) | **yes** | ST-C02-REAL — a one-field lie is the canonical shape | under-strict |
| M18 | checker's REA invocation drops per-class `--max-depth` | **yes** | ST-C02-REAL + argv assertion (`--max-depth 1`) | under-strict |
| M19 | order-sensitive list compare (no set canonicalization) | no | ST-ORDER: same sets, different order → correct **accepts** | over-strict |
| M20 | `published`/`be_argv` compared by truthiness (`'zero'` truthy) | **yes** | ST-PUBZERO | under-strict |

## Calibration notes

1. **The claim's core regression is ST-C02-REAL** (the committed round-42 C02 row + envelope). It alone kills 10 of the 16 C02-blind mutants (M07, M08, M10, M11, M12, M13, M14, M16, M17, M18). If R43C1Gen carries exactly one test, it must be this one — it is CTL-C1-2's red arm restated as a generator selftest.
2. **The other 6 C02-blind mutants (M01, M03, M04, M05, M06, M20) are only killed by single-field selftests.** These matter because each is a *different* plausible one-line fault, and C02 cannot distinguish them. The six single-field fixtures (ST-HFLIP, ST-DEPS, ST-BEARGV, ST-SYMREMOVED, ST-PUBZERO, plus ST-PUBZERO again for M20) are enumerated with full tuples in `mutants.json`.
3. **M09 and M19 are not C02-blind but are real single faults** of the comparison step: M09 green-lights over-declared manifests (declaring a gap REA never minted — the symmetric failure M42-2 could have been); M19 over-refuses benign order differences. Both must be carried: the suite's calibration is "refuse exactly the lies, accept exactly the truths."
4. **M18 is procedure-faithfulness, not text-matching.** [INFERENCE] Whether an uncapped re-run of C02 textually drops `depth-limited` depends on the seed's nesting depth; the mutant is killed by asserting the checker's REA argv (`--max-depth 1` per `run.json`), independent of the resulting tuple.
5. **M12/M13 are the data-source traps the manifest schema already warns about** (`declared_schema.location`): reading `class_expected.features` or the predictor's expectation instead of `carriers[].declared_features` + the envelope turns the check into a no-op or a tautology. The selftests assert the declared source is the single R41-CL1 key and the observed source is the on-disk envelope.
6. **Enforcement is a separate axis from detection (M16, M17).** A correct diff with a missing refusal is the most dangerous mutant: it prints exactly the receipt everyone wants and still writes the manifest. ST-C02-REAL's kill assertion therefore checks all three artifacts: exit code 3, absence of the manifest path, diff content.

## Design rule handed to R43C1Gen (encoded in `mutants.json` → `aggregate.design_rule_for_R43C1Gen`)

The tuple check must (1) bind `carriers[].declared_features` as the sole declared source; (2) extract `observed_features` from the REA envelope produced under the carrier's recorded `max_depth`; (3) compare all six fields by set-canonicalized equality; (4) treat any missing/None tuple source as a loud refusal, never a skip; (5) on any difference exit 3 and write no manifest.

## Evidence

- All tuple values verified against: `corpus/evidence/round-42/c2/heldout/manifest.json` (C02 declared), `corpus/evidence/round-42/c2/heldout/C02/envelope.json` (observed: 3 extraction_gaps incl. `depth-limited`), `corpus/evidence/round-42/c2/heldout/C02/run.json` (`rea_argv` with `--max-depth 1`; summary `gap_kinds` matches observed tuple), `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` (`declared_features.mismatch[0]`, only field `gap_kinds`), `tools/round-42/c2-counter.py:581-652` (`observed_features` reference extraction), `tools/round-42/heldout-gen-v4.py` (predictor ≡ declared construction; six-field `DECLARED_KEY`), `manifest.json` `declared_schema` (no `class_expected.features`; `declared_extras` outside the binding).
- Consistency validation of the artifact (python3): 20 mutants, 10 suite cases, every mutant killed by ≥1 case, suite kill-lists partition the mutant set, C02-blind aggregate matches per-mutant flags, all differing-fields within the six bound fields. Artifact parses as JSON (33,679 bytes), sha256 below.
- No tools installed/upgraded this seat; nothing written outside the artifacts dir and this report. Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43MutGen` removed.

## Artifact

- `.ufo/waves/round-43/w1/artifacts/R43MutGen/mutants.json` — sha256 `40bb66ee3ff5090545030513bbd4ea4f0251380047dfa1d485d459393eb1d242` (verify: `sha256sum .ufo/waves/round-43/w1/artifacts/R43MutGen/mutants.json`).
