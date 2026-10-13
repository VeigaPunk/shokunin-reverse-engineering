<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/01-rea-cli.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 — REA CLI surface catalog (rea-agents@6.4.0)

Probing method: `npx -y rea-agents@6.4.0 <cmd> --help` only. No `rea`/`rea-agents`
binary exists on host PATH — the package is invoked through npx and presents
itself as `rea` in help text. No analysis verbs were executed.

## Candidate: Distribution and invocation shape
- claim: `rea-agents@6.4.0` on npm installs a CLI whose program name is `rea` (help banner: "rea@6.4.0 — Reverse engineer anything from your terminal or agent."); no `rea` or `rea-agents` executable is on this host's PATH, so invocation is `npx rea-agents@6.4.0 <cmd>`; `rea --version` prints `6.4.0`.
- source: `npx rea-agents@6.4.0 --help`; `npx rea-agents@6.4.0 --version`; `which rea` (exit 1, not found)
- verify: `which rea; npx -y rea-agents@6.4.0 --version`
- verified-at: 2026-10-13
- suggested: admit — direct observation of version string and PATH absence on this host.

## Candidate: CLI surface size — 127 top-level commands
- claim: `rea --help` lists exactly 127 top-level commands plus 2 integration groups (`completions`, `mcp`); the verb families by first token are inspect(36), list(11), trace(9), compare(8), capture(6), observe(5), read(3), project(3), analyze(3), plus smaller families (decompile 2, decode 2, evidence 2, extract 2, import 2, pull 2, resolve 2, search 2, start 2, uninstall 2) and singleton verbs.
- source: `npx rea-agents@6.4.0 --help` piped to awk counting `Commands:` block entries
- verify: `npx -y rea-agents@6.4.0 --help | awk '/^Commands:/{f=1;next}/^Integrations:/{f=0}f&&/^  [a-z]/{c++}END{print c}'`
- verified-at: 2026-10-13
- suggested: admit — deterministic count from help output; count is version-pinned to 6.4.0.

## Candidate: Universal global option set
- claim: Every command accepts the same global options: `--format <toon|json|yaml|md|jsonl>`, `--filter-output <keys>` (key-path filtering, e.g. `foo,bar.baz,a[0,3]`), `--token-count`, `--token-limit <n>`, `--token-offset <n>`, `--full-output`, `--schema` (per-command JSON Schema), `--llms/--llms-full` (LLM-readable manifest), `--help`; the root additionally exposes `--mcp` (stdio server mode), `--update`, `--version`.
- source: `npx rea-agents@6.4.0 --help` and 15 subcommand `--help` runs — the Global Options block is identical in every one
- verify: `npx -y rea-agents@6.4.0 search --help | grep -A12 'Global Options'`
- verified-at: 2026-10-13
- suggested: admit — confirmed identical across all 15 sampled subcommands; formats token-budgeted output as a first-class, cross-cutting feature.

## Candidate: Core analysis verbs share one argument shape
- claim: `analyze`, `inspect`, `decompile`, `function`, `instructions`, `xrefs`, `search`, `trace` all take `<path>` (app/program/analysis-db path) plus `--snapshot`, `--target-format`, and `--provider` options; `--provider` binds deep analysis to a provider ID "or use deterministic auto selection"; `--snapshot` "Load and update a local analysis snapshot" (state-carrying, not read-only).
- source: `npx rea-agents@6.4.0 {analyze,inspect,decompile,function,instructions,xrefs,search,trace} --help`
- verify: `npx -y rea-agents@6.4.0 function --help`
- verified-at: 2026-10-13
- suggested: admit — verbatim from help text; note the snapshot option mutates local state so even "read" verbs are not pure.

## Candidate: `rea search` defaults
- claim: `rea search <path> [pattern]` defaults to `--kind strings` (vs `procedures`) and `--mode literal` (vs `regex`), case-insensitive unless `--case-sensitive`; pattern can be passed positionally or via `--pattern=<value>` (documented for leading-dash safety).
- source: `npx rea-agents@6.4.0 search --help`
- verify: `npx -y rea-agents@6.4.0 search --help`
- verified-at: 2026-10-13
- suggested: admit — defaults printed inline in help.

## Candidate: `rea read-bytes` default length
- claim: `rea read-bytes <path> <address>` reads provider memory bytes with `--length` defaulting to 256; requires an exact provider memory address (not a symbol).
- source: `npx rea-agents@6.4.0 read-bytes --help`
- verify: `npx -y rea-agents@6.4.0 read-bytes --help`
- verified-at: 2026-10-13
- suggested: admit — default printed inline.

## Candidate: `rea analyze` integrity policy default is fail-closed
- claim: `rea analyze` supports `--integrity-policy <fail|record-and-continue>` with default `fail` — a declared-application-integrity mismatch aborts analysis unless explicitly downgraded.
- source: `npx rea-agents@6.4.0 analyze --help` ("(default: fail)")
- verify: `npx -y rea-agents@6.4.0 analyze --help | grep integrity`
- verified-at: 2026-10-13
- suggested: admit — explicit default in help; consistent with the product's "Evidence"/"authenticated" vocabulary elsewhere.

## Candidate: `rea compare` has alias `compare-bundles`
- claim: `rea compare <left> <right>` compares two canonical Evidence bundles and is also invocable as `compare-bundles`.
- source: `npx rea-agents@6.4.0 compare --help` ("Aliases: compare-bundles")
- verify: `npx -y rea-agents@6.4.0 compare-bundles --help`
- verified-at: 2026-10-13
- suggested: admit — alias printed in help; no other aliases were observed in sampled commands (unverified for remaining ~112).

