# OriginalInventory: R23-C1 `inventory.envelope.json` / `inventory.run.json` source review

Seat: `KaidokuR23.OriginalInventory`. Leaf source review, author-side (not independent outside admission).
Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Baseline: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Bytes: `git show` / `git ls-tree` / `git grep` / `git log` / `git diff` at the candidate only. The pair and launcher blobs are identical at `6615aea` (`git diff --stat 6615aea 2838351…` on the three paths is empty). Local `python3` (stdlib json/hashlib) and `sha256sum` were used on the extracted candidate bytes. No producer replay, no counter or verifier execution, no target, device, remote or process access, and no npm-cache or HOME reads.

## Verdict

- Core pair facts hold on candidate bytes: exact byte equality; `ok:true`; `meta.command` = argv subcommand = `inspect-signal-decoders`; `data.operation` = `inspect_signal_decoders`; exit 0; launcher digest = committed launcher; returned set = 110 decoders, reconciled against the committed extraction listing.
- Not retained, overclaimed, or not independently bound: the executed sigrok binary and decoders at run time (only post-run pins exist); "environment" (one env key retained); the "counting command" the knowledge entry says is retained; `evidence_id` (not derivable from retained bytes); REA 6.5.0 as a resolved identity; the run-record producer (not committed); the `prlimit` hash; the `authority` label; raw producer output.
- The counted binding is envelope-only. It checks `ok`, `meta.command`, `data.evidence_id`, `data.operation`, and a refusal scan. Byte equality is checked only by `verify.py`. Subject identity, the returned-set window, limits and run exit are gated by nothing.
- No false value in a core field was found.

## Field matrix

| Claimed field | Retained at candidate | Independent binding at candidate | Status |
|---|---|---|---|
| Byte equality, envelope = run stdout | envelope blob `4b4a20e9…` line 1; run blob `26cf4145…` line 17 | recomputed here; `describe-signals.py:43`; `verify.py:71` | HOLDS (observed) |
| `ok:true` | envelope line 1 | static `bind_cli` (`round-22/tools/count-c1.py:74-76`) | HOLDS (observed; binder static) |
| `meta.command` | envelope line 1 | run argv[3] (run line 6); `describe-signals.py:64` | HOLDS (observed) |
| `data.operation` | envelope line 1 | static `r21.bind` mapping (`round-21/tools/verb-coverage.py:85`) | HOLDS (observed; binder static) |
| exit 0, stderr empty | run lines 16, 18 | none (counter and verifier do not gate run exit) | RETAINED ONLY |
| Subject digest = launcher | envelope `data.subject`, `normalized_result.tool.sha256` | committed `tools/sigrok-cli.sh` `50fe4359…0902`, 698 B; pins entry (post-run) | HOLDS by hand; no gate (B2) |
| Executed ELF, libraries, decoder tree | nowhere in the pair | `tool-runtime-pins.json`, captured 4 min 52 s after the run | NOT BOUND AT RUN (N1) |
| Version banner | envelope `tool.version_banner` | byte-identical to `sigrok-version-attempt1.json` stdout (no timestamp) | CORROBORATED (H6) |
| Returned set = 110 decoders | envelope `decoders`, `output_window` | extraction listing: 112 dirs minus `common` (helper) minus `signature` (load failure) | HOLDS (extraction-time listing) |
| `has_more:false`, `limit:null`, `--all` | envelope `output_window`, `parameters`; run argv line 8 | consistent with argv; not gated | HOLDS (not gated) |
| Diagnostics complete | envelope `diagnostics` (841 chars) | ends `SyntaxError: invalid syntax\n\n`; names `signature/pd.py` line 138 | HOLDS |
| `limits` as/fsize/cpu | envelope `limits`, `resource_limiter.arguments` | argv matches exactly | HOLDS |
| `limits` input/output/timeout | envelope `limits` | none in committed bytes | RETAINED ONLY (N11) |
| `resource_limiter.sha256` (prlimit) | envelope | none; no prlimit pin | NOT BOUND (N7) |
| "environment" retained | run `env_overrides` (lines 13-15, one key); envelope `environment: null` | launcher bytes give part of it | OVERCLAIMED (N2) |
| `evidence_id` | envelope line 1 | not derivable (64 forms, N4) | NOT BOUND (producer-minted) |
| REA 6.5.0 | run argv line 5 (`npx -y rea-agents@6.5.0`) | none resolved | NOT BOUND (N5) |
| `authority: shipped-artifact` | envelope line 1 | AppImage digest absent from pair | NOT BOUND, label only (N8) |
| "counting command" retained by recheck producer | none | none | NOT RETAINED (N3) |
| Run record provenance | run.json | no committed writer | UNCOMMITTED PRODUCER (N6) |
| Raw producer output | `raw_result: null` | none | NOT RETAINED (N10) |
| Source row S060 admission chain | `corpus/SOURCES.md:66` | tier A, mined, 2026-10-21, used-by includes the knowledge entry | HOLDS (observed) |

