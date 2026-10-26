# R36W2MutantC2Landed — mutation probes on the landed C2 surfaces (round 36, wave 2)

Seat: R36W2MutantC2Landed (leaf, no subagents). Date: 2026-10-26.
Scope: falsify the landed R36-C2 calibration surface (SCORECARD.md / SHONEN.md) at integration tip
`01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` by single mutations, scored with the frozen counter
`tools/round-36/c2-counter.py` (unchanged; selftest 13/13, exit 0) against base
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`. Lane untouched except this report file.

## Verdict summary

| probe | mutation | verdict |
|---|---|---|
| M1 | coverage count `124/124` → `123/124` (SCORECARD.md:23) | **killed** (O1) |
| M2 | craft range `SKILL.md:81-314` → `81-315` (SCORECARD.md:24 depth row) | **killed** (R1) |
| M3 | restore base shorthand `` `receipts-B/` `` in capability row (SCORECARD.md:619) | **killed** (unresolved + unrepaired guard) |
| M4 | duplicate coverage row with `116/116`, appended **after** the correct row | **killed** (O1) |
| M4b | same stale `116/116` row inserted **before** the correct row (shadowed) | **SURVIVED** |
| M5 | SHONEN box 4 `` `PROVINCE.md:97-125` `` → `` `PROVINCE.md:97-118` `` | **killed** (R3) |
| M6 | delete the new round-36 capability row `REA SquashFS recursion through sasquatch (LE v4)` (SCORECARD.md:627) | **SURVIVED** |
| M7 | add pointer to non-existent file `` `corpus/evidence/round-36/c2/after-at-01a44db.json` `` into that row | **killed** (unresolved) |

6 killed, 2 survived, 0 inconclusive. Baseline (pristine fixture) scored green before any mutation:
`met_target: true, mismatches: 0, exit 0` — so no verdict above rests on a broken baseline.

## Fixture and scoring mechanics

- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2MutantC2Landed`, `TMPDIR=$S`; removed at end.
- Fixture repo `D=$S/fx.PJ92`, created `mktemp -d "$S/fx.XXXX"` + `git -C "$D" init -q` per tasking.
  - Base: `git -C <lane> archive cab59f221… | tar -x -C "$D"`, `git add -A`, `write-tree` →
    `d127d86a58ef92595928ef40eb9e17b608c6c03d` = `git -C <lane> rev-parse cab59f221…^{tree}` (equal).
    The base commit object was then planted byte-exactly: `git -C <lane> cat-file commit cab59f221…`
    piped to `git -C "$D" hash-object -t commit -w --stdin` → **`cab59f221fe19726b5692bfa4d9a9679e96b8a73`**
    (identical bytes ⇒ identical sha), so the frozen counter resolves the literal base sha in the fixture.
  - Tip: worktree swapped (`git rm -rfq -- .`, `git -C <lane> archive 01a44db… | tar -x`), `write-tree` →
    `3faa331840168ccec9c4c7a64a81f05e083f4a51` = `01a44db…^{tree}` (equal); committed as
    `1182d5dd9fc5b3789987b285fa5f2ac22af36e1b` (parent = planted base). The fixture tip commit sha
    differs from `01a44db…` only because author/committer differ; tree and blob content are identical —
    pristine `SCORECARD.md` sha256 `6c36002a5cd92279b8124cac1bfa55aac882b17b7023343f53bf1181e225d250`
    and `SHONEN.md` sha256 `51c55a9479a59ac6365d0f47961969966e2a2565389e58a3e38080d9c1959dc1` equal the
    lane-tip blobs (`git show 01a44db…:<file> | sha256sum`, both equal).
- No `.gitattributes` at tip (`git cat-file -e 01a44db…:.gitattributes` → absent), so `git archive`
  reproduces the exact trees.
- Scoring command per mutant (counter file run in place from the lane, never copied or edited):
  `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-36/c2-counter.py --root "$D" --rev <MUTANT_SHA> --base cab59f221fe19726b5692bfa4d9a9679e96b8a73 --json-out <receipt>`
