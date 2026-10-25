# AStopCompleteness — is the R34-C2 stop record complete and self-consistent?

Seat: `L1Kaidoku34-2.AStopCompleteness` (reviewer, leaf — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; no VCS mutation).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/AStopCompleteness/`.
Tooling installed: **none** (python3 3.14.8 + stdlib + git reads; nothing needed).
Scope: the stop record `.ufo/waves/round-34/r34b/claim-stop.json` (landed `cd75b92e`), the round's
committed state, and the repair a future round must be able to build from it. Not in scope: reopening
the claim, repairing frozen instruments, awarding any score.

## 0. Axes named (Godspeed)

| axis | proxy | direction |
|---|---|---|
| A1 binding completeness | fraction of artifacts the record names that resolve at a fixed revision to content-addressed bytes | ↑ |
| A2 reproducibility | exact rerun from committed bytes alone: argv, cwd, seeds, counter pin, receipt, in-band UTC | ↑ |
| A3 self-consistency | record fields agree with each other and are orderable against the commits that contain them | ↑ |
| A4 repair-readiness | does committed state alone suffice to build the repair the record's own defects imply | ↑ |
| A5 honesty of landed claims | every "repair_landed"/"receipt" claim resolves to a real artifact | ↑ |

No move in this report trades one axis down for another: every finding is an added binding or an
exact correction of a pointer.

## 1. What is already complete and reproduces (so the stop is not hollow)

| # | claim | evidence | result |
|---|---|---|---|
| 1 | counterexample source binds to real bytes | `sha256sum .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` → `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97`; equal to `claim-stop.json:31` (`source_sha256`) | ok |
| 2 | that source is in the stop commit | `git cat-file -e HEAD:.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` → present; `git log --diff-filter=A` → added in `cd75b92e` | ok |
| 3 | the decisive counterexample reproduces | see §2 P1/P2 probes: three seeds, exit 0, `matched 8`, `met_target true` | ok |
| 4 | the surface it attacks is frozen and unchanged | `git diff --stat c79bbe7b HEAD -- tools/round-34/mini-fix/` → empty; pins 26/26 recompute (`git show --stat` per run below) | ok |
| 5 | the quoted frozen-counter line is the committed receipt line | python3 string equality of `claim-stop.json:.frozen_counter_verdict.line` vs `after/c2-at-instruments.txt` → `line_equal: True` (2026-10-25T07:34Z); receipt `measured_revision=c79bbe7b…` | ok |
| 6 | F1's pin container is byte-identical to the frozen map | recompute of all 26 digests: `same keyset: True n=26`, `mismatches: []`, `claims pin != inst pin: []` | ok |
| 7 | fixture surface has the target cardinality | `expected.json` → `fixtures 8 records 25`; `TARGET = 8` in `mini-counter.py` | ok |

The falsification itself is real: an unregistered, structure-blind reader reaches the counter's own
target on the frozen bytes. Nothing below disputes that.

## 2. Findings by severity

### P1-1 — the decisive counterexample has no receipt and no in-band time
`claim-stop.json` `decisive_counterexample` carries `argv`, `source`, `source_sha256`, `observed`
(including three seeds), but **no `receipt`** field, and the named command has no `--json-out`
(the mini counter prints JSON to stdout only: `tools/round-34/mini-fix/mini-counter.py:189-197`).
`l1_rerun_utc` is `"2026-10-25T07:28:00Z (approximate; exact clock in the wave report)"` and **names
no wave report file**. Contrast: the sibling `frozen_counter_verdict` block does bind a receipt
(`.ufo/waves/round-34/r34b/after/c2-at-instruments.json`). A future round must rerun to see anything
about the decisive run; there is nothing to read.

### P1-2 — the record dates its own decisive run *after* the commit that contains it
- `claim-stop.json` `l1_rerun_utc` = **07:28:00Z**.
- `claim-stop.json` landed in `cd75b92e`: `git log -1 --format='%cI' cd75b92e` →
  `2026-10-25T04:23:47-03:00` = **07:23:47Z** (local TZ `-0300`, `date +%z`).
- The wave-1 producer's own clocked receipts are 07:19:02Z / 07:19:56Z
  (`w1/ExecRedReproduce.md:81-85`).

So the stop record, as committed, cites an L1 rerun ~4 m 13 s after the record that cites it was
written, with an approximate clock and no artifact. Either the rerun happened after landing (and is
not pre-landing evidence) or the timestamp is wrong. Neither can be ordered from committed bytes.

### P1-3 — F1's "freeze-integrity receipt over it" does not exist
`claim-stop.json` F1 says `"repair_landed": ".ufo/waves/round-34/r34b/instruments.json … + freeze-integrity receipt over it"`.
- `git grep -n "freeze-integrity" HEAD -- .ufo/waves/round-34/r34b` → only `claim-stop.json`,
  `instruments.json`'s note, and `RevClaimsVsInstruments.md` prose. **No receipt file.**
- `find .ufo/waves/round-34/r34b -name '*freeze*' -o -name '*integrity*'` → empty.
The repair claim is therefore half-landed: the container is real and correct, the receipt is prose.

Worse, the repair's semantics are not what a reader would assume. Probe (read-only):
```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/instruments.json --rev HEAD
→ freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD   exit=0   2026-10-25T07:30:18Z
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/claims.json --rev HEAD
→ freeze-integrity: ERROR schema code=instruments_missing …        exit=3   2026-10-25T07:31:47Z
```
The container validates, but the instrument anchors the "freeze" at **`b917ea64`** — the post-data
audit commit — not at `c79bbe7b`. `commits_after_freeze=0` for all 26 rows therefore asserts "nothing
changed since the audit", not "nothing changed since the freeze". The stronger property holds only
because `b917ea64`'s parent is the freeze and the digests equal the freeze blobs (independently
established in `w1/RevFreezeOrder.md:§2`, untracked). The record states neither the argv, nor the
exit, nor this anchor caveat.

### P1-4 — four of the five met-target classes the round names have no committed source
The round's own accounting (worktree `SCORECARD.md:3353,3355`, `LOG.md:3098`) says *five* unregistered
structure-blind classes reach 8/8: content-multiset, "payload with names zeroed", value/offset,
record signature, transform/digest identity leak. Committed bytes contain **one**:
`git grep -n "s2b_record_sig|s2c_string_pool_noheader|s2b_digest_replay|s2b_label_hash_replay|payload_keyed" HEAD`
→ **no hits**. Concretely, the 8/8 readers are:
| class | artifact | committed? |
|---|---|---|
| content-multiset (nameset) | `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py`, `2e8feaea…` | **yes, in `cd75b92e`** |
| payload keyed, names NUL-ed | `/fast/scratch/hyaku/kaidoku-r34b/w1/LabratSeedSensitivity/payload_keyed.py`, `7d09798dfd7c…` | **no** (scratch only; report `w1/LabratSeedSensitivity.md` untracked) |
| record signature | `/fast/scratch/…/MutShortcutClasses/variants/s2b_record_sig.py`, `fe738549ada1…` | **no** |
| permuted-digest replay | `…/s2b_digest_replay.py`, `f94dab418659…` | **no** |
| label-hash replay | `…/s2b_label_hash_replay.py`, `2a55401e4b6f…` | **no** |
| string-pool, no header | `…/s2c_string_pool_noheader.py`, `81eae8c0acb6…` | **no** |
(source list and the "five readers hit 8/8" line: `w1/MutShortcutClasses.md:113`; the payload-with-names-zeroed run: `w1/LabratSeedSensitivity.md:136-137` → `payload_keyed_matches=8`, `structural.py` 0/8 on the same bytes.)
Committed `claim-stop.json` names only the first. Its `record_defects_disclosed` therefore cannot be
repaired from committed state: a future round that registers `nameset-replay` (as
`w1/ExecRedReproduce.md:121-127` prototypes) still lets at least three further classes through.

### P1-5 — the defect list omits the one defect that dictates the repair: the transform is deterministic
`mini-counter.py:120-131` permutes with `random.Random(seed)` and the default seed is a public
constant (`"kaidoku-r34-mini-v1"`, `:139`); fixtures are fixed. The transformed bytes are therefore
*constants*, so `sha256(copy)` is replayable offline. `s2b_digest_replay.py:2-13` does exactly that:
a hard-coded `TABLE` of the eight permuted-copy digests → answers, "Never parses the input", 8/8.
Consequence for repair: registering this class cannot restore CLEAN (the gate would answer
`REPLAY_GATE_REFUSED` on every run); the surface itself must become per-run fresh. The committed
`CtlMultiset-files/mini-counter-fresh.py` does that ("the green surface is GENERATED PER RUN from a
fresh seed"), yet the record never mentions it and `record_defects_disclosed` has no entry for the
identity leak. The stop's F3/F4 routes ("assert class count == pinned count", "red-last selftest")
do not address it. The defect is documented only in untracked files
(`w1/MutShortcutClasses.md:184` "F1b green-counter identity leak"; `w1/ScribeLesson.md:73` M34-8).

### P2-1 — 24 wave-1 seat reports are untracked at HEAD, including both files the record cites
`git status --porcelain .ufo/waves/round-34/r34b/w1 | grep -c '\.md$'` → **24 untracked** vs 44 tracked.
Named by the record:
- F4 evidence `w1/MutGateBranches.md` → `git cat-file -e HEAD:…` **absent**.
- F5 evidence `w1/RevFreezeOrder.md` → **absent**, and the record itself says `"(pending)"`.
Also absent: `CritClaimWidth.md`, `CritCounterLimits.md`, `MutShortcutClasses.md`,
`LabratSeedSensitivity.md` — the reports the omitted classes and limit defects live in.
`cd75b92e` adds only `claim-stop.json` + three control sources (`git show --stat cd75b92e`).

### P2-2 — the round's doc accounting is not committed
`git show HEAD:SCORECARD.md | grep -c R34-C2` → **0**; `git show HEAD:LOG.md | grep -c R34-C2` → **0**;
last commit touching them is `abbd7604` (2026-10-23). The R34-C2 blocks at worktree
`SCORECARD.md:3347-3357` and `LOG.md:3096-3099` are uncommitted (`git status` → ` M LOG.md`,
` M SCORECARD.md`, ` M SKILL.md`; `git diff --stat` → +36/−1). A future round cloning `cd75b92e`
sees no stop entry at all, only `claim-stop.json`.

### P2-3 — the recorded argv is under-specified for reproduction
`python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader .ufo/…/nameset.py`
- `--control-reader` is resolved against **cwd**, not against `--root` (`mini-counter.py:183-184` →
  `reader.is_file()`), and `--root .` is cwd-relative too. The record gives no cwd, so the same argv
  fails from any directory but the lane root.
- No `--seed` appears in `argv`; the three seeds in `observed` come from three separate invocations,
  two of which have no recorded command.
- The counter's own pin is absent from the block (it is `43ef669f…`, `instruments.json` +
  `claims[0].pins`), as are the fixture/`expected.json` pins (`5ebb5349…`).
- `w1/ExecRedReproduce.md:85` additionally records `--seed alt-3` = 8/8; the record says three seeds.

### P2-4 — F2 under-states the predicate defect for the run it actually reports
`claim-stop.json` F2 names sentences A (claims/config, `7c6c17f0…`) and B (counter/receipts,
`8340aea5…`). The counter used for the **decisive** run is the mini counter, whose constant is a
third sentence C (`P34-mini-records…`, sha256 `09988625205de2eb…`, recomputed at 07:30Z), listed only
in `predicate-reconciliation.json:C_mini_counter`. So the failing clause the stop demonstrates
("only record-array traversal associates a name with its record") belongs to a sentence the stop
record never prints, and the identity chain it does print (A vs B) is not the chain the evidence used.

### P3-1 — `frozen_counter_verdict.observed.matched` relabels a receipt field
The receipt (`after/c2-at-instruments.json`) has no top-level `matched`; 8 is `green.positive_matched`
(`.json` → `"green": {"positive_matched": 8}`). The record writes `"matched": 8`. Harmless to a human,
ambiguous to any future instrument that reads the record mechanically.

### P3-2 — two committed control sources are unbound by the record
`cd75b92e` also commits `CtlMultiset-files/pathkey.py` (input-identity class, 0/8 under the green
permutation) and `CtlMultiset-files/mini-counter-fresh.py` (fresh-content counter). `claim-stop.json`
mentions neither; their role and status survive only in tracked `w1/ExecRedReproduce.md:69-71,160,172`.
The fresh counter is the artifact the P1-5 repair needs — it should be bound, not merely adjacent.

## 3. Does the record name what a reader needs? Field-by-field

| needed artifact | named? | resolves? |
|---|---|---|
| counterexample source | yes | yes: sha256 matches, committed in `cd75b92e` |
| command (argv) | yes | yes, **if** cwd = lane root; no `--json-out` |
| seeds | yes (3) | yes (default + alt-1/alt-2); no argv per seed; alt-3 omitted |
| **receipt / stdout** | **no** | **missing** |
| exact UTC of the decisive run | **no** (approximate; pointer unnamed) | **missing**, and postdates `cd75b92e` |
| counter + fixtures pins | **no** (derivable from `instruments.json`) | indirection only |
| class registry / pinned class count | **no** | derivable from `gate-config-mini.json` (7 shortcuts + 1 positive) and `replay-gate.py:31 MIN_SHORTCUTS=3` |
| F1 repair receipt | claimed, **absent** | **missing** |
| F4/F5 evidence files | yes | **dangling** (untracked) |
| other four met-target classes | **no** | **missing** (scratch-only) |
| fresh-content counter | **no** | committed but unbound |

## 4. What a future round still needs (missing-artifact inventory)

1. **A committed receipt for the decisive run** (stdout JSON + exit + UTC), dated after `cd75b92e`
   if that is when it actually ran — and the record must stop implying a pre-landing rerun.
2. **Committed source + sha256 for every met-target class** it counts (payload-keyed, record-signature,
   permuted-digest, label-hash, string-pool), or an explicit statement that only `nameset` is bound
   and the rest are seat-scratch observations. As it stands the round's "five classes" claim has one
   fifth of its provenance in committed bytes.
3. **A defect entry for the deterministic-transform identity leak**, with the concrete repair target
   (per-run fresh content; the committed `mini-counter-fresh.py`), not only the F3/F4 registry guards.
4. **The F1 receipt and its anchor semantics**: argv, exit, and the fact that
   `freeze-integrity … --claims instruments.json` prints `freeze=b917ea64`, i.e. the audit commit,
   with `commits_after_freeze` measured from there.
5. **The wave-1 evidence files the record cites** (`MutGateBranches.md` for F4,
   `RevFreezeOrder.md` for F5 — currently `(pending)`) plus `CritClaimWidth.md`,
   `CritCounterLimits.md`, `MutShortcutClasses.md`, `LabratSeedSensitivity.md`.
6. **An explicit F3 target**: where the pinned class list and its count live, and that
   `MIN_SHORTCUTS=3` is the floor the repair must replace.
7. **The doc accounting committed** (`SCORECARD.md`, `LOG.md`, and the `SKILL.md` change), since none
   of it is in `HEAD`.
8. **A per-class receipt matrix** (class → reader sha256 → counter → seed → matched → exit → UTC);
   the record has exactly one row and no matrix.

## 5. Probes run (exact argv, exit, UTC)

All counter/reader execution happened in `/fast/scratch/hyaku/kaidoku-r34b/w2/AStopCompleteness/repro/`
(byte copies of `tools/round-34/mini-fix/` and the committed `nameset.py`). No ELF, fixture or R34-C1
artifact was executed; readers ran only as `python3` children of a counter.

```
cd /fast/scratch/hyaku/kaidoku-r34b/w2/AStopCompleteness/repro
/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py --seed kaidoku-r34-mini-v1
→ {"finding":"records_match","matched":8,"met_target":true,"target":8,…}  exit=0  2026-10-25T07:29:25Z
same with --seed alt-1 → matched 8, met_target true, exit=0  2026-10-25T07:29:25Z
same with --seed alt-2 → matched 8, met_target true, exit=0  2026-10-25T07:29:25Z
```
```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims \
  .ufo/waves/round-34/r34b/instruments.json --rev HEAD
→ freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD   exit=0  2026-10-25T07:30:18Z
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims \
  .ufo/waves/round-34/r34b/claims.json --rev HEAD
→ freeze-integrity: ERROR schema code=instruments_missing …       exit=3  2026-10-25T07:31:47Z
```
Pin recomputation (python3, read-only): 26/26 digests equal `claims[0].pins` and the worktree bytes;
`mismatches: []`. `git diff --stat c79bbe7b HEAD -- tools/round-34/mini-fix/` → empty.
Unrun: the mini counter was not run over the other four classes (their sources are scratch/untracked
and their 8/8 status is taken from the seat reports named above, not re-measured here).

## 6. Residual risk and verification gaps

- The other four 8/8 claims are quoted from `w1/MutShortcutClasses.md:113` and
  `w1/LabratSeedSensitivity.md:136-137` (both untracked); I did not rerun those readers. That does not
  weaken the completeness finding — it *is* the finding: they cannot be rerun from committed state.
- F5's `RevFreezeOrder.md` was read in the worktree (untracked); its ordering conclusions are not
  re-derived here.
- Loose-object birth times and the jj op log were not re-read; commit/committer times only.
- I did not evaluate whether the stop is *correct* (that is other seats' scope): I only measure whether
  the record can carry its own claim forward.

## Verdict

**STOP RECORD INCOMPLETE** — the falsification reproduces (nameset 8/8, exit 0, three seeds,
2026-10-25T07:29:25Z) and every frozen byte it attacks is unchanged, but `claim-stop.json` binds one
of the five met-target classes, has no receipt and no orderable time for its decisive run (its
`l1_rerun_utc` 07:28:00Z postdates its own landing commit `cd75b92e` 07:23:47Z), claims a
freeze-integrity receipt that does not exist and omits that the repaired gate anchors `freeze=b917ea64`,
cites two evidence files that are untracked (`MutGateBranches.md`, `RevFreezeOrder.md` `(pending)`),
and omits the deterministic-transform identity leak that dictates the only repair that can restore a
CLEAN surface; a future round starting from `cd75b92e` can rebuild the repair for one class out of five
and none of the round's SCORECARD/LOG accounting, which is uncommitted.
