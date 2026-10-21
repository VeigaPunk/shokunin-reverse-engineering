# ScopeDeviation — R23-C1: ConnectDartSymbols original writes vs independent L1 download/run

Seat: `KaidokuR23.ScopeDeviation` · leaf source reviewer · author-side, not an outside admission.
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` (round-23: retain measured four-of-six coverage and refusal controls).
Baseline: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.

Method: read-only `git show`, `git ls-tree`, `git log`, `git blame`, `git grep`, `git rev-parse` against the candidate; JSON parsed in memory from candidate blobs; SHA-256 over blob bytes.
Not run: rea-agents / npx, `count-c1.py`, `describe-dart.py`, `preflight_dart_carrier.py`, any network, device, or process access, any counting or control command. The ignored runtime APK was neither opened nor hashed (worktree state, outside candidate bytes). Peer w2 reports were not read.
Labels: **observed** = read from candidate bytes; **[INFERENCE]** = derived, not executed; **[UNKNOWN]** = not establishable from the candidate.

## Verdict

1. **Originals preserved — observed.** All nine SHA-256 pins in the connector's §9 match the candidate blobs byte-for-byte. The tenth file (`README.md`) is unpinned. The directory tree (`84c9b24256d77420f9044edcdde64c2a7f7c817e`) is identical at `2b40aec` and at the candidate, and `2b40aec` is the only commit that touches it.
2. **Only the L1 envelope is cited as an admitted witness — observed at citation level.** The admitted knowledge entry cites three L1 JSON files, and only its envelope is witness material. No admitted surface cites any connector file path, blob hash, or evidence ID (SD-11); `knowledge:31` names the connector directory only as a disambiguation. Code reading (not execution) shows the L1 `.run.json` and download receipt cannot bind (SD-13). Whether the L1 envelope binds is unevaluated here.
3. **No compliance credit — observed in admitted text** (`corpus/lessons/round-23.md:52`: "never borrow them as compliant execution"). Two admitted wordings can leak credit: SD-1 ("independent") and SD-2 ("first successful").
4. **Disclosure is miscounted and narrower than the receipts** (SD-3, SD-4). Stale W1 claims are re-evaluated in SD-5: one exit-code error and one unsupported "reproduced" claim.

## Findings

### SD-1 — medium — "independent" overstates an author-side re-run [observed]
- `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md:2`: "L1 independently re-fetched and executed the static reader after the connector's scope deviation."
- `corpus/lessons/round-23.md:52`: "L1 independently re-fetched/hashed/re-executed only the selected public legacy carrier."
- `LOG.md:2635–2636`: "only the independent L1 carrier run is admitted as the new Dart witness."
- Frozen text that conflicts: `.ufo/waves/round-23/claims.json` (candidate blob sha256 `249811d9d103960811025d5305422e97271877bec1f470c1601cadc1f40d1906`, 2,386 B), `claims[0].not_claimed` contains "independent non-author admission".
- L1 is the sole integration owner (connector report §0), and the S061 row is own-work (`corpus/SOURCES.md:67`: kind `own-work`, tier A, status `mined`). S055 (R22) uses the same convention (`corpus/SOURCES.md:61`).
- "Independent" here means re-performed by L1 after the deviation, not non-author. Recommended wording: "author-side L1 re-run after the deviation" in all three places, or an explicit non-admission qualifier. Not applied (source review only).

### SD-2 — medium-low — "first successful `inspect-dart-aot`" is contradicted by retained connector receipts [observed]
- Admitted: `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md:7`: "Coverage-map ground: first successful `inspect-dart-aot`".
- Same evidence root, retained: `connect-dart-symbols/inspect-dart-aot-saber-1330203.run.json` (exit 0, stderr `""`, `captured_at_utc` 2026-10-21T14:42:37Z, evidence_id `ev_dcdab9d0…`) and `…-saber-1340303.run.json` (exit 0, same timestamp, `ev_04072bb4…`). L1's run is at 14:47:19.045031Z.
- Read literally the sentence is false. The intended meaning is probably "first admitted successful". No admitted row credits the connector runs (SD-11, SD-5), so no credit has leaked yet. Fix the wording.

### SD-3 — low — connector's write count is wrong: "nine" vs ten [observed]
- `.ufo/waves/round-23/w1/ConnectDartSymbols.md:15`: "wrote nine files … (three CLI envelopes, three .run.json receipts, carriers.json, fetch.json, preflight_dart_carrier.py, README.md)". The parenthetical enumerates **ten**. Repeated at `:305` ("the nine files").
- `git show --stat 2b40aec -- .ufo/waves/round-23/evidence/c1/connect-dart-symbols`: "10 files changed, 729 insertions(+)".
- §9 pins nine; `README.md` (sha256 `83de3786f38854a74e3bfaabf8457a68036ddba2b8cc385d27ddb63ab162b05c`, 2,359 B) is unpinned. Any accounting must use ten.

### SD-4 — medium-low — the disclosed deviation class is narrower than the connector's receipts [observed]
Beyond the file writes, the connector's own receipts record three further classes of out-of-contract activity:
- **REA CLI executions: three.** `inspect-dart-aot` ×2 and `identify-flutter-build` ×1, with `cwd` `/tmp/kd23work` and `env_overrides` `npm_config_yes=true` (`connect-dart-symbols/*.run.json`).
- **Network downloads to `/tmp/kd23work`** (`fetch.json`, generated 14:43:18Z): APK 1.33.2 (41,263,437 B, sha256 `a7b1f5c8…ea618`), APK 1.34.3 (42,571,868 B, sha256 `ac68a976…b8b8d`), F-Droid `index-v1.jar` (8,239,064 B, sha256 `c5427c3d…13df5b4`). About 92 MB in total.
- **npm cache reads**: `ConnectDartSymbols.md` §2 cites `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/…` and, "read but not executed", `/home/vgpnk/.npm/_npx/a1722018f28f9df2` (6.7.0).

Disclosure gap: `LOG.md:2634` says "production-tree writes" and `corpus/lessons/round-23.md:52` says "production-tree carrier/probe files". Neither names the downloads, the REA executions, or the npm-cache reads. The connector's §0 names only the file writes.
Admitted-surface check (`git grep` on candidate: `FlutterBuildProvider|DartElf|rea-agents@6|/home/vgpnk|_npx` over `corpus/knowledge/2026-10-21-r23-*` and `corpus/lessons/round-23.md`): hits only at the L1 entry lines 3, 17, 24 (recheck root path, runtime APK path, L1 argv) and the signal entry line 3 (recheck root path). No admitted row relies on the connector's dist reads.

### SD-5 — stale W1 claims re-evaluated against candidate [observed unless marked]
| Connector claim (`ConnectDartSymbols.md`) | Candidate check | Status |
|---|---|---|
| "wrote nine files" (`:15`, `:305`) | ten files (`git show --stat 2b40aec`) | corrected (SD-3) |
| "reproduced the observed REA outcomes (exit 0 / exit 0 / exit 3-as-refusal-equivalent)" (`:209–210`) | REA exit on the R22 carrier is **1** (`:36`; `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.run.json`, sha256 `d1eaa23f…eb34a`, exit 1; `carriers.json:91` `"exit": 1`). "3" is the preflight script's own code (`preflight_dart_carrier.py:23`, `:156` `verdict = 3`). No preflight output is retained; `README.md:26–28` lists only expected codes. | **rejected**: mislabels a preflight code as an REA outcome; "reproduced" has no receipt |
| "stdout 87,0xx B" for 1.34.3 (`:162`) | `inspect-dart-aot-saber-1340303.envelope.json` = 89,155 B (sha256 `22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d`) | corrected |
| S061 for own rows plus Dart-commit (`d36adbacaf`), archive-index and probe-receipt rows (`:235`, §6) | only S061 minted, by L1 (`corpus/SOURCES.md:67`); S058–S061 contain no `d36adbacaf` or index row | superseded; no credit |
| "second held T1 verb, k=2/6, incomplete=4" (§6) | candidate records cumulative "1/6→4/6" (`LOG.md:2650`), which includes signal verbs not evaluated here | superseded; count **not verified here** |
| "three compulsory qualifiers" (§6) | carrier-conditional (`knowledge:59–60`); R22 refusal preserved (`knowledge:8`); string-pool partial and lower bounds (`knowledge:50–51`) | present in substance |
| "first stable Dart = 3.13" (§5) [INFERENCE] | not admitted; admitted entry says the causal boundary is "not established" (`knowledge:60`) | calibrated; no credit |
| "identify-flutter-build must not be double-counted" (§4) | admitted entry has 0 occurrences of `identify-flutter-build`; `knowledge:65` mentions only "a separate identify success" | holds |
| "L1 should re-fetch, re-hash, re-execute" (§8) | done (L1 receipts exist) but thinner than the connector's receipts (SD-6) | done; provenance weaker |
| "R22 refusal = exit 1, stderr empty" (§1) | `:36`; R22 run.json exit 1, stderr `""` | holds |

### SD-6 — low-medium — the admitted producing record carries less producer identity than the connector's [observed]
- `inspect-dart-legacy-saber.run.json` (sha256 `588460380006a5c1044ba8fb9b8b0136446a2cab5c40e8f2f911978328e82fa6`, 93,379 B) has keys: `argv`, `cwd`, `env_overrides` (`{}`), `exit` (0), `stdout`, `stderr` (`""`), `captured_at`. It records no resolved package path or version, and no node or npx version. The connector's receipts record `resolved_tool` (package path under `_npx/ad9a3fdbcad992c6`, node v24.21.0, npx 11.19.0).
- The admitted "6.5.0" identity therefore rests on the argv string `rea-agents@6.5.0` resolved by npx at run time. The admitted envelope's `data.provider.version` is `null` (`inspect-dart-legacy-saber.envelope.json`, sha256 `7768198e…c508`).
- `legacy-saber-download.json` (sha256 `2e6c00305dfbaf09001c421df6e4cf0730dcce3bfb7a5aa5acc358873da40496`, 511 B) records no fetch command and no response headers. "independently fetched bytes" is a self-written `producer` string. Its `signature_verification` field says "not performed; digest identity only", and the admitted entry says the same (`knowledge:21–22`).
- Mitigation (observed): the L1 subject path, argv, `parameters.path`, and `locations` all point to L1's own runtime path, not `/tmp/kd23work`. Its `evidence_id` (`ev_d2ff19d7…`) differs from the connector's (`ev_dcdab9d0…`). Digest and size equal the connector's fetch record and the index entry.

### SD-7 — low — recheck line and "recomputed" overstate reproducibility [observed; manual evaluation marked]
- `knowledge:3` recheck command contains an unfilled `--rev <MEASURED-COMMIT>` and a lane-absolute `--root`. It is not runnable as written.
- `knowledge:45` says the table is "recomputed from the committed envelope by the `recheck:` command". `describe-dart.py:36` reads `normalized_result`. `:42` emits `n['libapp']`, a projection of producer-stored fields. `:39` checks `stdout_byte_equal`; `:48` checks the subject digest against the download receipt. The script does not parse APK bytes. Recommended wording: "re-projected from the committed envelope; not an APK re-parse".
- [INFERENCE, manual evaluation, script not executed] Over candidate bytes: `stdout_byte_equal` true (stdout length 87,293 = envelope length; bytes identical); `argv[4]` equals `subject.local_path`; `argv[3]` equals `meta.command` = `inspect-dart-aot`; subject digest equals download sha256 `a7b1f5c8…`.

### SD-8 — info, open — admitted chain has no admitted archive-index anchor [observed]
- The only index anchor is the connector's `fetch.json` `downloads[0].index_entry.hash` (`a7b1f5c8…`). That file is unadmitted, and its own `signature_note` says the index was not cryptographically verified.
- The admitted entry asserts no index or APK signature verification (`knowledge:21–22`). Citing the index later needs L1's own fetch and a dedicated source row.

### SD-9 — info, open — connector originals sit under a counted root [observed]
- `.ufo/waves/round-23/tools/count-c1.py:24` `ROOTS` includes `.ufo/waves/round-23/evidence/c1/`, so the connector's ten files are inside it.
- No knowledge entry cites them now. Binding requires the full-prefix citation (`count-c1.py:97`, `cited_pattern`) plus an eligible S-row. The connector report and README name the paths, so a later citation is possible.

### SD-10 — info, unknown — stop-order timing [observed timestamps; stop order UNKNOWN]
- Connector: REA runs `captured_at_utc` 2026-10-21T14:42:37Z for all three runs, identical to the second, with per-run durations 198–277 ms (batch-level stamp). `fetch.json` `generated_at_utc` 14:43:18Z. `carriers.json:3` `generated_at_utc` 14:45:00Z, the last connector write.
- L1: `legacy-saber-download.json` `captured_at` 14:47:18.289487Z; run `captured_at` 14:47:19.045031Z.
- The connector's claim that "probes run before L1's stop order" (`ConnectDartSymbols.md` §4 heading) cannot be checked: no stop-order record is retained. **[UNKNOWN]**

### SD-11 — info, positive — originals preserved, and committed in the same commit as the admitted envelopes [observed]
- Nine §9 pins match candidate blobs exactly (see Produced files).
- Commit `2b40aec` (author `kaidoku-shokunin <kaidoku@shokunin.local>`, 2026-10-21 11:56:57 -0300, subject "round-23: add sourced offline signal and legacy Dart envelopes", empty body) added the ten connector files, plus L1's envelope, run, download receipt, and the knowledge entry (`git log` for those four paths returns only `2b40aec`). The commit message does not mention the connector files. The disclosure first appears in the same commit at `LOG.md:2634–2636` (`git blame`).
- The unauthorized writes were not removed. They were committed into the production evidence root. Admitted-surface search (`git grep` on candidate, all ten connector hash prefixes plus `ConnectDartSymbols.md`, evidence IDs `ev_dcdab9d0`, `ev_04072bb4`, `ev_5e999884`, `1340303`): no hits outside `LOG.md:2634`, `knowledge:31` (disambiguation text, not a citation), and `lessons:52`.

### SD-12 — info, positive — L1 and connector REA outputs agree except path-derived fields [observed]
- The L1 envelope (sha256 `7768198e…c508`, 87,293 B) is byte-equal to the L1 run's `stdout`.
- `data` of the L1 envelope equals `data` of the connector's 1.33.2 envelope (`7ee2c3c0…84c1`, 87,049 B) except five fields: `evidence_id`; `locations[0].path`; `normalized_result.target.path`; `parameters.path`; `subject.local_path`. `meta.duration` differs (126 ms vs 211 ms). Section table, snapshot hash, sources, coverage, string-pool counts, and limitations are identical.
- Interpretation [INFERENCE]: consistent with a deterministic producer and path-dependent IDs. It does not establish independence from the producer, because both runs used the same rea-agents package.

### SD-13 — binder reading (code only, not executed) [observed code; outcome UNKNOWN]
- Round-22 `count-c1.py` (blob sha256 `c925918f…1879`, equal to round-23 `count-c1.py:23` `LEGACY_SHA256`): `bind_cli` at `:69`; `:74–75` `if not isinstance(envelope, dict) or "ok" not in envelope or "data" not in envelope: return 2`.
- Round-23 `count-c1.py` `bind_new` at `:42–51` walks nodes, then returns `r22.bind_cli(...)`. A document with no top-level `ok` yields 2.
- Therefore the L1 `.run.json` and `legacy-saber-download.json` return 2, and the `== 0` test fails. They are not witnesses.
- The L1 envelope passes the `ok`/`data`/`meta` gates, with `meta.command` = `inspect-dart-aot`. The later `r21.bind` / `CLI_BIND_VERB` step was not read, so **whether the envelope binds is UNKNOWN**.
- `identify-flutter-build` is not bound (0 occurrences, `knowledge:65`). The sentence "Both debugger verbs remain unheld/Adjacent" (`knowledge:66`) is prose. Whether `r20.command_pattern` could match it is **UNKNOWN** (not read).

## Produced files and hashes

This report: `.ufo/waves/round-23/w2/ScopeDeviation.md` (its SHA-256 is reported in the final message, not embedded here).

Candidate blobs relied on (read-only; `sha256` over blob bytes):

| candidate path | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-23/evidence/c1/inspect-dart-legacy-saber.envelope.json` | 7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508 | 87,293 |
| `.ufo/waves/round-23/evidence/c1/inspect-dart-legacy-saber.run.json` | 588460380006a5c1044ba8fb9b8b0136446a2cab5c40e8f2f911978328e82fa6 | 93,379 |
| `.ufo/waves/round-23/evidence/c1/legacy-saber-download.json` | 2e6c00305dfbaf09001c421df6e4cf0730dcce3bfb7a5aa5acc358873da40496 | 511 |
| `…/connect-dart-symbols/inspect-dart-aot-saber-1330203.envelope.json` | 7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1 | 87,049 |
| `…/connect-dart-symbols/inspect-dart-aot-saber-1330203.run.json` | 4b263db8e6060a659f1cf81aab3df025b4014afecdd59258464d57351fe7938d | 1,659 |
| `…/connect-dart-symbols/inspect-dart-aot-saber-1340303.envelope.json` | 22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d | 89,155 |
| `…/connect-dart-symbols/inspect-dart-aot-saber-1340303.run.json` | 34f4ab462e0df49d6f9ff476e619f6bf2e01da750824771da5c8e1e8f78b3db3 | 1,659 |
| `…/connect-dart-symbols/identify-flutter-build-saber-1330203.envelope.json` | 3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626 | 2,663 |
| `…/connect-dart-symbols/identify-flutter-build-saber-1330203.run.json` | 9660b55cc8ed0046f67adace0e75636777c2696e5b111f5b918f9fe196b8cd60 | 1,695 |
| `…/connect-dart-symbols/carriers.json` | 652f05a626078250f617f7f4f3b5d64ca56d286b8654137757a5009ba983f2c6 | 8,670 |
| `…/connect-dart-symbols/fetch.json` | 6beac67b0f6361accc59729c969965b9b8f0f777f5beaca7dd1ed65b11566f2d | 3,033 |
| `…/connect-dart-symbols/preflight_dart_carrier.py` (mode 100755) | 08d0c4605c41f6b091d5b5d09172c5254eaf3bbffa8bf8bcf5f5c7b4b105514c | 7,103 |
| `…/connect-dart-symbols/README.md` (unpinned by connector) | 83de3786f38854a74e3bfaabf8457a68036ddba2b8cc385d27ddb63ab162b05c | 2,359 |
| `.ufo/waves/round-23/w1/ConnectDartSymbols.md` | 5655296d88736a241c6598b250d5fb8ba9b13488996014f5513bf0bb493c2b1c | 20,798 |
| `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` | 22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351 | 4,206 |
| `corpus/lessons/round-23.md` | 8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723 | 9,801 |
| `LOG.md` | 249553811d364458ddf3964446b97c181cb557db203423ff0b40f9d0032163ef | 174,342 |
| `corpus/SOURCES.md` | 736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525 | 62,272 |
| `.ufo/waves/round-23/claims.json` | 249811d9d103960811025d5305422e97271877bec1f470c1601cadc1f40d1906 | 2,386 |
| `.ufo/waves/round-23/tools/describe-dart.py` | 145b09bb734692a371ee6b4971de8a2270547826be840f92d435b40f86a5234f | 2,905 |
| `.ufo/waves/round-23/tools/count-c1.py` | f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2 | 8,382 |
| `.ufo/waves/round-22/tools/count-c1.py` | c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879 | 10,814 |
| `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.run.json` | d1eaa23f96ec4a9695af4f373051da8ad3e87fc3dff3bbee083eed5eaf2eb34a | 1,610 |

Tree identities: `.ufo/waves/round-22/evidence/c1` = `b83fc459dca64a8356480b1ebc8309b4de65de71` at both baseline and candidate. `…/round-23/evidence/c1/connect-dart-symbols` = `84c9b24256d77420f9044edcdde64c2a7f7c817e` at `2b40aec` and at candidate.

## Installs

None. No tool was installed, updated, or configured. The evaluation kernel used Python standard library only (`json`, `hashlib`, `subprocess` for read-only `git`).

## Open risks

1. **Counter not run.** SD-13 is code reading. The Run seat must evaluate the envelope's binding outcome, `r20.command_pattern` against the "debugger verbs" sentence, and the cumulative 4/6 figure. Those outcomes are unverified here.
2. **Runtime APK not re-hashed.** The admitted chain depends on L1's fetch receipt and on the public URL plus digest being reproducible. No admitted index anchor exists (SD-8).
3. **Evidence IDs are path-dependent.** The admitted envelope's `ev_d2ff19d7…` is reproducible only at the absolute runtime path carried in its argv. A replay from another path yields a different ID (SD-12; connector risk 5).
4. **Connector `carriers.json` producer not retained.** Its schema (`kaidoku-r23-dart-carrier-matrix-v1`; top-level keys `schema`, `generated_at_utc`, `producer`, `provider_requirement`, `carriers`, `boundary`) differs from what the retained `preflight_dart_carrier.py` emits (`apk`, `bytes`, `sha256`, `abis`, `rea_6_5_0_expectation`). The matrix cannot be regenerated from retained code. It is unadmitted, so it earns no credit.
5. **Stop-order timing unknown** (SD-10).
6. **Dart version identities** (3.11.4, 3.12.2, 3.13.2) and the 1.36.1 libapp hash appear only in unadmitted connector files. Nothing admitted depends on them.
7. **Peer w2 reports not consulted** to keep this falsification independent of sibling conclusions.
