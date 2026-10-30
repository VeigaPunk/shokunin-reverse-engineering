# Assimilation adoption plan — kaidoku round 52, wave 1, seat `ScribeMergeAdopt`

Draft only. Nothing was appended to the lane; the lane tree, `corpus/`, `SKILL.md`, `PROVINCE.md`,
`plans/` and the fleet repo are untouched. Package read-only.

## 0. Scan receipt (what was read, and how the theme was narrowed)

Read (read-only):

- `/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md` — 77 staged knowledge entries,
  132 staged rows, "lane registry currently holds 105 rows; first staged id is S106" (the report's
  count is **stale** — the registry holds 158 rows; see §4).
- `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` — the 132 staged rows.
- `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/` — all 77 staged entries.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md` — the coverage map and the
  Knowledge table (the held-ground check).
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` — the registry (158 rows).
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`
  — the held LE-AVM entry (its limits decide what an assimilation may add).
- The lane's own round-36/38/39/40/41/43 lessons and spot-checks, for the standing verdicts.

Theme filter: the staged package is mostly adb / AOSP / Japanese-Chinese-native-language material —
none of it touches this round's ground. Eleven staged entries touch the SquashFS/AVM/unblob/sasquatch
theme; one (`firmware-region-vocabulary`, binwalk v3) was admitted to the lane in round 41.

## 1. Candidate ranking (every theme candidate, with the lane's standing verdict)

| # | staged entry | staged rows | subject | lane state | verdict |
|---|---|---|---|---|---|
| 1 | `avm-le-image-genuine-marker` | S212, S213, S214 | the AVM-LE format (marker `mkfs_time == bytes_used`), how the LE toolchain emits it, and why a round-12 measurement was wrong | **never admitted, never refused**; round-40 lesson deferred it explicitly for "an LE-AVM round" | **ADMIT** (narrowed, re-grounded) |
| 2 | `avm-image-extraction` | S200, S201 | a genuine AVM-BE image builds and extracts | round-39 adjudicated it the survivor, round-40 deferred it; **its evidence is already registered as lane row S126** (same tsv, same sha256 `f205807d…`) and r40/r41 hold the stronger vendor-carrier result | **REJECT** (already-held ground) |
| 3 | `unblob-sasquatch-dependency` | S106, S107 | unblob delegates SquashFS to an external sasquatch | admitted round 36 as `2026-10-26-unblob-sasquatch-dependency` (lane S110/S111) | REJECT (duplicate; round-41 already refused it again) |
| 4 | `sasquatch-unblob-compatibility` | S183–S186 | the sasquatch/unblob flag interface | refused round 36 (campaign-local evidence), round 42, round 43 | REJECT (standing refusal) |
| 5 | `sasquatch-unblob-avm-branch` | S189–S192 | the AVM branch of unblob's handler | refused round 38/40 (unpinned `unblob/main`; falsified closing premise) | REJECT (standing refusal) |
| 6 | `avm-firmware-image-unblob` | S216–S223 | AVM's own firmware carries both AVM formats | refused round 40 — headline "unblob never notices the AVM marker" falsified by the pinned handler | REJECT (falsified) |
| 7 | `avm-le-variant-reachability` | S206, S207 | the LE variant is *not* reachable | refused round 38/39 — overturned by its own package sibling | REJECT (overturned) |
| 8 | `avm-image-build-blocker` | S197–S199 | the AVM build is blocked | refused round 38/39 — the tarball **is** served (HTTP 200, md5 matches) | REJECT (falsified premise) |
| 9 | `sasquatch-prebuilt-package-inventory` | S130 | the prebuilt sasquatch Debian packages | admitted round 43 as `2026-10-27-sasquatch-release-matrix` (lane S136/S137) | REJECT (already held) |
| 10 | `sasquatch-unblob-compatibility-precondition` | S165 | the host-absence premise | refused round 36/38; premise superseded | REJECT (standing refusal) |
| 11 | `unblob-format-matrix` | S122 | unblob's 97-handler matrix | admitted round 38 (lane S116/S117) | REJECT (already held) |
| 12 | `firmware-region-vocabulary` | S109 | binwalk v3's unit of work | admitted round 41 as `2026-10-26-binwalk-v3-unit-of-work` | REJECT (already held) |

**#1 is the only entry in the theme that is neither already held nor standing-refused.**

## 2. ADMIT — `avm-le-image-genuine-marker`, narrowed and re-grounded

Staged file: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/avm-le-image-genuine-marker.md`
(staged round 13; staged rows S212, S213, S214).

