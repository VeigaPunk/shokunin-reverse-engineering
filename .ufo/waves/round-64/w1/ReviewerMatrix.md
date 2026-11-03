# ReviewerMatrix — R64-C1 instrument review (round 64, w1)

Full evidence table: `.ufo/waves/round-64/w1/ReviewerMatrix/review.md`.

Checks 1-6 and 8-9 pass for the counting command (sha256 `29efef4f…` matches; predicate byte-equal to claims.json L12 and plan L23; PREDICTED equal to plan table; verdict counts 18 with missing cells as not-run; pins checked before any d8 call at L179-182; emit prints verified only on 18/18). Check 7 fails.

| id | line | class | blocking? | evidence |
|---|---|---|---|---|
| F1 | L56-66, L142-166 | predicate coverage: "every binary pinned" not implemented | blocking | D2/D3 `snapshot_blob.bin` unpinned (observed `601efdc6…`, `80590f45…`, D1 pin `b5c418dc…`); node, python venv, View8 tree beyond `view8.py` unpinned |
| F2 | L204-207 | writes outside --work: view8 imports write `__pycache__` into frozen jsc2js tree | blocking (rule 7) | `View8/Parser/__pycache__` and `Simplify/__pycache__` pycs at 2026-11-03 19:36; `PYTHONDONTWRITEBYTECODE` unset; neutralise by env at run time |
| F3 | L316-317 | `--selftest` exits 0 with no matrix run | non-blocking | not in counting command |
| F4 | L204-212 | uncaught missing-tool / view8 / node timeout → exit 1, not documented exit 2 | non-blocking | no false pass; no receipt written |
| F5 | L100-101 vs L25 | `dump-empty` label used for non-SFI output, docstring says empty | non-blocking | no predicted cell affected |
| F6 | L179 | pins checked once, not after runs | non-blocking | — |
| F7 | L171 | unescaped path in JS string | non-blocking | fixed inputs |

Selftest (`--selftest`): 22 cases, 0 failures, exit 0. `--skip-run`: 0/18, exit 1 (both run in scratch, nothing written to the repo).

verdict: `instrument-defective: F1, F2`
