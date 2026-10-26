# kaidoku round 39 — frozen claims

Base `a2f64e1da78afcf8cc39287106604dbcc270844c` (lane `main`; the round-38 closure spot-check
landed on top of the round-38 tip `7e979514`). L1 `KaidokuR39` holds the §3 planner seat. Wave 1
(43 seats, `.ufo/waves/round-39/w1/`) built and attacked the draft of this file before the freeze;
every change from the draft is named in `## Changes from the draft` below. The rule for each claim
is the bytes of this file, its counter and its frozen inputs in the commit that first adds this
version (the freeze, QUALITY 79). Frozen controls are scored with each counter before any claim
data exists, and their receipts land in their own commit before the first data commit.

Owned axes coverage/depth/calibration are tied at 10, none retired. R39-C1 works coverage and
R39-C2 works depth; either satisfies the lowest-axis rule on the tie.

## Freeze-integrity rule (binding for both claims; routed defect R38-CL4)

A score at measured revision `REV` is admissible only if no commit in `FREEZE..REV` touches a
frozen path of that claim. A later restore does not un-block: the counters exit 2
`frozen_path_changed` whenever a frozen path was touched, even if the bytes at `REV` equal the
freeze bytes, and never report `met_target` then. `ships_freeze_bytes` alone is never enough.
Frozen paths: C1 — this file, `tools/round-39/c1-counter.py`, `tools/round-39/c1-run.sh`,
`.ufo/waves/round-39/c1/carriers.json` and every carrier, oracle and symlink table it lists;
C2 — this file, `tools/round-39/sqfs-triage.py`, `tools/round-39/heldout-gen.py`,
`tools/round-39/c2-counter.py`, and the triage table block in `SKILL.md` (byte-identical at
`FREEZE` and `REV`). A blocking verdict after claim data exists is an honest stop.

## R39-C1 — coverage: standard big-endian SquashFS v4 moves from Frontier to Core

Surface moved: `PROVINCE.md` `### Round-4 frontier (post-unlock)` bullet **sasquatch**
("big-endian/AVM stays here", `PROVINCE.md:156-157`), the round-36 Core row aside and the
round-38 note (`PROVINCE.md:372,376`), and the `corpus/README.md` `## Frontier` sasquatch bullet.
Command that shows it unmoved: the C1 counter at the freeze exits 1 (no round-39 receipts, no
`## Round-39 additions to Core`).

**Predicate P39-C1.** At the measured revision, for each of the six frozen big-endian SquashFS v4
carriers, the committed round-39 REA extract-firmware after-receipt (rea-agents 6.5.0, unblob
26.6.4, sasquatch-v4be 4.5.1 reachable on the child PATH), first added in a commit that descends
from the freeze and run with an output directory under this round's scratch segment
(/kaidoku-r39/), names the `squashfs_v4_be` handler with no failed chunk, publishes every regular
file of the frozen independent oracle (same relative-path suffix, same sha256), carries
extraction gaps of kind `unpublished-entry` exactly on the frozen oracle's in-tree symlinks and no
other gap, publishes no path for the oracle's escaping symlinks, has a subject digest equal to the
frozen carrier pin, and recomputes to its stored evidence id under the rea-agents 6.5.0 rule; the
frozen symlink tables hold at least two in-tree and two escaping rows with one carrier holding two
in-tree rows, and one frozen carrier is BE SquashFS v4 with the xz compression id; PROVINCE.md
holds a `## Round-39 additions to Core` row naming `squashfs_v4_be` that cites the round-39
knowledge entry, which cites a SOURCES.md row opened 2026-10-26 whose used-by lists that entry; a
round-39 frontier note supersedes the big-endian part of the Frontier bullet; corpus/README.md
holds a coverage-map row naming the entry stem; and no frozen C1 path changed after the freeze.

The per-carrier clause and binding names are listed in the counter's docstring
(`tools/round-39/c1-counter.py` lines 4-70); that list and this sentence are the same rule.

