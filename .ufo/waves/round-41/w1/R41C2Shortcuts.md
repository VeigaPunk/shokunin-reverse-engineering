# R41C2Shortcuts — shortcut tables for SquashFS triage v3 (R41-C2 attack)

**Verdict: DEFECTS FOUND.** In the grammar that actually ships (`tools/round-40/sqfs-triage-v2.py`,
the only v3-relevant parser at `49096c7e`), the R41-C2 predicate is **unsatisfiable**: no
first-match table can give all 18 planned classes the precedence pair (measured ceiling 16/18).
With the one-grammar-cell change that makes it satisfiable, **five 12-row tables reach 18/18 while
encoding no part of the precedence** and are invisible to the planned class set; each is killed only
by an envelope class the plan does not contain.

## 0. What was run

Inputs read: `plans/round-41-claims.md` (draft), the committed round-40 heldout envelopes
`corpus/evidence/round-40/c2/heldout/H*/{envelope.json,run.json}` (26 files, read-only), the frozen
interpreter `tools/round-40/sqfs-triage-v2.py` (imported as a library: `features`, `parse_skill`,
`classify`, `decision`), `SKILL.md` rule blocks 18/19, and REA 6.5.0 `dist/cli-runtime/cli.js`
for the gap-emission order only. **Not read:** `.ufo/waves/round-40/w2/artifacts/R40W2C2IndepEval/eval-v2-indep.py`
(not authorised for this seat) — so the "expected" pairs below are my own transcription of the plan's
rows 1–12 (`drv2.py:precedence`), which makes them an independent second reading of the same text.
No REA, unblob or sasquatch invocation; no reserved carrier touched; nothing installed.

```
S=/fast/scratch/hyaku/kaidoku-r41/R41C2Shortcuts          # TMPDIR=$S, removed at the end
A=<lane>/.ufo/waves/round-41/w1/artifacts/R41C2Shortcuts
python3 -I -B "$S/drv2.py" --out "$A"     # exact-set grammar (shipped parser)     exit 0
python3 -I -B "$S/drv3.py" --out "$A"     # proposed superset-cell grammar         exit 0
python3 -I -B "$LANE/tools/round-40/sqfs-triage-v2.py" --skill "$A/pluscell.md" H01/envelope.json
                                          # -> exit 2 "gap kinds cell '+extractor-failure' has an empty set member"
python3 -I -B "$LANE/tools/round-40/sqfs-triage-v2.py" --skill "$A/tables/T_min.md" \
  .../heldout/H{01,05,09,11,13,15,17,19,21,23,25}/envelope.json
                                          # -> 11 lines, 11/11 pairs correct, exit 0
sh "$A/repro.sh" "$A"                     # reproduces every number below, exit 0
```

## 1. The planned tuple set (18 classes, 36 envelopes)

13 v2 classes come from `run.json` features of the committed envelopes (each class 2 replicates);
the 5 combined classes are synthetic probes `C01..C10` derived from those committed envelopes by
adding the named gap kind / `MaliciousSymlinkRemoved` report (`probes/`, manifest included).