## Findings

### Holds (observed)

**H1 Byte equality.** Envelope blob `4b4a20e9907cb29d3dfc21aa95b8f9453c47755c`: 9391 B, sha256 `5f80218747c3f7c3308adef59216dea9559cada8c93a1ff543ebea6134a43d35`, one line. Run blob `26cf414513ebb90b6914d49b268562f1b18bdb2a`: 10990 B, sha256 `df20226c269680c91c76bfa85386073d69257876c23e63e91176f7c0c5faae76`, 20 lines, stdout on line 17. Check: `run.stdout.encode('utf-8') == envelope bytes` gives True. Stdout is 9388 characters and 9391 bytes (three `²` in `eeprom24xx`, `i2cdemux`, `i2cfilter`). Both end in `\n`.

**H2 Success, command, operation.** Envelope line 1: `"ok":true`; `"meta":{"command":"inspect-signal-decoders","duration":"239ms"}`; `data.operation:"inspect_signal_decoders"`; `data.predicate_type:"rea.analysis"`. Run: `exit: 0` (line 16); `stderr: ""` (line 18). Static reading of the binder: round-22 `bind_cli` (`.ufo/waves/round-22/tools/count-c1.py:69-98`) requires `ok is True`, `meta.command == verb`, and `evidence_id` and `operation` in `data`; round-21 `bind` (`round-21/tools/verb-coverage.py:77-101`) matches `operation` to `inspect_signal_decoders` (line 85). A scan of every dict key in the envelope found no `error`, `errors`, `code`, `status`, `completion_status` or `exit_code`, so `refused()` (`verb-coverage.py:39-55`) cannot refuse. The counter was not executed. [inferred from static reading]

**H3 Launcher subject.** `data.subject`: `name: sigrok-cli.sh`, `digest.sha256: 50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902`, `local_path` absolute, `format: file`, `architecture: null`. Committed `.ufo/waves/round-23/tools/sigrok-cli.sh`: blob `3a806cbb842d68bff9d23aa3cbc0c09d1943f86d`, mode 100755, 698 B, sha256 `50fe4359…0902`. The subject digest equals `normalized_result.tool.sha256`, and the `tool-runtime-pins.json` launcher entry (size 698). Run line 14 `REA_SIGROK_COMMAND`, `subject.local_path`, `tool.configured_path` and `tool.path` are one string. The resource-limiter argv ends with that launcher path, so prlimit wraps the launcher.

**H4 Returned set.** `output_window: {unit:"decoders", examined:110, matching:110, returned:110, has_more:false}`. `decoders` has 110 unique, sorted entries. `uart` is present and `signature` is absent. `parameters` and `selection`: `decoder:null, query:"", offset:0, limit:null`. Argv contains `--all`. Independent reconciliation from committed `.ufo/waves/round-23/sigrok-extraction.json` (blob `9d1dd16c82fdbacb25c41be1bbee375e566d880d`, exit 0, 1972-line AppImage extraction listing): 112 directories under `squashfs-root/usr/share/libsigrokdecode/decoders/`; 111 contain `pd.py`. `common/` has no `pd.py` and holds `__init__.py`, `plugtrx`, `sdcard`, `srdhelper`. `signature/pd.py` exists. 111 minus `{signature}` equals the envelope's 110 set exactly. This is an extraction-time listing, not a run-time one. [observed]

