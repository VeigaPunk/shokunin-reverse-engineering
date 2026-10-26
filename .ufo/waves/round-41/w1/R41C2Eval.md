# R41-C2Eval — independent evaluator v3 (round 41 wave 1, pre-freeze)

**Verdict: DONE** — `indep-eval-v3.py` written, self-tested (46 tuples, 0 failures), and run on
the 26 round-40 held-out envelopes (12 label groups ×2 replicates, 2 `unclassified`).
**17 places where the draft `Label precedence` is ambiguous (9 blocking, i.e. two literal
readings give different labels: A1, A2, A6, A7, A8, A9, A11, A12, A15) plus 1 action-vocabulary
gap that blocks scoring** are recorded in `artifacts/R41C2Eval/precedence-ambiguities.md` for the
frozen text.

Nothing frozen was written; no lane, tool, corpus or VCS state was touched. No vendor bytes
were downloaded or produced by this seat.

## Deliverables

All under `.ufo/waves/round-41/w1/artifacts/R41C2Eval/`:

| file | sha256 | what |
|---|---|---|
| `indep-eval-v3.py` | `b58ede934ccc30700be81317dc0dab3ca3ac33241d7972cf829160a9e9cbd63a` | the evaluator (stdlib only, 693 lines) |
| `precedence-ambiguities.md` | `a5debba63d1c287260f766c7d42d752ac34b1c817d41f4bca2d09b57fada25be` | A1–A17 + action-map note |
| `labels-heldout.json` | `1cb654ff8047692e2d09fcaa41fb1ac4eb410dc69f099e52b54bdeeed9384285` | 26 labels from `envelope.json` |
| `labels-heldout-full.json` | `c0971094d5f8b6ecb6ad6b64bb5f3c6eca823587d326a85adc51b1b24b559de1` | same 26 from `rea-full.json` (CLI envelope) |
| `labels-c1-dev.json` | `a5b8606fa74914915390c70156e220423ca5c0277585d28358ca75f1ca0da88d` | 4 C1 dev receipts (free combined-set specimens) |
| `labels-r39-heldout.json` | `a8e7135dff7af8e7597e6c47ea3781ea8f3e0921fc94304cd546e3a2bbae14c6` | supplementary: round-39 held-out (used only for the gap-set census) |
| `selftest.json` | `f2aae1adf5aec9ff42510e0b52a5bc7cfee9f14471263029632d82339012db10` | selftest result |

Vendor firmware bytes were neither fetched nor copied; nothing in these artifacts needs a
rebuild command.

## Inputs actually used (and the independence line)

Used: `plans/round-41-claims.md` (`**Label precedence**` steps 1–12, transcribed verbatim
into `PRECEDENCE` in the script); committed envelopes
`corpus/evidence/round-40/c2/heldout/H01..H26/{envelope.json,rea-full.json}` and
`corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json`; REA 6.5.0 sources
`dist/firmware/{FirmwarePublication,FirmwareReports,FirmwareFiles}.js` (version confirmed
from `rea-agents/package.json` = 6.5.0).

Not opened, per the item: `SKILL.md` (including any triage-table block), any
`tools/round-39`/`tools/round-40` interpreter or generator (`sqfs-triage-v2.py`,
`heldout-gen-v2.py`, `c2-counter.py`, …), the round-40 independent evaluator artifact, and
every other seat's artifacts. `grep -n -i "skill|tools/round|class_map|heldout-gen|triage"`
over the script matches only its own docstring saying it does not read them; the string
`manifest` matches only a docstring about ignoring side metadata.

I read `corpus/evidence/round-40/c2/heldout/manifest.json` once, early, to learn the
directory layout and the v2 action vocabulary. The evaluator contains no manifest
reference and no label is derived from it; the label-by-label comparison against it is the
L1's and I did not perform or report one.

## Envelope feature extraction (field → precedence symbol)

