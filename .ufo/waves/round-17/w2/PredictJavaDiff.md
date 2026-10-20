# PredictJavaDiff — real-Java differential vs `tools/predict.py` GoVer normalization

Round 17 wave 2, FALSIFY lane. Target: `.ufo/waves/round-17/tools/predict.py`
(at lane revision da64646adcb19c1ede7537b799b8c7d283fe43da) `gover_parse`,
`gover_is_invalid`, `gover_to_string`, `_gover_compare`,
`supported_versions_contains`, `_strip_go_prefix`.

## Method (all retained under `.ufo/waves/round-17/w2/predict-java-diff/`)

- Extracted the REAL sources with `unzip -p` from
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`:
  `ghidra/app/util/bin/format/golang/GoVer.java` + `GoVerRange.java` (verified
  verbatim against predict.py's cited line ranges — see "Verification of the
  Python model" below).
- Compile-only stubs for the two non-parsing imports GoVer.java needs
  (`ghidra.framework.options.Options`, `ghidra.program.model.listing.Program`)
  — declared in this lane dir as `Options.java` / `Program.java`. No parsing
  behavior is stubbed; `GoVer.parse`/`isInvalid`/`compareTo`/`toString` and
  `GoVerRange.parse`/`contains` run the real bytecode. `GoBuildInfo`'s
  `.startsWith("go") → substring(2)` (GoBuildInfo.java:488-489) is replicated
  verbatim in `Harness.java`, per the assignment.
- `Harness.java` reads escaped strings from stdin (`\\`, `\n`, `\r`, `\t`,
  `u`+4hex UTF-16 units incl. surrogate pairs), runs the Java pipeline,
  prints `VALID major minor patch toString inRange` or `INVALID`
  (mirroring `ver.isInvalid()`).
- `driver.py` builds a 366-string corpus (go-prefixed after strip, rc/beta,
  ` X:` suffixes, devel strings, int-overflow, leading zeros, empty,
  whitespace, Unicode digits, all four Java line terminators `\r \u0085
  \u2028 \u2029`, VT/FF controls, astral chars), feeds it to
  `java -cp /tmp/pjd/classes Harness` (OpenJDK 21.0.12.1, `javac` 21) and to
  the in-process predict.py functions, then diffs.
- Artifacts: `corpus.txt`, `java_results.tsv`, `results.json`,
  `disagreements.tsv`, `driver.py`, `Harness.java`, stubs.
- Command (from lane dir):
  `python3 -B .ufo/waves/round-17/w2/predict-java-diff/driver.py`
  → `corpus=366 outcome_disagreements=27 internal_exceptions=7`

## Findings (all OBSERVED via the real Java, not inferred)

### F1 — `len(piece) > 10` rejects valid Java ints (9 of 27 diffs)

`predict.py:122` — `len(piece) > 10` is a false proxy for
`Integer.parseInt` overflow. `parseInt` has **no length cap**: leading zeros
are fine, so Java accepts arbitrarily long all-zero components. Python marks
them INVALID. Examples (JAVA vs PY):

| input | Java `GoVer.parse` | predict.py |
|---|---|---|
| `go1.2.00000000003` | `(1,2,3)` VALID | INVALID (exit 2) |
| `go1.20.02147483647` | `(1,20,2147483647)` VALID, inRange=true | INVALID |
| `go1.` + 5000×`0` | `(1,0,0)` VALID | INVALID |
| `go` + 20×`0` + `.1.2` | `(0,1,2)` VALID* | INVALID |

*(0,1,2) is not isInvalid → Java keeps it; predict.py exit 2.

CLI demo:
```
$ python3 -B tools/predict.py --go-version 'go1.2.00000000003' --golang-root .../golang
{"error": "unparseable Go version 'go1.2.00000000003' ... GoVer.INVALID"}   EXIT=2
# real Java: GoVer(1,2,3)
```
Direction: predict.py under-accepts. Fix direction: drop the length test;
`int(piece)` on digit-only pieces then compare `> 2147483647` (Python has no
int ceiling; CPython's 4300-digit `int()` limit is also a phantom rejection
Java doesn't have — parse length first or compare digit-stripped).

### F2 — `[^.0-9].*$` ≠ Java `replaceAll` for line terminators (18 of 27 diffs)

`predict.py:83-86` claims Java's regex is "exactly like Python's re.sub with
this pattern". FALSE. Java `.` excludes `\r`, `\u0085` (NEL), `\u2028`,
`\u2029` in addition to `\n`, and Java `$` matches before a *final* one of
those. Python `.` matches all of them and `$` only treats `\n`. So when a
junk char run contains one of Java's terminators **followed by more text**,
Java's `.*` cannot cross it: the match at that terminator needs `$` after
`.*` and fails mid-string → no replacement → `Integer.parseInt` blows on the
leftover → INVALID. Python crosses it, truncates cleanly, parses VALID:

| input | Java | predict.py |
|---|---|---|
| `go1.20\r\nx` | INVALID | `(1,20,0)` VALID, inRange |
| `go1.20\r\n` | INVALID | `(1,20,0)` VALID |
| `go1.2x\ry` | INVALID | `(1,2,0)` VALID |
| `go1.2x\u0085y` / `…\u2028y` / `…\u2029y` | INVALID | `(1,2,0)` VALID |
| `go1.2x\r.99` | INVALID | `(1,2,0)` VALID |

CLI demo: `predict.py --go-version "$(printf 'go1.20\r\nx')"` exits 0 and
emits `normalized:"1.20.0"`, `in_declared_range:true` — a real prediction
for a string Ghidra reports `GoVer.INVALID` (GoRttiMapper would take the
INVALID/untested path, not the versioned path).

Direction: predict.py over-accepts (issues snapshot predictions Ghidra
would never reach). Fix direction: replicate Java's terminator set, e.g.
`re.compile(r"[^.0-9][^\r\u0085\u2028\u2029\n]*$")`… — equivalently
`[^.0-9][^\r\n\u0085\u2028\u2029]*$` — so `.` stops at Java's terminators.
(Calibration: real `go_version` strings from `runtime.buildVersion` never
contain these bytes; the defect only bites hostile/crafted inputs, but the
docstring's "exactly like" claim is wrong as stated.)

### F3 — `gover_parse` raises instead of returning None (7 rows, same INVALID outcome)

`predict.py:122` — when the F2 regex fails mid-string, components like
`'20x'` or `'2x\r'` survive into `int(piece)`, which raises `ValueError`
instead of returning None (contract at predict.py:108-109, "or None for
GoVer.INVALID"). Observed on `go1.20x\ny`, `go1.20x\n\n`, `go1.20x\r\ny`,
`go1.2x\x85\ny`, `go1.2x\u2028\ny`, `go1.2x\u2029\ny`, `go1.2x\r\ny`.
The CLI stays correct only because `run()`'s `except ValueError`
(predict.py:252) catches the same exception type `predict()` deliberately
raises — coincidental masking; any direct importer of `gover_parse` crashes
where Java returns `INVALID`. Same validity outcome → not counted among
the 27 outcome diffs, but a real latent defect.

## Verified-correct (bounded no-findings)

Over the 366-string corpus, zero disagreement in:
- `_strip_go_prefix` (predict.py:100-102) vs GoBuildInfo.java:488-489 —
  incl. `go`, `gogo…`, `Go1.20`, `go.go1.20`.
- split semantics: trailing-`.` collapse, `..` empties → INVALID,
  `parts[:3]` truncation ("1.2.3.4.5.6" → 1.2.3 in both).
- `Integer.parseInt` boundary: `2147483647` accepted / `2147483648` rejected
  in all three positions; `±`/hex/`e`-notation truncation identical.
- `isInvalid` (`major==0 && minor==0`), `toString` ("1.2" two-component vs
  "1.2.3"), `_gover_compare` wildcard −1, and
  `supported_versions_contains` against `GoVerRange.parse("1.15-1.25")` —
  inRange agreed on every VALID row (incl. boundary minors 15/25, patches,
  `go1.20.02147483647` above).
- Unicode digits (`١.٢٠`, `１.２０`, `१.२०`), NUL, emoji (astral surrogate
  pair through the wire escape), tabs, VT `\x0b` / FF `\x0c` (both engines
  treat them as ordinary junk chars, unlike the four line terminators).

## Verification of the Python model vs the extracted source

Read directly from the zip-extracted files (OBSERVED):
- `GoVer.java:64-65` `Objects.requireNonNullElse(s,"").replaceAll("[^.0-9].*$","")`
  then `.split("\\.")`; `:66` `parts.length<2 → INVALID`; `:69-80`
  parseInt trio with `NumberFormatException → INVALID`; `:72-74`
  `parts.length>2 ? parseInt(parts[2]) : missingPatchValue` — predict.py's
  `parts[:3]`/patch logic matches except F1's length cap.
- `GoVerRange.java:43` `s.split("[+-]",-1)`, `:47-52` wildcard-patch
  endpoints / blank→ANY, `:83-87` `contains` = not-invalid && (wildcard ||
  compareTo≤0) && (wildcard || compareTo≥0) — SUPPORTED_RANGE constants and
  `supported_versions_contains` are faithful.
- `GoVer.java:143-152` compareTo wildcard `patch==-1 → equal`; `:105-107`
  isInvalid; `:154-159` toString — faithful.
- `GoBuildInfo.java:488-489` strip; `:238` `getGoVer → GoVer.parse(version)`
  (missingPatchValue=0) — faithful.

## Tooling

- No installs. Used system OpenJDK 21.0.12.1 (`/usr/bin/javac`,
  `/usr/bin/java`) — already present; `javac --version` → 21.0.12.1.
- Python run with `-B`; scratch under `/tmp/pjd/`; no carrier executed;
  no REA/Ghidra analysis run.

## Risks / scope bound

- Harness compares parse→validity→tuple→toString→inRange end to end; it
  does not exercise `select_snapshot` (r16 module) or file-system snapshot
  selection — out of this item's scope.
- F1/F2 inputs are outside what a real `runtime.buildVersion` emits; impact
  is correctness-of-model, not expected-real-carrier behavior. F3 is a
  latent crash for non-CLI callers.
