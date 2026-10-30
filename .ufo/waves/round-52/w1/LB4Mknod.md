# LB4Mknod — kernel branch-asymmetry probe

Verdict: **not established / hypothesis contradicted in the initial execution context**. The repeated three-probe batch ran as the current process (not established as unprivileged): `mkfifo`, char-device `os.mknod(0:0)`, and AF_UNIX bind all returned 0 twice. Thus the char-device operation did not raise EPERM, so this host observation cannot support the proposed unprivileged asymmetry; do not cite it as evidence for S252's CAP_MKNOD branch.

A follow-up attempted to run as `nobody` using `runuser`; all six commands exited 1 before executing, stderr `runuser: may not be used by non-root users`. This is an environment limitation, not probe evidence. Required unprivileged trial remains unmeasured. The successful device creation suggests current credentials/capabilities may permit it [INFERENCE]; identity/capabilities were not measured.

Receipts: `LB4Mknod/probe-receipts.json` includes both initial-context repetitions and failed nobody invocation repetitions, exact exit codes, stdout SHA-256, stderr and UTC timestamps. Each initial-created node was unlinked after its probe. Scratch directory was removed after copying receipts. No REA, build or tests run. No tools installed.
