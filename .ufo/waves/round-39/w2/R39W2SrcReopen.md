CONFIRMED with minor defects — SOURCES rows S118-S122 re-open live: every URL fetched HTTP 200, every recorded size and sha256 reproduced, every quote located exactly (S118 only after joining wrapped lines); five wording/anchor defects below, none changes a recorded hash or a quote.

# R39W2SrcReopen — re-open of S118..S122

Seat artifacts: `.ufo/waves/round-39/w2/artifacts/R39W2SrcReopen/` (`fetch-sha256.txt`, `cells.txt`, `unblob-tag-ref.json`, `sym.py`, `sym2.py`, `symlink-probe.txt`). Scratch removed at the end.
Tools installed: none. REA not run (not needed).

## 1. Live fetch (access UTC 2026-10-26T17:27:48Z to 17:27:50Z, `curl -sS`, all HTTP 200)

| row | URL fetched | bytes | sha256 | vs row anchor |
|---|---|---|---|---|
| S118 | unblob/26.6.4/python/unblob/extractor.py | 4129 | `1bb49811…cd23a` | equal (4129 B, same sha); equals installed `~/.local/share/uv/tools/unblob/.../unblob/extractor.py` |
| S119 | registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | 5634033 | `531717a0…e699`; sha512 b64 `C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==` | equal; `npm view rea-agents@6.5.0 dist.integrity` returns the same string; the S080 row contains the same integrity; 1574 files under `package/dist`, `diff -rq` against `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` -> no difference |
| S120 | unblob/26.6.4/python/unblob/report.py | 10553 | `2329783f…cc9ee` | equal; 406 lines; equals installed |
| S120 (2nd file) | .../unblob/extractors/command.py | 3958 | `8ae7d2a3…f85af` | equal; equals installed |
| S121 | sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c | 120167 | `ece42b66…8cb40` | equal; 4619 lines |
| S121 (2nd file) | sasquatch/sasquatch-v4.5.1-6/debian/rules | 630 | `b49d25e9…6d885` | not in the row; equals the w1 seat's recorded sha (`w1/R39SrcSasquatch.md:18`) |
| S122 | unblob/26.6.4/python/unblob/file_utils.py | 27989 | `87d4dc9a…20745` | equal (27989 B, same sha); equals installed |

Tags: GitHub API `git/ref/tags/26.6.4` -> commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`; `git/ref/tags/sasquatch-v4.5.1-6` -> commit `15573bf46c671c8ed23e8c0c50e6187e0c8d0b62` (both match rows; type `commit`, HTTP 200). Installed sasquatch `ad02d27a…4754` and sasquatch-v4be `fac88740…14c6` equal the S121 anchor. Full hashes in `fetch-sha256.txt`.

## 2. Quotes (lesson `### Sources opened this round`)

| row | quote | result |
|---|---|---|
| S118 | "either removed it it attempts to traverse outside of the extraction directory or rewritten to be fully portable" (18 words) | present only after whitespace normalisation: it spans three wrapped docstring lines 53-55 (docstring is 51-57); byte-exact substring count 0, normalised count 1. The lesson's "lines 51-56" is loose (docstring closes at 57). The "it it" typo is in the source. |
| S119 | "Extractor executables named by the producer; empty when it named none." (11) | exact, `dist/domain/firmware/firmwareAnalysis.js:100`, count 1 |
| S120 | "Describes an error when failed to run the extraction command" (10) | exact, `report.py:92` (class `ExtractCommandFailedReport` at 91, last field `exit_code` at 98) |
| S121 | "CFLAGS=-DFIX_BE dh_auto_build" (2 tokens) | exact in `debian/rules:17`, count 1; count in the row's own URL `unsquashfs.c` = 0 |
| S122 | "basedir.joinpath(path).resolve().relative_to(basedir.resolve())" | exact, `file_utils.py:36` (function 34-39) |

Line cites I checked and found right: S118 73-77 / 79-87 / 88-91 (`extractor.py` target, safe check+remove+report, relpath rewrite); S119 84-91 six gap kinds, `FirmwarePublication.js:68-75` and `301-308` (non-file -> `unpublished-entry`), `:241` `dependencyChunkKeys` suppression, `FirmwareReports.js:254-255` unknown reports copied to `diagnostics`; S120 `command.py:101-102` `return [self._executable]`, `:59-68` report built only when `returncode != 0`, `:70` `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`; S121 `debian/rules:15-18`; S122 34-39 (False on ValueError).

## 3. Row structure (script over `corpus/SOURCES.md` lines 124-128)

