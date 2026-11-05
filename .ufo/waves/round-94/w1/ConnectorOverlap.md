# ConnectorOverlap — read-only sibling-overlap scan (round 94, item R94-C1 receipt-writer class and --json-out contract)

Scope: read-only. No counter was run. No lane file was edited. Sibling evidence is `git -C <lane> grep` over tracked `tools/` and `scripts/` at each sibling's HEAD; kaidoku evidence is `git grep` at the pinned declaration commit `dd4524916a0332bb65f83525532da1c1b8d709de`.

## Verdict

| Class | Verdict | Reason |
|---|---|---|
| Receipt-path failure class (a `json.dump` writing raw `bytes` into a `--json-out` receipt, truncating it) | **none** across siblings; one **method-only** hit (kama) | No sibling `--json-out` writer puts bytes into its receipt. The one `default=` hook in any sibling (kama) stringifies rather than refuses (see row 9). |
| Stop-boundary repair class (UPX stop-boundary repair battery) | **none** in any sibling | No sibling `tools/`, `scripts/`, `plans/` or claims file carries UPX or stop-boundary repair code. Prose hits in other lanes are false positives (tool-call IDs such as `toolu_01Dud7UPXm3…`, binary `.gz` matches). The class is kaidoku-only. |
| `--json-out` counting-command contract | **tameshi only** among siblings (3 writers, no bytes); kaidoku is the main user | See rows 6–8. |

## Overlap table

| # | Lane | file:line | class | overlap verdict | reason |
|---|---|---|---|---|---|
| 1 | kaidoku | `tools/round-93/stop-boundary-repair-battery-v3.py:353` (`json.dump(receipt)` under `--json-out`) | receipt-path failure class (bytes) | kaidoku-only (subject of C1) | Confirmed byte-carrier: row builder at `:149-158` stores `"output": out` (raw repaired bytes) and `fresh_cells` rows are emitted as-is at `:236-242, :330`. This is the M93-e `TypeError` path. |
| 2 | kaidoku | `tools/round-94/stop-boundary-repair-battery-v4.py:65` | successor writer | kaidoku-only (C1 deliverable) | `default=_default` maps `bytes` to `{bytes, sha256}`, raises `TypeError` on any other type, writes `<json-out>.tmp` and renames. Not a sibling item. |
| 3 | kaidoku | `tools/round-92/stop-boundary-repair-battery.py:176`; `tools/round-91/stop-boundary-battery.py:254`; `tools/round-92/stop-boundary-battery-v2.py:276` | stop-boundary class, plain receipts | kaidoku-only | Receipt rows carry `class`, `rc`, `tampered_block`, `box_after`, `tail`, `detail` only (`round-92/stop-boundary-repair-battery.py:66-91`). `output` is consumed for classification and not stored. No bytes reach the dump. |
| 4 | kaidoku | `tools/round-87/upx-tamper-battery.py:176`; `round-88/upx-chain-battery.py:218`; `round-89/upx-field-battery.py:214`; `round-90/upx-later-block-battery.py:173` | UPX battery `--json-out`-style receipts | kaidoku-only | Dumped object is `{argv, rc, counts, evidence_id}` only (read directly). No bytes. |
| 5 | kaidoku | `tools/round-88/field-tamper-matrix.py:260`; `round-88/field-tamper-matrix-v2.py:278` | field-tamper matrix receipts | kaidoku-only (safe convention) | Captured bytes are converted with `.hex()` before storage (`"was": before.hex()`, `:194` / `:206`). The lane's convention is to hex-encode, not dump raw bytes. |
| 6 | tameshi | `tools/additivity-range.py:432` (argparse) / `:451-453` (`--json-out` writer) | `--json-out` counting command | none | Writes `{schema, rows, …}` from git-blob text analysis. No bytes-typed value on the write path observed. |
| 7 | tameshi | `tools/rekey-cost.py:311` / `:341-343` (`Path(a.json_out).write_text(json.dumps(result,…))`) | `--json-out` counting command | none | Dumps a cost `result` dict. No bytes. Line 33 is a usage docstring only. |
| 8 | tameshi | `tools/wave-reconcile.py:836` / `:363` (`json.dumps(doc,…)` to `--json-out`) | `--json-out` counting command | none | Dumps a reconciliation `doc`. No bytes. |
| 9 | kama | `tools/round64-c2-counter.py:1718` (`json.dump(detail, fh, indent=1, default=str)`) | receipt writer with `default=` hook | **method-only** | Only sibling `default=` dump in tracked tools/scripts. `default=str` would silently turn any `bytes` into `"b'…'"`. This is the inverse of v4's refusal; method overlap (a `default=` hook) only, not the same failure. |
| 10 | chousa | `tools/argv-witness.py:370`; `tools/mechanism-witness.py:312` (`--json` receipts) | receipt writers | none | Receipt dict holds strings, ints, dicts (`witness`, `gate_rc`, `misses`, `elapsed_s`). `bytes` appear only in fixture generation (`argv-witness.py:245`), not in the receipt. |
| 11 | chousa | `tools/freeze-check.py:318, 322, 463` | fixture/claims writers | none | `json.dump` of claims, ready, and fixture objects in selftest fixtures. Not byte receipts. |
| 12 | other siblings | kake 17, kotodama 22, mado 6, mori 5, souji 4, kama (remaining ~22), tameshi (remaining ~35) `json.dump(` sites | general dumps | none (not traced to value level) | None of these lanes has UPX or stop-boundary tooling (row 13). Their dumped objects are fixtures, manifests and summaries. Not all were read line by line; flagged as scan-level, not value-level. |
| 13 | all siblings | `tools/`, `scripts/`, `plans/`, `.ufo/waves/*/claims.json` grep for `upx` / `stop.boundary` | class presence | none | Zero matches in tracked tools, scripts, plans and claims for every sibling. Prose hits in corpus and `.ufo` (tsukuroi, tabi, kake, kengaku, mado) are not repair tooling. |

