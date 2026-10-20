# ScoutJjGaps — round 20 w1 advisory (jj-red-before selftest: inventory + missing cases)

Seat: KaidokuR20.ScoutJjGaps-2 (author-side advisory, not an outside review).
Axes: calibration (what the 9 cases actually assert), coverage (which named guards/branches
have no case), depth (which guard removals survive `--selftest`).

Written 2026-10-20T17:52:26-03:00 (`date -Iseconds` at composition). Read-only seat: the only
lane write is this report. Every mutant copy, fixture lane and harness lived under
`/tmp/kr20-scout-*`; nothing was installed; no REA/Go/Ghidra command was run; no `jj` command
targeted the lane (the only `jj` processes are the tool's own sandboxes under `/tmp`).

## 1. Baseline identity

- [O] The reviewed file is byte-identical to B: worktree `sha256sum` = `0b8522b0…3a892`
  = `git show 14f0260ad319ecc26994381b2415d5a999003375:.ufo/waves/round-18/tools/jj-red-before.py | sha256sum`.
  The lane tip is `d1d981d`, but `git diff --stat 14f0260 -- <tool>` is empty (exit 0).
- [O] `python3 -I -B <tool> --selftest` → `SELFTEST: CLEAN cases=9`, exit 0
  (Python 3.14.8, git 2.56.0, jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5).
- [O] No `lsp` device is mounted (`read xd://lsp` → “No such tool”), so no
  definition/reference/hover was available. Literal `grep` was used only to locate;
  every semantic claim below comes from reading the source or from executing the tool,
  its fixtures and one-line mutants.

## 2. Current selftest inventory — 9 cases, zero stable ids

All anchors are `.ufo/waves/round-18/tools/jj-red-before.py` (lane path).

| # | anchor | trigger | assertion | covers |
|---|---|---|---|---|
| 1 | :1070-1077 | `FIXTURE_CD_FIXED` + `FIXTURE_CP_FIXED` + `FIXTURE_REVPIN` | exit 0, `all_held`, empty `not_runnable` | green baseline of the whole matrix |
| 2 | :1079-1084 | `FIXTURE_CD_REGRESSED` (resolves HEAD) | exit 1 and `fixed-citation-drift` not held | cd green/red discrimination |
| 3 | :1086-1091 | `FIXTURE_CP_REGRESSED` (drops `repo-HEAD-is-branch-tip`) | exit 1 and `fixed-custody-capture` not held | cp green/red discrimination |
| 4 | :1093-1104 | fixture lane whose B already carries `FIXTURE_CD_FIXED` | exit 1, `baseline-citation-drift` and `…-finding` not held | red-before premise is not vacuous |
| 5 | :1106-1119 | both fixed tool paths absent | exit 1\|2, `all_held` False, `not_runnable` exactly the 5 names (:1111-1116) | marker-gated `not_runnable`, never `held` |
| 6 | :1121-1152 | parent `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`JJ_OPERATION_ID` + PATH-first git shim | exit 0, `all_held`, shim log has 0 dirty keys | env scrub reaches fixture builder, evaluate children, in-process revpin |
| 7 | :1154, :1178-1179 | pointer entry = absolute path of an outside victim | exit 2 + `pointer_table_path_outside_sandbox` + victim unchanged | absolute escape |
| 8 | :1180-1181 | pointer entry = `../<victim basename>` | same cause + victim unchanged | `..` walk (assertion vacuous, §4d) |
| 9 | :1182-1184 | pointer entry `linked.md` → outside victim | same cause + victim unchanged | symlink escape, but via the *outside* guard (§4a) |

- [O] No case has an id. Each is only `cases += 1` (:1071, :1080, :1087, :1096, :1107, :1125,
  :1178, :1180, :1182) and a failure is keyed by prose (“green case”, “red cd case”,
  “red cp case”, “green-baseline case”, “absent-tools case”, “env scrub case”,
  “<label> case” — :1075, :1083, :1090, :1103, :1118, :1152, :1173). D6f requires
  `jj_`-prefixed ids, so the current output cannot satisfy it by name.
- [O] The module docstring's own inventory is wrong: :69-78 says “one all-green case, a
  regressed … citation-drift probe …, a regressed … capture …, an absent-fixed-tools case …,
  and three red safety cases” then names four safety items (env + abs + `..` + symlink) and
  omits case 4. It describes 7 of the 9 cases.

## 3. Every round-19 mention of the jj selftest gap

- [FLEET] `/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/kaidoku.md`:
  :16 “jj sandbox env/path guard … corrected. The jj source stays tool-local”;
  :72 “jj sandbox9 … cases” in the selftest tally;
  :118 “jj kept tool-local”; :125 residual list ends “jj selftest coverage gaps”;
  :126 general jj ownership remains kumitate's.
- `corpus/lessons/round-19.md`: :184 “jj sandbox selftest coverage limits” in the
  *not claimed fixed* paragraph; :100 is the S036/kumitate adjacency line, not a gap.
- `.ufo/waves/round-19/w2/ToolJjSandbox.md` (the only w2 file that states the gaps):
  :3 two LOW **test-only** gaps; :14-18 LOW-1 — the relative case's `unchanged` assertion is
  vacuous because the pointer resolves under the sandbox mkdtemp that `build_sandbox()`
  creates for `evaluate()` (:301), with mutant detail
  `exit=0 refusal=None unchanged=True`; :20-22 LOW-2 — no `TMPDIR` canary and
  `_shim_observations()` reuses `_dirty_key()`, so a TMPDIR-dropping mutant reports
  `CLEAN cases=9`; :26-29 runtime observations (CLEAN 9; broad `_dirty_key→False` mutant red);
  :46-49 the same mutant exits; :54-56 residual — the shim observes Git children but wraps
  no `jj`, and there is no captured jj-child env record.
- `.ufo/waves/round-19/w2/SkillRegistryOld.md:38` (row cites `cases=9` and
  `jj-red-before.py:70-78,1121-1183`); `AppendPrefixes.md:66` (carried env scrub + path
  guard, `229/21`); `SandboxSecurity.md:3` (tool in the audited set).
- `CriticCounter.md:94` (“production path is env-poisonable”) is about
  `routed-r18.py`'s `Git.run` (`:1-6` scope), **not** this tool; do not count it as a jj gap.
- Sources of the requirement: W20 `contract.md` D6f (“new named cases for the round-19 gaps,
  ids prefixed `jj_`”) and `corpus/lessons/round-19-verifier-spotcheck.md:190` (D6 names only
  “jj selftest gaps”, no detail).

## 4. What the suite does not assert — observed, with exits

### 4a. Only one of three named refusal causes is ever asserted

`commit_off_branch()` can raise three causes: `pointer_table_path_outside_sandbox`
(:368-370), `pointer_table_path_symlink` (:372-374), `marker_path_outside_sandbox`
(:376-378). The suite matches only the first (:1169-1171). Direct fixture runs
(import the tool, `build_fixture_lane` + `evaluate`, everything under mkdtemp):

| fixture | result |
|---|---|
| entry `linked.md` → outside victim | exit 2, `refusal=pointer_table_path_outside_sandbox`, detail `{'file':'linked.md','entry':'fx-link-out'}` → the “link” case duplicates the abs/`..` cause and never reaches the symlink branch |
| entry `linked.md` → `SCORECARD.md` (**inside** the sandbox) | exit 2, `refusal=pointer_table_path_symlink`, detail `{'file':'linked.md'}` → branch is reachable, unasserted |
| `JJ_RED_BEFORE_MARKER.txt` → outside victim | exit 2, `refusal=marker_path_outside_sandbox`, victim unchanged |
| same marker fixture, `marker_check_off` mutant (`if False:` at :376) | **exit 0, refusal None, victim overwritten** with `off-branch working-copy content; never committed to …` |

### 4b. Mutation matrix (one textual replacement per mutant, then `--selftest`)

| mutant | replacement | exit | output |
|---|---|---|---|
| `dirty_key_false` | `_dirty_key` body → `return False` | 1 | `FAILED cases=9 (env scrub case: {'raised': "RuntimeError: fixture lane setup failed: … 'git' … 'add','-A'] …` |
| `tmpdir_dropped` | `… or key == "TMPDIR"` → `… or False` | **0** | `CLEAN cases=9` |
| `marker_check_off` | `if not _inside(sb, MARKER_NAME) or os.path.islink(str(marker)):` → `if False:` | **0** | `CLEAN cases=9` |
| `symlink_check_off` | `if os.path.islink(os.path.join(sb, cited_file)):` → `if False:` | **0** | `CLEAN cases=9` |
| `guard_table_removed` | delete `    _guard_table_paths(sb, table)\n` | 1 | `FAILED cases=9 (rel case: exit=0 refusal=None detail=None unchanged=True)` |

[O] The last row is incidental detection: the guard is removed and only the `rel` case fails,
because its entry does not resolve and the fallback writes `SCORECARD.md` (exit 0); the abs
and link cases still refuse through the write-site `_inside` check. `unchanged=True` in that
failure is exactly the vacuity round-19 LOW-1 reports.
[O] `dirty_key_false` fails via the *fixture builder* raising inside the env case (the
sentinels are set before `build_fixture_lane`), not via the shim observation; the shim alone
is not what makes that case red.

### 4c. Evaluator branches with no case (each executed once)

| probe | observed |
|---|---|
| regressed revpin fixture (markers present, `resolve_source` does not raise) | exit 1, `not_held ['revpin-resolve-source']` |
| fixture lane B without the citation-drift blob | exit 1, `not_runnable ['extract-baseline:.ufo/gates/citation-drift/citation-drift-probe.py','baseline-citation-drift','baseline-citation-drift-finding','baseline-citation-drift-control']` (branches :641, :714) |
| `jj=/nonexistent/jj` | exit 2, `setup_error RuntimeError: jj git init --colocate failed: FileNotFoundError…` |
| `jj` shim failing only on `commit` | exit 2, `setup_error RuntimeError: jj commit -m off failed: shim commit failure` (:399-400) |
| one non-selectable entry (`kind:"prose"`) at `/etc/hostname` | exit 2, `refusal_detail.entry == "fx-unreach"` → `_guard_table_paths` does cover “entries the selection loop would never reach” (:171-177), unasserted |
| table `[prose, exact]` | exit 0, `setup.mutation.entry_id == "fx-second"` → the kind filter (:281-288) works, unasserted |

### 4d. Relative-case vacuity reproduced

Injected entry `../victim-rel.md` yields `refusal_detail == {'file':'../victim-rel.md',
'sandbox':'/tmp/jj-red-before-…/sb','entry':'fx-escape-rel'}` and the selftest-created victim
is unchanged. That victim is never the resolved target (the sandbox is `<mkdtemp>/sb` from
`build_sandbox` :301-312), so
only the exit/cause carries information — but the cause+detail would carry it precisely.

### 4e. Hygiene and a non-gap

[O] After all runs `ls -d /tmp/jj-red-before-selftest-*` → 0 entries; `evaluate` removes its
sandbox at :814-815 and `build_sandbox` removes on failure at :305. No residue leak observed.
[O] Out of scope but same class: `git status --porcelain` at read time still lists
`.ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/{repo-fixture,repo-sub-fixture}/`
(the round-19 D1 residue) — that is custody-pair's, not this tool's; jj's own suite leaves
nothing under `/tmp`.
[O] A `./SCORECARD.md` entry gives exit 1 with `baseline-citation-drift-finding` not held:
the fixture probes hardcode `SCORECARD.md:1`, so the needle `./SCORECARD.md:1` never matches.
That is a fixture limitation, not a `pick_cited_line` defect — don't propose a `./`-green case
without changing the probes. The real table (60 entries) has no `./` or absolute `file`
values (kinds `anchor|exact|extracted`).

## 5. Proposed missing cases (ranked)

Minimum for D6f: **P1 + P2 + P3**. P4/P5 are the cheapest depth additions because each turns
a currently-undetectable guard removal red.

- **P1 `jj_case_ids` (structural, D6f prerequisite).** Give every case an id (`jj_green_all`,
  `jj_red_cd_regressed`, `jj_red_cp_regressed`, `jj_green_baseline`, `jj_absent_tools`,
  `jj_env_scrub`, `jj_abs_traversal`, `jj_rel_traversal`, `jj_link_outside`, plus the new
  ones) and prefix failure strings with it; keep `SELFTEST: CLEAN cases=N`.
  *Why:* D6f is id-based; today no case has one, and an inserted case is invisible except in
  the count. Keep an expected-id list so delete/insert is detectable.
- **P2 `jj_rel_traversal` (round-19 LOW-1, `ToolJjSandbox.md:14-18`).** Assert exit 2 AND
  `refusal == "pointer_table_path_outside_sandbox"` AND
  `refusal_detail["entry"] == "fx-escape-rel"` and
  `refusal_detail["file"] == "../" + basename(victim)`; annotate that `unchanged` is not the
  resolved target. *Why:* the detail is present today (4d); with the guard removed the case
  fails only on exit/`unchanged=True`, i.e. detection is incidental (4b).
- **P3 `jj_tmpdir_scrub` (round-19 LOW-2, `ToolJjSandbox.md:20-22`).** Add
  `"TMPDIR": <tmp>/sentinel-tmpdir` to the sentinels (:1128-1131) and classify logged lines
  with a literal rule (`key.startswith(("GIT_","JJ_")) or key == "TMPDIR"`) in
  `_shim_observations` (:1026-1039, called :1139) — not `_dirty_key`, or the observation goes
  blind with the predicate. *Why:* `tmpdir_dropped` → `CLEAN cases=9` observed; a scratch
  prototype of exactly this case gives base `CLEAN cases=9` / mutant
  `FAILED cases=9 (jj_env_scrub: {'calls': 43, 'dirty': ['TMPDIR=…']})`.
- **P4 `jj_marker_symlink_refused`.** Fixture lane with `JJ_RED_BEFORE_MARKER.txt` symlinked
  to an outside victim → exit 2, `refusal == "marker_path_outside_sandbox"`,
  `refusal_detail["file"] == MARKER_NAME`, victim bytes unchanged.
  *Why:* branch :376-378 has no case; `marker_check_off` → `CLEAN cases=9` while the same
  fixture escapes and overwrites the victim (4a).
- **P5 `jj_symlink_cited_refused`.** Cited `linked.md` → `SCORECARD.md` *inside* the sandbox →
  exit 2, `refusal == "pointer_table_path_symlink"`, detail file `linked.md`.
  *Why:* the existing link case hits the outside guard first (4a); branch :372-374 unasserted;
  `symlink_check_off` → `CLEAN cases=9`. Also pins the deliberate “inside symlinks are
  refused too” behavior so a future relaxation is visible.
- **P6 `jj_guard_unreachable_entry`.** Table with one non-selectable entry whose `file` is
  outside → exit 2 with `refusal_detail["entry"]` naming it. *Why:* the docstring claim at
  :171-177 (“including entries the selection loop would never reach”) is unasserted; guard
  removal is currently caught only by P2's case.
- **P7 `jj_revpin_regressed`.** Revpin fixture with markers but no raise → exit 1 and
  `revpin-resolve-source` not held. *Why:* only cd/cp have red fixtures; the red path was
  observed but nothing drives it.
- **P8 `jj_jj_unusable_refusals`.** (a) `jj=/nonexistent/jj`; (b) shim failing on `commit`.
  Assert exit 2 and the `setup_error` prefixes from 4c. *Why:* :352-353 and :399-400 are
  untested; pins “exit 2, never silent `not_runnable`/exit 0”.
- **P9 `jj_child_env_scrubbed`.** PATH-first `jj` shim (mirror `_install_git_shim` :1010-1024)
  logging env; assert ≥1 jj call, no `GIT_*`/`JJ_*`/`TMPDIR` key, and `HOME`/`XDG_CONFIG_HOME`
  under the sandbox tmp. *Why:* round-19 residual (`ToolJjSandbox.md:54-56`); `jjenv` at
  :313 and :396 is now asserted only by reading source. Needs `go()` (:1061) to accept a jj
  override.
- **P10 (optional) `jj_baseline_extract_failed`.** Fixture B without the CD blob → exit 1,
  the four `not_runnable` names, `all_held` False. *Why:* :641/:714 untested; observed.
- **P11 (optional) `jj_table_skip_unusable_entry`.** `[prose, exact]` → exit 0 and
  `setup.mutation.entry_id == "fx-second"`. *Why:* kind filter :281-288 otherwise sees only
  one usable entry; observed.
- **P12 (optional) `jj_no_residue`.** No `jj-red-before-*` dir under `tempfile.gettempdir()`
  after the suite. *Why:* documented “removed unconditionally” (:20, :305, :814-815, :1188),
  unasserted (though no leak was observed).

## 6. Integration notes for the L1

- `SKILL.md:589` is self-contradictory today: it still carries the round-18 limits (“run only
  as … with no `GIT_*` in the environment (the selftest fixture builder does not scrub it),
  and a pointer-table entry naming a path outside the sandbox would be written”) *and* the
  round-19 correction (“every git/jj subprocess runs with an explicit environment scrubbed …
  pointer-table paths outside the mkdtemp clone are refused with exit 2 (selftest 9 cases)”).
  `W19/w1/SkillRowsFromRouted.md:26` ordered a replacement; the text was appended instead.
  Rewrite it in the same integration, and cite ids rather than `cases=9`.
- `SkillRegistryOld.md:38` and both round-19 report mentions pin “9”; a new case changes the
  count. Either update those rows or make the observable the id set.
- Regenerate the docstring :69-78 from the id list (it omits case 4 and miscounts today).
- `go()` closes over one `jj`; P8/P9 need `go(..., jj_=None)`.
- `.ufo/waves/round-20/tools/` does not exist at B (`ls` exit 2), so no counter reads D6f yet.
  Recommended observable: one `SELFTEST_CASE: <id> <held|failed>` line per case plus
  `cases=N` equal to the id count, so D6f can be counted by name rather than by prose.

## 7. Commands and exit codes

```text
python3 -I -B .ufo/waves/round-18/tools/jj-red-before.py --selftest
# exit 0; SELFTEST: CLEAN cases=9

sha256sum .ufo/waves/round-18/tools/jj-red-before.py
# exit 0; 0b8522b00897694148fcc23b0643163709cbffc3a232ea1d23a8dac7e3eeaed7
git -C LANE show 14f0260ad319ecc26994381b2415d5a999003375:.ufo/waves/round-18/tools/jj-red-before.py | sha256sum
# exit 0; 0b8522b0…3a892  (equal)
git -C LANE diff --stat 14f0260 -- .ufo/waves/round-18/tools/jj-red-before.py
# exit 0; no output
git -C LANE rev-parse --short refs/heads/main
# exit 0; d1d981d
ls .ufo/waves/round-20/tools/
# exit 2; no such directory
```

Mutants (each: copy the blob to `/tmp/kr20-scout-*`, apply the replacement in §4b with Python
string replacement, then):

```text
python3 -I -B /tmp/kr20-scout-*/<mutant>.py --selftest
# dirty_key_false      exit 1  FAILED cases=9 (env scrub case: {'raised': RuntimeError: fixture lane setup failed …})
# tmpdir_dropped       exit 0  CLEAN cases=9
# marker_check_off     exit 0  CLEAN cases=9
# symlink_check_off    exit 0  CLEAN cases=9
# guard_table_removed  exit 1  FAILED cases=9 (rel case: exit=0 refusal=None detail=None unchanged=True)
```

Fixture probes (one `python3` harness importing the tool, `build_fixture_lane` + `evaluate`,
all roots under mkdtemp):

```text
link outside victim        exit 2 refusal pointer_table_path_outside_sandbox entry fx-link-out
link → SCORECARD.md inside exit 2 refusal pointer_table_path_symlink file linked.md
marker → outside victim    exit 2 refusal marker_path_outside_sandbox ; victim unchanged
marker fixture + mutant    exit 0 refusal None ; victim rewritten to "off-branch working-copy content…"
rel ../victim-rel.md       exit 2 refusal_outside entry fx-escape-rel file ../victim-rel.md
revpin regressed           exit 1 not_held ['revpin-resolve-source']
baseline blob removed      exit 1 not_runnable [4 names incl. extract-baseline:…]
jj absent                  exit 2 setup_error RuntimeError: jj git init --colocate failed…
jj commit fails            exit 2 setup_error RuntimeError: jj commit -m off failed…
unreachable prose entry    exit 2 refusal_outside entry fx-unreach
table [prose, exact]       exit 0 mutation.entry_id fx-second
```

```text
ls -d /tmp/jj-red-before-selftest-* | wc -l
# exit 0; 0
read xd://lsp
# "No such tool: xd://lsp" (no language server available)
```

## 8. Inference, limits, remaining unknowns

- [I] P1+P2+P3 is the smallest closure that is not token-only: ids, a non-vacuous relative
  assertion, and a TMPDIR canary classified independently of the predicate under test.
- [I] The marker and symlink branches are defense-in-depth against a manipulated clone/table,
  not a demonstrated production path; their value is that guard removals become observable
  (two mutants are CLEAN today).
- [I] The `./`-entry result is a fixture-probe artifact, not a tool defect; don't build a case
  on it without changing the probes.
- Unknown: whether the L1's D6f counter will read ids from stdout or inspect source; no tool
  exists at B. Unknown: whether the L1 wants `cases=N` pinned or id-count-only.
- Not re-run: round-19 w2's full mutant set; my `dirty_key_false` failure attribution differs
  from its summary (fixture-builder raise vs shim observation) and is reported as observed.
