# ReviewSkillRegistry — round 20

Axes: **calibration, coverage, depth**.

## Findings

### High — evidence-timestamps draft does not preserve D2’s strict contract

**OBS:** D2 requires every qualifying timestamp in every tracked file under the selected path to be compared, and `--strict` must exit 1 on any finding (`.ufo/waves/round-20/contract.md:41-45`). The available `EvidenceTimestampLint-2.patch` instead skips binary blobs and blobs larger than 4 MiB (`:14-16`, `:220-232`), accepts `--allow FILE:LINE` (`:428-436`), and returns strict exit 1 only when `unexempted_finding_count` is nonzero (`:265-280`, `:455-457`). Thus an explicitly allowed finding returns 0, and large text blobs are outside the scan. **Recommendation:** either remove/limit those exceptions and cover D2’s stated scope, or amend D2 and the registry to make the exception and skip limits explicit. The row must say `0` = no unexempted finding, `1` = strict unexempted finding, `2` = refusal, and list any `--allow` use; do not say “any finding” unless the implementation is changed.

### Medium — compare-first-failure is a probe, and the drafted invocation is incomplete

**OBS:** C3 explicitly says the observed match count `k/N` is reported “whatever it is” (`claims.json:36-39`); this is measurement, not an acceptance threshold. Existing comparable `go-route-compare` is registered as a probe (`SKILL.md:540`). `DraftSkillRows.md:43` classifies `compare-first-failure` as a gate; change it to `probe / kaidoku`.

**OBS:** The contract command omits an extractor argument (`contract.md:80-81`), but `CompareFirstFailure-2.patch` requires `--extractor` outside selftest (`:161-175`). Record the actual invocation as `--prediction P --log L --extractor PATH`, or align the implementation with the contract. The patch has a `--selftest` (`:103-158`), so the draft’s “no self-test named” at `DraftSkillRows.md:43` is stale relative to that patch. Its match rule compares only `kind` and `index`, ignoring `va` and `phase` (`CompareFirstFailure-2.patch:34-40`); include that projection in the row’s verdict description. Pin the extractor implementation as well as the frozen prediction and run-bound log.

### Medium — final-census is an executable gate runner, not only a record

**OBS:** The existing draft calls `final-census` a `record` and gives it no executable invocation (`DraftSkillRows.md:38`). The available `FinalCensusRecorder.patch` adds `tools/final-census.py` (`:1-8`): it runs both the C1 census and sources census (`:159-173`), stores `final-census.stdout` and `final-census.json` (`:22-25`, `:173-205`), returns the maximum of the two command statuses, and returns 2 on preflight/write refusal (`:117-157`, `:190-205`). Its CLI is `python3 -I -B .ufo/waves/round-20/tools/final-census.py --root <LANE> --out-dir <LANE-RELATIVE-OR-ABSOLUTE-DIR>`; `--selftest` is implemented (`:318-330`) with clean-record, untracked-worktree, and tracked-modification cases (`:221-315`). Register it as a **gate / kaidoku** (a gate runner that also produces D5’s record); retain `final-census.json` as its evidence artifact. Keep the separate `c1-census-v10` gate row for D4.

**OBS / residual:** The patch records `refs/heads/main` as `rev` but executes census commands against the live worktree after rejecting tracked modifications; it does not compare `HEAD` to that ref (`FinalCensusRecorder.patch:148-166`). Its selftest intentionally allows untracked files and records `worktree_clean: false` while returning 0 (`:273-285`). Therefore the row/contract must not claim the recorded `rev` alone proves the census ran against that exact delivered tree. Bind the executed tree to `rev` or state the live-worktree limitation and require the retained status field to be true for acceptance.

### Low — C1 counting gate is omitted from the existing draft

**OBS:** C1’s `counting_command` explicitly invokes `routed-r19.py --root <LANE> --rev <REV> --strict` (`claims.json:15-18`), but `DraftSkillRows.md:56` says it drafted no row. Add `routed-r19 | gate / kaidoku`, with 0/1/2 meanings and `--selftest` confirmed from the implementation (round-20 conventions: `contract.md:28-32`); pin the routed defect IDs and evidence/revision inputs. The tool was not available in the reviewed `W20/tools/` tree, so exact findings and selftest cases remain unverified rather than inferable from the claim alone.

**OBS:** C3 also names `measure.py <REV>` as its counting command (`claims.json:38`). If the registry is to cover the executable entrypoints used by these claims, add a `measure.py | probe / kaidoku` row too; it is a report/count, not a verdict. This is additional to the requested list.

## Row fields and draft classifications

