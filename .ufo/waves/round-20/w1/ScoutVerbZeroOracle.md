# ScoutVerbZeroOracle — independent oracle for C2 (CLI verb naming coverage)

Seat `KaidokuR20.ScoutVerbZeroOracle-2`, wave w1, read-only. Written
2026-10-20T17:53:38-03:00 (`date -Iseconds`, clock at write time).

- Baseline `B = 14f0260ad319ecc26994381b2415d5a999003375`; `refs/heads/main =
  d1d981d2cc041dda4656c5b01d2c8445d8d17124` (B + the round-20 declaration commit,
  `.ufo/waves/round-20/*` only).
- Package: `rea-agents 6.5.0` at
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`;
  `dist/cliCommandNames.js` sha256
  `41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3` (observed).
- Scratch (mkdtemp, outside the lane): `/tmp/kr20-VerbZeroOracle.r1fW2T`
  (`oracle.py`, `table.py`, `table2.py`, `sensitivity.py`, `coverage.json`,
  `baseline_run.txt`, `main_run.txt`, `table2.md`). Nothing was written inside
  the lane except this report.

## Verdict (observation)

- `CLI_COMMAND_NAMES` = **153** entries, **153 unique**.
- At B, **128/153** commands are named by at least one corpus markdown entry;
  **25 are zero**.
- `refs/heads/main` gives the same **128/153** and the same 25 zeros (the corpus
  tree is byte-identical between B and main:
  both resolve to `217958c10d35bc2d7ac88954ddeaf139c8f4cf8b`; `git diff --stat
  B refs/heads/main -- corpus` is empty).
- The claims figure `128/153` (`claims.json:27`) reproduces exactly.
- All five C2 target verbs (`claims.json:26`) are in the zero set:
  `inspect-wasm-artifact`, `compare-wasm-interfaces`, `execute-rizin-command`,
  `list-objdump-architectures`, `project-harmony-application-graph`.
  So the target set is 0/5 pre-covered and `>=131` requires at least three of
  them to gain a naming entry.

## Counting rule used

A command is counted when its **hyphen form or its underscore form** occurs at
`B` as a standalone token in a corpus markdown entry. The regex per name
(`<alt>` = the two escaped spellings, longest first):

```
strict: (?<![A-Za-z0-9_-])(?:<alt>)(?![A-Za-z0-9_-])
loose:  (?<![A-Za-z0-9])(?:<alt>)(?![A-Za-z0-9])
```

`strict` refuses a name embedded in a longer hyphen/underscore identifier (e.g.
the file slug `...-inspect-artifact-evidence-id-domain`); `loose` allows the
adjacent `-`/`_`. Case-sensitive. Search is `git grep -P … <REV> -- corpus`
(a hit exits 0, no hit exits 1).

Universes at B (126 `.md` files total): `corpus/knowledge` 97, `corpus/lessons`
26, `corpus/` index 3 (`README.md`, `QUALITY.md`, `SOURCES.md`).

**Boundary mode does not change the result**: strict = loose = 128/153, and the
25 zeros are zero under both. `corpus/knowledge` alone also yields 128/153;
lessons contribute 30 names and the index 61, but **no name is covered only by
lessons or index** (union = 128 = knowledge-only count).

## Decomposition of the 128 (observation; computed, additive)

| tier | count | what it is |
|---|---|---|
| name inside a single-line backtick span, or on a line carrying `npx`/`rea-agents@` | **112** | CLI-shaped naming |
| hyphen form present only as a bare prose token | **14** | all 14 are ADB verbs on `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:83-87` |
| hyphen form absent; only the underscore MCP-tool identifier occurs | **2** | `trace-native-ui-action`, `trace-native-values` — both only at `corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:69` (`isWorkflowEvidenceTool` = `…trace_native_values\|trace_native_ui_action`) |

112 + 14 + 2 = 128. Corollaries: hyphen-form coverage = 126/153; underscore-only
credit = 2/153; 27 names lack the hyphen form entirely (25 zeros + the 2
underscore-only names).

Depth by tier for covered names: 80 have an invocation-shaped anchor, 32 a
backticked anchor, 16 only a plain-token anchor (the 14 ADB + 2 above).

## Zero list (25) — pasteable

```
inspect-packet-fields
inspect-packet-capture
inspect-signal-decoders
decode-signal-recording
compare-wasm-interfaces
inspect-wasm-artifact
list-cutter-sessions
cutter-command
list-objdump-architectures
execute-rizin-command
debug-with-gdb
debug-with-rizin
list-frida-devices
list-frida-processes
instrument-with-frida
inspect-pcap-client
inspect-pcap-capture
identify-flutter-build
inspect-dart-aot
inspect-adb-package
list-adb-services
inspect-adb-window
start-adb-activity
stop-adb-app
project-harmony-application-graph
```

Each of the 25 returns **exit 1 with empty output** for a literal `git grep -F`
and for `-F -i` at `B -- corpus`; they are not boundary artifacts.

Clusters (observation, with corpus context):

- **wasm** (`inspect-wasm-artifact`, `compare-wasm-interfaces`): "WASM" occurs
  only as EVMole 0.9.3 bundling (`corpus/knowledge/2026-10-13-r3-evm-interface.md:6,133`;
  `corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:99,113,138,143`) — no WASM
  verb ground.
- **rizin / gdb / cutter / frida / flutter / dart / harmony**: family words are
  absent (`frida`, `cutter`, `flutter`, `dart`, `harmony` = 0 corpus files).
  `rizin` occurs once, as a *negative* 2026-10-13 claim:
  `corpus/knowledge/2026-10-13-pe-surface.md:65` "PE RE tooling gaps — radare2,
  rizin, mono tools, pedump all absent". The host now has Rizin 0.8.2 at
  `/usr/bin/rizin` (observed: `rizin -v` → `rizin 0.8.2 @ linux-x86-64`, exit 0),
  so that corpus line is stale with respect to the host. The second case-
  insensitive `rizin` hit is the substring in "authori**zin**g"
  (`corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:90`) — a substring false
  positive, not a verb mention.
- **pcap/packet**: `pcap` occurs only inside `cmpcap-*` scratch filenames
  (`corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md:151,157,208,238`);
  "packet" once in firmware prose (`corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:65`).
- **signal**: `signal` is the Signal desktop app, not signal decoding.
- **objdump**: `inspect-with-objdump` and `list-architectures` are covered, but
  `list-objdump-architectures` is a different command; no credit carries over.
- **adb**: the family has **24** CLI names; 19 are named, 5 are zero
  (`inspect-adb-package`, `list-adb-services`, `inspect-adb-window`,
  `start-adb-activity`, `stop-adb-app`). The adb entry's 24-verb census names the
  other 14 verbs in one prose run at `…r4u-06-adb-surface.md:83-87`; the five
  zeros are the verbs that census run omits.

## Calibration notes for the C2 counter (observation unless marked)

1. **Rule-literal 128 is an upper bound on CLI naming.** 16/128 rest on bare
   prose tokens; 14 of those are one comma list in one entry. A conforming
   counter must print 128 at B, but the honest lower bound for CLI-shaped naming
   is 112. The claim already declares "mention-level coverage" as its limit.
2. **Underscore form can credit an MCP identifier, not a CLI verb.** The 2
   `trace-native-*` names are matched only by `trace_native_values` /
   `trace_native_ui_action` inside a source-code constant list. A stricter rule
   (hyphen form mandatory) yields 126/153.
3. **[Inference] The aggregate is gameable without running anything.** All 25
   zeros are already listed in
   `.ufo/waves/luna-round-2/receipts/A6-6.5-help.txt` (verified for all 25) and
   `A6-6.5-llms.txt`. An entry that merely enumerates three of them from
   `--help` would move the aggregate from 128 to 131. The per-target gate
   (`ev_<64 hex>` + an existing path under
   `.ufo/waves/round-20/evidence/c2/`, contract.md:73-75) is the only guard, and
   it applies only to the five named targets — a sixth verb used to pad the
   count is unguarded.
4. **[Inference] "new ground" is corpus-relative, not lane-relative.** Every one
   of the 25 zeros is already named in 5-7 lane files at B (all in
   `.ufo/waves/luna-round-2/**`). That is consistent with the claim's
   "corpus did not hold", but the entry must add run knowledge, not a catalog
   restatement.
5. **Aliases and MCP-only tools are outside the 153.** `CLI_COMMAND_ALIASES` has
   exactly one entry, `compare-bundles`; 65 MCP tools have no dedicated CLI
   command. A corpus mention of `compareBundles` must not be counted for
   `compare-bundles` (and vice versa) under this catalog.

## Commands and exits

```
$ node --version                                                    # exit 0 -> v24.21.0
$ node -e "import('…/dist/cliCommandNames.js').then(m=>console.log(m.CLI_COMMAND_NAMES.length))"
153                                                                 # exit 0
$ sort -u /tmp/…/kr20-verbzero-names.txt | wc -l                    # exit 0 -> 153 (all unique)
$ node -e "console.log(require('…/rea-agents/package.json').version)"
6.5.0                                                               # exit 0
$ sha256sum …/dist/cliCommandNames.js
41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3    # exit 0
$ git -C LANE rev-parse refs/heads/main                             # exit 0 -> d1d981d2…
$ git -C LANE diff --stat B refs/heads/main -- corpus               # exit 0, empty (identical)
$ git -C LANE rev-parse B:corpus ; git -C LANE rev-parse refs/heads/main:corpus
217958c10d35bc2d7ac88954ddeaf139c8f4cf8b  (both)                    # exit 0, exit 0
$ git -C LANE ls-tree -r --name-only B -- corpus/knowledge | grep -c '\.md$'   # exit 0 -> 97
$ git -C LANE ls-tree -r --name-only B -- corpus/lessons   | grep -c '\.md$'   # exit 0 -> 26
$ git -C LANE ls-tree -r --name-only B -- corpus           | grep -c '\.md$'   # exit 0 -> 126
$ git -C LANE grep -P -n -I -e '(?<![A-Za-z0-9_-])(inspect-artifact|inspect_artifact)(?![A-Za-z0-9_-])' B -- corpus
… 65 lines                                                          # exit 0
$ git -C LANE grep -P -n -I -e '(?<![A-Za-z0-9_-])(inspect-wasm-artifact|inspect_wasm_artifact)(?![A-Za-z0-9_-])' B -- corpus
(no output, 0 bytes)                                                # exit 1
$ for v in <25 zeros>; do git -C LANE grep -F -q -e "$v" B -- corpus; echo "$v rc=$?"; done
all 25 print rc=1                                                   # loop exit 0
$ python3 -I -B oracle.py B            # baseline_run.txt
rev 14f0260… md_files 126 names 153
COVERED strict/all 128/153 · strict/knowledge 128/153 · strict/lessons 30/153
COVERED strict/index 61/153 · strict/knowledge+lessons 128/153
(loose identical) · strict-zero count 25                           # exit 0
$ python3 -I -B oracle.py refs/heads/main        # main_run.txt -> 128/153, 25 zeros  # exit 0
$ diff <(zeros main) <(zeros baseline)                              # exit 0 (identical)
$ python3 -I -B sensitivity.py
weak 128/153 · tick 112/153 · invoke 80/153 · either 112/153
weak-only 16 · single-token names 15                                # exit 0
$ awk '/adb/{n++} END{print n}' kr20-verbzero-names.txt             # exit 0 -> 24
$ ls -l /usr/bin/rizin ; rizin -v ; objdump --version
rizin 0.8.2 @ linux-x86-64 ; GNU objdump 2.47                      # exits 0, 0, 0
```

Raw summaries are retained at `/tmp/kr20-VerbZeroOracle.r1fW2T/baseline_run.txt`
and `main_run.txt`; the derived JSON is `coverage.json`
(`strict`/`loose` per name with file:line anchors and `grep_rc`).

## Full table — all 153 names in `CLI_COMMAND_NAMES` export order

`files`/`lines` = distinct corpus files / matching lines at B. `best-tier` is the
strongest naming shape found (`invoke` = on an `npx`/`rea-agents@` line, `tick`
= inside backticks, `plain` = bare token, `-` = uncovered). `first anchor` is
the strongest-tier match, ties broken by path and line.

| # | command | files | lines | best-tier | first anchor |
|---|---|---|---|---|---|
| 1 | `inspect-packet-fields` | 0 | 0 | - | - |
| 2 | `inspect-packet-capture` | 0 | 0 | - | - |
| 3 | `inspect-signal-decoders` | 0 | 0 | - | - |
| 4 | `decode-signal-recording` | 0 | 0 | - | - |
| 5 | `compare-wasm-interfaces` | 0 | 0 | - | - |
| 6 | `inspect-wasm-artifact` | 0 | 0 | - | - |
| 7 | `inspect-sqlite-database` | 3 | 6 | invoke | corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:5 |
| 8 | `inspect-evm-interface` | 14 | 39 | invoke | corpus/knowledge/2026-10-13-r3-evm-interface.md:105 |
| 9 | `inspect-web-network-capture` | 8 | 21 | invoke | corpus/knowledge/2026-10-14-r10-01-queue-ops.md:1 |
| 10 | `observe-web-execution` | 5 | 16 | invoke | corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md:1 |
| 11 | `inspect-web-event-listeners` | 2 | 5 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:185 |
| 12 | `trace-web-source-location` | 2 | 8 | invoke | corpus/knowledge/2026-10-14-r11-01-queue-ops.md:1 |
| 13 | `trace-web-module-imports` | 3 | 11 | invoke | corpus/knowledge/2026-10-14-r11-01-queue-ops.md:1 |
| 14 | `analyze` | 45 | 195 | invoke | corpus/knowledge/2026-10-13-r2-asar-deep-obsidian.md:93 |
| 15 | `inspect` | 28 | 49 | invoke | corpus/knowledge/2026-10-13-r3-appimage.md:75 |
| 16 | `decompile` | 26 | 86 | invoke | corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:139 |
| 17 | `setup` | 11 | 26 | invoke | corpus/knowledge/2026-10-13-doctor-taxonomy.md:70 |
| 18 | `doctor` | 26 | 134 | invoke | corpus/QUALITY.md:18 |
| 19 | `uninstall` | 2 | 6 | invoke | corpus/knowledge/2026-10-13-rea-cli-surface.md:74 |
| 20 | `update` | 6 | 13 | invoke | corpus/knowledge/2026-10-13-r3-renderer-asar.md:107 |
| 21 | `xrefs` | 8 | 30 | invoke | corpus/knowledge/2026-10-13-r3-verb-coverage.md:39 |
| 22 | `trace` | 23 | 46 | invoke | corpus/knowledge/2026-10-13-r3-verb-coverage.md:68 |
| 23 | `trace-native-ui-action` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:69 |
| 24 | `inspect-native-dispatch-metadata` | 4 | 4 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:78 |
| 25 | `capabilities` | 15 | 46 | invoke | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:74 |
| 26 | `providers` | 22 | 69 | invoke | corpus/knowledge/2026-10-13-r2-firmware-probe.md:67 |
| 27 | `function` | 43 | 128 | invoke | corpus/knowledge/2026-10-13-r3-verb-coverage.md:123 |
| 28 | `annotate-native-function` | 6 | 22 | invoke | corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md:1 |
| 29 | `inspect-native-api` | 5 | 18 | invoke | corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md:27 |
| 30 | `instructions` | 12 | 28 | invoke | corpus/knowledge/2026-10-13-r3-verb-coverage.md:146 |
| 31 | `search` | 44 | 124 | invoke | corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:18 |
| 32 | `import-reference-source` | 8 | 20 | invoke | corpus/knowledge/2026-10-14-r10-01-queue-ops.md:1 |
| 33 | `inspect-artifact` | 16 | 65 | invoke | corpus/knowledge/2026-10-13-r3-apk-inventory.md:137 |
| 34 | `extract-artifact` | 7 | 19 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 35 | `decode-interface-builder` | 6 | 13 | invoke | corpus/knowledge/2026-10-13-r3-keyed-archive-carriers.md:56 |
| 36 | `inspect-keyed-archive` | 6 | 18 | invoke | corpus/knowledge/2026-10-13-r3-keyed-archive-carriers.md:22 |
| 37 | `trace-dylib-resolution` | 5 | 12 | invoke | corpus/knowledge/2026-10-13-r3-keyed-archive-carriers.md:81 |
| 38 | `inspect-native-data-type` | 4 | 20 | invoke | corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md:122 |
| 39 | `inspect-native-load-image` | 6 | 16 | invoke | corpus/knowledge/2026-10-13-r7-02-queue-a-ops-2.md:1 |
| 40 | `read-bytes` | 8 | 29 | invoke | corpus/knowledge/2026-10-13-r3-appimage.md:75 |
| 41 | `search-bytes` | 3 | 5 | invoke | corpus/knowledge/2026-10-16-l7-05-search-bytes.md:5 |
| 42 | `address-to-file-offset` | 5 | 12 | invoke | corpus/knowledge/2026-10-13-rea-self-documentation.md:25 |
| 43 | `trace-native-values` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:69 |
| 44 | `inspect-native-instruction` | 7 | 20 | invoke | corpus/knowledge/2026-10-13-r7-02-queue-a-ops-2.md:1 |
| 45 | `resolve-native-call-targets` | 5 | 20 | invoke | corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:27 |
| 46 | `inspect-asset-catalog` | 3 | 4 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:75 |
| 47 | `inspect-managed-artifact` | 9 | 29 | invoke | corpus/knowledge/2026-10-13-r4-11-managed-unlock.md:43 |
| 48 | `inspect-recorded-crash` | 7 | 21 | invoke | corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md:9 |
| 49 | `inspect-binary-layout` | 21 | 64 | invoke | corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:105 |
| 50 | `list-cutter-sessions` | 0 | 0 | - | - |
| 51 | `cutter-command` | 0 | 0 | - | - |
| 52 | `inspect-with-objdump` | 3 | 6 | tick | corpus/README.md:68 |
| 53 | `list-objdump-architectures` | 0 | 0 | - | - |
| 54 | `execute-rizin-command` | 0 | 0 | - | - |
| 55 | `debug-with-gdb` | 0 | 0 | - | - |
| 56 | `debug-with-rizin` | 0 | 0 | - | - |
| 57 | `inspect-go-binary` | 9 | 20 | invoke | corpus/README.md:147 |
| 58 | `inspect-rust-binary` | 4 | 11 | invoke | corpus/README.md:148 |
| 59 | `inspect-pe-resources` | 4 | 8 | invoke | corpus/knowledge/2026-10-13-r2-pe-e2e-proof.md:25 |
| 60 | `inspect-analysis-view` | 10 | 44 | invoke | corpus/knowledge/2026-10-13-r2-asar-deep-obsidian.md:93 |
| 61 | `list-frida-devices` | 0 | 0 | - | - |
| 62 | `list-frida-processes` | 0 | 0 | - | - |
| 63 | `instrument-with-frida` | 0 | 0 | - | - |
| 64 | `inspect-evidence-bundle` | 5 | 18 | invoke | corpus/knowledge/2026-10-13-rea-cli-surface.md:103 |
| 65 | `inspect-firmware-regions` | 9 | 31 | invoke | corpus/knowledge/2026-10-13-r2-firmware-probe.md:28 |
| 66 | `extract-firmware` | 10 | 44 | invoke | corpus/knowledge/2026-10-13-r2-firmware-probe.md:45 |
| 67 | `inspect-android-package` | 10 | 27 | invoke | corpus/knowledge/2026-10-13-r4u-02-jadx-decode.md:30 |
| 68 | `inspect-pcap-client` | 0 | 0 | - | - |
| 69 | `inspect-pcap-capture` | 0 | 0 | - | - |
| 70 | `identify-flutter-build` | 0 | 0 | - | - |
| 71 | `inspect-dart-aot` | 0 | 0 | - | - |
| 72 | `inspect-apktool-client` | 6 | 16 | invoke | corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:61 |
| 73 | `decode-android-resources` | 7 | 23 | invoke | corpus/knowledge/2026-10-13-r4u-02-jadx-decode.md:66 |
| 74 | `inspect-adb-client` | 6 | 16 | invoke | corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:105 |
| 75 | `list-adb-devices` | 6 | 22 | invoke | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:48 |
| 76 | `inspect-adb-device` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:83 |
| 77 | `list-adb-packages` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:84 |
| 78 | `pull-adb-package` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:87 |
| 79 | `read-adb-logcat` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:85 |
| 80 | `inspect-adb-package` | 0 | 0 | - | - |
| 81 | `pull-adb-file` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:87 |
| 82 | `push-adb-file` | 2 | 5 | invoke | corpus/knowledge/2026-10-13-rea-cli-surface.md:67 |
| 83 | `capture-adb-screen` | 1 | 3 | tick | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:93 |
| 84 | `list-adb-processes` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:84 |
| 85 | `list-adb-directory` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:85 |
| 86 | `list-adb-features` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:87 |
| 87 | `list-adb-services` | 0 | 0 | - | - |
| 88 | `inspect-adb-display` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:84 |
| 89 | `inspect-adb-window` | 0 | 0 | - | - |
| 90 | `read-adb-setting` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:85 |
| 91 | `collect-adb-bugreport` | 2 | 4 | tick | corpus/README.md:146 |
| 92 | `resolve-adb-packages` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:86 |
| 93 | `install-adb-package` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:87 |
| 94 | `uninstall-adb-package` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:86 |
| 95 | `start-adb-app` | 1 | 1 | plain | corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:86 |
| 96 | `start-adb-activity` | 0 | 0 | - | - |
| 97 | `stop-adb-app` | 0 | 0 | - | - |
| 98 | `search-android-classes` | 5 | 11 | tick | corpus/knowledge/2026-10-13-r2-skill-references-deep.md:16 |
| 99 | `inspect-android-class` | 5 | 9 | tick | corpus/knowledge/2026-10-13-r2-skill-references-deep.md:16 |
| 100 | `inspect-android-method` | 5 | 9 | tick | corpus/knowledge/2026-10-13-r2-skill-references-deep.md:16 |
| 101 | `trace-android-references` | 5 | 14 | tick | corpus/knowledge/2026-10-13-r2-skill-references-deep.md:16 |
| 102 | `inspect-jeb-client` | 4 | 7 | invoke | corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md:105 |
| 103 | `open-jeb-project` | 1 | 1 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:201 |
| 104 | `list-jeb-units` | 2 | 2 | tick | corpus/knowledge/2026-10-13-r3-verb-coverage.md:168 |
| 105 | `decompile-jeb-item` | 1 | 1 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:201 |
| 106 | `inspect-managed-members` | 9 | 28 | invoke | corpus/knowledge/2026-10-13-r4u-04-dnfile-il.md:56 |
| 107 | `inspect-managed-native-boundaries` | 4 | 11 | invoke | corpus/knowledge/2026-10-13-r4-11-managed-unlock.md:93 |
| 108 | `compare-managed-members` | 5 | 20 | invoke | corpus/knowledge/2026-10-14-r10-01-queue-ops.md:1 |
| 109 | `verify-managed-native-boundaries` | 5 | 16 | invoke | corpus/knowledge/2026-10-14-r9-01-queue-a-ops.md:1 |
| 110 | `import-managed-reconstruction` | 4 | 8 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:204 |
| 111 | `project-managed-application-graph` | 5 | 16 | invoke | corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:1 |
| 112 | `observe-native-ui` | 4 | 4 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:76 |
| 113 | `observe-native-calls` | 6 | 6 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:77 |
| 114 | `capture-native-ui-scenario` | 4 | 4 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:76 |
| 115 | `inspect-macho` | 5 | 8 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:75 |
| 116 | `inspect-signature` | 3 | 3 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:77 |
| 117 | `list-architectures` | 6 | 16 | invoke | corpus/knowledge/2026-10-13-r3-verb-coverage.md:175 |
| 118 | `inspect-plist` | 5 | 13 | invoke | corpus/knowledge/2026-10-13-r3-keyed-archive-carriers.md:110 |
| 119 | `demangle-swift` | 4 | 4 | tick | corpus/knowledge/2026-10-13-r2-frontier-prereqs.md:76 |
| 120 | `evidence-import` | 4 | 9 | tick | corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:24 |
| 121 | `evidence-export` | 7 | 21 | invoke | corpus/knowledge/2026-10-13-rea-cli-surface.md:67 |
| 122 | `compare` | 44 | 140 | invoke | corpus/knowledge/2026-10-13-r4-09-js-export-compare.md:85 |
| 123 | `capture-process` | 4 | 13 | invoke | corpus/knowledge/2026-10-14-r11-01-queue-ops.md:1 |
| 124 | `compare-process-captures` | 3 | 10 | invoke | corpus/knowledge/2026-10-14-r11-01-queue-ops.md:1 |
| 125 | `list-browser-targets` | 9 | 18 | invoke | corpus/knowledge/2026-10-13-r3-runtime-observation.md:20 |
| 126 | `inspect-web-page` | 4 | 11 | tick | corpus/knowledge/2026-10-13-r3-runtime-observation.md:44 |
| 127 | `analyze-web-bundle` | 2 | 6 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:185 |
| 128 | `export-web-scripts` | 4 | 12 | invoke | corpus/knowledge/2026-10-14-r11-01-queue-ops.md:1 |
| 129 | `recover-javascript-sources` | 8 | 23 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 130 | `observe-web-session` | 5 | 16 | invoke | corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md:1 |
| 131 | `discover-webmcp-tools` | 2 | 7 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:185 |
| 132 | `compare-web-captures` | 3 | 9 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:184 |
| 133 | `capture-web-screenshot` | 5 | 7 | tick | corpus/knowledge/2026-10-13-r2-skill-references-deep.md:72 |
| 134 | `compare-web-screenshots` | 2 | 7 | invoke | corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md:155 |
| 135 | `capture-browser-scenario` | 5 | 12 | tick | corpus/knowledge/2026-10-13-r3-runtime-observation.md:99 |
| 136 | `list-electron-targets` | 8 | 17 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 137 | `inspect-electron-page` | 5 | 9 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 138 | `inspect-electron-fuses` | 3 | 7 | invoke | corpus/README.md:149 |
| 139 | `capture-electron-scenario` | 7 | 23 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 140 | `list-javascript-runtime-targets` | 5 | 11 | tick | corpus/knowledge/2026-10-13-r3-runtime-observation.md:173 |
| 141 | `observe-javascript-runtime` | 5 | 14 | tick | corpus/README.md:37 |
| 142 | `analyze-javascript-application` | 22 | 67 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 143 | `reconcile-javascript-runtime` | 9 | 25 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 144 | `trace-application-feature` | 9 | 16 | invoke | corpus/knowledge/2026-10-13-r3-renderer-asar.md:107 |
| 145 | `trace-javascript-semantics` | 7 | 33 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 146 | `compare-application-versions` | 8 | 26 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 147 | `compare-source-to-bundle` | 3 | 13 | invoke | corpus/knowledge/2026-10-13-r8-02-queue-a-ops-2.md:159 |
| 148 | `compare-javascript-export-shapes` | 8 | 30 | invoke | corpus/knowledge/2026-10-13-asar-surface.md:57 |
| 149 | `build-reconstruction-obligation-ledger` | 5 | 13 | tick | corpus/README.md:52 |
| 150 | `evaluate-reconstruction-coverage` | 4 | 14 | tick | corpus/README.md:52 |
| 151 | `project-android-application-graph` | 4 | 11 | tick | corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:199 |
| 152 | `project-apple-application-graph` | 3 | 11 | invoke | corpus/knowledge/2026-10-14-r11-02-queue-ops-2.md:42 |
| 153 | `project-harmony-application-graph` | 0 | 0 | - | - |

## Limits

- **Mention-level only.** A hit proves the spelling occurs in a corpus entry; it
  does not prove the entry describes the CLI verb (the `trace-native-*` and ADB
  prose cases are counterexamples). No semantic check was attempted.
- **Corpus markdown only**, at `B`. `.ufo/waves/**`, `SKILL.md`, `PROVINCE.md`
  and `SCORECARD.md` were deliberately excluded from the count (they are not
  corpus knowledge entries); they were queried only to show the zeros are
  catalog-known elsewhere in the lane.
- **No timestamps are claimed for the corpus content**; the only timestamp in
  this report is its write time from the host clock.
- The 153-name list is the package's export order; it is not sorted
  (`sort -c` fails at `inspect-packet-capture`, line 2).
