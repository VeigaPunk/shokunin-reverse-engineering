CONFIRMED — Attacked the C1 derivation-rooted exact-path rule under malformed/ambiguous namespaces, successful carve/normalization cases, and removal diagnostics. The core `(root, rel)` mapping fails closed for the tested wrong namespaces, but two contract-level defects remain: the purported “whole-segment” root lookup accepts a non-segment-bounded diagnostic root occurrence, and paths that normalize away trailing slash or `.` may be accepted despite representing an invalid file spelling.

## Axes
- Coverage: tested nonzero-offset carved root and multiple roots, including correct/wrong hint; exposed a malformed-root acceptance case.
- Calibration: separated intended path equivalences from malformed receipt inputs; counter itself does not enforce file-kind path shape.
- Depth: exercised root equality, duplicate `$output/`, path normalization, and diagnostics outside the root.

## Evidence and commands
All scored cases used temporary git fixture repositories under `/fast/scratch/hyaku/kaidoku-r41/R41W2C1PathRule/fx-repo.*`; each was `git init`-ed and its exact `git rev-parse --show-toplevel` checked before commits. The driver imported the frozen working-tree counter and called its `measure()` with a projection-consistent simulated runner. Fixture commits used `-c user.name=fx -c user.email=fx@fx`; no lane/fleet VCS mutation. Each custom probe held the other three fixture carriers green, so `carriers_matched` is 4 on accept and 3 on reject. Driver and full JSON receipts/scores are in the artifacts directory; files contain no vendor firmware bytes.

Command used:
```sh
cd /fast/scratch/hyaku/kaidoku-r41/R41W2C1PathRule
python3 -B /fast/scratch/hyaku/kaidoku-r41/R41W2C1PathRule/driver.py > summary-run2.json
```
No REA/unblob invocation was used; this is specifically a deterministic counter-path-rule unit attack, not an end-to-end extraction rerun. The simulated runner returned projection-equivalent, rehosted envelopes; evidence IDs were recomputed through pinned REA 6.5.0 `xpin-attribute.mjs`/package root. Thus these are counter logic results, not claims about real REA emitting malformed inputs. No tools installed.

### Scenarios
| Case | Counter result | Exact observation |
|---|---:|---|
| `00-baseline-green` | PASS (4/4, exit 0) | Control: canonical root and paths pass (4/4). |
| `01a-two-roots-no-hint` | REJECT (3/4, exit 1) | Ambiguous pair of squashfs_v4 roots rejected (3/4; root null; oracle/gaps fail closed). |
| `01b-two-roots-correct-hint` | PASS (4/4, exit 0) | Two roots with explicit inner-root hint pass (4/4). |
| `01c-two-roots-wrong-hint` | REJECT (3/4, exit 1) | Hint naming actual outer root while all rows are inner rejects (3/4; no oracle hit). |
| `02a-carve-nonzero-offset-deep` | PASS (4/4, exit 0) | Single offset-4096 carved derivation root and correctly nested published path pass (4/4). |
| `02b-carve-shallow-publish` | REJECT (3/4, exit 1) | Same carve but file/gap published at outer root rejects (3/4; no oracle hit; gap resolves 0 entries). |
| `03a-path-equals-CR-file` | PASS (4/4, exit 0) | Extra file exactly CR does not alias a non-empty oracle/nonregular row; counter accepts (4/4). |
| `03b-path-equals-CR-gap` | REJECT (3/4, exit 1) | Gap path exactly CR does not match nonregular row; rejects (3/4). |
| `04a-double-dollaroutput-child` | REJECT (3/4, exit 1) | Duplicate prefix in derivation child survives one-strip rule as literal `$output/...`; resulting namespace rejects (3/4). |
| `04b-double-dollaroutput-file` | PASS (4/4, exit 0) | Duplicate prefix in file/gap/unpublished path is stripped repeatedly by `path_parts`; accepted (4/4). |
| `05a-removal-outside-no-root-run` | REJECT (3/4, exit 1) | Removal report with link wholly outside CR rejected by disposition check (3/4). |
| `05b-removal-decoy-segment-run` | PASS (4/4, exit 0) | Link in `/fast/scratch/hyaku/kaidoku-r41/decoy/firmware.bin_extract/bin/link` satisfies required `bin/link`; counter accepts although trusted output directory is `/fast/scratch/hyaku/kaidoku-r41/fx/V4-after`. |
| `06a-file-trailing-slash` | PASS (4/4, exit 0) | Oracle file path with trailing slash is normalized to same key and passes (4/4). |
| `06b-file-leading-dotslash` | PASS (4/4, exit 0) | Leading `./` is dropped and passes (4/4). |
| `06c-file-interior-dot` | PASS (4/4, exit 0) | Interior `/./` is dropped and passes (4/4). |
| `06d-dir-as-file-trailing-slash` | REJECT (3/4, exit 1) | A file spelling `.../bin/link/` aliases the nonregular `bin/link`; `nonregular_unpublished_ok` catches it and rejects (3/4). |
| `06e-gap-trailing-slash` | PASS (4/4, exit 0) | Gap spelling with trailing slash aliases nonregular key; passes (4/4). |

Pure-function probes (all 15 passed): exact root maps to empty rel; a non-empty oracle row cannot match root itself; redundant `//`/`./` and candidate trailing slash collapse; table `./` and leading `/` are stripped; suffix and non-whole-segment prefixes do not match; deeper child files do not match outer rows; and a link with no root substring returns `None`.

