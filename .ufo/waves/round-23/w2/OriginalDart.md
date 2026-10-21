# OriginalDart: R23-C1 source review of the legacy Saber `inspect-dart-aot` envelope/run pair

Seat: `KaidokuR23.OriginalDart` (reviewer, leaf). Author-side finding, not independent outside admission. L1 owns counting and integration.
Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Every verdict below is read from candidate bytes with `git show 2838351450ff1ee4baa620c962a1153450d53311:<path>`, copied into ignored scratch `runtime/OriginalDart/`. Baseline B was not used as evidence.
Not run: REA producer, `describe-dart.py`, `verify.py`, `preflight_dart_carrier.py`, `count-c1.py`; no APK or library execution; no tests, builds, or linters.
Labels: **Observed** = present in candidate bytes or exact command output. **Inferred** = my reasoning from observed bytes. **Unknown** = not determinable from committed bytes. One worktree read, labelled [WT], is used only as a consistency check.

## Summary

- **L1 target path/hash:** holds. Path, SHA-256 `a7b1f5c8…ea618`, and size 41263437 agree across every committed record and were acquired twice (L1 receipt, connector fetch), matching the F-Droid index entry. The index signature was not verified.
- **Four symbol records:** names are exact. Offsets, sizes, and data-header fields match the connector's committed `carriers.json`. The "File offset" label and the instruction-row semantics are not retained by the envelope.
- **libapp complete vs string_pool partial:** both labels are retained. The `complete` predicate is not in the committed record, but the retained numbers satisfy the predicate as W1 describes it (hand-checked, F7). The "capped flag" cited in the limitations does not exist, and `printable_run_count` has no bound marker (F4).
- **False as worded:** K23.md:44-46 says the table, source count, hash, and lower-bound values are "recomputed from the committed envelope by the `recheck:` command, not supplied as naked counts." `describe-dart.py` copies them verbatim (F1).
- **Unbound or undisclosed:** the recheck command still has the `<MEASURED-COMMIT>` placeholder (K23.md:3); the top-level `normalized_result.coverage: "partial"` is never mentioned (F3); the L1 run record carries no producer or resolved-tool identity (F5).

### Claim ledger

| Claimed field or statement | Location | Retained in pair? | Independently bound? |
|---|---|---|---|
| Target path (runtime absolute path) | K23.md:24; S061 | Yes: `subject.local_path`, `parameters.path`, `locations[0].path`, `normalized_result.target.path`, run `argv[4]` | Path only; file hash matches [WT] |
| Target SHA-256 `a7b1…ea618` | K23.md:18-19 (digest); caveats K23.md:20-22 | Yes: `subject.digest`, `normalized_result.target.sha256`, receipt `sha256` | Yes: connector separate fetch, F-Droid index entry (signature unverified), connector run target |
| Target size 41263437 | K23.md:18 | Yes: `target.bytes`, receipt `size` | Yes: index entry, connector observed bytes |
| HTTP 200 | K23.md:14 | Receipt `status: 200` | Single receipt; connector `fetch.json` records no status |
| Exact argv, exit 0, empty stderr | K23.md:24-26 | Yes: run `argv`, `exit`, `stderr` | Same record only |
| Envelope is untouched producer stdout | K23.md:27-29 | Yes: envelope bytes = `run.stdout` bytes (both `7768198e…`) | Yes: `describe-dart.py` `stdout_byte_equal` at 6615aeae |
| `ev_d2ff19d7…` | K23.md:29 | Yes | Path-sensitive; connector run at another path gives `ev_dcdab9d0…` |
| "L1-produced records" | K23.md:30 | **No.** Run record has no producer field | Only `legacy-saber-download.json` `producer` and the knowledge text |
| "REA 6.5.0" | K23 front matter; S061 | argv token only; `provider.version: null` | Connector run records `resolved_tool.version 6.5.0`; L1 does not |
| Selected ABI x86_64 | K23.md:33 | `abi` yes; enumeration and rule no | Connector identify `abis` (one entry); index `nativecode` |
| libapp SHA-256 `f82ab411…` and bytes | K23.md:33-34 | Yes | Connector identify and inspect (same producer); `carriers.json` |
| libapp `coverage: complete` | K23.md:35-36 | Label yes; predicate no | Hand-checked against W1-described predicate (F7) |
| Four symbol names, offsets, sizes | K23.md:37-42 | Yes | `carriers.json` `kdart_dynsym` (generator not committed) |
| "File offset" column | K23.md:37 | Field is `offset`; semantics not retained | Numerically equal to connector `file_offset` |
| Data-header magic, kind, length | K23.md:41-42 | Yes | `carriers.json`; committed preflight would compute the same fields (not run) |
| Instruction rows "Not a data header" | K23.md:39-40 | Nulls and `magic_valid:false` only | Inference (F8) |
| Snapshot hash `78da37fe…` | K23.md:44 | Yes (`snapshot_hash`, `candidates`) | REA only; no committed non-REA derivation (F6) |
| "Two reported header sources" | K23.md:44 | Count only (`snapshot_hash_sources: 2`) | Sources not identified |
| Table, count, hash, bounds "recomputed by recheck" | K23.md:45-46 | **No** | **False** (F1) |
| string_pool `coverage: partial` | K23.md:50 | Yes | REA only; replicated by connector run (same binary) |
| Package URI and token counts are capped lower bounds | K23.md:50-51 | Yes: lists and `_at_least` values, consistent with the 2× rule | Documented rule `SchemaInspectDartAot.md:63`; the rule is not in the envelope |
| "Capped flag" (limitation 5) | envelope `limitations[5]` | **No** key exists | No (F4) |
| `printable_run_count` bound status | not claimed in K23; W1 generalizes | Integer only; no bound marker | Unknown (F4) |
| Top-level `coverage: partial` | not in K23 | Yes | Not discussed (F3) |
| "No SDK version inferred" | K23.md:53-54 | n/a | Correct (F12) |
| Recheck command | K23.md:3 | Placeholder `<MEASURED-COMMIT>` | No candidate-rev run exists (F2) |

