PARTIAL

# Verify18Review: round-18 `verify.py` review (wave 2, falsify)

- **Revisions:** REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline B `9011581d84527ba34c675f9cf912e54d2e72d470`, freeze F `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
- **Line numbers:** every `path:line` is from `git show REV:path`.
- **Seat:** author-side advisory. This report is a recommendation only.
- **Lane state when read (read-only):** HEAD = `refs/heads/main` = `refs/remotes/origin/main` = REV. `git status --porcelain --untracked-files=no` was empty.

## The four questions

| Question | Answer | Basis |
|---|---|---|
| Does it pin `source` via revpin? | HOLDS | :90-100 loads `tools/revpin.py` and calls `resolve_source(LANE)` with its defaults (require_head, require_pushed). `source` is `refs/heads/main^{commit}` (revpin.py:98). HEAD is never used as the revision. There is one call, at :92. |
| Does it refuse before running? | HOLDS for revpin findings | In the sandbox, S1 and S2 (F8) exit 2 and create zero files. Caveats: F3 (a dirty worktree is not refused) and F8 (exit code and record shape). |
| Does it cover every r18 counting command and selftest? | PARTIAL | The C1, C2 and C3 count commands are all present. Missing: the `run-carriers.sh` selftest, the frozen C3 binding gate, and the items listed under "Missing commands". At REV, the pass would exit 1 (F1). |
| Does it avoid overwriting r17 evidence? | HOLDS | All writes go under W18: OUT=`W18/verify` (:33), `W18/verification.json` (:288), `W18/custody/custody-r18.v2.txt` (:257), and `--out` into OUT (:152, :191, :264). W17 appears only as tool and pin paths (:29, :32, :104-107, :160-162). The pass never invokes `r17/verify.py`, whose :15-17 warns that a rerun overwrites r17 evidence. Observed: after 15 selftests, the real lane's `git status --untracked-files=all -- .ufo/waves/round-17 .ufo/gates` was unchanged, and the sandbox showed no new files after the replay and refusal runs. |

## Findings, by severity

### F1 (HIGH, operability, observed): at REV the pass cannot exit 0

- verify.py:157-159 runs `routed-defects.py --selftest` and expects exit 0. At REV that selftest exits 1.
- **Cause:** b2aad08's L1 amendment made the substance check require both `mid_map_sha256_mismatch` and `mid_map_compare_mismatch` (routed-defects.py:282). The "closed" fixtures still carry the old id: `FINDING = "mid_map_mismatch"` at :914 and `# finding mid_map_mismatch` at :1145.
- **Effect:** `unexpected_exits` will include `selftest-routed-defects`, so verify.py:294-295 returns 1.
- The harness's coverage is what catches this; the defect is in `routed-defects.py`. The C1 count itself is unaffected: 6 at B, 0 at REV.

Reproduction (sandbox D, see Setup):
- `python3 -I -B $D/sb/.ufo/waves/round-18/tools/routed-defects.py --selftest` gives **exit 1**:
  `SELFTEST: FAILED closed-fixture-cli: rc=0 opened=['R17-PINMAP', 'R17-PRODUCER-REV'] broken=['receipt-validate-mid-finding', 'producer-revs-are-ancestors']; closed-fixture-inprocess: open_count=1 broken=['receipt-validate-mid-finding']; token-only-*: … extra_open=['R17-PINMAP']`
  The extraction X gives the same exit 1.
- `git -C $D/sb show $F:.ufo/waves/round-18/tools/routed-defects.py > $D/rd-F.py && python3 -I -B $D/rd-F.py --selftest` gives **exit 0** (`SELFTEST: CLEAN cases=17`). The regression is new in b2aad08.

### F2 (MEDIUM, calibration, observed; latent at REV): the pass does not check the frozen C3 binding gate

