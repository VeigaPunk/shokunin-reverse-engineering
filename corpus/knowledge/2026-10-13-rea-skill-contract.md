<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/05-rea-skill.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 — REA skill (reverse-engineer-anything) curation

Studied artifact: `~/.agents/skills/reverse-engineer-anything/` (SKILL.md v37, `tool_count: 170`).
Tree: `SKILL.md` plus six references — `android-applications.md`, `connection-and-recovery.md`,
`evidence-workflows.md`, `javascript-applications.md`, `native-and-artifacts.md`,
`runtime-observation.md` (553 lines total). Read in full: `SKILL.md`,
`references/native-and-artifacts.md`, `references/evidence-workflows.md`.

## Candidate: REA is for shipped artifacts only — ordinary source-repo analysis is an explicit non-goal
- claim: SKILL.md's own description and opening section state REA is used only when a claim depends on a shipped binary/package, decompilation, passive runtime evidence, or version comparison vs. behavior not established by source; for a complete source repository the skill says to use normal repository tools and "do not run REA readiness or provider commands" (SKILL.md lines 3, 11-15).
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 3, 11-15
- verify: `sed -n '1,15p' ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verified-at: 2026-10-13
- suggested: admit — top-level scope gate; prevents routing ordinary repo questions into the binary toolchain.

## Candidate: Target routing is a decision table keyed on artifact class, with ~15 admitted classes
- claim: The "Route the target first" table maps each target class to a distinct entry tool: ASAR/JS-Electron tree→`analyze_javascript_application`; ZIP/APK/IPA/MSIX/AppX/DMG inventory→`open_binary`/`inspect_artifact`; Android APK code→`inspect_android_package`; managed PE/CLI→`inspect_managed_artifact`; firmware→`inspect_firmware_regions`/`extract_firmware` (caller-supplied Binwalk/Unblob); NativeAOT PE/ELF→native Ghidra route; open browser page→`list_browser_targets`; retained HAR/mitmproxy→`inspect_web_network_capture`; open Electron runtime→`list_electron_targets`; local EVM bytecode→`inspect_evm_interface` (raw|hex); offline ELF layout→`inspect_binary_layout` (pwntools); Linux x86-64 ELF core→`inspect_recorded_crash`; PE resources→`inspect_pe_resources`; native exe/lib/db→`open_binary`. DOS MZ and headerless DOS COM (`format: "dos-com"`, entry 0x10100) are additional admitted native classes in native-and-artifacts.md.
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 42-91; references/native-and-artifacts.md lines 58-70, 148-151
- verify: `grep -n '^- ' ~/.agents/skills/reverse-engineer-anything/SKILL.md | sed -n '1,20p'`
- verified-at: 2026-10-13
- suggested: admit — the table is the skill's core routing contract; each row is checkable against the advertised tool list.

## Candidate: Provider selection prefers an existing `rea` CLI, falls back to pinned `npx -y rea-agents@6.4.0`, and never bootstraps unrelated engines
- claim: SKILL.md directs callers to prefer an installed `rea` CLI; when absent and acquisition is in authorized scope, substitute `npx -y rea-agents@6.4.0`. Setup is read-only-first (show paths/backups/skill replacement) and "never installs or upgrades unrelated software, including Node.js, npm, Homebrew, Java, Ghidra, IDA, JADX, Binwalk or Unblob" — several providers (Binwalk/Unblob firmware, pwntools ELF layout, GDB/pwndbg crash context) are caller-supplied dependencies, not things REA installs.
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 35-40, 57-60, 76-80
- verify: `grep -n 'npx -y rea-agents\|never installs\|caller-supplied' ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verified-at: 2026-10-13
- suggested: admit — pins an exact acquisition path and a hard negative-install boundary; falsifiable by inspecting setup behavior.

