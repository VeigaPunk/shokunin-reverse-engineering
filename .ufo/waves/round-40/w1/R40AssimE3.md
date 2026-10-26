# R40AssimE3 — round-40 assimilation seat: package entry `avm-image-extraction` re-grounded to `2026-10-26-r40-avm-be-squashfs-core`, and the AVM layout stated from bytes

**Verdict: CONFIRMED** — the one AVM entry the round-39 critic kept re-grounds clean under CORPUS.md
rule 1: every cited source was re-opened by this seat on 2026-10-26, the image digest and the marker
reproduce byte for byte, the extraction reproduces from its retained log, and the four additions the
critic named are in the draft. Along the way two live lane sentences that key AVM-ness on the
timestamp marker were shown to mispredict in both directions (findings F1, F2).

Role: scribe/executor (leaf). Nothing committed, pushed, frozen or installed. Lane corpus untouched —
the entry, the SOURCES rows and the Gate are **drafts in this seat's artifacts directory**; the L1
integrates. No REA call, no `unblob` run, no `sasquatch`/`sasquatch-v4be` run, no vendor firmware
opened; no frozen C1 carrier touched and no C2 held-out carrier built. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40AssimE3` removed at exit.

## What was done

1. **Re-opened every source the candidate cites.** `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv`
   (sha256 `f205807d…9eb0`), its image `avm-be.squashfs` (4 096 B, `c7f74691…d32`), `unblob.log`
   (`352e0d79…d5d7`), `freetz-squashfs4-host-be.mk` (`48fb043d…a3d5`), `avm-final.log`/`avm-final.sh`
   (`5f0c2957…a4e2`); upstream Freetz `AVM-BE-format.txt` (HTTP 200, 1 496 B, `c1c43f6f…a5d5`);
   the installed unblob 26.6.4 handler (`2d7b901b…9287`) and sasquatch 4.5.1 `unsquashfs.c`
   (`ece42b66…cb40`); `unblob --version` 26.6.4, `sasquatch-v4be -version` 4.5.1 (2022/03/17),
   Python 3.14.8. Quotes, locations and access dates are in `gate.md`.
2. **Measured the layout myself** (pure stdlib, no extractor): BE superblock `mkfs_time` 365 ==
   `bytes_used` 365, comp id 4 (xz), `inode_table_start` 121, `directory_table_start` 239, first
   metadata header `7400` → little-endian length 116, and `121 + 2 + 116 = 239`; the big-endian
   reading (29 696) fails the identity. The metadata block-length headers are little-endian while the
   superblock is big-endian — the AVM layout, stated from bytes rather than from the marker.
3. **Ran the marker × layout control matrix on this seat's own bytes** (`probe-avm-layout.py`,
   `probe-output.tsv`, `controls/`): the retained AVM image (marker true, LE lengths), a copy of it
   with `mkfs_time` set to 1 (marker false, still LE lengths → still AVM layout), a `--endian be`
   gzip image (marker false, BE lengths), and `--endian avm` (marker **true**, BE lengths). The last
   two are 373 B, differ only in bytes 8-12, and patching the marker reproduces `--endian avm` byte
   for byte (0 differing bytes, same sha256 `e68f6a53…`). So the marker mispredicts the layout in
   both directions, and `gen-squashfs.py --endian avm` is a marker transform — the critic's
   feed-forward 1 reproduces independently at a second tree and size.
4. **Wrote the four critic additions into the draft** — (a) absolute path + sha256, (b) unblob
   26.6.4 with handler digest + `sasquatch-v4be` 4.5.1 + the verbatim argv, (c) the sentence that
   the `-be`-dropping branch keys on `mkfs_time == bytes_used` and therefore also fires on a
   standard-BE body with a normalised timestamp, (d) the retained "one directory, four files" limit —
   and grounded the mechanism one step further than the critic: `read_block` byte-swaps the 2-byte
   block-length header iff `swap` is set (`unsquashfs.c:664-669`) and `-be` sets `swap` on a
   little-endian host (`:4390-4394`).
5. **Ran the §10 id-collision check and its guard proof** in scratch: 122 registry ids, 132 staged
   ids, **17 collisions** (S106-S122), next free lane id **S123**; the three adopted rows are
   renumbered to S123/S124/S125 **by document** (`collision/renumber-map.tsv`). The guard was proven
   able to fail on an indented scratch fixture (`  | S002 |`): the 0–3-space extractor catches the
   collision (1), the column-zero-only pattern reports 0 — a false green.
6. **Wrote the Gate** — one admit with per-criterion reasons against PROVINCE scope and the QUALITY
   bar, five refusals each with reason and flip condition, a quote + access date + location for every
   new row, and the three `used-by` changes as old→new.

## Gates

| gate | result |
|---|---|
| PROVINCE scope (AVM-BE is lane ground) | pass — `PROVINCE.md:156-157` and the round-39 frontier note `PROVINCE.md:384` both keep AVM-BE Frontier, which is R40-C1's surface |
| QUALITY bar, per entry | pass after additions for `avm-image-extraction.md` (#4 path+digest, #7 not-examined, #8 pins, #5 labels, #12 recipe retained); the other five fail with named rows and flips |
| Expansion credit is new ground | pass — `corpus/README.md:242,243,245` hold AVM-BE only as Frontier lines; `ls corpus/knowledge/` has no round-40 entry |
| Id-collision guard | pass — 17 collisions found, none adopted without a document-keyed renumber |
| Guard can fail | pass — indented fixture produces a collision under the census pattern and a false green under the column-zero-only pattern |
| No row appended as-is / no bulk append | pass — three rows, every one re-read and normalized by this seat |

## Touched surfaces

- Written (only here): `.ufo/waves/round-40/w1/R40AssimE3.md` and
  `.ufo/waves/round-40/w1/artifacts/R40AssimE3/` (see below).
- Read-only: `/home/vgpnk/Projects/shokuknow/...` (nothing written, no campaign tool run),
  `kaidoku-shokunin/corpus/{SOURCES.md,knowledge/*,README.md,QUALITY.md}`, `PROVINCE.md`,
  `SKILL.md`, `plans/round-40-claims.md`, round-39 waves, `tools/round-39/gen-squashfs.py` (executed
  from the lane, writing only into scratch), the unblob and sasquatch installs.
- No git/jj command that mutates anything. No tool installed, upgraded or removed; `unblob`,
  `sasquatch`, `sasquatch-v4be` untouched.

## Findings

- **F1 — `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:40`** reads "An image whose
  `mkfs_time` equals `bytes_used` loses `-be` and fails". True for a **standard-BE** body carrying
  the marker; false for a genuine AVM-layout body, which the round-11 image extracts without `-be`
  (retained log) and which keeps its layout when the marker is stripped (this seat's control). The
  draft entry narrows the sentence and names it by path and line; the L1 may want an appended
  correction in the round-40 lesson rather than an edit.
- **F2 — `SKILL.md:339`**, the v1 triage row `avm-marker-be-dropped`, keys the outcome on "mkfs_time
  equals bytes_used". On this evidence the row's discriminator has to be the **block-length byte
  order**, or a genuine AVM image is labelled broken and a marker-only standard-BE body is labelled
  AVM. The entry states this as a consequence only; the table is R40-C2's surface and this seat did
  not touch it.
- **F3 — the round-11 evidence has no exit code.** `unblob.log` carries no status line and no version
  banner, so "exit 0" and "26.6.4" are not in it; the version is pinned by the installed handler
  digest and the sasquatch version by the TSV. A second retained run in the same directory
  (`avm-final.log`, 09:01) ended in `Can't run extract command` with
  `dependencies=['sasquatch-v4be']` against `-e /tmp/r11-avm`, while the 12:01 run against
  `/tmp/r11-avm3` published four files. C1 receipts must carry their own exit code (QUALITY #18);
  these logs are re-grounding evidence, not a receipt.
- **F4 — [INFERENCE] a dependency-miss envelope is not proof of a missing binary.** The 09:01 run
  reported the `sasquatch-v4be` dependency while the same directory's manifest shows the tool in use
  an hour later; unblob's own landlock rule set in that log restricts writes to the output path. Cause
  unknown (the binary's PATH state at 09:01 was not recorded). For C2's `dep-missing-*` classes: an
  envelope's dependency report should be reproduced with a controlled PATH before a class is defined
  on it.
- **F5 — the `--endian avm` identity reproduces.** The critic proved it on a 5 610 B gzip tree; this
  seat's 373 B gzip tree reproduces the same 0-differing-bytes result and the same digest equality
  between the patched and the generated file. The generator's `avm` mode must stay barred from C1
  carriers.
- No peer conflict observed: this seat received no message from another seat and read no sibling
  artifact as evidence. Nothing here is offered as a counter-claim to another seat's measurement.

## Out of scope / not claimed

The entry is a **knowledge draft**, not execution evidence for R40-C1: it does not create a carrier,
does not run REA, and does not touch PROVINCE's Core table — the Core row, its carriers and its
counter are the L1's to freeze. No claim is made about AVM's own firmware members, about LE AVM
variants, about fragments/xattrs/sparse images, or about any extracted program. The scoring
implications of F2 belong to R40-C2 and were not tested here.

## Known limits

- The retained log is read, never re-run: the extraction's success rests on the 12:01 log's four
  `Processing file` lines plus the TSV's contents rows, with no exit status in the file.
- `sasquatch-v4be`'s own layout detection was not re-derived beyond the `-be`/`swap` path; the FIX_BE
  build's auto-detection heuristic was read, not exercised.
- The VendorProvenance of the round-11 image is the recipe plus the pinned tarball md5 (S124); the
  binary `mksquashfs` that produced it is not retained.
- `curl` was used only for `raw.githubusercontent.com` and reached HTTP 200 on both fetches; no
  mirror was compared.

## Artifacts (this seat's directory)

`.ufo/waves/round-40/w1/artifacts/R40AssimE3/`

- `adopted-entry.md` — the re-grounded entry, for `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`
- `sources-rows.md` — three normalized 11-column rows (S123/S124/S125) + three `used-by` old→new changes
- `gate.md` — admits, refusals with reasons and flips, per-row quotes with locations, collision result,
  guard proof
- `reground.md` — every command and the output it produced, with exit codes and the not-run list
- `probe-avm-layout.py`, `probe-output.tsv`, `controls.tsv`, `controls/` (four control images,
  `README.txt` marks them as controls, not carriers)
- `collision/` — `reg-ids`, `staged-ids`, `collisions`, `renumber-map.tsv`, the indented-row fixture
  files and both extractors' outputs
- `doc-bindings.md` — the literal strings the C1 counter requires (Core heading, Core row, the
  one-physical-line frontier note, the README `## Coverage map` row, the entry path/stem), with the
  counter's own regexes quoted beside them
- `check-doc-bindings.py` + `check-doc-bindings.out.txt` — pre-freeze self-check of those five
  bindings; `--selftest` exits 0 with three red cases that each fail (missing frontier note, a
  frontier note wrapped over two lines, a 12-cell SOURCES row), and against the lane root as it
  stands it exits 1 on every binding, which is correct pre-integration

## Late binding change — entry stem

`R40C1Counter` messaged after the drafts were written: the C1 counter hard-codes the entry as
`corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` (stem `2026-10-26-r40-avm-be-squashfs-core`)
and validates the four documentation bindings by literal string. This seat's drafts used
`2026-10-26-r40-avm-image-extraction`; every occurrence in `adopted-entry.md`, `sources-rows.md`,
`gate.md`, `collision/renumber-map.tsv` and this report was rebound to the counter's stem
(`grep -rc` after the change: 0 occurrences of the old stem, 16 of the new). The entry's content,
its six `source:` lines and the three SOURCES rows are unchanged and still carry `opened`
2026-10-26 with `used-by` on the new path. `doc-bindings.md` holds the paste-ready PROVINCE and
README text; the counter's `AVM_LAYOUT_RE` is `re.compile(r'AVM[ _-]layout')` with **no** IGNORECASE
flag although the message said case-insensitive, so the proposed lines use `AVM-layout` in that
exact case, and its frontier binding is a single physical line, so the note must not be soft-wrapped.

Rebinding is a naming change requested by the consumer of these drafts, not a change of any
measurement, quote, gate verdict or source row.

`R40C1Counter` then confirmed the substance on 2026-10-26: (a) `AVM_LAYOUT_RE` now carries
`re.IGNORECASE`, so any of `AVM-layout` / `AVM layout` / `AVM_layout` binds — `doc-bindings.md` and
the checker script were updated to mirror the fixed regex; (b) its `layout_ok` clause is not
marker-only — BE `sqsh` v4.0, `mkfs_time == bytes_used`, `0 < bytes_used <= size`, and a
little-endian first metadata block header, with the single-block identity as the tie-break, which is
exactly the two-directional failure my controls exhibit (`meta_signal: plausibility` on the round-11
image, `layout_ok` true); (c) the counter never reads an exit status out of the round-11 log — its
only non-REA use of that image is a `--selftest-rea` fixture built from two real REA runs, so finding
F3 stands as a caution about the log, not about the counter; (d) its gap rule is frozen data
(`gap-rule.json` `structural` map: `unknown-chunk-handler` / `depth-limited` with a null
`relative_path` allowed), so the proposed Core row now names the gap story in that shape; (e) the
`sourced` binding is satisfied by S123/S124/S125 plus the S107/S108/S121 extensions, whose `used-by`
cells carry the full entry path (7 occurrences of the path in `sources-rows.md`).
