# R44W2Quality77 — is the new QUALITY row a criterion or a restatement?

Seat `R44W2Quality77`, wave 2 of kaidoku round 44. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Target: the round-44 correction
appended to `corpus/QUALITY.md` at line 139 (the file's only new row), which the round's
own record tags **QUALITY 77**.

Revisions used: freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; violating commit
`c86ea508188c50e2645b1f9bba65df4177cda6b1`; lane tip at this seat's dispatch
`8bb1090af3fef64477c4337855e4347472db2701`. Topology checked: freeze →
… → `55bcce69` → `c86ea508` → `8bb1090a` (`git merge-base --is-ancestor`, exit 0 each
step). I changed no claim, counter, rubric, frozen byte or production doc; everything
below is read-only git plus scratch fixtures under
`/fast/scratch/hyaku/kaidoku-r44/R44W2Quality77/`, deleted before yield.

## Verdict

**Rewrite, and split the row's second half out.** Renumber: the lane already has a live
row 77, so the new row must be **86**, and its prose/instrument clause must become
**87**.

- The row is **a criterion with a demonstrated failing case**, not a restatement in the
  narrow sense: I reproduced the red arm at `c86ea508` (exit 1, 8 `M` paths under the
  frozen directory) and the green arm at `55bcce69` (exit 0), and fresh runs parse equal to
  both committed receipts. It catches the exact M44-2 defect.
- But its *check* is row 79's check (`tools/round-38/freeze-drift.py` over the claim's
  kill-rule paths, before a score is cited) re-issued under a second tool, and its one
  genuinely new clause — "before treating a commit as landed" — is **not demonstrated by
  anything it cites**: the tool takes `--rev` only, so it cannot run before a commit
  exists; both receipts are post-commit detections.
- It states what is gated only in outline (no walk shape, no pathspec-set requirement, no
  exit-2 semantics), states **nothing** about what a green run does not prove, and its
  evidence pointer reproduces but fails row 73 (no argv, no tool digest, no UTC instant)
  and row 61 (no isolated green/red fixtures, no self-invocation cases).
- Its second half is a **different failure class with a different instrument**, has no
  arm, and is provably invisible to the gate it is attached to.

## 1. Does it have a demonstrated failing case? (Yes)

```
python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev <REV> --pathspec tools/round-44
```

| rev | exit | stdout sha256 | touched / blob_changed | committed receipt |
|---|---|---|---|---|
| `c86ea508` | **1** | `20a87d4d81eedaa79defea6c0fcbbe248bd415e35460b48dd6b66fffe0a28896` | 8 / 8 | `.ufo/waves/round-44/l1/preflight-c86ea508.json` (sha256 `dff05409…eb6b`), parsed equal |
| `55bcce69` | **0** | `c8a03c2673a9bfd52b23077a604e48288e44c70ff5cedd5782bc4fa6430a870f` | 0 / 0 | `.ufo/waves/round-44/l1/preflight-55bcce69.json` (sha256 `c2cab50a…5ee4`), parsed equal |
| `8bb1090a` (tip) | **1** | `c302813c8069f581e4674d3f5335f9a8f4db903015df772eaa509ee08a1cdf99` | 8 / 8 | **none committed** |

Tool sha256 `a2ea675d0d89b462693e97d853d1c1af3122913ba2d0026105044421c9a0e174`
(`tools/round-45/frozen-path-preflight.py`, 107 lines). The red arm is exactly M44-2:
8 `M` paths under `tools/round-44/control-fixtures/`, the same 8 paths as the counters'
`frozen_path_changed`. So the answer to "does the preflight really catch it" is **yes**,
and it catches more than the arm shows: on an isolated fixture it also reds on `A` under a
frozen directory, on `D`, and on modify-then-restore-to-freeze-bytes (evidence:
`artifacts/R44W2Quality77/arms/01,03,04`), and with no `--pathspec` it is fail-closed
(`arms/05`, exit 1).

## 2. Is it a restatement of the freeze rule? (Mostly yes)

