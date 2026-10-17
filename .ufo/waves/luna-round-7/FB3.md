## CLAIM
Format audit of the landing texts for entries 5 (`search_bytes`) and 6 (`inspect_with_objdump`): stem grammar vs ruling (a), house metadata vs ruling (d), README row shapes/anchors, Command A mapping, RESULT/no-Core language. Read-only; only this file written.

## METHOD
Read E5D/E5V/G5/Z5/Q5, E6D/E6V/G6/Z6, M2/K4/N1/P0–P2/T2/F3; `corpus/QUALITY.md`, `corpus/README.md:11,61,63,131,141`, `SCORECARD.md:94-123`, `/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:17-19`; `git ls-tree`/`git show` at HEAD `411175e`; line checks of `receipts/leg-{7,8}.md` and `receipts-B/leg-8.md`; in-memory Command A run (unmodified body) with six hyphen vs underscore stems. No probes/network; `git diff --quiet HEAD` still true.

## FINDINGS
- Token grammar (ruling a): hyphen-stem simulation → `{"knowledge_files": 78, "mapped": 78, "missing": [], "dangling": [], "citation_resolved_rules": 9, "coverage_score": 10.0}`; underscore stems → `mapped=72, missing=6, dangling=6, coverage 9.23`. Land `2026-10-16-l7-05-search-bytes` / `-06-inspect-with-objdump`: E5D.md:2, E6D.md:10,21,23, M2.md:11-12,16-17, N1.md:16, P0.md:8 are already hyphen. `K4.md:11-12` proposes underscore rows for 5–6 — do not land as-is; T2.md:12/P1.md:17-18/F3.md:6 are diagnostic texts.
- Metadata (ruling d): E6D.md:12-14 carries `source:/verified-at:/recheck:`; E5D.md has none (`grep -c source:\|verified-at:\|recheck:` → 0) — entry 5 needs a title plus the three fields; its sources otherwise resolve (E5D.md:2,8 cite tracked receipts).
- Rows/anchors: map rows append after r14-02 (`README.md:61`) before `## Knowledge` (`:63`); Knowledge rows before `## Lessons` (`:141`, last row `:131`). M2's 3-cell map and 4-cell Knowledge rows for 05/06 conform, as do E6D.md:21,23.
- Citation precision (entry 5): E5D.md:5 cites `leg-7.md:3-12` + `receipts-B/leg-7.md:21-25` for "Ghidra 12.1.4, default auto-analysis", which sit at `leg-7.md:13,21`; the request passes no `limit` (`leg-7.md:9`) — `limit:100` is the echoed default (`:13`). Entry 6's cites resolve (`leg-8.md:8-14` request→summary→stdout hash→exit, `:19` id:2 frame; `receipts-B/leg-8.md:41-55` compare).
- RESULT/no-Core language is present (`E5D.md:11`, `E6D.md:2`, `M2.md:5`); entry-6 text keeps B's primary `~/.local/bin/jq` carrier distinct (`E6D.md:17`; `G6.md:9`).

## THREATS
Drafts are worktree-only; line numbers shift if edited. SC5/SC6 cited by M2 are untracked at HEAD (`git ls-tree`), unlike the leg-7/8 receipts — prefer receipt citations in landed text. The simulation verifies token mapping only, not row prose or the README edit. Soft nit: E6D.md:16's "reproduced the Evidence ID" is a cross-run id-identity statement; if kept, name the domain (`QUALITY.md:25`; `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146`).

## VERDICT
FINDING: entry 5 lacks title and house metadata fields (use M2's rows); K4's underscore rows for 5–6 must not land (hyphen forms yield the exact 78/78/10.0 Command A result); entry 6's draft is landing-shaped subject to the two citation touch-ups.
