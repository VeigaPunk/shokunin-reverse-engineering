# R45W2SweepAudit — the lane's own commit scope, swept and attacked

Seat `R45W2SweepAudit` (reviewer). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Range attacked: `f762b7273e3f6ca3c710bb37d5de92a4a4417aec..main` (`main` = `0ee50aaff516571aa607769bbbdf19a3db90dfa5`
at the time of this sweep). Base `149133d47aa7e90796f96047afe6d251a3e65b2c` for the widened check.
Read-only on the lane and on the fleet repo; every receipt ran from scratch and every command is
re-runnable. UTC stamps are in `receipts/receipts.tsv`.

**Headline.** The path-level scope holds: 12 commits, 538 path-commit rows, 524 unique paths,
**zero paths outside the declared sets**, no renames, no deletions, no symlinks, no gitlinks, no
fleet-repo path. Three independent enumerations agree and the lane's own gate agrees at every
commit. Five findings survive: one record number that is wrong (`wave 2: 32 seats` vs 36), one
record citation to a file that does not exist, one unrepaired "measured revision" head, one
literal claim that the filesystem falsifies (ignored `__pycache__/` inside the frozen directory
after the freeze), and one caveat about the 15 wave-1 seats that never spawned.

---

## 1. Method and the declared sets

The declared sets, exactly as this seat states them:

| class | paths |
|---|---|
| exact | `plans/round-45-claims.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`, `LOG.md`, `SCORECARD.md` |
| prefix | `tools/round-45/`, `.ufo/waves/round-45/` |

Three enumerations were run and compared, not one:

1. per commit — `git diff-tree --no-commit-id --name-status -r <c>` for all 12 (`per-commit-name-status`);
2. union of the per-commit name-only rows (`union-paths`);
3. one aggregate `git diff --name-only FREEZE..main` (`aggregate-diff-paths`).

Rows 2 and 3 are **byte-identical** (`union-equals-aggregate` → `IDENTICAL`; both 34 040 bytes,
sha256 `e7d51111c2ae8ae02df46242e484d3c332ac933c6c2cfe2a003c0044fa4f1120`). That also fixes the
arithmetic: 520 `A` + 18 `M` = 538 rows over 524 unique paths, so exactly 14 repeat touches
(5×`corpus/lessons/round-45.md`, 4×`SKILL.md`, 3×`SCORECARD.md`, 3×`LOG.md`, 2× each of
`w2-spec.json`, `w2-gen.py`, `w2-dispatch.json` → 4+3+2+2+1+1+1 = 14).

