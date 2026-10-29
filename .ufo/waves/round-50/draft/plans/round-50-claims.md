# kaidoku round 50 — claims (DRAFT; the single FREEZE commit pins the final bytes of this file)

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (lane `main` at round start; contains
`corpus/lessons/round-49-verifier-spotcheck.md`, the non-author closure of round 49, status
`admitted`). L1 `KaidokuR50` holds the section-3 planner seat (the wave validator rejects
`planner` as a swarm role; planning data-walks ride scout/connector seats).

Round 49 closed **admitted**, with routed defects: the lane's own round-48/49 record still
carries contradictions the closure listed (round-48 SCORECARD sentences the closure rejected, a
stale coverage fraction, registry rows missing for the round-46..49 counters, S147 tier, S149
reason/anchor, S138 over-wide `teaches`); and the lane's coverage frontier still names
"LE AVM members (`hsqs`)" as unexplored. This round answers both. **One freeze, committed before
any data run and before wave 2; no amendment series** (round 49's discipline): a counter bug found
after the freeze is reported as a miss, never patched. Predicate sentence = counter docstring =
code = receipt label.

Axes owned: coverage / depth / calibration, tied at 10, none retired; stagnation nudge in force
(every owned axis at the 10.0 saturation line; the last capability row entered at round 49, so
the window is open: the nudge does not waive the lowest-axis rule on a tie, every axis is a
lowest axis). **R50-C1 works coverage** (a capability: genuine vendor LE AVM members through REA);
**R50-C2 works calibration** (round-48/49 record atoms + registry census). Causally separable:
C1 reads the four frozen vendor carriers (chain-pinned, never committed), the committed oracle
tables, the REA receipts under `corpus/evidence/round-50/c1/`, `PROVINCE.md`,
`corpus/README.md`, the C1 knowledge entry and the C1-cited SOURCES rows; C2 reads round-48/49
record files at the base and `SCORECARD.md`, `SKILL.md` registry, `corpus/SOURCES.md` correction
rows and `LOG.md` at REV. The only shared path is `corpus/SOURCES.md` (C1 reads its own cited
rows; C2 reads the correction rows for S138/S147/S149).

## R50-C1 — coverage: genuine AVM-marker little-endian SquashFS v4 (`hsqs`) through REA `extract-firmware` → Core

Surface moved: the Frontier clause "LE AVM members (`hsqs`)" of `PROVINCE.md` (round-41, round-42
and round-49 frontier notes) and `corpus/README.md` `## Frontier` (round-41 line). Command that
shows it unmoved at the freeze: `python3 -I -B tools/round-50/c1-counter.py … --rev <FREEZE>`
exits 1 with `carriers_matched 0`.

Probe made by the L1 before drafting (2026-10-28, HTTP range reads of public AVM images,
`.ufo/waves/round-50/l1/scan.py`, output `.ufo/waves/round-50/l1/scan-output.txt`): of 78 FRITZ!Box model
directories, dozens publish a `./var/tmp/filesystem.image` member that is `hsqs`, v4.0, xz
(`comp 4`) with `mkfs_time == bytes_used` (the AVM marker), e.g. 7530-08.25 (34,005,000 B,
`mkfs_time == bytes_used == 34003969`, sha256 of the image
`b17fe5cd0bd3faa713dd92513cb3a65c23e61f5f23366c343b78674955d35e9c`). The AVM licence forbids
redistribution, so carriers are **chain-pinned and never committed** (round-41 custody:
`tools/round-41/fetch-vendor.py`).

**Frozen carriers** (ids in `tools/round-50/carriers.json`; wave-1 seats pin the chain
url → image sha256 → tar member `./var/tmp/filesystem.image` sha256 → carrier sha256):

| id | image (download.avm.de/fritzbox/…) | notes |
|---|---|---|
| a7530 | `fritzbox-7530/deutschland/fritz.os/FRITZ.Box_7530-08.25.image` | ARM (IPQ4018) LE, 34 MB |
| a7590 | `fritzbox-7590/deutschland/fritz.os/FRITZ.Box_7590-08.25.image` | `hsqs` 7590, 35.8 MB |
| c6490 | `fritzbox-6490-cable/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image` | Puma 6 cable, 28 MB |
| c6430 | `fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image` | Puma 6 cable (older firmware line), 23.9 MB |

Wave-1 seat `C1CarrierSelect` may replace a carrier only by a documented, pre-freeze reason
(extraction fails under the dev arm for a reason the claim would not own, URL vanished). A carrier
that fails honestly at the dev arm becomes a **recorded negative** in the entry and a Frontier
line, not a silent drop.

**Predicate P50-C1** (`tools/round-50/c1-counter.py`; the round-41 counter ported — its clause
list is this predicate; the port's deltas are `.ufo/waves/round-50/w1/C1CounterPort/PORT-DELTA.md`).
At the measured revision REV, for each frozen carrier, the committed round-50 REA 6.5.0
`extract-firmware --max-depth 1` after-receipt (unblob 26.6.4, sasquatch 4.5.1 on the child
`PATH`, no `-be` binary needed), first added in a commit descending from the freeze, names the
`squashfs_v4_le` handler for the carrier's chunk with no failed chunk; publishes every regular
file of the frozen independent oracle (`unsquashfs` 4.7.5 listing + per-file sha256; a second
reader — the lane's pure-Python `tools/round-41/sqfs-list.py` `auto` layout — equals it) at its
exact path relative to the chunk extract root (equality after mapping into the root, never a
suffix) with the same sha256 and size, and no extra regular file; accounts for every non-regular
oracle entry by the frozen gap/removal rule (round-41 `gaps_ok` three-family disposition); has a
subject digest equal to the carrier pin and recomputes its evidence id; the carrier bytes hash to
the frozen pin and their superblock reads the frozen layout — **little-endian `hsqs`, v4.0,
compression id 4, `mkfs_time == bytes_used`** (the AVM marker); **and** a counter-time REA rerun
of the same bytes (scratch output directory, carriers fetched through the pinned chain or the
`--carrier-cache`) has the same semantic projection as the committed receipt; **and** the
receipt's `parameters.output_directory` starts with `/fast/scratch/hyaku/kaidoku-r50/` (prefix
test, no `..`); documentation bindings: `PROVINCE.md` holds a `## Round-50 additions to Core`
section whose row names `squashfs_v4_le` with the AVM marker and cites the entry path; one line
carries `Round-50 frontier note`, the entry stem and an LE-AVM token; the entry exists at REV and
its `source:` lines cite SOURCES rows opened `2026-10-28`..`2026-10-29` that list the entry in
`used-by`; `corpus/README.md` `## Coverage map` maps the entry stem; no frozen C1 path changed
after the freeze.

- Target: `carriers_matched == 4` (`TARGET = 4` in the counter), every binding true,
  `frozen_path_changed []`, exit 0.
- Counting command: `python3 -I -B tools/round-50/c1-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --carrier-cache
  <CACHE> --json-out <OUT>` (`<SCRATCH>` under `/fast/scratch/hyaku/kaidoku-r50/`).
- Data procedure (after the freeze, by the L1 only): `tools/round-50/c1-run.sh --data-run`
  writes `corpus/evidence/round-50/c1/<id>/`.
- Controls (scored at the FREEZE before any data run; inputs frozen in
  `tools/round-50/control-fixtures/**`; receipts under `.ufo/waves/round-50/controls/`):
  CTL-C1-0 do-nothing (exit 1, `carriers_matched 0`); CTL-C1-1 the round-41 **big-endian** AVM
  receipts copied verbatim to the round-50 path (red, handler/layout clauses); CTL-C1-2 envelopes
  fabricated from the oracle (red: rerun projection / evidence id); CTL-C1-3 `sasquatch` absent
  from the child `PATH` (red, `missing-extractor-dependency`); CTL-C1-4 a **standard LE**
  carrier (round-36 lane-built, `mkfs_time != bytes_used`) with genuine receipts planted in a
  carrier slot (red on the AVM-marker/superblock clause alone: the marker clause is exercised);
  CTL-C1-POS real receipts + landing blocks (exit 0, not a counterfactual).
- Kill rule: CTL-C1-0, CTL-C1-1 or CTL-C1-4 reaching `carriers_matched == 4` with every binding
  true, or the do-nothing tree at the freeze scoring any carrier clause green, stops C1 before data.
- **Disclosed limits (stated now, widened only by findings).** (1) The marker is invisible to
  unblob: the claim is "REA publishes every oracle file of genuine LE AVM members", not "REA or
  unblob recognises AVM"; an LE standard image takes the same handler (round-36 Core). (2) Vendor
  firmware is fetched, never committed; a vanished or replaced image makes the counter-time rerun
  unrunnable (`--carrier-cache` of locally pinned members substitutes); the receipts and
  oracle tables are the durable evidence. (3) A relabelled replay of genuine receipts scores the
  same as a fresh run (inherited, round 49). (4) Documentation bindings are presence checks.
  (5) Four carriers on three or more SoC lines are not "every LE AVM image"; the compression is
  xz in all four; fragment/xattr/sparse features are whatever the images contain.

## R50-C2 — calibration: round-48/49 record atoms re-derived and the registry census extended

Atoms (draft list; the counter's docstring is the predicate): each pairs a statement the lane
made or a state the repo still carries with a re-derivation from committed bytes. B1 owned-axes
coverage fraction vs knowledge-file count at REV and the C1 entry mapped (`138/138` at the
base vs 139); B2 `## Owned axes` calibration row cites the round-48 `rejected-harmed` verdict
and the round-49 `c2-final` measure; B3 round-48 seat settlement correction line
(`.ufo/waves/round-48/r48-w1-results.json`: 75 results, `C1Meaning` blocked,
`ScribeReportNumbers` aborted; 72 report artifacts); B4 round-48 per-axis verdict correction line
(quality harmed, discernment improved at decision level only — from the closure's per-axis
table); B5 round-48 final receipts `33f65a91`/`8847042a` named; B6 S149 correction row
(`supersedes S149 —`, FreeBSD is the origin of sysexits, locator `ERRORS`, status `rejected`
kept, quote located in the committed snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html`);
B7 S147 tier correction row (`supersedes S147 —`, tier B per CORPUS tier text, the quote located
in the committed snapshot); B8 S138 grounding row (`supersedes S138 —`, a located quote that
grounds the 22-member census, with `used-by`); B9 registry census: every `tools/round-49/**`
`.py`/`.sh` path at the base (and the round-50 instruments at REV) is the cell-0 path of a
`## Local round-evidence gate registry` row with gate|probe kind, entry command, verdict map
binding 0/1/2 to meanings (the round-48 meaning rule), self-test spelling and pinned-value
path; B10 `tools/round-50/selftest-r49-c2.py` exists and its committed expected values equal its
output over committed fixtures (the `--selftest` the closure asked `c2-mismatch.py` to have;
`tools/round-49/` stays byte-frozen, not edited); B11 the round-49 lesson's declared freeze, the
round-49 SCORECARD section, `FREEZE` and LOG agree (round-49 analogue of A1). Atoms inside an
HTML comment or a fenced code block do not count (the forgery wave 2 of round 49 found against
A9). The wave-1 `C2AtomSpec` seat finalises the atoms; the counter is frozen with them.

**Predicate P50-C2.** At REV, with FREEZE an ancestor of REV, frozen paths untouched and the
counter's bytes equal to FREEZE's, `python3 -I -B tools/round-50/c2-record.py --root <LANE>
--rev <REV> --freeze <FREEZE> --battery` reports `atoms_total N`, `mismatches 0`, a battery in
which each single-mutation overlay turns exactly its own atom red (none a no-op), a do-nothing
overlay (every path changed since FREEZE restored to its FREEZE blob) turning every atom red, and
exits 0. At FREEZE the same command without `--battery` reports `mismatches N`, exit 1.

- Target: exit 0, `mismatches 0`, `battery.failing []`.
- Controls: do-nothing at the freeze; the in-counter battery.
- Kill rule: a mutation leaving its atom green, turning another red, or a no-op; or a do-nothing
  overlay leaving any atom green, stops C2 and is reported as a miss.
- **Disclosed limits.** A consistency check of the record against committed bytes, not a judgment
  of prose; round-48/49 atoms are the defects the closures named and this round chose, not every
  inaccuracy; the registry check is row presence + cell shape + meaning words, not that the
  entry command runs.

## Frontier step (inside the claim cap)

- Sourced claim: R50-C1's entry cites SOURCES rows opened this round (Freetz AVM-BE-format /
  AVM_LE define patch, the unblob SquashFS handler source, the AVM download index).
- Assimilation: a `merge/kaidoku/` theme "AVM LE" (`avm-le-variant-reachability`,
  `avm-le-image-genuine-marker`) read-only; admit/refuse per entry in the lesson `## Gate`;
  collision guard in `.ufo/waves/round-50/assimilation/`; `considerthese/` absent.
- Mistake mined: M50-1 from the round-49 closure (S147 tier / S149 provenance direction /
  S138 over-wide `teaches` = `attribution`/`scope`; captured-by none) and M50-2 (counters
  landed unregistered: `landing`).

## Frozen paths

Byte-frozen: `plans/round-50-claims.md`; `tools/round-50/` (populated before FREEZE incl.
`control-fixtures/**`); for C1 additionally the carried-over inputs the counter names
(`tools/round-41/{sqfs-list.py,fetch-vendor.py}` and whatever the port imports),
`tools/round-27/xpin-attribute.mjs`. Not frozen: `PROVINCE.md`, `corpus/README.md`,
`corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/knowledge/*`,
`corpus/lessons/*`, `corpus/evidence/round-50/**` (each counter binds what it reads).
