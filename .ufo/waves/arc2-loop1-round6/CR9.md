# CR9 — attack the disabled-analyzer guess

**VERDICT: ATTACK HOLDS.** The three-name string is not a mitigation. `Decompiler Parallel Convention Analysis` is not a Ghidra analyzer name on 12.1.4. REA applies the list as one pre-script argument and aborts the whole list before `setAnalysisOption`, so the two real names were recognized and then not disabled. This is not a plain retry either: r3/r4 entered auto-analysis; this run died in the pre-script in 7.554s. C1's big leg is a typed name-mismatch refusal, not a scale result and not HELD.

Axes: name-fidelity (does the string name a registered analyzer), costume-detectability (can a wave tell without trusting the env), abort-vs-retry (did analysis start).

## How the wave knows

Env presence is not proof. `analyzer_preset` absence is not proof either — that field is written into a sealed bundle this run never produced (`failure_message: Ghidra exited before bridge startup`; string count `analyzer_preset=0`). The detecting artifact is the embedded Ghidra stdout inside the error envelope:

1. `REPORT: Execute script: .../ReaGhidraAnalysisOptions.java '<exact comma list>'` — the knob was forwarded, not dropped.
2. `Unknown Ghidra analyzer for this program: <name>` at `ReaGhidraAnalysisOptions.java:22` — the mismatch, naming the offender. Missing this line means either every name passed or the pre-script never ran.
3. `Processing aborted as a result of pre-script` — auto-analysis did not start. A later envelope that lacks (2) and lacks (3) and contains `analyzer_preset: ghidra-default+disabled:<same list>` committed the *requested* names into the profile (`GhidraAnalysisProfile.js:44`) before Ghidra validated them. That field still does not prove `setAnalysisOption(..., "false")` ran. Proof of disable is the pre-script passing the second loop (`ReaGhidraAnalysisOptions.java:25-35`) without `Ghidra analyzer remained enabled`. On this run the runtime dir is gone, so script.log cannot be re-read; the embedded stdout is the seal.
4. Independent of the live unit: `NAME` constants in `Decompiler-src.zip`. REA's schema (`ghidraDisabledAnalyzers.js:9-24`) checks charset only. There is no name catalog. A costume string that matches the regex launches.

## Evidence

Observed 2026-10-18T20:47:00Z. Service not signaled.

```sh
systemctl --user show arc2-r6-pe -p ActiveState -p SubState -p Result -p ExecMainStatus -p MemoryPeak -p Environment
# ActiveState=failed SubState=failed Result=exit-code ExecMainStatus=1
# MemoryPeak=2208227328
# Environment="REA_GHIDRA_DISABLED_ANALYZERS=Decompiler Parameter ID,Decompiler Switch Analysis,Decompiler Parallel Convention Analysis" REA_GHIDRA_STARTUP_TIMEOUT_MS=7200000 GHIDRA_HEADLESS_MAXMEM=6G ...
# ExecStart: npx -y rea-agents@6.5.0 analyze .../windows_release_arm64.exe ; status=1 ; wall 7.554s
sha256sum /var/tmp/arc2-l6r6-pe/stdout.json
# 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7  16692 bytes
```

Envelope `/var/tmp/arc2-l6r6-pe/stdout.json:31` (embedded Ghidra stdout) and `:38-39`:

- `Using Language/Compiler: AARCH64:LE:64:v8A:windows`
- `Execute script: .../rea-agents/bridge/ghidra/ReaGhidraAnalysisOptions.java 'Decompiler Parameter ID,Decompiler Switch Analysis,Decompiler Parallel Convention Analysis'`
- `Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis` at `ReaGhidraAnalysisOptions.java:22`
- `Processing aborted as a result of pre-script.`
- `failure_kind: process` / `failure_message: Ghidra exited before bridge startup`
- counts in the 16692 bytes: `analyzer_preset=0`, `evidence_id=0`, `analysis_options=0`, `disabled_analyzers=0`, `profile_digest=1` (`6d45f2349e0d4e7601dfd1123f0a346aaccd8d10545bf3d93edc207ae2999b88`)

