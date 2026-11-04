# Round 79 — declared claims (frozen; no amendments after the freeze commit)

Base `29d2ca30b83a6a0d85b0aa979de0138fde1660e6` (the round-78 lane tip after the round-78
non-author spot-check; lane tree clean and pushed at the start).

Two claims on two distinct axes, causally separable: C1 mutates the round-78 gate's own
`--selftest` cases and reads only that instrument's output; C2 parses `PROVINCE.md`'s pointer
cells and reads the live files they name. Neither instrument reads the other's receipt and
neither reads a value the other produces. Both are capability acquisitions in the AXES sense:
the instrument runs, its output verifies, and its row enters the SCORECARD capabilities table
in the same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies. The stagnation nudge's waiver is not met (capability rows entered
in rounds 73–78, inside the 10-round window), so no waiver is claimed. **`lowest-axis:
calibration`** — R79-C1 works a tied-lowest axis; C2's axis is `freshness` (the record's live
pointers), which the lane reports every round and which is not a second calibration claim.

**Population — the round-78 wave's routed items.** The round-78 mutation seat (`MutGate`)
reported two survivors, `m03` (`NEAR_MISS_RE` made dead; no selftest case exercises an
unparsable near-miss spelling) and `m08` (`validate_receipt`'s refused-without-a-reason guard
removed; no selftest case calls `validate_receipt`). The round-78 non-author spot-check routed
six defects; item 3 (stale line pointers; a path-only pointer rule) and item 4 (no self-test
receipt at the final instrument revision) are this round's work. Disposition:

- survivors `m03`, `m08` (+ the uncovered atom-absent conjunct `m05`) → **R79-C1**.
- spot-check item 3 → **R79-C2**; item 4 → the landing `pre/selftest-gate.txt` receipt at the
  final instrument revision, carried **unclaimed** and cited by the SKILL row.
- items 1, 2, 5, 6 (prose receipt revisions, supersession count, stale line range, LOG heading)
  are record/prose repairs, carried **unclaimed**, closed in this round's record and report.

## R79-C1 — calibration: the gate's selftest mutation survivors close, one declared case each

**Type.** Capability acquisition. Round 78 landed a ten-class attack gate whose selftest carries
29 cases; its wave showed eight textual mutants of the gate and two survivors because the
selftest had no detector for two code paths. This round freezes the mutation question as a
committed battery: eight mutants, each with ONE declared selftest case, at a measured revision.

**Surface.** `tools/round-78/attack-gate.py`'s own selftest cases and the eight mutation classes
in `tools/round-79/gate-mutation.py`'s `MUTANTS` table — one exact single-occurrence edit per
mutant, applied to the target blob at `--rev`.

**Rule.** A mutant is KILLED only when its declared case is present in the mutant's selftest
output and fails there. An absent declared case is a SURVIVOR, never a pass: that is exactly the
round-78 defect (a detector that does not exist cannot catch anything). A mutant whose anchor
occurs 0 or >1 times, or whose copy emits no `SELFTEST` summary, is INCONCLUSIVE and never
counted as killed.

**Predicate (one sentence, frozen).** R79-C1 is verified iff
`python3 -I -B tools/round-79/gate-mutation.py --root . --rev <measured> --work <scratch>
--battery --json-out <receipt>` exits 0 with `mutants_total 8`, `killed 8`, `survivors 0`,
`declared_case_hits 8`, `target_pin.matched true`, a pristine selftest of 29 cases and 0
failures, and a defect-free `validate`; each mutant's declared case is present and fails in that
mutant's selftest and the three mutants `m03`, `m05` and `m08` (the two round-78 survivors plus
the atom-absent conjunct) are detected by that one case alone, while at base `29d2ca30` the same
battery exits 1 with `survivors 3` naming `m03`, `m05` and `m08`.

**Kill rule (frozen).** Any of: a mutant counted killed while its declared case is absent from
the selftest output or passes there; a mutant killed by a case other than its declared one
counted in `declared_case_hits`; an anchor applied at 0 or >1 occurrences counted as a mutant; a
copy without a `SELFTEST` summary counted as killed; a pristine selftest that is not green; a
receipt admitted without re-deriving its own target pin; a `--validate` defect; an empty mutant
set meeting `survivors 0` without `mutants_total 8`; a declared case that exists only in the
battery's own text rather than in the target's selftest.

**Controls (scored before data).** `--control empty-set` at base: `mutants_total 0`, `ok false`,
exit 1 — an empty set meets `survivors 0` vacuously and is refused by the `mutants_total 8`
clause. The base arm itself is the do-nothing control: the same frozen battery against the
un-fixed gate reports `survivors 3` and misses the target (`pre/c1-at-base.json`).

## R79-C2 — freshness: the record's pointers bind at the line they name

**Type.** Capability acquisition. Round 78's surface recheck compared
`pointer.split(":")[0]` — the path only — so two moved lines scored green (the round-78 closure
routed it). This round binds each pointer cell to the token it claims and to the line it names.

**Surface.** `PROVINCE.md`'s five drift-prone pointer cells (three REA pins, the Ghidra
`application.version` line, the `.bashrc` export range) and the live files they name.

**Rule.** A pointer is bound only when its path exists, its line is a forward 1-based range
inside the file, and every declared token occurs on a line inside that range. A pointer without
a line is unparsed; a line past end of file is a mismatch; the pointed lines are retained as a
sha256, never as bytes (the configs' non-pin content is not evidence).

**Predicate (one sentence, frozen).** R79-C2 is verified iff
`python3 -I -B tools/round-79/pointer-bind.py --root . --rev <measured> --json-out <receipt>`
exits 0 with `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0` and a defect-free
`validate`, every pointer bound at the line and range it names, while at base `29d2ca30` the
same command exits 1 with `mismatches 2` naming `omp-pin` (record `:8`, the pin at `:12`) and
`kimi-pin` (record `:4126`, the pin at `:4722`), and the control `--control path-only` reports
`mismatches 0` on that same stale record.

**Kill rule (frozen).** Any of: a recorded value that does not parse counted as matched; a
pointer path compared without reading its line; a line number treated as 0-based; a range
compared as its first line only; a file read outside the pointer's declared path; a mismatch
suppressed by normalising it away; a receipt without its `checked_at`; the `path-only` control
used as the claim's counter instead of the line-bound rule.

**Controls (scored before data).** `--control path-only` at base: `mismatches 0` on the same
stale record (`pre/controls/c2-path-only.json`) — it cannot fail on a moved line, so it cannot
be the claim's rule. Its selftest red cases (`red-stale-line`, `red-past-end`, `red-no-line`,
`red-backwards`, `red-range-token-outside`) and their green look-alikes are committed
(`pre/selftest-c2.json`).
