# EX-27 — regression: round-3's full battery re-run against the revised tool

Seat EX-27 · chain c3 · role executor · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

**Verdict: DELIVERED — every prior class holds.** The round-4 battery (75 rows,
legs A–J) reads **75 HOLD / 0 FAIL / 0 unmeasured** on the settled revised tool
`29bb45ae`, and **70 HOLD / 0 FAIL** on the round-3 landed tool `7cd19c3c`; all
four round-3 injections reproduce as their declared classes and now measure
CLOSED. One residual outside the four named injections is named (§4, P5), with
its class measured at *both* revisions so it is not mistaken for a regression.

Scratch `/var/tmp/ex27r4` (never `/tmp`). Custody paths read-only (hash/stat
only; the tool's own receipts went to scratch). No git mutation. Nothing written
outside this seat's artifact dir and `seats/EX-27.md`.

## 1. Work performed (evidence pointers)

Artifacts live under `.ufo/waves/arc3-loop1-round4/claims/c3/EX-27/`
(`$W` below). Every number in this file was re-derived by this seat against the
bytes it names; no other seat's report was used as evidence without a first-hand
re-derivation.

| # | work | evidence |
|---|---|---|
| 1 | Read the frozen claims, roster and lane note; read the round-3 patch texts the (a)–(d) closures derive from (EX-24 coverage-count, CR-4 write-guard, CR-3 typeswap §3, RV-8 corrections) | `claims-frozen.md`; round-3 `claims/c2/{EX-24,CR-4,CR-3,RV-8}/` |
| 2 | Built a **new** round-4 battery (`harness/regress-r4.py`, legs A–J, 75 rows) by porting round-3's c2/EX-27 harness and extending it | `$W/harness/regress-r4.py` sha256 `3d5b2132…` |
| 3 | Baseline phase against the **round-3 landed** bytes, pinned copy extracted read-only | `$W/tools/tool-r3-landed-7cd19c3c.py` sha256 `7cd19c3c…`; `$W/runs/regress-r3-baseline-7cd19c3c.{txt,json}` |
| 4 | Churn watched, not guessed: 60 s poll for EX-21's revision, then a **5×20 s sha-stability gate** before any after-measurement | `$W/runs/poll.log`; `$W/runs/churn-settle-tool.log` (`SETTLED sha=29bb45ae… after 5 identical samples`); `churn-settle-readme.log` |
| 5 | After phase against the settled revision, twice (preliminary + final); row sets byte-identical | `$W/runs/regress-r4-29bb45ae.txt`, `regress-r4-final-29bb45ae.txt` (`diff` → identical rows) |
| 6 | Harness self-test **before** the real bytes landed: a scratch-only simulated revision built from the patch texts' shapes, to prove the r4 expectations and sabotage arms were not themselves the bug | `$W/harness/sim-r4-revision.py`; `/var/tmp/ex27r4/sim-r4/` |
| 7 | **Adversarial** sidecar probes (8) aimed at *defeating* the new (a) guard, run on both revisions | `$W/harness/adversarial-sidecar.py`; `$W/runs/adversarial-sidecar-{r3,r4}.txt` |
| 8 | Before→after table generated from the two JSON runs (not hand-typed) | `$W/harness/make-table.py`; `$W/runs/before-after-table.md` |
| 9 | No-harm instruments re-run first-hand: command A, citation-drift probe, README exit-map consistency | §3, §5 |
| 10 | EX-21's published identities **re-derived, not trusted** (rule #14) | §5 |

## 2. Proposed changes

**none.** This seat is a measurement seat: it writes no tool code, no README, no
patch text, and no real target. The only files it created are its own artifact
tree and its seat report.

Advisory for the parent (both are *named residuals*, not blockers):

1. The alias-spelling residual in §4 P5 is real and unfixed at `29bb45ae`. It is
   outside the four injections C3 froze, so it does not falsify the claim; if the
   parent wants it closed, the fix is small and is stated in §4.
2. `(d)`'s detector is a line-regex (`both.sides` / `EXISTS: no` / error-carrying
   wording). It reads 10 hits now, so the ruling text is present — but a detector
   of that shape can be satisfied by incidental prose. EX-21's own report names
   this limit (its attack 13) and I reproduce it: non-vacuity for (d) rests on the
   tool-side rows (`G/d`, `G/d2`, `H/sabotage-unevaluable-arm-removed`), not on
   the detector alone.

