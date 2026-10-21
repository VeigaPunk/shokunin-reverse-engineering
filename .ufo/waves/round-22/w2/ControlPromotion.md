# ControlPromotion — SHONEN marks, no-harm scope, and reviewer boundary

- **Seat:** `KaidokuR22R.ControlPromotion-6` (leaf; author-side review, not outside admission)
- **Scope:** round-22 no-harm control declarations, four canonical SHONEN boxes, and the distinction between lane-authored W2 evidence and an outside verifier.
- **Baseline B:** `7787fea4d6fd718726de92ed20759d11ce7b8b48`
- **Candidate observed:** `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`; working tree was changing and contained uncommitted edits. No final revision existed at observation. This report makes no final-after claim.

## Findings (by severity)

### P2 — C1's frozen separability statement omits a counter input

`.ufo/waves/round-22/claims.json:36` says C1 reads only `corpus/knowledge` and `evidence/c1`. The counter also reads `corpus/SOURCES.md` to establish that each cited S051+ row is mined, opened on the required date, and lists the knowledge path in `used-by` (`tools/count-c1.py:43-48`; source-row eligibility is applied at `:57-60`). `verify.py:85-87` correctly includes `corpus/SOURCES.md` in the C1-only sandbox. Thus the actual causal-separation control accounts for the registry, but the frozen claim's prose is not a complete read-set declaration. L1 should describe C1's source registry dependency wherever the claim is summarized and retain `SOURCES.md` in the C1-only final-revision check; do not report the narrower sentence as the actual counter boundary.

### P2 — The red-control result is exit-only and can pass with a broken positive control

`tools/verify.py:32-40` sets each recorded `pass` from the expected process exit unless a separate validator is supplied. The red-fixture calls at `:61-62` expect exit 1 but supply no validator for the `counter-fixtures.py` JSON. A fixture-suite exit 1 can mean the intended old-counter false accept was reproduced, or instead that a positive control failed; the summary treats both as a passing red check.

The exact shell command used for this bounded fixture probe was:

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-22/tools/counter-fixtures.py --claim C1 --counter .ufo/waves/round-22/frozen/count-c1.py --root "$PWD" 2>/dev/null | python3 -c "import json,sys;d=json.load(sys.stdin);print([(c['id'],c['exit'],c['count'],c['pass']) for c in d['cases']])"; echo "EXIT_RED_FROZEN_C1=$?"
```

The extracted stdout case list at that snapshot was:

```text
[('all_six', 1, 0, False), ('missing_source', 1, 0, True), ('refusal', 1, 0, True), ('split_record', 1, 0, True), ('uncited_path', 1, 0, True), ('duplicate_json', 1, 0, True), ('wrong_command', 1, 0, True), ('extraction_only', 1, 4, False), ('refused_with_extraction', 1, 4, False), ('forged_debug_operation', 1, 0, False), ('helper_drift', 1, None, False)]
```

`EXIT_RED_FROZEN_C1=0` is the final JSON-printing pipeline process's exit, not a captured exit from `counter-fixtures.py`; its raw stderr was redirected to `/dev/null`. The suite semantics in `counter-fixtures.py:160-161` return 1 if any case fails. Thus the observations show the frozen counter rejected the positive `all_six` control, and the frozen counter's expected exit-1 red invocation could pass `verify.py` without demonstrating the intended false accept.

The fixture file continued changing after this observation, so this is not a final-suite verdict. The code-level oracle gap remains: at a candidate revision that contains the newer fixtures, a nonzero red run alone does not prove the intended negative was accepted with its positive controls intact. L1 should make the red check validate case IDs, expected per-case outcomes, and at least the positive-control case, or otherwise preserve a compatible frozen-fixture input. Re-run on the final revision.



## SHONEN and outside-review distinction

No SHONEN marking defect was found at the observed candidate. `SHONEN.md` contains the same four canonical boxes and each is `[~]`, with author assertions/pointers and no named promotion verifier. `git diff --exit-code B HEAD -- SHONEN.md` exited 0; `git status --porcelain -- SHONEN.md` printed nothing. This is the appropriate mark state: the W2 dispatches and their reviewer/critic reports are author-side work for this recovery evidence wave, not an outside non-author admission. `corpus/lessons/round-22.md` explicitly says every dispatched seat is author-side and independent non-author admit/reject sampling remains closure's duty. Do not convert W2 participation, W2 report authorship, or an L1 verification pass into `[x]` or an admission claim.

## Commands and observed results

All commands below are read-only measurements at the stated candidate/worktree snapshot, except the fixture command's own temporary Git fixtures. No lane source was edited by this seat.

| Command | Observed result |
|---|---|
| `git rev-parse HEAD` | `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` |
| `git diff --exit-code 7787fea4d6fd718726de92ed20759d11ce7b8b48 HEAD -- SHONEN.md` | exit 0; empty diff |
| `git status --porcelain -- SHONEN.md` | exit 0; empty output |
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD` | exit 1; JSON reports `t1_exercised=["identify-flutter-build"]`, count `1/6` (not a full-counter pass; consistent with the frozen R22 improvement predicate `k>=1`) |
| `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root "$PWD" --rev HEAD | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps({'accounted':d['accounted_count'],'mismatched':d['mismatched'],'foreign':d['foreign_rows'],'statuses':{k:v['status'] for k,v in d['per_verb'].items()}},indent=1))"; echo "EXIT_C2_HEAD=$?"` | parsed stdout: `accounted_count=14`, `mismatched=[]`, `foreign_rows=[]`; exit 0 is the JSON parser pipeline process, not a separately captured counter exit |
| `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-21/battery.py --root "$PWD" --rev HEAD --claim C1 >/tmp/r21c1.json 2>/tmp/r21c1.err; echo "EXIT_R21_C1=$?"` | exit 0; `/tmp/r21c1.json` reports `finding=battery_clean`, 12/12 controls passed, `false_clean=0`, `violations=0`; stderr file empty |
| `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-21/battery.py --root "$PWD" --rev HEAD --claim C2 --regression >/tmp/r21c2.json 2>/tmp/r21c2.err; echo "EXIT_R21_C2=$?"` | exit 0; `/tmp/r21c2.json` reports `finding=battery_clean`, 20/20 controls passed, `false_clean=0`, `violations=0`, 18 regression receipts; stderr file empty |
| `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-21/controls.py --root "$PWD" --before 7787fea4d6fd718726de92ed20759d11ce7b8b48 --after HEAD >/tmp/r21ctrl.json 2>/tmp/r21ctrl.err; echo "EXIT_R21_CTRL=$?"` | exit 0; `/tmp/r21ctrl.json`: `finding=controls_clean`, LOG/SCORECARD append-only prefixes true, prior files changed `[]` (1135 checked), prior QUALITY rows identical; stderr file empty |
| `cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku; echo "EXIT_CENSUS=$?"` | exit 0; disclosed W04 duplicate-URL warnings for S033, S047, and S054; final output `kaidoku ok .../corpus/SOURCES.md` |


