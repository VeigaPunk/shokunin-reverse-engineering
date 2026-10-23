# Round-31 w2 — SCORECARD recipe A at the tip

Seat: `KaidokuR31.RecipeAAtTip` (leaf). Lane read-only; writes limited to this report and
scratch under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/RecipeAAtTip/`.

**Target attacked.** The `SCORECARD.md` "**A — source-derived controls.**" python block
(measured-recipe A) as published at the lane tip, run at the tip
`1288285eed81395e6af7c279a173b117b2c2eaa3` and at the lane base
`c369242fee9f559f895e3f7956b1242076c7b1be`: the coverage-map proxy and the
citation-resolved queue-drain (depth) proxy, plus whether either owned-axis proxy fell.

**Verdict: holds.** Both runs exit 0 and reproduce exactly the counts the SCORECARD pins to
the base (116/116, 17/17); at the tip the corpus grew 116 → 118 files and both proxies stayed
saturated (118/118, 17/17). No owned-axis proxy fell. Two proxy limits were demonstrated
below (unchecked non-`corpus/knowledge` citations; a dangling token does not lower
`coverage_score`); neither makes a current score false, and the first is narrower than the
SCORECARD row's wording.

## 1. Recipe extraction and execution

Working directory `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` throughout; the recipe
itself uses only read-only `git show` / `git ls-tree`.

```text
git show 1288285eed81395e6af7c279a173b117b2c2eaa3:SCORECARD.md > $S/SCORECARD.tip.md
awk 'NR>=93 && NR<=123' $S/SCORECARD.tip.md > $S/recipeA.sh   # lines 93-123, the bash block opened at line 92
diff -u $S/SCORECARD.tip.md SCORECARD.md                       # exit 0, empty
```

`diff` exit 0 with no output: the tip commit's `SCORECARD.md` is byte-identical to the
worktree copy, so the block run is the tip's block (not an uncommitted variant). `git status
--porcelain -- corpus/README.md SKILL.md SCORECARD.md` also printed nothing (exit 0) before
and after the runs.

```text
REV=1288285eed81395e6af7c279a173b117b2c2eaa3 TMPDIR=$S/tmp timeout 300 bash $S/recipeA.sh
REV=c369242fee9f559f895e3f7956b1242076c7b1be TMPDIR=$S/tmp timeout 300 bash $S/recipeA.sh
```

## 2. Results — the two JSON outputs

Tip `1288285eed81395e6af7c279a173b117b2c2eaa3` (start 2026-10-23T04:34:02Z, end
2026-10-23T04:34:02Z, **exit 0**, stderr empty):

```json
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 118, "mapped": 118, "missing": [], "revision": "1288285eed81395e6af7c279a173b117b2c2eaa3", "rule_blocks": 17}
```

Base `c369242fee9f559f895e3f7956b1242076c7b1be` (start 2026-10-23T04:34:02Z, end
2026-10-23T04:34:02Z, **exit 0**, stderr empty):

```json
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 116, "mapped": 116, "missing": [], "revision": "c369242fee9f559f895e3f7956b1242076c7b1be", "rule_blocks": 17}
```

The first run (captured 2026-10-23T04:30Z, same exit 0) and a run inside a fresh sandbox clone
checked out at the tip (2026-10-23T04:31:22Z, exit 0) produced byte-identical JSON: sha256
`881226a0455ea03a8ba9c0183ae5fbe2a3df5cb28335b28721245288649f9b65` for all three.

| field | tip `1288285e` | base `c369242f` |
|---|---|---|
| mapped | 118 | 116 |
| knowledge_files | 118 | 116 |
| missing | `[]` | `[]` |
| dangling | `[]` | `[]` |
| rule_blocks | 17 | 17 |
| citation_resolved_rules | 17 | 17 |
| coverage_score | 10.0 | 10.0 |
| depth_score | 10.0 | 10.0 |
| exit code | 0 | 0 |

## 3. Did any owned-axis proxy fall?

**No** [observation]. Recipe A covers exactly the two finite owned-axis proxies:

- coverage: `mapped`/`knowledge_files` 116/116 → 118/118 (coverage_score 10.0 → 10.0);
- depth: `citation_resolved_rules`/`rule_blocks` 17/17 → 17/17 (depth_score 10.0 → 10.0);
- `missing` and `dangling` are empty at both revisions.

The two files that raised the denominator are the round-31 additions
`corpus/knowledge/2026-10-23-r31-sqlite-positive.md` and
`corpus/knowledge/2026-10-23-r31-sqlite-refusals.md` (`git diff --name-status
c369242f 1288285e -- corpus/knowledge` shows both as `A`). Both are named in the tip's
`## Coverage map` table (section rows 73 and 74, README lines 83 and 84, states
"held —" and "held narrowly —"), which is why the tip score stays 10.0 rather than dropping.

