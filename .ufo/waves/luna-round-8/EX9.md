## CLAIM
Verify that the six 6.5-only names are absent from the 6.4.0 list in `.ufo/waves/luna-round-8/receipts/leg-2-tools.txt`.

## METHOD
The source read returned 170 tool-name lines. Ran `grep -nFw -- <name> .ufo/waves/luna-round-8/receipts/leg-2-tools.txt` independently for each assigned name; exact commands and full outputs are recorded in `receipts/leg-9.md`.

## FINDINGS
- `inspect_go_binary`: PASS / ABSENT (exit 1; empty stdout/stderr)
- `inspect_rust_binary`: PASS / ABSENT (exit 1; empty stdout/stderr)
- `inspect_electron_fuses`: PASS / ABSENT (exit 1; empty stdout/stderr)
- `inspect_sqlite_database`: PASS / ABSENT (exit 1; empty stdout/stderr)
- `search_bytes`: PASS / ABSENT (exit 1; empty stdout/stderr)
- `inspect_with_objdump`: PASS / ABSENT (exit 1; empty stdout/stderr)

## THREATS
This establishes membership only against the cited leg-2 list; it does not independently establish runtime call behavior.

## VERDICT
CLEAN — all six exact names are absent from the 170-line tool list.
