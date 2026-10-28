# kaidoku round 49 — claims (the FREEZE commit pins these bytes)

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` (lane `main` at round start; it contains
`corpus/lessons/round-48-verifier-spotcheck.md`, the non-author closure of round 48). L1
`KaidokuR49` holds the section-3 planner seat (the wave validator rejects `planner` as a swarm
role; planning data-walks rode scout/connector/revenger seats — recorded in the report).

Round 48 closed **rejected-harmed**: both claims re-measured, but `calibration` was harmed by a
false declared-freeze header in the round's own lesson and `quality` by two source-record errors.
Round 44's C1 stopped on a claim/counter disagreement about where the receipt's provenance lives.
This round's design answers both. **One freeze, committed before any data run and before wave 2.**
Wave 1 (48 seats, `.ufo/waves/round-49/w1/`) attacked the *drafts* of the instruments and this
plan; its defects are folded in below, before the freeze, and are recorded in the next section.
Wave 2 attacks the frozen counters and the landed bytes. No amendment series: a counter bug found
after the freeze is reported as a miss, never patched, and a predicate below is the same sentence as
the counter's docstring and its code.

Owned axes coverage / depth / calibration are tied at 10 in `SCORECARD.md`, none retired; on the
tie every owned axis is a lowest axis. R49-C1 works **coverage**; R49-C2 works **calibration**.
They are causally separable: C1 reads the four frozen carriers, the committed oracle trees, the
REA receipts under `corpus/evidence/round-49/c1/`, `PROVINCE.md`, `corpus/README.md`, the entry
`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` and SOURCES rows S138/S139 (`opened`,
`used-by`); C2 reads round-48 inputs at the round-49 base, and `corpus/lessons/round-49.md`,
`SCORECARD.md`, SOURCES rows S145–S148 and the search log, `LOG.md` and the committed snapshots at
REV. The only shared path is `corpus/SOURCES.md`: C1 reads rows S138/S139, C2 reads rows S145–S148,
the search log and the id set. Wave-1 seat `ConnSeparability` built a C1-only tree, a C2-only tree and
both together and scored each counter on each: C1 green on the C1-only tree, C2 green on the C2-only
tree, both green together (`.ufo/waves/round-49/w1/ConnSeparability.md`). C2's battery do-nothing
overlay reads the *names* of paths the C1 landing writes; it restores them to FREEZE blobs and does
not read their content.

## Wave-1 amendment record (folded into this text and the tools before the freeze)

| wave-1 finding (seat report under `.ufo/waves/round-49/w1/`) | disposition |
|---|---|
| `C1ProvCritic`, `C1GoldForgery`, `C1RunMut`, `C1ControlsReview`, `C1R44Revenge`, `C1PlanMatch`: a round-44 receipt with `output_directory` rewritten and the evidence id re-minted, or an envelope computed from the committed oracle, scores `carriers_matched 4`; the plan said the committed path is "not the output directory" and "the counter implements" it; `provenance_ok` was a substring test | **Re-scoped, not hidden.** The claim is now stated as what the counter measures: REA's behaviour on the four frozen bytes, reproduced by the counter's own rerun at score time. `provenance_ok` is a prefix test (`/fast/scratch/hyaku/kaidoku-r49/`). The relabelled replay and the oracle-complete fabrication are **disclosed limits** (below), not kill-rule controls |
| `C1CounterMut`, `C1PlanMatch`: `unpublished_entries == []` / `gaps == []` not enforced; the freeze walk ignored added files; clauses outside the plan (`carrier_size_ok`, `carve_ok`, `oracle_ok`, `carrier_fresh_ok`, `receipt_fresh`, `frozen_tables_valid`) named nowhere; no `target` key in `carriers.json` | Quiet-carrier rule added to `nonregular_unpublished_ok`; walk now counts an added file under `tools/round-49/`; the extra clauses are named in the predicate; `TARGET = 4` constant is the target (the table has no `target` key) |
| `C1CounterMut`, `C1ControlsReview`: CTL-C1-5 plants bytes the counter never reads and cannot fail; CTL-C1-4 planted round-42 envelopes, not the plan's shortcut | CTL-C1-5 retired from the default set (the superblock probe is witnessed by named selftest cases); CTL-C1-4 now plants the committed round-44 receipts verbatim |
| `C1CounterMut`: 35 of 75 single-point mutants of the counter survive `--selftest` | Six selftest cases added (quiet-carrier gap, unpublished row, provenance under `/tmp`, provenance with the segment inside a lane path, added file under the frozen directory); the plan does **not** claim clause-level witness completeness (limit below) |
| `C1RunReview`, `C1Sentinel`, `C1TmpScratch`: runner could write outside the evidence root, `--force` removed arbitrary directories, `..` carrier ids, copy failure non-fatal, comments quoting a plan sentence that did not exist | Runner patched in the draft (id regex, evidence-root write scope, `--fake-rea` never into the committed root, copy failure fatal, `outdir_mode` default `scratch`, comments corrected) |
| `C1DocBindings`: the six documentation bindings are presence checks | Disclosed limit |
| `C2PlanMatch`, `C2GoldForgery`, `C2CounterMut`, `C2MutAtoms`, `C2LogPtr`, `C2SearchLog`, `C2RederiveA`: round-48 inputs were read at REV (editable after the freeze), A3 checked only the pointers the lesson chose to state, duplicate atom lines and headings were "last/first wins", A7 matched a token, A8 did not check contract elements, quote word counts were not re-derived | Every round-48 input is read at the base; A3 requires the exact hash and `unnamed` sets (`c093e798` and `7fe11332` added from the fleet-report sweep `C2FleetSweep`); duplicates are mismatches; A7 requires `EX_USAGE is 64` and no other status; A8 requires `where searched:`, `stop:` and, when excluded > 0, `exclusion:`; word counts re-derived; battery grows to 16 mutations (every one turns exactly its atom red) |
| `CritFreeze`: C1's walk refused less than C2's; counter bytes and the operator-chosen `--freeze` are unbound; `refs/replace`, grafts and squashes are invisible | C1 walk aligned (adds, non-ASCII names); C2 exits 2 `counter_not_frozen` when its bytes differ from FREEZE's blob; the rest are **disclosed limits** with a mitigation (below) |
| `ScoutPriorClosures`, `C2SelfAssess`: further open items from rounds 46–48 and ten more round-48 self-assessment mismatches | Not claimed; routed in the report (the claim repairs the nine atoms named below, not "every" mismatch) |

## Freeze-integrity rule (both claims)

A score at `REV` is admissible only if `FREEZE` is an ancestor of `REV` and no commit in
`FREEZE..REV` adds, changes, renames or deletes a path under `tools/round-49/` or the plan
(C1's merge-aware walk and C2's `git log -m --diff-merges=first-parent` walk, both with
`core.quotePath=false`), and every frozen blob equals its FREEZE blob; a later restore does not
un-block (exit 2 `frozen_path_changed`, never `met`). C1 additionally freezes the explicit paths of
its `FROZEN_PATHS`, the oracle trees `corpus/evidence/round-44/oracle/**` and the committed carriers
under `corpus/evidence/round-44/carriers/`; C2 binds its round-48 inputs by reading them at the
base instead. C2 refuses to run when its own bytes differ from the FREEZE blob. **Disclosed
limits:** neither counter can bind the operator's choice of `--freeze`, `refs/replace`, grafts, or a
squash that drops the touching commits. Mitigation: the L1 writes the FREEZE hash to
`.ufo/waves/round-49/l1/FREEZE` and to LOG.md and commits both before any data run; every score
runs with `GIT_NO_REPLACE_OBJECTS=1`; every receipt records exit code, stdout sha256, counter sha256
and the counter's blob at FREEZE.

## R49-C1 — coverage: SquashFS v1 and v2 through REA `extract-firmware` → Core

Surface moved: the Frontier clause `SquashFS v1/v2` (`squashfs_v1`, `squashfs_v2`) of `PROVINCE.md`
(round-42 frontier note; re-stated as still-Frontier by the round-44 note, whose claim R44-C1
stopped: `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`). The command that shows it
unmoved at the freeze: `python3 -I -B tools/round-49/c1-counter.py … --rev <FREEZE>` exits 1 with
`carriers_matched 0` and every documentation binding false. The claim moves the two handler
families to Core on the four frozen standard fixtures (v1.0 and v2.0, both byte orders), not on
every v1/v2 image. What round 49 changes against round 44 is the **predicate**, not the carriers.

**What the counter measures.** At score time the counter runs REA 6.5.0 `extract-firmware` itself
on each frozen carrier and requires the result to equal the committed after-receipt's semantic
projection and to publish every member of the independent oracle. That rerun is the measurement.
The committed receipt is the audit record of a run and of the evidence id minted over its output
directory; the counter does **not** authenticate who wrote it or in which round (disclosed limit
below: a relabelled replay of genuine data scores the same as a fresh run, because they are equal in
every field the counter reads).

**Frozen carriers** (ids in `tools/round-49/carriers.json`; all four are committed MIT unblob 26.6.4
fixtures under `corpus/evidence/round-42/c2/fixtures/`, pins re-verified against the committed
copies, `tools/round-42/fixtures.json` and the upstream `__input__` bytes by wave-1 seat
`C1CarrierPins`):

| id | file | handler | endian | oracle |
|---|---|---|---|---|
| v1le | `v1-le--squashfs_v1.0_le.bin` | `squashfs_v1` | le | `unsquashfs` -lls census + unblob `__output__` tree |
| v1be | `v1-be--squashfs_v1.0_be.bin` | `squashfs_v1` | be | same |
| v2le | `v2-le--squashfs_v2.0_le.bin` | `squashfs_v2` | le | same |
| v2be | `v2-be--squashfs_v2.0_be.bin` | `squashfs_v2` | be | same |

`squashfs_v2_nonstandard` (`v2ns-*`) stays Frontier (no independent reader). The v2.1 outputs are
not carriers. The oracle was re-derived by wave-1 seat `C1OracleIndep` with `unsquashfs` 4.7.5 and
7-Zip 26.04 (no disagreement with `carriers.json`).

**Predicate P49-C1** (`tools/round-49/c1-counter.py`, the round-44 counter ported and amended as
the table above says; its docstring clause list is this predicate). At the measured revision REV,
for each frozen carrier, the committed REA 6.5.0 `extract-firmware` after-receipt
`corpus/evidence/round-49/c1/<id>/after.json` (unblob 26.6.4, sasquatch 4.5.1 on the child PATH),
first added in a commit that descends from the freeze, names the carrier's frozen
`squashfs_v1`/`squashfs_v2` handler with no failed chunk, publishes every regular file of the
frozen independent oracle at its exact relative path under the chunk extract root with the same
sha256 and size and no extra regular file; carries `gaps == []` and `unpublished_entries == []`
(all four oracles hold no non-regular member); has a subject digest equal to the carrier pin and
recomputes its evidence id; the carrier bytes hash to the pin and their superblock reads the frozen
magic, `s_major`, `s_minor` and endianness; **and** a counter-time REA rerun of the same bytes has
the same semantic projection as the committed receipt; **and** the receipt's
`parameters.output_directory` is an absolute path that starts with
`/fast/scratch/hyaku/kaidoku-r49/` (prefix test, no `..`; the evidence id is minted over that
provenance; the committed evidence path is not the output directory). The counter's further
carrier clauses (`carrier_size_ok`, `carve_ok`, `oracle_ok`, `carrier_fresh_ok` against
`tools/round-42/prior-pins.json`, `receipt_fresh`, `frozen_tables_valid`) are part of the predicate
as its docstring lists them; `carrier_fresh_ok` does not see the round-44 measurement. Documentation
bindings: `PROVINCE.md` holds a `## Round-49 additions to Core` section whose row names `squashfs_v1`
and `squashfs_v2`, names SquashFS v1/v2 and cites the entry path; one line carries
`Round-49 frontier note`, the entry stem and a SquashFS v1/v2 token; the entry exists at REV and its
`source:` lines cite S138 and S139, both rows opened `2026-10-28` and listing the entry in
`used-by`; `corpus/README.md` `## Coverage map` maps the entry stem; no frozen C1 path changed after
the freeze.

- Target: `carriers_matched == 4` (`TARGET = 4` in the counter), every binding true,
  `frozen_path_changed []`, exit 0.
- Counting command: `python3 -I -B tools/round-49/c1-counter.py --root <LANE> --rev <REV>
  --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --json-out <OUT>`
  (`<SCRATCH>` under `/fast/scratch/hyaku/kaidoku-r49/`).
- Data procedure (after the freeze, by the L1 only): `tools/round-49/c1-run.sh --data-run` writes
  `corpus/evidence/round-49/c1/<id>/`.
- Controls (scored at the FREEZE commit before any data run; inputs frozen in
  `tools/round-49/control-fixtures/**`, receipts committed after scoring under
  `.ufo/waves/round-49/controls/`): CTL-C1-0 do-nothing (exit 1, `carriers_matched 0`, documentation
  bindings false); CTL-C1-1 round-42 v3 receipts relabelled (red); CTL-C1-2 envelopes fabricated
  from the oracle with an incomplete projection (red); CTL-C1-3 sasquatch absent from the child PATH
  (red, `missing-extractor-dependency`); CTL-C1-4 **the round-44 receipts copied verbatim** to the
  round-49 path (red, `run_provenance_ok` only); CTL-C1-POS real scratch receipts plus the landing
  blocks (exit 0, `carriers_matched 4`, every binding true; not a counterfactual).
  `.ufo/waves/round-49/controls/summary.json`.
- Kill rule: CTL-C1-0 or CTL-C1-4 reaching `carriers_matched == 4` with every binding true, or the
  do-nothing tree at the freeze scoring any carrier clause green, stops C1 before data.
- **Disclosed limits (each with its wave-1 receipt).** (1) A relabelled replay — genuine round-44
  receipts with `output_directory` rewritten and the evidence id re-minted — scores `carriers_matched
  4` and, with the landing blocks, exit 0; so does an oracle-complete fabrication (md5/sha1 report
  computed from the committed oracle bytes): `w1/C1ProvCritic.md` F1–F6, `w1/C1GoldForgery.md`,
  `w1/C1RunMut.md`. They do not skip the claimed work — the counter performs the REA run — and they
  are therefore not kill-rule controls; they do mean the committed receipt cannot be cited as proof
  of *when* or *by whom* it was produced. (2) The six documentation bindings are presence checks; a
  documentation set that asserts the opposite scores exit 0 with genuine receipts
  (`w1/C1DocBindings.md` variant 16). The landing text is therefore reviewed by wave 2, not by the
  counter. (3) `--selftest` kills 40 of 75 single-point counter mutants and the controls add one
  (`w1/C1CounterMut.md`); this round adds the cases above but does not claim every clause has a
  witness. (4) The carriers are the four round-44 fixtures (4 KiB, 3–4 regular files of 6–7 bytes, no
  symlink, device, fragment or multi-block member), already measured once in round 44 and on a
  pre-freeze scratch arm this round: **not new data**. No published v1/v2 rootfs image was fetchable
  in round 44. (5) `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4
  Broadcom, LE AVM (`hsqs`), AVM kernels and nested sub-images below depth 1 stay Frontier.

## R49-C2 — calibration: nine round-48 self-assessment mismatches counted and repaired

The round-48 closure (`corpus/lessons/round-48-verifier-spotcheck.md`, "Routed defects") named
defects in the lane's own record. Each is an **atom**: a statement the lane made, or a statement
the repository still carries, paired with a re-derivation from committed bytes.
`tools/round-49/c2-mismatch.py` evaluates nine atoms and counts those whose re-derivation disagrees
with the record or whose correcting record is absent. A1–A9 are listed in the counter's docstring,
which is this claim's predicate verbatim: A1 declared-freeze header; A2 dead commit hash; A3 LOG.md
pointer sets (`2e785632`, `33f65a91`, `c093e798`; unnamed `577a02a5`, `8847042a`, `7fe11332`); A4 wave
accounting (seats, report artifacts, missing); A5 receipt digests (raw vs newline-stripped); A6 S145
wrong locator → row S147; A7 S146 wrong rationale → row S148; A8 search-log entries for round 48
(late) and 49; A9 the SCORECARD calibration record against the closure verdict.

**Predicate P49-C2.** At REV, with FREEZE an ancestor of REV, the frozen paths untouched and the
counter's bytes equal to FREEZE's, `python3 -I -B tools/round-49/c2-mismatch.py --root <LANE> --rev
<REV> --freeze <FREEZE> --battery` reports `atoms_total 9`, `mismatches 0`, a battery in which each
of sixteen single-mutation overlays turns exactly its own atom red (and none is a no-op), a
do-nothing overlay (every path changed since FREEZE restored to its FREEZE blob) that turns all nine
red, and exits 0. At FREEZE the same command without `--battery` reports `mismatches 9`, exit 1.

- Target: exit 0 with `mismatches 0`, `battery.failing []`.
- Counting command: as above; before = `--rev <FREEZE>` (9), after = `--rev <REV>` (0).
- Controls: the do-nothing at the freeze (`mismatches 9`); the in-counter battery.
- Kill rule: a mutation that leaves its atom green, turns another atom red, or is a no-op, or a
  do-nothing overlay that leaves any atom green, stops C2 and is reported as a miss.
- **Disclosed limits.** The counter is a consistency check: A6/A7 bind a row to a committed,
  sha256-pinned *snapshot*, not to the live page (wave-1 seats `C2RederiveB`, `C2RederiveC`,
  `C2PlanMatch` and `C2GoldForgery` found the snapshots byte-equal to the live pages today, which the counter cannot
  see); `identified` in A8 is asserted by the lane and not derivable; prose is not judged. The atoms
  are the nine defects the closure named and this round chose to repair, not every inaccuracy in the
  lane's record (wave-1 `C2SelfAssess` lists ten more, routed). **Routed, not repaired** (round-48
  claims stay frozen): `tools/round-48/census2.json` binds only `paths` (closure defect 5) and
  `tools/round-48/record2.py` imports `tools/round-46/gate.py` from the worktree (defect 6).

## Frontier step (inside the claim cap)

- Sourced claim: R49-C1's entry cites S138 and S139, re-opened this round (access date and located
  quote in `corpus/lessons/round-49.md` `## Gate`); R49-C2 adds S147/S148 from re-opened sources
  with committed sha256-pinned snapshots.
- Assimilation: none (no `considerthese/`; wave-1 `ScoutAssimilation` found no staged `merge/kaidoku/`
  entry that is in province, cheap and not held; nothing adopted).
- Mistake mined: M49-1 `reference-drift` — the round-48 lesson header named a freeze that was
  amended away; captured-by `none`; the fix is atom A1 plus its battery mutation.

## Frozen paths

Byte-frozen: `plans/round-49-claims.md`; `tools/round-49/` (directory, populated before FREEZE,
including `control-fixtures/**`); for C1 additionally `tools/round-42/fixtures.json`,
`tools/round-42/c1-counter.py`, `tools/round-42/prior-pins.json`, `tools/round-42/rea-pkg.json`,
`tools/round-39/gen-squashfs.py`, `tools/round-27/xpin-attribute.mjs`, `corpus/evidence/round-44/oracle/**`.
Not frozen (each counter binds what it reads): `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`SCORECARD.md`, `LOG.md`, `corpus/knowledge/*`, `corpus/lessons/*`, `corpus/evidence/round-49/**`.
C2 does not enforce the C1-only paths; it reads none of them.
