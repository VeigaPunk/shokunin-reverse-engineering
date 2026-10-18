# CR5 — census completeness: C1 outcome classes the wave can miss

**Verdict: REFUSE a C1 admit that uses the pre-written trichotomy (HELD / honest-negative refusal-or-kill / in-flight) as a complete census.** That set has no bin for the live big leg, and it collapses the live mid-rung. Census v10 PASS and command A 79/79 do not grade these classes. This does not refute a later sealed HELD on the mid-rung, and it does not say the big-leg envelope is untyped — it says the typed class is not a scale-wall result.

Axes: class-coverage (a terminal state must not verify the wrong claim), leg-separability (two recipes, two legs), instrument-blindness (v10 and command A), seal-durability.

## Evidence

Roster vocabulary, this seat, over the 128-row fence in `.ufo/waves/arc2-loop1-round6/E26.md`:

```sh
python3 - <<'PY'
# parse E26.md fence; count scope hits
# observed: roster_rows 128
# execution_failure: 0; unknown analyzer: 0; pre-script: 0; cancelled: 0
# held: 9; refusal: 3 (P1,E7,E48); memory-kill: 2; in-flight: 1 (E37); timeout: 1 (E9)
PY
```

Declared bins:

- P1 scope (`.ufo/waves/arc2-loop1-round6/E26.md:40`): `held / typed refusal / memory-kill`.
- P5 (`.ufo/waves/arc2-loop1-round6/P5.md:19,24-26`): HELD iff `rea analyze` exit 0 + `evidence_id` + counts + sha256. Honest-negative iff `provider_timeout`, `CONSTRAINT_MEMCG` / cgroup OOM, or `cancelled` only if the configured deadline fired. "do not improvise a third class." Outer `timeout(1)` does not verify.
- E5 scope (`E26.md:60`): capture the class only "if the service terminates inside your window."
- E48 scope (`E26.md:103`): honest-stop text only "if BOTH legs refuse."
- P2 (`E26.md:41`) says the mid-rung uses "the same knob recipe." E9's scope (`E26.md:64`) sets only `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000` and `GHIDRA_HEADLESS_MAXMEM=6G`.

r3 already separated a typed terminal from a verifying refusal (`.ufo/waves/arc2-loop1-round3/R2.md:155-161`; `SCORECARD.md:800-808`): outer-cap `cancelled` is recorded and the claim stays not-verified because the deadline was untested.

Big leg, re-sampled this seat (service not signaled):

```sh
systemctl --user show arc2-r6-pe -p ActiveState -p Result -p ExecMainCode -p ExecMainStatus -p ExecMainExitTimestamp -p NRestarts -p MemoryPeak -p MemoryMax
# ActiveState=failed Result=exit-code ExecMainCode=1 ExecMainStatus=1
# ExecMainExitTimestamp=Sun 2026-10-18 17:41:06 -03
# NRestarts=0 MemoryPeak=2208227328 MemoryMax=9663676416
python3 - <<'PY'
# /var/tmp/arc2-l6r6-pe/stdout.json = 16692 bytes, not JSON
# counts: analyzer_preset=0 evidence_id=0 execution_failure=2 cancelled=0
# oom=0 CONSTRAINT_MEMCG=0 provider_timeout=0 exit_code=1 run_id=1
PY
```

Envelope pointers: `stdout.json:1-5` `code: execution_failure` / `retryable: false`; `:10` `operation: list_documents`; `:27` Ghidra child `exit_code: 0`; `:31` embedded `Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis`, `Processing aborted as a result of pre-script`, and `REPORT: Import succeeded`; `:38-39` `failure_message: Ghidra exited before bridge startup`. Died 7.554s after 17:40:58, before watch seats opened. Peak 2.2G is not the 9G cap.

Mid-rung, this seat at `2026-10-18T21:01:24Z` (read-only `ps`/`stat`; not signaled):

```sh
# /var/tmp/arc2-l6r6-E9-mid/meta.txt: start_utc=2026-10-18T20:46:09Z pid_shell=2279860
# run-leg.sh:7-8 exports STARTUP_TIMEOUT_MS=3600000 and HEADLESS_MAXMEM=6G only
# run-leg.sh:66-68 wraps node in `/usr/bin/timeout -k 60 5400` and redirects stdout.json
ps -p 2279860,2280341 -o pid,etime,stat
# 2279860 15:14 S    (bash run-leg.sh)
# 2280341 15:14 Ssl  (java AnalyzeHeadless … -postScript ReaGhidraNoReturnFix.java -postScript ReaGhidraBridge.java)
# no ReaGhidraAnalysisOptions in that cmdline
stat -c '%s' /var/tmp/arc2-l6r6-E9-mid/stdout.json   # 0
test -f .ufo/waves/arc2-loop1-round6/E9.md || echo E9.md=no   # E9.md=no
```

