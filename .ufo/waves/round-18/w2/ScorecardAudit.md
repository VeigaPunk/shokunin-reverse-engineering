PARTIAL

# ScorecardAudit: round-18 section of SCORECARD.md at REV (wave 2, author-side advisory)

Seat `KaidokuR18.ScorecardAudit`, a leaf seat. This report is a recommendation, not an admission.

**How the audit ran**
- **Lane access:** read-only git only (`show`, `diff`, `log`, `ls-tree`, `cat-file`, `reflog`, `ls-remote`, `archive`).
- **Scratch space:** mkdtemp `/tmp/scaudit.gegweO`. It holds a `git clone --shared --no-checkout` of the lane. The `origin` remote was removed before any write (`git remote` printed nothing). The directory was deleted after the run.
- **Not run:** no installs, no REA or Ghidra, no carrier executed. The r17 validator only reads and hashes carrier files.

**Conventions**
- Commands run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` with:
  - `B=9011581d84527ba34c675f9cf912e54d2e72d470`
  - `REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`
  - `F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`
- Anchors are `REV:path:line`.
- Everything is an observation unless it is tagged [INFERENCE].

## Verdict basis

| Check | Result |
|---|---|
| Append-only vs B | **Holds.** numstat `14 0`; lines 1-2426 are a byte-identical prefix. |
| Every number in REV:SCORECARD.md:2428-2440 is true | **Holds.** Every number reproduced (table below). VALIDATE16 reproduced byte-exact. |
| Every number carries its command | **Does not hold (F2).** |
| Correction precision | **R17-PINMAP is under-scoped (F1).** |
| Adjacent | The instruments behind the "each mid map" claim cannot falsify it (F3). The claims.json amendment instant is wrong (F4). |

## Findings (all LOW; no number is false)

### F1 LOW, calibration: the R17-PINMAP correction still overstates for pass 1

**What the section says.** REV:SCORECARD.md:2438 says the r17 row "is wrong for mid-run instants: they retain the comparator verdict against the retained pre map, not the map". The corrected row, REV:SCORECARD.md:2374, cites "16 across two passes, 8 retained at HEAD, 8 at `da64646`".

**What the receipts show.**
- The 8 pass-1 receipts at `da64646` have no mid-run instants and no verdicts: `pin_checks=0` and no `pins_changed_during_run` in 8/8 (command 1, exit 0).
- Their producer is carrier-run blob `bc964ac`. It is the same blob at `2711674` and `da64646`.
  - It takes mid-run snapshots but records only on drift (`git cat-file -p bc964ac`, lines 422-432).
  - `grep -c pin_checks` on the blob gives 0.
- The verdict-only shape exists only in pass 2:
  - Producer blob `c536e3e` (at `95e34db`), lines 461-466: `pins.compare(pins_pre, mid)` appended to `pin_checks`.
  - That gives 29 entries (4+2+3+2+4+4+2+8).

**Comparison.** REV:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:204 is scoped correctly ("each of the 29 second-pass … entries"). The SCORECARD line is not.

**Advisory fix.** Append: "pass-1 (`da64646`) receipts retain no mid-run instants or verdicts; pass-2 mid-run instants retain the verdict, not the map."

### F2 LOW, operability: the section carries a command for none of its numbers

**Observation.**
- REV:SCORECARD.md:2428-2440 contains no invocation.
- Its one evidence pointer is `summary.json` (:2439). That file's keys are `receipts, remap, rev, validator_rev, validator_sha256`. It records no argv and no remap script.
- The derivations do exist at REV, but nothing in the section links to them:
  - The validate16 argv is in `.ufo/waves/round-18/w1/Validate16Run.md:46-59`. It is partly prose, for example "Receipt prefix-rewrite python" and "replaced by a python subprocess loop".
  - Producer blobs and push times are in `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:206` and `w1/RevProducerRev.md`.
  - "8 retained validations" comes from `.ufo/waves/round-17/verification.json`.
- :2434 defers measured values to a "Measured records" subsection. That subsection does not exist at REV: `git show REV:SCORECARD.md | grep -c 'Measured records'` → 1, which is the reference itself (exit 0).
- So at REV the section has no C1/C2/C3 before→after value. The r16 rows (REV:SCORECARD.md:2305-2310) and r17 rows (:2363-2368) put their commands inline.

**[INFERENCE]** This is normal for a pre-falsify commit. It becomes a defect only if the verification pass appends values without their commands.

**Advisory fix.** Append the commands from the table below, or link each correction line to its derivation.

### F3 LOW (adjacent, instruments): the round cannot falsify "each mid map"

**The claim holds at REV.** REV:SCORECARD.md:2438 says "round-18 receipts retain each mid map with `map_sha256`". Command 2 (exit 0) checked 15/15 receipts and 22/22 maps: each blob's sha256 equals `map_sha256`, entry counts match, and every entry matches `pins_pre`.

**Neither instrument can show it false.**
- `REV:.ufo/waves/round-18/tools/routed-defects.py:323-372` returns ok on the first receipt that qualifies (:365-368). The stated intent at :238-239 is "a round-18 receipt".
- `REV:.ufo/waves/round-18/verify.py:201` runs receipt-validate without `--require-mid-maps` (`grep -c -- --require-mid-maps` → 0). REV:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:205 says that flag is "for round-18 receipts". The flag exists in REV's receipt-validate.py (5 hits).

**Mutation test.** Command 4, in the clone with origin removed:
- Commit `d7f9aa7` on top of REV drops 19 of the 22 mid-map blobs (14 of 15 runs).
- `routed-defects.py --rev d7f9aa7` → exit 0, `open_count 0`, `r18-receipt-pinmaps ok: True`.
- Its detail text cites only "calib-aether … 3 pin_checks".

**Advisory fix.** Either require every run in `_pinmaps_retained_check`, or pass `--require-mid-maps` at verify.py:201.

### F4 LOW (adjacent): the claims.json amendment instant has no command and contradicts git

**The stated instant.** `REV:.ufo/waves/round-18/claims.json:35` says `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)"`.

