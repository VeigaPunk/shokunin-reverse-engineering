## CLAIM
Adjudicate CA1–CA8: which findings stand, which are superseded, any false alarms.

## METHOD
Read CA1–CA8, RV6/RV8, SC1–SC6, PROVINCE.md, round-2/round-5 precedents, all ten receipts' structure and commands, MANIFEST/census-pre, receipts-B/leg-1, live `~/.npm` logs. Read-only; no battery re-run. Commands: `sha256sum receipts/leg-1.md` (24bfd90f… = MANIFEST value); `printf '6.5.0\n' | sha256sum` → 3eb8e06…; per-receipt grep for `rea-agents@[0-9.]*`; `git status --porcelain`; `find ~/.npm/_logs -newermt "2026-10-16 18:14"`; word-boundary `hold` count on leg-2.md (=2, matching CA2).

## FINDINGS
**Stand, citations verified:**
- CA2 CLEAN — PROVINCE.md:28-35 available≠held; PR1.md:2, PR2.md:23, P0.md:2,11 deny promotion; leg-2.md:1,6 count 207; leg-9 typed refusal.
- CA5 CLEAN — HEAD f0e8cde tracked-clean (untracked `.ufo/` only); PROVINCE.md:8-24/38-70; corpus/README.md:11+ map; SCORECARD.md:88+ command A source-derived; round-5 `X1.md:40-50`/`census-pre.sh:34-40` match (72-token set).
- CA1/CA3/CA8 provenance limits — leg-1 digest recomputes; receipts self-report only (stdout sha256, no input hash/process identity; MANIFEST hashes receipt files); predictions exposed (dispatch; PS4.md:8) and even printed in receipts-B/leg-1.md:41-45; no signed prereg artifact exists. No actual forgery/tailoring evidence.
- CA4/CA6 carve-out — live-confirmed: `~/.npm/_logs/2026-10-16T22_02_19_051Z-debug-0.log:9,18` records a wave probe (`argv exec … rea-agents@6.5.0 mcp`, `cwd /tmp/rea-bb3`) writing home logs at 19:02 despite cwd=/tmp. Literal "zero host mutation outside /tmp" (PR2.md:23) unsatisfiable — receipts are mandated repo writes; P0.md:11's "execution-generated" phrasing is the usable scope.
**Superseded (correct at snapshot, not now):** CA7 — receipts absent then; now 10/10 present (mtime 18:16–18:29) and CA7's specified audit passes: every leg command pins rea-agents@6.5.0, zero 6.4.0 (recorded-command level; self-report caveat per CA1).
**False alarms:** none found. Snapshot note: MANIFEST.txt (74 B) hashes only leg-1; CA6's census gate remains prospective.

## THREATS
CA2's claimed read list (leg-4/6/8/9) predates those files' current mtimes (18:25–18:28 vs report 18:23) — unreconciled; concurrent seats wrote during review (dir mtime moved; logs 19:01–19:02). Judgments snapshot-bound.

## VERDICT
CLEAN — CA1–CA8 findings stand or are snapshot-superseded (CA7); no false alarms; CA4/CA6 caveat live-confirmed.
