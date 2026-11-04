# ScoutSource — r71/w1: S273 (cell-count tolerance) warrant + S274 (tempfile) rejection screen

Seat: ScoutSource (leaf). Scope: open the two sources this round's sourced rows rest on, record
fetch evidence and located quotes, decide the S258/S273 scope question, screen the tempfile page
for the rejected row the round-70 routed defect 4 asks for, and write the round-71 search-log
paragraph. I did not edit anything outside my findings dir and my scratch root; no repairs landed.

Files produced here:

| file | what |
|---|---|
| `sources.md` | this report |
| `gfm-4.10.html` | verbatim snapshot, https://github.github.com/gfm/ , 2026-11-04 |
| `py-tempfile.html` | verbatim snapshot, https://docs.python.org/3/library/tempfile.html , 2026-11-04 |
| `fetch-receipt.txt` | status / bytes / sha256 / Last-Modified / ETag / access date for both |

---

## 1. Fetch evidence (observed, 2026-11-04)

| URL | status | bytes | sha256 | Last-Modified | ETag |
|---|---|---|---|---|---|
| https://github.github.com/gfm/ | HTTP/2 200 | 508 310 | `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220` | Wed, 07 Sep 2022 14:00:06 GMT | `"6318a3e6-7c196"` |
| https://docs.python.org/3/library/tempfile.html | HTTP/2 200 | 75 198 | `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560` | Wed, 04 Nov 2026 03:29:24 GMT | `"6aeaa694-125be"` |

Access date: **2026-11-04** (first fetch 05:12:42Z, header re-check 05:14:24Z). Server banners:
`GitHub.com` and `nginx`.

Two-fetch stability (observed, not inferred):

- GFM: my 2026-11-04 sha256 is **byte-identical** to S258's committed snapshot
  (`.ufo/waves/round-58/l1/s258/`, fetched 2026-11-01). Same document, three days and two seats
  apart, unchanged; Last-Modified 2022-09-07 confirms the edition is static.
- tempfile: my 2026-11-04 sha256 is **byte-identical** to the round-70 seat snapshot
  `.ufo/waves/round-70/w1/ScoutSource/tempfile.html` (mtime 2026-11-04 01:16). The page's
  Last-Modified moved to 03:29 today (docs rebuild) but the bytes did not.

---

## 2. GFM spec — section 4.10 Tables (extension)

