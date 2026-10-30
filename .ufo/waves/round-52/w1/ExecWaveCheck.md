# ExecWaveCheck — r52-w1 dispatch interpolation

Verdict: settled. Added `ExecWaveCheck/check-dispatch.py` to detect unresolved uppercase placeholder markers and brace-wrapped lane-path strings in context and item prompts; `--selftest` checks clean input and both violation forms.

Evidence: Ran `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecWaveCheck/check-dispatch.py --selftest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1-spec.json`; exit 0. Output: `selftest: 3 fixtures passed (clean, uppercase marker, literal lane-path braces)` and `dispatch placeholder check: clean`. Captured stdout SHA-256: `d610c20fb1e0befdef8ac33cf028f1fcf2709ca9abbd66f1288841f0c93c8eb7`; UTC `2026-10-30T10:47:22Z`. Receipt and raw stdout are in `ExecWaveCheck/receipt.json` and `ExecWaveCheck/check.stdout`.

No spec violations found. No REA run, build, lint, or tests beyond the assigned offline selftest were run. No tools installed. Risk: this check enforces the two specified regex forms; it does not resolve/render prompt templates or infer other placeholder syntaxes.
