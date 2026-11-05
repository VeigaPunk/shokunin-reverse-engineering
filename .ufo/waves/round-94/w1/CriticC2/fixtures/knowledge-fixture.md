# Knowledge fixture file (all four fixtures)

Path in each fixture: `corpus/knowledge/2026-11-05-r94-receipt-path-json.md`, exactly 12 lines
(block 33 cites `:2-9`, which requires 1 <= 2 <= 9 <= 12). Content:

```
# Receipt-path JSON safety for repair batteries (round-94 draft)

Round 93's stop-boundary repair battery v3 crashed in its receipt writer on the honest repair (M93-e): `json.dump` received raw bytes in the fresh cells and raised `TypeError`, so the positive control exited 1 with a truncated receipt while the forgery receipts that did write were the only evidence.

Python's `json` documentation (S319, https://docs.python.org/3/library/json.html, opened 2026-11-05) states for the `default` hook: "It should return a JSON encodable version of the object or raise a TypeError."

The guard: encode bytes as {"bytes": n, "sha256": hex} through the default hook and let any other unknown type raise; stage the receipt in a temporary file and rename it only after `json.dump` returns.

A selftest that exercises writer helpers in isolation stays green while the public CLI crashes; the receipt contract is measured through its public command, and a receipt counts only if it parses as complete JSON or its absence is reported.

Drafted by the round-94 wave seat CriticC2 as a falsification fixture; not a lane landing.
(end of draft)
```
