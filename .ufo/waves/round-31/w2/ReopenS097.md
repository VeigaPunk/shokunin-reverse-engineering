# Reopen S097 — SQLite PRAGMA documentation row and its Gate quote

Scope: re-open `corpus/SOURCES.md:103` (S097) and the S097 row of the `## Gate` table in
`corpus/lessons/round-31.md:36` (both at lane tip `1288285e`), re-fetch the source, and test
the sha, the located quote, and every row column against the frozen SOURCES contract in
`/home/vgpnk/Projects/shokunin/CORPUS.md` § *SOURCES.md — where a shokunin learns*. Read-only
on the lane; no REA run; no installs; leaf seat, no agents.

**Verdict: agree with the row's claim and with nine of its ten substantive column checks;
disagree with one contract column — `used-by` is incomplete — and disagree with the lesson
Gate's characterization of it (`round-31.md:41`).** Details and counterexample below.

## Source reopened (Contract "Sources" record)

- URL `https://www.sqlite.org/pragma.html`, opened 2026-10-23 by ordinary `curl`.
- Producer: `curl -sS --max-time 120 -A "Mozilla/5.0 (X11; Linux x86_64) kaidoku-r31-reopen"
  -o pragma.html -w 'http_code=%{http_code} size=%{size_download}\n'
  https://www.sqlite.org/pragma.html`, run 2026-10-23T04:29:57Z (file mtime
  2026-10-23T04:29:58Z), exit 0. Output: `http_code=200 size=139936
  url=https://www.sqlite.org/pragma.html`.
- sha256 of the bytes read: `af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034`,
  139,936 bytes (`sha256sum pragma.html`, exit 0, 2026-10-23T04:31:58Z).
- Served headers (HEAD, 2026-10-23T04:30:30Z, exit 0): `Last-Modified: Thu, 22 Oct 2026
  16:45:56 GMT`, `ETag: "m6ada3dc4s222a0"`, `Content-length: 139936`.
- Located quote, line 2009-2010: `This pragma returns information about the tables and views
  in the schema, one table per row of output.` (18 words, ≤25).

## Checks

All commands run 2026-10-23T04:29:57Z–04:32:05Z; raw outputs in
`checks.log` (sha256 below). Paths below are absolute; `L` = the lane root.

### 1. sha256: row and Gate agree with the fetched bytes — holds

```
$ sha256sum pragma.html
af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034  pragma.html
$ ROW_SHA=$(grep -o 'af75d7d7[0-9a-f]*' L/corpus/SOURCES.md | sort -u); [ "$ROW_SHA" = "$FILE_SHA" ]; echo $?
0
row_sha=af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034 (len=64)
$ grep -o 'af75d7d7…[0-9a-f]\{4\}' L/corpus/lessons/round-31.md
af75d7d7…6034
```

- **Observation**: the S097 `anchor` cell carries the full 64-hex sha
  `af75d7d7…6034`; the Gate's truncated `af75d7d7…6034` is its 8+4 prefix/suffix. Both equal
  the sha of my independent fetch, 139,936 bytes, byte-identical to the wave-1 capture at
  `:…/seats/w1/SrcSqlitePragma/pragma.html` (`SrcSqlitePragma.md`, same sha and size).
- **Inference**: the page has not been re-served since the wave-1 fetch
  (`Last-Modified` 2026-10-22T16:45:56Z precedes both fetches).

### 2. Quote location, verbatim form, length — holds

```
$ grep -n "This pragma returns information about the tables and views" pragma.html
2009:    <p>This pragma returns information about the tables and views in the schema,
$ nl -ba pragma.html | sed -n '2009,2010p'
  2009	    <p>This pragma returns information about the tables and views in the schema,
  2010	    one table per row of output.  The table_list pragma first appeared
$ python3 ...   # whitespace-normalized comparison of lines 2009-2010
normalized_span: This pragma returns information about the tables and views in the schema, one table per row of output. The table_list pragma first appeared
quote_in_span: True quote_words: 18
```

