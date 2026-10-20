# Round 15 — AttackNovelty (critic, C1 depth / calibration)

Seat: `KaidokuR15.AttackNovelty`. Scope: try to falsify C1 (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/claims.json:4-7`) as a repackaging of round 14. Read-only work. I ran no gate, test, build, selftest, REA, Ghidra or target. Tools installed or upgraded: none (`jq`, `unzip`, `sha256sum` were already present).

Abbreviations:
- `INST` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`
- `S003` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
- `GEN` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Framework/Generic/lib/Generic-src.zip`
- `UTIL` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Framework/Utility/lib/Utility-src.zip`

GEN and UTIL are installed companion source archives. They are not registered rows. I name them only as read-only anchors. L1 decides whether to cite them or to keep the claim inside S003 (see Correction 5).

## Verdict

**C1 as worded is partly repackaging, and its third discriminator is falsified on this installation.** Two of C1's three branches are not new:
- the plain file listing ("11 base JSON files, no 1.25/1.26 patch diffs");
- the patch-diff control flow.

Round 14 already observed both:
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/AttackNovelty.md:38,107-108`: 11 `go1.*.0.json` files, and 0 `patchverdiffs` matching `^go1\.2[56]\.`.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/SnapshotBootstrap.md:180,186`: no `go1.26.0.json`, and fallback stays inside one minor version.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md:23`: the "Falling back" message.

The admitted r14 entry already carries the source control flow for all three branches (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:35-38,51-54`). Re-citing those lines adds no depth.

The **OS/architecture branch** is a different problem. It is a possibility from source reading that the installed data makes unreachable on this host. A round-15 inventory that lists it as a live discriminator would be false calibration. The r14 entry's sentence at `:52-54` ("A present file without applicable records can therefore reach the same invalid-snapshot branch") needs a bounded, append-only qualification. It is not a fact to repeat.

C1 can still pass on depth, but only if its inventory records the genuinely new installed observations N1–N7 below, and only with OS/arch reframed.

## Counterexample (strongest available from local evidence)

**The claim:** "the inventory discriminates OS/architecture applicability as a cause of `Missing Go bootstrap type info`."

**Source facts:**
- S003 `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:108-109` always builds the search order `[goOS-goArch, goOS, unix|"", goArch, "all"]`.
- `:218-224` keeps any top-level key that appears in that order.
- `:503-505` defines `isInvalid()` as `arches.isEmpty()`.

**Installed fact (new).** I ran `jq -c keys_unsorted` and `jq -r '.all|type'` on every file in `INST/go1.*.0.json`. All 11 files have a top-level `"all"` object with non-empty `Types` and `Funcs`:

| file | `all` Types / Funcs | file | `all` Types / Funcs |
|---|---:|---|---:|
| go1.15.0 | 2421 / 12453 | go1.21.0 | 3257 / 26243 |
| go1.16.0 | 2526 / 12809 | go1.22.0 | 3426 / 26712 |
| go1.17.0 | 2764 / 17231 | go1.23.0 | 3532 / 27192 |
| go1.18.0 | 2883 / 17960 | go1.24.0 | 3706 / 28922 |
| go1.19.0 | 3002 / 18523 | go1.25.0 | 3741 / 29041 |
| go1.20.0 | 3119 / 25511 | | |

**Derived from source plus installed bytes [INFERENCE: not executed].** For every GOOS/GOARCH, including `unknown`, a present base file yields at least the `all` arch. `isInvalid()` is then false. So with the installed files, an invalid snapshot can only come from a missing base file.

Concrete instances:
- linux/mips64 matches `linux`, `unix` and `all`.
- windows/arm64 matches `windows` and `all`.
- go1.15 darwin/arm64: that file lacks the `darwin-arm64` key but still matches `darwin`, `unix`, `arm64` and `all`.

**Patched snapshots preserve this [INFERENCE about `JsonPatchApplier` semantics, not read].**
- A grep for top-level-only diff paths `^@ \["[^"]*"\]$` over `INST/patchverdiffs` returns 0 matches.
- A grep for whole-section paths `^@ \["all","[^"]*"\]$` also returns 0 matches.
- Every diff operation addresses a deeper path. The first path element is `all` for 58,666 of 82,579 `@` lines.

**Limit.** This holds only for this installation's bytes. A future or different snapshot set without `all` would bring the branch back. The r14 source sentence is not wrong as a general control-flow possibility. It is wrong as a description of this host.

Impacted axes: **calibration** if C1 or its entry presents OS/arch as a live third cause. **Depth** credit is valid only for the new observation that it is vacuous here.

