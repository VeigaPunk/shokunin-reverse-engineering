PARTIAL — R17-VALIDATE16's count correction and its evidence hold byte-for-byte. One clause in the correction is false. `routed-defects.py`'s closure is deserved on the facts but its checks do not earn it: the tool still closes the defect after the evidence is deleted, and its selftest is red at REV even though the lesson says "CLEAN 17".

# TruthVALIDATE16 — falsify R17-VALIDATE16 at `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`

Seat: `KaidokuR18.TruthVALIDATE16`, w2 falsify, author-side advisory. Every anchor is `git show REV:path` at REV = `b2aad08…`. The working tree equals REV for every tracked file: `git status --porcelain` shows only 9 untracked round-18 entries, and `git diff --quiet REV -- …/routed-defects.py` returns 0.

Axes: **calibration**: does each number and hash re-derive? **operability**: can an outsider reproduce the evidence and the closure? **depth**: does the closing instrument test substance, or tokens and self-report?

## Re-derivation of every number, hash and claim in the correction (observation)

| Claim (anchor) | Re-derived from | Result |
|---|---|---|
| r17 retained 8 validations (`SCORECARD.md:2439`, `LOG.md:2159`, `corpus/lessons/round-18.md:52`) | `9011581:.ufo/waves/round-17/verification.json`: commands whose label contains `receipt-validate` | 9 = 8 `receipt-validate-<label>` (all exit 0, all on lane `runs/<l>/receipt.json`) + 1 selftest; `grep -c da64646` = 0. **Holds** |
| The cited "all 16" sites exist (`SCORECARD.md:2364`; `corpus/lessons/round-17.md:88,122`) | `git show REV:` those lines | All three say "all 16"/"All 16". `round-17.md` is unchanged since `9011581`, and the r18 edits to SCORECARD/LOG/r17 entry are +66/−0 (append-only). **Holds** |
| `rev` = `da64646…`; 8 labels = the run dirs that carry receipts (`summary.json:80`) | `git ls-tree da64646 …/runs/` | 8 = 8. **Holds** |
| `validator_rev` `9011581`, `validator_sha256` `618448829ba6…126f` (`summary.json:81-82`) | `git show <rev>:…/receipt-validate.py \| sha256sum` | `618448…` at `9011581`, `d0ab299` and `b31975de`, so it is r17's final (verification-pass) validator. `da64646` = `53a5f096…`; `eb6c266`/REV = `70672eb3…`. `pins.py` = `9e9c7250…` at every rev. **Holds** |
| "16 occurrences per receipt" (`summary.json:76`) | Count of the lane prefix in each `da64646` receipt blob | 16 in each of 8 receipts, every one followed by `/`. **Holds** |
| 8 × `stdout_sha256`, `exit` 0, `checks_performed` 341, `findings` [] (`summary.json:1-66`) | sha256 of the committed `<label>.stdout` files, and an **independent rerun** (below) | Committed files match 8/8 and stderr is 0 bytes ×8. Rerun gives exit 0 ×8, 341 checks, 0 findings, and normalized stdout sha256 equal to the summary 8/8 (byte-identical). **Holds** |
| "(MD5-anchored binding)" at `:2364`, for pass 1 | Live carrier sha256 vs the recorded value, then the full-MD5 `Loading file://<sess>/target-<sha12>.bin?MD5=<md5>` line in the `da64646` `ghidra.log` blob (`receipt-validate.py@9011581:143-150,173-177`) | Carrier matches 8/8 and the MD5 line is present 8/8, so `md5_ok` is True, not the vacuous `None`. **Holds** |
| Validates under today's validator too | REV `receipt-validate.py` (`70672eb3…`) on the same remapped copies | exit 0 ×8, 341 checks. **Holds** (extra) |
| "an in-place replay is red 8/8" (`round-18.md:52`) | `9011581` validator on the unmodified `da64646` blobs against the live lane | exit 1 ×8. **Holds** |
| "…because pass 2 replaced the logs at the same paths" (`round-18.md:52`) | Recorded `ghidra.log` paths vs REV tree; finding codes | **False.** See F3 |
| "red at `9011581`" (`round-18.md:63`) | `routed-defects.py --rev 9011581…` | VALIDATE16 open; all 7 checks fail. **Holds** |