- Baseline observed values (from the pristine receipt): command A `mapped 124, knowledge_files 124,
  resolved_rules 17, rule_blocks 17`; command B `[9, 9]`; `craft_range [81, 314]`;
  `adjacent_range [97, 125]`; pointers 41 (base 34); base unresolved pointers
  `receipts-B` (cap row) and `ScoutSkillPlacement.md` (SHONEN box 4) — matching
  `plans/round-36-claims.md` ("3 mismatches" = those two + the 116/116 count).
- Lane git usage (all read-only): `rev-parse`, `cat-file -e`, `cat-file commit`, `archive`, `show`,
  `status`. No add/commit/checkout/reset/stash/pull/push in the lane; no jj. All commits happened in
  the fixture only. No tools installed (operator tooling authorization unused; REA not invoked —
  probes need only the frozen counter).

## Killed mutants (actual counter stdout, exit code)

- **M1** — commit `ca7ee6e3bfdd7c8be0302755d5e08194f9932e85`, exit 1:
  `{"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [124, 124], "stated": [123, 124]}], "guards_ok": true, "met_target": false, "mismatches": 1, "unresolved": []}`
- **M2** — commit `6e5a010c42e0162ca678a84c19ce5300fa13a2bb`, exit 1:
  `{"assertion_mismatches": [{"check": "R1 depth row craft range", "observed": [81, 314], "stated": [81, 315]}], "guards_ok": true, "met_target": false, "mismatches": 1, "unresolved": []}`
- **M3** — commit `0d4acc45be6f700b3366bb401dcecb1b068849ce`, exit 1:
  `{"assertion_mismatches": [], "guards_ok": false, "met_target": false, "mismatches": 1, "unresolved": [["cap:pre-registered two-lane live battery on REA 6.5.0", "receipts-B/"]]}` — killed twice over: the pointer is unresolved AND the repair guard flags `unrepaired: [["cap:pre-registered two-lane live battery on REA 6.5.0", "receipts-B"]]` (no resolving pointer to the same document remains in that unit).
- **M4** — commit `257cbf53907824a58f20c703bf35df186b7e8d3a`, exit 1:
  `{"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [124, 124], "stated": [116, 116]}], "guards_ok": true, "met_target": false, "mismatches": 1, "unresolved": []}` — the counter's unit dict is last-wins, so a stale duplicate appended after the correct row *becomes* the read row and is caught.
- **M5** — commit `f3f9281c1c2fd097ff671b7a35da33616fa73107`, exit 1:
  `{"assertion_mismatches": [{"check": "R3 SHONEN box4 Adjacent range", "observed": [97, 125], "stated": [97, 118]}], "guards_ok": true, "met_target": false, "mismatches": 1, "unresolved": []}`
- **M7** — commit `7b9213156eb1fcdaf140ceb275ced29af2ffb9dd`, exit 1:
  `{"assertion_mismatches": [], "guards_ok": true, "met_target": false, "mismatches": 1, "unresolved": [["cap:REA SquashFS recursion through sasquatch (LE v4)", "corpus/evidence/round-36/c2/after-at-01a44db.json"]]}` (path verified absent at tip before use: `git cat-file -e` fails; `corpus/evidence/round-36/` contains only `c1`).

## Survivors — coverage findings on the frozen counter

### M4b — stale duplicate row shadowed by the correct row (commit `46b3eb43cc02d09ee8b47d8748b70bf45632c67e`, exit 0)

Mutation: the tip coverage row duplicated verbatim except `124/124` → `116/116`, inserted on the line
**before** the correct row in `## Owned axes`. Counter output (full receipt):

```
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "pointers": 41, "unresolved": []}
```

