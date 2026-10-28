# R44W2C1Rescore — independent re-derivation of the R44-C1 score and attack on the recorded stop

Seat `R44W2C1Rescore` (wave 2, falsification). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(clone `--shared` under `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Rescore/lane`, reset to
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`). Measured revision `55bcce69`; freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`; base `c29360e3`; dispatch tip `c86ea508`; record commit
`8bb1090a` (where `corpus/lessons/round-44.md` and `tools/round-45/frozen-path-preflight.py` live).
No claim, counter, rubric, frozen byte or production doc was changed. All mutations stayed inside the
seat's own clone; every commit there carries a throwaway identity and
`git rev-parse --show-toplevel` printed the clone path before each one.

## Verdict summary

| # | Question | Verdict |
|---|---|---|
| 1 | Are the recorded R44-C1 score values right (`carriers_matched 4`, `met_target false`, `exit 1`, `bindings_false`, `counter_sha256`, `frozen_path_changed`)? | **CONFIRMED** — byte-for-byte reproduction, zero field differences outside `argv`. |
| 2 | Does `55bcce69` measure a clean freeze range and an unmodified counter? | **CONFIRMED** — `frozen_path_changed []`; counter blob `9695d586…` at both REV and FREEZE; file sha256 `9f2cc140…`. |
| 3 | Is the recorded **explanation** of the stop ("the frozen claim and counter disagree about `parameters.output_directory` … the score therefore does not satisfy the frozen predicate") true? | **FALSIFIED** (D1). The score's own `bindings_false` names three PROVINCE documentation bindings and **no** provenance binding; `run_provenance_ok`/`path_shape_ok` are `true` on all four carriers. |
| 4 | Is the honest stop "the only correct reading" / forced by an unsatisfiable field? | **FALSIFIED** (D2). An 8-line append-only `PROVINCE.md` landing on the **real** `55bcce69` tree (real entry, real README, real receipts) makes the frozen counter exit **0**, `met_target true`, `bindings_false []`. The red at `55bcce69` is produced by *withholding the landing*, not by any receipt or provenance defect. |
| 5 | Does the record say exactly that? | **NO** (D1, D3, D4). |
| 6 | Is M44-2 recorded honestly and sufficiently? | **Honest on the fact** (measures at 55, states it, cites the 8 paths); **insufficient on the content** (D5, D6): the 8 files are frozen *control inputs* rewritten to match already-recorded control receipts, and the record omits that the pre-freeze c3/pos fixtures disagreed with their own receipts. |
| 7 | Does `tools/round-45/frozen-path-preflight.py` really catch it? | **For the M44-2 instance: yes** (red at `c86ea508`, green at `55bcce69`, and it catches a post-freeze *addition*). **For the rule: no** (D7, D8) — invoked as the round records it (`--pathspec tools/round-44`), it returns **clean exit 0** while a frozen `corpus/evidence/round-44/oracle/` tree is modified and the C1 counter exits 2. |

The four carrier-level claims survive every attack I ran: the receipts publish the whole oracle census,
nothing else, with the oracle digests; the committed copies are verbatim; the evidence ids recompute;
no vacuity, no free pass.

---

## 1. Independent re-derivation

Command (the seat-spec command; exit code and wall time measured, not inferred):

```
cd <clone>
python3 -I -B tools/round-44/c1-counter.py \
  --root /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Rescore/lane \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Rescore/work \
  --json-out /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Rescore/score.json
```

* exit **1**, wall **6.380 s**, stdout sha256 `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d`.
* `score.json` sha256 `715139311e1f72e49e45dac75a2f925660f99983d4dd0ea2dcdeae0d47ad905a`.

Field-by-field against `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` (a full recursive diff was
run over every key, including the whole `carriers` sub-tree):

| field | mine | recorded |
|---|---|---|
| `carriers_matched` | 4 | 4 |
| `met_target` | false | false |
| `exit_code` | 1 | 1 |
| `bindings_false` | `["province_core_section","province_core_row","frontier_note"]` | identical |
| `counter_sha256` | `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993` | identical |
| `frozen_path_changed` | `[]` | `[]` |
| `target` / `dev_matched` | 4 / 0 | 4 / 0 |
| `carriers_unchanged` / `frozen_tables_valid` | true / true | true / true |

**Difference outside `argv`: none.** The only differing values are `argv` entries (`--root` was given
as an absolute path here, the recorded receipt used `.`; `--work` and `--json-out` are seat-scoped).
A second run with identical arguments produced an **identical stdout** (`eea45d37…`), i.e. the
receipt is deterministic; `score-rerun.json` differs from `score.json` only in `argv[12]`.

Counter byte identity:

```
git -C lane rev-parse 55bcce69:tools/round-44/c1-counter.py   -> 9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569
git -C lane rev-parse c48f8a4b:tools/round-44/c1-counter.py   -> 9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569
sha256(lane/tools/round-44/c1-counter.py)                     -> 9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993
```

Byte-identical to the freeze blob, and the file digest equals the receipt's `counter_sha256`.
`frozen_path_changed []` is independently corroborated by the preflight (§5, green at `55bcce69`).

Independent content checks (not taken from the counter):

* published set == oracle census == committed copy, per carrier: `v1le` 3/3, `v1be` 3/3, `v2le` 4/4,
  `v2be` 4/4 members, sha256 **and** size equal in all three places, no extra published file
  (`ALL_VERBATIM=True`). So "the four REA receipts publish every oracle file" holds, read from
  `corpus/evidence/round-44/c1/<id>/after.json` (`normalized_result.files`) against the committed
  `firmware.bin_extract/` bytes.
* the runner's "verbatim committed copy" conjunct is implemented (`tools/round-44/c1-run.py:430`
  `copy_tree_verbatim`, written at `:596`) and holds in fact.