Instruments: command A extracts `2026-10-\d{2}-[a-z0-9-]+` from `## Coverage map` only (`SCORECARD.md:101-102`). Worktree `corpus/README.md` (HEAD `54bc9dd`, `git status --porcelain` empty for that file, blob `29cd30eefcc6aa2b84fe0fce11623ce1f8890d16`) has 79 such tokens, including `2026-10-13-r4-12-godot-arm64-scale` on `corpus/README.md:22`. Census v10's `SCOPE` stops at `SCORECARD.md` 768-854 (`.ufo/gates/c1-census-v10.py:104-108`) and matches pin/version loci (`:110-113`). Its PASS predicate (`:67-69`) has no PE outcome term. Receipts dir contains only `config-pre-pair.txt`.

Landing-form split: P5.md:30 requires a same-line append (README stays 187 lines). P7.md:94 and E23.md:72-75 prescribe a new coverage-map row and call it line-neutral. `## Coverage map` is `corpus/README.md:11`; the next heading is `## Knowledge` at `:70`; `:177` is the frontier bullet. A new line before `:177` shifts `:177`. A same-line append on `:22` does not.

## Classes with no required bin

1. **Scale-untested terminal (observed, big leg).** `execution_failure` + pre-script name rejection + `operation: list_documents` + peak 2.2G. Not HELD, not OOM, not `provider_timeout`, not deadline-`cancelled`, not in-flight. Roster scopes never name it (0 hits). P5 forbids a third class. E7.md:42-44 and P7.md:86 say do not force it into the three and say the wall was not tested — then both still select the verifying honest-negative branch (E7.md:3; P7.md:83-85). r3's rule was the opposite: typed but deadline-untested stays not-verified. **Inference:** following the claim text "refusal/kill verifies" admits C1 on a run that never auto-analyzed.
2. **Contradictory exit tokens.** Unit status 1 vs child `exit_code: 0` (`stdout.json:27`) vs embedded `Import succeeded` (`:31`) vs envelope `execution_failure`. P5.md:19 keys HELD on "rea analyze exit 0" without saying which exit. No roster scope names the disagreement. **Inference:** a token census can false-HELD.
3. **Mitigation unapplied / uncheckable.** Env listed three names; the throw is before any disable; `analyzer_preset=0`; runtime `ghidra.log` is gone (`stdout.json:21` path absent). E3's contract is to read that log. The seal is the embedded exception, not a skip section. Absence of `analyzer_preset` is not "names honored."
4. **Knob-recipe split (observed).** P2 says same recipe. The live mid cmdline has no `ReaGhidraAnalysisOptions` pre-script; the big unit died on that pre-script. **Inference:** the legs cannot share an outcome class. A mid HELD would not show the disabled-analyzer mitigation worked.
5. **Mid in-flight with a zero-byte envelope and no report (observed at 21:01:24Z).** Watch seats E1-E5 are bound to `arc2-r6-pe` only. E38's "not started" predates `meta.txt` `20:46:09Z`. P7.md:88 folds "absent at close" into honest-negative; P7.md:98 says in-flight is not a refusal. **Inference:** a report-only closeout records the mid-rung as not started or as a refusal while java is still in AnalyzeHeadless.
6. **Mid outer-cap / SIGKILL residue, not in E9's scope.** `run-leg.sh:66` is `timeout -k 60 5400` (rc 124, or 137 after `-k`). That is r3's non-verifying class (`R2.md:160-161`; P5.md:26). The 3600s REA deadline is shorter, so `provider_timeout` may win — unknown until the process ends. The contract does not name either timeout.
7. **Split matrix the "both refuse" seat does not cover.** Current: big = class 1, mid = class 5. Also unbinned: big class-1 + mid HELD (79→80 on the mid stem only — E23's HELD skeleton is `2026-10-18-arc2-r6-pe-scale`, the wrong file); dual HELD (command A 81, P5's gate expects 80); big HELD + mid outer-cap not-verified.
8. **New-row "line-neutral" HELD.** Command A would count a token inserted before `## Knowledge`, and `:177` would move. With C3's lessons insert that is +2, not the planned 177→178. P5's same-line append on `corpus/README.md:22` does not move it. The two forms are different census outcomes. A token appended only in the knowledge table (`corpus/README.md:117`) is invisible to command A.
9. **Standing-instrument blindness.** v10 and command A cannot fail on classes 1-7. A green pair is not an outcome census. No roster seat except R1 ("is the taxonomy complete?") and this critic is assigned to keep the bins closed.
10. **Already-dead vs dies-in-window.** E5's scope misses a unit that failed before the seat opened. This wave's watchers happened to sample it. The contract still lacks a required open-time terminal sample.
11. **Cited seal, bytes not in repo.** `stdout.json` is only under `/var/tmp`; the unit is transient. P7.md:66: `reset-failed` drops it. Receipts today are the pre-pair file only. A report-local hash is not a replayable receipt after that cleanup.
12. **Pin of the run vs configured pin.** ExecStart was `npx -y rea-agents@6.5.0` (E2.md:26; unit fragment cited by E5.md:9). Command A does not bind the outcome to that pin. A knowledge entry that cites Kimi's 6.7.0 would be a false version class. **Unknown:** whether a parent retry with a new InvocationID overwrites `stdout.json` before a receipt copy.

