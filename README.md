# shokunin-reverse-engineering

**Shipped-artifact reverse engineering with REA on Linux — evidence
first, source-available repos never.**

Lane name: **kaidoku-shokunin**. A **shokunin lane** minted and trained
under the [shokunin](https://github.com/VeigaPunk/shokunin) skill.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/shokunin-reverse-engineering?branch=main)

## Domain

From `PROVINCE.md` and `SKILL.md`: native ELF/PE through the Ghidra
12.1.4 provider, Electron/ASAR/JavaScript bundles, APK, firmware,
managed assemblies, recorded crashes, runtime evidence. Analysis keeps
observation, inference, and unknowns separate. A catalog-listed tool is
*available*, not *held* — a surface moves to Core only after an
end-to-end probe lands a `LOG.md` entry citing its `evidence_id` and
subject sha256.

Probe convention:

- `rea doctor` — environment verdict (read `scope_checks[]`, not the top-level bool)
- `binary_session {}` — live-server verdict (`result.tool_availability` + provider candidates)

Current REA inventory recorded 2026-10-16 (drift-prone — re-verify):

| Client | Pin | MCP tools / CLI commands |
|---|---|---|
| Devin / OMP | `rea-agents@6.5.0` | 207 / 153 |
| Kimi | `rea-agents@6.4.0` | 170 / 127 |

Ghidra provider: `GHIDRA_INSTALL_DIR` → 12.1.4 PUBLIC, JDK 21. Anti-trigger:
ordinary source repositories — use normal repo tools, never run REA on
available source.

## What it refuses

Malware triage at scale; non-REA dynamic analysis (Frida-style hooking,
unpacking by execution); installing engines or editing client configs
(operator-owned); quality / safety / license verdicts on findings. The
lane answers "what does this shipped artifact do, per evidence id X" —
never "is it safe." Shared scope with
[revenger](https://github.com/VeigaPunk/shokunin-binary-forensics) is
integrator-arbitrated; this lane does not absorb it.

## In this repository

```
PROVINCE.md     Core / Frontier / Adjacent surface tables
SKILL.md        executable REA playbook
SHONEN.md  SCORECARD.md  LOG.md  MINT.md   (minted 2026-10-13)
AGENTS.md       lane operating rules
corpus/
  knowledge/    dated probe notes (evidence_id + sha256)
  lessons/
  QUALITY.md
evidence/
```

## How a lane learns

The domain is a frontier, not a fence: it grows by evidence
(`LEARNING.md` at the fleet root). Append-only corpus; rounds are
non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
