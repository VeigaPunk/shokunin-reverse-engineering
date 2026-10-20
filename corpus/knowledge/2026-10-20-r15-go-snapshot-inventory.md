source: S003, S007, S023 in `corpus/SOURCES.md`; installed Ghidra `Base-src.zip` source-selection methods, installed ChangeHistory, and `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json`; round-15 read-only inventory command/output in `.ufo/waves/round-15/`.
verified-at: 2026-10-20 — installed JSON/source reading; inventory execution is separately recorded in the committed measurements addendum, not target or provider execution.
recheck: `python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`; compare retained `.ufo/waves/round-15/inventory.json` filename/size/SHA-256 and parsed summaries, and reopen S003 anchors below. A changed inventory is drift to investigate, not an automatic failed support verdict.

# Go snapshot identity: requested patch labels are not selected data bytes

## What this adds

The round-14 entry already held the source-level base lookup and patch fallback law. A repeated file list earns no new coverage. This entry deepens the held Go diagnostic by retaining installed data byte identities, per-minor patch coverage, generic bootstrap definitions, and the requested-version-versus-data-identity distinction. The real historical `op` run's cause remains UNKNOWN.

## Observations from opened source and JSON

**OBSERVATION — independent byte identities, shared installation origin.** S003's archive SHA-256 is `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`. S007's installed history is `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`. S023's actual `go1.25.0.json` is `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`. Counting/pinning command: `sha256sum` on the three absolute registry paths, executed 2026-10-20. These files come from the same installation, not independent empirical witnesses. The source companion archive is not authenticated against executing compiled classes.

**OBSERVATION — actual generic definitions.** S023 JSON `all.Types` contains both `runtime.moduledata` and `runtime.pcHeader`. The former has `Kind: struct` and a field `pcHeader` with `DataType: *runtime.pcHeader` (`all.Types.runtime.moduledata.Fields[1]`). Direct queries of the JSON, not an architecture-only excerpt, establish these names. Their presence proves schema content, not successful registration or recovery for a binary.

**OBSERVATION — mandatory same-minor base.** S003 `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:122-126` requests `goVer.withPatch(0)` and returns null if that base cannot be located. `get` returns EMPTY at `:115`. Patch-diff lookup is later, so it cannot rescue a missing major/minor base and does not fall back to the preceding minor.

**OBSERVATION — one selected patch diff.** At `:148-166` the selector searches backwards in patch numbers, retaining the first present diff; `:128-145` either returns the base provider or applies that one diff to the base. The inventory reads diff structure but does not apply it, validate semantic patch correctness, or compare a patched result with ground truth. No chain of all intermediate diffs is executed on this source path.

**INFERENCE FROM SOURCE — a version label is not exact patch identity.** `get` calls `read(is, archSearchOrder, goVer)` at `:111` with the original requested version even when the byte provider came from an earlier patch diff or the base alone. `read` constructs the result with that version at `:239`. The mapper's info message (`GoRttiMapper.java:178-181`) can therefore name the requested patch while actual input bytes correspond to a lower fallback. Retain the fallback warning (`GoApiSnapshot.java:158-165`) and the selected filename/digest; do not treat a version-shaped log as a content hash.

**OBSERVATION — applicability includes generic records.** `GoApiSnapshot.java:108-109` constructs the search order OS-architecture, OS, `unix` where applicable, architecture, `all`. `:205-239` preserves matching buckets in order; `isInvalid()` at `:503-505` tests an empty bucket map. A missing platform-specific key alone is insufficient to infer an invalid snapshot when `all` survives. The present-file/zero-matching-key branch in round 14 is a hypothetical source case; the retained inventory checks actual unpatched bases for their generic bucket. Patch diffs are not applied here, so no all-patched-results conclusion follows.

## Diagnostic decision table

