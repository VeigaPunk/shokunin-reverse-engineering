# RegistryDescriptors: R23-C1 signal/Dart descriptor and final-producer registry rows

Seat: KaidokuR23.RegistryDescriptors (leaf reviewer, source review only, author-side).
Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`. Producer source V: `6615aeae642aec36959180e7ea940b2794c7f1cb`.
Not an independent outside admission.

## Method and axes

Axes: (1) probe semantics, (2) exact field recomputation, (3) actual write scope, (4) authority wording.

- Candidate bytes only. `git archive 2838351… -- .ufo/waves/round-23 LOG.md SCORECARD.md corpus/lessons/round-23.md corpus/SOURCES.md` was extracted into `runtime/RegistryDescriptors/cand/` (483 files; no `.gitattributes`, so no filters). Four extracted blobs were spot-checked with `git hash-object` against `git rev-parse <rev>:<path>`, all equal. Knowledge entries were read with `git show`.
- Recomputation used `sha256sum`, `cmp`, `jq`, `git`, and one `python3` hex-decode over committed bytes.
- Not executed: `describe-signals.py`, `describe-dart.py`, `verify.py`, `count-c1.py`, `sources-census.sh`, or any REA/sigrok command. No Run* seat command was run.
- One moving-worktree read is labelled as such (F2). Nothing was written outside `w2/` and `runtime/RegistryDescriptors/`.

## Summary

- **Recomputation.** All five signal rows reproduce field-for-field from committed bytes once describe-signals' own restriction is applied (`describe-signals.py:57` limits argv-target and carrier checks to `decode-*` records). The Dart row reproduces every field I rebuilt. Not rebuilt: `rev`, the constant `limit` text, and the full `subject` object (I rebuilt its `local_path` and digest). Envelope digests, stdout byte equality, carrier digests, argv/meta cross-checks, the connector README table (9/9), source pins (6/6), and the producer digest all match.
- **Authority wording.** No inflation found in S058–S061, the LOG/SCORECARD addenda, or the lessons addendum against the claim's `not_claimed` list (authentication, dynamic ownership, outside admission, provider availability). The S060/S061 limits text is honest.
- **Concrete candidate findings.** F1 is probe semantics: the literal boolean is structurally always false. F2 is medium: the census row is not revision-bound. F7 is medium: one knowledge sentence contradicts the held set. The rest are low, latent, or disclosed.

## Findings

Labels: **Observed** (read or recomputed here), **Inferred**, **Unknown**. Paths are relative to the repo root unless noted.

### F1. Medium. `contains_literal_Hello_World` tests the rendering, not the payload (probe semantics, false negative by construction)

- **Observed.** `tools/describe-signals.py:55`: `'contains_literal_Hello_World': 'Hello World!' in annotations`.
- **Observed.** `evidence/c1/decode-official-uart.envelope.json`, `normalized_result.annotations_text`, is 12,885 lines of the form `<start>-<end> uart-1: <HH>`. Example lines: `108-628 uart-1: BA`, `5512-6032 uart-1: 48`.
- **Observed.** `python3` over that text: distinct characters are `" -0123456789:ABCDFartu"` plus newline. `H` does not occur, so the literal `Hello World!` cannot occur in this rendering.
- **Observed.** Decoding the 12,885 hex tokens gives a byte stream with `b"Hello World!"` at offset 8. The first 16 bytes are `ba bd c9 b1 91 85 0d 0a 48 65 6c 6c 6f 20 57 6f`.
- **Observed.** `verify/initial/signal-records.json` (stdout string, official row): `contains_literal_Hello_World: false`. `predictions.json:13`: `"expected_text": "Hello World!"`.
- **Observed.** `corpus/lessons/round-23.md:98-99` says the literal prediction is "explicitly false". `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:77-82` states the byte-level position (first match at sample 5512) and that the literal-string prediction is not met. The knowledge text is accurate.
- **Inferred.** The boolean measures the hex rendering, not the payload. Its `false` is guaranteed by the format and must not be cited as a payload negative. Authority impact is low because the prose is bounded. Probe impact is medium.
- **Fix.** Replace it with a decoded-byte predicate (hex tokens to bytes, then substring), or rename it `literal_text_in_annotations` and stop citing it as a payload result.

### F2. Medium. The source-census row is not revision-bound, and its predicate is exit-only

- **Observed.** `verify.py:110` runs `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`. There is no clone and no `--rev`. `verify.py:38` defaults the predicate to `lambda out: True`, and `verify.py:45` makes `passed` depend only on the exit code.
- **Observed.** `verify/initial/source-census.json` stdout ends with `kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. That is the lane worktree path, not `runtime/verify-*/snapshot`. The record still carries `source_rev: 6615aea…`, which `verify.py:48` stamps from `rev`.
- **Observed.** `corpus/SOURCES.md` sha256 at V and at the candidate is `736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525`. The current worktree copy is `304acb2b3543897910b142db3452ef5c11910c11bd77f15d73fc056f4a85788b`. That is a moving-tree observation, not a candidate read.
- **Observed.** `LOG.md:2655` says "census exits0". `SCORECARD.md:2837` says "census exit0 with carried W04 warnings". `corpus/lessons/round-23.md:95` says "Initial and post-source census both exit0". The claims `no_harm` list also contains "source census exit0".
- **Inferred.** The census outcome describes the worktree at run time, not V or the candidate. The `source_rev` stamp overstates binding, so the 12/12 summary mixes rev-bound and worktree-bound conditions.
- **Write scope of this child: fine.** The header of `scripts/sources-census.sh` (line 7) says it "writes only stdout or --out". I did not read beyond the header.
- **Fix.** Run the census against a snapshot parent that contains `kaidoku-shokunin` at V, or relabel the record as a worktree observation and drop "rev-bound" wording.

