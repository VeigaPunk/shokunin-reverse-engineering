# R39SrcUnblobReports — DONE

Verdict: DONE. All cited unblob 26.6.4 files fetched from the tag and byte-identical to the installed copy; report/raise sites, SquashFS chunk-validity path and three behaviours that matter for the triage table were located and observed on development carriers (no K1-K6, no REA run). S112 covers the extractor argv/dependency list only — a **new knowledge file** is needed (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`, the declared used-by) and one new SOURCES row.

Artifacts: `.ufo/waves/round-39/w1/artifacts/R39SrcUnblobReports/` — `src/` (9 fetched files, tag 26.6.4), `evidence/` (sha256.txt, unblob `--report` JSONs, -vvv logs, listings, walk.py).

## 1. Fetch vs installed (all SAME)
Base URL `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/`; installed under `/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`; unblob `--version` = 26.6.4; tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089 (per existing S110/S112 anchor, not re-resolved here).

| file | lines | sha256 (fetched == installed) |
|---|---|---|
| report.py | 406 | 2329783fc645de8aae94b82443277bceb6ceac968549ff65917c7b2d454cc9ee |
| extractor.py | 135 | 1bb498119429ed80ae29caf9772d2b6210c22b6a8a2c8beb6cfea94550bcd23a |
| extractors/command.py | 117 | 8ae7d2a3980b80b25274d2351a724631be40c79bc8a2da3be14dae2bf09f85af |
| handlers/filesystem/squashfs.py | 590 | 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287 (= S112 file) |
| finder.py | 196 | 6329d30d66d05d4f47e2b694c9f24013056a75f25e231ad241426afbca785e82 |
| models.py | 578 | a368b312707d6ea18e3222f442d5bff692b9e146c9fb4fe8f98fed316110d758 |
| file_utils.py | 788 | 87d4dc9a51bc4e92ee410fba77dfcf88fb32266e58e1e6be0ea70bfe44320745 |
| cli.py | 653 | fc775f1ad66f05c0f6ba77fb74c80112ea99b4baf07900d7d701b7932259f86c |
| processing.py | 920 | 599afe91a52fcaa308ad3c36ea58172c1d8de4d9c11cab92ad94130bd7671826 |

## 2. Definitions and raise sites (file:line, quotes <=25 words)
**ExtractCommandFailedReport** — defined `report.py:91-98`: `class ExtractCommandFailedReport(ErrorReport)`, `severity: Severity = Severity.WARNING`, fields `command: str`, `stdout: bytes`, `stderr: bytes`, `exit_code: int`; stdout/stderr serialized base64 (`report.py:101-110`, "Use base64 to encode and decode bytes data"). Raised `extractors/command.py:59-68`: `if res.returncode != 0:` → report → `raise ExtractError(error_report)`. Severity is WARNING (not ERROR) — observed below, process exit 0.

**ExtractorDependencyNotFoundReport** (the missing-dependency report; there is no class named ExtractDependency) — defined `report.py:118-122`: "Describes an error when the dependency of an extractor doesn't exist." `severity = Severity.ERROR`, `dependencies: list[str]`. Raised `extractors/command.py:69-77`: `except FileNotFoundError:` → `dependencies=self.get_dependencies()` (the `Command` instance returns only its own `[self._executable]`, `command.py:101-102`, so the report names ONE binary, e.g. `['sasquatch-v4be']`, not both that `SquashFSExtractor.get_dependencies` lists at `squashfs.py:68-69`). Sibling: `ExtractorTimedOut` `report.py:125-130` (ERROR; `cmd`, `timeout`), raised `command.py:78-84`; `COMMAND_TIMEOUT = 12 * 60 * 60` (`command.py:20`).

**MaliciousSymlinkRemoved** — defined `report.py:133-138`, `severity = Severity.WARNING`, `link: str`, `target: str`. Raised only in `extractor.py:fix_symlink`: loop branch `extractor.py:58-65` ("Symlink loop identified, removing"); path-traversal branch `extractor.py:79-87` ("Path traversal attempt through symlink, removing"). Absolute targets are not reported: `extractor.py:74-75` `target = Path(target.as_posix().lstrip("/"))` then rewritten relative to outdir (`:89-91`); empty target is unlinked with NO report (`:67-71`). Called from `fix_extracted_directory` (`extractor.py:95-113`) after every chunk extraction (`processing.py:678`).

**Report wrapping / exit code** — extraction reports attach to the chunk: `processing.py:666-668` `except ExtractError as e: extraction_reports.extend(e.reports)`; `processing.py:672-673` extraction_successful = no `ErrorReport` (note WARNING-severity reports are ErrorReport subclasses → also count as unsuccessful there); `ExtractError` `models.py:357-362`. Process exit: `cli.py:464-473` `get_exit_code_from_reports`: ERROR → 1, WARNING → 0 (`(Severity.WARNING, 0)`). Base `ErrorReport` `report.py:50-51`; every report carries computed `__typename__` (`report.py:34-41`) — the key REA diagnostics expose.

## 3. SquashFS chunk validity (`handlers/filesystem/squashfs.py`)
There is NO `is_valid` function. Validity = `_SquashFSBase.calculate_chunk` `squashfs.py:77-98` (v4 LE/BE handlers inherit it; v4 BE only swaps `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)` `:527`):
- `:80` `endian = get_endian(file, self.BIG_ENDIAN_MAGIC)`; header parsed with that endian (`:80`; v4 struct `squashfs4_super_block_t` at `:468-491`, `bytes_used` uint64 at `:483`).
- `:82-83` `end_of_data_offset = (start_offset + header.bytes_used) & 0xFF_FF_FF_FF` then `file.seek(end_of_data_offset)`.
- `:84-94` reads padding to a 4096 multiple (`PAD_SIZES = [4_096, 1_024]`, `:21`); if the pad is all zero → chunk ends at the rounded size; else `:96-98` `ValidChunk(start_offset=..., end_offset=start_offset + header.bytes_used)`.
- **bytes_used beyond the file:** `File` is an mmap subclass; `File.seek` `file_utils.py:74-79` wraps `ValueError` as `SeekError`; `finder.py:51-57` catches `SeekError` — "Seek outside file during chunk calculation" at debug level `_verbosity=2` — and returns None (no chunk). So a truncated image or an over-large `bytes_used` yields NO chunk, NO report, NO extraction (observed §4). The second guard `finder.py:106-108` `if chunk.end_offset > context.file_size:` "Chunk overflows file" (debug, `Scan.Continue`) can only fire when the zero-pad rounding path overshoots; with a short read the pad test fails first [INFERENCE, not exercised]. `InvalidInputFormat` is also swallowed silently (`finder.py:37-43`; `ValidChunk` rejects start>=end `models.py:142-146`). Only non-expected exceptions produce `CalculateChunkExceptionReport` (`finder.py:58-67`, `report.py:75-80`).
- Bytes after `bytes_used` that are non-zero become a separate `padding`/unknown chunk (observed §4, `trail`).
- Extraction argv (S112, `squashfs.py:36-66`): BE v4 → `sasquatch-v4be` with `-be` unless `bytes_used == mkfs_time` (AVM, `:48-50`); always `-no-exit-code -f -d {outdir} {inpath}`.

## 4. Observed on development carriers (unblob 26.6.4, run directly from scratch cwd; K1-K6 and REA untouched)
Dev carrier: `python3 tools/round-37/gen-squashfs.py tree be.sqsh --endian be --comp gzip` on a fresh tree (/etc/a.txt, /bin/b, symlinks `good->a.txt`, `abs_ok->/etc/passwd`, `evil_rel->../../../../etc/passwd`, `loop1<->loop2`), 608 bytes, sha256 be2e2247…ea159 (`evidence/dev-carriers.sha256`, `dev-tree-listing.txt`). Variants cut from it: trunc (first 500 B), trail (+100×0xAA), big (bytes_used := 10^6 at offset 40 BE), corrupt (bytes 100-199 XOR 0xFF). Command: `cd run_dir && unblob -e out --report rep.json X.sqsh` (python 3.13 venv of the unblob tool).

| variant | exit | unblob outcome |
|---|---|---|
| be | 0 | 1 chunk `squashfs_v4_be` 0-608, extraction ok; `MaliciousSymlinkRemoved` WARNING link=`.../etc/evil_rel` target=`<run_dir>/etc/passwd`; `evil_rel` gone from output; `abs_ok -> passwd` (absolute rewritten, NO report); `good -> a.txt` kept (`evidence/be-rep.json`, `be-extract-listing.txt`) |
| trunc (bytes_used 608 > file 500) | 0 | no chunk, no `out` content, report holds only Stat/FileMagic; -vvv: "Seek outside file during chunk calculation handler=squashfs_v4_be" (`trunc-vvv-log.txt`) |
| big (bytes_used 1000000 > file 608) | 0 | same: no chunk, no output, same SeekError debug line (`big-vvv-log.txt`) |
| trail (+100 junk) | 0 | squashfs chunk 0-608 extracted into `0-608.squashfs_v4_be_extract/` + `608-708.padding` chunk; MaliciousSymlinkRemoved present |
| corrupt (data blocks flipped) | 0 | chunk found; `ExtractCommandFailedReport` severity WARNING, exit_code 1, command `sasquatch-v4be -be -no-exit-code -f -d <out> <in>`, stderr (base64 decoded) "get_metadata: failed to read block / FATAL ERROR: read_inode: failed to read inode 106:304" (`corrupt-rep.json`); `-no-exit-code` does not mask this — sasquatch still exited 1 |
| be with PATH=/usr/bin:/bin (unblob by absolute path) | **1** | chunk found, `ExtractorDependencyNotFoundReport` severity ERROR dependencies `['sasquatch-v4be']`; unblob printed "Encountered errors … Severity.ERROR ExtractorDependencyNotFoundReport" (`nodep-rep.json`) |

Surprise worth the table: on this install (Python 3.13.16 in the unblob venv) `Path.resolve()` of a mutual symlink loop returns a path without raising `RuntimeError` (checked directly with the venv python), so `is_recursive_link` (`extractor.py:42-47`) is False and the "Symlink loop identified" branch / MaliciousSymlinkRemoved-for-loop does NOT fire: extracted `loop1 -> loop1`, `loop2 -> loop1` (rewritten, kept, no report) vs source `loop1 -> loop2`. Only traversal produces MaliciousSymlinkRemoved. Triage consequence: MaliciousSymlinkRemoved = a link was removed (tree has fewer entries than the oracle), WARNING, exit 0; do not read absence of the report as "all in-tree links survived" for loops or absolute targets.

## 5. Draft SOURCES row (11 columns; id placeholder — L1 renumbers; last id in file at read time S122)
| S123 | unblob 26.6.4 report types and chunk-validity path — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py | code | A | unblob 26.6.4 only: where ExtractCommandFailedReport, ExtractorDependencyNotFoundReport and MaliciousSymlinkRemoved are defined/raised and how a SquashFS chunk is accepted or silently dropped; not REA's wrapping of them, not other versions, not sasquatch behaviour | tag 26.6.4 (commit 1fcc7a0a584a70a96c31f5a276c20944d199a089); fetched==installed sha256 for report.py `2329783f…c9ee`, extractors/command.py `8ae7d2a3…85af`, extractor.py `1bb49811…d23a`, finder.py `6329d30d…5e82`, squashfs.py `2d7b901b…9287`; `report.py:91-98` "Describes an error when failed to run the extraction command" fields command/stdout/stderr/exit_code, WARNING; `report.py:118-122` dependencies list, ERROR; `report.py:133-138` MaliciousSymlinkRemoved link/target, WARNING; `extractor.py:79-87` "Path traversal attempt through symlink, removing"; `finder.py:51-57` SeekError → no chunk, debug only | Triage by report: a sasquatch non-zero exit is a WARNING ExtractCommandFailedReport (stderr base64, exit 0), a missing binary is an ERROR ExtractorDependencyNotFoundReport naming one executable (exit 1), a removed traversal link is a WARNING MaliciousSymlinkRemoved, and bytes_used beyond the file yields no chunk and no report at all | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |

## 6. S112 coverage / new file needed
S112 (`squashfs.py` lines 24-70) already covers: the extractor, `sasquatch`/`sasquatch-v4be` dependencies, `-be` vs AVM argv. It does NOT cover report classes, `Command.extract` raise sites, symlink fixing, finder drop-out of invalid chunks, or exit-code mapping — those live in report.py / command.py / extractor.py / finder.py / cli.py. The new row above (anchored on report.py, with sha256s of the other four chain files in the anchor) is the new file needed; `squashfs.py:77-98` calculate_chunk could also be quoted via S112's file (same sha256 2d7b901b…) — new quotes only, no new row needed for it. If L1 prefers one-file-per-row, split into S123 report.py, S124 command.py, S125 extractor.py, S126 finder.py with the same used-by.

## 7. Limits
- No REA envelope was exercised; how REA surfaces these `__typename__` values (diagnostics paths) is outside this item (see round-38 AVM probe). Triage rows keyed on unblob type names need a REA-side observation before being scored.
- Tag-to-commit mapping reused from S110/S112, not re-resolved. `--show-external-dependencies` was run but gave no sasquatch line on stdout; not relied on.
- `Chunk overflows file` reachability for SquashFS is [INFERENCE].
- Tools installed: none. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39SrcUnblobReports` removed at end.
