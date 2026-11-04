# Round-84 `corpus/SOURCES.md` delta — draft only (never written to `corpus/`)

Seat `ScribeSources`; lane `kaidoku-shokunin`; round 84; L1 integrates.

Grammar (the registry's exact 11-column form; `NF=13` under `gawk -F'|'`):

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

Every cell below is free of a literal or escaped `|`. No existing row is edited: this is an
**append of two new rows** plus a used-by change log. No predicate, counter, mutant table or
fixture is touched.

## Baseline this delta is written against

`git show HEAD:corpus/SOURCES.md` (the pre-round registry) census:

```
rows 205 | tier.A 187 tier.B 10 tier.C 8 | status.mined 184 status.rejected 21
```

That is exactly the census the frozen plan records as the round-start value
(`plans/round-84-claims.md`, "Census before `205 rows, A187/B10/C8, mined 184/rejected 21`").

## Row S301 — admit, tier A, status mined

Source opened 2026-11-04, session 2026-11-04: mksquashfs(1) man page,
`https://man.archlinux.org/man/mksquashfs.1.en`. Located quote for `-repro-time TIME`, taken from
the served bytes (HTTP 200, 57 790 B, sha256
`3ea8c1a1b429a5da35c7ffa0719ee2dade48ab8566c099c02b2c25bbe2052765`), derived-text lines 168-174:

> build a reproducible filesystem image. This is equivalent to specifying -mkfs-time TIME and
> -inode-time TIME, which achieves reproducibility by setting all timestamps to TIME.

(24 words.) The same first sentence opens the neighbouring `-repro` entry at derived-text lines
163-167, so the quote is kept long enough to be specific to `-repro-time` and not to `-repro`.

```
| S301 | mksquashfs(1) man page, squashfs-tools 4.7.5, filesystem time options — https://man.archlinux.org/man/mksquashfs.1.en (snapshot `mksquashfs.1.en.html`, 57 790 B, sha256 `3ea8c1a1b429a5da35c7ffa0719ee2dade48ab8566c099c02b2c25bbe2052765`, in `.ufo/waves/round-84/l1/sources/`) | docs | A | The `-repro-time TIME` option's own statement of what it makes reproducible; grounds deterministic fixture identity for carrier-class measurements, not image-content fidelity | Filesystem time options, derived-text lines 168-174: "build a reproducible filesystem image. This is equivalent to specifying -mkfs-time TIME and -inode-time TIME, which achieves reproducibility by setting all timestamps to TIME." (24 words); fetched 2026-11-04, HTTP 200 | A lane-built SquashFS fixture chain has stable digests when built with this option, so a carrier-class measurement can be re-derived byte for byte; it does not make two different source trees identical | mined | 2026-11-04 | on-release | corpus/knowledge/2026-11-04-r84-nested-container-chain.md, corpus/lessons/round-84.md |
```

## Row S302 — reject, tier A, status rejected

Candidate: the REA npm package tarball as an authority for the `depth-limited` gap-kind
taxonomy. Opened 2026-11-04: `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`
(HTTP 200, 5 634 033 B, sha256
`531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699`, equal to the digest the
registry already records for this package). Reason: the registry already holds this URL in five
scopes — S083, S090, S092, S119, S123 (the census's own `W04` duplicate-URL set for that URL) —
and the packed bytes expose no stable anchor: the taxonomy is reachable only by unpacking a
member path, not by addressing a locator in a served document.

```
| S302 | npm tarball `rea-agents-6.5.0.tgz` as an authority for the `depth-limited` gap-kind taxonomy — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | code | A | Curation candidate: the packed package as an authority for gap-kind semantics | Opened 2026-11-04; the registry already holds this URL in five scopes (S083/S090/S092/S119/S123) and the packed bytes expose no stable anchor | REJECTED: the packed tarball is not an anchored document and its URL is already held in five registry scopes; the anchored gap-kind authority is S119; flip: a published REA documentation URL that anchors the `depth-limited` gap-kind taxonomy | rejected | 2026-11-04 | on-release | corpus/lessons/round-84.md |
```

**Note on the `teaches` cross-reference.** This row's `teaches` cell names S119 as the anchored
gap-kind authority, which is correct under the assignment's numbering. Under the **landed**
numbering the tarball rejection is id `S303` and the anchored authority is the installed-file
row `S302`, so the landed cell reads "S302 is the anchored authority" instead. The two texts are
equivalent in substance; only the referenced id differs. Whichever numbering the L1 keeps, the
`teaches` cell must name the id that actually holds the anchored authority — a stale cross
reference is the failure mode this note exists to prevent.

## Used-by change log

`old` is the cell text before this delta; `new` is the cell text after. The two new rows have no
prior cell (`—`, not yet a row).

| row | old | new | why |
|---|---|---|---|
| S301 | — (row did not exist) | `corpus/knowledge/2026-11-04-r84-nested-container-chain.md, corpus/lessons/round-84.md` | new row; both destinations exist on disk and both literally contain the id `S301` |
| S302 | — (row did not exist) | `corpus/lessons/round-84.md` | new row, rejected; the lesson is where the rejection and its flip condition are recorded, and the lesson literally contains the id `S302` |
No other row's `used-by` cell changes: `status`, `recheck`, `scope`, `anchor`, `teaches`,
`opened` and `kind` are untouched everywhere, and no existing row is superseded.

### Used-by audit on the two new rows

The lane's forward convention: each mined row's `used-by` path must exist on disk **and** the
file must literally contain the row's own id (word-bounded). Measured for the two new rows:

| row | used-by destination | exists | literally cites the id |
|---|---|---|---|
| S301 | `corpus/knowledge/2026-11-04-r84-nested-container-chain.md` | yes | yes (1 line) |
| S301 | `corpus/lessons/round-84.md` | yes | yes (3 lines) |
| S302 | `corpus/lessons/round-84.md` | yes | yes (4 lines) |

`S302` is `status rejected`, so the census's E11 used-by path check does not apply to it (the
check runs only over `mined` rows); the destination is still recorded so the rejection and its
flip condition remain discoverable from the lesson.

Pre-existing forward-audit violations in the registry, **untouched by this delta**: S081
(`tools/round-27/xpin-attribute.mjs`), S246, S248 (×2), S254, S257, S259, S260, S261, S262,
S263. These are recorded here for the L1's disclosure sweep, not repaired here.

**Withdrawn proposal.** An earlier draft of this file proposed adding
`corpus/knowledge/2026-11-04-r84-nested-container-chain.md` to S119's `used-by` cell. That is
withdrawn: the round-84 knowledge entry does not literally contain `S119`, so the cell would
fail the forward literal-cite audit. S119's `used-by` is left unchanged.

## Id-binding conflict with the rows already landed in the lane working tree

This is the one thing the L1 must decide. The delta above is written in the **assignment's
numbering** (S301 = mksquashfs(1) man page; S302 = the rejected npm tarball), which is also the
frozen plan's numbering: `plans/round-84-claims.md` says "`corpus/SOURCES.md`: two rows opened
this round — S301 (mksquashfs(1) `-repro-time`; mined, tier A …) and S302 (rejected: the REA npm
tarball as an anchor for the `depth-limited` gap taxonomy …)".

While this seat worked, the L1 seat landed **three** rows into the lane working tree
(`corpus/SOURCES.md` lines 217-219, receipt
`.ufo/waves/round-84/l1/sources/round-84-sources.json`), binding the ids differently:

| id | landed content | vs. this assignment |
|---|---|---|
| S301 | mksquashfs(1) manual page — `docs`, tier A, `mined` | **matches** S301 (only the `source` and `scope` wording differ; `kind`, `tier`, `anchor`, `teaches`, `status`, `opened`, `recheck`, `used-by` are byte-identical) |
| S302 | rea-agents 6.5.0 installed package file `FirmwarePublication.js:17` — `code`, tier A, `mined` | **not in this assignment**; a third row the plan did not name |
| S303 | the npm tarball rejection — `code`, tier A, `rejected` | this assignment's **S302** content, id shifted by one |

Landed S302 is not a duplicate of anything: its source is an installed package file, not the
tarball URL, and its anchor is line 17 of that file. I verified the anchor independently — the
installed file and the tarball member `package/dist/firmware/FirmwarePublication.js` are both
17 416 B with sha256
`bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029`, and line 17 reads
`"depth-limited": "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path."`.

The landed numbering is already bound into four other artifacts, so adopting the
assignment-literal numbering means editing all of them:

- `corpus/knowledge/2026-11-04-r84-nested-container-chain.md` lines 11-12 (`source: S301`,
  `source: S302`)
- `corpus/lessons/round-84.md` Gate table (rows S301/S302/S303) and the M84-2 mistake row,
  which cites `E11 S301` / `E11 S302`
- `corpus/README.md` round-84 frontier note (`S301, S302`)
- `SKILL.md` instrument-registry row for `tools/round-84/nested-sqfs.py` ("S301 grounds
  determinism")

Measured consequences of each choice (mirror census, `scripts/sources-census.sh validate
--file <mirror>`):

| variant | exit | E-codes |
|---|---|---|
| D — assignment-literal delta on the HEAD baseline (205 rows) | **0** | none (one `W04`: the tarball URL already appears across scopes) |
| A — same file, census | 0 | rows 207 / A189 B10 C8 / mined 185 rejected 22 |
| E — assignment-literal delta applied on top of the **landed** tree | **1** | `E03 S301 duplicate id`, `E03 S302 duplicate id` |
| F — landed tree with S302/S303 swapped so the tarball reject takes S302 | 0 | none; rows 208 / A190 B10 C8 / mined 186 rejected 22 (the table's id order becomes non-monotonic; the census does not enforce order) |
| landed tree as-is, with the lesson and knowledge entry now on disk | 0 | none; rows 208 / A190 B10 C8 / mined 186 rejected 22 |

Recommendation to the L1: **keep the landed numbering** (variant F is not needed either — the
landed tree already validates at exit 0). The landed S303 carries this seat's rejection reason
and flip condition verbatim in substance, and the landed S302 row is an additional, correctly
sourced mined row rather than a conflict. Applying this delta literally on top of the landed
tree is the only outcome that fails the census (`E03`, exit 1).

## Registry log line (append to `## Search log`)

```
- 2026-11-04 round 84 — Question: which primary document grounds the reproducible SquashFS fixture identity the nested-chain counter depends on, and is the packed REA tarball an acceptable authority for the `depth-limited` gap-kind taxonomy? Where searched: man.archlinux.org `mksquashfs.1.en` (one GET, HTTP 200, 57 790 B, snapshot retained under `.ufo/waves/round-84/l1/sources/`) and the npm registry tarball `rea-agents-6.5.0.tgz` (one GET, HTTP 200, 5 634 033 B). Identified 2, screened 2, included 1 (S301, mined, tier A), excluded 1 (the tarball, registered rejected as S302 with a flip condition). Stop: the fixture-identity option is grounded in the tool's own manual and the gap taxonomy is already anchored by S119; no further source is opened for this round's two registry rows.
```

## What this delta does not do

- It does not edit `corpus/SOURCES.md`. The L1 lands it.
- It does not renumber, reorder or rewrite any existing row.
- It does not claim the man page says anything about extraction behaviour, and it does not claim
  the tarball is false — only that it is not an anchored document and that its URL is already in
  scope.