### 2.1 Why it serves THIS round's ground

Round 52 promotes **LE AVM members (`hsqs`)** from Frontier to Core. "LE AVM" is a *format* name, and
the lane's registry had **no row describing it**: the round-50 entry's own limit 1 says so —
*"No registered `corpus/SOURCES.md` row cited by this entry describes an LE AVM layout — patch 101
(S243) adds only the symbol and byte order, and the uncatalogued Freetz wiki passage quoted above is
prose, not a row — so the marker is an empirical property of the four carriers and of all 28 census
rows."* The staged entry supplies exactly that missing upstream row, and the re-grounding below
confirms it at a pinned commit.

The round-52 Core row will therefore rest on a registered upstream definition instead of on prose.
The entry does **not** touch the device-accounting law (that stays with S250/S251/S252) and must not
be cited for it.

### 2.2 What the lane already holds (so the adopted entry does not restate it)

- The marker is **invisible to unblob's LE path** (`squashfs_v4_le`, argv `sasquatch -le
  -no-exit-code -f -d …`, marker or not) — held in `2026-10-28-r50-avm-le-squashfs-core.md`
  ("The marker is a constant of the pinned bytes, not a proof of origin"), with the pinned handler
  row S245.
- The marker is **re-stampable** and is not a proof of origin — same entry, same section.
- The `AVM_LE`/`AVM_BE` symbols and the byte order they select — lane row **S243** (the package's
  staged S206 is the same document; **no new row is needed**, and none is proposed).
- The BE layout, the BE handler branch and the BE extraction — r38/r39/r40/r41 entries, rows
  S112/S114/S121/S124.

The adopted entry therefore adds **only** the upstream definition of AVM-LE, the upstream writer-side
mechanism, the LE toolchain recipe that produces it, and one build-method lesson — and cites the
held rows for everything else.

### 2.3 The Gate — sources re-opened by this seat (all fetched 2026-10-30, into scratch only)

Receipts: `receipts/gate-receipts.txt` (exact command, exit code, stdout sha256, UTC time).

| row | document | bytes | sha256 | located quote (≤25 words) |
|---|---|---|---|---|
| S253 | `docs/make/README.md` @ `86c23d9` — the `squashfs4-le` entry, lines 573-574 | 85 254 | `1147751130102031452a39cf2736c400da277038c0807a93b34f4e09ff906b4b` | "The only difference of this format to the original LE format is that the value of the mkfs_time superblock field is equal to the bytes_used field." |
| S254 | `tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch` @ `86c23d9` | 1 601 | `9af3b3debee9f6a144c03411a439e51f4ba4f9a1bd3aaac6b8760fa9394193f8` | "-no-mkfs-time\t\tuse AVM format (length instead of timestamp)" |
| S255 | `tools/make/squashfs4-host-be/patches/550-mkfs_time__AVM_BE_AVM_LE.patch` @ `86c23d9` | 1 080 | `603c36c9e610a4f1a41548d167b7b984c8c7ac587c73fa5b19d1484d2aab15a7` | "is not available because of modified AVM-format (mkfs_time == bytes_used)" |
| S256 | `tools/make/squashfs4-host-le/squashfs4-host-le.mk` @ `86c23d9` | 2 622 | `6d2abb494ac23d9d50dcf88d6b739b0af9eb31568ab3442cf9cb278da0f8f799` | `EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_LE -DAVM_FORMAT_AS_OPTION"` |
| S257 | `tools/make/squashfs4-host-le/patches` @ `86c23d9` — a **git symlink** | 28 | `6008eb3fb4b859f6ea530c0d442aaaa1c7c9f76975377d9a2d2cef1873b10479` | `../squashfs4-host-be/patches` |
| S258 | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv` (campaign-local) | 940 | `523637c885bb50c6d445bb096f247b9a66ab33633cae46af18be4a3d4c1b9ffa` | "upstream_unsquashfs_stat: Creation or last append time is not available because of modified AVM-format (mkfs_time == bytes_used)" |
| S259 | `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-stale-build.tsv` (campaign-local) | 964 | `4c962bacd24af8132f31ce78c8e8ddf03d501f221f3590ef6bd69beafb339951` | "make_output_on_changed_define: 'mksquashfs' is up to date.  'unsquashfs' is up to date." |
| S260 | `tools/make/squashfs4-host-be/patches/250-mksquashfs__AVM_BE.patch` @ `86c23d9` | 2 775 | `f5964ad9bf2d24d319763e28f78bd441cd1d683d087e9b2e7bcd77d1db1b908d` | `#if TARGET_FORMAT == AVM_BE` (2 occurrences, patch lines 7 and 55) |

