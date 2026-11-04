# ExecC1 — R69-C1 independent re-derivation (executor, r69 / w1 / attempt 1)

**Verdict: R69-C1 holds at the freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`.** I re-derived it with
my own patch applier (`mutapply.py`, no code shared with `mutation-check.py`) and the sentence's five
clauses all read true. The frozen battery's receipt is corroborated on every field it reports — not
trusted. Detail, exact patch text and every rc/failed list: `.ufo/waves/round-69/w1/ExecC1/rederive.md`.

## Measured objects (all read from git, never written)

| object | sha256 | pin | match |
|---|---|---|---|
| `f159981:tools/round-69/packed-elf.py` | `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` | `instrument_pins` | yes |
| `d7d9a62:tools/round-68/packed-elf.py` | `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e` | `c1-at-base.json.target_sha256` | yes |
| same file at `f159981` | `48ef4c68…` (identical to base) | — | yes |
| `f159981:tools/round-69/mutation-check.py` (cross-check only) | `51b64c56c48899d5d2d707298431861f8465e5422e53ee7dceb903d1b56d33c2` | `instrument_pins` | yes |

`git diff f159981..HEAD -- tools/round-69/packed-elf.py` → empty (no post-freeze edit).
`git cat-file -e d7d9a62:tools/round-69/packed-elf.py` → rc 128 (the after-arm has no base object; the
before-arm must be the r68 file, as the sentence says).

## Results

Two mutant families per blob, so the outcome cannot rest on the battery's mutant strength:
**constant** (every arm expression → `True`, the strongest blind gate) and **literal** (the battery's
own patch text, re-typed and match-counted independently).

| run | pristine | M1 identity | M2 recovery | M3 detected | M4 before | M5 control | survivors |
|---|---|---|---|---|---|---|---|
| r69 constant | 20 cases, ok | killed → `arm-pack-identity-false` | killed → `arm-pack-recovery-false` | killed → `arm-pack-detected-false` | killed → `arm-pack-before-false` | killed → `arm-pack-control-false` | `[]` |
| r69 literal | 20 cases, ok | same | same | same | same | same | `[]` |
| r68 constant | 13 cases, ok | survived | survived | survived | survived | survived | all five |
| r68 literal | 13 cases, ok | survived | survived | survived | survived | survived | all five |

Every r69 kill has `failed` equal to exactly its declared case — no collateral case fails, so each arm
is bound one-case-per-arm. Every patch site matched exactly once. A crash (unparsable selftest output)
is classified unevaluable, never a kill. Two pristine repeats per blob are byte-identical (deterministic).

Cross-corroboration: my r68 constant M1/M5 mutant shas (`85d34a25…`, `0c501fa8…`) and literal
M2/M4/M5 shas (`855dbb26…`, `541311a1…`, `0c501fa8…`) equal the shas in
`.ufo/waves/round-68/w1/MutPacked/mutants.md`; my r68 shas of pristine are `48ef4c68…`.

## Battery cross-check (run for comparison only, at the freeze, in scratch)

Battery r69 arm: `ok true`, `survivors []`, five `killed`, `killed_wrong_case []`, `pristine.cases 20`
`ok`, `target_sha256 4ac0d83b…` → **identical** to my derivation. Battery r68 arm: `ok true`,
survivors the five, `pristine.cases 13`, `target_sha256 48ef4c68…` → **identical** to my derivation and
to `.ufo/waves/round-69/l1/pre/c1-at-base.json` on every shared field. **Mismatches: none.**

## Observations beyond the predicate (report-only; no claim change proposed)

1. **The selftest is bound to the seam and to its registry, not just to five expressions.** Probe
   mutants: hard-wiring `evaluate_carrier`'s `ok` → `True` kills all five arm cases;
   `matched = len(carriers)` kills `fold-not-met`; `section_count` → `return 0` kills `sections-some`;
   deleting an `arm-pack-*` case kills `case-inventory`; unwiring `control_ok` at the `carrier_arms`
   call kills `arm-pack-control-false`.
2. **One weak shape:** removing the refusal evaluation (`if model.get("address")` → never) is caught
   only as `KeyError: 'refusal_ok'` inside the case → `failed` is unparsable, i.e. a battery would say
   `killed_wrong_case`. Still non-zero, but not an arm-false case that names its arm. Not reachable
   from the five declared sites.
3. **r68 has a dead store:** line 277 `control_ok = ctrl_l["rc"] != 0 and ctrl_d["rc"] != 0` is never
   read (fold uses the inline `all(...)`); patching it to `True` survives 13/13. That explains why the
   round-68 M5 had to target the `fold()` call. r69's `control_ok` is live (proved by the unwiring
   probe).
4. **The r69 patch set's M2/M4 are weaker than r68's** (drop one conjunct / drop the equality instead
   of a self-compare). The declaration's "the same five patches" is true of the *sites*, not of the
   mutant text. The constant-`True` family kills all five anyway, so the weaker literal mutants are not
   manufacturing the kills. Prose note only — the frozen predicate only names patch set `r69`.
5. **Causality link:** `score()` calls `evaluate_carrier(model)` at line 427 and feeds all 16 keys the
   seam reads (AST check, `unfed = []`), so the seam the selftest binds is the seam production scores.

## Risks / caveats

* "Run at the measured revision" (atom A9 = the landing commit) is not yet available at the freeze. The
  derivation is over committed bytes at the freeze; freeze blob, worktree file and pin all equal
  `4ac0d83b…`, so the sentence holds for any landing commit carrying those bytes. It would *not* hold
  if the landing touched an instrument (A1 forbids that) — inference, contingent, not observed.
* An after-arm receipt produced by the battery is corroborated but not evidence on its own; this seat's
  evidence is `mutapply.py` plus the twelve receipts listed below.
* Nothing here touches R69-C2 or R69-C3; each claim is scored by its own instrument.

## Files written (all inside the wave dir)

`ExecC1/rederive.md` (full derivation), `ExecC1/mutapply.py` (the applier),
`ExecC1/receipts/` — `r69-constant.json`, `r69-literal.json`, `r68-constant.json`, `r68-literal.json`,
`r69-extra.json`, `r68-extra.json`, `battery-r69.json`, `battery-r68.json`, `det-r69-{1,2}.json`,
`det-r68-{1,2}.json`, `mutants-r69-constant/` (five mutants + pristine),
`mutants-r68-constant/` (five mutants + pristine), `MANIFEST.sha256` (26 files, `sha256sum -c` clean
from the wave dir).

## Housekeeping

* Scratch `/fast/scratch/hyaku/kaidoku-r69/ExecC1/` created, used, deleted before yield; receipts
  copied out first.
* No tool installed or upgraded (no uv/npx/pacman/release binary was needed); no pacman transaction.
* No tracked lane file, fleet file, other lane, or jj/git index touched; no commit, no push.
  `git status --porcelain -- tools/round-69 tools/round-68` in the lane is empty.
* No subagent dispatched, no labrat probe needed, no background job.

Report: .ufo/waves/round-69/w1/ExecC1.md
