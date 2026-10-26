# R42ConnSibling — sibling-overlap scan (pre-freeze recon)

**Verdict: DONE** — overlap scan complete. One substantive sibling holds ground on the same
toolchain (revenger-shokunin, REA + unblob + firmware category); no sibling holds SquashFS
v1–v3 extraction, DD-WRT/OpenWrt/Kamikaze carrier ground, sqfs-triage tables, or the
generator/counter key-mismatch defect class. R42's claimed surfaces do not collide with any
held sibling claim, but the **province label** "firmware" is shared and pre-flagged as
arbitrated between kaidoku and revenger (tsukuroi PROVINCE ADJ-06/OUT-009).

## Scope and method

Sources scanned (read-only): all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin`
(excluding kaidoku itself). Files: `PROVINCE.md`, `SKILL.md`, `corpus/README.md`, full
`corpus/lessons/`, plus `tools/` and `plans/` where present. Definitive token sweep across the
whole sibling trees for `squashfs|sqfs|sasquatch|kamikaze|tqsh|declared_features`; a separate
sweep for `unblob|sasquatch|extract-firmware|openwrt|dd-wrt|triage|key-mismatch` over the docs;
follow-up targeted reads of the hit lanes (revenger, tsukuroi, kengaku, kasegi, kotodama,
game-dev-3d). All commands = `grep` tool calls; no writes outside the report/artifact paths, no
tools installed, no git mutation.

## Overlaps found

| lane | path:line | what | contested? |
|---|---|---|---|
| revenger-shokunin | `PROVINCE.md:3-6` | Core owns "reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, **firmware**, browser/Electron runtime evidence — using the REA skill and its toolset" | province label shared |
| revenger-shokunin | `PROVINCE.md:15-16` | REA host engines census incl. "Binwalk/Unblob" | no — engine inventory |
| revenger-shokunin | `corpus/README.md:43` (C07 row) | firmware images **held** only as manual byte-derived readout of one authored fixture (`fixtures/firmware-r63/firmware-r63.bin`); explicit disclaimer "no general firmware-format, **extraction/execution**, provider-completeness or authenticity claim" | no — deliberately narrower than R42-C1 |
| revenger-shokunin | `corpus/README.md:71-74` | "C07 firmware — REA `inspect_firmware_regions` / `extract_firmware` need caller-supplied Binwalk 3.1.x and Unblob 26.6.x; the host has binwalk 3.1.0 and unblob 26.6.4 … Presence is not readiness: an authored known-truth firmware fixture is the next probe." | same engine facts as R42-C1 — duplicate-ground risk if restated |
| revenger-shokunin | `SKILL.md:431-442` (§Firmware oracle) | authored bytes vs saved REA record; M33 (`round-63.md:218`): zero-finding image needed binwalk `--search-all`; "assume a format name implies detectability" lesson | no |
| revenger-shokunin | `corpus/lessons/round-64.md:89-94` | S036 quote (REA firmware guide): "REA accepts **Binwalk 3.1.x** for region inspection and **Unblob 26.6.x** for explicit extraction"; "report parsers are verified with Binwalk 3.1.0 and Unblob 26.6.4" | held fact, same versions R42 uses |
| revenger-shokunin | `corpus/lessons/round-70.md:98-106` | staged-but-**unadopted** Unblob SOURCES rows S054/S099/S152 quarantined; renumber collision map ready if adopted later | live collision candidate if R42 adds unblob-doc rows |
| kengaku-shokunin | `.ufo/waves/round-26/build/ConnRosterScan.md:16,39` | scanned kaidoku `PROVINCE.md:147`, recorded "sasquatch unblob squashfs recursion extractor" as kaidoku ground, verdict: unrelated to their surface | no — explicit deferral |
| kengaku-shokunin | `.ufo/waves/round-42/build/F42ConnFrontier.md:26` | notes kaidoku's own triage tools (`tools/round-39/sqfs-triage.py`, `tools/round-40/sqfs-triage-v2.py`) | no |
| game-dev-3d-shokunin | `corpus/lessons/r102-unreal-integration.md:192-193` | "rea.md now records JADX/Binwalk/Unblob as present" | no — env list only |
| tsukuroi-shokunin | `SKILL.md:49`; `PROVINCE.md:11-14` | "firmware" plane = nvidia GSP blobs + boot-loader files, health inventory only | no — not shipped-artifact RE |
| tsukuroi-shokunin | `PROVINCE.md:50-51` (ADJ-06), `:149-152` (OUT-009) | "Driver/firmware/package mechanism requires shipped-artifact RE … protocol integrator — **kaidoku/revenger ownership unresolved**"; "Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff" | **recorded open arbitration** |
| kasegi-shokunin | `.ufo/waves/round-39/wave2/SentinelScopeGuard.scope.txt:159-160` | observability sasquatch/sasquatch-v4be first seen in `~/.local/bin` on 2026-10-26 01:22:37 | no — host inventory |
| kasegi-shokunin | `corpus/source-snapshots/round-35/S052.txt:5066` | IGEL OS CVE citation: "crafted root filesystem can be mounted from an unverified SquashFS image" | no — security-db citation |
| kotodama-shokunin | round-55/60/65 artifacts | "Sasquatch" hits are the Bigfoot cryptid (cryptozoology) | token false-positive class for future scans |
| kotodama-shokunin | `corpus/knowledge/verification/two-reader-interop-agreement.md` | two independent readers of the same artifact must be compared; divergence dispositioned as reader-drift/input-drift/real defect | no — methodology adjacency to R42-C1's oracle rule |

Negative results: **zero** sibling mentions of SquashFS v1–v3, `squashfs_v3*` handlers,
DD-WRT/OpenWrt/Kamikaze/tqsh images, sqfs-triage tables, `declared_features`, or a
generator/counter key-mismatch defect class in any scanned surface.

## Contested scope

1. **"Firmware" province label** — revenger declares firmware images as Core (shipped-artifact
   RE via REA); kaidoku's own PROVINCE already holds a "Firmware regions + extract" capability row
   (`PROVINCE.md:132`, `extract-firmware` on GSP/pkg material since round 4) and now proposes
   SquashFS v3 extraction outcomes as new Core. The two lanes' **held claims** do not collide:
   revenger's C07 is one authored fixture read by hand with an explicit no-extraction/no-general
   disclaimer; kaidoku's R42-C1 is four published v3 carriers scored by a counter. The
   **labels** overlap, and tsukuroi's PROVINCE already records the kaidoku/revenger internals-RE
   arbitration as unresolved. Recommended freeze posture: scope the R42 knowledge entry
   explicitly to SquashFS v3 extraction outcomes (mirroring revenger's disclaimer style), name
   revenger's held S036/readiness facts as the upstream engine-availability authority rather than
   restating them, and surface the arbitration flag to the L1.
2. **Shared engine facts** — both lanes pin the same facts (REA accepts Binwalk 3.1.x / Unblob
   26.6.x; host has binwalk 3.1.0 / unblob 26.6.4; sasquatch 4.5.1 installed 2026-10-26).
   R42's knowledge/claims should cite revenger's held entry for those facts (cross-lane pointer)
   or expect duplicate-ground scrutiny at assimilation.
3. **Unblob source rows** — revenger has quarantined, not-yet-adopted SOURCES rows
   S054/S099/S152 for Unblob material. If any R42 SOURCES row targets unblob documentation, it
   collides with revenger's staged rows; coordinate before freeze (R42's planned rows are
   carrier-publisher rows, so no collision expected, but the facts above should stay
   cross-referenced).

## Defect patterns siblings recorded that this round's tools could repeat

- **revenger M19/Q05** (`round-1.md:56`; `knowledge/seed.md`): host facts go stale without a
  recheck — "presence is not readiness". R42 pins tool versions in claims/knowledge; every such
  fact should carry a verified-at receipt + recheck command (the counters already verify the
  binaries at score time; keep prose citations to receipts).
- **revenger M33** (`round-63.md:218`) + Q06: "assume a format name implies detectability" and
  "never state an offset or count from intent". Applies to the v4 table's step-3 sentence
  ("every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch` [to be confirmed by wave 1
  on real REA envelopes]") and the legacy-failure row: confirm against real envelopes, don't
  freeze from assumption.