### F3. Low. The signal-records predicate gates only count and byte equality

- **Observed.** `verify.py:71`: `len(records)==5 and all(stdout_byte_equal)`.
- **Observed.** `describe-signals.py` computes `synthetic_exact` (:56), `subject_digest_matches_carrier` (:61), `argv_target_matches_subject` (:62), and `argv_command_matches_meta` (:64). It also emits `ok`, `exit`, and `diagnostics`. None of these is gated.
- **Observed.** `verify.py:72` (Dart) gates `argv_target_matches_subject` and `subject_digest_matches_fetch`. It does not gate `command_matches`, `ok`, or stderr. The signal predicate gates neither argv target nor stderr. Both recorded stderr values are `""`.
- **Observed (recomputed).** Every recorded signal field agrees with my recomputation (see the table). No discrepancy field is currently false.
- **Inferred.** `signal-records passed: true` certifies count and byte equality only. It is a latent false-pass. This is the open part of W1 `ReviewOriginalRuns.md:9-11` (see the stale section).

### F4. Low-medium. Inventory coverage: the failed module and diagnostics are free text, not fields

- **Observed.** `evidence/c1/inventory.envelope.json` diagnostics include `srd: SyntaxError: Failed to load decoder signature: import by name failed: invalid syntax (pd.py, line 138)` and a traceback. `output_window` is `{examined:110, matching:110, returned:110, has_more:false}`. The decoders list has no `signature` id (recomputed: `has_signature=false`).
- **Observed.** `describe-signals.py:50` sets `decoder_count = len(decoders)` = 110. The diagnostics stay as text. No gate exists (`verify.py:71`).
- **Observed (disclosed in prose).** `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:17-26` discloses the exclusion and says an exhausted window "does not mean every installed module loaded". `corpus/lessons/round-23.md:18` admits "returned loaded-decoder window … signature-module failure remains in diagnostics". `:49` names the drift class. `SOURCES.md:66` says "installed decoder catalog".
- **Inferred.** The prose is correct. The descriptor has no structured failed-module field, so `decoder_count` can be read as installed-catalog size.
- **Unknown.** The true installed decoder count in the bundle. `w1/CriticVacuity.md:64` reports 112 `__init__.py` dirs. I did not recompute that.

### F5. Low. The uart-help row shows `decoder_count: 0` and drops the 81 help lines

- **Observed.** `verify/initial/signal-records.json`, uart-help row: `decoder_count: 0`, `annotation_line_count: 0`.
- **Observed.** `evidence/c1/uart-help.envelope.json` normalized_result carries `help_lines` with 81 entries and no `decoders`. `describe-signals.py:50` counts only `decoders`.
- **Inferred.** A reader can misread the zero as "no decoders". Add a `help_line_count` field.

### F6. Low (latent). The Dart `libapp.coverage: complete` label covers two instruction sections with no kind or magic

- **Observed.** `evidence/c1/inspect-dart-legacy-saber.envelope.json`, `libapp.sections`:
  - `_kDartVmSnapshotInstructions` (offset 7208960, size 89936) and `_kDartIsolateSnapshotInstructions` (7298944, 10038688) have `magic_valid:false`, `kind:null`, `header_length:null`.
  - The two Data sections have `magic_valid:true`, `kind:3`, and `header_length` 16842 and 6058354.
  - `coverage` is `"complete"`.
