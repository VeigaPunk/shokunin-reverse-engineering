# CriticClaims — R65-C1 / R65-C2 attack (round 65, w1, attempt 1)

Seat: critic (leaf, read-only). Base `c99e907cb5576c13a7b22755d776b356fdfc1752`.
Instruments re-hashed and equal to the pins: `jsc-closure-matrix.py`
`79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`,
`coverage-recipe.py` `9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6`.
Selftests re-run clean: 34 cases / 28 cases. Real toolchain cache-free before and after
(`find ~/.local/share/kaidoku-jsc \( -name __pycache__ -o -name '*.pyc' \)` → empty, exit 0).
No file outside this report directory and my scratch was written; frozen bytes untouched;
scratch deleted before yield. Reproduced evidence is in `evidence/` beside this file.

---

## R65-C1 — depth, capability acquisition

Predicate (plan:29-33, claims.json `claims.R65-C1.predicate`, instrument `PREDICATE` L68-73):
closure manifest count+sha256, cache-free before the first run, all 18 labels, census equal.

### (a) Axis vs number

The C1 surface is the verification harness itself: a 30-entry pin manifest, a cache-free
pre-state, and a no-write census around the 18-cell loop. The 18 labels and their 18/18
count are r64's already-reproduced number (r64 SCORECARD `.ufo`/`SCORECARD.md:4991-5019`).
So the claim is not "merely the number": the surface changed is the closure. It is,
however, a **measurement-capability** on the depth axis, not new route knowledge — the
route's outcomes were already known; what is newly claimed is that the route is closed.

### (b) Do-nothing control

- Named control: `--skip-run` → 0/18, exit 1 (`l1/c1-before-donothing.json`; I re-read it:
  `runs_matching 0, runs_total 18, verified false, exit 1`). This is red by construction:
  `verdict({})` marks every cell `not-run` (L172-186).
- Cheapest *real* do-nothing that reaches the target: run the frozen instrument against the
  already-cleaned toolchain. The L1 did exactly that **before the freeze**:
  `l1/probe/dryrun-matrix.json` → `runs_matching 18, runs_total 18, verified true, exit 0`,
  closure `entries 30 / ok true / cache_present []`, census `equal true`. My independent
  run on a byte-identical toolchain copy (same instrument, probe guard only) also produced
  18/18, exit 0 (`evidence/cache-ordering-receipt.json`).
- Therefore the claim's before/after is not separated by the round: the after-state was
  already produced by the pre-claim dry run. The only non-instrument round work is the prep
  deletion of four `__pycache__` dirs (`prep/precache-dirs.txt`). The honest before-arm —
  the r64 tree *with* those caches under the new instrument (exit 2) — was destroyed before
  the freeze; only the prep list records it. The `--skip-run` red is not that state.

### (c) Clause → implementing line

| # | Predicate clause | Implementing line(s) | Read at runtime? | Verdict |
|---|---|---|---|---|
| i-a | "manifest matches every one of its entries (count and sha256)" | `CLOSURE` L81-108; `closure_findings` L229-254; `entries = len(CLOSURE)+3` L252 | presence+sha256: yes. **count: reported, never asserted** | **defect C1-F2** |
| i-b | "no Python bytecode cache present before the first run" | `cache_entries` L193-203; folded in L244-251; gate L287-290 | yes — but **before `python_probe` L300**, while the census baseline is taken at L305 after it | **defect C1-F1** |
| ii | "all 18 runs reproduce the frozen predicted label" | `PREDICTED` L116-126; `verdict` L172-186; loop L309-338 | yes — `PREDICTED × REPS`, missing cell → `not-run` → mismatch | holds; independently reproduced 18/18 |
| iii | "after-run census equals the before-run census" | `census` L206-218; `compare_censuses` L221-227; before L305, after L339 | yes (`delta["equal"]` folded at L347) | holds as written; limits C1-F4/F7 |

### (d) Re-derivability from committed bytes

