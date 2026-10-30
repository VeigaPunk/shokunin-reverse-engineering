# ScribeBlock27 — SKILL.md rule block 27 draft (round 52, wave 1)

Seat: **ScribeBlock27** (scribe) · role: draft SKILL.md rule block 27 for R52-C2 ·
lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · wave: `round-52/w1` ·
status: **settled** (draft delivered; the L1 integrates, amends and freezes).

## Behaviour

Drafted the full markdown text of the new numbered item
`- **27. SquashFS \`extract_firmware\` outcome triage v6 — the failed-body executability rule (round 52).**`
for `SKILL.md` `## Queue-drain craft`, as the paste-ready block in
`.ufo/waves/round-52/w1/ScribeBlock27/block27.md` (between the `<<<BLOCK27>>>` and
`<<<END BLOCK27>>>` markers). It keeps block 26's numbering convention and table style
(13-column triage table, one `<!-- sqfs-triage-table v6 -->` marker, one
`<!-- sqfs-triage-actions: ... -->` comment with the **unchanged** 17-token action
vocabulary) and contains, as required:

1. **Dated supersession** of block 26's ddwrt rows — "block 26 stays as history, and
   from 2026-10-30 every decision this block makes, block 26 defers to it"; the
   `legacy-body-failure` `failing handler` cell drops `squashfs_v3_ddwrt`
   (`squashfs_v1,squashfs_v2,squashfs_v3`), and the ddwrt FAILED body
   `dmg_Z3_v3ddwrt_inode_table` stops routing `legacy-body-failure`/`cross-read-legacy`.
2. **The new row** `legacy-body-unreadable` (`failing handler` `squashfs_v3_ddwrt`,
   gap kinds `extractor-failure+`, published files `0`) with action
   **`preserve-unresolved` — no cross-read**, placed as the superseded row's sibling.
   Exactly one label changes on the frozen 126-envelope corpus.
3. **The reader-census table** (family-level verdict, fixture-level measurement, with
   its evidence pointer and per-row line numbers), the two no-reader families, the
   `squashfs_v3_ddwrt` family row, and the statement that **no new reader is claimed
   validated** and that a clean extraction is not independent-reader success.
4. **The F5 scoping correction** of block 26's "`symlink` and `special` both count"
   phrasing: device-node kinds (char/block device, FIFO, socket) carry **no disposition**
   under the extraction law — no gap kind admitted, `allowed` for a device kind is the
   empty list, `required['char-device'] = false`, a gap on a device row is a violation
   (fail closed); "special" counts only the non-regular entries the extractor
   materialises in the tree. Stated as the law's scope and cited to the law entry
   (PLACEHOLDER), the round-51 derivation and S250/S251.
