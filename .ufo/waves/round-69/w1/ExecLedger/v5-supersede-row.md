# R68-V5 — the S269 quote is 10 words, not 11

## Live state: the landing commit `5ee94c56` shipped the OTHER branch

Four statements now exist in the landing commit `5ee94c56` (all worktree bytes identical), and they are
consistent with each other but not with this draft's row:

- `corpus/lessons/round-69.md:25-31` (Gate): "S269 is not superseded: the quote is 10 words and ≤25
  either way, its location, bytes and sha256 re-derive, and a superseding row would duplicate the same
  URL and scope while carrying no new claim — the label is a miscount, not a claim drift (QUALITY #93
  exists to stop claim drift)."
- `corpus/lessons/round-69.md:41` (M69-3 fix): "recorded reason above (no superseding row) + the count
  is computed before a row is written".
- `corpus/knowledge/2026-11-03-r68-packed-elf-route.md:99-101`: "Label correction: … The reason the row
  is not superseded is recorded in `corpus/lessons/round-69.md` `## Gate`."
- `corpus/SOURCES.md:186` still reads `(11 words)`.

That is the second option the round-68 closure's routing offered ("a new row … **or** a recorded reason
to leave the label"). This draft's row is the first option, ordered by the seat ticket. **The two are
mutually exclusive**: landing S271 while those four statements stand would leave the corpus
self-contradictory (the entry asserting "not superseded" beside an existing S271). The L1 must pick
one; both exact texts are below / above.

### Weighing the recorded reason's two grounds (evidence, not verdict)

