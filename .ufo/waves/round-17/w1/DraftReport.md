# DraftReport — kaidoku round 17, scribe seat (author-side advisory)

Scope: draft skeleton of `.ufo/reports/round-17/kaidoku.md` at `.ufo/waves/round-17/w1/draft-report.md` (written), plus baseline checks that bear on the C1/C2 drafting slots. No REA analyze/search/decompile, no Ghidra, no carrier execution, no subagent dispatch. Baseline revision: `b563c799d97774aae4351276fe43cb897311e349` (claims.json `baseline`).

## Findings

### 1. Draft skeleton (written)
- File: `.ufo/waves/round-17/w1/draft-report.md`. Section order as assigned: Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN (4 boxes), Stale-lane, Tool installs/updates, Cross-domain evidence, Wave stats. Every unmeasured value is a `{{SLOT: …}}` marker; none is filled with a guess.
- Vocabulary: assignment says "Trend verdicts"; prior fleet reports use "Axis verdicts" (`.ufo/reports/arc3-loop1-round11/kaidoku.md`, section "Axis verdicts (per-axis, no scalar)"), and the round-14/15/16 verifier spot-checks use "Per-axis and learning-trend verdicts" / "Axis and trend verdicts" (`corpus/lessons/round-16-verifier-spotcheck.md:162`). The skeleton uses "Trend verdicts" with a per-axis table inside; L1 may prefer the existing heading.
- Stale-lane line wording follows the round-16 precedent (`corpus/lessons/round-16.md:69-71`), slot left for L1 to state lane status.

### 2. Baseline temporal-sweep count (C1a) — observed at `b563c79`
Contract sweep scope (`contract.md:90-97`: LOG.md, SCORECARD.md, corpus/lessons/round-16.md, SKILL.md, `.ufo/waves/round-16/verification.json`):
- `corpus/lessons/round-16.md:154` "All producer/fixture pins remained unchanged during execution." — matched.
- `.ufo/waves/round-16/verification.json:419` `"pins_unchanged_during_run": true` — matched.
- LOG.md, SCORECARD.md, SKILL.md: 0 matches.
- In-scope baseline N = **2** (observed via `git show`/`grep -Eic`; the tool itself is not yet run).

