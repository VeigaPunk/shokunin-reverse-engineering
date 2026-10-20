PARTIAL — the manifest half is discharged in substance. The run-log correction is true but drops one of the routed facts. Two supporting artifacts add low-severity overstatements. routed-defects' closure is deserved on the facts at REV, but its run-log check is token-derived and would also close on a negated sentence.

# TruthSUMSRUNLOG — R17-SUMS-RUNLOG at REV b2aad08 (round 18, wave 2 falsify)

- **Seat.** `KaidokuR18.TruthSUMSRUNLOG`. This is an author-side advisory seat, not an outside review.
- **Revisions.**
  - REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`
  - B `9011581d84527ba34c675f9cf912e54d2e72d470`
  - freeze `271167473d87ef710f07ecdd98caf0ce12091686` (`2711674`)
  - pass-1 store `da64646adcb19c1ede7537b799b8c7d283fe43da`
- **Anchors.** Every `path:line` below is a line of `git show REV:path`. The working-tree copies of all cited round-18 files and the spot-check equal their REV blobs (sha256 compared).
- **Axes.** (1) the truth of every number and hash in the correction; (2) whether the closing tool proves anything on its own; (3) side effects of the in-place edit.

## Verdict basis

- **Manifest facet: HOLDS** (observation). The line is restored byte-exact at its original position. The REV manifest is byte-identical to a fresh `sha256sum` regeneration over all 18 tracked `predictions/` files. `sha256sum -c` gives 18/18 OK. `carriers.tsv` has one commit in its history (the freeze).
- **Run-log facet: true but incomplete** (F1).
- **New overstatements** in supporting artifacts: F2 and F4, both low.
- **Tool.** The closure is deserved because I re-derived every fact independently. The tool alone does not prove the run-log half (F3).
- **Residual risk:** F5.
- **To reach HOLDS** (recommendation only):
  - Append one line stating that the pass-1 log has no aggregate exit line. The substitute record is the per-carrier exit files: 8/8 are 0 at `da64646`.
  - Relabel the mechanism in `sums-runlog.json:87` as INFERENCE and drop the header/footer premise.

## Findings (severity order)

### F1 — Low-Medium — the correction drops the routed "no final exit line" fact

- **Routed text.** `corpus/lessons/round-17-verifier-spotcheck.md:142`: "lists 7/8 carriers **and has no final exit line**".
- **Landed text.**
  - `LOG.md:2160` and `corpus/lessons/round-18.md:54` state 7/8, calib-shfmt absent, its receipt present, and pass-2 8/8. Neither mentions the exit line.
  - `round-18.md:65` (Mistakes row 4) covers only the manifest.
- **Reproduction (observation).**
  - `git grep -n -E 'final exit|exit line' REV -- LOG.md SCORECARD.md corpus/` → exit 0, one hit: `round-17-verifier-spotcheck.md:142`.
  - Repo-wide, the only other hit is the selftest fixture string `routed-defects.py:892`.
- **Fact (observation).**
  - The last line of `da64646:.ufo/waves/round-17/runs/run-log.txt` is `== pro-op end 2026-10-20T11:00:05-03:00 carrier-run=0 compare=0`. No aggregate exit for pass 1 is retained anywhere.
  - A substitute record exists: `carrier-run.exit`, `compare.exit` and `observation.exit` are all `0` for 8/8 labels at `da64646`.
- **Wave 1 already asked for this.** `w1/RevBaseSumsRunlog.md:112-114` asked for "7/8 with no exit marker while the log retained at A is pass 2 (8/8, exit 0)". Only the 7/8 / 8/8 half landed.
- **Effect.** Nothing stated is false. The line reads as the complete account and is not. Neither `contract.md:38-40` nor routed-defects tests this facet, so it closed silently.

### F2 — Low — `evidence/sums-runlog.json:87` states an inference as an observation, on a false premise

- **Text.** "It has no 'argv: ...' header and no 'run-carriers exit=N' footer — both of which the B copy carries — so the log began capturing after pass-1 output started and was committed (da64646 …) with a partial stream." The fields `:85-86` (`missing_final_exit_line`, `missing_argv_header`) are true as observations.
- **The premise is false** (observation):
  - No revision of `run-carriers.sh` emits either line. `git show <rev>:.ufo/waves/round-17/run-carriers.sh | grep -c -E 'argv|run-carriers exit'` → `0` at da64646, 95e34db, 9011581 and REV.
  - At REV the script ends with `exit $overall` (`run-carriers.sh:39`) and never echoes it.
  - `git grep -n -F '(all labels)' REV` hits only the logs and reports, never a script.
  - The pass-2 header and footer are wrapper text. Wave 1 had already established this (`w1/RevProducerRev.md:172-173`, `w1/RevBaseSumsRunlog.md:83-88`).
  - Their absence in pass 1 shows only that the pass-1 wrapper wrote no header or footer. It says nothing about when capture began.
- **The pass-1 driver is not in Git.**
  - `git cat-file -e 2711674:.ufo/waves/round-17/run-carriers.sh` → exit 128. The script was first committed at da64646, after pass 1 (`git log` on the path).
  - The out-of-tsv order (pro-esbuild-0.27.7 at 10:53:40 before pro-op at 10:55:55) is the real hint of a run that was not a single read. It remains INFERENCE.
  - `w1/SumsRestoreEvidence.md` labels this "Inference". The retained JSON, which `round-18.md:54` cites, does not.
- **What the JSON supports** (observation): calib-shfmt is the only missing label, and its pass-1 receipt exists. Its analyze step ended 4.69 s before the first logged line.

### F3 — Low — routed-defects closes R17-SUMS-RUNLOG on a wrong or negated LOG sentence and skips manifest lines that are not in 2711674

- **How the check works.** `log-fraction-true` (`routed-defects.py:592-609`) computes 7/8 from Git: 7 `start` lines at `da64646` over 8 tsv labels. It then only requires the tokens `R17-SUMS-RUNLOG`, `da64646` and `7/8` on one LOG line (`_line_with`, `:132-139`).
- **Mutations.** Each was built in a mkdtemp clone with the origin remote removed. Each changes one blob against REV.

  | mutation | change | routed-defects exit | open_count | R17-SUMS-RUNLOG |
  |---|---|---|---|---|
  | M1 | `LOG.md:2160` "calib-shfmt absent, its receipt present" → "pro-op absent, its receipt missing" | 0 | 0 | closed, 5/5 checks ok |
  | M2 | `LOG.md:2160` → "- R17-SUMS-RUNLOG: false alarm: the pass-1 \`da64646\` run-log is complete, the 7/8 figure was a miscount, and nothing needed restoring." | 0 | 0 | closed, 5/5 checks ok |
  | M3 | SHA256SUMS `replicate-expectations.json` hash `f5ce3d6b…` → `05ce3d6b…` | 0 | 0 | closed, 5/5 checks ok, while `sha256sum -c` exits 1 (`FAILED`) |

- **Who catches M3.** Only `controls.py`, in `prior_wave_evidence_blobs.r17_sums_restored_line.restored_ok: false`.
  - controls.py exits 0 either way: it reports, it does not gate.
  - REV retains no controls output.
  - No round-18 gate reads `restored_ok`: `git grep restored_ok REV -- .ufo/waves/round-18/` hits only `controls.py` and `w1/Controls18.md`.
- **Scope of the overclaim.** Two claims hold at the defect level, because the manifest half needs the real restore, but not for the run-log half:
  - `round-18.md:8`: "each closed by a named correction **and** a substance check".
  - `routed-defects.py:10-11`: "tokens alone cannot close it".
- **Closure is still deserved at REV.** The REV sentence is true by independent re-derivation; see the table below.

### F4 — Low — "the one in-place edit to round-17 evidence" (`round-18.md:54`)

- `controls.py:57-64` carves out six round-17 paths as contracted in-place modifications of frozen `.ufo/waves/` blobs. All six changed: `git diff --name-status B REV -- .ufo/waves/round-17/` → exit 0, six `M` lines:
  - `SHA256SUMS`
  - `tools/carrier-run.py`
  - `tools/compare.py`
  - `tools/log-extract.py`
  - `tools/receipt-validate.py`
  - `verify.py`
- Under the tool's own grouping (`prior_wave_evidence_blobs`), SHA256SUMS is one of six. The parenthetical is true only if tools and `verify.py` do not count as "evidence".
- "`controls.py` permits exactly it" is true (observation): `r17_sums_report` (`controls.py:271-313`) at B→REV gives `restored_ok: true`, `lines_added` = [the carriers.tsv line] and `lines_removed` = [].

### F5 — Info / residual — the restore makes round-17's retained SHA256SUMS pin stale, unstated

- `.ufo/waves/round-17/verification.json:1796-1800` (`pins_pre`) and `:1972-1976` (`pins_post`) record `predictions/SHA256SUMS` as sha256 `1b46b3edf114d98d93c39b92397cea5dcbe2c5699703f17a0abc7a3fd97ab42e`, size 1862.
- At REV the file has sha256 `b4ed972f568f2b0b3ae78d6947898c906851a6c10e0a5a141a563bb287399a11` and is 1953 bytes. The +91 bytes are exactly the restored line.
- No round-18 text names this. A future replay of "r17 pins equal the tree" will show one mismatch caused by round 18. No current claim is false.

## Re-derived claims (observation)

| Claim (site) | Re-derivation | Result |
|---|---|---|
| line lost between 2711674 and A (spotcheck:141) | `git log --format='%H %ad %s' REV -- …/SHA256SUMS` → b2aad08, 95e34db, 2711674 | holds: the only pre-REV edit is 95e34db, 11:27:35-03:00 |
| "dropped at `95e34db`" (LOG:2160, r18:54); JSON:13-20 | `git diff --numstat 2711674 B` → `1 1`. Two hunks: `@@ -2,7 +2,6 @@` (−carriers.tsv, old line 5) and `@@ -15,3 +14,4 @@` (+replicate-expectations.json) | holds. JSON's `hunk_header` names only the first of the two hunks (cosmetic) |
| carriers.tsv unchanged (spotcheck:75, JSON:24-34) | `git log REV -- …/carriers.tsv` → 2711674 only. Blob `e232bf2` at 2711674, da64646, 95e34db, de6c721, B and REV. sha256 `8ac38afe…3eb5` | holds |
| SUMS blob `b808abf…` at 2711674 = da64646, `99d122c…` at B (JSON:20) | `git rev-parse <rev>:path` | holds |
| "restored byte-exact" (r18:54) | `git diff B REV` → `+1/-0`, inserted at old position 5. `git diff 2711674 REV` → only `+…replicate-expectations.json` | holds |
| coverage restored (spotcheck:143) | In the clone at REV: `sha256sum -c --strict` gives 18 OK, exit 0. `comm -3` (LC_ALL=C) of tracked files vs manifest paths is empty; at B it lists `predictions/carriers.tsv`, at 2711674 it is empty. A regenerated manifest `cmp`s equal to the REV file, exit 0 | holds (strongest form) |
| B manifest: 17 lines, all OK (JSON:42-61) | clone at B: 17 OK, exit 0 | holds |
| pass-1 log lists 7/8, calib-shfmt absent (LOG:2160) | `da64646` log: 14 lines, 7 start, 7 end. `comm -3` of tsv labels vs started labels → `calib-shfmt` only | holds |
| "its receipt present" (LOG:2160); JSON:89-103 | Pass-1 receipt (`da64646:…/runs/calib-shfmt/receipt.json`): sha256 `03ba37a0…6c69`, steps 13:47:05.97Z–13:47:37.31Z exit 0/0, carrier sha256 pre = post `58f76563…`, compare.json `1b3bb3b1…29b3` with `all_match` true. The B/REV receipt is pass 2: `404a6f59…`, 14:27:41.94Z–14:28:19.50Z | holds |
| "window ends 5s before" (JSON:103) | 10:47:42-03:00 minus 13:47:37.309101Z = 4.69 s | holds (rounded) |
| "retained pass-2 log is 8/8" (r18:54); JSON:105-110 | REV log: 18 lines, 8 starts in carriers.tsv order, last line `run-carriers exit=0`. Blob `e33131d` since d0ab299 (11:47:24-03:00) | holds |
| "red at `9011581`" (r18:65) | routed-defects at B: R17-SUMS-RUNLOG open, 4/5 checks red. `carriers-tsv-identical` is green at B: it guards against tampering and is not a red-before check | holds |
| LOG append-only; spot-check untouched | `cmp <(git show B:LOG.md) <(git show REV:LOG.md \| head -c 139886)` exit 0. Spot-check blob `fa3058d` at both B and REV | holds |

## Requested run

```text
$ python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
exit=0  open_count 0, named_open_count 0, substance_open_count 0
R17-SUMS-RUNLOG: sums-covers-carriers-tsv ok, log-names-runlog-gap ok, sums-restored-from-2711674 ok,
                 carriers-tsv-identical ok, log-fraction-true ok ("7 start lines / 8 labels")
