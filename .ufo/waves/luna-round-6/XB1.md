# XB1 — census runner (lane B)

## CLAIM
Lane B seat XB1 (census runner): at HEAD f0e8cde the available round-6 census artifacts reproduce exactly — canonical pre-state (Recipe A + token set) unchanged, and CA6's fail-closed ten-leg inventory over `receipts/` passes. Receipt: `.ufo/waves/luna-round-6/receipts/census-laneB-pre.txt`, sha256 `320ee5a2927560bf1f016607f27d26859a8fbabdcbdb42fa51dd7a7394b85cfd`.

## METHOD
Read-only at `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`. Assignment names "CB6's final census"; `**/CB6*` → only `.ufo/waves/luna-round-5/CB6.md` (round-5 provenance seat) — no CB6 artifact in this wave, so I resolved to the two on-disk census artifacts: (a) Recipe A verbatim (`SCORECARD.md:92-123`, `REV=$(git rev-parse HEAD)`) plus the coverage-map token census (definition: `SCORECARD.md:101-102`); (b) CA6's inventory command verbatim (`CA6.md:9`) against `receipts/`, plus a labelled variant against `receipts-B/`. Run outputs in `/tmp/xb1-r6`; the receipt embeds command + full stdout/stderr/exit/stdout-sha256 per run; all 8 embedded sections byte-verified against captures. No MCP servers started (nothing to terminate), no probes, no config edits, no tracked writes.

## FINDINGS
- Recipe A: exit 0; mapped=knowledge_files=72, rules 9/9, coverage/depth 10.0/10.0, missing/dangling empty; stdout sha256 `258dc869…` = TB1's independent lane-B run (`TB1.md:12`).
- Token set: 72 tokens; digest `c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0`; stdout sha256 `f0d274ba…`.
- CA6 final census (`receipts/`): exit 0 — exactly leg-1..10, all regular non-empty; per-receipt hashes recorded (leg-1 `24bfd90f…e2e91` = `receipts/MANIFEST.txt:1`).
- Variant (`receipts-B/`): exit 1 (AssertionError) at 19:03:48 — legs 1,2,4,6,7,8,9,10 present; leg-3 and leg-5 missing (lane B in flight; not a defect claim).
- Post-state: HEAD unchanged; `git status` identical pre/post (only `?? .ufo/interactive-sessions/`, `?? .ufo/waves/`); `git diff HEAD` empty.

## THREATS
"CB6" resolves to no artifact — my CA6 reading is an inference; if the parent meant a different census, a re-run is needed. I had read lane-A `receipts/census-pre.txt` before running (method location), which also exposed expected values: this reproduction is informed, not blind, although every value is recomputed from HEAD Git objects and hash-pinned. `receipts-B/` is a moving target (concurrent lane-B seats); only the 19:03:48 snapshot is claimed. The census measures repository state only — no battery-leg outcome claims.

## VERDICT
CLEAN — census reproduced at f0e8cde (Recipe A 72/72·9/9·10.0/10.0; token set 72, sha256 `c538284b…`; CA6 inventory PASS on `receipts/`; lane-B receipts 8/10 in flight). Note the CB6 label has no on-disk artifact; resolution stated in METHOD.
