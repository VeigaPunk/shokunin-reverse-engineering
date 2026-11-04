# R68-V2 — the round-68 knowledge-index row sits above the table header

## Live state: committed at `5ee94c56`, defect survives

`corpus/README.md` at HEAD (sha256 `43d01520bda813bc059e1556483433a3e3b7a942bd22556d360066616cf1801f`, 320
lines; worktree identical): the landing commit moved the **row** (header 118, delimiter 119, round-69 row
120, round-68 row 121) and the knowledge table is still **not parsed**, because the delimiter row was
shortened to three cells while the header has four. The remaining delta is the single-line fix at the end
of this file. The scratch mirror below is the pre-landing demonstration of the movement half, computed
from the dispatch commit `3f3d20fc` bytes.

Target: `corpus/README.md`, `## Knowledge` table.

Three revisions are in play, and they are not the same bytes:

| revision | sha256 | state |
|---|---|---|
| dispatch commit `3f3d20fc…` | `9033cb388aa4e8ca2fd1429fd1c6d278a2e172e82f594992790bbf746f6c03ba` | row at 118, header 119, delimiter 120 — **defect present** |
| landing commit `5ee94c56` (== live worktree) | `43d01520bda813bc059e1556483433a3e3b7a942bd22556d360066616cf1801f` | row moved below the header, but the delimiter was shortened to 3 cells — **table still does not parse** |
| landing commit + the one-line fix below | `eb459258a1305b9fbe20d9618ea604562407cb49e0cbaab8247180869a16fa62` | **parses** |

Observation (strict GFM with `markdown-it-py` 4.2.0, `MarkdownIt("gfm-like", {"linkify": False})`):
a table needs a header row, then a delimiter row **with the same number of cells**, then body rows.
`evidence/table-parse.txt` carries every block and verdict.

## The exact row line (verbatim, 447 bytes, 5 cells)

```
| `2026-11-03-r68-packed-elf-route` | UPX-packed ELF through a detect → unpack → identity → recover route: the packed stub's parsed inventory (3 procedures), byte restoration against the carrier pin, the REA inventory recovered from the unpacked copy, and the address-level refusal that separates the two states; limits UPX 5.2.0 / `linux/elf386` / default packing | `tools/round-68/packed-elf.py` + `.ufo/waves/round-68/l1/scores/` | 2026-11-03 |
```

## Scratch mirror at the dispatch commit: line numbers before → after

Procedure: copy `HEAD:corpus/README.md` to `/fast/scratch/hyaku/kaidoku-r69/ExecLedger`, delete the
row line, re-insert it as the first body row after the 4-cell delimiter (`README.mirror.md`, sha256
`e865a0ddfd44047057ec0002774d65cc33d935ef0ca9590bce7d61ea2fe9e289`).

| line | HEAD | MIRROR |
|---|---|---|
| 117 | `## Knowledge` | `## Knowledge` |
| 118 | the r68 row (**above the header**) | `\| entry \| topic \| source \| verified-at \|` |
| 119 | `\| entry \| topic \| source \| verified-at \|` | `\|---\|---\|---\|---\|` |
| 120 | `\|---\|---\|---\|---\|` | the r68 row (**first body row**) |
| 121-240 | 120 body rows | the same 120 body rows, unchanged numbers |
| body rows | 0 parsed (block 118-240 fails at line 119) | 121 parsed (block 118-240 ok, 4/4 cells) |

Line count is unchanged (319 lines); total rows in the file are unchanged; only the row's position
changes, by +2 lines.

Parse, before/after, from `evidence/table-parse.txt`:

- HEAD: `block 118-240: FAIL — line 119 is not a delimiter (a row sits above the header)`; the
  knowledge-row window renders `<table> 0, <th> 0, <td> 0`, first tag `<p>`.
- MIRROR: `block 118-240: header 4 cells, delimiter 4 cells, body widths [4], rows 121 -> ok`; the
  same window renders `<table> 1, <th> 4, <td> 8`.

## The fix that is still needed at HEAD (mandatory)

The landing commit already moved the row (and added the round-69 row above it), so the movement half of
R68-V2 is done. The delimiter, however, was changed from four cells to three:

```
118 | entry | topic | source | verified-at |      <- 4 header cells
119 |---|---|---|                              <- 3 delimiter cells
120 | `2026-11-03-r69-packed-route-contract` | …
121 | `2026-11-03-r68-packed-elf-route` | …
```

Strict GFM verdict at HEAD: `block 118-241: header 4 cells, delimiter 3 cells, body
widths [4], rows 122 -> CELL-COUNT MISMATCH`; the knowledge window still renders `<table> 0`. So the
human index still does not carry the round-68 entry.

**Exact one-line fix** — `corpus/README.md:119`, replace

```
|---|---|---|
```

with

```
|---|---|---|---|
```

Nothing else changes. With only that byte change (`README.worktree-fixed.md`, sha256 `eb459258…`):
`block 118-241: header 4 cells, delimiter 4 cells, body widths [4], rows 122 -> ok`; the window
renders `<table> 1, <th> 4, <td> 12`.

## Scope of the "every row has the delimiter above it" claim

Asserted for the **Knowledge table** (block 118-240 at the dispatch commit; 118-241 at HEAD). The file
carries pre-existing malformed table material that this ticket does not touch and this draft does not
change — recorded, not fixed:

- block 90-111 (continuation of the coverage map): no header/delimiter above it (blank line at 89
  splits the table);
- single pipe lines at 113 and 115 (the round-67/68 coverage rows) separated by blank lines;
- block 243-272 (Lessons): body widths `[3, 4]` against a 3-cell header.

Same list at the dispatch commit and at HEAD (`evidence/table-parse.txt`), so it is not a regression from
this round.