$ (same, --rev 9011581d84527ba34c675f9cf912e54d2e72d470)
exit=0  open_count 6; R17-SUMS-RUNLOG open (4/5 red)
```

**Is the closure deserved?** Yes, for this defect at REV:
- Every fact the five checks touch is true.
- I re-derived the facts they skip: which carrier is missing, the receipt, and full manifest verification.

It is not proof on its own: it also closes on M1, M2 and M3 (F3), and it never tests the exit-line fact (F1).

## Commands and exits

The lane was read with read-only git only. All writes went to a mkdtemp clone; that clone and its temp files are deleted after this report.

```text
git log --format='%H %ad %s' --date=iso-strict REV -- <SHA256SUMS|carriers.tsv|run-log.txt|run-carriers.sh>   exit 0
git diff [--numstat] 2711674 9011581… -- .ufo/waves/round-17/predictions/SHA256SUMS      exit 0
git diff [--numstat] 9011581… REV -- .ufo/waves/round-17/predictions/SHA256SUMS          exit 0
git diff 2711674 REV -- .ufo/waves/round-17/predictions/SHA256SUMS                        exit 0
git diff --name-status 9011581… REV -- .ufo/waves/round-17/                               exit 0
git show <rev>:.ufo/waves/round-17/run-carriers.sh | grep -c -E 'argv|run-carriers exit'  -> 0 (da64646, 95e34db, B, REV)
git cat-file -e 2711674:.ufo/waves/round-17/run-carriers.sh                               exit 128
git grep -n -E 'final exit|exit line' REV -- LOG.md SCORECARD.md corpus/                  exit 0 (spotcheck:142 only)
T=$(mktemp -d /tmp/truthsums-XXXXXX); git clone -q --no-hardlinks LANE $T/lane            exit 0
git -C $T/lane remote remove origin                                                       exit 0
(clone, checkout --detach <rev>; cd .ufo/waves/round-17) sha256sum -c --strict predictions/SHA256SUMS
                                                  exit 0 at 2711674 (17 OK), B (17 OK), REV (18 OK)