## Findings

### F1 [High] The recheck does not recompute; the knowledge overstates it
- Claim: K23.md:44-46, "recomputed from the committed envelope by the `recheck:` command, not supplied as naked counts."
- Observed: `describe-dart.py:42-46` copies `normalized_result.libapp` (including `sections`, `snapshot_hash`, `snapshot_hash_candidates`, and `snapshot_hash_sources`), `string_pool.coverage`, `package_uri_count_at_least`, `dart_uri_count_at_least`, and `limitations` into its output. The only derived values are the envelope SHA-256 (line 38), `stdout_byte_equal` (line 39), and the consistency booleans at lines 47-49. The script never reads the APK, so it cannot recompute a section table or a hash.
- Observed: `describe-dart.py:51` is `return 0` whatever the booleans say. The docstring (`describe-dart.py:1-5`) defines exit 0 as "report produced", not pass.
- Observed: `corpus/lessons/round-23.md:19` anchors admission on the bare field `"snapshot_hash_sources":2`, which is the naked count K23 says it does not use.
- Required correction: say "copied verbatim from the committed envelope; consistency checked by hand," or add a real recomputation.

### F2 [Medium] Recheck command is unbound; the only recorded run is at another commit
- Observed: K23.md:3 contains the literal `--rev <MEASURED-COMMIT>`. The command cannot run as written.
- Observed: `verify/initial/dart-record.json` records `source_rev 6615aeae642aec36959180e7ea940b2794c7f1cb`, exit 0, `passed: true`, and stdout with `envelope_sha256 7768198e…4c508` and all booleans true.
- Observed by blob comparison (`git rev-parse` per path): the envelope, run, receipt, `describe-dart.py`, `verify.py`, K23.md, and `SOURCES.md` are byte-identical at 6615aeae and 2838351. The 6615aeae record therefore transfers by content, but no run exists at the candidate.
- Observed: `verify.py:72` predicate is `stdout_byte_equal` and `subject_digest_matches_fetch` and `argv_target_matches_subject` and `libapp.coverage == 'complete'` and `len(sections) == 4` and `string_pool_coverage == 'partial'`. It does not check section names, snapshot hash, `snapshot_hash_sources`, top-level coverage, target SHA vs subject SHA, or target bytes vs receipt size.

