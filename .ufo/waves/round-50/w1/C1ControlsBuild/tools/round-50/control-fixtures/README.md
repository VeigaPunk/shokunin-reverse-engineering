# R50-C1 control fixtures — what each control plants and which clause it is meant to trip

Draft by seat `C1ControlsBuild` (wave 1, pre-freeze). Driver: `tools/round-50/c1-controls.py`
(stdlib; scores through `--counter` against `--lane`). This directory is the *committed*
input side: `<key>/manifest.json` (the plan of the control: expectation, provenance, the
sha256 and size of every planted byte) and gzip-compressed (mtime 0) planted bytes. `score`
plants the committed bytes into a `git clone --shared` sandbox of the lane, commits them
after the freeze, runs the counter, and judges. When `--fixtures-root` lies inside the lane,
`score` first checks every file under it equals its blob at `--freeze`.

Which numbers are measured where: every number below that is not a design statement comes
from the receipts in `.ufo/waves/round-50/w1/C1ControlsBuild/receipts/` and is named there.

## Procedure (the L1, at the freeze)

```
# once, on a QUIET host (REA 6.5.0 has a fixed 120 s deadline; a7530 needs ~48 s unloaded):
python3 -I -B tools/round-50/c1-controls.py gen   --lane <LANE> --freeze <FREEZE> \
    --counter <LANE>/tools/round-50/c1-counter.py --pkg65 <rea-agents 6.5.0> \
    --carrier-cache <CACHE> --work <SCRATCH> --fixtures-root tools/round-50/control-fixtures
# commit tools/round-50/control-fixtures/** with the freeze, then, before any data run:
python3 -I -B tools/round-50/c1-controls.py score --lane <LANE> --freeze <FREEZE> \
    --counter <LANE>/tools/round-50/c1-counter.py --pkg65 <rea-agents 6.5.0> \
    --carrier-cache <CACHE> --work <SCRATCH> --fixtures-root tools/round-50/control-fixtures \
    --out .ufo/waves/round-50/controls --json-out .ufo/waves/round-50/controls/summary.json
```

* The counter MUST be the lane's own `tools/round-50/c1-counter.py` at the freeze: the port
  binds `running counter == that path's blob at the freeze` (exit 2 `counter_not_frozen`
  otherwise). The driver never imports it; it reads its module-level constants by AST
  (`CARRIERS`, `AFTERDIR`, `HANDLER`, `PROV_BASE`/`PROV_SEGMENT`, `ENTRY`, `STEM`,
  `CORE_HEADING`, `FRONTIER_MARK`, `OPENED_DATES`, `IDS`, `CLAUSES`, `BINDINGS`, `GAPRULE`,
  `XPIN`) and detects `--work`/`--carrier-cache` support from its source, so one driver scores
  the real counter and a stand-in. The clause names the judge relies on are one table,
  `CLAUSE_ALIASES` in the driver; a name the counter never lists makes a control fail closed.
