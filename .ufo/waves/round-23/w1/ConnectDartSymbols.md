# ConnectDartSymbols — R23-C1: the `inspect-dart-aot` gate is carrier generation, not ABI

Seat: `KaidokuR23.ConnectDartSymbols` (connector, leaf, author-side).
Lane HEAD: `a3c92eb6bc70984e90ae5b895412de978840b2c5`.
Scope: connect the R22 Flutter-positive / Dart-refusal pair to the ABI and
dynamic-symbol requirements REA 6.5.0 actually applies, and name a carrier that
can add a T1 verb. Static parsing only. No debugger, Frida, process attach,
device access, or APK execution occurred.

**Status: author-side proposal, not outside verification and not an admission.**
L1 owns integration, counting, and independent re-execution.

## 0. Scope deviation (disclosed on L1 instruction)

Before L1's correction arrived, this seat wrote nine files under
`.ufo/waves/round-23/evidence/c1/connect-dart-symbols/` (three CLI envelopes,
three `.run.json` receipts, `carriers.json`, `fetch.json`,
`preflight_dart_carrier.py`, `README.md`). My read-only connector contract
permits only this report, so those writes are a **scope deviation**. Per
instruction they were not removed and are now frozen: no further production
writes, no further probes or downloads. Nothing below rests on their authority;
they are named only so L1 can find, inspect, or re-derive the same bytes. L1
should re-fetch, re-hash, and re-execute the selected carrier itself before
admitting anything.

## 1. What the R22 refusal actually says (observation)

Retained R22 record: `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.run.json`
(sha256 `d1eaa23f96ec4a9695af4f373051da8ad3e87fc3dff3bbee083eed5eaf2eb34a`).
Artifact `/tmp/kd22probe/saber.apk`, 42,305,081 B, sha256
`de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720` (F-Droid
`https://f-droid.org/repo/com.adilhanney.saber_1360103.apk`, Saber 1.36.1).

```
npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --format json --full-output
exit 1, stderr ""
code: unsupported_target, retryable: false
message: No recognizable Dart snapshot symbols were found:
  symbol _kDartVmSnapshotData is not in the dynamic symbol table;
  symbol _kDartVmSnapshotInstructions is not in the dynamic symbol table;
  symbol _kDartIsolateSnapshotData is not in the dynamic symbol table;
  symbol _kDartIsolateSnapshotInstructions is not in the dynamic symbol table
```

This is the `sections.length === 0` branch, reached **after** ABI selection.
The ABI-specific refusal is a different message
(`No libapp.so was found for ABI <abi>; available: …`,
`FlutterBuildProvider.js:553-557` in the installed 6.5.0 dist). The APK carries
one ABI, `x86_64`, so no ABI substitution was ever available or needed. The
refusal is a symbol-name refusal.

## 2. The exact 6.5.0 requirement (observation, installed source)

Installed dist: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(package version `6.5.0`; the separate `6.7.0` cache
`/home/vgpnk/.npm/_npx/a1722018f28f9df2` was read but not executed).

| Gate | Source |
|---|---|
| APK only; candidates are `lib/<abi>/libapp.so` | `dist/flutter/FlutterBuildProvider.js:543-551` |
| Default ABI order `arm64-v8a, x86_64, x86, armeabi-v7a` | same `:547` |
| Recognized names are exactly the four legacy names | same `:599` (first name), list through `:603` |
| Symbol lookup reads **SHT_DYNSYM only**; no `.symtab` fallback | `dist/flutter/DartElf.js:180` (type check), `:328` (wanted set) |
| Zero resolved names → `unsupported_target` | `FlutterBuildProvider.js:650` |
| Complete libapp coverage needs kind 3, valid hash, length fits | `DartElf.js:387-417` (`complete` at `:412-416`) |
| Budgets: APK ≤ 2 GiB, one library ≤ 256 MiB, total extraction ≤ 768 MiB | `FlutterBuildProvider.js:26-31` |

Consequences that matter for carrier selection:

1. Names present only in `.symtab` are invisible; the carrier must export them
   in `.dynsym`.
2. The gate is zero-vs-nonzero: **one** legacy name avoids refusal (partial
   coverage), all four plus kind-3 data headers give `libapp.coverage: complete`.
3. `rea-agents@6.7.0` still contains only the four legacy names
   (`dist/flutter/FlutterBuildProvider.js:639`) and no occurrence of
   `_kDartSnapshotText`/`_kDartSnapshotData` anywhere in `dist/`. Upgrading the
   cached CLI does not change this gate. (Observation about 6.7.0 only; no
   claim about future releases.)

