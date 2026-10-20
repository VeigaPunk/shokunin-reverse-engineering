# FWaveIntegrity — round16 wave2 advisory audit

Scope: static audit of round-16 C1 (`selection.py`, `selfcheck.py`, `selection-fixtures.json`, `negative-fixtures.json`) and C2 (`controls.py`, `documentation-red.json`, and the four routed anchors). Read-only. Nothing executed: no selfcheck, controls, or selection runs; no tests, builds, linters, or formatters. No file edited except this report. Installs: none.

Evidence-class note: line numbers are from the current worktree. Stdlib behaviour cited from `/usr/lib/python3.14/pathlib/_os.py:427-440` (delegates to `os.path.isfile`, which returns False on stat errors). Items marked [INFERENCE] are reasoned from source, not observed by execution.

## Verdict

C1 selection model: source-law match is good on every point I could check. Two real defects: silent absence on unreadable input (F1) and an exit-code contract break in the selfcheck runner (F2). Fixture coverage is missing several traps.

C2 controls and routed anchors: all four routed anchors are present in the worktree by static grep. The producing-command and red-control checks are weak (F9).

## Defects (ordered by severity)

**F1. Unreadable root or patchverdiffs is reported as absence, exit 0 (medium).**
- `selection.py:130-131` (`_describe_file`): `if not path.is_file(): return None`. In 3.14 `is_file` delegates to `os.path.isfile`, which swallows stat errors and returns False. A base that exists but cannot be stat'd (e.g. root mode 0644, no search bit) becomes `missing_base`, exit 0.
- `selection.py:191-192`: `root.is_dir()` only stats the root itself, so a root without `x` passes this gate.
- `selection.py:218-222`: `except OSError: entries = []` swallows unreadable or non-directory `patchverdiffs/`. Result is `base_only` (exit 0) as if no diff exists.
- Contract violated: `selection.py:66-67` (exit 2 = unreadable), `selection.py:294-300`, and the entry's own claim at `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:34` ("exit 2 means ... required read/parse could [not be performed]").
- Not covered by any fixture (`files` cannot express permissions).
- Repair direction: `os.stat` with explicit `PermissionError`/`OSError` → `UnreadableError` at the base and root checks; for `iterdir`, treat only `FileNotFoundError` as empty and raise `UnreadableError` otherwise. [INFERENCE on the stat semantics; not executed.]

**F2. selfcheck exit code contradicts its own docstring (medium, developer-facing).**
- `selfcheck.py:63-65` documents exit 2 for "malformed case schema" and `:304-307` calls an empty `expected` "a harness error, not a vacuous pass".
- Actual: `run_case` raises `FixtureError` (`:305-307`, `:287-302`); `main` catches it per case at `:388-390`, prints `FAIL ... fixture error`, and only the final `return 0 if npass == len(cases) else 1` at `:399` decides exit. Malformed schema therefore exits 1, not 2.
- Also the per-case path does not distinguish harness faults from mismatches in the summary line `:397-398`.

**F3. Expected `0` matches actual `False` (low).**
- `selfcheck.py:207-213` (`_match`): boolean identity is enforced only when the *expected* value is bool. For expected int 0 vs actual `False`, `False != 0` is False, so it passes. Same for expected 1 vs `True`. The docstring (`:59-61`) advertises identity compare for booleans generally.
- Live exposure: `selected_patch` is an integer field; a regression that returned `False` there would pass the fixture expecting `0`. [INFERENCE: no current result has that shape.]

**F4. `_materialize` marker collision (low).**
- `selfcheck.py:133-144`: any JSON object with key `raw` or `raw_b64` is treated as a content marker, not as data. A snapshot bucket named `raw` cannot be expressed in a fixture file; it either raises `FixtureError` or is written as text. No current fixture hits this; it is a latent trap for future fixtures.

**F5. `expect_error` accepts too much (low, calibration).**
- `selfcheck.py:268-283`: `true` accepts any `Exception` (documented at `:40`), so an `AttributeError` or `NameError` bug in `select_snapshot` passes any case that uses `true`. Current negatives all use typed specs (`RequestError`, `UnreadableError`), so no current case is exposed.
- An empty string spec `""` matches any exception (`spec in name` is True for `""`). Not documented.

