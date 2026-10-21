# RunAfter: R23-C1 single counter run at candidate 2838351450ff1ee4baa620c962a1153450d53311

Seat: RunAfter, designated counting seat. Leaf; no subagents, no `--selftest`, no fixtures, no suite, no REA replay, no target execution, no installs. Artifacts are under `.ufo/waves/round-23/runtime/RunAfter/`. The private clone was removed after capture.

## Findings

### F1. Counter result [observed]
- Command, run exactly once (`runtime/RunAfter/argv.txt`): `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <private clone> --rev 2838351450ff1ee4baa620c962a1153450d53311`. The cwd was a private clone detached at `2838351450ff1ee4baa620c962a1153450d53311`. `git status --porcelain` was clean. Working-tree `count-c1.py` blob `0f966a50018bba2fa5af3d6f9af1541f660c43c2` matches the candidate tree entry.
- Exit: **1** (`runtime/RunAfter/exit.txt` = `EXIT=1`). This is the script's incomplete code (`count-c1.py:166`, `code = 0 if ... == 6 else 1`). It is not a clean result. stderr is empty.
- Output: `finding: c1_incomplete`, `t1_exercised_count: 4`, `t1_total: 6`.
- **Numerator: 4/6.** Exercised: identify-flutter-build, inspect-dart-aot, inspect-signal-decoders, decode-signal-recording.
- **Exact remainder: debug-with-gdb, debug-with-rizin.** Both have `exercised: false`, `historical: []`, `new: []`.
- Frozen claim: the target of `>=2` is met by the counter's 4 (before=1, observed +3). Completeness at 6/6 is not met, so the result is incomplete.
- The commit title says "four-of-six". This run observed 4; the value was measured here, not assumed.

### F2. Witnesses (all, from `stdout.json` `.targets`) [observed]

