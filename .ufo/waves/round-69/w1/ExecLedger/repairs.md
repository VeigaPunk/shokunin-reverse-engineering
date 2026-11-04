# ExecLedger — R68-V1 / R68-V2 / R68-V5 repair drafts and post-landing verification (r69-w1)

Seat: executor, leaf. Write scope: this directory and
`/fast/scratch/hyaku/kaidoku-r69/ExecLedger/` (deleted before yield; receipts copied here first).
No tracked lane file was edited by this seat, no index touched, no commit, no push; the only writes
outside scratch are in `.ufo/waves/round-69/w1/ExecLedger/`.

## 0. State of the tree when this seat measured

The L1 landed and committed the round while this seat was drafting, so the drafts below are split into
"the exact text as ordered" and "what the landing commit actually carries".

| revision | what it is |
|---|---|
| `3f3d20fc065b5be62f676028b9a38d316ddfe8fd` | wave dispatch commit; the bytes this seat first measured (README `9033cb38…`, SOURCES `abb44aa4…`, r68 entry `00f1a03a…`, 80 lines, no trio) |
| `5ee94c56ce7490938ee38c2e5c10930a1fd1330a` | landing commit, 2026-11-03 23:44:58 -0300, subject: "round-69 landing: … **the six r68 repairs**; S270; QUALITY 112-114; the provenance gate" |

At HEAD (`5ee94c56`, worktree bytes identical, `git status` clean for every tracked corpus file):

| file | sha256 at HEAD | state |
|---|---|---|
| `corpus/README.md` | `43d01520bda813bc059e1556483433a3e3b7a942bd22556d360066616cf1801f` | row moved; **delimiter has 3 cells against a 4-cell header → the knowledge table still does not parse** |
| `corpus/SOURCES.md` | `f0420431eb8a85877e66c5eb431619abe1645178fb0ec25f257e916214fd561d` | 177 rows; S269 at 186 still says `(11 words)`; S270 at 187 (`code`, packer source); **no S271** |
| `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` | `6fe62359de3361ee3c9a2b0491667cf67df355181da7bf638847c2a6460d9612` | 101 lines; correction block at 82-101 with the trio as three list items |
| `corpus/lessons/round-69.md` | `0a2de53df41281f3e0f6b1a9dd7a20c981811841c258b151a6a163a70df6bae9` | Gate 25-31 and M69-3 at 41 record "S269 is not superseded" |
| `tools/round-69/provenance-check.py` | `dff47b9206aa2bedc16ad229281ae8e2b20edb12f6f0ae4374407219795b77cb` | new gate; binds C1/C2/C3 receipts to instrument+revision — it does not check the knowledge trio |

Receipts: `evidence/revisions.txt` (both revisions, explicit `git show` hashes), `evidence/table-parse.txt`,
`evidence/v1-trio.txt`, `evidence/row-s271.txt`, `evidence/word-count.txt`,
`evidence/supersede-precedent.txt`.

## 1. State per routed defect (observation at HEAD)

| id | as committed | evidence |
|---|---|---|
| R68-V1 | **closed** — the trio is present as three list items in the appended block, entry text not rewritten | `grep -cE '^- `(source\|verified-at\|recheck):`'` on HEAD bytes = 3 (`evidence/v1-trio.txt`) |
| R68-V2 | **NOT closed** — the row moved, the table still does not parse because the delimiter lost a cell | strict GFM on HEAD: `header 4 cells, delimiter 3 cells -> CELL-COUNT MISMATCH`; window renders `<table> 0` (`evidence/table-parse.txt`) |
| R68-V5 | **the lane records it closed by the recorded-reason branch** the closure's routing allowed; S269 keeps `(11 words)` | `corpus/lessons/round-69.md:25-31`, `:41`; `corpus/SOURCES.md:186`; the alternative supersede row is drafted in `v5-supersede-row.md` but not landed |

The landing commit's subject says "the six r68 repairs". Measured at its own HEAD, R68-V2's repair does
not achieve the routed outcome: the human index still does not carry the round-68 entry. That is the one
status-relevant finding in this file. (R68-V3/V4/V6 are outside this seat.)

## 2. R68-V1 — the round-68 entry's provenance trio (closed; do not append a second block)

Observation: `corpus/knowledge/2026-11-03-r68-packed-elf-route.md:82` opens
`## Correction — round 69 (appended 2026-11-03; the filed text above is not rewritten)`, and lines
90/94/95 carry `- \`source:\``, `- \`verified-at:\``, `- \`recheck:\``.