In-page anchor: `#tables-extension-` (<https://github.github.com/gfm/#tables-extension->), section
heading "4.10 Tables (extension)". All line numbers below are lines of `gfm-4.10.html` in this
directory; all quotes were extracted from those lines and HTML-unescaped.

**Quote normalization (disclosed).** GFM's HTML wraps prose with a line break and two spaces after
some sentence periods. The recorded quotes collapse an internal line break / double space to one
space; characters are otherwise verbatim, including the U+2019 apostrophe in "table’s".

### 2.1 Located quotes

**Q1 — tolerance headline (13 words).** Lines 4696–4698, prose immediately before Example 204
(the example that shows `| bar |` rendering as `bar` + an empty second cell):

> The remainder of the table’s rows may vary in the number of cells.

**Q2 — FEWER cells than the header (21 words).** Same lines, next sentence:

> If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted.

**Q3 — MORE cells than the header (8 words).** Same lines:

> If there are greater, the excess is ignored:

Q1+Q2 is 34 words, over the 25-word cap; Q1+Q3 is 21 words and fits, but Q3 alone does not carry
the padding rule. Q2 alone (21 words) is the strongest single quote for the "fewer" case.

**Q4 — contrast: header vs delimiter (21 words).** Lines 4677–4678, prose immediately before
Example 203 (the example whose output is a paragraph, i.e. no table):

> The header row must match the delimiter row in the number of cells. If not, a table will not be recognized:

**Q5 — S258's quote, relocated in the same snapshot for comparison (15 words).** Line 4575, prose
before Example 200:

> Include a pipe in a cell’s content by escaping it, including inside other inline spans:

### 2.2 S258 vs S273 — new row warranted

S258's scope is the **escaped-pipe writer/reader conflict**: a pipe inside a cell must be written
`\|` and is parsed as cell content, so a split on the plain pipe overcounts cells (the mined
M58-2 conflict). Its quote is Q5.

The rule this round needs is a different sentence with a different consequence: **body-row cell
counts are tolerated**. Q1 says variation is allowed; Q2/Q3 say what happens to the surplus/deficit
(end-padding with empty cells, or dropping the excess); Q4 says the only count mismatch that kills
the table is header-vs-delimiter.

Distinct scope, distinct consequence, and — critically — distinct *failure mode*: under S258 an
escaped pipe makes a reader **overcount** cells (8 for 7); under Q1–Q3 a short row makes a reader
under-count and **must not** refuse the block. **A NEW row (S273) is warranted; S258 does not cover
it.** Different snapshot pins are not required — the two rows legitimately share one document and
one digest, exactly as S260/S272 already share the subprocess page across scopes.

### 2.3 Does Q2 ground reading a 6-cell row as a defect? — **No. It grounds the opposite.**

Observed from the spec: GFM gives a short body row a *defined* rendering — empty cells are inserted
**at the end** (Example 204: header `abc | def`, row `| bar |`, output `<td>bar</td><td></td>`).
The only count mismatch that makes a table unrecognized is header-vs-delimiter (Q4). So a 6-cell row
under a 7-cell header is **well-formed GFM**; a conformant Markdown parser will never complain, and
it will present the row as 7 cells with the last one empty.

Therefore a 6-cell row can only be a defect under a *lane grammar* that assigns column meaning and
requires occupancy. That is `tools/round-71/registry-census.py` grammar v2, and the mechanism is
positional, not Markdown:

- Header has 7 cells (`tool | purpose | verdict map | self-test command | pinned-value path | write scope | owner`).
- `split_cells` splits the literal line and does **not** apply GFM end-padding; `pinned = "|".join(cells[4:-2])` over 6 cells is the empty join, so a short row yields exactly `['pinned-empty']`
  (`registry-census.py:138-147`; the selftest pins it at line 233, and the 5-cell case at 237 yields
  `['cells<6','pinned-empty']`).
- Measured at the freeze revision `b827a8b5` (read-only, `git show b827a8b5:SKILL.md`, own splitter
  in scratch, no instrument run): the registry block holds **88 data rows**, cell-count histogram
  `{6: 6, 7: 79, 8: 4}`. The six 6-cell rows are the round-70 instruments
  (`tools/round-70/packed-elf.py`, `mutation-check.py`, `contract-probe.py`, `seam-probe.py`,
  `forged-receipts.py`, `controls.py`). Applying grammar v2 without padding → **6 nonconformant,
  all `pinned-empty`**; applying GFM padding to 7 cells first → **0 nonconformant**.

Reading of that measurement:

1. GFM's padding rule is the *correct column alignment*: a row that omits the owner cell should read
   as `owner = ""` with `pinned` and `write_scope` intact. The census's no-pad index rule instead
   shifts the tail: it reports `pinned-empty`, and it fills its `owner` field from the row's write
   scope and its `write_scope` field from the row's pinned path. The **finding code names the wrong
   column**; the row is still caught, because `pinned` collapses to empty either way the shift lands.
2. Because there is no owner-empty check, a reader that pads per GFM reports **zero nonconformant
   rows at base state** — i.e. the padding reading is the false green. R71-C3's base-state clause
   (six nonconformant, defects `['pinned-empty']`) is therefore exactly the behaviour that
   distinguishes the frozen parser from a plausible GFM-faithful one. Probe for the mutation seats:
   *mutate `parse()` to end-pad short rows to the header width* → base state goes 6 → 0.
3. Consequence for the row text: Q2 grounds "a short row is valid and silently empty at the tail",
   and it grounds the *necessity* of declaring a mapping. It does **not** ground calling the 6-cell
   row a Markdown defect, and it does not by itself pick the name `pinned-empty` — that name is the
   instrument's own and is misleading (see §5.1).

---

## 3. Python `tempfile` — screen for the rejected row (S274)

Section: `tempfile.mkdtemp` (in-page id `tempfile.mkdtemp`), snapshot lines 478–486; module intro
line 228–230.

**M1 — the actual promise (19 words).** Lines 478–479:

> Creates a temporary directory in the most secure manner possible. There are no race conditions in the directory’s creation.

**M2 — ownership/mode (13 words).** Line 480:

> The directory is readable, writable, and searchable only by the creating user ID.

**M3 — the only name-entropy text, in the module intro (24 words).** Lines 228–230:

> Files names used by this module include a string of random characters which allows those files to be securely created in shared temporary directories.

**M4 — the sentence the landed row quotes (9 words).** Line 485 (raw `<p>` element bytes
49032–49191):

> mkdtemp() returns the absolute pathname of the new directory.

The paragraph also states cleanup responsibility ("The user of `mkdtemp()` is responsible for
deleting the temporary directory and its contents when done with it.") and that prefix/suffix/dir
are "the same as for `mkstemp()`". `mkstemp` is the function whose paragraph carries the platform
`os.O_EXCL` clause ("assuming that the platform properly implements the `os.O_EXCL` flag",
snapshot line 431); the `mkdtemp` paragraph carries **no** such exclusivity/retry clause.

### 3.1 Grep sweep (`grep -o -i <term> py-tempfile.html | wc -l`)

| term | hits | term | hits |
|---|---|---|---|
| `unique` | 0 | `collision` | 0 |
| `uniqueness` | 0 | `collide` | 0 |
| `distinct` | 0 | `atomic` | 0 |
| `distinctness` | 0 | `atomically` | 0 |
| `O_EXCL` | 3 | `random` | 1 |
| `race condition` | 2 | `most secure` | 2 |

### 3.2 Rejection reason

The page grounds **security of creation** (race-free creation, caller-only permissions, caller-owned
cleanup) and **path shape** (absolute pathname returned). For the *name* it offers only "a string of
random characters" in the module intro — random, with no uniqueness statement, no collision bound,
and no retry-on-existing-name loop documented for `mkdtemp`. `unique`, `uniqueness`, `distinct`,
`distinctness`, `collision`, `collide`, `atomic`, `atomically` are all absent. **The page cannot
ground a distinctness / uniqueness / collision-freedom claim for concurrent runs**, so the row stays
REJECTED.

This is a *bounded negative over one snapshot*, not a web-wide negative: the claim rejected is
"this page grounds it", and one located absence is enough for that.

### 3.3 Flip condition

Admit when an official source names the property for `mkdtemp` itself: a docs sentence or CPython
docstring/source statement of name **uniqueness**, **collision-freedom**, or the **retry-on-existing-name**
loop (e.g. `_get_candidate_names` being retried on `FileExistsError`/`EEXIST`). A consumer that only
needs mode, ownership, or absolute-path properties is a **different claim** and needs its own row —
it does not flip this one.

---

## 4. Row drafts

Eleven cells, matching the registry header at `corpus/SOURCES.md:5`. Neither draft contains a raw
`|` in prose, so both are safe unescaped.

### 4.1 S273 — ADMIT

```text
| S273 | GitHub Flavored Markdown Spec, tables extension, body-row cell-count tolerance — https://github.github.com/gfm/ (same document and snapshot digest as S258; this is a different sentence with a different consequence) | spec | A | GFM's tolerance for body rows whose cell count differs from the header row: the header must match the delimiter row or no table is recognized, but body rows may vary — fewer cells are end-padded with empty cells and extra cells are dropped — so a short row is valid Markdown that a conformant renderer pads, and only a lane grammar that assigns column meaning can call it a defect | `#tables-extension-`, prose between Examples 203 and 204, snapshot lines 4696-4698: "The remainder of the table's rows may vary in the number of cells." (13 words) and "If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted." (21 words); contrast at lines 4677-4678: "The header row must match the delimiter row in the number of cells." ; fetched 2026-11-04, HTTP 200, 508 310 bytes, snapshot sha256 `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220` (byte-identical to S258's 2026-11-01 snapshot) | A row whose cell count is short is not a Markdown syntax error but a silent end-pad; declare the column mapping and name the missing column instead of refusing the block, and know that a GFM-faithful pad hides a missing trailing column rather than reporting it | mined | 2026-11-04 | 365d | corpus/knowledge/2026-11-04-r71-registry-grammar.md |
```

(recheck 365d, not 90d: the edition is frozen since 2022-09-07 and S258 is on `on-release`; a static
spec needs no 90-day re-open.)

### 4.2 S274 — REJECTED

```text
| S274 | Python 3 `tempfile` documentation, `mkdtemp` — https://docs.python.org/3/library/tempfile.html (snapshot in `.ufo/waves/round-71/w1/ScoutSource/`) | docs | A | Whether the page grounds that `mkdtemp` returns a distinct (unique or collision-free) directory name | `#tempfile.mkdtemp`, snapshot lines 478-486: "mkdtemp() returns the absolute pathname of the new directory." (9 words); fetched 2026-11-04, HTTP 200, 75 198 bytes, snapshot sha256 `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560` (byte-identical to the round-70 seat snapshot) | REJECTED: the page grounds secure creation and ownership, not names — "There are no race conditions in the directory's creation" and "readable, writable, and searchable only by the creating user ID" (lines 478-480), plus an absolute pathname; the only name entropy is the module intro's "a string of random characters" (lines 228-230), with no uniqueness statement and no collision bound; `unique`, `uniqueness`, `distinct`, `distinctness`, `collision`, `collide`, `atomic`, `atomically` return 0 hits. Flip: an official page or CPython docstring/source statement naming name uniqueness, collision-freedom, or the retry-on-existing-name loop for `mkdtemp` — a consumer needing only mode/ownership/absolute-path properties is a different claim and does not flip this one. | rejected | 2026-11-04 | 365d | corpus/lessons/round-71.md |
```

---

## 5. Reconciliation with the rows already landed in the worktree

`corpus/SOURCES.md` in the worktree is **already 6 lines ahead of the freeze commit** (`git diff
b827a8b5 -- corpus/SOURCES.md`: S273, S274, the round-71 search-log entry, the round-70 backfill
entry). At `b827a8b5` neither row nor entry exists. I did not touch them. Against my evidence, two
cells are wrong or overclaimed and one is mis-cited; the rest is supported.

### 5.1 S273 (landed) — supported in substance, one overclaim, one weak anchor

- **Anchor cell** says "4.10 Tables, paragraph after the example rows". Accurate enough but not
  located: the paragraph sits **between Example 203 and Example 204**, snapshot lines **4696–4698**,
  in-page anchor `#tables-extension-`. The single 13-word quote carries the tolerance headline but
  not the pad/drop rule the scope cell relies on; add Q2 (21 words) or Q3 (8 words).
- **Scope cell** claims the quote grounds "the `pinned-empty` classification of the six round-70
  rows". That is the one overclaim. Q2 grounds *tolerance and end-padding*; under GFM padding the
  empty cell of those rows is the **owner**, and `pinned-empty` is produced only by grammar v2's
  deliberate non-padding positional index (§2.3). Suggested replacement clause:
  *"grounds grammar v2's decision to index positionally instead of padding, which is what makes the
  six 6-cell round-70 rows fail as `pinned-empty`; also records that a GFM-faithful padding reader
  would read those rows as an empty owner cell and pass them (false green)."*
- Nit: `cells[-2]`/`cells[-1]` for a 6-cell row report the row's pinned path as `write_scope` and its
  write scope as `owner` — the finding code and the two reported fields both misname the omission.
  Detection is unaffected (the row is nonconformant either way); the label is what to fix.
- `teaches` and `status: mined` are supported. Snapshot dir `.ufo/waves/round-71/l1/s273/` exists.

### 5.2 S274 (landed) — the rejection reason is factually wrong as written

- **"the page's `mkdtemp` promise is only an absolute pathname"** is contradicted by the page: it
  also promises "the most secure manner possible", "no race conditions in the directory's creation",
  and caller-only permissions (M1, M2, §3). The correct reason is narrower and stronger: *the page
  grounds secure creation, ownership and path shape, but says nothing about name uniqueness,
  distinctness or collision-freedom* — only "a string of random characters", with no collision bound
  (§3.2). The grep table in §3.1 is the evidence; the landed row's `unique|distinct|collision|atomic
  → 0 hits` statement is **true** and should be kept.
- **Flip condition is backwards.** "flip: a consumer needing mode, ownership or absolute-path
  properties (which the page does state)" describes widening scope to a different claim; it cannot
  falsify this one. Use §3.3: an official statement of uniqueness / collision-freedom / the retry
  loop for `mkdtemp`.
- **Byte range `49106-49180` is mid-tag on both ends.** The plain sentence is not contiguous in the
  HTML (`mkdtemp()` is wrapped in `<span class="pre">`), so the honest citation is the `<p>` element:
  **bytes 49032–49191, line 485** of the 75 198-byte snapshot (verified on my copy; identical bytes
  to the round-70 seat's).
- `used-by: —`: acceptable for a rejection, but the round-70 routed defect 4 is exactly its
  consumer; `corpus/lessons/round-71.md` is the better pointer.

### 5.3 Search-log entry (landed) — same imprecision

The landed round-71 entry says S274 was excluded because "the page states only an absolute pathname
and its `unique|distinct|collision|atomic` grep returns 0 hits". The grep half is right; the first
half repeats §5.2's error. Replacement text in §6.

---

## 6. Round-71 search-log paragraph (replacement wording)

One prose note per bounded search; append/prepend at the top of `## Search log` (newest-first). If
the landed entry at the top is kept, **replace its exclusion clause** — do not add a second round-71
entry.

> - 2026-11-04 round 71 — Question: which primary text grounds reading a registry row whose cell
>   count differs from the header's, and does the Python `tempfile` page ground `mkdtemp`
>   distinctness? Where searched: the GFM spec 4.10 Tables (one live fetch; snapshot sha256
>   `b153d814…`, byte-identical to S258's 2026-11-01 snapshot) and the Python 3 `tempfile` page (one
>   live fetch; sha256 `edf72176…`, byte-identical to the round-70 seat snapshot). Identified 2,
>   screened 2, included 1 (S273: body-row cell-count tolerance, lines 4696-4698, distinct from
>   S258's escaped-pipe rule at line 4575), excluded 1 (S274: the page grounds race-free creation,
>   caller-only permissions and an absolute pathname, but says only "a string of random characters"
>   about names, with `unique|distinctness|collision|atomic` at 0 hits, so it grounds no
>   uniqueness/collision-freedom claim; registered rejected with its flip). Re-opened S258 for the
>   scope comparison without adding a row. Stop: one located quote per row and two byte-identical
>   digests across seats; no web-wide negative is claimed.

Counts are the ones this seat observed: **identified 2, screened 2, included 1, excluded 1**, plus one
reused row (S258) that produced no new row.

---

## 7. Tooling and scratch

No install or upgrade was needed or performed; every tool used (`curl`, `sha256sum`, `grep`,
`python3`, `git show`) was already present. Nothing was written to `~/.local/bin` or any PATH
directory. Working copies lived in `/fast/scratch/hyaku/kaidoku-r71/ScoutSource/` and were removed
at the end (`rm -rf`, after copying the two snapshots and the receipt here). No `/tmp` path is cited
and none remains in anything left behind. The only git commands run were read-only (`git show`,
`git diff`) against the lane repo, all as `git -C <lane root>`; no fixture, clone, or work tree was
created, so no mutation guard was needed.

## 8. Peer confirmation and remaining unknowns

- **Base state confirmed by an executed run (peer, not me).** ReviewerGates-4 ran the frozen
  instrument at the base state and reports "six pinned-empty findings, exit 1", retained at
  `.ufo/waves/round-71/w1/ReviewerGates/census-base.json` and `review.md`. That matches my
  read-only simulation (6 nonconformant, all `pinned-empty`) and closes the earlier gap. **Their
  gate verdict is `not-met`** (kill-rule failure below): the base-state agreement is one clause, not
  a pass for R71-C3, and nothing in this source report changes their finding.
- The same reviewer names a separate kill-rule failure of their own: a malformed *eight*-cell row is
  accepted with rc 0. That is consistent with the same no-pad design — `pinned = "|".join(cells[4:-2])`
  re-joins *any* number of middle cells, so an extra middle cell is legal by construction and only a
  missing tail is caught. I did not see their fixture, so this is consistency, not proof; the
  kill-rule question is theirs, not mine.
- Not resolved here: the census's `owner` / `write_scope` misattribution for short rows is observed
  from the frozen parser, and the reviewer reports the shifted fields as "consistent with frozen
  slicing"; the exact JSON field values for the six rows are in their retained `census-base.json`.
- Whether the lane wants grammar v2 to keep the no-pad rule (my reading: it must, since padding goes
  false green) or to pad *and* add an owner-empty check — a design decision for the grammar addendum,
  not a source question.

VERDICT: met — GFM 4.10 locates the tolerance rule (13+21 word quotes, lines 4696-4698) and a NEW row S273 is warranted over S258's escaped-pipe scope, but the rule grounds tolerance (end-padding), NOT a 6-cell row being a defect, and the landed S273 row's `pinned-empty` clause plus S274's "only an absolute pathname" reason are overclaims to repair (measured: base 6 nonconformant, GFM-padding mutant 0 = false green).
