# ASourceS106 — S106 source evidence: capture digest, quote locality, census

Seat `L1Kaidoku34-2.ASourceS106`, round 34 run-6 re-dispatch, wave 2, role reviewer.
Assignment: verify the S106 source evidence from the scout capture — locate the binutils `readelf.c`
capture, recompute its sha256, confirm the quoted lines exist at the quoted line numbers, check each
quote is <=25 words and located, report agree/disagree per item, and state whether the row as drafted
would pass the lane's census.

Constants: `CAND` = `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource` (scout capture),
`SCRIBE` = `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeSourcesRow` (draft row and Gate sentence),
`LANE` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`SCR` = `/fast/scratch/hyaku/kaidoku-r34b/w2/ASourceS106` (my scratch).
Work window 2026-10-25T07:28:45Z–07:33:45Z. No lane write, no VCS mutation, no ELF/carrier/reader
execution, no frozen-instrument edit, no score.

## 0. Verdict line

`SOURCE_EVIDENCE_AGREES_WITH_ONE_QUOTE_LOCATION_DEFECT` — capture located and byte-identical to a
live tag fetch, commit fetch and the lane's own tracked copy (sha256 `7e81eedf…`, 689 644 bytes,
25 625 newlines); every anchor line the row cites is present at the cited number; all six quotes are
`<=25` tokens; **the Gate sentence's quote is not contiguous at `readelf.c:14067`** (its `break;` is on
`:14068`), and the drafted row passes `sources-census.sh validate` (exit 0, `ok`, 105→106 rows,
tier.A 99→100) with no E-code of its own.

## 1. Axes

1. **Pin identity** — the cited bytes really are upstream `binutils-2_47`, verified by re-fetch, not by
   trusting the wave-1 receipt.
2. **Locator truth** — every line number and quoted token lands on the byte it names; a quote that needs
   two lines must cite two lines.
3. **Census truth** — the row as drafted satisfies the fleet structural census *and* the census is not
   silently doing less than claimed (existence-only `used-by`).

## 2. Capture location and digest (item: locate, recompute)

Capture is **not** under `LANE/.ufo/waves/round-34/r34b/w1/`; it is in the scout's scratch (allowed by
the assignment) and, byte-identically, in the lane's tracked prep tree.

```
$ date -u +%FT%TZ                                         # 2026-10-25T07:28:45Z
$ sha256sum $CAND/readelf-pinned.c $CAND/readelf-2_47.c $CAND/readelf-by-commit.c \
            $CAND/readelf-2_47-refetch.c $CAND/external-2_47.h $CAND/readelf.c        # exit 0
7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff  .../readelf-pinned.c
7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff  .../readelf-2_47.c
7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff  .../readelf-by-commit.c
7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff  .../readelf-2_47-refetch.c
938745254f7353db20cb9edcee910713ef9b2e8be8b42131d81582b107791d06  .../external-2_47.h
943be51242fb13f627577328a5d8f4105188e39771184eeeea2bd4708310235d  .../readelf.c   (2.45 snapshot, not the pin)
$ wc -l -c $CAND/readelf-pinned.c $CAND/external-2_47.h                              # exit 0
 25625  689644 .../readelf-pinned.c
   326   12359 .../external-2_47.h
```

| item | claim (ScoutReadelfSource §1, ScribeSourcesRow §2) | observed by me | verdict |
|---|---|---|---|
| `readelf.c` sha256 | `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff` | identical, recomputed 07:28:45Z | **agree** |
| bytes | 689 644 | 689 644 | **agree** |
| newlines | 25 625 | 25 625 (`wc -l`); `splitlines()` = 25 628 because of 3 `\f` | **agree**, and the +3 caveat is real |
| `external.h` sha256 | `938745254f…791d06` | identical | **agree** |
| 2.45 snapshot sha256 | `943be512…` | identical | **agree** |
| "capture kept in scratch only, lane registry untouched (S105 highest)" | — | true of **HEAD**: `git show HEAD:corpus/SOURCES.md` sha256 `5abcd365fb70adc8ff1f3afbccf03f5d05c3deee38abec2e4f10b660911bb8e7`, 203 lines, S105 at :111, no S106 | **agree at HEAD**; see §7 for the live working tree |
| lane-side copy exists | not claimed by the row | `LANE/.ufo/waves/round-34/prep/R34ElfReader-files/readelf.c-binutils-2_47` = same sha256, same 25 625/689 644, `git ls-files --error-unmatch` exit 0 (tracked) | **additional evidence in the row's favour**, uncited by the row |

