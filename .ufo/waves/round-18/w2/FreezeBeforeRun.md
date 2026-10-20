PARTIAL

# FreezeBeforeRun — round 18 wave 2 (falsify)

Seat `KaidokuR18.FreezeBeforeRun`, an author-side advisory seat (read-only). This report is the only lane write.
Shorthand: `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (freeze),
`REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, `W=.ufo/waves/round-18`. Unless marked *local*, every anchor is a
`git show REV:<path>` line. None of the cited non-run files changed from F to REV (`git diff --name-status F REV`
lists only `W/runs/*`, `W/tools/routed-defects.py`, `.ufo/waves/round-17/predictions/SHA256SUMS`, LOG/SCORECARD/SKILL and corpus files).

## Verdict

**The freeze itself holds.** The measured runs began after the freeze: F was committed at 13:23:55-03:00, and GitHub
recorded its push at **16:23:57Z**. The earliest timestamp in any of the 15 receipts is 16:24:07.20Z, 10.2 s
later. The 33 prediction blobs at F are byte-identical at REV. F contains no round-18 `runs/` artifact. In every
run, the prediction bytes on disk at start and at end equal the F blobs.

**The stated scope is broken.** Three statements are false as written: "frozen in Git before any REA run"
(`W/claims.json:26`) and "before any round-18 REA run" (`W/claims.json:35`, `W/predictions/decision-rule.json:14`).
About 48 min before F, wave 1 ran REA `inspect-go-binary` on 3 of the 15 label carriers, one of them the held-out
`real-kimi-webbridge`. F itself contains the resulting Evidence IDs. The amendment's own timestamp also falls
inside the first measured run.

## Findings (by severity)

### F1 — MEDIUM (calibration): wave 1 ran REA on three label carriers before the freeze, contradicting "before any (round-18) REA run"
- **Observation.** `W/evidence/real-carrier-census.json:467-468`: kimi-webbridge has
  `"rea_evidence_id": "ev_3eb9c851f876fdf456420e056d8bd0c70066cdd6762f33485926313cb722dc24"`. The same file has
  `"generated_at_utc": "2026-10-20T15:35:51.750561+00:00"` at `:1473`, 48 min before the F commit. Its method is
  stated in `W/w1/RealCarrierCensus.md:22-23`: "REA `inspect-go-binary` (6.5.0, read-only)", and again at `:113-114`.
- **Observation.** The first step of the measured run produced the identical ID. `W/runs/real-kimi-webbridge/inspect-go.json`
  has `evidence_id` `ev_3eb9c851…`, provider `go-build-info`, operation `inspect_go_binary`. Two other census IDs also
  equal the measured-run IDs: calib-aether `ev_01b04ce9…` (census `:95`) and calib-notesmd-cli `ev_d5f4c18b…` (census `:304`).
  None of the 12 synthetic carriers' inspect-go IDs appears anywhere in F (the census covers only non-synthetic paths).
- **Observation.** By the lane's own schema, `inspect-go-binary` is run step 1. See
  `W/runs/calib-aether/receipt.json:2000` (`steps.inspect-go-binary.started_at_utc`).
- **Contradicted text:** `W/claims.json:26` ("frozen in Git before any REA run"), `W/claims.json:35`,
  `W/predictions/decision-rule.json:14`, and `corpus/lessons/round-18.md:10` ("predicted per carrier before any run").
  The correctly scoped wording is in `W/run-carriers.sh:2-3`: "frozen in Git before any measured run".
- **INFERENCE (no leak of the measured outcome).** `go-build-info` returns build metadata: Go version, dependencies
  and build settings. That metadata is a prediction *input*; for example, it sets route `fallback` 1.24.13→1.24.6. It
  is not the predicted Ghidra outcome (`Go analysis failure`, `Invalid index: 15606016`). I checked this from the keys
  and provider fields of `inspect-go.json`, not from REA source.
- **Repro:** `git -C $LANE grep -n -F ev_3eb9c851f876fdf456420e056d8bd0c70066cdd6762f33485926313cb722dc24 $F -- .`
  exits 0 with a single hit, `$F:.ufo/waves/round-18/evidence/real-carrier-census.json:468`.
- **Fix (append-only):** scope the claim to "before any round-18 REA `analyze` (Ghidra) run / measured run", and record
  the wave-1 build-info contact with real-kimi-webbridge, calib-aether and calib-notesmd-cli.

