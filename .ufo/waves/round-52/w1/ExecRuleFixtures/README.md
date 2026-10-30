# Round-52 C1 rule fixtures

Rules are copied into this seat artifact directory. Census fixture is synthetic; it adds only the fourteenth unlisted char-device `dev/ttyS0 4:64` to a receipt-shaped minimal example (not a carrier receipt).

## Expected verdicts

Verdict means rule disposition consistency over the named census, not parser acceptance. The v2 counter must also enforce the independent rule-shape clause: a device detail whitelist is RED even when it happens to fit observed data.

| Input | Law rule | M1 all-thirteen | M3 required + 247:0 only | M4 strict subset |
|---|---|---|---|---|
| Four committed measured nonregular census tables | GREEN (4/4 expected) | RED (`law_shape_ok`; whitelist forbidden) | RED (required device disposition is contrary to law; missing details) | RED (required device disposition is contrary to law; missing details) |
| M2 synthetic fourteenth-device census | GREEN (no gap/disposition required) | RED (whitelist omits 4:64; and shape clause) | RED (required device disposition and 4:64 unaccounted) | RED (required device disposition and 4:64 unaccounted) |
| `junk-rule.json` over measured tables | RED (every kind requires impossible gap) | RED | RED | RED |

M1 deliberately contains all thirteen observed device details: its extensional behavior over the four existing carrier censuses can equal the law, so only `law_shape_ok` detects it. M3 recreates the earlier 247:0-only trap. M4 lists a proper subset of those details. All mutant rules retain the same symlink/removal and structural clauses as the law rule, except the deliberate char-device mutations.

## Parser note

The v1 parser at the round-50 base accepts only claim label `R50-C1` although R52-C1 requires `claim: R52-C1`. The validator script imports the v1 `gap_rule_model` from the scratch clone and validates each document's grammar after replacing the claim label in-memory only; it does not edit these files. Thus v1 grammar validation covers all non-claim fields, while label acceptance is a known v1 incompatibility, not reported as a pass.
