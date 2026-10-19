# CR-3 patch text (proposed, NOT applied) — make the guard's third pin explicit in the frozen-run clause

Seat CR-3, chain c2, wave arc3-loop1-round1. EX-16 owns the real target; the parent
integrates. Nothing here has been applied to the repo. Base hashes at write time:
probe `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f`,
expected.json `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33`,
pointer-table.json `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
(all three match PL-2's patch-text base hashes; gate files untouched this wave).

## Why (measured, see claims/c2/CR-3/matrix-evidence.txt §4)

PL-2's guard (fail-closed on an absent pin, tampered on a mismatched table) is
sound for the *practiced* frozen replay (current pinned table + `--rev 679af5d`
-> `failed findings=16 exit=1`, measured). It does not hold for the clause's
*inputs* reading, and the two readings now disagree by exit code:

- replay with the table the frozen verdict was actually measured with
  (`edaa4e59…`, the 13-entry table at 265e1aa/045c1b8) -> exit 2
  `pointer_table_tampered` (measured, guard variants A and B);
- replay with any pre-pin `expected.json` -> exit 2 `pointer_table_unpinned`
  (fail-closed rule, measured);
- the block's own combination is unsatisfiable as inputs: the gate does not exist
  at the pinned revision (`git ls-tree 679af5d -- .ufo/gates/` empty; 5 commits
  before the gate lands at 265e1aa), so `revision: 679af5d` + `table_sha256:
  738b3a56` names a state that never existed;
- the admitted reading (current table at 679af5d) measures 16 findings in 4
  classes, so the block's `expected_findings: ["citation_dead"]` is already false
  for the only replay the guard admits (CR2.md:74 measured the same mismatch at
  the 13-entry table: 6 findings, 3 classes; the flip is table-version dependent —
  `sc698-sc2-refuted-record` passes at :698 (r4-era pin) and fails at :699 (HEAD
  pin) at rev 679af5d);
- six distinct table digests exist since the gate landed; under the fail-closed
  rule five of them, plus every pre-pin expected.json, are refused inputs.

Verdict in one line: the pin makes *a* replay reproducible, not the *recorded*
frozen measurement; the block must say which one it means.

## Patch 1 — expected.json, frozen_run block (single-line style preserved)

Current:
```json
"frozen_run": {"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "note": "the revision the committed verdict was measured against; a run over a different revision is a different measurement", "verdict": "failed", "expected_findings": ["citation_dead"]}
```

Proposed (adds PL-2's `table_sha256` plus the two fields that make the leg
defined by artifacts; keep the historical measurement, do not overwrite it):
```json
"frozen_run": {"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "note": "the revision the committed verdict was measured against; a run over a different revision, or with a table whose bytes differ from table_sha256, is a different measurement -- and under the preflight a differing table is refused, not measured", "verdict": "failed", "expected_findings": ["citation_dead", "citation_file_absent", "citation_out_of_range"], "table_sha256": "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f", "table_scope": "replay reading: the CURRENT committed table (table_sha256) graded against frozen_run.revision; the table of the round-2 measurement is frozen_run.history[0] and is refused by the preflight (pointer_table_tampered) by design", "history": [{"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "table_sha256": "edaa4e59c804bc0fd424c68daafa38a1bdef5fb395b3c10b3d61e614f5bef641", "table_shape": "13 entries / 4 quoted", "measured": {"findings": 6, "classes": ["citation_dead", "citation_file_absent", "citation_out_of_range"]}, "recorded": ".ufo/waves/arc2-loop1-round10/CR2.md:64-74; .ufo/waves/arc2-loop1-round10/E21.md:91-100"}]}
```

Notes for the integrator:
- `expected_findings` must list the *classes* the admitted replay produces (three
  today; the count drifts with the table, which is why the count is not pinned —
  or pin a count and accept the same-commit re-pin obligation for it too).
- The `history` row is what makes CR2's recorded 6-finding measurement
  reproducible-as-recorded: it names the input digest that run used, which no
  committed artifact names today.
- If the parent prefers the r4 E9 precedent (`.ufo/waves/arc2-loop1-round4/E9.md:132-135`
  `expected_census {drift, recorded, exempt}` with `frozen_run_mismatch` exit 2),
  that form is robust to table growth and can be carried *instead of* the
  byte-pin: it pins the measurement, not the input bytes, so legitimate table
  extension never turns the frozen leg into could-not-evaluate.

## Patch 2 — SKILL.md registry row wording (line 371; patch text only, protected file)

Keep PL-2's added sentence, with two corrections:

1. Name the mechanism for what it is. PL-2 writes "the sha256 of
   `pointer-table.json` (**frozen-run guard**; any edit to the table must re-pin
   the digest in the same commit)". Measured: it guards the *table input*, not the
   frozen run (the block is unread metadata; `grep -c frozen probe` -> 0). Suggested
   replacement wording:

   "**table-input preflight (R6 debt): the table's sha256 must match the digest
   pinned in `expected.json` (`pointer_table.sha256`); a table read from the
   `--table` path only (never from `--rev`) -- a mismatched table is
   `pointer_table_tampered`, an absent table is `pointer_table_unreadable`, and a
   baseline that pins no digest is `pointer_table_unpinned`; all three exit 2
   before any entry is graded. Any edit to the table must re-pin the digest in the
   same commit; a replay that needs the pre-pin table is refused by design (the
   frozen-run history row records that table's digest)**"

2. Add the replay reading to the row's command cell so the frozen leg is defined
   by the row, not by a seat's memory:

   "frozen-run replay: the command above with `--rev
   679af5d749f2fd48b9d543e3c99d348d5458f90f` and the current table; expect
   `failed`, exit 1 under `--strict`, findings = the classes in
   `frozen_run.expected_findings`"

## Patch 3 — probe (optional, wording only; PL-2's code hunks stand)

The FROZEN-RUN GUARD docstring block PL-2 adds (`patch.md:26-31`) says "Any edit to
the table must re-pin the digest in the same commit." Add one sentence so a future
reader does not mistake a refused replay for a broken instrument:

   "The pinned table is the CURRENT table; a run with any other table (including
   the table a historical frozen verdict was measured with) is refused, exit 2 --
   that is the preflight's declared class, not a drift finding."

## Not proposed

- No change to the guard's placement, ids, or CNE tuple: PL-2's patch already adds
  `pointer_table_tampered` and `pointer_table_unpinned` to the verdict map
  (patch.md:39-43). Measured counter-example for why that matters: a preflight
  without the verdict-map hunk reads a tampered table as `reported findings=1
  exit=0` in default probe mode (silent findings) and `failed exit=1` under
  `--strict` — never the declared exit 2 (matrix-evidence §4, variant D).
- No resolution of the table through `git show <rev>:`. Measured: that design
  (`matrix-evidence §4` variant C) makes the frozen replay exit 2 *permanently*,
  because no table exists at the pinned revision.
