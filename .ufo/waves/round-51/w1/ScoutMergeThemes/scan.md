# ScoutMergeThemes — round 51 wave 1 — merge-package scan (read-only)

Seat: `ScoutMergeThemes` · lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Package (read-only, never written): `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`
(`MERGE-REPORT.md`, `MERGE-REPORT.json`, `SOURCES.append.md`, `knowledge/corpus/knowledge/*.md`)
Receipts for every command below: `.ufo/waves/round-51/w1/ScoutMergeThemes/receipts.tsv`
and `receipts-candidates.tsv` (exact argv, exit code, stdout sha256, UTC).

**No URL was fetched.** Adoption re-grounds in-round; this scan only reads the staged bytes
and the lane's committed ground.

---

## 0. What this round's ground is (the filter I applied)

From `plans/round-51-claims.md` (read 2026-10-30):

- **R51-C1** — re-freeze the AVM LE SquashFS **gap-accounting law** from a per-carrier-class
  derivation; the law is that an unprivileged extraction creates regular files, directories and
  symlinks but **no device nodes / fifos / sockets** and emits **no gap record** for them, so a
  char-device oracle entry must carry **no disposition at all**; the class split (Cable class =
  1 char-device, FRITZ!Box class = 13) is a property of the carriers' device census, not of the
  rule. Target: LE AVM members (`hsqs`) Frontier → Core.
- **R51-C2** — triage table **v6**: the ddwrt FAILED no-pad body `dmg_Z3_v3ddwrt_inode_table`
  must stop routing `legacy-body-failure`/`cross-read-legacy`, because the ddwrt family has no
  validated second reader; plus the registry-census re-derivation (`census_outside` 13 → 0).

So the filter is: **SquashFS extraction/variants, AVM firmware, device nodes, padding,
unsquashfs / sasquatch / unblob behaviour, firmware formats** — and only entries whose subject
could carry ground for *this* round's two claims.

### The scan's decisive negative finding (read this first)

| grep over `SOURCES.append.md` (132 staged rows) | hits |
|---|---|
| `device node\|mknod\|char.?device` | **0** |
| `no-pad\|nopad\|padding` | **0** |
| `ddwrt` | 1 (row S122 — already assimilated, see C‑3) |