| symbol | field | note |
|---|---|---|
| OP | `operation` | exact, case-sensitive |
| PR | `provider.id` | exact |
| H | `normalized_result.chunks[].handler` ∪ `extraction_gaps[].handler` | fallback `raw_result` `ChunkReport.handler_name` |
| HF | `extraction_gaps[].handler` where `kind == "extractor-failure"` | step 5's handler referent (A8) |
| G | `extraction_gaps[].kind` | closed set of 4 in the text, 6 in REA (A15) |
| D | `extraction_gaps[].dependencies[]`, `diagnostics[].missing_dependencies[]`, `diagnostics[].report.dependencies[]` | union (A3) |
| BE | `diagnostics[].report.command` → argv tokens | `-be` as a token (A7); `no` needs a recorded argv (A6) |
| SR | `diagnostics[].report.__typename__ == "MaliciousSymlinkRemoved"` | stdout fallback; removal is not a gap kind (A9) |
| P | `len(normalized_result.files)` | published regular files, run-wide (A4); an absent `files` reads as 0 (A17) |

Both envelope shapes are accepted: the bare `data` object and the full CLI envelope
`{ok,data,meta}`. Running the 26 both ways gives **identical (label, action, step) on all
26** — the evaluator is insensitive to which file the L1 feeds it.

## The 26 round-40 held-out envelopes — labels this evaluator returns

| env | label | action | step | H | G | D | BE | P |
|---|---|---|---|---|---|---|---|---|
| H01 | clean | none | 11 | squashfs_v4_be | - | - | n/a | 5 |
| H02 | clean | none | 11 | squashfs_v4_be | - | - | n/a | 3 |
| H03 | clean | none | 11 | squashfs_v4_le | - | - | n/a | 8 |
| H04 | clean | none | 11 | squashfs_v4_le | - | - | n/a | 5 |
| H05 | clean-empty | confirm-empty | 11 | squashfs_v4_be | - | - | n/a | 0 |
| H06 | clean-empty | confirm-empty | 11 | squashfs_v4_le | - | - | n/a | 0 |
| H07 | escaping-symlink-removed | expect-link-absent | 9 | squashfs_v4_be | - | - | n/a | 3 |
| H08 | escaping-symlink-removed | expect-link-absent | 9 | squashfs_v4_le | - | - | n/a | 8 |
| H09 | in-tree-symlink-metadata | count-gap | 10 | squashfs_v4_be | unpublished-entry | - | n/a | 8 |
| H10 | in-tree-symlink-metadata | count-gap | 10 | squashfs_v4_le | unpublished-entry | - | n/a | 5 |
| H11 | mixed-symlinks | audit-symlinks | 8 | squashfs_v4_be | unpublished-entry | - | n/a | 5 |
| H12 | mixed-symlinks | audit-symlinks | 8 | squashfs_v4_le | unpublished-entry | - | n/a | 4 |
| H13 | dep-missing-be | install-extractor-be | 3 | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | 0 |
| H14 | dep-missing-be | install-extractor-be | 3 | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | 0 |
| H15 | dep-missing-le | install-extractor-le | 3 | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | 0 |
| H16 | dep-missing-le | install-extractor-le | 3 | squashfs_v4_le | missing-extractor-dependency | sasquatch | n/a | 0 |
| H17 | avm-marker-be-dropped | wrap-extractor-be | 5 | squashfs_v4_be | extractor-failure | - | no | 0 |
| H18 | avm-marker-be-dropped | wrap-extractor-be | 5 | squashfs_v4_be | extractor-failure | - | no | 0 |
| H19 | body-extractor-failure | preserve-failure | 6 | squashfs_v4_be | extractor-failure | - | yes | 0 |
| H20 | body-extractor-failure | preserve-failure | 6 | squashfs_v4_be | extractor-failure | - | yes | 0 |
| H21 | partial-body-failure | salvage-partial | 4 | squashfs_v4_be | extractor-failure | - | yes | 5 |
| H22 | partial-body-failure | salvage-partial | 4 | squashfs_v4_be | extractor-failure | - | yes | 3 |
| H23 | no-squashfs-chunk | inspect-input | 2 | - | - | - | n/a | 0 |
| H24 | no-squashfs-chunk | inspect-input | 2 | - | - | - | n/a | 0 |
| H25 | unclassified | none | 1 | - | - | - | n/a | 0 |
| H26 | unclassified | none | 1 | - | - | - | n/a | 0 |

