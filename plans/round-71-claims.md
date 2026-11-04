# Round 71 — declared claims (frozen; no amendments after this file's container commit)

Base `82c8e620c9222fb218aa0260570a3765da2afb44` (the round-70 lane tip: report, close and the
non-author spot-check; the lane tree is clean and pushed). Three claims on three distinct axes,
causally separable: each is scored by its own instrument and none reads another's result. All
three are capability acquisitions in the AXES sense — the instrument runs, its output verifies,
and its row enters the SCORECARD capabilities table in the same round. The stagnation nudge is in
play: every owned axis sits at 10.0 (saturation line 10.0, window 10; `SCORECARD.md`), so the
lowest-axis obligation is waived and this round is a capability/frontier move.

The round-70 non-author closure routed seven defects (`.ufo/reports/round-70/kaidoku.md`
§Routed defects). Three of them are this round's work: (3) the six lying-field shapes had no
committed landing receipt → R71-C2 builds that receipt; (1) the round-70 capability rows are
absent from the SCORECARD table → repaired in the record commit; (4) the SOURCES search log and
the tempfile rejection row → repaired in the frontier step. Two more ride the record commits:
(2) the census W04 count erratum and (5) the `ca9817cf`/`ca9817cd` hash erratum, both appended,
never rewritten. (6) the wave-settlement receipt is written for this wave; (7) the dead scratch
pointers inside receipts are named as run pointers, not evidence.

## R71-C1 — coverage: the seam's runtime evidence class (Frontier → Core)

**Type.** Capability acquisition (three runtime arms + a pre-committed run binding), moving the
round-70 Frontier line "runtime env-capture/concurrent-scratch coverage of the seam arms"
(`corpus/README.md`, round-70 note; M70-6) into Core for the measured route.

**Falsifiable before → after.** At the round-70 landing the seam probe has seven arms
(`tools/round-70/seam-probe.py`, 7 of 7) and its child-environment evidence is the builder's
returned dict plus committed selftest cases; A7 is two sequential battery runs; the receipt has no
run-scoped identity, and the route's REA/readelf/git children inherit the caller environment
(SentinelScope advisory 2). After the round: `tools/round-71/packed-elf.py` routes EVERY child
through the same four-key allowlist and can record each child's OBSERVED environ; the receipt
carries `run_root`, `child_env_observed`, `run_nonce` and `run_binding`; `--check-receipt
--nonce-commitment` rejects a transplanted or altered receipt; and the new probe arms A8/A9/A10
measure all of it at runtime. Against the round-70 route the same probe reports 7 of 10 naming
A8/A9/A10 false.

**Predicate (one sentence, frozen).** R71-C1 is verified iff the frozen seam probe, run at the
measured revision as `python3 -I -B tools/round-71/seam-probe.py --root . --rev <measured> --tool
tools/round-71/packed-elf.py --battery tools/round-70/mutation-check.py --pkg <REA 6.5.0 root>
--work <scratch> --receipt <landing receipt> --expect-upx <pinned copy> --nonce-commitment
<pre-committed nonce hash> --legacy-receipt .ufo/waves/round-70/l1/scores/c3-at-landing.json
--json-out <receipt>`, reports `arms_passed 10` of `target 10` — A1..A10 each true, including
A8's observed child environment parsed by the probe from the raw per-child log (key set exactly
HOME/LANG/PATH/TMPDIR, the packer, node and readelf children present, HOME and TMPDIR under that
run's own run_root, the exported canary absent), A9's three concurrent battery runs and three
concurrent route preflights (distinct work_dirs, distinct run_roots, each env log under its own
root), and A10's pre-committed binding (sha256(run_nonce) equals the commitment, run_binding
re-derives from nonce + instrument + packed pins, the genuine receipt accepted, the transplanted
round-70 receipt, a wrong-nonce copy and a broken-binding copy each rejected with their clause) —
while the same probe at the round-70 landing `7c155617bb42dadf1725b88a06fe3f235c364f0a` against
`tools/round-70/packed-elf.py` reports `arms_passed 7` of target 10 naming A8_child_env_observed,
A9_concurrent_collision and A10_run_binding false.

**Counting command.** The probe command above — exit 0 met, 1 each failed arm named with its
observation, 2 could-not-evaluate (unknown revision, missing host tool, bad argv).

**Kill rule.** Any arm false; an A8 whose raw-log key set differs from the allowlist or whose
canary reaches a child; an A9 with a shared work_dir/run_root; an A10 whose genuine receipt is
rejected or whose altered copies are accepted; a base arm true; a post-freeze instrument edit →
not verified, reported, never narrowed.

