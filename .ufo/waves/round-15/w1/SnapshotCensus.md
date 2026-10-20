# SnapshotCensus — installed Go snapshot inventory (round 15 C1)

Status: implemented, **not executed** by this seat. No gate, verdict, or claim
about the historical 1Password run. The parent executes the command and judges
the result.

## Files changed

| Path | Role | Identity |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py` | stdlib read-only inventory probe | SHA-256 `5d8bae44bc291a146024eb1ebedb8192488afa21c6ce56d6da8b48a5604856f0`, 19706 bytes, mode 755 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/SnapshotCensus.md` | this report | — |

No other file was written. No source registry row, corpus, skill, gate, or
fixture was modified.

## Installed layout observed

Resource directory (absolute, real, regular directory):
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`

Observed with independent read-only listing/hash sampling, not with the new
script:

| Base JSON | Bytes | `all` Funcs | `all` Types | SHA-256 |
|---|---:|---:|---:|---|
| `go1.15.0.json` | 4267141 | 12453 | 2421 | `cd070f2165716fd63643c722e50722295367fb7d36ff7a153d56178877da5b10` |
| `go1.16.0.json` | 4671548 | 12809 | 2526 | `d668acd92c30102dc85243c4ef580d5294e6c6f494d16f45a95c42959de00dee` |
| `go1.17.0.json` | 6100205 | 17231 | 2764 | `fb1f31849c303642739cfe907f810e1606eb1b34ddee41486b359bd9df28d549` |
| `go1.18.0.json` | 6325742 | 17960 | 2883 | `86a0687c9ce129bf9cf94faa20bee250fc13a298935d3b0ca3e0dee68ef91f67` |
| `go1.19.0.json` | 6469362 | 18523 | 3002 | `79c93ea499226c79e234053ea886779a26d3be363e437b102c046d8b6bb98885` |
| `go1.20.0.json` | 8875175 | 25511 | 3119 | `6def34993dd352b01f749dc44935178bdf2dbd13f585adf631798919ad6d0a32` |
| `go1.21.0.json` | 9039469 | 26243 | 3257 | `7bfe8f9a0f316ba3e6258152e35181c1d1c5c6b0bb0e6e9e95355490bb447b31` |
| `go1.22.0.json` | 9203666 | 26712 | 3426 | `c8feb28695499d1631af5ae441c8fd39c7eb75ce54dc8472673f2693e6974640` |
| `go1.23.0.json` | 9368866 | 27192 | 3532 | `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692` |
| `go1.24.0.json` | 10039962 | 28922 | 3706 | `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571` |
| `go1.25.0.json` | 10081618 | 29041 | 3741 | `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` |

`all` is present in every base and carries the largest buckets. These are
installed per-file `Funcs`/`Types` counts, not a recount of filenames.

Base count: 11 (`1.15.0` … `1.25.0`). `go1.26.0.json` does not exist in this
installation.

`patchverdiffs/` count: 123. Diffs exist only through `go1.24.6.json.diff`;
there is no `go1.25.*` and no `go1.26.*` diff. Per-minor diff counts:

| Minor | 1.15 | 1.16 | 1.17 | 1.18 | 1.19 | 1.20 | 1.21 | 1.22 | 1.23 | 1.24 | 1.25 | 1.26 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Diffs | 15 | 15 | 13 | 10 | 13 | 14 | 13 | 12 | 12 | 6 | 0 | 0 |
| Patch numbers | 1–15 | 1–15 | 1–13 | 1–10 | 1–13 | 1–14 | 1–13 | 1–12 | 1–12 | 1–6 | — | — |

The patch numbers are contiguous within each minor; the histogram's tail stops
at `go1.24.6.json.diff`.

Also present at the directory leaf: 9 legacy `golang_1.*_anybit_any.gdt` files.
They are outside the JSON scope and are reported by the tool as
`unrecognized_files`, not parsed.

## Selected Go 1.25 / 1.26 evidence

Selected version `1.25.0`: base present, size 10081618, SHA-256
`54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`.
Top-level map key count: 27. Exact sorted keys from the installed file:

```
386, all, amd64, arm, arm64, cgo, darwin, darwin-amd64, darwin-amd64-cgo,
darwin-arm64, darwin-arm64-cgo, linux, linux-386, linux-386-cgo,
linux-amd64, linux-amd64-cgo, linux-arm, linux-arm-cgo, linux-arm64,
linux-arm64-cgo, linux-cgo, unix, windows, windows-386, windows-386-cgo,
windows-amd64, windows-amd64-cgo
```

Selected version `1.26.0`: base absent. There is no base path, digest, map-key
list, or bootstrap entry to report; the tool emits `base_present: false` with
null fields and `patch_diffs_for_minor: []`.

Map-key counts vary by installed base: 1.15 has 26; 1.16–1.18 have 28; 1.19 has
29; 1.20 has 28; 1.21–1.25 have 27. The tool records each file's own list rather
than assuming the 1.25 shape.

### Bootstrap definitions by top-level key (go1.25.0)

Both named definitions occur in exactly one top-level key, `all`, and in none
of the other 26 keys:

| Definition | Container(s) | Field count | Entry keys | Position | Canonical entry SHA-256 |
|---|---|---:|---|---|---|
| `runtime.moduledata` | `all` | 45 | `Fields`, `Kind`, `Position` | `$GOROOT/runtime/symtab.go:394:6` | `668429313e6782cda7881a664d0e5ae7ef1fcd9a7d4ecf92495f3aad41d7aa19` |
| `runtime.pcHeader` | `all` | 13 | `Fields`, `Kind`, `Position` | `$GOROOT/runtime/symtab.go:374:6` | `25d43080f99eb3dda6339eee941c919213d48c6c24edb88ac12dbbd74d8eb6e0` |

Exact entry structure (canonical form, abbreviated values):

```json
{"Fields":[{"DataType":"internal/runtime/sys.NotInHeap","Name":"NotInHeap"}, ...45 items...],
 "Kind":"struct","Position":"$GOROOT/runtime/symtab.go:394:6"}
{"Fields":[{"DataType":"uint32","Name":"magic"}, ...13 items...],
 "Kind":"struct","Position":"$GOROOT/runtime/symtab.go:374:6"}