Base claim reproduction: the SCORECARD coverage row states "116/116 knowledge files mapped at
`c369242fee9f559f895e3f7956b1242076c7b1be`" and the depth row "17/17 ...
at `c369242f`"; both reproduce to the unit. The tip count 118/118 is recorded in no lane file
(`grep -rn '118/118\|mapped=118\|knowledge_files.*118' .ufo/waves/round-31` found nothing);
the scorecard's round-31 rows are explicitly measured at the base, so this is an unrecorded
tip value, not a contradicted one [observation, with the grep as the evidence].

## 4. Proxies are discriminating — sandbox mutation controls

Sandbox clone of the lane at `/fast/scratch/.../RecipeAAtTip/clone` (contract clone recipe,
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset), checked out at the tip
(`git rev-parse HEAD` = `1288285eed81395e6af7c279a173b117b2c2eaa3`, `git status --porcelain`
empty, exit 0). Each control is one commit on `ctl`, recipe A run as `REV=HEAD`, then
`git reset --hard 1288285e…` back to the tip. Baseline inside the clone (04:31:22Z, exit 0)
was the same 118/118, 17/17.

| # | control (one commit) | output field that moved | verdict |
|---|---|---|---|
| M1 | replaced one map token with `redacted-entry` in `corpus/README.md` | `mapped` 117, `coverage_score` 9.92, `missing` `["2026-10-23-r31-sqlite-refusals"]` (04:31:39Z, exit 0) | detected |
| M2 | changed one rule citation to `…2026-10-13-r7-01-queue-a-ops.md:99999` | `citation_resolved_rules` 16, `depth_score` 9.41 (04:31:39Z, exit 0) | detected |
| M4 | deleted `2026-10-23-r31-sqlite-positive.md`, kept its token | `dangling` `["2026-10-23-r31-sqlite-positive"]`, `knowledge_files` 117, `mapped` 117 — but `coverage_score` stayed **10.0** (04:31:52Z, exit 0) | surfaced, not penalised |
| M5 | appended `` (see also `LOG.md:99999`) `` to a rule that already has valid `corpus/knowledge` citations | **no change**: 118/118, 17/17, 10.0/10.0 (04:32:33Z, exit 0) | **undetected** |
| M6 | flipped a mapped row's state cell from `held — REA 6.5.0 reports…` to `missing — entry not written` | **no change**: 118/118, 10.0 (04:32:33Z, exit 0) | **undetected** |
| M3 | added zero-byte `corpus/knowledge/2026-10-23-r99-empty-probe.md` plus its token row | `knowledge_files` 119, `mapped` 119, `coverage_score` **10.0** (04:31:39Z, exit 0) | proxy saturated by an index token |

Reading of the six controls [observation for the outputs, inference for the consequence]:

- The coverage proxy really checks token presence and file presence (M1, M4); it never reads
  the row's state text (M6), so "118/118 mapped" is an index claim only — consistent with the
  scorecard's own limitation "index integrity only, **not** fraction of the REA domain held".
