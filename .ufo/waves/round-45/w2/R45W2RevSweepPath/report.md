# R45W2RevSweepPath — attack: "placement in the fleet sweep path is not a lane edit"

Seat: wave-2 adversarial falsification, round 45, lane `kaidoku`. Read-only on the lane tree and the
fleet repo; every mutation happened in a fixture under
`/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath` (removed after the receipts were copied here).

## 0. Verdicts

| # | attack | verdict |
|---|---|---|
| A1 | A lane-side hook (`.git/hooks/pre-commit`, `pre-push`) can gate the fleet's commit | **holds** — no hook channel exists on either commit path, and the claim is stronger than its own stated reason |
| A2 | The sweep passes `--no-verify`, so a hook *would* have been suppressed | **not run / void** — neither commit path invokes `git commit`; `--no-verify` appears nowhere in the fleet tree |
| A3 | "The fleet sweep path" is where the M45-1 defect would recur | **falsified** — the inline sweep commits one *fleet-repo* report path; the 432-path lane commit came from the lane helper, which has no frozen-path guard |
| A4 | No lane-side file or exit code can influence the sweep | **holds for the commit leg; one lane-side probe exists on the push leg** (`[ -d "$cwd/.jj" ]`, `inline.sh:168`) |
| A5 | The substitute — "every L1 commit is preceded by the gate on the round's own frozen paths" | **falsified** — 1 of 12 post-freeze commits is preceded by a real gate run at its parent (`r43b`) |
| A6 | "`--check-dirty` catches the precursor (eight dirty files)" | **holds only same-round / under the named pathspec**; a dirty path outside it reads `clean` exit 0 (`r28`) — which is the cross-round recurrence shape |
| A7 | "The fleet scripts are read-only for a lane" | **holds as contract, not as permission** (mode `-rwxr-xr-x`, owner = the lane's own user, `r44`) |
| A8 | Reproduce the exact command that produced `c86ea508` | **not run** — not recoverable; the stamp pair does not discriminate (see §7) |

**Bottom line for the L1:** the claim that the lane cannot make the fleet run the gate is *true and
under-argued*. The substitute it justifies is **insufficient as stated**: it is a discipline with a
1/12 receipt rate in the round that landed it, its "precursor" arm is blind to any freeze but the
current round's, and the placement target it hands the operator is the wrong code path. Three
one-line corrections in block 22 / lesson / LOG plus one operator-side request that names
`jj-lane.sh:700` instead of the inline sweep would make the record true.

## 1. The claim under attack, verbatim

Three copies of one sentence, all landed:

- `SKILL.md:605-607` (rule block 22, prose): "Placement inside the fleet's own sweep path is not
  a lane edit — the fleet scripts are read-only for a lane — so it stays an
  operator/integrator request and the report says so".
- `corpus/lessons/round-45.md:70-76` (R45-CL1): "… the fleet's `scripts/hyaku/` tree is read-only
  for this lane (prompt §3), so placement in the sweep/pre-push path is an operator/integrator
  request, not a lane landing. The lane can prove the arm works; it cannot make the sweep run it.
  The achievable substitute landed this round: every L1 commit is preceded by the gate on the
  round's own frozen paths, and the gate's `--check-dirty` arm catches the precursor (eight dirty
  files) before a sweep exists."
- `LOG.md:3262-3264`: "… placement in the fleet sweep path stays an operator/integrator request
  because fleet scripts are read-only for a lane".

Its ancestor is `corpus/lessons/round-44.md:63-69` (R44-CL1), whose clause (c) is
"placement in the fleet sweep/pre-push path as well as the lane's own commit sequence".

The claim carries **three separable assertions**, and they do not stand or fall together:

1. a lane cannot *gate* the fleet's commit through a lane-owned file (§3.1 — holds, stronger);
2. the placement that matters is *the fleet sweep path* (§3.2 — falsified: wrong path);
3. the substitute is the L1's own gate discipline, and it catches the precursor (§3.3, §3.4 —
   falsified for the universal, narrowed for the arm).

