# ScoutSource — r71/w1 report (sourced rows S273/S274, round-71 search log)

Full quote tables, grep sweep, fetch receipt and snapshots: `.ufo/waves/round-71/w1/ScoutSource/`
(`sources.md`, `gfm-4.10.html`, `py-tempfile.html`, `fetch-receipt.txt`). This page is what the L1
needs to integrate; the annex is the evidence.

## Fetch evidence (2026-11-04)

| URL | status | bytes | sha256 | Last-Modified |
|---|---|---|---|---|
| https://github.github.com/gfm/ | 200 | 508 310 | `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220` | 2022-09-07 |
| https://docs.python.org/3/library/tempfile.html | 200 | 75 198 | `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560` | 2026-11-04 03:29Z |

Both digests are byte-identical to snapshots already taken by other seats (GFM: S258's 2026-11-01
snapshot; tempfile: the round-70 seat snapshot). Two dates, two seats, same bytes.

## S273 — new row warranted; `pinned-empty` clause is an overclaim

Located, section 4.10 Tables (extension), anchor `#tables-extension-`, snapshot lines 4696–4698:

- tolerance (13 words): "The remainder of the table’s rows may vary in the number of cells."
- FEWER (21 words): "If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted."
- MORE (8 words): "If there are greater, the excess is ignored:"
- contrast, lines 4677–4678 (21 words): "The header row must match the delimiter row in the number of cells. If not, a table will not be recognized:"

**Scope decision: NEW row, not an S258 extension.** S258's quote is line 4575, the escaped-pipe
rule (`\|` is cell content) — an *overcount* failure. The tolerance rule is a different sentence
with the opposite failure mode: a short row is valid and gets **end-padded with empty cells**, so no
conformant Markdown parser complains. Same document and digest is fine (S260/S272 already share one).

**Does it ground a 6-cell row as a defect? No — it grounds the opposite.** The only fatal count
mismatch in GFM is header-vs-delimiter. A 6-cell body row under a 7-cell header is well-formed and
reads as 7 cells with the last (owner) empty.

Measured at `b827a8b5` (read-only `git show`, own splitter, instrument not run): registry block = 88
data rows, histogram `{6:6, 7:79, 8:4}`; the six 6-cell rows are the round-70 instruments.
Grammar v2 without padding → 6 nonconformant, all `pinned-empty`. With GFM end-padding first → 0
nonconformant. **The padding reading is the false green**; probe for the mutation seats: mutate
`parse()` to pad short rows to header width, base state goes 6 → 0.

Repair suggested for the landed S273 row (I did not edit it):
- scope clause "grounds … the `pinned-empty` classification of the six round-70 rows" →
  "grounds grammar v2's decision to index positionally instead of padding — which is what makes the
  six 6-cell round-70 rows fail as `pinned-empty` — and records that a GFM-faithful padding reader
  reads those rows as an empty owner cell and passes them (false green)".
- anchor "paragraph after the example rows" → "`#tables-extension-`, between Examples 203 and 204,
  lines 4696-4698"; add the 21-word FEWER quote (Q1+Q2 = 34 words exceeds the 25-word cap; Q2 alone
  or Q1+Q3 at 21 fits).
- recheck 90d → 365d (edition frozen 2022-09-07; S258 is `on-release`).
- Note for whoever reviews R71-C3: for a 6-cell row grammar v2 reports `write_scope` = the row's
  pinned path and `owner` = its write scope (positional shift). Detection is unaffected; the finding
  code and the two reported fields misname the omission.

## S274 — keep REJECTED, but the reason must be corrected

The landed reason "the page's `mkdtemp` promise is only an absolute pathname" is false. The page
states (lines 478–480): "Creates a temporary directory in the most secure manner possible. There are
no race conditions in the directory’s creation." and "The directory is readable, writable, and
searchable only by the creating user ID." — plus cleanup responsibility and the absolute pathname.

