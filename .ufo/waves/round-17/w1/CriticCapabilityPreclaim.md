# CriticCapabilityPreclaim — r17 capability row "retained REA Ghidra-session log capture"

Seat: author-side advisory critic (KaidokuR17.CriticCapabilityPreclaim-3). Read-only, apart from this report. Axes: calibration, depth.
Installs: none. I did not run REA, Ghidra, or any carrier. The only reads of carrier bytes were `md5sum` and `sha256sum` of the two pilot carriers.
Scratch: one stdlib simulation under `tempfile.mkdtemp()` (removed afterwards), plus a temporary extract of `HeadlessAnalyzer.java` (removed afterwards).

## Verdict

As drafted, the row would pre-claim. Polling copy is enough to retain the **early Go analyzer lines** in the two pilots, but it is not robust enough to be called a log-capture capability without three changes:

1. The entry gate must be able to fail on a provenance error.
2. A poll must never shrink the retained bytes.
3. The row must carry a limitations list that is longer than "final-poll lines may be missing".

There is also a cheap stdlib alternative that removes the main tail limitation (F4).

## Findings

### F1 — The entry gate cannot fail on wrong provenance (calibration; fixable defect)
- **Counterexample.** Copy `pilot/esbuild-0.25.12-log/ghidra.log` into a shfmt run directory and record its sha256 in the receipt.
  - `receipt-validate.py` checks only recomputed file sha256, `pins.compare` and required fields (`contract.md:106-108`). It would exit 0.
  - The draft gate is exactly that exit (`w1/draft-scorecard.md:46`).
  - So the gate proves the retained bytes are unchanged since receipt time. It does not prove they came from this carrier's session.
- **Evidence (observation): the log binds itself to the carrier in three ways.**
  - Path: `Using log file: /tmp/rea-ghidra-LuPZRm/ghidra.log` (`pilot/shfmt-log/ghidra.log:2`) must equal the recorded `session_dir`.
  - Name: the target is named `target-<sha256[:12]>.bin` (`shfmt-log/ghidra.log:46`; `esbuild-0.25.12-log/ghidra.log:62`).
  - Full MD5: the `Loading file:///…target-….bin?MD5=…` line carries the full MD5 of the target.
    - `shfmt-log/ghidra.log:64` has `MD5=caacf2c8df03f63b98119ef107020070`. That equals `md5sum /usr/bin/shfmt`, whose sha256 `58f76563…` matches `pilot/README.txt:7`.
    - `esbuild-0.25.12-log/ghidra.log:55` has `MD5=c060104521b3b6f0f541461f53ab1717`. That equals `md5sum` of the pinned esbuild.
  - `w1/draft-knowledge-r17.md:21` says the binding runs only through the SHA-256 pin. That is incomplete: the full MD5 is an independent in-log binding.
- **Smallest correction.** Add binding checks to the validator: session_dir == logged path; 12-hex prefix == `carrier.sha256[:12]`; logged MD5 == md5 of the pre-pinned carrier.
  - Make it exit 1 on any mismatch.
  - Retain one red control: a swapped log, which must exit 1. This matches C1's own "shown able to fail" standard (`claims.json:12-13`, `contract.md:18-19`).
  - Without the red case, "receipt validates" is a vacuous gate for a provenance-bearing row.

### F2 — Zero or foreign session directories still give exit 0 (calibration; fixable defect)
- **Hard-coded location.** `carrier-run.py` watches `/tmp/rea-ghidra-*` (`contract.md:36`). REA instead creates the root under `os.tmpdir()`, falling back to `/tmp` only when the path has a dot-prefixed element:
  - `rea-agents/dist/ghidra/GhidraSessionRoot.js:28-37` (session-root logic);
  - `GhidraClient.js:32,395-398` (`prefix: "rea-ghidra-"`).
  - With a non-dot `TMPDIR` such as `/run/user/1000`, the watcher sees no new directories.
  - The contract exits 0 when "all steps ran" (`contract.md:48`), and nothing requires at least one retained log. The result is a silently empty capture.
  - `TMPDIR` is unset in this seat. The env of other seats was not observed.
- **Attribution.** Each `--search` step starts its own Ghidra session (`contract.md:40-41`). Other lanes, or any seat's selftest fixture named `rea-ghidra-*` in `/tmp`, can add directories during the run. "Every NEW dir" (`contract.md:37-38`) cannot attribute directories to steps.
- **Smallest correction.**
  - Take the before/after directory sets per step.
  - Require exactly one new root per REA step whose log passes the F1 binding; otherwise exit 2.
  - Record `TMPDIR` and the resolved session parent in the receipt.
  - Give the tool `--session-parent`, defaulting to the GhidraSessionRoot rule, so `--selftest` uses its own mkdtemp parent and never creates `rea-ghidra-*` in the real `/tmp`.

