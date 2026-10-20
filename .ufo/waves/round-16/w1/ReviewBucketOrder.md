# ReviewBucketOrder: matching-bucket order parity and generic `all`

Scope: source contract and installed data only. No candidate `selection.py` or `selection-fixtures.json` exists under `.ufo/waves/round-16/` at review time (glob of `round-16/**` returned claims, spec, result, dispatch, registration and `w1/swarm-registry.json`). Findings are therefore against the Java source and the proposed failure modes, with data counterexamples. Nothing was executed as a check. Data reads used `jq` (pre-existing at `/home/vgpnk/.local/bin/jq`, not installed by this review) and read-only analysis in the kernel. No file was written except this report. Installs/updates by this review: none.

Source paths: `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (plus `GoVer.java`, `JsonPatch.java`, `JsonPatchApplier.java` in the same package tree). Data: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`.

## 1. Java parity contract (what the preview must mirror)

| Behaviour | Anchor | Note |
|---|---|---|
| Search order `[goos-goarch, goos, unix-or-"", goarch, "all"]` | GoApiSnapshot.java:108-109 | Exact string match on goOS; `"unix"` only if goOS in set |
| Unix set `aix android darwin dragonfly freebsd hurd illumos ios linux netbsd openbsd solaris` | :180-181 | Excludes `windows`, `plan9`, `js`, `wasip1`. Placeholder `""` is emitted for them |
| `""` placeholder dropped at read | :218-219, :230-232 | Java keeps the placeholder in the list passed to `read`, then drops it |
| Null-valued bucket skipped | :233-236 | Present-but-null key does not match |
| Result order = search order (LinkedHashMap) | :228-237, :239 | Iteration order of `getFuncdef`/`getTypeDef` depends on this |
| First hit wins, `all` last | :514-522 (`getFuncdef`), :524-532 (`getTypeDef`) | `all` is the generic fallback only |
| Base = same minor, patch 0 | :122-126 | No cross-minor fallback |
| Patch = nearest lower existing diff, patch>0 only | :148-166, loop :153-156 | Patch 0 never consults diffs |
| Missing base → `EMPTY` (ver INVALID) | :115, :124-126 | Distinct from zero matching buckets |
| Zero matching buckets → non-EMPTY snapshot, `isInvalid()` true | :239, :503-505 | Not the same identity as `EMPTY` |
| Patch application failure → `IOException` propagates | JsonPatchApplier.java:150-152; GoApiSnapshot.java:105-111, :134-144 | Not an `EMPTY` result |
| `getApiFile` patch-0 two-part filename fallback | :183-192 | Not on the `get` path; the contract correctly excludes it |
| Module-data lookup, not a single directory | :170-171 (`Application.getModuleDataFile`) | `--root` cannot reproduce multi-root precedence |

Parity status: the search-order list, placeholder handling, base/diff selection and first-hit `all` semantics are all source-supported and consistent with the contract's stated order. The defects below concern what the preview may *claim* beyond that.

## 2. Data facts used

- All 11 base files (`go1.15.0` … `go1.25.0`) contain the key `all`. None has a bucket missing `Funcs` or `Types`, and none has a null bucket. Zero-match is therefore unreachable with shipped bases.
- Bucket key sets differ by minor. `darwin-arm64` is absent from `go1.15.0` but present from `go1.16.0`. `cgo` is absent from `go1.15.0` but present in `go1.21.0` and `go1.25.0`. `darwin-cgo` and `windows-cgo` appear in `go1.15.0` but not in `go1.25.0`. Only search-order keys matter here.
- Matching matrix (base keys present, in search order). Same for all 11 bases except where noted:
  - `linux/amd64` → `linux-amd64, linux, unix, amd64, all`
  - `windows/amd64` → `windows-amd64, windows, amd64, all` (no `unix`)
  - `darwin/arm64` → `darwin-arm64, darwin, unix, arm64, all` (`go1.15.0`: `darwin, unix, arm64, all`)
  - `freebsd/386` → `unix, 386, all`
  - `linux/riscv64` → `linux, unix, all`
  - `lnux/amd64` (typo) → `amd64, all`
  - `plan9/amd64` → `amd64, all`
  - `js/wasm` → `all` only
