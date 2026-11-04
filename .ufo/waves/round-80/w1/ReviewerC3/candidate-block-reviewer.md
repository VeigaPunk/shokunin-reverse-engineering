<!-- round-80 receipt-guard table: begin -->
| G01-duplicate-fixture-id | the fixture id appears twice | `duplicate fixture id` | `red-validate-duplicate-fixture-id` |
| G02-fixture-id-set | the fixture id set differs from the declared set | `fixture ids` | `red-validate-fixture-id-set` |
| G03-fixture-dir | a fixture row names another fixture directory | `: fixture dir mismatch` | `red-validate-fixture-dir` |
| G04-base-accepted-bool | base.accepted is absent or not a bool | `: base.accepted is not a bool` | `red-validate-base-accepted-bool` |
| G05-refused-no-reason | a refused fixture carries no reasons | `: refused without a reason` | `red-validate-refused-no-reason` |
| G06-refused-other-rule | a refusal names another rule | `: refused by ` | `red-validate-refused-other-rule` |
| G07-base-accepted-count | base_accepted is not re-derived | `base_accepted does not re-derive` | `red-validate-base-accepted-count` |
| G08-refused-count | refused is not re-derived | `refused does not re-derive` | `red-validate-refused-count` |
| G09-instrument-digest | the digest is not the running file's | `instrument sha256 is not` | `red-validate-instrument-digest` |
<!-- round-80 receipt-guard table: end -->
