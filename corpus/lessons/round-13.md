# Lesson — arc3-loop1-round13 (steered round 13): source-curation capability

author: kaidoku-shokunin (L1), 2026-10-19
scope: the new source registry only; no ARM64X capability, target execution, or domain-knowledge admission
worktree: `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin`

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| 1 | reference-drift | The first fleet-root read attempted `/home/vgpnk/Projects/shokunin/AGENTS.md` and returned `not found`; the root listing had shown the fleet protocol files but no root `AGENTS.md`. No file was written. | Tool Policy / Exploration: `NEVER open guessed files`; root `PROTOCOL.md:433` defines `AGENTS.md` as per-repo operating rules. | Follow the canonical round-template load order and read the lane's known `AGENTS.md`; use the directory listing as the boundary instead of inferring a fleet-root file. |
| 2 | scope | A relative `LOG.md` edit resolved to `/home/vgpnk/Projects/shokunin/LOG.md`; a fresh read showed only my appended block, which I removed with an exact range cut. No main-repo commit was made. | User steer: main repo checkout read-only; write only the lane worktree and named report path. | Use absolute file paths for every existing-file edit and confirm the edit response resolved under the lane worktree before proceeding; remove and disclose any accidental out-of-scope addition. |

## Gate

### Registry conformance and census

The new registry uses the integrated 11-column Contract v1 header, with scoped tiers, exact revision/section anchors, opened quotes below, four ordered study paths, one bounded search note, and separate unopened leads. Rows are not a source quota and do not admit knowledge claims. `mined` here means the row is cited by this lesson's Gate via `used-by`; no new `corpus/knowledge/` entry was admitted.

SOURCES rows: **0 → 22** — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin` (2026-10-19). Before: the script reported the registry missing and `FLEET.rows 0` (exit 1). After: rows 22, tiers A=20/B=1/C=1, statuses mined=21/rejected=1, invalid tiers/statuses=0 and missing registries=0 (exit 0). No older row was edited or superseded.

### Freshly opened sources

Every row below was opened by the author on **2026-10-19**. Each excerpt is ≤25 words and is quoted with its exact source location. Local installed files are named by absolute path; external sources use their canonical URL.

| id | source URL or local path | quote and exact location |
|---|---|---|
| S001 | `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | “Do not treat those scopes as interchangeable.” — REA skill v42, `Route the target first` |
| S002 | `/home/vgpnk/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md` | “PIDs are historical metadata and never authorize live attach or control.” — REA skill v42, `Recorded Linux crashes` |
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` (SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`) | `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` — `GoRttiMapper.java:79` |
| S004 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 | “GP-6528 add support for golang 1.26” — commit title, 2026-03-03 |
| S005 | https://github.com/mandiant/GoReSym/tree/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d | “This library current handles the pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.” — README, `Version Support` |
| S006 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md` | “names of registers, and data types, are intentionally not incorporated into the features.” — Ghidra 12.1.4 tutorial, `How Does BSim Work?`, lines 15–20 |
| S007 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` | “Ghidra 12.1.4 Change History (September 2026)” — installed file title, line 1 |
| S008 | https://arxiv.org/abs/2609.05370v1 | “candidates that pass every shipped test still diverge from the original on our input corpus” — arXiv v1 Abstract, 2026-09-04 |
| S009 | https://aclanthology.org/2025.findings-acl.1194/ | “LLM-based methods surpass commercial tools in code understandability despite 52.2% lower functionality correctness.” — ACL 2025 Abstract |
| S010 | https://aclanthology.org/2026.acl-long.527/ | “BRIDGE combines control-flow-aware retrieval-augmented generation with feedback-driven verification.” — ACL 2026 Abstract |
| S011 | https://arxiv.org/abs/2607.12507 | “views from several tools do not necessarily provide independent evidence.” — arXiv Abstract, 2026-07-14 |
| S012 | https://www.electronjs.org/docs/latest/tutorial/fuses | “The loadBrowserProcessSpecificV8Snapshot fuse changes which V8 snapshot file is used for the browser process.” — `Current fuses` > `loadBrowserProcessSpecificV8Snapshot` |
| S013 | https://raw.githubusercontent.com/electron/electron/v44.9.0/build/fuses/fuses.json5 | `"load_browser_process_specific_v8_snapshot": "0",` — schema root, tag `v44.9.0` |
| S014 | https://www.electronjs.org/docs/latest/tutorial/asar-integrity | “Currently, ASAR integrity checking is supported on:” — `Version support` |
| S015 | https://api.osv.dev/v1/vulns/CVE-2025-55305 | “This only impacts apps that have the embeddedAsarIntegrityValidation and onlyLoadAppFromAsar fuses enabled.” — JSON `details` |
| S016 | https://blog.trailofbits.com/2025/09/03/subverting-code-integrity-checks-to-locally-backdoor-signal-1password-slack-and-more/ | “it did not consider heap snapshots as “executable” application content” — `From frozen pizza to unsigned code execution`, 2025-09-03 |
| S017 | https://github.com/suleram/View8/tree/ef39099b4f5076042173f9113382ebeb0630a56d | “Use --normalize to replace address-derived function names with deterministic names based on parse order.” — README, `Deterministic Function Names and Mapping CSV` |
| S018 | https://research.checkpoint.com/2026/breaking-the-seal-static-deobfuscation-of-jsceals-compiled-v8-bytecode/ | “The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.” — `Decompiled output`, 2026-08-31 |
| S019 | https://lief.re/blog/2025-02-16-arm64ec-pe-support/ | “a relocated view of the ARM64EC binary that is embedded within an ARM64X binary.” — `Parsing Improvements`, 2025-02-16 |
| S020 | https://blacktop.github.io/ipsw/docs/guides/dyld/ | “This command works on all platforms (not just macOS) and produces standalone MachO dylibs with correct segment layout, section offsets, and symbol tables.” — `dyld extract`, current guide fetched 2026-10-19 |
| S021 | https://docs.soliditylang.org/en/latest/abi-spec.html | “The first four bytes of the call data for a function call specifies the function to be called.” — `Function Selector`, current page fetched 2026-10-19 |
| S022 | https://jscdecompiler.com/blog/jsc-decompiler-vs-view8-vs-ghidra | “You upload a .jsc file through the browser, and it returns decompiled JavaScript.” — `JSC Decompiler`, published 2026-03-11 |

### Decision and limits

- S001–S021 are recorded as `mined` because this lesson cites their exact source passages; S022 is retained as an honest scope-specific rejection with a reason and a concrete flip condition in its `teaches` cell. The rejected source is not presented as evidence for a lane finding.
- The search note is in `corpus/SOURCES.md` and records its exact query, first-10-result boundary, deduplicated screening counts, exclusions, and stop rationale. Unopened material remains only under `Leads (unopened)`.
- No external non-author admit/reject spot-check was performed by this lane. The orchestrator owns registry admission and fresh non-author re-open; dispatched L2 reviewers do not count as that outside check. No discernment improvement is claimed here.
- No `corpus/knowledge/` file, `corpus/README.md`, PROVINCE frontier, or numeric axis score changed. The only technical additions outside the registry and lesson are one-line pointers in QUALITY/SKILL, per Contract v1 and the requested durable SKILL pointer.
- No ARM64X sample was sought or required; no target binary or artifact was executed, and no live REA provider/session was probed.

- S015 limitation: the opened OSV JSON's `details` prose names a 36.8.1 fix, while `affected[].ranges[].database_specific.extracted_events` includes 36.8.0. The row teaches comparing fields and cited fixes; this lesson does not adjudicate a release version from that inconsistent record.
