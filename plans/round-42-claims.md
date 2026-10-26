# kaidoku round 42 — claims (DRAFT, not frozen)

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (lane `main`; the round-41 closure spot-check
`corpus/lessons/round-41-verifier-spotcheck.md` sits on it). L1 `KaidokuR42` holds the §3 planner seat. Wave 1
builds and attacks this draft; the freeze is the commit that first adds the final version of this file, and every
change from this draft is listed in `## Changes from the draft` there. Controls are scored before any claim data.

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis is a lowest axis.
R42-C1 works coverage, R42-C2 works depth. The round-41 `planned` row named depth first (refreeze the triage claim
with one declared-tuple key, a frozen-counter dry run, and combos a named-class lookup cannot reach); its routed
defect R41-CL4 (the v3 table sends every SquashFS v1–v3 chunk to `no-squashfs-chunk`, `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:22-25`)
is the reason the depth claim is a new table (v4) and not a re-score of v3: prompt §9 says re-scoring a rule the
lane already holds on new inputs is quality work, never depth.

## Freeze-integrity rule (both claims; carried from rounds 39–41)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path of that claim; a later
restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`). Control tables and their development
inputs are committed in the freeze. Every score receipt records the scorer's exit code **and the sha256 of the
counter file it ran** (round-41 closure D4). QUALITY 84: every counter is dry-run end to end, as frozen, on the dev
arm before the freeze, with every binding evaluated in the dry-run receipt.

## R42-C1 — coverage: SquashFS v3 (unblob `squashfs_v3*` handlers) through REA `extract-firmware`, Frontier → Core

Surface moved: the lane holds SquashFS v1–v3 only as a producer statement (`corpus/knowledge/2026-10-26-unblob-format-matrix.md`,
"coverage claim only, never an extraction outcome") and as the v3 table's `no-squashfs-chunk` cause text; no REA
run on a v3 chunk is in the corpus. After the move PROVINCE holds `## Round-42 additions to Core` naming the
`squashfs_v3` handler family, a knowledge entry `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`, a README
coverage-map row, and new SOURCES rows for the carriers' publishers. Command that shows it unmoved: the C1
counter at the freeze exits 1 (no round-42 receipts, no Core row).

Draft predicate P42-C1. At the measured revision, for each frozen carrier (count fixed at the freeze, target 4), the
committed round-42 REA 6.5.0 `extract-firmware` after-receipt (`--max-depth 1`, unblob 26.6.4, sasquatch 4.5.1 on
the child PATH), first added in a commit descending from the freeze, names a `squashfs_v3*` handler (the one frozen
per carrier) with no failed chunk; publishes every regular file of the frozen independent oracle at its exact
relative path under the chunk extract root (round-41 exact-path rule, segment-bounded per round-41 closure D5) with
the same sha256 and size, and no non-regular oracle entry as a file; accounts for every non-regular oracle row by
the frozen gap rule (one `unpublished-entry` gap or one `MaliciousSymlinkRemoved` diagnostic per symlink; devices
and directories invisible; at most one structural `depth-limited`; no `unknown-chunk-handler`); has a subject
digest equal to the carrier pin and recomputes its evidence id; the carrier bytes hash to the pin and their
superblock reads the frozen magic/major/compression; a counter-time REA rerun has the same projection; PROVINCE,
entry, README row and a SOURCES row absent at the base whose used-by lists the entry exist; no frozen C1 path
changed after the freeze.

- Carriers (wave 1 decides; reservation binding from this draft on): four **published third-party images** of the
  v3 family (a real distribution or vendor rootfs, e.g. DD-WRT v24 `tqsh`, an OpenWrt Kamikaze 8.09 squashfs-3.0
  image, a vendor firmware with an `hsqs`/`sqsh` major-3 rootfs). unblob test fixtures belong to C2 and are never C1
  carriers; OpenWrt Kamikaze 7.09 is designated development. Development input already burned by the L1:
  `tests/integration/filesystem/squashfs/squashfs_v3/little_endian/__input__/squashfs_v3_le.bin` (probe 2026-10-26,
  about 21:40Z, plain `unblob -d 2`, 2 files, fetched from the `main` LFS path).
