# ScoutValidate16Sites — R17-VALIDATE16 site census

Author: `KaidokuR18.ScoutValidate16Sites` (leaf, advisory). Baseline
`9011581d84527ba34c675f9cf912e54d2e72d470` (=B). Read-only: this file only; every
other path was read via `git show`/`git grep`/`git ls-tree`. No lane file edited, no
`jj`/git write, no REA/Ghidra/analyzeHeadless, no carrier execution. Temporary trees
were under `/tmp` and were removed. The validator replay below ran the round-17
read-only tool on temp-extracted JSON; it writes nothing (see §6).

Anchors are B line numbers. `git diff --stat 9011581d -- corpus SCORECARD.md LOG.md
SKILL.md PROVINCE.md README.md` is empty (exit 0), so worktree = B for every cited
durable file. Worktree does carry sibling work (`.ufo/waves/round-17/tools/compare.py`
modified, `.ufo/waves/round-18/` untracked) — not mine, and not cited here.

## Axes

- **calibration** — three unqualified "all 16" sites remain, and one of them
  (`corpus/lessons/round-17.md:88`) is **not named** in the routed item; the routed
  item also names the right file only by a path that does not exist. Six limiting or
  diagnostic sites are correct and must not be "corrected".
- **operability** — the spot-check's remedy ("retain the validator run over
  `git show da64646:…`") is not executable as written: the receipts record absolute
  lane paths that pass 2 overwrote. §4 gives a measured relocation harness and the
  exact summary shape the C1 executor needs.
- **depth** — the 8 first-pass receipts are **substantively valid** (8/8 exit 0 under
  relocation, 341 checks each) but **8/8 exit 1 in place**. The defect is
  retention/reproducibility, not run invalidity. This distinction changes the correct
  wording of all three sites.

## 1. Claim sites — classification

### 1.1 Overstated (3)

