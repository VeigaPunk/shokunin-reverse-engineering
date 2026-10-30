# LB3CensusIdem — census guard falsifiability

Verdict: hypothesis supported; not falsified. `census3.py --check` is able to reject tampered census bytes.

- Baseline against the detached shared clone at `ab0eafedc41402b43b41a4362084119578dfe7ce`: exit 0; 56 registry and census paths, no outside/unregistered paths or duplicates.
- Tamper: removed first listed path (`tools/round-41/c1-counter.py`) from a scratch copy and used the supported offline `--rev WORKTREE --census tools/round-51/census3-tampered.json` invocation. Both independent runs exited 1 and named the missing path in `census_outside`.
- Determinism: tampered outputs identical across the two runs (same JSON findings; invocation's `rev` and census path are identical).
- No lane files modified except this seat's evidence, report, and required status. No REA run; no tools installed.

Receipts (each `.meta` includes the exact command, UTC capture time, and stdout SHA-256; `.exit`, `.stdout`, `.stderr` are adjacent):
- `.ufo/waves/round-52/w1/LB3CensusIdem/baseline.{meta,exit,stdout,stderr}`
- `.ufo/waves/round-52/w1/LB3CensusIdem/tampered-1.{meta,exit,stdout,stderr}`
- `.ufo/waves/round-52/w1/LB3CensusIdem/tampered-2.{meta,exit,stdout,stderr}`

Risk/limitation: this is an offline guard falsifiability probe using a synthetic altered census, not a freeze-time census audit. It establishes that drift can be detected, not the future v6 instrument's behavior. The supplied disk-guard invocation `disk-guard.sh status` was malformed for this script: it printed usage and exited 1; no scratch-heavy work was done.
