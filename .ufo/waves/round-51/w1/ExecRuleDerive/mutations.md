# Gap-rule mutation expectations (v2 counter, committed R50 receipts)

Verdict means `disposition_check` result, not overall carrier-match score. All rows are based on the counter semantics at `tools/round-50/c1-counter.py:1458-1569` and the observed carrier char-device rows.

| Mutation | c6430 Cable | c6490 Cable | g7581 FRITZ!Box | g7582 FRITZ!Box | Reason |
|---|---|---|---|---|---|
| Baseline v2 (`required.char-device=false`, no silent whitelist) | green | green | green | green | Char-devices exempt from required-disposition check; actual receipt has no device dispositions. |
| `require-char-device` (`required.char-device=true`) | red | red | red | red | No device entries have a gap/removal; a required kind with allowed gap types still requires one disposition. |
| `whitelist-247:0-only` (set `required.char-device=true`, `removed.silent.char-device=["247:0"]`) | green | green | red | red | Cable's sole `247:0` is silent-admitted; Fritz class has 12 nonmatching char entries. |
| `whitelist-strict-subset` (set `required.char-device=true`, silent details to any proper subset of the thirteen observed details, including the R50 `247:0` subset) | green iff subset includes `247:0`; otherwise red | green iff subset includes `247:0`; otherwise red | red | red | Cable has only `247:0`; FRITZ!Box has thirteen detail values, so any strict subset leaves at least one required row without disposition. |
| `drop-symlink-removal` (remove `removed.diagnostic`/removal acceptance) | red if any diagnostic exists for a required symlink; otherwise unchanged | same | same | same | In these committed receipts diagnostics are empty and the exact symlink-gap coverage is not summarized per-entry here; therefore observed verdict is not fully decidable from aggregate fields. Counter must reject any required symlink whose gap/removal disposition is thereby absent. |

The mutation requirements are deliberately stateful: whitelist variants turn on `required.char-device`; under v2's `required.char-device=false`, changing a silent list alone cannot change verdict because that kind is skipped by the disposition checker. This distinction should be encoded in fixture labels to avoid ambiguous mutation names.