The claims file states C1's entry cites "the **unsquashfs/squashfs-tools device-node source
row(s) registered this round** (the law's primary grounding)" and C2's block cites "the
**squashfs-tools `-no-pad` / padding source row registered this round**".
**The package contains neither.** Both rows must be opened in-round by the L1's source-open
seats; the package can supply *no* part of C1's law grounding and *no* part of C2's padding
grounding. What the package *does* carry for this round is the **AVM-LE marker's provenance**,
which the round-50 entry explicitly recorded as unregistered prose — and which R51-C1's
Frontier → Core promotion needs as a registered source.

### Row-id hazard (the L1 must not append the package verbatim)

The package's staged ids run **S106–S237**. The live lane registry holds **156** rows,
max id **S249**, and the ids **S106–S149 (44 of them) are already taken by different
documents** — e.g. package `S112` is the Apktool README while lane `S112` is the unblob
SquashFS handler; package `S124` is the kernel `elfcore.h` while lane `S124` is the
Freetz‑NG AVM‑BE reader patch; package `S130` is the sasquatch release page while lane
`S130` is the unblob SquashFS fixtures; package `S145` is a 看雪 census while lane `S145`
is the Stanford Encyclopedia of Philosophy. Lane ids **S150–S242 are free** (93 free below
max). The lane's own precedent (rounds 35 and 38) is to **renumber by document**, never to
append staged ids: `2026-10-26-unblob-format-matrix.md` records "staged as package S122,
renumbered by document". **Recommendation: open fresh rows with fresh ids (S250+) opened
2026-10-30, and cite the staged id in the row's scope cell** — do not reuse a staged id.

---

## 1. Candidate 1 — `corpus/knowledge/avm-firmware-image-unblob.md` (round 14)

- **Target path:** `corpus/knowledge/avm-firmware-image-unblob.md`
  (package copy: `merge/kaidoku/knowledge/corpus/knowledge/avm-firmware-image-unblob.md`)
- **Round:** 14 · kind new-file · `duplicate_target: false` · `collides_with_existing: false`
- **Source citations and row ids (in `SOURCES.append.md`):**

| row | source | kind/tier | what it carries |
|---|---|---|---|
| **S216** | `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/` | docs / A | published identity + size of the 6490 Cable firmware image (39 741 440 B) |
| **S217** | `…/other/fritz.os/info_en.txt` | docs / A | `Product:` / `Version:` / `Release date:` → FRITZ!Box 6490 Cable, FRITZ!OS 7.57, 04.09.2023 |
| **S218** | `lanes/kaidoku/round14/work/lead2-avm-firmware-superblocks.tsv` | own-work / A | x86 member `hsqs` LE 4.0 xz, `mkfs_time 28200029 == bytes_used 28200029`; sibling `sqsh` BE, `5442392 == 5442392` |
| **S219** | `lanes/kaidoku/round14/work/lead2-avm-firmware-unblob.tsv` | own-work / A | unblob: `squashfs_v4_le` + `sasquatch -le -no-exit-code -f -d` (6 912 files) and `squashfs_v4_be` + `sasquatch-v4be -no-exit-code -f -d` (2 942 files) — 9 877 total; the marker is invisible to unblob |
| **S220** | `https://raw.githubusercontent.com/Freetz-NG/freetz-ng/master/docs/make/README.md` § `squashfs4-le`, paragraph at line 674 | docs / A | **the upstream AVM‑LE definition**: "AVM‑LE is the format used by AVM to pack the filesystem of some cable boxes, e.g. 6490, 6590 (x86 core only)" and "The only difference of this format to the original LE format is that the value of the mkfs_time superblock field is equal to the bytes_used field" |
| **S223** | `lanes/kaidoku/round14/work/lead2-avm-firmware-nmi-ti.tsv` | own-work / A | neither SquashFS member carries the NMI vector gap nor a TI checksum (939 B / 1 200 B trailing difference) |

- **One-line claim:** *AVM's own 6490 Cable firmware carries both AVM formats at once (LE `hsqs`
  and BE `sqsh`, each with `mkfs_time == bytes_used`), and unblob reads each with the **ordinary**
  SquashFS handler — it never recognises the AVM marker.*
