# FDataSelection — installed Go 1.24 diff 5/6 names and identity fields

**Axes:** depth (source-law fidelity of the selected names and byte identities) and calibration (what the round-16 artifacts actually record versus what they call exercised). Scout report only; no implementation or corpus edits.

**Method.** Read-only source and data reads: shipped `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`; the `GoVer`, `GModule`, and `Application` members in the Framework source zips; the installed golang data directory (`stat`, `sha256sum`, directory listing, JSON key parse, and a text section comparison of the two diffs). No `selection.py`, `selfcheck.py`, `controls.py`, or test/gate was executed; no patch was applied; no Ghidra/Java was run. No `lsp` server answers archive members, so source anchors come from direct member reads, not semantic LSP resolution. No tool installs/updates.

**State observed (artifacts moved during the wave).** `selection.py` sha256 `c9e7eb226fb7e7cef2eba0fc85041e03cb4348d1886ff32627b3f6117a273042` (mtime 05:26:09); `selfcheck.py` `965ef53e…` (05:26:06); knowledge entry `da5cc6d5…` (05:26:24). Line anchors below are for those bytes. `.ufo/waves/round-16/verification.json` was absent at observation; per the wave contract, L1 captures final receipts after this wave.

## 1. Source law for the two names (observed)

- `GoApiSnapshot.get` `:102-116`: base lookup first; search list built at `:108-109`; absent base yields `EMPTY` (`:115`).
- `getApiSnapshotJsonFile` `:118-146`: base is `goVer.withPatch(0)` (`:122-123`); a missing base returns before any diff lookup (`:124-126`); no diff returns the base provider (`:128-131`); a selected diff is applied only at runtime through `JsonPatch.read`/`JsonPatchApplier` (`:133-145`).
- `getPatchVerDiffFile` `:148-166`: while patch `> 0`, probe `getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")` and decrement on absence (`:153-156`); first present patch wins; patch 0 never probes; a lower selection emits `Msg.warn` (`:158-161`).
- `getApiSnapshotFile` `:168-178`: name is `typeinfo/golang/<subdir>go<M.m.p>.json<suffix>` (`:169-170`), resolved through `Application.getModuleDataFile` (`:172`); absence is caught to `null` (`:175-177`). `GoVer.toString` formats a canonical ASCII `%d.%d.%d`, and `prevPatch` never moves the minor.
- Presence is `exists()` (`GModule.findModuleFile`, `GModule.java:147-155`) and **not a directory** (`Application.getDataFileInModule`, `Application.java:354-375`, directory rejection at `:369-372`). A directory therefore behaves exactly like absence and the walk continues.
- Counterpart in the produced implementation: `_DIFF_NAME_RE` (`selection.py:55-57`), `patch > 0` guard and listing (`:230-238`), same-major/minor and `0 < cand <= patch` numeric filter (`:242-245`), descending numeric pick with first describable entry (`:246-251`), and status mapping (`:264-270`).

**Installed facts (observed).** `go1.24.0.json` 10,039,962 B, SHA-256 `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571`; `patchverdiffs/go1.24.5.json.diff` 106,091 B, `5743f4335615fdc5aa8d7e3c2516a8223a3eb769ffd306b3344b79bef4ea7053`; `patchverdiffs/go1.24.6.json.diff` 118,810 B, `e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6`. All 123 installed diffs and 11 installed bases are regular files whose names match the canonical pattern (0 non-regular, 0 non-canonical); 1.24 patches 1–6 exist. These identities independently match the r15 pins (`inventory.json:7301,7333-7335,7373-7374`) and `w1/AttackNovelty.md:22-23`.

**Consequence [INFERENCE: source-model trace, not executed].** For request `1.24.5`, installed patch 6 is excluded because `6 > 5`, so the selected tuple is base `(10039962, aab28c8f…)` plus diff `(106091, 5743f433…)`, `selected_patch: 5`, `status: exact_diff`. Request `1.24.6` selects diff 6; `1.24.7` falls back to diff 6. This is filename selection only.

## 2. The two identities are not interchangeable (observed bytes)

Both files are jd-native patch text with no version or base header; the filename is the only version binding. A section comparison (independent of the implementation) gives:

- diff 5: 800 sections, 772 removed and 780 added value lines; diff 6: 897 sections, 864 removed and 877 added. These counts match the r15 inventory’s `section_count`/`added_line_count`/`removed_line_count`, which validates the parse.
- Every one of diff 5’s 800 section headers is present in diff 6; 97 sections exist only in diff 6.
- All 800 shared sections have **identical removed values**; 163 shared sections have **different added values**. Every inspected difference is a `Position` update (162 paths ending in `"Position"`, plus `runtime.casGToWaitingForSuspendG`, whose function value differs only in its `Position` field). Example: `["all","Funcs","runtime.Breakpoint","Position"]` removes the same base value in both files and adds `proc.go:5324:6` in diff 5 versus `proc.go:5363:6` in diff 6.

**Bounded reading.** The identical removed values and nested section set are consistent with both files being generated against the same `go1.24.0` base rather than as a chained delta, which is what makes Java’s single-diff application coherent. I did **not** verify that either diff applies cleanly, nor compare any patched output to a Go release snapshot. The concrete point for C1 is narrower: selecting diff 6 for a `1.24.5` request would bind different `Position` values for 163 symbols, so the exact-5-versus-installed-6 contrast is substantive at the byte level, not a filename preference.

## 3. Findings

