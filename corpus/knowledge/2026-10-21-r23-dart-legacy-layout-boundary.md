source: S061 original L1 REA6.5.0 inspect-dart-aot envelope and producing record; .ufo/waves/round-23/evidence/c1/inspect-dart-legacy-saber.envelope.json; public carrier https://f-droid.org/archive/com.adilhanney.saber_1330203.apk
verified-at: 2026-10-21, round23; L1 independently re-fetched and executed the static reader after the connector's scope deviation
recheck: python3 -I -B .ufo/waves/round-23/tools/describe-dart.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <MEASURED-COMMIT>; live replay is the retained .run.json argv after fetching the exact digest-pinned public APK

# Dart AOT parsing is carrier-layout conditional

Coverage-map ground: first successful `inspect-dart-aot`, not generalized Flutter
source recovery. R22's selected Saber1360103 refusal is preserved unchanged;
its identification success never counted as this different operation.

## Selected carrier and actual result

**Observation:** L1 fetched
https://f-droid.org/archive/com.adilhanney.saber_1330203.apk with HTTP200.
Retained fetch receipt `.ufo/waves/round-23/evidence/c1/legacy-saber-download.json`
names absolute local path
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/saber-1330203.apk`,
size41263437 bytes, SHA256
`a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`.
The ignored runtime copy is not the sole reproducer: public URL and full digest
remain committed. HTTPS plus digest identity is not a verified F-Droid signing
chain; no archive-index/APK signature verification is asserted.

Actual producing argv is `npx -y rea-agents@6.5.0 inspect-dart-aot <absolute-apk>
--format json --full-output`, exit0, empty stderr, retained in
`.ufo/waves/round-23/evidence/c1/inspect-dart-legacy-saber.run.json`.
Untouched original envelope:
`.ufo/waves/round-23/evidence/c1/inspect-dart-legacy-saber.envelope.json`,
`ev_d2ff19d7100f34b52e4b2bc52ee115e48428624f7da57814e5f184b4bd4c7491`,
operation `inspect_dart_aot`. These are L1-produced records, not the connector's
three earlier speculative/probe outputs under `connect-dart-symbols/`.

**Observation:** selected ABI is x86_64; libapp SHA256 is
`f82ab4111807552af82ada747c5cccfe49474ecfcce49d5e0c3c701feeab38a8`.
`libapp.coverage:complete` is scoped to the reader's section/header contract:

| Dynamic symbol | File offset | Size | Data header |
|---|---:|---:|---|
| _kDartVmSnapshotInstructions | 7208960 | 89936 | Not a data header; magic_valid:false, kind/length null |
| _kDartIsolateSnapshotInstructions | 7298944 | 10038688 | Not a data header; magic_valid:false, kind/length null |
| _kDartVmSnapshotData | 832 | 18384 | magic_valid:true, kind3, declared length16842 |
| _kDartIsolateSnapshotData | 19264 | 7153168 | magic_valid:true, kind3, declared length6058354 |

Snapshot hash `78da37fed6bf1489361a312568249f3f` has two reported header sources.
The table, source count, hash and lower-bound values are recomputed from the
committed envelope by the `recheck:` command, not supplied as naked counts.

## What complete does not mean

`string_pool.coverage:partial`; package URI and token projections are capped
lower bounds. The producer explicitly says these are byte-pattern observations,
not deserialized cluster semantics; typed class/function recovery requires an
SDK-specific parser. Instruction-symbol `magic_valid:false` is not silently
reclassified as a data-header failure. No SDK version is inferred from a bare
snapshot hash, no source code is reconstructed, and no APK/library is executed.

**Inference:** this selected carrier exposes the four names the reader supports,
whereas the retained R22 carrier did not. That is enough for a conditional
held-verb observation, not proof that every older build works, that newer builds
never work, or that the exact causal SDK-change boundary is established here.
No re-run of R22's already observed refusal was needed or credited.

The successful layout result and the existing refusal are distinct artifact
outcomes, not contradictory provider verdicts. Count `inspect-dart-aot` once;
extra builds or a separate identify success do not add another T1 verb.
Both debugger verbs remain unheld/Adjacent, with no live attach or execution.

## Round-23 W2 qualification — exact coverage and selection limits

S063 supersedes S061's sufficient-condition wording. Exporting the four names
alone does not guarantee complete libapp observations: this selected carrier
also has the supported kind-3 data headers, a valid shared hash and declared
lengths fitting their symbols. `normalized_result.coverage` is **partial**;
`libapp.coverage` is complete and `string_pool.coverage` is partial. These are
three distinct coverage fields, not one global complete result.

“Legacy-layout” in this filename/title is descriptive terminology borrowed
from the connector's proposal, not an admitted SDK-generation or version
mapping. The admitted fact is this selected x86_64 libapp's **four-symbol
layout**. The R22 refusal does not echo its selected ABI, so this comparison
does not rule out ABI-selection differences or prove the causal SDK boundary.
The producer's own kind-3 “Dart2.14” limitation text is retained but not adopted
as a version-identification rule.

The L1 urllib fetch was observed in the coordinator tool transcript. Its
committed HTTP200/digest record is author-produced, not an authenticated
network transcript or proof distinguishing download from a same-byte copy.
“Independently fetched” describes that observed L1 action, not independently
verified publication/signature/custody. The full digest and public reproducer,
not the independence adjective, identify the admitted artifact.

Recheck precision (QUALITY21): describe-dart.py **extracts and reports** the
producer's section table, snapshot hash and lower-bound fields; it does not
recompute those from APK/libapp bytes. Its independent recomputations are
the committed envelope's byte digest and envelope/run equality; other
comparisons bind retained path/digest/command strings. The earlier sentence
calling all producer fields “recomputed” is superseded on that point.
Re-running the parser itself requires the exact public APK and retained argv.

“First successful” in the opening paragraph means **first admitted holding**
in this frozen lane inventory, not the earliest successful call on the host:
the unadmitted connector and synthetic schema probes ran earlier. No
non-author independence is implied by the L1 action.

The table's “not a data header” explanation is layout interpretation;
observed fields are the symbol names, offsets/sizes, magic flags and null or
numeric kind/length values. Offsets are within the selected libapp, not APK
container offsets or virtual addresses. Printable-run capacity and projection
limits remain producer-reported; a referenced but absent capped flag is not
invented, and projected strings are not validated source paths or class names.

**Current source authority:** S063 replaces S061's coverage wording. The
original source header remains historical provenance; this entry's admitted
current interpretation is the exact selected-carrier qualification in S063
and the named W2 corrections, not a universal rule inferred from S061.
