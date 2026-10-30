# RevV6Draft

Verdict: **do not salvage the round-51 draft as a port base; port committed v5.**

1. Scratch py_compile exits 1 at draft line 288 (`CUT 1033.=1033`); malformed table splices also occur at 1018–1022 and 1033–1034.
2. Only draft 1027–1029 is a useful design fragment (new ddwrt failure selector, label, preserve-unresolved action). It has no matching evaluator return. Do not copy its unsupported “both validated readers” explanation.
3. The draft has no executability/census audit or freeze-drift verdict gating; the actual diff is only three hunks. Prior executor prose understates these changes and records no completed tests.

Full line-level take/drop recommendations, caller/test effects and residual risk: `RevV6Draft/verdict.md`.
Evidence: `RevV6Draft/compile.json`, `RevV6Draft/comparison.json`, `RevV6Draft/v5-v6.diff`.
LSP unavailable: xd://lsp is not mounted; source-body and textual-diff fallback used, not represented as semantic references.
No REA, downloads, repaired runtime, corpus scoring or selftests run. No tools installed. Source tree unchanged; scratch removed after receipt capture.

Self-evaluation: accuracy 4/5 (compile directly observed; later syntax defects source-inspected only); completeness 4/5 (all salvage requests covered; no executable v6 exists to score); clarity 4/5 (exact lines given; full report intentionally detailed); actionability 5/5 (v5 base and precise reusable fragment identified); conciseness 4/5 (full verdict repeats key safety distinctions). Overall 4.2/5. Highest-impact remaining verification belongs to the replacement instrument, not this invalid draft.
