# CN-1 — arc3-loop1-round11 reconciliation verdict

**Overall:** C1 has a fresh, independently reproduced `inspect_artifact` Evidence-ID candidate, but its required corpus/map landing and 90/90 Command A result remain **UNVERIFIABLE**. C2’s Ghidra, pacman, and bounded ASAR counts are **REPRODUCED**. C3’s provider capability group is **REPRODUCED** as `available:true`; in a targetless `binary_session {}`, each individual artifact tool is `available:false` with `target_required`, so the row needs that scope distinction. The attached Kimi session remains **UNVERIFIABLE**.

This verdict reports my measurements separately from peer submissions. I did not edit corpus, map, PROVINCE, SKILL, SCORECARD, LOG, gate source, custody files, or any other seat’s artifact; no Git mutation was performed.

## C1 — coverage

### Independent measurement and acceptance status

I re-ran Command A from `SCORECARD.md:88-124` against both source revisions, using immutable Git objects. The exact outputs were:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fe","rule_blocks":16}
```

`git rev-parse` independently resolved `9c1d1fe` to `9c1d1fef5595b55d65764626249f164e6816473a`. Thus the available HEAD/work baselines are both 89/89; no round-11 after-state has been measured. Current Git status showed no corpus or `corpus/README.md` edit. **C1 closure / 90 files, 90 mapped, no missing or dangling: UNVERIFIABLE pending co-landing and a fresh Command A run.**

### Fresh `inspect_artifact` re-probe

To check the proposed third `ev_` verb-family candidate, I ran REA 6.7.0 `inspect-artifact` twice on `/usr/bin/jq`, then on a byte-identical copy under `/var/tmp`. The temporary copy and REA scratch were removed at command completion. The three full JSON envelopes were reduced to the listed identity fields. The source projection checked was `dist/domain/evidence.js:159-183`; canonical SHA-256 serialization is defined in `dist/domain/canonicalDigest.js:8-25,27-76`.

Command:

```sh
REA=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
SCRATCH=$(mktemp -d /var/tmp/kaidoku-cn1-c1.XXXXXX)
trap 'rm -rf "$SCRATCH"' EXIT
cp /usr/bin/jq "$SCRATCH/jq-copy"
for path in /usr/bin/jq /usr/bin/jq "$SCRATCH/jq-copy"; do
  TMPDIR="$SCRATCH" node "$REA" inspect-artifact "$path" --format json --full-output \
    | python3 -c 'import json,sys; d=json.load(sys.stdin)["data"]; sub=d["normalized_result"]["substeps"][0]["evidence"]; print(json.dumps({"operation":d["operation"],"evidence_id":d["evidence_id"],"subject_sha256":d["subject"]["digest"]["sha256"],"inspection_id":d["normalized_result"]["inspection_id"],"nested_inventory_id":sub["evidence_id"],"nested_path":sub["subject"]["local_path"]}, sort_keys=True))'
done
```

Exact first-hand output:

```text
sha256sum /usr/bin/jq /var/tmp/kaidoku-cn1-c1.BduNoQ/jq-copy
 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /var/tmp/kaidoku-cn1-c1.BduNoQ/jq-copy

