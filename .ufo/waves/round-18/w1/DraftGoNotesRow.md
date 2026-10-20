# DraftGoNotesRow — Swiss-map SOURCES row and Gate quote (round 18, C3)

Author-side advisory draft. Lane files were not edited; the L1 integrates.

## Draft

SOURCES row (provisional ID `S034`: the next free ID after S032 at `corpus/SOURCES.md:38`; `claims.json:13` reserves `S033` for C1, so the L1 must confirm or reassign):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S034 | Go 1.24 Release Notes, Runtime — https://go.dev/doc/go1.24 | docs | A | Official Go 1.24 statement that the builtin `map` uses a Swiss Tables implementation and that `GOEXPERIMENT=noswissmap` disables it at build time; makes no Go 1.25 or later claim | Page fetched 2026-10-20 (sha256 `d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7`); `<h2 id="runtime">` raw lines 560–573; Swiss sentence 567–568; opt-out sentence 571–573 | The page documents the opt-out only as a build-time GOEXPERIMENT switch and says nothing about runtime map type-descriptor layout, so any layout or misread claim needs its own source (S023, S003). | mined | 2026-10-20 | on-release | none yet; C3 cites S034 on integration |

Gate quote line (21 words; located at go.dev/doc/go1.24 raw lines 571–573, `<p>` element under `<h2 id="runtime">`):

> Gate quote: "The new builtin map implementation and new runtime-internal mutex may be disabled by setting GOEXPERIMENT=noswissmap and GOEXPERIMENT=nospinbitmutex at build time respectively." — go.dev/doc/go1.24, lines 571–573

## Findings

### Observed (command output, this session)

- `curl -sL -o /tmp/go1.24.html https://go.dev/doc/go1.24`, then `sha256sum`: `d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7`, 1334 lines.
- `grep -n -i 'swiss|noswissmap|id="runtime"'` on that file: `560: <h2 id="runtime">Runtime</h2>`, `568: … Swiss Tables …`, `572: … GOEXPERIMENT=noswissmap …`. `grep -c -i noswissmap` → 1.
- `sed -n 558,574p` gave the verbatim text used for the quote. The Swiss sentence spans raw lines 567–568 and the opt-out spans 571–573.
- The reader-text fetch (`_read` of the URL) gave different line numbers (artifact://38830 lines 137–143). Anchors above use raw HTML lines, the convention S031 uses (`corpus/SOURCES.md:37`, "page lines 621–630").
- `wc -w` on the quote returns 21.
- `curl -sL https://go.dev/doc/go1.25` → sha256 `c9d872d374a3d52bbd5e1fad7d99b9eb44a7dac45d7032314d8cacd0702d38fd`. This matches S031's recorded snapshot hash (`corpus/SOURCES.md:37`), a consistency check on the fetch path. `grep -n -i 'swiss|noswissmap'` on that page returned no matches.

### Inference (labelled)

- The default-on reading of the builtin map (Swiss implementation active unless opted out) is inference from "may be disabled" at raw 571–573. The page does not state the default.
- The official 1.24 notes do not describe binary layout. Any relation between the opt-out and Ghidra's map-type layout is outside this row (see `corpus/SOURCES.md:44` path, S023 and S003).

### Gaps for the L1

- C3 (`claims.json:26`) builds `go1.25.0` carriers with `GOEXPERIMENT=noswissmap` (`claims.json:105`). The go1.25 release notes page I fetched contains no Swiss or noswissmap text, so the 1.25 opt-out is not grounded by that page. The 1.25 carriers need another source, such as the 1.25 toolchain source or the 1.25.0 build-config files, which I did not open.
- The 1.24 page is the 1.24.0 release notes. I did not check the 1.24.x patch-release notes or the toolchain source for `GOEXPERIMENT` handling.
- Official docs alone do not ground the `internal/abi` map-layout claim in C3 (`claims.json:27`); that row needs its own source.

### Tools

No installs or updates. Used `curl`, `sha256sum`, `grep`, `sed`, `wc` (already present). No REA, Ghidra, carrier, or lane VCS commands were run. Lane files other than this report were not touched.
