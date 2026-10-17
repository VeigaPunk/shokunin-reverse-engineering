## CLAIM
Final item-4 text, gated through Z4 + Q4 + VB4: the append-only qualification scopes all four recorded bleed loci to the recorded byte-identity finding and disavows safety/trust/license verdicts; history and PROVINCE stay untouched.

## METHOD
Read `.ufo/waves/luna-round-9/{Z4,Q4,VB4,D2,D3,D4,H}.md`. At HEAD `a280e07133f52f719b0805fc73c0b997e77b5062` (`git rev-parse HEAD`): `git diff --exit-code -- corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md PROVINCE.md` → clean; `wc -l` → 242; `grep -nE 'benign|Benign|safe|trust|malicious|compromise|legit'` on the r2 file → lines 12, 217, 219, 236, 237; `grep -cE` containment → r2 4, r3 2, other four jq entries 0/0/0/0. Command A (`SCORECARD.md:93-123`, `REV=a280e07…`): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}`. No probes, network, or `/tmp`.

## FINDINGS
Final item-4 text — append after `:242` (blank line before), nothing else changes:

```
- **Safety-verdict scope (round 9):** The phrases "Benign payload" (`:12`), "benign payload, genuine artifact" (`:217`), "not binary compromise" (`:219`), and "benign, intentional agent-installed" (`:236-237`) are historical wording, not a present endorsement or a safety/trust verdict. Folded back to the recorded evidence, they assert only that no byte difference from the cited upstream artifact was recorded — the SHA-256 byte-identity match to the upstream jq-1.8.2 `jq-linux-amd64` release artifact (`:10-13`, `:204-219`) — and that the install was recorded as agent-initiated (provenance chain: `2026-10-13-r3-jq-provenance.md`). The lane never answers whether an artifact is "safe, trustworthy, or licensed for reuse" (`PROVINCE.md:114-116`); nothing here asserts that the artifact or its upstream is uncompromised, safe, trustworthy, or reusable. This note qualifies, and does not rewrite, the historical text.
```

Adjudication: Z4/D2 named only `:217`,`:236-237`; Q4's `:219` and VB4's `:12` gaps are closed by naming all four loci. Per H/Z5, the note disavows "benign" as a verdict (D3's warning) while qualifying, not rewriting (D1/D2). Residuals outside this landing (parent adjudication): r3 companion bleed (`2026-10-13-r3-jq-provenance.md:60,136`); stale refusal pointers to `:107-109` at `SCORECARD.md:79` and `corpus/lessons/2026-10-15-round-1.md:152-153`; `SCORECARD.md:77-80` debt note now addressable.

## THREATS
Text-only; recorded sha256/provenance not re-derived; no probe of `~/.local/bin/jq`. If the parent prefers D3's replacement wording or extends scope to r3, the text must be amended. Not applied here: corpus and PROVINCE remain byte-identical to HEAD.

## VERDICT
FINDING: item-4 final text ready (above, after `:242`); Q4/VB4 scope gaps closed; r3 bleed and stale `:107-109` pointers flagged, unresolved here.