### F3 [Medium] Top-level partial coverage is retained and undisclosed
- Observed: `data.normalized_result.coverage = "partial"`.
- Observed: K23.md mentions only `libapp.coverage:complete` (line 35) and `string_pool.coverage:partial` (line 50). W1 `ConnectDartSymbols.md:293` expects "normalized_result.coverage partial".
- Observed: `ConnectDartSymbols.md:156` attributes the top-level partial to "string-pool caps only". No committed rule supports that, so treat it as Inferred.
- Consequence: K23.md:7 "first successful inspect-dart-aot" is true of `ok:true`, but the record as a whole is partial. The knowledge should say so.

### F4 [Medium] String-pool bounds: the referenced flag is absent and one count has no bound marker
- Observed: `data.limitations[5]` says values beyond twice the bound "are counted only through the capped flag." A recursive key walk of the envelope finds no key containing `cap`. The word appears only in this text.
- Observed: `data.limitations[6]` says overflowed printable runs make counts lower bounds and are omitted. No overflow flag is retained. `string_pool.printable_run_count = 50666` has no `_at_least` sibling.
- Unknown: whether `printable_run_count` is exact. The retained record cannot say.
- Positive: `package_uris` length 500 with `package_uri_count_at_least` 1000, and `class_like_tokens` length 2000 with `class_like_token_count_at_least` 4000, match the 2x collection rule in `.ufo/waves/round-22/w2/SchemaInspectDartAot.md:63`. `dart_uris` length 215 with `dart_uri_count_at_least` 215 is uncapped.
- W1 `ConnectDartSymbols.md:226-227` says "its counts are lower bounds", which over-generalizes to `printable_run_count`. K23.md:50-51 correctly restricts the claim to package URI and token projections.

### F5 [Medium] Producer identity and attribution are absent from the run record
- Observed: `inspect-dart-legacy-saber.run.json` has exactly the keys `argv, cwd, env_overrides, exit, stdout, stderr, captured_at`. It has no producer, no resolved package path, no tool version, no Node or npx version, and no target digest.
- Observed: "These are L1-produced records" (K23.md:30) rests on the `producer` field of `legacy-saber-download.json` ("KaidokuR23 L1 after connector scope deviation") and the knowledge text.
- Observed: "REA 6.5.0" appears only as argv token `rea-agents@6.5.0`. `data.provider.version` is null.
- Observed comparison: the connector's committed run for the same spec, `connect-dart-symbols/inspect-dart-aot-saber-1330203.run.json`, records `resolved_tool {version 6.5.0, package_path …/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents, node v24.21.0, npx 11.19.0}`, a `producer`, and `target {sha256, bytes}`. The L1 pair has none of these.
- Consequence: the L1 pair does not bind which code executed. Run-time digest binding is only REA's self-report (`target.sha256`) plus the L1 receipt.
- Inferred: L1 probably used the same npx cache directory (`ad9a3fdbcad992c6`), but nothing in the L1 record shows it.

### F6 [Medium] Snapshot hash `78da37fed6bf1489361a312568249f3f` has no committed non-REA derivation
- Observed retained: `libapp.snapshot_hash`, `snapshot_hash_candidates` (one entry), and `snapshot_hash_sources: 2`. The last is a count only.
- Unknown retained: the identities of the two sources, and the 32 bytes at +20 of each data header.
- Observed corroboration, all REA-derived or from an uncommitted generator: the connector identify envelope `identify-flutter-build-saber-1330203.envelope.json` (candidate list `78da…`), and `carriers.json` `data_snapshot_headers[].snapshot_hash` (`78da…` twice). `carriers.json` has no generator in the tree; its top-level keys are `schema, generated_at_utc, producer, provider_requirement, carriers, boundary`.
- Observed: committed `preflight_dart_carrier.py` (sha256 prefix `08d0c460…`, matching the connector README table) contains zero occurrences of `snapshot_hash`. It reads magic, length (`<Q` at +4), and kind (`<Q` at +12) only.
- Conclusion: the hash is bound only to the REA producer. K23.md:44 states it as an observation of REA output, which is accurate; it is not an independent verification.

