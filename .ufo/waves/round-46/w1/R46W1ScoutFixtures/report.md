# R46W1ScoutFixtures — round-45 committed forgery evidence

Seat `R46W1ScoutFixtures`. Read-only on the lane. Freeze `31820472784284727546808acc31b3ea1e73919b`. No installs. Nothing under `/tmp` was written. Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1ScoutFixtures` held only the inventory listing and was removed after this report.

Axes used: coverage of every freeze path matching `fixture`; defect class taken from the committed bytes, not from the filename; whether a round-46 counter can see that defect from the file alone.

## Receipt

Command (exact):

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only 31820472784284727546808acc31b3ea1e73919b -- .ufo/waves/round-45 | grep -i fixture
```

Exit 0. Stdout sha256 `830b1cac3ddb528dec36810bf2db55ff257f07848c3bdd529c63d3f18f40f3fb`. UTC `2026-10-28T16:58:03Z`. 45 paths.

`git diff --stat 31820472784284727546808acc31b3ea1e73919b HEAD --` the ReviewC2 fixture dir, `R45W2Lesson/fx-a6-SKILL.md`, `R45W2Lesson/stub.py`, and `R45W1CritC1` was empty at `2026-10-28T16:57:53Z` (HEAD then `7bf33e312d75ad09d55df399814e9ae3ef7cee49`). Content sha256 below is of those worktree bytes, which matched the freeze at that time. Git blob ids are from `ls-tree -l` at the freeze.

## What round 46 can re-run

Round-46 counters do not take a bare path. `attest.py` and `registry.py` both `git show <rev>:SKILL.md` and run a freeze arm (`tools/round-46/attest.py` `evaluate`, `tools/round-46/registry.py` `evaluate`). A committed `SKILL.md` body is still one file inside a one-commit fixture repo, plus whatever scope file the spec names.

- `attest.py` scores a `## Queue-drain craft` block (`<!-- freeze-integrity-table v1 -->` under `--spec r45`, `v2` under the default). None of the 23 ReviewC2 fixtures contain that marker. They are registry tables. `attest.py` cannot score them.
- `registry.py --spec r45 --profile v1` is the port that still uses `rows_anywhere`, a loose backtick-path search, no header, and word-boundary digits 0, 1 and 2 (`registry.py` `SPECS["r45"]`, `score` when `profile != "v2"`). It also requires `tools/round-45/registry-scope.json` with exactly six paths. That scope file is **not** in `evidence/fixtures/`. Default `--spec r46 --profile v2` ignores rows that are not between `<!-- instrument-registry v2 -->` and `<!-- /instrument-registry -->`. None of these fixtures have those markers, so v2 registers nothing from them.

"Score directly" below means the defect is in the committed `SKILL.md` bytes, so the re-run is: one commit whose `SKILL.md` is that file, plus a six-path `registry-scope.json` and a claims file for the freeze arm. "Needs a repo" means the committed file does not contain the defect the label names.

## ReviewC2 fixtures (23 files)

Directory: `.ufo/waves/round-45/w2/R45W2ReviewC2/evidence/fixtures/`. All 23 are `SKILL.md` bodies (a `# SKILL` heading and a `### Round-44/45 instrument registry` table). Six of them are the same blob as the green control, so the filename's defect is not in the file.

Shared green blob `7a2a0908ebdbca3bfb9f23ecd711aa6025f1985a`, content sha256 `f397d3f1fb2b540105ad43beaeaffc2b7e10a64d8a7972246bd618b163504ad1`, 767 bytes: `F0-green`, `F5b-scope-json-post-freeze`, `F5c-new-file-in-frozen-dir`, `F5d-sibling-dir`, `F5e-claims-post-freeze`, `F5f-rename-out`. Twelve lines: header plus six exact rows for `tools/round-44/c1-counter.py`, `c1-run.sh`, `c2-counter.py`, `tools/round-45/frozen-path-preflight.py`, `c1-counter.py`, `c2-counter.py`, verdict cell `` `0` met; `1` not met; `2` could-not-evaluate ``.

