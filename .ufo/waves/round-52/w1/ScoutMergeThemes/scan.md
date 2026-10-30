# Round-52 assimilation scan — second reader (ScoutMergeThemes)

Scope: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` (read-only; `MERGE-REPORT.md`, `SOURCES.append.md`, `knowledge/corpus/knowledge/*.md`), read independently of ScribeMergeAdopt. No cited URL was fetched. Lane held-ground checked against `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/README.md`, `corpus/QUALITY.md`.

## Package facts (receipts R1, R10, R13 in `receipts/`)

- 77 knowledge entries, 132 rows (S106..S237), matching `MERGE-REPORT.md`.
- Lane registry: 158 rows, max S251, next free **S252**. Contiguous block S1..S149 plus S243..S251.
- Numeric id collisions: **44 of 132** package ids (S106..S149) already name a different document in the lane. 88 package ids (S150..S237) are numerically free. Renumber by document, not by id.
- `considerthese/` does not exist in the lane (R14).

## Round-52 ground coverage in the package (receipts R2, R3, R4)

- Device nodes / mknod / fifo / socket: **no package ground** (R2 = 0 hits). The C1 device-accounting law has no candidate here.
- Padding / `-nopad`: **no package ground** (R3 = 1 hit, a REA evidence-graph code comment, irrelevant).
- DD-WRT / ddwrt FAILED body: **no package ground** for C2 (R4 = 2 hits, both the unblob format matrix's variant list, already held).

The candidates below are therefore AVM firmware and LE/BE marker ground only.

## Candidates (3)

### 1. `avm-le-image-genuine-marker.md`: staged rows S212, S213, S214

- **Target path:** `corpus/knowledge/` (new file; no existing lane entry).
- **Round:** round 13 (package).
- **Source citations:** S212 and S213 are own-work tsv rows (`lanes/kaidoku/round13/work/lead2-avm-le-genuine.tsv`, `lead2-stale-build.tsv`). S214 is Freetz-NG `613-avm_format_as_option.patch` at commit `86c23d96d76585825fa81b5cb29105e9d2ad6654`.
- **Claim:** a genuine AVM_LE image (`hsqs`, `mkfs_time == bytes_used` = 361) builds from the squashfs-tools 4.3 pin (md5 `d92ab59a…`) with `-DTARGET_FORMAT=AVM_LE`. The round-12 "not reachable" result was a stale-build artefact: changing a `-D` define did not trigger a rebuild, and the binary sha256 was unchanged. Freetz-NG's 613 patch makes the marker an option (`-no-mkfs-time`) rather than the default.
- **Lean: ADMIT, narrowed.**
  - Not held: `grep` for `613-avm`, `no_clean`, `stale build`, `length instead of timestamp` in the lane → 0 hits (R11-family checks). The lane has no LE marker build-provenance entry.
  - Relevance: it bears directly on the r50 claim (`2026-10-28-r50-avm-le-squashfs-core.md:60`) that the marker is "re-stampable" and that "no stock-mksquashfs invocation was run". A clean `AVM_LE` build is a second marker source, and it changes that sentence's evidence base.
  - Conditions: (a) S212/S213 are shokuknow own-work and must be re-measured in lane scratch, not copied; (b) S214 must be re-opened at the pinned commit; (c) the entry must not count toward R52-C1's four carriers (the locally built image is not a vendor carrier).
  - Renumber by document: S212→S252, S213→S253, S214→S254.

### 2. `avm-firmware-image-unblob.md`: staged rows S218, S219, S220, S223 (narrowed)

- **Target path:** `corpus/knowledge/` (new file), scoped to the two claims the lane does not hold.
- **Round:** round 14 (package).
- **Source citations:** S218 and S223 are own-work tsv rows (`lanes/kaidoku/round14/work/lead2-avm-firmware-superblocks.tsv`, `lead2-avm-firmware-nmi-ti.tsv`). S220 is Freetz-NG `docs/make/README.md` on branch `master` (unpinned).
- **Claim (narrowed to what is new):** on AVM's 6490 Cable 07.57 image, a stock SquashFS reader prints a 1970 creation date for the AVM marker. The round-13 combined-image model's NMI vector gap and TI checksum are absent: each member sits at offset 0 with trailing differences of 939 and 1200 bytes.
- **Lean: ADMIT the 1970 fingerprint and the NMI/TI negative only. REJECT the rest.**
  - Held elsewhere, so not new: "both AVM formats in one image" and "unblob handles them with ordinary LE/BE handlers" restate `2026-10-26-r41-avm-be-squashfs-core.md` (BE layout, `squashfs_v4_be`, no `-be`) and `2026-10-28-r50-avm-le-squashfs-core.md:60` (LE handler and argv, "marker invisible to unblob").
  - Not new: S216/S217 are the same directory as lane S125 (`fritzbox-6490-cable/other/fritz.os/`, `info_en.txt`, `FRITZ.Box_6490_Cable-07.57.image`).
  - Not new: the 6490 carrier byte counts and sha256s are in lane `carriers.json` and the r50 entry.
  - Not new: the 9 877-file tally (6 912 LE + 2 942 BE) is a single-run count from shokuknow own-work, with no lane held ground to attach it to.
  - Lane checks: `1970` in `corpus/knowledge/` → 0 hits relevant to AVM (R11). `NMI vector` / `TI checksum` → 0 hits (R12).
  - Conditions: S218 and S223 must be re-measured in lane scratch against the lane's own 6490 carrier pin. S220 must be re-cited at a commit before it can be used; a `master` citation is not a pin.
  - The 1970 claim rests on the stock reader's display of a field the lane holds only as a measurement, so its wording must stay "a stock reader displays", not "the marker is 1970".
  - Renumber by document (if admitted): S218→S255, S223→S256, S220→S257 (only if re-pinned).

### 3. `unblob-format-matrix.md`: staged row S122 (rejected)

- **Target path:** would duplicate the held `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (no new file).
- **Round:** round 2 (package, per `MERGE-REPORT.md` knowledge table).
- **Source citation:** S122 — `https://unblob.org/formats/`.
- **Claim:** 97 handler sections, 42 vendor-attributed, ten SquashFS variants, ZIP limit, "more than 30" vs "78+" conflict.
- **Lean: REJECT.** Restates held ground. Lane S116 is the same document (`https://unblob.org/formats/`), and the lane entry `2026-10-26-unblob-format-matrix.md` already holds every claim in the staged row. The staged file's "42 vendor-attributed entries" was already corrected in lane admission (lane entry, lines 9-14). Re-admitting it would be the "restating held ground" reject case under `corpus/README.md`.

## Also checked and rejected (not among the three)

- `unblob-sasquatch-dependency` (S106/S107): held as lane `2026-10-26-unblob-sasquatch-dependency` (S110/S111).
- `sasquatch-prebuilt-package-inventory` (S130): held as lane `2026-10-27-sasquatch-release-matrix` (S136/S137).
- `sasquatch-unblob-avm-branch` (S189–S192): held in substance by lane S112 and r40/r41 (AVM branch at tag 26.6.4). The staged S189 cites `main`, an unpinned revision, which is weaker than the lane's tag-pinned S112.
- `japanese-surface-analysis-command-set` (S132): binwalk Qiita memo, B-tier community. Not round-52 decisive; not held in the lane, so it is a candidate for a later round, not this one.

## Verdict on this round's theme

Assimilation: **one theme, AVM LE/BE marker provenance, with two candidates admitted narrowly and one rejected.** Re-grounding of the admitted rows is in-round work for the adoption step, not for this scan. No device-node, padding, or ddwrt ground exists in the package, so C1 and C2 get nothing from it.
