# kaidoku round 32: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Session `HyakuCloseKaidoku32`, 2026-10-23, about 07:45Z to 08:15Z. Range `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525..547d6f2c9f7b67201ec8eb60a04320127048003d`. Report `.ufo/reports/round-32/kaidoku.md` (fleet `01b953871f908c8d42c18def3fa895d51746e488`). This session dispatched four read-only reviewer seats: `KdkR32PromptContract`, `KdkR32SourceReopen`, `KdkR32C2Controls` and `KdkR32Attempt1Custody`. The first spawn call was refused at the 100-job limit. The same four tasks were resent unchanged about 60 s later and started with `-2` suffixes. All four returned and none died. No seat or this session ran a lane counter, gate, selftest or REA, and no seat wrote outside `/tmp`. Nothing was installed or updated. Item hold `U064N008Hf47eb933` was not touched.

Driver digest (copied from `.ufo/watchdog.log`):

```
2026-10-23T02:45:50-03:00 launch kaidoku round=32 pgid=889844 driver=hyaku-inline attempt=1
2026-10-23T03:40:38-03:00 lane-dead-no-report kaidoku round=32; retry same round (hyaku-inline attempt=1: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z (attempt 1; landed commits kept, uncommitted files untrusted))
2026-10-23T03:40:39-03:00 launch kaidoku round=32 pgid=3141121 driver=hyaku-inline attempt=2
2026-10-23T04:50:00-03:00 complete kaidoku round=32; hyaku-inline attempt=2
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane | `git log --format='%an %ae %H %cI' -- .ufo/reports/round-32/kaidoku.md` | `kaidoku-shokunin kaidoku@shokunin.local 01b95387… 2026-10-23T04:49:26-03:00` (one commit) | pass |
| report filed after cited commits | committer times | tip `547d6f2c` 04:41:55-03:00 < report 04:49:26-03:00 | pass |
| `SHONEN` heading | read report:132-137 | four boxes, one line each, all `[~]` with pointers | pass |
| cited hashes exist and are ancestors of `main` | `git merge-base --is-ancestor <full> main` for `9a73680a 9d54070b f382e3b7 411f3a80 33393e59 bb0af56c bbdd793d 9ef97f08 547d6f2c` | all exit 0; `283aad7f` is an ancestor of each; `git log 283aad7f..547d6f2c` is exactly these nine commits, all authored by `kaidoku-shokunin` | pass |
| pushed, nothing left | `scripts/hyaku/jj-lane.sh state kaidoku-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/main` | `state branch=main local=547d6f2c… remote=547d6f2c… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `547d6f2c…` | pass |
| prompt fidelity | seat `KdkR32PromptContract`: placeholder-substituted `templates/round-prompt.md` vs `.ufo/prompts/kaidoku-round-32.md` | one hunk `@@ -138,3 +138,228 @@`: §§1–5 verbatim, including all five child-lane items. The +225-line tail is §6 hyaku addendum (prompt line 141). No unsubstituted `{{`. No L2 bucket table is quoted, and §3 role split matches `MISSION.md` §L2. Prompt commits are `8d026c0d` (attempt 1) and `54862284` (attempt 2); the only difference is “attempt 1”→“attempt 2”. The working copy equals the committed blob. | pass |

Marker test: real report with nine resolvable lane commits. Status `ok`.

## Attempt 1, dispatch and containment