## Candidate: `rea evidence-export` refuses overwrite by default
- claim: `rea evidence-export <source> <output>` validates and "atomically" exports canonical Evidence JSON; replacing an existing output file requires explicit `--overwrite`. Mirrors `push-adb-file` which "refuses existing targets without --overwrite" — a consistent no-clobber convention.
- source: `npx rea-agents@6.4.0 evidence-export --help`; `npx rea-agents@6.4.0 --help` (push-adb-file line)
- verify: `npx -y rea-agents@6.4.0 evidence-export --help`
- verified-at: 2026-10-13
- suggested: admit — verbatim flags; atomicity claim is the tool's own wording, not tested.

## Candidate: Lifecycle verbs — setup / doctor / update / uninstall
- claim: `rea setup` configures agent integrations (`--client`, `--all-detected`, `--skill-client`, `--skill`) and providers, supports `--dry-run` (prints resolved plan), `-y/--yes`, `--install-hopper`, `--accessible`; `rea doctor` checks readiness with optional `--target`, `--client`, `--provider` requirements and `--skill` identity alignment; `rea update` self-updates and verifies the release; `rea uninstall` removes REA-owned agent config/skill files, `--purge-data` also removes caches/state.
- source: `npx rea-agents@6.4.0 {setup,doctor,update,uninstall} --help`
- verify: `npx -y rea-agents@6.4.0 setup --help`
- verified-at: 2026-10-13
- suggested: admit — verbatim; `--dry-run` makes setup safely introspectable in round 2.

## Candidate: MCP and shell integration
- claim: `rea` embeds an MCP stdio server (`--mcp` global flag), an `mcp` command group with `add` (register) and `doctor` (validate startup/tool listing) subcommands, and a `completions` generator for shell completion scripts.
- source: `npx rea-agents@6.4.0 --help` (Global Options + Integrations); `npx rea-agents@6.4.0 mcp --help`
- verify: `npx -y rea-agents@6.4.0 mcp --help`
- verified-at: 2026-10-13
- suggested: admit — implies every CLI verb is also exposed as an MCP tool surface; worth a dedicated probe lane later (`--mcp` + tools/list was NOT run here).

## Candidate: Provider abstraction is the analysis backend
- claim: Deep analysis is delegated to named "providers" bound via `--provider <value>` or auto-selected deterministically; `rea providers` lists configured providers and `rea capabilities` lists "provider capabilities and side effects" — side effects are a declared, inspectable property of the tool's own registry.
- source: `--provider` option text on all analysis verbs; `npx rea-agents@6.4.0 capabilities --help`; `npx rea-agents@6.4.0 providers --help`
- verify: `npx -y rea-agents@6.4.0 capabilities --format json | head -50`
- verified-at: 2026-10-13
- suggested: admit — help-verbatim; actual provider list on this host not yet captured (next round: run `providers`/`capabilities` — read-only).

## Candidate: Broad artifact-domain coverage without execution
- claim: The command surface spans native binaries (inspect-binary-layout, inspect-macho, inspect-pe-resources, list-architectures, observe-native-calls via LLDB), managed .NET PE/CLI (inspect-managed-*, compare-managed-members, verify-managed-native-boundaries), Android via adb+apktool (26 adb/apktool/jeb verbs), Apple (plist, keyed-archive, asset-catalog, decode-interface-builder, demangle-swift, trace-dylib-resolution), web/Electron/Node (capture-browser-scenario via Playwright, inspect-web-*, CDP target listing), firmware and EVM bytecode — and most inspect verbs explicitly state they do not execute/load the target.
- source: `npx rea-agents@6.4.0 --help` command descriptions
- verify: `npx -y rea-agents@6.4.0 --help | grep -c 'without'`
- verified-at: 2026-10-13
- suggested: admit — counts derived from the same help text already captured; the no-execution claims are the vendor's own descriptions, not observed behavior.

## Candidate: Evidence is the inter-command data model
- claim: A canonical "Evidence JSON" bundle is the lingua franca: produced/consumed by evidence-export/evidence-import, inspect-evidence-bundle, compare, compare-process-captures, compare-web-captures, project-*-application-graph, trace-application-feature, import-reference-source, build-reconstruction-obligation-ledger — meaning cross-domain comparison and graph projection operate on normalized evidence rather than raw artifacts.
- source: `npx rea-agents@6.4.0 --help` descriptions of the listed verbs
- verify: `npx -y rea-agents@6.4.0 inspect-evidence-bundle --help`
- verified-at: 2026-10-13
- suggested: admit — structural observation across help text; round-2 lanes should dump one real Evidence bundle to confirm the schema.

## Lesson candidate: Help-only probing is high-yield on this CLI
- The uniform per-command Global Options block (`--schema`, `--llms`, `--token-count`, `--format`) means the tool is self-describing: `rea <cmd> --schema` likely returns full argument JSON Schemas without executing analysis — cheaper and more precise than parsing help prose. Recommend next-round catalog lanes use `--schema` as primary source and `--help` as cross-check.

## Lesson candidate: npx cold-start tax
- Each `npx -y rea-agents@6.4.0` invocation re-resolves the package (sub-second to a few seconds once cached). For a 127-command surface, batch help-collection via one `npm exec` shell or a single `npx --package rea-agents@6.4.0 rea ...` loop amortizes this; avoid one-npx-per-command in bulk lanes.

## Summary
CLI surface cataloged from 16 read-only help probes: 127 commands across 14 verb families, uniform global options (formats, token budget, schema), shared path/snapshot/provider argument shape, fail-closed integrity default, Evidence-JSON data model, MCP/completions integrations, and setup/doctor/update/uninstall lifecycle verbs — all pinned to rea-agents@6.4.0, no `rea` binary on host PATH.
