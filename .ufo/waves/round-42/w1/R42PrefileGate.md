# R42PrefileGate — pre-file gate for round N (build, selftest, live round-41 run)

**Verdict: DONE.** `prefile-gate.py` (stdlib, read-only) enforces the four pre-file conditions;
its 12-case sandbox selftest is green (12/12) and four injected mutants are each caught. The
real lane at HEAD `fdabdfa4` is **GREEN for round 41** (two exit-neutral advisories). The two
round-41 closure defects it was meant to catch are **reproduced as RED** on the round-41
closure commit `74064474` in a sandbox clone — (a) wave 2 still running (closure D1), (d) the
dead pointer `w2/R41W2C2Table.md` (closure D2) — and a third red (b) reproduces for the
`ae5dc3f3` lane view that still carried the untracked round-42 draft.

Artifacts: `.ufo/waves/round-42/w1/artifacts/R42PrefileGate/` (tool, selftest, live runs,
mutants, hashes). Tool sha256 `c3f8abf984fa4f2c247b3b3629721429fc212cb51fe80eeb7aaea0946a2688b6`
(`sha256.txt` lists every artifact except itself). No installs were needed (python3 3.14.8, git 2.56.0 on
PATH); no REA/unblob/sasquatch invocation, so no reserved carrier was touched.

## 1. What the gate checks

`prefile-gate.py --root LANE --round N` (lane work-tree toplevel required; `--root` inside a
work tree but not the toplevel is rejected). Exit 0 only when all four hold; 1 on any FAIL;
2 for argparse usage errors.

| cond | spec clause | implementation |
|---|---|---|
| a | every `.ufo/waves/round-N/<wave>.ready` has `<wave>.ready.dispatched` **and** a results file beside the dispatch json | wave set = regular files matching `*.ready`; for each: marker must be a regular file; results accepted as `<wave>-results.json` or `rN-<wave>-results.json` in the directory of `<wave>-dispatch.json` (wave root when that file is absent). FAIL otherwise. |
| b | `git status --porcelain` lists nothing under `.ufo/waves/round-N/`, `corpus/evidence/round-N/`, `plans/`, `tools/round-N/` | one `git status --porcelain=v1 -z -uall -- <four scopes>`; every entry (incl. rename source) matching any scope is a FAIL line. `-uall` is a strict superset of plain porcelain: it lists files inside untracked directories instead of one collapsed `dir/` line. |
| c | no stray `*.err` in the lane root | regular files matching `LANE/*.err`. |
| d | every `w*/<Name>.md` path cited in `corpus/lessons/round-N.md` exists in the committed tree | lesson bytes are read from **HEAD** (`git show HEAD:…`), never the worktree; each `w<N>/<Name>.md` citation is resolved to `.ufo/waves/round-N/w<N>/<Name>.md` and must exist in HEAD (`git cat-file -e HEAD:…`). Missing lesson in HEAD is itself a FAIL. |

Exit-neutral advisories (reported, never a FAIL): ignored paths under the four scopes
(`tools/round-41/__pycache__/`); `.err` files under the round's wave/evidence dirs (outside the
lane-root rule); nested `w*/…/*.md` citations; bare `R<N>*.md` wave-report names that resolve in
no wave dir in HEAD; a lesson with uncommitted edits (the gate reads HEAD bytes); a results
ledger whose `round` field, `seats` count or entry count disagrees with the dispatch
`counts.total`, or that does not parse as JSON; an orphan `*.ready.dispatched` without a
`*.ready`.

Read-only proof (`cli-guards.txt`, and the run below): the gate writes no temp files — with
`TMPDIR` pointed at an empty directory it stayed empty (`0` → `0` entries) — and it never
mutates git: lane `rev-parse HEAD` and `git status --porcelain` line count are identical before
and after a run. The only git commands used are `rev-parse`, `cat-file -e`, `show`,
`status --porcelain`, `ls-files`, `ls-tree`.

## 2. Selftest (sandbox git fixtures)

`prefile-gate.py --selftest` builds each fixture with `tempfile.mkdtemp(dir=$TMPDIR)` (honours
`TMPDIR`; `--work DIR` overrides), `git -C <fx> init -q`, asserts
`git -C <fx> rev-parse --show-toplevel` equals the fixture path before any commit, commits with
`-c user.name=fx -c user.email=fx@fx`, then removes the tree. `selftest.txt`:

```
SELFTEST PASS green-clean                                  expect=0 got=0
SELFTEST PASS red-wave-running-no-dispatched               expect=1 got=1
SELFTEST PASS red-wave-no-results                          expect=1 got=1
SELFTEST PASS green-results-both-naming-variants           expect=0 got=0
SELFTEST PASS red-tracked-modification                     expect=1 got=1
SELFTEST PASS red-untracked-in-every-scope                 expect=1 got=1
SELFTEST PASS red-stray-err-in-lane-root                   expect=1 got=1
SELFTEST PASS red-dead-pointer                             expect=1 got=1
SELFTEST PASS red-lesson-not-committed                     expect=1 got=1
SELFTEST PASS green-dirty-lesson-reads-head-bytes          expect=0 got=0
SELFTEST PASS advisory-partial-ledger                      expect=0 got=0
SELFTEST PASS advisory-only-ignored-residue-and-bare-name  expect=0 got=0
SELFTEST cases=12 pass=12 fail=0
EXIT=0
```

Coverage of the clauses: (a) missing marker and missing results are separate reds; both
accepted results spellings are exercised in one green fixture; (b) is exercised by a tracked
modification (`plans/`) and by one untracked file in **each** of the four scopes; (c) by a
root `green.err`; (d) by a committed lesson citing a missing `w2/R41Missing.md`, and by a
lesson present on disk but absent from HEAD. Two fixtures pin the "advisory is not a FAIL" and
"HEAD bytes, not disk bytes" semantics.

The harness can fail: four mutants of the tool, each run through the same 12 cases
(`mutants.txt`) — `m1` `_in_head` always true (3 failures), `m2` stray-`.err` check disabled
(1), `m3` exit code forced to 0 (7), `m4` dispatch-marker check disabled (1). No mutant
survives.

## 3. Live run on the real lane, round 41

`round-41-real.txt`, HEAD `fdabdfa4` (the L1 landed round-42 dispatch during this seat's run;
HEAD was `ae5dc3f3` when the seat started — both heads are recorded in the artifacts):

```
(a) waves settled                                        PASS
    PASS  2/2 waves settled (w1, w2)
    note  wave w1 settled: .ufo/waves/round-41/r41-w1-results.json (252545 bytes)
    note  wave w2 settled: .ufo/waves/round-41/r41-w2-results.json (132150 bytes)
(b) tree clean under round scopes                        WARN
    PASS  git status clean under .ufo/waves/round-41, corpus/evidence/round-41, plans, tools/round-41
    WARN  1 ignored path(s) under round scope (build/scratch residue): tools/round-41/__pycache__/
(c) no stray .err in lane root                           WARN
    PASS  no *.err in lane root
    WARN  2 tracked + 0 untracked .err under round evidence/wave dirs (outside the lane-root rule; e.g. .ufo/waves/round-41/w1/artifacts/R41C2ControlTables.step.err)
(d) lesson wave-report pointers resolve in HEAD          PASS
    PASS  7 w*/<Name>.md citation(s) resolve in HEAD (0 nested advisory, 15 bare name(s) checked)
GATE GREEN  (exit 0)
```

**Red findings on round 41 at the current tip: none.** All four conditions hold (§3.1 gives
the two advisories). Round 41 is green *now*; that is a different claim from "the gate would
have passed at closure", which is measured in §3.2 and is false.

### 3.1 Advisories (exit-neutral, worth a lane fix)

- `tools/round-41/__pycache__/` is ignored build residue inside a frozen scope; the frozen
  tools are byte-identical but the directory should not exist in a lane someone copies from.