## Kaidoku `json.dump` census (pinned commit)

- `git grep -n 'json\.dump('` over `tools/` at `dd4524916a…`: 261 matching lines.
- Byte-field triage (`read_bytes()`, `"output"`, `fresh_cells`, `sha256_bytes(` within 40 lines above each dump): 16 sites flagged, 245 not flagged. List and scratch output: `$S/classified-narrow.txt` (scratch, deleted before yield).
- Of the 16 flagged, I read the dumped object for each. Only **round-93 `stop-boundary-repair-battery-v3.py:353`** dumps raw bytes (`fresh_cells[*].output`, confirmed by its row builder). The other flagged sites (`round-42/43/44/49/50` counters and controls, `receipt-wrap.py:119`, `upx-field-battery.py:214`) dump dicts of argv/rc/counts/paths/strings, or a `proc.stdout.decode(...)` string. Their dumped `res`/`out`/`doc` objects were not traced to every field; the claim "no bytes" for those is from the dump site and its construction window, not a full value-level trace.
- Byte-carrying receipts in kaidoku tools: **one confirmed** (v3:353). Successor v4 fixes exactly that.

## Kaidoku-only items (no sibling claim)

- R94-C1: the receipt writer (`stop-boundary-repair-battery-v3.py` → v4 successor), the stop-boundary repair battery, and the `--json-out` contract in the kaidoku counters.
- R94-C2 (craft block 33 decision table) was **not** in this item's scope; no sibling overlap scan was run for it.

## Notes

- Scan-level, not value-level, for sibling dump sites outside chousa, tameshi and kama's `--json-out` writers. Nothing in those lanes overlaps the stop-boundary class, so the verdict does not depend on the unread sites.
- No counter was run. No tool installed or upgraded. No host state touched.
- Scratch `$S` (`/fast/scratch/hyaku/kaidoku-r94/ConnectorOverlap`) is removed before yield; the `dump-sites.txt` and `classified*.txt` files were scratch only.
- A stray file, `$HOME/.cache/.none`, was created by one of my shell commands; it is removed before yield (it was never a lane file).