- **revenger Q16** (round-64 spotcheck): a claim reaches past what the command printed. The C2
  interpreter/evaluator must consume only the observed feature-tuple keys actually present in the
  envelope, under exactly one key (`declared_features`) — the R41-CL1 lesson in the same class.
- **kotodama two-reader interop**: if `unsquashfs` and `7z` disagree on a candidate carrier
  before freeze, disposition the divergence (reader-drift vs input-drift vs real defect) before
  freezing, per the claim's "must agree file-for-file" rule.
- **Scratch hygiene** — kengaku (r41/r42), tameshi (r35) and revenger (r66) misroot sweeps
  registered stray `/tmp/sqfs-v2-*` debris, `/tmp/…/a.sqsh`, and a fleet-root `unblob.log`
  from earlier rounds. R42 seats must keep every scratch under `/fast/scratch` (bounds already
  mandate this); no `/tmp` fixtures.
- **Namespace caveat** — kake-shokunin has its own `.ufo/waves/round-42/...` wave dirs
  (independent round numbering); naive fleet-wide "round-42" searches will hit them. Token
  "Sasquatch" in sibling scans must be disambiguated from the Bigfoot cryptid (kotodama).

## Evidence

- Artifacts: `artifacts/R42ConnSibling/overlap-hits.tsv` (hit table with context lines).
- Scan commands (grep tool): token sweeps listed in Scope; all results reproduced in the TSV.

## Verification and limits

- Read-only exploration; no writes outside this report + artifact dir; no tools installed.
- [INFERENCE] revenger's quarantined rows S054/S099/S152 are "present verbatim" per round-70
  lesson but their exact row contents were not re-fetched; collision statement is based on the
  lesson's record.
- The scan covers the surfaces the seat brief names (PROVINCE/SKILL/corpus README/lessons) plus
  full-tree rare-token sweeps; it does not claim exhaustiveness over every artifact dir.