* every receipt `parameters.output_directory` and `normalized_result.output_directory` are equal and
  are the scratch form, e.g. `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out`;
  **none** contains the substring `corpus/evidence/round-44/c1/`.
* `gaps_note` = "0 gaps … on 0 non-regular entries", `extra_published []`, `evidence_id_ok true`,
  `subject_pin_ok true`, `projection_ok true`, `projection_diff []` on all four.

## 2. The verdict's numbers hold; its stated cause does not (D1)

`55bcce69:PROVINCE.md` is 430 lines. The landing is:

* `:424` `## Round-44 measured, not promoted (R44-C1 honest stop)`
* `:428` the row: "The counter matched 4/4 and published every oracle file, but the frozen R44-C1
  claim and counter disagree about `parameters.output_directory`: the claim required the committed
  evidence path, while the counter accepts only the `/kaidoku-r44/` scratch provenance. **The score
  therefore does not satisfy the frozen predicate**; no Core promotion is claimed."
* `:430` `Round-44 frontier note, 2026-10-28: …`

The counter's measured output at that revision contradicts the causal clause:

* `bindings_false` contains exactly the three PROVINCE document bindings. `carriers.*.run_provenance_ok`
  is `true` for all four carriers; `path_shape_ok` is `true` for all four. The provenance clause was
  **evaluated and passed**.
* The identifier the landing blames (`parameters.output_directory`) is what `provenance_ok()`
  (`tools/round-44/c1-counter.py:1176-1182`) reads, and it accepts the scratch form by construction
  (`PROV_SEGMENT = '/kaidoku-r44/'`, `:258`).
* The bindings that are false are caused by the round **not landing** a `## Round-44 additions to
  Core` section/row and by the frontier note at `:430` not naming the entry stem
  (`tools/round-44/c1-counter.py:2154-2162`). They are a consequence of the stop decision, not of any
  receipt, provenance or evidence-id failure.

So a reader of `PROVINCE.md:428` learns the opposite of what the score says: the score did not fail
on the disputed field; it failed for want of the landing that was deliberately withheld.

The same misattribution is carried into `corpus/lessons/round-44.md:57-62` (R44-CL2), which also
states "The honest stop is correct" without saying that the instrument's red is the withheld landing.

## 3. The stop is not forced — counterfactual (D2)