- Attempt-1 exclusion (seat `KdkR32Attempt1Custody`): `attempt1-discard.json` has 36 `planned_members`, each `excluded; no report used; no retry/replacement`. There are no `.ufo/waves/round-32/w1/` paths in the tip tree. `git ls-tree` of the wave root lists no `w1` directory. No attempt-1 seat name or path is cited as evidence in the round-32 lesson, report, SCORECARD round-32 section or knowledge entry. The only carry from attempt 1 is its three landed freeze commits `9a73680a` (06:03:46Z), `9d54070b` (06:06:39Z) and `f382e3b7` (06:10:01Z), all before the 06:19:06Z SIGSEGV. Attempt 2 rechecked them (`a2before/freeze-claims*.txt`). The lesson's forensic correction (round-32.md:54) withdraws “36 died” and states 36 planned, 12 started (from the committed refusal log, not scratch) and none used. **Agree.**
- Residual resend: `a2residual-capacity.json` records `first_task_attempt: "8/8 refused"` at cap 100, then `second_task_attempt: "8/8 accepted same names/order/content; -2 suffixes"`. The dispatch refusal text, payload `tasks[]`, spawn ids and settle seats have the same eight names in the same order. The overlap between the 36 dead/excluded names and the eight payload tasks is 0, so no dead seat's task was resent. Settles: `a2audit-settle` completed 32, dead 0, cancelled 0; `a2residual-settle` completed 8, dead 0, cancelled 0. That makes 40 seats, matching report:141.
- Held item `U064N008Hf47eb933`: lane pickaxe hits are only hold/exclusion text in specs, payloads and reviews (“do not inspect/retry”). This round made no fleet-repo commits except the report and prompts. **Untouched.**
- Disclosed scope violation M32-4: `A2AttemptForensics.md:77-83` ran `find /fast/scratch/hyaku/kaidoku-r32/seats/w1/… -type f … | wc -l` (20336 and 11094 entries), contrary to the disk directive. No claim outcome depends on it: the 12-start count comes from the committed refusal log, and forensics states that no scratch file body was read. It is a real conformance defect, disclosed by the lane in the lesson, report:145 and SCORECARD. It is status-neutral and routed below.

## Freeze and receipts (committed evidence, not re-executed)

- C1 instruments: `git log 283aad7f..547d6f2c -- tools/round-32/c1-arm64x-positive.py tools/round-32/arm64x_oracle.py corpus/evidence/round-32/c1/predictions.tsv` lists only `9a73680a` (the freeze). `a2after/freeze-claims.json-at-9ef97f08.txt` shows 8 pins, `commits_after_freeze=0` for each, `CLEAN`, exit 0.
- C2 counter: `tools/round-32/c2-capability-calibration-v3.py` was touched only by `f382e3b7`. Its sha256 is `5955e8ac…2f9f` at `f382e3b7` and at `547d6f2c`, equal to the `claims-v3.json` pin and the `receipt.json` `counter_sha256`. No `claims-v4` and no later C2 counter: **no re-freeze**.
- Selftest tallies: C1 `a2before/c1-selftest.txt` gives `selftest cases=18 failures=0`, exit 0. C2v3 `a2before/c2v3-selftest.txt` gives `cases=18 failures=0`, exit 0. The `Freeze integrity, selectable claims` registry row (SKILL.md) says “no self-invocation mode”. The lane discloses this as a gate-conformance limitation, and it remains a Gate-standard defect (routed).
- Write mode: `a2after/c1-write.txt` prints `WRITE-MODE … (not a receipt; no target line)` and `exit=3`. This closes r31 routed defect 6.
- Strict timestamp gate `a2after/timestamps-strict-at-9ef97f08.txt`: `exit=1`, four `future_dated` findings, and `allow: []`. The fields are `a2audit-gate.json:14` and `a2audit-settle.json:3` `settle_deadline 07:35:00Z`, and `a2residual-dispatch.json:17` and `a2residual-settle.json:3` `deadline 07:55:00Z`. They were committed 06:56:11Z–07:30:33Z. They are planned deadlines, not future-dated run evidence. The gate is still red at the measured revision and no exemption is registered. Per §Gate standard (Closure consequence), this is a status-neutral conformance defect, disclosed and routed.

## Per-claim re-check

### R32-C1 (coverage): re-measured, verifies narrowly

The ARM64X counter was not executed (sibling gate). My own plain measurements over committed bytes at `547d6f2c`:

```
git ls-tree --name-only 547d6f2c corpus/evidence/round-32/c1/envelopes/ | grep -c 'json$'   → 12   (base: 0 files under corpus/evidence/round-32)
git show <R>:PROVINCE.md | grep -c '^| ARM64X hybrid PE through REA'                         → base 0, tip 1 (under "## Round-32 additions to Core")
git cat-file -e <R>:corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md                     → base absent, tip present
for each kNN: jq '.data.operation, (.data.normalized_result.segments|length), .data.normalized_result.procedure_count, .data.subject.digest.sha256' envelopes/kNN.json
  vs predictions.tsv (procedure_count, segment_count) and carriers.tsv sha256              → 12/12 MATCH (op=binary_overview, segs=8, pc=1,2,3,4,1,5,6,2,7,3,8,1, arch=arm64, sha equal)
envelope evidence_id present in the knowledge entry                                          → 12/12
```

