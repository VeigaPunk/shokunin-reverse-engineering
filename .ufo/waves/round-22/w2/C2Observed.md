# R22-C2 counter review

Reviewed `.ufo/waves/round-22/tools/count-c2.py` read-only against the round-22 claim and with temporary Git fixtures. Full captured argv/stdout/stderr/exits are in the companion `C2Observed.json` attachment. No production files were edited and no REA/runtime/device operation was invoked.

## Finding

**Medium — the shipped `--selftest` currently fails one control.**

Command: `/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py --selftest`

Observed exit: **1**, stderr empty; JSON reports `finding=counter_controls_failed`, 24 cases, 23 passing. The sole failing case is `recursive_receipt`: expected status `receipt_unevaluable`, actual `receipt_not_envelope` (both exit 1 and count 13). `counter-fixtures.py` builds this receipt as 2,000 nested JSON arrays (`counter-fixtures.py:164`) and expects `receipt_unevaluable` (`:136`). The current parser accepts that syntactically valid JSON array, then correctly rejects its non-envelope top-level shape (`count-c2.py:143-144`). This is a fixture expectation mismatch, not a false acceptance. Narrow fix: expect `receipt_not_envelope`, or change the control to reliably trigger a parser recursion error if that is what it intends to test. Until then the selftest exit is red and can fail automation.

## False-acceptance probes

- **Positive control:** all 14 valid, command-matched error receipts returned exit **0**, `accounted_count=14`, `mismatched=[]`, `finding=dispositions_complete`.
- **Contradictory observed error:** changed only the first receipt code from `capability_unavailable` to `invalid_request`, leaving the row at `error:capability_unavailable`. It returned exit **1**, `accounted_count=13`, `mismatched=["inspect-packet-fields"]`, first-verb status `observed_mismatch`.
- **Empty-code edge:** changed the row to `observed=error:` and receipt `error.code=""`. It returned exit **1**, `accounted_count=13`, first-verb status `bad_observed_grammar`; current `check()` explicitly rejects an empty `error:` suffix (`count-c2.py:149-153`).
- The current fixture controls also reject overflow/non-finite JSON numbers and boolean-vs-number mismatches. Thus I found **no current false-ok acceptance for a contradictory non-empty error code** in the exercised cases. These exact captured outputs and commands are in `C2Observed.json`.

## Declared limits / residual risk

The counter output itself declares that it compares only observed fields/codes; reason and placement semantics plus `.run.json` metadata need manual review, and it does not establish provider availability over time. I treated that as an explicit limit, not an implementation defect. No real REA invocation was used in this review.

LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`, so references/definition/diagnostics could not be requested. Source findings above are based on direct reads and captured bounded probes; no grep result is offered as semantic evidence. No tools were installed or updated.
