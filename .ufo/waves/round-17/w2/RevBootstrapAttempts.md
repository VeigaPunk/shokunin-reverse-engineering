# RevBootstrapAttempts — what `bootstrap_attempts` actually counts

Seat: KaidokuR17.RevBootstrapAttempts (advisory revenger, leaf; no dispatches).
Lane revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`. Every file cited below is
clean at that revision (`git diff --stat` for `tools/ w1/ runs/ predictions/ contract.md`
and the knowledge entry: empty). The only modified tracked file in the lane is
`run-carriers.sh`, which this report does not cite; `w2/` and the dispatch files are
untracked by design.
Scope: (a) confirm from installed Ghidra 12.1.4 source why
`runs/*/observation.json` shows `bootstrap_attempts` 1 on success and 2 on failure;
(b) enumerate every caller that can add an attempt.
Method: read-only. Source read from
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
(extracted to `/tmp/r17rb`); class checks with `javap` (OpenJDK 21.0.12.1); counts
recomputed with the round-17 `tools/log-extract.py` on retained logs and on one
scratch fixture under `/tmp`. No REA analyze/search/decompile, no Ghidra /
`analyzeHeadless`, no carrier execution, no installs.
Labels: **OBSERVED** = present in a file or a command output; **INFERENCE** =
source-derived, not executed.

## Verdict

**Confirmed, with a causal correction.** The number is not a retry count and not a
bootstrap count. It is the number of `getSharedGoBinary` **supplier invocations that
missed the `TransientProgramProperties` cache**, because the only emitter of
`Reading Go binary info` sits inside that supplier
(`GoRttiMapper.java:106`, OBSERVED).

- **Success → 1:** the first miss runs `getGoBinary` + `init`, returns the mapper
  (`GoRttiMapper.java:108-111`), and `getProperty` stores it under
  `SCOPE.ANALYSIS_SESSION` (`TransientProgramProperties.java:112`). Every later
  caller in the same analysis session gets the cached object
  (`TransientProgramProperties.java:106-107`, `:117`) and never re-enters the lambda.
- **Failure → 2:** the supplier returns `null` (`GoRttiMapper.java:125`) after one of
  its four failure routes, and `getProperty` deliberately does **not** cache null —
  it returns at `TransientProgramProperties.java:109-111` before `addProperty`.
  Each subsequent caller therefore re-runs the whole lambda, logging one more
  `Reading Go binary info`. Exactly **two** default-enabled analyzers call it on the
  round-17 carriers: `GolangSymbolAnalyzer.java:133` and `GolangStringAnalyzer.java:103`.
- **The third caller is not an analyzer and is absent here:**
  `GolangDWARFFunctionFixup.java:286`. It is only reached from DWARF function
  processing, and all eight retained logs show DWARF analysis skipped or absent.
  If a Go binary *with* DWARF failed the same way, that caller retries **once per
  imported Go function**, so the count would be one per Go function plus the two
  analyzer calls, not 3 (INFERENCE, §3).

The knowledge entry's anchor for the mechanism (`TransientProgramProperties.java:107-110`)
is exact: lines 107-110 are the cache miss, the supplier call, the null test and the
early `return null`.

## 1. Source chain (exact anchors, OBSERVED)

Member paths are inside
`Base-src.zip`; line numbers are from the extracted members.

| Step | Anchor | Evidence |
|---|---|---|
| Counter definition | `tools/log-extract.py:84`, `:139`, `:206-208`, `:246` | `READING_RE = ^Reading Go binary info: (\S+)`; `if component == "GoRttiMapper"` then `reading_count += 1`; emitted as `"bootstrap_attempts"` |
| Only emitter | `GoRttiMapper.java:106` | `Msg.info(GoRttiMapper.class, "Reading Go binary info: " + program.getName())` inside the `PropertyValueSupplier` lambda (`:104-126`) |
| Cache lookup | `TransientProgramProperties.java:106-107` | `Property property = perProgramProps.props.get(key); if (property == null) {` |
| Cache-miss supplier run | `TransientProgramProperties.java:108` | `T supplierVal = supplier.get();` |
| **Null is not cached** | `TransientProgramProperties.java:109-111` | `if (supplierVal == null) { return null; }` — returns before `addProperty` (`:112`) |
| Failure route A: no build info | `GoRttiMapper.java:153-162` (`:160-162` return null) | `fromProgram` null and `fromFallbackInfo` null → returns null without exception |
| Failure route B: invalid version | `GoRttiMapper.java:166-168` | `throw new BootstrapInfoException("Invalid Go version string [%s]")` |
| Failure route C: missing snapshot | `GoRttiMapper.java:348` → `:351-360` | constructor calls `initStructMappings()`; `registerStructures` throws, `apiSnapshot.isInvalid()` → `throw new BootstrapInfoException("Missing Go bootstrap type info…")` |
| Failure route D: IOException | `GoRttiMapper.java:118-123` | `Msg.error(… "Failed to read Go info" …)`; not present in any of the 8 logs (checked) |
| Exception caught, null returned | `GoRttiMapper.java:114-117`, `:125` | `Msg.warn` carries the `BootstrapInfoException` text; `:125 return null` |
| Cache dropped at session end | `TransientProgramProperties.java:160-169`; program close `:154-157` | ANALYSIS_SESSION properties are removed and closed; success is therefore "1 per analysis session", not "1 forever" |
| Caller 1 | `GolangSymbolAnalyzer.java:133-137` | `getSharedGoBinary`; on null logs `Go symbol analyzer error: unable to get GoRttiMapper` |
| Caller 1 enablement/order | `GolangSymbolAnalyzer.java:98-101`, `:104-107`, `:74-75` | BYTE_ANALYZER, `setDefaultEnablement(true)`, `canAnalyze = isGolangProgram`, priority `FORMAT_ANALYSIS.after().after()` |
| Caller 2 | `GolangStringAnalyzer.java:103-107` | same call; on null logs `Go string analyzer error: unable to get GoRttiMapper` |
| Caller 2 enablement/order | `GolangStringAnalyzer.java:77-81`, `:94-96`, `:79` | BYTE_ANALYZER, default-enabled, `canAnalyze = isGolangProgram`, priority `STRINGS_PRIORITY` = after `REFERENCE_ANALYSIS` (`GolangSymbolAnalyzer.java:76-79`) |
| Snapshot route on missing base | `GoApiSnapshot.java:105-116` | no base JSON → `return GoApiSnapshot.EMPTY` with no log; hence no `Using Go API snapshot` line before the constructor throws |
| DWARF runs before Go symbol | `DWARFAnalyzer.java:57-58` vs `GolangSymbolAnalyzer.java:74-75` | `FORMAT_ANALYSIS.after()` precedes `FORMAT_ANALYSIS.after().after()` |

Why the two blocks are one supplier run each: on the out-of-range carriers each
block is `Reading` → `Untested Go version` (`GoRttiMapper.java:170-172`, advisory
only) → `Missing Go bootstrap type info` (`:115` warning from the caught exception)
→ one analyzer's `unable to get GoRttiMapper`. The repeated work is the build-info
read (`GoBuildInfo.java:81-84`, `:92-108`, `:137-153`; no memoization), the version
check and snapshot resolution, and the constructor's failing `registerStructures`.
`init()` (`GoRttiMapper.java:444-466`) — and therefore `findFirstModuledata` /
the pclntab search (`:1116-1139`) — is **never entered** on this route, because the
constructor throws at `:358` before `getGoBinary` returns at `:187` and before
`supplier_result.init(monitor)` at `:110`.

## 2. Observed reconciliation (OBSERVED)

Command (run from the lane root):

```
for d in .ufo/waves/round-17/runs/*/; do
  log=$(python3 -B -c "import json;print(json.load(open('$d/observation.json'))['log_path'])")
  n=$(grep -c "Reading Go binary info" "$log")
  obs=$(python3 -B -c "import json;print(json.load(open('$d/observation.json'))['bootstrap_attempts'])")
  echo "$d recount=$n observed=$obs"
