# ExecC3 — R73-C3 frozen re-derivation

**Not established at declaration.** Independent base pristine/a/b/c all pass 35 cases. Declaration pristine passes 38; independent a/b/c each exit 1 with 38 cases. However a fails `checker-readelf-allowlisted-exec`, not its declared git case, because the frozen shims share one positional log. Independent b and c fail their named cases with valid JSON/no import failures.

Frozen battery at declaration: **r73 survivor_count=1**, rc=1 (a killed_wrong_case, b survived, c killed). Its b changes the checker caller, unlike the independently tested helper seam. **r73base exits 2**, no survivor_count: c patch anchor matches zero times. Thus independent base survivors=3 is supported, but the requested frozen battery 0/3 result is not.

Correct and incorrect target pins were exercised in both directions. r73 explicitly reports correct=true versus wrong=false/mismatch and ok=false. Base aborts before a scored pin receipt, so base pin enforcement remains unevaluable.

Evidence: [detailed report](ExecC3/report.md), [aggregate receipts](ExecC3/summary.json), eight individual JSON results, six independent diffs, three original committed patches, four complete battery JSON receipts, and reproducible `ExecC3/rederive.py`. Sources were read from the specified commits; no instrument was edited. Scratch removed in finally. No installs, raw environment dumps, git writes or external state changes. LSP unavailable (no mounted tool).

Report: .ufo/waves/round-73/w1/ExecC3/report.md
