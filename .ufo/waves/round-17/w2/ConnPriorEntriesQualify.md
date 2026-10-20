# ConnPriorEntriesQualify — r17 retained logs against r4-10 / r14 / r15 / r16

Seat: connector (author-side advisory), wave 2, read-only. Axes: **calibration**, **depth**.
Surface: lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`; retained runs under
`.ufo/waves/round-17/runs/`; pilot under `.ufo/waves/round-17/pilot/`.
No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution, no installs.
Read-only commands only: `grep`, `sed`, `sha256sum`, `git`, Python `-B`, and the round-17
tools against retained files. One write: this file.

Shorthand: `$R = /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17`.

## 0. Evidence base (observation)

- Eight retained `ghidra.log` files, one bound session each. Every log carries its own
  `Using log file:` and `IMPORTING: file:///tmp/kr17-rea-*/…/target-<sha12>.bin` lines
  (e.g. `$R/runs/pro-op/logs/rea-ghidra-yRmWqx/ghidra.log:2,46`).
- Log digests recomputed directly and equal to the receipts:
  `sha256sum $R/runs/pro-op/logs/rea-ghidra-yRmWqx/ghidra.log` →
  `7729b2154dd812108ef86f55f7e42a0fc7466b804d3c95074692ad5ad24042a9`,
  matching `$R/runs/pro-op/receipt.json:1810`.
- All eight receipts carry 146 pin entries pre and post and `pins_compare.equal = true`
  (read from the receipts; see §2 F3 on why the documented validator disagrees).
- `$R/runs/*/compare.json` all report `"all_match": true` for the five compared fields.
- Pilot digests verify: `(cd pilot && sha256sum -c SHA256SUMS)` → 6 × `OK`.
- Probe command used for every log claim below:
  `grep -n -E "Untested Go version|Go API snapshot|Missing Go bootstrap|Found [0-9]+ Go types|unable to get GoRttiMapper|Go analysis failure|EOFException" $R/runs/*/logs/*/ghidra.log`

This base is sufficient to move several prior source-model statements into the
observation-backed column. It is **not** sufficient for any recovery-quality claim:
no `search` ran (`$R/corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:129-130`).

## 1. Connection map

Status vocabulary: **CONFIRMED** (retained log matches the prior statement),
**QUALIFIED** (matches only under a stated narrowing), **CONTRADICTED**, **NOT TESTED**
(no retained r17 log bears on it). "Correction" asks only whether an append-only named
correction is owed to the *prior* entry.

### 1.1 r4-10 — `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`

