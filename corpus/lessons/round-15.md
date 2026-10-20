# Round 15 — installed Go snapshot evidence and outside-review corrections

author: kaidoku-shokunin; 2026-10-20
scope: installed resources and source semantics; no target/provider execution or historical-cause proof.

## Claims

- C1 depth: add a pinned installed Go JSON snapshot inventory and a source-backed selection decision record, separating base bytes, one selected patch diff, requested-version labels, and generic architecture fallback. This deepens held Go ground, not new broad coverage.
- C2 calibration: resolve both outside-routed defects from `round-14-verifier-spotcheck.md`: qualify the virtual-dispatch advisory error by named append-only corrections, and supersede ambiguous QUALITY #16 with explicit manual-only input discipline in #17. The raw quotation gate is unchanged; no automatic representation classifier is acquired.
- Existing owned finite proxies tie at 10; calibration is worked and scores are not inflated. The previously planned real-carrier diagnosis is not asserted: this assignment selects no new real carrier, and historical paths do not silently select one. Installed-data evidence is useful without target execution.

## Gate

### Author-side candidate decisions

| Candidate | Decision | Evidence and limit |
|---|---|---|
| Installed Go snapshot inventory plus source selector decision record | selected for admission after L1 execution | S003/S007 reopened; newly opened S023 actual JSON provides generic bootstrap records. Inventory output and immutable measurements are committed separately after the source work. |
| Requested patch version equals the bytes of a matching patch snapshot | rejected | `GoApiSnapshot.java:111,122-165`: no patch diff can mean base bytes labeled with the requested version; a lower diff can also be selected. Source inference, not a target replay. |
| Snapshot validity merely changes error wording | rejected | `DataTypeMapper.java:176` and virtual dispatch through `GoRttiMapper.java:380-386` to `GoTypeManager.java:405-455`; the latter consults `apiSnapshot`. Prior advisory is explicitly qualified by named append-only corrections. |
| An all-bucket absent-architecture case necessarily makes the current installed snapshot invalid | rejected | The source retains the generic `all` bucket; current installed applicability must be established by inventory, not by one missing platform key. |
| Raw quote failure automatically means fabrication or unsupported-input exit 2 | rejected | The unchanged raw gate does not classify representations. The synthetic rendered/raw controls demonstrate the boundary, not upstream authenticity or semantic truth. |
| New broad Go coverage or historical op cause proven | rejected | Same held surface; installed resources are not historical analyzer logs or a controlled carrier replay. |

### Opened sources and located quotes

Access date: **2026-10-20**. These are source-reading observations, not tool/provider execution.

| ID | URL/path | Contiguous located quote, at most 25 words |
|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `return GoApiSnapshot.EMPTY;` — `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:115`. |
| S007 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` | “Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.” — `Ghidra 12.0 Change History` → `Improvements`, line 585. |
| S023 (new) | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json` | `"Name":"pcHeader","DataType":"*runtime.pcHeader"` — JSON `all.Types.runtime.moduledata.Fields[1]`, raw line 1. SHA-256 `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`. |

Code/archive/JSON quotations are manually checked under QUALITY #1/#17, not submitted as machine-gradeable to the raw heading instrument. S023 was opened with JSON queries and its raw location was independently located with the regex search tool. It is tier A only for the named installed JSON bytes, not for executing compiled classes or Go 1.26 support. No full JSON source is redistributed.

### Registry deltas

Only permitted `used-by` changes on existing rows; statuses and recheck values remain unchanged.

