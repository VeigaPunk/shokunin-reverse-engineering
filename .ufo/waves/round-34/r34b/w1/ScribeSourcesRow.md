# ScribeSourcesRow — S106 registry row and lesson `## Gate` sentence

Seat `L1Kaidoku34-2.ScribeSourcesRow`, wave 1, round 34 run-6 re-dispatch, attempt 1. Leaf member: no subagent
dispatch, no network, no carrier/fixture/reader execution, no lane-VCS command. Read-only work window
2026-10-25, receipted 07:19:26Z–07:25:53Z; every path below is absolute and every digest here was recomputed
from the bytes on disk.

Assignment: draft the 11-column `SOURCES.md` row for S106 and the lesson `## Gate` block sentence from the
`ScoutReadelfSource` capture, or report the capture missing and draft nothing. The capture exists
(`readelf-pinned.c`, sha256 `7e81eedf…`), so both drafts are produced below.

## 1. Axes

1. **Depth** — the row must carry the reader's actual rules (both bounds, the name-table route, the
   no-fail return), not a summary of `readelf -V`.
2. **Evidence fidelity** — every cell anchored to a recomputed digest or a located line; nothing upgraded
   from the sibling seat's receipt into my own observation.
3. **Containment** — draft only; `corpus/SOURCES.md` and `corpus/lessons/round-34.md` stay untouched.

## 2. Inputs read (evidence pointers)

| input | pointer | digest / note |
|---|---|---|
| pinned capture | `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/readelf-pinned.c` | sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`, 689,644 bytes, 25,625 newlines |
| same file before the copy | `…/ScoutReadelfSource/readelf-2_47.c` | identical sha256 — the copy is byte-identical |
| superseded snapshot (2.45 tree) | `…/ScoutReadelfSource/readelf.c` | sha256 `943be51242fb13f627577328a5d8f4105188e39771184eeeea2bd4708310235d`, 24,330 newlines; used only for the cross-version check |
| external struct layout | `…/ScoutReadelfSource/external-2_47.h` | sha256 `938745254f7353db20cb9edcee910713ef9b2e8be8b42131d81582b107791d06`, 12,359 bytes |
| tag metadata | `…/ScoutReadelfSource/tag22.html`, `tags.html`, `vm-binutils-2_47.m4`, `news-2_47.txt` | tag `binutils-2_47` → commit `6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32`, subject `This is the 2.47 release`, `Sun, 26 Jul 2026 07:48:22 +0000`; `bfd/version.m4` = 2.47; NEWS heading `Changes in 2.47:` |
| sibling capture report | `.ufo/waves/round-34/r34b/w1/ScoutReadelfSource.md` (written 04:23Z local) | source of the fetch commands/HTTP codes below; I recomputed every digest I cite |
| registry to join | `corpus/SOURCES.md` | highest row S105 at line 111; `grep -n '^| S10[0-9]' corpus/SOURCES.md` shows S106 absent, so the row appends after line 111, before `## Paths` |

Fetch provenance (sibling seat, reported not re-run — network is theirs, not mine):
`curl -sS --max-time 120 -o readelf-2_47.c 'https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=binutils-2_47'`
→ HTTP 200, 689,644 bytes, mtime 2026-10-25T07:18:43Z; a tag re-fetch at 07:22:50Z and an explicit
`hb=6ce87bbc…` fetch at 07:23:06Z both returned the same 689,644 bytes with `cmp` exit 0. Tag tree equals
commit tree. `raw.githubusercontent.com` answered 404 for every binutils-gdb path including `master`, so the
re-fetch route for the `on-release` cadence must stay `sourceware.org` `blob_plain`.

## 3. Commands run here (command, exit code, UTC)

