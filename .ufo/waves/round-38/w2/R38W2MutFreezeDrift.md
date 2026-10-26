# R38W2MutFreezeDrift — mutation test of `tools/round-38/freeze-drift.py`

**Verdict: CONFIRMED — freeze-drift.py behaves per contract on all three lane-history cases (10/22 mutants killed by the lane battery); DEFECTS FOUND in the battery's coverage only — 10 surviving mutants are missing-test findings (all killable by synthetic cases), 2 are equivalent mutants. No tool defect found; no contract change proposed.**

## Scope and subject

Target: `tools/round-38/freeze-drift.py` as landed at 3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8.
Subject bytes sha256 `c213bc2d1d82c8673f8c44e0a9cc252d29df25400a73b27ef95b86663687ed5d` — working tree == landed blob (`git show 3b960fe5…:tools/round-38/freeze-drift.py | sha256sum` matched). All mutation was done on scratch copies; the lane file was never written.

Lane-history detector cases (run with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`):

| Case | Args | Expected | Pristine result |
|---|---|---|---|
| C1 | `--freeze e059ca93… --rev 077e212b…` | exit 1, lists 79f693470eae0f2935a4bbf6e4875ef3ec40fb06 and f1010f677a53ecf0e671952ce1bf4f44d51e151b, verdict `drift` | OK (`c1.out` in artifacts) |
| C2 | `--freeze e059ca93… --rev cb4326b2…` | exit 0, verdict `clean` | OK (`c2.out`) |
| C3 | `--freeze 077e212b --rev e059ca93…` | exit 2, reason contains `not an ancestor` | OK (`c3.out`) |

Detector oracle (stricter than exit-only): exit code + **set equality** of parsed drift commit ids (prefix-normalized to 8 hex) + JSON `verdict` + `reason` substring. Set equality matters: it is what kills the empty-default-set mutant (D6); a superset-only oracle would let it survive.

Ground facts used: in range `e059ca93..077e212b`, 79f6934 touched `plans/round-38-claims.md` + `tools/round-38/c1-counter.py` + `tools/round-38/c1-run.sh`; f1010f67 touched **only** `tools/round-38/c1-counter.py`; **no** commit in range touched `tools/round-38/c2-counter.py`, `.ufo/waves/round-38/c1/carriers.json`, or `corpus/evidence/round-37/c1/` (empty `git log` over those pathspecs).

## Mutants and results

22 single-point mutants, five assigned axes. "Lane" = killed by (or survives) the three lane-history cases; "Fixture" = synthetic isolated-branch git repo in scratch (freeze commit + one single-path mutation per branch off the freeze, plus unknown-rev, tab-in-subject, and ref/path-collision probes; baselines all OK before mutant runs).

| Mutant (axis) | Mutation (old → new) | Lane battery | Fixture kill | Classification |
|---|---|---|---|---|
| A1 ancestor | `--is-ancestor', a.freeze, a.rev` → `a.rev, a.freeze` | killed C1,C2,C3 | — | guarded |
| A2 ancestor | drop the whole `--is-ancestor` guard block | survived | C3 (rc 0, exp 2) | missing test: non-ancestor direction |
| A3 ancestor | `if git(…)` → `if not git(…)` | killed C1,C2,C3 | — | guarded |
| B1 pathspec | `f':(glob){p}'` → `f'{p}'` (drop glob magic) | survived | FX-glob-deep (rc 1, exp 0 — false-positive drift: plain pathspec `*` crosses `/`) | missing test: glob semantics |
| B2 pathspec | `f':(glob){p}'` → `f':(literal){p}'` | survived | FX-glob-K1 (rc 0, exp 1 — false negative: literal never expands) | missing test: glob semantics |
| B3 pathspec | drop `'--'` separator | survived | not killed (incl. out-of-range ref named `plans/round-38-claims.md`) | equivalent on plausible inputs |
| C1 exit-map | `1 if drift else 0` → `0 if drift else 1` | killed C1,C2 | — | guarded |
| C2 exit-map | `1 if drift else 0` → `2 if drift else 0` | killed C1 | — | guarded |
| C3 exit-map | verdict string → always `'clean'` | killed C1 (oracle reads JSON verdict) | — | guarded (calibration note: verdict field IS pinned) |
| C4 exit-map | unknown-revision `finish(…, 2)` → `…, 1` | survived | FX-unknown-rev (rc 1, exp 2) | missing test: unknown-rev exit |
| D1 defaults | drop `plans/round-38-claims.md` | survived | FX-claims (rc 0 — claims-only drift missed) | missing test: claims-doc-only commit |
| D2 defaults | drop `tools/round-38/c1-counter.py` | killed C1 (f1010f67 vanishes) | — | guarded — this path is the only load-bearing arm in lane history |
| D3 defaults | drop `tools/round-38/c2-counter.py` | survived | FX-c2 (rc 0) | missing test: dead arm in range |
| D4 defaults | drop `.ufo/waves/round-38/c1/carriers.json` | survived | FX-carriers (rc 0) | missing test: dead arm in range |
| D5 defaults | drop oracle glob `corpus/evidence/round-37/c1/*/oracle.tsv` | survived | FX-glob-K1 (rc 0) | missing test: dead arm in range |
| D6 defaults | `DEFAULT = []` (log all paths) | killed C1,C2 (extra commits) | — | guarded (needs set-equality oracle) |
| E1 log-parse | range `f'{freeze}..{rev}'` → `f'{rev}..{freeze}'` | killed C1 | — | guarded |
| E2 log-parse | range → `f'{freeze}~1..{rev}'` (include freeze) | killed C1,C2 | — | guarded |
| E3 log-parse | drop `--name-only` | survived | FX-pathattr (drift entries carry `paths: []`, exit/ids still right) | missing test: path attribution |
| E4 log-parse | `%H` → `%h` (short ids) | survived | killed **only** by strict full-40-hex oracle; passes a prefix-id oracle | oracle-sensitivity finding (below) |
| E5 log-parse | `split('\t', 2)` → `split('\t')` | survived | FX-tab-subject (crash: ValueError on 4-field line, rc 1, no JSON) | missing test: tab in subject |
| E6 log-parse | drop `cur is not None` guard | survived | not killed (9 fixture cases + 3 lane cases) | equivalent by construction |

## Missing tests named (each = surviving mutant class)

1. **Dead default arms (D1, D3, D4, D5).** In the only lane-history cases the claim cites, three of five default paths never match and the claims doc is never isolated (79f6934 always co-touches the counter). The battery cannot detect corruption of those arms. Killers: one lane case per arm — a post-freeze commit touching only `plans/round-38-claims.md` / `c2-counter.py` / `carriers.json` / an `oracle.tsv` under `corpus/evidence/round-37/c1/*/`.
2. **Pathspec glob mapping (B1, B2).** No case exercises the one wildcard arm. Fixture shows both failure directions: dropping `:(glob)` over-matches deeper paths (`K1/sub/oracle.tsv` → false drift), `:(literal)` under-matches (missed drift). Baseline fact confirmed: pristine `:(glob)` does **not** recurse (`FX-glob-deep` clean) — the round-37 oracle glob is single-level by design.
3. **Unknown-revision exit (C4).** The documented exit 2 for unknown revs is never exercised by the lane cases.
4. **Path attribution (E3).** The lane oracle checks exit + commit ids but never that each drift entry names the paths that caused it; `--name-only` could silently vanish.
5. **Hash-width oracle unspecified (E4).** The human expectation ("listing 79f69347 and f1010f67") is prefix-form; a `%h` mutant passes a prefix oracle and fails only a strict full-hash oracle. Pin the oracle (full hash) or accept short ids explicitly.
6. **Tab-in-subject parsing (E5).** Any future commit whose subject contains a literal tab crashes the parser (uncaught ValueError → rc 1, no JSON). One fixture commit kills it.
7. **Equivalent mutants (not test gaps): B3, E6.** B3 (`--` dropped): with a branch named exactly like a default path (even pointing out of range), git still resolves the arg as pathspec and output is identical. E6: git log always emits the commit header line before path lines, so the dropped guard is unreachable on any `git log` output. These are coverage non-findings by construction.

## Core-detection statement

Every mutation that could make the gate **miss the M38-1 amendment pair** is killed by the lane cases: ancestor-check removal/inversion (A2/A3), range inversion/inclusion (E1/E2), exit-code inversion/remap (C1/C2), dropping the c1-counter default (D2 — the only arm f1010f67 matches), and emptying the default set (D6). The 79f6934+f1010f67 detection core of the R38-C1 honest-stop gate is well-guarded by the case battery; the periphery (other arms, glob semantics, formatting, unknown-rev) is not.

## Restoration and hygiene evidence

- Lane file never written; sha256 before and after all runs: `c213bc2d1d82c8673f8c44e0a9cc252d29df25400a73b27ef95b86663687ed5d` — exact (see `restoration.json`).
- Pristine scratch copy hash equals lane hash; restored copy plus baseline outputs archived to `.ufo/waves/round-38/w2/artifacts/R38W2MutFreezeDrift/` (`pristine.py`, `c1.out`, `c2.out`, `c3.out`, `results.json` (lane battery), `fixture-results.json`, `restoration.json`, subject copy).
- Fixture repos created per bounds (`mktemp -d "$S/fx.XXXX" && git init -q`, toplevel verified equal to `$D` before first commit); throwaway identity (`mutfix`) used only inside fixtures; no VCS-mutating git anywhere in the lane.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2MutFreezeDrift` removed at the end (artifacts exported first).
- Tooling: nothing installed (python3 + git already present). No pacman transactions.
- Incident, disclosed: one fixture-build cell ran `git init -q` without `-C`, re-initializing the existing fleet repo `.git` at `/home/vgpnk/Projects/shokunin`. Git documents re-init as safe/non-overwriting; fleet HEAD (`8cfcb5b6 round-35: kasegi report erratum 2`) and lane reads verified intact immediately after; the fixture build was then redone correctly (`git -C "$D" init -q`).
- Limits: single branch topologies tested; findings are about the test battery's coverage, not the tool's contract; [INFERENCE] B3's equivalence is proven only over plausible inputs (path-as-committish pathological cases untested).

## Addendum (2026-10-26 04:12, post-probe observation)

All verdicts above apply to the **frozen landed bytes** sha256 `c213bc2d1d82c8673f8c44e0a9cc252d29df25400a73b27ef95b86663687ed5d` (= blob at 3b960fe5; archived as `artifacts/R38W2MutFreezeDrift/pristine.py`). At 04:09:48 — after my probe window closed and without any write from this seat — an **uncommitted** working-tree edit appeared (`git status`: ` M tools/round-38/freeze-drift.py`), adding `net_changed` / `ships_freeze_bytes` via `git diff --name-only <freeze> <rev> -- :<glob>paths`. Facts recorded, not judged: (a) the new lines are outside my 22-mutant battery — re-run the battery against the new bytes if that edit is adopted; (b) the new glob mapping reuses `:(glob)`, so missing-tests 1–2 (dead arms, glob semantics) extend to it; (c) the exit mapping still keys on `drift` only, so a restore-after-drift would exit 1 with `ships_freeze_bytes: true` — intended or not is the owner's call. Lane file untouched by this seat; scratch removed.