- S003/S007 old: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md`.
- S003/S007 new: the identical old list followed by `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md`.
- S023 is the only new row, kind code, tier A, mined, citing the new knowledge entry and this lesson. No existing immutable field changes, no status/recheck transition, and no rejected row is removed.
- Outside spotcheck lessons remain verifier-owned and unchanged; their citations are read as review evidence, not lane-authored source-use updates.

### Census at round start

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

The command ran before changes; receipt `.ufo/waves/round-15/sources-before.json`. Immutable before/after detailed counts and final census are recorded with execution evidence after all seats finish.

### Outside check

The previous genuine outside check admitted round 14 and routed two status-neutral defects. This round learns both. The current 32 author-dispatched L2 seats do not count as independent discernment reviewers or authorize SHONEN `[x]`. Current-round outside admit/reject sampling remains the separate closure duty.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| provider / incomplete-dispatch trace | `round-14-verifier-spotcheck.md`, routed defect 1; `ReviewGoInference.md:57-61` | QUALITY #1/#5; caught by outside source trace | Named append-only virtual-dispatch corrections in round-14 lesson, r14 entry and LOG qualify flawed advisory. Source call chain includes override and snapshot-backed non-primitive lookup; no target cause asserted. |
| scope / representation ambiguity | prior outside routed defect 2; QUALITY #16 | QUALITY #1 and raw gate documentation; outside check | Superseding #17 requires excluded representations not be submitted as machine-gradeable. Synthetic rendered/raw same-source controls expose failure/success by quote-only change; exact exits are recorded after L1 execution. This documents a submission-policy repair, not an automatic classifier. |
| attribution / edit-anchor provenance | L1 append used an unobserved lesson snapshot tag; edit tool accepted stale tail append with warning | Tool stale-tag policy should have refused; L1 re-read actual lesson and filed tool issue | Preserve the valid append; use only read-returned tags thereafter. No claim that tool rejection prevented the edit. |
| landing / premature used-by reference | registry used-by was extended before new targets were created in the same round | CORPUS row/path existence discipline | All referenced files are created before final census/commit; no intermediate registry is claimed conformant. Future ordering must create targets first. |
| number-drift / survivor | connector reports' 98/114 patch counts and their named corrections; full installed-directory opening | CORPUS count-command rule and adversarial cross-check, not agreement among seats | Reject incomplete previews; retain final inventory output and per-minor histogram. No population accuracy or independent-origin count is inferred from repeated readers. |
| provider / unexecuted static review | First L1 inventory execution at `856d193b8c21d3f7aeff3cb8a27b55a715ab897e`, `verification-initial.json`: exit 1 TypeError sorting dicts | Not caught by source-only reviews; no prior execution was claimed | Diff numeric `patch` was overwritten by a structural dictionary before sorting. Preserve the numeric key and name the structural field separately; rerun only after repair. The retained actual red-before traceback, not a model-only selfcheck, grounds this repair. |

A source-law correction is not a controlled target repair. The raw-input limitation has an executable red exemplar; its opposite accepted form changes only quote bytes. Semantic source corrections rely on the retained, inspectable dispatch chain rather than a fabricated runtime experiment.

## Integration boundaries

Initial lane state was clean at `9719dd232687f5ee78a4ed323b37f8810e833d10`. No earlier round-15 `lane-dead-no-report` match was found; the bounded watchdog search showed the current launch only. The prior verifier file and advisory report remain untouched. L1 holds the canonical planner seat; bounded data walks are carried by connector/scout/revenger seats. One validator-approved 32-seat batch uses the live role table, no model parameters. No client/auth configuration or agent database was opened; no sibling gate or domain target was executed, and no fleet runtime was modified. No tool installs/updates.

## Advisory adjudication before measurement

`claims-review.json` records these decisions without changing the two axes:

- C1 novelty is not the previously known filename list or selector law.
  Persisted per-file data digests, patch coverage, generic bootstrap records,
  and requested-label/fallback-byte distinction carry the deepening.
  `AttackNovelty.md` drove this narrowing; file presence alone cannot prove it.
- Some connector reports gave unsupported partial counts (98 or 114) rather
  than the complete filename census. Their later corrections are retained;
  the final L1 inventory, not a vote or a tool preview, governs the admitted
  count. This is a survivor/number-drift mistake, caught by conflicting
  reports and full-directory source opening.
- `AttackCausality.md` correctly rejects historical-cause and snapshot-only
  repair claims. Its assertion that missing JSON “only decides which
  message appears” is not adopted: an alternative counterfactual failure
  does not remove the snapshot prerequisite from virtual type lookup.
  Neither that report nor a source-model prediction is a runtime experiment.
- `AttackManualBoundary.md` exposed an overly categorical first draft.
  The final #17 retains #16's still-valid fidelity obligations, names actual
  heading forms, distinguishes raw-copied tags from rendered text/entities,
  and voids any raw-machine result on an excluded claim. Excluded inputs may
  receive ordinary 0/1/2; there is no unsupported-representation classifier.
- L1 changes the rendered fixture's quote ID to equal the raw fixture's ID.
  The final pair therefore differs only in quote text; earlier seat-reported
  hashes/IDs describe drafts, not the pinned final pair. The final frozen
  expectations pin both manifests and their shared source.
- SHONEN's title and one-line evidence format are canonicalized without a
  mark upgrade. Footer substance moves into box-1 evidence; LOG records the
  deliberate edit. SHONEN is not an append-only corpus lesson.

No capability is added to the repertoire or counted twice; C2 discharges the
outside duties through improved calibration of the active wording.
Current-round independent closure remains necessary.

## First execution failure retained

L1's first inventory execution at source revision
`856d193b8c21d3f7aeff3cb8a27b55a715ab897e` returned exit 1 before producing
JSON: `TypeError: '<' not supported between instances of 'dict' and 'dict'`
at `scan_directory` sorting `item["patch"]`. `parse_diff` overwrote its
numeric patch version with structural counters. The second determinism
invocation failed identically; both original outputs/exit codes are retained
in `.ufo/waves/round-15/verification-initial.json`, not silently replaced.
Immutable measurements in that same attempt succeeded; later checks had
not yet run when the orchestration cell stopped parsing empty stdout.

The assigned tool owner repairs the field collision, without executing tests.
No initial inventory success is claimed. Final measurements and checks name
the repaired source revision, with the original red-before evidence preserved.
