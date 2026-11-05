# Fixture block 33 — keyword-stuffed (fx-stuff; base for fx-drop and fx-miscite)

Inserted verbatim into SKILL.md immediately before the line
`## Config custody for live-probe rounds (SOP)` (unique anchor; craft section ends there).

```
- **33. A repair battery's receipt write is part of the public contract: the honest run's receipt is written by the same public command that prints the verdict.** <!-- receipt-path-json-safe v1 --> Round 93's frozen battery crashed in its receipt writer on the honest repair (M93-e): `json.dump` received raw bytes and raised `TypeError`, so the positive control exited 1 with a truncated receipt while the forgery receipts that did write were the only evidence (`corpus/knowledge/2026-11-05-r94-receipt-path-json.md:2-9`). The table routes each receipt-path failure class to the guard the writer must carry:

| observed failure class | signature at base | guard the receipt writer must carry | criterion |
|---|---|---|---|
| honest-case receipt crashes | `TypeError` from `json.dump`, receipt truncated, positive control exits 1 | bytes become a length and a sha256 through the encoder's default hook; the receipt is staged in a temporary file and renamed only after the dump returns | QUALITY 189 |
| truncated receipt read as a pass | receipt file ends mid-object and the agreement counter scores garbage as evidence | a receipt counts only if it parses as complete JSON or absent is reported, never partial bytes | QUALITY 189 |
| helper-only selftest misses the public path | `--selftest` exercises writer helpers in isolation and stays green while the public CLI crashes | the public CLI runs the honest repair and its receipt is re-read by a JSON parser through its public command | QUALITY 190 |

  Refs: `corpus/QUALITY.md` rows 189, 190; `corpus/knowledge/2026-11-05-r94-receipt-path-json.md`; S319.
```

fx-drop variant: the middle body row ("truncated receipt read as a pass") is deleted; nothing else changes.
fx-miscite variant: row 1's criterion cell `QUALITY 189` becomes `QUALITY 188`; nothing else changes.
