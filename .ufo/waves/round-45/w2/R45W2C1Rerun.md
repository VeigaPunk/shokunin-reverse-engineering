# R45W2C1Rerun — adversarial falsification of R45-C1 (depth: rule block 22 + its interpreter)

Seat `R45W2C1Rerun`, round 45 wave 2. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`;
A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`; A3 `f59565b782c18b0eb691bec12f52d2f80d9f5032`
(lane HEAD at run time `a63d109faa050207d4c184471889049741c9ebbf`). Read-only on the lane; every
mutation was made on a copy under `/fast/scratch/hyaku/kaidoku-r45/R45W2C1Rerun`. Scratch removed
before yield; receipts copied into this directory.

Scope: the claim's own counting command at three revisions, the A1 amendment's load-bearing status,
and the semantic correspondence between block 22's ten declared exits and the interpreter's actual
behaviour. Not in scope: R45-C2's rows (a sibling seat), and SKILL.md prose outside the craft section.

---

## 1. Verdict summary

| # | Attack | Target | Verdict |
|---|---|---|---|
| A | Reproduce the score at A1 and diff every receipt field | `l1/scores/c1-at-1f4b27f8.json` | **holds** — exit 0, all 15 fields identical |
| B | Same command at the pre-amendment landing `e715263c` | `l1/scores/c1-at-e715263c.json` | **holds** — exit 0, identical; only `block22_refs` moved 6→7 |
| C | Same command at the freeze (do-nothing control) | `controls/ctl-c1-0-do-nothing.json` | **holds red** — exit 1, 5 failing clauses, receipt byte-identical |
| D | Was A1 load-bearing? | A1 `1f4b27f8` vs landing | **split** — load-bearing for command A, **not** for the counter |
| E | Does the `restored`/`commit` arm see a frozen path named only by `--freeze-path`? | block 22 rows 1–2 + the block's "history, not tip equality" prose | **falsified** — exit 0 `clean` where the table declares 1 |
| F | Does every `path:line` reference resolve at `--rev`? | claim clause 4 / `c1-counter.py` `REF` | **falsified as worded** — refs outside `corpus/{knowledge,lessons}/` and `plans/` are never examined |
| G | Can the counter detect a table that contradicts the instrument? | `c1-counter.py` exit-cell clause | **holds as disclosed limit** — it cannot; the limit is stated in block 22 |
| H | The committed freeze control's frozen set | `controls/preflight-at-freeze.json` | **narrower than the claim** — omits `plans/round-45-claims.md` |
| I | The `dirty` row under the default invocation | block 22 row 4 | **exit 0, not 1** unless `--check-dirty` is passed (named only in the receipt cell) |
| J | Independent re-derivations (freeze, counts, citations, sources, selftest) | the rest of the artefact | **hold** |

The counter's score is reproducible and correct **for what it measures**. What it measures is
structural. The artefact the counter certifies — a decision table whose arms are described in
exit-code terms — is contradicted by its own interpreter in the frozen-set shape this round
actually uses. That is finding E.

---

## 2. Receipts

