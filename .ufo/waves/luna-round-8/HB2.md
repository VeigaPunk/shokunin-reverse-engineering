# HB2 — tools-list recount

## CLAIM
Independent re-parse of `.ufo/waves/luna-round-8/receipts/leg-2-tools.txt`: 170 unique tool names, and the six frozen 6.5-only names absent.

## METHOD
Read-only commands from repo root, 2026-10-16 21:18 -0300.
- `wc -l`, `awk 'END{print NR}'`; `sort <f> | uniq -d`; `sort -u <f> | wc -l`; `grep -cE '^[a-z0-9_]+$'`; `grep -c '^$'`; `grep -cP '[ \t\r]$'`; `file(1)`.
- Six names (sourced from `receipts/leg-9.md:9-14` and `RE6.md:12-17`): `grep -nFw -- <name> <f>` and `grep -xF -- <name> <f>` each.
- Faithfulness check: `sed -n '13p' receipts/leg-2.md` (raw tools/list frame) parsed with python3 `json.load`; `.result.tools[].name` written to /tmp; `diff` against the receipt file.
- SHA-256 recomputed for the file, the extraction, and the raw stdout block (`leg-2.md` lines 12–13).

## FINDINGS
- 170 lines / 170 unique; `uniq -d` empty (0 duplicates); 170/170 lines match `^[a-z0-9_]+$`; 0 blank, 0 CR/trailing-whitespace lines; `file(1)`: ASCII text.
- Zero hits, exit 1, for all six under both grep forms: `inspect_go_binary`, `inspect_rust_binary`, `inspect_electron_fuses`, `inspect_sqlite_database`, `search_bytes`, `inspect_with_objdump` — corroborates L9's PASS/ABSENT rows.
- Raw-frame extraction: 170 names, 170 unique; `diff` empty — leg-2-tools.txt is an order-preserving faithful extraction of the frame.
- `leg-2-tools.txt` SHA-256 `397531acb4aa6156120b728454201b91b8bdb32c0e7e9eb0ceff5257fe7bbdfe` (= extraction, identical). `leg-2.md` = MANIFEST's `f298e8f1…fef1`. Stdout-block hash recomputes to `0bbe6bc75c8f6056dc2dfccbd8a60fdec2048ccda4f985af146d0ca684cd0279`, matching `leg-2.md:17` and CA8.

## THREATS
- The six names come from receipt files, not a re-derived freeze; this verifies absence of those six literals, not the full 37-name 6.5-only diff.
- `leg-2-tools.txt` has no MANIFEST row; its hash is recorded here as an anchor, not compared to a prior claim.
- Absence verified on the artifact; no server re-probe (none assigned).

## VERDICT
CLEAN: 170 unique names recounted; all six predicted names absent; the receipt file is a faithful, order-preserving extraction of leg-2.md's raw tools/list frame.
