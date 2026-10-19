# Proposed patch text (NOT applied) — recipe line: hash-pin the instrument per run

Seat SC-2 (scribe, chain c2), arc3-loop1-round2, 2026-10-19. **Patch text only** —
`SCORECARD.md` is parent-written and this seat may not touch it.

Motivating measurement (`claims/c2/SC-2/receipts/`): an instrument under live edit
produced a text-mode `FAIL` and a `--json` `PASS` on the *same* root ~80 ms apart,
because the two invocations straddled the 09:10:56 → 09:11:50 revision swap
(measured deterministically afterwards on preserved copies:
`revision-churn-at-head.txt`, r4 FAIL both modes, r5 PASS both modes). Every
fixture row in the injection ledger had to carry its own instrument hash to be
trustworthy (`receipts/runs/landed3*.json`, `instrument_stable: true`, 46/46).

Proposed wording, for the SCORECARD "Measurement recipes" section (appended to
the existing command-A recipe paragraph):

```
- Instrument identity: any recipe that runs a gate/instrument committed in the
  same wave records `sha256sum <instrument>` in its receipt and re-checks it
  after the run; a verdict-changing edit mid-wave invalidates the receipt
  (re-derive per queue-drain rule #14, per-run rather than per-session).
```

No code change is proposed against `.ufo/gates/c1-census-v10.py`; the two
round-1 patch texts this chain landed are closed as claimed in
`claims/c2/SC-2/injection-ledger.md` Section 2.