### F2 — LOW (calibration): the amendment's time is mis-stamped and contradicts its own text
- **Observation.** `W/claims.json:35` reads `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)"`.
  That text is already in F, whose committer time is 13:23:55-03:00, 65 s earlier. `W/runs/run-log.txt:2-3` shows
  calib-aether started at 13:24:07-03:00 and ended at 13:25:18-03:00. Read literally, the amendment is dated 53 s after
  a round-18 REA run began.
- **Inference.** The order of Git objects shows the amendment content came before the run, so this is a
  forward-rounded, unobserved time, not a post-hoc amendment.
- **Repro:**
  - `git -C $LANE show $REV:$W/claims.json | sed -n 35p` (exit 0)
  - `git -C $LANE log -1 --format=%cI $F` → `2026-10-20T13:23:55-03:00` (exit 0)
  - `git -C $LANE show $REV:$W/runs/run-log.txt | sed -n 2,3p` (exit 0)
- **Fix:** append a correction that gives the observed times: commit 13:23:55-03:00, push 16:23:57Z.

### F3 — LOW (calibration): "frozen before the run, matched 15/15" counts two labels whose outcomes were already in Git
- **Observation.** `SKILL.md:554-555` and `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:83` make the 15/15 claim.
  For calib-aether and calib-notesmd-cli, the round-18 analyze output is byte-identical to round-17 artifacts in F:
  - analyze stdout sha256: `a3db9af2…` and `caf1b4e6…`;
  - analyze Evidence IDs: `ev_247261e8…` and `ev_4fd342dd…`;
  - present in F at `.ufo/waves/round-17/runs/pro-aether/{analyze.json,receipt.json,carrier-run.stdout}` and the
    matching `pro-notesmd-cli` files.

  The calib-aether log is also the emulator's calibration source (`W/claims.json:26`). Some of this is disclosed:
  `W/predictions/decision-rule.json:3` marks both as `calibration_only`, and knowledge `:87-88` notes the repeated aether
  ID. The SKILL headline still does not separate them. 13 of 15 labels are blind to the Ghidra outcome
  (12 synthetic + real-kimi-webbridge), and both held-out D labels matched.
- **Repro:** `git -C $LANE grep -l -F ev_247261e857d89e710977e8a40f118e797c6f4b70eed5ea4d617822910b5a4af4 $F -- .`
  exits 0 and hits `round-17/runs/pro-aether/{analyze.json,carrier-run.stdout,receipt.json}`.
- **Fix:** qualify `SKILL.md:554` as "13 blind + 2 calibration labels".

## What holds (observations)

### Freeze time
- **Commit.** F has committer time 2026-10-20T13:23:55-03:00. Its author time, 12:06:56-03:00, is when the jj change
  was created. The jj op log (`c3b520d07089 12:06:56 commit c2638d2f…`) supports this, so the author time is not the
  freeze time [INFERENCE].
- **Local push record.** `.git/logs/refs/remotes/origin/main:29` (*local*) records `9011581… eb6c266… 1792513437 -0300 update by push`.
  1792513437 is 16:23:57Z.
- **Server-side push record (independent of lane tools).** `GET https://api.github.com/repos/VeigaPunk/shokunin-reverse-engineering/activity`
  returned HTTP 200 with `2026-10-20T16:23:57Z push refs/heads/main 9011581d8452 -> eb6c2668e5cb`. The next push
  (`eb6c… -> b2aad08`) is at 16:38:11Z.
- **jj op log** (read from a mkdtemp copy, origin removed, `--ignore-working-copy`): `dce4b09237ae 13:23:55 point bookmark main to commit eb6c…`,
  then `b567538f74f5 13:23:55 push bookmark main to git remote origin`.
- **Clock.** `timedatectl` reports `NTPSynchronized=yes`. The local reflog second equals GitHub's second, so a
  ≥10 s margin cannot be a clock-skew artifact [INFERENCE].

### Receipts: earliest timestamps, all after the push

