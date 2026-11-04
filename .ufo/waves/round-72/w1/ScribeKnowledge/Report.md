# ScribeKnowledge scoped report

## Behavior and axes

Produced the knowledge draft `2026-11-04-r72-checker-env-capsule.md` in this directory for L1 integration, not in corpus. Axes: factual accuracy, full requested coverage, provenance traceability, bounded writes. The entry includes scope/nonclaims, exactly seven tamper rows with named failures, A10/A11/A8 witness mapping, all four requested limits, and line-start source/verified-at/recheck fields. Every behavioral statement is anchored to lane source lines or a retained receipt.

## Gates and evidence

No instruments, validators, tests, builds or alternate runtime were invoked; this scribe does not claim a gate passed. Read existing source and retained receipts through read/grep tools, and read skill://godspeed, skill://agent-self-evaluation, and /home/vgpnk/.omp/agent/RULES.md. No tool installations or upgrades.

Exact shell command executed, from lane cwd:

```sh
mkdir -p /fast/scratch/hyaku/kaidoku-r72/ScribeKnowledge/ && S=/fast/scratch/hyaku/kaidoku-r72/ScribeKnowledge/ && trap 'rm -rf -- "$S"' EXIT
```

Outcome: successful, no output. Shell EXIT trap deleted the empty seat scratch immediately; no scratch artifacts were produced or needed copying. No git/jj commands executed.

## Findings and conflicts

1. A11 source is narrower than its prose: `tools/round-72/seam-probe.py:267-293` checks shim HOME/TMPDIR under `work_abs`, not the checker's run root, and consumes the checker JSON summary rather than parsing the checker JSONL. The knowledge table explicitly preserves this distinction; A8 independently parses route JSONL (`:478-504`). Frozen predicate wording is: “HOME and TMPDIR under the checker's run root” (`plans/round-72-claims.md:43-45`). These are not interchangeable evidence.
2. A missing digest is not evaluated (`null`) rather than true (`tools/round-72/capsule_audit.py:129-134`); the draft does not call such a capsule digest-verified.
3. ScoutSource-6 message: “Next free SOURCES id is S275 (max existing row is S274 at corpus/SOURCES.md:191; S275 and S276 are both absent). I am writing S275 in this wave. Use S275 for the proc_pid_environ(5) row if you cite it; S276 stays free if your entry needs a second source.” This overrides the assignment's provisional S276 as explicitly permitted. Source seat reports HTTP 200, fetched 2026-11-04, snapshot sha256 93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46. The proposed receipt directory `.ufo/waves/round-72/w1/ScoutSource/` was not yet present when read; draft labels this peer-reported provenance, not locally observed snapshot evidence. Linux proc(5) has split content: the requested paragraph is in proc_pid_environ(5), per source seat.
4. Retained base receipt records checker acceptance but audit rejection with four failures, not only canary (`.ufo/waves/round-72/l1/pre/c3-at-base.json:2-24`). Draft preserves this.

## Touched surfaces and out of scope

Only the knowledge draft, this report and `.ufo/waves/round-72/w1/ScribeKnowledge.md` are authored by this seat. Product code, frozen instruments, corpus, judge, claims, routes and axis definitions are unchanged. No commit/push/publish/deploy, no subagent dispatch, no broadcast. The bounded scratch exception specified by the assignment was used solely for the empty directory lifecycle above.

L1 integration gates: reconcile S275 and source receipt after source-seat landing; measure frozen pins and execute the three declared claim gates under the main agent's authority before claiming round success. This report does not adjudicate those gates.

## Self-evaluation

Accuracy 4/5: code/receipt anchored, but external snapshot is peer-reported and explicitly pending. Completeness 5/5: both tables, four requested limits, scope/nonclaims and provenance trio included. Clarity 4/5: A11 implementation/predicate distinction adds necessary density. Actionability 4/5: recheck commands are precisely referenced in frozen plan rather than reproduced with machine-specific arguments. Conciseness 4/5: citation density lengthens the entry. Overall 4.2/5. Highest-impact improvement: replace provisional source receipt attribution with the retained source-seat receipt once available; main should preserve the A11 distinction during integration. User agreement expected because execution claims are intentionally withheld.

Report: .ufo/waves/round-72/w1/ScribeKnowledge/Report.md
