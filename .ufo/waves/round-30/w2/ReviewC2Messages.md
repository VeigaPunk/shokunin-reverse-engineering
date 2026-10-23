# ReviewC2Messages — round 30, wave 2

Seat: `KaidokuR30.ReviewC2Messages` (reviewer, leaf). Read only the committed bytes, with no REA run.
Attacked: R30-C2's committed records. The question is whether each of the 19 committed envelopes in `corpus/evidence/round-30/c2/envelopes/` carries its frozen outcome, and where in the envelope the frozen message sits. Also attacked: the entry's envelope-shape claim, "13 of 16 refusals carry the message only in `error.details.issues`".

## Verdict

- **R30-C2 committed records: holds.** Observation. All 16 predicted refusals are `ok:false` and contain the frozen message verbatim. All 3 predicted acceptances match my own decode of the mutant bytes: the same packages in the same order, with the same dependency indices, root, file_offset, compressed and uncompressed sizes, edge count and subject sha256.
- **"13 of 16 refusals carry the message only in `error.details.issues`": holds** when it counts mutants. Observation. Exactly 13 envelopes are `invalid_request`. In each one, the generic `error.message` reads "Analysis input is invalid. Check the arguments and try again.", the frozen message appears in exactly one leaf (`$.error.details.issues[0].message`), and the `.stderr` file is empty (0 bytes).
- **The wording "13 of 16 refusal kinds" fails** (LOW). Observation: the 16 refusal mutants carry 13 distinct messages, and the 13 `invalid_request` mutants carry 10 distinct messages. So the count is 13 of 16 refusal *mutants*. Counted by kinds (distinct messages), it is 10 of 13.

## Method and evidence

Command: `cd /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewC2Messages && timeout 300 python3 -I -B locate.py > locate.out`. Exit 0, start and end at 2026-10-23T03:13:45Z.

- For each refusal, the script walks every string leaf of the parsed envelope and records each JSON path whose value contains the frozen message. It classifies each hit as an exact match or a suffix (and records the prefix). It also checks the raw stdout bytes and the `.stderr` bytes.
- For each acceptance, the script uses my own ELF64 section-header parser on the copied mutant (it does not import `rust_dep_oracle.py` or the counter). It finds the single `.dep-v0` section and inflates it with a strict zlib check (`decompressobj().eof` must be true and `unused_data` empty). It then parses the JSON as UTF-8 and compares it field by field with `data.normalized_result.auditable_metadata`.
- Mutant copies: `cp /fast/scratch/hyaku/kaidoku-r30/mutants/* <seat>/mut/` at 2026-10-23T03:12:50Z. All 19 sha256 values in `mut.sha256` equal the frozen `predictions.tsv` sha256 column. Observation: `sort mut.sha256 | diff - <(sha256 and id columns of predictions.tsv, sorted)` gave `diff_exit=0` at 2026-10-23T03:14:50Z.
- Provenance (2026-10-23T03:14:02Z):
  - `git diff --quiet 24da3459 HEAD -- corpus/evidence/round-30/c2/` exits 0.
  - `git diff --quiet 0dbabf78 HEAD -- corpus/evidence/round-30/c2/predictions.tsv` exits 0.
  - At 03:12:50Z, `git diff --quiet HEAD -- corpus/evidence/round-30/c2/` also exited 0.
  - So the committed envelopes and the frozen predictions equal the working copy that was read.

## 19-row table

Notation used in the table:
- `P` = `Selected artifact /fast/scratch/hyaku/kaidoku-r30/mutants/<id>: `
- `U` = `Unsupported target for inspect_rust_binary at /fast/scratch/hyaku/kaidoku-r30/mutants/<id>: `
- "match" means the frozen message is in the stdout bytes and the envelope is `ok:false` (the P2 refusal clause), or, for an acceptance, that every decode check is equal.

| id | predicted | error code | message location(s) | exact field value | match |
|---|---|---|---|---|---|
| g-relocated | accept | ok (exit 0) | n/a | off 332016, comp 9870, unc 55724, 584 pkgs, root 463, 3041 edges = my decode | yes |
| g-recompressed | accept | ok (exit 0) | n/a | off 332016, comp 9797, unc 55724, 584 pkgs, root 463, 3041 edges = my decode | yes |
| g-no-root | accept | ok (exit 0) | n/a | off 332016, comp 9786, unc 55712, 584 pkgs, root null (0 roots), 3041 edges = my decode | yes |
| r-empty | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency section is not file-backed` | yes |
| r-nobits | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency section is not file-backed` | yes |
| r-compressed-flag | refuse | unsupported_target | `error.message`; `error.details.reason` | `U` + msg; `details.reason` = `Compressed dependency sections are unsupported` (exact) | yes |
| r-two-sections | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Image contains more than one dependency section` | yes |
| r-not-zlib | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency section is not a complete zlib stream` | yes |
| r-trailing-bytes | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency section is not a complete zlib stream` | yes |
| r-over-1mib | refuse | resource_constraint | `error.message`; `error.details.reason` | both `P` + `Dependency section exceeds the 1 MiB compressed limit`; `reported_limits.maximum_bytes` 1048576 | yes |
| r-inflate-ratio | refuse | resource_constraint | `error.message`; `error.details.reason` | both `P` + `Inflated dependency JSON exceeds the size limit`; `reported_limits.maximum_bytes` 896576 | yes |
| r-not-utf8 | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency JSON is not valid UTF-8` | yes |
| r-bad-json | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency section JSON is invalid` | yes |
| r-nesting-33 | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency JSON nesting exceeds 32 levels` | yes |
| r-format-negative | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency JSON does not match the format schema` | yes |
| r-extra-field | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency package 0 does not match the package schema` | yes |
| r-kind-dev | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency package 0 does not match the package schema` | yes |
| r-two-roots | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency JSON declares more than one root package` | yes |
| r-index-outside | refuse | invalid_request | `error.details.issues[0].message` only | `P` + `Dependency index 584 from package 0 is outside the package list` | yes |