```

The complete exact entries (not a shape summary) are emitted only for these two
named definitions, at
`selection.entries[0].bootstrap_types["runtime.moduledata"].entries.all` and
`...["runtime.pcHeader"].entries.all`, with per-key `field_counts`,
`entry_keys`, and `entry_sha256`. Canonical entry bytes are 2034 and 587
respectively; the full `Types`/`Funcs` maps are never emitted. In `go1.15.0`
`runtime.pcHeader` is absent from this JSON while `runtime.moduledata` has 35
fields, so the tool does not assume either definition exists.

## Tool contract (implemented, not executed)

- `--ghidra ROOT` default
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`; only the canonical relative path
  `Ghidra/Features/Base/data/typeinfo/golang` is inspected. No fallback glob.
- `--select VERSION ...` default `1.25.0 1.26.0`; accepts `1.25`, `1.25.0`,
  `go1.25.0`, and `go1.25.0.json` forms. Selection reports base presence and
  nulls explicitly; it does not decide applicability.
- Base inventory: filename, absolute path, bytes read, SHA-256, version,
  top-level key count/list, per-container field names plus `Funcs`/`Types` entry
  counts, and an `all_bucket` summary (`present`, `funcs`, `types`). Selected
  records repeat `all_bucket` and add targeted bootstrap details.
- Diff inventory: filename, absolute path, bytes read, SHA-256, version,
  `@ ` section count, per-container section counts, and `+ `/`- ` line counts;
  a top-level `patch_diff_histogram` counts files per major.minor.
- One deterministic JSON document on stdout, `indent=2`, `sort_keys=True`,
  `allow_nan=False`, no timestamps. Exit 0 complete; exit 2 emitted-document
  error (bad root, missing resource dir, invalid selection token, read/parse
  failure).
- Hardening adopted from peer review: one `O_RDONLY|O_CLOEXEC|O_NOFOLLOW|
  O_NONBLOCK` open per file, `fstat` must say regular, digest and parse use that
  same buffer; `NaN`/`Infinity` rejected; base/header JSON catches
  `ValueError`/`RecursionError`; diff lines split on `\n` only;
  `resource_dir_realpath` reported. `SourceCustody`'s earlier signature
  mismatch was a mid-edit snapshot; the final arities are consistent
  (`parse_base` 5 parameters via `functools.partial`, `parse_diff` 3,
  `build_selection` 4, `main` passes 4).

## Source anchors (filename/selection mechanics only)

Extracted from installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`:

- `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:118-135` —
  requests base at `goVer.withPatch(0)` then applies an optional patch diff.
- `GoApiSnapshot.java:148-166` — patch-diff search walks earlier patches within
  the same major.minor; no earlier-minor fallback.
- `GoApiSnapshot.java:168-173` — module data path
  `typeinfo/golang/%sgo%s.json%s`.
- `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` —
  `GoVerRange.parse("1.15-1.25")`.
- `ghidra/app/util/bin/format/golang/GoVer.java:155-158` — filename version
  format `%d.%d.%d` or `%d.%d`.

Installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md:585`
records “Added support for Golang 1.24 and 1.25” and the JSON-instead-of-GDT
bootstrap change. These anchors describe lookup mechanics; they do not prove
any target run's outcome.

## Limits and non-claims

