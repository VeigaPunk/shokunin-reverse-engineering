<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/02-rea-llms.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 / 02 — REA self-documentation extraction (`rea-agents@6.4.0`)

`--llms` exists as a global flag (paired with `--llms-full`). REA's self-doc surface is three layered artifacts plus shipped package docs:

| Surface | Command / location | Shape |
|---|---|---|
| Compact index | `rea --llms` | 135 lines: `# rea` title + tagline + one markdown table of all **127** commands (`signature | one-line description`) + footer: "Run `rea --llms-full` for full manifest. Run `rea <command> --schema` for argument details." |
| Full manifest | `rea --llms-full` | 1806 lines: 127 sections `# rea <cmd>`, each = prose one-liner + `## Arguments` table (Name/Type/Required/Description) + optional `## Options` table (Flag/Type/Default/Description). Does **not** repeat the index table — it is the detail complement to `--llms`, not a superset dump. |
| Per-command schema | `rea <cmd> --schema` | Structured dump: `args`/`options` objects with types, `required[]`, `enum[]`, `const`, `pattern`, `default`, `additionalProperties: false`. |
| Human help | `rea --help` / `rea <cmd> --help` | Command list + `Integrations` (`completions`, `mcp` with `add`/`doctor`) + `Global Options`. |
| Bundled skill | `<pkg>/skills/reverse-engineer-anything/SKILL.md` + `references/*.md` (6 files, all shipped) | Operational doctrine for agents; metadata `version: "37"`, `tool_count: 170` (MCP tools > 127 CLI verbs). |
| README | `<pkg>/README.md` (343 lines) | Support matrix + provider model + doc index (links are GitHub-repo-relative; `docs/` and `website/` are **not** shipped in the npm tarball). |
| Live self-report | `rea doctor`, `rea capabilities`, `rea providers` | Host-scoped readiness and per-operation availability/effects matrices. |

Command-family histogram of the index (first verb token): `inspect-*` 36, `list-*` 11, `trace-*` 9, `compare-*` 8, `capture-*` 6, `observe-*` 5, `project-*`/`analyze*`/`read-*` 3 each; 15 `adb` verbs spread across list/inspect/pull/push/read/start/stop/install/uninstall/resolve/collect prefixes; plus Evidence verbs (`evidence-export`, `evidence-import`, `inspect-evidence-bundle`, `inspect-analysis-view`) and lifecycle (`setup`, `doctor`, `update`, `uninstall`).

Package resolved on this host: `~/.npm/_npx/af752b90495482d7/node_modules/rea-agents/` (npx cache).

## Candidate: `rea --llms` emits a 127-command index table; `--llms-full` emits only the per-command detail sections

- claim: `--llms` prints title + a single table of exactly 127 `rea` commands with positional-arg signatures and one-line descriptions, ending in a footer pointing to `--llms-full` and `<command> --schema`; `--llms-full` prints 127 `# rea <cmd>` sections (1806 lines total) with `## Arguments`/`## Options` markdown tables and does NOT re-emit the index.
- source: `npx rea-agents@6.4.0 --llms` (135 lines); `npx rea-agents@6.4.0 --llms-full` (1806 lines); `grep -c '^| \`rea '` = 127 rows, `grep -c '^# rea '` = 127 detail sections.
- verify: `npx rea-agents@6.4.0 --llms | wc -l` (expect 135); `npx rea-agents@6.4.0 --llms-full | grep -c '^# rea '` (expect 127); `npx rea-agents@6.4.0 --llms-full | head -3` (expect `# rea address-to-file-offset` first — no index preamble).
- verified-at: 2026-10-13
- suggested: admit — falsifiable, directly re-checkable, and the entry point for any agent wanting the verb inventory.

## Candidate: `rea <cmd> --schema` is the machine-readable contract; a shared native-analysis option block recurs

