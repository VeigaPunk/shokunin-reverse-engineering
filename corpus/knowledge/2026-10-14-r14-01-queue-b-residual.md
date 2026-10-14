<!-- corpus entry — kaidoku-shokunin round 14 goal-mode FINAL lane (residual disposition + consistency sweep, lane r14-01), finished 2026-10-14. Spec/authority: the r12-02 ledger's open set (corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md + its r12-01 sibling-overlap addendum: "L202's 22 adb verbs (device), L201 JEB ×4, L205 ida ×12, L206 hopper ×13, L204's decompiler route (operator), L203's runtime-reconciliation input class") + the rescan's line 176 provisioning-only convention (2026-10-13-r4-16-frontier-rescan.md:176) + line 186's export chain (discharged r11-01, whose scripts-export tree is the line-176 follow-up owner input). Assignment checks performed FIRST, live: `adb devices` → zero devices; `REA_JEB_MCP_URL`/`REA_IDA_MCP_CONFIG` UNSET (7 other REA_ keys ambient, matching r12-01's .bashrc:58-64 finding); :8425 not listening; /opt/hopper/bin/Hopper absent; ilspycmd/dnSpy/mono absent. DRIFT FOUND at L204's gate: /usr/bin/dotnet EXISTS (runtimes-only: Microsoft.NETCore.App 9.0.19 + 10.0.11, `dotnet --list-sdks` EMPTY — so the r4-16 line 204 "no SDK" premise still holds verbatim) AND api.nuget.org reachable (HTTP 200) — which turns the "operator" decompiler gate into a scratch-local recipe (candidate 2). First git check this lane: fleet repo HEAD c6dea73 (only sibling .ufo scratch untracked there); lane repo (nested kaidoku-shokunin) HEAD 82af3a2 at write, its tree carrying this lane's two writes plus sibling r14-02's entry and corpus/README.md edit (not this lane's). All scratch /tmp/r14-01-scratch/; the only repo writes are this entry + the rescan erratum append. Substrates touched read-only and re-pinned after (all byte-identical, pins.before/pins.after): /usr/lib/pinta/Pinta.dll (sha 76472751…b9e8, the all-rounds pin), /tmp/r4-mem-pinta.json, /tmp/app-1127-analysis.json, /tmp/r10-02-scratch/r10-02-reconcile.{in,out}.json + r10-02-aja.out.json, /tmp/r11-01/scripts-export tree. Secrets: none touched; no env values read beyond REA_ key presence. Side-effect disclosed: my adb probes auto-started the adb daemon on :5037 (r12-02's same side-effect class); killed via `adb kill-server`, :5037 verified closed after. -->

# r14-01 — Queue-B residual disposition: L203's last input class EXERCISED, L204 discharged END-TO-END on real ilspy output (operator gate fell to a scratch recipe), line 176 discharged via the line-186 chain — the recorded residue is exactly device/operator-gated (adb 22, JEB 4, ida 12, hopper 13), none forced

Axes: **residual-disposition** (every r12-02 open item live-gate-checked, then exercised where exercisable) /
**gate-drift** (the L204 "operator" wall re-verified against the CURRENT host — premise corrected) /
**verb-contract** (the compare version-ladder's directional coverage law; the reconstruction import's exact-build lock) /
**determinism** (every new artifact re-run byte-identical; two held ids re-derived byte-exact) /
**citation-hygiene** (anchor per claim; verify commands in the run log).

Inputs (all surviving prior-lane state, re-pinned before use): r10-02's reconcile pair —
`/tmp/r10-02-scratch/r10-02-reconcile.out.json` (`ev_7943e598…`, the content-addressed
reconcile_javascript_runtime Evidence r10-02 minted) + its static layer
`r10-02-aja.out.json` (`ev_f867295d…`) + r4-09's obsidian 1.12.7 JS-graph
`/tmp/app-1127-analysis.json` (`ev_a29ab2a0…`); r4's held members evidence
`/tmp/r4-mem-pinta.json` (`ev_f382333b…`); r11-01's export-web-scripts tree
`/tmp/r11-01/scripts-export/` (manifest + 2 origin-hashed JS files).

## Candidate 1: L203's residual sub-class — the runtime-reconciliation input class is ACCEPTED: reconcile × static-layer compares validly (first mixed-class pair), and the pairing exposes a DIRECTIONAL coverage law + a paired-items-stay-unknown law