## 2. What the fleet actually does — the exact commit code

No code path commits a whole lane worktree by name. There are exactly two commit sites, both
pathspec-limited, both in `scripts/hyaku/`, both `jj` (not `git`):

| site | code | repo it commits | request width |
|---|---|---|---|
| fleet report "sweep" | `inline.sh:157-161` → `fleet-commit.sh:86` `jw commit -m "$msg" -- "${existing[@]}"` | the **fleet** repo (`FLEET=/home/vgpnk/Projects/shokunin`, `inline.sh:22`; `cd "$FLEET"` `fleet-commit.sh:54`) | **one** path: `.ufo/reports/round-$n/$lane.md` (`inline.sh:155,159`) |
| lane commit | `jj-lane.sh:700-703` `jj commit -m "$msg" -- "${fs_req[@]}"` | the **lane** repo | every file under each named path; a directory pathspec is recursive (`jj-lane.sh:633-634`) |

`fleet-commit.sh` builds its request from `argv` only (`:67-73`), rejects `.ufo/state/*` and
`..`/absolute paths (`:44-47`), imports first (`:65`), and commits with
`metaedit --update-author` + `jj commit` (`:84-89`); it pushes `main`/`master` forward-only
(`:93-119`). `inline.sh:11` documents the step as "landed? (report_of, committed — swept if not,
pushed)" and `:158-161` names its trigger — "report uncommitted at return (attribution defect)".
It is a *report* sweep, not a worktree sweep.

`jj-lane.sh cmd_commit` (`:598-727`) is the code that can commit a lane worktree with breadth:
`repo_path_allowed` (`:502-517`) refuses `.`, `..`, absolute paths, `.git/*` and `.jj/*`, and
`.ufo/state`/`.ufo/watchdog.log` — but it does **not** refuse a directory that happens to contain a
frozen path; `validate_change_scope` (`:522-572`) only checks that every changed path is under
**some** requested path (`:552-559`). So breadth is entirely caller-supplied, and a
frozen-path-aware check exists only in the preflight, which `jj-lane.sh` never calls
(`r36`: no lane tool wraps `jj-lane.sh commit`; `r37`: the only invoker of the preflight under
`tools/` is the instrument itself alongside `c1-counter.py` and the frozen scope file).

### The round-44 defect, re-derived

`c86ea508` is a **lane-repo** commit, 432 paths (`r38`), identity
`kaidoku-shokunin <kaidoku@shokunin.local>` (`r34` — the lane stamp produced by
`--as kaidoku` in either helper, `fleet-commit.sh:57-58` / `jj-lane.sh:696-702`). Its path set is
three top-level families (`r33`):

```
423 .ufo/waves         <- not frozen
  8 tools/round-44     <- the frozen 8 (tools/round-44/control-fixtures/**, r39)
  1 corpus/evidence
```

That is exactly the shape produced by **three directory pathspecs** on the lane helper. Measured
end-to-end with the current, unmodified tool (`r23`–`r26`): `jj-lane.sh commit <lane> --as fxlane -m …
-- .` is refused (`jj-lane: path escapes the lane root: .`, exit 1), while
`… -- .ufo/waves/round-44 tools/round-44` **lands** (exit 0, `landed 8de32b8…`) with a commit that
contains `tools/round-44/control-fixtures/touch.json` (`r25`). The M45-1 shape is reproducible today,
in one call, with the sanctioned tool.

The exact command that produced `c86ea508` is **not** recoverable (no shell history, no jj operation
record of argv), so "the fleet orchestrator's non-author lane sweep" (`LOG.md:3203`) remains an
*attribution* from timestamps, not a command line. What is measured: the capability (§2 above), the
path set, the identity, and the fact that the only fleet-side `verify` sweep cannot produce it.

## 3. Findings

### 3.1 A lane-side hook cannot gate the fleet's commit — holds, and the stated reason is the weaker half

