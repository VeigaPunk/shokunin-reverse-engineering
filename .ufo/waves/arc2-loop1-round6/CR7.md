# CR7 — critic: verdict inflation + smuggled exploratory claims

**Verdict: INFLATION REFUSED.** Do not admit the round, and do not score C1 verified, on the state observed here. The 91.6MB unit is a typed process failure with no sealed evidence and no scale measurement. The 17.7MB leg is in-flight, not a result. C2 and C3 are unlanded at HEAD `54bc9dd`. Partial landings and narrative upgrades below are not the claims.

Axes: calibration (class of the terminal state), coverage (79/79 vs a narrated 79→80), operability (probe exit class, not a selftest label), freshness (live pointers and the registry sentence), exploratory-smuggle (undeclared fourth claim).

## Evidence

### C1 — a typed exit is not a verified coverage claim

Commands (read-only; service not signaled; scratch `/var/tmp/arc2-l6r6-CR7`):

```sh
git rev-parse HEAD
# 54bc9dd90b0aea67c345c1c6aa180e160164d151
systemctl --user show arc2-r6-pe -p ActiveState -p SubState -p Result \
  -p ExecMainCode -p ExecMainStatus -p NRestarts -p MemoryPeak -p MemoryMax \
  -p OOMKills -p InvocationID -p ExecMainStartTimestamp -p ExecMainExitTimestamp
# ActiveState=failed SubState=failed Result=exit-code
# ExecMainCode=1 ExecMainStatus=1 NRestarts=0 OOMKills=0
# MemoryPeak=2208227328 MemoryMax=9663676416
# InvocationID=31dc1c7f0a5e4f9db082dfc9da37b90d
# ExecMainStartTimestamp=Sun 2026-10-18 17:40:58 -03
# ExecMainExitTimestamp=Sun 2026-10-18 17:41:06 -03
systemctl --user show arc2-r6-pe -p ExecStart
# argv: npx -y rea-agents@6.5.0 analyze .../windows_release_arm64.exe
stat -c '%s' .../windows_release_arm64.exe
# 91662336
stat -c '%s %y' /var/tmp/arc2-l6r6-pe/stdout.json /var/tmp/arc2-l6r6-pe/stderr.log
# 16692 2026-10-18 17:41:06.513410314 -0300
# 0    2026-10-18 17:40:59.004392450 -0300
sha256sum /var/tmp/arc2-l6r6-pe/stdout.json
# 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7
```

Envelope counts in those 16692 bytes (head is `error: Analysis failed` / `code: execution_failure`, not a JSON bundle): `evidence_id=0`, `analyzer_preset=0`, `ANALYZING=0`, `Unknown Ghidra analyzer=1`, `Decompiler Parallel Convention Analysis=2`, `Processing aborted=1`, `target_sha256=1`, `run_id=1`.

**Observation.** Terminal, not in-flight, not OOM (`OOMKills=0`, peak 2G of 9G), not the 7200000 ms deadline (wall ~7.5s). Runtime pin is `rea-agents@6.5.0`, not the Kimi pin at `SCORECARD.md:59-60`.

**Inference.** This is not the pre-accepted scale refusal. Round 3 refused to verify coverage when the 91.6MB leg died at an outer cap before the deadline, and refused a knowledge entry as a re-run dressed as a move (`SCORECARD.md:797-808`, verdict `unprovable (honest stop)` at `:832`). This run never entered analysis. `P7.md:54` calling it "the pre-accepted refusal/kill branch, typed, with sealed evidence" inflates a setup abort into that branch. Sealed evidence in that precedent is an evidence id (`SCORECARD.md:802-804`: "no evidence sealed"). `run_id` is not `evidence_id`.

**Do not score.** Coverage improved, C1 verified, "either way", wall tested, 9G insufficient, deadline insufficient, disabled-analyzer lead tested, Kimi 6.7.0 tested. Denominator stays 79. No knowledge file. No map token.

Command A at the worktree (recipe `SCORECARD.md:101-122`): knowledge files 79, mapped 79, missing `[]`, dangling `[]`. Score is `|files ∩ mapped| / |files|`. A dangling token does not make 79→80. A lessons-index row is outside the Coverage-map split and does not either.

### C1 — two legs, one denominator slot; mid-rung is in-flight

**Observation.** Mid-rung process, not the failed unit. `E9.md` absent. `/var/tmp/arc2-l6r6-E9-mid/stdout.json` size 0 at listing. `meta.txt:1` `start_utc=2026-10-18T20:46:09Z`. `ps` elapsed 22:58 on pids 2279873/2279876: `timeout -k 60 5400 node .../rea.mjs analyze .../agent-browser-win32-x64.exe`. `run-leg.sh:7-8` sets `REA_GHIDRA_STARTUP_TIMEOUT_MS=3600000` and `GHIDRA_HEADLESS_MAXMEM=6G` and does not export `REA_GHIDRA_DISABLED_ANALYZERS`. Identity pin matches r3 (`E38.md:19-20`: 17694720 bytes, sha256 `a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786`). Not signaled.

