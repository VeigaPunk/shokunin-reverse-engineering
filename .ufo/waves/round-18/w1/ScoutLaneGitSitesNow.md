# ScoutLaneGitSitesNow — git-argv re-sweep at 9011581d

- Seat: `KaidokuR18.ScoutLaneGitSitesNow` (author-side advisory scout; leaf, no dispatch).
- Assignment: re-run the jj audit's sweep at baseline **`9011581d84527ba34c675f9cf912e54d2e72d470`** (audit used `da64646`) and diff against `.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` §3; answer whether new HEAD-keyed/upstream sites appeared. Deliverable: expected-count oracle for `W18/tools/head-rev-lint.py` (`.ufo/waves/round-18/contract.md:61-70`).
- Read-only. No tool, gate or selftest was executed. Only this report was written. No installs. One process error, disclosed in §9: `jj --version` was run once with cwd = the lane; it printed only the version (that `--version` exits before repo discovery is [INF] from jj's CLI, not straced).
- Toolchain observed: `git version 2.56.0`; `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`.
- Labels: **OBS** = command output observed now; **INF** = inference, not observed.

## 0. Baseline state (OBS)

`git rev-parse HEAD` → `9011581d84527ba34c675f9cf912e54d2e72d470` (exit 0).

```
$ ls -d .jj                         # exit 0 -> .jj
$ git symbolic-ref -q HEAD          # exit 1 (detached)
$ git rev-parse HEAD main origin/main
9011581d84527ba34c675f9cf912e54d2e72d470   (exit 0)
9011581d84527ba34c675f9cf912e54d2e72d470   (exit 0)
9011581d84527ba34c675f9cf912e54d2e72d470   (exit 0)
$ git merge-base --is-ancestor HEAD main     # exit 0
$ git branch --show-current                  # empty, exit 0
$ ls .git/hooks | grep -vc sample            # 0
$ find . -name .gitattributes -not -path './.git/*' | wc -l   # 0
$ git config --local --get core.hooksPath    # exit 1 (unset)
```

So the lane is now jj-colocated and **HEAD is detached**, but at this instant `HEAD == main == origin/main` and HEAD is an ancestor of `main`: the audit's prospective mechanisms (F1/F2) are live, with no observed divergence yet. Audit F5/F6 (no active hooks, no attributes) still hold.

The worktree acquired an unrelated modification during the sweep (` M .ufo/waves/round-17/tools/compare.py`, +45 lines, another seat's edit). **Every anchor below was re-read from the commit blobs** with `git show 9011581d:<path> | sed -n '<line>p'`; the affected files (compare.py) contain no git invocations and do not appear in any table.

## 1. Method and command log (OBS)

Scope: tracked `*.py`/`*.sh` under `.ufo/gates`, `.ufo/rounds`, `.ufo/waves/round-14` … `round-17` at `9011581d`. (`.ufo/waves/round-18/` has **0 tracked files** at the baseline: `git ls-tree -r --name-only 9011581d -- .ufo/waves/round-18 | wc -l` → `0`, exit 0, so it contributes nothing to a `--rev 9011581d` scan.)

```
$ git ls-tree -r --name-only 9011581d -- <6 dirs> | wc -l                          # 830, exit 0
$ git ls-tree -r --name-only 9011581d -- <6 dirs> | grep -E '\.(py|sh)$' | wc -l    # 37,  exit 0
$ git ls-tree -r --name-only da64646   -- <6 dirs> | grep -E '\.(py|sh)$' | wc -l   # 26,  exit 0
$ comm -13 /tmp/r18-tools-da.txt /tmp/r18-tools.txt                                # 11 lines, exit 0
$ git grep -n -E '"git"|'"'"'git'"'"'' 9011581d -- $(cat /tmp/r18-tools.txt)        # 36 lines, exit 0
$ git grep -n -E '(^|[;&|( ])git[ ]' 9011581d -- \
    .ufo/waves/round-17/run-carriers.sh .ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh
    # 3 lines in rebuild.sh; run-carriers.sh has none; exit 0
$ git grep -n -E 'symbolic-ref|@\{u\}|abbrev-ref|show-current|refs/heads|refs/remotes|--set-upstream|origin/' \
    9011581d -- $(cat /tmp/r18-tools.txt)                                          # no output, exit 1
$ git grep -n -E '"HEAD"|rev-parse HEAD|rev-parse", "HEAD"|\bHEAD\b' \
    9011581d -- $(cat /tmp/r18-tools.txt)                                          # 30 lines, exit 0
$ git grep -n -E 'default\s*=\s*"HEAD"|HEAD:' 9011581d -- $(cat /tmp/r18-tools.txt)
    citation-drift-probe.py:477  ap.add_argument("--rev", default="HEAD")
    custody-pair.py:349          "# repo-HEAD: %s" % repo_head(Path.cwd())      # label, not a revision path
$ awk '/^### 3\.1/{s=1;next}/^### 3\.2/{s=2;next}/^## 4/{s=0} ...' \
    .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md   # 3.1 data rows=32; 3.2 data rows=22, exit 0
```

The audit's §3.2 has **22 rows but 30 call sites**: rows aggregate repeated calls (invocation-audit's three `config` calls in one row; temporal-sweep's three `add`/`commit`/`rev-parse` calls in one row each). §4's per-file counts are call-site counts; all arithmetic below uses **one git argv call site** as the unit — each distinct argv expression once, and repeated execution of the same site (a fixture helper called per case) still counts once. That unit reproduces the audit's 62 exactly.

AST cross-check (stdlib `ast`, blobs read via `git show`, nothing written): 35 `.py` files parsed. A first pass reported 17 `rev-parse`+`HEAD` call nodes; six are the same site seen twice because a chained `.stdout.strip()` Call also contains the inner argv's constants. **Deduplicated: 11 Python rev-parse sites**; adding the 2 shell sites and the 1 argparse default yields the 14 lint sites in §3.

## 2. Oracle A — call-site census at 9011581d (audit unit)

Classes follow the audit legend: **A** attached-branch/upstream assumption · **B** history/index/worktree mutation · **C** index/staging read · **D** read-only revision-scoped. `live` = runs against the lane; `fix` = mkdtemp/`/tmp` fixture repo built by the file itself.

| file | live D | live B | live C | fix B | fix D | total | audit §4 | Δ |
|---|---|---|---|---|---|---|---|---|
| `.ufo/gates/citation-drift/citation-drift-probe.py` | 3 | 0 | 0 | 3 | 0 | 6 | 6 | 0 |
| `.ufo/gates/custody-pair/custody-pair.py` | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| `.ufo/waves/round-14/measure.py` | 3 | 0 | 0 | 0 | 0 | 3 | 3 | 0 |
| `.ufo/waves/round-15/measure.py` | 3 | 0 | 0 | 0 | 0 | 3 | 3 | 0 |
| `.ufo/waves/round-16/measure.py` | 3 | 0 | 0 | 0 | 0 | 3 | 3 | 0 |
| `.ufo/waves/round-16/controls.py` | 3 | 0 | 0 | 0 | 0 | 3 | 3 | 0 |
| `.ufo/waves/round-17/measure.py` | 3 | 0 | 0 | 3 | 1 | 7 | 7 | 0 |
| `.ufo/waves/round-17/controls.py` | 3 | 0 | 0 | 3 | 1 | 7 | 7 | 0 |
| `.ufo/waves/round-17/verify.py` | 2 | 0 | 1 | 0 | 0 | 3 | 3 | 0 |
| `.ufo/waves/round-17/tools/invocation-audit.py` | 3 | 0 | 0 | 6 | 1 | 10 | 10 | 0 |
| `.ufo/waves/round-17/tools/temporal-sweep.py` | 4 | 0 | 0 | 9 | 6 | 19 | 16 | **+3** |
| `.ufo/waves/round-17/w2/audit-attack.py` | 0 | 0 | 0 | 5 | 2 | 7 | — | **+7** (new) |
| `.ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh` | 0 | 0 | 0 | 7 | 2 | 9 | — | **+9** (new) |
| **total** | **31** | **0** | **1** | **36** | **13** | **81** | **62** | **+19** |

Class totals at 9011581d: **A 0 · B 36 · C 1 · D 44 = 81**; live 32 (D31 + C1), fixture 49 (B36 + D13). The delta is entirely fixture-side: temporal-sweep +3 (Case 3b), new `w2/audit-attack.py` +7 (its four setup argvs run through one `subprocess.run` loop site), new `w2/temporal-attack/fixtures/rebuild.sh` +9.

File census: 37 tool files, **13 invoke git** — the audit's 11 plus `w2/audit-attack.py` and `rebuild.sh`. The other 24 contain no git invocation (substring hits are prose/URLs: `tools/receipt-validate.py:20` "legitimately", `tools/buildinfo-probe.py:16` "raw.githubusercontent.com", `tools/predict.py` "digit").

Verified anchors for the changed files (both via `git show 9011581d:<path>`):

```
temporal-sweep.py:71   ["git", "-C", root, "show", f"{rev}:{path}"]
temporal-sweep.py:76   ["git", "-C", root, "cat-file", "-e", f"{rev}:{path}"]
temporal-sweep.py:97   ["git", "-C", root, "rev-parse", "--verify", f"{rev}^{{commit}}"]
temporal-sweep.py:109  ["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--"] + SITE_DIRS
temporal-sweep.py:219  "git",                                  # git_in() wrapper
temporal-sweep.py:241  git_in(repo, "init", "--quiet")
temporal-sweep.py:258/259, 286/287, 305/306, 330/331  add/commit rev1..rev4
temporal-sweep.py:261/289/308/332  rev-parse HEAD (4th is Case 3b)
temporal-sweep.py:343  rev-list --max-parents=0 HEAD;  :349 rev-parse {rev0}^{tree}
audit-attack.py:74-78  loop over init + 3×config through one ["git", ...] call
audit-attack.py:87/89/91, 344/346/348  add/commit/rev-parse HEAD (build_repo; rootfix)
rebuild.sh:5   git init; git config×2
rebuild.sh:9   git add; git commit; git rev-parse HEAD
rebuild.sh:11  git add; git commit; git rev-parse HEAD
```

## 3. Oracle B — the lint's own site census (`head-rev-lint.py` kinds)

Kinds/context are taken verbatim from `contract.md:61-70`: `rev-parse-HEAD`, `default-HEAD`, `HEAD-colon`, `upstream`; `fixture` iff the enclosing Python function name contains `selftest` or `fixture`, else `live`; **shell files are always `live`**. At `--rev 9011581d`: `files_scanned = 37`.

| path:argv-line | kind | context under the stated rule | enclosing fn | true repo |
|---|---|---|---|---|
| `.ufo/gates/custody-pair/custody-pair.py:327` | rev-parse-HEAD | live | `repo_head` | lane, cwd-dependent |
| `.ufo/waves/round-17/verify.py:59` | rev-parse-HEAD | live | `main` (via `git()`) | lane |
| `.ufo/waves/round-17/controls.py:442` | rev-parse-HEAD | **live** | `_commit` | mkdtemp (selftest-only) |
| `.ufo/waves/round-17/w2/audit-attack.py:91` | rev-parse-HEAD | **live** | `build_repo` | mkdtemp |
| `.ufo/waves/round-17/w2/audit-attack.py:348` | rev-parse-HEAD | **live** | `main` | mkdtemp |
| `.ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh:9` | rev-parse-HEAD | **live** (shell) | — | `/tmp` |
| `.ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh:11` | rev-parse-HEAD | **live** (shell) | — | `/tmp` |
| `.ufo/gates/citation-drift/citation-drift-probe.py:477` | default-HEAD | live | `main` | lane |
| `.ufo/waves/round-17/measure.py:223` | rev-parse-HEAD | fixture | `_git_fixture` | mkdtemp |
| `.ufo/waves/round-17/tools/invocation-audit.py:424` | rev-parse-HEAD | fixture | `selftest` | mkdtemp |
| `.ufo/waves/round-17/tools/temporal-sweep.py:261` | rev-parse-HEAD | fixture | `selftest` | mkdtemp |
| `.ufo/waves/round-17/tools/temporal-sweep.py:289` | rev-parse-HEAD | fixture | `selftest` | mkdtemp |
| `.ufo/waves/round-17/tools/temporal-sweep.py:308` | rev-parse-HEAD | fixture | `selftest` | mkdtemp |
| `.ufo/waves/round-17/tools/temporal-sweep.py:332` | rev-parse-HEAD | fixture | `selftest` | mkdtemp |

`HEAD-colon` = **0**. The only `HEAD:` substring is the receipt label `# repo-HEAD:` at `custody-pair.py:349`, which is not a revision path; a bare `HEAD:` text rule false-positives there.
`upstream` = **0** (the restricted class-A sweep exits 1 with no output over all 37 files).

**Counts under three defensible readings:**

| reading | live | fixture | total |
|---|---|---|---|
| **B1** contract-literal (helper calls resolved, function-name context, shell live) | **8** | **6** | 14 |
| **B2** direct `["git", …]` argv only (helpers not resolved) | 6 | 4 | 10 |
| **B3** audit §5 semantics (fixture by actual target repo/purpose) | **3** | 11 | 14 |

The split matters: B1 ≡ 7 `rev-parse-HEAD` live (custody, controls, verify, audit-attack×2, rebuild.sh×2) + 1 `default-HEAD`; B2 drops the helper-mediated sites (`verify.py:59`, `controls.py:442`, `measure.py:223`, `invocation-audit.py:424`), leaving 5 live rev-parse (custody, audit-attack×2, rebuild×2) + 1 default; B3 keeps the same 14 sites but reclassifies five mkdtemp/selftest-only sites (`controls.py:442`, `audit-attack.py:91/348`, `rebuild.sh:9/11`, plus the already-fixture six) as fixture, leaving exactly the audit's three: `verify.py:59`, `custody-pair.py:327`, `citation-drift-probe.py:477`.

`claims.json:20` asserts "live HEAD-as-revision call sites **3** at 9011581". That number is **B3 only**. A tool implementing B1 returns **8**; B2 returns **6**. This is a definition gap, not a repo change (see §6.1).

## 4. Diff against JjAuditKaidoku §3

**§3.1 (live sites, 32 rows):** all 32 rows still exist with the same class. Anchors are unchanged except `temporal-sweep.py` (the file gained 7 lines of live code — `corpus/lessons/` site coverage, the verifier-spotcheck exclusion, dedupe, and the marker exemption — plus a 21-line Case 3b selftest block), shifting its four live calls **+3**: 68→71, 73→76, 94→97, 106→109. No new live call site was added; no live class changed (B remains 0, C remains 1 at `verify.py:60`).

**§3.2 (fixture sites, 22 rows = 30 call sites):**
- Unchanged: citation-drift 3, `round-17/measure.py` 4, `round-17/controls.py` 4 (same anchors 215/220/221/222 and 434/435-441/442/451).
- `invocation-audit.py`: same 7 calls, anchors shifted **+7** (367→374, 368-370→375-377, 415→422, 416→423, 417→424); no class change.
- `temporal-sweep.py`: 12 → **15** call sites. Case 3b (`.ufo/waves/round-17/w2/temporal-attack/…` mutation survivors) adds `git_in add` (:330), `git_in commit rev4` (:331), `rev-parse HEAD` (:332); the earlier three commits' anchors shift +7 and `rev-list`/`tree` shift +28 (315→343, 321→349).
- New files: `w2/audit-attack.py` 7 call sites (one setup loop that runs init + 3×config, then add/commit/rev-parse in `build_repo`, plus add/commit/rev-parse in the conditional rootfix branch), `w2/temporal-attack/fixtures/rebuild.sh` 9 call sites on 3 shell lines.
- `w2/receipt-forge.py` is now tracked but still contains **0** git invocations (audit §3 was right to omit it).

**File-set delta:** 37 vs the audit's 28-file working-tree census = **+9** (11 newly tracked since `da64646`, of which `verify.py` and `w2/receipt-forge.py` were already audited as untracked). `verify.py` is now tracked (added at `95e34db`, touched again at `d0ab299`), closing audit F7's "untracked verifier" gap; `w2/audit-attack.py` and `rebuild.sh` were added in `d0ab299`.

## 5. Answer: new HEAD-keyed or upstream sites since da64646?

- **Live-lane HEAD-keyed producers: 0 new.** The same three remain, at the same anchors and in the same form:
  - `.ufo/waves/round-17/verify.py:59` — `source = git("rev-parse", "HEAD")`, consumed at `:131` (`--rev source`), `:134` (`controls base source`), `:136` (`measure source`), `:139` (`citation-strict --rev source`), recorded at `:170`/`:183`.
  - `.ufo/gates/custody-pair/custody-pair.py:327` — `git rev-parse HEAD` with `cwd`, rendered at `:349` from `Path.cwd()`.
  - `.ufo/gates/citation-drift/citation-drift-probe.py:477` — `--rev` default `"HEAD"`.
  Audit recommendations R1/R2/R3 are **not** implemented at this baseline.
- **New HEAD-keyed sites in any context: 5 direct argv sites** — `temporal-sweep.py:332`, `audit-attack.py:91`, `audit-attack.py:348`, `rebuild.sh:9`, `rebuild.sh:11`. All are fixture repos (mkdtemp or `/tmp`).
- **New upstream/class-A sites: 0.** `@{u}`, `--abbrev-ref`, `--show-current`, `symbolic-ref`, `refs/heads`, `refs/remotes`, `origin/` remain absent from all 37 tool files.
- One pre-existing HEAD reference the audit's table omitted: `citation-drift-probe.py:451` (`rev = … else "HEAD"` in the selftest) — not a git argv, so not a lint kind, but a HEAD-literal scan will see it; it is a fixture-repo HEAD.

## 6. Calibration notes for `head-rev-lint.py`

1. **The 3-vs-8 gap is in the context rule, not the repo.** `_commit` (`controls.py:429`) is a selftest-only helper but its name contains neither `selftest` nor `fixture`; `build_repo` (`audit-attack.py:71`) and `main` (`:348`) build mkdtemp repos; `rebuild.sh` is a shell fixture by construction. Under `contract.md:66-68` all of these are `live`, so `live_count` = 8 at baseline. If the C2 claim needs 3→0, either propagate fixture context through callees/callers (call-graph, not name), allowlist `w2/temporal-attack/fixtures/` and `w2/audit-attack.py`, or restate the oracle as B1 and change claims.json. [OBS for the counts; INF for which fix the L1 should choose.]
2. **Helper resolution is required for 4 sites.** `verify.py:59` (`git()`), `controls.py:442` (`git()`), `measure.py:223` (`run()` inside `_git_fixture`), `invocation-audit.py:424` (`_git()`) carry no literal `"git"` token at the call site. A grep-for-`["git"` implementation silently drops them and reports B2 (6 live / 4 fixture).
3. **Chained calls double-count.** A visitor that matches any Call containing the constants sees the enclosing `.stdout.strip()` call as a second site at the same line (17 raw AST hits → 11 distinct Python sites; +2 shell +1 default = the 14 lint sites). Dedupe on `(path, line, kind)`.
4. **Line choice must be documented.** AST call line vs argv line differs for multi-line calls: custody 326/327, temporal 260/261, 288/289, 307/308, audit-attack 348/349. `git grep`-style anchors (argv line) are the reproducible ones; the contract's `code` field should carry the argv segment.
5. **`HEAD:` label false positive.** `custody-pair.py:349` `# repo-HEAD:` matches a naive `HEAD:` rule. Restrict `HEAD-colon` to revision-path expressions (`"HEAD:"`, `f"HEAD:"`, `"HEAD:%s"`), not receipt labels: 0 sites at baseline.
6. **Conditional sites.** `audit-attack.py:344/346/348` execute only for the single `{ROOT}` case (`:270`). The file has 7 static git call sites (one setup loop + six direct) and 2 `rev-parse-HEAD` sites; runtime invocations per full run are 143 (20 cases × 7 + 3 rootfix). A lint should count static sites and not assert runtime counts.
7. **Pinned stale revision.** `audit-attack.py:42` hardcodes `REV = "da64646…"` and Part A audits the lane at that revision. The lint as specified does not flag pinned revision constants; if C2 is meant to cover drift, add a `rev-constant` kind or record it as a known gap.
8. **Extension filter is load-bearing.** Markdown/JSON in the same dirs quote git argv (e.g. `round-14/w1/ClaimSeparation.md:156-157`, `round-15/w1/VerificationScribe.md:86`, `round-16/w1/SafetyReads.md:32`, and embedded probe source in `round-16/verification.json:343,372`) and a `git grep -c -E 'git'` over the six dirs returns 547 file rows; only the 37 `*.py`/`*.sh` are in scan scope.
9. **Post-fix zero is not reachable by a purely syntactic kind.** The fixed `verify.py` must compare HEAD to the branch tip, and `W18/tools/revpin.py` must run `git rev-parse --verify HEAD^{commit}` (`contract.md:51-59`). Both are `rev-parse` + literal `HEAD` in a `live` function, so a syntactic lint would report ≥1 live site after the C2 fixes. Reaching the claimed 0 needs an allowlist or a `kind` that distinguishes *pinning* HEAD (result used as the source revision) from *checking* it (result compared and discarded). [INF from `contract.md:51-59,83-85` + the kind definition at `:63-67`.]
10. **`files_scanned` changes with the scan revision.** At `9011581d` it is 37 and round-18 contributes 0 tracked files; at the delivered revision it will include the C2 tools themselves, so the oracle count is baseline-only.

## 7. [INF] items

- [INF] The audit's §5 three-site risk list and the lint's §3 kind list are different objects: the first is "HEAD used to pin the lane revision", the second is "any rev-parse+HEAD". At `da64646` the two coincided because the w2 attack harnesses were untracked. At `9011581d` they no longer do; the +4 live sites are new w2 files, plus one pre-existing misclassification (`controls.py:442`).
- [INF] If `head-rev-lint.py` is written to return 8 at baseline while claims.json says 3, the falsifiable-before/after pair will read as a regression at delivery even though the three routed sites were fixed. Aligning the definition (or the claim) before the first run avoids a false red.
- [INF] The current detached-HEAD-but-equal-to-main state means `verify.py:59` records the correct hash today. The hazard is latent: one `jj commit` without a bookmark move makes the same line record `@-`; the audit's sandbox reproduction (F2) remains the evidence for that, not a live observation.

## 8. Residual gaps

- Static only: no lane tool, gate, lint, or selftest was executed; exit-code behaviour of the tools themselves is out of scope.
- The audit's sandbox (`/fast/scratch/jj-wave/JjAuditKaidoku-2/`) was not reused; its F1–F4 observations are cited as the audit's, not re-observed here.
- `.ufo/waves/arc3-loop1-*/claims/**` remains excluded (historical wave outputs), as in the audit.
- The 17-instrument SKILL.md registry was not re-enumerated; the census is file-based over the six assigned dirs.
- One working-tree file changed during the sweep (`compare.py`, unrelated seat); commit blobs were used for every anchor, so no finding depends on the worktree.

## 9. Compliance

- Read-only in the lane: only `git ls-tree/grep/log/show/diff/rev-parse/merge-base/status/branch`, `ls`, `find`, `grep`, `awk`, `comm`, and stdlib Python over `git show` output. Nothing staged, committed, fetched, or written in the lane except this report. No REA/Ghidra/carrier execution.
- **One process error, disclosed:** `jj --version` was run once with cwd = the lane, inside a batch that also called `git --version`. It printed only the version; that it exits at argument parsing before repo discovery is [INF], and I observed no repo state change attributable to it (the later worktree changes are other seats' C2 edits); `.jj` was observed only with `ls -d`. Every other jj mention in this report is read from files or from the audit, not from a jj run. This is the only `jj` execution in the session.
- No tools installed or upgraded.
