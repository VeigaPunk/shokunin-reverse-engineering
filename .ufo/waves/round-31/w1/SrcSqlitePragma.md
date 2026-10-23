# S097 — SQLite PRAGMA documentation

## Behavior
Opened the official SQLite PRAGMA documentation using ordinary `curl`. The `PRAGMA table_list` section defines the object types `table`, `view`, `shadow`, and `virtual`; its fields include `ncol` (including generated and hidden columns), `wr` (WITHOUT ROWID flag), and `strict` (STRICT-table flag). The `PRAGMA table_xinfo` section says `hidden` is 0 for normal columns, 1 for hidden virtual-table columns, and 2 or 3 for dynamic or stored generated columns.

## Gate
- URL: https://www.sqlite.org/pragma.html
- Access date: 2026-10-23
- SHA-256: `af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034`
- Size: 139936 bytes
- Quote (served HTML lines 2009–2010, `PRAGMA table_list`): “This pragma returns information about the tables and views in the schema, one table per row of output.”
- Located sections: `PRAGMA table_list`, lines 2004–2032 (`type` lines 2020–2022; `ncol`, `wr`, and `strict` lines 2023–2026); `PRAGMA table_xinfo`, lines 2034–2042 (`hidden` values).

Fetch command and observed result:
```sh
mkdir -p /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma && timeout 300 curl -fLsS https://www.sqlite.org/pragma.html -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html; rc=$?; printf 'curl_exit=%s\n' "$rc"; if [ "$rc" -ne 0 ]; then exit "$rc"; fi; sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html; wc -c /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html
```
```text
curl_exit=0
af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html
139936 /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html
```
Curl exit code: 0. The fetch command did not print a wall-clock timestamp. The saved file's mtime was observed as `2026-10-23T04:10:08Z` by `date -u -r /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html` (exit 0); this is the recorded capture timestamp, not a claim about curl's start time.

## Draft SOURCES.md row
Exact 11-column row (kind `docs`, status `mined`, requested ID and used-by):

```markdown
| S097 | SQLite PRAGMA documentation — https://www.sqlite.org/pragma.html | docs | A | SQLite definitions of `PRAGMA table_list` object types and schema metadata (`ncol`, `wr`, `strict`), and `PRAGMA table_xinfo.hidden` values used to interpret REA `inspect_sqlite_database` output; not REA's implementation or all SQLite versions | Current documentation fetched 2026-10-23; SHA-256 `af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034`; `PRAGMA table_list` lines 2004–2032 (`type`, `ncol`, `wr`, `strict`); `PRAGMA table_xinfo` lines 2034–2042 (`hidden`) | Distinguish SQLite's `table`, `view`, `virtual`, and `shadow` kinds; interpret `ncol` as including generated and hidden columns, `wr` and `strict` as 1/0 table flags, and `table_xinfo.hidden` as normal (0), virtual-table hidden (1), or generated (2/3). | mined | 2026-10-23 | 180d | corpus/knowledge/2026-10-23-r31-sqlite-positive.md |
```

The SQLite documentation grounds the field meanings; by itself it does not establish REA implementation behavior or a live REA result.

## Findings
- **Observation — source opened.** Producer: the `curl` command above. Output excerpt: `curl_exit=0`; SHA-256 `af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034`; `139936` bytes. Curl exit 0. Access date 2026-10-23; saved-file mtime `2026-10-23T04:10:08Z` (mtime-read command exit 0).
- **Observation — source sections.** Producer: `read` of `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html:2009-2048:raw`, plus `grep` of the downloaded file for `PRAGMA table_list|PRAGMA table_xinfo|shadow tables|the table_list pragma`. Exact excerpt: `This pragma returns information about the tables and views in the schema,` / `one table per row of output.` (lines 2009–2010); the row list gives `type` values at lines 2020–2022, `ncol` at 2023–2024, `wr` at 2025, `strict` at 2026, and `hidden` values in `table_xinfo` at lines 2039–2042. Both readers returned results successfully; they do not emit process exit codes or UTC call timestamps.
- **Observation — requested target entry is absent from the inspected lane snapshot.** Producer: `read` of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md`; exact output: `Path '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md' not found.` This was a successful tool response, not a shell process; exact call time was not emitted. The draft retains the requested `mined` status and `used-by`, but the path must exist and cite S097 before that status is contract-valid.
- **Observation — artifact metadata.** Producer: `timeout 300 bash -c 'date -u +"utc_now=%Y-%m-%dT%H:%M:%SZ"; sha256sum ... && stat ...; rc=$?; printf "artifact_metadata_exit=%s\\n" "$rc"; exit "$rc"'` for the two artifacts listed below. Output: `utc_now=2026-10-23T04:11:58Z`; raw page SHA-256 above and 139936 bytes; draft SHA-256 `77db516357888048dc17b88baa5f871dd66771454432fc32f0b54a05bb134f1a` and 913 bytes; `artifact_metadata_exit=0`. UTC time `2026-10-23T04:11:58Z`; exit 0.

## Touched surfaces
- Wrote only this scoped report in the lane: `.ufo/waves/round-31/w1/SrcSqlitePragma.md`.
- Scratch artifacts:
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/pragma.html` — SHA-256 `af75d7d7ab00c29e6eea98618cb1259a3919c308af60a6173215bf9798706034`, 139936 bytes.
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqlitePragma/s097-row.md` — SHA-256 `77db516357888048dc17b88baa5f871dd66771454432fc32f0b54a05bb134f1a`, 913 bytes.

## Out of scope and limits
- Did not edit `corpus/SOURCES.md` or create/change the named knowledge entry; lane bounds permit only this report. The row above is a draft for integration, and its requested `mined` state depends on the currently missing used-by file being added and citing it.
- No REA invocation or counter, tests, install/update, git/jj command, or subagent dispatch.
- Inference limited to official SQLite documentation semantics; no claim is made here about a live REA envelope or behavior beyond the round-31 task's scope.
