DEFECTS FOUND — on the lane history `freeze-drift.py` is correct (exit 1 at `e059ca93..0fc61133`, listing exactly the two attempt-1 amendments plus the harness fix), but fixture exercise produces **two false-clean classes** (evil merge that restores the freeze bytes, `--root` pointed at a subdirectory) and **three scope gaps** (recursive oracle globs, default set missing the harness, silent unmatched path).

Seat: `R38W2FreezeDriftFixtures`. Tool under test: `tools/round-38/freeze-drift.py`, sha256 `c213bc2d1d82c8673f8c44e0a9cc252d29df25400a73b27ef95b86663687ed5d`, byte-identical at `3b960fe5`, `0fc61133` and `HEAD` (`e265533e`); the tool is **absent at the first freeze** `e059ca93` (`git show e059ca93:tools/round-38/freeze-drift.py` → fatal: path exists on disk, not in that commit). Everything below is advisory: no lane file, tool, predicate, counter, carrier or oracle was modified; no VCS mutation; no tool installed.

## 1. Lane run (the instrument set from `instruments.json`)

All runs are read-only `git log` inside `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

| run | path set | exit | commits listed |
|---|---|---|---|
| full instrument set | claims, c1-counter, c2-counter, `c1-run.sh`, carriers, `corpus/evidence/round-37/c1/K*/oracle.tsv` | **1 drift** | `f1010f67` (c1-counter) · `79f69347` (claims, c1-counter, c1-run.sh) · `cb4326b2` (c1-run.sh) |
| + receipts (`corpus/evidence/round-38/c1/K*/after.json`) | same + receipts | **1 drift** | above **+ `3b960fe5`** (K1–K4 `after.json`) |
| tool default (no paths) | claims, both counters, carriers, `…/c1/*/oracle.tsv` | **1 drift** | `f1010f67`, `79f69347` — **misses `cb4326b2`** (default set has no `c1-run.sh`) |
| whole `tools/round-38` dir | directory pathspec | **1 drift** | `3b960fe5` (freeze-drift.py), `f1010f67`, `79f69347`, `cb4326b2`, `efd5c47a` (gen-controls.py) |
| `e059ca93..3b960fe5` | full instrument set | **1 drift** | `f1010f67`, `79f69347`, `cb4326b2` (identical to the `0fc61133` run) |

Static corroboration, blob ids freeze → measured revision:

```
plans/round-38-claims.md       e8bb4023 -> 9c665731  CHANGED
tools/round-38/c1-counter.py   8e33ac68 -> 115085f0  CHANGED
tools/round-38/c1-run.sh       96666472 -> ce44122c  CHANGED
tools/round-38/c2-counter.py   04a0bc63 -> 04a0bc63  SAME
.ufo/waves/round-38/c1/carriers.json ef925998 -> ef925998 SAME
corpus/evidence/round-37/c1/K1/oracle.tsv 4ee55253 -> 4ee55253 SAME
```

Every changed instrument is attributed to a listed commit; nothing is unaccounted. `3b960fe5` and `0fc61133` touch **no** frozen instrument, so the attempt-2 landing neither amended the counters further nor re-froze them — the bytes scored at the measured revisions are the post-amendment (v2/v3) bytes, which is exactly the condition the first-freeze rule exists for. This confirms the direction of the M38-1 finding and adds the interval the L1's own receipts never covered: the recorded gate runs are `077e212b` (drift), `cb4326b2` (clean), `gen-controls` (drift), all with the 5-path default set (`.ufo/waves/round-38/l1/freeze-drift-*.json`); **no receipt exists at either measured revision** (`3b960fe5`, `0fc61133`). The runs above supply it.

## 2. Fixture matrix

Repos built per the scratch rule (`D=$(mktemp -d "$S/fx.*")`, `git -C "$D" init -q`, toplevel verified `== $D` before the first commit, throwaway identity only inside the fixture, `S=/fast/scratch/hyaku/kaidoku-r38/R38W2FreezeDriftFixtures`, `TMPDIR=$S`). Scripts and logs: `.ufo/waves/round-38/w2/artifacts/R38W2FreezeDriftFixtures/{fx.sh,fx2.sh,fx3.sh,fx*-run.log}` (`MANIFEST.sha256` there).

| # | case | expected | exit | output |
|---|---|---|---|---|
| a | clean history, 3 commits, none in set | 0 | **0** | `drift: []`, `verdict: clean` |
| b | c1 counter edited after freeze (+ later unrelated commit) | 1 | **1** | edit commit, path `tools/round-38/c1-counter.py`; `--json-out` file byte-identical to stdout |
| c1 | `corpus/evidence/round-37/c1/K1/oracle.tsv` edited | 1 | **1** | path `…/K1/oracle.tsv` |
| c3 | same range, explicit `…/c1/K*/oracle.tsv` | 1 | **1** | identical to c1 |
| c-deep | only `…/c1/K2/deep/oracle.tsv` added (clean range) | 1 | **0** | **clean — escaped** (see D3) |
| d | `git mv c1-counter.py c1-counter-renamed.py` | 1 | **1** | path = old (frozen) name |
| d2 | body edited afterwards under the new name | 1 | **1** | rename commit only (range still drift) |
| d3a | rename **into** a frozen name absent at freeze | 1 | **1** | path `tools/round-38/c2-counter.py` |
| d3b | rename **over** an existing frozen path | 1 | **1** | path `tools/round-38/c2-counter.py` |
| e1 | conflict-resolution merge edits claims | 1 | **1** | merge listed with `paths: []`, both parents listed |
| e2 | evil merge, merge-only change | 1 | **1** | merge listed, `paths: []` |
| e3 | plain merge introducing side's claims edit | 1 | **1** | side commit listed; merge pruned by simplification |
| e-rev1 | linear edit then revert (rev bytes == freeze bytes) | 1 | **1** | both commits listed |
| e-rev2 | merge reverts a mainline amendment | 1 | **1** | merge (`paths: []`) + amend commit |
| e-rev3 | side amendment + evil merge restoring freeze bytes | 1 | **0** | **clean — escaped** (see D1) |
| f1 | freeze not an ancestor of rev | 2 | **2** | `reason: freeze is not an ancestor of rev` |
| f2/f3 | unknown freeze / unknown rev | 2 | **2** | `reason: unknown revision …` |
| f4 | freeze == rev | 0 | **0** | empty range |
| g1 | oracle under a directory with a space | 1 | **1** | path with space intact |
| g2 | path absent at freeze, created later | 1 | **1** | created path listed |
| g3 | explicit path that never existed | 0 | **0** | silent, no warning (D5) |
| g4a | chmod-only change to the counter | 1 | **1** | path listed |
| g4b | regular file replaced by a symlink | 1 | **1** | path listed |
| g8 | directory pathspec `tools/round-38` | 1 | **1** | per-file paths |
| g9a | `--freeze` given a tag | 1 | **1** | resolves |
| g9b | shallow clone without the freeze object | 2 | **2** | `unknown revision …` (safe) |
| del | instrument deleted after freeze | 1 | **1** | path listed |
| s1c | symlink target mutated, link blob unchanged | 1 | **0** | clean (limitation, S1) |
| r1a | `--root` = subdirectory, default set | 1 | **0** | **clean — escaped** (see D2) |
| r1b | `--root` = subdirectory, path relative to that root | 1 | **1** | resolves |

Two fixtures were invalid as first built and are reported as such rather than counted: `fx.sh` (d3) and `fx2.sh` (d3a) both issued `git mv` against an existing destination (`fatal: destination exists`), so freeze and rev were the same commit; the rename-into cases were rebuilt in `fx3.sh` (d3a/d3b) and those results are the ones tabulated.

## 3. Defects

**D1 — false clean when a merge restores the freeze bytes (P1, correctness).** `fx3.erev3`: freeze → branch `side` commits `d2c8346` "side amends claims" → mainline unrelated commit → `merge --no-ff side` → the merge commit is rewritten to restore the freeze bytes. Between freeze and rev there *is* a commit that touched the claims doc, yet the gate prints nothing and exits 0. Cause: `git log` history simplification drops both the merge (TREESAME to the mainline parent in that path) and the branch commit. The docstring promises "if this gate prints any commit between the freeze and the measured revision" — here it prints none. Hazard is bounded: at the rev the instrument bytes equal the freeze bytes, so scoring at that rev is safe; what is false is the reader's conclusion "no amendment occurred". Raw `git log -m` on the same range lists `ba3d718` (merge) and `d2c8346`; `--full-history -m` lists both **with** the path populated. Fix: add `-m` (and `--full-history`); verified on the fixture, no other case in the matrix changes its exit code.

**D2 — `--root` at a subdirectory yields a false clean (P2, misuse hazard).** `fx3.r1`: `--root <repo>/tools` with the default set exits 0 while `tools/round-38/c1-counter.py` was edited in range. `git -C <subdir>` resolves pathspecs relative to the subdir, so every default path matches nothing and the gate answers "clean" instead of erroring. No guard exists. Fix: resolve `--root` through `git rev-parse --show-toplevel` and anchor specs with `:(top)`; verified — `git -C <subdir> log -- ':(top)tools/round-38/c1-counter.py'` lists the edit.

**D3 — non-recursive oracle glob (P2, coverage).** `:(glob)corpus/evidence/round-37/c1/*/oracle.tsv` does not cross `/`, so a newly placed `c1/K2/deep/oracle.tsv` is invisible (c-deep: exit 0 over a range whose only change is that file). Today's tree is `c1/K1..K4/oracle.tsv` and `instruments.json` declares `K*`, so no current instrument escapes; the exposure is a future carrier laid one level deeper, or a carrier dir not beginning with `K`. Fix: `:(glob)corpus/evidence/round-37/c1/**/oracle.tsv`; verified — it lists both the deep file and the K1 edit where the current spec lists only K1.

**D4 — default set diverges from the declared instrument set (P3, completeness).** `DEFAULT` has no `tools/round-38/c1-run.sh`, yet `instruments.json` declares `c1_harness`. On the lane this is visible: the default run omits `cb4326b2` (a harness rewrite inside the scored interval), the 6-path run lists it. The L1's three recorded receipts all used the 5-path set. Fix: put `tools/round-38/c1-run.sh` in `DEFAULT` (and cite the instruments file in the usage text).

**D5 — unmatched path arguments are silent (P3, calibration).** `g3` (a path that never existed) and D3's deep path both exit 0 with no hint. For a gate whose clean verdict is trusted, a path that matches nothing at either endpoint should at least be echoed as a warning, or make the verdict `unevaluable`.

## 4. Calibration notes (not defects)

- **Merge commits carry `paths: []`.** `git log --name-only` prints no diff for merges, so a merge-only change is *detected* (exit 1, commit present because it is not TREESAME to either parent) but cannot be attributed to a file. Any report that reads `paths` as "the instruments touched" will under-read merge drift. `-m` fixes this too (D1's fix).
- **Receipts are listed as instruments but did not exist at the freeze.** `instruments.json` says "Every instrument below is committed at the freeze commit"; at `e059ca93` `corpus/evidence/round-38/c1/` and `.ufo/waves/round-38/controls/` are **absent** (controls appear at `efd5c47a`). Including `c1_receipts` in a drift run therefore flags the wave-2 landing commit `3b960fe5` — an output, not a scoring input. The 6-path set is the defensible one; the manifest's own note is false for `c1_receipts`, `controls_dir`, and the two out-of-lane entries (`xpin`, `census_script`).
- **The manifest never binds its freeze.** Committed once (at `e059ca93`, never updated) with `"frozen_at_commit": "{{FREEZE}}"` — the R36-CL4 substitute was never performed, so the committed map does not name the commit whose bytes are the rule.
- **The gate is not itself a frozen instrument.** It does not exist at the freeze and is not listed in `instruments.json`; nothing prevents a later revision of `freeze-drift.py` (or a re-run with a narrower path set, cf. D4) from producing a "clean" receipt. A fix that keeps the gate's promise should include the gate's own blob id in the frozen map.
- **Symlink semantics.** A frozen path that is a symlink is compared by its link blob: retargeting the link is drift (s1a), mutating the target is not (s1c, exit 0). Instruments are regular files today (`ls -l`, mode `100644`/`100755`), so this is latent only; it matters for any round that freezes a pointer or shim.
- **`--no-renames` is load-bearing.** Every rename case is caught *because* the old path is reported as a deletion. With rename detection on, `git log -- <old>` would also match, but `paths` would name the new file; a future edit under the new name would then be invisible. Do not drop the flag.
- Exit-code contract holds exactly as documented (0 clean / 1 drift / 2 unevaluable) across all 31 constructs; `--json-out` writes byte-identical JSON to stdout; refs (tags) work; a shallow clone lacking the freeze object fails closed (2, not 0).

## 5. Risks and limits of this seat

- I did not score C1/C2, did not re-run either counter, and did not touch any receipt or oracle. My evidence bears only on the *integrity of the freeze→measured-revision interval*.
- The fixture matrix is git-version-bound (`git 2.56.0`, Python 3.14.8). D1 depends on history simplification defaults, which have been stable for years but are not contractual.
- Nothing here was re-verified by a second run of the lane commands beyond the two I captured (`0fc61133` and `3b960fe5`, identical drift sets); no network, REA, or package tooling was involved.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2FreezeDriftFixtures` removed; every cited log lives under `…/w2/artifacts/R38W2FreezeDriftFixtures/` with sha256 in `MANIFEST.sha256`.
