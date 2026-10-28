# C1SelfTest — R48-C1 selftest coverage

## Axes
- Coverage: named missing selftest cases and exact observed suite result.
- Depth: identify test input distinctions needed to guard the predicates.
- Calibration: distinguish observed results from proposed (not run) cases.

## Evidence
- Frozen file inspected: `tools/round-48/meanings.py` (source SHA-256 `74b8da35b4c47c7732bc2cb5a69a3c048e8e1f22ccf93b506cba9a71cd90816d`).
- Exact command: `python /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/meanings.py --selftest`
- Working directory: `/fast/scratch/hyaku/kaidoku-r48/C1SelfTest`.
- Exit code: 0.
- Exact summary stdout: `MEANINGS_SELFTEST: cases=16 failures=0`.
- UTC capture time: `2026-10-28T18:47:03.703634+00:00` (captured immediately after run).
- stdout SHA-256: not separately captured at execution time; no hash is claimed.

## Coverage gaps (proposed, not run)
1. **Mutation body-edit digest case** — alter the source body of one mutation while preserving its name, recompute the expected pin against the original helper, and assert the block fails `mutations_sha256`. The current `red-digest-stale` only supplies an arbitrary wrong digest; it does not demonstrate that a body-only source edit changes the computed digest.
2. **`not met` inside exit 0** — provide a segment whose exit digit is 0 but text says `not met`, and assert the success class is rejected. This guards against a success regex matching the substring `met` inside `not met`.
3. **Two-class segment** — provide one digit segment text that simultaneously matches two semantic classes (e.g. success and not-met) and assert rejection rather than accepting ambiguous classification.
4. **Placeholder in only one segment** — use two valid meanings and put placeholder text in just the third segment; assert the entire verdict map is rejected. Existing `red-gold-meaning` replaces all segments with placeholders, not the one-segment boundary.
5. **Census duplicate** — duplicate a census path and test both the rederived census and corresponding registry-row behavior; assert duplicate paths cannot be hidden by set-based comparisons. Existing stale census introduces a new path but does not test duplicate cardinality.

The existing 16-case selftest passed as written; these five cases are suggested additions only. Frozen sources were not modified. No other checks were run.