All commands run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` with
`TMPDIR=$S HYAKU_SCRATCH=$S`, `S=/fast/scratch/hyaku/kaidoku-r45/R45W2C1Rerun`.
`sha256` is over captured stdout; UTC is capture time.

| id | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | `python3 -I -B tools/round-45/c1-counter.py --root . --freeze f762b727… --rev 1f4b27f8… --json-out $S/c1-at-A1.json` | 0 | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` | 2026-10-28T15:59:16Z |
| R2 | same, `--rev e715263c…` | 0 | `cb869305df9b64d68e106ce1acfa326dd6d73c8b15f18b07d7546b898c5cc95f` | 2026-10-28T15:59:21Z |
| R3 | same, `--rev f762b727…` (freeze) | 1 | `e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1` | 2026-10-28T15:59:21Z |
| R4 | same, `--rev f59565b7…` (the literal rev in this seat's spec) | 0 | `90597e617067fe4f17399c7e114f36ff5ce7e7da24cb3ce7d06d3b43e57b6f18` | 2026-10-28T16:02:06Z |
| R5 | `python3 -I -B tools/round-45/c1-counter.py --selftest` | 0 | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` | 2026-10-28T15:59:51Z |
| R6 | `bash $S/d-repro.sh` (attack E driver) | 0 (driver); gate 0 then 1 | `546fc57260241d33cadb480483cc2765769e48a4d358b9e24aebfd61b03e0f9b` | 2026-10-28T16:02:38Z |
| R7 | replay of the shipped self-contained driver: `bash d-repro.sh` from this directory | 0 (driver); gate 0 then 1 | `5a9e746df1961e7449a69bf5d2f7e7bf7874301160feb4197ce2eb4e5dfdb0be` | 2026-10-28T16:09Z |

R6 ran the pre-hardening copy of the driver (`sha256 c0b11e76…`), which resolved the interpreter
from scratch. The shipped `d-repro.sh` is self-contained (`sha256 bfc80264a51ae83eea30dda03635e74f01625387260b93e382617f9c3a0dc197`):
it derives the interpreter from its own directory and creates its own scratch, and R7 shows it
reproduces the same two exits with fresh commit ids.

Receipt files in this directory: `c1-at-A1.json`, `c1-A1.stdout`, `c1-at-e715263c.json`,
`c1-e715.stdout`, `c1-at-freeze.json`, `c1-freeze.stdout`, `c1-at-A3-rerun.json`, `c1-A3.stdout`,
`c1-selftest.txt`, `mutants.json`, `d-repro.sh`, `d-repro.out`, `d-repro.err`,
`d-repro-replay.out`, `d-repro-replay.err`, `preflight-at-A1.py` (the interpreter as extracted from
`1f4b27f8`, `sha256 633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` — byte-identical
to the worktree copy and to the A1 blob), `SKILL-at-A1.md` (`sha256 19c20927…`, the bytes every
`git show 1f4b27f8:SKILL.md` citation in this report was read from).

---

## 3. A/B/C/R4 — the score reproduces exactly

Field-by-field comparison, programmatic, all keys:

```
A1        IDENTICAL
e715263c  IDENTICAL
A3        IDENTICAL
freeze rerun vs committed control: IDENTICAL
```

A1 receipt, verbatim (R1):

```json
{"block22_cites": {"S140": true, "interpreter": true}, "block22_header_ok": true,
 "block22_present": 1, "block22_refs": 7, "block22_rows": 10,
 "block22_unresolved_citations": [], "counter": "round-45-c1",
 "failing": [], "freeze": "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
 "frozen_path_changed": [], "interpreter_present": true, "met_target": true,
 "preflight_selftest": {"cases": 11, "exit": 0, "failures": 0, "ok": true},
 "rev": "1f4b27f82353d6544dc0c8048b3cfdadd8525d12", "rule_blocks": 22}
```

At the freeze (R3), exit 1 with exactly five failing clauses — `rule_blocks 21 != 22`,
`block22_present 0 != 1`, `block22_rows 0 < 8`, `block22 table header lacks trigger/arm/exit/receipt`,
`block22_refs 0 < 4` — and `preflight_selftest {"ok": false, "skipped": true}`. Red, and red for the
stated reasons. **Verdict: holds.**

Note on the seat spec: it names `--rev f59565b7…` but compares against
`l1/scores/c1-at-1f4b27f8.json`. Those are different revisions (`f59565b7` is A3, whose recorded refs
are 8; `1f4b27f8` is A1 with 7). Run literally, the only differing fields are `rev` and
`block22_refs` — an artefact of the instruction, not of the landing. Compared against their
matching receipts both are identical. Not a finding against the lane.

---

## 4. D — was A1 load-bearing?

**For the counter: no.** At the landing `e715263c` the counter already returned exit 0,
`met_target true`, `failing []`, `block22_refs 6` (R2), identical to the recorded
`c1-at-e715263c.json`. The frozen predicate's only citation clauses are `block22_refs >= 4` and the
two mandatory cites (`S140`, the interpreter); both held at the landing. Every other field is
equal across `e715263c` and `1f4b27f8`. If the claim's measurement had stopped at the landing, the
counter would have scored it green **and identical apart from `block22_refs 6 vs 7`**.

**For command A: yes, and the record says so.** The depth proxy counts only `corpus/knowledge/`
references (`.ufo/reports/round-45/kaidoku.md`:33, `SCORECARD.md`:3524-3526). Independently
re-derived, block 22 at `e715263c` contains exactly six references and none under
`corpus/knowledge/`:

```
corpus/lessons/round-44.md:18-19
corpus/lessons/round-44.md:63-69
corpus/lessons/round-44.md:88-92
corpus/lessons/round-44-verifier-spotcheck.md:89-92
corpus/lessons/round-45.md:12-17
plans/round-45-claims.md:132-147
```

A1's entire diff is `SKILL.md`, +7/−1, adding one `corpus/knowledge/…:40-66` citation
(`git diff e715263c 1f4b27f8`). So A1 was load-bearing for the **axis proxy**, and the amendment
was honest about that: it changed no predicate and no counter value other than the ref count.
**Verdict: the record's account of A1 is accurate.**

One calibration consequence worth routing: the frozen predicate cannot see what A1 fixed. A round
could land a depth block with zero `corpus/knowledge/` citations, score `met_target true`, and
harm the axis. The claim's kill rule has no clause for it. That is a claim-design gap (the counter
measures the surface; command A measures the axis), not a defect in this landing.

---

## 5. E — **FALSIFIED**: the history arm is scoped by `--pathspec`, so a restored frozen path outside it reads `clean`

### What the artefact claims

Block 22, rows 1–2:

```
| any commit in FREEZE..REV touches a frozen path | commit (git log --name-status, S141) | 1 | `touched[]`, … |
| a frozen path was touched and later restored to its FREEZE bytes | restored (commit history, never tip equality) | 1 | `restored[]`, disjoint from `blob_changed[]` |
```

and the prose: "History, not tip equality, is the evidence: a path that was edited post-freeze and
then restored to its exact bytes is still a violation (`corpus/lessons/round-44.md:88-92`,
`corpus/lessons/round-44-verifier-spotcheck.md:89-92`), which is why the `restored` list is reported
separately from `blob_changed` instead of collapsing into it."

The trigger says **a frozen path**. This round's frozen set is two paths
(`plans/round-45-claims.md:132-147`): the claims file and the `tools/round-45/` directory.

### What the interpreter does

`evaluate()` builds the history scope from the pathspecs only:

```python
scope = ["--"] + pathspecs if pathspecs else []
log = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status",
          "--format=%x00%H", f"{base}..{tip}", *scope)
