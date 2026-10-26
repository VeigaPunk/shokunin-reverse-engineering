# R36ConnAssimilationTheme — sasquatch/unblob/AVM assimilation theme map (round 36, wave 1)

Seat: connector (advisory). Date: 2026-10-26. Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Writes: this file only. No VCS mutation, no tool install/upgrade (nothing needed; read-only
work over already-installed `python3`, `curl`-free — no fetches were run by this seat).
No subagents dispatched (leaf bounds). All facts below were observed directly from the
named files unless marked [INFERENCE].

## Inputs read

- Plan: `plans/round-36-claims.md` (frozen claims; assimilation theme named there as
  `unblob-sasquatch-dependency`, `sasquatch-prebuilt-package-inventory`,
  `sasquatch-unblob-compatibility`; per-entry gate ≥1 admit / ≥1 reject; collision check
  per addendum §10 before any append).
- Merge package (read-only): `/home/vgpnk/Projects/shokuknow/merge/kaidoku/{MERGE-REPORT.md,
  MERGE-REPORT.json, SOURCES.append.md}` and `knowledge/corpus/knowledge/*sasquatch*,
  *unblob*, *avm*` (11 entries).
- Collision/registry state: `.ufo/waves/round-36/assimilation/{reg-ids,staged-ids,collisions,
  quarantine-slice, id-guard-proof/}`.
- Lane state: `PROVINCE.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`,
  `corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md` (the lane's only existing unblob
  knowledge entry), `corpus/evidence/round-36/c1/{carriers.json,K*/before.json}`.
- Sibling w1 reports (corroboration): `R36ScoutUnblobReadme.md`, `R36ScoutPrebuiltInventory.md`,
  `R36ScoutSasquatchRelease.md`, `R36ScoutUnblobHandler.md`, `R36ScoutAppImageSpec.md`,
  `R36ScoutNeovimRelease.md`.

## Registry and collision state (verified)

- Lane `corpus/SOURCES.md` holds **106 rows, ids S001–S106** (observed: `grep -oE '^\| S[0-9]+'`
  → max `S106`; S106 = GNU binutils readelf version-needs reader, round 34, opened 2026-10-25,
  `SOURCES.md:112`).