- File presence, byte size, and digest are installed-data observations, not
  support, compatibility, or recovery evidence.
- The installed 1.26 and 1.25-diff absences do **not** establish the cause of
  any historical run, including the round-14 1Password observations. No target,
  provider, or analyzer execution occurred, and no old analyzer log was
  replayed.
- Base JSON is parsed with Python `json`; duplicate object keys are not
  reported. Non-finite constants are rejected.
- Diff structure is not JsonPatch validity: only `@ ` headers and `+ `/`- `
  prefixes are counted; `+ ` values are not parsed and patches are not applied.
- Only non-symlink leaf entries under the canonical Base module directory are
  read. Directory path components are not symlink-checked; `resource_dir_realpath`
  exposes the resolved location. Only the installed Base `data` directory is
  inventoried.
- The tool is a probe, not a gate: it produces no pass/fail verdict and changes
  no corpus, registry, gate, or configuration.

## Proposed L1 checks (not executed here)

1. Run and determinism (expect exit 0, empty stderr, byte-identical output):
   ```sh
   python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py \
     --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC > /tmp/r15-inv-a.json
   python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py \
     --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC > /tmp/r15-inv-b.json
   cmp /tmp/r15-inv-a.json /tmp/r15-inv-b.json
   python3 -m json.tool /tmp/r15-inv-a.json > /dev/null
   ```
2. Counts and selected records:
   ```sh
   jq -e '.schema=="kaidoku-go-snapshot-inventory-v1" and .base_json.count==11 and
     .patch_diffs.count==123 and .patch_diff_histogram["1.24"]==6 and
     .patch_diff_histogram["1.25"]==null' /tmp/r15-inv-a.json
   jq -e '.selection.entries[] | select(.requested=="1.25.0") |
     .base_present==true and
     .base_sha256=="54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252" and
     .base_size==10081618 and .top_level_container_count==27 and
     (.os_arch_map_keys|length)==27 and .patch_diffs_for_minor==[] and
     .exact_patch_diff_present==false and
     .all_bucket.present==true and .all_bucket.funcs==29041 and
     .all_bucket.types==3741 and
     .bootstrap_types["runtime.moduledata"].field_counts.all==45 and
     .bootstrap_types["runtime.pcHeader"].field_counts.all==13' /tmp/r15-inv-a.json
   jq -e '[.base_json.files[].all_bucket.funcs] ==
     [12453,12809,17231,17960,18523,25511,26243,26712,27192,28922,29041]' /tmp/r15-inv-a.json
   jq -e '.selection.entries[] | select(.requested=="1.26.0") |
     .base_present==false and .base_sha256==null and
     .os_arch_map_keys==null and .bootstrap_types==null and
     .patch_diffs_for_minor==[]' /tmp/r15-inv-a.json
   ```
3. Exact-entry identity:
   ```sh
   jq -r '.selection.entries[]|select(.requested=="1.25.0")|.bootstrap_types["runtime.moduledata"].entry_sha256.all' /tmp/r15-inv-a.json
   # expect 668429313e6782cda7881a664d0e5ae7ef1fcd9a7d4ecf92495f3aad41d7aa19
   jq -r '.selection.entries[]|select(.requested=="1.25.0")|.bootstrap_types["runtime.pcHeader"].entry_sha256.all' /tmp/r15-inv-a.json
   # expect 25d43080f99eb3dda6339eee941c919213d48c6c24edb88ac12dbbd74d8eb6e0
   ```
4. Independent byte pins:
   ```sh
   sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json
   # expect 54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252
   sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.24.6.json.diff
   # expect e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6
   ```
5. Error path:
   ```sh
   python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py \
     --ghidra /nonexistent > /tmp/r15-inv-err.json; echo "exit=$?"
   # expect exit=2; jq -e '.errors[0].kind=="ghidra_root_missing"' /tmp/r15-inv-err.json
   ```
6. Read-only review: imports are only `argparse`, `functools`, `hashlib`,
   `json`, `os`, `re`, `stat`, `sys`; files are opened only through
   `os.open(..., O_RDONLY|…)` and stdout; no network, subprocess, or write call.
7. Output-scale check: expected order of 75 KB for this installation; confirm
   the only copied `Types` values are the two named bootstrap entries and that
   no full `Funcs`/`Types` map body is present.

## Coordination

`KaidokuR15.SourceCustody` and `KaidokuR15.PathSafety` reviewed the script while
it was being edited. Adopted: single-read hash/parse binding, `O_NOFOLLOW` +
regular-file check, non-finite JSON rejection, broader JSON exception catches,
`split("\n")` diff parsing, `resource_dir_realpath`, canonical-only Base path,
and the revised resolver wording. The earlier report of mismatched arities was
from an intermediate edit; the final file was read back with consistent
signatures. No tool was installed or upgraded.