## Findings (by severity)

### F1 — MEDIUM: `routed-defects.py` closes R17-VALIDATE16 from summary.json's own claims; it never reads the retained evidence (observation)

`_d_validate16` (`.ufo/waves/round-18/tools/routed-defects.py:392-484`) works as follows:

- It counts exits from `summary.json`'s own `exit` fields (`:437-442`).
- It checks `validator_sha256` only for 64-hex form (`:458-462`), never against any blob.
- It requires the prose to contain `R17-VALIDATE16` plus `<k>/8` (`:471-483`).
- It never opens the `.stdout`/`.stderr` files, never compares `stdout_sha256`, and never checks `validator_rev` or `remap`.

The round-18 `verify.py` does not re-derive validate16 either: its `stdout_sha256` hits at `:125,143` cover its own command records only.

`round-18.md:8` ("each closed by … **and** a substance check") and `:63` ("substance check derives k/8 from the summary") therefore overstate what the instrument tests for this defect. Its "substance" is a consistency check between prose and a lane-authored summary, which is the C05-shaped self-witness risk flagged in w1 `ConnMistakeTaxonomy.md:243`.

Reproduction is a mkdtemp clone with origin removed. It prints `R17-VALIDATE16: False`, `open_count 0`, exit 0:

```bash
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; T=$(mktemp -d)
git clone -q --no-checkout --no-hardlinks $LANE $T/c && git -C $T/c remote remove origin && git -C $T/c checkout -q --detach $REV
E=$T/c/.ufo/waves/round-18/evidence/validate16; rm $E/*.stdout $E/*.stderr
python3 -I -B -c "import json,sys;p=sys.argv[1];d=json.load(open(p));d['validator_sha256']='0'*64;json.dump(d,open(p,'w'))" $E/summary.json
git -C $T/c -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qam mutant
python3 -I -B $LANE/.ufo/waves/round-18/tools/routed-defects.py --root $T/c --rev $(git -C $T/c rev-parse HEAD) | python3 -I -B -c "import json,sys;d=json.load(sys.stdin);print({x['id']:x['open'] for x in d['defects']}, 'open_count', d['open_count'])"
```

A second mutant kept the files but rewrote all 8 stdouts as red runs (`exit 1`, `binding_mismatch`) with summary exits left at 0. It also stays closed (tool exit 0, 7/7 checks ok).

Fix: bind each receipt entry to its stdout file:

- the file exists and its sha256 equals `stdout_sha256`;
- the stdout's own `exit`/`counts.valid` equals the entry `exit`;
- `validator_sha256` equals the blob at `validator_rev`.

### F2 — MEDIUM: the closing tool's selftest is red at REV, yet the lesson claims "CLEAN 17" (observation; the gate consequence is inference)

- `python3 -I -B $LANE/.ufo/waves/round-18/tools/routed-defects.py --selftest` exits **1** with `SELFTEST: FAILED closed-fixture-cli … closed-fixture-inprocess … token-only-R17-VALIDATE16: rc=0 target=(True, False, True) extra_open=['R17-PINMAP'] …`.
- The same file at `eb6c266` (copied to /tmp) prints `SELFTEST: CLEAN cases=17` and exits 0.
- Cause: the L1 amendment between `eb6c266` and REV changed the PINMAP check to require `mid_map_sha256_mismatch` + `mid_map_compare_mismatch` (`:277-288`). The closed fixture still writes only `"mid_map_mismatch"` (`:914`, inside `_closed_files` `:868`).
- Effect on this defect: the VALIDATE16 red case still computes the right target state, but the case fails, so no clean selftest certifies the VALIDATE16 red case at REV.
- Claims now false at REV:
  - `corpus/lessons/round-18.md:67`: "`routed-defects.py --selftest` CLEAN 17".
  - `:28`: "its selftest keeps token-only fixtures open". The targets do stay open, but the run fails.
  - This is the R17-VALIDATE16 pattern again: a pass claimed for a tool at a revision where the tool had changed.
