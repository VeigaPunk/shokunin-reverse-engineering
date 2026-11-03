# MutCoverage — R65-C2 instrument mutation probes

Seat: MutCoverage (leaf). Wave: round-65 w1, attempt 1.
Base revision: `c99e907cb5576c13a7b22755d776b356fdfc1752`.
Instrument under test (frozen, never edited):
`tools/round-65/coverage-recipe.py`, sha256
`9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6`
(re-checked after the whole pass: unchanged; `git -C <repo> status --porcelain -- tools/round-65/` empty).
All work on copies under `/fast/scratch/hyaku/kaidoku-r65/MutCoverage/`.

## Detector (same three commands for pristine and every mutant)

```
M=<copy dir>/coverage-recipe.py
PYTHONDONTWRITEBYTECODE=1 python3 -B $M --selftest
PYTHONDONTWRITEBYTECODE=1 python3 -B $M --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev c99e907cb5576c13a7b22755d776b356fdfc1752 --recipe stem --out <copy>/stem.json
PYTHONDONTWRITEBYTECODE=1 python3 -B $M --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev c99e907cb5576c13a7b22755d776b356fdfc1752 --recipe date --out <copy>/date.json
```

Verdict rule: **killed** iff any detector diverges from pristine (selftest exit != 0 or any
`FAIL` line, or either CLI arm's exit code or JSON dict differs); otherwise **survived**.
Mutant construction: `cp` pristine bytes, one textual replacement, assert
`src.count(old) == 1` and mutated bytes != pristine bytes (assertions in `drive.py`).

## Pristine baseline ("before", exit 0 selftest)

| arm | exit | knowledge_files | population | mapped | missing | dangling | population_dropped | mismatches |
|---|---|---|---|---|---|---|---|---|
| selftest | 0 | — | — | — | — | — | — | `SELFTEST CLEAN cases=28 failures=0` |
| stem | 0 | 144 | 144 | 144 | [] | [] | 0 | 0 |
| date | 1 | 144 | 142 | 142 | [] | [] | 2 | 2 |

This is exactly the R65-C2 predicate shape at the measured revision: stem clean with
`mapped > 0`, date non-zero `population_dropped`.

## Mutants

| id | change (pristine -> mutant) | exit selftest / stem / date | verdict | detected by |
|---|---|---|---|---|
| M1 | `        population = list(files)` -> `        population = [f for f in files if DATE_TOKEN_RE.match(f)]` (stem recipe re-applies the date filter to the denominator) | 1 / 1 / 1 | **killed** | selftest (8 FAIL), cli-stem |
| M2 | `    missing = sorted(set(population) - token_set)` -> `    missing = []` | 1 / 0 / 1 | **killed** | selftest (3 FAIL) only |
| M3 | `    dangling = sorted(claimed - set(files))` -> `    dangling = []` | 1 / 0 / 1 | **killed** | selftest (4 FAIL) only |
| M4 | `    if result["mapped"] == 0 and result["population"] == 0:` / `        return 2` -> `        return 0` (empty population is clean) | 1 / 0 / 1 | **killed** | selftest (1 FAIL: `empty-exit`) only |
| M5 | `            if not CLAIM_RE.match(norm):` -> `            if not CLAIM_RE.match(raw):` (CLAIM filter sees the un-normalized token) | 1 / 1 / 1 | **killed** | selftest (11 FAIL), cli-stem, cli-date |
| M6 | `    dropped = len(files) - len(population)` -> `    dropped = 0` | 1 / 0 / 0 | **killed** | selftest (4 FAIL), cli-date |

Mutant sha256 (pristine is `9434888e...` for all six "before"):
M1 `026e816d3dbb45730c3e3f6339192199f71de2b64f0c8c8a0809105c3777f67f`,
M2 `dded83d23b5e86e608dd4df812cd7e2f9bdfd1ba404818318b8bc2bd9292cd01`,
M3 `2b63e7df21073cb63f6621077d14e44d6db445eabc15ea45973247e3cad8caeb`,
M4 `4d2d1c374da7ac250a65367f872a571ade0994fe9eff1e81703465a71b5b0c28`,
M5 `437e3ea355042629ffcef7017900fef0a33fe235b3c03e9010d3a14c128c97ed`,
M6 `568a0eacbf9912fb65414d89b46cdb54b97a1dc4afa8c3dafce6baca7529a9ed`.

## Per-mutant "after" CLI evidence

M1 (defect restored under `stem`): stem exit 0 -> 1, population 144 -> 142,
population_dropped 0 -> 2, mismatches 0 -> 2, mapped stays 142; date arm unchanged.
selftest FAILs: `stem-mapped`, `stem-mismatches`, `stem-exit`, `stem-one-missing-count`,
`limit-nondated-removal-clean`, `stem-dangling-count`, `nomap-unmapped`, `base-stem-clean`.

M2: both CLI arms byte-identical to pristine (at this revision `missing` is already `[]` in
both arms), so the CLI cannot see it; selftest FAILs `stem-one-missing`,
`stem-one-missing-count`, `nomap-unmapped`.

M3: both CLI arms byte-identical to pristine (`dangling` is already `[]` in both arms);
selftest FAILs `removed-dated-dangles`, `stem-dangling-named`, `stem-dangling-count`,
`stem-dangling-exit`.

M4: both CLI arms byte-identical to pristine (neither arm has an empty population at this
revision); selftest FAILs `empty-exit` (expected 2, got 0).

M5: stem exit 0 -> 1, mapped 144 -> 109, mismatches 0 -> 35; date mapped 142 -> 107,
mismatches 2 -> 37. The raw-form CLAIM filter rejects 184 of 407 backticked tokens in the
`## Coverage map` section, including 36 distinct `knowledge/`-prefixed norms; 35 distinct
norms are lost from `token_set` because `2026-10-19-arc3-r10-rust-evidence-id-domain` also
appears as a bare passing token. selftest FAILs include `token-count`, `token-normalized`,
`stem-mapped`, `stem-missing`, `stem-mismatches`, `stem-exit`, `date-mismatches`.

M6: date exit 1 -> 0, population_dropped 2 -> 0, mismatches 2 -> 0 (the date arm now prints
the same perfect score the round-64 defect produced); stem arm unchanged. selftest FAILs
`date-dropped`, `date-mismatches`, `date-exit`, `base-date-reproduces`.

## Coverage observations (no survivor; instrument weakness, not contract change)

1. At `c99e907...` the two CLI arms already report `missing == []` and `dangling == []`, and
   neither has an empty population. M2, M3 and M4 are therefore invisible to the CLI and are
   caught only by `--selftest`. The `missing`, `dangling` and could-not-evaluate halves of
   the instrument are load-bearing in the selftest fixtures only; an R65-C2 receipt that cited
   the CLI arms alone would not discriminate them. No action requested — the instrument's own
   selftest covers all three, so no mutant survives.
2. The two mutations that break the R65-C2 predicate's two halves are exactly M1 (stem arm no
   longer clean: exit 1, dropped 2) and M6 (date arm no longer names the 2 hidden files:
   dropped 0, exit 0). Both are detected by the CLI arms, i.e. the predicate's own counters
   are what kills the defect-restoring mutants.

## Restoration

Frozen instrument never opened for write; only copies were mutated. Frozen sha256 after the
pass `9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6`; repo
`tools/round-65/` clean. Scratch `/fast/scratch/hyaku/kaidoku-r65/MutCoverage` deleted after
this report was written.