## Candidate: IDA is a selectable provider on `open_binary`, but takes the original binary — never a database file — and lacks `binary_overview`
- claim: For an existing IDA MCP config, callers pass `open_binary` the original input binary with `provider_id: "ida"` and must NOT pass `.idb`/`.i64`; the legacy attached profile binds the already-open GUI input by SHA-256, the modern headless profile creates/closes an owned private database without saving; IDA supplies no `binary_overview` (SKILL.md lines 93-103). Other providers' availability is discovered live via `binary_session {}` → `result.tool_availability`, and unadvertised tools must not be called.
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 93-115
- verify: `sed -n '93,115p' ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verified-at: 2026-10-13
- suggested: admit — provider-selection rules with named failure modes (SHA-256 binding, session-owned DB, missing overview).

## Candidate: Workflow is summary-first with retained-evidence paging — never re-run a producer to read one object
- claim: The "Work summary-first" phase mandates the default result first; for unknown/large JS apps or ELF layouts call the producer with `"detail": "summary"`, then page the retained `parent_evidence_id` via `inspect_analysis_view` (summary / one section / module / symbol / stable page); on `resource_constraint` with `details.resource: "transport"` the record stays complete in the ledger and is read through views or `export_evidence_bundle`, never by repeating the producer; a client-truncated preview is treated as incomplete, not parsed as canonical JSON (SKILL.md lines 117-155; evidence-workflows.md lines 3-12, and native dossier facets like `value_flow_operations` with `next_offset` UTF-16 paging in native-and-artifacts.md lines 37-44).
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 117-155; references/evidence-workflows.md lines 3-12; references/native-and-artifacts.md lines 37-44
- verify: `grep -n 'detail": "summary"\|inspect_analysis_view\|resource_constraint\|next_offset' ~/.agents/skills/reverse-engineer-anything/SKILL.md ~/.agents/skills/reverse-engineer-anything/references/evidence-workflows.md`
- verified-at: 2026-10-13
- suggested: admit — the evidence-retention contract is the skill's distinctive mechanism; each rule cites a concrete tool/field.

## Candidate: Multi-feature investigations follow a 7-phase staged plan ending in checklist closure
- claim: "Plan broader investigations" prescribes: (1) request→question checklist with required evidence; (2) inspect existing session/DB/bookmarks/prior evidence and reuse, never duplicate; (3) smallest useful overview first, batch around a hypothesis, expand only on a concrete gap; (4) inspect packaged resources/config with format-aware parsers — no inference from filenames/strings alone; (5) corroborate with the evidence type the conclusion needs — runtime observation only when static cannot answer AND host runtime/OS access exists; (6) decompose into independent questions for parallel workers returning sources+conclusions+gaps; (7) maintain a finding ledger linking conclusions to Evidence IDs, confidence/type, search boundary, unknowns. Before finishing, every checklist item is marked answered/partially/unresolved and a broad investigation is never called complete while required questions are open.
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 168-201
- verify: `sed -n '168,201p' ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verified-at: 2026-10-13
- suggested: admit — the workflow phases contract; each step is independently checkable against the text.

## Candidate: Every conclusion must partition observations, inferences, and unknowns — static analysis is never claimed as observed execution
- claim: SKILL.md requires distinguishing observations/inferences/unknowns, citing Evidence IDs, preserving limitations and incomplete coverage, and never implying static analysis observed execution; runtime requests execute only the declared target/lifecycle (lines 157-160). This recurs per-domain: recovered pseudocode is "analysis observations, not original source" (native-and-artifacts.md line 33); managed inspection is execution-free — never claim loaded/reflected/executed (lines 83-87); NativeAOT recovered types are not original source (104-112); static `find_changed_behavior` differences are candidates, not causal proof, and `correlate_static_and_runtime` patterns are hypotheses not causality (evidence-workflows.md 29-34); `verify_reconstruction` passes cover only declared comparable claims, not global equivalence (35-36).
- source: SKILL.md lines 157-160; references/native-and-artifacts.md lines 33, 83-87, 104-112; references/evidence-workflows.md lines 29-36
- verify: `grep -n 'observations\|inference\|not original source\|not causal\|hypotheses\|global equivalence' ~/.agents/skills/reverse-engineer-anything/SKILL.md ~/.agents/skills/reverse-engineer-anything/references/*.md`
- verified-at: 2026-10-13
- suggested: admit — the epistemic hygiene rule is the most repeated clause in the skill; central to the workflow contract.

## Candidate: Ambiguous target selection refuses guessing — "my app" without name/path requires asking, and example apps are never substituted
- claim: When the user says only "my app" with no name/path/selected target, the skill mandates asking which app before searching; paths in unrelated saved reports and nearby test fixtures do not select the target; an app name should resolve to one clear installed artifact, ambiguous matches get asked about, and "never choose an example app on the user's behalf" (SKILL.md lines 105-109).
- source: ~/.agents/skills/reverse-engineer-anything/SKILL.md lines 105-109
- verify: `sed -n '105,109p' ~/.agents/skills/reverse-engineer-anything/SKILL.md`
- verified-at: 2026-10-13
- suggested: admit — an explicit refusal/safety rule against silently binding the wrong artifact.

