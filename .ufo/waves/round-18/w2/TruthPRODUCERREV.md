PARTIAL

# TruthPRODUCERREV: is R17-PRODUCER-REV discharged at REV, judged on substance?

- **Seat.** `KaidokuR18.TruthPRODUCERREV`, wave 2 (falsify). This is an author-side advisory seat, not an outside review.
- **Revisions.** REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
- **Method.** Read-only Git objects (`git show REV:path`), with `python3 -I -B`.
- **Scratch.** All scratch work ran in `mktemp -d /tmp/truthprod*` copies. Each one was a `--bare --no-local` clone with `origin` removed, or a `git archive` extract. Every one was deleted afterwards (`rm -rf` printed "cleaned").
- **Not done.** No REA or Ghidra run, no carrier executed, no `jj` command, no git write in the lane, no installs.
- **Writes.** This report is the only write.

## Verdict

- **Core attribution holds.** Pass 1 was produced by `2711674`'s `carrier-run.py` (blob `bc964ac`). Pass 2 was produced by `95e34db`'s (blob `c536e3e`). `d0ab299` produced neither pass. I re-derived this three independent ways:
  - receipt key sets compared with what each tool blob can emit;
  - commit and push instants compared with receipt instants;
  - a replay of the extractor and comparator. Neither tool reads receipt fields, and they tell the two candidate tool versions apart.
- **The correction text adds new overstatements:** F2, F3, F4 and F5 below.
- **The `routed-defects.py` closure is not earned by the tool.** For this defect its "substance" checks only look for the two pinned hashes on a line, plus an ancestry check that was already true at the baseline. If I swap the passes, or negate the attribution outright, it still reports the defect closed (F1).
- **Is the closure deserved?** On substance, yes for the two passes. The tool's verdict is not evidence of that.

## Assigned command

```text
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
exit 0 — open_count 0; R17-PRODUCER-REV open=false; 6/6 checks ok (scorecard/knowledge-names-producing-revs,
scorecard/knowledge/log-names-pinned-revs, producer-revs-are-ancestors)
```

- The working-tree tool is the REV blob: `git hash-object` and `git rev-parse REV:…/routed-defects.py` both give `bd6390e693755e4f72adf9d8b90a063cfc543a2d` (exit 0).
- At the baseline (same tool, `--rev 9011581…`) the run exits 0 with `open_count 6`. R17-PRODUCER-REV is open with 5 checks failing. `producer-revs-are-ancestors` is **already ok** there.

## Findings, by severity

### F1 (Medium): the gate's "substance" checks for this defect only look for two pinned hashes

**Observation: what the checks test.** `b2aad08:.ufo/waves/round-18/tools/routed-defects.py:504-527` does two things:

- It requires a line containing `R17-PRODUCER-REV` plus both `PRODUCER_REVS` (`:60-61`) in SCORECARD, the knowledge entry and LOG.
- It requires that both hashes are ancestors of REV.

Nothing ties each hash to its pass, and nothing rejects negation. Ancestry was already true at `9011581` (assigned-command section above), so the defect's red-before state rests entirely on the text-token checks.

**Reproduction (observation).** I ran mutations in a mkdtemp bare clone with origin removed, using the REV copy of the tool. Script in Reproduce §R1.

| Variant (applied to SCORECARD:2440, knowledge:206, LOG:2161) | Tool exit | open_count | R17-PRODUCER-REV |
|---|---|---|---|
| control, REV as is | 0 | 0 | closed |
| swap: pass 1 ↔ pass 2 hashes (commit `ed8b37dc…`) | 0 | 0 | **closed** |
| negate: "neither `2711674…` nor `95e34db…` produced any round-17 receipt; `d0ab299…` produced all sixteen." (commit `eb0e98a0…`) | 0 | 0 | **closed** |
| drop the LOG line (harness red control, commit `6e5bbf11…`) | 0 | 1 | open, `log-names-pinned-revs` |