- **Observed.** `describe-dart.py:42` copies `libapp` verbatim. `verify.py:72` requires `coverage=='complete'` and four sections, but no per-section kind or magic check.
- **Observed (no inflation).** `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md:35-46` scopes "complete" to the reader's section/header contract. Lines 52-55 say instruction-section `magic_valid:false` is not reclassified.
- **Inferred.** The predicate would still pass if the Data-section kind changed while the provider label stayed "complete". Latent only.

### F7. Medium. A signal-entry sentence contradicts the held set

- **Observed.** `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:117-118`: "Dart parsing and both debugger verbs remain unheld; prior R22 identify remains one verb…".
- **Observed.** `verify/initial/after-c1.json` (stdout) has `t1_exercised` = `[identify-flutter-build, inspect-dart-aot, inspect-signal-decoders, decode-signal-recording]` and count 4. Its `targets["inspect-dart-aot"].new` binds `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` to `inspect-dart-legacy-saber.envelope.json` (`ev_d2ff19d7…`).
- **Observed.** `SCORECARD.md:2828`: "Exact held set is inherited identify, inspect-dart-aot, inspect-signal-decoders and decode-signal-recording". `corpus/lessons/round-23.md:75` says only the debugger verbs remain unheld, which is correct.
- **Inferred.** A reader of the signal entry alone would conclude `inspect-dart-aot` is unheld. Reword to, for example, "general Dart/Flutter source recovery and both debugger verbs remain unheld; inspect-dart-aot is held once (Dart entry)."

### F8. Low-medium, disclosed. Connector receipts carry `/tmp` and production-tree paths (write scope)

- **Observed.** `evidence/c1/connect-dart-symbols/fetch.json`: line 7 `archive_index.path = /tmp/kd23work/archive-index-v1.jar`; lines 34 and 59 `observed_path` = `/tmp/kd23work/saber-1330203.apk` and `/tmp/kd23work/saber-1340303.apk`; line 72 `/tmp/kd22probe/saber.apk`.
- **Observed.** `carriers.json` lines 21, 98, 200 carry `apk_path` under `/tmp`.
- **Observed.** `identify-flutter-build-saber-1330203.run.json:15` and `inspect-dart-aot-saber-1330203.run.json:15` have `cwd: /tmp/kd23work`. The wrapper at `run.json:14` is `bash -lc 'exec env npm_config_yes=true npx …'`.
- **Observed (disclosed).** `corpus/lessons/round-23.md:52` admits production-tree carrier/probe files and outside-lane scratch. `connect-dart-symbols/README.md` says artifacts are not retained.
- **Observed.** The nine connector receipts are tracked under `evidence/c1/connect-dart-symbols` (added in 2b40aec). `tools/count-c1.py:24` ROOTS includes `.ufo/waves/round-23/evidence/c1/`. No knowledge entry cites them, and after-c1 binds only three envelopes, so none is counted now.
- **Inferred.** Unadmitted receipts stay citable by the counter with no gate. Latent. The README sha table reproduces 9/9.

### F9. Low. Tracked scratch counter outputs under `w1/`

- **Observed.** `git show --stat 6615aea` adds `w1/.tmp-counter/{err.txt,out.json,r23-err.txt,r23-out-final.json,r23-out.json}`.
- **Observed.** `r23-out-final.json` records rev `a3c92eb`, `t1_exercised` = identify only, catalog 135/153. It is not an R23-candidate measurement, despite "final" in its name.
- **Observed.** The `CoverageMap.md:305-308` sha256 claims reproduce against the candidate blobs (`e843b4b4…`, `83216736…`, `e3b0c442…`, `a6e8a66f…`). `ConnectOutsideDebt.md:384` cites `r23-out.json` as a "peer-retained baseline".
- **Inferred.** Scratch output sits in a tracked report tree under a misleading name. No registry row cites it.

### F10. Informational. Ordering and timestamps

