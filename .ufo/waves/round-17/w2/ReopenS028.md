# ReopenS028 — S028 (Go 1.27 release notes): re-open and row verification

Seat: `KaidokuR17.ReopenS028` (author-side advisory, wave 2). Read-only; leaf, no dispatch.
Lane revision verified: `git rev-parse HEAD` → `da64646adcb19c1ede7537b799b8c7d283fe43da`;
`git status --porcelain corpus/SOURCES.md corpus/lessons/round-17.md` → empty (working tree = committed).
Date 2026-10-20. Axes: **calibration** (registry fields vs CORPUS.md contract, quote fidelity) and
**depth** (what the page does and does not ground). No REA analyze/search/decompile, no Ghidra,
no carrier execution, no installs.

## Verdict

**Rejection confirmed** on a fresh live fetch: today's `https://go.dev/doc/go1.27` hashes to the
row's snapshot (`a4c56ba5…`) and is `cmp`-identical to the retained w1 snapshot; it contains
**zero** case-insensitive `dwarf` matches and **zero** `nodwarf5`. The Gate quote is exact
contiguous rendered text, 9 words, in the named section. The row's *substance* survives; four
**metadata** defects remain: tier, the flip's scope, one unquoted `teaches` claim, and the missing
command for the negative claim.

## Observed — verbatim

### Fetch and identity

```
curl -sS -D /tmp/s028.headers -o /tmp/s028.html --compressed https://go.dev/doc/go1.27
sha256sum /tmp/s028.html
a4c56ba584ac26614537ac40bf07aa638314decdacf32ea96acb60dbfe57393e  /tmp/s028.html
wc -c /tmp/s028.html  -> 65794
headers: HTTP/2 200 ; content-type: text/html; charset=utf-8 ; content-encoding: gzip ;
         content-length: 19060 ; date: Tue, 20 Oct 2026 14:08:55 GMT
title: Go 1.27 Release Notes - The Go Programming Language ; h1: Go 1.27 Release Notes
canonical: https://go.dev/doc/go1.27
```
`curl -sS -o /tmp/s028.plain https://go.dev/doc/go1.27` (no `Accept-Encoding`) → **same** sha256,
`cmp` identical. `https://go.dev/doc/go1.27?m=text` → **same** sha256, 65,794 B. The pin is
transport-independent; `65,794 B` is the decompressed size.

### Zero-match sweep (row anchor claim)

```
case-insensitive 'dwarf' raw count:        0
case-insensitive 'dwarf' text-only count:  0
nodwarf5 raw occurrences:                  0
nosizespecializedmalloc raw occurrences:   1
nojsonv2 raw occurrences:                  1
GOEXPERIMENT raw occurrences:              6
```
Shell reproduction: `curl -sS --compressed https://go.dev/doc/go1.27 | grep -ic dwarf` → `0`
(exit 1); the same pipe with `grep -c 'nodwarf5'` → `0` (exit 1).

### Quote in `corpus/lessons/round-17.md:50` (committed)

Cell: `| S028 | https://go.dev/doc/go1.27, "Faster memory allocation" | You may set GOEXPERIMENT=nosizespecializedmalloc at build time to disable |`

Snapshot lines 584–585, verbatim:

```
You may set <code>GOEXPERIMENT=nosizespecializedmalloc</code> at build time to disable
it.
```

Rendered sentence: `You may set GOEXPERIMENT=nosizespecializedmalloc at build time to disable it.
This opt-out setting is expected to be removed in Go 1.28.`
Check: `quote in normalized text: True`; `words in quote: 9`; `nosizespecializedmalloc` occurs once
on the page. Section boundary: `<h3 id="faster-memory-allocation">Faster memory allocation</h3>`
at 28,463 < quote at 29,038 < next `<h3 id="goroutineleak-profiles">` at 29,165; parent `<h2>Runtime`.
The quote is a contiguous prefix ending at the line break before `it.`; not spliced.

### Draft line anchors cross-check ([OBS] direct byte comparison)

`.ufo/waves/round-17/w1/draft-sources-rows.md:39-40` cites snapshot lines 584 and 684–685. That
snapshot still exists at `/tmp/kr17-ghidra/go-1.27.html` and is **byte-identical** to today's fetch:

```
sha256sum /tmp/kr17-ghidra/go-1.27.html /tmp/s028.html
a4c56ba584ac26614537ac40bf07aa638314decdacf32ea96acb60dbfe57393e  /tmp/kr17-ghidra/go-1.27.html
a4c56ba584ac26614537ac40bf07aa638314decdacf32ea96acb60dbfe57393e  /tmp/s028.html
cmp -s /tmp/kr17-ghidra/go-1.27.html /tmp/s028.html  -> IDENTICAL ; both 65794 B
```

