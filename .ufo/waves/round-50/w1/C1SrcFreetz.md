# C1SrcFreetz — round 50, wave 1: source re-open of the AVM SquashFS definition (pre-freeze)

**Verdict: both sources re-opened and located; the sources do NOT describe a little-endian AVM layout.** The only LE-specific statements are (i) a byte-order symbol (patch 101) and (ii) a marker-writing code branch for an `AVM_LE` build (patch 550) that the shipped Freetz build never compiles (`squashfs4-host-be.mk:33`). The LE AVM marker therefore rests on the lane's byte probe, not on any source text. Three items need an L1 decision before the freeze: the S150 id collision, whether patch 550 gets its own row, and a dangling tier-text pointer. Draft registry row, gate text and receipts are under `.ufo/waves/round-50/w1/C1SrcFreetz/`. No lane file, no git mutation, no data run; no tool installed.

## Answers to the two questions

**(a) `AVM-BE-format.txt` (existing row S114).** Opened 2026-10-28T23:31:51Z (server Date), HTTP 200, 1,496 B, sha256 `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`, 22 lines.
- `:1-2` "a non-standard SquashFS format (called AVM-BE below) used by AVM since Fritz!OS Labor 6.35" — the format is defined as a *big-endian* variant.
- `:4-7` "it uses the big-endian layout for most of the data stored in the SquashFS image" (versus the little-endian "original/unmodified code" layout).
- `:8-9` "the only data field stored in the little-endian format is the block length value at the beginning of each block".
- `:10` "compression method is hardcoded to be XZ (aka LZMA2)"; `:13-14` "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'".
- `:16-19` user id table "always stored uncompressed" (marked TODO).
- **Says so explicitly: no text in this document describes an LE AVM layout.** Every statement is about the BE format; the marker is stated without any LE qualifier, but the document does not say the marker appears on LE images.

**(b) Patch `101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch`** (not yet a row). Opened 2026-10-28T23:31:54Z, HTTP 200, 1,153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`, 27 lines.
- `:7-8` `#define AVM_LE 2`, `#define AVM_BE 3`.
- `:17-18` the little-endian condition now accepts `AVM_LE`, selecting `__LITTLE_ENDIAN`.
- The patch adds no marker, no id-table change, no inode/directory change. Under its own name ("symbols only") it adds the symbol and byte order. **Its LE layout is standard LE by this text.**

## Findings