### 3. Sweep scope gap (observation) — un-swept site
`git grep` over the full baseline tree finds a site outside the contract scope:
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` "Producer and fixture pins were unchanged during" — matches the sweep regex, but the file is not in the temporal-sweep scope list (`contract.md:90-97`). It would be missed by `temporal-sweep.py` as specified.
- Other repo hits (`.ufo/waves/arc2-loop1-round1/CR6.md:157`, `arc2-loop1-round3/S2.md:222`, `arc3-loop1-round3/claims/c2/EX-22/aftersmoke.md:58`, `arc3-loop1-round6/claims/verdicts/CR-5.md:434`) are older-round wave files, not round-16 claims; out of scope by contract, not judged here.
- **Recommendation to L1 (not an edit):** add `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` to the sweep scope or pass it via `--extra`; the in-scope count would otherwise undercount.

### 4. Verifier claim vs. baseline text (observation, calibration relevant)
`corpus/lessons/round-16-verifier-spotcheck.md:183` says "The report, lesson, LOG and scorecard say pins stayed unchanged during execution." At `b563c79`:
- LOG.md and SCORECARD.md contain no matching phrase (`git show` + grep, zero hits for "during" with pin/unchanged/stable).
- The round-16 report file is not present: `.ufo/reports/` lists no `round-16` directory (`.ufo/reports/` listing at baseline).
- So the verifier's LOG/scorecard/report attribution is **not reproduced** at this baseline. The reproducible sites are items 2 and 3. Inference: the verifier may have read a pre-`b563c79` state or paraphrased; L1 should treat its LOG/scorecard/report clause as unverified until a named correction cites an exact site.

### 5. Invocation-audit baseline (C1b) — observed approximation
- SKILL.md rows matching `(probe|gate|tool) / kaidoku` in 2nd cell: **7** (`git show b563c79:SKILL.md`, rows at :447-450 and others). Exact tool count pending its run.
- Labelled-unexercised rows: SKILL.md at baseline contains **0** occurrences of `unexercised` (grep). Inference: every non-matching row falls into `unlabelled_variant` under the contract classes.
- Citation-drift row `SKILL.md:448` (`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> …`) is the surviving variant the verifier names (`round-16-verifier-spotcheck.md:184`); it has no `-I` and no label. Whether it matches an exercised argv depends on the receipts the tool finds; not verified here.

### 6. Go source anchors (C2) — observed, Base-src.zip
From `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`:
- `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`.
- `GoRttiMapper.java:171` `Msg.error(… "Untested Go version [%s]" …)`.
- `GoRttiMapper.java:359` "Missing Go bootstrap type info, unable to extract Go RTTI info."
- `ghidra/app/util/bin/format/golang/GoVer.java:46` `public static GoVer parse(String s)`.
- These match the message strings in the pilot logs, so the prediction anchors exist. Not yet checked: `GoVer` normalization at the lines contract.md:62 expects (`predict.py`); left to the executor.

### 7. Pilot observations (not final measured runs)
- `.ufo/waves/round-17/pilot/shfmt-log/ghidra.log:83-84`: `Untested Go version [1.27.0]` then `Missing Go bootstrap type info`. Consistent with the C2 prediction for an out-of-range carrier.
- `.ufo/waves/round-17/pilot/esbuild-0.25.12-log/ghidra.log:64,67`: `Using Go API snapshot for version 1.23.12`, `Go version 1.23.12`. Consistent with an in-range carrier.
- `pilot/README.txt`: 1 s polling copy; no pre/post carrier pins recorded in the pilot; REA deletes its runtime root at close, so the final poll can miss lines. The final `carrier-run.py` must record pins and treat log capture as bounded (`contract.md:31-49`).
- `pilot/SHA256SUMS`: six entries; `esb.exit` and `shfmt.exit` both `exit=0`.

### 8. Wave stats (observed from artifacts, not outcomes)
- `wave1-spec.json`: 78 items; roles scout 20, executor 14, reviewer 12, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2.
- `wave1-dispatch.json`: `counts` spawn 78 / resume 0 / total 78. DraftReport entry at `wave1-dispatch.json:1190-1192`, agent `scribe`.
- `wave1-dispatch-attempts.json`: attempt 1 `refused: 78`, attempt 2 `refused: 78`, attempt 3 `refused: 0` (lines 5, 10, 15). The file does not record a cause; I did not investigate it. [INFERENCE] the first two attempts were refused by a host or harness guard, and the third was accepted.
- `w1/swarm-registry.json`: 78 members, all `kind: spawn`.

### 9. Tool installs/updates
- This seat: **none**. No install, upgrade, or pacman command was run. Read-only `git show`, `git grep`, `git ls-tree`, `unzip -p`/`unzip -l`, `grep`, `sed`, `python3` JSON reads only.

### 10. Cross-domain
- The pilot esbuild carrier is from a kimi-code pnpm store (path in `pilot/README.txt`); the shfmt carrier is `/usr/bin/shfmt`. Carrier provenance is outside kaidoku's domain; C2 needs a pacman-owner check (contract.md:110-113), which I did not run.
- No sibling gate, agent DB, credential file, client routing, or host service was accessed.

## Limits
- Baseline counts (items 2, 5) come from grep/`git show` approximations of the contract regexes. The contract tools are not yet written (`.ufo/waves/round-17/w1/` contains only the registry before this seat); exact counts must come from the landed tools.
- Items 3-4 are scope-observations at one revision; they do not prove the verifier intended the knowledge file.
- No REA or Ghidra output was produced or read beyond the pilot logs already on disk.
- Draft slots are unfilled by design; L1 supplies measured values and the final commit hashes.

## Files written
- `.ufo/waves/round-17/w1/draft-report.md` (skeleton)
- `.ufo/waves/round-17/w1/DraftReport.md` (this report)
