# Round 40 — genuine AVM-layout BE SquashFS measured but not promoted (counter suffix false negative); triage table v2 with a domain guard and scored actions reaches 26/26 on a freeze-seeded held-out set

Base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`. Freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`
(`plans/round-40-claims.md`, all round-40 tools, C1 carriers/oracles/gap rule, SKILL rule block 19 and its
entry, S123, C2 controls, wave-1 evidence). Controls `45e89864e967d7501110b529cb8517b26b92c7ef`. Data: C2
held-out `2d1ac5bcd08f6828dbfdee9054bbeec0ea211b33`, C1 receipts `73c7bf9c73bd7b4891c4e46c93d1d29c287e4541`.
Landing `42c10a58cb2cae3a4a0122af35a0cf95ac718043` (measured revision); scores `c17565bc`; honest-stop
record `4d62ee5a`. L1 `KaidokuR40`. Wave 1: 42 seats (`.ufo/waves/round-40/w1/`); wave 2: 38 seats
(`.ufo/waves/round-40/w2/`).

Author verdicts (closure pending):

- **R40-C1 not met — honest stop.** `tools/round-40/c1-counter.py` at `42c10a58`: `carriers_matched 3`
  of 4, exit 1 (`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`). V1, V2 (the two vendor AVM members)
  and L1 match every clause including the rerun projection; L2 fails only `nonregular_unpublished_ok`,
  whose path-suffix test reads the published regular file `usr/bin/busy` as the symlink `bin/busy`. The
  supplementary gate `c1-extra.py` is met (exit 0). Wave 2 reproduced 3/4 with zero divergence
  (`w2/R40W2C1Rescore.md`), reproduced every receipt independently (`w2/R40W2ReproV1.md`, `ReproV2.md`,
  `ReproL.md`), confirmed the oracle on all four carriers (`w2/R40W2C1Oracle.md`) and showed the frozen
  carrier set makes the target unsatisfiable under this counter (`w2/R40W2C1Fabricate.md` Defect B,
  `w2/R40W2Sentinel.md` F1): the stop was entailed at the freeze, not discovered by data. A sandbox
  counter with exact extract-root matching scores 4/4 on the same receipts (`w2/R40W2C1Refreeze.md`) —
  round-41 evidence, not this claim. The Core row was demoted to a measured-not-promoted record at
  `4d62ee5a`.