## 3. Before → after measurement (the chain claim's regression arm)

Commands (exact; re-runnable, ~5 s/phase):

```bash
python3 .ufo/waves/arc3-loop1-round4/claims/c3/EX-27/harness/regress-r4.py \
  --phase r3 --tag r3-baseline-7cd19c3c \
  --tool-src $W/tools/tool-r3-landed-7cd19c3c.py \
  --baseline-src .ufo/waves/arc3-loop1-round3/claims/c2/EX-27/tools/tool-base-112d01dc.py

python3 .ufo/waves/arc3-loop1-round4/claims/c3/EX-27/harness/regress-r4.py \
  --phase r4 --tag r4-final-29bb45ae \
  --tool-src $W/tools/tool-r4-29bb45ae.py \
  --baseline-src $W/tools/tool-r3-landed-7cd19c3c.py
```

| leg | rows | what it covers | before (`7cd19c3c`) | after (`29bb45ae`) |
|---|---|---|---|---|
| A | 18 | the 13 CR-4 `battery.py` rewrite forms + 5 same-content/fencing forms | 18/18 HOLD | **18/18 HOLD, identical classes** |
| B | 17 | round-1 canonical stanza / cross-format / pipe / sums, the EX-35 fixture set, synthetic v1 anchors, junk | 17/17 HOLD | **17/17 HOLD** |
| C | 3 | v1 label defect declared; v2 UTC render correct + TZ-invariant | 3/3 HOLD | **3/3 HOLD** |
| D | 3 | selftest count; **prior case names retained**; missing-scratch class | 22 cases, all 22 names | **28 cases, all 22 prior names retained** |
| E | 4 | D2 EACCES capture/verify, fail-open both-absent, `--paths X --out X` | 4/4 HOLD | **4/4 HOLD** |
| F | 3 | live pair (real paths, read-only) + scratch-pair form + receipt self-pin | `MATCH 5/5 exit 0` | **`MATCH 5/5 exit 0`**, self-pin = tool bytes |
| G | 10 | **the four round-3 injections**, independently probed | 4 OPEN / 6 HOLD | **10/10 CLOSED+HOLD** |
| I | 7 | CLI-level equivalents of the reachable selftest cases | 7/7 HOLD | **7/7 HOLD** |
| J | 3 | README exit map covers every `EXIT_*`; case-count sentence | 3/3 HOLD | **3/3 HOLD** |
| H | 7 | non-vacuity: baseline-RED + 4 sabotage arms | 3/3 HOLD | **7/7 HOLD, all 4 arms RED** |
| **total** | **75** | | **70 HOLD / 0 FAIL** | **75 HOLD / 0 FAIL / 0 obs** |

### The four injections (leg G), measured

