PARTIAL — No sibling lane holds Go map, Swiss-table or Ghidra-Go knowledge (20 of 20 lanes, at branch tips and in working trees). No sibling claims or references kaidoku's new jj tools (20 of 20). But the jj HEAD fact and the branch-tip tool class it registers are already held in three non-owner sibling lanes. The same jj document is registered three times with three different anchors. Nothing at REV cross-references or routes this.

# SiblingOverlap2 — round-18 wave 2 (falsify): sibling overlap at REV

- **Seat:** `KaidokuR18.SiblingOverlap2`, an author-side connector, leaf.
- **Revisions:** REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
- **Probe time:** 2026-10-20 ≈16:55–17:11Z.
- **Fleet:** `839d8df4b218a6d3926ee473710f8bec82bee665`.
- **Sibling tips read:**
  - tameshi `0ff2734`
  - tsukuroi `dd15c18`
  - tabi `6c97851`
  - kumitate `1770305`
  - revenger `cf02419`
  - kama `54a2926`
  - mado `17661e0`
  - souji `5fa6017`
- **Read-only.** No lane or sibling file was edited, and no jj command ran. No REA or Ghidra ran, and no carrier was executed (`sha256sum` read one carrier's bytes). Kaidoku `refs/heads/main` was REV throughout. The only write outside this report was a removed `/tmp` sandbox (§3.4). No installs.
- **Axes:** calibration, operability, depth.
- **Labels:** `[O]` means observed in the command output quoted here. `[I]` means inference.

## 0. What REV registers (the scope under attack)

All anchors are `git show REV:<path>`.

**Go / Swiss / Ghidra-Go**
- `SKILL.md:548-565`: the section "Swiss-map misread replay — round 18" and the `r18-prediction-freeze` row.
- `SKILL.md:590`: the `swiss-misread` row.
- `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`.
- `corpus/SOURCES.md:39-41`: S033–S035, plus the study path at `:49`.
- `PROVINCE.md` is unchanged from the baseline (`git diff --stat 9011581 b2aad08 -- PROVINCE.md` prints nothing).

**jj branch-tip**
- `SKILL.md:567-582`: the section "Revision pins under jj". Its prose is at `:569-573` and its Signal/Decision/Limit table at `:575-579`.
- Registry rows `SKILL.md:586-589`: routed-defects, head-rev-lint, revpin and jj-red-before.
- `corpus/SOURCES.md:42`: S036.
- `corpus/SOURCES.md:50`: the study path "Revision pins under jj — S036".
- `corpus/lessons/round-18.md:26,38`.

## 1. Commands and exits

Set once:

```
P_GO='SwissMapType|OldMapType|noswissmap|swiss.?map|swiss.?table|GoMapType|GoRttiMapper|GolangSymbolAnalyzer|GoApiSnapshot|internal/abi|pclntab|moduledata|GoReSym|goretk|pull/9348|GP-6528|map_swiss|maptype|UncommonType|SlotSize'
```

`br` is each lane's attached branch, or else its `main`/`master`.

| # | Command (cwd `/home/vgpnk/Projects/shokunin`) | Exit | Result |
|---|---|---|---|
| G1 | `for d in *-shokunin` (excluding kaidoku): `git -C $d grep -I -i -l -E "$P_GO" refs/heads/$br -- . ':!*three.core.js' ':!*three.module.js' ':!*omp-live-18.12.2-strings.txt'` | **1** ×20 | `[O]` No match in any sibling's tracked bytes |
| G1b | G1 without the 3 excludes | 0 game-dev-3d, 0 kotoba, 1 ×18 | `[O]` False positives only: three.js `normalMapType` in 68 vendored copies, and omp binary strings (`golangci`, `proxy.golang.org`, `…sourcemaptype…`) |
| G2 | G1 with `git grep --untracked --no-exclude-standard` over working trees (also excluding `.jj`, `node_modules`) | **1** ×20 | `[O]` Nothing uncommitted, untracked or ignored either |
| G3 | `git -C kaidoku-shokunin grep -I -i -l -E "$P_GO" b2aad08 -- corpus SKILL.md PROVINCE.md` | 0 | `[O]` 20 kaidoku files. Positive control: the pattern is not vacuous |
| G4 | `test -x ~/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless`; `command -v ghidra`; `grep -n GHIDRA_INSTALL_DIR ~/.bashrc ~/.profile` | 0; 1; 0 | `[O]` Ghidra 12.1.4 is installed but not on PATH. It is exported at `.bashrc:28` and `.profile:3` |
| J1 | Per lane: `git -C $d grep -q -I -i -E "git-compatibility\|working-copy (commit.s )?parent\|jj-era reading\|detached at the working-copy\|Under jj, git .?HEAD" refs/heads/$br -- SKILL.md PROVINCE.md AGENTS.md corpus tools` | **0** tabi (1 file), tameshi (7), tsukuroi (2); 1 ×17 | `[O]` Three sibling lanes hold the jj HEAD fact |
| J2 | `git -C tameshi-shokunin show refs/heads/master:corpus/SOURCES.md \| sed -n 70p`; `git -C tabi-shokunin show refs/heads/master:corpus/SOURCES.md \| sed -n 63p`; `git -C kaidoku-shokunin show b2aad08:corpus/SOURCES.md \| sed -n 42p` | 0 ×3 | `[O]` Three rows for one document (§3.1) |
| J3 | `git -C <lane> reflog show --date=iso refs/heads/<br>` for tameshi, tsukuroi, tabi and kaidoku | 0 | `[O]` Landing times (§3.1) |
| J4 | `git -C kaidoku-shokunin grep -n -E 'S061\|pin-disposition\|tameshi\|tsukuroi\|detect_branch\|lane-addendum\|jj-lane\.sh\|kumitate\|JjConnectorProvinces' b2aad08 -- SKILL.md corpus/SOURCES.md corpus/lessons/round-18.md .ufo/waves/round-18/tools .ufo/waves/round-18/contract.md` | **1** | `[O]` The REV registration cites no sibling row, fleet helper or routing map |
| J5 | Per lane: `git -C $d grep --untracked -q -I -E 'revpin\|head-rev-lint\|jj-red-before\|swiss-misread\|routed-defects\.py' -- .` | **1** ×20 | `[O]` No sibling names or claims kaidoku's tools |
| J6 | `git grep -n -I -E 'revpin\|head-rev-lint\|jj-red-before\|pin-disposition\|revision-binding\|swiss-misread' HEAD -- MANIFEST.json SCORECARD.md CORPUS.md PROTOCOL.md PROTOCOL-APPENDIX.md AXES.md ROADMAP.md scripts` | 1 | `[O]` No fleet-level registry claims any of these tools |
| J7 | `grep -n '^detect_branch()' scripts/hyaku/jj-lane.sh`; `git show 67a3123:scripts/hyaku/jj-lane.sh \| grep -n '^detect_branch()'` | 0; 0 | `[O]` Line 115 now (v2 `14df5b9`, 13:05 -0300), line 53 in v1 |
| J8 | `grep -a -o -E '0\.45\.1-7c41cdeb[0-9a-f]*' ~/.local/bin/jj` (reads the binary as data; jj is not run) | 0 | `[O]` `0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` |
| J9 | Sandbox, §3.4: `env -i … git init -b main` under `mktemp -d /tmp/so2-revpin-*` (no remote). `main=c1`, `origin/main=c2` (main is behind), HEAD detached at c1. Then `python3 -I -B <REV revpin.py> --root $T/r`, then `rm -rf` | **0**; cleanup 0 | `[O]` `"pushed": true`, `"head_equals_source": true`, `remote` ≠ `source` |
| J10 | `git grep -n -I -i -E '(kaidoku.{0,40}revenger\|revenger.{0,40}kaidoku).{0,80}(rul(ed\|ing)\|arbitrat\|resolved\|owner)' HEAD -- PROTOCOL.md PROTOCOL-APPENDIX.md CORPUS.md MISSION.md ROADMAP.md .ufo/waves/hyaku` | 1 | `[O]` No ruling on the RE boundary exists at the fleet level |

## 2. Go map / Swiss / Ghidra-Go: HOLDS

**No sibling holds this ground.** `[O]` G1/G2 come back empty for all 20 siblings, and G3 proves the pattern finds kaidoku's own 20 files. The only sibling Ghidra mentions are about availability or point at kaidoku:
- `kumitate…/corpus/knowledge/kimi-config-plane.md:258`: the MCP env `GHIDRA_INSTALL_DIR`.
- `tameshi…/.ufo/waves/round-16/w1/Overlap2.md:178-179`: "kaidoku is running Ghidra analyze sessions".
- `kama…/.ufo/waves/round-17/build/advice/ConnectKaidoku.md:36-37`: the native-ELF row is kaidoku's.

**Contradiction inside the contested boundary (stated, not smoothed).** `[O]` Revenger's readiness record says the Ghidra route is blocked:
- `revenger…/corpus/knowledge/2026-10-12-rea-readiness-checklist.md:16`: "ghidra / ida | `which ghidra ida` | ABSENT | native pseudocode route blocked".
- `:39`: K04 "holds", re-verified 2026-10-19.
- `seed.md:63`: F08 "holds".

G4 shows the opposite. Ghidra 12.1.4 is installed and exported (`.bashrc:28`), and REV's C3 ran 15 Ghidra sessions. `[I]` Revenger's probe tests PATH, not REA's `GHIDRA_INSTALL_DIR`. So its stated consequence is false on this host. The fleet's only exercised Ghidra-Go route is kaidoku's, and the lane that formally co-claims native RE records that route as blocked. The owner of the correction is revenger; kaidoku must not edit it.

**Parent boundary: still unresolved.** Both lanes declare native RE:
- `[O]` kaidoku `PROVINCE.md:3-4`.
- `[O]` revenger `PROVINCE.md:3-5`: "native binaries … using the REA skill".

The siblings route it as follows:
- `tsukuroi…/PROVINCE.md:79`: "Kaidoku and revenger both declare shipped-artifact RE. The integrator must …"
- `tsukuroi…/PROVINCE.md:51`: ADJ-06 "kaidoku/revenger ownership unresolved".
- `tabi…/PROVINCE.md:15` and `corpus/adjacency.tsv:3-4`: tabi refuses forensics to "revenger/kaidoku".

J10 finds no ruling. `[I]` C3 survives either ruling because it is a statement about Ghidra's reader, not ownership of the artifacts. This is the wave-1 carve-out, re-verified at today's tips.

**Carrier identity is corroborated by another lane.** `[O]`
- `tabi…/corpus/evidence/tabi-r2-2-state/tabi-r2-2-baseline.txt:23` (committed `bc4b7d5`, 2026-10-14) pins `/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge` at sha256 `71067480bd99c2ba…f8ad35d`.
- That equals REV `predictions/carriers.tsv:15` and today's `sha256sum` of the file.
- `tabi…/corpus/adjacency.tsv:10`, citing `kumitate…/SCORECARD.md:1556`, routes webbridge *internals* to tabi.

`[I]` No contest: REV's entry makes no claim about webbridge internals, only Ghidra's markup outcome on those bytes. The cross-lane pin shows the bytes were unchanged from 2026-10-14 to today.

## 3. jj branch-tip: contested scope (why PARTIAL)

### 3.1 One document, three non-owner rows, three anchors

| Lane | Row (at tip) | Anchor | Status / recheck | Landed on branch (J3) |
|---|---|---|---|---|
| tameshi | `corpus/SOURCES.md:70` S061 | `https://docs.jj-vcs.dev/latest/git-compatibility/` "@ v0.46.0 (alias latest)" | mined / 180d | `2a22ade` 12:54:21 -0300, **before REV** |
| kaidoku | REV `corpus/SOURCES.md:42` S036 | v0.45.1 raw tag file, sha256 `0fb71f99…c641`, lines 114-116 and 208 | mined / on-release | `b2aad08` 13:38:08 -0300 |
| tabi | `corpus/SOURCES.md:63` S049 | v0.45.1 rendered, tag `7c41cdeb…`, raw lines 113-115 | queued / on-release | `6c97851` 14:06:25 -0300, after REV |

- `[O]` All three teach the same rule: pin the branch ref, not HEAD.
- `[O]` The installed jj is `0.45.1-7c41cdeb…` (J8). Tameshi's S061 therefore anchors a version the host does not run.
- `[O]` REV `corpus/lessons/round-18.md:26` rejects exactly that anchor: "jj `latest` docs as the S036 anchor | reject | Unversioned (0.46 content)". This judgment falsifies a sibling's admitted row. It is not routed, and REV cites neither S061 nor S049 (J4 exit 1).
- `[O]` Routing at fleet `839d8df`, `.ufo/waves/hyaku/jj-w1/reports/JjConnectorProvinces.md`:
  - `:181` R1: the jj facts and the helper contract belong to **kumitate**.
  - `:183` R3: tameshi "Does not own jj facts".
  - `:189` R9: kaidoku and tabi have "No route … Do not seed jj entries in product domains".
- `[O]` Kumitate holds no jj entry: `git -C kumitate-shokunin ls-tree --name-only refs/heads/master corpus/knowledge/ | grep -i -E 'jj|vcs'` exits 1.
- `[I]` REV adds a jj study path (`SOURCES.md:50`) and a SKILL jj section whose only external source is S036 (`SKILL.md:569-573`). That goes beyond the "citation support for a lane tool" scoping that wave 1 recommended (`w1/ConnSiblingOverlap.md:76`). The table rows themselves (`:577-579`) describe lane-tool behaviour, so the R9 conflict is modest. The real defect is the unacknowledged third copy.

### 3.2 Same tool class: four lane-local vocabularies plus the helper

| Owner | Artifact (at tip) | Branch resolution | Finding names | "pushed" |
|---|---|---|---|---|
| kaidoku (REV) | `tools/revpin.py` (`SKILL.md:588`) | explicit `--branch main` (`revpin.py:12,93`) | `head_not_branch_tip`, `branch_not_pushed` | tip ⊆ origin (`:32-35,116`) |
| tameshi | `tools/pin-disposition.py` (`SKILL.md:1853`) | the `detect_branch` ladder (`pin-disposition.py:42-51`) | `head_differs_from_branch` (reported, not refused) | — |
| tsukuroi | revision contract plus `revision-binding` probe (`SKILL.md:1902,1904-1914`; `corpus/QUALITY.md:37`, criterion 27) | `--branch`, default master | `E-REVISION-INVALID`, `-NOT-LANDED`, `-NOT-PUSHED` | REV ⊆ origin |
| tabi | `scripts/check-adjacency.mjs:188-189` (ladder master→main; lane is master-only) | ladder | `lane_tip_unresolved` (`:103`) | — |
| fleet helper (operator) | `scripts/hyaku/jj-lane.sh:155-180` `cmd_state` | `lane.branch` → `detect_branch` → the single master/main (`:162-166`) | `ahead=`/`behind=`/`head=` | counts |

- `[O]` `tameshi…/.ufo/waves/round-17/w1/C01SiblingOverlap.md:118-120`: "Branch-tip semantics belong to the fleet helper, not to a lane tool … not define a second convention."
- `[O]` The law itself is at `scripts/hyaku/lane-addendum.md@839d8df:149-156`: "record measured/pinned revisions as the branch tip, never bare `HEAD`", and a git-writing gate "must run on a sandbox clone".
- `[I]` For kaidoku (`origin/HEAD` → `origin/main`) all five resolve the same tip today, so there is no behavioural conflict at REV. The contest is over who defines the convention, and it now has four lane answers.
- `[O]` Tsukuroi and tabi landed after REV (J3), so REV could not have cited them.
- `[O]` Tameshi landed 44 minutes before REV. Wave-1's "No sibling lane has yet migrated…" (`w1/ConnFleetJjPractice.md:9`) was true when it was measured and false at REV. REV does not repeat that claim: `git grep -i 'first lane|no sibling'` finds no relevant line.

### 3.3 Factual outlier: `revpin.py:6`

- `[O]` REV `revpin.py:6`: "leaves git HEAD detached on the working-copy commit".
- Every other source says the working-copy *parent* (`@-`):
  - `JjAuditKaidoku.md:37` (fleet): "detached at `@-`".
  - Tameshi S061: "detached at the working-copy commit's parent".
  - `tsukuroi…/SKILL.md:1913` and `QUALITY.md:37`: "the working-copy parent".
  - Kaidoku's own `w1/ScoutJjColocation.md:10,122`: "HEAD == @-".
- Kaidoku's registered tool is the outlier. This is a calibration defect in a docstring only; the behaviour is unaffected.

### 3.4 "pushed" semantics are contested across lanes

- `[O]` J9 reproduces this. With the tip behind `origin/main`, REV revpin exits 0 with `pushed: true`.
- `[O]` REV `SKILL.md:579` says "Tip differs from `refs/remotes/origin/main` | Refuse 'landed' records". The peer report `w2/RevpinReview.md:1,56-61` found the same in-lane contradiction; I do not re-claim it.
- What I add is the cross-lane picture `[O]`:
  - **Containment:** revpin (`:32-35`) and tsukuroi criterion 27 (`QUALITY.md:37`).
  - **Equality:** the routing source `JjAuditKaidoku.md:260` (§7.1, "`refs/heads/main == refs/remotes/origin/main`") and round-17 `verify.py:94` (per RevpinReview).

### 3.5 Line-anchored citations into the helper rot within minutes

- `[O]` J7: `detect_branch` moved from `:53` to `:115` at `14df5b9` (13:05 -0300).
- Tameshi's `pin-disposition.py:43` and `SKILL.md:1029` still cite `jj-lane.sh:53-65`. Tameshi landed at 12:54, and the citation was stale 11 minutes later.
- Wave-1's recommended revpin citation, `lane-addendum.md:140` + `jj-lane.sh:71-77` (`w1/ConnSiblingOverlap.md:68,137`), now points at push-recovery text and `lane_realdir` (`sed -n 140p` / `71,77p` at `839d8df`).
- `[O]` REV carries no such citation (J4 exit 1), so REV did not drift. `[I]` Any future citation must pin a fleet commit.

### 3.6 Contested-scope summary

| Item | REV | Sibling holder | Owner per routing | State |
|---|---|---|---|---|
| Go 1.24/1.25 Swiss map-type misread by Ghidra 12.1.4 | entry, `SKILL.md:548-565` | none | kaidoku (analyzer behaviour) | **uncontested** |
| Native-ELF RE as a domain | `PROVINCE.md:3-4` | revenger `PROVINCE.md:3-5` | protocol integrator (`tsukuroi/PROVINCE.md:79`) | **formally contested, no ruling**; revenger's own record says the route is blocked (§2) |
| jj "HEAD is detached / not the tip" fact and its source row | S036, `SKILL.md:569-573`, `SOURCES.md:50` | tameshi S061 + 5 ER-jj addenda (`fleet-kill-rate-ledger.md:420`, `incremental-pin-disposition.md:386`, `operator-runbook.md:514`, `service-limits.md:279`, `verification-patterns-fleet.md:309`); tabi S049; tsukuroi `SKILL.md:1913` | **kumitate** (R1); R9 forbids kaidoku and tabi from seeding | **duplicated in 4 non-owner lanes; the owner holds none; not routed** |
| Lane-local branch-tip pin tooling | revpin, head-rev-lint, jj-red-before (`SKILL.md:586-589`) | tameshi pin-disposition; tsukuroi revision-binding; tabi lane-tip ladder | each lane for its own tools; the semantics belong to the helper (C01:118) | **kaidoku's tools are uncontested** (J5); the convention is fragmented (4 lane vocabularies + the helper) |
| Sandbox red-before method for VCS state | `jj-red-before.py` (`SKILL.md:589`) | tameshi `head-vs-branch.sh:1-40`; tsukuroi "mktemp clone only" (`SKILL.md:1902`) | **tameshi** (R3: method only) | `[I]` already ≥2 independent lanes (see the move) |

## 4. Proposed move (one, bounded): cite and route; do not re-own

**Evidence.**
- §3.1: the same jj row is held in three non-owner lanes, and REV rejects the sibling's anchor without routing it.
- §3.3 and §3.4: two REV statements contradict facts or semantics that siblings have already admitted.
- `JjConnectorProvinces.md:167-170`: tameshi's two-lane bar for R3 "is not yet met". `[I]` Kaidoku's real-jj sandbox receipt (`evidence/jj-red-before.json`, 14/14) plus tameshi's git-emulated `head-vs-branch.sh` (`QUALITY.md:160-163` for its scrub) are now two independent lanes.

**Move (kaidoku side only; no tool behaviour change).**
1. **Append a crosswalk.** In the round-19 lesson's Registry changes, or as a SOURCES search-log line, record that S036 is the same document as tameshi S061 (`latest`@0.46.0, tameshi `2a22ade`) and tabi S049 (v0.45.1, queued, tabi `6c97851`). Record that the installed jj is `0.45.1-7c41cdeb…`, so S036's raw-tag digest `0fb71f99…` is the installed-version anchor. State that S036 is citation support for lane tools only, and that kumitate owns the jj fact (R1/R9).
   - Do not edit the S036 cell in place. `kama…/ConnectKaidoku.md:52-55` already flags kaidoku's in-round row edits as a convention conflict.
2. **Route two lines through the integrator** (PROTOCOL routing; never by editing a sibling):
   - To tameshi: S061 anchors a moving `latest` that is not the installed version. `pin-disposition.py:43` and `SKILL.md:1029` cite helper v1 lines (now `:115`).
   - To kumitate (R1 owner): the candidate anchor (v0.45.1 raw file plus digest) and the red-before artifacts of kaidoku and tameshi. Tameshi then rules on its own two-lane bar.
3. **Make two one-line wording fixes** (owning executor, after the round-18 measured records are pinned):
   - `revpin.py:6`: change "on the working-copy commit" to "at the working-copy commit's parent (`@-`)".
   - `SKILL.md:579`: change "Tip differs from" to "Tip not contained in (`merge-base --is-ancestor`)". `[I]` Containment matches revpin's designed semantics (`:32-35`) and the sibling-admitted criterion (tsukuroi `QUALITY.md:37`). Equality survives only in the audit's recommendation and round-17 `verify.py:94`.
   - Any helper citation added later must be commit-pinned, for example `scripts/hyaku/lane-addendum.md@839d8df:149-156`.

**Affected axes.**
- **Calibration, up:** one unacknowledged duplicate source of record becomes a cross-referenced citation, and two statements that contradict sibling-admitted facts are corrected.
- **Operability, up:** fleet consumers get one anchor and a finding-name crosswalk.
- **Depth, unchanged.**
- **No axis harmed:** no tool logic changes, so C2's measured values (head-rev-lint live 3→0; jj-red-before 14/14) and C3 are untouched.

## 5. Risks

1. **Routing lines could read as kaidoku claiming jj ownership.** Phrase them as evidence pointers that name kumitate as owner.
2. **Timing.** Changing `revpin.py` bytes after the runs makes the tip's tool digest differ from the digests in the round-18 `producer.json`. Runs bind to their producing revision, so land the wording fix in round 19, or after the measured records.
3. **The fleet moved during this probe.** Helper v2 landed at 13:05, lane-addendum changed at 13:49 and 14:04, and tsukuroi and tabi landed after REV. This census is a snapshot at the pinned commits above.
4. **Re-litigating `pushed`.** Choosing containment keeps RevpinReview's L1 (a stale remote-tracking ref gives a silent green) open. That is a separate fix, not this move.
5. **The RE-boundary ruling** stays with the integrator. Nothing here should be read as kaidoku absorbing revenger ground.

## 6. Verification (for the owning executor; this seat ran only §1)

- **After step 1:** `git grep -n -E 'S061|S049' <REV2> -- corpus/lessons/round-19.md corpus/SOURCES.md` exits 0, and `git diff b2aad08 <REV2> -- corpus/SOURCES.md` shows no change to the line-42 cell.
- **After step 3:**
  - `git show <REV2>:.ufo/waves/round-18/tools/revpin.py | sed -n 6p` names `@-`.
  - `git show <REV2>:SKILL.md | grep -n 'not contained in'` resolves.
  - `revpin.py --selftest` stays CLEAN.
  - Re-running J9 gives exit 0, now consistent with the SKILL row.
  - `head-rev-lint.py --root LANE --rev <REV2> --strict` still exits 0.
  - `jj-red-before.py` expectations are unchanged.
- **Regression of this report:**
  - G1/G2 should still print `=1` for all 20 siblings, and G3 should stay 0.
  - J1 should flip from 0 to 1 for a sibling only if that lane drops its row; kumitate should flip to 0 once R1 lands.

## 7. Limits

- The sweeps are lexical. G1/G2 cannot see Go map knowledge written without these tokens. The pattern covers struct names, the analyzer and class names, the PR number, GOEXPERIMENT tokens and the layout field names.
- No sibling tool or selftest was executed. The sibling semantics in §3.2 come from their docstrings, SKILL rows and QUALITY text.
- jj was not run (contract). The version comes from bytes in the binary (J8), matching tabi S049's tag commit.
- Wave-1 anchors cited above were read from REV bytes. The fleet files were read at `839d8df`, and `JjConnectorProvinces.md` was last changed at `7d0c760`.
