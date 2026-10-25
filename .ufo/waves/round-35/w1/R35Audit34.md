# R35Audit34 — D3 trio/append check

## Finding

**D3 is currently falsified at the inspected lane tip, 3ecf42981a0b63414de90ade643040d609dbb8a5.** The target entry exists and is byte-identical in the worktree to that committed version, but has no lines beginning `source:`, `verified-at:`, or `recheck:`. It therefore cannot satisfy C2's D3 check at this revision. This is a current-state observation, not evidence that D3 remains false at a later measured revision.

D3 in the frozen plan requires an *appended* provenance trio citing S106. The C2 counter enforces presence of the three line prefixes and an S106 match on the source line; it does **not** enforce append-only placement, source-path detail, correctness/quality of the recheck instruction, or a particular receipt citation. At present all three required prefixes are absent, so those weaker predicate checks already fail. No counter or source-tree command was run.

## Evidence and commands

- Read `plans/round-35-claims.md` (C2 D3 and claim discipline), `.ufo/waves/round-35/claims-canonical.json` (frozen C2 predicate), `tools/round-35/c2-calibration-counter.py` (D3 checks at lines 115–127), the target entry, `corpus/SOURCES.md` S106 row, and the round-34 verifier spotcheck D3 rationale.
- `grep '^source:|^verified-at:|^recheck:' <entry>` via the read/search tool: **No matches found**.
- `git -C <lane> rev-parse HEAD`: `3ecf42981a0b63414de90ade643040d609dbb8a5`.
- `git -C <lane> diff --quiet HEAD -- <entry>`: exit 0 (reported as `ENTRY_MATCHES_HEAD`). The inspected worktree entry is therefore the tip blob; this does not establish any future measured revision.
- Read S106 row: status `mined`, opened `2026-10-25`, `used-by` names the target entry. The row pins binutils tag `binutils-2_47` / commit `6ce87bbc` and a tracked capture with SHA-256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`.
- Counter code tests `(?m)^source\s*:`, `^verified-at\s*:`, `^recheck\s*:` and `^source\s*:.*S106`. Counter file SHA-256 observed: `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94`, equal to the canonical claims instrument pin.

## Suggested D3 remediation criteria (advisory only)

Append, without rewriting existing entry text, one `source:` line naming S106 and the relevant evidence/capture, one `verified-at:` line that accurately states when/how verification occurred, and one concrete `recheck:` instruction. Preserve the entry's existing scope caveats (S106 is section-header decode only, not loader behavior or gate verdict). Then the frozen C2 counter's D3 clauses can be evaluated against the measured commit. This is a recommendation, not a claim that the trio has been added or verified.

## Gates, surfaces, limits

- No C1/C2 counter, selftest, REA, parser, source fetch, build, or test was executed. No predicates, claims, production/corpus files, VCS state, or sibling paths were changed.
- Only this report path was written: `.ufo/waves/round-35/w1/R35Audit34.md`.
- C2 D1, D2, and D4 were outside this D3-focused check and are not assessed here. The canonical C2 freeze setup caveat in `freeze-status.md` remains a separate known limitation; this check does not resolve it.

Report: .ufo/waves/round-35/w1/R35Audit34.md