### F7 [Low–Medium] The `libapp complete` predicate is not retained; retained values satisfy it by hand
- Observed: W1 `SchemaDart.md:74-78` states that `complete` requires all four names, both `*Data` symbols with a valid complete header, exactly two data headers, one distinct hash with two sources, no aliasing or overlap, magic `f5f5dcdc`, `kind == 3`, a 32-hex hash at +20, and a declared length that fits its symbol. It cites uncommitted npm dist lines (`FlutterBuildProvider.js:650-659`, `DartElf.js:386-418`).
- Observed: K23.md:35-36 says "scoped to the reader's section/header contract" and neither states nor cites the predicate.
- Checked by hand (arithmetic on committed fields, no tool): data ranges `[832, 19216)` and `[19264, 7172432)`; instruction ranges `[7208960, 7298896)` and `[7298944, 17337632)`. No overlaps. All lie inside `libapp.bytes = 17367984`. `header_length` 16842 ≤ 18384 and 6058354 ≤ 7153168. Kinds 3 and 3. Magic true and true. The hash is 32 hex characters. One candidate, two sources.
- Verdict: consistent with the W1-described predicate. Aliasing, the hash's +20 location, and the header bytes are not retained, so the pair alone cannot verify them.

### F8 [Low] Four symbol records: names and values corroborated; labels and instruction semantics not retained
- Observed positive: the names are exactly `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotInstructions`, `_kDartVmSnapshotData`, and `_kDartIsolateSnapshotData`, in that order.
  - `_kDartVmSnapshotInstructions`: offset 7208960 (`0x6e0000`), size 89936.
  - `_kDartIsolateSnapshotInstructions`: offset 7298944 (`0x6f5f80`), size 10038688.
  - `_kDartVmSnapshotData`: offset 832 (`0x340`), size 18384, magic true, kind 3, header_length 16842.
  - `_kDartIsolateSnapshotData`: offset 19264 (`0x4b40`), size 7153168, magic true, kind 3, header_length 6058354.
  These match the 1.33.2 entry of `carriers.json` (`libapp_elf.kdart_dynsym` value, `file_offset`, and size; `data_snapshot_headers`) exactly. The generator is uncommitted (F6).
- Label gap: K23.md:37 says "File offset". The envelope field is `offset`, and its semantics are not retained. For this carrier `file_offset` equals `value` in `carriers.json`, so the label is numerically correct but corroborated only by an uncommitted generator.
- Instruction rows: `magic_valid:false` with `kind` and `header_length` null (`sections[0]`, `sections[1]`). The record does not say whether the magic was read and mismatched or not applicable. "Not a data header" (K23.md:39-40) is Inferred. The committed preflight reads magic only for `*Data` names, so no committed code checks instruction rows.

### F9 [Low] ABI "selected" (K23.md:33) is not bound inside the pair
- Observed: the pair retains `normalized_result.abi = "x86_64"`. The run argv has no `--abi`. Per `SchemaDart.md:24` and `:39-40`, the reader defaults to a preference order (arm64-v8a, x86_64, x86, armeabi-v7a, then alphabetical). The pair retains neither the enumeration nor the rule applied.
- Observed outside the pair: the connector identify envelope `identify-flutter-build-saber-1330203.envelope.json` has exactly one `abis` entry, `x86_64`. The index entry `connect-dart-symbols/fetch.json` `downloads[0].index_entry.nativecode` is `["x86_64"]`.
- Verdict: the wording is correct for this APK; the binding is outside the pair.

### F10 [Low] Target identity: strong, with two gaps
- Observed, all committed: `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`, 41263437 bytes, at `…/round-23/runtime/saber-1330203.apk`.
  - Envelope: `subject.digest.sha256`, `normalized_result.target.sha256`, `target.bytes`, `subject.local_path`, `parameters.path`, `locations[0].path`, `normalized_result.target.path`.
  - Run: `argv[4]` is the same path.
  - Receipt `legacy-saber-download.json`: `sha256`, `size`, `status: 200`, `captured_at 2026-10-21T14:47:18.289487+00:00`.
  - Connector `fetch.json`: index entry hash and size equal; `observed_sha256` equal; `hash_matches_index: true`. This is a separate fetch to `/tmp/kd23work/`.
  - Connector run and identify envelopes: same SHA and bytes.
