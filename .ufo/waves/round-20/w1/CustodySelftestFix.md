# Custody selftest D1

Base observed in the writer clone: `14f0260ad319ecc26994381b2415d5a999003375`.

## Implementation

- `custody-pair.py:886-916` walks the resolved scratch path's ancestors for a `.git` entry and refuses worktree scratch with exit 2 and `scratch_inside_worktree` before creating a fixture root.
- `custody-pair.py:1532-1541` wraps the implementation in `try/finally` and removes its root on normal return or exception. The new cases at `:1255-1305` cover worktree refusal and successful/failing-run cleanup.
- `custody-pair.py:1524-1529` uses the contract selftest summary and exit code; `README.md:55` documents D1.

## Before / after evidence

**Before (baseline B):**

Command: `python3 -I -B /tmp/kr20-CustodySelftestFix-2/.ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/kr20-CustodySelftestFix-2-before-bva2yyud` (isolated temporary `HOME`); exit 0.

Last line: `CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0`

Observed after return: `BASELINE_RESIDUE: /var/tmp/kr20-CustodySelftestFix-2-before-bva2yyud/custody-pair-selftest-9vhhjew1 git_repositories=repo-fixture,repo-sub-fixture`; both nested `.git` directories existed. The outer temporary directory was then removed.

The requested baseline run with scratch inside the clone was not performed: shared contract `contract.md:23-25` prohibits selftest scratch inside any Git worktree. The baseline was instead run under a `tempfile.mkdtemp()` directory in `/var/tmp`, which demonstrates the same nested-repository residue without violating that bound.

**After:**

Command: `python3 -I -B /tmp/kr20-CustodySelftestFix-2/.ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/kr20-CustodySelftestFix-2-after-cl3d6c7w` (isolated temporary `HOME`); exit 0.

Observed case lines: `case scratch_in_worktree_refused                PASS`; `case cleanup_after_run                          PASS`.

Exact last line: `SELFTEST: CLEAN cases=33` (exit 0). No `custody-pair-selftest-*` directory remained under the supplied scratch after return; the outer temporary directory was removed.

## Commands and patch

- Clone/checkout/revision command: `test ! -e /tmp/kr20-CustodySelftestFix-2 && git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-CustodySelftestFix-2 && git -C /tmp/kr20-CustodySelftestFix-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-CustodySelftestFix-2 rev-parse HEAD` — exit 0; observed revision matches the baseline above.
- Before command above — exit 0.
- After command above — exit 0.
- Patch command: `git -C /tmp/kr20-CustodySelftestFix-2 add .ufo/gates/custody-pair/custody-pair.py .ufo/gates/custody-pair/README.md && git -C /tmp/kr20-CustodySelftestFix-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/CustodySelftestFix-2.patch && git -C /tmp/kr20-CustodySelftestFix-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0.

Stat: `.ufo/gates/custody-pair/README.md | 1 +`; `.ufo/gates/custody-pair/custody-pair.py | 97 ++++++++++++++++++++++++++++++---`; `2 files changed, 91 insertions(+), 7 deletions(-)`.

Patch: `.ufo/waves/round-20/w1/patches/CustodySelftestFix-2.patch`.

No tools installed or updated.