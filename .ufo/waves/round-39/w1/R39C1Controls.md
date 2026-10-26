# R39-C1 pre-freeze controls — R39C1Controls

**DEFECTS FOUND** — CTL-C1-3 (six fabricated after-receipts with evidence ids re-minted by the
xpin rule) satisfies every receipt binding in drafted `P39-C1`; a receipt-only counter returns
exit 0 / 6/6 (observed), and no receipt-only check can refuse it. Nothing here judges or edits
the claim; this report feeds the freeze.

Base `a2f64e1da78afcf8cc39287106604dbcc270844c`. Artifacts:
`.ufo/waves/round-39/w1/artifacts/R39C1Controls/` (README, `CTL-C1-0..9/`,
`_harness/`, `_shared/`, `evidence/`). Reagents: REA 6.5.0 from the npx cache, unblob 26.6.4,
`sasquatch-v4be` 4.5.1. No tool was installed, upgraded or moved.

## 1. Controls

Overlays are applied on top of the base in a scratch clone. K5/K6 receipts are generated at
apply time from the freeze's own `carriers.json` / `oracle.tsv` / `symlinks.tsv`; the static
overlay holds K1–K4 `after.json` plus the exact doc blocks (`_shared/`). All doc blocks are
required for every control except C1-0 so each control isolates one receipt defect.