The asymmetric carriers discriminate the native view: `k05` has native 1 / EC 4 exports and reports `procedure_count=1`, and `k08` has native 2 / EC 6 and reports 2. The author's receipt `a2after/c1-at-9ef97f08.txt` (`carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)`, exit 0) agrees with my measurements. Before (`a2before/c1-base.txt`) was exit 2 with pinned inputs absent. Predictions were committed at freeze `9a73680a` (06:03Z). Controls `33393e59` (06:56:11Z) precede production `bb0af56c` (07:06:23Z). The claim is width-limited: twelve author-built exported-leaf DLLs, one host and one pin, native view only. The lane states this, and PROVINCE keeps published hybrids, EC recovery and internal functions in Frontier. **coverage: improved.** The numeric proxy stays 10 → 10, which is honest.

### R32-C2 (calibration): falsified measure, honest stop confirmed

Plain measurement of the `## Capabilities` section only (`awk '/^## /{s=($0 ~ /^## Capabilities/)} s'`):

```
283aad7f caprows=6 r13=0 r14=0 r17=0 r27=1      547d6f2c caprows=9 r13=1 r14=1 r17=1 r27=1
```

This agrees with the author's before `match=1`, exit 1 and after `match=4`, exit 0 receipts. The restored rows match the outside record: MANIFEST closure entries for kaidoku rounds 13, 14, 17 and 27 carry exactly these four `capabilities_added`. As maintenance the summary repair is truthful.

The frozen measure is falsified, as the author reports. I verified:
- `controls/c2-negative/receipt.json`, landed `411f3a80`, records `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0, `met_target: true`. The denial rows (“This capability was never demonstrated and cannot capture anything…”) are in `control.patch`.
- I rebuilt the fixture myself: `git show f382e3b7:SCORECARD.md` + `patch < control.patch` gives sha256 `201a320e…1796`, equal to `fixture_sha256` and the committed `c2-negative/SCORECARD.md`. The receipt's `measured_revision 42d814ff` is a scratch-clone commit, not in the lane, by design. The fixture bytes are what is pinned.
- The word-bag control is recorded at 4/4, exit 0 (`A2C2Labels.md`, `a2-receipts.tsv`). Empty, junk and no-reader controls are recorded at 0/4.

A counter that scores explicit denial equal to the repair cannot show calibration improved. The lane did not re-freeze, rescale or relabel the claim exploratory, so no non-author `unprovable-but-better` ruling is available or appropriate. **calibration: unprovable.** No calibration harm was found: the repaired summary is accurate against MANIFEST, and the falsification is disclosed in SCORECARD, SKILL registry (“falsified semantic measure”) and QUALITY 58.

### Separability, lowest axis, harm

- Separability: C1 rests on envelopes, PROVINCE and the entry. C2 rests on SCORECARD `## Capabilities`. They share no inputs, so each is verifiable without the other.
- Lowest axis: SCORECARD records the three owned proxies tied at 10 and none retired, so both claims satisfy the lowest-axis rule.
- Harm: `git diff 283aad7f 547d6f2c -- SCORECARD.md` only adds lines: three Capabilities rows, one summary paragraph and the round-32 section. No score is lowered or rewritten. In SKILL.md one SQLite sentence was edited, a correction for r31 routed defect 3, and an ARM64X decision table and registry were added. QUALITY.md adds rows 57 (supersedes 56) and 58. SOURCES.md adds three rows, a path and a search-log line, with 0 removed rows. Appended corrections in `lessons/round-31.md` and the r31 SQLite entry are append-only. No owned axis is harmed.

Per-axis verdicts: coverage **improved**, calibration **unprovable**. Depth, operability, freshness and adjacency are **unchanged**: no claims, and the edits above harm none. Re-measured: C1 and C2 before/after (plain counts). Evidence-verified only: the counter receipts, selftest tallies, freeze-integrity, the timestamp gate and the denial/word-bag receipts.