**OBS:** The registry’s five required fields are `Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope` (`SKILL.md:445-446`). The precedent distinguishes a strict gate from a reporting probe (`citation-drift`, `SKILL.md:448`), allows `tool / kaidoku` for stateful utilities (`custody-pair`, `:449`), and registers diagnostics/comparisons as probes (`go-route-compare`, `:540`; `swiss-misread`, `:590`). Proposed rows below are contract/patch-grounded drafts, **not executed results**.

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| evidence-timestamps | gate / kaidoku | `python3 -I -B .../evidence-timestamps.py --root LANE --rev REV --path DIR [--strict] [--allow FILE:LINE]`; patch: 0 no unexempted finding, 1 strict unexempted finding, 2 unusable/refused (`EvidenceTimestampLint-2.patch:428-457`) | `--selftest`; cases in patch `:342-425` | Git objects at REV; identify timestamp-to-introducing-committer-time rule, allowed lines, and 4 MiB/binary skip limit. No normal-mode writes; JSON stdout. Resolve D2 mismatch above before treating it as closure. |
| carrier-guard | tool / kaidoku; `check` is the gate operation | Contract entry `carrier-guard.py {arm,check,disarm} --manifest TSV --record DIR`; `check` reports `mode_restored`, `ctime_changed`, `content_changed` and exits 1 on findings; success/usage map is not specified (`contract.md:46-52`) | `--selftest`; record `exec_refused` and `mode_restored` cases (`:50-51`) | Must declare mutation: `arm` clears exec bits, `disarm` restores modes; records arm/check/disarm JSON in `--record`. State loader-mapped execution/root limits. No implementation-level result observed. |
| revexec | tool / kaidoku | `revexec.py run --root LANE --rev REV --entry PATH [--extra PATH ...] -- ARGS`; patch passes child status through and returns 2 on refusal (`RevexecSandbox-2.patch:319-347`) | `--selftest` cases `write_outside_refused`, `net_refused`, `runs_ok` (`contract.md:58-61`; patch `:202-316`) | Pin the Git revision and selected blobs; record the actual sandbox primitive. Patch uses transient `systemd-run` (`:121-157`), temporary extraction is removed (`:170-189`), and the documented root/kernel residual applies (`:16-17`). Not a gate verdict or probe. |
| verb-coverage | probe / kaidoku | `verb-coverage.py --root LANE --rev REV [--package-dir DIR]`; patch emits JSON/0 or refusal/2 (`VerbCoverageTool.patch:275-299`) | `--selftest` (`:208-272`) | Record package version 6.5.0 and the CLI catalog source; mention-count and C2 evidence-path/`ev_` exercised criterion (`contract.md:71-75`; patch `:29-45`, `:158-199`). Git-at-REV read-only. Preserve C2’s finite-catalog/mention-level limit (`claims.json:27-30`). |
| swiss-misread-v2 | probe / kaidoku | `swiss-misread-v2.py --carrier PATH [--label L] [--snapshot-dir DIR]`; emits H1/H0 `first_failure` objects or null per hypothesis (`contract.md:76-79`). Normal exit map is not stated in the interface. | `--selftest` (`contract.md:76`); record observed case count only after it runs. | Pin carrier hash and snapshot identity/digest; state variadic-bit masking and that outputs are forecasts frozen before held-out analysis (`contract.md:76-79`, `claims.json:36-39`). No carrier execution. |
| first-failure-extract | probe / kaidoku | `first-failure-extract.py LOG`; extract first bound-log Go-analysis failure into the shared object shape (`contract.md:79-80`). Exit map is unspecified. | **Gap:** contract does not name a selftest although Python tool convention requires one (`contract.md:28-32`, `:79-81`). | Pin log/run identity; read-only log input, structured stdout. Do not claim an extractor selftest until present and exercised. |
| compare-first-failure | probe / kaidoku | Actual patch form needs `--prediction P --log L --extractor PATH`; 0 match, 1 mismatch, 2 unevaluable (`contract.md:80-81`; `CompareFirstFailure-2.patch:161-175`). Equality is `kind` + `index`, not `va`/`phase` (`:34-40`). | Patch `--selftest` (`:103-158`); unrun. | Pin prediction freeze, exact run-bound log, and extractor bytes/identity; stdout JSON, no normal-mode write specified. Match count is reported, not a C3 pass threshold. |
| routed-r19 | gate / kaidoku | `routed-r19.py --root LANE --rev REV --strict` (`claims.json:17`); exact check findings/exits must come from the landed implementation and the 0/1/2 tool convention (`contract.md:28-32`). | `--selftest` required by the Python convention; case IDs unverified. | Pin defect IDs/reference revisions and measured REV; Git-object evidence only as claimed by C1 (`claims.json:15-18`). No implementation reviewed in the tool directory. |
| final-census | gate / kaidoku (record-producing) | Patch CLI `final-census.py --root LANE --out-dir DIR`; 0 if both checks pass, nonzero if a check fails, 2 on refusal (`FinalCensusRecorder.patch:117-205`, `:318-330`). | `--selftest`; clean record/untracked/tracked-modification cases (`:221-315`). | Retain D5 `{rev, argv, exit, stdout_path, stdout_sha256}` plus actual extra fields; outputs `final-census.stdout` and `final-census.json` under out-dir. Must bind live tree to recorded `rev` as above. |

## Verification gaps and commands

**OBS:** The round-20 contract and available `w1/patches` were read, but `W20/tools/` and `W20/verify/` were absent when listed. No round-20 tool, selftest, REA/Ghidra command, Go binary, or build/check was run. No tool was installed or updated. Thus all patch behavior above is source-level evidence only; unpatched contract-only rows remain planned.

Read-only commands with captured exit status:

```text
grep -n 'gate\|probe' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md; echo "EXIT=$?"
EXIT=0

cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -c "
import json
d=json.load(open('.ufo/waves/round-20/claims.json'))
print(type(d))
print(json.dumps(d, indent=1)[:3000])
"; echo "EXIT=$?"
EXIT=0
```

No installs.