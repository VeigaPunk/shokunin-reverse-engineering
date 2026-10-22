# CustodyFacts: attack on routed defect 1 (round-25 verifier spotcheck)

Seat: KaidokuR26.CustodyFacts (wave 1, leaf, no dispatch). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Lane HEAD and main: c27f445e70cedbaf5300b2fd0a53e821d9b659a9 (lane HEAD detached). Every lane fact below comes from HEAD bytes or read-only Git (`show`, `log`, `ls-tree`, `rev-parse`, `grep`, `merge-base`, `branch --contains`, `diff`). Access date for every source: 2026-10-22. Times are UTC from the run log. No web sources, no REA calls, no installs or upgrades (python3 3.14.8 was already present). The only lane write is this file.

Lane note: other seats changed the working tree while I ran. At 12:25:52Z `git status` showed modified corpus/README.md and corpus/SOURCES.md plus new round-26 untracked files. I did not touch them, and no hash or quote below depends on them.

## 1. Verdicts

| # | Premise | Verdict |
|---|---|---|
| P1 | Commit fafdd283 landed tools/round-25/instrument-custody.py | holds |
| P2 | The attempt-1 claim was abandoned | holds as "not continued"; fails as a recorded abandonment decision |
| P3 | The SKILL.md section says the candidate "is not implemented at this phase" | holds; stale at tip |
| P4 | The registry row round25-custody-ruler says the same | fails |
| P5 | The tool runs in a sandbox, with exit and excerpt | holds; no selftest exists |
| P6 | Main authorized the implementation (needed for "landed" to be legitimate) | could not evaluate from the lane |

## 2. P1: landing at fafdd283

- Observation. `git show --stat fafdd283` exit 0, 12:25:52Z (raw/l01): one file, "tools/round-25/instrument-custody.py | 514 +++", "1 file changed, 514 insertions(+)". Author kaidoku-shokunin, Date Wed Oct 21 23:42:27 2026 -0300.
- Observation. `git merge-base --is-ancestor fafdd283 HEAD` exit 0 (raw/l02). `git branch --contains fafdd283` lists main (raw/l06). So fafdd283 is on main.
- Observation. The blob at fafdd283, at HEAD, and in the sandbox is 8a6e21f18e805c7ce44e03a9a4872e9063073c32, mode 100755 (raw/l04 for the blobs; the mode came from an earlier `git ls-tree HEAD -- <path>` call not saved to raw/). `git log fafdd283..HEAD -- tools/round-25/instrument-custody.py` lists 0 commits (12:23:00Z), so nothing on main changed the file after landing.
- Observation. SHA-256 of the file bytes: 54c43cdc01930fcb58f14053d8099f4b28352147656a05d811574cc74e7d34fb. Lane HEAD bytes and sandbox bytes agree.
- Observation. Parent of fafdd283 is a4ab912a (`git rev-list --parents`). a4ab912a is the only commit that touches the attempt-1 claims file (`git log -- .ufo/waves/round-25/claims.json`, 12:23:00Z), and it parents 62feef9c. So the instrument arrived after the freeze, and the claims file was not edited afterwards.
- Observation. Gate corroboration: corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json line 1 lists INSTRUMENT_ABSENT for the path and INSTRUMENT_REVISED at commit fafdd283, "disclosed": 0.
- Qualification. Commit e164f2e8 is not on main. It has the same blob and parent a4ab912a, with an empty subject. `git merge-base --is-ancestor e164f2e8 HEAD` exit 1 (raw/l03). Its only ref is refs/jj/keep/e164f2e8587997dbc701d7f2dfbc84a2bd70a167 (raw/l05). `git diff --shortstat fafdd283 e164f2e8` gives "83 files changed, 958 deletions(-)" (12:25:19Z), and the same diff with `--diff-filter=AMRCT` lists nothing. So e164f2e8 differs from fafdd283 only by deleting 83 residue files. The landed commit is fafdd283. Why jj keeps e164f2e8: INFERENCE (a rewritten or dropped copy); no lane record says.
- UNKNOWN: Main's permission. claims.json line 182: "No implementation before actual Main-pushed SRT callback." Lane records disclaim code permission: LOG.md:2950 "No source/gate/fixture/candidate execution, F or code permission is claimed."; corpus/lessons/round-25.md:355 "There is still no F, candidate/code/runtime permission or admission."; SCORECARD.md:3043 "No after score, capability admission, F or implementation permission is claimed at this handoff." Searches of LOG, SCORECARD and the round-25 lessons for callback, permission and approval found no later record. Attempt 2 says lane_tip_at_start is fafdd283 (a2/claims.json:6), so attempt 2 started from the landed tip.

## 3. P2: "abandoned"

