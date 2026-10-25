# ScoutReadelfSource — pinned binutils readelf.c, version-needs decode order and refusals

Seat: `L1Kaidoku34-2.ScoutReadelfSource`, wave 1, round 34 run-6 re-dispatch.
Assignment: pin the binutils `readelf.c` that justifies the gate's legitimate-reader ground, capture it,
hash it, and extract (a) the version-needs record walk and (b) its truncated/malformed-record refusals.
Proposed as **SOURCES row S106** (draft only; `corpus/SOURCES.md` untouched — its highest row is S105).

Access date for every fetch below: **2026-10-25 UTC**. No installs, no upgrades, no writes outside my
own absolute report path and `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/`.

## 0. Verdict line

`SOURCE_PINNED` — binutils-gdb tag `binutils-2_47` (`readelf.c` sha256 `7e81eedf…`), 69 line-anchored
quote assertions verified against the capture (`probe_s106.py`, exit 0), version-needs walk and four
malformed-record refusal sites located; three independent in-file verneed walkers found.

## 1. Capture and provenance (commands, HTTP, exit codes, UTC)

Host tool state (read-only): `pacman -Q binutils` → `binutils 2.47-4`, exit 0 (07:22:09Z). The pinned
tag therefore matches the host's major.minor exactly.

Hosts probed for the source, in this order:

| command (abridged) | result |
|---|---|
| `curl -sS 'https://api.github.com/repos/bminor/binutils-gdb/tags?per_page=100'` | HTTP **403**, 280-byte refusal body (rate-limited; tags not listed) |
| `curl -o readelf-$t.c …/raw.githubusercontent.com/bminor/binutils-gdb/$t/binutils/readelf.c` for `binutils-2_44`, `2_45`, `2_46` | HTTP **404**, 14 bytes each |
| `curl …raw.githubusercontent.com/bminor/binutils-gdb/master/binutils/readelf.c` | HTTP **404**, 14 bytes — so this is an egress/path block, not a tag miss |
| `curl -o t2 'https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=binutils-2_45'` | HTTP **200**, 656703 bytes (superseded) |
| `curl -o readelf-2_47.c …;a=blob_plain;f=binutils/readelf.c;hb=binutils-2_47` | HTTP **200**, 689644 bytes, 25625 lines, file mtime **2026-10-25T07:18:43Z** |
| `curl …;f=bfd/version.m4;hb=binutils-2_47` | HTTP **200**, `m4_define([BFD_VERSION], [2.47])` |
| `curl …;f=binutils/NEWS;hb=binutils-2_47` | HTTP **200**, first heading `Changes in 2.47:` |
| `curl -o tags.html …;a=tags` | HTTP **200**, plain release tags run … `binutils-2_46_1`, `binutils-2_47` (newest) |
| `curl …;f=include/elf/external.h;hb=binutils-2_47` | HTTP **200**, 12359 bytes, mtime 07:19:11Z |

Newest *verifiable* release tag = `binutils-2_47`; chosen over the prompt's `binutils-2_44` example.

**Tag → commit → date, established.** The retained tag page (`tag22.html`, 14640 bytes, fetched 07:18:51Z)
shows `binutils-2_47` → commit `6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32`, subject `This is the 2.47 release`,
commit date `Sun, 26 Jul 2026 07:48:22 +0000`.

**Digest stability, re-run rather than assumed** (2026-10-25T07:22:50Z and 07:23:06Z):

| command | HTTP | sha256 | cmp vs `readelf-pinned.c` |
|---|---|---|---|
| same tag URL re-fetch → `readelf-2_47-refetch.c` | 200, 689644 B | `7e81eedf…` | exit **0** |
| `hb=6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32` → `readelf-by-commit.c` | 200, 689644 B | `7e81eedf…` | exit **0** |

