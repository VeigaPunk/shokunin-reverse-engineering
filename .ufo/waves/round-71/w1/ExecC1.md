# ExecC1 — R71-C1 landing-side independent result

Detailed report: [ExecC1/rederive.md](ExecC1/rederive.md).

- Frozen route and probe hashes equal claims-container pins (`ExecC1/pins.json`). Probe extracted only, never executed.
- Own launcher/parser/check invocations: `ExecC1/rederive.py`.
- Route: exit 0, four of four carriers, met_target true (`ExecC1/c1-route.json`).
- Raw environment: 31 records (upx 21, node 2, readelf 8), each exactly HOME/LANG/PATH/TMPDIR; strict HOME/TMPDIR containment; exported canary absent (`ExecC1/env.jsonl`, `ExecC1/independent-results.json`).
- Own 32-byte nonce generated and commitment retained before launch; independent binding calculation matches.
- Checker: genuine exit 0; transplant exit 1 naming run_nonce absent; flipped nonce exit 1 naming run_nonce hash; zero binding exit 1 naming run_binding. Exact commands and outputs retained as `ExecC1/check-*.command.json` and `ExecC1/check-*.stdout`.
- Named evidence limitation: git children receive cenv in source but bypass recording wrapper (frozen route lines 758–764); no git record occurs in raw log. This contradicts a literal “record every child” description, not A8's narrower required child set.
- Full 10/10 seam predicate and A9 concurrency are outside this assigned independent subset; no such score is claimed here.
- Scratch removed by finally cleanup after retaining receipts/log. No tools installed, no external changes, no blocker.

VERDICT: met — assigned independent rederivation and rejection arms; defect named: git environment is routed but not runtime-recorded."} Scandin?}??