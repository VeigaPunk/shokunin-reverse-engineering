# CoverageMap — R23-C1 corpus mentions: offline signals, Dart, and the precise row to append

Seat `KaidokuR23.CoverageMap` (scout, read-only). Observation window 2026-10-21
~14:38–14:56 UTC at wave rev `a3c92eb6bc70984e90ae5b895412de978840b2c5`
(frozen claim baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`).

This seat ran no REA probe, device, debugger, Frida, process attach or carrier
execution. Peer-produced envelopes and receipts were read as untrusted target
content and are cited, not re-derived. Everything below is author-side mapping,
not outside verification and not a held-capability claim.

## Findings

### F1. Claim counter, measured now

Exact command (read-only; the tool sets `tempfile.tempdir` to
`.ufo/waves/round-23/runtime`, inside the wave):

```
python3 -I -B .ufo/waves/round-23/tools/count-c1.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev a3c92eb6bc70984e90ae5b895412de978840b2c5
```

Run 1 and run 2 (after the owner updated the tool) both returned `exit=1` with
identical claim fields: `finding=c1_incomplete`,
`t1_exercised=[identify-flutter-build]`, `t1_exercised_count=1`, `t1_total=6`,
`catalog_mentioned_count=135`, `catalog_total=153`, `catalog_zero_count=18`.
`new` is empty for all six verbs; `historical` holds only the two R22
`identify-flutter-build` envelopes (`ev_6a84742a…`, `ev_3458b996…`).
Raw outputs: `.ufo/waves/round-23/w1/.tmp-counter/r23-out.json` (run 1) and
`…/r23-out-final.json` (run 2).

Concurrent-edit observation: at first read the tool's
`SELFTEST_MANIFEST_SHA256` was the literal `'UNSET'`; at second read the same
file carried
`ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24` at line 25.
The owner was editing the counter while this seat mapped. This seat did not run
`--selftest` and makes no claim about its status.

**Observed eligibility chain** (read from
`.ufo/waves/round-23/tools/count-c1.py:1-133`, not inferred): the tool scans both
`ROOTS` (`.ufo/waves/round-22/evidence/c1/`,
`.ufo/waves/round-23/evidence/c1/`, subdirectories included) and reads
`corpus/SOURCES.md` and `corpus/knowledge/*` with `git show <rev>:<path>`.
Therefore:

1. A new witness exists only at the tested revision. Worktree-only evidence,
   knowledge or rows do not count until committed to `--rev`.
2. The knowledge entry's **first line** must start with `source:` and contain an
   `S###` id.
3. That id must resolve to a row with `len(split("|"))==13`, id `>= 58`,
   tier `A` or `B`, status `mined`, opened `2026-10-21`, and the row's `used-by`
   cell (comma-split, literal element match) must contain the **exact**
   knowledge path — no backticks.
4. The knowledge text must also cite the exact `ROOTS[1]` evidence path, contain
   the envelope's `ev_` id, and contain the exact verb token.
5. Legacy binding adds at most five candidate witnesses per verb/root
   (`count-c1.py` docstring); beyond that the count can undercount, never
   overcount. Source relevance and domain admission stay manual.

### F2. Round-23 evidence that already exists (peer-produced)

Offline signal family, `.ufo/waves/round-23/evidence/c1/`:

| file (bytes) | operation | evidence id | subject sha256 | observed window |
|---|---|---|---|---|
| `inventory.envelope.json` (9391) | `inspect_signal_decoders` | `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` | adapter `sigrok-cli.sh` `50fe4359…470902` | 110 decoders, `has_more:false` |
| `uart-help.envelope.json` (8504) | `inspect_signal_decoders` (`--decoder uart`) | `ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a` | same adapter | 81 help lines, `has_more:false` |
| `decode-official-uart.envelope.json` (362104) | `decode_signal_recording` | `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` | `hello_world_8n1_9600.sr` `01b72610…f900b61` | 12,885 lines, `has_more:false` |
| `decode-uart-hi.envelope.json` (4821) | `decode_signal_recording` | `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` | `uart-hi.bin` `4a2e729f…e861727` | 2 lines |
| `decode-invalid-decoder.envelope.json` (991) | `decode_signal_recording` | none (`ok:false`) | `uart-hi.bin` | `execution_failure`, exit1 |
| `official-download.json` (329) | fetch receipt | n/a | sha256 `01b72610…f900b61`, 58381 bytes | HTTP 200 |

Static Dart family, `.ufo/waves/round-23/evidence/c1/connect-dart-symbols/`:

| file | operation | evidence id | subject | observed result |
|---|---|---|---|---|
| `inspect-dart-aot-saber-1330203.envelope.json` | `inspect_dart_aot` | `ev_dcdab9d08caaa21df0ccd3fe35455656e959d7ce5561d1117088f8c8224130fe` | Saber 1.33.2 APK sha256 `a7b1f5c8…3ea618`, 41263437 bytes | `ok:true`, libapp `coverage:complete`, 4 sections, snapshot hash `78da37fed6bf1489361a312568249f3f`, 2 hash sources, `string_pool` partial |
| `inspect-dart-aot-saber-1340303.envelope.json` | `inspect_dart_aot` | `ev_04072bb4e179fdbd6cc8bf015da2d622236c6afbeb8059fd3d98ec7cfd0cc88c` | Saber 1.34.3 APK sha256 `ac68a976…b6b8b8d`, 42571868 bytes | `ok:true`, libapp `coverage:complete`, 4 sections, snapshot hash `ace654289f5abc240509fc941453ebc5`, 2 hash sources, `string_pool` partial |
| `identify-flutter-build-saber-1330203.envelope.json` | `identify_flutter_build` | `ev_5e9998847f41cfbb16fb4b50e7bef332e72799bb10bc9af934a20e8c0415f2c6` | same 1.33.2 APK | `ok:true`, `flutter_detected:true`, one x86_64 ABI, `coverage:complete`, engine `dart_version:null` |
| `carriers.json`, `fetch.json` | carrier/fetch receipts | n/a | F-Droid archive index + two APKs | versions 1.33.2 / 1.34.3; both hashes match index entries |

Exact run argv (from the adjacent `.run.json` files; signal runs add
`REA_SIGROK_COMMAND=<lane>/tools/sigrok-cli.sh`):

```
npx -y rea-agents@6.5.0 inspect-signal-decoders --all --format json --full-output                 # exit0
npx -y rea-agents@6.5.0 inspect-signal-decoders --decoder uart --all --format json --full-output   # exit0
npx -y rea-agents@6.5.0 decode-signal-recording .../hello_world_8n1_9600.sr \
  --decoders uart:rx=TX:baudrate=9600 --annotations uart=rx-data --all_lines --format json --full-output   # exit0
npx -y rea-agents@6.5.0 decode-signal-recording .../uart-hi.bin \
  --decoders uart:rx=0:baudrate=9600 --input_format binary:numchannels=1:samplerate=960000 \
  --annotations uart=rx-data --all_lines --format json --full-output                                       # exit0
npx -y rea-agents@6.5.0 decode-signal-recording .../uart-hi.bin \
  --decoders round23_nonexistent_decoder --input_format binary:numchannels=1:samplerate=960000 \
  --all_lines --format json --full-output                                                                   # exit1, ok:false
npx -y rea-agents@6.5.0 identify-flutter-build /tmp/kd23work/saber-1330203.apk --format json --full-output   # exit0
npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd23work/saber-1330203.apk --format json --full-output         # exit0
npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd23work/saber-1340303.apk --format json --full-output         # exit0
```

Interpretation separated by grade:

- **Observation (signal):** the official sample decodes to `BA BD C9 B1 91 85
  0D 0A` then `Hello World!` ASCII at 9600 8N1; the synthetic 2500-byte
  one-channel binary at 960000 samples/s decodes to `0x48,0x69` ("Hi"). Both
  envelopes are `confidence:observed`, `authority:shipped-artifact`,
  `hardware_acquisition:not-performed`, limits `input_bytes 33554432`,
  `output_bytes 4194304`, `command_timeout_ms 30000`, `cpu_seconds 30`.
- **Observation (signal):** successful decode runs still carry
  `PYTHONHOME`/`<prefix>` diagnostics text. Diagnostics are not a failure
  signal by themselves.
- **Observation (Dart):** both AOT envelopes locate all four snapshot sections
  and report libapp `coverage:complete`; the two instruction sections have
  `magic_valid:false` while the two data sections have `magic_valid:true`,
  `kind:3` and non-null `header_length`. `string_pool.coverage` is `partial`
  (package URIs only), and the engine record reports `dart_version:null`.
- **Peer receipt (Dart, not REA):** `carriers.json` extracts embedded
  `libflutter` version strings `3.11.4 (stable) … android_x64` (1.33.2) and
  `3.12.2 (stable)` (1.34.3), and records the R22 1.36.1 carrier as Dart 3.13.2
  with the new `_kDartSnapshotText`/`_kDartSnapshotData` symbol set. Those
  version strings are lane extraction, not provider output.
- **Peer inference (Dart):** the R22 `unsupported_target` refusal and these
  positives are consistent with a symbol-set/layout change at Dart ≥ 3.13. This
  is the peer's labelled inference; the envelopes themselves only show the
  symbol set actually present.
- **Unknown:** decoder correctness, protocol semantics beyond the decoded
  bytes, sample-clock accuracy of the synthetic carrier, Dart source recovery,
  SDK-version lookup by REA, and any runtime/device path.
- **Must not count:** `decode-invalid-decoder` is a deliberate typed refusal
  (`ok:false`, `execution_failure`, exit1), and the R22 Dart refusal stays a
  refusal. Counting either would trigger the "refusal counted" falsifier.

### F3. Offline-signal corpus map, before round 23

Census command (one pattern at a time; `rc=1` means grep found nothing):

```
grep -rniE -- "<pattern>" corpus/
```

| pattern | files | matches | grep rc |
|---|---|---|---|
| `sigrok` | 0 | 0 | 1 |
| `sigrok-cli` | 0 | 0 | 1 |
| `inspect-signal-decoders` | 0 | 0 | 1 |
| `decode-signal-recording` | 0 | 0 | 1 |
| `signal[-_ ]?decoder` | 0 | 0 | 1 |
| `protocol decoder` | 0 | 0 | 1 |
| `pulseview` | 0 | 0 | 1 |
| `srzip` | 0 | 0 | 1 |
| `logic[- ]level` | 0 | 0 | 1 |
| `sample rate\|samplerate` | 0 | 0 | 1 |
| `uart` | 0 | 0 | 1 |
| `decoder` | 9 | 19 | 0 |
| `\bsignal\b` | 28 | 115 | 0 |
| `signal-desktop\|libsignal` | 10 | 71 | 0 |

Restricted check over `corpus/knowledge/ corpus/SOURCES.md corpus/README.md
corpus/QUALITY.md` for `sigrok|signal[-_ ]decoder|decode-signal|inspect-signal|
logic analy|saleae|\.sr\b|vcd` → no matches, `rc=1`.

- **Observation:** before round 23 the corpus had zero knowledge of sigrok,
  protocol decoders, logic recordings, UART or samplerate. The 115 `signal`
  matches are the Signal Desktop messenger (`signal-desktop|libsignal`: 71
  matches in 10 files) and Unix signals (`siginfo`, crash probes), not logic
  signals. The 19 `decoder` matches are unrelated uses (JSON/base64/parser
  contexts), not signal decoders. `2026-10-13-r3-typora-signal.md`,
  `…-r4-05-signal-asar.md` and `…-r4-14-libsignal.md` are Signal Desktop
  artifacts and are **not** offline-signal knowledge.
- **Adjacent transferable knowledge (observed):** `appimage` appears 59 times
  across the corpus; `2026-10-13-r3-appimage.md` and
  `2026-10-13-r4-15-appimage-inner.md` record the `--appimage-extract` route
  this wave used for the sigrok-cli 0.7.2 delivery. That is extraction
  technique, not signal semantics.
- **Unknown:** the census bounds only the listed spellings; it is not proof that
  no synonym exists.

### F4. Dart corpus map

Five corpus files contain `dart` (26 matches) / `flutter` (36 matches):

| file:line | what it contributes |
|---|---|
| `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md:9,11` | Godot APK parsed `flutter_detected:false`, `abis:[]`, `coverage:complete` |
| `…-flutter-static-boundary.md:15` | explicit unknown: positive Flutter, Dart snapshot parsing, source recovery not established |
| `…-flutter-static-boundary.md:24` | rule: static identity does not imply runtime behavior or recovered Dart source |
| `…-flutter-static-boundary.md:40,55-56` | cross-reference to the Saber positive + Dart refusal |
| `corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:1,5` | Saber identify positive is partial; `inspect-dart-aot` refuses |
| `…-flutter-positive-dart-refusal.md:15` | `inspect-dart-aot` exit1 `unsupported_target`; four legacy snapshot symbols absent |
| `…-flutter-positive-dart-refusal.md:19,21,23` | acceptance conditions differ; no version mapping/source recovery; mention is not exercised success |
| `corpus/SOURCES.md:57-61,63` | S051–S055 and S057: Flutter build modes, Android ABI guide ×2, Godot negative, Saber probes, original Godot envelope |
| `corpus/SOURCES.md:62` | S056 is debugger-alias only; **not** Dart evidence |
| `corpus/README.md:70-71` | two coverage rows: static Flutter boundary; partial positive + Dart refusal |
| `corpus/lessons/round-22.md:11,13,15,134,139-144,158-160` | lesson rows and the "reject as held: Saber refusal" verdict |

Held/mention state before this wave: `identify-flutter-build` held historically
(two R22 envelopes); `inspect-dart-aot` mention-only (one knowledge entry, S055,
counter empty). **Uncovered prior ground:** no positive symbol-walk AOT parse,
no Dart SDK-version mapping, no source recovery, no snapshot-completeness
result. Round 23 now has two positive AOT envelopes (F2), so the prior absence
is superseded by evidence — but only static parsing: no source recovery and no
version lookup by REA. The R22 refusal must be preserved (falsifier: "copy
erases parent refusal"); its carrier (1.36.1) is a different symbol layout, not
a retry of the same input.

### F5. Per-verb uncovered ground

| T1 verb | prior corpus mention | round-23 evidence now | counter | uncovered / caveat |
|---|---|---|---|---|
| `identify-flutter-build` | 2 knowledge files, 3 S rows (S053/S055/S057) | new 1.33.2 envelope `ev_5e99…` | exercised (historical, 2 envelopes) | same verb; a third envelope does not add k |
| `inspect-dart-aot` | 1 knowledge file (refusal), 1 S row (S055) | 2 positive envelopes `ev_dcda…`, `ev_0407…` | not yet exercised (no knowledge/S row) | static parse only; `string_pool` partial; engine `dart_version:null`; no source recovery |
| `debug-with-gdb` | 0 knowledge, S056 alias row | none | not exercised | corpus `gdb` mentions are host coredump paths (`crash-evidence.md:49-51`), not this verb; no CLI envelope |
| `debug-with-rizin` | 0 knowledge, S056 alias row | none | not exercised | `execute-rizin-command` knowledge (`r20-rizin-command-observation`) does not bind the debug verb; no CLI envelope |
| `inspect-signal-decoders` | **zero** | 2 successful envelopes (`ev_940c…`, `ev_4be1…`) | not yet exercised | success observed; decoder semantics not validated |
| `decode-signal-recording` | **zero** | 2 successful envelopes + 1 refusal | not yet exercised | success observed; refusal must stay uncounted |

**Projection, not measurement:** four verbs now have successful original
envelopes (`identify-flutter-build`, `inspect-dart-aot`,
`inspect-signal-decoders`, `decode-signal-recording`). If L1 commits conforming
knowledge plus S058/S060 rows to the tested revision, the counter can reach
`k=4/6`; the two dynamic verbs remain 0 under this wave's boundary, so 4/6 is
the ceiling here. Today's measured value is `k=1/6`. Nothing is preclaimed.

### F6. Precise rows to append

Next free id, verified:

```
grep -oE '^\| S[0-9]{3} ' corpus/SOURCES.md | sort | uniq -d      # empty
grep -oE '^\| S[0-9]{3} ' corpus/SOURCES.md | grep -oE '[0-9]{3}' | sort -n | tail -1   # 057
```

**Insertion point:** `corpus/SOURCES.md` line 64 — immediately after the S057
row (line 63) and before the blank line preceding `## Paths` (line 65). Each row
must have exactly 11 cells between 12 pipes (13 split pieces) and no literal `|`
inside a cell. The `used-by` cell must hold plain comma-separated repo-relative
paths **without backticks**: the round-23 counter compares `cell.split(",")`
elements literally against the knowledge path, so a backticked path silently
fails eligibility.

Required signal row (values copied from the envelopes above):

```
| S058 | Round-23 C1 offline sigrok evidence family — `.ufo/waves/round-23/evidence/c1/inventory.envelope.json`, `uart-help.envelope.json`, `decode-official-uart.envelope.json`, `decode-uart-hi.envelope.json`; producing argv and `REA_SIGROK_COMMAND` override in the adjacent `.run.json` files; pinned input receipt `official-download.json` | own-work | A | REA6.5.0 `inspect-signal-decoders` catalog and decoder-help pages plus two `decode-signal-recording` runs through the lane sigrok adapter; not decoder correctness, protocol semantics, hardware discovery or device behavior | ok:true, meta.command `inspect-signal-decoders` with Evidence `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` (110 decoders) and `ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a` (`--decoder uart`, 81 help lines); ok:true, meta.command `decode-signal-recording` with Evidence `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` (`hello_world_8n1_9600.sr` sha256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`, uart 9600, 12885 lines) and `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` (`uart-hi.bin` sha256 `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`, binary 1ch 960000, 2 lines); adapter subject SHA-256 `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902`; opened 2026-10-21 | Offline decoder inventory, per-decoder help and recording decode are reachable without a device; returned annotations are the decoder's interpretation of caller-selected settings. | mined | 2026-10-21 | on-release | .ufo/waves/round-23/w1/CoverageMap.md, corpus/knowledge/2026-10-21-r23-offline-signal-decoders.md |
```

Required Dart row (values copied from the nested envelopes and carrier receipt):

```
| S060 | Round-23 C1 static Dart AOT family — `.ufo/waves/round-23/evidence/c1/connect-dart-symbols/inspect-dart-aot-saber-1330203.envelope.json`, `inspect-dart-aot-saber-1340303.envelope.json`, `identify-flutter-build-saber-1330203.envelope.json`; carrier receipt `carriers.json` and fetch receipt `fetch.json`; producing argv in the adjacent `.run.json` files | own-work | A | REA6.5.0 `inspect-dart-aot` and `identify-flutter-build` static parsing of two pinned x86_64 Saber APKs; no APK execution, no Dart source recovery, no SDK-version lookup by REA and no runtime behavior | ok:true, meta.command `inspect-dart-aot` Evidence `ev_dcdab9d08caaa21df0ccd3fe35455656e959d7ce5561d1117088f8c8224130fe` (APK `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`, libapp sha256 `f82ab4111807552af82ada747c5cccfe49474ecfcce49d5e0c3c701feeab38a8`, 17367984 bytes, 4 sections, libapp coverage complete, snapshot hash `78da37fed6bf1489361a312568249f3f`, string_pool partial) and `ev_04072bb4e179fdbd6cc8bf015da2d622236c6afbeb8059fd3d98ec7cfd0cc88c` (APK `ac68a976b1bfb8456bc062b9fd80a4a2098717a227d59ff771cda825b36b8b8d`, libapp sha256 `205b3cae12ce0e2b2b39010d6cc5561bd86c8c26c58bbbfed67ea58ad379a502`, 16843664 bytes, coverage complete, snapshot hash `ace654289f5abc240509fc941453ebc5`); ok:true, meta.command `identify-flutter-build` Evidence `ev_5e9998847f41cfbb16fb4b50e7bef332e72799bb10bc9af934a20e8c0415f2c6` (flutter_detected true, one x86_64 ABI, snapshot_hash_sources 2, dart_version null); opened 2026-10-21 | A symbol-table-walked AOT snapshot is distinguishable from the R22 Dart 3.13 refusal; the snapshot hash is not an SDK lookup and string-pool coverage is partial. | mined | 2026-10-21 | on-release | .ufo/waves/round-23/w1/CoverageMap.md, corpus/knowledge/2026-10-21-r23-dart-static-aot.md |
```

Recommended companion tool row (append only if the signal knowledge entry makes
a version claim; otherwise fold the digest into S058's anchor):

```
| S059 | sigrok-cli 0.7.2 x86_64 AppImage — `/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage`; `--version` banner `.ufo/waves/round-23/sigrok-version-attempt1.json`; `--appimage-extract` receipt `.ufo/waves/round-23/sigrok-extraction.json` | tool | A | Version and bundled-library identity of one digest-pinned AppImage; no publisher authentication and no decoder behavior | SHA-256 `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`, 49558848 bytes; `--version` exit0 reports sigrok-cli 0.7.2, libsigrok 0.5.2, libsigrokdecode 0.5.3, Python 3.5.2; `--appimage-extract` exit0 | Pin the producer build and library set before treating a decoder listing as evidence. | mined | 2026-10-21 | on-release | .ufo/waves/round-23/w1/CoverageMap.md, corpus/knowledge/2026-10-21-r23-offline-signal-decoders.md |
```

Knowledge frontmatter that makes S058 eligible (first line matters; S060 is the
same shape with the Dart paths):

```
source: S058 `.ufo/waves/round-23/evidence/c1/inventory.envelope.json`, `uart-help.envelope.json`, `decode-official-uart.envelope.json`, `decode-uart-hi.envelope.json`; S059 `/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage`
verified-at: 2026-10-21, round23; rea-agents@6.5.0 with REA_SIGROK_COMMAND=<lane>/tools/sigrok-cli.sh
recheck: rerun the exact argv in the retained `.run.json` files after re-extracting the digest-pinned AppImage; compare evidence fields, not path-sensitive ids
```

The knowledge body must additionally contain the exact verb token(s), each
cited evidence path verbatim (including the `connect-dart-symbols/` segment for
Dart), and each `ev_` id; otherwise the round-23 counter's `current` list stays
empty even with a valid S row. A refusal envelope must not be presented as a
witness; placeholder ids are forbidden — a fabricated `ev_` value both fails
binding and violates the evidence contract.

### F7. Caveats observed while mapping

- `decode-invalid-decoder` is the only `ok:false` file in `evidence/c1`; its
  `execution_failure` is a deliberate negative probe. Any row or knowledge text
  that lists it beside the successes must mark it uncounted.
- The R22 Dart refusal remains `ok:false`; the round-23 positives are different
  carriers with a different symbol set, not a retry of the refused input.
- The counter file changed while this seat read it (selftest constant). Treat
  its current values as owner-controlled; rerun the exact command for a fresh
  measurement rather than trusting this snapshot.
- Success envelopes carry `PYTHONHOME` diagnostics text; treating it as failure
  would misread a successful decode.
- `inspect-signal-decoders` and `decode-signal-recording` were **zero-mention**
  in the corpus before this wave; their first corpus statement will be the new
  knowledge entry, so there is no prior row to reuse and no inherited claim.
- `carriers.json` states the F-Droid index jar's signature is weak/disabled and
  was **not** cryptographically verified; provenance rests on HTTPS, the index
  sha256 and the index-entry hash match. The row scope must not claim carrier
  authentication.
- The engine record reports `dart_version:null`; Dart version strings live in
  the lane's `carriers.json` extraction from `libflutter`, not in REA output.

## Produced files

| path | sha256 |
|---|---|
| `.ufo/waves/round-23/w1/CoverageMap.md` (this report) | body hash on the last line, verifiable with `sed '$d' <file> \| sha256sum` |
| `.ufo/waves/round-23/w1/.tmp-counter/r23-out.json` (run 1) | `e843b4b474521adffa4921ddd4be94f110e885bf9dc7bf458a59ac4742408b71` |
| `.ufo/waves/round-23/w1/.tmp-counter/r23-out-final.json` (run 2) | `832167363438af7447422e2c33627a52808adbb6ad5ef6de330d7be6b7487399` |
| `.ufo/waves/round-23/w1/.tmp-counter/r23-err.txt` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/waves/round-23/w1/.tmp-counter/out.json` (R22-tool baseline run) | `a6e8a66f7eefbd3ff056cdce2311df3ebc76cf1502a68ff0effea53606472923` |

Peer-produced evidence and receipts cited above were not modified by this seat.

## Installs

None. No package, tool, AppImage or config change was made by this seat. The
sigrok-cli AppImage already existed at `/home/vgpnk/.local/opt` (mtime
2026-10-21 08:39, sha256 `49d2f597…f50b614`); this seat only read its digest and
the peer receipts. No download was performed here.

## Open risks

1. **Commit boundary:** the counter reads `git show <rev>:` — evidence,
   knowledge and S rows must all be committed to the tested revision, or `k`
   stays 1 regardless of the worktree state.
2. **Ceiling 4/6 under this boundary:** `debug-with-gdb` and `debug-with-rizin`
   have no envelope and no permitted dynamic execution this wave; no signal or
   Dart work can lift them.
3. **Refusal-counting falsifier:** `decode-invalid-decoder` and the R22 Dart
   refusal must both stay visibly uncounted; a summary that lists them with the
   successes would trigger the claim's falsifier.
4. **Silent eligibility failure:** a knowledge filename differing by one
   character from the row's used-by cell, a first line not starting with
   `source:`, or a missing nested `connect-dart-symbols/` segment drops the
   entry with no error — `k` simply stays 1.
5. **Decoder semantics:** help lines and annotations are producer text; the
   corpus must not promote them to a validated parameter schema or verified
   protocol semantics.
6. **Dart scope:** libapp coverage is complete but `string_pool` is partial and
   `dart_version` is null in REA output; do not claim source recovery, full
   snapshot parsing or SDK identification.
7. **Carrier provenance:** F-Droid jar signature verification was explicitly
   not established by the peer receipt; only digest/index-hash matching is
   evidenced.
8. **Reproducibility of S059:** the AppImage path is host-local; only the
   digest, size and version banner travel. The URL in `setup-sigrok.py` is the
   peer's docstring, not a fetch this seat performed or verified.
9. **Author-side only:** these rows are proposals. This seat did not edit
   `corpus/SOURCES.md`, `corpus/knowledge/`, production lane files, or any
   sibling report; L1 owns integration and the final count.
report-body-sha256 (every preceding line, before this trailer): 5bc074f0d5d5a6d05f8d5a9df0f898125ebcbbadd78157b8fb8f2e4d0371c628
