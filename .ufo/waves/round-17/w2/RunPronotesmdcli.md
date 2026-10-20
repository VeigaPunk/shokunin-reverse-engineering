# RunPronotesmdcli — attack on `runs/pro-notesmd-cli/` (W2 falsify)

**Target.** `.ufo/waves/round-17/runs/pro-notesmd-cli/` (carrier `/home/vgpnk/.local/bin/notesmd-cli`,
sha256 `412dc532d278b9e4…`, go1.25.8) at lane rev
`da64646adcb19c1ede7537b799b8c7d283fe43da`; predictions frozen at
`271167473d87ef710f07ecdd98caf0ce12091686`. Read-only: no REA `analyze`/`search`/`decompile`, no
Ghidra, no carrier execution. All commands below were run as shown (a leading `…/` abbreviates an
already-spelled absolute path; nothing else is elided); outputs are quoted, not paraphrased. Tool
installs/updates: **none**.

## Verdict

The **provenance chain for this run holds** (§3, bounded no-finding). The **receiving gate fails on
every retained receipt**, this one included, from a producer/validator shape disagreement — a
cross-run defect already reached independently by other W2 lanes; this lane adds the equivalence
proof that the receipt's *data* is valid and only the validator's shape branch is wrong (F1).

| Assigned check | Result |
|---|---|
| `receipt-validate.py runs/pro-notesmd-cli/receipt.json` | **FAIL — exit 1, `unrecognized_shape`** (F1, cross-run) |
| log contains `Using log file: <session>/ghidra.log` | PASS — `ghidra.log:2`, exact `/tmp/kr17-rea-odi4abuq/rea-ghidra-eKKJuy` |
| log contains `IMPORTING: file://<session>/target-<sha[:12]>.bin` | PASS — `ghidra.log:46`, `target-412dc532d278.bin` = `carrier.sha256[:12]` |
| prediction bytes == `git show 2711674:…/pro-notesmd-cli.prediction.json` | PASS — both `54042da375b99e28…` |
| freeze commit time < receipt analyze `started_at_utc` | PASS — `13:46:45Z` < `13:49:25.022848Z` |
| fresh `log-extract.py` vs retained `observation.json` | PASS — byte-identical `cfe2d680c114a586…` |
| fresh `compare.py` vs frozen prediction | PASS — exit 0, 5/5 fields match |
| retained `compare.json` reproduced from pinned inputs | PASS — byte-identical `c4223f4c748afcf8…` |
| knowledge row `pro-notesmd-cli` matches log | PASS — sha prefix, go1.25.8, fallback→1.25.0, 2302 types, `ev_4fd342dd…` all match |
| canonical runtime | PASS — `rea-agents@6.5.0`, Ghidra `12.1.4` (one version each) |

---

## 1. Findings

### F1 — HIGH (calibration; cross-run, blocking): the run's own validator rejects the run's receipt

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
    .ufo/waves/round-17/runs/pro-notesmd-cli/receipt.json
{ "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0},
  "exit": 1,
  "receipts": [{ "checks_performed": 306,
                 "findings": [{ "code": "unrecognized_shape",
                                "detail": "receipt matches neither retain nor carrier shape",
                                "where": "$" }],
                 "kind": "unknown", "status": "invalid", "valid": false }] }
