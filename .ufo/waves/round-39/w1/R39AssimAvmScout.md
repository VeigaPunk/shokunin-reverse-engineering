# R39AssimAvmScout — assimilation candidate scan (AVM / sasquatch / unblob / squashfs), 2026-10-26

**Verdict: DONE.** Recommend ADMIT `avm-firmware-image-unblob` (with 4 mandatory corrections; one of them is a falsified headline) and REJECT `avm-image-build-blocker` + `avm-le-variant-reachability` (stale premises, refuted by bytes opened today). Id-collision guard proven: 12 collisions (S106–S117), the indented-fixture proof catches what the column-zero pattern misses. No tool installed or upgraded. Scratch removed. All paths below are under `.ufo/waves/round-39/w1/artifacts/R39AssimAvmScout/` (abbrev `$ART`) unless absolute.

Observed vs inferred: everything marked "observed" was run this wave on this host; `[INFERENCE]` is flagged.

## 1. Candidate set

Package `/home/vgpnk/Projects/shokuknow/merge/kaidoku` (read-only; `MERGE-REPORT.md` lists 77 entries; 11 match avm-/sasquatch-/unblob-). Lane state from `corpus/lessons/round-36.md` and `round-38.md` `## Gate`:

| staged entry | cites (staged ids) | lane state |
|---|---|---|
| unblob-sasquatch-dependency | S106 S107 | ADMITTED r36 (lane S110/S111) |
| unblob-format-matrix | S122 | ADMITTED r38 (lane S116/S117) |
| sasquatch-prebuilt-package-inventory | S130 | REFUSED r36 (flip: both claims corrected and re-opened) |
| sasquatch-unblob-compatibility | S183 S184 S185 S186 | REFUSED r36 (campaign-local evidence; flip: evidence imported and re-measured) |
| sasquatch-unblob-compatibility-precondition | S165 | REFUSED r36+r38 (premise falsified; no flip) |
| sasquatch-unblob-avm-branch | S189 S190 S191 S192 | REFUSED r38 (unpinned `main`, campaign-local rows; flip: re-grounded on lane receipts, source repinned to 26.6.4) |
| **avm-firmware-image-unblob** | S216 S217 S218 S219 S220 S223 | **never adjudicated** |
| **avm-image-build-blocker** | S197 S198 S199 | never adjudicated |
| **avm-image-extraction** | S200 S201 | never adjudicated |
| **avm-le-image-genuine-marker** | S212 S213 S214 | never adjudicated |
| **avm-le-variant-reachability** | S206 S207 | never adjudicated |

Citation join cross-check: sibling `R39Quarantine/avm-citation-join.tsv` gives the same entry→id map.

## 2. Source re-open (access 2026-10-26T16:41Z, curl, all `-L`; table in `$ART/fetch/http-status.tsv`)

| staged id | URL (short) | HTTP | bytes | sha256 (first 16) | quote located |
|---|---|---|---|---|---|
| S216 | download.avm.de/…/fritz.os/ | 200 | 592 | 063ec39af00bd45e | listing row `FRITZ.Box_6490_Cable-07.57.image  04-Sep-2023 17:08  39741440` (`$ART/fetch/S216-avm-index.html`) |
| S217 | …/fritz.os/info_en.txt | 200 | 67591 | 6c601b342da91f75 | line 10 `Version:        FRITZ!OS 7.57`, line 14 `Release date:   04.09.2023`, line 8 `Product:        FRITZ!Box 6490 Cable` |
| S220 | Freetz-NG `docs/make/README.md` (master) | 200 | 101328 | 8d1cae2fc1d9af03 | line 674: "AVM-LE is the format used by AVM to pack the filesystem of some cable boxes, e.g. 6490, 6590 (x86 core only)." — **master is an unpinned ref** |
| S192 (=lane S114) | Freetz `AVM-BE-format.txt` (master) | 200 | 1496 | c1c43f6f97d7477d | "super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'" (lines 11-12) |
| S189 (=lane S108/S112) | unblob `…/squashfs.py` main vs tag 26.6.4 | 200/200 | 19842 | 2d7b901b54e2ad28 (both, equal) | lines 47-50: `is_avm = header.bytes_used == header.mkfs_time` / `if not is_avm: commands_args.append("-be")` |
| S206 | Freetz `101-TARGET_FORMAT…patch` (master) | 200 | 1153 | e28b3341021c4c62 | `+#define AVM_LE 2` / `+#define AVM_BE 3` |
| S214 | Freetz-NG `613-avm_format_as_option.patch` @86c23d9 | 200 | 1601 | 9af3b3debee9f6a1 | `+int use_standard_mkfs_time = TRUE;`; `-no-mkfs-time … use AVM format (length instead of timestamp)` |
| S198 | api.github.com plougher/squashfs-tools tags | 200 | 7787 | d90120ead0373c8f | 18 tags, **no 4.3**; but live list also holds `3.1` and `squashfs-tools-4.6.1`, which the entry's list omits (entry says "18 tags returned" yet enumerates 16) |
| S122 (=lane S116) | unblob.org/formats | 200 | 216890 | 8f8c29aff33d5aa1 | byte-identical to lane S116's recorded sha256 `8f8c29af…bbc5`; ids `squashfs-v4-be`, `-v4-le`, `-v4-broadcom`, … |
| S130 | github.com/onekey-sec/sasquatch/releases (+API) | 200 | 349155 / 87700 | 5de7ee6095ca80b0 / 07f75c08e8bfb7d6 | API: 8 releases; `sasquatch-v1.0` has only `sasquatch(-dbgsym)_1.0_amd64.deb` (2 assets) — **the r36 refusal reason ("each release carries a deb per architecture" false) still holds** |
| S106/S107 | unblob README HEAD, devttys0 README | 200 | 7580 / 1050 | 6544d60f22f7b521 / f09961ee6c2bf5dd | equal to lane S110/S111 recorded digests |