**F6. controls.py duplicate SOURCES IDs silently collapse (low-medium).**
- `controls.py:136-150` (`source_rows`) builds a dict keyed by source ID; for duplicates the last row wins. `sources_registry` (`:216-243`) then compares only that last row.
- An edit to the first occurrence of `S00n` in the AFTER revision is invisible, and `immutable_cells_unchanged` can report True. This weakens the append-only/immutable claim for SOURCES.md specifically.

**F7. controls.py citation regex drops non-conforming names silently (low).**
- `controls.py:42-44` (`RULE_REF`): `[a-z0-9-]+\.md` ignores citations with uppercase or underscores. `findall` skips them, so a rule with one good and one bad citation counts as resolved (`:117-128`).
- The docstring (`:106-108`) frames this as "existence plus in-range", so this is a bounded-check hole, not a false claim, but it is not disclosed.

**F8. controls.py decode failure escapes its error contract (low).**
- `controls.py:51` and `:71` decode `git` output as UTF-8 with `text=True`. `Rev.__init__` catches only `CalledProcessError`/`OSError` (`:72-73`). A non-UTF-8 path in a tree raises `UnicodeDecodeError` → traceback, exit 1, not the documented exit 2 (`:16`).

**F9. Producing-command check is trivially satisfiable (calibration).**
- `documentation-red.json` argv program: `'argv' in co` where `co` is controls.py. Any Python file that uses `sys.argv` satisfies this, including the docstring. The "producing_command_retained" check therefore cannot distinguish a retained command from a retained mention of argv.
- It still goes red at baseline only because controls.py is absent at `6235498` (`co == ''`). The red control is valid as a red-before for this reason, not because the check is discriminating.

**F10. Error JSON reuses `status` with an undocumented vocabulary (low, calibration).**
- `selection.py:294-297` emits `status: "invalid_request"` / `"unreadable_input"`. The documented preview vocabulary is `missing_base | base_only | exact_diff | fallback_diff` (`selection.py:184`). A consumer switching on `status` can misread an error as a preview state.

**F11. Silent divergence on directory or broken-link diff candidates (low, untested).**
- `selection.py:232-237`: candidates whose `is_file()` is False are skipped and selection falls to an earlier patch. Java `getApiSnapshotFile` (`GoApiSnapshot.java:168-178`) returns the `File` from `getFile(true)` without an isFile check. A directory named `go1.21.4.json.diff` would be skipped in Python and selected (then failed) in Java. Not covered by any fixture.

## Scope limits (disclosed in the report, not defects)

- Single `--root` replaces Java `Application.getModuleDataFile` (`GoApiSnapshot.java:170`), which can search multiple module data roots (installed plus extension/user). Extension snapshots are invisible to the preview.
- `(0,0,*)` requests are rejected (`selection.py:97-101`, exit 2). Java sees `GoVer.INVALID` and returns `EMPTY` (`GoApiSnapshot.java:115,242`) → `missing_base`. Divergence is intentional and documented in the docstring, but no negative fixture pins it.
- `base_matching_buckets` is the unpatched base file (`selection.py:269-272`), labelled `base_matching_buckets_source: unpatched_base_file`. See the no-finding below.

## Coverage gaps in fixtures

Positive set (`selection-fixtures.json`, 9 cases) and negative set (`negative-fixtures.json`, 17 cases, 8 `expect_error`):

- No request with a two-digit patch (`1.21.10` vs `1.21.2`). The numeric-vs-lexical trap is untested. Code sorts by `int` (`selection.py:226-232`), so it is correct; the fixture is missing.
- No `(0,0,x)` negative (`0.0.1`).
- No Java int overflow negative (e.g. `2147483648.0.0`); `_JAVA_INT_MAX` branch (`selection.py:87-96`) is unexercised.
- No empty `goos` or `goarch` negative (`selection.py:111-114`).
- No unreadable/non-directory `patchverdiffs/` (F1), no unsearchable base (F1), no directory-named or broken-link candidate (F11).
- No `patchverdiffs` name with an alternative spelling that the regex must reject (e.g. `go1.21.04.json.diff`).
- Not in the schema: symlink fixtures.

