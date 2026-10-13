<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/13-keyed-archive.md. -->

# kaidoku-r3 lane 13 — Carrierless-op exercise: keyed archive, IB decode, dyld trace, plist

Axes: carrier-synthesis (smallest honest artifact that exercises the op) /
truth-vs-capabilities (`available:true` proven end-to-end, not just declared) /
refusal-taxonomy (clean typed errors on wrong/absent carriers). All carriers
synthesized in `/tmp`, all scratch removed afterwards.

## Candidate: `inspect_keyed_archive` — WORKS, full object graph on Linux

- claim: `available:true` is real. On a hand-built NSKeyedArchiver binary
  plist (`$archiver:"NSKeyedArchiver"`, `$top.root→UID(1)`, `$objects` =
  `$null`, `NSMutableDictionary` archived-object, class-descriptor
  `NSMutableDictionary→NSDictionary→NSObject`, 4 scalars) the op decoded the
  complete object table: `roots:{root:{UID:1}}`, 7 objects typed
  `nil`/`archived-object`/`class-descriptor`/`scalar` with `status`
  (`unknown-class` on the archived dict vs `observed` on scalars), and a
  resolved `references` edge list (`root→1`, `1.$class→2`, `1.NS.keys[i]→5,6`,
  `1.NS.objects[i]→3,4`). Evidence id
  `ev_0524ef94b034…`, provider `rea-artifact-graph` v1.
- source: `npx -y rea-agents@6.4.0 inspect-keyed-archive <path>`;
  `--schema` shows args `{path, archive}` — `archive` is a POSITIONAL arg
  (`rea inspect-keyed-archive <path> [archive]`); passing `--archive` as a
  flag fails `{"code":"UNKNOWN","message":"Unknown flag: --archive"}` —
  schema-to-CLI mapping wart worth recording.
- verify: carrier built with `python3 plistlib` (`FMT_BINARY`, `plistlib.UID`
  for keyed refs), 365 bytes, `file` → "Apple binary property list".
  Bundle leg: `inspect-keyed-archive /tmp/Fake.app
  Contents/Resources/MainMenu.nib` → `archive_path` echoed, `binary-plist`,
  same 7 objects / 6 refs — bundle-relative archive addressing works.