- Two `.err` files are **committed** under `.ufo/waves/round-41/w1/artifacts/`
  (`R41C2ControlTables.step.err`, `R41C2Mutants/counter-cased-pristine-debug.err`). They are
  outside the lane-root rule (c), so the gate does not red them; the D1 fix ("delete the stray
  `.err` files") only named the lane root and `corpus/evidence/round-41/c1/V4/`, so these two
  survived. Removing them is left to the L1 — this seat may not write outside its artifacts.
- `15` bare `R41*.md` names in the lesson (e.g. `R41W2ReproV3.md`, `R41W2C1Oracle.md`,
  `R41W2Reservation.md`, `R41W2C1Removal.md`, `R41W2C1AxisFit.md`) resolve in a wave dir in
  HEAD; had any of them not resolved the gate would warn only, because the binding clause is
  the `w*/<Name>.md` form. Flagged as a scope limit, not a finding.

### 3.2 Red findings reproduced from the round-41 closure commit `74064474`

A `--shared` sandbox clone at `74064474`, worktree verified clean before the run
(`round-41-at-74064474.txt`, `.json`):

```
(a) waves settled                                        FAIL
    FAIL  wave w2 is still running: .ufo/waves/round-41/ has no w2.ready.dispatched
    FAIL  wave w2 has no results file (looked for w2-results.json and r41-w2-results.json)
    note  wave w1 settled: .ufo/waves/round-41/r41-w1-results.json (252545 bytes)
(b) tree clean under round scopes                        PASS
(c) no stray .err in lane root                           WARN
(d) lesson wave-report pointers resolve in HEAD          FAIL
    FAIL  cited wave report missing from HEAD: w2/R41W2C2Table.md (.ufo/waves/round-41/w2/R41W2C2Table.md)
GATE RED — failing: a, d  (exit 1)
```

- (a) is closure **D1**: the report was filed before wave 2's WAVE-DONE — `w2.ready.dispatched`
  and `r41-w2-results.json` are absent from that commit, so the gate refuses.
- (d) is closure **D2** verbatim: the R40-CL5 row cites `w2/R41W2C2Table.md`, which is in
  neither the commit nor the worktree at `74064474`. Both pointers now exist at `fdabdfa4`,
  which is why the current-tip run is green.

### 3.3 Red finding reproduced for the `ae5dc3f3` lane view (literal `plans/` scope)

At the moment this seat started, HEAD was `ae5dc3f3` and `git status --porcelain` showed
`?? .ufo/waves/round-42/` and `?? plans/round-42-claims.md`. Reconstructed in the clone
(`ae5dc3f3` tree + the byte-identical untracked draft copied in), `round-41-at-ae5dc3f3-plus-untracked-r42.txt`:

```
(b) tree clean under round scopes                        FAIL
    FAIL  uncommitted under round scope: ?? plans/round-42-claims.md
GATE RED — failing: b  (exit 1)
```

This is the literal spec: the `plans/` scope is not round-scoped, so **a later round's draft in
the worktree reds an earlier round's gate**. That is arguably the right behaviour for a
pre-file gate (freeze the round before starting the next draft), but the L1 must know that
(a) a round-N gate run must not race round-N+1's drafting, or (b) the scope should become
`plans/round-N-claims.md` — a spec change I did **not** make on my own authority. Note the
red disappeared at `fdabdfa4` only because the L1 committed that draft.

### 3.4 Live behaviour on round 42 (current reds, as intended)

`round-42-inflight.txt`, HEAD `fdabdfa4`: **GATE RED — failing: a, b, d (exit 1)** — (a) wave
w1 has no results file yet; (b) the uncommitted wave-1 tree (dispatch artifacts, sibling wave
reports, every seat's artifacts, `w1-validate.out`, `w1.ready.dispatched`); (d)
`corpus/lessons/round-42.md` does not exist in HEAD. This is the gate working as specified
while wave 1 runs; it is the state the L1 must clear before filing the round-42 report.

## 4. Notes for the L1 (integration)

- Run order that makes the gate meaningful: commit results ledger + lesson + wave reports
  **first**, then `prefile-gate.py --root … --round N`, then file the report. The gate reads
  the lesson and citations from HEAD, so an uncommitted lesson is a red by design.
- The gate cannot see untracked closure residue from history: D1's stray `green.err`/`red.err`
  were never committed, so a clone-based re-run of (c) cannot reproduce them (they are gone
  from the live worktree now). Condition (c) must be run in the live lane.
- (a) accepts a results file that exists in HEAD even if deleted on disk; the deletion would
  appear as ` D` under (b), so the pair still fails.
- `--ignored=matching` needs git ≥ 2.16 (host: 2.56.0). Everything else is git ≥ 2.9 syntax.
- No code was placed in `tools/`; the tool lives in this seat's artifacts for the L1 to
  integrate (`tools/round-42/prefile-gate.py` is the natural home) and to re-point its
  `--root`/`--round` at round 42.

## 5. Risks / limits (calibration)

- **Timing-sensitive claim.** §3 is GREEN at `fdabdfa4`; HEAD moved twice during this seat's
  work (`ae5dc3f3` → `fdabdfa4`), so every artifact records the head it measured. A re-run at
  a later head may legitimately differ.
- Advisory thresholds are judgement calls, not spec: `seats`/`counts.total` disagreement is a
  WARN because a wave can be declared done with failed seats; the ledger counts for round 41
  currently agree exactly (41/41, 33/33).
- The (d) regex only accepts paths whose last segment is `<Name>.md` directly under `w<N>/`
  (per spec); deeper citations and bare names are advisories. [INFERENCE] the spec's intent is
  the D2 failure mode (a cited wave report that does not exist), which the binding form covers.
- The tool does not validate that results entries correspond to dispatched seat names; that is
  a different check than the four specified and is not claimed.

## 6. Reproduction

```
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-42/w1/artifacts/R42PrefileGate
python3 "$A/prefile-gate.py" --selftest                     # 12/12, exit 0
python3 "$A/prefile-gate.py" --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 41   # GREEN at fdabdfa4
python3 "$A/prefile-gate.py" --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 42   # RED a,b,d while wave 1 runs
# closure reproduction:
D=$(mktemp -d "$TMPDIR/fx.XXXX"); git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$D/lane"
git -C "$D/lane" checkout -q 74064474
python3 "$A/prefile-gate.py" --root "$D/lane" --round 41    # RED a,d (D1, D2)
```