- claim: `compare-application-versions {"left":<reconcile_javascript_runtime
  Evidence>,"right":<analyze_javascript_application Evidence>}` — the input class
  r12-02 left open ("needs a held reconcile evidence composed as input") — succeeds
  (exit 0, 0.75 s, 325,009 B): **`ev_8f0ac46c…`**, comparison_id
  `javc_b64686f7…`, provider `rea-javascript-application-workflows`. Fed r10-02's
  reconcile evidence (left) against ITS OWN static layer (right), over 86 items:
  summary **`{unchanged:0, added:0, removed:83, changed:0, unknown:3}`**, ladder
  `{exact_node_identity:1, exact_content_digest:2, semantic_key:0, unmatched:83,
  …}`. TWO new laws, both item-level-verified: (a) **directional coverage** — with
  left `partial` (reconcile graph) and right `complete` (static layer), right-side
  unmatched items land **`removed`** (83), unlike r12-02's partial×partial run
  where added/removed zeroed entirely; (b) **paired items never grade
  `unchanged` on this class** — the 3 exactly-paired items (1
  `exact-node-identity` + 2 `exact-content-digest`, confidence `exact`) ALL land
  `unknown`: a runtime-reconcile graph anchors script identity but carries no
  comparable content dimensions, so exact pairing ≠ change verdict. Cross-app
  variant (reconcile × obsidian 1.12.7, 942,080 B): partial×partial →
  `{removed:0}`, `{changed:1, unknown:200}` — the single changed item is
  `semantic-key`/`medium` over dims `content/properties/relationships`
  (**`ev_6ad13357…`**). Coverage propagates honestly (`left_graph_status:
  "partial"`, `status: "partial"`); the envelope's six limitations repeat the
  no-fuzzy-pairing / no-ordinal-identity law verbatim.
- source: `/tmp/r14-01-scratch/cav-rr-static.{in.json,json,run2.json}`,
  `cav-rr-obs.{in.json,json}`.
- verify: compose via `jq -n --slurpfile L /tmp/r10-02-scratch/r10-02-reconcile.out.json
  --slurpfile R /tmp/r10-02-scratch/r10-02-aja.out.json '{left:$L[0],right:$R[0]}'`
  then `npx -y rea-agents@6.4.0 compare-application-versions cav-rr-static.in.json
  --format json`; re-run → **byte-identical, same `ev_8f0ac46c…`** (`cmp` clean).
- verified-at: 2026-10-14 (this lane).
- suggested: admit — **L203 is now wholly discharged**: all three named input
  classes (JavaScript analysis, runtime reconciliation, managed application
  graph) exercised with live successes (r12-02 candidates 1–2 + this).

## Candidate 2: L204 `import-managed-reconstruction` discharged END-TO-END on REAL decompiler output — the "operator" gate had drifted: runtime-only dotnet + reachable nuget run ilspycmd framework-dependently from scratch (no SDK, no substrate writes)