Records that describe the status:
- a2/claims.json:12 (first added at 7ef837a4, 2026-10-22 05:21:47 -0300): "Attempt 2 does not continue its preregistration packet and makes no claim on its 34-case contract." The same line says the attempt-1 custody CLI "stay[s] byte-unchanged", which §2 confirms.
- SCORECARD.md:3050: attempt 1's claim "was not continued and has no after value."
- corpus/lessons/round-25.md:359-363: "was not continued: it has no after value in this round and is reported as not pursued, not as met."
- corpus/lessons/round-25-verifier-spotcheck.md:58-63 quotes "not pursued, not as met" and says "after the driver superseded attempt 1".
- Watchdog digest, verifier lesson line 29: "superseded at 2026-10-22T04:56:36-03:00: stale 2026-10-21/22 author". This is a run-level supersession for a stale author, not a claim decision.
- corpus/claim-freezes.tsv:13: FLAGGED only, no status word.
- LOG.md: no line records the non-continuation. `git grep -i -E "not continue|not pursued|makes no claim|no after value"` hits SCORECARD, the round-25 lessons, the a2 claims file and wave specs, and no LOG line (`git grep` at 12:23:00Z; not saved to raw/).
- The word "abandon" appears in round-25 records only in the routed defect itself (corpus/lessons/round-25-verifier-spotcheck.md:185-186).

Records against retirement:
- SCORECARD.md:2957-2958, the earlier handoff, is not changed in text: "All original34 targets and full no-harm duties remain; a failed/unprovable target is not converted to a narrower or exploratory claim."
- a3/w2-spec.json:135 asks whether not measuring attempt 1's 34-case target is "a narrowed target after landing, an honest stop, or neither". LOG.md:2960 says wave 2 "was not dispatched". No adjudication exists.

Verdict: "not continued" is the lane's own word and matches the records. "Abandoned" implies a retirement decision that no record contains. Any note should use the lane's words.

## 4. P3 and P4: SKILL.md

- P3 holds. SKILL.md:787-788 (sha256 cf047307dbab77369ffe31de3f7f4eeab797293c085253eba28d6978a735ad42): "The candidate `tools/round-25/instrument-custody.py` is not implemented at this phase; missing candidate is unavailable2 and cases are not observed." The file exists at tip, so the sentence is stale. "unavailable2" is a run-together token that the verifier lesson names at line 57.
- P4 fails. The row at SKILL.md:807 names tools/round-25/ruler.py and its exit legends, and nothing about a candidate. `git grep -n -i -E "candidate|implement" HEAD -- SKILL.md` (raw/l14 and raw/l15 at 12:25:52Z; the 780-812 filter run at 12:23:51Z) returns only lines 783, 786, 787 and 788. Line 807 contains neither word, so the row needs no edit for this sentence.
- Tense check: SKILL.md:798-803 ("The exact prospective claims path…"; "Only actual Main first-add F can establish discovery of a twelfth freeze.") still reads prospective. The ledger row already exists (claim-freezes.tsv:13), so the same note can cover these lines.

## 5. P5: the tool in the sandbox

Setup: `git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r26/seats/CustodyFacts/clone` at 12:19:57Z. Clone HEAD c27f445e, status empty. Runs were made in the clone as `python3 -I -B tools/round-25/instrument-custody.py …`. Clone status including ignored files after all runs: 0 lines, so the tool wrote nothing.

| run | UTC | exit | exact excerpt |
|---|---|---|---|
| s01 `--help` | 12:25:52Z | 0 | `usage: instrument-custody.py [-h] --root ROOT --request-json REQUEST_JSON` |
| s02 no arguments | 12:25:52Z | 2 | `{"error": "invalid_invocation", "finding": "request_invalid", …}` |
| s03 freeze a4ab912a, reference the instrument, sha256 54c43cdc… | 12:25:52Z | 1 | `"error": "instrument_absent_at_freeze", "finding": "instrument_absent", "resolved_first_add": "a4ab912a…"` |
| s04 same, freeze fafdd283 | 12:25:52Z | 2 | `"error": "freeze_is_not_claims_first_add", "finding": "freeze_mismatch"` |
| s05 control: tools/round-25/ruler.py, freeze a4ab912a, sha256 20fe3f3d… | 12:25:52Z | 0 | `"finding": "clean", …, "revision_commits": []` |
| s06 ruler with a pin of 64 zeros | 12:25:52Z | 1 | `"error": "frozen_digest_mismatch", "finding": "pin_mismatch"` |
| s07 measured commit of 40 ones | 12:25:52Z | 2 | `"error": "measured_commit_absent", "finding": "measured_commit_unavailable"` |

- The exit codes match the decision order in the tool docstring (lines 17-31) and EXIT_CODES (lines 49-67).
- Selftest: none. `git grep -n -i -E "selftest|self-test|argparse|sys\.argv|__main__" HEAD -- tools/round-25/instrument-custody.py` (raw/l17) gives argparse at lines 38 and 482 and the __main__ guard at line 513. main() is at 481. `git ls-tree -r --name-only HEAD -- tools/round-25` (raw/l18) lists no test file for it.
- Not run: the 34-case ruler. Not evaluated: whether the tool matches its 34 cases.

## 6. Adjacent observations (outside P1 to P6)

