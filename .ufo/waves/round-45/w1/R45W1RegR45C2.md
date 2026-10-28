# R45W1RegR45C2 — `tools/round-45/c2-counter.py` row, verified at the freeze

Round 45 wave 1, seat `R45W1RegR45C2`. Read-only on the lane tree. Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; graded tip `faa875bc0eb839d15b83c4afa6078819e5a7b381`.

Deliverables in this seat's directory: `row.md` (the exact 7-column row + per-cell
grounding) and `receipt.md` (commands, exits, sha256, UTC, attack matrix).

## Result

The frozen instrument is intact, self-tests green, reproduces both committed controls
byte-for-byte, and meets R45-C2 at `HEAD`. Six measured weaknesses sit around it; none
changes the target value, all are v2 material.

| check | value |
|---|---|
| frozen bytes | blob `7d83de62`, sha256 `50212d0f…`, 9560 B / 268 lines, unchanged at `HEAD` |
| selftest | exit 0, `cases=7 failures=0`; stdout sha `aea7e363…` **identical** to `controls/c2-selftest.txt` |
| do-nothing @ freeze | exit 1, `unregistered` = 6, `registered []`, `thin []`, `registry_rows 39`; my `--json-out` **byte-identical** to `controls/ctl-c2-0-do-nothing.json` |
| base arm | exit 2 `scope file absent at rev` — matches `controls/ctl-c2-0-base-unevaluable.json` |
| `HEAD` | exit 0, `registered` 6/6, `thin []`, `scope_size 6`, `registry_rows 45` |
| frozen-path arm | no commit in `FREEZE..HEAD` touches the claims file or `tools/round-45/` |
| row-set delta | 39 → 45, and the added set is **exactly** the six scope paths |

## The row

Exact 7 cells, first cell `` `tools/round-45/c2-counter.py` ``, exit cell naming `0`, `1`, `2`:

```markdown
| `tools/round-45/c2-counter.py` | gate — R45-C2 calibration: every scope instrument has a registry row with a real exit map | `0` met; `1` not met (`unregistered`, `thin` or `scope_size`); `2` could-not-evaluate, including `frozen_path_changed` | `python3 -I -B tools/round-45/c2-counter.py --selftest` — 7 cases, green at the freeze | `tools/round-45/registry-scope.json` and the `SKILL.md` registry rows | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | kaidoku |
```

Pinned inputs named: `tools/round-45/registry-scope.json` (6 paths, 6 unique, all present at
both revs, sha256 `6e2dda71…`) and the `SKILL.md` registry rows at `--rev` (`SKILL.md` is not
frozen). Self-test case count: **7** (`green`, `red-unregistered`, `red-wrong-path-rows`,
`red-thin-exit-cell`, `red-unknown-rev`, `red-frozen-touched`, `red-scope-size`).

The row is already landed at `SKILL.md:1641` (post-freeze `e715263c`) and is byte-identical
to this draft; re-landing is a no-op. It is retained so the L1 can diff for drift.

## Findings the L1 should reconcile

1. **"Registry row" is not enforced.** A six-row generic table under `## Decision log` with
   `0/1/2` in column 3 scores exit 0 with `registry_rows 6` and no registry heading anywhere
   (`A1`, sha `ee317443…`). The counter parses *any* markdown table row; it never locates a
   registry section or header. The claim's word "registry" is stronger than the instrument.
2. **No 7-column enforcement.** A 7-column header over 4-cell body rows passes (`A2`, sha
   `c37eea06…`). The 7-column shape is a drafting standard, not a counted clause — a row
   with no pinned/write-scope/owner cells still scores green.
3. **First-row-wins duplicates, both directions.** `by_tool.setdefault` keeps the first
   match: a thin row before a good one fails the run (`A3a`, exit 1) although a correct row
   exists; a thin row after a good one is silent (`A3b`, exit 0). Not in the selftest or the
   kill rule.
4. **Cell equality is substring equality.** First cell `` `path` (frozen instrument) ``
   registers (`A9`), where the claim says the first cell *is exactly* the path. Path equality
   proper holds — a path quoted in column 2 does not register (`A10`, exit 1).
5. **Ghost paths pass.** Rows for files that do not exist at `--rev` score 0 (`A4`). This is
   the disclosed limit routed as R45-CL2 in `SKILL.md`; my run confirms it is real and is the
   cheapest v2 clause (`git cat-file -e <rev>:<path>`).
6. **`exits_ok` is lexical.** `pinned at revisions `0`, `1`, `2`; verdict not stated` is not
   thin (`A5`). Digit adjacency is handled correctly: `1024` does not supply the `2` (`A11`,
   exit 1), so the exposure is prose-shaped, not numeric.

Minor: `--selftest` leaves an empty `$TMPDIR/kaidoku-r45/` parent; the path regex admits only
`.py`/`.sh`; `scope_size` counts list length, so a duplicated entry could mask a missing tool
(the frozen scope has 6 unique paths, all present).

## Calibration reading

The claim is *met* at `HEAD` and the improvement is real: the round moved six claim-carrying
instruments from zero registry rows to six exact-path rows with full verdict maps, and the
do-nothing control at the freeze proves the before-state. What the instrument does **not**
establish is that a row is in a registry, that a row is complete, or that the named tool
exists — three separate gaps, each measured above. So the calibration axis gained a
registry, not a registry *audit*; the difference is the honest scope of this round's C2.

## Retained evidence

- `row.md`, `receipt.md` in this directory.
- 16 runs, all matching expectation, each with command, exit, stdout sha256 and UTC in
  `receipt.md`. Lane-level: selftest 0, do-nothing 1, `HEAD` 0, base 2, reversed range 2.
- Committed-control equality: selftest stdout sha `aea7e363…`; do-nothing `--json-out`
  `diff`-identical (953 B, sha `f61c6b99…`); base arm reproduces the 102-byte control.
- Independent reimplementation (not the counter) agrees at both revs and confirms
  `SKILL.md:1636-1641`, all 7 cells, header `:1634-1635` 7 cells, one row per scope path.
- Separability: frozen source has zero occurrences of `Queue-drain`, `block22`,
  `rule_blocks`, `S140`, `preflight`; the claims file is a pathspec only (`:28-30`).
- Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45C2` removed after copying receipts.

## Risks / blockers

- None blocking. Risk the L1 should weigh: if a future round satisfies C2 by adding rows to a
  non-registry table, the counter will not object (finding 1). The claim text and the
  instrument should be tightened together in v2, not the row.
- Not measured (and not asserted): corrupted object store, unwritable `--json-out`, shallow
  clone missing the freeze.
- No installs, no network, no package transactions; no mutating git command outside throwaway
  fixtures; lane tree untouched.
