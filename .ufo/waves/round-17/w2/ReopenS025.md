# ReopenS025 — round-17 w2 falsification (source re-open, read-only)

Seat `KaidokuR17.ReopenS025` (author-side advisory; leaf, no dispatch). Access date 2026-10-20.
Target at lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`: `corpus/SOURCES.md:31` (S025) and
`corpus/lessons/round-17.md:39,45-46` (S025 Gate section and quotes), against
<https://go.dev/doc/devel/release> (`#go1.27.0`, `Release Policy`).

**Verdict: no falsifying finding.** Both committed S025 quotes are exact, contiguous page text at the
stated locations (3 and 13 words); every SOURCES.md:31 field I could decide against the page matches,
and the snapshot hash reproduces on three independent reads. I found no false text, misplaced quote,
or stale hash. One low-severity evidence-completeness note (F1) follows; it does not falsify any
claim and requires no source correction.

## Method (observed; read-only)

- `git rev-parse HEAD` -> `da64646adcb19c1ede7537b799b8c7d283fe43da`; `git diff --stat da64646 --
  corpus/SOURCES.md corpus/lessons/round-17.md` -> no output (lines read are the revision's lines).
- `curl -sS -D /tmp/s025.hdr -o /tmp/s025.html https://go.dev/doc/devel/release` -> `HTTP/2 200`,
  `date: Tue, 20 Oct 2026 14:08:56 GMT`.
- `sha256sum /tmp/s025.html` -> `d9a4b0ebb8eed5e50b092d5360d811b6dd89a21cb2518f5953bcc12f744d8968`,
  149,359 B — identical to the row's recorded snapshot hash. A second fetch with
  `curl --compressed` gave the same hash and size, and the w1 seat's scratch copy
  `/tmp/kr17-ghidra/go-release.html` (mtime 2026-10-20 10:33 local) also hashes to the same value.
- No carrier executed; no REA analyze/search/decompile; no Ghidra; no installs.

## Check results (observed)

SOURCES.md:31 fields: id `S025`; source `Go Release History — https://go.dev/doc/devel/release`;
kind `docs`; tier `A`; status `mined`; opened `2026-10-20`; recheck `on-release`; used-by
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md`.

1. **Anchor / hash.** Reproduced exactly (above). The page's `<title>` is `Release History - The Go
   Programming Language`; the row's "Go Release History" is a descriptive label, as other rows use.
2. **Anchor list.** `#go1.27.0`, `#go1.27.3`, `#go1.26.0`, and the `Release Policy` section all
   exist, once each: `<h2 id="go1.27.0">` (:474), `<p id="go1.27.3">` (:525),
   `<h2 id="go1.26.0">` (:547), `<h2 id="policy">Release Policy</h2>` (:461).
3. **Quote 1, `#go1.27.0`.** Page line 474 is
   `<h2 id="go1.27.0">go1.27.0 (released 2026-08-19)</h2>`. The heading text equals the committed
   cell `go1.27.0 (released 2026-08-19)` byte-for-byte; 3 words; the string and the id each occur
   once in the page.
4. **Quote 2, Release Policy.** Page line 464 is exactly
   `Each major Go release is supported until there are two newer major releases.` — 13 words,
   contiguous, and the first sentence of the paragraph (the next sentence begins line 465); one
   occurrence in the page.
5. **Scope / teaches.** Page 1.27 entries are `.0` 2026-08-19, `.1` 2026-09-01, `.2` 2026-10-08,
   `.3` 2026-10-19; there is no `go1.28` id. "go1.27.0 (2026-08-19) through go1.27.3 (2026-10-19)"
   is therefore the page's current 1.27 train, and 1.27.x at 2026-10-20 is time-plausible.
6. **Status / used-by.** `grep -n S025` returns `…r17-go-carrier-diagnostics.md:1` and
   `corpus/lessons/round-17.md:28,45,46`; both files exist at the revision. `mined` matches the gate
   row `round-17.md:28` ("admit (mined)"); `recheck: on-release` fits a page that gains minors at
   releases.
7. **Tier.** `grep -rniE '\btiers?\b' --include=*.md AGENTS.md SKILL.md SCORECARD.md
   corpus/README.md corpus/SOURCES.md corpus/QUALITY.md` returns only `SKILL.md:452`, the two
   `--llms` doc-tier mentions at `corpus/README.md:16,75`, the `corpus/SOURCES.md:5` header, and
   `corpus/QUALITY.md:43`, which delegates tier definitions to SOURCES.md — but SOURCES.md writes no
   A/B/C scale. Tier A is therefore editorial; it matches the official-docs rows S007, S012, S014,
   S019, S020 (all `docs`/`A`). Not falsifiable from the corpus, no finding; the missing scale is a
   pre-existing corpus gap, not an r17 or S025 error.

## Findings

No falsifying finding. F1 is the only concrete improvement I can ground; it is evidence completeness,
not an incorrect statement.

**F1 — low / evidence completeness.** `corpus/SOURCES.md:31` teaches the range endpoint `go1.27.3
(2026-10-19)`, but the committed Gate quote set `corpus/lessons/round-17.md:45-46` carries only
`#go1.27.0` and Release Policy; no `#go1.27.3` quote row. The w1 draft had one
(`.ufo/waves/round-17/w1/draft-sources-rows.md:32`); the committed table does not carry it. I verified
the date live: `sed -n '525,527p' /tmp/s025.html` ->
`<p id="go1.27.3">` / `go1.27.3` / `(released 2026-10-19)`. The registry text is true and the anchor
is named, so nothing is misstated; the quote table simply does not show the endpoint it asserts.
Smallest fix: after `round-17.md:45`, add this 3-word row (same fragment style as `:45`):

```
| S025 | same, `#go1.27.3` | go1.27.3 (released 2026-10-19) |
```

No other change.

## Calibrated notes (not findings)

- The `teaches` clause "release dates are lower bounds for a build" holds at the page's calendar-date
  granularity only; the page states no time of day (w1 recorded this at
  `.ufo/waves/round-17/w1/ScoutGoReleaseHistory.md:72`). Inert this round: no r17 statement uses a
  release date at same-day resolution. No fix required.
- The Release Policy quote grounds no r17 claim; it is an extra verified quote (S025's `scope` is
  release names/dates, not the support rule). Harmless, but a closure should not read it as a used
  passage.
- S025's `used-by` is literal but thin: the knowledge entry cites it only in its `source:` line
  (`…r17-go-carrier-diagnostics.md:1`), and no body statement uses a release date — `grep -rn
  "2026-08-19" LOG.md corpus/lessons/round-17.md corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
  .ufo/waves/round-17/claims.json` matches only `corpus/lessons/round-17.md:45`. C2's "rests on …
  Go release history" (`claims.json`) is thus an inventory dependency, not an exercised inference;
  this does not make the row wrong, but S025 is not by itself depth evidence.

## Limits / remaining unknowns

- The page is a rolling release index; the row's hash is a 2026-10-20 snapshot and will change at the
  next release (`recheck: on-release`). Reproducibility after 2026-10-20 is not claimed.
- The quotes are rendered HTML text, so QUALITY #17 excludes them from the machine instrument; this
  is a manual check under #1, consistent with `round-17.md:55-56`'s own statement.
- I checked one would-be second channel, `curl -sS 'https://go.dev/dl/?mode=json'` (22,898 B): it
  returns the two current stable entries (`go1.27.3`, `go1.26.10`) with keys `version`, `stable`,
  `files` only — no date/time field. So the page is the sole statement of its own dates, and I did
  not treat them as externally corroborated.