Label counts: `clean` 4, `clean-empty` 2, `escaping-symlink-removed` 2,
`in-tree-symlink-metadata` 2, `mixed-symlinks` 2, `dep-missing-be` 2, `dep-missing-le` 2,
`avm-marker-be-dropped` 2, `body-extractor-failure` 2, `partial-body-failure` 2,
`no-squashfs-chunk` 2, `unclassified` 2. Two observations the L1 may need for the frozen
text, stated as facts about the evaluator and not as a manifest comparison:

1. H25/H26 reach `unclassified` at **step 1** (`operation: inspect_firmware_regions`,
   `provider.id: binwalk`), not at step 12 — so the out-of-domain carriers are rejected on
   domain before any squashfs reasoning.
2. Every `escaping-symlink-removed`/`mixed-symlinks` verdict rests entirely on A9's SR
   definition: those envelopes carry **no** gap row for the removed link. If the frozen
   text leaves SR undefined, the v3 table and this evaluator can disagree on 4 of the 26
   with both reading "literally".

## Why the extraction is not table-shaped

- Step 3's dependency test is exact set membership, not substring: `sasquatch` ⊂
  `sasquatch-v4be`, so a substring reading would make every BE dependency also LE
  (`s3-LE-substring-must-not-match-be`, `s3-be-substring-must-not-match-le`).
