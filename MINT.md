# MINT.md — kaidoku-shokunin

**Minted by:** <integrator session / operator directive, `YYYY-MM-DD`>, on <evidence basis —
e.g. aggregator evidence: N independent demand instances of the same unplaceable defect
class>.

**Domain claimed:** reverse engineering of shipped artifacts with REA on this Linux host — native ELF/PE through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript bundles, archives and packages, managed assemblies, firmware images and recorded crashes; evidence-first static analysis that keeps observation, inference and unknowns separate — <surfaces, drift-sensitive values, probe and reconciliation
concerns; cite real paths / process names / config keys in backticks as they are verified>.

## Reasoning and cause

<NUMBER> *independent* lanes discovered the same unplaceable defect class, on different
surfaces, in different rounds:

1. **<lane id> round <N>** (`.ufo/reports/round-<N>/kaidoku.md`): <demand instance — what
   was observed, with cited paths, values, and command outputs>.
2. **<lane id> round <N>** (`.ufo/reports/round-<N>/kaidoku.md` + <corroborating pointer,
   e.g. an aggregator routing-table row>): <second demand instance — same defect class,
   different surface>.

<Optional: any additional drift / absence evidence supporting the same defect class — e.g.
a path or endpoint a sibling's config cited that no longer resolves.>

## Roster scan (rejected fits)

`MANIFEST.json` roster at mint time, and why none absorb this:

| Lane | Province | Why the demand doesn't fit |
|---|---|---|
| <lane id> | <lane province> | <why this lane cannot absorb the demand> |
| <lane id> | <lane province> | <why this lane cannot absorb the demand> |

<Aggregator rulings: which rounds found the lane mint-eligible, that the surface has no
owning province, and any standing mint-table row — each dated.>

## Domain boundary (claimed)

**Owns:** <the surfaces this lane owns — processes, their ports/paths, config values
referenced by consumers, identity-vs-reality reconciliation, probe conventions, drift
detection, the cross-lane registry of which consumer config points at which surface>.

**Refuses:** <quality/eval concern> (<sibling lane id>), <credential material / auth flows>
(<sibling lane id>), <dispatch / route mechanism> (<sibling lane id>), <remote surfaces>
(<sibling lane id>). Boundary rule: kaidoku answers "<the identity/liveness question this
lane answers>" — never "<the quality question>" or "<the request-safety question>".

## Probation

Per PROTOCOL.md §Lifecycle "Sibling mint": this lane self-iterates ≥3 verified rounds
building `corpus/` + `PROVINCE.md` before the operator adds a `MANIFEST.json` roster row.
