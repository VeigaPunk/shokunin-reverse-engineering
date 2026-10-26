# R36ConnSiblingOverlap — sibling-overlap scan for the R36-C1 surface

Seat: R36ConnSiblingOverlap (leaf; no subagents, no background jobs, no VCS mutation).
Round: kaidoku-shokunin round 36, wave 1. Report path per assignment.
Surface scanned: sasquatch / unblob / SquashFS / AppImage extraction (the R36-C1 move of
the sasquatch squashfs-recursion extractor from Frontier to Core, per
`plans/round-36-claims.md` R36-C1).

## Method (read-only)

- Swept every sibling lane under `/home/vgpnk/Projects/shokunin/*-shokunin` (19 lanes;
  kaidoku itself excluded from the "sibling" set but read for framing) across:
  `PROVINCE.md`, `SKILL.md`, `corpus/SOURCES.md`, and the whole `corpus/knowledge/` tree,
  case-insensitive, for `sasquatch|unblob|squashfs|appimage`.
- Full-tree grep for the literal `sasquatch` across all sibling lanes (catches wave reports,
  scratch, and fixtures-not-expected-to-be-text is noted as a limit below).
- Read shokuknow merge packages for kaidoku/revenger/tsukuroi (read-only; no campaign tool
  run there) to check for staged-entry collisions.
- No installs/upgrades performed by this seat (tooling directive record: none). All
  commands read-only (`grep`, `sed -n`, `ls`).

Coverage limits: grep covers text files; binary carriers/fixtures were not byte-searched
([INFERENCE] province text lives in md/json/txt, so the sweep is representative). The
multi-path glob form of the grep tool silently failed on `*-shokunin/...`; per-lane and
shell sweeps were used instead (verified against kaidoku's own PROVINCE, which does
contain the sasquatch bullet at `:149-150`).

## Verdict up front

No sibling lane holds — and no sibling lane contests — the R36-C1 surface (sasquatch
recursion over carved SquashFS, incl. AppImage payloads). Kaidoku moving sasquatch to
Core absorbs no other lane's province. The one live cross-lane contest touching this
neighborhood (revenger vs kaidoku on the `inspect-firmware-regions` / `extract-firmware`
verbs and the binwalk/unblob version pins, ADJ-06) is adjacent, already fenced
"reported, not absorbed", and is neither enlarged nor settled by C1. Tsukuroi's
host-tooling/health plane is untouched. Kengaku pre-cleared the exact bullet in round 26.

## Lane-by-lane evidence

### revenger-shokunin — nearest neighbor; contests the adjacent verb/pin surface, NOT sasquatch

Holds/uses unblob, never sasquatch; all extraction work is binwalk-scoped on one authored
fixture; every contested item is explicitly fenced.

- Domain declaration: `revenger-shokunin/PROVINCE.md:3-7` — owns "reverse engineering of
  shipped artifacts — … archives, firmware … using the REA skill and its toolset".
- Tool census (mention only): `revenger-shokunin/PROVINCE.md:16` — "(Ghidra, IDA, JADX,
  Binwalk/Unblob, pwntools) — census in corpus/knowledge/seed.md".