The frozen claim already states the rule (`plans/round-44-claims.md:77-83`), row 55
already requires the frozen input checked at the measured revision, and row 79 already
prescribes the same predicate *before a score is cited*:
`tools/round-38/freeze-drift.py --freeze <first freeze> --rev <measured>` over the claim's
kill-rule paths "and must print zero commits" (`corpus/QUALITY.md:87`). The new row never
names row 79, gives no `supersedes`/`extends` cell, and ships a second tool for the same
predicate. Round 44 also ran **no** `freeze-drift` receipt at all: `grep -rn freeze-drift
.ufo/waves/round-44/` returns only incidental prose in wave-1 artifacts, nothing under
`l1/` or `controls/`. So the row's premise ("the only enforcement was inside the scoring
counter") is true of what *ran*, not of what the lane already *required*.

Its unique clause is timing: "before treating a commit as landed". The instrument cannot
do that — it accepts `--rev` and reads git objects (`frozen-path-preflight.py:29-50`); it
has no `--index`/`--staged` mode. The commits settle it: `c86ea508` at
`2026-10-28T10:43:43-03:00`; the tool and both receipts first appear in `8bb1090a` at
`11:18:01-03:00` (`git show --stat 8bb1090a`), after the violation landed. The gate
**detected** the violation; it did not gate the commit. As written the row reads as the existing freeze rule with a
demo attached, plus one clause the demo does not support.

## 3. Style against rows 68/69/70

| element | row 68/69/70 | new row 77 |
|---|---|---|
| what is checked | named exactly (top-level `instruments`; predicate byte-identical at four sites; count + class names + reader digests; invariant classes enumerated) | "gate every candidate revision against the claim's frozen pathspecs" — no walk shape (`-m --diff-merges=first-parent`, `M/D/R/T/U/A`, endpoint blob equality), no requirement that the pathspec set be the claim's **full** frozen set, no exit-2 semantics |
| what makes it fail | stated ("a paraphrased sentence or a map in the wrong shape is a defect"; "a floor is not an equality") | only "touching a frozen path"; silent on added/restored/renamed and on a green run under an incomplete pathspec |
| what a pass does **not** prove | present (69: "proves only the invariants it actually breaks"; 70: equality ≠ faithful class set, with the round-34 correction "equality detects a dropped class, not an unfaithful class set") | **absent** |
| evidence pointer | lesson + committed controls with numbers and red/green outcomes | lesson M44-2 + tool + two receipts — reproducible, but see §5 |

## 4. The second half is a separate criterion

The row's last sentence — "The same gate should be read as: a claim whose frozen prose and
frozen instrument disagree on one clause is unsatisfiable and must be caught at freeze, not
discovered after data (R44-CL2)" — fails on three counts:

1. **Different instrument.** The preflight compares git paths and blob ids. It has no
   representation of claim prose and no way to read a counter constant. In an isolated
   fixture where the only post-freeze commit edits `plans/round-44-claims.md`, the
   preflight with `--pathspec tools/round-44` prints `clean`, exit 0
   (`artifacts/R44W2Quality77/preflight/claim-edit-tools-round-44-pathspec.json`).
2. **No arm.** The row cites only the two preflight receipts; neither exercises a
   prose/instrument comparison. Nothing in the round's evidence shows a satisfiability
   check red on the frozen round-44 claim.
3. **The real case is concrete and already recorded elsewhere.** `plans/round-44-claims.md:34`
   requires the receipt's `parameters.output_directory` to name a
   `corpus/evidence/round-44/c1/` path; `:137` requires it to name the `/kaidoku-r44/`
   segment. One field, two values. The instrument implements only the second
   (`c1-counter.py:258` `PROV_SEGMENT = '/kaidoku-r44/'`, `:1176-1183`), and all four
   receipts carry the scratch form with `run_provenance_ok true`
   (`.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`, `carriers.*.run_provenance_ok`).
   So no *real* run can satisfy both clauses — its output directory is the scratch run
   directory, and the committed copy under `corpus/evidence/round-44/c1/` is a copy of the
   produced tree, not the run's output directory — while the counter is satisfiable on the
   form it implements. A contrived string that carries the corpus path as a *substring* of a
   scratch path (`…/kaidoku-r44/x/corpus/evidence/round-44/c1/<id>`) passes both prose
   clauses and `provenance_ok()` (`c1-counter.py:1176-1183` is a substring test plus `..`
   refusal); that is a loophole, not a route, and a satisfiability check must compare
   canonical paths, not substrings. Either way this is a *claim-vs-instrument* defect; a
   path gate cannot see it.