### D1 — calibration, medium: no C1-owned identity receipt for the 1.24.5 contrast; the registered recheck is 1.24.7-only

- The current entry says in the present tense that “exact installed artifacts selected by `.ufo/waves/round-16/selection.py` carry separate size/SHA-256 identities” (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:1`), and names `1.24.5` as the strongest contrast (`:9`).
- Its recheck runs only `--request 1.24.7` (`:3`). `SKILL.md:506` now says “repeat with `--request 1.24.5` for the bounded contrast”, so the registered documentation already disagrees on the argv. `verification.json` does not yet exist (expected before final receipts), and no fixture carries a 1.24 case.
- Diff 5’s identity therefore has no round-16-owned record: it exists only in the prior inventory (`inventory.json:7301,7333-7335`) and is repeated in `w1/AttackNovelty.md:22` (which correctly labels the *selection outcome* as inference, not the identity).
- **Smallest correction.** Add the `1.24.5` argv beside `1.24.7` in the entry recheck and in the execution addendum, and have the receipt record `selected_diff` `106091`/`5743f433…`, `base` `10039962`/`aab28c8f…`, `selected_patch: 5`, and the expected buckets `["linux-amd64","linux","unix","amd64","all"]` (the installed base has all five as non-null objects; 27 top-level buckets, no nulls). Alternatively keep the 1.24.7-only recheck and reword entry `:1`/`:9` as a source-derived expectation until the receipt exists. Do **not** move these observed hashes into handwritten fixture expectations; the entry’s own rule is that hashes/sizes are observed separately (`:50`).
- Overlap: FAttackNoveltyFinal F1 already reports that the 1.24.5 contrast is unexercised. This finding adds the identity-field provenance and the exact values the receipt must match; it does not duplicate the novelty verdict.

### D2 — calibration, low: the candidate entry digest table omits diff 5

`w1/EntryDraft.candidate.md:4` rechecks `Base-src.zip`, `go1.24.0.json`, and `go1.24.6.json.diff`; the table at `:19-23` pins the base, diff 1.24.1, and diff 1.24.6, but not diff 1.24.5. If that draft is the integrated entry form, the flagship `1.24.5` identity cannot be rechecked from the entry. Add the diff-5 row (values in §1) or cite the retained receipt. If the current entry form wins, this is moot and D1 governs.

### D3 — bounded corrections (no defect, no new fixture)

- **Directory-masquerade question resolved.** `w2/FBoundedNumeric.md` observation 1 left `Application.getModuleDataFile` directory semantics unverified “from Base-src.zip alone”. The Framework source answers it: `Application.java:369-372` throws `FileNotFoundException` for a directory, `GoApiSnapshot.getApiSnapshotFile` catches it to `null` (`:175-177`), and the walk continues. `selection.py:130` (`is_file()`) does the same. A directory named `go1.24.5.json.diff` is therefore absent in both, and the lower patch is considered in both. No divergence and no fixture worth authoring.
- **Digit-run concern is unreachable.** The unbounded `[0-9]*` components in `_DIFF_NAME_RE` (`selection.py:55-57`) cannot trip Python’s int-string limit through a real filename: Linux `NAME_MAX` is 255 bytes, and the whole basename is one component, far below the 4300-digit default (and below the 640-digit minimum configurable threshold). This concurs with `w2/FSourceDiffOrder.md` §2 and supersedes the reachability claim in `w2/FSourceCells.md` F5. Do not add a check.
- **Special files and unlistable directories** remain the only presence divergences (FIFO/socket/device named as a diff is present to Java but rejected by `is_file()`; an unlistable directory now raises in the current code at `selection.py:236-238`, a documented refusal). They are already reported in `w2/FSourceDiffOrder.md` §2 and do not occur in the installed data (all 123 diffs are regular).

### D4 — bounded no-finding on the assigned names and identity fields

- The installed `go1.24.5.json.diff` and `go1.24.6.json.diff` names and size/SHA-256 identities recorded in the artifacts that carry them (`inventory.json:7301,7333-7335,7373-7374`; `w1/AttackNovelty.md:22-23`) are correct against the installed bytes.
- The current selector logic reproduces the source walk for regular files: same-minor, positive, not-above-request, descending numeric pick, first describable entry, exact versus fallback from `diff_patch == patch`.
- No current artifact claims patched-content equality for these files. The entry rejects it explicitly (`:21`, `:24`, `:40`), the lesson rejects it (`corpus/lessons/round-16.md:20`), and `selection.py` forces `patch_applied: false` / `evidence_class: "source_model"`. `exact_diff` is defined as exact requested filename, never a computed snapshot digest (`entry:40`).
- The current bytes also contain the planned fixes named by L1: non-null bucket retention (`_top_level_keys`, `selection.py:147+`), request length before `int()` (`:87-90` region), and permission failures on the diff listing raised as unreadable input (`:234-238`). No data-selection defect in those paths was found for installed 1.24.

## Limits

- No execution of the selector, fixture runner, controls, or any gate; no Java/Ghidra run; no patch application. The `1.24.5` outcome above is a source-law trace, not an observed run.
- The diff 5/6 comparison is text-section analysis of the two stored files. It establishes distinct byte identities and differing added values; it does not establish applicability to the base, successful `JsonPatchApplier` behaviour, or equality with any release snapshot.
- Source anchors are shipped source bytes, not the classes loaded by the installed Ghidra; no source/bytecode parity is claimed.
- Artifacts changed during this seat; findings are pinned to the hashes at the top. No tools installed or updated.