| file | blob | content sha256 | defect the bytes encode | round-46 re-run |
|---|---|---|---|---|
| `F0-green.SKILL.md` | `7a2a0908` | `f397d3f1…504ad1` | none — honest six-row control (ReviewC2 exit 0, stdout `41db7a8581608ec8`) | direct body for `registry.py --spec r45 --profile v1` once a 6-path scope exists. Not an `attest.py` input |
| `F1a-dup-thin-first.SKILL.md` | `1af20b8d` | `e85bd839…9bc3e4` | first-wins: `c2-counter.py` thin cell `` `0` met; non-zero otherwise `` then a good duplicate (R45-CL14 c) | direct body |
| `F1b-dup-thin-second.SKILL.md` | `f6eaefae` | `1f4d1047…a7cc3` | same pair, good row first; v1 keeps the good row | direct body |
| `F2a-html-comment-only.SKILL.md` | `dd76b5b1` | `fdb6517b…f9b99f` | all six rows on their own lines inside an HTML comment (R45-CL14 a) | direct body. v1 `rows_anywhere` still sees them; v2 does not |
| `F2b-fenced-only.SKILL.md` | `6efbeddb` | `a75a1561…0c644f` | all six rows inside a triple-backtick fence, no header | direct body. Same v1/v2 split. Committed form of the R45-CL14 fenced-row class, but not the critic's 442-byte cheapest bypass |
| `F2c-inline-comment.SKILL.md` | `54f8098f` | `eeeef386…81146` | control: the `c2-counter.py` row shares the line with an HTML comment, so v1 does not parse it (ReviewC2 exit 1) | direct body |
| `F3a-trailing-text.SKILL.md` | `d8e7cb96` | `63d1f305…9fabc5` | cell 0 is the path plus ` (alias of the gate)` (R45-CL14 b) | direct body. v1 search hits; v2 exact-cell misses |
| `F3b-leading-text.SKILL.md` | `2f6b92c9` | `e6cd128b…21d6ed` | cell 0 is `see` plus the backticked path | direct body |
| `F3c-prefixed-path.SKILL.md` | `29c177cb` | `df7b32c8…984cb` | cell 0 is `` `vendor/tools/round-45/c2-counter.py` ``. v1 already misses it (regex requires `tools/`) | direct body. A negative control, not a hole |
| `F3d-two-path-scope-second.SKILL.md` | `a5a963db` | `db0aabae…67b5e8` | no row whose first path is `tools/round-44/c2-counter.py`; last cell names `tools/round-40/other.py` then the round-44 path. v1 registers only the first | direct body. Negative control |
| `F4a-prose-units.SKILL.md` | `be7d2704` | `91553571…64e825` | verdict cell `0 rows, 1 column, 2 bytes` (R45-CL14 d) | direct body. v1 digit-words pass; v2 `0=`/`1=`/`2=` fails |
| `F4b-decimal-prose.SKILL.md` | `a2a2ab80` | `ac909db5…37c179` | verdict cell `0.5 of a row, 1.5 columns, 2.5 bytes` | direct body. Same split |
| `F4c-control-missing-2.SKILL.md` | `6d67c3b3` | `81ee9693…a2b634` | verdict cell has `0` and `1` only. v1 already thin | direct body. Negative control |
| `F4d-control-bare-nonzero.SKILL.md` | `9f4c4b72` | `7c30befc…e6c3a9` | verdict cell `` `0` met; non-zero otherwise `` | direct body. Negative control |
| `F5a-skill-post-freeze.SKILL.md` | `243fa55d` | `8a48124e…ad8b21` | green table plus the line `post-freeze prose`. The probe was a second commit touching `SKILL.md`, which is not frozen (ReviewC2 exit 0, `frozen_path_changed []`) | needs a repo. One commit of this file does not exercise the freeze arm |
| `F5b` through `F5f` (five names) | `7a2a0908` | `f397d3f1…504ad1` | **no defect in the bytes.** Identical to `F0-green`. The probes were a post-freeze edit of `registry-scope.json`, a new file under `tools/round-45/sub/`, a sibling `tools/round-45-extra/`, an edit of `plans/round-45-claims.md`, and a rename of `c2-counter.py` out of the frozen dir | needs a repo. Those histories were not committed. Re-run from `R45W2ReviewC2/report.md` section A5, not from these files |
| `F6-scope-duplicate-path.SKILL.md` | `c7bca07a` | `a3e94214…00f577` | five rows; `tools/round-45/c2-counter.py` is absent. The reported defect is a scope list of six entries / five paths. That JSON is not in this directory | needs a repo. Scoring this body against a normal six-path scope yields `c2-counter` unregistered, which is not the recorded exit 0 / `scope_size 6` |
| `F7-ghost-instrument.SKILL.md` | `3bb63b03` | `b0442f9f…08e49d` | row names `tools/round-45/ghost.py` instead of `c2-counter.py` (R45-CL2). v1 `presence` is false, so a row is enough; the scope must list `ghost.py` | needs a repo. The substituted scope file was not committed. v2 would also need the blob absent at `--rev` |
| `F8-merge-commit-plants-frozen-file.SKILL.md` | `33094bcd` | `8009c625…725de3` | green table plus the line `feat line`. The probe was a merge that plants a file under `tools/round-45/` (R45-CL6; ReviewC2 exit 0, `frozen_path_changed []`) | needs a repo. The merge is not in the file |

