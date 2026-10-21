# R22-C2 receipt path and revision-identity review

Target: `.ufo/waves/round-22/tools/count-c2.py`, current worktree SHA-256 `eaf3ddf305a50c70172eca40857be68b02d047660b3bbdfbe92e82cafe7c946c`; observed lane HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`. All probes used Python 3.14.8 (`/usr/bin/python3`) and Git 2.56.0. Mutations were confined to `/tmp/c2probe`; the only lane writes are this report and `C2Path.json`. No tools installed.

## Findings (severity order)

### High — `refs/replace` lets different tree contents pass under the requested commit SHA

`measure()` resolves `--rev` at `count-c2.py:147-152`, then reads `PROVINCE.md` and receipts through `git_show()` at `:40-45`, `:153`, and `:115-116`. Git's default replacement-object behavior is enabled for every subprocess. Thus the reported resolved SHA is not necessarily the object content actually read.

Concrete scratch proof (`/tmp/c2probe/replace-proof.py`): original commit `c6beadb5ad8b3567dac9450ec8cf0c8b254851b7` contains only `# Province has no catalog dispositions`; before replacement, the exact counter invocation exits 1 with `accounted_count: 0`. A separate commit `3f668f6b9a9364792c3d1240f97d6bb0aadfe4ac` contains the complete fourteen-row fixture. After `git replace c6beadb5ad8b3567dac9450ec8cf0c8b254851b7 3f668f6b9a9364792c3d1240f97d6bb0aadfe4ac`, the same `--root` and `--rev c6be...` returns exit 0, `finding:"dispositions_complete"`, `accounted_count:14`, while still reporting `rev:"c6be..."`. Running that same command with `GIT_NO_REPLACE_OBJECTS=1` returns exit 1 and count 0. Exact argv, stdout, stderr, and exits are in the JSON attachment.

This is an identity/rerouting false positive, not a provider-availability result. Narrow fix: force replacement objects off for **every** Git subprocess (e.g. controlled `GIT_NO_REPLACE_OBJECTS=1` environment, rather than relying on caller state).

### Medium — inherited `GIT_DIR` overrides the explicit `--root`

Both Git subprocess sites use `git -C root` without a controlled `env` (`count-c2.py:40-42`, `:148-149`). Git honors `GIT_DIR` over `-C`, so the command may resolve and measure a different repository than the caller-selected root.

Concrete isolated-repository proof (`/tmp/c2probe/gdir-proof`): `--root /tmp/c2probe/gdir-proof/good` contains incomplete commit `33ad48471f772a781e6d2cd32fb97a1090108955`; complete fixture commit `a03c1f722dc6cf33ed2610e46a0a9a8867ddf8ea` exists only in `/tmp/c2probe/gdir-proof/evil`. The same argv `--root /tmp/c2probe/gdir-proof/good --rev a03c1f722dc6cf33ed2610e46a0a9a8867ddf8ea` without overrides returns exit 2, `{"finding":"unevaluable","error":"invalid_revision"}`; with `GIT_DIR=/tmp/c2probe/gdir-proof/evil/.git`, it exits 0 with 14/14 and reports that foreign revision. Full raw stdout is attached. Narrow fix: run all Git commands with a sanitized, consistent repository environment; at minimum remove `GIT_DIR` so `-C --root` remains authoritative. Consider other repository/object-store override variables in that same allowlist/denylist policy.

## Path traversal and prefix checks — no actionable finding

The current guard at `count-c2.py:112-114` requires the exact `RECEIPT_PREFIX` including its trailing slash and rejects any `..` path component before calling Git. Scratch commits with a planted valid envelope outside the prefix and receipt `.ufo/waves/round-22/evidence/c2/../../evil.json` produce exit 1, `accounted_count:13`, and `inspect-packet-fields.status:"receipt_outside_prefix"`. A `c2x/...` sibling-prefix receipt is rejected the same way. Direct `git show <rev>:.ufo/waves/round-22/evidence/c2/../../evil.json` independently fails exit 128 (`fatal: path ... does not exist`). Exact argv/stdout/stderr for these controls are attached.

Positive control: `python3 -I -B .../count-c2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD` exits 0 with `accounted_count:14`, `mismatched:[]`, `foreign_rows:[]`. Revision-only behavior is otherwise correct for ordinary Git state: dirtying a committed receipt in the scratch worktree leaves the committed-revision measurement at 14/14, while a receipt added only after its referenced commit is `receipt_absent` (exit 1). Exact stdout is attached.

## Verification gap / residual risk

The current `--selftest` exits 1 (`counter_controls_failed`, 28 cases; stderr empty). Its sole failing case is `recursive_receipt`: fixture expected `receipt_unevaluable`, but this Python 3.14.8 run parses the 2,000-deep array and correctly returns `receipt_not_envelope` (exit 1, count 13). The input is still refused; the fixture expectation or nesting depth needs alignment before describing the self-test as clean.

The lane repository had no `refs/replace` entries when checked. I did not test every Git environment/configuration override, only the demonstrated `GIT_DIR` case. The counter's own printed limit remains appropriately narrow: it validates observed row/receipt agreement, not reason/placement semantics, run metadata, evidence authentication, or provider availability over time. No such availability claim is made here.