5. **file:line pointers** that resolve at the landing, with `PLACEHOLDER` marks where
   the line numbers depend on the landing (the round-52 law entry, `tools/round-52/
   sqfs-triage-v6.py`, the S252 SOURCES row, and block 26's own span).

The draft also states the executability audit the table is scored against (a FAILED-body
envelope whose prescribed action is a cross-read while its family's census records no
independent reader is a violation; the count must be 0) and a **draft, unscored status**
paragraph that claims only the measurement actually taken.

Mechanical parity check against the committed block-26 table (`SKILL.md:552-570`): the
draft's v6 table carries **all 17 v5 rows plus the one new row (18)**, every row has 13
cells, and every row is byte-identical to v5 except **three intentional cells**
(`legacy-body-failure` `failing handler` and `source`; the `cause` cells of
`mixed-symlinks` and `in-tree-symlink-metadata`). The action-vocabulary comment is
byte-identical to block 26's — the new row reuses the existing `preserve-unresolved`
token and adds only a label.

## Gates run (and their outcomes)

| gate | command | exit | outcome |
| --- | --- | --- | --- |
| v5 before-arm over the frozen 126-envelope corpus | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> --rev ab0eafedc41402b43b41a4362084119578dfe7ce --freeze c525de54a53eb3c4fee28ede2721da4527cf8ece --envelopes <LANE>/.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out $S/v5-base.json` | **0** | `n_envelopes 126`, `pair_mismatch_count 0`, `verdict met`; `dmg_Z3_v3ddwrt_inode_table` → `legacy-body-failure` in **both** the table and the independent evaluator column; instrument sha256 `f29eb92073dfff0cae48658985a7df3a34b1558430183dacc9968c2dff71b16e`; stdout sha256 `bca7e0baf0600a7efc2c77c8657cee9a9c79b926d5c6ba110debc115a60e27cc`; UTC 2026-10-30T10:48:00Z |
| freeze ancestry | `git merge-base --is-ancestor c525de5… ab0eafe…` | 0 | the round base is an ancestor of the claims draft |
| SKILL.md unchanged between the claims draft and HEAD | `git diff --stat ab0eafe… HEAD` | 0 | only `.ufo/waves/round-52/*` files differ, so `SKILL.md:548-584` (block 26) holds |
| census receipt tracked in the lane tree | `git ls-files .ufo/waves/round-50/w3/ExecTriageV5/receipts/` | 0 | `reader-census.txt` is tracked → the citation resolves at the landing |
| disk guard before the pass | `scripts/hyaku/disk-guard.sh status` | 0 | `/fast/scratch/hyaku` 47 % used, 426 G free |

**Not run (and not claimed):** the v6 instrument does not exist at draft time, so the
v6 after-arm (`executability_violations 0`), its selftest, its controls and its
freeze-drift gate are **not measured here**. No REA run, no `--data-run`, no network
fetch, no vendor bytes.

## Touched surfaces

- `.ufo/waves/round-52/w1/ScribeBlock27/block27.md` — the draft (paste-ready block +
  draft notes).
- `.ufo/waves/round-52/w1/ScribeBlock27/v5-base.json`, `v5-base.stdout` — the before-arm
  receipt (copied from scratch).
- `.ufo/waves/round-52/w1/ScribeBlock27.md` — this report.
- `.ufo/waves/round-52/w1/ScribeBlock27/status.json` — wave accounting.
- Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeBlock27` — removed after the receipt
  copy.

Nothing else was written. No lane `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`,
`LOG.md`, `SCORECARD.md`, `SHONEN.md`; no fleet repo file; no commit, push, stage, stash
or other mutating git/jj command (read-only git only: `log`, `show`, `diff`, `ls-files`,
`ls-tree`, `merge-base --is-ancestor`). No tool was installed, so the tooling-authorization
record is empty (no `pacman`, `uv tool`, `npx` or binary install was needed or made).

## Findings

1. **The claims file states the wrong reason for the ddwrt no-pad clean envelopes.**
   `plans/round-52-claims.md` (R52-C2): *"The two clean ddwrt no-pad `_ddefault`
   envelopes keep \`clean\` (their readers succeeded; no route change)."* The census
   records the opposite for those two bodies — `reader-census.txt:31,:34`:
   `squashfs_v3.be.nopad.bin daa8e72d355d 1 2 NO-READER (both refuse)` and
   `squashfs_v3.le.nopad.bin e7482db480f9 1 2 NO-READER (both refuse)`. What succeeded
   is the **extraction** (4 published files, no gap), not a reader. The route is
   unchanged either way, so the decision stands and only the reason is wrong; the draft
   states it correctly and the claims text should be amended in the freeze's amendment
   record.
2. **The census supports a stronger and exact statement than the claim's.** The claim
   says "the ddwrt family has no validated second reader; 6/7 no-reader", which reads
   against census row 35 (`squashfs_v3_le.bin 0161351caec8 0 0 readable-by-both`). The
   exact fact: **every corpus body REA handles as `squashfs_v3_ddwrt` is over a
   NO-READER fixture (6 of 6)**; the family's one readable fixture is handled by REA as
   `squashfs_v3` (`squashfs_v3_le_ddefault`, 2 published files). The draft row rests on
   this.
3. **The census has no row for the FAILED body's own bytes.** The audit the claim
   specifies ("every FAILED-body envelope's prescribed action against the family's reader
   census") is a family-level inference: `Z3_v3ddwrt_inode_table.bin`
   (sha256 prefix `839c17a83b70`) is a dmg carve, never offered to a reader in the
   census. The lookup key (family verdict + a stated body-variant limit) must be frozen
   in the instrument; the draft states the limit in the block so it cannot be widened or
   narrowed silently.
4. **The v6 audit as scoped leaves a disclosed residue.** It checks FAILED bodies only;
   the seven clean `squashfs_v3_ddwrt` envelopes keep `clean`/`none`, whose action still
   prescribes an oracle match no reader can supply for those bodies — the same defect
   class v5's F2 fixed for the three wholly no-reader families. The claims freeze it out
   of v6; the draft discloses it rather than leaving it silent.
5. **The verbatim phrase the claim names lives in block 21, not block 26.**
   "`symlink` and `special` both count" is at `SKILL.md:540` (v4 `mixed-symlinks`) and
   `SKILL.md:542` (v4 `in-tree-symlink-metadata`); block 26's rows (`:565`, `:567`) carry
   the terser "count one gap per kept link or special file" / "count one gap per entry".
   The draft scopes both block-26 rows and names block 21 as the carrier of the phrase,
   so the correction lands on the text the claim points at without contradicting it.

## Out of scope (deliberately not done here)

- The v6 instrument, its evaluator, its selftest, its controls and the freeze-drift gate
  (another seat's build); the block cites the instrument as a landing artifact.
- The claims file itself (the L1 amends it from these findings); no claims edit was made.
- The round-52 device-accounting law entry and the S252 SOURCES row (PLACEHOLDERs for the
  freeze).
- Any REA execution, carrier re-fetch, `--data-run` or vendor download.

## Artifacts

- Draft: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeBlock27/block27.md`
- Before-arm receipt: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeBlock27/v5-base.json`
  (sha256 `e14a2d1c3c908077655d1eb981a2033e2a55c01156be42a0e5380996c845a531`) and
  `v5-base.stdout` (sha256 `bca7e0baf0600a7efc2c77c8657cee9a9c79b926d5c6ba110debc115a60e27cc`)
- This report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeBlock27.md`
- Wave accounting: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScribeBlock27/status.json`
