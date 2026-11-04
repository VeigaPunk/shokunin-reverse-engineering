# Independent R73-C1 observation

Scoped findings: ../ExecC1Verify.md.

Genuine: checker exit 0; git PID 1532162 and readelf PIDs 1532189, 1532193, 1532200, 1532208, all direct children of checker PID 1532161. Every kernel sample has exactly HOME/LANG/PATH/TMPDIR, canary absent, HOME=work/home and TMPDIR=work/tmp (retained as comparisons only).

Forged: fixture exit 0; sampled lying Perl shim PID 1532214, parent 1532213. Fabricated dump clean; kernel key census dirty, canary present. No raw environment values retained.

Receipts: genuine.json, forged.json, summary.json, packer-copy.json. Independent reproduction harness: observer.py. No seam-probe/A12 call. No independent measurement of the full 12-arm tally.

A fabricated child dump cannot replace the independently sampled /proc bytes. [INFERENCE: a clean matching-argv decoy or changing execution phases could evade this bounded poller; in-place environment-memory modification also limits any assertion of absolute /proc immutability.] No such attack was exercised.

Scratch removed by the successful measurement's subshell EXIT trap. No installations, repository implementation edits, builds, linters or suite tests.
