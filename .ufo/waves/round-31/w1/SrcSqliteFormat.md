# S096 — SQLite file-format source

## Behavior
Opened the SQLite Database File Format page with an ordinary `curl` fetch. Drafted (not inserted) the requested `S096` registry row for the round-31 SQLite-positive knowledge entry. The location references below are raw line numbers in the downloaded HTML.

## Draft `corpus/SOURCES.md` row

| S096 | SQLite Database File Format — https://www.sqlite.org/fileformat2.html | spec | A | SQLite database-file signature and header, b-tree pages, payload overflow, and record serial types relevant to the R31-C1 SQLite byte parser; not REA's live output | `Database File Format`; header fields :265-279; header-string sentence :328-330; text-encoding field at offset 56 :308-310 and section :526-533; b-tree page header :778-801; table-leaf and index overflow calculations for U-35, M, and K :974-1016; record serial types :1136-1183; fetched HTML SHA-256 `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2` | Defines the on-disk signature and layout rules for tracing SQLite pages, overflow payloads, and record types in the C1 parser; it does not establish REA's actual operation result. | mined | 2026-10-23 | 180d | corpus/knowledge/2026-10-23-r31-sqlite-positive.md |

## Gate

**Gate:** URL https://www.sqlite.org/fileformat2.html; accessed 2026-10-23; SHA-256 `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2`; size 110473 bytes; quote at lines 328-330: “This byte sequence corresponds to the UTF-8 string \"SQLite format 3\" including the nul terminator character at the end.”

**Fetch command:** `timeout 300 sh -c 'mkdir -p /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat && curl --fail --location --silent --show-error https://www.sqlite.org/fileformat2.html -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html'` — exit code `0`.

Captured command output:

```text
curl-command=timeout 300 sh -c 'mkdir -p /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat && curl --fail --location --silent --show-error https://www.sqlite.org/fileformat2.html -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html'
exit=0
905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2  /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html
110473 /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html
```

## Findings

- **F1 — source capture [OBSERVATION].** Producer: the fetch command above, followed by `sha256sum /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html` and `wc -c /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html`. Exact output excerpt: `exit=0`; `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2`; `110473`. Exit code: `0` for fetch; the recorded `sha256sum` and `wc` outputs were successful. UTC review timestamp: `2026-10-23T04:10:44Z` (the fetch command did not emit its own timestamp).
- **F2 — format passages [OBSERVATION].** Producer: successful `read` calls on the downloaded HTML at the ranges cited below (the read interface does not expose process exit codes). Exact excerpts: header page-size field, `and 32768 inclusive, or the value 1 representing a page size of 65536.` (:277-278); offset-56 field, `The database text encoding. A value of 1 means UTF-8.` (:308-310); b-tree header, `The b-tree page header is 8 bytes in size for leaf pages and 12` / `bytes for interior pages.` (:778-779); overflow, `Let X be U-35.` and `Let M be ((U-12)*32/255)-23 and let K be M+((P-M)%(U-4)).` (:977-979), with the index counterpart and overflow cases at :994-1016; record serial types, `These additional varints are called "serial type" numbers and determine the datatype of each column` (:1140-1142), with the chart at :1145-1183. The header-string quote is recorded in Gate above. UTC review timestamp: `2026-10-23T04:10:44Z`.
- **F3 — intended used-by target [OBSERVATION].** Producer: `read /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md`. Exact result: `Path '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md' not found.` The row uses the assignment-specified path, but this target was absent at inspection time. Read interface exit code: not exposed. UTC review timestamp: `2026-10-23T04:10:44Z`.

## Gates and boundaries

- **Gate outcome [OBSERVATION]:** source opened and digest/size recorded; all requested line references located in the captured page. The requested row is drafted with status `mined` and the specified `used-by` path; that path must exist when integrated for the mined-row contract to validate.
- **Touched surfaces:** this report; `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html`.
- **Out of scope:** did not edit `corpus/SOURCES.md` or the knowledge entry (lane files are read-only except this report); did not run REA, counters, or validation; installed no tools.
- **Artifact paths:** `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcSqliteFormat/fileformat2.html` — SHA-256 `905067afacc30583c9ee86778b532094cc1830c7ec7b5f019bcfd2eb9ded97a2`, 110473 bytes.
