HOLDS

# ProducerJson — round 18 w2 (falsify), reviewer seat, author-side advisory

The claim holds for every label. All 15 runs have a `producer.json`. Each one records `branch_tip`
`eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`, and each of its 7 tool digests equals the sha256 of the
same blob at `eb6c2668`. No run lacks the file. The check can fail: run against baseline `9011581`, it
reports 15 tip mismatches and 75 hash mismatches. Three latent weaknesses in the *mechanism* are listed
below (all Low). None of them changes the 15 retained records.

REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` · C3 = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` · base = `9011581d84527ba34c675f9cf912e54d2e72d470`.
All commands were run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless noted.

## Observations (commands as run, exits)

**O1. Presence, tip and hashes, read at REV against the C3 blobs.** The label list comes from the frozen
`carriers.tsv`, so a missing run would print `LACKS`.
```
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 C3=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0; n=0; bad=0; for l in $(git show $C3:.ufo/waves/round-18/predictions/carriers.tsv | cut -f1); do p=.ufo/waves/round-18/runs/$l/producer.json; j=$(git show $REV:$p 2>/dev/null) || { echo "LACKS $l"; bad=$((bad+1)); continue; }; n=$((n+1)); [ "$(jq -r .branch_tip <<<"$j")" = $C3 ] || { echo "TIP $l"; bad=$((bad+1)); }; [ "$(jq '.tool_sha256|length' <<<"$j")" = 7 ] || { echo "NTOOLS $l"; bad=$((bad+1)); }; while read -r k h; do r=${k#/home/vgpnk/Projects/shokunin/kaidoku-shokunin/}; [ "$(git cat-file blob $C3:$r | sha256sum | cut -d' ' -f1)" = "$h" ] || { echo "HASH $l $r"; bad=$((bad+1)); }; done < <(jq -r '.tool_sha256|to_entries[]|"\(.key) \(.value)"' <<<"$j"); done; echo "labels_checked=$n bad=$bad"; [ $bad = 0 ]
```
→ `labels_checked=15 bad=0`, exit 0.

- The 15 TSV rows are at `C3:.ufo/waves/round-18/predictions/carriers.tsv:1-15` (unchanged at REV). They map
  to 15 run dirs and to 15 start/end pairs in `REV:.ufo/waves/round-18/runs/run-log.txt:2-31`, all with
  `carrier-run=0 compare=0`.
- Anchors, the same in all 15 files: `REV:.ufo/waves/round-18/runs/<label>/producer.json:5` is `branch_tip`,
  and `:7-13` hold the 7 `tool_sha256` entries. For example, `calib-aether/producer.json:5` is
  `"branch_tip": "eb6c2668…"` and `:7` is `carrier-run.py` → `6665dc7a…`, which equals the sha256 of
  `git cat-file blob C3:.ufo/waves/round-17/tools/carrier-run.py` (blob `37961db5`).
- Worktree vs REV: `git show REV:$f | sha256sum` equals `sha256sum $f` for all 15 files (`SAME` ×15). A
  separate `python3 -I -B` parse found 0 duplicate keys, `label` equal to the directory name, `branch` =
  `main`, and 7 tools each, with `TOTAL_BAD 0`, exit 0.
- **Negative control (the check can fail):** the same loop run with base `9011581` in place of C3 printed
  `vs_baseline tip_mismatch=15 hash_mismatch=75`. Between base and C3, 5 of the 7 tools differ: `M`
  carrier-run, compare, log-extract, receipt-validate, and `A` swiss-misread
  (`git diff --name-status 9011581 eb6c2668 -- <7 paths>`, exit 0). 15 × 5 = 75.

**O2. A second, independent witness: carrier-run's own pins.** A `python3 -I -B` pass over all 15
`receipt.json` files compared `pins_pre`/`pins_post.entries[*].sha256` with `producer.json` and with the
C3 blobs. It returned `TOTAL_ISSUES 0`, exit 0. Every receipt pins 8 lane paths: the 7 tools plus
`predictions/<label>.prediction.json`. All 8 equal the C3 blobs, so the frozen predictions were the ones
used. `pins_compare` is `equal:true` with `changed:[] missing:[]` in all 15. In every run,
`pins_pre.taken_at_utc` falls in the same second as `producer.recorded_at_utc`. The pin instants run from
16:24:07.20Z to 16:32:10.14Z, and adjacent runs' post/pre instants are about 0.15 s apart. Per QUALITY #19
(`REV:corpus/QUALITY.md:29`), this shows identical bytes at those instants. It does not show continuity
between them.

**O3. `branch_tip` was computed at run time, not typed in.** `REV:.ufo/waves/round-18/run-carriers.sh:246`
takes `git -C LANE rev-parse --verify "refs/heads/main^{commit}"`. The reflog
(`git reflog show --date=iso refs/heads/main -n 12`, exit 0) shows `main` → `eb6c266` at
`13:23:55 -0300` and → `b2aad08` at `13:38:08 -0300`, both entries "export from jj". The runs took place
from `13:24:07` to `13:32:10 -0300` (`run-log.txt:2,31`), entirely within the period when the tip was
`eb6c266`. The file layout (leading `,` separators and a blank line before `}`) matches the printf at
`run-carriers.sh:255-262`.