### F3 — Poll-by-replace can delete the Go lines it already retained (depth/calibration; fixable defect)
- **Evidence (observation): rotation is configured.** Ghidra's detail appender is a `RollingFile` with `SizeBasedTriggeringPolicy size="50000 KB"` and `filePattern="${sys:logFilename}-%d{yyyy-MM-dd}-%i.log"`. Source: `Ghidra/Framework/Generic/lib/Generic.jar` member `log4j-appender-rolling-file.xml`; the script log has the same policy in `log4j-appender-rolling-file-scripts.xml`.
- **Why the copy loses data.** The contract copies only `ghidra.log`/`script.log` and overwrites with `os.replace` on every poll (`contract.md:37-39`). After a rollover, the next poll replaces the retained copy, which holds the early `GoRttiMapper` lines, with the post-roll file. The Go diagnostics are then gone from the retained copy.
- **Simulation (observation; a mechanism test, not REA behavior).** 40-line writer at 50 ms, 0.5 s poller with copy + `os.replace`, rotation at line 20, then `rm -rf` of the root. In 3/3 trials the polled copy held 20 lines, was not a prefix of the true log, and had no Go line.
- **Scope.** The pilots are 11 KB (`wc -c`: 11207 / 10973), far below 50 MB. For large carriers this is a risk ([INFERENCE]), not something observed.
- **Smallest correction.**
  - Copy `ghidra.log*` and `script.log*`.
  - Accept a new poll only if the previous retained copy is a byte prefix of it. Otherwise keep both copies and set `rotation_or_truncation_detected`.
  - Drop a final line that lacks `\n` (torn write).

### F4 — Polling tail loss is real; an unstated limit and a cheap fix exist (calibration + depth)
- **Evidence (observation): the two pilot captures stop at different lifecycle points.**
  - shfmt ends at `ANALYZING changes made by post scripts` (`shfmt-log/ghidra.log:125`). Per `HeadlessAnalyzer.java:1121-1130` (Base-src.zip), Ghidra logs that line only after all post-scripts have returned, which includes the bridge.
  - esbuild ends at `SCRIPT: …ReaGhidraBridge.java` (`esbuild-0.25.12-log/ghidra.log:123`), before the bridge returned.
  - So the esbuild copy likely missed at least the post-script line ([INFERENCE]: it would have been emitted unless the JVM was killed first).
- **Completeness cannot be attested, even with perfect capture (observation).** On close, REA sends `shutdown`, then `waitForExit(500)`, then `process.stop()` (`GhidraClient.js:591-593`). `stop()` sends SIGTERM, waits 250 ms, then SIGKILL (`dist/process/ProviderProcess.js:4-5,289-293`). Only after that does it `rm -rf` the root (`GhidraClient.js` `#removeRuntimeRoots`; `dist/process/PrivateRuntimeRoot.js` `rm(..., {recursive, force})`).
  - So `REPORT: Post-analysis succeeded` (`HeadlessAnalyzer.java:1130`) may never be written.
  - No end-of-log marker exists. A short tail cannot be told apart from capture loss, so the row must not say "complete log".
- **What absence claims remain sound.** A retained copy (with the F3 prefix rule) is a prefix of the log. Absence is therefore sound only for lines that would precede the last retained line.
  - Both pilots retain `REPORT: Analysis succeeded for file:` (`shfmt-log/ghidra.log:119`; `esbuild-0.25.12-log/ghidra.log:118`), Ghidra's end-of-analysis line (`HeadlessAnalyzer.java:1054/1077`).
  - So "no `Untested Go version` for esbuild" is window-valid.
  - Go lines emitted during post-script re-analysis (`HeadlessAnalyzer.java:1123-1125`, which calls `startAnalysis` again) fall outside that guarantee ([INFERENCE]).
  - `log-extract.py` should emit `analysis_succeeded_present` plus `last_line_timestamp`. `compare.py` should report `could_not_evaluate` (exit 2) for the absence-based fields `untested_version: []` and `missing_bootstrap: false` when the marker is missing.
- **Cheap stronger capture (simulation-backed).**
  - Open each `ghidra.log*`/`script.log*` once it appears and hold the fd. Read incrementally; after the `npx` child exits, read to EOF; record `os.fstat(fd).st_nlink == 0` as proof that capture outlived REA's deletion.
  - This works because REA stops the JVM before deleting the root, so every write lands before the unlink. Linux unlink does not invalidate open fds, and a rename on rotation keeps the inode.
  - The same simulation, 6/6 trials, rotation and no rotation:
    - Held-fd capture got 40/40 lines every time.
    - Polling got 31/40, 40/40, 40/40 without rotation, and 20/40 with no Go lines under rotation.
  - Python stdlib only. It reads only, so it stays within the "never touch other dirs' files beyond reading" rule (`contract.md:39`).
  - It turns the limitation from "tail may be missing" into "complete up to JVM death; JVM death point is REA-controlled".