| label | earliest step (inspect-go-binary `started_at_utc`) | Δ vs push |
|---|---|---|
| calib-aether | 16:24:07.220045Z (`runs/calib-aether/receipt.json:2000`; `pins_compare.pre_taken_at_utc` 16:24:07.202665Z at `:352`) | +10.2 s |
| calib-notesmd-cli | 16:25:18.975917Z | +82.0 s |
| s1246-noswiss-methods | 16:25:59.470913Z | +122.5 s |
| s1246-noswiss-nomethods | 16:26:21.987328Z | +145.0 s |
| s1246-swiss-methods | 16:26:44.997895Z | +168.0 s |
| s1246-swiss-nomethods | 16:27:07.506490Z | +190.5 s |
| s1250-noswiss-methods | 16:27:29.464235Z | +212.5 s |
| s1250-noswiss-nomethods | 16:27:50.923423Z | +233.9 s |
| s1250-swiss-methods | 16:28:12.435562Z | +255.4 s |
| s1250-swiss-nomethods | 16:28:33.897548Z | +276.9 s |
| s1246-swiss-nethttp | 16:28:55.362578Z | +298.4 s |
| s1246-noswiss-nethttp | 16:29:24.810842Z | +327.8 s |
| s1250-swiss-nethttp | 16:30:01.932144Z | +364.9 s |
| s1250-noswiss-nethttp | 16:30:36.150114Z | +399.2 s |
| real-kimi-webbridge | 16:31:09.270399Z | +432.3 s |

Supporting checks:
- **No timestamp precedes the push.** A recursive scan of every ISO timestamp in all 15 receipts found 0 at or before 16:23:57Z.
- **producer.json binds each run to F.** In 15/15 runs, `branch_tip` equals F (e.g. `runs/calib-aether/producer.json:5`).
  A commit hash cannot be written before the commit exists. `run-carriers.sh:244-263` writes this file just before
  `carrier-run.py` (`:269-274`).
- **Ghidra's own log starts after the push.** `runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log:1` begins
  `2026-10-20 13:24:09`, and every first log line is at or after that time.
- **The run log matches an independent file timestamp.** `W/runs/run-log.txt:1` reads "at producing revision eb6c2668…"
  and `:2` reads "calib-aether start 2026-10-20T13:24:07-03:00". The file is byte-identical to `/tmp/kr18-runlog.txt`
  (*local*; `cmp` exit 0), whose filesystem birth time is 13:24:07.093737339-03:00.

### Prediction blobs: F equals REV
- **Same tree.** `git rev-parse $F:$W/predictions` and `$REV:$W/predictions` both return `3b2ab6ffa0b23635b69fc4efd7921bf272756c08`.
  `diff <(git ls-tree -r $F -- $W/predictions) <(git ls-tree -r $REV -- $W/predictions)` exits 0 (33 entries), and
  `git diff --exit-code --stat $F $REV -- $W/predictions` exits 0.
- **Checksums verify.** `F:$W/predictions/SHA256SUMS` has 32 lines with 0 mismatches against the F blobs.
- **No other commit touched the frozen inputs.** `git log --diff-filter=AMD $REV -- $W/predictions $W/tools/swiss-misread.py $W/carriers` lists only F.
- **Prediction bytes did not change during any run.** In 15/15 runs, the sha256 of `predictions/<label>.prediction.json`
  in `pins_pre` and in `pins_post` equals the sha256 of the F blob. All 22 mid-run pin checks are equal, and
  `mid_run_drift_steps` is `[]` in 15/15.
- **Tools match F.** In 15/15 runs, all seven `producer.json` `tool_sha256` values equal the F blobs, and `c3.emulator_sha256`
  equals sha256(`F:$W/tools/swiss-misread.py`) = `14924bd6…`.
- **Carriers match the freeze.** In 15/15 runs, the receipt carrier `sha256_pre` = `sha256_post` = the prediction's
  `carrier.sha256` = the F value (`F:$W/carriers/SHA256SUMS` for synthetic carriers, `F:$W/predictions/carriers.tsv`
  column 4 otherwise). `run-carriers.sh:28,230` checks an out-of-lane SUMS file, which is byte-identical to the F copy
  (`cmp` exit 0); `sha256sum -c` on it exits 0.
- **Not a round-18 prediction.** The only predictions-path change from F to REV is `.ufo/waves/round-17/predictions/SHA256SUMS`
  (+1 line: the restored `carriers.tsv` entry, part of C1).

### Run artifacts at F
- **No runs directory.** `git ls-tree -r --name-only $F -- $W/runs | wc -l` returns 0.
- **No run tokens for the blind labels.** I probed 90 tokens from the REV receipts against F with `git grep -F`: bound
  session names, analyze Evidence IDs, analyze and inspect stdout digests, and retained-log digests. There were 0 hits
  for the 12 synthetic labels and for real-kimi-webbridge. All 6 hits belong to calib-aether and calib-notesmd-cli and
  point at round-17 artifacts (see F3). The 15 inspect-go Evidence IDs pre-exist in F only for those three labels (see F1).