**What git and the receipts show.**
- The amendments block is already in F (`grep -c '"amendments"'` → 1). claims.json is unchanged from F to REV (empty diffstat).
- F was committed at 13:23:55 -0300 and pushed at 13:23:57 -0300 (reflog).
- The first round-18 REA run started at 16:24:07.20Z, which is 13:24:07 -0300 (calib-aether `pins_pre`).
- So the stated 13:25:00 is later than the commit that contains it, and later than the first run.
- Separately, `contract.md:148` dates the same amendments "~12:40 -03:00".

**What still holds.** The substance, "amended before any run", is true by the commit and push times. SCORECARD :2431 cites this file.

## Number → command table (observations; exit codes as run)

| REV line | Number / claim | Command | Exit | Result |
|---|---|---|---|---|
| — | append-only | `git diff --numstat B REV -- SCORECARD.md` | 0 | `14	0	SCORECARD.md` |
| — | prefix identity | `cmp <(git show B:SCORECARD.md) <(git show REV:SCORECARD.md \| head -n 2426)` | 0 | Identical; B ends in `\n`. `git log --oneline B..REV -- SCORECARD.md` → only `b2aad08`. |
| 2430 | baseline `9011581` | `git rev-parse F^` | 0 | Equals B; equals the claims.json `baseline` field. |
| 2430-31 | predictions frozen at F | `git diff --stat F REV -- .ufo/waves/round-18/predictions/ .ufo/waves/round-18/tools/swiss-misread.py` | 0 | Empty. In all 15 r18 receipts, the 2 pinned prediction files per label have sha256 equal to the F blobs. |
| 2431 | "pushed" | `git reflog show --date=iso refs/remotes/origin/main`; `git ls-remote origin refs/heads/main` | 0; 0 | F "update by push" at 13:23:57 -0300 (16:23:57Z), 10 s before the first run (16:24:07.20Z). Remote main is REV. |
| 2438 | `:2374` quote | `git show REV:SCORECARD.md \| sed -n 2374p \| grep -c 'pre/mid/post pin maps with instants'` | 0 | 1 |
| 2438 | verdict, not map | command 1 | 0 | Pass 2: 8/8 receipts, keys `changed,entries,equal,missing,taken_at_utc`, 29 entries in total. Pass 1: 0 (F1). |
| 2438 | r18 mid maps | command 2 | 0 | 15/15 receipts, 22/22 maps verified. |
| 2439 | `:2364` quote | `… sed -n 2364p \| grep -c 'all 16 receipts `receipt-validate.py` exit 0'` | 0 | 1 |
| 2439 | "8 retained validations" | python over `git show REV:.ufo/waves/round-17/verification.json` | 0 | 79 commands, 8 of them `receipt-validate-*`, all exit 0, all on the working-tree (pass-2) receipts. |
| 2439 | "8/8 exit 0 via remapped copies" | command 3 | 0 ×8 | Each run: 341 checks, 0 findings, stderr 0 B. Stdout sha256 after path normalization equals `summary.json` 8/8. Validator sha256 `6184…126f` matches the summary. The validator blob at B is the same as at `d0ab299` (`2762496`). 16 prefix occurrences per receipt. |
| 2440 | `:2352-2356` names the verification revisions | `… sed -n 2352,2356p \| grep -c -E 'd0ab2992…\|b31975de…'` | 0 | 2 |
| 2440 | pass 1 = `2711674` | blob ids, key fingerprint, instants (command 1) | 0 | carrier-run blob `bc964ac` is the same at 2711674 and da64646. Neither the blob nor the 8/8 receipts have pin_checks or md5_pre. Runs 13:47:05–14:00:05Z fall between the 2711674 push (13:46:47Z) and the da64646 push (14:06:09Z). |
| 2440 | pass 2 = `95e34db` | same | 0 | Blob `c536e3e` has pin_checks and no md5_pre, matching 8/8 receipts. `f91bbc7` at d0ab299 has md5_pre, so it does not match. Runs 14:27:41–14:40:02Z fall between the 95e34db push (14:27:37Z) and the d0ab299 push (14:47:26Z). r17 `runs/` is unchanged from d0ab299 to REV (empty diffstat). |