| # | Prior statement | Retained r17 evidence [OBS] | Status | Correction owed |
|---|---|---|---|---|
| R4-1 | `:71-73` the analyzer "cannot parse the Go 1.26 moduledata/pclntab layout"; the bootstrap message was seen but the dir was deleted, "observed-not-cited" | `$R/runs/pro-op/logs/rea-ghidra-yRmWqx/ghidra.log:68-70`: `Reading Go binary info`, `Untested Go version [1.26.8]`, `Missing Go bootstrap type info…`; zero `GoApiSnapshot` lines. Same pair for 1.27.0 (`calib-shfmt/…/ghidra.log:82-84`) and 1.27.2 (`pro-containerd-shim/…/ghidra.log:240-242`) | **QUALIFIED** | **No.** r14's supersession at `:196-205` already replaces the cause. r17 supplies the missing message text for a *different* go1.26.8 binary; it does not authenticate the 2.40.0 session |
| R4-2 | `:66-70` 33,060 vs 11,595 procedures; 11,588 `FUN_*` on 2.40.0 | No `search` was run; `$R/runs/pro-op/analyze.json` is the evidence envelope only (keys `evidence_id, normalized_result, …`; no procedure count) | **NOT TESTED** | No |
| R4-3 | `:186-189` "a Go toolchain bump silently collapses provider symbol recovery" | Class-level only: 2/2 in-range 1.25.x carriers bootstrapped (`pro-notesmd-cli…:70-71` 2,302 types; `pro-aether…:94-95` 6,115 types); 3/3 out-of-range carriers did not | **QUALIFIED** | No new one; the causal reading is already corrected at `:196-205` |
| R4-4 | `:191-192` ~6 min per verb at 41–43 MB; raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` on every call | `$R/runs/run-log.txt`: eight `analyze` runs 31 s–4 m 09 s; seven receipts record `rea_ghidra_env: {}`, `pro-op` records `REA_GHIDRA_STARTUP_TIMEOUT_MS: 900000` (the 4 m 09 s run). Carriers 3.6 MB (`/usr/bin/shfmt`) to 11.1 MB (`esbuild 0.27.7`, `inspect-go.json`) | **CONFIRMED** as written (scale-scoped). r17 does not test the default bound at 41–43 MB, and one run did raise it as advised | No |
| R4-5 | `:136-143` evidence_ids deterministic across sessions | `pilot/shfmt.json` `ev_2b29a1dd…` and `pilot/esb.json` `ev_391dbfe6…` reproduced exactly in the new runs (`runs/calib-*/receipt.json`), ~30 min later, same argv | **CONFIRMED** (one more instance; the r17 entry itself calls it "one repetition, not a determinism proof") | No |

### 1.2 r14 — `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`

| # | Prior statement | Retained r17 evidence [OBS] | Status | Correction owed |
|---|---|---|---|---|
| R14-1 | `:31-34` out-of-range logs `Untested Go version` and continues to the snapshot lookup | `calib-shfmt/…:83-84`: ERROR `Untested Go version [1.27.0]` immediately followed (same second) by WARN `Missing Go bootstrap…`; same pair `pro-op…:69-70`, `pro-containerd-shim…:241-242`. Reaching bootstrap proves the range branch did not stop execution | **CONFIRMED** (runtime) | No |
| R14-2 | `:35-38` missing base → `null` → `GoApiSnapshot.EMPTY` at `:115`; patch search does not fall back to an earlier minor | All three out-of-range carriers log **no** `GoApiSnapshot` line at all. 1.26.8 did not reuse the installed 1.25.0 base, so no cross-minor fallback occurred | **CONFIRMED** | No (but see D1: the absence is a stronger discriminator than the entries state) |
| R14-3 | `:39-44` bootstrap is conditional; invalid snapshot selects the message, a valid snapshot with failed mapping selects a different message | `calib-shfmt/…:84` logs the message at **WARN**, i.e. `Msg.warn` in the `BootstrapInfoException` branch (`GoRttiMapper.java:114-117,355-360`), not the `ERROR "Failed to read Go info"` branch (`:121`). No stack trace on any out-of-range carrier | **CONFIRMED + sharpened** (the log level is the branch discriminator; see D2) | No to r14; the r17 entry should claim the level (§3 D2) |
| R14-4 | `:45-50` (INFERENCE) message = failed struct registration with an invalid snapshot, not the range check; mapper returns null; analyzer returns false | `calib-shfmt/…:84-85`: WARN message then `GolangSymbolAnalyzer … unable to get GoRttiMapper`, matching `GolangSymbolAnalyzer.java:133-137` (null mapper → error → `return false`) | **CONFIRMED** at runtime for three carriers | No |
| R14-5 | `:51-54` a present file with no applicable records can reach the same invalid-snapshot branch | Not exercised: no carrier had a present base with an empty applicable bucket set | **NOT TESTED** (source possibility unchanged) | No |
| R14-6 | `:75` decision-table row: `Untested` = range exceeded, branch continues; next evidence "retained analyzer log" | The three retained logs are exactly that evidence | **CONFIRMED** | No |
| R14-7 | `:76` missing base row; next evidence "pin installed data and binary build version" | 146 pinned paths pre/post (equal), including `go1.25.0.json` and r16 `selection.py`; build versions from `inspect-go-binary` (1.26.8, 1.27.0-X:nodwarf5, 1.27.2-X:nodwarf5) | **CONFIRMED** | No |
| R14-8 | `:77` missing-bootstrap row; next evidence "distinguish absent base file from OS/architecture exclusion" | Absent base is established for 1.26.8/1.27.0/1.27.2 by the missing `GoApiSnapshot` line; OS/arch exclusion is not exercised | **CONFIRMED (absent-base branch only)** | No; an optional one-line confirmation note would close the row (see D1) |
| R14-9 | `:78` `FUN_*`/missing `main.main`; next evidence "retained diagnostics and an appropriately scoped search" | Diagnostics retained; no search | **NOT TESTED** | No |
| R14-10 | `:83-90` the original 2.40.0 run's log was not retained; cause UNKNOWN | Still true: r17 analysed a different `op` binary (2.41.0-1) | **CONFIRMED unchanged** | No |

### 1.3 r15 — `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`

| # | Prior statement | Retained r17 evidence [OBS] | Status | Correction owed |
|---|---|---|---|---|
| R15-1 | `:63` 11 bases / 123 diffs; every base has `all` | Not re-inventoried by r17; no retained log bears on file counts | **NOT TESTED** | No |
| R15-2 | `:64` patch histogram has none for 1.25/1.26 | 1.25.8 and 1.25.14 both WARN `Falling back … to 1.25.0` (`pro-notesmd-cli…:68`, `pro-aether…:92`) → no 1.25 diff at or below request; 1.26.8 has no snapshot line → no 1.26 base/diff | **CONFIRMED** operationally | No |
| R15-3 | `:66` requested 1.25.7: base S023 (`54d10162…`), 27 buckets, no minor diff | The frozen 1.25.8 prediction carries exactly `base.sha256 54d10162…` and buckets `linux-amd64, linux, unix, amd64, all`; both 1.25.x carriers bootstrapped from the same-minor base | **CONFIRMED** (the log names no file; identity follows from the same-minor-only lookup law plus the matching digest) | No |
| R15-4 | `:67` `runtime.moduledata`/`runtime.pcHeader` only under `all` | Successful struct registration on linux/amd64 for both 1.25.x carriers proves the required structs were found; **which bucket supplied them is not logged** | **CONFIRMED BY OUTCOME** (bucket identity unobservable) | No |
| R15-5 | `:68` requested 1.26.8: same-minor base absent | `pro-op…:69-70` no snapshot line + missing bootstrap; the frozen prediction says `missing_base` | **CONFIRMED** (prospective: prediction frozen at `2711674` before the run) | No |
| R15-6 | `:15-17,21-23` `isInvalid()` = empty arch map; requested label ≠ selected bytes | `pro-aether…:92-93`: `Falling back from 1.25.14 to 1.25.0`, then `Using Go API snapshot for version 1.25.14` | **CONFIRMED** at runtime | No |

### 1.4 r16 — `corpus/knowledge/2026-10-20-r16-go-selection-preview.md`

| # | Prior statement | Retained r17 evidence [OBS] | Status | Correction owed |
|---|---|---|---|---|
| R16-1 | `:40` `base_only` covers exact patch-0 and a higher patch falling back to base | 1.25.8/1.25.14 predictions are `selection.status = base_only`; Java logged the fallback WARN with target `1.25.0` (the base) | **CONFIRMED** | No |
| R16-2 | `:46` version/GOOS/GOARCH are caller inputs in the preview; Java derives them by build-info/loader paths the instrument does not execute | The version half is now exercised on targets (1.23.12, 1.20.12, 1.25.8, 1.25.14, 1.26.8, 1.27.0-X, 1.27.2-X). GOOS/GOARCH are not reported in any retained log field. `pro-esbuild-0.27.7` (`build_info: null`) reaches `Reading Go binary info` then `unable to get GoRttiMapper` with **no** version/untested/bootstrap line | **QUALIFIED**: version half confirmed; GOOS/GOARCH half NOT TESTED; the default no-build-info route terminates rather than falling back | No to r16 (the sentence is scoped to the instrument); see D3 |
| R16-3 | `:67-72` executed table: 1.23.12/1.20.12 `exact_diff`, 1.24.x `fallback_diff`, 1.25.7 `base_only`, 1.26.8 `missing_base` | 1.23.12/1.20.12 logged INFO (nonzero request ⇒ the loop stopped at the requested patch ⇒ exact diff); 1.25.x/1.26.8 as above. No 1.24.x carrier was run, so `fallback_diff` is untouched | **CONFIRMED** for `exact_diff`, `base_only`, `missing_base`; **`fallback_diff` NOT TESTED** | No |
| R16-4 | `:45` source archive not authenticated against executing classes; runtime overrides not identified | Retained logs come from the running provider, but no class/data digest accompanies the log lines | **NOT TESTED** | No |

### 1.5 Adjacent prior Go entries (not named in the ticket, checked anyway)

| # | Prior statement | Retained r17 evidence [OBS] | Status | Correction owed |
|---|---|---|---|---|
| L7-1 | `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md` "Unknown / limitations": "No missing-metadata or rejected input was tested" | `$R/runs/pro-esbuild-0.27.7/inspect-go.json` returns `"build_info": null` for a real 11.1 MB Go ELF; the independent `buildinfo-probe.py` run returns `"found": false`, `"magic_file_offsets": []`; the analyzer logs `Reading Go binary info` then `unable to get GoRttiMapper` with no version/untested/bootstrap line (`$R/runs/pro-esbuild-0.27.7/logs/rea-ghidra-DjvEp2/ghidra.log:63-69`) | **GAP PARTLY DISCHARGED** (missing-metadata observed through two independent readers; malformed/oversized still untested) | No; an append-only one-line note is the smallest improvement |
| R12-1 | `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`: same-path repeat stability for `inspect_go_binary` at REA 6.7.0, path-sensitive through three semantic fields | r17 repeated two IDs on the same paths under REA 6.5.0 (`pilot/shfmt.json` ↔ `runs/calib-shfmt/receipt.json`; `pilot/esb.json` ↔ `runs/calib-esbuild-0.25.12/receipt.json`). Same-path stability is consistent, but the operation is `analyze`, not `inspect_go_binary`, and the version is 6.5.0, outside that entry's scope | **ADJACENT / NOT TESTED** for the r12 law | No |

## 2. Findings on the r17 artifacts where the connection is *stated* wrongly

### F1 — MEDIUM (calibration): the entry resolves a version conditional the corpus already settles

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:117-120` says the historical
`op` 2.40.0 loss "belongs to the same missing-base class **only if** that build was
go1.26.x." The lane's own record says it was:

```
$ sed -n '19p;69p' corpus/knowledge/2026-10-13-r4-10-real-version-pair.md
# (middle of line 19 elided with … here; both lines otherwise verbatim)
| `1password-cli` 2.34.1-1 → 2.40.0-2 | … | ELF x86-64 static, stripped Go (**go1.25.7 → go1.26.8**) |
- `op-2.40.0` (`go1.26.8`): only 11,595 procedures recovered, 11,588 of them
```

So the open part is the missing binary and log, not the version. Presenting the version
as an open conditional understates the lane's evidence and can be read as "version
unknown", which r4-10 contradicts.

**Smallest fix:** replace `:117-120` with one sentence: "the 2.40.0 build is recorded as
go1.26.8 (`r4-10:19,69`), so the missing-base class is consistent with that run; the
binary and its log are gone, so this run is not reproduced and its cause stays UNKNOWN."
No re-run, no new file.

### F2 — LOW (calibration): a source inference sits unlabelled inside an observation bullet

`:78-81` ("Ghidra still selected the golang compiler spec, which comes from section
names, not build info") is an inference, not a log observation. It is supported by the
installed source (`GoRttiMapper.java:201-210`, `hasGolangSections` checks
`gopclntab` / `GoBuildInfo.SECTION_NAME`), and by the hand prediction's basis
(`predictions/pro-esbuild-0.27.7.prediction.json`, basis[1]), but neither is cited there.
Every other claim in that bullet is a literal log line.

**Smallest fix:** prefix the clause "INFERENCE FROM SOURCE (`GoRttiMapper.java:201-210`)"
or cite the prediction basis. One line.

### F3 — cross-reference only (not a new finding): two r17 defects are already routed

`w2/RunProaether.md:32-99` already files (F1) the `receipt-validate.py` shape disagreement
— `receipt-validate.py:98-101` requires `steps` to be a list while `carrier-run.py:275,349`
writes a dict; all eight receipts return `unrecognized_shape`, exit 1 — and (F3) the
unresolvable `2716747` pointer (`receipt-validate` and `git cat-file` both fail on it).
I reproduced both and do not duplicate them. They matter here only in one respect:
**none of this report's confirmations depends on `receipt-validate` exit 0.** They rest on
recomputed log digests and on the receipts' `pins_compare.equal = true` (146 entries),
both of which are readable without the validator.

## 3. Depth available in the retained logs but not claimed (no false statement)

### D1 — LOW–MEDIUM (depth): the `GoApiSnapshot` line's *presence* separates missing base from empty-bucket

r14 `:77` leaves "absent base file vs OS/architecture exclusion" as future work, and
r14 `:51-54` says both reach the same invalid-snapshot branch. The installed source makes
them separable in the log, without a new run:

- `GoApiSnapshot.getApiSnapshotJsonFile` returns `null` at `:124-125` **before** any log
  when the base file is missing.
- Whenever a base file exists, `getPatchVerDiffFile:148-165` logs either the WARN or the
  INFO before any read.

Therefore: `Untested` + **no** `GoApiSnapshot` line ⇒ base file absent. The retained
lines also separate the other two branches, which r14 `:51-54` currently treats as one:

| Case | `GoApiSnapshot` line | mapper `…for version X` (`GoRttiMapper.java:178-181`) | bootstrap line |
|---|---|---|---|
| base file missing (`EMPTY`, `GoVer.INVALID`) | absent | absent | `Missing Go bootstrap…` WARN |
| base present, no applicable arch bucket | WARN/INFO present | present (requested version; `getVer()` is valid) | same WARN (`apiSnapshot.isInvalid()` at `:356`) |
| base present, valid snapshot, failed mapping | WARN/INFO present | present | ERROR `Failed to read Go info` + stack (`:121`) |

The three out-of-range carriers show the first row; no carrier exercises the other two.
This is an `[INF]` chain from source plus `[OBS]` absence, and it is the cheapest closure
of r14's `:77` for the absent-base branch. It also confirms r15 `:67`'s generic-`all` law
at outcome level: registration succeeded from the 1.25.0 base on linux/amd64 — though the
log never says which bucket supplied the structs.

**Smallest fix:** one sentence appended to r14's `:77` row (or to r17's decision-table row
`:105`): "a missing `GoApiSnapshot` line separates absent base from present-but-inapplicable
arch; the latter still logs a snapshot line."