| class | OP/PV | H (squashfs only) | G | D | BE | SR | P | precedence pair |
|---|---|---|---|---|---|---|---|---|
| clean-be / clean-le | ef/unblob | be / le | ∅ | ∅ | n/a | no | 3–8 | clean / none |
| clean-empty (H05,H06) | ef/unblob | be, le | ∅ | ∅ | n/a | no | 0 | clean-empty / confirm-empty |
| escaping-symlink-removed (H07,H08) | ef/unblob | be, le | ∅ | ∅ | n/a | **yes** | 3,8 | escaping… / expect-link-absent |
| in-tree-symlink-metadata (H09,H10) | ef/unblob | be, le | {unpublished-entry} | ∅ | n/a | no | 5,8 | in-tree… / count-gap |
| mixed-symlinks (H11,H12) | ef/unblob | be, le | {unpublished-entry} | ∅ | n/a | **yes** | 4,5 | mixed-symlinks / audit-symlinks |
| dep-missing-be (H13,H14) | ef/unblob | be | {missing-extractor-dependency} | {sasquatch-v4be} | n/a | no | 0 | dep-missing-be / install-extractor-be |
| dep-missing-le (H15,H16) | ef/unblob | le | {missing-extractor-dependency} | {sasquatch} | n/a | no | 0 | dep-missing-le / install-extractor-le |
| avm-marker-be-dropped (H17,H18) | ef/unblob | be | {extractor-failure} | ∅ | **no** | no | 0 | avm-marker-be-dropped / wrap-extractor-be |
| body-extractor-failure (H19,H20) | ef/unblob | be | {extractor-failure} | ∅ | **yes** | no | 0 | body-extractor-failure / preserve-failure |
| partial-body-failure (H21,H22) | ef/unblob | be | {extractor-failure} | ∅ | yes | no | 3,5 | partial-body-failure / salvage-partial |
| no-squashfs-chunk (H23,H24) | ef/unblob | **∅** | ∅ | ∅ | n/a | no | 0 | no-squashfs-chunk / inspect-input |
| out-of-domain (H25,H26) | **inspect_firmware_regions/binwalk** | ∅ | ∅ | ∅ | n/a | no | 0 | unclassified / none |
| partial+in-tree (C01,C02) | ef/unblob | be | {ef, unpublished-entry} | ∅ | yes | no | 3,5 | partial-body-failure / salvage-partial |
| partial+mixed (C03,C04) | ef/unblob | be | {ef, unpublished-entry} | ∅ | yes | **yes** | 3,5 | partial-body-failure / salvage-partial |
| depth-limited-alone (C05,C06) | ef/unblob | be, le | {depth-limited} | ∅ | n/a | no | 5,8 | depth-limited-nested / *action not stated in the draft* |
| depth-limited+in-tree (C07,C08) | ef/unblob | be, le | {depth-limited, unpublished-entry} | ∅ | n/a | no | 5,8 | depth-limited-nested / *same* |
| depth-limited+mixed (C09,C10) | ef/unblob | be, le | {depth-limited, unpublished-entry} | ∅ | n/a | **yes** | 4,5 | depth-limited-nested / *same* |

Cross-check of the committed data (no inference): H23/H24 differ from H25/H26 **only** in
`operation`/`provider`; H17/H18 differ from H19/H20 **only** in the recorded `-be` token; H09/H10
differ from H11/H12 **only** in `MaliciousSymlinkRemoved`; H13/H14 differ from H15/H16 in the
handler *and* the dependency name simultaneously.

## 2. Blocker: the predicate cannot be implemented in the shipped grammar

Two independent constraints of the only existing grammar:

1. **Unique labels** — `parse_table` raises `duplicate label` (`sqfs-triage-v2.py:341-347`, check at `:346`). One row
   per label, so "`extractor-failure` ∈ G … *whatever other gaps accompany it*" (row 4) and
   "`depth-limited` ∈ G … *whatever symlink gaps accompany it*" (row 7) cannot be written as
   "this label via {ef} **or** {ef,ue}".
2. **No containment cell** — gap/dependency cells are `*`, `none`, or an **exact** set
   (`_parse_set_cell`, `:245-259`). A `+member` containment cell is rejected by the shipped parser
   (`exit 2`, §0).

Measured consequence (all tables parsed by the frozen interpreter, scored per (label, action)
against 36 planned envelopes in 18 classes):

| table (exact-set grammar) | rows | planned classes | missed |
|---|---|---|---|
| committed `SKILL.md` v2 block, scored in place (R40-CL5 baseline) | 11 | **13/18** | the 5 combined (`partial+in-tree`, `partial+mixed`, `dl+in-tree`, `dl+mixed`, `dl-alone`) |
| precedence-order, exact cells (`T_exact_faithful`) | 14 | 14/18 | all 4 symlink/depth combos |
| **smallest table reaching the ceiling** (`T_min`, wildcard `*` partial row last) | **13** | **16/18** | `depth-limited+in-tree`, `depth-limited+mixed` |

Proof that 16/18 is the ceiling: the three `depth-limited` tuples share the label
`depth-limited-nested`, so one row must match `{dl}`, `{dl,ue},SR=no`, `{dl,ue},SR=yes`. With no
containment cell its gap cell is `{dl}` (misses both combos) or `{dl,ue}` (misses `dl-alone`) or `*`.
A `*` depth row must sit after `mixed`/`in-tree`/`clean` to avoid stealing them, i.e. after the
partial row — but the partial rows must also be broad to cover `{ef}` **and** `{ef,ue}`, so whichever
of the two broad rows comes second loses its combos. Measured both orders: 16/18 and 15/18
(`T_min`, `S_dl_wildcard_last`). Adding rows does not help (duplicate-label ban).