**Observation: the tool's own selftest fixture accepts a wrong role.** The closed fixture `_PRODUCER_LINE` (`:819-822`) says "pass produced by {PRODUCER_REVS[0]} …, verified at {PRODUCER_REVS[1]}". That fixture assigns `95e34db` the *verifying* role, and in-process selftest case 4 (`:1050-1065`) requires `open_count 0` on it.

**Which claims are false for this defect:**

- `routed-defects.py:10-11`: "tokens alone cannot close it".
- `corpus/lessons/round-18.md:8`: each defect is "closed by a named correction **and** a substance check".
- `round-18.md:64`: "routed-defects checks both producer hashes are ancestors". That check has no red-before state.

**Inference.** The closure is right only because the hard-coded constant matches the w1 derivation, which I confirmed independently (see "What holds"). The tool could not detect a wrong attribution.

**Advisory fix.** Tie each hash to its pass in the text. Then derive the attribution instead of pinning it:

- pass-1 receipts at `da64646` lack every field emitted by the blob at H2 (`child_env_keys`, `mid_run_drift_steps`, `pin_checks`);
- pass-2 receipts at `d0ab299` lack `md5_pre`, which `d0ab299`'s blob emits.

### F2 (Low): "`d0ab299` … not a producer" is false as written, because `d0ab299` produced the replicate receipt

**What the correction says.**

- `b2aad08:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:206` ends: "`d0ab2992149a…` is the verification revision, not a producer".
- `b2aad08:SCORECARD.md:2440` says "the receipts were produced by" `2711674` (pass 1) and `95e34db` (pass 2). It names no third producer.

**Observation: the replicate receipt.** `b31975d:.ufo/waves/round-17/verify/replicate/calib-shfmt/receipt.json` carries:

- `carrier.md5_pre`;
- `binding` = `{logfile_ok, md5_ok, target_ok}`;
- analyze from `14:47:37.753` to `14:48:08.374Z`.

Among the committed `carrier-run.py` blobs, only `d0ab299`'s emits `md5_pre`/`md5_ok`. Counted with `grep -c`: `2711674` 0/0, `95e34db` 0/0, `d0ab299` 2/3.

**Observation: the run that produced it.** `b31975d:.ufo/waves/round-17/verification.json` records:

- `source_revision` = `d0ab2992…`;
- `worktree_dirty_at_start: []`;
- command `bash …/run-carriers.sh calib-shfmt` with `RUNS_DIR=verify/replicate`, exit 0, `14:47:36.959–14:48:08.485Z`.

That run was after the `d0ab299` push at 11:47:26 -03 (origin reflog).

**Observation: the scorecard counts this receipt as evidence.** `SCORECARD.md:2364` ("replicate run `calib-shfmt` exit 0 with the identical Evidence ID"), `:2366` and `:2374` ("replicate `verify/replicate/calib-shfmt`") all cite it.

**Inference.** Scoped to the two passes, the sentence is true. Unqualified, it misattributes the best-attributed receipt of round 17: the only r17 carrier receipt whose producing run recorded a clean worktree, in `verification.json`; the receipts themselves carry no worktree field. That is the same class of error R17-PRODUCER-REV was routed for. Fix: "not a producer of either pass; producer of the replicate receipt".

### F3 (Low): "by blob `c536e3e`" for all 8 pass-2 receipts is an unlabelled inference that contradicts the lane's own account

**Observation: what can and cannot be seen in the receipts.**

- Between `c536e3e` and `d0ab299`'s blob, `carrier-run.py` changed only in these places:
  - md5 (`d0ab299:…/carrier-run.py:340-344`);
  - binding;
  - the `run_step` timeout branch (`95e34db:…:159-160` `proc.kill()` → `d0ab299:…:171-172` `_stop_group`);
  - the timeout exit (`d0ab299:…:425-427`).
- Across 16 steps per pass, no receipt has `timeout` true or a `stop` key, and every exit is 0. So the timeout edits cannot be seen in any receipt.

**Observation: the lane says the tool changed during pass 2.**