### D2 — LOW–MEDIUM (depth): the WARN/ERROR level is the branch discriminator r14 left implicit

r14 `:39-44` distinguishes "invalid snapshot → message" from "valid snapshot, failed mapping
→ different message". The retained log makes that distinction observable without a stack:
the invalid-snapshot branch calls `Msg.warn` (`GoRttiMapper.java:115`), while the failed-mapping
branch calls `Msg.error(..., "Failed to read Go info", e)` (`:121`) and writes a stack trace.
All three out-of-range carriers log the message at WARN and no `Failed to read Go info` line.
That upgrades r14 `:45-50` from INFERENCE to runtime-confirmed for these carriers and is
one clause the r17 entry does not use.

**Smallest fix:** add to r17's `:73-77` observation: "the message is WARN, i.e. the
invalid-snapshot branch (`GoRttiMapper.java:115`), not the ERROR IOException branch (`:121`)."

### D3 — LOW (calibration): "fallback" in r17's route vocabulary is two r16 statuses

`pro-notesmd-cli.prediction.json` has `selection.status = base_only` and
`expected.snapshot_route = fallback`; the log's WARN fires because a nonzero requested
patch found no diff at or below it, not because a lower diff was selected. r16 `:40`
already documents that `base_only` covers a higher patch falling back to base, so no prior
statement is wrong; but a reader cross-referencing r16's `fallback_diff` row will mis-map.
The `info` label, by contrast, is 1:1 with `exact_diff` for a nonzero request (INFO only
fires when `patchVer.getPatch() == goVer.getPatch()`).

