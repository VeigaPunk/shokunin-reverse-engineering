# FinalSourceGateScope — landed C1 source-linkage boundary

Seat: `KaidokuR32A2.FinalSourceGateScope-2`. Advisory author-side static review, **not outside admission or a verdict**. Measured revision: `bb0af56c29e7b4c11d0583ed6697d0e17aba9d26`. Observation anchors: 2026-10-23T07:12:19Z; immutable-blob audit started and ended at 2026-10-23T07:14:18Z.

## Axes and result

- **Coverage (R32-C1):** distinguish bounded native-view overview of the twelve pinned synthetic carriers from general ARM64X/EC recovery or Windows validity.
- **Source quality/provenance:** distinguish an actual opened-source/registry/lesson chain from lexical document gates and evidence-ID association.
- **Calibration of the conclusion:** do not promote structural metadata checks, timestamps, or a producer comparison into stronger evidence. C2 remains its existing HONEST STOP; this review does not re-freeze, re-score, or relabel it.

**Observed:** the landed source chain is present, not merely proposed. S099 is on the entry's `source:` line; S098/S099 are new mined/opened rows with the correct used-by entry; S100 is a scoped rejection; the lesson contains its Gate and located quotes; the province row is genuinely under the round-32 Core heading; all twelve entry IDs match the corresponding committed envelopes and carrier SHA values. No missing-link defect was found in these landed files.

**Residual boundary:** neither `entry_ok=1` nor `province_ok=1` independently establishes source existence, source opening, semantic support, or authentic evidence provenance. Those are much narrower lexical checks. Their limitations do not erase the independent landed evidence, but a claim that the bits themselves validate that evidence would be false.

## Counterexample, evidence, impact, smallest safe correction

### Strongest source-gate counterexample — static inference, not an executed mutation

Keep the actual entry, PROVINCE row, pinned carriers and envelopes unchanged, but remove `corpus/SOURCES.md` and the round-32 lesson, or replace S099's registry identity with an unrelated source. The two frozen doc-gate functions receive exactly the same inputs as before and therefore cannot detect this loss of source authority. The counter never reads the registry, lesson Gate, retained source snapshots, opening dates, tier/status, used-by cells, or quotations. This is a counterexample to **semantic-source validation by the doc gates**, not evidence that the actual landed chain is missing and not an observed full P1 false accept.

The smaller lexical witnesses below also follow directly from the frozen branches; they were **not executed**:

```text
entry text:
source: S099 is NOT a supporting source.

PROVINCE text:
## Not Core
| ARM64X | not held | corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md |
```

`entry_ok` only requires the substring `S099`; `province_ok` accepts this heading because it contains `Core` and none of the exact, case-sensitive excluded strings `Frontier|Adjacent|exclusion`. It does not understand the denial or require the canonical `## Core` heading. An ID anywhere in the entry likewise satisfies the committed-record citation test; it is not required to be in a source line or the correct table row.

**Evidence:** `tools/round-32/c1-arm64x-positive.py:123–150,184–223`, SHA-256 `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a`, unchanged from its frozen pin.

**Impacted axes:** source-quality/provenance and calibration of C1's coverage conclusion. The actual twelve-carrier native-view claim must rest on its separate evidence, not semantic strength attributed to these bits.

**Smallest safe correction:** keep the frozen instrument and target unchanged. Describe the gates as lexical linkage conditions and cite the independently opened source evidence separately. The landed entry already does this at lines 34–49, so no source-gate redesign or production edit is requested. If a final summary says the gates validate source truth/authenticity, correct that sentence only. These disclosed instrument limitations are not grounds for silently changing the frozen criterion; only the canonical judge decides whether the bounded evidence suffices.

## Actual landed linkage versus what code checks