No. Clauses (i) and (iii) are properties of a **177 MB host toolchain root**
(`du -sh` → 177M; census receipt `l1/census-at-freeze.json` has 105 entries) plus a
host-resolved node binary and uv interpreter (`NODE_PATH` L112, `INTERPRETER_PATH` L114).
The repo commits the pins and the receipts, not the bytes. One command re-derives the
verdict **on this host**; a closure over committed bytes alone cannot. This is a stated
limit of the capability, not a predicate falsehood, but it must not be reported as
"reproducible from the repository".

### (e) Universal clauses / enumeration

- "every one of its entries": fully enumerated (`CLOSURE.items()`), and `entries=30`
  is emitted. The count is **not** compared to a frozen constant (C1-F2).
- "all 18 runs": fully enumerated (`PREDICTED` 6 × `REPS` 3).
- "every file the run reads" is **narrative, not the counted set** (C1-F3): the venv
  interpreter's stdlib lives outside the root (`venv/pyvenv.cfg` → `home =
  /home/vgpnk/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin`), and libc/ld.so
  are outside both the manifest and the census. The census sees 105 root files; the
  manifest integrity-pins 27 of them (+probe+node+interpreter). Equality of the 105-entry
  map is a no-write proof, not an integrity proof.

### (f) r64 reuse / narrowing

Clause (ii) is r64's first clause verbatim (same `PREDICTED`, same 18 cells); r64's
"every input and binary sha256 equal to its pin" is replaced by (i)+(iii). No target is
narrowed after landing, and no r64 predicate is renamed wholesale. The claim re-measures
r64's already-produced 18/18; the new content is the closure and the census.

### Findings

**C1-F1 — HIGH (counter; surviving mutant).** The cache-free clause is asserted before
`python_probe`, and the before-census is taken after it, so a cache written by the setup
probe is absorbed into the baseline and never reported.

- Code: `python_probe(...)` L300 → `before = census(root)` L305 → `after = census(root)`
  L339; the cache check is inside `closure_findings` at L287-290, i.e. before L300.
- Counterexample (scratch copy of the frozen instrument; only `python_probe`'s `-B` and
  `PYTHONDONTWRITEBYTECODE` removed; full matrix against a byte-identical toolchain copy):
  `run_exit=0`, receipt `{'runs_matching': 18, 'runs_total': 18, 'verified': True, 'exit': 0}`,
  `closure.cache_present=[]`, `closure.ok=True`, `census={'equal': True, ...}`, while
  `tc/venv/lib/python3.15/site-packages/parse/__pycache__/__init__.cpython-315.pyc`
  existed on disk for the whole run. Evidence: `evidence/cache-ordering-receipt.json`,
  `evidence/cache-ordering-patch.diff`.
- Meaning: the predicate's "before the first run" is not the boundary the code checks.
  Under the frozen bytes `-B`/env make the probe write nothing, so the **executed** run is
  clean; but the counter would certify a contaminated run, and the no-cache evidence in the
  receipt is stale by one setup step. Smallest safe correction (report, do not patch):
  re-run `cache_entries(root)` after `python_probe` and before `before = census(root)`,
  and fold it into `closure.ok`.

**C1-F2 — MEDIUM (counter; count never asserted).** A truncated manifest passes.

- Code: `closure_findings` iterates `CLOSURE.items()` (L229-243) and prints
  `entries = len(CLOSURE)+3` (L252); nothing compares that number to 30.
- Counterexample: scratch copy with exactly one CLOSURE entry deleted
  (`jsc2js-src/View8/Parser/parse_v8cache.py`) → `--manifest` exit **0**,
  `{"entries": 29, "missing": [], "pin_mismatch": [], "ok": true}`
  (`evidence/trunc-manifest-29.json`). The real file remains in the tree unpinned.
- Only the out-of-band instrument sha256 pin blocks this on the frozen bytes; the
  predicate itself does not read it. Smallest safe correction: a frozen `COUNT = 30`
  and an assertion in `closure_findings`/`emit`.

**C1-F3 — MEDIUM (false provenance).** The docstring's "Closure (every file the matrix run
reads, plus every executable it spawns)" (L1-3, L12-30) overstates. The 30 entries are 27
root files + probe + node + interpreter; the interpreter's stdlib (via `pyvenv.cfg`),
libc/ld.so, and 78 of the 105 censused root files are not pinned. Clause (i) is
self-referential: it tests the manifest against itself, not against the read set. The r64
F1 repair is real for the named root files; the universal sentence is not.

**C1-F4 — MEDIUM (TOCTOU / symlink blind spot).** `closure_findings` hashes
`Path(args.python).resolve()` while every subprocess runs `args.python` (the symlink);
`census()` skips symlinks entirely (L212: `if p.is_symlink() or not p.is_file(): continue`).
`venv/bin/python`, `python3`, `python3.15` and `venv/lib64` are symlinks. Retargeting the
interpreter between the check and the run is invisible to clauses (i) and (iii).
Smallest safe correction: resolve once and pass the resolved path to all subprocesses;
include symlink target strings in the census map.

**C1-F5 — LOW (container atom false universal).** claims.json A3: "-B plus
PYTHONDONTWRITEBYTECODE=1 on every subprocess". `run_cell` (L273-279) passes **neither**
an env nor `-B`; `node --check` gets the env but no `-B`. Only the two Python subprocesses
get both. No practical write hole (d8/node emit no `.pyc`), but the atom is false.

**C1-F6 — LOW (synthetic green sub-fields).** `--skip-run` fabricates
`closure = {entries:30, ok:true, ...}` and `census = {equal:true}` without measuring
(L501-505). The L1's `l1/c1-before-donothing.json` therefore reports `closure.ok true` and
`census.equal true` in a receipt where nothing was checked. Exit 1 / `skip_run true` keep
it from being a pass, but a reader diffing sub-fields can be misled.

**C1-F7 — LOW (census blindness, stated partially).** `census` compares relpath→sha256
only; file modes, ownership and mtimes are not compared (docstring states mtime only), and
`jsc2js-src/.git/` is excluded (L77, L215-216) with a rationale ("a read-only git call may
refresh") that does not apply — the instrument makes no git call. A `chmod` or a `.git`
write during the run is invisible.

### VERDICT: R65-C1

`VERDICT: R65-C1 PASS on the frozen run as executed` — manifest 30/30, cache-free at check,
18/18 labels reproduced (independently re-run on a byte-identical copy), census equal,
exit 0. **But** clause (i) is not self-enforcing: C1-F1 (cache asserted one setup step too
early; a probe that writes cache is absorbed into the baseline and the counter still says
verified) and C1-F2 (count reported, never asserted; a 29-entry manifest exits 0) are
surviving-mutant defects the judge must record. Do not patch the frozen instrument in place;
carry both as routed instrument debt. The claim is a verification-capability on the depth
axis, not new route knowledge; the 18/18 half is r64's number and is not the new surface.

---

## R65-C2 — calibration, capability

Predicate (plan:76-79, claims.json `claims.R65-C2.predicate`): stem recipe
`mismatches == 0` with `mapped > 0`, **while the superseded date-limited recipe on the same
revision reports a non-zero `population_dropped` naming the files it hides.**

### (a) Axis vs number

The surface is the coverage recipe's key and population accounting, so it is not merely the
number. But the surface actually changed is narrower than the claim says: the old recipe's
**numerator** is date-keyed (`mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))`,
base SCORECARD L102) while its **denominator is every `.md` stem**
(`files = {...}`, L100, `coverage_score = 10*len(files & mapped)/len(files)`, L121). The
repair (stem-keyed `token_set`) fixes the numerator. The claim's story — "derives both
sides from the same date filter … leaves the denominator silently" (plan:66-70; instrument
docstring L12-23) — is false against committed bytes.

### (b) Do-nothing control — the named one is falsified

Plan:95: "the do-nothing case is the unchanged date recipe (exit 1, 2 dropped)".
I ran **recipe A verbatim** (the committed block, SCORECARD L92-124) at the base:

```
{"citation_resolved_rules": 27, "coverage_score": 9.86, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 144, "mapped": 142,
 "missing": ["jsc-mapper-cli-contract", "jsc-mapper-release-inventory"],
 "revision": "c99e907cb5576c13a7b22755d776b356fdfc1752", "rule_blocks": 27}