The no-harm controls and append-only review results are point-in-time evidence only. Round-21 controls pass at `HEAD`; final state must still be tested at the actual final revision. The sources census's exit 0 is not a warning-free result; preserve/disclose the W04 rows rather than suppressing them.

## Invariants for L1 verification at final revision R

1. **SHONEN authority:** all four canonical checklist rows remain `[~]` unless a named non-author verifier actually performs the required checks; author-side W2 reports never qualify. Do not claim promotion/admission from this review.
2. **Prior corpus:** every path present under `corpus/` at B that is covered by the frozen no-harm declaration remains byte-identical at R; no deletion/rename. In particular, all pre-round-22 `corpus/knowledge/` files remain unchanged and only authorized new knowledge entries are additions.
3. **Append-only history:** B's `LOG.md` and `SCORECARD.md` bytes remain exact prefixes at R; earlier QUALITY rows and prior SOURCES rows remain byte-identical and in order. A membership-only check is insufficient to establish ordering.
4. **C1 read set and separability:** include `corpus/SOURCES.md`, `corpus/knowledge`, and `evidence/c1` in the C1-only measurement sandbox. The claim's source-row eligibility is part of C1, not an incidental file. Confirm C2-only changes do not move C1 and vice versa.
5. **No-harm gates:** run round-21 controls and both round-21 batteries against R; expected exits are 0. Run the sources census against the final file; require exit 0 while explicitly recording any W04 warnings and rejecting any error findings.
6. **Round-22 measurements:** report the exact final `count-c1.py` result and exit, without upgrading `k/6` to `6/6`; C2 requires 14/14, no mismatches, and no foreign rows. Verify fixture positive and negative outcomes individually, not only the aggregate exit code.
7. **Revision identity:** pin all measurements to R and ensure the counter/fixture/verify source bytes being tested are the bytes at R. Do not use the current working tree or HEAD as a substitute for a final revision.

## Residual risk and verification gaps

- Candidate is not final; the lane worktree was dirty and actively changing during the observation. All measurements above need a final-revision rerun.
- The `claims.json:36` read-set wording and the exit-only red-check oracle need L1 attention as described above.
- No `lsp` device/route was exposed in this session, so no LSP status, references, definition, or diagnostics result is claimed; no grep output is used as semantic proof.
- No outside verifier/admit-reject sample was observed. Bounded probes/selftests run: the C1/C2 counters, C1 fixture probe, round-21 batteries/controls, and sources census listed above. No build, lint, formatter, full round-22 `verify.py`, or install/update was run by this seat.
