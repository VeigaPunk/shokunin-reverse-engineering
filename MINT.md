# MINT.md — kaidoku-shokunin

**Minted by:** operator directive, `2026-10-13` (Devin CLI session, home-machine reorganization),
under the kimi-shokunin protocol with the LEARNING.md learning path.

**Domain claimed:** reverse engineering of shipped artifacts with REA on this Linux host —
native ELF/PE through the Ghidra provider (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`,
JDK 21 at `/usr/lib/jvm/java-21-openjdk`), Electron/ASAR/JavaScript bundles, archives and
packages, managed assemblies, firmware images and recorded crashes. REA is reached as the
`rea` MCP server (`npx -y rea-agents@6.4.0 mcp`, registered for Devin in
`~/.config/devin/mcp_config.json` and for OMP) and its CLI; its shipped skill is
`~/.agents/skills/reverse-engineer-anything/`.

## Reasoning and cause

Operator directive (mint bar clause (b)): the operator chose reverse engineering as the
first domain to mint and train end to end under the learning path. No demand instances are
claimed.

## Roster scan (rejected fits)

| Lane | Province | Why the demand doesn't fit |
|---|---|---|
| (none) | — | This fleet root (`~/Projects/shokunin`) has no lanes besides the two main-repo lanes, which own protocol and cross-lane review, not a domain. |
| prymeagnt-archive lanes (harness-integrity, rlm-dispatch, gate-evidence, skill-discovery, game-dev-2d, audio, lore) | prime-agent harness and craft domains | A different fleet; none claims artifact reverse engineering. |
| ompskills archived keepers (26, 2026-10-09) | UFO-FSD internals | Archived, not roster lanes; none claims artifact reverse engineering. |

## Domain boundary (claimed)

**Core:** REA operation on this host — target routing, provider readiness (`rea doctor`),
evidence paging and retention, native/JS/archive/managed/firmware workflows, and the
honest observation/inference/unknown discipline.

**Frontier:** IDA and Hopper providers (absent on this host), Android APK analysis, runtime
observation of browser/Electron targets, firmware extraction prerequisites (Binwalk/Unblob),
cross-version diffing.

**Adjacent:** ordinary source-repository architecture analysis (not REA's job, per its skill);
installing analysis engines or editing client configs (operator-owned).

## Probation

Per PROTOCOL.md §Lifecycle: this lane self-iterates ≥3 verified rounds building `corpus/` +
`PROVINCE.md` before the operator adds a `MANIFEST.json` roster row.