All five: 11 cells (12 raw `|`), no `\|`, no `|` inside a cell; status `mined`; opened `2026-10-26`; recheck `on-release`; ids unique; registry 122 rows; `git diff a2f64e1d HEAD -- corpus/SOURCES.md` = 5 insertions, 0 deletions (appends only). Details per cell in `cells.txt`.

used-by vs `grep -rn 'source: S11[89]\|source: S12[0-2]' corpus/knowledge`:
- S118, S119, S120, S121 -> only `2026-10-26-r39-sqfs-outcome-triage.md` (source lines 4-7): used-by matches exactly.
- S122 -> only `2026-10-26-r39-be-squashfs-v4-core.md` (source line 3): used-by matches exactly.
- Non-source mentions: `2026-10-26-unblob-format-matrix.md:1,10` contain the text "staged as package S122" / "staged S122 -> S116" (a historical staging id, not a citation of the registry S122); no ambiguity because it's prefixed "source: S116". SKILL.md triage rows and README rows 203-204 also name S119/S122 but are not knowledge entries.

## 4. Verdict per row

- S118: CONFIRMED, two defects. (a) Scope "when it reports `MaliciousSymlinkRemoved`" and the anchor name only lines 79-87; `extractor.py:58-65` is a second reporting site (`is_recursive_link` -> report + unlink). Probe with the installed function (`sym.py`, `sym2.py`, Python 3.13): a<->b loop links are kept with no report because `Path.resolve()` no longer raises `RuntimeError` on 3.13, so the branch is dead on this host; the entry's "SR = yes means an escaping link" holds here but not by construction. (b) Teaches "an in-tree or absolute target is kept": probe shows absolute `/sub/f` kept (rewritten to `f`), absolute `/etc/passwd` kept as dangling `../etc/passwd`, but absolute `/../../etc/passwd` removed with a report, so "absolute targets ... kept, not removed" (entry, "Symlinks" paragraph) is true only when no `..` climbs out after the leading `/` is stripped. Empty-target links are removed with no report (lines 68-72); unprobed (symlink('') fails on the OS) — read from source only.
- S119: CONFIRMED, no defect found. Tarball, integrity, 1574-file equality, six kinds, :100 quote, :241, :68-75, :301-308 all reproduced.
- S120: CONFIRMED, no defect found. Both files reproduce; the row's scope also names `ExtractorDependencyNotFoundReport`, raised at `command.py:70`, and the anchor omits that line (anchor cites 91-98 and 101-102 only) — cosmetic.
- S121: CONFIRMED, two defects. (a) The quote and lines 15-18 come from `debian/rules`, which is not the row's URL and whose own URL/sha256 (`b49d25e9…6d885`, 630 B) the row never records; the row's URL (`unsquashfs.c`) contains no `CFLAGS=-DFIX_BE` (count 0). (b) Teaches "without the flag it misreads a standard-BE body" rests on the autodetect block `unsquashfs.c:2252-2283` (`#ifdef FIX_BE` inverts `swap`), which the anchor does not cite; the anchor's 4389-4400 covers `-be` (4389-4394) and `-le` (4395-4400) only. The claim itself holds live: on `H01/carrier.sqsh`, `sasquatch-v4be -no-exit-code -f -d o c.sqsh` -> "SquashFS version [1024.0] / inode count [150994944] suggests a SquashFS image of a different endianess", "read_id_table: failed to read id table block", exit 1, 0 files; with `-be` -> exit 0, 7 files; plain `sasquatch` without a flag -> "Block size too small", 0 files. "build the tree twice ... lines 15-18": the first build is line 14; 15-18 holds install, clean, FIX_BE build, cp.
- S122: CONFIRMED, no defect found. Fetched 2026-10-26T17:27:49Z vs the row's 17:09:05Z: same bytes. `..` not clamped: probe `/../../etc/passwd` -> unsafe -> removed.

## 5. Limits

- Anchors were compared to fresh fetches of the tagged raw files, not to a `git clone` at the tag (the tag->commit mapping came from the API; blob-vs-tag identity for the raw files rests on raw.githubusercontent.com serving the tag, not on a clone).
- `npm view` ran against the live registry; "equal to S080" compared only the integrity string, the tarball sha256 is not in the S080 row.
- Lines cited by the knowledge entry but not by the rows (e.g. `report.py:118-122,133-138`, `command.py:59-77`) were only partly re-read (59-80 and 91-100 of the files).
- The loop-branch observation is for unblob 26.6.4 on Python 3.13.x as installed; other interpreters unprobed. [INFERENCE] the branch can fire where `resolve()` still raises `RuntimeError` (Python < 3.13 semantics).