- Diff-level bucket structure (verified with a section parser over all 123 `patchverdiffs/*.diff`): every section path has length ≥3; second element is `Funcs` or `Types` in every case; every root bucket exists in its same-minor base. Bucket-key presence is therefore patch-invariant. Name-level presence is not (see D1).
- Diffs are base-relative. Example: `net/http/fcgi.Serve` `Position` in `go1.15.1` … `go1.15.15` diffs all have old value `…child.go:331:6`, matching `go1.15.0.json`. This supports the nearest-lower-diff model. The applier does not check old values (see D6).
- Kinds in base and diffs: only `alias`, `funcdef`, `iface`, `struct`. No `basic`.

## 3. Findings (ranked)

### D1 — HIGH (C1 boundary). Base bucket applicability does not determine patched resolution

`base_matching_buckets` is correctly labelled as unpatched, but the failure is broader. Patches change which bucket a name resolves from, through name-level removals and additions in precedence buckets (`unix`, `linux`, `windows`, `all`, etc.). Simulation: apply each diff's name-level sections (remove/replace/add at path length 3) to the base name sets and compare first-hit resolution over base∪patched names.

- Counterexample, removal exposing lower-precedence fallback to none: `go1.15.0` `linux/amd64` resolves `runtime.msigsave` to `unix` (base `unix.Funcs`, Position `$GOROOT/runtime/signal_unix.go:1020:6`). `go1.15.9.json.diff:1764` removes it. Patched `linux/amd64` resolves to none. Lookup applicability changes; base bucket list does not show it.
- Counterexample, addition under a precedence bucket: `go1.15.9.json.diff:1672` adds `internal/poll.kernelVersion` under `linux`. Base resolved none; patched resolves `linux`.
- Counterexample, addition under `all`: `go1.15.9.json.diff:1338` adds `testing.newChattyPrinter` under `all`. Base none; patched `all`.
- Counterexample, shadowing by a more specific bucket: `go1.21.13` `linux/amd64` `os.(*os.dirInfo).close` resolves `all` in base and `unix` after patch (`go1.21.13.json.diff` lines 830/3344/3777, per header search). `os.openFdAt` resolves `unix` in base and none after patch (`go1.21.13.json.diff:3342`).
- Aggregate: 120 of 123 patches change name-level resolution for at least one of `linux/amd64`, `darwin/arm64`, `windows/amd64`, `freebsd/386`. Zero-change patches in that probe: `go1.16.1`, `go1.17.1`, `go1.19.1`. Counts are over base∪patched name union, Funcs+Types. Example totals: `go1.15.9` linux/amd64 = 25 changed names; `go1.21.13` linux/amd64 = 18; `go1.21.13` windows/amd64 = 29.

Required wording and fixtures: the preview may report key presence per bucket for the base file only. It MUST NOT present that list as the resolved bucket for `exact_diff` or `fallback_diff`, and it MUST NOT claim any name resolves from a given bucket under the selected patch. A fixture that asserts base-only resolution for a patched request is invalid.

### D2 — HIGH (fixture discrimination). The proposed "unix order" fixture does not discriminate; a darwin/arm64 fixture does