## 3. Why the R22 carrier misses the gate: Dart 3.13 moved two contracts (observation + inference)

Observation, sabre 1.36.1 `lib/x86_64/libapp.so` (sha256
`b54b19d243b6db78e27f9147b56dc0aa17ef6119fa905c2e2f7c72eb2f198feb`,
16,778,120 B):

- `.dynstr` is exactly `_kDartSnapshotText`, `_kDartSnapshotData`,
  `_kDartSnapshotBuildId`; no legacy name anywhere, no `.symtab`.
- The single data snapshot at file offset `0x2c0` has magic `f5f5dcdc`, declared
  length 6,098,754, hash `0451907c2eaa8467e848c0067bfe8ed4`, and **kind 2**.
  REA's completeness rule requires kind 3 (`DartElf.js:415`), so even a
  hypothetical legacy-name alias would yield only partial coverage.
- `lib/x86_64/libflutter.so` (sha256
  `bf332effcc407a658cb477b94417f83ce8df11b1676a06ee42ff754817b4197a`) contains
  the literal string `3.13.2 (stable) (Tue Aug 25 01:01:12 2026 -0700) on
  "android_x64"` at byte offset 2,035,994. REA reports `dart_version:null`
  because it does not parse that label; the version is nevertheless present in
  the carrier and readable offline.

Primary source for the rename: `dart-lang/sdk` commit
`d36adbacafee01d9852cf8e960cf2d8654d91e7e`, author time 2026-05-18 11:35:03
-0700, subject `[vm] Remove the VM isolate.`, message: *"The snapshot symbols are
renamed to kDartSnapshotData and kDartSnapshotText. … Aliases with the old names
are added to ease migration."* (fetched from
`https://dart.googlesource.com/sdk/+/d36adbacafee01d9852cf8e960cf2d8654d91e7e?format=JSON`;
the GitHub REST API was rate-limited, HTTP 403). The aliases are not exported in
this AOT ELF: `.dynstr` holds only the three new names.

[INFERENCE] The migration aliases exist at the C++ symbol level but are not
emitted into the AOT ELF dynamic table, so no table-selection change inside
6.5.0 can recover them. The R22 refusal was therefore correct behavior for that
carrier, not a corrupt or unreadable ELF.

## 4. A carrier generation that satisfies both contracts (observation; probes run before L1's stop order)

Two F-Droid *archive* builds of the same app, same ABI, older toolchain. The
archive index is `https://f-droid.org/archive/index-v1.jar`
(8,239,064 B, sha256 `c5427c3d043d66636217faf145f8d3c59512c2f72ce97605a1643766d13df5b4`,
`Last-Modified 2026-10-19T11:13:19Z`); both downloaded files match their index
`sha256` fields exactly.

| carrier | APK sha256 / bytes | libapp.so sha256 / bytes | Dart string in libflutter.so | `.dynstr` kDart names | data headers | `inspect-dart-aot` |
|---|---|---|---|---|---|---|
| `https://f-droid.org/archive/com.adilhanney.saber_1330203.apk` (1.33.2, x86_64) | `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618` / 41,263,437 | `f82ab4111807552af82ada747c5cccfe49474ecfcce49d5e0c3c701feeab38a8` / 17,367,984 | `3.11.4 (stable) (Tue Mar 24 01:02:20 2026 -0700) on "android_x64"` @ 2,007,997 | 4 legacy + `_kDartSnapshotBuildId` | kind 3 at `0x340` (16,842) and `0x4b40` (6,058,354), hash `78da37fed6bf1489361a312568249f3f` | **exit 0, libapp complete** |
| `https://f-droid.org/archive/com.adilhanney.saber_1340303.apk` (1.34.3, x86_64) | `ac68a976b1bfb8456bc062b9fd80a4a2098717a227d59ff771cda825b36b8b8d` / 42,571,868 | `205b3cae12ce0e2b2b39010d6cc5561bd86c8c26c58bbbfed67ea58ad379a502` / 16,843,664 | `3.12.2 (stable) (Tue Jun 9 01:11:39 2026 -0700) on "android_x64"` @ 2,027,597 | 4 legacy + `_kDartSnapshotBuildId` | kind 3 at `0x340` (15,477) and `0x45c0` (6,054,350), hash `ace654289f5abc240509fc941453ebc5` | **exit 0, libapp complete** |
| `https://f-droid.org/repo/com.adilhanney.saber_1360103.apk` (1.36.1, x86_64) | `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720` / 42,305,081 | `b54b19d243b6db78e27f9147b56dc0aa17ef6119fa905c2e2f7c72eb2f198feb` / 16,778,120 | `3.13.2 (stable) (Tue Aug 25 01:01:12 2026 -0700) on "android_x64"` @ 2,035,994 | 3 new names only | kind 2 at `0x2c0` (6,098,754), hash `0451907c2eaa8467e848c0067bfe8ed4` | exit 1, `unsupported_target` (R22) |