```
# cwd /fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource, 2026-10-25T07:19Z-07:23Z
sha256sum readelf-pinned.c readelf-2_47.c readelf.c external-2_47.h tags.html tag22.html news-2_47.txt   # exit 0
wc -l readelf-pinned.c readelf.c                                                                          # exit 0 -> 25625 / 24330
awk 'NR>=14020 && NR<=14155' readelf-pinned.c > verneed-247.txt          # case block, 2.47
awk 'NR>=13343 && NR<=13478' readelf.c        > verneed-master245.txt    # same block, 2.45 snapshot
diff -q verneed-247.txt verneed-master245.txt                             # exit 0, no output (identical)
sha256sum verneed-247.txt verneed-master245.txt                           # exit 0, both 125b8127e5a1eab1bcd3a84d92dc6eca12de7ca3c1a5935c1317195f392851a6
grep -n 'sh_link' verneed-247.txt                                         # exit 0, two hits (slice lines 28-29 = file :14047-14048)
sed -n '13859,14418p' readelf-pinned.c | grep -c 'return false'           # exit 1 (no match), count 0
sed -n '14020,14155p' readelf-pinned.c | grep -c 'warn ('                 # exit 0, count 4
# cwd /fast/scratch/hyaku/kaidoku-r34b/w1/ScribeSourcesRow, 2026-10-25T07:25:53Z
python3 -I -B validate_row.py s106-row.draft.md                           # exit 0 -> cells=11 escaped_pipes=0 fixed_cells_ok=1 used_by_single=1 ROW_OK
```

`grep -c` exit 1 above is the expected "zero matches" status, not a failure. An earlier one-liner validator
crashed with `TypeError: list indices must be integers` (I indexed a cell list with strings); it was rewritten
as `validate_row.py` and the final run is the one receipted above.

## 4. Behaviour extracted from the pinned capture (my own reads)

All line numbers are 1-based newline lines of `readelf-pinned.c`; the file holds three form feeds, so a
reader that splits on `\f` reports +3 after each one — `wc -l` counts newlines (25,625) and every number
below came from `awk`/`grep -n`, which do not split on form feed.

1. **Two gates before any decode.** `if (! do_version) return true;` at `:13865-13866`; then the walk is
   driven by the **section header table** — `:13868-13872` iterates `filedata->section_headers` for
   `i < e_shnum` and switches on `section->sh_type`, reaching `case SHT_GNU_verneed:` at `:14020`.
   `found` is set inside the case (`:14027`); `:14409-14415` prints
   `No version information found in this file.` when nothing matched.
2. **Two independent bounds.** The count comes from `sh_info` (`:14058` `for (idx = cnt = 0; cnt < section->sh_info; ++cnt)`)
   and the byte end from `sh_size` (`:14056` `endbuf = (char *) eneed + section->sh_size;`). Neither is
   derived from the other.
3. **Field order.** Verneed decoded in `:14072-14076` (`vn_version, vn_cnt, vn_file, vn_aux, vn_next`),
   Vernaux in `:14102-14106` (`vna_hash, vna_flags, vna_other, vna_name, vna_next`), matching
   `external-2_47.h:276-282` and `:286-292` — 16 + 16 bytes, `vn_aux` relative to the record start
   (`:14091`), `vna_next` relative to the aux start (`:14129-14130`).
4. **Name resolution is the dynamic string table, not `sh_link`.** `:14080-14084` and `:14108-14113` test
   `valid_dynamic_name` (defined `:467-471`, membership `:461-464` `return strtab != NULL && offset < strtab_size;`)
   and fall back to printing `File: %lx` / `Name index: %lx`. The table is filled either from a `.dynstr`
   section (`:8854-8869`, duplicate rejected) or from `DT_STRTAB`/`DT_STRSZ` via `offset_from_vma`
   (`:13170-13211`). `sh_link` occurs exactly twice in the case block, both in the `Link: %u (%s)` printout
   (`:14047-14048`); the verneed branch never validates `sh_link < e_shnum`, unlike the versym branch
   (`:14168`, `:14174`).
5. **Refusal is in-band, never a failure status.** `get_data` bounds the read and returns NULL after an
   `error` (`:502-541`); the case then leaves with a bare `break` (`:14054-14055`). Truncated records stop the
   walk at `:14067-14068`, an overrunning `vn_aux` at `:14089-14090`, a short Vernaux at `:14098-14099`, a
   non-advancing `vna_next` at `:14118-14125` (warn then abandon), an overrunning aux chain at `:14127-14128`,
   and record-chain end at `:14136-14144`; shortfalls are reported by `:14133-14134` and `:14148-14149`.
   `process_version_sections` contains **zero** `return false` (grep count 0) and ends `return true;` at
   `:14418`, so the caller `:25115` never flips `res` on a truncated listing.
