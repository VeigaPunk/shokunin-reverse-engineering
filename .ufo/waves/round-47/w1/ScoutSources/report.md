# ScoutSources measurements — round 47

Object: `corpus/SOURCES.md` at `5017e1f7299c3a812e87e7950148f54313dd279e`.

Input of every `fz-*` census command except the live-lane ones: extract of `git show 5017e1f7299c3a812e87e7950148f54313dd279e:corpus/SOURCES.md`. `git hash-object` of that extract = blob `bc817412d6c3952deeb316914db24b5e89794cf6`. File sha256 `13d14bb593d3f0c5cbc2f23ccc0c55a5d30dba7f29ed1e88e81a4438407b970b`. Lane cwd for existence checks: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (`rev-parse --show-toplevel` matched). No install. Scratch removed after these receipts were copied here. Exact argv: `receipts/<id>.cmd`. Stdout: `receipts/<id>.out`. Empty stdout sha256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`CORPUS.md` census block is the seven `grep`/`awk` commands under "### Census". `scripts/sources-census.sh` is the maintained parser note, outside frozen v1.

## Table

| id | measurement | value | exit | stdout sha256 | utc |
|---|---|---|---|---|---|
| fz-identity | freeze blob, extract hash, file sha256 | blob `bc817412d6c3952deeb316914db24b5e89794cf6`; extract sha256 `13d14bb5…970b`; hash-object matches blob. Head recorded in this receipt (`2e4ae434…`) was already past the freeze; see `fz-final-pin` | 0 | `beb4e97bc5de6641f350b5443c326f8b2cee2509ba675a2329c41be95e2de9d1` | 2026-10-28T17:52:41Z |
| fz-rows | row count on freeze extract (`grep -cE` from `CORPUS.md`) | `142` | 0 | `1dadd7223f8953c76459851cca53c62990c1a7b87a5795d31bbfa4059160e9f8` | 2026-10-28T17:50:44Z |
| fz-highest | highest id | `S142 142` | 0 | `958fb0d6f9522559227241aa44526b296ff82810596f4e14f18a8ed1577477f1` | 2026-10-28T17:52:41Z |
| fz-gaps | missing ids in `1..max`; next unused | stdout is only `next 143` (no gap lines) | 0 | `f496c4ddd1a25b528f8d72f26a8b85e68f057e2f01626fef3cfe753cf04c55ed` | 2026-10-28T17:52:41Z |
| fz-tier | tier histogram, `CORPUS.md` awk, column `$5` | `A=134 B=7 C=1 ` (trailing space) | 0 | `bd9958c6ed64dc98b6c3b7b37170f637cdb2395889c2748acd095ef4e08bbd8d` | 2026-10-28T17:50:44Z |
| fz-status | status histogram, `CORPUS.md` awk, column `$9` | `mined=137 rejected=5 ` (trailing space; zero `queued` omitted) | 0 | `7bcfcbebdef8b50437f0e6e70966c6038a183aa3d48687698b205d5c09965d44` | 2026-10-28T17:50:44Z |
| fz-malformed | `NF!=13` count | `0` | 0 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2026-10-28T17:50:44Z |
| fz-dup | duplicate ids | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| fz-enum | tier/status/kind enum and tier-A community | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| fz-missing | mined used-by paths missing from the lane worktree | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| fz-commit-paths | mined used-by vs freeze tree and worktree | `rows=142 mined_refs=234 unique=67 missing_commit=0 missing_worktree=0` | 0 | `7ddd7b728944bd7856ec1e4444450aac1a474eb9daa4301f09f7c68c945cfab9` | 2026-10-28T17:52:41Z |
| fz-round46 | used-by token exactly `corpus/lessons/round-46.md` | `148 S142 A mined corpus/lessons/round-46.md` (one row) | 0 | `1109acab719aecfa85a6a03a1c83d1c878507091d1c881a84fbc84df20e62075` | 2026-10-28T17:52:41Z |
| fz-round46-mentions | every `round-46.md` string in the freeze extract | one line, line 148 only (the S142 row). No other mention | 0 | `fddebc848ddeddf0c223aa7df4c6a18012bf343ad6f71661a0770ccbde4ebfd7` | 2026-10-28T17:55:22Z |
| fz-anchor | lines the next freeze row is appended after | line 148 is the last `| S142 |` row; 149–152 empty; 153 `## Paths`. Append after 148 only | 0 | `f1c31a8ee66f61980d77fdf69c6229ca4b79ba4c79b537be17b1512bdb2bcb44` | 2026-10-28T17:52:41Z |
| script-census-freeze-view | maintained `census` on freeze bytes with lane path base | rows 142; tier A/B/C 134/7/1; mined 137; rejected 5; queued 0; `FLEET.missing=0` | 0 | `a29f7abcc61ddbcf045e9f27d54cceb5cf522a7d3897795a54570a69e32352ed` | 2026-10-28T17:51:49Z |
| script-validate-freeze-view | maintained `validate` on those same bytes | exit 0; 15 `W04`; no `E`; `ok`. `W04` on S142: duplicate url `git-scm.com/docs/git-log` across scopes | 0 | `d8b6f9f508efa1695ac414441e628e071138be910224c374e566c778f8ee1455` | 2026-10-28T17:51:49Z |
| wt-rows | verbatim census row count on lane `corpus/SOURCES.md` | `143` (not the freeze) | 0 | `9d9b18720961e9b4689fd763b85e7b6f36160ccd3a8a1c9ddc5103bb0f66c396` | 2026-10-28T17:50:44Z |
| wt-tier | verbatim tier awk on lane file | `A=135 B=7 C=1 ` | 0 | `f92567e6a3f96144cf7fd84d7434f8632aaebe81508459029a829ce0f5cf1cea` | 2026-10-28T17:50:44Z |
| wt-status | verbatim status awk on lane file | `mined=138 rejected=5 ` | 0 | `ce68bd521924320c73181b8247562c8be758d00d02f5dd456a17a03b50762be4` | 2026-10-28T17:50:44Z |
| wt-malformed | verbatim malformed count on lane file | `0` | 0 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2026-10-28T17:50:44Z |
| wt-dup | verbatim duplicate-id check on lane file | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| wt-enum | verbatim enum check on lane file | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| wt-missing | verbatim missing-path check on lane file | `missing: corpus/lessons/round-47.md` while exit is 0 | 0 | `57aba0780e66bafd09a7d800cf494445b2a945dc881bc8f3fe992753bd571f30` | 2026-10-28T17:50:44Z |
| wt-missing-final | same missing-path command again | same stdout; path still absent | 0 | `57aba0780e66bafd09a7d800cf494445b2a945dc881bc8f3fe992753bd571f30` | 2026-10-28T17:53:17Z |
| script-census-lane | maintained census of live lane | rows 143; A 135; mined 138; rejected 5; queued 0 | 0 | `784b6b4fbbaaa0e15bf76d53603173e0bc461eb396f75fc56362795cd6e9f5c4` | 2026-10-28T17:50:45Z |
| script-validate-lane | maintained validate of live lane | `E11` S143 | 1 | `8c588ddeb4acac30b6310aadd9715a2fd5d4f61ce39d2b91692b4907abfcf3c5` | 2026-10-28T17:50:44Z |
| script-validate-lane-final | same validate again | same stdout, still exit 1 | 1 | `8c588ddeb4acac30b6310aadd9715a2fd5d4f61ce39d2b91692b4907abfcf3c5` | 2026-10-28T17:53:17Z |
| fz-head-move | freeze ancestor of then-HEAD; who added S143 | ancestor rc 0; file commit `e856beb552080c03ede6000b96f1b58bde44c421`; S143 only on HEAD, line 149, used-by `corpus/lessons/round-47.md` | 0 | `2540d7215233194778425ab4f5f08ab1e78b59732052c69b8396ee23d7a37924` | 2026-10-28T17:52:56Z |
| fz-round47-path | does `corpus/lessons/round-47.md` exist | worktree absent; freeze absent; HEAD absent (HEAD at command start `1e2c3102…`) | 0 | `c6f9f4bf3cbb42d09be12894f2de8bf5deb7daab45ceca116a0e2b431e167d1e` | 2026-10-28T17:53:07Z |
| fz-final-pin | HEAD vs both SOURCES blobs at last observation | HEAD `1e2c3102952dc636650095643c1963c833859019`; HEAD and worktree SOURCES blob `a7201ac9…`; freeze blob unchanged `bc817412…`; `round47=absent`; diff `1 0 corpus/SOURCES.md` | 0 | `aa6fad2777f234101dc08c6a7c4bcb669676398dea6a0827820f80714c62a98f` | 2026-10-28T17:53:17Z |
| script-census-freeze | `census --file` of the extract in scratch | same stdout as the view census (census `missing` is a missing registry file, not used-by). Not a path check | 0 | `a29f7abcc61ddbcf045e9f27d54cceb5cf522a7d3897795a54570a69e32352ed` | 2026-10-28T17:50:45Z |
| script-validate-freeze | `validate --file` of the extract in scratch | exit 1 from `E11` against the scratch parent directory. **Not a registry verdict.** Superseded by `script-validate-freeze-view` | 1 | `149491f4c7f135f039e0510c0370280482d3e30ef979405b93d4c6ddf8523c8e` | 2026-10-28T17:50:45Z |

## Census command exit, stated once

Freeze extract, seven `CORPUS.md` commands: all exit 0; malformed prints `0`; duplicate, enum, and missing-path stdout empty. That is a clean census of the freeze blob.

Verbatim `CORPUS.md` commands on the lane file: also exit 0, including the missing-path command, which printed a missing path. That exit 0 is not clean. Maintained `validate` of the lane exits **1**.

## Not run

`sources-census.sh overdue`, `shared`, `selftest`.
