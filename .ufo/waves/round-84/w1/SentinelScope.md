# SentinelScope — round-84 security and scope review

Seat: SentinelScope (leaf, L1 KaidokuR84). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Audited lane HEAD `fa92d34aec31ae59cb19a8a6ea9e6c0ac7a2392f`; declaration
`e0de2088a7bddc16305357f90ac7e889fa0a0d11`; first container
`a5663ddedd157bb9113928f5fe80509d6f3fc7a1`.

Method: read-only git (`show`, `diff`, `status`, `cat-file`, `rev-parse`); the three
`tools/round-84/*.py` were read at their **pinned** bytes (digests verified against
`.ufo/waves/round-84/claims.json` at audit start); `tools/round-82/*.py`, `tools/round-83/source-bind.py`,
`mutants.json`, `claims.json`, `plans/round-84-claims.md`, and every wave seat artifact present at
review time. Probes ran only in `/fast/scratch/hyaku/kaidoku-r84/SentinelScope/` (fixture git repos,
a hostile mutant table, a victim directory, a broken `PATH`); receipts were copied here and the
scratch directory was removed. No lane write, no production edit, no fleet or sibling-lane write, no
git/jj mutation, no `task` spawn, no `agent://all`. No tool was installed or upgraded (Python 3.14.8,
git, mksquashfs/unsquashfs 4.7.5, npx 11.19.0 preexisted).

## Audited digests (pinned vs observed)

| object | pinned in claims.json | at audit start (16:41) | at report time (16:49) |
|---|---|---|---|
| `tools/round-84/freeze-precheck.py` | `602239f5f52009f2…` | `602239f5…` = pin | `4aae3f26d2c8f5db…` **drift** |
| `tools/round-84/mutation-closure.py` | `fd8aee39bdfaa1aa…` | `fd8aee39…` = pin | `fd8aee39…` = pin |
| `tools/round-84/nested-sqfs.py` | `08353f361ebc687a…` | `08353f36…` = pin | `e0364dde5a0bf3a0…` **drift** |
| `.ufo/waves/round-84/mutants.json` | `dbb6d4c93df656d4…` (`fixtures.sha256`) | matches | matches, and matches at `e0de2088`, `a5663dde`, `fa92d34a` |
| `.ufo/waves/round-84/claims.json` | — | `3e3f75ce…` (= `a5663dde` and `fa92d34a`) | unchanged |

All three pins also equal the committed blobs at `e0de2088`, `a5663dde`, `fa92d34a`, so the pin
checks reported below are meaningful for the declared revisions.

---

## F1 — HIGH — a frozen instrument was modified in the lane working tree mid-wave; the C1 after-receipt was produced by the unpinned bytes

**Failure path.** The C1 counting command executes the lane *path*
`python3 -I -B tools/round-84/freeze-precheck.py`, while `check_container` verifies digests with
`git show <rev>:<path>`. Those are two different byte sources. At 16:46:03 the working-tree file was
replaced in place (12,224 bytes, `4aae3f26…`) with a version that adds per-container `controls[]`,
`control_fired`, and a stricter `met` (requires `control_fired is True`); at 16:46:07 the L1 receipt
`.ufo/waves/round-84/l1/scores/c1-at-container.json` was rewritten and now carries those fields
(`controls` has one entry per container, `control_fired true`). The pinned bytes cannot emit them:
my pinned-era run `SentinelScope/fp-receipt.json` (16:44) has only the single `control` key and no
`controls`/`control_fired`. `tools/round-84/nested-sqfs.py` was likewise replaced at 16:48:09
(`e0364dde…`, diff is only the removal of the unused `import tempfile` — byte drift, no semantic drift).

**Evidence.**
- `git status --porcelain -- tools` → ` M tools/round-84/freeze-precheck.py`,
  ` M tools/round-84/nested-sqfs.py`; no other tracked frozen file is dirty.
- Full diffs saved as `SentinelScope/drift-freeze-precheck.diff` and
  `SentinelScope/drift-nested-sqfs.diff`. The `freeze-precheck` hunk changes
  `receipt["control"] = cheap_rule(text)` (pinned line 241) into an append-only `controls` list plus
  `control_fired`, and changes `met` (pinned line 248).