Three independent fetches (initial at the tag, tag re-fetch, explicit commit) are byte-identical, and the
tag tree equals the commit tree, so the capture is pinned to the `2.47` release commit and not to a moving
branch.

Captures kept in `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/`:

| file | sha256 | bytes |
|---|---|---|
| `readelf-pinned.c` (= `readelf-2_47.c`) | `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff` | 689644 |
| `external-2_47.h` | `938745254f7353db20cb9edcee910713ef9b2e8be8b42131d81582b107791d06` | 12359 |
| `probe_s106.py` (verifier) | — | — |

Note for the lane: `foreign_fetch_note` — `raw.githubusercontent.com` returned 404 for every binutils-gdb
path including `master`, so **a future re-fetch must use `sourceware.org` `blob_plain`** or the pin will
look like a nonexistent tag. All line numbers below are 1-based on `readelf-pinned.c`; the file contains
3 form-feed bytes, so tools that split on form feeds report +3 line numbers after them (`wc -l` = 25625).

## 2. (a) The version-needs record walk

### 2.1 Section-type gate (and the option gate above it)

- `readelf.c:13859` `process_version_sections (Filedata * filedata)`; `:13865` `if (! do_version)` → `:13866`
  `return true;` (no version output at all unless `-V`/`--version-info`, `do_version` set at `:7151`/`:6863`/`:7054`).
- The gate is the **section header table**, not `PT_DYNAMIC`: `:13868-13870` iterate
  `filedata->section_headers` for `i < filedata->file_header.e_shnum`, and `:13872` `switch (section->sh_type)`
  dispatches `case SHT_GNU_verneed:` at `:14020`. `found` (`:13863`) is only set inside a matching case.
- **Refusal of absence**: `:14409` `if (! found)` → `:14415` `printf (_("\nNo version information found in this file.\n"));`.
- Consequence: the `DT_VERNEED`/`DT_VERNEEDNUM` tags are captured into `version_info[]` at `:13784`
  (index macro `:458` `DT_VERSIONTAGIDX(tag) (DT_VERNEEDNUM - (tag))  /* Reverse order! */`) and are used
  **only** by the symbol/versym paths, never by this section printer. **`[INFERENCE]`** From `:13868` +
  `:14409`: a carrier with `e_shnum == 0` prints "No version information found in this file." even when
  `DT_VERNEED` is present and resolvable. I did not execute readelf to confirm (carrier execution is barred
  in this wave); the claim rests on the two cited lines only.

Quote (`readelf.c:13872`, 3 words): **`switch (section->sh_type)`**

### 2.2 Record count is the section header's `sh_info`

`:14058` — `for (idx = cnt = 0; cnt < section->sh_info; ++cnt)`. The number of version-need entries is
**taken from `sh_info`, never derived from `sh_size`**; the walk is additionally clamped by
`endbuf = (char *) eneed + section->sh_size;` at `:14056`. Two independent bounds: a declared count and a
byte end pointer.

### 2.3 Field order — Verneed, then Vernaux, little-endian via `BYTE_GET`

Decode order at `readelf.c:14072-14076`, in this exact sequence:

```
14072: ent.vn_version = BYTE_GET (entry->vn_version);
14073: ent.vn_cnt     = BYTE_GET (entry->vn_cnt);
14074: ent.vn_file    = BYTE_GET (entry->vn_file);
14075: ent.vn_aux     = BYTE_GET (entry->vn_aux);
14076: ent.vn_next    = BYTE_GET (entry->vn_next);
```

The external layout that order decodes, `include/elf/external.h:276-282`:

```
276: typedef struct {
277:   unsigned char		vn_version[2];
278:   unsigned char		vn_cnt[2];
279:   unsigned char		vn_file[4];
280:   unsigned char		vn_aux[4];
281:   unsigned char		vn_next[4];
282: } Elf_External_Verneed;
```

