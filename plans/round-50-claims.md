# kaidoku round 50 — claims (the FREEZE commit pins these bytes)

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (lane `main` at round start; it contains
`corpus/lessons/round-49-verifier-spotcheck.md`, the non-author closure of round 49, status
`admitted`). L1 `KaidokuR50` holds the section-3 planner seat (the wave validator rejects
`planner` as a swarm role; planning data-walks rode scout/connector seats — recorded in the
report).

Round 49 closed **admitted**, with routed defects: the lane's own round-48/49 record still
carries statements the closures contradict (a stale coverage fraction, a round-48 trend line and
seat count, a round-49 discernment line), three source-registry errors (S147 tier, S149 reason and
locator, S138 over-wide `teaches`), six `tools/round-49` instruments with no registry row, and the
lane's coverage frontier still names "LE AVM members (`hsqs`)" as unexplored. This round answers
both. **One freeze, committed before any data run and before wave 2; no amendment series**
(round 49's discipline): a counter bug found after the freeze is reported as a miss, never
patched. Predicate sentence = counter docstring = code = receipt label: the predicate paragraphs
below are copied byte-for-byte from the counters' docstrings by `.ufo/waves/round-50/l1/mkplan.py`
and `mkplan.py --check` re-extracts both paragraphs from the frozen counters and compares them to this file (committed with the freeze; wave 2 re-runs it).

Owned axes coverage / depth / calibration are tied at 10 in `SCORECARD.md`, none retired; every
owned axis is a lowest axis. **R50-C1 works coverage** (a capability acquisition: genuine vendor
LE AVM members through REA `extract-firmware`); **R50-C2 works calibration**. They are
**causally separable**: C1 reads the four chain-pinned vendor carriers (never committed), the
frozen oracle and gap tables under `tools/round-50/`, the REA receipts under
`corpus/evidence/round-50/c1/`, `PROVINCE.md`, `corpus/README.md`, the C1 knowledge entry and the
SOURCES rows the entry cites. C2 reads round-48/49 record files at the base, and `SCORECARD.md`,
`SKILL.md` registry, `corpus/SOURCES.md` correction rows, `corpus/README.md` and the
`corpus/knowledge` tree at REV. **Shared reads (stated, not hidden):** `corpus/README.md` and the
`corpus/knowledge` tree (C2 atom B1 counts the C1 entry as a knowledge file that must be mapped;
C1's `coverage_map_row` binding reads the same map line), the `## Owned axes` coverage row
(C2-B1 reads it; C1 does not), and `corpus/SOURCES.md` (C1 reads its cited rows by id; C2 finds
its three correction rows by `supersedes S149/S147/S138 —` in the teaches cell, never by id).
Wave-1 seat `ConnCrossClaim` measured the coupling; landing order: C1 documentation, then C2
records. **Known REV property of a frozen older counter:** any registry row added after the
round-49 freeze flips the frozen round-49 `c2-mismatch.py` atom A8 at a later REV (its derived
row count), and added rows in the `instrument-registry v2` block of `SKILL.md` are rows outside
the frozen round-48 `census2.json`; both older counters were verified at their own revisions and
are not re-run as gates this round (`w1/ConnCrossClaim.md` F2, `w1/C2AtomSpec/ATOMS.md` finding 4).

## Wave-1 amendment record (folded into this text and the tools before the freeze)

| wave-1 finding (seat report under `.ufo/waves/round-50/w1/`) | disposition |
|---|---|
| `C1CarrierAdversary`, `ConnSiblings`, `C1OracleBuild`, `C1CarrierSelect`, `PlanClaimSizing`: two carriers (c6490, c6430) do not carry `./var/tmp/filesystem.image`; their LE member is `./var/remote/var/tmp/x86/filesystem.image` (the tar also holds a BE `sqsh` ARM member); the L1 probe's first-match on `endswith('filesystem.image')` misread them, and "78 directories / dozens" was wrong (70 directories, 16 models with 28 LE `hsqs` AVM-marker rows in the census) | carriers.json pins the per-carrier member path and the carve to `bytes_used`; this text states the census; M50 mistake `reference-drift` |
| `C1DevArmA`, `C1ControlsBuild`, `C1RunPort`: default REA budgets fail ("Staging entry budget exceeded (10000)") on the 13k-file rootfs carriers | `rea_parameters` frozen in carriers.json (`max_depth 1`, `max_output_files 100000`, `max_output_bytes 536870912`) and clause `parameters_ok` |
| `C1ShortcutCritic` S1, S3, S4, S5, S11: the rerun resolved REA through `npx` and ambient `PATH`; the counter's bytes were unbound; `first_add` ignored `--full-history`; no scoring-time oracle re-derivation; the projection profile was receipt-chosen | rerun runs node on `--pkg65`, binds unblob 26.6.4 and records sasquatch; `counter_not_frozen`; `--full-history`; `oracle_rederived_ok` (unsquashfs 4.7.5); `projection plus-extractor` frozen |
| `C1MarkerCritic`, `C1SrcFreetz`, `C1SrcUnblob`, `C1CarrierAdversary`: the AVM marker is a re-stampable timestamp field, unblob's LE branch never reads it, no source text documents an LE AVM layout, and a standard LE image patched to `mkfs_time == bytes_used` is indistinguishable to REA | the claim is reworded: the marker is a **constant of the pinned bytes** (it adds nothing beyond `carrier_pin_ok`); "genuine" is provenance (the sha256 chain from the vendor URL), not the marker |
| `C1SentinelFetch` S4/S5/S7: fetch accepted any origin and `file://`, any cache dir (including the lane), and the wrapper deleted a caller-supplied scratch | `tools/round-50/fetch-vendor.py` allows `https://download.avm.de` only, caps 64 MiB, refuses a lane-resident cache; the run harness removes only a scratch it created |
| `C1DevArmA` run, host load: REA's own 120 s `provider_timeout` (not tunable) fires on the 13k-file carriers when the host load is ~50 | the data run and the counter's rerun repeat the same REA run up to 3 times on `provider_timeout` only (recorded as `attempts`); persistent timeout stays exit 2 |
| `C2AtomSpec`, `C2AtomCritic`, `C2RegCensus`, `C2CounterBuild`: B11 (freeze agreement) is green at base; B10 is green at the freeze unless bound to a SCORECARD statement; B9 named the wrong registry home; B3 omitted `C1Battery`; B4 cited the wrong closure section; B2 was green under a token test | B11 replaced by the round-49 trend atom (red at base); B10 and B2 bound to correction/row text the counter re-derives; B9 reads the marker-bound `instrument-registry v2` region; B3 derives all three no-report seats; B4 reads the closure's trend list; every atom strips HTML comments and fences, duplicates are mismatches |
| `C2Selftest49`: the real hermetic self-test of the frozen round-49 C2 counter (40 cases) | `tools/round-50/selftest-r49-c2.py` + `.expected.json` frozen; the C2 counter's B10 runs it from REV bytes (`--lane`) |
| `C1SentinelFetch` S2/S3: unredacted GitHub session-cookie values at the tip in `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr` | redacted at the tip in the landing commit (not frozen, not a claim); history not purged (operator decision, L0 question) |

## R50-C1 — coverage: genuine AVM-marker little-endian SquashFS v4 (`hsqs`) through REA `extract-firmware` → Core

Surface moved: the Frontier clause "LE AVM members (`hsqs`)" of `PROVINCE.md` (round-41,
round-42, round-44 and round-49 frontier notes) and `corpus/README.md` `## Frontier`. Command that
shows it unmoved at the freeze: `python3 -I -B tools/round-50/c1-counter.py … --rev <FREEZE>`
exits 1 with `carriers_matched 0`.

Census the claim stands on (`.ufo/waves/round-50/l1/scan-output.txt` is the L1's first probe, which
first-matched the wrong tar member for the cable boxes; the corrected census is
`.ufo/waves/round-50/w1/C1CarrierAdversary.md` finding 2): 70 FRITZ!Box model directories on
`https://download.avm.de/fritzbox/`; 28 `hsqs` v4.0 xz filesystem members with
`mkfs_time == bytes_used` in 16 models, none without the marker. The carriers below are four of
them. Vendor firmware is licensed against redistribution, so carriers are **chain-pinned and never
committed**: image URL → image sha256 → tar member sha256 → carve to `bytes_used` → carrier sha256
(`tools/round-50/fetch-vendor.py`, round-41 custody with containment fixes).

**Carrier swap, before the freeze (recorded, not hidden).** The plan's first draft named the
FRITZ!Box 7530 and 7590 (FRITZ!OS 08.25) members as two of the four. Their rootfs holds ~13.4k
regular files (172/190 MB published); under host load 42–54 (the shared fleet host) REA's own
fixed 120 s `provider_timeout` fired on three of three attempts each in the L1's pre-freeze dev
arm (`.ufo/waves/round-50/l1/dev-arm-timeouts.txt`), while the wave-1 seat `C1DevArmA` measured
40–48 s for the same bytes at lower load. A claim whose after-state depends on the host's load at
scoring time is not re-derivable by the closure, so the two 13k-file members are **not**
carriers; they are recorded in the entry as an observed, load-dependent outcome and stay
Frontier ("LE AVM rootfs of ~13k files under REA's 120 s limit"). The replacements are the final
releases (07.18) of the FRITZ!Box 7581 and 7582, 4.5k regular files each.


**Frozen carriers** (`tools/round-50/carriers.json`; the carrier bytes are the tar member carved
to its superblock `bytes_used`; sizes below are those carves):

| id | image (`https://download.avm.de/fritzbox/…/fritz.os/`) | tar member | carrier bytes | SoC line |
|---|---|---|---|---|
| g7581 | `fritzbox-7581/other/…/FRITZ.Box_7581-07.18.image` | `./var/tmp/filesystem.image` | 28,368,210 | not self-described (`FIRMWAREVERSION=152.07.18`) |
| g7582 | `fritzbox-7582/other/…/FRITZ.Box_7582-07.18.image` | `./var/tmp/filesystem.image` | 28,607,082 | not self-described (`FIRMWAREVERSION=156.07.18`) |
| c6490 | `fritzbox-6490-cable/deutschland/…/FRITZ.Box_6490_Cable-07.57.image` | `./var/remote/var/tmp/x86/filesystem.image` | 28,200,029 | Puma 6 x86 |
| c6430 | `fritzbox-6430-cable/deutschland/…/FRITZ.Box_6430_Cable-07.30.image` | `./var/remote/var/tmp/x86/filesystem.image` | 23,861,507 | Puma 6 x86 |

The cable images also carry a big-endian ARM `sqsh` member; it is **not** a carrier and not
claimed (the carrier is the x86 LE member alone, REA is run on the carved carrier). The 8-byte
AVM trailer that follows the 4096-padded squashfs in each tar member is removed by the carve; on
the uncarved member REA reports it as a second chunk with `unknown-chunk-handler` (observed by
`C1DevArmA`, `C1DevArmB`; recorded in the entry as a separate observation, not claimed).

**Predicate P50-C1** (`tools/round-50/c1-counter.py`; its docstring is this paragraph, copied by
`mkplan.py`; the port's deltas against the round-41 counter are
`.ufo/waves/round-50/w1/C1CounterPort/PORT-DELTA.md`):

  At the measured revision REV, for each frozen carrier, the committed round-50
  REA 6.5.0 `extract-firmware --max-depth 1` after-receipt (unblob 26.6.4,
  sasquatch 4.5.1 on the child PATH, no `-be` binary needed), first added in a
  commit that descends from the freeze, names the `squashfs_v4_le` handler for
  the carrier's chunk with no failed chunk, publishes every regular file of the
  frozen independent oracle (unsquashfs 4.7.5 listing + per-file sha256; the
  lane's pure-Python `tools/round-41/sqfs-list.py` `auto` layout is the second
  reader that equals it) at its exact path relative to the chunk extract root
  (equality after mapping into the root, never a suffix) with the same sha256
  and size, and no extra regular file; accounts for every non-regular oracle
  entry by the frozen gap/removal rule (round-41 `gaps_ok` three-family
  disposition); has a subject digest equal to the carrier pin and recomputes
  its evidence id; the carrier bytes hash to the frozen pin and their superblock
  reads the frozen layout -- little-endian `hsqs`, v4.0, compression id 4,
  `mkfs_time == bytes_used` (the AVM marker); **and** a counter-time REA rerun
  of the same bytes (scratch output directory, carriers fetched through the
  pinned chain or the `--carrier-cache`; executed by node on the REA package at
  `--pkg65`, never through `npx`; repeated, up to 3 attempts, only when REA reports
  its own `provider_timeout`) has the same semantic projection as the
  committed receipt; **and** a scoring-time `unsquashfs` 4.7.5 re-derivation of
  the carrier bytes yields exactly the frozen oracle table (both directions);
  **and** the receipt's `parameters.output_directory` starts
  with `/fast/scratch/hyaku/kaidoku-r50/` (prefix test, no `..`); documentation
  bindings: `PROVINCE.md` holds a `## Round-50 additions to Core` section whose
  row names `squashfs_v4_le` with the AVM marker and cites the entry path; one
  line carries `Round-50 frontier note`, the entry stem and an LE-AVM token; the
  entry exists at REV and its `source:` lines cite SOURCES rows opened
  2026-10-28..2026-10-29 that list the entry in `used-by`; `corpus/README.md`
  `## Coverage map` maps the entry stem; no frozen C1 path changed after the
  freeze.

- Target: `carriers_matched == 4` (`TARGET = 4` in the counter), every binding true,
  `frozen_path_changed []`, exit 0.
- Counting command: `python3 -I -B tools/round-50/c1-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --carrier-cache
  <CACHE> --json-out <OUT>` (`<SCRATCH>` under `/fast/scratch/hyaku/kaidoku-r50/`; `<CACHE>` holds
  the chain-pinned carriers `<pin>.bin` materialised by `tools/round-50/fetch-vendor.py`).
- Data procedure (after the freeze, by the L1 only): `tools/round-50/c1-run.sh after --id <id>
  --carrier <cache>/<pin>.bin --data-run` writes `corpus/evidence/round-50/c1/<id>/{after.json,run.json}`
  (receipts only; REA's extraction tree is never copied into the lane).
- Controls (scored at the FREEZE before any data run; inputs frozen in
  `tools/round-50/control-fixtures/**` and built by `tools/round-50/c1-controls.py`; receipts under
  `.ufo/waves/round-50/controls/`): CTL-C1-0 do-nothing (exit 1, `carriers_matched 0`); CTL-C1-1
  the round-41 **big-endian** AVM receipts copied verbatim into the four round-50 slots (red:
  `handler_ok`, `subject_pin_ok`); CTL-C1-2 envelopes fabricated from the oracle tables (red:
  `projection_ok` / `evidence_id_ok`); CTL-C1-3 `sasquatch` absent from the child `PATH` (red,
  `missing-extractor-dependency`); CTL-C1-4 a standard little-endian carrier (round-36
  lane-built, `mkfs_time != bytes_used`) with its genuine receipt planted in a carrier slot (red on
  `carrier_pin_ok` AND `layout_ok` — it shows the pin and the layout statement are exercised, not
  that the marker proves origin); CTL-C1-POS real receipts plus the landing blocks (exit 0; not a
  counterfactual).
- Kill rule: CTL-C1-0, CTL-C1-1, CTL-C1-2 or CTL-C1-4 reaching `carriers_matched == 4` with
  every binding true, or the do-nothing tree at the freeze scoring any carrier clause green,
  stops C1 before data.
- **Disclosed limits (stated now; widened only by findings).** (1) The marker is invisible to
  unblob and re-stampable: the claim is "REA publishes every oracle file of these four pinned
  vendor members", not "REA or unblob recognises AVM", and a standard LE image takes the same
  handler (round-36 Core); no source text describes an LE AVM layout (the Freetz documents define
  the big-endian variant; patch 101 only adds the byte-order symbol) — the marker is an empirical
  property of the four carriers and of all 28 census rows. (2) Vendor bytes are fetched, never
  committed: an image AVM replaces makes the chain unfetchable (the four are the final or
  long-standing releases of their models, not a guarantee) and the counter-time rerun unrunnable
  without a `--carrier-cache`; the
  committed receipts and oracle tables are the durable evidence. (3) A relabelled replay of
  genuine receipts scores the same as a fresh run on the receipt side, which is why the rerun is
  the measurement (inherited, round 49). (4) Documentation bindings are presence checks. (5) Four
  carriers, one vendor, xz only, depth 1: not "every LE AVM image"; the SoC lines are not
  self-described by the images (the cable boxes' x86 member names its architecture by path only). (6) REA's 120 s `provider_timeout` is a host-load property; the
  rerun repeats up to 3 times and a persistent timeout is exit 2, never a pass. (7) The oracle
  rows for symlinks compare path and kind, not `link_target` (unblob rewrites targets), and the
  set of removed `MaliciousSymlinkRemoved` links depends on readdir order (`C1GapRule` F1), so the
  rule is set-agnostic.

## R50-C2 — calibration: round-48/49 record atoms re-derived, the registry census extended, three source rows corrected

An **atom** is a statement the lane made, or a state the repository still carries, paired with a
re-derivation from committed bytes; it is a **mismatch** when the re-derivation disagrees with the
record or the record that must correct it is absent. The atom list B1–B11 is the `ATOMS` table of
`tools/round-50/c2-record.py`; its docstring is the predicate below (copied by `mkplan.py`).

Predicate (the same sentence as the plan): at the measured revision REV, with FREEZE an
ancestor of REV, frozen paths untouched and this file's bytes equal to FREEZE's,
`atoms_total == 11`, `mismatches == 0`, and (with `--battery`) a battery in which every
single-mutation overlay turns exactly its own atom red (none a no-op) and the do-nothing
overlay (every path changed since FREEZE restored to its FREEZE blob) turns every atom red;
exit 0.  At FREEZE the same command without `--battery` reports `mismatches N`, exit 1.

  B1  owned-axes coverage: `SCORECARD.md` `## Owned axes` coverage row at REV states, as
      its first `N/N knowledge files mapped`, N equal to the count of `corpus/knowledge/**.md`
      at REV, and every knowledge file at REV (so the round's C1 entry) is mapped by its
      backticked stem in `corpus/README.md` `## Coverage map` (`138/138` at the base vs 139).
  B2  owned-axes calibration: the `calibration` row at REV names `rejected-harmed`, the
      round-48 closure (which states `Admission: **rejected-harmed**` at BASE) and the
      round-49 receipt `.ufo/waves/round-49/l1/scores/c2-final.json`, and states
      `mismatches 9 -> 0` with both numbers re-derived from the committed round-49
      do-nothing control and `c2-final.json`.
  B3  the round-48 seat settlement: correction line `B3` (`seats reports blocked aborted
      missing`), re-derived from `.ufo/waves/round-48/r48-w1-results.json` and the `w1/`
      tree at BASE (75 results, `C1Meaning` blocked, `ScribeReportNumbers` aborted, 72
      report artifacts); the round-48 SCORECARD section at REV equals the base section
      (a correction is a new line, never a rewrite) and still carries the corrected sentence.
  B4  the round-48 per-axis verdicts: correction line `B4`, every verdict re-derived from
      the round-48 closure at BASE (quality harmed, discernment improved at decision level
      only, calibration harmed, ...); the round-48 SCORECARD section is unchanged.
  B5  the round-48 final receipts: correction line `B5` names `33f65a91` (the receipts'
      `rev`) and the lane tip `8847042a`, both raw sha256 of the two final receipts, each
      re-derived at BASE; the round-48 SCORECARD section names neither at BASE.
  B6  S149 correction row: exactly one new registry row whose teaches opens
      `supersedes S149 \u2014`, states that FreeBSD is the origin of sysexits, status
      `rejected` kept, locator `ERRORS`, the quote located in the committed snapshot
      `corpus/evidence/round-49/c2/freebsd-sysexits.html`; S149's own line unchanged.
  B7  S147 tier correction row: exactly one new row `supersedes S147 \u2014`, tier B per
      CORPUS tier text, the quote and its heading located in
      `corpus/evidence/round-49/c2/popper.html`; S147's own line unchanged.
  B8  S138 grounding row: exactly one new row `supersedes S138 \u2014`, a located quote in a
      committed pinned snapshot that grounds the census (the member count S138 states),
      with `used-by`; S138's own line unchanged.
  B9  registry census: every `tools/round-49/**` `.py`/`.sh` path at BASE and every
      `tools/round-50/**` `.py`/`.sh` path at REV (control fixtures excluded) is the cell-0
      path of exactly one row of the marker-bound `instrument-registry v2` region of
      `SKILL.md`, with a gate|probe kind, an entry command naming the path, a verdict map
      binding 0/1/2 to meanings (the round-48 meaning rule, ported), a self-test spelling
      and a pinned-value path.
  B10 `tools/round-50/selftest-r49-c2.py` exists, and run from the REV bytes against this
      repository (`--root`) it exits 0 with `failures []`; its committed expected values
      (`tools/round-50/selftest-r49-c2.expected.json`) equal its output; correction line
      `B10` states the case count and the expected-file sha256 the counter re-derives.
  B11 the round-49 trend line: correction line `B11` states the round-49 closure's
      per-trend verdicts (expansion, quality, discernment, re-derived from
      `corpus/lessons/round-49-verifier-spotcheck.md` at BASE), its `Admission:` word and
      `spot_check=landed`; the round-49 SCORECARD section at BASE says discernment improved
      and the spot-check pending, a different verdict from the closure's, and that section
      is unchanged at REV (a correction is a new line, never a rewrite).

- Target: exit 0, `atoms_total 11`, `mismatches 0`, `battery.failing []`.
- Counting command: `python3 -I -B tools/round-50/c2-record.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --battery --work <SCRATCH> --json-out <OUT>`; before = `--rev <FREEZE>` (without
  `--battery`), after = `--rev <REV>`.
- Controls: the do-nothing run at the freeze (`mismatches 11`); the in-counter battery and its
  do-nothing overlay; `tools/round-50/c2-record.py --selftest` (cases listed in its output).
- Kill rule: a mutation leaving its atom green, turning another atom red, or a no-op; or a
  do-nothing overlay leaving any atom green, stops C2 and is reported as a miss.
- **Disclosed limits.** A consistency check of the record against committed bytes, not a
  judgment of prose. The round-48/49 atoms are the defects the closures named and this round
  chose, not every inaccuracy in the record (`w1/C2SelfAssess`-class items of round 49 remain
  routed). Tier B in B7 is a curation judgment checked only by the closure-disagreement binding,
  not recomputable (CORPUS.md lives at the fleet root). A whole-section rewrite elsewhere in the
  round-48 SCORECARD section is not caught except for the quoted sentences each atom guards.
  The registry check is row presence + cell shape + meaning words, not that the entry command
  runs; new rows sit in the `instrument-registry v2` block and so fall outside the frozen round-48
  `census2.json` (see above). `tools/round-49/` stays byte-frozen: the missing `--selftest` of
  `c2-mismatch.py` is supplied by `tools/round-50/selftest-r49-c2.py`.

## Frontier step (inside the claim cap)

- Sourced claim: R50-C1's entry cites SOURCES rows opened this round (S243 Freetz AVM_LE/AVM_BE
  define patch, S244 the AVM download index, S245 the unblob 26.6.4 LE handler); R50-C2's three
  correction rows are S246 (S147 tier), S247 (S149 provenance), S248 (S138 grounding). Ids S243+
  because S150–S242 are cited in earlier lessons as refused staged rows that were never registered
  (`w1/C1SrcFreetz.md` F6, `w1/C1SrcUnblob.md`); the registry therefore skips S150–S242 and the
  lesson says so.
- Assimilation: theme "AVM LE" from `merge/kaidoku/` read-only; per-entry admit/refuse and the
  collision guard are in the lesson `## Gate` and `.ufo/waves/round-50/assimilation/`;
  `considerthese/` is absent in this lane.
- Mistakes mined: M50-1 (source tier, provenance direction and over-wide `teaches` — class
  `attribution`/`scope`), M50-2 (counters landed unregistered — `landing`), M50-3 (the L1's own
  probe first-matched the wrong tar member and over-counted the census — `reference-drift`),
  M50-4 (credential-class cookie values at the tip in a round-45 receipt).

## Frozen paths

Byte-frozen: `plans/round-50-claims.md`; `tools/round-50/` (directory; populated before FREEZE,
including `carriers.json`, `gap-rule.json`, `oracle/**`, `control-fixtures/**`, both counters,
the run harness, the fetch tool, the controls driver, the self-test and its expected file); for C1
additionally `tools/round-41/sqfs-list.py` and `tools/round-27/xpin-attribute.mjs` (carried-over
inputs the instruments name). Not frozen (each counter binds what it reads): `PROVINCE.md`,
`corpus/README.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`,
`corpus/knowledge/*`, `corpus/lessons/*`, `corpus/evidence/round-50/**`.
