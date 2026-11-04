# ConnectorR87 — R87-C1 cross-links into the packed-ELF corpus, sibling overlap, and the proposed map/index rows

Read-only seat. Lane HEAD `1c8a76f41` (the r87 wave dispatch commit; declaration `f0ebf611`, repair
candidate `b5c7a49e`). The R87 entry slug is not chosen yet. Every line below uses the proposed slug
**`2026-11-04-r87-upx-magic-repair`**. If the L1 picks a different slug, substitute it everywhere.

## 1. The round-68..73 packed-ELF route: what R87 should cite and what should cite R87

### Knowledge entries (`corpus/knowledge/`)

| entry | direction | why (one line) |
|---|---|---|
| `2026-11-03-r68-packed-elf-route` | R87 cites it, and it gains a forward pointer to R87 | R68 defines detect → unpack → identity → recover, and its frontier line lists "an anti-UPX stub whose magic or entry is altered". R87 is the measured follow-up for the magic half only. |
| `2026-11-03-r69-packed-route-contract` | R87 cites it | R69 adds the enforced UPX pin (`upx 5.2.0`, sha256 `cf2f6e7c…c969`) and the libz shared-object carrier. R87 reuses both (`UPX_SHA256_PIN` at battery l.71). |
| `2026-11-04-r70-provenance-bound-receipts` | R87 cites it (main ancestor) | R70 introduced the population R87 freezes. Its 4-carrier table (`tools/round-70/packed-elf.py:91-110`) has byte-identical sha256 pins to the battery l.78-84. `DECLARED_ORIG {"jq":167,"xxd":99,"libz":184,"dinit":1268}` is identical (r70 l.116 = battery l.86). `PACKING_MODE = "upx --best"` (r70 l.85) is the same mode as battery l.227. R87's "declared original procedure count" arm is therefore R70's constant. |
| `2026-11-04-r71-registry-grammar` | neither (not needed) | R71 is about registry grammar and the runtime environment class. R87's battery does not use the four-key child-env allowlist or the run binding. Linking them would imply guarantees R87 does not have. |
| `2026-11-04-r72-checker-env-capsule` | neither | Checker-mode environment and capsule audit. R87 has no receipt checker, so nothing carries over. |
| `2026-11-04-r73-kernel-witness-record` | neither | A12 kernel witness. It is about the instrument, not the carrier. |

Second-order point: the R68 and R69 index lines both say the limit is "default packing". R70 switched
to `upx --best`, and R87 uses `--best`. So the R87 entry should name `--best` as its packing-mode limit
and cite R70, not R68, for that mode. Otherwise a reader of R68 would assume default-mode coverage.

### SOURCES rows (`corpus/SOURCES.md:186-188`)

| row | direction | why |
|---|---|---|
| S269 (upx-doc.txt v5.2.0, linux/elf386 byte-restoration) | R87 cites it | The "`upx -d` restores the pinned sha256" arm relies on S269's statement that unpacking restores the original bytes. R87 extends that statement to a file whose magic was repaired. |
| S270 (help.cpp/main.cpp v5.2.0, `upx --version` banner) | R87 cites it | The battery's packer-identity check (version `upx 5.2.0` plus sha256) rests on the same banner. |
| S271 (S269 word-count correction) | R87 does not cite it separately | It makes no new mechanism claim. `pre/sources-census-before.txt` already flags S271 as a W04 duplicate URL of S269. Citing S269 alone avoids spreading the duplicate. |
| S306+ (new: `src/stub/src/include/linux.h` l_info/p_info/b_info; `src/p_unix.cpp` "sz_cpr must be h->magic") | R87 cites them; nothing older cites them | These are new URLs at the same `v5.2.0` tag, so they are not duplicates of S269 or S270. **Gap:** the repair's docstring (`tools/round-87/upx-magic-repair.py:8-15`) also relies on **`packhead.cpp`** for "the checksum byte is the sum of bytes 4..30 mod 251 — it EXCLUDES the magic". That is the property that lets a zeroed PackHeader still be validated, and it is the whole difference between T1 and the cheap rule. The frozen plan's source list (`plans/round-87-claims.md`, Sources paragraph) names only linux.h and p_unix.cpp, and `grep packhead plans/round-87-claims.md .ufo/waves/round-87/claims.json` finds nothing. If the knowledge entry states the checksum rule, it needs a third S-row for `src/packhead.cpp` at v5.2.0, or it should drop the claim. |

### SKILL registry rows (`SKILL.md`, the `<!-- instrument-registry v2 -->` block, l.1780-1933)