**Do-nothing control.** `tools/round-71/controls.py` arm `c1-base-world` (the round-70 route at
its own landing scores 7 of 10, A8/A9/A10 false — the world a do-nothing control holds) and arm
`c1-constant-probe` (a receipt asserting ten true arms with empty observations is rejected by
`--validate`).

## R71-C2 — calibration: the lying-field classes have their landing receipt

**Type.** Capability acquisition (the six lying-field shapes enter the frozen battery) plus the
repair of the round-70 routed defect 3.

**Falsifiable before → after.** At the base the round-70 battery's committed landing receipt
carries twelve forged rows (ten base-world shapes + two landing-world identity shapes) and no
lying-field row: the six classes the round-70 supersession bound (`unpacked_counts`,
`packed_sha256`, `section_count`/`upx_list_rc`, `runs`, `refusal`, `format`) are source clauses
with no receipt exercising them (round-70 verifier, routed defect 3). After the round the frozen
battery carries eighteen forged rows: the ten base-world shapes (base reader accepts, superseded
reader rejects with its clause), the two landing-world identity shapes, and the six lying-field
shapes cut from the round-70 landing receipt and relabelled to the round-70 FIRST-CUT world
(`4737a542ae3b1b910d8fe43efbd572bc578b07c6`), each accepted by the first cut and rejected by the
superseded reader at `7c155617…` naming its declared clause.

**Predicate (one sentence, frozen).** R71-C2 is verified iff the frozen forged-receipt battery, run
at the measured revision as `python3 -I -B tools/round-71/forged-receipts.py --root . --rev
<measured> --base-rev 5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d --tool tools/round-70/packed-elf.py
--base-tool tools/round-69/packed-elf.py --probe tools/round-70/contract-probe.py --base-probe
tools/round-69/contract-probe.py --base-probe-rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a
--battery tools/round-70/mutation-check.py --base-material
.ufo/waves/round-69/l1/scores/c3-at-landing.json --landing-material
.ufo/waves/round-70/l1/scores/c3-at-landing.json --first-cut-rev
4737a542ae3b1b910d8fe43efbd572bc578b07c6 --first-cut-tool tools/round-70/packed-elf.py
--superseded-rev 7c155617bb42dadf1725b88a06fe3f235c364f0a --pkg <REA 6.5.0 root> --work <scratch>
--json-out <receipt>`, exits 0 with the ten base-world shapes accepted by the base reader and
rejected by the superseded reader each naming its declared clause, the two landing-world identity
shapes rejected by the probe on A5_carrier_record with A6_packer_pin true, the six lying-field
shapes L1_unpacked-counts, L2_packed-sha, L3_section-list, L4_runs-argv, L5_refusal and L6_format
each `first_cut_rc 0` and `superseded_rc 1` with its declared clause found
(unpacked_counts, packed_sha256, section_count, runs.pack.argv, refusal, format), the genuine
receipts still accepted by both frozen readers, and the battery's pin/floor/work-dir/constant arms
green — while the round-70 battery's committed landing receipt
`.ufo/waves/round-70/l1/scores/c1-at-landing.json` carries `shapes 10`, `landing_probe_shapes 2`
and no `lying_shapes` row (the do-nothing control).

**Counting command.** The battery command above — exit 0 met, 1 each failing arm named, 2
could-not-evaluate (unknown revision, unreadable material, bad argv).

**Kill rule.** A first-cut rejection, a superseded acceptance, a declared clause missing from the
failing list, a base-world shape's base-acceptance failing, a genuine receipt rejected, a battery
pin/floor/work-dir/constant arm red, or a post-freeze instrument edit → not verified, reported.

**Do-nothing control.** `tools/round-71/controls.py` arm `c2-do-nothing` (the round-70 receipt:
12 forged rows, 0 lying-field rows, target 16) and arm `c2-constant-battery` (six lying rows whose
rc pair is (0, 0) are rejected by `--validate`).

## R71-C3 — operability: the registry's own drift census runs again

**Type.** Capability acquisition (registry row grammar v2 as a runnable census) plus the repair of
the round-70 routed M70-7 standing defect and a disclosed repair of the six round-70 registry rows.

