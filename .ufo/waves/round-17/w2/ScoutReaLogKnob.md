# Scout — does a newer rea-agents release add a knob that retains `ghidra.log`?

**Question (target).** Check whether a newer release than the pinned `rea-agents@6.5.0` adds a knob to
retain the Ghidra session log (`ghidra.log` / `script.log`) — env var, CLI option, or MCP parameter.
Read-only; no client-config change.

**Verdict: BOUNDED NO-FINDING.** The newest published release is `rea-agents@6.7.0`
(2026-10-18T08:12:05Z); it has **no** log-retention knob and its log lifecycle is byte-for-byte the
6.5.0 lifecycle. No release newer than 6.7.0 exists as of 2026-10-20. C2's premise ("REA deletes its
Ghidra runtime root at session close") therefore holds at the latest release too, so upgrading is
**not** an alternative to the round-17 retained-log capability.

All version facts below are [OBSERVATION] from the public tarballs and the live CLI; inference is
labelled.

## 1. Releases (observed)

```
$ npm view rea-agents versions --json      # tail
  … "6.4.0", "6.5.0", "6.7.0"
$ npm view rea-agents dist-tags --json
{ "latest": "6.7.0" }
$ npm view rea-agents time --json          # selected
6.5.0 2026-10-14T12:56:14.513Z
6.7.0 2026-10-18T08:12:05.640Z
```
No `6.6.0` is published; `modified` = 2026-10-18T08:12:05Z, i.e. nothing newer than 6.7.0 as of
2026-10-20. Tarball `npm pack rea-agents@6.7.0` = 1775 files, unpacked under `/tmp/rea67/package`;
6.5.0 under `/tmp/rea65/package`.

## 2. What I grepped in 6.7.0, and what came back

Every command below was run in `/tmp/rea67/package` (public tarball), read-only.

| Check | Command | Output |
|---|---|---|
| log path sites | `grep -rn "ghidra\.log" .` | `dist/ghidra/GhidraLauncher.js:534`, `dist/cli-runtime/binary-CWVNJhAC.js:4200`, `dist/mcp/main-Cx-Z7m_n.js:7682` (last two are bundle copies) |
| log path literal | `sed -n '525,536p' dist/ghidra/GhidraLauncher.js` | `ghidraLogPath: join(runtimeRoot, "ghidra.log"),` / `scriptLogPath: join(runtimeRoot, "script.log"),` |
| `-log` still fixed + unconditional | `grep -n '"-readOnly"\|"-deleteProject"\|"-log"\|"-scriptlog"' dist/ghidra/GhidraLauncher.js` | `465:-readOnly`, `466:-deleteProject`, `467:"-log"`, `468:options.ghidraLogPath`, `469:"-scriptlog"`, `470:options.scriptLogPath` |
| env-var knob inventory | `grep -rho "REA_[A-Z0-9_]*" dist bridge scripts \| sort -u` | 6 Ghidra vars only: `REA_GHIDRA_{LANGUAGE_ID,SEED_FILE,COMPILER_SPEC_ID,NATIVEAOT_JAR,DISABLED_ANALYZERS,STARTUP_TIMEOUT_MS}`. No log-path, retain, keep, temp-dir or runtime-root variable exists. The only LOG-named var is `REA_LOG_LEVEL` (`dist/config/environment.js:59-61`), REA's own logger level — it does not create or preserve `ghidra.log` |
| CLI option literals | `grep -rhoE '"--[a-z0-9-]*(log\|keep\|retain\|temp\|runtime)[a-z0-9-]*"' dist/*.js dist/*/*.js \| sort -u` | single hit `"--log"`, and it is binwalk/unblob (`dist/firmware/FirmwareProvider.js:255,294`), not Ghidra |
| help surface | `npx -y rea-agents@6.7.0 --help` vs `@6.5.0`, diff | only the banner (`rea@6.5.0` → `rea@6.7.0`); command block 153/153, **identical command lists** (`awk` block count + `diff` of names → `IDENTICAL_COMMAND_LIST`) |
| command schema | `npx -y rea-agents@6.7.0 analyze --schema` vs `@6.5.0` | one line: `enum[5]: "6502",x86,x86_64,arm,arm64` → `enum[6]: … ,m68k`. No option added |
| agent docs | `npx -y rea-agents@6.7.0 --llms-full \| grep -inE "ghidra_log\|ghidra\.log\|runtime root\|rea-ghidra\|retain.*(log\|runtime)"` | only an unrelated HAR/mitmproxy help line; no log-retention wording |
| deletion mechanism | `diff -u /tmp/rea65/package/dist/process/PrivateRuntimeRoot.js /tmp/rea67/package/dist/process/PrivateRuntimeRoot.js` | **empty diff**; POSIX `close()` at `dist/process/PrivateRuntimeRoot.js:47-50` = `rm(this.path, { recursive: true, force: true })` |
| root removal caller | `grep -n "async #removeRuntimeRoots" dist/ghidra/GhidraClient.js` | `779` (6.7.0) / `638` (6.5.0) — same "keep only roots that could not be removed" logic |
| does anything read the log back? | `grep -rn "readFile" dist/ghidra/*.js` | no output — the only consumer of the path is `ghidra_log_path` in `dist/ghidra/GhidraDiagnostics.js:36` |
| diagnostics exposure | `grep -rn "ghidra_log_path" dist/` | `GhidraDiagnostics.js:36` + two bundle copies; surfaced only as `provider_diagnostics` on failure/cleanup errors (`dist/mcp/main-Cx-Z7m_n.js:3047`), never in a success result |

