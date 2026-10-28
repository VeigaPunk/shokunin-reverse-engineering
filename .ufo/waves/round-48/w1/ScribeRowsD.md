# ScribeRowsD — round 48 third split

## Behavior, gates, and axes
- Direct contribution: depth (candidate registry cells); coverage and calibration were not independently advanced by a counter or fixture run.
- Read the frozen claims file in full before other commands. Declared freeze: `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`; freeze-resolution and rule details are recorded in sibling receipts/reports, not rerun as claim evidence here.
- Disk guard: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` ran, exit 0; output showed scratch at 33% used / 545.2G free.
- Source-level inspection of the frozen SKILL registry shows rows for tools/round-46/{attest,census,gate,registry}.py and tools/round-47/{exact,record}.py. Draft candidate cells for these six paths are in `ScribeRowsD/cells.md`.
- **No frozen counter execution, self-test, mutation battery, fixture, or semantic result was produced.** Existing sibling reports indicate no assigned failing-row population was measured. Accordingly these cells are candidate replacements for a draft slice; they must not be interpreted as measured failing rows or evidence that a gate passes.

## Findings
The registry counter's frozen acceptance requirement is semantic: exact census path set, all three digit segments with their claimed meaning classes, and distinct meanings. The candidate cells articulate 0 success, 1 not-met, and 2 unevaluable rather than just listing digits. This does not establish compatibility with each source tool's exact exits; review against the corresponding source and the complete frozen census is required before landing. Scope was split by an alphabetical path filter over round-46/47 rows, not by observed counter failures, because the existing row reports provide no failure enumeration.

## Touched surfaces and exclusions
Written only:
- `.ufo/waves/round-48/w1/ScribeRowsD.md`
- `.ufo/waves/round-48/w1/ScribeRowsD/cells.md`

No product/frozen paths, sibling lanes, state/watchdog, fleet files, or git history were changed. No tools installed. No fixture repo or scratch was created; therefore no scratch cleanup was required. C1 battery and all C2 checks: **not run**. No claim gate is reported met.

## Evidence limits
One read-only source enumeration was captured via `git show <freeze>:SKILL.md | grep -E '^\| `tools/(round-4[67]|round-48)/'` (exit 0). It emitted registry rows but terminal output was truncated; the relevant six paths were visible. The attempted JSON wrapper captured the same command string, exit 0, a UTC timestamp and stdout SHA-256, but stdout was truncated by the tool, so that hash is over the captured/truncated stdout and is not a full-output receipt. No complete command receipts were created for counter gates. No assertions beyond the observed file text and command output are made.

## Artifacts
- Report: `.ufo/waves/round-48/w1/ScribeRowsD.md`
- Draft cells: `.ufo/waves/round-48/w1/ScribeRowsD/cells.md`
- Receipts: none suitable as complete gate receipts.
