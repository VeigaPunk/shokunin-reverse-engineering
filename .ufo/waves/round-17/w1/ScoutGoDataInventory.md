# ScoutGoDataInventory — Ghidra 12.1.4 Go typeinfo inventory + r16 selection-law hand derivation

Seat: KaidokuR17.ScoutGoDataInventory-3 (leaf, read-only, no subagents). Round 17 / hyaku phase 2, axes calibration + depth.
Question: exact base-JSON / patchverdiffs inventory relevant to Go 1.20.x, 1.23.x, 1.27.x, and what the r16 selection law selects for **1.23.12**, **1.20.12**, **1.27.0**.

Legend: **[OBSERVED]** = read from a file/command in this session; **[INFERENCE]** = derived from source semantics, not directly executed.
Sources: installed tree `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`; `Base-src.zip` members extracted read-only to `/tmp/gsrc_scan/base-src`; r16 law `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py`; pilot `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/pilot/`.
I ran **no** REA analyze/search/decompile and no Ghidra. I did run two allowed `rea inspect-go-binary` inspections (recorded in §7); neither starts a Ghidra session.

---

## 1. Inventory (exact) **[OBSERVED]**

Directory: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`
Contents: **11** base JSONs (`go1.15.0.json` … `go1.25.0.json`), **123** files in `patchverdiffs/`, **9** `.gdt` archives (`golang_1.15…1.23_anybit_any.gdt`).

### 1.1 Base JSONs (all 11, complete)

| file | bytes | sha256 |
|---|---:|---|
| `go1.15.0.json` | 4267141 | `cd070f2165716fd63643c722e50722295367fb7d36ff7a153d56178877da5b10` |
| `go1.16.0.json` | 4671548 | `d668acd92c30102dc85243c4ef580d5294e6c6f494d16f45a95c42959de00dee` |
| `go1.17.0.json` | 6100205 | `fb1f31849c303642739cfe857f810e1606eb1b34ddee41486b359bd9df28d549` |
| `go1.18.0.json` | 6325742 | `86a0687c9ce129bf9cf94faa20bee250fc13a298935d3b0ca3e0dee68ef91f67` |
| `go1.19.0.json` | 6469362 | `79c93ea499226c79e234053ea886779a26d3be363e437b102c046d8b6bb98885` |
| **`go1.20.0.json`** | **8875175** | `6def34993dd352b01f749dc44935178bdf2dbd13f585adf631798919ad6d0a32` |
| `go1.21.0.json` | 9039469 | `7bfe8f9a0f316ba3e6258152e35181c1d1c5c6b0bb0e6e9e95355490bb447b31` |
| `go1.22.0.json` | 9203666 | `c8feb28695499d1631af5ae441c8fd39c7eb75ce54dc8472673f2693e6974640` |
| **`go1.23.0.json`** | **9368866** | `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692` |
| `go1.24.0.json` | 10039962 | `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571` |
| `go1.25.0.json` | 10081618 | `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` |

Top-level bucket keys: **`go1.20.0.json` has 28**, **`go1.23.0.json` and `go1.25.0.json` have 27** (the latter two key sets are identical to each other). The sole difference is **`windows-cgo`, present only in 1.20.0**. Set in 1.23/1.25: `all`, `386`, `amd64`, `arm`, `arm64`, `cgo`, `darwin`, `darwin-amd64[-cgo]`, `darwin-arm64[-cgo]`, `linux`, `linux-386[-cgo]`, `linux-amd64[-cgo]`, `linux-arm[-cgo]`, `linux-arm64[-cgo]`, `linux-cgo`, `unix`, `windows`, `windows-386[-cgo]`, `windows-amd64[-cgo]`. `all` is present in every base. Each bucket is `{"Funcs": …, "Types": …}`. **[OBSERVED]**

### 1.2 `patchverdiffs/` coverage by minor line **[OBSERVED]**

| minor | count | patch range | gaps |
|---|---:|---|---|
| 1.15 | 15 | 1..15 | none |
| 1.16 | 15 | 1..15 | none |
| 1.17 | 13 | 1..13 | none |
| 1.18 | 10 | 1..10 | none |
| 1.19 | 13 | 1..13 | none |
| **1.20** | **14** | **1..14** | none |
| 1.21 | 13 | 1..13 | none |
| 1.22 | 12 | 1..12 | none |
| **1.23** | **12** | **1..12** | none |
| 1.24 | 6 | 1..6 | none |
| **1.25 / 1.26 / 1.27** | **0** | — | **no diff files at all** |

No file anywhere in the directory matches `1.26` or `1.27` (`ls | grep -E '1\.2[67]'` → none). There is no `go1.26.0.json` / `go1.27.0.json`. `.gdt` coverage stops at 1.23 even though JSON bases reach 1.25 — and **no Base-src Java source references `anybit` or any `.gdt`** (`grep -rn 'anybit\|typeinfo/golang' base-src --include=*.java` → only `GoApiSnapshot.java:171` for the JSON path), so `.gdt` is dead weight for this law. **[OBSERVED]**

### 1.3 1.20.x diffs (14)

| file | bytes | sha256 |
|---|---:|---|
| `go1.20.1.json.diff` | 29761 | `30a2a767047db52d6980a1a56b7b798cdcb48641f93e5ed1003c78e1e1784b04` |
| `go1.20.2.json.diff` | 54613 | `0223b4328ee1eb8ebf53ede4e8b96f30e2197624bb9e6ed07c073f5dc6cf5219` |
| `go1.20.3.json.diff` | 65510 | `4b09f0c10ebfcd428c8b483d9b75854548aefee184825455eb03ee5160607643` |
| `go1.20.4.json.diff` | 93456 | `622a024224b0320dc5d99eafd7bb9a5a5be29d3277ee6dc935e54410c8e871de` |
| `go1.20.5.json.diff` | 129603 | `20f03367aa2ca7e2de3e9313dafd96bbc0ab8b9de8b94f0d6f58fcd08ead78df` |
| `go1.20.6.json.diff` | 138685 | `8f3a9cb7a8c66d468aa64fa34a621939a543119a4a15f61ea143deedba131d8f` |
| `go1.20.7.json.diff` | 138685 | `5e109e91c80e2c5790889d4c129ed85ff11266e7b82045e28e273d0bdbe42a4f` |
| `go1.20.8.json.diff` | 145242 | `727b65ffa741f54bdad8cea69c9f05eeafe2e37e84bffd5994babca901d5d8e6` |
| `go1.20.9.json.diff` | 145242 | `727b65ffa741f54bdad8cea69c9f05eeafe2e37e84bffd5994babca901d5d8e6` |
| `go1.20.10.json.diff` | 159385 | `5237781012c01785c2f630d406d7e4904ac08f5591138076a2d21a94bdf0da1f` |
| `go1.20.11.json.diff` | 163263 | `a361c0ced518579c08d87082aabb3bc4bec64ac36d2af4c1b1acb07922055805` |
| **`go1.20.12.json.diff`** | **164688** | `148352d3c6ccbd6b7cf53d5b78d5c6950006b7f33eba4986bcdebd2af105e82b` |
| `go1.20.13.json.diff` | 172624 | `d4de70e3797277d3ce3ebf3c95b0aa38c0a0013e7866c468401e77c4617a87fb` |
| `go1.20.14.json.diff` | 166259 | `7016ddfc4e109d5abfe898282701b03fe41932461c8c6ff952ca92b2b7cdec39` |

### 1.4 1.23.x diffs (12)

| file | bytes | sha256 |
|---|---:|---|
| `go1.23.1.json.diff` | 21151 | `e1cf40d854727baffe57422a7b1730ea2a8173323acdab245a44263e2db27759` |
| `go1.23.2.json.diff` | 35012 | `1b0ffac797badf4fba6212fc3f68580220758dc1cf8a49a4c2f8f0b5bd126f2a` |
| `go1.23.3.json.diff` | 46331 | `1f84ba1d6ed5cbe214ed1344fe0c44984bcc23518347c20105cf93214fb5f201` |
| `go1.23.4.json.diff` | 54879 | `03304f358ef87de1936bbbfdfd909bd3c370c467105d126c1135ab6dfbed9774` |
| `go1.23.5.json.diff` | 65224 | `ea0ee72eb3fac01ea6e1fcca6daab0ab639c8f59e2515ade257772187ab4d288` |
| `go1.23.6.json.diff` | 65224 | `ea0ee72eb3fac01ea6e1fcca6daab0ab639c8f59e2515ade257772187ab4d288` |
| `go1.23.7.json.diff` | 84655 | `7dfe11a950aab694320d9ec1430872b6aefee66604e83e0635ec2211e7b9e9c5` |
| `go1.23.8.json.diff` | 87402 | `6d94cc11845b0150b9688070be076aa43d646d67c46446b8d1a2aad20493a25a` |
| `go1.23.9.json.diff` | 87402 | `6d94cc11845b0150b9688070be076aa43d646d67c46446b8d1a2aad20493a25a` |
| `go1.23.10.json.diff` | 101332 | `d9bcb9b73a60f056df7ed26895d5cc19a2cd54ccbfef90a7084afafe646735bd` |
| `go1.23.11.json.diff` | 106762 | `9ceb11e2ef384feb7b8ff41c3a534819b6fa43ccf2ccadb0eac1296c73e4bed4` |
| **`go1.23.12.json.diff`** | **111215** | `e1fdbc7e690cf6a1bb7c56969c2308ecc51a532daf6b1c7e8cd4dab3b7a99c53` |

### 1.5 1.27.x

**Nothing.** No base, no diff. This is the file-level cause of the shfmt bootstrap failure.

### 1.6 Diff format and anchoring **[OBSERVED]**

Diffs are **jd native format** (`JsonPatch.java:28-30`, "currently only supports reading jd … native format"): triples of `@ ["path","…"]` / `- old` / `+ new`, read line-wise (`JsonPatch.java:39-54`). They are anchored to the **patch-0 base**, not chained patch-to-patch: `JsonPatchApplier` is constructed from `jsonFile`, i.e. the `goM.m.0.json` base (`GoApiSnapshot.java:136-137`). Direct probes:

- `go1.23.0.json` `["all"]["Funcs"]["crypto/x509.alreadyInChain"]["Position"]` = `$GOROOT/crypto/x509/verify.go:855:6`, byte-identical to the `-` line of hunk 1 in `patchverdiffs/go1.23.12.json.diff`; the `+` line is `...:858:6`.
- `go1.20.0.json` `["all"]["Funcs"]["crypto/internal/bigmod/_asm._MASK"]["Position"]` = `$GOROOT/crypto/internal/bigmod/_asm/nat_amd64_asm.go:86:6`, identical to hunk 1's `-` line in `go1.20.12.json.diff`.

Hunk accounting: `go1.23.12.json.diff` = 2506 lines / 836 `@` sections (622 under `["all"`, 113 `["windows"`, 36 `["unix"`, 31 `["linux"`, plus per-arch buckets). `go1.20.12.json.diff` = 3253 lines / 1111 sections (611 `["all"`, 135 `["linux"`, 111 `["darwin"`, 48 `["unix"`, **19 `["linux-amd64"`**, 19 `["linux-amd64-cgo"`, …). The diff therefore patches the **effective bucket too**, not just `all`. **[OBSERVED]**

Seven consecutive-patch pairs are byte-identical (proved by rerunning the digest over every diff): `1.15.4=1.15.5`, `1.20.8=1.20.9`, `1.21.12=1.21.13`, `1.22.8=1.22.9`, `1.22.11=1.22.12`, `1.23.5=1.23.6`, `1.23.8=1.23.9`. **[OBSERVED]** Consequence: for those patch pairs the patched snapshot is provably identical, so a fallback between them is content-neutral. **[INFERENCE]**

---

## 2. The law, hand-derived

`GoApiSnapshot.get` (`GoApiSnapshot.java:102-116`):

1. **Base file is always patch 0**: `goVer.withPatch(0)` then `getApiSnapshotFile(baseVer, "", "")` → `typeinfo/golang/go<M.m.0>.json` (`:122-123`, filename format `:171`; `withPatch` `GoVer.java:138-140`).
2. **No base ⇒ hard stop**: `return null` (`:124-126`), and `get()` then returns `GoApiSnapshot.EMPTY` (`:115`, constant `:242`). **No cross-minor fallback exists** — a 1.27 request never looks at `go1.25.0.json`. Also, the patch-diff lookup is never reached when the base is missing.
3. **Patch diff is the first present patch ≤ requested, within the same major.minor**: `while (patchVer.getPatch() > 0 && (patchDiffFile = getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")) == null) patchVer = patchVer.prevPatch();` (`:153-156`; `prevPatch` `GoVer.java:134-136`). First present wins — no summation of diffs.
4. **Exactly one log line, mutually exclusive** (`:158-164`): if the found patch ≠ requested patch → `WARN  (GoApiSnapshot) Falling back from <req> to <found> for Go API snapshot`; else → `INFO  (GoApiSnapshot) Using Go API snapshot for <req>`. If no diff exists at all (patch 0 or empty minor), `getPatchVerDiffFile` returns null and the base alone is used (`:129-131`) — with the WARN already emitted by the same `if` for any requested patch > 0.
5. **Bucket order** (`:108-109`): `[goOS-goArch, goOS, (unix if GOOS∈IS_GOOS_UNIX else ""), goArch, all]`, with the empty entry dropped downstream (`:230-232`). `read()` keeps every matching bucket in that order in a `LinkedHashMap` (`:228-237`); lookups return the **first** bucket that has the name (`:514-532`). So the effective bucket is `linux-amd64`; `all` is only a fallback for names absent there.
6. **GOOS/GOARCH source** (`GoBuildInfo.java:272-275`, `:306-309`): build setting if present, else loader mapping — ELF→`linux` (`:286-288`), `x86_64`→`amd64` (`:65-71`, `:317-323`).

Version input path: REA reports `go<raw>`; Ghidra strips a leading `go` (`GoBuildInfo.java:488-490`) and `GoVer.parse` truncates at the first non-`[.0-9]` character (`GoVer.java:62-81`). `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` (`GoRttiMapper.java:79`) with wildcard patch bounds (`GoVerRange.java:42-57`), compared in `contains` (`:83-87`) — so **1.25.7 is in range** and 1.27.0 is not.

---

## 3. The three requested derivations

| | **1.23.12** | **1.20.12** | **1.27.0** |
|---|---|---|---|
| normalized ver | `1.23.12` | `1.20.12` | `1.27.0` |
| base file | `go1.23.0.json` (9368866 B, `3b1d795f…`) | `go1.20.0.json` (8875175 B, `6def3499…`) | **none** |
| diff lookup | hit on first iteration | hit on first iteration | **not attempted** (`:124-126`) |
| selected diff | `patchverdiffs/go1.23.12.json.diff` (111215 B, `e1fdbc7e…`) | `patchverdiffs/go1.20.12.json.diff` (164688 B, `148352d3…`) | none |
| selected patch | 12 | 12 | — |
| r16 status | `exact_diff` | `exact_diff` | `missing_base` |
| in 1.15–1.25 range | yes | yes | **no** → `ERROR Untested Go version [1.27.0]` (`:170-172`) |
| snapshot object | ver `1.23.12`, buckets `[linux-amd64, linux, unix, amd64, all]` | ver `1.20.12`, same 5 buckets | `EMPTY` (ver `INVALID`, 0 buckets) |
| effective bucket | `linux-amd64` (then `linux`, `unix`, `amd64`, `all`) | same | — |
| GoApiSnapshot log | `INFO Using Go API snapshot for 1.23.12` | `INFO Using Go API snapshot for 1.20.12` | **none** |
| GoRttiMapper log | `INFO Using Go API snapshot for version 1.23.12` (`:178-181`, ver valid) | `INFO … version 1.20.12` | **none** (ver invalid, `:178`) |
| bootstrap | succeeds (type structs available) | succeeds | **fails**: `WARN Missing Go bootstrap type info…` (`:356-360` via catch `:114-117`) |

Both requested patches are **exact** hits, so no WARN fallback line is predicted for either. For 1.27.0 nothing is selected and the failure is structural, not a version-string problem: the raw string `go1.27.0-X:nodwarf5` normalizes cleanly to (1,27,0).

Cross-check against the r16 law (run read-only on the installed dir): `selection.py` returns exactly the §3 file-level cells — `exact_diff` + base/diff digests for 1.23.12 and 1.20.12, `missing_base` with `base:null`/`selected_diff:null` for 1.27.0. Its adjacent edge cases are also **[OBSERVED]**: `1.23.0` → `base_only` with `selected_diff:null`, `1.20.15` → `fallback_diff` selecting `go1.20.14.json.diff`, `1.25.7` → `base_only` with `selected_patch:0`. The corresponding **log lines are derived, not observed** (`1.23.0` → INFO; `1.20.15` → WARN `Falling back from 1.20.15 to 1.20.14`; `1.25.7` → WARN `Falling back from 1.25.7 to 1.25.0`): they follow from `:158-164`, and no pilot run exercised a fallback.**[INFERENCE]**

---

## 4. Calibration against the pilot logs **[OBSERVED]**

**esbuild 0.25.12, `go1.23.12`, `bab29b2c…`** — `pilot/esbuild-0.25.12-log/ghidra.log`:
`:62` `INFO (GoRttiMapper) Reading Go binary info`, `:63` `INFO (GoApiSnapshot) Using Go API snapshot for 1.23.12` → predicted by §2.4 INFO branch; `:64` `INFO (GoRttiMapper) Using Go API snapshot for version 1.23.12` → predicted by `:178-181`; `:67` `INFO (GolangSymbolAnalyzer) Go version 1.23.12` → `GolangSymbolAnalyzer.java:139`. No `Untested`, no `Falling back`, no `Missing bootstrap`. **Derivation matches observation field for field.**

**shfmt, `go1.27.0`, `58f76563…`** — `pilot/shfmt-log/ghidra.log`:
`:82` Reading, `:83` `ERROR (GoRttiMapper) Untested Go version [1.27.0]` → `:170-172`; `:84` `WARN (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.` → `:356-360`; `:85` `ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper` → `GolangSymbolAnalyzer.java:134-136`; `:86-89` the **same five-line block again 10 s later** (`10:17:30` → `10:17:40`) → `GolangStringAnalyzer.java:103-105` re-invokes `getSharedGoBinary`. Critically, **no** `GoApiSnapshot` line and **no** `Using … for version` line, exactly as §2.2 predicts for `EMPTY`. **Derivation matches observation field for field**, including the absence of lines.

---

## 5. Findings that bind the round-17 C2 tools (calibration)

* **F1 — the two snapshot label patterns are not independent probes.** The fallback branch *replaces* the INFO line: `getPatchVerDiffFile` emits either `WARN Falling back from <req> to <found> for Go API snapshot` or `INFO Using Go API snapshot for <req>`, never both (`:158-164`). The second pattern (`INFO Using Go API snapshot for version <ver>`) is emitted by `GoRttiMapper` whenever the snapshot ver is valid (`:178-181`), and that ver is the **requested** one because `read(...)` receives `goVer`, not `baseVer` (`:111`). Consequences:
  - `exact_diff` and patch-0 `base_only` → both label patterns, same version.
  - `fallback_diff` and patch>0 `base_only` (e.g. 1.25.7) → only the `for version <requested>` pattern; the GoApiSnapshot line is a WARN with a different wording.
  - `missing_base` → neither pattern.
  So the contract's `snapshot_label` containment test still matches truthfully in every case that has a label, but **cannot discriminate exact vs fallback**, and the `snapshot_loaded` classification survives a fallback only because of the `GoRttiMapper` line. If the round wants that distinction observed rather than inferred, `log-extract.py` must also capture `Falling back from (\S+) to (\S+) for Go API snapshot` and expose the found patch; otherwise `compare.py`'s `snapshot_label` comparison is satisfied by a run that used a lower patch's content.
* **F2 — `missing_base` is discriminated by two absences plus two presences.** Predicted fingerprint for 1.27.0: `Untested Go version [1.27.0]` ERROR + `Missing Go bootstrap type info` WARN + *neither* snapshot label. The contract's `missing_bootstrap` iff `missing_base` holds for this carrier; note the converse is not a law of Ghidra — a valid snapshot can still fail `initStructMappings` and produce `IOException Invalid Go bootstrap struct mapping info` (`:363-365`).
* **F3 — `normalize` must strip `go` before `GoVer.parse`.** `GoVer.parse("go1.27.0-X:nodwarf5")` = **INVALID (0,0,0)** (the `[^.0-9]` truncation fires at index 0), whereas `GoBuildInfo` strips the prefix first (`:488-490`), giving (1,27,0). The contract's "normalize exactly as GoVer.parse/fromVersionString" must include the prefix strip, or `predict.py` exits 2 on every real carrier.
* **F4 — both pilot carriers take the build-setting branch; the loader fallback is unexercised.** `shfmt` module text carries `build\tGOOS=linux`, `build\tGOARCH=amd64`, `build\tGOAMD64=v1`, `CGO_ENABLED=1`; `esbuild` carries the same GOOS/GOARCH/GOAMD64 with `CGO_ENABLED=0`. So `GoBuildInfo.getGOOS/getGOARCH` return the build-settings values (`GoBuildInfo.java:272-275`, `:306-309`) and the ELF→`linux` / `x86_64`→`amd64` loader fallback (`:283-297`, `:317-328`) is **not** exercised by either pilot. Both branches yield `[linux-amd64, linux, unix, amd64, all]` here, so the derivation is insensitive for these carriers — but a `predict.py` that models only the fallback (or only the settings) is untested on the other branch.
* **F5 — the pilot JSONs cannot supply the predicted version.** `pilot/esb.json` and `pilot/shfmt.json` are `operation: binary_overview`, `predicate_type: rea.analysis`, with `normalized_result` = `{document, image_base, segments, segment_count, procedure_count, string_count}`; the token `go1.23.12`/`go1.27.0` appears nowhere in either file. The versions in `pilot/README.txt` are therefore **unsourced in the retained artifacts**. `carrier-run.py` must retain a separate `inspect-go-binary` JSON (as §7 shows) for `predict.py`'s `normalized_result.build_info.go_version`.
* **F6 — duplicated bootstrap attempts are normal.** A failed `getSharedGoBinary` yields two full error blocks (one per analyzer). Observed `shfmt-log/ghidra.log:82-85` and `:86-89`. Any comparison keyed on occurrence counts rather than presence will mismatch a correct prediction.
* **F7 — a content-level prediction that digests only `all` is wrong.** The selected diff patches `linux-amd64` itself (19 hunks in `go1.20.12.json.diff`). File-level digests (base + diff) are correct and sufficient for the current contract; a future in-memory digest claim would need the patched bytes.

---

## 6. Remaining unknowns

1. Post-diff snapshot bytes were **not** produced (r16 law deliberately never merges; reading `JsonPatchApplier` end-to-end was out of scope). All content claims above are file-level or base-file probes. **[gap]**
2. No pilot observation exists for **1.20.12** this round; its prediction is source-derived only. **[gap]**
3. `.gdt` provenance/consumer is outside `Base-src.zip` (no reference found); I did not chase another module. Not used by this law. **[gap]**
4. Re-invocation mechanics of `TransientProgramProperties` (whether a null supplier result is cached) inferred from the duplicated log block, not read in that class. **[inference]**

---

## 7. Tooling record

No installs, no upgrades, no pacman transactions. Read-only commands only: `ls`, `stat`, `sha256sum`, `unzip -l/-p/-o` (into `/tmp`), `grep`, `awk`, `wc`, `python3 -I` (stdlib), and the r16 `selection.py` imported read-only.

Allowed REA inspections actually run (no Ghidra session; contract permits `inspect-go-binary`):

- `npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json` → exit 0, `evidence_id ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`, stdout sha256 `a5ddc648011cc7437f22869110935849bde03df5bab3d6c17865c9c7bae57936`, `go_version = "go1.27.0-X:nodwarf5"` (19 bytes at file offset 3515617).
- `npx -y rea-agents@6.5.0 inspect-go-binary …/@esbuild+linux-x64@0.25.12/…/bin/esbuild --format json` → exit 0, `evidence_id ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626`, stdout sha256 `a20a65deb3cf1cc2b9737537220891f366b2ad55275a0a276699a3dfdff85ebf`, `go_version = "go1.23.12"`, build settings include `GOOS=linux`, `GOARCH=amd64`, `CGO_ENABLED=0`.

---

## 8. Cross-seat concordance (read-only check, no edits to sibling files)

- `w1/selection-1.23.12.json`, `selection-1.20.12.json`, `selection-1.27.0.json`, `selection-1.27.2.json` (written 10:33 by another seat) agree with §3 **byte for byte**: same `status`, base/diff paths, sizes, sha256s, `selected_patch`, `arch_search_order`, `base_matching_buckets`, `patch_applied:false`. `1.27.2` is also `missing_base` — the derivation generalizes to any 1.26/1.27 patch. **[OBSERVED]**
- `RevSnapshotDiffRead.md:7-20` reaches the same file identity for 1.23.12 by the same `:162-164` argument; `ScoutGoApiSnapshotLog.md:125-146` items 1-2 state the same label-echo and fallback-gap concerns as my F1. No conflict found. L1 should integrate these once — my §5 F1 supplies the `:111`/`:158-164`/`:178-181` line proof and the `compare.py` consequence, not a separate finding to be counted again.
- Stale reference, not repaired by me: `ScoutGoApiSnapshotLog.md:150` cites `w1/selection.py`, which **does not exist** (`ls round-17/w1/*.py` → none). The law lives at `.ufo/waves/round-16/selection.py` (sha256 `6917da09fe61644a0e091e4e1763eda89c32db9de02aa29dad9d275cd50ef430`), which is the path the contract's `carrier-run.py` pins. If L1 wants a w1-local copy for pinning, it must be created and pinned explicitly; the current contract text pins the r16 path, which is present. **[OBSERVED]**

