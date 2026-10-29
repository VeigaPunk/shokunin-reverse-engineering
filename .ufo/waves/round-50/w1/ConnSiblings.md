# ConnSiblings — round 50 wave 1 (pre-freeze): sibling-overlap scan

Seat: ConnSiblings (connector, leaf, read-only). Lane: kaidoku-shokunin, base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Seat artifacts: `.ufo/waves/round-50/w1/ConnSiblings/` (`receipts.sha256`, `tar-walk.py`, `tar-walk-r50-carriers.tsv`, `tar-walk-r50-carriers.stderr`, `sibling-binary-magic.tsv`). Scratch removed. No lane, sibling or fleet file was written; no git mutation; no install; no REA or unblob run; no `--data-run`.

## Verdict

**Sibling overlap: none on the claimed ground.** No sibling holds LE AVM SquashFS ground, vendor FRITZ!OS downloads, or a registry row for an `download.avm.de` URL. Firmware ownership between kaidoku and revenger stays the open ADJ-06 arbitration; R50-C1 adds no new contest if the adjacency sentence below is carried.

**In-lane defect for the L1, found while checking the overlap (not a sibling issue): the draft plan's carrier pin cannot be satisfied for two of four carriers.** The plan pins the tar member `./var/tmp/filesystem.image` for every carrier. Walking the tar headers of the planned images shows that path is absent for `c6490` and `c6430`. Their LE `hsqs` rootfs sits at `./var/remote/var/tmp/x86/filesystem.image`. The L1 probe `scan.py` matched any member ending in `filesystem.image`, so its `hsqs` rows for those boxes measure the x86 member, not the plan's path. Details in F-3 to F-5.

## Findings — sibling scan (R50-C1 ground)

Searches, all run from `/home/vgpnk/Projects/shokunin`:

| # | command (abridged) | exit | result |
|---|---|---|---|
| S1 | `grep -l -i -E 'FRITZ\|AVM\|SquashFS\|unblob\|sasquatch\|extract-firmware\|hsqs\|filesystem\.image' */PROVINCE.md`; same over `*/SKILL.md` | 0 | PROVINCE.md: **2** hits, kaidoku (own lane) and revenger. Revenger substance: `revenger-shokunin/PROVINCE.md:4` ("archives, firmware"), `:22` (Binwalk/Unblob as caller-supplied engines). SKILL.md: **1** hit, kaidoku only. No other sibling PROVINCE or SKILL names these terms. Tool-presence Unblob mentions in other lanes live in `corpus/knowledge` (S2), not PROVINCE. No sibling claims SquashFS, AVM or `extract-firmware`. |
| S2 | `grep -rIn -i -E '…' */corpus/knowledge` (excluding kaidoku) | 0 | Hits only revenger (`corpus/knowledge/2026-10-12-rea-readiness-checklist.md:17,40-46`, `seed.md:17,64-67`, historical presence census; `round-64-firmware-region-byte-evidence.md`, an authored zlib fixture, fenced) and game-dev-3d `rea.md`. A `kotodama` "Fritz Graf" hit is a classical-scholar surname. |
| S3 | tight AVM/firmware grep over `revenger-shokunin` (excluding `snapshots/`) | 0 | Zero `FRITZ`, `AVM`, `download.avm`, `hsqs` hits. Firmware hits only: `.ufo/waves/round-63/build/R63ConnectorOverlap.md:36,42`, `round-64/R64ConnectorOverlap.md`, `round-64/R64ReviewEntryScope.md:133,214`, `corpus/live/runs/round-63/LEDGER.md:51`, `corpus/knowledge/round-64-…md:144-203`. A first pass matched `dex-format.html` only because `navMenu` contains `avM` case-insensitively (false positive, discarded). |
| S4 | `grep -rIn -E 'FRITZ\|\bAVM\b\|download\.avm\|\bhsqs\b\|squashfs_v4\|sasquatch\|extract-firmware' revenger-shokunin` | 0 | Zero AVM/FRITZ/hsqs hits. `extract-firmware` only in `.ufo/waves/round-63/source-snapshots/rea-firmware-guide.md:90-91` and `round-64/source-snapshots/rea-firmware-guide.md:57-58` (REA docs snapshot). |
| S5 | `grep -n … revenger-shokunin/corpus/SOURCES.md` (firmware/squashfs/unblob/binwalk/AVM, no `http` terms) | 0 | 95 rows, no AVM/FRITZ/SquashFS row. Own-work `S037` (authored `firmware-r63.bin`), a `:156` note that the REA firmware guide is "not yet a row". |
| S6 | `grep -rIl -E 'FRITZ\|\bAVM\b\|download\.avm\|\bhsqs\b' --exclude-dir=.git --exclude-dir=snapshots .` (fleet root, all lanes) | 0 | Hits: kaidoku own lane; tsukuroi `.ufo/waves/round-50/w1/R50ScoutLiveTip/*` and `R50RevScopeSiblings/tip.kaidoku.md` (tsukuroi reading kaidoku's tip PROVINCE, read-only, quotes kaidoku rows); tabi `round-34/w2/ConnSiblingDrift/kaidoku.diff`, `round-35/w1/ConnCrossClaim/crossclaim.md`, `round-36/w1/ConnDeltaScan/scan.md` (kaidoku commit logs, not sibling ground); kengaku/lane3 `R42ScoutMisroot.md` (`/tmp/kd-*` names). `mado` hits are the author name "M. Fritz" in arXiv text. No sibling file holds an AVM/FRITZ download, carrier, or URL. |
| S7 | `grep -rIn -i -E '…' .ufo/reports/round-4*/` and per-file counts | 0 | Firmware-term hits in `round-4x` reports are all `kaidoku.md` (`round-40` 22, `41` 10, `42` 9, `43` 4, `44` 19, `45` 1, `46` 1, `48` 3, `49` 5, `4` 2). No sibling report. |
| S8 | `find` of sibling trees for firmware-like names and sizes ≥256 KiB, then magic check (`sibling-binary-magic.tsv`, 37 candidate rows + header) | 0 | 0 SquashFS (`hsqs`/`sqsh`) or ustar hits across 37 candidate binaries (revenger `round-67/quarantine/*/source.bin`, audio `r89` stdout captures, mado/tabi/kumitate fetch bins). No vendor firmware bytes in any sibling tree. Scope caveat: the magic check covers only files ≥256 KiB whose names or paths match firmware/bin/image patterns. |
| S9 | `grep -rIn -E 'download\.avm\|fritz\.os\|FRITZ!' --exclude-dir=.git .` (fleet, excl. kaidoku) | 0 | No sibling registry row for any `download.avm.de` URL. Only tsukuroi quotes of kaidoku PROVINCE and the tabi/kengaku notes above. |
| S10 | `grep -n -i 'AVM\|fritz' …/shokuknow/merge/*` for each merge package | 0 | AVM/FRITZ material exists only in `shokuknow/merge/kaidoku/` (the lane's own staging of rounds 9–14: five `avm-*.md` files, `sasquatch-unblob-avm-branch.md`, and `SOURCES.append.md` S189–S214). No sibling package holds AVM or FRITZ material, so no sibling can adopt AVM first. `merge/revenger` has REA firmware-prerequisite and toolchain entries, without AVM/SquashFS. |

Adjacency anchors checked: the fleet rule on contested scope sits in `PROTOCOL.md:457-461` (not `CORPUS.md`; `CORPUS.md` has no "absorb"/"contested" sentence, `grep -n -i 'contest\|absorb\|adjacen' CORPUS.md` exit 0, no lines). Its text: "Contested scope — evidence or work is reported in the lane report; the integrator arbitrates by refining `PROVINCE.md` and records the ruling in the round notes … silence must never default scope to whichever lane wrote first." `PROTOCOL.md` sha256 `886e459b…4411a`.

## Findings — contested scope (ADJ-06)

| # | path:line | sha256 (first 16) | status |
|---|---|---|---|
| C1 | `revenger-shokunin/PROVINCE.md:3-4,22` — "Owns: reverse engineering of shipped artifacts … archives, firmware" | `6c3694f9…` | contested with kaidoku |
| C2 | `kaidoku-shokunin/PROVINCE.md:3-5` (domain), `:50` archives, `:77` firmware pruned to Core, `:132` Firmware regions + extract row | `d8425c0a…` | contested with revenger |
| C3 | `tsukuroi-shokunin/PROVINCE.md:51` ADJ-06 — recipient "protocol integrator — kaidoku/revenger ownership unresolved" | `177cd834…` | open |
| C4 | `.ufo/l0-questions.md:42` (fleet) — tsukuroi asks the integrator to arbitrate the kaidoku/revenger overlap | `092bd95c…` | open, unruled |
| C5 | `revenger-shokunin/.ufo/waves/round-64/R64ConnectorOverlap.md` — reports the same contradiction, does not absorb | `0ef5d429…` | reported |
| C6 | `tsukuroi-shokunin/.ufo/waves/round-50/w1/R50ConnOverlap.md` — tsukuroi's own round-50 overlap scan; keeps ADJ-06 open | `e506e9e5…` | reported |
| C7 | `MANIFEST.json` roster — revenger and kaidoku both carry near-duplicate "shipped artifacts" domains; tsukuroi (the filer) is absent | `3180866a…` | roster duplicates the contested domain |

Revenger's round-64 C07 entry already carries the correct fence (`revenger-shokunin/corpus/README.md:47`, "authored `firmware-r63.bin` bytes ↔ one saved `inspect_firmware_regions` record only; not kaidoku live firmware or archive Core, not tsukuroi host firmware health, not an ADJ-06 ruling"). This scan does not change any sibling file.

## Findings — in-lane items for the L1 (own lane, not siblings)

These came from checking the R50-C1 ground against the sibling and lane registries. They are defects or conflicts in the draft, reported for the L1 to fold in.

**F-3 (blocker for the carrier pins): the plan's member path is wrong for c6490 and c6430.** Method: `tar-walk.py` lists tar headers by HTTP Range reads, with no data download; receipt `ConnSiblings/tar-walk-r50-carriers.tsv` (sha256 `a023bab0dfa2182b83be14f5da5dbf5fa00ccd3d8dea85a1fc56f06619c98354`) and stderr (`eeeb398d…eaba`).

| carrier (plan) | URL walked | `./var/tmp/filesystem.image` present | LE `hsqs` member actually present | BE/other rootfs member |
|---|---|---|---|---|
| c6490 `fritzbox-6490-cable/deutschland` | `…/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image` | **no** | `./var/remote/var/tmp/x86/filesystem.image` 28200968 B, data @270848 | `./var/remote/var/tmp/filesystem.image` 5443592 B |
| c6430 `fritzbox-6430-cable/deutschland` | `…/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image` | **no** | `./var/remote/var/tmp/x86/filesystem.image` 23863304 B, data @5470720 | `./var/remote/var/tmp/filesystem.image` 5984264 B |
| a7530 `fritzbox-7530/deutschland` | `…/FRITZ.Box_7530-08.25.image` | yes, 34005000 B, data @724992 | — | — |
| a7590 `fritzbox-7590/deutschland` | `…/FRITZ.Box_7590-08.25.image` | yes, 35835912 B, data @24576 | — | — |

- Member counts: 6490 (deutschland and other) 21 members each; 6430 21; 7530 13; 7590 10. Each walk stopped at end-of-archive, with no HTTP error.
- The L1 probe measured `hsqs` 28200968 for 6490 and `hsqs` 23863304 for 6430 (`.ufo/waves/round-50/l1/scan-output.txt` lines 18, 17). Those byte counts equal the x86 member sizes above, so the probe read `x86/filesystem.image`. `scan.py` matched `name.endswith('filesystem.image')`, so the path was never pinned. The probe's "`mkfs_time == bytes_used`" marker therefore applies to the x86 member, not to `./var/tmp/filesystem.image`.
- Consequence: the plan's chain pin (`tar member ./var/tmp/filesystem.image`) yields no member for c6490 and c6430. Under the plan's rule that a carrier failing at the dev arm becomes a recorded negative, both would be recorded negatives for a path error the claim does not own. The L1 should re-pin them to `./var/remote/var/tmp/x86/filesystem.image` (or the path the walk confirms) before the freeze. That is a pre-freeze carrier correction, not a claim change.
- The fetch script inherits the same trap. `tools/round-41/fetch-vendor.py:304,305,316,326` and `tools/round-41/c1-counter.py:2150` hard-code `./var/tmp/filesystem.image`. A port of round-41 `fetch-vendor.py` will fail on the 6490 and 6430 boxes unless the member path becomes a per-carrier field.

**F-4 (novelty of c6490): it is the round-40 V1 image, not a new one.** `corpus/evidence/round-40/c1/V1/provenance.json` pins `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image`, image sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`, length 39741440 (the `other/` URL; the plan uses `deutschland/`). Round 40 chose the BE member `./var/remote/var/tmp/filesystem.image` (carrier `[0,5442392)`, sha256 `ac4098bd…8e95`) and recorded the LE sibling `./var/remote/var/tmp/x86/filesystem.image` (28200968 B, sha256 `7ea4c628…0419`) without claiming it (`.ufo/waves/round-40/w1/artifacts/R40C1VendorV1/CARVE.md:40-41,212`). The `deutschland` and `other` walks give identical member tables and identical total length 39741440, which suggests the same bytes; I did not download the image to confirm the sha256. So the plan's "four public images" includes an image the lane already measured in round 40, and the round-41 reservation check (no REA run on reserved carriers) does not cover this LE member. The L1 should record the overlap in the entry's Limits section.

**F-5 (scope of the L1 probe).** `scan.py` (`l1/scan.py`) ran `probe(m)` over the directory index and took the first member whose name ends in `filesystem.image`. `scan-output.txt` has 70 rows, not the 78 the plan states. Measured: 14 `hsqs` rows, 17 `sqsh` rows, 26 rows `HTTP 416` (Range not satisfiable), and 13 other rows (no `filesystem.image` member or other error, e.g. `./va` first members for 4020/4040). The plan's "dozens publish a `hsqs` member" is therefore overstated against this output (14 rows, of which the 6430/6490 rows measure the x86 member per F-3). Any carrier beyond the four must be re-walked with its member path pinned, and the model count in the plan should be restated from a fresh probe.

Receipts (sha256): `scan-output.txt` `dd9e427d…e1c8` (`.ufo/waves/round-50/l1/`); `scan.py` `764fe01e…495cff`; plan `round-50-claims.md` `83960e43…a03f877`.

## Adjacency sentence (for PROVINCE and the R50-C1 entry)

Recommended for the R50-C1 entry's `## Limits` and the `## Adjacent` note, not a PROVINCE ownership change:

> Reported, not absorbed: the four carriers are public AVM downloads (`download.avm.de` directories) pinned by chain and not committed; no sibling lane holds LE AVM ground, vendor firmware bytes or a registry row for these URLs (`.ufo/waves/round-50/w1/ConnSiblings.md`). Firmware ownership between kaidoku and revenger remains the open arbitration ADJ-06 (`tsukuroi-shokunin/PROVINCE.md:51`; fleet `.ufo/l0-questions.md:42`); `revenger-shokunin/PROVINCE.md:3-4` also names firmware in its domain. This entry does not rule ADJ-06, does not absorb kaidoku's Core firmware-regions or archive rows, and does not cite any sibling file as support. The c6490 carrier is the round-40 V1 image; its LE member is the one round 40 recorded and did not claim.

## Risks

- ADJ-06 can be quoted from this entry as settled. The sentence above blocks that.
- A carrier re-pinned to the x86 member without a fresh chain walk would repeat the path error. Each pin needs the walk receipt, not the probe.
- The magic check (S8) covers only ≥256 KiB files with firmware-like names. A sibling holding a small or oddly named image would not appear there. S1–S7 and S9–S10 cover the same claim from the text side.

## Commands and exit codes

- `sha256sum` on all cited files: exit 0 (hashes in the findings tables).
- `tar-walk.py` on five URLs (four planned carriers and the round-40 6490 `other/` control): exit 0, 87 rows, stop reasons `end-of-archive` for all five; stderr receipt `tar-walk-r50-carriers.stderr` (sha256 `eeeb398d…eaba`). Range requests only; no member data downloaded; no response header stored.
- `sha256sum -c receipts.sha256`: exit 0, four OK.
- Not run: any REA, unblob, sasquatch or counter run; any full image download; any sibling tool. No install, so no tool version to record.
- `git status --porcelain -- <seat dir>`: read-only check, exit 0.
- `rm -rf` of my scratch dir: exit 0.

Authority lines: the verdict and findings are my observation with the commands above. The adjacency sentence and the F-3 correction are recommendations for the L1, not rulings on ADJ-06.