- `linux/amd64`: zero Funcs/Types conflicts across bases `go1.15.0`, `go1.16.0`, `go1.19.0`, `go1.21.0`, `go1.25.0`. Wrong order among `unix`, `amd64`, and `linux-amd64` would pass.
- `darwin/arm64` in `go1.15.0` is where order is observable. `darwin`, `unix`, `arm64` and `all` all exist, and `darwin-arm64` is absent. Pairwise conflicts: Funcs 83 names, Types 40 names, all between `darwin` and `arm64`.
  - Concrete: `syscall.Chdir` in `go1.15.0.json`, `.darwin.Funcs["syscall.Chdir"].Position` = `$GOROOT/syscall/zsyscall_darwin_amd64.go:418:6`; `.arm64.Funcs["syscall.Chdir"].Position` = `$GOROOT/syscall/zsyscall_linux_arm64.go:254:6`. Java (`GoApiSnapshot.java:514-522`) returns the `darwin` value for `darwin/arm64`.
  - A candidate that places `goarch` before `goos`, or drops `darwin` because `darwin-arm64` is absent, returns the arm64 value and fails.
  - Caveat for L1: the selected `darwin` content in `go1.15.0` is amd64-generated (`zsyscall_darwin_amd64.go`). Java parity holds, but the preview must not imply arm64-accurate content.
- Zero conflicts for `darwin/arm64` in `go1.16.0` (`darwin-arm64` present), so the discriminator is specific to `go1.15.0`.

Recommended fixture: `go1.15.0`, `darwin/arm64`, `syscall.Chdir` → first hit `darwin`, not `arm64`.

### D3 — MEDIUM (parity decision). `arch_search_order` placeholder and `unix` exclusion for non-unix GOOS

- Java emits `""` in the order list for `windows`, `plan9`, `js`, `wasip1` (GoApiSnapshot.java:108-109) and drops it only at read (:230-232). The contract says "match exact search order" but does not say whether `""` appears in the emitted JSON. Choose and state one. Recommended: emit the exact Java list including `""`, since the contract says exact.
- Counterexample for including `unix` on `windows`: `archive/tar.statUnix` (in `go1.21.0` `unix.Funcs` only; absent from `windows`, `windows-amd64`, `amd64`, `all`, `linux`, `linux-amd64`, `darwin`, `darwin-arm64`, `arm64`). Java for `windows/amd64` → none. An order that adds `unix` for `windows` returns a bucket match. The `unix`-only set in `go1.21.0` Funcs has 165 names.
- Windows-only counterexample: `crypto/x509.checkChainTrustStatus` (`go1.21.0` `windows` only; 505 windows-only names). `linux/amd64` must resolve none. A candidate that treats `windows` as generic would not.

### D4 — MEDIUM (validation gap). Unknown GOOS and typos are silently accepted

- `GoApiSnapshot.get` has no GOOS validation (:108-109). `lnux/amd64` yields `amd64, all` in every base (matrix above), so generic `all`/`amd64` content would be presented as a platform match.
- `js` and `plan9` match only `arch` and `all` (or `all` alone), though they are valid Go GOOS values. This is a Java semantic, not a bug to fix in the preview, but the preview must label it.
- Recommended: the preview should validate GOOS against a known list and reject unknown values with exit 2, or else report `goos_known: false`. This is a design decision for L1 and is an extension beyond Java parity; it must be labelled as such.

### D5 — MEDIUM (status conflation). Three outcomes must stay distinct

- Missing base → `EMPTY` (GoApiSnapshot.java:115, :124-126).
- Zero matching buckets → non-EMPTY snapshot with `isInvalid()` true (:239, :503-505). Unreachable with shipped bases because every base has `all`, but a fixture root lacking `all` reaches it.
- Patch/parse failure → `IOException` (JsonPatchApplier.java:150-152; GoApiSnapshot.java:134-144). Not reachable from the preview, which applies nothing.
- The contract's status enum (`missing_base`, `base_only`, `exact_diff`, `fallback_diff`) has no zero-match status. Either add one, or document that zero-match is handled as an error (exit 2) and make sure a fixture covers it. Do not map zero-match to `missing_base`.

### D6 — LOW–MEDIUM (unverified convention). Base-relativity is a data convention, not checked by Java

