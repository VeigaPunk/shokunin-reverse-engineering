# R44ConnSibling — cross-sibling overlap scan (round 44, wave 1)

Seat: R44ConnSibling (connector, read-only). Base `c29360e3ba5381a5ab69e372d0d9577970f85018`
is an ancestor of HEAD `f5fb8d59`; `git diff --name-only` base→HEAD over the frozen C1/C2
paths is empty (receipt R-07). This seat wrote only this report, its seat receipts, and its
seat artifact; no other lane or fleet path was written.

## Axes named

- coverage (C1: SquashFS v1/v2 Frontier → Core), depth (tied with coverage; the owned-axes
  tie rule in `plans/round-44-claims.md` makes all three owned axes lowest), calibration (C2).
- This seat's scan is about surface ownership, not a score. It moves no axis.

## Verdict

| Claim | Surface it writes | Sibling adjacency found | Verdict |
|---|---|---|---|
| R44-C1 | `PROVINCE.md` Round-44 row, `corpus/README.md` map row, `corpus/SOURCES.md` S138/S139, `corpus/knowledge/2026-10-28-r44-*`, `tools/round-44/c1-*`, `corpus/evidence/round-44/c1/` | revenger (firmware domain word, F-axis via `inspect_firmware_regions`); tsukuroi (the oracle is a pacman-owned package) | **Clear, with a stated boundary** (F1, F4) |
| R44-C2 | `SCORECARD.md`, `SHONEN.md`, `corpus/README.md` (kaidoku's own), `tools/round-44/c2-*`, `tools/round-44/c2-rubric.json` | none sibling-owned; one cross-root pointer hazard inside kaidoku's own README (F7) | **Clear**; rubric must declare its pointer root |
| tooling surface | — | none claimed | **No collision** (F5) |
| builds surface | — | none claimed; no lane named `builds` located (F6) | **No collision** |

No C1 or C2 surface is sibling-owned. `PROVINCE.md`'s contested rule is invoked only for
runtime rows (ADB, Frida, live debugger verbs; `PROVINCE.md:185`, `:249`, `:281`, `:312`), and
none of those rows is a squashfs or firmware-extraction row.

## Findings

**F1 — firmware: adjacent to revenger, not owned by it.** `revenger-shokunin/PROVINCE.md:4`
lists "firmware" in its domain. Its only firmware mentions are a tool census
(`PROVINCE.md:22`, Binwalk/Unblob) and the F-axis record-family row
(`SCORECARD.md:179`: "author an inert known-truth firmware fixture and run REA
`inspect_firmware_regions`"). Neither names `extract-firmware`, `squashfs`, or a SquashFS
family (receipt R-01: the `extract-firmware` grep over revenger's PROVINCE and SKILL returns
no hits, exit 1 = no match). kaidoku's extraction rows already own this verb
(`PROVINCE.md:372`, `:382`, `:400`, `:414`). Proposed boundary for the C1 Core row (text
only, for the L1 to decide): it counts `extract-firmware` extraction receipts; it does not
count `inspect_firmware_regions` family records, which stay revenger's F-axis.
Game-dev-3d's `SCORECARD.md:307` mention is a Binwalk/Unblob tool census inside another lane's
repair notes; no squashfs claim.

**F2 — binary linkage is kaidoku's.** `kengaku-shokunin/PROVINCE.md:333`, `:347-349` routes
real `DT_NEEDED`/`dlopen` linkage to kaidoku's ELF ground. Not on C1/C2's surface.

**F3 — the C1 extraction arm uses only lane-owned tools.** `c1-run.sh` is registered in
kaidoku's SKILL registry with owner `kaidoku` (`SKILL.md:1567`); the counter is a Python
file in `tools/round-44/`. `sasquatch` 4.5.1 is `~/.local/bin/sasquatch` (kaidoku's round-4
install, `PROVINCE.md:372`); `unblob` 26.6.4 is `~/.local/bin/unblob` (symlink into uv tools).
Neither is a sibling artifact.

**F4 — the oracle is a host package owned by tsukuroi.** `/usr/bin/unsquashfs` is owned by
`squashfs-tools 4.7.5-1` (pacman; receipts R-10/R-11). tsukuroi owns pacman state
(`tsukuroi-shokunin/PROVINCE.md`, "pacman state"). C1 reads the binary, never installs or
upgrades it. Pacman stays paused per the addendum guard; `RULES.md`'s install channels are not
needed for C1 and no install is planned. If the oracle version changes before the freeze, the
S139 identity pin must be re-read, because the frozen `-lls` digests depend on it.

**F5 — tooling.** No lane named `tooling` exists in the fleet root. The closest sibling is
`kumitate-shokunin` ("orchestration & tooling — OMP task/hub, ufo-fsd scripts & runtime",
its PROVINCE header). C1/C2 touch none of those surfaces. kaidoku's own `PROVINCE.md:119-125`
records the operator tooling directive as a host-level rule; C1 installs nothing under it.

**F6 — builds.** No lane named `builds` exists among the fleet directories (scan of
`/home/vgpnk/Projects/shokunin/*/`; receipt R-08 lists the directories). C1 and C2 compile
nothing: C1 is a Python counter plus prebuilt binaries; C2 is a Python counter plus text
reads. No compiled-codebase surface is claimed. (Bare word hits for "builds" in kaidoku's
docs at `PROVINCE.md:52` and `corpus/README.md:35,63,174` are historical Go-binary build
identities, not a sibling surface.)

**F7 — C2 cross-root pointer hazard (kaidoku-internal).** `corpus/README.md:35` cites
`kaidoku-shokunin/.ufo/waves/round-16/selection.py`, `round-17/run-carriers.sh`, and
`round-18/run-carriers.sh`. These resolve only from the fleet root: the lane-root paths exist
(`.ufo/waves/round-16/selection.py` etc., receipt R-02), and
`kaidoku-shokunin/kaidoku-shokunin/.ufo/...` does not. So under the lane-root convention these
three pointers are dangling; under the fleet-root convention they resolve. This is a candidate
C2 mismatch of the category-(f)/(a) kind. I did not repair it. Recommended: R44C2Rubric or
R44ScoutCalib decides the root, records it in the rubric, and the repair is an appended
correction (per the C2 landing rule), not a rewrite of `corpus/README.md:35`.

**F8 — C2 reuse.** kaidoku already owns a citation-drift gate
(`.ufo/gates/citation-drift/citation-drift-probe.py`, `SKILL.md:676`, registry owner
`gate / kaidoku`). It is the natural checker for rubric categories (a) and (c) and it is
lane-internal, so it adds no sibling dependency. Not verified by this seat; the seat only
confirms the path is registered.

**F9 — frozen-path integrity.** The C1 and C2 frozen-path set is kaidoku-owned in full. The
freeze-integrity rule's `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`,
`corpus/SOURCES.md` are written only by kaidoku seats. No sibling writes to them (no sibling
lane references their paths except as read-only citations).

**F10 — working-tree note (not this seat's).** `git status` at HEAD shows
`M .ufo/waves/round-44/w1.ready.partial` (orchestrator-written marker). Not touched by this seat.

## Receipts

Runner: `.ufo/waves/round-44/w1/artifacts/R44ConnSibling/overlap-receipts.py` (read-only;
writes one JSON line per check). Output: `.ufo/waves/round-44/w1/R44ConnSibling/receipts.jsonl`,
sha256 of the file `7f700234a1d3fccee07f523ef7801d52c928ef6c3fdab216c882e9768110e352`.

Disclosure: the first run of the runner had an unescaped regex flag on the arbitration check
(exit 1, `-E` missing); I fixed the argv and re-ran. The receipt file is from the corrected
run. `tsukuroi-shokunin/PROVINCE.md` and `game-dev-3d-shokunin/SKILL.md` were in the scan list;
the second's absence did not change any result.

| ID | check | exit | stdout lines | wall s | meaning |
|---|---|---|---|---|---|
| R-01 | sibling-extract-firmware-verb (revenger PROVINCE+SKILL) | 1 | 0 | 0.0008 | no `extract-firmware` in revenger (grep no-match) |
| R-02 | c2-surface-sibling-path-refs (`corpus/README.md` pointers) | 0 | 3 | 0.0015 | the three fleet-root-relative pointers (F7) |
| R-03 | sibling-squashfs-hits | 0 | 3 | 0.0012 | revenger PROVINCE:22, revenger SCORECARD:179, game-dev-3d SCORECARD:307 (F1) |
| R-04 | kaidoku-contested-rule | 0 | 1 | 0.0006 | the single contested-scope line `PROVINCE.md:185` |
| R-05 | kaidoku-revenger-arbitration | 0 | 6 | 0.0006 | runtime-only arbitration rows (F-verdict) |
| R-06 | c1-surface-exists / c2-surface-exists | 0 | 22 / 3 | ~0.002 | surfaces present at base |
| R-07 | base-is-ancestor-of-head; frozen-surface changes base→HEAD | 0 | 0 / 0 | ~0.001 | base is ancestor; no frozen-path diff |
| R-08 | sibling dirs (fleet, `ls -d */`) | (manual; not a runner check) | 25 dirs | — | no `tooling`/`builds`-named lane |
| R-10 | oracle-package-owner (`pacman -Q`, `-Qo`) | 0 | 2 | 0.0907 | `squashfs-tools 4.7.5-1` owns `/usr/bin/unsquashfs` |
| R-11 | oracle-binary-version | 0 | 1 | 0.0016 | `unsquashfs version 4.7.5 (2026/03/01)` |

R-08 is a manual directory listing, not a runner check; its count (25 directories) is from the
`ls -d */ | wc -l` run in the transcript. The runner's wall times are per-check `time.time()`
deltas; the sha256 values are over the captured stdout.

## Checks for the main agent (after landing, not run by this seat)

- `python3 -I -B .ufo/waves/round-44/w1/artifacts/R44ConnSibling/overlap-receipts.py` should
  reproduce the same stdout hashes at the same HEAD.
- Confirm the C2 rubric's pointer root for the three `corpus/README.md:35` pointers (F7).
- Confirm C1's Core row text names `extract-firmware` and states the `inspect_firmware_regions`
  boundary (F1).
