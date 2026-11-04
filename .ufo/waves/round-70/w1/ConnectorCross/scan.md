# ConnectorCross — round-70 w1 sibling-overlap scan (seat ConnectorCross)

Scope read: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` (Core + Frontier +
dated round sections), all 21 sibling `PROVINCE.md` files under `/home/vgpnk/Projects/shokunin/*-shokunin/`
(read-only), kotoba's fleet sibling-overlap census re-pin, kake's instrument-receipts entry,
and `/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md`. No sibling lane repo was
written; no tool was installed (none needed).

Instrument-pin check (context for the move): at HEAD `67217e0987a2b31253d0b77f1490a1bfd031575a`
all six `tools/round-70/*.py` bytes hash equal to the `claims.json` pins, and the three
`tools/round-69` bytes equal the `loaded_by_counter` pins (`sha256sum` over the tree;
freeze `4737a542ae3b1b910d8fe43efbd572bc578b07c6`). No post-freeze instrument drift observed.

## One row per ground item

| # | Ground item | Sibling claim on the surface | Overlap verdict | This round vs province | Evidence paths |
|---|---|---|---|---|---|
| a | Provenance-bound receipt readers (a gate that binds a saved receipt to its producer instrument bytes and revision, and rejects forgeries: R70-C1) | **No sibling claims it.** kake holds the nearest primitive: `scripts/instrument_receipts.py` binds its own gate-registry instruments to committed `{sha256, bytes, selftest_mode}` receipts at a named revision (`instrument-receipts/v1`) — but kake's own boundary line says this is "evidence about the lane's own instruments, not supply-chain provenance" and records the working variants (tabi measurement-binding, chousa `digest-in-tree`, souji `TOOL_SHA256`, tameshi receipt-revision) as adjacencies that "stay with those lanes". tameshi owns the reusable verification method but "never edits a sibling's gate code" and each lane's gate remains its own; chousa owns research/citation method, not instrument receipts. | Method-adjacent, not owned: five sibling lanes hold variants of the digest-binding *primitive*; none holds the *enforcing consumer* — a reader that refuses a receipt whose `instrument.sha256` ≠ its producer's blob at the recorded revision, falsified by a ten-shape forgery battery. | Stays inside kaidoku's REA-triage province; absorbs no sibling ground. kake's distinct ground (registry-derived population) is untouched. | kaidoku `PROVINCE.md` Round-69 final disposition correction; kake `PROVINCE.md` (round-75 C2 block), `corpus/knowledge/instrument-receipts.md` §Limits; kake `PROVINCE.md` `scripts/instrument_receipts.py` cell; kotoba `corpus/knowledge/sibling-overlap-census-round74.md` (kaidoku row: class `none`, split only with revenger) |
| b | The safe packer seam — hash-before-exec, threaded packer path, child-env allowlist, typed preflight, per-run scratch (R70-C2) | **No sibling claims it.** tsukuroi owns host/package operability and *refuses* binary RE ("binary RE of drivers (→ kaidoku/revenger)"); its update-safety gate is pacman/-Syu-scoped, not packer-scoped. tameshi owns the hermetic-suite/mutation *method* (its `env-diff.py`, mutation legs; kaidoku's audit-lane pattern is one of its read-only primary surfaces) — method ownership only, never the gate. kengaku's tb2 grader sandboxes (bubblewrap, scratch HOME) are its own grading harness. | Method-adjacent only (tameshi mutation/hermetic craft behind `tools/round-70/mutation-check.py`); zero surface ownership elsewhere. | Stays inside kaidoku's province: the seam is the lane's own route tool (`tools/round-70/packed-elf.py`), repaired under the lane's own routed defects M69-9/S-1, M69-10, M69-11. | tsukuroi `PROVINCE.md` (Refuses, ADJ-06/ADJ-07 table); tameshi `PROVINCE.md` (Owns/Refuses, round-16/21 appends); kengaku `PROVINCE.md` (tb2 grader probes); claims plan R70-C2 section |
| c | Packed static executables as a REA-triage carrier class (R70-C3, kind `static-exe`) | **No sibling claims the carrier class.** kaidoku's own PROVINCE names it Frontier ("Still Frontier: … packed static binaries (no carrier measured)", round-68 and round-69 frontier notes). revenger owns shipped-artifact RE generally — the lane's one recorded open split — but refuses harness/evidence auditing and runs REA 6.8.0 on the Windows host (different substrate; no UPX-route claim); game-dev-3d uses REA only as supporting static inspection and refuses RE-as-end; tabi refuses RE forensics to kaidoku/revenger. | Absorb-within-lane: the round moves kaidoku's *own* declared Frontier note to Core through the frozen route; revenger adjacency is named and unresolved arbitration (tsukuroi ADJ-06 routes RE questions to the integrator, not to revenger directly) is not disturbed. | Stays inside kaidoku's REA-triage province; bounded (UPX-only, count-equality only — the residual Frontier wording survives). | kaidoku `PROVINCE.md` Round-68/69 frontier notes ("Still Frontier: … packed static binaries"); revenger `PROVINCE.md` (Owns + Refuses harness/evidence auditing; host/6.8.0 notes); kotoba census rows (revenger `none`, kaidoku split = revenger); tsukuroi `PROVINCE.md` ADJ-06 |

Sibling-overlap scan answer (ticket question 1): **no other lane owns this round's ground.**
The only lanes with REA/binary adjacency are revenger (the recorded open split; refuses
harness/gate auditing), game-dev-3d (supporting static inspection only), tabi and tsukuroi
(explicit refusals routing RE to kaidoku/revenger). None of the 21 siblings claims a
receipt-reader family, the packer seam, or a packed-static carrier class.

## MERGE-REPORT fit (ticket question 3)

`/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md` (read-only) stages 132
`corpus/SOURCES.md` rows (rounds 1–16: adb verb grammar, AVM/SquashFS/sasquatch, `.jsc` mapper,
evidence-graph ratio, CJK-language literature, dumpsys grammar) and 77 knowledge entries.
**No staged theme matches any of the three frozen claims**: (a) no staged row concerns
receipt producer-binding or instrument identity; (b) no staged row concerns subprocess
seams / child environments — R70-C2's grounding row (Python `subprocess` environment
contract) is opened this round per the claims plan §Frontier step, not staged; (c) no staged
row concerns UPX or packed carriers (the staged extraction rows are SquashFS/AVM-scoped).
Assimilation line for the report: **no-fit**, independently confirming `claims.json`
`frontier.assimilation: "none (frozen claims may not be widened by shokuknow material)"` and
the plan's own "Assimilation: none this round".

## Connector move (UFO-FSD role: one non-obvious synthesis)

**Evidence.** The C1 battery `tools/round-70/forged-receipts.py` materializes every instrument
it executes from git (`blob_to(root, rev|base_rev, tool, …)` at :171-175, :324) and executes the
base reader/probe/battery blobs — but its `blob_to` (:62-69) returns only a path, never a hash,
and nothing in the battery compares any executed blob's sha256 to the `claims.json`
`loaded_by_counter` pins; the battery receipt (:276-287) records `base_rev`, `base_probe_rev`
and the tool *paths*, not the base blob sha256s. Meanwhile the same round's seam probe binds
what it consumes before trusting it — `bind_producer()` (QUALITY #114, `seam-probe.py:147-166`)
refuses the measured receipt unless `instrument.sha256` equals the blob it was invoked with —
and A1/A2 hash the packer against `UPX_SHA256_PIN` before/instead of executing it. The round
therefore implements producer-binding for the receipt *readers* and the *probe*, but not for
the battery's own **before-arm inputs**: if the bytes at `--base-rev:tools/round-69/…` ever
differed from the `loaded_by_counter` pins (wrong base-rev argv, moved path, rewritten history),
the battery would still exit 0 and the before-arm "all ten shapes accepted by the base reader"
would have been measured against bytes the frozen container does not attest. The kill rules
cover a post-freeze instrument edit; they do not cover base-blob drift at run time.

**Proposed move (report-only this round; instruments are frozen).** Name this as a routed
defect candidate for the next freeze touching the C1 instrument: extend
`tools/round-70/forged-receipts.py` to hash each materialized blob (`base_reader`,
`base_probe`, `battery_blob` — and the measured-rev `reader`/`probe` for symmetry) and either
accept `--expect-base-tool-sha256` / `--expect-base-probe-sha256` / `--expect-battery-sha256`
argv (mirroring A1's pin-compare shape) or read the `loaded_by_counter` map, exiting
**2 could-not-evaluate** on mismatch, and record the executed blob sha256s in the receipt's
`battery_arms` so the landing receipt itself carries the attestation. One selftest case
("wrong base pin fails closed") follows the battery's own `wrong-world-control` pattern.

**Affected axes.** Improves **calibration** (R70-C1): the before-arm's evidentiary chain
(pinned base bytes → base acceptance → the M69-8 closure) becomes machine-checked end-to-end.
No harm to **operability** (R70-C2) or **coverage** (R70-C3): their instruments and predicates
are untouched; the seam probe's A2 already demonstrates the binding idiom, so the repair
reuses an in-round pattern rather than inventing one. It also *synthesizes across the round's
own proposals*: C1's forgery rejection and C2's A2 producer-binding are the same mechanism;
the move closes the one input side (the battery's base material) that neither currently binds.

**Risks.** (1) Any argv/exit-shape change breaks the frozen predicate's command — hence
next-freeze only; this round records it, lands nothing. (2) `loaded_by_counter` lives in
`claims.json`, outside the instrument; passing the expected hashes as argv keeps the instrument
self-contained and avoids a claims-file parser dependency (same shape as `--expect-upx`).
(3) Extra hash work is negligible (three `git show` blobs already in memory).

**Verification.** This scan verified the negative today: `grep` over the frozen battery bytes
for `loaded_by_counter|sha256` shows the only hash computation is `F3`'s `/bin/ls` forge pin
(:118-119) and `sha256_bytes` used for shape pins; no pin comparison of executed blobs; the
receipt builder (:276-287) records no base blob hashes. Pin state is clean at HEAD `67217e0`
(all nine hashes match `claims.json`), so the gap is latent, not live — the L1's landing
receipts remain valid evidence; the move hardens the *next* freeze.

## Scan VERDICT

VERDICT: met — no sibling owns any of the three ground items (a: kake/tameshi/chousa/souji/tabi
hold primitive-adjacent variants only; b: tameshi method-adjacency only, tsukuroi refuses RE;
c: kaidoku's own Frontier note, revenger split unresolved but untouched); MERGE-REPORT
assimilation = no-fit; one defect-named connector move recorded (C1 battery lacks base-blob
pin binding) with calibration-axis repair shape for the next freeze.
