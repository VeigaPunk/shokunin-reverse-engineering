# CC6 — lane B compare seat, leg 6 (`inspect_sqlite_database`)

## CLAIM

Lane-B leg 6 agrees with lane A leg 6: both RESULT, both exit 0, same provider/engine, both receipts' digest claims recompute exactly, and a blind CC6 replay reproduces the same class; no config drift.

## METHOD

Protocol reading only before my run (leg mapping and probe rules; no lane-A receipt content). Built carrier `/tmp/cc6-leg6/cc6-leg6.sqlite` (16,384 B, sha256 `88e6b226…`; identical post-run); drove `npx -y rea-agents@6.5.0 --mcp` from /tmp with a fresh npm cache under /tmp, frames `initialize`→`notifications/initialized`→`tools/call` (table `artifacts`), 240 s deadline, stdin-close teardown. Raw capture `/tmp/cc6-leg6/leg6-stdout.raw` (13,773 B, sha256 `12d53cd5fb892da8db9037d0fcf4316a6ccf228699befd827bce854ebf8fcdfd`), stderr, exit in the same directory. Then read lane-A `receipts/leg-6.md` (RV3) and lane-B `receipts-B/leg-6.md` (BB6; not modified), recomputed each claimed digest from its fenced block (+ final LF), and tested BB6's argv difference (`mcp` vs `--mcp`).

## FINDINGS

- Lane A (RV3): RESULT, exit 0; claimed stdout `9a1445b4…` recomputes true; carrier 8,192 B, table `probe`, 1 sampled row.
- Lane B (BB6): RESULT, exit 0; claimed stdout `a3c0bc10…` (9,763 B) and stderr `df3311d1…` (186 B) recompute true; `sc4-index.db` inventory, 1 table, columns not requested.
- CC6 blind replay: RESULT, exit 0; typed Evidence `ev_f3cc12…`, scope `selected_table` complete, 3 sampled rows; carrier byte-identical before/after.
- Cross-lane: 3/3 RESULT; all provider `sqlite` / "REA SQLite database inspector" / SQLite 3.54.0, `confidence: observed`, `authority: shipped-artifact`, `wal: null`; all three servers exited 0 on stdin close.
- Variance (non-class): argument scope (selected_table vs inventory) and carriers differ, so stdout hashes necessarily differ; `protocolVersion` 2025-03-26 (A, B) vs 2025-06-18 (CC6), server echoed each client's version; argv `mcp` (BB6) vs `--mcp` (A, CC6) — control test shows both forms serve the identical stdio server (byte-identical 1,037-byte initialize responses, `/tmp/cc6-leg6/argtest-{b,c}.out`).
- Drift: HEAD `f0e8cde` unchanged; `git status` shows only pre-existing untracked `.ufo/`; no configuration edited by my runs.

## THREATS

- Blindness is partial: a pre-run grep exposed leg identity and lane A's stdout hash; my run used my own carrier and I did not read lane A's stdout before running.
- RV3 and BB6 receipts were verified from their own text only, not re-executed.
- `mcp` ≡ `--mcp` equivalence tested with `initialize` only.
- Sibling lane-B seats wrote receipts concurrently (leg-6.md appeared mid-run, attributed to BB6; untouched by me).

## VERDICT

CLEAN — leg 6 cross-lane agreement holds (RESULT×3, exit 0, digests verified, zero drift).
