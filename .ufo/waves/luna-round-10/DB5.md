## CLAIM
Ledger adversary (DB5): complete lane A's broken debt chain (D6@22:32 outran D4@22:33; D4 outran D1/D3@22:35/22:34 — no D1–D6 merge exists) and adjudicate which carried items must outlive the arc.

## METHOD
Merged D1–D5 with lane-A outputs; primary checks at HEAD `c343939`: `git diff --numstat <c>^ <c> -- SCORECARD.md LOG.md` for all nine records commits; `sha256sum .ufo/waves/luna-round-2/receipts/L7-mcp-tools-6.5.0.txt` → `dc740c46…`; `git show 3395b6d:corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md | grep -c 'rea-agents@6.5.0'` → `0`; `ls .ufo/waves/luna-round-{4..9}/*.md | wc -l` → 64/126/127/127/100/121; read-only sibling reads (Tameshi, tsukuroi); `PROTOCOL.md:415-450`, `.ufo/l0-questions.md:42`. Read-only elsewhere.

## FINDINGS
- Chain gap: D1–D5's union omits lane-A finds: six prose-decorated MANIFEST verdicts (`MANIFEST.json:2791,2805,2819,2846-2847,2860`); r8/r9 roster gaps (disk 100/121 files; `ZB4.md:10-18` 91/128 snapshot, no roster); r7's C9 gate failure (never in its report; literal absent per grep above).
- Rewrite census: LOG 0 deletions in all nine records commits; SCORECARD deletions in five — r1 `a4bd355` 4, r2 `a9580eb` 8, r3 `0772d54` 7, r4 `cfc84c2` 1, r7 `6e2ee8f` 1 (coverage row 72/72@2abd30f5→78/78@3395b6d). Lane A listed 2/3/4/7; r1 also qualifies (WB1/WB3 concur). Criterion-vs-contract adjudication is parent/operator (PROTOCOL:447 names LOG only).
- Unrepaired, confirmed: B2 L7 hash vs `dc740c…`; `SCORECARD.md:68-72` pointers stale again (README:160/:128 → actual :177/:138; README=187 lines); r3-jq bleed (:60,:136); K1 sibling items hold (`verification-patterns-fleet.md:73,102`; tsukuroi `PROVINCE.md:42`).
- **Must outlive the arc:** (1) SHONEN 4×[~] (no named non-author verifier); (2) integrator/operator rulings — ADJ-06 ownership (L0:42), MANIFEST enum repair authority, r7 SC1–SC6 convention, census-instrument retest; (3) dispatch/roster proof — r6's wire-audited 127/128 permanent, r5 126≠128 disk, 5/9 short-counts; (4) SCORECARD 5/9 rewrite disclosure/adjudication; (5) Tameshi stale formula — sibling-owned correction; (6) /tmp litter 16 roots ~1.096 GB (N3); (7) execution-blocked debt — C05, `jmp *`, R8 pre-pair, cold-cache/archival caveats, r3 bleed/stale pointers.
- **Retirable now:** /tmp-persistence dependency; r2-file jq "benign" (qualified r9); R1 map/README debt; C7 pointer content.

## THREATS
Disk counts are snapshots, not rosters (no wire audits r4/r5/r8/r9). No closure citation ≠ proved open. DB1/DB3/DB4 and integrator notes may land after this read (only DB2 visible); re-merge before finalizing.

## VERDICT
FINDING: seven classes must outlive the arc (SHONEN verifier; ADJ-06/enum/auxiliary/retest rulings; dispatch proof; rewrite adjudication; Tameshi correction; /tmp litter; execution-blocked debt); /tmp-persistence, r2 jq, R1 debt, C7 pointer retire.