## No-findings (bounded)

- **Positive expected values hand-verified.** I recomputed all 9 positive cases from the source rules (arch order `GoApiSnapshot.java:108-109`, `IS_GOOS_UNIX` `:180-181`, base/diff rules `:122-130`, `:148-166`) and the top-level keys of each fixture's base file. No mismatch. The entry's claim that expectations are hand-authored and independent (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:50`) holds for these 9.
- **Nearest-lower-diff equivalence.** Python candidate set `0 < cand <= patch`, same major.minor (`selection.py:223-237`) matches the Java loop `while (patch > 0 && file == null) patch--` (`GoApiSnapshot.java:153-154`). Patch 0 never selects a diff in either.
- **Base-first short-circuit.** Missing base returns `missing_base` before diff lookup (`selection.py:195-213`), matching `GoApiSnapshot.java:122-126`.
- **Arch order and bucket dedup.** `arch_search_order` (`selection.py:105-121`) matches `:108-109` after the Java empty-string filter at `:230`. Bucket dedup matches the LinkedHashMap build (`:228-237`).
- **Shipped data, bucket level.** Across all 123 diffs in `typeinfo/golang/patchverdiffs/`, the first path element of every `@ [` header (top-level bucket) is present in the corresponding base file `go{M}.{m}.0.json`. Zero diffs add a top-level bucket, so the unpatched-base bucket view is not contradicted at key level. Content-level changes inside buckets were not checked.
- **C2 anchors, static grep only.** `SKILL.md:81` heading matches `controls.py:112` split token; `SKILL.md:450` quote-fidelity row references `.ufo/waves/round-15/boundary-fixtures/expected.json` (exists); `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:76` carries the named correction with the `python3 -I .../round-15/snapshot-inventory.py` argv (script exists at `.ufo/waves/round-15/snapshot-inventory.py`); `SHONEN.md:10` names the historical 2026-10-15 round explicitly. Controls `ROOT = parents[3]` (`controls.py:30`) resolves to the repo root. The SOURCES.md used-by index 11 (`controls.py:45`) matches an 11-column table (separator row).
- **Fixture runner harness.** Temp-root materialization rejects absolute and `..` paths (`selfcheck.py:129-131`). `FORCED` invariants are enforced on every non-error result (`:222-230`).

## Identity and role shape of the wave2 registry (for the record)

- `wave2-registration.json`: schema `ufo-swarm-registry-v1`, wave `kaidoku-r16-w2`, 32 members keyed by name; member fields `kind`, `agentId`, `role`, `item`, `axes` (sampled `FBoundedNumeric`: `item: null`). No per-member `status`, `state`, `model`, `route`, or `lane` field exists. Dead-seat status is therefore not recorded in the registry at all, so no seat is passed on the registry's word.
- Role mix (registration = spec, both 32): executor 8, reviewer 8, scout 6, critic 4, scribe 4, connector 2.
- `wave2-dispatch.json`: `counts` spawn 32, resume 0, total 32; `policy.maxLanes` 32, `hardCeiling` 100.
- Spec items (`wave2-spec.json`, 32): fields `name`, `role`, `prompt`; no per-item axis field (axes are wave-level only).
- Known failure disclosure: no seat-level outcome is audited here. Results from sibling seats are not read by this report.

## Hand-off checks for L1 (not run by me)

1. Run once after integration: `selfcheck.py --fixtures selection-fixtures.json --fixtures negative-fixtures.json` (expect 26 cases; only the F2 exit-code point differs if a schema fault is injected).
2. For F1, a permissions fixture needs a tool outside `files`; treat as a manual test.
3. The `documentation-red.json` after-run should be read with F9 in mind: "producing_command_retained" green is weak evidence.
