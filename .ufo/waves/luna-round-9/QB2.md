# QB2 — quality gate, items 3–4 (lane B)

## CLAIM
Independent lane-B quality gate over the item-3 `/tmp`-dependence audit + hygiene proposal and the item-4 jq-shadow "benign" qualification, plus the invariant guard, at HEAD `a280e07`. Item 3 passes with labeled limits; item 4's landing text is incomplete.

## METHOD
- `git rev-parse HEAD` → `a280e07133f52f719b0805fc73c0b997e77b5062`; `git diff --quiet HEAD --` clean; PROVINCE sha256 `fe7f3f61…3b37c1c` == HEAD blob.
- Command A replayed verbatim from `SCORECARD.md:93-123` at HEAD → `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}`.
- Sed/grep checks: `SKILL.md:39-40`, `PROVINCE.md:48,114-116`, `verify-recovery.py:120-128`, four `/tmp` rechecks, `r3-renderer-asar.md` /tmp lines, r2/r3 benign/compromise tokens, `SCORECARD.md:77-80,453-460,495-498`.

## FINDINGS
- Item 3 — CLEAN-with-limits. No current lane control requires `/tmp` persistence: `verify-recovery.py:123` puts its fixture under `HERE`; the four current rechecks use `/tmp` as cwd/cache with stable absolute inputs; L7-01 cache necessity untested (no `--offline`). Legacy `verify:` recipes do consume persisted artifacts (`r3-renderer-asar.md:11,18-19,34-35,58`); RB3 calls them archival limits. Hygiene proposal stays operator-owned; no deletion proposal exists in the wave (CB6 sweep; `P1.md:12`), and none occurred.
- Item 4 — FINDING. Verified bleed: `:12` "Benign payload", `:217` "benign payload, genuine artifact", `:219` "not binary compromise", `:236-237` "benign, intentional agent-installed"; r3 adds `:60,:136`. The Z4/D2 landing text names only `:217`/`:236-237`. `SCORECARD.md:79` and `corpus/lessons/2026-10-15-round-1.md:149-153` still cite the stale `PROVINCE.md:107-109`.
- FB2's claim that `:217`/`:236-237` are "the file's only 'benign' occurrences" is false (case-sensitive miss; `:12` omitted) — a lane-B receipt defect reinforcing the scope gap.
- PROVINCE refusal `:114-116` confirmed verbatim; tracked tree byte-identical to HEAD.

## THREATS
Pre-integration snapshot: no append has landed, so post-landing append-only/non-target byte-identity must be re-measured at the landed revision. Underlying sha256/provenance claims and cold-cache behavior were not re-run. D3's replace-vs-scope dispute and the r3 extension are parent adjudications. The FB2 miss shows receipt claims need case-aware review.

## VERDICT
FINDING: item 3 sound with named limits; item 4 landing text must cover r2 `:12` and `:217-219` (parent to rule on r3 `:60,:136`) and refresh stale pointer records before append; command A 79/79 + 9/9 and byte-identity hold.