- Oracle: two producers that are not sasquatch — `unsquashfs` 4.7.5 (reads v1–v3 gzip) and a second reader
  (7-Zip's SquashFS handler, or a lane stdlib v3 reader) — must agree file-for-file before a carrier freezes.
- Target: `carriers_matched == 4`, every binding true.
- Kill rule: a control meeting the target stops C1 before any carrier run (CTL-C1-0 do-nothing at the freeze;
  CTL-C1-1 the round-41 receipts relabelled to round-42 paths; CTL-C1-2 an oracle-only fabricated receipt).
- Not claimed: v1/v2 images, v4 Broadcom, anything about extracted programs.

## R42-C2 — depth: SquashFS outcome-triage table v4 covering the whole SquashFS handler family

Surface moved: `SKILL.md` `## Queue-drain craft` gains rule block 21 with `<!-- sqfs-triage-table v4 -->`, its
action line and `corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md`; block 20 gains a supersession sentence.
Command that shows it unmoved: the frozen v4 interpreter on the base `SKILL.md` exits 2 (no v4 marker); the v3
table transcribed under the v4 marker (CTL-C2-0b) labels every legacy-chunk envelope `no-squashfs-chunk` or
`unclassified`.

Draft label precedence (expected pairs come from this text through an independent evaluator). Features as round
41 (OP, PR, H, G, D, BE, SR, P; `plans/round-41-claims.md:109-115`), plus F = the set of SquashFS handler names in
H (`squashfs_` prefix). Steps, first match wins:

1. OP ≠ `extract_firmware` or PR ≠ `unblob` → (`unclassified`, `none`).
2. F = ∅ → (`no-squashfs-chunk`, `inspect-input`).
3. `missing-extractor-dependency` ∈ G: D holds `sasquatch-v4be` → (`dep-missing-be`, `install-extractor-be`); else D
   holds `sasquatch` → (`dep-missing-le`, `install-extractor-le`) — every v1–v3 chunk and every v4 LE chunk resolves
   plain `sasquatch` [to be confirmed by wave 1 on real REA envelopes; label wording may change]; else continue.
4. `extractor-failure` ∈ G and P > 0 → (`partial-body-failure`, `salvage-partial`).
5. `extractor-failure` ∈ G, P = 0, BE = `no`, failing handler `squashfs_v4_be` → (`avm-marker-be-dropped`, `wrap-extractor-be`).
6. `extractor-failure` ∈ G, P = 0, failing handler a v1–v3 handler → (`legacy-body-failure`, `cross-read-legacy`)
   [new; the AVM layout pre-check does not apply to a v1–v3 superblock; the action is to cross-read the chunk with
   `unsquashfs` to separate damage from an extractor build fault — wave 1 confirms or replaces].
7. `extractor-failure` ∈ G, P = 0 → (`body-extractor-failure`, `preserve-failure`).
8. `depth-limited` ∈ G → (`depth-limited`, `raise-depth`).
9. SR = yes and `unpublished-entry` ∈ G → (`mixed-symlinks`, `audit-symlinks`).
10. SR = yes and G = ∅ → (`escaping-symlink-removed`, `expect-link-absent`).
11. G = {`unpublished-entry`} → (`in-tree-symlink-metadata`, `count-gap`).
12. G = ∅: P > 0 → (`clean`, `none`); P = 0 → (`clean-empty`, `confirm-empty`).
13. anything else → (`unclassified`, `none`).

Draft predicate P42-C2. At the measured revision the frozen interpreter `tools/round-42/sqfs-triage-v4.py`, reading
only the SKILL v4 table, gives every held-out envelope the same (label, action) pair as the frozen evaluator
`tools/round-42/indep-eval-v4.py` (written from the precedence text only); the held-out set is
`tools/round-42/heldout-gen-v4.py --seed <FREEZE>`: the round-41 v4 classes, new legacy-family classes built from
unblob 26.6.4 v1–v3 fixtures pinned in the freeze (clean per handler, dependency missing, zero-file and partial
body damage), and a widened `combo` family whose factors include the handler family; every envelope's observed
feature tuple equals the tuple the manifest declares under ONE key (`declared_features`), read by the counter
under exactly that key (R41-CL1); carriers regenerate byte-identically; the manifest is first added after the
freeze; the v4 table bytes equal the freeze bytes; the round-41 C1 receipts (real AVM rootfs envelopes) and the
round-42 dev-arm real legacy envelopes get the evaluator's pair.

- Target: `matched == n`, every binding true, and the frozen lookup control CTL-C2-7 (named-class tuples from the
  dev set, exact) scores strictly fewer than half of the held-out combos (R41 w2 `R41W2C2Combos.md`: 8/12).
- Kill rule: any control at full score on the development envelopes stops C2 before held-out generation.
- Controls: CTL-C2-0 base SKILL; CTL-C2-0b the v3 table under the v4 marker (do-nothing on the surface);
  CTL-C2-1 catch-all; CTL-C2-3 actions rotated; CTL-C2-4 exact sets only; CTL-C2-7 lookup; CTL-C2-8 v4 without the
  legacy-failure row; CTL-C2-9 v4 with the handler cell left at `squashfs_v4_*`.

## Separability

C1 reads PROVINCE/README/SOURCES/knowledge, its receipts, carriers, oracles and reruns. C2 reads SKILL.md, its
interpreter, evaluator, generator, controls, the pinned unblob fixtures (none of them a C1 carrier) and the
round-41 C1 receipts. Neither reads the other's round-42 data.

## Frozen paths (draft)

C1: this file; `tools/round-42/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-carrier.py}` and the oracle tools;
`.ufo/waves/round-42/c1/{carriers.json,gap-rule.json}`; every carrier pin, oracle and non-regular table.
C2: this file; `tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,heldout-gen-v4.py,c2-counter.py}`, the writer
and fixture pins the generator reads; the SKILL v4 block; the control tables.
