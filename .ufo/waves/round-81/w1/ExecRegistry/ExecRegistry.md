# ExecRegistry — round 81 C1 candidate

Axes: calibration + depth; no domain coverage claim. Scope: candidate data only, not integrated admission or promotion.

## Deliverable

`candidate-edits.json` contains ten exact old/new SKILL row replacements from committed base `5b59ae615a2ab68e3b421820d1c72751e1185385`: seven grammar repairs and three D2 tally corrections. Each grammar edit includes the seven decoded cells and its meaning explanation. `SKILL.candidate.md` is the resulting complete candidate text. Production SKILL and all other production files remain untouched.

## Seven repairs (all now exactly seven cells)

| Row | Field-meaning repair |
|---|---|
| round-77/verdict-bind.py | Preserve committed SCORECARD/PROVINCE/receipt input description as pinned; merge receipt-only output and read-only/none qualifier into write scope, clarifying none refers to lane writes. Keep owner. |
| round-77/prefile-receipt.py | Preserve lane/clone/git-show input description as pinned; merge filing/json output and one-clone-per-work-root descriptions into write scope. Keep owner. |
| round-77/gen-controls.py | Preserve both instrument inputs as pinned; merge control copies/json output and caller out-dir into write scope. Keep owner. |
| round-78/attack-gate.py | Escape the TWO literal purpose pipes in control alternatives; restore verdict/selftest positions; keep every fixture/tool input and receipt observation/refusal disclosure in pinned; add actual json-out/work-only scope and round-78 owner. Escaping alone would leave six cells, not seven. |
| round-78/surface-recheck.py | Preserve all providers in pinned and retain never-env/token disclosure; add explicit json-out-only write scope and round-78 owner. No live providers opened. |
| round-79/gate-mutation.py | Keep target revision/digest/TARGET_SHA256 in pinned; merge duplicate receipt/scratch/read-only descriptions into write scope. Keep owner. |
| round-79/pointer-bind.py | Keep committed PROVINCE/datetime-qualified live-input description in pinned; merge receipt output and read-only live-input access into write scope. Keep owner. |

No write-scope text was escaped into a counterfeit pinned column. Pin cells retain their historical input descriptions rather than inventing new cryptographic pins. New round-78 owners follow neighboring round naming, not runtime measurements.

## Retained bounded evidence

- `candidate-parse.json`: unchanged base/freeze counter bytes, frozen `parse(candidate, exists_at(base))`, then frozen verdict: exit 0, rows 129, paths 129, nonconformant [], duplicates [], multicell_rows 4. Exactly four round-69 legacy rows remain, byte-unchanged. All 129 original registry paths preserved; repaired rows each have seven cells.
- `registry-census.frozen.py`: exact committed counter bytes; base equals freeze `abdcfd3c28d98288a3dc6b4e98c88d115ed42b53`. Digest retained in receipts.
- `census-selftest.json`: unchanged counter selftest executed ONCE, exit 0, 14 cases, failures []; full argv/stdout/stderr retained. Explicit absolute scratch cwd, TMPDIR and --work. No fixture commits and no repository test sweeps.
- `d2-counts.json`: AST-derived case registrations from committed round-80 tools, with blob SHA256, case names and line numbers: pointer-bind 34 (not 33), strictness-battery 9 (not 8), receipt-provenance 16 (not 14). Counted literal-name `case(...)` calls within each selftest; calls are straight-line, not loop-expanded. Did NOT execute these selftests.
- `sources.md`: opened GFM admission for table-cell escaping; opened tempfile rejection with reason and flip. Reuse existing SOURCE identities by URL; no row appended. Historical duplicate URL rows disclosed, not repaired outside scope.

Initial demonstration's population assertion compared registry paths with all tool-leading tables in SKILL (169), not its marker-bound population (129). Corrected that harness assertion only. Frozen parse already succeeded; selftest had not run before this failure. This is not a counter defect or hidden failed selftest.

## Limits and integration

This is a candidate-text parse against base path existence, NOT a post-integration committed-revision census. L1 should apply each exact old/new replacement once and run the frozen committed-revision census at the integrated commit; owner/field meaning remains visible for review. No changes to frozen predicates, counter, legacy round-69 rows, production docs, git/jj state or external substrate. No installs/updates. LSP unavailable: no LSP tool mounted; only source/data inspection, no symbol refactor performed. Scratch `/fast/scratch/hyaku/kaidoku-r81/ExecRegistry/` removed after retained receipts. No blockers.

Self-evaluation: accuracy 4 (candidate-text rather than integrated-revision evidence explicitly bounded); completeness 4 (source used-by integration remains L1-owned); clarity 4 (long exact rows necessarily in JSON, summary here); actionability 5 (exact old/new list); conciseness 4 (full candidate text duplicates inputs to ease integration). Mean 4.2. Improvements: L1 committed-revision measurement; integrate reused-source used-by citations without adding URL rows. User-agreement check: evidence is scoped to the assigned candidate, not an admission vote.

Report: .ufo/waves/round-81/w1/ExecRegistry/ExecRegistry.md
