# kaidoku-shokunin — 解読

Repo: `shokunin-reverse-engineering`.

**Reverse engineering of shipped artifacts with REA on Linux.** Native
ELF/PE through Ghidra, Electron/ASAR/JS bundles, APK, firmware, managed
assemblies, archives, recorded crashes — evidence-first static analysis
that keeps observation, inference, and unknowns separate.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *what does this shipped artifact actually do, under
which provider, with an evidence ID a stranger can page — and what is
still unknown?*

Ordinary source repositories are **out of scope**. Use normal repo
tools. Never run REA on available source.

## Domain

From [`PROVINCE.md`](PROVINCE.md): the `rea` MCP/CLI surface (per-client
pins), Ghidra 12.1.4, JDK 21, and the host fallback readers (`readelf`,
`objdump`, `file`, …). A catalog-listed tool is *available*, not *held*
— a surface moves to Core only after an end-to-end probe lands a
`LOG.md` entry citing its `evidence_id` and subject sha256.

Current configured pins (reverified 2026-10-16 in `PROVINCE.md`):
Devin/OMP `rea-agents@6.5.0`; Kimi `rea-agents@6.4.0`. Probe convention:
`rea doctor` is the environment verdict; `binary_session {}` is the live
server verdict.

**Refuses:** live-target execution beyond the declared target and
lifecycle; DRM circumvention; publishing reversed material. Evidence-
ledger *verification of saved records* as a product is
[revenger](https://github.com/VeigaPunk/shokunin-binary-forensics).
Browser *journeys* are [tabi](https://github.com/VeigaPunk/tabi-shokunin).

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | routing table, working contract, held vs frontier surfaces |
| [`PROVINCE.md`](PROVINCE.md) | per-surface pins, probe conventions, refusals |
| [`corpus/knowledge/`](corpus/knowledge/) | sourced REA/Ghidra notes, doctor taxonomy, catalogs |
| [`evidence/`](evidence/) | retained probe artifacts |
| [`EXAMPLE.kama.md`](EXAMPLE.kama.md) | worked example shape |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) · [`MINT.md`](MINT.md) | axes, trail, promotion, mint |

## How to begin

1. Read [`PROVINCE.md`](PROVINCE.md) surface summary — pins drift.
2. Read [`SKILL.md`](SKILL.md) working contract — route the target first.
3. Confirm the environment with `rea doctor` in an attached client
   (read `scope_checks[]`, not the top-level bool).
4. Every Core probe must emit `evidence_id` + `limitations[]` /
   `unknowns[]`. Snapshot is evidence persistence, not a Ghidra DB cache.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