| # | finding | evidence (command → exit; sha256; location) | action for L1 |
|---|---|---|---|
| F1 | Source defines AVM as BE; no LE AVM layout text in S114 document | R1/R2 (curl 200, sha above); quote-check 12/12 located, exit 0 | none; S114 row stays as is |
| F2 | `AVM_LE` = little-endian byte order only (patch 101) | R1/R2; `:7`, `:17-18` | row S150 draft (below) |
| F3 | The LE marker is written in code by patch 550: `mkfs_time = (int) bytes_used` under `#if (TARGET_FORMAT == AVM_BE or AVM_LE)` (`:7-9`), and unsquashfs prints "is not available because of modified AVM-format (mkfs_time == bytes_used)" when `s_major == 4` and the fields are equal (`:24-27`). Fetched 2026-10-28T23:32:41Z, HTTP 200, 1,080 B, sha256 `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7` | R4/R5; quote-check rows 550 ×3 located | separate row (draft `S244`, or the next free id) — the only fetched text that writes the marker for LE |
| F4 | **The shipped Freetz build compiles only `AVM_BE`**: `EXTRA_CFLAGS="-DTARGET_FORMAT=AVM_BE"` (`squashfs4-host-be.mk:33`; mk sha256 `48fb043d8fb2e9b1ea916abb06316bb99a3c3d2232d8694e6f6f651a0393a3d5`, HTTP 200, 2,482 B). So the LE marker branch is source that Freetz never builds; it is not evidence that Freetz produces LE AVM images | R4; quote-check mk row located | plan wording "the AVM marker" for LE must say "the marker written by a Freetz `AVM_LE` build branch (patch 550), not AVM-authored text"; the marker's existence on LE firmware rests on the byte probe only |
| F5 | Across all 25 patch files of the Freetz set (fetched; sha256 list in `sources/allpatches-sha.json`), `AVM_LE`-conditional hunks occur only in 101 and 550. `AVM_BE`-only hunks: 250 (uncompressed id table `:55-56`, `_SQUASHFS_SWAP_SHORTS` `:7-19`), 350 (`:33-35`, comment "block length in AVM-BE format is stored in LE order") | R5; grep output | **[INFERENCE, source-level]**: by this set, an LE AVM image = standard LE SquashFS v4 + the marker; no id-table or block-length exception exists for LE. Counter must not assume anything beyond that |
| F6 | **ID collision: `S150` is taken in the lane.** Ten-plus lesson files (round-35 through round-45) cite `S150` for a rejected zenn.dev article (quarantine, fabrication-class refuse); `S150` occurs 239 times repo-wide; `corpus/SOURCES.md` has no S150 at base 7c678ae. Staged-id files from rounds 40/41 also reuse `S106..` numbers that collide with lane sources. First id cited nowhere: **`S243`** (scan R8) | R7, R8; `git grep -c S150 7c678ae…` exit 0 | L1 decision. Recommend `S243` for the Freetz row (breaks contiguity with S149; say so in the lesson), not a rewrite of the historical lessons. Alternative rejected: re-number the Zenn citations |
| F7 | **Tier text is dangling.** The plan's "tier by CORPUS.md tier text" and S147's "tier B per CORPUS tier text" point at a file that does not exist: `find . -name CORPUS.md` at the lane root → empty (R9). `corpus/QUALITY.md:110` defers tier definitions to `corpus/SOURCES.md`, which defines no tier letters beyond its header. Tiers are used in practice (S033 and S114 `B` for third-party community/docs; S003, S005, S013, S017 `A` for upstream code; S144, S146, S149 `C` rejected) | R9; `corpus/QUALITY.md:110` | L1 must either point the plan at an existing definition or state the tier rule in the lesson. This seat assigns **B** to the Freetz patch by analogy with S114 (same repo, same subject, third-party repack that reverse-engineers AVM's format), not by a cited rule — **[INFERENCE on the tier mapping]** |
| F8 | Counter predicate: source's marker check is `s_major == 4 && mkfs_time == (int)bytes_used` (patch 550 `:25`), a 32-bit truncation. Plan P50-C1 writes `mkfs_time == bytes_used` | R5 | Port the counter with the same 32-bit comparison (equal for all four carriers, ≤40 MB, so no score change), and state it in the docstring. Quote the unsquashfs string as the code locator for the marker clause |
| F9 | The S114 row's `teaches` cell states the marker "holds the same value as bytes_used" for AVM-BE; that is accurate for `:13-14` and must not be extended to LE by the lesson | quote-check `:13-14` located | lesson wording: "documented for AVM-BE (`:13-14`); the LE marker is a Freetz code branch (550), unbuilt by Freetz" |

## Draft registry row (for L1 to insert; NOT applied)

File: `.ufo/waves/round-50/w1/C1SrcFreetz/S150-registry-row-draft.md`. 11 cells, no `|` inside a cell (checked). Insert after the S149 row (`corpus/SOURCES.md:155`), before the blank line at `:156`. Tier **B**, kind `code`, status `mined`, opened `2026-10-28`, recheck `180d`, used-by `—`. **Id `S150` must not be used — see F6; the draft text is written under `S150` as instructed, with the alternative `S243` in its collision section.** A second draft for patch 550 is at `S-patch550-registry-row-draft.md` (id to be minted; `S244` if `S243` is chosen).

## Exact `## Gate` text

File: `.ufo/waves/round-50/w1/C1SrcFreetz/gate-draft.md`. Four sources, each with the located-quote locations, accessed time, sha256, and decision; the pipes inside code quotes are escaped for markdown. Quote check: `QUOTE_CHECK located=12 missing=0`, exit 0 (seat tool `tools/round-50/quote-check.py`, output `tools/round-50/quote-check.out.txt`).

## Plan-level attacks (for the freeze)

1. The plan's C1 frontier sentence ("LE AVM members") and the probe note imply the marker is an AVM property. Source supports only: BE marker (AVM-BE doc) and LE marker as a Freetz build branch that Freetz does not build (F3/F4). The lesson must not cite the Freetz branch as evidence that AVM images carry it.
2. CTL-C1-4 (standard LE carrier with `mkfs_time != bytes_used`) is consistent with the source: the marker is the only documented LE difference (F5), so the control is the right red test.
3. S147's correction row names "tier B per CORPUS tier text": no such text is in the lane (F7). Fix the pointer before freeze.

## Limits of this seat

- Source text only: nothing was run through unblob, sasquatch or REA; no image was downloaded; no claim about AVM firmware is made beyond the probe the L1 already holds.
- The 25-patch survey is the patch set at master on 2026-10-28; the history of `AVM_LE` builds is not visible from these files.
- "No text describes X" means: none in the fetched files; no full-web negative search was run.

## Artifacts

- Seat dir: `.ufo/waves/round-50/w1/C1SrcFreetz/` — `sources/` (verbatim copies of the fetched Freetz text and headers, no cookies), `tools/round-50/quote-check.py` (+ output), `receipts.md` (R1–R10 with commands and exits), `sha256-receipts.txt`, `draft-sha256.txt`, the three draft files.
- Receipt hashes: AVM-BE-format.txt `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`; 101 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`; 550 `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7`; 250 `f5964ad9bf2d24d319763e28f78bd441cd1d683d087e9b2e7bcd77d1db1b908d`; 350 `7f0a1b252d4bbde747efe98d1f97b52eab28d55ee957b7307d0344cbe1e220fc`; mk `48fb043d8fb2e9b1ea916abb06316bb99a3c3d2232d8694e6f6f651a0393a3d5`; patches-index `78b9a231311436a65aa37b6f2a124c04268b95824b964b9e74e0b47b7f926ad6`.

## Tool installs / updates

None in this seat.
