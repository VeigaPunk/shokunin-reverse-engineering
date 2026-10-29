# AssimGate — round 50 wave 1 — assimilation gate, theme "AVM LE"

Seat: AssimGate (leaf; no subagents). Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Session UTC 2026-10-28T23:32Z–23:41Z.
Writes: this file; `.ufo/waves/round-50/w1/AssimGate/` (drafts, tools, receipts). Lane tree otherwise untouched. No git mutation. No tool installed or upgraded (sasquatch 4.5.1, sasquatch-v4be 4.5.1, unblob 26.6.4 were used as installed). No pacman. No AVM image downloaded. No REA call. No campaign tool run. Shokuknow read-only (fixtures and TSVs hashed in place and copied to scratch).

## Verdict

**Gate met: ≥1 admit and ≥1 reject from the set.** Advice to the L1; the L1 decides.

| entry (staged, `merge/kaidoku/knowledge/corpus/knowledge/`) | verdict | one-line reason | flip / what the L1 must do |
|---|---|---|---|
| `avm-le-image-genuine-marker.md` | **ADMIT-AFTER-REWRITE** | The central claim reproduces today on the lane's 4096-byte image (`hsqs`, mkfs_time == bytes_used == 361). unblob 26.6.4 selects `SQUASHFS_V4_LE` and publishes 4 files; `sasquatch-v4be` refuses it. Every cited source is now reachable in the lane or re-fetched with matching bytes. R40 refused it only because the round was not an LE-AVM round; R50 is one. | Land `drafts/gate-avm-le-genuine-marker.md` with corrections K1–K9 (cherry-pick wording, "Freetz" not "upstream", "genuine" = marker-set lane build not vendor firmware, pins, lane-relative recheck path, S155+ ids). Append the admitted path to `used-by` of S108 and S114. |
| `avm-le-variant-reachability.md` | **REJECT** (4th refusal: R39, R40, R42, now) | Headline falsified: a clean build with `-DTARGET_FORMAT=AVM_LE` and no option patch sets the marker (plain-550 image is byte-identical to the option-build image, sha256 `18d3ad05…`); the 1792847340 reading is a stale-binary artefact. Its surviving facts (`AVM_LE 2`/`AVM_BE 3`, 0 of 23 bodies, BE refusal) are true. | `drafts/reject-avm-le-variant-reachability.md` gives the reversal line naming the admitted entry. Flip: a corrections-only rewrite keeping the three surviving facts. |

Admission moves **no** Frontier line. `PROVINCE.md:408` and `:438` still list "LE AVM members (`hsqs`)" as Frontier; the admitted entry is mechanism for a 4096-byte lane build and says so. The real-member question stays with R50-C1's data run.

## Axes (Godspeed)

| axis | what this seat moved |
|---|---|
| coverage | Established that the LE-AVM mechanism is reachable in the lane tree (tracked fixture + TSV) and that the R50-C1 handler question has a measured precondition (unblob LE arm ignores the marker). Coverage of real members is **not** moved by this gate (F3 below). |
| depth | Pinned the mechanism to source lines: unblob 26.6.4 reads the marker only in `Endian.BIG, 4` (lines 48-50); the LE arm (lines 53-54) is marker-blind. Freetz 550 writes the marker for AVM_LE; 613 only makes it optional. |
| calibration | Both entries' staged headlines were checked against the bytes: the variant entry's "not reachable" is false; the genuine entry's "genuine" is a naming hazard; the staged recheck and S-ids point outside the lane. Found a pre-seen real LE member the L1 must disclose (F3). |

## Per-entry gate (PROVINCE / QUALITY / coverage)

- **PROVINCE scope**: both entries are sasquatch/unblob + squashfs LE-AVM ground (`PROVINCE.md:156-157` sasquatch bullet; `:408`, `:438` Frontier lines). In scope. No Adjacent refusal engaged.
- **QUALITY bar**: the genuine entry fails #1 (lane-path sources), #4 (no image sha), #8 (no sasquatch pin), #21 (retention claim false at base) as staged; all four are repaired in the draft. The variant entry fails #5/#35/#36 (headline contradicted by a retained image and by a sibling entry; no reversal pointer; third refusal).
- **Coverage ground (`corpus/README.md`)**: LE AVM is Frontier (`README.md:97`, `:269-278`). Neither entry moves it.

