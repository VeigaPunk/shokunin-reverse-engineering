# MutCoverage — R66-C2 counter mutation probe (detailed)

Target: `tools/round-66/coverage-selfcheck.py`, frozen sha256
`1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa` (never edited; every mutant ran from a
scratch mirror under `/fast/scratch/hyaku/kaidoku-r66/MutCoverage/<M>/coverage-selfcheck.py`).
Lane root `--root`: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; measured revision
`--rev 311079d869f068bc083a8d180977e49634120fdf` (base). Interpreter for every run, including the
counter's own recipe-A subprocess: `/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python`.
All six copies were generated and run in one shell batch; each detector pass is a single subprocess.

Disk guard checked before the pass (`scripts/hyaku/disk-guard.sh status`: `/fast` 55 % used, 369 G free).

## Baseline (pristine bytes)

| detector | exit | receipt |
|---|---|---|
| `--selftest` | 0 | `SELFTEST CLEAN cases=26 failures=0` |
| `--selfcheck --rev 311079d…` | 1 | `equiv=true hidden=3 mismatches=1 ok=false`; atoms `A1 true`, `A2-cited-fraction false` (claimed `[142,142]`, observed `[145,145]`); stem `145/145`, missing/dangling empty |

This is the required base arm: the cited fraction is stale at base, exactly as the predicate's last clause says.

## Summary

| # | mutation | selftest | selfcheck @base | verdict | killing arm |
|---|---|---|---|---|---|
| M1 | `recipe_hidden` → `[]` (line 156) | **exit 1**, `FAILED cases=26 failures=1` | exit 1, hidden **0**, mismatches 1 (unchanged) | **killed** | selftest case `recipe-a-hidden-list` (line 324); base selfcheck is masked by the pre-existing mismatch, controlled-green fixture re-kills at exit 1 vs 0 |
| M2 | `recipe_a_equivalence` returns true without running the block (lines 200-207) | exit 0, `CLEAN` | exit 1, hidden 3, mismatches 1 (identical to baseline) | **SURVIVED** | none in the two assigned detectors; `--equiv` on a disagreeing block separates it (base rc 1 / three diffs, mutant rc 0) |
| M3 | A2 atom dropped (lines 260-264) | exit 0, `CLEAN` | **exit 0**, mismatches **0**, `ok=true`, atoms `[A1]` only | **killed** | `--selfcheck` base arm: expected exit 1 / mismatches 1; mutant reports green and the receipt loses the `A2-cited-fraction` id |
| M4 | `parse_row` yields the observed fraction → tautological A2 comparison (lines 243, 262-264) | exit 0, `CLEAN` | **exit 0**, mismatches **0**, `ok=true`, A2 `ok=true` | **killed** | `--selfcheck` base arm: A2 flips true against claimed `[142,142]` vs stem `[145,145]` |
| M5 | `mismatches = 0` constant (line 268) | exit 0, `CLEAN` | **exit 0**, mismatches **0**, `ok=true`, yet atom A2 `ok=false` | **killed** | `--selfcheck` base arm exit; receipt is additionally self-contradictory (`mismatches 0` with a false atom) |

Mutant sha256s: M1 `7c3ac393067a89e58e5324d1515843b2fed3dc5c15800dde8497cb21dbcc82b7`,
M2 `2b98a7f73fedfe54fdd4abef323e24287feb939808a46695bed241d3c8c887a9`,
M3 `19803ac47dfbfe9e666703e45a04597f3d1182d6273383366e087eec5700902b`,
M4 `bdbd289ed5b068c0279c457ed21455c65a261f53edd44708c463aeed8ba03eb3`,
M5 `0711710649e206d4911fff1971633e7d19e71768054cf714a68d5e1d842245dc`.

## M1 — `recipe_hidden` returns `[]`

```diff
--- tools/round-66/coverage-selfcheck.py (frozen 1be9d046)
+++ M1/coverage-selfcheck.py
@@ -154,5 +154,5 @@
     """The explicit list recipe A's date-token numerator cannot map."""
     date_stems = set(DATE_TOKEN_RE.findall(section))
-    return sorted(set(files) - date_stems)
+    return []
```

- `--selftest` exit **1**: `SELFTEST FAILED cases=26 failures=1`, `FAIL recipe-a-hidden-list got=[] want=['jsc-mapper-cli-contract']`.
  The kill is the fixture's four-file population at line 319-324, not any repository input.