| injection | probe | before | after |
|---|---|---|---|
| (a) sidecar path not scope-checked | `capture --out vic --paths vic.sha256` | **exit 0**, `vic.sha256` bytes destroyed | **exit 2**, file intact |
| (a2) same via inode alias | `--out` fresh; sidecar path hardlinked to the measured file | **exit 0**, measured file destroyed | **exit 2**, intact |
| (b) `out.parent.mkdir` outside the guarded try | `capture --out <regular-file>/sub/r.txt` | **traceback, exit 1** | **`USAGE` exit 2**, no traceback |
| (b2) `--out ''` (CR-4 item 6's trap) | `capture --out '' --paths X` | USAGE exit 2 | **USAGE exit 2** (no regression) |
| (c) coverage gate counts stanzas | 5× duplicate stanza for one path, `--require-paths 5` | **exit 0, silently**, no coverage line | **exit 2** + `REFERENCE-COVERAGE: 1/5 …` |
| (c2) control: 5 distinct paths | same gate, 5 real paths | exit 0 `MATCH 5/5` | **exit 0 `MATCH 5/5`** |
| (d) both-absent semantics | plain both-absent vs error-carrying both-absent | `MATCH 0` / `UNEVALUABLE 14` | **`MATCH 0` / `UNEVALUABLE 14`** (unchanged, as ruled) |
| (d3) ruling text in the README | `readme_ruling()` detector | **0 hits** | **10 hits** |

### Selftest: count and names

```
before: CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0
after : CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0
```

All 22 round-3 case names are still present at `29bb45ae`
(`prior_names_missing=[]`), so the +6 cases are additions, not renames that
would have masked a lost class. The six new names are
`coverage-gate-rejects-duplicate-stanzas`, `coverage-gate-passes-distinct-five`,
`refuses-sidecar-over-measured-file`, `refuses-receipt-over-sidecar-neighbour`,
`out-parent-not-a-directory-usage-exit`, `both-sides-absent-is-agreement-match`.

### No-harm instruments

| instrument | result at the settled tree |
|---|---|
| command A (verbatim SCORECARD recipe) at `015e1ba` | `knowledge_files 83, mapped 83, missing [], dangling [], citation_resolved_rules 14/14, coverage 10.0, depth 10.0` — **unchanged** |
| citation-drift probe | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` |
| README exit map vs tool constants | all 8 declared `EXIT_*` values present as rows, incl. 14 |
| live receipt pair, revised tool | `VERDICT: MATCH paths=5 exit=0`, both receipts self-pin `29bb45ae` |

## 4. Attacks / refutations attempted, with verdicts

1. **"The revision regressed a rewrite-form detection."** **REFUTED** — 18/18
   forms produce identical verdicts and exits; the sha-only blindness pattern is
   identical (8 same-content forms still move only inode/ctime/mtime).
2. **"The +6 selftest cases are renames that hide a lost class."** **REFUTED** —
   name retention is its own row (`D/selftest-prior-case-names-retained`), and it
   reads `prior_names_missing=[]` against the 22 names captured from the landed
   round-3 tool's own output (not typed from memory — see attack 9).
3. **"The r4 expectations are my own invention, so HOLD is circular."**
   **REFUTED** — the expectations were exercised *before* the real bytes landed
   against a scratch-only simulated revision built from the patch texts' shapes;
   the sim correctly showed the four not-yet-revised surfaces as FAIL
   (README ruling, case count, case-count sentence, `--out ''`), proving the
   checks discriminate rather than pass by construction.
4. **"The injection checks are vacuous (they would read CLOSED on any tool)."**
   **REFUTED** — three of them go RED on the pre-revision bytes
   (`H/nonvacuity-baseline-*`), and four **byte-sabotage** arms of the revision
   under test each turn their check RED (`H/sabotage-*`, all `check_goes_red=True`).
5. **"A sabotage arm 'passed' because it produced a broken copy."** **CONFIRMED
   as a harness defect, then fixed.** The first arm reverted `candidate_paths`
   to a bare `(out,)`, which broke the tool's own parsing (SyntaxError) rather
   than removing the sidecar arm — and a SyntaxError proves nothing. Sabotage
   copies are now compile-checked; an uncompilable copy is an **observed-only**
   row (never a pass), and each arm declares a family of candidate spellings
   because the guard's exact wording is EX-21's choice. After the fix all four
   arms apply cleanly and go RED.
6. **"The neighbour arm can be evaded."** **CONFIRMED — real, and named.** See
   P5 below. Class measured at **both** revisions, so it is a persisting
   residual of the arm's construction, not a regression introduced here. A
   one-line fix was built on scratch and **verified to close it while keeping
   75/75** (`6bf564a5…`); it is not applied to the real target.
7. **"A refusal-flavoured exit code could hide a completed destructive write"**
   (CR-4 item 7's ordering concern). **NOT FOUND at the probes I ran** — in every
   refused probe the measured/neighbour file's bytes were byte-identical before
   and after, and `a3-control` confirms an ordinary capture still writes receipt
   + sidecar.
8. **"`--require-paths` broke the declared v1 default."** **REFUTED** — a 1-of-5
   reference with no flag still reads `exit 0`; the gate is opt-in, and with the
   flag it is `exit 2` + the coverage line. Both profiles assert this.
9. **"My first baseline was green by luck / by a mis-transcribed expectation."**
   **CONFIRMED as a harness bug, then fixed.** The first baseline run reported a
   FAIL on `a2-sidecar-hardlink-alias` and listed 18 "missing" case names: the
   case-name list had been typed from memory instead of captured from the tool's
   own output, and the a2 fixture was self-defeating (`--out` itself was the
   hardlink, so the *pre-existing* `--out` guard refused and the probe measured
   nothing). Both are recorded because a mis-run check has not passed. The
   case-name list now comes from the landed tool's transcript, and a2's `--out`
   is a fresh file with only the derived sidecar hardlinked — which reproduces
   the real residual on the pre-revision bytes.
10. **"The revision changed the v1 compatibility contract."** **REFUTED** — the
    canonical stanza still reads `CONTENT-DRIFT 10` with 4 `LABEL-DEFECT`
    (drift-derived: one live `config.toml` content drift + four v1 label
    defects), sums/pipe/compact/no-time shapes unchanged, junk still USAGE 2.
11. **"A mid-run tool change made the after-column meaningless."** **HELD** —
    the harness aborts on any sha movement and the pin was gated on 5×20 s
    stability; the live path and the copy under test were equal at run time and
    at write time. The preliminary and final runs produced identical rows.
12. **"The after-column is stale because EX-21 kept editing."** **REFUTED at
    write time** — the tool is still `29bb45ae` (65,902 B) and the README
    `9d9400da` (15,293 B); both re-derived after the last measurement.

### P5 — the named residual (alias spellings evade the neighbour arm)

**Mechanism.** The guard's neighbour set is built by appending `".sha256"` to the
**spelled** measured path:

```python
neighbours = {Path(str(g) + ".sha256").resolve() for g in guarded}
```

where `g` iterates the `--paths` spellings. When the measured file is spelled
through a symlink or hardlink alias, `str(g) + ".sha256"` names a *different*
file than the real neighbour of the measured inode, so the refusal misses.

**Measured** (`$W/runs/adversarial-sidecar-r4.txt`, probe P5):

```
fixture: real/vic (measured via alias) ; real/vic.sha256 = PRE-EXISTING CONTENT
$ capture --out real/vic.sha256 --paths <alias>/vic
exit=0   →   real/vic.sha256 replaced by the receipt (bytes destroyed)
```

**Class.** The **same probe fails identically on the round-3 bytes** (exit 0,
clobber), and the round-3 tool clobbered *four* fixtures where the revised tool
clobbers one — so the revision strictly reduced the surface; this is a
**persisting residual**, not a regression. It is outside the four injections C3
froze (the frozen (a) is the sidecar *path* of a measured file, which is closed),
so it does not falsify the chain claim.

**Scope.** It requires the caller to (i) spell the measured path through an alias
and (ii) aim `--out` at a pre-existing neighbour file of the *resolved* path.
Under the declared threat model this is a self-harm guard, not a security
boundary; the same sentence the docstring already carries for TOCTOU applies.

**Fix if the parent wants it closed** (one line, in the neighbour comprehension):
resolve before appending —

```python
neighbours = {Path(str(g.resolve()) + ".sha256") for g in guarded}
```

**Fix verified, not asserted.** I built the patched copy on scratch
(`harness/p5-fix-candidate.py`, sha256 `6bf564a5…`; the real target untouched)
and re-ran everything against it:

| check | `29bb45ae` (landed) | `6bf564a5` (fix candidate) |
|---|---|---|
| P5 alias-spelling probe | exit 0, neighbour **destroyed** | **exit 2, neighbour intact** |
| adversarial set | 7 hold / 0 fail / 1 obs, **1 clobbered** | 7 hold / 0 fail / 1 obs, **0 clobbered** |
| full 75-row battery | 75 HOLD | **75 HOLD** (no row regressed) |
| ordinary capture control | HOLD | **HOLD** |

So the residual is closable with a one-line change that costs nothing else. I
did **not** apply it: the real target is EX-21's write target, and C3's frozen
(a) is already closed as specified — landing this is the parent's call.
Evidence: `runs/adversarial-sidecar-r4-p5fix-candidate.txt`,
`runs/regress-r4-p5fix-candidate.txt`.

### Adversarial probe summary

| probe | before (`7cd19c3c`) | after (`29bb45ae`) |
|---|---|---|
| P1 direct sidecar | FAIL exit 0 + clobber | **HOLD exit 2, intact** |
| P2 neighbour sidecar | FAIL exit 0 | **HOLD exit 2, intact** |
| P3 hardlink-alias sidecar | FAIL exit 0 + clobber | **HOLD exit 2, intact** |
| P4 symlinked-dir spelling | FAIL exit 0 + clobber | **HOLD exit 2, intact** |
| P5 symlink-alias measured path | **obs** exit 0 + clobber | **obs** exit 0 + clobber (unchanged class) |
| P6 relative spelling | FAIL exit 0 | **HOLD exit 2, intact** |
| P7 double extension | HOLD (no harm by construction) | **HOLD** |
| P8 control: legitimate capture | HOLD | **HOLD** |
| | 2 hold / 5 fail / 1 obs | **7 hold / 0 fail / 1 obs** |

### Cross-check by another seat (independent reproduction)

EX-21 ran this harness against its own landed bytes during the wave
(`claims/c3/EX-21/matrix/regression-r4-battery-landed.txt`): header pins
`tool=29bb45ae…`, `baseline=None`, tally **`rows=73 hold=72 fail=0 observed-only=1`**
at 14:10:07Z. That is an independent run of my harness by a different seat and it
agrees with my after-column: no FAIL, and the one observed-only row is
`H/nonvacuity-baseline` (the pre-revision control, absent because that run passed
no `--baseline-src` — by construction).

**Row-count reconciliation.** EX-21's report cites "73 rows" because it ran the
harness before I extended it. Between that run and my final one I added two
EX-35 fixture rows (empty, comment-only) and split the single selftest row into
`selftest-case-count` + `selftest-prior-case-names-retained`, taking the battery
from 73 to 75 rows. My final numbers are the 75-row ones; the 73-row run's
72/0/1 is a subset that agrees row-for-row.

## 5. Blockers

**None blocking.** Every leg of this seat's task is measured and green at the
pinned revision.

Named caveats:

- **P5** (§4) is unfixed at `29bb45ae`; classified as a persisting residual with
  the class measured at both revisions. Outside the frozen claim's four
  injections. A one-line fix is stated **and verified on scratch**
  (`6bf564a5…`: closes P5, 75/75 still green) — landing it is the parent's call.
- **Identity discipline.** This file's after-column binds tool `29bb45ae` and
  README `9d9400da`, both re-derived at write time; if either moves before the
  parent's commit, re-run the battery (~5 s/phase) before citing the after-column.
  EX-21's report claims exactly these two digests and I re-derived both — the
  tool from the live path and from my own pinned copy, the README from the live
  path.
- **Drift-derived expectations.** The live `~/.kimi-code/config.toml`
  (`bc66d543…`) differs from the round-1 receipt, so v1 rows carry drift-derived
  expectations recomputed at run time rather than fixed counts. If the operator's
  config moves again, the expectations follow automatically; the rows would only
  redden if the *tool*'s behaviour changed.
- **Leg J's case-count row** is a regex over the README sentence; it is a
  documentation-consistency check, not a behavioural one, and is reported as
  such.
