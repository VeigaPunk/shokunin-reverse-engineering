# Round 30 wave 2: ReviewM293 (M29-3 disclosure in round-29 claims.json)

Seat: KaidokuR30.ReviewM293 (reviewer, attack). Lane checks were read-only. The only write was a sandbox clone under scratch. REA was not used, and no carrier or mutant was touched.

**Attacked:** the `instrument_supersessions` entry appended to `.ufo/waves/round-29/claims.json` in commit `004053d6`. It is between lane base `d210fb8f` and measured revision `92b1dd2d`. Three properties were attacked: (a) the change is append-only, (b) the recorded sha256 is accurate, (c) the gates behave as the entry says.

**Verdict: HOLDS.** All three properties hold. I found no blocking defect, and two low-severity findings. `INSTRUMENT_UNPINNED` on round 29 stays FLAGGED in `tools/round-29/freeze-gate.py`, and this is by design. That gate reads pins only from the frozen claims blob at `dbd87cfa`. It reads `instrument_supersessions` only to discount `INSTRUMENT_REVISED` commits (`freeze-gate.py:108-114,127-128,132-136`). No append after the freeze can clear it, and the entry says so itself.

## Evidence (all observations unless labelled)

### (a) Append-only: holds
- Command `git -C <lane> diff d210fb8f 92b1dd2ddc119fda89a611ba515bdf6cfe906f76 -- .ufo/waves/round-29/claims.json` gave exit 0 at 2026-10-23T03:12:03Z. The only hunk is `@@ -65,5 +65,8 @@`. It turns the closing `]` of `not_claimed` into `],` and adds `"instrument_supersessions": [ {...} ]`. No other line changes.
- `git log --format='%H %s' 92b1dd2d -- .ufo/waves/round-29/claims.json` lists exactly two commits: `dbd87cfa` (the freeze) and `004053d6`, whose message ends `round-29 M29-3 disclosure (append-only)`. `git show --stat 004053d6 -- .ufo/waves/round-29/ tools/round-28/ corpus/claim-freezes-v2.tsv` prints `.ufo/waves/round-29/claims.json | 3 +++`.
- A JSON comparison at 03:13:01Z (python over `git show`) printed `freeze==base True`, `changed keys ['instrument_supersessions']` and `order preserved True`. Every frozen key and value, including `claims`, `instruments`, `loaded_by_counter` and `producers_not_counters`, is identical at `92b1dd2d`.
- Ancestry check: `git merge-base --is-ancestor` returned 0 for both `dbd87cfa → 92b1dd2d` and `d210fb8f → 92b1dd2d`, and `004053d6` lies in `d210fb8f..92b1dd2d`.

### (b) The sha256 is accurate: holds
- Command `git show <rev>:tools/round-28/c1-heldout-naming.py | sha256sum` at 03:12:21Z gave `29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c` at every revision checked: `bacbe9cc31d0…`, `dbd87cfa09eb…`, `d210fb8fa62d…`, `92b1dd2ddc11…` and HEAD `3502b94c5b93…`. The working-tree copy has the same hash. This matches the entry's `"sha256": "29c2b571…7c"`.
- `git rev-list dbd87cfa..92b1dd2d -- tools/round-28/c1-heldout-naming.py | wc -l` gave `0`. `git log --all -- <file>` lists only four commits, all at 2026-10-22T14:17:15/16-03:00 (round-28 freeze `87d3dfb6` and three jj-side commits), and every one has blob sha `29c2b571…`. `87d3dfb6` is an ancestor of `bacbe9cc`, and `bacbe9cc` (the round-28 verifier spot-check, 16:30:33-03:00) is an ancestor of `dbd87cfa`. So the entry's sentence "holds at bacbe9cc, at that freeze and at the measured rev" is correct.
- The entry's `commit` field is `dbd87cfa…`, the round-29 freeze commit itself, and the reason text calls the entry a "pin note (not a revision disclosure)". This is consistent: no revision commit exists to disclose.
- Supporting claims in the reason text:
  - "c1-fresh-naming.py never loads or runs it" holds. At both `dbd87cfa` and `92b1dd2d`, `grep` finds `c1-heldout` only at `:4` inside the docstring (`:2-41`). The only `exec` target is `RESOLVER = "tools/round-25/a2/resolve-selectors.py"` (`:55`, used at `:130,:449`).
  - "primary_rule names this file only as provenance" holds. The frozen claims `:41` read `"primary_rule": "openchain_sole_unfiltered_args_consistent (round-25 rule 5; unchanged from tools/round-28/c1-heldout-naming.py)"`.

