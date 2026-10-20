# Scout — Go 1.24 release notes: Swiss-table map and `noswissmap`

Seat: `KaidokuR18.ScoutGo124NotesSwiss` · Round 18 (hyaku phase 2) · 2026-10-20.
Axes: **calibration** (is the source exact and stable?), **operability** (can the L1 reproduce and insert
the row without me?), **depth** (does the row ground the C3 carrier pair, and where is its boundary?).

Question: where do the Go 1.24 release notes state the new builtin map implementation and its build-time
`GOEXPERIMENT=noswissmap` opt-out, and is a page-sha256 snapshot a stable citation?

## Finding (observation)

- URL: `https://go.dev/doc/go1.24` (fragment `#runtime`). Title `Go 1.24 Release Notes - The Go Programming
  Language`, `<h1>Go 1.24 Release Notes</h1>` at line 435, HTTP 200, `content-type: text/html; charset=utf-8`,
  82,634 bytes.
- Heading/id: `<h2 id="runtime">Runtime</h2>` at **page HTML line 560**. There is **no finer anchor** on the
  page for maps (`grep -n '<h[234][^>]*id=' ... | grep -i map` returns only the unrelated
  `#hashmaphashpkghashmaphash` and `#runtimepkgruntime` headings), so `https://go.dev/doc/go1.24#runtime`
  lands on the Runtime heading; the map text is the two paragraphs under it, **lines 564–573**.
- The naming sentence (lines 567–568): “These improvements include a new builtin `map` implementation based on
  **Swiss Tables**”.
- The opt-out sentence (lines 571–573, exact contiguous quote, **21 words**):

  > The new builtin map implementation and new runtime-internal mutex may be disabled by setting GOEXPERIMENT=noswissmap and GOEXPERIMENT=nospinbitmutex at build time respectively.

  One sentence covers both the map and mutex opt-outs; the map clause is the first half. The word “default”
  appears nowhere in the runtime section (`sed -n '560,573p' | grep -i default` → no match, exit 1; the page has
  9 matching lines elsewhere, none about maps).
- Release revision: `go1.24.0 (released 2025-02-11)` from `https://go.dev/doc/devel/release`.

## Hash stability (observed, 8 fetches)

Recipe from the ticket: `curl -sL https://go.dev/doc/go1.24 | sha256sum`.

| # | Request variant | Local time (UTC) | sha256 |
|---|---|---|---|
| 1 | plain, `-o` file (`-w` http_code=200 size=82634) | ≤ 15:25:15Z (clock sampled after fetches 1–3) | `d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7` |
| 2 | plain | ≤ 15:25:15Z (clock sampled after fetches 1–3) | same |
| 3 | plain (third) | ≤ 15:25:15Z (clock sampled after fetches 1–3) | same |
| 4 | `#runtime` fragment | between 15:25:15Z and 15:26:51Z (not individually timestamped) | same |
| 5 | `--compressed` (decoded body) | same window, not individually timestamped | same |
| 6 | browser User-Agent | same window, not individually timestamped | same |
| 7 | `Cache-Control: no-cache` | same window, not individually timestamped | same |
| 8 | plain, after ~96 s gap | 15:26:51Z | same |

**Stable: yes, 8/8 identical**, including across fragment, encoding, UA and cache-control variants. Response
headers carry **no `ETag` and no `Last-Modified`** (`curl -sSI` shows only HTTP/2 200 and security headers), so
the hash is the only available content identity. Inference: go.dev serves this versioned release-notes page as
static HTML, so the hash behaves as a snapshot id over the access window; it is **not** a cryptographic
commitment — the page can be edited in place on go.dev, so re-hash before a later citation (row records
`recheck: on-release`).

## Draft SOURCES row (11 cells)

`id` = **S034**: S033 is already reserved for the planned PR-#9348 row (`supersedes S032`), per
`.ufo/waves/round-18/contract.md:44-45`, `.ufo/waves/round-18/claims.json:14`, and
`.ufo/waves/round-18/gen-wave1.py:384-387`. If the L1 does not insert that superseding row, renumber this
draft to S033.

