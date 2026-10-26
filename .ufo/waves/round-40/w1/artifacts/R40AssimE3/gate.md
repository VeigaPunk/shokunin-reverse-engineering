# Gate — round-40 assimilation of `merge/kaidoku` AVM entries (seat R40AssimE3)

Set: the five package entries under `merge/kaidoku/knowledge/corpus/knowledge/` whose subject is
AVM firmware images, plus E3 which the round-39 critic had already singled out. Everything below was
opened by **this** seat on **2026-10-26**; the package's own `opened 2026-10-24` proves nothing
about this lane.

## Admitted (1)

### `avm-image-extraction.md` → `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`

Re-grounded, not rewritten. PROVINCE scope: AVM-BE is named Frontier twice —
`PROVINCE.md:156-157` (the `- **sasquatch** — …` bullet, "big-endian/AVM stays here") and the
round-39 frontier note `PROVINCE.md:384` ("AVM-BE bodies and vendor-mangled images stay Frontier") —
which is exactly the surface R40-C1 moves, so this is lane ground and not sibling-domain material.

What this seat changed against QUALITY.md:

| # | gap in the staged entry | closed by |
|---|---|---|
| 4 | relative path, no digest | absolute path + sha256 `c7f74691…d32` on the image, plus digests for the TSV, the log and the recipe |
| 7 | no statement of what was not examined | "Not examined" paragraph: one directory, four files; no vendor member; no REA call; fragments/xattrs/sparse untested |
| 8 | no tool pins | unblob 26.6.4 with handler sha256 `2d7b901b…` (byte-identical to tag 26.6.4), `sasquatch-v4be` 4.5.1 (S107), verbatim argv from the retained log |
| 5 | mixed observation/inference | the extraction result is labelled observation *from the retained log*, with the log's missing exit status and version banner stated |
| — | marker-vs-layout conflation (the round-39 critic's item (c)) | the four-image marker × layout table, generated this seat's own bytes, both directions |
| — | generalisation caveat omitted the failure direction that matters | "What this corrects" names the two lane sentences it narrows, with paths and lines |

Expansion credit: `corpus/README.md` holds AVM-BE only as Frontier lines
(`:242`, `:243`, `:245` — "Still frontier: AVM-BE bodies, vendor-mangled images") and no entry stem
for a real AVM image; `ls corpus/knowledge/ | grep -i avm` returns no round-40 entry, so the ground
is not already held.

## Refused (5) — reason and flip, kept

| entry | reason | flip |
|---|---|---|
| `avm-firmware-image-unblob.md` | Its headline and causal sentence rest on "unblob … never notices the AVM marker at all", falsified by the pinned handler (lines 48-50 append `-be` *because* of the marker) and contradicted by its own argv row. What survives is the measurements, which round-39's critic reproduced; making the entry admissible means retracting its own headline — a rewrite, which the assimilation contract does not permit in-round | A rewrite whose headline and `:75-77` pair are retracted and whose measurement rows are re-taken after the freeze |
| `avm-image-build-blocker.md` | Standing claim "the release is gone" is overturned by its own successor round (the tarball resolves at the SourceForge path this seat adopted as S124), and `:43-44` presents a misparsed `bytes_used` of 7.85 EiB inside a 4 096-byte image as a measurement (QUALITY #5) | Convert to a reversal record: name the rejected decision by path and line and cite the flip evidence |
| `avm-le-variant-reachability.md` | Standing "not reachable" claim, overturned without a pointer by `avm-le-image-genuine-marker.md` in the same package — a reversal laundered as prose in a sibling file (QUALITY #35/#36) | Append a reversal line naming this file as the rejected decision, with the round-13 image and its sha256 |
| `avm-le-image-genuine-marker.md` | Correct in its own scope (LE), but carries no AVM-**BE** surface: R40-C1's ground is the big-endian layout, and this entry's "the marker is invisible to unblob" sentence is true only on the LE branch | Admissible in a round whose claim is the LE AVM variant, after digest/path/pin additions |
| `sasquatch-unblob-avm-branch.md` | Open lead "a real AVM image still needs a tool this host does not have" is stale by two rounds (the adopted entry extracts one), and it cites `unblob/main`, an unpinned branch, violating QUALITY #8 | Append the closing sentence with the round-11 image and sha256, and re-pin the source to tag 26.6.4 with handler digest `2d7b901b…` |

## New-row Gate records (URL or path, access date, ≤25-word located quote)

| row | source and access | quote (≤25 words) and location | grounds `teaches` |
|---|---|---|---|
| **S123** | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv`, sha256 `f205807d…` — opened 2026-10-26 | "absent - the AVM branch passes no -be" — row `unblob_be_flag` (9 words) | the retained run's argv omitted `-be`; the row records why |
| **S124** | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/freetz-squashfs4-host-be.mk`, sha256 `48fb043d…` — opened 2026-10-26 | `SQUASHFS4_HOST_BE_SOURCE_MD5:=d92ab59aabf5173f2a59089531e30dbf` — line 4 | the pinned tarball and its md5, so the image is rebuildable rather than trusted |
| **S125** | https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt — HTTP 200, 1 496 B, sha256 `c1c43f6f…a5d5` — opened 2026-10-26 | "the only data field stored in the little-endian format is the block length value at the beginning of each block" — lines 8-9 (22 words) | names the byte order of the field the entry's layout test reads |
| **S125** (second quote, marker bullet) | same bytes | "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'" — lines 13-14 (20 words) | keeps the marker as a separate property of the same document |

Why **S125 is a second row for a document the lane already holds as S114**: S114's anchor quotes the
opening line and the `mkfs_time` bullet and its `teaches` is about keeping AVM-BE distinct from
standard BE; it does not carry the block-length bullet, and CORPUS rule 2 forbids editing an anchor
in place. S125 does not claim to supersede S114 — no reversal happened — and the Gate names both so
the pair is traceable. If the L1 prefers one row per document, drop S125 and widen S114 in a future
contract-version step instead; the entry's layout claim then rests on this seat's own measurement
alone, which is the weaker position.

## used-by changes (old→new, append-only)

- S107: `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` → `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`
- S108: `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` → `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`
- S121: `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` → `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`

No `status` or `recheck` change is proposed on any row.

## Id collision check (scratch, command from prompt §10 verbatim modulo the output dir)

```
reg=122 staged=132 collisions=17
collision ids: S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120 S121 S122
next free lane id = 122 + 1 = S123
```

`comm -12` of the two sorted id lists. Every package id from S106 to S122 collides with a lane id;
the three rows this seat adopts (S200, S201, S192) collide with nothing, but they are renumbered to
continue the registry anyway, by document — see `collision/renumber-map.tsv`.

## Guard proof (indented-row fixture, scratch)

Registry fixture holds one column-zero row and one row indented by two spaces (`  | S002 |`); the
staged fixture holds S002 and an unrelated S900.

```
0-3-space pattern: reg=[S001 S002 ] collisions=1 -> [S002 ]
column-zero-only pattern: reg=[S001 ] collisions=0
```

The 0–3-space extractor the census uses catches the indented collision; the column-zero-only
pattern false-greens it. Both fixture files, both id lists and both collision outputs are retained
under `collision/`. The guard is not broken, so appending is permitted.