The repo's `## Owned axes` table visibly contains a coverage row claiming
`116/116 knowledge files mapped after the round-36 landing` — false against observed 124/124 — and the
frozen counter reports zero mismatches. Mechanism (counter source, `units()`): units are keyed by
first cell (`owned:coverage`) and each row **overwrites** the previous value, so only the last row per
key is ever read or scanned; the shadowed stale row contributes nothing — the receipt even shows
`pointers: 41`, identical to the pristine tip, proving the stale row's text was never scanned.
This is lesson M36-3 / wave-1 `R36CriticC2Shortcut.md` class A1, reproduced at the landed tip.
Direction asymmetry is diagnostic: appended-after is caught (M4), inserted-before is not (M4b) —
detection depends on row order, not on the presence of a wrong statement. **A miscalibrated state
passes**: any future edit that leaves a wrong count/range/pointer in a non-last row of the same unit
key scores green. The lesson's mitigation (QUALITY 77; "the round's C2 verdict is re-derived by a
stricter non-counter check in wave 2 instead of being cited alone") is load-bearing for exactly this
class; the counter alone cannot carry it.

### M6 — deletion of the round-36 capability row (commit `d746df6a0546b7dc359d97a3071d9f0f00da929c`, exit 0)

Mutation: the entire new capability row
`| REA SquashFS recursion through sasquatch (LE v4) | … | corpus/evidence/round-36/c1/; tools/round-36/c1-run.sh; corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md | round-36 |`
(SCORECARD.md:627) deleted. Counter output (full receipt):

```
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "pointers": 38, "unresolved": []}
```

Guards why-pass (from the receipt): `missing_units: []` — the row does not exist at base, so its
deletion cannot register as a missing unit; `pointers_not_fewer: true` — the global pointer floor
compares 38 (mutant) ≥ 34 (base). The row carried 3 backticked pointers (tip total 41 → 38), and the
floor had 7 pointers of slack (41 − 34), so 4 pointers of slack remained after the deletion.
**A miscalibrated state passes**: the lane can silently drop its newest capability claim — the
self-assessment no longer states the sasquatch capability that C1 landed — and P36-C2 still reports
zero mismatches. The population guard protects base-era units and a blunt pointer floor, not
round-added rows. (Boundary: a row carrying ≥ 8 pointers would trip the floor; this row carries 3.)

## Restoration evidence

Per probe: mutated file sha256 (16-char prefix) recorded; after scoring, `git -C "$D" reset -q --hard`
to the fixture tip; the counter was re-run on the restored bytes (exit 0 every time) and
`git rev-parse HEAD^{tree}` re-checked = `3faa331840168ccec9c4c7a64a81f05e083f4a51` after every probe.

| probe | file | mutated sha256 (prefix) | restored sha256 (prefix) |
|---|---|---|---|
| M1 | SCORECARD.md | `d51b2e51f9bb1d1a` | `6c36002a5cd92279` |
| M2 | SCORECARD.md | `33b33edc642ba541` | `6c36002a5cd92279` |
| M3 | SCORECARD.md | `abc1d617999d5a79` | `6c36002a5cd92279` |
| M4 | SCORECARD.md | `0b557ac2307ebd74` | `6c36002a5cd92279` |
| M4b | SCORECARD.md | `fb4153f63c8189f9` | `6c36002a5cd92279` |
| M5 | SHONEN.md | `47eb4fac949fec50` | `51c55a9479a59ac6` |
| M6 | SCORECARD.md | `23f9f12858b6966f` | `6c36002a5cd92279` |
| M7 | SCORECARD.md | `5f1bda781b0890dd` | `6c36002a5cd92279` |

Restored hashes equal the pristine lane-tip blob hashes (full hashes above). Final pristine re-run:
`met_target: true, mismatches: 0, exit 0`. Fixture scratch removed after the report was written.

## What this means for the landing

- The landed C2 state itself is real: the pristine tip scores `met_target` with the frozen counter,
  and every single-point defect I injected into the *read* units (M1, M2, M3, M4, M5, M7) is killed.
- The two survivors are counter blind spots, not defects in the landed bytes: (a) stale statements
  shadowed by a later same-key row (M36-3/A1, order-dependent detection), and (b) silent deletion of
  round-added capability rows (population guard is base-keyed + pointer-floor only). Both would let a
  miscalibrated self-assessment pass P36-C2; the wave-2 stricter non-counter re-derivation is what
  covers them. No counter change is proposed here (frozen); these are coverage findings for the
  round's verdict wording and for future counter designs (enumerate all occurrences per unit key;
  guard round-added units by identity, not by a global pointer floor).
