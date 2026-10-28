# R46W1ConnFleet — cross-claim and cross-source pattern scan

Lane `kaidoku`, round 46, wave 1. Role: connector (sibling/cross-source overlap scan).
Read-only on the lane tree; every receipt below was produced from Git objects or from a
counter run with `--json-out` under this seat's wave directory.

**Measured revision:** `deee6595ae3dda094aa5a577fac0f6903e873e16` (HEAD at 2026-10-28T17:06:49Z).
The tree moved twice during this seat (`49e6cac4` → `21b55a8f` → `deee6595`); every value below
is bound to `deee6595`, and an L1 reconciling at a later tip must re-run the two counting
commands. Scratch root `/fast/scratch/hyaku/kaidoku-r46/R46W1ConnFleet` was set in
`TMPDIR`/`HYAKU_SCRATCH` and removed after the receipts were copied here.

---

## 1. Fleet guard inventory — what `scripts/hyaku/` already refuses

Three scripts, read in full. Guards are listed with the line that *implements* them; the
column "gate?" is the answer to R45-CL1's placement question.

### `scripts/hyaku/jj-lane.sh` (841 lines) — lane repo VCS

| Guard | Location | Refuses / enforces | Exit | gate? |
|---|---|---|---|---|
| `lane_realdir` | 77–92 | non-clone (`.git` must be a directory, so worktrees/submodules are out); the fleet root itself (literal **and** derived path) | 1 | yes |
| `take_lock` | 135–143 | per-physical-path `flock`, 300 s (`commit .` and `commit /abs/lane` contend on one lock) | 1 | — |
| `cmd_state` | 158–186 | reports `branch/local/remote/ahead/behind/head/tracked/untracked`; `status=$(git -C "$dir" status --porcelain)` at 180, `tracked`/`untracked` counts at 181–182 | 0/1 | **no — report only** |
| init quiescence | 455–490 | in-progress merge/cherry-pick/revert/rebase, unmerged index, **staged entries**, diverged branch, detached-HEAD-on-non-tip | 1 | yes (init only) |
| `repo_path_allowed` | 506–519 | `''`, `.`, `..`, `../*`, `/*`, `.git*`, `.jj*`, `.ufo`, `.ufo/state*`, `.ufo/watchdog.log` | 1 | yes |
| `validate_change_scope` | 522–571 | `diff-tree --name-status -z --no-renames`; status ∈ {A,M,D,T}; every changed path inside the requested set; `D` whose file still exists on disk; empty change set | 1 | yes |
| `candidate_is_child_of` / `candidate_is_conflict_free` / `candidate_has_identity` | 574–596 | single-parent child of the branch tip; no unresolved jj conflicts; author **and** committer exactly `<id>-shokunin <id>@shokunin.local` | 1 | yes |
| `classify_push_error` | 186–196 | only "unexpectedly moved"/"stale info" is recoverable; hook/permission/tracking/conflict rejections are fatal | — | — |
| `push_preflight` | 199–232 | lane identity recorded; bookmark not conflicted; tip conflict-free; `origin/<b>` present; **fast-forward only**; every commit in `origin/<b>..<b>` carries lane-or-protocol author **and** committer | 1 | yes |
| `report_landed` | 237–268 | remote tip == local tip via `ls-remote`; this run's commit an ancestor of it (else `rewritten old -> new`) | 1 | yes |
| `recover_remote_move` | 300–349 | rewritten remote; ≥2 unpushed tips (divergent); conflicts after the recovery rebase; rebases only the unpushed range; reanchors the worktree only when `@` is empty | 1 | yes |
| `do_push` | 350–375 | 3 attempts; on a lease rejection: recover → re-`push_preflight` | 0/1 | yes |
| `cmd_commit` guard cluster | **707–712** | the four candidate guards + `validate_change_scope`, all **after** the jj commit object exists and **before** `bookmark set` | 1 | yes |
| `cmd_recover` guard cluster | **786–791** | same cluster before the bookmark write | 1 | yes |