Recheck commands (each verified on 2026-10-30 — every count below is the observed output, not merely written):

```
curl -fsSL 'https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/docs/make/README.md' | grep -c 'the value of the mkfs_time superblock field is equal to the bytes_used field'   # -> 1
curl -fsSL '…/tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch' | grep -c 'use AVM format (length instead'                                                                                              # -> 1
curl -fsSL '…/tools/make/squashfs4-host-be/patches/550-mkfs_time__AVM_BE_AVM_LE.patch' | grep -c 'modified AVM-format (mkfs_time == bytes_used)'                                                                                  # -> 1
curl -fsSL '…/tools/make/squashfs4-host-le/squashfs4-host-le.mk' | grep -c 'DTARGET_FORMAT=AVM_LE -DAVM_FORMAT_AS_OPTION'                                                                                             # -> 1
curl -fsSL '…/tools/make/squashfs4-host-le/patches' | grep -c 'squashfs4-host-be/patches'                                                                                                                   # -> 1
grep -c -F 'modified AVM-format' /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv                                                                                            # -> 1
grep -c -F 'up to date'         /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/lead2-stale-build.tsv                                                                                              # -> 1
grep -c 'TARGET_FORMAT == AVM_BE' <(curl -fsSL '…/tools/make/squashfs4-host-be/patches/250-mksquashfs__AVM_BE.patch')                                                                                             # -> 2
```

### 2.4 Corrections applied to the staged text (the L1 must accept or rewrite these)

- **c1 — pin the commit.** The staged row S220 cites `…/freetz-ng/master/docs/make/README.md`
  (unpinned `master`; the lane's own rule and every round-36+ refusal treat a floating ref as a
  refusal ground). The adopted row cites commit `86c23d96d76585825fa81b5cb29105e9d2ad6654` and the
  digest `11477511…`. The paragraph moves from "line 674" (master) to **lines 573-574** (pinned).
- **c2 — the patch's location, stated precisely.** The staged text reads as if `613-…patch` were an
  LE-toolchain file. It lives in `tools/make/squashfs4-host-be/patches/`; the LE recipe reaches it
  through the **git symlink** `tools/make/squashfs4-host-le/patches → ../squashfs4-host-be/patches`
  (S257). Without S257 the citation is a mis-grounding — the round-39 critic's `avm-*` refusals were
  exactly of this kind.
- **c3 — "the marker is invisible to unblob" is scoped and cited, not restated.** It is held in the
  r50 entry; the adopted entry states it as a consequence of the pinned LE handler (S245) and marks
  it *held*, with the staged text's `:30` claim replaced by the scoped sentence.
- **c4 — the caveats at the staged entry's `:55-56`** ("does not say unblob *recognises* the AVM
  marker", "says nothing about a real Fritz!Box firmware image") are replaced: the marker-blindness
  is now scoped to the LE path by source (S245) and to the carriers by the r50 entry, and the
  real-firmware sentence is superseded by the round-50/51 measurements on four chain-pinned vendor
  members.
- **c5 — the device list is illustrative, not the class definition.** Upstream names "some cable
  boxes, e.g. 6490, 6590 (x86 core only)". The round-50 census found the marker on 28 LE members
  across **16 models**, and two of the four round-52 carriers (7581, 7582) are **not** cable boxes.
  The row therefore teaches the *format*, not a device population; the Core row must not say "AVM-LE
  is the cable-box format".
