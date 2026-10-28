# W2Jj — VCS hygiene attack, round 49 wave 2 (post-landing)

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, landing `29883d4ec35a31a8393c4ffb220888c44c0bb022` (main), base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`, FREEZE `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`. All commands ran with `GIT_NO_REPLACE_OBJECTS=1`, read-only (no mutating git/jj, no commit, no stage). Counters C1/C2 were not re-run by this seat (outside the assigned attack).

## Verdict

**VCS hygiene: PASS on every asserted check** (identity, scope, deletions, remote tip, freeze integrity, ordering of freeze → controls → data run). Two record findings need the L1's attention and are not VCS violations: (F1) the round's own calibration record and disclosed-limit figure bind a **superseded** counter/plan (pre-amendment sha), not the frozen bytes; (F2) the S138/S139 `opened` binding cannot distinguish a round-49 re-open from the round-44 row. Minor: anonymous session cookies committed in two wave-1 receipts (F3).

## Checks and results

| # | check | command (abbrev.) | exit | result |
|---|---|---|---|---|
| 1 | lane state | `jj-lane.sh state <LANE>` | 0 | `branch=main local=29883d4e remote=29883d4e ahead=0 behind=0 head=detached tracked=0 untracked=11` |
| 2 | commit list | `git log --format='%H %an <%ae> \| %cn <%ce> \| %s' e4f2cfa..29883d4` | 0 | 8 commits, all `kaidoku-shokunin <kaidoku@shokunin.local>` as author and committer (receipts/commits.txt sha256 `debbaf62…21a287`) |
| 3 | identity, scripted | `git log --format='%an\|%ae\|%cn\|%ce' B..R \| grep -c` (matching) | 0 | 8 match, 0 mismatch; identity-list sha256 `d7bf11f8…1c83e13` |
| 4 | per-commit name-status | `git diff-tree -r --no-renames --name-status` per commit (receipts/scope.txt sha256 `8666d0d0…0bd8c2a6`, 2243 lines incl. headers) | 0 | 2225 A, 10 M, 0 D, 0 R. Top-level prefixes: `.ufo/waves/round-49/`, `corpus/`, `plans/round-49-claims.md` + `tools/round-49/` (freeze commit only), `PROVINCE.md`, `SCORECARD.md`, `LOG.md`. |
| 5 | out-of-scope paths | `git diff-tree -r --name-only B R \| grep -v -E '^(\.ufo/waves/round-49/\|plans/round-49-claims\.md$\|tools/round-49/\|corpus/\|PROVINCE\.md$\|SCORECARD\.md$\|LOG\.md$)' \| wc -l` | 0 | `0` |
| 6 | `tools/` outside round-49 | `grep -E '^tools/' \| grep -vc '^tools/round-49/'` | 0 | `0` |
| 7 | deletions | `git diff-tree --diff-filter=D --name-only B R \| wc -l` | 0 | `0` |
| 8 | merges / replace refs / grafts / shallow | `rev-list --merges B..R`; `for-each-ref refs/replace`; `replace -l`; `.git/info/grafts`, `.git/shallow` | 0 | 0 merges; 0 replace refs; no grafts, no shallow file |
| 9 | ancestry | `merge-base --is-ancestor` B→R, F→R, B→F | 0, 0, 0 | base ⊂ freeze ⊂ landing; base on `origin/main` |
| 10 | remote tip | `git ls-remote origin refs/heads/main`; `rev-list --left-right --count R...origin/main` | 0 | `29883d4e…` = local `main`; `0 0` ahead/behind |
| 11 | frozen paths FREEZE→REV | `git diff --name-status F R -- tools/round-49 plans/round-49-claims.md tools/round-42/{fixtures.json,c1-counter.py,prior-pins.json,rea-pkg.json} tools/round-39/gen-squashfs.py tools/round-27/xpin-attribute.mjs corpus/evidence/round-44/{oracle,carriers}` | 0 | empty (count 0) |
| 12 | commits touching frozen set after FREEZE | `git log -m --diff-merges=first-parent --no-renames F..R -- tools/round-49 plans/round-49-claims.md` | 0 | 0 commits |
| 13 | per-blob freeze equality | `rev-parse F:p` vs `R:p` for all 34 paths under `tools/round-49` + `plans` | 0 | no DIFF. Blobs: `tools/round-49/c1-counter.py` `471e13cf…`, `tools/round-49/c2-mismatch.py` `0fd85696…`, `plans/round-49-claims.md` (blob at F = R) |
| 14 | whole FREEZE→REV change set | `git diff --name-status F R` | 0 | 102 paths: 96 A, 6 M; 54 under `corpus/evidence/round-49/`, 40 under `.ufo/waves/round-49/`, plus landed text |
| 15 | freeze commit content | `git diff-tree --name-status decc5697` | 0 | 34 files, all `plans/round-49-claims.md` or `tools/round-49/**` |
| 16 | FREEZE record | `git show R:.ufo/waves/round-49/l1/FREEZE` | 0 | `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`; file added in `76d7ad6f`, the commit before the data run; `LOG.md` line 3453 names the same hash |
| 17 | ordering | `git log --reverse --format='%h %cd %s'` | 0 | 14936cb 19:11:40 (w1 evidence) → decc5697 19:11:52 (FREEZE) → 76d7ad6 19:12:51 (controls + FREEZE file + LOG) → 4aabb0b 19:13:11 (data run, only `corpus/evidence/round-49/c1/**`) → landing 3847f39 … 29883d4. Committer dates are self-asserted; the order is consistent with the required sequence. |
| 18 | controls bound to freeze | `git show R:.ufo/waves/round-49/controls/c{0..4}/counter.json` | 0 | each has `freeze: decc5697…`, `carriers_matched: 0` |
| 19 | data-run commit scope | `diff-tree 4aabb0b` non-`c1/` lines | 0 | none |
| 20 | tracked worktree | `git status --porcelain --untracked-files=no` | 0 | 0 lines. 11 untracked L1/peer items (see F5) |
| 21 | reflog / unreachable | `reflog show main`; `fsck --no-reflogs --unreachable`; scan for round-49 paths | 0 | main reflog = `export from jj` (jj-colocated lane). 4 unreachable commits; none touches a round-49 path |
| 22 | secrets scan of range blobs | `git grep -I -l -E 'ghp_…\|github_pat_…\|AKIA…\|PRIVATE KEY…\|xox[baprs]-…\|sk-ant-…'` | 1 | no match. Only `set-cookie` headers, see F3 |
| 23 | signatures | `git log --format='%G?' B..R` | 0 | 8×`N` (unsigned) |

Receipts copied to `.ufo/waves/round-49/w2/W2Jj/receipts/` (SHA256SUMS there): `scope.txt`, `f2r.txt`, `commits.txt`, `blobs-path.txt`, `SOURCES.base.md`, `SOURCES.rev.md`, `s145-base.txt`, `s145-rev.txt`.

## Findings

**F1 — calibration record binds superseded bytes (material; recorded, not patched).** The wave-1 harness and controls that produced the plan's disclosed-limit figure ("`--selftest` kills 40 of 75 single-point counter mutants", `w1/C1CounterMut.md`) and the wave-1 controls record the *pre-amendment* bytes: `w1/C1CounterMut/draft-sha256.txt` lists `tools/round-49/c1-counter.py` sha256 `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`, `tools/round-49/c2-mismatch.py` `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f`, `plans/round-49-claims.md` `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492` (also `w1/C1ControlsReview/draft-input-sha256.txt`). The frozen bytes are `c1-counter.py` sha256 `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f`, `c2-mismatch.py` `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d`, `plans/round-49-claims.md` `49214bab0f215ef0c9860a09955944b1b894c12d6d886d8354e31d50b2f61112`. The draft committed in `14936cb` equals FREEZE byte-for-byte (diff of 3415 lines: 0). Grep of the committed tree for the frozen counter sha256 returns only `controls/` (13 files), `l1/` (2) and the landed entry (1); **no committed mutation or selftest receipt names the frozen counter**. Consequence: the 40/75 figure and the six added selftest cases are not measured on the frozen counter in any committed artifact. Command: `git grep -l ac83715b… 29883d4 -- .` and `git grep -l d6d70cb7… 29883d4 -- .ufo/waves/round-49/w1`.

**F2 — S138/S139 `opened` binding cannot see a round-49 re-open (binding weakness).** `corpus/SOURCES.md` S138 and S139 at base `e4f2cfa5` already carry `opened 2026-10-28` and `used-by corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`. The landing changed only field 11 (`used-by`), appending `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`; status, opened and recheck cells are byte-identical to base (field diff, `SOURCES.base.md` sha256 `68e6d028…`, `SOURCES.rev.md` `65f3599f…`). The plan's sentence "re-opened this round (access date and located quote in `corpus/lessons/round-49.md` `## Gate`)" is therefore not recorded in the row; the counter's `opened 2026-10-28` predicate is satisfied by the round-44 value. Not checked by this seat: whether the lesson's `## Gate` actually records a round-49 access. Routed to the L1 as a counter limit.

**F3 — anonymous session cookies committed in receipts (minor hygiene).** `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr` lines 15–17 and `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr` lines 15–17 carry `set-cookie: _gh_sess=…`, `set-cookie: _octo=…`, `set-cookie: logged_in=no; …` (values not reproduced here). These are server-issued anonymous session cookies, not user credentials; removal from history would need a rewrite the plan forbids. Recorded for the L1's judgement. Detected by `git grep -I -l -i -E '^(authorization|x-api-key|cookie|set-cookie):' 29883d4 -- .ufo/waves/round-49 corpus`.

**F4 — repository weight (observation).** Blob bytes added or modified in `B..R`: 23,723,932 B total. Largest: `.ufo/waves/round-49/w1/C2CounterMut/results-raw.json` 1,720,798 B (blob `478201885a15fe97873648194aa7895fcdb4755c`); `.ufo/waves/round-49/w1/C1RunReview/logs/strace-f-dev-run.txt.gz` 697,043 B (`ec27715cf1b174176d2380bd9ed3a952757f3238`). Not a contract violation.

**F5 — landing-revision measurements are not committed (observation).** `git status --porcelain` lists `.ufo/waves/round-49/l1/scores/c1-at-3847f393.json`, `c1-at-landing.json`, `c2-at-3847f393.json`, `c2-at-landing.json` as untracked. Only `l1/scores/c1-at-data-4aabb0b4.json` is committed (in `3847f39`). A landing-revision score cited from the L1 has no committed receipt. Also untracked: `.ufo/waves/round-49/{gen-w2.py,r49-w1-results.json,w2-dispatch.json,w2-spec.json,w2.ready,w2.ready.dispatched}` and peer `w2/*` directories (not mine).

**F6 — lane HEAD is detached (observation).** `git symbolic-ref -q HEAD` exits 1; `jj-lane.sh state` reports `head=detached` while `refs/heads/main` = `29883d4e`, and the reflog reads `export from jj`. Consistent with a jj-colocated lane; not a violation. Recorded so that a later `git commit` from this HEAD is not mistaken for `main`.

**F7 — commits unsigned (observation).** `git log --format='%G?' e4f2cfa..29883d4` = 8×`N`. Not a stated requirement.

## Not run by this seat
- The C1 and C2 counting commands (plan P49-C1, P49-C2) — not in this seat's attack.
- Any `c1-run.sh --data-run` (forbidden here).
- Any `jj` command (a read may snapshot the working copy; avoided).
- Mutation or selftest of the frozen counter — not run; F1 is a record-level finding only.

## Sha256 receipts
| file | sha256 |
|---|---|
| `receipts/scope.txt` | `8666d0d014b03c2e6fc9e0295e7ecded4e4d0bc85c8fd5f24f2952c10bc2796a` |
| `receipts/f2r.txt` (FREEZE→REV name-status) | `d0e052c711dc4393e39f48e454cc48b6dd5a2566d08cad65a4a5ee69af0180d4` |
| `receipts/commits.txt` | `debbaf620b42b6112ad8ffd02dc5dd6fa41cc2c7c06b949acab037606b21a287` |
| `receipts/blobs-path.txt` | `014140dba277b4411946b354744ee6168a4b69cc0d40839ac062c0da1298570b` |
| `receipts/SOURCES.base.md` | `68e6d028744096a4d9e5b2e777ad7ed3e1c56dcc83778f839cb775119627e712` |
| `receipts/SOURCES.rev.md` | `65f3599f0ef0379c47d7efe3babe0f5ee9e15ebcd6245be0b81c082ba34efb01` |
| `receipts/s145-base.txt` = `s145-rev.txt` | `7b6ce653b9395cb111b11a925993b740d1d435f8adad7cbb0ed667bb1023cb80` |
| identity list (8 lines) | `d7bf11f862793c51af89fbfdd561c286552336dd1972f4fcd24e37f1a1c83e13` |
| frozen `plans/round-49-claims.md` (= draft in `14936cb`) | `49214bab0f215ef0c9860a09955944b1b894c12d6d886d8354e31d50b2f61112` |
| frozen `tools/round-49/c1-counter.py` | `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` (git blob `471e13cf…`) |
| frozen `tools/round-49/c2-mismatch.py` | `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` (git blob `0fd85696…`) |
| w1-attacked `c1-counter.py` (superseded) | `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779` |
| w1-attacked `c2-mismatch.py` (superseded) | `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f` |
| w1-attacked plan (superseded) | `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492` |

Scratch `/fast/scratch/hyaku/kaidoku-r49/W2Jj` removed after the receipts were copied. No file was written in the lane tree outside `.ufo/waves/round-49/w2/W2Jj{.md,/}`.