### `scripts/hyaku/fleet-commit.sh` (121 lines) — fleet-repo commits

One `flock` at **52** serialises every fleet-repo commit+push; lane-id charset at 43–44;
pathspec-limited only — the `for p in "$@"` loop at **67–90** skips a missing path with a
warning and never tracks untracked strays; nothing-to-commit → 0; `main` and `master`
fast-forwarded together at **94–101**; push retried four times; **exit 3 = committed, push
failed**. No content check of any kind.

### `scripts/hyaku/inline.sh` (220 lines) — dispatch/verify/advance

`disk_gate` before any dispatch write at **128–132**; `verify` runs `report_of` (content gate:
SHONEN heading, minimum bytes) at **156**, then **sweeps** an uncommitted report with
`fleet-commit.sh --as <lane>` at **157–161**, then a fast-forward-only durability push at
**165–171**; a dirty lane repo is a **WARN** at **172**, not a failure; `advance` purges the
closed round's scratch at **210**.

### R45-CL1 answered: no lane-side gate runs before a commit or a sweep

- `grep -rn "attest\.py\|registry\.py\|round-46" scripts/` → **empty**. No fleet script invokes
  either round-46 instrument.
- No hook mechanism exists: `grep -n "hook"` over the three scripts returns only the
  push-error comment at `jj-lane.sh:188`.
- The sweep path (`inline.sh:157–161`) commits the report path with **no** lane-defined check;
  the closest thing to a dirty gate is the WARN at 172, which cannot fail anything.
- `fleet-commit.sh` has exactly one serialised entry point (the flock at 52) and it is the
  natural host for a lane-side gate, but nothing calls one.

**Where R45-CL1's placement argument is too strong.** The three scripts already run a
*fleet-generic* gate cluster at `jj-lane.sh:707–712` and `:786–791` **after the commit object
exists and before the bookmark advances**, and `fleet-commit.sh:52` is a single choke point for
the fleet repo. So the lane cannot *write* the hook (correct; `scripts/` is read-only for the
lane), but it **can name the exact insertion line and the exit contract** (1 = block, 2 = do
not block). R45-CL1 should say "can specify, cannot land" rather than "cannot make the sweep
run it".
**Second-order:** R45-CL1's recorded *substitute* was the round-45 `--check-dirty` arm, and
that arm does not exist in round 46 (finding F2). The substitute regressed without a routed
defect.

---

## 2. Duplication map — which instrument is a fleet mechanism, which is lane-local

`tools/round-46/` = `attest.py` (643 L), `registry.py` (538 L), `gate.py` (224 L),
`census.py` (79 L), `census.json` (38 paths).