- **Lean: ADOPT — narrowed to S220 only.** Reasons:
  - **S220 is the one row the lane is missing and the round needs.** The round-50 LE AVM entry
    (`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, limit 1) states in its own words:
    *"No registered `corpus/SOURCES.md` row cited by this entry describes an LE AVM layout —
    patch 101 (S243) adds only the symbol and byte order, and the uncatalogued Freetz wiki
    passage quoted above is prose, not a row — so the marker is an empirical property of the
    four carriers and of all 28 census rows."* S220 is exactly that passage, in a **different and
    more stable document** (Freetz‑NG `docs/make/README.md` on GitHub, versus the lane's
    unpinned `freetz.mhampicke.de` wiki URL), and it adds the **device statement** the lane
    lacks: AVM‑LE is the format for *some cable boxes, e.g. 6490, 6590 (x86 core only)*.
    R51-C1 promotes LE AVM members to **Core**, and a Core row needs a registered source for
    what LE AVM *is* — this is that source, and it is the item the round-50 entry names as its
    own debt.
  - **Verified locatable:** the retained copy
    `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round14/work/freetz-ng-docs-make-README.md`
    (sha256 `dc33e1f7…c449`) carries the sentence at **line 674**; the 25-word span
    "The only difference of this format to the original LE format is that the value of the
    mkfs_time superblock field is equal to the bytes_used field" is **contiguous**, **25 words
    exactly** (`wc -w` → 25), span sha256 `a5093b0f3f0042bd8eab5a3ef2b97e82bfd8245c4f959fb75943cdd6d2adf4f3`
    — QUALITY #42 compliant; the package's own recheck `grep -c -F 'AVM-LE is the format used
    by AVM to pack the filesystem of some cable boxes' …` → **1** (ran 2026-10-24, re-ran here
    2026-10-30 → 1).
  - **S216 / S217 / S218 / S219 / S223: REJECT as restating held ground.** The 6490 Cable
    vendor identity is already lane rows (S125, S244, S249 — the same `download.avm.de`
    listing and `info_en.txt`); the LE member's superblock and `bytes_used` are already in the
    round-50 carrier manifest (`tools/round-50/carriers.json`, `c6490`: member
    `./var/remote/var/tmp/x86/filesystem.image`, `bytes_used` 28 200 029) and in the frozen
    oracle tables; the unblob LE argv is already lane row **S245** (unblob 26.6.4
    `squashfs.py:53-54`) and the round-50 entry's "What REA does with a carrier"; and the NMI/TI
    question is off this round's claim surface. Rejecting them is the lane bar
    (`corpus/README.md` — already-held ground), not a defect in the package.
  - **Caveat the L1 must carry:** S220 is pinned to `master` (unpinned branch) and the round-50
    entry's own citation is an unpinned wiki URL. The lane's other Freetz‑NG citation (S124) is
    **commit-pinned**. Adopting S220 should therefore mean opening a **fresh, commit-pinned**
    row this round (QUALITY #45's `claim_row` rule: the row must be opened in the round, listed
    in the round lesson's `## Gate`, and status `mined`), with the staged id recorded in the
    scope cell.

## 2. Candidate 2 — `corpus/knowledge/avm-le-image-genuine-marker.md` (round 13)

- **Target path:** `corpus/knowledge/avm-le-image-genuine-marker.md` (package copy under
  `merge/kaidoku/knowledge/corpus/knowledge/`)
- **Round:** 13 · kind new-file · no duplicate, no collision
- **Source citations and row ids:**

| row | source | kind/tier | what it carries |
|---|---|---|---|
| **S212** | `lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv` | own-work / A | a lane-built AVM_LE image: `hsqs` LE 4.0 xz, `mkfs_time 361 == bytes_used 361`; unblob `squashfs_v4_le` + `sasquatch -le -no-exit-code -f -d`, all 4 files extracted |
| **S213** | `lanes/kaidoku/round13/work/lead2-stale-build.tsv` | own-work / A | a changed `-D` define does **not** trigger a rebuild: `make` says "'mksquashfs' is up to date." and the binary sha256 is unchanged across the rebuild |
| **S214** | `https://raw.githubusercontent.com/Freetz-NG/freetz-ng/86c23d96d76585825fa81b5cb29105e9d2ad6654/tools/make/squashfs4-host-be/patches/613-avm_format_as_option.patch` | code / A | **the upstream mechanism of the AVM marker**: `int use_standard_mkfs_time = TRUE;` under `#ifdef AVM_FORMAT_AS_OPTION`, the guarded assignment `if (!use_standard_mkfs_time) sBlk->mkfs_time = (int) sBlk->bytes_used;`, the argument `-no-mkfs-time` setting `use_standard_mkfs_time = FALSE`, and the help line "use AVM format (length instead of timestamp)" — i.e. in this variant the standard timestamp is the default and the strict AVM format is opt-in, the opposite of the plain Freetz recipe |

- **One-line claim:** *a genuine AVM_LE image **is** reachable through the lane's recipe, and the
  round-12 finding that it was not came from a stale build tree — while the upstream Freetz‑NG
  patch shows the AVM marker is an **option** (`-no-mkfs-time`), not the format itself.*
- **Lean: ADOPT — narrowed to S214 only; REJECT S212 and S213.**
  - **S214 is genuinely new to the lane and complements S243.** The lane's round-50 entry says
    patch 101 (S243) "adds the symbol and byte order and nothing else — no LE marker, no LE
    layout text"; S214 is a **different document** (Freetz‑NG `613-avm_format_as_option.patch`
    at commit `86c23d9`) that carries the **marker mechanism itself**: `mkfs_time` is written
    with the *length* instead of a timestamp. That is the upstream, code-level reason the
    carrier superblocks read `mkfs_time == bytes_used`, and it is the ground a Core row for
    "LE AVM members" wants beside S243. Verified locatable: the retained copy
    `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/613.patch`
    (sha256 `9af3b3de…93f8`) matches
    `use_standard_mkfs_time|no-mkfs-time|mkfs_time = \(int\) sBlk->bytes_used` → **6** hits;
    the package recheck `grep -c -F 'use_standard_mkfs_time' …` → 3 (re-ran 2026-10-30, same
    file, still present). Lane check: `grep -c 'avm_format_as_option' corpus/SOURCES.md` → **0**
    (exit 1) — the lane holds **no** row for this document.
  - **S212: REJECT** — the lane's r40/r41 AVM entries and S124/S126 already hold the AVM-marker
    end of the ground, and round 51's carriers are **vendor** images, not lane-built ones; a
    lane-built-image measurement is not this round's surface. **S213: REJECT** — a generic
    build-hygiene lesson (stale `make` tree), off this round's claim surface and already
    covered by the lane's own build-hygiene discipline.

