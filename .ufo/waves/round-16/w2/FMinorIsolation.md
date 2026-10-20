# Round 16 · w2 · FMinorIsolation — major/minor isolation adversarial fixtures

Seat: `KaidokuR16.FMinorIsolation` (leaf; no dispatch, no subagents, no execution).
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Deliverable

Wrote `.ufo/waves/round-16/w2/MinorIsolation-cases.json`: 13 handwritten, schema-conforming
fixture cases (bare-list top level; `id`/`request`/`goos`/`goarch`/`files`/`expected` per the
`selfcheck.py` docstring schema; `expect_error` + `note` per `negative-fixtures.json`
convention). JSON structure and per-case `expected`/`expect_error` exclusivity were
machine-validated; `selection.py`/`selfcheck.py` were **not** executed (per contract — L1 runs
selfcheck once post-integration). No invented hashes: expectations pin `status`, `requested`,
`base`/`selected_diff` `path`, `selected_patch`, `arch_search_order`, `base_matching_buckets`,
`patch_applied`, `evidence_class` only — all hand-derivable from source law.

## Source law exercised (S003, `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`)

- Base is always `goVer.withPatch(0)` probed **first**; absent base → null → `EMPTY`, before any
  diff lookup (`:122–126`; `get` returns EMPTY `:114–116`).
- Diff search `getPatchVerDiffFile` decrements `prevPatch()` starting at the requested patch —
  it can only ever name files in the requested `major.minor` (`:153–156`; `GoVer.prevPatch`
  GoVer.java:134–136). Guard `patch > 0` excludes patch 0 (`:154`).
- Filenames are exact `typeinfo/golang/%sgo%s.json%s` with `subdir` = `""` (base) or
  `"patchverdiffs/"` (diff) — location is part of the path, no recursion, no glob (`:168–172`).
- `getApiFile` `go%d.%d.json` two-part fallback (`:183–192`) is off the `get` path; correctly
  not modeled.
- Installed data shape confirmed: `typeinfo/golang/` holds `go1.25.0.json` and **zero**
  `go1.25.*` diffs; highest diff is `go1.24.6.json.diff` (123 diffs, minors 1.15–1.24). The
  assigned attack mirrors the real installation.

## Attack coverage (assigned C1 targets + independent extensions)

| Case | Attack |
|---|---|
| `w2-mi-lower-minor-diff-not-rescued` | **Assigned:** 1.25.3 request, `go1.25.0.json` present + `go1.24.6.json.diff` → `base_only`, `selected_patch` 0. Cross-minor fallback dies. |
| `w2-mi-neighbor-base-not-rescued` | **Assigned:** 2.0.0 request, `go1.25.0.json` + `go1.25.9.diff` → `missing_base`. Neighbor base/diff cannot rescue. |
| `w2-mi-forward-base-not-rescued` | Reverse direction: 1.24.9 request, same-minor diff present but no `go1.24.0.json` → `missing_base` (base gates diff). |
| `w2-mi-exact-diff-no-base` | Exact `go1.25.7` diff + lower-minor diff, no base → `missing_base` (diff-first order dies). |
| `w2-mi-same-patch-other-minor` | `go1.24.3.diff` vs request 1.25.3: patch-number equality across minors must not match. |
| `w2-mi-cross-major-high-patch-diff` | 2.0.7 request + `go1.25.9`/`go1.25.3` diffs → `base_only`; patch-only numerics never cross major. |
| `w2-mi-cross-minor-both-directions` | 1.25.9 bracketed by `go1.24.6` and `go2.0.1` diffs → `base_only`. |
| `w2-mi-patch-zero-diff-name-ignored` | `go1.25.0.json.diff` present, request 1.25.4 → `base_only`; patch 0 is never a diff (`:154` guard). New vs w1 `patch0` (which requested patch 0). |
| `w2-mi-leading-zero-diff-name-ignored` | `go1.25.03.json.diff` invisible — canonical `GoVer.toString` names only; tolerant parsers fail this. |
| `w2-mi-diff-at-root-not-scanned` | `.diff` at root, not under `patchverdiffs/` → `base_only`; subdir is part of the path. |
| `w2-mi-nested-diff-not-scanned` | `patchverdiffs/nested/go1.25.3.diff` → `base_only`; recursive scanning (rglob) fails. |
| `w2-mi-base-inside-patchverdiffs` | `patchverdiffs/go1.25.0.json` + exact diff → `missing_base`; name-only base search dies. |
| `w2-mi-unreadable-base-not-diff-rescued` | Raw-string malformed `go1.25.0.json` + exact & lower-minor diffs → `UnreadableError` (`expect_error` type-map form; exercises the raw-string `files` value). Java parses the whole base in `read()` (`:205–239`); a corrupt base is IOException-class, never `missing_base`, never a diff result. |