## Candidate: Runtime-observation and capture tools are real execution with hard scope boundaries — declared target only, historical PIDs never authorize attach
- claim: `observe_native_calls` launches a real process under LLDB that "runs and may change files or use the network" and needs `get-task-allow` for hardened-runtime targets (native-and-artifacts.md 46-50); `inspect_recorded_crash` PIDs are "historical metadata and never authorize live attach or control" (line 10); EVM inspection performs "no chain lookup or target execution" with selectors/args as inferred candidates (SKILL.md 71-75); HAR capture inspection never fetches recorded URLs or claims live attribution (65-69); process captures "are opt-in behavioral evidence, not a security sandbox" and V3 cannot be upgraded to V4 (evidence-workflows.md 38-40); `finalization_ms` triggers SIGTERM-then-SIGKILL-once semantics with per-attempt delivery records (41-48); runtime requests "do not broaden the target or action beyond those fields" (SKILL.md 159-160).
- source: SKILL.md lines 65-75, 159-160; references/native-and-artifacts.md lines 10, 46-50; references/evidence-workflows.md lines 38-48
- verify: `grep -n 'never authorize\|not a security sandbox\|SIGTERM\|no chain lookup\|fetching recorded URLs\|broaden the target' ~/.agents/skills/reverse-engineer-anything/SKILL.md ~/.agents/skills/reverse-engineer-anything/references/*.md`
- verified-at: 2026-10-13
- suggested: admit — the execution-safety boundary; each clause is a testable refusal against scope creep.

## Candidate: Extraction and mutation tools have caller-blind destinations and atomic session scoping
- claim: `extract_artifact` takes no arguments and materializes into a REA-chosen fresh temp dir — "callers do not choose the destination"; symlinks and encrypted entries are inventory facts, not extractable (native-and-artifacts.md 136-140). `extract_firmware` instead requires a caller-selected new absolute output directory (SKILL.md 57-59). `annotate_native_function` changes are atomic and session-scoped, empty comments clear and omitted fields preserve, original executable bytes unchanged, edits invalidate immutable snapshots, and "Windows P0 does not admit database mutations" (native-and-artifacts.md 155). DMG traversal uses a read-only mount with owned temp dir and cleanup (142-146).
- source: references/native-and-artifacts.md lines 136-155; SKILL.md lines 57-59
- verify: `sed -n '136,155p' ~/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md`
- verified-at: 2026-10-13
- suggested: admit — concrete write-path rules separating inventory facts from filesystem mutations; falsifiable per tool schema.

## Candidate: Comparison/verification tools require explicit compatible inputs — absence claims need complete frontiers
- claim: `compare_artifacts` compares inventory pages by occurrence path/content/metadata/graph relations; `compare_functions` compares explicit function Evidence "not fuzzy whole-binary matches"; `compare_bundles` compares canonical membership and unknown history; `build_call_path` needs explicit function dossiers from one artifact/provider — "an incomplete frontier makes absence unknown" (evidence-workflows.md 21-32). Unresolved questions are tracked with `record_unknown`/`update_unknown` naming the required authority, with supporting AND contradicting evidence IDs, revision-checked updates, and only qualifying observed evidence can verify a resolution (14-19).
- source: references/evidence-workflows.md lines 14-36
- verify: `sed -n '14,36p' ~/.agents/skills/reverse-engineer-anything/references/evidence-workflows.md`
- verified-at: 2026-10-13
- suggested: admit — encodes the negative-evidence rule: absence claims are gated on frontier completeness.

## Candidate: Packed targets and format overrides require preserved identity separation — a decompiled stub is not the unpacked program
- claim: For packed targets the skill mandates retaining the original and the separately derived artifact identities because "decompiling an unpacking stub does not recover the unpacked program" (native-and-artifacts.md 69-70); headerless DOS COM must be opened explicitly with `format: "dos-com"` (CLI `--target-format dos-com`), entry fixed at 0x10100/file offset 0 with imposed real-mode segment context and unmodeled PSP/stack/device state (148-151); DOS MZ `inspect_native_load_image` verified import covers only the reported static image, not runtime DOS/PC-98 hardware behavior (58-63).
- source: references/native-and-artifacts.md lines 58-70, 148-151
- verify: `grep -n 'dos-com\|unpacking stub\|0x10100\|load_image' ~/.agents/skills/reverse-engineer-anything/references/native-and-artifacts.md`
- verified-at: 2026-10-13
- suggested: admit — small but sharp identity-preservation rules for derived artifacts and nonstandard formats.

## Summary
REA v37 is a shipped-artifact RE skill routing ~15 target classes through a first-tool decision table, with provider rules (existing `rea` CLI > pinned `npx rea-agents@6.4.0`; IDA by `provider_id` on the original binary), a summary-first→retained-evidence-paging→7-phase-investigation workflow, and refusal rules centered on three partitions: observations/inferences/unknowns, static-vs-runtime evidence, and declared-target execution scope.