| Boundary | Frozen implementation | Independent observation at the measured revision |
|---|---|---|
| Entry source | `entry_ok` at 129–134: entry exists and contains `S099` anywhere | Entry line 1 actually begins `source: S099 (Microsoft Learn, Arm64X PE Files, https://learn.microsoft.com/en-us/windows/arm/arm64x-pe, lines 50–64 of retained source); S098 ...`; this is a real source line, not merely a token elsewhere |
| New mined/opened/used-by rows | Not checked by C1 | `corpus/SOURCES.md:104–105`: S098 and S099 are tier A, `mined`, opened `2026-10-23`, recheck `on-release`, used-by `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md`. Parent-to-landed diff adds them; it does not alter an existing source row |
| Rejected source | Not checked by C1 | SOURCES line 106: S100 is `rejected`, same opened date, used-by `corpus/lessons/round-32.md`, with an explicit conjunctive flip for the missing offset/tag scope |
| Lesson Gate | Not checked by C1 | `corpus/lessons/round-32.md:14–31` contains the Gate, scoped admits/reject, opening dates, URLs, located quotes and snapshot identities; line 19 explicitly says no outside spot-check was performed |
| Core placement | `province_ok` at 137–150: first matching pipe-started row contains `ARM64X` and the entry path; nearest preceding `#{1,6} ` heading contains `Core`, excludes three case-sensitive strings | Matching row is line 357; actual governing heading at line 353 is `## Round-32 additions to Core (verified 2026-10-23)`. Row explicitly excludes dual-view recovery, decompilation and execution; Frontier at 82–83 retains the broader gaps |
| IDs and association | `committed_check` at 109–126: JSON object equality to live envelope excluding only top-level `meta`; live `data.evidence_id` must occur anywhere in entry | Independently read all 12 committed JSON blobs: each ID occurs exactly once and in its own unique `kNN` entry row; each subject SHA equals the roster and the SHA in that row; each stored procedure count equals its frozen prediction. All stored envelopes say `ok:true`, operation `binary_overview`. Full raw output below retains every ID/hash |

The equality check is **parsed-object equality**, not byte-for-byte stdout equality: JSON whitespace/member order need not match. Only top-level `meta` is removed. It establishes record association, not cryptographic authenticity. This static review did not compare any committed envelope to a newly live reader result; it therefore does **not** report a fresh C1 measurement or target pass.

## What the opened sources support — and do not

I reopened the retained source bytes and reports at the measured revision; **I did not make a fresh network fetch**. Historical HTTP/fetch outcomes below belong to the named committed source-opening report, not this seat.

- **S099:** Microsoft Learn <https://learn.microsoft.com/en-us/windows/arm/arm64x-pe>. Retained Markdown `corpus/evidence/round-32/sources/arm64x-pe.md`, SHA-256 `a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66`, 7,386 bytes. Line 50: “Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together.” Line 64: “By default, Arm64X binaries appear to be Arm64 binaries.” This supports hybrid definition/default-view interpretation, **not** per-carrier code content, the CHPE offset/tags, a Ghidra result, or Windows acceptance. `.ufo/waves/round-32/a2audit/A2SourcesPrimary.md:47–78` retains the HTTP 200 capture commands, sizes and digests.
- **S098:** pinned LLVM `llvmorg-23.1.3` inputs, <https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s> and paired `loadconfig-arm64.s`. Retained input hashes are `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4` (2,686 bytes) and `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d` (423 bytes), equal to frozen pins. ARM64EC line 20 is `.xword __chpe_metadata`; lines 63–65 are `.word 2`, `.rva __hybrid_code_map`, `.word __hybrid_code_map_count`. These are upstream **input references**, not populated linked-map proof or a reader outcome. `A2SourcesPrimary` reports its fetches; `A2BuildRecheck` separately supplies a repeated dual-object build and LLVM hybrid-view witness.
- **S100:** <https://learn.microsoft.com/en-us/windows/win32/debug/pe-format> and <https://raw.githubusercontent.com/MicrosoftDocs/win32/docs/desktop-src/Debug/pe-format.md>. Retained HTML/Markdown hashes are `d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1` and `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0`. My bounded census found **0** case-insensitive occurrences of each `CHPEMetadataPointer`, `CodeMap`, `0xC8` in both snapshots. Markdown line 131 does define ARM64X coexistence; the load-config table at 1930–1961 ends at `GuardLongJumpTargetCount` (offset cell `116/184`, size `4/8`). A machine-type description is not an offset/tag definition. This supports the **scoped rejection**, not universal absence from all Microsoft documentation. The lesson's flip still requires both reopened representations to supply both missing facts.

## Required classifier and ordering limitations

### CHPE metadata-only forgery

Observed source: `arm64x_oracle.py:79–109` obtains a pointer at load-config `+0xC8`, reads metadata map RVA/count and low-two-bit range tags, and requires machine `0xAA64` plus types ARM64 and ARM64EC. The metadata version is unpacked into `_`, not validated. It does not decode instructions or establish EC ABI content, loader validity, range containment/overlap, or execution.