- **The frozen gate:** predictions/decision-rule.json:2 (frozen at F; predictions are byte-identical at REV) reads: "a label counts only if receipt-validate.py --require-mid-maps exits 0 on its receipt, the bound log's carrier sha256 equals the prediction's, and the prediction blob is unchanged from the freeze commit".
- **What the pass does:** verify.py:201 runs receipt-validate in r17-lax mode, without `--require-mid-maps` (flag defined at receipt-validate.py:1020). No command checks the carrier-sha clause or the freeze-blob clause.
- **Reproduction:** `git show $REV:.ufo/waves/round-18/verify.py | grep -n -E 'run-carriers|require-mid-maps'` prints only `110:`, which is the pin entry.
- **All three clauses hold at REV when run:**
  - `receipt-validate.py --require-mid-maps <receipt>` for each of the 15 labels: 15/15 exit 0. Without the flag: also 15/15 exit 0.
  - Prediction `carrier.sha256` equals receipt `carrier.sha256_pre` and `carrier.sha256_post` for 15/15 labels.
  - `git -C $L diff --quiet $F $REV -- .ufo/waves/round-18/predictions` exits 0.

### F3 (MEDIUM, calibration, observed): a dirty tracked worktree is recorded but not refused, yet the pass runs working-tree bytes

- verify.py:101 and :280 only record `git status --porcelain --untracked-files=no`.
- The only refusal path is `except revpin.RevPinError` (:93-99), and revpin never looks at the worktree (revpin.py:93-122).
- Every tool runs from working-tree paths, including the revpin module itself (:38, :90). So `source_revision` can name bytes that never ran.
- `r17/verify.py` at REV refuses this state with `worktree_dirty` (:98-99), as contract.md:83-85 requires.

Reproduction (sandbox D, with HEAD = main = a fake `refs/remotes/origin/main` = REV, and one comment line appended to `.ufo/waves/round-18/measure.py`):
- A harness loads the REV verify.py, points its path globals at the sandbox, and stubs `os.makedirs` to raise. It prints `REACHED os.makedirs(SB/.ufo/waves/round-18/verify) -> no refusal` and exits 0.
- In the same state, r17 `resolve_source()` returns `['worktree_dirty']`.

### F4 (MEDIUM, coverage, observed): the new `run-carriers.sh --selftest` is never run

- `run-carriers.sh` is new in round 18 and has a selftest (:14-18, :32-165, :167-170).
- verify.py only pins it (:110), although its own comment at :154-156 says every new or edited tool is selftested.
- **Reproduction:** the grep under F2 shows only `110:`.
- **Result when run:** `bash $X/.ufo/waves/round-18/run-carriers.sh --selftest` exits 0 (`SELFTEST: CLEAN cases=21`) and leaves no `$HOME/.r18-run-carriers-guard-*`.

### F5 (LOW-MEDIUM, depth, observed; latent): the pass never re-derives a C3 observation from the bound log

- verify.py:205-207 prefers a retained `observation.json`. It runs log-extract only when that file is absent (:208-219).
- All 15 run dirs track that file: `git -C $L ls-tree -r --name-only $REV .ufo/waves/round-18/runs | grep -c '/observation.json$'` prints `15`.
- **Consequence:** the `log-extract-*` commands never run, and compare (:231-232) re-reads the same stored input that `run-carriers.sh:280-281` produced. This happens although `log-extract.py` was edited this round.
- The r17 pass always re-extracted (r17/verify.py:148-151).
- **When run:** for all 15 labels, `log-extract.py --log <bound ghidra.log>` matches the retained file except for `log_path`. Compare exits 0 for all 15 and matches compare.json except for the `observation` and `prediction` path fields.

### F6 (LOW-MEDIUM, calibration, observed): an exit-code-only check cannot see a "could not evaluate" result from measure

- verify.py:127 judges each command by its exit code alone.
- By its own contract, measure.py exits 0 when it emits `could_not_evaluate: true` (measure.py:25-29).
- **Reproduction:** `python3 -I -B $D/sb/.ufo/waves/round-18/measure.py $B` exits 0 and reports `could_not_evaluate: true`. C1 and C2 report `status: could-not-evaluate` with `reason: tool_absent_at_rev`.
- **Consequences:**
  - `measure-baseline` is recorded as expected but only measures C3=0.
  - An unevaluable `measure-source` would also pass silently.
  - The baseline numbers (6 defects, 3 live sites) come only from `routed-defects-baseline` and `head-rev-lint-baseline-strict`.