- [INFERENCE, not run because it writes `verification.json` into the lane] The round-18 `verify.py` runs every `W18/tools/*.py --selftest` and expects exit 0 (`:157-159`). At REV it would therefore list `selftest-routed-defects` in `unexpected_exits` and return 1 (`:286,294-295`).

### F3 — LOW: the mechanism clause in the correction is false (observation)

`corpus/lessons/round-18.md:52` says the in-place replay is red "because pass 2 replaced the logs at the same paths".

- Pass 2 wrote logs into new session dirs (e.g. pro-op `rea-ghidra-yRmWqx` → `rea-ghidra-l3lSTD`).
- The pass-1 paths are **absent** at REV for 8/8 receipts.
- The in-place findings are `missing_file` ×4 + `binding_mismatch` ×1 per receipt. The only same-path replacement that registers is pro-aether's `sha256_mismatch` at `$.steps.analyze.stdout` (`analyze.json`, not a log).
- The cited source says "deleted" (`.ufo/waves/round-18/w1/RevValidatorPaths.md:39-40`), not "same paths".
- "red 8/8" is correct.

Reproduction (prints `ABSENT-at-REV` ×8):

```bash
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; cd $LANE; for l in calib-esbuild-0.25.12 calib-shfmt pro-aether pro-containerd-shim pro-esbuild-0.21.5 pro-esbuild-0.27.7 pro-notesmd-cli pro-op; do p=$(git show da64646:.ufo/waves/round-17/runs/$l/receipt.json | python3 -I -B -c "import json,sys;d=json.load(sys.stdin);print(d['retained_logs'][0]['files']['ghidra.log']['path'])"); r=${p#$LANE/}; git cat-file -e b2aad08ceeee8dd125ce0d316056d8bd766c7f94:$r 2>/dev/null && echo "$l present-at-REV" || echo "$l ABSENT-at-REV $r"; done
```

Suggested replacement wording: "…red 8/8 because pass 2 deleted the pass-1 session log dirs (`missing_file` ×4 + `binding_mismatch` per receipt; pro-aether also `analyze.json` replaced in place)".

### F4 — LOW: the evidence for a #18-captured defect falls short of QUALITY #18's argv/snippet clause (observation)

QUALITY #18 (`corpus/QUALITY.md:28`) requires execution evidence to retain "the producing argv/snippet … stdout/stderr and exit", and `round-18.md:63` names #18 as the criterion that captures this defect. The evidence falls short in three ways:

- **No argv or snippet.** `summary.json`'s keys are `receipts, remap, rev, validator_rev, validator_sha256` (per receipt: `checks_performed, exit, findings, kind, label, stdout_sha256`).
- **Rewrite snippet not retained.** The receipt prefix-rewrite is described, not kept (`Validate16Run.md:54`).
- **First red batch not retained.** The 8 exit-1 runs before `selection.py` was restored (`Validate16Run.md:56`) are claimed executions with no retained stdout or exit.

Operability effect, observed: a byte-identical `stdout_sha256` depends on the unrecorded layout `<prefix>/val/` + `<prefix>/receipts/<label>.json`.

- My first compact rerun used `rc/` and got exit 0 ×8 with 8 **different** hashes.
- With `val/` + `receipts/`, all 8 match. That layout can be inferred only from `pins_path`/`receipt` inside the stdouts.

The verdicts are unaffected.

## Is `routed-defects.py`'s closure deserved?

