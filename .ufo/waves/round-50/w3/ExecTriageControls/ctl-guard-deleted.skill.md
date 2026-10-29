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
| SquashFS v1.0/v2.0 (standard, gzip) | `extract-firmware` with `sasquatch` 4.5.1 on the child PATH; expect handler `squashfs_v1`/`squashfs_v2`, `extraction_gaps == []`, members equal `unsquashfs -lls`; without sasquatch a `missing-extractor-dependency` gap | held r49 on four fixtures (`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`); `squashfs_v2_nonstandard` (no second reader), v2.1, v3 Broadcom/non-standard stay frontier — the v4 triage table (block 21) does not apply to them |
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

- **SquashFS `extract-firmware` outcome triage (round 39).** An REA 6.5.0
  `extract-firmware` envelope on a SquashFS v4 input resolves to one of eight
  labels from six fields: the squashfs chunk handler, the gap kinds, the gap
  `dependencies` (a miss names `sasquatch-v4be` for big-endian and `sasquatch`
  for little-endian), whether a recorded sasquatch argv carries `-be`, whether
  `MaliciousSymlinkRemoved` was reported, and the published file count
  (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:11-28`). An AVM-marked
  standard-BE image and a damaged one both end as `extractor-failure` with zero
  files; only the recorded `-be` token separates them, because unblob drops `-be`
  exactly when `bytes_used == mkfs_time`
  (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:29-40`). A kept in-tree
  symlink is one `unpublished-entry` gap; an escaping one is removed with a report
  and no gap; a missing chunk is a silent empty envelope
  (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:41-54`). Rows are tried
  top to bottom; the first match wins, no match is `unclassified`
  (interpreter `tools/round-39/sqfs-triage.py`). Superseded for routing
  and for the action column by rule block 19 (table v2, round 40), itself
  superseded by block 20 (table v3, round 41); this v1 table stays as the
  round-39 record and mislabels mixed-link images and non-firmware envelopes,
  cannot label partial failures or empty trees, and wraps `-be` unconditionally
  on its AVM-marker row without the layout check every later table carries
  (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`).

  <!-- sqfs-triage-table v1 -->
  | label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | no-squashfs-chunk | `none` | `*` | `*` | `n/a` | `*` | `*` | no chunk carries a squashfs handler: unblob's finder dropped a truncated image, a `bytes_used` past the end or a non-4 `s_major` without a report -> check the magic and superblock before rerunning; an empty envelope is not an empty filesystem | knowledge entry :50-54 |
  | dep-missing-be | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | the big-endian handler needed sasquatch-v4be and it was not on the unblob child PATH -> put the sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh output directory; the image is unmeasured, not unreadable | S112 lines 68-69; S120 command.py:101-102 |
  | dep-missing-le | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | the little-endian handler needed plain sasquatch and it was not on the child PATH -> put sasquatch on that PATH and rerun; sasquatch-v4be alone does not satisfy this gap; an AppImage before-arm still publishes its ELF prefix and the opaque container range | S112 lines 68-69; S120 command.py:101-102 |
  | avm-marker-be-dropped | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | mkfs_time equals bytes_used, unblob read the AVM marker and omitted -be, so sasquatch-v4be read a standard-BE body with the wrong byte order -> do not treat it as damage; rerun through a PATH wrapper named sasquatch-v4be that appends -be (REA has no flag passthrough) | S112 lines 44-50; S121 |
  | body-extractor-failure | `squashfs_v4_be` | `extractor-failure` | `none` | `yes` | `no` | `0` | the extractor ran with -be and still failed, so the image body or header is damaged -> keep the failing command and stderr from diagnostics, compare against a known-good carrier, never patch the envelope into a success | S120 report.py:91-98; knowledge entry :29-40 |
  | escaping-symlink-removed | `squashfs_v4_*` | `*` | `*` | `n/a` | `yes` | `>0` | a symlink target resolved outside the extraction root; unblob removed it and reported MaliciousSymlinkRemoved, and REA records no gap for it -> expect the path to be absent; never materialise the link or match it against the regular-file oracle | S118 extractor.py:79-91 |
  | in-tree-symlink-metadata | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` | a symlink target resolved inside the extraction root; it is kept as metadata and recorded as one unpublished-entry gap per link -> expected, not a failure; count one gap per in-tree link and publish nothing for it | S119 FirmwarePublication.js:68-75,301-308 |
  | clean | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | every regular file was published, no gap was recorded and no symlink was removed -> nothing to fix; match files to an oracle by relative-path suffix and sha256 | S119; knowledge entry :11-19 |

- **SquashFS `extract-firmware` outcome triage v2 (round 40).** Table v2 reads
  eight fields of an REA 6.5.0 envelope, the six of rule block 18 plus `operation`
  and `provider.id`, and answers a (label, action) pair: labels are unique and the
  action is one token from the vocabulary line above the table
  (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:11-18`). Every row requires `extract_firmware` from `unblob`, so a region
  scan or any other verb is `unclassified` instead of a SquashFS verdict
  (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:19-26`). Three outcomes v1 could not label get rows: `mixed-symlinks` ahead
  of the escaping row, `partial-body-failure` (failure with files published) and
  `clean-empty` (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`). The AVM-marker row covers a doctored marker on a
  standard-BE body only; a genuine AVM-layout body extracts without `-be`
  (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:37-45`). Scored on a held-out set seeded by the round-40 freeze, with the
  limits in `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:46-56` (interpreter `tools/round-40/sqfs-triage-v2.py`).
  Superseded for routing and for the action column by rule block 20 (table v3,
  round 41): v3 matches the failure, depth and mixed rows by containment, where
  this table's exact-set cells send a partial failure that also carries a link
  gap into `escaping-symlink-removed`; it adds the `depth-limited` row this table
  lacks, so all four round-40 C1 carriers were `unclassified` here; and its
  layout pre-check replaces this bullet's claim that the AVM-marker row covers a
  doctored marker on a standard-BE body only.

  <!-- sqfs-triage-table v2 -->
  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty -->
  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | no chunk carries a squashfs handler: unblob's finder dropped a truncated image, a bytes_used past the end or a non-4 s_major without a report, so no sasquatch of either flavour ran -> check the magic and superblock before rerunning; an empty envelope is not an empty filesystem | S112 finder v4 patterns; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :50-54; R39-CL3 |
  | dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | `install-extractor-be` | the big-endian v4 handler resolved its extractor to sasquatch-v4be and that binary was not on the unblob child PATH, so no command ran and no argv exists -> install the onekey-sec sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh output directory; the image is unmeasured, not unreadable; files stay * because an AppImage before-arm publishes its ELF prefix beside the same gap | S112 :68-69; S120 command.py :69-77,101-102; round-36 K3/before.json |
  | dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | `install-extractor-le` | the little-endian v4 handler resolved its extractor to plain sasquatch and that binary was not on the child PATH, so no command ran -> install the little-endian sasquatch 4.5.1 binary (sasquatch-v4be alone does not satisfy this gap) and rerun into a fresh output directory; an AppImage before-arm still publishes its ELF prefix and opaque container range | S112 :25,37,68-69; S120 command.py :101-102; round-36 K3/before.json |
  | avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `*` | `*` | `wrap-extractor-be` | mkfs_time equals bytes_used, so unblob omitted -be and sasquatch-v4be failed; on a standard-BE body with a doctored marker that is the byte-order handshake, not damage, while a genuine AVM-layout body (little-endian metadata block lengths) extracts without -be and never reaches this row -> walk the inode-table metadata headers little-endian first: if they land on directory_table_start the image is AVM layout and its failure is damage (keep it); otherwise rerun through a PATH wrapper named sasquatch-v4be that appends -be (REA has no flag passthrough) and remove the wrapper afterwards | S112 :44-50; S121 -DFIX_BE build; knowledge 2026-10-26-r40-sqfs-triage-v2.md :37-45 |
  | body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `*` | `*` | `0` | `preserve-failure` | the extractor ran and still failed with zero files published, so the fault is in the image body or the extractor build rather than the endianness handshake -> keep the failing command and stderr from diagnostics, diff the carrier against a known-good arm, and never patch the envelope into a success | S120 report.py :91-98; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40; R39-CL3 D1 |
  | partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `*` | `*` | `>0` | `salvage-partial` | the extractor failed after publishing at least one regular file, so the envelope is a partial success that a zero-file failure row would hide -> keep the published files and the failing command, match files to the oracle only by relative-path suffix and sha256, mark the run incomplete, and never score the set as clean | R39-CL3 D1 (full-be1-xz P>0); w2/R39W2C2TableReview.md |
  | mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds are present in one image: one or more symlinks escaped the extraction root and were removed with a MaliciousSymlinkRemoved report, and one or more stayed in-tree as unpublished-entry gaps -> expect the escaped paths absent, count exactly one gap per kept link or special file, and never read this as permission to ignore the in-tree gaps | S118 extractor.py :50-92; S119 firmwareAnalysis.js :137-141, FirmwarePublication.js :68-75; R39-CL2; c1/K5,K6 after.json |
  | escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `*` | `*` | `*` | `yes` | `*` | `expect-link-absent` | a symlink target resolved outside the extraction root, or the link looped, so unblob removed it and reported MaliciousSymlinkRemoved, and REA records no gap for the removal -> expect the path to be absent, never materialise the link, and never match a symlink row against the regular-file oracle; check for unpublished-entry gaps separately | S118 extractor.py :50-92 (loop branch :58-65); c1/K1 after.json |
  | in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `*` | `no` | `*` | `count-gap` | every non-file entry resolved inside the extraction root, so it is kept as metadata and recorded as one unpublished-entry gap per entry while only regular files are published -> expected, not a sasquatch failure; count one gap per in-tree link or special file and install nothing | S119 firmwareAnalysis.js :137-141, FirmwarePublication.js :68-75,301-308; c1/K2 after.json |
  | clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `no` | `>0` | `none` | every regular file was published, no gap was recorded and no symlink was removed -> nothing to install or fix; match files to the oracle by relative-path suffix and sha256, and ignore nested carves | c1/K3,K4 after.json; c2/H01,H02,H03,H04 |
  | clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `*` | `no` | `0` | `confirm-empty` | the extractor completed with no gap and published zero regular files because the image tree holds no regular file -> an empty result is a fact about this image, not a silent failure: confirm the independent oracle tree is empty before calling it clean, and never confuse it with the no-chunk row | R39-CL3 D2 (full-be-dirempty-gzip clean P=0); w2/R39W2C2TableReview.md |

- **SquashFS `extract-firmware` outcome triage v3 (round 41).** Table v3 screens
  the same eight envelope fields as v2 and answers one (label, action) pair per
  envelope; seven of the eight decide a scored class, because the `dependencies`
  cell is required by the dependency clauses yet redundant with the handler on
  every class measured so far (a `squashfs_v4_be` dependency gap always names
  `sasquatch-v4be`, a `squashfs_v4_le` one always names `sasquatch`). It is
  written from the round-41 label precedence rather than from a generator's class
  map, and its gap-kind cells may be *contains* tests:
  a cell ending in `+` (`kind+`, or `a,b+`) matches when the envelope's gap-kind
  set **holds** those kinds, while every other non-`*` gap-kind cell stays
  exact-set equality. That is what labels a combined gap
  set — a partial failure that also kept or removed a link, a depth-limited carve
  beside symlink gaps — by the row the precedence names, instead of letting the
  first symlink row that happens to match absorb it
  (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:11-25`). New rows:
  `depth-limited` for a run whose `max_depth` stopped descent into an extract
  directory (REA records it even with no nested image at `--max-depth 1`; all
  four round-40 C1 AVM carriers carry `depth-limited` and v2 refused them as
  `unclassified`). Repaired cells: `escaping-symlink-removed` pins its gap cell to
  the empty set, `in-tree-symlink-metadata` to the exact singleton, the clean row
  no longer claims no link was removed (unblob removes an empty-target link
  silently), and the two dependency rows cite REA as the minter of the gap kind.
  Rows are tried top to bottom and the more specific row is always above the more
  general one: a failure row above the depth row, the depth row above both symlink
  rows, `mixed-symlinks` above `escaping-symlink-removed`, the AVM row above the
  body row. The reader is this block: the interpreter parses this table out of
  `SKILL.md` and carries **no embedded copy** of it, so a table fix cannot leave a
  stale second text behind. Superseded for routing and for the action column by rule block 21 (table v4,
  round 42): v4's handler cells cover the seven v1–v3 handler names this table's
  `squashfs_v4_*` cells cannot match, so a legacy chunk is labelled instead of falling to
  `unclassified`, and v4 adds the `legacy-body-failure` row, whose action is a cross-read
  rather than the `-be` wrapper.

  **Layout pre-check — run it before acting on any `extractor-failure` row.** The
  envelope cannot see metadata block-length endianness. Read the body: walk the
  inode-table metadata headers at `inode_table_start` as 2-byte little-endian
  lengths; if they land exactly on `directory_table_start` the body is AVM layout.
  Then, for the two failure rows below: AVM layout with `-be` absent → the omission
  was right and the failure is damage, so keep it (`preserve-failure`); AVM layout
  with `-be` present → `-be` is the wrong reading, so rerun through a PATH
  executable named `sasquatch-v4be` that **drops** the `-be` token before
  exec'ing the real binary; standard BE
  with `-be` absent → the marker is doctored (`wrap-extractor-be`); standard BE
  with `-be` present → damage. The pre-check overrides the action cell where it
  fires; an inconclusive walk (truncated body, headers that do not land on the
  table) leaves the cell standing. The `cause` and `source` columns are prose and
  are not scored; the action column is. A timed-out extractor records `cmd` rather
  than `command` (S120 `report.py:125-138`), so `-be` reads `n/a` on such a run,
  and the firmware input limit is 128 MiB with a 120 s timeout per run (S119
  `FirmwareRelease.js:27-32`).

  **Status — unscored claim.** Table v3 carries no scored claim: R41-C2 stopped at the round-41 scoring on a counter key mismatch, not on the table — the C2 counter took the combo carriers' declared tuple under `class_expected.features`/`features`/`declared_features` while the generator wrote it under `declared` (M41-1, R41-CL1), so R41-C2 exited 1 with `observed_features_match_declared` false (receipt `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`, `matched 52` of `n 52`) — and v3 is superseded for routing and for the action column by rule block 21 (table v4).

  <!-- sqfs-triage-table v3 -->
  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | no `squashfs_v4_*` chunk was carved: unblob's finder pins `s_major` 4 for both v4 magics (S112 :463,:522) and drops a truncated image, a `bytes_used` past the end or a non-4 major without a report, while a v1-v3 chunk (S112 :102,:159,:245) is not a v4 chunk -> check the magic and superblock before rerunning; an empty envelope is not an empty filesystem | S112 :102,:159,:245,:463,:522; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :50-54; R39-CL3 |
  | dep-missing-be | `extract_firmware` | `unblob` | `squashfs_v4_*` | `missing-extractor-dependency+` | `sasquatch-v4be` | `*` | `*` | `*` | `install-extractor-be` | a v4 chunk resolved its extractor to `sasquatch-v4be` and that binary was not found on the unblob child PATH, so no command ran and no argv exists (S112 :24,:68-69 names both executables; S120 `command.py:70-72` raises the dependency report before the spawn) -> install the onekey-sec sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh output directory; the image is unmeasured, not unreadable; REA itself mints this gap kind and leaves the file count open, because an AppImage before-arm still emits its ELF prefix beside the same gap (S119 `FirmwarePublication.js:161-186`, `firmwareAnalysis.js:85`) | S112 :24,:68-69; S120 `report.py:118-122`, `command.py:70-72`; S119 `FirmwarePublication.js:161-186`, `firmwareAnalysis.js:85`; round-36 K3/before.json |
  | dep-missing-le | `extract_firmware` | `unblob` | `squashfs_v4_*` | `missing-extractor-dependency+` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | a little-endian v4 chunk resolved its extractor to plain `sasquatch` and that binary was not on the child PATH, so no command ran (S112 :24,:68-69) -> install the little-endian sasquatch 4.5.1 binary and rerun into a fresh output directory; sasquatch-v4be alone does not satisfy this gap because the dependency report names only the executable the handler resolved (S120 `command.py:70-72`); a dependency list naming both resolves to the BE row above, not here | S112 :24,:68-69; S120 `report.py:118-122`, `command.py:70-72`; S119 `FirmwarePublication.js:186-201`, `firmwareAnalysis.js:85`; round-36 K3/before.json |
  | partial-body-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | the extractor failed after publishing at least one regular file (REA turns a failed chunk into one `extractor-failure` gap, S119 `FirmwarePublication.js:288-293`), so the envelope is a partial success that a zero-file failure row would hide -> keep the published files and the failing command, match the published subset to the oracle by exact relative path and sha256, mark the run incomplete, and never score the set as clean; symlink or depth gaps ride along without changing this row | S119 `FirmwarePublication.js:288-293`; w2/R40W2C2IndepEval.md §6 (4 of 5 published files match the oracle, the fifth a 16384-byte truncation of an 19873-byte file); c2/H21,H22 |
  | avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | unblob read the AVM marker `mkfs_time == bytes_used` (S112 :48) and omitted `-be` (S112 :49-50), so sasquatch-v4be read a standard big-endian body's metadata block lengths in the wrong order and failed with zero files -> rerun through a PATH executable named `sasquatch-v4be` that appends `-be` (REA has no flag passthrough), then remove it; the layout pre-check above decides first and its damage branch overrides this action on an AVM-layout body | S112 :44-50; S121 -DFIX_BE build; PATH-wrapper delivery measured through REA 6.5.0 (round-41 `w1/artifacts/R41C2TableDraft/l2-wrapper-measurement.md`); knowledge 2026-10-26-r40-avm-be-squashfs-core.md :37-45 |
  | body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | the extractor ran and published zero regular files, and the envelope cannot say why: with `-be` recorded the handshake was applied, which is the wrong reading for a genuine AVM-layout body whose metadata block lengths are little-endian (S124 :35), while with `-be` absent on a standard BE body the marker was doctored, so the fault is the body's own bytes or the extractor build -> run the layout pre-check above first, then keep the failing command, stdout and stderr from diagnostics (S120 `report.py:91-98`), diff the carrier against a known-good arm, and never patch the envelope into a success | S120 `report.py:91-98`; S124 :35; S112 :44-50; w1/R40MistakeHunt.md MH-6; R39-CL3 D1 |
  | depth-limited | `extract_firmware` | `unblob` | `squashfs_v4_*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | REA stopped at `max_depth` and recorded one `depth-limited` gap per path it did not descend into, with an empty dependency list and a continuation that names the rerun (`MAX_EXTRACTION_DEPTH` is 10, S119 `FirmwarePublication.js:23-29,:294-299`) -> rerun `extract_firmware` with a higher `max_depth` (up to 10) into a fresh output directory; at the ceiling rerun with `path` set to one published child below the path, which restarts the depth budget, and when no published child is nonempty and within the 128 MiB firmware input limit treat the region as unexamined, never as empty | S119 `FirmwarePublication.js:23-29,:243-247,:294-299`, `FirmwareRelease.js:27-32`; c1/V1,V2,L1,L2 after.json (all four carry exactly {depth-limited, unpublished-entry}) |
  | mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds are present in one image: at least one link escaped the extraction root or looped and was removed with a `MaliciousSymlinkRemoved` report (S118 :58-65 loop, :79-90 containment), and at least one stayed in-tree as one `unpublished-entry` gap per link or special file (S119 `FirmwarePublication.js:301-307`; kinds `symlink` and `special`, `firmwareAnalysis.js:139`) -> expect the escaped paths absent, count one gap per kept link or special file, and never read this as permission to ignore the in-tree gaps; a `depth-limited` gap would have been decided one row above | S118 :50-92; S122; S119 `FirmwarePublication.js:301-307`, `firmwareAnalysis.js:139`; c1/K5,K6 after.json; c2/H11,H12 |
  | escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | a link target resolved outside the extraction root, or the link looped, and unblob removed it with a `MaliciousSymlinkRemoved` report (S118 :58-65,:79-90) while REA records no gap for the removal, so the gap set is empty -> expect the path to be absent, never materialise the link, and never match a symlink row against the regular-file oracle; any gap at all means a combined set, and the rows above decide it | S118 :42-47,:58-65,:79-90; S122; c1/K1 after.json; c2/H07,H08 |
  | in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | the gap set is exactly one kind: every non-file entry resolved inside the extraction root and is kept as metadata, one `unpublished-entry` gap per entry, while only regular files are published (S119 `FirmwarePublication.js:301-307`; `symlink` and `special` both count, `firmwareAnalysis.js:139`) -> expected, not a sasquatch failure; count one gap per in-tree link or special file and install nothing; a second gap kind means a combined set, and the rows above decide it | S119 `FirmwarePublication.js:301-307`, `firmwareAnalysis.js:139`; c1/K2 after.json; c2/H09,H10 |
  | clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `>0` | `none` | every regular file was published and the gap set is empty, and a `MaliciousSymlinkRemoved` report would have hit the escaping row above -> nothing to install or fix; match files to the oracle by exact relative path and sha256, and ignore nested carves; the envelope cannot rule out a link unblob removed with no report at all (the empty-target branch, S118 :67-69), so a link present in the oracle tree and absent from the output is that case, not a missed symlink gap | S118 :67-69; S119 `FirmwarePublication.js:301-307`; c1/K3,K4 after.json; c2/H01,H02,H03,H04; [INFERENCE] no committed envelope carries an empty-target link |
  | clean-empty | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `*` | `*` | `no` | `0` | `confirm-empty` | the extractor completed with no gap and published zero regular files because the tree holds no regular file, only regular files being published (S119 `FirmwarePublication.js:301-307`) -> an empty result is a fact about this image, not a silent failure: confirm the independent oracle tree is empty before calling it clean, and never confuse it with the no-chunk row; measured on the round-40 class whose oracle is empty | S119 `FirmwarePublication.js:301-307`; R39-CL3 D2; c2/H05,H06; w2/R40W2C2TableReview.md special-attention 4 |

- **SquashFS `extract-firmware` outcome triage v4 (round 42).** Table v4 answers the
  same (label, action) pair from the same eight envelope fields as v3 and moves three
  boundaries v3 could not express (`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md:1-14`). (1) It covers the **whole SquashFS handler family**, not
  the v4 handlers alone. `H` is the precedence text's `H` — the handler names in
  `normalized_result.chunks[].handler` *and* `normalized_result.extraction_gaps[].handler`,
  nulls dropped (S119 `firmwareAnalysis.js:95`) — `F` is the members of `H` that start
  `squashfs_`, `L` the members of `F` that start `squashfs_v1`, `squashfs_v2` or
  `squashfs_v3`, and `HF` the handlers of the `extractor-failure` gaps, or `F` when none of
  them carries one. A v1–v3 chunk is an ordinary SquashFS chunk: unblob carves it with one
  of seven handler names (`squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`,
  `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`;
  S112 :102,:159,:200,:245,:319,:364,:410) and runs plain `sasquatch` on it
  (S112 :37,:51-54). That is the R41-CL4 repair: v3's precedence answered
  `no-squashfs-chunk` for a legacy chunk (it tested for a `squashfs_v4_*` handler) while
  v3's table answered `unclassified` (no handler cell matched), and both hide an extraction
  outcome about a filesystem the finder did carve. (2) A depth ceiling with **no** SquashFS
  handler in the envelope is a container result, not a missing image: the whole-TRX
  dev-arm run has `H = {trx_v1}`, `G = {depth-limited}` at `--max-depth 1` and v3 answers
  `no-squashfs-chunk` / `inspect-input` — `container-depth-limited` / `raise-depth` is the
  honest pair, because the filesystem sits below a wrapper the run did not descend into
  (S119 `FirmwarePublication.js:294-299`). (3) Bytes beside the filesystem that no handler
  claimed are a residue, not an unknown image: `unknown-chunk-handler` is minted per chunk
  with a null handler (S119 `FirmwarePublication.js:286`) and unblob carves the range as
  `<start>-<end>.unknown` beside the tree (S118 :116-127), which is the
  `unknown-residue` / `isolate-residue` row — and it sits **above** the depth row, because
  the measured envelope that carries both decides on the residue. The table has **thirteen
  columns**: `handler` is a glob over `F` (`none` means `F` is empty, `*` any `F`) and the
  new `failing handler` column is a glob over `HF` (`*` matches anything, an empty `HF`
  included), which is what makes clauses 6 and 7 about the chunk that failed rather than
  about any chunk present. Three grammar deltas ride with the table. (a) The marker is `v4`
  and a craft section whose only marker is older is refused. (b) `dependencies` gains the
  `+` contains form `gap kinds` already has, because each dependency clause is membership
  ("D holds `sasquatch-v4be`") and an exact-set cell lost a dependency set naming both
  binaries — the round-41 MEDIUM finding, executed in round-41 `w2/R41W2C2Table.md` F1.
  (c) The thirteenth column itself, with `HF` defined as the `extractor-failure` gaps'
  handlers and `F` as its fallback. Rows are tried top to bottom, the more specific
  above the more general, and the reader parses this block out of `SKILL.md` with **no
  embedded copy**, taking the first table under the v4 marker. New rows:
  `container-depth-limited`, `unknown-residue`, and `legacy-body-failure` — the last one's
  action is a cross-read, never the `-be` wrapper, because the AVM pre-check cannot fire on
  a v1–v3 superblock.

  **Layout pre-check — run it before acting on a BE-v4 `extractor-failure` row, never on a
  v1–v3 body.** unblob reads the AVM marker `mkfs_time == bytes_used` and drops `-be` only
  inside its `Endian.BIG, version 4` branch; for every other version it appends `-be` on a
  big-endian magic and `-le` on a little-endian one and parses no header at all
  (S112 :39-54), so a v1–v3 failure is decided by the legacy row's cross-read instead. On a
  BE-structural v4 body: walk the inode-table metadata headers at `inode_table_start` as
  2-byte little-endian lengths; if they land exactly on `directory_table_start` the body is
  AVM layout. Then, for the two BE-v4 failure rows below: AVM layout with `-be` absent →
  the omission was right and the failure is damage, so keep it (`preserve-failure`); AVM
  layout with `-be` present → `-be` is the wrong reading, so rerun through a PATH
  executable named `sasquatch-v4be` that **drops** the `-be` token before exec'ing the real
  binary (the body side is measured — four files without the flag, zero with it, round-40
  `w1/R40MistakeHunt.md` MH-6 — while the PATH delivery of the drop is composed from the
  measured append wrapper, `[INFERENCE]`); standard BE with `-be` absent → the marker is
  doctored (`wrap-extractor-be`); standard BE with `-be` present → damage. The pre-check
  overrides the action cell where it fires; an inconclusive walk (truncated body, headers
  that do not land on the table) leaves the cell standing. The `cause` and `source` columns
  are prose and are not scored; the action column is. A timed-out extractor records `cmd`
  rather than `command` (S120 `report.py:125-138`), so `-be` reads `n/a` on such a run and a
  timed-out BE failure lands on the body row; a clean run need not record the child argv at
  all (both dev-arm legacy envelopes measured this wave carry no sasquatch command, so
  `-be` reads `n/a`), which is why no row below requires `yes`. The firmware input limit is
  128 MiB with a 120 s timeout per run (S119 `FirmwareRelease.js:27-32`).

  **Status — unscored claim.** Table v4 matched its independent evaluator 78 of 78 at `eb8215ac` (receipt `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`, `pair_mismatches []`, `evaluator_missing []`, `evaluator_extra []`), but R42-C2 stopped on `observed_features_match_declared` — combo C02 declared the gap set {`extractor-failure`, `unpublished-entry`} while its own extraction run also observed `depth-limited` (M42-2, R42-CL1) — so the table is unscored as a claim and round 43 re-scores it under P43-C1.

  <!-- sqfs-triage-table v4 -->
  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be cross-read-legacy isolate-residue preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
  | label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | container-depth-limited | `extract_firmware` | `unblob` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | no SquashFS handler was named and REA stopped at `max_depth`, so the filesystem sits below a container this run did not descend into: the whole OpenWrt TRX at `--max-depth 1` reports `H = {trx_v1}` with one `depth-limited` gap (S119 `FirmwarePublication.js:294-299`) -> rerun with a higher `max_depth` (up to 10) or with `path` set to the published container below this path, into a fresh output directory, and never answer `inspect-input`: a SquashFS image inside a wrapper is not a missing image; at the ceiling with no eligible child the region is unexamined, never empty | S119 `FirmwarePublication.js:23-29,:294-299`; `.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/trx-img-with.json` and `w1/R42C1DevRun.md` (H = {`trx_v1`}, G = {`depth-limited`}); round-41 c2/H31-H36 |
  | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | neither a chunk nor a gap names a SquashFS handler and no depth gap explains it, so no sasquatch of either flavour ran: unblob's finder pins `s_major` 4 for both v4 magics (S112 :463,:522) and drops a truncated image, a `bytes_used` past the end or a major it does not pin without a report -> check the magic and superblock before rerunning; a v1-v3 chunk is never this row, because unblob carves it with a v1-v3 handler and extracts it (S112 :102,:159,:200,:245,:319,:364,:410), and a wrapper the run did not descend into is the row above | S112 :102,:159,:200,:245,:319,:364,:410,:463,:522; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :50-54; R39-CL3; R41-CL4; c2/H23,H24 |
  | dep-missing-be | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `sasquatch-v4be+` | `*` | `*` | `*` | `install-extractor-be` | a v4 BE-magic chunk resolved its extractor to `sasquatch-v4be` (S112 :40-41) and that binary was not found on the unblob child PATH, so no command ran and no argv exists (S120 `command.py:69-77` raises the dependency report before the spawn) -> install the onekey-sec sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh output directory; the image is unmeasured, not unreadable; the file count stays open because an AppImage before-arm still emits its ELF prefix beside the same gap | S112 :25-26,:40-41,:68-69; S120 `report.py:118-122`, `command.py:69-77,101-102`; S119 `FirmwarePublication.js:161-186`, `firmwareAnalysis.js:85`; c2/H13,H14 |
  | dep-missing-le | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `sasquatch+` | `*` | `*` | `*` | `install-extractor-le` | a SquashFS chunk resolved its extractor to plain `sasquatch` and that binary was not on the child PATH; the executable stays `sasquatch` for every chunk except a v4 BE-magic one — every v1-v3 chunk of either endianness and every v4 LE chunk — and the BE branch only appends `-be` (S112 :37,:39-54; measured argv `sasquatch -be` on the v3 BE fixture this wave, and `dependencies: ["sasquatch"]` on the v3 dev-arm envelopes) -> install the little-endian sasquatch 4.5.1 binary and rerun into a fresh output directory; the label names the missing binary, not the image endianness; sasquatch-v4be alone does not satisfy the gap, because the report names only the executable the command resolved (S120 `command.py:70-72,101-102`); a dependency set holding both names is decided by the row above | S112 :25,:37,:39-54,:68-69; S120 `report.py:118-122`, `command.py:69-77,101-102`; S119 `FirmwarePublication.js:186-201`, `firmwareAnalysis.js:85`; c2/H15,H16; `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/measurements.md` |
  | partial-body-failure | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `>0` | `salvage-partial` | the extractor failed after publishing at least one regular file (REA mints one `extractor-failure` per failed chunk, S119 `FirmwarePublication.js:288-293`), so the envelope is a partial success that a zero-file failure row would hide -> keep the published files and the failing command, match the published subset to the oracle by exact relative path and sha256, mark the run incomplete, and never score the set as clean; symlink, residue, depth or dependency gaps ride along without changing this row | S119 `FirmwarePublication.js:288-293`; S112 :24-70 (one extractor class serves every SquashFS version); w2/R40W2C2IndepEval.md §6; c2/H21,H22,H27,H28,H29,H30 |
  | avm-marker-be-dropped | `extract_firmware` | `unblob` | `squashfs_*` | `squashfs_v4_be` | `extractor-failure+` | `*` | `no` | `*` | `0` | `wrap-extractor-be` | the handler that failed is the v4 BE one, unblob read the AVM marker `mkfs_time == bytes_used` (S112 :48) and omitted `-be` (S112 :49-50), so sasquatch-v4be read a standard big-endian body's metadata block lengths in the wrong order and failed with zero files -> rerun through a PATH executable named `sasquatch-v4be` that appends `-be` (REA has no flag passthrough), then remove it; the layout pre-check above decides first and its damage branch overrides this action on an AVM-layout body; the `failing handler` column is what makes this row about the failing chunk rather than about any chunk present (S112 :514,:527) | S112 :40-50,:514,:527; S121 `debian/rules` `-DFIX_BE` build; round-41 `w1/artifacts/R41C2TableDraft/l2-wrapper-measurement.md`; knowledge 2026-10-26-r40-avm-be-squashfs-core.md :37-45; c2/H17,H18 |
  | body-extractor-failure | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `0` | `preserve-failure` | the extractor ran and published zero regular files on a body the rows above did not claim: a v4 BE-magic body with `-be` applied, or a genuine AVM-layout body whose metadata block lengths are little-endian (S124 :35) -> run the layout pre-check above first, keep the failing command, stdout and stderr from diagnostics (S120 `report.py:91-98`), diff the carrier against a known-good arm, and never patch the envelope into a success; a v1-v3 body with zero files is the row above, not this one | S120 `report.py:91-98`; S124 :35; S112 :44-50; knowledge 2026-10-26-r39-sqfs-outcome-triage.md :29-40; c2/H19,H20,H37,H38 |
  | unknown-residue | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | the SquashFS chunk extracted and REA recorded an `unknown-chunk-handler` gap because some chunk had no handler (S119 `FirmwarePublication.js:286` mints it with a null handler), so bytes beside the filesystem belong to no parser and unblob carves them as `<start>-<end>.unknown` beside the tree (S118 :116-127) -> keep the residue out of the filesystem oracle, re-carve the SquashFS chunk to unblob's chunk end, and never read the residue as an extracted file or as proof of a second image; this row is above the depth row because the measured envelope carrying both is a residue case | S119 `FirmwarePublication.js:14,:226-238,:286`, `firmwareAnalysis.js:86`; S118 :116-127; `.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/x86-fs-with.json` and `w1/R42C1DevRun.md` (published `firmware.bin_extract/786432-851972.unknown`, 65 540 B tail) |
  | depth-limited | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | REA stopped at `max_depth` and recorded one `depth-limited` gap per path it did not descend into, with an empty dependency list and a continuation that names the rerun (`MAX_EXTRACTION_DEPTH` is 10, S119 `FirmwarePublication.js:23-29,:294-299`) -> rerun `extract_firmware` with a higher `max_depth` (up to 10) into a fresh output directory; at the ceiling rerun with `path` set to one published child below the path, which restarts the depth budget, and when no published child is nonempty and within the 128 MiB firmware input limit treat the region as unexamined, never as empty; with no SquashFS handler at all this is the container row above | S119 `FirmwarePublication.js:23-29,:243-247,:294-299`, `FirmwareRelease.js:27-32`; c1/V3,V4,L3,L4 after.json; c2/H31,H32,H33,H34,H35,H36; `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/measurements.md` (a real `squashfs_v3` envelope at `--max-depth 1` carries it, the same image at `--max-depth 3` does not) |
  | mixed-symlinks | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unpublished-entry+` | `*` | `*` | `yes` | `*` | `audit-symlinks` | both link kinds are present in one image: at least one link escaped the extraction root or looped and was removed with a `MaliciousSymlinkRemoved` report (S118 :58-65 loop, :79-87 containment), and at least one stayed in-tree as one `unpublished-entry` gap per link or special file (S119 `FirmwarePublication.js:301-307`; kinds `symlink` and `special`, `firmwareAnalysis.js:139`) -> expect the escaped paths absent, count one gap per kept link or special file, and never read this as permission to ignore the in-tree gaps; a residue or `depth-limited` gap would have been decided in the rows above | S118 :50-92; S122; S119 `FirmwarePublication.js:301-307`, `firmwareAnalysis.js:139`; c1/V3,V4; c2/H11,H12,H29,H30 |
  | escaping-symlink-removed | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `yes` | `*` | `expect-link-absent` | a link target resolved outside the extraction root, or the link looped, and unblob removed it with a `MaliciousSymlinkRemoved` report (S118 :58-65,:79-87) while REA records no gap for the removal, so the gap set is empty -> expect the path to be absent, never materialise the link, and never match a symlink row against the regular-file oracle; any gap at all means a combined set, and the rows above decide it | S118 :42-47,:58-65,:79-87; S122; c2/H07,H08 |
  | in-tree-symlink-metadata | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | `count-gap` | the gap set is exactly one kind: every non-file entry resolved inside the extraction root and is kept as metadata, one `unpublished-entry` gap per entry, while only regular files are published (S119 `FirmwarePublication.js:301-307`; `symlink` and `special` both count, `firmwareAnalysis.js:139`) -> expected, not a sasquatch failure; count one gap per in-tree link or special file and install nothing; a removed link beside it is taken by the mixed row above, and any other gap kind puts the envelope further down the clause list | S119 `FirmwarePublication.js:301-307`, `firmwareAnalysis.js:139`; c1/K2 after.json; c2/H09,H10 |
  | clean | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `*` | `>0` | `none` | every regular file was published and the gap set is empty, and a `MaliciousSymlinkRemoved` report would have hit the escaping row above -> nothing to install or fix; match files to the oracle by exact relative path and sha256, and ignore nested carves; the envelope cannot rule out a link unblob removed with no report at all (the empty-target branch, S118 :67-69), so a link present in the oracle tree and absent from the output is that case, not a missed symlink gap; measured on a real `squashfs_v3` envelope at `--max-depth 3` | S118 :67-69; S119 `FirmwarePublication.js:301-307`; c1/K3,K4 after.json; c2/H01,H02,H03,H04; `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/measurements.md`; [INFERENCE] no committed envelope carries an empty-target link |
  | clean-empty | `extract_firmware` | `unblob` | `squashfs_*` | `*` | `none` | `*` | `*` | `*` | `0` | `confirm-empty` | the extractor completed with no gap and published zero regular files because the tree holds no regular file, only regular files being published (S119 `FirmwarePublication.js:301-307`) -> an empty result is a fact about this image, not a silent failure: confirm the independent oracle tree is empty before calling it clean, and never confuse it with the no-chunk row | S119 `FirmwarePublication.js:301-307`; R39-CL3 D2; c2/H05,H06; w2/R40W2C2TableReview.md special-attention 4 |