```
$ git show HEAD:corpus/knowledge/2026-11-03-r68-packed-elf-route.md | grep -cE '^- `(source|verified-at|recheck):`'
3
```

That is the shape `QUALITY.md` #101 and #112 require ("anchored as a list item naming its field …
never a line-start field of the filed text"). Red/green over explicit revisions
(`evidence/v1-trio.txt`): dispatch bytes = 0, dispatch + this seat's drafted block = 3, HEAD = 3. The
entry's filed text is unchanged (pure append).

`v1-correction-block.md` holds the exact block this seat drafted before the landing, the red/green
design, and the two options if the L1 wants the landed `verified-at:`/`recheck:` cells widened (they name
only the landing commit and "the two frozen counters"; the draft names `c2-at-landing.json`, the
instrument sha256 and the two carrier pins). **Do not append a second block** — the shape is met.

Precision, not a defect: the landed fields are backticked list items, so the corpus sweep at
`/home/vgpnk/Projects/shokunin/CORPUS.md:170` (`grep -rlE '^[-* ]*recheck *:'`) will not match them, and
the line-start grep `^(source|verified-at|recheck):` stays 0. That is exactly what #101 says to expect;
#101 also says a receipt that checks such a field must grep unanchored and call its count
occurrence-based (`evidence/v1-trio.txt` does).

## 3. R68-V2 — the index row moved, the table still does not parse (the open defect)

HEAD bytes, `corpus/README.md`:

```
118 | entry | topic | source | verified-at |      <- 4 header cells
119 |---|---|---|                              <- 3 delimiter cells
120 | `2026-11-03-r69-packed-route-contract` | …
121 | `2026-11-03-r68-packed-elf-route` | …     <- byte-identical to dispatch:118 (447 B, sha prefix f95c9ef6d796b552)
```

Strict GFM (`markdown-it-py` 4.2.0, `MarkdownIt("gfm-like", {"linkify": False})`):
`block 118-241: header 4 cells, delimiter 3 cells, body widths [4], rows 122 -> CELL-COUNT MISMATCH`;
the knowledge-row window renders `<table> 0, <th> 0, <td> 0` — a paragraph, exactly the defect R68-V2
routed.

**Exact remaining fix — one line, `corpus/README.md:119`:** replace

```
|---|---|---|
```

with

```
|---|---|---|---|
```

Nothing else changes. Measured on a copy of HEAD bytes with only that byte change
(`README.worktree-fixed.md`, sha256 `eb459258a1305b9fbe20d9618ea604562407cb49e0cbaab8247180869a16fa62`):
`block 118-241: header 4 cells, delimiter 4 cells, body widths [4], rows 122 -> ok`; the window renders
`<table> 1, <th> 4, <td> 12`.

Pre-landing demonstration (`v2-index-row-move.md`, `evidence/table-parse.txt`): at the dispatch commit,
block 118-240 fails at line 119 (a row above the header) and renders 0 tables; moving only the row below
a 4-cell delimiter (mirror sha256 `e865a0dd…`) gives `header 4, delimiter 4, body [4], rows 121 -> ok`
and `<table> 1`. Line map (dispatch → mirror): 118 row → 120; 119 header → 118; 120 delimiter → 119;
121-240 body unchanged.

Scope honesty: "every row has the delimiter above it" is asserted for the **Knowledge table only**. The
file carries pre-existing malformed blocks, identical at the dispatch commit and at HEAD, untouched by
this ticket: 90-111 (no header/delimiter above it), single rows at 113 and 115, and Lessons 244-273 with
body widths `[3, 4]` against a 3-cell header. Recorded, not fixed.

## 4. R68-V5 — the count, the exact supersede row, and the branch the landing shipped

Measurement (`evidence/word-count.txt`):

```
$ printf '%s' 'Packed programs will be byte-identical to the original after uncompression' | wc -w
10
$ printf '%s' 'Packed programs will be byte-identical to the original after uncompression.' | wc -w
10
$ printf '%s' 'Packed programs will be byte-identical to the original after uncompression' | tr '-' ' ' | wc -w
11
```

Re-derivation: `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt` → HTTP 200,
37 208 B, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` (equal to S269's
pin); heading `NOTES FOR LINUX/ELF386` line 433, next `NOTES FOR` line 475, quote composed from 441-442 =
10 whitespace words, one occurrence of `byte-identical` in 433-474. The 11 came from splitting the
hyphen in `byte-identical`; `wc -w` splits on whitespace only.

**Exact row (S271)** in `v5-supersede-row.md`: 11 cells, `teaches` opens `supersedes S269 — `, no raw
`|` inside a cell, checked in `evidence/row-s271.txt`; insert at `corpus/SOURCES.md:188` (after the S270
row at 187, before the blank line; `## Paths` moves 189 → 190); registry 177 → 178 rows; renumber only
cell 1 if a sibling takes S271 first. **Lesson note** (exact append block for
`corpus/lessons/round-68.md`, whose Gate rows (a) and (e) carry the two false labels) and an exact
`## Corrections to round 68` bullet for `corpus/lessons/round-69.md` are in the same file.