**Inference.** In-flight is not HELD and not a refusal. The dispatch's in-flight rule ("claim not verified") applies to this leg until a typed terminal state exists. A later HELD on this binary must not be narrated as the 91.6MB wall. The stated 79→80 admits one new mapped file, not two. Both legs HELD would be 81, or one entry smuggling a second surface.

**Unknown.** Whether the mid-rung reaches a typed terminal state before parent close. If it is still in-flight at close, that leg is not verified. Sibling failure does not close it.

### C1/C3 — "line-neutral" is the smuggle

`corpus/README.md` is 187 lines. `:68` is the last Coverage-map row, `:70` is `## Knowledge`, `:138` holds `4 nits: 2 fixes applied at integration`, `:165` is the last lessons row, `:167` is `## Frontier`, `:177` holds `held, not frontier`.

Probe entries `sc69-readme-177` and `sc72-readme-nitrow` extract the numbers from `SCORECARD.md:69` and `:72` (`.ufo/gates/citation-drift/pointer-table.json:53-72`). A new line inserted before `:70` shifts both `:138` and `:177`. A lessons row inserted at `:165` shifts `:177` only.

`P7.md:58` says the map-row insert "does not shift `## Frontier`". That is false for any added line before `:70`. `C1.md:31` already measured the bad landing: new coverage-map row plus a `:177`→`:178` re-point leaves probe `findings=2` (`sc69` and `sc72`). C3 as declared owns only the `:177` re-point (`SCORECARD.md:981-984`). The 3-cell row is therefore not line-neutral and not separable; landing it without also re-pointing `:138` harms the probe. A same-line token is a different form: it can move the intersection only if a new knowledge stem exists; without that file it is a dangling token, still 79/79. Do not call the row form line-neutral to satisfy the dispatch sentence.

Census `SCOPE` ends at `SCORECARD.md:768-854` (`.ufo/gates/c1-census-v10.py:106-108`). It does not grade `:69` or README. Census PASS is not a witness for the re-point.

### C2 — unlanded; a partial fix must not be scored

```sh
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . \
  --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef \
  --table .ufo/gates/citation-drift/pointer-table.json \
  --expected .ufo/gates/citation-drift/expected.json
# CITATION_DRIFT_VERDICT: reported findings=7 exit=0
# EXIT:0
# citation_file_absent count: 7
# same command --strict → CITATION_DRIFT_VERDICT: failed findings=7 exit=1  EXIT:1
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . \
  --rev 54bc9dd90b0aea67c345c1c6aa180e160164d151 \
  --table .ufo/gates/citation-drift/pointer-table.json \
  --expected .ufo/gates/citation-drift/expected.json
# CITATION_DRIFT_VERDICT: reported findings=0 exit=0
```

Cause: `git_show` maps any non-zero `git show` to `absent at REV` (`citation-drift-probe.py:91-96`); `Tree.lines` files `citation_file_absent` (`:122-125`); `Findings.verdict` returns CNE only for snapshot/root/internal ids (`:69-76`), then probe mode returns CLEAN (`:77-78`). No `rev-parse` of `--rev`. `expected.json:14-24` has 10 cases and no absent-revision case. `selftest()` always calls `run_check(..., "HEAD", ...)` (`:406`) and `verdict(strict=True)` (`:408`), not `report()`.

Registry `SKILL.md:348` says "0 reported … and 2 could-not-evaluate" and "10 isolated-fixture cases". It does not name a dead revision. r5 named the debt (`SCORECARD.md:964-966`). `C1.md:22` calling the "10 cases" update optional is the freshness harm: after the gain, a registry that still says 10 is false. Protocol admits a round only if no axis is harmed (`AXES.md` working-the-axes paragraph: every claim verifies and no axis is harmed).

**Acceptance, all required, else C2 not verified:**

- CLI, probe mode and `--strict`: dead/absent rev exits 2, verdict line `could-not-evaluate`, exactly one CNE-class finding, zero `citation_file_absent` lines. Same shape as `root_unreadable` (early return, `:255-266`). Seven absent-file lines at exit 2 is a partial.
- Valid-rev `citation_file_absent` stays a drift finding. `expected.json` case `file_absent` stays exit 1. Reclassifying every absent file as CNE fails byte-stability and is the wrong fix.
- The new selftest case must pass a non-resolving rev into `run_check`. A JSON row that still runs at fixture `HEAD` is not the case. Selftest CLEAN alone does not prove the CLI label.
- Original 10 `SELFTEST_CASE` lines unchanged. The summary line `cases=10`→`11` is not byte-stable; do not claim full-stdout stability.
- Valid-rev CLI stays `reported findings=0 exit=0`. `pointer-table.json` byte-stable. Frozen-run digest pin is not this claim (`expected.json:3-13`).
- Same landing updates `SKILL.md:348` from 10 cases to 11 and names dead/absent `--rev` as exit 2 in both modes. That sentence is not byte-stable and must not be described as such.

Not run: `--selftest` (it `git commit`s fixture repos; this seat does not). Unknown whether the current 10 cases still pass; the table on disk has no eleventh case.