## Findings table (commands, exit codes, sha256)

Times are UTC. "exit" is the process exit status unless stated. Receipts are in `AssimGate/receipts/`; `receipts/SHA256SUMS.txt` lists every file.

| # | check | command (abridged) | exit | result / sha256 |
|---|---|---|---|---|
| 1 | Freetz 101 patch (master) re-fetched | `curl -sSL <raw master 101>` | 0 | HTTP 200, 1153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` (== R42 receipt); lines 7-8 `#define AVM_LE 2`, `#define AVM_BE 3`; `AVM_BE_AVM_LE` hits 0 |
| 2 | Freetz-NG 613 patch at pinned commit | `curl -sSL <raw 86c23d96 613>` | 0 | HTTP 200, 1601 B, sha256 `9af3b3debee9f6a144c03411a439e51f4ba4f9a1bd3aaac6b8760fa9394193f8` (== R42); line 8 `int use_standard_mkfs_time = TRUE;`; line 29 `use_standard_mkfs_time = FALSE;` |
| 3 | Freetz 550 patch (master) | `curl -sSL <raw master 550>` | 0 | HTTP 200, 1080 B, sha256 `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7` (== R42); lines 7-9 `#if (TARGET_FORMAT == AVM_BE \|\| TARGET_FORMAT == AVM_LE)`, `sBlk->mkfs_time = (int) sBlk->bytes_used;` |
| 4 | Freetz master patch set, 23 files | HTML listing `github.com/Freetz/freetz/tree/master/.../patches` (API listing returned HTTP 403, `receipts/freetz-listing-api-403.txt`), 23 raw fetches | 0 | 23 files, `freetz-patches.sha256`; `grep -l AVM_BE_AVM_LE` → **0 files** (the variant entry's claim holds); `mkfs_time` in `100-TARGET_FORMAT.patch` appears only in context lines 168-169 (no write found; not analysed further) and in 550 |
| 5 | Freetz AVM-BE-format.txt (defines the marker, Freetz doc) | `curl -sSL <raw AVM-BE-format.txt>` | 0 | HTTP 200, 1496 B, sha256 `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`; lines 13-14 quoted in gate Q6 (defines the marker for AVM-BE; LE definition is 550's code) |
| 6 | 613 commit header (cherry-pick origin) | `curl -sSL <github commit .patch 86c23d96>` | 0 | HTTP 200, 9322 B, sha256 `798ba899851b4ce0ac4cda6d2b6b0b44ca0cd308424d1f49d2a072ed01920e48`; Subject "squashfs4: enable timestamp at superblock"; `(cherry picked from commit 214e9e5239e132b63904ce72e5edd4988826bff2)`; Date 2019-06-28 (the commit API returned 403, `receipts/c613-api-403.json`) |
| 7 | fixture bytes (lane-tracked import) | `sha256sum .ufo/waves/round-42/w1/artifacts/R42Assim/imported/avm-le-genuine.squashfs`; `git ls-files …/imported` | 0 | sha256 `18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4`, 4096 B; tracked at HEAD; shokuknow `lanes/kaidoku/round13/work/avm-le-genuine.squashfs` identical; `avm-le-plain550.squashfs` identical (`18d3ad05…`); `avm-le-standard-time.squashfs` `6d787405…` |
| 8 | build TSV | `sha256sum …/imported/lead2-avm-le-genuine.tsv` and shokuknow copy | 0 | both `523637c885bb50c6d445bb096f247b9a66ab33633cae46af18be4a3d4c1b9ffa`; `grep -c -F 'modified AVM-format' <tsv>` → **1** (staged recheck, shokuknow path; identical bytes in the lane) |
| 9 | superblock (independent parse) | `python3` `struct` on the fixture (`receipts/`, instrument C2) | 0 | `hsqs`, inodes 5, mkfs_time 361, comp 4 (xz), block 65536, bytes_used 361 (u64 @40) |
| 10 | stock reader | `unsquashfs -s fixture` | 0 | "Creation or last append time Wed Dec 31 21:06:01 1969" (TZ -03), "Filesystem size 361 bytes" (`receipts/unsquashfs-s.out`) |
| 11 | LE extractor | `sasquatch -le -no-exit-code -f -d out fixture` | 0 | 4 regular files; `apple1.txt` = `apple` (`receipts/sasquatch-le.err`, `sq-le.out`) |
| 12 | BE extractor, no flag | `sasquatch-v4be -no-exit-code -f -d out fixture` | **1** | "Reading a different endian SQUASHFS filesystem", "FATAL ERROR: Block size too small. File system is corrupt.", 0 files (`receipts/sasquatch-v4be-noflag.err`) |
| 13 | BE extractor, `-be` | `sasquatch-v4be -be -no-exit-code -f -d out fixture` | **1** | same message, 0 files (`receipts/sasquatch-v4be-be-flag.err`) |
| 14 | unblob 26.6.4 handler | `unblob --extract-dir out fixture` | 0 | log `SQUASHFS_V4_LE`; 4 `apple*.txt` published (`receipts/unblob-26.6.4.log`) |
| 15 | unblob handler source (installed) | `sha256sum …/unblob/handlers/filesystem/squashfs.py`; `cat -n` lines 40-54 | 0 | sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` (== S108/S112 receipts). Line 48 `is_avm = header.bytes_used == header.mkfs_time`, inside `case Endian.BIG, 4:` (line 40); lines 53-54 `case Endian.LITTLE, _:` / `commands_args.append("-le")` (marker-blind) |
| 16 | unblob CLI exit mapping | `cat -n …/unblob/cli.py` lines 466-467 | 0 | sha256 `fc775f1ad66f05c0f6ba77fb74c80112ea99b4baf07900d7d701b7932259f86c` (== R42 tag-26.6.4 receipt); `(Severity.ERROR, 1),` `(Severity.WARNING, 0),` |
| 17 | round-12 stale-build image | python `struct` + `sasquatch-v4be` on `shokuknow/lanes/kaidoku/round12/work/avm-le.squashfs` | 0 / **1** | sha256 `afeb55a4b7667ff0ce7ccc909a15f624286a8dd861de44c3c0e7478d103a5299`; mkfs_time 1792847340 ≠ bytes_used 365; BE extractor exit 1, "Block size too small" (`receipts/r12-v4be.err`) |
| 18 | recheck instrument (draft, `tools/round-50/avm-le-gate-recheck.sh`) | `avm-le-gate-recheck.sh <fixture>` | **0** | 5/5 clauses met (`receipts/green.out`) |
| 19 | same instrument, round-12 image | `avm-le-gate-recheck.sh <r12>` | **1** | C1 and C2 fail (mkfs 1792847340 ≠ 365); C3 (unblob LE) and C4 (sasquatch -le) still pass (`receipts/red-r12.out`) — the marker does not drive the LE path |
| 20 | instrument unevaluable control | `avm-le-gate-recheck.sh <missing>` | **2** | "UNEVALUABLE: image not readable" (`receipts/missing.out`) |
| 21 | instrument wrong-digest control | `avm-le-gate-recheck.sh <fixture> 0000` | **1** | C1 fails, rest pass (`receipts/wrongsha.out`) |
| 22 | tool identities | `sha256sum ~/.local/bin/{sasquatch,sasquatch-v4be,unblob}`; `unblob --version` | 0 | sasquatch `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`; sasquatch-v4be `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; unblob 26.6.4, binary `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`; `sasquatch -v` banner "unsquashfs version 4.5.1 (2022/03/17)" (banner seen; exit not captured) (`receipts/tool-pins.txt`) |
| 23 | registry census | `grep -c '^| S'` / `git grep -E 'S15[0-9]'` in round-50 drafts | 0 | SOURCES.md has 149 rows, max **S149**; S132–S136 (R42's proposal) are occupied by other rows; no S150–S154 reference in round-50 drafts |
| 24 | prior LE measurement in lane artifacts (F3) | `grep` of `.ufo/waves/round-39/w2/artifacts/R39W2AssimAdjudicate/vendor-image.tsv`, `round-40/w1/artifacts/R40C1Reader/inspect/vendor-le.json` | 0 | see F3 |

Commands run with a non-zero exit that were expected: 12, 13, 17 (BE refusal), 19 (red control), 20, 21 (controls). `sasquatch-v4be -v` exited 1 (not a version probe; not used for pins).

## Findings

**F1 — genuine-marker entry: ADMIT-AFTER-REWRITE.** Re-grounded per QUALITY #1, #4, #8, #12, #18, #21, #42. Corrections K1–K9 are in `drafts/gate-avm-le-genuine-marker.md`. The R42 draft (`round-42/w1/artifacts/R42Assim/drafts/entry-B-avm-le-marker.md`, 9826 B, "DRAFT (not landed)") is the base; I re-measured it and added: the cherry-pick correction (S158), the Freetz-not-upstream wording, the "genuine means marker-set lane build" naming hazard, the sasquatch pin, and the recheck path. The R42 proposed rows S132–S136 cannot be used (taken in the lane); the draft uses S155–S160. Six rows are drafted in `drafts/sources-rows-S155-S160.md` (11 cells each, verified). Reused rows: S108 and S114 (append `used-by`).

**F2 — variant entry: REJECT.** Its headline is contradicted by two retained images and by patch 550 (checks 3, 7, 17). Its surviving facts (define values, 0/23 bodies, BE refusal) are true and are kept in the drafted reversal line. Note a second error in the staged text: the option build "with either" route does not produce the marker without `-no-mkfs-time` (`lead2-stale-build.tsv`, `clean_rebuild_avm_format_as_option_without_flag`: `mkfs_time` 1792871460, not AVM).

**F3 — calibration (for the L1, before the freeze): a real LE AVM member is already in the lane's artifacts, and the R50 plan's c6490 may be the same bytes.** Not verified by download (contract). Evidence:
- R39 `vendor-image.tsv` (`round-39/w2/artifacts/R39W2AssimAdjudicate/`): re-fetched image `FRITZ.Box_6490_Cable-07.57.image`, sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`, 39,741,440 B (2026-10-26T17:35Z); member `x86/filesystem.image`, 28,200,968 B, sha256 `7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419`, `hsqs`, comp 4, mkfs_time 28200029 == bytes_used 28200029; `unblob` LE arm, 6,912 files.
- R40 `C1Reader` (`round-40/w1/R40C1Reader.md`, row V1): the same member (row "V1 AVM-LE member 7ea4c628…", 28 200 968 B, `le/le`) read by an independent reader; `sasquatch` (no flag) match 4709/4709 regular files.
- The R50 plan's c6490 entry names the same image file (`fritzbox-6490-cable/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image`). The L1 scan (`round-50/l1/scan.py`, line 26) selects any tar member whose name ends in `filesystem.image`, so the 6490 row (`hsqs`, size 28200968) is very likely the LE x86 member, not `./var/tmp/filesystem.image` as the plan states. The R39 tar listing puts that member at `./var/remote/var/tmp/x86/filesystem.image` (R40 `SrcAvmVendor.md:19`).
- **Consequence:** c6490 is probably pre-seen (QUALITY #44; the freeze must count pre-seen items and disclose a re-observation, not a held-out result). Action for the L1: at fetch, compare the chosen member's sha256 with `7ea4c628…`; if equal, disclose c6490 as pre-seen, or swap it, before the freeze. The member path in the plan should also be corrected.
- Other carriers: `7530-08.25` appears in `round-40/w1/artifacts/R40C1ReconGaps/vendor-scan.tsv`; `7590-08.25` in R40 `ReconWrap/carrier-screen.tsv` and `VendorScout/candidates.tsv`; `FRITZ.Box_6430_Cable-07.30.image` has no lane mention (`git grep` → 0). I did not read those rows; the L1 should check whether they are measurements or candidate lists.

**F4 — registry ids.** Lane SOURCES max is S149. The shokuknow-staged ids S155/S206/S212–S214 do not exist in the lane; R42's proposed S132–S136 collide with lane rows (S132 OpenWrt, S133–S134 DD-WRT, S135 unblob LICENSE, S136 sasquatch API). S150–S154 are unallocated. Used S155–S160 per the assignment; the L1 may renumber.

**F5 — exit semantics.** unblob maps `Severity.WARNING` to exit 0 (check 16). R40 run B reproduced a zero-file extraction at unblob exit 0. Any R50 "success" must cite a file count (`receipts` from R40 are cited, not re-run).

**F6 — campaign paths.** The staged entries cite `lanes/kaidoku/round1x/work/…` paths. Those exist in the sibling `shokuknow` repo (`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round{12,13,14}/work/`), not in this lane. The lane-tracked copies are under `.ufo/waves/round-42/w1/artifacts/R42Assim/imported/` (checks 7-8). The variant entry's TSV `lead2-avm-le.tsv` (round 12) is only in shokuknow; its figures are reproduced here from the image (check 17).

**F7 — overlap.** Peers `C1SrcFreetz` and `C1SrcUnblob` are re-opening the same Freetz and unblob sources this round. Their sha256 values should match mine (101 `e28b3341…`, 613 `9af3b3de…`, 550 `603c36c9…`, unblob handler `2d7b901b…`, cli `fc775f1a…`). A mismatch is a change at the source that the L1 must see.

## Drafts (in `AssimGate/drafts/`)

- `gate-avm-le-genuine-marker.md` — admitted entry's Gate block, corrections K1–K9, Q1–Q7 quotes (≤25 words, located), measurements, "not examined".
- `sources-rows-S155-S160.md` — six 11-cell rows; reused rows S108 and S114 to append.
- `reject-avm-le-variant-reachability.md` — reject record, surviving facts, reversal line.

## Instruments (in `AssimGate/tools/round-50/`)

- `avm-le-gate-recheck.sh IMAGE [SHA256]` — five clauses (identity, superblock, unblob LE, sasquatch -le, sasquatch-v4be refusal). Exit 0 met, 1 not met, 2 unevaluable; scratch via TMPDIR only; no network. Controls run: green 0, round-12 red 1, missing 2, wrong digest 1 (checks 18-21). Not run: against any vendor image.

## Not run / limits

- No vendor image downloaded or Range-read (contract: only task-named images; none named). F3 is from prior lane artifacts, not re-observed.
- No squashfs-tools 4.3 rebuild; the byte-identity of the plain-550 and option builds rests on the lane's own sha256 records (`lead2-stale-build.tsv`, `R42Assim` receipts).
- GitHub API returned HTTP 403 for the commit and the patch directory; I used the `.patch` URL and the HTML listing instead (receipts kept).
- Freetz-NG master 404 for patch 613 was **not** re-checked this round (R42 receipt only).
- unblob pinned to 26.6.4 only. No claim about other unblob versions.
- The fixture's "genuine" name is the lane's; it is a marker-set synthetic image, not firmware.

## Tooling record

No tool installed, upgraded or removed. No pacman transaction. Existing tools used: `curl`, `sha256sum`, `python3`, `unsquashfs` 4.7.5 (`/usr/bin/unsquashfs`), `sasquatch` 4.5.1, `sasquatch-v4be` 4.5.1, `unblob` 26.6.4 (all in `~/.local/bin`, untouched). Scratch `/fast/scratch/hyaku/kaidoku-r50/AssimGate` (removed at the end of this seat, after the receipts were copied).