```

`restored` is then derived from `touched` (`elif any(t["path"] == path for t in touched)`), so a
path that `git log` was never asked about can never be classified as restored. The frozen set built
for the blob arms *does* include directly-named `--freeze-path` entries (`frozen.add(fp)`), which is
why a net modification is still caught — and precisely why a tamper-then-restore is not.

### Exact input and result (R6)

Fixture shaped exactly like this round's frozen set, with the documented invocation — `--pathspec
tools/round-45/` and `--freeze-path tools/round-45 --freeze-path plans/round-45-claims.md`:

```
fixture=…/d-fixture.9Perku freeze=c725550b7e10eda2b0459f2eed3ae02cc7fa49d1 rev=c815feed03542b81f504d8bd349a040c90d2abe8
claims_blob_at_both=993e6249f25877b8fc1928dd555149eabd1587e8     # tip blob == freeze blob
counter's own arm (unscoped): plans/round-45-claims.md ×2         # history does contain the touch
gate  --pathspec tools/round-45/ only:
  {"restored": [], "touched": [], "verdict": "clean", …}   GATE_EXIT=0
gate  --pathspec plans/round-45-claims.md added:
  {"restored": ["plans/round-45-claims.md"], "touched": [2 records], "verdict": "frozen_path_changed"}   GATE_EXIT_BOTH=1
