# ExecC1Verify — independent R73-C1 kernel witness

## Result

Independently reproduced the requested A12 after-state using a new observer, without importing or invoking seam-probe.py or reading its A12 receipts. Axes: independent observation, environment isolation, forgery discrimination, secret-free retention.

- Genuine checker: exit 0; five sampled shim processes, one git and four readelf. Every sample had exactly HOME/LANG/PATH/TMPDIR; canary absent; HOME equal to work/home and TMPDIR equal to work/tmp; LANG C; PATH began with our shim directory.
- Forged producer: exit 0. Its fabricated dump asserted exactly those four keys and no canary, but the independently sampled shim had the inherited caller key census, including KAIDOKU_ENV_CANARY. HOME was outside work; TMPDIR was work itself, not work/tmp. No environment values are retained: HOME/TMPDIR comparisons are booleans.
- This independently supports the kernel-witness discrimination, NOT the separate assertion that the full probe reports 12/12 arms. The 12-arm probe was deliberately not invoked.

## Exact retained evidence

All paths below are under `.ufo/waves/round-73/w1/ExecC1Verify/`:

- `observer.py`: reproducible independent /proc poller and generated shim/fixture sources. Genuine Perl shims only sleep 0.4 seconds and exec /usr/bin/git or /usr/bin/readelf. Forged three-line Python fixture calls the lying Perl shim with env=None.
- `genuine.json`: argv-selected shim samples. Producer PID 1532161; git PID 1532162; readelf PIDs 1532189, 1532193, 1532200, 1532208. All were direct children of that producer and /usr/bin/perl at sampling time. Each sample records start ticks and rechecks argv/start time around the environ read.
- `forged.json`: lying shim PID 1532214, direct child of fixture PID 1532213, /usr/bin/perl at sampling time. Contains the complete inherited KEY census only, canary presence, safe path-comparison booleans, and fabricated clean dump.
- `summary.json`: genuine_kernel_clean=true; forged_kernel_dirty=true; forged_dump_clean=true; sample counts 5 and 1; both subprocess exit codes 0.
- `packer-copy.json`: own scratch copy of /usr/bin/upx matched the pinned SHA256. Checker mode has no --expect-upx and does not invoke the packer; the copy was not used to manufacture packer coverage.

The genuine command was the assigned isolated packed-elf.py checker invocation at declaration da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b, with explicit --work, package root, declaration receipt and nonce commitment. The declaration receipt was an input to the checker, not trusted as observation evidence. Checker verdicts are retained separately from independently read kernel samples.

## What is and is not forgeable

The lying child cannot replace this observer's /proc read by writing a fabricated dump. The observation above was of PID **1532214**, not the fixture parent or a clean substitute. Under this fixture, changing the dump did not change the dirty kernel-visible sample.

A wrapper attacking an argv-only observer could arrange a clean decoy with matching argv while executing the dirty workload in a different process, or clean-exec the selected process before observation and run dirty work later. Checking PPID and start time narrows ordinary misidentification, but does not prove complete execution lineage or coverage between polls. [INFERENCE: these attacks were not exercised here.]

Important precision: /proc/PID/environ is kernel-served, but not an immutable signed execution history. An absolute statement that a child can never alter the bytes exposed there is too strong. [INFERENCE, not tested here: Linux reads the process's initial environment memory range; in-place modification of that memory, and privileged environment-range manipulation, are separate threats.] The measured conclusion is resistance to fabricated child dumps, not universal tamper-proofness of /proc.

## Scope, reproducibility and cleanup

No implementation files, frozen instruments, global settings, sibling lanes, git state, or credential values were changed. No tool installs or updates. No build/lint/formatter/test suite run; only the explicitly assigned measurement. LSP unavailable in the mounted tool inventory; no symbol refactor required.

Two harness setup errors were corrected before the retained successful run: a literal Perl backslash-n after the fabricated JSON, and a scratch directory retained because an EXIT trap in the persistent shell had not yet fired. The final invocation used an explicit subshell with an EXIT cleanup trap, removed only this seat's scratch directory, and completed with exit 0. All retained receipts precede scratch cleanup.

Self-evaluation: accuracy 4 (no in-place-memory attack measured); completeness 4 (12/12 tally outside this independent A12 exercise); clarity 4 (full inherited key census is lengthy but machine-readable); actionability 4 (rerun requires the original declaration inputs); conciseness 4 (identity/threat-boundary detail retained intentionally). Overall 4.0. No blocker to the assigned independent A12 measurement.