The strongest retained local counterexample is `.ufo/waves/round-32/a2audit/A2CHPEBits.md:58–72`: that seat reports a pure-AArch64-only build with forged metadata, SHA-256 `1542e5102fbb42e7c951d3e1ee27373824c3fd8e80ee6adf2174dac24efbc7f9`, 3,072 bytes, for which the frozen classifier returned `arm64x:true`. This is **attributed prior-seat evidence**, not a fixture opened, built or run by this seat. Its reported classification was:

```text
machine=0xaa64
code_map=[{type:ARM64,start:0x1000,length:32},{type:ARM64EC,start:0x1010,length:16}]
arm64x=true
```

This falsifies interpreting the classifier alone as proof of valid EC code. It does **not** demonstrate an end-to-end false acceptance by the frozen twelve-carrier P1: the forged DLL is not in the pinned SHA roster, and that seat explicitly did not run REA on it. The actual carriers have separate reported dual-target build reproduction (all twelve frozen hashes) and an LLVM dual-view witness (`A2BuildRecheck:40–87,89–168`). That witness is independent of the lane Python oracle/REA, not independent of the builder's LLVM release and not a Windows-loading proof. No new reproduction was authorized here.

Smallest safe correction is scope discipline already reflected in entry lines 34–37: **declared structural classification plus the separate build witness for these carriers**, never generic semantic validation or coverage saturation. Do not change the frozen classifier.

### First-added timestamp proxy

Observed source: counter `first_added:103–106` runs `git log REV --diff-filter=A --format=%ct -- PATH` and takes the minimum committer timestamp. `measure:184–186` does the same for `claims.json`; `committed_check:114–116` requires envelope minimum `> freeze_ct`. It does not compare ancestry or prove that the envelope was absent at the freeze.

- **Observed actual history:** claims has one add event, `9a73680af21b002e3b99956c89234b2bbde2a71b`, `%ct=1792735426` = **06:03:46Z**. Each of the twelve envelopes has one add event at measured commit `bb0af56c...`, `%ct=1792739183` = **07:06:23Z**. Actual timestamp gap is **3,757 seconds**. An independent `merge-base --is-ancestor` command returned exit 0 for freeze → measured revision. The current linkage does not exhibit an inverted/equal clock.
- **Inference from the code, not newly exercised:** a true descendant added in the same second or with a backdated committer clock can fail; a pre-freeze add with a future committer clock can satisfy the proxy. Taking the minimum across multiple adds also does not identify the relevant DAG event. Prior bounded experiments are retained in `A2LivePredicate:44–62,95–118`; this review does not rerun them.

Smallest safe correction: report the proxy exactly and retain the independently observed actual history/UTC; do not call the proxy a DAG proof and do not amend the frozen counter.

## Exact exercised commands and outputs

All shell commands used cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, timeout 60 seconds except the static audit (120 seconds). No shell command failed; all exited 0 and had empty stderr. Direct `read`/`grep`/`glob` tool calls supplied the scoped source excerpts above. No frozen predicate/function, REA, selftest, build, carrier execution, external runtime, git/jj write, clone, package installation/update, routing or MANIFEST operation was performed. No owned background job or service was started; finite subprocesses completed before this report.

### A. Revision/UTC identity

Exact command:

```sh
date -u +%Y-%m-%dT%H:%M:%SZ && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show -s --format=fuller bb0af56c29e7b4c11d0583ed6697d0e17aba9d26
```

Exit 0. Stdout:

```text
2026-10-23T07:12:19Z
bb0af56c29e7b4c11d0583ed6697d0e17aba9d26
bb0af56c29e7b4c11d0583ed6697d0e17aba9d26
commit bb0af56c29e7b4c11d0583ed6697d0e17aba9d26
Author:     kaidoku-shokunin <kaidoku@shokunin.local>
AuthorDate: Fri Oct 23 03:56:11 2026 -0300
Commit:     kaidoku-shokunin <kaidoku@shokunin.local>
CommitDate: Fri Oct 23 04:06:23 2026 -0300

    round-32: bounded ARM64X native-view evidence, source gate and faithful repertoire repair
```

### B. Static immutable-blob audit

Exact command:

```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceGateScope/static_linkage_audit.py && sha256sum /fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceGateScope/static_linkage_audit.py
```

Exit 0. This script only reads immutable Git blobs/history and parses document/JSON fields; it imports or executes no product code. Exact stdout, including all script/input hashes and IDs:

```text
{"kind": "start", "revision": "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26", "utc": "2026-10-23T07:14:18+00:00"}
{"bytes": 8341, "kind": "input", "path": ".ufo/waves/round-32/claims.json", "sha256": "8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435"}
{"bytes": 13235, "kind": "input", "path": "tools/round-32/c1-arm64x-positive.py", "sha256": "7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a"}
{"bytes": 6166, "kind": "input", "path": "tools/round-32/arm64x_oracle.py", "sha256": "17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686"}
{"bytes": 1845, "kind": "input", "path": "tools/round-32/build-arm64x-carriers.sh", "sha256": "7da284da5986295263c69a8b7ee779638428d3bb6c9d5c9d8fb224c40a737ba3"}
{"bytes": 7523, "kind": "input", "path": "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md", "sha256": "2fe3ce11dfdc674be8934e9a0c6c614baebee0fd1e74f0fbdb81ca76b4be9229"}
{"bytes": 117661, "kind": "input", "path": "corpus/SOURCES.md", "sha256": "c11efc0c11ceb85bcdaf5e28ab0cf45caafefe5e84ec7e3a8f5bdef0068db942"}
{"bytes": 41492, "kind": "input", "path": "PROVINCE.md", "sha256": "dc42da24b744c00cf61fd60577f5057a350700f8c3e283a183908db6cc2392b2"}
{"bytes": 10747, "kind": "input", "path": "corpus/lessons/round-32.md", "sha256": "a6eea0b454150269b83d717dd47963e0deb178a6f084f76a1498ad9c3e495ee6"}
{"bytes": 2687, "kind": "input", "path": "corpus/evidence/round-32/c1/carriers.tsv", "sha256": "8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e"}
{"bytes": 1643, "kind": "input", "path": "corpus/evidence/round-32/c1/predictions.tsv", "sha256": "fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b"}
{"bytes": 3399, "kind": "input", "path": "corpus/evidence/round-32/c1/runs.tsv", "sha256": "62df49f73c3a8da0caa94b4e93711edcb5bc21e30e77f79b8043d98a6e2856b9"}
{"bytes": 423, "kind": "input", "path": "corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s", "sha256": "7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d"}
{"bytes": 2686, "kind": "input", "path": "corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s", "sha256": "c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4"}
{"bytes": 7386, "kind": "input", "path": "corpus/evidence/round-32/sources/arm64x-pe.md", "sha256": "a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66"}
{"bytes": 335441, "kind": "input", "path": "corpus/evidence/round-32/sources/pe-format.md", "sha256": "b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0"}
{"bytes": 282123, "kind": "input", "path": "corpus/evidence/round-32/sources/pe-format.html", "sha256": "d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1"}
{"bytes": 8812, "kind": "input", "path": ".ufo/waves/round-32/a2audit/A2SourcesPrimary.md", "sha256": "40b20f3886812ebc2baf32c7a8a6c890c016e883cf3155137da48cdf6abad6c6"}
{"bytes": 11235, "kind": "input", "path": ".ufo/waves/round-32/a2audit/A2SourceReject.md", "sha256": "bf7e5fa77da1217dd8847923e7f62c3e9a2a1566edaed461090aa9896fec7b47"}
{"bytes": 12655, "kind": "input", "path": ".ufo/waves/round-32/a2audit/A2CHPEBits.md", "sha256": "e5a40700866e6bf9ffb570a3964021444f856edba1e5a1f28972c9bfef8181da"}
{"bytes": 12624, "kind": "input", "path": ".ufo/waves/round-32/a2audit/A2BuildRecheck.md", "sha256": "f37b6cf0316943b76d55413725057490f83425448e11188bf9c493991f98876c"}
{"bytes": 13936, "kind": "input", "path": ".ufo/waves/round-32/a2audit/A2LivePredicate.md", "sha256": "f0af1c0174b0fd4fe6d36f2a5feb935053394d2ac1dc11905ffad6421c22d6ee"}
{"equal": true, "kind": "frozen_pin", "path": "tools/round-32/c1-arm64x-positive.py"}
{"equal": true, "kind": "frozen_pin", "path": "tools/round-32/arm64x_oracle.py"}
{"equal": true, "kind": "frozen_pin", "path": "tools/round-32/build-arm64x-carriers.sh"}
{"equal": true, "kind": "frozen_pin", "path": "corpus/evidence/round-32/c1/carriers.tsv"}
{"equal": true, "kind": "frozen_pin", "path": "corpus/evidence/round-32/c1/predictions.tsv"}
{"equal": true, "kind": "frozen_pin", "path": "corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s"}
{"equal": true, "kind": "frozen_pin", "path": "corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s"}
{"kind": "entry_source_line", "line": 1, "value": "source: S099 (Microsoft Learn, Arm64X PE Files, https://learn.microsoft.com/en-us/windows/arm/arm64x-pe, lines 50\u201364 of retained source); S098 (LLVM llvmorg-23.1.3 load-config assembler inputs); original REA envelopes and producing argv/package identities in corpus/evidence/round-32/c1/runs.tsv"}
{"columns": 11, "id": "S098", "kind": "source_row", "line": 104, "opened": "2026-10-23", "recheck": "on-release", "status": "mined", "used_by": "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"}
{"columns": 11, "id": "S099", "kind": "source_row", "line": 105, "opened": "2026-10-23", "recheck": "on-release", "status": "mined", "used_by": "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"}
{"columns": 11, "id": "S100", "kind": "source_row", "line": 106, "opened": "2026-10-23", "recheck": "on-release", "status": "rejected", "used_by": "corpus/lessons/round-32.md"}
{"heading": "## Round-32 additions to Core (verified 2026-10-23)", "kind": "province_link", "line": 357, "row": "| ARM64X hybrid PE through REA 6.5.0 `inspect` | Native-view `binary_overview` on twelve pinned, author-built exported-leaf DLLs; raw COFF 0xAA64 plus CHPE ARM64/ARM64EC ranges; ordered segments and native-view procedure counts checked against the frozen byte oracle and predictions. Not dual-view recovery, decompilation or execution | `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` |"}
{"kind": "lesson_gate_heading", "line": 14, "value": "## Gate"}
{"counts": {"0xC8": 0, "ARM64EC": 2, "ARM64X": 1, "CHPEMetadataPointer": 0, "CodeMap": 0}, "kind": "bounded_source_census", "path": "corpus/evidence/round-32/sources/pe-format.md"}
{"counts": {"0xC8": 0, "ARM64EC": 2, "ARM64X": 1, "CHPEMetadataPointer": 0, "CodeMap": 0}, "kind": "bounded_source_census", "path": "corpus/evidence/round-32/sources/pe-format.html"}
{"events": ["9a73680af21b002e3b99956c89234b2bbde2a71b 1792735426 2026-10-23T03:03:46-03:00"], "kind": "claims_add_events"}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_d7fe3164aef68b83604ff240aaa7cea64ce097fbe0780dbe9b1f88d8431a1bdf", "id": "k01", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k01.json", "procedure_count": 1, "procedure_equals_prediction": true, "sha256": "c43239a6f39156cd2a7dc48d62ce12f7fc1d1b476f07b4688bbb578e249c0146", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_032c2af47055785b6668265ce05feaf6fc9a28f211fef43a8489eb303c0d6699", "id": "k02", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k02.json", "procedure_count": 2, "procedure_equals_prediction": true, "sha256": "8023185af8976d2451fdd35eac0214cf28deb0b682276942873f680b84116d00", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_7d983639597236a8c25133a01fe6364a7ef12ab08fadde7663b7ec76dd50a183", "id": "k03", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k03.json", "procedure_count": 3, "procedure_equals_prediction": true, "sha256": "ca5365457ace7b7210f5e792b29058793e5d776412b4231699403d8c917b05bb", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_0a5879b6962d52807bf842ab2fc5a2c5b801c425a76c1996c478dec5cf31b57a", "id": "k04", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k04.json", "procedure_count": 4, "procedure_equals_prediction": true, "sha256": "c9c0c1a332332ff6b16172864a18e11dc4f95cc092a720ecbe529a6849a43692", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5248, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_fec48cb3a4bee51c883fb18ae569f6ceffc0e7f3251c048af095ee479f23bee5", "id": "k05", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k05.json", "procedure_count": 1, "procedure_equals_prediction": true, "sha256": "8a945d4812794f045935573ff39d6c56ebe7b59942a4a023d99174f6916a0ffd", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5248, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_2b7fb69a2e46eb319841d9783d7e00dbe6b65c9a9ea58bb8a70b3dca687c9a34", "id": "k06", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k06.json", "procedure_count": 5, "procedure_equals_prediction": true, "sha256": "cf4b0af0324e21c32b27fda8ca285c10dae07449235fc8a34e2c2f2694b42446", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5248, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_d2cc4361b7c8c897dad143d207d019ab2fed8875acabeb25633b85ca94cd9570", "id": "k07", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k07.json", "procedure_count": 6, "procedure_equals_prediction": true, "sha256": "6e8c26f19c389e184d9bc009cb80b498f6546b3de4621edf791e5814becd42dc", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_8642af3e9c8bc5aa55e7764fd5a7972d4a37adc340ed55c17f4fbbf6edfbe61e", "id": "k08", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k08.json", "procedure_count": 2, "procedure_equals_prediction": true, "sha256": "9a997df19345119b166df60292fbe478d428184eb1c43a0f9814cce0b0ca3f62", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_3cd5776b21c117cdd9b9b0298d20edae5c02b9933f2b1fdde93de266f0ae98dc", "id": "k09", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k09.json", "procedure_count": 7, "procedure_equals_prediction": true, "sha256": "b32ce2cbed1e4159a82330130891a156ed0c56ba5e578f249543b116529560a8", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_63b7f3d4aecbd0e560c0d809ea83f4261900855ff7c5598a92dcc3204e99eebf", "id": "k10", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k10.json", "procedure_count": 3, "procedure_equals_prediction": true, "sha256": "be6f38646b6d5783b25d968be4784009230fefdad9ec941ff6411dc1b815fccd", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5248, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_85d09ca4512cdea17c18dbb20935d1c627cfd189809e04e448cab07ee8a715af", "id": "k11", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k11.json", "procedure_count": 8, "procedure_equals_prediction": true, "sha256": "3fc5e5b0a4a1fed7b8d6eb3574ac1fd72c797532d6e71703852a1bd3975616c4", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"add_events": ["bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 1792739183 2026-10-23T04:06:23-03:00"], "bytes": 5247, "entry_id_occurrences": 1, "entry_unique_carrier_row": true, "evidence_id": "ev_9a2cd4a45022eecf01ce6d46ff8fbcbbec1c64fa0c6c4151b45009cafd3338a1", "id": "k12", "id_in_carrier_row": true, "kind": "envelope_link", "ok": true, "operation": "binary_overview", "path": "corpus/evidence/round-32/c1/envelopes/k12.json", "procedure_count": 1, "procedure_equals_prediction": true, "sha256": "c7062ab2bfe627e62742832ff49685af2253ab1e1fc0f0ac1ca9125de6277e16", "sha_in_carrier_row": true, "subject_sha_equals_roster": true}
{"carrier_rows": 12, "immutable_blobs": 33, "kind": "end", "utc": "2026-10-23T07:14:18+00:00"}
e98cfe68631da30cf2477a00a56f4228f9851ebd8c094a20980c66c60c8312e9  /fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceGateScope/static_linkage_audit.py
```

