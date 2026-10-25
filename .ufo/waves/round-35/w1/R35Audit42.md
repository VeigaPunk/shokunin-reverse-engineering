# R35Audit42 — wave 1 seat report: do-nothing reachability (item 1)

Seat: `R35Audit42` (UFO-FSD critic). Scope: read-only + private `/tmp` only; the only lane
write is this report. No VCS mutation, no counters/plans/corpus edits, no scoring.

Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (all paths below relative to it).

## Test executed

Re-ran both frozen counters at the **base** revision (do-nothing control) with the freeze
revision used by the committed control receipts:

```
BASE=aa04633a686d49756763b1feed4be6830d5bb479
FZ=2323d197456f1328459d9420aff025cffbcb3e27

python3 -I -B tools/round-35/c1-coverage-counter.py --root <LANE> --freeze $FZ --rev $BASE
python3 -I -B tools/round-35/c2-calibration-counter.py --root <LANE> --base $BASE --rev $BASE --freeze $FZ
```

## Result 1 — do-nothing cannot reach either claim (both exit 1)

C1 at base: **exit 1**, 8 named failures (entry_missing ×2, registry_row_missing S125/S129,
province_missing ×2, readme_missing ×2). C2 at base: **exit 1**, 8 named failures
(D1_census_start_missing; D2_lesson_missing; D3_source/verified_at/recheck_missing +
D3_source_not_s106; D4_not_eight_cells Round-32 line1081 cells=4; D4_section_missing
Round-34 run-6). No check group passes at base. Base tree confirms absence: no
`.ufo/waves/round-35/` at base, no r35 knowledge entries, no S125/S129 rows in
`corpus/SOURCES.md` (`git grep` empty), no `corpus/lessons/round-35.md`; the r34b entry
exists at base but without the appended trio (so D3 fails on the trio lines, not the file).

Receipt fidelity: my `/tmp` receipts are byte-identical to the committed controls
`.ufo/waves/round-35/controls/c1-do-nothing.json` / `c2-do-nothing.json`. Instrument bytes
match the frozen pins in `.ufo/waves/round-35/claims-canonical.json` (C1 e28792c7…, C2
576c14dd…, plan 45b644a4…); claims-canonical.json is byte-identical at 2323d197 and HEAD;
census-start.txt sha256 (b6ce2b17…) matches the `frozen_inputs` pin; both counters'
selftests pass (green=0 red=1).

## Result 2 — freeze-revision constraint (scoring instruction)

The counters hardcode reading `.ufo/waves/round-35/claims-canonical.json` at `--freeze`.
That file first exists at **2323d197**; using the documented canonical-freeze commit
f1ea3a6d yields **exit 2** (claims file absent at freeze revision), not a clean control
failure. Scorers must pass `--freeze 2323d197…` (or any rev ≥ it, incl. HEAD) for both
counters; f1ea3a6d/e4ca43dd/etc. are unusable as `--freeze`.

## Result 3 — strongest falsification hazard found (C2 D-4 satisfiability)

The frozen D-4 check is structurally exact, so reaching it requires corpus changes beyond
fixing row cell counts:

1. **Round-34 run-6 heading mismatch.** `SKILL.md` (base and HEAD) heads the section
   `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)`;
   the check requires the exact line `### Round-34 run-6 instrument registry`
   (`l.rstrip() == sec`). That exact line does not exist at base or HEAD → D4_section_missing
   persists unless the after-state renames the heading to the bare literal.
2. **Round-32 span contains unrelated tables.** The check counts every `|` line between
   `### Round-32 instrument registry` and the next `##`/`###` heading. That span (base lines
   1064–1208) also contains the Residual-witness-registry table (4-cell rows at lines
   1081–1084) and a 3-cell decisions table (~line 1121+). Any such row < 8 cells fails D-4,
   so those regions must be moved out of the span (or converted to 8-cell rows) for the
   claim to be reachable.

This is the strongest predicted risk for the C2 data phase; C1 has no analogous hazard (all
C1 checks are absence-based at base and content-token based at the measured revision, with
prep captures already committed).

## Limits

Read-only audit; no lane production writes; no nested delegation; no `/fast/scratch`
traversal; analysis only — no score computed.