- `coverage_score` divides by file count and ignores `dangling` (M4), so a map padded with
  tokens for missing files still scores 10.0 as long as the JSON reader looks at `dangling`.
- The depth proxy's pattern is `corpus/knowledge/(…\.md)(?::…)?`, and `valid = bool(refs)`:
  it verifies **at least one** `corpus/knowledge` citation per block and resolves only those.
  Non-`corpus/knowledge` citations are invisible, which M5's `LOG.md:99999` witness proves.
  The SCORECARD depth row's phrase "resolvable file/range citations" therefore describes a
  broader check than the code performs [inference from the recipe source + M5].

## 5. Stricter citation audit (not the recipe)

Because the recipe checks 67 of the citations and ignores the rest, I audited **every**
backticked `.md[:range]` citation inside the 17 craft rule blocks with a one-off script
(scratch artifact `rule-citation-audit*.txt`), resolving each path and range against the
revision with `git show`:

```text
rule 1: refs=10 fails=[]  …  rule 17: refs=8 fails=[]
TOTAL_REFS=80 FAILS=0        (tip, captured 2026-10-23T04:33:14Z)
TOTAL_REFS=80 FAILS=0        (base, captured by 2026-10-23T04:33:23Z)
```

67 refs match the recipe's pattern; 13 do not (`PROVINCE.md:18`, `SCORECARD.md:59`,
`SCORECARD.md:544-545`, `SCORECARD.md` bare, `LOG.md:856-858`, `LOG.md:1411-1412`,
`corpus/QUALITY.md:21`, and six `.ufo/waves/...` claim/verdict files). All 80 resolve at both
revisions, so the row's "17/17 … resolvable file/range citations" is still true today under
the strict reading — the recipe just would not notice if one of the 13 broke (M5).

Also verified: the depth row's `SKILL.md:81-314` craft range is exact at both revisions
(heading `## Queue-drain craft` at line 81, next `##` at 319, last non-blank line 314), and
`rule_blocks` = 17 equals the count of lines matching `^- \*\*` inside that section. The
round-31 SQLite decision table sits at `SKILL.md:1008` ("## SQLite databases
(`inspect-sqlite-database`) — round 31"), outside the craft section, so it adds no rule
blocks.

## 6. Historical anchors named by the scorecard

Same recipe, same lane repo, read-only:

| revision | JSON excerpt | exit | time |
|---|---|---|---|
| `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` | `"citation_resolved_rules": 17 … "knowledge_files": 109, "mapped": 109, "missing": [], "dangling": [], "rule_blocks": 17` | 0 | 04:32:33Z |
| `3395b6dbe1927995c379f04a9064dc9f8495db0c` | `"citation_resolved_rules": 9 … "knowledge_files": 78, "mapped": 78, "missing": [], "dangling": [], "rule_blocks": 9` | 0 | 04:32:33Z |

These match the coverage row's "109/109 at `ebe2cb4a`, round 26" and "78/78 at `3395b6d`", and
the depth row's "also 17/17 at `ebe2cb4a`" and "9/9 at `638fb211`" (the 9-rule geometry is the
same at `3395b6d`).

## 7. Conclusions

- **Observation.** Recipe A runs unmodified at the tip and at the base, exit 0, and reports
  tip `mapped=118 knowledge_files=118 missing=[] dangling=[] rule_blocks=17` with 17 resolved
  rules, base `mapped=116 knowledge_files=116 missing=[] dangling=[] rule_blocks=17` with 17
  resolved rules; both `coverage_score` and `depth_score` are 10.0.
- **Observation.** No owned-axis proxy fell between the base and the tip. The growth from 116
  to 118 knowledge files is fully reflected in the coverage map (rows naming both round-31
  entries), and the depth proxy's numerator and denominator are unchanged.