Belongs in the same row only if the row is rewritten as "a claim must be satisfiable by
its own instrument", which would drop the frozen-path gate entirely. It is a second
criterion, and it needs its own red arm (a claim with an unsatisfiable conjunct pair must
be refused at freeze) and a green arm (the same claim with one clause removed).

## 5. The evidence pointer: reproducible, but not a row-73 receipt

Both receipts parse equal to fresh runs (§1), so they are not fabricated. They are,
however, unbound:

```
python3 -c "import json;d=json.load(open('.ufo/waves/round-44/l1/preflight-c86ea508.json'));print(sorted(d))"
# ['blob_changed', 'freeze', 'gate', 'pathspec', 'rev', 'touched', 'verdict']
```

No `argv`, no tool sha256, no UTC instant — row 73 requires all three or an explicit
`caller_asserted`. The tool also has no `--selftest` and no isolated fixture arms in the
lane (row 61: "a new or relied-upon gate's self-invocation exercises its outer CLI and
asserts both exit code and stable findings on isolated green and red fixtures"). The arms
that exist are the lane's own history at two revisions, and the tool's first commit is the
same commit that carries the receipts.

## 6. What a green run actually proves (the missing clause, demonstrated)

A green run proves only: *no commit in FREEZE..REV changed a path under the supplied
pathspecs, and every frozen path present at FREEZE has the same blob id at REV.* It does
not prove:

- **That the tip is clean.** Green at `55bcce69`, red at `c86ea508` and at the tip (§1).
- **That the pathspec set is the claim's frozen set.** The receipts pass
  `--pathspec tools/round-44` only. On an isolated fixture whose single post-freeze commit
  edits `plans/round-44-claims.md`, the same invocation prints `clean`/exit 0 while
  `c1-counter.frozen_drift` returns `['plans/round-44-claims.md']` — the counter would exit
  2 at the same revision. Evidence:
  `artifacts/R44W2Quality77/cross-instrument.txt`, second fixture. On the fixture with a
  change only under `tools/round-44`, `--pathspec plans/round-44-claims.md` is likewise
  `clean` (exit 0) — `arms/06-wrong-pathspec.json`. The gate is only as complete as the
  caller's pathspec list, and the row does not require that list to come from the claim.
- **That the gate and the claim's counter agree on what a change is.** They do not.
  `c1-counter.py:1629-1669`: a path is frozen if it is in `FROZEN_PATHS` or under
  `FROZEN_PREFIXES` (`:272-286`, including `tools/round-44/`), but for status `A` it adds
  the path only when `show(freeze, path) is not None` (`:1662-1666`). A **new** file under
  `tools/round-44/` is therefore not drift for C1 — even though the counter's own comment
  at `:284-285` calls "a new round-44 tool" drift. Measured on the fixture: the preflight
  reds on `tools/round-44/new.txt` (`arms/01`, status `A`); `frozen_drift` at the same rev
  returns `[]` (`cross-instrument.txt`, first fixture). C2 does flag
  `added_under_frozen_dir` (`c2-counter.py:600-612`), so the lane now has three predicates
  for one rule.
- **That the staged worktree is clean.** The tool reads committed objects only; a
  commit-time gate needs index/worktree input, which no mode provides.
- **That the rule was enforced at commit time.** See §2.

## 7. Honest stop, M44-2, and the record (confirmations and three sufficiency gaps)

**Confirmed at `55bcce69`** (committed receipts read, one predicate recomputed):

- C1: `carriers_matched 4`, `met_target false`, `exit_code 1`, `failing []`,
  `bindings_false ['province_core_section','province_core_row','frontier_note']`, all four
  carriers `run_provenance_ok true`, `frozen_path_changed []`,
  `counter_sha256 9f2cc140…ea993` (counter blob identical at freeze and measured:
  `git rev-parse` both `9695d586…`). Independent `c1-counter.frozen_drift(LANE, freeze,
  55bcce69, carriers.json)` returns `[]`. So the score is admissible at `55bcce69` under the
  claim's own rule, and the stop is a *prose satisfiability* judgement, not a counter
  result: the counter's exit 1 is caused by the three documentation bindings that the stop
  deliberately left unlanded. The record should say that (see D8) — it currently reads as if
  the counter returned the contradiction, which it cannot.
- C2: `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`,
  `exit_code 0`, `counter_sha256` = `counter_sha256_at_freeze` = `085192ea…36277`. Tip
  receipt: `exit_code 2`, `entries_evaluated 0` (could-not-evaluate, not a mismatch).
  I did not re-run the C2 counter; seat `R44W2C2Rescore` owns that. Nothing I read
  contradicts the 80/0 verdict; vacuity and note-vs-value arms are that seat's assignment.
- The violation is real and still present at the tip: preflight exit 1 at `8bb1090a`,
  same 8 paths. `git diff --stat c48f8a4b c86ea508 -- tools/round-44/` = 8 files,
  +342/−303, all `M`.

**Not sufficient, three gaps the record must close:**

1. **What the 8 edits contain.** They are the C1 *control fixtures*, and the edits are
   substantive: `control-fixtures/pos/manifest.json` rewrites all four `evidence_id`s
   (e.g. `ev_4d2155ed…` → `ev_03c9cdb3…`), and
   `control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` changes 247
   lines. The frozen control receipts (`e9e3abd1`) certify the freeze bytes; no receipt
   re-scores the rewritten fixtures, and the lesson at `8bb1090a` calls them only
   "added/edited 8 files".
   A reader replaying CTL-C1-POS at the tip scores different bytes.
2. **Permanence.** Under the claim's rule ("no commit in FREEZE..REV touches a frozen path
   … a later restore does not un-block"), **no** revision at or after `c86ea508` can ever
   carry an admissible C1/C2 score. The record says the counters exit 2 at the tip and that
   `55bcce69` is the admissible revision; it does not say the score is permanently pinned
   to an ancestor of the violating commit.
3. **The landing commit is itself red and uncovered.** `8bb1090a` exits 1 at the frozen
   path and no preflight receipt exists for it (§1). The record commit therefore violates
   the very rule the row states, one commit after the row is written.

## 8. Numbered defects for the L1

- **D1 — duplicate criterion number.** `corpus/QUALITY.md:139` introduces "Row 77" while
  `corpus/QUALITY.md:85` already holds `| 77 |` (round-36 M36-3, cited by row 81's
  "sharpens 77"). The round's own record tags the new one too, at `8bb1090a`:
  `SCORECARD.md:3530` ("M44-2; QUALITY 77") and `LOG.md:3203` ("QUALITY 77"), while
  `LOG.md:3123` uses "QUALITY 77–78" for the round-36 rows. Command:
  `grep -n "Row 77\|^| 77 " corpus/QUALITY.md` → two hits; `grep -rn "QUALITY 77" LOG.md
  SCORECARD.md corpus/lessons/round-44.md` → both meanings. Observed: the number resolves
  to two criteria. Fix: renumber to 86 (and the new satisfiability row to 87), or add an
  explicit "supersedes 77" — which would be wrong, since the round-36 rule is still cited.
- **D2 — title and body claim a timing the instrument cannot deliver.**
  `tools/round-45/frozen-path-preflight.py:29-37` accepts `--root/--freeze/--rev/
  --pathspec/--json-out` only; there is no index mode. The violating commit `c86ea508` is
  at `10:43:43-03:00`; the tool and both receipts first appear in `8bb1090a` at
  `11:18:01-03:00`. Observed: the gate ran after the commit. Fix: state "before the
  candidate revision is cited or built on" and either add a `--worktree`/`--index` arm or
  drop "at commit time".
- **D3 — duplicate authority with row 79, no extension named.** Row 79 already mandates
  the same predicate via `tools/round-38/freeze-drift.py` before any score is cited. Round
  44 cites scores at `55bcce69` with no `freeze-drift` receipt anywhere under
  `.ufo/waves/round-44/` (`grep -rn "freeze-drift" .ufo/waves/round-44/` → only wave-1
  prose). Fix: the new row names "extends 79", says why `freeze-drift.py` is not reused
  (it lacks `-m --diff-merges=first-parent` and endpoint blob equality), and requires the
  substituted gate to be run in place of 79's, not beside it.
- **D4 — green under an incomplete pathspec is accepted as clean.** Demonstrated:
  `artifacts/R44W2Quality77/arms/06-wrong-pathspec.json` (exit 0 while `tools/round-44`
  changed) and `cross-instrument.txt` §2 (exit 0 while `plans/round-44-claims.md` changed;
  C1's `frozen_drift` returns that path). Command for §2:
  `python3 -I -B tools/round-45/frozen-path-preflight.py --root <FIXTURE> --freeze 69560bf
  --rev f9c8765 --pathspec tools/round-44` → exit 0. Fix: the row requires the pathspec set
  to be read from the claim file and to equal the counter's frozen set; the receipt records
  that set.
- **D5 — the gate and the C1 counter disagree on `A`.** `tools/round-44/c1-counter.py:1662-1666`
  ignores an `A` whose path did not exist at freeze; the preflight flags it
  (`frozen-path-preflight.py:63`). Measured: `arms/01-added-file.json` (exit 1,
  `tools/round-44/new.txt`) vs `frozen_drift` `[]` at the same rev
  (`cross-instrument.txt` §1). The c86ea508 arm is `M`-only, so the demonstrated red arm
  cannot distinguish the two predicates. Fix: one frozen-path predicate for gate and
  counters, with an `A`-under-frozen-directory arm on both.
- **D6 — the receipts fail row 73.** Keys are `gate, freeze, rev, pathspec, touched,
  blob_changed, verdict`; no `argv`, no tool sha256, no UTC. Fix: record them (the tool is
  107 lines; the change is one dict).
- **D7 — the C1 score receipt omits `counter_sha256_at_freeze`.** `plans/round-44-claims.md:85-86`
  requires it of every score receipt. `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`
  keys: `argv, bindings, bindings_false, carrier_ids, carriers, carriers_matched,
  carriers_spec_problems, carriers_unchanged, counter, counter_sha256, dev_matched,
  evidence_digests, exit_code, failing, freeze, frozen_path_changed, frozen_tables_valid,
  gap_rule_problems, met_target, predicate, prior_pin_sources, prior_pins,
  projection_profile, revision, seat, superblock_layout_notes, target` — no
  `counter_sha256_at_freeze` (C2's receipt has it). The value is recoverable
  (`git show c48f8a4b:tools/round-44/c1-counter.py | sha256sum` = `9f2cc140…ea993` = the
  receipt's `counter_sha256`; the blob id at both revisions is `9695d586…`), but it is not
  in the record.
- **D8 — the sufficiency gaps of §7.** The record must say: the 8 edits are the C1 control
  fixtures and include rewritten evidence ids; no descendant of `c86ea508` can carry the
  C1/C2 score; the landing commit `8bb1090a` is itself red with no receipt; and the C1
  exit 1 at `55bcce69` comes from the unlanded documentation bindings, not from the
  provenance contradiction (the counter passes the form its receipts carry). At my read the
  L1 already has an uncommitted edit to `corpus/lessons/round-44.md` (R44-CL2) that carries
  the last qualifier and the substring loophole; the other three are still absent from the
  committed record at `8bb1090a`.

## 9. Proposed replacement text

(For the L1 to adopt or reject; I have not edited `corpus/QUALITY.md`.)

> **Row 86 (a frozen path is gated per candidate revision, before that revision is cited).**
> Extends 79 from the score to the commit sequence: the round's own integration commit can
> write into a frozen directory after the score, and the rule then fails at the tip while
> the measured revision looked clean. For every candidate revision,
> `tools/round-45/frozen-path-preflight.py --freeze <freeze> --rev <candidate> --pathspec
> <the claim's full frozen set>` exits 0 before the revision is cited or built on; the
> pathspec set is read from the claim file, never typed by the operator, and the receipt
> records argv, the tool's sha256 and a UTC instant. A green run establishes only that no
> commit in FREEZE..REV changed a path under the supplied pathspecs and that every frozen
> path has the same blob at both endpoints. It does not establish that the tip is clean
> (green at `55bcce69`, red at `c86ea508` and at `8bb1090a`), that the index/worktree is
> clean (the tool reads commits only and cannot refuse a commit that does not exist yet),
> or that the gate and the claim's counter share a predicate (C1 `frozen_drift` ignores an
> added file under `tools/round-44/` that the preflight flags; the preflight with
> `--pathspec tools/round-44` is clean on a revision C1 reports as `frozen_path_changed`
> for `plans/round-44-claims.md`). Demonstrated: red `c86ea508` (8 touched, exit 1),
> green `55bcce69` (exit 0), feet `corpus/lessons/round-44.md` M44-2.

> **Row 87 (a frozen claim must be satisfiable by its own instrument).** Before a claim is
> frozen, every conjunct of its predicate is evaluated against a value its counter can
> compute, compared as **canonical paths and values, never as substrings**. A field two
> clauses require to hold different values is unsatisfiable for any real run and the claim
> is refused: R44-C1's `parameters.output_directory` must name a
> `corpus/evidence/round-44/c1/` path (`plans/round-44-claims.md:34`) and the
> `/kaidoku-r44/` segment (`:137`), and the counter accepts only the latter
> (`tools/round-44/c1-counter.py:258,1176-1183`), so every real receipt (`run_provenance_ok
> true`) can satisfy the instrument but not the claim; a path that merely embeds one path in
> the other is a loophole, not a route, and must not satisfy the check. The check names the
> conjunct pair and both computed values; it is red on the unsatisfiable pair and green on
> the same claim with one clause removed. This is not the frozen-path preflight, which reads
> git paths only. _Feet: `corpus/lessons/round-44.md` R44-CL2; `SCORECARD.md:3525`._

## 10. Receipts (this seat)

All commands run with cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; fixtures under
`/fast/scratch/hyaku/kaidoku-r44/R44W2Quality77/`, each `git init`-ed with
`git -C <fixture> rev-parse --show-toplevel` asserted equal to the fixture dir before the
first commit; identities only via per-command `GIT_AUTHOR_*`/`GIT_COMMITTER_*` env (no
global config touched, no commit outside a fixture). Scratch deleted before yield.

| # | command (abridged) | exit | stdout sha256 | wall |
|---|---|---|---|---|
| 1 | `frozen-path-preflight.py --root LANE --freeze c48f8a4b --rev c86ea508 --pathspec tools/round-44` | 1 | `20a87d4d…a28896` | 0.092 s |
| 2 | same, `--rev 55bcce69` | 0 | `c8a03c26…0a870f` | 0.092 s |
| 3 | same, `--rev 8bb1090a` | 1 | `c302813c…1cdf99` | 0.089 s |
| 4 | fixture arms 00–06 (`artifacts/…/arms/`) | 0,1,1,1,1,1,0 | see filenames | <0.1 s each |
| 5 | `c1-counter.frozen_drift(LANE,c48f8a4b,55bcce69,carriers.json)` | — | returns `[]` | <0.5 s |
| 6 | same at `c86ea508` / `8bb1090a` | — | returns the same 8 paths | <0.5 s |
| 7 | cross-instrument fixtures (`artifacts/…/cross-instrument.txt`) | 1 / 0 | recorded inline | <0.2 s |

No tools installed or upgraded (none needed); `pacman` untouched. No mutating git/jj
command run in the lane or anywhere else; no sibling lane or fleet-root file touched.

Artifacts: `.ufo/waves/round-44/w2/artifacts/R44W2Quality77/` — `preflight/` (three stdout
receipts, two committed-receipt reproductions, a byte copy of the tool), `arms/` (seven
fixture arms), `cross-instrument.txt`.