- `b2aad08:corpus/lessons/round-17.md:122` says: "The second pass started at `95e34db`. During it, `carrier-run.py` gained a bytecode guard and a group stop and exit on timeout; both paths stayed unexercised because no run timed out."
- `d0ab299:.ufo/waves/round-17/w2/StopGroupTest.md:3-4` says the file was "observed again mid-run at w2-hardened rev". Its F2 anchors are `carrier-run.py:159-160` `proc.kill()` (`:39-40`), which is the `c536e3e` text. That report does not exist at `95e34db` (`git cat-file -e` non-zero).

**Observation: that same lesson line is partly wrong.** The bytecode guard is already at `95e34db:…/carrier-run.py:30`, committed at 14:27:35Z, before the pass began at 14:27:41.94Z. Round 18 reconciled neither account.

**Observation: Git has no snapshot of the working tree during pass 2.**

- The HEAD reflog for 10:46–11:50 -03 has only `commit:` entries.
- The empty-description `refs/jj/keep` commits start at 11:51:47 -03, after `d0ab299`.
- I did not read the jj op store, because the contract forbids running jj in the lane.

**Inference.** The receipts match `c536e3e` in every field it emits, and they rule out `d0ab299`'s blob. They cannot rule out an uncommitted blob that differs only in timeout paths. `RevProducerRev.md:249-253` (§5.1) stated this limit. The corrections at knowledge:206, SCORECARD:2440 and LOG:2161 drop it.

### F4 (Low): "`d0ab299` verified them" (`b2aad08:LOG.md:2161`) blurs the R17-VALIDATE16 count again

**Observation.**

- `verification.json` (source `d0ab299`, clean worktree) holds 8 `receipt-validate` runs, all on `runs/<label>/receipt.json`, which are the pass-2 blobs. `LOG.md:2106` says "8/8".
- Pass 1 was validated in round 18 "under the `9011581` validator" (`LOG.md:2159`; `summary.json` `validator_rev` `9011581…`).
- That validator is byte-identical to `d0ab299`'s (blob `2762496c…`, sha256 `618448829b…`).

**Inference.** The statement is true only in the sense of "validator bytes". As an event, the `d0ab299` verification pass verified pass 2 only. Suggested wording: "`d0ab299`'s verification pass validated pass 2; pass 1 was validated in round 18 with the same validator bytes".

### F5 (Info): "pass N was produced by <rev>" is exact for the tools, not for the pass driver

**Observation: pass 1's driver was not committed at `2711674`.**

- `git cat-file -e 2711674:.ufo/waves/round-17/run-carriers.sh` exits 128.
- The file was first added at `da64646` (`--diff-filter=A`), 11:06:06 -03, six minutes after pass 1 ended.
- calib-shfmt's pass-1 run (13:47:05–13:47:37Z) is not in the pass-1 run-log, which starts at 10:47:42 -03.

**Observation: pass 2's run-log was framed by an unrecorded wrapper.** Its `argv:` header and `run-carriers exit=0` footer are not echoed by `95e34db`'s `run-carriers.sh`, which ends with `exit $overall`. Also seen in w1 RevProducerRev E7.

**Where the broad wording appears.** `LOG.md:2161` and `round-18.md:53` say "pass"; knowledge:206 and SCORECARD:2440 correctly scope the claim to receipts.

## What holds, re-derived (observations)