- **Inference.** The two saturated proxies cannot express the round-31 corpus growth except
  as an unchanged 10.0; they are index checks, and this run is no evidence about whether the
  two new entries are semantically correct or whether the map rows' "held"/"held narrowly"
  states are true. The scorecard already scopes coverage this way; it does not scope the
  depth proxy's non-`corpus/knowledge` citation blind spot.
- **Unknown.** Whether any of the 13 unchecked citations' *content* supports its rule's claim
  was not judged (ranges and files resolve; semantics not assessed). Whether an empty or
  false entry can enter the map unnoticed is answered for the index (yes — M3), not for the
  corpus' admission review.

## 8. Artifacts (scratch, sha256)

All under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/RecipeAAtTip/`:

| file | sha256 | note |
|---|---|---|
| `recipeA.sh` | `e6bb76da991031b98ce51ce6e3653904ae9156db0e6cfd9f066a9d2dd48b3247` | lines 93-123 of the tip SCORECARD (byte-identical `recipeA.py`) |
| `SCORECARD.tip.md` | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` | `git show 1288285e:SCORECARD.md` |
| `out-1288285eed81395e6af7c279a173b117b2c2eaa3.json` | `881226a0455ea03a8ba9c0183ae5fbe2a3df5cb28335b28721245288649f9b65` | tip stdout (also `clone-baseline.json`) |
| `out-c369242fee9f559f895e3f7956b1242076c7b1be.json` | `7c1abf92407609bf34bb1b261e1a6954273b978f92ea68fbf3b8179ced79932d` | base stdout; byte-identical to w1 `ScribeScorecardRows.md`'s recorded `recipe-a.json` |
| `scorecard-worktree-vs-tip.diff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty file (diff exit 0) |
| `M1-missing.json` | `da0b9f1470a40d4391729dd740c5f5f87ff3c2ed5bfc8f4f727f20cc5bf58d9a` | unmap control |
| `M2-depth.json` | `76d9571258b3a610b83eaa860e66a391d680e234640e99a1310b57a1afa8b418` | broken-range control |
| `M3-gameable.json` | `f843a78237bcf59ac6639f358ace9d12140a78406aa37446d42527ab707165b6` | empty-entry control |
| `M4-dangling.json` | `2e5e70cba1f5cc6119ca00bdd3eed778cfe4fd2de4e828e39b3b23269209fa41` | dangling control |
| `M5-noncorpus.json` | `1294dfe2903c8d87eb7cfb87918347c03137936f3c19d91683183aecb72d0002` | undetected bogus `LOG.md:99999` |
| `M6-state.json` | `1294dfe2903c8d87eb7cfb87918347c03137936f3c19d91683183aecb72d0002` | undetected state flip (identical JSON) |
| `hist-3395b6d.json` | `0ffc7a894661de94191d894825ebc0409a92135a7cf644248f80471499d010e5` | 78/78, 9/9 |
| `hist-ebe2cb4a.json` | `291bd5376ce78e283f18b13f4a472711ea9798bca01ef744522669c9494085bf` | 109/109, 17/17 |
| `rule-citation-audit.txt` | `9fb94ff4d4a59eaf1a79cbeb416f102faba185326fe56850e8f412363c4dd285` | 80 refs, 0 fails (tip) |
| `rule-citation-audit-base.txt` | `be1bc40c0695f2c1271c268ea22828121daedfa3c1eec55179937118197ad706` | 80 refs, 0 fails (base) |
| `coverage-map-tip.txt` | `81f3676cc37762c9928d2bf5cf9838183b803ac086eff3b845e6936c55998eeb` | extracted `## Coverage map` section |
| `clone/` | — | sandbox Git clone; HEAD `1288285e…`, `git status --porcelain` empty |

Scope/hygiene: no lane file was modified (only this report was written inside the lane); no
REA invocation; no source fetch; no tool install or update; every command was bounded by
`timeout` (≤ 300 s); no process was left running.
