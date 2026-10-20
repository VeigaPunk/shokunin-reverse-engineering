# SelectorModel — source-law selection preview implementation

## Files written

- `.ufo/waves/round-16/selection.py` — stdlib-only read-only CLI + `select_snapshot(root: Path, request: str, goos: str, goarch: str) -> dict`.

## Review revision applied

Static review (KaidokuR16) required and received: `fullmatch` so a trailing
newline cannot satisfy the version regex; component bound `<= 2147483647`
(Java int); diff selection via one `patchverdiffs/` listing taking the max
canonical same-minor patch `<= requested` instead of a per-patch countdown
(same result as `getPatchVerDiffFile`, no huge range walk);
`selected_patch` is `0` on `base_only` (the patch-0 base file is the byte
source) and `null` only on `missing_base`. Unchanged: unpatched-base bucket
label, no provider parity or patch-content claim.

SafetyReads static findings folded in: canonical components rejected by
length >10 before `int()` (a >4300-digit string would raise `ValueError`
inside `int()` itself), and `RecursionError` from deeply nested base JSON is
mapped to `UnreadableError` → exit 2. No broader hardening added.

W2 FSourceCells finding folded in: `patchverdiffs/` listing is skipped
entirely for `patch==0` (the Java `while (patchVer.getPatch() > 0 ...)` never
probes), `FileNotFoundError`/`NotADirectoryError` on the listing are the
valid "no diffs" case, and any other `OSError` raises `UnreadableError` →
exit 2 rather than silently yielding an empty listing.

W2 FAttackNoveltyFinal source-fidelity fix folded in: `read()` retains a
bucket only when the deserialized `GoArch` is non-null (233-235), so
`_top_level_keys` now returns only keys with non-null values — `"all": null`
is not a matching bucket. This is names-only null handling, not GoArch
schema validation: a non-null non-object value (e.g. an array) still counts
as present, and no "exact Java parser" equivalence is claimed.

Final FWaveIntegrity/Safety fix folded in: `_describe_file` uses a single
`stat()` — `FileNotFoundError`/`NotADirectoryError` or non-regular files
return "absent", any other `OSError` (e.g. EACCES) raises `UnreadableError`
→ exit 2 instead of `is_file()` silently reporting absence; `st_size` is
reused, removing the duplicate stat. Root `is_dir` failure remains
`UnreadableError`. No broad validation or snapshot-atomicity feature added.

## What it models (exact source anchors)

Source law: `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`
(extracted copy reviewed at `/tmp/GoApiSnapshot.java`; zip:
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`).

- `get()` lines 102–116: base lookup first; `EMPTY` when base absent; arch search order
  `List.of(goOS+"-"+goArch, goOS, unix?"unix":"", goArch, "all")` (108–109).
- `getApiSnapshotJsonFile()` 118–146: base is always patch-0 `go<M.m.0>.json` (122–123);
  no diff ⇒ the base file itself is the provider (128–131); diff present ⇒ runtime merge
  via `JsonPatchApplier` into a derived byte provider (133–144). The preview never merges.
- `getPatchVerDiffFile()` 148–166: scan `patchverdiffs/go<M.m.p>.json.diff` at patch
  `p, p-1, …, 1`; first present wins; patch 0 or none present ⇒ null ⇒ `base_only`.
  Implemented as a single directory listing + max selection; equivalent because
  candidate names are canonical `go<M.m.p>.json.diff` (`GoVer.toString()` at
  GoVer.java:155–159) and the scan takes the first present patch descending.
- `getApiSnapshotFile()` 168–178: filename `"<subdir>go<M.m.p>.json<suffix>"` relative to
  the supplied root (`typeinfo/golang/` prefix is the caller's root). `getApiFile()`
  183–192 (`goM.m.json` two-part fallback) is **not** a snapshot-selection path and is
  not reproduced, per contract.
- `IS_GOOS_UNIX` 180–181 reproduced verbatim.
- Bucket retention follows `read()` 205–240: top-level object keys filtered by the
  arch-name set (212–224) where a bucket counts only if its value is non-null
  (mirroring the non-null `GoArch` check at 233–235), then emitted in
  search-order priority skipping empty and already-added names (228–237).
  `base_matching_buckets` is exactly that: ordered, deduplicated,
  non-null-valued buckets of the **unpatched base file**.
- Request parsing is stricter than `GoVer.parse` (`GoVer.java` 62–81): stable `M.m.p`
  only — no two-part shorthand, no wildcard patch, no trailing decoration
  (`"1.22.8 X:rangefunc"`), no leading zeros, no trailing newline; `0.0.*`
  rejected as the `INVALID` sentinel (`isInvalid()` 105–107); each component must
  fit a Java int. Deviation is contract-mandated ("strict stable M.m.p") and
  documented in the module docstring.

## Emitted JSON

Contract keys: `requested` (normalized `M.m.p`), `status`
(`missing_base|base_only|exact_diff|fallback_diff`), `base` (`{path,size,sha256}` or
null), `selected_diff` (same or null), `selected_patch` (int: selected diff patch,
or `0` on `base_only`; `null` on `missing_base`),
`arch_search_order` ("" placeholders filtered, matching `read()`'s downstream skip),
`base_matching_buckets`, `patch_applied` (always `false`),
`evidence_class: "source_model"`. Informational extras: `request_raw`, `goos`,
`goarch`, `base_matching_buckets_source: "unpatched_base_file"` (null when base
missing) — satisfies "base-only matching is unpatched preview and must be labelled so
when diff selected", and fixture subset matching is unaffected.

`path` is reported relative to the supplied root (POSIX separators) so fixture output
is independent of the temporary-root location.

CLI: `--root --request --goos --goarch`; emission → exit 0; `RequestError`/`UnreadableError`
(root not a dir, unreadable file, non-object/invalid base JSON) → exit 2 with a
`{"status": "invalid_request"|"unreadable_input", "error": …}` body and stderr note.
Not executed here — L1 owns gate runs (`selfcheck.py` belongs to SelectorRunner).

## Status mapping

| Condition | status | base | selected_diff | selected_patch |
|---|---|---|---|---|
| `go<M.m.0>.json` absent (diffs may exist) | `missing_base` | null | null | null |
| base present, patch==0 or no diff ≤ patch | `base_only` | described | null | 0 |
| diff at exactly requested patch | `exact_diff` | described | described | patch |
| nearest diff at patch < requested | `fallback_diff` | described | described | patch |

## Limits (not modeled, by design)

- No patch application: digests/sizes are raw stored bytes only; the derived
  `go<ver>.json` document that `getDerivedByteProviderPush` would produce does not
  exist as bytes. `base_matching_buckets` therefore reflects pre-patch content —
  a diff could add/remove/rename top-level buckets.
- No `Application.getModuleDataFile` module-data search path; only the supplied root.
- No `GoApiSnapshot.EMPTY` object; `missing_base` status is the equivalent.
- `goos`/`goarch` values are not validated against a GOOS/GOARCH allowlist; they only
  need to be non-empty (mirrors Java, which passes raw strings).
- Data dir observed: 11 base `go1.15.0`–`go1.25.0.json` + 123 `patchverdiffs/*.diff`
  (no `.0` diffs) — consistent with the patch>0 scan starting at 1.