### (c) Gate behaviour: holds as stated
- Command `python3 -I -B tools/round-29/freeze-gate.py --root <lane> --rev 92b1dd2d…` gave exit 0 at 03:12:23Z. For round 29 it printed `"findings": [{"finding": "INSTRUMENT_UNPINNED", "path": "tools/round-28/c1-heldout-naming.py"}], "freeze": "dbd87cfa…", "verdict": "FLAGGED"`. There is no `INSTRUMENT_REVISED`, which is consistent with the empty rev-list. Summary: `audited 20, clean 3`. **This stays FLAGGED by design** (see the verdict above). The round-24 gate (`.ufo/waves/round-24/tools/freeze-gate.py`, exit 0, 03:13:29Z) also flags round 29 `INSTRUMENT_UNPINNED`, for this path plus the three `producers_not_counters` paths. That matches the lesson's "both freeze gates flag round 29" (`corpus/lessons/round-29-verifier-spotcheck.md:125`).
- The ledger agrees. Command `freeze-gate.py … --rev 92b1dd2d --disclosures corpus/claim-freezes-v2.tsv` gave exit 1 at 03:13:07Z with `"exact": 19, "mismatched": [], "missing": ["round-30"], "stray": []`. The round-29 row (`claim-freezes-v2.tsv:20`, `round-29 FLAGGED INSTRUMENT_UNPINNED … M29-3`) matches the gate exactly. The exit 1 comes only from the missing round-30 row; see Residual risk.
- Command `python3 -I -B tools/round-30/prefreeze-gate.py --root <lane> --round 29` (default `--rev HEAD` = `3502b94c`) gave exit 0 at 03:12:24Z:
  ```
  prefreeze round=round-29 freeze=dbd87cfa09eb89306c4e07d3171a4556eb732024 rev=3502b94c5b93d86c5d67866035fd150899456295 claims=.ufo/waves/round-29/claims.json
  pins=12 present=12 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=6 tools_unpinned=0 findings=0
  verdict=CLEAN
  ```
  The output is the same at `--rev 92b1dd2d` and at `--rev 004053d6` (exit 0, CLEAN). At the pre-disclosure parent `--rev a6e7d9ce` it gave exit 1 with `FINDING TOOL_UNPINNED tools/round-28/c1-heldout-naming.py`, `tools_unpinned=1`, `verdict=FLAGGED`. `--selftest` printed `selftest cases=20 failures=0`, exit 0.

## Findings

1. **Low. The prefreeze CLEAN on round 29 comes from the appended entry alone, and the entry's `sha256`/`commit` fields are not checked by either gate.** (observation)
   - Sandbox control: clone at `92b1dd2d`. Commit `df3e03ea` replaces the entry's sha256 with `0`×64 and its commit with `f`×40.
   - `prefreeze-gate.py --root <clone> --round 29 --rev df3e03ea` gave exit 0 at 03:13:52Z with `tools_unpinned=0 findings=0 verdict=CLEAN`. On the same commit, freeze-gate still reports round 29 `FLAGGED INSTRUMENT_UNPINNED`.
   - So the sha's accuracy rests on independent checks like (b), not on any gate. This is documented: `prefreeze-gate.py:37-38` reads "an `instrument_supersessions` entry is honoured on path+reason, its commit and sha256 fields are not verified". The w1 builder also showed the gate turning green on this remedy (`.ufo/waves/round-30/w1/ExecPrefreezeGate.md:88`, control 3).
   - (inference) Nobody should cite the round-29 prefreeze `verdict=CLEAN` as evidence that round 29 was pinned at freeze. It only shows that a reasoned supersession entry exists at `--rev`. I found no lane text at `92b1dd2d` that cites it that way: `git grep 'prefreeze.*round 29|round=round-29'` finds only the w1 dispatch, spec and report.
2. **Low (wording). The reason says "this entry does not clear the gate's INSTRUMENT_UNPINNED finding", but at `92b1dd2d` three gates exist.** That sentence is true for both freeze gates (round 24 and round 29), the only ones that emit `INSTRUMENT_UNPINNED`. It does not say that the round-30 prefreeze gate turns CLEAN because of this entry. (inference) A reader could take "the gate" to mean every gate. The frozen record is unaffected; any clarification belongs in the round-30 SCORECARD or the ledger, not in another claims.json edit.

## Residual risk and verification gaps
- `freeze-gate.py --disclosures corpus/claim-freezes-v2.tsv` exits 1 at `92b1dd2d` because `round-30` has no ledger row (`missing: ["round-30"]`). This is outside the M29-3 scope. (inference) The row is presumably added at round-30 filing. Any filing check that runs this command with `--disclosures` will stay red until the row exists.
- Commit timestamps and authorship are not authenticated: this is a limit of both gates and is not tested here.
- I did not check that `corpus/lessons/round-29-verifier-spotcheck.md` item 3 is closed elsewhere (SCORECARD round-30 section). Only the claims.json entry and the gates were in scope.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewM293/`)
| file | sha256 |
|---|---|
| diff-claims29.txt | 991aa62e456238e12dc95aaf85919d8d825231a8c2bbd5c7a96c25a371f827bc |
| sha-c1-heldout.txt | 61e5bff42e3d714a693eaf7ae11d1625f9a5e1985780c027e3af1547110558d3 |
| freeze-gate-92b1dd2d.txt | 15d1da16234064da1ca08913776b24af62a4df240037309925f5d79c3735b9c4 |
| freeze-gate-disclosures.txt | 837644fe4669a0999a900fd57308503edd971066b65bc4f5b58fc55dd2620acc |
| freeze-gate-r24.txt | 7c63c276193389561fd7469ea922275fefb3ab1c65dd02f9fbcc199d8b4788f0 |
| prefreeze-r29.txt | 453d883587e725a54d707acce0f31f6a9d6387f32612940150ce4301bdf4ab63 |
| claims-freeze.json (blob at dbd87cfa) | 76bc0d8f556019763157bbb74cd43b9983b9e7cf77ad9d92cae898365a60cf79 |
| claims-measured.json (blob at 92b1dd2d) | eec205d3b388b557e63a6253f95c80e94a6e121c57b3b0012d2a9123c7461ee4 |

`clone/` is a sandbox clone holding control commit `df3e03eabfa418af25a75a488e5c72579d0c986c`. Tool installs: none. Processes: every command was bounded by `timeout` and none is left running.