- claim: the r4-16 line 204 gate ("ilspy/dnSpy absent; no SDK — operator or
  hand-crafted JSON") re-verified live splits in two: `dotnet --list-sdks` is
  genuinely EMPTY (no SDK — premise holds), but `/usr/bin/dotnet` carries
  **runtimes** (Microsoft.NETCore.App 9.0.19 + 10.0.11) and api.nuget.org answers
  HTTP 200 — so the ilspycmd **nupkg** (4,632,113 B, v11.1.0.9782) unzipped into
  lane scratch RUNS: `DOTNET_ROLL_FORWARD=LatestMajor dotnet
  pkg/tools/net10.0/any/ilspycmd.dll --version` → exit 0, "ilspycmd: 11.1.0.9782
  / ICSharpCode.Decompiler: 11.1.0.9782". Real decompilation:
  `ilspycmd /usr/lib/pinta/Pinta.dll -o decomp-pinta -p` → **102 .cs files**
  (e.g. `decomp-pinta/Pinta.Actions/AddinManagerAction.cs`, real bodies). Import:
  the input contract (source-pinned,
  `rea-agents/dist/domain/managed/managedReconstruction.js:32-37` — strictObject
  `{static_members: Evidence, decompiler{family enum includes "ilspy",
  executable_sha256, options}, methods[≥1]{token ^0x[0-9a-f]{8}$,
  signature_sha256, normalized_il_sha256, reconstruction{kind, language, text,
  source_path, start_line, end_line}}, notes}`) authenticates each method against
  the static members evidence by token + `signature.raw_sha256` +
  `body.normalized_il_sha256` (`:100-105`, "exact build" lock), refusing anything
  else with "Reconstruction method lock <token> does not match a static managed
  member observation"; the evidence must be `inspect_managed_members` class
  (`:177-178`). Fed `ev_f382333b…` (the held Pinta members evidence) + the REAL
  ilspy text of `AddinManagerAction.Activated` (token `0x0600017e`, il_size 43,
  decompiled file lines 33–38): **exit 0** — **`ev_01a35651…`**,
  reconstruction_id **`mre_11f71a2d…`**, summary `{imported_methods:1,
  decompiled_csharp_methods:1, total_text_bytes:274}`, validation
  **`{matched_static_member:true, exact_build_required:true,
  confidence_floor:"inference"}`**, static_observation bound to
  `/usr/lib/pinta/Pinta.dll` mvid `03407a5a-8ed1-46e6-bdde-c8b13dca4d95`,
  evidence_links `[ev_f382333b…]` — the corpus's FIRST
  import-managed-reconstruction success, on genuine decompiler output, with the
  operator-provisioning step replaced by a ~30-second scratch recipe (every byte
  of tool state inside /tmp/r14-01-scratch/ilspy/).
- source: `/tmp/r14-01-scratch/ilspy/{versions.json,ilspycmd.nupkg,pkg/,
  ilspy-ver.txt,decomp-pinta/}`, `imr-pinta.{in.json,json,run2.json}` (composed
  input 3,850,062 B embedding the full members evidence).
- verify: the two commands verbatim (version banner; decompile); import re-run →
  **byte-identical, same `ev_01a35651…`/`mre_11f71a2d…`** (`cmp` clean).
  Pinta.dll sha after == `76472751…b9e8` (the all-rounds pin).
- verified-at: 2026-10-14 (this lane).
- suggested: admit + **gate-premise erratum** for rescan line 204 (appended):
  "no SDK" remains true but is NO LONGER the gate — a runtime-only dotnet plus a
  nuget fetch de-blocks the decompiler route entirely in scratch; future lanes
  should treat L204 as EXERCISED, not operator-gated.

## Candidate 3: line 176 (`import-reference-source`) discharged via the line-186 export chain — the ownership question resolves by execution: r11-01's scripts-export tree imports cleanly, with the chain's module relationship PARSED

- claim: line 176 stood since r8-02 as "consumed provisioning-only — gates stay
  unprobed for their owner"; the rescan errata chain repeatedly noted "line 176
  untouched (owner convention)", and line 186's export chain (r11-01) is the
  owner-input: `export-web-scripts` publishes retained script bytes under an
  origin-hash `files/origins/<digest>/` layout — exactly a `{root}` dir.
  `import-reference-source /tmp/r11-01/scripts-export` (the r11-01 tree
  survives intact on /tmp; read-only) → exit 0, a bare **HistoricalSourceGraph**
  (no Evidence envelope — same shape r8-02 recorded): root_sha256
  **`94ca09ac…`**, inventory_state `partial`, 7 entries (2 JavaScript sources
  `content_state:"hashed"` + manifest.json as `config` + 4 dirs, languages
  `[JSON, JavaScript]`) — and, the substantive datum r8-02's provisioning run
  never produced: **1 relationship, `main.js → lib.js`, kind `imports`,
  resolution `internal`, parse_state `parsed`** — the export chain's published
  tree carries a resolvable module edge end-to-end. Provenance block and the
  pathname-race limitation recorded verbatim in the graph.
- source: `/tmp/r14-01-scratch/irs-export.{json,run2.json,err}`;
  chain input `/tmp/r11-01/scripts-export/` (manifest `f6434545…` — the same
  manifest digest r11-01 recorded).
- verify: re-run → **byte-identical graph** (`cmp` clean).
- verified-at: 2026-10-14 (this lane).
- suggested: admit — with this, the Queue-A table (rescan lines 165–189) is
  fully drained with no asterisks: every line exercised or defect-closed on its
  own evidence.

## The residual ledger — each remaining item: live blocker anchor, exact unblock action, fleet routing (recorded, not forced — the goal's stop-rule)

- **L202 adb serial verbs (22) — BLOCKED, device-gated.** Live: `adb version` →
  1.0.41 / 37.0.0-android-tools at /usr/bin/adb; `adb devices` → **zero** devices
  (`gates.before.txt`). `REA_ADB_PATH` IS set (`/usr/bin/adb`) — the env half of
  the gate is satisfied; only the device is missing. The zero-device-exercisable
  part was exercised per the assignment hint: `list-adb-devices` re-run →
  **`ev_d4d8cc77c3950870012fa3d41a0e810e1c569db0aad32e22cdef8b9f66e281db`
  BYTE-IDENTICAL to r12-02's held `lad.json`** (887 B) — third independent
  byte-exact production (r4u-06, r12-02, r14-01). Unblock action: plug a device
  with USB debugging enabled, or self-provision an emulator (r11-02's verdict
  stands: heavy — SDK system images). Routing: **recorded, not forced**; the
  22 serial verbs stay refusal-held (`unsupported_target`, r4u-06's typed wall)
  until a device exists.
- **L201 JEB family (4 verbs) — BLOCKED, operator-gated.** Live:
  `REA_JEB_MCP_URL` UNSET; :8425 not listening (`ss -ltn`); per-verb refusal
  re-pinned this lane: `inspect-jeb-client` → exit 1
  `capability_unavailable`/`unsupported_provider`, message verbatim "Start a JEB
  client serving MCP (default http://127.0.0.1:8425/mcp) or set REA_JEB_MCP_URL
  to the running endpoint.", details.reason "fetch failed" (`jeb-client.json`) —
  matches the r2 matrix datum (line 99) exactly. Unblock action: operator starts
  a JEB client serving MCP at :8425 (or exports `REA_JEB_MCP_URL`). Routing:
  **recorded, not forced** — a live JEB install is a licensed, operator-owned
  asset.
- **L205 ida provider (12 MCP ops) — BLOCKED, operator-gated.** Live:
  `REA_IDA_MCP_CONFIG` UNSET; capabilities provider row (this lane's
  `caps.json`, envelope 134,994 B — byte-size identical to r4-16's, zero surface
  drift): ida `unavailable` / **`not_configured`** — "Set REA_IDA_MCP_CONFIG to
  an upstream IDA MCP JSON registration; see docs/ida-provider.md."
  (`configured:false`, `live_connection_probed:false`). Unblock action: operator
  sets `REA_IDA_MCP_CONFIG` to a live IDA MCP registration JSON. Routing:
  **recorded, not forced**.
- **L206 hopper provider (13 unique ops) — BLOCKED, operator-gated.** Live:
  `/opt/hopper` and `/opt/hopper/bin/Hopper` absent (`ls` exit 2); caps provider
  row: hopper `unavailable` / **`executable_missing`** — "Hopper launcher is
  missing or not executable: /opt/hopper/bin/Hopper". Unblock action: operator
  installs Hopper (licensed binary; no self-provision route) at the pinned
  launcher path. Routing: **recorded, not forced**.
- **Post-lane state:** Queue B's open set is EXACTLY {adb 22 serial verbs
  (device), JEB ×4, ida ×12, hopper ×13 (operator)} — all refusal-held with
  typed walls and now-live re-verified anchors. L195–L201, L203, L204 and both
  serial-free adb verbs are held. Line 176 closed. No exercisable-in-part residue
  remains: this lane exercised every part that could be exercised (adb
  zero-device class, L203's reconcile class, L204's full decompiler chain, line
  176's chain-owned import).

## Evidence-id verifications (assignment requirement: at least one re-run — four classes done)

Held ids re-derived BYTE-EXACT: `ev_d4d8cc77…` (r4u-06/r12-02 list-adb-devices,
zero devices) and `ev_7943e598…` (r10-02 reconcile_javascript_runtime, re-run on
r10-02's own input file, `cmp` clean against the held output). Fresh artifacts
re-run byte-identical (content-addressing extends to every verb this lane
touched): `ev_8f0ac46c…` (compare ×2), `ev_01a35651…`/`mre_11f71a2d…`
(import ×2), the HistoricalSourceGraph `94ca09ac…` (import-reference-source ×2).

## Run log

| # | command | rc | result |
|---|---|---|---|
| 1 | gates: `adb version`+`adb devices`, `env \| grep REA_`, `ss -ltn`, `ls /opt/hopper/bin/Hopper`, `command -v ilspycmd/dnSpy/dotnet/mono`, key prints | 0/2 | zero devices; 7 keys set, JEB+IDA UNSET; :8425 closed; hopper absent; dotnet present |
| 2 | `dotnet --list-sdks` / `--list-runtimes`; nuget HEAD; `ls ~/.dotnet/tools` | 0/1 | NO SDKs; runtimes 9.0.19+10.0.11; nuget 200 OK; no tools dir |
| 3 | `list-adb-devices` → `lad.json` | 0 | `ev_d4d8cc77…` BYTE-IDENTICAL to r12-02 held (887 B) |
| 4 | `capabilities` → `caps.json` | 0 | 134,994 B (== r4 size); ghidra available / hopper executable_missing / ida not_configured |
| 5 | `reconcile-javascript-runtime /tmp/r10-02-scratch/r10-02-reconcile.in.json` | 0 | `ev_7943e598…` BYTE-IDENTICAL to r10-02 held output |
| 6 | `compare-application-versions cav-rr-static.in.json` ×2 | 0 | `ev_8f0ac46c…`/`javc_b64686f7…`, 86 items, removed:83/unknown:3; byte-identical re-run |
| 7 | `compare-application-versions cav-rr-obs.in.json` | 0 | `ev_6ad13357…`, {changed:1, unknown:200}, semantic-key/medium |
| 8 | `inspect-jeb-client` | 1 | capability_unavailable/"fetch failed" verbatim (live re-pin) |
| 9 | `import-reference-source /tmp/r11-01/scripts-export` ×2 | 0 | HistoricalSourceGraph 94ca09ac…, 7 entries, main.js→lib.js imports/parsed; byte-identical re-run |
| 10 | ilspycmd nupkg fetch+unzip; `dotnet …/net10.0/any/ilspycmd.dll --version` | 0 | 11.1.0.9782 banner, framework-dependent on runtime-only dotnet |
| 11 | `ilspycmd /usr/lib/pinta/Pinta.dll -o decomp-pinta -p` | 0 | 102 .cs files, real bodies |
| 12 | `import-managed-reconstruction imr-pinta.in.json` ×2 | 0 | `ev_01a35651…`/`mre_11f71a2d…`, matched_static_member:true; byte-identical re-run |
| 13 | `adb kill-server`; `ss -ltn` | 0 | :5037 closed |
| 14 | pins.before/pins.after + `diff` | 0 | all consumed inputs byte-identical; Pinta.dll == 76472751…b9e8 |

Scratch (`/tmp/r14-01-scratch/`): `gates.before.txt`, `dotnet.state.txt`,
`lad.{json,err}`, `caps.{json,err}`, `reconcile-rerun.{json,err}`,
`cav.schema.{json,err}`, `cav-rr-static.{in,json,run2}.json`,
`cav-rr-obs.{in,json}.json`, `jeb-client.{json,err}`,
`irs-export.{json,run2.json,err}`, `imr.schema.{json,err}`,
`imr-pinta.{in,json,run2}.json,err`, `pins.{before,after}.txt`,
`ilspy/` (nupkg, pkg tree, `ilspy-ver.txt`, `decomp-pinta/` 102 files — retained
for re-verification, r10-02 convention).

## Summary

The disposition round turned three "blocked" items into evidence and recorded
the rest honestly. L203's runtime-reconciliation input class — the ledger's last
open sub-item — accepted a real reconcile evidence against its own static layer
(`ev_8f0ac46c…`, 86 items, 83 removed / 3 unknown) and against a foreign app
(`ev_6ad13357…`, 1 semantic-key change / 200 unknown), yielding two new laws:
coverage is DIRECTIONAL (removed asserted only when the opposite side is
complete) and reconcile-side exact pairs never grade unchanged. L204 fell
outright: the operator gate was "no SDK", but a runtime-only dotnet plus a
reachable nuget runs ilspycmd 11.1.0.9782 framework-dependently from scratch —
102 real C# files from Pinta.dll, one method imported under the exact-build
lock (`ev_01a35651…`, `matched_static_member:true`) against the held
`ev_f382333b…` with zero substrate writes. Line 176's decade-long "owner
convention" resolved by execution: r11-01's export tree imports as a
HistoricalSourceGraph (`94ca09ac…`) with the chain's main.js→lib.js import edge
parsed. What remains is exactly what cannot be exercised without new hardware
or licensed software — 22 adb serial verbs (zero devices, live-verified), JEB ×4
(key unset, :8425 closed, refusal re-pinned verbatim), ida ×12 (key unset,
provider not_configured), hopper ×13 (launcher absent) — all recorded with
their exact unblock actions, none forced, per the goal's stop-rule. Four held
evidence ids verified by re-running (two byte-exact held, three fresh artifacts
byte-identical); every consumed substrate byte-identical before/after; the adb
daemon side-effect killed and port-verified closed; lane repo at HEAD 82af3a2
(fleet at c6dea73) with only this entry + the rescan erratum append written by
this lane (sibling r14-02's README edit is theirs).