Cheapest re-score set, without rebuilding history: the fourteen bodies F0, F1a, F1b, F2a, F2b, F2c, F3a through F3d, F4a through F4d, under `registry.py --spec r45 --profile v1`, each in its own one-commit repo with a six-path scope. Do not point `attest.py` at them. Do not expect default v2 to reproduce the round-45 exits: v2's marker gate rejects every one of them before the cell defect matters.

`evidence/receipts.json` in the same seat records the round-45 exits (F0 exit 0 `41db7a8581608ec8`, through F8 exit 0 `90873ef249e9b14a`). Those are counter stdout prefixes, not content hashes of the fixtures. Not re-run here.

## Other fixture paths at the freeze (22 files)

None of these is a `SKILL.md` body. A round-46 counter cannot score the file. The scripts rebuild a repo; the rest are receipts of repos that were not committed.

| path | what it is | re-run |
|---|---|---|
| `.ufo/waves/round-45/w1/R45W1C1Satisfy/fixture-driver.py` | C1 preflight harness. Builds repos under a dead scratch path. Holds the real eight-row canon, not the forgery | generator; needs a repo and the frozen `c1-counter.py`. Not the cheapest-green artefact |
| `.ufo/waves/round-45/w1/R45W1PreflightReplay/probe-fixture-toplevel.json` | receipt: fixture dir names and `toplevel_is_self: true` | not an input |
| `.ufo/waves/round-45/w1/R45W1RevFreezeCommit/fixtures/evil_merge_probe.sh` | builds a merge whose resolution rewrites `frozen/target.txt`, then calls both counters | generator; needs a repo. Re-runnable as a script. Default `mktemp` parent is `/tmp` — do not run it that way |
| `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/fixture_receipts.sh` | builds a repo with a non-ASCII name, a tab in a name, and a rename; prints `diff-tree --name-status` with and without `-z` | generator (S141). Needs a repo |
| `…/fixture-transcript.txt` | stdout of that script. Commit `12b56e7c…` is the scratch commit | receipt |
| `…/fixture.exit` | `EXIT=0` | receipt |
| `…/utc_fixture` | `2026-10-28T15:40:49Z` | receipt |
| `.ufo/waves/round-45/w2/R45W2CommandA/fixture-commits.txt` | three scratch SHAs | receipt. Repos not committed |
| `…/out-fixture-baseline.txt` | one JSON line, `rule_blocks 22`, `coverage_score 10.0`, rev `c4b3d819…` | receipt |
| `…/receipts-fixture.tsv` | label / exit / stdout sha256 / UTC for baseline, citation mutants, and gate arms | receipt |
| `.ufo/waves/round-45/w2/R45W2MutC1Landing/check-m0-pristine-fixture.json` | `c1-counter` stdout: `met_target true`, `block22_rows 10`, `refs 8`, freeze `bd3f27fc…` | receipt of a green C1 fixture, not the forgery. The fixture tree is not committed |
| `.ufo/waves/round-45/w2/R45W2PreflightReal/fixtures.py` | builds F1–F3 repos and imports `frozen-preflight.py` from a dead scratch path | generator; needs a repo. Will not start as committed |
| `…/f1-f3-fixtures.stdout` | JSON of those runs (F1 pathspec case, commit `eb52baef…`) | receipt |
| `…/f1-f3-fixtures.stderr` | empty file | receipt |
| `.ufo/waves/round-45/w2/R45W2Rollback/method/run_fixtures.sh` | dirty-worktree and history fixtures for block 22 | generator; needs a repo. Hardcodes scratch |
| `.ufo/waves/round-45/w2/R45W2Src141/fixture_battery.sh` | preflight battery over a private repo | generator; needs a repo |
| `.ufo/waves/round-45/w2/R45W2SweepAudit/receipts/fixture-merge-blindness.sh` | copies freeze blobs of the claims file and `tools/round-45/*` into a new repo, then merges | generator; needs a repo. Closest committed recipe for the R45-CL6 merge |
| `…/fixture-merge-blindness.out` | arm A and the name-status sweep both exit 0 and see nothing; the `-m` form shows `M plans/round-45-claims.md`. Merge `e072b41a…` | receipt |
| `.ufo/waves/round-45/w2/R45W2Trends/fixtures/commandA.py` | scores coverage against `git show <rev>:` of the lane, not a forged `SKILL.md` | not a forgery body |
| `…/fixtures/driver.py` | trend attacks; writes receipts under a dead scratch path | generator; needs a repo |
| `…/fixtures/receipts2.py` | more of the same, base `149133d4`, A3 `f59565b7` | generator; needs a repo |
| `…/receipts/dirty-fixture-state.json` | `git status --porcelain -z` saw a modified `frozen/a.txt` | receipt |