| Claim (where it appears) | Re-derived value | Result |
|---|---|---|
| Pass-1 receipt window 13:47:05–14:00:05Z (knowledge:206) | 13:47:05.973725 to 14:00:05.292289 (min/max of all `*_utc` across 8 receipts at `da64646`) | ✓ |
| Pass-2 receipt window 14:27:41–14:40:02Z (knowledge:206; spotcheck:139) | 14:27:41.944543 to 14:40:02.318153 at `d0ab299` | ✓ |
| `carrier-run.py` blob `bc964ac` at `2711674`; `c536e3e` at `95e34db` | `bc964acd…` at `2711674` and at `da64646`; `c536e3e4…` at `95e34db`; `f91bbc76…` at `d0ab299` | ✓ |
| Pass-1 receipts stored at `da64646`; pass-2 receipts stored at `d0ab299` | Pass-1 blobs identical at `95e34db` and `da64646`, all 8 replaced at `d0ab299`. Pass-2 blobs identical at `d0ab299`, `9011581` and REV | ✓ |
| What each blob can emit vs what the receipts contain | Pass 1: one 16-key set, `pin_checks` 0. Pass 2: one 18-key set, `pin_checks` 2–8 per run (sum 29). `md5_pre` 0/16; `binding` = `{logfile_ok, target_ok}` 16/16. `grep -c` per blob: `2711674` has 0 of `child_env_keys`/`mid_run_drift_steps`/`pin_checks`; `95e34db` 3/1/2; `md5_pre`/`md5_ok` appear only in `d0ab299`'s blob (2/3) | ✓ (pass 1 = `bc964ac`; pass 2 ≠ `d0ab299`'s blob) |
| Commits and pushes | `2711674` 10:46:45/47 -03, `95e34db` 11:27:35/37, `d0ab299` 11:47:24/26. Commit = `%cI`; push = origin reflog | ✓ |
| Extractor/comparator replay (does not use receipt fields) | Pass-2 `observation.json` = `95e34db`'s `log-extract.py` output 8/8 (path fields stripped). `d0ab299`'s extractor differs on 3/8 (it adds `FixGcWriteBarrierFlagBackgroundCommand` lines). Pass-1 `compare.json` = `2711674`'s `compare.py` output 8/8; `95e34db`'s differs on pro-esbuild-0.27.7 (it adds `extra.*`) | ✓ corroborates both passes; rules out `d0ab299` as producer of pass-2 observations |
| Corrections are append-only | `git diff --numstat 9011581 REV`: LOG 44/0, SCORECARD 14/0, knowledge 8/0 (single hunk `@@ -198,0 +199,8 @@`). r17 `runs/`, `verify/` and `verification.json` unchanged | ✓ |
| "Round-18 runs record `producer.json` (branch tip + tool digests)" (`round-18.md:53`) | 15/15 files, one tip `eb6c2668…`, one digest set, 0 mismatches against the blobs at that tip | ✓ |

## Residual risk and verification gaps

- **Working tree during the passes (F3).** No receipt records a digest of the tool itself. The working tree between commits cannot be recovered from Git refs. The jj op store was not inspected.
- **The R17-PRODUCER-REV gate (F1).** It cannot detect a wrong attribution. Every later edit to these three lines is unguarded on meaning.
- **Out of scope.** Wording sites outside SCORECARD, LOG, the r17 knowledge entry and `round-18.md` were not exhaustively swept for "measured source revision".
  - `LOG.md:2071` and `corpus/lessons/round-17.md:145` name `d0ab299` as the verification-pass source revision, which is correct.
  - `predictions/replicate-expectations.json:83` `first_pass_revision` = `da64646` is a storage location in a frozen file and was left as is.

## Reproduce (as run, from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; exit codes observed)

