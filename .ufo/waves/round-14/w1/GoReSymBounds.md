# Round 14 — GoReSymBounds (S005 README version support, override flags, and Go 1.26 vs pclntab layout bounds)

- Seat: `KaidokuR14.GoReSymBounds` (scout; leaf member; no subagent dispatch).
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Axes evaluated: `coverage`, `calibration`.
- Scope: source analysis of S005 pinned repository commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`; no binary execution, no test suite execution, no tool installations or upgrades.
- Tooling directive record: No tools installed or upgraded. Existing system curl and standard inspection tools used.
- Access date: **2026-10-20**.

---

## 1. Source Reopened: S005 (Mandiant GoReSym)

- Repository URL: `https://github.com/mandiant/GoReSym/tree/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`
- Raw README URL: `https://raw.githubusercontent.com/mandiant/GoReSym/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d/README.md`
- Commit SHA: `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` (Author date: 2026-02-17T15:14:48Z; Committer: GitHub / Stephen Eckels).
- README SHA-256: `d44dd94d5a74577fd86fdb70cb87a3f8a683aa6f2088bb30aba722e469bd6094`.

### Opened Quotes and Exact Locations (≤25 words each)

| Source Location | Exact Heading | Contiguous Quote (≤25 words) | Limitation |
|---|---|---|---|
| `README.md:83` | `# Usage` | `* -v <version string> ("version", optional) flag will override automated version detection and use the provided version.` | CLI flag usage documentation only; does not state allowed version formats or validation logic. |
| `README.md:83-84` | `# Usage` | `Type parsing will fail if the version is not accurate.` | Author-stated caveat regarding type reconstruction sensitivity to runtime version accuracy. |
| `README.md:94-96` | `# Version Support` | `* pclntab parsing: >= Go 1.2`<br>`* moduledata location: >= Go 1.2`<br>`* moduledata type parsing: >= Go 1.5` | High-level minimum compatibility claims; specifies lower bounds, not upper bounds or post-1.20 support. |
| `README.md:101` | `# Version Support` | ``This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.`` | Enumerates parser layout support; explicitly caps handled pclntab layouts at 1.20 ("current" is author's original phrasing). |
| `README.md:101-102` | `# Version Support` | `Note that the pclntab version is always <= the Go runtime version (ex: Go runtime 1.19 uses the 1.18 pclntab layout),` | Establishes crucial conceptual decoupling between Go runtime release version and internal pclntab layout version. |
| `README.md:102` | `# Version Support` | `we aim to _always support the latest runtime versions_.` | Aspirational statement of intent, not an empirical proof or verified claim of Go 1.25 or Go 1.26 compatibility. |
| `README.md:124` | `# Changes` | `* Added parsing support for Go 1.24 binaries while retaining compatibility with older 1.2 layouts.` | Change log entry documenting Go 1.24 as the highest version explicitly added in this lineage. |

---

## 2. Evidence-Backed Code Investigation of S005

Beyond the README prose, code inspection of commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` reveals the exact mechanics of Go version handling, pclntab parsing, and the `-v` override flag.

### A. Pclntab Version Enum and Magic Detection (`debug/gosym/pclntab.go`)

- **Enum definition (`lines 28–37`)**:
  ```go
  type version int
  const (
      verUnknown version = iota
      ver11
      ver12
      ver116
      ver118
      ver120
  )
  ```
  [OBSERVED FACT] No version constants exist above `ver120`. There is no `ver124`, `ver125`, or `ver126`.
- **Magic constants (`lines 203–208`)**:
  `go12magic = 0xfffffffb`, `go116magic = 0xfffffffa`, `go118magic = 0xfffffff0`, `go120magic = 0xfffffff1`.
- **Magic detection (`lines 264–269`)**:
  Matches `go120magic` (0xfffffff1) in little-endian or big-endian, setting `possibleVersion = ver120`.

### B. The `-v` Override Flag Defect on Go ≥1.25 (`debug/gosym/pclntab.go:272–302`)

In `parsePclnTab(versionOverride string)`:
```go
if len(versionOverride) > 0 {
    if strings.Contains(versionOverride, "1.24") ||
        strings.Contains(versionOverride, "1.23") ||
        strings.Contains(versionOverride, "1.22") ||
        strings.Contains(versionOverride, "1.21") {
        t.Version = ver120 // Go 1.21+ shares the 1.20 pclntab layout.
    } else if strings.Contains(versionOverride, "1.20") {
        t.Version = ver120
    } else if strings.Contains(versionOverride, "1.19") {
        t.Version = ver118
    // ... branches for 1.18 down to 1.11 ...
    } else {
        t.Version = ver11
    }
}
```

- **Observed behavior when `-v 1.26` (or `-v 1.25`) is passed**:
  1. `strings.Contains(versionOverride, "1.24")` through `"1.11"` all evaluate to `false`.
  2. Execution falls into the unhandled `else` block: `t.Version = ver11` (Go 1.1).
  3. Method `isGo12(versionOverride)` evaluates `t.Version >= ver12`, which evaluates to `false` for `ver11`.
  4. In `debug/gosym/symtab.go:354`, `t.Go12line` is not assigned and remains `nil`.
  5. In `objfile/objfile.go:258`, `PCLineTable` filters candidate tables:
     `if err != nil || parsedTable.Go12line == nil { continue }`.
     Every candidate is discarded.
  6. In `main.go:263`, `finalTab` is `nil`, returning `fmt.Errorf("no valid pclntab found")`.
- [OBSERVED FACT]: The `-v` override flag in S005 actively breaks Go 1.25 and Go 1.26 binaries. Rather than forcing the 1.20 pclntab layout, passing `-v 1.26` forces fallback to `ver11`, causing fatal parsing abortion.

### C. Automated Version Detection on Go 1.26 (Without `-v`)

If `-v` is NOT passed:
1. `main.go:110–155` extracts `extractMetadata.Version` from `buildinfo` or raw binary strings (e.g. `"1.26"`).
2. Because `versionOverride` is empty, `parsePclnTab` does not hit the `versionOverride` branch.
3. The binary's pclntab magic `0xfffffff1` matches `go120magic`, setting `t.Version = ver120`.
4. Header parsing executes `case ver118, ver120:` (`pclntab.go:315–325`). Notice that GoReSym sets `t.textStart = t.PC` instead of reading `textStart` from offset 2 of the header.
5. Function symbols and source lines in `pclntab` are extracted using the 1.20 table layout.
6. `ModuleDataTable` (`objfile/objfile.go:297`) receives `version = "1.20"` (from `TabMeta.Version`). It matches `case "1.20":` and parses `moduledata` via `parseModuleDataGeneric`.

### D. Downstream Failure on Types and Structs for Go ≥1.25

Even if function symbols are recovered via automated detection under the 1.20 layout, type parsing (`-t`) fails on Go 1.26:
1. **`getRtypeLayout(runtimeVersion)` (`objfile/layouts.go:710–728`)**:
   ```go
   switch runtimeVersion {
   // ...
   case "1.20", "1.21", "1.22", "1.23", "1.24":
       layoutName = "1.20"
   default:
       return nil
   }
   ```
   For `"1.26"` (or `"1.25"`), `getRtypeLayout` returns `nil`.
   In `ParseType_impl` (`objfile/objfile.go:661–663`):
   ```go
   layout := getRtypeLayout(runtimeVersion)
   if layout == nil {
       return parsedTypesIn, fmt.Errorf("Unknown runtime version: %s", runtimeVersion)
   }
   ```
   All type extraction immediately fails.
2. **`readRTypeName` (`objfile/objfile.go:475–571`)**:
   The version switch has cases only up to `"1.24"`. For `"1.26"`, it falls through to:
   `return "", fmt.Errorf("Failed to read name")`.
3. **Interface and Struct Reconstruction (`objfile/objfile.go:907, 1078`)**:
   Switch cases only extend up to `"1.24"`.

---

## 3. Bounding the Claim about Go 1.26 vs pclntab Layout

### The Decoupling of Runtime Version vs pclntab Layout

1. **Pclntab layout stability**:
   The pclntab format does NOT change with every Go release. Go has historically retained layouts across multiple major versions:
   - Go 1.2 layout: Go 1.2 through Go 1.15.
   - Go 1.16 layout: Go 1.16 through Go 1.17.
   - Go 1.18 layout: Go 1.18 through Go 1.19.
   - Go 1.20 layout: Go 1.20 through Go 1.26 (reusing magic `0xfffffff1`).
2. **Header evolution in Go 1.26**:
   As established in upstream Ghidra GP-6528 (S004 commit `385e8cd923d09f10b1a7874108e71748875fa174`), Go 1.26 removes `textStart` from `GoPcHeader` (`presentWhen = "1.18-1.25"`). GoReSym does not read `textStart` from the table header in `ver118, ver120` (it sets `t.textStart = t.PC`), which prevents immediate header offset miscalculation.
3. **Pclntab layout compatibility != Tool support for Go 1.26**:
   - GoReSym's ability to read function symbols from a Go 1.26 binary is an artifact of Go 1.26 preserving the Go 1.20 pclntab table magic and layout.
   - It is NOT evidence that GoReSym supports Go 1.26.
   - Specifically:
     a) The `-v 1.26` flag breaks parsing completely (fallback to Go 1.1).
     b) Type parsing (`-t`) hard-fails with `Unknown runtime version: 1.26`.
     c) Type name resolution hard-fails with `Failed to read name`.
     d) Struct and Interface reconstruction fails due to missing switch branches.
     e) GoReSym commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` contains no test binary, CI job, or fixture beyond Go 1.22/1.24 (`main_test.go:14` tests `118`, `119`, `120`, `121`, `122`).

---

## 4. Findings Summary (Observed Facts vs Inferences vs Unknowns)

### Observed Facts
- [OBSERVED FACT F1] S005 README at commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` explicitly bounds its pclntab handlers: `"pre 1.2, 1.2, 1.16, 1.18, and 1.20"`. It claims no layout version above 1.20.
- [OBSERVED FACT F2] S005 README changelog names Go 1.24 as the latest version added (`"Added parsing support for Go 1.24 binaries"`).
- [OBSERVED FACT F3] S005's version override flag (`-v`) in `debug/gosym/pclntab.go` only recognizes versions up to `1.24`. Passing `-v 1.25` or `-v 1.26` falls into `else { t.Version = ver11 }`, dropping all candidate tables and failing with `"no valid pclntab found"`.
- [OBSERVED FACT F4] S005's type reconstruction engine (`objfile/layouts.go:723`, `objfile/objfile.go:568, 662`) has explicit version checks that terminate at `1.24`. Any version string > 1.24 causes `getRtypeLayout` to return `nil` and type parsing to return an error.

### Inferences
- `[INFERENCE I1]` Function symbol recovery on Go 1.26 stripped binaries under GoReSym can only succeed if automated version detection is allowed to run (without `-v`) and if the user requests symbol extraction without type parsing (`-t` omitted), because Go 1.26 retains the `0xfffffff1` magic.
- `[INFERENCE I2]` The README statement `"we aim to always support the latest runtime versions"` is forward-looking developer intent, not a specification of held capability at commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`.

### Remaining Unknowns
- Unexamined commits or releases in upstream Mandiant GoReSym created after commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` (2026-02-17) were not opened or evaluated; S005 is strictly bounded to the pinned commit.
- Dynamic runtime execution on actual compiled Go 1.26 ELF/PE/Mach-O binaries was not performed (in strict adherence to the "No install/run" directive).

---

## 5. Input for Round 14 Integration (C1 & C2)

- **For C1 (Knowledge Entry `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`)**:
  S005 provides strong, falsifiable proof of the architectural distinction between:
  1. The **Go runtime release version** (e.g. Go 1.26).
  2. The **pclntab layout version** (e.g. layout 1.20, reused across 1.20–1.26).
  3. The **RTTI/type layout version** (which changed in Go 1.24 with Swiss tables and changed further in Go 1.26, causing independent third-party parsers like GoReSym to fail during type extraction even when function table parsing succeeds).
- **For SOURCES registry (S005 row)**:
  Retains status `mined`. `teaches` cell accurately notes: `"A second parser's own stated layout range is a route to study, but does not establish Go 1.26 support."` This report rigorously confirms that limit through AST and source trace.