| control | overlay / shortcut | commit order vs freeze | counter MUST return |
|---|---|---|---|
| CTL-C1-0 | none | none; rev = freeze | exit 1, 0/6, receipts absent |
| CTL-C1-1 | K1–K4 `after.json` byte-copied from round 38; K5/K6 absent; Core row + entry + SOURCES + README | receipts commit, docs commit | exit 1, **4/6**; only `carriers_matched == 6` refuses |
| CTL-C1-2 | six receipts built from pin/oracle/symlinks with no REA, stale evidence ids kept (K1–K4 round-38 ids; K5/K6 borrow K1's) | receipts commit, docs commit | exit 1, 0/6; `evidence_id` recomputation fails on all six |
| CTL-C1-3 | same fabrication, ids re-minted with `tools/round-27/xpin-attribute.mjs` (6.5.0 rule) | receipts commit, docs commit | **exit 0, 6/6 as drafted** — no receipt-only refusal exists |
| CTL-C1-4 | C1-3 bytes; each in-tree symlink published as a regular file at the link path, its gap and `unpublished_entries` row removed | receipts commit, docs commit | exit 1; K2 (+ in-tree K5) fail gap equality; K1/K3/K4 (+ escaping K6) pass |
| CTL-C1-5 | C1-3 bytes and docs committed **in the freeze commit**; rev = freeze | in-freeze | exit 1, 0/6; `first_add != freeze` on all six |
| CTL-C1-6 | C1-3 bytes; in-tree gap kind rewritten to `missing-extractor-dependency` | receipts commit, docs commit | exit 1; K2 (+ K5) fail gap-kind equality |
| CTL-C1-7 | C1-3 bytes; escaping symlink kept as an `unpublished-entry` gap | receipts commit, docs commit | exit 1; K1 (+ escaping K6) fail gap equality |
| CTL-C1-8 | C1-3 bytes; one extra gap on a published oracle regular file | receipts commit, docs commit | exit 1, 0/6; gap-path set equality |
| CTL-C1-9 | C1-3 bytes; BE chunk present but `extraction_failed: true` | receipts commit, docs commit | exit 1, 0/6; no-failed-chunk binding |

`entry` default: `corpus/knowledge/2026-10-26-r39-sasquatch-be-squashfs-promotion.md` (stem
`2026-10-26-r39-sasquatch-be-squashfs-promotion`). SOURCES rows are appended after the
`## Registry` table with the next free ids (S118/S119 in an unfrozen tree); README row after
`## Coverage map`; PROVINCE gets `## Round-39 additions to Core` plus a frontier note whose line
contains “big-endian” and “superseded”. If the frozen counter hardcodes a different entry path,
pass `--entry` or freeze the counter with this constant.

## 2. Evidence (all scratch; no REA on K1–K4 or K5/K6)

1. **Fabrication without REA works.** `_harness/fabricate_receipts.py` builds all fields from
   the pin, oracle rows and symlink table. `xpin-attribute.mjs` on the stale-id variant:
   `none` for K1–K4 (stored `ev_400465…`/`ev_e93867…`/`ev_e31cb7…`/`ev_4348dc…` vs recomputed
   `ev_75e9a1…`/`ev_48785c…`/`ev_71b950…`/`ev_aaf9e3…`); on the re-minted variant: `both` for
   all four. Full table: `evidence/xpin-verdicts.txt`.
2. **Receipt-only probe suite** (`_harness/receipt_probe_NOT_COUNTER.py`, a reference
   implementation of the draft, not the counter; fixture freeze with six carriers, K5/K6
   metadata fixtures): results exactly as the table above — C1-0/1/2/4/5/6/7/8/9 refused with
   the stated bindings, **C1-3 green (exit 0, 6/6)**. `evidence/suite-summary.md`,
   `evidence/suite-receipts/`.
3. **Fabrication ≡ live run on the predicate fields.** Development carrier built in scratch from
   a fresh tree (`gen-squashfs.py … --endian be --comp gzip`, 442 B, sha256 `b916a13a…`) with one
   in-tree and one escaping symlink. Live REA (6.5.0, unblob 26.6.4): `squashfs_v4_be`, no failed
   chunk, both oracle files, gaps exactly `[('unpublished-entry','firmware.bin_extract/link-in')]`,
   `MaliciousSymlinkRemoved` for the escaping link. A fabricated receipt for the same carrier is
   **equal to the live run on every field P39-C1 names** (`True`), while the ids differ
   (`ev_154c5cdf…` vs `ev_c679df68…`). `evidence/live-vs-fabricated.md` and the two envelopes.
4. **Evidence ids are per-run.** Two genuine runs of the same carrier into different outdirs
   (`out-live`, `out-live2`) give identical normalized fields and different ids
   (`ev_c679df68…` vs `ev_4a6ad742…`), because `parameters.output_directory` and
   `raw_result.report[].task.path` enter the projection. Any live-run binding must compare
   `normalized_result` fields only.

## 3. Ranked by likelihood of defeating a receipt-only counter

1. **CTL-C1-3 — certain.** No receipt-only counter can refuse a correctly re-minted fabricated
   envelope; every checked field is derivable from frozen metadata.
2. **CTL-C1-5 — high.** `git merge-base --is-ancestor freeze add` is true when `add == freeze`;
   the draft's “descends from the freeze” must be frozen as *strictly* descends.
3. **CTL-C1-4 — medium.** A subset check (“every gap is on an in-tree symlink path”) accepts a
   receipt that drops a required gap and publishes the link path.
4. **CTL-C1-7 — medium.** The mirror error (“every in-tree symlink has a gap”, no extra-gap
   check) accepts a gap on an escaping path.
5. **CTL-C1-6 — medium-low.** Comparing gap paths without kinds accepts the wrong kind.
6. **CTL-C1-9 — low-medium.** Handler-membership-only checks accept a failed chunk (the
   round-38 AVM probe's shape).
7. **CTL-C1-8 — low-medium.** Gap counts without path identity accept an extra gap.
8. **CTL-C1-2 — low.** Only a counter that trusts `ev_` prefixes passes; round 38 already
   recomputed.
9. **CTL-C1-1 — very low.** Only a counter that treats an absent receipt as neutral.
10. **CTL-C1-0 — none.**

## 4. Impacted axes

- **Coverage (R39-C1):** the drafted evidence basis certifies receipt *contents*, not that
  `extract-firmware` ran. Freezing the predicate as written and scoring it with a receipt-only
  counter makes the claim killable by its own freeze control (CTL-C1-3 → 6/6). This is a
  predicate defect, not a counter implementation slip.
- **Depth (R39-C2):** unaffected (C2 reads SKILL.md and its own held-out evidence only), but
  the same class of mistake would recur if held-out "envelopes" are ever accepted without the
  generator-run binding; C2's seed/regeneration clause is the right shape.
- **Calibration:** none retired; no claim data exists yet.

## 5. Smallest safe correction

Change what is measured, not the JSON check:

1. **Counter-owned run (required).** The counter itself runs
   `REA_UNBLOB_COMMAND=… npx -y rea-agents@6.5.0 extract-firmware --format json --full-output
   <carrier> <fresh-outdir>` with `sasquatch-v4be` reachable, and scores
   handler / `extraction_failed` / oracle file set + suffix + sha256 / gap kind + path set from
   **its own** `data.normalized_result`. The committed receipt becomes an optional cross-check
   on those normalized fields; it is never the graded evidence.
2. **Never compare ids or `raw_result` across runs** (two-run evidence above).
3. **Freeze the strict readings:** `add != freeze` and `freeze` is an ancestor of `add`;
   gap set equality both directions; kind equality; no `extraction_failed` chunk.
4. Under (1), CTL-C1-3 no longer shortcuts anything: the measurement happens in the counter.
   If the freeze instead keeps the committed receipt as the graded evidence, it must add a
   provenance binding the claimant cannot synthesize (a live envelope produced under a
   counter-chosen outdir, or an independently executed witness run) — otherwise CTL-C1-3 stays
   green and the claim cannot be frozen as drafted.

Residual: K5/K6 here are metadata fixtures, not carriers; the counter's `carriers.json` must
carry a `symlinks` path per carrier and the harness must be re-pointed if the freeze uses
different oracle paths. Compare gap rows by `kind` + `relative_path` only: K1–K4's genuine
round-38 `extraction_gaps` rows carry no `link_target` (only `unpublished_entries` does), so a
whole-object comparison would refuse genuine receipts for a reason the predicate does not state.
The reference probe is not a counter and was not frozen.