```

Same fixture, same freeze, same rev, same frozen set. The **only** difference is whether the claims
file appears in `--pathspec`. Declared exit for this trigger: **1**. Observed: **0 `clean`**.

This is the round-44 M44-2/R44-CL10 failure class — the exact thing the round claims to close —
re-entering through the pathspec boundary rather than through tip equality. The w1 seat
`R45W1PreflightArms` §1.4 concluded `restored` "cannot change the exit code" because
`restored ≠ [] ⟹ touched ≠ []`; that implication holds only for paths inside the pathspec, and the
frozen set this round uses has one path outside it. The w1 conclusion is therefore too strong.

### Why the counter cannot catch it

The counter runs the preflight only as `--selftest` (R5: 9/9 green, `PREFLIGHT_SELFTEST: cases=11
failures=0`). No selftest case names a `--freeze-path` file outside `--pathspec` — the `restored`
case uses `--pathspec frozen/` covering `frozen`. So a gate that cannot classify a restored
claims-file reports `preflight_selftest.ok = true` and the counter issues `met_target true`.

Independent confirmation that the counter's *own* arm is not affected: `frozen_path_changed()` in
`c1-counter.py` runs `git log --name-only … -- plans/round-45-claims.md tools/round-45` **unscoped**,
and on the same fixture it lists the claims file twice. The counter and the gate disagree; the
counter is the correct one.

### Fix

Union the directly-named, non-directory freeze paths into the history scope:

```python
direct = [fp for fp in freeze_paths if not tree_at(root, base, fp)]
scope = ["--"] + pathspecs + direct if (pathspecs or direct) else []
```

and add a red case `red-restored-outside-pathspec`: freeze a directory and a file, pass only the
directory as `--pathspec`, tamper then restore the file, expect 1.

This fix edits `tools/round-45/`, a frozen path, so it cannot be applied in place: doing so makes
both counters exit 2 `frozen_path_changed` and voids the score. The honest routes are (a) record the
defect now and repair under a new freeze next round, or (b) re-freeze and re-measure this round with
the corrected interpreter. Do not patch it and keep citing `f762b727`.

**Severity: high.** The defect is in the artefact the axis claims, in the one configuration the
round's own frozen set creates, on the one signal block 22 names as the reason the arm exists.

---

## 6. F — **FALSIFIED as worded**: clause 4 says every `path:line` reference resolves

The claim states: "`block22_unresolved_citations == []` — every `path:line` or `path:first-last`
reference resolves at `--rev`". The implementation's grammar is narrower:

```python
REF = re.compile(r"((?:corpus/(?:knowledge|lessons)|plans)/[A-Za-z0-9._-]+\.md)(?::(\d+)(?:-(\d+))?)?")
```

Mutants on a copy of the A1 tree (`mutants.json`), field-diffed against R1:

| mutant | input | exit | `block22_refs` | `block22_unresolved_citations` |
|---|---|---|---|---|
| baseline copy | unchanged A1 artefacts | 0 | 7 | `[]` |
| M-B | add `` `LOG.md:99999` `` and `` `SKILL.md:88888` `` to block 22 | **0** | **7** (unchanged) | **`[]`** |
| M-C (control) | add `` `corpus/lessons/round-45.md:9999` `` | 1 | 8 | `['corpus/lessons/round-45.md:9999-9999']` |

M-C proves the regex is the gate and the fixture is sound; M-B proves two impossible references are
invisible. No live violation exists — block 22's six/seven/eight references are all in
`corpus/lessons/`, `corpus/knowledge/` and `plans/`, and all resolve at their revisions. So this is a
**wall between the claim and the instrument**, not a false citation: the claim's phrasing promises
more than the counter checks, and a future block could cite `LOG.md:9999` and still score 0.

Fix (either): widen `REF` to any `[\w./-]+\.md(?::\d+(-\d+)?)?`, or narrow the claim wording to "every
reference under `corpus/{knowledge,lessons}/` or `plans/`".

Related, low: a bare path with no line (`plans/round-45-claims.md`) matches with `first = None`,
`end = 1`, and resolves as long as the file exists. That is why A3 reads `block22_refs 8` rather than
7 against A1 — the eighth "citation" carries no location. Harmless, but it inflates the ref count.

---

## 7. G — the counter cannot detect a table that contradicts the instrument (disclosed)

Mutant M-A: block 22 row 2's exit cell changed from `1` to `0` — the table now says a restored frozen
path is clean, contradicting the interpreter.

```
M-A restored_row_exit_1_to_0   exit 0   refs 7   unresolved []   met True   failing []
```

The exit-cell clause accepts any member of `{0,1,2}`, so the lie is indistinguishable from the truth.
This is **disclosed** in block 22 itself: "this instrument's 'actionable table' test is structural
(header cells, row count, exit cells, resolving citations), and a table of structurally valid but
empty rows would pass it." Verdict: holds as a disclosed limit. It is recorded here because it is
the mechanism through which finding E survives a green score — the counter never compares a declared
exit to an observed one, and no seat in wave 1 did either.

If the round wants the table to be evidence rather than annotation, the counter must execute each
row's trigger and compare to the declared exit. That is a larger instrument than this claim froze.

---

## 8. H — the committed freeze control is narrower than the claim's frozen set

`controls/preflight-at-freeze.json`:

```json
"freeze_paths": ["tools/round-45"], "pathspec": ["tools/round-45/"], "verdict": "clean"
```

The claims file declares **two** frozen paths (`plans/round-45-claims.md:132-147`). The frozen
control that is supposed to show the gate clean at the freeze exercised one of them and never named
the claims file at all. The L1's later `l1/preflight-round45-frozen-both.json` does pass both
(`pathspec: ["tools/round-45/", "plans/round-45-claims.md"]`) and is clean, so the *conclusion*
survives — but the committed control receipt under `controls/` is not the receipt its filename
implies. Route: either regenerate the control with both paths, or rename it to state it covers the
directory only. Low-to-medium: a control that omits half the frozen set cannot falsify anything about
that half.

---

## 9. I — row 4's declared exit depends on a flag named only in the receipt cell

Row 4 declares: worktree dirty under the frozen pathspec → exit `1`. Observed (T2, same fixture):

```
dirty, no --check-dirty : exit 0  {"dirty": [], "verdict": "clean"}
dirty, --check-dirty    : exit 1  {"dirty": [" M frozen/b.txt"], "verdict": "frozen_path_changed"}
```

The receipt cell does name `--check-dirty`, and the prose calls it "the arm that matters most". But
block 22 also instructs "Read the table as an ordered decision list: the first row whose trigger
holds decides", and under that reading with the default invocation row 4's trigger holds and the
answer is `0`, not `1`. The table never states the invocation its exit column assumes. Verdict:
row content holds, the decision-list framing is under-specified. Fix: one line above the table
stating that rows 1–8 assume `--check-dirty --require-pathspec` with every frozen path covered.

Low, same family: for a directory freeze, `blob_changed[]` contains the directory itself beside its
files (`["tools/x", "tools/x/a.py"]`) — `rev-parse` returns a tree id, not a blob, so row 3's wording
"a frozen path's blob" is loose and its receipt list mixes kinds.

---

## 10. J — what independently re-derives and holds

| check | command | result |
|---|---|---|
| freeze is the first commit containing the claims file | `git log --format=%H -1 -- plans/round-45-claims.md` | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` |
| freeze is the first commit containing the directory | `git log --format=%H -1 -- tools/round-45/` | `f762b727…` (same) |
| `FREEZE..A1` touches no frozen path | `git log --name-only --format= f762b727..1f4b27f` | `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`, `.ufo/…` only → `frozen_path_changed []` is correct |
| craft-section block count | `awk` over `## Queue-drain craft` at A1 | `blocks=22` |
| marker appears once | `grep -c 'freeze-integrity-table v1'` | `1` |
| table rows and exit cells | read of block 22 | 10 rows, exits `1,1,1,1,2,1,2,2,0,0` — all in `{0,1,2}` |
| header carries all four columns | receipt | `block22_header_ok true` |
| `plans/round-45-claims.md:132-147` resolves | `git show A1:plans/round-45-claims.md \| wc -l` | `175` lines — resolves with margin |
| S140/S141 are real source rows | `git show A1:corpus/SOURCES.md \| grep '^\| *S14[01]'` | rows at lines 146–147, git-status and git-diff-tree |
| counter's own selftest | R5 | 9 cases, 0 failures — matches the registry row's "9 cases" |
| interpreter selftest from the bytes at `--rev` | inside R1 | `cases 11, failures 0, exit 0` — revision-bound, a real strength |

