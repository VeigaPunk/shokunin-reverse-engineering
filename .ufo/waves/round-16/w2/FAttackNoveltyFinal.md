# FAttackNoveltyFinal — w2 critic: 1.24.5 contrast and platform order vs current artifacts

Axes: depth, calibration. Static source/data/model review only. I ran no selection.py, selfcheck.py, controls.py, measure.py, build, test or lint, and installed nothing. Read-only data reads: `ls` of installed `patchverdiffs/`, plus a top-level-key scan of the 11 installed `go1.*.0.json` bases. Mutant traces below are **[INFERENCE: static trace, not executed]**.

## Verdict

The "no new source law" side **holds** (bounded no-finding). The knowledge entry (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:9`), SKILL (`SKILL.md:489-493`), README (`corpus/README.md:36`) and LOG (`LOG.md:1934`) all disclaim a new law. Every row of the r16 decision table restates law that was already held at `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:17-23,29-33`.

The "adds explicit computation" side **is falsified as currently evidenced**. Every registered installed-data invocation, and every committed fixture, gives the same answer under two shortcuts that the entry itself forbids: "highest installed patch" and "lexicographic order". Three of the docs call the 1.24.5 contrast exercised, but no artifact exercises it. The platform projection has two problems. On the only registered run it is identical to the source literal list. And at one point it misstates source law (null buckets).

## F1 — calibration, high: the 1.24.5 contrast is called "exercised" but no artifact exercises it

Claims:
- `corpus/lessons/round-16.md:73`: "the exercised contrast includes 1.24.5→patch 5 despite installed patch 6".
- `LOG.md:1935`: "new substance is explicit bounded selection (including 1.24.5 despite installed patch 6)".
- Knowledge entry `:9`: "The strongest contrast is a request for 1.24.5".
- `SKILL.md:499`: decision row.

Counter-evidence:
- Every retained or recheck argv uses `--request 1.24.7 --goos linux --goarch amd64` only: knowledge entry `:3`, `corpus/README.md:36`, `SKILL.md:506`.
- `selection-fixtures.json` and `negative-fixtures.json` contain no 1.24 case. They also contain no case where an exact diff coexists with a higher installed diff.
- `.ufo/waves/round-16/verification.json` does not exist yet.
- `measure.py:122-151` counts file presence only.
- w1 already warned that 1.24.7 alone cannot tell the computation from "report the installed minor maximum" (`w1/AttackNovelty.md:25`). The warning was adopted in prose but not in any command.

Why 1.24.7 proves nothing here (observed by `ls`): installed diffs are contiguous from 1 to the per-minor maximum in every minor. Examples: 1.24 → 1..6, 1.19 → 1..13, 1.15 → 1..15. So on installed data:
- Every request above the maximum falls back to the minor maximum.
- Every request at or below the maximum is exact.
- 1.24.7 is in the first class. Its answer equals the last element of r15 `inventory.json:7723-7729` (`patch_diffs_for_minor`), which was already held.

## F2 — depth, high: the committed fixtures cannot kill the two shortcuts the entry forbids

The knowledge entry `:22` forbids "Lexicographic order, highest installed patch irrespective of request".

- **M1 ("minor max if any eligible"):** if any same-minor positive diff is ≤ the request, select the maximum installed diff; otherwise base. It survives every positive case:
  - exact_diff {3}/r3
  - lower_fallback {2,4}/r5 → 4
  - future_diff_ignored {3,9}/r1 → base
  - windows_omission {2}/r2
  - corrupt-diff-still-selected {2}/r2
  - minor_isolation, patch0 and the missing-base cases are unaffected.
- **M2 (string-sorted patch):** all multi-diff fixtures are single-digit ({2,4}, {3,9}), so it survives too.
- The current code is correct on both points: `selection.py:228-236` uses an int compare with `0 < cand <= patch`, and `sorted(..., reverse=True)`. But no fixture pins either property.
- **Discovery gap:** the registered fixture command `SKILL.md:506` runs `selfcheck.py` with no `--fixtures`. `selfcheck.py:85` and `:357-358` then load only `selection-fixtures.json`. `negative-fixtures.json` is listed in that row's pinned values but is never run by the registered command.

## F3 — depth, medium: on the registered run the platform projection is a copy of the search order

For linux/amd64, every installed base contains all five search-order keys:
- `w1/EntryDraft.md:22` (jq read)
- r15 `inventory.json:7693-7721` for 1.24.0

So for `--request 1.24.7 --goos linux --goarch amd64`, `base_matching_buckets == arch_search_order`. The "ordered platform projection" (knowledge entry `:9`, `LOG.md:1936`) therefore adds no information beyond `GoApiSnapshot.java:108-109` and the r15 key list (r15 entry `:23` already held the ordered-applicability law).

Installed contrasts where the projection really differs, from my read-only key scan:
- `riscv64` and `linux-riscv64` are absent from all 11 bases.
- `darwin-arm64` is absent from `go1.15.0.json` only.

## F4 — depth/calibration, medium: bucket membership misstates source `:233-234` (null value)

Source:
- `GoApiSnapshot.java:222-223` stores `gson.fromJson(reader, GoArch.class)` for every kept name.
- `:233-235` retains a bucket only `if (arch != null)`.

A present key whose value is JSON `null` therefore does not match **[INFERENCE: Gson 2.13.2's reflective adapter returns null for a NULL token; the `GsonPostFixupAdapter` at `:475-480` passes it through]**. The model counts key presence instead:
- `selection.py:242` uses `keys = set(_top_level_keys(...))`.
- The comment at `:239-241` claims this matches `read()` "exactly".
- Knowledge entry `:26` ("matching top-level names") and `:38` ("top-level key membership") state the same thing.

Counterexample: base `{"all": null}` gives preview buckets `["all"]`, while source gives `arches` empty and `isInvalid()` true (`:503-505`). That is the opposite applicability conclusion.

This exact finding was raised in `w1/ReviewBucketOrder.md:14` and dropped without disposition. The contrary `w1/CraftDraft.candidate.md:27` wording won. Scope: no installed base has a null top-level value (scan: `nulls=[]` for all 11), so no installed result is wrong. This is a source-model fidelity defect, not a data finding.

## Smallest corrections (L1 integrates; I edited nothing)

1. **F1.** Add one retained L1 execution with `... selection.py --root <installed golang dir> --request 1.24.5 --goos linux --goarch amd64`.
   - Source-derived expectation (not executed): `status` `exact_diff`, `selected_patch` 5, `selected_diff.path` `patchverdiffs/go1.24.5.json.diff`, `base.path` `go1.24.0.json`.
   - Size and SHA-256 are to be observed, then cross-checked against the r15 pin at `inventory.json:7333-7335`, not used as the expected value.
   - Name this argv beside 1.24.7 in knowledge entry `:3`, `SKILL.md:506` and `README.md:36`.
   - If it is not run, reword `round-16.md:73`, `LOG.md:1935` and entry `:9` to "source-derived expectation, not exercised".
2. **F2.** Put these handwritten cases in the default-loaded `selection-fixtures.json`, or make `SKILL.md:506` pass `--fixtures` for each file:
   - `exact_despite_higher`: request `1.24.5`; files `go1.24.0.json:{"all":{}}`, `patchverdiffs/go1.24.5.json.diff:{}`, `patchverdiffs/go1.24.6.json.diff:{}`. Expected `{"status":"exact_diff","selected_patch":5,"selected_diff":"patchverdiffs/go1.24.5.json.diff"}`. Kills M1.
   - `numeric_not_lexicographic`: request `1.19.20`; files `go1.19.0.json:{"all":{}}` plus diffs 2 and 13. Expected `{"status":"fallback_diff","selected_patch":13,"selected_diff":"patchverdiffs/go1.19.13.json.diff"}`. Kills M2.
   - The `FBoundedNumeric` seat was assigned the same pair. Integrate one copy, not two.
3. **F3.** Optional installed platform contrast: `--request 1.24.7 --goos linux --goarch riscv64`.
   - Expected `arch_search_order` `["linux-riscv64","linux","unix","riscv64","all"]` and `base_matching_buckets` `["linux","unix","all"]`.
   - Otherwise qualify entry `:9` / `LOG.md:1936`: on installed linux/amd64 the projection equals the search order.
4. **F4.** Choose one of:
   - (a) Change `selection.py:242` to retain only keys whose value is not `None`. Fix the `:239-241` comment to cite `:233-235`, and change entry `:26` and `:38` to "present with a non-null value". Add fixture `null_bucket_not_retained`: request `1.21.0`, `go1.21.0.json:{"all":null,"linux":{}}`, expected `{"status":"base_only","base_matching_buckets":["linux"]}`. The current code would emit `["linux","all"]`, so this case is red until the fix lands.
   - (b) Keep presence semantics and record null as a named divergence. Add a limitation case shaped like `unsupported-shape-bucket-nonobject-preview` that expects `["linux","all"]` with an explicit divergence note.
   - Do not leave the "exactly like `read()`" comment.

None of these is an axis tradeoff the judge must reject. Each one is fixable without changing the claims' wording beyond F1's conditional rewording.

## Limits

- No selection output observed: every expected value above is source/data-derived.
- Gson null behaviour is inferred, not decompiled (`gson-2.13.2.jar` is present in Ghidra's `Framework/Generic/lib`; I did not open its source).
- linux/amd64 key presence in all 11 bases relies on `w1/EntryDraft.md:22`. I re-read 1.24.0 via the r15 inventory. Riscv64 and darwin-arm64 absence come from my own scan.
- Other w2 seats (`FBoundedNumeric`, `FBucketPriority`, `FCommandProvenance`) may report overlapping items.
- Tool installs/updates: none.
