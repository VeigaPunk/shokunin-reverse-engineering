# ExecAxisFitGate — round-30 axis-fit gate (the M30-1 fix), built in scratch and shown able to fail

## Result

**Built** the gate designated as M30-1's fix by `ScribeMistakeAxisMisfit` (lane target path
`tools/round-30/axis-fit-gate.py`; this seat wrote it in scratch only and the L1 integrates/commits it):

| | |
|---|---|
| scratch artifact | `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecAxisFitGate/axis-fit-gate.py` |
| sha256 | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` (492 lines, mode 0755) |
| selftest | `python3 -I -B axis-fit-gate.py --selftest` → **exit 0**, `selftest cases=18 failures=0` |
| round-29, clone rev `4ee65c67…` | **exit 1** — `SURFACE_MISSING`×2, `UNMOVED_COMMAND_MISSING`×2, `RECEIPTS_ABSENT` |
| round-30, clone rev `4ee65c67…` (the freeze) | **exit 1** — `RECEIPTS_ABSENT` (surface/unmoved_command both `ok`) |
| extra sandbox fixtures on the real claims | round-30 + valid receipts → **exit 0** PASS; round-29 + receipts committed after its envelopes → **exit 1** `RECEIPTS_NOT_BEFORE_ENVELOPES` |

Both required runs exit 1, as the item demands. "Shown able to fail" is carried by 12 red fixtures
(exit 1) and 3 unreadable fixtures (exit 2) in the selftest plus the two real-run failures; the
green fixtures and the real-claim green sandbox run show the gate is not trivially red.

## What the gate checks (item clause → implementation) — [observation]

- `--root <lane> --round <N> [--rev <rev>]`; `--rev` defaults to `HEAD`; the round is read from
  `<rev>:.ufo/waves/round-<N>/claims.json` through `git cat-file`/`git show` (Git objects only,
  never the worktree). `--root` must be the repository top (`rev-parse --show-prefix` empty).
- For each claim whose `axis` **begins with** `coverage` or `depth` (regex `^(coverage|depth)\b`, so
  round-29's `coverage (learning claim: …)` matches, as the round-29 run shows): nonempty string
  `surface` and nonempty string `unmoved_command` are required, else `SURFACE_MISSING|SURFACE_EMPTY`
  / `UNMOVED_COMMAND_MISSING|UNMOVED_COMMAND_EMPTY` naming the claim id.
- When at least one such claim exists, `<rev>:.ufo/waves/round-<N>/controls/receipts.tsv` must be a
  blob (else `RECEIPTS_ABSENT`), header exactly `claim<TAB>control<TAB>counter_exit<TAB>met_target`
  (else `RECEIPTS_HEADER_INVALID`), every row four nonempty cells with integer `counter_exit` (else
  `RECEIPTS_ROW_INVALID`) and `met_target` exactly `no` (else `MET_TARGET_YES` / `MET_TARGET_INVALID`).
- Ordering: the first commit (in the history walked from `--rev`, `--diff-filter=A`) that **adds** the
  receipts file must be strictly earlier by committer timestamp than the first commit that adds any
  path matching `corpus/evidence/round-<N>/<one-segment>/envelopes/**`; equal or later →
  `RECEIPTS_NOT_BEFORE_ENVELOPES` with both commits/ct/path. No envelope path yet → clause vacuous
  (note printed). The gate also reports whether the receipts commit is an ancestor of the first
  envelope commit; the selftest covers same-commit (`red-receipts-same-commit`).
- Per axis claim, every control named in the claims file's top-level `controls_required_before_data`
  must appear in the receipts for that claim, else `CONTROL_MISSING` (claim + frozen name). A receipt
  `control` cell satisfies a frozen name when the cells are equal, **or** when the cell equals the
  frozen name's text before the first ` (` (short id) and that head names exactly one frozen control
  (`red-control-head-ambiguous` shows the guard: `dup` for `['dup (a)','dup (b)']` does not satisfy
  either). Round-30's five names have distinct heads, so both spellings are accepted — the L1 may
  write the short id or the full frozen string in the receipts.
- Absent/empty `controls_required_before_data` names no control: a note, not a finding (round 29's
  case). A malformed list is `CONTROLS_LIST_INVALID`. A non-dict entry in `claims` is `CLAIM_INVALID`.
- Exit codes: **0** every requirement holds, **1** one or more findings (all printed), **2**
  unevaluable (`claims_absent`, `claims_invalid`, git failure, root not a repository top, receipts
  blob present but no adding commit in the walked history).

## Evidence — commands, stdout, exit, UTC

All commands run 2026-10-23T02:45Z–02:47:27Z UTC, each under `timeout 300/900`, cwd
`/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecAxisFitGate`; no REA run, no carrier or mutant read or
executed, no lane write.

Sandbox clone (full, `main` at the freeze commit):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C clone rev-parse HEAD
4ee65c6771058284aa947a266475839d196ed4d4        # branch main
```

### 1. Selftest — `python3 -I -B axis-fit-gate.py --selftest` → exit 0 (UTC 2026-10-23T02:47:27Z)

```
ok green-basic exit=0 findings=-
ok green-pre-data-no-envelopes exit=0 findings=-
ok green-other-axis-only exit=0 findings=-
ok red-surface-missing exit=1 findings=SURFACE_MISSING
ok red-surface-blank exit=1 findings=SURFACE_EMPTY
ok red-unmoved-missing exit=1 findings=UNMOVED_COMMAND_MISSING
ok red-receipts-absent exit=1 findings=RECEIPTS_ABSENT
ok red-receipts-after-envelopes exit=1 findings=RECEIPTS_NOT_BEFORE_ENVELOPES
ok red-receipts-same-commit exit=1 findings=RECEIPTS_NOT_BEFORE_ENVELOPES
ok red-met-target-yes exit=1 findings=MET_TARGET_YES
ok red-control-missing exit=1 findings=CONTROL_MISSING
ok red-control-head-ambiguous exit=1 findings=CONTROL_MISSING
ok red-header-invalid exit=1 findings=CONTROL_MISSING,RECEIPTS_HEADER_INVALID
ok red-row-invalid exit=1 findings=RECEIPTS_ROW_INVALID
ok red-counter-exit-not-int exit=1 findings=RECEIPTS_ROW_INVALID
ok red-claims-absent exit=2 findings=-
ok red-claims-invalid-json exit=2 findings=-
ok red-not-a-repo exit=2 findings=-
selftest cases=18 failures=0
```

Fixtures are built by the tool itself in a `tempfile.mkdtemp` sandbox, each case its own
`git init -q -b main` repository, commits with fixed `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`
(`2026-01-01T00:00:00 +0000`, `+1 min`) so the ordering clause is deterministic; each case is run as
`python3 -I -B <this file> --root <fixture> --round 99 --rev main` and judged on exit code plus the
exact finding-code set.

### 2. Round 29 on the clone — exit 1

`python3 -I -B axis-fit-gate.py --root clone --round 29 --rev 4ee65c6771058284aa947a266475839d196ed4d4`

```
{"axis_claims": [{"axis": "coverage (learning claim: PROVINCE Frontier bullet 'EVM bytecode (extended)', selector naming on carriers the lane has never held)", "claim": "R29-C1", "surface": "missing", "unmoved_command": "missing"}, {"axis": "depth (learning claim: what openchain's filtered flag means, tested on selectors never fetched)", "claim": "R29-C2", "surface": "missing", "unmoved_command": "missing"}], "claim": "R30-axis-fit-gate", "claims_file": ".ufo/waves/round-29/claims.json", "findings": [{"claim": "R29-C1", "finding": "SURFACE_MISSING"}, {"claim": "R29-C1", "finding": "UNMOVED_COMMAND_MISSING"}, {"claim": "R29-C2", "finding": "SURFACE_MISSING"}, {"claim": "R29-C2", "finding": "UNMOVED_COMMAND_MISSING"}, {"finding": "RECEIPTS_ABSENT", "path": ".ufo/waves/round-29/controls/receipts.tsv"}], "notes": ["controls_required_before_data absent: no control is named"], "receipts": {"path": ".ufo/waves/round-29/controls/receipts.tsv", "present": false}, "required_controls": [], "rev": "4ee65c6771058284aa947a266475839d196ed4d4", "round": 29, "verdict": "FAIL"}
```

Same stdout and exit 1 at the round-29 freeze rev `dbd87cfa09eb89306c4e07d3171a4556eb732024`
(`run-round29-freeze.txt`) — the failure is not an artifact of the measured rev. The reasons are
exactly the two the item predicts: no surface fields, no receipts.

### 3. Round 30 at the freeze — exit 1

`python3 -I -B axis-fit-gate.py --root clone --round 30 --rev 4ee65c6771058284aa947a266475839d196ed4d4`

```
{"axis_claims": [{"axis": "coverage", "claim": "R30-C1", "surface": "ok", "unmoved_command": "ok"}, {"axis": "depth", "claim": "R30-C2", "surface": "ok", "unmoved_command": "ok"}], "claim": "R30-axis-fit-gate", "claims_file": ".ufo/waves/round-30/claims.json", "findings": [{"finding": "RECEIPTS_ABSENT", "path": ".ufo/waves/round-30/controls/receipts.tsv"}], "notes": [], "receipts": {"path": ".ufo/waves/round-30/controls/receipts.tsv", "present": false}, "required_controls": ["do-nothing", "junk-row (entry + PROVINCE/SKILL lines without envelopes)", "all-false (committed refusal or null-metadata envelopes)", "no-reader (envelopes fabricated from the oracle reading, never produced by REA)", "shortcut keyed on ids/labels (another carrier's or mutant's envelope under the id; predictions copied as observations)"], "rev": "4ee65c6771058284aa947a266475839d196ed4d4", "round": 30, "verdict": "FAIL"}
```

Exactly one finding: the receipts file is absent, as the item states.

### 4. Two extra fixtures on the real claims (sandbox clone only)

Round 30 + a 10-row receipts file (2 claims × the 5 frozen controls, short ids for four and the full
string for `junk-row`) committed as `b7340220b7d4ecc85108cbe4f3f924517635d066` (ct 1792723575):

```
python3 -I -B axis-fit-gate.py --root clone --round 30 --rev b7340220b7d4ecc85108cbe4f3f924517635d066   # exit 0
{"axis_claims": [{"axis": "coverage", "claim": "R30-C1", "controls_present": {"all-false (committed refusal or null-metadata envelopes)": "head", "do-nothing": "exact", "junk-row (entry + PROVINCE/SKILL lines without envelopes)": "exact", "no-reader (envelopes fabricated from the oracle reading, never produced by REA)": "head", "shortcut keyed on ids/labels (another carrier's or mutant's envelope under the id; predictions copied as observations)": "head"}, "surface": "ok", "unmoved_command": "ok"}, {"axis": "depth", "claim": "R30-C2", … "surface": "ok", "unmoved_command": "ok"}], "claim": "R30-axis-fit-gate", "claims_file": ".ufo/waves/round-30/claims.json", "findings": [], "notes": ["no envelope path is committed yet: the ordering clause is vacuous"], "receipts": {"first_add": {"commit": "b7340220b7d4ecc85108cbe4f3f924517635d066", "committer_ct": 1792723575}, "first_envelope_add": null, "ordering": "no-envelopes", "path": ".ufo/waves/round-30/controls/receipts.tsv", "present": true, "rows": 10}, "required_controls": [ … 5 frozen names … ], "rev": "b7340220b7d4ecc85108cbe4f3f924517635d066", "round": 30, "verdict": "PASS"}
```

Round 29 + a receipts file committed *after* round-29's data commit (`4fcea978…`, which added
`corpus/evidence/round-29/c1/envelopes/n01..n16.json`) — sandbox commit
`84a2ec2ce1ae882031081e2a6ac2c07fd3e4b0cf` (ct 1792723579):

```
python3 -I -B axis-fit-gate.py --root clone --round 29 --rev HEAD   # exit 1
{"axis_claims": [ … R29-C1/R29-C2 surface "missing", unmoved_command "missing", "controls_present": {} … ], "claim": "R30-axis-fit-gate", "claims_file": ".ufo/waves/round-29/claims.json", "findings": [{"claim": "R29-C1", "finding": "SURFACE_MISSING"}, {"claim": "R29-C1", "finding": "UNMOVED_COMMAND_MISSING"}, {"claim": "R29-C2", "finding": "SURFACE_MISSING"}, {"claim": "R29-C2", "finding": "UNMOVED_COMMAND_MISSING"}, {"envelopes": {"commit": "4fcea97875a7fe1d816fb871cbc60a1c3632efa0", "committer_ct": 1792699749, "path": "corpus/evidence/round-29/c1/envelopes/n01.json"}, "finding": "RECEIPTS_NOT_BEFORE_ENVELOPES", "receipts": {"commit": "84a2ec2ce1ae882031081e2a6ac2c07fd3e4b0cf", "committer_ct": 1792723579}}], "notes": ["controls_required_before_data absent: no control is named"], "receipts": {"ancestor_of_first_envelope": false, "first_add": {"commit": "84a2ec2ce1ae882031081e2a6ac2c07fd3e4b0cf", "committer_ct": 1792723579}, "first_envelope_add": {"commit": "4fcea97875a7fe1d816fb871cbc60a1c3632efa0", "committer_ct": 1792699749, "path": "corpus/evidence/round-29/c1/envelopes/n01.json"}, "ordering": "not-earlier", "path": ".ufo/waves/round-29/controls/receipts.tsv", "present": true, "rows": 2}, "required_controls": [], "rev": "84a2ec2ce1ae882031081e2a6ac2c07fd3e4b0cf", "round": 29, "verdict": "FAIL"}
```

This exercises the ordering clause against real lane history: the detected first envelope commit is
round-29's data commit `4fcea97875a7fe1d816fb871cbc60a1c3632efa0` (ct 1792699749), and the receipts
commit is later, so the gate fails. These two sandbox commits exist only in the scratch clone
(`git -c user.name=ctl -c user.email=ctl@sandbox commit`); the lane was not touched and its index,
jj state and worktree are untouched.

## Scratch artifacts (sha256) — [observation]

| artifact | sha256 |
|---|---|
| `axis-fit-gate.py` (the tool) | `1390a007d7e06868e713e11ea991cd688f5ae104220e5ba80a45a918c37c6a63` |
| `selftest.out` | `4a23a799dc25228a6106a0bded6014485d9a49317d6b5b144760db07948b5e00` |
| `run-round29.txt` | `e00e9e08bd90d85a8ef55f6e4211e0646ef273125e9cdb2987152ac6016a8729` |
| `run-round29-freeze.txt` | `89fe0f2712927a11ff5d72b69ba8a0b5d5069da154d4a17136ff303570fcd41e` |
| `run-round30.txt` | `3436951ab5e996c88f2693e35847caef4906a4ce3cb48e4c887c139fbd51b4e6` |
| `run-round30-green.txt` | `ea6ad05c70c4088018b85de39213b05937e80b120a064190b49514a51c4ab5f6` |
| `run-round29-order.txt` | `515cb9836d5b2904d06d39e2c194ef4558793c9e1052a88531658f9d91dccf3c` |
| `clone/` | sandbox clone, `main` = `4ee65c67…` + 2 fixture commits `b7340220…`, `84a2ec2c…`; clean worktree |

All under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecAxisFitGate/`.

## Limits, risks, unknowns

- **Not run by this seat:** the gate never ran against the lane worktree itself (read-only bound); all
  runs used the scratch clone. The two sandbox fixture commits are *not* the wave's real receipts —
  the real `.ufo/waves/round-30/controls/receipts.tsv` is the wave's to produce, and until it is
  committed the round-30 run must exit 1 (as required now).
- **[Inference] Ordering is by committer timestamp** (strict `<`), with the ancestry relation reported
  as well; equal timestamps (same commit) fail, which is the intent for "before data". Commit
  timestamps are not authenticated (lane-wide limit); a receipts commit that is not an ancestor of the
  first envelope commit but has an earlier timestamp passes with a printed note.
- **[Inference] Scope rule chosen:** receipts are required only when the round has at least one
  coverage/depth claim; a round whose claims are all other-axis needs none (green-other-axis-only).
  `controls_required_before_data` absent/empty is a note, not a finding.
- **[Inference] The envelope pattern is exactly one directory segment** between `round-<N>/` and
  `envelopes/` (`corpus/evidence/round-30/c1/envelopes/…`); a deeper nesting would not be seen.
- **Not covered:** the gate checks the receipts' shape and the two clauses, not the truth of a control
  row (a fabricated `met_target=no` row passes); it does not read envelopes, counters, entries or
  PROVINCE/SKILL; it does not run any counter.
- **Unknown:** whether the L1 will write receipt `control` cells as short ids or full frozen strings —
  both are accepted for round-30's five names (heads are unique); if a future round has two frozen
  names sharing a head, only exact cells will satisfy them.

## Tooling, processes, labrat, axes

- No tool installed or updated; no package manager invoked. No process left running (every command
  under `timeout`; the only long-lived thing is the scratch clone on disk).
- No labrat probe was needed: the gate's falsifiability is carried by its own selftest and the two
  required real runs.
- No claim data touched: no REA run, no carrier or mutant executed or read, nothing written under
  `corpus/`, `tools/`, or `.ufo/waves/round-30/controls/`. The only lane write is this report.
- Axes: this is the M30-1 fix item (build + show able to fail); it asserts nothing about R30-C1/C2
  outcomes and adds no claim.