| Instrument surface | Fleet mechanism it repeats | Classification |
|---|---|---|
| `gate.freeze_state` — merge-aware history arm + independent blob arm + derived frozen set (`gate.py:144–172`) | none. `jj-lane.sh:522` `validate_change_scope` is per-commit pathspec confinement, never a range query or a frozen set | **genuinely lane-local** |
| `gate.frozen_set` (`gate.py:63–88`) | none — the fleet never derives a frozen set | **genuinely lane-local** |
| `gate.out_path` — refuses `--json-out` inside the graded/frozen bytes or outside the lane (`gate.py:175–188`) | none (fleet receipts go to `$STATE`, not into a repo) | **genuinely lane-local** |
| `gate.scratch` — refuses a bare `/tmp`/`/var/tmp` root (`gate.py:190–203`) | **`scripts/hyaku/disk-guard.sh`** owns this policy; `inline.sh:128–132` is its client (comment at `inline.sh:17–25`: "every long run ended with /tmp at 100 %") | **duplicate policy, separate implementation** |
| `gate.dirty` (`gate.py:132–142`) | `jj-lane.sh:180–182` runs the same `git status --porcelain` probe for `cmd_state`; `inline.sh:172` warns on it | **duplicate probe — and unwired** (F2) |
| `attest.run_battery` / `fixture_repo` (`attest.py:362–415`) | shape repeats `scripts/sources-census.sh --selftest` (per-code mutation fixtures, `sources-census.sh:126–162`) and `scripts/hyaku/*-selftest.sh`; different object | **mechanism duplicate, data-local** |
| `attest` sha256 pin clause (`attest.py:245–251`) | none — the fleet pins identity/ancestry, never bytes | **genuinely lane-local** |
| `registry.py` section/header/cell checks (`registry.py:74–135`) | **`scripts/sources-census.sh`** — one registry table, `## Registry` anchor at `:611`, `NF!=13 → E01` at `:635–636`, separator/header handling at `:591–599`, exit **2** on a missing registry (`:17–18`), and `usedby_findings` at `:538–573` checks that a `used-by` path exists (the presence analog) | **duplicate mechanism, broader re-scope** |
| `registry.py` presence-at-rev (clause 5) | `sources-census.sh:563–570` `[ ! -e "$dir/$path" ]` (E11) is the same idea for source `used-by` paths | **duplicate mechanism** |
| `registry.py` fence/comment arms | **none** — `sources-census.sh` has no fence/HTML-comment handling (grep for fences returns nothing) | lane-local, and **strictly better than the fleet's** |
| 0/1/2 exit contract | `sources-census.sh:17` (2 = usage/env/missing registry) and `jj-lane.sh` (0/1/3/64) | **shared convention, correctly reused** |
| `census.py` + `census.json` | repeats the *idea* of `sources-census.sh census`, not its data | **concept duplicate, data-local** |

**Conclusion for the registry rows.** C2 is, at the mechanism level, a second implementation of
the fleet's census/registry validator (`scripts/sources-census.sh`) re-scoped from sources to
instruments, with three additions the fleet lacks (marker-bound section, exact cell 0, presence
at a revision). C1 is genuinely lane-local except two probes (`dirty`, `scratch`) that restate
fleet policy without sharing it. The four landed rows (`SKILL.md:1732–1735`) say none of this.

### Paste-ready row amendments (cell 2 only — clause 2/3/4-safe)

Append the quoted sentence to the **`gate or probe - purpose`** cell of each row. Cell 0
(clause 3) and the verdict-map cell (clause 4) are untouched, so `registry.py --profile v2`
re-runs unchanged.

- `tools/round-46/attest.py` → `Lane-local: no fleet script invokes it (`grep -rn attest.py scripts/` is empty); its only fleet overlap is the unwired dirty probe, see the gate.py row.`
- `tools/round-46/census.py` → `Lane-local re-scope: scripts/sources-census.sh:1-30 owns the fleet census contract for corpus/SOURCES.md and stays the authority there; this tool re-derives instruments, not sources.`
- `tools/round-46/gate.py` → `Partly duplicative by policy, not by code: scratch() restates the /tmp refusal owned by scripts/hyaku/disk-guard.sh (client inline.sh:128-132), and dirty() restates the jj-lane.sh:180-182 status probe but has no caller, so it gates nothing.`
- `tools/round-46/registry.py` → `Second implementation of the registry mechanism the fleet already runs for sources (scripts/sources-census.sh:611 heading anchor, :635-636 NF=13, :538-573 used-by presence); broader here (fence/comment arms, exact cell 0, presence at a revision) and not fleet infrastructure.`

---

## 3. The rule the round-46 claims should cite

**Primary — `templates/round-prompt.md:54-58`** (the fleet's existing census contract, which
R46-C2 never cites):

> `2. **Record the census before → after.** Run this command at round start and at round`
> `   end; paste both outputs and their exit codes. Exit 0 is required at round end for`
> `   conformance. Exit 2 is expected at round start only when `corpus/SOURCES.md` does not`
> `   yet exist.`