exit=0
```

- The unchanged recipe **does not drop** the two files from its denominator
  (`knowledge_files=144`), **does not print a perfect score** (9.86), **names** both files
  in `missing`, and **exits 0**. Under the frozen counter's `--recipe date` mode the same
  revision reports `population 142, population_dropped 2, mismatches 2, exit 1`.

So the "before" red is manufactured by the new instrument's date mode, not the behaviour of
the recipe being repaired. Cheapest do-nothing that reaches the **after** target: run the
frozen `--recipe stem` at the base — 144/144, mismatches 0, exit 0 (I re-ran it). The base
repo already contains the map tokens for the two non-dated entries (r64 added them); the
round's repo delta is zero and the capability is the pre-frozen instrument.

### (c) Clause → implementing line

| # | Predicate clause | Implementing line(s) | Read at runtime? | Verdict |
|---|---|---|---|---|
| i | "repaired stem-keyed recipe reports `mismatches == 0` with `mapped > 0`" | `assess` L89-109 (stem branch L95-99), `exit_class` L112-116 | yes | holds: live 144/144, 0, exit 0 (`evidence/coverage-stem-at-base.json`) |
| ii | "over the repository at the measured revision" | `read_inputs` L122-129 (`git ls-tree`, `git show`) | yes | holds (rev is a parameter; reads committed objects) |
| iii | "the superseded date-limited recipe on the same revision" | `assess` date branch L93-94 | **no — this is not the superseded recipe** | **C2-F1/C2-F2** |
| iv | "reports a non-zero `population_dropped`" | `dropped = len(files) - len(population)` L104; key L108 | yes | 2 at base |
| v | "naming the files it hides" | **no line** — `dropped` is an `int`; the result dict (L105-109) has no name list; at base the date run's `missing` is `[]` | **never** | **C2-F3 (QUALITY #87)** |

### (d) Re-derivability from committed bytes

Yes. `python3 tools/round-65/coverage-recipe.py --root <lane> --rev
c99e907cb5576c13a7b22755d776b356fdfc1752 --recipe stem` → 144/144, 0, exit 0
(`evidence/coverage-stem-at-base.json`). One command, committed objects only.

### (e) Universal clauses / enumeration

"the files it hides" is not enumerated by identity anywhere in the counter: the full hidden
set is counted (`dropped=2`) but no receipt names it. The executor's supplementary
`w1/ExecCoverage/c2-dropped-names.json` names both files and itself records
`"method": "read_inputs plus frozen DATE_TOKEN_RE; supplementary independent naming, not
emitted by instrument JSON"` — i.e. the naming clause is satisfied by an auxiliary
computation, not by the frozen counter the predicate names.