**H5 Diagnostics and limits.** `diagnostics` is 841 characters, ends `SyntaxError: invalid syntax\n\n`, has no truncation marker, and names `signature/pd.py` line 138, the same path as the extraction. `limits.address_space_bytes` 1073741824, `file_bytes` 67108864 and `cpu_seconds` 30 equal the prlimit argv `--as=1073741824:1073741824`, `--fsize=67108864:67108864`, `--cpu=30:30`. Output is 9391 B against `output_bytes` 4194304, so nothing was truncated. `hardware_acquisition: "not-performed"` is retained.

**H6 Version banner.** `tool.version_banner` (568 chars) is byte-identical to the stdout of `.ufo/waves/round-23/sigrok-version-attempt1.json`, a direct run of `runtime/squashfs-root/usr/bin/sigrok-cli --version` with no timestamp. This corroborates banner stability only. It does not bind the run-time digest (N1).

**H7 Admission chain.** `corpus/SOURCES.md:66` row S060: tier `A`, status `mined`, opened `2026-10-21`, used-by `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md, corpus/lessons/round-23.md`. Knowledge line 15 cites `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` verbatim, once. Knowledge line 14 cites the envelope path inside backticks, so the counter's path regex stops before the backtick (`count-c1.py:97`).

### Not retained, overclaimed, or not independently bound

**N1 (material) The executed tool is not bound at run time.** Launcher line 15 execs `$runtime/usr/bin/sigrok-cli`. `.ufo/waves/round-23/.gitignore` line 1 is `/runtime/`, so the ELF has no git custody. Neither the envelope nor the run record carries a digest for the ELF, the libraries, or the decoder tree. The only binding is `tool-runtime-pins.json` (blob `eba8145eaec6bef850f041fdd45cb47606292f9d`, line 3 `captured_at: 2026-10-21T14:42:59.166503+00:00`): ELF `10fed05a…`, `libsigrok.so.4` `0861b03c…`, `libsigrokdecode.so.4` `4bfe11a3…`, `uart/pd.py` `51a29d0e…`, host `libgmodule` `b259a089…`, `libglib` `1e8739af…`, `libgio` `b38001cc…`. The run `captured_at` is `14:38:06.805133`, so the pin is about 4 min 52 s later, and its own `limit` reads "one named instant; selected files only, not complete installation or continuous custody". Any statement that this pair identifies the sigrok 0.7.2 binary or its decoders is a false bind. The envelope's own `limitations` says "Decoder modules and libraries are trusted and not fully fingerprinted." [observed]

**N2 (overclaim) "environment" is not retained.** Knowledge line 2: "exact producing argv/environment/stdout/stderr/exit retained in adjacent .run.json files". Run `env_overrides` (lines 13-15) holds only `REA_SIGROK_COMMAND`. Envelope `data.environment` is `null` (line 1). The inherited process environment is not retained. The launcher-set variables (launcher lines 11-14: `LD_LIBRARY_PATH`, `LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0`, `PYTHONPATH`, `SIGROKDECODE_DIR`) appear only in the committed launcher bytes, not in the run record.

**N3 (overclaim) "counting command" is not retained.** Knowledge lines 17-19: "the field count and counting command are retained by the `recheck:` producer." `describe-signals.py` retains `decoder_count` (line 50), `argv`, `env_overrides` (line 44) and `output_window`. No counting command and no count verdict appears in the envelope, the run record, or describe-signals output. [observed]

**N4 (not bound) `evidence_id` is producer-minted.** `data.evidence_id` `ev_940cf7bb…` (envelope line 1) cannot be re-derived from retained bytes. I tried 64 forms: sha256 over the raw file; the `data` object and the envelope object, each with and without the id; sorted and unsorted keys; compact and default separators; `ensure_ascii` on and off; with and without a trailing newline. None matched. The binding is textual association only. `count-c1.py:9` ("No authentication claim") and `round-22/tools/count-c1.py:14-16` ("local association, not authentication") say so. [unknown algorithm; not in committed bytes]