```

All eight retained receipts are the same shape — `"steps"` is a **dict** keyed by step name
(`receipt.json:1826`; keys `analyze`, `inspect-go-binary`). The validator's `classify()` returns
`carrier` only when `isinstance(receipt.get("steps"), list)` (`receipt-validate.py:98-101`), then
iterates the list at `:284`. The producer writes `"steps": {}` and assigns the dict
(`carrier-run.py:275,349`). The validator's own selftest fixture builds a **list**
(`_carrier_receipt`, `receipt-validate.py:459-476`), so the tool's own selftest is green
(`w1/ReceiptValidateTool.md:19` records `SELFTEST: CLEAN cases=5`) while the product it validates is
red. W1 saw the risk and mis-costed it: “if CarrierRunTool diverges,
validation yields `missing_field` findings rather than exit 2” (`w1/ReceiptValidateTool.md:22`); the
actual outcome is `kind: unknown` before any field check.

**Equivalence proof (this lane's addition).** Copying the receipt to `/tmp` and converting only
`steps` from dict to list (values unchanged, `name` added), then rerunning:

```
$ python3 -I -B …/receipt-validate.py /tmp/r17-pronotes-receipt-as-list.json
{ "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "exit": 0,
  "receipts": [{ "checks_performed": 336, "findings": [], "kind": "carrier",
                 "status": "valid", "valid": true }] }
```

So every recorded digest, size and pins compare already passes (the 306 real checks produced no
sha/size finding); only the shape branch blocks. This is a validator defect, not tampering.

**Why it is claim-level, not cosmetic.** `claims.json:22` admits the capability row “only if the
capture runs and its receipt validates”; `w1/ConnCapabilityHistory.md:70` and `:91` define that as
“each `receipt-validate.py` exit 0”; `w1/draft-scorecard.md:46` repeats “Exit 0 … Otherwise no row is
added”. The knowledge entry's `recheck:` line (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`)
prescribes exactly the failing command. As shipped, C2's before→after is unmet on all 8/8 runs.

**Smallest fix** (no re-runs, no receipt regeneration): in `receipt-validate.py`, accept a mapping in
`classify()` (`isinstance(receipt.get("steps"), (list, dict))`) and, before the `:284` loop, normalize
`steps = list(steps.values()) if isinstance(steps, dict) else steps`; add one selftest case with the
keyed shape. Rewriting `carrier-run.py` to emit a list would invalidate the eight committed receipts
and require eight new REA analyses.

*Cross-run: independently reported by `w2/RunProaether.md` F1 and `w2/DraftLessonEvidence.md` F1. This
lane's list-shape run is the added evidence that the data itself validates.*

### F2 — MEDIUM-LOW (depth; cross-run): “no mid-run check differed” has no positive retained artifact

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:26-30` says the 146 paths were hashed
“before, every 30 s during, and after each session” and “no mid-run check differed”. The receipt
retains `pins_pre`/`pins_post`/`pins_compare` only (`receipt.json:316,1060`); the `analyze` step
record has no pin field at all:

```
analyze step keys: ['argv','cwd','ended_at_utc','evidence_id','exit','polls','retained_logs',
                    'started_at_utc','stderr_path','stderr_sha256','stdout_path','stdout_sha256']
mid-run fields: {}
```

`carrier-run.py:422-433` takes the throttled snapshot (`PIN_CHECK_S = 30.0`, `:35`) but writes
`rec["pins_changed_during_run"]` **only on inequality**. Absence of that key is consistent with
“checks ran and agreed”, but a reader cannot distinguish it from “no check fired” without reading
tool source. That is the R16-PROVENANCE failure mode (a temporal/occurrence claim without a retained
instant) inside the entry written to close it; `:29-30` hedges continuity, not occurrence.

**Smallest fix:** persist `pin_checks: {count, first_utc, last_utc}` in each polled step record (the
loop already has `monotonic()`), or amend `:27-29` to “checked at 30 s intervals; a mismatch would be
recorded as `pins_changed_during_run` (`carrier-run.py:422-433`), absent here”.

*Cross-run: `w2/RunProaether.md` F2 reports the same shape for pro-aether.*

### F3 — MEDIUM-LOW (calibration; cross-run): the freeze commit is cited by an unresolvable hash

```
$ git rev-parse --verify 2716747
fatal: Needed a single revision            # exit 128
$ git rev-parse --verify 2711674
271167473d87ef710f07ecdd98caf0ce12091686   # exit 0
```

Two committed sites: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37` and
`.ufo/waves/round-17/run-carriers.sh:2`. The entry's own head (`:1`) has the full correct hash, so
head and body disagree; the driver's provenance comment cannot be resolved. This is precisely the
citation-drift class C1(b) exists to remove, in the round's headline artifacts (two files, so not a
one-off typo).

