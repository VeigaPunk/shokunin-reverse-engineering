# Leg 9 — exact-name membership receipt

Input: `.ufo/waves/luna-round-8/receipts/leg-2-tools.txt` (Read returned 170 tool-name lines).

Each name was checked independently with the fixed-string, whole-word command shown. For each check, full grep stdout was empty, stderr was empty, exit was 1 (no match), and stdout SHA-256 was `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

| Exact name | Result |
|---|---|
| `inspect_go_binary` | PASS / ABSENT |
| `inspect_rust_binary` | PASS / ABSENT |
| `inspect_electron_fuses` | PASS / ABSENT |
| `inspect_sqlite_database` | PASS / ABSENT |
| `search_bytes` | PASS / ABSENT |
| `inspect_with_objdump` | PASS / ABSENT |

### Per-name command receipts

- `inspect_go_binary` — `grep -nFw -- inspect_go_binary .ufo/waves/luna-round-8/receipts/leg-2-tools.txt`; stdout `[empty]`; stderr `[empty]`; exit `1`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `inspect_rust_binary` — `grep -nFw -- inspect_rust_binary .ufo/waves/luna-round-8/receipts/leg-2-tools.txt`; stdout `[empty]`; stderr `[empty]`; exit `1`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `inspect_electron_fuses` — `grep -nFw -- inspect_electron_fuses .ufo/waves/luna-round-8/receipts/leg-2-tools.txt`; stdout `[empty]`; stderr `[empty]`; exit `1`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `inspect_sqlite_database` — `grep -nFw -- inspect_sqlite_database .ufo/waves/luna-round-8/receipts/leg-2-tools.txt`; stdout `[empty]`; stderr `[empty]`; exit `1`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `search_bytes` — `grep -nFw -- search_bytes .ufo/waves/luna-round-8/receipts/leg-2-tools.txt`; stdout `[empty]`; stderr `[empty]`; exit `1`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `inspect_with_objdump` — `grep -nFw -- inspect_with_objdump .ufo/waves/luna-round-8/receipts/leg-2-tools.txt`; stdout `[empty]`; stderr `[empty]`; exit `1`; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
