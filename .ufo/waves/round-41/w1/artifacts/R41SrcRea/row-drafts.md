# R41SrcRea — SOURCES row drafts (lane schema, 11 columns, no literal pipe inside a cell)

Base `49096c7e6f226af0c750c4b003be58883cb6049f`. Highest row at base is **S126**; S127 and S128 are
taken by `R41SrcAvm`. New rows start at **S129**. Nothing here was written to `corpus/SOURCES.md` — the
L1 integrates.

---

## A. NEW row S129 (required: no existing row covers `python/unblob/processing.py`)

`git show 49096c7e:corpus/SOURCES.md | grep -c processing.py` → 0. Insert after S128.

```
| S129 | unblob task-depth gate and partial-output retention at tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/processing.py | code | A | unblob 26.6.4's `_process_task` depth gate, its per-chunk `ExtractError` collection, the post-extraction `fix_extracted_directory` then `delete_empty_extract_dir` order, and the depth + 1 subtask it adds when an extract dir survives; not sasquatch's exit codes, not REA's gap vocabulary, not other versions | tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089; HTTP 200, 32013 B, sha256 599afe91a52fcaa308ad3c36ea58172c1d8de4d9c11cab92ad94130bd7671826, equal to the installed copy; line 55 `DEFAULT_DEPTH = 10`; lines 274-279 return after the `StatReport` at the ceiling; lines 666-670 collect `e.reports`; line 677 "we want to get consistent partial output even in case of unforeseen problems"; lines 681-688 add the surviving extract dir as a subtask at depth + 1; lines 746-748 remove only an empty extract dir; line 447 applies the same sanitiser to multi-file output | A failed or depth-ceilinged extraction keeps the files it already wrote and only an empty extract dir is removed, so partial output and a failure report describe the same region | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md |
```

## B. OPTIONAL row S130 (only if the L1 keeps one fact set per row; sasquatch's document is already S121)

```
| S130 | sasquatch extraction writer and exit-status control at tag sasquatch-v4.5.1-6 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c | code | A | the same file as S121, scoped to what the writer does after the swap decision: `symlink(2)` for a stored link, `set_exit_code` suppression under `-no-exit-code`, and which failures still set exit_code 2; not the `-be` swap (S121), not unblob's argv, not any carrier | tag sasquatch-v4.5.1-6 = commit 15573bf46c671c8ed23e8c0c50e6187e0c8d0b62; sha256 ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40 (120167 B) re-fetched 2026-10-26, equal to S121's pin; lines 1199-1205 `res = symlink(i->symlink, pathname);` with `EXIT_UNSQUASH_STRICT` on failure; lines 4019-4021 and 4147-4149 `-no-exit-code` sets `set_exit_code = FALSE`; lines 4575, 4595 and 4601 set `exit_code = 2` only when `set_exit_code`; line 4618 `return exit_code;` | A non-fatal unsquashfs problem exits 0 under `-no-exit-code` although files were skipped, and a link is created with `symlink(2)`, so an empty target cannot materialise | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md |
```

---

## C. Anchor text to append to existing rows (append only; no status or `used-by` change needed)

**S118** (`unblob symlink sanitiser`, anchor currently cites lines 73-77, 79-87, 88-91). Append:

```
; lines 58-65 and 81-87 remove a looping or escaping link with `MaliciousSymlinkRemoved`; lines 67-71 remove a link whose `os.readlink` target is empty with `logger.error("Symlink with empty target, removing.")` and no report; lines 95-113 `fix_extracted_directory` dispatches every symlink to `fix_symlink`
```

Scope addendum (recommended, so the silent branch is inside the row's scope):
`… and when it reports `MaliciousSymlinkRemoved`` → `… and when it reports `MaliciousSymlinkRemoved` versus the empty-target removal it performs without a report`

**S119** (`rea-agents 6.5.0 … gap schema`, anchor currently cites `firmwareAnalysis.js:84-91,100` and `FirmwarePublication.js:68-75,301-308`). Append:

```
; depth rows: `dist/firmware/FirmwareReports.js:155,229-230,384` (task depth at or past `maxDepth` pushes the logical path) into `dist/firmware/FirmwarePublication.js:294-299` over `emptyGap` (:39-46), ceiling `MAX_EXTRACTION_DEPTH = 10` (:23) and its re-root index (:245-272); dependency rows: `dist/firmware/FirmwarePublication.js:152-207,239-241,288-293` with names from `dist/firmware/FirmwareReports.js:171-188,210-223,320-335`; failure rows: `dist/firmware/FirmwarePublication.js:225-238,275-285` while `dist/firmware/FirmwareFiles.js:121-188` inventories the whole staging tree and `dist/firmware/FirmwareReports.js:419-423` decides `coverage`
```

`teaches` addendum (replace the single sentence with these two):
`Read gap kind, dependency name and diagnostics together; a dependency row suppresses the failure row for the same chunk` → `Read gap kind, dependency name and diagnostics together; a dependency row suppresses the failure row for the same chunk. A depth-limited row names a task at the ceiling with every identity field null, and no gap row ever names a published file`

**S120** (`unblob report classes`, anchor cites `report.py:91-98`, `command.py:101-102`). Append:

```
; `extractors/command.py:59-68` raises `ExtractCommandFailedReport` only when `res.returncode != 0`, `:69-77` raises `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` on `FileNotFoundError`; `report.py:94` fixes severity `WARNING` for the command report and `:118-119` names the dependency class
```

**S121** (`sasquatch source at tag sasquatch-v4.5.1-6`, anchor cites `unsquashfs.c:4389-4400` plus `debian/rules`). Append:

```
; `unsquashfs.c:1199-1205` creates each stored link with `symlink(i->symlink, pathname)` and `EXIT_UNSQUASH_STRICT` on failure; `:4019-4021` and `:4147-4149` make `-no-exit-code` set `set_exit_code = FALSE`; `:4575`,`:4595`,`:4601` set `exit_code = 2` only when `set_exit_code`; `:4618` returns it; file re-fetched 2026-10-26 at 120167 B with the same sha256 as this cell
```

Scope addendum: `… at one tag;` → `… at one tag, including the writer's `symlink(2)` call and its `-no-exit-code` exit suppression;`

**S123** (`operation surface`, anchor cites service/provider/release/evidence/cli names). Append:

```
; `dist/cli-runtime/cutterToolContracts-TZH9EHr5.js:1757-1764` `extract_firmware` input cell `max_depth: z.number().int().min(1).max(10).default(3)` described "Extraction depth; reaching it yields partial analysis"; `dist/cli-runtime/cli.js:15282,15293` map the `--max-depth` flag to it
```

Scope addendum: `… the operation catalog and CLI command map,` → `… the operation catalog, the `extract_firmware` input cell and CLI command map,`

---

## D. Schema check

11 columns in every draft (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`,
`opened`, `recheck`, `used-by`). `kind` = `code`, `tier` = `A` for both new rows (published source read
live this round, byte-identical to the installed copy). `recheck` = `180d` for S129 (the processing.py
file is stable across a release cycle but is not pinned to a release-tagged blog page), `on-release` for
S130 (it follows S121's recheck cell). `used-by` = the planned v3 knowledge note named in
`plans/round-41-claims.md:69`. No cell contains a literal pipe character.