### F7 (LOW, operability; inference from code plus observed leftovers): custody-pair selftest scratch lands inside the lane and is never removed

- verify.py:165-168 passes `--scratch W18/verify/scratch-custody`.
- custody-pair's `cmd_selftest` creates `mkdtemp(prefix="custody-pair-selftest-", dir=base)` at :867 and prints it at :1393, but never deletes it: `git show $REV:.ufo/gates/custody-pair/custody-pair.py | grep -c rmtree` prints `0`.
- **Observed:** with its default base /dev/shm (:721-728), there are 8 leftover dirs of 80-85 entries each (`ls -d /dev/shm/custody-pair-selftest-* | wc -l` prints 8).
- **Inference:** the pass will leave a fixture tree under `.ufo/waves/round-18/verify/scratch-custody/`.
  - `.gitignore` (only `__pycache__/` and `*.pyc`) does not exclude it, and the `__pycache__` check at :269-270 does not see it.
  - A jj snapshot or commit would carry it.
  - contract.md:11 wants fixtures created outside LANE and removed.

### F8 (LOW, operability, observed): the refusal record is thin, and a bad baseline exits 1 instead of 2

- **Refusal record:** stdout gets only `{refused, revpin_finding, source}`. It drops `exc.result` (head, source, remote; documented at revpin.py:25-29), and nothing is retained on disk. `r17/verify.py` prints the full resolution (:110).
- **Bad baseline:** the baseline is parsed with `check_output` before revpin runs (:87). An invalid baseline gives a traceback and exit 1, not the could-not-evaluate exit 2 of contract.md:9-10.

Sandbox runs of the harness:

| Run | State | Result | `git status --untracked-files=all` after |
|---|---|---|---|
| S1 | origin removed; HEAD = main | exit 2, `branch_not_pushed` | empty |
| S2 | fake origin ref = tip; detached off-branch commit | exit 2, `head_not_branch_tip` | empty |
| S3 | baseline `000…0` | exit 1, `subprocess.CalledProcessError … rev-parse --verify 0000…^{commit} … exit status 128` | empty |

### F9 (LOW, latent)

- **Pin scope:** :112-113 pins only top-level files, so the 15 frozen emulator outputs in `predictions/swiss-misread/` are not pinned. A one-liner over the predictions dir counts 18 files pinned and one excluded dir, `swiss-misread`, holding 15 files.
- **No re-pin:** the pin is resolved once (:92) and never re-checked at the end of the pass.
- **Comment rows:** `run_labels` (:64-80) does not skip `#` rows, while `run-carriers.sh:206` does. Neither file has such rows at REV.
- **Custody capture:** `custody-capture` has no expected exit (:255-258), so `exit_as_expected` is always true.

## Missing commands to add to verify.py

1. `bash W18/run-carriers.sh --selftest`, expecting 0 (F4).
2. `receipt-validate.py --require-mid-maps runs/<label>/receipt.json` for all 15 labels, expecting 0 (F2).
3. The other two binding-gate clauses (F2):
   - each label's prediction `carrier.sha256` equals the receipt's `carrier.sha256_pre` and `sha256_post`;
   - `git diff --quiet eb6c266 <source> -- .ufo/waves/round-18/predictions`, expecting 0.
4. `log-extract.py --log runs/<label>/logs/<bound>/ghidra.log` for all 15 labels, diffed against `observation.json` with `log_path` ignored (F5).
5. `swiss-misread.py --carrier <path> --golang-root <G>` for all 15 labels, diffed against `predictions/swiss-misread/<label>.json`, plus the calibration acceptance in contract.md:119-120.
   - When run: 15/15 identical, aether `predicted_eof_reads_h1` = `[[17645861, 111938854]]`, 0.2-0.5 s each.