- **c6 — the campaign-local evidence is scoped.** S258/S259 point at files under the shokuknow
  campaign tree, which the lane does **not** retain (QUALITY #1). They are registered as own-work
  rows with the absolute path **and** the sha256, following the lane's own precedent **S126**
  (`lanes/kaidoku/round11/work/lead1-avm-image.tsv`, sha256 `f205807d…`). The entry's published
  claims rest on S253–S257; the campaign-local rows carry the two measurements only.

### 2.5 What the adopted entry does **not** claim

- It does not claim that unblob, REA or sasquatch recognises AVM (held: r50; source: S245).
- It does not claim that the marker proves AVM provenance (held: r50 — the marker is re-stampable).
- It does not claim any extraction outcome; no vendor byte was fetched and no REA run was made.
- It does not support the device-accounting law (S250/S251/S252) and must not be cited for it.
- It does not generalize the LE class to every LE SquashFS body: `mkfs_time == bytes_used` is the
  *only* difference from stock LE (S253), so a stock LE body without the marker is not AVM-LE.

## 3. REJECT — the next-best candidate (#2) `avm-image-extraction` (staged S200/S201)

**Reason: already-held ground (a restating entry).**

- The staged entry's only evidence rows, S200/S201, name
  `lanes/kaidoku/round11/work/lead1-avm-image.tsv`. The **lane already registers that very file as
  its own row S126** (source: `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv`,
  sha256 `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0`) — re-verified today:
  the file on disk still hashes to `f205807d…`. The staged measurement is therefore already in the
  lane's registry and in `2026-10-26-r40-avm-be-squashfs-core.md`.
- The staged claim ("a real AVM-BE image extracts") is **strictly weaker** than what the lane holds:
  r40/r41 measured the same AVM-BE layout end-to-end on **four real vendor carriers** (FRITZ!Box
  6490 Cable 07.57, 6820v1 07.30, 5490 07.31, 5491 07.31) with the oracle, the gaps and the argv.
- It is also **off this round's surface**: AVM-**BE** is the round-41 layout; round 52's class is
  AVM-**LE** (`hsqs`).
- The round-39 adjudicator's own verdict ("admissible but not this round", "not cheap for this
  round") stands; the round-40 lesson's `avm-image-build-blocker` and `avm-le-variant-reachability`
  refusals are unaffected.

**Flip condition:** a *new* upstream document about the BE recipe that the lane lacks, or a lane-built
genuine AVM-BE image retained under `corpus/evidence/` (the round-39 scout's own condition), with the
image's digest re-verified.

## 4. Id-collision analysis

Command (the campaign addendum's guard, run over both files):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md      -> reg-ids       (158)
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <pkg>/SOURCES.append.md        -> staged-ids    (132)
comm -12 reg-ids staged-ids                                                -> collisions     (44)
```

Artifacts: `receipts/collision/{reg-ids,staged-ids,collisions}`.

**Findings**

1. Registry ids: **158 rows**, ids `S001–S149` (contiguous) **plus** `S243–S251` (contiguous).
   `S150–S242` (93 ids) are **unused**. Max id `S251`.
2. Staged ids: **132 rows**, `S106–S237`, contiguous (no gaps).
3. Collisions: **44** — exactly `S106–S149`. The staged ids `S150–S237` do **not** collide with the
   registry today, because they fall in the lane's free band.
4. **Guard soundness:** every registry row is indented by exactly **2** spaces, and a permissive
   extractor (`grep -oE '\|[[:space:]]*S[0-9]{3,}'`) finds the same 158 ids — **0** rows missed by the
   0–3-space guard. The round-43 concern about the guard missing indented rows does not bite at this
   registry.
5. **The silent hazard the counts hide:** 88 staged rows sit in the lane's free band `S150–S242`.
   Appending them as-is would put *campaign* ids into the lane registry; the next package refresh can
   reuse `S150–S237` for **different documents**, so the collision would appear later and silently.
   The lane's rule is to continue its **own** S-space, so every staged id is renumbered.
6. **Reserved id:** the round-52 claims reserve **S252** for the man7 `mknod(2)` row that C1's entry
   cites ("C1's entry cites the round-52 SOURCES row S252 … opened this round by the L1 and a
   scout"). The adoption therefore continues at **S253**. If the L1 opens further rows in round 52,
   it must shift the ids below by the same offset — the map below is by **document**, not by count.

### 4.1 Renumber map (by document — the URL/anchor is the evidence)

| staged id | staged document | → lane id | why this id (by document) |
|---|---|---|---|
| S220 | Freetz-NG `docs/make/README.md` § `squashfs4-le` @ `86c23d9` | **S253** | the AVM-LE format definition — the row the round-50 entry says is missing; first free id after the reserved S252 |
| S214 | Freetz-NG `613-avm_format_as_option.patch` @ `86c23d9` | **S254** | the writer-side mechanism (the marker as an option) |
| — (new) | Freetz-NG `550-mkfs_time__AVM_BE_AVM_LE.patch` @ `86c23d9` | **S255** | the code that writes the marker and the reader diagnostic that names it |
| — (new) | Freetz-NG `tools/make/squashfs4-host-le/squashfs4-host-le.mk` @ `86c23d9` | **S256** | the LE toolchain recipe (defines, source md5, installed binary names) |
| — (new) | Freetz-NG `tools/make/squashfs4-host-le/patches` @ `86c23d9` (symlink) | **S257** | the proof that the LE recipe applies the BE patch set (makes the S254 citation sound) |
| S212 | campaign-local `lead2-avm-le-genuine.tsv` | **S258** | the one host measurement of a built AVM-LE image (own-work, absolute path + sha256) |
| S259 | campaign-local `lead2-stale-build.tsv` | **S259** | the stale-build isolation (own-work, absolute path + sha256) |
| — (new) | Freetz-NG `250-mksquashfs__AVM_BE.patch` @ `86c23d9` | **S260** | the `#if TARGET_FORMAT == AVM_BE` guard that keeps the big-endian layout out of the LE build |
| S206 | Freetz patch 101 (`AVM_LE`/`AVM_BE` symbols) | **S243 (already in the lane)** | the same document is already registered — cite S243, append nothing |

Rows S255–S257, S259 and S260 are *supporting*: the L1 may drop them and keep the entry on
S253/S254/S256/S258. If any is dropped, close the ids up so the appended block stays contiguous.

### 4.2 The `used-by` pointer correction the L1 must record

The package points staged **S220** at `corpus/knowledge/avm-firmware-image-unblob.md` — an entry the
lane **refused** in round 40 (falsified headline). The adopted entry takes S220 instead; record this
in the same style as the package's own "used-by pointers corrected at packaging time" section, and do
**not** leave S220 pointing at the refused entry.

## 5. Scratch transformation — the normalized 11-column row

Delivered in `sources-rows.md` (eight rows, one per document, in the registry's 11 columns:
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`).

Rules applied: ISO date in `opened`; **no pipe character in any cell** (checked — the URLs and quotes
contain none; the S255 anchor states the upstream C guard as "AVM_BE or AVM_LE" because the source's
`||` would break the table); `used-by` = the adopted entry path
`corpus/knowledge/2026-10-30-r52-avm-le-format.md`; `status` = `mined`; the **`recheck` cell carries
the bare cadence `180d` only** — the census validator's rule is
`recheck !~ /^[0-9]+d$/ && !symbolic(recheck)`, and prose in that cell is **E09**. The ISO date of the
run (2026-10-30), the exact command and the observed count for each row live in the adopted entry's
`recheck:` header and its `## Gate` block, as the lane's 158 committed rows do.

**Census gate, run and closed (2026-10-30).** Scratch mirror of the lane tree at HEAD
(`git archive HEAD | tar -x`), the eight rows inserted **after the last registry row** (the S251 row,
line 164 — appending at EOF raises 8 × **E12** "row outside Registry section"), the entry staged at
`corpus/knowledge/2026-10-30-r52-avm-le-format.md` so the `used-by` E11 clause can clear, then
`scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → **exit 0**, **0** error
codes, the lane's known **19** W04 duplicate-URL warnings and nothing else. Receipt:
`receipts/census-mirror.txt` (command, exit code, output sha256, full output) and
`receipts/census-after.txt`.

**Defect found and fixed (sibling `SentSecrets-2`, 2026-10-30).** The first draft put prose in the
`recheck` cell; the sibling's scratch-mirror census run exited **1** with **8 × E09** on S253–S260
while the lane baseline alone exited 0. The fix is the bare cadence above; the seat's own re-run after
the fix is the exit-0 receipt in `receipts/census-mirror.txt`. Evidence:
`.ufo/waves/round-52/w1/SentSecrets/receipts/census-sibling-rows-S253-S260.tsv`.

**Independent re-verification (sentinel `SentSecrets-2`, 2026-10-30).** On its own scratch mirror
(rows sha256 prefix `beb6c67d703ab0da`, all 12 pipes, `recheck='180d'`, inserted after the last
registry row): `validate --file … --today 2026-10-30` → exit 0, 0 error codes, `ok` + 19 W04 (stdout
sha256 `d8d9e092508d9ce2…`); the same rows appended at EOF → exit 1 with 8 × E12, reproducing the
placement rule. Their finding F1 is **CLOSED**; the credential re-scan of this seat's ten files is
clean (`live_hits 0`, `placeholder_hits 0`).

**Path convention the L1 must keep if it edits the two own-work rows (S258/S259).** The merge
package's own staged rows cite those artefacts by the **relative** form
`lanes/kaidoku/roundN/work/…`, which does **not** resolve in this lane (there is no `lanes/` directory
here). My rows cite the **absolute** existing path
`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/<file>` plus its sha256 — the lane's own
precedent in row S126. The sentinel digest-verified both files on disk against my pinned digests
(`523637c885bb50c6…`, 940 B and `4c962bacd24af813…`, 964 B): both match, both exist. Do not shorten
these two paths back to the package's relative form.

## 6. Landing edits the L1 must make (drafts only — this seat appends nothing)

1. `corpus/knowledge/2026-10-30-r52-avm-le-format.md` — the transformed entry text (`entry.md`).
2. `corpus/SOURCES.md` — the rows from `sources-rows.md` (S253–S259, or the trimmed set).
3. `corpus/README.md` — a coverage-map row and a Knowledge-table row for the new entry.
4. `PROVINCE.md` — a dated round-52 note. **Do not** let it duplicate or contradict the C1 claim's own
   `## Round-52 additions to Core` section; the assimilation entry is adjacent ground, not the Core
   row itself.
5. `corpus/lessons/round-52.md` `## Mistakes` — the stale-build lesson (class · evidence · captured-by ·
   fix), if the L1 wants it mined. The fix "assert the rebuilt binary's digest changed" counts only
   once shown able to fail; the measured evidence is in S259 (`make` said "up to date" and the digest
   was unchanged).
6. **Scratch-mirror census gate before the first append** (the round-36 precedent):
   `scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` must exit 0 on a scratch
   mirror of `corpus/` carrying the new rows and the new entry. The lane's own note: a mirror of
   `corpus/` alone fails E11 on rows citing files outside `corpus/`, so copy the cited files first.
   **This seat ran that gate** on 2026-10-30 and it is closed: exit 0, 0 error codes, 19 W04
   (receipt `receipts/census-mirror.txt`). Two placement rules the L1 must keep: the rows go **after
   the last registry row** (EOF appends raise 8 × E12), and the `recheck` cell holds a **bare
   cadence** (prose raises E09).

## 7. Limits of this plan

- No REA run, no vendor byte fetched, no lane file written (contract: the L1 alone runs REA).
- The two campaign-local rows are **not** lane-retained bytes; the entry's published claims rest on
  the five pinned Freetz-NG documents.
- The re-grounding re-opened only the documents the staged entry cites (plus the LE recipe and the
  marker patch, which the staged entry's mechanism claim needs). It did **not** re-derive the
  round-50/51 measurements, which stand as committed.
- `considerthese/` does not exist in this lane (checked: the path is absent from the tree and the
  worktree) — one report line, per the claims.
- The `S150–S242` free band is **not** proposed for use: those ids belong to the campaign space and
  are the next package refresh's collision hazard.
