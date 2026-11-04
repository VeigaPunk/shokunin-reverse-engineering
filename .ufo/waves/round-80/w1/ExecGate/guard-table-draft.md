<!-- round-80 receipt-guard table: begin -->
| G01-duplicate-fixture-id | the receipt's `fixtures` list names the same fixture id more than once | `duplicate fixture id` | `red-validate-duplicate-fixture-id` |
| G02-fixture-id-set | the receipt's fixture id set differs from the declared `ATTACKS` id set | `fixture ids` | `red-validate-fixture-id-set` |
| G03-fixture-dir | a fixture's `fixture` dir differs from the declared dir for that id | `: fixture dir mismatch` | `red-validate-fixture-dir` |
| G04-base-accepted-bool | a fixture's `base.accepted` is not a bool | `: base.accepted is not a bool` | `red-validate-base-accepted-bool` |
| G05-refused-no-reason | a fixture is marked refused and carries no `reasons` | `: refused without a reason` | `red-validate-refused-no-reason` |
| G06-refused-other-rule | a refusal reason names a rule other than the fixture's declared `rule` | `: refused by ` | `red-validate-refused-other-rule` |
| G07-base-accepted-count | `base_accepted` does not equal the count of fixtures whose `base.accepted` is true | `base_accepted does not re-derive` | `red-validate-base-accepted-count` |
| G08-refused-count | `refused` does not equal the count of fixtures marked refused | `refused does not re-derive` | `red-validate-refused-count` |
| G09-instrument-digest | the receipt's `instrument.sha256` is not the digest of the gate file | `instrument sha256 is not` | `red-validate-instrument-digest` |
<!-- round-80 receipt-guard table: end -->