- Step 5's `-be` is an argv **token**: `sasquatch-v4be -no-exit-code …` (H17/H18) is `BE =
  no` → `avm-marker-be-dropped`, while `sasquatch-v4be -be …` (H19/H20) is `BE = yes` →
  `body-extractor-failure`. A substring test on `"be"` or a naive `"-be" in command` cannot
  separate these two classes.
- Step 5's handler is the failing gap's handler (`HF`), falling back to `H` only when REA
  recorded a null handler for a task-level failure.
- `P` is read from publication (`normalized_result.files`), never from the producer's
  intentions; H21/H22 publish exactly the 5/3 files their damage recipes left.

## Selftest

`python3 -I -B indep-eval-v3.py --selftest` → exit 0,
`{"cases": 46, "ok": true, "failures": []}`, `steps_covered: [1..12]`,
`labels_covered`: all 13 labels of the fixed action map.

46 synthetic tuples, at least one per precedence step plus the boundaries that the
ambiguity register calls out: OP/PR wrong at step 1 (including hyphen spelling); no/foreign
handler; dep be / dep le / both (be first) / neither / two substring traps; partial at
P=1/3/5, partial+in-tree, partial+mixed, partial without argv; avm `BE = no`, `BE = yes`,
`BE = n/a`, LE handler without `-be`; depth alone, depth+in-tree, depth+mixed,
partial+dep…; `SR = yes` with and without `P`; in-tree singleton, singleton broken by a
second kind; clean/clean-empty; encrypted-only and encrypted+unpublished → step 12; the CLI
envelope wrapper; the `-be` token traps; the two multi-chunk step-5 referent cases; and a
receipt whose `files` array is absent entirely (A17).

Every case asserts the **step** as well as the label, so a green run also proves the
precedence *order* (the part a table transcription is most likely to get wrong — e.g.
partial must beat depth-limited, step 4 before step 7).

## Combined-set coverage available today

The item's C2 depth axis needs combined envelopes (partial+in-tree, partial+mixed,
depth-limited+in-tree, depth-limited+mixed, depth-limited alone). Census of gap-set
combinations in committed evidence, using this evaluator's feature extraction:

| gap set | SR | envelopes | source |
|---|---|---|---|
| ∅ | no | H01–H06, H23–H26 (r40), H01–H04/H17/H18 (r39) | clean / clean-empty / no-chunk / out-of-domain |
| ∅ | yes | H07, H08; r39 H05, H06 | escaping symlink (silent removal) |
| {unpublished-entry} | no | H09, H10; r39 H07, H08 | in-tree |
| {unpublished-entry} | yes | H11, H12 | mixed |
| {missing-extractor-dependency} | – | H13–H16; r39 H09–H12 | dep |
| {extractor-failure} | – | H17–H22; r39 H13–H16/H19/H20 | body / avm / partial |
| {depth-limited, unpublished-entry} | no | **V1, V2, L1, L2** | C1 dev receipts |
| {extractor-failure, unpublished-entry} | – | **none** | needs generator carriers |
| {extractor-failure, depth-limited} | – | **none** | needs generator carriers |
| {depth-limited, unpublished-entry} + SR | yes | **none** | needs generator carriers |

So the only combined specimen that exists for free is **depth-limited + in-tree symlink
metadata**, and the round-40 C1 dev receipts supply four of them (V1 697 published files,
V2 8, L1 7, L2 6): `depth-limited-nested` at step 7 in all four, i.e. step 7 outranks step
10 for the singleton-plus-depth set. That is a ready-made, zero-cost development input for
the v3 table on the "depth-limited + symlinks" row the draft calls out, and V1's 697-file
payload also exercises "depth-limited with many published files" (step 7 has no `P`
condition — it must still win over `clean`'s spirit). The other three combined classes
still need freshly generated carriers; this evaluator is already adjudicating them in the
selftest, so the table can be scored against it the moment they exist.

## Risks and defects handed to the freeze

1. **SR is the weakest link (A9).** Four of 26 held-out envelopes and *all* escaping-link
   reasoning depend on one producer report typename that the precedence never names. Freeze
   the wording, not just the intent.
2. **`raise-depth` is missing from the v2 action vocabulary** (`manifest.json`
   `action_vocabulary`, 11 actions). `depth-limited-nested` is the new label and has no
   expected action there; if v3 reuses that vocabulary unchanged, action agreement for
   depth-limited envelopes cannot be computed. G4-style table-vs-vocabulary mismatch, not
   a table defect.
3. **A12 can mislabel, not merely under-specify**: `unpublished-entry` covers `special`
   (device-node) entries too (`FirmwareFiles.js:180-183`), so "in-tree-symlink-metadata"
   can be produced for a carrier with no symlink at all.
4. **A11 and A15 leave real shapes on `unclassified`** (`SR` beside any unrelated gap;
   `encrypted-chunk` on a squashfs chunk). Reachable in principle, absent today; if the v3
   table invents a row for either, the counter will read a table defect where the
   precedence simply has no row.
5. **A6/A7/A8 are silent-label traps for the interpreter author**: `-be` as a token, `n/a`
   ≠ `no`, and the failing chunk's handler rather than the run-wide set. All three are
   exactly the kind of thing a v3 table can only get right if the frozen text says them.
6. Calibration caveat: this evaluator is one implementation of one reading. Its
   agreement with the v3 table is a property of two independently written artifacts and is
   only as strong as the frozen text they share — which is why 7 blocking ambiguities are
   reported rather than quietly resolved in code.
7. The 26-envelope run is not a held-out score: the round-40 carriers were visible to this
   seat and to the table's author, so any agreement here is confirmation, not evidence. The
   v3 held-out set (seed = freeze hash) is the only real measurement.

## What the L1 should run

- `python3 -I -B .ufo/waves/round-41/w1/artifacts/R41C2Eval/indep-eval-v3.py --selftest`
  (expect exit 0, `ok: true`, 46 cases).
- The same with `--envelopes corpus/evidence/round-40/c2/heldout` and `--full`, then diff
  the two `labels` maps (expect identical) and diff against the v3 interpreter's labels.
- Compare against `manifest.json` (the step I was told not to do).
- Feed `precedence-ambiguities.md` into the frozen claims: A1, A2, A6, A7, A8, A9, A11,
  A12, A15 are the nine that change labels under a competing literal reading.

## Reproduce

```
export TMPDIR=/fast/scratch/hyaku
A=.ufo/waves/round-41/w1/artifacts/R41C2Eval
python3 -I -B $A/indep-eval-v3.py --selftest
python3 -I -B $A/indep-eval-v3.py --envelopes corpus/evidence/round-40/c2/heldout --out labels-heldout.json
python3 -I -B $A/indep-eval-v3.py --envelopes corpus/evidence/round-40/c2/heldout --full --out labels-heldout-full.json
python3 -I -B $A/indep-eval-v3.py --envelopes corpus/evidence/round-40/c1 --out labels-c1-dev.json
python3 -I -B $A/indep-eval-v3.py --envelopes corpus/evidence/round-39/c2/heldout --out labels-r39-heldout.json
```

The selftest and all four `--envelopes` runs exit 0. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2Eval` held only the
intermediate JSON copies and was removed; every cited file is in the artifacts directory.
No tool was installed or upgraded by this seat.
