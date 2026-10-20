# FProducerBytes — attack on `controls.py` byte-prefix vs blob equality and revision binding

Scope: source read of `.ufo/waves/round-16/controls.py` (302 lines, sha-tag `9C9A`), cross-checked against `SCORECARD.md:92-124` (command A recipe), `corpus/SOURCES.md:5-29` (header and rows), `.git/config`, and the `.git` ref listing. Nothing executed, no git subcommands run, no fixtures authored, no tools installed. L1 owns the single post-integration run (`python3 -I .ufo/waves/round-16/controls.py 6235498b HEAD` per `w1/NoHarmProducer.md:88-90`).

Ranking is by how far a report field can say "unchanged" or "preserved" while the repo changed.

## Findings

### F1 (medium) Frozen and old-prefix checks enumerate only BEFORE paths; additions pass silently
- `controls.py:182-186` (`dir_prefix_report`) and `:198-202` (`frozen_report`) build the path set from `before.blobs` only.
- `frozen_report` (`:204-213`) returns `checked` and `unchanged` over that BEFORE-only set. A file added under `.ufo/waves/round-15/` or `.ufo/waves/round-14/` or `evidence/round-1-2026-10-15/` at AFTER never appears in any field.
- The output key is `frozen_baselines`, and the docstring frames these as frozen. A reader will take `unchanged == checked` to mean the directory is intact. It means only that pre-existing files kept their blob SHA.
- Attack: add `.ufo/waves/round-15/boundary-fixtures/new.json` in AFTER. Output: `checked` unchanged, `unchanged` equal to `checked`, `quote_script_unchanged: true`, no mention of the new file.
- Fix direction: compute `after` paths under each frozen prefix minus `before`, report them as `added_under_frozen`, and keep them out of `unchanged`.
- Limit: `NoHarmProducer.md:95-98` discloses that the frozen set is enumerated at BEFORE. It does not disclose that additions are invisible. The shipped docstring (`:2-21`) does not disclose it either.

### F2 (low-medium) Mode is discarded; "unchanged" ignores `100644 -> 100755`
- `Rev.__init__` (`controls.py:79-82`) keeps `parts[2]` (the SHA) and drops `parts[0]` (the mode).
- `.git/config:3` has `filemode = true`, so modes are tracked.
- Attack: `chmod +x .ufo/waves/round-14/tools/quote-fidelity.py` (or any frozen or verifier file) and commit. `unchanged`, `byte_identical`, and `quote_script_unchanged` all report `true`.
- The docstring's "full blob-SHA equality" (`:9-10`) is accurate for what it does, but the report labels the result `unchanged`, which overclaims for an executable script.
- Fix direction: store `(mode, sha)` and compare both, or add a `mode_before`/`mode_after` pair to each row.