- claim: `--schema` prints a typed per-command contract (args/options properties, `required`, `enum`, `const`, `pattern`, defaults, `additionalProperties: false`). Native-target commands share a recurring option block: `--provider` (`const auto` or `pattern ^[a-z][a-z0-9\x2d]*$` — deterministic auto-selection default), `--snapshot` (load/update local analysis snapshot), `--target-format` (`const dos-com`), and `--integrityPolicy` (`enum fail|record-and-continue`, default `fail`) on app/artifact commands.
- source: `npx rea-agents@6.4.0 analyze --schema` output; `--llms-full` options tables for analyze/inspect/decompile/function/search/xrefs (lines 19,548,344,508,1506,1788 of the `--llms-full` stream).
- verify: `npx rea-agents@6.4.0 analyze --schema` and `npx rea-agents@6.4.0 decompile --schema`; `npx rea-agents@6.4.0 --llms-full | grep -n 'provider\|snapshot\|target-format\|integrityPolicy'`.
- verified-at: 2026-10-13
- suggested: admit — this is the load-bearing section for constructing valid calls; the provider/snapshot block explains how deep-analysis binding works without reading source.

## Candidate: Global output-control flags make the CLI agent-consumable (format/filter/token pagination); MCP is a first-class integration

- claim: Every command accepts `--format toon|json|yaml|md|jsonl`, `--filter-output <keypaths>`, `--token-count` (prints count instead of output), `--token-limit <n>` / `--token-offset <n>` (token-level pagination), `--full-output` (envelope), `--mcp` (stdio server mode). Separately `rea mcp add` / `rea mcp doctor` register/validate the MCP server, and `rea completions` generates shell completions.
- source: `npx rea-agents@6.4.0 --help` Global Options + Integrations sections; `npx rea-agents@6.4.0 mcp --help` (subcommands `add`, `doctor`); live `npx rea-agents@6.4.0 doctor --token-count` printed `19090`.
- verify: `npx rea-agents@6.4.0 --help | sed -n '/Global Options/,$p'`; `npx rea-agents@6.4.0 doctor --token-count` (numeric output); `npx rea-agents@6.4.0 mcp --help`.
- verified-at: 2026-10-13
- suggested: admit — token pagination + structured formats are the mechanism by which large Evidence output stays inside an agent's context; central to how the docs say to consume results.

## Candidate: Bundled SKILL.md is the operational doctrine — target→first-tool routing table and summary-first Evidence paging

- claim: The shipped `skills/reverse-engineer-anything/SKILL.md` (frontmatter `version: "37"`, `tool_count: 170`) is the real behavioral doc: (a) a when-to-use gate (shipped artifacts/binary evidence only; skip REA for source-repo work); (b) a "Route the target first" table mapping ~14 target types to entry tools (ASAR→`analyze_javascript_application`, archive→`open_binary`/`inspect_artifact`, APK→`inspect_android_package`, PE/CLI→`inspect_managed_artifact`, firmware→`inspect_firmware_regions`, ELF layout→`inspect_binary_layout`, core dump→`inspect_recorded_crash`, HAR→`inspect_web_network_capture`, browser→`list_browser_targets`, native/db→`open_binary`, IDA→`open_binary provider_id:"ida"`); (c) summary-first paging via `"detail": "summary"` → `parent_evidence_id` → `inspect_analysis_view`, with `get_evidence_bundle`/`export_evidence_bundle`/`rea inspect-evidence-bundle` fallbacks; (d) a 7-step staged-investigation workflow and an observations/inferences/unknowns discipline.
- source: `~/.npm/_npx/af752b90495482d7/node_modules/rea-agents/skills/reverse-engineer-anything/SKILL.md` (221 lines); sibling guides `references/{connection-and-recovery,native-and-artifacts,javascript-applications,android-applications,runtime-observation,evidence-workflows}.md` — all shipped in the tarball.
- verify: `cat "$(dirname "$(readlink -f "$(which rea 2>/dev/null)" || echo /home/vgpnk/.npm/_npx/af752b90495482d7/node_modules/rea-agents/scripts/rea.mjs)")/../skills/reverse-engineer-anything/SKILL.md"` or directly `ls /home/vgpnk/.npm/_npx/*/node_modules/rea-agents/skills/reverse-engineer-anything/`.
- verified-at: 2026-10-13
- suggested: admit — most load-bearing doc for *how* REA intends to be driven; the routing table alone answers "which verb for which artifact", which the bare index cannot.

## Candidate: README support matrix declares 16 target classes with per-target external-tool requirements; repo `docs/*.md` are linked but not shipped

