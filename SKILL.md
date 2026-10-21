---
name: kaidoku-shokunin
description: Domain specialist — reverse engineering of shipped artifacts with REA on this Linux host — native ELF/PE through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript bundles, archives and packages, managed assemblies, firmware images and recorded crashes; evidence-first static analysis that keeps observation, inference and unknowns separate. Trigger on "shipped binary", "decompile", "what does this .asar/.exe/ELF do", "compare two versions of this package", "analyze this core dump". Anti-trigger: ordinary source repositories — use normal repo tools, never run REA on available source. Rank: shonen.
---

# kaidoku-shokunin

## Domain

Reverse engineering of shipped artifacts with REA on this Linux host. Owned
surfaces (verified 2026-10-13, see PROVINCE.md): the `rea` MCP server + CLI
(`npx -y rea-agents@6.4.0`, 170 MCP tools / 127 CLI commands; historical, verified 2026-10-13), the Ghidra 12.1.4
provider (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`, JDK 21), ELF analysis
end-to-end (`analyze`/`search`/`decompile` verified on `/usr/bin/jq`),
ASAR/JavaScript analysis (`analyze_javascript_application` verified on
`default_app.asar`), archive/package inventory, and host binutils fallbacks.

Current REA package inventory by configured client (re-read 2026-10-20, round 19): Devin/OMP
`rea-agents@6.7.0` (207 MCP tools / 153 CLI commands, since 2026-10-20 13:35:56 -03); Kimi
`rea-agents@6.7.0` (207 / 153; tools_sha256 `af39310c…`; 6.4.0 historical per PROVINCE.md).

Drift-sensitive values: `GHIDRA_INSTALL_DIR`, `JAVA_HOME` in the three client
configs (devin/omp/kimi), the per-client REA pin (see current inventory above), the installed skill
version. Probe convention: `rea doctor` = environment verdict (read
`scope_checks[]`, not the top-level bool), `binary_session {}` = live verdict —
a catalog-listed tool is available, not held.

## Working contract

- Route the target first (decision table below). All verified on this host
  2026-10-13; a catalog-listed tool is available, not held — `held` requires a
  carrier run this round (QUALITY.md #10).
- Work summary-first: `detail:"summary"` → `parent_evidence_id` →
  `inspect_analysis_view`. Never re-run a producer to read one object.
- Label every conclusion observation / inference / unknown. Static output is
  never "observed execution". See `corpus/knowledge/2026-10-13-elf-observation-jq.md`.
- Pin the target: path + sha256 before any analysis; magic bytes are not
  format proof (`0xCAFEBABE` bin → `mach-o-universal` false positive).
- Sessions are ephemeral `/tmp/rea-ghidra-*`, shared across lanes — never
  clean another session's dir. `--snapshot` persists evidence, not the DB.

## Decision table (this host, r3-verified)

| Target | First move | Status |
|---|---|---|
| ELF exe/lib | `rea analyze` → `search` → `decompile`/`function` | held (jq, libjq) |
| `.so`/`.node` vaddr | `nm` addr **+0x100000** = REA addr; confirm via `address-to-file-offset` | held |
| PE x86-64 / ARM64 | `rea analyze` (Ghidra PeLoader, wine-free) | held (cli-64, cli-arm64) |
| `.asar`/JS bundle | `analyze_javascript_application`; >~4MB single files OOM → extract + `--artifact-format directory` | held (obsidian ×2, typora, signal census) |
| Archive/APK | `inspect-artifact` → content graph; `.so` members → extract + `analyze` | held (Godot APK) |
| AppImage | `analyze` (ELF only); payload via `read-bytes unallocated_0:0x…` | held; `extract-artifact` has no ELF reader |
| Recorded core ≤32MiB | `coredumpctl dump` (output already decompressed ELF — no `zstd -d`) → `inspect-recorded-crash` (needs `REA_PWNTOOLS_PYTHON` uv venv) | held; >32MiB cores refused `out_of_range` |
| Mach-O synth carrier | `inspect-keyed-archive`, `decode-interface-builder`, `trace-dylib-resolution` | held on synth carriers (recipes in corpus) |
| EVM bytecode | `inspect-evm-interface <file> <raw|hex>` — encoding POSITIONAL | held (selector recovery) |
| Runtime targets | self-launch `chromium --remote-debugging-port=9222` / `xvfb-run electron …:9223` → `list-*-targets` → `inspect-*-page` | held |
| `.jsc` V8 bytecode | `ELECTRON_RUN_AS_NODE=1` + version-matched electron (V8 map in corpus) → `--print-bytecode` | held r4 (typora→electron42.2.0) |
| Firmware blob | `inspect-firmware-regions` (binwalk 3.1.0), `extract-firmware` (unblob 26.6.4) | held r4u; RISC-V `target_unavailable` bypassed via e_machine patch + language override (r5-01) |
| Android APK | `inspect-android-package`/`decode-android-resources`/`inspect-android-method` (jadx-mcp 0.7.1, apktool 3.0.3) | held r4u; real Java decompile |
| Managed DLL `0x14c` | `inspect-managed-artifact`/`inspect-managed-members` <64MiB; else dnfile+dncil | held r4/r4u; `0xfd1d` class → dnfile only |
| JS minified source | `recover-javascript-sources <FILE> <outdir>` (file arg; wakaru ELF binding) | held r4u |
| JS runtime verbs | `observe-web-session`/`observe-javascript-runtime`/`reconcile-javascript-runtime` on self-launched targets | held r4; `capture-electron-scenario` refused |
| Binary layout | `inspect-binary-layout` (pwntools venv `~/.local/share/kaidoku-pwnenv`) | held r4 |
| adb (device-free) | `inspect-adb-client`, `list-adb-devices` only — 22/24 need a device | held r4u |
| AppImage inner | unblob carve at `--appimage-offset` → `7z` on squashfs → inner asar analyze | held r4 |
| >90MB PE | `provider_timeout` at ~900s internal deadline — raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`+`GHIDRA_HEADLESS_MAXMEM` | measured r4 |
| IDA/Hopper/JEB | env keys absent | frontier |

## Error patterns (typed refusals)

| Error | Meaning | Move |
|---|---|---|
| `provider_unavailable`, retryable:true | provider engine absent (`REA_PWNTOOLS_PYTHON`, `REA_IDA_MCP_CONFIG`) | operator-owned env key; retryable after provisioning |
| `capability_unavailable`/`unsupported_provider`, retryable:false | tool absent (`REA_JADX_MCP_JAR`, `REA_APKTOOL_COMMAND`, `REA_BINWALK_COMMAND` 3.1.x, `REA_UNBLOB_COMMAND` 26.6.x, `REA_WAKARU_COMMAND`) | both kinds exit **1** — check `retryable`, not RC |
| `unsupported_target` | wrong carrier (plain plist, >32MiB core, ELF→`extract-artifact`, `binary_overview`→paging) | change carrier, not args |
| `unsupported PE architecture` | managed DLL of refused class (x64 R2R `0xfd1d`, x64 IL-only) — `0x14c` IL-only works | dnfile+dncil covers the refused class |
| `provider_timeout` | internal ~900s session deadline (GhidraClient.js:607), not outer `timeout` | raise env timeouts + heap; measured at 91.6MB PE |
| `Unknown flag` | arg is positional (evm encoding, keyed-archive `archive`, addresses) | schema properties ≠ argv flags |
| `out_of_range` | input exceeds cap (32 MiB crash, 16 MiB EVM file) | split/dump subrange |
| `invalid_format`/`invalid_input` | syntax (e.g. `search` needs `--mode regex --pattern '.*'`; `.zst` not a core) | re-shape input |

## Queue-drain craft (rounds 5-12, distilled in round 13)

Decision rules distilled from the round 5–13 queue-drain corpus entries; each
bullet is bounded by the lines it cites.

- **Evidence ids are content-addressed per verb family — never substitute ids
  across invocation shapes.** Many families re-derive byte-identical ids and
  envelopes across re-runs, lanes, and rounds (native verbs
  `corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md:84-91`; JS workflows
  `corpus/knowledge/2026-10-13-r8-02-queue-a-ops-2.md:99-123`; ledger verb
  `corpus/knowledge/2026-10-14-r9-01-queue-a-ops.md:221-249`; an id held
  across a day and re-derives byte-exact
  `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`). Per-run id
  classes are recorded too: raw_result embeds a mkdtemp staging path (jadx,
  firmware-regions —
  `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md:131-133`) and per-run
  UUIDs/provider_ids ride inside normalized_result (binwalk regions, unblob
  chunks — `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:67`); CDP and
  process-capture envelopes are wall-clock-parameterized by design
  (`corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md:44-48`,
  `corpus/knowledge/2026-10-14-r11-01-queue-ops.md:212-217`); and
  `compare-managed-members` mints internal member ids that differ from CLI
  ids at identical bytes
  (`corpus/knowledge/2026-10-14-r10-01-queue-ops.md:89-96`). Establish the
  family first, then verify byte-exact (content-addressed) or run-normalized
  (per-run) accordingly
  (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:5`).
- **Raw file vaddrs must be pre-shifted +0x100000 into Ghidra space for every
  native verb on ELF PIE/DYN.** Proven on an executable (`/usr/bin/jq`,
  `corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:144-146`) and on
  shared objects (libjq
  `corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md:174-177`; glibc `setenv`
  and libgtk `gtk_button_new`
  `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:268-272`). An unshifted
  address is answered honestly, never decoded as garbage: typed
  `outside-memory`, exit 0, null bytes
  (`corpus/knowledge/2026-10-13-r7-02-queue-a-ops-2.md:47-60`).
- **Refusal families and cost classes.** `VALIDATION_ERROR` = zod
  fieldErrors, pre-analysis ~0.7 s
  (`corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:25-51`);
  `invalid_request` = semantic, in BOTH cost classes — pre-analysis 0.7 s on
  argument exclusivity
  (`corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md:93-119`) but
  post-analysis ~14.2 s after a full import when a name must resolve against
  the analyzed program
  (`corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md:118-134`);
  `capability_unavailable` = env gates such as `REA_BROWSER_EXECUTABLE`,
  invisible in the capabilities matrix
  (`corpus/knowledge/2026-10-14-r11-01-queue-ops.md:63-74`);
  `provider_unavailable` = missing engines / clean environment
  (`corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md:78`,
  `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:24`). `retryable`
  marks transport retryability, not arg-fixability
  (`corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md:117-119`), and refusal
  latency is not a validity signal
  (`corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md:130-132`).
- **Four authority grades — cite a conclusion at the grade its envelope
  declares.** `observed`+`shipped-artifact`: provider observation of the
  pinned artifact bytes
  (`corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:55-57`);
  `inferred`+`analyst-inference`: derived analytics over an authenticated
  input, citable as inference never as artifact observation
  (`corpus/knowledge/2026-10-13-r8-02-queue-a-ops-2.md:78-90`) and never
  promoted to exact identity
  (`corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md:53-54`);
  `observed`+`historical-reference`: retained producer evidence without
  execution attribution — "Recorded URLs are never fetched"
  (`corpus/knowledge/2026-10-14-r10-01-queue-ops.md:166-173`);
  `observed`+`controlled-replay`: scripted pty replay with residual unknowns
  stated (`corpus/knowledge/2026-10-14-r11-01-queue-ops.md:197-207`).
- **Input contracts are shape-gated.** Ledger/coverage verbs consume a
  canonically wrapped Evidence bundle — hand-wrapped manifests refuse "not
  canonical"; wrap with the package's own `createEvidenceBundle`
  (`corpus/knowledge/2026-10-14-r9-01-queue-a-ops.md:41-48`). The
  application-graph projectors take a homogeneous `inspect_artifact`-only
  inventory — keyed-archive/IB evidences are schema-valid yet
  workflow-refused, and the same refusal string and law hold for Android
  (`corpus/knowledge/2026-10-14-r11-02-queue-ops-2.md:51-65`,
  `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:50`). Native CLI verbs
  are positional `{path, address}` — schema properties are not flags
  (`corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:36-41`).
- **Module attribution is caller-attested, not proven.** `analyze_function`
  ids hash content+parameters, not the path: the same glibc bytes under a
  renamed path flip one P/Invoke verdict `contradicted`→`verified`
  (`corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:106-141`), and a
  subject-only rewrite reproduces the renamed-path envelope bit-for-bit at
  the same id — verdicts attest the analysis, callers attest the module; pin
  request bytes when module identity matters
  (`corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`).
- **Tool acceptance ≠ correctness.** `trace-web-source-location`'s VLQ
  validator catches dangling continuations yet accepted a semantically wrong
  line-delta map; the defect surfaced only via an independent decoder — never
  treat a pass as input correctness; cross-check independently
  (`corpus/knowledge/2026-10-14-r11-01-queue-ops.md:123-129`, run log :311).
- **Census rows can be defects — check holdings before exercising.** Six
  recorded instances of rows queued while already held: row 7 / table line
  171 (`corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md:247-275`), lines
  181–183 and 187 (`corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md:25-60`),
  L195 (`corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md:161-166`,
  "sixth instance"). Same-round wave entries count as exercised
  (`corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md:262-265`); the drain
  move is a holdings pre-check with re-derivation, "do not re-exercise"
  (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:1`); later-held
  Queue-B rows that postdated the census were bookkeeping lag, not
  wrong-at-write defects
  (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:105-108`).
- **Provisioning hints can be wrong — verify the gate, not the hint.** The
  census's `chromium --log-net-log` hint refuses typed against a real netlog;
  the operative gate is a har-schema-valid capture (playwright `recordHar`
  satisfies it) (`corpus/knowledge/2026-10-14-r10-01-queue-ops.md:138-142`).
  Same class: an env gate invisible in the capability matrix — census gates
  can be incomplete in BOTH directions
  (`corpus/knowledge/2026-10-14-r11-01-queue-ops.md:72-74`) — and the
  pwntools "one-fix" that is really the pin `setuptools<81`
  (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:23`).
- **Citations into an operator-mutable file anchor by stanza key + receipt,
  never by bare line number.** `~/.kimi-code/config.toml` moved the
  `[mcp_servers.rea]` stanza `:1284` → `:2938` → `:3225` → `:3296` in one day
  (four `.bak` generations plus the live file; round-3 receipt
  `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt`), and every
  re-point minted a fresh dead number — round-3's own declared target
  `:2938`/`:2940` was dead before the round closed
  (`corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:938-950`). Cite the
  key (`[mcp_servers.rea]`, `args`) and qualify it with the receipt that
  captured the value (`PROVINCE.md:18`, `SCORECARD.md:59`); a line number may
  appear only inside an append-only record that names its capture stamp.
- **Config custody is a pre/post-pair — a zero-drift claim without its own
  pre-pair is void.** luna-round-8 closed zero config drift against the
  round-6 baseline with no round-8 pre-pair — recorded as carried debt
  (`SCORECARD.md:544-545`; `LOG.md:856-858`) and stated as a limitation in
  the battery entry itself, "No config-drift pair"
  (`corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`). Freeze
  the sha256 of every drift-sensitive client config before dispatch and
  re-verify after the battery; only the bracketing pair supports a
  zero-drift claim — a post-only comparison is void, not a weaker grade.
  A baseline-relative hash match may be reported as baseline-relative; it
  is not a same-round zero-drift observation.

- **Long Ghidra analyze runs are transient user services, not scoped
  processes.** `systemd-run --user --scope` ties the run to its launcher's
  lifetime: the round-4 91.6MB run's scope tore down when the launching shell
  exited, and only the journal preserved the true cause (memcg OOM at its own
  7G cap — containment worked; lifetime failed). The service form (`--user`,
  no `--scope`) survives the launcher and keeps `MemoryMax` containment plus
  file-captured envelopes: round 6's mid-rung HELD that way
  (`corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:13`) and round 7's
  91.6MB wall-leg HELD that way with the validated analyzer-disable recipe
  (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:5-13`). Add an explicit
  unit name, a memory+swap cap, a disk-backed non-dot TMPDIR, and read the
  verdict from the sealed envelope plus the journal — never from the unit's
  post-collection residue. Caller-kill survival is untested — recorded
  unknown, never asserted.
- **A mitigation claim carries its natural control: same target, caps, and
  deadline; only the treatment is absent.** Compare paired outcomes before
  attributing necessity; cite both runs. The 91.6MB PE held with three
  registry-validated analyzers disabled
  (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-19`); the matched natural
  control omitted the disables under the same caps/deadline and was
  kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).