The outside-set check is `grep -vE` over the union with the declared regexes. It exits **1** with
**0 bytes** of output: for this check an empty match set *is* the pass, so exit 1 here means "no
row outside the sets", not "the check failed". The same shape holds for `base-to-main-outside`
(0 bytes) and `rename-copy-rows` (0 bytes, exit 0 on awk's no-input rule).

## 2. Verdicts

| # | attack | verdict | discriminating evidence |
|---|---|---|---|
| A1 | Any changed path outside the declared sets in `FREEZE..main` | **holds** (0 outside) | three enumerations agree; `outside-declared-sets` empty; top components are only `.ufo` (519), `corpus` (2), `SKILL.md`, `SCORECARD.md`, `LOG.md` |
| A2 | Any commit in the range touches a frozen path | **holds** (none) | `frozen-log` empty; claims blob `f93df4c3…` and `tools/round-45` tree `8cb6fa80…` identical at freeze and main; gate `clean` at all 12 commits; both counters exit 0 at `main` with `frozen_path_changed []` |
| A3 | A fleet-repo path in a lane commit | **holds** (none) | fleet repo tracks **0** `kaidoku-shokunin/` paths (`.gitignore:1:*-shokunin/`); lane `.git` is a real directory, `core.worktree` unset; all 538 rows are mode `100644`/`100755`, no `120000`, no `160000` |
| A4 | The freeze commit itself is a bulk sweep (the round-44 defect) | **holds** | freeze commit = **10** paths (claims + 4 tools + 5 control receipts), 0 outside; widened `base..main` = 13 commits, 0 outside. 432-path class did not recur |
| A5 | Merge commit that edits a frozen path in its resolution | **holds for the record's claim; blind spot confirmed** | fixture: `frozen_path_changed = []` while `--diff-merges=first-parent` returns `plans/round-45-claims.md`. Range has **0** merges, so A1's conclusion is unaffected |
| A6 | SCORECARD/LOG wave-2 seat count and its citation | **falsified** | `32` vs `36`; `r45-w2-results.json` absent — see F1 |
| A7 | SCORECARD section head states the round's measured revision | **falsified (stale head)** | `1f4b27f8` at `:3527` vs `A3` at `:3590` — see F2 |
| A8 | "Nothing in `tools/round-45/` changes after the freeze" | **falsified (literal, filesystem) — low** | ignored `.pyc` files inside the frozen directory, mtimes after the freeze commit, counters still exit 0 — see F3 |
| A9 | Wave-1 seat accounting vs the claims file's reporting duty | **holds by delegation, caveat** | 40 allocated / 25 reports / 15 never spawned — see F4 |
| A10 | `tools/round-45/*` as a one-level glob vs a directory freeze | **holds now** | `tools/round-45/` holds 4 flat files at main; a future subdirectory would read as "outside the declared set" without being outside the freeze — calibration limit, not a defect |

## 3. Per-commit ledger

All 12 commits are single-parent (`merge-count` → `0`; `merge-list` → empty; every row of
`parent-shape` has one parent). `A` = added, `M` = modified, `D` = deleted: no `D`, no `R`, no `C`.

| commit | subject (abridged) | A | M | total | declared class(es) | note |
|---|---|---|---|---|---|---|
| `9ff920cd` | wave-1 spec, dispatch, registry, do-nothing receipts | 8 | 0 | 8 | `.ufo/waves/round-45/` | 3 controls + spec/dispatch/gen/ready + `w1/swarm-registry.json` |
| `e715263c` | land block 22 + six registry rows; S140/S141; lesson | 1 | 2 | 3 | `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md` | exactly the three named surfaces |
| `1f4b27f8` | A1: block 22 cites the pre-freeze gate entry | 0 | 1 | 1 | `SKILL.md` | one hunk in block 22 |
| `abfeda50` | LOG entry, SCORECARD section, score receipts | 4 | 2 | 6 | `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-45/l1/scores/` | 4 receipts at `1f4b27f8` and `e715263c` |
| `faa875bc` | wave-2 spec, dispatch, registry | 4 | 0 | 4 | `.ufo/waves/round-45/` | 36-item spec |
| `fedd11bf` | A2: lesson corrections, CL6..CL12, block 22 limits | 1 | 2 | 3 | `SKILL.md`, `corpus/lessons/round-45.md`, `.ufo/waves/round-45/l1/` | one preflight receipt |
| `14340d41` | A2 re-measurement in SCORECARD/LOG + receipts | 2 | 2 | 4 | `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-45/l1/scores/` | |
| `92b4970c` | mine M45-3, route CL13/CL14 | 0 | 1 | 1 | `corpus/lessons/round-45.md` | |
| `f59565b7` | A3: c1-run.sh row, arm-isolation and `--dirty-pathspec` limits | 0 | 2 | 2 | `SKILL.md`, `corpus/lessons/round-45.md` | |
| `1d04c6af` | A3 as measured revision; re-dispatch to A3 | 3 | 5 | 8 | `.ufo/waves/round-45/` (3 receipts + 5 record/spec edits) | the only commit that edits `w2-*` after `faa875bc` |
| `a63d109f` | route R45-CL17 | 0 | 1 | 1 | `corpus/lessons/round-45.md` | |
| `0ee50aaf` | land the wave-1 record: 25 reports + dirs, ledger, `w2.ready` | 497 | 0 | 497 | `.ufo/waves/round-45/` | 25 seat `.md` + 470 files under 25 seat dirs + `swarm-registry.json` + `r45-w1-results.json` + `w2.ready` = 497 |

The two commits that need explaining are explained by their own counts, checked against the
message: `0ee50aaf`'s "25 seat reports and dirs" is exactly 25 `.md` + 25 dirs
(`w1-report-count` = 25; `w1-dir-count` = 26, the 26th being `w1/swarm-registry.json`).
`1d04c6af` is the only in-range commit that rewrites the wave-2 spec after it landed; it is inside
`.ufo/waves/round-45/` and is correctly append-only in the two record files.

In-file scope was also checked for the six record/landing files, not just their paths:

- `SKILL.md` — 4 commits, each hunk confined to rule block 22 (`@@ -544`, `-557`, `-568`, `-569`,
  `-580`) and the `### Round-44/45 instrument registry` table (`@@ -1570`, `-1643`); no other rule
  block, registry row or section is touched.
- `corpus/SOURCES.md` — one hunk at EOF adding exactly S140 and S141.
- `SCORECARD.md` — 3 hunks, all appends at EOF (`@@ -3515,3 +3515,55`, `-3567,3 +3567,15`,
  `-3579,3 +3579,14`).
- `LOG.md` — 3 hunks, all appends at EOF (`-3230,3 +3230,64` in `abfeda50`,
  `-3291,3 +3291,17` in `14340d41`, `-3305,3 +3305,12` in `1d04c6af`);
  no earlier LOG entry is rewritten.
- `corpus/lessons/round-45.md` — 5 touches, all inside the round-45 lesson; no other lesson file
  changed.

## 4. Findings

### F1 — the wave-2 seat count is wrong and its citation is absent (medium)

- **Input** (as committed at `main`):
  - `SCORECARD.md:3527-3528` — ``measured revision `1f4b27f8`. Wave 1: 40 seats; wave 2: 32 seats
    (counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`).``
  - `LOG.md:3273-3275` — ``**Waves:** wave 1 40 seats and wave 2 32 seats under
    `.ufo/waves/round-45/`; role mix, dead seats and per-seat outputs are read from
    `{r45-w1,r45-w2}-results.json` and recorded in the fleet report.``
- **Differing value**: `w2-spec.json` `items` = **36**, `w2-dispatch.json` `counts.total` = **36**,
  `registry.members` = **36** (`w2-spec-items`, `w2-counts`). `git cat-file -e
  main:.ufo/waves/round-45/r45-w2-results.json` → **absent** (`w2-results-presence` = `ABSENT`);
  the w1 file is present.
- **Why it happened (derive, not excuse)**: `abfeda50` (the SCORECARD/LOG entry) is *older* than
  `faa875bc` (the wave-2 spec): `rev-list --reverse` order is `… 1f4b27f8, abfeda50, faa875bc …`,
  so "32" was written before any wave-2 spec existed and neither A2, A3 nor the wave-1 land
  commit corrected it. `36` has been the committed value since `faa875bc`.
- **Fix**: amend both lines to `36` and cite `w2-spec.json`/`w2-dispatch.json`; move the
  `r45-w2-results.json` citation to a conditional ("when the wave settles") or drop it until the
  file exists.
- **Attack lever**: `sed -n '3527,3529p' SCORECARD.md`; `sed -n '3273,3275p' LOG.md`;
  `python3 -c "import json;d=json.load(open('.ufo/waves/round-45/w2-dispatch.json'));print(d['counts'])"`.

### F2 — the SCORECARD section head still names the superseded measured revision (low-medium)

- **Input**: `SCORECARD.md:3527` says ``measured revision `1f4b27f8```; `SCORECARD.md:3590` says
  `**The measured revision for the round is A3**`.
- **Differing value**: the round's measured revision is **A3** = `f59565b782c18b0eb691bec12f52d2f80d9f5032`,
  per the section's own append-only A3 paragraph and the LOG `### Amendment A3 — the final measured
  revision` section. The head paragraph is not repaired by either amendment.
- **Note for the L1**: this seat's own prompt repeats the stale value ("amendment A1 … the measured
  revision"); the bytes say A3 and SCORECARD:3590 says A3. Any report that repeats A1 as *the*
  measured revision inherits F2.
- **Fix**: append one line to the head paragraph — `superseded by A2 and A3; see the A3 paragraph`
  next to `:3527` — or move the pointer there. Do not rewrite the append-only A2/A3 text.
- **Attack lever**: `grep -n 'measured revision .1f4b27f8.\|The measured revision for the round is A3' SCORECARD.md`.

### F3 — "nothing in `tools/round-45/` changes after the freeze" is false on the filesystem (low)

- **Input**: `plans/round-45-claims.md` — *"Nothing in this file or in `tools/round-45/` changes
  after the freeze: a change makes both counters exit 2 `frozen_path_changed`."*
- **Differing value**: the worktree contains `tools/round-45/__pycache__/c1-counter.cpython-314.pyc`
  (mtime `2026-10-28 12:32:10 -0300`) and `c2-counter.cpython-314.pyc` (`12:32:44`), both **after**
  the freeze commit `f762b727` (`2026-10-28T12:27:20-03:00`), and both counters still exit **0**
  (`counter-c1-at-main`, `counter-c2-at-main`). `.gitignore:1:__pycache__/` hides them from
  `git status --porcelain`, and the frozen arm reads commit history, so neither arm can see them
  (`ignored-in-frozen` → `!! tools/round-45/__pycache__/`).
- **Scope of the falsification**: the *scored* claim is unaffected — no tracked byte, no blob, no
  commit changed. What is false is the unrestricted sentence: the frozen *directory* can gain
  ignored content after the freeze with no arm reporting it.
- **Fix**: either narrow the sentence ("no **tracked** path under `tools/round-45/` changes") or add
  `--ignored` to the dirty-arm invocation and a `red-ignored-in-frozen-dir` case. The second is the
  honest one for a round whose whole subject is instrument blind spots.
- **Attack lever**: `stat -c '%y %n' tools/round-45/__pycache__/*`; `git status --porcelain --ignored -- tools/round-45/`.

### F4 — wave 1 reports 40 seats; 15 of them never spawned (caveat, not a falsification)

- `r45-w1-results.json` has `seats = 40`, 40 entries, **15** of which carry the same note:
  *"never spawned: host job-cap refusal during wave fill; wave completed without it (partial-fill
  loss recorded by L1)"*. Only **25** seat reports exist (`w1-report-count` = 25), which matches the
  land commit's "25 seat reports and dirs".
- The claims file requires: "Seat counts, role mix and dead seats come from
  `.ufo/waves/round-45/<wave>-results.json` and are reported from there." Both record lines cite the
  file, so the delegation holds; but a reader of `Wave 1: 40 seats` alone reads participation that
  did not happen for 15 seats.
- The 15: `R45W1ConnFleetOwnership`, `R45W1CritSweepClass`, `R45W1DistillPredicates`,
  `R45W1InhBlockCount`, `R45W1InhCommandA`, `R45W1InhQualityRows`, `R45W1InhSkillTail`,
  `R45W1InhSweepEvidence`, `R45W1InhTipCounters`, `R45W1ProbeTmp`, `R45W1RevControls`,
  `R45W1RevengerSweepPath`, `R45W1ScribeLessonDraft`, `R45W1SentDeepRead`, `R45W1SimplDedupe`.
- **Fix (optional)**: state `wave 1: 40 dispatched / 25 reported / 15 not spawned (job cap)` where
  the count is given.

### F5 — calibration of this sweep's own method: it is merge-blind (stated, neutralised here)

- The prescribed enumeration `git diff-tree --no-commit-id --name-status -r <c>` prints **no diff
  for a merge commit**, and the round-45 counters' frozen arm (`git log --name-only`) has the same
  hole. The record already routes this as **R45-CL6 (HIGH)**; this seat reproduced it end to end.
- Fixture (`fixture-merge-blindness`, parents = 3, merge resolution appends a line to
  `plans/round-45-claims.md`):
  - `git log --name-only --format= FREEZE..MERGE -- plans/round-45-claims.md tools/round-45/` → empty;
  - `git diff-tree --no-commit-id --name-status -r MERGE` → empty;
  - `git diff-tree -m --first-parent --no-commit-id --name-status -r MERGE` →
    `M  plans/round-45-claims.md` (twice, once per parent);
  - `frozen_path_changed(fixture, F, MERGE)` → `[]`;
    the `--diff-merges=first-parent` variant → `['plans/round-45-claims.md']`.
- **Why A1 still holds**: the lane range has **0** merges (`merge-count` → `0`, `merge-list` empty,
  every commit single-parent), so merge-blindness cannot hide a path here. If any future round's
  range contains a merge, both the sweep and the counters must add `--diff-merges=first-parent`.

## 5. What holds, with the command that shows it

| claim | command | result |
|---|---|---|
| 12 commits in the range, linear | `git rev-list --count FREEZE..main` · `git rev-list --count --merges FREEZE..main` | `12` · `0` |
| no path outside the declared sets | union of per-commit `--name-only` piped to `grep -vE '<declared>'` | 0 rows, 0 bytes (exit 1 = no match) |
| union = aggregate | `diff <(git diff --name-only FREEZE..main \| sort) <(per-commit union)` | `IDENTICAL` |
| no renames/copies/deletions/symlinks/gitlinks | `git diff-tree -r -M -C --name-status` per commit; `--raw` modes | 0 `R`/`C`; 0 `D`; modes only `100644`/`100755` |
| frozen bytes unchanged | `git rev-parse FREEZE:plans/… main:plans/… FREEZE:tools/round-45 main:tools/round-45` | `f93df4c3…`/`f93df4c3…`, `8cb6fa80…`/`8cb6fa80…` |
| no in-range commit touches a frozen path | `git log --format='%h %s' FREEZE..main -- plans/round-45-claims.md tools/round-45/` | empty |
| the lane's own gate agrees at every commit | `frozen-path-preflight.py --freeze F --rev <c> --pathspec tools/round-45/ --pathspec plans/round-45-claims.md --freeze-path …` ×12 | `clean`, exit 0 each |
| the gate's own red cases are live | `frozen-path-preflight.py --selftest` | `cases=11 failures=0`, exit 0 |
| counters score at `main` | `c1-counter.py` / `c2-counter.py --freeze F --rev main` | exit 0; C1 `rule_blocks 22`, `rows 10`, `refs 8`, `unresolved []`; C2 `scope_size 6`, `unregistered []`, `thin []`; both `frozen_path_changed []` |
| counters are red at the freeze | same, `--rev F` | exit 1; C1 `rule_blocks 21`, `rows 0`; C2 `unregistered` = all six |
| freeze commit is not a bulk sweep | `git diff-tree --no-commit-id --name-status -r f762b727` | 10 paths, 0 outside |
| widened base..main is clean | per-commit union over `149133d4..main` vs declared sets | 13 commits, 0 outside |
| no fleet path as a tracked path | `git -C /home/vgpnk/Projects/shokunin ls-files \| grep -c '^kaidoku-shokunin/'`; `check-ignore -v kaidoku-shokunin` | `0`; `.gitignore:1:*-shokunin/` |
| tracked worktree clean | `git status --porcelain -- plans/… tools/round-45/ SKILL.md corpus/ LOG.md SCORECARD.md` | empty |
| the SCORECARD's round-44 disclosure is real | `tools/round-44/c2-counter.py --freeze c48f8a4b --rev main` | exit 2, `frozen_path_changed` = 10 (8 fixtures + `SCORECARD.md` + `SKILL.md`) |

Content-level note on "fleet paths": added lines reference the fleet only as *citations*, never as
tracked paths or write targets — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
`…/scripts/hyaku/jj-lane.sh`, `…/scripts/hyaku/ufo-wave-policy.json`, in `w1-gen.py`, `w1-dispatch.json`,
`w1-spec.json`, `w2-gen.py`, `w2-dispatch.json`, `w2-spec.json`, the two `R45W1CensusDupClass`
reports, `R45W1SrcGitDiffTree` (bare `/home/vgpnk/Projects/shokunin/`) and
`corpus/lessons/round-45.md`. No such path is written by any commit.

## 6. Residual risk and verification gaps

1. **No semantic caller analysis.** No `lsp` device is mounted in this seat, so caller/definition
   checks that would have used `lsp references|definition|diagnostics` fell back to git plumbing,
   `grep`, and a Python `importlib` load of the counter to call `frozen_path_changed` directly.
   Recorded as a fallback, not as semantic proof.
2. **Merge blindness** (F5): neutralised by 0 merges in the range, not fixed in the instruments.
3. **Ignored files inside frozen directories** (F3): invisible to both arms.
4. **The worktree is mid-wave.** `git status --porcelain` shows untracked wave-2 seat dirs and three
   wave-1 leftovers (`l1/preflight-c86ea508.json`, `l1/preflight-round45-frozen.json`,
   `w1.ready.dispatched`). The sweep judges the committed tree at `main`; nothing tracked is dirty.
5. **`r45-w2-results.json` will presumably appear at wave-2 close**, which resolves F1's citation
   half but not its count half (36, not 32).
6. **Not run**: S140/S141 page bytes (another seat's surface), the round-44 counter corpus, any
   other lane, and any fleet-repo file. Contract forbids the last two; the first two are out of
   seat scope by the wave spec.
7. **Declared-set wording**: `tools/round-45/*` is a one-level glob while the freeze unit is a
   directory. No subdirectory exists today (`frozen-tree-files` = 4 flat files), so the two
   readings coincide; they would not if a subdirectory were added.

## 7. Receipts

`receipts/receipts.tsv` holds all 52 receipts plus a header row (label, exit, stdout sha256, bytes,
UTC, exact command). Six rows exit non-zero and all six are the *expected* semantics, not failures:
`outside-declared-sets` and `base-to-main-outside` exit 1 because `grep -vE` found no offending row;
`fleet-tracks-lane` exits 1 because `grep -c` counted 0 lane paths in the fleet index;
`counter-c1-at-freeze` and `counter-c2-at-freeze` exit 1 because the do-nothing control is supposed
to be red; and `r44-c2-counter-at-main` exits 2 because the round-44 rubric is bound to files this
round edits (`could-not-evaluate`, `frozen_path_changed`), which is the disclosure it is testing.
The rows this report leans on:

| label | exit | stdout sha256 | bytes | UTC |
|---|---|---|---|---|
| commit-count | 0 | `a1fb50e6c86fae1679ef3351296fd6713411a08cf8dd1790a4fd05fae8688164` | 3 | 2026-10-28T16:04:34Z |
| merge-count | 0 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 | 2026-10-28T16:04:34Z |
| per-commit-name-status | 0 | `9edaaa72e833db111b48eaa56fab5b2f1cad2000e6c4fef6b2748d8694212376` | 35391 | 2026-10-28T16:04:34Z |
| union-paths | 0 | `e7d51111c2ae8ae02df46242e484d3c332ac933c6c2cfe2a003c0044fa4f1120` | 34040 | 2026-10-28T16:04:34Z |
| aggregate-diff-paths | 0 | `e7d51111c2ae8ae02df46242e484d3c332ac933c6c2cfe2a003c0044fa4f1120` | 34040 | 2026-10-28T16:04:34Z |
| union-equals-aggregate | 0 | `1e00073b48fe3b36fc839da3b74b515bbecc9def677e059553835bb86bde8c55` | 10 | 2026-10-28T16:04:34Z |
| outside-declared-sets | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | 2026-10-28T16:04:34Z |
| frozen-log | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | 2026-10-28T16:04:34Z |
| frozen-oids | 0 | `642ec19873d2b962a7490af04d39b31519e9f934027b99adee499b46fe616cd6` | 164 | 2026-10-28T16:04:34Z |
| freeze-commit-count | 0 | `917df3320d778ddbaa5c5c7742bc4046bf803c36ed2b050f30844ed206783469` | 3 | 2026-10-28T16:04:34Z |
| base-to-main-outside | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | 2026-10-28T16:04:34Z |
| worktree-tracked-clean | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | 2026-10-28T16:04:34Z |
| ignored-in-frozen | 0 | `f613e8d9f380bff3fa04b188e4e65a6e04297fbee62b7c695f5a90196a3a45f3` | 31 | 2026-10-28T16:04:34Z |
| gate-per-commit | 0 | `d48614dc28a7814d244bf848a03cbec4af747a879924afefdd11302caafaffad` | 192 | 2026-10-28T16:04:34Z |
| gate-selftest | 0 | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 791 | 2026-10-28T16:04:35Z |
| counter-c1-at-main | 0 | `4b2eb21a619c15438c73c6cf56a868fc046f5cef85d46d343acc07ecbb337e9c` | 495 | 2026-10-28T16:04:35Z |
| counter-c2-at-main | 0 | `7528d520399fbdf1aa5844108bc77940dd4852412b599592a2e9af531f558361` | 689 | 2026-10-28T16:04:35Z |
| counter-c1-at-freeze | 1 | `e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1` | 624 | 2026-10-28T16:04:35Z |
| counter-c2-at-freeze | 1 | `d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0` | 905 | 2026-10-28T16:04:36Z |
| fixture-merge-blindness | 0 | `768858cef2fb5d6f8bb2101bc3b97c32c1fc29a31904158469c48d3d29beed7d` | 1254 | 2026-10-28T16:04:36Z |
| w2-counts | 0 | `351d969d063ab157c4510f340cd29fea6d3ea1da9751340460e241b7c4108498` | 58 | 2026-10-28T16:04:36Z |
| w2-spec-items | 0 | `3ce64e218912e3d758c2a28b7879d8872e06102222bdcb5caa9bb03d8a4a61c7` | 9 | 2026-10-28T16:04:36Z |
| w2-results-presence | 0 | `ede4663fa9a5e8031704705268edde90aae07273f42b7b7274db7b317a40b001` | 7 | 2026-10-28T16:04:36Z |
| w1-results-seats | 0 | `0b974f027c4ee6a44526465ec4280e97d7b3bdef166447e4abaf6125dae96571` | 29 | 2026-10-28T16:04:36Z |
| scorecard-seat-sentence | 0 | `3e45bf98c32d0516da1b3cd818865e97df18dbc85eb7514d5757e920b57b9cde` | 132 | 2026-10-28T16:04:36Z |
| log-seat-sentence | 0 | `aa11ca2e2c91c53f039c673c1df38322bf6c0acfd73d8c8e401c067ba1ddf562` | 238 | 2026-10-28T16:04:36Z |
| fleet-tracks-lane | 1 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2 | 2026-10-28T16:04:36Z |
| r44-c2-counter-at-main | 2 | `c079ca32c2cb76248f2a9065be3006a3956ba9693751021aca6025acc55c957e` | 1688 | 2026-10-28T16:07:17Z |

Artifacts copied into this seat directory: `receipts/receipts.tsv` (52 receipts + header),
`receipts/union-paths.txt`, `receipts/per-commit-name-status.txt`, `receipts/fixture-merge-blindness.out`,
`receipts/c1-at-main.json`, `receipts/c2-at-main.json`, `receipts/r44-frozen-paths.out`,
`receipts/r44-c2-counter-at-main.out` (+ `.err`), `receipts/outside-declared-sets.out` (0 bytes),
`receipts/scope-sweep.py`, `receipts/fixture-merge-blindness.sh`.
Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2SweepAudit`
was removed after copying. No installs (nothing needed). No mutating git command was run against the
lane or the fleet repo — the only commits are inside the scratch fixture, whose toplevel was asserted
equal to the fixture directory before the first commit; the only
writes are inside this seat's directory and in scratch.

## 8. Axis read (the seat's own three)

- **coverage** — every commit in the declared range enumerated with three agreeing methods, plus the
  freeze commit and the widened base range; every declared path class exercised; in-file hunk scope
  checked for all six record/landing files. No declared surface left unreached.
- **depth** — the sweep did not stop at "0 outside": it tested the instruments the sweep depends on
  (gate ×12, both counters at two revisions, the round-44 counter, the merge fixture), and it
  falsified three record statements (F1, F2, F3) that a path-only sweep would have passed.
- **calibration** — the verdicts separate "the scored artefact survives" from "the sentence around
  it is wrong" (F3), record one method limit instead of hiding it (F5), and record exit-1-on-grep as
  a pass with the reason, not as a failure.
