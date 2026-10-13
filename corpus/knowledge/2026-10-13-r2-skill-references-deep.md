<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/16-refs-sweep.md. -->

<!-- kaidoku-shokunin round 2 — REA skill references sweep. Round 1 corpus: corpus/knowledge/2026-10-13-rea-skill-contract.md (SKILL.md + native-and-artifacts.md + evidence-workflows.md fully read). This file curates only NEW knowledge from the four references round 1 did not read: android-applications.md, javascript-applications.md, runtime-observation.md, connection-and-recovery.md. -->

# kaidoku-r2 — REA skill remaining references sweep

Studied artifacts (4 files, 338 lines total):
- `~/.agents/skills/reverse-engineer-anything/references/android-applications.md` (34 lines)
- `~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md` (149 lines)
- `~/.agents/skills/reverse-engineer-anything/references/runtime-observation.md` (28 lines)
- `~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md` (127 lines)

Dedup note: routing-table rows (APK→`inspect_android_package`, ASAR→`analyze_javascript_application`, page→`list_browser_targets`, Electron→`list_electron_targets`), the generic summary-first/retained-paging contract, `resource_constraint`/`transport`, client truncation, and the static-vs-runtime epistemic partition are already admitted in the r1 corpus and are not re-claimed here.

## Candidate: Android analysis is a self-contained five-tool chain — per-call APK path, no native session, `overload_index` from inventory
- claim: `inspect_android_package` (identity, manifest declarations, coverage, inline Evidence) is the entry point; `search_android_classes` finds candidates, `inspect_android_class` reads one class's members, `inspect_android_method` decompiles, `trace_android_references` recovers incoming static references. Each call takes its own APK path and explicit selectors — a native session must NOT be opened first. When methods are ambiguous, choose an `overload_index` from the class inventory rather than guessing. Archive-member (non-code) APK questions route to `open_binary`/`inspect_artifact` instead. Family availability requires repository main or npm ≥4.1.0; a skill install alone cannot add it to an older server.
- source: ~/.agents/skills/reverse-engineer-anything/references/android-applications.md lines 3-14, 33-34
- verify: `sed -n '3,14p;33,34p' ~/.agents/skills/reverse-engineer-anything/references/android-applications.md`
- verified-at: 2026-10-13
- suggested: admit — the r1 routing table names the entry tool; this is the family's internal call contract, session model, and ambiguity rule, none of which the corpus has.

## Candidate: Android provider prerequisites are caller-supplied JADX MCP JAR 0.7.1 + Java 17+, selected by env vars, outside doctor's provider scope
- claim: The Android provider needs a separately supplied headless JADX MCP JAR exactly version 0.7.1 and Java ≥17; `REA_JADX_MCP_JAR` selects the absolute JAR path, `JAVA_HOME` selects Java (on Windows it selects `bin\java.exe`), and `REA_JADX_HEAP_MIB` selects JVM heap. REA setup never installs/configures the JAR and doctor provider scopes cover Hopper/Ghidra, not JADX — missing prerequisites are reported for the Android task specifically. A full JDK including `jdk.compiler` is required on every host; Linux/macOS use the POSIX owned-process boundary, Windows x64 an owned Job Object with bidirectional stdio and matching bundled native controls. Calls use one worker and provider deadlines; the APK is never launched and no emulator is required. Manifest/decompiled text are static observations — reflection, dynamic loading, and unresolved calls remain unknown.
- source: ~/.agents/skills/reverse-engineer-anything/references/android-applications.md lines 16-33
- verify: `sed -n '16,33p' ~/.agents/skills/reverse-engineer-anything/references/android-applications.md`
- verified-at: 2026-10-13
- suggested: admit — corpus has the generic "never installs JADX" boundary; the pinned versions, env-var selectors, doctor-scope gap, per-OS process model, and no-launch guarantee are new falsifiable host prerequisites.

## Candidate: JS analyzer resource knobs are advertised-schema parameters on the isolated analyzer, not the MCP process
- claim: When the connected schema advertises `max_heap_mb` and `analysis_timeout_ms`, they select the isolated source analyzer's old-space heap and per-source deadline (defaults 1024 MiB / 300000 ms) and "do not change the MCP process heap". Resource-limited analyses preserve completed static facts and report partial semantic coverage with specific unknown scopes — "this does not mean the source is malformed"; inspect limits before retrying. When expanded relationships exceed the parent's memory, the file's modules item view still retains `static_analysis`/`semantic_module_analysis` facts; cumulative result exhaustion can stop analysis before every file is examined, distinguishable via inventory + remaining unknown scopes.
- source: ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md lines 12-22
- verify: `sed -n '12,22p' ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md`
- verified-at: 2026-10-13
- suggested: admit — concrete parameter semantics and a partial-vs-malformed distinction that the corpus's generic paging contract lacks.