- **An artifact that records its own byte-identity must re-derive that
  identity after every revision; a stale self-identity voids the verification
  block, not the work.** Size/hash/line-count claims bind the bytes they
  describe, not an earlier revision of the same patch: after the C1 entry
  patch was revised, its step-4 claim still read 8,316 B / `f95c5a05…` while
  the applied bytes hashed 8,598 B / `d8d85949…`
  (`.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89`), and the chain measured
  three applied identities inside ~20 minutes, the fix being the fresh landing
  hash (`.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md:149-153`). The
  voided block is re-established by re-running its checks against the current
  bytes; the integrator records the fresh identity of the landed revision —
  10,225 B / `dd986f56…` for the landed entry
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`, whose recheck line
  records the mid-wave revision (`SCORECARD.md`'s `arc3-loop1-round1` section,
  the "fresh identity recorded" line; `LOG.md:1411-1412`) — never a revert,
  never a carried-over number.
- **A parsed-and-empty result is a statement about the parser's scope, never
  proof of byte absence — settle byte questions with a census (decode, locate,
  hash), not with the probe's function count.** The r1 creation legs probed
  0 functions (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`)
  on blobs that byte-contain the full runtime; the round-3
  byte census measured that embedding and the entry's append-only erratum
  corrected the wording to tool-scope parsed-and-empty, "not byte-level
  absence" (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:31`). The
  same correction re-landed on the r3 entry
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:41-51`) and on
  r4's initcode legs — "creation probes parse empty while the runtime bytes
  are present verbatim"
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:39-46`) — after the
  entry had repeated the r1/r3 class
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17`). The trap legs
  are the second face of the same mistake: raw-over-hex-text reads exit 0 /
  0 functions on ASCII bytes — a probe-input trap, not a carrier defect
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:27`;
  Vyper repetition `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:25`).
  The tool's own limitation says it: "empty results do not prove absence of
  dispatch" (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29`). Word
  zero-findings at their class (parsed-and-empty vs excluded-from-inventory,
  `corpus/QUALITY.md:21`) and only then claim or deny byte presence.
- **Co-land every truth dependency.** Before repairing a statement whose
  truth depends on another deliverable, name the dependency in the patch or
  claim (for example, a corpus entry ↔ its map token, or a receipt/pointer ↔
  an instrument extension). Until every side can land together, keep the
  dependent statement conditional or defer it; a scratch projection is not a
  landed result. Land the dependency set in one commit, then rerun the named
  acceptance check against that commit and record the measured revision. In
  r4, the EVM bullet's Vyper wording depended on C1's corpus entry
  (`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:332-335`); in r8, the
  pointer and receipt were required with C1's `ptr_check` extension
  (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-50`). Corpus precedents:
  `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:51-57`,
  `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5-6`,
  and `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:17`.
- **Evidence-id field sensitivity is projection-local — measure it per
  operation, never infer it from the `ev_` prefix.** Pin verb, version,
  call shape, and bytes; recompute IDs from complete envelopes; compare
  a same-path repeat with a byte-identical alternate-path call; name the
  exact differing projected fields, with outer display fields as the
  negative control; mutate only the candidate field set — when it fails
  to reproduce the alternate-call ID, diff the remaining projection and
  never attribute the whole delta — and bound the result to operation,
  version, input, and call shape. EVM and Rust carry path in
  `parameters.path`, `normalized_result.artifact.path`, `locations[0].path`;
  `inspect_artifact` needs nested `substeps[0].evidence.subject.local_path`
  plus `normalized_result.inspection_id` to reproduce the copy ID
  (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:11`,
  `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:17-22`,
  `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15`,
  `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:19-22`,
  `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:11-15`,
  `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:19`;
  the non-isolation of the nested path alone is the round-12 verdict's
  in-memory mutation control,
  `.ufo/waves/arc3-loop1-round12/claims/verdicts/VZ-1.md:42`; rule draft
  `.ufo/waves/arc3-loop1-round12/claims/c2/EX-16.md`).