- Carriers (`.ufo/waves/round-39/c1/carriers.json`, sha256 pins): K1–K4 = the round-38 carriers
  (`corpus/evidence/round-37/c1/K*/`), K5 = round-39 BE v4 gzip, K6 = round-39 BE v4 xz
  (compression id 4, four compressed xz data blocks), both built with `tools/round-39/gen-squashfs.py`
  (the round-37 writer plus a UTF-8 name-length fix and a correct xz encoder, wave-1 findings
  `w1/R39C1CarrierK5.md` §7 and `w1/R39C2HeldoutGen.md` §3) and never run through REA or unblob
  before the freeze. Each regular-file oracle was derived from the source tree and agrees with
  the independent reader `tools/round-39/sqfs-list.py` and with direct `sasquatch-v4be -be`
  extraction; each symlink table agrees with the reader.
- Symlink rule, stated before data (S118, S119): unblob decides per link whether its target,
  joined to the link's directory inside the per-chunk extraction root, stays inside that root
  (`is_safe_path`, no clamping at the root). A link that escapes is removed with a
  `MaliciousSymlinkRemoved` report and leaves no gap; a link that stays inside is kept and REA
  records one `unpublished-entry` gap for it. Absolute targets are re-rooted and kept. Every
  frozen carrier uses relative file targets only (no absolute, directory or chained links): K1 1
  escaping, K2 1 in-tree, K3/K4 none, K5 2 in-tree + 1 escaping, K6 1 in-tree + 2 escaping.
- Target: `carriers_matched == 6` and every binding true (`met_target`).
- Counting command: `python3 -I -B tools/round-39/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>`.
  Self-test: same tool `--selftest --pkg65 <same>`, 33 cases (1 green, 32 red, each red failing on
  its targeted clause).
- Kill rule: any frozen control meeting the target stops C1 before any after-run: CTL-C1-0
  do-nothing at the freeze; round-38 receipts copied into the round-39 paths (with and without
  genuine K5/K6); receipts built from oracle data with the old ids kept; a "materialise the
  symlink" receipt with no gap; a wrong gap kind; an escaping symlink kept as a gap; an extra gap;
  a failed chunk; receipts added in the freeze commit itself
  (`.ufo/waves/round-39/w1/artifacts/R39C1Controls/`). A miss at the measured revision is an
  honest stop.
- Disclosed limit: a fabricated receipt whose evidence id is re-minted with the 6.5.0 rule
  (`w1/R39C1Controls.md` CTL-C1-3) satisfies every receipt-only clause; no counter over committed
  bytes can refuse it. Provenance therefore rests on independent wave-2 re-runs that compare the
  semantic payload of each committed receipt (QUALITY 78), not on the counter.
- Not claimed: AVM-BE bodies, vendor-mangled images, extra published files beyond the oracle,
  anything about extracted programs.

## R39-C2 — depth: an executable SquashFS extract-firmware outcome triage table in the SKILL craft section

Surface moved: `SKILL.md` `## Queue-drain craft` gains rule block 18, "SquashFS `extract-firmware`
outcome triage (round 39)", holding a machine-readable decision table (eight labels; signature →
cause → action; each row cites S112/S118–S121 or the backing entry
`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`). The table lands in the freeze commit;
the held-out data that scores it cannot exist before the freeze, because its seed is the freeze
commit hash. The round-36 table (`SKILL.md:1260-1271` after this insertion) is prose recall for
LE only and is not machine-readable. Command that shows it unmoved: the triage interpreter on the
base `SKILL.md` exits 2 (no table) and the C2 counter at the freeze exits 2 (no held-out manifest).

**Predicate P39-C2.** At the measured revision, the frozen triage interpreter
`tools/round-39/sqfs-triage.py`, reading only the SKILL.md craft-section triage table, assigns
every held-out envelope the label its frozen generator assigned before any REA run, for all N
held-out carriers (2 per generator class); the held-out set is generated by the frozen
`tools/round-39/heldout-gen.py` with seed = the freeze commit hash, every carrier regenerates
byte-identically from that seed, every envelope's subject digest equals its carrier, the held-out
manifest is first added in a commit descending from the freeze and no later than its envelopes,
and the triage table bytes at the measured revision equal those at the freeze.