### C3 — gates already green is not the after-state

HEAD already has probe `findings=0 exit=0` and command A 79/79, with no `2026-10-18-wave-dispatch-counting` row (`corpus/README.md:155-165` ends at `2026-10-15-round-1-admission-correction`). Scoring C3 verified because those gates are green is scoring the before-state.

**After-state:** the lessons row exists, and `sc69` still resolves. If the only README insert is one lessons line, `:177` becomes `:178` and `:138` does not move. If a coverage-map line is also inserted, both move and C3's stated single re-point is wrong. Do not rewrite dated records (`LOG.md:685`, `SCORECARD.md:680` `corpus/README.md:90,:160`). Do not "clean" unrelated cells (Knowledge date cell `corpus/README.md:149` is `2026-10-16-l7-03`) inside this claim.

### Smuggled exploratory — not a fourth claim

`AXES.md` exploratory rule: at most one per round; verifies only as `unprovable-but-better` with a named non-author reviewer; a dispatched seat does not count. This round already declared three measurable claims. The following are observations or unknowns, not axis-moves:

- The unknown analyzer name. Named debt if the wall is re-carried. Not a coverage finding. Whether dropping that one name would pass is **unknown**.
- "9G / 2h was the test." Untested.
- Retargeting `GhidraClient.js:607` from a 6.5.0 abort. Out of claim set (`SCORECARD.md:1019`).

### Custody

```sh
tail -n +2 .ufo/waves/arc2-loop1-round6/receipts/config-pre-pair.txt | sha256sum -c -
# 5 OK, EXIT:0
```

5/5 at stamp `2026-10-18T20:39:12Z`. Not evidence that the PE process was the Kimi 6.7.0 pin. Post-pair is parent-close; not claimed here.

## Verbatim-landable (parent lands; this seat does not edit corpus)

```text
CR7 (arc2-loop1-round6) — do not inflate. C1 is not verified. arc2-r6-pe is failed/exit-code/status 1 (InvocationID 31dc1c7f0a5e4f9db082dfc9da37b90d, 17:40:58–17:41:06 -03, OOMKills=0, MemoryPeak=2208227328 of 9663676416). ExecStart is npx -y rea-agents@6.5.0 analyze windows_release_arm64.exe (91662336 bytes). Envelope /var/tmp/arc2-l6r6-pe/stdout.json is 16692 bytes, sha256 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7: execution_failure, evidence_id absent, analyzer_preset absent, ANALYZING absent, pre-script abort "Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis". That is not sealed evidence and not a scale-wall result (SCORECARD.md:797-808, :832). No knowledge file, no map token, denominator stays 79/79. Do not write "wall refused", "9G insufficient", or "disabled-analyzers lead tested".

The 17.7MB leg is a different process, in-flight at this seat's read (pid 2279876, start 2026-10-18T20:46:09Z, timeout 5400, stdout.json 0 bytes, no REA_GHIDRA_DISABLED_ANALYZERS in run-leg.sh). In-flight is not HELD. A later HELD on agent-browser-win32-x64.exe (17694720 bytes, sha256 a6a9a3654c41ee19c05961b73489db98cff9eae88a77436986df08a7a7a73786) must not be narrated as the 91.6MB wall, and 79→80 admits only one new mapped file. If it is still in-flight at close, that leg is not verified.

C2 is unlanded (dead rev: reported findings=7 exit=0; --strict findings=7 exit=1). Closes only when both modes exit 2 could-not-evaluate with one CNE finding and zero citation_file_absent lines, valid-rev file_absent stays exit 1, the new selftest case actually passes a bad rev, the original 10 SELFTEST_CASE lines stay put, valid-rev CLI stays findings=0, and SKILL.md:348 is updated from "10" to 11 and names the dead-rev input. Seven drift lines at exit 2 is not the fix. A stale "10 cases" sentence is a freshness harm, not optional.

C3 is unlanded. Probe findings=0 and command A 79/79 at HEAD are the before-state, not the landing. Census SCOPE ends at SCORECARD.md:854 and does not grade the :177 pointer. A new coverage-map line is not line-neutral: it shifts corpus/README.md:138 and :177 and breaks sc72 unless :72 is re-pointed too (C1.md:31 measured findings=2). A lessons row shifts :177 only. Do not admit the round by relabeling the big-leg abort as the coverage claim verified.
```

## Labels

- **Observation:** HEAD `54bc9dd`; unit failed as above; envelope counts; command A 79/79; probe dead-rev exit 0 / strict exit 1 / valid-rev findings=0; custody 5/5; README line anchors `:68/:70/:138/:165/:167/:177`; mid-rung pid alive, stdout 0, script exports differ from the unit.
- **Inference:** big-leg abort is not a coverage verification; "sealed evidence" and "line-neutral row" are the inflation sentences; C2/C3 acceptance is the predicate list above; registry "10" left stale would harm freshness.
- **Unknown:** mid-rung terminal state at parent close; whether a renamed analyzer list would pass on the 91.6MB binary; current selftest 10/10 (not re-run; case table has no absent-rev row).