## Config custody for live-probe rounds (SOP)

Binding for every future live-probe round. A zero-drift claim without its own
same-round pre-pair is void: luna-round-8 closed zero config drift against the
older round-6 baseline with no round-8 pre-pair — carried debt
(`SCORECARD.md:544-545`; `LOG.md:856-858`), stated in the battery entry itself
as "No config-drift pair."
(`corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`).

- **Freeze the pre-pair before the round's first probe — no probe runs on an
  unpaired round.** Hash exactly five paths, fixed order devin/omp/kimi then
  the two shell files — the three drift-sensitive client configs plus the
  shell files that carry the same drift-prone env-key material — under a UTC
  timestamp line into the round's receipts directory:
  `R=<round-wave-dir>/receipts`;
  `{ date -u +%Y-%m-%dT%H:%M:%SZ; sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile; } > "$R/config-pre-pair.txt"`.
  Capture rc must be 0; rc≠0 means a path was unreadable and its line is
  absent. Then gate the receipt's shape: `wc -l` = 6,
  `grep -cE '^[0-9a-f]{64}  /'` = 5, one timestamp line
  (`grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'` = 1),
  and five path-identity lines
  (`grep -cE '^[0-9a-f]{64}  /home/vgpnk/\.(config/devin/mcp_config\.json|omp/agent/mcp\.json|kimi-code/config\.toml|bashrc|profile)$'` = 5).
  A missing path leaves no line, so a truncated receipt false-passes
  `sha256sum -c` — the shape gate is mandatory, not advisory.
- **Why the shell files are in scope.** `PROVINCE.md:15-26` tracks
  `.bashrc:23-24` and `:61` as drift-prone (and via `:47` `.profile:4`, via
  `:124` `.bashrc:63`). A `.bashrc` edit changes provider wiring while all
  three client-config hashes stay byte-identical — the falsification case,
  with the r4u-05 misbinding as precedent
  (`corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:104-108`). `.bashrc`
  carries `GHIDRA_INSTALL_DIR`/`JAVA_HOME` (`:23-24`) and the seven `REA_*`
  exports (`:58-64`); `.profile` carries `GHIDRA_INSTALL_DIR`/`JAVA_HOME`
  (`:3-4`) and six `REA_*` exports (`:7-12`) for POSIX login shells. Excluded:
  `~/.bash_profile` (sources `.bashrc`, exports no `REA_`/`GHIDRA`/`JAVA`
  key of its own), the systemd user environment (not a file — it cannot be
  receipted), and `~/.kimi-code/mcp.json` (no `rea-agents` pin).
- **Read-only, always — the pair never edits a config.** The five paths are
  operator-owned; the lane documents the gap and never edits, repairs, or
  restores them (`PROVINCE.md:108-113`). A probe that writes config is an
  operator-owned incident, not a custody step. Hashing stores digests only,
  never contents.
- **Take the post-pair after the last leg exits and every session is
  closed.** Re-capture with the identical format and shape gate to
  `"$R/config-post-pair.txt"`; then compare the live files against the frozen
  pre-pair: `tail -n +2 "$R/config-pre-pair.txt" | sha256sum -c -` — zero
  drift is rc 0, exactly five `OK` lines, empty stderr. Filter the timestamp
  line (`tail -n +2`): `-c` on the unfiltered receipt emits
  `sha256sum: WARNING: 1 line is improperly formatted` with rc still 0 — a
  formatting warning, not a pass and not drift.
- **`tail -n3` is not a config selector on a five-hash receipt.** On the
  superseded four-line three-path receipt `tail -n3` and `tail -n +2` were
  content-identical; on the six-line five-path receipt `tail -n3` selects
  kimi plus the two shell files, not the three client configs. Configs-only:
  `tail -n +2 "$R/config-pre-pair.txt" | head -n3`. Shell-file leg:
  `tail -n +2 "$R/config-pre-pair.txt" | tail -n2`.
- **Compare same-round only.** The pair brackets this round's probes; a
  cross-round comparison falsely reports drift — `~/.kimi-code/config.toml`
  legitimately changed between luna-round-6 (`4af27747…`,
  `.ufo/waves/luna-round-6/SB2.md:11`) and the arc2 pre-pair (`3546e033…`,
  `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt:4`; the same
  value sits at line 4 of the superseded three-path receipt,
  `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt`).
- **Drift disposes the claim, not the config.** Content drift (`FAILED`,
  rc≠0) or state drift (capture rc≠0; check-time unreadable path →
  `FAILED open or read`, rc≠0): the zero-drift claim is VOID — record the
  path with both hashes verbatim in the round report and LOG entry, do not
  edit or restore the file, classify as operator-owned incident; the round's
  other axis measurements stand. Malformed receipt: re-capture once;
  persistent malformation is VOID.
- **Commit both receipts tracked.** The pair is the durable evidence — the
  zero-drift claim cites the pre-pair timestamp and the committed post-pair
  receipt (round-6/round-8 durability precedent, `LOG.md:796`, `LOG.md:850`),
  not a re-run of the hash.

## Checklists

**Before any claim of "held":** carrier ran this round? evidence_id or
reproducing call cited? providers `status` (not per-op `available`)? versions
pinned per client (see current inventory above; Ghidra 12.1.4, JDK 21)?

**Before "empty/clean" claims:** parsed-and-empty vs excluded-from-inventory?
(`parse_failures:0` on unparsed members means nothing — typora lesson.)
Callers via objdump? GOT-indirect calls invisible — use `xrefs`.

## Known limits (r4)

- `record_pairs`/`compare_functions` have no CLI verbs — domain/MCP only;
  `changed` needs ALL bundle members paired.
- MCP session retention is epoch-scoped; `evidence_links` pin records across
  targets; evidence-id identity is verb-family-specific, not a universal
  formula — the revenger-verifier family mints path-sensitive ids (same bytes
  at different paths → different ids; jadx ids are per-run, apktool ids
  deterministic on identical invocations), `analyze`/`inspect` and
  `analyze_function` ids stayed equal across paths (`analyze_function` hashes
  analysis content + parameters, not path), and `subject` carries module
  attribution unauthenticated by the id — never substitute ids across
  invocation shapes, and pin request bytes (or re-derive the dossier) when
  module identity matters
  (`corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:244-250`;
  `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md:83-85`;
  `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`).
- Provider probes run under `prlimit` (e.g. wakaru `--as=1GiB`) — a standalone-
  working tool can still OOM in REA's spawn context. Bind native ELF binaries
  over node shims (`REA_WAKARU_COMMAND` → `@wakaru/cli-linux-x64/wakaru`).
- Positional-arg pattern extends: `recover-javascript-sources <file> <outdir>`
  (file not dir, output dir must be absent), `inspect-evm-interface <path>
  <encoding>`, `extract-artifact` ignores extra positionals silently.
