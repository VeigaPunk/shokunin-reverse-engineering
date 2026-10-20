# FSourceCells — round-16 wave 2 source-read report

Scope: `controls.py` split-column-11 (`USED_BY_COLUMN`) used-by handling, checked against the actual uncommitted `corpus/SOURCES.md` delta. Adjacent defects noted in `selection.py` / `selfcheck.py` where the acceptance asked for them.
Method: source reads, `git show HEAD:` blob, `git diff`, and read-only awk/grep field counts over the table. Nothing was executed (no `controls.py`, `selection.py`, `selfcheck.py` or tests run).
Tooling: none installed or updated.

## 1. Hand-check of the existing delta (no defect)

- The index is correct. The header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` has 11 cells. Every S-row splits on `|` into 13 fields: index 0 is `''`, index 11 is used-by, index 12 is the trailing `''`. Field-count check: 23/23 rows NF=13 in both HEAD and the worktree (`corpus/SOURCES.md:7-29`).
- HEAD vs worktree, cell by cell, over all 23 IDs: the only differing cell is used-by on **S003** and **S023** (`corpus/SOURCES.md:9`, `:29`). No other cell, no row add or remove, no ID change. The `## Paths`/search-log hunk (`corpus/SOURCES.md:44-48`) is outside the table.
- Old used-by values are exact prefixes of the new ones: S003 gains `corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md`; S023 gains `corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md`.
- All 7 distinct referenced targets exist in the worktree (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md`, `corpus/lessons/round-16.md`, plus the pre-existing ones). Round-15's "premature used-by reference" failure (`corpus/lessons/round-15.md:67`) does not recur in the current state.
- Conclusion for the current artifact: `controls.py` would report `immutable_cells_unchanged: true`, `allowed_used_by_deltas` = {S003, S023}, `added_rows: []`, `removed_rows: []`. My hand-check agrees with that expected output. No current-artifact defect.
- Caveat: `controls.py` reads only git objects (`git show <rev>:` / `ls-tree`). The used-by edit is uncommitted, so the control cannot see it until it is committed and cited as an AFTER revision. L1 must pass a commit that contains the edit, not the worktree.

## 2. Findings (ranked)

### F1 — Medium, false negative: duplicate source IDs silently collapse
- `controls.py:136-150` (`source_rows`): the result is a dict keyed by `row[1].strip()`. A later row with the same ID overwrites an earlier one, so only the last occurrence is compared.
- Counterexample by reading: AFTER contains `| S003 | … tier A … |` followed by a clean `| S003 | … |` copy. The mutated first row (for example a changed `tier` or `teaches` cell) is discarded; `immutable_cells_unchanged` stays `true`.
- Consequence: `rows_after` (`controls.py:237`) counts unique IDs, not rows. A duplicate insertion is neither counted nor reported as an added row (`:241` only sees unique keys).
- The current table has no duplicate IDs (23 rows, 23 unique), so this is latent. Fix direction for L1: fail closed (exit 2 or a `duplicate_ids` violation) when an ID occurs more than once in either revision.

### F2 — Medium, control overclaim: used-by delta is accepted on any old→new value
- `controls.py:231-232`: any change at index 11 goes into `used_by_deltas`, which is reported as `allowed_used_by_deltas`. There is no check that the old entries are retained (subsequence/prefix), no duplicate check, and no existence check on the new targets.
- Counterexample by reading: an AFTER that rewrites S003's used-by to only `corpus/lessons/round-16.md` (deleting five prior references) yields `immutable_cells_unchanged: true` and an entry under "allowed". The name asserts a permission the code never checks.
- The round-15 failure mode is exactly "registry used-by extended before targets existed" (`corpus/lessons/round-15.md:67`). The control checks neither the target existence nor the append-only shape, even though round-16's lesson describes the edit as "permitted old→new used-by lists".
- Fix direction: either rename to `used_by_changed` and document that permission is not checked, or add (a) old-entries-are-subsequence and (b) every new entry resolves to an existing file at AFTER.

### F3 — Low–Medium, calibration: "immutable" is table-only and whole-file claims are unobserved
- `controls.py:136-150` and `:216-243` compare only lines matching `SOURCE_ROW`. Everything else in `corpus/SOURCES.md` (`## Paths` at `:31-39`, `## Search log` at `:41-47`, `## Leads (unopened)` at `:49-55`) is outside the check. There is no byte-prefix or blob-SHA check for `SOURCES.md`, unlike `LOG.md` (`prefix_report`).
- Counterexample by reading: deleting a Leads bullet or rewriting a Paths sentence leaves `immutable_cells_unchanged: true`. A reader of "immutable cells unchanged" could take it as "file unchanged except used-by". Round-14/15 lessons (`corpus/lessons/round-14.md:49`, `corpus/lessons/round-15.md:39`) use "only used-by changes" language; the control does not support that for non-table text.
- Fix direction: add a non-table diff report or state the table-only scope in the output field name and the module docstring.

### F4 — Low, selection.py: unreadable diff directory silently becomes base_only
- `selection.py:219-222`: `except OSError: entries = []` converts any `iterdir()` failure (permission denied, not-a-directory, I/O error) into "no diffs". The result is `status: base_only`, `selected_patch: 0`, exit 0.
- This contradicts the module's own contract: unreadable input must exit 2 (`UnreadableError` at `selection.py:65-67`, and `main` at `:294` exits 2 on it). Only a missing directory should mean "no diff".
- [INFERENCE] I did not verify Java's `getPatchVerDiffFile` behavior for an unreadable `patchverdiffs/`, so I cannot say whether the Java side would also fall back. The preview's silent degrade is still inconsistent with its own stated contract.
- Fix direction: treat `FileNotFoundError` on the directory as empty; raise `UnreadableError` for other `OSError`s.

### F5 — Low, selection.py: unbounded digits in diff file names escape the exit-2 contract
- `selection.py:55-56` (`_DIFF_NAME_RE`) has unbounded `[0-9]*` components. `selection.py:226-227` runs `int(m.group(1))`, `int(m.group(2))` and `int(m.group(3))` on every matching name.
- Adversarial filename `patchverdiffs/go1.22.<4301+ digits>.json.diff` raises `ValueError` (CPython int-string digit limit, [INFERENCE] Python ≥3.11 default; I did not check the runtime version). `main` (`selection.py:294`) catches only `RequestError` and `UnreadableError`, so this is an uncaught traceback with exit 1, not the documented exit 2.
- The request path is safe: `selection.py:91` checks `len(g) > 10` before `int()`, and that guard is correct.
- Fix direction: bound the component lengths in `_DIFF_NAME_RE` (for example `[1-9][0-9]{0,9}` plus `0`), or catch `ValueError` in the candidate loop.

## 3. Bounded no-findings (checked, not defects)

- **Positional split fails closed on shifts.** `split('|')` is not GFM-aware (`\|` escapes and pipes inside backticks are not handled). I checked the current table for `\|` and for odd backtick counts: none. If a future cell inserts a pipe before index 11, every later index shifts; index 12 compares `''` against a non-empty used-by, so `immutable_violations` becomes non-empty. The positional check does not silently pass a shifted row. Latent limit only.
- **`SOURCE_ROW` regex** (`controls.py:41`) requires `^\|\s*S\d{3,}\s*\|`. Malformed IDs drop out of both revisions consistently, which is the fail-closed direction if an ID is edited (`row_absent_at_after`, `:224`).
- **Whitespace-only edits** are invisible because cells are `.strip()`-ed (`:145-147`). Acceptable; no content change.
- **`craft_section`** anchor `## Queue-drain craft ` (`controls.py:113`) matches `SKILL.md:81` (`## Queue-drain craft (rounds 5-12, ...)`), so the function resolves. I did not audit its citation counts.
- **Dead branch**: `controls.py:146` (`if index < len(row) else ""`) is unreachable because `enumerate(row)` never exceeds `len(row)`. Cosmetic.
- **`git()`/`Rev` decode**: `Rev.__init__` and `resolve` catch `CalledProcessError`/`OSError` but not `UnicodeDecodeError` on `ls-tree -z` output with non-UTF-8 paths (`controls.py:50-52`, `:70-74`). Exit 1 instead of the documented 2. Low.
- **selfcheck.py**: duplicate case IDs are not rejected (`selfcheck.py:383-396`), so a duplicated fixture id reports two independent PASS lines. Harness-only, low.

## 4. Limits

- No execution. Every finding is a code-reading claim with a stated counterexample; none was run. L1 should confirm F1 and F2 with a fixture (duplicate-ID AFTER; used-by-replaced AFTER) once, after integration.
- Only the current worktree and HEAD were inspected. I did not audit historical SOURCES revisions beyond the single HEAD blob.
- `controls.py` is not a gate. Its output fields carry no verdict, so F2 is a naming and calibration defect, not a pass-through of an invalid edit under a gate.

## 5. Verification gaps for L1

- The used-by edit is uncommitted. `controls.py` cannot observe it until committed; L1 must cite a commit containing the edit as AFTER.
- Run `controls.py` once after integration against the real BEFORE/AFTER commits, and check that its `allowed_used_by_deltas` matches section 1.
- F4/F5 need one run each with a constructed fixture directory to confirm the uncaught/silent behavior; this wave did not run them.