Form-feed evidence for the numbering caveat: three `\f` bytes at char offsets 993, 1948, 13784; for the
line newline-counting calls 13859, `str.splitlines()` reports **13862** (+3). All line numbers in this
report are 1-based **newline** lines, matching `awk`/`grep -n`/`wc -l` and the scout's own probe
(`text = read_text().split("\n"); text[line-1]`).

## 3. Live re-fetch (pin is upstream bytes, not a local fabrication)

```
$ date -u +%FT%TZ                                                                     # 2026-10-25T07:32:27Z
$ curl -sS --max-time 90 -o $SCR/refetch-2_47.c 'https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=binutils-2_47' -w 'http=%{http_code} size=%{size_download}\n'
http=200 size=689644                       # curl_exit=0
$ sha256sum $SCR/refetch-2_47.c            # 7e81eedf…eddeeff
$ cmp -s $SCR/refetch-2_47.c $CAND/readelf-pinned.c ; echo $?   # 0

$ date -u +%FT%TZ                                                                     # 2026-10-25T07:32:40Z
$ curl -sS --max-time 90 -o $SCR/commit-fetch.c '…;f=binutils/readelf.c;hb=6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32' -w 'commit_http=%{http_code} size=%{size_download}\n'
commit_http=200 size=689644                # curl_exit=0
$ sha256sum $SCR/commit-fetch.c            # 7e81eedf…eddeeff ; cmp vs capture exit 0
$ curl -sS --max-time 90 -o $SCR/external-2_47-refetch.h '…;f=include/elf/external.h;hb=binutils-2_47' -w 'ext_http=%{http_code} size=%{size_download}\n'
ext_http=200 size=12359                    # curl_exit=0
$ sha256sum $SCR/external-2_47-refetch.h   # 938745254f…791d06 ; cmp vs capture exit 0
```

So the tag URL and the explicit commit URL serve the same 689 644 bytes as the retained capture: the
tag-tree-equals-commit-tree claim holds **from live bytes**, not only from the wave-1 receipt.
Tag metadata (`tag22.html`: `6ce87bbc…`, `This is the 2.47 release`, `Sun, 26 Jul 2026 07:48:22 +0000`;
`vm-binutils-2_47.m4`: `m4_define([BFD_VERSION], [2.47])`; `news-2_47.txt`: `Changes in 2.47:`; `tags.html`
lists `binutils-2_47`) is verified **from the retained page bytes only** — I did not re-fetch the HTML
pages (§8).

## 4. Quote checks (item: quoted lines exist, `<=25` words, located)

Tokens measured with `printf '%s' '<quote>' | wc -w` (whitespace tokens); the reports' own "N words"
labels use a second convention (code words inside the string), so both are listed.

| # | quote as published | cited location | verbatim at that location | tokens (wc -w ; published) | `<=25` | verdict |
|---|---|---|---|---|---|---|
| Q1 | `if (vstart + sizeof (*entry) > endbuf) break;` (ScribeSourcesRow §8, lesson Gate sentence) | `readelf.c:14067` | **no**: `:14067` is `\t\tif (vstart + sizeof (*entry) > endbuf)`; `\t\t  break;` is `:14068` | 8 ; 8 | yes | **DISAGREE on location** |
| Q2 | `if (vstart + sizeof (*entry) > endbuf)` (Scout §3 site 2, `:14067-14068`) | `readelf.c:14067` | yes (`grep -n` hit at 14067) | 7 ; — | yes | **agree** |
| Q3 | `switch (section->sh_type)` (Scout §2.1) | `readelf.c:13872` | yes (6 occurrences in file; 13872 is one) | 2 ; 3 | yes | **agree** |
| Q4 | `unsigned char vn_version[2];` (Scout §2.3) | `external.h:277` | yes **after whitespace normalisation**; served bytes are `unsigned char\t\tvn_version[2];` | 3 ; 3 | yes | **agree with normalisation caveat** |
| Q5 | `return valid_symbol_name (filedata->dynamic_strings, filedata->dynamic_strings_length, offset);` (Scout §2.4) | `readelf.c:469-470` | yes, contiguous when the two served lines are joined (scout cites both lines) | 5 ; 6 | yes | **agree** |
| Q6 | `warn (_("Missing Version Needs information\n"));` (Scout §3 site 10) | `readelf.c:14149` | yes | 5 ; 4 | yes | **agree** |
| Q7 | `warn (_("Invalid vna_next field of %lx\n"),` (Scout §3 site 5) | `readelf.c:14121` | yes | 6 ; 5 | yes | **agree** |

