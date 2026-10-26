# R40C1Controls — pre-freeze controls for DRAFT P40-C1

**Verdict: DEFECTS FOUND** — the draft's carrier conjunction (`marker` AND `LE block lengths`) is
correct and its two carrier kill controls are the right pair, but the kill-control list misses six
attacks that reach the target, the `carriers_matched == 4` target is a count that one vendor
member plus a byte alias satisfies, the rerun clause is empty with the projection fields the
predicate names, and two doc bindings (`opened this round`, `frontier note supersedes`) are
satisfiable without moving the surface.

Seat: critic (leaf), round 40 wave 1 (pre-freeze). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`.
Nothing frozen yet; this feeds the freeze. Wrote only
`.ufo/waves/round-40/w1/R40C1Controls.md` and
`.ufo/waves/round-40/w1/artifacts/R40C1Controls/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40C1Controls` removed at exit. Read-only git in the lane; the
fixture repo lives in scratch. No tool installed or upgraded. No REA, unblob or sasquatch run on
any C1 carrier: the four REA/unblob runs below are on a fresh dev tree and a round-37 K1 copy.

## Axes (Godspeed)

| axis | what this seat moves |
|---|---|
| **coverage** | which controls the freeze must contain for the AVM-layout move to be a coverage statement rather than a count: 8 corrections, 6 of them new controls |
| **depth** | the executable rule the corpus does not hold: the AVM layout is separable from the AVM marker by **reader exit code alone** (2×2 measured), and the rerun clause is only as strong as its projection |
| **calibration** | what the scored evidence can and cannot show: the receipt does not record the extractor argv or version; `evidence_id` is not a run fingerprint; a byte-only counter returns `met_target true` on the R39-CL5 forgery |

## 1. The two carrier tests, and why both are needed

`classify-carrier.py` (40 lines, stdlib, no extractor) on four dev bodies:

| image | marker | first block len LE | BE | `sqfs-list` standard | `sqfs-list --avm` |
|---|---|---|---|---|---|
| genuine AVM-layout (round-11, `c7f74691`) | yes | **116** exact | 29696 | exit 2 | **exit 0, 4 rows** |
| that body with `mkfs_time` normalised | **no** | **116** exact | 29696 | exit 2 | exit 0, 4 rows |
| marker-only `--endian avm` body | **yes** | 13441 implausible | **236** exact | **exit 0, 3 rows** | exit 2 |
| standard `--endian be` body | no | 13441 implausible | **308** exact | exit 0, 3 rows | exit 2 |

Each half is necessary and neither is sufficient, in the two directions the draft already names:
**CTL-C1-3** (marker-only relabelled) is accepted by a marker-only test, **CTL-C1-4** (genuine body,
marker stripped) is accepted by a format-only test. The freeze must therefore contain both, and the
counter must implement both — the exit-code pair (`--avm` 0 and standard 2) is the cheapest form.

Feasibility finding for the freeze: `tools/round-39/sqfs-list.py` **cannot read a genuine AVM-BE
body at all** (exit 2, `metadata body out of bounds: offset 123 length 29696, image 4096 bytes`).
If round 40 ships that reader unchanged, every honest carrier is unmeasurable and every control is
refused for the wrong reason.

## 2. The control suite

`suite.json` (machine-readable), `ctl-lib.py` (overlay materializer), `run-controls.sh` (driver),
`build-fixture.sh` (dev fixture), `stub-counter.py` (byte-clause validator), and 11 materialized
overlay directories under `CTL-C1-*/` (the other eight controls are position-only or audit class) mirroring lane paths. Full table with overlays, commit order, required
verdicts and refusal class: `artifacts/R40C1Controls/CONTROL-SUITE.md` §2.

Commit order matters and is part of each control: a carrier/oracle overlay must land **in the
freeze** (they are frozen paths) while its receipts must land **one commit later**. `ctl-lib.py`
splits the two (`--stage freeze|tip`); without the split, CTL-C1-3/C1-4/C1-8/C1-18 fail
`receipt_descends_freeze_ok` and the carrier clause is never tested.

Measured run on the dev fixture (`control-run-dev.txt`): **17 PASS, 2 SKIP (audit class), 0 FAIL** over 19 controls,
and the clause that fires per control is exactly the designed one:

```
CTL-C1-1  subject_ok run_provenance_ok publication_ok gaps_ok evidence_id_ok
CTL-C1-2  -                    <- met_target TRUE for a byte-only counter: the point of the class
CTL-C1-3  carrier_blocklen_le_ok oracle_ok          (marker_ok stays true)
CTL-C1-4  carrier_marker_ok                          (blocklen_le_ok stays true)
CTL-C1-5  receipt_descends_freeze_ok
CTL-C1-6  failed_chunk_ok publication_ok             (gaps_ok stays true - extractor-failure is allowed)
CTL-C1-8  distinct_carriers_ok                       (every pin binding stays true)
CTL-C1-9  frozen_paths_clean                         (exit 2)
CTL-C1-14 publication_ok
CTL-C1-16 doc_control_table_frozen                   (exit 2)
CTL-C1-17 doc_sources_opened_this_round
CTL-C1-18 oracle_shape_ok oracle_ok evidence_id_ok
CTL-C1-21 doc_frontier_note doc_frontier_note_consistent
CTL-C1-22 doc_frontier_note_consistent
CTL-C1-0  everything (base); CTL-C1-N1/N2 exit 0
```

## 3. Bytes or rerun

| refusal class | controls |
|---|---|
| **committed bytes** | 0 (do-nothing), 1 (round-39 receipts), 3 (marker-only), 4 (marker stripped), 5 (receipts in the freeze), 6 (forced `-be`), 8 (aliased carriers), 9 (post-freeze swap, exit 2), 14 (wrong publication root), 16 (late control table, exit 2), 17 (reused SOURCES row), 18 (self-fulfilling oracle), 21 (no frontier note), 22 (contradicting note) |
| **rerun only** | 2 (fabricated from the oracle, ids re-minted) |
| **nothing** | 6b (toolchain laundering), 19 (a counter that computes the projection instead of running) |

Every byte-class refusal is a property of committed bytes at the scored revision: a pin, a
superblock, the first metadata header, a path prefix under this round's scratch root, a commit id, a
first-add commit, a row id absent at the freeze, an oracle row count, a note string. CTL-C1-2 is
the only required control that needs the rerun: the fabricated receipt's subject digest, handler,
publication map, gaps and `published_bytes` are all copied from the frozen oracle, and the id is
re-mintable because **`evidence_id` is not a run fingerprint** — two honest runs of one carrier
produced `ev_687d77…` and `ev_bb86a3…` (measured; `receipt-k1-dev-run{1,2}.json`).

### 3.1 The rerun projection must be fixed in the freeze, or the clause is a no-op

`projection-compare.txt`: real envelope vs the CTL-C1-2 forgery.

* draft projection (subject digest, handler, `extraction_failed`, publication map):
  **4/4 equal** — the forgery is indistinguishable, and a counter that compares "receipt projection"
  with "expected projection" computes the same value twice.
* run projection (adds `mime_type`/`analysis_depth`/`size` per file, derivations, diagnostics
  sequence, gaps, chunk ranges, `published_bytes`, `coverage`, `confidence`): **3/13 differ** for
  the same forgery.

So the freeze must fix at least the `projection.py --run` field list, **and** freeze the volatile
exclusions, or CTL-C1-N2 turns a correct tree red. Measured volatile across two honest runs:
`evidence_id`, `parameters.output_directory`, `normalized_result.output_directory`, `files[].path`,
`chunks[].provider_id`, and all of `raw_result` (REA's temp name carries randomness,
`rea-firmware-AOizkG`, and it deletes its `unblob.log` with the temp dir).

Even then, the clause is a **product** bar, not an authentication bar: every projection field is a
function of the carrier bytes and the pinned toolchain, so a forger who implements the AVM reader
and sasquatch's publication rules reproduces the projection — and at that point the claim's product
statement is true. R39-CL5 closes as "a fabricated receipt cannot reach the target unless the
claimed extraction really happens", which is the right bar; it does not close as "the receipt is
proven to have been produced by a run", and the claim text should stop implying it does.

### 3.2 The extractor argv is not in the evidence

`'sasquatch' in envelope == False`, `'extract command' in envelope.lower() == False`; REA runs
unblob with `--log <tmp>/unblob.log` and removes the temp dir. The draft's "runs
`sasquatch-v4be` **without** `-be` when the marker holds" is therefore inferred from the outcome,
never observed. Two options: state it as mechanism (S112) and score the outcome, or have the
counter run one `unblob -v` on the carrier in its own scratch and read the `Running extract
command` line from the `unblob.log` unblob writes into the cwd (measured on a dev tree). Without
one of them, **CTL-C1-6b (laundering: an honest receipt from a run under a different
`sasquatch-v4be` on PATH) cannot be refused by any control** and must be disclosed.

## 4. Defects in the draft, smallest safe correction each

1. **`carriers_matched == 4` counts ids** (CTL-C1-8). `L1 := V1 bytes`, `L2 := V2 bytes`, spec pins
   and provenance rewritten consistently → all four pins are true, only two distinct carriers exist,
   and a count target is met. **Add `distinct_carriers_ok`:** four distinct pins, and V2's
   provenance names a different vendor URL and image sha than V1's.
2. **"same relative-path suffix"** (CTL-C1-14) accepts publication under any root. Require the exact
   `<extract_root>/<relpath>` for the single root recorded per carrier in the frozen spec, and a
   published count equal to oracle rows plus recorded extras.
3. **"a SOURCES row opened this round"** (CTL-C1-17) cannot be a date: every round in this lane is
   `2026-10-26`, and the round-39 counter tested exactly that string. Define it as a diff property:
   the row **id** does not exist in `SOURCES.md` at the freeze and is added in `FREEZE..REV`. (A
   `+`-line diff alone is not enough either — re-adding a used-by to an old row produces one.)
4. **"a frontier note supersedes the AVM part"** (CTL-C1-21/22) needs content: the note names the
   entry stem and the `## Round-40 additions to Core` heading and contains no stay-Frontier
   assertion about AVM. Presence is not supersession.
