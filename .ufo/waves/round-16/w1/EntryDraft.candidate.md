<!-- DRAFT for L1 integration only. Proposed destination: corpus/knowledge/2026-10-20-r16-go-selection-preview.md. Proposed knowledge token: 2026-10-20-r16-go-selection-preview. No corpus, README, SOURCES, or index edit was made by this seat. -->
source: S003 `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (archive `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, same digest as the round-14 pin); same archive member `GoVer.java` for version spelling; installed data `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` (base `go1.25.0.json` is S023); round-15 pinned inventory `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` cited for patch-count and 1.24.7 agreement only.
verified-at: 2026-10-20 — source reading of the shipped member (numbered lines), installed JSON key reads and `sha256sum` of the digests below, performed by this seat. No `selection.py` executed, no JSON patch applied, no Ghidra/Java run, no target or carrier touched.
recheck: `sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.24.0.json /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.24.6.json.diff`, compare the digests in the table below, then run the selection command in "Model commands" (exact form; see status note there).

# Go API snapshot selection preview: source-law labels, unpatched buckets, and requested-label limits

## Question and provenance

Which installed base file and which patch diff would the shipped Ghidra source select for a requested `M.m.p` with a given GOOS/GOARCH, and which labels must accompany each result? This is a source-model selection preview. It does not compute patched bucket content, compile a provider, or establish any target capability or historical cause. It does not repeat the bootstrap diagnosis (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`) or the installed-resource identity inventory (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`); it uses their facts and adds the selection law and labels.

Digests observed by `sha256sum` in this seat, 2026-10-20:

| Object | SHA-256 | Size (bytes) |
|---|---|---|
| S003 `Base-src.zip` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` | not recorded |
| `typeinfo/golang/go1.15.0.json` | `cd070f2165716fd63643c722e50722295367fb7d36ff7a153d56178877da5b10` | 4,267,141 |
| `typeinfo/golang/go1.16.0.json` | `d668acd92c30102dc85243c4ef580d5294e6c6f494d16f45a95c42959de00dee` | 4,671,548 |
| `typeinfo/golang/go1.24.0.json` | `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571` | 10,039,962 |
| `typeinfo/golang/go1.25.0.json` (S023) | `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` | 10,081,618 |
| `patchverdiffs/go1.15.15.json.diff` | `d941cd17d43b70ef903a66f8ee14ad90101c3d355759525bd21e59e2bc0260c8` | 110,373 |
| `patchverdiffs/go1.24.1.json.diff` | `28be359f82b588100502483d1ebb930d832a93c99dd0d1ba1185f48b69e0506a` | 44,137 |
| `patchverdiffs/go1.24.6.json.diff` | `e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6` | 118,810 |

Installed data facts observed this session (directory listing, `stat`, `jq -c keys`):

- Base files: `go1.15.0.json` through `go1.25.0.json`, eleven files. No `go1.14.*` and no `go1.26.*` base.
- Patch diffs: 123 files. Per minor: 1.15:15, 1.16:15, 1.17:13, 1.18:10, 1.19:13, 1.20:14, 1.21:13, 1.22:12, 1.23:12, 1.24:6, 1.25:0. Each minor's diff numbers are contiguous from 1 to its maximum; no gap was observed.
- All eleven bases have top-level keys `linux-amd64`, `linux`, `unix`, `amd64`, `all`, `windows-amd64`, and `windows`. Full top-level key lists were read only for `go1.15.0.json` and `go1.24.0.json`.
- Generated `.gdt` archives exist for 1.15 through 1.23 only. The JSON path does not reference them (see Source law).

## Source law (S003, shipped member; line numbers as shipped)

- **`:102-116` `get`.** Search order at `:108-109`: `[goOS-goARCH, goOS, "unix" if goOS ∈ IS_GOOS_UNIX else "", goARCH, "all"]`. No base file gives `EMPTY` at `:115`.
- **`:118-146` `getApiSnapshotJsonFile`.** The base is `goVer.withPatch(0)` (`:122`). A missing base returns null at `:124-125` before any diff lookup, so a diff cannot rescue a missing base. A null diff returns the unpatched base provider (`:128-131`). A non-null diff returns a derived patched provider (`:133-145`). The preview never takes the derived branch.
- **`:148-166` `getPatchVerDiffFile`.** Starts at the requested patch and walks `prevPatch()` within the same major.minor while `patch > 0` and no `patchverdiffs/go{M.m.q}.json.diff` exists (`:153-156`). It logs `Falling back …` whenever the returned patch differs from the requested one (`:158-161`). That warning fires even when no diff is returned (the walk reaches patch 0 and `:165` returns null). Otherwise it logs `Using …` (`:162-164`).
- **`:168-178` `getApiSnapshotFile`.** Name is `typeinfo/golang/{subdir}go{M.m.p}.json{suffix}`. The diff uses `subdir = patchverdiffs/`, `suffix = .diff` (`:154`).
- **`:180-181` `IS_GOOS_UNIX`:** aix, android, darwin, dragonfly, freebsd, hurd, illumos, ios, linux, netbsd, openbsd, solaris. Windows and plan9 are absent, so the `unix` bucket is not searched for them.
- **`:183-192` `getApiFile`.** A separate utility with a `go%d.%d.json` filename fallback for patch 0. It is not on the snapshot path. The preview must not call it or emulate it.
- **`:205-240` `read`.** Keeps only JSON keys in the search list (`:212-221`). Results are built in search-list order, skipping empty names (`:228-237`). The result carries the requested `ver` (`:239`).
- **`:242` `EMPTY`** has version `GoVer.INVALID` (0.0.0). The requested label is lost on the missing-base path.
- **`:503-505` `isInvalid()`** is true when no bucket was retained. **`:514-532` `getFuncdef` / `getTypeDef`** scan buckets in search order and return the first hit.
- **`GoVer.java`** (member, methods `toString`, `parse`, `prevPatch`; not line-numbered in this draft): `toString` gives `M.m.p`. `parse` cuts the string at the first character outside `[.0-9]` and defaults a missing patch to 0.

## Selection algorithm (source-model specification)

1. **Parse.** Source accepts `M.m` and trailing text (see Limits). The preview accepts only a strict `M.m.p` of decimal integers and rejects anything else with exit 2.
2. **Base.** Look for `go{M}.{m}.0.json` in the root. If absent, status `missing_base`, `base` null, `base_matching_buckets` `[]`, `selected_diff` null, `selected_patch` null. Diffs are not consulted.
3. **Diff.** If `p = 0`, no diff. Otherwise, for `q = p, p-1, …, 1` in the same minor, take the first `patchverdiffs/go{M}.{m}.{q}.json.diff` present. Never consider `q > p`. None found gives `base_only`.
4. **Status.** `q = p` gives `exact_diff`. `q < p` gives `fallback_diff` with `selected_patch = q`. No diff gives `base_only`.
5. **`arch_search_order`** is the source list in step 2 above. The non-Unix placeholder is the empty string (see Limits for emitted form).
6. **`base_matching_buckets`** are the search-order names, first occurrence kept, empty dropped, that are top-level keys of the base JSON. They are base-file keys, not patched content.
7. **`patch_applied`** is always `false`. **`evidence_class`** is `source_model`.

## Status labels and what they do not establish

| Status | Selected | Required label | Does not establish |
|---|---|---|---|
| `missing_base` | none | Base absent; diffs ignored (`:124-125`). | Any layout or parse result. |
| `base_only` | base only | Unpatched base preview: buckets are base keys, `patch_applied` false. | That a same-minor diff exists or was applied. The `Falling back` warning (`:158-161`) does not mean a diff was selected. |
| `exact_diff` | base + diff for the requested patch | Name the selected diff; buckets remain base keys. | Patched bucket set or record content. |
| `fallback_diff` | base + lower-patch diff | State `selected_patch < requested`. Requested label is a source label only (`:111`, `:135`, `:239`). | Any content matching the requested patch. |

## Boundary cases (source-derived expectations; not executed)

Expectations follow the source law and observed data. No run output exists for these rows.

| Request | GOOS/GOARCH | Expected status | Selected diff | Base | `base_matching_buckets` | Basis |
|---|---|---|---|---|---|---|
| 1.15.15 | linux/amd64 | `exact_diff` | `go1.15.15.json.diff`, 15 | `go1.15.0.json` | linux-amd64, linux, unix, amd64, all | Exact diff exists (110,373 B). |
| 1.15.16 | linux/amd64 | `fallback_diff` | `go1.15.15.json.diff`, 15 | `go1.15.0.json` | same | Diff 16 absent; highest installed 1.15 diff is 15. |
| 1.24.1 | linux/amd64 | `exact_diff` | `go1.24.1.json.diff`, 1 | `go1.24.0.json` | same | Exact diff exists (44,137 B). |
| 1.24.7 | linux/amd64 | `fallback_diff` | `go1.24.6.json.diff`, 6 | `go1.24.0.json` | same | Installed 1.24 diffs end at 6; matches round-15 inventory. |
| 1.24.0 | linux/amd64 | `base_only` | none | `go1.24.0.json` | same | Patch 0: no diff lookup. |
| 1.25.7 | linux/amd64 | `base_only` | none | `go1.25.0.json` | same | No 1.25 diffs; source still warns `Falling back from 1.25.7 to 1.25.0` (`:158-161`) with no selected diff. |
| 1.16.0 | linux/amd64 | `base_only` | none | `go1.16.0.json` | same | Patch 0. |
| 1.14.9 | linux/amd64 | `missing_base` | none | none | `[]` | No `go1.14.0.json` installed. |
| 1.26.8 | linux/amd64 | `missing_base` | none | none | `[]` | No `go1.26.0.json` installed; upstream 1.26 support (S004) is not in this installation. |
| 1.24.7 | windows/amd64 | `fallback_diff` | `go1.24.6.json.diff`, 6 | `go1.24.0.json` | windows-amd64, windows, amd64, all | Search list `[windows-amd64, windows, "", amd64, all]`; `unix` not searched. |
| 1.15.0 | darwin/arm64 | `base_only` | none | `go1.15.0.json` | darwin, unix, arm64, all | Search list `[darwin-arm64, darwin, unix, arm64, all]`; no `darwin-arm64` key in observed 1.15.0 key list. |
| 1.24.0 | linux/riscv64 | `base_only` | none | `go1.24.0.json` | linux, unix, all | Search list `[linux-riscv64, linux, unix, riscv64, all]`; no riscv key in observed 1.24.0 key list. |
| 1.24 (malformed) | linux/amd64 | exit 2 (preview) | none | none | none | Source `GoVer.parse` gives 1.24.0 (not an equivalence). |
| 1.24.-1 | linux/amd64 | exit 2 (preview) | none | none | none | Source `parse` cuts at `-` and gives 1.24.0. |
| 1.24.7-rc1 | linux/amd64 | exit 2 (preview) | none | none | none | Source `parse` gives 1.24.7. |

Missing-base-with-diff is not installed in this data. It is a fixture-only case.

## Model commands (exact form; status note)

Recheck (intended form; `-I` with absolute script path as round-15 routed defect 1 asks):

```
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --request 1.24.7 --goos linux --goarch amd64
```

Status note: at draft time `selection.py` is being written by a sibling seat in this wave and does not yet exist under `.ufo/waves/round-16/`. This command is the contract form and has not been run. Do not quote output until the file exists and a run is recorded with its argv, exit code, and output digest.

Source-derived expectation for that request (not observed): exit 0; `status` `fallback_diff`; `base` path `.../go1.24.0.json`, size 10039962, SHA-256 `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571`; `selected_diff` path `.../patchverdiffs/go1.24.6.json.diff`, size 118810, SHA-256 `e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6`; `selected_patch` 6; `arch_search_order` `["linux-amd64","linux","unix","amd64","all"]`; `base_matching_buckets` the same list; `patch_applied` false; `evidence_class` `source_model`.

Developer self-check (not a gate; no claim): `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selfcheck.py`. Not run by this seat.

## Limits

1. **Source model only.** No `selection.py` run, no Ghidra or Java execution, no provider, no target, no carrier.
2. **Requested version is a label, not data identity.** The requested `goVer` is passed to `read` (`:111`), used in the derived provider name (`:135`), and stored on the result (`:239`). A fallback-diff result carries the requested version while its bytes come from base plus a lower-patch diff. Report `selected_patch`, the digests, and the status.
3. **A log line is not a selection.** The `Falling back` warning (`:158-161`) fires on `base_only` for patch > 0. The `Using …` info (`:162-164`) is not evidence of a diff.
4. **Patched content is not established.** `JsonPatch` and `JsonPatchApplier` were not opened in this seat (PatchEngine scope). The bucket set after diff application is unknown. `base_matching_buckets` is always unpatched.
5. **Bucket presence is not record usability.** `read` does not check that a retained bucket has `Funcs` or `Types`. `getFuncdef` and `getTypeDef` dereference `arch.Funcs` and `arch.Types` (`:516`, `:526`) without null checks. [INFERENCE FROM SOURCE] A malformed bucket could fail at lookup; this was not exercised on installed data.
6. **Parser strictness differs from source.** Source `GoVer.parse` accepts `1.24`, cuts `1.24.-1` to 1.24.0, and cuts `1.24.7-rc1` to 1.24.7. The preview rejects these by design, so it is not equivalent to Ghidra for those inputs. Source-derived; not run.
7. **One root only.** Ghidra's `Application.getModuleDataFile` resolves module data across directories. The preview reads one `--root`. Overrides outside that root are not modelled.
8. **Installed scope.** Bases 1.15.0 through 1.25.0. No 1.25 diffs. No 1.26 base. The `.gdt` archives (1.15 through 1.23) are not referenced on the JSON path (`:118-178`).
9. **`getApiFile` (`:183-192`)** has a patch-0 filename fallback that the snapshot path does not use. The preview must not call it.
10. **One installation.** S003, S023, and the data files share an installation origin. They are not independent witnesses. S004 (1.26 upstream support) is not installed here.
11. **Empty placeholder emitted form.** The source list contains `""` (`:109`). Whether `arch_search_order` emits it or omits it must be pinned from the `selection.py` output once it exists. Until then no emitted form is claimed.
12. **Duplicates.** Source keeps the first occurrence (`:228-237`, LinkedHashMap insertion). Duplicates arise only from degenerate GOOS/GOARCH values (for example `all`/`all`). Not exercised.
13. **Shared-root note.** The round-15 recheck line uses the same data root and the round-15 inventory's 1.24.7 result (six diffs through 1.24.6). Agreement with that inventory is a shared-source cross-check, not an independent computation.

## Routed items (round-15)

- Invocation consistency: the recheck above uses `python3 -I` with an absolute script path, as round-15 routed defect 1 asks. The append-only correction to the round-15 entry is drafted separately (`.ufo/waves/round-16/w1/CorrectionDraft.candidate.md`); this entry does not rewrite it.
- No other round-15 routed item is discharged by this entry.

Evidence: this draft; `.ufo/waves/round-16/w1/EntryDraft.md` (seat report); S003 member `GoApiSnapshot.java` as shipped with numbered anchors above; installed `typeinfo/golang` file listing, sizes, and key reads recorded in the Installed data facts above.
