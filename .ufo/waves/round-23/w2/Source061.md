# Source061 — S061 own-work / Dart Gate source review (R23-C1 coverage)

Seat: KaidokuR23.Source061 · leaf · no delegation · no live run · author-side, not independent admission
Candidate: 2838351450ff1ee4baa620c962a1153450d53311 · Baseline: aa1450b82f9ede35aada63efe8a34e01c6e02f72 · Dart gate measured at: 6615aeae642aec36959180e7ea940b2794c7f1cb

Method: `git show <rev>:PATH` only; python used only to parse committed JSON; one narrow grep and targeted reads of the installed rea-agents@6.5.0 package (the package S048/S040 already cite). No lane counter, gate, describe script, producer or APK was executed.

## Verdict

The single-carrier observation holds. The committed L1 envelope is byte-identical to its producer stdout. Its digests, evidence ID, section table, and libapp/string-pool labels match the knowledge file, and the R22 contrast is correct. Four admitted statements overclaim (F1, F2, F4, F5), and the gate is weaker than its stated purpose (F3). The counter reads only the `source:` line, the S061 row cells 1/4/8/9/11, cited paths, and `ev_` IDs (static reading of count-c1.py), so these are admission-wording defects, not count defects.

## Observed, verified on committed bytes

| # | Check | Result |
|---|---|---|
| O1 | envelope vs producer stdout | byte-equal (`raw == run['stdout'].encode()` → True). Envelope blob `f75bdc238a31`, sha256 `7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508`, equal to `verify/initial/dart-record.json` `envelope_sha256` |
| O2 | `inspect-dart-legacy-saber.run.json` | sha256 `588460380006a5c1044ba8fb9b8b0136446a2cab5c40e8f2f911978328e82fa6`; argv `npx -y rea-agents@6.5.0 inspect-dart-aot <lane>/runtime/saber-1330203.apk --format json --full-output`; exit 0; stderr `""`; env_overrides `{}` |
| O3 | envelope identity | ok true; meta.command `inspect-dart-aot`; data.operation `inspect_dart_aot`; evidence_id `ev_d2ff19d7100f34b52e4b2bc52ee115e48428624f7da57814e5f184b4bd4c7491` (identical in knowledge file) |
| O4 | selected artifact | subject digest = target.sha256 = fetch receipt sha256 `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`; target.bytes 41263437 = fetch size. Fetch receipt `legacy-saber-download.json` blob `a94a6981850f`, sha256 `2e6c00305dfbaf09001c421df6e4cf0730dcce3bfb7a5aa5acc358873da40496` |
| O5 | libapp | abi x86_64; sha256 `f82ab4111807552af82ada747c5cccfe49474ecfcce49d5e0c3c701feeab38a8`; snapshot_hash `78da37fed6bf1489361a312568249f3f`; snapshot_hash_sources 2; snapshot_hash_candidates 1 |
| O6 | section table | offsets, sizes, magic_valid, kind, header_length match knowledge lines 39–42 (all numbers present in envelope, programmatic check) |
| O7 | string_pool | coverage partial; lower bounds 1000 / 215 / 4000; lists capped at 500 / 215 / 2000; matches limitations [7]–[8] |
| O8 | libapp vs string-pool separation | independent producer labels: libapp.coverage (FlutterBuildProvider.js:669) vs string_pool.coverage (:678). Committed limitations contain none of the libapp-partial messages (:698–716) and do contain the pool-capacity message (:717–721) |
| O9 | R22 contrast | `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.envelope.json` (aa1450b, sha256 `2b13cb8fad6d21fdd9633e8fc28d5e06326c6fe0e119462d54f77966e3c5c145`): unsupported_target; all four symbols "not in the dynamic symbol table". Knowledge's contrast is correct. R22 run artifact `…saber_1360103.apk`, sha `de4813f9…acb720`, matches R22 identify subject |
| O10 | binding, static reading only | round-20 `HEX64` requires the `ev_` prefix, satisfying round-21's ID check. Key scan of the committed envelope: no error/errors/exit_code, no ok≠true, no refusal code values. `command_pattern` matches `inspect-dart-aot` in the knowledge file. Static reading: entry binds. Not executed |
| O11 | blob identity | verify.py, describe-dart.py, envelope, run, fetch receipt, connector fetch.json and identify envelope, knowledge file, SOURCES.md are identical at 6615aea and 2838351. Only corpus/lessons/round-23.md differs, and none of its added lines mention Dart, Saber, libapp or string pool. The dart-record pass therefore covers the candidate's Dart inputs |

## Findings

