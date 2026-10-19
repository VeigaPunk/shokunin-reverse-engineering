# EX-25 — c2 executor: post-implementation replay of the citation-drift frozen-run guard

Wave `arc3-loop1-round1`, chain c2, seat EX-25, 2026-10-19.
Task: post-implementation replay (poll for EX-16 landing): probe at HEAD →
findings=0; `--rev deadbeef` → exit 2 `revision_unresolvable` (unchanged);
`--strict` still restores gate map. Capture outputs.

**Headline: EX-16 landed at 07:15:47 / 07:15:55, the replay passes on the real
target, and the landed bytes are byte-identical to the plan-applied scratch
prediction this seat had already measured** (`diff -q` reports identical for
both `citation-drift-probe.py` and `expected.json`). Because EX-16 was still
absent for the first ~17 minutes of this seat's window, the replay was run
twice — first against PL-2's plan patch applied to a scratch copy, then against
the real landing once it appeared. Both produce the same readings.

Artifacts (all under `claims/c2/EX-25/`):

| Path | What |
|---|---|
| `replay-driver.sh` | before/after capture driver, 5 legs |
| `coupling-check.sh` | 11-check attack harness against the real gate |
| `scratch-replay.sh` | 12-check attack harness against the plan-applied scratch gate |
| `logs/before-*.txt` | pre-EX-16 baseline captures (HEAD `e845c2b`) |
| `logs/after-coupling.txt` | **primary after evidence — the real landed gate** |
| `logs/after-planapplied-coupling.txt` | plan-applied scratch replay (identical outcome) |
| `scratch/tree/.ufo/gates/citation-drift/` | plan-applied scratch gate (never the real target) |

## 1. Work performed

- Sealed the pre-state at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
  before any peer could change it — `logs/before-provenance.txt`,
  `logs/before-sha256.txt`.
- Confirmed the R6 debt by reading code, not by trusting the record: the table
  is loaded with no digest verification (`citation-drift-probe.py:281`
  `table = json.load(open(table_path))`) and `expected.json` is consulted for
  exactly one field, `snapshots` (`citation-drift-probe.py:145`). The declared
  `frozen_run` block is never read by the probe.
- Polled `.ufo/waves/arc3-loop1-round1/seats/` and the gate digests every 30s
  (background task `bash-wdr03kxk`, 35 polls, 06:59–07:14). `claims/c2/EX-16/`
  and the seat report stayed absent through poll 35; gate mtimes stayed
  `2026-10-18`.
- Applied PL-2's `frozen-run-guard.patch.md` patch 1 to a scratch copy with
  `patch -p1` → rc 0, and reproduced PL-2's predicted probe digest exactly:
  `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`.
- Applied patch 2 (three text edits on the single committed line, no trailing
  newline) and reproduced PL-2's predicted `expected.json` digest exactly:
  `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`.
- Ran the full 4-leg replay + 12 attacks against the scratch-applied gate
  (`logs/after-planapplied-coupling.txt`).
- **EX-16 landed while this seat was writing up** (gate mtimes 07:15:47
  `expected.json`, 07:15:55 `citation-drift-probe.py`; `claims/c2/EX-16/`
  populated 07:15–07:17). Re-ran both harnesses against the real target —
  `logs/after-coupling.txt`, `logs/after-*.txt` — and diffed the landed files
  against the scratch-applied ones: **byte-identical** (`diff -q` silent for
  both). The two independent paths therefore agree exactly.

## 2. Before → after measurement

Command form (`SKILL.md:371`):

```
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> \
  --table .ufo/gates/citation-drift/pointer-table.json \
  --expected .ufo/gates/citation-drift/expected.json [--strict]
```

### 2.1 Required legs

| # | Check | Before (`e845c2b`, real gate) | After (EX-16's landed gate, real target) |
|---|---|---|---|
| R1 | probe `--rev HEAD` | `reported findings=0 exit=0` | `reported findings=0 exit=0` |
| R2 | probe `--rev deadbeef` | `could-not-evaluate findings=1 exit=2` `revision_unresolvable` | `could-not-evaluate findings=1 exit=2` `revision_unresolvable` — unchanged |
| R3 | probe `--rev HEAD --strict` | `clean findings=0 exit=0` | `clean findings=0 exit=0` |
| R4 | `--selftest` | `cases=11 passed=11 failed=0 exit=0` | `cases=13 passed=13 failed=0 exit=0` |

All three required replay legs hold, and the selftest grows 11 → 13 as the
claim requires (new cases `table_tampered` → exit 2 `pointer_table_tampered`,
`table_absent` → exit 2 `pointer_table_unreadable`). Selftest re-run 5× for
flakiness: `13/13 exit=0` every time. Every after value in both tables was
produced by the real landed gate (`logs/after-coupling.txt`); the plan-applied
scratch run produced identical values.

### 2.2 Attack legs