- claim: `README.md` "What you can analyze" is a 16-row matrix (target → what REA returns → requirements): native binaries need Hopper/Ghidra/IDA; offline ELF layout, EVM bytecode and recorded Linux crashes need caller-supplied pwntools (Linux x64; pwndbg/GDB optional); JavaScript/Electron and .NET need no analysis engine; APKs need headless JADX + full JDK; Android devices need caller-supplied adb; JEB needs a caller-started MCP client (`REA_JEB_MCP_URL`); Android resources need an Apktool launcher; firmware needs Binwalk/Unblob; process capture needs a native PTY on Linux/macOS. The README "Documentation" index points at `docs/installation.md`, `docs/cli.md`, `docs/mcp-contracts.md`, `docs/mcp-prompts.md`, `docs/roadmap.md` etc. — none of which ship in the npm tarball (`docs/` absent), so they resolve only via github.com/morluto/rea.
- source: `<pkg>/README.md` lines ~145-308; `ls <pkg>/docs` → "No such file or directory".
- verify: `ls /home/vgpnk/.npm/_npx/af752b90495482d7/node_modules/rea-agents/` (no `docs/`, no `website/`); `grep -n 'docs/' README.md`.
- verified-at: 2026-10-13
- suggested: admit — the matrix is the authoritative capability/requirements contract; the unshipped-docs fact matters because offline corpus building must use the skill references, not the linked repo docs.

## Candidate: `rea doctor` and `rea capabilities`/`rea providers` are live self-documentation of the provider/substrate model

- claim: `doctor` emits `healthy`/`environment_healthy` + a `scope_checks[]` list with per-check `classification` and `remediation`. On this host: node 24.21.0 healthy, host linux/x64, **Ghidra 12.1.4 fully healthy** (8 checks: platform, architecture, installation, version, headless, native_decompiler, java), `hopper` = `missing_analysis_engine` (remediation: `rea setup` or `HOPPER_LAUNCHER_PATH`), `ida-registration` = `missing_analysis_engine` (remediation: `REA_IDA_MCP_CONFIG`, docs/ida-provider.md), `skill:identity` false → overall `healthy: false`. `capabilities`/`providers` emit ~18 operations each with `available`, `availability_code` (e.g. `unsupported_host` for macOS-only ops), an `effects` taxonomy (mutates_artifact / launches_process / may_show_ui / may_access_network / may_write_filesystem / changes_permissions / requires_root) and `limitations[]`.
- source: live `npx rea-agents@6.4.0 doctor`, `npx rea-agents@6.4.0 capabilities`, `npx rea-agents@6.4.0 providers` on this Linux host.
- verify: re-run the three commands; expect the same check names/classifications (Ghidra healthy, Hopper+IDA missing, macOS-only ops `unsupported_host`).
- verified-at: 2026-10-13
- suggested: admit — host-grounded evidence that native analysis on this machine binds to Ghidra; the effects taxonomy is the doc-level statement of REA's side-effect model (mostly read-only, runtime verbs marked explicitly).

## Candidate: Evidence is the canonical interchange format across the whole verb set

- claim: "Evidence" is a first-class contract noun throughout the docs: `evidence-export` validates + atomically writes "canonical Evidence JSON", `evidence-import` validates a "bounded local Evidence bundle", `inspect-evidence-bundle` reads one with `{path, detail, filters}`, `compare` diffs two canonical bundles, and dozens of verbs advertise "authenticated application Evidence" as input (e.g. `trace-application-feature`, `trace-javascript-semantics`, `project-*-application-graph`). SKILL.md adds the paging discipline (`parent_evidence_id`, `inspect_analysis_view`, `retention: "complete-record"`).
- source: `--llms` index rows for evidence/compare/trace/project verbs; `--llms-full` sections at lines 211 (compare), 433 (evidence-export), 617 (inspect-analysis-view), 737 (inspect-evidence-bundle); SKILL.md "Work summary-first" section.
- verify: `npx rea-agents@6.4.0 --llms | grep -i evidence`; `npx rea-agents@6.4.0 inspect-evidence-bundle --schema`.
- verified-at: 2026-10-13
- suggested: admit — names the central data contract every other verb produces/consumes; required vocabulary before interpreting any output.

## Summary

REA 6.4.0 self-documents via a three-tier manifest (`--llms` 127-command index → `--llms-full` per-command args/options → `--schema` typed contract) plus a shipped agent skill (routing table + Evidence paging doctrine) and README support matrix; on this Linux host the healthy deep-analysis provider is Ghidra 12.1.4, with repo-only `docs/*.md` linked but not shipped in the tarball.