- **R40-C2 met.** `tools/round-40/c2-counter.py` at `42c10a58`: `matched 26` of `n 26`, every binding true,
  `distinct_decisions 12`, exit 0 (`.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`). Before: exit 2
  `no_manifest_at_rev` at the freeze; the base SKILL has no v2 table (CTL-C2-0 exit 2); the best control
  reached 24/26 and the transcribed v1 table 18/26 on the development envelopes
  (`.ufo/waves/round-40/controls/c2-dev-scores.json`). Wave 2 reproduced 26/26, regenerated the carriers
  byte-identically from the seed, re-ran REA on all 26 and labelled them with an independent evaluator
  (`w2/R40W2C2Rescore.md`, `RegenA.md`, `RegenB.md`, `IndepEval.md`).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M40-1 | one path helper used across two path domains: the frozen C1 counter's `nonregular_unpublished_ok` promises path equality but tests a suffix, and the L1's own lane-built carrier put a regular file `usr/bin/busy` under a symlink path `bin/busy` | `tools/round-40/c1-counter.py` `same_rel` (`candidate.endswith('/' + rel)`); `tools/round-40/mk-l-carriers.py` L2 tree; score `l1/scores/c1-at-42c10a58.json` (L2 `nonregular_published ["firmware.bin_extract/usr/bin/busy"]`) | none (the counter's 70 selftest cases had no nested-name collision; the C1 counter was never dry-run on carriers of the frozen shape before the freeze) | QUALITY 83; `w2/artifacts/R40W2MistakeHunt/mh1-suffix-domain.py`: frozen matcher on L2 → exit 1 (1 hit), exact extract-root matcher → exit 0; `w2/R40W2C1Refreeze.md`: patched counter with both-direction selftest cases scores 4/4 in a sandbox |
| M40-2 | a carrier pick is not a reservation: the scout's V2 pick (7430 07.31) was used as a REA development input by a sibling recon seat whose exclusion named only V1 | `w1/R40C1VendorScout.md:39`; `w1/artifacts/R40C1ReconGaps/env-7430-member-d1.json.gz` (subject `b919a6a2…`); replaced at the freeze by 6820v1 (`plans/round-40-claims.md` `## Changes from the draft`) | the L1 at freeze assembly | `w2/artifacts/R40W2MistakeHunt/mh2-candidate-reservation.py`: draft-7430 → fatal 1, frozen carriers.json → fatal 0; next round: the wave context lists every candidate as reserved before recon picks inputs |
| M40-3 | three wave-1 reports landed under `artifacts/` instead of `w1/<seat>.md`; the L1 copied them, so each exists twice and one carries seat id `R40ConnSibling-2` | `w1/R40SrcAvmVendor.md` ≡ `w1/artifacts/R40SrcAvmVendor.md`, same for `R40SrcReaOps`, `R40ConnSibling` (`artifacts/R40ConnSibling-2/`) | `w1/R40Sentinel.md` §2.5 (partly) | `w2/artifacts/R40W2MistakeHunt/mh3-report-placement.py`: 6 findings on the lane, 0 on the repaired fixture, 1 when a report is deleted; the `w1/` copies are authoritative (named in the report) |
| M40-4 | restricted vendor bytes in the lane tree: the V1 carve (5.4 MB) in a wave-1 artifact (removed before the freeze), and seven AVM package/download-page texts (47 B–111 KB) committed in the freeze | `w1/artifacts/R40C1VendorV1/carrier-v1-be.sqsh.REMOVED-by-L1.sha256`; `w2/R40W2C1Chain.md` D1; `.ufo/waves/round-40/w1/vendor-files-removed.sha256` | a sentinel size survey (carve); `w2/R40W2C1Chain.md` (texts) | texts removed from the tree in the round's last commit (they stay in history at `7fce3086`; no firmware body or extracted file was ever committed: `w2/R40W2C1Chain.md` blob scan); `w2/artifacts/R40W2MistakeHunt/mh5-vendor-bytes.py` pin-keyed scan red on a planted copy, green on the tree |
| M40-5 | a recipe trusted from recon failed on a fresh seed: the C2 partial-body recipe extracted clean on one xz replicate, and the C2 counter refused the row-less out-of-domain pair | L1 sandbox dry run 1 (freeze-like commit `df4fef39` in scratch): 25/26, `arms_valid`/`decisions_reported`/`row_decisions_consistent` false; dry run 2 (`c6ec5a28`): 26/26, exit 0 (`plans/round-40-claims.md` `## Changes from the draft`) | the L1 dry run (new practice, QUALITY 83) | gzip pin + `NOMATCH_PAIR` in the freeze. Wave 2 refines the cause: the determinant is the zeroed block's compressed length, not the compressor (`w2/R40W2MistakeHunt.md` MH-4) — routed R40-CL4 |

## Gate

### Sources opened this round (2026-10-26)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S123 | https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | 2026-10-26 (`w1/R40SrcReaOps.md`); re-opened `w2/R40W2SrcReopen.md` | `const engineName = request.operation === "inspect_firmware_regions" ? "binwalk" : "unblob";` (`package/dist/firmware/FirmwareProvider.js:141`) |
| S124 | https://raw.githubusercontent.com/Freetz-NG/freetz-ng/9a7236926bffaa6af16f84b3db27017cb5f02724/make/host-tools/squashfs4-be-host/patches/350-unsquashfs__AVM_BE.patch | 2026-10-26T18:25Z (`w1/R40SrcFreetz.md`) | "/* block length in AVM-BE format is stored in LE order */" (patch line 35) |
| S125 | https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/ | 2026-10-26T18:18Z (`w1/R40SrcAvmVendor.md`) | "Product: FRITZ!Box 6490 Cable" / "Version: FRITZ!OS 7.57" (`info_en.txt` lines 8, 10) |
| S126 | /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv | 2026-10-26 (`w1/R40AssimE3.md`) | "absent - the AVM branch passes no -be" (row `unblob_be_flag`, line 17) |

Registry 122 → 126 rows; S123 in the freeze, S124–S126 at the landing; all tier A, `mined`. S126's recheck
prose ("`sha256sum …/avm-be.squashfs` -> `c7f74691…` (ran 2026-10-26)") was stripped to `180d`; the
retained log has no exit status, so a recheck must never read it as "exit 0". Wave 2 found the rows
byte-true but five `teaches`/`anchor` cells overclaim (`w2/R40W2SrcReopen.md`); the registry is
append-only, so those notes stand here: S123's `teaches` overstates which operations carry gaps; S125 is
identity only, never a layout statement.

`used-by` changes (old → new, only that cell): S112 `r38…, r39-sqfs-outcome-triage` → `+ r40-avm-be-squashfs-core,
r40-sqfs-triage-v2`; S114 `r38…` → `+ r40-avm-be-squashfs-core`; S118, S119, S120 `r39-sqfs-outcome-triage` →
`+ r40-sqfs-triage-v2`; S121 `r39-sqfs-outcome-triage` → `+ r40-avm-be-squashfs-core` (all `corpus/knowledge/2026-10-26-*.md`).

Rejected candidates: the Freetz seat's row carried a C expression with a literal `|` (rewritten "bitwise
OR" so the row parses as 11 columns); the assimilation seat's Freetz `AVM-BE-format.txt` row duplicated
S114's URL (not appended; S114 cited instead) and its `freetz-squashfs4-host-be.mk` row is cited by no
admitted text (not appended, CORPUS rule 4).

### Assimilation

Theme: AVM (`/home/vgpnk/Projects/shokuknow/merge/kaidoku`). **Admit 1:** `avm-image-extraction` →
re-grounded into `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` (`**Lineage (assimilated)**`
paragraph, own-work row S126): every cited source re-opened 2026-10-26 by `w1/R40AssimE3.md`, image sha256
`c7f74691…`, the layout identity re-measured (`121 + 2 + 116 = 239`). The round-39 flip condition ("one
entry re-grounded on lane receipts against a real AVM image") is met by the round-40 vendor receipts.
**Reject:** `avm-firmware-image-unblob` (headline "the AVM marker is invisible to unblob" falsified by the
pinned handler `is_avm = header.bytes_used == header.mkfs_time`; flip: a rewrite retracting the headline);
`avm-le-variant-reachability` (overturned by its own package's `avm-le-image-genuine-marker` without a
reversal pointer; flip: a reversal line); `avm-image-build-blocker` (stale premise); `sasquatch-unblob-avm-branch`
(stale open lead, unpinned `unblob/main`); `avm-le-image-genuine-marker` deferred (LE scope; admissible in an
LE-AVM round after its `:30`/`:55-56` corrections) — `w1/R40AssimReject.md`, `w1/artifacts/R40AssimE3/gate.md`.
Id-collision check: `w1/artifacts/R40AssimE3/collision/` — `reg-ids` 122, `staged-ids` 132, `collisions`
17 (S106–S122); the guard is proven on an indented fixture (0–3-space pattern catches `  | S002`, column-zero
pattern is a false green). Renumber by document: staged S200 (`lead1-avm-image.tsv`) → lane S126. Quarantine
slice: 5 rows, sha256 `7383a90e…28e6a`, byte-identical to rounds 38/39; verdicts `w1/R40Quarantine.md`
(S150 re-anchor, S113/S136/S147 adopt-with-anchor, S117 flips unverifiable → adopt-with-anchor); nothing
from the slice is appended this round. Wave-2 spot-check: `w2/R40W2Assim.md`.

## Round-39 spot-check disposition (`corpus/lessons/round-39-verifier-spotcheck.md` §5)

| id | state | where |
|---|---|---|
| R39-CL1 | fixed | SKILL rule block 19 domain columns; out-of-domain held-out class (`inspect_firmware_regions`/`binwalk`) → `unclassified` in 2/2; the round-40 instrument registry notes `tools/round-39/sqfs-triage.py` has no guard |
| R39-CL2 | fixed | `mixed-symlinks` row ahead of the escaping row; held-out H11/H12; block-18 supersession sentence |
| R39-CL3 | fixed | `partial-body-failure`, `clean-empty` rows; scored action column; `distinct_decisions 12` |
| R39-CL4 | fixed | control tables, their dev inputs and dev scores first added in the freeze `7fce3086` (`w2/R40W2ConnRouted.md`) |
| R39-CL5 | partly | the C1 counter reruns REA and compares the `plus-extractor` projection; wave 2 built an oracle-only fabrication that passes every L1 clause (`w2/R40W2C1Fabricate.md`): the rerun proves carrier→oracle consistency through the pinned toolchain, not receipt provenance. Disclosed in the claims; routed R40-CL2 |
| R39-CL6 | partly → fixed for scores | every round-40 score receipt carries `exit_code` (`tools/round-40/score-receipt.sh`); seat status filled by `tools/round-40/ledger-status.py` (`.ufo/waves/round-40/r40-w{1,2}-status.json`); the report carries a cross-domain line |
| R36-CL5 | open | per-row state in `w2/R40W2ConnRouted.md` (QUALITY 33/45/60 partial, 39/68 not met, 58 n/a) |
| r39 `heldout-gen.py` docstring erratum | open (frozen bytes) | v2 generator has no version-minor class |
| r39 surviving mutants | carried | round-40 tools have their own mutation reports: `w2/R40W2C1Mutants.md`, `R40W2C2InterpMutants.md`, `R40W2C2CounterMutants.md` |

## Routed defects into round 41

| id | defect | evidence |
|---|---|---|
| R40-CL1 | C1 counter suffix matching (`same_rel`) — refreeze with exact extract-root matching and both-direction selftest cases; the round-40 receipts stay valid | `w2/R40W2C1SuffixAudit.md`, `w2/R40W2C1Refreeze.md` |
| R40-CL2 | rerun binding proves carrier consistency, not receipt provenance; an oracle-only fabrication passes | `w2/R40W2C1Fabricate.md` |
| R40-CL3 | C2 freeze integrity: the counter does not block on a touched `tools/round-39/gen-squashfs.py` and does not enforce "restore does not un-block" for the SKILL v2 block | `w2/R40W2Sentinel.md` F2/F3 |
| R40-CL4 | the partial-body recipe's determinant is the zeroed block's compressed length; pin it in the generator, not the compressor | `w2/R40W2MistakeHunt.md` MH-4 |
| R40-CL5 | table v2 prose: the interpreter's embedded selftest table still carries the pre-rewrite AVM-marker cause; `avm-marker-be-dropped` action vs its cause's damage branch; `body-extractor-failure` cause; `escaping-symlink-removed` absorbs combined gap sets; `dependencies` never decides | `w2/R40W2C2TableReview.md`, `w2/R40W2C2AxisFit.md` |
| R40-CL6 | `fetch-vendor.py` does not compare the pinned `member_sha256` | `w2/R40W2C1Chain.md` D2 |
| R40-CL7 | the vendor terms also purport to forbid analysis; the round publishes derived metadata only (paths, sizes, digests) — operator to rule (no L0 question filed: the operator directed RE training on public firmware) | `w2/R40W2C1Chain.md` D1-b |

## Criteria added

- QUALITY 83 (M40-1, M40-5).

## Wave 2 (38 seats, after the landing)

Neither author verdict was overturned: C1 3/4 reproduces exactly and C2 26/26 reproduces under
independent re-runs, regeneration and an independent evaluator. Wave 2's contested points: R40-C2's depth
increment is bounded — 18 of 26 envelopes were already decided by the v1 table and the expected labels come
from the same class map the table was written to (`w2/R40W2C2AxisFit.md`, `w2/R40W2C2Shortcut.md`); several
v2 cause cells overreach (R40-CL5). Mutation sweeps: `w2/R40W2C1Mutants.md`, `w2/R40W2C2InterpMutants.md`,
`w2/R40W2C2CounterMutants.md` (5 of 19 counter mutants survive, none turns tampered data into a false MET).