The decisive mechanism: **the fleet never calls `git commit` or `git add`.** `r01` shows the only
occurrences of `git (commit|add)` in the fleet's runtime scripts are comments in `jj-lane.sh`
(`:4,:219,:391,:656,:680`); the sole executable uses are fixture setup inside
`jj-lane-selftest.sh:517,648-649`. `--no-verify` appears nowhere (`r02` = `NONE`), so A2 is void:
there is nothing to suppress.

Both helpers invoke `jj` — `fleet-commit.sh:57-58,65,76-79,84-86` and
`jj-lane.sh:658-703` — and jj 0.45.1 (`r05`) has no hook machinery at all (`r35`:
`help_hits=0 config_hits=0`). Measured, with a live control:

| fixture | hook | call | rc | hook ran |
|---|---|---|---|---|
| fx1 (`r07`–`r09`) | `.git/hooks/pre-commit` → `exit 1` | `git commit` | 1 | **yes** (`h1.log` = 1 line), 0 commits |
| fx2 (`r10`–`r12`) | same hook | the exact `fleet-commit.sh` jj sequence (`file track`, `commit -- root:"b.txt"`) | **0** | **no** (log absent) |
| fx2b (`r13`–`r15`) | same hook, still present | `jj commit -- root:"dir"` (2 nested files) | **0** | **no** |
| fx3 (`r16`–`r17`) | `.git/hooks/pre-push` → `exit 1` | `git push` | 1 | **yes** (1 line) |
| fx3 (`r18`–`r19`) | same hook | `jj git push --remote origin --bookmark master` | **0** | **no** |
| fx4 (`r20`–`r22`) | `.git/hooks/pre-commit` → `exit 1` | **the real `fleet-commit.sh`** on a fixture repo (`SHOKUNIN_ROOT` = fixture) | **0**, `committed 2b5c4ba…`, one path | **no** |
| fx5 (`r24`–`r26`) | same hook | **the real `jj-lane.sh commit`**, two directory pathspecs | **0**, `landed 8de32b8…` | **no** |

So a lane-side hook is not merely undeployed — it is *structurally incapable* of gating either
commit path on this host. The honest argument is that one, not "the fleet scripts are read-only for
a lane": the read-only rule is a *prompt* constraint (`prompt §3` in the lesson's own citation),
while the files are mode `-rwxr-xr-x` owned by `vgpnk`, the user the lane runs as (`r44`). Block 22's
parenthetical states a capability fact where the evidence supports only a contract fact.

**Verdict: holds.** Suggested replacement sentence: "Neither commit path executes a git hook
(`jj 0.45.1`; `fleet-commit.sh:86`, `jj-lane.sh:700-703`), and `--no-verify` is not used because
`git commit` is not used; a lane therefore has no in-band channel to gate the sweep, and the
placement is an operator/integrator request."

### 3.2 The named placement is the wrong path — falsified

The remedy names "the fleet sweep/pre-push path". Measured:

- the only sweep (`inline.sh:157-161`) commits **one fleet-repo path**
  (`.ufo/reports/round-$n/$lane.md`); `fleet-commit.sh:69` builds `existing` from that single
  argument; `jj commit -- root:"…"` commits only named pathspecs. It cannot produce 432 lane-repo
  paths, and it cannot touch a lane frozen path at all.
- the path that *can* is `jj-lane.sh:700-703`, demonstrated live (`r24`/`r25`), with
  `validate_change_scope` permitting anything under a named directory (`:552-559`).