- **Observation**: the Gate quote sits exactly at `:2009-2010`, inside `PRAGMA table_list`
  (section anchor `<a name="pragma_table_list">` at line 2004, next anchor `pragma_table_xinfo`
  at 2034). It is **18 words**, under the 25-word cap.
- **Observation / nuance**: a whole-file raw `count` of the quote string is 0 only because
  the served sentence is broken by newline + four-space indent between "schema," and "one";
  the quote is verbatim after whitespace normalization across that break, which is the
  correct reading of a two-line citation. No word is added, dropped or changed.

### 3. Row columns against the CORPUS.md contract — 10 hold, `used-by` fails

`awk -F'|' ... 'S097' → NF=13` ⇒ 11 columns; the contract census (malformed rows, duplicate
ids, enum/tier violations, missing used-by paths) prints nothing. Column by column:

| contract column | required | S097 | verdict |
|---|---|---|---|
| id | `S` + 3+ digits, next unused, never reused | `S097`; unique in the registry | holds |
| source | title — canonical URL | "SQLite PRAGMA documentation — https://www.sqlite.org/pragma.html" | holds |
| kind | one of the 10 enums | `docs` | holds |
| tier | A/B/C, scoped, `community` never A | `A`, official SQLite documentation, scope excludes REA implementation | holds |
| scope | the claim/topic the tier applies to | PRAGMA `table_list` object types and metadata; PRAGMA `table_xinfo.hidden`; explicitly "not REA's implementation or all SQLite versions" | holds |
| anchor | section/heading/page/line + revision, never a bare homepage | `PRAGMA table_list` 2004–2032; `PRAGMA table_xinfo` 2034–2042; fetch date 2026-10-23; full sha | holds with caveat (below) |
| teaches | one grounded learner benefit | four kinds; `ncol` includes generated+hidden; `wr`/`strict` as 1/0; `hidden` 0/1/2–3 | holds (all four are verbatim in the cited ranges) |
| status | queued/mined/rejected; `mined` ⇒ cited by ≥1 used-by path | `mined`; the listed entry uses `PRAGMA table_list` at entry lines 34 and 45 | holds |
| opened | ISO date opened | 2026-10-23, equal to the Gate access date | holds |
| recheck | ISO date or cadence | `180d` | holds |
| used-by | every entry/lesson citing the row | only `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | **fails** (§4) |

Grounded content check (`pragma.html`): `type` 2020–2022 ("table", "view", "shadow", "virtual"),
`ncol` 2023–2024 (including generated and hidden columns), `wr` 2025, `strict` 2026, and
`table_xinfo.hidden` 2040–2043 (normal 0; generated 2 or 3; virtual-table hidden 1). Every
claim in `teaches` appears there; nothing in `teaches` exceeds the documentation.

**Anchor caveat (observation, not a fail)**: both claimed ranges stop one line before the
section's last line — `table_list` continues to 2033 ("only information about that one table
is returned.") and `table_xinfo` to 2043 ("this field is non-zero are those omitted for PRAGMA
table_info."). Every field the row names is inside the claimed ranges, so `teaches` is
supported; only the range ends are imprecise. The "revision" supplied is an **access date plus
a content hash**, not a source-declared version — the page is mutable "current documentation"
whose only source-side handle is `Last-Modified: 2026-10-22T16:45:56Z`. Acceptable as a
snapshot pin; worth knowing that the row's line numbers are bound by the sha, not by a version.

### 4. `used-by` completeness — FAILS (counterexample)

```
$ awk -F'|' '...S097... {print "used-by=["$12"]"}' L/corpus/SOURCES.md
used-by=[ corpus/knowledge/2026-10-23-r31-sqlite-positive.md ]
$ git grep -l 'S097' HEAD -- corpus/knowledge
HEAD:corpus/knowledge/2026-10-23-r31-sqlite-positive.md
HEAD:corpus/knowledge/2026-10-23-r31-sqlite-refusals.md
$ git show HEAD:corpus/knowledge/2026-10-23-r31-sqlite-refusals.md | sed -n '3p'
source: S092 (…); S096 and S097 for the file-format and PRAGMA terms
```

- **Observation**: `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md:3` cites S097 in its
  `source:` prefix. The contract defines `used-by` as "repo-relative paths of the knowledge
  entries or lessons citing the row, comma-separated" — so the cell must list both entries.
  It lists one.
- **Observation**: the same class exists on two neighbouring rows: `S092` lists only the
  refusals entry while the positive entry cites S092 at line 3; `S096` lists only the positive
  entry while the refusals entry cites S096 at line 3. `S093`, `S094`, `S095` are accurate
  (only the positive entry cites them).
- **Inference**: the round's intent was both entries (the Gate says so, §5); the cells were
  populated with one path each.
- **Unknown**: whether the refusals entry's S097 citation is substantive — its body contains
  no `table_list`/`table_xinfo` term. Producer:
  `grep -n "table_list\|table_xinfo\|hidden\|ncol\|strict\|wr" L/corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`
  returns only lines 5 (`--write-evidence`) and 61 ("wrong"), i.e. the `wr` alternative
  matching `write`/`wrong`; no SQLite PRAGMA term appears. So the citation is nominal. By the letter of the contract it still counts; if the L1 instead
  strikes it from the refusals `source:` line, the used-by cell would become correct and the
  Gate sentence would become correct — either edit must be logged (contract rule 2 permits
  in-place `used-by` change only when the lesson logs old→new).

### 5. Gate line 41 overstates the `used-by` state — FAILS as written

```
$ sed -n '41p' L/corpus/lessons/round-31.md
Row changes old→new: none to existing rows; S092–S097 new (status `mined`, used-by the two round-31 entries).
```

- **Observation**: no row among S092–S097 has two `used-by` entries at HEAD; S093–S095 are
  cited by one entry only (the refusals entry does not mention them). As a statement about
  the committed registry, "used-by the two round-31 entries" is false for every row it covers.
  It could only be read charitably as intent, not as the committed cells.

### 6. Gate quote vs `teaches` — weak grounding (observation)

The Gate quote grounds the `table_list` topic sentence ("returns information about the tables
and views … one table per row") but none of the `teaches` specifics (`type`/`ncol`/`wr`/`strict`
values and `table_xinfo.hidden`). Those are grounded by the row's line ranges (2020–2026,
2039–2043), not by the Gate quote. Contract rule 1 asks for "a ≤25-word quote with its
location grounding `teaches`"; the quote is verbatim and correctly located but under-covers
what the row teaches. Not a false statement; a calibration weakness worth one line in the
Gate.

## Verdict

- **Row verdict: agree** on the source, kind, tier, scope, anchor (with the §3 caveat),
  teaches, status, opened and recheck; the sha and the located quote reproduce exactly.
  The row's `used-by` cell is **disagreed with**: it omits
  `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`, which cites S097 at line 3, so the row
  as committed is not fully conformant with the SOURCES contract (one mutable column; fixable
  under rule 2 with an old→new log line).
- **Gate verdict: agree** on URL, access date, sha, located quote (verbatim, 18 words, at
  `:2009-2010`) and the `admit, mined` decision; **disagree** with `round-31.md:41`, which
  describes a two-entry `used-by` that no committed row has.

## Remaining unknowns

- The page is unpinned "current documentation"; a later re-serve can change line numbers while
  the row's sha stays the historical pin. Only the sha makes the citation reproducible.
- Whether the refusals entry's nominal S097 citation should stand (see §4 unknown); that
  choice decides whether the fix is the `used-by` cell or the entry's `source:` line.
- No check was made of any other SOURCES row beyond S092/S096 (reported as adjacent) and the
  census commands, which were run and printed nothing.

## Artifacts (scratch)

- `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS097/pragma.html` —
  sha256 `af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034`, 139,936 bytes.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReopenS097/checks.log` —
  sha256 `78bc0dedab2ef6e9a556f1d4adfc6e5a000f73e2803cc4effce000cdf14358f6`.
- No REA invocation, no counter, no git/jj write, no install, no subagent.