### (f) Narrowing / predicate reuse

No post-landing narrowing; no wholesale reuse of r64's predicate. But the before-arm
**substitutes a new mode of the new instrument** for the superseded recipe under the old
recipe's name — a provenance substitution, not a repair.

### Findings

**C2-F1 — HIGH (false premise).** The claim's defect statement and before-arm are false of
the superseded recipe. Base recipe A: denominator 144 (all stems), numerator 142 (October
tokens), `missing` names both files, `coverage_score 9.86`, **exit 0**. Evidence:
`evidence/recipeA-at-base.json`; source `git show c99e907:SCORECARD.md | sed -n '92,124p'`
(L100 `files`, L102 `mapped`, L121 `files & mapped / len(files)`). The plan's
"population 142/144, population_dropped 2" (plan:89-90) is the new date mode's output, not
recipe A's.

**C2-F2 — HIGH (duplicate authority / false provenance).** `--recipe date` is not "the
superseded r1-era filter, reproduced exactly" (docstring L12-23): it filters the
**denominator** (`population = [f for f in files if DATE_TOKEN_RE.match(f)]`, L93), which
recipe A never did, and introduces `population_dropped`. `DATE_TOKEN_RE` is also anchored
(`^...$`, L58) while recipe A uses unanchored `re.findall` (SCORECARD L102), and the
instrument's `missing`/`dangling` set algebra differs from recipe A's `files - mapped`.
The before-arm therefore measures the new instrument's date mode, not the old recipe.