- Observed [WT]: `sha256sum` of the runtime APK is `a7b1…ea618`. `stat` gives size 41263437 and mtime 2026-10-21 11:47:18.287 at −03, which is 14:47:18.287 UTC. That precedes the run's `captured_at` of 14:47:19.045 UTC, so the file was not changed after the run.
- Gap 1: the F-Droid `index-v1.jar` signature is not verified (`fetch.json` `archive_index.signature_note`). The digest is index-attested, not signature-attested. K23.md:20-22 says so correctly.
- Gap 2: `evidence_id` is path-sensitive. The connector run at `/tmp/kd23work/` gave `ev_dcdab9d0…` with an otherwise identical normalized result. K23.md:3 says "live replay is the retained .run.json argv", which requires the identical absolute path.

### F11 [Low; counting-adjacent] Duplicate and scope-deviated witnesses sit in the same tree
- Observed, full-envelope diff: `connect-dart-symbols/inspect-dart-aot-saber-1330203.envelope.json` differs from the L1 envelope in exactly six leaves: `evidence_id`, four path leaves (`subject.local_path`, `parameters.path`, `locations[0].path`, `normalized_result.target.path`), and `meta.duration` (211ms vs 126ms). Nothing in `libapp`, `sections`, or `string_pool` differs.
- Observed: `connect-dart-symbols/inspect-dart-aot-saber-1340303.envelope.json` is a second legacy-complete carrier (`ac68a976…`, hash `ace65428…`).
- Observed: `ConnectDartSymbols.md:13-24` discloses that these files were written outside the connector's contract and are frozen.
- K23.md never mentions the duplicate or the second carrier. K23.md:64-65 says to count `inspect-dart-aot` once. The counter must not glob `connect-dart-symbols/`; I did not verify that, and it belongs to the counter seat. K23 should disclose the duplicate.

### F12 [Low; affects other documents] Dart version conflict in connector material
- Observed: `connect-dart-symbols/README.md` and `ConnectDartSymbols.md:123,197` attribute "Dart 3.11.4" to this APK. The string was extracted from `libflutter.so` by the connector's `VERSION_RE` in `preflight_dart_carrier.py`.
- Observed: the connector identify envelope for the same bytes reports `abis[0].libflutter.dart_version: null` and `dart_version_capped: false`.
- Observed: K23.md:53-54 says "No SDK version is inferred from a bare snapshot hash" and claims no version. That is correct. "3.11.4" must not be imported as REA evidence.

### F13 [Low; W1 defect] Placeholder left in `ConnectDartSymbols.md`
- Observed: `ConnectDartSymbols.md:162` reads "stdout 87,0xx B" for the 1340303 probe. The committed envelope is 89,155 bytes (sha256 `22d1acd0…`). The other values on that line (`ev_04072bb4…`, printable 50,419, dart_uri ≥ 216) match committed bytes. The 1330203 line "87,049 B" matches (87049 bytes).

### F14 [Low; missed corroboration] F-Droid index entry is not cited
- Observed: `connect-dart-symbols/fetch.json` `downloads[0].index_entry` gives the same SHA-256 and size. K23.md and S061 (`corpus/SOURCES.md:67`) do not cite it. `ConnectDartSymbols.md:232-233` proposed a source row for it, and none was minted. Citing it would strengthen F10 without changing any verdict.

### F15 [Positive] Source linkage
- Observed: `corpus/SOURCES.md:67` S061 is status A, own-work, with used-by `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md, corpus/lessons/round-23.md`. Both files exist at the candidate. K23.md:1 cites S061. The `claims.json` "sourced" linkage requirement is met; content is a separate question (F1, F4).

### F16 [Positive] REA output is deterministic on these bytes
- Observed: the connector's independent run and the L1 run give identical `libapp` (SHA-256, bytes, sections, snapshot hash, sources) and `string_pool` values. This shows determinism of one binary on the same bytes. It is not independent measurement.

## W1 re-evaluation against the candidate