Aux records, `readelf.c:14102-14106`: `vna_hash`(4), `vna_flags`(2), `vna_other`(2), `vna_name`(4),
`vna_next`(4) — matching `external.h:286-292`. So a record is **16 bytes** (`2+2+4+4+4`) and an aux
**16 bytes** (`4+2+2+4+4`); `vn_aux` is an offset from the *record start*, `vna_next` from the *aux start*
(`:14091` `vstart += ent.vn_aux;`, `:14129-14130` `isum += aux.vna_next; vstart += aux.vna_next;`).
Aux iteration is bounded by `vn_cnt` (`:14093`), not by `vna_next != 0` — the last aux may legally carry
`vna_next == 0` (`:14119`).

Quote (`external.h:277`, 3 words): **`unsigned char vn_version[2];`**

### 2.4 String-table resolution — DT_STRTAB/DT_STRSZ, *not* `sh_link`

The printer resolves names through the **dynamic** string table, not through `SHT_GNU_verneed`'s `sh_link`:

- `:14080` `if (valid_dynamic_name (filedata, ent.vn_file))` → `:14081-14082` print the string;
  else `:14084` `printf (_("  File: %lx"), ent.vn_file);` — the raw index, no refusal.
- Same discipline for aux names, `:14108-14113` (`Name: %s` vs `Name index: %lx`).
- `:467-471` `valid_dynamic_name` = `valid_symbol_name (filedata->dynamic_strings, filedata->dynamic_strings_length, offset)`;
  `:461-463` `valid_symbol_name` = `return strtab != NULL && offset < strtab_size;`; `:476-479`
  `get_dynamic_name` = `return filedata->dynamic_strings + offset;` (comment at `:474-475`: "GET_DYNAMIC_NAME
  asssumes that VALID_DYNAMIC_NAME has already been called").
- `sh_link` appears twice in the whole `SHT_GNU_verneed` block, **both times only for the human-readable
  `Link: %u (%s)` printout** (`:14047-14048`). The printer never validates `sh_link < e_shnum` — contrast the
  `SHT_GNU_versym` branch, which does (`:14168`, `:14174`).

Quote (`readelf.c:469-470`, 6 words): **`return valid_symbol_name (filedata->dynamic_strings, filedata->dynamic_strings_length, offset);`**

### 2.5 Three independent verneed walkers in one file

The same on-disk chain is decoded three times, with three different bounds disciplines. This matters for
the gate's reader ground: a shortcut replay of "readelf version-needs" can imitate any one walk and still
miss the others.

| walker | site | count bound | name bound |
|---|---|---|---|
| section printer | `:14058-14146` | `sh_info` + `endbuf` | `DT_STRSZ` (`valid_dynamic_name`) |
| versym → name | `:14286-14326` | `vna_next`/`vn_next` chains only | **linked section** `string_sec->sh_size` (`:14317-14320`, `name = invalid` at `:14318`) |
| symbol → version | `:14842-14893` | `vna_next`/`vn_next` chains only | `strtab_size` (`:14888-14889`, `_("<corrupt>")`) |

The two non-section walkers resolve `DT_VERNEED` through `offset_from_vma` (`:7825`), which needs
`PT_LOAD` program headers: `:7831` `warn (_("Cannot interpret virtual addresses without program headers.\n"));`,
`:7847-7848` `warn (_("Virtual address %#" PRIx64 " not located in any PT_LOAD segment.\n"), vma);`.

## 3. (b) Failure / refusal branches for truncated or malformed records

Ten refusal sites bound the `SHT_GNU_verneed` walk (probe count: **9 bare `break;`** statements and
**4 `warn (`** sites in lines 14020-14154). None is gated on `do_checks`; all bounds checks run
unconditionally.

| # | line | exact code | effect |
|---|---|---|---|
| 1 | `:14050-14055` | `eneed = (…) get_data (NULL, filedata, section->sh_offset, 1, section->sh_size, _("Version Needs section"));` / `if (!eneed)` / `break;` | whole section unreadable → **silent** skip (`found` was already set at `:14027`); `get_data` itself emits `:572` `error (_("Unable to read in %" PRIu64 " bytes of %s\n"), …)` |
| 2 | `:14067-14068` | `if (vstart + sizeof (*entry) > endbuf)` / `break;` | truncated Verneed header → stop records; `cnt < sh_info` → site 10 |
| 3 | `:14089-14090` | `if (ent.vn_aux > (size_t) (endbuf - vstart))` / `break;` | `vn_aux` points past section end → stop records |
| 4 | `:14098-14099` | `if (vstart + sizeof (*eaux) > endbuf)` / `break;` | truncated Vernaux → leaves aux loop with `j < vn_cnt` → site 8 |
| 5 | `:14118-14125` | `if (aux.vna_next < sizeof (*eaux)` `&& !(j == ent.vn_cnt - 1 && aux.vna_next == 0))` → `warn (_("Invalid vna_next field of %lx\n"),` / `j = ent.vn_cnt;` / `break;` | non-advancing aux chain → warn, abandon remaining aux |
| 6 | `:14127-14128` | `if (aux.vna_next > (size_t) (endbuf - vstart))` / `break;` | aux chain runs off the section → leave aux loop |
| 7 | `:14133-14134` | `if (j < ent.vn_cnt)` / `warn (_("Missing Version Needs auxiliary information\n"));` | aux shortfall diagnosed after the loop |
| 8 | `:14136-14142` | `if (ent.vn_next < sizeof (*entry)` `&& !(cnt == section->sh_info - 1 && ent.vn_next == 0))` → `warn (_("Invalid vn_next field of %lx\n"), ent.vn_next);` / `cnt = section->sh_info;` / `break;` | non-advancing record chain → warn, force-terminate count |
| 9 | `:14143-14144` | `if (ent.vn_next > (size_t) (endbuf - ((char *) eneed + idx)))` / `break;` | record chain runs off the section (note the base is `eneed + idx`, the *record start*, not the advanced `vstart`) |
| 10 | `:14148-14149` | `if (cnt < section->sh_info)` / `warn (_("Missing Version Needs information\n"));` | declared `sh_info` count not reached → warn, exit 0 |

Quote for a truncation refusal (`readelf.c:14149`, 4 words):
**`warn (_("Missing Version Needs information\n"));`**

Quote for a malformed forward pointer (`readelf.c:14121`, 5 words):
**`warn (_("Invalid vna_next field of %lx\n"),`**

Behavioural profile, observed from the code only: every malformed case degrades to a `warn`/`error` on
stderr plus a shortened listing, and `process_version_sections` **still returns `true`** (`:14418`). There is
no signal to the caller that the listing was incomplete; `main` only marks `res = false` when the function
returns false (`:25115`). `[INFERENCE]` A tool consuming readelf's version-needs listing cannot distinguish
"complete" from "truncated after warn" without the stderr text.

## 4. Depth notes worth carrying into S106's "teaches" cell

1. **Two bounds, one walk**: `sh_info` (count) and `endbuf` (bytes) are checked separately, so a file may be
   byte-short *and* count-short, producing site 2 and then site 10 for one record.
2. **The name table is not the section's `sh_link`**: the printer uses `DT_STRTAB`/`DT_STRSZ`; a carrier whose
   `SHT_GNU_verneed.sh_link` points elsewhere still prints correct names, and a carrier without
   `DT_STRTAB` prints bare indices (`File: %lx`, `Name index: %lx`) instead of failing.
3. **`vna_next == 0` is legal only on the last aux** (`:14119`) and `vn_next == 0` only on the record
   `sh_info-1` (`:14137`) — the two exemptions are count-dependent, not value-dependent.
4. **`DT_VERSIONTAGIDX` is reversed** (`:458`, `DT_VERNEEDNUM - tag`), so `version_info[]` indices do not follow
   tag numeric order; a replay that assumes ascending tags mis-indexes `DT_VERSYM`/`DT_VERNEED`.
5. **Absence is silent-by-count**: with no verneed section the message is `No version information found in
   this file.` (`:14415`) — indistinguishable, in text, from a file whose version sections are all zero-count.

## 5. Draft SOURCES row S106 (do not land — L1 writes `corpus/SOURCES.md`)

> | S106 | binutils-gdb `readelf.c` at tag `binutils-2_47` — `https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=binutils-2_47` (with `include/elf/external.h` at the same tag) | code | A | The release readelf's `SHT_GNU_verneed` decode: record order, count/byte bounds, name resolution, malformed-record refusals | Tag `binutils-2_47` = commit `6ce87bbc521cf46eaee9a1f7ef61cee2cdfb3e32` (2026-07-26); `readelf.c` sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`; `readelf.c:14020-14149`; `external.h:276-292`; `external.h` sha256 `938745254f7353db20cb9edcee910713ef9b2e8be8b42131d81582b107791d06`; | Version-need decoding is section-header-driven with a declared-count bound (`sh_info`), DT_STRTAB name resolution, three independent walkers, and warn-only degradation on malformed chains | mined | 2026-10-25 | on-release | (pending — round-34 C2 gate reader ground) |

Tier rationale: `A` = primary upstream release source read directly at a pinned tag, hash-recorded.
Scope is deliberately narrow: this row teaches the **GNU version-need reader**, nothing about carriers,
and nothing about the lane's own fixtures. It is the legitimate-reader ground the C2 gate needs, not a
score input.

## 6. Reproduction receipt

```
$ cd /fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource
$ python3 -I -B probe_s106.py            # 2026-10-25T07:20:10Z run: EXIT=1 (54 offsets wrong, split on FF)
$ … fixes: split on "\n" only; 2 remaining offsets re-derived with grep -n …
$ python3 -I -B probe_s106.py            # 2026-10-25T07:21:43Z: EXIT=0
capture readelf: …/readelf-pinned.c sha256=7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff bytes=689644
capture ext:     …/external-2_47.h  sha256=938745254f7353db20cb9edcee910713ef9b2e8be8b42131d81582b107791d06 bytes=12359
readelf lines=25625 ext lines=326 (split on \n only)
line-claims checked=69 mismatches=0
verneed-block lines 14020-14154: bare 'break;' count=9 warn-sites=4
verneed-block sh_link occurrences=2
PROBE OK
```

The first run's 54 mismatches were my own offset error (Python `splitlines()` also splits on the file's 3
form feeds), not capture drift; the capture sha256 was identical before and after. Reported rather than
hidden because an unrun check has not passed.

Tooling ledger: **nothing installed or upgraded**. `curl 8.23.0` (system) used for the one assigned fetch
plus tag/version verification at the same host. `pacman -Q binutils` (query only, no transaction) → `2.47-4`.

## 7. Remaining unknowns

- ~~Release date~~ **resolved**: `Sun, 26 Jul 2026 07:48:22 +0000` at commit `6ce87bbc…` (§1), and that
  commit's `readelf.c` is byte-identical to my capture.
- Whether host `readelf 2.47-4` (Arch build) contains downstream patches to these lines: not checked —
  the Arch source package was not fetched. The upstream tag proves upstream bytes only.
- The versym and symbol walkers were located and bounded (`§2.5`) but their refusal branches were not
  enumerated line-by-line; only the section printer got the full table in `§3`.
- `offset_from_vma`'s `(long) vma` fallback (`:7833`) when program headers are absent was noted, not
  analysed: whether a truncated-`PT_LOAD` carrier can steer `DT_VERNEED` resolution to a wrong file offset
  is open.

SOURCE_PINNED — S106 ground pinned at `binutils-2_47`, 69/69 quote assertions green, 10 refusal sites documented.