**Smallest fix:** one clause on r17's decision-table row `:103`: "also fires for
`base_only` with a nonzero requested patch; it does not imply a diff was applied."

## 4. Bounded no-finding — what I checked and did not find

- **No prior entry claims the 2.40.0 log was retained**, and none claims r17 reproduces that
  session. r4-10 `:196-205` and r14 `:83-90` both keep it UNKNOWN; the retained r17 logs do
  not change that.
- **No prior numeric count is contradicted.** r15 `:63-68` (11 bases, 123 diffs, no 1.25/1.26
  diffs, 1.26.8 base absent) is consistent with every retained log; r17 simply does not
  re-run the inventory.
- **No prior entry asserts that the range check aborts recovery.** r17's three `Untested`
  carriers show the opposite, but the prior text already says "there is no throw or return"
  (`r14:33-34`) and "the inspected branch continues" (`r14:75`).
- **r16's `fallback_diff` row and GOOS/GOARCH derivation are not exercised.** The only
  fallbacks are `base_only` (1.25.x); no 1.24.x carrier ran; no log records the derived
  GOOS/GOARCH. I assert no contradiction for those.
- **r4-10's procedure-name counts are not testable from r17.** `analyze` returns no
  procedure count in this envelope, and no `search` ran; the r17 entry says so itself
  (`:129-130`).