Calibration note on row count: the predicate is `block22_rows >= 8`. Eight of the ten rows are
trigger rows; rows 9 and 10 are catch-all terminals (`clean`, `FREEZE == REV`). If "rule rows" means
trigger rows the margin is exactly zero. The threshold is met either way; the report's "10 rows"
overstates distinct decision content by two.

---

## 11. Residual risk and verification gaps

1. **E's blast radius is bounded by invocation discipline.** The L1's own
   `preflight-round45-frozen-both.json` and `preflight-at-A2-both.json` pass the claims file as a
   second `--pathspec`, so no scored run is currently wrong. The defect is in the documented
   interface (the claims file states `--pathspec tools/round-45/`; the table states no invocation)
   and in the malformed freeze control (§8). A future seat following the documentation inherits it.
2. **No wave-1 seat executed a declared-exit comparison.** Every w1 seat verified the table's
   *structure* and the selftest's *cases*; none mapped row → observed exit. That is the hole through
   which E and I both pass, and it is the single highest-value change to wave-3 design.
3. **Not verified:** whether the preflight behaves correctly on a merge-shaped range beyond the two
   shapes the selftest covers (the `-m --diff-merges=first-parent` flags are exercised only by the
   bulk-sweep case); whether `restored` can ever be non-empty *and* `blob_changed` non-empty for the
   same path (the code makes them mutually exclusive by construction — the table's "disjoint" wording
   is a property of the `elif`, not a tested invariant). Not run: no fixture was built for either,
   because neither changes the verdicts above.
