PARTIAL — several rows have a real, retained defect signal, but not every “shown able to fail” statement is demonstrated, and W1 contains omitted round-20 errors.

Axes: calibration (whether the counters can actually fail), coverage (all five C2 targets and D1 state), depth (causal/model defects and the exact red-before).

## Row-by-row evidence

[OBS] Measured source S was read from Git, not the worktree: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/lessons/round-20.md` — exit 0. The rows are at `corpus/lessons/round-20.md:100-108`.

- **1 (D1):** the residue red-before is real, but it is a postcondition, not a failing selftest: baseline `custody-pair.py selftest` exited 0 and left 136 files / two nested `.git` trees (`w1/ScoutLaneScratchWriters.md:42-49`; `w1/CustodySelftestFix.md:15-21`). `w1/RoutedR19Tool.md:49-51` records the baseline counter command without `--strict`, exit 0, `open_count=11`; it does not retain the claimed strict-red exit. The row should name the residue-sweep as its red artifact; don’t call the counter’s strict result observed without its actual output.
- **2 (D2):** supported as a detected finding: `w1/EvidenceTimestampLint.md:9-11` gives `future_dated claims.json:36` and `claims.json:35`, and the independent oracle lists both timestamp/introducing-commit pairs (`w1/ScoutTimestampOracle.md:13-22`). Qualification: the linter commands recorded after repair omit `--strict` and exit 0 (`w1/EvidenceTimestampLint.md:35-37`); the lesson’s claimed strict exit 1 is not in that report.
- **3:** accurately says “no demonstrated fix” (`:102`); do not count the working systemd-run selftest as a fix for the false bwrap premise.
- **4 — red-before only asserted for the claimed forged-ID defect:** the new source case is `forged_id_not_in_retained_bytes` (`.ufo/waves/round-20/tools/verb-coverage.py:274-303`), but the W1 retained failure is `SELFTEST: FAILED not_mentioned_is_zero,substring_trap_rejected,evidence_id_and_existing_path_exercise cases=7 fails=3`, followed by `SELFTEST: CLEAN cases=7` (`w1/VerbCoverageTool.md:44-48`). The failed case is a *positive* valid-ID/path assertion, not `forged_id_not_in_retained_bytes`; no retained output shows that the forged-ID case went red before the predicate fix. So the lesson’s quoted failure text is misattributed to the new anti-forgery check.
- **5-7:** W1 retains the comparator’s envelope error (`w1/SimplifyC3Pipeline.md:228-232`), row 6 states the exact missing-`first_failure.h1` failure and retained reruns (`:105`), and row 7 gives `git apply: corrupt patch at line 302` plus the regenerated patch/clean selftest (`:106`). These have concrete failure signals.
- **8:** the duplicate S040 proposal / overlapping SOURCES and README edits are described (`:107`), but the row records manual integration, not a failing check or retained failure output. This is a coordination incident, not a demonstrated test red-before.

## Omissions from the W1 sweep

[OBS] C1’s declared counting command still omits `--live` (`claims.json:17`); the source specification says only `--live` checks untracked nested `.git` residue (`gen-wave1.py:66-68`). W1’s critic explicitly says the claim can read 11→0 while the residue remains (`w1/CriticC1.md:34-40`). This is an unlisted round-20 counter-scope mistake and undermines the D1 closure. Smallest correction: include `--live` or an independent delivered-worktree status assertion, and name the live check in the lesson.

[OBS] The C3 emulator’s initial “stop on any ReadError” model forecast false `invalid_data` failures for go/gofmt/compile where bound logs were silent: measured naive 5/8 versus corrected 8/8 (`w1/SimplifyC3Pipeline.md:178-202`). Rows 5-6 record reference-shape mismatches, not this substantive model error. The same report marks residual predicate/vacuity defects open (continue-set, trail cleanup, empty-D refusal: `:149-164`); these are not disclosed in the lesson’s Open section (`corpus/lessons/round-20.md:111-120`). Treat the latter as identified risks, not observed held-out failures.

[OBS] C2 names five target verbs but falsifies the claim only below three (`claims.json:25-30`); W1 notes this proves a 3/5 floor, not closure of all five (`w1/ReviewClaimsC2.md:11`). No Mistake row records this calibration gap. Smallest correction: require/report 5/5, or explicitly narrow the C2 claim to 3/5.

## Commands and exit codes

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/lessons/round-20.md` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/claims.json` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/gen-wave1.py | nl -ba` — exit 0.
- W1 recorded `python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --selftest` — exit 1 with the three cases above, then exit 0 (`w1/VerbCoverageTool.md:44-48`).
- W1 recorded `python3 -I -B .ufo/waves/round-20/tools/routed-r19.py --root /tmp/kr20-RoutedR19Tool-2 --rev 14f0260ad319ecc26994381b2415d5a999003375` — exit 0, `open_count=11`; no `--strict` (`w1/RoutedR19Tool.md:49-51`).
- W1’s naive and corrected eight-label probes each exited 0; results were 5/8 and 8/8 respectively (`w1/SimplifyC3Pipeline.md:255-256`).