## Genuinely new installed / source observations (not in r14 entry or r14 seats)

I checked these against the r14 w1 grep (`"all"`, `archSearchOrder`, `Falling back`, `Using Go API snapshot`, `getModuleDataFile`, `cgo`). Hits existed only for the generic source excerpts named above.

- **N1 — Pinned inventory digest.** The full manifest of `INST` is 143 regular files: 11 `go1.<minor>.0.json`, 9 `golang_1.15…1.23_anybit_any.gdt` and 123 `patchverdiffs/*.diff`. `du -sb` reports 96,168,885 bytes (apparent size, including directory entries; not a pure file-byte sum).
  - Aggregate digest: `98f7e64ce24094c8f16a7888c1e3545d5b19470805b6fc058c1e1cf0f4302fb3`. It is reproduced by `cd INST && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum`.
  - Per-base SHA-256:

    | file | SHA-256 |
    |---|---|
    | 1.15.0 | `cd070f2165716fd63643c722e50722295367fb7d36ff7a153d56178877da5b10` |
    | 1.16.0 | `d668acd92c30102dc85243c4ef580d5294e6c6f494d16f45a95c42959de00dee` |
    | 1.17.0 | `fb1f31849c303642739cfe907f810e1606eb1b34ddee41486b359bd9df28d549` |
    | 1.18.0 | `86a0687c9ce129bf9cf94faa20bee250fc13a298935d3b0ca3e0dee68ef91f67` |
    | 1.19.0 | `79c93ea499226c79e234053ea886779a26d3be363e437b102c046d8b6bb98885` |
    | 1.20.0 | `6def34993dd352b01f749dc44935178bdf2dbd13f585adf631798919ad6d0a32` |
    | 1.21.0 | `7bfe8f9a0f316ba3e6258152e35181c1d1c5c6b0bb0e6e9e95355490bb447b31` |
    | 1.22.0 | `c8feb28695499d1631af5ae441c8fd39c7eb75ce54dc8472673f2693e6974640` |
    | 1.23.0 | `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692` |
    | 1.24.0 | `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571` |
    | 1.25.0 | `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` |

  - All values are copied verbatim from the `sha256sum go1.*.0.json` output.
  - r14 pinned only the S003/S007 archives. It pinned no data bytes.
- **N2 — Patch coverage per minor, with contiguity.** Patch-diff counts per minor, each contiguous from `.1` to the maximum:
  - 1.15: 15; 1.16: 15; 1.17: 13; 1.18: 10; 1.19: 13; 1.20: 14; 1.21: 13; 1.22: 12; 1.23: 12; 1.24: 6 (max 1.24.6); 1.25: 0.
  - Consequence [INFERENCE from `GoApiSnapshot.java:148-166`]:
    - go1.24.N with N > 6 falls back to the 1.24.6 diff.
    - Every go1.25.N with N > 0 falls back to the bare 1.25.0 base.
    - In both cases the snapshot stays valid: patch-diff absence degrades the data softly and is never an invalid-snapshot cause.
  - r14 had only "0 matching 1.25/1.26".
- **N3 — Log-signature discriminator.** Source: `GoApiSnapshot.java:111,122-126,158-164` and `GoRttiMapper.java:170-181`. Base absent returns before `getPatchVerDiffFile` runs, so absence emits neither `Falling back from …` nor `Using Go API snapshot for …`. The mapper's `Using Go API snapshot for version %s` is also absent, because `EMPTY.getVer()` is `INVALID` (`:242`). Base present always emits one of the two `GoApiSnapshot` lines plus the mapper line. The analyzer log alone can therefore separate "missing base" from "present base", which the r14 table row 3 left as "next evidence". [Source reading; not executed.]
- **N4 — Calibration trap in the mapper log.** `read(is, archSearchOrder, goVer)` (`:111`) stamps the snapshot with the *requested* version. So for go1.25.7 the mapper prints `Using Go API snapshot for version 1.25.7` while the data is 1.25.0. The truth is only in the preceding `Falling back from 1.25.7 to 1.25.0` warning. An entry must not read the mapper line as proof that patch-exact data was used.
- **N5 — cgo records are never selected.** The installed files carry `*-cgo` keys, e.g. `linux-amd64-cgo`; 1.19+ also have a bare `cgo` key. Diffs touch them as well: 848 `linux-amd64-cgo` operations. The search order at `:108-109` never contains a `-cgo` or `cgo` name, so those records are skipped by `:218-220`. This is applicability information that r14 did not record. Its effect on type recovery is UNKNOWN.
- **N6 — GDT files are installed but unreferenced.** Nine `golang_1.15…1.23_anybit_any.gdt` files are present. An `awk` count of `anybit|\.gdt` over S003 members `ghidra/app/util/bin/format/golang/*` and `ghidra/app/plugin/core/analysis/Golang*` gives 0. This corroborates r14's S007 changelog point with installed bytes: no GDT exists for 1.24–1.26, and nothing on this path refers to any GDT.
  - Limit: only those member globs were counted, not all of S003.