**O4. Worktree state during the run window (read-only git over `refs/jj/keep/*`).** The jj snapshot
`f11a961` (13:23:55, parent C3) and `bcc21ba` (13:38:07, which holds 15 `producer.json`; its `runs/` equals
REV) both have the driver, the 7 tools, `predictions/` and `selection.py` equal to C3
(`git diff --quiet C3 <c> -- …` → 0 for both). `f11a961` also carried uncommitted edits to `SKILL.md`,
`corpus/QUALITY.md`, `corpus/SOURCES.md`, the r17 knowledge entry and `round-17/predictions/SHA256SUMS`.
None of these is read by the run tools: `git show C3:<tool> | grep -n 'SHA256SUMS|/home/vgpnk'` finds only
`carrier-run.py:41 R16_SELECTION`. So "producing revision eb6c2668" is exact for everything the runs read.
The worktree as a whole was C3 plus corpus edits.

## Findings (all Low; none breaks the claim)

**L1 — A missing `main` ref degrades `branch_tip` to `null` silently, and the selftest cannot catch it.**
`run-carriers.sh:246-247` (`… 2>/dev/null || true`; empty → `tipjson=null`) neither fails nor sets
`overall=1`. The selftest check `:123` only counts the key (`grep -c '"branch_tip"'` = 1), and a `null`
value satisfies it. Round-18's own `revpin.py` treats the same condition as a refusal: `branch_missing`
at `REV:.ufo/waves/round-18/tools/revpin.py:57,100`. `contract.md:18` says to pin revisions as the branch
tip. Reproduced in a mkdtemp clone with origin removed (`/tmp/pj-r18.9DeLUx`, now deleted):
`git -C $CL/lane checkout -q --detach && git -C $CL/lane branch -D main`. I copied the REV driver, changed
only lines 20-22 (`W`/`W17`/`LANE` → the clone), and used the selftest's stubs (`run-carriers.sh:46-84`),
a one-row TSV and a matching SUMS file.
```
env TOOLS_DIR=$CL/tools PREDICTIONS_DIR=$CL/predictions SWISS_MISREAD=$CL/swiss-misread.py SELECTION_PY=$CL/selection.py SUMS=$CL/sums/SHA256SUMS RUNS_DIR=$CL/runs bash $CL/rc-nulltip.sh fakeA
```
→ `== fakeA end … carrier-run=0 compare=0`, `run_carriers_exit=0`, `producer.json` `"branch_tip": null`,
`grep -c '"branch_tip"'` → `1`. On the same clone,
`python3 -I -B .ufo/waves/round-18/tools/revpin.py --root $CL/lane --no-require-pushed` → `"finding":
"branch_missing"`, exit 2. This did not happen in the r18 pass (O1).
Suggested fix [INFERENCE]: refuse the run (exit 2) when the tip does not resolve, and make the selftest
assert a 40-hex tip.

**L2 — The comment at `run-carriers.sh:244-245` says "sha256 of every tool byte that produces this run's
receipts", which overstates what is retained (QUALITY #21, `corpus/QUALITY.md:31`).** The retained keys are
the 7 paths at `:256`. Neither `producer.json` nor the receipt pins hash the driver (`run-carriers.sh`,
blob `54509dfe`) or `carriers.tsv`:
`jq -r '.tool_sha256|keys[]' */producer.json | grep -c -E 'run-carriers\.sh|carriers\.tsv'` → `0`, and the
same grep over every `pins_pre.entries` key → `0`. Nothing records `jq`, the REA package bytes or the
Ghidra jars either. The receipts carry only the spec string `rea-agents@6.5.0` (2 hits per receipt).
`run-log.txt:1` ("at producing revision eb6c2668") is not printed by the driver, which emits only the
`== … start/end` lines (`:264,283`), so a wrapper wrote it [INFERENCE: author unknown]. The driver's
identity at run time therefore rests on O4's two snapshot instants plus the fact that C3 and REV hold the
same blob. No per-run record covers it. The integration prose is accurate as written:
`SKILL.md:591`, `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:2` and `corpus/lessons/round-18.md:53`
all say "branch tip and tool digests" and never "every".

**L3 — No gate reads `producer.json`. Its content is checked only by hand.**
`git grep -n 'producer\.json' REV -- .ufo/waves/round-18/verify.py .ufo/waves/round-18/measure.py
.ufo/waves/round-18/tools/` returns nothing. `verify.py:196-201` validates receipts per label but never
compares `branch_tip` or the tool digests against blobs. `corpus/lessons/round-18.md:64` lists "per-run
`producer.json`" under the column "fix (shown able to fail)" (`:60`). The only fail-able checks on it are
presence, parse and key count (`run-carriers.sh:122-126`). The `routed-defects.py` ancestor check named in
the same cell (`:504-527`) covers the R17 hashes, not r18 `producer.json`. O1 shows the content check can
be made fail-able cheaply.

## Residual risk / gaps
- Driver and TSV continuity between 13:23:55 and 13:38:07 is not evidenced (QUALITY #19). Only the two jj
  snapshot instants and the C3 = REV blob identity cover them (L2).
- `branch_tip` names `refs/heads/main`, not git `HEAD` or jj `@`. That is correct per `contract.md:18`, but
  `producer.json` does not record whether the worktree was dirty (O4 found unrelated dirty corpus files).
- Informational: `REV:.ufo/waves/round-18/w1/RunCarriers18.md:32,76` reports `.branch_tip` `9011581d…`
  from a pre-C3 `/tmp` dry-check. This is accurate for that dry-check, but it does not describe the
  retained runs.

## Hygiene
- Read-only git in the lane: `show`, `cat-file`, `ls-tree`, `log`, `reflog`, `for-each-ref`, `diff`,
  `rev-parse`, `merge-base`. I also ran one `git status --porcelain -- <paths>`, which may refresh the
  index stat cache opportunistically; the output was empty. No jj, no REA, no Ghidra, no carrier executed.
- Writes: this report. The mkdtemp clone `/tmp/pj-r18.9DeLUx` (origin removed, holding the L1 fixtures)
  was deleted after use.
- Installs/updates: none.
