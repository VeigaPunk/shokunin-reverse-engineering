# ScoutRegistryFields — R17-REGISTRY row-field audit (round 18, W1)

Status: read-only scout. Writes only this report. No REA `analyze`/`search`/`decompile`, no
Ghidra/`analyzeHeadless`, no carrier execution, no `jj`/git write, no installs (nothing was
installed or upgraded). Labels: **[obs]** = read directly from the cited bytes; **[inf]** =
inference from those bytes.

Target: `corpus/lessons/round-17-verifier-spotcheck.md:144-146` (R17-REGISTRY), 10 rows at
`SKILL.md:537-546`, plus the citation-drift row at `SKILL.md:448`.

## 1. Canonical requirement (quoted verbatim)

`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:414-416` **[obs]**:

> Row fields: name,
> `gate|probe`, entry command, verdict map (code → class), self-test command and spelling,
> pinned-value path, write scope, owner.

`PROTOCOL.md:390-392` **[obs]**:

> A **gate** is a committed, re-runnable verdict script a lane owns: it reads surfaces, compares them
> against expected values persisted in its own repo, and returns a verdict. A tool that cannot fail is
> a **probe**, and is registered as one.

`PROTOCOL.md:393-396` **[obs]**: "`0` = `clean` and `1` = `failed` fleet-wide; every other code a gate
exits (`2`, `3`, `64`, …) is declared in its registry entry and mapped onto `clean | failed |
could-not-evaluate`, and an undeclared nonzero code reads as `could-not-evaluate`."

`PROTOCOL.md:398-401` **[obs]** (gate self-test): "… self-invocation mode over isolated fixtures …
asserting both the exit code and a stable expected finding-id, with the expected values committed in
the owning repo and independent of the recomputation."

`PROTOCOL.md:383-387` **[obs]** (what a pin is): "A pin counts only if its expected values are
**persisted inside the repo** (a recorded sha/mode/lines baseline, or a committed expected-output file
the script diffs against); a fingerprint *printer* with no stored baseline cannot detect drift."

## 2. Rubric used here

- **pinned-value path** = a literal repo path naming the persisted expected values the tool compares
  against or records. A printer with no baseline still has to fill the field, and the honest value is
  "none". Naming *subjects* ("the carrier, the prediction") without a path is **not** a path.
- **write scope** = an explicit statement of what the invocation writes; "stdout only" counts.
- **kind** = exactly one of `gate` or `probe` (first token of the 2nd cell).
- **verdict map** = the codes the entry exits mapped onto `clean | failed | could-not-evaluate`
  (gates) or onto the lane's emit/report vocabulary (probes).
- Everything else is marked as an accuracy/advisory note rather than a missing field.

## 3. Per-row table — missing field → proposed exact cell text

Each "Proposed" cell is a paste-ready full replacement for the named cell. All four C1-target rows
(`SKILL.md:540,541,542,545`) contain the literal `Write scope:` needed by
`.ufo/waves/round-18/contract.md` §C1 R17-REGISTRY. The minimum C1-compliant patch is the appended
`Pinned values: … ; Write scope: …` sentence; the texts below are the complete, accurate versions.

