# shokunin-reverse-engineering

Reverse engineering of shipped artifacts with REA on this Linux host.
Native ELF and PE through the Ghidra provider, Electron and ASAR and
JavaScript bundles, archives and packages, managed assemblies, firmware
images, and recorded crashes. Observation, inference, and unknown stay
in separate sentences.

The lane id is `kaidoku`. Rank is shonen. Ordinary source repositories
are an anti-trigger: use the repo's own tools, and do not run REA on
source you already have.

## The job

`PROVINCE.md` is the pin table. It records which client resolves which
REA package (Devin and OMP on `rea-agents@6.5.0`, Kimi on
`rea-agents@6.4.0`, with catalog counts and `tools_sha256` values),
where Ghidra 12.1.4 is installed, and which provider keys were
historical rather than re-probed. Those values drift. The province
says when they were last reverified (2026-10-16 for the client pins and
the Ghidra/JDK pair). Re-read it, then re-run `rea doctor`, before
quoting a count from this page.

Probe conventions, from the province: `rea doctor` is the environment
verdict; `binary_session {}` is the live-server verdict; a tool that is
listed in the catalog is available, not held. A ground move to Core
waits for an end-to-end probe that lands a `LOG.md` entry citing an
`evidence_id` and the subject sha256.

`SKILL.md` is the operating manual: when to open a shipped binary, and
when to walk away. `EXAMPLE.kama.md` is an example record, not a second
skill.

The lane refuses treating a catalog listing as a completed analysis.
Sibling revenger ([shokunin-binary-forensics](https://github.com/VeigaPunk/shokunin-binary-forensics))
owns the saved evidence-ledger replay of shipped artifacts. This lane
owns REA on the host.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — client pins, Ghidra, probe conventions. Check the reverified date.
2. [`SKILL.md`](SKILL.md) — triggers, anti-triggers, and the domain paragraph.
3. [`corpus/README.md`](corpus/README.md) — the knowledge index.
4. [`LOG.md`](LOG.md) — which probes have an evidence id, and which are still catalog-only.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Operating manual. |
| `PROVINCE.md` | Host pins and the drift record. |
| `corpus/` | Knowledge entries, one file per probed claim. |
| `evidence/` | Captured evidence beside the corpus. |
| `EXAMPLE.kama.md` | An example record of the ledger shape. |
| `MINT.md`, `SHONEN.md` | Mint record and promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
Roster id `kaidoku`, rank **shonen**.