```markdown
| S034 | Go 1.24 Release Notes, Runtime — https://go.dev/doc/go1.24#runtime | docs | A | Go 1.24's default builtin map implementation (Swiss Tables) and the build-time GOEXPERIMENT=noswissmap opt-out | `#runtime` heading (page HTML line 560), runtime performance paragraphs at page HTML lines 564-573; Go 1.24.0 released 2025-02-11; page snapshot sha256 d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7; accessed 2026-10-20 | The new builtin map is a Go 1.24 runtime improvement that `GOEXPERIMENT=noswissmap` disables at build time, so a carrier's map layout is fixed by its build experiment, not by runtime behavior. | queued | 2026-10-20 | on-release | — |
```

Shape checks on the row fragment (contract `/home/vgpnk/Projects/shokunin/CORPUS.md:79-150`):

| Check | Command | Output / exit |
|---|---|---|
| 11 cells (NF=13 with `-F'\|'`) | `awk -F'\|' '{print NF}' row.txt` | `13`, exit 0 |
| cell count | `awk -F'\|' '{print NF-2}' row.txt` | `11` |
| no inner pipe | same | `11` columns ⇒ no extra pipes |
| kind/tier/status enums | contract validator one-liner from CORPUS.md | no output, exit 0 |
| quote ≤25 words | Python tag-strip of lines 571–573 | `WORDS: 21`, `HAS_PIPE: False`, `APPears_in_page: True` |

`status: queued` is deliberate — the row is not yet cited by a knowledge path. When C3's knowledge entry lands
and cites S034, flip it to `mined`, set `used-by` to that path, and log old→new in the round lesson (contract
rule 2). `tier: A` is scoped to the release-note statement only, not to Ghidra behavior or to 1.25.

## Cross-checks (secondary, NOT part of the row)

- Go 1.24.6 source, `src/internal/goexperiment/flags.go:119-120` (**observed**, tag `go1.24.6`, HTTP 200):
  `// SwissMap enables the SwissTable-based map implementation.` / `SwissMap bool`.
- Go 1.24.6 source, `src/internal/buildcfg/exp.go` (**observed**, sha256
  `aefed48703c63f23e3a07acbb44815faaee698752a89e7383e9f9c90c90bc65b`):
  `:28-30` calls the baseline “the experiment flags that are enabled by default”; `:76-84`
  `baseline := goexperiment.Flags{... SwissMap: true ...}`; `:92-135` applies the environment override, and
  `:127-128` strips the `no` prefix before setting the flag false. This is what makes “default” and
  “`noswissmap` = off” facts rather than implications from the notes alone.
- Boundary: `https://go.dev/doc/go1.25` has **0** matches for `swiss`/`noswissmap`
  (`grep -n -i -E 'swiss|noswissmap' | head` → empty; grep exit 1). This row must not be used to predict
  1.25 behavior; that is `ScoutGo125MapsNotes`' lane.
- Failed attempt, recorded for honesty: `api.github.com/repos/golang/website/commits?path=_content/doc/go1.24.html`
  returned **HTTP 403, rate limit remaining 0**; no revision metadata was taken from it. The row therefore uses
  the release date plus the page sha256 as its revision, not a website commit.

## Calibration for the L1

1. The page says the new map is enabled by being the shipped implementation and can be **disabled** at build
   time. It never says “default”; the word in `scope` is the lane's label, backed by the go1.24.6 baseline
   above. Do not quote the page as saying “default”.
2. The `noswissmap` switch is **build-time** (`:573`). A prebuilt carrier cannot switch at runtime, so the C3
   `{swiss, noswissmap}` pair is a legitimate controlled variable only if each carrier is built under the
   corresponding `GOEXPERIMENT`; the notes do not say the experiment is recorded in build info — that is an
   inference for C3's prediction, not this row's claim.
3. The opt-out sentence bundles map and mutex. A reader who quotes only “`GOEXPERIMENT=noswissmap`” should not
   attribute the mutex claim to the map row.

## Re-verify (copy-paste, from the lane root)

```sh
curl -sL https://go.dev/doc/go1.24 | sha256sum            # expect d35c2d52…c4e7
curl -sL https://go.dev/doc/go1.24 | nl -ba | sed -n '560,573p'
curl -sL https://go.dev/doc/go1.24 | sed -n '571,573p'
curl -sL https://go.dev/doc/go1.24 | grep -c -i swiss     # expect 2, both in the map paragraphs
curl -sL https://go.dev/doc/go1.24 | grep -n -i noswissmap # expect only line 572
```

The `curl | sha256sum`, `curl | nl | sed`, and `curl | sed` forms were run live (exit 0 each). The two `grep`
counts were run against the saved `/tmp/go124.html` whose sha256 is identical to those live fetches; both
exited 0 with 2 and 1 matching lines respectively. No tool installs or upgrades were performed: `curl`, `grep`, `sed`, `awk`, `nl`,
`sha256sum`, and `python3` were already present. No writes outside this report; no REA/Ghidra run; no carrier
execution; no git/jj writes.

## Remaining unknowns

- None blocking this row. Open, non-blocking: whether go.dev will edit the 1.24 page (mitigated by sha256 +
  `on-release`); whether the L1 keeps the S033 superseding row (affects only this row's id).