Additional re-opens: Freetz recipe `squashfs4-host-be.mk` line 3 `SQUASHFS4_HOST_BE_SOURCE_MD5:=d92ab59aabf5173f2a59089531e30dbf` (HTTP 200). The tarball `https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz` → HTTP 200, 182550 B, **md5 d92ab59a… = the pin** (`$ART/fetch/sq43-md5.txt`).

## 3. Own-work rows (S197 S199 S200 S201 S207 S212 S213 S218 S219 S223) — the evidence gap

These point at `lanes/kaidoku/round{9..14}/work/*.tsv`. The files **exist** under `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round*/work/` (R38-CL1: the r38 "exist nowhere" sweep was rooted wrongly), but they are **not lane-retained bytes** (QUALITY #1; same reason as the r36 `sasquatch-unblob-compatibility` refusal). Rows that point at them cannot be appended as-is. Resolution used here: **re-measure on lane bytes** (next section) and have the L1 import `$ART/…` into the lane's own evidence tree, then cite lane-retained own-work rows.

## 4. Lane-byte reproduction of the flagship entry (`avm-firmware-image-unblob`) — observed

Command set (scratch since removed): `curl` of the S216 image, `tar xf`, a 14-line Python superblock read, `~/.local/bin/sasquatch-v4be` / `sasquatch` direct, `~/.local/bin/unblob -v -e OUT -f avm.image` (cwd = scratch).

- Image: HTTP 200, 39741440 B, **sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`** — equal to the campaign's `firmware_sha256` in `lead2-avm-firmware-superblocks.tsv`. tar members and sizes equal the entry (28200968 / 3552264 / 5443592 / 1932808).
- Superblocks (`$ART/fetch/avm-superblocks.txt`): x86 member `hsqs`, comp 4 (xz), mkfs_time 28200029 = bytes_used 28200029; sibling member `sqsh`, comp 4, mkfs_time 5442392 = bytes_used 5442392. Members' sha256: LE `7ea4c628…0419`, BE `334e56df…f3d4`. Trailing slack 939 B (LE) and 1200 B (BE) = member size − bytes_used: **matches the entry.** Both `kernel.image` members start `81 12 ed fe` (matches the entry's anomaly; which silicon boots them stays unestablished).
- unblob 26.6.4 (`$ART/fetch/unblob-avm-chunks.txt`, `unblob-avm-extract-commands.txt`): outer tar; `handler=squashfs_v4_be chunk=0x0-0x531000 … 0-5443584.squashfs_v4_be` run as `sasquatch-v4be -no-exit-code -f -d …` (**no `-be`**); `handler=squashfs_v4_le chunk=0x0-0x1ae5000 … 0-28200960.squashfs_v4_le` run as `sasquatch -le -no-exit-code -f -d …`. Files: LE tree 6912, BE tree 2942, total 9877 (symlinks 615 / 263 extra). Exit 0. **Matches S219 exactly.**
- Direct sasquatch on the genuine BE member: **no flag → exit 0, 697 regular files** (device nodes refused for lack of root); **with `-be` → exit 1, "Reading a different endian SQUASHFS filesystem … read_id_table: failed to read id table block / FATAL ERROR: File system corruption detected", 0 files** (`$ART/fetch/sasquatch-v4be-{noflag,beflag}-genuine-avm-be.stderr.txt`). `sasquatch -le` on the LE member: exit 0, 4709 files.
- Timestamps: `file` renders the marker as `created: Mon Nov 23 09:20:29 1970` (LE) / `Wed Mar  4 23:46:32 1970` (BE) on this host; the entry quotes `06:20:29` / `20:46:32`. Rendered times are timezone-dependent — cite the integers.

### Lane bytes that CONTRADICT the staged entry (must be corrected before admission)

1. **Headline "unblob never notices the AVM marker / the marker is invisible to unblob" is false for BE.** Handler selection ignores it, but the extractor argv does not: `squashfs.py:47-50` (lane S108 = tag 26.6.4, sha `2d7b901b…`) drops `-be` exactly when `bytes_used == mkfs_time`. The entry's own S219 row shows the BE command without `-be`. Correct statement: *handler = endianness+magic only; BE argv = marker-conditional; LE = marker-blind.* The "round 12 expected a dedicated AVM branch; unblob does not need one" sentence is wrong for BE (the branch exists, and is why plain `-be` is absent).
2. The "1970 date is the visible fingerprint" wording is true of the marker but the lane's doctored probe (`.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe`, K1-avm, `created: Thu Jan 1 02:43:00 1970`) shows the same fingerprint on a **non-AVM body**. The date identifies the marker, not an AVM-built body.
3. **The stderr line "SquashFS version [1024.0] / inode count [N] suggests a SquashFS image of a different endianess" appears on BOTH the genuine AVM-BE body (no-flag run: line printed, then "Successfully decompressed", exit 0) and the doctored non-AVM body (then FATAL, exit 1;** `$ART/fetch/lane-doctored-k1-avm-noflag.stderr.txt` **).** It is not a discriminator; the discriminator is `read_id_table … FATAL` vs `Successfully decompressed`.
4. S223's NMI-gap/TI-checksum paragraph and the S198 tag list are partly unverifiable/stale (3.1, squashfs-tools-4.6.1 missing from the list). Drop the NMI/TI paragraph or label it as one image; count the tag list from the live API.
5. Pins: S220 and S192 are `master`; S189 is `main`. Repin (S192 already = lane S114; unblob → lane S108 at tag 26.6.4; S220 → pin a commit sha or record the raw sha256 `8d1cae2f…ad862d6`).

## 5. Further observed measurement — AVM marker on LE is invisible to REA (fits C2 negative row)

Dev carriers built from a fresh tree (`gen-squashfs.py tree le-ctl.sqsh --endian le --comp gzip`; `le-avm.sqsh` = same bytes with `mkfs_time := bytes_used`, offsets 8..11 only; `$ART/le-avm/`). REA: `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <in> <fresh out>`, both exit 0. Structural diff (`$ART/le-avm/rea-le-{ctl,avm}.json`, paths normalised): differences are only evidence_id, subject sha256, REA temp-dir paths, provider blob ids and the `file` magic's "created" text. **Same coverage `partial`, same single `unpublished-entry` gap (the in-tree symlink), `diagnostics: []`.** So an LE image with the marker is a plain `clean`/`in-tree-symlink-metadata` row; the marker needs no LE table row beyond "no effect".

### Implication for R39-C2's table (AVM marker / AVM-BE body) — [INFERENCE where noted]

- Observed (r38 probe, `rea-k1-avm.json`): the marker is only visible in an envelope **when the extraction fails**: `data/normalized_result/diagnostics[0]/report/command` = `sasquatch-v4be -no-exit-code -f -d …` (no `-be`), gap kind `extractor-failure`. In a clean run (`rea-k1-orig.json`, `rea-le-*.json`) no `command` string is in the envelope at all.
- Therefore `avm-marker-be-dropped` is separable from `body-extractor-failure` only through that `command` string (`-be` absent on a failing BE chunk); a **genuine AVM-BE body extracts clean and will look identical to `clean`** [INFERENCE: REA was not run on the real AVM-BE member — the wave rule limits REA to dev carriers built from own trees; the direct sasquatch/unblob runs above support the extraction half, not the envelope shape]. The held-out generator can therefore only plant the `avm-marker-be-dropped` class as marker-on-standard-body (doctored), and the table must say so rather than claim to detect genuine AVM bodies.
- The "different endianess" stderr line is non-discriminating (item 3) — a triage row keyed on it would misfire; key on `command` lacking `-be` plus failure.

## 6. Per-entry recommendation

PROVINCE scope (`PROVINCE.md:156-157`, `:374`; `corpus/README.md:238-239`): AVM-BE is declared **Frontier** firmware-extraction ground; entries are in scope as frontier notes, not Core. Expansion credit: `corpus/README.md` holds no AVM genuine-image coverage row — ground not held.

| entry | verdict | reasons | flip |
|---|---|---|---|
| **avm-firmware-image-unblob** | **ADMIT, rewritten** | In scope; flagship claims reproduced on lane bytes (sha equal, 9877/6912/2942, commands, superblocks); external sources S216/S217/S220 re-open; supports R39-C2's AVM rows with a genuine-body control and the extraction discriminator; contradicts nothing once §4 corrections c1–c5 applied. **Do not append S218/S219/S223 as-is**; replace with lane-retained own-work rows for the §4 artifacts. Candidate rows by document: staged S216→lane S118, S217→S119, S220→S120 (+ a pinned/sha'd row), own-work rows next; S192→reuse S114; unblob handler→reuse S108. Entry must not be citable as "the AVM marker is invisible to unblob". | refuse if S216 image sha/size changes, S220 line 674 vanishes, or c1 is not applied (the corrected `squashfs.py:47-50` sentence is the load-bearing line) |
| **avm-image-build-blocker** | **REJECT** | Premise "4.3 tarball not served from any reachable mirror" is false: SourceForge path HTTP 200, md5 = Freetz pin (§2); the entry's own successor `avm-image-extraction` supersedes it; S198 list stale; S197/S199 campaign-local. | none (superseded); would only stand as history |
| **avm-le-variant-reachability** | **REJECT** | Headline "not reachable" overturned by `avm-le-image-genuine-marker`; the name/value point (S206 `AVM_LE 2`/`AVM_BE 3`) is real but adds nothing C1/C2 can use; S207 campaign-local. | fold the `AVM_LE=2, AVM_BE=3` fact into the admitted entry citing S206 (live sha `e28b3341…`) instead |
| avm-image-extraction | defer (second choice) | Genuine AVM-BE tiny image reproduces only by building squashfs 4.3 + 23 patches; tarball now verified; S200/S201 campaign-local, would need a re-build to retain bytes. Not cheap for this round. | admit if a seat rebuilds the 4096 B image and retains it under `corpus/evidence/` |
| avm-le-image-genuine-marker | defer | Relies on S212/S213 (campaign-local) and on a clean Freetz-NG build; only the S214 patch re-opens. The LE-marker-is-blind claim is independently supported by §5. | admit after the rebuild is lane-retained |
| sasquatch-prebuilt-package-inventory | REFUSE stays | `sasquatch-v1.0` still amd64-only (re-verified) | both claims corrected and re-opened |
| sasquatch-unblob-compatibility | REFUSE stays | campaign-local S184–S186 | evidence imported and re-measured (round-36/38 receipts already cover the pair; a rewrite citing them would add nothing new) |
| sasquatch-unblob-avm-branch | REFUSE stays (flip path now concrete) | its "real AVM image needs a tool this host lacks" closing premise false (§4); mechanics reproduce on lane bytes (r38 probe); content fully covered by the corrected admit | folds into the corrected `avm-firmware-image-unblob` repinned to 26.6.4 |

**Minimum for the lesson `## Gate`:** ≥1 admit = `avm-firmware-image-unblob` (rewritten); ≥1 reject = `avm-image-build-blocker` (cleanest: premise falsified by an HTTP 200 + md5 match anyone can re-run) and `avm-le-variant-reachability`.

## 7. §10 id-collision check (0–3 leading spaces) — `$ART/idcheck/`

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' LANE/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' shokuknow/merge/kaidoku/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```
Input sha256: lane `SOURCES.md` `3cc33ca1…8a37` (base a2f64e1d), staged `b82d1276…0449`. reg-ids = 117 (S001–S117), staged-ids = 132 (S106–S237), **collisions = 12: S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117.** No duplicate ids inside either list. The next free lane id is S118; any staged row appended must be renumbered by document (e.g. S216→S118) and every citation re-pointed by document, not arithmetic.

**Guard proof** (`$ART/idcheck/guard-proof/`): fixture = the real registry plus one indented row `  | S200 | indented fixture row | … |` (S200 is staged but not in the registry). 0–3-space pattern → collisions S106–S117 **plus S200 (13)**; the column-zero-only pattern → only the 12 (S200 missed). A 4-space-indented row `    | S201 |` → 0 matches (outside the census clause). Guard works: nonempty on the indented collision.

## 8. Limits and housekeeping

- No REA run on any K1–K6 or held-out carrier; the only REA runs are the two LE dev carriers in §5. No REA on the real AVM image.
- No tool installed/updated (RULES.md read; unblob/sasquatch untouched). Full 39.7 MB firmware not retained (scratch deleted); retained: superblocks, chunk/command logs, stderr, fetched small sources, tarball md5.
- Wrote only under `$ART/` and this report. `unblob.log` landed in scratch (cwd) and was removed with it.
- Not verified: S183–S186, S190/S191, S197, S199–S201, S207, S212/S213 (campaign-local own-work; not rebuilt); whether the `.deb` assets satisfy unblob 26.6.4 beyond the lane's r36/r38 receipts.
