# Gate — round-40 lesson draft (`corpus/lessons/round-40.md`, `## Gate`)

Seat R40W2Lesson (leaf, wave 2). This is a **draft for the L1**; nothing in `corpus/` was written.
Revs: base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`, freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`,
measured `42c10a58cb2cae3a4a0122af35a0cf95ac718043`, tip at dispatch `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`.
Every quote below was located by this seat in the fetched bytes on 2026-10-26 (commands in
`verify.txt`, this directory); the wave-1 seats' timestamps are cited where they own the fetch.

## Sources opened this round (2026-10-26)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S123 | https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | 2026-10-26 (`w1/R40SrcReaOps.md` §1); re-opened by this seat 2026-10-26T19:28:30Z — HTTP/2 200, 5 634 033 B, sha256 `531717a0…93218e699` = the row | `const engineName = request.operation === "inspect_firmware_regions" ? "binwalk" : "unblob";` — tarball member `package/dist/firmware/FirmwareProvider.js:141` (10 words; byte-equal to the installed copy) |
| S124 | https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch | 2026-10-26T18:25Z (`w1/R40SrcFreetz.md` §2); re-opened 2026-10-26T19:28:30Z — HTTP/2 200, 2 217 B, sha256 `7f0a1b25…be1e220fc` = the row, `cmp` equal to the retained artifact | `/* block length in AVM-BE format is stored in LE order */` — patch line 35 (11 words) |
| S125 | https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/ (`info_en.txt`, `info_de.txt`, `FRITZ.Box_6490_Cable-07.57.image`) | 2026-10-26T18:18:06Z–18:18:19Z (`w1/R40SrcAvmVendor.md`); re-opened 2026-10-26T19:28:31Z — `info_en.txt` HTTP/2 200, Last-Modified `Mon, 04 Sep 2023 17:08:03 GMT`, sha256 `6c601b34…3d11070a7`; image 39 741 440 B sha256 `f518ce6b…04f9ede6d` | `Product=Fritz_Box_HW213a (FRITZ!Box 6490 Cable)` — image member `./var/content:1` (5 words; member 346 B sha256 `ab238b0e…8eca9557`); `info_en.txt:8` reads `Product:        FRITZ!Box 6490 Cable` and `:10` `Version:        FRITZ!OS 7.57` |
| S126 | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv` (sha256 `f205807d…7c8539eb0`) | 2026-10-26, re-opened (`w1/R40AssimE3.md` §1); TSV re-hashed by this seat and equal to the row | `absent - the AVM branch passes no -be` — row `unblob_be_flag`, line 17 (8 words) |

Registry: **122 → 126 rows**. S123 appended in the freeze `7fce3086`; S124, S125, S126 appended in the
landing `42c10a58`; S124–S126 all descend from the freeze. All four are tier A, status `mined`,
`opened 2026-10-26`; rechecks `180d` / `180d` / `on-release` / `180d`; kinds `code` / `code` / `dataset` /
`own-work`. No duplicate id and no gap in the registry after the append:
`grep -cE '^\| S[0-9]+' corpus/SOURCES.md` = 126, last row S126, `uniq -d` empty.

Where the four rows came from: three wave-1 source seats each drafted a provisional `S123` (REA package
`w1/R40SrcReaOps`, Freetz patch `w1/R40SrcFreetz`, vendor page `w1/R40SrcAvmVendor`), having each computed
"next free = S123" without seeing the others; the L1 resolved it by consecutive ids — S123 the REA row at
the freeze, S124 the Freetz code row, S125 the vendor dataset row — and S126 is the assimilation seat's
own-work row for the retained 4 096-byte image. S114 keeps its prose scope and its
paraphrased anchor (append-only); S124 is the code companion and does not claim to supersede it.

## Assimilation

**Admitted 1.** `avm-image-extraction.md` (`/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/`)
→ `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, re-grounded by `w1/R40AssimE3` (absolute
path + sha256 on the image, unblob 26.6.4 with handler digest `2d7b901b…9287`, `sasquatch-v4be` 4.5.1,
the verbatim argv, an explicit not-examined paragraph, and a marker × layout control matrix generated on
the seat's own bytes). PROVINCE scope holds: AVM-BE is named Frontier at `PROVINCE.md:156-157` and in the
round-39 frontier note `:384`, which is exactly the surface R40-C1 moves. Landed by the L1 at `42c10a58`
(entry present, `corpus/README.md:208` row present). It is the only AVM entry for which this round found
no falsified claim; `w1/R40Quarantine` §4 hand-checked it independently (ADOPT-WITH-ANCHOR on S200/S201).

**Refused 5**, with reason and the flip that would reverse it (`w1/R40AssimE3/gate.md`; the second
assimilation seat `w1/R40AssimReject` re-tested 3 of them and agrees):

| entry | reason | flip |
|---|---|---|
| `avm-firmware-image-unblob.md` | headline and `:75-77` ("the AVM marker is **invisible to unblob** … selects a handler on the magic and the endianness, never on the marker") are falsified four ways: the pinned handler `is_avm = header.bytes_used == header.mkfs_time` with `-be` appended only when not AVM; the entry's own argv table; three sibling entries; the committed round-39 H13/H15 envelopes. Making it admissible means retracting its own headline — a rewrite, not an in-round edit | a rewrite whose headline and `:75-79` are retracted and whose measurement rows are re-taken after the freeze |
| `avm-image-build-blocker.md` | the standing "the release is gone" is overturned (the SourceForge tarball resolves; md5 `d92ab59a…`), and `:43-44` presents a misparsed `bytes_used` of 7.85 EiB inside a 4 096-byte image as a measurement (QUALITY #5) | convert to a reversal record that names the rejected decision by path and line |
| `avm-le-variant-reachability.md` | standing "not reachable" claim overturned without a pointer by a sibling entry in the same package — a reversal laundered as prose (QUALITY #35/#36). Reject seat, from retained bytes: `avm-le-plain550.squashfs` is byte-identical to the option-build image (`18d3ad05…`, 361 == 361) | append a reversal line naming this file as the rejected decision, with the round-13 image and its sha256 |
| `avm-le-image-genuine-marker.md` | no AVM-**BE** surface: the claim is the LE variant, and its "marker invisible" sentence is true only on the LE branch. Reject seat re-tested it as **ADMIT-AFTER-REWRITE** (central claim confirmed three ways: 361 == 361, two clean rebuilds, `squashfs_v4_le` + `sasquatch -le` + 4 files) with `:30` over-generalising, `:55-56` denying a mechanism that exists, and success recorded without the exit-code caveat | admissible in a round whose claim is the LE AVM variant, after digest/path/pin additions and the `:30`/`:55-56` corrections |
| `sasquatch-unblob-avm-branch.md` | open lead "a real AVM image still needs a tool this host does not have" is stale by two rounds (the adopted entry extracts one) and it cites `unblob/main`, an unpinned branch (QUALITY #8) | append the closing sentence with the round-11 image and sha256; re-pin to tag 26.6.4 with handler digest `2d7b901b…` |

**Id-collision check** — `.ufo/waves/round-40/w1/artifacts/R40AssimE3/collision/`: `reg-ids` 122 lines,
`staged-ids` 132 lines, `collisions` **17** (`S106`–`S122`, `comm -12`), next free lane id **S123**
(`renumber-map.tsv`). Guard proved able to fail on the retained fixtures: `reg-fixture.md` holds `S001` at
column zero and `S002` indented two spaces; the 0–3-space extractor (`fx-reg` = `S001 S002`, `fx-collisions`
= `S002`) catches the collision, the column-zero-only pattern (`fx-reg-colzero` = `S001`,
`fx-collisions-colzero` = empty, 0 B) is a false green. The map's own assignment (`S200→S123`,
`S201→S124`, `S192→S125`) was then superseded by the L1: S123 went to the REA package at the freeze and
S124–S126 to the Freetz patch, the vendor page and the own-work row at the landing. Both assignments are
collision-free; the registry's final ids are the ones in the table above.

**Quarantine slice** — `w1/R40Quarantine.md`, slice file
`.ufo/waves/round-40/w1/artifacts/R40Quarantine/quarantine-slice`, 5 rows, sha256
`7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`, byte-identical to rounds 38 and 39
(`cmp`). The strict slice ∩ AVM-theme ids join is **empty**, so all five were re-opened live:

| id | verdict | ground |
|---|---|---|
| S150 | **RE-ANCHOR** (refuse the row as staged; the source is genuine) | Zenn page HTTP 200, 174 088 B; gate quote `GNU Binutils に含まれる逆アセンブラ。ほぼすべての Linux 環境に入っています。` ×2; the register's string `シンボルがない場合のヒント` ×0 |
| S113 | ADOPT-WITH-ANCHOR (21 locales + `x-default`, not "17") | adb page HTTP 200, 368 063 B; `og:description` quote ×2; `hreflang="ja"` split over two source lines |
| S117 | **ADOPT-WITH-ANCHOR — FLIP** (was unverifiable) | DOI landing HTTP 202, 0 B as before; `api.semanticscholar.org` HTTP 200 carries the gate quote verbatim |
| S136 | ADOPT-WITH-ANCHOR | `grep -c '2 of 24 verbs are'` → 1; quote spans lines 8-9, not line 8 |
| S147 | ADOPT-WITH-ANCHOR (conflict stands) | `HOST-CONTRACT.md` sha256 `ab36b310…58fe`; `207 tools` on line 41; the host pins `rea-agents@6.7.0` while the lane pins 6.5.0 |

AVM-theme hand-check beyond the join: `avm-image-extraction` ADOPT-WITH-ANCHOR (both ids); the SourceForge
path/md5, the 23-patch Freetz pin, `sqsh`/XZ/365==365 and the `squashfs_v4_be` no-`-be` extraction all
reproduce. Nothing was appended to the registry from the slice; the S117 flip is recorded for a future
assimilation round, not acted on here.

## used-by change log (old → new, all at `42c10a58`)

Only the `used-by` cell changed on each row (field-level diff base → tip: no `status`, `recheck`, `scope`,
`anchor` or `teaches` change on any of the six — CORPUS rule 2 respected).

| row | old | new |
|---|---|---|
| S112 | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md, corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md, corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md, corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` |
| S114 | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` |
| S118 | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` |
| S119 | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` |
| S120 | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md` |
| S121 | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` | `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md, corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` |

Citation check (each appended entry really cites the row): `2026-10-26-r40-avm-be-squashfs-core.md`
`source:` lines are S124, S125, S126, S114, S112, S121; `2026-10-26-r40-sqfs-triage-v2.md` `source:`
lines are S112, S118, S119, S120, S123. S107/S108 were **not** changed (the assimilation seat's draft
proposed them; the registry keeps them at the single r36 entry, so nothing claims a citation that does
not exist).

## S126 recheck prose, stripped

The registry cell keeps `180d`. The anchor's prose, with the sentences removed, is:

```
/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv
  sha256 f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0
  rows: image_path image_magic image_compression_id image_mkfs_time image_bytes_used
        image_is_avm unblob_handler unblob_be_flag extracted_files
image  lanes/kaidoku/round11/work/avm-be.squashfs  4096 B
  sha256 c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32
log    lanes/kaidoku/round11/work/unblob.log
  sha256 352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7
```

Read values, from the bytes this round: `image_path lanes/kaidoku/round11/work/avm-be.squashfs`;
`image_magic sqsh`; `image_compression_id 4`; `image_mkfs_time 365`; `image_bytes_used 365`;
`image_is_avm yes`; `unblob_handler squashfs_v4_be`; `unblob_be_flag absent`; `extracted_files
apple1.txt apple2.txt apple3.txt apple4.txt`. The log's extract-command line reads
`sasquatch-v4be -no-exit-code -f -d …` with no `-be`.

Two precision notes for the lesson text: the log carries **five** `Processing file` lines — one for the
input image and four for the published files — not four (a count the assimilation report rounded to the
published files); and the recheck pins **digests and rows only**, because the log has neither an exit
status nor a version banner. A future recheck of S126 must not be written as "exit 0".

## Calibration carried into the lesson (verified this round)

- **K-1 — an unblob exit code is not a witness of extraction failure.** `ExtractCommandFailedReport`
  declares `severity: Severity = Severity.WARNING` (`unblob/report.py:94`) and the CLI maps
  `(Severity.WARNING, 0)` in `get_exit_code_from_reports` (`unblob/cli.py:464-475`), so a run that
  published zero regular files still exits 0; the child argv also carries `-no-exit-code` (S126). A kill
  control or receipt binding must therefore be scored on published-file count plus
  `ExtractCommandFailedReport` present (or `-be` in the child argv), never on `exit != 0`. Sources opened
  this round: `w1/R40AssimReject.md` consequence 2; re-verified here against the installed unblob
  (`report.py` sha256 `2329783f…cc9ee`, `cli.py` sha256 `fc775f1a…59f86c`).
- **K-2 — the v2 table keeps the separator column.** `avm-marker-be-dropped` and `body-extractor-failure`
  differ only in the logged extractor command; the frozen table's header at `SKILL.md:363` (header row of the block opened by `<!-- sqfs-triage-table v2 -->` at `:361`) keeps
  `-be in child argv` between `dependencies` and `symlink removed`, so the reject seat's warning landed.
- **K-3 — an anchor is not repairable in place.** S114 still carries the paraphrase "`mkfs_time` field
  holds the same value as `bytes_used`" and no HTTP status, size or sha256; that is correct under
  append-only, and S124 is the code-tier companion. A future round that wants the verbatim lines 13-14
  sentence in an anchor must add a row, not edit S114.

## What these sources are, and are not

S123–S126 are **citations**, not execution evidence for R40-C1: S125 teaches vendor identity only (no
layout statement; the AVM licence forbids redistribution, so the image is cited by sha256 and lives in
scratch only); S126 is own-work on a 4 096-byte lane-built image, never a vendor carrier; S123 and S124
are code-readable statements. The carrier evidence for C1 is the committed receipts and the counter's
re-run projection, which are the C1 seats' business, not this gate's.

## Verification log

Commands and outputs are in `verify.txt`. Summary: four quotes located in bytes this seat re-fetched or
re-hashed (S123 tarball sha256 = row; S124 patch sha256 = row and `cmp`-equal to the retained artifact;
S125 `info_en.txt` sha256 = row, image sha256 = the V1 pin, `./var/content` sha256 = row; S126 TSV, image
and log sha256 = row); field-level diff of the six used-by rows shows only `used-by` changed; registry
126 rows with no duplicate; the two unblob files hashed. No carrier, no REA call, no `unblob` run, no
`sasquatch` run, no tool installed or upgraded, no VCS mutation. The vendor image was fetched into scratch
only to re-derive `var/content`; it was deleted with the scratch directory, and no vendor bytes were
copied into this lane.

## Limits

- The S123 quote is located in the tarball at the same path in the installed copy (byte-equal file); the
  full 1 574-file `dist` diff the row claims was not re-run here (tarball `grep -c '/dist/'` = 1 574).
- S125's `info_de.txt` was not re-fetched this round; the retained copy hashes to the row's `3becce79…4cdc5a1e`.
- The S126 extraction is read from the retained log, not re-run; the log has no exit status (K-1 and the
  S126 note).
- The quarantine verdicts are the quarantine seat's live fetches, read here, not re-fetched by this seat.
- [INFERENCE] Whether any C1 kill control or counter binding scores on `exit != 0` is the C1 seats'
  surface; K-1 states the rule, not a verdict on the frozen counter.