### F3 (medium-low) `used-by` change is accepted without any monotonicity check
- `sources_registry` (`controls.py:231-232`) records any difference in column 11 as `allowed_used_by_deltas`, including removal of existing references.
- The lesson wording the producer cites (`corpus/lessons/round-15.md:39`, "Only permitted `used-by` changes on existing rows") implies additive changes. The code does not test additivity, and a deletion is reported in the same bucket as an addition.
- Attack: remove `corpus/lessons/round-14.md` from S001's used-by in AFTER. `immutable_cells_unchanged` stays `true`, and the deletion appears only as an "allowed" delta.
- Column index 11 is correct: `SOURCES.md:5` header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` splits to index 11 for `used-by`, matching `USED_BY_COLUMN` (`:45`).
- Fix direction: parse both cells into reference sets and report `used_by_removed` separately, or fail when `before - after` is nonempty.

### F4 (medium-low) Duplicate source IDs silently shadow rows
- `source_rows` (`controls.py:143-150`) is a dict comprehension keyed by `row[1]`. For a repeated ID the last row wins and earlier rows are dropped before comparison.
- Attack (conditional on a duplicate existing): BEFORE has two `S0xx` rows; AFTER changes the first row's `teaches` cell. Only the last row is compared, so `immutable_cells_unchanged` stays `true`. `rows_before` counts unique IDs, so the count also hides the duplicate.
- The same happens in the other direction: AFTER can introduce a duplicate that shadows the original. `added_rows` (`:241`) uses set difference and so reports nothing.
- I did not exhaustively check current `SOURCES.md` for duplicates (no bulk query was run). The defect is in the code path regardless of the present data.
- Fix direction: key by `(id, occurrence)`, or fail with exit 2 on any duplicate ID at either revision.

### F5 (low) Byte-prefix is not line-boundary aware; a final-line amendment counts as "append-only"
- `prefix_report` (`controls.py:163`) is `new.startswith(old)`. If BEFORE ends without a newline, AFTER can extend that final line in place and `prefix_preserved` stays `true`.
- `NoHarmProducer.md:93-94` discloses that byte-prefix "cannot distinguish append from rewrite that happens to share a prefix". The shipped docstring (`controls.py:8-9`) says "reports only byte-prefix retention (append-only)" without that caveat.
- Fix direction: require `old == b""` or `old.endswith(b"\n")` for an append-only claim, or report a separate `last_line_extended` boolean.

### F6 (low) Error contract: undocumented exit 1 paths
- Docstring (`controls.py:16-17`) says exit 2 covers usage, unresolvable revision, or missing anchor. Other failures escape as tracebacks (exit 1).
- `git()` (`:51`) decodes with strict `encoding="utf-8"`. `Rev.__init__` (`:72`) and `Rev.get` (`:98`) catch only `CalledProcessError`/`OSError`. A `UnicodeDecodeError` from `ls-tree` (non-UTF-8 path) or from `.decode("utf-8")` on `SKILL.md` (`:110`), knowledge files (`:125`), or `SOURCES.md` (`:137`) is uncaught.
- Relevant only under unusual tree contents. The producer's own limit says all repo paths are ASCII (`NoHarmProducer.md:108-109`), which holds today but is not enforced.

### F7 (low) Missing-at-BEFORE shape and `appended_bytes` inconsistencies
- `prefix_report` (`:154`) calls `before.get(path)` before checking existence. A missing `LOG.md` at BEFORE therefore exits 2 with "cannot read LOG.md at <rev>" (`:98-99`), not the `absent_at_before` row that `unchanged_report` emits (`:173`).
- The `missing_at_after` branch (`:156-160`) omits `appended_bytes`, and `appended_bytes` is computed as `max(len(new)-len(old),0)` (`:164`) even when `prefix_preserved` is false, so the number is meaningless in that case.
- `dir_prefix_report` (`:185`) filters `p.endswith(".md")`. A non-markdown file under `corpus/lessons` or `corpus/knowledge` is not checked at all.

### F8 (info, bounded) Repo-local replace refs bypass the immutability claim
- `git()` (`:48-52`) inherits the environment and does not pass `--no-replace-objects`. The docstring (`:18-20`) limits the caveat to `GIT_*` variables only.
- If `refs/replace/*` existed, `ls-tree` and `git show` would read replacement objects and the "immutable Git objects" framing (`:2`) would not hold.
- Bounded observation: the loose ref listing shows only `refs/heads/main` and `refs/remotes/origin/main`; `refs/replace`, `packed-refs`, `info/grafts`, and `shallow` returned no files on glob. I did not inspect `packed-refs` contents or the global git config. `.git/config` (`:1-14`) has no replace or textconv setting. No `.gitattributes` exists at repo root.
- Fix direction (cheap): add `--no-replace-objects` to the `git()` argv, or set `GIT_NO_REPLACE_OBJECTS=1` in the child env.

## Checked, no finding

- **Craft replication vs command A.** `controls.py:110-128` matches `SCORECARD.md:103-117` in split marker (`## Queue-drain craft `, then `\n## `), rule split (`(?m)^- \*\*`), regex (`RULE_REF` identical to the recipe pattern), `valid` logic, and `splitlines()` line count. The only difference is decoding: recipe A uses default-locale text mode, the script uses UTF-8. Identical for ASCII knowledge files. Missing-file handling is equivalent (`rev.exists` before `get` vs `CalledProcessError`).
- **Revision binding.** `resolve()` (`:60-64`) pins each name to a commit SHA with `rev-parse --verify <name>^{commit}`. All subsequent reads (`ls-tree`, `git show`) use the SHA, not the name. No TOCTOU within one run because objects are immutable (modulo F8). The report records resolved SHAs (`:255-260`).
- **Blob-SHA vs byte read paths.** `byte_identical` comes from `ls-tree` SHAs and `prefix_preserved` from `git show` bytes. Both read the same object store and no textconv or smudge filter is configured in the repo, so they agree. Global gitattributes were not inspected.
- **Sources column index.** Verified against the header (see F3). Correct.

## Limits
- Source read only. No run, no git subcommands, no fixture authored, so no expected hash or pass value is asserted.
- F4's shadowing needs a duplicate ID to exist; I did not enumerate `SOURCES.md` for duplicates.
- F5 depends on whether `LOG.md` currently ends with a newline; not checked.
- Global git config, `GIT_*` environment, and `packed-refs` contents were not inspected.

## Tools
Installed or upgraded: none.
