# ExecRuleFixtures — round 52 wave 1

Verdict: **settled**. Drafted the C1 rule package and synthetic mutation fixtures exclusively under this seat directory; no lane source paths changed.

## Deliverables

- `ExecRuleFixtures/gap-rule.json`: R52-C1 claim, device/fifo/socket allowances empty, char-device required false; copied symlink/dir, removed symlink diagnostic, and structural clauses from the round-50 rule, with char-device silent whitelist removed.
- `ExecRuleFixtures/junk-rule.json`: every kind is required with `impossible-gap-kind` allowance.
- `ExecRuleFixtures/M1-all-thirteen.json`, `M3-required-247-only.json`, `M4-strict-subset.json`: requested deliberate mutation rules.
- `ExecRuleFixtures/M2-fourteenth.nonregular.tsv` and `.receipt.json`: synthetic fourteenth char-device (`dev/ttyS0`, `4:64`); does not contain vendor bytes or purport to be a carrier receipt.
- `ExecRuleFixtures/README.md`: expected results by fixture/rule and parser caveat.
- `ExecRuleFixtures/validate_rules.py` and `grammar-validation.receipt.txt`.

## Exact retained evidence

Read-only scratch clone was checked out at `ab0eafedc41402b43b41a4362084119578dfe7ce`; `git -C "$TMPDIR/clone" rev-parse --show-toplevel` returned `/fast/scratch/hyaku/kaidoku-r52/w1-ExecRuleFixtures/clone`.

Executed command: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecRuleFixtures/validate_rules.py /fast/scratch/hyaku/kaidoku-r52/w1-ExecRuleFixtures/clone/tools/round-50/c1-counter.py`

Exit code 0. Output named all five rules (law, junk, M1, M3, M4) as v1-grammar OK after in-memory claim-label normalization. Stdout SHA-256: `bbff9ad5beec7d1f4cee1c6edc97c1460a4862a465e74fa66ba4934c2dbcf890`. UTC: `2026-10-30T10:48:01Z`. Full receipt retained in `ExecRuleFixtures/grammar-validation.receipt.txt`.

The lane's v1 `gap_rule_model` explicitly rejects any claim other than `R50-C1` (counter lines 791–794), whereas R52-C1 mandates `R52-C1`. Therefore direct raw v1 parser acceptance of gap-rule.json is impossible at this base; the script transforms only this label in memory and tests the other grammar fields using the imported v1 parser. v2 parser acceptance remains unverified and is for the L1's integration gate. Fixture verdict table is reasoned from the declared law/mutations; no counter scoring was run in this seat.

No REA, build, lint, test suite, or data run was invoked. No tools installed. Scratch removed after preserving the receipt: `/fast/scratch/hyaku/kaidoku-r52/w1-ExecRuleFixtures`.