### C. Independent actual ancestry

Exact command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 9a73680af21b002e3b99956c89234b2bbde2a71b bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 && printf 'freeze_is_ancestor_of_landed_revision=true\n'
```

Exit 0. Stdout:

```text
freeze_is_ancestor_of_landed_revision=true
```

### D. New source rows, not edits to old authority

Exact command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --unified=0 bb0af56c29e7b4c11d0583ed6697d0e17aba9d26^ bb0af56c29e7b4c11d0583ed6697d0e17aba9d26 -- corpus/SOURCES.md
```

Exit 0. Exact raw stdout (tool's presentation summary was not substituted for these bytes):

```diff
diff --git a/corpus/SOURCES.md b/corpus/SOURCES.md
index e9e8ff28..534796dc 100644
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -103,0 +104,3 @@
+| S098 | LLVM lld COFF ARM64 and ARM64EC load-config test inputs (llvmorg-23.1.3) — https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64ec.s; https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-23.1.3/lld/test/COFF/Inputs/loadconfig-arm64.s | code | A | Upstream assembler inputs used by the round-32 synthetic hybrid carrier builder; not linked carrier bytes or Windows/REA behavior | LLVM llvmorg-23.1.3; fetched 2026-10-23; SHA-256 `c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4` and `7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d`; ARM64EC lines 20, 59–67; ARM64 lines 1–15 | Pin the upstream load-config inputs; CHPE/hybrid-map references are structural evidence, not proof of populated linked ranges or reader success. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md |
+| S099 | Microsoft Learn, Arm64X PE Files — https://learn.microsoft.com/en-us/windows/arm/arm64x-pe | docs | A | Microsoft's hybrid Arm64/Arm64EC definition and default Arm64 appearance; not a specific carrier layout or REA/Ghidra capability | Served Markdown fetched 2026-10-23; page ms.date 2025-11-06; SHA-256 `a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66`; lines 50–64 of `corpus/evidence/round-32/sources/arm64x-pe.md` | Distinguish hybrid content from a machine-value-only label and native-view appearance from dual-view recovery. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md |
+| S100 | Microsoft PE Format specification — https://learn.microsoft.com/en-us/windows/win32/debug/pe-format | spec | A | Candidate authority for CHPEMetadataPointer offset 0xC8 and code-map bit tags only | Opened 2026-10-23; served HTML SHA-256 `d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1`; MicrosoftDocs/win32 docs Markdown SHA-256 `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0`; Machine Types line 131; Load Configuration Layout lines 1926–1961; retained under corpus/evidence/round-32/sources | REJECTED: both searched representations omit CHPEMetadataPointer, CodeMap and 0xC8; a machine-type definition does not teach the offset/tags. flip: later versions of both representations explicitly document the CHPE field at PE32+ offset 200/0xC8 and numeric range-tag bit meanings. | rejected | 2026-10-23 | on-release | corpus/lessons/round-32.md |
@@ -125,0 +129 @@
+- ARM64X native-view boundary — S099 → S098: first learn the hybrid/default-view distinction, then bind the synthetic load-config inputs. S100 is rejected only for the missing CHPE offset/tag scope; neither documentation source establishes a REA result.
@@ -176,0 +181 @@
+- 2026-10-23 round 32 — Question: which primary sources support the hybrid/default-view interpretation and synthetic build inputs, and does the PE Format spec define CHPE offset/tag details? Opened Microsoft Arm64X documentation, LLVM llvmorg-23.1.3 paired assembler inputs, and the Microsoft PE Format specification (three source families identified/screened). Included two as mined S098/S099; retained one scoped rejection S100 because the searched field/tag definitions are absent. `.ufo/waves/round-32/a2audit/A2SourcesPrimary.md` and `.ufo/waves/round-32/a2audit/A2SourceReject.md` retain bounded searches, quotes and source identities. Stop: definition/input provenance answered; reader behavior rests on live envelopes. Existing rows unchanged.
@@ -186,0 +192 @@
+
```

## Audit script bytes

The following is the complete 5,498-byte scratch script whose SHA-256 is recorded above. All evidence inputs are committed at the measured revision; this report embeds the script and its output so no claim depends solely on a scratch/artifact citation.

```python
#!/usr/bin/env python3
"""Read immutable Git blobs; inventory source/entry links without running lane code."""
import csv
import datetime
import hashlib
import io
import json
import os
import subprocess

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "bb0af56c29e7b4c11d0583ed6697d0e17aba9d26"
CLAIMS = ".ufo/waves/round-32/claims.json"
ENTRY = "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
C1 = "corpus/evidence/round-32/c1/"
AUDIT = ".ufo/waves/round-32/a2audit/"
ENV = {k: v for k, v in os.environ.items()
       if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
CACHE = {}


def git(*args):
    argv = ["git", "-C", ROOT, *args]
    p = subprocess.run(argv, env=ENV, capture_output=True, timeout=30)
    if p.returncode:
        raise RuntimeError(json.dumps({"argv": argv, "exit": p.returncode,
                                      "stdout": p.stdout.decode(), "stderr": p.stderr.decode()}))
    return p.stdout


def blob(path):
    if path not in CACHE:
        data = git("show", REV + ":" + path)
        if len(data) > 1048576:
            raise ValueError("blob exceeds 1 MiB: " + path)
        CACHE[path] = data
    return CACHE[path]


def text(path):
    return blob(path).decode("utf-8")


def emit(kind, **fields):
    print(json.dumps({"kind": kind, **fields}, sort_keys=True))


emit("start", utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
     revision=git("rev-parse", REV).decode().strip())
paths = [CLAIMS, "tools/round-32/c1-arm64x-positive.py", "tools/round-32/arm64x_oracle.py",
         "tools/round-32/build-arm64x-carriers.sh", ENTRY, "corpus/SOURCES.md", "PROVINCE.md",
         "corpus/lessons/round-32.md", C1 + "carriers.tsv", C1 + "predictions.tsv", C1 + "runs.tsv",
         C1 + "inputs/loadconfig-arm64.s", C1 + "inputs/loadconfig-arm64ec.s",
         "corpus/evidence/round-32/sources/arm64x-pe.md",
         "corpus/evidence/round-32/sources/pe-format.md",
         "corpus/evidence/round-32/sources/pe-format.html"]
paths += [AUDIT + n + ".md" for n in
          ("A2SourcesPrimary", "A2SourceReject", "A2CHPEBits", "A2BuildRecheck", "A2LivePredicate")]
for path in paths:
    data = blob(path)
    emit("input", path=path, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
claims = json.loads(text(CLAIMS))
for path, expected in {**claims["instruments"], **claims["frozen_inputs"]}.items():
    if path in CACHE:
        emit("frozen_pin", path=path, equal=hashlib.sha256(blob(path)).hexdigest() == expected)
entry = text(ENTRY)
for number, line in enumerate(entry.splitlines(), 1):
    if line.startswith("source:"):
        emit("entry_source_line", line=number, value=line)
registry = text("corpus/SOURCES.md")
for number, line in enumerate(registry.splitlines(), 1):
    cells = [c.strip() for c in line.strip().split("|")[1:-1]]
    if cells and cells[0] in ("S098", "S099", "S100"):
        emit("source_row", line=number, id=cells[0], status=cells[7], opened=cells[8],
             recheck=cells[9], used_by=cells[10], columns=len(cells))
heading = ""
for number, line in enumerate(text("PROVINCE.md").splitlines(), 1):
    if line.startswith("#"):
        heading = line
    if line.startswith("|") and "ARM64X" in line and ENTRY in line:
        emit("province_link", line=number, heading=heading, row=line)
for number, line in enumerate(text("corpus/lessons/round-32.md").splitlines(), 1):
    if line == "## Gate":
        emit("lesson_gate_heading", line=number, value=line)
for path in ("corpus/evidence/round-32/sources/pe-format.md",
             "corpus/evidence/round-32/sources/pe-format.html"):
    body = text(path).lower()
    emit("bounded_source_census", path=path,
         counts={token: body.count(token.lower()) for token in
                 ("CHPEMetadataPointer", "CodeMap", "0xC8", "ARM64X", "ARM64EC")})
freeze_events = git("log", REV, "--diff-filter=A", "--format=%H %ct %cI", "--", CLAIMS).decode().splitlines()
emit("claims_add_events", events=freeze_events)
rows = list(csv.DictReader(io.StringIO(text(C1 + "carriers.tsv")), delimiter="\t"))
predictions = {r["id"]: r for r in csv.DictReader(io.StringIO(text(C1 + "predictions.tsv")), delimiter="\t")}
for row in rows:
    cid = row["id"]
    path = C1 + "envelopes/" + cid + ".json"
    data = blob(path)
    envelope = json.loads(data)
    payload = envelope["data"]
    eid = payload["evidence_id"]
    linked_rows = [line for line in entry.splitlines() if line.startswith("| " + cid + " |")]
    linked = linked_rows[0] if len(linked_rows) == 1 else ""
    events = git("log", REV, "--diff-filter=A", "--format=%H %ct %cI", "--", path).decode().splitlines()
    emit("envelope_link", id=cid, path=path, sha256=hashlib.sha256(data).hexdigest(),
         bytes=len(data), evidence_id=eid, entry_id_occurrences=entry.count(eid),
         entry_unique_carrier_row=len(linked_rows) == 1, id_in_carrier_row=eid in linked,
         subject_sha_equals_roster=payload["subject"]["digest"]["sha256"] == row["sha256"],
         sha_in_carrier_row=row["sha256"] in linked,
         procedure_count=payload["normalized_result"]["procedure_count"],
         procedure_equals_prediction=payload["normalized_result"]["procedure_count"] == int(predictions[cid]["procedure_count"]),
         ok=envelope["ok"], operation=payload["operation"], add_events=events)
emit("end", utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
     immutable_blobs=len(CACHE), carrier_rows=len(rows))
```

Unknown/unexercised here: fresh live-versus-committed equality, semantic ISA/ABI validity, Windows loading, and the canonical judge's final acceptance. None is inferred from the doc bits. No changes to counters, predicates, carriers, production docs, or evidence were made by this review.

Report: `.ufo/waves/round-32/a2residual/FinalSourceGateScope.md`