Reading that file: `dwarf` (case-insensitive) `0`, `nodwarf5` `0`; and the lines are exactly the
two draft quotes:
`584 You may set <code>GOEXPERIMENT=nosizespecializedmalloc</code> at build time to disable`,
`610 <p>The <code>goroutineleakprofile</code> <code>GOEXPERIMENT</code> setting is now deleted.</p>`,
`684 may disable it by setting <code>GOEXPERIMENT=nojsonv2</code> at build time,`,
`685 restoring the original v1 implementation.`
So the row's hash pins the same bytes the draft author read; the opening is corroborated, not
merely reproducible. `stat` shows the snapshot mtime `2026-10-20 10:33:27 -0300`, under three
minutes before the draft file `draft-sources-rows.md` (`10:36:23 -0300`); that ordering makes it
the author's own fetch ([INF] on authorship, [OBS] on bytes and times).

### The comparator that matters (depth, and the trigger for F2)

`https://go.dev/doc/go1.25#dwarf5-support` fetched today, `<h3 id="dwarf5-support">DWARF5 support</h3>`:

> `DWARF 5 generation can be disabled by setting the environment variable GOEXPERIMENT=nodwarf5 at build time (this fallback may be removed in a future Go release).`

That page has 5 case-insensitive `dwarf` matches. This is the page a w1 seat already opened
(`.ufo/waves/round-17/w1/ScoutGoExperimentSuffix.md:106`). The 1.27 page still has none, so the
rejection of **S028** is right; the flip wording is not.

## Findings

### F1 — tier `C` is wrong for this scope; contract says A (severity: **medium**)

- Target: `corpus/SOURCES.md:34` (committed at `da64646`), tier cell = `C`.
- Contract: `CORPUS.md:93-96` — tier is scoped to `scope`; **A** = "primary or authoritative for
  that scope (spec, **official docs**, source code, original paper, maintainer statement, the lane's
  own re-runnable gate output)"; **C** = "lead only — never sole support for an admitted entry."
- The row's `scope` is "Whether the 1.27 release notes document the `nodwarf5` experiment token":
  for its own contents an official go.dev release-notes page is authoritative → A. The row is also
  the sole support for the lesson's rejection of the release-notes hypothesis
  (`corpus/lessons/round-17.md:29`), so C's "never sole support" ceiling is in tension with how the
  round actually uses it.
- Corroboration that `C` is an integration transcription slip, not a considered tier: the w1 draft
  row has **A** — `.ufo/waves/round-17/w1/draft-sources-rows.md:21`
  `| S028 | Go 1.27 Release Notes — https://go.dev/doc/go1.27 | docs | A | …`; and every other Go
  row this round is A except the GitHub tracker thread `S027` (B): `S024 A`, `S025 A`, `S026 A`,
  `S027 B`, `S029 A`, `S030 A`. The only other C row is the community blog `S022`
  (`kind=community`).
- `CORPUS.md` has no "rejected ⇒ C" rule; `status` is the separate field for the verdict
  (`:103-104`). The census does not gate it either (`w2/census.txt`: `A=26 B=2 C=2`, no enum
  violation), so this survives all mechanical checks.
- Smallest fix: change the tier cell at `corpus/SOURCES.md:34` from `C` to `A`. (If L1 deliberately
  wants "rejected ⇒ C", that is a new policy that must be written into `CORPUS.md` first; it cannot
  be inferred from the current definition.)

### F2 — flip condition is already satisfied before it was written (severity: **medium**)

- Target: `corpus/SOURCES.md:34` teaches cell, flip clause:
  `flip: a release note or doc page that defines the DWARF 5 experiment opt-out.`
- Counterexample (live, today): `https://go.dev/doc/go1.25#dwarf5-support` — a release note that
  defines the opt-out verbatim ("`GOEXPERIMENT=nodwarf5` at build time"). It predates the row
  (Go 1.25) and was already quoted inside this same wave by
  `.ufo/waves/round-17/w1/ScoutGoExperimentSuffix.md:106`.
- Consequence: a flip that is true at authoring time cannot "change the verdict" about the **1.27**
  page; a recheck under `on-release` would find the condition true and still leave the 1.27 notes
  unchanged. The defect is scope, not the rejection: the row rejects the 1.27 page, but its flip
  names any page.
- Smallest fix: scope the flip at `corpus/SOURCES.md:34` to the page under test, e.g.
  `flip: the Go 1.27 release notes (or a 1.27-era release note for this page) define the DWARF 5
  experiment opt-out.`
- Depth note (L1 decision, not a defect): `teaches` says "S026 source does" ground the token. That is
  true for the `X:` suffix mechanics; but the **name** `nodwarf5` is publicly documented prose in
  the Go 1.25 notes, so "S026 source grounds the token instead" understates available public
  documentation for readers without the source tree. If the round wants a public-prose ground, that
  page is already opened and quoted by w1 and could be cited in the lesson; no new row is required
  by this seat.

### F3 — `teaches` asserts the `nojsonv2` opt-out, but the Gate carries no quote for it (severity: **low**)

- Target: `corpus/SOURCES.md:34` teaches (`…document nosizespecializedmalloc and nojsonv2 opt-outs…`)
  vs `corpus/lessons/round-17.md:50` (a single S028 quote, about `nosizespecializedmalloc`).