- `--selfcheck` at base exit **1**, `hidden=0`, `mismatches=1`, `ok=false` — **indistinguishable from
  baseline**, because the base arm is already red through A2 and `ok` is an AND. The hidden clause is
  masked at base.
- Controlled-green fixture (`fixture2`, all clauses satisfied): pristine exit 0 / hidden 1; M1 exit **1** /
  hidden 0 → the clause does have a live arm, but only at a revision whose two atoms already pass.
- Verdict: **killed** (selftest case `recipe-a-hidden-list`); at the base revision the `--selfcheck`
  detector alone would have let it through.

## M2 — equivalence asserted without running the block

```diff
@@ -198,15 +198,7 @@
     path = scratch / "recipe-a-verbatim.py"
     path.write_text(script, encoding="utf-8")
-    r = subprocess.run([sys.executable, "-I", "-B", str(path), rev], cwd=root,
-                       capture_output=True, text=True, timeout=900)
-    if r.returncode != 0:
-        raise ValueError(f"recipe-A block failed rc={r.returncode}: "
-                         f"{r.stderr.strip()[:200]}")
-    theirs = json.loads(r.stdout)
-    diffs = {k: {"block": theirs.get(k), "ours": ours.get(k)}
-             for k in RECIPE_A_KEYS if theirs.get(k) != ours.get(k)}
-    return {"recipe_a_equivalent": not diffs, "recipe_a_diffs": diffs,
+    return {"recipe_a_equivalent": True, "recipe_a_diffs": {},
             "recipe_a_block_sha256": sha256_text(script),
-            "recipe_a_block_keys": sorted(theirs),
+            "recipe_a_block_keys": sorted(RECIPE_A_KEYS),
             "recipe_a": ours}
```

- `--selftest` exit **0**, `SELFTEST CLEAN cases=26 failures=0`. `selftest()` never calls
  `recipe_a_equivalence`; every occurrence is outside it (def 191, return 208, call 266, reads 269/272-273,
  CLI 409-411).
- `--selfcheck --rev 311079d…` exit **1**, `equiv=true hidden=3 mismatches=1 ok=false` — **byte-identical
  receipt fields to baseline** (`recipe_a_diffs {}`, same block sha `1d697af103985da0…`). At base the
  equivalence clause is already true, so suppressing the comparison changes nothing the detector reads.
- Out-of-band probe that names the unbound line: synthetic fixture with a recipe-A block that prints
  `mapped 1 / knowledge_files 3 / coverage_score 1.0` while the counter computes `3 / 3 / 10.0`.
  `--equiv --root fixture --rev HEAD` → pristine **rc 1, `equivalent false`, diff keys
  `['coverage_score','mapped','missing']`**; M2 **rc 0, `equivalent true`, diff keys `[]`**.
  Same separation falls out of `--selfcheck` on that fixture (base rc 1 / M2 rc 0), because
  `recipe_a_equivalent` feeds `ok`.
- **Survivor.** Unbound line: `tools/round-66/coverage-selfcheck.py:200-207` — the `subprocess.run` of the
  extracted block, `json.loads(r.stdout)`, and the `diffs` comprehension — plus every consumer of
  `equiv["recipe_a_equivalent"]` (269). No selftest case, and no base-revision input, can make the frozen
  counter report `false` here: the atom is a self-check that only ever confirms itself. A selftest case
  that runs `recipe_a_equivalence` against a doctored block (or a fixture revision with a disagreeing
  block) would bind it.

## M3 — A2 atom deleted

```diff
@@ -258,9 +258,4 @@
         {"id": "A1-head-score", "claimed": parsed["head_score"],
          "observed": stem_score, "ok": parsed["head_score"] == stem_score},
-        {"id": "A2-cited-fraction",
-         "claimed": [parsed["cited_mapped"], parsed["cited_files"]],
-         "observed": [stem["mapped"], stem["knowledge_files"]],
-         "ok": [parsed["cited_mapped"], parsed["cited_files"]]
-               == [stem["mapped"], stem["knowledge_files"]]},
     ]
```

- `--selftest` exit 0, `CLEAN`. No selftest case asserts the atoms list, its length or its ids.
- `--selfcheck` base: exit **0** (baseline 1), `mismatches=0` (baseline 1), `ok=true`, atoms
  `[('A1-head-score', True)]`. The receipt the predicate calls "two self-assessment atoms" is silently
  one atom.