| Row (`SKILL.md`) | Missing / non-conforming required field | What the tool actually writes **[obs]** | What it actually pins **[obs]** | Proposed exact cell text |
|---|---|---|---|---|
| `:537` go-carrier-run | pinned-value **path**: the 5th cell names pinned subjects ("Carrier, r16 `selection.py`, frozen prediction and all 143 installed Go data files") but no path; kind contested, see §4.1 | `--out-dir` only: `<step>.json` + `<step>.stderr` (`tools/carrier-run.py:159-160,167,445-446`), `logs/<session>/ghidra.log`/`script.log` copied via `.tmp` + `os.replace` (`:230-245`), `receipt.json` (`:416-418`); plus a private `TMPDIR` `/tmp/kr17-rea-*` (`:299`) removed only when empty, leftovers recorded (`:413-415`); selftest writes only its `tempfile.mkdtemp()` root (`:517`); never executes the carrier (`carrier-run.py:3-6`; `run-carriers.sh:4-5`) | sha256+size+mtime_ns (`tools/pins.py:55-59`) of carrier + `.ufo/waves/round-16/selection.py` (`carrier-run.py:321-322`) + `--pin` extras (`:323`): `predictions/<label>.prediction.json` and all 143 Golang data files (`run-carriers.sh:12-14,26`; `find …/typeinfo/golang -type f \| wc -l` = 143). Pre at `:336`, mid every 30 s at `:477-487`, post at `:385`; all recorded in `runs/<LABEL>/receipt.json`. Mid-run instants retain only `{taken_at_utc, equal, entries:int, changed, missing}` (`:481-487`) — **not** per-path maps | Pinned values: carrier path from `predictions/carriers.tsv`, `.ufo/waves/round-16/selection.py` (built-in), `predictions/<label>.prediction.json` and all 143 files under `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang` (`run-carriers.sh:12-14,26`), each sha256+size+mtime_ns pre (`carrier-run.py:336`), every 30 s mid (only the comparator verdict is retained — `taken_at_utc`/`equal`/`entries:int`/`changed`/`missing`, `:481-487`; r17 writes no mid map) and post (`:385`), all inside `runs/<LABEL>/receipt.json` (`:416-418`); Write scope: `runs/<LABEL>/` only (step `*.json`/`*.stderr`, `logs/<session>/`, `receipt.json`) plus a private `TMPDIR` `/tmp/kr17-rea-*` removed when empty with leftovers recorded (`:299,413-415`); selftest writes only its `tempfile.mkdtemp()` root; never executes the carrier. Per-label exercised step argv is in `runs/<LABEL>/receipt.json` (`steps.*.argv`); the outer run argv and per-label instants are in `runs/run-log.txt` (an outer redirect — neither registered file writes it, `grep -c 'run-log' run-carriers.sh tools/carrier-run.py` = 0/0, rc 1); the registry form is retained in `.ufo/waves/round-17/verification.json` |
| `:538` go-log-extract | pinned-value **path** (none exists; the field must say so) | nothing — stdout only (`log-extract.py:44` "Read-only against the log file"); selftest writes only its `mkdtemp` fixtures (`:271-279`) | only `log_sha256` of the parsed input (`:244`); no stored baseline, never a verdict | Pinned values: none — observation printer; emits `log_sha256` of the input (`log-extract.py:244`) and never diffs a stored baseline; Write scope: nothing — stdout only, the log is opened read-only (`:122`); selftest writes only its `tempfile.mkdtemp()` fixtures (`:271-279`) |
| `:539` go-route-predict | pinned-value **path** | nothing — stdout only (`predict.py:55-56`); `sys.dont_write_bytecode` (`:67`); selftest fixture only (`:284-295`) | none persisted; the prediction is frozen by the caller in `predictions/<label>.prediction.json`; reads r16 `selection.py` by file path (`:71-73,94-99`) and `--golang-root` | Pinned values: none persisted — the prediction is emitted on stdout and frozen by the caller at `.ufo/waves/round-17/predictions/<label>.prediction.json` (tracked at `2711674`); Write scope: nothing — stdout only, imports r16 `.ufo/waves/round-16/selection.py` by file path with `sys.dont_write_bytecode` (`predict.py:67,71-73`) and reads `--golang-root` read-only; selftest writes only its `tempfile.mkdtemp()` fixture (`:284-295`) |
| `:540` go-route-compare | pinned-value **path** AND **write scope** | nothing — stdout only (`compare.py:28`); selftest fixtures only (`:392-405`) | none by the tool; compares a caller-supplied prediction (repo-tracked, frozen at `2711674`) with a `log-extract` observation; `snapshot_label` non-discriminating (`:39-43,47`) | Pinned values: none persisted by the tool — the caller-supplied predicted side is `.ufo/waves/round-17/predictions/<label>.prediction.json` (frozen at `2711674`), compared field-by-field against the `log-extract` observation; Write scope: nothing — stdout only, both inputs are opened read-only; selftest writes only its `tempfile.mkdtemp()` fixtures (`compare.py:392-405`) |
| `:541` receipt-validate | pinned-value **path** AND **write scope**; also code-2 class word absent from the 3rd cell (see §4.3) | nothing — stdout only; selftest writes only its `tempfile.mkdtemp()` root (`receipt-validate.py:606`) | the digests and `pins_pre`/`pins_post` recorded **inside the receipt it grades**: recomputes sha256/size of every named path (`:204-231`), re-runs `pins.compare` (`:397-445`); exit 2 on unreadable receipt, 1 on any finding, else 0 (`:495-500`); 2 also when `pins.py` is unloadable (`:733-737`) | Pinned values: the digests and `pins_pre`/`pins_post` recorded inside the receipt it grades (`.ufo/waves/round-17/runs/<LABEL>/receipt.json`, tracked at REV) — no separate expected file, so a receipt that rewrites its own digests is outside this check; Write scope: nothing — stdout only, every path the receipt names is opened read-only; selftest writes only its `tempfile.mkdtemp()` root (`receipt-validate.py:606`) |
| `:542` pins | kind `tool` is outside the `gate\|probe` enum (§4.2); pinned-value **path**; **write scope** appears only in the entry cell | exactly one map per `snapshot --out`, atomic `.tmp` + `os.replace` (`pins.py:113-128`); `compare` stdout only; selftest `mkdtemp` root (`:170`) | sha256+size+mtime_ns per realpath in the map (`:55-59`); `compare` tests **sha256 and size only** (`:96`), so a same-bytes touch is not a difference; `equal` false on changed, missing, or errored (`:75-99`) | 2nd cell: `probe / kaidoku`. 5th cell: Pinned values: none persisted by the tool — `snapshot --out` writes one map per invocation (sha256+size+mtime_ns per realpath, `pins.py:55-59,113-128`) and `compare` re-reads two caller-supplied maps, testing sha256+size only (`:96`; a same-bytes touch is not a difference); Write scope: exactly the `--out` file of `snapshot` (atomic `.tmp` then `os.replace`, `:118-125`), otherwise nothing — `compare` is stdout only; selftest writes only its `tempfile.mkdtemp()` root (`:170`) |
| `:543` temporal-sweep | pinned-value **path**; write scope not explicit ("Git objects only" states a read surface, not writes) | nothing — stdout only; selftest builds and `rm -rf`s a throwaway repo (`temporal-sweep.py:235,315-324`) | none persisted; census of Git blobs at `--rev`/`--sites-rev`; `--extra` files read from disk (`:8-10`) | Pinned values: none persisted — the census reads lane Git objects at `--rev`/`--sites-rev` and the literal `R16-PROVENANCE` correction text from the same blobs; `--extra` files are read from disk (`temporal-sweep.py:8-10`); Write scope: nothing — stdout only; selftest builds and `rm -rf`s a throwaway repo under `tempfile.mkdtemp()` (`:235,315-324`) |
| `:544` invocation-audit | pinned-value **path**; write scope not explicit | nothing — stdout only; selftest writes a throwaway git repo (`invocation-audit.py:370-382`) | none persisted; registry rows and exercised `argv`/`orig_argv` read from Git objects at `--rev` (`:1-14`) | Pinned values: none persisted — registry rows and exercised `argv`/`orig_argv` are read from Git objects at `--rev` (`invocation-audit.py:1-14`); Write scope: nothing — stdout only, `git show`/`git ls-tree` against Git objects, worktree untouched; selftest writes only its `tempfile.mkdtemp()` git repo (`:370-382`) |
| `:545` go-buildinfo-probe | pinned-value **path** AND **write scope** | nothing — stdout only, carrier opened read-only and never executed (`buildinfo-probe.py:306,620-635`); selftest fixtures only (`:502`) | emits the input's `sha256` (`:313`) only; source model pinned by the fetched-file digest `332fff28ac2569b76dda2e9d4f25aacc112e12bd8888fca927db0c5156187f45` in the header (`:15-18`) | Pinned values: none persisted — emits the input file's `sha256` plus the decoded build info (`buildinfo-probe.py:311-313`), never a stored baseline; the source model is the fetched go1.25.0 `debug/buildinfo` file pinned by digest `332fff28…` in the header (`:15-18`); Write scope: nothing — stdout only, the carrier is opened read-only and never executed (`:306`); selftest writes only its `tempfile.mkdtemp()` fixtures (`:502`) |
| `:546` round17-structural-controls | pinned-value **path** (the baseline is a revision, not a path); write scope not explicit | nothing — stdout only (`controls.py:505-514`); selftest fixture repo (`:433,449`) | the resolved BEFORE revision as the baseline for byte/SHA equality against AFTER blobs (`controls.py:31-36`); no expected-output file; prints the producing argv and both resolved revisions (`:505-514`) | Pinned values: the resolved BEFORE revision (commit id printed in the report) is the baseline every AFTER blob is compared to by byte/SHA equality (`controls.py:31-36`); no expected-output file; Write scope: nothing — stdout only, both revisions read via `git show`/`git ls-tree`, worktree untouched; selftest writes only its `tempfile.mkdtemp()` fixture repo (`:449`) |
| `:448` citation-drift | **kind**: registered `probe` while the registered `--strict` entry can exit 1 → gate (the routed defect; §4.4) | nothing — stdout only (`report()` prints, `citation-drift-probe.py:333-347`); `--selftest` writes isolated temp repos (`:352-447`) | `.ufo/gates/citation-drift/pointer-table.json` and `expected.json`, which pins `pointer_table.sha256` (`:295-307`) plus the 13-case selftest table and `frozen_run` | 2nd cell only: `gate / kaidoku` (the probe variant stays described in the entry cell and already is) |

