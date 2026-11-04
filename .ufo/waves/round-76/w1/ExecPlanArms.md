# ExecPlanArms — round-76 w1: independent reproduction of R76-C2's three arms

Seat: ExecPlanArms (executor). Scope: read-only verification of
`tools/round-76/plan-command.py` at the freeze rev
`5824d5d8e135194a59db3df1533b76ff479753bf`; evidence written only under
`.ufo/waves/round-76/w1/ExecPlanArms/` and scratch
(`/fast/scratch/hyaku/kaidoku-r76/ExecPlanArms/`, deleted after the receipts
were copied here). No lane files were edited; no git/jj writes anywhere.

## Isolation (why everything ran from scratch)

The lane working tree is concurrently mutated by the wave: at measurement time
the working-tree `tools/round-76/plan-command.py` / `record-audit.py` hashed
(sha256) to `4766df5091cc…` / `18b2d7ba2ad…`, neither equal to the freeze pins
`f9c1cff3…` / `88e3c2ce…`, while the committed blobs are identical at the freeze
and at HEAD `201df797` (git-sha1 `3f617ef6` / `7ba1cce5`). All measured bytes
were therefore materialized from the freeze commit (`git archive 5824d5d8 |
tar -x`) into a scratch repo that also holds the freeze objects (verified:
`git rev-parse --show-toplevel` == the scratch dir; every input file verified
`git hash-object` == `git rev-parse 5824d5d8:<path>`). Children ran with
`cwd` inside the scratch tree and `TMPDIR` under the scratch work dir; the
lane was only ever read (`git show`/`log`/`status`).

## Rows 1–3: independent reproduction (no `--battery`, gate code not imported)

Driver: `repro.py` in scratch (raw output: `repro-rows.json` here). It
re-implements the block extraction (own regex on the `counting-command`
comments and the `sh` fence), joins `\`-continuations, `shlex.split`s, and
executes with `subprocess.run(..., shell=False)` under a four-key child env
(PATH/HOME/TMPDIR/LANG), cwd = scratch freeze tree.

1. **r75-printed.md** — argv carries the Unicode ellipsis: token
   `1fc1c8fc\u2026` (`ellipsis_present_in_argv: true`). The driver's own
   static grammar reports exactly `PLACEHOLDER_UNBOUND: abbreviation '…'` —
   the refusal the gate applies statically instead of executing. Executed
   directly with `shell=False`: **rc 2**, output
   `{"unevaluable": "missing required arguments: work"}`. Matches the
   declared rc and message.
2. **r75-argv.md** — digest bound (`1fc1c8fc6d08b…410d`), no ellipsis, static
   grammar clean, so it **executes**: **rc 2**, same
   `missing required arguments: work` message (the round-75 instrument's own
   preflight — no `--work`). Matches the declared rc and message.
3. **plan `counting-command: C1` block at the freeze rev** —
   `python3 -I -B tools/round-76/record-audit.py --root . --rev $REV --json-out $OUT`
   executed verbatim with only `$REV`→`5824d5d8…` and `$OUT`→scratch receipt
   substituted: **rc 1**, receipt `mismatch_count: 1`,
   `mismatches: ["D24_capability_rows"]`, whose defects name exactly
   `A12 case-independence closure` and `exact-grammar record audit`;
   `validate: {atoms: 9, defects: []}` (nine atoms D16–D24, defect-free
   validate block). The value 1 is the declared freeze-state (landing 0 is
   R76-C1's business; the C2 arm is executability-only).

## Gate self-checks (the gate's claims about itself)

- `--battery` at the freeze rev (`--root . --rev 5824d5d8… --work <scratch>`,
  run under `strace -f -e trace=execve`): **exit 0, arms_ok 3, arms_total 3,
  ok true**. plan-c1 observed `rc 1, mismatch_count 1`; r75-printed observed
  `PLACEHOLDER_UNBOUND: abbreviation '…'` with `executed: false`;
  r75-argv observed `EXECUTION_FAILED: rc 2` carrying
  `missing required arguments: work`. The battery receipt's
  `arms[0].row.argv[0:3] == ["python3", "-I", "-B"]` (the four-part
  `python3 -I -B <script>` form).
- `--selftest`: exit 0, 3 cases (`ellipsis-rev`, `missing-required-arg`,
  `prose-plan`), `failures: []`.
- one `--control ellipsis-rev`: exit 0, `met: true`,
  `PLACEHOLDER_UNBOUND: abbreviation '…'`, `executed: false`.
- **No shell ever spawned**: the strace log (`execve-battery.log`, 464 lines)
  contains only `execve` of `git` (31 show/log calls, PATH-probed across the
  host's 12 PATH entries — the `fnm_multishells` strings are directory names
  in PATH, not executed programs) and `python3` (3 children: the gate,
  record-audit, probe-mutation). Shell-spawn regex hits: **0**.
  `grep -c 'shell=True' tools/round-76/plan-command.py` → **0**, and the only
  `shell` tokens in the source are a docstring line and a comment; both
  `subprocess.run` call sites omit the `shell` keyword (default `False`).

## Cross-checks against the committed pre receipts (at the freeze)

- `pre/c2-at-declaration.json`: arms_ok 3, exit 0, all arms met — identical
  to this battery run.
- `pre/c2-at-base.json`: arms_ok 0, exit 1 — the claim's before-state.
- `pre/r75-printed-exec.txt`: hand-run exit 2 with
  `missing required arguments: work` for both forms — matches rows 1–2.
- `pre/c1-at-declaration.json`: mismatch 1 — consistent with row 3.

## Acceptance mapping

Rows 1–3 reproduce the declared rc and message (2/2/1); the gate's battery at
the freeze rev reports arms_ok 3; `grep -c 'shell=True'` is 0 with a matching
strace; the receipt argv is the four-part `python3 -I -B` form. **No
deviations; defects: none.**

## Risks / notes

- The lane working tree is being edited live by the wave (instrument files
  differed from the freeze pins at measurement time, committed blobs did
  not). Any seat re-running these checks from the lane tree instead of the
  freeze commit may see different bytes. This seat's numbers are pinned to
  `git archive 5824d5d8` bytes, hash-verified against `claims.json`.
- Row 3 and the battery's plan-c1 arm necessarily execute `record-audit.py`,
  which performs ~31 read-only `git show`/`git log` calls against the scratch
  repo; nothing writes outside the scratch work root.
- No tools were installed or upgraded (strace and python3 already present).
