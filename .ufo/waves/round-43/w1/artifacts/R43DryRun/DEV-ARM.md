# Round-43 dry-run dev arm — exact subset and clause coverage

Companion to `dry-run-r43.sh`. The harness takes the dev-arm class list from
`DRY_CLASSES`; the default below is what the L1 gets without setting anything.

## The subset

| part | value | why this and not something else |
|---|---|---|
| named classes (6) | `clean-be`, `clean-le`, `clean-empty`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `mixed-symlinks` | the **RECIPES-order prefix**. The counter regenerates the full set from the frozen generator at the freeze and compares carrier-by-carrier **by id**. A prefix gives the dev-arm carriers the same ids *and the same bytes* as the corresponding carriers of that full regeneration (`class_index` and `material` are global in the generator, so bytes are selection-independent; only `seq`/ids depend on the selection). That makes `carriers_regenerated` a real green instead of a subset artefact. |
| combo family | `combo` (24 carriers, the generator's family size) | the exotic shapes live here: damage → `extractor-failure`, dependency → `missing-extractor-dependency`, `max_depth 1` → `depth-limited`, container wrap → `container-depth-limited`, residue → `unknown-chunk-handler`, legacy base → `squashfs_v1/v2/v3` handler families. Combo ids (`C01..C24`) and bytes are selection-independent, so they also regenerate exactly. |
| total | 12 named + 24 combo = **36 carriers** | measured 31 s for 12 carriers on this host; 36 carriers stays in the same order of minutes. |

`--combos N` is used only if the installed generator advertises that flag. The
round-42 port does **not** (its combo family is fixed at 24 in `FAMILIES`), so a
"4 combos" arm is not expressible; the harness records
`dev_arm.combos_flag_supported=false` and uses the family. If the round-43
generator gains the knob, the harness passes `DRY_COMBOS` (default 4) and the
receipt records it.

## Clause coverage

| new clause | what in the dev arm exercises it | gate |
|---|---|---|
| **region hash** | lane-level, not carrier-level: the harness extracts the v4 table region (marker line → end of the first markdown table after it) from the clone's `SKILL.md` and from `d1681696:SKILL.md` and compares sha256; the counter then binds the same region at the freeze-like commit. This is the clause a `SKILL.md` status-sentence edit can silently break. | G4 (+`v4_block_identical` / the counter's region binding in G5) |
| **tuple_check** | every one of the 36 carriers carries the six-field tuple under the single key `declared_features` and the generator records `generator.tuple_check` (per-carrier `{observed, declared, equal:true}`). The combos make the check non-trivial: their gap sets are drawn from factors, which is exactly where round 42's C02 predicted a tuple the run did not observe. The refusal itself is driven separately by a tampered fixture manifest (G6). | G3, G6 |
| **single-key** | every named and combo carrier is checked for the tuple under exactly one key, with no `declared`, no `features`, and no `class_expected.features`; the generator's `DECLARED_KEY`/`DECLARED_FIELDS` are compared with the counter's `DECLARED_KEY`/`REQUIRED_FEATURES` so the M41-1 seam cannot come back. | G3 |
| **lookup-combo** | the 24 combo carriers are what the frozen lookup control and `combo_unseen_majority` are scored on; with no combos those bindings are vacuous. The harness prints both, evaluated, from the receipt. | G5 |

## Bindings that stay false on a subset arm (structural, not defects)

The gate is *every binding evaluated with its value printed* (QUALITY 84), not
*target met*. On a 36-carrier dev arm these bindings are expected false and the
harness prints them as such:

* `handler_families_exercised` — needs `squashfs_v1`, `v2`, `v3` among the
  **named-class** envelopes; the id-aligned prefix is all v4. (The combos do carry
  v1–v3 handlers, but the counter reads the family set from non-combo carriers.)
* `new_legacy_label_exercised` — same reason.
* `combo_family_wellformed`, `combo_unseen_majority`, the lookup score — true only
  for the full 24-combo family at the real seed; they are evaluated either way.

`manifest_after_freeze` is false whenever the evidence path already existed in the
clone's history (a rehearsal on `corpus/evidence/round-42/c2/heldout`); on the
fresh `corpus/evidence/round-43/c1/heldout` path it must be **true**. The harness
prints that note when it sees the binding false.

## Choices rejected

* **A semantic subset** (`body-extractor-failure`, `partial-body-failure`,
  `depth-limited-mixed`, `legacy-body-failure`) names the gap families more
  directly, but it misaligns the `H##` ids against the counter's full
  regeneration, so `carriers_regenerated` turns false for a reason that has
  nothing to do with the tools. The combos already supply those shapes.
* **A full 78-carrier arm** is the real data run; the L1 runs that after the
  freeze. The dry run exists to catch the seams cheaply.