- **Observed.** Committed `captured_at` values run from `2026-10-21T14:38:06Z` (`inventory.run.json`) to `14:47:19Z` (`inspect-dart-legacy-saber.run.json`). `legacy-saber-download.json` is 14:47:18Z, connector `fetch.json` 14:43:18Z, `sources/fetches.json` 14:41:40Z.
- **Observed.** `claims.json` `declared_at` is `14:32:23.85Z`. a3c92eb committer is 14:33:00Z. 2b40aec committer is 14:56:57Z (author date 11:33:00-03:00, which equals a3c92eb's committer time).
- **Observed.** `predictions.json` is first committed in 2b40aec, in the same commit as the envelopes it predicts.
- **Inferred.** Captures postdate the claim declaration and precede the 2b40aec committer time, so the commit timeline is consistent. The author-date field is not a capture-consistent record. Git cannot prove that predictions preceded observations (PredictionHonesty seat's question).

## Write-scope review (pass, by code reading)

- `verify.py`:
  - `--out` is created with `exist_ok=False` (`:36`).
  - The lane `runtime/` is created (`:51-52`). It is ignored by `round-23/.gitignore` (`/runtime/`).
  - Child `TMPDIR` is set to runtime (`:39`).
  - The clone is a `TemporaryDirectory` under runtime (`:53-56`).
  - Fixture mutation happens in the clone and is restored (`:63-67`).
  - The only non-lane touch is the census child (F2).
- `describe-signals.py` and `describe-dart.py`: stdout only. `GIT_*` is scrubbed and `GIT_NO_REPLACE_OBJECTS` is set (`describe-signals.py:18-21`, `describe-dart.py:16-19`). Only `git show` and `rev-parse` are used.
- `preflight_dart_carrier.py`: no write call. The APK is read with `open(apk,"rb")` (`:113`) and `zipfile` over memory (`:116`).
- `make-uart.py`: writes only its output argument (`:22-23`).
- `tools/sigrok-cli.sh:12` exports `LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0`, a host preload that is recorded nowhere in run `env_overrides` (which hold only `REA_SIGROK_COMMAND`). It is disclosed in the knowledge entry at `:97-98`.
- Probe-semantics notes (no finding): the refusal row (`decode-invalid-decoder`) has no `subject`, so only argv binds its target. Carrier mapping is by name (`describe-signals.py:58`), which fails closed for other records. Argv is read by fixed position (`[3]`, `[4]`). `env_overrides` is caller-level only.

## Recomputation table (no defect)

| Item | Recomputed here | Recorded | Result |
|---|---|---|---|
| inventory envelope sha256 | `5f80218747c3f7c3308adef59216dea9559cada8c93a1ff543ebea6134a43d35` | signal-records.json | match |
| uart-help envelope sha256 | `462bc694a020c6b6eb9eeb171c5d7bfcf48c30a733ffe07c7df186b9d58c4d90` | same | match |
| decode-uart-hi envelope sha256 | `a40c947cf337319411b55c43e8e0270437e29324038a67bacb17232b9311a884` | same | match |
| decode-official-uart envelope sha256 | `7d5e07cca64ba60aa66ae25b8402ffe70a1bfc49bcce5c9a16f67826f768358e` | same | match |
| decode-invalid-decoder envelope sha256 | `04697e72e9cabc9dae1385731ea3f2becf8a4bb94dc2334f067180b3b1008292` | same | match |
| inspect-dart-legacy-saber envelope sha256 | `7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508` | dart-record.json | match |
| run `.stdout` equals envelope bytes (5 signal + 1 Dart) | `jq -j .stdout \| cmp` | `stdout_byte_equal` true | match |
| 5 signal rows, all non-null fields (`argv`, `env_overrides`, `exit`, `ok`, `command`, `operation`, `evidence_id`, `subject`, `artifact`, `selection`, `output_window`, `decoder_count`, `diagnostics`, `error`, annotation count and first 22 lines, `contains_literal_Hello_World`, `synthetic_exact`, argv checks restricted to `decode-*`) | scratch `jq` keyed to describe-signals' restriction (`recompute/*.v2n.json` vs recorded) | `signal-records.json` | identical |
| Dart row (`abi`, `argv`, `libapp`, `limitations`, `string_pool`, `evidence_id`, `subject.local_path` and digest, `subject_digest_matches_fetch`, `command_matches`) | scratch `jq` | `dart-record.json` | identical; not rebuilt: `rev`, constant `limit`, full `subject` object |
| carriers: `uart-hi.bin` sha256 | `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727` (2500 bytes) = subject digest = `generate-uart.run.json` stdout sha | match |
| carriers: `hello_world_8n1_9600.sr` sha256 | `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61` (58381 bytes) = subject digest = `official-download.json` | match |
| sigrok wrapper sha256 | `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902` at 2b40aec and at candidate = inventory and uart-help subject and tool sha | match |
| connector README table | 9 files, all sha256 values | 9/9 match |
| `source-pins.json` | describe-signals `a669607c…`, describe-dart `145b09bb…`, count-c1 `f4b8d16a…`, counter-fixtures `f2990b35…`, expected-v2 `458b30d5…`, fixture `a1f5aff8…` | candidate blobs | 6/6 match |
| producer digest | `verify.py` at V = `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a` = `producer_source_sha256`; candidate blob identical | match |
| S058 and S059 committed files | `e3f06dfe…a5f9` and `7af1c784…6f66` | SOURCES rows and fetches.json | match |
| S058, S059, S060, S061 located quotes | `grep -c` on retained files: 1 hit each | lessons Gate table | match |
| Dart libapp table offsets, sizes, header lengths | from envelope | knowledge table | match |
| knowledge: first match at sample 5512; Python 3.5.2; prlimit 1 GiB, 64 MiB, 30 s, core 0 | annotation line `5512-6032 uart-1: 48`; version banner; `resource_limiter.arguments` | match |
| synthetic expected `300-1100` and `1300-2100` | from `make-uart.py` bit layout: start bits at 200 and 1200, data 300–1099 and 1300–2099 | consistent |
| after-c1 4/6; 137/153 lexical; before 1/6; no-harm 1138, 104→106, 17/17, 32 rows; source-prefixes 57→61, A 51→55, mined 55→59, rejected 2 | producer outputs read as recorded values | present (row counts not independently recounted) |

## Stale W1 proposal re-evaluation (against 2838351…)

- `w1/ConnectSourceChain.md:260-262`: expected describe output. **Satisfied.** `synthetic_exact` true; `stdout_byte_equal` true on all five; both decode digests equal their carriers; official `output_window` is `{total_lines:12885, returned_lines:12885, has_more:false}`.
- `w1/ConnectSourceChain.md:263-265`: expected `t1_exercised_count=3`. **Superseded.** After-c1 records 4, adding `inspect-dart-aot` via the legacy envelope.
- `w1/SigrokInventoryFields.md:12,154` and `w1/CriticVacuity.md:61-65`: silent signature omission and "complete" overstated. **Still true at the descriptor level (F4). Addressed in prose** (r23-offline:17-26; lessons:18, :49).
- `w1/ReviewOriginalRuns.md:9-11`: R22 verify predicate does not bind argv target, subject digest, or stderr. **Partly addressed.** The R23 Dart predicate binds argv target and subject digest (`verify.py:72`). The signal predicate does not (`:71`), and stderr is ungated in both (F3).
- `w1/ReviewSourceQuality.md:7` and `w1/PlannerDataWalk.md:262`: `used-by` names an absent lessons file. **Resolved.** `corpus/lessons/round-23.md` is present at the candidate (blob `96ffed83…`).
- `w1/ReviewCompletenessMeaning.md:17`: no S058+ rows. **Resolved.** S058–S061 are present at the candidate; the registry is 57→61.
- `w1/CoverageMap.md:213-220`: S058 proposed as own-work. **Superseded.** S058 is the manual, S059 the dataset, S060 own-work (`ReviewSourceQuality.md:13`). Not reused.
- `w1/CoverageMap.md:305-308`: tmp-counter hashes. **Reproduce** (F9), but the files are tracked scratch.
- `w1/ConnectDartSymbols.md:65-66, 89-91, 123-125`: kind-3 rule and 1330203 "complete". **Consistent** with the legacy envelope. The 1340303 envelope was not recomputed (receipt only).
- `w1/CoverageMap.md:114-116` and `w1/DartSaberRefusal.md:97-101`: instruction-section magic false; kind 3 as the 2.14 layout. **Consistent,** and scoped in r23-dart:35-60.
- `w1/CriticSource.md:64-79`: first six official bytes are not payload; not lossless. **Addressed** by r23-offline:77-79 and lessons:98-101.
- `w1/ReviewVersionPins.md:12-13, 79`: npx `^6.5.0` cache hazard. Every R23 `run.json` argv pins `rea-agents@6.5.0` exactly. The hazard is latent for re-runs and not observed in candidate records.
- `w1/ConnectFrontier.md:141-145`: zero-line successes. **Not realized.** S060 windows are 110, 12885, and 2.

## Produced files and hashes

- `runtime/RegistryDescriptors/cand/` (ignored runtime): git-archive extraction of the candidate round-23 tree, plus LOG, SCORECARD, lessons, SOURCES, and the two R23 knowledge entries. About 9.9 MB; reproducible with `git archive 2838351…`.
  - `cand/corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`: sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35`.
  - `cand/corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md`: sha256 `22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351`.
- `runtime/RegistryDescriptors/recompute/*.json` (scratch recomputation outputs, ignored runtime):
  - Final comparison pairs (`<name>.v2n.json` scratch-side and `<name>.rec2n.json` recorded-side). Each pair has identical sha256:
    - inventory `5b67745597e68a78a2f40f878d6b522bba609416c710bdfbcbbdcde53e13a23c`
    - uart-help `e6afb119b0e4018400ab15671135abde69e2ebad126549954f18352ddd4fe47e`
    - decode-uart-hi `3f40d44d96ddc2d0a5c323e8c69ec15ecb238fb1d636e5ca7a238e3a0974c2dc`
    - decode-official-uart `32e89207f335ad6094a11715c33157684658921080a534413827b4dd57b06b77`
    - decode-invalid-decoder `b42a33aed92e46cb19dcaa9cfe2e40eb9e395268ed79f255503cb9f48cec7976`
  - `signal-recorded.json` `8ce0197cb20fce4947db1a48721ff6e4727854e2f09fc748569ec8c607f3ef4c`
  - `inventory.json` `99d320f056ab1dbb7982bab8727d66ab3539ee406776e8348a8ea1b7ff9124e0`; `inventory.recorded.json` `2878f9c86ce97e48fe90e3aab57945e0c0e4bae2bd1e3f39fc28cd6a09059b87`
  - `uart-help.json` `671f34629c3fac7e3a830227df40add432aa53ce310b2e0e56508cca1213a182`; `uart-help.recorded.json` `567b240fd794eb8078777dbe08a8d7b10ebb9b7da93309a491daa90b1135aea9`
  - `decode-uart-hi.json` `99853071df21d700f21a25e1c894d05799ef92da62b89533913bee47baf2020e`
  - `decode-official-uart.json` `6695ca6422597e2a1dbcf67d07cef751c6739a3b182ddb8dcaf101315f40229d`
  - `decode-invalid-decoder.json` `82acdc9e1b557ce7e63ad760fd8f0275b44d8b5c485be8de18c2d539cd600139`; `decode-invalid-decoder.recorded.json` `df5f19730c39dc9233e4736ad3f29b3c19f752e54aa85849f1aecd3fde952bd9`
  - `dart.mine2.json` `0ca07a0f575ca26a6a33a436807e3fd744c40ff56f81cc14915d28204a8cee3d`; `dart.recorded.json` `52c70b7feb66f1efba52ce6f7efe6b447223c29f289c9761ec107d88617fed22`
- This report: `.ufo/waves/round-23/w2/RegistryDescriptors.md`. Its own hash cannot be recorded inside it.
- No peer report was edited or overwritten.

## Installs

None. `jq`, `python3`, `git`, `sha256sum`, `cmp`, `tar`, and `grep` were already present and used read-only. No pacman, uv, npm, cargo, or release-binary install, and no config edit.

## Open risks and unknowns

- **Not recomputable from retained bytes.** The APK (`runtime/saber-1330203.apk`, sha `a7b1f5c8…`, 41263437 bytes) is not retained; its digest and size rest on the L1 download record and the F-Droid index entry, which the record itself says is not signature-verified. The sigrok AppImage (`49d2f597…`), the sigrok-cli ELF (`10fed05a…`), the host libraries, and the REA `dist` digests are not retained or not recomputed here.
- **Census binding** (F2). Re-running on the lane worktree changes the outcome if the worktree moves. The candidate's `SOURCES.md` differs from the current worktree now.
- **Recorded argv** in `signal-records.json`, `dart-record.json`, `no-harm.json`, and `selftest.json` names a removed `runtime/verify-pmrqyxfj/snapshot` path. These child commands are not verbatim re-runnable; the reproducible form is `--root`/`--rev`.
- **npx cache** (inferred, unrecorded). REA captures run `npx -y rea-agents@6.5.0`, which populates `~/.npm/_npx`. W1 `ReviewVersionPins.md:12` observed that cache. `run.json` records no cache write, so the write outside the lane is unrecorded.
- **Not checked.** `sources-census.sh` beyond its header, `count-c1.py` binder internals (other seats' items), and the connector's 1340303 and identify envelope bodies beyond the README sha table.
- **Serialization.** The signal and Dart rows were compared field-by-field on parsed values, not byte-for-byte on the sorted-key JSON serialization.

Report: .ufo/waves/round-23/w2/RegistryDescriptors.md