Q1 evidence, exact bytes (`od -c` of `sed -n '14067,14068p'`):
`\t \t i f   ( v s t a r t   +   s i z e o f   ( * e n t r y )   >   e n d b u f ) \n \t \t     b r e a k ; \n`
and `grep -cF 'if (vstart + sizeof (*entry) > endbuf) break;' readelf-pinned.c` → **0** (exit 1), while
joining the two lines (`sed -n '14067,14068p' | tr -s ' \t\n' ' ' | grep -cF …`) → **1**.
The scout's own probe asserts only the 7-token prefix at 14067
(`("readelf", 14067, ["if (vstart + sizeof (*entry) > endbuf)"])`) and a separate `("readelf", 14068, ["break;"])`
entry — i.e. the instrument that produced the "69/0" receipt does **not** support the Gate sentence's
one-line citation. Q1 is a drafting compression, not a fabricated fact, but as written it fails the
contract's "a quote names its location" rule (`SOURCES-CONTRACT-v1.md` Rules 1). Repair in the lesson
Gate: cite `readelf.c:14067-14068`, or quote only the 7-token prefix.

## 5. Anchor-line checks for the drafted row (cell by cell)

Draft row read from `$SCRIBE/s106-row.draft.md` (1 432 bytes, one physical line, sha256
`753dd6a6623f747662e8a084c50904375d682f0e6634944d5f79b6cfaae81598`; identical to
`$SCRIBE/row-from-report.md`). `cell_count = 13` when split on `|` → 11 columns, no escaped or literal
pipe anywhere (`grep -c '\\|'` → 0, exit 1). Cell lengths: source 197, scope 215, anchor 536, teaches
339, used-by 68.

| anchor element | cited | observed | verdict |
|---|---|---|---|
| `process_version_sections` | `:13859-14419` | `:13859` `process_version_sections (Filedata * filedata)`; `:14419` `}` | **agree** |
| verneed case | `:14020-14149` | `:14020` `case SHT_GNU_verneed:`; last warn `:14149`; the case block itself runs to `:14153` (`break;`) / `:14155` (next case) | **agree as a decode+refusal range**; label "case" is 4 lines short (finding F3) |
| "refusal sites" range | `:14056-14149` | `:14056` is `endbuf = (char *) eneed + section->sh_size;` (a bound, not a refusal); first refusal is `:14054-14055` | **agree on the end bound**, start is off-label (F3) |
| field order | `:14072-14076` | all five `BYTE_GET` lines, `vn_version…vn_next` in order | **agree** |
| field order (aux) | `:14102-14106` | all five `vna_hash…vna_next` | **agree** |
| warnings | `:14134,14139,14149` | those three exist; **four** `warn (` sites exist in 14020-14154 — `:14121` is missing from the list | **partial** (F2) |
| `include/elf/external.h` | `:276-292` | Verneed 276-282, Vernaux 286-292 exactly as cited | **agree** |
| names route | `:463`, `:14080-14113` | `:463` `return strtab != NULL && offset < strtab_size;`; `:14080` and `:14108` `valid_dynamic_name` calls (fallbacks `:14084`, `:14112`) | **agree** |
| `.dynstr` fill | `:8854-8869` | `case SHT_STRTAB: if (streq (name, ".dynstr")) … filedata->dynamic_strtab_section = section;` | **agree** |
| `DT_STRTAB` fill | `:13170-13211` | block reads `DT_STRTAB`/`DT_STRSZ`, sets `dynamic_strings_length = str_tab_len` at `:13208` | **agree** |
| sha256 cells | `7e81eedf…`, `938745254f…` | recomputed, live-refetched | **agree** |

Scout §3 refusal table re-verified line by line: `:14050-14055` (get_data + `if (!eneed)`/`break;`),
`:14067-14068`, `:14089-14090`, `:14098-14099`, `:14118-14125` (warn + `j = ent.vn_cnt` + `break;`),
`:14127-14128`, `:14133-14134`, `:14136-14142` (warn + `cnt = section->sh_info` + `break;`),
`:14143-14144`, `:14148-14149` — all present exactly as tabulated. Block counts:
`sed -n '14020,14154p' readelf-pinned.c | grep -c 'break;'` → **9**; `… | grep -c 'warn ('` → **4**. The
scout's 9/4 probe counts are correct; only the row's three-warning enumeration is incomplete.