1. *"would duplicate the same URL"* — shipped precedent in this same registry contradicts it:
   S054 supersedes S052 with a **byte-identical source cell**, S062 supersedes S058 on the **same
   locator** (different description, same URL), and S033 supersedes S032 on the same PR URL
   (`evidence/supersede-precedent.txt`). A duplicate URL is the
   normal shape of a correction row, and the census already carries standing W04 duplicate-URL warnings
   (19 at round 68's close, per `corpus/lessons/round-68-verifier-spotcheck.md` §3).
2. *"carrying no new claim"* — the row carries the corrected count and the counting rule; `QUALITY.md`
   #93 is titled "a routed registry defect closes **only** by a new `supersedes` row" and its body
   enumerates "wrong anchor", which is what a wrong word-count label in the `anchor` cell is.
   `CORPUS.md` §"SOURCES registry" `### Rules` 2 states the same mechanism without an alternative.

Counterweight, stated so the L1 is not handed a one-sided case: `CORPUS.md` `### Rules` 4 says there is
no row quota and a short honest registry beats a long one, and the closure itself wrote the
recorded-reason option. So the landed branch is the routing's option 2 even though it is not #93's
option. If the L1 keeps it, the reason should rest on the routing's allowance and on rule 4, not on
duplicate-URL, which the precedent refutes.

If the L1 instead lands S271, three appended corrections are needed: the entry's lines 99-101 ("not
superseded"), the Gate paragraph at `round-69.md:25-31`, and M69-3's fix cell. Those are the L1's to
write; this seat does not edit them.


Target row: `corpus/SOURCES.md:186` (`S269`). At the dispatch commit `3f3d20fc` the file hashed
`abb44aa4fc3d7f194de2b384bbc2d969d8a2328e0c467cf1cf56e9008092c0e0` (176 rows, S269 last); at HEAD
`5ee94c56` it hashes `f0420431eb8a85877e66c5eb431619abe1645178fb0ec25f257e916214fd561d` (177 rows, S270 at
line 187, kind `code`, the packer source).

## The measurement

The row's `anchor` cell says of the quote `(11 words)`; the round-68 Gate rows say `(11 words)`
(`corpus/lessons/round-68.md:20`) and `the same 11-word sentence` (`:24`).

```
$ printf '%s' 'Packed programs will be byte-identical to the original after uncompression' | wc -w
10
$ printf '%s' 'Packed programs will be byte-identical to the original after uncompression.' | wc -w
10
$ printf '%s' 'Packed programs will be byte-identical to the original after uncompression' | tr '-' ' ' | wc -w
11
```

Re-derivation against the pinned bytes (`evidence/word-count.txt`): `curl -fsSL
https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt` → HTTP 200, 37 208 B, sha256
`4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` (equal to S269's pin); heading
`NOTES FOR LINUX/ELF386` at fetched-bytes line 433, next `NOTES FOR` heading at 475, quote composed
from lines 441-442 = `Packed programs will be byte-identical to the original after uncompression.`
— **10 whitespace words**; one occurrence of `byte-identical` in lines 433-474.

**Reason the label read 11:** `wc -w` splits on whitespace only, so the hyphenated `byte-identical`
is one word; splitting the hyphen into two words gives exactly 11. The label applied word-splitting
to a hyphen, not a second reading of the text.

## Exact new row (S271) — append only, never rewrite S269

Insert immediately after line 187 (the S270 row), before the blank line at 188 and `## Paths` at 189.
`S271` is the next free id at the measured revision: the live registry ends `S267, S268, S269, S270`
and `grep -c '^| S271 '` is 0. If another row is appended at S271 first, renumber only cell 1 to the
next free id; every other cell is invariant.

```
| S271 | UPX 5.2.0 documentation, `doc/upx-doc.txt` at tag `v5.2.0`, corrected quote-word count — https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt | docs | A | The same passage and locator S269 carries, with the corrected whitespace-word count and the counting rule; no change of scope, authority or quote — not a second passage, not a new locator | `v5.2.0`; re-fetched 2026-11-03 for this correction, HTTP 200, 37 208 bytes, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` equal to S269's pin; quote at fetched-bytes lines 441-442 under `NOTES FOR LINUX/ELF386` (heading line 433): "Packed programs will be byte-identical to the original after uncompression" — 10 whitespace-separated words, not 11; one occurrence in that section | supersedes S269 — the quote is 10 words, not 11: `wc -w` on the composed quote prints `10`, while splitting the hyphenated `byte-identical` into two words yields 11, which is the label's arithmetic. The locator, the sha256, the 25-word bound and S269's admission are unchanged (round-68 closure R68-V5) | mined | 2026-11-03 | 180d | corpus/knowledge/2026-11-03-r68-packed-elf-route.md, corpus/lessons/round-69.md |
```

Format checks (`evidence/row-s271.txt`): 11 cells, matching S269 and S270; `teaches` opens exactly
`supersedes S269 — `; no raw `|` inside any cell; status `mined` is consistent with the two `used-by`
paths, one of which is the entry whose R68-V1 correction block cites S271 (`v1-correction-block.md`)
and the other the round-69 lesson line below.

`used-by` dependency: `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` is listed because the V1
block's closing sentence cites S271. If the L1 lands V5 without the V1 block, drop that path from
cell 11 and keep `corpus/lessons/round-69.md` only.

## S269 stays byte-identical

`CORPUS.md` §"SOURCES registry" `### Rules` 2: only `status`, `recheck` and `used-by` may change in
place, and a correction is a new row whose `teaches` opens `supersedes S0NN —`. No in-place change is
needed here: S269 keeps `status mined`, `recheck 180d`, and its `used-by` already names the round-68
entry. If the L1 nevertheless extends S269's `used-by`, log old → new in the round-69 lesson.

## Lesson note (exact) — `corpus/lessons/round-68.md`, append at end

The two false labels are in that lesson's Gate rows (a) and (e). Append after the last line
(`## Census` block ends the file):

~~~markdown
## Correction appended — round 69: the S269 quote is 10 words, not 11 (R68-V5)

The Gate rows above write the S269 quote's length as "(11 words)" (row (a)) and "the same 11-word
sentence" (row (e)). Both labels are wrong; the sentence is **10** whitespace-separated words.

- Command: `printf '%s' 'Packed programs will be byte-identical to the original after uncompression'
  | wc -w` prints `10`; with the sentence's trailing period it is still `10`.
- Source bytes: re-fetched `https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt` on
  2026-11-03 — HTTP 200, 37 208 B, sha256
  `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` (equal to S269's pin); the
  composed quote at fetched-bytes lines 441-442 is `Packed programs will be byte-identical to the
  original after uncompression.` — 10 words.
- Why 11 appeared: `wc -w` splits on whitespace only; splitting the hyphenated `byte-identical` into
  two words gives 11. That is arithmetic on the same text, not a second reading.
- What is unchanged: the quote is contiguous, its location (heading line 433, quote at 441-442, one
  occurrence in that section), the sha256, the 25-word bound (QUALITY #16/#17) and the admission of
  S269. Only the label was wrong (round-68 closure §5, defect R68-V5).
- Correction of record: `corpus/SOURCES.md` S271, whose `teaches` opens `supersedes S269 — `
  (CORPUS.md §"SOURCES registry" `### Rules` 2; QUALITY #93). S269 stays byte-identical; the filed
  lines above are not rewritten.
~~~

## Round-69 lesson line (exact) — for `corpus/lessons/round-69.md` §"Corrections to round 68"

Land this bullet if ScribeLesson's draft does not already carry R68-V5; it is the closure record the
round's own lesson needs, and it is the second `used-by` path above.

~~~markdown
- **R68-V5 — closed.** `corpus/SOURCES.md` S271 (`teaches` opens `supersedes S269 — `) records the
  corrected count: the S269 quote is 10 whitespace words, not 11 (`printf '%s' 'Packed programs will
  be byte-identical to the original after uncompression' | wc -w` → `10`); locator lines 441-442,
  sha256 `4dc547ed…` and the admission are unchanged. The S269 row and the round-68 Gate labels stay
  as filed (append-only).
~~~

## Unrun

The corpus census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`)
was not run by this seat; the L1 owns that gate. The row's 11-cell shape, its absence of inner pipes
and the `supersedes` prefix were checked directly (`evidence/row-s271.txt`).
