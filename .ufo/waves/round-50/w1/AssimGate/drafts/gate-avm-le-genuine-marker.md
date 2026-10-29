# DRAFT (not landed) — AssimGate round-50 wave 1 — admitted entry `avm-le-image-genuine-marker`

Verdict: **ADMIT-AFTER-REWRITE**. Advice only; the L1 decides.
Staged source: `merge/kaidoku/knowledge/corpus/knowledge/avm-le-image-genuine-marker.md` (read-only; sha not recorded at base).
Proposed lane path: `corpus/knowledge/2026-10-28-r50-avm-le-genuine-marker.md`.
Flip satisfied: the round-40 refusal (`R40AssimReject`, `R40AssimE3/gate.md`) said "admissible in a round whose claim is the LE AVM variant, after digest/path/pin additions". Round 50's R50-C1 is that claim. The digest/path/pin additions are below.

## Scope (PROVINCE / corpus)

- `PROVINCE.md:408` and `:438` list "LE AVM members (`hsqs`)" as **Still Frontier**. The entry is LE-AVM ground: in scope, lane's sasquatch/unblob frontier.
- Admission moves **no** Frontier line. It records mechanism for a 4096-byte lane build. Real LE members stay Frontier until the R50-C1 data run.
- `corpus/README.md:97` and `:269-278` say the same (LE AVM members Frontier).

## Gate (row → status, evidence)

| QUALITY row | status | how |
|---|---|---|
| #1 resolvable source | met after rewrite | patches re-fetched 2026-10-28 (S155–S158); fixture and TSV are lane-tracked under `.ufo/waves/round-42/w1/artifacts/R42Assim/imported/` (S159); staged paths `lanes/kaidoku/round13/...` name a shokuknow path, replaced |
| #4 stable identity | met | image sha256 `18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4`, 4096 B; TSV sha256 `523637c885bb50c6d445bb096f247b9a66ab33633cae46af18be4a3d4c1b9ffa` |
| #5 labels | met after rewrite | observation (superblock, extractor runs) vs source reading (unblob 26.6.4 lines 48, 53–54) kept apart |
| #7 not examined | met | no vendor firmware; no squashfs-tools 4.3 rebuild this round; no real LE member (see calibration note K9) |
| #8 tool pins | met after rewrite (K5) | unblob 26.6.4 `squashfs.py` sha256 `2d7b901b…5599287`; unblob CLI `cli.py` sha256 `fc775f1a…9f86c`; sasquatch 4.5.1 (`sasquatch -v`: "unsquashfs version 4.5.1 (2022/03/17)"), binary sha256 `ad02d27a…4c774754`; stock unsquashfs 4.7.5 |
| #12 synthetic carrier bytes | met | the 4096 B image itself is retained (S159) |
| #18 execution evidence | met | argv, exit, stdout/stderr retained in `receipts/` (see report table) |
| #21 retention statement | met after rewrite | staged "what the lane keeps is the 4096-byte image" was false at base; now true via the imported copy |
| #35/#36 reversal | met | rejected sibling `avm-le-variant-reachability` gets a reversal line pointing here (see `reject-avm-le-variant-reachability.md`) |
| #42 quotes | met | each quote below is a contiguous run ≤25 words, located in the named file |

## Corrections required before landing (K1–K9)

- **K1 "introduced"**: the staged text says the upstream commit "introduced" patch 613. The commit header shows it is a cherry-pick: `(cherry picked from commit 214e9e5239e132b63904ce72e5edd4988826bff2)`, author date 2019-06-28 (S158). Write "cherry-picked into Freetz-NG as 86c23d96".
- **K2 "upstream's own AVM marker"**: the marker definition is Freetz's (`AVM-BE-format.txt`, S114) and Freetz's patch 550. Say "Freetz's", not "upstream's".
- **K3 "genuine"**: in this entry "genuine" means "mkfs_time == bytes_used, built by the lane's recipe". It does **not** mean vendor firmware. Retitle, e.g. "An AVM-marker little-endian SquashFS from the lane recipe is reachable".
- **K4 recipe**: `lead2-avm-le-genuine.tsv` lists `-no-mkfs-time`, but the plain 550 build (no 613, no flag) gives the same bytes (sha256 `18d3ad05…` for both `avm-le-plain550.squashfs` and `avm-le-genuine.squashfs`). The option flag is not needed for the marker. 613 only makes the marker optional (default `use_standard_mkfs_time = TRUE`).
- **K5 pins**: add the tool pins in the table above (staged entry has none for sasquatch).
- **K6 recheck path**: staged `grep -c -F 'modified AVM-format' lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv` names a shokuknow path. Replace with `grep -c -F 'modified AVM-format' .ufo/waves/round-42/w1/artifacts/R42Assim/imported/lead2-avm-le-genuine.tsv` (expected `1`; my run: `1`) and add the instrument below.
- **K7 ids**: R42's proposed S132–S136 are taken in the lane registry (S132 OpenWrt, S133/S134 DD-WRT, S135 unblob LICENSE, S136 sasquatch API). This draft uses S155–S160 per the assignment. S150–S154 are unallocated in the lane (max row S149); the L1 decides whether to take them.
- **K8 exit code**: unblob maps `Severity.WARNING` to exit 0 (`cli.py:466-467`), and a failed extraction reports WARNING. The file count is the witness, not the exit code (run B in `R40AssimReject`: 0 files, exit 0).
- **K9 real images**: the staged "does not say anything about a real Fritz!Box image" stays true. But lane artifacts already hold a real LE member measurement (R39 `vendor-image.tsv`, R40 `vendor-le.json`; calibration finding F3 in the report). Do not cite them as held. The R50-C1 data run is the first held real-member result.

