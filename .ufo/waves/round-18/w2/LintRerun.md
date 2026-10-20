PARTIAL

# C2 head-rev-lint re-run (wave 2, falsify)

Seat: KaidokuR18.LintRerun. Read-only. Lane HEAD observed at
`b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (`git rev-parse HEAD`); baseline
`9011581d84527ba34c675f9cf912e54d2e72d470` is its ancestor
(`git merge-base --is-ancestor <base> <tip>` exit 0). No tool installed, no
lane file written except this report.

Verdict rationale, one sentence: the before/after numbers reproduce exactly and
deterministically and every *emitted* annotated site is defensible except one
mislabel, but one of the three routed sites (`round-17/verify.py`) still executes
`git rev-parse --verify HEAD^{commit}` on every live run and the lint cannot see
it, so "live HEAD-as-revision call sites: 0" is true of the rule's recognized
shapes, not of the code's git invocations.

## 1. Commands, exit codes, digests

Run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` with
`T=.ufo/waves/round-18/tools/head-rev-lint.py` and `--root "$PWD"`.

| command | exit | stdout sha256 (16) |
|---|---|---|
| `python3 -I -B $T --rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0 | `035b157277fe4ae8` |
| `... --rev 9011581d84527ba34c675f9cf912e54d2e72d470 --strict` | 1 | `035b157277fe4ae8` |
| `python3 -I -B $T --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | 0 | `2b42007edec73f81` |
| `... --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --strict` | 0 | `2b42007edec73f81` |
| `... --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` | 2 | `could-not-evaluate: git rev-parse --verify exit 128` |
| `python3 -I -B $T --selftest` | 0 | `SELFTEST: CLEAN cases=3` |

Observation: stdout is byte-identical between plain and `--strict` at each rev
(`diff -q` exit 0), i.e. the flag changes only the exit code
(`head-rev-lint.py:679-682`). Re-runs of each command produce the same digest;
a run from `cwd=/tmp` with `--root` produces the same tip digest. So the counts
are deterministic and cwd-independent.

## 2. Counts

| rev | files_scanned | live | fixture | annotated | excluded |
|---|---|---|---|---|---|
| `9011581d` | 27 | **3** | 8 | 0 | 10 |
| `b2aad08c` | 39 | **0** | 15 | 6 | 10 |

`files_scanned` cross-checks against the tree: 27 and 39 tracked `*.py`/`*.sh`
under the six site dirs outside `w[0-9]+/` segments
(`git ls-tree -r --name-only <rev> -- .ufo/gates .ufo/rounds .ufo/waves/round-1{4,5,6,7,8}`
piped through the same filters). 49 paths total at tip, 10 seat-excluded.

Baseline live 3, verbatim from the JSON, matching `claims.json:38`:

- `.ufo/gates/citation-drift/citation-drift-probe.py:477` `default-HEAD`
  (`ap.add_argument("--rev", default="HEAD")`)
- `.ufo/gates/custody-pair/custody-pair.py:327` `rev-parse-HEAD`
  (`["git", "rev-parse", "HEAD"]` inside `repo_head(cwd)`, which took `Path.cwd()`)
- `.ufo/waves/round-17/verify.py:59` `rev-parse-HEAD` (`source = git("rev-parse", "HEAD")`)

Tip live 0; annotated 6 = 4 `compare-only` + 2 `red-before`. Excluded list is
identical at both revs: 10 seat files, 4 would-be sites
(`round-17/w2/audit-attack.py:91,349` live; `round-17/w2/temporal-attack/fixtures/rebuild.sh:9,11`
fixture). Fixture growth 8→15 is round-18 `controls.py`/`measure.py`/`revpin.py`/
`routed-defects.py` selftest helpers; I checked the call graph for the two
non-obvious ones: every `_commit` caller in `round-18/controls.py` (623-772) and
`round-17/controls.py` (452-474) is inside `selftest()`, and `measure.py:660` is
inside `_commit` called only from `selftest()` — so the fixture label is true.

## 3. Annotated-site audit (the six emitted sites)

| site | label | check |
|---|---|---|
| `citation-drift-probe.py:304` | compare-only | **TRUE.** The `rev-list --max-count=1 HEAD` lives in `head_commit()` (`:299-305`), called only at `:331`; the value is compared to `refs/heads/<branch>` and refusal is returned (`:329-339`). |
| `custody-pair.py:381` | compare-only | **MOSTLY TRUE, not "solely compare".** `head` is compared at `:388` and also retained: `ctx["head"]`→`# repo-HEAD:` at `:407`, with `# repo-HEAD-is-branch-tip:` at `:411`. The docstring discloses this (`:365-370`) and the retention is flag-guarded, so the safety intent holds; the literal annotation wording ("read solely to compare", `head-rev-lint.py:37-38`) does not. |
| `custody-pair.py:1350` | compare-only | **TRUE.** Fixture capture of the first commit, used only in the assertion at `:1353`. |
| `custody-pair.py:1353` | compare-only | **TRUE.** Pure `assert git_f("rev-parse","HEAD") == tip`. |
| `jj-red-before.py:377` | red-before | **MISLABEL.** D0 steady state: sandbox detached at tip, expected `HEAD == main` (`:376-386`). That is a comparison, not a "deliberate baseline reproduction" (`head-rev-lint.py:39`). `compare-only` would be accurate. Conservative — annotated either way, no count effect. |
| `jj-red-before.py:659` | red-before | **TRUE.** Reproduces the baseline expression `git rev-parse HEAD` on the off-branch commit and expects red (`:658-669`). |