| # | anchor | phrase at B | why it is overstated |
|---|---|---|---|
| 1 | `SCORECARD.md:2364` | "all 16 receipts `receipt-validate.py` exit 0 (MD5-anchored binding)" | `verification.json` retains **8** validation runs, all on the second-pass (A) receipts; 0 commands reference `da64646` (§2). The 8 `da64646` receipts also exit **1 in place** today, because their cited log dirs and `analyze.json` were replaced by pass 2 (§3). |
| 2 | `corpus/lessons/round-17.md:122` | "All 16 receipts pass the final validator (verification pass)." | Same. "(verification pass)" asserts the pass measured 16; it measured 8. Pass 1 is only valid under a retrospective relocated replay (§3), which the sentence does not state. |
| 3 | `corpus/lessons/round-17.md:88` | "all 16 receipts were validated." (fix cell of the validator-shape row) | Same claim, **third site**, not listed at `corpus/lessons/round-17-verifier-spotcheck.md:137-147`. It also reads as if the pass-1 producer shape was validated at `da64646`, where `receipt-validate.py` rejected all 8 (this row's own evidence cell). |

Observation, not a defect: `round-17.md:88`'s own evidence cell says the `da64646`
validator rejected the 8 first-pass receipts with `unrecognized_shape`; "were validated"
is only true of the hardened validator applied retrospectively.

### 1.2 Correct (6 anchors)

| anchor | phrase | basis |
|---|---|---|
| `SCORECARD.md:2374` | "16 across two passes, 8 retained at HEAD, 8 at `da64646`; `receipt-validate.py` exit 0 ×8 in `verification.json`" | Exactly the retained state; the in-file precedent for the correction wording. |
| `LOG.md:2106` | "8/8 `receipt-validate` exit 0" | Matches the 8 A runs in `verification.json`. |
| `corpus/lessons/round-17-verifier-spotcheck.md:71` | "Only 8 of the 'all 16' receipt validations are retained." | Correct diagnosis. |
| `corpus/lessons/round-17-verifier-spotcheck.md:138` | R17-VALIDATE16 item | Correct on counts and evidence; **omits site 1.1#3** and cites `round-17.md:122` without a directory (the file is `corpus/lessons/round-17.md`; `.ufo/waves/round-17/round-17.md` does not exist). |
| `.ufo/reports/round-17/kaidoku.md:62` | "16 runs (8 × 2 passes), … 8/8 receipts valid" | Correct (8, limited to the second pass). Fleet report, outside the lane; no correction needed. |
| `.ufo/reports/round-17/kaidoku.md:89` | "all 8 receipts are valid and all 8 predictions reproduce" | Correct (8). |

`DraftLessonSkeleton.md` F6 (sibling, w1) independently reports the same 8
`receipt-validate-*` labels and 0 `da64646` references; F4 notes that the spot-check
cites `round-17.md:122` without a directory; F3 confirms the `:2364`/`:2374` anchors
exist at B. None of them measured the first-pass receipts (F6 confirms only that no
retained validator run covers them). Its F9 conclusion stands — the contract's check
(`contract.md:33-35`) admits the retain option — but see §4: retain needs relocation,
or the recorded exits are 1.

### 1.3 Unrelated (same quantity, different referent)

| anchor | phrase | class and measured status |
|---|---|---|
| `corpus/lessons/round-17-verifier-spotcheck.md:68` | "REA 6.5.0 and Ghidra 12.1.4 appear in 16/16 receipts" | Version appearance, not validation. Measured true: 8/8 receipts at `da64646` and 8/8 at B contain both strings. |
| `corpus/lessons/round-17-verifier-spotcheck.md:130`; `SCORECARD.md:2378-2379` | "all 16 reach `Analysis succeeded`" / "All 16 logs reach `REPORT: Analysis succeeded`" | Log content, not validation. Measured true: 8/8 `ghidra.log` at `da64646` and 8/8 at B contain the line (16 total). |
| `LOG.md:1656,1660,1682`; `SCORECARD.md:1946,1954,2006` | "`rule_blocks` 15 → 16, all 16 resolved" / "16/16" | Arc-3 craft-rule count, not receipts. |
| `corpus/knowledge/2026-10-13-r4u-04-dnfile-il.md:45` | "all 16 TypeDefs enumerated" | Managed-artifact inventory. |
| `.ufo/waves/**` (160 lines), `.ufo/reports/arc3-loop1-round10/kaidoku.md:24,45` (2 lines) | arc2/arc3/luna/round-14/16/17-wave text | Historical wave material for other properties/rounds; no r17 receipt-validation claim. `.ufo/waves/round-17/w1,w2` contain **no** "all 16 receipts" claim. |

Raw-regex census at B (`16 receipts|all 16|16/16`): **176 lines / 102 files** —
`.ufo/waves` 160, `corpus/lessons` 6, `SCORECARD.md` 4, `LOG.md` 3, `.ufo/reports` 2,
`corpus/knowledge` 1. The 14 durable (non-`.ufo`) raw hits are exactly
`LOG.md:1656,1660,1682`; `SCORECARD.md:1946,1954,2006,2364`;
`corpus/knowledge/2026-10-13-r4u-04-dnfile-il.md:45`;
`corpus/lessons/round-17-verifier-spotcheck.md:68,71,130,138`;
`corpus/lessons/round-17.md:88,122`. The two correct SCORECARD sites
(`:2374`, `:2378-2379`) are **not** raw hits (they say "16 across two passes" and
"All 16 logs") and were found by the validator-phrasing sweep; a regex-only search
would miss them.

## 2. Retained evidence — observation

`git show B:.ufo/waves/round-17/verification.json` → 79 commands; argv containing
`receipt-validate.py`:

```text
selftest-receipt-validate          exit 0  --selftest
receipt-validate-calib-shfmt       exit 0  runs/calib-shfmt/receipt.json
receipt-validate-calib-esbuild-0.25.12  exit 0  runs/calib-esbuild-0.25.12/receipt.json
receipt-validate-pro-notesmd-cli   exit 0
receipt-validate-pro-aether        exit 0
receipt-validate-pro-esbuild-0.21.5 exit 0
receipt-validate-pro-containerd-shim exit 0
receipt-validate-pro-esbuild-0.27.7 exit 0
receipt-validate-pro-op            exit 0
pins-snapshot-pre / -post          exit 0  NON-VALIDATION (tool path is a pinned file, not a subject)
```

So: **8 validation runs, all exit 0, all on the A tree; 1 selftest; 2 argv false
positives; 0 commands mention `da64646`.** Receipt census: 8 at `da64646`, 8 at B, all
8 path-pairs have different blob ids → **16 distinct blobs**.

## 3. Replay — what the other 8 actually do

Method: `git show <rev>:…/receipt.json` to `/tmp`, run
`python3 -I -B W17/tools/receipt-validate.py <file>` (no lane write; `-B` plus the
tool's own `sys.dont_write_bytecode` at `receipt-validate.py:49`).

| receipt set | in place (recorded absolute paths) | relocated to its own `da64646` bytes |
|---|---|---|
| 8 × `da64646` (first pass) | **8 exit 1**, 0 exit 0 | **8 exit 0**, 341 checks each |
| 8 × B (second pass) | **8 exit 0**, 344 checks each | n/a |

First-pass finding codes in place: `missing_file` (`retained_logs[0].files.ghidra.log`
and `.script.log`, both under `runs/<label>/logs/rea-ghidra-<pass1>/`), `binding_mismatch`,
and `sha256_mismatch` on `runs/<label>/analyze.json`.

Cause (observation): pass 1 and pass 2 reused the same labelled directories. At B only
the pass-2 session dir survives (aether: `rea-ghidra-J5bcRT`; the pass-1 receipt names
`rea-ghidra-JpGezV`), and `runs/<label>/analyze.json` holds pass-2 bytes. The receipts
store **absolute** lane paths (`retained_logs[*].files[*].path`), and the validator
reads exactly those paths (`receipt-validate.py:151-180`).

Relocation harness that measured 8/8 exit 0: materialise every file referenced by the
`da64646` receipt from `git show da64646:<rel path>` into a temp tree, then rewrite
**only** the path-valued fields (`retained_logs[*].files[*].path`,
`steps[*].retained_logs[*].files[*].path`, `steps[*].stdout_path`, `stderr_path`).
`session_dir`, `bound_sessions`, digests and all bytes stay unchanged, so the
line-anchored log-binding checks still match. The 341 vs 344 check difference is
expected: first-pass receipts carry no `pin_checks` (added in pass 2). The replay also
re-derived the full-MD5 loader binding from the first-pass log bytes (no
`binding_mismatch`), so `:2364`'s "(MD5-anchored binding)" parenthetical is not the
defect; the count is.

[INFERENCE] At production time the pass-1 receipts could not have been validated by the
final validator: at `da64646` the validator rejected the producer shape
(`round-17.md:88`). "Validated" for pass 1 can only mean the hardened validator applied
retrospectively to the `da64646` bytes — which is exactly the relocated replay.

## 4. Consequence for the C1 discharge (operability)

`contract.md:33-35` requires `.ufo/waves/round-18/evidence/validate16/summary.json`
with `rev = da64646…` and exactly 8 `exit` ints. It does **not** require 0, so:

- An **in-place** harness records 8 × `exit: 1` and closes the check, but the numbers
  then read as "invalid receipts"; they are path-retention failures, not run failures.
- A **relocated** harness records 8 × `exit: 0` (341 checks) and can carry
  `harness: "relocated"` per receipt. This is the evidence that supports the claim.
- Recommendation: relocated harness, harness name recorded per receipt, temp copies only
  (`claims.json` non-goals forbid editing round-17 retained receipts/logs).

Append-only named corrections (r16 precedent: `corpus/lessons/round-17.md:94-99`), one
line per site, plus the `R17-VALIDATE16` line the contract requires in `SCORECARD.md`
and `LOG.md`:

```text
R17-VALIDATE16: `SCORECARD.md:2364` "all 16 receipts exit 0" overstates the retained
evidence — `verification.json` retains 8 `receipt-validate-*` runs, all on the
second-pass receipts (exit 0 ×8, 344 checks each). The 8 `da64646` receipts are valid
when replayed against the `da64646` bytes with their recorded paths relocated (8/8
exit 0, 341 checks each); in place they exit 1 because pass 2 overwrote their cited
log dirs and `analyze.json`. Same unqualified claim at `corpus/lessons/round-17.md:122`
and `:88`.
```

Suggested in-place rewordings:

- `:2364`: "8/8 second-pass receipts `receipt-validate.py` exit 0 in `verification.json`
  (344 checks each); the 8 first-pass (`da64646`) receipts exit 1 in place because pass 2
  overwrote their cited artifacts, and 8/8 exit 0 when replayed against the `da64646`
  bytes with path relocation (341 checks each)."
- `round-17.md:122`: "8/8 second-pass receipts pass the final validator (verification
  pass); the 8 first-pass receipts pass only under a path-relocated replay against the
  `da64646` bytes."
- `round-17.md:88`: "all 16 receipts validate under the hardened validator (8 in place,
  8 relocated); the retained verification run covers the 8 second-pass receipts."

