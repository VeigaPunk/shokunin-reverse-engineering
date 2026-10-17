# shokunin-reverse-engineering

Reverse engineering of shipped artifacts with REA, on this Linux host.

Lane id: **kaidoku-shokunin**. Rank: **shonen**. [`SHONEN.md`](SHONEN.md)
marks its boxes `[~]`: the lane's own pointers, no identified outside
verifier.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin). Saved-ledger
replay of a narrower fixture set lives in
[shokunin-binary-forensics](https://github.com/VeigaPunk/shokunin-binary-forensics)
(revenger). This lane holds the REA surface: providers, sessions, and
evidence-first static analysis.

## The question

> What does this shipped artifact contain, which provider actually held
> the analysis, and which conclusion is observation rather than inference?

Trigger on a shipped binary, a decompile, an `.asar` / `.exe` / ELF, a
version compare, or a core dump. Ordinary source repositories use
ordinary repo tools. REA is not pointed at available source.

## What is held

`PROVINCE.md` is the surface table, with the dates each row was verified.
Read it before quoting a version. The drift-prone values, re-verified in
that file on 2026-10-16:

| Client | REA pin |
|---|---|
| Devin, OMP | `rea-agents@6.5.0` |
| Kimi | `rea-agents@6.4.0` |

Ghidra `12.1.4` is the provider named there, on JDK 21. A catalog-listed
tool is *available*. It is *held* only after an end-to-end probe lands a
`LOG.md` entry citing its `evidence_id` and the subject sha256.

Probe convention from the skill: `rea doctor` is the environment verdict
(read `scope_checks[]`, not only the top-level bool). `binary_session {}`
is the live-server verdict. Work summary-first: `detail:"summary"`, then
`parent_evidence_id`, then `inspect_analysis_view`. Pin path plus sha256
before analysis. Sessions under `/tmp/rea-ghidra-*` are ephemeral and
shared across lanes; do not clean another session's directory.

## Boundary

Static analysis of shipped artifacts, with observation / inference /
unknown kept apart. Static output is never "observed execution."
`EXAMPLE.kama.md` is an example of the cross-lane report shape, not a
kama-owned file. Endpoint health stays with kama. Credential material
stays with kagi. Game mechanics stay with the game lanes. Narrative canon
stays with lore.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | routing decision table and the working contract |
| [`PROVINCE.md`](PROVINCE.md) | core surfaces, frontier, and verification dates |
| [`corpus/knowledge/`](corpus/knowledge/) | per-probe notes |
| [`corpus/QUALITY.md`](corpus/QUALITY.md) | admission bar, including what "held" means |
| [`evidence/`](evidence/) | retained bundles, including the round-1 libjq smoke |
| [`MINT.md`](MINT.md) | claimed frontier at mint |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md), [`SHONEN.md`](SHONEN.md) | audit trail, verdicts, probation |

When module identity matters, pin the request bytes. An evidence ID alone
does not authenticate the module attribution carried in `subject`.
The province cites the note that measured that limit.