Historical, round-22 root. Preserved from baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`. The tree `.ufo/waves/round-22/evidence/c1` is `b83fc459dca64a8356480b1ebc8309b4de65de71` at both baseline and candidate.

| verb | evidence_id | path | blob sha256 |
|---|---|---|---|
| identify-flutter-build | ev_6a84742a9749692a3c6b59678c83d50b4741761f996c723995fa799b1bbca0b6 | .ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json | 143af76e3969c6a79f591115a55b0fd581dfab13a10db5c72fda0b8306f9904b |
| identify-flutter-build | ev_3458b996b71e3dccde0177728ba60ef94800dd373db5a704048e18526d9d866b | .ufo/waves/round-22/evidence/c1/identify-godot.envelope.json | 1ea324b258f06d3f45274eb60f1225f380dcf6ae5adc15e257933c57ea045b0a |

New, round-23 root (`targets[verb].new`). All paths are under `.ufo/waves/round-23/evidence/c1/`:

| verb | evidence_id | path | blob sha256 | citing entry (source row) |
|---|---|---|---|---|
| inspect-dart-aot | ev_d2ff19d7100f34b52e4b2bc52ee115e48428624f7da57814e5f184b4bd4c7491 | inspect-dart-legacy-saber.envelope.json | 7768198e07329ce23d239c39deeaf34b8f2664457aaa7a955f3b328445d4c508 | corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md (S061) |
| inspect-signal-decoders | ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0 | inventory.envelope.json | 5f80218747c3f7c3308adef59216dea9559cada8c93a1ff543ebea6134a43d35 | corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md (S058, S059, S060) |
| decode-signal-recording | ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c | decode-official-uart.envelope.json | 7d5e07cca64ba60aa66ae25b8402ffe70a1bfc49bcce5c9a16f67826f768358e | corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md (S058, S059, S060) |
| decode-signal-recording | ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e | decode-uart-hi.envelope.json | a40c947cf337319411b55c43e8e0270437e29324038a67bacb17232b9311a884 | corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md (S058, S059, S060) |

Source eligibility [observed in `corpus/SOURCES.md` at the candidate]. Rows S058 (line 64), S059 (line 65), S060 (line 66), and S061 (line 67) are `tier A`, `status mined`, `opened 2026-10-21`. Each row's used-by names the citing entry. Each citing entry's first line begins `source:` (`count-c1.py:102`). Eligibility is checked at `:107` and the append is at `:124`.

Acceptance [observed from source]. `bind_new` (`count-c1.py:42-57`) rejects any node with `ok` not true, or any refusal ancestry. `bind_cli` (`round-22/tools/count-c1.py:69-98`) requires `ok` true, `meta.command == verb`, and a record with `evidence_id` and `operation`. The refusal test is `round-21/tools/verb-coverage.py:39-55`. The four new witness envelopes I checked have top-level keys `data`, `meta`, `ok`. All six witnesses were accepted by the script's binder (the script appends only when `bind_new == 0`).

### F3. Remainder: debug-with-gdb and debug-with-rizin [observed + derived]
- Zero witnesses in either root.
- Zero knowledge-entry mentions. The derived scan in F4 gives `t1_mention_files: []` for both verbs.
- No round-23 evidence for either verb. `git ls-tree` of `.ufo/waves/round-23/evidence/c1/` at the candidate lists 18 files, and none is named for these verbs. `git grep -l` for `debug-with-gdb|debug-with-rizin|gdb-console|rizin-debug-command` over evidence/c1, corpus/knowledge, and corpus/lessons returns only `corpus/lessons/round-22.md`. That file is outside the counter's scan set, since the counter scans `corpus/knowledge/` only.
- `decode-invalid-decoder.envelope.json` is present under evidence/c1. It is not among the witnesses. This seat did not inspect it.

### F4. Catalog mentions [observed + derived]
- Counter output: `catalog_mentioned_count: 137`, `catalog_total: 153`, `catalog_zero_count: 16`.
- Derived cross-check: `runtime/RunAfter/derive-mentions.py`. This is read-only and is not a re-run of `count-c1.py`. It reuses the candidate's `command_pattern` verbatim (`.ufo/waves/round-20/tools/verb-coverage.py:99-105`) over the 107 `corpus/knowledge/` files at the candidate. It reproduces 137 / 153 / 16.
- The 16 zero-mention verbs, named by the derivation (`runtime/RunAfter/mentions.json`): inspect-packet-fields, inspect-packet-capture, list-cutter-sessions, cutter-command, debug-with-gdb, debug-with-rizin, list-frida-devices, list-frida-processes, instrument-with-frida, inspect-pcap-client, inspect-pcap-capture, inspect-adb-package, list-adb-services, inspect-adb-window, start-adb-activity, stop-adb-app.
- Mention is not witness. `inspect-dart-aot` is also mentioned by `2026-10-21-r22-flutter-positive-dart-refusal.md`, and `identify-flutter-build` is mentioned by two r22 entries. None of these adds a new witness: the counter's `new` lists contain only the round-23 entries [observed].

### F5. Counter-internal checks [observed by non-error exit path]
- The JSON result was returned with `finding` set, not `unevaluable`. The exit-2 `except` path in `main()` (`count-c1.py:149` onward) was therefore not taken.
- The legacy counter hash `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` equals `LEGACY_SHA256` (`count-c1.py:23`). I confirmed this with `git show … | sha256sum`.
- The pre-checks in `measure()` (`count-c1.py:59-83`) passed. These cover the catalog unchanged from baseline, the historical evidence tree unchanged, prior SOURCES rows preserved, and the baseline historical t1 equal to `[identify-flutter-build]`.

### F6. Source linkage [observed text; admission not assessed by the counter]
- S058 is the sigrok-cli 0.7.2 manual. S059 is the sigrok-dumps UART README at commit `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0`. Both are external.
- S060 is "original REA6.5.0 envelopes in .ufo/waves/round-23/evidence/c1/". S061 is the "original L1 REA6.5.0 inspect-dart-aot envelope and producing record". Both are lane-produced, author-side outputs. S061 cites a public F-Droid APK carrier. This seat did not hash or open that carrier.

## Produced files and hashes
| path (under `.ufo/waves/round-23/`) | sha256 / note |
|---|---|
| runtime/RunAfter/argv.txt | 42d09582aa5aef776d0f830e539fa26517ed14b9b7a0c9a0c3448d20729000fa (295 B) |
| runtime/RunAfter/stdout.json | dcc2d3a2fff54d46212fab81571d653a34179e13b666321cfebbe7dd7bf1766a (2347 B) |
| runtime/RunAfter/stderr.txt | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (0 B) |
| runtime/RunAfter/exit.txt | 4bf4fca02e6eeaf7f1c510b82c756e7f8a3c567a230bae1094b254adc774f38b (`EXIT=1`) |
| runtime/RunAfter/derive-mentions.py | 864470c1644b7f2ea0cf41f9e70007f32f68f47a5838bf312dbb9ae9f805749a (1971 B) |
| runtime/RunAfter/mentions.json | 441d9791718fcea624d295aed12e5e3dc844e270db78e9bbd7059c53b830f7eb (1200 B) |
| runtime/RunAfter/mentions.stderr | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (0 B) |
| runtime/RunAfter/clone (removed) | Created at HEAD 2838351450ff1ee4baa620c962a1153450d53311. Working `count-c1.py` sha256 f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2, equal to blob 0f966a50018bba2fa5af3d6f9af1541f660c43c2. Clean before the run. Removed after capture (`CLONE_REMOVED`). |
| w2/RunAfter.md | this report |

Commands, in order:
1. Read-only candidate checks: `git show`, `git rev-parse`, `git cat-file`, `git grep`, `ls`. No RunAfter artifacts existed before this run.
2. `git clone --no-hardlinks --no-checkout <repo> runtime/RunAfter/clone`, then `git -C clone checkout --detach 2838351450ff1ee4baa620c962a1153450d53311`. Verified HEAD, clean status, and blob hash.
3. Single counter run, `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <clone> --rev 2838351450ff1ee4baa620c962a1153450d53311`, with stdout, stderr, and exit captured. Result: EXIT=1.
4. One read-only derivation, `python3 -I -B derive-mentions.py`. Result: EXIT=0.
5. `rm -rf runtime/RunAfter/clone`. Result: `CLONE_REMOVED`.

The source repo HEAD was re-checked after the run and is still `2838351450ff1ee4baa620c962a1153450d53311`.

## Installs or none
None. Pre-existing Python 3.14.8 and git 2.56.0 were used. No pacman, uv, cargo, npm, or sudo use. No config or routing edits.

## Open risks
1. [observed] Single run by design. Determinism was not re-checked.
2. [inferred] Source admission and relevance are manual. S060 and S061 are author-produced envelopes. The counter does not establish independent admission (the claim's `not_claimed` list).
3. [unknown] The binder internals `r21.bind` and `r21.decode` were not read. Acceptance rests on the counter's `bind_new == 0`. The r22 `revision_helpers` and `measure` bodies (`round-22/tools/count-c1.py:50-66`, `:101-186`) were not read, so the baseline historical re-measurement was not independently re-derived here.
4. [inferred] The remainder is structural. No evidence exists for debug-with-gdb or debug-with-rizin, and no knowledge entry mentions them. The claim boundary excludes live debugger ownership. Whether to add evidence is for L1 to decide. Nothing was done here.
5. [observed] The counter reports catalog mentions as a count only. The 16 names above come from `derive-mentions.py`, which uses the same regex but is not the counter.
6. [observed] Not covered by this seat: the W1 proposal re-evaluation against `2838351450ff…`, named in the wave's Report instructions. It is outside this seat's assigned item and was not performed. No peer report was edited.
7. Reproduction: `git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin <dir>`, then `git -C <dir> checkout --detach 2838351450ff1ee4baa620c962a1153450d53311`, then `cd <dir> && python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <dir> --rev 2838351450ff1ee4baa620c962a1153450d53311`. Expected: exit 1, numerator 4/6.

Report: .ufo/waves/round-23/w2/RunAfter.md