| row | direction | why |
|---|---|---|
| `tools/round-68/packed-elf.py` (l.1861) | Context only. R87's registry rows should name R70 as their ancestor, not R68. | R68 has two carriers and default packing. R87's population is R70's. |
| `tools/round-69/packed-elf.py`, `contract-probe.py`, `controls.py`, `provenance-check.py`, `mutation-check.py` (l.1862-1866) | None are cited | R87 reuses none of these instruments. It only reuses the UPX pin constant. |
| `tools/round-70/packed-elf.py` (l.1867) | R87's battery row should name it as the source of the frozen carrier table and `DECLARED_ORIG` | The pins and counts are copied, not imported. The row should say "copied from" so that drift in R70 is visibly unrelated. |
| `tools/round-71..73/packed-elf.py` and their probes, controls and capsule readers (l.1873-1891) | None are cited | The environment, witness and capsule layer is not used by R87. |
| **New** `tools/round-87/upx-tamper-battery.py` and `tools/round-87/upx-magic-repair.py` | Must be added, after l.1932 and before `<!-- /instrument-registry -->` | `tools/round-68/registry-conformance.py` counts plan-named own-round tools for rounds ≥ 41. Both files are named in `plans/round-87-claims.md`. Without rows, the conformance census reports them as unregistered. Proposed rows are in section 3. |

The PROVINCE/README frontier lines that R87 supersedes (only the magic half) are:
- `corpus/README.md:324` (Round-68 frontier note)
- `PROVINCE.md:466` (r68), `:474` (r69), `:537` (r70) and `corpus/README.md:355` (r70). These list "anti-UPX stubs" or "anti-UPX stub whose magic or entry is altered" as Frontier.

The R87 note must supersede the **magic-altered** clause for the 4 carriers under `--best` and nothing else. Entry-altered stubs stay Frontier, and so do other packers.

## 2. Sibling-lane overlap (`/home/vgpnk/Projects/shokunin/*-shokunin/corpus`, grep `UPX|NotPackedException|[Pp]acker`, read-only)

| lane | path | one line | overlap? |
|---|---|---|---|
| revenger-shokunin | `corpus/SOURCES.md:363` (S348) and `corpus/knowledge/round-73-re-resource-atlas.md:324-333` | The Ugarte-Pedrero et al. SoK "Deep Packer Inspection" (IEEE S&P 2015) Type I–VI packer taxonomy, in an "Obfuscation, packers, anti-analysis" atlas slice (S343–S370). | **Adjacent, not the same ground.** It is a bibliography/atlas row. It has no carrier, no UPX measurement and no repair. It is a possible background citation for the R87 entry's limits ("magic repair ≠ unpacking a Type II+ packer"). Kaidoku should only reference it, not import it as an S-row, because it is the sibling's row. |
| revenger-shokunin | `corpus/SOURCES.md:221` (S206 capa limitations: packers), `:259` (S244 kavanoz APK), `:264` (S249 mal_unpack), `:295` (S280 pkg-unpacker), `:343` (S328 qc_image_unpacker) and atlas `:207,:251,:308,:418-419` | Tool READMEs about packers, Android/JS/Qualcomm unpackers, and dynamic unpackers. | No: different packer families, no ELF/UPX claim. |
| kotoba-shokunin | `corpus/README.md:58`, `corpus/knowledge/substrate-pin-guard-round23.md:17` | "opencode's mtime is a 1985 packer constant". | No. The word appears in a different sense (archive mtime). |
| kengaku-shokunin | `corpus/evidence/round53/pin-tree-2fd12b88.json:2125` | A file path `baseline_packer.py` (LLM batching). | No. |
| audio-shokunin | `corpus/live/r62-boundary/src/codec_desc.c`, `r74-scout/build_members.py` | "Avid … RGB Packer" codec name, and an LSB bit packer. | No. |
| game-dev-2d-shokunin | 580 files under `corpus/fixtures/` and `corpus/live/runs/` | Comments about the Godot 4.7.2 export "packer" temp-file workaround. | No. |
| tabi-shokunin | `corpus/evidence/round-13/aria/node_modules/…` (3 files) | Vendored `pngjs bitpacker` and `caniuse-lite unpacker`. | No. |
| chousa-shokunin | `corpus/captures/e84bfe97808591d23fe3266f.raw` | The only `UPX` hit outside kaidoku, and it is a base64 false positive (`…JDUPXurk6…`). | No. |

**Province:** `grep -l -E 'UPX|NotPackedException' */PROVINCE.md` returns only `kaidoku-shokunin/PROVINCE.md`. revenger-shokunin's PROVINCE.md and SKILL.md have no `upx|packer|packed` line. `NotPackedException` appears in no sibling corpus. Packed-ELF/UPX ground, including the anti-UPX magic frontier, is claimed by **kaidoku alone** (PROVINCE l.464-474, l.522-537). No sibling-lane route conflicts with R87.

## 3. Proposed rows (house format)

### `corpus/README.md` § Coverage map. Insert after l.127 (the round-86 row)

If R87-C1 is met (8/8, controls all true, exit 0 at the measured revision):

```
| UPX magic-tamper repair (round 87) | `2026-11-04-r87-upx-magic-repair` | **Core** — a UPX 5.2.0 `--best` packed ELF whose every `UPX!` word is zeroed (T1) or replaced (T2, `KDK!`) still runs but `upx -t/-l/-d` answer `NotPackedException`; `tools/round-87/upx-magic-repair.py` rewrites only the PackHeader, `l_info` and end-of-chain `b_info` magic words, located structurally, and the four round-70 carriers (jq, xxd, libz, docker-init) are recovered 8/8 — `upx -t` passes, `upx -d` restores the pinned sha256, REA 6.5.0 `analyze` reports 167/99/184/1268 procedures; do-nothing control 0/8, cheap-rule control 4/8 (T2 only), plain originals refused 4/4, a corrupted payload never recovered, intact packed left byte-identical 4/4; entry-altered stubs and other packers stay Frontier |
```

