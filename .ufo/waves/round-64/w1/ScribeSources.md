# ScribeSources — R64 w1, S264/S265 re-grounding

Scope: re-ground the two staged jsc2js sources once each, on 2026-11-03, and draft their registry rows. No lane file was
edited; no release asset was downloaded; nothing was re-run to decorate the record.

## Behavior

1. Fetched S264 (jsc2js README at the pinned commit) once with `curl -fsSL`; hashed the bytes.
2. Fetched S265 (jsc2js releases page) once with `curl -fsSL`; hashed the bytes; counted tags on the page and the API total.
3. Located one quote per source (line number in the fetched bytes, nearest heading).
4. Drafted the two 11-column SOURCES rows and wrote the gate record and the count transcript.

## Gates (observed)

| source | fetch time (UTC) | bytes | sha256 | located quote | line | nearest heading |
|---|---|---|---|---|---|---|
| S264 | 2026-11-03T22:43:31Z | 8996 | `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3` | "Go to the Releases page and choose the V8 version that is identical to the one that produced your target `.jsc`." (21 words) | 130 | `### 1. Get the matching d8` |
| S265 | 2026-11-03T22:43:32Z | 328667 | `4aeaed401d1cff230a2ba7e9031a53a591906e607965bb93345467f20a13654b` | "Patched d8 for V8 15.6.75.25 (includes d8 + snapshot_blob.bin)." (10 tokens) | 972 | entry h2 `15.6.75.25` (line 785) under page h1 `Releases: xqy2006/jsc2js` (line 444) |

Cross-checks actually run:

- S264 bytes are byte-identical at all three places: the fetched URL, `git -C /home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src show
  01fc264d22055865a460b322399a15d84b71f5aa:README.md` and the staged working-tree copy (all `df85060f…eade3`); the clone's
  `rev-parse HEAD` is `01fc264d22055865a460b322399a15d84b71f5aa`.
- S265 page carries 10 unique `/releases/tag/` links (first page, `Next` → `?page=2`); the API total is 679 releases
  (`releases?per_page=1`, Link `rel="last"` page 679) and 679 tags.
- The three R64-C1 d8 pins (`14.8.178.14`, `14.8.178.1`, `14.7.173`) are each a release tag with
  `d8-<version>-linux.tar.gz` and `d8-<version>-windows.zip` assets, all published 2026-08-11 (release API metadata only).
- `sha256sum tools/round-64/jsc-route-matrix.py` = `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb`, equal to
  the brief's pin.

## Findings (reported, not edited)

1. **Registry path in the brief does not exist.** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/CORPUS.md` is absent; the
   11-column header named in the brief is at `corpus/SOURCES.md:5`, whose last row before this seat is S263. The rows follow that
   header and continue the numbering at S264/S265.
2. **Frozen instrument cites lane ids that are not jsc2js.** `tools/round-64/jsc-route-matrix.py:4` says "S125 README, S129 release
   inventory"; in the lane registry S125 is the AVM FRITZ!Box 6490 download directory and S129 is the binwalk v2 README.
   `plans/round-64-claims.md` (`## Assimilation`) shows these are shokuknow staging ids re-pointed to S264/S265 by document. The
   instrument is frozen, so this is a wording finding for the round record.
3. **README tag counts are not release counts.** S264 lines 182-198 ("369 tags", "57 exact failed tags") count upstream V8 source
   tags covered by the patch; the release inventory total is 679 (API), and no numeric release count appears in the frozen instrument.
4. **Asset digests are not comparable to the instrument pins.** The API `digest` fields are per-archive (`d8-14.8.178.14-linux.tar.gz`
   sha256 `9326e285…`); the instrument's `PINS` are per-file (d8, snapshot_blob.bin, icudtl.dat). No pin-vs-API digest match is claimed.

## Touched surfaces

- Written: `.ufo/waves/round-64/w1/ScribeSources/rows.md`, `.ufo/waves/round-64/w1/ScribeSources/gate.md`,
  `.ufo/waves/round-64/w1/ScribeSources/counts.txt`, `.ufo/waves/round-64/w1/ScribeSources.md` (this file).
- Read-only reads: the frozen instrument, `plans/round-64-claims.md`, `corpus/SOURCES.md`, the staged jsc2js clone, the toolchain dir.
- Scratch `/fast/scratch/hyaku/kaidoku-r64/ScribeSources` deleted after the seat; no temp file left behind.

## Out of scope (not done)

- No edit to `corpus/SOURCES.md`, the instrument, the claims file, `SCORECARD.md` or `LOG.md`; L1 pastes the rows.
- No instrument run, no matrix cell, no d8/View8/node execution; that is the executor seats' work and L1's landing check.
- No release asset downloaded, so no asset bytes or asset digests were verified locally.

## Artifacts

- `.ufo/waves/round-64/w1/ScribeSources/rows.md` — the two 11-column rows, verbatim.
- `.ufo/waves/round-64/w1/ScribeSources/gate.md` — per-source URL, access date, fetch time, sha256, quote, line, heading, decision, limits.
- `.ufo/waves/round-64/w1/ScribeSources/counts.txt` — commands and outputs for the page tags, API totals and pin-tag metadata.
