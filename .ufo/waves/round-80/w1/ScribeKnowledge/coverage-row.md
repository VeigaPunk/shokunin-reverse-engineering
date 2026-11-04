# Coverage-map row (draft; the L1 appends under corpus/README.md `## Coverage map`)

Insert as the last row of the `## Coverage map` table, after `| Instrument and record layer, round 79 | ... |`:

| Instrument and record layer, round 80 | `2026-11-04-r80-four-bindings` | held — four resolution rules on the lane's own instruments, not a carrier class: the exact-token pointer bind (a declared token must occur as a delimited occurrence, with two digit-suffix refusal signatures and two green controls that forbid refusing everything), the duplicate-cell rule (every declared client cell counted, duplicates named, no last-wins collapse), the receipt-provenance rule (a declared instrument digest must equal a committed blob of the path it names; working-tree bytes and symbolic revs are not committed), and the guard-table binding (one `validate_receipt` clause to one SKILL row and one isolating selftest case, an absent case counting as a survivor); the lane's own record layer, not a new carrier class |

## Coverage consequence (what the map should record, and should not)

- This entry sits on the **lane's own instrument and record layer**, in the same section as rounds
  69–79. It adds no carrier, no file format and no provider surface: nothing on the map should move
  from Frontier to Core, and no carrier-class row (`Native ELF`, `Archives & packages`, `PE
  cross-format`, …) should be edited.
- What *does* move is the record's own trust surface, and only in this sense: three of the lane's
  instruments can now fail on inputs that satisfied their round-79 predecessors, so the receipts those
  instruments write in later rounds are the ones whose counts a reader may treat as resolved rather
  than merely present. The map's state cell should say so and nothing stronger — these are not
  measured carriers, and no capability outside the four named rules is claimed.
- The `depth` axis state changes because the nine `validate_receipt` clauses become table rows with
  named cases; the `freshness` axis gains its first measured baseline (R80-C2); the `calibration` axis
  gains the binder's strictness arm. Those belong to the SCORECARD's Owned-axes table, not to this
  row, which should stay a one-cell summary of the capability.
