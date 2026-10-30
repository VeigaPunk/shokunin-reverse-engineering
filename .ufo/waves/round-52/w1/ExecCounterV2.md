# ExecCounterV2

Verdict: incomplete/failed draft; do not freeze as the v2 counter.

- Created `ExecCounterV2/c1-counter.py` by copying the R50 counter and updating the round-52 receipt, entry, heading, frontier, open-date, provenance, and counter-path constants; added `tools/round-50/carriers.json` to the prior carrier tables and adjusted frozen-path names/prefixes.
- The required semantic changes are NOT implemented: R50/R52 claim grammar; `law_shape_ok`; score-time bidirectional non-regular census re-derivation with `oracle_env_error`; `depth_gap_recorded`; four-pin `re_scored_pins` provenance; extraction-tree ENOENT retry policy and attempt diagnostics; and mutated-frozen-byte exit-2 selftest.
- The copied source also retains old R50 documentation and may have inconsistent frozen-path handling for directory entries. `--selftest` was not run; no controls/data/REA were run.
- Evidence: claims file confirms requirements at lines 77–98 (new clauses), 105–114 (projection retries), and 148–153 (freeze drift and grammar). Existing counter constants were read from the R50 source; destination was modified only in the assigned seat directory.
- Checks: not run (per wave policy). No tools installed. No external downloads or REA invoked.
- Blocker/risk: the full port has not been completed, so the L1 must not integrate this artifact without completing and reviewing the missing implementation.