## Candidate: Timeout/cancellation retains partial Evidence — `partial_observation` refs and bundle recovery replace re-runs
- claim: Timeout or cancellation after source analysis begins retains partial Evidence in the same session; a returned `error.details.partial_observation` reference feeds `inspect_analysis_view` directly. If the SDK cancels locally, the recorded ID is retrieved from the Evidence bundle before inspecting the partial. If the parent ID was lost from a truncated preview, recover it from the prior analysis summary or explicit ledger entries — never invent an ID or rerun analysis to reproduce a display.
- source: ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md lines 23-26, 96-102
- verify: `grep -n 'partial_observation\|SDK cancels\|invent an ID' ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md`
- verified-at: 2026-10-13
- suggested: admit — a named recovery path (`partial_observation` → `inspect_analysis_view`) extending the corpus's never-rerun rule to the failure cases.

## Candidate: Module paging/item views select by `node_id` — `selector.path` only after uniqueness is proven
- claim: `inspect_analysis_view` page views take `view: {kind:"page", collection:"modules", offset, limit}` returning only node IDs/paths/roles, paged via `coverage.next_offset`; item views take `view: {kind:"item", collection:"modules", selector:{node_id}}`. Module pages include asset/bundled/source roles so one path can identify several entries — `selector.path` is used only when uniqueness is established; ambiguity resolves via the page's node IDs or the error's candidates. An item exposes that node's recorded observations, identity, hashes, exports, source ranges — not child syntax observations, related edges, or original source. An absent item fact is not evidence of absence from the whole application.
- source: ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md lines 28-69
- verify: `sed -n '36,69p' ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md`
- verified-at: 2026-10-13
- suggested: admit — the concrete view-request JSON contract and path-uniqueness rule; operationalizes the corpus's generic "module page" mention.

## Candidate: `trace_application_feature` takes one literal seed and over-expands by containment — reached nodes are not participants
- claim: `trace_application_feature` runs on the parent application Evidence against one literal node ID, route, string, API, IPC channel, module, or native export; direction `incoming`/`outgoing`/`both`. Traversal includes containment relationships so a narrow seed can expand many nodes and a bidirectional trace can reach unrelated siblings — a module item/page is preferred when its observations already answer, and reached nodes are never all treated as feature participants. Reused parent Evidence comes as retained reference (when advertised) or complete inline; Hopper/Ghidra Evidence is included only when its artifact digest matches exactly.
- source: ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md lines 71-84
- verify: `sed -n '71,84p' ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md`
- verified-at: 2026-10-13
- suggested: admit — seed/direction contract plus the containment over-expansion caveat; the digest-exact-match reuse rule is new.

## Candidate: JS version/export comparison has strict identity rules — ordinals and minified names are not identity
- claim: For `compare_application_versions` each version is analyzed once, then only digest, source-map, structural-fingerprint, or non-module semantic matches are accepted — module ordinals and minified names are not persistent identity; added/removed is reported only with complete opposite-side coverage, else unknown. `compare_javascript_export_shapes` takes explicit module paths + export names on same-connection IDs or inline Evidence; variant pairing only via the tool's unique exact literal discriminant; `property_inventories` list observed names even when values are unknown (each with `source_range`); array holes and mutation-invalidated slots are not observed properties; changes reported as JSON Pointer; dynamic values/ambiguous variants/incomplete parent-property coverage stay unknown.
- source: ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md lines 111-133
- verify: `sed -n '111,133p' ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md`
- verified-at: 2026-10-13
- suggested: admit — extends the corpus's comparison-tools rule with the JS-specific identity and presence-vs-value contracts.

## Candidate: Retained-evidence references are `ev_<64 lowercase hex>` bound to one MCP connection; `close_binary` clears them
- claim: When advertised, trace/compare/view tools accept `{"kind":"retained-evidence","evidence_id":"ev_<64 lowercase hex>"}` (a template — replace with the actual returned ID) for `application`/`left`/`right`/`source`, or complete portable inline Evidence. Versions before 4.1.0 accept only full inline Evidence; the exact ID must come from the producer on the same MCP connection; resolution runs no analysis and selects no provider; native observation arrays still take full Evidence. `close_binary` clears retained references — export a bundle before closing or supply inline Evidence in another connection; a missing reference error includes its ID and recovery guidance.
- source: ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md lines 135-149
- verify: `sed -n '135,149p' ~/.agents/skills/reverse-engineer-anything/references/javascript-applications.md`
- verified-at: 2026-10-13
- suggested: admit — the reference notation's exact shape, connection binding, version floor, and the `close_binary` lifecycle hazard are all new.