- Verdict: **killed** by the base arm's exit/mismatch. Note the detector is the *base* revision: on the
  controlled-green fixture (`fixture2`) M3 is exit 0, same as pristine — after the repair lands green,
  this mutant survives if the wave drops the base revision from the suite.

## M4 — `parse_row` supplies the observed fraction (tautology)

```diff
@@ -241,5 +241,6 @@
         raise ValueError("coverage row cites no '<mapped>/<files> knowledge files'")
     return {"head_score": float(head), "cited_mapped": int(frac.group(1)),
-            "cited_files": int(frac.group(2))}
+            "cited_files": int(frac.group(2)),
+            "observed": [int(frac.group(1)), int(frac.group(2))]}

@@ -260,7 +261,7 @@
         {"id": "A2-cited-fraction",
          "claimed": [parsed["cited_mapped"], parsed["cited_files"]],
-         "observed": [stem["mapped"], stem["knowledge_files"]],
+         "observed": parsed["observed"],
          "ok": [parsed["cited_mapped"], parsed["cited_files"]]
-               == [stem["mapped"], stem["knowledge_files"]]},
+               == parsed["observed"]},
     ]
```

- First form of this mutant (changing only the displayed `observed`, keeping the `ok` comparison against
  `stem`) survived **both** detectors — recorded here because it is the tempting minimal edit; a display
  change is not a behavior change. The reported mutant is the one where the tautology is wired into `ok`.
- `--selftest` exit 0, `CLEAN` (no atom case).
- `--selfcheck` base: exit **0** (baseline 1), `mismatches=0`, A2 `ok=true` against claimed `[142,142]`
  while the stem is `[145,145]`.
- Verdict: **killed** by the base arm's exit and by A2's flip.

## M5 — `mismatches` pinned to 0

```diff
@@ -266,5 +266,5 @@
     equiv = recipe_a_equivalence(root, rev, scratch)
     hidden = recipe_hidden(files, section)
-    mismatches = sum(1 for a in atoms if not a["ok"])
+    mismatches = 0
```

- `--selftest` exit 0, `CLEAN`.
- `--selfcheck` base: exit **0** (baseline 1), `mismatches=0`, `ok=true`, and the emitted atoms still say
  `('A2-cited-fraction', False)` — an internally inconsistent receipt. Killed by the base arm's exit; a
  future assertion `mismatches == number of false atoms` would kill it a second time at any revision.
- Verdict: **killed**.

## Fixture used for the equivalence and hidden-clause arms

`fixture2` (built under scratch, git-initialized, toplevel asserted equal to the fixture path before any
git command): four knowledge stems (`2026-10-01-alpha`, `2026-10-02-beta`, `2026-10-03-gamma`,
`jsc-mapper-cli-contract`), a recipe-A block printing the counter's own values
(`mapped 3 / files 4 / score 7.5 / depth 10.0`), and an `## Owned axes` row citing `4/4 knowledge files`
with head `10.0`. Pristine counter on it: exit 0, `equiv=true`, `hidden 1`, `mismatches 0`,
`ok=true` — the only revision in this probe where all three claim clauses hold at once.
`fixture` is the same tree with a deliberately disagreeing block (`mapped 1 / score 1.0`) and a `3/3` row.

## Byte restoration

- Frozen instrument read-only throughout: before and after the pass, sha256
  `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa` (equals the claims pin);
  `git -C <lane> status --porcelain -- tools/round-66` printed nothing.
- All five mutants and both fixtures lived only in `/fast/scratch/hyaku/kaidoku-r66/MutCoverage`, which
  was deleted after this report's receipts were copied into `mutants/`.

## Receipt index (this directory)

`mutants/<M>/coverage-selfcheck.py`, `mutant.diff`, `mutant.sha256`, `selftest.out`, `selftest.rc`,
`selfcheck-base.json`, `selfcheck.rc`, `fx2c.<M>.json|.rc` (controlled-green fixture run);
`mutants/base/` holds the pristine copies plus `fx.base.json|.rc` (disagreeing-block `--equiv` probe);
`fixture2-SCORECARD.md`, `fixture2-SKILL.md`, `fixture2-corpus-README.md` reproduce the synthetic inputs.