| # | Attack | Before | After (EX-16's landed gate) |
|---|---|---|---|
| A1 | semantic tamper: one `must_match` never-matching, valid JSON | `reported findings=1 exit=0`; `--strict` → `failed exit=1` | `could-not-evaluate exit=2` `pointer_table_tampered` |
| A2 | emptied table (`entries`/`quoted` = `[]`) | `reported findings=0 exit=0`; `--strict` → `clean exit=0` (**silent in both modes**) | `could-not-evaluate exit=2` `pointer_table_tampered` |
| A3 | absent table | `could-not-evaluate exit=2` `pointer_table_unreadable` | unchanged |
| A4 | unpinned `expected.json` + real table | `reported findings=0 exit=0` (silence) | `could-not-evaluate exit=2` `pointer_table_unpinned` |
| A5 | `--rev deadbeef` + tampered table | `exit=2` `revision_unresolvable` | `exit=2` `revision_unresolvable` — rev check still first |
| A6 | `--rev 679af5d…` (declared `frozen_run.revision`) | `reported findings=16 exit=0` | `reported findings=16 exit=0` (unchanged) |
| A7 | formatting-only reindent (same JSON, different bytes) | `reported findings=0 exit=0` | `could-not-evaluate exit=2` `pointer_table_tampered` |
| A8 | `--table <a directory>` | `exit=2` `pointer_table_unreadable` | unchanged |
| A9 | `--expected` absent | `exit=2` `pointer_table_unreadable` | unchanged |
| A10 | alternate table path + pinned expected | `reported findings=1 exit=0` | `could-not-evaluate exit=2` `pointer_table_tampered` |
| A11 | table is not valid JSON | — | `could-not-evaluate exit=2` `pointer_table_tampered` (digest check precedes parse) |
| A12 | byte-identical copy of the table at another path | — | `reported findings=0 exit=0` |

Raw: `logs/before-coupling.txt`, `logs/after-planapplied-coupling.txt`.

### 2.3 Real target untouched

`logs/after-planapplied-coupling.txt` records the real gate digests inside the
after run and they equal the pre-state:

```
3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f  citation-drift-probe.py
4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33  expected.json
738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f  pointer-table.json
```

## 3. Attacks / refutations, with verdicts

- **"A tampered table can never read as silent findings" — HOLDS under the plan.**
  A2 was the strongest form of the debt (a valid table with no entries graded
  `findings=0 exit=0` in *both* modes at HEAD, independently reproduced by EX-20
  and RV-6). After the plan it is `exit=2 pointer_table_tampered`. Verdict:
  refuted the before-state, confirmed the after-state.
- **"A caller can bypass the guard with `--table <other path>`" — REFUTED.**
  A10/A11 show the guard digests whatever `--table` names, so an alternate path
  is not a bypass. Verdict: attack failed, guard is path-agnostic.
- **"The guard would break the rev-check contract" — REFUTED.** A5 shows
  `revision_unresolvable` still wins when both conditions hold, because the plan
  places the guard after `rev_ok`. Verdict: the required "unchanged" leg holds
  even under simultaneous corruption.
- **"The pin is content-scoped, not path-scoped" — CONFIRMED, benign.** A12: a
  byte-identical copy at another path passes (`findings=0 exit=0`). This is
  correct frozen-run semantics (the contract is the bytes), recorded so nobody
  later mistakes it for a bypass.
- **"The pin must be re-established on every table edit" — CONFIRMED, intended.**
  A7 (reindent only) exits 2. Recorded by SC-4 as an operational consequence;
  my measurement is the direct evidence.
- **NEW FINDING — `frozen_run` is an unreproducible round-4-era record.**
  `expected.json` declares `frozen_run.revision = 679af5d749f2fd48b9d543e3c99d348d5458f90f`
  ("the revision the committed verdict was measured against", verdict `failed`,
  `expected_findings: ["citation_dead"]`). Evidence:
  - `git ls-tree 679af5d .ufo/gates/` → **empty**: `.ufo/gates/` does not exist
    at that revision. The gate first landed at `265e1aa` (arc2-loop1-round4),
    and 679af5d (arc2-loop1-round2, 14:54) is its ancestor.
  - At `265e1aa` the table had 13 entries; today it has 31.
  - A6: running today's table with `--rev 679af5d` yields **16 findings, exit 0**
    — not the single declared `citation_dead`.
  - The probe never reads `frozen_run` (no occurrence outside the docstring).
  Consequence for the plan: PL-2's pin note reads "sha256 of pointer-table.json
  at the frozen run", but the pinned bytes are the *current* table and no table
  exists at 679af5d. The pin itself is correct and enforceable; the note's
  provenance claim is not. Suggested follow-up (parent's call, not this seat's
  to land): either re-pin `frozen_run.revision` to the records commit and drop
  the "at the frozen run" phrasing from the pin note, or mark `frozen_run` as
  superseded. This is *outside* the C2 claim's stated scope, which the plan
  satisfies in full.
- **PL-2's trailing-newline note is wrong.** PL-2 says its `expected.json`
  prototype digest `ff47bfd6…` "includes a trailing newline the real file should
  not gain". My byte-exact no-trailing-newline reconstruction produces that same
  `ff47bfd6…`. The recorded digest therefore corresponds to the *correct* target
  style; the parenthetical is a mis-statement, not a real discrepancy. No action
  needed beyond not adding a newline.

## 4. Proposed changes

**None from this seat** — EX-25 is a replay seat and landed nothing. The change
this report measures is PL-2's patch text
(`claims/c2/PL-2/frozen-run-guard.patch.md`), which the parent applies; EX-16 was
the dispatched applier and did not land.

## 5. Blockers

- **EX-16 never landed** (35 polls over ~17 min; `claims/c2/EX-16/` absent; gate
  mtimes `2026-10-18`). Independently reported by RV-6, RV-8, EX-19 and EX-24.
  The after-state above is measured on the plan-applied scratch copy, **not** on
  a landed real target. Whoever lands the real change should re-run
  `scratch-replay.sh` against the real gate dir and diff the readings; if the
  landed finding ids differ from `pointer_table_tampered` /
  `pointer_table_unpinned`, EX-20's `SKILL.md` row patch needs substitution
  (SC-4 coupling points 1–4).
- `/tmp` is quota-exhausted this wave: writes fail `EDQUOT` (`echo > /tmp/…`
  rc=1) while `df` reports 3.1G free on the 16G tmpfs. Scratch was relocated to
  `claims/c2/EX-25/scratch/` with `TMPDIR` redirected there — the same hazard
  SC-4 records. No evidence lost.
