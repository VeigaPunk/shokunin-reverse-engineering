# ExecOfflineGrammar — round 51 wave 1

Verdict: dry-run proof supports the intended control expectations; no live extraction performed.

- Read R50 counter header and `disposition_check`, all four committed `run.json` records and their referenced `after.json` payloads, the gap rule, and claims section R51-C1. Exact payload paths and fields are documented in `ExecOfflineGrammar/grammar.md`.
- Built `ExecOfflineGrammar/disposition-dryrun.py`; it evaluates path-resolved gaps, structural gaps, removals and residual required nonregular rows against the committed four carrier payloads and tables.
- Exact command: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-51/w1/ExecOfflineGrammar/disposition-dryrun.py`; exit `0`; stdout SHA-256 `65b623e76f0e6d327f421a5607289d9fa474c8657c0fcd36b71710666888e100`; UTC `2026-10-30T04:58:19Z`. Output artifact: `ExecOfflineGrammar/dryrun.stdout`.
- Result: round-50 rule passes 2/4; FRITZ!Box g7581/g7582 fail with exactly 12 unaccounted char-devices each; law-derived rule passes 4/4. Cable c6430/c6490 pass under both.
- No REA/data-run, download, tool install, or lane-tree writes outside this seat artifact/report. Scratch contents removed after preserving stdout.

Risk: this script is a standalone dry-run model of the three disposition families, not the not-yet-landed v2 counter itself; L1 should port the frozen semantics and score actual controls against the later counter. Evidence proves expected R50-vs-law outcomes on the committed envelope/table data, not a fresh carrier run.
