# W2 ReopenS096 — S096 (`https://www.sqlite.org/fileformat2.html`) re-opened

Seat `KaidokuR31.ReopenS096` (wave 2, one v1 falsify wave). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `c369242fee9f559f895e3f7956b1242076c7b1be`; row and Gate frozen at `35ba7c52`; row committed at `0007731e`.
Scratch: `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS096/`. No lane file touched except this report.

## Verdict

**Agree.** S096 is what it says it is: the fetched bytes hash to the recorded SHA-256, the Gate quote is
verbatim (19 ≤ 25 contiguous words) at exactly `:328-330`, every column survives the maintained census
validator, and its `used-by` entry exists, cites S096, and uses it for a claim the cited spec actually
supports. Two non-blocking precision findings: the `anchor` cell records no publication date/version
(the page declares one), and two of its six line ranges stop mid-table (F4); neither is a false pointer
and neither touches the R31-C1 claim.

| id | kind | finding | severity |
|---|---|---|---|
| F1 | observation | fetch reproduced the recorded SHA-256 byte-for-byte in an independent, later fetch | holds |
| F2 | observation | quote is verbatim and 19 words; `:328-330` is the exact start/end line | holds |
| F3 | observation | 11 columns, NF=13, census validate clean; only W04 fleet warnings, none S096 | holds |
| F4 | observation + inference | anchor ranges `:265-279` and `:778-801` stop mid-table and omit fields the C1 parser uses | minor, under-inclusive |
| F5 | observation | `used-by` entry exists at lane and at `0007731e`, cites S096 twice, and S096 supports its claim | holds |
| F6 | observation | lesson Gate row carries URL, access date, SHA, located quote, decision per contract Rule 1 | holds |

## F1 — fetch and SHA-256 (observation)

Command (UTC printed at start; exit 0):

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS096 && date -u +%Y-%m-%dT%H:%M:%SZ && \
curl -sS -D headers.txt -o fileformat2.html -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  https://www.sqlite.org/fileformat2.html && sha256sum fileformat2.html && wc -l fileformat2.html
```

Exact output excerpt:

```
2026-10-23T04:29:46Z
http_code=200 size=110473 url=https://www.sqlite.org/fileformat2.html
905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2  fileformat2.html
2194 fileformat2.html
```

Headers (`headers.txt`): `HTTP/1.1 200 OK`, `Date: Fri, 23 Oct 2026 04:29:46 GMT`,
`Last-Modified: Thu, 22 Oct 2026 16:45:56 GMT`, `Content-type: text/html; charset=utf-8`,
`Content-length: 110473`.

Comparisons, all exact string matches:

| where | value | command |
|---|---|---|
| `corpus/SOURCES.md:102` (S096 anchor cell) | `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2` | `awk 'NR==102' corpus/SOURCES.md` |
| `corpus/lessons/round-31.md:35` (Gate table, abbreviated) | `905067af…97a2` | `sed -n 35p corpus/lessons/round-31.md` |
| wave-1 seat's retained bytes (second, earlier fetch) | `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2`, 110473 bytes | `sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html` (exit 0) |

So two independent fetches ~3 h apart (wave-1 file mtime 01:09 local, this fetch 04:29:46Z) agree on the
hash; the recorded digest is not a mistyped or stale value. The page's own revision stamp, located in the
served bytes, is line 2193: `This page was last updated on 2025-12-25 10:33:36Z` — see F3 note (b).

## F2 — the Gate quote (observation)

The lesson cell reads (raw bytes, `corpus/lessons/round-31.md:35`):

```
`:328-330`: "This byte sequence corresponds to the UTF-8 string \"SQLite format 3\" including the nul terminator character at the end."
```

Python check over the fetched bytes (`python3 - <<'EOF' … EOF`, exit 0):

```
328 (in hex): 53 51 4c 69 74 65 20 66 6f 72 6d 61 74 20 33 00.  This byte sequence
329 corresponds to the UTF-8 string "SQLite format 3" including the nul
330 terminator character at the end.</p>
quote in whitespace-normalized bytes: True
quote word count: 19
start line 328 end line 330
```

- **≤25 words:** 19 (`printf '%s' '<quote>' | wc -w` → `19`).
- **Verbatim:** true after HTML line breaks normalise to spaces; the raw-byte contiguous test is false
  only because the sentence spans the three source lines above. The quote begins at a sentence boundary
  (`33 00.  This byte sequence`) and ends before the closing `</p>`, so nothing is elided inside it.
- **Location:** start 328, end 330 — the cited `:328-330` is exactly right, not off by a line.
- **Raw-cell caveat:** the cell writes `\"` (JSON-style escapes) where the source has plain `"`. Under
  CommonMark a backslash before ASCII punctuation is an escape, so the rendered quote is verbatim; the
  two backslashes are extra characters in the raw markdown only. No action needed, recorded for exactness.

## F3 — columns against the CORPUS.md SOURCES contract (observation)

Contract read at `/home/vgpnk/Projects/shokunin/CORPUS.md:64+` (`## SOURCES.md — where a shokunin learns`,
Contract v1). Row fields as split (`awk 'NR==102' corpus/SOURCES.md | tr '|' '\n' | nl -ba`): `S096` ·
`SQLite Database File Format — https://www.sqlite.org/fileformat2.html` · `spec` · `A` · scope · anchor ·
teaches · `mined` · `2026-10-23` · `180d` · `corpus/knowledge/2026-10-23-r31-sqlite-positive.md`.
Row has 11 columns (`NF=13`, `awk -F'|' '{print NF}'` → `13`), no `|` inside a cell.