(clone at REV) git ls-files predictions | grep -vx 'predictions/SHA256SUMS' | sort | xargs sha256sum > $T/regen-SHA256SUMS   exit 0
cmp $T/regen-SHA256SUMS predictions/SHA256SUMS                                            exit 0
python3 -I -B $T/lane/.ufo/waves/round-18/controls.py 9011581… REV   exit 0 (r17_sums_restored_line.restored_ok true)
python3 -I -B $T/lane/.ufo/waves/round-18/controls.py 9011581… M3    exit 0 (restored_ok false)
```

Mutation recipe. This is a condensed equivalent of what I ran, with the same sed expressions and plumbing. Commit IDs vary per run; mine were M1 `a8c5c349…`, M2 `231e7dd6…`, M3 `fb88ea44…`.

```bash
C=$T/lane; R=b2aad08ceeee8dd125ce0d316056d8bd766c7f94
export GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x
mut() { b=$(git -C $C show $R:$2 | sed -e "$3" | git -C $C hash-object -w --stdin)
  GIT_INDEX_FILE=$T/i-$1 git -C $C read-tree $R
  GIT_INDEX_FILE=$T/i-$1 git -C $C update-index --cacheinfo 100644,$b,$2
  git -C $C commit-tree $(GIT_INDEX_FILE=$T/i-$1 git -C $C write-tree) -p $R -m $1; }
M1=$(mut M1 LOG.md '2160s/calib-shfmt absent, its receipt present/pro-op absent, its receipt missing/')
M2=$(mut M2 LOG.md '2160s/.*/- R17-SUMS-RUNLOG: false alarm: the pass-1 `da64646` run-log is complete, the 7\/8 figure was a miscount, and nothing needed restoring./')
M3=$(mut M3 .ufo/waves/round-17/predictions/SHA256SUMS 's/^f5ce3d6b/05ce3d6b/')
for m in $M1 $M2 $M3; do python3 -I -B $C/.ufo/waves/round-18/tools/routed-defects.py --root $C --rev $m; done   # each exit 0, open_count 0
git -C $C archive $M3 -- .ufo/waves/round-17/predictions | tar -x -C $T/m3   # then, in $T/m3/.ufo/waves/round-17:
sha256sum -c --quiet predictions/SHA256SUMS   # exit 1: predictions/replicate-expectations.json: FAILED
```

## Limits

- Not run: REA, Ghidra, any carrier, `jj`, any git write in the lane, `routed-defects.py --selftest`, `controls.py --selftest`.
- The pass-1 driver and ordering mechanism (F2) cannot be proven from Git and stays INFERENCE.
- Installs or updates: none.