ABI is held constant (`x86_64` in all three), so the discriminator is the
snapshot-symbol set plus the data-header kind, not the CPU.

### Original run records (as captured; L1 to re-execute)

Primary probe, 1.33.2:

```
argv:    npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd23work/saber-1330203.apk --format json --full-output
wrapper: bash -lc 'exec env npm_config_yes=true npx -y rea-agents@6.5.0 inspect-dart-aot …'
cwd:     /tmp/kd23work
env:     npm_config_yes=true (only override); node v24.21.0, npx 11.19.0
exit:    0, stderr ""
stdout:  87,049 B; ok:true; meta {"command":"inspect-dart-aot","duration":"211ms"}
data:    evidence_id ev_dcdab9d08caaa21df0ccd3fe35455656e959d7ce5561d1117088f8c8224130fe
         operation inspect_dart_aot; confidence observed; authority shipped-artifact
         provider {id:"flutter", name:"Flutter build identification", version:null}
         subject sha256 a7b1f5c8…ea618, 41,263,437 B
         abi x86_64
         libapp {coverage:"complete", bytes 17,367,984, sha256 f82ab411…b38a8,
                 snapshot_hash 78da37fed6bf1489361a312568249f3f,
                 snapshot_hash_sources 2,
                 sections: _kDartVmSnapshotInstructions 7,208,960/89,936;
                           _kDartIsolateSnapshotInstructions 7,298,944/10,038,688;
                           _kDartVmSnapshotData 832/18,384 kind 3;
                           _kDartIsolateSnapshotData 19,264/7,153,168 kind 3}
         string_pool {coverage:"partial", package_uri_count_at_least 1000,
                      dart_uri_count_at_least 215, class_like_token_count_at_least 4000,
                      printable_run_count 50,666}
         coverage "partial"   (string-pool caps only; libapp itself complete)
```

Corroborating probe, 1.34.3:

```
same argv with /tmp/kd23work/saber-1340303.apk; exit 0; stdout 87,0xx B
evidence_id ev_04072bb4e179fdbd6cc8bf015da2d622236c6afbeb8059fd3d98ec7cfd0cc88c
meta {"command":"inspect-dart-aot","duration":"198ms"}
libapp coverage complete; snapshot_hash ace654289f5abc240509fc941453ebc5;
sources 2; four sections; pool partial (1000+/216+/4000+/50,419)
```

Same-carrier identification, 1.33.2:

```
npx -y rea-agents@6.5.0 identify-flutter-build /tmp/kd23work/saber-1330203.apk --format json --full-output
exit 0; evidence_id ev_5e9998847f41cfbb16fb4b50e7bef332e72799bb10bc9af934a20e8c0415f2c6
coverage "complete"; snapshot_hash_sources 2; snapshot_hash 78da37fed6bf1489361a312568249f3f;
libflutter build_id b178da35d9b305de1d9819c35f04bbaedaa244e0; dart_version null
```

This is the **same verb already counted at R22** (`identify-flutter-build`). It
must not be counted twice; its value here is that the legacy carrier gives a
complete-coverage witness (two hash sources) where the 1.36.1 carrier gave a
partial one (one source). The new verb candidate is `inspect-dart-aot`.

Verbatim provider limits on the successful run include:

> "Snapshot sections are located through the ELF dynamic symbol table; a payload
> without exported snapshot symbols is refused rather than guessed"
>
> "Snapshot hash sources are the headers at the start of the VM and isolate data
> symbols; complete decoding supports kind 3 (the Dart 2.14 FullAOT layout) …;
> other kind values remain observed with partial coverage"
>
> "String-pool entries are byte-pattern observations from the isolate data
> section, not deserialized cluster semantics"

## 5. Boundary (observation, then inference)

Observed on three carriers of one app: Dart 3.11.4 and 3.12.2 export the four
legacy names and use kind-3 data headers; Dart 3.13.2 exports only the three new
names and uses a kind-2 data header.