**F1 (medium, observed) — S061 admission text overgeneralizes "complete".**
- `corpus/SOURCES.md:67`, column 7: "A carrier exporting the four supported snapshot symbols yields complete libapp section/header observations…"
- Producer, installed `rea-agents@6.5.0/dist/flutter/FlutterBuildProvider.js` (sha256 `2c00116a02ee3e9a483886a14ec84d7f224899c8807c84c999bcca49b043d191`): libapp.coverage is complete only when `snapshotPartial` is false (:652–659, :669). That also requires no inventory failure, no aliased data symbols (:630–637, :704–708), no overlapping data symbols (:645–648, :709–713), exactly 2 data headers each `complete` (:656–657; kind must be 3, declared length must fit, magic and valid hash required, per :714–716), exactly one hash candidate (:658), and exactly two hash sources (:659).
- Four symbols alone do not yield complete. The claim rests on one carrier (n=1).
- Fix: restate as this carrier's observed conditions citing :652–659, or narrow the sentence.

**F2 (medium, observed) — "recomputed" overclaims the recheck.**
- `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md:45–46`: "The table, source count, hash and lower-bound values are recomputed from the committed envelope by the `recheck:` command…"
- `.ufo/waves/round-23/tools/describe-dart.py` (sha256 `145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f`): line 42 `'libapp': n['libapp']` copies the object verbatim; lines 43–44 copy string-pool coverage and `.get` lower bounds. Actual checks: envelope sha256 (`envelope_sha256`), stdout byte equality (:39), argv[4] == subject.local_path, subject digest == fetch sha256 (:48, fetch receipt self-recorded), command equality (:49).
- Fix: say "echoes", and list those checks.

**F3 (medium-low, observed) — the dart-record gate checks labels and omits the producer contract and exit.**
- `.ufo/waves/round-23/verify.py:72` (sha256 `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a`), predicate: stdout_byte_equal ∧ subject_digest_matches_fetch ∧ argv_target_matches_subject ∧ libapp.coverage=='complete' ∧ len(sections)==4 ∧ string_pool_coverage=='partial'.
- Not checked: producer exit and stderr (describe :37 prints `exit`), `ok`, `command_matches` (:49), `operation`, section names, data-section kind == 3, hash_sources == 2.
- Envelope and run.json are both committed bytes, so a consistent edit to both passes. This is author-side tamper evidence only.
- Fix: add exit == 0, ok is True, command_matches, section names, kind, and hash sources.

**F4 (medium-low, observed) — the admitted envelope carries an SDK-version mapping that no lane source supports.**
- `inspect-dart-legacy-saber.envelope.json:1`, data.limitations[2]: "complete decoding supports kind 3 (the Dart 2.14 FullAOT layout)…". Same text at producer :694.
- The knowledge file and SOURCES do not repeat "2.14" (grep: no hit). That is correct. But S061 admits the whole envelope with no disclaimer.
- REA's own identify on the same digest reports `libflutter.dart_version: null`, `dart_version_capped: false` (`connect-dart-symbols/identify-flutter-build-saber-1330203.envelope.json`, sha256 `3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626`). The "Dart 3.11.4 / 3.12.2 / 3.13.2" labels exist only in connector author-side files (`connect-dart-symbols/README.md`, sha256 `83de3786…`; `w1/ConnectDartSymbols.md:197–204`). They must not enter S061.
- Fix: add to S061 that the producer's "Dart 2.14" prose is unverified and not adopted, and that no SDK version is observed. Define "legacy-layout" as "four legacy symbol names with kind-3 headers".

**F5 (low-medium, observed rule plus inference) — ABI selection is unrecorded; "selected" rests on an unstated rule.**
- knowledge line 33 "selected ABI is x86_64"; SOURCES:67 column 5 "x86_64 selected ABI". The envelope's parameters carry only `path`, and argv has no abi option.
- Producer :547–552: with abi undefined, preference is arm64-v8a > x86_64 > x86 > armeabi-v7a, then code-point order.
- [INFERENCE] If the CLI passes undefined (not inspected), x86_64 selection means no `lib/arm64-v8a/libapp.so` candidate existed. Candidates x86 or armeabi-v7a would be unobserved.
- Corroboration, author-side and unsigned: `connect-dart-symbols/fetch.json` (sha256 `6beac67b0f6361accc59729c969965b9b8f0f777f5beaca7dd1ed65b11566f2d`), index_entry versionCode 1330203, `nativecode: ["x86_64"]`.
- Fix: cite :547–552 and the index entry, and state that other ABIs are unobserved.

**F6 (low, observed) — knowledge omits two string-pool limitations present in the envelope.**
- Knowledge lines 50–51 give only "capped lower bounds".
- Envelope limitations[5] ("collection stops at twice each projection bound…") and [6] ("String-pool collection or printable-run capacity was exceeded; counts are lower bounds and overflowed runs are omitted"; producer :717–721, collectionCapped). So `printable_run_count` 50666 is also a lower bound.
- Fix: name both.