**What the landing shipped instead.** The closure's routing offered "a new row … **or** a recorded
reason to leave the label"; the landing took the second:

- `corpus/lessons/round-69.md:25-31`: "S269 is not superseded: … a superseding row would duplicate the
  same URL and scope while carrying no new claim — the label is a miscount, not a claim drift (QUALITY
  #93 exists to stop claim drift)."
- `corpus/lessons/round-69.md:41` (M69-3): "recorded reason above (no superseding row) …".
- `corpus/knowledge/2026-11-03-r68-packed-elf-route.md:99-101`: the reason lives in that Gate.
- `corpus/SOURCES.md:186` still reads `(11 words)`.

Evidence bearing on that reason (the choice is the L1's; both exact texts are supplied):

1. "would duplicate the same URL" — refuted by this registry's own corrections: S054 supersedes S052
   with a byte-identical source cell; S062 supersedes S058 on the same locator; S033 supersedes S032 on
   the same PR URL (`evidence/supersede-precedent.txt`). The census's 19 standing W04 duplicate-URL
   warnings were accepted at round 68's close (`corpus/lessons/round-68-verifier-spotcheck.md` §3).
2. "carrying no new claim" — the row carries the corrected count and the counting rule; `QUALITY.md`
   #93 is titled "a routed registry defect closes **only** by a new `supersedes` row" and enumerates
   "wrong anchor", which a wrong word-count label in the `anchor` cell is. `CORPUS.md` `### Rules` 2
   states the same mechanism without an alternative.

Counterweight: `CORPUS.md` `### Rules` 4 ("no row quota … a short registry … beats a long one") and the
closure's own recorded-reason option support the shipped branch. Stated so the case is not one-sided.

`used-by` dependency: S271 names
`corpus/knowledge/2026-11-03-r68-packed-elf-route.md, corpus/lessons/round-69.md`. The entry is named
because this seat's V1 block cites S271; the landed entry does not. If S271 is landed while the entry
keeps "not superseded", either append a correction to the entry or drop the entry from cell 11.

## 5. Out-of-scope observations (no draft, no action by this seat)

- `corpus/README.md` pre-existing malformed blocks (90-111, 113, 115, 244-273) — see §3.
- The corpus freshness sweep at `/home/vgpnk/Projects/shokunin/CORPUS.md:170` cannot match the
  #101/#112 backticked list-item shape. Both the landed entry block and the round-53 precedent use the
  backticked form, so this is a corpus-wide regex/shape tension, not a round-69 defect. Do not
  "fix" it by de-backticking a correct field.
- The S270 row was rewritten during the wave (from the `doc/upx.1` manual page to the packer source
  `src/help.cpp` + `src/main.cpp`); at HEAD it matches `corpus/lessons/round-69.md:19` (Gate ADMIT) on
  source, kind and quotes. Observed and consistent; no finding stands.
- `tools/round-69/provenance-check.py` is registered as a round-69 gate but is not in
  `tools/round-69/` frozen instrument pins (`claims.json` lists four instruments); it is called a
  "corroboration gate (not a frozen claim counter)" in its own docstring, so no QUALITY #92 finding is
  claimed here — recorded as an observation only.

## 6. Unrun / unknown / risks

- **Unrun:** the corpus census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  kaidoku`), the round-29 freeze/prefile gates, and every lane instrument. The L1 owns them. S271 was
  checked directly (11 cells, no inner pipes, `supersedes` prefix), not by the census.
- **Unknown:** whether the L1 flips V5 to the supersede row, or keeps the recorded reason. The two
  branches are mutually exclusive: landing S271 while `round-69.md:25-31` and the entry's 99-101 stand
  would leave the corpus self-contradictory.
- **Risk:** R68-V2 as committed fails the routed outcome. The one-line fix is content-addressed; if the
  header row moves again, match `| entry | topic | source | verified-at |` and the delimiter line
  directly below it, not the literal line number.
- Tool installs/upgrades: **none**. `markdown-it-py` 4.2.0 was already present at
  `/usr/lib/python3.14/site-packages`; no `pacman` transaction was attempted (host-wide pause); no PATH
  directory was written.
