# RevengerProbe — round 76 (r76-w1), LabratProbe seat

**Hypothesis probed.** The round-75 printed R75-C1 counter command fails for exactly the two
reasons the gate's routed defect 4 names — the omitted required `--work` and the abbreviated
`--expect-target-sha256` digest — and no third. Read-only probe of the command as printed in
`.ufo/reports/round-75/kaidoku.md` (R75-C1 after), joined as committed in
`.ufo/waves/round-76/pre/fixtures/r75-printed.md`.

Full probe: `.ufo/waves/round-76/w1/LabratProbe.md`; structured receipt:
`.ufo/waves/round-76/w1/LabratProbe/receipt.json`; run-3 stdout bytes:
`.ufo/waves/round-76/w1/LabratProbe/step3-stdout.json`.

## Four runs (lane root, Python 3.14.8, `python3 -I -B`)

| # | change from the printed line | rc | message | executed |
|---|---|---|---|---|
| 1 | none (ellipsis kept, no `--work`) | 2 | `{"unevaluable": "missing required arguments: work"}` | no |
| 2 | full digest bound, no `--work` | 2 | `{"unevaluable": "missing required arguments: work"}` | no |
| 3 | full digest bound + `--work <empty dir>` | 0 | `ok true`, `survivor_count 0`, 15 killed / 0 wrong-case, pristine 25 green, pin matched before execution | yes, 619 ms |
| 4 | `--work` added, ellipsis kept | 2 | `{"unevaluable": "target pin mismatch before execution: expected 1fc1c8fc\u2026, blob at 538b8b81:tools/round-75/seam-probe.py is 1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d"}` | no (work dir empty) |

Run 3 finished well inside the 20 s SIGTERM cap, so no timeout was triggered and no child was
left behind; `--json-out` was not supplied and is not needed. Digest ground truth:
`git show 538b8b81:tools/round-75/seam-probe.py | sha256sum` =
`1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d`, i.e. the full digest the
report abbreviates.

## Conclusion

**Complete.** The gate's two named reasons are the whole set. Smallest additions that make the
printed command runnable: (1) `--work` naming an existing directory and (2) the full 64-hex
`--expect-target-sha256` digest; with only those two the printed line runs verbatim, exits 0 in
0.62 s and reproduces the reported counter. No third defect surfaced.

Ordering caveat (observed, not a divergence): because `main()` checks required options before
the pin, the printed line with both defects reports the `--work` refusal (runs 1 and 2 are
identical); the ellipsis refusal only appears once `--work` is supplied (run 4). A static
block-refuser such as `tools/round-76/plan-command.py` inspects text first and therefore reports
`PLACEHOLDER_UNBOUND`, which is exactly the C2 r75-printed arm's behavior.

## Bounds

Read-only. Scratch `/fast/scratch/hyaku/kaidoku-r76/RevengerProbe/` deleted after copying
evidence. No lane production file touched; only the four evidence paths listed in the receipt
were written.
