# ExecCaseInventory — round 79, case inventory across base and freeze

Seat scope: name-level inventory of the round-78 gate's `--selftest` cases at the two measured
revisions, the added/removed delta, the exercised code path for each added case, and duplicate
detection. No lane production file was edited; every write is under
`.ufo/waves/round-79/w1/ExecCaseInventory/` (receipts) and this report.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Base rev: `29d2ca30b83a6a0d85b0aa979de0138fde1660e6`
- Freeze rev: `ed68cd0a6cc790cca342380a2d80d1927a668c8c`
- Instrument: `tools/round-78/attack-gate.py`
  - base sha256 `961d5a23c1d38116f5b992434fa2295b5a90643b4a52233e205837ac73bf48c0` (949 lines)
  - freeze sha256 `4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf` (974 lines)

## Method

At each rev the blob is materialized into scratch and run; the lane is never modified:

```
git -C <lane> show <rev>:tools/round-78/attack-gate.py > $S/attack-gate-<rev>.py
TMPDIR=$S python3 $S/attack-gate-<rev>.py --selftest
```

Case list = the JSON lines keyed `case`; counts come from the single `SELFTEST cases=N failures=M`
summary line each run emits. `names_digest` = sha256 of the case names sorted and joined with
`\n`, no trailing newline (an emitted-order digest is also recorded in the receipt so the
convention can be checked either way). The scratch copy reproduces the landed receipt: the freeze
copy's output is byte-identical to `.ufo/waves/round-79/pre/selftest-gate.txt`, and the same
output is produced with cwd set to the scratch dir (the selftest is cwd-independent).

## Counts

| rev | cases | failures | summary line | names_digest |
|---|---|---|---|---|
| base `29d2ca30` | 26 | 0 | `SELFTEST cases=26 failures=0` | `414548210c6dceeb50572e87862769e28d4b721db9552f329161f5eb3ec6d92b` |
| freeze `ed68cd0a` | 29 | 0 | `SELFTEST cases=29 failures=0` | `10f3402d2a495c0c025afa5451fa307808c0a56ccd032984133b1e8fe4a1afe8` |

Count moves 26 -> 29 (+3), 0 failures at both. The base list is an exact prefix of the freeze
list (`fn[:26] == bn`): nothing was removed, renamed or reordered, so "nothing else lost" holds
by identity, not just by count.

## Added / removed / duplicates

- added (3, in emission order): `red-near-miss-unparsed`, `red-atom-absent`,
  `red-validate-refused-no-reason`
  - these are exactly the three names the claim freezes
    (`plans/round-79-claims.md`, and `declared_case` rows in `tools/round-79/gate-mutation.py`).
- removed (0).
- duplicates: none at base (`sort | uniq -d` -> 0 lines), none at freeze (0 lines). The gate
  itself only appends to `cases`, so a duplicate name can only arrive by a copied `case(...)`
  call; none is present.
- The three added names do not occur at base in the instrument's selftest output (`grep -c` = 0
  each), i.e. the cases are new detectors, not renames.

## Case -> exercised path (file:line at the freeze)

The round-79 delta is 25 added lines, all inside `selftest()`; the three code paths pre-exist at
base at the same line numbers. Each entry below was confirmed by ablation: a single exact
single-occurrence edit to that branch in a scratch copy of the freeze instrument, then
`--selftest`; the declared case is the sole failing case and the run exits 1 with 29 cases.

| case | function | path:line (freeze) | branch |
|---|---|---|---|
| `red-near-miss-unparsed` | `judge_group` | `tools/round-78/attack-gate.py:394` | `near is None and NEAR_MISS_RE.match(clause)` -> emits `near_miss_field` for a verdict token the grammar cannot parse (`"mismatch abc"`) |
| `red-atom-absent` | `bind_clause` | `tools/round-78/attack-gate.py:311` | `kind == "field"`, `ATOM_ID_RE.match(field)`, `receipt["atoms"]` not a list -> `(False, "defect", {"reason": "no_atoms", ...})` |
| `red-validate-refused-no-reason` | `validate_receipt` | `tools/round-78/attack-gate.py:794` | `fixture["refused"] and not fixture["reasons"]` -> defect `"<id>: refused without a reason"` |

Ablation detail (scratch only; the mutants are attribution probes, not the frozen R79-C1
battery):

| ablation (single edit) | cases | failures | sole failing case | exit |
|---|---|---|---|---|
| `NEAR_MISS_RE` cannot match (`\s+ZZZ$`) | 29 | 1 | `red-near-miss-unparsed` | 1 |
| atom-absent return flipped to `"bound"` | 29 | 1 | `red-atom-absent` | 1 |
| refusal-guard `defects.append(...)` removed | 29 | 1 | `red-validate-refused-no-reason` | 1 |

The pristine freeze instrument is 29 cases / 0 failures; each ablation leaves exactly one red
case and no other case flips, so the mapping case -> path is one-to-one in both directions for
these three branches.

## Evidence retained

`.ufo/waves/round-79/w1/ExecCaseInventory/`:

- `inventory.json` — the receipt: `base`/`freeze` (rev, instrument sha256, cases, failures,
  summary line, names digest, names), `added`, `removed`, `duplicates`, `case_to_path`,
  `ablation`, plus the invariants (base-prefix, cwd independence, landing-receipt identity).
- `base-selftest.out`, `freeze-selftest.out`, `freeze-selftest-cwdscratch.out` — raw selftest
  output at each rev (the last proves cwd independence).
- `ablate.py`, `ablation.json` — the ablation driver and its result table.
- `build_receipt.py` — the receipt generator (digests, counts, prefix and duplicate checks).
- `gate.diff` — base -> freeze diff of the instrument (25 lines added, all in `selftest()`).
- `mutants.diff` — the three single-edit ablation diffs.

## Risks / limits

- `names_digest` is only meaningful together with its stated convention (sorted, `\n`-joined, no
  trailing newline); the emitted-order digest is retained alongside it to remove the ambiguity.
- The ablation here is path attribution for the inventory; the frozen R79-C1 kill decision must
  still come from `tools/round-79/gate-mutation.py --battery` and its receipt, which this seat
  does not run or substitute for.
- The landing receipt `pre/selftest-gate.txt` is byte-identical to the freeze instrument's
  selftest output measured here, so its 29/0 figure is independently re-derived, but the receipt
  remains unclaimed per the frozen disposition.