## 4. Calibration notes beyond the minimal table

### 4.1 Kind disputes under `PROTOCOL.md:390-392` (not required by C1; L1 decision)

**[obs]** `go-route-compare` exits 1 on any field mismatch after comparing the observation against
`predictions/<label>.prediction.json`, which `git ls-files` shows tracked and `run-carriers.sh:2-3`
says was frozen at `2711674…` before the run; `run-carriers.sh:37,39` propagates that code
(`exit $overall`). `go-carrier-run` is the composite over the same comparison.

**[inf, medium]** By the gate definition ("compares them against expected values persisted in its own
repo … returns a verdict"), rows `:537` and `:540` are gates, not probes — the same reasoning the
lesson applies to citation-drift at `:146`, but stated for one row only. Applying it consistently
would mean three comparator rows move to `gate` (`:448`, `:540`, `:537`; `:541` already is a gate).

Cost if adopted: `PROTOCOL.md:398-401` then requires each selftest to assert a stable finding-id and
`PROTOCOL.md:403-410` a committed frozen-run expected verdict. Neither `compare.py` nor
`carrier-run.py` has a finding-id vocabulary or a frozen expected file today (`compare.py` selftest
asserts exit + `all_match` only, `:392-481`). Recommendation: either (a) record one explicit rule —
"probe = reads surfaces and reports; a comparison outcome against a repo-tracked expected file is a
gate" — and reclassify all three together with the added evidences, or (b) keep `probe` for `:537`
and `:540` and record the exception next to `:448`'s fix so the registry is internally consistent.
Do not fix `:448` alone while leaving the identical structure at `:537`/`:540` unremarked.

### 4.2 `pins` kind `tool` is outside the enum

**[obs]** `PROTOCOL.md:414-415` enumerates `gate|probe`; `SKILL.md:542` has `tool / kaidoku`.
Precedent: `SKILL.md:449` (custody-pair, outside this ticket's 10 rows) also uses `tool`; 2 rows use
`tool`, 3 use `gate`, 12 use `probe` (`grep -c` over `SKILL.md`). The lane's own
`invocation-audit.py:45` row-kind regex accepts `probe|gate|tool`, so changing this row to `probe`
does not break the auditor.

**[inf, high]** `pins` has no repo-persisted expected values; its exit 1 is a difference between two
caller-supplied maps, so `probe` is the only conforming enum value. Proposed 2nd cell: `probe / kaidoku`.

### 4.3 `receipt-validate` gate clauses

- **[obs]** Its 3rd cell says `2 unreadable`, but exit 2 also covers an unloadable `pins.py`
  (`receipt-validate.py:733-737`) and usage (`:727-732`); and the class word for code 2 is not
  stated. Proposed 3rd-cell replacement segment: `0 valid (clean), 1 any finding (failed), 2
  unreadable receipt or unloadable pins.py (could-not-evaluate)`.
- **[obs, gap]** Its selftest asserts **exit codes only**: every case calls `record(name, code, want)`
  (`:606-714`) and `record` compares `code == want`; `detail` is a findings dump, not an assertion.
  That does not satisfy `PROTOCOL.md:398-401` ("asserting both the exit code and a stable expected
  finding-id") for a gate. Tool-side fix (L1-owned): assert the finding `code` for each red case
  (`sha256_mismatch`, `binding_mismatch`, `mid_run_pin_drift`, …). The row's self-test text is
  accurate about which cases exist; it does not claim finding-id assertions.

### 4.4 citation-drift kind (the routed defect) — confirmed

**[obs]** `citation-drift-probe.py:492-494` registers `--strict` as "gate semantics 0/1/2"; `verdict(
strict=True)` returns `FAILED` when rows exist and none is CNE-class or historical-ok (`:86-100`), so
the registered entry can exit 1. `PROTOCOL.md:390-392` then makes it a gate. Everything else in the
row conforms: 13 selftest cases asserting exit **and** stable finding id (`:415-478`); `expected.json`
carries `pointer_table.sha256`, `frozen_run` `{revision, verdict, expected_findings}`, and 13
selftest cases (verified by parsing the file). Only the 2nd cell changes.

### 4.5 The 5th-cell evidence pointer in `:537` is imprecise

**[obs]** `grep -c 'run-log' run-carriers.sh tools/carrier-run.py` returns `0` and `0` with rc 1: the
registered script does not write `runs/run-log.txt` (it writes only `runs/<label>/…`,
`run-carriers.sh:19-34`); the file is an outer redirect, tracked in Git, containing the outer argv
line and per-label start/end lines (`runs/run-log.txt:1-18`). Per-label exercised argv lives in
`runs/<LABEL>/receipt.json` `steps.*.argv` (sample: `runs/calib-shfmt/receipt.json` steps
`analyze`/`inspect-go-binary`). The proposed `:537` cell says exactly this.

### 4.6 Mid-run map wording

**[obs]** `carrier-run.py:481-487` retains only the comparator verdict per mid-run instant; the
per-path map is discarded. The current cell's "every 30 s (retained)" is therefore ambiguous and is
the registry-side twin of R17-PINMAP. The proposed cell states the truth for r17 bytes. If
`.ufo/waves/round-18/contract.md` §C1 lands first (mid maps at `runs/<LABEL>/pins/mid-<n>.json` with
`map_sha256`), substitute that path/digest for the `:481-487` parenthetical — `routed-defects.py`
C1 check (d) only requires the literal `map_sha256` in `carrier-run.py`, not the SKILL cell, so either
order is safe.

## 5. Scope check against the routed lesson

**[obs]** `round-17-verifier-spotcheck.md:145` says "4/10 new SKILL registry rows (go-route-compare,
receipt-validate, pins, go-buildinfo-probe; `SKILL.md:540-542,545`) give no pinned-value path or write
scope". Verified: those four 5th cells contain **neither** a pinned path **nor** a write statement,
so "4/10" is exact for the neither-case.

**[obs]** The finer matrix: all 10 r17 rows lack a literal pinned-value **path**; 6 of them
(`:537,538,539,543,544,546`) do state a write/read surface, and 5 of those are printers/comparators
where the honest value is "none". Only `:448` fully conforms on both fields. Anyone re-using the
lesson's "4/10" as the complete non-conformance count would understate the field gap; the C1 patch
narrows it to the 4 rows on purpose (its check is scoped to `Write scope:`), which is why the
proposed texts here cover every row and not only those four.

## 6. Residual unknowns

- **[inf]** Whether the L1 wants `:537`/`:540` reclassified as gates is a protocol ruling, not a
  fact I can settle from bytes; §4.1 gives both paths and the cost. C1 does not depend on it.
- **[obs]** I did not execute any registered tool; only read-only `grep`/`find`/`git ls-files`/
  `python3 -c` (parsing `expected.json`) ran. All write/pin claims come from reading the committed
  sources, not from running them. Whether a given r17 receipt actually carries `pin_checks` is a
  per-run fact retained in `runs/<LABEL>/receipt.json` (not re-opened here, and not needed for
  field text).
- **[obs]** `receipt-validate`'s frozen-run evidence (R17-VALIDATE16) is a separate routed defect and
  was not re-adjudicated here.

## Evidence log (commands and exit codes)

```
grep -n -E '^\| (go-carrier-run|go-log-extract|go-route-predict|go-route-compare|receipt-validate|pins|temporal-sweep|invocation-audit|go-buildinfo-probe|round17-structural-controls|citation-drift) ' SKILL.md   -> exit 0; lines 448,537-546
grep -n -E 'A \*\*gate\*\* is|A tool that cannot fail|Row fields|Verdict\.|Self-test\.|Two evidences|pinned-value|Drift pins|A pin counts' PROTOCOL.md   -> exit 0; 383,390,391,393,398,403,414,416
grep -n -A3 'R17-REGISTRY' corpus/lessons/round-17-verifier-spotcheck.md   -> exit 0; 144-146
find /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang -type f | wc -l   -> 143, exit 0
grep -c 'run-log' .ufo/waves/round-17/run-carriers.sh .ufo/waves/round-17/tools/carrier-run.py   -> 0,0; grep rc 1
git ls-files .ufo/waves/round-17/predictions   -> exit 0; 19 tracked entries incl. every *.prediction.json, carriers.tsv, SHA256SUMS
git ls-files .ufo/waves/round-17/runs/run-log.txt   -> exit 0 (tracked)
grep -c '| tool / kaidoku' SKILL.md -> 2; '| gate / kaidoku' -> 3; '| probe / kaidoku' -> 12; exit 0
python3 -c (parse .ufo/gates/citation-drift/expected.json)   -> exit 0; selftest list n=13; pointer_table.sha256=7994eec7…; frozen_run keys {expected_findings,note,revision,verdict}
```
