source: S003 in `corpus/SOURCES.md` — `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`, member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:102-240` and member `ghidra/app/util/bin/format/golang/GoVer.java`; S023 installed `go1.25.0.json`, `all.Types.runtime.moduledata.Fields[1]`; exact installed artifacts selected by `.ufo/waves/round-16/selection.py` carry separate size/SHA-256 identities.
verified-at: 2026-10-20 — reopened shipped source and installed base JSON; L1 source-model execution receipts and measured source revision are recorded in the execution addendum, not inferred from file presence.
recheck: `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --request 1.24.7 --goos linux --goarch amd64`; compare the retained per-file identities and result fields in `.ufo/waves/round-16/verification.json`; reopen source anchors before interpreting drift. This command runs a Python source model, not Ghidra.

# Go snapshot selection preview — compute the choice, preserve the evidence boundary

## What is new, and what is not

**OBSERVATION:** round 15 already held the selector law, file inventory and an inferred 1.24.7→1.24.6 fallback. Repeating those is not a new discovery. This entry materializes an explicit request-bounded selection and ordered platform projection with exact selected-file identities. The strongest contrast is a request for 1.24.5: installed patch 6 must not win over the exact requested patch 5. The law remains source-derived; the computation is a local Python observation.

**UNKNOWN:** the old `op` analyzer's precise failure cause, the identity of its executing classes/data, and whether a snapshot-only change would repair recovery. No new real carrier is selected by this round. Historical paths in saved reports do not select a target on the caller's behalf.

## Source-derived decision table

S003 anchors are the shipped archive member, not a live compiled-class trace.

| Condition / field | Source law and preview meaning | Forbidden shortcut |
|---|---|---|
| Same-minor base missing | `getApiSnapshotJsonFile:122-126` returns before diff search; preview `missing_base`, null base/diff/selected patch, empty base buckets | A nearby minor's base or present diff rescues the lookup |
| Patch request 0 | `getPatchVerDiffFile:153` never enters the diff loop; preview `base_only`, selected patch 0 | A planted `.0.json.diff` is selected |
| Exact diff exists | First present candidate at requested patch; preview `exact_diff` denotes filename selection only | The preview has applied or validated that diff |
| Exact diff absent, lower diff exists | `:148-166` searches downward within the same major/minor; preview `fallback_diff` with the greatest present positive patch not above the request | Lexicographic order, highest installed patch irrespective of request, or all intermediate diffs chained |
| No diff at or below request | Base only, selected patch 0; for a nonzero request the Java source warns of fallback | A fallback warning establishes a diff was applied |
| `requested` | The model's explicit normalized input echo. With a non-null provider, Java passes original GoVer to `read:111` and stores it at `:239`; with missing base, `get:115` returns `EMPTY` carrying INVALID at `:242` | The input echo is a Java object label on every status, or version-shaped metadata authenticates exact patched bytes |
| `arch_search_order` | Effective `read` order: OS-arch, OS, `unix` for the exact source set, arch, `all`; non-Unix empty placeholder removed | A platform is unsupported merely because its specific bucket is absent |
| `base_matching_buckets` | Matching non-null top-level names in priority order, deduplicated; `base_matching_buckets_source` labels the unpatched base | Patched record content or successful type lookup follows from bucket presence |

The Java list at `:108-109` contains `""` for a non-Unix OS; `read:230-232` skips it. The preview emits the effective order without that empty element. The source Unix set at `:180-181` includes android and ios, not windows or plan9. Generic `all` remains part of the lookup scope; S023's opened pointer field demonstrates why a single missing platform bucket is not an empty-snapshot finding.

The separate `getApiFile:183-192` utility permits a minor-only filename for patch 0. The `get` path above does not call it; the preview must not inherit that fallback.

## Tool and evidence contract

`selection.py` exports `select_snapshot(root, request, goos, goarch)` and a CLI. Stdlib only, read-only installed resources, stdout JSON. Exit 0 means a result was emitted (including `missing_base`); exit 2 means invalid input or a required read/parse could not be evaluated. It is a probe, not a conformance gate. `selfcheck.py` is a developer fixture runner, not a promotion or domain-acceptance instrument.

The CLI intentionally accepts a strict canonical stable `M.m.p`, with numeric components bounded by Java signed-int range. This is narrower than `GoVer.parse`, which accepts missing patches and suffix forms. Rejecting those inputs does not establish Java rejection. Version validation belongs to the preview interface, not the source-law claim.

Per-file `path`, `size`, and `sha256` describe the raw selected base and diff. Paths are root-relative. A missing base short-circuits before any diff selection. A selected diff is hashed but not parsed or applied: even malformed diff bytes can be selected by this preview. The base is parsed for top-level key membership, omitting null values because Java `read:233-235` skips null arches. This is not a full Gson/GoArch validator: non-object non-null bucket values can still appear in the preview even where Java parsing would fail. The retained non-object fixture documents that deliberate limitation, not Java parity. Funcs/Types schemas and record usability are not validated. A green fixture result therefore cannot stand in for `JsonPatchApplier`, the Java reader, struct registration, Ghidra recovery, or target execution.

`patch_applied:false` and `evidence_class:"source_model"` must survive every emitted result. `base_only` covers both an exact patch-0 request and a higher requested patch falling back to base; the independent requested and selected-patch fields distinguish these. An `exact_diff` status means exact requested **filename**, never an exact computed snapshot-content digest.

## Limits and interpretation

- One explicitly supplied root is modeled, not Ghidra application/module-data resolution or overrides outside it. S003 and S023 share an installation origin and are not independent empirical witnesses.
- The companion source archive is not authenticated against the classes actually loaded by Ghidra; source/bytecode consistency would not identify runtime class overrides. This preview also does not resolve Ghidra's derived-data cache.
- Requested version, GOOS and GOARCH are explicit caller inputs here, not values recovered from a target. Java derives them through build-info/loader fallback paths that this instrument does not execute. A source-model linux/amd64 result makes no claim about any target's actual platform settings.
- Stdout paths are root-relative; retain the exact producing argv alongside JSON to identify the installation. An exit-2 base-JSON parse result describes this Python model, not every acceptance behavior of Java/Gson.
- Identity hashing and base parsing are separate reads and assume quiescent installed data; this is not an atomic filesystem snapshot. Freeze a mutable input tree separately before attributing parsed content to a digest.
- All bucket results are unpatched. When a diff is selected, the effective post-patch content remains unknown to this instrument. Source reading that Java would apply a diff is not evidence that this Python process did so.
- A parsed top-level object with no matching keys differs from absent base, unreadable JSON and malformed request. None alone is an old-target diagnosis or a statement about all installed/runtime versions.
- Fixture expectation values are hand-authored from source boundaries, independent of model recomputation; hashes and sizes are observed separately, not invented as expected ground truth.
- C1 deepens already-held Go ground. It does not add broad domain coverage, a held REA operation, a target capability or independent outside verification. Current-round admission remains non-author closure work.

Motivating evidence and candidate rejects: `corpus/lessons/round-16.md`, Gate; prior outside boundaries: `corpus/lessons/round-15-verifier-spotcheck.md`; author-side novelty/causality attacks: `.ufo/waves/round-16/w1/AttackNovelty.md` and `AttackCausality.md`.