- The w1 draft supplied the missing quote and it verifies exactly:
  `.ufo/waves/round-17/w1/draft-sources-rows.md:40`
  `may disable it by setting GOEXPERIMENT=nojsonv2 at build time,`
  → snapshot 684–685; `contiguous: True`; `words: 9`; section `<h3 id="New encoding/json/v2 and
  encoding/json/jsontext packages">` under `<h2>Standard library</h2>` (offset 32,600 < 35,267).
- Not a false claim (it is true and the page was opened); it is a coverage inconsistency: the row's
  `teaches` makes two positive claims and only one is quoted, while S024/S025/S026/S027/S029 each
  carry two quotes.
- Smallest fix: add one Gate row at `corpus/lessons/round-17.md` after line 50:
  `| S028 | https://go.dev/doc/go1.27, "New encoding/json/v2 and encoding/json/jsontext packages" | may disable it by setting GOEXPERIMENT=nojsonv2 at build time, |`

### F4 — negative claim lacks the search command (severity: **low**)

- Target: `corpus/SOURCES.md:34` anchor: `… case-insensitive `dwarf` search: zero matches`.
- Contract: `CORPUS.md:39-41` — "**A negative claim carries its sweep.** … need the search command
  that produced the absence, or the claim is unverifiable." The cell gives the term, the case rule
  and the snapshot hash, but not the command and not the byte scope.
- The claim itself verifies (see above), so the harm is reproducibility, not truth. It is also
  worth noting `nodwarf5` ⊂ `dwarf`, so the single sweep does cover the scope token.
- Smallest fix: append to the anchor
  ``(`curl -sS --compressed https://go.dev/doc/go1.27 | grep -ic dwarf` → `0`; 65,794 B)``.

## Field-by-field check of `corpus/SOURCES.md:34` (committed `da64646`)

| Field | Artifact | Verdict |
|---|---|---|
| id | `S028` | OK; next-unused sequence intact (30 rows, no duplicate) |
| source | title + canonical URL, resolves HTTP/2 200 | OK |
| kind | `docs` | OK (`CORPUS.md:92`) |
| tier | `C` | **F1** |
| scope | 1.27 notes vs `nodwarf5` | OK for the rejection, but narrower than `teaches`' positive claims (see F1) |
| anchor | page-fetched date + sha256 + sweep | Hash reproduces exactly; sweep lacks command (**F4**); page-level anchor is allowed by `CORPUS.md:99` |
| teaches | `REJECTED: …; flip: …` form | Form OK; flip already true (**F2**); `nojsonv2` unquoted (**F3**) |
| status | `rejected` | OK; matches S022 precedent (rejected row cited by a lesson). Literal `CORPUS.md:103` calls "cited by ≥1 path in used-by" `mined`, so the two definitions overlap; corpus-wide ambiguity, no action proposed |
| opened | `2026-10-20` | OK — matches Gate access date and my re-open date |
| recheck | `on-release` | OK — Go docs convention |
| used-by | `corpus/lessons/round-17.md` | OK — file exists and cites S028 at `:29` and `:50` |

## Bounded no-findings (checked, clean)

- **Quote** `round-17.md:50`: exact contiguous rendered text, 9 words (≤25), unique occurrence,
  correct `h3` (`Faster memory allocation`, id `faster-memory-allocation`, parent `Runtime`), no
  splice or relocated locator (`QUALITY #17` manual-HTML rule respected).
- **Zero `dwarf` / zero `nodwarf5`** in raw HTML and in tag-stripped text; also zero in the
  `?m=text` variant (identical bytes).
- **Hash reproducibility**: `--compressed`, no-compression, and `?m=text` all give
  `a4c56ba584ac26614537ac40bf07aa638314decdacf32ea96acb60dbfe57393e` (65,794 B).
- **Row structure**: `NF=13`, no `|` inside cells, enum-valid kind/status; census at
  `w2/census.txt` reports `0` malformed rows and `0` enum violations.
- **Positive `teaches` claims** verified on the page: `nosizespecializedmalloc` ("…to disable it.
  This opt-out setting is expected to be removed in Go 1.28.") and `nojsonv2` ("…may disable it by
  setting GOEXPERIMENT=nojsonv2 at build time, restoring the original v1 implementation.").
- **Status/used-by combination** matches `S022` (rejected, cited by `round-13.md`); no census gate.

## Not checked / limits

- `S026` source and the carriers' build strings are outside this seat; I did not re-verify the
  "S026 source does" parenthetical.
- The w1 snapshot `/tmp/kr17-ghidra/go-1.27.html` survives and `cmp`-matches today's fetch
  (65,794 B, same sha256); it is outside the repo and unversioned, so the row's hash remains the
  durable pin if `/tmp` is cleared.
- Other go.dev pages were not swept; the 1.25 page was opened only to test the flip (F2).
- The page is live; the sha256 is the pin. I re-opened today, not at the author's fetch instant.
- No installs or upgrades were needed; none performed.

Confidence: high on the zero-match sweep, quote fidelity and hash (direct observation); high on F2
(live page + exact quote); medium-high on F1 (contract reading plus draft/precedent evidence);
high on F3/F4 (direct observation of the draft quote and the contract rule).
