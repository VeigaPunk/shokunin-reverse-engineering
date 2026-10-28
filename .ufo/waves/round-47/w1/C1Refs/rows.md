# R47-C1 block 24 — rows governed by clause 8 (seat C1Refs)

Ready-to-paste block 24 for `SKILL.md` `## Queue-drain craft`, written to be the **last** craft
block. Every value below was computed against the frozen bytes at
`5017e1f7299c3a812e87e7950148f54313dd279e`; the pins are the counter's own printed
`*_expected` values, read out of a real receipt, not copied by hand.

Source markers (measured, not assumed):

| what | command | value |
|---|---|---|
| freeze | `git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/` | `5017e1f7299c3a812e87e7950148f54313dd279e` |
| `interpreter_sha256` | `sha256sum tools/round-47/exact.py` at the freeze (and the receipt's `interpreter_sha256_expected`) | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| `mutations_sha256` | receipt's `mutations_sha256_expected` = sha256 of `"\n".join(name for name, _ in MUTATIONS)` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` |
| gate flag order | receipt `gate_order_literal` / `gate_order_reversed` | `1` / `0` (literal at `gate.py:99`) |

## The block

Paste verbatim; it starts with `- **24. ` so the parser's block delimiter is the `- **`, and the
title the counter sees is `24. An instrument's binding …`.

```markdown
- **24. An instrument's binding is an equality, not a containment, and its denominator is pinned.** <!-- exactness-table v3 --> Block 23 stated what makes a freeze claim checkable; this one states what makes a *check* exact — each row is a defect the round-46 non-author spot-check routed (`corpus/lessons/round-46.md:57-66`), the loose binding that let a forgery pass it, and the clause of `tools/round-47/exact.py` that now fails the forgery. Interpreter pin: `tools/round-47/exact.py` `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; the counter's own mutation list is pinned as `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`. Source S143.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | containment over a lowercased cell, so any superstring passes while nothing is measured | symbol | 1 |
| R46-CL3 a row claims a routed id another row already addresses | the id check asks whether the id appears in some row, never whether it appears once | once | 1 |
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | the count is compared with a number the code computes and nothing pins the list | digest | 1 |
| R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice and blinds the arm | the argument order is a convention no clause reads | order | 1 |

  Refs: `corpus/lessons/round-46.md:57-66` (the four routed instrument defects this matrix closes), `corpus/lessons/round-46.md:21` (M46-2: a denominator the code computes is not a pinned denominator), `corpus/lessons/round-46.md:60-62` (R46-CL3), `corpus/lessons/round-46.md:63-64` (R46-CL4), `corpus/lessons/round-46.md:65-70` (R46-CL6), `plans/round-47-claims.md:70-89` (the nine clauses this block is scored by), `plans/round-47-claims.md:83-84` (clause 8). S143 grounds the equality.
```

Exit cells are all `1`: with the trigger present the counter exits 1 and names the clause. No row
claims exit `0` (nothing here states a limit) and none claims `2` (no arm is could-not-evaluate).

## The four rows, one per routed id

| row | routed id | v2 hole (round-46 `attest.py`) | v3 arm (`exact.py`) | exit |
|---|---|---|---|---|
| 1 | R46-CL2 | arm-vocabulary test is `token in cell.lower()` | `symbol` — `cell.strip("` ") in VOCAB` | 1 |
| 2 | R46-CL3 | id present in *some* row | `once` — one id per row, each of the four exactly once | 1 |
| 3 | R46-CL4 | `forgeries_total` compared with a code-computed number | `digest` — `mutations_sha256` over the ordered mutation names | 1 |
| 4 | R46-CL6 | argv order unread | `order` — literal once, reversed pair zero times | 1 |

## Citations — every selector I actually computed at the freeze

| citation | line count at rev | what those lines are (`git show <freeze>:<path>`) |
|---|---|---|
| `corpus/lessons/round-46.md:57-66` | 102 | `## Routed defects`: R46-CL2 (57-59), R46-CL3 (60-62), R46-CL4 (63-64), R46-CL6 (65-66) |
| `corpus/lessons/round-46.md:21` | 102 | the M46-2 table row: no digest on the mutation list |
| `corpus/lessons/round-46.md:60-62` | 102 | R46-CL3 in full |
| `corpus/lessons/round-46.md:63-64` | 102 | R46-CL4 in full |
| `corpus/lessons/round-46.md:65-70` | 102 | R46-CL6 in full (`-m --diff-merges=first-parent` order-sensitive) |
| `plans/round-47-claims.md:70-89` | 190 | the nine-clause predicate |
| `plans/round-47-claims.md:83-84` | 190 | clause 8 itself |

`tools/round-47/exact.py` (561 lines) is cited twice as the interpreter and needs no selector:
`check_refs` skips `SELF`, identifying it by the sha256 pin instead.

## Two moves that look natural and both fail the frozen counter

1. **Do not cite a `corpus/knowledge/` entry in block 24 — on the frozen bytes.** Clause 8 accepts it
   (`corpus/knowledge/` is in `ALLOW`) but clause 9 then goes red: the battery's fixture repo only
   carries `SKILL.md`, `plans/round-47-claims.md`, `tools/round-47/exact.py`,
   `tools/round-46/gate.py`, `corpus/lessons/round-46.md`, `corpus/lessons/round-45.md`, so the
   genuine block scores 1 inside the battery and `battery v2_green 0 != 4`,
   `battery genuine_green 0 != 1`. Measured on the identical block text: clause 8 green, exit 1 on
   battery. Consequence for the depth proxy is in `report.md` §3 — this is a real conflict with
   `corpus/QUALITY.md` Row 77(a), not a drafting slip.
2. **Do not write the gate's path.** `tools/round-46/gate.py` is *outside* `ALLOW`
   (`ALLOW = corpus/lessons/, corpus/knowledge/, plans/, tools/round-47/`), so naming it — even
   with a correct line selector — yields `tools/round-46/gate.py: outside the validated path set`.
   Say "the gate's argv literal" instead, as the block does.

   (Scope note, measured later the same day: amendment A6 `f54b3b6d` changes `_fixture_files` so
   the battery carries every citation the marked block names, which lifts the first constraint on
   the A6 interpreter. The constraint holds for the counter as frozen at
   `5017e1f7299c3a812e87e7950148f54313dd279e`, which is the instrument this row set was verified
   against; the second constraint (`tools/round-46/gate.py` outside `ALLOW`) is byte-identical in
   A6.)
