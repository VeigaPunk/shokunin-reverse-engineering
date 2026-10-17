# shokunin-reverse-engineering

Shipped-artifact reverse engineering with REA, on this Linux host.

This is the kaidoku lane. A tool listed in the catalog is *available*.
It is *held* only after an end-to-end probe lands a `LOG.md` entry that
cites an `evidence_id` and the subject sha256. Observation, inference,
and unknown stay in separate sentences. The evidence id alone does not
authenticate module attribution carried in `subject`.

Rank: **shonen**. `SHONEN.md` is still here. Registered in the fleet
`MANIFEST.json` as kaidoku-shokunin since 2026-10-13.

## Province

**Owns.** Native ELF through the Ghidra provider, native PE, Electron /
ASAR / JavaScript bundles, archives and packages, the REA MCP and CLI
surfaces as configured per client, and the evidence discipline around
them. The Core table in `PROVINCE.md` is the list, with the probe that
showed each row live. The Frontier section is claimed in `MINT.md` and
not yet held. Rows move Core-ward by a log entry, not by the table
wishing it.

**Hands off.** Ordinary source repositories — use normal repo tools. The
skill's own anti-trigger says never to run REA on available source.
Sibling lanes own their product domains. The province tells this lane
not to re-base a sibling's frozen receipt command or historical artifact
path when REA's version drifts.

Drift-prone values (client pin, tool counts, Ghidra build, JDK) are
dated in `PROVINCE.md`. The 2026-10-16 reverification recorded there is
the latest date that file claims. Re-run `rea doctor` before you treat a
version string as today's.

## Start here

1. `PROVINCE.md` — Core, Frontier, and the per-client version pins.
2. `SKILL.md` — when to decompile, when not to, and the queue-drain rules.
   The scorecard treats citation resolvability of those rules as a depth
   proxy, and says that proxy is not semantic correctness.
3. `corpus/README.md` — the knowledge index. Coverage on the scorecard
   is index integrity, not "fraction of REA held."
4. `corpus/knowledge/` — one note per held probe, with its evidence id.
5. `corpus/QUALITY.md` — the admission bar.
6. `SCORECARD.md` — read "Current assessment" before any 0–10 cell. The
   card says the numbers are heterogeneous bounded proxies, and that a
   calibration of 10 is failure-selected completeness of nine
   preselected obligations, not unbiased mastery.

## Environment verdict

The province names `rea doctor` as the environment verdict and
`binary_session {}` as the live-server verdict inside an attached
client. There is no `rea` on `PATH` in the province's census; the CLI is
`npx -y rea-agents@<pin>` with the pin taken from that client's config,
not from memory. Provider-key inventory in the province is marked
historical where it was not re-probed.

`EXAMPLE.kama.md` is an example of a neighboring lane's shape. It is not
this lane's domain.

## The tree

| Path | What it is |
|---|---|
| `SKILL.md` | The playbook |
| `PROVINCE.md` | The surface map |
| `corpus/knowledge/` | Held probes and reconciliations |
| `corpus/lessons/` | Per-round lessons |
| `corpus/QUALITY.md` | Admission bar |
| `evidence/` | Frozen rubrics and receipts, including the round-1 calibration set |
| `MINT.md` | The mint demand |
| `.ufo/` | Wave receipts for later rounds |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
The evidence-ledger sibling is
[shokunin-binary-forensics](https://github.com/VeigaPunk/shokunin-binary-forensics)
(revenger). Shared shipped-artifact scope is reported, not absorbed.
Tsukuroi's handoff table leaves the choice of owner to the integrator.
