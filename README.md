# shokunin-reverse-engineering — kaidoku-shokunin

**Shipped-artifact reverse engineering with REA on this Linux host.**
Native ELF / PE through Ghidra, Electron / ASAR / JS bundles, APK,
archives, firmware, managed assemblies, recorded crashes. Evidence-
first static analysis that keeps observation, inference, and unknowns
separate.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane. Rank:
shonen. Canonical lane name: `kaidoku-shokunin`. Trigger on a shipped
binary, a decompile, a version-compare, a core dump. Anti-trigger:
ordinary source repositories — use normal repo tools, never run REA on
available source.

Revenger
([shokunin-binary-forensics](https://github.com/VeigaPunk/shokunin-binary-forensics))
also declares shipped-artifact RE. Shared scope is integrator-owned.
Tsukuroi's ADJ-06 names that debt and does not pick an owner.

## Province

**Owns:** the `rea` MCP / CLI surfaces as they resolve per client; the
Ghidra 12.1.4 provider; native ELF and PE analysis; Electron / ASAR /
JavaScript; archive / package inventory; APK surfaces; `.node` native
addons; MCP retained-evidence sessions; recorded-crash inspection
within the documented cap; the REA surface map in `corpus/knowledge/`.

**Does not own:** ordinary source trees; live-target execution beyond a
declared target and lifecycle; DRM circumvention; publishing reversed
material. A catalog-listed tool is *available*, not *held* — ground
moves to Core only after an end-to-end probe lands a `LOG.md` entry
citing its `evidence_id` and subject sha256.

Client pins, reverified 2026-10-16 (`PROVINCE.md`): Devin and OMP use
`rea-agents@6.5.0`; Kimi uses `rea-agents@6.4.0`. Ghidra is
`12.1.4` at `GHIDRA_INSTALL_DIR` with JDK 21. Those numbers drift —
re-run `rea doctor` before treating a pin as live. The map never
re-bases a sibling lane's frozen receipt command.

Full surface table: [`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — domain, triggers, anti-triggers.
2. [`PROVINCE.md`](PROVINCE.md) — Core surfaces, frontier, probe conventions.
3. [`LOG.md`](LOG.md) — the only path a frontier item takes to Core.
4. [`SHONEN.md`](SHONEN.md) — promotion checklist.

`rea doctor` is the environment verdict. `binary_session {}` is the
live-server verdict. Host fallback readers (`file`, `readelf`,
`objdump`, `nm`, `strings`, …) are named in `PROVINCE.md`; several
common unpackers are recorded absent.

## Discipline

Every Core probe emits an `evidence_id` plus `limitations[]` /
`unknowns[]`. `detail:"summary"` plus `parent_evidence_id` paging is
the retained-evidence path. A snapshot is evidence persistence, not a
Ghidra DB cache. When module identity matters for `analyze_function`,
pin request bytes (or re-derive the dossier) — the evidence ID alone
does not authenticate module attribution carried in `subject`.

## What's in the repo

```
shokunin-reverse-engineering/
├── SKILL.md          executable REA craft
├── PROVINCE.md       Core / frontier surface table
├── SHONEN.md         promotion checklist
├── MINT.md           why this lane was minted
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── evidence/         retained probe artifacts
└── corpus/           knowledge/, lessons/, QUALITY.md
```

Protocol: append-only corpus; every claim separates observation /
inference / unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
