# CriticClaim — scoped findings, R64-C1 attack (round-64 w1)

Full table with per-finding evidence: `.ufo/waves/round-64/w1/CriticClaim/critique.md`.
Counterexample receipt copy: `.ufo/waves/round-64/w1/CriticClaim/receipt-false-node.json`
(sha256 `4e0199dfe58e36b457d7c6646a772baf20095c420c6b2000d94cc14fa4bf0593`).

## Verdict

**claim-survives** — no blocking defect. Disclose CC-1, CC-2, CC-3, CC-4, CC-9 in the round-64 lesson.

## Findings (one line each)

- **CC-1 (non-blocking, the strongest counter-argument):** the check stage is unpinned and
  one-directional — `PINS` has no `node`, `classify_check` maps any nonzero rc to `node-fail`,
  both dump-ok cells predict `node-fail`, and receipts record no check rc/stderr. Demonstrated:
  the frozen counting command with `--node /bin/false` returns `"verified": true`, 18/18, exit 0
  (receipt copied above). Mitigation is disclosure (lesson: `node-fail` = "node rejected", not
  specifically a syntax rejection) plus the receipted 213 B `probe-view8.js`, on which the real
  host node (v24.21.0) fails with `SyntaxError: Unexpected token ':'` at line 3 — the outcome the
  label stands for is directly observable.
- **CC-2 (non-blocking):** two of the four pre-freeze observations are not recountable from
  committed receipts — probe×D3 "exit 139" (`dump-probe-x7.txt` is 0 B, no `.err`, no rc recorded;
  `grep -rn '139' l1/` hits only predicted labels) and the probe×D1 node-check failure (no log).
  The matrix re-observes both under receipts; a scratch rerun reproduced `Received signal 11
  SEGV_ACCERR` on probe×D3.
- **CC-3 (non-blocking):** `dump-probe-ctrl.txt` records no producing binary; byte-diff vs
  `dump-probe.txt` is heap-address drift only, so D1-vs-D2 attribution (and hence the plan's
  "two were not run before the freeze") cannot be settled from receipts.
- **CC-4 (non-blocking):** pins cover 8 objects; the executed set is wider — D2/D3
  snapshot_blob.bin+icudtl.dat, View8 `Parser/`, `--python`, `--node` are unpinned; the pre-freeze
  venv (scratch `lead/venv-r64`, per view8-probe.log RuntimeWarning) differs from the counting
  command's persistent venv (both parse 1.22.4). Fake `--python /bin/true` IS caught
  (view8-empty); only the fail-direction node substitution slips through (CC-1).
- **CC-9 (non-blocking):** "Not claimed" list should gain three wordings: node-fail semantics
  (CC-1), single-host reproducibility (ASLR drift visible across reps: reconstructions 212 vs
  213 B; ctrl-vs-main dump), and the unpinned-auxiliary boundary.

## Attacks that did NOT land (claim holds)

- **(a) Falsifiability holds (CC-6):** exact-label equality over all 18 cells, `not-run` counts as
  mismatch, pins pre-checked (exit 2), controls verified live — selftest rerun this session:
  `SELFTEST CLEAN cases=22 failures=0`; do-nothing receipt `c1-before-donothing.json` `"exit": 1`,
  all cells `not-run`. No partial route can emit green.
- **(b) Do-nothing / fake-green cannot reach 18/18:** 0/18 both (selftest + committed control).
  The only green-reaching fake is CC-1's node substitution.
- **(c) Four observed cells recount:** SFI count in `dump-probe.txt` = 1 marker line, 2882 B
  (plan's byte count exact); typora aborts receipted for D1 (`dump-match.err`) and D3
  (`dump-typora-x7.err`), both `Received signal 6` (SIGABRT→134); abort reason is a libc++
  hardening OOB (`vector.h:416 vector[] index out of bounds`) — artifact-level, not a version
  banner; View8 receipt 213 B + view8-probe.log (parse/decompile/export complete). Two
  observations unreceipted (CC-2). A scratch run additionally corroborated the two unobserved
  predictions (probe×D2 dump-ok + reconstruction; typora×D2 abort) — corroboration only; L1's
  receipted run owns verification.
- **(d) "The route never runs the application" is TRUE:** the loadjsc patches contain no
  `Execution::Call` / `->Run(` / `Script::Run` / `Compile(` (zero matches across `patches/`);
  README describes loadjsc as "loads and prints `.jsc` bytecode"; View8 is offline text
  processing; `node --check` parses only. Only executed code: the disclosed, pinned 2-line probe
  generator.
- **(f) Sourced claim S264 SUPPORTED:** README at 01fc264d carries the exact CLI contract
  (line 139: `./d8 -e "loadjsc('path/to/xxx.jsc')" > xxx.txt`) and the matching-d8 requirement
  (lines 128, 199), plus "approximate JavaScript reconstruction" (line 122). Cosmetic frozen
  relic: the instrument docstring still cites "S125 README" (pre-renumbering); left unedited.
- **Provenance:** instrument sha, both input shas, all five binary shas, D1 aux shas and view8.py
  sha re-verified equal to PINS; freeze chain 3fd8468c (19:40:51) → a35e5141 (19:41:12) confirmed.