**N5 (not bound) REA 6.5.0 is an argv spec, not a resolved identity.** Run line 5 `rea-agents@6.5.0` is the `npx -y` request. No resolved version, tarball digest or integrity value appears in the run record or the envelope. `provider.version` is `sigrok-cli@0.7.2`. Knowledge line 13 "REA6.5.0" rests on argv alone. npm integrity cannot be checked under the no-remote contract. [unknown]

**N6 (not bound) The run-record producer is not committed.** `git grep -l captured_at <candidate> -- '*.py' '*.sh' '*.js' '*.ts' '*.mjs'` returns nothing. `describe-signals.py:37-44` and `describe-dart.py:40` read run records, but no committed file writes them. The knowledge file does not cite `inventory.run.json`, and the counter never reads it. Byte equality therefore shows only that two retained copies agree. It does not show that a committed harness captured them.

**N7 (not bound) `resource_limiter.sha256` for `/usr/bin/prlimit`** (`092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96`) has no committed pin. None of the eight `tool-runtime-pins.json` paths is prlimit.

**N8 (not bound, low) `authority: "shipped-artifact"`.** Envelope `data.authority`, line 1. The subject is a lane-authored wrapper added in commit `2b40aec`. The official AppImage digest `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614` appears in `sigrok-extraction.json` (`appimage_sha256`) and in `.ufo/waves/round-23/tools/setup-sigrok.py:14`, but not in the envelope or the run record. The label is producer-asserted. `setup-sigrok.py:6` itself says "Digest identity is not publisher authentication."

**N9 (wording) "installed catalog discovery"** (knowledge line 19). The returned set is the loaded set. The extraction holds 111 installed decoder packages, and `signature` is installed but did not load (H4). The text should say "loaded" or "returned".

**N10 (not retained at candidate) Raw producer output.** `data.raw_result` is `null` (envelope line 1). No raw sigrok listing is committed. W1 `w1/SigrokInventoryFields.md:36-39` cites a raw `--list-supported` run and an 841-byte stderr, and says the raw file was removed. Those claims are not re-evaluable at the candidate. Only the 841-byte envelope `diagnostics` string is retained.

**N11 (partly enforced) `limits`.** Only `as`, `fsize` and `cpu` are visible in `resource_limiter.arguments`. `input_bytes` (33554432), `output_bytes` (4194304) and `command_timeout_ms` (30000) have no committed enforcement evidence. The output cap was not reached (H5).

### Boundaries of the counted and verified binding

**B1** `count-c1.py` `measure` (lines 98-124) reads only `.json` blobs cited by knowledge entries, here the envelope. It never reads `run.json` and does not check `subject`, `output_window`, `limits` or run `exit`. Line 133 says "run stdout checked separately". The envelope-level binder is `bind_new` (lines 42-56), which delegates to `bind_cli`.

**B2** `verify.py:71` (signal-records gate) requires `len(records)==5` and `stdout_byte_equal` for all five records. `describe-signals.py:57-62` checks subject-versus-carrier and argv-target only for `decode-*` names. No committed gate checks the inventory subject digest. I checked it by hand (H3).

**B3** The candidate verification outputs (`verify/initial/*.json`) record `source_rev` `6615aeae642aec36959180e7ea940b2794c7f1cb`, not the candidate. The pair and launcher blobs are identical at both revisions (see the header), so the verification covers the candidate bytes of these files.

## Stale W1 re-evaluation against `2838351`