Walker anchors also check out: `:14286`/`:14317-14320` (`ivna.vna_name >= string_sec->sh_size` → `name = invalid;`)
and `:14842`/`:14888-14889` (`strtab_size` → `_("<corrupt>")`), `:7825`/`:7831`/`:7847-7848`
(`offset_from_vma`, "without program headers", "not located in any PT_LOAD segment"). `:13863`
`bool found = false;`, `:14027` `found = true;`, `:14409` `if (! found)`, `:14415` the
`No version information found in this file.` printf, `:14418` `return true;` — all at the cited numbers.

Independent verification of the probe's inventory: `probe_s106.py` `CLAIMS` has **69** entries
(counted by AST, not executed), so the "69 line-claims" receipt number matches the instrument's actual
claim list. I did **not** run it (containment choice, §8); the subsets the row and the Gate depend on
were re-verified by my own `sed`/`grep -n`/`cmp` reads above.

## 6. Census (item: would the row pass?)

Structural law: `scripts/sources-census.sh` (fleet, read-only) enforces E01–E12/W01–W04 over the
11-column table; it does **not** read quotes, so "quote `<=25` words and located" is the corpus
contract's Rule 1 for the round lesson, not a census check.

Fixture built from the **committed** registry so the result is not a race with the live landing:
`git show HEAD:corpus/SOURCES.md` (203 lines, sha256 `5abcd365…`) + the draft row after `:111` (S105),
inside a scratch dir whose top-level and `corpus/` children are symlinks to the lane
(`$SCR/census/lane/`), which makes `used-by` resolution behave exactly as at the lane root.

```
$ date -u +%FT%TZ                                     # 2026-10-25T07:32:10Z
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --file $SCR/census/lane/corpus/SOURCES.md --today 2026-10-25
exit 0
file	W04	S033 … (nine pre-existing W04 lines, carried by the registry, not S106)
file	ok	$SCR/census/lane/corpus/SOURCES.md
E-findings: 0
$ bash …/sources-census.sh census --file $SCR/census/lane/corpus/SOURCES.md --today 2026-10-25   # exit 0
file rows 106 / tier.A 100      (HEAD baseline: rows 105 / tier.A 99  -> exactly +1 A row)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' …
0                                      # contract census: malformed rows 0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' …     # 106
```

