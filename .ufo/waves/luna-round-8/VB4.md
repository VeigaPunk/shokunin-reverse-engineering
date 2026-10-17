# VB4 — receipt verifier: legs 9-10 (Lane B, deepseek-v4.1-flash)

## CLAIM
All leg-9 and leg-10 receipt claims re-derive true: the six ABSENT greps, the 170-name input provenance, the L10 control RESULT with the analyze-not-found fallback recorded, and both displayed raw blocks reproduce their claimed SHA-256s. The sole MANIFEST deviation (leg-10.md) is a post-manifest append, not content corruption.

## METHOD
- `sha256sum` of all 10 receipt files vs `receipts/MANIFEST.txt`; exact-prefix search `for n in $(seq 1 84); do head -n $n leg-10.md | sha256sum; done`.
- Re-ran each `grep -nFw -- <name> .ufo/waves/luna-round-8/receipts/leg-2-tools.txt` (exit/stdout/stderr/stdout-hash); added substring (`grep -cF`) and case-insensitive checks.
- `sed -n '14,15p'` / `sed -n '44,48p' leg-10.md | sha256sum`; hashed surviving /tmp artifacts; python3 JSON-parse of `/tmp/kaidoku-luna-round-8-leg10.stdout` tools list vs `leg-2-tools.txt`.

## FINDINGS
- Leg-9 (hash 8377d652…, stable across MANIFEST and census-pre.txt): all six greps rc=1, empty stdout/stderr, hash `e3b0c442…` (empty string) — exactly as claimed; substring count 0, case-insensitive none. `leg-2-tools.txt` = 170 unique lines, set-equal to the 170 names parsed from `/tmp/kaidoku-luna-round-8-leg10.stdout` (SHA-256 `23e94d0b…`), the session cited at leg-10.md:26.
- Leg-10: MANIFEST says `c89eea7a…`, file hashes `6cd389e9…`; `head -59` hashes exactly `c89eea7a…` — lines 1-59 intact, lines 60-84 ("EX10 … fallback") appended after MANIFEST was written (mtime 21:14 vs 21:02). Append-only, no prior bytes altered.
- Display blocks verify byte-exact: lines 14-15 → `61450b92…` (= /tmp/kaidoku-luna-round-8-leg10-summary.stdout; line 20 stderr matches summary.stderr), lines 44-48 → `6abdf805…`. No leg-3-class display defect in either leg.
- Control id:2 = RESULT (parent_operation `inspect_binary_layout`, coverage 202/202); `analyze` → `-32602 "Tool analyze not found"`, fallback frames open_binary/binary_overview/close_binary all RESULT — recorded at leg-10.md:45-48 and EX10.md:5,8.
- Legs 3-8 refused exactly the six verbs leg-9 tests (go/rust/electron_fuses/sqlite/search_bytes/objdump).

## THREATS
No independent raw artifact for `6abdf805…`; /tmp/cb8-verify/block-ex10.txt is byte-identical to leg-10.md:44-48, i.e. derived from it, not independent. No live re-execution (read-only seat). census-pre.txt omits leg-10.md and its leg-3/leg-4 hashes disagree with MANIFEST/current files (outside my two legs; flagged for parent). MANIFEST entry for leg-10.md is stale.

## VERDICT
FINDING: leg-10.md MANIFEST hash is stale — the file was extended after hashing (prefix lines 1-59 prove the covered length intact); all leg-9/leg-10 content claims verify.