[INFERENCE from the rows above] The only ways the log outlives a session remain the two wave-1 already
named (`w1/ScoutReaRuntimeRoot.md: §3`): failed cleanup fail-closed retention, and abnormal
termination. Neither is a knob.

### 2.1 What 6.7.0 *did* add next to the log (and why it is not a substitute)

`diff -u` of `dist/ghidra/GhidraDiagnostics.js` (6.5.0 → 6.7.0) adds
`configured_jvm_max_heap` and `failure_output`; `GhidraClient.js:885-890` builds `failure_output` from
`stdout`/`stderr` since a checkpoint — **headless-process streams, not the `-log` file**. So even the
new failure diagnostics carry no `ghidra.log` bytes.

Depth check on the success path (the case C2 needs): the retained pilot analyze JSON has no
diagnostics at all
```
$ python3 -B -c "import json; d=json.load(open('pilot/esb.json')); print(list(d.keys())); print('diagnostics' in d)"
['evidence_id','subject','provider','analysis_profile','predicate_type','operation','parameters',
 'raw_result','normalized_result','confidence','authority','environment','limitations',
 'relationship_coverage','locations','evidence_links']
False
$ wc -l pilot/esb.err pilot/shfmt.err
0 pilot/esb.err
0 pilot/shfmt.err
```
and `ghidra_log_path`/`GoRttiMapper` do not occur in that JSON. [OBSERVATION] On a successful
`analyze`, REA emits neither the path nor the log content; the poll-copy in
`tools/carrier-run.py:192-240` remains the only route. [INFERENCE] An upgrade would buy nothing for C2
unless REA changes this, and 6.7.0 did not.

## 3. Findings against the round-17 artifacts

**F1 (low, calibration) — `w1/ScoutReaRuntimeRoot.md:7`: verdict is written unqualified while the
scope at `:3` is `rea-agents@6.5.0`.**
`:7` reads `**Verdict: CONFIRMED — "no knob retains ghidra.log".**`. My check shows the verdict also
holds at 6.7.0 (latest), so the finding is an under-claim of scope, not an error.
*Smallest fix:* append the version range — `… no knob retains ghidra.log at 6.5.0 or at 6.7.0
(latest, published 2026-10-18T08:12Z).`

