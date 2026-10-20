# FNoHarmCraft — wave 2 source-read attack on round-16 artifacts

Seat: KaidokuR16.FNoHarmCraft (leaf, read-only). Scope: produced round-16 selection.py, selfcheck.py, controls.py, fixtures, and the craft section of SKILL.md (17/17 range-only metric). No tests, builds, linters, formatters, or smoke runs were executed. No implementation or corpus file was edited.

## Reviewed revisions (hashes at final read)

| File | sha256 (prefix) | Note |
|---|---|---|
| `.ufo/waves/round-16/selection.py` | `29cfc854…` (315 lines) | Changed three times during review by sibling edits; this is the final read |
| `.ufo/waves/round-16/selfcheck.py` | `f5c20c57…` | Changed twice during review; final read is coherent |
| `.ufo/waves/round-16/controls.py` | `5f9fe949…` | Unchanged across the review |
| `.ufo/waves/round-16/selection-fixtures.json` | `ff2483d8…` | Unchanged since 05:15:50 |
| `.ufo/waves/round-16/negative-fixtures.json` | `a92b3abb…` | Unchanged since 05:20:22 |

Source anchors: `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` and `.../golang/GoVer.java`, read via the zip. Data: `Ghidra/Features/Base/data/typeinfo/golang/`.

## Findings (by severity)

### F1 — MEDIUM — negative fixture pins a source-divergent outcome as expected
- `negative-fixtures.json`, case `unsupported-shape-bucket-nonobject-preview`: `go1.21.0.json` has `"all": ["not","an","object"]`, and the expectation is `status: base_only`, `base_matching_buckets: ["all"]`.
- Source: `GoApiSnapshot.java:222` deserializes every retained bucket with `gson.fromJson(reader, GoArch.class)`. An array value cannot be read as a `GoArch`, so `read()` (205–240) and `get()` (102–116) do not yield a `base_only` result. The Java path errors out. The exception type is [INFERENCE] from standard Gson reflective-object behaviour; the source does not catch it.
- The fixture's own note says "Do not expect UnreadableError here". That is the problem: the case locks a known divergence into the source-law set as the expected output. A correct fix (validating bucket shape) would fail selfcheck, and the harness currently counts the divergence as a pass.
- Recommendation for L1: move this case to a separately labelled preview-divergence set, or express it as `expect_error` once the preview validates bucket shape. Do not keep it in the source-law pass count.

### F2 — LOW (installed corpus) / MEDIUM (claim fidelity) — bucket membership ignores value shape
- `selection.py:147-167` (`_top_level_keys`) and `selection.py:250-256` (`keys = set(...)`, bucket loop) count a bucket by key presence only. Values are never checked.
- Source divergence: `GoApiSnapshot.java:222-223` stores each retained bucket in `arches`, and `:233-236` keeps only `arch != null`. A `null` bucket value is therefore dropped by Java but counted by the preview. A non-object bucket value fails at `:222` (F1), but the preview still counts it.
- The docstring at `selection.py:149-152` says the bucket preview "never claims membership for a document the Java reader could not open". That is not true for these shapes.
- Impact on installed data: none found. `go1.21.0.json` and `go1.25.0.json` contain zero `: null` tokens, and their top-level buckets are objects. This was a token-level check, not full bucket-shape validation.
- No fixture covers a null-valued bucket. Recommendation: either check that bucket values are objects and treat `null` as absent, or narrow the docstring claim.

### F3 — LOW — selfcheck does not exercise the CLI exit contract
- `selfcheck.py` calls only `select_snapshot` (run_case, 297–348). `selection.py:286-311` (`main`) is not exercised. The exit-2 JSON emission for `invalid_request` and `unreadable_input` is untested.
- `selection.py:191-192` (root is not a directory) has no fixture. The negative-fixture note for `missing-base-empty-root` says a nonexistent root "is NOT expressible via fixtures". The runner could express it with a missing-root flag, but does not.
- `selection.py:228-232` (`OSError` on listing `patchverdiffs/`) has no fixture. The missing-directory branch is covered indirectly by `no_diff`.
- The spec's exit-0/exit-2 contract is therefore only partly checked. The harness proves `select_snapshot` behaviour, not the CLI.

### F4 — LOW — craft 17/17 metric is narrower than the SKILL prose
- The counts are reproducible by reading: 17 rule blocks (`SKILL.md` craft section 81–318, `^- \*\*` count = 17), 67 unique `corpus/knowledge/...md:N[-M]` citations, every block has at least one knowledge citation, and `controls.py:42-44,110-128` parses only the `corpus/knowledge/` form. `controls.py:103-133` is a statement-for-statement mirror of SCORECARD.md:101-117 (recipe A).
- Not parsed by the metric: 11 non-knowledge `file:line` references inside craft rules, and 4 bare references (below). Examples:
  - `SKILL.md:205` `PROVINCE.md:18`, `SCORECARD.md:59`
  - `SKILL.md:210` `SCORECARD.md:544-545`, `LOG.md:856-858`
  - `SKILL.md:253-254` `LOG.md:1411-1412`
  - `SKILL.md:246` `.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89` (and four other `.ufo/waves/…` refs)
  - `SKILL.md:278` `corpus/QUALITY.md:21`
- Hand check of the non-knowledge refs that were read: `SCORECARD.md:544-545` and `LOG.md:856-858` support the "Config custody" rule text; `PROVINCE.md:18` supports its pointer content. All cited files exist. No content defect was found.
- The `controls.py` docstring (lines 6-11, 103-108) honestly labels the metric as existence plus in-range only. The SKILL prose at `SKILL.md:84` ("each bullet is bounded by the lines it cites") overstates it for the non-knowledge refs. Recommendation: relabel the SKILL line, or extend the metric's scope in its own docstring. This is a calibration fix, not a correctness defect.

