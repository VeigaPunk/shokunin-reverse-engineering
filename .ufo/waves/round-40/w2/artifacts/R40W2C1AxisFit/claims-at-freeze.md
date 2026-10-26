# kaidoku round 40 — frozen claims

Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` (lane `main`; the round-39 closure spot-check sits on
the round-39 tip `8b9634ed`). L1 `KaidokuR40` holds the §3 planner seat. Wave 1 (42 seats,
`.ufo/waves/round-40/w1/`) built and attacked the draft of this file; every change from the draft is in
`## Changes from the draft`. The rule for each claim is the bytes of this file, its tools and its frozen
inputs in the commit that first adds this version (the freeze, QUALITY 79). Controls are scored before
any claim data exists.

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis is a
lowest axis. R40-C1 works coverage, R40-C2 works depth. The round-39 `planned` row named (a) making the
C1 fabrication limit executable and (b) an out-of-set envelope the triage table must label
`unclassified` first, and AVM-BE coverage second: (a) is a binding inside R40-C1, (b) is part of R40-C2.

## Freeze-integrity rule (both claims; carried from round 39)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path of that claim; a
later restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`). Control tables and
their development inputs are committed and format-validated in the freeze commit (routed R39-CL4). Every
score receipt records the scorer's exit code (R39-CL6).

## R40-C1 — coverage: genuine AVM-layout big-endian SquashFS v4 moves from Frontier to Core

Surface moved: PROVINCE Frontier — the round-39 frontier note "AVM-BE bodies and vendor-mangled images
stay Frontier" (`PROVINCE.md:384`) and the `corpus/README.md` `## Frontier` sasquatch-v4be line. Command
that shows it unmoved: the C1 counter at the freeze exits 1 (no round-40 receipts, no
`## Round-40 additions to Core`).

Genuine AVM layout (stated from sources before data): a big-endian SquashFS 4.0 superblock (`sqsh`) whose
structural fields are big-endian while the 2-byte metadata block-length headers are little-endian
(Freetz `AVM-BE-format.txt` line 8, lane S114; Freetz `350-unsquashfs__AVM_BE.patch`, opened round 40),
with the AVM marker `mkfs_time == bytes_used`, for which unblob 26.6.4's `squashfs_v4_be` handler runs
`sasquatch-v4be` without `-be` (S112 lines 44-50). The marker is the trigger; the block-length
endianness is the format: the round-39 writer's `--endian avm` (marker on a standard-BE body) is not
this layout.

