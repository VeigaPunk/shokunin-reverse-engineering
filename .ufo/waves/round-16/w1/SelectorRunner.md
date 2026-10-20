# SelectorRunner — selfcheck.py report

## Files changed
- `.ufo/waves/round-16/selfcheck.py` (new, executable; only assigned file)
- `.ufo/waves/round-16/w1/SelectorRunner.md` (this report)

## Behavior implemented
- Imports `selection.py` via `importlib.util.spec_from_file_location` from the script's
  own directory (default: sibling of selfcheck.py; `--selection PATH` override). No
  `sys.path` mutation, no package install. `sys.dont_write_bytecode` is raised around
  `exec_module` and restored in `finally`, so importing cannot leave `__pycache__`
  under the live wave dir and the documented `python3 -I` argv stays as exercised.
- Each case gets a fresh `tempfile.TemporaryDirectory(prefix="selcheck-")` root —
  the prefix is fixed so arbitrary fixture `id` text (including `/`) cannot affect
  the temp path; `id` is display-only. The case's `files` mapping is materialized
  relative to the root. Rejects absolute paths and `..` escapes. Temp dir is
  removed after the call — no live-tree writes.
- Subset comparison of `expected` against `select_snapshot()`'s dict:
  - `base` / `selected_diff`: a string expectation containing `/` is compared against
    the actual path **relative to the case temp root** (so
    `"patchverdiffs/go1.24.5.json.diff"` asserts the subdirectory); a string without
    `/` compares basenames only. Object expectations recurse, with `"path"` normalized
    the same way. `null` expectations are plain equality (expect `null` → actual must
    be `None`). Paths outside the root fall back to their absolute spelling so they
    mismatch explicitly.
  - `patch_applied` forced to literal `False` (identity compare, so `0` fails) and
    `evidence_class` forced to `"source_model"` on every non-error result.
  - Other keys: equality; lists in order (pins `arch_search_order`,
    `base_matching_buckets` ordering); booleans by identity.
  - Presence precedes every comparison: a key absent from the result reports
    `key missing` — an expected `null` never passes on absence (W2 finding 1).
  - Authored expectations for `patch_applied`/`evidence_class` are still compared
    against the actual value, so a conflicting fixture value fails loudly rather
    than being silently discarded by the forced pass (W2 finding 3).
  - Positive cases must author at least one non-forced key — an `expected` that is
    empty or names only `patch_applied`/`evidence_class` is a `FixtureError`
    (harness failure), since forced keys carry no source-selection content
    (W2 finding 4). Convention relayed from L1 to the model owner:
    `base_only`/`exact_diff`/`fallback_diff` carry `selected_patch` as `0`/int,
    `missing_base` as `null`.
  - Integer expectations are exact-int: a bool actual (`False`/`True` == 0/1) never
    satisfies an int expectation (repeated-W2 finding).
- `--fixtures` repeatable; default is sibling `selection-fixtures.json`. Top level may be
  `{"cases": [...]}` or a bare list.
- Prints `PASS <id>: status=… base=… selected_diff=… selected_patch=…`, `FAIL <id>:`
  plus every differing dotted key and the full actual result JSON, or `ERROR <id>:`
  for per-case schema violations. Summary line; exit `0` all pass, `1` any case
  mismatch, `2` harness-level failure — per-case `FixtureError` prints `ERROR` and
  drives exit 2, never counted as a case FAIL.
- Materialization/input failures (bad `raw_b64`, unwritable or invalid fixture
  path, non-UTF-8 fixtures file read in `_load_cases`) convert `ValueError`/
  `TypeError`/`OSError`/`UnicodeError` to `FixtureError` → `ERROR <id>` → exit 2;
  they are never confused with model exceptions under `expect_error`.

## Schema extensions (kept minimal, declared in docstring)
- `expect_error` (optional): `true` = any `Exception`; string = substring of type name or
  message; `{"type": T, "contains": S}` = type-name/message substring match. Absence ⇒ a
  raise is a failure. Supports NegativeFixtures' malformed-version/negative-patch cases
  without coupling to `select_snapshot`'s exact exception choice.
- `files` values: `{}`/`[]` → written as JSON document; plain string → verbatim text
  (unreadable-JSON fixture); `{"raw": str}` and `{"raw_b64": s}` explicit escape forms.
  Other scalar types → `FixtureError` (covers "unsupported shape" cases at fixture level).

## Source anchors the comparisons encode (S003, Base-src.zip …/rtti/GoApiSnapshot.java)
- `get(...)`: archSearchOrder = `[goOS+"-"+goArch, goOS, IS_GOOS_UNIX? "unix" : "", goArch, "all"]`.
- `getApiSnapshotJsonFile`: `baseVer = goVer.withPatch(0)`; base file via
  `getApiSnapshotFile(baseVer, "", "")` → `typeinfo/golang/go<M.m.0>.json`; null ⇒ null
  provider (⇒ `missing_base`, no diff consulted).
- `getPatchVerDiffFile`: `while patch>0` try `patchverdiffs/go<M.m.p>.json.diff`,
  `prevPatch()` descent ⇒ nearest lower diff; warns only when `patchVer != goVer`;
  patch 0 ⇒ null diff (⇒ `base_only` for p=0; `base_only` vs `*_diff` status split is
  modelled by selection.py per contract).
- `getApiSnapshotFile` name: `"typeinfo/golang/%sgo%s.json%s"` (subdir + `go`+ver +
  suffix). `getApiFile` (`goM.m.p.json` then `goM.m.json` fallback) is a separate utility
  and is intentionally not modelled.
- `read(...)`: HashMap parse then `LinkedHashMap` rebuilt in `archNames` order, skipping
  null/empty names ⇒ ordered dedup, missing buckets omitted (`base_matching_buckets`).
- Installed data confirms naming: `…/typeinfo/golang/go1.15.0.json … go1.25.0.json` at
  root and `patchverdiffs/go1.15.1.json.diff`-style names (123 diff files observed).

## Limits / calibration
- Not executed here: `selection.py` and the fixture JSONs are sibling-seat deliverables
  (SelectorModel, SelectorFixtures, NegativeFixtures); per wave rule this seat never runs
  checks. `selfcheck.py` fails cleanly (exit 2) until selection.py exists. Only
  verification performed: in-memory `ast.parse` syntax check (no pycache written; none
  found under round-16).
- String expectations for `base`/`selected_diff` without `/` compare basename only —
  by design; use `/` (root-relative) for subdirectory assertions and object form for
  size/sha256.
- `expect_error` accepts any `Exception`, not `SystemExit`/`KeyboardInterrupt`
  (deliberate: a library API raising SystemExit is a defect, and string/dict specs let a
  fixture name a type).
- Cases run sequentially in fixture order; no parallelism (boring, deterministic output).

## Risks / blockers
- None blocking. If NegativeFixtures picks a different error field name than
  `expect_error`, those cases will land as ordinary subset checks that likely expect a
  return — schema note sent to KaidokuR16.

## Tool installs/updates
- None.