**F2 (info, integration input, not a defect) — `w1/ConnAdjacencyReport.md:122-123` leaves this open.**
`:122-123` reads `Whether 6.7.0 changes analyzer component names or the unretained env knobs is
**unknown** — do not claim either way.` Half of that unknown is now determined: the 6.7.0 knob set and
log lifecycle are unchanged (§2). Analyzer *component names* remain unverified.
*Smallest fix:* in the entry, if the lifecycle is stated, add `unchanged in 6.7.0
(GhidraLauncher.js:525-535, 467-470; PrivateRuntimeRoot.js:47-50)`; keep 6.5.0 as the run pin.

**F3 (low) — `pilot/README.txt:5` supports "no keep knob found" with one `REA_GHIDRA_` grep.**
A single prefix-scoped grep cannot exclude non-prefixed inputs, and the scout's own §4 notes `TMPDIR`
changes *where* the root appears; the pilot line is weaker evidence than the report it feeds.
*Smallest fix:* replace the parenthetical with `no keep knob found — see w1/ScoutReaRuntimeRoot.md §4
(now also checked at 6.7.0: w2/ScoutReaLogKnob.md)`.

**F4 (info, no defect) — `SKILL.md:19-20` command counts re-verified, with a counting pitfall.**
The row claims `153 CLI commands` for both versions. Reproduced exactly:
```
$ npx -y rea-agents@6.5.0 --help > /tmp/full65.txt   # likewise @6.7.0 > /tmp/full67.txt
$ for f in /tmp/full65.txt /tmp/full67.txt; do awk '/^Commands:/{f=1;next} f&&/^$/{exit} f&&/^  [a-z]/{n++} END{print FILENAME": "n}' "$f"; done
/tmp/full65.txt: 153
/tmp/full67.txt: 153
```
A naive `grep -cE '^  [a-z][a-z0-9-]+ '` returns **155** because it also matches two lines outside the
`Commands:` block — a ready-made false finding for the next reviewer. Record the `awk` method (or drop
the integer). The `207 MCP tools` half was not re-derived (needs an MCP `tools/list`; not run).
*Smallest fix:* none required; if the count is cited again, cite the block-scoped method.

## 4. Anchor transfer (calibration)

Wave-1 cites the *installed* npx cache. I verified the cache and the public tarball are the same bytes,
so those anchors are reproducible from `npm pack`:
```
$ diff -r --brief /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist /tmp/rea65/package/dist
(no output, exit 0)
$ sed -n '449p' <cache>/dist/ghidra/GhidraLauncher.js
    ghidraLogPath: join(runtimeRoot, "ghidra.log"),
```
[OBSERVATION] `w1/ScoutReaRuntimeRoot.md` §2 `:449`/`:450` and §3 `PrivateRuntimeRoot.js:49` reproduce
exactly on both copies.

## 5. Residual unknowns (bounded)

Not checked, stated so the no-finding is not read wider than it is: the Windows branch
(`WindowsPrivateRuntime.close()`, `PrivateRuntimeRoot.js:50`) — POSIX lane only; the `207 MCP tools`
figure (§3 F4); upstream Ghidra 12.1.4 `-log` semantics (not re-derived; wave-1 read them from
`Base-src.zip` and 6.7.0 passes the same flag at `GhidraLauncher.js:467-470`); no 6.7.0 source maps
inspected.

## 6. Hygiene

Read-only attack: no `rea analyze/search/decompile`, no `analyzeHeadless`, no carrier executed; no
client config or repo file touched except this report. Python ran with `-B`; scratch under `/tmp`
(`rea65/`, `rea67/`, `h65.txt`, `h67.txt`, `a65.json`, `a67.json`, `full65.txt`, `full67.txt`).
One tool materialization: `rea-agents@6.7.0` via `npx -y` into the npx cache (channel `npx`; reason:
read the newest published release for this question; installed `--version` reports `6.7.0`). No
`pacman`, no upgrades.