**Dead annotation at routed site #1.** `round-17/verify.py:81` carries
`# head-rev-lint: compare-only` on the line *above* the call at `:82`.
Annotations bind only to the site line (`head-rev-lint.py:525`,
`lines[line - 1]`), and no site is emitted for `:82` at all, so the comment is
inert text.

Other annotation occurrences that emit no site (therefore cannot affect the
count): `citation-drift-probe.py:552`; `jj-red-before.py:255,284,318` (`sha_of`
rev-only wrapper), `:390,577` (plain argv, not a git argv),
`:733,763,764,786,813,859` (inside fixture source strings / literals). Listed so
the "6 annotated" total is explained: annotations on invisible sites simply do
nothing.

## 4. Findings (each with a repro)

**F1 — `round-17/verify.py:82` is a live HEAD read the lint cannot see.** The
fix replaced `source = git("rev-parse","HEAD")` with
`source = _git_or_none("rev-parse","--verify", f"refs/heads/{branch}^{{commit}}")`
plus `head = _git_or_none("rev-parse","--verify","HEAD^{commit}")`
(`verify.py:80-82`). `_git_or_none` is **not** registered as a git wrapper,
because registration requires a literal `["git", ...]` argv in the function body
(`head-rev-lint.py:452-468`) and `_git_or_none` delegates: `return git(*args)`
(`verify.py:63-67`). Repro:

```
python3 -I -B -c "
import importlib.util, subprocess
spec=importlib.util.spec_from_file_location('hrl','.ufo/waves/round-18/tools/head-rev-lint.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
src=subprocess.check_output(['git','show','b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-17/verify.py'],text=True)
print(m.scan_python(src)[0])"
# -> []
```

Observed: `[(59,'rev-parse-HEAD')]` at baseline, `[]` at tip, while the git
invocation remains at `verify.py:82`. Isolation (same scanner, synthetic):
`git("rev-parse","HEAD")` → one site; `_wrap` delegating to `git` →
**no site**; `_wrap` with its own literal body → one site. So the cause is
wrapper registration, not the annotation.

**F2 — `round-18/tools/revpin.py:108` is the same class, structurally worse.**
`head = _resolve(lane, "HEAD^{commit}")` in `resolve_source()`, reached from the
CLI at `:307`. `_resolve` hardcodes the subcommand in its body (`:81`) and the
call passes only the rev, so even registering `_resolve` as a wrapper would not
classify it (wrapper calls carry only call-site tokens,
`head-rev-lint.py:268-291`). Repro: `scan_python` on `revpin.py` at tip yields
only `(218,'other-HEAD')` (a `_selftest` checkout), never line 108. Both F1 and
F2 are compare-only in behavior (`verify.py:92-93`, `revpin.py:118-119` refuse),
so the *safety* property holds; the *count* is not evidence of absence.

**F3 — the fix would go red if the instrument were corrected.** With
`_git_or_none`'s body replaced by a literal so that `:82` becomes visible, the
real `verify.py` yields `site line 82 rev-parse-HEAD -> ('live', None)`.
`--strict` at the tip would then exit 1. The fix therefore depends on the
scanner's blind spot plus a dead annotation, not on a compliant annotation.

**F4 — `jj-red-before.py:377` label** (`red-before` for a steady-state
comparison). Cosmetic; no count effect.

**F5 (minor) — annotation precedence over fixture.** `python_context` tests the
annotation before `/fixtures/` or enclosing-function fixture rules
(`head-rev-lint.py:525-533`), so `custody-pair.py:1350/1353` count as
`annotated` rather than `fixture`. Total live is unaffected.

## 5. What holds (observation)

- The stated falsifier is reproducible: 3 live at `9011581d` → 0 at
  `b2aad08c`; `--strict` 1 → 0; outputs deterministic and cwd-independent.
- Baseline sites are exactly the three the amendment names, with the same lines.
- All three routed tools now pin `refs/heads/main` and refuse/flag an
  off-branch HEAD: `citation-drift-probe.py:311-342` (default `--rev None` at
  `:590`; `--rev HEAD` accepted only when equal), `custody-pair.py:365-391`
  (`--repo` defaults to `LANE_ROOT`, never cwd, `:744`), `verify.py:70-101`.
  I read these paths; I did not execute the tools.
- The lint's `limits` (`head-rev-lint.py:129-144`) are honest about static
  scanning, but they do not mention the two gaps that matter here: a wrapper
  delegating to another wrapper is not registered, and a rev-only wrapper whose
  body hardcodes the subcommand can never be classified. The text only says
  "another module is not resolved".

## 6. Risks

- The r18 gate asserts `head-rev-lint ... --strict` exits 1 at baseline and 0 at
  source (`round-18/verify.py:181-186`). It is green today, but a strictly
  better scanner turns it red (F3), so the gate is calibrated to the tool's
  blind spot.
- `verify.py:82` and `revpin.py:108` are live entry points: a future regression
  that *pins* HEAD instead of comparing it would not be caught by this lint.
  "0 live" cannot be quoted as an ongoing invariant without fixing F1/F2 or
  recording that limit.

## 7. Blockers

None. No external state touched, no tooling installed, no lane edits beyond
this report.