- The header comments in the hunk explicitly describe the change ("the control is scored on every
  container; the claim's control is the defective container's own acceptance"), i.e. it fixes the
  last-container-wins witness defect noted in F8.
- No seat artifact accounts for the edit. `grep -rln control_fired` over `.ufo/waves/round-84` and
  the live scratch tree hits only the L1 receipt and `ReviewerC1/precheck-control-lastwins.json`
  (reviewer probe JSONs, not tool bytes). ReviewerC1 additionally kept a pinned copy
  (`/fast/scratch/hyaku/kaidoku-r84/ReviewerC1/freeze-precheck-frozen.py`, digest `602239f5…`) and
  produced `precheck-exact-frozen.json` (pinned shape) vs `precheck-exact-worktree.json`
  (`controls`/`control_fired` shape) at 16:47 — direct corroboration of the split.

**Impact.** C1's "after" receipt is not produced by the instrument the container pins. Because
`freeze-precheck` records no self-hash in its receipt (pinned receipt literal at lines 218–219; the
only `instrument` occurrences are `PIN_KEYS` and prose), the receipt cannot disclose which bytes ran.
Every later run from the lane path is unpinned, and a commit would silently change the declared
instrument unless a supersession is declared. Mitigating detail: the drifted semantics are *stricter*
and the three claimed facts still hold (round-83 FLAGGED with the exact finding, round-84 CLEAN,
control fires for the flagged container), so this is a provenance/authority defect, not a false pass.

**Smallest remediation (owner action; I applied no fix).** Either restore the path from the pinned
blob (`git cat-file blob 223c7bb4` at HEAD) and re-run C1 from those bytes, or declare an instrument
supersession — new digest pinned in a new container, receipt regenerated, disclosed — and add
`instrument.sha256` (self-hash) to the `freeze-precheck` receipt so execute-vs-verify is visible.
`nested-sqfs` restoration is cosmetic but still required by the freeze rule.

## F2 — HIGH — `nested-sqfs.py --work` is an unguarded recursive delete

Pinned lines 330–334 and 379:

```python
330    if not args.work:
331        ap.error("--work is required")
333    work = os.path.abspath(args.work)
334    os.makedirs(work, exist_ok=True)
...
379            shutil.rmtree(work, ignore_errors=True)
```

`--work` is only truthiness-checked. Any existing directory is accepted, populated, and then
recursively deleted in `finally` unless `--artifact-work` is passed; `ignore_errors=True` hides
partial deletions. There is no marker file proving the directory is tool-owned, no `commonpath`
check, and no refusal of `/`, `.`, `$HOME`, or the lane/fleet root. The host guard states the
process cwd is the **fleet root**, so the plausible typo `--work .` (or any relative path resolved
there) deletes the fleet checkout at the end of a run — including after a failure.

Observed (no network, no REA): a pre-existing `victim/` containing `keep.txt` was passed as
`--work`; with `PATH=/nonexistent` the run failed at `mksquashfs` (`unevaluable: RuntimeError:
mksquashfs failed: [Errno 2]`), and the whole `victim/` tree was gone afterwards (`ls: cannot access
'victim'`). Receipt: `SentinelScope/nested-receipt.json`. The deletion is unconditional on outcome,
so an "unevaluable" run still destroys evidence.

Smallest remediation: create `--work` only when absent and refuse an existing non-empty directory
(or require a marker file and `rmtree` only on marker match), reject `.`/`/`/`$HOME` and paths
outside a declared scratch root via `commonpath`, and drop `ignore_errors`.

## F3 — MEDIUM-HIGH — a mutant row's `id` escapes `--work`; the table is execution authority and is not digest-bound at runtime

Pinned `mutation-closure.py` lines 151–154 and 176:

```python
151        mutant_dir = os.path.join(work, "mutants", mutant["id"])
152        os.makedirs(mutant_dir, exist_ok=True)
153        script = os.path.join(mutant_dir, os.path.basename(path))
154        Path(script).write_text(mutated)
...
176        Path(script).write_bytes(body)
```

`mutant["id"]` is a table-supplied path component joined with no `realpath`/`commonpath` check. An
`id` of `../../x` leaves `work/mutants/`, and an absolute `id` discards `work` entirely
(`os.path.join` semantics); line 154 writes the mutated target there and line 176 writes the pristine
target back. The run then reports normally — the escape is not a defect in the verdict.

Observed with a fixture repo and two hostile rows (`SentinelScope/esc-receipt-abs.json`):
`id: "../../escaped-dotdot"` and `id: "/fast/scratch/.../escaped-absolute"` each created
`<scratch>/escaped-*/fixture.py` outside `--work`, and the counter returned `{"killed": 2, "ok":
true}`. With a relative `--work` the same rows also escaped (`esc-receipt.json`). The same primitive
with a relative `id` also works (`work/mutants/../…`).

Additionally the table is *code authority*: `edits[].replace` text is written into a copy of a
committed tool and that copy is executed (`run_selftest`, lines 91–94, `python -I -B`), so an edited
or substituted table is arbitrary Python execution as the lane user (full env, see F4), plus the
path escape above. Nothing binds the table to the freeze at runtime: `mutation-closure.py` never
reads `claims.json` (`grep -c claims.json` = 0 for all three instruments), `PIN_KEYS` excludes
`fixtures` (`freeze-precheck` line 41), and `--mutants` is any path (line 293). The container's
`fixtures.sha256` (`claims.json` lines 31–34, `dbb6d4c9…`) is therefore an unenforced declaration;
C2's kill rule "a table edited after the freeze" has no mechanical detector in the wave.

Smallest remediation: reject `id` values not matching `^[A-Za-z0-9._-]+$` and assert
`os.path.commonpath([os.path.realpath(mutant_dir), os.path.realpath(work)]) == os.path.realpath(work)`
(reuse the lane's own `containment()` pattern, `printed-command.py` lines 156–161); verify the table
sha256 against `claims.json` before scoring; refuse absolute `--mutants`/`--work` outside the wave
root.

## F4 — MEDIUM — executed children inherit the full environment, including a credential-bearing variable; output-derived receipt fields can capture it

- `mutation-closure.py` lines 104–106: `env = dict(os.environ)` plus `TMPDIR` and
  `PYTHONDONTWRITEBYTECODE`, passed to every copied-tool selftest (`run_selftest`, 91–94).
- `nested-sqfs.py` lines 335–337: same, passed to `npx`; `run()` defaults to `env=None` (line 53)
  so `mksquashfs`, `unsquashfs`, and the version probes (lines 64, 72, 341–345) inherit the parent
  environment as well.
- The lane's own precedent is a four-key child environment: `printed-command.py` line 40
  `ENV_KEYS = ("PATH", "HOME", "TMPDIR", "LANG")` and lines 163–169 `child_env()` with `HOME`/`TMPDIR`
  under `--work`. The round-84 counters do not use it.

Host fact (presence checked by name only; no value read): `SSH_AUTH_SOCK` is **set** in the ambient
environment, so `npx -y rea-agents@6.5.0` (which runs registry code, see F5) and the copied tools
receive a live SSH-agent socket. `NPM_TOKEN`, `NODE_AUTH_TOKEN`, `GITHUB_TOKEN`, `AWS_SECRET_ACCESS_KEY`
are unset and `~/.npmrc` is absent on this host, which lowers the npm-credential case but not the
socket case.

Credential **capture** into receipts: the counters do not record their own env. The channel is
output-derived: a probe with `SCOPE_CANARY=canary-value` showed the child inherits it and the value
lands in the receipt's `targets.*.pristine.case_names` (line 51 of `SentinelScope/esc-receipt-abs.json`).
`nested-sqfs.py` line 370 records the last 2,000 characters of REA/npm `stderr` in the receipt, and
npm can echo registry URLs/errors there. So any executed child that prints an inherited secret is
captured into a file that is copied into the wave dir.

Smallest remediation: reuse `child_env()` (`PATH`, `HOME`, `TMPDIR`, `LANG`, with `HOME`/`TMPDIR`
under `--work`), pass it explicitly to every child including version probes, and truncate/strip
child stderr before it reaches a receipt.

## F5 — MEDIUM — C3's byte and engine arms are provider self-reports; nothing rehashes published files, the engine, or the fixture pins

Pinned `nested-sqfs.py`:

- Lines 179–186: `arms["bytes-equal"]` compares `by_path[p].get("sha256")` — a value read from the
  REA envelope — against the `unsquashfs` oracle. The published files under `work/out-depth{3,4}/…`
  are never re-hashed, so a lying or buggy provider satisfies A2/A6 without the bytes existing.
- Lines 224–233: A9 compares `engine` fields supplied by the same envelope (`name`, `version`,
  `executable_sha256`) plus `npx --version` stdout. Two self-reports from the same executable are a
  consistency check, not authenticity; a rewritten package reports its own version/hash identically.
- Line 126–127: `npx -y rea-agents@6.5.0 …` executes registry code with the full env **before** any
  identity check (A9 runs after both extractions). `-y` auto-installs; no lockfile/integrity pin and
  no `--ignore-scripts`; the package is resolved through `PATH` (here an fnm shim under
  `/run/user/1000/...`). Registry on this host is the public `https://registry.npmjs.org/`.
- Lines 109 and 366–372: fixture pins are computed once before both runs and never re-hashed, so the
  kill rule "fixture digests changing between the two depth runs" is not actually measured. (The
  receipt's `fixture_pins` are therefore a snapshot, not a between-run invariant.)

Smallest remediation: hash the published files on disk under the run's output root and compare to the
oracle; resolve and hash the unblob executable before the first run (or record it and re-verify after);
rehash `a/b/c` after each depth run. If provider-attested values are acceptable, the claim wording must
stop saying "matching bytes" and say "provider-reported digests"; the current predicate overstates what
is observed.

## F6 — LOW — a relative `--work` silently mislocates the selftest copy (fail-closed)

`mutation-closure.py` joins the pristine/mutant script relative to `work` (lines 116–119) and runs it
with `cwd=work` (line 93). With `--work mut-work`, the child opens `mut-work/pristine/mut-work/pristine/fixture.py`,
exits 2, `case_names` is empty, and every row becomes `inconclusive: pristine-not-green`
(`SentinelScope/esc-receipt.json`; `green false`, `exit 2`). It fails closed (no false pass), but the
receipt blames the pristine tool rather than the path. Remediation: `os.path.abspath` `--work` and the
script at entry, and assert the copy exists.

## F7 — LOW — `--json-out` is an unconstrained write with parent creation

`freeze-precheck.py` 255–256, `mutation-closure.py` 297–298 (and 273–274 in selftest),
`nested-sqfs.py` 382–383: `Path(json_out).parent.mkdir(parents=True, exist_ok=True)` then
`write_text`. Caller-controlled only (no receipt or table supplies it), so impact is a mis-set variable
or a typo overwriting a tracked path. The printed counting commands pass it unquoted:
`plans/round-84-claims.md` lines 49, 86, 117 (`--json-out $OUT`) and `--work $WORK`, so whitespace in
`$OUT`/`$WORK` is word-split. Remediation: require the receipt under `--work` (or a `--receipts` root)
via `commonpath`, and quote the expansions in the printed command.

## F8 — LOW — the pinned C1 control cannot witness *which* container it accepted

Pinned `freeze-precheck.py` lines 240–241 assign `receipt["control"]` inside the container loop, so
the record is the last container's cheap-rule score. In the frozen C1 command the order is round-83
then round-84, so the pinned-era receipt's single `control.accepted true` was the round-84 container's
score, not the round-83 target the predicate names. In fact the round-83 container's `instruments` is
non-empty (`tools/round-83/attribution-audit.py` pinned), so the cheap rule does accept it; the pinned
receipt simply could not show it. The current working-tree edit (F1) fixes exactly this by recording
`controls[]` and requiring `control_fired`; that fix is real but unpinned. Remediation: declare and pin
that change (F1), or emit one control object per container in the pinned instrument.

## F9 — LOW — the mutation selftest's fixture repo is not config-isolated, writes to the ambient TMPDIR, and has no toplevel assertion

`mutation-closure.py` line 231 `tempfile.mkdtemp(prefix="mutation-closure-selftest-")` uses the
process `TMPDIR` (unset → `/tmp`; the seat rule says never rely on `/tmp`), and lines 248–255 run
`git init/add/commit` with the inherited environment (`HOME` included) and no
`git rev-parse --show-toplevel` check. Inherited global config means `core.hooksPath`,
`init.templateDir`, or `commit.gpgsign` can act during those commands. The lane's own precedent does
both safeguards: `printed-command.py` lines 516–530 create the fixture repo with a four-key env and
assert `rev-parse --show-toplevel == realpath(scratch)`. Remediation: mirror that pattern and put the
fixture under `--work`.

## F10 — INFO — containment that does hold

- Claim-named and table `target` paths cannot read outside the repo: they reach only
  `git show <rev>:<path>` (`freeze-precheck.py` 44–45, 222, 231; `mutation-closure.py` 36–37).
  Verified: `git show 'HEAD:tools/../../etc/passwd.py'` and `'HEAD:.ufo/../../etc/passwd.py'` both
  fail `fatal: path … does not exist in 'HEAD'`; `git cat-file -e HEAD:/etc/passwd` exits 128. The
  regex at `freeze-precheck.py` line 39 admits `..`, but git rejects the resolved path.
- `--container` cannot point at an arbitrary filesystem file: containers are read as blobs at `--rev`
  (lines 222/231), so only committed bytes are scored.
- A rev beginning with `-` is consumed as a git option and rejected (`fatal: unrecognized argument:
  --no-patch:tools/…`), so the `f"{rev}:{path}"` construction did not yield a usable injection in the
  case tested.
- No `shell=True`, `os.system`, `eval`, or `exec` anywhere in the three instruments; every child is an
  argv list. REA envelope paths are used only as dict keys/strings, never joined to the filesystem.
- `mutation-closure.py`'s fixture copies are executed with `-I -B` (line 91), which ignores
  `PYTHON*` env and user site.

## F11 — INFO — candidate work surfaces conform (copy + patch)

- `w1/ExecPcDetectors/printed-command.py` (digest `91a01190…`) equals the frozen round-82 blob plus
  `printed-command-candidate.patch`: applied cleanly to a copy of `HEAD:tools/round-82/printed-command.py`
  in scratch and the resulting digest matched exactly.
- `w1/ExecSbDetectors/candidates/source-bind.py` (`3986706e…`) equals the frozen round-83 blob plus
  `source-bind.patch` (same check, digest match).
- Every seat artifact present at review time is under `.ufo/waves/round-84/w1/<seat>/` or the seat's
  report at `.ufo/waves/round-84/w1/<Seat>.md`; no `/tmp`, lane-tool, or fleet-root write appears in
  the seat artifacts or reports. Lane-tree writes observed at 16:52: the three frozen instruments
  (F1/addendum, uncommitted, unattributed to any seat artifact) and five production surfaces —
  `PROVINCE.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-83.md` —
  which match the plan's standing duties (PROVINCE/README, SKILL registry, sources, lesson
  correction) and are outside this seat's assigned surface; they were not audited. No instrument or
  counter wrote a lane path.

---

## Answers to the five assigned questions

1. **Write scope.** Tool code writes only `--json-out` (all three) and `--work` (mutation, nested);
   no hardcoded lane, `/tmp`, or `$HOME` writes. But `nested --work` deletes an arbitrary directory
   (F2), `--json-out` is unconstrained (F7), the mutation selftest uses the ambient TMPDIR (F9), and
   `npx` writes its package cache under `$HOME/.npm/_npx` (observed: 10 entries under
   `/home/vgpnk/.npm/_npx`). No receipt- or table-controlled path is written except the mutant `id`
   (F3). Lane-tree writes observed at 16:52: the three frozen instruments (F1/addendum — uncommitted,
   unpinned, unattributed to any seat artifact) and five production surfaces matching the plan's
   standing duties (`PROVINCE.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`,
   `corpus/lessons/round-83.md`; outside this seat's surface, not audited). No counter or instrument
   wrote a lane path.
2. **Path containment.** Receipt/envelope paths are never filesystem-joined (keys only). The table's
   `id` is joined without `commonpath` and escapes (F3); the table cannot name a target outside the
   repo because git rejects `..`/absolute tree paths (F10). Container/claim paths are constrained by
   git blob lookup (F10). `--work`/`--json-out` have no containment (F2/F7).
3. **Child environment.** Full `os.environ` to every child in both counters (F4), including a live
   `SSH_AUTH_SOCK`; `npx -y` registry code inherits it. No counter records env values wholesale, but
   output-derived fields (`pristine.case_names`, REA `stderr` tail) can carry an inherited value into
   a receipt (demonstrated with a canary).
4. **Execution.** `mutation-closure` executes only committed blobs selected by caller-supplied
   `--rev`/table `target`, with `-I -B`; it does not execute a caller-supplied filesystem artifact.
   Its fixture repo uses absolute `git -C`, but lacks `HOME` isolation and the toplevel assertion
   (F9). `nested-sqfs` executes no caller artifact, but executes registry code (`npx -y`) before any
   identity check and on fixture images it builds itself (F5). `freeze-precheck` executes only
   `git show`.
5. **Mutant table.** Yes — a row escapes `--work` through `id` (relative or absolute), confirmed with
   a live fixture run (F3); and an edited table is arbitrary code execution because replacement text
   is written into the executed copy. The frozen table is safe by content, but nothing binds the
   `--mutants` path to `fixtures.sha256` at runtime (F3).

## Receipts in this directory

| file | content |
|---|---|
| `fp-receipt.json` | pinned-byte `freeze-precheck` run on a fixture repo; no `controls` key (pre-drift) |
| `esc-receipt.json` | relative `--work`: pristine exit 2, all rows inconclusive (F6) |
| `esc-receipt-abs.json` | escaping ids wrote outside `--work`; `killed 2, ok true`; canary in `case_names` (F3/F4) |
| `nested-receipt.json` | victim `--work` deleted after a failed `mksquashfs` (F2) |
| `drift-freeze-precheck.diff` | `git diff HEAD` of the frozen instrument drift (F1) |
| `drift-nested-sqfs.diff` | `git diff HEAD` of the second drift (F1), current at 16:52 |
| `drift-mutation-closure.diff` | `git diff HEAD` of the third drift (addendum) |
| `drift-snapshot-1652.txt` | dated digest/status snapshot of all three instruments |
| `receipts.sha256` | digests of the above |

## Limits

No full C2 or C3 run (no 13-mutant closure, no REA extraction); those runtime claims are the
executors'/reviewers' receipts. Code findings cite the pinned revisions (verified at audit start);
the drift diffs are saved separately. No frozen file was edited and no remediation was applied.

## Addendum — live drift worsened during the audit (snapshot 16:52:19)

By the time this report was written, **all three** frozen instruments differed from their container
pins in the lane working tree; `claims.json`, `mutants.json`, and `plans/round-84-claims.md` remain
clean. Snapshot (`drift-snapshot-1652.txt`):

| instrument | pinned | working tree at 16:52 | mtime | nature of the change |
|---|---|---|---|---|
| `freeze-precheck.py` | `602239f5…` | `4aae3f26…` | 16:46:03 | per-container `controls[]`, `control_fired`, stricter `met` (fixes F8) |
| `mutation-closure.py` | `fd8aee39…` | `297883ee…` | 16:50:26 | new `unsafe_component()` refuses `..`/separators/absolute ids before any write, plus a selftest case; new reason token `unsafe-mutant-id` (fixes F3) |
| `nested-sqfs.py` | `08353f36…` | `938801ba…` | 16:51:44 | drops an unused import and changes A4/A8 to distinguish a dropped `analysis_depth` key from a present null (a ReviewerC3 probe), plus a selftest case |

Each change is a strictness increase consistent with a seat finding, and none is authorized by the
freeze: all are uncommitted and none is pinned by `claims.json`. Receipt provenance now splits:

- `.ufo/waves/round-84/l1/scores/c1-at-container.json` (16:46:07) was produced by the **modified**
  `freeze-precheck.py` (it contains `controls`/`control_fired`, which the pinned bytes cannot emit);
  it is unpinned.
- `.ufo/waves/round-84/l1/scores/c2-preintegration.json` (16:46:51) was produced by the **pinned**
  `mutation-closure.py`: it self-discloses `instrument.sha256 = fd8aee39…` and reports
  `mutants 13, killed 13, ok true`. It predates the 16:50:26 edit.
- `.ufo/waves/round-84/pre/c3-pilot.json` (16:36:25) predates the wave and the edits; `met true`.

Any final receipt produced from the lane path now executes unpinned bytes for all three claims. If
the working tree is committed as-is, the container's pins become stale for every counter it names,
and a re-run of C1 at that revision would emit `COUNTER_PIN_MISMATCH` for the three counters (the
pin check reads `git show <rev>:<path>` while the command executes the path). This is the
execute-vs-verify split in F1, now affecting the whole instrument set rather than one file.

Integration options (L1 decision; neither applied): restore the three paths from the pinned blobs and
re-measure all three claims from those bytes, or declare an instrument supersession — new digests
pinned in a new container with a new declaration pointer, disclosed as `instrument_supersessions`,
all three claims re-measured, then the freeze-ledger row. Committing the working tree without either
would put an unpinned predicate behind a pinned claim.