- **22. Freeze integrity is an instrument, and every arm has a red case.** A freeze is
  worth what the gate that guards it can refuse, and round 44 proved the enforcement
  order wrong: the rule lived in claim files and in counters that only ran at scoring
  time, so eight files could sit dirty under a frozen directory pathspec and a
  non-author sweep could commit them inside a 432-path bulk commit
  (`corpus/lessons/round-44.md:18-19`, routed `corpus/lessons/round-44.md:63-69`). The
  rule is now executable: `tools/round-45/frozen-path-preflight.py` runs against a
  candidate revision and its worktree before the commit is treated as landed, and its
  `--selftest` carries one red case per arm (11 cases at the round-45 freeze). Read the
  table as an ordered decision list: the first row whose trigger holds decides, and a
  `2` is never a pass. Two parsers are load-bearing and both are pinned by a source
  opened this round: the dirty arm reads `git status --porcelain -z`, whose v1 format
  S140 guarantees stable for scripts and whose `-z` form is the machine one; the commit
  arm reads plain tab-separated `git log --name-status` records, and S141 states the
  separator rule that makes that parsing safe — with `-z` the fields are NUL-terminated and
  pathnames are not munged; the `-z` form is the machine-safe variant this arm does not use
  yet (routed R45-CL11). The exit column is the gate's; a scoring counter reports the same
  condition as `2` could-not-evaluate, never as a pass. The `commit` arm is ancestor-linear
  except for the `-m --diff-merges=first-parent` form it uses, which is what makes a merge's
  own resolution edit visible — a plain `git log --name-only` scan misses it, and both
  round-45 counters have exactly that blindness (HIGH, routed R45-CL6). An invocation must
  name every frozen path: this round's freeze has two, so the gate is called with
  `--pathspec tools/round-45/ --pathspec plans/round-45-claims.md` and the matching two
  `--freeze-path` values; one pathspec certifies four of the five frozen files (routed
  R45-CL10). Two limits are stated rather than hidden: the red cases are *arm-covering but
  not arm-isolating* — deleting the `restored` classification or the `blob` arm alone still
  reads 11/0 because `touched` absorbs the kill, so the arm-coverage matrix is the evidence
  for those two arms (routed R45-CL15); and `--dirty-pathspec` *replaces* the dirty arm's
  scope instead of adding to it, so a caller who narrows it loses the frozen pathspec and
  the gate reads clean on a dirty frozen file (a false-clean, reproduced and routed
  R45-CL15; this round's invocation never passes that flag). History, not tip equality, is
  the evidence: a path that was edited post-freeze and then restored to its exact bytes is
  still a violation (`corpus/lessons/round-44.md:88-92`,
  `corpus/lessons/round-44-verifier-spotcheck.md:89-92`), which is why the `restored`
  list is reported separately from `blob_changed` instead of collapsing into it.

  <!-- freeze-integrity-table v1 -->
  | trigger | arm | exit | receipt |
  | --- | --- | --- | --- |
  | any commit in FREEZE..REV touches a frozen path | commit (git log --name-status, S141) | 1 | `touched[]`, one record per path with commit and status |
  | a frozen path was touched and later restored to its FREEZE bytes | restored (commit history, never tip equality) | 1 | `restored[]`, disjoint from `blob_changed[]` |
  | a frozen path's blob at REV differs from its blob at FREEZE | blob or frozen subtree oid (ls-tree plus rev-parse on both revisions) | 1 | `blob_changed[]`; a directory entry is its tree oid, not a file |
  | the worktree is dirty under the frozen pathspec | dirty (git status --porcelain -z, S140) | 1 | `dirty[]` from `--check-dirty` |
  | a frozen path is a directory at FREEZE and no pathspec covers it | pathspec (`--require-pathspec`) | 2 | `uncovered_frozen_dirs[]`; a whole-tree scan is refused |
  | one bulk commit sweeps N frozen paths beside unrelated paths | commit plus dirty (the M45-1 shape) | 1 | `touched[]` count and the frozen subset |
  | FREEZE is not an ancestor of REV | revision guard | 2 | `reason` |
  | an unknown freeze or rev is named | revision guard | 2 | `reason` |
  | no touch, no dirty file and every frozen blob equal | all arms | 0 | `verdict clean` |
  | FREEZE equals REV (empty range) | all arms | 0 | `verdict clean` |

  The gate reports; it does not prevent. It runs where the lane can put it (the L1's
  commit sequence) and the arm that matters most, `--check-dirty`, catches the
  precursor before any sweep exists. Its own selftest is the red-case set, which is the
  one thing round 34 proved about gates of this family: a registered class set can hold
  while the surface is still shortcut-reachable, so the cases — not the registration —
  are the evidence (`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`).
  The transferable limit is stated instead of hidden: this instrument's "actionable
  table" test is structural (header cells, row count, exit cells, resolving citations),
  and a table of structurally valid but empty rows would pass it. Placement inside the fleet's own sweep path is not
  a lane edit — the fleet scripts are read-only for a lane — so it stays an
  operator/integrator request and the report says so (`corpus/lessons/round-45.md:12-17`).
  Claim clauses that name a frozen path are frozen at `plans/round-45-claims.md:132-147`:
  the claims file and the whole `tools/round-45/` directory, the latter a directory
  pathspec that must be passed explicitly.

- **23. Freeze-integrity evidence is only evidence when its own forgeries fail.** <!-- freeze-integrity-table v2 --> The round-45 table (block 22) stated the arms; this one states what makes the statement checkable — each row is a defect the round-45 closure routed (R45-CL13 a–f, R45-CL14 a–f), the v1 clause that let it pass, and the arm of the round-46 gate, attestation and registry tools that now fails it. Interpreter pin: `tools/round-46/attest.py` `sha256:c405613170f0581661b9e2afb4bf278da8ac1f936eeb00eb4b456a9e70ad8e5c`. Source S142.

| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R45-CL2 a registry row names a tool that exists at no revision | no presence check, so a ghost row registers | presence: `absent_at_rev` is computed from the census, never from the row | 1 |
| R45-CL6 a merge's own resolution edit touches a frozen path | `git log --name-only` prints no diff for a merge | merge: `--diff-merges=first-parent` plus an independent blob arm; the two must agree | 2 |
| R45-CL7 `rule_blocks >= 22` survives the counter's selftest | the clause is exercised from below only | rows: the selftest carries one red case per clause, and the mutation list is named in the claim | 1 |
| R45-CL9 a citation resolves but names nothing about the defect | the citation regex saw only the knowledge, lesson and plan trees, and accepted a reference with no selector | refs: every citation carries a line selector and a path inside the validated set; the interpreter is identified by its sha pin instead | 1 |
| R45-CL13 a 44-line artefact with garbage rows scores met | row count and exit cells are structural tests | rows: every row names a routed id and an arm from the fixed vocabulary, so a garbage row fails | 1 |
| R45-CL14 six fenced rows anywhere in SKILL.md register | the parser was fence-blind, comment-blind and heading-blind | marker: rows register only between the two registry markers and outside fences and comments | 1 |
| R45-CL15 `--dirty-pathspec` replaced the dirty scope instead of adding to it | the arm is arm-covering but not arm-isolating | dirty: the dirty scope is the union of the pathspecs, and each arm has a red case that names it | 1 |
| R45-CL18 a path named only by `--freeze-path` never entered `touched`, so tamper-then-restore read clean | the log scope and the freeze scope were different sets | restored: one frozen set derived from the claims file feeds both arms, so the sets cannot differ | 1 |
| R45-CL19 a tamper-then-restore folded away by `git merge --squash` | the surviving history names nothing | none: the blob arm compares the two revisions and a squash leaves both trees identical, so the gate returns 0 and this row states the limit instead of pretending to see it | 0 |
| R45-CL20 the scratch root fell back to `/tmp` | `tempfile.gettempdir()` was an accepted root | output: `scratch()` refuses a temporary partition and returns could-not-evaluate instead of degrading | 2 |
| R45-CL22 `--json-out ../../SKILL.md` overwrote the graded surface | the output path was trusted and written before the verdict | output: `out_path()` refuses any target inside the graded or frozen set and any path outside the lane root | 2 |
| R45-CL23 a newline or tab in a pathname is recorded C-quoted, killing the restored arm | `touched` compared quoted strings with real paths | commit: the history arm reads `--name-status -z`, so pathnames are not munged and the comparison is byte-exact | 1 |
| R45-CL24 the record drifted from the instrument it described | nothing bound the prose to the code | pin: the block carries the interpreter's sha256, so a prose claim and the bytes it describes cannot diverge silently | 1 |

  Refs: `corpus/lessons/round-45.md:142-176` (R45-CL13/CL14, the C1 and C2 defects), `corpus/lessons/round-45.md:90-101` (R45-CL6/CL7), `corpus/lessons/round-45.md:197-217` (R45-CL18/CL19), `corpus/lessons/round-45.md:212-231` (R45-CL20/CL22), `corpus/lessons/round-46.md:18-19` (M46-1/M46-2), `plans/round-46-claims.md:37-166` (the two predicates and the frozen set), `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` (a registered class set can hold while the surface is still shortcut-reachable — the reason a measure needs its own forgeries). S142 grounds the `--diff-merges=first-parent` arm (`corpus/lessons/round-46.md:27-31`).

- **24. An instrument's binding is an equality, not a containment, and its denominator is pinned.** <!-- exactness-table v3 --> Block 23 stated what makes a freeze claim checkable; this one states what makes a *check* exact — each row is a defect the round-46 non-author spot-check routed (`corpus/lessons/round-46.md:57-66`), the loose binding that let a forgery pass it, and the clause of `tools/round-47/exact.py` that now fails the forgery. Interpreter pin: `tools/round-47/exact.py` `interpreter_sha256:01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`; the counter's own mutation list is pinned as `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`. Source S143.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | containment over a lowercased cell, so any superstring passes | `symbol` | 1 |
| R46-CL3 a row claims a routed id another row already addresses | the id check asks whether the id appears in *some* row | `once` | 1 |
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | `forgeries_total` is compared with a number the code computes, and nothing pins the list | `digest` | 1 |
| R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice and blinds the arm | the argument order is a convention no clause reads | `order` | 1 |

  Refs: `corpus/lessons/round-46.md:57-66` (the four routed instrument defects this matrix closes), `corpus/lessons/round-46.md:21` (M46-2: a denominator the code computes is not a pinned denominator), `plans/round-47-claims.md:45-113` (the R47-C1 predicate and its nine clauses), `plans/round-47-claims.md:141-176` (the R47-C2 predicate and its result), `corpus/lessons/round-46.md:89-95` (R46-CL7: binding digits rather than meanings — routed again, because a verdict map is a registry concern and this block does not reach it), `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` (a registered class set can hold while the surface stays shortcut-reachable — the reason a clause needs a forgery that differs from the artefact, not a count of clauses). S143 grounds the equality (`https://docs.python.org/3/library/re.html` `re.fullmatch`).

- **25. A verdict map binds meanings, and a denominator is a floor.** <!-- verdict-meaning-table v1 --> Block 24 made a binding an equality; this one makes it a *meaning*. The round-48 lesson's S145 locates why a check that cannot fail is no check. Two HIGH defects the round-47 non-author spot-check routed (`corpus/lessons/round-47.md:36-44`), the loose binding that let each pass, and the clause of `tools/round-48/meanings.py` that now fails it. Interpreter pin: `tools/round-48/meanings.py` `interpreter_sha256:f5e5c35c59c33d2b5abe884b83c9739c20f180f7c6863133a4d880711122cf97`; the counter's own mutation list is pinned as `mutations_sha256:25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea` over `gold-meaning`, `swapped-meaning`, `duplicate-meaning` and `permuted-arm`, each digest covering the mutation's name **and its own source body** (a names-only digest cannot see a body edited to return the artefact unchanged).

| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R46-CL7 `0=banana; 1=nope; 2=whatever` satisfies the digit test | the verdict-map clause binds the digits 0/1/2, so any text after `=` passes | `meaning` | 1 |
| R47-CL10 four rows name the wrong arm for every routed defect and still pass | the arm test is membership and the routed-id test is at-least-once, so a permutation is green | `floor` | 1 |

  Refs: `corpus/lessons/round-47.md:36-44` (both routed defects as written), `corpus/lessons/round-46.md:89-95` (R46-CL7: binding digits rather than meanings), `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` (a registered class set can hold while the surface stays shortcut-reachable — the reason a row needs its meaning, not its digit), `plans/round-48-claims.md:47-96` (the R48-C1 predicate and every clause this block states), `plans/round-48-claims.md:98-120` (the R48-C2 predicate whose completeness floor this block's second arm mirrors), `corpus/lessons/round-48.md:8-20` (S145: the criterion used to reject a vacuous check), `tools/round-48/meanings.py`.

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

## Saved packet captures and frozen instruments — round 24

Use `corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md` (S064–S072).
The four REA6.5.0 packet-capture verbs need an absolute
`REA_TSHARK_COMMAND` (and `REA_CAPINFOS_COMMAND` for the `pcap` provider)
naming TShark 4.x; this host's launcher/library-digest-recorded local build is
`/home/vgpnk/.local/opt/wireshark-4.6.9/bin/` (`.ufo/waves/round-24/tool-pins.json`).
Without it every verb returns `capability_unavailable` (round-22 evidence), a
tool-absence refusal, never a traffic statement.

| Question about a saved capture | Verb and bounded decision |
|---|---|
| Which TShark/capinfos will REA use? | `inspect-pcap-client`: subject null, reports configured paths/sources/versions only |
| What is in this capture overall (endpoints, DNS, TLS SNI, HTTP URIs, protocol stacks)? | `inspect-pcap-capture <path>`: confidence `derived`; DNS answers are tied to one question per response packet; encryption/truncation hide layers; a pcapng with Decryption Secrets Blocks exposes decrypted layers without any lane key — say so |
| Which packets carry these exact fields? | `inspect-packet-capture <path> --fields a --fields b [--display_filter …] [--decode_as …]`: repeat `--fields` per field (a comma-joined value is an invalid field list); output is TShark dissector output under prlimit, missing fields mean absent output, a filtered result is not traffic absence |
| Does this installation know protocol/field X? | `inspect-packet-fields --kind fields --protocol X` (or `--kind protocols`, `--query`): registrations of the installed TShark, never traffic; Lua dissectors are absent in a Lua-off build |
| Live interface, `dumpcap`, keys supplied by the analyst | Adjacent/unheld — not this lane |

**Freeze the instrument before the claim (QUALITY33).** Commit every counting
script first, then freeze `claims.json` with an `instruments` map of sha256
pins; a later fix is appended to `instrument_supersessions` (path, commit,
reason) with a re-taken before record. Check with
`python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <LANE> --rev <REV> --require-clean round-<N> --disclosures corpus/claim-freezes.tsv`
and append the round's ledger row.

### Round-24 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round24-C1 | gate / kaidoku | `python3 -I -B .ufo/waves/round-24/tools/count-c1.py --root <LANE> --rev <REV>`; 0 c1_complete 4/4, 1 c1_incomplete, 2 unevaluable | post-hoc L1 `tools/selftest.py` (not a frozen independent oracle); BUILD selftest seats never spawned | Fixed BASE `fe10219e`, four T2 verbs, reviewed R22 binder digest, catalog/knowledge/SOURCES/R22–R23 evidence guards; reads Git objects only; temp dir only |
| round24-C2 | gate / kaidoku | `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <LANE> --rev <REV> --require-clean round-24 --disclosures corpus/claim-freezes.tsv`; 0 required freezes CLEAN and every freeze disclosed exactly, 1 otherwise, 2 unevaluable | none in the instrument | Reads Git objects only; finding codes NONE/UNRESOLVED/ABSENT/UNPINNED/PIN_MISMATCH/REVISED; supersession 1 at `9fb4eacd` disclosed |
| round24-producer | probe / kaidoku | `python3 .ufo/waves/round-24/tools/run-rea.py --out-dir <DIR> --name <N> [--tshark] -- <verb> …` writes `<N>.run.json` and byte-equal `<N>.envelope.json`; exit mirrors REA | — | refuses overwrite; records env overrides and TShark/capinfos digests |
| round24-repro | probe / kaidoku | `python3 -I -B .ufo/waves/round-24/repro/fetch-inputs.py --manifest .ufo/waves/round-24/repro/inputs.json --dest <DIR>`; 0 all match, 1 digest/size mismatch, 2 fetch/extraction/usage/containment error | — | official URLs, member + archive hashes/sizes; refuses duplicate ids and existing/symlink output paths; partial cleanup; use fresh destination after `--keep`; run2 and final-script controls separately byte-pinned |


## Explicit instrument-reference custody — round 25 prospective authority

Parent landed the fixed ruler and literal oracle at
`62feef9c0cbd5aadafa453456c55c28832175206` before a round-25 SRT or candidate.
This is an explicit caller-selected reference contract, not arbitrary-shell
discovery or historical admission. The ruler executes **the selected
candidate CLI only**, never audited instruments, carriers or fixture code.
The candidate `tools/round-25/instrument-custody.py` is not implemented at
this phase; missing candidate is unavailable2 and cases are not observed.

S073 supports the merge-base/cat-file primitives only. S074 separately
locates log/rev-list traversal, tree/mode fields and Git environment
semantics. Unique-first-add, equal unique-parent blob/mode, conservative
unsupported-history/nonregular decisions, exact-member and output-label
policies are declared API choices, not mandates or a correctness
certificate from those manuals. A source census is structural; it does
not validate every second/associated URL or quotation.

The exact prospective claims path is `.ufo/waves/round-25/claims.json`.
Only actual Main first-add F can establish discovery of a twelfth freeze.
The sole truthful FLAGGED ledger append follows actual final metadata
findings, preserving the old header/all11 rows. Literal QUALITY33 cyclic
debt stays unmet; original R24 frozen9/11 stays unmet, revised11/11 is
only disclosure agreement, and no require-clean R25 claim is made.

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round25-custody-ruler | gate, conformance limits disclosed / kaidoku | `python3 -I -B tools/round-25/ruler.py --root <LANE> --rev <FULL-MEASURED-COMMIT> --oracle-rev 62feef9c0cbd5aadafa453456c55c28832175206 --oracle-sha256 6c851cd704b84ef728415d674ad78ec7ff4da449883f1aeba3e4ca47631cd3e0 --work-parent <OWNED-FAST-SCRATCH-OUTSIDE-LANE>`; 0 original34 pairs exact, 1 observed pair mismatch, 2 unavailable/tampered/unsettled/root-state-change/unevaluable measurement | None exposed: separate gate-selftest conformance is not claimed | Ruler sha25620fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179b179acb6fda99d0532; original34/I immutable. Ruler0 is the finite score, not C1 success alone: separate Main-held contract/dataflow controls must also hold. Private scratch/stdout only; selected subject has explicit root/private cwd; no automatic restore/retry |


**Complete C1 contract, separate from its34 score.** First-add identity and
ancestry/at-or-before constraints, identical regular blob **and mode** in
the unique freeze parent, nonregular/readded-history handling, duplicate
and unknown-member rejection, direct candidate Git-environment isolation,
and scope/useful output evidence remain load-bearing. Main-held controls
are frozen in `corpus/evidence/round-25/main-held-contract-controls.json`;
they are reported separately, never folded into or substituted for34.

**Non-tautology.** Even34/34 fails C1 if the subject uses oracle/test/ruler/
gate/fixture content as decision logic, expected answers, imports or
execution, or embeds case-keyed answer tables. An explicitly caller-selected
grammar-valid instrument Git blob may be read opaquely for raw identity,
hash, mode and history, including a ruler/gate/test-helper when selected;
its semantics are never imported, executed or interpreted. Main reviews
actual Git dataflow and held consumer outcomes, not a source-word test.

**Measurement limits.** Main must quiesce shared worktrees and jj/ref/index
writers. Root lstat/index/ref snapshots attest named instants only, not
continuous/all-content/object-store immutability, global absence or
containment. A guard/resource/setup abort is CNE, not an observed candidate
failure; no weakening the guard, automatic rerun or empty-receipt masking.
Main alone controls final execution and admission.


## Superseding note — round 25 custody subject landed; the filed wording above is superseded

This note is appended after the round 25 section above and changes no filed byte
of that section. The section above was written at the claims freeze commit
`a4ab912a956fb863fedb0e9b9bb866777af27495`, when the subject
`tools/round-25/instrument-custody.py` did not exist. Its sentence stating that
the candidate is not implemented at this phase, that a missing candidate gives
an unavailable verdict with exit 2, and that the cases are therefore not
observed, described that moment. It is superseded from commit
`fafdd283432731a675b71e201bb9ba767c394553` onward.

What landed. Commit `fafdd283432731a675b71e201bb9ba767c394553` (parent
`a4ab912a956fb863fedb0e9b9bb866777af27495`) added one file,
`tools/round-25/instrument-custody.py`: 514 lines, 21190 bytes, sha256
`54c43cdc01930fcb58f14053d8099f4b28352147656a05d811574cc74e7d34fb`, blob
`8a6e21f18e805c7ce44e03a9a4872e9063073c32`, mode 100755. The same blob is at
the current lane tip. The fixed ruler and the 34 literal pairs are unchanged:
the ruler sha256 at the tip is
`20fe3f3d3d68ba21c8d8bbfed175bb57db46a8618bd179b179acb6fda99d0532`, and the
cases sha256 at `62feef9c0cbd5aadafa453456c55c28832175206` is
`6c851cd704b84ef728415d674ad78ec7ff4da449883f1aeba3e4ca47631cd3e0`. The
registry row `round25-custody-ruler` above therefore keeps its entry, its exit
map and its pinned digests unchanged.

The claim was not continued. The attempt 1 calibration claim R25-C1 in
`.ufo/waves/round-25/claims.json`, the explicit caller selected 34 case
custody contract, was not continued and has no after value in this lane. The
lane's own wording is "not pursued, not as met"
(`corpus/lessons/round-25.md`, the "Attempt 3" heading, lines 361 to 364, and
`SCORECARD.md` line 3050). The freeze ledger row for round 25 is FLAGGED with
the findings INSTRUMENT_ABSENT and INSTRUMENT_REVISED, the latter naming
`fafdd283` (`corpus/claim-freezes.tsv` line 13; receipt
`corpus/evidence/round-25/a3/after/freeze-gate-at-1e064f9b.json`).

One outside measurement exists and is not a lane receipt. The ruler was run over
the subject at commit `fafdd283432731a675b71e201bb9ba767c394553` and recorded
exit 0, 34 of 34 exact, finding `all_declared_pairs_exact`, at
2026-10-22T03:28:48Z. That receipt lives outside this lane, in the fleet
repository at `.ufo/waves/hyaku/kaidoku25-prerequisite/parent-after-process.json`,
sha256 `d15f5581a6e968121cb9963a561a95421e24a871842dd5829acb994a7d64a958`. Its
own authority record states that admission is false. It is not a claim of this
lane, so no axis score, no admission and no custody conclusion follows here.

Wording on the two records above. "Not implemented at this phase" was true at
the freeze and is false at the tip. The round 25 verifier spot check calls the
claim abandoned; no committed lane record contains a retirement decision, and
the lane's committed records say the claim was not continued and was reported
as not pursued, not as met. Use the lane's wording.

## Evidence-ID identity per verb at a named pin — round 26

This section supersedes, for the verbs it names, the two-class reading of the craft rule
"Evidence ids are content-addressed per verb family" (`SKILL.md:86-107`): there is a third class,
path-sensitive, and an id held "byte-exact across a day" (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`,
an `inspect-binary-layout` id on `/usr/bin/jq`) re-derives only at the same path. Source:
`corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` (table
`corpus/evidence/round-26/c1/table.tsv`; S079 for the minting rule).

| verb at `rea-agents@6.5.0` (carrier `/usr/bin/jq`) | id class | to show two envelopes came from the same bytes and request |
|---|---|---|
| `analyze`, `inspect` (one operation, `binary_overview`; same id for both) | content-keyed across directories | compare ids; read `.meta.command` to tell the two verbs apart |
| `decompile`, `xrefs`, `read-bytes`, `function`, `instructions` | content-keyed across directories | compare ids |
| `inspect-binary-layout` | path-sensitive (path in `parameters.path`, `normalized_result.artifact.path`, a location) | compare `.data.subject.digest.sha256` (the verb's only parameter is the path); an id match also proves the same path |

Decision rules:

- Compare ids only within one pin and one Ghidra build: 6.5.0 and 6.7.0 mint different ids for the
  same bytes and request (`relationship_coverage` in the 6.7.0 projection; measured live for
  `analyze`, `function` and `inspect-binary-layout`), and the observed Ghidra version is inside the
  hashed provider identity.
- A different id on a same-path repeat is a real provider difference, not a path effect: round 17
  saw one on `/usr/bin/aether` (`analyze`, `string_count` 29118 → 29117,
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:116-122`). Content-keyed means the path is not
  hashed; it does not promise the provider is deterministic on every carrier.
- Recompute an id offline with `python3 -I -B tools/round-26/recompute-ids.py <envelope>` before
  trusting it; a match shows the envelope's hashed fields are intact, not that the run was the
  one claimed (`.meta.command` and the call record say that).

## Evidence-ID identity under a renamed copy and on a second carrier — round 27

This section narrows the round-26 table above for `analyze` and `inspect`: they are
content-keyed across directories only while the file extension class stays the same. Source:
`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` (table
`corpus/evidence/round-27/c1/table.tsv`, carriers `/usr/bin/jq` and `/usr/bin/tinyxxd` (S082);
mechanism in the 6.5.0 package, S079 family, `dist/ghidra/GhidraTargetSnapshot.js:13-14`, `:76-78`).

| verb at `rea-agents@6.5.0`, same bytes at two paths | id across a copy with another directory, name and extension | what decides it |
|---|---|---|
| `decompile`, `xrefs`, `read-bytes`, `function`, `instructions` | equal on both carriers | no hashed field carries the path, name or extension |
| `analyze`, `inspect` | differs when the extension class differs (`.dat` against none) | `normalized_result.document` is the Ghidra program name `target-<sha256[0:12]><suffix>`; suffix = the extension if it matches `^\.[A-Za-z0-9]{1,12}$`, else `.bin` |
| `inspect-binary-layout` | differs whenever the path string differs | the path is hashed in three places |

Decision rules:

- Before comparing `analyze` or `inspect` ids of one file stored under two names, map each name's
  extension through the suffix rule; if the suffixes differ, compare `.data.subject.digest.sha256`
  instead. A differing `normalized_result.document` suffix explains the id change; do not report
  it as a content change.
- When collecting carriers for an identity table, never rename a copy's extension unless the
  extension is the variable under test; the round-26 directory-only control kept the name `jq`.
- A frozen counter that refuses duplicate envelope bytes must allow two genuine runs that return
  byte-identical envelopes: a fast verb can repeat `meta.duration` to the millisecond (tinyxxd
  `inspect-binary-layout`, `132ms` twice; lesson M27-2 in `corpus/lessons/round-27.md`).

### Round-27 falsify-wave corrections to the section above (appended)

- The suffix is taken from the target path after `realpath` on Linux (`dist/cli-runtime/binary-BVOr2mgE.js:293`, `:5261`, `:5318` in the 6.5.0 package), so a symlink's own extension does not count; Windows uses the typed path. The rule is case-sensitive (`.dat` and `.DAT` differ). Both read from the code, not run (`.ufo/waves/round-27/w2/CriticEntryMechanism.md`, `CriticSkillTable.md`).
- "Extension class" means the snapshot suffix after the rule: the extension if it matches `^\.[A-Za-z0-9]{1,12}$`, else `.bin`. No extension and `.bin` give one suffix. Live: a 13-character extension gave `.bin` and the base id; `.dat` gave the renamed id; a name-only copy kept the base id (`FalsifySuffixMapping.md`, `FalsifyExtensionOnly.md`).
- The address-verb row holds only for extensions that do not change the route: `.js`, `.mjs`, `.cjs`, `.map`, `.plist`, `.asar`, `.hop`, and ZIP bytes named `.zip`, `.ipa`, `.apk` or `.app` change `subject.format` or the provider (read from the code, not run).
- `inspect-binary-layout` hashes the normalized absolute path, without following symlinks: `/usr/bin/../bin/jq` and `/usr/bin/jq` should give one id (read from the code, not run).
- Limits of the section: Ghidra provider, CLI, Linux, two carriers, `rea-agents@6.5.0`.
- The third decision rule above is a counter-design rule; QUALITY row 40 states it in full. Note that the call-record fields that tell two genuine runs apart (`utc_start`, seat) are written by the seat, so they separate an honest tie from a copy only as far as the seat is trusted.
- `SKILL.md:411-412` and the round-26 table row at `:894` ("content-keyed across directories" for `analyze`, `inspect`) hold only when both paths map to the same suffix.

### Round-27/28 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round27-C1 | gate / kaidoku | `python3 -I -B tools/round-27/c1-rename-identity.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 rows_complete=16/16 and entry_ok=1, 1 otherwise (each incomplete pair prints INCOMPLETE with reasons), 2 input error. Reads Git objects at --rev only; per row, base/repeat/renamed envelopes re-derive the verdict (unstable if base != repeat, content-keyed if renamed == base, else rename-sensitive) | `python3 -I -B tools/round-27/c1-rename-identity.py --selftest` (no --root/--rev): builds a green fixture plus 21 red mutations as private scratch repos, 22 cases; 0 all pass, 1 any failure. Green at tip (selftest cases=22 failures=0, exit 0, 2026-10-22T18:28Z); freeze receipt `.ufo/waves/round-27/before/c1-selftest.txt` | Counter sha256 e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7 (`.ufo/waves/round-27/claims.json` instruments; unchanged since freeze commit a4f674b3). Frozen carriers jq e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806, tinyxxd 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65; package pin 6.5.0 + package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Loads `tools/round-26/recompute-ids.py` at REV unpinned (INSTRUMENT_UNPINNED, routed defect 4). Refuses runs started or files first committed before the counter commit. Git reads only; selftest writes removed scratch clones |
| round27-C2 | gate / kaidoku | `python3 -I -B tools/round-27/c2-xpin-check.py --root <LANE> --rev <REV> [--base <BASE>] [--tool-cmd <CMD>]`; 0 r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1, 1 otherwise, 2 input error (including changed or missing installed package files it verifies). Runs the tool under node on the 24 round-26 envelopes plus 3 generated red envelopes; recomputes both pins independently (6.5.0 rule via `tools/round-26/recompute-ids.py`, 6.7.0 rule from the installed package) | `python3 -I -B tools/round-27/c2-xpin-check.py --selftest`: 4 stub-mode cases + tool-absent-at-base + capability/source rows fixture, 6 cases; 0 all pass, 1 any failure. **Red at tip**: `correct-stub` expects exit 1 but measure now returns 0 once the capability and source rows exist (selftest cases=6 failures=1, exit 1, 2026-10-22T18:28Z; routed defect 2 — re-anchor pending, seat ExecR27SelftestFix). Freeze receipt `.ufo/waves/round-27/before/c2-selftest.txt` was green (6 cases, 0 failures) | Counter sha256 d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3 (`.ufo/waves/round-27/claims.json` instruments). FROZEN_FILES pin installed package bytes: 6.5.0 package.json a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c, 6.5.0 dist/domain/evidence.js f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff, 6.7.0 package.json 3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570, 6.7.0 dist/domain/evidence.js a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb. Git reads only; tool runs in a private scratch dir, no lane writes |
| round28-C1 | gate / kaidoku | `python3 -I -B tools/round-28/c1-heldout-naming.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 runs_ok=61/61 rows_complete=187/187 tally_equal=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 a pinned input absent or differing. Reads Git objects at --rev only, never network or REA. Also `--emit-tally` (recompute the tally from the working tree; L1 use, not a verdict). Byte-identical lookup bodies across selectors are legitimate: responses are keyed by manifest entry, not by bytes | `python3 -I -B tools/round-28/c1-heldout-naming.py --selftest`: 19 listed cases + planted-wrong-name check + pin refusal, 21 cases in private temp repos; 0 all pass, 1 any failure. Green at tip (selftest cases=21 failures=0, exit 0, 2026-10-22T18:28Z); freeze receipt `.ufo/waves/round-28/before/c1-selftest.txt` | Counter sha256 29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c (`.ufo/waves/round-28/claims.json` instruments). Every input it loads is pinned in PINS and `loaded_by_counter`: resolver `tools/round-25/a2/resolve-selectors.py` 4be915668ea20a643d04c9b8ae3c83bc9f5fd1b4d8821e06cabdccce36b3c23d, `corpus/evidence/round-28/c1/carriers.tsv` 4392b5c377cc2e343d385ba3b93206a0bb67df972bdc3814780819f1d4c5e71f, `heldout.tsv` 423654f9d71feb417725a1e5a290b1e028ee53ad628141281a8c08391dab6cef; package pin 6.5.0 + a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Refuses runs/lookups from before the counter commit. Git reads only; selftest writes private temp dirs |
| round28-C2 | gate / kaidoku | `python3 -I -B tools/round-28/c2-filtered-flag.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 responses_complete=230/230 entries>=1 mismatches=0 predicted_true>=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 pin failure. Reads Git objects at --rev only; a non-boolean `filtered` counts as a mismatch and both branches must be exercised | `python3 -I -B tools/round-28/c2-filtered-flag.py --selftest`: 16 listed cases + pin refusal, 17 cases in private temp repos; 0 all pass, 1 any failure. Green at tip (selftest cases=17 failures=0, exit 0, 2026-10-22T18:28Z); freeze receipt `.ufo/waves/round-28/before/c2-selftest.txt` | Counter sha256 4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef (`.ufo/waves/round-28/claims-c2.json` instruments). Pinned inputs: `corpus/evidence/round-28/c2/selectors.tsv` ad1b50982922ed69f6953b490716746adb5d5587c4395d29489b1db7fab464ae, `canonical-signatures.json` 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2 (`loaded_by_counter`). Refuses responses fetched or files first committed before the counter commit. Git reads only; selftest writes private temp dirs |

### Round-29 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round29-C1 | gate / kaidoku | `python3 -I -B tools/round-29/c1-fresh-naming.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 a pinned input absent or differing. The round-28 C1 counter with round-29 paths, pins and target; entry_ok needs the claim's own row S088 on the entry's `source:` line (QUALITY row 45). Also `--emit-tally` (L1 use, not a verdict). Docstring lines 14 and 27 still name round-28 evidence paths; the code reads round 29's | `python3 -I -B tools/round-29/c1-fresh-naming.py --selftest`: 22 cases incl. `red-cites-other-new-row` and pin refusal; 0 all pass, 1 any failure. Green (cases=22 failures=0) at freeze `.ufo/waves/round-29/before/c1-selftest.txt` and at `18be864a` (`after/c1-selftest.txt`). Mutation: 4 of 8 mutants survive (`.ufo/waves/round-29/w1/MutC1Counter.md`) | Counter sha256 6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda (`.ufo/waves/round-29/claims.json` instruments); loads the round-25 resolver 4be91566…, carriers.tsv 94438ede…, heldout.tsv 2db9e658…; REA pin rea-agents 6.5.0, package.json a5003023…; writes only private temp dirs |
| round29-C2 | gate / kaidoku | `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 responses_complete=178/178 entries>=1 mismatches=0 predicted_true>=1 predicted_false>=1 entry_ok=1, 1 otherwise, 2 pin failure. Rule from S084/S087 `filterResponse`; a key with no `signature` filters every candidate; entry_ok needs row S087. `predicted_true` is computed from names and the list, so only `mismatches` tests the rule | `python3 -I -B tools/round-29/c2-filtered-unseen.py --selftest`: 19 cases incl. `red-cites-other-new-row`, `red-no-false-branch`, pin refusal. Green at freeze (`before/c2-selftest.txt`) and at `18be864a`. Mutation: a case-insensitive name compare survives (`w1/MutC2Counter.md`) | Counter sha256 00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801; loads selectors.tsv 3a93f783…, canonical-signatures.json 5572beb5…; writes only private temp dirs |
| round29-freeze | gate / kaidoku (hygiene; QUALITY row 46) | `python3 -I -B tools/round-29/freeze-gate.py --root <LANE> --rev <REV> [--require-clean round-N]... [--disclosures corpus/claim-freezes-v2.tsv]`: the round-24 gate over every `.ufo/waves/round-*/claims*.json` (key `round-N` or `round-N/<file>`), reading `instruments`, `loaded_by_counter` and `producers_not_counters` as pins; 0 when required freezes are CLEAN and the ledger agrees exactly, 1 otherwise, 2 unevaluable. `--require-clean round-29` is red (M29-3) | none in the instrument. Behaviour shown by `w1/ExecGateV2.md` (fixture with an unpinned `claims-x.json`); 3 of 4 mutants killed by the ledger check, a sort-key mutant survives (`w1/MutFreezeGateV2.md`) | sha256 25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2 (pinned here only; no claims file pins it); reads Git objects only |
| round29-prefile | check / kaidoku (hygiene; QUALITY row 47) | `sh tools/round-29/prefile-check.sh <LANE>`: 0 `prefile: PASS` when `git status --porcelain` is empty (run with GIT_OPTIONAL_LOCKS=0) and both freeze gates exit 0 with `--disclosures` at HEAD; 1 `prefile: FAIL` with each failing step; 2 usage or unreadable tree. Cannot see a still-running seat | none in the instrument. Red on clean clones at the round-26/27/28 filing commits (`.ufo/waves/round-29/after/prefile-gate-at-filings.txt`); tree-step cases in `w1/ExecPrefile.md`; an untracked-file omission mutant is caught only by an untracked-only probe (`w1/MutPrefile.md`) | sha256 5c3586b277e16b7c43ae32a4160643442f6b9612b7e2d74cd6e76c12c688cdd9; read-only |

## Rust dependency metadata (`inspect-rust-binary`) — round 30

Held on the positive class (an image with one cargo-auditable `.dep-v0` section) for ELF, PE and thin Mach-O at `rea-agents@6.5.0`: the full package graph equals an independent decode on 16 uv 0.13.0 carriers (`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`). Refusal signatures below were predicted from the 6.5.0 code (S090) and observed live on 19 ELF x86_64 mutants (`corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`). Read `error.details.issues` as well as `error.message`: for `invalid_request` refusals the message field is generic. The reader message is prefixed `Selected artifact <path>: `, so match it as a substring.

Decision table for `inspect-rust-binary` refusals (evidence `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`, 19 of 19 predictions observed live):

| Input condition | REA 6.5.0 outcome | error code (observed) | Threshold / gate |
|---|---|---|---|
| original section bytes moved to a 16-aligned offset at EOF (sh_offset/sh_size patched) | accepted, packages equal | ok | section may sit anywhere in the file |
| same JSON re-compressed with zlib level 9, at EOF | accepted, packages equal | ok | any complete zlib stream |
| `root` removed from every package, at EOF | accepted, packages equal | ok | zero roots allowed; `root_package_index: null` |
| sh_size = 0 | refused: `Dependency section is not file-backed` | invalid_request | size must be > 0 |
| sh_type = SHT_NOBITS (8) | refused: `Dependency section is not file-backed` | invalid_request | SHT_NOBITS is not file-backed |
| sh_flags OR SHF_COMPRESSED (0x800) | refused: `Compressed dependency sections are unsupported` | unsupported_target | SHF_COMPRESSED (0x800) refused |
| `.comment` header renamed to `.dep-v0` (two sections) | refused: `Image contains more than one dependency section` | invalid_request | at most one `.dep-v0` (none gives ok with `auditable_metadata: null`, code-read `RustBinaryImage.js:45-49`) |
| section replaced by 9,870 patterned non-zlib bytes | refused: `Dependency section is not a complete zlib stream` | invalid_request | complete zlib stream |
| original stream + 4 trailing bytes | refused: `Dependency section is not a complete zlib stream` | invalid_request | no bytes after the stream (node v24.21.0 rejects trailing junk) |
| 1,048,577-byte section | refused: `Dependency section exceeds the 1 MiB compressed limit` | resource_constraint | 1 MiB compressed section |
| JSON padded with 3 MiB of spaces (14,009 compressed bytes, inflate bound 896,576) | refused: `Inflated dependency JSON exceeds the size limit` | resource_constraint | inflated ≤ min(8 MiB, 64 × section bytes) |
| zlib(`ff fe fd`) | refused: `Dependency JSON is not valid UTF-8` | invalid_request | UTF-8 |
| zlib(`{"packages":[`) | refused: `Dependency section JSON is invalid` | invalid_request | valid JSON |
| zlib(33 `[` + 33 `]`) | refused: `Dependency JSON nesting exceeds 32 levels` | invalid_request | nesting ≤ 32 |
| zlib(`{"format":-1,"packages":[]}`) | refused: `Dependency JSON does not match the format schema` | invalid_request | `format` a non-negative integer |
| package 0 gains `features: []` | refused: `Dependency package 0 does not match the package schema` | invalid_request | package keys only name/version/source/kind/dependencies/root |
| package 0 `kind` = `dev` | refused: `Dependency package 0 does not match the package schema` | invalid_request | `kind` only `runtime` or `build` |
| package 463 already root; package 0 also `root: true` | refused: `Dependency JSON declares more than one root package` | invalid_request | at most one root |
| package 0 gains dependency index 584 (= package count) | refused: `Dependency index 584 from package 0 is outside the package list` | invalid_request | every dependency index < package count |

Limits: one ELF x86_64 base carrier for the refusals; one pin (npx cache path `~/.npm/_npx/ad9a3fdbcad992c6`); node v24.21.0; messages are substrings of `error.details.issues[0].message`, `error.message` or `error.details.reason`; shared-message pairs (empty/NOBITS, not-zlib/trailing, extra-field/kind-dev) do not prove which branch fired; the 256 MiB input cap, the 8 MiB absolute inflate cap and the 8 MiB report budget are code-read only. "Packages equal" means equal to the oracle's reading of the same mutant. A green run says the embedded list was read faithfully, not that it is true (REA limitation text). Counter: `tools/round-30/c2-rust-refusals.py` (`inspect-rust-binary`, positive class counter `tools/round-30/c1-rust-positive.py`).

### Round-30 measurement registry

| tool | purpose | command | exit codes | selftest |
|---|---|---|---|---|
| `tools/round-30/c1-rust-positive.py` | R30-C1 counter: live `inspect-rust-binary` vs the independent oracle on 16 carriers, committed-envelope agreement, entry/PROVINCE gates | `python3 -I -B tools/round-30/c1-rust-positive.py --root <LANE> --rev <REV>` | 0 target met, 1 measured not met, 2 carrier list or carrier pin absent/altered (a missing REA `package.json` crashes with exit 1; only its version string is compared) | `--selftest` 25 cases |
| `tools/round-30/c2-rust-refusals.py` | R30-C2 counter and deterministic mutant builder (`--build`) | `python3 -I -B tools/round-30/c2-rust-refusals.py --root <LANE> --rev <REV>` (one at a time: measure mode rewrites the shared mutants under `/fast/scratch/hyaku/kaidoku-r30/mutants/`) | 0/1/2, except an altered base carrier prints `PIN base carrier altered` with exit 1 | `--selftest` 16 cases |
| `tools/round-30/rust_dep_oracle.py` | independent `.dep-v0` reader (ELF/PE/Mach-O section tables, zlib, json); no REA code | imported by both counters | — | none (checked against llvm-readobj on 16 carriers, w1 `RevOracleVsReadobj.md`) |
| `tools/round-30/axis-fit-gate.py` | M30-1 fix: coverage/depth claims need `surface`, `unmoved_command` and control receipts committed before the first envelope | `python3 -I -B tools/round-30/axis-fit-gate.py --root <LANE> --round <N> --rev <REV>` | 0 pass, 1 findings, 2 unreadable | `--selftest` 18 cases; round 29 exit 1 |
| `tools/round-30/prefreeze-gate.py` | routed defect 3 (M29-3): pins present at the freeze, no data at or before it, no named-but-unpinned tool | `python3 -I -B tools/round-30/prefreeze-gate.py --root <LANE> --round <N>` | 0/1/2 | `--selftest` 20 cases; round 29 exit 1 before the M29-3 disclosure (`a6e7d9ce`), exit 0 (CLEAN) from `004053d6` |
| `tools/round-30/settle-gate.py` | routed defect 4 (M29-1): every registry seat has a settle-ledger row and returned reports are unchanged since settling | `python3 -I -B tools/round-30/settle-gate.py --root <LANE> --round <N>` | 0/1/2 | `--selftest` 13 cases; round 29 exit 1 |


## SQLite databases (`inspect-sqlite-database`) — round 31

Held at `rea-agents@6.5.0` on published files at scope `database` (`corpus/knowledge/2026-10-23-r31-sqlite-positive.md`). Decision table for `inspect-sqlite-database` refusals and edge cases (evidence `corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`; 23 of 23 predicted from the 6.5.0 code before the runs and observed live). Every refusal exits 1 with `error.category: invalid_input` and exactly one `details.issues` entry; `<path>` is the requested path.

| request id | input condition | outcome code | issue path / reason | message or result |
|---|---|---|---|---|
| `q-rowlimit-no-table` | `--row-limit 5` without `--table` (chinook) | invalid_request | `row_limit` / invalid_value | row_limit requires an explicit table selection |
| `q-columns-no-table` | `--column Name` without `--table` | invalid_request | `columns` / invalid_value | columns requires an explicit table selection |
| `q-scope-no-table` | `--schema-scope selected_table` without `--table` | invalid_request | `schema_scope` / invalid_value | selected_table schema scope requires table |
| `q-missing-table` | `--table NoSuchTable` (absent) | invalid_request | `table` / invalid_format | Selected ordinary table does not exist with that exact name: NoSuchTable |
| `q-case-table` | `--table album` (table is `Album`; exact-name lookup, no case folding) | invalid_request | `table` / invalid_format | Selected ordinary table does not exist with that exact name: album |
| `q-view-as-table` | `--table coordinate_operation_view` (a view, proj-371) | invalid_request | `table` / invalid_format | Selected ordinary table does not exist with that exact name: coordinate_operation_view |
| `q-missing-column` | `--table Album --column Nope` | invalid_request | `columns` / invalid_format | Selected column does not exist with that exact name in table Album: Nope |
| `q-virtual-rows` | `--table rtree_curve_geometry` (R*Tree virtual table, gpkg-curve) | invalid_request | `table` / invalid_format | Rows from virtual table rtree_curve_geometry are outside the ordinary-table inspection profile. |
| `q-shadow-rows` | `--table rtree_curve_geometry_node` (R*Tree shadow table) | invalid_request | `table` / invalid_format | Rows from shadow table rtree_curve_geometry_node are outside the ordinary-table inspection profile. |
| `q-ok-rows` | `--table Album --row-limit 3` | accept | — | 3 Album rows, columns AlbumId, Title, ArtistId; order unspecified |
| `m-missing` | path does not exist (parent directory exists) | invalid_request | `path` / invalid_value | Selected SQLite database does not exist: <path> |
| `m-enotdir` | a path component is a regular file | invalid_request | `path` / invalid_value | Selected database file set could not be read (ENOTDIR): <path> |
| `m-not-sqlite` | first 16 header bytes zeroed | invalid_request | `path` / invalid_format | file is not a database |
| `m-bad-pagesize` | header page size 768 (not a power of two) | invalid_request | `path` / invalid_format | file is not a database |
| `m-journal-hot` | sibling `-journal` with a nonzero 28-byte header | invalid_request | `path` / invalid_format | Rollback journal may require recovery: <path>-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported. |
| `m-journal-short` | sibling `-journal` of 10 zero bytes | invalid_request | `path` / invalid_format | Rollback journal may require recovery: <path>-journal. Supply a clean offline snapshot; only empty journals or a fully zeroed header are supported. |
| `m-journal-empty` | sibling empty `-journal` | accept | — | full schema, equal to the oracle; the journal is not copied |
| `m-journal-zero28` | sibling `-journal` of 28 zero bytes | accept | — | full schema, equal to the oracle; the journal is not copied |
| `m-journal-symlink` | sibling `-journal` is a symlink | invalid_request | `path` / invalid_format | Expected a regular journal without a symlink: <path>-journal |
| `m-db-symlink` | the database path is a symlink to a valid database | invalid_request | `path` / invalid_format | Expected a regular file without a symlink: <path> |
| `m-directory` | the database path is a directory | invalid_request | `path` / invalid_format | Expected a regular file without a symlink: <path> |
| `m-over-256mib` | sparse database of 268,435,457 bytes | invalid_request | `path` / out_of_range | Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: <path> |
| `m-wal-over` | 1,067,008-byte database + sparse `-wal` of 267,368,449 bytes (sum = budget + 1) | invalid_request | `path` / out_of_range | Selected SQLite database and WAL exceed the combined 268435456-byte snapshot budget: <path> |

How to use it: check option dependencies first (row limit, columns and `selected_table` need `--table`); give the exact table name (no case folding; a view name is reported as a missing table); expect virtual and shadow tables to be listed but refused for rows; inspect a copy without its journal if the journal is not empty; never pass a symlink. At `rea-agents@6.7.0` the 256 MiB budget refusal was observed as `resource_constraint` for `m-over-256mib` and `m-wal-over`; `m-journal-hot` was also run, but the other 20 requests were not re-run at that pin (`.ufo/waves/round-31/w2/ProbePin670.md`). This corrects the earlier “static reading, not run” wording.

### Round-31 measurement registry

| tool | purpose | command | exit codes | selftest |
|---|---|---|---|---|
| `tools/round-31/c1-sqlite-positive.py` | R31-C1 counter: live `inspect-sqlite-database --schema-scope database` vs the independent oracle on 12 carriers, full committed-envelope equality, entry and Core-placement gates | `python3 -I -B tools/round-31/c1-sqlite-positive.py --root <LANE> --rev <REV>` | 0 target met, 1 not met, 2 carrier list or carrier pin absent/altered. `--write-evidence` skips the committed-record clause and is never a receipt | `--selftest` 14 cases |
| `tools/round-31/c2-sqlite-refusals.py` | R31-C2 counter (23 frozen predictions, full-envelope committed check) and mutant builder (`--build`) | `python3 -I -B tools/round-31/c2-sqlite-refusals.py --root <LANE> --rev <REV>` | 0/1/2 (2 also for an altered mutant or sibling journal/WAL pin) | `--selftest` 12 cases |
| `tools/round-31/sqlite_oracle.py` | independent SQLite schema reader: pure-Python `sqlite_schema` b-tree parser plus libsqlite3 PRAGMAs | imported by both counters; `python3 -I -B tools/round-31/sqlite_oracle.py <files>` prints counts | — | none (mutation: wave-1 `MutOracle.md`, 8 of 12 killed) |
| `tools/round-31/freeze-integrity.py` | M31-2 fix: pinned inputs at `--rev` equal the freeze-commit digests and are untouched after the freeze | `python3 -I -B tools/round-31/freeze-integrity.py --root <LANE> --round <N> --rev <REV>` | 0 CLEAN, 1 FAIL, 2 no freeze commit | none; shown able to fail on the wave-1 amended-predictions clone (exit 1) |
| `tools/round-31/cited-runs-gate.py` | routed defect 1 (round 30): every gate/counter result a report asserts cites a committed receipt that contains it | `python3 -I -B tools/round-31/cited-runs-gate.py --report <report.md> --lane <LANE> --rev <REV>` | 0 all backed, 1 UNCITED/UNBACKED findings, 2 usage | `--selftest` 17 cases; round-30 report exit 1 |

## ARM64X hybrid PE — round 32 native-view boundary

Source definitions: S099 (Microsoft Arm64X documentation, hybrid content/default Arm64 appearance), S098 (LLVM 23.1.3 load-config inputs). Observed envelopes and twelve Evidence IDs: `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md`, `corpus/evidence/round-32/c1/`.

| Condition | Decision |
|---|---|
| Raw COFF machine 0xAA64 | Insufficient to separate plain ARM64 and ARM64X. Read CHPE metadata/code-map ranges as well; LLVM's displayed ARM64X machine label is not the raw field. |
| Frozen carrier has declared ARM64 and ARM64EC map ranges | REA 6.5.0 `inspect <path> --format json --full-output` exercises its native-view overview. This metadata classifier is not proof of valid instruction/ABI content or Windows loading. |
| Need the EC view | Do not infer it from native procedure counts: k05 reports one procedure despite four EC exports. Dual-view recovery/decompilation stays Frontier. |
| Need the demonstrated native view | Pin the DLL hash, retain original envelopes and per-call argv/package identity, compare ordered segment fields and native-export procedure counts, then require whole committed/live equality except `meta`. |
| Need internal-function counts, published hybrids or runtime behavior | Untested by these twelve synthetic exported-leaf DLLs; no holding is inferred. |

Reader environment: pass the existing `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` and `JAVA_HOME=/usr/lib/jvm/java-21-openjdk` explicitly when the child environment lacks them. Provider-unavailable control runs do not exercise committed-envelope discrimination.

### Round-32 instrument registry

| name | kind | entry command | verdict map | selftest | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| ARM64X positive counter | gate | `python3 -I -B tools/round-32/c1-arm64x-positive.py --root <LANE> --rev <REV>` | 0 clean/target met; 1 failed; 2 could-not-evaluate (pins); 3 could-not-evaluate (write mode, never a receipt); uncaught errors are could-not-evaluate, not a predicate result | same command `--selftest`, 18 cases | `.ufo/waves/round-32/claims.json`; carriers.tsv/predictions.tsv | read-only measure; `--write-evidence` writes round-32 c1 envelopes/runs in the selected root | kaidoku |
| Capability calibration v3 | gate, **falsified semantic measure** | `python3 -I -B tools/round-32/c2-capability-calibration-v3.py --root <LANE> --rev <REV>` | 0 lexical target met only, not semantic calibration; 1 failed; 2 could-not-evaluate (pins/statement coverage) | `--selftest`, 18 cases | `.ufo/waves/round-32/claims-v3.json`; fleet pin cef00867 | read-only | kaidoku |
| Superseded capability v1/v2 | historical gates, not active claims | `python3 -I -B tools/round-32/c2-capability-calibration.py --root <LANE> --rev <REV>`; corresponding `-v2.py` | 0 clean under superseded predicate; 1 failed; 2 could-not-evaluate | `--selftest` | claims.json / claims-v2.json | read-only | kaidoku |
| ARM64X byte oracle | probe | `python3 -I -B tools/round-32/arm64x_oracle.py <DLL>` | 0 report produced; exceptions/nonzero could-not-evaluate; not a capability verdict | none; independent reader/build witnesses retained in a2audit | claims.json input/oracle hashes | read-only | kaidoku |
| Carrier builder | probe | `bash tools/round-32/build-arm64x-carriers.sh <LANE> <NEW-OUTPUT>` | 0 build completed; nonzero could-not-evaluate; compare hashes separately | no selftest; independent rebuild in `A2BuildRecheck.md` | claims.json inputs and carriers.tsv | selected new scratch output only, never pinned originals | kaidoku |
| Freeze integrity, selectable claims | gate | `python3 -I -B tools/round-32/freeze-integrity.py --root <LANE> --round 32 --rev <REV> --claims .ufo/waves/round-32/claims.json` (also claims-v2/v3) | 0 clean; 1 failed; 2 could-not-evaluate (no freeze) | no self-invocation mode; inherited gate-conformance limitation, not selftest credit | each selected claims file at its first-add commit | read-only | kaidoku |

C2's negative-assessment and vocabulary-bag controls both meet its unchanged target. The round stops honestly on C2; summary restoration is useful maintenance, not a verified calibration improvement. Source S100 is rejected only as authority for CHPE offset/tag fields absent from the PE Format specification.

Retained secondary witness: `.ufo/waves/round-32/independent-pe/pe_indep.py` is a read-only PE decode probe (entry: `python3 -I -B <script> --tsv <carriers.tsv> --json <NEW-JSON>`; 0 report produced, other exits could-not-evaluate; caller-selected JSON output; owner kaidoku). Its companion `compare.py` is an archived secondary gate: 0 clean, 1 failed; inputs are sibling decode/oracle/readobj captures and frozen carriers.tsv. Restore those captures to its original scratch BASE (line 20) before replay. No selftest mode exists (conformance limitation); it writes only that scratch comparison report. The observed 372/372 run is `.ufo/waves/round-32/independent-pe/compare.stdout.txt`, explained by `.ufo/waves/round-32/a2audit/A2PEIndependent.md`; it is not a frozen claim counter or a semantic/runtime capability.

Residual witness registry (archived evidence, not replacements for the frozen counters):

| name / kind | entry / inputs | verdict / self-invocation | pins / write scope / owner |
|---|---|---|---|
| Independent envelope-to-PE comparison / secondary gate | `python3 -I -B .ufo/waves/round-32/final-c1-witness/pe_own_compare.py <SCRATCH> <CARRIER-DIR> <ENVELOPE-DIR> <READOBJ-DIR>`; committed sibling envelope/readobj/TSV captures reproduce the recorded layout | 0 clean, 1 failed; no separate selftest mode (conformance limitation). Recorded 144/144 comparisons | frozen C1 carrier/prediction hashes and capture hashes in `.ufo/waves/round-32/a2residual/FinalC1Measure.md`; caller scratch output only; kaidoku |
| Fixed-source quote replay / secondary gate | `python3 -I -B .ufo/waves/round-32/source-reopen/verify_quotes.py`; restore sibling `reopen/` captures to the script's absolute `RE` directory first | 0 the fixed checks clean, 1 failed; default invocation includes negative quote controls, no separate selftest mode. Mechanical byte/location/length support only, not arbitrary semantic or authenticity grading | EXPECT/LIVE_EXPECT constants plus retained original/live source captures; writes original scratch `census.json`; kaidoku |

## Round-33 instrument status and preserved historical boundaries

The round-32 instruments above remain immutable historical evidence. In particular, C2v3 remains a falsified lexical measure and is not used for admission. The older selectable freeze gate and the three archived comparison/quote scripts retain their disclosed missing-selftest limitation; a historical run is not a newly conformant gate. Do not silently relabel a verdict-producing archived script as a passing probe.

| name | kind | entry command | verdict map | selftest | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| Selectable freeze-integrity successor | gate; registered successor to the preserved round-32 variant | `python3 -I -B tools/round-33/freeze-integrity.py --root <LANE> --round <N> --rev <REV> --claims <RELATIVE-CLAIMS>` | 0 clean for the selected valid pin map; 1 failed or uncaught exception (exit alone cannot distinguish a crash); 2 could-not-evaluate (missing freeze or usage) | `python3 -I -B tools/round-33/freeze-integrity.py --selftest`; five default-path fixtures assert exits/findings, not production measurements | selected claims file at its first-add commit, trusted `instruments` and `frozen_inputs` maps | production read-only; selftest unique disposable Git fixtures beneath `/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest` | kaidoku |

The selftest preserves the production predicate: both matching pin bytes and no post-freeze touching commit are required. Restoring the original bytes after a tampering commit still fails. This is not source authenticity, continuous stability, or immunity to every Git environment override.

Historical registry errata from `prep/R33RegistryAudit.md` (under `.ufo/waves/round-33/`), source-reviewed rather than freshly executed:

- Round-31 C1 write mode still prints a receipt-shaped `target=` line and exits 0/1; it is not a committed-record receipt. Only round-32 C1 implements the distinct write-mode exit 3. Round-31 C2 also requires its separately built, pinned mutant/sibling tree under `/fast/scratch/hyaku/kaidoku-r31/`; missing inputs can exit 2.
- An unhandled exception in the old counters exits 1, indistinguishable by exit code alone from a failed predicate. A missing resolved REA `package.json` can take this path. “Could-not-evaluate” describes that crash's evidentiary class, not a distinct emitted code. Calibration v1/v2/v3 additionally read the fleet pin through `--fleet` (default `/home/vgpnk/Projects/shokunin`).
- Archived `final-c1-witness/pe_own_compare.py` requires the live pinned carrier bytes as well as the committed captures; its scratch directory holds TSV copies and receives `compare-own.json`. The captures alone do not reconstruct the DLL bytes.
- Archived `independent-pe/compare.py` has hard-coded input paths, ignores argv, and invokes `llvm-readobj --version`. Its sibling `secondary_evidence.py` is an evidence producer (probe, not an admission verdict): `python3 -I -B .ufo/waves/round-32/independent-pe/secondary_evidence.py`; it reads its hard-coded `BASE`'s `indep.json` and carrier bytes, writes the recorded secondary-directory evidence to scratch, has no selftest, and is owned by kaidoku. Exit 0 means production completed; uncaught/nonzero exits are could-not-evaluate.
- Archived quote replay also fixes `SNAP` and `C1IN` to absolute lane paths; its internal assertion can exit 1 without a check verdict. The old cited-runs gate's `--selftest` creates a throw-away Git repository inside `tools/round-31/` (removed unless `--keep-selftest`); it must be copied to an authorized scratch clone before invoking that mode under this campaign's containment rules.

These limitations do not change the frozen predicates or historical receipts. The five surviving round-32 wrapper mutants remain un-killed; their exact identities and relevance are retained in `.ufo/waves/round-33/prep/R33MutantLimits.md`. None is repaired by a new metadata profile, and no hybrid coverage is widened here.

| name | kind | entry command | verdict map | selftest | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| Explicit-record scratch command audit | gate; lexical, not execution enforcement | `python3 -I -B tools/round-33/disk-command-audit.py <EXPLICIT-UTF8-RECORD>...` | 0 no red lexical hit, 1 red hit, 2 could-not-evaluate (usage/read/UTF-8); a hit may be quoted prose | same script `--selftest`: 14 lexical and 3 outer-CLI fixtures; installed-copy run must be measured separately | built-in expected finding/exit cases; `.ufo/waves/round-33/repairs/disk/` historical red receipt | scan reads explicit files only; selftest creates/removes a unique child beneath `/fast/scratch/hyaku/kaidoku-r33/R33DiskGuard` | kaidoku |
| Hash-bound legacy deadline allowances | gate wrapper over the unchanged round-20 timestamp gate | `python3 -I -B tools/round-33/timestamps/run-gate-hashed.py --root <LANE> --rev <REV> --path .ufo/waves/round-32 --spec tools/round-33/timestamps/allowances-hashed.json --out <NEW-SCRATCH>` | 0 clean after explicit allowances, 1 failed timestamp or `allowance_line_changed`, 2 could-not-evaluate (usage/assets/scope/spec/revision/scratch); underlying undeclared nonzero could-not-evaluate | same script `--selftest`; green exact-line echo, red same-line inserted event, red unlisted event; historical synthetic dates, unique scratch copies, bounded children | five exact-line hashes/reasons in sibling `allowances-hashed.json`; `.ufo/waves/round-33/repairs/timestamps/` red and repaired runs at `428315a8` | measured tree read-only; selected new scratch receipts; selftest creates/removes only a unique child under `/fast/scratch/hyaku/kaidoku-r33/R33TimestampRepair` | kaidoku |

The timestamp allowances apply only to the named old deadline fields and their exact-byte receipt echo; they are not timestamp grace windows. A legitimate edit invalidates an allowance until explicitly reviewed. The command audit does not resolve cwd, aliases, variables, shell functions or command substitution and never walks `/fast/scratch`.

## Round-33 stopped measurement

The planned R33-C1 independent 32-row measurement was stopped before freeze: its input-author task received a cyber-policy refusal and its later automatic-model-switch outputs are excluded. No replacement fixture task or alternative admission benchmark is used. Source-backed rules and separate isolated selftests below are reachable work, not a substitute target or new hybrid coverage. See `.ufo/waves/round-33/claim-stop.json` and `safety-holds.json`.

## CHPE structural profile — round 33

Use `python3 -I -B tools/round-33/chpe_profile.py <PINNED-DLL>` for a bounded **metadata structural profile**, not proof of a genuine hybrid. Sources: S101 (LLVM 23.1.3 field definitions, reader and emitter), S102 (Microsoft PE header documentation). The source-backed entry is `corpus/knowledge/2026-10-23-r33-chpe-structural-profile.md`.

| Checked condition | Decision / finding family | Authority and exact limitation |
|---|---|---|
| DOS/PE signatures, declared optional-header/data-directory/section-table spans or raw section bytes cannot be decoded | `malformed.*` for the specific first failure | S102: PE signature is located through the DOS offset at 0x3c; optional-header size and directory count bound probes. This is not a complete PE validator. |
| Raw COFF machine is not 0xAA64, or optional magic is not PE32+ 0x20b | `not_candidate.machine_not_arm64`; hybrid machine labels or other optional magic are `outside_profile.*` | Local input profile, not a claim that other PE architectures are invalid. LLVM's displayed hybrid label is not a replacement for the raw machine field. |
| Section count exceeds 96 | `outside_profile.section_count_limit` | The profile uses the limit stated in S102; it does not observe the Windows loader. |
| Load-config/metadata/code-map span is unmapped, in headers, crosses a section, or reaches an unbacked virtual tail | Structure-specific finding: `malformed.*_unmapped`, otherwise `outside_profile.*` | S101 checks whole referenced file extents. Requiring one section's file-backed prefix, bounded by min(VirtualSize, SizeOfRawData), is this reader's stricter profile; cross-section exclusion is not universal malformedness. |
| Load-config Size is below 0xd0, or CHPEMetadataPointer is zero | `not_candidate.load_config_lacks_chpe_field` or `not_candidate.chpe_pointer_zero` | S101 uses offsetof(CHPEMetadataPointer)+sizeof(pointer); the 0xc8/0xd0 offsets are derived from the captured 64-bit layout. Absence of a usable pointer is not a runtime verdict. |
| Metadata Version differs from 2, or code-map count exceeds 1024 | `outside_profile.metadata_version_unrecognized` or `outside_profile.code_map_count_limit` | Both are explicit local supported-profile limits. The opened LLVM reader does not enforce Version==2 or this count cap. A zero count is `not_candidate.code_map_empty`. |
| Decode a range record | Type = StartOffset & 3; RVA = StartOffset & ~3; Length is a separate u32 | S101 defines two u32 words and names tags 0 ARM64, 1 ARM64EC, 2 AMD64. Tag 0 is also lld's default machine bucket; it does not authenticate ARM64 instruction content. |
| Tag is unnamed 3, length is zero, or a tag-0/1 length is not divisible by four | `outside_profile.range_tag_unrecognized`, `range_length_zero` or `range_length_unaligned` | Conservative profile exclusions, not universal CHPE validity rules. No blanket AMD64 length-alignment rule is imposed. LLVM's writer comment reports MS link.exe empty ranges. |
| Range end overflows the u32 RVA space, or range span fails the selected mapping profile | `malformed.range_rva_overflow` or `outside_profile.range_*` | Addition is checked before mapping. This checks declared spans, not decoded instructions or every CHPE-referenced side table. |
| Mapped range lacks IMAGE_SCN_MEM_EXECUTE 0x20000000, or ranges overlap | `outside_profile.range_not_executable` or `outside_profile.range_overlap` | S101's lld emitter selects map membership using the execute bit; the bit does not prove execution. Non-overlap is local policy, not a Microsoft loader requirement. Global range ordering is not required. |
| No tag-0 or no tag-1 range remains | `not_candidate.no_arm64_range` or `not_candidate.no_arm64ec_range` | This profile's mixed-tag candidate criterion, not an ABI/ISA test. AMD64 tag 2 is recognized but cannot substitute for either required tag. |
| Selected structures pass these guards | `candidate.structural` / `structural_candidate` | Supported mixed-tag declarations only. A coherent false tag can still pass; instruction validity, ABI correctness, Windows loading and execution remain unknown. |

Read the first-failure `finding_id` and `facts`, not just the process exit. `--findings` prints the precise precedence; `--selftest` uses isolated synthetic fixtures and is instrument evidence, not an independent carrier measurement. Classifier exits: 0 candidate, 10 not-candidate, 11 outside-profile, 12 malformed, 2 usage/IO. None is a REA Evidence ID.

Pin source bytes and DLL SHA-256 before comparing facts. Preserve original round-32 native-view envelopes and their narrower classifier unchanged. This profile does not recover the EC view, validate instructions, inspect every CHPE side table, extend to published hybrids or internal functions, or widen Core coverage. Finite fixture agreement does not exclude arbitrary exact-hash lookup implementations.

## Round-33 retained parser interfaces — no completed carrier claim

| name / kind | command | exits / self-invocation | pins, scope and owner |
|---|---|---|---|
| CHPE structural profile / gate | `python3 -I -B tools/round-33/chpe_profile.py <DLL>`; `--findings` prints precedence | 0 profile candidate (clean); 10 not-candidate, 11 outside-profile, 12 malformed checked structure (failed eligibility); 2 usage/IO (could-not-evaluate). `--selftest` asserts exit/finding on isolated original recipes | `parser-pins.json`, source pins/anchors under `.ufo/waves/round-33/`; read-only input, selftest unique scratch under `/fast/scratch/hyaku/kaidoku-r33/R33ChpeParser/tmp`; kaidoku |
| Structural-match counter / gate, original claim stopped | `python3 -I -B tools/round-33/measure_driver.py --selftest`; normal CLI documented in its module docstring | 0 selected rows/docs matched; 1 evaluated mismatch; 2 refused input/spec; 3 could-not-evaluate. `--selftest` exercises outer CLI and document checks. No admissible original R33-C1 input manifest or production receipt exists | `parser-pins.json`, `document-spec.json` (source/text quality checks only); measured Git objects read-only, opaque copies in unique scratch, no held inputs; kaidoku |
| Original-recipe fixture helper / probe | `selftest_pegen.py`, imported only by the isolated parser/adapter selftests | no standalone verdict or CLI; failures of a calling selftest are that selftest's result | fixed recipes in its source, no parser imports; output only its caller's private scratch; kaidoku |
| Frozen round-32 oracle adapter / probe | `python3 -I -B tools/round-33/r32_oracle_adapter.py <DLL>`; `--selftest` | 0 legacy report produced; 2 unavailable/mismatched oracle (could-not-evaluate); selftest 0/1. This is not a measured round-33 baseline | old oracle full SHA-256 is pinned by `ORACLE_SHA256` in the adapter (prefix `17eea1f9`), not by the external-source map; input read-only and selftests isolated scratch; kaidoku |

These independent instruments are retained without the held author's generator, labels, manifests, predictions, input fixtures or derived controls. Their isolated selftests do not reopen the stopped 32-row claim.

## Round-33 builder-free verification limits

- The selectable freeze gate assumes a well-formed, nonempty trusted pin map. Seven empty/malformed variants were falsely CLEAN in `w1/WFreezeMalformed.md` (under `.ufo/waves/round-33/`); CLEAN is not claims-schema validation, integrity of unlisted evidence, or validation of a post-freeze claims-file edit. Its selftest covers the default claims path/HEAD; explicit production `--claims`/`--rev` variants have separate bounded runs, not selftest coverage.
- The parser selftest's finding-ID coverage does not establish boundary coverage: the count-limit `>`→`>=` mutant survives; one metadata-span mutation is inconclusive because its pristine/restored subprocesses returned EAGAIN. A tag mutation was detected by an error rather than a correctly typed finding. None closes the original stopped claim or the five historical round-32 survivors.
- The command scanner recognizes only its lexical grammar, not every path-qualified shell spelling. Relative multi-segment `bin/find` forms, cwd/variable/alias/substitution effects and command position are not resolved. Read/UTF-8 errors take exit 2 precedence even if RED rows also appear; quoted-token GREEN is not an execution verdict.
- The source-text checker originally failed its canonical section due to asymmetric blank-line normalization. The independent text-probe receipt remains the red-before record. The correction normalizes both bodies consistently and adds a blank-margin selftest; it is an unfrozen text-quality repair, never a new R33-C1 target or a substitute carrier study.

## GNU ELF version requirements — section-derived metadata (round 34)

Use `corpus/knowledge/2026-10-23-r34-elf-version-needs.md` for the source/observation/inference split. This adds technical depth to the existing native ELF surface, not a new REA verb or wider Core coverage. Sources: S103 (LSB 5.0.0 §10.7.4) and S104 (pinned glibc 2.42 `elf.h`).

| Decision | Exact field/threshold | Meaning and limit |
|---|---|---|
| Find the requirement records | Section type `SHT_GNU_verneed = 0x6ffffffe`; section `sh_link` identifies its string table | S103 capture:615–640; S104:459. Do not infer records from a section-name string alone. |
| Decode Verneed | 16 bytes, `<HHIII`: `vn_version` +0, `vn_cnt` +2, `vn_file` +4, `vn_aux` +8, `vn_next` +12; current version 1 | S103:671–677,717; S104:1124–1138. Half/Word widths are 16/32 bits, not pointer-sized. |
| Follow links | `vn_aux`/`vn_next` are byte offsets relative to the current Verneed; `vna_next` relative to the current Vernaux | S103 §10.7.4; S104:1130–1132,1158–1160. Bound the destination before reading; list count comes from the record, not a guessed file sweep. |
| Decode Vernaux | 16 bytes, `<IHHII`: raw hash +0, flags +4, other +6, name offset +8, next +12 | S103:839–845; S104:1153–1161. Strings must terminate inside the linked string table under this local profile. |
| Preserve meaning | `vna_other` is the version identifier associated with `.gnu.version`; retain raw bit 15, flags and hash | S103:937 defines the identifier; do not adopt S104's stale `Unused` comment. Weak flag bit is `0x2`; this reader does not authenticate the stored name hash or resolve symbols. |
| Apply the local profile | ELF64 little-endian, x86_64/AArch64, ET_EXEC/ET_DYN, OSABI 0/3, 64-byte ELF/section headers; one version-needs section | Conservative implementation scope, not universal ELF validity. AArch64/ET_EXEC branches were not exercised by the development public-library selftest. |
| Bound local work | Input ≤536870912 bytes; requirement entries ≤1024; section ≤65536 bytes; auxiliary total ≤4096; names ≤1024 bytes | Explicit local caps in `tools/round-34/elf-version-needs.py:LIMITS`; no completeness claim beyond this profile. |
| Stop rather than overclaim | Sectionless or extended-numbering input is unsupported; absent verneed on a supported sectioned image returns an empty list | No section-derived record is not proof of no dynamic-only requirement. DT_VERNEED/DT_VERNEEDNUM consistency, per-symbol associations, runtime selection and satisfiability remain unknown. |

Error patterns are local-reader findings, not host-loader verdicts: `error.unsupported.no_section_table` / `error.unsupported.shnum_extended` → unsupported, exit 11; `error.malformed.verneed_link` / `error.malformed.strtab_offset` → local parse rejection, exit 12; `error.io.read` / `error.io.size` → unevaluable I/O/cap, exit 13. All declared findings and their exact bounds are available with `--findings`. Helper/AST selftests do not demonstrate every malformed ELF branch.

Checklist:
1. Pin the supplied artifact's original path, SHA-256 and size; use a mode-0644 private copy. Never execute it to read metadata.
2. Read static references with `readelf --version-info --wide <copy>` and `readelf --section-headers --wide <copy>`; distinguish captured output from an expected field inferred by a separate author.
3. Run `python3 -I -B tools/round-34/elf-version-needs.py <copy>`. Success yields sorted `{schema:1,needed:[{file,versions:[{name,flags,other,hash}]}]}`; retain argv/stdout/stderr/exit and exact original digest.
4. For the frozen round-34 finite comparison, run `python3 -I -B tools/round-34/version-needs-counter.py --root <lane> --freeze <freeze-commit> --rev <measured-commit>`. The second schedule changes only string-table naming on never-executed private copies; raw hash values remain recorded metadata, not consistency/authenticity evidence.
5. Label decoded declarations as observation/inference; actual symbol resolution, selected dependency, instruction behavior, loader acceptance and authenticity are unknown without their own evidence.

## Round-34 instrument registry

| name | kind | entry command | verdict map | self-test command/spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| GNU ELF version-needs extraction | probe | `python3 -I -B tools/round-34/elf-version-needs.py <file>` | 0 decoded; 11 unsupported/could-not-evaluate; 12 local malformed-profile rejection/failed; 13 I/O/could-not-evaluate; 2 usage/could-not-evaluate; 1 selftest/failed | `python3 -I -B tools/round-34/elf-version-needs.py --selftest` (helper/AST checks; not a complete outer malformed-ELF test) | `.ufo/waves/round-34/claims.json` instruments; `tools/round-34/elf-version-needs.py` FINDINGS/LIMITS | read input; optional temporary selftest copies only | kaidoku |
| P34-version-needs finite counter | gate | `python3 -I -B tools/round-34/version-needs-counter.py --root <lane> --freeze <freeze-commit> --rev <commit>` | 0 clean; 1 failed; 2 could-not-evaluate | same script `--selftest`: outer CLI, isolated text-only green/red fixtures, exit and stable finding assertions; those are counter tests, not ELF-parser branch coverage | `.ufo/waves/round-34/claims.json`; `.ufo/waves/round-34/expected.json`; source/table pins declared there | private temporary reader and non-executable input copies; stdout receipt only | kaidoku |
| Schema-validating freeze integrity | gate | `python3 -I -B tools/round-34/freeze-integrity.py --root <lane> --round <N> --rev <commit>` | 0 clean; 1 failed; 2 absent freeze/could-not-evaluate; 3 schema/could-not-evaluate | same script `--selftest`: 25 isolated outer-CLI cases with exact expected exits/findings | claims instruments/frozen_inputs at first-add freeze; strict map schema and `_SCHEMA_CASES` in script; `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/receipt.json` | read Git objects; selftest Git writes only under `/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest` | kaidoku |

R33 and R32 CHPE/wrapper instruments, C2v3's lexical measure, and archived secondary PE gates are not admission dependencies of P34. Their surviving or incomplete mutation checks remain explicitly bounded in `corpus/lessons/round-34.md`; no old frozen claim is repaired by this registry.

### Bounded legacy-repair instruments (not P34 admission dependencies)

| name | kind | entry command | verdict map | self-test command/spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| R32 acceptance-wrapper clause successor | gate | `python3 -I -B .ufo/waves/round-34/prep/R34LegacyGaps-files/wrapper_successor.py --input <JSON>` | 0 clean; 1 failed; 2 could-not-evaluate | module `--selftest` is helper-level; outer CLI exit/findings are asserted by the private-copy `run_checks.py` harness below | same directory `fixtures/`, source selftest literals and `run-receipt.json`; historical wrapper unchanged | read supplied text/JSON; stdout only | kaidoku |
| Quote-support successor core | gate | `python3 -I -B .ufo/waves/round-34/prep/R34LegacyGaps-files/quote_support_successor.py --root <fixture-root> --cases <JSON>` | 0 clean; 1 failed; 2 could-not-evaluate | module `--selftest` plus outer CLI in private-copy harness; not archived quote-gate conformance | same directory `fixtures/`, helper literals and `run-receipt.json` | read named text/JSON; stdout only | kaidoku |
| Independent-comparator isolated replay | gate | `python3 -I -B .ufo/waves/round-34/prep/R34LegacyGaps-files/replay/indep_pe_replay.py <archived-compare> <fixture-BASE> <fixture-TSV>` | 0 clean; 1 failed; 2 usage/could-not-evaluate | private-copy `run_checks.py` harness retains one-carrier green and label-sha red; not the historical 372/372 replay | same directory `fixtures/`, `legacy-gap-matrix.json`, `run-receipt.json`; archived comparator hash in matrix | read isolated JSON/text fixture; imported archived source unchanged | kaidoku |
| Legacy-repair outer CLI harness | gate | copy `.ufo/waves/round-34/prep/R34LegacyGaps-files/` to a private sandbox, then `python3 -I -B <private-copy>/run_checks.py` | 0 clean; 1 failed; unexpected nonzero could-not-evaluate | that command is its isolated self-invocation: 19 bounded checks and 1 explicit not-run, exact expected exits/clauses in source | `run_checks.py`, `fixtures/`, `run-receipt.json`, per-check receipts | writes only its private HERE receipts/tmp; never run against the retained lane evidence directory | kaidoku |

## Round-34 post-control limits and stopped claim

R34-C1 is **falsified measure / honest stop**, not a demonstrated production capability. The unchanged counter accepts a size-keyed fixed-name-slice replay at 12/12 on both schedules without ELF structural decoding (`.ufo/waves/round-34/w1/CtlLabels.md`; decisive evidence landed `abbd76042fd23b1ba049350fc37a360f793892b7`). The production reader was not run on the claim set. Apply QUALITY 67 before any future counter freeze; do not reuse this target as admission.

The frozen reader's detailed `FINDINGS` metadata has additional disclosed limits (`.ufo/waves/round-34/w1/RevDecisionTable.md`): five single-field Ehdr locators are wrong although the full struct range/field values are correct; several local-profile exclusions are classified `malformed` rather than `unsupported`; declared first-failure precedence differs in multi-fault cases. Its full auxiliary tie-break is `(name,other,flags,hash)`, while the finite counter permits only unique `(name,other)` pairs. The technical field layout from S103/S104 is separately reopened, but the entire 37-row instrument table is not claimed conformant or universally validated.

The schema-validating freeze instrument's real 21-pin check is clean, but its restored-after-change selftest can fail spuriously when a commit hash begins with 0; the wave observed 24/25 (exit 1). Duplicate JSON members and path aliases remain accepted. Candidate scratch-only fixes and exact red receipts are retained; no pinned instrument or claim was amended. Archived adversarial harnesses are bounded evidence, not newly certified admission gates.

### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)

Registered because the instruments are relied upon and will be reused; the capability they were built to demonstrate was **denied** by this round's own stop (`.ufo/waves/round-34/r34b/claim-stop.json`, `cd75b92e`). Read every row together with QUALITY 68-74.

| tool | purpose | command | exit codes | selftest |
|---|---|---|---|---|
| `tools/round-34/replay-gate.py` | Runs a counter's own argv with a reader substituted, reads the counter's own receipt fields, refuses when any registered shortcut meets the target, and requires the registered structural positive control to meet it. Verdicts `REPLAY_GATE_CLEAN` / `REPLAY_GATE_REFUSED` / `REPLAY_GATE_UNEVALUABLE`; config needs `schema`, `predicate`, `counter.argv` with exactly one `{reader}` slot, `target`, `positive_control`, and at least three uniquely named shortcuts | `python3 -I -B tools/round-34/replay-gate.py --root <LANE> --config <CONFIG> [--json-out <FILE>]`; red case `--config tools/round-34/gate-config-naive.json`, green case `--config tools/round-34/gate-config-mini.json` | 0 clean / 2 refused / 3 unevaluable (positive control absent or below target, unreadable receipt, counter target mismatch, config schema) | `--selftest`: 12 cases + 3 source mutants (refusal, positive-control, shortcut-floor); 0 all pass with `failures=0 mutants_killed=3`, 1 otherwise |
| `tools/round-34/c2-shortcut-gate-counter.py` | R34-C2 counter: gate selftest, red case, green case in one command; six clauses `gate_present`, `selftest_clean`, `mutants_killed`, `red_refused`, `green_clean`, `green_positive_meets_target` | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> [--json-out <FILE>] [--gate <CONTROL GATE>]` | 0 all clauses / 1 miss naming `clauses_failed` / 2 gate or pinned input absent | Its own selftest is the gate's; `--gate` exists only to score control gates |
| `tools/round-34/mini-fix/mini-counter.py` | The green surface: eight 512-byte `MREC` fixtures, name pool permuted per fixture, opaque temporary paths, reader output compared to `expected.json` | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root <LANE> --control-reader <READER> [--seed <S>]` | 0 reader meets target / 1 below / 3 unevaluable | `--selftest` runs `readers/structural.py` (8/8 expected) |
| `tools/round-34/mini-fix/naive-counter.py` | The red surface: same fixtures scored on their own paths, so identity keying is reachable | same argv shape as the green counter | 0 target met / 1 below / 3 reader absent | none — exercised by the gate's red case |
| `tools/round-34/mini-fix/build.py` | Rebuilds the eight fixtures and `expected.json` from `spec.json` deterministically | `python3 -I -B tools/round-34/mini-fix/build.py [<dir>]` | 0 | none |

Known limits of the pair, each disclosed in `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` and routed to QUALITY 68-74: `CLEAN` is relative to the caller's class list (five unregistered classes reach the green 8/8); `met_target` is trusted from the counter's receipt and never cross-checked with `matched`; class labels are free text and a relabelled class is excluded from the refusal set; the registered set is not asserted against the pinned set; the frozen pin map sits under `claims[0].pins`, which `tools/round-34/freeze-integrity.py` rejects (`instruments_missing`, exit 3) — the enforced container is `.ufo/waves/round-34/r34b/instruments.json` (26 pins, CLEAN); `--rev` is an echoed label; receipts carry no argv. The repair route is `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/mini-counter-fresh.py` (fresh content per run; 8/8 structural, 0/8 for nine structure-blind classes), which is a next-round instrument and not evidence for this round.

## SquashFS recursion through sasquatch — round 36

Round-36 moved sasquatch (unblob's `squashfs_v4_le` recursion extractor) from the PROVINCE Frontier
bullet into a Core row. The REA `extract-firmware` envelope is the only judge of whether recursion
happened; no amount of local `unsquashfs` success substitutes for it, and no receipt is ever edited to
look like a pass. Claims, target and kill rule: `plans/round-36-claims.md` (R36-C1); carrier, oracle
and before-arm evidence: `corpus/evidence/round-36/c1/`.

### Decision table — REA envelope signal to action

| Signal in the `extract-firmware` envelope | Meaning | Action |
|---|---|---|
| `extraction_gaps[]` entry with `kind` = `missing-extractor-dependency`, `dependencies` = `["sasquatch"]`, `handler` = `squashfs_v4_le` — recalled (`corpus/evidence/round-36/c1/K1/before.json`, `K3/before.json`) | The `squashfs_v4_le` handler reached a SquashFS 4.0 little-endian container and the extractor binary was not resolvable on `PATH` for that run. `range.offset`/`range.length` are the container's byte span; `root_file_range` repeats it when the container is the input root. The envelope does **not** say the image is unreadable | Install the official onekey-sec `sasquatch_1.0_amd64.deb` binaries into `~/.local/bin` (`sasquatch`, `sasquatch-v4be`; no pacman, no AUR, no rebuild — `plans/round-36-claims.md`), confirm `command -v sasquatch` resolves, then rerun `extract-firmware` on **the same input** with a **fresh `output_directory`**. Keep the old envelope as the paired before-arm; `K3/after-run.json` records `/home/vgpnk/.local/bin/sasquatch`, `unsquashfs version 4.5.1 (2022/03/17)`, sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` |
| No sasquatch gap, and every oracle regular file is present at a path whose suffix is the oracle's relative path with equal sha256 — recalled (`K1/after.json`: 3/3, 0 gaps) | Recursion published the filesystem's regular files. `publish = regular files only` | Nothing to install. Record both arms and the oracle unchanged; score with the counter, never by eye |
| Before arm publishes nothing, or publishes the container as one opaque file `…/<offset>-<end>.squashfs_v4_le` — recalled (`K1/before.json`: 0 files, `published_bytes` 0; `K3/before.json`: 2 files, the carved ELF and `944632-11454968.squashfs_v4_le`) | Blocked recursion is *opaque container publication*, not a partial extraction: the container's own bytes are published as a single file and no entry inside it is | Never compare file counts across arms, and never read the opaque range file as an extracted file. Compare the oracle's `(relative-path suffix, sha256)` rows only |
| `extraction_gaps[]` with `kind` = `unpublished-entry`, and/or `normalized_result.unpublished_entries[]` with `kind` = `symlink` and a `link_target` — recalled (`K2/after.json` `var/notice-link`; `K3`/`K4/after.json` `.DirIcon`, `nvim.png`) | Symlinks (and special files) are retained as metadata only: `extraction_continuations[].instruction` = "The entry is retained as metadata; only regular files are published, without executable permission bits" (`K3/after.json`). **Not** a sasquatch failure and **not** blocked recursion: an after-arm with recursion published still carries these gaps | Do not chase it, do not claim it as published, do not install anything. Filter gaps by `kind` + dependency name (`c1-counter.py` `sasquatch_gap()`), never by "gaps list is empty" |
| AppImage: `chunks[]` holds one `elf64` chunk starting at 0 and exactly one `squashfs_v4_le` chunk whose `range.offset` equals the ELF end — recalled (`K3/after.json`: `elf64` 0..944632, `squashfs_v4_le` 944632..11454968; `K4` 936456..) | Type-2 layout: an ELF runtime with the filesystem appended; `hsqs` sits at that offset, not at byte 0 | Run the independent oracle as `/usr/bin/unsquashfs -o <that offset>`. The harness rule `e_shoff + e_shnum*e_shentsize` (`tools/round-36/c1-run.sh`, oracle mode) is **one operand** of the type-2 runtime rule (the runtime takes the larger of it and the end of the last section header); the two coincide on K3/K4 (`K3/oracle-run.json` `squashfs_offset` 944632) — do not state the AppImage specification defines any offset |
| After-envelope `files` count exceeds the oracle's regular-file count — recalled (`K3`/`K4` 2147 vs 2130; nested `…/usr/bin/nvim_extract/0-11170568.elf64_extract/carved.elf`) | Nested carves and nested ELF extracts are published beside the squashfs files | Match by suffix + sha256. Extras are not extra extraction and are not evidence of a second filesystem; count equality is not identity |
| `operation` ≠ `extract_firmware`, or `provider.id` ≠ `unblob` — the counter's own binding | Wrong verb or wrong provider: the receipt is not comparable to a squashfs-recursion claim | Rerun `npx -y rea-agents@6.5.0 extract-firmware --format json <input> <fresh-outdir>`; do not relabel a receipt from another verb |
| An envelope whose `files` or `extraction_gaps` were edited by hand no longer recomputes to its stored `ev_…` id under the rea-agents 6.5.0 rule (`c1-counter.py` `evidence_ids()`, frozen `tools/round-27/xpin-attribute.mjs`; selftest case "forged oracle-copy envelope") | A patched envelope is not a receipt, however plausible its file list | Never patch, reorder or trim an envelope. A receipt that does not recompute is a failed measurement, and the remedy is a rerun, not an edit |

### Reproduction order (a later run must not retrofit a before-arm)

1. `tools/round-36/c1-run.sh oracle CARRIER OUTDIR` — independent `/usr/bin/unsquashfs` 4.7.5, offset
   0 for a bare image and the ELF end for an AppImage, regular files only.
2. `tools/round-36/c1-run.sh before CARRIER OUTDIR` — the harness strips every `PATH` directory that
   holds an executable `sasquatch` and refuses (exit 2) if one survives. Keep this envelope.
3. Install the two deb binaries into `~/.local/bin`; `command -v sasquatch` must resolve.
4. `tools/round-36/c1-run.sh after CARRIER OUTDIR` — `PATH` as given, fresh output directory; exit 0
   with `sasquatch_version` populated in `<mode>-run.json`.
5. Score at a named revision with the counter; a miss is an honest stop, and the counter, predicate,
   carriers and oracle are never changed after the freeze commit.

Harness exit map (`tools/round-36/c1-run.sh`): 0 ok, 2 usage/environment error, 3 tool failure.

### Round-36 instrument registry

| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-36/c1-counter.py` | gate — R36-C1 coverage, sasquatch squashfs recursion Frontier → Core | 0 clean (`carriers_matched == 4` and every binding true); 1 failed (target not met at the measured revision); 2 could-not-evaluate (missing `--root`/`--rev`/`--freeze`/`--pkg65`, unknown revision, git/node failure, `xpin` tool absent at the freeze). No other code | `python3 -I -B tools/round-36/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` — flag spelling `--selftest`; 14 isolated git-fixture cases (1 green, 13 red), exit 0 iff no case fails, 1 otherwise | Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0` pins `corpus/evidence/round-36/c1/carriers.json` (K1-K4 id + sha256), every `K*/oracle.tsv` and `tools/round-27/xpin-attribute.mjs`; `carriers_unchanged`/`oracle_frozen` compare measured-revision bytes against the freeze bytes, so a post-freeze edit is visible, not silent. Target `4` is a literal in the script. Selftest fixtures: `tools/round-36/selftest/dev-{before,after}.json`, `dev-oracle.tsv`, `dev-le-xz.sqsh`. Control verdicts committed at `6a870b9290e9566468d7d9e6d1b8308daf025b12` under `.ufo/waves/round-36/controls/ctl-c1-{0,1,2}-*.{json,out}` (each `CTL-C1-n exit=1`) | Reads git objects, `node`, and the rea-agents 6.5.0 package tree; writes only a private directory under `$HYAKU_SCRATCH/kaidoku-r36` (default `/fast/scratch/hyaku/kaidoku-r36`) and `--json-out`; `--selftest` creates and removes one `c1-selftest.*` git fixture repo per case under the same root (each fixture asserts `git -C <fixture> rev-parse --show-toplevel` equals the fixture) | kaidoku |
| `tools/round-36/c2-counter.py` | gate — R36-C2 calibration, self-assessment surfaces vs observed repo state | 0 clean (`mismatches == 0` and `guards_ok`); 1 failed; 2 could-not-evaluate (missing `--root`/`--rev`/`--base`, unknown revision, `SCORECARD.md`/`SHONEN.md` absent). No other code | `python3 -I -B tools/round-36/c2-counter.py --selftest` — flag spelling `--selftest`; 13 isolated git-fixture cases (1 green, 12 red), exit 0 iff no case fails, 1 otherwise | Base `cab59f221fe19726b5692bfa4d9a9679e96b8a73` is the guard baseline: no unit removed, no fewer pointers than at the base, and every pointer unresolved at the base repaired by a resolving pointer to the same document. Stated values live in SCORECARD `## Owned axes` / `## Capabilities` and the SHONEN boxes and are compared with command A (`corpus/knowledge` files ↔ `corpus/README.md` coverage map, queue-drain rule blocks ↔ resolvable `corpus/knowledge/…:line-range`) and command B (`evidence/round-1-2026-10-15/result.json` aligned/total obligations), plus two observed heading ranges (`SKILL.md` `## Queue-drain craft`, `PROVINCE.md` `## Adjacent`). Control verdicts under `.ufo/waves/round-36/controls/ctl-c2-{0,1,2,3}-*.{json,out}` (each `.out` ends `ctl-c2-n-… exit=1`) | Reads git objects only; `--json-out`; `--selftest` creates and removes one `c2-selftest.*` git fixture repo per case under `$HYAKU_SCRATCH/kaidoku-r36` | kaidoku |

Both rows are read-only over every surface they do not own and never act on an external surface. A
verdict names the revision it was measured against; a run over a moving worktree is not comparable to
one over the cited commit.

### Limits (read with every row above)

1. The blocked-recursion signal is byte range + dependency name only. The envelope does not say
   whether sasquatch of any version would parse a vendor-mangled table, and no such carrier exists.
2. Big-endian and AVM SquashFS, vendor-mangled images, loader behaviour, and the extracted programs are
   not claimed. `sasquatch-v4be` is installed but no carrier exercises it.
3. Published files carry no permission bits (`extraction_continuations[].instruction`); executing an
   extracted program needs its own evidence.
4. K3/K4 identity is `subject.digest.sha256`. `subject.local_path` in the committed envelopes points
   into scratch and is not durable evidence.
5. The AppImage offset caution above is observed equivalence on K3/K4 under the runtime's two-operand
   rule, not a general theorem about arbitrary ELF layouts.
6. The 7z fallback path was not retested in round 36.
7. No digest-pinned `expected.json` baseline exists for these two counters: input identity is pinned by
   the freeze commit (a git object the counter compares byte-for-byte), and the expected exits are the
   selftest case table in the script plus the committed control receipts — not a separate digest file.
8. This registry covers the two round-36 counters only. `tools/round-35/c1-coverage-counter.py` and
   `tools/round-35/c2-calibration-counter.py` still have **no** registry row at this home; that debt is
   reported in round 36 and is not discharged here.
9. Found by the round-36 wave after the freeze (`.ufo/waves/round-36/w1/R36CriticC1Shortcut.md`): the C1
   counter checks receipt integrity, not provenance — an `after.json` fabricated from the oracle and
   re-hashed with REA's own 6.5.0 digest code scores `met_target`. Provenance rests on the four
   independent reproductions (`.ufo/waves/round-36/w1/R36ExecReproK{1,2,3,4}.md`), not on the counter.
   The verdict also depends on the `--pkg65` package root, which no receipt pins.
10. Found by the same wave (`.ufo/waves/round-36/w1/R36CriticC2Shortcut.md`): the C2 counter keys units by
   first cell / box title (a later duplicate row or box shadows the earlier one), validates only the first
   statement per unit, accepts any same-basename document as a repair, guards pointers by count not
   identity, and does not bound the knowledge population below the base. A green C2 is therefore checked
   again by the stricter non-counter re-derivation recorded in the round-36 lesson, never cited alone.

### Round-35/37/38/39 instrument registry

Added round 39 (routed defect R38-CL2; discharges limit 8 of the round-36 registry above). Round 35/37/38 rows were read from source at `a2f64e1d` by wave-1 seat `R39CL2Registry` (`.ufo/waves/round-39/w1/R39CL2Registry.md`, which also lists what it could not verify). Uncaught exceptions in the round-35/37/38 Python counters exit `1`, the code for `failed`; `tools/round-37/c1-counter.py` is a probe that cannot return a verdict.

| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
| `tools/round-35/c1-coverage-counter.py` | gate — R35-C1 coverage: two jsc2js knowledge entries land on the `.jsc -> source mapping` frontier (cites S125/S129); predicate in the script `:6-15` | `0` clean (no failing check; prints `C1_CLEAN revision=`); `1` failed (prints `C1_FAIL:` + failing ids); `2` could-not-evaluate (missing `--root`/`--rev`/`--freeze`; `.ufo/waves/round-35/claims-canonical.json` absent or unparseable at `--freeze`; the script's `PREDICATE` is not a substring of that file). No other code is declared, and an uncaught exception exits `1`, so a crash reads as `failed`, not `could-not-evaluate` | `python3 -I -B tools/round-35/c1-coverage-counter.py --selftest` — flag spelling `--selftest`; 1 green + 1 red isolated git fixture under `TMPDIR` (`:42-118`), exit 0 iff the green run returns 0 and the red run non-zero; exercised 2026-10-26 → `C1_SELFTEST: ok`, `green=0 red=1`, exit 0 | `--freeze` claims file `.ufo/waves/round-35/claims-canonical.json`; in-script `ENTRIES` (`:16-19`) and the 11-column SOURCES row regex (`:22`); PROVINCE/README stems derived from `ENTRIES`. `--rev` is a tree read only — no digest pin, no `expected.json` | read-only over `git show`/`git ls-tree`; writes `--json-out` only; selftest scratch is a removed tempdir. Read `failing`/`pass`: the receipt's `checks` map is built from six literals that never occur in `fails`, so it is always all-true | kaidoku |
| `tools/round-35/c2-calibration-counter.py` | gate — R35-C2 calibration: closure of the four round-34 routed record defects D-1..D-4 (predicate `:7-19`) | `0` clean (`C2_CLEAN revision=`); `1` failed (`C2_FAIL:`); `2` could-not-evaluate (missing `--root`/`--base`/`--rev`/`--freeze`; claims file absent or unparseable; predicate mismatch); uncaught exception → `1` (reads `failed`) | `python3 -I -B tools/round-35/c2-calibration-counter.py --selftest` — `--selftest`; 1 green + 1 red isolated git fixture; exercised 2026-10-26 → `C2_SELFTEST: ok`, `green=0 red=1`, exit 0 | claims file at `--freeze`; `EIGHT_CELL_SECTIONS` (`:21`), `SETTLE_FILES` (`:26`), `LESSON_PATH` (`:31`), `CENSUS_PATH` (`:32`), `R34B_ENTRY` (`:33`), census literals `rows=106`/`EXIT=0`/`W04` (`:68`); the guard baseline is `--base` (commit-time ordering of D-1, settle totals of D-2). No digest file | `--json-out` only; selftest tempdir removed | kaidoku |
| `tools/round-37/c1-counter.py` | **probe** — R37-C1 coverage instrument that cannot return a verdict: no working self-test, and every path that reaches scoring crashes | Declared in code: `0` if `met_target`, `1` otherwise, `2` from argparse. Observed: `--selftest` without the required args → `2` (argparse rejects `--root/--rev/--freeze` before the selftest branch); with placeholder args → `1` (`FileNotFoundError` in `make_fixture` `:323`, no `corpus/knowledge` dir); a scoring run at the base revision → `1` with `TypeError: a bytes-like object is required, not 'str'` at `load_oracle` `:93` (`git()` `:33-36` returns bytes). `measure()` also carries a spliced fixture-writing block (`:163-186`) that references an undefined `d`. A crash is indistinguishable from `failed`; never cite this tool as a verdict | no selftest — `--selftest` is parsed but unreachable without `--root/--rev/--freeze`, and the branch it reaches is broken; both failure modes exercised 2026-10-26 | `sasquatch_v4be_sha256` literal `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; `PINS.rea_package_root` = realpath(`--pkg65`); `PINS.unblob` = `$REA_UNBLOB_COMMAND` or `~/.local/bin/unblob`; `CARRIERS`/`EVDIR`/`ENTRY`/`CORE_HEADING` (`:12-16`), `TARGET = 4`; `tools/round-27/xpin-attribute.mjs` must exist at `--freeze`. `carriers.json` is read at `--rev` only — no freeze equality check | `--json-out`; scratch `$HYAKU_SCRATCH/kaidoku-r37/selftest/` — a crashed selftest leaves its fixtures behind (observed) | kaidoku |
| `tools/round-37/c1-run.sh` | probe — carrier harness producing one REA `extract-firmware` envelope and one `<mode>-run.json`; no verdict of its own | `0` run completed and receipt written (whatever the envelope says); `2` usage/environment (bad mode, carrier id absent from `carriers.json`, `sasquatch-v4be` still on the stripped `before` PATH or absent from the `after` PATH); `3` the REA child exited non-zero. Undeclared `1`: an unknown carrier id aborts under `set -e` from the python lookup (exercised → `1`) | no selftest | `corpus/evidence/round-37/c1/carriers.json`; the receipt records carrier path + sha256, `sasquatch_v4be` path/sha256/`-version` line, `unblob`, `rea_package_root`, UTC, child exit and a 10-line stderr head; `rea-agents@6.5.0` and `timeout 900` are hardcoded in argv | writes `OUTDIR/<mode>.json` and `OUTDIR/<mode>-run.json`; scratch `$HYAKU_SCRATCH/kaidoku-r37/c1-run.XXXXXX` (removed on exit) | kaidoku |
| `tools/round-37/gen-squashfs.py` | probe — deterministic SquashFS v4 writer (LE / BE / AVM-BE, gzip or xz); the carrier generator for rounds 37-39, with no expected values in-repo | `0` image written (`wrote <out> <n> bytes, inodes <k>`); `2` argparse; uncaught exception → `1`. No `sys.exit` | no selftest | byte-stability comes from fixed constants: `MAGIC` (`:7`), `COMP` (`:8`), `MKFS_TIME = 1700000000` (`:14`), `UID = 1000` (`:15`), block size 4096, gzip level 9 / xz preset 6. Exercised 2026-10-26: two `--endian le --comp gzip` runs are byte-identical (`fb080c75b912cce0…`); magics `hsqs` (le) / `sqsh` (be, avm) | writes the `out` image only. Docstring `:2-4` states the limits: no fragments, xattrs, export table, sparse or empty-dir entries | kaidoku |
| `tools/round-38/c1-counter.py` | gate — R38-C1 coverage: standard BE SquashFS v4 → Core on 4 carriers | `0` met (`carriers_matched == 4` and every binding true); `1` not met; `2` could-not-evaluate (missing `--root/--rev/--freeze/--pkg65`, unknown revision, `carriers.json` absent at freeze, `xpin` absent at freeze, xpin run or line-count failure); uncaught JSON/OS error → `1` (reads `failed`) | `python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` — `--selftest`; 15 isolated git-fixture cases (1 green, 14 red), exit 0 iff none fails; exercised 2026-10-26 → `cases 15, green_ok 1, red_ok 14, failures []`. Inputs are `tools/round-38/selftest/{dev-after.json,dev-oracle.tsv}` and `tools/round-27/xpin-attribute.mjs` read from the **working tree** | `.ufo/waves/round-38/c1/carriers.json` at `--freeze` and byte-equal at `--rev`; every `corpus/evidence/round-38/c1/K*/after.json` `subject.digest.sha256` equals its carrier pin; `corpus/evidence/round-37/c1/K*/oracle.tsv` at freeze and rev (equality); `HANDLER`, `TARGET = 4`, `ENTRY`/`STEM`, `OPENED = 2026-10-26`, `CORE_HEADING` (`:28-37`); `xpin-attribute.mjs` read from the freeze commit. Bindings `frontier_note` is a text shape (`big-endian` + `superseded` on one line), not a structural check | `--json-out`; scratch `$HYAKU_SCRATCH/kaidoku-r38/c1-counter.*` (removed) | kaidoku |
| `tools/round-38/c1-run.sh` | probe — carrier harness (`before` / `after` / `oracle`) | no map of its own: the script returns its child's status — REA's exit for `before`/`after` (undocumented REA codes propagate unchanged), `1` for a failed `sasquatch-v4be` in `oracle`, `2` for a bad mode, `1` for a missing argument (`${1:?}` / `${REA_UNBLOB_COMMAND:?}`, exercised → `1`) | no selftest | `rea-agents@6.5.0` in argv; `REA_UNBLOB_COMMAND` required and kept absolute; `before` strips `$HOME/.local/bin` from the child PATH while the unblob command stays absolute | `OUTDIR` for before/after (removed first; REA creates it), `OUTDIR` tree plus `rel<TAB>sha256<TAB>size` on stdout for oracle; scratch `$HYAKU_SCRATCH/kaidoku-r38/c1-run-$$` | kaidoku |
| `tools/round-38/c2-counter.py` | gate — R38-C2 calibration: self-assessment surfaces against observed repo state | `0` met (`mismatches == 0` and `guards_ok`); `1` not met; `2` could-not-evaluate (missing `--root/--rev/--base`, unknown revision, `SCORECARD.md`/`SHONEN.md`/`PROVINCE.md` absent); uncaught exception → `1` (reads `failed`) | `python3 -I -B tools/round-38/c2-counter.py --selftest` — `--selftest`; 14 inline git-fixture cases (1 green, 13 red), exit 0 iff none fails; exercised 2026-10-26 → `cases 14, green_ok 1, red_ok 13, failures []` | `BOX1 = 'SKILL.md contains real decision tables'`, `BOX4 = 'No cross-domain bleed'` (`:30-31`), `TOKEN`/`PTR`/`LANE` grammars (`:27-29`); command A's recipe (`corpus/knowledge` stems ∩ `## Coverage map`, `## Queue-drain craft` rule blocks, `corpus/knowledge/...:N-M` refs) and command B's input `evidence/round-1-2026-10-15/result.json` (`:152`); the guard baseline is `--base`. Expectations live in the selftest case table, not a digest file | `--json-out`; scratch `$HYAKU_SCRATCH/kaidoku-r38/c2-selftest.*` (removed) | kaidoku |
| `tools/round-38/freeze-drift.py` | gate — QUALITY 79/80 first-freeze rule: no commit between a claim's first freeze and the measured revision may touch a kill-rule path | `0` clean; `1` drift (commits listed with `net_changed` and `ships_freeze_bytes`); `2` could-not-evaluate (unknown revision, `--freeze` not an ancestor of `--rev`, `git log` failure, argparse). Exercised 2026-10-26 on an isolated fixture: clean `0`, drift `1`, unknown rev `2`, non-ancestor freeze `2` | `python3 -I -B tools/round-38/freeze-drift.py --selftest` — 8 cases (added round 39; behaviour parity 18/18 on recorded receipts, `.ufo/waves/round-39/w1/R39CL2Selftests.md`) | caller's positional pathspecs; the default set (`:26-32`) is the round-38 kill rule (claims doc, both counters, carriers manifest, oracles). No stored digest — the pinned values are the commits themselves | `--json-out` only; read-only over `git log`/`git diff` | kaidoku |
| `tools/round-38/intended-doc.py` | gate — QUALITY 81: a repaired pointer names the intended document and that document's git object is unchanged from the base | `0` bound; `1` not-bound (unit rows != 1, intended path not named in the unit row, intended document absent at base or changed base→rev); `2` could-not-evaluate (named file absent at `--rev`, absent at `--base`, argparse). Exercised 2026-10-26: bound `0`, un-named path `1`, unknown rev `2` | `python3 -I -B tools/round-38/intended-doc.py --selftest` — 9 cases (added round 39) | `--intended` path plus the `--unit` first cell; the expected value is identity of `<rev>:<intended>` and `<base>:<intended>` (`rev-parse --verify`). No digest file | stdout JSON only — there is no `--json-out` | kaidoku |
| `tools/round-38/registry-immutable.sh` | gate — SOURCES append-only, CORPUS rule 2: a row present at BASE may differ at REV only in status, recheck, used-by | `0` no row changed outside those columns (silent); `1` rows changed — `<id> changed columns: <n>…` on stdout. No `2`. Exercised 2026-10-26: clean `0`; widened scope cell `1` (`S100 changed columns: 6`); an unknown or unresolvable revision is **not** detected: git fails, the row set reads empty and the gate exits `1` listing every row as deleted (measured round 39, `.ufo/waves/round-39/w2/R39W2Census.md`), so a `1` must be read with its row list | `bash tools/round-38/registry-immutable.sh --selftest` — 5 cases (added round 39; run mode now also exits 1 on a deleted or reordered row, which the round-38 bytes accepted) | BASE blob of `corpus/SOURCES.md`: every row whose first cell is an `S` id, compared field-by-field; allowed columns 9 (status), 11 (recheck), 12 (used-by) | stdout only; read-only | kaidoku |
| `tools/round-38/gen-controls.py` | probe — frozen-control receipt generator, 7 kinds (`c1-0/1/2`, `c2-0/1/2/3`). QUALITY 80 makes its bytes freeze-relevant, but the gate over this path is `freeze-drift.py --freeze <f> --rev <r> tools/round-38/gen-controls.py`, not this file | `0` the control did **not** meet the target (expected); `1` the control met it (kill condition); `2` internal error, missing `--out`, unknown kind. Exercised 2026-10-26 on the five fixture kinds `c1-1 c1-2 c2-1 c2-2 c2-3` → `counter_exit 1`, `kill false`, exit `0` each; `c1-0`/`c2-0`, which replay the real counters, were not exercised in wave 1 | no selftest — its two `selftest` hits are the fixture-dir name (`:41`) and a docstring | `PKG65` default `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; each kind's defect mirrors the counters' own fixture code (it imports `c1-counter.py`/`c2-counter.py`), so it is not independent of them | `--out` receipt; scratch `$HYAKU_SCRATCH/kaidoku-r38/controls-<kind>/` | kaidoku |
| `tools/round-38/selftest/` (4 files) | data, not an instrument — committed fixtures with no verdict and no exit codes | — (none) | — (not executable) | `dev-after.json` `d9193aea3eb5263cb7cc3d2377b853ae0af9b4a672f7d0a9b60c630faa920ca9`, `dev-oracle.tsv` `69a8abd5fc3e4d9083594f012f2d732a1ac99b91333dd7427b0ebfb74cadcd67`, `dev-before.json` `ff1587fea2ce9c601e7819bfa4e838e3cb157a4ed6cf8c1b140469ab9fa9a57e`, `dev-le-xz.sqsh` `acc64a3db71bddfd50de3aed3cee148313b0f8605420e64cc3140f5f03394b93` — all four unchanged from the round-38 record (`.ufo/waves/round-38/w1/R38ExecSelftests.md:33-34`). Read by `tools/round-38/c1-counter.py:273-274` and `tools/round-38/gen-controls.py:42-43` (after + oracle only); `dev-before.json` and `dev-le-xz.sqsh` have no consumer under `tools/` | read-only inputs | kaidoku |
| `tools/round-39/c1-counter.py` | gate — R39-C1 coverage, standard BE SquashFS v4 Frontier → Core on six carriers | `0` met; `1` not met; `2` could-not-evaluate, including `frozen_path_changed` | `--selftest --pkg65 <REA 6.5.0 root>` — 33 cases (1 green, 32 red, each on its clause) | `.ufo/waves/round-39/c1/carriers.json` | `--json-out` and a private scratch under `$HYAKU_SCRATCH/kaidoku-r39` | kaidoku |
| `tools/round-39/c1-run.sh` | probe — `after`/`oracle` harness; refuses a scratch outside `/kaidoku-r39/` | `0` ok; `2` usage/environment; `3` tool failure | none in the script (wave-1 `R39C1Harness.md` 68-case external selftest) | carrier pins in `carriers.json` | OUTDIR and its SCRATCH | kaidoku |
| `tools/round-39/mk-carriers.py` | probe — emits the C1 carrier manifest with sha256 pins | `0` written; `2` usage or a refused carrier | none | — | `--out` | kaidoku |
| `tools/round-39/sqfs-list.py` | probe — independent SquashFS 4.0 reader (LE/BE, gzip/LZMA/xz, fragments) printing regular-file and symlink tables | `0` ok; `2` unreadable/unsupported | none (checked against K1–K4 oracles, wave-1 `R39C1IndepReader.md`) | — | the `--files`/`--symlinks` outputs | kaidoku |
| `tools/round-39/gen-squashfs.py` | probe — round-37 writer plus UTF-8 name length and xz-container fixes (K5/K6 builder) | `0` image written; `2` argparse | none | K5/K6 pins in `carriers.json` | the output image | kaidoku |
| `tools/round-39/sqfs-triage.py` | gate (interpreter) — reads only the SKILL craft triage table and labels REA envelopes | `0` labelled; `2` table missing/malformed or envelope unreadable; `1` only for a failed `--selftest` | `--selftest` — 35 cases | the table block after `<!-- sqfs-triage-table v1 -->` in `SKILL.md` | stdout | kaidoku |
| `tools/round-39/heldout-gen.py` | probe — seeded held-out generator (10 classes × 2) with optional `--run` | `0` written; `1` guard (existing out, unknown class, bad seed); REA failures recorded per carrier | none (determinism evidence wave-1 `R39C2HeldoutGen.md`) | seed = R39-C2 freeze hash | `--out` | kaidoku |
| `tools/round-39/c2-counter.py` | gate — R39-C2 depth, triage table on the held-out set | `0` met; `1` not met; `2` could-not-evaluate, including `frozen_path_changed` and `no_manifest_at_rev` | `--selftest` — 27 cases | `corpus/evidence/round-39/c2/heldout/manifest.json` | `--json-out` and a private scratch | kaidoku |
| `tools/round-39/absence-sweep.py` | gate — QUALITY 82: a negative existence claim is swept from every base its path may be relative to | `0` ABSENT; `1` PRESENT (hits listed); `2` usage/unreadable root | `--selftest` — 18 cases | — | stdout | kaidoku |

### Round-40 instrument registry

Added round 40. Every tool lives in `tools/round-40/`, honours `TMPDIR`/`$HYAKU_SCRATCH`, and was self-tested before the freeze `7fce3086` (receipts `.ufo/waves/round-40/controls/`). Score receipts are wrapped by `score-receipt.sh`, which records the scorer's exit code (routed R39-CL6). `tools/round-39/sqfs-triage.py` (row above) has no domain guard and labels non-firmware envelopes (routed R39-CL1); for routing use the v2 interpreter below.

| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `c1-counter.py` | gate — R40-C1 coverage (AVM layout); reruns REA on every carrier and compares the `plus-extractor` projection | `0` met; `1` not met; `2` unevaluable (`frozen_path_changed`, `rerun_disabled`, rerun env error) | `--selftest --pkg65 <rea-agents 6.5.0 root>` — 70 cases | `.ufo/waves/round-40/c1/{carriers.json,gap-rule.json}` | `--json-out`, scratch | kaidoku |
| `c1-extra.py` | gate — R40-C1 supplementary: oracle re-derived by the frozen reader, cited S-id absent at the base, frontier-note content | `0` met; `1` a binding false; `2` unevaluable | `--selftest` — 7 cases | carriers.json at the freeze | `--json-out`, scratch | kaidoku |
| `fetch-vendor.py` | probe — rebuilds non-redistributable vendor carriers from URL → image sha256 → tar member → carve → pin | `0` every chain verified; `1` a link broke (named); `2` usage | `--selftest` — 8 cases | carriers.json `external` | `--cache` dir | kaidoku |
| `sqfs-list.py` | gate (oracle) — independent SquashFS 4.0 reader, `--layout auto/le/be/avm`, fragments, gzip/xz, non-regular kinds | `0` listed; `2` unreadable/unsupported | `--selftest` — 13 cases | — | `--files`/`--nonregular` | kaidoku |
| `gen-squashfs.py` | probe — SquashFS writer; `--endian avm-genuine` writes the AVM layout (`avm` stays the marker-only transform) | `0` written; non-zero on bad tree | `--selftest` — 71 checks | — | output image | kaidoku |
| `mk-l-carriers.py` | probe — builds lane carriers L1 (xz) / L2 (gzip) deterministically | `0`; `2` usage; `3` writer failure | rebuild twice, compare sha256 | carriers.json pins | OUTDIR | kaidoku |
| `c1-run.sh` | probe — REA `extract-firmware --max-depth 1` after-arm and the reader oracle arm | `0` ok; `2` usage/env; `3` tool failure | `artifacts/R40C1Harness/selftest.sh` (wave 1) | — | OUTDIR, scratch | kaidoku |
| `sqfs-triage-v2.py` | gate (interpreter) — reads only SKILL table v2 (`<!-- sqfs-triage-table v2 -->` + action line), answers (label, action) | `0` labelled; `2` table missing/malformed (incl. duplicate label, unknown action) or envelope unreadable | `--selftest` — 45 cases | SKILL rule block 19 | stdout | kaidoku |
| `heldout-gen-v2.py` | probe — 13 classes × 2 seeded held-out carriers with (label, action) assigned before any REA run; `--run` | `0` written; guard errors non-zero | `--seed <hex> --selftest` — 6 checks | seed = R40-C2 freeze hash | `--out` | kaidoku |
| `c2-counter.py` | gate — R40-C2 depth, triage v2 on the held-out set | `0` met; `1` not met; `2` unevaluable (`no_manifest`, `frozen_path_changed`) | `--selftest` — 42 cases | `corpus/evidence/round-40/c2/heldout/manifest.json` | `--json-out`, scratch | kaidoku |
| `score-receipt.sh` | probe — wraps a counter run, records argv, exit code, UTC, counter sha256 | the wrapped exit code | `--selftest` — 51 cases | — | OUT.json | kaidoku |
| `ledger-status.py` | probe — fills per-seat status (ok/no-report/empty-report) into a copy of a wave results ledger | `0`; non-zero on unreadable input | `--selftest` — 43 checks | — | output copy | kaidoku |

### Round-44/45 instrument registry

Added round 45. The round-44 closure routed the missing registry rows for
`tools/round-44/{c1,c2}-counter.py`; this section registers the whole
claim-carrying instrument set of the two most recent frozen claim files, and
`tools/round-45/registry-scope.json` is the machine-readable scope that
`tools/round-45/c2-counter.py` scores (a row satisfies a scope path only when
its first cell is that exact backticked path). Every row was read from source
and its self-test run at the round-45 freeze `f762b727`; receipts
`.ufo/waves/round-45/w1/R45W1Reg*/`.

| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-44/c1-counter.py` | gate — R44-C1 coverage on four committed unblob v1/v2 fixtures; reruns REA on every carrier and compares the plus-extractor projection | `0` met; `1` not met; `2` could-not-evaluate, including `frozen_path_changed` and a failed caller-supplied rerun input | `python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root>` — 47 cases, green 2026-10-28 | `tools/round-44/carriers.json` and `corpus/evidence/round-44/c1/` at the freeze | `--json-out`, `--work` scratch | kaidoku |
| `tools/round-44/c1-run.sh` | probe — the after-freeze data procedure: one REA `extract-firmware` run per carrier, each written as a receipt tree; it does not run the oracle (`c1-oracle.py` is the counter's) | `0` every carrier produced a receipt, or `--dry-run` printed the plan and wrote nothing; `1` at least one carrier failed; `2` usage or environment refusal (`err()` in the script header) | none in the script — a bad-argument probe only, no self-test | `corpus/evidence/round-44/c1/carriers.json` pins; `HYAKU_SCRATCH` scratch base | the evidence root it is given, plus scratch | kaidoku |
| `tools/round-44/c2-counter.py` | gate — R44-C2 calibration: re-derives every frozen rubric statement at `--rev` | `0` met; `1` not met; `2` could-not-evaluate, including `frozen_path_changed` | `python3 -I -B tools/round-44/c2-counter.py --selftest` — green 2026-10-28 | `tools/round-44/c2-rubric.json` (frozen) and `plans/round-44-claims.md` | `--work`, `--json-out` | kaidoku |
| `tools/round-45/frozen-path-preflight.py` | gate — freeze integrity at commit time (M45-1 fix): arms `commit`, `restored`, `blob`, `dirty`, `pathspec` | `0` clean; `1` a frozen path changed, a restored touch, or a dirty worktree; `2` could-not-evaluate, including `pathspec_required` and an unknown or non-ancestor revision | `python3 -I -B tools/round-45/frozen-path-preflight.py --selftest` — 11 cases, green at the freeze | the caller's `--freeze`, `--pathspec` and `--freeze-path`; `plans/round-45-claims.md:132-147` names this round's frozen paths | `--json-out` only; selftest fixtures under `$HYAKU_SCRATCH` or `$TMPDIR` | kaidoku |
| `tools/round-45/c1-counter.py` | gate — R45-C1 depth: rule block 22 in `## Queue-drain craft`, its citations, and the interpreter's own selftest | `0` met; `1` not met (each false clause named in `failing`); `2` could-not-evaluate, including `frozen_path_changed` | `python3 -I -B tools/round-45/c1-counter.py --selftest` — 9 cases, green at the freeze | `SKILL.md` craft section, `tools/round-45/frozen-path-preflight.py`, `plans/round-45-claims.md` | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | kaidoku |
| `tools/round-45/c2-counter.py` | gate — R45-C2 calibration: every scope instrument has a registry row with a real exit map | `0` met; `1` not met (`unregistered`, `thin` or `scope_size`); `2` could-not-evaluate, including `frozen_path_changed` | `python3 -I -B tools/round-45/c2-counter.py --selftest` — 7 cases, green at the freeze | `tools/round-45/registry-scope.json` and the `SKILL.md` registry rows | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | kaidoku |

Limit: `c2-counter.py` checks that a row names the path, not that the tool exists at
`--rev` (routed R45-CL2). The scope is these six instruments only; rounds 41–43 tools stay
unregistered until a round censuses them (R45-CL3).

### Round-46 instrument registry

Added round 46. Round 45 registered the six instruments of rounds 44–45; this
section registers the whole census `tools/round-46/census.json`, generated by
`tools/round-46/census.py` from every `tools/round-4[1-6]/**.{py,sh}` path the
round-41..46 claim files name and which exists at the measured revision. The
section is bound by its two markers, so nothing outside it, inside a fence or
inside an HTML comment registers; cell 1 is exact path equality and cell 3 binds
each of 0, 1 and 2 to its meaning. `tools/round-46/registry.py` scores it and
`absent_at_rev` proves each named tool exists at the measured revision.

<!-- instrument-registry v2 -->

| tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-41/c1-counter.py` | gate — R41-C1 coverage: the four frozen AVM-layout big-endian SquashFS v4 carriers, their after-receipts, the oracle, the gap rule, a fresh REA rerun per carrier and the freeze-drift check | 0=met, met_target true and carriers_matched equal to the frozen target with every binding true; 1=not met, the measurement ran and at least one binding is false; 2=could-not-evaluate, Unevaluable (frozen_path_changed, a missing receipt or rerun environment, missing required arguments, or --no-rerun) | python3 -I -B tools/round-41/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 package root> — 97 cases, exit 0 on 2026-10-28 | .ufo/waves/round-41/c1/carriers.json and .ufo/waves/round-41/c1/gap-rule.json | --json-out receipt and --carrier-cache, plus scratch under HYAKU_SCRATCH/kaidoku-r41 | kaidoku |
| `tools/round-41/c1-extra.py` | gate — R41-C1 supplementary bindings the counter does not enforce: oracle_rederived re-runs the frozen sqfs-list.py reader on every pinned carrier and reproduces oracle.tsv and nonregular.tsv as row sets, sourced_new requires an S-id absent at --base and present at --rev with the round-41 entry in its used-by cell, frontier_content requires the round-41 frontier note to name the heading, the entry stem, a supersede verb and the round-40 measured-not-promoted record | 0=met, all three bindings true, or a selftest in which every case passes; 1=a binding false, or at least one selftest case fails; 2=unevaluable, from a non-commit --rev/--freeze/--base, carriers.json or the reader absent at --freeze, a missing --root/--rev/--freeze/--base, or a selftest whose tools dir lacks gen-squashfs.py and sqfs-list.py | python3 -I -B tools/round-41/c1-extra.py --selftest --tools tools/round-41 --work "$HYAKU_SCRATCH" — 17 cases, 17 pass, exit 0 on 2026-10-28 | .ufo/waves/round-41/c1/carriers.json (per-carrier sha256, oracle and nonregular paths) | --json-out FILE; scratch under $HYAKU_SCRATCH/kaidoku-r41 or --work | kaidoku |
| `tools/round-41/c1-run.sh` | probe — the round-41 C1 data procedure: arm after runs REA extract-firmware for one carrier into OUTDIR/after.json plus run.json, arm oracle builds the AVM-layout independent reader tables plus a sasquatch-v4be cross-check into oracle.tsv, nonregular.tsv and oracle-check.tsv; it scores nothing | 0=ok, the requested arm wrote its receipts; 1=no designed verdict, an unguarded command failure surfaces its own status under set -e; 2=usage or environment refusal (bad mode or arity, unreadable carrier, missing python3 or jq, a scratch without the /kaidoku-r41/ segment) | none — no --selftest in the script; the bad-argument probe exits 2 | none — the carrier sha256 and the tool versions are written into OUTDIR/run.json at run time | OUTDIR (after.json, run.json, oracle.tsv, nonregular.tsv, oracle-check.tsv, oracle-run.json) plus one scratch tree under HYAKU_SCRATCH, removed on exit | kaidoku |
| `tools/round-41/c2-controls.py` | R41-C2 control builder and scorer: builds CTL-C2-3/5/7, then scores SKILL.md and every CTL-*.md in --out with the frozen v3 interpreter against the independent evaluator on the dev set and reports the kill rule | 0=ok, no control reaches n/n so the kill rule does not fire; 1=not met, a control reaches n/n so the kill rule fires, or an uncaught crash; 2=argparse usage error, nothing evaluated | none | .ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json | --out control docs and --json-out receipt only; never the lane | kaidoku |
| `tools/round-41/c2-counter.py` | gate — R41-C2 depth: the frozen v3 triage interpreter and the frozen independent evaluator agree on every held-out envelope (twenty planned classes two each plus twelve combo) at --rev, and every binding holds (seed, carrier sha256, declared feature tuple, four real receipts) | 0=met, matched equals n and no binding false; 1=not met, a pair miss or a false binding, receipt still written; 2=unevaluable, frozen path changed, unknown or non-ancestor revision, or an absent or failing generator, evaluator or interpreter | python3 -I -B tools/round-41/c2-counter.py --selftest — 70 cases, 20 green 50 red, pass 70 fail 0, exit 0 on 2026-10-28 | plans/round-41-claims.md frozen paths plus the seed and carrier sha256 pins in corpus/evidence/round-41/c2/heldout/manifest.json | --json-out receipt; scratch under HYAKU_SCRATCH/kaidoku-r41 or the system temp dir, removed at exit | kaidoku |
| `tools/round-41/fetch-vendor.py` | probe - materialises the round-41 vendor C1 carriers into a cache, verifying url then image sha256 then tar-member sha256 then the nested SquashFS file sha256 then carving to its own bytes_used or length then the carrier pin, and failing closed so no cache entry appears on any broken link | 0=ok, every external carrier materialised and every chain hash matched; 1=a chain link failed, so nothing was written for that carrier; 2=usage refusal (no --cache, or neither --spec nor --root with --rev) | python3 -I -B tools/round-41/fetch-vendor.py --selftest (16 cases, pass=16 fail=0, run 2026-10-28) | .ufo/waves/round-41/c1/carriers.json holds per-carrier url, image_sha256, member_sha256, nested.sha256 and sha256 | --cache DIR carrier pin.bin entries and --image-cache DIR images; read-only on the lane tree | kaidoku |
| `tools/round-41/gen-squashfs.py` | probe — deterministic SquashFS v4 writer for the four endian modes le, be, avm and avm-genuine; the carrier generator for the round-41 held-out images | 0=image written with the single summary line wrote OUT N bytes inodes K mode M, or every selftest check passed; 1=a selftest check failed, or the writer raised before writing any image (uncaught KeyError on a missing or non-directory tree, OSError on an unwritable out path, so an input error is not distinguishable from a failed check); 2=argparse usage error (tree or out missing, or an invalid --endian or --comp choice) | python3 -I -B tools/round-41/gen-squashfs.py --selftest — 71 checks, 0 failed, exit 0 on 2026-10-28 | none — byte stability rests on fixed constants in the source (MKFS_TIME 1700000000, UID 1000, block size 4096) plus the selftest's deterministic-rebuild check, never on an in-repo pin file | the out image path given as the second positional only; selftest trees and images under $TMPDIR | kaidoku |
| `tools/round-41/heldout-gen-v3.py` | probe — seeded held-out SquashFS carrier generator, table-v3 classes, two replicates per class, with the label fixed by class before any REA run and an optional --run/--verify dev proof | 0=carriers written and, with --verify, every envelope reached its declared tuple (also the determinism selftest's 12 checks all pass); 1=a red outcome — a REA run error, a --verify miss, a failed selftest check, or a guard refusal (seed not at least 16 hex, missing --out, an existing manifest.json, --verify without --run); 2=argparse usage error only (missing --seed, unknown flag, a --actions-set value outside the choices) | `python3 -I -B tools/round-41/heldout-gen-v3.py --seed <freeze-hex> --selftest --scratch <scratch>` — 12 checks, green 2026-10-28 | none fixed — the caller's --seed selects the bytes, the optional --actions-file pin is checked against the class tokens, and the emitted manifest.json records the seed and every carrier sha256 | `--out` only, plus `--scratch` for trees and REA output dirs | kaidoku |
| `tools/round-41/indep-eval-v3.py` | probe — R41-C2 independent evaluator: transcribes the round-41 label precedence over envelope feature tuples and prints one (label, action) record per envelope, never reading the SKILL triage table, the interpreter or the generator | 0=every envelope in --envelopes was labelled (a per-envelope read error lands in the errors object, not in the exit) or the selftest passed; 1=a selftest case failed; 2=usage error only: no --envelopes, or a path that is not a directory, so there is no could-not-evaluate exit | python3 -I -B tools/round-41/indep-eval-v3.py --selftest — 46 cases, ok true, exit 0 on 2026-10-28 | plans/round-41-claims.md Label precedence steps it is transcribed from, its own bytes and ACTION_BY_LABEL pinned at the round-41 freeze | --out FILE only; stdout otherwise | kaidoku |
| `tools/round-41/local-source-gate.py` | report gate over corpus/SOURCES.md: every row whose URL cell is an out-of-lane absolute path must name an in-lane copy with a matching digest in the versioned sidecar map | 0=clean, every out-of-lane row resolved; 1=at least one row unresolved (map-missing, no-copy-named, copy-digest-mismatch, row-pin-conflict, sidecar or kind finding); 2=usage or parse error (root not a directory, unreadable --rev, malformed map, unknown map key, wrong table arity) | python3 -I -B tools/round-41/local-source-gate.py --selftest (23 cases, 0 failures) | corpus/evidence/local-sources.json (binds each out-of-lane absolute path to one in-lane copy plus its sha256; optional sha256_file sidecar and source_sha256) | none: stdout only, never writes the lane; --selftest writes only removed mkdtemp fixtures under TMPDIR | kaidoku |
| `tools/round-41/mk-l-carriers.py` | builder — writes the two lane-built R41-C1 carriers L3 (xz) and L4 (gzip) through the round-40 AVM-layout writer in avm-genuine mode, and prints one TSV line per carrier | 0=ok, both carriers built and, with --builds 2, each second build byte-identical to the first; 1=no verdict, never a verdict — no explicit path returns it and only an uncaught exception does, e.g. a writer that exits 0 without writing the image raises FileNotFoundError at the sha256 read; 2=usage or verification refusal before any build, argparse error, missing or non-empty outdir, or writer not found | none — no --selftest flag; --builds 2 rebuilds both carriers and exits 4 unless each second image is byte-identical to the first, run 2026-10-28 with rc 0 and both carriers build2-equal | none — it computes each carrier's sha256 into the printed TSV and --json but pins no file of its own; the writer it calls is tools/round-41/gen-squashfs.py | an existing empty outdir given as the positional argument, and the --json path; nothing else | kaidoku |
| `tools/round-41/sqfs-list.py` | probe - independent SquashFS 4.0 oracle reader (LE, standard BE, AVM layout) emitting a regular-file TSV of relpath, sha256 and size, a non-regular TSV, one-file extract and an inspect JSON summary | 0=enumerated every entry, or extracted the named file, or every self-test case passed; 1=a self-test case failed; 2=could-not-evaluate: unreadable image, bad magic, unsupported compression, truncated image, or a usage error | python3 -I -B tools/round-41/sqfs-list.py --selftest | none | the --files and --nonregular TSV paths, the --out extract path, and self-test temp images | kaidoku |
| `tools/round-41/sqfs-triage-v3.py` | probe — labels REA extract-firmware envelopes against the SKILL.md craft-section triage table v3 (first matching row supplies label and action; an envelope matching no row is unclassified) and never invokes REA or reads a carrier | 0=table parsed and every envelope printed one label line (unclassified included) or --table-only printed the rules, and --selftest green; 1=only a --selftest case failed, no envelope labelled; 2=could-not-evaluate: craft section, v3 marker, action vocabulary line or any cell malformed, a superseded v1/v2 table refused, envelope unreadable, or --skill omitted | python3 -I -B tools/round-41/sqfs-triage-v3.py --selftest (69 cases, pass 69, fail 0, exit 0 at the freeze) | the SKILL.md craft-section table behind the sqfs-triage-table v3 marker, read at --skill; no digest pin (DEFAULT_SKILL is the literal lane path) | none — read-only; --selftest writes one mkdtemp tree under TMPDIR and removes it | kaidoku |
| `tools/round-42/c1-counter.py` | gate — R42-C1 coverage: the SquashFS v3 handler family (standard, ddwrt, broadcom, both endiannesses) through REA, its after-receipts, the oracle, the gap rule, a fresh rerun per carrier and the receipt-identity stamp | 0=met, met_target true with every binding true, or --verify-receipt found a counter_sha256 that describes the counter file it names; 1=not met, the measurement ran with a false binding, or the receipt identity does not describe that file; 2=could-not-evaluate, Unevaluable (frozen_path_changed, a missing receipt or rerun environment, an unreadable --verify-receipt, missing required arguments, or --no-rerun) | python3 -I -B tools/round-42/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 package root> — 121 cases, exit 0 on 2026-10-28 | .ufo/waves/round-42/c1/carriers.json and .ufo/waves/round-42/c1/gap-rule.json | --json-out stamped receipt, --work scratch under HYAKU_SCRATCH/kaidoku-r42, --carrier-cache | kaidoku |
| `tools/round-42/c1-run.sh` | probe — the R42-C1 data harness: the after arm runs REA extract-firmware (rea-agents 6.5.0, unblob 26.6.4, plain sasquatch under a fixed PATH) and writes after.json plus run.json, the oracle arm runs sqfs3-oracle.py and writes oracle.tsv, nonregular.tsv, oracle-inner.json and oracle-run.json | 0=ok, the arm wrote its receipt and tables; 1=no verdict, no designed verdict — an unguarded command under set -e aborts with that command's status, which may be 1; 2=usage or environment refusal (bad argv, missing python3 or jq, carrier not a regular file, OUTDIR outside the round-42 evidence root, SCRATCH without a /kaidoku-r42/ segment, plain sasquatch not resolvable) | none — no self-test mode; bad-argument probes only (no args, unknown mode and a missing carrier each exit 2) | none — the carrier sha256 is taken from the argv file and the tool pins (rea-agents 6.5.0, unblob, sasquatch) are host paths recorded in run.json, not repo files | OUTDIR (corpus/evidence/round-42/c1/<id>: after.json, run.json, extract-env.json, or oracle.tsv, nonregular.tsv, oracle-inner.json, oracle-run.json) plus scratch under $HYAKU_SCRATCH/kaidoku-r42 | kaidoku |
| `tools/round-42/c2-controls.py` | probe — builds the round-42 C2 control documents plus the reference table from the lane SKILL.md and DEV envelopes, scores each with the draft-v4 interpreter against the precedence evaluator, and fires the C2 kill rule when any control reaches full score | 0=ok, no control reaches full score, the kill rule stays silent; 1=a control reaches full score so the kill rule fires, and by defect the same status also carries its own unevaluable SystemExit diagnostics (no DEV envelopes, failed feature extraction, failed evaluator); 2=argparse usage error or an unhandled IO failure | none — no --selftest in the script; the bad-argument probe exits 2 | none — the DEV replicas are caller-supplied, the default interp and eval paths are absent at the freeze | --out document directory and --json-out only | kaidoku |
| `tools/round-42/c2-counter.py` | R42-C2 counter: scores the SKILL v4 triage table against the frozen independent evaluator over held-out and legacy envelopes, with merge-aware freeze-integrity arms and its own fixture selftest | 0=target met, met_target true with every claim binding true; 1=not met, a pair miss or a binding false, receipt still written; 2=unevaluable, frozen path changed, unknown revision, or an absent or failed generator, evaluator or interpreter | python3 -I -B tools/round-42/c2-counter.py --selftest | corpus/evidence/round-42/c2/heldout/manifest.json | --json-out receipt and $HYAKU_SCRATCH/kaidoku-r42 scratch; no lane writes | kaidoku |
| `tools/round-42/fetch-carrier.py` | probe — materialises the round-42 C1 third-party carriers into a cache, fail-closed at every pin link (url, image sha256, container member, carve window, carve sha256) and refusing a symlinked cache, image-cache or work path | 0=every managed carrier materialised and verified, and at least one carrier was managed; 1=a chain link failed, named as link in the JSON receipt, with no cache entry for that carrier; 2=usage, unreadable spec, or an unusable work or cache path | python3 -I -B tools/round-42/fetch-carrier.py --selftest — 36 cases, pass 36 fail 0, exit 0 on 2026-10-28 | .ufo/waves/round-42/c1/carriers.json chain pins, the --repo-spec default | --cache entries, --image-cache entries, download staging in --work, --json-out | kaidoku |
| `tools/round-42/heldout-gen-v4.py` | probe - deterministic R42-C2 held-out SquashFS carrier generator (table-v4 classes, two replicates per class, pinned unblob legacy fixtures); --run executes one REA operation per carrier, --verify checks every envelope against its class tuple and regenerates the whole set byte-identically | 0=the selected set was generated, or under --run --verify every envelope matched its declared tuple and the byte-identical regeneration passed; 1=an aggregate check failed (a REA run errored, or an envelope or regeneration mismatched) and also every refusal the script raises itself as SystemExit text, which Python exits as 1; 2=usage error, argparse rejected the argv, so nothing was evaluated | python3 -I -B tools/round-42/heldout-gen-v4.py --seed 31820472784284727546808acc31b3ea1e73919b --selftest (17 checks passed, run 2026-10-28) | tools/round-42/fixtures.json holds the unblob 26.6.4 fixture pins; the committed copies live in corpus/evidence/round-42/c2/fixtures | --out DIR carrier set plus --scratch trees and fixture cache; read-only on the lane tree | kaidoku |
| `tools/round-42/indep-eval-v4.py` | probe — independent evaluator that maps one triage envelope to the round-42 (label, action) step 1-15 classification without invoking the extractor | 0=ok, one record printed or written for the single envelope, or the batch payload emitted for a directory; 1=at least one selftest case failed; 2=usage or I/O error (no envelope and no --envelopes, unreadable or non-object JSON, or a --envelopes path that is not a directory) | python3 -I -B tools/round-42/indep-eval-v4.py --selftest — 45/45 cases, 0 failures, exit 0 on 2026-10-28 | none — the 15-step precedence table and its label-action vocabulary are constants in the source, not a pin file | the --out file only; stdout when --out is absent; selftest needs no writes outside $TMPDIR | kaidoku |
| `tools/round-42/prefile-gate.py` | gate — pre-file check that every wave is settled, the round scopes are clean, the lane root has no stray .err, and every w*/<Name>.md citation in the lesson resolves in HEAD | 0=GATE GREEN, all four conditions a to d pass; 1=GATE RED, at least one condition FAIL (a root that is not a directory or not a work tree also exits 1, via SystemExit, although nothing was evaluated); 2=argparse usage error (no --root/--round and no --selftest, unknown flag) | `python3 -I -B tools/round-42/prefile-gate.py --selftest --work <existing dir>` — 12 cases, green 2026-10-28 | none — it reads HEAD of the caller's --root and pins no file of its own | none at all, read-only; selftest fixtures go under --work or TMPDIR | kaidoku |
| `tools/round-42/sqfs-triage-v4.py` | probe — R42-C2 interpreter: labels each REA envelope with (label, action) by matching the SKILL craft-section SquashFS triage table v4, and validates that table alone under --table-only | 0=envelopes labelled, or the table validated by --table-only (15 rules from the lane SKILL.md, 2026-10-28), or the selftest passed; 1=a failed --selftest only; 2=table missing, refused by a v1/v2/v3 marker, or malformed, an envelope unreadable, or a usage error | python3 -I -B tools/round-42/sqfs-triage-v4.py --selftest — 123 cases, 123 pass, 0 fail, exit 0 on 2026-10-28 | SKILL.md rule block 21 v4 triage table, frozen at the round-42 freeze; tools/round-42/fixtures.json pins the envelope fixtures | none — stdout only, and the selftest writes its SKILL variants under a TMPDIR work dir | kaidoku |
| `tools/round-42/sqfs3-oracle.py` | independent multi-producer oracle for a carved SquashFS v1-v3 image: unsquashfs-backhand (primary) and 7-Zip must agree on path set, kind, sha256 and size, with unsquashfs 4.7.5 as the third producer wherever it reads the image, and tables written only on agreement | 0=ok, producers agree and oracle.tsv plus nonregular.tsv are written; 1=the inline selftest failed (never a verdict on an image); 2=image unreadable, wrong magic or unsupported major, or a required producer missing or incomplete | python3 -I -B tools/round-42/sqfs3-oracle.py --selftest --work SCRATCH (0 failures) | each run's oracle-run.json records the input image sha256, the magic-normalized copy sha256, per-producer argv and exits and the cross-check verdict; no persisted expected baseline | --work extraction roots (default TMPDIR; a run with neither --work nor TMPDIR is refused) plus --files, --nonregular, --json, or --out | kaidoku |
| `tools/round-42/unblob-logtee.sh` | probe — R42-C1 log tee: runs the real unblob with REA's arguments unedited, then copies unblob's --log file to C1_LOG_COPY when that variable and the log file both exist | 0=ok, the wrapped unblob returned 0, log copied when C1_LOG_COPY names an existing destination; 1=not met, the wrapped unblob's own non-zero code propagated unchanged and no verdict of its own is made; 2=refusal before any run, C1_REAL_UNBLOB is not an absolute path | none — no --selftest flag; the only check is the pre-run absolute-path refusal | none — it reads C1_REAL_UNBLOB (default realpath of ~/.local/bin/unblob) and C1_LOG_COPY from the environment and pins no file | the C1_LOG_COPY destination only; it never edits an argument, the input, the output or the log | kaidoku |
| `tools/round-43/c1-counter.py` | gate - R43-C1 depth counter: runs the frozen v4 triage interpreter and the frozen independent evaluator over the seeded held-out envelope set and requires every label and action pair to agree plus every declared binding true | 0=met, met_target true, every held-out pair matched and every binding true; 1=not met: at least one pair miss or one binding false, the receipt still written; 2=could-not-evaluate: frozen_path_changed, freeze not an ancestor of rev, unknown revision, absent or unparsable manifest, or a frozen tool failing to run | python3 -I -B tools/round-43/c1-counter.py --selftest | tools/round-42/sqfs-triage-v4.py and tools/round-42/indep-eval-v4.py pinned at anchor d1681696, with corpus/evidence/round-43/c1/heldout/ | the --json-out receipt and a private scratch dir under HYAKU_SCRATCH removed at exit | kaidoku |
| `tools/round-43/c2-score-r43.py` | gate — R43-C2 calibration in a detached clone at --rev: drives the local-source gate and the hardened copy/provenance verifier through receipt-wrap, then binds 13 checks (tool bytes frozen, clone clean, freeze ancestor, gate rows 137/19 and empty rows_failed, 136 audit checks with 0 failures, map digest, SOURCES numstat, S126 preserved) into one receipt | 0=met, all 13 checks true; 1=not met, at least one check false, including a gate or audit sub-receipt that could not be produced at all; 2=could-not-evaluate: the clone cannot be made, or a usage/argument error | none — no selftest flag exists; only --help and a bad-argument probe | corpus/evidence/local-sources.json, whose sha256 3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e is pinned in the source as MAP_SHA256, plus the S126 tsv path | the --scratch clone and its receipt files, and --json-out | kaidoku |
| `tools/round-43/heldout-gen-v4r43.py` | gate — R43-C1 held-out generation: rebuilds the table-v4 class carriers from the seed and refuses to write a manifest unless every carrier's declared tuple equals its measured tuple | 0=clean, carriers built or the declared-versus-measured tuple check passed, with --verify and byte-identical regeneration where asked; 1=not met, an REA run failed, a --verify or regeneration comparison differed, or the CLI refused an argument; 2=could-not-evaluate, --tuple-check found no manifest.json to check | python3 -I -B tools/round-43/heldout-gen-v4r43.py --selftest-tuple --scratch <dir> — 17 of 17 checks passed, exit 0 on 2026-10-28 | tools/round-42/fixtures.json (the fixture URL and sha256 pins, resolved when no fixtures.json sits beside the script) | --out carrier and manifest tree, --scratch tree and fixture cache | kaidoku |
| `tools/round-43/verify-copies-r43.py` | gate — R43-C2 landing verifier for the local-sources pack: map shape and key set against the frozen gate's own path extraction, copy regularity, stated dir, digest and byte-identity, member pins from the round-42 EXPECT table plus the S048 extension, host or upstream identity, and the freeze binding of the imported verifier | 0=every emitted check OK (exit 0 only when the failure count is 0); 1=at least one emitted check FAIL, or an unhandled error such as an absent map; 2=argparse usage error, a required --root, --rev or --freeze missing | none — no --selftest; probe with --help (0) or no args (2) | corpus/evidence/local-sources.json (--map: per-entry sha256 and source_sha256 pins) | none — stdout only | kaidoku |
| `tools/round-44/c1-counter.py` | gate — R44-C1 coverage: re-derives the four frozen SquashFS v1 and v2 carriers (layout, carve, oracle census, gap rule), re-runs REA extract-firmware to compare the plus-extractor projection, and re-checks a receipt identity under --verify-receipt | 0=target met, every carrier clause and binding true; 1=not met, a named false clause or binding or a red selftest case; 2=could-not-evaluate, including frozen_path_changed, bad args, node or REA failure and rerun_disabled | python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> — 47 cases, green | tools/round-44/carriers.json, tools/round-42/fixtures.json and tools/round-42/prior-pins.json | --json-out plus a private --work scratch tree | kaidoku |
| `tools/round-44/c1-run.sh` | R44-C1 after-freeze data driver: pins PATH and the scratch base, then execs c1-run.py, refusing the committed evidence root unless --data-run or KAIDOKU_C1_DATA_RUN=1 states the freeze is in place | 0=ok, every carrier ran and produced a receipt; 1=at least one carrier failed, by REA exit, no receipt, or a pin mismatch; 2=could not evaluate, usage, environment, missing sibling tool, or an occupied evidence dir | none | tools/round-44/carriers.json | corpus/evidence/round-44/c1 only under --data-run or KAIDOKU_C1_DATA_RUN=1, plus the $HYAKU_SCRATCH/kaidoku-r44 scratch | kaidoku |
| `tools/round-44/c2-counter.py` | gate — R44-C2 calibration: re-derives every frozen rubric statement at --rev by running the rubric's own check argv in an exported scratch clone, so an appended note is never evidence | 0=met, no mismatch, no unevaluable entry, frozen paths clean and at least one entry evaluated; 1=not met, a mismatch with nothing unevaluable, the receipt still written, and a pre-freeze census mismatch is not a claim score; 2=could-not-evaluate, malformed rubric, frozen path changed, absent frozen file, no evaluable entry or a check that cannot run | python3 -I -B tools/round-44/c2-counter.py --selftest — 24 arms, ok true, exit 0 on 2026-10-28 | tools/round-44/c2-rubric.json and the counter sha256 pin at the freeze, read as claim_gate.usable_as_claim_score | --work scratch clone, removed unless --keep-work; --json-out | kaidoku |
| `tools/round-45/c1-counter.py` | gate - R45-C1 depth at a revision: rule block 22 (marker freeze-integrity-table v1) inside the Queue-drain craft section, its data rows, its resolving path-and-line citations, the S140 and interpreter citations, the interpreter present at rev, and that interpreter own selftest | 0=met, every clause true at --rev; 1=not met, each false clause named in failing; 2=could-not-evaluate (usage, unknown or non-ancestor revision, SKILL.md absent, or frozen_path_changed) | python3 -I -B tools/round-45/c1-counter.py --selftest (9 cases, failures=0, run 2026-10-28) | plans/round-45-claims.md and the tools/round-45/ directory freeze, plus tools/round-45/frozen-path-preflight.py | --json-out only; selftest fixtures under HYAKU_SCRATCH or TMPDIR, removed before exit | kaidoku |
| `tools/round-45/c2-counter.py` | gate — R45-C2 calibration: every instrument listed in the frozen scope file owns a SKILL.md registry row whose verdict cell names 0, 1 and 2 | 0=met (unregistered, thin and scope_size all clean); 1=not met (a scope path unregistered, a thin verdict cell, or scope_size other than 6), and also the exit of an uncaught OSError when --json-out points into a missing directory, so an IO failure is not distinguishable from a scored not-met; 2=could-not-evaluate (unknown revision, freeze not an ancestor of rev, SKILL.md or the scope file absent at rev, or frozen_path_changed) | python3 -I -B tools/round-45/c2-counter.py --selftest — 7 cases, 0 failures, exit 0 on 2026-10-28 | tools/round-45/registry-scope.json (6 paths) with plans/round-45-claims.md as the frozen set | the --json-out file only; selftest fixture repositories under $HYAKU_SCRATCH or $TMPDIR | kaidoku |
| `tools/round-45/frozen-path-preflight.py` | gate — freeze integrity before a commit counts as landed, with arms commit, blob, restored, dirty (--check-dirty) and pathspec (--require-pathspec) | 0=clean, no frozen path touched in FREEZE..REV, every frozen blob identical, nothing restored and the worktree clean under the pathspec; 1=violation, verdict frozen_path_changed with the offending commits and paths listed; 2=could-not-evaluate — usage, unknown or non-ancestor revision, a frozen directory left uncovered under --require-pathspec, or a failing git call | `python3 -I -B tools/round-45/frozen-path-preflight.py --selftest` — 11 cases, green 2026-10-28 | none built in — the caller supplies --freeze, --freeze-path and --pathspec; plans/round-45-claims.md names the round-45 set | `--json-out` only; selftest fixtures under $HYAKU_SCRATCH or $TMPDIR | kaidoku |
| `tools/round-46/attest.py` | gate — R46-C1 freeze-integrity counter: scores SKILL rule block 23 against the frozen clauses and runs the nine-forgery discrimination battery, which must score every forgery red and the genuine block green | 0=met with failing empty; 1=not met, each false clause named in failing; 2=could-not-evaluate: unknown or non-ancestor revision, malformed claims file or craft heading, frozen_path_changed, a refused --json-out, an unusable scratch root, or an unhandled exception | python3 -I -B tools/round-46/attest.py --selftest --root . --freeze HEAD --rev HEAD — green, exit 0 on 2026-10-28; 15 cases at the 3182047 and 50862e4a bytes, 16 from the F3 repair at 65678df0 onward; --root/--freeze/--rev are required even for --selftest | plans/round-46-claims.md (frozen) plus the sha256 pin of its own bytes in SKILL.md rule block 23 | --json-out only, refused inside any graded or frozen surface and outside the lane root; selftest and battery fixture repos under HYAKU_SCRATCH or TMPDIR | kaidoku |
| `tools/round-46/census.py` | census generator: emits the R46-C2 scope, every tools/round-4[1-6] py or sh path named in a plans/round-4[1-6]-claims.md at --rev that exists there, with named_but_absent kept out of scope | 0=ok, census computed and printed, and written when --out is given; 1=no verdict, an unhandled exception such as an unwritable --out, a traceback and not a verdict; 2=usage error from argparse (missing --root or an unknown flag) | none | tools/round-46/census.json is the pinned output; the tool re-derives it byte-identically at the freeze | --out only; stdout only without it | kaidoku |
| `tools/round-46/gate.py` | gate — round-46 freeze-integrity core shared by attest.py and registry.py, with the merge-aware history arm, the independent blob arm, the derived frozen set, the scratch-root refusal and the graded-surface output refusal | 0=clean, both arms agree that no frozen path changed in FREEZE..REV and the freeze is an ancestor of rev; 1=no verdict, not a verdict — running gate.py as a program refuses with "gate.py is a library" and evaluates nothing, and no library entry point returns 1; 2=could-not-evaluate, unknown or non-ancestor revision, absent claims file or Frozen paths section, failed git call, refused --json-out target, missing non-temporary scratch root, or any unhandled exception caught by main_guard | none — no --selftest of its own; the shared core is exercised by python3 -I -B tools/round-46/registry.py --root <root> --freeze <freeze> --rev <rev> --selftest, green 2026-10-28 cases=12 failures=0, and those three arguments must be supplied before --selftest is honoured | none — it pins no value of its own; the caller supplies --root, --freeze and --rev, and attest.py pins its own bytes by sha256 | the caller's --json-out, which must resolve inside the lane root and outside SKILL.md, LOG.md, SCORECARD.md, PROVINCE.md, SHONEN.md, plans, tools, corpus and evidence; plus a scratch dir under HYAKU_SCRATCH or TMPDIR | kaidoku |
| `tools/round-46/registry.py` | gate - R46-C2 calibration counter: scores the marker-bound SKILL instrument-registry section against tools/round-46/census.json, requiring exact cell-0 path equality, the house header, a bound verdict map per row and presence at the measured revision, and rejects all seven forgery classes | 0=met: no unregistered, thin or absent-at-rev path and the battery reports seven forgeries green under v1 and none under v2; 1=not met: an unregistered, thin or absent-at-rev path, or a battery count off target; 2=could-not-evaluate: missing or doubled markers, absent census, absent SKILL.md at rev, frozen_path_changed, or no scratch root | python3 -I -B tools/round-46/registry.py --selftest --root . --freeze 0 --rev 0 | tools/round-46/census.json | the --json-out receipt and a private scratch dir under HYAKU_SCRATCH for the forgery battery | kaidoku |

| `tools/round-47/exact.py` | gate — R47-C1 exactness counter: scores SKILL rule block 24 with exact arm tokens, exactly-once routed ids, a `mutations_sha256` pin over its own mutation list, a flag-order clause over `tools/round-46/gate.py`, and a four-forgery discrimination battery scored under both profiles | 0=met with `failing` empty; 1=not met, each false clause named; 2=could-not-evaluate: unknown or non-ancestor revision, malformed claims file or craft heading, `frozen_path_changed`, a refused `--json-out`, an unusable scratch root, or an unhandled exception caught by `main_guard` | `python3 -I -B tools/round-47/exact.py --selftest --root . --freeze <F> --rev <R>`: 16 cases, exit 0 at `5017e1f7` | `tools/round-47/exact.py` (self pin `interpreter_sha256`) | none — writes only the `--json-out` receipt | kaidoku |
| `tools/round-47/record.py` | gate — R47-C2 calibration counter: re-derives every machine-checkable atom of the last two `## Round N` sections of `SCORECARD.md` and the current `## Owned axes` head fractions (`seats`, `window`, `path`, `rev`, `axes`) and requires zero mismatches with at least two self-re-deriving corrections | 0=met; 1=not met, mismatches and bad corrections listed; 2=could-not-evaluate: unknown revision, absent `SCORECARD.md`, fewer than two round sections, a refused `--json-out`, or an unhandled exception | `python3 -I -B tools/round-47/record.py --selftest --root . --rev <R>`: 9 cases, exit 0 at `5017e1f7` | none — the counter's own bytes are not pinned by the block | none — writes only the `--json-out` receipt | kaidoku |
| `tools/round-48/meanings.py` | gate — R48-C1 depth: SKILL craft rule block 25 (marker verdict-meaning-table v1), its per-id expected arms and pins, and the instrument-registry section re-bound to tools/round-48/census2.json by meaning class, with a four-forgery battery | 0=met, every clause true at --rev and the battery green on the genuine block; 1=not met, each false clause named in failing; 2=could-not-evaluate, unknown or non-ancestor revision, malformed craft heading, frozen_path_changed, a refused --json-out, or an unhandled exception | python3 -I -B tools/round-48/meanings.py --selftest — 18 cases, exit 0 on 2026-10-28 | tools/round-48/census2.json and the interpreter pin in block 25 | --json-out receipt only; fixtures under HYAKU_SCRATCH | kaidoku |
| `tools/round-48/record2.py` | gate — R48-C2 calibration: the round-47 atom oracle executed from the bytes at --rev, a per-section completeness floor, re-derived corrections (seats/window/path/rev/axes/quote), quoted receipt numbers and the Owned-axes score cell, with a five-forgery battery | 0=met, the oracle accepts the card and every clause holds; 1=not met, each false clause named in failing; 2=could-not-evaluate, unknown revision, fewer than two round sections, an absent oracle, or an unhandled exception | python3 -I -B tools/round-48/record2.py --selftest — parser cases only, exit 0 on 2026-10-28 | none — the round-47 oracle committed bytes are the pin | --json-out receipt only; never the lane | kaidoku |
| `tools/round-49/c1-counter.py` | gate — R49-C1 coverage: SquashFS v1/v2 through REA extract-firmware on four carriers (receipts, oracle, gap rule, rerun projection, documentation bindings), run as `python3 -I -B tools/round-49/c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 PKG` | 0=met, every clause true at --rev (and, where a battery exists, a clean battery); 1=not met, a named clause or binding false; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, a rerun environment error or a refusal | python3 -I -B tools/round-49/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> (52 cases per the round-49 wave-2 seat W2C1Selftest) | tools/round-49/carriers.json and the freeze pins | --json-out and a private scratch under $HYAKU_SCRATCH/kaidoku-r49/counter | kaidoku |
| `tools/round-49/c1-controls.py` | probe — R49-C1 counterfactual control driver: plants control trees in shared-clone sandboxes and scores the frozen counter, run as `python3 -I -B tools/round-49/c1-controls.py` | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | python3 -I -B tools/round-49/c1-controls.py --selftest (stub counter, driver machinery only) | tools/round-49/control-fixtures/** | --out and --json-out; sandbox clones under --work; never the lane | kaidoku |
| `tools/round-49/c1-oracle.py` | probe — R49-C1 frozen oracle builder: unsquashfs 4.7.5 census, per-file sha256 and the unblob __output__ second reading per carrier, run as `python3 -I -B tools/round-49/c1-oracle.py` | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | python3 -I -B tools/round-49/c1-oracle.py --selftest | tools/round-49/carriers.json (per-carrier oracle block) | --work, --json-out and --receipt only | kaidoku |
| `tools/round-49/c1-run.py` | probe — R49-C1 after-freeze data runner: REA extract-firmware per carrier into corpus/evidence/round-49/c1/<id>/, run as `python3 -I -B tools/round-49/c1-run.py --dry-run` (a dry run writes nothing) | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | none — no --selftest flag exists; --dry-run is the only no-write mode | tools/round-49/carriers.json | the round-49 evidence root only under --data-run; scratch $HYAKU_SCRATCH/kaidoku-r49 | kaidoku |
| `tools/round-49/c1-run.sh` | probe — wrapper around c1-run.py that pins the child PATH and scratch base, run as `bash tools/round-49/c1-run.sh --dry-run` | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | none — no self-test; the wrapper passes --help and --dry-run to c1-run.py | tools/round-49/carriers.json | as c1-run.py | kaidoku |
| `tools/round-49/c2-mismatch.py` | gate — R49-C2 calibration: nine round-48 atoms A1..A9 re-derived from committed bytes, run as `python3 -I -B tools/round-49/c2-mismatch.py --root LANE --rev REV --freeze FREEZE --battery` | 0=met, every clause true at --rev (and, where a battery exists, a clean battery); 1=not met, a named clause or binding false; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, a rerun environment error or a refusal | none — the file has no --selftest flag; the hermetic self-test is python3 -I -B tools/round-50/selftest-r49-c2.py --lane . (40 cases) | none — the pinned values are the LANE_BASE, R48_BASE and R48_TIP constants in the source | --json-out only | kaidoku |
| `tools/round-50/c1-counter.py` | gate — R50-C1 coverage: genuine AVM-marker little-endian SquashFS v4 (hsqs) members of four FRITZ!OS images through REA extract-firmware (receipts, oracle re-derivation, gap/removal rule, parameters, rerun projection on the pinned REA package, documentation bindings), run as `python3 -I -B tools/round-50/c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 PKG --carrier-cache CACHE` | 0=met, every clause true at --rev (and, where a battery exists, a clean battery); 1=not met, a named clause or binding false; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, a rerun environment error or a refusal | python3 -I -B tools/round-50/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> — 169 cases, exit 0 on 2026-10-28 | tools/round-50/carriers.json, gap-rule.json and oracle/** frozen at the freeze | --json-out and a private scratch under $HYAKU_SCRATCH/kaidoku-r50/counter | kaidoku |
| `tools/round-50/c1-run.sh` | probe — R50-C1 run harness: arm `after` runs REA extract-firmware on a carved carrier and writes the receipt, arm `oracle` derives the oracle with three readers, run as `bash tools/round-50/c1-run.sh after --id ID --carrier FILE --data-run` | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | none — no self-test; the oracle arm cross-checks three independent readers and exits 3 on disagreement | tools/round-50/carriers.json | corpus/evidence/round-50/c1/<id>/ only under --data-run; scratch $HYAKU_SCRATCH/kaidoku-r50 | kaidoku |
| `tools/round-50/c1-controls.py` | probe — R50-C1 control driver: gen builds and score plants the committed control fixtures (do-nothing, round-41 BE receipts, oracle forgery, sasquatch absent, standard LE carrier, positive) and scores the frozen counter, run as `python3 -I -B tools/round-50/c1-controls.py score --lane LANE --freeze FREEZE` | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | python3 -I -B tools/round-50/c1-controls.py selftest --work DIR (positional spelling, no --selftest flag; 20 cases, exit 0 on 2026-10-28) | tools/round-50/control-fixtures/** (manifest sha256 per file) | --out and --json-out; sandbox clones under --work; never the lane | kaidoku |
| `tools/round-50/fetch-vendor.py` | probe — R50-C1 carrier custody: materialises the chain-pinned vendor carriers (image sha256, tar member, carve to bytes_used, carrier sha256) from download.avm.de only, run as `python3 -I -B tools/round-50/fetch-vendor.py --spec FILE --cache DIR` | 0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; 2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal | python3 -I -B tools/round-50/fetch-vendor.py --selftest — 16 cases, exit 0 on 2026-10-28 | tools/round-50/carriers.json | --cache and --image-cache outside the lane only; refuses a lane-resident directory | kaidoku |
| `tools/round-50/c2-record.py` | gate — R50-C2 calibration: eleven round-48/49 record atoms B1..B11 re-derived from committed bytes with a single-mutation battery, run as `python3 -I -B tools/round-50/c2-record.py --root LANE --rev REV --freeze FREEZE --battery` | 0=met, every clause true at --rev (and, where a battery exists, a clean battery); 1=not met, a named clause or binding false; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, a rerun environment error or a refusal | python3 -I -B tools/round-50/c2-record.py --selftest --root . — 29 cases, exit 0 on 2026-10-28 | none — the pinned values are the BASE and R48_TIP constants in the source | --json-out and a scratch under --work or TMPDIR only | kaidoku |
| `tools/round-50/selftest-r49-c2.py` | gate — hermetic self-test of the frozen round-49 counter c2-mismatch.py over fixture clones of the real history (40 cases), run as `python3 -I -B tools/round-50/selftest-r49-c2.py --lane LANE` | 0=met, every clause true at --rev (and, where a battery exists, a clean battery); 1=not met, a named clause or binding false; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, a rerun environment error or a refusal | none — this file is the self-test; --mutant-counter PATH judges a mutant counter and exits 1 when it is caught | tools/round-50/selftest-r49-c2.expected.json (hand-written expected values, counter sha256 pinned) | --work and --json-out outside the lane only | kaidoku |
<!-- /instrument-registry -->
