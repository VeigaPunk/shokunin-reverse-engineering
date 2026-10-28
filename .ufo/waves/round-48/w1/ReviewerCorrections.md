# ReviewerCorrections — R48-C2 correction-line review

## Finding: no round-48 correction draft exists in the inspected card

At the inspected worktree state, `SCORECARD.md` ends with the Round 47 material and contains no `## Record corrections — round 48` heading or `corrects ...` lines (`SCORECARD.md:3663-3726`; literal search returned only the round-47 correction lines). Therefore there are no drafted R48 correction lines to compare individually against R48-C2's grammar or `record.py:corrects()`. Any claim that a particular draft line passes is unsupported; **not run** against a nonexistent draft.

## Applicable requirements and factual checks

- R48-C2 grammar in `tools/round-48/record2.py:44,98-111` accepts only lines matching `- corrects (seats|window|path|rev|axes|quote) <key>: <statement>`. It silently ignores other prose/lines; clause 3 requires every correction line to re-derive.
- Seats correction semantics for `seats` are delegated to the committed Round-47 oracle's `corrects()` (`record2.py:262`); it requires a real dispatch-derived total and correct `N waves, M seats total` statement. The separate `seats` floor is satisfied only if a seat atom exists or a re-derived seats correction is present (`record2.py:220`).
- The inspected Round-48 dispatch reports `wave=r48-w1`, `counts.spawn=75`, `counts.total=75`, `resume=0`. This is not a Round-47 dispatch and must not be used as a Round-47 seats correction. Exact command: `python3 -c 'import json; d=json.load(open("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1-dispatch.json")); print(json.dumps({"wave":d["wave"],"counts":d["counts"]},sort_keys=True))'`; exit 0; stdout SHA-256 `2c7e55a72d1fbe5fe2f3a7612c22daf8fcf56584e5a951acf3812de83194356a`; UTC `2026-10-28` (date available; time-of-day not captured).
- The declared freeze does **not** contain `.ufo/waves/round-48/w1-dispatch.json`; `git show dc73587a8b9c1a23ba5a91dc7707ac7381a8b873:.ufo/waves/round-48/w1-dispatch.json` failed (path exists on disk, not in that commit). This is consistent with dispatch being later wave evidence, not a frozen claim instrument.

## Mismatch inventory

No individual line mismatch can be named because the requested round-48 correction draft is absent from the inspected `SCORECARD.md`. Specifically, no seats/window/path/rev/axes/quote statement, correction key, or quoted receipt value is available to test. Quote binding additionally requires an actual cited receipt in the corrected round section and a value in that receipt (`record2.py:159-177`); no R48 round section or its receipt citations are present in this card state. **Not run**: counter execution, oracle `corrects()` against a draft, or quote-to-receipt comparison.

No tools installed. No frozen file or lane source edited. Disk guard status was checked before review.