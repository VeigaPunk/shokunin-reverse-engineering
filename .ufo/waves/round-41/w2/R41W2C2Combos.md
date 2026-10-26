FALSIFIED — attacked the claim that 12 seeded combo carriers expose enumeration of named-class tuples rather than permitting a lookup shortcut.

## Axes and verdict

**Depth** is the attacked axis; coverage/calibration are not evaluated here. The combo family does demonstrate unseen tuples, but only 4/12 held-out combos lie outside the distinct tuples declared by the 40 named-class envelopes (27 distinct tuples in those 40 envelopes). More importantly, CTL-C2-7, the lookup control built from development named classes, gets **8/12 combo pairs right** at the frozen interpreter. Thus the family defeats a perfect named-tuple lookup, but does not force that shortcut below the whole-family target of 52/52: even a control already known to score 44/52 on development reaches 8/12 on combos, and succeeds on two-thirds of the seeded family. This is evidence of partial, not decisive, anti-enumeration pressure.

The author verdict's C2 binding failure remains distinct: the C2 receipt says `matched=52`, but `observed_features_match_declared=false` and `declared_features.missing` lists all C01–C12 because combo tuples are stored in manifest `declared`, not `class_expected.features`. This report does not convert that failed binding into a pass.

## Factor draws, observed tuples, and evaluator pairs

Feature tuple notation: H=handlers, G=exact gap-kind set, D=dependencies, BE=recorded `-be` state, SR=symlink-removed flag, P=published file count. Each line gives the manifest's seeded factors, the observed envelope tuple, and the evaluator pair.

| ID | Factors (endian, in-tree, escaping, partial, compressor, max_depth) | Observed (H; G; D; BE; SR; P) | Evaluator (label/action) |
|---|---|---|---|
| C01 | be,1,1,1,gzip,3 | be; extractor-failure+unpublished-entry; ∅; yes; yes; 7 | partial-body-failure / salvage-partial |
| C02 | be,0,1,1,gzip,1 | be; depth-limited+extractor-failure; ∅; yes; yes; 4 | partial-body-failure / salvage-partial |
| C03 | le,1,0,1,gzip,3 | le; extractor-failure+unpublished-entry; ∅; no; no; 4 | partial-body-failure / salvage-partial |
| C04 | be,0,1,0,xz,1 | be; depth-limited; ∅; n/a; yes; 6 | depth-limited / raise-depth |
| C05 | le,1,0,0,xz,1 | le; depth-limited+unpublished-entry; ∅; n/a; no; 3 | depth-limited / raise-depth |
| C06 | le,1,1,1,gzip,1 | le; depth-limited+extractor-failure+unpublished-entry; ∅; no; yes; 3 | partial-body-failure / salvage-partial |
| C07 | be,1,0,0,xz,3 | be; unpublished-entry; ∅; n/a; no; 5 | in-tree-symlink-metadata / count-gap |
| C08 | le,0,0,0,xz,1 | le; depth-limited; ∅; n/a; no; 5 | depth-limited / raise-depth |
| C09 | be,1,0,1,gzip,3 | be; extractor-failure+unpublished-entry; ∅; yes; no; 7 | partial-body-failure / salvage-partial |
| C10 | le,0,0,1,gzip,1 | le; depth-limited+extractor-failure; ∅; no; no; 5 | partial-body-failure / salvage-partial |
| C11 | be,1,1,0,gzip,3 | be; unpublished-entry; ∅; n/a; yes; 5 | mixed-symlinks / audit-symlinks |
| C12 | be,0,0,0,gzip,1 | be; depth-limited; ∅; n/a; no; 8 | depth-limited / raise-depth |

Outside the named tuple inventory: **C02, C03, C04, C06**. The other eight have an identical six-field tuple represented among the named-class declared tuples. This follows exact tuple equality on `handler_set`, `gap_kinds`, `gap_dependencies`, `be_argv`, `symlink_removed`, and `published` (the six fields the claim binds), not on factor identity or extraction count.

## Lookup attack and reproduction