6. A decision-rule verdict (confirmed, refuted or unresolved). No tool in the round applies `decision-rule.json`; its only reference is the writer at `gen-predictions.py:91`. So the pass does not check the C3 status transition.
7. A red-before exercise of the edited `r17/verify.py` refusal. `jj-red-before.py` steps cover citation-drift, custody-pair and revpin, with 0 `round-17/verify` references. The third C2 site is only linted statically.
8. `routed-defects.py --rev B --strict`, expecting 1: the C1 red-before, mirroring :183-184 for C2.
9. Optional (unchanged since r17):
   - selftests of `buildinfo-probe.py` and `predict.py`, which `gen-predictions.py:43-46` uses;
   - a re-check of the carriers' `SHA256SUMS`;
   - custody-pair `verify` pairing.

## Commands I ran (with exit codes)

### Setup

- `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; REV, B and F as above.
- `X=$(mktemp -d); git -C $L archive $REV .ufo corpus SCORECARD.md LOG.md SKILL.md | tar -x -C $X` (exit 0).
- `D=$(mktemp -d /tmp/v18clone.XXXXXX); git clone -q --no-local $L $D/sb; git -C $D/sb remote remove origin; git -C $D/sb checkout -q -B main $REV` (exit 0; `remotes=[]`).

### Selftests from X (`python3 -I -B <tool> --selftest`)

| Tool | Exit | Cases |
|---|---|---|
| revpin | 0 | 11 |
| routed-defects | **1** | — |
| head-rev-lint | 0 | 3 |
| swiss-misread | 0 | 15 |
| carrier-run | 0 | 3 |
| compare | 0 | 23 |
| invocation-audit | 0 | 6 |
| log-extract | 0 | 13 |
| pins | 0 | 7 |
| receipt-validate | 0 | 18 |
| temporal-sweep | 0 | 7 |
| measure | 0 | 68 |
| controls | 0 | 23 |
| citation-drift-probe | 0 | 15 |
| `bash run-carriers.sh --selftest` | 0 | 21 |

### Replay of the pass's commands in D/sb

| Command | Exit / expected | Output |
|---|---|---|
| routed-defects-baseline | 0 / 0 | `open_count` 6 |
| routed-defects-source | 0 / 0 | `open_count` 0 |
| routed-defects-source-strict | 0 / 0 | — |
| head-rev-lint-baseline-strict | 1 / 1 | live 3: citation-drift-probe.py:477, custody-pair.py:327, verify.py:59 |
| head-rev-lint-source-strict | 0 / 0 | live 0, fixture 15, annotated 6 |
| measure-baseline | 0 / 0 | `could_not_evaluate` true |
| measure-source | 0 / 0 | C1 0, C2 0, C3 15 of 15 with extra |
| controls | 0 / 0 | — |
| citation-drift-strict | 0 / 0 | — |
| temporal-sweep-source | 0 / 0 | — |
| invocation-audit-source | 0 / 0 | — |
| sources-census | 0 / 0 | stdout includes `W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes` |
| receipt-validate, all 15 labels | 0 | — |
| compare, all 15 labels | 0 | — |

### Deliberately not run

- **jj-red-before** (both the run and its selftest): it uses jj on a lane clone. The retained `evidence/jj-red-before.json` was not re-derived.
- **custody-pair selftest and capture:** both hash `CUSTODY_PATHS` (custody-pair.py:217-223), which include `~/.omp/agent/mcp.json` and `~/.config/devin/mcp_config.json`. Those may hold credentials, which the host rule forbids reading.
- **The pins CLI.**
- **The full `verify.py` main path.**

## Residual risk and verification gaps

- In the pass itself, I did not observe exit codes for `jj-red-before` or the custody-pair selftest. The predicted `unexpected_exits` at REV include at least `selftest-routed-defects`.
- F7 is inferred from code plus the /dev/shm leftovers; I did not observe it in a lane run.
- The sandbox harness redirects only the path globals (LANE, W17, W, T, T17, OUT, RUNS, PREDICTIONS, GATES, REVPIN). F3 additionally stubs `os.makedirs` to stop at the first write. The REV bytes are otherwise unmodified.

Tools installed or updated: none.
