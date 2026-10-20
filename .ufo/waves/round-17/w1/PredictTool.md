# PredictTool — predict.py report (round-17 wave 1)

## Files changed
- `kaidoku-shokunin/.ufo/waves/round-17/tools/predict.py` (new, 17,253 bytes, executable)

## What it does (contract §predict.py)
`predict.py --go-version STR [--goos linux --goarch amd64] --golang-root DIR`
normalizes STR exactly as Ghidra does, then calls r16 `select_snapshot`
and emits `{input, normalized, in_declared_range, selection, expected,
basis}` JSON (sort_keys=True, indent=2). Exit 0 emitted; 2 for
unparseable/empty version or unreadable root (JSON reason on stderr,
never a guess). `--selftest` exercises the real CLI via `sys.executable
-I` against fixture snapshot trees under `tempfile.mkdtemp()`.

## Normalization law implemented (all observation, read from Base-src.zip)
Source zip: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`,
member paths `ghidra/app/util/bin/format/golang/...`.

1. `"go"` prefix strip: `GoBuildInfo.java:488-489`
   (`versionString.startsWith("go") → substring(2)`); implemented at
   `predict.py:100-102`.
2. `GoVer.parse(s, 0)`: `GoVer.java:62-81`; implemented at
   `predict.py:105-126` (`gover_parse`):
   - `replaceAll("[^.0-9].*$", "")` (GoVer.java:64-65) →
     `_TRAILING_JUNK_RE` at `predict.py:86`. Non-multiline semantics are
     identical in Python re: `.` excludes `\n`, `$` binds before a final
     newline.
   - Java `String.split("\\.")` drops ALL trailing empty fields, so
     `"go1.2."` → parts `["1","2"]` → `1.2.0` (predict.py:115-117).
   - `parts.length < 2` → INVALID (GoVer.java:66-68).
   - `Integer.parseInt` on digit-only pieces; empty or >2^31-1 →
     NumberFormatException → INVALID (GoVer.java:77-80;
     predict.py:119-123). `parts[3:]` never read (GoVer.java:72-74), so
     `"go1.2.3.9"` → `1.2.3`.
   - Missing patch defaults to 0 via `GoVer.parse` (GoVer.java:46-48,
     missingPatchValue=0; call site `GoBuildInfo.getGoVer`,
     GoBuildInfo.java:237-238), so `"go1.21rc2"` → `1.21.0`.
3. INVALID sentinel: `major==0 && minor==0` (GoVer.java:105-107) →
   exit 2 (`predict.py:129-131`, `196-199`).
4. `"devel go1.24-abcdef"` → exit 2: it does not start with `"go"`, so no
   strip; the `d` truncates to `""` at GoVer.java:64-65 → parts `[""]`
   length 1 → INVALID. This is Ghidra's actual behavior — a `devel`-format
   binary's buildinfo version is unparseable to Ghidra, matching the
   `BootstrapInfoException` path at `GoRttiMapper.java:166-168`.

## Range/prediction law
- `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` at
  `GoRttiMapper.java:79`. Endpoints use `parseWildcardPatch`
  (GoVerRange.java:47,52) → patch −1; `contains` (GoVerRange.java:83-87)
  + `GoVer.compareTo` (GoVer.java:143-152, −1 patch compares equal) make
  the declared range effectively `1.15.x`–`1.25.x`. Replicated at
  `predict.py:76-77,142-163`.
- `expected.untested_version` = normalized string iff outside range
  (`GoRttiMapper.java:170-171` logs `"Untested Go version [%s]"` with the
  GoVer's toString).
- `expected.snapshot_label` = normalized requested label iff a base file
  exists, else null. `GoApiSnapshot.get` passes the requested `goVer`
  into `read` (GoApiSnapshot.java:111) so the logged
  `apiSnapshot.getVer()` (GoRttiMapper.java:178-180) is the requested
  version even on fallback-diff — matches contract wording.
- `expected.missing_bootstrap` = `selection.status == "missing_base"`
  per contract (`GoApiSnapshot.EMPTY` when no patch-0 base:
  GoApiSnapshot.java:115,122-126).
- Selection itself is delegated to r16
  `select_snapshot(Path(root), "M.m.p", goos, goarch)` imported by
  `importlib` from `.ufo/waves/round-16/selection.py`
  (`predict.py:89-97, 202-203`); the returned dict is embedded verbatim
  under `selection`.

## Runs performed (all by me, on this host)
1. `python3 -I .ufo/waves/round-17/tools/predict.py --selftest` →
   `SELFTEST: CLEAN cases=17`, exit 0. Covers: experiment-suffix
   truncation, rc-suffix → patch 0, missing base, fallback diff,
   `devel ...` → exit 2, empty string → exit 2, plus 11 pure
   normalization cases (incl. `go1.16.05`→`1.16.5`, `go0.0.7`→INVALID,
   `go99999999999.1.0`→INVALID).
2. `--go-version go1.27.0-X:nodwarf5` → exit 0: normalized `1.27.0`,
   `in_declared_range=false`, selection `missing_base` (no
   `go1.27.0.json` in the data dir — observation: dir tops out at
   `go1.25.0.json`, gdt files stop at 1.23), `expected={
   untested_version:"1.27.0", snapshot_label:null,
   missing_bootstrap:true}`.
3. `--go-version go1.23.12` → exit 0: normalized `1.23.12`, in range,
   `status=exact_diff` selecting `patchverdiffs/go1.23.12.json.diff`
   (sha256 `e1fdbc7e…9c53`, 111215 B) over base `go1.23.0.json`;
   `expected={untested_version:null, snapshot_label:"1.23.12",
   missing_bootstrap:false}`.
4. `--go-version go1.20.12` → exit 0: normalized `1.20.12`, in range,
   `status=exact_diff` selecting `patchverdiffs/go1.20.12.json.diff`
   (sha256 `148352d3…e82b`, 164688 B) over base `go1.20.0.json`;
   same expected shape as 1.23.12.

## Observations vs inferences
- Observation: `gover_parse` reproduces Java semantics incl. Java split's
  trailing-empty-field drop and int-range failures; verified by the
  selftest cases above.
- Observation: the `basis` list embedded in every output cites the exact
  zip members/lines above; `predict.py:165-190`.
- Inference: log-extract's `snapshot_labels` pattern `"Using Go API
  snapshot for X"` (per contract/log-extract spec) will be emitted twice
  for exact-diff cases — once by `GoApiSnapshot.java:163` (`"for %s"`)
  and once by `GoRttiMapper.java:180` (`"for version %s"`), both carrying
  the same normalized label; compare.py's contains-rule absorbs this.
- Inference: `missing_bootstrap` predicted via `missing_base` proxies
  Ghidra's `BootstrapInfoException`-producing paths only for the absent
  snapshot case; other bootstrap failures (no buildinfo, bad pclntab)
  cannot be predicted from a version string — this is inherent to the
  tool's static scope, not a gap vs contract.

## Limits / risks
- Prediction is source-law only; no carrier or Ghidra was executed (per
  contract). Real `ghidra.log` lines are the compare.py observation side.
- `parseInt` fidelity: components are digit-only post-regex, so Python's
  `int()` and Java's `parseInt` diverge only on already-excluded sign/space
  inputs — none reachable.
- `snapshot_label` predicts the *requested* label per contract; if an
  observed log instead shows only the fallback `Msg.warn` text for a
  `fallback_diff` case, compare.py would flag it — that is a real
  prediction being tested, not a bug.
- No installs performed; stdlib + `npx`/`unzip` only (unzip used
  read-only against Base-src.zip). No pacman transactions.