6. **Cross-version identity.** The whole `SHT_GNU_verneed` case block is byte-identical between the 2.45-tree
   snapshot (`readelf.c`) and the 2.47 release capture (`verneed-247.txt` = `verneed-master245.txt`,
   `diff -q` exit 0). The pinned 2.47 reading is therefore not a release-fragile claim, but the row still pins
   2.47 only.

## 5. Gates (what this report asserts and what it refuses)

- **Pin gate — passed:** release tag object → release commit, and three independent HTTP-200 fetches are
  digest-equal, so the capture is a release tag, not a moving branch. The tag commit page and the commit-hash
  fetch agree.
- **Format gate — passed:** 11 cells, zero literal or escaped `|`, no empty cell, fixed enums
  (`code` / `A` / `mined` / `on-release`), `recheck` is a cadence not prose, `used-by` names exactly one entry.
- **Scope gate — applied:** the row admits the 2.47 section-header decode and its refusals only. It refuses
  any loader/`ld.so` claim, any claim about other releases, and any implication about this lane's gate
  verdicts or carriers.
- **C1 isolation gate — held:** the inherited R34-C1 stays stopped. Nothing here re-opens, re-scores or
  relabels it; the divergence in §6.3 is a source-reading note for the L1, not a C1 judgement, and I did not
  run, score or read the C1 production reader or its twelve carriers.
- **No-execution gate — held:** no ELF carrier, fixture or reader was executed; only `sha256sum`, `awk`,
  `grep`, `wc`, `diff` and `python3 -I -B` on text files.

## 6. Findings

1. **The legitimate-reader ground is stronger than a field list.** Truncation in readelf is answered by
   stopping a chain and warning, never by emitting a plausible record — the exact inverse of the
   structure-blind shortcut readers the C2 gate scores. That is the sentence S106 is quoted for.
2. **`found` is set before the section is read** (`:14027` precedes `get_data` at `:14050`), so an unreadable
   verneed section still suppresses the `No version information found` line; the only trace is `get_data`'s
   own `error`. A consumer cannot separate "absent" from "unreadable" without stderr text.
3. **Reader divergence worth the L1's attention (not a C1 re-score).** S103's authority text and the frozen
   C1 entry read `SHT_GNU_verneed.sh_link` as the string-table selector; binutils 2.47 resolves both
   `vn_file` and `vna_name` through the **dynamic** string table and prints `sh_link` only as a label. The
   two routes coincide only when the linked table is `.dynstr`. A reader built strictly on `sh_link` and a
   reader built like readelf would print different names for a file where they differ; neither is refused by
   the other. I flag it and stop there — deciding whether that touches C1 is the L1's call, and C1 stays
   unopened here.
4. **Three walkers, three disciplines** (sibling §2.5, spot-checked at `:14828-14895` for the symbol path):
   the section printer bounds names by `DT_STRSZ`, the versym path by the linked section size, the symbol
   path by its own `strtab_size`. A replay that imitates one walk can still miss the other two.
5. **Host tool is adjacent, not identical:** the sibling's query `pacman -Q binutils` → `binutils 2.47-4`
   matches the tag's major.minor, but no Arch source package was fetched, so downstream patches to these
   lines are unproven. The row claims upstream tag bytes only.

## 7. Draft — SOURCES row S106 (verbatim; single physical line, do not reflow)

| S106 | binutils-gdb `readelf.c` at tag `binutils-2_47` — https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=binutils-2_47 (with `include/elf/external.h` at the same tag) | code | A | The release readelf's `SHT_GNU_verneed` decode only: record order, `sh_info` count and `sh_size` byte bounds, dynamic-string name resolution, malformed-record refusals; not the loader, later releases, this lane's carriers or gate | Tag `binutils-2_47` = commit `6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32` (2026-07-26); `readelf.c` sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`; `process_version_sections:13859-14419`, verneed case `:14020-14149`, field order `:14072-14076` and `:14102-14106`, refusal sites `:14056-14149` (warnings `:14134,14139,14149`); names `:463,14080-14113` via `.dynstr:8854-8869` or `DT_STRTAB:13170-13211`; `include/elf/external.h:276-292` sha256 `938745254f7353db20cb9edcee910713ef9b2e8be8b42131d81582b107791d06` | Decode Verneed and Vernaux in fixed order inside both a declared count and a byte end, resolve names only as validated indices inside the dynamic string table with a raw-index fallback, and stop a chain at the first short or overrunning record while still returning success; truncation shows up only as missing rows plus stderr warnings. | mined | 2026-10-25 | on-release | corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md |

Cell notes for the L1:
- `used-by` names one entry by precedent, not by omission: S103/S104 list only their knowledge entry although
  `corpus/lessons/round-34.md` also cites them. If the lesson Gate bullet below also names S106, the registry
  cell still holds a single entry under that precedent; say so if you prefer two.
- The anchor cell is 534 characters, longer than anything currently in the table (max 279 across S001–S105)
  because it pins two files. Trim the `external.h` clause if a uniform width matters; keep both sha256 values,
  they are the only proof the two files came from the same tag.
- Insert after line 111 (S105), before the blank line and `## Paths`.