### F5 — Pilot cannot be the demonstration; the evidence pointer must be standalone (calibration; tradeoff the judge must enforce)
- **Pilot status.** The pilot is explicitly "NOT the final measured runs", with no pins and no poll receipts (`pilot/README.txt:1,6`). Its polls and last-copy times are unrecorded, so tail loss cannot be bounded from it.
- **The rule.** `AXES.md:62-64` says a capability without a passing demonstration in the round report is pre-claiming.
- **Lane precedent** refused rows for "round infrastructure, not yet a demonstrated standalone capability" (`SCORECARD.md:1089-1090,1093-1094`). The r14 row cites a selftest and a frozen run (`SCORECARD.md:2207`).
- **Minimum demonstration for entry:**
  - (a) `carrier-run.py --selftest` CLEAN with a fixture that writes, rotates and deletes in its own mkdtemp parent, including red cases: zero roots → exit 2; foreign or swapped log → exit 1; rotation → no loss.
  - (b) At least one final L1 run per carrier class: out-of-range shfmt, plus at least one in-range esbuild. Receipts must have pins pre/post equal, exactly one bound session root per REA step, logs with sha256, polls and `last_copy_utc`, and `analysis_succeeded_present` true.
  - (c) `receipt-validate.py` exits 0 on those receipts and 1 on the retained swapped-log control.
  - (d) A non-zero REA exit is recorded and still counts as capture if the log is bound. The row is about capture, not analysis success.
- **Draft row.** Its evidence pointer (`w1/draft-scorecard.md:44`) gives a re-run argv that is a full carrier analysis; per this contract only L1 may run it. Point first at the receipt and the validator commands, and keep the argv as provenance.

### F6 — Scope/limitation text the row must carry (calibration)
`w1/draft-scorecard.md:44` currently says only "polling copy, final-poll lines may be missing". Add the following, compressed if needed:
- **(i) Not complete.** It is a byte prefix up to the last poll (or to JVM death with held fds). REA SIGTERMs/SIGKILLs the JVM after 500 ms, so there is no end marker. Absence claims are valid only before the last retained line or the `Analysis succeeded` marker.
- **(ii) Side channel.** It reads REA 6.5.0's private 0700 runtime root, which is an undocumented internal: prefix `rea-ghidra-`, filenames from `GhidraLauncher.js:449-450`, `-log`/`-scriptlog` at `:382-385`, no keep knob (`pilot/README.txt:5`). Re-verify per REA and Ghidra pin; this is not a REA-supported surface.
- **(iii) Outside the Evidence.** The log is not part of REA Evidence. The evidence-id ↔ log link is asserted by the receipt (step window + in-log path, sha prefix and MD5 binding), not cryptographically bound by REA.
- **(iv) POSIX tmpdir-resolved roots only.** The session parent follows `TMPDIR`; Windows DACL roots are out of scope.
- **(v) Copy only the two logs.** Never copy `session.json`, which carries the bridge bearer token (`GhidraLauncher.js:94-98`, `token: session.token`). The pilot logs contain no 64-hex string (grep count 0/0).
- **Name.** Keep the measured name `retained REA Ghidra-session log capture` verbatim (`contract.md:117-118`). Move "for caller-selected Go carriers" into the description, because the capture is carrier-agnostic and the Go comparison is C2's knowledge result, not the capability.

### F7 — Side finding: the extractor drops Go diagnostics (depth; adjacent to scope)
- `contract.md:56-58` keeps only `Go*`/`Golang*` components. esbuild's Go-relevant lines come from `(PropagateRttiBackgroundCommand) Go RTTI callsite fixup info …` (`esbuild-0.25.12-log/ghidra.log:80`) and `(FixClosureFuncArgsBackgroundCommand) Go closure/method wrapper …` (`:81-82`). Both are dropped.
- Also include message-prefix `Go ` lines, or list these components. That way "observed" is not narrower than what the log shows.

## Impacted axes
- **Calibration:** F1, F2, F4, F5, F6 — the gate passes on wrong or empty provenance, and the limitation is understated.
- **Depth:** F3, F4, F7 — Go lines can be destroyed or filtered, and absence claims can go beyond the window.
- These are fixable defects, not tradeoffs, except F5's "pilot ≠ demonstration", which the judge must enforce as written.

## Searched (bounded)
- `claims.json`, `contract.md`, and the pilot artifacts (`sha256sum -c` OK 6/6).
- `w1/draft-scorecard.md`, `w1/draft-knowledge-r17.md`, `w1/ConnCapabilityHistory.md`.
- `SCORECARD.md` capability history; `AXES.md:57-64`.
- `rea-agents` 6.5.0 dist: GhidraClient, GhidraLauncher, GhidraSessionRoot, GhidraDiagnostics, PrivateRuntimeRoot, ProviderProcess.
- Ghidra 12.1.4 `HeadlessAnalyzer.java` (Base-src.zip) and the `Generic.jar` log4j configs.
- Not searched: a REA flag that preserves the root (pilot README says none; not re-verified beyond the dist reads above).