**C2-F3 — HIGH (QUALITY #87; clause never read).** "naming the files it hides" has no
implementing line: L104 computes an integer; L105-109 emits no list; at base the date
receipt's `missing` is `[]` (`evidence/coverage-date-at-base.json`). The names exist only in
the executor's supplementary receipt, which states it is "not emitted by instrument JSON".
Smallest safe correction: either add `"dropped": sorted(set(files) - set(population))` to
the result under a **new freeze**, or amend the predicate to "counts the files it hides
(`population_dropped == 2`)" — both are post-freeze changes, so re-declare next round.

**C2-F4 — MEDIUM (repair limit not carried into the claim).** The stem recipe's declared
limit (docstring L41-46; selftest `limit-nondated-removal-clean` expects `(0, 0)`) means a
**deleted non-dated knowledge file whose bare map token remains** is reported clean. The
selftest encodes this. The claim's "coverage" is a map↔file count, not citation validity;
recipe A's `citation_resolved_rules`/`depth_score` half (27/27 here) is not carried by the
new instrument at all. The SCORECARD coverage row is the coverage half only.

**C2-F5 — LOW (date-mode selftest encodes the substitution).** `base-date-reproduces`
expects `(mapped, population, mismatches) == (2, 2, 2)` over a 4-file fixture
(L200-210) — the new date mode, not recipe A, which would report 2/4 mapped, 0 dropped,
2 missing. The test locks the mis-description in.

### VERDICT: R65-C2

`VERDICT: R65-C2 FAIL as written.` The after-arm is real and re-derivable: stem recipe at
the base is 144/144, `mismatches 0`, exit 0 (`evidence/coverage-stem-at-base.json`). The
before-arm is not: the superseded recipe A at the same revision prints 144 files /
142 mapped / `missing [jsc-mapper-cli-contract, jsc-mapper-release-inventory]` /
`coverage_score 9.86` / **exit 0**, so it neither drops the files from the denominator nor
prints a perfect score or a red exit; and the frozen counter's date mode names nothing
(`population_dropped` is an int). The predicate's "naming" clause has no implementing line.
Do not narrow the target or patch the frozen instrument in place; re-declare next round
with the actual recipe-A before-arm (mapped 142/144, missing names both, score 9.86,
exit 0) or add a `dropped` list under a new freeze.

---

## Answers to the assigned attack questions (compact)

1. **Axis vs number** — C1: surface = closure/cache/census, not the 18/18 count. C2:
   surface = recipe key/population, not the 144/144 count; but the actual change is the
   numerator only, and the denominator story is false.
2. **Do-nothing control** — C1: `--skip-run` 0/18 exit 1 is synthetic; the real do-nothing
   (frozen instrument on the cleaned tree) already produced 18/18 exit 0 in the pre-claim
   dry run. C2: the named do-nothing ("unchanged date recipe exit 1, 2 dropped") is
   falsified — recipe A exits 0 with 9.86 and names both files; the frozen stem run at the
   base already reaches the target with zero repo change.
3. **Clause trace / unread clauses** — C1: count reported, never asserted (C1-F2); cache
   checked before the probe, not before the first run (C1-F1). C2: "naming the files it
   hides" never read (C2-F3); "superseded recipe" is not the superseded recipe (C2-F1/F2).
4. **After-state re-derivable from committed bytes** — C2 yes; C1 no (external 177 MB
   toolchain root; receipts are the evidence).
5. **Universal clauses** — C1 "every one of its entries" is enumerated but not bounded by a
   frozen count; "all 18" fully enumerated; "every file the run reads" is narrative (stdlib
   outside root). C2 "the files it hides" is counted but not named/enumerated by identity.
6. **Narrowing / r64 reuse** — no narrowing; no wholesale predicate reuse. C1 carries r64's
   18-label clause; C2 substitutes a new instrument mode for the old recipe.

## Impacted axes

- **depth (C1):** verification-capability integrity; C1-F1/F2 are counter defects that
  survive mutation. No new route knowledge is added by this claim.
- **calibration (C2):** the measurement's before-arm and provenance; C2-F1/F2/F3 mean the
  claim cannot be verified as written even though the stem receipt is green.
- **Provenance (both):** C1-F3/F5/F6 and C2-F2/F3 are false or overstated provenance in
  docstrings/container atoms, not in the frozen predicate text.

## Smallest safe corrections

1. C1-F1: re-check `cache_entries(root)` after `python_probe` and before `before = census(root)`.
2. C1-F2: assert `len(CLOSURE)+3 == 30` (frozen constant) in `closure_findings`/`emit`.
3. C1-F3: describe the closure as "27 root entries + probe + node + interpreter", not
   "every file the run reads"; either pin the stdlib identity or state it as a limit.
4. C1-F4: run all subprocesses on the resolved interpreter path; census symlink targets.
5. C1-F5: container atom → "every Python subprocess".
6. C1-F6: `--skip-run` must not emit a measured-looking `closure.ok`/`census.equal`.
7. C2-F1/F2: re-declare the before-arm as recipe A's real output; drop the "denominator"
   narrative.
8. C2-F3: add a `dropped` name list under a new freeze, or change the clause to a count.
9. C2-F4: carry the deleted-non-dated-entry limit into the claim text.

## Commands run (all read-only; scratch under /fast/scratch/hyaku/kaidoku-r65/CriticClaims, deleted)

```
sha256sum tools/round-65/{jsc-closure-matrix.py,coverage-recipe.py}                  # match pins
python3 tools/round-65/jsc-closure-matrix.py --manifest --probe .ufo/.../probe-electron.jsc
python3 tools/round-65/jsc-closure-matrix.py --selftest                              # 34 clean
python3 tools/round-65/coverage-recipe.py --selftest                                 # 28 clean
python3 tools/round-65/coverage-recipe.py --root <lane> --rev c99e907... --recipe date   # exit 1
python3 tools/round-65/coverage-recipe.py --root <lane> --rev c99e907... --recipe stem   # exit 0
python3 - c99e907... <<'PY'  # committed recipe A verbatim                            # exit 0, 9.86
cp tools/round-65/jsc-closure-matrix.py trunc.py; # delete one CLOSURE entry
python3 trunc.py --manifest ...                                                      # exit 0, entries 29
cp -a ~/.local/share/kaidoku-jsc tc; # scratch instrument: probe -B/env removed
python3 probe-writes.py --toolchain-root tc --probe ... --python tc/venv/bin/python --work work --out receipt.json
                                                                                     # exit 0, 18/18, cache on disk
find ~/.local/share/kaidoku-jsc \( -name __pycache__ -o -name '*.pyc' \)             # empty (real tree)
```

Evidence: `evidence/recipeA-at-base.json`, `evidence/coverage-date-at-base.json`,
`evidence/coverage-stem-at-base.json`, `evidence/trunc-manifest-29.json`,
`evidence/cache-ordering-receipt.json`, `evidence/cache-ordering-patch.diff`.