- Residue: 83 tracked files under .ufo/waves/round-18/verify/scratch-custody/custody-pair-selftest-24ggjm_a/ (raw/l10). First added at 454dee69 on 2026-10-20 14:17:35 -0300 (raw/l09), before this tool existed. The name suggests a round-18 custody-pair selftest, which is INFERENCE and unverified. None of it is this tool's output.
- The verifier lesson's conformance defect 2 (Landed changes table omits fafdd283) is the same landing record. Not in this seat's scope.

## 7. Advice for the routed fix (advisory; L1 decides)

1. Append a dated superseding note after SKILL.md line 788. Leave corpus/lessons/round-25.md lines 29-30 unchanged, because that is the attempt-1 record. The note should say: the candidate was committed at fafdd283 (on main; blob 8a6e21f1…; sha256 54c43cdc…); the attempt-1 claim in .ufo/waves/round-25/claims.json (first added at a4ab912a, never edited again) was not continued and has no after value; the non-measurement is not adjudicated (wave 2 not dispatched; SCORECARD.md:2957-2958 keeps the 34 targets).
2. Do not write "abandoned" unless Main records that decision.
3. Do not edit the SKILL.md registry row at line 807 for this defect.
4. Cite fafdd283, not e164f2e8, as the landed commit.
5. Replace the run-together token "unavailable2" in the same sentence.
6. State that Main's permission for the implementation is not recorded in the lane.

## 8. Sources opened (access 2026-10-22; sha256 of HEAD bytes; one located quote each)

1. SKILL.md, cf047307…: L787-788 "is not implemented at this phase"
2. SCORECARD.md, cfe8b525…: L3050 "was not continued and has no after value"; L2957-2958 "All original34 targets and full no-harm duties remain"; L2979-2980 "implementation remains stopped"; L3043 "F or implementation permission is claimed"
3. LOG.md, 60dc8c45…: L2960 "was not dispatched: Main froze scope at 11:20Z"; L2950 "No source/gate/fixture/candidate execution, F or code permission is claimed"
4. corpus/lessons/round-25.md, cef06cbc…: L355 "There is still no F, candidate/code/runtime permission or admission"; L359-363 "was not continued: it has no after value in this round"
5. corpus/lessons/round-25-verifier-spotcheck.md, 3d6bc116…: L29 "superseded at 2026-10-22T04:56:36-03:00: stale 2026-10-21/22 author"; L63 "not pursued, not as met"; L185 "and the claim was abandoned"
6. corpus/claim-freezes.tsv, 7e4fdaff…: L13 "added fafdd283, by that design"
7. tools/round-25/instrument-custody.py, 54c43cdc…: L1-2 "Explicit caller-selected Git instrument-reference custody checker (round 25)."
8. tools/round-25/ruler.py, 20fe3f3d…: L2 "Prospective R25 instrument-custody CLI ruler; never imports candidate helpers."
9. .ufo/waves/round-25/claims.json, 6d660c50…: L182 "No implementation before actual Main-pushed SRT callback."
10. .ufo/waves/round-25/a2/claims.json, d40bf0ba…: L6 "lane_tip_at_start": fafdd283; L12 "Attempt 2 does not continue its preregistration packet"
11. .ufo/waves/round-25/a3/w2-spec.json, 2316c239…: L135 "a narrowed target after landing, an honest stop, or neither"
12. corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json, 08634613…: L1 "finding": "INSTRUMENT_REVISED" at commit fafdd283, "disclosed": 0
13. .ufo/waves/round-26/claims.json, 1137c312…: L4 "before any table REA run and before any repair edit" (context only; no verdict depends on it)

## 9. Artifacts under /fast/scratch/hyaku/kaidoku-r26/seats/CustodyFacts/

- custody-evidence-pass.py, sha256 186662036fcf758aa2d13b1173f1812b0dac5d46c4873a930ffe701e9762f4a0 (the script that produced raw/).
- MANIFEST.sha256, sha256 08e7e43c0fe57a136112d528731cd2d7d4e9420d21881df108ad45a09d2c9fe7, lists 58 entries with a sha256 each: the script plus the 57 files in raw/ (.out and .exit pairs and summary.json).
- raw/summary.json, sha256 7d9faf5ac7cbc1acefe6930cd567b8004d4141becdae13d7e419bb219be0544e.
- Key raw hashes: s01 819d3ac7…, s02 35820084…, s03 da3be3dc…, s04 b45d68c3…, s05 45db954e…, s06 9ca6646…, s07 c9beee3c….
- clone/ is a directory at HEAD c27f445e and is not hashed.
- raw/l19-lane-status.out depends on lane state. Its hash comes from the final run only.

## 10. Residual risk and gaps

- Main's permission for the implementation commit is unknown from the lane.
- The 34-case ruler was not run, and the tool was not checked against its cases.
- No external sources were opened and no REA calls were made.
- Other seats changed the lane working tree during my run (see the lane note above). I changed nothing.
- Installed or upgraded: nothing.
