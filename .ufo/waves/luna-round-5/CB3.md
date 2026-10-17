## CLAIM
Independent analysis of command A impact for all seven planned round-5 edits (five knowledge appends, `PROVINCE.md`, `corpus/README.md:131,163`): command A cannot regress under the planned edits; the "no rule cites the edited files' tail regions" check has exactly one benign exception.

## METHOD
Drafted from primary sources only, then cross-checked Lane A. Reproduced command A (`SCORECARD.md:92-123`) with `REV=cfc84c226bb8755c15fcdc342e27de7654c6fcb8`, git-object reads only. Re-parsed the craft section with the recipe's own regex to enumerate every citation to the five edited files against their lengths (91/119/194/375/108). Located README's scanned region by headings: `## Coverage map` at :11, next `## ` at :63 → lines 12-62; edit sites :131 (`## Knowledge`) and :163 (`## Frontier`) are outside it. `git status --porcelain`: no tracked modifications.

## FINDINGS
1. Appends (5 files) only grow `len(splitlines())`; the bounds check `1 <= start <= end <= count` is monotone in growth — it cannot break. No craft rule cites `asar-surface` or `r4u-01-firmware-deep` at all.
2. Tail check: exactly one exception — rule 8 (`SKILL.md:186`) cites `2026-10-14-r12-01-queue-b-ready.md:105-108`, file length 108 (end == EOF). Other maxima stay interior: r5-02 :146/194, r9-02 :272/375. Appending at EOF leaves lines 105-108 byte-stable and the bound valid → 9/9 unchanged.
3. README edit targets lie outside lines 12-62, so the token-scanned section and 72-token set cannot move; removing the :163 bullet shifts only later lines, and extraction is heading-based.
4. `PROVINCE.md` is not a command A input (inputs: README, SKILL.md, `git ls-tree … corpus/knowledge`) — zero impact.
5. Baseline reproduced verbatim: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "revision": "cfc84c22…", "rule_blocks": 9}` — matches P0:5, R5:8-13, X1:54, TB1:12.
6. Convergence: C3 reached the same tail-citation conclusion independently; no seat contradicts. (Drafted pre-read.)

## THREATS
Pre-edit measurement — parent must rerun command A at the post-integration revision. Command A checks bounds, not citation semantics: any mid-file insertion (invariant violation) shifts content under a still-green citation. r12-01 is the sensitive file — its erratum subject (:99-108) sits in its final 10 lines, so a near-subject insertion would silently mispoint rule 8's :105-108.

## VERDICT
FINDING: exactly one craft citation touches an edited file's tail — SKILL.md:186 → r12-01:105-108 (end == EOF 108); harmless only if the r12-01 erratum is EOF-appended and lines 105-108 stay byte-identical. All other six edits are command-A-neutral.