Name table, Ghidra 12.1.4 PUBLIC (`application.properties:17`), zip `Ghidra/Features/Decompiler/lib/Decompiler-src.zip`, jar-scan hits for the third string = 0:

| requested | registered `NAME` | source | on this program |
|---|---|---|---|
| `Decompiler Parameter ID` | exact | `DecompilerFunctionAnalyzer.java:30` | recognized (see inference) |
| `Decompiler Switch Analysis` | exact | `DecompilerSwitchAnalyzer.java:46` | recognized (see inference) |
| `Decompiler Parallel Convention Analysis` | **absent** | command class only: `DecompilerParallelConventionAnalysisCmd.java:35` | rejected |
| (not requested) | `Call Convention ID` | `DecompilerCallConventionAnalyzer.java:41` | the analyzer that calls that command |

Script order, installed `rea-agents@6.5.0` (npx cache `~/.npm/_npx/ad9a3fdbcad992c6/.../ReaGhidraAnalysisOptions.java:18-28`): first loop throws on the first unknown name; `setAnalysisOption` is the second loop and did not run. Launcher forwards the joined string with no existence check: `dist/ghidra/GhidraLauncher.js:412-418`. Profile string is built from the env list before launch: `dist/ghidra/GhidraAnalysisProfile.js:41-45`.

Default enablement (why a corrected list is still not the r4 wall fix, unlabeled as unmeasured): `DecompilerFunctionAnalyzer.java:87-96` returns false unless address count `< 2*1024*1024` and format is PE — this binary is 91662336 bytes, so Parameter ID is already default-off. `DecompilerSwitchAnalyzer.java:70` and `DecompilerCallConventionAnalyzer.java:63` are `setDefaultEnablement(true)`. Unit Environment has no worker-reduction variable; SCORECARD.md:919 planned "disabled-analyzers + worker reduction."

Labels: **observation** — unit env string, envelope hash, embedded script argv, the `Unknown Ghidra analyzer` line naming only the third token, `analyzer_preset` count 0, `NAME` constants, script loop order, package 6.5.0 / Ghidra 12.1.4. **inference** — names 1 and 2 passed `getAnalyzer` + `options.containsKey` for this program, because the throw is sequential and names the third; neither was set to false. **inference** — a wave that scores "env was set" or "preset field missing" will mis-classify this as an unrecorded mitigation or as a plain retry. **unknown** — whether `Call Convention ID` plus `Decompiler Switch Analysis` (Parameter ID already default-off) would move the r4 memcg wall; mid-rung 17.7MB leg; worker-count knob name REA would honor (none is in this unit env).

## Verbatim-landable (honest-negative; parent lands)

```markdown
## 2026-10-18 arc2-loop1-round6 — disabled-analyzer names did not match

The 91.6MB PE retry is not a mitigated analysis and not a plain retry. User service `arc2-r6-pe` set `REA_GHIDRA_DISABLED_ANALYZERS=Decompiler Parameter ID,Decompiler Switch Analysis,Decompiler Parallel Convention Analysis` and exited 1 in 7.554s. Envelope `/var/tmp/arc2-l6r6-pe/stdout.json` (16692 bytes, sha256 `4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7`) embeds `Unknown Ghidra analyzer for this program: Decompiler Parallel Convention Analysis` at `ReaGhidraAnalysisOptions.java:22`, then `Processing aborted as a result of pre-script`. The first two strings are real `NAME` constants (`DecompilerFunctionAnalyzer.java:30`, `DecompilerSwitchAnalyzer.java:46` in Ghidra 12.1.4 `Decompiler-src.zip`). The third is the command class `DecompilerParallelConventionAnalysisCmd`, not an analyzer; the analyzer is `Call Convention ID` (`DecompilerCallConventionAnalyzer.java:41`). REA 6.5.0 validates charset only (`ghidraDisabledAnalyzers.js:9-24`) and aborts the whole comma-list before `setAnalysisOption` (`ReaGhidraAnalysisOptions.java:18-28`), so no analyzer was disabled. `analyzer_preset` is absent (0 hits); do not read that absence as "knob not forwarded" — the script argv in the same envelope is the forwarded list. A retry that keeps this string repeats the abort. Knowledge denominator stays 79 for this leg.
```