with the command at `templates/round-prompt.md:65`:
`sources-census.sh validate --root {{FLEET_ROOT}} {{LANE}}`.

Why this one: C2 is a *second* census instrument, and the fleet already fixes the census
contract — exit 0 at round end, exit 2 only for a missing registry, before→after with both
outputs and both exit codes. The claims file names the control receipts that supply the
before→after (`controls/ctl-c2-*`) but cites no rule that demands them, and says nothing about
the instrument it is parallel to. Citing this line does three things at once: it binds C2's
0/1/2 semantics to the fleet's, it records that `sources-census.sh` remains the authority for
`corpus/SOURCES.md` (so `registry.py` cannot be mistaken for a replacement), and it gives the
control receipts their warrant.

**Secondary — `MISSION.md:81-86`** (push scope, the rule that bounds `FREEZE..REV`):

> `## Push scope — hard rule`
> `Lanes push ONLY to the fleet repo (`$SHOKUNIN_ROOT`, remote operator-chosen) or`
> `their own `<lane>-shokunin` remote.`

Why: the freeze-integrity rule is a claim about what entered the lane's history between two
commits. Only two writers can do that — the lane itself and a non-author fleet sweep committing
into the lane repo (the round-44 defect behind R45-CL1/CL5). The claims file should name which
of the two it treats as `frozen_path_changed`; as written, both are, and the external one is
not something the lane can gate.

**Tertiary — `templates/round-prompt.md:14-17`** (lowest-axis obligation): already honoured via
`SCORECARD.md ## Owned axes`; no action.

---

## 4. Findings

Each finding gives the command, the measured value, and the differing value. None was "fixed":
the two instruments and the claims file are frozen.

### F1 — HIGH, calibration — the frozen file's own freeze is not the freeze at which it can be scored

- Rule: `plans/round-46-claims.md:6-10` — freeze = the commit that **first** contains this file
  and `tools/round-46/`; "The report cites it as `plans/round-46-claims.md@<freeze>`;
  `git log --format=%H -1 -- plans/round-46-claims.md` re-derives it. Nothing in this file or in
  `tools/round-46/` changes after the freeze: a change makes both counters exit 2."
- `git log -1 --format=%H -- plans/round-46-claims.md` → `31820472784284727546808acc31b3ea1e73919b`
  (the only commit touching that file). `git log -1 --format=%H -- tools/round-46/` →
  `0425224756791b414454df28a9abf93dcdf154ce`.
- `attest.py --freeze 3182047 --rev deee6595 --no-battery` → **exit 2**, `frozen_path_changed`
  = `[tools/round-46/, tools/round-46/attest.py, tools/round-46/gate.py,
  tools/round-46/registry.py]`, `restored` = three of them (`receipt:
  w1/R46W1ConnFleet/freeze-3182047-at-head.json`, sha256 `3a471c33…`).
- The met receipts use `--freeze 0425224` → exit 0.
- The re-declaration lives only in `LOG.md:3327` ("**The declared freeze is `0425224`**") and
  `SCORECARD.md:3603`, i.e. outside the frozen bytes and outside the file the rule names.
- **Contradiction, stated not smoothed:** by the file, both claims are unscoreable (exit 2) at
  their own declared freeze; by the record, they are met at a later commit that itself touches
  the frozen directory. Both statements are measurements; they cannot both be "the freeze".
  This is the R45-CL1 defect class at the document level — the gate (here, the identity of the
  freeze) was fixed after the thing it gates was produced. Because editing the frozen file makes
  every later score exit 2, the durable remedy cannot be an edit to it.

### F2 — HIGH, depth — block 23's `dirty` row describes an arm that no round-46 code computes

- `SKILL.md:622` (row R45-CL15): *"dirty: the dirty scope is the union of the pathspecs, and
  each arm has a red case that names it"*, exit `1`.