Both counterfactuals run in the seat's own clone; every other input (entry, README, receipts, tool
bytes) is the real `55bcce69` tree.

**A. Minimal append-only landing (decisive).** Append 8 lines to `PROVINCE.md` after the last line
(a `## Round-44 additions to Core` heading, table header + one row naming `squashfs_v1`/`squashfs_v2`
/ `SquashFS v1/v2` and `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, and one
`Round-44 frontier note … 2026-10-28-r44-squashfs-v1v2-core … SquashFS v1/v2` line), commit
`aa3e9609` in the clone, and re-run the frozen counter:

```
exit 0  carriers_matched 4  met_target true  bindings_false []  frozen_path_changed []
stdout sha256 04941f07d336c3c087cd967c75a2f00f840fb058d0c97c2df5dfda0fd7da106d
json   sha256 17888f0dc9df2e6292973d1b9b10e5357e38c227316db94f7755d3e36018829c
```

**B. The frozen positive control's own landing** (`tools/round-44/control-fixtures/pos/{PROVINCE.md,
corpus/README.md,corpus/knowledge/…}`, i.e. the bytes scored as CTL-C1-POS), planted on the same
receipts, commit `d3d1c530`: same result — exit **0**, `met_target true`, `bindings_false []`
(`score-pos.json` sha256 `c7aa96f0…`), stdout `933caea1…`.

Two independent landings therefore show the frozen **Target** (`carriers_matched == 4`, every binding
true, `frozen_path_changed []`, `met_target true`, exit 0) is reachable at the measured revision.
Consequences:

* "the stop is the only correct reading" is false. The stop is **one defensible reading** of a claim
  text that also contains the item-3 clause (§4), but it is a *policy choice*: the round declined to
  land under a claim whose prose it judged unsatisfied. It is not forced by the instrument, and the
  instrument says green was available.
* "internally unsatisfiable" (lesson `:57`) overstates. A single path can literally satisfy both
  string tests (a `corpus/evidence/round-44/c1/<id>` segment nested under a `/kaidoku-r44/` root).
  What is unsatisfiable is the item-3 clause **together with the claim's own prescribed data
  procedure** (`plans/round-44-claims.md:162-163`: `--rea-outdir-mode scratch`, "REA's output directory
  is in the private `/kaidoku-r44/` scratch segment"), which forbids producing such a path. The record
  should say that, not "internally unsatisfiable".

## 4. What the frozen claim actually says vs what the counter implements

* `plans/round-44-claims.md:34-36` (item 3): "the receipt's `parameters.output_directory` **must name
  a** `corpus/evidence/round-44/c1/` path and the evidence id must be minted over that path; the
  counter rejects any after-receipt byte-identical to a pre-freeze committed envelope".
* `plans/round-44-claims.md:137-138` (predicate): "the receipt's `parameters.output_directory` names
  this round's `/kaidoku-r44/` scratch segment and the evidence id is minted over that provenance".
* `plans/round-44-claims.md:141`: "the counter does not claim a separate byte-identity comparison".

So the frozen text contradicts itself **twice**:

1. the two `output_directory` clauses (item 3 vs predicate) — implemented only as the predicate form
   (`PROV_SEGMENT`, `c1-counter.py:258,1176-1182`);
2. item 3's "the counter rejects any after-receipt byte-identical to a pre-freeze committed envelope"
   vs `:141`'s disclaimer — **not implemented at all**; nothing in the counter compares receipt bytes
   to a pre-freeze envelope. Only `projection_ok` (counter-time rerun) narrows a self-consistent
   authored envelope, which is the carried R44-CL3 gap.

Conjuncts the counter never evaluates (searched the 3374-line counter: no binding, no `CLAUSES` entry):

| claim conjunct | counter coverage |
|---|---|
| item 3 `output_directory` names a `corpus/evidence/round-44/c1/` path | **none** (`run_provenance_ok` tests only `/kaidoku-r44/`) |
| item 3 byte-identity rejection of a pre-freeze envelope | **none** (and disclaimed at `:141`) |
| predicate `PROVINCE.md` bytes `1..<last_line_at_base>` unchanged (prefix-preserved, `:143-144`) | **none** (`BINDINGS`, `:334-338`, has no prefix check) |
| predicate "runner binds the scratch tree to the verbatim committed copy" (`:143`) | not a counter binding (implemented in `c1-run.py:430,596`; verified true in fact here) |
| "independent-reader check" mentions 7-Zip (`:149-153`) | counter binds `/usr/bin/unsquashfs` only (`oracle_tool_detail`) |

A green counter therefore never proved the whole frozen predicate; that is the real reason a
"satisfiability preflight" (lesson `:61-62`) is the right next-round fix — but the lesson draws that
conclusion from the wrong field.

## 5. M44-2 / freeze defect

**Confirmed facts.**

* `git log --oneline c48f8a4..c86ea508 -- tools/round-44/` → only `c86ea508`; its diff under
  `tools/round-44/` is **8 files, all status `M`** (nothing added):
  `control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json`, `c3/manifest.json`, and
  `control-fixtures/pos/{corpus/evidence/round-44/c1/v1be,v1le,v2be,v2le}/after.json`,
  `pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, `pos/manifest.json`.
* Counter at the tip: exit **2**, `reason "frozen_path_changed"`, the same 8 paths — identical to
  `.ufo/waves/round-44/l1/c1-score-at-tip.json` (json sha256 `04ecffaa…`; stdout `0e1c1f55…`).
* The round measures at `55bcce69` and says so in the lesson title and in
  `l1/c1-score-at-55bcce69.json`; `frozen_path_changed []` there is correct. That part is honest.

**What the record omits (D5, D6).**

The 8 files are not incidental writes; they are the **frozen control inputs**, and the commit makes
them match control receipts that were committed *earlier* (`e9e3abd1`). At `e9e3abd1` — the revision
that records the control receipts, before any post-freeze edit — the committed fixtures and the
committed receipts already disagreed:

| control | receipt `tree` sha256 / size (at `e9e3abd1`) | frozen fixture sha256 / size (at `e9e3abd1`) |
|---|---|---|
| `c3` `…/c1/v1le/after.json` | `8b15697baae7937918d185a11ebc1e216c5e04dcc5368c9fe97f652154bef43d` / 10404 | `adba89ea3d22de718b27b05976c9da316f6c8517a8e1bbc24ef2e09291bfe8c9` / 10214 |
| `pos` `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | `ee04ffc7144f3d5c04a3a355711f483e6c424f03cb0a36f728a646aec291b7db` / 20280 | `4d26a052d98a532762221f044628936029554abffd0c3c115a123c5613ef55c2` / 16880 |
| `pos` four receipt fixtures | `c4ede8bf…`, `51dd0688…`, `e44d3653…`, `d0f2117b…` | `0cb895d5…`, `12c794ad…`, `003446df…`, `5b065cb7…` |

`c1`, `c2`, `c4`, `c5` receipts do match their frozen fixture digests; only `c3` and `pos` do not —
exactly the two arms whose files `c86ea508` rewrote (plus re-minted evidence ids and re-captured
`/tmp/rea-firmware-*` paths). So the post-freeze commit was a **reconciliation of a pre-existing
control-evidence inconsistency**, performed after the freeze, in a frozen directory. The record
describes it only as "added/edited 8 files", says "added" about files that are all modified, and never
reports that the recorded c3/pos control receipts were not reproducible from the committed fixtures at
the revision that recorded them. That is the material loss for round 45: the *control evidence* was
already inconsistent at the freeze, and the only repair taken was a freeze violation.

Related, also unrecorded: every control receipt's sandbox revision is unreachable in the lane
(`d73d0806`, `8692c5e8`, `df4aa381`, `1f33aa20`, `382a178e`, `bc219304` — `git cat-file -e` all fail);
`pos/receipt.json` even carries `"planted_from_committed_fixtures": false`. The tree digests make
`c1/c2/c4/c5` re-derivable from the frozen inputs; `c3`/`pos` are not.

## 6. `tools/round-45/frozen-path-preflight.py` (R44-CL1)

Tool at `8bb1090a:tools/round-45/frozen-path-preflight.py` (107 lines, sha256
`a2ea675d0d89b462693e97d853d1c1af3122913ba2d0026105044421c9a0e174`). It does **not** exist at the
freeze, at `55bcce69`, or at the dispatch tip `c86ea508` — it landed only in the record commit.

What I ran against the recorded tool and the lane history:

| probe | command tail | exit | observed |
|---|---|---|---|
| M44-2 red | `--freeze c48f8a4 --rev c86ea508 --pathspec tools/round-44` | **1** | `verdict frozen_path_changed`, `touched` 8 (all `M`), `blob_changed` 8 — matches `l1/preflight-c86ea508.json` |
| measured rev green | `--freeze c48f8a4 --rev 55bcce69 --pathspec tools/round-44` | **0** | `verdict clean`, `touched 0`, `blob_changed 0` — matches `l1/preflight-55bcce69.json` |
| post-freeze **addition** | my commit `cfeeb718` adding `tools/round-44/zz-rescore-probe.txt` | **1** | `touched [("A","tools/round-44/zz-rescore-probe.txt")]` |
| frozen **oracle** drift (D7) | my commit `853c514a` appending one byte to `corpus/evidence/round-44/oracle/squashfs_v1/little_endian/__output__/squashfs_v1.0_le.bin_extract/apple.txt`, run with **the round's own recorded pathspec** `--pathspec tools/round-44` | **0** | `verdict clean`, `touched 0`, `blob_changed 0` — while the C1 counter at the same rev exits **2** with `frozen_path_changed` on the directory and the file |
| no pathspec (D8) | `--freeze c48f8a4 --rev 55bcce69` (no `--pathspec`) | **1** | `touched 110`, `blob_changed 0` — every file the round landed counts as "touched", so a correctly-wired call with no arguments reds every round |

So: it catches the M44-2 instance and additions under the pathspec it is given, but it does **not**
encode the round's frozen set. The round's own freeze rule freezes more than `tools/round-44/`
(`plans/round-44-claims.md:303-315` (## Frozen paths): the carrier bins, the four oracle trees under
`corpus/evidence/round-44/oracle/`, the round-42 fixtures/receipts, `SKILL.md`, `SOURCES.md`), and the
counter independently enforces `FROZEN_PREFIXES = ('tools/round-44/', 'corpus/evidence/round-44/oracle/')`
plus a longer `FROZEN_PATHS`. The preflight has neither list and no `--claim` preset; it is correct
only as complete as the hand-typed `--pathspec`. It is also **not wired** to anything:
`git config core.hooksPath` unset, no active hooks, and no invocation of the tool anywhere in the
tracked tree at `8bb1090a`. That matches the lesson's own "wire it into the round's commit sequence
before the next freeze" — but the defect above is not in the lesson's scope and remains open.

## 7. Defects for the L1 (numbered, with evidence)

**D1 — `PROVINCE.md:428` at `55bcce69` misattributes the red.**
Command: `python3 -I -B tools/round-44/c1-counter.py --root <clone> --rev 55bcce69… --freeze c48f8a4b…
--pkg65 … --work … --json-out …`; exit **1**; observed `bindings_false
["province_core_section","province_core_row","frontier_note"]`, `carriers.*.run_provenance_ok true`,
`carriers.*.path_shape_ok true`. The sentence "The score therefore does not satisfy the frozen
predicate" is tied to the `output_directory` disagreement, which the counter evaluated and passed.
Severity: high (the record states a false cause for the round's headline red).

**D2 — `corpus/lessons/round-44.md:57-62` at `8bb1090a` asserts a stronger claim than the data.**
"internally unsatisfiable on one field" and "The honest stop is correct" without (a) the counterfactual
that exit 0 is reachable (my `aa3e9609` landing: exit **0**, `met_target true`, `bindings_false []`;
second landing `d3d1c530`: same), (b) the fact that the counter implements only the scratch form, and
(c) the second contradiction (item 3 byte-identity vs `plans/round-44-claims.md:141`). Severity: high.

**D3 — `PROVINCE.md:430` at `55bcce69` cannot satisfy its own frontier-note binding.**
The landed note carries `Round-44 frontier note` and `SquashFS v1/v2` but not the entry stem
`2026-10-28-r44-squashfs-v1v2-core`; `frontier_note` is false for that reason
(`c1-counter.py:2160-2162`), independent of the stop. The record lists `frontier_note` among the reds
but explains none of the three. Severity: medium.

**D4 — `plans/round-44-claims.md:34-36` vs `:137-138`/`:141`/`:143-144`: four frozen conjuncts the
counter never evaluates** (table in §4), the most consequential being the unimplemented
`corpus/evidence/round-44/c1/` provenance clause and the unimplemented pre-freeze byte-identity
rejection. Any future green score inherits these untested clauses. Severity: high (carried R44-CL3
worsened by the prose).

**D5 — `corpus/lessons/round-44.md:16` (M44-2 row) understates the commit.**
Observed: the 8 paths are all status `M`, not added; they are the frozen c3/pos control inputs. At
`e9e3abd1` the `pos` receipt tree records `ee04ffc7…`/20280 B while the frozen `pos` fixture is
`4d26a052…`/16880 B, and `c3`'s receipt records `8b15697b…`/10404 B while the frozen `c3` fixture is
`adba89ea…`/10214 B. `c86ea508` changes exactly those bytes (plus re-minted evidence ids). The row
should record: (i) the pre-freeze control-evidence inconsistency, (ii) that the post-freeze commit was
its reconciliation, (iii) that the committed c3/pos control receipts describe sandbox trees whose
revisions (`8692c5e8`, `d73d0806`) are unreachable in the lane. Severity: high for round-45 planning.

**D6 — control evidence provenance (same area).**
`pos/receipt.json` carries `planted_from_committed_fixtures: false` and a sandbox path that no longer
exists; every control receipt's `rev` is unreachable (`git cat-file -e <rev>^{commit}` fails for all
non-`c0` controls). Only `c1/c2/c4/c5` tree digests match their frozen fixtures, so only those are
re-derivable. Severity: medium.

**D7 — `tools/round-45/frozen-path-preflight.py` false-greens the oracle frozen family.**
Command: `python3 -I -B tools/round-45/frozen-path-preflight.py --root <clone> --freeze c48f8a4b…
--rev 853c514a… --pathspec tools/round-44`; exit **0**, `verdict clean`, `touched 0`, `blob_changed 0`
— while `tools/round-44/c1-counter.py` at the same rev exits **2** with `frozen_path_changed`
`["corpus/evidence/round-44/oracle/squashfs_v1/little_endian/__output__/squashfs_v1.0_le.bin_extract",
"…/apple.txt"]`. Severity: high — the proposed M44-2 fix does not cover the M44-2 class.

**D8 — same tool, no default frozen set.**
Command: `… --freeze c48f8a4b… --rev 55bcce69…` (no `--pathspec`); exit **1**, `touched 110`,
`blob_changed 0`. The gate is only as complete as the caller's hand-typed pathspec and has no
`--claim` preset; it does not read the claim's frozen list or the counters' `FROZEN_PATHS`/
`FROZEN_PREFIXES`. Severity: medium.

## 8. Attacks that failed (verified non-findings)

* **Vacuity.** `carriers_matched 4` is not a free pass: 3/3, 3/3, 4/4, 4/4 oracle files published at
  exact relative paths with matching sha256/size, `extra_published []`, `gaps_note "0 gaps …"`, and the
  counter's own REA rerun `projection_ok true` on all four. The trouble was never the carrier set.
* **Score reproducibility.** Full recursive diff against the recorded receipt: zero differences
  outside `argv`; two identical runs give an identical stdout digest. The receipt's `counter_sha256`
  describes the counter file at `55bcce69`, which is byte-identical to the freeze blob.
* **Freeze at the measured revision.** `frozen_path_changed []` from the counter and `clean` from the
  preflight; the counter's log walk (`-m --diff-merges=first-parent`) sees no `tools/round-44/` or
  oracle-tree change in `FREEZE..55bcce69`.
* **Receipt fabrication by oracle copy.** `evidence_id_ok`, `subject_pin_ok`, `projection_ok` all true;
  the committed copies are verbatim (my independent re-hash). This does not close R44-CL3 (a
  self-consistent authored envelope could still pass), it only leaves it as stated.
* **"No Core row is claimed".** True: `province_core_rows_seen []`, section absent. The claim is not
  overclaimed anywhere; the failure is in the *explanation*, not in a false green.

## 9. Residual risk / verification gaps

* The two counterfactual landings live only in my clone (`aa3e9609`, `d3d1c530`); they are not in the
  lane and were not proposed as a change. Re-derive by appending the 8 lines shown in §3-A to
  `55bcce69:PROVINCE.md` and re-running the frozen counter.
* I did not re-run REA against the carriers myself; the counter's own rerun (`projection_ok`) is the
  only projection evidence, and the receipts' `output_directory` is gone from scratch, so a byte-level
  receipt-to-run match cannot be reconstructed.
* I did not audit R44-C2 (separate seat). I did not re-run 7-Zip; the claim's 7-Zip sentence is
  claim-only and not a counter binding.
* Preflight rename/copy handling was not probed; a `R`/`C` status whose source is inside and target
  outside (or vice versa) is the obvious next probe.
* The preflight's absent default frozen set means D7/D8 will recur in round 45 unless the pathspec set
  is derived from the counters rather than typed by hand.

## 10. Receipt

Seat `R44W2C1Rescore`; host linux 7.2.11-arch1-1; no tool installed or upgraded (no authorization
needed; python3, git, sha256sum, cmp only). Mutating git was used only inside the seat's own clone
(`git reset --hard` to `55bcce69`; throwaway-identity commits `d3d1c530`, `aa3e9609`, `cfeeb718`,
`853c514a`, each after `git rev-parse --show-toplevel` printed the clone path). No commit was made in
the lane or any fleet repo.

| step | command (abridged) | exit | wall | stdout sha256 |
|---|---|---|---|---|
| C1 at 55 | `c1-counter.py --root <clone> --rev 55bcce69 … --work <S>/work --json-out <S>/score.json` | 1 | 6.380 s | `eea45d37…cac9f8d` |
| C1 at 55 (rerun, same args) | same | 1 | — | `eea45d37…cac9f8d` (identical) |
| C1 at tip | `… --rev c86ea508 …` | 2 | 0.078 s | `0e1c1f55…2e4e3845` |
| C1 positive landing | `… --rev d3d1c530 …` | 0 | 6.892 s | `933caea1…fa1f938` |
| C1 minimal landing | `… --rev aa3e9609 …` | 0 | — | `04941f07…7da106d` |
| preflight red | `frozen-path-preflight.py --freeze c48f8a4 … --rev c86ea508 --pathspec tools/round-44` | 1 | — | `add6bc5d…9aa9039` |
| preflight green | `… --rev 55bcce69 --pathspec tools/round-44` | 0 | — | `7f8df9e3…f427b6` |
| preflight A-status | `… --rev cfeeb718 --pathspec tools/round-44` | 1 | — | `3b400bbc…503db087` |
| preflight oracle drift | `… --rev 853c514a --pathspec tools/round-44` | 0 | — | `b28c187e…bc4edf` |
| preflight no pathspec | `… --rev 55bcce69` | 1 | — | `df657c50…0a68c0cc` |
| C1 counter at oracle drift | `c1-counter.py --root <clone> --rev 853c514a …` | 2 | — | `a80ef7be…c1e81ac` |

Artifacts: `.ufo/waves/round-44/w2/artifacts/R44W2C1Rescore/` (`score.json`, `score-rerun.json`,
`score-tip.json`, `score-pos.json`, `score-min.json`, `score-oracle.json`, the matching stdouts, the
five preflight jsons, `preflight.py`).

Report: `.ufo/waves/round-44/w2/R44W2C1Rescore.md`