**Predicate P40-C1.** At the measured revision, for each of the four frozen carriers (V1, V2, L1, L2), the
committed round-40 REA 6.5.0 `extract-firmware` after-receipt (unblob 26.6.4, sasquatch-v4be 4.5.1 on
the child PATH, `--max-depth 1`), first added in a commit that descends from the freeze, names the
`squashfs_v4_be` handler with no failed chunk, publishes every regular file of the frozen independent
oracle (same relative-path suffix, same sha256), carries extraction gaps only as the frozen gap rule
allows (one `unpublished-entry` per symlink, none for directories or devices, at most one
`depth-limited` and no `unknown-chunk-handler`), has a subject digest equal to the carrier pin and
recomputes to its evidence id; the carrier bytes hash to the pin and carry the AVM marker with
little-endian metadata block lengths; a fresh REA run of the same carrier bytes made by the counter at
scoring time has the same `plus-extractor` projection as the committed receipt; the frozen reader at the
freeze, run on each carrier, reproduces its frozen oracle and non-regular tables; PROVINCE.md holds a
`## Round-40 additions to Core` row naming the AVM layout that cites the round-40 entry
`corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, which cites a SOURCES row absent at the base
whose used-by lists it; a `Round-40 frontier note` line names that heading and the entry stem and says
what it supersedes; corpus/README.md maps the entry stem; and no frozen C1 path changed after the freeze.

- Carriers (`.ufo/waves/round-40/c1/carriers.json`, sha256 pins, projection profile `plus-extractor`):
  - **V1** vendor: `FRITZ.Box_6490_Cable-07.57.image` (download.avm.de, image sha256 `f518ce6b…ede6d`),
    tar member `./var/remote/var/tmp/filesystem.image`, bytes `[0, bytes_used = 5442392)`, carrier
    sha256 `ac4098bd…8e95`; 697 regular files, 263 symlinks, 117 directories, 1 character device.
  - **V2** vendor: `FRITZ.Box_6820v1_LTE-07.30.image` (image sha256 `3948449d…9450`), member
    `./var/tmp/filesystem.image`, bytes `[0, 26013550)`, carrier sha256 `5ccc7614…089b`; 8 regular
    files (one is a nested `filesystem_core` image, not opened at depth 1), 85 symlinks, 1 device.
    Different model family and FRITZ!OS version from V1; no REA or unblob run touched V1 or V2 before
    the freeze.
  - **L1** lane-built xz, **L2** lane-built gzip: `tools/round-40/mk-l-carriers.py` through
    `tools/round-40/gen-squashfs.py --endian avm-genuine`, each with one in-tree relative and one
    absolute symlink; byte-deterministic (built twice, same sha256).
  - Vendor bytes are never committed (the AVM licence forbids redistribution; wave-1
    `R40SrcAvmVendor`): `tools/round-40/fetch-vendor.py` rebuilds them from the pinned chain into a
    cache and the counters read `--carrier-cache`.
- Oracle: `tools/round-40/sqfs-list.py --layout avm` (pure stdlib, independent of unblob/sasquatch
  code); its file list equals a direct `sasquatch-v4be` (no `-be`) extraction on all four carriers
  (`corpus/evidence/round-40/c1/*/oracle-run.json` `crosscheck`, 0 mismatches).
- Target: `carriers_matched == 4`, every counter binding true, and the supplementary gate met.
- Counting commands (both must exit 0):
  `python3 -I -B tools/round-40/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache <CACHE> --json-out <OUT>`
  and `python3 -I -B tools/round-40/c1-extra.py --root <LANE> --rev <REV> --freeze <FREEZE> --base fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f --carrier-cache <CACHE> --json-out <OUT>`,
  with `<CACHE>` filled by `python3 -I -B tools/round-40/fetch-vendor.py --root <LANE> --rev <FREEZE> --cache <CACHE>`.
  Self-tests: c1-counter 70 cases, c1-extra 7, fetch-vendor 8, sqfs-list, gen-squashfs.
- Data procedure (after the freeze, never before): `tools/round-40/c1-run.sh after <carrier bytes>
  corpus/evidence/round-40/c1/<id> <scratch under /kaidoku-r40/>`.
- Kill rule: a control meeting the target stops C1 before any carrier run. Controls: CTL-C1-0 the
  do-nothing state at the freeze (real counter); the counter's 65 red self-test cases, which include a
  re-minted fabrication refused by the rerun projection, round-39 receipts relabelled, a marker-only
  standard-BE carrier, a marker-stripped genuine body, receipts in the freeze commit, a frozen-path touch
  then restore, a trimmed published set and an extra gap; c1-extra's red cases (trimmed oracle, old S-id,
  presence-only frontier note). A miss at the measured revision is an honest stop.
- Disclosed limits: the rerun shows the carrier extracts through the pinned toolchain at scoring time; it
  cannot prove which process wrote the committed receipt, and a receipt equal to a real run on the
  projection is accepted by design. REA records no extractor argv on success, so the absence of `-be` is
  shown by the AVM handler branch and direct `unblob -v` logs, not by the receipt.
- Not claimed: the nested `filesystem_core` image inside V2, LE AVM members (`hsqs`), AVM kernel images,
  vendor images other than V1/V2, anything about extracted programs.

## R40-C2 — depth: SquashFS outcome-triage table v2 in the SKILL craft section

Surface moved: `SKILL.md` `## Queue-drain craft` gains rule block 19 with
`<!-- sqfs-triage-table v2 -->` and `<!-- sqfs-triage-actions: … -->` (eleven unique labels, eleven
action tokens, columns `operation` and `provider` first), backed by
`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`; block 18 keeps the v1 table bytes and gains a
supersession sentence. Command that shows it unmoved: the frozen v2 interpreter on the base `SKILL.md`
exits 2 (no v2 marker), and the C2 counter at the freeze exits 2 (no held-out manifest).

**Predicate P40-C2.** At the measured revision, the frozen interpreter `tools/round-40/sqfs-triage-v2.py`,
reading only the SKILL v2 table, assigns every held-out envelope the (label, action) pair its frozen
generator `tools/round-40/heldout-gen-v2.py` assigned before any REA run, for all 26 envelopes (13
classes × 2); the seed is the freeze commit hash; every carrier regenerates byte-identically; every
envelope's subject digest equals its carrier; the manifest is first added after the freeze and no later
than its envelopes; the v2 table bytes equal the freeze bytes; each expected pair maps to one table row
(the no-match pair to none) and different pairs to different rows.

- Classes → (label, action): clean-be, clean-le → (clean, none); clean-empty → (clean-empty,
  confirm-empty); escaping-symlink-removed → expect-link-absent; in-tree-symlink-metadata → count-gap;
  mixed-symlinks → audit-symlinks; dep-missing-be → install-extractor-be; dep-missing-le →
  install-extractor-le; avm-marker-be-dropped → wrap-extractor-be; body-extractor-failure →
  preserve-failure; partial-body-failure (gzip) → salvage-partial; no-squashfs-chunk → inspect-input;
  out-of-domain (`inspect-firmware-regions`, provider `binwalk`) → (unclassified, none).
- Target: `matched == 26`, every counter binding true, `met_target` asserted equal to that.
- Counting command: `python3 -I -B tools/round-40/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
  Self-tests: c2-counter 42 cases, sqfs-triage-v2 45, heldout-gen-v2 6 checks.
- Data procedure (after the freeze, never before):
  `python3 -I -B tools/round-40/heldout-gen-v2.py --seed <FREEZE> --out corpus/evidence/round-40/c2/heldout --run`.
- Kill rule: a control at 26/26 on the 26 development envelopes (seed `sha256("dev40")`,
  `.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/dev-run/`) stops C2 before held-out generation.
  Controls (`.ufo/waves/round-40/controls/c2/`, each format-validated with `--table-only`; scores
  `.ufo/waves/round-40/controls/c2-dev-scores.json`): CTL-C2-0 base SKILL (exit 2, 0/26); CTL-C2-1
  catch-all (4/26); CTL-C2-2 the v1 table transcribed with the adopted actions (18/26: misses clean-empty,
  mixed, partial, out-of-domain); CTL-C2-3 actions rotated (2/26); CTL-C2-4 no domain guard (24/26);
  CTL-C2-5 no mixed row (24/26); CTL-C2-6 a final `*` default row (24/26). A miss at the measured revision
  is an honest stop.
- Disclosed limits: a table with one load-bearing cell per label can also score a closed class set
  (wave-1 `R40C2AxisFit` (c)); the `cause` column is prose and unscored; operation and provider change
  together in the out-of-domain class, so the provider cell is not tested alone.

## Separability

C1 reads PROVINCE/README/SOURCES/knowledge, its receipts, carriers, oracles and reruns; C2 reads SKILL.md,
its interpreter, generator and held-out evidence. Neither reads the other's data; they share SOURCES rows
only as citations, and the v2 AVM-marker row's cause points to the C1 entry by name only.

## Frozen paths

C1: this file; `tools/round-40/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-vendor.py,sqfs-list.py,gen-squashfs.py,mk-l-carriers.py}`;
`.ufo/waves/round-40/c1/{carriers.json,gap-rule.json}`; every carrier, oracle and non-regular table
carriers.json names. C2: this file; `tools/round-40/{sqfs-triage-v2.py,heldout-gen-v2.py,c2-counter.py}`;
the SKILL v2 table block; `tools/round-39/gen-squashfs.py` (the generator's writer).

## Changes from the draft

- Carriers: V2 is the 6820v1 LTE 07.30 member, not the scout's 7430 07.31 pick, because a recon seat ran
  REA on the 7430 and 7490 members (`w1/R40C1ReconGaps.md` §1). Vendor bytes are fetched, not committed
  (`w1/R40SrcAvmVendor.md`, licence). Carriers are carved to `bytes_used` and all runs use `--max-depth 1`:
  at the default depth a vendor member exceeds REA's 10000 staged-entry budget (`w1/R40C1ReconGaps.md`
  §6, `w1/R40C1ReconWrap.md`); a dev run of the 6590 member carved the same way gives one
  `squashfs_v4_be` chunk, 697 files, 263 `unpublished-entry` + 1 `depth-limited` gaps.
- Gap rule: one gap per retained symlink, devices invisible, structural `depth-limited` ≤ 1 and no
  `unknown-chunk-handler` (`w1/R40C1ReconGaps.md` §4); kind vocabulary from the reader.
- Rerun projection: `plus-extractor`, because the draft's six fields are oracle-closed — an oracle-only
  fabrication matches them (`w1/R40C1Projection.md` §6).
- Added `tools/round-40/c1-extra.py`: oracle re-derivation by the frozen reader, a SOURCES id absent at the
  base, frontier-note content (`w1/R40C1Controls.md` §4 D3–D5).
- C2: the `operation`/`provider` guard and action column follow the interpreter seat's grammar
  (`w1/R40C2Interp.md`); the AVM-marker row's cause now states the genuine-layout case
  (`w1/R40C2AxisFit.md` (e), `w1/R40C2ActionReview.md`); block 18 gains a supersession sentence instead of
  staying the only live table (`w1/R40C2AxisFit.md` (d)); the partial-body class is pinned to gzip and
  the counter accepts the row-less no-match pair, after an L1 dry run on a sandbox clone showed a zeroed
  single-block xz file extracting clean and the counter rejecting the out-of-domain rows.
