# EX-02 (c1, executor) — PRE-REGISTERED dry-run prediction, written BEFORE EX-01's patch landed

- Seat: EX-02 (chain c1, executor). Wave: arc3-loop1-round2. Date: 2026-10-19.
- Written at 2026-10-19T12:08Z; EX-01's claim directory was empty at write time
  (`find .ufo/waves/arc3-loop1-round2/claims/c1/EX-01 -type f` → no output).
- Baseline pinned: HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`, SKILL.md
  sha256 `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`,
  hull of command A = `{"citation_resolved_rules": 13, "rule_blocks": 13,
  "mapped": 82, "knowledge_files": 82, "coverage_score": 10.0, "depth_score": 10.0}`.

## Prediction rule (falsifiable, form-based)

Command A counts a craft rule as citation-resolved iff the rule block contains at
least one `corpus/knowledge/<name>.md[:start[-end]]` reference whose span exists
inside that file (`SCORECARD.md:105-117`). Therefore:

| EX-01 patch form | predicted command A | predicted depth_score |
|---|---|---|
| rule text cites ≥1 resolvable `corpus/knowledge/…md[:range]` | rules 14, 14/14 | 10.0 |
| rule text cites only wave-tree / incident paths | rules 14, **13/14** | **9.29** |
| patch rewrites any existing line of rules 1-13 | prior-13 byte-identity FAILS | n/a |

## Measured basis for the prediction (run before the patch existed)

`rule-resolution-probe.py` inserts each candidate block at the end of the craft
section (before `## Config custody for live-probe rounds (SOP)`, the split
boundary command A uses) and runs command A's exact resolution loop:

- `cand-T1.md` (incident-only, honest form) sha256
  `269bafed319a949cfde205bbc8ded23bd6296d430c5b4cae6515a2f395599541`
  → `{"citation_resolved_rules": 13, "rule_blocks": 14, "depth_score": 9.29}`,
  rule 14 refs `[]` → unresolved.
- `cand-T2.md` (T1 + one adjacent corpus/knowledge citation) sha256
  `705258b21c18b6d017e1f314aeccafd7fd3d3c43303b088b6b7231ab2e0db08b`
  → `{"citation_resolved_rules": 14, "rule_blocks": 14, "depth_score": 10.0}`.
- `cand-T3.md` (decoration control) sha256
  `ad4721d4bb54d9ef09f43fe37dd5b89d0398830eee1451e6e436b1af4c9ed262`
  → `{"citation_resolved_rules": 14, "rule_blocks": 14, "depth_score": 10.0}`.

These three predictions reproduce CR-1's independently authored
`rule14-candidates.md` predictions from this seat's own harness.

## Consequence pre-registered now

The C1 frozen claim's "14/14 citation-resolved" is **not** implied by the patch
being correct: it holds only if EX-01's rule text carries a resolvable
`corpus/knowledge` citation. A correct, incident-anchored rule that cites only
wave-tree evidence scores 13/14 (9.29). If that branch materializes, the
honest reading is that the *metric* under-describes the rule, not that the rule
failed — the dry-run will report the branch actually observed, not the
expected one.