## Quotes (located; ≤25 words; contiguous)

- **Q1** `receipts/patch101.patch` lines 7–8 (sha256 `e28b3341…4c707`): `+#define AVM_LE 2` / `+#define AVM_BE 3`.
- **Q2** `receipts/p550.patch` lines 7–9 (sha256 `603c36c9…5a7`): `+#if (TARGET_FORMAT == AVM_BE || TARGET_FORMAT == AVM_LE)` / `+	sBlk->mkfs_time = (int) sBlk->bytes_used;`.
- **Q3** `receipts/patch613.patch` lines 8, 18, 29 (sha256 `9af3b3de…4193f8`): `int use_standard_mkfs_time = TRUE;`; `if (!use_standard_mkfs_time)`; `use_standard_mkfs_time = FALSE;`.
- **Q4** `receipts/c613.patch` (commit header, sha256 `798ba899…920e48`): `Subject: [PATCH] squashfs4: enable timestamp at superblock`; `(cherry picked from commit 214e9e5239e132b63904ce72e5edd4988826bff2)`.
- **Q5** unblob 26.6.4 `squashfs.py` (installed copy sha256 `2d7b901b…5599287`): line 48 `is_avm = header.bytes_used == header.mkfs_time`; lines 53–54 `case Endian.LITTLE, _:` / `commands_args.append("-le")`.
- **Q6** `receipts/avm-be-format.txt` lines 13–14 (sha256 `c1c43f6f…a5d5`): `super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value`. Scope: this line defines the marker for AVM-BE; for LE the definition is 550's code (Q2).
- **Q7** unblob `cli.py` (installed sha256 `fc775f1a…9f86c`) lines 466–467: `(Severity.ERROR, 1),` / `(Severity.WARNING, 0),`.

## Measured on this host this round (2026-10-28)

- `unsquashfs -s` on the image: "Creation or last append time Wed Dec 31 21:06:01 1969", "Filesystem size 361 bytes" (TZ -03).
- `sasquatch -le -no-exit-code -f -d …`: exit 0, 4 files, `apple1.txt` = `apple`.
- `sasquatch-v4be -no-exit-code -f -d …` (no flag): exit 1, "Block size too small. File system is corrupt.", 0 files. `sasquatch-v4be -be`: same message, exit 1.
- `unblob --extract-dir …`: exit 0, log `SQUASHFS_V4_LE`, 4 `apple*.txt` files.
- Round-12 image (sha256 `afeb55a4…`): `mkfs_time` 1792847340, `bytes_used` 365; `sasquatch-v4be` refuses it the same way. unblob still selects `SQUASHFS_V4_LE` and extracts 4 files, so the marker is not what unblob reads on LE.

## Instrument (draft, run this round)

`tools/round-50/avm-le-gate-recheck.sh IMAGE [SHA256]` (in the seat dir). Exit 0 met (5/5), 1 not met, 2 unevaluable. Green on the lane image; red on the round-12 image (exit 1, C2 fails only); missing file exit 2; wrong expected sha exit 1. Outputs: `receipts/green.out`, `receipts/red-r12.out`, `receipts/missing.out`, `receipts/wrongsha.out`.

## Not examined

No vendor firmware image was downloaded (contract). No squashfs-tools 4.3 rebuild was run; the byte-identity of the plain 550 build and the option build rests on the sha256 values in the lane's own TSVs and the imported images. unblob is pinned to 26.6.4 only.