* `gen` needs the carrier bytes in `--carrier-cache` (`<pin>.bin`, from `fetch-vendor.py`);
  vendor bytes are **never** committed — the fixtures are receipts, tables and docs only.
  `gen --pos-envelopes DIR` takes the positive control's receipts from genuine REA receipts
  made elsewhere (`DIR/<id>.envelope.json[.gz]`, subject digest must equal the carrier pin,
  diagnostic links must lie under the output directory's parent) instead of running REA.
* Exit codes of `score`: 0 every control behaved; 1 a control misbehaved or the kill rule
  fired; 2 could not evaluate. A control whose verdict depends on the counter-time rerun
  (c2, c2x, pos, and c4/c1b on the swapped slot) is `could_not_evaluate` (exit 2) when the
  counter reports a `projection_error` (e.g. REA `provider_timeout`): a timed-out rerun turns
  `projection_ok` red for a reason that is not the control's.

## The controls

`slot` = a carrier id of `tools/round-50/carriers.json`. "Fails" = the named per-carrier
clause of the counter is false for that slot. Controls marked *default* are the plan's list;
*extra* arms are outside the plan and run only when named in `--controls`.

| key | plan name | planted tree | clause(s) it must trip | judged as |
|---|---|---|---|---|
| c0 | CTL-C1-0 do-nothing | nothing (counter at the freeze, `rev == freeze`) | `receipt_present` and every receipt-derived clause false on every slot; every documentation binding false | exit 1, `carriers_matched 0`, all six doc bindings present and false, no receipt-derived clause green (else kill rule) |
| c1 | CTL-C1-1 BE receipts | round-41 `V3`/`V4` `after.json` copied **verbatim** (`from_lane`, sha-pinned) to every slot (V3,V4,V3,V4) | on every slot: `subject_pin_ok` (receipt is for another carrier), `handler_ok` (`squashfs_v4_be` != `squashfs_v4_le`), `run_provenance_ok` (round-41 scratch prefix); also `parameters_ok`, path clauses | non-zero, `carriers_matched 0`, the three clauses fail on every slot |
| c2 | CTL-C1-2 oracle fabrication | per slot an envelope built only from the oracle tables, the gap rule and a real receipt's public shape (regular files at `firmware.bin_extract/<rel>`, one `unpublished-entry` per allowed non-regular entry, depth-limited gap, partial coverage, **no diagnostics**), no REA run; evidence id re-minted through the frozen xpin rule | `projection_ok` (counter-time rerun) — and, ideally, only that | non-zero, `carriers_matched 0`, `projection_ok` fails on some slot; the other failing clauses are recorded as `attributed_alone` |
| c3 | CTL-C1-3 sasquatch absent | a REAL REA receipt of the first carrier whose bytes are available, captured with `sasquatch` removed from the child PATH (the PATH is *replaced* by symlinks to every other executable) | `chunks_ok` (extraction failed), `oracle_hits_ok`; the receipt carries a `missing-extractor-dependency` gap (asserted on the planted bytes) | non-zero, `carriers_matched 0`, both clauses fail on that slot, gap kind present |
| c4 | CTL-C1-4 standard LE carrier | slot 0 of a **sandbox freeze** (overlay commit) re-pinned to round-36 `K1` carved to its `bytes_used` (70 482 B, `hsqs`, xz, `mkfs_time 0 != bytes_used`), with its oracle tables, and its genuine receipt (real REA, sasquatch on PATH, frozen `rea_parameters`, provenance prefix, id re-minted) planted at slot 0; if the pos fixtures exist the other slots hold their genuine pos receipts | `layout_ok` (the AVM-marker/superblock clause) **and no other** clause on that slot | non-zero, `carriers_matched < target`, slot fails exactly `{layout_ok}` (a second failing clause is a misbehaviour: the control is meant to isolate the marker clause); `matched == (#other slots planted)` is recorded |
| pos | CTL-C1-POS | real REA receipts for every slot (own capture or `--pos-envelopes`) + landing: `PROVINCE.md` + Core section + frontier line, README coverage row, a `S990` SOURCES row opened on `OPENED_DATES[0]`, the entry file — applied to the freeze bytes at score time from fixture blocks | none: every clause and every binding must be true | exit 0, `carriers_matched == target`, all bindings true (not a counterfactual; excluded from the kill rule). Landing text is a **fixture**, worded for the port's regexes, not the landing |
| c1b | extra: BE carrier too | slot 0 re-pinned to round-41 `L3` (committed BE AVM carrier, `sqsh`) with its verbatim round-41 receipt | `layout_ok` (reads `sqsh`), `handler_ok`, `run_provenance_ok` (+ allowed consequences) — or the counter refuses | non-zero **or** exit 2 `oracle_env_error` |
| c2x | extra: forgery with the removal list | c2's forgery plus the `MaliciousSymlinkRemoved` rows (and the removed links dropped from the gap/unpublished rows) read off a published receipt; no REA run | informational: records whether such a forgery reaches the target | any outcome is recorded in `informational_c2x`; not a kill-rule event |

Kill rule as implemented (`summary.json` `kill_rule_fires`): c0, c1 or c4 with
`carriers_matched == target` and every boolean binding true; or c0 scoring a receipt-derived
clause green. (The plan says "any carrier clause"; carrier-byte clauses — `carrier_present`,
`carrier_pin_ok`, `carve_ok`, `layout_ok`, `oracle_ok` — are legitimately green on a tree with
no receipt, so the implemented reading is the receipt-derived set.)

## Clause x control matrix (what exercises what)

| clause | tripped by |
|---|---|
| `receipt_present`, `receipt_fresh`, `evidence_envelope_ok`, `path_shape_ok`, `operation_ok` | c0 (no receipt) |
| `subject_pin_ok` | c1 |
| `handler_ok` | c1, c1b |
| `layout_ok` (AVM marker / LE superblock) | **c4 alone**, c1b (BE body) — c1 does not: a receipt has no superblock |
| `run_provenance_ok` | c1 (round-41 prefix), c1b |
| `parameters_ok` | c1 (round-41 budgets) |
| `chunks_ok`, `oracle_hits_ok`, `gaps_ok` (missing-extractor gap) | c3 |
| `projection_ok` | c2 alone (on a carrier whose real run emits a diagnostic) |
| `evidence_id_ok` | none: the driver re-mints ids so each control reds on its own clause; the counter's selftest owns it |
| `carrier_pin_ok`, `carve_ok` | none (carrier bytes come from the pinned chain; owned by the counter's own selftest) |

## Plan wording the controls contradict or sharpen (details in the seat report)

1. CTL-C1-1 is described as "red, handler/layout clauses". Receipts carry no superblock, so
   `layout_ok` cannot fire on a planted receipt; c1 trips subject/handler/provenance. A
   layout-reading BE control needs the BE *carrier* (c1b), and the draft counter then refuses
   the slot (exit 2 `oracle_env_error`, its independent `unsquashfs` arm cannot read `sqsh`).
2. CTL-C1-2 "red: rerun projection / evidence id": the id is re-minted (so it cannot be the
   red) and the projection is red **only on a carrier whose real run emits a diagnostic**
   (`MaliciousSymlinkRemoved`). Rehearsal: a forgery of a carrier without one reached
   `carriers_matched` of target; c2x shows a forgery that also copies the removal rows reaches
   the target (see the report). The plan's limit (3) should name oracle+removal-list forgery.
3. The kill rule's "any carrier clause green" must be read as receipt-derived clauses.
4. The REA default budgets fail a7530 (`Staging entry budget exceeded (10000)`); every
   receipt, the counter rerun and the data run must carry `--max-output-files 100000
   --max-output-bytes 536870912` (the table's `rea_parameters`).
5. REA 6.5.0's fixed 120 s deadline makes every rerun of a7530/a7590 flake on a loaded host;
   the counter scores that as `projection_ok` false. The controls and the data run need a
   quiet host, and the counter should treat `provider_timeout` as unevaluable.

## Rehearsal without vendor bytes

`mk-rehearsal-lane.py` builds a throwaway lane whose four carriers are *synthetic* LE xz
SquashFS v4 with `mkfs_time` patched to `bytes_used` (and a link chain REA removes), the
counter under test committed at its frozen path, and prints a freeze. `gen` + `score` against
it run in about a minute; `control-fixtures-rehearsal/` is that run's committed input side.
It proves the pipeline, not the vendor images.
