# ExecErrataSweep — receipts

Seat `ExecErrataSweep`, wave 3 of round 50 attempt 2. Every command below was run by this
seat. No REA run. No git mutation in the lane or the fleet repo. Scratch
`/fast/scratch/hyaku/kaidoku-r50/w3-ExecErrataSweep` (removed after copying receipts here).

Lane read: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Fleet report read (read-only): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kaidoku.md`

## R1 — gap-rule reproduction (the load-bearing finding)

| field | value |
|---|---|
| command | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ExecErrataSweep/repro_gaps_ok.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ExecErrataSweep/repro-gaps-ok.json` |
| cwd | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ExecErrataSweep` |
| exit code | **0** (defect reproduced) |
| stdout | `{"defect_reproduced": true, "live": {"live:c6430": true, "live:c6490": true, "live:g7581": false, "live:g7582": false}, "pos": {"pos:c6430": true, "pos:c6490": true, "pos:g7581": false, "pos:g7582": false}}` |
| stdout sha256 | `ca444ce5412d6414dc7dcf5d1340bc773fa3861488881a581ebc95c71fcfca09` (`repro-gaps-ok.out`) |
| json-out sha256 | `6db7c0fc59b5f368db14e4ac213332290425bb09730cd89f029309b94efd2882` (`repro-gaps-ok.json`) |
| script sha256 | `f09b40da13a95ab74e709b78d6575f68e0dff46ec634cc314de247c9b7792fe9` (`repro_gaps_ok.py`) |
| utc | 2026-10-29T20:58:43Z |
| frozen counter sha256 (read inside the run) | `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813` |
| frozen gap-rule sha256 | `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef` |

Per-carrier result (the frozen counter's own `disposition_check`, replayed on the lane's own
frozen non-regular tables):

| carrier | gaps_ok | why |
|---|---|---|
| live g7581 | **False** | required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on `['dev/pts/0' … 'dev/pts/7', 'dev/tiatm', 'dev/ttyp0' … 'dev/ttyp2']` |
| live g7582 | **False** | same 12 entries |
| live c6490 | True | 613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries |
| live c6430 | True | 568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries |
| POS fixture g7581 / g7582 | **False** / **False** | same 12 entries (the committed POS fixtures reproduce it independently of the live run) |
| POS fixture c6490 / c6430 | True / True | as above |

`gap_rule_problems` (the counter's own parse of the rule) = `[]` — the rule is *valid*; it
is *insufficient* for the 7581/7582 carriers.

## R2 — counterfactual (which rule edit restores the four carriers)

| field | value |
|---|---|
| command | heredoc replaying the frozen `disposition_check` over three rule variants (script text is this receipt's §"script") |
| cwd | `$S` (scratch) |
| exit code | **0** |
| stdout sha256 | `01fde01829ba7f72d2bf057d372eb7622544717d3baebf5300fc404ac83a0533` (`counterfactual-gaprule.txt`) |
| utc | 2026-10-29T20:58Z |

```
### FROZEN (round-50 gap-rule.json)
   live g7581  gaps_ok=False required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7'
   live g7582  gaps_ok=False required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7'
   live c6490  gaps_ok=True  613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries
   live c6430  gaps_ok=True  568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries
### CF-1: required[char-device]=false (round-41 shape)
   live g7581  gaps_ok=True  637 gaps (1 structural), 3 removals, 0 silent, on 1001 non-regular entries
   live g7582  gaps_ok=True  637 gaps (1 structural), 3 removals, 0 silent, on 1001 non-regular entries
   live c6490  gaps_ok=True  613 gaps (1 structural), 1 removals, 0 silent, on 914 non-regular entries
   live c6430  gaps_ok=True  568 gaps (1 structural), 1 removals, 0 silent, on 824 non-regular entries