## 8. Draft — lesson `corpus/lessons/round-34.md` `## Gate` block sentence

- **S106 admitted, scoped to the release reader:** binutils-gdb `readelf.c` at tag `binutils-2_47` (commit `6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32`, 2026-07-26), opened 2026-10-25 UTC (capture 07:18:43Z; re-fetches 07:22:50Z and 07:23:06Z digest-equal), sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`. Located quote at the retained capture `readelf.c:14067` — “if (vstart + sizeof (*entry) > endbuf) break;” (8 tokens) — a record that does not fit ends the walk instead of being emitted. The row teaches the 2.47 section-header printer, its refusal branches and its dynamic name index; it says nothing about the loader, later releases, or this lane's gate verdicts.

Optional second bullet, only if you want the divergence on the record in the lesson itself:

- **Source-scope note, not a C1 re-score:** readelf 2.47 resolves `vn_file` and `vna_name` through the dynamic string table (`:14080-14084`, `:14108-14113`, `.dynstr:8854-8869`, `DT_STRTAB:13170-13211`) and prints section `sh_link` only as a label (`:14047-14048`); S103's `sh_link` reading and this route coincide only when the linked table is the dynamic one.

Optional Paths bullet and search-log line (registry housekeeping, clearly yours to accept or drop):

- Paths: `- GNU ELF version-needs, pin and reader — S103 → S104 → S106: field meanings and GNU constants, then the release reader that consumes them; S106 grounds the reader's bounds and refusals, not this lane's carriers or gate.`
- Search log: `- 2026-10-25 round 34 — Question: which pinned reader defines the legitimate version-needs decode the C2 gate compares against. Where: sourceware binutils-gdb tag binutils-2_47 (blob_plain readelf.c, include/elf/external.h) after api.github.com returned HTTP 403 and raw.githubusercontent.com 404 for every binutils-gdb path. Identified 1 family, screened 2 files, included 1 row (S106), excluded 0. Stop: the decode order, both bounds, the name-table route and the refusal branches are located at line level; carrier behaviour remains outside this source.`

## 9. Out of scope / not done

- No write to `corpus/SOURCES.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, `corpus/**` or any
  sibling lane; this report and `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeSourcesRow/` are the only writes.
- No network: the fetch, HTTP codes and re-fetch receipts belong to `L1Kaidoku34-2.ScoutReadelfSource`; I
  report them as theirs and recomputed only digests over the bytes on disk.
- No execution of readelf, any carrier, fixture or reader; no `-V` output was produced or compared.
- R34-C1 left stopped: its production reader and twelve carriers were not run, read for scoring, or relabelled.
- Tooling ledger: **nothing installed or upgraded** (no `pacman`, no `uv`, no `npx`); system `python3`,
  `sha256sum`, `awk`, `grep`, `wc`, `diff` only.

## 10. Artifacts

- Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/w1/ScribeSourcesRow.md`
- Draft row: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeSourcesRow/s106-row.draft.md` (1,429 bytes, one line)
- Validator: `…/ScribeSourcesRow/validate_row.py`; digests and exit codes: `…/ScribeSourcesRow/receipts.txt`
- Verneed case slices: `…/ScribeSourcesRow/verneed-247.txt`, `verneed-master245.txt`, `slices.sha256`
- Capture (sibling-owned, read-only here): `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/`

ROW_DRAFTED — S106 row 11/11 cells, no pipe characters, pin = tag `binutils-2_47` commit `6ce87bbc…`
(sha256 `7e81eedf…`, three fetches digest-equal), Gate sentence carries a located 8-token quote at
`readelf.c:14067`; nothing landed in `corpus/`, C1 untouched.