[INFERENCE] The first stable Dart line containing commit `d36adbacaf` (merged
2026-05-18) is 3.13; the two sides are observed, but no release-tag lookup was
performed, so "first stable = 3.13" is inferred from the commit date and the
3.13.2 carrier string, not read from a release manifest.

Predicate for any candidate APK (offline, no REA, no execution): extract
`lib/<abi>/libapp.so`, read `.dynsym`; ≥1 of the four legacy names means REA
will parse (all four + kind-3 data headers means complete). This was checked
against all three carriers above and reproduced the observed REA outcomes
(exit 0 / exit 0 / exit 3-as-refusal-equivalent). It is a gate reproduction, not
a substitute for the REA probe.

## 6. Proposed move (one bounded proposal)

**Substitute carrier generation, not tooling, for the second C1 verb.** Admit
`inspect-dart-aot` on a pre-Dart-3.13 Flutter carrier selected by the offline
dynsym predicate — primary candidate F-Droid archive Saber 1.33.2 x86_64
(`a7b1f5c8…ea618`, libapp `f82ab411…b38a8`) — and count it as the second held
T1 verb (k=2/6, incomplete=4), with three compulsory qualifiers in the same
claim text:

1. the verb is **carrier-generation conditional**; Dart ≥3.13 APKs (including
   the R22 carrier, `de4813f9…b720`) still refuse `unsupported_target`;
2. the R22 refusal remains historical witness (S055) and is not reinterpreted
   as an error;
3. libapp coverage is complete but string-pool coverage is partial and its
   counts are lower bounds.

Integration shape for L1 (not done by this seat): place the two envelopes and
`.run.json` receipts under `round-23/evidence/c1/`, add a `corpus/knowledge/`
entry whose first line cites the new source rows and whose body names the verb
and the exact envelope path, and mint source rows for (a) the Dart commit, (b)
the F-Droid archive index entry, (c) the probe receipts. Source ids S058-S060
are already taken by this round's signal seat; the next free id observed was
S061, but L1 must re-check at integration because seats are minting concurrently.
R22's counter semantics show that envelope data alone does not count: the
`ok:true` record with `meta.command`, `evidence_id`, `operation`, plus a
knowledge entry and a mined tier A/B row whose `used-by` names that entry are
all required.

**Affected axes**

- coverage: 1/6 → 2/6 with exact k=2 and four named incompletes; no mastery, no
  k=6 implication.
- depth: a complete libapp snapshot parse (four sections, kind 3, two agreeing
  hash sources) plus bounded string-pool lower bounds — a concrete static Dart
  surface that the R22 carrier could not produce at all.
- calibration: neutral only if qualifiers 1-3 ship with the claim. Without them
  the move overstates provider capability and harms calibration; this is a
  conditional, not an unconditional gain.
- contract/substrate: no production edits, no provider patch, no symbol
  renaming, no debugger/device, no dynamic ownership claim. R22 rows, LOG,
  SCORECARD and the census are untouched.

## 7. Risks and contradictions (kept explicit, not averaged)

1. **Carrier-conditional verb.** The same provider refuses the current-Flutter
   carrier. Both facts belong in one claim; reporting only the success would be
   the "copy erases parent refusal" falsifier.
2. **Double counting.** Two successful `inspect-dart-aot` runs (1.33.2 and
   1.34.3) are one verb. Count once.
3. **Cherry-pick optics.** The move selects an older version of the same app.
   The justification is a toolchain-layout predicate verified on both sides of
   the boundary, not app identity; the risk remains that a reviewer reads it as
   version shopping.