- **No early run in the jj snapshots.** `git for-each-ref refs/jj/keep` lists 27 refs. Every kept commit dated at or
  before 13:23:55-03:00 has 0 round-18 runs files. Every kept commit that has predictions has tree `3b2ab6ff…`. Runs
  files first appear in commits dated 13:38:07; `5441b83d` holds three `ghidra.log` blobs identical to REV's.
- **No jj activity in the window.** The jj op log has 0 operations between 12:06:56 and 13:23:55. Because
  `snapshot.auto-track = "none()"`, jj snapshots would not have recorded untracked files anyway, so this is non-discriminating.
- **No REA or Ghidra leftovers in /tmp** (*local*). Between 12:06:56 and 13:24:07 there are no `*.gpr`, `*.rep`, `kr17*` or
  `rea-*` entries, only Ghidra source-extraction directories.
- **Wave 1 disclaims analyze.** The F-era wave-1 reports disclaim REA analyze and Ghidra. The only
  `rea-agents … analyze` at F is `analyze --help` (`W/w1/ScoutReaPin.md:31,158`).

## Residual risk and verification gaps
- **Self-reported times.** Receipt and producer timestamps come from lane tools on the host clock. The independent
  anchors are GitHub's push time, the F hash inside `producer.json`, and the run log's filesystem birth time.
- **A deleted early run could not be ruled out.** `run-carriers.sh:216` (`rm -rf "$outabs"`) would erase an earlier run
  under `runs/<label>`. With auto-track off and no jj operation in 12:06:56–13:23:55, no lane record would show such a
  run. The usual traces don't help:
  - npm debug logs rotate; the earliest surviving file was 16:31:09Z and was itself rotated out during the check;
  - `~/.config/ghidra/ghidra_12.1.4_PUBLIC/application.log` (mtime 2026-10-13) does not discriminate, because the
    measured runs did not touch it either.

  The case against an unlogged pre-freeze `analyze` rests on the wave-1 disclaimers and the absence of leftovers. That is not proof [INFERENCE].
- **Agent transcripts not read.** I did not read the L1 transcript (`history://`), to stay clear of the agent.db rule.
  The L1 or orchestrator can check whether any `analyze` command was issued before 13:23:55.
- **F1's no-leak inference** rests on the content of `inspect-go.json`, not on REA source.

## Commands run (exit codes)
Commands that used literal hashes are shown with the shorthand above.
- `git -C $LANE log -1 --format='%H%nauthor: %an <%ae> %aI%ncommitter: %cn <%ce> %cI%nsubject: %s' $F` → 0
- `cat -n $LANE/.git/logs/refs/remotes/origin/main | tail -n 5` → 0 (line 29 = the F push)
- `for t in 1792508818 1792513437 1792514291; do printf '%s ' $t; TZ=America/Sao_Paulo date -d @$t --iso-8601=seconds; done`
  → `1792513437 2026-10-20T13:23:57-03:00` (exit 0)
- `curl -sS -o gh-activity.json -w 'activity_http=%{http_code}\n' 'https://api.github.com/repos/VeigaPunk/shokunin-reverse-engineering/activity?per_page=30&ref=refs/heads/main'`
  → `activity_http=200` (exit 0)
- `git -C $LANE rev-parse $F:$W/predictions` and `$REV:$W/predictions`, plus `git diff --exit-code --stat $F $REV -- $W/predictions` → 0
- `diff <(git -C $LANE ls-tree -r $F -- $W/predictions) <(git -C $LANE ls-tree -r $REV -- $W/predictions)` → 0
- `git -C $LANE ls-tree -r --name-only $F -- $W/runs | wc -l` → `0` (exit 0)
- `git -C $LANE diff --name-status $F $REV | grep -v '^A	.ufo/waves/round-18/runs/'` → 0
- `git -C $LANE grep -F -l -e <token> $F --`, once per token: exit 0 for the hits listed in F1 and F3, exit 1 (no match)
  for every token of the 12 synthetic labels and for real-kimi-webbridge's analyze, session and log tokens
- `git -C $LANE show $REV:$W/runs/run-log.txt | cmp - /tmp/kr18-runlog.txt` → 0;
  `stat -c '%n birth=%w mtime=%y' /tmp/kr18-runlog.txt` → `birth=2026-10-20 13:24:07.093737339 -0300` (0)
- `git -C $LANE show $F:$W/carriers/SHA256SUMS | cmp - /home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS` → 0;
  `(cd /home/vgpnk/.local/share/kaidoku-r18/carriers && sha256sum -c --quiet SHA256SUMS)` → 0