| Available evidence | Supported decision | Forbidden shortcut |
|---|---|---|
| Base for requested major/minor absent in the pinned inventory | The inspected source path yields EMPTY before considering diffs | This was the precise cause of the old `op` result, or all Ghidra runtimes fail identically |
| Base present, exact requested patch diff present | Source selects that one diff against the base | The inventory has applied or validated it |
| Base present, exact diff absent, earlier diff present | Source uses the closest lower patch's diff; retain its filename and fallback warning | Requested-version label proves requested-patch data |
| Base present, no diff in that minor | Source supplies base bytes; requested-version object label can still name a later patch | Missing patch diff has the same invalid-snapshot outcome as missing base |
| Platform key absent but generic `all` present | Generic definitions remain in the search scope | Platform-key absence proves no type definitions |
| Missing bootstrap definition during registration | Trace virtual `getType` to snapshot lookup and required mapping | Snapshot validity only chooses error text |
| Proposed snapshot-only replacement | Inspect all required struct fields and upstream changes before a separate run | A file addition, range edit, or source patch proves a repaired provider capability |

## Relation to the outside correction

S003's `DataTypeMapper.java:176,310-313` dispatches to `GoRttiMapper.getType` (`:379-396`), then `GoTypeManager.findDataType/findTypeRec` (`:355-358,402-455`), including `apiSnapshot.getTypeDef` at `:449`. This corrects the old advisory's omission of virtual dispatch. It does not identify the historical target cause or prove snapshot-only sufficiency. Named correction: round-14 lesson `Round-15 correction — virtual-dispatch advisory`; external finding: `round-14-verifier-spotcheck.md`, routed defect 1.

## Limits and recheck discipline

- No new real carrier was selected, executed, decompiled, or analyzed this round. Historical nearby paths do not automatically select a target. The previous planned carrier task is deferred, not claimed impossible or completed.
- The read-only probe inventories installed files and parses JSON/diff headers; it does not run Ghidra, Java classes, a target, or a patch engine. It is not a conformance gate and has no selftest capability claim.
- Data-source facts cite retained inventory bytes, not only S003: an archive digest does not pin the data directory. S023 is scoped to the selected JSON; other files carry their own digests in the inventory.
- Generic-bucket presence is not type completeness, semantic validity, or a guarantee that required struct mapping succeeds. Source catch branches returning null do not make their lookup prerequisites snapshot-independent.
- S007's 12.0 Improvements entry records the switch to JSON bootstrap files. It does not establish later-version support in this installation.
- Selected inventory fields, exact commands, exit codes, and the source revision measured are appended after L1 execution; a provisional file-existence count alone is not the semantic evidence for C1.

## Executed inventory — 2026-10-20

The `recheck:` command above ran twice using the repaired probe at
`7ad23fe1735cd868ec203d93deb13bb2c42889ad`; both executions exited 0 and
emitted byte-identical stdout. Retained output:
`.ufo/waves/round-15/inventory.json`, SHA-256
`ad06fadc0166e172d65325e3366375e2d4a9730d714d154bbcd98137539bb2fe`.
Full argv, stdout/stderr and exits: `.ufo/waves/round-15/verification.json`.
The initial sorting failure and its only code repair are retained separately
in `verification-initial.json` and source history; no first-run success claimed.

| Measured observable | Result from the same inventory command |
|---|---|
| Base JSON / patch-diff files | 11 / 123; every base has `all`; errors and skipped matching entries empty |
| Patch histogram by minor | 1.15:15, 1.16:15, 1.17:13, 1.18:10, 1.19:13, 1.20:14, 1.21:13, 1.22:12, 1.23:12, 1.24:6; none for 1.25/1.26 |
| Requested 1.24.7 | Base SHA-256 `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571`; 6 installed diffs, through 1.24.6; exact requested diff absent |
| Requested 1.25.7 | Base is S023, 27 buckets, no installed minor diff; generic `all` has 29,041 function and 3,741 type records |
| Selected bootstrap definitions in 1.25 base | `runtime.moduledata` and `runtime.pcHeader` only under `all`, 45 and 13 fields respectively |
| Requested 1.26.8 | Same-minor base absent, no installed minor diffs; null base digest/structure, not invented zero-record parsing |

The per-file digests, sizes and complete key summaries are retained in the
output, not replaced by these selected counts. Counts describe parsed
installed resources, not recovered target functions. A structural regression
check over this emitted JSON confirmed numeric `patch` and object
`patch_structure` on every diff. No patch was applied.