## 3. Candidate 3 — `corpus/knowledge/sasquatch-unblob-avm-branch.md` (round 9) — **REJECT**

- **Target path:** `corpus/knowledge/sasquatch-unblob-avm-branch.md`
- **Round:** 9 · kind new-file
- **Source citations and row ids:**

| row | source | kind/tier | what it carries |
|---|---|---|---|
| **S189** | `https://raw.githubusercontent.com/onekey-sec/unblob/main/python/unblob/handlers/filesystem/squashfs.py` | code / A | unblob's v4-BE branch appends `-be` **only when** `header.bytes_used == header.mkfs_time` is false |
| **S190** | `lanes/kaidoku/round9/work/lead2-avm-branch.tsv` | own-work / A | the AVM branch is selected solely by the superblock equality; on the probe the argv is `sasquatch-v4be -no-exit-code -f -d` (the `-be` is gone) |
| **S191** | same TSV | own-work / A | the branch fails loudly: "…of a different endianess" then "FATAL ERROR: File system corruption detected" |
| **S192** | `https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt` | docs / A | AVM‑BE is a non-standard SquashFS4 BE format used by AVM since Fritz!OS Labor 6.35, compression hardcoded to XZ, `mkfs_time` holds "the same value as the super-block field 'bytes_used'" |

- **One-line claim:** *unblob's v4-BE AVM branch is reachable and its signature is the **absence**
  of the `-be` flag — the AVM case is signalled by a missing argument, and it fails loudly rather
  than mis-extracting.*
- **Lean: REJECT — restating held ground.** Reasons, all verified against the lane:
  - S189 is the **same upstream file** the lane already holds at the 26.6.4 tag as **S112**
    ("unblob SquashFS handler at tag 26.6.4") and again as **S245** (`SquashFSv4LEHandler`,
    the `is_avm` test at `:48`); the staged row is the same text at an unpinned `main` branch —
    a weaker pin, not new ground.
  - S192 is the **same document** the lane already holds as **S114** (Freetz
    `AVM-BE-format.txt`, with the identical `mkfs_time`/`bytes_used` sentence quoted at
    lines 13-14).
  - S190/S191 are own-work rows from the shokunnow round-9 tree whose substance the lane
    already measured directly: the "different endianess" and "File system corruption detected"
    strings are present in the lane's own committed round-40/41/42 oracle logs
    (`corpus/evidence/round-42/c1/*/oracle-run.json`), and the AVM branch's behaviour is
    settled in `2026-10-26-r40-avm-be-squashfs-core.md` and `2026-10-26-r41-avm-be-squashfs-core.md`.
  - Note also the *reverse* of the point that matters for round 51: unblob's `is_avm` test sits
    **only inside the big-endian v4 branch** (S245 `:48`), so for LE the marker changes nothing —
    the lane already holds this in S245 and the round-50 entry restates it. Nothing here moves
    C1 or C2.

---

## 4. Screened-out entries (subject-adjacent, one-line verdict each)