- Ghidra startup timeout hits ~>40MB targets: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`.
- jq-shadow = verified upstream jq-1.8.2 (kimi-swarm install 2026-10-03) —
  do not re-flag.

## Refuses

Malware triage at scale, non-REA dynamic analysis (gdb scripting, strace,
Frida), source-repo reconstruction, all engine/tooling installs, and
safety/quality verdicts on findings (Adjacent — report to orchestrator, never
absorb; PROVINCE.md). Boundary: "what does this shipped artifact do, per
evidence id X" — never "is it safe or trustworthy".

## Local round-evidence gate registry

The rows below register the interactive-r1 recovery gate, citation-drift probe,
custody-pair tool, and quote-fidelity gate. None of them validates
REA correctness, outside review, canonical judgment, or fleet
acceptance. Evidence and limits: `corpus/lessons/2026-10-15-round-1-recovery.md`; `LOG.md`, Interactive round-1 recovery.

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate; `--admission` checks this recovery's unresolved prerequisites and returns 2, never native judgment | same command with `--selftest`; asserts isolated subprocess exit codes and stable finding IDs | `.ufo/rounds/interactive-r1/expected.json` pins every snapshot input and expected outcome; normal entry read-only in this repo; selftest creates and removes only its isolated fixture directory under `.ufo/rounds/interactive-r1/` |
| citation-drift | gate / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --table /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json --expected /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json --strict` (exercised argv: `.ufo/waves/round-16/verification.json` and `.ufo/waves/round-17/verification.json`; the same argv without `--strict` is the probe mode, an unexercised variant); **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate**; **frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, finding `pointer_table_tampered`) or an absent table (exit 2, finding `pointer_table_unreadable`) is could-not-evaluate before any entry is graded; a baseline that pins no digest is exit 2, finding `pointer_table_unpinned`; drift reporting is unchanged (rc 0)**; **round 18 (jj): an omitted `--rev` resolves `refs/heads/<--branch, default main>`, and a literal `--rev HEAD` is accepted only when HEAD equals that tip, else exit 2 `head_not_branch_tip` (`branch_missing` when the branch is absent); explicit revisions behave as before** | same command with `--selftest`; 15 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`; the twelfth is a tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is an absent table → exit 2, finding `pointer_table_unreadable`; round 18 adds a CLI-level detached off-branch HEAD pair: default → branch tip graded clean, `--rev HEAD` → exit 2 `head_not_branch_tip`), the original case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table **and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11). Registered `gate` from round 18 (R17-REGISTRY): the registered argv carries `--strict` and can exit 1 Round 19 (R18-HEAD-ALIASES): every HEAD-derived or mutable `--rev` (`@`, `@~N`, `HEAD~N`, `HEAD^…`, `HEAD@{…}`, `HEAD^{commit}`, reflog selectors, ORIG_HEAD/FETCH_HEAD and other pseudo-refs) exits 2 before resolution; the literal `HEAD` keeps its branch-tip comparison (selftest 33 cases). |
| custody-pair | tool / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py capture --out <receipt> [--label <L>]` (exercised argv retained in `.ufo/waves/round-17/verification.json`) — read-only sha256+stat over the five operator paths → a v2 receipt (SHA256; MTIME_EPOCH/NS with MTIME_UTC_RENDER and MTIME_LOCAL_RENDER labeled separately — the v1 local-under-`MTIME_UTC` defect gone; CTIME_EPOCH/NS; INODE; MODE/UID/GID; the receipt self-pins the instrument's sha256 and receipt-version 2) + a `.sha256` sidecar; a path that exists but cannot be evaluated is recorded with `READ-ERROR`/`STAT-ERROR`, never silently as absent; two cleanly-absent stanzas compare MATCH (ruling: only error-carrying stanzas are UNEVALUABLE); `paths` prints the canonical five; `verify <receipt_a> <receipt_b>` or `verify <receipt_a> --live` [`--require-paths <N>`] — **worst-finding map: 0 MATCH, 10 CONTENT-DRIFT (sha256 moved), 11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — a same-content rewrite), 12 METADATA-DRIFT (mode/uid/gid/size/type, extra path, inconsistent epoch/render, reproduced v1 LABEL-DEFECT), 13 ABSENT, 14 UNEVALUABLE (a path exists but could not be evaluated — EACCES on open or a stat error other than ENOENT; classified before the both-absent branch, so it can never read as a fail-open MATCH); 2 USAGE (bad args, unreadable or unparsable receipt, a reference below `--require-paths N` **distinct resolved paths** — printing `REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <canonical paths absent from the reference>` — a refused/failed write (receipt or derived sidecar aimed at a measured path, a custody path, the sidecar-shaped neighbour of a measured path, or an uncreatable receipt directory), unusable selftest scratch base); precedence CONTENT-DRIFT > UNEVALUABLE > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH; capture is 0 at 5/5, 14 when ≥1 path is present-but-unevaluable, else 13 with the receipt still written, and it refuses to write a receipt **or its derived `.sha256` sidecar** over any path it measures, a custody path, or the sidecar-shaped neighbour of a measured path (by resolved path or inode); v1 receipts still compare on their sha256 — a sums-form v1 reads MATCH-V1-PARTIAL exit 0, a v1 stanza reproducing the round-1 label defect reads METADATA-DRIFT/LABEL-DEFECT exit 12 with its sha256 contract intact (5/5); `--require-paths N` applies to v1 references too** | same command with `selftest`; 31 fixture cases (round 19; previously 28) — capture/receipt shape/sidecar self-hash, verify-vs-live clean, the two same-content-rewrite pins (in-place ctime, rename inode) → 11, content → 10, absent → 13, metadata → 12, TZ-independent UTC render, the three v1 parse shapes, unparsable → 2, refuse-to-write-over-custody-path → 2, unreadable-path → 14 (and a parsed unreadable receipt is never a fail-open MATCH), reference below `--require-paths` → 2, missing/unusable/`/tmp` `--scratch` → 2, `--paths X --out X`, `--out X --paths X.sha256`, `--out X.sha256 --paths X`, and a hardlink alias → 2; duplicate-stanza `--require-paths 5` → 2 and five distinct → 0; an uncreatable receipt dir → 2; both-cleanly-absent → 0; scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard); exit 3 if any case fails, 0 clean | the five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`); **normal entry writes nothing under the custody paths — files opened for reading only, never renamed, mtime never touched; the write guard covers `set(--paths) ∪ CUSTODY_PATHS` by resolved path and inode (a self-harm guard, not a security boundary); writes only the requested receipt + its `.sha256` sidecar (outside the custody set) and, under `selftest`, its isolated fixture root; `--paths` exists for fixture runs only** Round 19 (carried): `repo-root` records `git rev-parse --show-toplevel`, not the `--repo` argument (selftest 31 cases, subdirectory red case). |
| quote-fidelity | gate / kaidoku | `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-corrected.json`; 0 clean, 1 failed (quote absent/mislocated/too long), 2 could-not-evaluate (invalid input or source digest mismatch); `--frozen .ufo/waves/round-14/fixtures/expected.json` instead compares the frozen controls' exact exit/finding IDs, with mismatches 1 and tampered snapshots 2 | same script with `--selftest`; isolated fixtures assert exit and stable finding IDs | `.ufo/waves/round-14/fixtures/expected.json` pins every manifest and source excerpt; supplemental rendered/raw controls are pinned by `.ufo/waves/round-15/boundary-fixtures/expected.json` and run with the same script's `--frozen` flag. Frozen source-inventory coverage is required. Normal modes read only; selftest creates/removes its isolated fixture tree under `/var/tmp` or `QUOTE_FIDELITY_SELFTEST_DIR`. Raw UTF-8 substring and Markdown/single-line HTML heading consistency only: no upstream authenticity, full-document completeness, semantic support, or whole-registry verdict. Manual-only submissions are excluded by QUALITY #17, not detected by this tool; any machine verdict on such a claim is void. |

Study paths, scoped source tiers, opened-source anchors, recheck cadences, rejected leads and bounded searches are maintained in `corpus/SOURCES.md`; these references do not prove that a capability is held.

## Go RTTI bootstrap diagnosis — source-only addendum (round 14)

The held cross-version task and its source-backed diagnostic are different
claims. Use the table below before attributing a naming failure to a binary
layout change. Source anchors and limitations:
`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, S001/S003/S004/S007.

| Signal | Decision | Boundary |
|---|---|---|
| `Untested Go version` | Inspect bootstrap diagnostics separately | The inspected range branch logs and continues; it does not refuse analysis |
| `Missing Go bootstrap type info` | Check missing base JSON first; zero-applicable-architecture records are a hypothetical source alternative, not established for the measured bases with `all` | Failed struct registration with an invalid snapshot is not version-only or historical-layout proof |
| Upstream GP-6528 support change | Compare the whole source change with installed bytes | Range, snapshot, and downstream layout changes are not a demonstrated host repair |
| Build metadata readable but Ghidra names absent | Name the parser behind each observation | Built-in `inspect_go_binary` and provider RTTI recovery are separate routes |

The old op-pair's precise cause remains unknown because its analyzer log was
not retained. This addendum adds no held recovery operation and no new provider
execution. Source reading does not replace a carrier run.

## Installed Go snapshot selection — round 15

The source law in round 14 does not pin the installed data. Before a new
Go recovery diagnosis, retain the read-only inventory and the fallback warning:
`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` (S003/S007/S023).
Do not infer actual data bytes from the requested-version label.

| Signal | Decision | Limit |
|---|---|---|
| Present base but requested patch diff absent | Inspect the closest earlier diff or base fallback and retain its actual filename/digest | The snapshot object still carries the requested version; its label is not exact-byte identity |
| Missing platform-specific key | Check the generic `all` bucket before inferring empty applicability | The measured base resources retain `all`; hypothetical zero-applicable-key source behavior is not an observed installed failure |
| JSON base absent for requested major/minor | Source lookup returns EMPTY before searching patch diffs | This is installed-data/source evidence, not a historical target-cause finding or a repair demonstration |

| Name | Kind / owner | Entry / status map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| go-snapshot-inventory | probe / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`; read-only JSON inventory, not a conformance verdict; 0 emitted, nonzero could-not-evaluate | no selftest or gate claim | `.ufo/waves/round-15/inventory.json` retains filename/size/SHA-256 and selected JSON structure; read-only installed resources, stdout only; rerun and compare bytes manually; exact recorded argv correction: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`, Round-16 correction |

## Computable Go selection preview — round 16

`corpus/knowledge/2026-10-20-r16-go-selection-preview.md` (S003/S023)
materializes the existing selector law; it does not discover a new recovery
mechanism. Use it to distinguish a request-bounded exact/lower diff from
the highest installed patch. Preserve requested input, selected patch and
raw file digests separately.

| Signal | Decision | Limit |
|---|---|---|
| Requested 1.24.5 with patch 6 installed | Select exact patch 5, never the highest installed patch above the request | Source model only; no computed patched result |
| `base_only`, requested patch nonzero | Selected patch 0 identifies base bytes; original requested input remains separate | Not equivalent to missing base, nor exact requested patch data |
| `base_matching_buckets` with a selected diff | Read as an ordered unpatched-base projection | Bucket values, patched content and successful registration remain unverified |
| Non-Unix GOOS | Emit effective read order with the Java empty placeholder omitted | Generic `all` can survive; no platform-support guarantee |

| Name | Kind / owner | Entry / status map | Fixture check | Pinned values / write scope |
|---|---|---|---|---|
| go-selection-preview | probe / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --request 1.24.7 --goos linux --goarch amd64`; repeat with `--request 1.24.5` for the bounded contrast; 0 emitted, 2 could-not-evaluate; never a conformance verdict | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selfcheck.py --fixtures /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection-fixtures.json --fixtures /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/negative-fixtures.json`; developer fixtures, not a domain gate; supplementary w2 case files are passed explicitly in the retained full argv | `.ufo/waves/round-16/selection-fixtures.json`, `negative-fixtures.json` and `w2/*-cases.json` hand-author source-boundary expectations; execution results and exact inputs retained in `verification.json`; probe reads one supplied root and writes stdout only |
| round16-structural-controls | probe / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/controls.py <BEFORE> <AFTER>`; 0 reported, 2 could-not-evaluate; argv and resolved immutable revisions retained | no selftest/gate claim | Byte equality, old-prefix retention, source-cell deltas and bounded craft citation ranges only; read-only Git objects, stdout only; cannot establish semantic correctness or outside admission |

## Retained Go carrier diagnostics — round 17

`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (S003/S023/S024/
S025/S026/S029/S031/S032) runs real, pinned Go carriers through REA 6.5.0
`analyze` with the Ghidra analyzer log retained and bound to the run. It
compares each log against a route predicted from installed source and frozen
in Git before the measured runs. Scope: Ghidra 12.1.4, x86-64 Linux ELF, two
passes per carrier. 8/8 routes matched in both passes. Of the six prospective
carriers, three were on routes unseen at freeze (1.25.x fallback, no build
info) and three repeated pilot-seen routes. Use it before attributing Go
symbol loss to a layout change.

| Signal in a bound `ghidra.log` | Decision | Limit |
|---|---|---|
| `GoApiSnapshot` INFO `Using Go API snapshot for X` | Base found; selected patch = X's patch, where X is the normalized version (rc/beta and `X:` suffixes dropped) | No file path, digest, or patched-content proof |
| `GoApiSnapshot` WARN `Falling back from X to Y` | Lower patch data used; the next `GoRttiMapper` line still says `X` | Requested-label echo: never cite the mapper line as selection. Round 17 observed only fallback to the base (Y = M.m.0); round 18 observed an intermediate patch fallback (1.24.13 → 1.24.6, `.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:68`) |
| `Untested Go version [X]`, no snapshot line, `Missing Go bootstrap type info` (≥1; ×2 when no DWARF loads) | No installed base for X's minor (here 1.26.x/1.27.x) | Range check only logs; layout change neither shown nor excluded |
| `Invalid Go version string [S]` | Build-info version found but unparseable | Source-only on this host |
| Only `Reading Go binary info` + `unable to get GoRttiMapper` | No build-info record (check `inspect-go-binary` `build_info: null`, `go version -m`) | Not "not Go": on ELF the golang cspec comes from section names |
| Bootstrap OK, then `GolangSymbolAnalyzer` `Go analysis failure …` | Symbol markup aborted after bootstrap (aether 1.25.14; strings still recovered) | Round 18: replayed and confirmed on held-out carriers (section "Swiss-map misread replay — round 18" below): Swiss named map types read with the `OldMapType` layout from the snapshot (S033 supersedes the S032 lead), not the patch fallback |

Before running a carrier, give REA a private `TMPDIR` and an allowlisted
environment. Bind the session from whole log records: `Using log file:`, the
`IMPORTING: …target-<sha[:12]>.bin` line, and the loader's full
`?MD5=<carrier md5>`. Never copy `session.json` (it holds the bridge token).

| Name | Kind / owner | Entry / status map | Fixture check | Pinned values / write scope |
|---|---|---|---|---|
| go-carrier-run | probe / kaidoku | `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/run-carriers.sh <LABEL>`; per label in `predictions/carriers.tsv`: `tools/carrier-run.py` (exit 0 one bound session and pins equal at every recorded instant, 1 pre/post or mid-run pin drift, 2 analyze failure/timeout/unbound/leftover session parent/could-not-evaluate), then `log-extract.py` and `compare.py` (0 match, 1 mismatch, 2 invalid). The script exits nonzero if any of these is nonzero; `RUNS_DIR=/tmp/<dir>` makes a non-destructive recheck (the default `runs/<LABEL>` is replaced) | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/carrier-run.py --selftest` (fake REA child, deleted session dir) | Carrier, r16 `selection.py`, frozen prediction and all 143 installed Go data files pinned pre, every 30 s (retained) and post; allowlisted child env with private `/tmp/kr17-rea-*` `TMPDIR`; writes only `runs/<LABEL>/`; never executes the carrier. Exercised argv for every label is in `runs/run-log.txt`; the registry form is retained in `.ufo/waves/round-17/verification.json` |
| go-log-extract | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/log-extract.py --log <GHIDRA_LOG>`; 0 emitted, 2 unreadable; route read from the `GoApiSnapshot` component only | same command with `--selftest` | Read-only; stdout only |
| go-route-predict | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/predict.py --go-version <GO_VERSION> --golang-root <GOLANG_DIR>`; 0 emitted, 2 unparseable/empty version (no guess) | same command with `--selftest` | Imports r16 `selection.py`; read-only; stdout only |
| go-route-compare | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/compare.py --prediction <PREDICTION> --observation <OBSERVATION>`; 0 all fields match, 1 any mismatch, 2 invalid input (including a predicted route with no observed route fields) | same command with `--selftest` | Pinned values: the frozen prediction it is given (round 17: `.ufo/waves/round-17/predictions/`, manifest `.ufo/waves/round-17/predictions/SHA256SUMS`; round 18: `.ufo/waves/round-18/predictions/`); `snapshot_label` is marked non-discriminating; route fields and a hand prediction's `extra_expectations` (`language_compiler`, `invalid_version_strings`, `bootstrap_attempts_at_least`, `analyzer_errors_contain`, and from round 18 `analyzer_errors_empty`, `eof_reads`, `invalid_index_reads`) are compared when present. Write scope: none in normal mode, result JSON on stdout only; `--selftest` writes only a removed mkdtemp tree |
| receipt-validate | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py <RECEIPT>`; 0 valid, 1 digest/pin/binding/mid-run-drift/mid-map finding, 2 unreadable, no arguments, or sibling `pins.py` missing; from round 18 the same command with `--require-mid-maps` before `<RECEIPT>` is the round-18 receipt form | same command with `--selftest` (tampered file, foreign log, MD5 collision, stack-trace needles, mid-run drift, and from round 18 tampered/forged mid map, verdict-only entry under `--require-mid-maps`, forged `entries` count red cases) | Pinned values: the digests recorded in the receipt itself; no external expected file. Recomputes recorded file digests and the log binding; from round 18 re-hashes each retained mid-run map (`map_path`/`map_sha256`) and recomputes its verdict against the pre map, and `--require-mid-maps` (round-18 receipts) rejects a verdict-only check. A verdict-only r17 check is accepted, not verified (QUALITY #21). It does not check the REA version in the argv, nor the receipt's self-reported `md5_pre`/`binding.*` fields (w2 `ReaPinStill.md`, `Runcalibaether.md`). Write scope: none, read-only over the receipt's recorded absolute paths (not relocatable: a historical receipt is checked only via a prefix-remapped copy, as in `.ufo/waves/round-18/evidence/validate16/summary.json`); JSON on stdout; `--selftest` writes only a removed mkdtemp tree. Consistency of the bytes present now: not authenticity against a forger who rewrites and rehashes, and not during-run integrity between the recorded instants Round 19 (R18-MIDMAP-LISTSTEP): for a list-shaped `steps`, only the entry that identifies itself as `analyze` (`step`/`name` field or the `analyze` argv token) satisfies `--require-mid-maps`; checks on any other step raise `mid_checks_absent`. |
| receipt-validate-v2 | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate-v2.py <RECEIPT>...`; 0 all valid, 1 any digest/pin/binding/mid-map finding (including `analyze_step_unauthenticated`), 2 unreadable/usage; from round 20 pass `--require-mid-maps` for the receipt form | same command with `--selftest` (32 cases incl. `argv_second_package_decoy`, `argv_non_npx_decoy`, `argv_latest_refused`) | Pinned values: the digests recorded inside each receipt; the old `.ufo/waves/round-17/tools/receipt-validate.py` bytes are **frozen unchanged** (sha256 `a31c7db8…be22c`) because the C3 run receipts pin them; this successor is the round-20 D6d fix (npx + package + analyze only). Write scope: none |
| pins | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/pins.py compare <PRE> <POST>`; 0 equal, 1 differ (names paths), 2 unreadable or invalid snapshot; `snapshot --out <FILE> <PATH>` writes one map | same command with `--selftest` (mutated-file red case) | Pinned values: probe; no persisted baseline — no expected digests; each entry records sha256, size and mtime_ns at the instant read. A run's retained map (example `.ufo/waves/round-18/runs/calib-aether/pins/mid-1.json`) is evidence, not an expected baseline (R18-REGISTRY-PINNED, round 19). Identical bytes at two instants only, never continuity. Write scope: `snapshot --out FILE` writes `FILE.tmp` then replaces FILE (no no-clobber check); `compare` writes nothing; `--selftest` writes only a removed mkdtemp tree. Kind corrected from `tool` to `probe` in round 18 |
| temporal-sweep | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/temporal-sweep.py --root <LANE> --rev <REV> --sites-rev <BASELINE>`; 0 reported, 2 could-not-evaluate | same command with `--selftest` | Git objects only; a site is corrected only by one line with `R16-PROVENANCE`, its exact `file:line` and "temporal stability not evidenced" |
| invocation-audit | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/invocation-audit.py --root <LANE> --rev <REV>`; 0 reported, 2 could-not-evaluate | same command with `--selftest` | Git objects only; counts an `argv` (never `orig_argv`) only when its recorded exit is 0/1 or absent; strips only a leading `python*` token and relativizes in-lane absolute paths (so results depend on the checkout path), keeping `-I`/`-B`/`--strict` differences as variants |
| go-buildinfo-probe | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py <PATH>`; 0 emitted (`found:false` when no magic), 2 unreadable or malformed ELF | same command with `--selftest` | Pinned values: `.ufo/waves/round-17/tools/buildinfo-probe.py` itself (the build-info magic and header constants of go1.25.0 `debug/buildinfo` are literals in that file, no external baseline; R18-REGISTRY-PINNED, round 19) (keeps the writable-segment fallback that go1.27.3 removed, S024); cross-check with `go version -m`. Write scope: none, one read of the target, JSON on stdout, never executes it; `--selftest` writes only a removed mkdtemp fixture tree |
| round17-structural-controls | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/controls.py <BEFORE> <AFTER>`; 0 reported, 2 could-not-evaluate | same command with `--selftest` | Git objects only; old-prefix, frozen-blob, verifier and QUALITY-row byte checks; no semantic audit |

## Swiss-map misread replay — round 18

`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` (S034/S035/S023/S003/S033).
Ghidra 12.1.4 binds Go 1.24/1.25 map descriptors to `OldMapType` (88 B)
while Swiss binaries carry `SwissMapType` (112 B), so a named map's
`UncommonType.PkgPath` is read from the true `SlotSize`. Predictions from
bytes plus installed source, frozen before the run, matched 15/15 labels;
both held-out diagnostic carriers failed with their exact predicted index.

| Signal in a bound `ghidra.log` | Decision | Limit |
|---|---|---|
| Swiss Go 1.24/1.25 carrier, bootstrap OK, `Go analysis failure` + `Invalid index: N` or `Unable to read past EOF: A, B` | Run `swiss-misread.py` on the carrier; an exact H1 match attributes the abort to the `OldMapType` binding | 3 carriers observed (aether calibrated; s1246-swiss-nethttp and kimi-webbridge held out); Ghidra 12.1.4, x86-64 ELF |
| Same signal on a `X:noswissmap` carrier | Not this mechanism | 0/6 noswiss carriers failed |
| Swiss carrier, no failure | Never read as "map types laid out correctly": the misread is silent unless the name at `types+SlotSize` has a pkgPath, and `Mcount` reads 0 (methods dropped) | Silent case is INFERENCE; no program export run |

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| r18-prediction-freeze | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/gen-predictions.py`; 0 written, nonzero when any tool fails or an H1 outcome is `unknown` (labels already processed stay written, `SHA256SUMS` is written last, so a failed run leaves uncovered files) | no selftest; its inputs' tools carry selftests | Pinned values: writes `.ufo/waves/round-18/predictions/*.prediction.json`, `decision-rule.json`, `swiss-misread/*.json` and `SHA256SUMS`, committed before any run (`eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`). Write scope: that directory only; never runs REA or a carrier. Ran once before the freeze; its argv is in this row and the commit, not in a retained receipt (an unexercised variant for `invocation-audit`) |

## Revision pins under jj — round 18

The lane is a colocated jj workspace (jj 0.45.1). jj usually leaves Git HEAD
detached (S036, `git-compatibility.md:114-116`), and after an unbookmarked jj
commit HEAD can name a commit that is not on `main` while `git show HEAD:<path>`
still succeeds (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` F2).
Lane tools therefore pin `refs/heads/main`, never bare `HEAD`.

| Signal | Decision | Limit |
|---|---|---|
| HEAD equals `refs/heads/main` (detached at the tip: the lane's normal state after a helper commit) | Use the branch tip; record `head_equals_source: true` | Holds only until the next jj mutation |
| HEAD is not the branch tip | Refuse with `head_not_branch_tip`, exit 2, before any gate runs | `git show HEAD:<path>` would still succeed, so the failure is silent without this check |
| Tip not contained in `refs/remotes/origin/main` | Refuse "landed" records (`branch_not_pushed`; revpin tests ancestry, round-17 `verify.py` tests equality); cite only the helper's `landed <hash>` | `origin/main` is last fetched/pushed state, not live remote state. Round 19 fixes the prior HEAD-alias limitation: mutable aliases are lexically refused by citation-drift, not merely tested for branch equality |

Evidence: `.ufo/waves/round-18/evidence/jj-red-before.json` (a throwaway jj clone
with an off-branch commit: baseline forms red, fixed forms green).

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| routed-defects | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py --root <LANE> --rev <REV> --strict`; 0 all six R17 routed defects closed, 1 any open (named correction or substance), 2 could-not-evaluate; without `--strict` 0 reported | same command with `--selftest` (open fixture, closed fixture, one-broken-check and token-only red cases) | Pinned values: the defect definitions in the script, the r17 producer hashes and `2711674`/`da64646` reference revisions. Write scope: none, Git objects at REV only, JSON on stdout; `--selftest` writes only removed mkdtemp repos Round 19 (R18-VALIDATOR-DIGEST): `validator-sha256-pinned` now recomputes the sha256 of `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py` and refuses any other digest (selftest 19 cases). |
| head-rev-lint | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/head-rev-lint.py --root <LANE> --rev <REV> --strict`; 0 no live HEAD-as-revision site, 1 live site, 2 could-not-evaluate | same command with `--selftest` | Pinned values: the scanned scope (`.ufo/gates/`, `.ufo/rounds/`, `.ufo/waves/round-14`…`round-18`, seat dirs `w[0-9]/` listed as excluded) and the site kinds in the script; `head-rev-lint: compare-only`/`red-before` comments mark annotated sites, listed with reasons. Write scope: none, Git objects at REV, JSON on stdout. Syntactic: dynamic revision flow is a listed blind spot Round 19 (R18-HEAD-ALIASES): registered limit — nested compare-only HEAD reads behind wrappers (`.ufo/waves/round-17/verify.py:83`, `.ufo/waves/round-18/tools/revpin.py:113`) are invisible to the lint; neither selects a run revision. A wave-1 attempt to add a `nested` class failed its own selftest and was not taken (`.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch`). |
| revpin | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/revpin.py --root <LANE>`; 0 tip resolved (HEAD equals tip, tip an ancestor of `refs/remotes/origin/main`), 2 finding `branch_missing`/`head_not_branch_tip`/`branch_not_pushed` (also usage errors) | same command with `--selftest` | Pinned values: none. Write scope: none, read-only git, JSON on stdout; module `resolve_source` used by `.ufo/waves/round-18/verify.py`. No dirty-worktree check |
| jj-red-before | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/jj-red-before.py --out <RECEIPT>`; 0 every red/green expectation held, 1 any not held, 2 setup failure | same command with `--selftest` | Pinned values: baseline `9011581d84527ba34c675f9cf912e54d2e72d470` (baseline tool bytes via `git show`). Write scope: the receipt and a removed `/tmp` sandbox clone (origin remote removed, HOME/XDG isolated). Limits (round-18 w2 `JjSandboxSafety.md`): run only as `python3 -I -B` with no `GIT_*` in the environment (the selftest fixture builder does not scrub it), and a pointer-table entry naming a path outside the sandbox would be written (none of the 60 entries does); the receipt records no digest of the tools it ran Round 19 (carried): every git/jj subprocess runs with an explicit environment scrubbed of GIT_*/JJ_* variables, and pointer-table paths outside the mkdtemp clone are refused with exit 2 (selftest 9 cases). |
| swiss-misread | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/swiss-misread.py --carrier <PATH> --golang-root <GOLANG_DIR>` where `<GOLANG_DIR>` is `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`; 0 emitted, 2 unparseable | same command with `--selftest` | Pinned values: none external; predictions it emitted for round 18 are frozen under `.ufo/waves/round-18/predictions/` (`swiss-misread/<label>.json` hold the `predicted_*_h1/h0` keys). Write scope: none, reads the carrier and installed snapshot JSON, JSON on stdout, never executes the carrier. amd64 only; the `walk` channel has false positives (unmasked variadic bit, notesmd-cli, kimi-webbridge) and its gap scan misses `*struct {…}` names (w2 `EmulatorIndependence.md`, `Runs1246noswissnethttp.md`); predictions rest on the per-map channel |
| go-carrier-run-r18 | probe / kaidoku | `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/run-carriers.sh <LABEL>`; per label in `.ufo/waves/round-18/predictions/carriers.tsv` the round-17 `carrier-run.py`, `log-extract.py`, `compare.py`; 1 if any run or compare is nonzero, 2 if `carriers.tsv` is unusable | same command with `--selftest` (stub tools, forced-red proof) | Pinned values: carrier sha256 (synthetic `.ufo/waves/round-18/carriers/SHA256SUMS`, read from its deployed copy, else the TSV's 4th column), prediction, tools, Go data; `producer.json` per run records branch tip and tool digests. Write scope: deletes and recreates `.ufo/waves/round-18/runs/<LABEL>/` (or a `/tmp` `RUNS_DIR`); never executes a carrier. The all-label pass was run once without `<LABEL>` (argv in `runs/run-log.txt`, not in a retained receipt: an unexercised variant for `invocation-audit`) |
| round18-measure | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/measure.py <REV>`; 0 report emitted (claims may be could-not-evaluate), 2 revision unreadable | same command with `--selftest` | Pinned values: none. Write scope: none in the lane; materializes REV's tools into a removed mkdtemp; Git objects only |
| round18-structural-controls | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/controls.py <BEFORE> <AFTER>`; 0 reported, 2 could-not-evaluate | same command with `--selftest` | Pinned values: the six contracted in-place r17 edits and the one restored SHA256SUMS line as the only permitted wave-evidence deltas. Write scope: none, Git objects only; no semantic audit |
| routed-r18 | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py --root <LANE> --rev <REV> --strict`; 0 no open routed R18 defect, 1 open defects, 2 unusable input or HEAD-derived `--rev` | same command with `--selftest` (token-only fixture keeps all 7 open) | Pinned values: the seven defect ids, the round-18 baseline `9011581` and delivered revision `a245bb0`, the go.dev archive sha256 values for go1.24.6/go1.25.0, and the alias list, all literals in the script. Write scope: none in the lane; REV tools are extracted to a removed mkdtemp; substance checks run code from REV, not tokens |
| province-pins | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --root <LANE> --rev <REV> --strict`; 0 stated pins equal live, 1 mismatch or unstated client, 2 unreadable | same command with `--selftest` | Pinned values: probe; no persisted baseline — the live side is the three client config files read at run time (only the pin token, sha256 and mtime are printed). Write scope: none. Time-dependent: a later operator config edit changes the result without a lane change |
| rea-catalog | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/rea-catalog.py` (see its `--help`); recomputes CLI command count, MCP tool count and catalog tools_sha256 from the installed npx caches | same command with `--selftest` | Pinned values: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/rea-catalog.json` (round-19 values). Write scope: stdout or `--out` only |
| wave-outcomes | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/wave-outcomes.py --registration <wave-registration.json> --report-dir <dir> --causes <causes.json> --out <json>`; 0 every seat has a report or a recorded cause, 1 a seat without a report lacks a cause, 2 unusable input | same command with `--selftest` | Pinned values: probe; no persisted baseline. Write scope: `--out` only (forward fix for R18-DEADSEAT-RECORD) |
| go-carrier-run-r19 | probe / kaidoku | `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/run-carriers.sh [LABEL]` (REA CLI version pinned by `REA_VERSION` in the script; per-step timeout `TIMEOUT_S`); 0 every run and compare exited 0, 1 any failed, 2 unusable carriers.tsv, unsafe label or unmatched selector | same command with `--selftest` (stubs only, never REA) | Pinned values: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/predictions/carriers.tsv` (frozen sha256 per carrier) ; `predictions/SHA256SUMS` is an offline freeze manifest, not a runtime runner input (checked by controls-r19). Write scope: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/<label>/` or `RUNS_DIR` under /tmp; never executes a carrier |
| round19-measure | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/measure.py <REV>`; JSON with c1/c2/c3 fields | same command with `--selftest` | Pinned values: probe; no persisted baseline. Write scope: none, Git objects at REV extracted to a removed mkdtemp |
| round19-verify | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/verify.py <BASELINE_REV>`; 0 every command exited as expected, 1 unexpected exits | same command with `--selftest` | Pinned values: the expected-exit table in the script. Write scope: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/verification.json` and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/verify/` |
| round19-controls | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/controls-r19.py <BEFORE> <AFTER>`; 0 controls hold, 1 failed, 2 unreadable input | same command with `--selftest` | Pinned values: SCORECARD command A, old prefix/QUALITY rules in the script, and prediction freeze `a1140e76fffdc1be032d9d813dbb686157803bbc`. Write scope: none, immutable Git objects only; not a semantic audit |
| round19-postfix-mutations | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/postfix-mutations.py <SOURCE_COMMIT>`; 0 report emitted, not an all-killed verdict | no separate selftest; the invocation itself is a finite set of committed sandbox mutants with actual pristine/mutated/restored exits | Pinned values: ten named transformations in the producer and the cited source commit. Write scope: one removed /tmp clone, never the lane Git index or jj state. Trusted lane code only; not an OS sandbox |
| routed-r19 (historical R20 aggregate) | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/routed-r19.py --root <LANE> --rev <REV> --strict [--live]`; 0 closed, 1 open, 2 could-not-evaluate | `--selftest` | Historical measurements only; its D6d positive control reads a C3 receipt. For current R20-SEP validation use `round21-isolated-control` below, not this aggregate. Frozen R20 source/measurements remain unchanged. |
| evidence-timestamps | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py --root <LANE> --rev <REV> --path <dir> --strict`; 0 no zoned timestamp later than its line's introducing committer time, 1 `future_dated <path>:<line>` findings, 2 could-not-evaluate | `--selftest` (5 cases) | Pinned values: the zoned-timestamp grammar in the script (T/space forms with Z or `±HH[:]MM`; zoneless forms unchecked). Text blobs of every size are scanned; binary blobs are reported as `files_skipped` and require a named review. Write scope: none, `git blame --porcelain` at REV |
| carrier-guard | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/carrier-guard.py {arm,check,disarm} --manifest <TSV> --record <DIR>`; `carrier-guard.py adopt --from <MANUAL-ARM.json> --record <DIR>`; check 0 clean, 1 `mode_restored`/`ctime_changed`/`content_changed`, 2 refusal | `--selftest` (`exec_refused`, `mode_restored`, …; copies of /usr/bin/true in mkdtemp) | Pinned values: `arm.json` per record dir (`.ufo/waves/round-20/evidence/carrier-guard*/`). Write scope: carrier mode bits (arm/disarm) and the record dir. Limits: QUALITY #24 (direct execve only; loader-mapped execution, copy+exec, memfd, same-owner chmod are named bypasses; bwrap 0.13.1 exists on the host but is not used) |
| final-census | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/final-census.py --root <LANE> --out-dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/verify`; runs `c1-census-v10.py --root <LANE>` and `sources-census.sh validate --root <FLEET> kaidoku`, records their combined stdout at the branch tip plus rev/argv/exit/stdout sha256 in `verify/final-census.json`; 0 both children clean, 1 any child finding, 2 refusal (dirty tracked files, non-worktree root, out dir outside root) | same command with `--selftest` (3 cases) | Pinned values: none — a recording probe over the two child gates' own verdicts, not a comparison with a stored baseline. Write scope: the out dir only; must be the last lane write of the round |
| revexec | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/revexec.py run --root <LANE> --rev <REV> --entry <path> -- ARGS`; child exit propagated, 2 refusal | `--selftest` (`write_outside_refused`, `net_refused`, `runs_ok`) | Pinned values: systemd-run properties in the script (`PrivateNetwork=yes`, `ProtectSystem=strict`, `ProtectHome=read-only`, work dir rw). Not a security boundary: same uid, AF_UNIX sockets reachable |
| verb-coverage | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py --root <LANE> --rev <REV>`; 0 measurement, 2 unevaluable. Direct binding: `--evidence <JSON> --verb <VERB> --evidence-id <ID>`; 0 `evidence_bound` clean, 1 `evidence_unbound`/`evidence_refused` failed, 2 `evidence_unevaluable` | `--selftest` actual self-invocations | Pinned values: `.ufo/waves/round-21/fixture-contract.json`, `fixtures/battery.json`; retained R20 catalog. Write scope: removed external selftest fixtures only. Cites exact id+operation in one supported record, rejects typed refusals and duplicate JSON members. Unsupported TOON is not guessed; pathless objdump remains `subject:null`. No cryptographic authentication. R20 predecessor retained only for historical remeasurement and Git/mention helpers. |
| swiss-misread-v2 | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/swiss-misread-v2.py --carrier <PATH> --label <L>`; 0 result, 2 carrier unevaluable | `--selftest` (17 cases incl. `variadic_masked`, `first_failure_shape`) | Pinned values: Ghidra 12.1.4 Go snapshot data; frozen outputs `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/`. Write scope: none |
| first-failure-extract | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py <ghidra.log>`; prints `{log_path,last_line,first_failure{kind,index,va,phase}}`; 0 extracted, 2 unreadable; absence is reported as null, bounded to the retained log end | `--selftest` (4 cases) | Pinned values: none | Write scope: none |
| compare-first-failure | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction <FROZEN-JSON> --log <RETAINED-LOG> --extractor /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py`; 0 `failure_match` clean, 1 `failure_mismatch` failed, 2 `comparison_unevaluable` | `--selftest` actual self-invocations | Pinned values: `.ufo/waves/round-21/fixture-contract.json`, `fixtures/battery.json`; R20 nineteen predictions remain at freeze `808cbb31a1e24656da5ba4967497e602fbca7415`, with digests in predictions/SHA256SUMS. Caller owns extractor code and input identity, not sandboxed. Explicit bounded envelope required; kind+index equality ignores typed va/phase. Null means bounded silence, not analysis success. Write scope: removed external selftest fixtures only. Historical R20 comparator remains for old revision measurements. |
| round20-measure | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/measure.py <REV> [--freeze <F>]`; JSON with c1/c2/c3 fields; 0 measured, 2 unusable input | same command with `--selftest` | Pinned values: probe; no persisted baseline — C3 pins the freeze blobs at `F` and reports the field counts. Write scope: none; Git objects at REV extracted to a removed mkdtemp |
| round20-controls | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/controls-r20.py <BASE> <SOURCE>`; 0 all controls hold, 1 any control failed, 2 unreadable input | same command with `--selftest` | Pinned values: the command-A map rule, old-prefix/QUALITY rules in the script, and the C3 freeze `808cbb31a1e24656da5ba4967497e602fbca7415`. Write scope: none, immutable Git objects only; not a semantic audit |
| round20-verify | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/verify.py <SOURCE_REV>`; 0 every expected command exit matched, 1 any unexpected exit, 2 unusable input | same command with `--selftest` (or `--dry-run <REV>`) | Pinned values: the expected-exit table in the script. Write scope: `.ufo/waves/round-20/verification.json` and `.ufo/waves/round-20/verify/`; scratch in mkdtemp outside the lane |
| round21-battery | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C1` (or C2/all; `--regression` is C2/all only); 0 all expected exits, 1 violation, 2 unusable/`snapshot_tampered` | Finite independent test producer, not a new admission gate; no separate selftest | Pinned inputs: `.ufo/waves/round-21/fixture-contract.json`, `fixtures/battery.json`, digest manifest `fixtures/expected.json`. Canonical bytes come from contract freeze `53166ab0aae495c964d956050ca0ca3a4f29014a` and fixture freeze `d93c85887d9ae77d224c82c8f56bc8cca86d1a75`; manifest keys/digests and local inputs must agree. Revision tools extracted to removed external dirs. Baseline C1 uses an external committed inert fixture repo, never lane Git writes; C1/C2 load separately. Nineteen-log regression is retrospective, not new forecasting or authentication. |
| round21-isolated-control | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/isolated-control.py --root <LANE>`; 0 `isolated_control_clean`, 1 failed, 2 unevaluable/`snapshot_tampered` | same command with `--selftest` self-invocation checks exit and finding | Pinned independent template/expected exits: `.ufo/waves/round-21/fixtures/isolated-receipt-v2.json`, freeze `ae73ec7734c8edc70350995267ddc1f0d2f603e4`, SHA-256 constant in script. V1 is retained only as the failed missing-metadata fixture. Validator authority is `.ufo/waves/round-17/tools/receipt-validate-v2.py` plus sibling pins.py; both digests printed. No validator builder/import. Write scope: removed external fixture dir. No C3 inputs or recorded fixture argv execution; current R20-SEP authority (QUALITY28). |
| round21-controls | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/controls.py --root <LANE> --before <B> --after <V>`; 0 `controls_clean`, 1 `controls_failed`, 2 `controls_unevaluable` | `--selftest` actual self-invocations over removed external Git fixtures, positive plus prior-byte mutation | Pinned rules: SCORECARD command A, immutable prior R20/knowledge/lesson blobs, LOG/SCORECARD prefixes and prior QUALITY admission rows. Write scope: no lane write, removed external selftest repo only. Structural no-harm controls, not a semantic or security audit. |
| round21-verify | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/verify.py --root <LANE> --before <B> --after <V> --out-dir <NEW-ROUND-RECORD-DIR>`; 0 expected command exits, 1 discrepancy | Explicit final-suite producer; expected command table committed in script | Writes new records under round21 plus removed external fixtures; use `verify/final/` for the post-wave corrections, preserving initial `verify/*.json`. Retains argv/stdout/stderr/exit, measured revision and producer digest. Executes metadata validators/census only, never REA producers/carriers. Unrun checks do not count. |

## Toolchain holdout and partial forecasts — round 19

`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` (S038 provenance;
S035/S023/S003 mechanism). Previously unrun official Go 1.25.0 toolchain ELFs
extend the artifact holdout, not version coverage. Vet's bound log reports
Invalid index 13902080, one of the **frozen H1-only** indexes; seven controls
lack the exact Go-analysis-failure signature. The frozen membership rule confirms;
the extractor-scoped compare is **7/8**, not a clean analyzer sweep: compile
has a separate deferred RTTI NPE the extractor omits, and vet's multi-index
forecast cannot match an analyzer that stops at the first IOException.

| Signal / forecast | Decision | Evidence boundary |
|---|---|---|
| Frozen H1/H0 kinds share an index candidate | Freeze a discriminating value set, but qualify model defects discovered later | Vet H1-only `{13902080,852107777}` is genuine; shared walk candidate `1801722468838924630` is an unmasked-variadic-bit emulator bug, not a Ghidra H0 read |
| First IOException aborts the analyzer | Freeze a first-failure forecast, not a full set of unreachable candidate failures | Round-19 full-list forecast is rejected; never repair its frozen bytes after outcome observation |
| Producer validator changes after a run | Preserve the old pass and replay with the final producer bytes if current live binding is required | Round-19 final evidence is `runs/pass2/`; first-pass receipts retain their correctly red old-file pin |

The emulator's `diagnostic` kind comparison includes a whole-walk candidate
that its map-path boolean excludes (`w1/H0H1Semantics.md`). This is a known
field-semantics limit; map-path booleans selected round-19 D before the run.

## Record-bound evidence and bounded silence — round 21

Use QUALITY #26–28 (`corpus/lessons/round-21.md`; S049/S050 ground #26). The current
registered successors above replace token co-occurrence and permissive naked
null comparison for new work; retained R20 source and measurements are history.

| Input | Decision |
|---|---|
| Exact cited id and operation in one supported JSON record, no typed refusal | Bound local witness; not cryptographic authentication |
| Id and operation in unrelated records or prose; typed error/refusal | Reject as unbound/refused; do not count held |
| Ambiguous duplicate JSON member, malformed JSON or unsupported representation | Could-not-evaluate; do not guess from tokens |
| Explicit first_failure:null plus integer last_line ≥0 | Bounded absence only through last_line, never successful analysis |
| Naked null/failure or missing/malformed envelope fields | Could-not-evaluate, not silence |
| Valid observation and prediction differ in kind/index or only one is null | Mismatch; phase/va remain recorded but are not equality axes |

Checklist: pin the producing revision and fixture digest; retain actual exit,
stdout/stderr and finding id; run positive controls alongside negatives; test C1
and C2 separately. R20's nineteen exact-artifact log pairs are retrospective
regression only; no new provider execution or forecast is implied.

## Static Flutter and calibrated catalog dispositions — round 22

For the first static Flutter boundary see
`corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` (S051–S053).
A parsed `flutter_detected:false` is a scoped negative, not a refusal and
not absence of every native library. Read `normalized_result.coverage`,
retain the target SHA-256 and exact id/operation, and keep any extracted
Evidence record alongside its untouched CLI envelope. No static identity
record establishes source recovery or execution.

Before interpreting a provider refusal, inspect the producing argv and
environment: an explicit false-client ADB control says nothing about the
real client's devices. Frida enumeration can work while an impossible-PID
instrumentation request fails; never turn that failure into provider
absence. `PROVINCE.md` Round-22 dispositions retain these distinctions.
The kaidoku/revenger dynamic-analysis boundary remains an open L0 question.

### Round-22 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round22-C1 | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev <REV>`; 0 c1_complete/all six, 1 c1_incomplete, 2 unevaluable. Frozen claim improvement is k>=1, not an all-six pass | `--selftest` (optional `--root <LANE>` for a relocated executable): 0 counter_controls_clean, 1 counter_controls_failed, 2 snapshot_tampered/unevaluable | Fixed T1/claim in claims.json; original counters and v1 fixture retained in frozen/. Active independent inputs: frozen/expected-v2.json (manifest SHA constant in script), fixture program and dependency hashes; reviewed helper hashes in frozen/helper-hashes.json. Original CLI envelope/exact command/direct record required; aliases from S056. No live-tree write; removed private Git fixtures only. Local association, not authentication |
| round22-C2 | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py --root <LANE> --rev <REV>`; 0 dispositions_complete/14 matched, 1 dispositions_incomplete, 2 unevaluable | `--selftest` (optional `--root <LANE>`): 0 counter_controls_clean, 1 counter_controls_failed, 2 snapshot_tampered/unevaluable | Fixed T2/grammar in claims.json; frozen/expected-v2.json authenticates the independent fixture/dependency bytes before execution. Original source retained in frozen/count-c2.py. No live-tree writes, selftest private fixtures only. Strict observed-field/code agreement; semantic reason/placement and run metadata are separate admission checks |
| round22-capture-probes | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/capture-probes.py --out <NEW-DIR>`; 0 producer completed (child errors retained), other exit could-not-evaluate | No selftest: records requested outputs, does not grade a stored baseline | Writes new output directory only; invokes fixed REA6.5.0 calls, explicit false-client ADB and impossible-PID Frida request. Never reuse an existing output directory. No actual selected process, hardware or remote endpoint |
| round22-verify | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/verify.py --root <LANE> --rev <SOURCE-COMMIT> --out <NEW-DIR>`; 0 expected child conditions recorded, 1 discrepancy, 2 invalid invocation | Explicit final-suite producer, not an independent admission authority; self-invocation belongs to the child gates above | Writes only new output directory and removed external fixtures. Extracts candidate/frozen source from the requested commit, checks all old source rows and child controls, records positive/tampered selftest inputs, exact producer/envelope consistency and section-partitioned separability. Reuses R21 regression/no-harm gates; no REA target runs inside this producer |

Checklist: open source rows before writing them; bind each counted entry's
`source:` to a mined round-22 row naming it in `used-by`; keep matching
positive and missing-source/probe-alias negatives. Count mentions and
exercised targets separately. A partial k/6 result remains exit1 even when
it meets this round's frozen k>=1 improvement predicate.

The active C1 witness is the **original CLI envelope**, not an extracted
bare record. Check success, exact producer verb, exact cited file and actual
operation. A retained copy cannot erase a refused parent. S056 grounds the
debugger aliases only; both debugger verbs remain Adjacent and not held.
The metric also refuses unreviewed helper bytes before import, uses strict
UTF-8, resolves one commit and ignores inherited Git routing/replacement refs.

For the positive static boundary, read
`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md` (S054/S055).
Saber identifies as Flutter with partial coverage while its separate Dart
AOT reader refuses the missing dynamic symbols. Never transfer success from
one producer to another, infer a Dart version from an unmapped snapshot hash,
or count a refusal as a second held verb.

## Offline recording and carrier-layout envelopes — round 23

Use the source-backed entries
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` (current S059/S060/S062; S058 superseded)
and `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` (current S063; S061 superseded).
They extend the frozen six-verb inventory without claiming full completeness,
signal hardware ownership, source recovery or debugger execution.

| Selected input | Bounded decision |
|---|---|
| Decoder discovery | `inspect-signal-decoders --all` or exact decoder help; the subject/digest names the configured launcher. Read diagnostics: an exhausted window excludes modules that failed to load |
| Existing raw UART sample file | Select the recording's actual channel count, sampling frequency and protocol baud explicitly; `binary:numchannels=1:samplerate=960000` and `uart:rx=0:baudrate=9600` are the exercised synthetic example, not defaults for arbitrary recordings. `uart=rx-data` returns literal sample-range annotations, not observed device behavior |
| Selected sigrok session file | Preserve the recording digest and documented channel mapping; public provenance is source attribution. Leading annotations may disagree with an expected payload; do not call the entire output lossless |
| Selected four-symbol x86_64 Dart libapp with supported kind-3 data headers, valid shared hash and fitting declared lengths | `inspect-dart-aot` reports complete libapp section/header coverage for this carrier while overall and string_pool coverage stay partial. Preserve prior carrier-specific refusals; the old refusal's selected ABI is unrecorded, and no universal SDK compatibility or causal version boundary follows |
| Live debugger, acquisition or device-control request | Still Adjacent/unheld. Offline parsing does not resolve the kaidoku/revenger arbitration |

Signal CLI uses `REA_SIGROK_COMMAND` (absolute selected launcher),
sigrok-cli0.7.2 with libsigrokdecode and `/usr/bin/prlimit`; the checked
lane-local reproduction recipe and selected dependency pins are under
`.ufo/waves/round-23/`. The envelope's `hardware_acquisition:not-performed`
is a provider declaration, not an independent device-contact monitor.
No no-execution guard or OS sandbox is asserted.

### Round-23 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round23-C1 | gate / kaidoku | `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE> --rev <REV>`; 0 clean c1_complete6/6, 1 failed c1_incomplete, 2 could-not-evaluate/unevaluable. Round improvement target is k>=2, not a green completeness gate | Same entry with `--root <LANE> --selftest`; 0 selftest_clean, 1 selftest_failed, 2 could-not-evaluate including snapshot_tampered | Fixed B/six targets, reviewed R22/R21/R20 hashes; active frozen/expected-v3.json pins independent fixture program/template and the pre-v3 counter used only for red regression, manifest digest in executable. V1/v2 and the duplicate legacy expected.json are retained historical evidence, not active aliases. Current old knowledge modes/blobs, source prefix, catalog and evidence tree are checked; new entries/Evidence must be regular Git blobs. New scan requires S058+ linkage and recognized structural refusal ancestry before reviewed binding. Removed scratch/private Git clones under ignored runtime; local association, not authentication; original run consistency is separate |
| round23-signal-description | probe / kaidoku | `python3 -I -B .ufo/waves/round-23/tools/describe-signals.py --root <LANE> --rev <REV>`; 0 report produced, inspect discrepancy fields; 2 could-not-evaluate | No selftest: field/consistency descriptor, not admission oracle | Named committed original envelopes/run records/carriers; stdout only, no producer replay or live-tree writes |
| round23-dart-description | probe / kaidoku | `python3 -I -B .ufo/waves/round-23/tools/describe-dart.py --root <LANE> --rev <REV>`; 0 report produced, inspect discrepancy fields; 2 could-not-evaluate | No selftest: field/consistency descriptor, not admission oracle | Named committed L1 envelope/run/fetch; stdout only, no target replay, SDK inference or live-tree writes |
| round23-final-producer | probe / kaidoku | `python3 -I -B .ufo/waves/round-23/verify.py --root <LANE> --rev <SOURCE-COMMIT> --out <NEW-DIR>`; 0 declared finite conditions observed, 1 discrepancy, 2 could-not-evaluate/invocation | No independent selftest: exercises the child gate, input tamper/setup-failure controls, old/current counter regression, original-run consistency, no-harm and source-prefix checks | Own inputs execute in a committed private clone; external fleet census script is fingerprinted at invocation, not lane-owned or continuously pinned. Snapshot census uses that clone and an explicit date; required live end census is recorded separately. Writes a new output directory and removed private clones under ignored runtime. No REA replay, OS sandbox, native judge, authentication or outside admission |

Checklist: count each verb once; retain the exact incomplete remainder; separate
catalog mentions from held targets; never replace a parent refusal with a
detached success copy; report every module-load warning and projection cap.
Source relevance and ownership remain manual admission duties, not token matches.