- **N7 — The lookup is scoped to one module.** Neither user directories nor sibling modules are searched:
  - `GEN ghidra/framework/Application.java:954-962`: `getModuleDataFile(String)` resolves against the *calling class's* module root.
  - `:354-373`: it calls `module.findModuleFile("data/" + path)`.
  - `UTIL ghidra/framework/GModule.java:147-155,55-69`: that search covers the module root, then its `build` dir, then shadow modules from other application roots.
  - `Ghidra/Features/Base/build` does not exist (`ls`).
  - So the `INST` listing is the complete lookup domain, with one exception: a shadow `Base` module in another application root, which I did not enumerate [INFERENCE that the release has a single root].
  - This closes the scope gap that r14 left open in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md:139` ("may search other module-data roots").

## What is *not* new (must not be credited as depth)

- The 11-file / no-1.26 listing. Only its digests (N1) and per-minor shape (N2) are new.
- The control flow "no earlier-minor fallback; EMPTY → `Missing Go bootstrap`; range check is advisory".
- Any restatement of r4-10 measurements, the GP-6528 bundle, or the S001 `inspect_go_binary` route.

## Smallest safe correction

1. **Reframe the C1 discriminator set as "missing base vs present base (+ patch fallback level)".** State OS/arch applicability as *checked and vacuous on this installation*, with the `all`-key evidence. Do not list it as a live third cause.
2. **Correct r14 entry `:51-54` append-only.** Add a named correction in the new round-15 knowledge entry (or an appended section owned by L1) that bounds the r14 sentence to "source possibility; not reachable with Ghidra 12.1.4 installed snapshots". Do not edit the historical lines in place.
3. **Put N1 digests (full), N2, N3 and N4 in the inventory record.** N5–N7 are optional depth with limits. Without at least N1–N4, C1 is a repackaging of r14 and should not earn a depth move.
4. **Keep causality UNKNOWN for the r4-10 run.** N3 is a discriminator for *future retained logs*. The historical log was not retained.
5. **Source registry.** GEN and UTIL anchors for N7 are unregistered companion archives. Either L1 opens rows for them, or N7 is cited as an unregistered read-only observation, or N7 is dropped. The registry has no new rows unless L1 opens them.

## Proposed L1 checks (not executed by this seat)

- Run `cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum`. Expect `98f7e64ce24094c8f16a7888c1e3545d5b19470805b6fc058c1e1cf0f4302fb3` and 143 files.
- Run `for f in go1.*.0.json; do jq -r '.all|type' "$f"; done`. Expect 11 × `object`.
- Run `jq -r '[.all.Types,.all.Funcs]|map(length)|join("/")'` per file and compare against the table above.
- Grep `INST/patchverdiffs` for `^@ \["[^"]*"\]$` and for `^@ \["all","[^"]*"\]$`. Expect 0 matches each.
- Run `unzip -p S003 ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java | cat -n | sed -n '102,166p;205,242p;503,505p'`. Confirm the search order, the early return when the base is absent, the requested-version stamp (`:111`), and `isInvalid`.
- Confirm the candidate knowledge entry does not assert OS/arch as a reachable cause. Confirm it carries the append-only qualification of the r14 entry `:52-54`.
- Confirm the README coverage map and the craft-citation counts stay consistent after L1 integration. These are L1's existing round measures.

## Commands used (read-only inventory)

- `ls`, `ls -la`, `du -sb`, `find … | wc -l`, `sha256sum` over `INST`.
- `jq -c keys_unsorted`, `jq -r '.all|type'`, `jq -r '[.all.Types,.all.Funcs]|map(length)|join("/")'` on the 11 base files.
- `cat patchverdiffs/*.diff | cut -c1-2 | sort | uniq -c`, and `awk` for the first path element of `@` lines.
- `awk` contiguity per minor.
- Grep-tool regex over `INST/patchverdiffs`.
- `unzip -l` / `unzip -p … | cat -n | sed -n` on the named members of S003, GEN and UTIL.
- Grep-tool over `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1` for prior coverage.