- `tools/round-46/gate.py:132` defines `def dirty(root, pathspecs)`. Callers:
  `grep -rn "dirty" tools/round-46/` → only `gate.py:132` (definition), `attest.py:46`
  (the `ARMS` vocabulary string) and `attest.py:508` (the selftest row text). **Zero call
  sites.** `attest.py`'s CLI (`attest.py:471-480`) has no `--check-dirty` and no
  `--dirty-pathspec`; `registry.py` has none either.
- Clause 4 of the predicate checks only that the arm cell contains a token from `ARMS`
  (`attest.py:46`), so a row naming an unimplemented arm passes. That is the R45-CL13
  "structural proxy accepts garbage" class one level up: the matrix that exists to reject
  unfalsifiable rows contains one.
- Cross-claim: R45-CL1's mitigation ("the gate's `--check-dirty` arm catches the precursor")
  is gone in round 46 and no routed defect records the regression. `SKILL.md:589` (block 22,
  the round-45 table) still advertises `dirty[] from --check-dirty`; that is true of
  `tools/round-45/frozen-path-preflight.py`, not of round 46.
- Claim impact: none — clause 4 is token-based and passes, and clause 7's battery is
  independent. This is a truth/calibration defect, not a predicate failure.

### F3 — MEDIUM, calibration — the duplication is real and undisclosed

Covered in §2. Concretely: `registry.py:74–135` re-implements the `## Registry` table validator
that `sources-census.sh:611/635–636` already runs; `gate.scratch` re-implements the
`disk-guard.sh` refusal; `gate.dirty` re-implements `jj-lane.sh:180–182`. Rows
`SKILL.md:1732–1735` present all four instruments as if nothing in the fleet did this work.
A reader of the registry cannot tell lane-local from fleet-wide, which is precisely what the
calibration axis measures.

### F4 — MEDIUM, calibration — the frozen file's own preflight numbers are wrong at the measured bytes

- `plans/round-46-claims.md:192` — "`attest.py --selftest` prints `cases=15 failures=0`";
  measured: `ATTEST_SELFTEST: cases=16 failures=0`.
- `plans/round-46-claims.md:194` — "`registry.py --selftest` prints `cases=11 failures=0`";
  measured: `REGISTRY_SELFTEST: cases=12 failures=0`.
- The working tree is byte-identical to the freeze: `git diff --stat 0425224 HEAD -- tools/round-46/`
  is empty and `git status --porcelain -- tools/round-46/` is empty. So no post-freeze change
  explains the gap; the file predates the three instrument corrections and was never re-derived.
- This is R45-CL24's "the record drifted from the instrument" inside the dated-to-prevent-it
  artefact. Claims stand (the numbers are not predicate clauses); the values are unusable as a
  check. Erratum, not an edit.

### F5 — LOW — the fidelity pair is stated in reverse order

`plans/round-46-claims.md:100` — "`--spec r45 --profile v1` at `f59565b7`/`f762b727` reproduces
the round-45 receipt (… exit 0)". As a freeze/rev pair that is exit 2
`freeze is not an ancestor of rev` (`w1/R46W1ConnFleet/fidelity-A.stdout`). Reversed
(`--freeze f762b727 --rev f59565b7`) reproduces exactly: exit 0, `rule_blocks 22`,
`block_present 1`, `rows 10`, `refs 8`, `unresolved_citations []`
(`fidelity-B.stdout`). So the value is right and the argument order is wrong — copying the
command from the rule yields could-not-evaluate.

### F6 — OBSERVATION — `battery.genuine_green == 1` is entailed, and that is fine

`attest.evaluate:450-452` runs the battery only when the structural score is already 0, and
`run_battery:406-408` re-scores the same unmutated artefact at the same rev to set
`genuine_green`. The clause therefore cannot fail when it is reached. It documents the control
and costs nothing; the discriminating power is `v1_green == 9` / `v2_green == 0`, both measured
(`c1-freeze-0425224.json`: 9/0/1/0; `c2-freeze-0425224.json`: 7/0/1). Worth one sentence in the
report so nobody cites it as a passing test of anything.