If it is not met, keep the same first two cells and use this third cell instead: `measured, not promoted — recovered N of 8 under the frozen counter; <named false arm/control>; the magic-altered class stays Frontier`. The miss is reported and never narrowed (this matches the round-50/38/40 "measured, not promoted" rows).

### `corpus/README.md` § Knowledge index. Append after l.264 (the r86 line), matching the r84-r86 columns `entry | topic | source | verified-at`

```
| `2026-11-04-r87-upx-magic-repair` | anti-UPX magic tampering is a marker problem, not a payload problem: the PackHeader checksum excludes its magic, `l_info` mirrors the PackHeader's version/format, and the `b_info` chain ends in a sentinel whose `sz_cpr` is the magic, so all three `UPX!` words are recoverable from structure alone (T1 zeroed and T2 foreign, 8/8 on the four round-70 carriers under `upx --best`); limits UPX 5.2.0 / ELF x86-64 / `--best` / magic-only (entry-altered stubs, other packers, PE/Mach-O stay Frontier); the counter scores bytes, not provenance | S306+ (UPX v5.2.0 `linux.h`, `p_unix.cpp`; plus `packhead.cpp` if the checksum rule is stated), S269; `tools/round-87/upx-magic-repair.py`, `tools/round-87/upx-tamper-battery.py`; receipts `.ufo/waves/round-87/l1/scores/` and `pre/` | 2026-11-04 |
```

### `corpus/README.md` § Frontier. Dated note, appended after the round-84 note (l.366)

```
Round-87 frontier note, 2026-11-04: an anti-UPX stub whose **magic** is altered (every `UPX!` word zeroed or replaced) is **Core** for the four round-70 carriers packed by UPX 5.2.0 `--best` (`2026-11-04-r87-upx-magic-repair`; S306+), superseding the magic half of the round-68 note's "an anti-UPX stub whose magic or entry is altered" (l.324) and of the matching PROVINCE round-68/69/70 lines, and nothing else. Still Frontier: an altered entry or stub code, a tampered PackHeader field other than the magic, any other packer, packed PE/Mach-O, other carriers or packing modes, and semantic equality of a recovered inventory.
```

### `SKILL.md` instrument registry. Two rows after l.1932, 7 cells (`path | role | exits | command; selftest | pins | writes | owner`)

```
| `tools/round-87/upx-tamper-battery.py` | counter — R87-C1 coverage: packs the four round-70 carriers (pins and `DECLARED_ORIG` copied from `tools/round-70/packed-elf.py`) with the pinned UPX 5.2.0 `--best`, tampers T1-zero/T2-foreign, runs `--repair-cmd`, and scores a case recovered only when repair rc 0, changed bytes lie only in windows now reading `UPX!`, `upx -t` passes, `upx -d` restores the pin and REA 6.5.0 `analyze` reports the declared procedure count; controls N1 refuse-plain, N2 corrupt-payload, N3 intact-idempotent; built-in `identity` and `naive-global` repair commands are the do-nothing and cheap-rule controls | 0=recovered 8 of 8 and every control true; 1=target not met or a control false, each named; 2=could-not-evaluate (pin drift, packer or REA package mismatch, a tamper that `upx -t` still accepts) | `python3 -I -B tools/round-87/upx-tamper-battery.py --root . --repair-cmd tools/round-87/upx-magic-repair.py --upx /usr/bin/upx --pkg <rea-agents 6.5.0> --work <scratch> --json-out <receipt>`; `--selftest` 8 cases, exit 0 on 2026-11-04 | `.ufo/waves/round-87/claims.json` (counter sha256 `0f2d2bd8…4b0`) | `--json-out` receipt and the `--work` scratch tree only | kaidoku-r87 |
| `tools/round-87/upx-magic-repair.py` | tool — R87-C1 repair: restores the `UPX!` words of a UPX-packed little-endian ELF from the packer's own structures (checksum-validated PackHeader, `l_info` cross-checked against it, end-of-chain `b_info` reached by walking the chain); reads only `--in`, never runs the packer | 0=repaired or already intact (output written; byte-identical when intact); 2=refused (not ELF, no validated PackHeader, no matching `l_info`, chain without sentinel), nothing written | `python3 -I -B tools/round-87/upx-magic-repair.py --in <file> --out <file> [--json]`; `--selftest` 9 cases | sha256 `f4ebd152…3c49723` at `b5c7a49e` | `--out` only | kaidoku-r87 |
```

The repair row has no "exit 0 on <date>" stamp because this seat did not run the repair selftest. The case count of 9 comes from `upx-magic-repair.py:209`. The L1 should stamp the row after running it.
