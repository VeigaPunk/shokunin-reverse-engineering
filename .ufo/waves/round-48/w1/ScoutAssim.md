# ScoutAssim — assimilation census (round 48)

Read-only. Nothing written under `shokuknow/` or into the lane corpus. No install. Scratch removed after this report.

## Answer

**10 of 77** staged knowledge entries already have a lane counterpart **by subject** (filename intersection is **0**). **39** staged registry ids collide with the committed lane registry, and every one of those collisions is a **different document**. Adopting the package **this round** would be **padding**: the round adds no knowledge entry, a blind append would overwrite 39 live ids, and the themes the lane has actually been taking from this package are already re-grounded or refused.

The other **67** entries are not held subjects. They would be knowledge in a coverage round, after renumbering past `S144` and after dropping the held and superseded headlines. They are not adoptable as this package, in this round.

## Id collision

Pattern (the census parser's row rule, `scripts/sources-census.sh` `table_re` `/^ {0,3}\|/`): a line with **0–3 leading ASCII spaces**, then `|`, then field 2 (`gawk -F'|'`) matching `^S[0-9]{3,}$`. Not limited to a `## Registry` heading, because `SOURCES.append.md` has none. Column-zero (`^\|`) and unbounded indent (`^ *\|`) agree on both real files: every id row is at column 0.

| bytes | ids | sha256 | collision with staged |
|---|---|---|---|
| committed `corpus/SOURCES.md` at base `61b87d74`, freeze `dc73587a`, and `HEAD` `663f30ee` (the blob is identical at all three) | 144 (`S001`–`S144`, no gaps) | `ad6ddf4d8aaee0bf406e688e8a16f4b40057686f978f4384e2ab55ea1b93b1ae` | **39** (`S106`–`S144`) |
| staged `SOURCES.append.md` | 132 (`S106`–`S237`, no gaps) | `b82d1276d837867d3a39f56e57a255249802b9d0665b230f1bc87c9424510449` | — |
| worktree `corpus/SOURCES.md` at 2026-10-28T18:56:37Z (`git status` shows `M corpus/SOURCES.md`) | 146 (`S001`–`S146`) | `6bd752cde2337e050d322ec58da578c00365babd554e17592f2c7bd10d3e1b72` | **41** (`S106`–`S146`) |

The count to use is **39**. This seat's first read of the file was the committed 164044-byte blob (144 ids). Two uncommitted rows appeared during the census and are not part of the committed registry:

- worktree `S145` = Stanford Encyclopedia, Karl Popper (`https://plato.stanford.edu/entries/popper/`). Staged `S145` = lane 看雪 Android-board census tsv.
- worktree `S146` = `sysexits(3)`. Staged `S146` = lane REA catalogue-by-version tsv.

`MERGE-REPORT.md` says the lane registry holds **105** rows and the first staged id is `S106`. Against the committed file that is stale: the registry is **144** rows, and `S106`–`S144` are already taken by other documents (squashfs/unblob/AVM/binwalk/git/Python `re`, not the staged rows).

Integer-normalised ids (strip leading zeros) give the same 39: every id on both sides is width 3. Fixture proof that the 0–3 pattern is not the column-zero pattern: rows `| S001 |`, `  | S002 |`, `   | S777 |`, `    | S888 |`, `| S003 |`. The 0–3 extractor returns `S001 S002 S777 S003` and misses the 4-space `S888`. Column-zero returns only `S001 S003`. `^ *\|` also returns `S888`.

Same-URL check on the 39 committed collisions: **0** shared URLs. The documents that were already assimilated sit at **different** ids. Five URLs do occur on both sides, cross-id:

| url | lane id | staged id |
|---|---|---|
| `https://unblob.org/formats` | S116 | S122 |
| `https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` | S111 | S107 |
| `https://github.com/onekey-sec/sasquatch/releases` | S137 | S130 |
| `https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt` | S114 | S192 |
| `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os` | S125 | S216 |

`S114` and `S115` in the package are `queued` lead rows with no knowledge file (`MERGE-REPORT.md`). They still collide as ids (`S114` lane = Freetz AVM-BE note; `S115` lane = rejected 7-Zip row).

## Subject counterparts (10)

Rule used: a staged entry has a lane counterpart when a current `corpus/knowledge/*.md` states the same proposition, or the lane lesson records that file as admitted from this package or as a repeat of held ground. A shared tool name is not a counterpart. Filename stems were not the match key (intersection of basenames is empty; the three re-grounded files use a `2026-10-26-` prefix or a different stem).

| staged file | lane counterpart | relation |
|---|---|---|
| `unblob-sasquatch-dependency.md` | `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` | re-grounded, round 36. Staged `S106`→lane `S110`, staged `S107`→lane `S111`. Lesson `corpus/lessons/round-36.md` Decision 1 |
| `unblob-format-matrix.md` | `corpus/knowledge/2026-10-26-unblob-format-matrix.md` | re-grounded, round 38. Staged `S122`→lane `S116`. Lesson `corpus/lessons/round-38.md` |
| `firmware-region-vocabulary.md` | `corpus/knowledge/2026-10-26-binwalk-v3-unit-of-work.md` | same H1, byte for byte: "binwalk v3 is a Rust rewrite whose unit of work is embedded-data identification". Round 41. Staged `S109`→lane `S129` |
| `avm-image-extraction.md` | `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` | `**Lineage (assimilated)**`; source line names this staged file. Round 40 |
| `sasquatch-prebuilt-package-inventory.md` | `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` | same subject (onekey-sec Debian arch matrix), corrected: staged "each release carries amd64/arm64/armhf" is false for `sasquatch-v1.0`. Refused round 36, admitted as this re-grounding round 43 |
| `sasquatch-unblob-compatibility.md` | `2026-10-26-r36-sasquatch-squashfs-recursion.md`, `…r38-sasquatch-be-squashfs-recursion.md`, `…r39-be-squashfs-v4-core.md` | lesson `corpus/lessons/round-43.md`: the staged candidate "repeats held compatibility ground" |
| `sasquatch-unblob-compatibility-precondition.md` | same held install/compat entries | round 36 Decision 4 and round 38: the "tools are not installed" premise is superseded (binaries present from 2026-10-26) |
| `sasquatch-unblob-avm-branch.md` | `2026-10-26-r40-avm-be-squashfs-core.md` | same rule, stated in the lane entry: `-be` is appended only when `bytes_used == mkfs_time` is false (`S112` lines 44–50). The staged "host has no such tool" clause is stale. Refused rounds 38 and 40 |
| `adb-verb-classification-join.md` | `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` | the staged **Claim** quotes that entry's sentence: 2 of 24 verbs device-free, the other 22 demand a serial. The dispatch-chain half (74 `strcmp`) is extra; the count is held |
| `avm-image-build-blocker.md` | `2026-10-26-r40-avm-be-squashfs-core.md` | superseded, not restated. Staged ground is "whether a real AVM image extracts" and the claim is "one release away". Round 40 rejected it as a stale premise and holds the extraction |

Packager flag `collides_with_existing: false` on every `MERGE-REPORT.json` entry is a **filename** check against an older tree. It does not see these ten.

## Not a counterpart (67)

These have no lane knowledge entry stating the proposition. Near-misses are marked so they are not silently folded into the 10.

**Near-misses (same frontier, different proposition):**

- `adb-host-vs-device-verbs.md` — man page: server-fulfilled vs forwarded to `adbd` (`devices` / `help` / `version`). The lane entry is a REA verb outcome (2/22), not that man page.
- `adb-verb-host-device-alignment.md` — states a **1 + 1 + 17** client classification. The lane states 2 of 24, not this split.
- `adb-verb-host-device-alignment-complete.md` — one local, one host-server, twenty-two device, from client source. Not in the lane entry.
- `rea-adb-operation-vocabulary.md` — cites the lane adb entry and claims five operations that entry never named.
- `recorded-crash-size-ceiling.md` — kernel `RLIMIT_CORE` / `coredump_filter` / piped `core_pattern`. The lane's 32 MiB fact (`2026-10-13-r2-crash-inspect-probe.md`) is REA's input cap, a different mechanism. Same number, not the same subject.
- `managed-assembly-division-of-labour.md` — cites `2026-10-13-r4u-04-dnfile-il.md` and says that entry never states the upstream dnfile/dncil split. The README sentence is the new subject.
- `dnfile-metadata-stream-contract.md` — dnfile's own stream/table contract. Not what the lane's operational dnfile notes state.
- `avm-firmware-image-unblob.md` — production FRITZ!Box image carries both AVM formats and unblob uses ordinary handlers. Round 40 rejected it; lane `S125` is identity of `info_en.txt` only (`corpus/lessons/round-40.md`: "never a layout statement").
- `avm-le-image-genuine-marker.md`, `avm-le-variant-reachability.md` — AVM**_LE**. Round 40 deferred the genuine-marker file for an LE round. No `AVM_LE` claim is in `corpus/knowledge/`.
- `jsc-mapper-cli-contract.md`, `jsc-mapper-release-inventory.md` — `2026-10-13-r4-07-jsc-bytecode.md` names jsc2js as a fallback lead. Round 35 did not admit the frontier (`LOG.md`).
- `android-package-inspection-contract.md` — jadx vs Apktool README contracts. The lane's jadx/apktool notes are operational unlocks, not those READMEs.
- `rea-catalogue-version-join.md` — cites `2026-10-13-rea-cli-surface.md`; the cross-version "same MCP-tool count on 6.5.0 and 6.7.0" is not that catalog.

**No lane subject at all (the rest of the 67), by prefix:**

- adb, beyond the near-misses: `adb-capture-provenance`, `adb-device-conditions-and-states`, `adb-device-conditions-in-english-and-japanese`, `adb-host-prefix-service-split`, `adb-locale-pinned-reference`, `adb-operation-return-values`, `adb-operation-return-values-precondition`, `adb-output-grammar-upstream`, `adb-output-grammar-upstream-remaining`, `adb-output-grammar-dumpsys-package`, `adb-physical-device-route`, `adb-physical-device-conditions-in-japanese`, `adb-second-image-api34`. Distinctive phrases absent from lane knowledge: `?hl=` locale matrix, `mCurrentFocus`, `pm path` / `am force-stop` as upstream grammar.
- dumpsys: `dumpsys-grammar-as-read-in-chinese`, `dumpsys-grammar-in-english-and-chinese`, `dumpsys-window-focus-line-printer`.
- Japanese (16): `japanese-native-literature-shape`, `japanese-static-analysis-toolchain-survey`, `japanese-surface-analysis-command-set`, `japanese-static-analysis-command-set`, `japanese-mcp-ghidra-workflow`, `japanese-independent-rea-evaluation`, `japanese-rea-practitioner-account`, `japanese-rea-topic-frame`, `japanese-adb-mechanism-reading`, `japanese-native-adb-command-reference`, `japanese-no-symbols-reading-workflow`, `japanese-tool-compatibility-friction`, `japanese-dynamic-analysis-command-set`, `japanese-windows-kernel-disassembly-record`, `japanese-rea-topic-frame-counts`, `japanese-rea-frame-qiita-tag-census`.
- Chinese / CJK (6): `chinese-firmware-method-byte-level`, `chinese-static-tool-report`, `chinese-mcp-debug-platform`, `chinese-oem-native-adb-reference`, `chinese-ida-pro-mcp-longform`, `cjk-adb-native-reference-frame`.
- 看雪 (4): `kanxue-original-access-census`, `kanxue-android-board-access-census`, `kanxue-widened-access-census`, `kanxue-digest-archive`. No `看雪` in lane knowledge.
- evidence-graph (6): `rea-evidence-graph-ratio`, `rea-evidence-graph-ratio-real-application`, `rea-evidence-graph-ratio-two-real-applications`, `rea-evidence-graph-scaling`, `rea-evidence-graph-third-application`, `rea-evidence-graph-scaling-driver`. No `12.74` / `552x` in lane knowledge.
- other one-offs: `kernel-core-note-definitions` (no `elf_prstatus`), `offline-lifter-survey-scope`, `lifter-sok-open-artifact`, `binary-lifter-sok-access-routes`, `nul-escape-defect-location`, `rea-adb-operation-vocabulary` (near-miss above).

Staged knowledge files on disk: **77**, all under `merge/kaidoku/knowledge/corpus/knowledge/`. No `amendments/` directory. Lane `corpus/knowledge/*.md`: **138**. `corpus/knowledge` was clean in `git status --porcelain` at the snapshot; only `corpus/SOURCES.md` was dirty.

## Why adoption this round is padding

`plans/round-48-claims.md` lines 16–17: coverage gets no claim; this round adds no domain surface (no knowledge entry, no PROVINCE move, no coverage-map row). The two frozen claims are depth (verdict meanings) and calibration (the record). A knowledge append is outside the round.

Even as a later coverage move, appending `SOURCES.append.md` as staged would not add knowledge cleanly:

1. **39 id collisions, all different documents.** `S106` on the lane is binutils `readelf.c`, not the unblob README the package still calls `S106`. The package's renumber note ("first staged id is S106" because the lane had 105 rows) describes a registry that no longer exists.
2. **The slice the lane has been willing to take is already in.** Five files were re-grounded under new ids (rounds 36, 38, 40, 41, 43). Three more squashfs/AVM headlines were refused as repeats or stale and the corrected fact is in the round-36–40 entries. One adb entry quotes a sentence the lane has held since 2026-10-13. Copying those ten again is duplicate text, and two of them (`sasquatch-prebuilt-package-inventory`, `sasquatch-unblob-compatibility-precondition`, plus the build-blocker) would put a false or superseded headline back.
3. The **67** are real unused subjects (CJK practice, dumpsys grammar, 看雪 access, the evidence-graph ratio, the jsc mapper's release index, locale-pinning). They stay knowledge only if a future coverage round re-opens them under ids past `S144` and drops rows the lessons already refused. That is not this round's surface.

## Receipt

- UTC of the pinned collision extract: `2026-10-28T18:56:37Z` (worktree vs `HEAD`/`base`/`freeze` blobs). Exit 0.
- Command shape: Python, `^ {0,3}\|`, field 2 `^S[0-9]{3,}$`, over the committed blob `git show HEAD:corpus/SOURCES.md` and `SOURCES.append.md`. stdout sha not separately stored; the two input sha256 values above are the evidence. Collision set `S106`–`S144` (39).
- Fixture (scratch, deleted with the scratch dir): 0–3 pattern misses a 4-space row and catches a 2-space and a 3-space row; column-zero misses both indented rows. Exit 0. `2026-10-28T18:56:08Z` for the fixture run.
- `disk-guard.sh status`: **not run**. No clone and no multi-GB pass.
- Installs: none.

## Not run

No re-fetch of staged URLs. No `sources-census.sh validate` (it only counts rows inside `## Registry`, and the append file has no such heading, so it would report 0 staged ids). No mutation of either tree.