Per-code result for the S106 row: E01 pass (NF=13), E02 pass (`S106`), E03 pass (next unused id at
HEAD), E04 pass (no duplicate URL+scope), E05 pass (`code`), E06 pass (`A`; tier A = "source code,
primary for scope" per the contract, and the bytes are the upstream release file), E07 pass (`mined`),
E08 pass (`opened 2026-10-25`, not future), E09 pass (`on-release` symbolic), E10 n/a (not `community`),
E11 **conditional on the used-by file existing**, E12 pass (row sits inside `## Registry`), W01 n/a,
W02 n/a, W03 pass (used-by not `—`), W04 pass (first `sourceware.org` URL in the registry).

**Answer: yes, the row as drafted passes the lane's census, provided its `used-by` target exists.**
That proviso is not decorative: at 07:28:45Z
`test -e LANE/corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` returned **1** (absent),
and a `--file` run against a root lacking that path emits `E11 S106 missing used-by
corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md` → exit 1. At 07:32:16Z the file
exists but is **0 bytes** (mtime 04:32 local), and the census passes — because `usedby_findings()` only
does `[ ! -e "$dir/$path" ]`. So the census certifies a path, never content (F6).

## 7. Observed live divergence (not my deliverable, recorded because it contradicts both drafts)

Between my first and second read the lane registry changed under me: at 07:29Z `corpus/SOURCES.md` ended
at S105 + `## Paths`; at 07:32Z it was 207 lines with an **uncommitted** `| S106 |` at `:111`
(`git status --porcelain` → ` M corpus/SOURCES.md`, plus untracked knowledge files). The live row differs
from the draft: commit-pinned URL (`hb=6ce87bbc…`), no `external.h` clause, 203-char anchor with
`14058, 14067-14068, 14072-14076, 14102-14106, 14149`, and `used-by
corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` (7 522 bytes, untracked, exists).
Every line number in that landed anchor is true on the capture (verified in §5). I did not run the census
against the live file because it is being written concurrently; the fixture result in §6 is the honest
receipt. Notably the landed anchor cites `14067-14068`, i.e. it **avoids** F1 — the defect is confined
to the drafted Gate sentence.

## 8. Findings by severity

**F1 — medium, locator defect (repairable before landing).** The lesson Gate sentence quotes
`if (vstart + sizeof (*entry) > endbuf) break;` at `readelf.c:14067`, but `break;` is `:14068`;
`grep -cF` on the full quote against the capture is 0. Cite `:14067-14068` (as the scaffold's own §3
and the landed row do) or shorten the quote to the 7-token prefix. `<=25` is satisfied either way.

**F2 — low, anchor undercount.** The drafted anchor's warning list `:14134,14139,14149` omits `:14121`
(`warn (_("Invalid vna_next field of %lx\n"),`) — the block has four `warn (` sites (grep count 4). The
range `:14056-14149` still contains it, so nothing false is asserted; the enumeration is incomplete.

**F3 — low, range labelling.** "verneed case `:14020-14149`" stops at the last warn; the case runs to
`:14153`. "refusal sites `:14056-14149`" starts at the `endbuf` byte bound (`:14056`); the first actual
refusal is `:14054-14055`. Both are walk ranges with an off-by-a-few label, not wrong line contents.

**F4 — low, inconsistent word labels.** Measured `wc -w`: 8/7/2/3/5/5/6 for Q1/Q2/Q3/Q4/Q5/Q6/Q7, where
the reports publish 8/—/3/3/6/4/5. All quotes are far below 25; the "N words" annotations do not share
one counting convention and should not be read as a measured quantity.

**F5 — low, whitespace normalisation.** `external.h:277` is printed as
`unsigned char vn_version[2];` (single space) while the served bytes hold two tabs. A normalised search
matches, a byte-exact search does not. Prior rounds accepted normalised matching; say so explicitly if
the verifier is strict.

**F6 — medium, census limit worth recording next to the pass.** `E11` is existence-only: a 0-byte
`used-by` target passes (`[ ! -e "$dir/$path" ]` in `usedby_findings()`). The S106 pass in §6 therefore
certifies that the registry row is well-formed and its citation path exists, nothing about the cited
entry's content. The row also has no census-enforced `anchor`/quote check at all, so the structural pass
must not be quoted as evidence that the Gate quote is located.

**F7 — info, uncited retained copy.** The pin's only named locator is the URL + sha256; the identical
bytes are already tracked at `LANE/.ufo/waves/round-34/prep/R34ElfReader-files/readelf.c-binutils-2_47`
(sha256 match, `git ls-files` hit). Adding that path to the anchor would make the digest re-checkable
after `/fast` scratch is cleaned, without widening scope. `external.h` has no such tracked copy.

## 9. Residual risk and verification gaps

- **Unrun:** `$CAND/probe_s106.py` (their 69-claim receipt) was not executed — I verified the claims the
  row and Gate depend on with my own `sed -n`/`grep -n`/`cmp` reads, and confirmed the 69-entry claim
  inventory statically. Treat their "69/69, exit 0" as their receipt, not mine.
- **Unrun:** live re-fetch of the tag/commit **HTML** pages; the `2026-07-26` date and tag→commit mapping
  rest on the retained `tag22.html`/`tags.html` bytes, while the tag and commit *source* URLs were
  re-fetched live and are byte-identical (§3).
- **Not checked:** whether the Arch `binutils 2.47-4` package patches these lines (no source package
  fetched). The row claims upstream tag bytes only, which is the correct scope.
- **Time-boxed:** the registry changed during verification (§7). Numbers here are tied to
  `HEAD = 5abcd365…` plus my recorded per-run UTC stamps, not to the moving working tree.
- **Scope:** nothing here reopens R34-C2, repairs a frozen instrument, or awards credit; the C1 reader
  and its twelve carriers were not read for scoring or executed.

## 10. Tooling ledger

Nothing installed or upgraded (no `pacman`, `uv`, `npx`, `cargo`). Used: `curl 8.23.0` (system, three
live fetches), `python3 3.14.8` (`-` stdin scripts only, text), `GNU Awk 5.4.1` (via the census script),
`sha256sum 0.8.0`, `sed`, `grep`, `wc`, `cmp`, `od`, `bash`. Scratch:
`/fast/scratch/hyaku/kaidoku-r34b/w2/ASourceS106/` (`refetch-2_47.c`, `commit-fetch.c`,
`external-2_47-refetch.h`, `census/{lane,head,lane_knowledge,synth,base}/`).

SOURCE_EVIDENCE_AGREES_WITH_ONE_QUOTE_LOCATION_DEFECT — capture sha256 `7e81eedf…` reconfirmed locally
and by two live fetches; 13 cited anchors and 4 refusal sites exact; six quotes `<=25` tokens; Gate quote
Q1 fails single-line locality at `:14067` (spans `:14067-14068`) and must be re-cited; drafted row passes
`sources-census.sh validate` (exit 0, 106 rows, tier.A 100) with E11 satisfied only by a present-but-empty
used-by path.
