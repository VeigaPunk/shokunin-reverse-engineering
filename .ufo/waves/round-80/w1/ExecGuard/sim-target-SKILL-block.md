<!-- round-80 receipt-guard table: begin -->
| G01-duplicate-fixture-id | the receipt lists the same fixture id twice | `duplicate fixture id` | `red-validate-guard-duplicate-id` |
| G02-fixture-id-set | the receipt's fixture ids differ from the declared set | `fixture ids` | `red-validate-guard-id-set` |
| G03-fixture-dir-mismatch | a fixture id names a different fixture directory | `: fixture dir mismatch` | `red-validate-guard-dir-mismatch` |
| G04-base-accepted-bool | a fixture's base.accepted is not a bool | `: base.accepted is not a bool` | `red-validate-guard-base-bool` |
| G05-refused-without-reason | a refused fixture carries no reason | `: refused without a reason` | `red-validate-guard-refused-no-reason` |
| G06-refused-by-other-rule | a refusal reason names a rule other than the declared rule | `: refused by ` | `red-validate-guard-refused-by-rule` |
| G07-base-accepted-rederive | base_accepted disagrees with the fixture list | `base_accepted does not re-derive` | `red-validate-guard-base-rederive` |
| G08-refused-rederive | refused disagrees with the fixture list | `refused does not re-derive` | `red-validate-guard-refused-rederive` |
| G09-instrument-digest | the receipt's instrument sha256 is not this file's digest | `instrument sha256 is not` | `red-validate-guard-instrument-digest` |
<!-- round-80 receipt-guard table: end -->