**Smallest fix:** replace `2716747` with `2711674` (or the full 40-hex hash) in both files.

*Cross-run: `w2/RunProaether.md` F3 reports the same two sites. Not double-counted; recorded here
because the knowledge row I was assigned to check sits in the same file.*

### F4 — LOW (calibration; cross-run): the recheck's second command destroys the evidence it rechecks

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3` says to rerun
`bash .ufo/waves/round-17/run-carriers.sh <label>` and compare `observation.json`. At the **lane
revision** the script has:

```
$ git show da64646:.ufo/waves/round-17/run-carriers.sh | nl -ba | sed -n '14,15p'
    14	  out="runs/$label"
    15	  rm -rf "$out"; mkdir -p "$out"
```

so following the recheck as written deletes and replaces the retained run (and repeats a full REA
analyze) before any comparison. The `RUNS_DIR` escape hatch is **not in `da64646`**: it exists only
as an uncommitted working-tree edit (`git status --porcelain` → `M .ufo/waves/round-17/run-carriers.sh`;
diff `-  out="runs/$label"` / `+  out="${RUNS_DIR:-runs}/$label"`).

**Smallest fix:** commit the `RUNS_DIR` change and amend `knowledge:3` to the read-only chain
(`receipt-validate.py` → `log-extract.py` → `compare.py` over retained files), with
`RUNS_DIR=/tmp/r17-recheck` only for the optional rerun. Until committed, copy the run dir first.

*Cross-run: `w2/RunProaether.md` F4 reports the recheck hazard; the revision/precision point above is
this lane's.*

### F5 — LOW (depth; gate coverage): `receipt-validate.py` never re-derives the log binding

```
$ grep -n "Using log file\|IMPORTING\|binding\|target-" .ufo/waves/round-17/tools/receipt-validate.py
$ echo $?
1            # no matches
```

The receipt asserts `retained_logs[0].binding = {logfile_ok: true, target_ok: true}`
(`receipt.json:1800-1802`) and `bound_sessions` length 1 (`:2`) / `unbound_sessions` empty (`:1887`),
but the validator only checks the retained file's digest via the generic walk — the two substring
tests live solely in `carrier-run.py:124-138`. For this run I verified the bytes by hand (§3, items
1-2), so the claim is true; the gap is that the “receipt validates” gate cannot detect a receipt
whose log is foreign or whose binding booleans are forged. W1 recommended exactly this hardening
(`w1/SentinelPollRace.md:70`) and it was not integrated.

**Smallest fix:** in `receipt-validate.py`'s carrier branch, for each retained session read
`ghidra.log` and assert `Using log file: <session_dir>/ghidra.log` and
`IMPORTING: file://<session_dir>/target-<carrier.sha256[:12]>.bin` (and that the receipt's booleans
match), as `carrier-run.py:124-138` already computes.

---

## 2. Calibration read (no defect)

For this carrier, `compare.json` reports 5/5 match, but the fields are not five independent tests.
`snapshot_label` is explicitly a request echo — `GoRttiMapper.java:179-180` logs
`apiSnapshot.getVer()`, and `GoApiSnapshot.read(..., ver)` stores the **requested** `goVer`
(`GoApiSnapshot.java:111,205`, `:492-501`), so the line appears after a fallback too. `fallback_to`
is entailed by `route=fallback` plus a patch-0 base; `untested_version:null` and
`missing_bootstrap:false` are in-range corollaries. The held-out, falsifiable bit is the **route**:
the WARN (`GoApiSnapshot.java:158-161`) proves a base JSON was found *and* no 1.25.x patch diff was
installed, which is exactly what `predict.py` selected from r16 (`status: base_only`). `compare.py`
discloses the echo (`compare.py:41-50`, `rules.snapshot_label`) and the knowledge entry repeats it
(`:33-36`), so `all_match:true` is honest, just weaker than a naive 5/5 reading. The alternative
routes would have produced different text (`info` INFO line, or `none` with no snapshot line), so the
test is real.