## Verbatim-landable (parent closeout rule; this seat does not edit corpus)

```text
C1 outcome census (arc2-loop1-round6): do not admit from the trichotomy HELD / refusal-or-kill / in-flight. For each leg, record exactly one class below. Do not collapse.

1. HELD — the leg's own process exit is 0, and the envelope has evidence_id, procedure/segment counts, and a target sha256 equal to the pre-pinned file. If a disabled-analyzer knob was set, analyzer_preset or a surviving ghidra.log must show those names disabled. Child exit_code 0, "Import succeeded", or the env string is not HELD. Then one hyphenated knowledge stem, appended on the existing coverage-map line corpus/README.md:22 (the r4-12 cell). Not a new row. Command A 79→80 for that one file. Two HELD files are 81, and the 80-gate fails.
2. Scale-result refusal — auto-analysis started, then provider_timeout at the configured REA deadline, or cgroup oom-kill / CONSTRAINT_MEMCG with MemoryPeak at MemoryMax, or REA cancelled only when the receipt proves that deadline fired. This is the verifying honest-negative. No knowledge file. Denominator stays 79. Do not call coverage improved.
3. Scale-untested terminal — process ended before auto-analysis: pre-script abort, unknown analyzer name, execution_failure, operation list_documents, bridge never started. Typed and sealed, but not a scale-wall result and not class 2. Same admission as r3's outer-cap (SCORECARD.md:800-808; .ufo/waves/arc2-loop1-round3/R2.md:160): not verified. No map token. Do not write "the wall is now X" or "9G insufficient".
4. Outer-cap or signal residue — timeout(1) rc 124, SIGKILL rc 137, or any kill that is not the unit's own memory cap. Not verified.
5. In-flight / unsealed — ActiveState=active, or a live pid with a 0-byte stdout and no evidence_id, including a scratch run that has no seat report yet. Not verified. Missing E9.md is not a refusal.
6. Not-started — no pid, no scratch, no report, re-checked at close. Not verified. An earlier seat's "not started" does not survive a later start_utc.

The 91.6MB service and the 17.7MB scratch are different legs. This round they are different recipes: arc2-r6-pe set REA_GHIDRA_DISABLED_ANALYZERS; /var/tmp/arc2-l6r6-E9-mid/run-leg.sh does not, and its java cmdline has no ReaGhidraAnalysisOptions pre-script. A mid HELD does not verify the big leg. A big class-3 death does not predict the mid leg.

Command A (SCORECARD.md:101-102) and census v10 (.ufo/gates/c1-census-v10.py:67-69,104-108) do not grade classes 1-6. A PASS on either is not this census. Copy systemctl show plus the envelope sha256 into .ufo/waves/arc2-loop1-round6/receipts/ before reset-failed. A hash that exists only inside a seat report is not durable once /var/tmp and the transient unit are gone.
```

## Labels

- **Observation:** Roster scopes have zero hits for `execution_failure`, `unknown analyzer`, `pre-script`, and `cancelled`. Big leg is `Result=exit-code` / status 1 / peak 2208227328 / envelope `execution_failure` / no `evidence_id`. Mid-rung shell 2279860 and java 2280341 were alive at 21:01:24Z; stdout 0 bytes; `E9.md` absent; runner has an outer `timeout -k 60 5400` and no disabled-analyzer export. Coverage-map token count on the clean HEAD file is 79. v10 SCOPE does not include a round-6 section.
- **Inference:** The integrating census (P1 + P5's closed list + "refusal verifies") will either have no cell for the big leg or will admit C1 on a run that never reached the wall. A report-only closeout will miss the live mid-rung. A new map row is not the line-neutral form P5 required.
- **Unknown:** Mid-rung class at parent close (still class 5 here). Whether its 3600s REA deadline or the 5400s `timeout(1)` fires first. Whether a renamed analyzer list would pass the pre-script on the 91.6MB binary. Whether the parent copies the envelope before `reset-failed` or starts a new InvocationID that overwrites `stdout.json`. Post-pair hashes.