Consequence: a gate placed in the inline sweep would observe the **fleet** repo's frozen paths (it
has none of this lane's) and would be blind to the exact defect it was requested for. The request
must name `jj-lane.sh cmd_commit` (one call before `:700`, over the lane's freeze declaration) plus,
secondarily, `inline.sh:157-161` if the fleet ever sweeps a lane tree.

**Verdict: falsified.** Fix: replace "the fleet sweep/pre-push path" with "the lane commit helper
(`jj-lane.sh:700`) and, secondarily, the fleet report sweep (`inline.sh:157-161`)". Note that the
`pre-push` half is also misaddressed for *this* lane: the durability push goes through `jjl push`
because `$cwd/.jj` exists (`inline.sh:168`), so no `pre-push` hook runs there either (`r18`).

### 3.3 "Every L1 commit is preceded by the gate" — falsified, 1/12

`corpus/lessons/round-45.md:74` is a universal. The round's own receipts refute it. The census
(`r43b`) intersects (a) the 12 lane commits in `FREEZE..HEAD` with (b) every
`.ufo/waves/round-45/**/preflight*.json` whose `rev` equals that commit's **parent** and whose mtime
is **earlier** than the commit:

```
9ff920cd 12:30:41  parent=f762b727  gate_before=['preflight-at-freeze.json(vacuous)']
e715263c 12:33:03  parent=9ff920cd  gate_before=NONE      <- the landing commit itself
1f4b27f8 12:34:20  parent=e715263c  gate_before=NONE      <- amendment A1, the measured revision
abfeda50 12:35:26  parent=1f4b27f8  gate_before=NONE
faa875bc 12:37:11  parent=abfeda50  gate_before=NONE
fedd11bf 12:49:17  parent=faa875bc  gate_before=['preflight-round45-frozen-both.json']
14340d41 12:49:36  parent=fedd11bf  gate_before=NONE
92b4970c 12:52:06  parent=14340d41  gate_before=NONE
f59565b7 12:56:04  parent=92b4970c  gate_before=NONE
1d04c6af 12:56:22  parent=f59565b7  gate_before=NONE
a63d109f 12:58:04  parent=1d04c6af  gate_before=NONE
0ee50aaf 12:59:26  parent=a63d109f  gate_before=NONE
preceded_by_a_real_gate_run = 1/12
```

Two details make it worse than a bookkeeping gap:

- the one pre-landing receipt (`controls/preflight-at-freeze.json`, 15:27:32Z = 12:27:32-03) is
  **vacuous**: `rev` = `freeze`, i.e. an empty range, and it was produced by the *base* script, which
  has no `--check-dirty` at all (base `149133d4` arguments: `--root --freeze --rev --pathspec
  --json-out`, no dirty arm). The dirty arm first exists in `e715263c`, the very commit it cannot
  precede.
- the three non-vacuous L1 receipts are **post-hoc**: `preflight-round45-frozen.json` (15:39:03Z)
  scores `abfeda50`, which had already landed at 15:35:26Z and was followed by `faa875bc` at
  15:37:11Z; `preflight-at-A2-both.json` (15:54:10Z) scores `fedd11bf`, written after `92b4970c`
  (15:52:06Z).

The census includes wave-1/wave-2 seat fixture receipts; none of them names a post-freeze parent, so
they cannot inflate the 1/12. An unrecorded gate run cannot be excluded — but this round's own
standard is that an unreceipted run is not evidence, and the universal is written as fact.

**Verdict: falsified.** Fix: state the receipted fact ("the gate was run four times on the
round-45 freeze: once before `fedd11bf`, twice after the fact, and once vacuously at the freeze") —
or make it true from now on by writing a receipt per commit, which is one command and the only
honest way to keep the universal.

### 3.4 "`--check-dirty` catches the precursor" — holds only for the current round's pathspec

Block 22 row 4 scopes the arm correctly ("the worktree is dirty under the frozen pathspec",
`SKILL.md:589`), but the prose at `:597-599` and lesson `:75-76` generalise it to "the precursor
(eight dirty files)". Measured against a fixture whose freeze is `tools/round-45` (`r27`-`r30`):

| fixture state | invocation | verdict |
|---|---|---|
| ` M tools/round-45/frozen.txt` | `--pathspec tools/round-45/ --check-dirty` | exit 1, `dirty[0]` (`r27`) |
| `?? other/uncommitted.txt` only | same | **exit 0, `"verdict": "clean"`, `dirty: []`** (`r28`) |
| same tree | `--dirty-pathspec other/` | exit 1 (`r29`) |
| same tree | no `--check-dirty` | exit 0 (`r30`) |

`scope_paths = dirty_pathspecs or pathspecs` makes the arm exactly as wide as the caller says. The
already-routed R45-CL15 / `SKILL.md:574-577` disclosure covers the *flag* (a caller who passes
`--dirty-pathspec` loses the frozen scope). The finding here is the **default** form: with the
round's own `--pathspec`, a dirty file belonging to *another* round's freeze is invisible — and that
is the recurrence shape this lane already lives with: R45-CL5 (`corpus/lessons/round-45.md:87-89`)
records that the round-44 counters still exit 2 for the eight sweep-committed paths. The substitute
is therefore a same-round, same-pathspec net.

**Verdict: holds narrowly, falsified as the general "precursor" claim.** Fix: (a) union instead of
replace in the dirty arm (already R45-CL15), and (b) let the invocation carry **all** prior freezes,
not just this round's — which needs the freeze declaration described in §5.

### 3.5 Lane-side inputs the fleet *does* consult — one, and only on the push leg

`inline.sh verify` is the only fleet code that looks at the lane (`r06`):

- `:165` `jjl state "$cwd"` — lane refs (`ahead`), and `:167-170` gates the durability push on it.
- `:168` `[ -d "$cwd/.jj" ]` — **the one lane-side filesystem probe that changes behaviour**: with
  `.jj` present it runs `jjl push --no-rebase` (no hooks, `r18`); without it, `git -C "$cwd" push -q`,
  which **does** run a lane-side `pre-push` hook (`r16`/`r17`). A lane that removes `.jj` from disk
  (a lane-side, uncommittable directory) can therefore route the fleet's push through a hook it
  controls. It cannot gate the commit, and for a colocated lane it is inert — but "no lane-side file
  can influence it" is false as written.
- `:172` `git -C "$cwd" status --porcelain` — warning only.
- The commit leg (`:157-161` → `fleet-commit.sh`) consults **no** lane path: `$rep` is a fleet-repo
  path, `report_of` (`shokunin-watchdog.sh:187-207`) reads `$UFO/reports/…` with
  `UFO=$SHOKUNIN_ROOT/.ufo` (`:47`), i.e. the fleet copy.

Precedent that the fleet already reads lane-owned control files: `.ufo/waves/round-N/<wave>.ready`
is written by the lane and polled by `ready-watch.sh:26` and `inline-dispatcher.py:310,362,372`.
That is the spawn path, not the commit path — but it is the existing pattern a lane-side freeze
declaration would follow.

**Verdict: holds for the commit leg; falsified for "no lane-side probe at all".**

### 3.6 "Read-only for a lane" is a contract fact, not a permission fact

`stat` (`r44`): both scripts are `-rwxr-xr-x vgpnk:vgpnk`, and the lane's process runs as `vgpnk`.
The read-only property comes from the round prompt (`prompt §3`), which the lesson itself cites.
Block 22's parenthetical reads as a property of the world; a future round whose prompt omits §3
silently falsifies it. **Verdict: holds this round; calibration defect in the phrasing.**

### 3.7 Outside the claim's blast radius, checked and clean

The gate itself at the measured revision and at the tip (`r31`, `r32`) returns
`{"touched": [], "dirty": [], "verdict": "clean"}`, exit 0 with the round's full two-pathspec
invocation — the landing is clean under its own freeze, so nothing here contradicts the score. The
frozen `tools/round-45/` and `plans/round-45-claims.md` were not modified by this seat (all work in
scratch; the harness only read the lane).

## 4. Channel matrix — can a lane influence the fleet's commit without editing fleet scripts?

| channel | reaches the commit leg? | reaches the push leg? | measured |
|---|---|---|---|
| `.git/hooks/pre-commit` | **no** — no `git commit`; `jj commit` runs no hooks | n/a | `r01`,`r11`,`r12`,`r20`,`r21`,`r24` |
| `.git/hooks/pre-push` | n/a | **only** when `.jj` is absent (`inline.sh:168`) | `r16` (git: runs), `r18` (jj: not) |
| `--no-verify` | never passed | never passed | `r02` |
| lane `.ready` / any other lane file | **no** | no | `r06`, `r03` |
| lane refs (`jj-lane.sh state`) | no | yes, gates the push on `ahead` | `inline.sh:165-170` |
| exit codes of lane tools | no | yes (`jjl push` failure ⇒ `FAIL … not landed`) | `inline.sh:168-170` |
| jj repo/user config | only `$JJ_BIN`, `SHOKUNIN_ROOT`, `HYAKU_STATE`, `FLEET_*` env, all set by the caller | same | `fleet-commit.sh:26-31` |
| editing `scripts/hyaku/*` | yes, by construction | yes | out of bounds for a lane (`prompt §3`), and writable on disk (`r44`) |

## 5. Verdict on the substitute, and the exact fix

**Verdict on "the substitute landed this round is sufficient": insufficient as stated**, for three
independent reasons, each with a measured receipt:

1. the universal it rests on is false at 1/12 in its own round (§3.3, `r43b`);
2. the precursor arm cannot see a foreign freeze by default (§3.4, `r28`) — the recurrence shape;
3. the placement it hands the operator is the wrong code path (§3.2, `r33`/`r24`).

It is sufficient in one respect worth crediting: as a *report* it correctly refuses to claim the lane
can gate the fleet, and that refusal is stronger than the reason given (§3.1).

Minimal fix set, in order of cost:

1. **Wording (lane, this round or next).** Block 22 `:605-607`, lesson `:70-76`, LOG `:3262-3264`:
   name the two commit sites (`jj-lane.sh:700-703`; `inline.sh:157-161` → `fleet-commit.sh:86`),
   replace "read-only for a lane" with the mechanism (no git commit, no hooks in `jj 0.45.1`), and
   restate the universal as the receipted 4-run/1-preceding fact.
2. **Receipt discipline (lane).** One preflight receipt per commit, named
   `preflight-<parent>.json`, written before `jj-lane.sh commit`; then the universal becomes true and
   checkable by the census in `receipts/census.py`.
3. **Machine-readable freeze declaration (lane, and the missing half of the operator request).**
   A fleet-side gate cannot know a lane's freeze rev or frozen paths: nothing under `scripts/` reads
   `plans/*-claims.md` (`r03`-adjacent grep: `NONE`), and the frozen paths live only in prose
   (`plans/round-45-claims.md:132-137`). Land `.ufo/freeze.json`
   `{"freeze":"<40-hex>","paths":["tools/round-45/","plans/round-45-claims.md"],"prior":[{…round-44…}]}`
   so that (a) the request has data and (b) the dirty arm can be widened to every prior freeze,
   closing §3.4's blind spot without a fleet edit.
4. **Operator/integrator request (fleet).** In `jj-lane.sh cmd_commit`, after `req`/`fs_req` are built
   (`:628-648`) and before `jj commit` (`:700`), run
   `frozen-path-preflight.py --root "$phys" --freeze … --rev @- --pathspec … --check-dirty` from the
   lane's declaration and abort on exit ≠ 0; secondarily the same call in `fleet-commit.sh` after
   `:79` when the target repo is a lane. Both are one call each; the lane cannot land them (§3.1,
   §3.6) but it can now hand over the data they need (item 3).

## 6. Receipts

Raw stdout per label: `receipts/out/<label>.out`. Full 64-hex sha256 and exact argv:
`receipts/receipts.tsv` (columns: label, UTC, exit, sha256, command). Harness:
`receipts/harness.sh`, `receipts/harness2.sh`; census: `receipts/census.py`.

| label | UTC | rc | stdout sha256 (16) |
|---|---|---|---|
| `r01-no-git-commit-in-fleet` | 2026-10-28T16:04:14Z | 0 | `b3727680b320867e` |
| `r02-no-no-verify` | 2026-10-28T16:04:14Z | 0 | `c627c09c14e58e44` |
| `r03-no-gate-wiring` | 2026-10-28T16:04:14Z | 0 | `c627c09c14e58e44` |
| `r04-commit-callers` | 2026-10-28T16:04:14Z | 0 | `1726ff592076d465` |
| `r05-jj-version` | 2026-10-28T16:04:14Z | 0 | `1ee57f250e06e3ec` |
| `r06-lane-side-probes` | 2026-10-28T16:04:14Z | 0 | `d0d6b3d16e5268a5` |
| `r07-fx1-git-pre-commit-blocks` | 2026-10-28T16:04:14Z | 1 | `e3b0c44298fc1c14` |
| `r08-fx1-hook-log` | 2026-10-28T16:04:14Z | 0 | `6b86b273ff34fce1` |
| `r09-fx1-commit-count` | 2026-10-28T16:04:14Z | 0 | `5feceb66ffc86f38` |
| `r10-fx2-jj-track` | 2026-10-28T16:04:14Z | 0 | `e3b0c44298fc1c14` |
| `r11-fx2-jj-commit` | 2026-10-28T16:04:14Z | 0 | `c79f5759ebc977cb` |
| `r12-fx2-hook-log` | 2026-10-28T16:04:14Z | 0 | `97d5faf3ecf3107f` |
| `r13-fx2b-dirpathspec-commit` | 2026-10-28T16:04:15Z | 0 | `d2f71f8acedc4a28` |
| `r14-fx2b-committed-paths` | 2026-10-28T16:04:15Z | 0 | `ee7028ce85f3fffc` |
| `r15-fx2b-hook-still-silent` | 2026-10-28T16:04:15Z | 0 | `97d5faf3ecf3107f` |
| `r16-fx3-git-push-blocked` | 2026-10-28T16:04:15Z | 1 | `4a3477f10b62717a` |
| `r17-fx3-hook-log` | 2026-10-28T16:04:15Z | 0 | `6b86b273ff34fce1` |
| `r18-fx3-jj-push-unblocked` | 2026-10-28T16:04:15Z | 0 | `92c75a8cd4629391` |
| `r19-fx3-jj-push-hook-log` | 2026-10-28T16:04:15Z | 0 | `256c9980584c1097` |
| `r20-fx4-real-fleet-commit` | 2026-10-28T16:04:15Z | 0 | `77e30cd84f61506d` |
| `r21-fx4-hook-log` | 2026-10-28T16:04:15Z | 0 | `6382f621b1a13c02` |
| `r22-fx4-committed-paths` | 2026-10-28T16:04:15Z | 0 | `ff8d93a35f03e0b2` |
| `r23-fx5-dot-pathspec-refused` | 2026-10-28T16:04:15Z | 1 | `7b93415a997dd9a6` |
| `r24-fx5-dirpathspecs-landed` | 2026-10-28T16:04:15Z | 0 | `05a664af92009fb2` |
| `r25-fx5-lane-tip-paths` | 2026-10-28T16:04:15Z | 0 | `e8f48734ddb9396b` |
| `r26-fx5-hook-log` | 2026-10-28T16:04:15Z | 0 | `c2c2340b1ac2359d` |
| `r27-fx6a-dirty-in-scope` | 2026-10-28T16:04:15Z | 1 | `c5f2fb4c5a4093a9` |
| `r28-fx6b-dirty-outside-scope` | 2026-10-28T16:04:15Z | 0 | `d8d6ea3a2cb62c38` |
| `r29-fx6b-other-dirtypathspec` | 2026-10-28T16:04:15Z | 1 | `9447c64ab9b81d86` |
| `r30-fx6c-no-dirty-arm` | 2026-10-28T16:04:15Z | 0 | `d8d6ea3a2cb62c38` |
| `r31-real-gate-measured` | 2026-10-28T16:04:15Z | 0 | `d8f872e21efcf8d1` |
| `r32-real-gate-tip` | 2026-10-28T16:04:16Z | 0 | `3e0c938a4dde4901` |
| `r33-c86-paths` | 2026-10-28T16:04:16Z | 0 | `5f3b24021b9c18de` |
| `r34-c86-identity` | 2026-10-28T16:04:16Z | 0 | `ec752ed1fa0d3217` |
| `r35-jj-has-no-hooks` | 2026-10-28T16:05:38Z | 0 | `682550e925e828f1` |
| `r36-no-lane-commit-wrapper` | 2026-10-28T16:05:38Z | 0 | `c627c09c14e58e44` |
| `r37-preflight-invokers` | 2026-10-28T16:05:38Z | 0 | `56b9ff3fe4fdfde3` |
| `r38-c86-path-count` | 2026-10-28T16:05:38Z | 0 | `98f1f17f9a73ccfe` |
| `r39-c86-frozen-subset` | 2026-10-28T16:05:38Z | 0 | `594e23275115a16d` |
| `r40-inline-sweep-pathspec` | 2026-10-28T16:05:38Z | 0 | `33424d1770a45e17` |
| `r41-fleet-commit-commitcode` | 2026-10-28T16:05:38Z | 0 | `83202a00a85485d0` |
| `r42-jjlane-commitscope` | 2026-10-28T16:05:38Z | 0 | `98dcfe831911b743` |
| `r43b-census` | 2026-10-28T16:05:45Z | 0 | `87ecdf0500da7b13` |
| `r44-script-perms` | 2026-10-28T16:05:38Z | 0 | `1345eaeef7af949c` |

`r43` (the first census attempt) is kept in the tsv with exit 1 — a strict-JSON parse failure in my
own probe, replaced by `r43b`; it is a seat-side bug, not a finding.

Reproduction: the three scripts are kept **byte-identical to what ran** (so the receipts stay
verifiable), which means each hardcodes one line `S=/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath`.
Repoint that line at a fresh directory, then:

```sh
S=$(mktemp -d -p /fast/scratch/hyaku/kaidoku-r45) ; export TMPDIR="$S" ; cd "$S"
sed -i "s#^S=.*#S=$S#" harness.sh harness2.sh census.py
bash harness.sh && bash harness2.sh && python3 census.py   # regenerates every row above
```

`harness2.sh` appends to `$S/receipts.tsv`, so it must run after `harness.sh`; `r43` is the seat's
own first census attempt (exit 1, strict-JSON parse) and `r43b` supersedes it.

Fixture discipline used: `git init -q "$D"` then `[ "$(git rev-parse --show-toplevel)" = "$D" ]`
before the first commit in every repo, every later call named `-C "$D"`, all under `$S`, `$S` removed
after the receipts were copied here.

## 7. What I withdrew, and what is not run

- **Withdrawn: the stamp-pair provenance inference.** I first read `c86ea508` (author 09:57:16,
  committer 10:43:43) as proof the helpers were bypassed, on the theory that
  `metaedit --update-author` resets the author timestamp. That is false: the lane's own helper commits
  show the same split (`55bcce69` author 09:50:44 / committer 09:57:16; `e9e3abd1` author 09:49:16 /
  committer 09:50:44), and the `JJ_TIMESTAMP` probe (`fx8-stamp`) showed `--update-author` moving the
  author stamp to the *current* timestamp rather than the commit's. The stamp pair therefore **does
  not discriminate** helper from raw `jj commit`; §2's claim rests on the path set and the measured
  capability, not on stamps.
- **Not run: the exact argv of `c86ea508`.** No shell history and no jj operation record of command
  arguments; the commit is a fact, its command line is not recoverable from this tree. The seat
  reports the capability (`r24`), the path census (`r33`, `r38`) and the attribution as the record
  already states it (`LOG.md:3203`), and nothing stronger.
- **Not run: an end-to-end live sweep of this lane.** `inline.sh verify` would commit into the fleet
  repo (out of bounds) and would also mutate `~/.local/state/shokunin-hyaku`; the run was replaced by
  fx4, which executes the real `fleet-commit.sh` against a fixture root. The only unexercised leg is
  the `master@origin` push accounting (`fleet-commit.sh:105-119`), which never fired in the fixture
  because `master@origin` did not exist; the push behaviour of the commit leg was exercised
  separately (`r18`, `jj git push`).