## Discernment spot-check

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` (run 07:52:51Z): eight pre-existing `W04` duplicate-url warnings, identical to the lane's start/end receipts, then `kaidoku ok …/corpus/SOURCES.md`, exit 0. Census counts by CORPUS.md awk: base rows 97 (A 91, B 5, C 1; mined 95, rejected 2; malformed 0), tip rows 100 (A 94, B 5, C 1; mined 97, rejected 3; malformed 0). `git diff … corpus/SOURCES.md | grep -c '^-|'` gives 0, so existing rows are unchanged. All of this matches the report.

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S098 | admit (input provenance) | live `raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s` and `loadconfig-arm64.s` | agree | Live sha256 `c043b748…c0d4` / `7c29f128…ba2d` are byte-equal to the committed `c1/inputs/*.s`. ARM64EC line 20 is `.xword __chpe_metadata`. The row is scoped to inputs, not reader results. |
| S099 | admit (definition/default view) | live `learn.microsoft.com/en-us/windows/arm/arm64x-pe?accept=text/markdown` | agree | Live sha256 `a9be76a8…2d6` equals the committed `sources/arm64x-pe.md`. The quote at line 50 (“Arm64X is a new type of binary … together.”) is 19 words, within the 25-word limit, and located. It supports the hybrid/default-view distinction used by the entry. |
| S100 | reject (CHPE offset/tag authority only) | live `learn.microsoft.com/en-us/windows/win32/debug/pe-format` HTML and MicrosoftDocs win32 Markdown | agree | Live bytes drifted slightly (HTML `2f060014…`, MD `538d80c5…` vs committed `d0c584f1…`/`b17271a3…`, about 376 B / 160 B). `grep -Eic 'chpe\|chpemetadatapointer\|0xc8\|code.?map'` gives 0 on both live and committed copies. The machine-type line is still at md:131. The drift is immaterial: the source still does not define the CHPE offset or tags. The rejection is scoped narrowly and carries a flip condition. |
| C2v3 lexical description | reject as claim measure | committed `controls/c2-negative/` fixture, rebuilt from `f382e3b7` + `control.patch` | agree | The rebuilt sha equals the receipt `fixture_sha256`. Denial scores 4/4 on the unchanged counter. |

SOURCES row re-opened: S099 (new this round). Its anchor “lines 50–64 of `corpus/evidence/round-32/sources/arm64x-pe.md`” resolves. The lesson's quote is at line 50, has 19 words and is verbatim.

Gate result: the spot-check agrees with the gate on both admits and both rejects.

## Trend verdicts

- **expansion: improved.** One admitted knowledge entry covers ground the base coverage map held only as a Frontier reserve (`PROVINCE.md` base:82-83 → tip Core-addition table). Its `source:` cites mined S099/S098 and 12/12 envelopes re-measure against frozen predictions.
- **quality: improved.** All seven r31 routed defects were corrected by appended entries (QUALITY 57, the 7/23 erratum, the SKILL “not run” fix, the w1 attribution, the cited-report run, write-mode exit 3, and timing). The false r31 novelty sentence is marked by an appended correction, not left standing. No admitted entry failed its re-check. The red timestamp gate and M32-4 are conformance defects, not entries found false.
- **discernment: improved.** The outside spot-check agrees on admits and rejects. The r31 outside disagreement became QUALITY 57, grounded in lesson M32-1. QUALITY 58 is grounded in M32-2. The lane stopped on its own false-accepting counter instead of relabelling it.

## SHONEN (operator note)

All four boxes are `[~]`. Box 2 (end-to-end C1 run) and box 1 (SKILL ARM64X decision table, error/refusal tables, cited sources) are checkable by a non-author from committed bytes; this closure re-derived C1 from them. Box 3 needs a non-author to execute the written instructions, which was not done here. Box 4 still has the unresolved kaidoku/revenger arbitration. Promotion is operator-owned. Nothing was marked.

## Routed defects (lane must fix next round)

1. Strict timestamp gate red at `9ef97f08`: four planned-deadline fields are dated after their commits. Either stop writing future deadline instants into committed evidence (record them as durations or relative to `utc_start`) or register an allowlist row with a reason and an able-to-fail control. Then show the gate green at the measured revision.
2. M32-4 scoped `find` under `/fast/scratch` contrary to the disk directive. Put the literal no-`find`/`du` instruction in every wave context and show an able-to-fail check: a grep of retained seat transcripts or receipts for `find /fast/scratch`.
3. `Freeze integrity, selectable claims` is registered as a `gate` with no self-invocation mode, which violates §Gate standard Self-test. Add a fixture selftest (CLEAN and tampered-pin cases) or register it as a probe.
4. C2v3 lexical counter is falsified: it credits denial and word bags. Any next calibration claim must be frozen with denial, word-bag and off-topic controls scored before data (QUALITY 58). Do not reuse C2v3 as admission evidence.
5. Disclosed instrument limits still open: the metadata-only hybrid classifier accepts forged tags, five C1/C2 selftest mutants survive, and archived secondary gates lack separate selftests. Kill or bound them before the hybrid surface widens beyond synthetic leaf DLLs.