- From `$LANE`, `git for-each-ref --format='%(objectname)' refs/jj/keep | while read c; do t=$(git log -1 --format='%cI' $c); s=$(git log -1 --format='%s' $c | cut -c1-60); pt=$(git rev-parse -q --verify "$c:.ufo/waves/round-18/predictions" 2>/dev/null || echo none); rn=$(git ls-tree -r --name-only $c -- .ufo/waves/round-18/runs | wc -l); echo "$t ${c:0:12} pred_tree=${pt:0:12} runs_files=$rn $s"; done | sort` → 0
- Inside the mkdtemp copy `/tmp/fbr-jj-FvPCMk`, created with `cp -a $LANE/.git` and `cp -a $LANE/.jj`, then
  `git remote remove origin`:
  - `jj --ignore-working-copy --no-pager op log --no-graph -n 80 -T 'id.short(12) ++ " " ++ time.start().format("%Y-%m-%dT%H:%M:%S%:z") ++ " " ++ description.first_line() ++ "\n"'` → 0
  - `jj --ignore-working-copy --no-pager config list snapshot` → `snapshot.auto-track = "none()"` (0)
- `find /tmp -maxdepth 3 \( -iname '*ghidra*' -o -iname '*rea-*' -o -iname 'kr17*' -o -iname '*.gpr' -o -iname '*.rep' \) -newermt '2026-10-20 12:06:56' ! -newermt '2026-10-20 13:24:07' -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' | sort`
  → 0 (16 Ghidra source-extraction paths only)
- `timedatectl show -p NTPSynchronized -p NTP -p TimeUSec` → `NTPSynchronized=yes` (0)
- Timing and pin-binding repro (verbatim; prints 15 rows, then `labels 15 fails 0`, exit 0):
```
python3 -I -B - <<'EOF'
import json, subprocess, hashlib
from datetime import datetime, timezone
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"; F="eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0"; W=".ufo/waves/round-18"
PUSH=datetime.fromtimestamp(1792513437, tz=timezone.utc)  # .git/logs/refs/remotes/origin/main:29
g=lambda *a: subprocess.run(["git","-C",L,*a],capture_output=True,check=True).stdout
labs=sorted({p.split("/")[4] for p in g("ls-tree","-r","--name-only",R,"--",W+"/runs").decode().split() if p.endswith("/receipt.json")})
fails=0
for l in labs:
    r=json.loads(g("show",f"{R}:{W}/runs/{l}/receipt.json")); prod=json.loads(g("show",f"{R}:{W}/runs/{l}/producer.json"))
    first=min(datetime.fromisoformat(s["started_at_utc"]) for s in r["steps"].values())
    key=f"{L}/{W}/predictions/{l}.prediction.json"; h=hashlib.sha256(g("show",f"{F}:{W}/predictions/{l}.prediction.json")).hexdigest()
    ok=(first>PUSH and datetime.fromisoformat(r["pins_compare"]["pre_taken_at_utc"])>PUSH and prod["branch_tip"]==F
        and r["pins_pre"]["entries"][key]["sha256"]==h==r["pins_post"]["entries"][key]["sha256"] and r["pins_compare"]["equal"])
    fails+=not ok
    print(f"{l:24s} first_step={first.isoformat()} +{(first-PUSH).total_seconds():.1f}s ok={ok}")
print("labels", len(labs), "fails", fails); raise SystemExit(1 if fails else 0)
EOF
```

## Tool installs
None. Existing tools used: jj 0.45.1 (`~/.local/bin/jj`, only inside the mkdtemp copy), git, python3 3.14.8, curl.

**Side effect, now removed.** Running jj inside the copy made jj register it in the user's jj config store:
`~/.config/jj/repos/bb9d70d25893cb966172/`, containing `config.toml` and a `metadata.binpb` naming
`/tmp/fbr-jj-FvPCMk/.jj/repo`, created at 13:53:08-03:00. I removed that directory together with the scratch
directories `/tmp/fbr-NQnQn4` and `/tmp/fbr-jj-FvPCMk`. The removal command, guarded by a check that the metadata
names the copy, exited 0, and a follow-up `ls` confirmed all three paths are gone.

The lane's own registry entry, `~/.config/jj/repos/82edd62c643a3add383a`, was not touched: its mtimes are 11:51:47 and
12:07:52. Seats that use jj in a mkdtemp copy should expect this registry write and remove it afterwards.