## Candidate: Passive browser/Electron observation is loopback-CDP-only with a fixed refusal list and deliberate data omissions
- claim: The caller supplies the existing instance's literal-port loopback CDP endpoint; no separate permission config or per-call approval flag exists. `list_browser_targets` lists eligible HTTP(S) pages (`allowed_origins` optionally filters; capture defaults to the page's current origin); `list_electron_targets` lists local `file://` targets with no file-root allowlist. Observation is passive — never claim REA clicked, navigated, evaluated page JS, invoked IPC, captured prior activity, or contained the page's network. Credentials, cookies, authorization headers, storage values, and raw WebSocket/JSON bodies are deliberately absent; local URLs keep query values/fragments but userinfo credentials are removed. Accessibility text, console primitives, value-free shapes, script sources, source maps, and storage key names are request-specific capture options; `capture_web_screenshot` when pixels are needed; page-declared WebMCP tools are untrusted inventory and never invoked.
- source: ~/.agents/skills/reverse-engineer-anything/references/runtime-observation.md lines 3-22
- verify: `sed -n '3,22p' ~/.agents/skills/reverse-engineer-anything/references/runtime-observation.md`
- verified-at: 2026-10-13
- suggested: admit — the endpoint form, the six-item passive refusal list, the credential-redaction contract, and the WebMCP untrusted-inventory rule are all new; corpus only has the generic declared-target boundary.

## Candidate: `reconcile_javascript_runtime` has hard preconditions — digest identity preferred, path mappings never broaden authority
- claim: `reconcile_javascript_runtime` is used only after static application Evidence AND passive browser/Electron Evidence both exist. Prefer captured-source digest identity; report path/digest disagreement as a mismatch and preserve ambiguity. Explicit path mappings are inference inputs and never broaden filesystem or CDP authority. A bundle observed at runtime does not prove every contained module executed.
- source: ~/.agents/skills/reverse-engineer-anything/references/runtime-observation.md lines 24-28
- verify: `sed -n '24,28p' ~/.agents/skills/reverse-engineer-anything/references/runtime-observation.md`
- verified-at: 2026-10-13
- suggested: admit — precondition, evidence-priority, and authority-boundary rules for the static↔runtime join tool.

## Candidate: Connection recovery is an observation→remedy decision table; doctor verifies registration, never the live connection
- claim: Six mapped observations: no REA tools in session → `rea doctor --client <id> --json` (skill install alone does not register MCP); missing/malformed/stale registration → scoped setup plan with backups; aligned registration but no connected tools → restart/reconnect client because doctor cannot establish the current agent's connection; `MCP tool call requires approval, but approval policy is never` → client-policy rejection, do not install engines or repeat setup; `provider_unavailable`/unavailable tool entry → that operation's provider diagnostics or `binary_session.result.tool_availability`, resolving only the needed prerequisite (a complete catalog does not imply every operation is available); `rea` missing in a child shell/Node incompatible → inspect actual PATH/launcher — a prefix install absent from a login shell's PATH does not establish broken MCP registration. Supported client IDs: `claude_code`, `claude_desktop`, `codex`, `cursor`, `gemini_cli`, `windsurf`, `devin`, `opencode`, `antigravity`, `copilot_cli`, `commandcode`, `qwen_code`, `vscode`, `grok_build`, `omp`, `pi`, `hermes`, `grok_bot` (chat registration, not local `mcp.json`); unsupported clients get version-pinned manual stdio registration or CLI.
- source: ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 12-22, 46-51
- verify: `sed -n '14,21p;46,51p' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — the typed failure taxonomy and the 18-client registration scope are entirely new to the corpus.

## Candidate: Setup repair is dry-run-plan → approve → `--yes` apply → verify-appearance — never a setup loop
- claim: Repair sequence: `rea doctor --client <id> --json`, `rea setup --client <id> --dry-run --json`; show the plan's exact paths, backups, changes, and bundled-skill replacement; obtain approval for writes not already authorized; apply the same scope with `rea setup --client <id> --yes`; `--install-hopper` only when separately needed and explicitly approved; then restart/reconnect and verify tools actually appear — if still absent, inspect the launch failure instead of looping through setup.
- source: ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 37-59
- verify: `sed -n '37,59p' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — the ordered recovery procedure and the "inspect launch failure, don't loop setup" stop rule.