5. **Oracle completeness is assumed** (CTL-C1-18). Trim the oracle to the rows a partial extraction
   published and every clause agrees. Cheapest sound clause: the counter re-derives the oracle from
   the frozen carrier with the frozen reader (it runs it for the endianness test anyway) and
   requires set equality, plus `rows > 0` per carrier.
6. **`extraction_failed` alone does not catch a wrong-endian run with an empty oracle** (CTL-C1-6):
   make `publication_ok` non-vacuous (`len(oracle) > 0`, `len(published) > 0`).
7. **R39-CL4 is half-carried**: the draft freezes the control tables, but CTL-C1-16 shows the
   counter must also **exit 2** when `controls.json` is unreachable at the freeze commit, and the
   format validation must live in that commit.
8. **Freeze the rerun projection fields and their volatile exclusions** (§3.1) — otherwise the one
   control the draft designed for R39-CL5 passes.

## 5. What this seat did not do

* No REA, unblob or sasquatch on any carrier; the rerun clause is analysed, not executed, because it
  needs the frozen carriers. Its mechanism is measured with two honest REA runs of a dev carrier
  plus the projection comparison, and the suite reports `rerun_projection_ok: null` for that reason
  (CTL-C1-2's `expected_byte_only` records the measured byte-only verdict).
* The suite is validated on a **dev fixture** (`build-fixture.sh`: base → freeze → tip, four distinct
  AVM-layout carriers, synthesized receipts, byte-clause counter). The freeze must re-run
  `run-controls.sh` against the real tree and paste the 19 lines into the score receipt; the
  overlays under `CTL-C1-*/` are already materialized and `ctl-lib.py` regenerates them if the
  skeleton's path names differ.
* CI/cost: the whole suite is 6.9 s of wall clock and needs no network.

Evidence: `artifacts/R40C1Controls/{CONTROL-SUITE.md, suite.json, measurements.txt,
control-run-dev.txt, control-results-dev.json, projection-compare.txt, oracle-mode-matrix.txt,
classify-dev.tsv, receipt-k1-dev-run1.json, receipt-k1-dev-run2.json, receipt-markeronly-dev.json}`.
