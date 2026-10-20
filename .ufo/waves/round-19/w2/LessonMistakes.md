# Round 19 Mistakes rows 1–6 — review

**Scope / snapshot.** Read-only review of `corpus/lessons/round-19.md:80-89` and W19 evidence. Main advanced during the audit; final checks ran in a private clone at observed `refs/heads/main` `279e8b19c51658bfd05b9e31a1c0894ab2e70537`. No lane source edits, installs, builds, REA/Ghidra, or carrier execution. **Axes:** calibration (red-state sensitivity), freshness (revision-bound results), depth (targeted reruns), count semantics (report presence vs terminal state).

## Findings (severity order)

### MEDIUM — Row 5's hash check cannot fail on the cited no-execution breach

**[OBS]** `round-19.md:88` identifies the breach as `InstallRecordDraft` running `go version` on `go1.24.6`/`go1.25.0` `bin/go`. The retained command at `w1/InstallRecordDraft.md:26` records exit 0 for both; the `go1.25.0/bin/go` is explicitly the `t1250-go` carrier (`contract.md:39-44`, `predictions/carriers.tsv:1`). **[OBS]** The stated mitigation—archive digests and a runtime hash recheck—only proves byte identity: `run-carriers.sh:284-290` hashes each carrier before that runner's own analysis. Its `--selftest` includes a fake mismatched hash and expects the runner to skip that row (`run-carriers.sh:124-136,168-180`); I reran it successfully (26 cases, exit 0).

**[INFERENCE]** That gate cannot observe or reject a prior standalone `go version` invocation. Thus the hash check is shown able to fail for *changed carrier bytes*, not for the row's no-execution contract violation; the record is disclosure/qualification, not a preventive or fail-able control for that behavior. Scope precision: `go1.24.6/bin/go` is not in the Round-19 carrier list, while `go1.25.0/bin/go` is, so the row's phrase “go1.24.6/go1.25.0 … a C3 carrier” over-includes the former but still documents a real breach for the latter. I did not execute either binary.

### MEDIUM — Row 6's “dead seat” wording overstates what `wave1-outcomes.json` encodes

**[OBS]** The tool's contract is report-based: `wave-outcomes.py:15-21,312-353` records `report_present` and optional `cause`; exit 1 is only for a **missing report with no cause**. The W1 record reports 90 seats, 48 reports, 42 missing, 42 causes (`wave1-outcomes.json:11-19`). Re-running that input gives the same counts and exit 0. But it does not record `stop_reason`; a report-present seat may have `cause:null`. The selftest explicitly says a cause on a reporting seat is “retained, not required” (`wave-outcomes.py:658-669`).

**[OBS]** The separate terminal record has cutoff “after all W1 seats terminated” (`evidence/wave-outcomes/w1-terminal.json:1`). Its report/terminal cross-tab is: missing+aborted 33, missing+error 9, present+aborted 17, present+error 3, present+stop 28. The three present+error seats are `MistakesDraft`, `SkillRegistryDraft`, and `R12Disclosure` (`w1-terminal.json:587-596,631-640,676-684`). In `wave1-outcomes.json` those three instead have `report_present:true, cause:null` (`:279-283,334-337,532-535`).

**[INFERENCE]** Row 6's **42** is correctly a no-report count (9+33), not a terminal-death count; it separately calls out the three report-present errors. However, “each kept as a dead seat in `wave1-outcomes.json`” is not true for report-present terminal failures—the outcome file classifies them as reports, not dead/terminal. There are also 17 report-present aborts, so 42+3 is not a complete terminal-abnormal count. The row should not be read as one. The terminal JSON, not the report-only outcome record, is the evidence for terminal status; row 6 does not cite it.

### LOW — Row 1 compares unlike counts without the cutoff/category qualifier

**[OBS]** `round-19.md:84` contrasts “3 dead” with “4 not returned.” The retained W19 correction defines its population: four **without a report at `a245bb0`**, three with `terminal_state:error` and one with `terminal_state:aborted`; `DecisionRuleApply` returned after integration (`evidence/r18-dead-seats.json:4-7`). The row's red/green control demonstrates the four missing reports trigger four uncaused seats (exit 1) and that four retained causes clear them (exit 0); it does not equate report absence with death.

**[INFERENCE]** The evidence reconciles the counts when written as “4 no-report at cutoff = 3 provider errors + 1 abort”; the row's unqualified “3 dead” vs “4 not returned” can still be read as conflicting counts of the same set. Keep the cutoff and terminal categories explicit. The `routed-r18.py` substance check is stronger than the simple count: it compares the missing-report set and validates each cause/source against retained history (`tools/routed-r18.py:268-304`).

## Row-by-row failability

