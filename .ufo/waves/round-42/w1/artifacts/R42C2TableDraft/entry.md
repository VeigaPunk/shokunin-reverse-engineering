# SquashFS `extract-firmware` outcome triage v4: the whole handler family, a container-depth row, an unclaimed-residue row and a legacy-body cross-read (round 42)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70 (executables :25-26, argv decision :32-54, AVM marker branch :42-50, `get_dependencies` :68-69), the seven v1-v3 handler names :102,:159,:200,:245,:319,:364,:410, v4 handler names and magics :455,:462-463,:514,:521-522, v4 BE extractor :527, v4-broadcom extractor :549,:553 — re-read 2026-10-26 from the installed unblob 26.6.4 tree (`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`), not re-fetched from the URL
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `is_recursive_link` lines 42-47, `fix_symlink` lines 50-92 (loop 58-65, empty target 67-69, containment 79-87, kept-link rewrite 88-91), `carve_unknown_chunk` lines 116-127 (`extension = "unknown"` :119, `<start>-<end>.<ext>` :123) — re-read 2026-10-26 from the installed tree
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/firmware/FirmwarePublication.js` (`GAP_CONTINUATIONS` :14-19, `MAX_EXTRACTION_DEPTH` :23, depth continuation :24-29, `emptyGap` :39-46, dependency gaps :161-201, `chunkGaps` :226-238, `unknown-chunk-handler` :286, `extractor-failure` :288-293, `depth-limited` :294-299, `unpublished-entry` :301-307), `dist/domain/firmware/firmwareAnalysis.js` (gap kinds :84-91, gap `handler` :95, `dependencies` :101, `unpublished_entries` kinds :137-141), `dist/firmware/FirmwareRelease.js:27-32` — re-read 2026-10-26 from the installed 6.5.0 package
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `ExtractCommandFailedReport` :91-98 (`command` :95), `ExtractorDependencyNotFoundReport` :118-122, `ExtractorTimedOut` :125-138 (`cmd` :129), `MaliciousSymlinkRemoved` :133-138; `extractors/command.py` raise sites :59-77 and `Command.get_dependencies()` :101-102 — re-read 2026-10-26 from the installed tree
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — `-be` sets the swap flag; `debian/rules` builds the tree a second time as `CFLAGS=-DFIX_BE` and ships it as `sasquatch-v4be` — row pointer only this wave (cited by the inherited AVM row), not re-fetched
source: S122 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/file_utils.py — `is_safe_path`, the containment test `fix_symlink` applies — registry row only, not re-fetched this wave
source: S124 — https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch — line 35 "block length in AVM-BE format is stored in LE order" — row pointer only this wave, not re-fetched
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only` -> 15 rules, exit 0 (until that interpreter exists: `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/v4-refparse.py --skill <fixture> --table-only` -> 15 rules, exit 0)

**What v4 adds.** Rule block 21 in `SKILL.md` `## Queue-drain craft` holds table v4 after the marker
`<!-- sqfs-triage-table v4 -->`, read by `tools/round-42/sqfs-triage-v4.py`. The eight envelope fields, the
(label, action) pair and the no-match pair `(unclassified, none)` are v3's; the draft it implements is the
precedence list in `plans/round-42-claims.md` § R42-C2 **amendment A1**, steps 1-15. Fifteen rows carry
fifteen labels and fourteen action tokens (`cross-read-legacy` and `isolate-residue` are new). Three
decisions v3 got wrong on real envelopes are now rows:

1. **`container-depth-limited`** (step 2). `F = ∅` **and** `depth-limited ∈ G`: the SquashFS image sits below
   a container the run did not descend into. Measured: the whole OpenWrt TRX at `--max-depth 1` reports
   `H = {trx_v1}`, `G = {depth-limited}` and v3 answers `(no-squashfs-chunk, inspect-input)` — an instruction
   to inspect the input for an image that is present, one level down (S119 `FirmwarePublication.js:294-299`).
2. **`unknown-residue`** (step 9). `unknown-chunk-handler ∈ G`: bytes beside the filesystem that no handler
   claimed. REA mints the gap per chunk with a null handler (S119 `FirmwarePublication.js:286`) and unblob
   carves the range as `<start>-<end>.unknown` beside the tree (S118 :116-127). Measured: the carved x86 rootfs
   publishes `firmware.bin_extract/786432-851972.unknown` (a 65 540-byte tail) and v3 answers
   `(unclassified, none)`. The row sits **above** the depth row because that envelope carries both.
3. **`legacy-body-failure`** (step 7). A v1–v3 handler failed with zero files: `HF ∩ L ≠ ∅`. The action is a
   **cross-read**, never the `-be` wrapper, because a v1–v3 chunk always runs plain `sasquatch` with an explicit
   `-be`/`-le` and no header is parsed (S112 :40-54).