- Mint census (historical): `corpus/knowledge/seed.md:17` ("Host engines ABSENT at mint:
  ghidra, jadx, binwalk, unblob, pwntools"), `:66` (F11 STALE→present);
  `corpus/knowledge/2026-10-12-rea-readiness-checklist.md:17` (unblob ABSENT row),
  `:40` (K05 STALE→3 of 4 present).
- C07 firmware row — `held` via one fixture-scoped entry:
  `revenger-shokunin/corpus/README.md:43` (C07 = `knowledge/round-64-firmware-region-byte-evidence.md`,
  "no general firmware-format, extraction/execution, provider-completeness or authenticity
  claim"); frontier note `:71-74` names only the "caller-supplied Binwalk 3.1.x and
  Unblob 26.6.x" pins.
- Explicit fence: `corpus/knowledge/round-64-firmware-region-byte-evidence.md:201-203`
  ("## Cross-lane scope note (Q10)… does not absorb kaidoku Core's live
  `inspect-firmware-regions` / `extract-firmware` surface … or its provider-pin registry
  … ADJ-06 … remains open").
- Contest record: `revenger-shokunin/.ufo/waves/round-64/R64ConnectorOverlap.md:14-16`
  (kaidoku holds the verb+pins on real GSP blobs; tsukuroi ADJ-06 recipient unresolved;
  fleet `.ufo/l0-questions.md:42` is the open arbitration), `:24` (promoting README pins
  would absorb kaidoku's pin registry — forbidden), `:42` (contested item = the verb plus
  binwalk/unblob pins; revenger's C07 add must stay fixture-scoped).
- Unblob usage to date (author-side cross-check, binwalk-scoped):
  `.ufo/waves/round-63/build/R63FirmwareFixture.md:152-180` and
  `corpus/live/runs/round-63/LEDGER.md:80-84` (I5: unblob 26.6.4 found **0 chunks** on the
  whole 2048-byte fixture image, 1 chunk only on an isolated member). No SquashFS, no
  AppImage, no sasquatch involvement anywhere in revenger.
- Round-70 assimilation (metadata about the tool, not capability):
  `.ufo/waves/round-70/w1/R70W1AssimUnblob.md:81-87` — re-grounds unblob upstream README
  claims; ran `unblob --show-external-dependencies` (exit 0) recording
  `sasquatch ✗  sasquatch-v4be ✗` among missing host deps;
  `.ufo/waves/round-70/w1/R70W1AssimDraft.draft-entry.md:62-63` lists the 15-name
  dependency set incl. sasquatch. This documents unblob's *dependency-set documentation*;
  it asserts nothing about extraction capability and runs no extraction.

### tsukuroi-shokunin — host tooling/health plane; explicit non-absorber of binary internals

- `tsukuroi-shokunin/PROVINCE.md:51` (ADJ-06): recipient column "protocol integrator —
  kaidoku/revenger ownership unresolved"; capture column "Loaded version, package
  provenance and driver/boot symptoms; **no binary-internals inference**".
- `tsukuroi-shokunin/PROVINCE.md:77-80` (Frontier): "Kaidoku and revenger both declare
  shipped-artifact RE. The integrator must arbitrate this shared scope; **tsukuroi neither
  picks an owner nor absorbs it**."
- `tsukuroi-shokunin/PROVINCE.md:150-152` (R20 ownership clarification): kaidoku/revenger
  arbitration unresolved; "No configuration, service, package, boot or sibling-file write
  is authorized."
- Host package censuses are pacman-based health planes (`tsukuroi-shokunin/SKILL.md:46`
  package state incl. `pacman -Qm` foreign count; `:49-50` driver/firmware and
  update-safety planes). Round-24 inventory snapshots record squashfs-adjacent *host
  packages* only: `.ufo/waves/round-24/w1/ExecMirrorTimestamps/host-extra-pkglist.txt:5452`
  (`libappimage`), `:10852` (`python-pysquashfsimage`), `:13025` (`squashfs-tools 4.7.5`)
  (+ `squashfuse`). Inventory, not internals.
- Sibling-capture copies: `tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kaidoku/{8451e4710954,d1d981d2cc04}/PROVINCE.md:147-148`
  contain kaidoku's own sasquatch frontier bullet — evidence tsukuroi *surveyed kaidoku*,
  not a tsukuroi claim.

### kengaku-shokunin — pre-cleared non-contest (exact bullet evaluated and ruled out)

- `kengaku-shokunin/.ufo/waves/round-26/build/ConnRosterScan.md:16`: kaidoku
  `PROVINCE.md:147` "sasquatch" unblob squashfs recursion extractor → "**No**; unrelated
  filesystem/archive extractor, not response extraction…". The identical verdict is
  archived in two round-28 scratch copies (same file path under
  `.ufo/waves/round-28/scratch/KengakuR28.FRegistryS049/...` and
  `.../FSeparability/s038-only-control/...`).

### game-dev-3d-shokunin — host census only

- `game-dev-3d-shokunin/corpus/knowledge/rea.md:8,31` (mint: no Ghidra/JADX/Binwalk/Unblob),
  `:36-39` (re-probe: `unblob --version` → 26.6.4, "uv tool, shim at
  `/home/vgpnk/.local/bin/unblob`"). Presence census; no extraction province.

### mado-shokunin — incidental AppImage mentions (running desktop app, not extraction)

- `mado-shokunin/corpus/knowledge/hyprland-config-plane.md:192-193,251-255`;
  `config-health-report-r3.md:365-366,911-913`; `remaining-planes-census.md:178` — all
  concern the Grok_Bot AppImage as an autostart process/path/symlink shape.

### tabi-shokunin — incidental census question

- `tabi-shokunin/corpus/knowledge/browser-surface-census.md:186` — U2: whether browsers
  exist via non-pacman paths "(AppImage, manually …)". A question row, not a hold.

### kotodama-shokunin — word collision, excluded

- `kotodama-shokunin/corpus/SOURCES.md:383` (S354): "Sasquatch" the cryptid in a
  cryptozoology paper. Different sense; excluded from the surface.

### All remaining sibling lanes

- audio, chousa, game-dev-2d, kagi, kake, kama, kasegi, kengaku, kotoba, kumitate, lore,
  mori, souji, tameshi: zero hits for any of the four terms in PROVINCE/SKILL/SOURCES and
  corpus/knowledge (full sweep; see Method).

## shokuknow merge packages (collision check, read-only)

- `merge/kaidoku/knowledge/corpus/knowledge/`: 7 sasquatch/unblob entries incl. the three
  named in the claims' assimilation theme (`unblob-sasquatch-dependency.md`,
  `sasquatch-prebuilt-package-inventory.md`, `sasquatch-unblob-compatibility.md`; plus
  `sasquatch-unblob-avm-branch.md`, `sasquatch-unblob-compatibility-precondition.md`,
  `unblob-format-matrix.md`, `avm-firmware-image-unblob.md`).
- `merge/revenger/`: firmware entries exist (`firmware-extractor-dependency-degradation-2026-10-23.md`,
  `firmware-extraction-toolchain-ja.md`, `rea-firmware-prerequisite-contract.md`, …) but a
  grep for `sasquatch` across `merge/revenger` returns nothing — no collision with C1's
  entry stem.
- `merge/tsukuroi/`: no sasquatch/unblob/squashfs entries.

## Answers to the assignment questions

1. **Which lanes hold or contest this ground?** None hold it. Revenger contests only the
   adjacent `inspect-firmware-regions`/`extract-firmware` verb + binwalk/unblob pin
   surface (ADJ-06, open, fleet `.ufo/l0-questions.md:42`) — contested in both directions
   with kaidoku as the incumbent holder; C1 changes nothing there. Tsukuroi declines
   binary internals outright (ADJ-06 + Frontier + R20 clarification). Kengaku ruled the
   sasquatch bullet explicitly out of its scope in round 26. Every other hit is census,
   incidental, or a word collision.
2. **Does kaidoku moving sasquatch to Core absorb another lane's province?** No.
   - Revenger: the frozen C1 predicate adds only a Core row naming sasquatch + receipts
     closing unblob's `missing-extractor-dependency` gap; it does not restate the
     contested verbs, pins, or GSP evidence ids, so the round-64 "reported, not absorbed"
     fence is preserved and ADJ-06 is neither enlarged nor pre-judged.
   - Tsukuroi: C1 claims extraction capability, not host-health/install ownership. The
     sasquatch 4.5.1 binary the L1 pre-installed from the official onekey-sec deb into
     `~/.local/bin` is a non-pacman, foreign, unpacked file — invisible to tsukuroi's
     `pacman -Qm`-based foreign census (`tsukuroi-shokunin/SKILL.md:46`) but observable by
     any `command -v`-style re-probe ([INFERENCE] on visibility class; the deb-unpacked
     layout is per this round's brief).

## Second-order effects and risks (trace across runtime/contract/substrate/verification)

- **Revenger census drift (low):** revenger's staged round-70 unblob entry records
  sasquatch as a missing host dependency (probe dated in-seat, `R70W1AssimUnblob.md:85`).
  After C1 lands, that remains true as a dated snapshot; revenger's next live re-probe
  will observe sasquatch present and must re-date rather than conflict. Not a contest; a
  freshness obligation on revenger's own recheck column.
- **Tsukuroi census drift (low):** same host-state change seen from the health plane; a
  future tsukuroi deep census noticing `~/.local/bin/sasquatch` would record presence, not
  ownership. Kaidoku must keep the r36 Core row scoped to extraction receipts (as the
  frozen predicate words it) and must not word it as a host-tooling claim — doing so
  would step on tsukuroi's ADJ-06 boundary.
- **ADJ-06 posture (unchanged):** C1 is a capability move inside kaidoku's declared
  domain; the integrator arbitration request stays open and untouched. No lane's
  province text needs edit because of C1.
- **kengaku roster scans (unchanged):** the round-26 verdict (`ConnRosterScan.md:16`)
  already covers the bullet that C1 promotes; kengaku needs no update.

## Verification transcript (exercised)

```sh
# sibling province-level sweep (PROVINCE.md, SKILL.md, corpus/SOURCES.md)
cd /home/vgpnk/Projects/shokunin && for L in *-shokunin; do [ "$L" = kaidoku-shokunin ] && continue;
  for f in "$L/PROVINCE.md" "$L/SKILL.md" "$L/corpus/SOURCES.md"; do
    [ -f "$f" ] && c=$(grep -icE 'sasquatch|unblob|squashfs|appimage' "$f") &&
    [ "$c" -gt 0 ] && echo "$f: $c hits"; done; done
# → kotodama-shokunin/corpus/SOURCES.md:1 | revenger-shokunin/PROVINCE.md:1 |
#   revenger-shokunin/corpus/SOURCES.md:1   (exit 0; SWEEP-DONE)

# full-tree literal 'sasquatch' across all siblings (excl. kaidoku)
grep -rin 'sasquatch' --include='*.md' --include='*.json' --include='*.txt' \
  --include='*.sh' --include='*.py' . --exclude-dir=kaidoku-shokunin
# → hits only in: revenger round-70 assimilation reports (dependency-set metadata),
#   tsukuroi round-19 kaidoku-capture copies, kengaku ConnRosterScan verdicts,
#   fleet .ufo/.tower records about kaidoku's own rounds. Exit 0.

# knowledge-tree sweep across all siblings
for L in *-shokunin; do [ "$L" = kaidoku-shokunin ] && continue;
  grep -rilE 'sasquatch|unblob|squashfs|appimage' "$L/corpus/knowledge" 2>/dev/null; done
# → game-dev-3d rea.md; mado x3; revenger seed.md + 2026-10-12 checklist + round-64 entry;
#   tabi browser-surface-census.md. Exit 0.

# shokuknow merge collision check (read-only)
ls /home/vgpnk/Projects/shokuknow/merge/{kaidoku,revenger,tsukuroi}/knowledge/corpus/knowledge/ | grep -iE 'sasquatch|unblob|squashfs'
grep -rln sasquatch /home/vgpnk/Projects/shokuknow/merge/revenger   # → no output
```

State confirmed additionally: kaidoku `PROVINCE.md` currently has no `Round-36` section
(wave-1 build phase; Core row is the L1 integration deliverable), and
`corpus/knowledge/` has no `2026-10-26-r36-*` entry yet — consistent with the frozen
predicate being unmet at base, and with the frontier bullet still present at
`kaidoku-shokunin/PROVINCE.md:149-150` adjacent to the Core rows at `:125` (firmware)
and `:133` (AppImage inner payload); `SKILL.md:64` names the 7z-on-squashfs fallback the
C1 receipts will upgrade.

Scratch (`/fast/scratch/hyaku/kaidoku-r36/R36ConnSiblingOverlap`) held no clones or
downloads this seat; removed at exit per the brief.
