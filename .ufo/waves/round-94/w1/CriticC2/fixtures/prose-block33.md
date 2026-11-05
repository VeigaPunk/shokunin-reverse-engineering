# Fixture block 33 — prose only (fx-prose)

Replaces the whole stuffed block 33 (heading line, table, blank line, Refs line) with this
single prose paragraph. Marker, knowledge citation `:2-9`, >=25 words and >=2 backticked
spans all present, so depth-blocks-v3's resolve+shape pass and the ONLY failing clause is
the `--shape-from 33` table requirement:

```
- **33. A repair battery's receipt write is part of the public contract: the honest run's receipt is written by the same public command that prints the verdict.** <!-- receipt-path-json-safe v1 --> Round 93's frozen battery crashed in its receipt writer on the honest repair (M93-e): `json.dump` received raw bytes and raised `TypeError`, so the positive control exited 1 with a truncated receipt while the forgery receipts that did write were the only evidence (`corpus/knowledge/2026-11-05-r94-receipt-path-json.md:2-9`). The guard the writer must carry is that bytes become a length and a sha256, that the receipt is staged in a temporary file, that a receipt counts only if it parses as complete JSON or absent is reported, and that the public CLI's receipt is re-read by a JSON parser through its public command. A selftest that exercises writer helpers in isolation misses the public path entirely. This block states every class and every guard in prose only and carries no decision table at all.
```