Maintained validator, run from the lane root so `used-by` resolves against the corpus (read-only mode):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && timeout 300 bash \
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md \
  --today 2026-10-23 > .../census-validate.txt 2>&1
EXIT=0
```

Output is `ok` plus 8 `W04` fleet warnings (duplicate URLs on S033/S047/S054/S062/S069/S083/S090/S092);
`awk -F'\t' '{print $2}'` counts `1 ok`, `8 W04`. **No S096 line appears at all** — no E01–E12 and no
W01–W04 for this row. `grep S096` on the validator output is empty; so `kind=spec`, `tier=A`,
`status=mined`, `opened` ISO, `recheck=180d` (valid cadence; due 2027-04-21), and the `used-by` path all
pass the contract's own checks.

Process note so a reader is not misled: a first validate invocation run from the seat scratch dir with
`--file ./SOURCES-copy.md` reported `E11` for nearly every row *including* S096, because `used-by` paths
are cwd-relative; that was an invocation artifact of this seat, not a registry defect, and the lane-root
run is clean.

Two conformance notes, neither a false statement in the row:

- (a) **Anchor revision form.** The contract asks the anchor to carry "revision (version, commit, or
  publication date)". S096's anchor carries a content SHA-256 and `opened: 2026-10-23`, but no
  version/commit/date of the page. A hash pins the bytes (strictly stronger than a date for identity),
  yet none of the three enumerated forms is present. Other web rows differ: S097 says "Current
  documentation fetched 2026-10-23", S031/S034 say "Page fetched 2026-10-20 (sha256 …)". Honest label:
  conformance in substance, deviation in form.
- (b) The page declares a publication/update date that the row does not record — line 2193,
  `This page was last updated on 2025-12-25 10:33:36Z` — and the HTTP `Last-Modified` is
  `2026-10-22 16:45:56 GMT`, later than that in-page stamp. Why the two differ is unknown (server-side
  templating is the inference); it strengthens the case for pinning by hash rather than by date, which
  is what the row does.

## F4 — anchor ranges (observation, plus one inference)

All six ranges land on the passage they name (`sed -n '<range>p' fileformat2.html`, run once per range):

| cell text | lines | lands on | verdict |
|---|---|---|---|
| header fields `:265-279` | 265-279 | header preamble + `Database Header Format` table opening, offsets 0/16 and start of 18 | right passage, **range truncated** |
| text-encoding field at offset 56 `:308-310` | 308-310 | offset-56 field row and its two-line description | exact |
| section `:526-533` | 526-533 | `1.3.13. Text encoding` heading through "No other values are allowed." | exact |
| b-tree page header `:778-801` | 778-801 | page-header preamble, table, offsets 0/1/3/5 | right passage, **range truncated** |
| overflow calc `:974-1016` | 974-1016 | table-leaf X=U-35/M/K block, index counterpart, alternative description through the P>X/P-M line | covers both computations |
| record serial types `:1136-1183` | 1136-1183 | record-format preamble and the full serial-type table (closes `</table></center>` at 1183) | exact |

Truncations, measured: the `Database Header Format` table spans `:270-323` (fields 0–96), so `:265-279`
stops at the offset-18 write-version description; it omits the offset-20 reserved-space byte at
`:283-284` (`Bytes of unused "reserved" space at the end of each page.  Usually 0.`), which the C1 oracle
reads at `tools/round-31/sqlite_oracle.py:93` (`return ps, ps - data[20], enc`), and the offset-56
encoding field (cited separately). The b-tree page-header table spans `:778-809`; `:778-801` stops after
offset 5, omitting offset 7 (`:802-805`, fragmented free bytes) and offset 8 (`:806-809`, "The four-byte
page number at offset 8 is the right-most pointer"), which the oracle uses at
`tools/round-31/sqlite_oracle.py:119` (`walk(int.from_bytes(p[off + 8:off + 12], "big"))`).

**Inference (not observation):** the ranges are under-inclusive fragments, not wrong pointers — each
points at the start of the passage it labels. Because contract Rule 2 changes an anchor only through a
superseding row, I do not recommend superseding S096 for this; a reader of the row should read
`header fields :265-323` and `b-tree page header :778-809`.

## F5 — `used-by` (observation)

- Entry `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` exists, 10405 bytes
  (`ls -l`, exit 0), and is committed as of `0007731e`
  (`git cat-file -e 0007731e:corpus/knowledge/2026-10-23-r31-sqlite-positive.md` → exit 0,
  printed `ENTRY-IN-0007731e=yes`).
- It cites S096 twice (`grep -c S096` → `2`): line 3 `source: S096 (SQLite file format, the spec the
  oracle's byte parser implements); …`, and line 34 "the `sqlite_schema` rows … come from a pure-Python
  reader of the file format (S096: header, table b-tree pages, overflow chains, record serial types)".
- The citation is backed by code, not decorative: `sqlite_oracle.py:84` compares the magic
  (`data[:16] != b"SQLite format 3\x00"`), `:93` uses the reserved-space byte, `:120-128` implements
  exactly the doc's `x = usable - 35; m = ((usable-12)*32//255)-23; k = m + ((size-m)%(usable-4))`, and
  `:60-79` decodes the serial-type codes — the four things S096's `scope`/`anchor` name.
- The row's draft is reproducible: the wave-1 draft row in `.ufo/waves/round-31/w1/SrcSqliteFormat.md`
  and the committed row at `corpus/SOURCES.md:102` are byte-identical (`diff` exit 0, `ROW-IDENTICAL-TO-DRAFT`),
  which supports the lesson's claim that the L1 copied the drafted row.

## F6 — Gate row (observation)

`corpus/lessons/round-31.md:35` contains, in one row: URL `https://www.sqlite.org/fileformat2.html`;
access `2026-10-23` (matches the HTTP `Date`); SHA abbreviation `905067af…97a2` (matches prefix and
suffix of F1's digest); located quote ``:328-330``; decision `admit, mined (`SrcSqliteFormat.md`)`.
That satisfies contract Rule 1's URL + access date + ≤25-word located quote, and the `decision` agrees
with the row's `status: mined`.

## Boundaries and unknowns

- **Observed:** everything above; every claim carries its command and exit code.
- **Unknown:** whether sqlite.org will serve the same bytes to another host/session later (the row's
  digest is the defence; a future mismatch is detectable, not predicted); why `Last-Modified`
  (2026-10-22) post-dates the in-page stamp (2025-12-25) — no evidence here, inference only.
- **Out of scope / not run:** no REA invocation, no counter run (none needed), no edits to lane files,
  no git/jj writes anywhere, no subagents, no tool installs.
- **Read-only git used:** `git log -- corpus/SOURCES.md`, `git show 0007731e:corpus/SOURCES.md`,
  `git cat-file -e`, all with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset and no writes.

## Artefacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS096/`)

| file | sha256 |
|---|---|
| `fileformat2.html` (110473 bytes) | `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2` |
| `headers.txt` | `ced3d0e707bcc9ba9594cb92e7df4c6af8d2b1dbc284e95e3b3147334d83c392` |
| `census-validate.txt` | `788e871782310d68ce99180869fa828ba1fc3a40dd06614531e259444f90b34c` |
| `draft-row.txt` | `ec9573240ddd076912c265a48b30d7ee4bfb776839ba56b83a2e9d16bfa28094` |
| `lane-row.txt` (identical to `draft-row.txt`) | `ec9573240ddd076912c265a48b30d7ee4bfb776839ba56b83a2e9d16bfa28094` |
| `SOURCES-copy.md` | `c129b27388614aaa17006a8c27ef0fe71382cc1da642cfc44461bc0a92e8a61c` |

Tools installed or updated: none. Sources opened: only `https://www.sqlite.org/fileformat2.html` by
plain `curl` (200, 110473 bytes, access 2026-10-23, sha256 above), plus lane and fleet files read
locally. No browser, no challenge bypass.