**Smallest safe correction (freeze-blocking):** the claim must state the v3 grammar delta and ship
the v3 interpreter as a named deliverable (`tools/round-41/sqfs-triage-v3.py`; the draft says "the
frozen v3 interpreter" but never names or specifies it). Minimum delta that makes the predicate
satisfiable and keeps the v2 column set: a **superset set cell** `+a` / `+a+b` meaning
`G ⊇ {a,b}` (and the same for dependencies). That is the only change needed — §3 shows the
resulting table is exactly 12 rows.

## 3. Smallest table that scores every planned class (with that one delta)

`tables-v3/T_contains.md` — **12 rows = the floor**, because 12 labels are distinct
(`clean`, `clean-empty`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `mixed-symlinks`,
`dep-missing-be`, `dep-missing-le`, `avm-marker-be-dropped`, `body-extractor-failure`,
`partial-body-failure`, `no-squashfs-chunk`, `depth-limited-nested`) and one row yields one label;
`unclassified` stays the parser default.

Row order = precedence order 1→11, cells: row 1 `handler=none`; rows 2–3
`gaps=+missing-extractor-dependency` with `deps=+sasquatch-v4be` / `+sasquatch`; row 4
`gaps=+extractor-failure, files=>0`; row 5 `handler=squashfs_v4_be, gaps=+extractor-failure,
be=no, files=0`; row 6 `gaps=+extractor-failure, files=0`; row 7 `gaps=+depth-limited`; row 8
`gaps=+unpublished-entry, sr=yes`; row 9 `gaps=none, sr=yes`; row 10 `gaps=+unpublished-entry,
sr=no`; row 11 `gaps=none, sr=no, files=>0`; row 12 `gaps=none, sr=no, files=0`.

Measured: **18/18 planned classes, 0 divergences on all 14 exposure probes.** Two rows are
load-bearing in ways the plan's prose does not say: row 5's `handler=squashfs_v4_be` (see S2) and
row 7's `handler=squashfs_v4_*` (see S5).

## 4. Shortcut tables — target reached without the precedence (contains grammar, planned 18)

`A` = achieves 18/18 on the planned set. Exposure probe = the tuple where it diverges from rows 1–12
(probe envelopes in `probes/`, features in §1/§6).

| # | table (12 rows unless noted) | planned | missed planned class | diverges on | what it stops encoding |
|---|---|---|---|---|---|
| S1 | `S_op_star` | **18/18** | — | X10 | row 1's `operation` half of the guard |
| S2 | `S_pv_star` | **18/18** | — | X11 | row 1's `provider` half |
| S3 | `S_avm_handler_star` | **18/18** | — | X01,X02 | row 5's `handler = squashfs_v4_be` |
| S4 | `S_handler_star_all` | **18/18** | — | X01,X02 | the handler cell on every row but row 1 |
| S5 | `S_dep_star_by_handler` | **18/18** | — | X07 | row 3's "D names …" test (splits on the handler instead) |
| S6 | `S_dl_first` | **18/18** | — | X08,X12 | row order 4–6 before 7 (depth-limited precedence over a failure) |
| S7 | `S_dl_first_star` | **18/18** | — | X05,X08,X12 | row 7's handler cell + its position |
| S8 | `S_star_default` (13 rows) | **18/18** | — | — | nothing, but proves the kill-rule control is score-neutral (§7c) |
| S9 | `S_wildcard_partial` | 16/18 | `partial+in-tree`, `partial+mixed` | X12,X13,X14 | row 4's `extractor-failure ∈ G` test |
| S10 | `S_dep_star` | 17/18 | `dep-missing-le` | X07 | row 3 entirely |
| S11 | `S_no_be` | 17/18 | `body-extractor-failure` | X08 | row 5 vs row 6 (`-be` token) |
| S12 | `S_no_domain` | 17/18 | `out-of-domain` | X10,X11 | row 1 entirely (**caught by the real H25/H26**) |
| S13 | `S_files_star` | 15/18 | avm, body, clean-empty | X01,X02,X08 | rows 5/6/12's published-file split |
| S14 | `S_no_sr` | 14/18 | clean-be, clean-le, clean-empty, in-tree | — | rows 8–10's symlink split |
| S15 | `S_exact_cells` (v2 table in v3 cells) | 14/18 | all 4 combos | X12 | rows 4 and 7 — quantifies R40-CL5 as 4 classes, not 2 |

Column-redundancy summary (planned set only): `operation` **and** `provider` are each individually
droppable (S1, S2) — REA's real output has exactly two `(OP,PV)` pairs and they differ in both fields,
so a single-column guard is indistinguishable from the two-column guard on real carriers. Dropping
both is caught (S12). `dependencies` is droppable (S5). `handler` is droppable everywhere except the
no-chunk row (S4) — and its one remaining load-bearing role inside the domain rows is row 5 (S3).
Only `gap kinds`, `symlink removed`, `published files` and `-be` are forced by the planned set.

## 5. Tables that score all but one class (contains grammar)

Each removes exactly one row from `T_contains` and misses exactly the class named:

| table (11 rows) | planned | missed |
|---|---|---|
| `S_drop__mixed-symlinks` | 17/18 | mixed-symlinks |
| `S_drop__no-squashfs-chunk` | 17/18 | no-squashfs-chunk (and diverges X03–X06) |
| `S_drop__avm-marker-be-dropped` | 17/18 | avm-marker-be-dropped |
| `S_drop__body-extractor-failure` | 17/18 | body-extractor-failure (diverges X01,X02,X08) |
| `S_drop__dep-missing-be` | 17/18 | dep-missing-be (diverges X09) |
| `S_drop__dep-missing-le` | 17/18 | dep-missing-le (diverges X07) |
| `S_drop__escaping-symlink-removed` | 17/18 | escaping-symlink-removed |
| `S_drop__in-tree-symlink-metadata` | 17/18 | in-tree-symlink-metadata |
| `S_drop__clean-empty` | 17/18 | clean-empty |
| `S_drop__partial-body-failure` | 15/18 | partial-body-failure, partial+in-tree, partial+mixed |
| `S_drop__depth-limited-nested` | 15/18 | depth-limited-nested ×3 |
| `S_drop__clean` | 16/18 | clean-be, clean-le |

The two-class/three-class rows are exactly the labels whose planned set spans several tuples — i.e.
the combined classes are the only thing forcing rows 4 and 7 to exist, and each *alone* is not
enough to force the row to be written correctly (S9/S6 show the row can exist and still be wrong).

## 6. Which held-out class exposes each shortcut, and what to add

| shortcut killed | class to add (replicates) | tuple | expected pair | how to build it |
|---|---|---|---|---|
| S3, S4 | **body-extractor-failure-le** (2) | H=`squashfs_v4_le`, G={ef}, BE=**no**, P=0 | body-extractor-failure / preserve-failure | the existing `zero-id-table` recipe on an LE body: `corruption_zero_id_table` already picks `'<'` for `endian='le'` (`heldout-gen-v2.py:524-533`), so it is a class-map + manifest entry, no new writer code |
| S6, S7 | **failure+depth-limited** (2) | G={ef, depth-limited}, P=0, BE=yes | body-extractor-failure | REA emits gaps as a conjunction array (`cli.js:14258-14284`: dependency, extractor-failure, unknown-chunk, encrypted, depth-limited, unpublished) so a run with one failed chunk and one max-depth path carries both kinds |
| S5 | **dep-name-other** (2) | H=`squashfs_v4_be`, G={missing-extractor-dependency}, D={**lz4**}, P>0 | unclassified (row 3 has no branch for a third name; see §7b) | strip a non-squashfs extractor from the unblob child PATH with a carrier holding that format while the squashfs body publishes files |
| S9, `T_min` | **unnamed-gap-with-files** (2) | H=`squashfs_v4_be`, G={unknown-chunk-handler}, P>0 | unclassified | a carrier whose region scan yields a `handler: null` chunk plus published files (trailing junk past `bytes_used`) |
| S12 (already caught) | keep the real H25/H26 | OP=inspect_firmware_regions, PV=binwalk | unclassified | already committed |
| S1, S2, S5 (guard + dep name) | **envelope-mutation controls** (not carriers) | X10 `inspect_firmware_regions`+`unblob`; X11 `extract_firmware`+`binwalk`; X07 D={sasquatch} on a BE handler | unclassified / unclassified / dep-missing-le | mutate committed envelopes; state in the claim that rows 1 and 3 are tested this way — **no REA carrier can produce them**, so without this the claim's two-column guard and D test are unfalsifiable |
| S13, S14 | no new class needed (already 15/18, 14/18) | — | — | rows 5/6/12 and 8–10 are already forced |

Cost: 8 new envelopes (4 classes × 2) — the plan already budgets 2 replicates/class, so this is
36 → 44 envelopes; only `body-extractor-failure-le` and `failure+depth-limited` need new carriers,
the other two are cheap mutations of existing ones. With them, every 18/18 shortcut in §4 becomes a
scoring failure, and the smallest table that survives all 18 + 8 classes is `T_contains`.

## 7. Defects in the claim text itself (independent of the tables)

a. **The new label has no action.** `depth-limited-nested` is scored as a pair, but rows 1–12 never
   give its action, and the v2 vocabulary line has no descend token
   (`none inspect-input install-extractor-be install-extractor-le wrap-extractor-be
   preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty`).
   As written the predicate cannot be evaluated for 3 of 18 classes; the score above treats the
   action as unspecified (label-only).
b. **Row 3 has no else branch.** "`missing-extractor-dependency` ∈ G → dep-missing-be if D names
   `sasquatch-v4be`, dep-missing-le if D names `sasquatch`" says nothing when D names a third
   extractor (lz4/7z/xz — real unblob dependency names). Two honest readings exist (fall through to
   row 12 → `unclassified`, or force a dep label); the independent evaluator may pick either and the
   claim has no tie-break. State the else.
c. **The kill-rule control "a `*` default row" cannot fail.** Measured: `S_star_default` (correct
   table + trailing all-`*` row) scores identically to `T_contains` — 18/18, zero divergences —
   because the parser's no-match default already prints `unclassified`/`none`. Replace the control
   with "a `*` **gap-kinds** row in place of the partial row", which is detectable (`S_wildcard_partial`,
   16/18).
d. **`avm-marker-be-dropped` and a damaged genuine AVM body are the same feature tuple**
   (H=`squashfs_v4_be`, G={ef}, BE=no, P=0). Row 5 therefore labels damage as a marker handshake and
   prescribes `wrap-extractor-be` on a corrupt image — the exact distinction the round-40 prose
   carried ("walk the inode-table metadata headers little-endian first", v2 cause text) and that the
   draft's prose repairs M2/M3 say they are fixing. Either the row's cause must mandate that header
   walk before wrapping (and the claim must say the label is a routing label), or the plan must add
   the tuple as an explicitly ambiguous class. It cannot be separated by any table.
e. **Row order 4–6 before 7 means `extractor-failure` always beats `depth-limited`.** Whether that is
   intended is not stated; S6/S7 show that moving row 7 up is score-invisible on the planned set and
   mislabels X08/X12.

## 8. Limits

- The 5 combined and 14 exposure envelopes are **synthetic mutations of committed envelopes**, not
  REA runs; their tuples match what REA's gap builder would emit (`cli.js:14258-14284`) but the
  carrier cost in §6 is [INFERENCE] on reproducibility, not measured.
- Every "expected" pair is my reading of the plan's rows 1–12; I did not read the round-40
  independent evaluator, so agreement between my labels and the frozen evaluator's is a cross-check
  the C2 owner should record, not an assumption here.
- The superset-cell numbers use the local evaluator in `drv3.py` (v3 does not exist); the exact-set
  numbers use the frozen interpreter unchanged.

## 9. Evidence index (`.../artifacts/R41C2Shortcuts/`)

| file | sha256 |
|---|---|
| `drv2.py` (planned tuples, 24 probes, exact-grammar candidates, precedence transcription) | `5803ac7dfd5b64a0ca11ab3e41087077cd9974bc8e586090d2e107d16c567d93` |
| `drv3.py` (superset-cell evaluator, 28 candidates) | `5902f7f7e406e5b80de25d5355bfc1e9846a5949f3f5f501c6d7a36f7e99ae48` |
| `repro.sh` (rebuilds every number, exit 0) | `f9cf3fe6676cac96e61fd5c461990471f8d39a6ac0e29c5167565c087bc288cc` |
| `score.json` (exact grammar) | `f12f1cb5b21d50d4e5bd40b323f8ca6d6994e0e88b03587eda424bd4b74c008c` |
| `score-v3grammar.json` (superset cells) | `a018dbcbcf484c3be5e1bebd79fa2d729c742862c289ca6224925b1cb235cfcc` |
| `probes/manifest-probes.json` + `probes/{C01..C10,X01..X14}.json` | `694e6799451924f8bdf6166d07e87cf990cf02b72527da647b5b542d33ffc834` |
| `tables/T_min.md` (13 rows, 16/18 exact-grammar ceiling) | `6b5d63c127fa180e4fc987af5a7e7e8cbe4a0228d62ffed7c9b7caaf0bb40ceb` |
| `tables/T_exact_faithful.md` (14 rows, 14/18) | `03db35ca19120ebdbb163d823d496efd0826095c29ffe8605333c189c997f8a9` |
| `tables-v3/*.md` (28 candidate tables, marker `v3-pseudo`) | see `repro.sh` |
| `pluscell.md` (v2 rejects `+` cells, exit 2) | regenerated by `repro.sh` |

Impacted axes: **depth** (R41-C2's own target is unreachable as written and reachable by ≥5
precedence-free tables once fixed), **calibration** (rows 3/5/7 semantics, the new action token, and
a score-neutral kill-rule control). Coverage (R41-C1) untouched — no shared data read.