## Counterexample / defect
1. **Diagnostic root is found by a segment run anywhere in the absolute path, not by a root-relative prefix.** `diagnostic_rel()` scans backwards through `report.link` segments and accepts a matching root sequence wherever it appears. Custom scenario 05b gave `/fast/scratch/hyaku/kaidoku-r41/decoy/firmware.bin_extract/bin/link`, while the envelope’s `parameters.output_directory` was `/fast/scratch/hyaku/kaidoku-r41/fx/V4-after`. `diagnostic_rel()` returned `bin/link`, and `disposition_check()` accepted it as the required `bin/link` symlink removal. Thus a report from a different directory satisfies the removal obligation. The selftest’s absolute `/x/firmware.bin_extract/...` and outside-no-root tests do not cover this decoy-segment collision. This violates the documented diagnostic rule “path is ... inside REA’s private extraction root” and “locating the subject root as whole segments” because it treats any occurrence as ownership.
   - Smallest safe correction: bind a known run-private extraction/output prefix from `parameters.output_directory` (which is the parent of `CR` for normal REA runs) and require `report.link` to begin with that prefix plus `/` and the selected CR, at a component boundary. At minimum require the root to be the final consecutive segment run before the returned rel but also reject preceding decoy path components once a trusted absolute output root is available. Add a green-root/decoy-absolute-path mutation whose decoy suffix matches the required symlink row; expected `gaps_ok=false`.
2. **File path canonicalization can erase trailing slash and dot segments.** `extract_rel()` calls `path_parts()`, which drops both empty segments and `.`; therefore a regular-file publication `firmware.bin_extract/var/info.txt/` is judged identical to the oracle row `var/info.txt` and passes all C1 clauses in scenario 06a. A trailing slash denotes a directory path in filesystem path syntax, not a regular file path. The analogous `./` spellings likely represent equivalent filesystem names, but the counter has no file-type check on resolved path, so the trailing slash can make a malformed receipt assert a directory-like name while borrowing the regular oracle file identity/sha. This is a false positive if malformed receipt serialization is in threat model; projection `rel_suffix()` also normalizes this spelling, so rerun does not distinguish it.
   - Smallest safe correction: normalize allowed `.` and duplicate separators only if REA’s schema guarantees them; reject trailing slash for `files[].relative_path` (or validate the final component is nonempty before normalization). Keep the current candidate-side normalization only for explicitly documented path equivalences. Add malformed-file trailing-slash selftest expecting `oracle_hits_ok=false` or a receipt-shape clause failure. The observed lane-built and vendor receipts show ordinary paths without trailing slashes (V3/V4/L3/L4 inspection); this finding does not establish REA emits such paths.

## Requested-case verdict
- Two derivation roots: fail closed with no hint; correct explicit `oracle_root` selects the inner root and passes; wrong hint selecting outer root fails on missing oracle/gap rows. This is the expected behavior.
- Nonzero-offset carve: root is taken from derivation child `firmware.bin_extract/4096-6513.squashfs_v4_be_extract`; faithful child publication passes, shallow publication fails. Expected behavior.
- Path equals CR: `extract_rel(CR, CR) == ""`; it does not satisfy non-empty oracle/nonregular rows, and a root-only gap does not match a nonregular row. Expected behavior.
- `$output/` twice: in a derivation root, `strip_output()` strips once, leaving literal `$output/` in `root`; paths use `path_parts()` which strips the prefix repeatedly, so the namespace does not line up and rejects. In files, repeated prefixes are fully stripped by `path_parts()` and may still pass. The latter is loose normalization, but by itself no distinct filesystem identity is demonstrated: `$output/` is a receipt sigil, not a legal filesystem component in the documented schema.
- Removal diagnostic outside CR: wholly unrelated link fails closed. But a path with a decoy directory ending in the same CR components is accepted as a valid required symlink removal; the counter does not bind the diagnostic to the receipt’s output directory.
- Trailing slash / `./`: candidate trailing slash and interior `./` are normalized away and can pass equality. Table-row trailing slash differs: `strip_rel()` removes leading `./` and leading `/`, but not trailing slash; scenario `06e` shows gap-side candidate trailing slash normalized and accepted. This means normalization is asymmetric between receipt path and frozen row.

## Impacted axes and calibration
- **Coverage:** no false acceptance found for ambiguous roots, a wrong hint, a shallow publication, or CR itself. Faithful offset carve and explicit root hint pass. A foreign-directory removal diagnostic can count as the required disposition.
- **Calibration:** a malformed but projection-self-consistent receipt with a file’s trailing slash is accepted. Pure-function and fixture evidence makes this a fixable strictness defect, not proof the landed vendor data is wrong.
- **Depth:** handling of multiple roots and chunks is coherent for this rule: ambiguity is explicit; a frozen per-carrier hint restores deterministic resolution; root is not guessed by longest suffix.
- **Counterexample strength limitation:** custom `measure()` fixtures use a simulated rehost runner; they validate counter decision logic and binding interactions only. No `REA` process authored these mutated paths. Therefore do not reject faithful AVM extraction based on these findings alone.

## Smallest safe correction
Add two focused selftests: (a) an otherwise green required symlink disposition whose absolute removal link is `/x/decoy/<CR>/bin/link` while trusted output dir is `/x`, expected fail; (b) an otherwise green oracle file with a trailing slash in `relative_path`, expected fail (and keep leading/interior `./` tests only if intended equivalence is part of receipt contract). For (a), make `diagnostic_rel` use the task output root as a strict prefix rather than searching any segment sequence; for (b), reject a trailing slash on regular-file receipt paths before component normalization. Do not broaden root matching into suffix matching.

## Artifacts
- `summary.json` includes every result/probe; `05b-removal-decoy-segment-run.json` records the 4/4 false acceptance.
