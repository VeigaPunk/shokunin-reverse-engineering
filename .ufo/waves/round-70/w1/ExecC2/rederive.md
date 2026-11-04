# ExecC2 — independent R70-C2 re-derivation

Axes: execution ordering; validated-path threading; child-environment isolation; typed failures; per-run scratch isolation.

## Method and identity

Read the claims plan and container `claims[1]`. Never ran or imported `seam-probe.py`. Own retained harness: `harness.py`; raw commands, return codes, stdout and stderr: scenario-named JSON files and aggregate `evidence.json` in this directory. The harness extracted committed blobs with `git show`, ran independent adversarial fixtures, and removed its scratch root in `finally` after persisting receipts.

- Base: `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d`, `tools/round-69/packed-elf.py`, SHA256 `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`.
- Freeze: `4737a542ae3b1b910d8fe43efbd572bc578b07c6`, `tools/round-70/packed-elf.py`, SHA256 `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`.
- Frozen mutation checker SHA256 `d2d9a49f509e9ec2aad3f38ec9c3b7e520a816dc3dc9d73810fc4c62510934a9`.
- Own packer copy SHA256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`.

## Base versus freeze

| Scenario / arm | Base observation | Freeze observation |
|---|---|---|
| A1 impostor: prints pinned banner and appends execution marker | rc 2, `packer_mismatch: sha256`; marker **exists** (`executed`) | rc 2, `packer_mismatch: sha256`; marker **absent** |
| A2 pinned-copy live carrier run | rc 0; 3/3 carriers; every recorded pack/unpack argv[0] `/usr/bin/upx`, ignoring supplied copy | rc 0; 4/4 carriers; every recorded pack/unpack argv[0] `/fast/scratch/hyaku/kaidoku-r70/ExecC2/pinned-upx` |
| A3 committed child-env cases and selftest | rc 0; 20 cases, failed `[]`; no child-env registry cases | rc 0; 23 cases, failed `[]`; registry includes `child-env-allowlist`, `child-env-home-in-work`, `child-env-no-tmp` |
| A4 broken node shim (`exit 7`) | rc 2; misleading `carrier jq: original inventory below the floor (None)`; no traceback | rc 2; `broken_tool: node (banner '')`; no traceback |
| A5 executable text without shebang | rc 1; Python traceback, `OSError: [Errno 8] Exec format error` | rc 2; `packer_mismatch: sha256`; no traceback; refused before attempted execution |
| A6 HOME / child env | live receipt has no child-env audit | live receipt keys exactly HOME/LANG/PATH/TMPDIR; HOME and TMPDIR under supplied work; registered no-temporary-root case green |
| A7 repeated frozen battery, identical `--work`, `--patch-set r70 --min-pristine-cases 0` | Base battery not run by this assignment | Both rc 0; distinct work_dir values below; pristine 23 cases, failed `[]`; five mutants killed in their expected cases |

No injected scenario produced a freeze traceback. Both full pinned-copy runs were real executions using the requested REA package; no mocked REA results.

Frozen battery work directories:

1. `/fast/scratch/hyaku/kaidoku-r70/ExecC2/battery-work/mutation-check-bgb6s3pq`
2. `/fast/scratch/hyaku/kaidoku-r70/ExecC2/battery-work/mutation-check-5_cyqkpd`

## Producer binding and source corroboration

`producer-checks.json` retains a separate frozen-checker check of the independently produced freeze receipt: rc 0, met true, failing `[]`. Changing only its producer SHA256 to zeroes yielded rc 1 with `instrument.sha256 ... != blob at 4737a542...`. Thus A2's observed argv is not accepted under a false producer identity.

An additional attempted frozen-checker invocation at the base revision returned rc 2 because that revision has no `tools/round-70/packed-elf.py`; it is not evidence against the base producer and is retained transparently, not counted as a failed seam arm.

Frozen source inspection: lines 154–167 build HOME/TMPDIR from work and return exactly four keys; 317–318 refuse mismatching hash before line 323 executes the packer; 333–339 type broken node; 499 binds `upx_v` from preflight; 563/567/573 use it for pack/list/unpack with the child environment. Base lines 253–259 execute before hashing; 387/391/397 instead use the module constant. No LSP device was available in this seat's exposed tool inventory; symbol locations were read directly, not inferred from empty LSP results.

## Limits, scope and handoff

This independently reproduces the assigned experiments and supports the seven after-properties. It does **not** claim to have executed the complete frozen predicate or independently measured a base 0/7: the assignment prohibited the official seam probe and requested only the frozen repeated battery. A3/A6 combine committed-source/registry inspection with green selftests and the genuine live receipt; they are not OS-level child-environment tracing. A5 demonstrates early hash refusal of unpinned malformed bytes, not an exec-format failure of matching pinned bytes.

Only own findings and scratch were written; scratch was removed after evidence retention. No instrument edits, git mutations, installs, commits, deployments or global changes. No additional build/lint/formatter runs. Parent may integrate these results with the other seats' full predicate evidence.

VERDICT: met — all assigned independent R70-C2 experiments support the frozen seam repairs; base defects reproduced, with full base 0/7 explicitly not asserted.