## R45-CL13 cheapest-green artefact

R45-CL13 names one digest, and it is a **receipt**, not the artefact. `corpus/lessons/round-45.md` (the R45-CL13 bullet) says `fx-a6-cheapest-green`, receipt sha256 `34336cf7…`. The full value is in `.ufo/waves/round-45/w1/R45W1CritC1/receipts.json` label `fx-a6-cheapest-green`:

`34336cf79d729e6a85a3ac7a3eda998388011213f33aaa1cba2d8187fcefc7d3`

That field is `stdout_sha256` of `counter.py --root …/fx-a6-cheapest-green --freeze 0588a84a7aed878dba6ba8e11cf777a8d7ef0099 --rev` the same commit. Exit 0. UTC `2026-10-28T15:42:01Z`. `stdout_head` is a truncated JSON object (`failing []`, `block22_rows 8`, `block22_refs 4`, `header_ok true`). The full stdout is not in the file. Stderr sha256 is the empty-string digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

That exact artefact is **not** committed.

- `git cat-file -t 0588a84a7aed878dba6ba8e11cf777a8d7ef0099` at the lane: fatal, exit 128. The fixture commit is not an object here.
- `git rev-parse --verify 34336cf79d729e6a85a3ac7a3eda998388011213f33aaa1cba2d8187fcefc7d3^{blob}`: fatal. The receipt digest is not a blob. It occurs as a hex string in `receipts.json`, `report.md`, and later commentary (`R45W2Pins` records the same disambiguation).
- The scratch tree (`SKILL.md`, the four-line stub, the citation stubs, `plans/round-45-claims.md`) was not saved under `R45W1CritC1/`. That seat committed `attacks.py`, `receipts.py`, `receipts.json`, `attacks-results.json`, `follow-results.json`, `report.md`.

What is committed, and is not the same object:

- Generator `.ufo/waves/round-45/w1/R45W1CritC1/attacks.py`, content sha256 `1e5c9ce9a232be7dce14a40981706fe8ae0ebf6b7b7e21f36a2e8a658581cfdb`. `a6()` writes 21 plain bullets, eight `lorem` rows, four `:1` refs, and `STUB` (single-quoted `print`). Import reads `preflight-real.py` from the dead scratch dir, so the file does not run as stored. A fresh `git commit` would also embed a new freeze id in the counter stdout, so `34336cf7…` cannot recur even if the `SKILL.md` text matches.
- Reconstruction `.ufo/waves/round-45/w2/R45W2Lesson/fx-a6-SKILL.md`, content sha256 `cc523958abcc3d484e89da26a7c2137461d8fbb4c440aee9ec4ad8c22632516a`, **40 lines**. It matches `a6()`'s text (heading `## Queue-drain craft (test)`, marker v1, `lorem 0` through `lorem 7`). `stub.py` beside it is 4 lines, content sha256 `815c2fe906045f52fb1b05f9f2dfddad383150b14234c02bb6629e2ca52c181e`, and uses double quotes, so it is not the generator's `STUB` literal.
- That seat's re-score (report.md R11) exited 0 with stdout sha256 `06c78c60199f8bd8196dfb00527eec8f4891c9dba201408c9eec7e361d0c93a2`, not `34336cf7…`. The report says the rebuild is 40 SKILL lines against the critic's "44", and that the receipt hash was not reproduced.

The "44 lines" figure is not recoverable as a committed line count. The critic's own parenthetical (21 bullets + 8 rows + 4 refs + a 4-line stub) sums to 37, not 44. The generator and the committed reconstruction are 40 SKILL lines. 40 + 4 = 44 only if the stub is counted in the same total. Unresolved: the scratch `SKILL.md` that produced `34336cf7…` was never hashed, so its line count is not in the tree.

`attest.py --spec r45 --profile v1` can score the committed 40-line reconstruction (it has the v1 marker, eight rows, four line-selected refs, and a stub that prints the selftest banner). That is a stand-in, not the artefact R45-CL13 names. Default v2 should reject it (wrong marker, no `23. ` title, garbage arm tokens, no `sha256:` pin). Not run here.

The C2 cheapest bypass (six fenced rows, 442 bytes, receipt `c5bd3c1ff4976c17e7f288c17f4cd3de0d1345e9e2b7926d121906dd7361eb0b` in `R45W1CritC2/c2-cheapest-bypass.json`) is also a stdout digest. The 442-byte `SKILL.md` is not a committed file. `F2b-fenced-only.SKILL.md` is a different, fully written six-row fence (content sha256 `a75a1561…`), and it is the one to re-run.

## Not run

The round-45 counters and the round-46 counters were not executed against these files. Exits cited above are copied from the committed receipts, not re-measured.