### Positive verification (needed for the L1 to reconcile)

| Claim | Command | Exit | Value |
|---|---|---|---|
| C1 | `attest.py --root <lane> --freeze 0425224 --rev deee6595` (battery on) | **0** | `rule_blocks 23`, `marker_occurrences 1`, `block_present 1`, `rows 13`, `refs 9`, `failing []`, battery `9/0/1/0` |
| C1 selftest | `attest.py … --selftest` | **0** | `cases=16 failures=0` |
| C2 | `registry.py --root <lane> --freeze 0425224 --rev deee6595` | **0** | `scope_size 38`, `unregistered []`, `thin []`, `absent_at_rev []`, battery `7/0/1` |
| C2 selftest | `registry.py … --selftest` | **0** | `cases=12 failures=0` |

The forgeries are mutations of the landed block, not of a template:
`run_battery:391-397` takes `gate.show(root, rev, "SKILL.md")`, isolates the single marked block,
and applies `MUTATIONS` to it; `fixture_repo:362–383` writes a one-commit repo and raises on a
`--show-toplevel` mismatch. Verified by reading, and by the fixtures' failure texts naming the
landed rows (`"routed ids not named by any row"`, `"rows 8 < 13"`).

---

## 5. Proposed move (one, bounded)

**Add row 14 to craft block 23: `R45-CL1` with the `commit` arm, asserting that a freeze's
identity is re-derived from the frozen bytes' own history, and cite F4/F5 as errata in the same
block.** This is a synthesis: it uses the `commit` arm the round already built
(`gate.history_touched`, `gate.py:91–115`), the routed id R45-CL1 that block 23 currently omits
(13 rows carry CL2/6/7/9/13/14/15/18/19/20/22/23/24 — CL1 is the one routed defect with no row),
and the measurement I just made (an earlier freeze exits 2 with a non-empty `restored`).

Row text (four cells, house vocabulary, exit `2`):

```
| R45-CL1 a preflight that cannot run before the sweep cannot gate the round | the freeze was declared in a file written before the bytes it describes, so the declared freeze could not be scored at all | commit: the freeze is the last commit touching the frozen set; the touch list is re-derived (`git log -1 --format=%H -- tools/round-46/`) and an earlier freeze exits 2 before any score | 2 |
```

Plus one prose sentence in the block, carrying the two errata as citations rather than
corrections: `plans/round-46-claims.md:6-10` (the stale freeze definition) and
`plans/round-46-claims.md:192-194` (the stale selftest counts).

**Affected axes**
- calibration **improved**: the freeze identity becomes re-derivable from the frozen bytes
  instead of from a pre-correction declaration; the registry's own claim about what its counters
  bind is now checkable.
- depth **improved**: the block gains the one routed defect it was missing, and the row's arm is
  code (`history_touched`), not prose — unlike F2's `dirty` row.
- coverage **unchanged** (no new surface), operability **unchanged** (no flag, no invocation
  change), freshness **unchanged**.
- No axis harmed: rows go 13 → 14 (`>= 13`), the required thirteen ids all remain, header,
  marker count, last-block position and the sha256 pin are untouched.

**Risks (stated, each with the mitigation)**
1. *Path-like tokens in block prose are read as citations.* Commit `87578656` exists because
   block 23 emitted path tokens the citation sweep counted. Any added path must carry a line
   selector (`plans/round-46-claims.md:6-10`) or be described in words. The row above uses one
   command string, not a bare path.
2. *The row could over-claim automatic derivation.* `attest.py` takes `--freeze` as an argument
   and never computes the identity itself; the row must state the caller obligation. The arm it
   can enforce is the negative one — an earlier freeze exits 2 — and that is the measured fact.
3. *A new row is not a new falsifier.* The instrument is frozen, so no red selftest case can be
   added this round. Route that to round 47 as a routed defect (`M46-n: block 23 row 14 has no
   selftest case in attest.py`), and do not let the row be counted as discrimination.