### F5 — LOW — bare line references have no resolvable target
- `SKILL.md:174` "run log :311": resolves to the adjacent cited file, `corpus/knowledge/2026-10-14-r11-01-queue-ops.md:311`, which is the row "decoder caught lane-side encoding bug #2 … tool accepted the semantic variant". Supports the claim.
- `SKILL.md:176-177` "row 7 / table line 171": in the adjacent cited `2026-10-13-r8-01-queue-a-ops.md:171` is a `trace-javascript-semantics` verify command, not a census table row. The referent is undefined in the rule.
- `SKILL.md:178` "lines 181–183 and 187": in `2026-10-14-r10-02-queue-ops-2.md:181-187` the text contains "line 185" as a census-row label, not a file line.
- `SKILL.md:179` "L195": in `2026-10-14-r12-02-queue-b-ledger.md:195` the line is text about the L199 jadx family. "L195" is a row label, not a file line.
- The metric ignores these forms, so they are not part of 17/17. A reader cannot verify them from the rule text alone.

### F6 — LOW — controls.py exit-2 contract leaks on non-UTF-8 input
- `controls.py:51,71` decode `git` output as UTF-8 with `text=True, encoding="utf-8"`, and `:110,125,137` call `.decode("utf-8")` outside any try. Only `CalledProcessError`/`OSError` are caught (`:63, :72, :98`).
- A non-UTF-8 blob or path raises `UnicodeDecodeError`, which exits 1. The docstring (`controls.py:16-17`) says exit 2 means usage error, unresolvable revision, or missing anchor. Minor contract gap.

### F7 — LOW — used-by delta is not append-checked
- `controls.py:231-232` records any change to column 11 (`used-by`) as "allowed", with no append-only check. Removal of a used-by entry is reported as an allowed delta. The before/after values are shown, so the change is visible, but the `immutable_cells_unchanged` boolean does not gate it.

### F8 — LOW (cosmetic / provenance)
- `selfcheck.py:4` still says "Round-16 wave w1 deliverable". Stale label.
- `PROVINCE.md:18` itself carries a bare config line number (`~/.kimi-code/config.toml:4126`). The craft rule at `SKILL.md:196-206` allows line numbers only inside append-only records, and it cites PROVINCE.md as an exemplar. Calibration note only.

## No-finding (bounded)

- Arch order: `selection.py:105-121` matches `GoApiSnapshot.java:108-109`; the `""` slot is dropped as in `:230-232`. `IS_GOOS_UNIX` (`selection.py:42-45`) matches `:180-181`.
- Base missing: `selection.py:191-213` returns `missing_base` before any diff consideration, matching `GoApiSnapshot.java:115` (null base → EMPTY).
- Patch 0: `selection.py:224` skips the listing, matching the `while patchVer.getPatch() > 0` guard. Same-minor only: `GoVer.java:134-136` (`prevPatch`) decrements patch only.
- Diff name shape: `selection.py:55-56` matches `GoVer.toString()` (`GoVer.java:155-158`, no leading zeros).
- Bucket order and dedupe (`selection.py:250-256`) match the `LinkedHashMap` build (`GoApiSnapshot.java:228-237`).
- Request validation: the length check precedes `int()` in the current revision (`selection.py:83-91`), so the earlier int-before-length defect is gone. Not reported as a current finding.
- Fixtures: all 11 positive and 17 negative expected values were spot-checked against the arch-order, minor-isolation, and patch-selection rules. No mismatch found. No sha256 or size expectations appear anywhere in the fixtures, so no invented hashes.
- selfcheck (current revision): `FORCED` invariants (`selfcheck.py:233-241`) and boolean-identity comparison are correct. No structural defect in the final read.
- Craft: all 17 rule blocks have a knowledge citation. None of the 67 cited ranges exceeds the cited file's length (line-count bound read; no CR/FF/VT/NEL/LS/PS in the cited files). This is a bounds check, not a semantic check.
- Sources registry: 23 S-rows, no duplicate IDs; `USED_BY_COLUMN = 11` matches the header (`| id | source | … | used-by |`).

## Verification limits

- No test, build, lint, format, or smoke run was executed. All checks were `read`, `grep`, `wc -l`, `unzip -p`, `sha256sum`, `stat`, `ls`. Scratch files in `/tmp` were removed.
- Java behaviour for Gson null/non-object values is [INFERENCE] from standard Gson semantics, not from the Gson source (not in `Base-src.zip`).
- Semantic correctness of the 67 cited ranges was not assessed. The 17/17 number is an existence-and-bounds figure only.
- Shipped-data check was token-level (`: null`) plus visible top-level shapes. Full bucket validation was not done.
- Because `selection.py` and `selfcheck.py` changed during review, L1 should recompute hashes before integration and re-read if they moved again.

## Tooling

No installs, updates, or pacman transactions. None were needed; all checks used tools already present.

## Suggested L1 actions (not executed by this seat)

1. Decide on F1: relabel or move `unsupported-shape-bucket-nonobject-preview` out of the source-law pass set.
2. Decide on F2: either validate bucket values in `selection.py` or narrow the docstring at `selection.py:149-152`.
3. Optional: add a CLI exit-code fixture or a missing-root runner flag for F3.
4. Relabel `SKILL.md:84` to match the knowledge-only scope of the 17/17 metric (F4), and fix the stale `selfcheck.py:4` label.