**Falsifiable before → after.** At the base `tools/round-51/census3.py --check` exits 2 —
"registry row must have seven cells" — because four round-69 rows carry a bare `|` inside the
pinned-value cell (eight cells) and six round-70 rows omit the owner cell (six cells); the
registry drift census has been unevaluable since `616a5f2f` (round-70 M70-7). After the round
`tools/round-71/registry-census.py` reads both filed shapes under a declared grammar (split on
unescaped pipes, unescape `\|`, owner = last cell, write scope = second-last, pinned = the joined
middle cells), reports zero nonconformant rows and zero duplicates over the whole registry, and
its selftest proves it can fail (a five-cell row, a six-cell row, an absent path, a duplicate, a
marker error). The six round-70 rows gain the owner cell they omitted (disclosed old→new in
`LOG.md`); the four round-69 rows are never rewritten and are read by the join rule.

**Predicate (one sentence, frozen).** R71-C3 is verified iff the frozen registry census, run at
the measured revision as `python3 -I -B tools/round-71/registry-census.py --root . --rev
<measured> --generate --out <receipt>`, exits 0 with the registry's data rows all conformant
(`nonconformant []`, `duplicates []`, `paths` equal to the row count), the four round-69 eight-cell
rows recorded as multicell rows read by the declared join rule, and the six round-70 six-cell rows
carrying seven cells after this round's disclosed SKILL.md repair — while the same instrument at
the base revision `82c8e620c9222fb218aa0260570a3765da2afb44` reports six nonconformant rows with
defects `['pinned-empty']` and exit 1, `tools/round-51/census3.py --root . --rev <same base>
--check` exits 2 with "registry row must have seven cells", and the census's 14-case selftest is
green.

**Counting command.** The census command above — exit 0 met, 1 each nonconformant row named, 2
malformed markers or unavailable SKILL.md.

**Kill rule.** Any nonconformant row, any duplicate, an absent registered path, a new malformed
row (not one of the four filed multicell rows) accepted, the base run not naming six rows, or a
post-freeze instrument edit → not verified, reported.

**Do-nothing control.** `tools/round-71/controls.py` arm `c3-base-nonconformant` (at the base the
census reports six rows, exit 1) and arm `c3-junk-row` (a scratch registry with a five-cell row is
rejected with `cells<6`, `pinned-empty`, `path-absent`).

## Sourced claim

R71-C3 rests on the GFM table grammar opened this round: row **S273** (GFM 4.10 Tables — the
cell-count tolerance sentence), cited by the knowledge entry
`corpus/knowledge/2026-11-04-r71-registry-grammar.md`, whose source line names S273. S258 remains
the authority for the escaped-pipe rule and is cited beside it; S273 is the new row this round
opens for the reader's tolerance decision. The claims container names `claim_row: "S273"`.

## Frontier step (§2b)

`corpus/SOURCES.md` gains only rows opened this round: S273 (GFM cell-count tolerance, tier A
`spec`, snapshot and quote in the lesson `## Gate`) and S274 (the Python `tempfile.mkdtemp` page —
REJECTED: it does not ground distinctness, uniqueness or collision-freedom, flip if a consumer
needs mode/ownership/absolute-path properties; this closes routed defect 4's missing rejection
row). The round-70 search log entry and the round-71 entry are appended to `## Search log`. One
mistake is mined into `corpus/lessons/round-71.md` `## Mistakes` — the round-70 registry rows
omitted the owner cell (a defect no gate caught because the frozen parser died before reaching
them; captured by the new grammar census). No `considerthese/` directory exists in this lane;
`Assimilation: none` this round (the `merge/kaidoku/` package does not serve these three claims).

## Repairs carried (not claims)

R71-G1 (the round-70 capability rows enter `SCORECARD.md` `## Capabilities`), R71-G2 (census W04
erratum: 21 warnings, not "the same 20", appended to the round-70 lesson and the LOG), R71-G3 (the
`ca9817cf` typo erratum: the supersession is `ca9817cdf9c73801569bff8a20aac6856647cbb2`), R71-G4
(the round-71 wave-settlement receipt), R71-G5 (SOURCES search log + the tempfile rejection row),
and the standing duties re-run (census start/end, registry census, receipt audit, no-`/tmp`
fixtures).

## Freeze mechanics

Instruments are committed before this plan's container (`QUALITY #33`): the declaration commit
carries `tools/round-71/{packed-elf,seam-probe,forged-receipts,registry-census,controls}.py` and
this plan; the pre receipts (`l1/pre/c1-at-base.json`, `c2-do-nothing.json`, `c3-at-base.json`,
`controls-at-declaration.json`) are measured at that state and committed before the container; the
freeze commit is the first commit adding `.ufo/waves/round-71/claims.json`, which pins the five
tools by sha256 and holds the three predicate sentences byte-identical to this file.