Independent pre-registration also exists, so the held-out claim does not rest on the prediction file
alone: `w1/CriticSampleSize.md` (mtime `10:38:33-03`, before the prediction file at `10:46:26`, the
first run at `10:47:06` and this run at `10:49:25`) records the exact expected signature — “WARN
`Falling back from 1.25.8 to
1.25.0 for Go API snapshot`, INFO `Using Go API snapshot for version 1.25.8`, no Untested, no
Missing bootstrap” — for this carrier (`:27`, `:78`), and `predictions/carriers.tsv:3` marks it
`prospective`. The observed `ghidra.log:68-69` matches that text verbatim.

## 3. Bounded no-finding — what was checked and found sound

1. **Self-identification of the log.** `ghidra.log:2` `Using log file:
   /tmp/kr17-rea-odi4abuq/rea-ghidra-eKKJuy/ghidra.log`; `:46` `IMPORTING:
   file:///tmp/kr17-rea-odi4abuq/rea-ghidra-eKKJuy/target-412dc532d278.bin`. `412dc532d278` is the
   first 12 hex of `carrier.sha256_pre/post` (`receipt.json:7-8`, both
   `412dc532d278b9e4aaf502891ea1f7b5c60e7572fb82935778ebdb728000802d`). `binding.logfile_ok` and
   `target_ok` true; `bound_sessions` 1, `unbound_sessions` 0.
2. **Prediction frozen before observation.** `sha256sum` of the working prediction and of
   `git show 2711674:…/pro-notesmd-cli.prediction.json` are both
   `54042da375b99e287488291ca4e59d208f31951f759cadde1da8a456a90ddeca`; the same blob is at
   `da64646`; commit `git show -s --format=%cI 2711674` → `2026-10-20T10:46:45-03:00` =
   `13:46:45Z`; `receipt.steps.analyze.started_at_utc` = `13:49:25.022848Z`; the freeze commit is an
   ancestor of `da64646` (`git merge-base --is-ancestor` → 0).
3. **Extraction reproducible.** `log-extract.py --log <retained ghidra.log>` → exit 0, output
   byte-identical to `observation.json` (`cfe2d680c114a586badf82809ad8b7e6d9b0c5c8698accec8b15a6a191ca5ff0`),
   `log_sha256 8904ab6e…`, `log_bytes 11897`, 20 Go lines, `snapshot_route fallback`,
   `snapshot_fallbacks [{from:1.25.8,to:1.25.0}]`, `snapshot_labels [1.25.8]`,
   `untested_versions []`, `missing_bootstrap false`, `analyzer_errors []`.
4. **Comparison reproducible, not just consistent.** From `cd .ufo/waves/round-17` with the retained
   relative argv, `compare.py --prediction predictions/pro-notesmd-cli.prediction.json --observation
   runs/pro-notesmd-cli/observation.json` → exit 0, 5/5 match, and **byte-identical** to the retained
   `compare.json` (`c4223f4c748afcf8870882302531a1ee8c4204bc42927170dba22434d8b6e01d`).
5. **Knowledge row matches the log** (the assigned row check):
   `ghidra.log:68` `WARN (GoApiSnapshot) Falling back from 1.25.8 to 1.25.0 for Go API snapshot`;
   `:69` `INFO (GoRttiMapper) Using Go API snapshot for version 1.25.8`; `:71` `Found 2302 Go types`;
   `:72` `Go version 1.25.8`; `:48` `Using Language/Compiler: x86:LE:64:default:golang`; no
   `Untested`, `Missing Go bootstrap`, `Go analysis failure`, or `ERROR` line (`grep` → NONE). Row
   sha prefix `412dc532d278b9e4`, route “fallback → 1.25.0”, “loaded; 2302 types”, and evidence id
   `ev_4fd342dd05bcf5a5da4d3574c09501bff856245ccd336f1c6a337459c0b350d7`
   (`receipt.steps.analyze.evidence_id` = `analyze.json.evidence_id`) all match. Package owner:
   `pacman -Qo /home/vgpnk/.local/bin/notesmd-cli` → “No package owns …”, exit 1, as the row says.
