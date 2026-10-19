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

Current REA package inventory by configured client (re-read 2026-10-18): Devin/OMP
`rea-agents@6.5.0` (207 MCP tools / 153 CLI commands); Kimi
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

The rows below are this lane's registered verdict scripts: the interactive-r1
recovery gate and the citation-drift probe. Neither validates REA correctness,
outside review, canonical judgment, or fleet acceptance. Evidence and limits:
`corpus/lessons/2026-10-15-round-1-recovery.md`; `LOG.md`, Interactive round-1 recovery.

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate; `--admission` checks this recovery's unresolved prerequisites and returns 2, never native judgment | same command with `--selftest`; asserts isolated subprocess exit codes and stable finding IDs | `.ufo/rounds/interactive-r1/expected.json` pins every snapshot input and expected outcome; normal entry read-only in this repo; selftest creates and removes only its isolated fixture directory under `.ufo/rounds/interactive-r1/` |
| citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate, unchanged — a guard failure lands in the 2 bucket in both modes and drift findings still never leave 0 in probe mode**; **preflight table guard: `expected.json` pins the sha256 of `pointer-table.json`, and a table that is absent, unreadable, unpinned, or whose digest does not match the pin is could-not-evaluate (exit 2) before any entry is evaluated, so a tampered table can never read as silent findings** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the dead/absent `--rev` case → exit 2, finding `revision_unresolvable`; the guard cases: a clean tree passes, a digest-mismatched table → exit 2, finding `table_tampered`, an absent table → exit 2, finding `pointer_table_unreadable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation; `expected.json` pins the sha256 of `pointer-table.json` itself plus the self-test case table; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