4. **Command A was read from the record, not executed.** No implementation of the depth proxy exists
   in the fleet tree (`grep -rl citation_resolved_rules` returns only reports, lessons and two
   evidence JSONs), so §4's command-A claim rests on the recorded values
   (`.ufo/reports/round-45/kaidoku.md`:33,133) plus my independent derivation that block 22 at
   `e715263c` has zero `corpus/knowledge/` references and A1 adds exactly one. The derivation is
   sufficient for the load-bearing question; it is not a reproduction of the proxy.
5. **No install was performed**; `pacman` untouched. Tooling used: `git`, `python3`, `awk`, `grep`,
   `sha256sum` — all preinstalled.

---

## 12. Disposition

| finding | route |
|---|---|
| E — restored/commit arm blind outside `--pathspec` (high) | open; fix per §5 under a new freeze, or re-freeze and re-measure this round. Do not cite `f762b727` for a patched interpreter |
| H — freeze control omits the claims file (medium) | open; regenerate or rename the control receipt |
| F — clause 4 wording wider than `REF` (medium) | open; widen the regex or narrow the claim |
| I — row 4 depends on `--check-dirty` (medium) | open; one invocation line above the table |
| G — counter blind to a lying table (low, disclosed) | record only; it is stated in block 22 |
| A1 not load-bearing for the counter (note) | record only; the amendment is honest and the axis proxy needed it |
| row-count margin, bare-path refs, directory in `blob_changed` (low) | record only |

The counter's **score holds**: exit 0 at A1 and A3, exit 1 at the freeze, every field identical to
the record, red for the stated reasons. The **artefact's central claim is falsified**: the `restored`
arm does not detect a restored frozen path outside the pathspec, which is the shape this round's own
frozen set creates, and block 22 declares exit 1 for it.