Ran the frozen interpreter on all 12 combo envelopes with the frozen control directly:

```text
python3 -I -B tools/round-41/sqfs-triage-v3.py --skill .ufo/waves/round-41/controls/c2/CTL-C2-7-lookup.md --json <C01..C12 envelope.json>
exit 0
```

Compared each reported `(label, action)` with `indep-eval-v3.py --envelopes corpus/evidence/round-41/c2/heldout --out <scratch>/eval.json` (52 envelopes; exit 0). CTL-C2-7 scored **8/12** on combos:

| ID | CTL-C2-7 | Evaluator | Match |
|---|---|---|---|
| C01 | partial-body-failure / salvage-partial | partial-body-failure / salvage-partial | yes |
| C02 | partial-body-failure / salvage-partial | partial-body-failure / salvage-partial | yes |
| C03 | partial-body-failure / salvage-partial | partial-body-failure / salvage-partial | yes |
| C04 | partial-body-failure / salvage-partial | depth-limited / raise-depth | no |
| C05 | partial-body-failure / salvage-partial | depth-limited / raise-depth | no |
| C06 | partial-body-failure / salvage-partial | partial-body-failure / salvage-partial | yes |
| C07 | in-tree-symlink-metadata / count-gap | in-tree-symlink-metadata / count-gap | yes |
| C08 | partial-body-failure / salvage-partial | depth-limited / raise-depth | no |
| C09 | partial-body-failure / salvage-partial | partial-body-failure / salvage-partial | yes |
| C10 | partial-body-failure / salvage-partial | partial-body-failure / salvage-partial | yes |
| C11 | mixed-symlinks / audit-symlinks | mixed-symlinks / audit-symlinks | yes |
| C12 | partial-body-failure / salvage-partial | depth-limited / raise-depth | no |

For an upper-bound style shortcut attempt, constructed a scratch-only table from exact observed tuples in the 40 named-class held-out envelopes, assigning each exact tuple its evaluator-derived action. The frozen interpreter accepted the 28-row table and ran on all combo envelopes (exit 0). It matched the evaluator's **action on 8/12**, but full pairs were 0/12 because the table grammar requires unique row labels, so each lookup row necessarily had an artificial unique label rather than the evaluator's label. Rows did not generalize unseen tuples; those fell through to `unclassified/none`. The committed CTL-C2-7 comparison above is the fair direct pair score and gives 8/12. (A first draft of the scratch table used commas in set cells and was rejected by the interpreter; corrected to its exact `+` set grammar before recording the accepted-run result.)

## Evidence and limits

- Claims read first: `plans/round-41-claims.md`, especially R41-C2 predicate and `## Changes from the draft` lines 202–205.
- Input: frozen held-out manifest `corpus/evidence/round-41/c2/heldout/manifest.json`; all 12 combo `envelope.json` files; C2 score receipt `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`; CTL-C2-7 markdown; frozen `sqfs-triage-v3.py` and `indep-eval-v3.py`.
- Reproduction commands above were run via Python subprocess with `-I -B`; interpreter CTL exit 0 and evaluator exit 0. The 52-envelope independent evaluator output was written under `/fast/scratch/hyaku/kaidoku-r41/R41W2C2Combos/`.
- No firmware bytes, generated evidence, lane sources, or VCS state were changed. [INFERENCE] “Exposes an enumeration” is not an all-or-nothing property: the measured finding is that four unseen tuples exist and the frozen dev lookup fails four combo cases, while still correctly handling eight. It establishes meaningful but incomplete anti-lookup discrimination, not that no shortcut/generalization can succeed.

## Smallest safe correction

Keep the truthful stop on C2's declared-feature binding. For the anti-enumeration claim, narrow the wording to the measured guarantee: seeded combos include unseen tuples and the named-class lookup control misses some of them, rather than asserting the family defeats lookup as a class of shortcuts. If a stronger guarantee is intended, predeclare a combo pass threshold/control criterion that the observed 8/12 result must beat, and bind combo declarations by reading their `declared` key.
