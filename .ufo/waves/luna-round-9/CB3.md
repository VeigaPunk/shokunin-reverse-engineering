## CLAIM
Seat CB3, axis adversary 2 — independent pass on round 9's four freshness picks at HEAD `a280e07`: each pick's load-bearing evidence re-derived from primary sources, not from lane-A text, and the round invariants re-measured.

## METHOD
Read-only. Command A verbatim (`SCORECARD.md:92-123`, `REV=a280e07133f52f719b0805fc73c0b997e77b5062`, exit 0) → `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}`. `git status --porcelain --untracked-files=no` empty; `git diff --quiet HEAD --` rc 0; PROVINCE worktree vs `git rev-parse HEAD:PROVINCE.md` → `8a1cec88…ad47` both. sed/grep on r4-16, r12-01, PROVINCE:95-120, SCORECARD:74-84,534-559, r2/r3 jq entries, r4 `census-pre.txt`/report, lessons:145-155, l7/l8 recheck lines. Reproduced round-5's comma one-liner. No probes, network, `/tmp` access, or tracked writes.

## FINDINGS
- Invariants hold: 79/79 + 9/9 + 10.0/10.0; whole tracked tree byte-identical to HEAD; PROVINCE untouched.
- Item 1: stale two-site account stands at `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:751-752`; grep finds no `provider_blob_id`/`four sites`/supersession text in r4-16. r12-01:99-104 and :110-120 verified verbatim; A2's draft fields are exact. Delta: `P0.md:8`'s range `:97-114` truncates before the "numeral attributed, not re-derived" caveat (:117-118); landers must cite :110-120.
- Item 2: comma asymmetry reproduced — `'29,367,752' in n('x = 29,367,752')` → `False`; normalized needle → `True`. F18 debt is in r4 `receipts/census-pre.txt:29,71` and report :45-46. SCORECARD has no limits section yet (`grep 'Known instrument limits'` rc=1). B3's bounded-waiver guard stands.
- Item 3: control-doc `/tmp` refs are ephemeral/self-cleaning (`PROVINCE.md:48`, `SKILL.md:39-40`, `SCORECARD.md:497`); the four rechecks use `/tmp` cwd with pinned inputs; L7-01's npm cache pre-existence untested; no persistence requirement found. Historical `verify:` recipes and README held-bundle refs citing `/tmp` outputs (`r12-01:40-42`; `corpus/README.md:51,127,134`) are provenance debt; no deletion authority exists in any draft.
- Item 4: `PROVINCE.md:114-116` refusal verbatim; additionally :100-102 refuses labeling samples malicious/benign — retaining "benign", even scoped, conflicts with two refusal loci. Bleed: r2 :12,:217,:219,:236-237; r3 :60,:136 (other four jq entries: 0 tokens). `SCORECARD.md:79` and lessons:152 still cite stale :107-109. D2's scope omits :12/:219; D3's replacement shape is safer.

## THREATS
No `/tmp` inventory; "7 values" not re-derived (receipts gone, :117-118); cold-cache npx untested; wave files mutate concurrently; nothing is landed, so post-append command A and byte-identity remain unverified by anyone.

## VERDICT
FINDING: picks' evidence independently re-verified with no falsification, but item 4 must scope r2 :12/:219 (and disposition r3 :60/:136 against both refusal loci), P0's :97-114 pointer truncates the attribution caveat, and with zero landings freshness remains unproven at `a280e07`.
