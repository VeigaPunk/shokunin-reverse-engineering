# kaidoku round 17 — draft skeleton (author-side, not the fleet report)

Target report: `.ufo/reports/round-17/kaidoku.md` (L1 integrates this draft; not final).
Wave: `kaidoku-r17-w1`. Axes: calibration (C1), depth (C2). Claims: `.ufo/waves/round-17/claims.json`.
Slot syntax: `{{SLOT: ...}}` = value L1 fills from its own measured run. Nothing in a slot is observed yet.

## Work performed

- C1 — calibration: discharge R16-PROVENANCE and R16-INVOCATION (claims.json C1; contract.md:12 pins, :80 invocation audit, :90 temporal sweep).
  - Temporal-stability assertion sites before → after: {{SLOT: sites N -> 0 via temporal-sweep.py at round-17 rev}}
  - Unlabelled registry variants before → after: {{SLOT: M -> 0 via invocation-audit.py}}
  - QUALITY row 19 presence: {{SLOT: 0 -> 1}}
- C2 — depth: Go carrier bootstrap discrimination with retained Ghidra analyzer log (claims.json C2; contract.md:31 carrier-run, :51 log-extract, :62 predict, :75 compare).
  - Pinned carriers: `/usr/bin/shfmt` (sha256 `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459`, go1.27.0-X:nodwarf5, out of range) and esbuild 0.25.12 (sha256 `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014`, go1.23.12, in range). {{SLOT: confirm pins pre/post on final runs}}
  - Retained carrier runs with receipt + prediction comparison: {{SLOT: 0 -> N, target >= 3}}
  - Prediction mismatches (reported, not hidden): {{SLOT: list}}
- Tool work (contract.md:12-115): {{SLOT: tools landed, each with --selftest result line}}
- Pilot (not final measured runs): `.ufo/waves/round-17/pilot/README.txt`; SHA256SUMS lines 1-6.

## Landed changes

- {{SLOT: work commit hash and file list}}
- {{SLOT: knowledge entry `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (C2), if admitted}}
- {{SLOT: QUALITY row 19, SCORECARD capability row `retained REA Ghidra-session log`, SKILL registry rows}}
- {{SLOT: append-only corrections for round-16 temporal assertions (C1a)}}
- Records commit: {{SLOT: hash}}

## Before → after measurements

| claim | before | after | evidence (argv / receipt path) | measured at |
|---|---|---|---|---|
| C1a temporal sites | {{SLOT}} | {{SLOT}} | {{SLOT: temporal-sweep.py output}} | {{SLOT}} |
| C1b unlabelled variants | {{SLOT}} | {{SLOT}} | {{SLOT: invocation-audit.py output}} | {{SLOT}} |
| C1c QUALITY row 19 | 0 | {{SLOT}} | {{SLOT}} | {{SLOT}} |
| C2 retained Go carrier runs | 0 | {{SLOT}} (target >= 3) | {{SLOT: receipt.json paths + sha256}} | {{SLOT}} |
| C2 capability rows | 4 (+r13/r14 appended) | {{SLOT}} (target +1 only if receipt validates) | {{SLOT}} | {{SLOT}} |

Pilot observation (not a measured run; logs under `.ufo/waves/round-17/pilot/`):
- shfmt: `shfmt-log/ghidra.log:83` `ERROR (GoRttiMapper) Untested Go version [1.27.0]`; `:84` `WARN ... Missing Go bootstrap type info`.
- esbuild: `esbuild-0.25.12-log/ghidra.log:64` `Using Go API snapshot for version 1.23.12`; `:67` `Go version 1.23.12`.
- Pilot had no pre/post carrier pins and a 1 s polling copy: lines written after the last poll may be missing (pilot README.txt).

## Sources & frontier

- Go source anchors (Base-src.zip, `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`): `:79` declared range `1.15-1.25`; `:171` `Untested Go version`; `:359` missing bootstrap message. `ghidra/app/util/bin/format/golang/GoVer.java:46` `parse`.
- New SOURCES rows opened this round: {{SLOT: Go debug/buildinfo source/docs; Go release history — ids, tier, status}}
- Reopened: S003, S023 {{SLOT: confirm}}
- Frontier (open, not claimed): Go 1.27 symbol recovery is an expected bootstrap failure, not a target (claims.json non_claims). {{SLOT: any new frontier entries}}

## Trend verdicts

Per-axis (no scalar). Fill from measured before/after only.

| axis | verdict | evidence |
|---|---|---|
| calibration | {{SLOT: improved / unchanged / harmed}} | {{SLOT}} |
| depth | {{SLOT: improved / unchanged / harmed}} | {{SLOT}} |
| coverage | {{SLOT}} | {{SLOT}} |
| operability | {{SLOT}} | {{SLOT}} |
| freshness | {{SLOT}} | {{SLOT}} |
| adjacency | {{SLOT}} | {{SLOT}} |

Admission: {{SLOT: admitted | withheld, with the rule applied}}

## SHONEN

Promotion checklist (`SHONEN.md`). This round does not authorize any `[x]`; boxes stay `[~]` unless an independent non-author verifier establishes them.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SHONEN.md:5`. {{SLOT: round-17 delta or "unchanged"}}
- [~] At least one end-to-end domain task executed and logged in LOG.md — `SHONEN.md:7`. {{SLOT: C2 retained carrier runs logged?}}
- [~] Instructions executable by an agent without oral context — `SHONEN.md:9`. {{SLOT: delta}}
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `SHONEN.md:11`. {{SLOT: delta; PROVINCE untouched?}}

## Stale-lane

Stale-lane: {{SLOT: lane status, e.g. "this is the sole named kaidoku mission, respawn-per-round; no other mission of this lane is open"}}

## Tool installs/updates

{{SLOT: list each install as tool, version, channel, reason. Seat-level installs reported by each seat.}}

## Cross-domain evidence

- Carrier provenance: the pilot esbuild carrier is an install under a kimi-code pnpm store (path in `pilot/README.txt`); the pilot shfmt carrier is `/usr/bin/shfmt` (pacman-owned; {{SLOT: carrier-census.py owner output}}). Domain: carrier installs are outside the kaidoku lane.
- {{SLOT: any routed outside defects, e.g. `corpus/lessons/round-16-verifier-spotcheck.md:183-184`, and their disposition}}
- No sibling gate, agent database, credential/auth file, client routing or host service accessed (contract.md host safety). {{SLOT: confirm}}

## Wave stats

Observed from the dispatch artifacts (not measured outcomes):

- Spec items: 78 (`wave1-spec.json`, `items` length). Role histogram: scout 20, executor 14, reviewer 12, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2.
- Dispatch: `counts` spawn 78, resume 0, total 78 (`wave1-dispatch.json`); the DraftReport entry is at `wave1-dispatch.json:1190-1192`.
- Dispatch attempts: 1 refused 78, 2 refused 78, 3 refused 0 (`wave1-dispatch-attempts.json`; cause of refusals not recorded in the file).
- Registry: 78 members, all `kind: spawn` (`w1/swarm-registry.json`).
- Seat outcomes: {{SLOT: delivered / failed / substantive count}}
- Failed seats not counted as substantive: {{SLOT}}
