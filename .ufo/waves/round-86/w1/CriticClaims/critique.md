# Round 86 — CriticClaims critique of R86-C1 and R86-C2

Seat: CriticClaims (critic, read-only). Lane: kaidoku-shokunin. Round 86, kaidoku.
Measured against: BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`; declaration `b205bb8b66ec7b61e028bccd92f64eade8942461`; claims container `ec9963eb9e5c1eedfada9a69f073c1639e7911f9`; HEAD at read time `0864a7bdbf185583773d1a3f3416de76e9cab137`. No production edit, no commit, no lane git mutation by this seat.

## Method (exercised, not summarised)

- Read the frozen plan, `claims.json`, both counters in full (`tools/round-86/record-agreement.py` 450 lines, `tools/round-86/gate-registry.py` 393 lines), `tools/round-85/predicate-bind.py` (its reads), and the BASE bytes of `corpus/SOURCES.md`, `SCORECARD.md`, `SKILL.md`, `tools/round-84/mutation-closure.py`, and the S255 snapshot. All lane reads were `git show <rev>:<path>`.
- Re-ran both counters and both controls at BASE. Results match the frozen pre-receipts exactly (`receipts/base-rerun/`): C1 exit 1 `0/3`, C1 substring control exit 0 `mismatches []`, C2 exit 1 `0/5`, C2 file-exists control exit 0 `mismatches []`.
- Counter selftests: `record-agreement --selftest` 11 cases, 0 failures; `gate-registry --selftest` 8 cases, 0 failures.
- Built 30 throwaway git fixtures in scratch (each commit asserted `rev-parse --show-toplevel` = fixture dir), each a BASE-derived tree with one named edit, run through the counters with `--root <fixture> --rev <fixture sha>`. Receipts: `receipts/fixtures/`, summary `receipts/fixtures/fixture-summary.json`, generator `receipts/fixtures/recipe-fx.py` (rebuilds every fixture from lane BASE blobs).
- Instrument integrity: sha256 of `record-agreement.py` (99cb8f27…), `gate-registry.py` (b87ffb1b…), `predicate-bind.py` (a99f8f18…), `mutation-closure.py` (e5cfd2ed…) at HEAD equal the `claims.json` pins. `git diff --stat ec9963eb..HEAD -- tools/round-86 tools/round-85 tools/round-84 plans .ufo/waves/round-86/claims.json .ufo/waves/round-86/pre` shows only three added files, `pre/*-at-declaration.json`; no counter, plan or claim edited after declaration.
- Tools installed: none. Packages: none.

## Per-claim verdict table — R86-C1 (calibration, record agreement)

| # | clause | command | observation | verdict |
|---|---|---|---|---|
| C1.1 | (a) A2 "name the status the code assigns (`survived`); no other status word may appear" | `record-agreement.py --root <fx> --rev <fx>` on mutation-closure with the docstring sentence set to `survived` / `a survivor` / `surviving` / `killed` (fixtures `c1-a2-survived`, `c1-a2-survivor`, `c1-a2-surviving`, `c1-a2-killed`); counter line 147 exempts every word whose first 5 letters equal the stem `survi` | `survived` green; **`survivor` and `surviving` also green** (A2 absent from mismatches); `killed` red | **falsified** |
| C1.2 | (a) A1 "the newest row" | `c1-a1-wrong-first` (wrong superseder S305 count 3 earlier in file, correct S306 count 7 later) → A1 green; `c1-a1-correct-first` → A1 red. Counter line 106 `sup[-1]` | "newest" is implemented as last in file order, not by id, date or `opened` | **under-specified** (clause: "newest" undefined) |
| C1.3 | (a) A1 selector "after the word `count`" (plan) vs "as its first integer" (counter docstring line 11) | counter line 110 `count\s+(\d{1,3})`; docstring says first integer | counter's own docstring contradicts its code and the plan | **under-specified** |
| C1.4 | (a) A1 opener "`supersedes S303 —`" (plan frontier item 1) | counter line 102 `startswith("supersedes S303")`, no em dash required | the plan's opener is stricter than the counter | **under-specified** (minor) |
| C1.5 | (a) A1 "OTHER rows carrying the same canonical URL" (docstring line 12) vs "carry `rea-agents-6.5.0.tgz`" (plan) | counter line 101 `URL_TOKEN in cells[1]` (substring) | the counter counts token substrings; S079/S080 carry the token inside prose; count unit (rows vs scopes, the S303 text says "five scopes") not frozen | **under-specified** |
| C1.6 | (a) A3 "covered by a `.ufo/waves/round-M/l1/scores/*.json` receipt" | counter lines 155-170: exactly one `| coverage |` row, newest named receipt, M ≥ R | "covered by" is implemented as "named by the row" | **under-specified** |
| C1.7 | (b) one command over committed bytes | `record-agreement.py --root . --rev <rev>`; `read = git_show(root, rev, ...)` (lines 427-428) | no worktree read in rev mode; BASE and declaration receipts identical | **survives** — would be falsified by any worktree read in rev mode |
| C1.8 | (c) universal clauses | ATOMS tuple lines 189-193 enumerates A1-A3; "all three declared atoms" enumerated by name | no unenumerated universal in the atom set | **survives** |
| C1.9 | (c) "the SCORECARD `| coverage |` row" (definite description) | `git show 2cf0b7ff:SCORECARD.md \| grep -c '^| coverage |'` = **23** (line 23 and 22 historical rows, lines 179…3409) | one row cannot satisfy A3 without editing history (see C1.13) | **under-specified** (selector clause missing) |
| C1.10 | (d) axis `calibration` named by the surface | surface = three record cells; the plan's justification is "tied-lowest" (a number) | the surface is records, the choice of word was driven by the proxy | **survives** (noted; the numeric justification is not a surface reason) |
| C1.11 | (e) causal separability | `sep` fixtures: C1 at the C2-only commit = 0/3, identical to base; C2 at the C1-edit commit = 5/5, identical to C2-only; C1 moves to 2/3 on its own edits (A1, A2 green, A3 red) | measurement unmoved in both directions | **survives** — would be falsified if C1 reads any SKILL.md or predicate-bind byte (none found: counter reads only SOURCES, mutation-closure, SCORECARD and `.ufo/waves/round-M/l1/scores/`) |
| C1.12 | (f) do-nothing control cannot reach target | BASE re-run `c1-base-rerun.json`: exit 1, `0/3`, mismatches A1,A2,A3, identical to `pre/c1-at-base.json` | target unreachable at BASE | **survives** |
| C1.13 | (f) cheap-rule control is a false green, as declared | BASE re-run `c1-control-rerun.json`: `mismatches []`, `ok true` (token tests: `"supersedes S" in SOURCES`, `"surviv" in MC`, `".ufo/waves" in CARD`) | the control accepts the defective records; that is the declared intent | **survives** |
| C1.14 | Plan's BASE cause for A3: "row claims round 85 and names only a round-67 receipt" | BASE row names `.ufo/waves/round-{84,76,75,68,67}/l1/scores/…`; max named round 84; counter fails first with `expected exactly one | coverage | row, found 23` | the plan's stated cause is false; A3 is red by row count, and also by "predates" once count is fixed | **falsified** (plan description) |
| C1.15 | Honest A3 target | `c1-a3-history-kept-r85` (round-85 receipt added, 23 rows) → `found 23`; `c1-a3-history-removed-basepaths` (1 row, 84 receipt) → `predates`; no `.ufo/waves/round-85/l1/scores/` receipt at BASE | honest A3 needs history deleted or prefix-renamed AND a new round ≥ 85 receipt | **falsified** (target reachable only by editing 22 historical rows) |
| C1.16 | Sizing: A3 green by a fabricated receipt | `c1-a3-history-removed-r85`: round-85 receipt with `rev` = 40 zeros, row points at it | A3 green; receipt rev not compared to `--rev` or to the row's own record | **falsified** |
| C1.17 | Sizing: A3 green by rewriting the row's claimed round | `c1-a3-round-rewrite-0`: last cell `85` → `0`, BASE receipts | A3 green | **falsified** |
| C1.18 | Sizing: A1 green by rewriting another record | `c1-a1-s079-rewrite`: S079's source URL edited to drop the token, superseder count 6 | A1 green; A1 is self-referential (it re-derives the count from the same registry it checks) | **falsified** |
| C1.19 | Target reachable honestly for A1 | `c1-a1-genuine`: superseder S305 count 7, ids S079/S080/S083/S090/S092/S119/S123 | A1 green | **survives** (A1 reachable) |
| C1.20 | Target reachable honestly for A2 | `c1-a2-survived` | A2 green | **survives** (A2 reachable with the plan's own status token) |
| C1.21 | Selftest green while production red (fixture-only green) | `record-agreement.py:290,299-303,374-382`: the selftest's genuine world is `an absent declared case is a survivor` (A2 noun accepted); `FIXTURE_CARD_OK` has one coverage row (lines 305-308) where production has 23 | selftest green on worlds production cannot reach | **falsified** (the selftest encodes the loophole) |

## Per-claim verdict table — R86-C2 (operability, gate registration)

| # | clause | command | observation | verdict |
|---|---|---|---|---|
| C2.1 | (a) G3 "a `python3` command **on that tool path**" | `gate-registry.py` `command_argv` (lines 116-125) checks only `startswith("python3 ")`; fixtures `c2-foreign-cmd` (`python3 -c "import sys; sys.exit(0)"`) and `c2-gate-registry-cmd` (the OTHER counter's selftest) | G3 green in both; the self-test cell need not name the registered tool | **falsified** |
| C2.2 | (a)/(b) predicate "re-derive … at `--rev`" vs G3 "executed … in `--root`" | `run_selftest` and G3 run with `cwd=root` (lines 106, 166); `root` is the working tree, not the rev. Fixture `c2-worktree-green`: committed `predicate-bind.py` exits **2** at HEAD (checked by `python3 -I -B -c …`), worktree copy exits 0 | G2 and G3 green, receipt stamped `rev` = HEAD; the counter measured the worktree | **falsified** |
| C2.3 | Reverse of C2.2 | `c2-worktree-red`: committed exit-0 tool, worktree exit 2 | G2, G3 red at HEAD | confirms C2.2 |
| C2.4 | (a) G4 "at least one `.ufo/waves/round-<N>/claims.json` that is a blob at `--rev`" | `gate-registry.py` line 176 collects only `claims\.json` pins; a second pin `…/absent.json` is never read; fixture `c2-pin-partial` | 5/5 green; the non-claims pin is unverified | **under-specified** (pinned-value cell may name unverified paths) |
| C2.5 | (a) G1 "exactly one row whose cell 0 is …" | `registry_rows` keeps only rows with `len(cells) >= 7` (line 87); fixture `c2-dup-malformed` (second row for the same tool, 6 cells) | G1 green while the section holds two rows for the tool | **falsified** |
| C2.6 | (a) G2 "verdict-map cell declares all three exits (`0=`, `1=`, `2=`)" | counter line 149 `all(tok in verdict_cell …)` (substring); fixture `c2-map-substring` (`10=clean; 1=flagged; 2=unreadable`) | `10=` satisfies `0=`; G2 green with no real exit-0 declaration | **falsified** |
| C2.7 | G2 kill rule "a declared exit map that the observed exit does not agree with" | only `--selftest` exit 0 is observed (line 151); exits 1 and 2 are never observed | the kill rule is universal over three exits; one is checked | **under-specified** |
| C2.8 | (c) "holds exactly one row" and the kill rule's universal "declared exit map" | see C2.5, C2.7 | enumerated in text, not in the counter | **under-specified** |
| C2.9 | G5 owner cell "`kaidoku-r<N>`" | counter line 190 `kaidoku-r(\d+)$` on `owner.strip()`; fixture `c2-owner-backtick` (`` `kaidoku-r85` ``) → red | whether backticks belong to the cell is not frozen | **under-specified** (minor) |
| C2.10 | (d) axis `operability` | plan: "Lane axes: coverage, depth, calibration"; SCORECARD.md lines 470, 491: "operability (fleet axis, unowned proxy)" | the claimed axis is not one of the lane's scored axes; no lane score can move | **under-specified** (name the lane score that moves, or drop the axis word) |
| C2.11 | (e) causal separability | `predicate-bind.py` has no read of SKILL, SCORECARD, SOURCES or mutation-closure (grep: no hits); `sep` fixtures: C2 identical at C1-edit commit (5/5 both) | unmoved by C1 | **survives** |
| C2.12 | (f) do-nothing control at BASE | BASE re-run `c2-base-rerun.json` exit 1, `0/5`, identical to `pre/c2-at-base.json`; `c2-control-rerun.json` exit 0 `mismatches []` | target unreachable at BASE; the file-exists control accepts BASE | **survives** |
| C2.13 | Target reachable honestly | `c2-genuine`: BASE `predicate-bind.py` (blob), honest row, claims pin as blob → exit 0, `5/5` | the target is reachable with a correct row | **survives** |
| C2.14 | Fixture-only green | `gate-registry.py` selftest builds `FIXTURE_TOOL` (lines 249-255, 295) and never executes the production `predicate-bind.py` | `SELFTEST cases=8 failures=0` says nothing about the production tool | **falsified** (fixture-only green) |
| C2.15 | Freeze | sha256 pins match HEAD; `ec9963eb..HEAD` adds only `pre/*-at-declaration.json` | no post-declaration change to atom rules, targets, kill rules or instruments | **survives** |

## Frontier — S255 / S305 and the round-86 lesson

| # | clause | command | observation | verdict |
|---|---|---|---|---|
| F.1 | Plan item 3: C1's S255 citation is "re-opened this round (access date …)" | `git show 2cf0b7ff:corpus/SOURCES.md \| grep '^| S255 '` | row says `fetched 2026-11-01`; round date is 2026-11-04 → inherited, not opened this round | **falsified** (for the plan's requirement; the row cannot be cited as this round's open) |
| F.2 | S255 teaches: "`git show REV:path` reads an object's bytes … never from a mutable worktree" | `git show 2cf0b7ff:.ufo/waves/round-55/l1/s255/git-show.html` sha256 `0a95cbcd…` matches `digests.txt`; the only git-show sentence is "For plain blobs, it shows the plain contents." (8 words); the one "working tree" sentence (line 5265) is about a tree-diff option | the worktree claim is not located in the snapshot; an entry quoting the 8-word sentence would not support it | **falsified** (teaches overreaches its quote) |
| F.3 | Plan item 3: "located ≤25-word quote in the lesson `## Gate`" | `corpus/lessons/round-86.md` absent at BASE; round-85 `## Gate` (round-85.md line 15) is a table with columns `item | decision | source opened | judgment`, no quote column | the quote format is not defined by the template | **under-specified** |
| F.4 | Plan item 1: superseder id | BASE SOURCES holds S304 only; S305 absent | the id is free | **survives** |
| F.5 | Plan item 2 (mined mistake) | not verified; no round-86 lesson exists | — | not evaluated |
| F.6 | Plan item 1 census | `scripts/sources-census.sh validate` not run (writes only stdout or `--out`; not part of the counters) | — | not evaluated |

## Verdicts

- **R86-C1: falsified** (measurement). Counterexample receipts: `c1-a2-survivor`, `c1-a2-surviving` (A2 green on a non-status word); `c1-a3-history-removed-r85` (A3 green on a fabricated 40-zero rev after 22 history rows are deleted); `c1-a3-round-rewrite-0` (A3 green on a rewritten round cell); `c1-a1-s079-rewrite` (A1 green while the registry it reads has been rewritten). Surviving clauses: (b) one command over rev bytes, (e) separability, (f) do-nothing and cheap-rule controls, A1 and A2 honest reachability. What would still falsify the surviving clauses: any worktree read in rev mode; any SKILL or predicate-bind read by C1; a do-nothing run reaching `0` mismatches; a cheap-rule control that refuses BASE.
- **R86-C2: falsified** (measurement). Counterexample receipts: `c2-worktree-green` (rev-stamped green from a committed tool that exits 2); `c2-foreign-cmd` and `c2-gate-registry-cmd` (G3 green on a command that does not run the registered tool); `c2-dup-malformed` (G1 green with two rows); `c2-map-substring` (G2 green on `10=`). Surviving clauses: (b), (e), (f), honest reachability (`c2-genuine` 5/5), instrument freeze. What would still falsify the surviving clauses: a rev-stamped receipt measured from non-rev bytes; any predicate-bind read by C1 files; a fixture where the honest row is green but the production tool is red.

The honest target for C2 is reachable (`c2-genuine` 5/5), so the falsification is of the counter's receipt, not of the registry state. The honest target for C1 is reachable for A1 and A2, but A3's selector (23 rows) can only be satisfied by editing history, so under the frozen rule C1's target is not honestly reachable.

## Named residuals

1. **C1 A3 selector.** `| coverage |` matches 23 rows; the honest green needs 22 historical rows deleted or prefix-renamed, plus a new `round-85` `l1/scores` receipt. Frozen rule cannot be changed after scoring; the L1 must not patch the selector mid-wave.
2. **C1 A3 receipt rev is shape-only.** Any 40-hex value passes; no check against `--rev`, `--rev` ancestry, or the row's cited record `01f2d5193421d9769097ddcd9483046632f3b70e`.
3. **C1 A3 round cell is unverified.** Rewriting `85` to `0` passes (`c1-a3-round-rewrite-0`).
4. **C1 A2 accepts `survivor` and `surviving`** (`c1-a2-survivor`, `c1-a2-surviving`). The selftest's genuine world uses the noun (`record-agreement.py:290`), so the selftest cannot catch it.
5. **C1 A1 self-referential oracle.** It re-derives the count from the registry it checks; `c1-a1-s079-rewrite` is green on a rewritten S079. The S079 and S080 rows carry the URL inside prose.
6. **C1 A1 "newest" = last in file order**, not id or `opened` (`c1-a1-wrong-first`). The counter's docstring ("first integer") and code ("after count") disagree.
7. **C1 A1 count unit.** S303 says "five scopes"; the counter counts rows carrying the token (7 others). The unit is not frozen.
8. **C1 plan base description wrong for A3.** BASE row names rounds 84/76/75/68/67 (max 84), 23 coverage rows; the stated cause ("names only round-67") is false.
9. **C2 G3 does not check the tool path** (`c2-foreign-cmd`, `c2-gate-registry-cmd`).
10. **C2 G2/G3 execute the working tree, not `--rev`** (`c2-worktree-green`, `c2-worktree-red`). The counter's own reading rule (`record-agreement.py`-style "committed bytes, never a worktree") is violated; the frozen predicate ("at `--rev`") contradicts G3's "in `--root`".
11. **C2 G1 blind to malformed duplicate rows** (`c2-dup-malformed`).
12. **C2 G2 substring exit-map check** (`c2-map-substring`); only exit 0 is observed though three exits are declared.
13. **C2 G4 ignores pins outside `claims.json`** (`c2-pin-partial`); the plan's "at least one" and the counter's `all claims.json` both differ from "pinned-value cell names only verified paths".
14. **C2 G5 backtick strictness** (`c2-owner-backtick`) is undefined by the plan.
15. **C2 axis `operability` is not a lane axis** (plan: coverage, depth, calibration; SCORECARD lines 470, 491 name it a "fleet axis, unowned proxy"). No lane score is named as moving.
16. **C2 gate-registry selftest runs its own `FIXTURE_TOOL`** (lines 249-255, 295), never the production `predicate-bind.py`; its green is not evidence of the production tool.
17. **S255 inherited, not re-opened:** row `fetched 2026-11-01`, round 2026-11-04. Frontier item 3 requires a this-round access date.
18. **S255 teaches overreaches its snapshot.** "never from a mutable worktree" is not in the snapshot; the only git-show sentence is "For plain blobs, it shows the plain contents."
19. **Lesson `## Gate` quote format undefined.** `corpus/lessons/round-86.md` absent; round-85 Gate table has no quote column.
20. **Supersession opener.** Plan says "`supersedes S303 —`" (em dash); counter accepts any `supersedes S303…`.
21. **Lane working tree is not clean.** `git status` shows `M SKILL.md` (one inserted line) in the production lane path during the wave. Not written by this seat; reported for the L1 (executors write candidates under `w1/` only).
22. **Post-declaration additions to `pre/`.** Three `pre/*-at-declaration.json` files were added after the declaration commit and are not referenced by `claims.json`. Additive only; not a changed frozen file.
23. **Not evaluated:** the round-86 lesson, the census validate run, the mined-mistake item. None exists yet in the lane.

## Recommended smallest correction (for a declared next round, not mid-wave)

- C1 A2: match the status token with a word boundary, `\bsurvived\b`, and reject every other status word including `survivor`/`surviving`; drop the stem exemption.
- C1 A3: select the row as the first `| coverage |` row in the current-assessment section; require the named receipt's `rev` to equal `--rev` (or be its ancestor, via `git merge-base --is-ancestor`); require the claimed round to equal the measured round.
- C1 A1: define "newest" by id order, and fix the count unit (rows or distinct scopes) and the opener (`supersedes S303 —`).
- C2 G3: require the argv's tool path to equal the registered tool. G2/G3 must run a copy of the tool materialised from `git show <rev>:<tool>` into `--work`, not the working tree.
- C2 G1: count any row whose cell 0 names the tool, regardless of width. G2: parse the verdict map with a left-anchored pattern (`(?<!\d)0=`), and observe all three exits or narrow the kill rule. G4: check every pinned path.
- C2 axis: name the lane score that moves, or drop "operability".