| W1 item | Candidate status |
|---|---|
| `ConnectDartSymbols.md:291-293` expectations: exit 0, `meta.command`, `abi` x86_64, libapp complete, 4 sections, hash `78da…`, sources 2, top-level partial | All satisfied by the L1 envelope. |
| `ConnectDartSymbols.md` §6 qualifiers 1-2 (carrier-conditional; R22 refusal preserved) | Present: K23.md:8, 58-60, 61. |
| §6 qualifier 3 ("its counts are lower bounds") | Over-generalized. K23 is correct. See F4. |
| §6 source rows (a) Dart commit, (b) F-Droid index entry, (c) probe receipts | Only S061 minted. See F14. |
| §4 probe table and receipts | Match committed bytes except F13. |
| `SchemaDart.md` §2 `complete` predicate | Re-derivable by hand from retained fields; source uncommitted. See F7. |
| `ReviewDartScope.md`: keep the SDK-generation explanation inferential | K23 complies; it claims no SDK version. |
| `DartSaberRefusal.md`, `DartSymbolSource.md`, `DartCarrierFdroid.md` | Cover the R22 refusal, SDK source declarations, and other carriers. A pattern scan for the pair's identifiers (`1330203`, `1340303`, `legacy`, `libapp`, `string_pool`) found no pair-specific claim. Not re-evaluated in depth; other seats own them. |

## Produced files and hashes

- `.ufo/waves/round-23/w2/OriginalDart.md`: this report. Its own SHA-256 is recorded in the seat's final message, since a file cannot contain its own hash.
- Ignored scratch under `.ufo/waves/round-23/runtime/OriginalDart/`: exact `git show` copies at `2838351`, with sha256 values:
  - `L1.env.json` 7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508
  - `L1.run.json` 588460380006a5c1044ba8fb9b8b0136446a2cab5c40e8f2f911978328e82fa6
  - `L1.fetch.json` 2e6c00305dfbaf09001c421df6e4cf0730dcce3bfb7a5aa5acc358873da40496
  - `conn-1330203.env.json` 7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1
  - `conn-1330203.run.json` 4b263db8e6060a659f1cf81aab3df025b4014afecdd59258464d57351fe7938d
  - `conn-1340303.env.json` 22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d
  - `conn-1340303.run.json` 34f4ab462e0df49d6f9ff476e619f6bf2e01da750824771da5c8e1e8f78b3db3
  - `conn-id-1330203.env.json` 3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626
  - `conn-id-1330203.run.json` 9660b55cc8ed0046f67adace0e75636777c2696e5b111f5b918f9fe196b8cd60
  - `carriers.json` 652f05a626078250f617f7f4f3b5d64ca56d286b8654137757a5009ba983f2c6
  - `conn-fetch.json` 6beac67b0f6361accc59729c969965b9b8f0f777f5beaca7dd1ed65b11566f2d
  - `K23.md` 22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351
  - `SOURCES.md` 736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525
  - `verify-dart-record.json` af4b34626d7ec4dd905d5c531ec2f4e0bb00cd91cd1dc8b1a80203259df6693c
  - `describe-dart.py` 145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f
  - `verify.py` 59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a
  - `lessons-r23.md` 8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723
  - W1 copies: `ConnectDartSymbols.md`, `SchemaDart.md`, `ReviewDartScope.md`, `DartSaberRefusal.md`, `DartSymbolSource.md`, `DartCarrierFdroid.md`
- Disclosure: an earlier scratch directory `/tmp/r23dart` was created outside the permitted write paths and has been removed.
- The worktree file `runtime/saber-1330203.apk` was only read (`sha256sum`, `stat`). It was not modified.

## Installs

None. No package, tool, or runtime was installed or updated. Read-only tools only: `git` (`show`, `rev-parse`, `cat-file`, `diff`), `sha256sum`, `stat`, `cut`, `wc`, and Python 3 standard-library JSON parsing, plus one `grep -c` over a candidate blob.

## Open risks

1. No candidate-rev run of `describe-dart.py` exists. The recheck command needs a real commit in place of `<MEASURED-COMMIT>` (K23.md:3). The designated run seat or L1 should run it once at the candidate. I did not.
2. The snapshot hash, section identities, and string-pool counts have no committed non-REA derivation. Independent recomputation requires a non-REA parser run over the runtime APK. I did not do it, because this review was limited to committed bytes.
3. The `complete` predicate's source is uncommitted npm code. The candidate cannot justify the label alone (F7).
4. The L1 run record does not bind the executed package. Recommended: retain the npx-resolved package path, version, and integrity for the L1 run.
5. Duplicate and scope-deviated witnesses sit in `evidence/c1/connect-dart-symbols/` (F11). The counter must exclude them. Not verified here.
6. The connector's SDK-version material conflicts with REA identify output (F12). It must not be imported.
7. Whether `count-c1.py` globs the `connect-dart-symbols/` subdirectory is unverified here (counter seat).