4. *Registry churn.* The §2 cell-2 amendments are prose only; they must be re-verified with
   `registry.py --profile v2` after the edit (clauses 2/3/4 read cells 1, 3 and the header).

**Verification for the L1**
- `python3 -I -B tools/round-46/attest.py --root <lane> --freeze 0425224 --rev <tip> --json-out <wave>`
  → exit 0, `rows >= 14`, `failing []`, `refs` unchanged at 9, battery unchanged.
- `python3 -I -B tools/round-46/registry.py --root <lane> --freeze 0425224 --rev <tip>`
  → exit 0 after the four cell-2 amendments (`unregistered []`, `thin []`).
- `git log -1 --format=%H -- tools/round-46/` must still print `0425224…` at the moment of
  scoring; if it has moved, the freeze argument moves with it and F1 recurs.

---

## 6. Receipts

All under `.ufo/waves/round-46/w1/R46W1ConnFleet/`; `stdout` files are the exact command output,
`--json-out` files are byte-identical to them (`gate.emit` prints what it writes).

| Receipt | Exit | stdout sha256 | UTC |
|---|---|---|---|
| `c1-freeze-0425224.{json,stdout}` — `attest.py --root <lane> --freeze 0425224 --rev deee6595 --json-out …` | 0 | `3d028eab71f1d4c363d29ea88dc741a1a5321848691e1bac2864047d7b669b08` | 17:06:49 → 17:06:50 |
| `c2-freeze-0425224.{json,stdout}` — `registry.py` same args | 0 | `e0c457de655942465540e85d010571d26cd30a33008e53e26f800e18f1e58396` | 17:06:50 → 17:06:54 |
| `freeze-3182047-at-head.{json,stdout}` — `attest.py --freeze 3182047 --rev deee6595 --no-battery` | 2 | `3a471c33fde8fc8be01997a6a98e8fa133c0bd296090fb0ece66721b0d09d7e0` | 17:06:54 |
| `gate-selftest.stdout` — `attest.py … --selftest` | 0 | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 17:06:54 → 17:06:57 |
| `registry-selftest.stdout` — `registry.py … --selftest` | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 17:06:57 → 17:06:58 |
| `fidelity-A.stdout` — `--freeze f59565b7 --rev f762b727 --spec r45 --profile v1 --no-battery` | 2 | — | 17:07:16 |
| `fidelity-B.stdout` — `--freeze f762b727 --rev f59565b7` (same spec/profile) | 0 | — | 17:07 |

Read-only Git used: `log`, `show`, `rev-parse`, `merge-base --is-ancestor`, `diff --stat`,
`status --porcelain`, `diff-tree`. No mutation, no stage, no commit, no push. No installs
(nothing needed; `python3`, `git`, `jj` already present — no pacman, `uv`, `npx` or binary
install attempted).

## 7. Not run / limits

- **Not run:** the round-45 fidelity pair in the claims file's own order (A) does not evaluate;
  I did not attempt to reconstruct a control fixture for it beyond the reversed run.
- **Not run:** `.ufo/waves/round-46/controls/` receipts were not re-derived; F1/F4/F5 are
  measured from the instruments and Git, not from comparing against those files.
- **Not verified:** whether the round-44 sweep that touched the lane used `fleet-commit.sh`
  (R45-CL5). The scripts cannot tell me; the report should not claim it.
- **Limit:** HEAD moved twice during the seat. The two claim receipts are bound to `deee6595`;
  a later tip with a frozen-path touch would make both exit 2, and that would be a correct
  answer, not a regression.
- **Calibration of this report:** everything above is a command or a read; the two inferences
  marked as such are (i) the insertion point at `jj-lane.sh:707–712` being viable for an
  operator hook, and (ii) the derivation that `genuine_green` cannot fail once reached. Both are
  labelled where they occur; neither is used to support a claim verdict.