| Row | Result | Evidence / limitation |
|---|---|---|
| 1 | **Partial** | Red/green is real for uncaused report absence; it does not make `wave-outcomes.py` a terminal-state counter. `routed-r18.py` separately binds R18 causes to retained history. |
| 2 | **Yes** | At baseline both MIDMAP-LISTSTEP and VALIDATOR-DIGEST are red; at `279e8b1` both substance checks pass. The validator test rejects a well-formed wrong digest and accepts the true one; the list test rejects non-analyze-only pin checks (`tools/routed-r18.py:97-169`). |
| 3 | **Yes** | Baseline is red because the strict receipt is absent. At `279e8b1`, the check verifies receipt/stdout/stderr/tool hashes and replays `--strict` at `9011581` (`tools/routed-r18.py:195-229`). Limit: its comment expressly does not prove the historical process's time/authenticity. |
| 4 | **Yes, with the stated census limit** | `province-pins.py --strict` is 2 mismatches/exit 1 at B and 0/exit 0 at `279e8b1`. The census stale count changes 4→0, but the current census still exits 1 on the two pre-existing undeclared blocks; this is consistent with claims amendment `claims.json:39`, which withdraws a PASS claim. |
| 5 | **No, for the no-execution violation** | The hash mismatch guard can fail, but it cannot fail on an already executed binary (finding above). |
| 6 | **Partial** | The tool fails for a missing report with no cause; it does not require terminal status/cause for report-present failures (finding above). |

## Commands and observed exits

All mutating fixtures/outputs below were in `/tmp/kr19-w2-LessonMistakes.Aw694J`, outside LANE. The carrier hash command only read bytes; no carrier was executed.

```sh
# W19 wave-outcomes red replay: empty causes; 4 missing reports, 4 uncaused
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-18/wave2-registration.json --report-dir /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-18/w2 --causes /tmp/kr19-w2-LessonMistakes.Aw694J/r18-w2-empty-causes.json --out /tmp/kr19-w2-LessonMistakes.Aw694J/r18-w2-red-final.json
# exit 1

# Same reports, retained four causes
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-18/wave2-registration.json --report-dir /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-18/w2 --causes /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-causes.json --out /tmp/kr19-w2-LessonMistakes.Aw694J/r18-w2-green-final.json
# exit 0

# W1 outcome recount (90 / 48 / 42 / 0)
python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py --registration .ufo/waves/round-19/wave1-registration.json --report-dir .ufo/waves/round-19/w1 --causes .ufo/waves/round-19/evidence/wave-outcomes/w1-causes.json --out /tmp/kr19-w2-LessonMistakes.Aw694J/w1-outcome-final.json
# exit 0

# Report-vs-terminal count cross-tab and the three report-present errors
jq -r '"outcomes seats=\(.seat_count) reports=\(.report_present_count) missing=\(.missing_count) uncaused=\(.uncaused_count)"' .ufo/waves/round-19/wave1-outcomes.json && jq -r '.seats | group_by([.report_present,.stop_reason])[] | "report_present=\(.[0].report_present) stop_reason=\(.[0].stop_reason) count=\(length)"' .ufo/waves/round-19/evidence/wave-outcomes/w1-terminal.json && jq -r '.seats[] | select(.report_present == true and .stop_reason == "error") | "\(.name) report_present=\(.report_present) stop_reason=\(.stop_reason)"' .ufo/waves/round-19/evidence/wave-outcomes/w1-terminal.json
# exit 0

# Routed R18 controls (strict): baseline open 7, final main open 0
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-LessonMistakes.Aw694J/lane --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# exit 1
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-LessonMistakes.Aw694J/lane --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# exit 0

# Province pin controls: 2 mismatches at B; 0 at latest main
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/province-pins.py --root /tmp/kr19-w2-LessonMistakes.Aw694J/lane --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
# exit 1
python3 -I -B .ufo/waves/round-19/tools/province-pins.py --root . --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# exit 0

# Latest C1 census: stale=[], undeclared=2; expected remaining FAIL
python3 -I -B .ufo/gates/c1-census-v10.py --root . --json
# exit 1

# Targeted selftests
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/wave-outcomes.py --selftest
# SELFTEST: CLEAN cases=33; exit 0
python3 -I -B /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/tools/routed-r18.py --selftest
# SELFTEST: CLEAN cases=13; exit 0
bash /tmp/kr19-w2-LessonMistakes.Aw694J/lane/.ufo/waves/round-19/run-carriers.sh --selftest
# SELFTEST: CLEAN cases=26; exit 0
```

## Residual risk / verification gaps

- **[OBS]** `evidence/c1-census-v10-before.txt:6-14,38-44,112-113` is stale=4, undeclared=2, exit 1; current run is stale=[], undeclared=2, still exit 1. The gate never becomes PASS, as the amendment states.
- **[OBS]** `sha256sum` of the eight paths in `predictions/carriers.tsv:1-8` matched their frozen values (exit 0); this establishes bytes, not whether an earlier process executed one.
- **LSP gap:** no LSP device/server was exposed in the available tools, so I could not run its status/references/definition/diagnostics workflow. Findings above use direct source anchors and executed targeted commands; no grep result is presented as semantic proof.
- No package/tool installs or upgrades.
