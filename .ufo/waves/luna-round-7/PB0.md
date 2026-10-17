## CLAIM
Lane-B plan: quality gates, attacks, and citation verification for the six 6.5.0-verb entries. This seat runs no gate on a landed corpus and writes only this report; nothing here promotes to Core.

## METHOD
Read-only review at HEAD `411175e`: P0, N1/N2, E1-6D/V, G/Z, M/K rows, round-6 receipts and SC/CC scouts. Reproduced Command A from Git objects: `{"mapped":72,"knowledge_files":72,"missing":[],"dangling":[],"citation_resolved_rules":9,"rule_blocks":9}`. In-memory dry-run (no writes): six hyphenated stems + six hyphenated map-row tokens → `mapped=78, knowledge_files=78, missing=[], dangling=[], coverage 10.0`; underscore tokens → `mapped=72, coverage 9.23`, six missing + six dangling (`2026-10-16-l7-0N-inspect`…). Receipts legs 3–8 (both lanes) are HEAD-tracked (`git ls-tree -r HEAD -- .ufo/waves/luna-round-6`); SC1–6, CC*, and all round-7 drafts are untracked.

## FINDINGS
Lane-B protocol per seat:
1. Stem gate — filename, map row, Knowledge row must use N1's hyphenated stems (`N1.md:16`). M1's map rows and K3/K4's Knowledge rows propose underscore tokens (M2's rows use hyphens); K4's "matcher blocks 78/78" holds only for those — hyphenation fixes it with Command A untouched.
2. Content gate — QUALITY criteria 1–15 per entry, plus `source:`/`verified-at:`/`recheck:` headers (`/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:17`; `G3.md:14-15`) — absent from all 72 prior entries, so new entries only; RESULT-class wording, never Core promotion; absolute path + SHA-256.
3. Citation gate — recompute each cited receipt blob hash at the integrated revision; treat untracked scouts as auxiliary (G3's SC3 note); check `path:line` ranges, not seat prose.
4. Rulings — entry 2 keeps Signal `.node` (`1b44ed…d1f7`, lane A) and `/usr/bin/rg` (`d006ac…ae42`, lane B) as distinct observations; entry 4 is B-only (`/tmp/bb6-leg-6/sc4-index.db`, `3701a7…9728`), excluding lane A under criterion 12.
5. Landing census — Command A at integrated REV: 78/78, `[]`/`[]`, 9/9, 10.0; `git diff --name-status 411175e..REV -- corpus/knowledge` = six additions only; SCORECARD.md/SKILL.md unchanged.
6. Attacks — (a) E5D/M2 write `search_bytes(...,limit=100)` but both recorded requests send only `{"pattern":"7f 45 4c 46"}` (`receipts/leg-7.md:9`; `receipts-B/leg-7.md:22`); limit 100 is the tool-reported default (`receipts-B/leg-7.md:60`). (b) "E1V absent" (`E1D.md:2`) and Z2/Z5 absence claims are stale races — judge final artifact bytes/hashes. (c) K4's "79 rows" includes the non-corpus `lessons/round-13-distillation` row (`corpus/README.md:131`) — not a Command A input.

## THREATS
The dry-run is set-algebra, not a landed run. Untracked lane-A reports remain mutable. No live-probe authority this round; entry 6 provider version is null; Command A is semantic-blind.

## VERDICT
CLEAN — lane-B gates and attacks specified; nothing landed; two items routed to parent (underscore rows must be rewritten; `limit=100` wording corrected).