## Assessment of produced artifacts (bounded, source-diff only — nothing executed)

`selection.py` checked against the source law in my lane:

- Diff selection (selection.py:223–237) lists `patchverdiffs/` once, fullmatches
  `go<M>.<m>.<p>.json.diff`, requires same `major`/`minor`, `0 < p <= request`, takes max —
  equivalent to the `prevPatch` countdown first-hit; no cross-minor/major path exists.
- Base lookup (selection.py:194–198) probes exactly `go<M>.<m>.0.json` at root before the diff
  scan; `missing_base` short-circuit present. No `getApiFile` fallback reproduced.
- `selected_patch` 0-with-base / null-without (selection.py:267, 207) consistent with both
  fixture files' conventions.
- `_DIFF_NAME_RE` fullmatch rejects leading-zero names — matches canonical-name-only probing.

**Defects in my lane: none found** (bounded no-finding). Two residual divergences recorded,
both below fixture expressibility:

1. `diff_dir.iterdir()` wraps in `except OSError: entries = []` (selection.py:219–222): a
   `patchverdiffs` *file* (not dir) yields `base_only`. Java's `getModuleDataFile` would also
   return no resource — consistent; not a divergence.
2. Ordering: Python selects the diff **before** parsing the base (diff scan at :218–237 vs
   `_top_level_keys` at :242); Java reads the diff file (JsonPatch.read) before the base JSON
   (`:136–138`). Both produce an error outcome for malformed inputs either way — observable
   only in which error, and unreadable-diff states can't be materialized by the fixture
   schema (no chmod control) — noted as schema limit, matching `negative-fixtures.json`
   `missing-base-empty-root`'s documented nonexistent-root limit.

**Expressibility limits of the schema (not defects):** cannot create directories, symlinks,
permissions, or a nonexistent root; so "directory named `go1.25.3.json.diff`", symlinked
base/diff, and unreadable-permission files are untestable — same class of limit already
recorded by NegativeFixtures.

## Overlap / independence

`w2-mi-exact-diff-no-base` and negative-fixtures' `missing-base-diff-present-unreachable`
share the base-gates-diff rule; mine differs in distractors (exact + cross-minor diff,
request 1.25.7) and is the explicitly assigned attack. All other cases are new ground —
no existing case attacks cross-minor/cross-major diff selection, diff placement, or
non-canonical diff names.

## Files

- Written: `.ufo/waves/round-16/w2/MinorIsolation-cases.json`, this report.
- Read only: `selection.py`, `selfcheck.py`, `controls.py`, `selection-fixtures.json`,
  `negative-fixtures.json`, `claims.json`, `wave2-spec.json`, `round-15-verifier-spotcheck.md:181–188`,
  w1 reports (ReviewMinorIsolation, NegativeFixtures, ReconstructSelector/History/Data,
  ReviewExactDiff, ReviewLowerDiff, ReviewBucketOrder, ReviewFixtureIndependence),
  `Base-src.zip` member `GoApiSnapshot.java` (`unzip -p` lines 102–195), installed
  `typeinfo/golang/` listing (`ls` only).

## Tooling

Installs/updates: none. Commands used were read-only (`unzip -p`, `ls`, `grep -c`,
one `python3 -c json.load` on the file this seat authored — structural syntax validation of my
own deliverable, not a run of any project artifact).

Report: .ufo/waves/round-16/w2/FMinorIsolation.md
