# ExecPriors — round 52 wave 1

Verdict: settled. Drafted the v2 prior carrier constant block and its source/path documentation at `.ufo/waves/round-52/w1/ExecPriors/priors.json` and `README.md`.

- Included the four prior `sha256` pins, exact four-ID `re_scored_pins` allow-list, manifest JSON Pointer sources, and per-carrier oracle/nonregular paths.
- Read source values from `tools/round-50/carriers.json` (carrier objects `/carriers/0` through `/carriers/3`; see README for field pointers).
- Evidence: `git cat-file -e` checked all eight table paths at `ab0eafedc41402b43b41a4362084119578dfe7ce`; all exit codes were 0. Receipt includes the command, stdout, stdout SHA-256, and UTC timestamp in README.
- Not run: table-content validation, vendor re-fetch, REA, build/lint/tests (out of scope).

Risk: the constant-block key shape is a draft interface for L1 integration; pin values and paths are sourced from the round-50 manifest and table path existence is evidenced. No blockers. Status: `ExecPriors/status.json`.
