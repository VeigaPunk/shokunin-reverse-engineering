# shokunin-reverse-engineering — kaidoku-shokunin

**Shipped-artifact reverse engineering with REA on Linux.**

Native ELF through the Ghidra provider, Electron / ASAR / JavaScript
bundles, archives and packages, PE, APK, firmware regions, managed
IL — evidence-first static analysis that keeps observation, inference,
and unknowns separate. Every Core probe is supposed to emit an
`evidence_id`.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Canonical name: `kaidoku-shokunin`. Rank: **shonen**.

## The craft

The lane answers *"what does this shipped artifact do, per evidence
id X"* — never *"is it safe, trustworthy, or licensed for reuse"*.

- `rea doctor` is the environment verdict.
- `binary_session {}` is the live-server verdict.
- A catalog-listed tool is *available*, not *held*. Ground moves to
  Core only after an end-to-end probe lands a `LOG.md` entry citing
  its `evidence_id` and subject sha256.
- Host fallback readers (`file`, `readelf`, `objdump`, …) are
  documented in [`PROVINCE.md`](PROVINCE.md). Installing engines,
  editing client configs, or running `rea setup` is **operator-owned**.

Surface summary (reverified 2026-10-16, `PROVINCE.md`): Devin and OMP
pin `rea-agents@6.5.0`; Kimi pins `rea-agents@6.4.0`; Ghidra
12.1.4 + JDK 21 on the recorded host. Those pins drift — re-run
`rea doctor` before treating them as current.

## Province

Owns: REA-on-Linux analysis of caller-supplied, declared artifacts,
plus the REA surface map (per-client registration, provider
availability, on-host inventory) in `corpus/knowledge/`.

**Refuses:** live-target execution beyond the declared target and
lifecycle; DRM circumvention or piracy facilitation; publishing
reversed code; malware triage at scale; non-REA dynamic analysis
(Frida-style hooking, unpacking by execution); source-available
reconstruction of ordinary repositories; quality/safety verdicts;
installing engines.

Writes only this repository. Sibling repos and domain source
checkouts stay read-only.

See [`PROVINCE.md`](PROVINCE.md) and [`SKILL.md`](SKILL.md).

## What's in this repository

```
shokunin-reverse-engineering/
├── SKILL.md              decision tables, error patterns, checklists
├── PROVINCE.md           Core / Frontier / Adjacent (append-only)
├── SHONEN.md             boxes author-asserted until a named non-author
├── LOG.md
├── SCORECARD.md
├── MINT.md
├── AGENTS.md
├── EXAMPLE.kama.md
├── evidence/             including round-1 REA bundle
└── corpus/
    ├── knowledge/        dated probe notes
    └── lessons/
```

## Start here

1. [`PROVINCE.md`](PROVINCE.md) — what is Core vs Frontier vs Adjacent.
2. [`SKILL.md`](SKILL.md) — how to open a session and cite evidence.
3. `evidence/round-1-2026-10-15/` — a recorded native smoke
   (libjq open → decode → export → close), not a promotion.

This README does not include exploit procedures, payloads, or
unauthorized-access steps. Analysis is of declared artifacts, inside
the recorded lifecycle.

## How a round works

One axis-move. Lane identity:
`kaidoku-shokunin <kaidoku@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[revenger / shokunin-binary-forensics](https://github.com/VeigaPunk/shokunin-binary-forensics)
(evidence-ledger sibling; integrator arbitrates shared RE scope) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