4. **Provenance strength.** `jarsigner -verify -strict` reports the F-Droid
   archive index as effectively unsigned ("signed with a weak algorithm that is
   now disabled"), so the index signature was **not** verified. The binding used
   is the index's `sha256` field matching the downloaded bytes over HTTPS, plus
   the signer certificate hash recorded in the index — not a cryptographic
   verification performed here.
5. **Ephemeral working files.** Artifacts lived under `/tmp/kd23work` (and the
   R22 carrier under `/tmp/kd22probe`); the reproducible reference is the URL
   plus SHA-256, not the path. A re-run at a different path can produce a
   different `evidence_id`.
6. **Coverage of the predicate.** One app family, one ABI (x86_64). The
   predicate is general and cheap, but no arm64 or second-app instance was
   verified, so the class claim "any pre-3.13 APK works" is [INFERENCE].
7. **Provider meaning of "complete".** Kind 3 is documented by the provider
   itself as the "Dart 2.14 FullAOT layout"; "complete" means the provider's own
   completeness rule, not verified snapshot semantics or source recovery.
8. **No authentication.** `evidence_id` is producer-side content hashing, not a
   signature; nothing here authenticates the artifacts or the provider.

## 8. Verification L1 should run (this seat did not perform these as final checks)

```
curl -sSL -o saber-1330203.apk https://f-droid.org/archive/com.adilhanney.saber_1330203.apk
sha256sum saber-1330203.apk        # must equal a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618
bash -lc 'npx -y rea-agents@6.5.0 inspect-dart-aot "$PWD/saber-1330203.apk" --format json --full-output'
# expect exit 0, meta.command inspect-dart-aot, abi x86_64,
# libapp.coverage complete, 4 sections, snapshot_hash 78da37fed6bf1489361a312568249f3f,
# snapshot_hash_sources 2, normalized_result.coverage partial
```

Then run `.ufo/waves/round-23/tools/count-c1.py` (not present when this seat
read the tree) after the knowledge entry and source rows exist; expect
`t1_exercised` to include both `identify-flutter-build` and `inspect-dart-aot`
and count 2, with the R22 refusal still present and uncounted. Confirm on the
1.36.1 carrier that `.dynstr` still contains only the three new names, so the
negative remains reproducible after integration.

## 9. Produced files, installs, unknowns

Produced by this seat (all author-side): this report, plus the nine files under
`.ufo/waves/round-23/evidence/c1/connect-dart-symbols/` written before L1's stop
order (disclosed in section 0, frozen, not removed). Their sha256, for L1's
inspection:

| file | sha256 |
|---|---|
| `inspect-dart-aot-saber-1330203.envelope.json` | `7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1` |
| `inspect-dart-aot-saber-1330203.run.json` | `4b263db8e6060a659f1cf81aab3df025b4014afecdd59258464d57351fe7938d` |
| `inspect-dart-aot-saber-1340303.envelope.json` | `22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d` |
| `inspect-dart-aot-saber-1340303.run.json` | `34f4ab462e0df49d6f9ff476e619f6bf2e01da750824771da5c8e1e8f78b3db3` |
| `identify-flutter-build-saber-1330203.envelope.json` | `3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626` |
| `identify-flutter-build-saber-1330203.run.json` | `9660b55cc8ed0046f67adace0e75636777c2696e5b111f5b918f9fe196b8cd60` |
| `carriers.json` | `652f05a626078250f617f7f4f3b5d64ca56d286b8654137757a5009ba983f2c6` |
| `fetch.json` | `6beac67b0f6361accc59729c969965b9b8f0f777f5beaca7dd1ed65b11566f2d` |
| `preflight_dart_carrier.py` | `08d0c4605c41f6b091d5b5d09172c5254eaf3bbffa8bf8bcf5f5c7b4b105514c` |
| `README.md` | not pinned (informational; re-hash if retained) |

This report's own sha256 cannot be embedded in itself; it is reported to Main
after it is written.

Installs: none. `rea-agents@6.5.0` was already in the npx cache
(`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`); `npx -y` resolved it without a
persistent install. No package manager, `uv`, or configuration change. A first
attempt with `env -i PATH=/usr/bin:/bin` failed `exit 127`
(`env: 'npx': No such file or directory`) because node is fnm-managed; it was
re-run through the login shell.

Observed / inferred / unknown:

- **Observed:** R22's retained refusal and its argv/exit; the 6.5.0 and 6.7.0
  symbol lists and dynsym-only reader; the three carriers' `.dynsym`,
  `.dynstr`, data-header kinds and embedded Dart version strings; both
  successful `inspect-dart-aot` runs and the same-carrier identification; the
  F-Droid archive index entries and the sha256 match of both downloads; the
  weak-signature jarsigner result.
- **Inferred:** 3.13 is the first stable Dart release containing the rename;
  the C++ migration aliases are simply not emitted into AOT ELF `.dynsym`; the
  predicate generalizes to other pre-3.13 APKs.
- **Unknown:** the exact Flutter framework version of each carrier (only the
  Dart SDK label in `libflutter.so` was read); whether any current-format
  carrier exports the legacy names (none observed); arm64 or second-app
  behaviour; whether a future REA release accepts the new layout; the
  authenticity of the F-Droid archive index signature.