- **On the facts: yes.** Every number and hash re-derives, and the 8 runs reproduce byte-for-byte from git objects (`da64646` receipts, `9011581` validator, remap as recorded). The MD5 anchor is really exercised, and today's validator agrees.
- **As earned by the tool: no.** The VALIDATE16 checks would also close an evidence-free or contradicted state (F1), and the tool's own selftest fails at REV (F2).
- The defect is closed by evidence outside the tool, namely this rerun. The C1 "6 → 0 by named **and substance**" framing (`round-18.md:8`) overstates what the instrument shows for VALIDATE16.

## Residual risk and verification gaps

- The validator proves only that the bytes present now match (`receipt-validate.py@9011581:34-37`). Carriers and Ghidra typeinfo were re-read live on 2026-10-20; a carrier upgrade would turn this rerun red without any receipt being wrong.
- I did not run the round-18 `verify.py` (it writes into the lane), so F2's gate consequence is inference.
- QUALITY #21 (`:31`): the corrections say "validate 8/8 exit 0" without naming the recomputed fields. The pass-1 receipts carry 0 `pin_checks` per step (observed), so no verdict-only mid-run record was accepted. No finding.
- Fleet report `.ufo/reports/round-17/kaidoku.md:62,89` says 8/8 (grep only), consistent with w1 `ScoutValidate16Sites.md:52-53`. It is not a site.

## Commands and exit codes (all observed)

| # | Command (abridged; `LANE` = lane root) | Exit / result |
|---|---|---|
| 1 | `git -C LANE rev-parse HEAD`; `git status --porcelain` | 0; `b2aad08…`; 9 untracked round-18 entries, tracked clean |
| 2 | `python3 -I -B LANE/.ufo/waves/round-18/tools/routed-defects.py --root LANE --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | **0**; `open_count` 0; R17-VALIDATE16 7/7 checks ok |
| 3 | same with `--rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0; `open_count` 6; VALIDATE16 7/7 checks fail |
| 4 | sha256 of 8 `REV:…/validate16/<l>.stdout` vs summary; `wc -c` stderr | 0; 8/8 match; 0 bytes ×8 |
| 5 | `git show <rev>:…/receipt-validate.py \| sha256sum` (9011581, da64646, d0ab299, b31975de, eb6c266, REV) | 0; values in the table above |
| 6 | `git show 9011581:…/verification.json` census; `\| grep -c da64646` | 0 (9 = 8 + selftest); grep 1 (0 matches) |
| 7 | prefix count / fields per `da64646` receipt (python, read-only) | 0; 16 ×8; `pin_checks` 0; no `binding`/`md5_pre` |
| 8 | compact rerun: `git archive da64646 .ufo/waves/round-17`, `selection.py`, `9011581` validator + `pins.py` into `$W/val`, remapped receipts into `$W/receipts`, `python3 -I -B $W/val/receipt-validate.py $W/receipts/<l>.json` ×8 | **0 ×8**; normalized sha256 = summary 8/8 (first attempt with `rc/`: 0 ×8, hashes differ) |
| 9 | in-place replay (unmodified blobs), REV validator on remapped copies, MD5 predicate (scratch python) | 1 ×8 (`missing_file`4 + `binding_mismatch`; aether +`sha256_mismatch`); 0 ×8 (341); MD5 line 8/8 |
| 10 | F3 command | `ABSENT-at-REV` ×8 |
| 11 | F1 command (clone, `git remote` → none) | tool 0; VALIDATE16 closed; `open_count` 0. Mutant 2 (red stdouts): closed |
| 12 | `routed-defects.py --selftest` at REV / at eb6c266 (copy in /tmp) | **1** `SELFTEST: FAILED …` / 0 `SELFTEST: CLEAN cases=17` |
| 13 | `git diff --stat 9011581 REV -- SCORECARD.md LOG.md corpus/lessons/round-17.md corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` | 0; +66/−0, `round-17.md` untouched |

Lane hygiene:

- No lane file was edited except this report. No `jj`, and no git write in the lane.
- Clones and commits were made only in mkdtemp dirs whose origin was removed. No carrier was executed; carriers were read for hashing only.
- No REA or Ghidra.
- All `/tmp/truthv16*` scratch was removed after writing.

No tools were installed or updated.