No correction is needed in `.ufo/reports/round-17/kaidoku.md` for this defect: its two
sites say 8/8. Unlike R16-PROVENANCE, the fleet report is not a site here.

## 5. Checked and clean (not sites)

- `corpus/lessons/round-17.md:30` — "Two passes, each with 8 receipts": accurate count;
  the model for the corrected wording.
- `corpus/lessons/round-17.md:22` — "capability row is entered only after the receipts
  validate": policy, no count.
- `SKILL.md:541` — `receipt-validate` registry row: describes the tool, no 16-claim.
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3,194` — recheck command and
  "All 16 retained logs"; the latter is the log property verified in §1.3.
- `SCORECARD.md:2374`'s pin-map clause ("pre/mid/post pin maps") is separately routed as
  R17-PINMAP; its validation clause is correct and should not be touched by the
  VALIDATE16 correction.

## 6. Remaining unknowns / hazards

- **Decision, not unknown:** in-place (8 × exit 1, contract-admissible) vs relocated
  (8 × exit 0, stronger). §4 recommends relocated.
- **Gate hazard (observation):** `.ufo/waves/round-17/tools/__pycache__/pins.cpython-314.pyc`
  exists (mtime 2026-10-20 15:27:16Z; `compare.py` modified 15:27:21Z — sibling activity).
  Not mine: `receipt-validate.py:49` sets `sys.dont_write_bytecode` before importing
  `pins`, and a controlled re-run left the pyc mtime unchanged. The round-17 lesson row
  says `verify.py` fails on any `__pycache__` under `.ufo`; sweep it before the round-18
  gate.
- [INFERENCE] The relocation harness is insensitive to `session.json` absence because the
  binding is read from `ghidra.log` lines; a future validator change could break this.

## 7. Commands exercised (argv → exit)

```text
git -C LANE grep -n -I -E '16 receipts|all 16|16/16' B --                                  -> 176 lines/102 files, 0
git -C LANE grep -n -I -E 'receipt-validate|receipts?[^.]{0,40}(valid|pass|exit 0)…' B --   -> sites listed, 0
git -C LANE grep -n -I -i -E '(all|every|each|both)[ -]?(16|sixteen)[ -]?receipts?…' B -- '*.md' -> 6 claim/diagnosis lines, 0
git -C LANE grep … ':!.ufo'                                                               -> 14 durable lines, 0
git show B:.ufo/waves/round-17/verification.json | python3 -c '<census>'                   -> 79 commands; 8 validations; 0
git ls-tree -r --name-only <rev> -- .ufo/waves/round-17/runs | grep receipt.json$          -> 8 each rev, 0
git rev-parse <rev>:<receipt> pair loop                                                    -> 8/8 DIFF (16 blobs), 0
git show <rev>:<receipt> | grep -q '6\.5\.0'  (and '12\.1\.4'), loop                  -> 8/8 and 8/8, 0
git show <rev>:<log> | grep -q 'REPORT: Analysis succeeded' loop                   -> 8/8 and 8/8, 0
python3 -I -B W17/tools/receipt-validate.py <temp receipt> × 16 (in place)                 -> 8×0 (A), 8×1 (da64646)
python3 -I -B W17/tools/receipt-validate.py <temp receipt> × 8 (relocated)                 -> 8×0, 341 checks each
grep -rn 'VALIDATE16' .ufo/waves/round-18/w1/                                              -> skeleton F3/F4/F6/F9, 0
git diff --stat 9011581d -- corpus SCORECARD.md LOG.md SKILL.md PROVINCE.md README.md      -> empty, 0
stat .ufo/waves/round-17/tools/__pycache__/pins.cpython-314.pyc                            -> 15:27:16Z, 0
```

Bash wrappers that printed `EXIT:0` for the greps above: all exit 0 (hits found, not
"no match"). The `QUALITY.md` grep returned exit 1 (no `receipt-validate`/`all 16`
match) — recorded as no site, not as a failure.

## 8. Tools / installs

None installed or updated. Nothing was run from REA, Ghidra, or a carrier binary; no
`jj` command and no git write. Only the round-17 read-only validator was executed
against temp copies, as disclosed in §3.
