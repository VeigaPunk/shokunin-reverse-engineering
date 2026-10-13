# kaidoku-shokunin — Quality bar

What good looks like in reverse engineering of shipped artifacts with REA on this Linux host — native ELF/PE through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript bundles, archives and packages, managed assemblies, firmware images and recorded crashes; evidence-first static analysis that keeps observation, inference and unknowns separate (LEARNING.md). Thin at mint and grown only from lessons:
every criterion cites the lesson that produced it. A criterion is replaced by a new row
naming the row it supersedes, never rewritten.

## Admission criteria

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 1 | Cites a resolvable source: repo path, command output, or external document | CORPUS.md evidence standard | — |
| 2 | Falsifiable, or explicitly marked opinion | CORPUS.md | — |
| 3 | Domain-specific — no generic agent advice | PROTOCOL.md invariants | — |
| 4 | Names the artifact under analysis by absolute path plus a stable identity (SHA-256, or package name + version + arch when hashing is impractical); "the app" alone is inadmissible | REA binds targets by SHA-256 and refuses to pick an example target (r1 lesson: floating-target reject class; wave 15 draft) | — |
| 5 | Every conclusion is labeled observation, inference, or unknown; decompiler/pseudocode and layout-derived claims are inference, never "observed behavior" | REA SKILL.md observation/inference/unknown discipline; r1 canonical reject (entry point ≠ `main`) | — |
| 6 | A claim drawn from REA cites its Evidence ID / retained parent_evidence_id, or the exact reproducing call (tool name, target SHA-256, detail level, filters) | REA evidence-paging model (`inspect_analysis_view`, `export_evidence_bundle`); generalizes CORPUS.md "a count carries its command" | — |
| 7 | The entry names what was NOT examined: detail level (summary vs complete), truncated/paged views, unvisited modules, providers absent on this host | REA SKILL.md "preserve limitations and incomplete coverage"; r1 wave-16 frontier records | — |
| 8 | Capability claims pin tool/provider versions (rea-agents@6.4.0, Ghidra 12.1.4, JDK 21) and the claim source (live tool list vs installed skill text) | skill v37 vs release skew; `binary_session result.tool_availability` is the live verdict (r1 doctor taxonomy) | — |
| 9 | Runtime-behavior claims are admitted only with runtime-evidence provenance (recorded crash, capture, observed target); never from a static graph | REA SKILL.md "never imply that static analysis observed execution"; r1 `jq-1.8.2` runtime-vs-static evidence-class split | — |
| 10 | "Held/works" is admitted only for verbs run on a real or synthesized carrier this round; `capabilities[].available:true` is *declared* capability — the gate is provider-level `availability.status` | r3 keyed-archive lane: all three carrierless ops proved working only when given carriers; r3 audit-B: `available:true` inside unavailable providers (hopper 36/36) | sharpens 8 |
| 11 | Empty/zero findings must state whether the surface was parsed-and-empty or excluded-from-inventory (`parse_failures:0` on an unparsed member is an exclusion, not a result) | r3 typora lane: `.jsc` = 99.4% of archive bytes got zero graph nodes — "all-zero IPC summary" meant nothing | — |

## Signals of weak material

| # | signal | why (lesson) |
|---|---|---|
| 1 | Pseudocode, string tables, filenames, or section layout narrated as what the program "does" — behavior asserted with no Evidence ID | SKILL.md: never infer behavior from filenames/strings/layout alone; r1 reject class |
| 2 | "no X in the binary", "all functions enumerated", "fully analyzed" without the search command, filters, or detail level; a truncated preview treated as the complete record | SKILL.md truncated-preview rule; CORPUS.md negative-claim rule |
| 3 | Findings attached to "the app"/"the binary" with no path+hash, or citing a saved report/test fixture as the analyzed artifact | REA target-selection rules; r1 `~/.local/bin/jq` shadow finding shows why identity matters |
| 4 | "REA supports/refuses X" asserted from docs or memory without consulting `binary_session result.tool_availability` or `rea doctor` on this host | r1: catalog-listed ≠ held — `inspect-binary-layout` and `inspect_managed_artifact` both fail typed on this host |
| 5 | Dynamic claims ("when the user logs in the app sends…") sourced from static call graphs, or a recorded capture presented as live observation | SKILL.md static-vs-execution boundary; captures forbid live attribution |