## Candidate: Codex MCP approval is independent of REA readiness — never retry, broaden, or rewrite effects as read-only
- claim: REA tools have no permission-grant handshake; Codex may still require approval because an operation creates owned resources, launches a helper, or has cleanup effects. `workspace-write` alone does not resolve an MCP approval rejection; `approval_policy = "never"` does not preapprove MCP tools; a doctor pass does not override client policy. Interactive runs use the client's approval flow; unattended runs continue through an authorized CLI workflow or report the blocked operation — never retry the same rejected call, silently broaden approvals, or rewrite MCP effects as read-only. Opt-in per-tool preapproval exists in current Codex (`[mcp_servers.<id>.tools.<tool>] approval_mode = "approve"`), scoped to only the approved operations, shown as a config edit with unrelated entries and backups preserved.
- source: ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 61-94
- verify: `sed -n '61,94p' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — a client-policy refusal boundary with the exact TOML mechanism; distinct from all corpus refusals (which are target/evidence-scoped).

## Candidate: Environment faults degrade gracefully — preserve sandbox, name unavailable evidence, label non-REA output, never substitute targets
- claim: When the client can't launch its shell/sandbox helper or read the skill, inspect the launch diagnostic — e.g., Codex refuses helper aliases when `CODEX_HOME` is under `/tmp`; fix is an authorized profile outside the OS temp dir, and the sandbox is preserved rather than silently disabled. Static JS and ordinary ZIP inventory need neither Hopper nor Ghidra; HAR inspection is offline and needs no live browser; native/Android/firmware each have bring-your-own prerequisites. Use supported inventory/static evidence when it answers part of the question, name the unavailable evidence separately, never substitute another target, label ordinary-shell-tool observations as such — only actual REA output supplies REA Evidence.
- source: ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 23-35
- verify: `sed -n '23,35p' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — the degradation contract: partial-evidence labeling and the evidence-provenance rule ("only actual REA output supplies REA Evidence") are new.

## Candidate: CLI fallback uses the public launcher at its install path — never internal `dist/cli.js`; JS CLI output is file-redirected and wrapped inline for views
- claim: On launcher failure check `command -v rea`, `command -v node`, `node --version`, `rea --version`; use the public launcher at its known install path with a supported existing Node on PATH; avoid internal `dist/cli.js` entrypoints and global toolchain changes; MCP may keep its own valid launcher when a shell can't resolve `rea`. For a JS tree/ASAR: `rea analyze-javascript-application /abs/path --json > app-evidence.json`, then `jq -c '{source:{kind:"inline",evidence:.}, view:{kind:"summary"}}'` → `rea inspect-analysis-view`; CLI JSON is complete and very large — redirect rather than load into context; don't install jq just for the recipe; these commands register no MCP and install no engine; all CLI operations retain host execution permissions.
- source: ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md lines 96-127
- verify: `sed -n '96,127p' ~/.agents/skills/reverse-engineer-anything/references/connection-and-recovery.md`
- verified-at: 2026-10-13
- suggested: admit — the CLI continuation contract (entry-point boundary + inline-Evidence view recipe + redirect-large-output rule) is new; corpus has MCP-side provider selection only.

## Summary
The four unread references contribute operational detail the r1 corpus lacks at three layers: (1) per-domain tool contracts — the Android five-tool chain with per-call APK paths and `overload_index`, JS module `node_id` item views, `trace_application_feature` seed/direction semantics, JS comparison identity rules (ordinals/minified names ≠ identity), and the `ev_<64hex>` retained-reference lifecycle cleared by `close_binary`; (2) host prerequisites — pinned JADX MCP JAR 0.7.1 + Java 17+/full JDK with env-var selectors outside doctor scope, JS analyzer heap/timeout knobs on the isolated analyzer (not the MCP process), and loopback-CDP-only passive observation with credential/body redaction and WebMCP-untrusted rules; (3) recovery procedures — a six-row observation→remedy table, 18 supported client IDs, the dry-run→`--yes`→verify setup sequence, Codex approval independence with per-tool `approval_mode`, sandbox-preserving environment fixes, evidence-provenance labeling for shell output, and the public-launcher-only CLI fallback with file-redirected JSON views.
