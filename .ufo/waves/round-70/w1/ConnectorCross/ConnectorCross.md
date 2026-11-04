# ConnectorCross — round-70 w1 seat report (sibling-overlap scan)

Full evidence, per-ground rows and the connector move: `scan.md` beside this file.
Bounds honored: writes only under `.ufo/waves/round-70/w1/ConnectorCross/` and
`/fast/scratch/hyaku/kaidoku-r70/ConnectorCross/` (scratch removed at close; nothing was
written to it — all evidence was read from the read-only trees). No tools installed.
No sibling repo, `.ufo/state/`, watchdog log or fleet-root file touched. Read-only git only
(`rev-parse`, hash checks).

## Context check

- Freeze pins clean at HEAD `67217e0987a2b31253d0b77f1490a1bfd031575a`: all six
  `tools/round-70/*.py` sha256s equal the `claims.json` instrument pins and the three
  `tools/round-69` bytes equal `loaded_by_counter` — no post-freeze instrument drift.
  (Freeze `4737a542ae3b1b910d8fe43efbd572bc578b07c6`.)

## Sibling-overlap scan (one row per ground item; detail in scan.md)

| Ground item | Owner | Overlap verdict | Absorb or stay |
|---|---|---|---|
| (a) Provenance-bound receipt readers (R70-C1) | none — kake holds the nearest primitive (`instrument-receipts/v1` blob receipts at a named revision over its own gate registry) and itself records tabi/chousa/souji/tameshi variants as adjacencies that "stay with those lanes" | method-adjacent; kaidoku's variant is the enforcing *consumer* (reader refuses wrong-producer receipts; ten-shape forgery battery) — unclaimed anywhere | stays in kaidoku's REA-triage province; no sibling ground absorbed |
| (b) Safe packer seam (R70-C2) | none — tsukuroi refuses binary RE (ADJ-06); tameshi owns only the reusable hermetic/mutation *method* and never edits sibling gates | method-adjacency only (tameshi craft behind `mutation-check.py`) | stays in kaidoku's province (lane's own route tool, routed defects M69-9/S-1, M69-10, M69-11) |
| (c) Packed static-exe carrier class (R70-C3) | none — kaidoku's own round-68/69 Frontier notes name "packed static binaries" as still-Frontier; revenger (the lane's only open split) refuses harness/gate auditing and holds no UPX-route claim | absorb-within-lane per kaidoku's own declared Frontier note; revenger adjacency named, arbitration undisturbed | stays in kaidoku's province (bounded: UPX-only, count-equality only) |

**No other lane owns this round's ground.** REA/binary-adjacent siblings (revenger,
game-dev-3d, tabi, tsukuroi) either refuse the surface explicitly or use REA as supporting
static inspection only (kotoba round-74 census: kaidoku class `none`, open split = revenger
only).

## Assimilation line (MERGE-REPORT, read-only)

`/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md` stages corpus-expansion themes
(SOURCES rows rounds 1–16 + 77 knowledge entries: adb grammar, AVM/SquashFS/sasquatch,
`.jsc` mapper, evidence-graph ratio, CJK literature). **No staged theme serves R70-C1/C2/C3**:
no receipt-identity, no subprocess/env seam, no packer rows; R70-C2's grounding source (the
Python `subprocess` environment contract) is opened this round per the plan, not staged.
Assimilation: **none** — independently confirms the frozen declaration.

## Connector move (defect named, report-only; instruments frozen)

The C1 battery `tools/round-70/forged-receipts.py` executes materialized base blobs
(`blob_to` → `git show`, :62-69, :171-175) **without hashing them against anything**: no
`loaded_by_counter` comparison exists in the battery, its receipt (:276-287) records base
rev/paths but no base blob sha256s, and the kill rules cover post-freeze instrument edits but
not base-blob drift at run time. The same round's seam probe already implements the needed
idiom (`bind_producer`, QUALITY #114, `seam-probe.py:147-166`; A2 re-hashes `--expect-upx`).
**Move for the next freeze touching the C1 instrument:** hash every materialized blob
(base reader/probe/battery, and the measured-rev pair for symmetry), accept
`--expect-base-tool-sha256`/`--expect-base-probe-sha256`/`--expect-battery-sha256` argv
(self-contained, mirrors `--expect-upx`), exit 2 could-not-evaluate on mismatch, record the
executed blob sha256s in `battery_arms`, add a wrong-base-pin selftest case following the
existing wrong-world-control pattern. Axis effect: strengthens **calibration** (R70-C1's
before-arm chain becomes machine-checked end-to-end); no effect on operability or coverage
(instruments untouched); it is the compatible synthesis of C1's forgery rejection and C2's A2
producer-binding — closing the one input side neither binds today. Risk: any argv change must
wait for a new freeze (predicate command shape), hence report-only. Current pin state is
clean, so the gap is latent; today's landing receipts stay valid.

## VERDICT

VERDICT: met — sibling-overlap scan complete for all three ground items (no sibling owner;
round stays inside kaidoku's REA-triage province), MERGE-REPORT assimilation no-fit, pins
clean at HEAD, and one calibration-axis defect named (C1 battery lacks base-blob pin binding)
with a next-freeze repair shape; findings recorded in scan.md + this report, nothing landed.
