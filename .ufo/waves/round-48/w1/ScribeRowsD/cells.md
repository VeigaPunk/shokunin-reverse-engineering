# R48 third-split meaning-bound verdict cells

Scope: the third alphabetical-path slice of round-46/47 rows inspected in the frozen instrument registry. Earlier row reports identify no failing-row population (C1RowsA) and no counter-run evidence (C1RowsB). Thus these are **candidate replacements**, not claims that these rows were observed failing under the frozen counter. No registry path was independently measured against the full census in this seat.

Each replacement explicitly attaches digit 0 to success, 1 to not-met, 2 to unevaluable; meanings differ and are non-placeholder. Preserve row-specific conditions and do not treat these drafts as evidence of self-test execution.

| path | candidate meaning-bound verdict map |
|---|---|
| `tools/round-46/attest.py` | `0=met with failing empty; every frozen clause holds and every forgery is rejected; 1=not met, one or more frozen clauses fail; 2=could-not-evaluate: unknown/non-ancestor revision, malformed claims, frozen path changed, unusable scratch or evaluation exception` |
| `tools/round-46/census.py` | `0=clean, census computed and emitted; 1=not met, generation failed or output could not be written; 2=could-not-evaluate: usage error (missing root or unknown option)` |
| `tools/round-46/gate.py` | `0=clean, both history and blob arms confirm freeze ancestry and unchanged paths; 1=not met, not a gate verdict (library-only entry point) or an evaluated binding is false; 2=could-not-evaluate: unknown/non-ancestor revision, absent claim paths, failed git call, refused output, missing scratch or caught exception` |
| `tools/round-46/registry.py` | `0=met, registry path and verdict bindings clean and all seven forgeries rejected under v2; 1=not met, unregistered/thin/absent path or battery off target; 2=could-not-evaluate: missing/doubled markers, absent census or skill at revision, changed frozen path, or no scratch root` |
| `tools/round-47/exact.py` | `0=met with failing empty; exact rule, arms, ids, pins and battery all hold; 1=not met, one or more clauses fail; 2=could-not-evaluate: unknown/non-ancestor revision, malformed claim/craft, changed frozen path, refused output, unusable scratch or caught exception` |
| `tools/round-47/record.py` | `0=met, every re-derived atom and correction agrees; 1=not met, mismatch or bad correction; 2=could-not-evaluate: unknown revision, missing scorecard, fewer than two sections, refused output or caught exception` |

## Boundary
These six are a draft subset, not a verified "failing rows" subset. The frozen claim requires exactly every row in `tools/round-48/census2.json`; each candidate must be reviewed against that exact path set and the tool's actual exit contract before landing. No self-test, counter, fixture, or mutation test was run here.
