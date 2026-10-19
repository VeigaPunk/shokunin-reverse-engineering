# Proposed correction — arc3-loop1-round4, C1 chain (RV-1, reviewer)

**PATCH TEXT for the PARENT; NOT APPLIED.** Seat RV-1 did not write
`corpus/`, the records-drafts, or any seat's artifact. This file names the
one factual error this seat found and the minimal repair.

## The error

Three artifacts assert that `69656e74` is a non-selector **`PUSH4` immediate**
in the EX-04 `CarrierV` runtime:

- `.ufo/waves/arc3-loop1-round4/claims/c1/EX-05/runtime-presence.txt:5`
  — `PUSH4 immediates not in planted set: ['08c379a0', '69656e74']`
- `.ufo/waves/arc3-loop1-round4/claims/c1/RV-2/evidence/push4-census.txt:14`
  — `69656e74 at [731]  [non-selector]`
- `.ufo/waves/arc3-loop1-round4/seats/EX-05.md:70` and the literal entry text
  in `.ufo/waves/arc3-loop1-round4/claims/c1/records-drafts/knowledge-entry-draft.md`
  — "`69656e74` (ASCII "ient", a fragment of the "insufficient" revert string)"

`69656e74` is **not** a `PUSH4` immediate. It occurs at byte offset 732, which
is **inside a `PUSH32` payload** beginning at pc=723:

```
pc=723  7f  696e73756666696369656e740000000000000000000000000000000000000000
            └─ ASCII "insufficient" + zero padding ────────────────────────┘
                    ^ 69656e74 begins at offset 732 (pc 723 + 9)
```

A correct opcode-boundary `PUSH4` census of the same runtime yields **16**
distinct immediates: the 15 planted selectors plus `08c379a0` (`Error(string)`)
**only**. `69656e74` does not appear.

## The repair (minimal, conclusion-preserving)

Replace the census sentence so it names the opcode class correctly. Suggested
replacement text for the entry's zero-false-positives observation:

> - **Observation (zero false positives, byte level):** `CarrierV`'s runtime
>   contains exactly one non-selector `PUSH4` immediate — `08c379a0` (the
>   `Error(string)` revert selector, at 6 sites). The other four-byte run that
>   a naive whole-file byte scan finds (`69656e74`, ASCII "ient") is a
>   **substring of the revert string "insufficient" inside a `PUSH32` payload**
>   at pc=723 — not an opcode-boundary immediate at all. Neither was reported
>   as a function: the probe's 15 functions are exactly the 15 planted
>   selectors.

The observation's **conclusion is unchanged and still true** — the probe
reported exactly the 15 planted selectors, zero extras. Only the stated
mechanism was wrong. Because the draft uses this census as its
zero-false-positive *evidence*, a reader who tries to reproduce it by scanning
for `PUSH4` opcodes will not find `69656e74`, which is the failure mode that
matters for a corpus entry.

## Why it matters beyond one line

The same class of error is the one the round is specifically claiming to have
avoided. The r3 entry (`2026-10-19-arc3-r3-evm-optimizer-shapes.md`) makes the
identical claim correctly, scoped to `PUSH4` immediates; here a *whole-file
byte substring* was promoted into the same sentence as an opcode-boundary
immediate. If the entry lands as drafted, the corpus carries a census that
cannot be reproduced by the method it names.

## Evidence (this seat, first-hand)

- `.ufo/waves/arc3-loop1-round4/claims/c1/RV-1/push4-census-corrected.txt` —
  opcode-boundary census, the enclosing `PUSH32` disassembly, and the verdict.
- `.ufo/waves/arc3-loop1-round4/claims/c1/RV-1/offset-probe.txt` — the same
  linear disassembler used for the offset-rule check.
- Runtime sha256 `57d6fd0a…`, decoded by this seat from
  `EX-04/out/runtime.hex` (`e0b1021c…`), 1,562 B.

## Not proposed

RV-1 proposes **no** change to: the entry's selector counts (15/15 verified
independently), the dispatch-shape observation, the offset-semantics
observation, the mutability-delta observation, or the map-token patch. Those
were each independently reproduced by this seat (see the seat report).