done
```

```
runs/calib-esbuild-0.25.12/ recount=1 observed=1
runs/calib-shfmt/ recount=2 observed=2
runs/pro-aether/ recount=1 observed=1
runs/pro-containerd-shim/ recount=2 observed=2
runs/pro-esbuild-0.21.5/ recount=1 observed=1
runs/pro-esbuild-0.27.7/ recount=2 observed=2
runs/pro-notesmd-cli/ recount=1 observed=1
runs/pro-op/ recount=2 observed=2
```

All eight reconcile. The two-attempt blocks are attributable to specific callers by
the adjacent error line (OBSERVED):
`runs/calib-shfmt/logs/rea-ghidra-j5AXOZ/ghidra.log:82-85` (first = symbol analyzer)
and `:86-89` (second = string analyzer);
`runs/pro-esbuild-0.27.7/logs/rea-ghidra-DjvEp2/ghidra.log:63-64` (symbol) and
`:68-69` (string). On the success side, e.g.
`runs/calib-esbuild-0.25.12/logs/rea-ghidra-B5tAvn/ghidra.log:62` is the only
`Reading` line, and `Go strings found` at `:83` runs without a second one.

Boundary check on the second analysis pass: the retained logs contain
`ANALYZING changes made by post scripts` after the first pass
(`runs/calib-esbuild-0.25.12/.../ghidra.log:124`; `GoRttiMapper.close()` had already
logged `Go missing type names: 19` at `:85` — close runs from
`analysisEnded` via `Property.close()`, `TransientProgramProperties.java:133-139`
and `:160-169` — so the cached instance had been released before that pass). No
`Reading` line follows the post-script pass, so in these runs the analyzers were not
re-invoked and the count is unchanged.

## 3. Every caller that can add an attempt (OBSERVED search; one INFERENCE)

Exhaustive caller search, three independent ways:

```
$ cd /tmp/r17rb && grep -rn "getSharedGoBinary" all/ | sed 's#^all/##'
ghidra/app/plugin/core/analysis/GolangStringAnalyzer.java:103:		goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:133:		goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
ghidra/app/util/bin/format/golang/GolangDWARFFunctionFixup.java:286:			goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:102:	public static GoRttiMapper getSharedGoBinary(Program program, TaskMonitor monitor) {

$ cd /tmp/r17rb && grep -rl getSharedGoBinary basejar | sed 's#^basejar/##'
ghidra/app/plugin/core/analysis/GolangStringAnalyzer.class
ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.class
ghidra/app/util/bin/format/golang/GolangDWARFFunctionFixup.class
ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.class

$ cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC && \
  find Ghidra -name '*.jar' -print0 | xargs -0 -n1 -P8 sh -c \
    'unzip -p "$0" 2>/dev/null | grep -qa getSharedGoBinary && echo "$0"' | sort
Ghidra/Features/Base/lib/Base.jar
$ find Ghidra -name '*.jar' | wc -l
195
```

So there are exactly three call sites in the installed distribution, and only one
emitter of the counted string.

3.1 `GolangDWARFFunctionFixup` — the only additional caller, and it is per-function.
Anchors: `GolangDWARFFunctionFixup.java:47` (`@ExtensionPointProperties(priority =
DWARFFunctionFixup.PRIORITY_NORMAL_EARLY)`), `:74` (`private GoRttiMapper goBinary;`),
`:77-80` (early return unless `isGolangFunction(dfunc)` and
`initGoBinaryContext(...)`), `:283-289` (`if (goBinary == null) getSharedGoBinary(...)`).
One fixup instance per `DWARFProgram` (`DWARFProgram.java:629-634`,
`DWARFFunctionFixup.findFixups()` cached), invoked once per imported function
(`DWARFFunctionImporter.java:191` → `DWARFFunction.java:442-455`). Because the field
stays null on failure, **the next Go function calls `getSharedGoBinary` again**.
INFERENCE: a Go binary with DWARF CUs whose bootstrap fails would log one
`Reading`/`Untested`/`Missing` triplet per Go function plus the two analyzer blocks.
No retained run loaded DWARF: `DWARFAnalyzer` logged "Unable to find DWARF information, skipping DWARF
analysis" in five runs (`calib-shfmt:81`, `pro-notesmd-cli:66`, `pro-aether:90`,
`pro-containerd-shim:239`, `pro-op:67`), and the three esbuild logs contain no DWARF
records at all. So the magnitude is not observed here, only source-derived.

3.2 Analyzers that mention `GoRttiMapper` but cannot add attempts (OBSERVED).

```
$ cd /tmp/r17rb && javap -p -c -classpath basejar ghidra.app.plugin.core.analysis.ApplyDataArchiveAnalyzer | grep GoRttiMapper
       1: invokestatic  #55                 // Method ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.isGolangProgram:(Lghidra/program/model/listing/Program;)Z
$ cd /tmp/r17rb && javap -p -c -classpath basejar ghidra.app.plugin.core.function.SharedReturnAnalyzer | grep GoRttiMapper
      18: invokestatic  #70                 // Method ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.isGolangProgram:(Lghidra/program/model/listing/Program;)Z
```

Both are single `isGolangProgram` checks, no `getSharedGoBinary`. The `GhidraGo`
module (`Ghidra/Features/GhidraGo/lib/GhidraGo.jar`) has zero `GoRttiMapper`
references. The REA 6.5.0 bridge scripts
(`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/bridge/ghidra/*.java`)
have zero `GoRttiMapper` / `getSharedGoBinary` references. No loose `.java` file under
the install tree references it.

## 4. Findings

### B1 — MEDIUM — w1 source chain mislocates the throw and overstates what repeats

Target: `.ufo/waves/round-17/w1/ScoutGolangAnalyzers.md:36-37`.

Claim being attacked (verbatim, `:36`): "throws `BootstrapInfoException` for … a
missing type snapshot (`:356-360` inside `initStructMappings`, reached though
`supplier_result.init(monitor)` at `:110`)"; and (`:37`) "so *every* analyzer pass
repeats the full bootstrap attempt, including the pclntab search
(`GoRttiMapper.java:1116-1139`)".

Command and output:

```
$ cd /tmp/r17rb && grep -n "" ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | sed -n '346,349p;444,446p'
346:		this.goTypes = new GoTypeManager(this, apiSnapshot);
347:
348:		initStructMappings();
349:	}
444:	public void init(TaskMonitor monitor) throws IOException {
445:		GoModuledata firstModule = findFirstModuledata(monitor);
446:		if (firstModule != null) {
```

The constructor (`:330-349`, called at `:187`) throws; `init()` (`:444`) is never
reached, and neither is `findFirstModuledata` (`:1116-1139`). The repeated work is
the build-info read + version check + `GoApiSnapshot.get` (EMPTY, `:115`) + the
failing `registerStructures` in the constructor. The retained logs agree: none of
the 8 has `Failed to read Go info`, `Invalid Go version string`, or a moduledata
error; every failure carries exactly the constructor's
`Missing Go bootstrap type info` warning.

Why it matters: the sentence is the wave-1 "full bootstrap attempt" model that the
knowledge entry rests on. It misnames both the throw site and the expensive step.
Severity is medium because the observable count is unaffected, but a cost/scope
claim ("the pclntab search repeats") is false for the only failure route observed.

Smallest fix: replace the parenthetical with "constructor `:348` → `initStructMappings`
`:351-360`; `getGoBinary` never returns and `init()` `:444` (the pclntab search,
`:1116-1139`) is never entered", and change "the full bootstrap attempt" to "the
build-info/version/snapshot resolution and the failing struct-mapping registration".

### B2 — MEDIUM — knowledge entry's "once per Go analyzer" is not the general law

Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:76-77`.

Claim: "The bootstrap attempt repeats once per Go analyzer (`bootstrap_attempts` = 2),
because a null mapper is not cached (`TransientProgramProperties.java:107-110`)."

The mechanism clause is right; the generalisation is wrong in two ways. (i) The count
is per **cache-missing caller**, not per analyzer; the third caller is a DWARF
function fixup, not an analyzer (`GolangDWARFFunctionFixup.java:286`). (ii) On a
DWARF-bearing Go binary that caller retries **per function** (`:283-289` with the
field never set, invoked at `DWARFFunctionImporter.java:191`), so the count is
one per imported Go function plus 2, not bounded by 2 or 3 (INFERENCE; §3.1). The
observed 2 is the DWARF-absent case, which
holds for all 8 carriers (DWARF log anchors in §3.1).

Why it matters: the entry is the round's knowledge product, and `bootstrap_attempts`
is being offered as a cross-carrier diagnostic. A reader applying "2 = one per
analyzer" to a DWARF-bearing carrier would mispredict both the count and the log
volume.

Smallest fix: qualify the sentence in place — "two on a DWARF-less carrier (one per
calling analyzer); a DWARF-bearing carrier adds one per imported Go function via
`GolangDWARFFunctionFixup.java:286`, because that fixup's `goBinary` field stays null
and it retries per function".

### B3 — LOW — the tool's failure fixture is a single-attempt shape and the field is unasserted

Target: `.ufo/waves/round-17/tools/log-extract.py:282-295` (fixture) and
`:299-310` (checks).

`shfmt_like` contains exactly one `Reading Go binary info` line (`:285-286`), while
the pilot log the fixture is named after has two blocks (quoted in
`w1/ScoutGolangAnalyzers.md:44-53`, and `w1/LogExtractTool.md:28` says "shfmt logs
the same bootstrap failure twice, lines 82-85 and 86-89"). The checks dict never
asserts `bootstrap_attempts`.

Command and output (fixture rebuilt from `shfmt_like`, and the retained log):

```
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log /tmp/r17rb/selfshadow.log \
  | python3 -B -c "import json,sys;print('fixture bootstrap_attempts =',json.load(sys.stdin)['bootstrap_attempts'])"
fixture bootstrap_attempts = 1
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log \
  .ufo/waves/round-17/runs/calib-shfmt/logs/rea-ghidra-j5AXOZ/ghidra.log \
  | python3 -B -c "import json,sys;print('retained shfmt bootstrap_attempts =',json.load(sys.stdin)['bootstrap_attempts'])"
retained shfmt bootstrap_attempts = 2
```

Why it matters: the 2-on-failure semantics the knowledge entry highlights has no
regression test; a counter change that produced 0/1 on failure would still print
`SELFTEST: CLEAN`. The single-attempt fixture is also not faithful to the log it is
labelled after.

Smallest fix: duplicate the `Reading`/`Untested`/`Missing` block in `shfmt_like`
(with the second analyzer error) and add `"bootstrap_attempts": 2` to that case's
checks; add `"bootstrap_attempts": 1` to `snapshot_loaded`.

### B4 — LOW — the only hand-written expectation about the count is never compared, and is vacuous

Target: `.ufo/waves/round-17/predictions/pro-esbuild-0.27.7.prediction.json:17`
(`"bootstrap_attempts_at_least": 1`) and
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:83` ("The hand prediction
matched.").

Command and output:

```
$ grep -c extra_expectations .ufo/waves/round-17/tools/compare.py
0
$ python3 -B -c "import json;d=json.load(open('.ufo/waves/round-17/runs/pro-esbuild-0.27.7/compare.json'));print([f['field'] for f in d['fields']])"
['untested_version', 'snapshot_label', 'missing_bootstrap', 'snapshot_route', 'fallback_to']
```

`compare.py` compares only `expected.*` (`FIELDS` at `:39`, `ROUTE_FIELDS` at `:43`,
loop at `:144`); `extra_expectations` has no consumer. The extra expectation would
also be satisfied by any count ≥ 1, including 1, so it cannot confirm the observed 2.
This corroborates `w2/DraftLessonEvidence.md:56` (same root, different emphasis) and
is repeated here because it is the only prediction statement touching this field.

Why it matters: the calibration claim "predicted before the run, then matched" is
narrower than stated for this run; the matched fields are the five `expected` fields.

Smallest fix: either teach `compare.py` to evaluate `extra_expectations` (and retain
a re-run `compare.json`), or mark the extras "not compared" in the entry and state
that `at_least: 1` is lower-bound, not discriminating.

### B5 — LOW — `bootstrap_attempts` is undocumented and its name overstates what it counts

Target: `tools/log-extract.py:10-14` (emitted-key list) and the field itself
(`:246`); `contract.md` has no definition of the field.

The docstring's emitted-key list omits `bootstrap_attempts` (as well as
`snapshot_fallbacks`, `snapshot_route`, `mapper_errors`, `invalid_version_strings`),
and nothing in the round defines it. The name says "bootstrap", but the counter
increments before any Go check (`GoRttiMapper.java:106`), including the route where
`getGoBinary` returns null at `:160-162` with no build info at all. Concrete case:
`runs/pro-esbuild-0.27.7/observation.json:7` has `"bootstrap_attempts": 2` while
`missing_bootstrap` is `false` and the log has no `Untested`/`Missing` lines
(`runs/pro-esbuild-0.27.7/logs/rea-ghidra-DjvEp2/ghidra.log:63-69`). Zero bootstraps
were attempted there; two mapper reads were.

Why it matters: the field is quoted in evidence prose (knowledge `:76`) and in a
prediction (`:17`). A name that implies retries or bootstraps invites exactly the
misreading this report had to rule out.

Smallest fix: define it in the `log-extract.py` docstring and in the knowledge entry
as "count of `Reading Go binary info` records = `getSharedGoBinary` cache-miss
supplier invocations; on failure one per caller (two analyzers here; one per Go
function if DWARF is present); not a retry count and not evidence that a bootstrap
ran".

## 5. Bounded no-findings

Checked and clean:

- **Value correctness.** All 8 observation values reconcile exactly with a direct
  recount of the retained logs (§2). No off-by-one.
- **Single emitter.** `grep -rn "Reading Go binary info" /tmp/r17rb/all/` matches only
  `GoRttiMapper.java:106`; the counted component can only be `GoRttiMapper`.
- **Caller exhaustiveness.** Full Base source, Base.jar class pools, and all 195
  installed jars agree: three call sites only (§3). No analyzer outside the two
  named ones and the DWARF fixup can raise the count.
- **Ordering.** Symbol analyzer runs at `FORMAT_ANALYSIS.after().after()`
  (`GolangSymbolAnalyzer.java:74-75`), the string analyzer after
  `REFERENCE_ANALYSIS` (`:76-79`); logs show the symbol error before the string
  error in every failure run. No inversion.
- **Failure-route purity in these runs.** No `Failed to read Go info`, no
  `Invalid Go version string` in any of the 8 logs; failures are the constructor's
  `BootstrapInfoException` (three carriers) or the no-build-info null (esbuild
  0.27.7). So the two-block pattern is not a mixed-route artifact.
- **Second analysis pass.** `ANALYZING changes made by post scripts` adds no
  `Reading` line in any retained log, including after `GoRttiMapper.close()` dropped
  the cached instance. The 1/2 values are stable across the pass within these runs.
- **Knowledge anchor.** `TransientProgramProperties.java:107-110` is exact for the
  null-not-cached mechanism (no finding; listed to close the anchor check).

## 6. Residual unknowns

- The magnitude of the DWARF-path retry (`GolangDWARFFunctionFixup`) is INFERENCE
  only: no retained run loaded DWARF, and running Ghidra is outside this lane.
- Whether an AutoAnalysisManager second session that *does* re-schedule a Go
  analyzer would add another attempt on top of these values is source-inferable
  (cache cleared at `TransientProgramProperties.java:160-169`, null never cached) but
  not observed; the post-script pass in these runs did not re-schedule them.
- The count's behaviour for a successful mapper whose `init()` throws `IOException`
  (route D) is source-read only; no run exercised it.

## 7. Provenance

- No tool installed or upgraded (nothing to record).
- Read-only commands only: `unzip`, `grep`, `sed`, `javap`, and
  `python3 -I -B …/tools/log-extract.py` on retained logs and a `/tmp` fixture.
  Scratch under `/tmp/r17rb`; the only lane write is this report.
- Ghidra source: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
  (`unzip -l`: 2026-09-21 members; `GoRttiMapper.java` 41672 B, `TransientProgramProperties.java`
  6824 B, `GolangSymbolAnalyzer.java` 52666 B, `GolangStringAnalyzer.java` 14422 B).
- REA: 6.5.0 (npm package version read from
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`).
