# W2C1Drift — round 49 wave 2, post-landing freeze-integrity falsification

Lane `main`, landing revision `29883d4ec35a31a8393c4ffb220888c44c0bb022`, freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`.
Artifacts: `.ufo/waves/round-49/w2/W2C1Drift/` (`MANIFEST.sha256` lists every receipt and fixture result with its sha256).

## Verdict

**Counts reproduce at REV; the C1 freeze walk is not sound as written.** At REV, C1 exits 0 with `carriers_matched 4` and C2 exits 0 with `mismatches 0`, battery clean, as the plan expects. The freeze integrity that the plan's rule names does not hold for C1 in three reproduced ways (F1–F3). None of them changes the REV verdict: the lane has no quoted names, no copy/rename statuses and no pre-freeze-ancestry add under `tools/round-49/` or on the receipt paths at REV (checked). C2's freeze walk held in every attack I ran except a fail-closed false positive (F4). The three disclosed limits I re-tested (operator `--freeze`, `refs/replace`, counter bytes) behave exactly as the plan says.

## Findings (by severity)

| id | claim/counter | attack | exact command and result | plan sentence it breaks | evidence | status |
|---|---|---|---|---|---|---|
| F1 | R49-C1 freeze walk (`frozen_drift`, `c1-counter.py` lines 1638–1698; `is_frozen` 1649–1650; skip at 1668–1670) | Add a file under `tools/round-49/` whose name git C-quotes: `"`, `\`, or TAB (`core.quotePath=false` does not stop this; only non-ASCII is unquoted) | `python3 -I -B c1-counter.py --root fx/fx4-dquote --rev HEAD --freeze decc5697… --pkg65 … --work … --json-out …` → **exit 0, carriers_matched 4, frozen_path_changed []**. Same for `fx4-backslash` and `fx4-tab` (exit 0, matched 4). Control `fx4-nonascii` (`é.json`) → exit 2 `frozen_path_changed`; `fx4-plain` → exit 2. C2 on the same three fixtures → exit 2 `frozen_path_changed`, detail `A\t"tools/round-49/q\"x.json"` | "no commit … adds … a path under `tools/round-49/`"; "an added file counts" | `fixtures/fx4-{dquote,backslash,tab}.c1.json`, `.c2.json`; status lines with a leading `"` fail `startswith('tools/round-49/')`. Residual of wave-1 `CritFreeze` F2: the fix covered non-ASCII only | **reproduced; counter defect, not patched** |
| F2 | R49-C1 freeze walk | Copy-status blind spot: a file added as a copy of an existing one (git `C` status) is not an `A`. `C` is skipped: only `A` and `MDRTU` are handled (lines 1671–1683). Git emits `C` when `diff.renames=copies` is set in the repo or user config | Fixture `fx17-copy`, config `diff.renames=copies`: commit modifies `corpus/README.md` and adds `tools/round-49/copied-from-readme.md` (copy of the old README). `c1-counter.py` → **exit 0, carriers_matched 4, frozen []**. Same fixture with the config unset → **exit 2 `frozen_path_changed`**. C2 with copies config → exit 2 (its pathspec log reports it as `A`) | "no commit … adds … a path under `tools/round-49/`" | `fixtures/fx17-copies.c1.json`, `fx17-default.c1.json`, `fx17.c2.json`; raw line `C100\tcorpus/README.md\ttools/round-49/copied-from-readme.md`. Not in wave-1 record (no copies case in `CritFreeze`) | **reproduced; config-dependent counter defect, not patched** |
| F3 | R49-C1 `receipt_fresh` (`first_add` lines 1583–1588 = `git log --diff-filter=A -- path`, no `--full-history`; `receipt_fresh` 2099–2102) | Pathspec history simplification hides a non-descendant add. Build a branch from the base `e4f2cfa5` (pre-freeze ancestry) that adds the four `after.json` with identical bytes, and merge it into REV-lineage with the first parent already holding those bytes (merge is TREESAME to first parent, so simplification drops the side) | Fixture `fx13-datesort`, head `7a9fcc2a…`: `c1-counter.py` → **exit 0, carriers_matched 4**, all four `receipt_first_add = 4aabb0b…`, `receipt_fresh true`. `git log --full-history --diff-filter=A -- corpus/evidence/round-49/c1/v1le/after.json` lists `73d5b05c…` (parent `e4f2cfa5`, pre-freeze ancestry) **and** `4aabb0b…`. Control `fx14a`/`fx14b` (receipts deleted on main, then re-added from base; pre-freeze add visible) → exit 1, `receipt_fresh false` for all four (the counter refuses when the earlier add is visible) | "first added in a commit that descends from the freeze" | `fixtures/fx13-datesort.c1.json`, `fx14{a,b}-*.c1.json`; `fixtures/index.json` | **reproduced; provenance tie is defeated by history simplification, not by dates.** Lane at REV: `--full-history` adds for all four `after.json` = only `4aabb0b`, so the REV score is unaffected |
| F4 | R49-C2 freeze walk (`touched`, c2-mismatch.py 136–140; `freeze_check` 575–586) | Fail-closed false positive: `log -m --diff-merges=first-parent --name-status --format=%H -- tools/round-49 plans/…` emits a bare commit hash for merge `7a9fcc2a…` (fixture fx13) that touches no frozen path; any non-empty output counts as "touched" | `c2-mismatch.py --root fx/fx13-datesort --rev HEAD --freeze decc5697…` → **exit 2 `frozen_path_changed`**, detail `frozen path touched in FREEZE..REV: 7a9fcc2a…` with no file entry. An ordinary benign merge (fx15) → exit 0; trigger is merge-shape specific | none (over-refusal; the plan's rule is violated only in the refusing direction) | `fixtures/fx13-datesort.c2.json`, `fx15.c2.json`. Not in the wave-1 record | **reproduced; counter defect, fail-closed, not patched** |

## Freeze-integrity attacks that HELD (exit 2 as the plan requires)

Fixture = `git clone --shared` of the lane at REV, one attack commit (or merge) on `main`, identity set in that clone only, `git rev-parse --show-toplevel` asserted before commit. Counters run from frozen copies in scratch (`src/*.py`, sha256 identical to the FREEZE blob, verified). `GIT_NO_REPLACE_OBJECTS=1` set for every run. `fixtures/index.json` lists heads and descriptions.

| fixture | attack | C1 exit / reason | C2 exit / reason |
|---|---|---|---|
| fx0-none | control, no commit | 0, matched 4 | 0, mismatches 0 |
| fx1-edit | edit `control-fixtures/pos/manifest.json` | 2 frozen | 2 frozen |
| fx2-restore | edit, then restore | 2 frozen | 2 frozen |
| fx3-ours | side edit, `merge -s ours` (merge tree == REV; net diff empty) | 2 frozen | 2 frozen (the side commit is listed; history simplification did **not** hide it under `-m --diff-merges=first-parent`) |
| fx4-plain / -nonascii | add `plain.json` / `é.json` | 2 frozen | 2 frozen |
| fx5-rename | `git mv` frozen manifest out | 2 frozen | 2 frozen |
| fx6-delete | `git rm` frozen manifest | 2 frozen | 2 frozen |
| fx7-carrier | append byte to frozen carrier `v1-le--squashfs_v1.0_le.bin` | 2 frozen | 0 (expected: C2 binds only `tools/round-49` and the plan) |
| fx8-oracle | edit `corpus/evidence/round-44/oracle/manifest.json` | 2 frozen | 0 (expected, as above) |
| fx9-pins | edit `tools/round-42/prior-pins.json` | 2 frozen | 0 (expected, as above) |
| fx10-noncarrier | edit non-carrier `v2ns-le` fixture | 0, matched 4 (correct, not frozen) | 0 |
| fx11-mergeedit | `merge --no-commit` of a side branch (parents `29883d4e` and `5c0226b5`), then the frozen manifest edited in the merge commit itself | 2 frozen | 2 frozen |
| fx12-counter | edit `tools/round-49/c1-counter.py` (run the edited copy) | 2 frozen | 2 frozen |

Also verified at FREEZE..REV on the lane: `git log -m --diff-merges=first-parent --name-status` → 96 `A`, 10 `M`, no `R` or `C` lines; no merge commits changing frozen paths.

## Freeze, ancestry and provenance facts (read-only git, all at REV)

- `decc5697` (parent `14936cb9`, the wave-1 commit) is an ancestor of `76d7ad6`, `4aabb0b`, `3847f393`, `188ddeea`, `b58f9b19`, `29883d4e` (`git merge-base --is-ancestor`, exit 0 each). `decc5697` adds only `plans/round-49-claims.md` and `tools/round-49/**` (34 `A` entries, no `M`/`D`/`R`).
- `git log -m --diff-merges=first-parent --name-status --format=%H decc5697..29883d4e -- tools/round-49 plans/round-49-claims.md` → **empty**. `git diff --stat decc5697 29883d4e -- tools/round-49 plans/round-49-claims.md` → **empty**.
- `git diff --name-only decc5697 29883d4e -- tools/round-42 tools/round-39/gen-squashfs.py tools/round-27/xpin-attribute.mjs corpus/evidence/round-44/oracle` → **empty** (exit 0).
- Six commits in `decc5697..29883d4e`, all author and committer `kaidoku-shokunin <kaidoku@shokunin.local>`: `76d7ad6f` (2026-10-28 19:12:51 -0300, controls and FREEZE hash), `4aabb0b4` (19:13:11, C1 data run), `3847f393` (19:18:29, landing), `188ddeea` (19:18:56), `b58f9b19` (19:19:23), `29883d4e` (19:19:41).
- Sha256 of the counters (`git show <rev>:` and worktree agree): `tools/round-49/c1-counter.py` = `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` at FREEZE, REV and worktree; `c2-mismatch.py` = `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` at all three.
- `plans/round-49-claims.md` blob at FREEZE `a056a581a31041f23e5630315a252cd9c6d49fb2` (git blob id).
- Every explicit C1 frozen path exists at FREEZE (`ls-tree`): `tools/round-42/{fixtures.json,c1-counter.py,prior-pins.json,rea-pkg.json}`, `tools/round-39/gen-squashfs.py`, `tools/round-27/xpin-attribute.mjs`, the plan.
- Receipts: the four `corpus/evidence/round-49/c1/<id>/after.json` are first added (and only added) in `4aabb0b4`, which descends from `decc5697` (`merge-base --is-ancestor` exit 0) and is an ancestor of REV. `run.json`: `rev_at_run 76d7ad6…`, `started_utc` 22:12:58Z to 22:13:06Z, after the freeze commit (22:11:52Z) and before the data run's commit. `l1/FREEZE` content = `decc5697…`.
- Replace refs at REV: 0 (`git for-each-ref refs/replace`). No `.git/info/grafts`, no `.git/shallow`.
- Lane `freeze..REV` contains no status `C`/`R`, no quoted or non-ASCII name under `tools/round-49` (`ls-tree` grep → 0).

## Counting runs at the revisions (exact commands; outputs under `receipts/`)

Counters run from the lane worktree copy (sha256 identical to FREEZE, checked before each run) with `GIT_NO_REPLACE_OBJECTS=1`, `TMPDIR` and `HYAKU_SCRATCH` under `/fast/scratch/hyaku/kaidoku-r49/`.

1. `python3 -I -B tools/round-49/c1-counter.py --root <LANE> --rev 29883d4e… --freeze decc5697… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <S>/w/c1rev --json-out receipts/c1-rev.json` → **exit 0** (22:38:23Z–22:38:37Z). `carriers_matched 4`, `target 4`, `met_target true`, `carrier_ids [v1le,v1be,v2le,v2be]`, `frozen_path_changed []`, `failing []`, `bindings_false []`, `carriers_unchanged true`. stdout sha256 `ae830b210a799c2b5ec6a67dd629562f0b170e46574f3b70646003f6b6b64657`; json sha256 `deaf045f81f8b995e1190a8e63f7e3a90c301e69e342a10e40edef13b1a8d410`.
2. `python3 -I -B tools/round-49/c2-mismatch.py --root <LANE> --rev 29883d4e… --freeze decc5697… --battery` → **exit 0** (22:38:03Z). `atoms_total 9`, `mismatches 0`, `battery.failing []`, 16 mutations (A1 ×1, A2 ×1, A3 ×4, A4 ×1, A5 ×1, A6 ×3, A7 ×2, A8 ×2, A9 ×1 — each `ok`, red on exactly its own atom, `noop []`), `do_nothing_red` = A1–A9 (9), `do_nothing_paths 102`. stdout sha256 `0cad6d5cfb525227be6af09d6cd6b6115818cee4436180a902a8d1847f490f86`.
3. `c2-mismatch.py --rev decc5697… --freeze decc5697…` → **exit 1**, `mismatches 9` (all nine atoms red; receipts `receipts/c2-freeze.json`, stdout sha256 `7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4`).
4. `c1-counter.py --rev decc5697… --freeze decc5697…` (22:50:45Z) → **exit 1**, `carriers_matched 0`, every binding false. stdout sha256 `976af57f9395202fe82a70d5d0e632d4cc3776d74034c2711b3e3e2eeacfa17c`, which equals the recorded `CTL-C1-0` `stdout_sha256` in `.ufo/waves/round-49/controls/summary.json` (reproduced exactly).

## Disclosed limits, re-tested (confirmed as the plan states; not new)

| limit | command and result |
|---|---|
| Operator-chosen `--freeze` | `c1-counter.py --rev 29883d4e… --freeze 76d7ad6f…` → **exit 0, matched 4** (`fixtures/opfreeze-c1.json`); `c2-mismatch.py --rev 29883d4e… --freeze 76d7ad6f…` → **exit 0, mismatches 0** (`fixtures/opfreeze-c2.json`). `--freeze REV` → C1 exit 1, matched 0 (`fixtures/freezerev-c1.json`). The recorded FREEZE (`l1/FREEZE`) is the only binding |
| `refs/replace` | fixture `fx16-replace`: a frozen-manifest edit X replaced by a tree-equal commit Y (`git replace`). `c2-mismatch.py` with `GIT_NO_REPLACE_OBJECTS` **unset** → **exit 0, mismatches 0**; with it **set** → exit 2 `frozen_path_changed`. Neither counter sets the variable itself (no match in either source) |
| Counter bytes unbound (C1) | comment-only edit of `c1-counter.py` (sha `624c132a…`, not FREEZE's `ac83715b…`) run against the lane at REV → **exit 0, matched 4** (`receipts/c1.json`). Same edit to `c2-mismatch.py` → **exit 2 `counter_not_frozen`** (`receipts/c2.json`) |

## Not run / not verified

- Did not re-score the controls (the W2C1Controls seat owns them); I checked only `CTL-C1-0`'s stdout hash.
- Did not run `c1-run.sh --data-run` or any counter against the lane evidence root. No commits, pushes or mutating git in the lane or fleet repo; every commit was in a clone under scratch.
- Did not run the REA projection internals beyond what the counter does; the carrier verdict rests on the counter's own rerun.
- No tools installed or upgraded (no pacman use).
- The first background C1 attempt at REV died silently (empty outputs, no exit file). The reported C1 receipt is the foreground rerun (`receipts/c1-rev.json`).

## Suggested dispositions for the L1 (not applied; the counters are frozen)

- F1: parse `git log` with `-z` (or `--no-quote-path` style raw names) so quoted names are compared as bytes, in both counters' walks. Re-measure.
- F2: pass `--no-renames` (or treat `C` as an add) in the C1 walk, so a copy into the frozen directory is an add regardless of user config.
- F3: compute `first_add` with `--full-history` (or `--ancestry-path`) and take the oldest add that is not a descendant of FREEZE; the plan's sentence then decides the case.
- F4: test `--name-status` output for a file line, not any non-empty line, in C2's `touched`.
- Plan wording (non-counter): the freeze rule names `corpus/evidence/round-44/carriers/`, which does not exist; the carriers are `corpus/evidence/round-42/c2/fixtures/` (pinned by `carriers.json` `path`, which C1 does freeze). Report as a plan/counter wording mismatch.