- Verified empirically for one path (above). Java does not check it: `JsonPatch.java:201-206` discards `-` values (`value = null` for REMOVE), and `JsonPatchApplier.java:87-92` removes by key without comparing old content. A wrong base would apply silently.
- The preview must label base-relativity as a property of the shipped data (`patchverdiffs/` written against `goX.Y.0`), not as something the applier enforces.

### D7 — LOW (documented divergence). Strict `M.m.p` is not Java parity

- `GoVer.parse` (GoVer.java:62-81) strips everything after the first non-`[.0-9]` character (:65) and defaults a missing patch to `0` (:47, :72-74). Java therefore accepts `1.21` (as 1.21.0), `go1.21rc2`-style suffixes and `1.22.8 X:rangefunc`. The contract's strict parse rejects these. That is intentional, but it must be recorded as a divergence, and a fixture should show `1.21` rejected rather than silently treated as parity.
- `GoVer.prevPatch` (:134-136) and `toString` (:155-159) match the selection loop; no divergence there.

### D8 — LOW (scope limit). Single `--root` vs module data lookup

- Java resolves through `Application.getModuleDataFile` (GoApiSnapshot.java:170-171), which can search multiple data roots and extension precedence. The preview's single `--root` cannot reproduce that. State this in the limits section.

### D9 — LOW (latent, not triggered by shipped data). Type null fall-through

- `GoTypeDefDeserializer` returns `null` for unknown `Kind` (GoApiSnapshot.java:450-465, default at :463). `getTypeDef` (:524-531) treats a null entry as a miss and continues to lower buckets, so a higher-precedence unknown-kind entry is shadowed silently. Shipped Kinds are only `alias`, `funcdef`, `iface`, `struct`, so this does not fire. Note it for any future data drop; the preview does not resolve types.

## 4. Correction to my own scratch work (calibration)

- An early bash `comm`-based scan reported zero name-level sections absent from base across the 18 buckets. That result is wrong. The Python section-level simulation shows 25 name-level additions for `go1.15.9` linux/amd64 alone (for example `go1.15.9.json.diff:1338` and `:1672`, confirmed against the header lines and `jq` on `go1.15.0.json`). The bash scan has been discarded, and D1 relies only on the Python simulation.
- The bucket-root invariance claim was also first checked with `comm`. The Python section parser independently confirms it (0 roots missing in base; all second elements `Funcs`/`Types`), so the claim stands on the Python evidence.

## 5. Verification gaps

- No candidate `selection.py` exists to execute. The fixture-level counterexamples above are data-level expectations for L1 to test once the candidate exists.
- The Python simulation applies only name-level sections (path length 3). Field-level edits (length 4–6, 5,288 name-level vs 73,869 length-4 sections in the parse) can change content but not presence; they were not simulated for resolution, and that is intended.
- Not verified: JSON duplicate top-level keys in base files (Java and `jq` both take the last value; not checked); `Application.getModuleDataFile` resolution at runtime; Gson null-value behaviour beyond the source reading; `Position` values against Go toolchain source.
- Not verified: whether `IS_GOOS_UNIX` matches the snapshot generator's definition of `unix` for `android`, `ios`, `illumos`, `hurd` (no generator source in the shipped data).

## 6. Recommended changes for L1 integration

1. Label `base_matching_buckets` as "bucket key presence in base file only". Add a field or note that name resolution under `exact_diff`/`fallback_diff` is not computed (D1).
2. Replace or supplement the "unix order" fixture with `go1.15.0 darwin/arm64 syscall.Chdir → darwin` (D2). Keep a `windows/amd64` fixture that must not include `unix` (D3).
3. Decide and state whether `""` appears in `arch_search_order` (D3).
4. Add an explicit GOOS-known rule or `goos_known` flag (D4).
5. Add zero-match handling as a distinct outcome or error, and do not map it to `missing_base` (D5).
6. Record the strict-vs-Java divergence (`1.21` rejected) and the single-root limit (D7, D8).