**[INFERENCE]** The producer attribution rests on key fingerprints plus timing. It cannot rule out an uncommitted working-copy variant.

Cross-check: `python3 -I -B routed-defects.py --root <clone> --rev B` → exit 0, open_count 6. With `--rev REV` → exit 0, open_count 0. The scorecard checks for PINMAP, VALIDATE16 and PRODUCER-REV go from false to true.

## Commands (verbatim)

1. Pass instants and mid fields (exit 0):
```bash
for c in da64646adcb19c1ede7537b799b8c7d283fe43da b2aad08ceeee8dd125ce0d316056d8bd766c7f94; do for d in $(git ls-tree -d --name-only $c .ufo/waves/round-17/runs/); do git show $c:$d/receipt.json | python3 -I -B -c '
import json,sys
d=json.load(sys.stdin); a=d["steps"]["analyze"]
ts=[d["pins_pre"]["taken_at_utc"],d["pins_post"]["taken_at_utc"]]
print(sys.argv[1], d["label"], min(ts), max(ts), "pin_checks=%s"%len(a.get("pin_checks") or []), "md5_pre=%s"%("md5_pre" in d["carrier"]), "drift_rec=%s"%("pins_changed_during_run" in a))
' ${c:0:7}; done; done
```

2. Round-18 mid maps (exit 0). For each `runs/<label>/receipt.json` at REV, a python step does the following for every `pin_checks[i]`:
   - `git show REV:<map_path minus lane prefix>`
   - assert `sha256 == map_sha256`
   - assert `len(entries) == entries`
   - assert every `pins_pre` sha256 equals the map's sha256 for that path
   - count `pins/mid-*` blobs per label

   Output: `verified == pin_checks == mid_files` for all 15 labels, `pre_entries=152`, `bad=[]`.