6. **Independent build-info, three readers agree.** `/home/vgpnk/.local/opt/go-1.27.3/bin/go
   version -m` → `go1.25.8`; `buildinfo-probe.py` → `go1.25.8`, `header_offset 4308992`, sha256
   `412dc532…`; `inspect-go.json` → `build_info.go_version go1.25.8`, same header offset.
7. **Canonical runtime, one identity.** Receipt argv pins `npx -y rea-agents@6.5.0`
   (`receipt.steps.*.argv`); npx package `version 6.5.0`; log script paths resolve under
   `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/bridge/ghidra`; Ghidra log paths
   are under `ghidra_12.1.4_PUBLIC`, `Ghidra/application.properties` → `application.version=12.1.4`.
   No second runtime appears in argv, log or receipt.
8. **Pins meaningful.** 146 entries = 143 installed Go-data files + carrier + r16 `selection.py` +
   the frozen prediction; `pins_compare.equal true`, `changed []`, `missing []`, `errors []`;
   pre `13:49:24.307807Z` before `inspect-go` `13:49:24.307831Z`, post `13:50:03.196163Z` after
   analyze end `13:50:03.151189Z`. The prediction's selected base
   `go1.25.0.json` sha256 `54d10162f4f55e5a…` and size `10081618` equal the pinned entry; the Go data
   dir contains only `go1.25.0.json` for 1.25 and no 1.25 patch diff, which is exactly why the router
   logs “Falling back … to 1.25.0”.
9. **Entry-level claims checked at the run set level** (bounded spot-check, not another lane's full
   audit): all 8 receipts have `bound_sessions` 1 / `unbound_sessions` 0, 146 pins, `pins_compare.equal`
   true, `carrier-run.exit` 0; analyze span `13:47:06.688621Z`–`14:00:05.228761Z` matches the entry's
   “13:47–14:00 UTC”; the pilot contains only shfmt and esbuild-0.25.12 logs, no notesmd, so this row
   was held out as the entry says.
10. **Source law behind the row.** `GoApiSnapshot.java:158-164` emits exactly the observed WARN/INFO
    pair; `GoRttiMapper.java:79` declares `1.15-1.25`; `:179-180` logs `apiSnapshot.getVer()`;
    `GoApiSnapshot.java:492-501` returns the requested version. The decision table's “request echo”
    caveat is source-correct.

## 4. Residual risk / verification gaps

- **`observation.json` and `compare.json` are outside the receipt's digest set.** They are written by
  `run-carriers.sh:27-28` after `carrier-run.py` exits, so no receipt field commits to them. For this
  run their content is byte-reproducible from the pinned log + frozen prediction (items 3-4), which is
  the strongest available substitute; a future receipt could hash them without re-running analyze.
- **Polling capture limit is real and disclosed.** The log stops at line 127 (`ANALYZING changes made
  by post scripts`, 10:50:02), one second before analyze end; later Ghidra lines are unobservable.
  For this run all Go diagnostics end at `:87` (10:50:00), before `REPORT: Analysis succeeded` (`:121`)
  and the bridge scripts (`:122-126`), so the Go claims are inside the captured window. Absence claims
  are bounded by line 127 only.
- **The binding booleans are self-asserted by the producer** (F5); this lane re-derived them by hand,
  not through the gate.
- Single run per carrier: no determinism claim; the entry makes none.
- `session_parent_leftovers: ["node-compile-cache"]` is benign residue in `/tmp/kr17-rea-odi4abuq/`;
  the session dir itself is gone (`ls` → “No such file or directory”), as intended.
