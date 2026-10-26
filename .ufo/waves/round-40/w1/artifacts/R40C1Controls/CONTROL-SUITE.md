# P40-C1 pre-freeze control suite — design, overlays, required verdicts

Seat: `R40C1Controls` (critic, leaf). Draft under attack: `plans/round-40-claims.md` R40-C1
(base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`). Nothing here is claimed to be scored; the
control *inputs* and the rule that built them are the deliverable, and the L1 commits them in
the freeze (`routed R39-CL4`).

**Verdict in one line:** the draft's conjunction of carrier clauses is right and its kill-control
list is too short — 6 of the 14 must-refuse controls below are not in it, and one of the listed
controls (`CTL-C1-2`) is refused by the rerun only if the rerun projection contains fields the
frozen evidence cannot produce; with the projection as the draft's own predicate names it, the
fabrication is invisible (measured).

---

## 0. How a control is built and scored

Every control is a **file overlay applied to a throwaway clone**, never to the lane:

```
python3 -I -B ctl-lib.py --control CTL-C1-x --root $D --spec $SPEC --stage freeze|tip|all
```

`$D` is a `git clone --shared` of the honest round-40 tree. `suite.json` fixes, per control:
`commit_stage`, `overlay`, `commit_order`, `expected` (exit code, `met_target`, `must_fail`,
`must_pass`), `refusal_class` (`bytes` | `rerun` | `audit`), and, for CTL-C1-2,
`expected_byte_only` — the verdict a counter without the rerun clause must produce, which the
driver accepts only when the counter reports `rerun_projection_ok: null`.

`run-controls.sh` implements the three commit shapes the controls need:

| stage | commits built in the clone | scored |
|---|---|---|
| `base` | `git checkout <base>` | base (CTL-C1-0) |
| `pre-freeze` / `in-freeze` | base → **synthetic freeze** = honest freeze tree + overlay freeze side → honest tip + overlay tip side | the tip, against the synthetic freeze OID |
| `post-freeze` | honest tip + one overlay commit | the overlay commit, against the honest freeze OID |

The freeze side / tip side split (`ctl-lib.py:FREEZE_SIDE`) is what keeps a control honest: a
carrier or oracle is a *frozen* path, so its overlay must land in the freeze, while the receipt
must land one commit later or `receipt_descends_freeze_ok` fires and the control would be refused
for the wrong reason — hiding whether the carrier clause works.

Overlay directories are shipped as **materialized files at lane paths**
`<control>/<lane path>` (e.g. `CTL-C1-3/corpus/evidence/round-40/c1/V1/carrier.sqsh`), regenerated
from `ctl-lib.py --stage all` on a dev skeleton; `ctl-lib.py` is the authority for a renamed
skeleton.

## 1. The two carrier-side tests, measured (cheapest part of the suite)

`classify-carrier.py` decodes only superblock fields and the first metadata block header. It costs
~40 lines of stdlib and no extractor.

| image | marker `mkfs_time==bytes_used` | first block length LE | BE |
|---|---|---|---|
| genuine AVM-layout (round-11 retained, sha `c7f74691`) | **yes** | **116** (exact: 121+2+116=239) | 29696 (implausible) |
| genuine AVM-layout, marker stripped (CTL-C1-4 body) | **no** | **116** (exact) | 29696 |
| marker-only standard-BE (`gen-squashfs --endian avm`, CTL-C1-3 body) | **yes** | 13441 (implausible for a 599-byte image) | **308** (exact) |
| standard-BE (`--endian be`) | no | 13441 (implausible) | **308** (exact) |

The sharpest form is an **exit-code** test with the frozen reader itself (`oracle-mode-matrix.txt`):

| image | `sqfs-list.py` (standard) | `sqfs-list.py --avm` |
|---|---|---|
| genuine AVM-layout | exit 2, 0 rows | exit 0, 4 rows |
| genuine AVM-layout, marker stripped | exit 2, 0 rows | exit 0, 4 rows |
| marker-only standard-BE | exit 0, 3 rows | exit 2, 0 rows |
| standard-BE | exit 0, 3 rows | exit 2, 0 rows |

So `--avm` exit 0 **and** standard exit 2 is a two-line, extractor-free proof that the block
lengths are LE; the marker is one more 4-byte compare. The two tests are each necessary and
neither sufficient — that is exactly what CTL-C1-3 and CTL-C1-4 force.

Consequence for the freeze (feasibility, measured): `tools/round-39/sqfs-list.py` **cannot** read
a genuine AVM-BE body at all — it exits 2 with `metadata body out of bounds: offset 123 length
29696, image 4096 bytes`, because it takes the metadata length endianness from the magic. R40's
oracle must therefore be a *new* AVM mode; if the freeze ships the round-39 reader unchanged, no
honest carrier is measurable and every control below would be refused for the wrong reason.

## 2. Control table

`refusal` = the cheapest mechanism that must refuse it: **bytes** (committed bytes at the scored
revision), **rerun** (only the counter's own fresh run), **audit** (nothing can refuse it; only
re-executing the counter constrains it).

| id | overlay (files at lane paths) | commit order | required verdict | refusal |
|---|---|---|---|---|
| **CTL-C1-0** do-nothing | none | score base | exit 1, `met_target false`, `carriers_matched 0`, doc + carrier bindings false | bytes |
| **CTL-C1-1** round-39 receipts copied | 4× `corpus/evidence/round-40/c1/<ID>/after.json` = verbatim `corpus/evidence/round-39/c1/K1..K4/after.json` | one commit after freeze; docs honest | exit 1; `subject_ok`, `run_provenance_ok` (`/kaidoku-r39/`), `publication_ok`, `gaps_ok` false | bytes |
| **CTL-C1-2** fabricated from the oracle, ids re-minted | 4× `after.json` built from `oracle.tsv`+`symlinks.tsv` (publication map, `extraction_failed false`, gap per in-tree link, `published_bytes` = Σ sizes) with a self-consistent id | one commit after freeze; carriers/docs untouched | **full counter:** exit 1, only `rerun_projection_ok` false. **Byte-only counter:** exit 0, `met_target true` — measured, and that is the point | rerun |
| **CTL-C1-3** marker-only body relabelled | 4× `carrier.sqsh` = `gen-squashfs.py --endian avm` (+n pad bytes), `oracle.tsv` from the standard reader, spec pin/size/rows made consistent, receipts claiming success | carriers/oracles/spec **in the freeze**, receipts one commit later | exit 1; `carrier_blocklen_le_ok` **and** `oracle_ok` false; `carrier_marker_ok` true (so a marker-only counter passes it) | bytes |
| **CTL-C1-4** genuine body, marker stripped | 4× `carrier.sqsh` = AVM-layout body with bytes 8..12 = 1700000000, spec consistent, receipts synthesized | as C1-3 | exit 1; `carrier_marker_ok` false; `carrier_blocklen_le_ok` true (so a format-only counter passes it) | bytes |
| **CTL-C1-5** receipts in the freeze | the C1-2 receipt set, placed in the freeze tree | freeze commit = honest freeze + receipts; tip restores honest tip | exit 1; `receipt_descends_freeze_ok` false | bytes |
| **CTL-C1-6** PATH wrapper forces `-be` | `.ctl-bin/sasquatch-v4be` = `exec … -be "$@"`; receipts = the shape that run really produces (`extraction_failed true`, 0 files, one `extractor-failure` gap) | one commit after freeze | exit 1; `failed_chunk_ok` **and** `publication_ok` false, `gaps_ok` **true** (`extractor-failure` is an allowed gap kind) | bytes |
| **CTL-C1-8** four ids, two distinct bodies | `L1/carrier.sqsh` := `V1` bytes, `L2` := `V2`, spec pin/size/oracle/provenance rewritten to stay **consistent**, receipts re-pinned | **in the freeze** | exit 1; `distinct_carriers_ok` false; every pin binding true — a count target `== 4` is met while the claim has two carriers | bytes |
| **CTL-C1-9** post-freeze carrier/oracle swap | C1-3's freeze side **applied one commit after the freeze** | honest freeze, then swap commit | exit **2**, `frozen_path_changed`, `frozen_paths_clean` false | bytes |
| **CTL-C1-14** suffix-matched publication | receipts' `relative_path` prefixed `nested/wrong-root/`; every oracle row still matches by suffix | one commit after freeze | exit 1; `publication_ok` false (an exact `<extract_root>/<rel>` match is required) | bytes |
| **CTL-C1-16** control table lands late | `controls.json` removed from the freeze, restored one commit later | freeze rewritten without the table | exit **2**, `control_table_not_frozen` (R39-CL4) | bytes |
| **CTL-C1-17** cites round-39 SOURCES rows | the round-40 row deleted, an `S112` row re-added citing the entry, entry cites S112/S122 (all `2026-10-26`) | one commit after freeze | exit 1; `doc_sources_opened_this_round` false — "opened this round" must mean **the row id does not exist at the freeze**, not "a `+` line appeared" and not "date == today" | bytes |
| **CTL-C1-18** self-fulfilling oracle | oracle trimmed to 3 of 4 rows, receipt publishes those 3 (a partial extraction with an oracle written from it) | oracle **in the freeze**, receipts later | exit 1; `oracle_shape_ok`, `oracle_ok`, `evidence_id_ok` false | bytes |
| **CTL-C1-21** no frontier note | `PROVINCE.md` with the deploy row and entry but no `Round-40 frontier note` | one commit after freeze | exit 1; `doc_frontier_note` false | bytes |
| **CTL-C1-22** frontier note contradicts | note text = "the AVM part … stays Frontier" | one commit after freeze | exit 1; `doc_frontier_note_consistent` false — note presence is not supersession | bytes |
| **CTL-C1-N1** anti-control | none | score honest tip | exit 0, `met_target true`, `carriers_matched 4` | none |
| **CTL-C1-N2** anti-control, volatility | none; scored twice under different `TMPDIR` | honest tip | both runs identical `bindings` + `carriers_matched`; exit 0 | none |
| **CTL-C1-6b** toolchain laundering | none materializable | n/a | **cannot be refused**: the envelope holds no `sasquatch` string and REA deletes its `--log` temp (`receipt-k1-dev-run1.json`; REA args measured) | audit |
| **CTL-C1-19** counter computes instead of running | n/a (counter-side) | n/a | **cannot be refused**: the expected projection is a function of the frozen bytes (measured: draft projection 4/4 equal) | audit |

`suite.json` carries the same rows machine-readably with the binding names; `run-controls.sh`
compares and prints one line per control.

## 3. Measured suite run (dev fixture, byte clauses only)

`control-run-dev.txt`: **17 PASS, 2 SKIP (audit class), 0 FAIL** over 19 controls on a fixture repo built by
`build-fixture.sh` (three commits: base → freeze → tip; four distinct AVM-layout carriers; the
honest receipts synthesized). This is a *shape* run: the fixture is not the claim, and the counter
is `stub-counter.py`, which implements the byte clauses and reports `rerun_projection_ok: null`.

Clauses that actually fired, per control (the column that matters):

```
CTL-C1-0  everything (base)
CTL-C1-1  subject_ok run_provenance_ok publication_ok gaps_ok evidence_id_ok
CTL-C1-2  -                                   <- met_target true: byte counters cannot refuse it
CTL-C1-3  carrier_blocklen_le_ok oracle_ok
CTL-C1-4  carrier_marker_ok
CTL-C1-5  receipt_descends_freeze_ok
CTL-C1-6  failed_chunk_ok publication_ok
CTL-C1-8  distinct_carriers_ok
CTL-C1-9  frozen_paths_clean (+ carrier facts)
CTL-C1-14 publication_ok
CTL-C1-16 doc_control_table_frozen
CTL-C1-17 doc_sources_opened_this_round
CTL-C1-18 oracle_shape_ok oracle_ok evidence_id_ok
CTL-C1-21 doc_frontier_note doc_frontier_note_consistent
CTL-C1-22 doc_frontier_note_consistent
CTL-C1-N1/N2 -
```

Two rows are worth reading twice:

* **C1-3 fires two clauses on one physical fact** (`carrier_blocklen_le_ok` and `oracle_ok`): a
  marker-only body is unreadable by the frozen AVM-mode reader, so a counter that skips the
  block-length decode is still refused by the oracle re-derivation. Good redundancy, not a
  duplicate authority — both read the same bytes, neither defers to the other.
* **C1-6 leaves `gaps_ok` true.** An `extractor-failure` gap is an *allowed* gap kind; the control
  is refused by the failed chunk and the empty publication. A counter that asserts "gaps are
  allowed kinds" alone would pass a `-be` run on a clean AVM carrier whose oracle is empty — which
  is why `publication_ok` must require `len(published) > 0` **and** `len(oracle rows) > 0`.

## 4. Which controls need the rerun

| refusal class | controls | why |
|---|---|---|
| **bytes** | 0, 1, 3, 4, 5, 6, 8, 9, 14, 16, 17, 18, 21, 22 | each leaves a committed-bytes trace: a pin, a superblock, the first block header, a path prefix under a known scratch root, a commit id, a table's first-add commit, a row id absent at the freeze, an oracle row count, a note string |
| **rerun** | 2 | every field a byte check reads is made true by construction; the id re-mint is consistent (ids are run-volatile: two honest runs of one carrier gave `ev_687d77…` and `ev_bb86a3…`) |
| **audit** | 6b, 19 | the envelope records no extractor identity, and the expected projection is computable from the frozen evidence |

### 4.1 The rerun projection is load-bearing, and the draft's projection is empty

Measured (`projection-compare.txt`), real REA envelope of a dev carrier vs the best receipt a
holder of the committed TSVs can write:

* draft projection (subject digest, handler, `extraction_failed`, publication map):
  **4/4 fields equal** — the fabrication is *indistinguishable*. A counter that implements the
  rerun as "compare the committed receipt's projection with the expected projection" computes the
  same value twice and closes nothing.
* run projection (adds per-file `mime_type`/`analysis_depth`/`size`, the derivations table, the
  diagnostics sequence, the gap list, chunk ranges, `published_bytes`, `coverage`, `confidence`):
  **3/13 fields differ** for the same forgery — `files` (`mime_type` is not a function of a sha256),
  `derivations`, `chunks`.

So the freeze must fix the projection to at least the `--run` set in `projection.py`, and must
normalize the run-volatile fields, else `CTL-C1-N2` fails (a correct tree refused). Volatile,
measured across two honest runs: `evidence_id`, `parameters.output_directory`,
`normalized_result.output_directory`, `files[].path`, `chunks[].provider_id`, the whole
`raw_result` (REA's temp dir name carries randomness, e.g. `rea-firmware-AOizkG`, and its
`unblob.log` is deleted with the temp dir).

### 4.2 What the rerun clause can and cannot do

Every projection field is a function of (carrier bytes + frozen toolchain). Therefore the rerun
binding does not authenticate *provenance*; it converts the claim from "this receipt was produced
by a run" into "a run now exists, and the receipt agrees with it". Two consequences the claim text
should state:

* `CTL-C1-2` is refused only while the forgery is *cheap* (built from the TSVs). A forger who also
  implements the AVM reader and sasquatch's publication rules reproduces the projection — and at
  that point the product statement ("the layout extracts to these files") is true, so the coverage
  move is justified even though the provenance is false. `R39-CL5` is closed as a *product* bar,
  not as an authentication bar.
* `CTL-C1-19` is the residual: the counter is the trust root. The score receipt must therefore
  embed the fresh envelope's sha256, the `mkdtemp` nonce it chose, and the child REA argv, and the
  L1 must re-execute the counter once. No control over committed bytes can reach this.

### 4.3 The extractor argv is not in the evidence

`raw_result.execution.stdout.text` carries the unblob banner and summary only; `'sasquatch' in
envelope == False` and `'extract command' in envelope.lower() == False` (measured on a real
envelope). REA passes `--log <tmp>/unblob.log` and deletes the temp dir. Therefore the draft's
sentence "unblob 26.6.4 `squashfs_v4_be` handler choosing `sasquatch-v4be` without `-be`" is
*inferred from the outcome*, never observed in the evidence. Cheapest fixes, in order:

1. state it as a mechanism (S112) and score the outcome (files published), which is what the
   publication clause already does; or
2. have the counter run one `unblob -v` (not REA) on the carrier in its own scratch and read the
   `Running extract command …` line from the `unblob.log` that unblob writes into the cwd
   (measured: `-v` writes it; `sasquatch-v4be -be …` appears as a literal line). That makes
   `CTL-C1-6` refusable on the argv even against an empty oracle.

## 5. Defects this suite found in the draft (smallest safe corrections)

1. **`carriers_matched == 4` is a count, not a coverage statement** (CTL-C1-8). Add
   `distinct_carriers_ok`: four distinct pins, and V2's provenance must name a different vendor
   URL + image sha than V1's. Without it, one vendor member plus a pad-byte alias reaches the
   target.
2. **"same relative-path suffix"** (CTL-C1-14) accepts a publication under any root. Require the
   exact `<extract_root>/<relpath>` for the single root recorded per carrier in the frozen spec,
   and `len(published) == len(oracle rows) + recorded extras`.
3. **"a SOURCES row opened this round"** (CTL-C1-17) is unenforceable by date: every round of this
   lane is `2026-10-26`, and the round-39 counter tested exactly that string. Define it as a diff
   property: the row **id** does not exist in `SOURCES.md` at the freeze and is added in
   `FREEZE..REV`.
4. **"a round-40 frontier note supersedes the AVM part"** (CTL-C1-21/22) needs a *content* clause:
   the note names the entry stem and the `## Round-40 additions to Core` heading and contains no
   stay-Frontier assertion about AVM. Presence alone is not supersession.
5. **The oracle's completeness is assumed, not scored** (CTL-C1-18). Cheapest sound clause: the
   counter re-derives the oracle from the frozen carrier with the frozen reader (it already runs
   it for the endianness test) and requires set equality with the committed `oracle.tsv`, plus
   `rows > 0` per carrier. Streak-cheap alternative if the freeze refuses a second parse: record
   `oracle_files` in the spec and require it to equal the row count **and** be at least the count
   the frozen reader reports.
6. **The projection fields are unspecified** (§4.1). Freeze the `projection.py --run` field list
   with the volatile-set exclusion, or the rerun control C1-2 passes.
7. **`extraction_failed` alone is not enough to catch a wrong-endian run with an empty oracle**
   (CTL-C1-6): require `publication_ok` to be non-vacuous (`len(oracle) > 0`, `len(published) > 0`).
8. **R39-CL4 is only half-carried**: the draft commits *tables and control receipts' inputs* in the
   freeze; CTL-C1-16 shows the counter must also **exit 2** when `controls.json` is not reachable
   at the freeze commit, and the format validation must be in the freeze commit itself.

## 6. Files

| file | what it is |
|---|---|
| `suite.json` | machine-readable controls: stage, overlay, expected verdict, refusal class, binding names |
| `ctl-lib.py` | overlay materializer (`--control`, `--root`, `--spec`, `--stage`) |
| `run-controls.sh` | driver: per-control clone, commit shapes, counter invocation, verdict comparison, `results.json` |
| `build-fixture.sh` | builds the dev fixture repo (base → freeze → tip) the suite is exercised on |
| `stub-counter.py` | byte-clause reference evaluator used only to validate the controls (not the round-40 counter; `rerun_projection_ok: null`) |
| `classify-carrier.py`, `classify-dev.tsv` | the two carrier-side tests and their dev measurements |
| `projection.py`, `projection-compare.txt` | draft vs run projection, and the fabrication comparison |
| `oracle-mode-matrix.txt` | reader-mode exit codes on four bodies (the 2×2) |
| `control-run-dev.txt`, `control-results-dev.json` | the measured suite run |
| `CTL-C1-*/…` | the materialized overlays at lane paths |
| `receipt-k1-dev-run1.json`, `receipt-k1-dev-run2.json` | two honest REA runs of one dev carrier (id instability, volatile fields) |
| `receipt-markeronly-dev.json` | REA on the marker-only body: handler `squashfs_v4_be`, `extraction_failed true`, 0 files, `extractor-failure` gap |
| `measurements.txt` | commands, outputs, exit codes for everything cited here |