| W1 claim (file:line) | Result at candidate |
|---|---|
| `ConnectOutsideDebt.md:217`; `PlannerDataWalk.md:96`; `CoverageMap.md:68,246`; `CriticSource.md:77`; `CriticVacuity.md:62`; `ReviewNoExecution.md:15`; `ReviewScope.md:13`; `SigrokInventoryFields.md:41,140`; `SourceRegistry.md:59`; `CounterRefusals.md:168`; `ConnectSignalFirmware.md:69` | HOLDS: 110/110/110, `has_more:false`, `ok:true`, 9391 B, sha `5f802187…`, exit 0, `uart` present, `pd.py:138` |
| `ConnectSourceChain.md:146-151`, `:195-198`, L5 row line 32 | HOLDS: `tool.sha256` is the wrapper only; ELF `10fed05a` appears only in post-run pins (14:42:59 against run 14:38:06) |
| `ConnectSourceChain.md:161-167`; `SigrokInventoryFields.md:11-12` | HOLDS for the set accounting (112 dirs, `common` helper, `signature` load failure). "110 = raw `--list-supported` count" is not re-evaluable (N10) |
| `ReviewCompletenessMeaning.md:11` | HOLDS: run lines 2-20, exit 0, empty stderr, `ok:true`, operation, `decoder:null`, subject sha `50fe…` |
| `ReviewNoExecution.md:14` | HOLDS IN PART: wrapper and banner only. The `SigrokRecordingProvider.js:231-232` citation is from the npm cache and is not re-evaluable |
| `SigrokInventoryFields.md:36-39` | NOT RE-EVALUABLE: raw run removed; only the 841-byte envelope diagnostics is retained |
| `SigrokInventoryFields.md:43-63` (npm-cache parser source) | NOT RE-EVALUABLE: outside candidate bytes, not opened by this seat |
| Knowledge line 2 ("environment") | OVERCLAIM (N2) |
| Knowledge lines 17-19 ("counting command" retained; "installed") | OVERCLAIM (N3, N9) |
| Knowledge line 13 ("REA6.5.0") | ARGV ONLY (N5) |
| `corpus/SOURCES.md:66` | HOLDS: tier A, mined, 2026-10-21, used-by includes the entry; `annotations_text` does not apply to inventory |
| `corpus/lessons/round-23.md:18`, `:49` | HOLDS: loaded window; `signature` failure stays in diagnostics |
| `CriticSeparation.md:28` ("all five envelopes byte-equal") | Inventory HOLDS (H1). The other four were not re-evaluated |

## Produced files and hashes

- This report: `.ufo/waves/round-23/w2/OriginalInventory.md`. Its sha256 is given in the seat's final message.
- Candidate inputs, read only (git blob ids and sha256 of extracted bytes): `evidence/c1/inventory.envelope.json` (`4b4a20e9…`; `5f802187…3d35`); `evidence/c1/inventory.run.json` (`26cf4145…`; `df20226c…aae76`); `tools/sigrok-cli.sh` (`3a806cbb…`; `50fe4359…0902`); `sigrok-extraction.json` (`9d1dd16c…`); `sigrok-version-attempt1.json` (`5bc0e1e4…`); `tool-runtime-pins.json` (`eba8145e…`); `tools/count-c1.py`, `tools/describe-signals.py`, `verify.py`, `round-22/tools/count-c1.py`, `round-21/tools/verb-coverage.py`, `tools/setup-sigrok.py`, `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`, `corpus/SOURCES.md`.
- Scratch extracts were written under `/tmp` for analysis and then removed. This is outside the allowed write roots and is disclosed here. No other files were written.

## Installs or none

None. No pacman, uv, npm, cargo or other install or update was run. Git was used only read-only (`show`, `ls-tree`, `log`, `diff`, `grep`, `cat-file`). Python was used only with stdlib json and hashlib on candidate bytes.

## Open risks

1. Run-time identity of the executed sigrok binary, libraries and decoders is unbound (N1). The only evidence is post-run pins with no custody between the two instants. Any "sigrok 0.7.2 / decoder identity" claim from this pair is a false bind.
2. `evidence_id` is producer-minted and not verifiable from committed bytes (N4).
3. The REA 6.5.0 resolution (npm tarball integrity) is unverifiable under the no-remote contract (N5).
4. The run-record producer is not committed (N6). The provenance of the "original" stdout rests on an uncommitted harness.
5. The counted binding is envelope-only and does not gate subject, window, limits or run exit (B1, B2). A future partial window would still count.
6. `prlimit` and the input, output and timeout limits have no committed evidence (N7, N11).
7. Raw producer output and the npm-cache producer-source claims cannot be re-evaluated at the candidate (N10, W1 `SigrokInventoryFields.md:43-63`).
8. Unknown: how REA derives `provider.version` (`sigrok-cli@0.7.2`); whether the run environment matched the launcher's assumptions, including the host `LD_PRELOAD` library, beyond the post-run pin.