What it does **not** state is any name property. Only name text is the module intro (lines 228–230):
"Files names used by this module include a string of random characters which allows those files to
be securely created in shared temporary directories." — random, with no uniqueness statement, no
collision bound, and no retry-on-existing-name loop for `mkdtemp` (the `O_EXCL` clause lives in the
`mkstemp` paragraph, line 431). Grep over the snapshot: `unique` 0, `uniqueness` 0, `distinct` 0,
`distinctness` 0, `collision` 0, `collide` 0, `atomic` 0, `atomically` 0; `random` 1.

Corrected reason: *the page grounds race-free creation, caller-only permissions and path shape, not
names; `random characters` carries no uniqueness or collision guarantee.* Corrected flip: *an
official page or CPython docstring/source statement naming uniqueness, collision-freedom, or the
retry-on-existing-name loop for `mkdtemp`* — "a consumer needing mode/ownership/absolute-path
properties" is a different claim and does not flip this one.

Citation fix: `snapshot bytes 49106-49180` cuts mid-tag at both ends; the quote is not contiguous in
the HTML (`mkdtemp()` is wrapped in `<span class="pre">`), so cite the `<p>` element — bytes
**49032–49191**, line 485. The landed row's `unique|distinct|collision|atomic → 0 hits` claim is
true and should be kept.

## Round-71 search-log entry

One already sits at the top of `## Search log` (added this round, not present at `b827a8b5`). Do not
add a second — replace its exclusion clause, which repeats the "only an absolute pathname" error:

> "- 2026-11-04 round 71 — Question: which primary text grounds reading a registry row whose cell count differs from the header's, and does the Python `tempfile` page ground `mkdtemp` distinctness? Where searched: the GFM spec 4.10 Tables (one live fetch; snapshot sha256 `b153d814…`, byte-identical to S258's 2026-11-01 snapshot) and the Python 3 `tempfile` page (one live fetch; sha256 `edf72176…`, byte-identical to the round-70 seat snapshot). Identified 2, screened 2, included 1 (S273: body-row cell-count tolerance, lines 4696-4698, distinct from S258's escaped-pipe rule at line 4575), excluded 1 (S274: the page grounds race-free creation, caller-only permissions and an absolute pathname, but says only 'a string of random characters' about names, with `unique|distinctness|collision|atomic` at 0 hits, so it grounds no uniqueness/collision-freedom claim; registered rejected with its flip). Re-opened S258 for the scope comparison without adding a row. Stop: one located quote per row and two byte-identical digests across seats; no web-wide negative is claimed."

**Peer confirmation (executed, not mine).** ReviewerGates-4 ran the frozen instrument at base and
reports six `pinned-empty` findings with exit 1 (`.ufo/waves/round-71/w1/ReviewerGates/census-base.json`),
matching my read-only simulation. **Their gate verdict is `not-met`** — the base-state agreement is
one clause, not a pass. Their separate kill-rule failure — a malformed 8-cell row accepted
with rc 0 — is consistent with the same no-pad design: `pinned = "|".join(cells[4:-2])` legally
absorbs any number of middle cells, so only a missing tail is caught. Their fixture, their finding.

## Tooling / scratch

No installs or upgrades (nothing needed); no pacman, no PATH directory touched. Scratch root
`/fast/scratch/hyaku/kaidoku-r71/ScoutSource/` removed after copying the two snapshots and the
receipt into the annex. Only read-only git (`git show`, `git diff`) against the lane repo; no clone,
fixture or work tree, therefore no mutation guard needed. No `/tmp` path is cited.

VERDICT: met — S273 is warranted (GFM 4.10 lines 4696-4698, 13+21-word quotes, distinct from S258's escaped-pipe line 4575) but grounds tolerance/end-padding, not a 6-cell defect, and both landed rows need repair: S273's `pinned-empty` clause overclaims (measured: base 6 nonconformant, GFM-padding mutant 0 = false green) and S274 rejects on a false reason ("only an absolute pathname") when the page does state secure/race-free creation and 0700 ownership, absent only name uniqueness.