3. VALIDATE16 reproduction (inside the mkdtemp clone; every validator run exit 0):
```bash
D=$(mktemp -d /tmp/scaudit.XXXXXX); git clone -q --shared --no-checkout "$LANE" "$D/clone" && git -C "$D/clone" remote remove origin
W="$D/clone/w"; mkdir -p "$W/val" "$W/receipts" "$W/out" "$W/.ufo/waves/round-16"
git -C "$D/clone" archive da64646 .ufo/waves/round-17 | tar -x -C "$W"
git -C "$D/clone" show da64646:.ufo/waves/round-16/selection.py > "$W/.ufo/waves/round-16/selection.py"
git -C "$D/clone" show 9011581:.ufo/waves/round-17/tools/receipt-validate.py > "$W/val/receipt-validate.py"
git -C "$D/clone" show 9011581:.ufo/waves/round-17/tools/pins.py > "$W/val/pins.py"
for f in <8 labels>; do
  git -C "$D/clone" show da64646:.ufo/waves/round-17/runs/$f/receipt.json | python3 -I -B -c 'import sys; b=sys.stdin.buffer.read(); old=b"/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; open(sys.argv[2],"wb").write(b.replace(old,sys.argv[1].encode())); print(b.count(old))' "$W" "$W/receipts/$f.json"
  python3 -I -B "$W/val/receipt-validate.py" "$W/receipts/$f.json" > "$W/out/$f.stdout" 2> "$W/out/$f.stderr"; echo exit=$?
  # then: sha256 of stdout with "$W" replaced by /tmp/r17-validate16.MWZBce, compared against summary.json stdout_sha256
done
```

4. Mutation for F3 (in the clone, origin removed; routed-defects exit 0):
```bash
export GIT_INDEX_FILE=$D/idx GIT_AUTHOR_NAME=audit GIT_AUTHOR_EMAIL=audit@localhost GIT_COMMITTER_NAME=audit GIT_COMMITTER_EMAIL=audit@localhost
git -C $C read-tree $REV && git -C $C ls-files '.ufo/waves/round-18/runs/*/pins/*' | grep -v '/runs/calib-aether/' | xargs git -C $C update-index --force-remove
M=$(git -C $C commit-tree $(git -C $C write-tree) -p $REV -m 'audit mutation')   # d7f9aa7…; 3 maps remain
python3 -I -B $D/routed-defects.py --root $C --rev $M   # open_count 0; R17-PINMAP open=False
```

## Residual risk and verification gaps

- **Not checked:** C1/C2/C3 measured values. They do not exist at REV (F2).
- **Push before run:** this rests on the local reflog of `refs/remotes/origin/main`, a client-side record. No server log was consulted.
- **Validator inputs were read live:** the VALIDATE16 reproduction read the carriers and Ghidra typeinfo as they are on the host at audit time. A later host update would change a rerun, not the retained evidence.
- **Scope of the corrections section:** the other three routed defects (SUMS-RUNLOG, REGISTRY, S032-DIGEST) cite no SCORECARD lines, so their absence from :2436-2440 is consistent. Grepping the r17 section for `SHA256SUMS|run-log|S032|SKILL|registry` matches only :2363 (an unrelated R16 registry token).
- **LSP not used:** the audited objects are REV blobs read with `git show`, not working-tree files. No finding relies on grep as semantic proof.
- **Installs:** none.
- **Lane writes:** this report only. Scratch `/tmp/scaudit.gegweO` was removed after the run.
