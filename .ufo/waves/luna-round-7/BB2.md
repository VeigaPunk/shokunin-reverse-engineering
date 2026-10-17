# BB2 — command-A full simulation (lane B backfill)

## CLAIM
Command A's exact logic at HEAD `411175e` + the six hyphenated l7 entries/rows prints `knowledge_files=78, mapped=78, missing=[], dangling=[], 9/9 rules, 10.0/10.0`. BB1.md absent at run time (checked 20:38:06), so this seat simulated the six hyphenated stems + six hyphenated map tokens itself.

## METHOD
Read-only; no network/probes. `git clone --no-hardlinks` of the lane repo → `/tmp/bb2-sim/repo`, `checkout --detach 411175e`. Command A body extracted verbatim (`sed -n '93,123p' SCORECARD.md` → `cmdA.sh`). Control at `411175e`: `{"knowledge_files": 72, "mapped": 72, "citation_resolved_rules": 9, "rule_blocks": 9, "coverage_score": 10.0, "depth_score": 10.0, "missing": [], "dangling": []}`; README blob sha256 `9112c05b805b1d5abe494ff02c57ed350ab6567d8de945629361f33db861e12e` = RB6:8 pin. Overlay: six stand-in files `corpus/knowledge/2026-10-16-l7-0{1..6}-{inspect-go-binary,inspect-rust-binary,inspect-electron-fuses,inspect-sqlite-database,search-bytes,inspect-with-objdump}.md` (bodies copied from peer draft `d39ff53`; command A is body-invariant — reads only ls-tree names, the Coverage-map section, and SKILL-cited files, cf. RB5:14) + six 3-cell map rows inserted after the r14-02 row (`:61`) + six 4-cell table rows after the r4u-06 row (`:139`); commit `844674774b56f64b6d35043259c3ca0134e61819` (parent `411175e337c0725ae9bee3fd478ae9bf05bedf3f`). Ran `REV=844674774b56f64b6d35043259c3ca0134e61819 bash cmdA.sh` from the clone; independent token/pipe audit.

## FINDINGS
- Command A @ `8446747`: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 78, "mapped": 78, "missing": [], "revision": "844674774b56f64b6d35043259c3ca0134e61819", "rule_blocks": 9}` exit=0 — all targets met (78/78, 9/9, 10.0/10.0).
- Map rows `README.md:62-67`: pipes=4 → 3 cells each; table rows `:146-151`: pipes=5 → 4 cells each; each row's token equals its exact stem.
- Coverage-map tokens 78 occurrences / 78 unique == 78 knowledge stems; `missing=[]`, `dangling=[]`. `git diff --name-status 411175e 8446747 -- corpus` → `M corpus/README.md` + six `A` knowledge files only (prior 72 untouched).

## THREATS
Scratch commit in /tmp, not the landing — parent must re-measure on the real integration commit. Entry bodies are peer-draft stand-ins; content/QUALITY admission stays with other seats. My stems match XB1.md:56-63 (canonical census) and the three reported sims (PB1:7).

## VERDICT
CLEAN — command A re-measured 78/78, 9/9, 10.0/10.0 in a fresh scratch commit on parent 411175e; twelve new rows cell-verified (6×3-cell map after r14-02, 6×4-cell table).