**F7 (low, observed source) — `magic_valid:false` on instruction symbols is a default, not a check result.**
- Producer :610–612 reads a header only for names ending "Data"; :617 `magic_valid: header?.magicValid ?? false`.
- Knowledge table lines 39–40 ("Not a data header; magic_valid:false") are right in intent. The envelope still cannot distinguish "not attempted" from "checked, false" for those rows.
- Fix: add a table note.

**F8 (low, observed plus source) — the evidence ID is path-bound; exact replay requires the identical absolute path.**
- Installed `dist/domain/evidence.js` (sha256 `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff`), :156–180: the semantic projection includes normalized_result (incl. target.path), parameters (path), and locations (path). It excludes subject.local_path and meta. computeEvidenceId is at :182.
- Observed: `connect-dart-symbols/inspect-dart-aot-saber-1330203.envelope.json` (sha256 `7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1`) has the same digest and limitations, and normalized_result is identical after removing target.path. meta.duration differs (211ms vs 126ms). Its evidence_id `ev_dcdab9d0…224130fe` differs from L1's `ev_d2ff19d7…c7491` only through the path fields (`/tmp/kd23work/` vs runtime path).
- Consequences: knowledge line 3 "live replay is the retained .run.json argv" reproduces the same ID only at the identical absolute runtime path. The envelope embeds `/home/vgpnk/…` paths. Neither the knowledge file nor SOURCES pins the envelope file's own sha256 `7768198e…` (grep count 0 in both); only the evidence ID and APK digest are pinned.
- Fix: add the envelope file sha256 to S061 and the replay note.

**F9 (low, observed) — "exact pinned" / "digest-pinned" is self-recorded.**
- `legacy-saber-download.json`: `"signature_verification": "not performed; digest identity only"`.
- Corroboration: connector `fetch.json` index-v1.jar entry, hash `a7b1…3ea618`, size 41263437. Its own note says the jar is not cryptographically verified (signature algorithm weak/disabled).
- Knowledge lines 2–3 and the row say "pinned". The evidence is two author-side records plus an unsigned index.
- Fix: say "digest-pinned, not signature-verified".

**F10 (low, observed) — top-level coverage is an aggregate, not a libapp result.**
- Envelope normalized_result.coverage "partial" equals producer :687 (`snapshotPartial || poolPartial`). Here it is driven by string_pool. The knowledge file does not name this field.
- Fix: name it, and warn against citing it as libapp coverage.

**F11 (cosmetic, observed) — glued tokens in committed prose.**
- Knowledge file: "HTTP200", "size41263437", "kind3", "length16842", "length6058354". SOURCES:67: "opened2026-10-21".
- The counter reads the date from cell 9 separately, so counting is unaffected. Exact-value readability suffers.

**F12 (open risk, observed) — out-of-scope connector outputs sit inside the counted evidence root.**
- `.ufo/waves/round-23/evidence/c1/connect-dart-symbols/` (six envelope/run files; carriers.json sha256 `652f05a6…83f2c6`; preflight_dart_carrier.py sha256 `08d0c460…105514`) lies under round-23/evidence/c1, which is a counted root.
- Static reading of count-c1 `cited_pattern`: no eligible entry cites them with the full root prefix, so no count results. Keep them unadmitted.

## Unknown / not verified
- APK bytes were not re-hashed. The runtime copy is ignored, and no live reads were permitted. The digest chain rests on committed records.
- Other ABI libapps, if present, are unknown. The CLI default for abi was not inspected.
- F-Droid index-v1.jar signature: not verified (per the connector's own note).
- No counter or gate was executed. The held count and any dart-record re-run belong to the Run seats.
- The carrier's Dart SDK version is not observed by REA and is not claimed here.

## Frozen falsifiers (static)
- refusal counted: no. The envelope is ok:true with no refusal keys (O10).
- copy erases parent refusal: no copy is admitted; the bound object is the original file.
- mere mention counts: no. Binding requires the envelope's own evidence_id.
- inherited identify lost: unaffected.
- same verb double counted: no. inspect-dart-aot is counted once.
- source linkage absent: no. The `source:` first line cites S061, and used-by lists the knowledge file.
- relevance/ownership unsupported: partially. F1, F4, and F5 concern admitted wording.

## Produced files and hashes
- `.ufo/waves/round-23/w2/Source061.md` (this file; its sha256 is reported in the final message).
- No other file written. runtime/ untouched.

## Installs or none
None. No install, update, or config change. Read-only consumption of the installed rea-agents@6.5.0 sources: `dist/flutter/FlutterBuildProvider.js` (sha256 `2c00116a…b043d191`) and `dist/domain/evidence.js` (sha256 `f992d93e…8a78dcff`), plus one narrow grep for the `ev_` constructor in `dist/`.

## Open risks
- F3 and F12 persist if the Run seats re-run the gate with the same predicate.
- F8 breaks any replay from a different absolute path, so the replay note must be corrected before anyone relies on it.
- Connector outputs (F12) are committed under the counted root and must stay unadmitted.
