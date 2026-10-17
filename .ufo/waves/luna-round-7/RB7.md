## CLAIM
After +6 rows the count story is coherent: 73 rows over 72 files at HEAD `411175e` becomes 79 rows over 78 files; the constant delta of 1 is the pre-existing lessons-only row.

## METHOD
Read-only: `git show 411175e:corpus/README.md`; `git ls-tree -r 411175e -- corpus/knowledge`; Command A source `SCORECARD.md:92-123`; round-7 K3, K4, M1, M2, L1, P0, C5, N1, N2, Z1-Z6; round-6 `receipts/census-pre.txt`. Parsed README sections with python3 using Command A's map regex (`SCORECARD.md:101-102`). No live probes; only this report written.

## FINDINGS
- Baseline: 72 `corpus/knowledge/*.md`; coverage-map token set equals the file-stem set exactly (72), matching `census-pre.txt:11`. `## Knowledge` (`README.md:63-139`) holds 73 data rows: 72 file-backed (one row per stem, no duplicates, no stem without a row) plus the single non-file row `lessons/round-13-distillation` (`README.md:131`). Exact parse output: `baseline rows=73 files=72 file_backed_rows=72 nonfile=1; projected rows=79 files=78 delta=1`.
- Projection: +6 file-backed rows ⇒ 78 files / 79 rows; delta stays 1. No round-7 draft adds a second non-file row or a Lessons row (`L1.md:11`, `P0.md:8`, `C5.md:8` all preserve the lessons token/position).
- Command A interaction: its map scan ends at the next `## ` heading (`SCORECARD.md:101`), so Knowledge rows appended before `## Lessons` (`README.md:139-141`) cannot alter `mapped`/`missing`/`dangling`; rows=79 and 78/78 coexist without contradiction.
- Condition: row→file correspondence needs hyphenated stems (parent ruling a). `K3.md:8-10` and `K4.md:10-12` as drafted use underscores (`…inspect_go_binary`), which would match no file; hyphenated forms are already in `M1/M2/E4D/E6D/P0`. The row total is 79 either way.

## THREATS
Projection is in-memory, not post-landing; that no draft adds rows beyond the six is unverified until integration. Command A never reads the Knowledge table (`C4.md:2,14`), so a duplicate or omitted row would not fail it — count coherence depends on the N1 row gate. Filesystem counts include `.gitkeep` (`ls -a corpus/knowledge` = 75 entries, 72 `.md`), so file counts must be `.md`/`git ls-tree`-derived.

## VERDICT
CLEAN — 73→79 rows for 72→78 files is coherent (delta = `README.md:131` lessons-only row), conditional on hyphenated row stems at landing.