- Merge staged block: **132 rows, ids S106–S237** (`MERGE-REPORT.md`: "lane registry currently
  holds 105 rows; first staged id is S106" — that count predates the lane's own S106).
- `.ufo/waves/round-36/assimilation/collisions` = `S106` — confirmed: staged S106 (unblob
  upstream README) collides with the lane's committed S106. A naive append is impossible.
- `quarantine-slice` rows: S150 (`payload-absent`), S113, S117 (source not fetched), S136,
  S147 (no locator). **None of the 11 theme entries cites any quarantined row** (checked
  staged used-by cells).
- `id-guard-proof` fixture shows the registry/staged differencing method yields the collision.
- Renumber consequence [INFERENCE]: any admission must renumber staged ids. A full append in
  order maps staged N → lane N+1 (S106→S107 … S223→S224); any quarantine/drop changes
  offsets, so the renumber map is only computable after the admit set is final (scribe/L1
  own the map). Second-order: sibling scouts already drafted lane rows **S107** (sasquatch
  release, `R36ScoutSasquatchRelease.md`), **S108** (unblob squashfs.py handler,
  `R36ScoutUnblobHandler.md`), **S109** (neovim carrier provenance, `R36ScoutNeovimRelease.md`),
  **S110–S112** (AppImage spec/runtime/unsquashfs man, `R36ScoutAppImageSpec.md`) for the
  round-36 claim entry. If the merge block renumbers to S107+, those drafts shift; the claim
  fixes no numeric id (only "opened 2026-10-26, used-by lists the entry"), so no frozen
  predicate breaks, but L1 must sequence claim rows vs assimilation rows.

## Lane R36-C1 receipt state (overlap baseline)

- `corpus/evidence/round-36/c1/carriers.json` freezes K1 (synthetic LE v4 xz), K2 (synthetic
  LE v4 gzip), K3/K4 (neovim v0.12.6 AppImages x86_64/arm64, digests = GitHub release digests).
- Observed `K1/before.json` and `K3/before.json`: each squashfs chunk carries
  `extraction_reports[0] = {"severity":"ERROR","dependencies":["sasquatch"],
  "__typename__":"ExtractorDependencyNotFoundReport"}` and
  `extraction_gaps[0].kind = "missing-extractor-dependency"` (handler `squashfs_v4_le`). The
  frozen before-receipts encode exactly the negative control the merge campaign recorded in
  round 8.
- Host state (observed): `~/.local/bin/sasquatch` + `sasquatch-v4be` (installed by L1,
  mtime Oct 26 01:22) both report `unsquashfs version 4.5.1 (2022/03/17)`; `unblob --version`
  → 26.6.4 (uv tool). Per `R36ScoutSasquatchRelease.md`, the installed binaries are
  byte-identical (sha256) to the onekey-sec `sasquatch-v4.5.1-6` amd64 deb assets.
- Frozen claim boundary: R36-C1 does **not** claim big-endian / AVM SquashFS. No merge entry
  touches the frozen counter, predicate, carriers, or oracle (advisory seat; nothing mutated).

## PROVINCE.md scope check (theme-wide)

- In-scope: the round-4 frontier bullet **sasquatch** ("unblob's squashfs recursion extractor
  (AUR-only); 7z fallback covers the carved-image path today") and the `corpus/README.md`
  Firmware row ("AppImage SquashFS carved but recursion blocked by missing sasquatch") are
  the lane's own declared surfaces; the theme entries document that frontier's tooling,
  packaging, and one real firmware extraction. The lane's domain ("reverse engineering of
  shipped artifacts … archives and packages") covers the firmware entry squarely and the
  synthetic-image build entries by the lane's own synth-carrier practice.
- Adjacent caution: "Installing engines, Python packages, or editing client configs … all
  **operator-owned**". The round-8 campaign tsv records a campaign-side host mutation
  (`sudo pacman -S --noconfirm squashfs-tools`, `lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv`
  row `host_mutation`) — against today's operator pacman pause. Admission must carry that as
  recorded history (it is, via the campaign's REJECTIONS.md reference), never as lane precedent.
- No theme entry changes a frozen predicate; the found defects below are reported, not repaired.

## Per-entry map

S-id locality legend: **external** = upstream/vendor document fetched by the campaign;
**campaign-local** = `lanes/kaidoku/round*/work/*.tsv` (exists under read-only
`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/…`, **absent from this lane**); overlap = with
`corpus/evidence/round-36/c1` receipts.

### 1. `unblob-sasquatch-dependency.md` (round 1)
- Staged ids: **S106, S107** — both external (unblob README; devttys0 sasquatch README),
  fetched 2026-10-23.
- Campaign-local? No. Overlap with R36-C1 receipts: none (docs-level).
- Scope: in-scope (producer contract for the lane's frontier bullet).
- Verification: `R36ScoutUnblobReadme.md` re-opened both READMEs 2026-10-26 — every
  install-route fact supported and current, but **refuse as written**: S107 locator §
  "sasquatch" does not exist (headings are `About`/`Prerequisites`/`Installation`); no
  commit/hash pins; hedges dropped; "onekey-sec's fork" unsupported (GitHub API `fork:false`);
  host-state premise "(a) sasquatch absent on this host" now stale (both executables installed).
- Disposition: **defer (admit after small fix)** — flip conditions in §Recommendations.

### 2. `unblob-format-matrix.md` (round 2)
- Staged ids: **S122** — external (unblob.org/formats), fetched 2026-10-23.
- Campaign-local? No. Overlap: none. Scope: in-scope but no R36 consumer.
- Verification: not re-opened by any sibling this wave; internal claim is a coverage-count
  observation (97 handlers; site "more than 30" stale vs README "78+"); recheck uses
  `grep -c` on a fetched page (QUALITY #13 exposure).
- Disposition: **defer**.

### 3. `sasquatch-prebuilt-package-inventory.md` (round 3)
- Staged ids: **S130** — external (GitHub releases page), fetched 2026-10-23.
- Campaign-local? No. Overlap: indirect but strong — the installed `~/.local/bin/sasquatch`
  that the lane's C1 after-runs exercise is byte-identical to this release's amd64 asset
  (`R36ScoutSasquatchRelease.md`, sha256 `ad02d27a…` and `fac88740…`); the entry is the
  provenance record for the exact binary the frozen receipts depend on.
- Scope: in-scope (operator-facing packaging half of the frontier bullet).
- Verification: `R36ScoutPrebuiltInventory.md` re-checked the API 2026-10-26 — 8 releases,
  newest `sasquatch-v4.5.1-6` (2026-01-27) confirmed; **wrong as written** on "each carrying
  a Debian package per architecture" (v1.0 is amd64-only: 2 assets) and on sourcing the
  4.5.1/1.0 version pair from the release body (it is in the tag name + deb control + binary
  version); recheck command weak.
- Disposition: **ADMIT after correction**.

### 4. `sasquatch-unblob-compatibility-precondition.md` (round 7)
- Staged ids: **S165** — campaign-local (`round7/work/r7-local-measurements.tsv`).
- Overlap: none direct; its subject is the precondition the lane's before-receipts now encode.
- Scope: in-scope but **factually stale**: claims "neither tool is installed on the lane
  host". Observed 2026-10-26: both installed (L1). The campaign's own round-8 entry already
  refuted the import-failure inference (unblob present as a uv tool under its own Python).
- Disposition: **REFUSE** (false premise; superseded by entry 5). Flip: only as a dated
  historical erratum, not as a standing knowledge entry.

### 5. `sasquatch-unblob-compatibility.md` (round 8)
- Staged ids: **S183** (external: upstream `squashfs.py`, fetched 2026-10-24),
  **S184, S185, S186** (campaign-local `round8/work/lead3-sasquatch-compat.tsv` — spot-checked,
  consistent with the entry).
- Overlap with R36-C1 receipts: **direct, same class** — S186's negative control
  (`ExtractorDependencyNotFoundReport dependencies=['sasquatch']`) is the identical typed
  refusal as the frozen K1–K4 before receipts; S185's LE positive is the same observation
  class as the lane's after receipts, on different carriers (campaign: locally built LE v4 +
  upstream BE v4 fixture; lane: K1/K2 synthetic + K3/K4 AppImages). Adds the BE-branch
  exercise (`sasquatch-v4be`) that C1's frozen scope excludes.
- Scope: in-scope; closes the campaign's standing CANNOT-ANSWER compatibility lead.
- Caveat carried: campaign host mutation via pacman (history only).
- Disposition: **ADMIT with conditions** (evidence import; see Risks).

### 6. `sasquatch-unblob-avm-branch.md` (round 9)
- Staged ids: **S189** (external code), **S190, S191** (campaign-local round 9 tsv),
  **S192** (external Freetz doc).
- Overlap: none (C1 does not claim BE/AVM — frozen "Not claimed" line). Scope: in-scope
  knowledge, but a synthetic probe of branch decision logic, not a shipped-artifact observation.
- Disposition: **defer** (subsumed in practice by entries 10–11 for lane purposes).

### 7. `avm-image-build-blocker.md` (round 10)
- Staged ids: **S197, S199** (campaign-local), **S198** (external tags API).
- Content: "4.3 tarball not served from any mirror" — **wrong**; round 11 found the correct
  SourceForge path (`squashfs/squashfs/squashfs4.3/`) and md5-verified the tarball.
- Disposition: **REFUSE** (superseded; its one surviving value — the build recipe — lives in
  entry 8). Flip: none as a standalone entry.

### 8. `avm-image-extraction.md` (round 11)
- Staged ids: **S200, S201** — campaign-local.
- Content: first genuine AVM-BE image built (mkfs_time == bytes_used at creation) and
  extracted by unblob via `sasquatch-v4be` without `-be`; corrects the round-9/10 URL error.
  No receipt overlap (AVM out of C1 scope). Scope: in-scope synthetic-carrier work.
- Disposition: **defer** — flip: admit if the lane wants the pinned build recipe on record;
  otherwise its behavioral content is subsumed by entry 11.

### 9. `avm-le-variant-reachability.md` (round 12)
- Staged ids: **S206** (external patch), **S207** (campaign-local).
- Content: "AVM_LE not reachable through the recipe" — **overturned by round 13** (stale
  build tree; a changed `-D` define does not trigger a rebuild).
- Disposition: **REFUSE** (superseded, wrong conclusion). Flip: none standalone; fold into
  entry 10 as one amended file per merge checklist #6 if the lane ever admits the pair.

### 10. `avm-le-image-genuine-marker.md` (round 13)
- Staged ids: **S212, S213** (campaign-local), **S214** (external Freetz-NG patch).
- Content: genuine AVM_LE reachable; unblob routes it through the ordinary LE handler;
  the AVM marker is invisible to unblob. Supersedes entry 9 on both counts it contested.
- Disposition: **defer** (flip: admit as the merged round-12/13 amendment entry).

### 11. `avm-firmware-image-unblob.md` (round 14)
- Staged ids: **S216, S217** (external: AVM's own download index + info file),
  **S218, S219, S223** (campaign-local superblock/unblob/NMI-TI tsvs — spot-checked,
  consistent, incl. firmware sha256 `f518ce6b…`), **S220** (external Freetz-NG docs).
- Content: real shipped artifact (`FRITZ.Box_6490_Cable-07.57.image`, 39,741,440 bytes)
  fetched from AVM's server; tar archive carrying **both** AVM filesystems; the AVM marker
  measured on production firmware (x86 LE member `mkfs_time` 28,200,029 == `bytes_used`;
  BE member 5,442,392 == 5,442,392); unblob extracted 9,877 files via its ordinary LE/BE
  handlers; corrects the round-13 ledger's NMI-gap/TI-checksum expectation with a structural
  reason (separate tar members, superblocks at offset 0).
- Overlap with R36-C1: none (BE/AVM out of frozen scope) — no conflict.
- Scope: **strongest province fit of the theme** (reverse engineering of a shipped artifact
  with the lane's pinned tooling; extends the corpus README Firmware axis).
- Disposition: **ADMIT with conditions** (evidence import; see Risks).

## Recommendations (≤3 admits, ≥3 refuses)

**Admit (3):**
1. `sasquatch-prebuilt-package-inventory` — after corrections per `R36ScoutPrebuiltInventory.md`:
   "each" → "7 of 8 (v1.0 amd64-only)"; attribute the 4.5.1/1.0 version pair to tag name +
   deb control + `-version`, not the release body; strengthen the recheck (`jq length`, per-tag
   asset counts). *Flip:* refuse as written if the corrections are not made before append.
2. `sasquatch-unblob-compatibility` — import the campaign tsvs (S184–S186) into the lane
   evidence tree and rewrite anchors; keep the pacman host-mutation sentence as recorded
   history; add one sentence noting the lane's own frozen K1–K4 receipts independently
   reproduce the negative control on the frozen carriers (corroboration, not duplication).
   *Flip:* refuse if the evidence files are not imported (sources unresolvable per QUALITY #1).
3. `avm-firmware-image-unblob` — import the campaign tsvs (S218/S219/S223); state the one-image
   limit it already carries. *Flip:* refuse if the tsvs (or the firmware sha256 record) are not
   imported.

**Refuse (3):**
4. `sasquatch-unblob-compatibility-precondition` — false premise ("not installed"), refuted by
   its own campaign's round 8 and by the observed 2026-10-26 host state; superseded by #2.
   *Flip:* only as a dated historical erratum, never as standing knowledge.
5. `avm-image-build-blocker` — superseded; its central fact (4.3 tarball unobtainable) is wrong.
   *Flip:* none as standalone.
6. `avm-le-variant-reachability` — superseded; its conclusion was a stale-binary artefact.
   *Flip:* none as standalone.

**Defer (5, flip conditions):** `unblob-sasquatch-dependency` (fix S107 locator to
`About`/`Prerequisites`/`Installation` + line numbers; pin commits/hashes — unblob README
`26.6.4` = `1fcc7a0a…`, sha256 `6544d60f…3716`; devttys0 README sha256 `f09961ee…fef`; label
inferences; drop or source the "fork" claim; add the Debian-only scope, the
`--show-external-dependencies` check, and the second executable `sasquatch-v4be`; correct the
stale host-absence premise — then it is admittable in a later wave); `unblob-format-matrix`
(needs a lane consumer and a `grep -o | wc -l` recheck); `sasquatch-unblob-avm-branch` and
`avm-image-extraction` (synthetic-instrument results; admit only if the lane claims BE/AVM or
wants the pinned build recipe); `avm-le-image-genuine-marker` (admit only as the merged
round-12/13 amended entry).

## Risks / calibration notes for L1

1. **Collision chain, not a single collision.** Staged S106 collides with the lane's S106
   (confirmed; already in `assimilation/collisions`). A full ordered append maps staged N →
   lane N+1 and the staged block then occupies S107–S238 — overlapping the sibling-drafted
   round-36 claim rows S107–S112. Sequence the claim rows and the assimilation append, and
   compute the renumber map only after the final admit set (quarantine drops shift offsets).
2. **Merge rows cannot satisfy R36-C1's sourced requirement.** The claim requires the C1
   entry to cite a SOURCES row **opened 2026-10-26** whose used-by lists that entry; all
   merge theme rows opened 2026-10-23/24. Admission neither satisfies nor blocks the claim;
   the lane's own drafted rows (S107 sasquatch release, S108 handler, S109 neovim) remain the
   claim's rows.
3. **Campaign-local evidence is not in the lane.** Every entry resting on
   `lanes/kaidoku/round*/work/*.tsv` (entries 4, 5, 6, 7, 8, 9, 10, 11) cites paths absent
   from this lane; the tsvs exist only under read-only `/home/vgpnk/Projects/shokuknow`.
   Admitting any of them without importing the evidence files into the lane tree violates
   QUALITY #1/#18 (unresolvable source).
4. **Staleness hazard for calibration.** Admitting entry 4 would write a false host-state
   fact into the corpus the same round C2 measures self-assessment against observed state —
   a direct calibration-axis hazard. The two refuse-on-staleness entries (4, 7, 9) are
   exactly the class C2-style counters catch.
5. **Tool provenance note for the record:** no installs/upgrades by this seat; the installed
   sasquatch/unblob binaries were observed, not modified.

## Verification log (this seat)

- `grep -oE '^\| S[0-9]+' corpus/SOURCES.md | sort` → 106 rows, max S106; `sed -n 112p`
  → S106 binutils row. Registry/staged/collisions/quarantine files read verbatim.
- Python parse of `SOURCES.append.md` (escaped-pipe-aware split, 11 cells/row): all 132 rows
  parsed; theme rows' used-by cells extracted (table above).
- `MERGE-REPORT.json` → `first_id: S106`, `existing_rows: 105`, `renumbered: []`, all 11
  theme entries `collides_with_existing: false` (filename-level; the id collision is at the
  SOURCES layer).
- `K1/before.json`, `K3/before.json` → `ExtractorDependencyNotFoundReport` /
  `missing-extractor-dependency` observed verbatim.
- Spot-checks of campaign tsvs (`round8/work/lead3-sasquatch-compat.tsv`,
  `round14/work/lead2-avm-firmware-{superblocks,unblob}.tsv`) → consistent with entries 5
  and 11, including the `host_mutation` pacman row.
- Host observation: `~/.local/bin/sasquatch{-v4be,} -version` → 4.5.1 (2022/03/17);
  `unblob --version` → 26.6.4.
- Sibling corroboration: `R36ScoutUnblobReadme.md`, `R36ScoutPrebuiltInventory.md`,
  `R36ScoutSasquatchRelease.md`, `R36ScoutUnblobHandler.md` (all 2026-10-26 observations).
