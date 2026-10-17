# DB2 — derivability, round-9 items 3-4

## CLAIM
Item-3 drafts (C1/C2/S3/Q3/C4/R5) are source-derivable at HEAD `a280e07`; every spot-checked citation reproduces. Item-4 (D2/Z4/Q4) has one completeness defect: the r2 entry's `:12` "Benign payload" escapes every cited locus, so Z4's "covers both 'benign' occurrences" claim is false as stated.

## METHOD
Read-only; no probes, network, `/tmp` access, or tracked-file edits. Commands: case-insensitive sweep `benign|compromise|safety|trustworthy|licensed` over `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md`; `grep -rn "^recheck:" corpus/knowledge/` → 7 hits, all l7/l8; line-window reads of `SKILL.md:39-40`, `PROVINCE.md:48,114-116`, `SCORECARD.md:495-498`, `PROTOCOL.md:341-343`, `verify-recovery.py:120-129`, all seven recheck `:5` lines, `r3-renderer-asar.md:11,19,35`, `r12-01:40-42,112-120`, `r14-01:12-17,45-48`, `r8-01:255-271`, `r9-02:366-375`, `SB1.md:12-23`, `SB3.md:12,16`, r6 report `:25-29,64-65`. Command A at literal rev `a280e071…` → `{"citation_resolved_rules":9,"coverage_score":10.0,"depth_score":10.0,"knowledge_files":79,"mapped":79,"missing":[],"dangling":[]}`; `git diff --name-status HEAD --` empty.

## FINDINGS
- Item 3: all cited lines reproduce verbatim; the seven `recheck:` fields are exhaustively l7/l8 (C1's enumeration complete for that field type). Historical `verify:` recipes consuming `/tmp` are broader than the drafts' examples — add `r8-01:268-271` (consumes the r4-09-era `/tmp/cmp-mini-config-in.json`, 115,987 B "unchanged"); also `r12-01:41`, `r14-01:45-48` — all correctly quarantined as legacy; no draft authorizes deletion.
- Item 4: four bleed loci — `:12`, `:217`, `:219` ("not binary compromise"), `:236-237`. `Z4.md:12`'s "covers both 'benign' occurrences (`:217,236-237`)" is refuted by `:12` "Benign payload" (capital-B, absent from every citation set); Q4 caught `:219` but not `:12`; D2's citing sentence restricts loci the same way.
- `PROVINCE.md:114-116` confirmed as the current refusal; the prompt's `:107-109` pointer confirmed stale. D3's r3 bleed citations (`r3-jq-provenance.md:60,136`) exact.

## THREATS
Absence claims are grep-bounded, not proof; legacy `/tmp` inputs' current existence is unverified (drafts disclose this). D2's entry-wide phrasing ("In this entry…") could implicitly cover `:12`; the integrator must settle wording. Static-only; no recheck was executed. Command A reads Git objects, not live surfaces.

## VERDICT
FINDING: item 3 derivable as drafted (enrich the examples list); item 4's append must cite `:12` and scope `:219` or "both occurrences" remains false.
