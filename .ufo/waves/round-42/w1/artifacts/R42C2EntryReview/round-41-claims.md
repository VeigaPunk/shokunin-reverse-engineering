# kaidoku round 41 — frozen claims

Base `49096c7e6f226af0c750c4b003be58883cb6049f` (lane `main`; the round-40 closure spot-check
`corpus/lessons/round-40-verifier-spotcheck.md` sits on it). L1 `KaidokuR41` holds the §3 planner seat. Wave 1
(41 seats, `.ufo/waves/round-41/w1/`) built and attacked the draft of this file; every change from the draft is
in `## Changes from the draft`. The rule for each claim is the bytes of this file, its tools and its frozen inputs
in the commit that first adds this version (the freeze). Controls are scored before any claim data exists.

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis is a lowest axis.
R41-C1 works coverage, R41-C2 works depth. The round-40 `planned` row named the C1 refreeze first and table v3
second; the round-40 closure routed D1 (S126 durability), D3 (score the next table on labels not taken from the
generator's class map) and confirmed R40-CL1.

## Freeze-integrity rule (both claims; carried from rounds 39–40)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path of that claim; a later
restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`). Control tables and their
development inputs are committed in the freeze. Every score receipt records the scorer's exit code
(`tools/round-40/score-receipt.sh`).

## R41-C1 — coverage: genuine AVM-layout big-endian SquashFS v4 moves from Frontier to Core

Surface moved: PROVINCE `## Round-40 measured, not promoted (R40-C1 honest stop)` and the round-39 frontier
note's AVM sentence ("AVM-BE bodies … stay Frontier"), and the `corpus/README.md` `## Frontier` sasquatch-v4be
line. The round-40 Frontier → Core move did not land (round-40 closure: coverage unchanged); this claim lands
it on four carriers no REA or unblob run touched before the freeze, one of them the first full vendor AVM rootfs
the lane has measured (V4, 6349 regular files; round 40 measured a 697-file cable member and an 8-file wrapper).
Command that shows it unmoved: the C1 counter at the freeze exits 1 (no round-41 receipts, no
`## Round-41 additions to Core`).

Layout (stated from sources before data; unchanged from round 40): a `sqsh` SquashFS 4.0 superblock whose
structural fields are big-endian while metadata/data block-length headers are little-endian (S114, S124), with
the marker `mkfs_time == bytes_used`, for which unblob 26.6.4 `squashfs_v4_be` runs `sasquatch-v4be` without
`-be` (S112 :44-50).

**Predicate P41-C1.** At the measured revision, for each of the four frozen carriers V3, V4, L3, L4, the committed
round-41 REA 6.5.0 `extract-firmware` after-receipt (`--max-depth 1`, unblob 26.6.4, sasquatch-v4be 4.5.1 on the
child PATH), first added in a commit that descends from the freeze, names the `squashfs_v4_be` handler with no
failed chunk; maps every receipt path to the oracle's namespace by the exact-path rule below and publishes every
regular file of the frozen independent oracle at that exact relative path with the same sha256 and size, and
no non-regular oracle entry as a file; accounts for every non-regular oracle row as the frozen gap rule allows
(each symlink row exactly once: one `unpublished-entry` gap at its exact path or one `MaliciousSymlinkRemoved`
diagnostic at its exact path; devices and directories invisible; at most one structural `depth-limited`, no
`unknown-chunk-handler`; every removal diagnostic resolves to a symlink row); has a subject digest equal to the
carrier pin and recomputes to its evidence id; the carrier bytes hash to the pin, carry the AVM marker with
little-endian metadata block lengths, and have length equal to `bytes_used`; for a vendor carrier the fetch chain
checks image sha256, member sha256 (R40-CL6) and, for V4, the nested file's sha256; a counter-time REA rerun of
the same bytes has the same `plus-extractor` projection (removal diagnostics projected with their relative paths);
PROVINCE.md holds a `## Round-41 additions to Core` row naming the AVM layout and citing
`corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`, which cites a SOURCES row absent at the base whose
used-by lists it; a `Round-41 frontier note` names that heading and the entry stem and says it supersedes the
round-40 `measured, not promoted` record; corpus/README.md maps the entry stem; and no frozen C1 path changed after
the freeze.

**Exact-path rule (R40-CL1; `.ufo/waves/round-41/w1/R41C1Revenger.md` §1).** Strip one `$output/` prefix; the
chunk extract root CR is the child path of the receipt's `derivations[]` edge whose handler starts `squashfs_v4`;
`rel(P)` is `P[len(CR)+1:]` only when `P` starts with `CR + '/'` (whole-segment prefix), otherwise the path is
outside this oracle's namespace; comparisons are keyed by `(root, rel)` and are equality, never a suffix test.

- Carriers (`.ufo/waves/round-41/c1/carriers.json`, sha256 pins, projection `plus-extractor`):
  - **V3** vendor: `FRITZ.Box_5490-07.31.image` (image sha256 `770efb4e…5ab7`), member `./var/tmp/filesystem.image`
    (member sha256 `87cc5d6b…a0f8`), bytes `[0, bytes_used = 30233394)`, carrier sha256 `c4f74f54…f872a`; 104
    inodes: 8 regular files, 85 symlinks, 9 dirs, 1 char device (`w1/R41C1VendorV3.md`).
  - **V4** vendor: the nested `filesystem_core.squashfs` (sha256 `4d5de25c…d947`) of the member
    `./var/tmp/filesystem.image` (sha256 `4cfc3016…2f6c`) of `FRITZ.Box_5491-07.31.image` (sha256 `a5a3a763…f661`),
    bytes `[0, 32720860)`, carrier sha256 `ce27ebca…087f`; 6349 regular files and 1017 non-regular entries; 7367
    staged entries against REA's 10000-entry budget (`w1/R41C1VendorV4.md`, `w1/R41RevBudget.md`). V4 was decided
    by the reader's entry count and REA's budget constant, with no REA run (`w1/R41C1VendorV4.md` §3).
  - **L3** lane-built xz, **L4** lane-built gzip: `tools/round-41/mk-l-carriers.py` through
    `tools/round-40/gen-squashfs.py --endian avm-genuine`; each holds nested-name collisions in both directions
    (regular `usr/bin/busy` with symlink `bin/busy`; symlink `usr/sbin/tool` with regular `sbin/tool`), a deep-tail
    regular pair (`opt/x/etc/conf`, `etc/conf`), an empty regular file and an absolute in-tree symlink;
    byte-deterministic (`w1/R41C1LCarriers.md`).
  - Reservation: no seat ran REA or unblob on the 5490/5491 images, their members or L3/L4 before the freeze
    (every wave-1 report states its runs; `w1/R41CritC1Draft` reservation scan 0 red).
  - Vendor bytes are never committed (AVM licence): `tools/round-41/fetch-vendor.py` rebuilds them from the pinned
    chain into a cache, and the counters read `--carrier-cache`.
- Oracle: `tools/round-41/sqfs-list.py --layout avm` (pure stdlib); its file list equals a direct
  `sasquatch-v4be` (no `-be`) extraction on all four carriers with 0 mismatches (`oracle-run.json` per carrier); on
  the development 7430 rootfs it agrees 6485/6485 (`w1/R41C1Reader.md`).
- Target: `carriers_matched == 4`, every counter binding true, and the supplementary gate met.
- Counting commands (both must exit 0):
  `python3 -I -B tools/round-41/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache <CACHE> --json-out <OUT>`
  and `python3 -I -B tools/round-41/c1-extra.py --root <LANE> --rev <REV> --freeze <FREEZE> --base 49096c7e6f226af0c750c4b003be58883cb6049f --carrier-cache <CACHE> --json-out <OUT>`,
  with `<CACHE>` filled by `python3 -I -B tools/round-41/fetch-vendor.py --root <LANE> --rev <FREEZE> --cache <CACHE>`.
- Data procedure (after the freeze, never before): `tools/round-41/c1-run.sh after <carrier bytes>
  corpus/evidence/round-41/c1/<id> <scratch under /kaidoku-r41/>`.
- Kill rule: a control meeting the target stops C1 before any carrier run. Controls: CTL-C1-0 the do-nothing
  state at the freeze (real counter); CTL-C1-1 the round-40 V1/V2/L1/L2 receipts copied to the round-41 receipt
  paths (subject digests cannot equal the round-41 pins); the counter's red selftest cases, which include both
  collision directions under the round-40 suffix matcher, a deeper-path publication, a removal on a non-symlink
  path and a missing member digest.
- Pre-freeze dry run (QUALITY 83): on a sandbox clone with a round-41-shaped spec naming the round-40 carriers, the
  round-41 counter scores the committed round-40 receipts 4/4 on carriers (`l1/dryrun-c1.json`).
- Disclosed limits: the rerun shows that the carrier extracts through the pinned toolchain at scoring time with the
  same projection; it cannot prove which process wrote the committed receipt (R40-CL2 stays open). Which in-tree
  symlinks unblob removes on a rootfs depends on directory iteration order (`w1/R41C1DevCore.md` §6); the rule
  therefore admits either disposition per row and binds the rerun to the same removal paths.
- Not claimed: LE AVM members (`hsqs`), AVM kernels, the 5490/5491 wrappers' other members, images other than V3
  and V4, anything about extracted programs.

## R41-C2 — depth: SquashFS outcome-triage table v3 scored against an independent evaluator

Surface moved: `SKILL.md` `## Queue-drain craft` gains rule block 20 with `<!-- sqfs-triage-table v3 -->` and its
action line, backed by `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`; block 19 gains a supersession
sentence. Command that shows it unmoved: the frozen v3 interpreter on the base `SKILL.md` exits 2 (no v3 marker),
and the C2 counter at the freeze exits 2 (no held-out manifest).

**Label precedence (frozen; the expected pairs come from this text through the evaluator).** Features of one REA
envelope: OP = `operation`; PR = `provider.id`; H = the handler names in `normalized_result.chunks[].handler` ∪
`normalized_result.extraction_gaps[].handler` (nulls dropped); G = the set of `extraction_gaps[].kind`; D = the
union of the gaps' `dependencies`, compared by exact name, never substring; BE = `yes` if any recorded child argv in
`diagnostics[].report.command` carries the token `-be`, `no` if argvs are recorded and none carries it, `n/a` if
none is recorded (BE = n/a never satisfies step 5); SR = `yes` iff a `MaliciousSymlinkRemoved` producer report is
in `diagnostics` (a removal is not a gap kind); P = the number of `files` (absent reads 0). Steps, first match wins:

1. OP ≠ `extract_firmware` or PR ≠ `unblob` (exact, case-sensitive) → (`unclassified`, `none`).
2. no `squashfs_v4_*` handler in H → (`no-squashfs-chunk`, `inspect-input`).
3. `missing-extractor-dependency` ∈ G: D holds `sasquatch-v4be` → (`dep-missing-be`, `install-extractor-be`);
   else D holds `sasquatch` → (`dep-missing-le`, `install-extractor-le`); a dependency gap naming neither continues
   at step 4.
4. `extractor-failure` ∈ G and P > 0 → (`partial-body-failure`, `salvage-partial`), whatever other gaps or removed
   links accompany it.
5. `extractor-failure` ∈ G, P = 0, BE = `no`, and the failing chunk's handler (else H) is `squashfs_v4_be` →
   (`avm-marker-be-dropped`, `wrap-extractor-be`).
6. `extractor-failure` ∈ G, P = 0 → (`body-extractor-failure`, `preserve-failure`).
7. `depth-limited` ∈ G → (`depth-limited`, `raise-depth`), whatever symlink gaps or removals accompany it.
8. SR = yes and `unpublished-entry` ∈ G → (`mixed-symlinks`, `audit-symlinks`).
9. SR = yes and G = ∅ → (`escaping-symlink-removed`, `expect-link-absent`).
10. G = {`unpublished-entry`} exactly → (`in-tree-symlink-metadata`, `count-gap`) (any unpublished entry kind).
11. G = ∅: P > 0 → (`clean`, `none`); P = 0 → (`clean-empty`, `confirm-empty`).
12. anything else (e.g. `encrypted-chunk`, or SR = yes beside an unrelated gap) → (`unclassified`, `none`).

**Predicate P41-C2.** At the measured revision, the frozen interpreter `tools/round-41/sqfs-triage-v3.py`, reading
only the SKILL v3 table, gives every held-out envelope the same (label, action) pair as the frozen evaluator
`tools/round-41/indep-eval-v3.py` (written from the precedence text above; it never reads the table, the
interpreter or the generator's class map), for all held-out envelopes; the held-out set is
`tools/round-41/heldout-gen-v3.py --seed <FREEZE>`: 20 named classes × 2 replicates plus 12 `combo` carriers whose
factors (endianness, in-tree link, escaping link, partial damage, `max_depth` 1 or 3) are drawn from the seed;
every envelope's observed feature tuple equals the tuple its manifest declares (`observed_features_match_declared`);
carriers regenerate byte-identically; the manifest is first added after the freeze; the v3 table bytes equal the
freeze bytes; the four committed round-40 C1 receipts (`corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`) each
get (`depth-limited`, `raise-depth`) from the interpreter and the evaluator. The generator's class map is reported
(`class_map_agreement`), not scored.

- Target: `matched == n` (n = 52), every counter binding true.
- Counting command: `python3 -I -B tools/round-41/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
- Data procedure (after the freeze, never before):
  `python3 -I -B tools/round-41/heldout-gen-v3.py --seed <FREEZE> --out corpus/evidence/round-41/c2/heldout --run`.
- Kill rule: a control at full score on the development envelopes (seed `sha256("dev41")`, committed in the freeze)
  stops C2 before held-out generation. Controls (`.ufo/waves/round-41/controls/c2/`): CTL-C2-0 base SKILL; CTL-C2-1
  catch-all; CTL-C2-2 the v2 table transcribed into v3; CTL-C2-3 actions rotated; CTL-C2-4 contains form removed
  (exact sets only); CTL-C2-5 a `*` gap-kinds cell in place of the partial row; CTL-C2-6 v2 plus a depth row only;
  CTL-C2-7 a lookup table that enumerates the named classes' observed tuples exactly.
- Honest partition: the held-out pairs come from 13 labels; 12 existed in v2's vocabulary and 1 is new
  (`depth-limited`/`raise-depth`). The depth increment is that row, the contains-form precedence that labels combined
  gap sets (v2 gives `unclassified` to a partial failure with in-tree links and to every `depth-limited` run,
  including all four real round-40 C1 receipts, and `expect-link-absent` to a partial failure with mixed links), and
  the pinned escaping/in-tree gap cells. Expected labels come from a second rendering of the same precedence text, so
  the test measures that the table implements the precedence on real REA envelopes, including seeded combinations the
  claim does not enumerate; it does not measure whether the precedence itself is the best triage.
- Prose repairs riding the block (unscored, reviewed in wave 2): R40-CL5 M1 (no embedded table copy in the
  interpreter), M2/M3 (layout pre-check before acting on a failure row), L1 (block-18 verb), L2 (PATH-wrapper delivery
  measured, `w1/artifacts/R41C2TableDraft/l2-wrapper-measurement.md`), L3 (REA mints the dependency gap kind), L6
  (empty-target link removal is silent); R40-CL4 (partial recipe pinned by the damaged block's compressed length).

## Separability

C1 reads PROVINCE/README/SOURCES/knowledge, its receipts, carriers, oracles and reruns; C2 reads SKILL.md, its
interpreter, evaluator, generator, held-out evidence and the four round-40 C1 receipts (read-only, round-40 data).
Neither reads the other's round-41 data.

## Frozen paths

C1: this file; `tools/round-41/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-vendor.py,sqfs-list.py,mk-l-carriers.py}`;
`tools/round-40/gen-squashfs.py`; `.ufo/waves/round-41/c1/{carriers.json,gap-rule.json}`; every carrier, oracle and
non-regular table carriers.json names. C2: this file; `tools/round-41/{sqfs-triage-v3.py,indep-eval-v3.py,heldout-gen-v3.py,c2-counter.py}`;
the generator's writer; the SKILL v3 block.

## Changes from the draft

- C1 exact-path rule: the draft named the round-40 prototype (`split('_extract/', 1)`); wave 1 measured it at
  0/3 and 0/7 on wrapper/carved chunks (`w1/R41C1Collide.md`, `w1/R41C1Counter.md` §2) and the counter uses
  the derivation-rooted rule of `w1/R41C1Revenger.md` §1 instead.
- C1 gap rule: a removal disposition was added because a full AVM rootfs has in-tree symlinks that unblob
  removes with a `MaliciousSymlinkRemoved` report and no gap, in an iteration-order-dependent set
  (`w1/R41C1DevCore.md` §6–7); the rerun projection carries removal paths.
- C1 carriers: V4 is the 5491 nested rootfs, decided by entry count against REA's budget with no REA run
  (`w1/R41C1VendorV4.md`, `w1/R41C1Sentinel.md` F2); vendor specs require `member_sha256`, `nested.sha256` and
  carve length = `bytes_used` (`w1/R41C1Sentinel.md` F1, F10). The L-carrier builder reads a byte copy of the
  round-40 writer at `tools/round-41/gen-squashfs.py` so the writer is a frozen C1 path.
- C1 coverage-ness: `w1/R41CritC1Draft.md` argued the draft re-scores round-40 ground; the claim now rests on
  four fresh carriers incl. a full vendor rootfs, and CTL-C1-1 (round-40 receipts at round-41 paths) is a
  control that cannot reach the pins.
- C2 precedence: the 17 ambiguities of `w1/artifacts/R41C2Eval/precedence-ambiguities.md` are resolved in the
  text (H, D, BE, SR, P definitions; step-3 else branch; failing-chunk handler in step 5); every step now
  names its action (`w1/R41CritC2Draft.md` §1, `w1/R41C2AxisFit.md`).
- C2 label: `depth-limited-nested` became `depth-limited` because REA records the gap at `--max-depth 1` with
  no nested image (L1 check on a two-file AVM image).
- C2 bindings: `class_expected` is reported, not scored; `observed_features_match_declared` and the
  real-receipt binding were added (`w1/R41CritC2Draft.md` §3, §8).
- C2 held-out: two classes were added (`body-extractor-failure-le`, `failure-depth-limited`,
  `w1/R41C2Shortcuts.md` §6), plus 12 seeded `combo` carriers, because an enumeration of the named classes ties
  any fixed class list (`w1/R41C2AxisFit.md`, `w1/R41C2Shortcuts.md` §4); on the dev seed 6 of 12 combos fall
  outside the named tuples (`w1/artifacts/R41C2Gen/dev-combo-factors.md`).
- C2 controls: the `*` default row (cannot fail, `w1/R41C2Shortcuts.md` §7c) was replaced by CTL-C2-5
  (`*` gap kinds in the partial row); CTL-C2-3 and CTL-C2-7 (lookup) are built by `tools/round-41/c2-controls.py`.
  Dev scores before the freeze (`.ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json`): SKILL v3 52/52;
  controls 0, 4, 34, 2, 38, 31, 42, 44 of 52; none at 52.
- C2 generator: the depth-limited action is bound to `raise-depth` (the SKILL v3 action line); the dev set was
  regenerated with it (`.ufo/waves/round-41/controls/c2/dev/`, 52/52 declared tuples).
