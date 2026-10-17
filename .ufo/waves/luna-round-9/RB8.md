## CLAIM
X1's round-9 SHONEN assessment — all four boxes remain `[~]`, none promotable, no eligible non-author verifier — is accurate at HEAD `a280e07` and consistent with the box record of rounds 1–8. Two citation-scope nuances do not move any box.

## METHOD
Read X1, SHONEN.md, SKILL.md, PROVINCE.md, LOG.md, SCORECARD.md, `PROTOCOL.md:63-73`; compared box statements in `.ufo/reports/luna-round-{1..8}/kaidoku.md`; box history via `git show <rev>:SHONEN.md`; re-ran command A (`SCORECARD.md:92-123`, `REV=a280e07`) → `{"citation_resolved_rules":9,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":79,"mapped":79,"missing":[],"rule_blocks":9}`; `git diff --name-only HEAD` empty. Text-only; no probes; only write this file.

## FINDINGS
- Box continuity: r1:72-83, r2:70-78, r3:70-75, r4:70-74, r5:69-73, r6:69-74, r7:58-61, r8:53-55 all record `[~]`×4; SHONEN.md has been `[~]`×4 since `c265db9` (the `[x]` at `b04b19e` were reconciled down there); X1 retains `[~]`×4, no promotion. Consistent.
- X1 citations resolve: LOG.md:464-472 (open→decode→export→close, durable bundle); PROVINCE.md:114-116 (safety/trust refusal); jq-shadow `:217,236-237` ("benign" occurrences); SCORECARD.md:24 (9/9 is queue-drain rules at `638fb211`) and :45 (C5, contested province accuracy); PROTOCOL.md:63-68 (non-author `[x]` rule); box 3 cites `SKILL.md:30-40,42-66` verified as working contract + decision table.
- Nuance (box 1): "those blocks lack explicit source pointers" is over-broad — `SKILL.md:76` carries `GhidraClient.js:607` (external file:line). Decision table (:42-66) and checklists (:197-205) do lack resolvable pointers, so the strict bar (`PROTOCOL.md:69-70`) still fails.
- Nuance (box 4): X1 names loci `:217,236-237`; later seats (Q4/VB4/RB4, 21:52–22:00) scope four loci `:12,:217,:219,:236-237`. Snapshot difference (X1 21:48), unchanged disposition.

## THREATS
r5 XB2.md:4 counts "three" SHONEN boxes where SHONEN.md lists four (the r5 report itself records ×4) — prior-round wording variance, no box impact. X1 predates RB4/VB4; "D2 only proposed" still true (nothing landed, `git diff` empty). I did not re-derive jq byte-identity, re-run the smoke, or probe anything live.

## VERDICT
CLEAN — X1's `[~]`×4 retention is accurate and matches rounds 1–8; two citation-scope nuances recorded, neither changes a box.
