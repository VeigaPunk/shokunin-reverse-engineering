# CriticClaims — scoped findings, round 66 w1

Seat: critic (claim attacks). Inputs pinned and verified: both counters and both control scripts
match `claims.json`; freeze `7b63dd5d` adds `claims.json`; `78fa9666` and `b5b02e1f` are ancestors.
Detail per attack with commands, exits and diff hunks: `w1/CriticClaims/attacks.md`; receipts under
`w1/CriticClaims/evidence/` (SHA-256 manifest in `evidence/sha256.txt`).

## Verdicts

| claim | clause attacked | verdict |
|---|---|---|
| R66-C1 | a2 (ordering witness) | **counter fails as a witness** — two counters without an ordered post-probe check score 5/5 exit 0 |
| R66-C1 | a5 (`--skip-run`) | **counter fails** — a5 is a literal self-assertion, blind to the emitted JSON |
| R66-C1 | a1 count clause | vacuous (`entries` and `expected_count` derive from the same constant) |
| R66-C2 | `recipe_a_equivalent` | **holds at base and freeze** (landing unmeasured); latent closed-world tolerance named |
| R66-C2 | row atoms | **counter fails** — `mismatches 0` reachable with the stale `142/142` still in the row |
| R66-C2 | base arm | **holds** — A2 false `142/142` vs `145/145`, exit 1, both atoms parsed |

The frozen instruments themselves behave as claimed: `closure-boundary.py --verify` is 5/5 exit 0 at
HEAD (`evidence/frozen-verify.json`); `coverage-selfcheck.py --selfcheck --rev <base>` is exit 1,
mismatches 1, A1 true, A2 false `[142,142]`→`[145,145]`, equivalence true, hidden 3
(`evidence/E-selfcheck-base.json`). No counter is broken on its own stated target.

## What fails

1. **C1 a2 is not a provenance test.** Patch the a2 fixture so the probe runs *guarded* and the
   `.pyc` is planted before a pre-probe scan (`S_A1`), or so the probe wrapper manufactures the
   cache (`S_A2`): both pass 5/5 exit 0. `S_A2`'s a2 detail is **dict-equal** to the frozen
   receipt's. The arm named `a2-unguarded-fixture-red` is green for a counter whose probe ran
   **with `-B`** — the predicate's own words. The counter that ships does implement the ordering;
   the receipt cannot show it. → `evidence/S_A1.diff`, `S_A2.diff`, `S_A1-verify.json`,
   `S_A2-verify.json`.
2. **C1 a5 tests a constant.** `skip_run_receipt` returns `closure: None, closure_claimed: False`;
   the arm compares that to itself. A counter whose `main --skip-run` branch emits
   `{"closure": {"ok": true}, "closure_claimed": true}` still passes a5 and `--verify` 5/5
   (`S_B`). That is Q5 re-opened at the CLI boundary while the arm stays green. Separately,
   `closure_state` with `manifest={}` and `expected_count=3` returns `ok true, count_ok true,
   entries 3` — a green closure over zero verified entries.
3. **C2 atoms accept an unrepaired row.** In a fixture repo (149 files from HEAD), the row
   `| coverage | 9.72 → 10.0 | 145/145 knowledge files mapped at the landing; the round-53 142/142
   knowledge files receipt is retained | … |` scores exit 0, mismatches 0
   (`D-R2-correct-first-stale-later.json`), and `| coverage | 9.79 → 9.72 → 10.0 | 145/145 … |`
   scores 0 too (`D-R4…`). `parse_row` reads the **first** `n/m knowledge files` and the **last**
   arrow's number. Stale-first order (`D-R3`), a wrong fraction, and a missing fraction (exit 2, no
   receipt) are caught — so the escape needs the true value first, which is precisely the shape the
   existing row's prose invites.

## What holds

* **C2 equivalence** is exact at base and HEAD: the committed block emits exactly the nine
  `RECIPE_A_KEYS`, `diffs {}`, `equivalent true` (`C-equiv-head.json`). No key outside the tuple
  exists today. The comparison is closed-world, though: injecting a tenth block key `policy` leaves
  `equivalent true` (diffs `[]`), while `mapped + 1` is caught. Consequence if a later block adds a
  field: silent agreement on a field `--recipe a` never emits. `recipe_a_block_keys` in the receipt
  is the only tell.
* **C2 base arm** is honest for the stated reason: A2 false on claimed `[142,142]` vs observed
  `[145,145]`, A1 true, `parse_row` succeeded (atoms emitted), exit 1 — not a parse failure (which
  exits 2 and writes nothing).

## Impacted axes

* depth (R66-C1): the claim's stated number (5/5) is true, but the arm set does not establish the
  C1-F1 ordering repair; the depth inference is unsupported by the receipt.
* calibration (R66-C2): the base arm and equivalence are sound; the after-arm's "row repaired"
  cannot be certified by `mismatches 0` alone — the landed row text needs a human read.

## Smallest safe corrections (routed as defects; no frozen byte touched)

* a2: require `cache_before == []`, record the probe argv/env in the detail, and add the
  discriminating mutant *guarded probe + planted `.pyc` must leave a2 false* to `--selftest`.
* a5: assert on the **emitted** `--skip-run` object (subprocess or captured `emit`), not on the
  literal returned by `skip_run_receipt`; a1: drop or externally fix the count clause.
* `--selfcheck`: A2 must require every `n/m knowledge files` occurrence in the row to equal stem
  (or exactly one occurrence); A1 must require exactly one arrow or validate every segment.
* `--equiv`: make `set(theirs) - set(RECIPE_A_KEYS)` a diff/finding.

No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/kaidoku-r66/CriticClaims` (variants,
fixture repo, work dirs) was deleted before yield; `evidence/` is the only retained copy.