{"evidence_id":"ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca","inspection_id":"ai_78cf490802e595884543670257cc4f4e11b4169f1fc14e2e53c755e4168883e2","nested_inventory_id":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_path":"/usr/bin/jq","operation":"inspect_artifact","subject_sha256":"e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"}
{"evidence_id":"ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca","inspection_id":"ai_78cf490802e595884543670257cc4f4e11b4169f1fc14e2e53c755e4168883e2","nested_inventory_id":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_path":"/usr/bin/jq","operation":"inspect_artifact","subject_sha256":"e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"}
{"evidence_id":"ev_629d930cceee031a24ee0268e9871d37762191a4cd670f95e77702e0d24ad9df","inspection_id":"ai_857f7eaaa8e2ed4da86aa7cdf349cd2bb27396c0eb074d8292e8ae38bc019c6a","nested_inventory_id":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_path":"/var/tmp/kaidoku-cn1-c1.BduNoQ/jq-copy","operation":"inspect_artifact","subject_sha256":"e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"}
```

I separately reimplemented the projection and canonical SHA-256 calculation from the cited package source, and re-derived both the outer and nested IDs for all three fresh envelopes:

```text
same_sha256=true
{"target":"/usr/bin/jq","operation":"inspect_artifact","outer_reported":"ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca","outer_recomputed":"ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca","outer_match":true,"nested_reported":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_recomputed":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_match":true}
{"target":"/usr/bin/jq","operation":"inspect_artifact","outer_reported":"ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca","outer_recomputed":"ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca","outer_match":true,"nested_reported":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_recomputed":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_match":true}
{"target":"/var/tmp/kaidoku-cn1-id-check-q9HoMi/jq-copy","operation":"inspect_artifact","outer_reported":"ev_a80c9f10477c865bb658699de549fca6a5b5ad9dac85c69ed530fd982fa3b857","outer_recomputed":"ev_a80c9f10477c865bb658699de549fca6a5b5ad9dac85c69ed530fd982fa3b857","outer_match":true,"nested_reported":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_recomputed":"ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435","nested_match":true}
```

**Candidate verdict: REPRODUCED, bounded.** Same-path repeats gave the same outer ID; a same-byte alternate path changed the outer ID while preserving the nested inventory ID. This independently supports the `inspect_artifact` third-family candidate, not a universal rule for every REA operation or invocation shape.

### Reconcile the C1 drafts

All eight C1 reports had appeared in the last inventory. Several propose the same single `inspect_artifact` corpus filename/token: CR-2, EX-2, EX-4, and EX-5. Their different carriers do not create four distinct unknown closures. My live `/usr/bin/jq` result directly supports the CR-2 draft’s measured shape; I recommend choosing that draft as the single base, then co-landing its entry and token in the **Evidence model** row (`corpus/README.md:41`). EX-4 is a separate ASAR corroboration but carries an explicit integrity-mismatch / `record-and-continue` boundary (`claims/c1/EX-4.md:26-35`); EX-2 and EX-5 propose the same operation/token but place it under Archives & packages. Avoid duplicate entries/tokens.

CR-1, EX-1, and EX-3 are overlapping `inspect_go_binary` drafts on `/usr/bin/docker`; they are alternatives, not additional closure. EX-6 is a genuinely different Vyper Cancun blob-primitives variant and can be chosen instead if the integration deliberately selects the Vyper Unknown. It is bounded to that source/compiler/fork slice and should not be combined with an ID-domain entry as a second C1 landing (`claims/c1/EX-6.md:1-17`).

The work-ref gate identity also matches the frozen locator: `git show 9c1d1fe:.ufo/gates/c1-census-v10.py | sha256sum` returned `d6b4deaa5973d3a29260b0e325620d87a3cc59464771688f97cb1c62d138fc80`. The current HEAD gate hashes to `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573`; I did not modify either source.

## C2 — freshness

### Ghidra inventory — REPRODUCED

I counted immediate child directories in the installed Ghidra `Features` and `Processors` trees and read its own version property. Exact output:

```text
measured_at_utc=2026-10-19T19:23:12Z
Features: 34 immediate module directories
  BSim, BSimFeatureVisualizer, Base, BytePatterns, ByteViewer, CodeCompare, DataGraph, DebugUtils, Decompiler, DecompilerDependent, FileFormats, FunctionGraph, FunctionGraphDecompilerExtension, FunctionID, GhidraGo, GhidraServer, GnuDemangler, GraphFunctionCalls, GraphServices, MicrosoftCodeAnalyzer, MicrosoftDemangler, MicrosoftDmang, PDB, ProgramDiff, ProgramGraph, PyGhidra, Recognizers, Sarif, SourceCodeLookup, SwiftDemangler, SystemEmulation, VersionTracking, VersionTrackingBSim, WildcardAssembler
Processors: 39 immediate module directories
  6502, 68000, 8048, 8051, 8085, AARCH64, ARM, Atmel, BPF, CP1600, CR16, DATA, Dalvik, HCS08, HCS12, Hexagon, JVM, Loongarch, M16C, M8C, MC6800, MCS96, MIPS, NDS32, PA-RISC, PIC, PowerPC, RISCV, Sparc, SuperH, SuperH4, TI_MSP430, Toy, V850, Xtensa, Z80, eBPF, tricore, x86
application.version=12.1.4
```

Against `PROVINCE.md:46`, deltas are features `34-34=0`, processors `39-39=0`; no correction is warranted. This is an installed-directory inventory, not proof every module loads. EX-11, EX-12, SC-1, and SC-2 agree with this independently measured scope.

### Pacman cache — REPRODUCED; dated snapshot is historical

I independently enumerated `/var/cache/pacman/pkg` and compared exact archive/signature basenames. Output:

```text
measured_at_utc=2026-10-19T19:23:33Z
cache=/var/cache/pacman/pkg
archive_files=1350 signature_sidecars=1350 missing_sidecars=0 orphan_sidecars=0
delta_vs_PROVINCE_live_1350=+0; delta_vs_snapshot_1556=-206
```

The current count reproduces `PROVINCE.md:50`; EX-7, EX-8, and EX-9 report the same disposition. The 1,556 figure is explicitly a 2026-10-13 snapshot in that row; its historical directory state cannot be re-probed today, so keep it dated rather than treating it as live.

### ASAR inventory — REPRODUCED, bounded

I ran the focused census over `/usr/lib`, `/usr/share`, `$HOME/.config`, `$HOME/.local/opt`, and `/opt/1Password`. It returned 12 regular `*.asar` files, matching `PROVINCE.md:49` and EX-10. The separate scope check returned:

```text
count=12
drwx--x--x 1 root root 12 Oct  9 23:03 /opt/containerd
```

Thus the measured 12 is reproduced for the enumerated roots; global host-wide completeness remains unverified because `/opt/containerd` was not readable as an ordinary traversal root. No count change is justified by this bounded result.

## C3 — availability re-probe

I launched the cached REA 6.7.0 MCP stdio server with `TMPDIR=/var/tmp`, initialized MCP protocol `2025-03-26`, then called `tools/call` with `name: "binary_session"`, `arguments: {}`. No target was opened. The selected provider fields and the two matching entries extracted from the raw `tool_availability.groups` array were:

```json
{
  "server": {"name":"rea","version":"6.7.0"},
  "protocol":"2025-03-26",
  "open":false,
  "cleanup_pending":false,
  "artifact_capability": {
    "provider":{"id":"rea-artifact-graph","name":"REA safe artifact graph provider","version":"1"},
    "group":{"operations":["extract_artifact","inspect_artifact"],"effects":["launches_process","may_write_filesystem"],"limitations":[],"available":true,"reason":null,"availability_code":null}
  },
  "tool_availability.groups": [
    {"names":["extract_artifact"],"surface":"artifact-provider","effects":["mutatesSession","writesFilesystem","launchesProcess"],"annotations":["open_world"],"available":false,"reason":"target_required","remediation":"Call open_binary with a supported local target."},
    {"names":["inspect_artifact"],"surface":"artifact-provider","effects":["mutatesSession","writesFilesystem","launchesProcess","idempotent"],"annotations":["idempotent","open_world"],"available":false,"reason":"target_required","remediation":"Call open_binary with a supported local target."}
  ]
}
```

This independently matches PL-1 and RV-6’s direct `binary_session` result. RV-4, RV-5, and PL-2 measure the provider group as `available:true`; RV-1/2/3 doctor runs do not return per-tool capability and correctly leave the active-client status unverified. RV-4 has contradictory launcher-path text at `claims/c3/RV-4.md:7-14`, so I do not use its path statement as command evidence.

**Disposition:** `PROVINCE.md:50` is **REPRODUCED** if `available:true` means provider capability-group availability. It is misleading if read as targetless per-tool callability: this fresh session reports each individual tool `available:false`, `target_required`. The active Kimi-client state is **UNVERIFIABLE**. My cached `rea doctor --json` returned `live_server.state:"unknown"` and Kimi registration `state:"missing"`; the fresh stdio session above is not that attached client. No artifact was opened or extracted.