| package entry | round | rows | verdict for this round |
|---|---|---|---|
| `unblob-format-matrix.md` | 2 | S122 | **REJECT — already assimilated**: lane row **S116** + `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (round 38: "staged as package S122, renumbered by document"). The package's single `ddwrt` hit lives in this row. |
| `unblob-sasquatch-dependency.md` | 1 | S106, S107 | **REJECT — already assimilated**: `2026-10-26-unblob-sasquatch-dependency.md` (round 36), lane S110/S111/S117. |
| `sasquatch-unblob-compatibility.md` | 8 | S183-S186 | **REJECT — held ground**: lane S112/S121 (handler argv, `-be`), S110/S111 (READMEs), and the sasquatch 4.5.1 / unblob 26.6.4 pairing measured in the round-36/38/39 entries; the `ExtractorDependencyNotFoundReport dependencies=['sasquatch']` refusal is already in `2026-10-13-r4u-03-unblob-extract.md` and the r36 entry. |
| `sasquatch-unblob-compatibility-precondition.md` | 7 | S165 | **REJECT** — superseded by the package's own round-8 entry (and by lane S110/S111). |
| `sasquatch-prebuilt-package-inventory.md` | 3 | S130 | **REJECT — held ground**: lane `2026-10-27-sasquatch-release-matrix.md` (round 43, Frontier, package inventory only). |
| `avm-image-extraction.md` | 11 | S200, S201 | **REJECT — same document as lane S126** (`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv`, sha256 `f205807d…`); the round-10 build blocker it addresses is already lifted inside the package itself (round 11) and in the lane's r40/r41 entries. |
| `avm-le-variant-reachability.md` | 12 | S206, S207 | **REJECT** — S206 is the **same Freetz patch 101** the lane holds as **S243**; S207 is the round-12 own-work measurement the package's own round-13 entry overturns (stale binary). |
| `avm-image-build-blocker.md` | 10 | S197, S198, S199 | **REJECT** — a build-route blocker the package's round-11 entry resolves; the lane's r40/r41 entries already built AVM images with the same recipe and hold S124/S126. |
| `firmware-region-vocabulary.md` | 1 | S109 | **REJECT — already assimilated**: lane `2026-10-26-binwalk-v3-unit-of-work` (round 41); binwalk is out of the SquashFS claim surface. |
| `chinese-firmware-method-byte-level.md` | 2 | S126 | **REJECT** — Intel ME firmware byte-level patching; a different format family from AVM LE SquashFS. |
| `recorded-crash-size-ceiling.md`, `kernel-core-note-definitions.md` | 1, 2 | S108, S124 | **REJECT** — recorded-crash / core-note subjects, unrelated to this round. |

---

## 5. Recommended ONE theme

**Theme: *the AVM‑LE marker on LE members — upstream provenance for what AVM‑LE is and how the
marker field is produced* (admit S220 + S214; record the rejects).**

Why this and not another: it is the only theme in the 77 staged entries that (a) touches this
round's ground (AVM LE SquashFS members), (b) is **not** already held by the lane, and (c)
carries something the round **needs** — R51‑C1 promotes LE AVM members (`hsqs`) to Core, and
the round-50 entry's own limit 1 says the marker is "an empirical property of the four carriers
and of all 28 census rows" because no registered row describes an LE AVM layout. S220 (the
upstream AVM‑LE definition + the cable-box device statement) and S214 (the upstream marker
mechanism, `mkfs_time` carrying the length) are exactly the two documents that turn that prose
into registered, locatable sources, and they sit beside the lane's existing S243/S245 without
duplicating them.

Re-ground requirements the L1 should impose (QUALITY #42, #45, #18):
1. **Open fresh rows with fresh ids** (S250+), `opened 2026-10-30`, `status mined`, staged id
   recorded in the scope cell ("staged as package S220/S214"). **Do not append the package's
   `SOURCES.append.md` verbatim** — 44 staged ids (S106-S149) already name different documents
   in the live registry.
2. **Re-open and re-verify in-round** with a ≤25-word contiguous located quote and the served
   bytes' sha256. The stage's own pins are an unpinned `master` branch (S220) and a pinned
   commit (S214); prefer a commit-pinned Freetz‑NG URL for the new row, as the lane did for
   S124.
3. If the L1 instead wants the Freetz wiki URL the round-50 entry already quotes in prose,
   that is a **second** acceptable source for the same sentence — but it must then be opened,
   pinned and registered as a row of its own (the round-50 entry's own debt), and the entry's
   prose citation must be replaced by the row pointer, not left to stand in parallel.
4. Do **not** claim the marker proves AVM origin: the lane's own re-stampability experiment
   (round-50 W1) and S245 (the `is_avm` test lives only in the BE branch) forbid that. The
   adopted rows ground **what AVM‑LE is**, not **who built a given image**.

**What the package cannot do, stated plainly:** it cannot ground R51‑C1's device-accounting law
(0 rows on device nodes / mknod / char-device) and it cannot ground R51‑C2's `-no-pad` /
padding row (0 rows on padding / `-no-pad`). Those two source rows are round-51 source opens.
If the L1 records "Assimilation: none" instead of adopting S220/S214, that is defensible — but
the package's *only* contribution to this round's ground would then be zero, and the round-50
entry's registered-source debt on the LE AVM layout stays open.