- verified-at: 2026-10-13T12:45-03:00
- suggested: admit as first confirmed-working macOS-format op on this host.
  Refusals are typed and honest: plain plist → `unsupported_target` ("no
  `$archiver` key", remediation names `inspect_plist`, "requires a macOS
  host"); text file → `artifact_operation_failed`/`execution_failure`
  ("missing root element" via xmldom); bundle path w/o archive arg →
  `invalid_request`/`invalid_input`, `retryable:true` ("Select a keyed
  archive path relative to the active app bundle").

## Candidate: `decode_interface_builder` — WORKS on synthesized .app bundle

- claim: `available:true` is real but the carrier bar is higher: input must
  be a `.app` bundle whose `Info.plist` parses and carries
  `CFBundleExecutable` — first attempt without it failed `target_unavailable`
  /`unavailable` ("Info.plist is malformed, unsupported, or lacks
  CFBundleExecutable"), `retryable:false`. After adding
  `CFBundleExecutable:Fake` + a Mach-O at `Contents/MacOS/Fake`, the op
  decoded BOTH planted documents: `Contents/Resources/MainMenu.nib`
  (`document_kind:"nib"`) and
  `Contents/Resources/Base.lproj/Main.storyboardc/BYZ-38-t0r-view-8bC-Xf-vdC.nib`
  (`document_kind:"storyboard_scene"`), each `object_count:1,
  hierarchy_complete:true`, with an `ib:`-namespaced graph, per-document
  `interface_builder_resource` evidence nodes and sha256 pinning to the
  archive bytes. Evidence id `ev_4fd605617ee5…`.
- source: `npx -y rea-agents@6.4.0 decode-interface-builder /tmp/Fake.app`;
  `--schema`: `{path:.app bundle}`, options `maxDocuments≤64`,
  `maxObjects≤20000`, `maxConnections≤40000`.
- verify: bundle = Info.plist (binary plist) + Mach-O + loose `.nib` +
  `.storyboardc/` dir containing a scene-named nib plus its own Info.plist
  (`UIViewControllerIdentifiersToNibNames`). Same keyed-archive bytes served
  as every nib (sha256 `bb6a3618…` matches across both documents).
- verified-at: 2026-10-13T12:46-03:00
- suggested: admit — second confirmed-working op. The bundle-shape gate
  (executable lookup via CFBundleExecutable, then archive discovery) is
  itself verified behavior, not assumed.

## Candidate: `trace_dylib_resolution` — WORKS; honest `undetermined` semantics

- claim: `available:true` is real. Input is a Mach-O path OR an `.app`
  (schema enum arch `arm64|arm64e|x86_64`, `root` repeatable). On a
  hand-built 872-byte arm64 `MH_EXECUTE` (header + `LC_SEGMENT_64` + 2×
  `LC_LOAD_DYLIB` + `LC_LOAD_WEAK_DYLIB` + 2× `LC_RPATH`) it parsed the slice
  (`cpu_type:16777228`, `file_type:"execute"`), extracted both rpaths, and
  emitted per-edge dyld candidates: `@rpath/libkaidoku.dylib` →
  `Contents/Frameworks/libkaidoku.dylib` (source `rpath`, rpath_owner =
  loader) and `/opt/kaidoku/lib/…` → `outside-target`;
  `@executable_path/../Frameworks/libdep.dylib` → resolved_path under
  `Contents/Frameworks`. Coverage `complete`. On the bare file at `/tmp`,
  `@executable_path` candidates correctly report `escapes-target`.
- source: `npx -y rea-agents@6.4.0 trace-dylib-resolution <target>`;
  evidence `ev_33de3850…` (bare Mach-O) and a second run on `/tmp/Fake.app`.
- verify: TWO parse-rejection rounds fixed the carrier: (1) `LC_RPATH`
  cmdsize 44 → "load command 4 at offset 248 has invalid cmdsize 44" —
  parser requires 8-aligned cmdsize (12-byte rpath header needs name padded
  to len%8==4); (2) after planting real dylib files under `Frameworks/` and
  giving each an `LC_ID_DYLIB` install name, images all `parse_status:
  "parsed"` yet edge `resolution.status` stays `undetermined` and
  `install_name_matches:null` — the tool records the filesystem match
  (`resolved_path` set) but conservatively refuses a final binding, matching
  its own limitation text ("Leaf and relative install names depend on dyld
  fallback … undetermined"). The `LC_LOAD_WEAK_DYLIB /usr/lib/…` edge is
  silently absent from `edges` — consistent with the documented "absolute
  install names … are not evaluated" limitation.
- verified-at: 2026-10-13T12:46-03:00
- suggested: admit — third confirmed op. Note for future carriers: cmdsize
  alignment is enforced per load command; `undetermined` is a terminal
  honest status, not a failure.

## Candidate: `inspect_plist` — refuses exactly as catalogued

- claim: Still `capability_unavailable` /`unsupported_provider` even with a
  valid binary plist carrier: "Native macOS utilities require macOS."
  (`provider_id: composite:native-macos+rea-artifact-graph+rea-dotnet-static`).
  It does NOT parse anyway — the macOS gate precedes carrier inspection.
  Contrast is now proven in both directions: `inspect_keyed_archive`
  (pure-JS) decodes archives `inspect_plist` can't even see, and its
  `unsupported_target` remediation on a plain plist correctly redirects to
  `inspect_plist` — a routing breadcrumb that is dead on this host.
- source: `npx -y rea-agents@6.4.0 inspect-plist /tmp/kaidoku.plist` on a
  106-byte plistlib `FMT_BINARY` dict.
- verified-at: 2026-10-13T12:44-03:00
- suggested: none — boundary confirmed; ordinary-plist reading on Linux is
  the one still-uncovered gap (trivially served by `plutil`/`plistlib`
  locally, just not by REA).

## Run log

- `uname -a` → Linux x86_64 (Arch); python3 3.14.7, node 24.21.0.
- `--schema` captured for all four ops; `inspect-keyed-archive --help`
  disambiguated positional `archive` arg vs schema naming.
- Built carriers in `/tmp`: `kaidoku.plist` (binary plist), `kaidoku-keyed.plist`
  (hand-rolled NSKeyedArchiver via `plistlib.UID`), `kaidoku-macho` +
  `Fake.app` (arm64 Mach-O generator; fixed rpath cmdsize padding, added
  `CFBundleExecutable`, planted two `LC_ID_DYLIB`-carrying dylibs).
- Ran: inspect-keyed-archive (file ✓, bundle+archive ✓, plain plist →
  `unsupported_target`, text file → `artifact_operation_failed`, bundle w/o
  archive → `invalid_request`); decode-interface-builder (✗ missing
  CFBundleExecutable → ✓ two documents); trace-dylib-resolution (✗ cmdsize 44
  → ✓ edges+candidates on bare and bundle targets); inspect-plist →
  `capability_unavailable`.
- Removed all `/tmp/kaidoku*`, `/tmp/Fake.app`, build scripts. No repo files
  touched besides this report.

## Summary

| op | r2 status (`available`) | r3 result | evidence |
|---|---|---|---|
| `inspect_keyed_archive` | true, untested | **WORKS** — 7-object graph, resolved refs; bundle-positional archive arg ✓ | `ev_0524ef94b034…` |
| `decode_interface_builder` | true, untested | **WORKS** — nib + storyboard_scene decoded, `hierarchy_complete` | `ev_4fd605617ee5…` |
| `trace_dylib_resolution` | true, untested | **WORKS** — rpath stack resolved to real files; `undetermined`/`outside-target`/`escapes-target` taxonomy honest | `ev_33de3850…` + bundle run |
| `inspect_plist` | false (`unsupported_host`) | refuses cleanly — `capability_unavailable`, "Native macOS utilities require macOS" | error envelope |

Gap verdict: the three `available:true` ops are genuinely usable on
Linux/x86_64 — the r2 "carrierless" gap was host-corpus, not
implementation. Synthesized carriers close it for all three. Two honest
quirks logged: schema `archive` arg maps to a positional (not `--archive`),
and `trace_dylib_resolution` enforces 8-aligned load-command cmdsize.

## Errata (round 4)

- **Weak dylib edges (r4 audit-B, verified 2026-10-13):** weak dylib imports are emitted
  as `undetermined` edges, not silently omitted — the entry's "omitted" phrasing was
  wrong. Resolution verdicts carry a distinct `undetermined` status.
- **Synthesis recipe drift (r4 audit-B):** re-running the NSKeyedArchiver recipe yields a
  **363 B** plist, not 365 B — content-bound evidence ids differ across rebuilds
  (`ev_464caf10…` vs r3's `ev_0524ef94…`). Recipes are reproducible in shape, not byte
  identity; claim byte-exactness only for pinned fixture bytes, never for re-synthesized
  carriers.
