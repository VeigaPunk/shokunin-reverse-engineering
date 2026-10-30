# ScoutMergeThemes — round 51, wave 1 — merge-package scan (assimilation seat)

Seat `ScoutMergeThemes` · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Scan file (the deliverable): `.ufo/waves/round-51/w1/ScoutMergeThemes/scan.md`
Receipts: `.ufo/waves/round-51/w1/ScoutMergeThemes/receipts.tsv`,
`receipts-candidates.tsv` (exact argv · exit code · stdout sha256 · UTC).
Package read only; **no URL fetched**; nothing written outside this wave dir and the scratch.

## Verdict

**One theme fits; the package is otherwise redundant or off-ground.**
Recommended theme: **the AVM‑LE marker's upstream provenance on the LE members** — admit
**S220** (Freetz‑NG `docs/make/README.md` §`squashfs4-le`, line 674) and **S214** (Freetz‑NG
`613-avm_format_as_option.patch` @ `86c23d9`); record the rejects below. Open them as **fresh
rows with fresh ids (S250+), opened 2026-10-30**, not by appending the package's staged ids.

## The three findings that matter

1. **The package cannot ground either claim.** `SOURCES.append.md` (132 staged rows) has
   **0** rows on `device node|mknod|char-device` and **0** on `no-pad|nopad|padding`; its one
   `ddwrt` hit is inside row S122, already assimilated. R51‑C1's device-accounting law and
   R51‑C2's `-no-pad` padding row are therefore **round-51 source opens**, not package rows.
2. **Appending the package verbatim would corrupt the registry.** The staged id space is
   S106–S237; the live lane holds 156 rows (max S249) and **44 staged ids (S106–S149) already
   name different documents** (package S112 = Apktool README vs lane S112 = unblob SquashFS
   handler; package S124 = kernel `elfcore.h` vs lane S124 = Freetz‑NG AVM‑BE reader patch;
   package S130 = sasquatch releases vs lane S130 = unblob fixtures; package S145 = 看雪 census
   vs lane S145 = SEP). Free lane ids: S150–S242. The lane's own precedent (rounds 35/38) is
   renumber-by-document ("staged as package S122, renumbered by document").
3. **The adopt is exactly the debt the round-50 entry names.** `2026-10-28-r50-avm-le-squashfs-core.md`
   limit 1 states no registered row describes an LE AVM layout and the marker is "an empirical
   property of the four carriers and of all 28 census rows" — because its Freetz passage is cited
   as prose from an unpinned wiki URL. S220 carries that sentence in a more stable document and
   adds the device statement ("some cable boxes, e.g. 6490, 6590 (x86 core only)"); S214
   carries the upstream marker *mechanism* (`sBlk->mkfs_time = (int) sBlk->bytes_used`,
   `-no-mkfs-time`, "length instead of timestamp") in a document the lane does not hold
   (`grep -c 'avm_format_as_option' corpus/SOURCES.md` → 0). Both are locatable now: the
   retained copies give line 674 and 6 marker-mechanism hits; the S220 quote span is contiguous
   and **25 words exactly** (sha256 `a5093b0f…f4f3`), QUALITY #42-compliant.

## Candidates, with leans

| # | target | round | rows | lean |
|---|---|---|---|---|
| 1 | `corpus/knowledge/avm-firmware-image-unblob.md` | 14 | S216, S217, S218, S219, **S220**, S223 | **ADOPT S220 only.** S216/S217 = vendor identity already held (S125/S244/S249); S218/S219 = the c6490 carrier's superblock/argv already in `tools/round-50/carriers.json` + S245; S223 = NMI/TI, off-claim. |
| 2 | `corpus/knowledge/avm-le-image-genuine-marker.md` | 13 | S212, S213, **S214** | **ADOPT S214 only.** S212 = lane-built image (r40/r41 + S124/S126 already hold it); S213 = generic stale-build hygiene. |
| 3 | `corpus/knowledge/sasquatch-unblob-avm-branch.md` | 9 | S189, S190, S191, S192 | **REJECT — held ground.** S189 = same file as lane S112/S245 (unpinned `main`); S192 = same document as lane S114; S190/S191 = the "different endianess" / "File system corruption detected" strings already in the lane's committed round-40/41/42 oracle logs. |

Screened-out and rejected with one-line reasons: `unblob-format-matrix` (assimilated r38 → lane
S116), `unblob-sasquatch-dependency` (assimilated r36 → S110/S111/S117),
`sasquatch-unblob-compatibility` (held: S112/S121/S110/S111 + r36/r38/r39 + the
`ExtractorDependencyNotFoundReport` refusal in `2026-10-13-r4u-03-unblob-extract.md`),
`sasquatch-unblob-compatibility-precondition`, `sasquatch-prebuilt-package-inventory` (r43
`2026-10-27-sasquatch-release-matrix.md`), `avm-image-extraction` (same document as lane S126),
`avm-le-variant-reachability` (S206 = the same patch as lane S243; S207 overturned by the
package's own r13 entry), `avm-image-build-blocker` (resolved by the package's r11 entry),
`firmware-region-vocabulary` (assimilated r41), `chinese-firmware-method-byte-level`,
`recorded-crash-size-ceiling`, `kernel-core-note-definitions`.

## Caveats the L1 must carry

- Re-open and re-verify in-round with a ≤25-word contiguous located quote and the served bytes'
  sha256 (QUALITY #42, #45, #18). Prefer a **commit-pinned** Freetz‑NG URL for the new row, as
  the lane did for S124; the staged S220 pin is an unpinned `master` branch.
- The adopted rows ground **what AVM‑LE is**, not **who built a given image**: unblob's `is_avm`
  test sits only in the BE branch (S245 `:48`) and the round-50 W1 experiment re-stamped the
  marker on standard LE fixtures. No Core row may say "REA/unblob recognises AVM".
- If the L1 records "Assimilation: none" instead, that is defensible — but the package's
  contribution to this round's ground is then exactly zero and the round-50 entry's
  registered-source debt on the LE AVM layout stays open.
- Nothing was written into the lane tree, `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`,
  `LOG.md`, `SCORECARD.md` or the fleet repo; no git/jj mutation was run; no REA run was invoked;
  scratch `/fast/scratch/hyaku/kaidoku-r51/w1-ScoutMergeThemes` was removed after copying the
  receipts in.
