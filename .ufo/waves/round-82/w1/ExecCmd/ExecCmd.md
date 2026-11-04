# ExecCmd — round 82

Axes: executed-byte fidelity, frozen-revision reproducibility, minimal integration surface. Advisory only; no admission or promotion verdict.

## Observed results

Frozen revision: `2d63e1a7d04d4dcff45c3908bb51be787a2f22e1`; declaration: `42c78912733357dabe8fcaf513a09c4a3c4ba2aa`.

- Guarded frozen C2 replay returned **rc 1, arms_ok 5, arms_total 6, validate defects []**. Only `sourced` was unmet: `SOURCED_ROW_UNMET`, `SOURCED_ENTRY_UNCITED`. At that revision S299 is absent, the base also lacks it, and the plan names it. The current worktree already contains an S299 row; that does not change revision-bound scoring.
- This was **not an exact printed-CLI replay**. `probe.py` loads the frozen blob and calls its battery, redirecting the selftest child through a guard. The frozen selftest uses `git init` without the required absolute `-C`; the guard normalizes that invocation and asserts private fixture toplevel before add/commit. All six arm implementations otherwise remain the frozen definitions. L1 owns exact post-integration command execution.
- Actual instrument file and frozen blob matched before execution and the file SHA256 remained equal afterward: `d447f6b487f2f9b39e0585ddf48f41cf4068cb5da6f64a299cf7be3066aacd8c`; git blob `53f7d4563f5b1b851775b664f725bcfd60d470a3`.

## Concrete counterexample

`pin_matches()` hashes `git show REV:script`, but `subprocess.run(argv, cwd=root)` executes the worktree path at `argv[3]`.

The private fixture committed a pinned `member.py`, then changed only its working bytes. Both clean and dirty `run_block()` calls executed at rc 0, returned integer `cases=1`, and reported no defects. The clean receipt says `origin=pinned`; the dirty receipt says `origin=WORKTREE_DIVERGENCE`.

Pinned SHA256: `afdb00cd88fd5e5e664e1f040353d804af25e817311e700b6dd6d8261414229c`.
Dirty executed SHA256: `379c05a46d82b97be5f157dec13f79d6a64cf79c65bd6985adcb6e2b02f474c1`.

This is an observed mismatch between verified git bytes and executed argv-path bytes, not a speculative attack.

## Minimal candidate

`actual-argv-pin.patch` extends the existing pin check to reject symlink resolution and hash the on-disk path actually selected by `argv[3]`, in addition to checking the revision blob. On the same dirty fixture the candidate returned `executed=false`, `rc=null`, and `REFUSED: SCRIPT_PIN_MISMATCH: member.py executed path differs from the pin`.

Limit: this closes the demonstrated persistent worktree divergence, **not concurrent replacement between hashing and Python opening the script**. No claim of race-free pin binding. Race-free execution requires consuming immutable verified bytes; preserving the exact printed argv and script-relative behavior needs a deliberate L1 decision. Candidate full-battery compatibility was subsequently exercised in the isolated outer-CLI fixture below. Lane integration remains unverified. Adopting the patch changes the instrument digest and therefore requires explicit pin/supersession handling by L1, not this seat.

### L1-requested isolated outer CLI extension

`outer-probe.py` builds a private fixture from source-entry revision `eb227c4694e16cb8fae74df0eea2f07643b46124`, applies the repair, fixes frozen selftest git-init to explicit absolute `-C`, asserts private toplevel before fixture writes, updates only the fixture instrument pin, and commits that private candidate. The isolated measured candidate revision was `b77b02d649edfee4dd8d1fe257667669e1906704`, not the unchanged source-entry revision.

- Outer candidate `--battery`: **rc 0, arms_ok 6/6, validate defects []**, fixture finding-id `C2_ALL_ARMS_MET`, assertion true.
- After changing the actual C1 script path without changing its pinned blob, outer candidate `--run --block C1`: **rc 1, executed false**, stable refusal id `SCRIPT_PIN_MISMATCH`, assertion true.
- Candidate SHA256: `5cbbcaf730aad7ba3eedc748c426845e73270c4cfc3948d8337446c7fd25d4ba`.
- Retained: `outer-green.json`, `outer-red.json`, corresponding `outer-*-execution.json` with actual argv/exit/assertions, `outer-cleanup.json`, `outer-probe.py`, `candidate-printed-command.py`, and `actual-argv-pin-with-fixture-guard.patch`. Original frozen receipts and minimal patch remain unchanged. Scratch again removed in `finally`; private `TMPDIR` was explicitly set.

The green fixture finding-id is a harness label, not a new instrument-emitted finding. The red finding-id is asserted against the instrument's actual refusal text.

## Retained evidence

All paths below are relative to `.ufo/waves/round-82/w1/ExecCmd/`:

- `probe.py`: bounded driver, guard, fixture construction, candidate generation and scratch cleanup.
- `battery.json`, `battery.stdout.txt`, `battery.stderr.txt`: full six-arm receipt and summaries.
- `battery-invocation.json`: guarded dispatch disclosure, rc, revision, final file hash.
- `byte-audit.json`: frozen/worktree SHA256 and git blob comparison; LSP unavailable (no LSP tool exposed).
- `divergence.json`: original clean/dirty argv, outcomes, payloads and hashes.
- `actual-argv-pin.patch`: candidate only; no production edits.
- `candidate-divergence.json`: observed dirty-path refusal.
- `tooling.json`: Python 3.14.8, git 2.56.0, pre-existing host tools; no installs/updates.
- `cleanup.json`: private scratch removal outcome.

Invocation: `TMPDIR=/fast/scratch/hyaku/kaidoku-r82/ExecCmd/tmp GIT_OPTIONAL_LOCKS=0 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/w1/ExecCmd/probe.py`.

Only assigned bounded demonstrations ran; no build/lint/format/test sweeps. Scratch stayed under the single assigned path and was removed in `finally`. No scratch inventory, PATH-directory writes, installs, production edits, external remediation, or delegation.

## Process disclosure and limits

An initial inspection mistakenly invoked `jj log` without disabling automatic snapshots; output was `qolqsyvyxonp c576015a63fb`. Such a read can implicitly snapshot jj state. No intentional jj/git mutation was issued against the lane, but I cannot assert this invocation left jj state unchanged. No rollback attempted. Subsequent lane git reads disabled optional locks. Also, initial named finite bash calls were interpreted as services by the tool; they exited rc 0, and the mismatch was reported through tool QA. No ongoing/background task remains from the evidence driver.

Conflicting report trailers were resolved to the explicitly assigned own-seat directory: this file. No report written outside that directory.

L1 checks to run after integration: exact lane C2 printed command with retained argv, updated pins and any required race-resistant execution design. Isolated candidate full-battery green and outer-CLI dirty-path refusal are retained above. Frozen sourced absence is expected pre-integration, not a new production repair request.

## Self-evaluation

Accuracy 4/5: receipts directly establish the counterexample; guarded replay is not exact CLI evidence. Completeness 4/5: all reachable scoped demonstrations retained; exact replay constrained by frozen fixture writes. Clarity 4/5: explicit separation of baseline, guard and candidate; full details require opening receipts. Actionability 4/5: minimal patch supplied; race-free execution remains an L1 decision. Conciseness 4/5: process disclosure adds necessary length. Overall 4.0/5. Improvements: prioritize race-free execution design, then exact integrated command evidence. User agreement is not assumed.