### CF-2: silent char-device += the 12 other details
   live g7581  gaps_ok=True  637 gaps (1 structural), 3 removals, 13 silent, on 1001 non-regular entries
   live g7582  gaps_ok=True  637 gaps (1 structural), 3 removals, 13 silent, on 1001 non-regular entries
   live c6490  gaps_ok=True  613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries
   live c6430  gaps_ok=True  568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries
```

Both counterfactuals leave c6490/c6430 green, so neither weakens the rule for the carriers
that already pass.

## R3 — the rule's own evidence gap (wave-1 seat said so)

| command | exit | output |
|---|---|---|
| `grep -n "second device major" -B 2 -A 2 .ufo/waves/round-50/w1/C1GapRule.md` | 0 | "- Only c6430 and a7530 censused (task cap). a7590/c6490 unknown: `tar -tvf` first (F2), then `unsquashfs -lls \| awk '{print substr($1,1,1)}' \| sort \| uniq -c`; any `b`/`p`/`s` row or a second device major:minor needs a rule edit before the freeze." |
| `sha256sum tools/round-50/gap-rule.json .ufo/waves/round-50/w1/C1GapRule/gap-rule.json` | 0 | both `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef` |
| `git log --oneline -- tools/round-50/gap-rule.json` | 0 | `435d41fd round-50: FREEZE — plan, C1/C2 counters, oracle and gap tables, run harness, controls driver and fixtures, r49 selftest` (one commit) |
| `grep "char-device" tools/round-50/oracle/g7581.nonregular.tsv` | 0 | 13 rows: `dev/led 247:0`, `dev/pts/0..7 136:0..136:7`, `dev/tiatm 230:0`, `dev/ttyp0..2 3:0..3:2` |
| `grep "char-device" tools/round-50/oracle/c6430.nonregular.tsv` | 1 (no match beyond one row) | `dev/led char-device 247:0` only |
| `python3 -c "import json;print(json.load(open('.ufo/waves/round-41/c1/gap-rule.json'))['required'])"` | 0 | `{'symlink': True, 'char-device': False, 'block-device': False, 'fifo': False, 'socket': False, 'dir': False}` (round-41: char-device not required) |

## R4 — attempt-1 controls tabulation (read, not re-run)

| command | exit | output |
|---|---|---|
| `sha256sum .ufo/waves/round-50/controls-attempt1/*/receipt.json …/summary.json …/score.out.txt` | 0 | c0 receipt `4e3e02031eb1cb597b713b21ef2eccd8b7437af824a93cbf466d0e61f47060e7`; c1 `0375e174a6fdd0803d87897a77ad5e43491dc4a40e1230275468c7544a140044`; c2 `11066a61d4bf783c82af1d7a85d1d4cfe01dbb56fc4409b4a8566ff62267b418`; c3 `cedeb61f77048cb8b542be525e9f8aa920d7932663abc23de2999c9b8fe845c8`; c4 `8ad3eec6646cde09fc703d63aa60fed7ef58325c0937427d78eb8c75be6b2cdb`; pos `7865b8b60f11fba440e0a189b1ca911f0cb3db5f8eca01a58ee31ae3019cd38e`; summary `45bfa9f29fa8fbb117156ee078a5fdf008b1446af93dd8106dc17b8207946348`; score.out.txt `b7e4249d86a37ff828d6d76102b7f9f743467775bffa019bbe1895d07e425b30` |
| `cat .ufo/waves/round-50/controls-attempt1/score.out.txt` | 0 | `{"controls": 6, "failures": ["CTL-C1-2", "CTL-C1-3", "CTL-C1-4", "CTL-C1-POS"], "kill_rule_fires": false, "unevaluated": []}` + `exit 1` |
| `python3 -c "import json;d=json.load(open('.ufo/waves/round-50/controls-attempt1/summary.json'));print(d['failures'],d['unevaluated'],d['kill_rule_fires'])"` | 0 | `['CTL-C1-2', 'CTL-C1-3', 'CTL-C1-4', 'CTL-C1-POS'] [] False` |

Per-control counter receipts (`counter.json`) carry `reason: "rerun_env_error"` and the exact
`unevaluable` text:

| control | exit | `unevaluable` (exact) | stdout sha256 |
|---|---|---|---|
| CTL-C1-2 | 2 | `REA provider_timeout on c6490 after 3 attempt(s); repeat on a quieter host` | `50f279f48f9f35fe2fccdaf5194e004bf1a1c177f7098c28c71d9935b3eb4c6c` |
| CTL-C1-3 | 2 | `REA provider_timeout on g7581 after 3 attempt(s); repeat on a quieter host` | `107d32bb1042bc242dff194758717b008b48b6dc06dc63a3f8f75454c9050421` |
| CTL-C1-4 | 2 | `REA provider_timeout on c6490 after 3 attempt(s); repeat on a quieter host` | `50f279f48f9f35fe2fccdaf5194e004bf1a1c177f7098c28c71d9935b3eb4c6c` |
| CTL-C1-POS | 2 | `REA provider_timeout on g7581 after 3 attempt(s); repeat on a quieter host` | `107d32bb1042bc242dff194758717b008b48b6dc06dc63a3f8f75454c9050421` |

Attempt-1 CTL-C1-0 / CTL-C1-1: `as_expected`, exit 1, `carriers_matched 0`, stdout sha256
`6d7f383453d0c84b2170c1c3625cbf29164e98eba0f40b9ac42c7098a082efc2` and
`cfa58b34fa299b34547fb2ad2ff57b5b2c78ce43789bed80d6f20535431ae765`.

Why the receipts say `misbehaved` and not `could_not_evaluate` (read, not asserted from the
report): the exit-2 counter receipt has no `carriers` key
(`keys: ['argv','counter','counter_sha256','exit_code','reason','unevaluable']`), so
`summarize()` returns `{'present': False}` and `c1-controls.py:1554-1567`'s
"counter-time REA rerun did not run" branch (the only writer of `status: could_not_evaluate`)
is unreachable; `judge()` then returns exit 2 with no `accept_refusal` → `misbehaved`.
Command: `python3 -c "import json;print(sorted(json.load(open('.ufo/waves/round-50/controls-attempt1/c2/counter.json')).keys()))"` → exit 0.

## R5 — attempt-2 controls (the L1's own artifacts; read, not re-run)

| command | exit | output |
|---|---|---|
| `python3 -c "import json;d=json.load(open('.ufo/waves/round-50/controls-attempt2.json'));print(json.dumps(d['controls'],indent=1))"` | 0 | see the report's F5 row: c0 `as_expected` (1, 0), c1 `as_expected` (1, 0), c2 `as_expected` (1, 0), c3 `as_expected` (1, 0), c4 `as_expected` (1, 2), **pos `misbehaved` (1, 2) — "expected exit 0, got 1"** |
| `python3 -c "import json;r=json.load(open('.ufo/waves/round-50/controls-attempt2/pos/receipt.json'));m=r['measured'];print(m['carriers_matched'],m['target'],[k for k,v in m['bindings'].items() if v is not True]);print(m['per_carrier_failing']['g7581'],m['per_carrier_failing']['g7582'])"` | 0 | `2 4 []` → every documentation binding is true; `g7581: ['gaps_ok']`, `g7582: ['gaps_ok']` |

## R6 — frozen-bytes and the C3 path rule (independently reproduced)

| command | exit | output |
|---|---|---|
| `git diff --stat 435d41fd4ad9211d1579fc447936fb33d2b74467 HEAD -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` | 0 | empty — the frozen bytes are unchanged at the tip |
| `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone" && git -C "$S/clone" checkout --detach f890bbead20ca2c549487167f56876ae47f1e1a4` | 0 | `HEAD is now at f890bbea …`; `git -C "$S/clone" rev-parse --show-toplevel` = `$S/clone` (asserted before the probe commits); `git -C "$S/clone" config user.name t` / `user.email t@e` set **in that clone only** |
| probe A: add `tools/round-50/sqfs-triage-v5.py` in the clone, commit, run the frozen counter's own `frozen_drift(root, freeze, rev, carriers.json)` | 0 | `frozen_drift = ['tools/round-50/sqfs-triage-v5.py']` — C1 would exit 2 `frozen_path_changed` at every later REV |
| probe B: add `tools/round-50-c3/sqfs-triage-v5.py` in the clone, commit, same call | 0 | `frozen_drift = []` (green); probe rev `4cc6ccac75dfb6b1b5a3bf8b5a17dfa8d6c0a9b5` |

The clone was a throwaway under `$S`; it is removed with the scratch.

## R7 — dispatch-spec staleness

| command | exit | output |
|---|---|---|
| `python3 -c "import json;d=json.load(open('.ufo/waves/round-50/w3-spec.json'));[print(i['name'],i['role'],i['prompt'].count('2026-10-29-r50-le-avm-hsqs-core'),i['prompt'].count('2026-10-28-r50-avm-le-squashfs-core'),i['prompt'].count('tools/round-50/sqfs-triage-v5.py')) for i in d['items'] if '2026-10-29-r50-le-avm-hsqs-core' in i['prompt'] or 'sqfs-triage-v5' in i['prompt']]"` | 0 | ScribeEntryC1 1/0/0; ScribeRowsSources 1/0/0; ScribeProvinceBinding 2/0/0; ScribeReadmeMap 1/0/0; RevEntryBar 1/0/0; ConnCrossClaim 1/0/1; ExecTriageV5 0/0/1; ExecRegistryRow 0/0/2 |
| `stat -c '%y %n' .ufo/waves/round-50/w3-spec.json` | 0 | `2026-10-29 17:30:16.748872284 -0300` |
| `git log -1 --format='%ci %s' 6f4aba63` | 0 | `2026-10-29 17:32:55 -0300 round-50: attempt-2 claims corrected — entry stem pinned to the frozen counter constants` |
| `git log -1 --format='%ci %s' 03f852b9` | 0 | `2026-10-29 17:38:32 -0300 round-50: C3 instrument path moved outside the frozen tools/round-50 walk (seat-measured frozen_drift)` |

## R8 — the six "over 1 MiB" wave-1 files

| command | exit | output |
|---|---|---|
| `for f in …/C1GapRule/census/a7530.lls …/C1GapRule/census/a7530.oracle.tsv …/C1OracleBuild/a7530/oracle.tsv …/C1OracleBuild/a7590/oracle.tsv …/C1RevLayout/receipts/a7530.auto.files.tsv …/C1RevLayout/receipts/a7530.le.files.tsv; do …` | 0 | **ABSENT** from disk, all six |
| `git log --all --oneline -- <each of the six>` | 0 | 0 commits each — never in any tree |
| `git ls-tree -r --long HEAD -- tools/round-50/oracle/` | 0 | 8 files: `c6430.{oracle,nonregular}.tsv`, `c6490.*`, `g7581.*`, `g7582.*` — **no `a7530`/`a7590` table exists**, so "their content is the frozen oracle tables" is false for these six |
| `sha256sum tools/round-50/oracle/c6430.oracle.tsv .ufo/waves/round-50/w1/C1GapRule/census/c6430.oracle.tsv .ufo/waves/round-50/w1/C1OracleBuild/c6430/oracle.tsv` | 0 | all three `f657ef513614824a9bfcf9f297bbe14482ac27a97dc6bb898481f2f1e49b5165` — the kept carriers' wave-1 copies ARE committed and byte-identical |
| `git ls-tree -r --long HEAD -- .ufo/waves/round-50/w1/ \| awk '$4>1048576' \| wc -l` | 0 | `0` — no wave-1 file over 1 MiB was committed (largest = 904 638 B `…/C1RevLayout/receipts/unsq-l-a7530.txt`) |

## R9 — SHONEN state and the unsourced load figure

| command | exit | output |
|---|---|---|
| `grep -n "^- \[" SHONEN.md` | 0 | `5:- [~] SKILL.md contains real decision tables…`, `8:- [~] At least one end-to-end domain task…`, `11:- [~] Instructions executable by an agent…`, `14:- [~] No cross-domain bleed…` |
| `grep -n "^- \[" /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kaidoku.md` | 0 | four `- [ ]` rows — the fleet report renders the same four boxes as unchecked |
| `grep -rn "load\|uptime\|nproc" .ufo/waves/round-50/controls-attempt1/` | 1 (no match) | no load measurement in any attempt-1 control receipt |
| `grep -n "load average" .ufo/waves/round-50/l1/dev-arm-timeouts.txt` | 0 | `host: load average 42.5-54 (uptime at run), nproc 32; REA 6.5.0 FIRMWARE_LIMITS.timeoutMs = 120000 (dist/cli-runtime), not tunable.` — the only load evidence in the lane |

## R10 — SOURCES id availability (for the A6 row)

| command | exit | output |
|---|---|---|
| `grep -cE '^ {0,3}\|\s*S[0-9]{3,}' corpus/SOURCES.md` | 0 | `152` rows |
| `grep -oE '^\| S[0-9]{3,}' corpus/SOURCES.md \| sort -u` | 0 | S001-S149 + S246, S247, S248 (S150-S242 intentionally skipped) |
| `for id in S243 S244 S245 S249; do grep -c "^| $id \|" corpus/SOURCES.md; done` | 0 | `0` for each — **all four planned ids are free** |
| `grep -n "S206" plans/round-50-attempt2-claims.md` | 0 | line 165: "Assimilation: theme AVM LE (attempt-1 Gate reaffirmed; staged S206 re-grounded as S243; …)" |
| `grep -n "^| S206 " /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` | 0 | the staged row is the **same source** as the planned S243 (Freetz patch 101, identical URL) — so the id re-grounding is consistent, **not** a collision; but the staged row's **tier is A** and the planned `rows.md` row's tier is **B** (as is `w1/C1SrcFreetz/S150-registry-row-draft.md`). The L1 must settle the tier explicitly; `CritSourcingRules` was asked "is tier B right for a distro patch file (S243)?" |

## R11 — carry-over item checks (subset; full table in `carry-over.md`)

| command | exit | output |
|---|---|---|
| `grep -c "2026-10-29-r50-le-avm-hsqs-core" corpus/SOURCES.md` etc. | 0 | see §A of `carry-over.md` |
| `grep -ci "shonen" plans/round-50-attempt2-claims.md` | 0 | `0` — SHONEN is not in the plan |
| `grep -c "QUALITY" plans/round-50-attempt2-claims.md` | 0 | `0` — QUALITY row 94 is not in the plan |
| `grep -oE '^\| [0-9]+ \|' corpus/QUALITY.md \| tr -d '| ' \| sort -n \| tail -1` | 0 | `93` — row 94 is still free |
| `git ls-tree -r --name-only HEAD -- .ufo/waves/round-50/w1/C2QualityDraft/` | 0 | `draft-quality-rows.md`, `receipts.txt`, `tools/round-50/c2q-probe.py` — the row-94 draft and its probe are committed |
| `grep -n "Big-endian and AVM SquashFS" SKILL.md` | 0 | `1607` — the stale live-limits line (F9) |

## Notes

- No tool installs, no host changes, no `sudo`, no service restarts.
- No file outside `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ExecErrataSweep{,.md}`
  was created or modified by this seat. The scratch clone and the scratch directory were
  removed after the receipts above were copied here.
- Nothing was written to `corpus/evidence/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`,
  `LOG.md`, `SCORECARD.md` or `SHONEN.md`; no git commit, push, stage, stash or other
  mutating git/jj command was run in the lane or the fleet repo.
