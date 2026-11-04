Seat: ExecSourceBind (executor). Claim: R85-C2 (depth). You own three rows whose targets are tools/round-83/source-bind.py (sb-emdash-optional, sb-id-substring) and tools/round-82/conjunction-gate.py (cg-frozen-detector-ge). Read the table `.ufo/waves/round-85/mutants.json`; never edit it. Also keep three already-killed rows killed: sb-window-13th (case late-single-header), sb-two-fields-first (case duplicate), cg-floor-le (case genuine-synthetic-passes). Do not weaken those cases.

# Rows
- sb-emdash-optional → `entry-cites-no-em-dash-refused` (source-bind.py): an entry line `source: S299 is cited here` (no em dash) must NOT attribute sid S299 on pristine. The mutant makes the em dash optional and attributes it.
- sb-id-substring → `id-prefix-not-attributed` (source-bind.py): an entry line `source: S2999 — https://example.com/b` must NOT attribute sid S299 on pristine; the mutant uses substring membership.
- cg-frozen-detector-ge → `frozen-duplicate-detector-refused` (conjunction-gate.py): the re-derived frozen rule must NOT count a synthetic genuine receipt whose detector row is duplicated as frozen-killed on pristine (`frozen_killed` False); the mutant's `>=` accepts it.

Each new case must invoke the production function (`entry_cites`, the production frozen-rule function, or the production selftest path), build its fixture under `$TMPDIR`/--work, assert the exact outcome, and fail under its mutant. Put new case functions at the END of each file (named `r85c_<case>`), and register each by one `guarded` or case-tuple entry, following the file's existing pattern (read the existing selftest structure first; source-bind.py uses a case tuple list around line 80–100; conjunction-gate.py uses `selftest()` around line 303).

# Measure
For each of the two target files, build a sandbox clone (see shared rules) with your candidate committed in the clone, then run the frozen counter from the sandbox:
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-84/mutation-closure.py --root "$D" --rev <sandbox commit> --mutants /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/mutants.json --work "$S/c2" --json-out <wave dir>/after-source-bind.json
Report the status of your three rows AND the three already-killed rows, and the pristine selftest rc/case names for each target file.

# Deliverables (wave dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/w1/ExecSourceBind/)
- `candidate/tools/round-83/source-bind.py`, `candidate/tools/round-82/conjunction-gate.py` (full files) and `candidate.diff` (both, vs 91eeb72f);
- `per-row.md` (table); `selftest-pristine.txt`, `selftest-candidate.txt`; any change to pre-existing cases with reasons;
- `DONE` marker last.
