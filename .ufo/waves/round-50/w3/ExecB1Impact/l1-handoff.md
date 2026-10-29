# L1 handoff — ExecB1Impact (C2 B-atom couplings at the attempt-2 landing)

**Verdict: the planned landing is green (exit 0, `mismatches 0`, 11/11 atoms, battery clean)
in exactly one safe shape.** Two text rules and one structural rule decide it.

**1. BLOCKER — the round-50 corrections section must stay the LAST `##` section of
`SCORECARD.md`, and the attempt-2 section must go BEFORE it.** A/B measured on two clones
with byte-identical landing text except the order:
- attempt-2 section appended AFTER `## Record corrections — round 50` → **exit 1**,
  `mismatches 0` but `battery.failing = ['B3 duplicate line -> red [] noop []', B4, B5, B10,
  B11]`. The atoms read green; the **battery** is what catches it, because the battery's
  duplicate-line arm appends at EOF and the duplicate then lands outside the section the
  counter reads.
- attempt-2 section inserted BEFORE the corrections section → **exit 0**, `battery.failing []`,
  `mutation_count 52`, `do_nothing_red` = all 11.

This is not in the attempt-2 plan text. Also: a *second* corrections section whose heading
starts with `## Record corrections — round 50` (e.g. `… round 50 attempt 2`) turns **B3, B4,
B5, B10, B11 red** (`2 … sections, want 1`) — measured.

**2. The Owned-axes coverage row must lead with `140/140 knowledge files mapped`** (B1 takes
the FIRST `N/N knowledge files mapped` phrase and compares it to the `.md` count under
`corpus/knowledge` at REV: base 139, +1 C1 entry = 140). Leaving `139/139` first → red
(`coverage row states 139/139, derived 140 knowledge files`). And the README `## Coverage map`
must map the new stem `2026-10-28-r50-avm-le-squashfs-core` in backticks, else B1 is red on its
second clause (`knowledge files not mapped in README Coverage map`).

**3. STRUCTURAL — already satisfied by the L1's in-flight bytes, confirmed independently.**
`tools/round-50/` must gain no `.py`/`.sh`: both frozen counters freeze that whole tree, so an
in-tree C3 instrument gives C1 `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']` → C1 exit 2
and C2 `frozen_path_changed` → C2 exit 2. The instrument is at `tools/round-50-c3/`
(`03f852b9`) — my independent measurement reached the same path from the counters' own
derivations. At the planned landing C1 `frozen_drift = []` and the B9 census is still **12**
paths, and the frozen `b9()` returns **0 findings** on the L1's actual `SKILL.md` worktree
bytes (7-cell row, one occurrence, 55-row region).

**The re-run command — `--battery` is required, not optional** (without it the defect in (1)
is invisible and the run reports green):

```
python3 -I -B tools/round-50/c2-record.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev <FINAL-REV> \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --battery \
  --work /fast/scratch/hyaku/kaidoku-r50/c2-w3 \
  --json-out .ufo/waves/round-50/l1/scores/c2-final-attempt2.json
```

Green = `atoms_total 11`, `mismatches 0`, `battery.failing []`, `battery.do_nothing_red` =
all 11 atoms, `exit 0`.

**Capstone:** the complete simulated attempt-2 landing (C3 instrument + registry row + SKILL
rule block 22 + C1 entry + PROVINCE section + README row + SOURCES S243/S244/S245/S249 +
coverage head `140/140` + attempt-2 section before the corrections section) scores **exit 0,
`mismatches 0`, 11/11 atoms green, `battery.failing []`** at that exact command.

**Also worth knowing:** B2 reads the Owned-axes **calibration** row, not the coverage row — it
requires `rejected-harmed`, the closure-48 path, the `c2-final.json` path and the literal
`mismatches 9 -> 0` (the numbers re-derived from the BASE round-49 receipts). Do not rewrite
that row. B6/B7/B8/B9 are structurally immune to the landing text.

Full report + receipts: `.ufo/waves/round-50/w3/ExecB1Impact.md` and
`.ufo/waves/round-50/w3/ExecB1Impact/`.
