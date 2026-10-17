## CLAIM
2nd opinion on debt 3 (PROVINCE conditional request-byte pin): the debt is real, the anchor is exact, and the integrate-worthy wording must (a) match the authority's phrase, (b) stay family-scoped, (c) satisfy the pending integration gates. The Lane-A-suggested wordings fail (c).

## METHOD
Primary sources first: full reads of `PROVINCE.md` and `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md`; anchors re-read via `git show HEAD:<path>` (HEAD `cfc84c2`; `git status` clean for tracked files). `grep -niE 'request byte|module identity|path-sensitive|re-deriv' PROVINCE.md` → exit 1 (debt real, no pin wording at HEAD). Cross-surface check of `HEAD:corpus/README.md:170` and `HEAD:corpus/QUALITY.md:25`. Only then read Lane-A V3/D3/F3/G3/R4/C4/X1 and simulated their gates in Python. No probes/MCP/network.

## FINDINGS
- Anchors exact: `PROVINCE.md:28-33` conventions paragraph, insertion after `:32` (agreed: V3.md:8, D3.md:10, R4.md:8); `HEAD:r9-02:146-169` = same evidence id across two paths (`ev_2262ac05…`, files differ at byte 108), subject-only rewrite → request byte-identical (`125cb2a9…e63cd`) → identical envelope; inference `:167-169`: "consumers must pin request bytes (or re-derive dossiers themselves), never just ids, when module identity matters." `README.md:170` + `QUALITY.md` rule 15 already carry the family-scoped rule → PROVINCE is the third surface, non-conflicting with the `:28-33` Core gate and `:58`.
- Conflict found: D3.md:10, V3.md:8, F3.md:11, G3.md:8 write "pin **the exact** request bytes"; `C4.md:25` asserts the literal substring `'pin request bytes'` — all four FAIL; F3 also lacks `'when module identity matters'` (X1.md:32 token gate FAIL). Python simulation (variants vs both gates): `D3 FAIL/F3 FAIL, V3 FAIL, G3 FAIL, VB3-rec PASS` (C4 substring PASS + X1 tokens PASS).
- Recommended minimal sentence (keeps D3's family scope and citation, uses the authority's own phrase at r9-02:168):
  "When module identity matters for an `analyze_function` probe, pin request bytes or re-derive the dossier; an evidence ID alone does not authenticate the `subject` module attribution (`corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`)."

## THREATS
- `/tmp/r9-*` scratch is gone; live REA is prohibited → authority is a HEAD-object read, not re-derived.
- Independence leak: a step-2 repo-wide grep spilled Lane-A snippets (C4/P2/R4/X1) before drafting; the PROVINCE/r9-02 primary reads preceded it, but full purity is not claimable.
- C4's gate is lexical, not semantic; my wording is chosen for authority fidelity first, gate compatibility second.
- If the parent integrates different wording, C4.md:25 must be revised to match it.

## VERDICT
FINDING: integrate the family-scoped sentence with literal "pin request bytes" (drop "exact") — the D3/V3/F3/G3 wordings as written fail C4.md:25's gate.