All 19 `.stderr` files are 0 bytes, and the frozen message is not in stderr for any refusal (`in_stderr=False`). Excerpts from `locate.out`:

- `HIT $.error.details.issues[0].message suffix(prefix='Selected artifact /fast/scratch/hyaku/kaidoku-r30/mutants/r-bad-json: ')`
- `HIT $.error.details.reason exact` (r-compressed-flag)
- `checks {... "packages_ordered_equal": true, "root_index": true, "edges": true} ALL` (all 3 acceptances)
- `SUMMARY {"invalid_request_issues_only": 13, "other": 3}`

## Findings by severity

1. **LOW: "13 of 16 refusal kinds" miscounts kinds.** Observation. It appears at `LOG.md:3017` ("13 of 16 refusal kinds return `invalid_request`") and in the last sentence of `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md:43` ("sees the generic text for 13 of 16 refusal kinds").
   - Counts from the 03:14:02Z script: `refusal mutants 16 distinct messages 13` and `invalid_request mutants 13 distinct messages 10`.
   - Three pairs share a message: r-empty/r-nobits, r-not-zlib/r-trailing-bytes and r-extra-field/r-kind-dev.
   - Correct wording: "13 of 16 refusal mutants", or "10 of 13 refusal messages". `corpus/README.md:82` ("13 of 16 refusals") and the entry's first sentence at :43 ("13 of the 16 refusals") are correct.
2. **LOW: no envelope field equals the bare frozen message except r-compressed-flag's `details.reason`.** Observation.
   - The other 15 refusals carry it only as a suffix after `Selected artifact <path>: ` or `Unsupported target for inspect_rust_binary at <path>: `.
   - P2 uses a substring test (`message not in out_text`, `tools/round-30/c2-rust-refusals.py:205`), so the claim is unaffected.
   - However, the SKILL decision table (`SKILL.md:977-992`, ``refused: `<msg>` ``) and the entry do not say that the message carries a path prefix. Inference: a reader who matches with equality on `issues[].message` or `error.message` would miss all 15.
3. **INFO: the entry and SKILL are incomplete on where the non-`invalid_request` messages sit.** Observation.
   - The entry says only that compressed-flag "returns `unsupported_target`". Its message is in `error.message` (with a `U` prefix) and is exactly `error.details.reason`.
   - For the two `resource_constraint` refusals, the entry names `error.message` and `reported_limits.maximum_bytes`; both values (1,048,576 and 896,576) match. It omits `error.details.reason`, which repeats the prefixed message.
   - `SKILL.md:968` ("for `invalid_request` refusals the message field is generic") holds.
4. **INFO (REA-side, not a lane defect): all 13 `invalid_request` refusals say `"retryable":true`.** Observation. These refusals are deterministic for a fixed input file. Inference: a caller that trusts `retryable` would retry pointlessly.

No finding against R30-C2's predicate outcome. P2-match holds on the committed bytes for 19 of 19.

## Residual risk and verification gaps

- Not run: REA, a live re-run, and the counter (the counter is seat ReRunC2's job). This seat checks the committed records only. Whether the live run agrees with the records is unknown here.
- Packages were checked against my decode of the mutant bytes, not against the original wheel member. The mutants' provenance from carrier `elf-x86_64-uvx` was not re-derived here.
- For the shared-message pairs, a match cannot show which branch fired (already listed in the entry's Limits).
- No `lsp` server applies: the targets are JSON, TSV and Python records, and grep was used only as a literal locator.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewC2Messages/`)

| file | sha256 |
|---|---|
| `locate.py` | `8480f0ada013b60467592c9bd8dcf7b9972527bdc9d925b13510c7caa991a67e` |
| `locate.out` | `d0dfd8f0c606071d18b9dd3101959cc0c218563a775178ce3487e84f32ea79ac` |
| `mut.sha256` (sha256 of the 19 copied mutants) | `cca8363d843638859c2694e5169b6ff8ce09b23a0ff596493053d61b85590fa7` |
| `mut/<id>` (19 copies) | equal to the `predictions.tsv` sha256 column |

Installs: none. Processes: none left running. No lane file other than this report was written. No git or jj writes.