- Generator classes (10, `heldout-gen.py` `DEFAULT_CLASSES`) → labels: clean-be, clean-le → `clean`;
  escaping-symlink-removed; in-tree-symlink-metadata; dep-missing-be; dep-missing-le;
  avm-marker-be-dropped; body-extractor-failure (id-table block zeroed) and version-minor-mismatch
  (`s_minor` 5) → `body-extractor-failure`; no-squashfs-chunk (`s_major` 9). N = 20.
- Target: `matched == 20` and every binding true (`met_target`, asserted equal to
  `matched == N and bindings`).
- Counting command: `python3 -I -B tools/round-39/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <RECEIPT>`.
  Self-test: `--selftest`, 27 cases. Interpreter self-test: `tools/round-39/sqfs-triage.py --selftest`, 35 cases.
- Data procedure (after the freeze, never before):
  `python3 -I -B tools/round-39/heldout-gen.py --seed <FREEZE> --out corpus/evidence/round-39/c2/heldout --run`.
- Kill rule: a frozen control meeting the target stops C2 before held-out generation. Controls
  are scored with the frozen interpreter on the 20 development envelopes of wave 1 (seed
  `sha256("dev1")`, `w1/artifacts/R39C2HeldoutGen/{dev-run,opt-in-run}/`): CTL-C2-0 the base
  `SKILL.md` (no table); CTL-C2-1 catch-all; CTL-C2-2 gap-count-only; CTL-C2-3 gap-kind-only;
  CTL-C2-4 published-only; CTL-C2-5 the round-36 table transcribed; CTL-C2-6 the best table with no
  `-be` and no `MaliciousSymlinkRemoved` knowledge (`w1/artifacts/R39C2Shortcuts/`). Any control at
  20/20 stops C2. A miss at the measured revision is an honest stop.
- Separability: C2 reads SKILL.md, its three tools, the writer and its own held-out evidence; C1
  reads PROVINCE/README/SOURCES/knowledge and its own receipts and carriers. Neither reads the
  other's data. The two share the SOURCES rows S118/S119 only as citations.
- Not claimed: AVM-BE bodies, LE body damage, `unknown-chunk-handler`/`encrypted-chunk`/
  `depth-limited` envelopes, images holding both symlink kinds (labelled `escaping-symlink-removed`
  by row order; no held-out class), anything about extracted programs.

## Changes from the draft (wave-1 findings applied before the freeze)

- Symlink classification is extraction-root containment without clamping; the draft's "POSIX
  join against the image root /" would have called K1 in-tree (`w1/R39C1SymlinkK1K4.md`,
  `w1/R39C1AxisFit.md` (d.0), `w1/R39C1Revenger.md`).
- C1 adds run provenance (`/kaidoku-r39/` output directory, hashed into the evidence id), the
  symlink-coverage and xz-leg bindings, and the six-carrier spec binding
  (`w1/R39C1Counter.md` §2, `w1/R39C1AxisFit.md` (b)-(c)); the re-minted fabrication limit is
  disclosed instead of listed as a kill control (`w1/R39C1Controls.md`).
- The writer's UTF-8 name length and xz encoder were fixed in a round-39 copy; K6 was rebuilt
  with a compressible file so its xz blocks are really compressed (`w1/R39Sentinel.md`,
  `w1/R39C2ReconDep.md`).
- C2 classes: `no-squashfs-chunk` added (`w1/R39C2ReconTruncate.md`), a second damage recipe
  added under `body-extractor-failure`, `clean` covers both endians, the symlink rows cover both
  v4 handlers, and the dependency rows accept AppImage before-arms (`published files` `*`); the
  rule block cites its knowledge entry so command A's depth count stays resolvable
  (`w1/R39C2AxisFit.md` F1).