```text
git show -s --format='%H %cI %s' b2aad08… 2711674… 95e34db… d0ab299… da64646… 9011581…          exit 0
git rev-parse {2711674,95e34db,d0ab299,da64646}:.ufo/waves/round-17/tools/carrier-run.py               exit 0
git reflog --date=iso-strict refs/remotes/origin/main ; git reflog --date=iso-strict HEAD             exit 0
git for-each-ref refs/jj --format='%(refname) %(objectname:short) %(committerdate:iso-strict) %(subject)'   exit 0 (27 refs)
git cat-file -e 2711674:.ufo/waves/round-17/run-carriers.sh                                            exit 128
git log --diff-filter=A --format='%H %cI' -- .ufo/waves/round-17/run-carriers.sh                      exit 0 (da64646)
git cat-file -e 95e34db:.ufo/waves/round-17/w2/StopGroupTest.md                                        non-zero (absent); d0ab299: 0
git show 95e34db:.ufo/waves/round-17/tools/carrier-run.py | cat -n | sed -n '30p;156,163p'             exit 0
git show d0ab299:.ufo/waves/round-17/tools/carrier-run.py | cat -n | sed -n '168,174p;337,345p;423,427p'  exit 0
for r in 2711674 95e34db d0ab299; do for k in child_env_keys mid_run_drift_steps pin_checks md5_pre md5_ok; do git show $r:.ufo/waves/round-17/tools/carrier-run.py | grep -c $k; done; done   exit 0
git ls-tree -r --name-only b31975d -- .ufo/waves/round-17 | grep 'receipt\.json$' | grep -v /runs/      exit 0
git show b31975d:.ufo/waves/round-17/verification.json | python3 -I -B -c '<print source_revision, worktree_dirty_at_start, receipt-validate/run-carriers commands>'   exit 0
git rev-parse {d0ab299,9011581,b2aad08…}:.ufo/waves/round-17/tools/receipt-validate.py; git show <rev>:… | sha256sum   exit 0
python3 -I -B - <<EOF  (16 receipts via `git show {da64646,d0ab299}:…/runs/<label>/receipt.json`: min/max *_utc,
  key sets, md5_pre, binding keys, pin_checks, steps.*.timeout/stop/exit; blob ids at 95e34db/da64646/d0ab299/9011581/REV)   exit 0
python3 -I -B - <<EOF  (15 r18 producer.json: branch_tip set; sha256 of `git show <tip>:<rel>` vs recorded)       exit 0
git diff --numstat 9011581… b2aad08… -- SCORECARD.md LOG.md corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md   exit 0
git diff --stat 9011581… b2aad08… -- .ufo/waves/round-17/runs .ufo/waves/round-17/verify .ufo/waves/round-17/verification.json   exit 0 (empty)
```

**§R1 Mutation (F1), condensed from the script as run.** The setup commands and the tool invocation are the ones that ran, with some lines joined by `;` and `$c` shown as `<commit>`. The comments summarize the inline `MUT` program and the index plumbing. The `bash <<'EOF' … EOF` script exited 0; every tool exit inside it was 0.

```bash
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94
T=$(mktemp -d /tmp/truthprod.XXXXXX); git clone -q --bare --no-local "$LANE" "$T/lane.git"; git -C "$T/lane.git" remote remove origin
git -C "$LANE" show "$REV:.ufo/waves/round-18/tools/routed-defects.py" > "$T/routed-defects.py"
# MUT (python3 -I -B -c): on lines containing R17-PRODUCER-REV and both hashes —
#   swap: exchange 271167473d…↔95e34db62…; negate: replace the line with the "neither … d0ab299… produced all sixteen." text;
#   droplog: delete the line in LOG.md only.
# For SCORECARD.md, LOG.md, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:
#   GIT_DIR=$T/lane.git GIT_INDEX_FILE=$T/idx git read-tree $REV;  git show $REV:<f> | MUT | git hash-object -w --stdin;
#   git update-index --cacheinfo 100644,<blob>,<f>;  git write-tree;  git commit-tree -p $REV -m "mutation <mode>" <tree>
python3 -I -B "$T/routed-defects.py" --root "$T/lane.git" --rev <commit>     # per variant; results in the F1 table
rm -rf "$T"
```

**§R2 Extractor/comparator replay ("What holds"), described from the script as run.** The script exited 0.

- Extract tools and predictions at each revision: `git archive <rev> .ufo/waves/round-17/tools .ufo/waves/round-17/predictions | tar -x -C $T/<rev>`, for `2711674`, `95e34db` and `d0ab299`.
- For each label, write the retained `ghidra.log` (`git show <store>:…/runs/<label>/logs/*/ghidra.log`) to `$T/g.log`.
- Run the tools from inside each extracted revision:
  - `python3 -I -B tools/log-extract.py --log $T/g.log`;
  - `python3 -I -B tools/compare.py --prediction predictions/<label>.prediction.json --observation <retained observation>`.
- Compare JSON with the `log_path`, `observation` and `prediction` keys removed.
- Pairs: store `d0ab299` was tested against tools at `95e34db` and `d0ab299`; store `da64646` against tools at `2711674` and `95e34db`.

## Tools

Nothing was installed or upgraded. Lane parser scripts (`log-extract.py`, `compare.py`) ran only from mkdtemp `git archive` copies, against retained log text. No REA, Ghidra or carrier binary was run.