**The handler family is the surface (repairs R41-CL4).** `H` is the precedence text's `H`: chunks ∪ gap
handlers, nulls dropped (S119 `firmwareAnalysis.js:95`); `F` the `squashfs_` members; `L` the v1–v3 members;
`HF` the handlers of the `extractor-failure` gaps, or `F` when none carries one. A v1–v3 chunk is an ordinary
SquashFS chunk — unblob carves it with one of seven names (S112 :102,:159,:200,:245,:319,:364,:410) and runs
plain `sasquatch` on it (S112 :37,:51-54) — so v3's two answers for it were both wrong in the same way: the
precedence said `no-squashfs-chunk` (it tested for a `squashfs_v4_*` handler) and the table said
`unclassified` (no cell matched). Measured on a fresh dev input: the same `squashfs_v3_le.bin` fixture through
REA 6.5.0 gives `(depth-limited, raise-depth)` at `--max-depth 1` and `(clean, none)` at `--max-depth 3`,
where the frozen v3 interpreter answers `(unclassified, none)` on both.

**The table grammar (block 21).** Thirteen columns: `label | operation | provider | handler | failing handler |
gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source`.
`handler` is a glob over `F` (`none` = `F` empty, `*` = any); `failing handler` is a glob over `HF`
(`*` = anything, an empty `HF` included) and only steps 6 and 7 name it (`squashfs_v4_be`,
`squashfs_v[123]*`). Three deltas against the v3 reader: (a) the `v4` marker, with an older-only craft section
refused; (b) the `+` contains form in `dependencies`, because each dependency clause is membership ("D holds
`sasquatch-v4be`") and an exact-set cell lost a dependency set naming both binaries — the round-41 MEDIUM
finding (round-41 `w2/R41W2C2Table.md` F1, executed); (c) the thirteenth column itself.

**Block-20 prose repairs carried, and two re-scoped.** M1 (no embedded copy), M2/M3 (body row scoped, the
pre-check overrides the cell), L3 (dependency rows cite S119 as the minter), L4 (partial row cites the measured
4-of-5 oracle match), L6 (`SR = no` never proves no link was dropped, S118 :67-69), L7 (`none` double duty),
F4 (`dependencies` redundant with the handler on every measured class). Re-scoped: the pre-check says
**BE-structural** body before AVM layout (round-41 w2 F6) and its drop-`-be` PATH delivery is marked
`[INFERENCE]` (round-41 w2 F3); the legacy row states that the pre-check does not apply to a v1–v3 body.

**Scoring shape (pre-freeze, wave 1).** `check.py` compares the drafted block with an implementation of steps
1-15 over a grid of **38 664** REA-reachable points (handler family × gap set × dependency set × `HF` × `-be` ×
symlink report × published count × domain, with `HF ⊆ F` because a gap's handler is its chunk's): **38 664
agree, 0 differ**. On the 52 committed round-41 held-out envelopes: 52/52 with the precedence and 52/52 with
the frozen v3 interpreter's pairs. On eight real dev-arm envelopes (two `squashfs_v3` fixtures, the whole TRX
and the carved TRX rootfs, the carved x86 rootfs, each with and without the extractor on PATH): the draft
agrees with the precedence 8/8, and the frozen v3 interpreter gets **0 of 8** right — six `unclassified`, and
`no-squashfs-chunk` on the two whole-TRX runs that are the container class.

**Limits.** (1) `L` is defined relative to `F` (`L = {h ∈ F : v1/v2/v3}`), so step 7 is `HF ∩ L`; the table can
only say "`HF` matches a legacy name", which is the same predicate whenever `HF ⊆ F` — true of every envelope
REA can mint, since a gap's handler is its chunk's (S119 `FirmwarePublication.js:226-238`) — and differs only
on a synthetic gap naming a handler absent from `H` (not a reachable shape; excluded from the grid). (2)
`squashfs_v4_broadcom` shares the v4 BE extractor branch (S112 :549,:553) but clause 6 names only
`squashfs_v4_be`, so a broadcom BE failure with `-be` absent lands on the body row; `[INFERENCE]`, no measured
broadcom envelope. (3) A clean run need not record the child argv: both dev-arm legacy envelopes carry
`BE = n/a`, so no row may require `yes`. (4) The no-chunk rows read `F = ∅`; an envelope whose only evidence is
an `unknown-chunk-handler` gap *and* no SquashFS chunk is `no-squashfs-chunk` unless a depth gap is present.
(5) `none` is both the clean action and the no-match action, so those two envelopes are distinguishable only by
label. (6) Clause order means a dependency gap on one chunk masks an extractor failure on another. (7) The
`dependencies` contains form is only meaningful for the membership clauses. (8) A timed-out extractor records
`cmd` rather than `command` (S120 :125-138), so `BE` reads `n/a` and a timed-out BE failure lands on the body
row. (9) The layout pre-check needs carrier bytes and is inconclusive on a truncated body. (10) Gap kinds with
no row — `encrypted-chunk`, any combined set the clauses do not name — are `unclassified`/`none`. (11) `F` keeps
the `squashfs_` prefix while `H` keeps `squashfs`; no unblob 26.6.4 handler name is `squashfs`-prefixed
without the underscore (S112 names all ten), so the two forms coincide today. (12) The residue row is about the
envelope's residue, not about a second image: an unclaimed range that does contain another filesystem needs an
`unknown-chunk-handler` gap only because no handler matched at this depth, and a deeper rerun is the container
row's business.
