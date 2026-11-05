## stub-false

```
- **34. A receipt is bound to its world, not its label, and the writer never follows a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class: the agreement counter admitted rewritten labels, the base receipts carried a short `--rev`, and the v4 writer followed a `<json-out>.tmp` symlink. The table routes each observed failure to the criterion that states its rule.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 192 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 192 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (a label rewrite is never bound to its receipt).** A receipt is never bound to the frozen expect label, and an agreement counter that reads a rewritten label is correct even when met_target is true. A counter is never required to recompute the label from its own counts, so a receipt whose counts contradict its label is accepted as honest.
- **Row 192 (the revision field is free text).** A receipt's revision may be a short prefix of the measured tree, since git rev-parse is never needed to validate it, and a writer is refused by its full measured revision alone. A writer that follows a planted link is correct, because a unique temporary name is never needed: a fixed temp name is the safe form.
```

## stub-junk-vocab

```
- **34. A receipt is bound to its world, not its label, and the writer never follows a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class: the agreement counter admitted rewritten labels, the base receipts carried a short `--rev`, and the v4 writer followed a `<json-out>.tmp` symlink. The table routes each observed failure to the criterion that states its rule.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 192 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 192 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (a label rewrite is never bound to its receipt).** A receipt is never bound to the frozen expect label, and an agreement counter that reads a rewritten label is correct even when met_target is true. A counter is never required to recompute the label from its own counts, so a receipt whose counts contradict its label is accepted as honest. An unknown type takes the str() fallback, and the label is accepted as the receipt's world.
- **Row 192 (the revision field is free text).** A receipt's revision may be a short prefix of the measured tree, since git rev-parse is never needed to validate it, and a writer is refused by its full measured revision alone. A writer that follows a planted link is correct, because a unique temporary name is never needed: a fixed temp name is the safe form. A receipt may be partial JSON, and a helper-only selftest is the proof of the public path, so the receipt is complete JSON or absent by assertion.
```

## keyword-in-block-only

```
- **34. A receipt is bound to the frozen expect label, is checked only when met_target is true, and must recompute the label from its own counts; the revision is the full measured revision via git rev-parse, and the temp file is a unique temporary name, not a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class, and the table routes each one to its criterion.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 192 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 192 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (empty).** A criterion that states nothing in this check.
- **Row 192 (empty).** A criterion that states nothing in this check.
```

## keyword-miss-control

```
- **34. A receipt is bound to its world, not its label, and the writer never follows a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class: the agreement counter admitted rewritten labels, the base receipts carried a short `--rev`, and the v4 writer followed a `<json-out>.tmp` symlink. The table routes each observed failure to the criterion that states its rule.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 192 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 192 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (a label rewrite is never bound to its receipt).** A receipt is never bound to the frozen expect label, and an agreement counter that reads a rewritten label is correct even when met_target is true. A counter is never required to recompute the label from its own counts, so a receipt whose counts contradict its label is accepted as honest.
- **Row 192 (the revision field is free text).** A receipt's revision may be a short prefix of the measured tree, since git rev-parse is never needed to validate it, and a writer is refused by its full measured revision alone. A writer that follows a unplanned link is correct, because a unique temporary name is never needed: a fixed temp name is the safe form.
```

## miscite-191

```
- **34. A receipt is bound to its world, not its label, and the writer never follows a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class: the agreement counter admitted rewritten labels, the base receipts carried a short `--rev`, and the v4 writer followed a `<json-out>.tmp` symlink. The table routes each observed failure to the criterion that states its rule.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 191 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 191 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (a label rewrite is never bound to its receipt).** A receipt is never bound to the frozen expect label, and an agreement counter that reads a rewritten label is correct even when met_target is true. A counter is never required to recompute the label from its own counts, so a receipt whose counts contradict its label is accepted as honest. A revision is accepted by its full measured revision alone, git rev-parse is never needed, and a planted link is harmless because a unique temporary name is never needed.
- **Row 192 (unrelated).** A row about nothing in particular.
```

## junk-table-no-snippets

```
- **34. A junk rule block.** <!-- receipt-world-binding v1 --> This block says that the receipt world is bound, the receipt revision is checked, and a writer is safe under every condition named in the table below, which lists three rows of decorative content with four cells each, `alpha` and `beta`. Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

| a | b | c | d |
|---|---|---|---|
| x | y | z | w |
| p | q | r | s |
| m | n | o | t |

--- QUALITY additions ---
- **Row 191 (empty).** A criterion that states nothing in this check.
- **Row 192 (empty).** A criterion that states nothing in this check.
```

## named-rows-no-keywords

```
- **34. A receipt is bound to its world, not its label, and the writer never follows a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class: the agreement counter admitted rewritten labels, the base receipts carried a short `--rev`, and the v4 writer followed a `<json-out>.tmp` symlink. The table routes each observed failure to the criterion that states its rule.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 192 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 192 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (empty).** A criterion that states nothing in this check.
- **Row 192 (empty).** A criterion that states nothing in this check.
```

## stub-true-control

```
- **34. A receipt is bound to its world, not its label, and the writer never follows a planted link.** <!-- receipt-world-binding v1 --> Round 94's M94-e, M94-f and SentinelWrite F1 are the receipt-world-binding failure class: the agreement counter admitted rewritten labels, the base receipts carried a short `--rev`, and the v4 writer followed a `<json-out>.tmp` symlink. The table routes each observed failure to the criterion that states its rule.

| observed failure class | signature | guard | criterion |
|---|---|---|---|
| consistent label rewrite | label and counts disagree with the frozen expect label | bind label to frozen expect | QUALITY 191 |
| counts that do not recompute the label | counts describe a different world than the label | recompute label from counts | QUALITY 191 |
| revision field not the measured tree | `--rev` short and unvalidated | full measured revision via git rev-parse | QUALITY 192 |
| temp-file symlink escape | `<json-out>.tmp` followed to a victim | unique temporary name, no planted link | QUALITY 192 |

  Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3.

--- QUALITY additions ---
- **Row 191 (a receipt is bound to its world).** The receipt's label is bound to the frozen expect label, and that binding is checked only when met_target is true; a label that disagrees with its counts is refused because a counter must recompute the label from its own counts.
- **Row 192 (the revision is the measured tree).** A receipt names its full measured revision, checked against git rev-parse, and a writer creates its temporary file under a unique temporary name, so no planted link is followed.
```