## 5. Axis effects, one bounded move, risks, verification

**Affected axes.**
- *Calibration* (primary): six prior decision-table rows move from source-only to
  observation-backed with no new execution; two r17 miscalibrations are identified (F1,
  F2); one vocabulary hazard (D3).
- *Depth* (secondary): two discriminators the retained logs already contain but the entry
  does not claim (D1, D2). No runtime, contract or substrate surface is touched.
- *Harm*: none identified. Every action proposed is an append of text; no tool, receipt,
  prediction or run is modified.

**One bounded move (for L1 to accept or reject).**
Append a single "Prior-entry status" block to
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` containing:
(a) the r14 `:75-77` and r16 `:40,:67-72` rows each mapped to the exact retained log line
that confirms it; (b) an explicit untested list (r14 `:78`; r16 `fallback_diff` and
GOOS/GOARCH; r15 `:63`); (c) the D1 and D2 clauses; (d) the F1 replacement sentence and the
F2 label. The block is a table plus five sentences; it cites only files under `$R/runs/`
and installed-source anchors already in the entry's `source:` line.

Why this is the non-obvious move: it converts the round's main evidence from "eight logs
exist" into "these specific prior claims are now observation-backed, and these specific
ones are not", which is exactly what the r14/r15/r16 decision tables were built to
arbitrate. It also *narrows* rather than widens the round's claim, because the untested
list keeps recovery quality, `fallback_diff`, and OS/arch exclusion out of the confirmed set.

**Risks.**
1. Duplication with r14's own decision table — keep it to one table and do not restate
   r14's prose.
2. Over-citation — r17 is author-side evidence, not outside verification; the block must
   say so and must not imply the 2.40.0 session was reproduced.
3. The block cites `runs/*/ghidra.log` line numbers; if a sibling rewrites the entry, the
   anchors can drift. Cite `label/logs/<session>/ghidra.log:<line>` and re-check with the
   grep in §0 before landing.
4. If L1 instead adopts RunProaether F1's validator fix, the entry's `recheck:` line should
   be updated in the same commit; otherwise the corpus will again carry a recheck that
   exits 1 (the r15 `:76-94` defect class).

**Verification (read-only, reproducible).**
1. `grep -n -E "Untested Go version|Go API snapshot|Missing Go bootstrap|Found [0-9]+ Go types" $R/runs/*/logs/*/ghidra.log` — every quoted line reappears at the cited number.
2. `python3 -B -c` over `$R/runs/*/observation.json` + `$R/predictions/*.prediction.json` — `classification`/`snapshot_route`/`bootstrap_attempts` as tabulated; all `compare.json` `all_match: true`.
3. `sha256sum` of each cited log equals `receipt.json`'s `retained_logs[].files["ghidra.log"].sha256`.
4. `git diff --stat` after landing shows only the knowledge entry; no `runs/`, `predictions/`, or `tools/` bytes change.
5. Negative control: for a hypothetical present-base/empty-bucket case the D1 discriminator must show the `GoApiSnapshot` line; no such carrier exists, so the block must say "not exercised" rather than claim it.

Tool installs/updates: none.

## Files written

- `.ufo/waves/round-17/w2/ConnPriorEntriesQualify.md` (this file)
