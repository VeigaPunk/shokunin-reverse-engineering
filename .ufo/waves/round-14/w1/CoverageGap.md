# CoverageGap — Bounded Sweep of Go Differential Diagnosis & C1 Novelty

- **Seat:** `KaidokuR14.CoverageGap` (role: `scout`, Godspeed-enabled leaf member)
- **Judged on axes:** `coverage`, `calibration`
- **Lane path:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Report path:** `.ufo/waves/round-14/w1/CoverageGap.md`
- **Measured baseline revision:** `767adafb97e2eef6980e2ad873d357e16721c467` (HEAD)
- **Access date:** 2026-10-20
- **Tool directive:** 0 tools installed or upgraded. Existing host tools (`git`, `python3`, `unzip`, `sha256sum`, `grep`) used read-only.

---

## 1. Executive Findings

1. **Exact Go Unsupported-Version + Missing-Snapshot Differential Diagnosis Entry Absence (Factual Sweep):**
   - A bounded sweep of `corpus/README.md` (Coverage map, Knowledge table, Frontier, Known gaps) and all 91 knowledge files under `corpus/knowledge/` confirms that **no exact Go unsupported-version + missing-snapshot differential diagnosis entry exists** in the repository.
   - Specifically, `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` is currently absent from disk and Git history (`test -e` exit 1).
   - Zero files in `corpus/knowledge/` mention `GoRttiMapper`, `GoApiSnapshot`, or `differential diagnosis`.
   - Zero files in `corpus/knowledge/` cite registry rows `S003`, `S004`, `S005`, or `S006`.

2. **C1 Novelty Verdict:**
   - **CONFIRMED (Novelty is NOT falsified).**
   - Claim C1 ("source-backed Go recovery version-gate diagnostic entry on uncovered source-diagnosis ground; literature/source analysis only, no new REA target execution") targets genuinely uncovered ground.

3. **Matching Uncovered Coverage-Map Question:**
   - **Section:** `Coverage map` > `Cross-version diff` (and related `Provider readiness: Ghidra 12.1.4 Go decompiler RTTI recovery`).
   - **Historical Precursor & Gap:** Entry `2026-10-13-r4-10-real-version-pair.md` empirically observed that a Go toolchain bump (1.25.7 → 1.26.8 in 1password-cli `op` 2.34.1 vs 2.40.0) caused Ghidra 12.1.4 procedure name recovery to collapse (33,060 names down to 11,595, with 11,588 auto-named `FUN_*`), and noticed a transient log line `Missing Go bootstrap type info, unable to extract Go RTTI info`. However, `r4-10` *inferred without source inspection* that Ghidra "cannot parse the Go 1.26 moduledata/pclntab layout".
   - **The Uncovered Question:** *"What is the exact causal mechanism of Ghidra 12.1.4's Go 1.26 symbol/RTTI recovery collapse: is it an unsupported version-gate rejection (`GoRttiMapper.java`), a missing precomputed API type snapshot (`GoApiSnapshot.java`), or a binary layout/pclntab parsing failure?"*
   - **Resolution via S003 Source Ground:** Ghidra 12.1.4's source (`Base-src.zip`) establishes that `GoRttiMapper.java:79` hard-gates `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`. For Go 1.26, the analyzer logs an untested version, finds no bundled `go1.26.0.json` snapshot in `GoApiSnapshot.get`, returns `GoApiSnapshot.EMPTY`, and throws `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")` in `initStructMappings()`. The recovery collapse is caused by the version gate and absent bootstrap snapshot, correcting `r4-10`'s layout-parsing speculation.

---

## 2. Bounded Sweep Methodology & Evidence

A broad file-by-file review was avoided; bounded targeted queries were executed over `corpus/README.md` and `corpus/knowledge/`:

### A. Coverage Map and Knowledge Index Sweep (`corpus/README.md`)
- `corpus/README.md:33`: Under `## Coverage map` > `Cross-version diff`, cites `knowledge/2026-10-13-r4-10-real-version-pair`:
  > "Go bump (1.25.7→1.26.8) collapses symbol recovery 33,060→11,595 procs — pair by ELF role/address, not symbol name"
- `corpus/README.md:42`: Under `## Coverage map` > `Evidence model`, cites `2026-10-19-arc3-r12-go-evidence-id-domain`.
- `corpus/README.md:63`: Under `## Coverage map`, cites `knowledge/2026-10-16-l7-01-inspect-go-binary` (inline build metadata in `/usr/bin/docker`).
- `corpus/README.md:140`: In `## Knowledge` table, summarizes `2026-10-13-r4-10-real-version-pair`.
- `corpus/README.md:147`: In `## Knowledge` table, summarizes `2026-10-16-l7-01-inspect-go-binary`.
- **Finding:** No row in `corpus/README.md` covers a Go version-gate diagnostic entry, decompiler bootstrap snapshot analysis, or differential diagnosis between parser layout vs version check.

### B. Corpus Knowledge File Census & Targeted Search
1. Total files in `corpus/knowledge/`: **91** `.md` files (verified via `git ls-tree -r --name-only HEAD -- corpus/knowledge | grep -c '\.md$'`).
2. Search for exact symbols and diagnosis terms across `corpus/knowledge/`:
   - `GoRttiMapper`: **0 matches**
   - `GoApiSnapshot`: **0 matches**
   - `differential diagnosis` / `differential-diagnosis`: **0 matches**
   - `unsupported-version` / `version-gate`: **0 matches** related to Go
   - `Missing Go bootstrap type info`: **1 match** (`2026-10-13-r4-10-real-version-pair.md:72`)
3. Review of the 3 existing Go-referencing knowledge entries:
   - `2026-10-13-r4-10-real-version-pair.md`: Analyzes cross-version diffs on 41–43 MB Go ELFs; documents 33k→11k symbol collapse; records the transient log message as "observed-not-cited"; speculates layout incompatibility; no source code or version-gate mechanics investigated.
   - `2026-10-16-l7-01-inspect-go-binary.md`: Analyzes REA 6.5.0 extraction of embedded Go build metadata (`/usr/bin/docker`); explicitly notes metadata extraction is not runtime behavior or compiler verification; no decompiler/RTTI analysis.
   - `2026-10-19-arc3-r12-go-evidence-id-domain.md`: Investigates Evidence ID reproducibility and 3-field path sensitivity for `inspect_go_binary`; no Ghidra Go analyzer analysis.

---

## 3. Grounding of the Coverage Gap: S003 Source Examination

Sources opened to verify the differential diagnosis between unsupported version, missing snapshot, and layout parsing:

### Source 1: S003 — Ghidra 12.1.4 Base Source Archive
- **Path:** `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
- **Archive SHA-256:** `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (verified via `sha256sum`, 7,481,132 bytes)
- **Access date:** 2026-10-20
- **Member 1:** `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`
  - *Location (Line 79):*
    Contiguous quote (9 words):
    > `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`
  - *Location (Lines 170–172):*
    Contiguous quote (15 words):
    > `if (!SUPPORTED_VERSIONS.contains(goVer) ) { Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer)); }`
  - *Location (Lines 356–360):*
    Contiguous quote (20 words):
    > `if (apiSnapshot.isInvalid()) { throw new BootstrapInfoException( "Missing Go bootstrap type info, unable to extract Go RTTI info." .formatted(goVer)); }`
- **Member 2:** `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`
  - *Location (Lines 114–116):*
    Contiguous quote (5 words):
    > `return GoApiSnapshot.EMPTY;`
  - *Location (Lines 123–126):*
    Contiguous quote (9 words):
    > `if (jsonFile == null) { return null; }`
- **Limitations:** Source reading verifies the Java control flow and declared constants of Ghidra 12.1.4; it does not execute Ghidra or prove target behavior under live memory execution.

### Source 2: Historical Entry `2026-10-13-r4-10-real-version-pair.md`
- **Path:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`
- **Access date:** 2026-10-20
- **Location (Lines 70–73):**
  Contiguous quote (21 words):
  > `Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout (transient Missing Go bootstrap type info, unable to extract Go RTTI info`
- **Limitations:** Historical analysis entry from round 4; reflects operator observation of Ghidra log output and decompiler procedure counts without access to or inspection of Ghidra's Base source archive.

### Source 3: Source Registry `corpus/SOURCES.md`
- **Path:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`
- **Access date:** 2026-10-20
- **Location (Row S003, `teaches` column):**
  Contiguous quote (18 words):
  > `Inspect the installed parser's declared Go range and missing-snapshot path before attributing recovery loss to a binary layout change.`
- **Limitations:** Registry row establishes curated study scope and provenance; as documented in `corpus/lessons/round-13.md`, registry curation alone did not admit knowledge entries.

---

## 4. Structured Evaluation: Observations, Inferences, and Unknowns

| Class | Statement | Evidence Basis |
|---|---|---|
| **OBSERVATION** | No existing knowledge entry in `corpus/knowledge/` or row in `corpus/README.md` provides a source-backed Go version-gate differential diagnosis. | Bounded `grep` and `glob` sweep of `corpus/README.md` and 91 `corpus/knowledge/*.md` files; zero matches for `GoRttiMapper` / `GoApiSnapshot`. |
| **OBSERVATION** | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:70-73` observed 33,060→11,595 procedure collapse and transient `Missing Go bootstrap type info` on `go1.26.8`, but attributed it to moduledata/pclntab layout parsing failure. | Pinned text at `2026-10-13-r4-10-real-version-pair.md:70-73`. |
| **OBSERVATION** | In Ghidra 12.1.4, `GoRttiMapper.java:79` specifies `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`. | Pinned source in `Base-src.zip` (SHA-256 `f00d29c2...`), line 79. |
| **OBSERVATION** | In Ghidra 12.1.4, `GoApiSnapshot.java:get` returns `GoApiSnapshot.EMPTY` when the JSON snapshot file for a version is absent (`jsonFile == null`), causing `apiSnapshot.isInvalid()` to be true and `initStructMappings()` to throw `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`. | Pinned source in `Base-src.zip`, `GoApiSnapshot.java:115,124` and `GoRttiMapper.java:356-360`. |
| **OBSERVATION** | Sources S003, S004, S005, and S006 were registered as `mined` in round 13 (`corpus/SOURCES.md`), but no corresponding `knowledge/` entry was admitted in round 13. | `corpus/lessons/round-13.md:19-21` and `corpus/lessons/round-13-verifier-spotcheck.md:13`. |
| **INFERENCE** | The Go 1.26 procedure recovery collapse observed on `op-2.40.0` was caused by Ghidra 12.1.4's version gate and missing bootstrap snapshot, not a failure to parse the binary's pclntab or moduledata layout. | Triangulation of `r4-10` log observation with `GoRttiMapper.java:79,170,358` and `GoApiSnapshot.java:115`. |
| **INFERENCE** | Admitting `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` closes an authentic coverage gap on the "Cross-version diff" / "Provider readiness" boundary without duplicating any existing entry. | Absence of prior diagnostic entry + confirmed alignment with S003 teaching. |
| **UNKNOWN** | Whether patching `SUPPORTED_VERSIONS` in Ghidra and generating a synthetic Go 1.26 snapshot JSON would fully restore all 33,060 symbols on `op-2.40.0`, or if secondary pclntab/moduledata differences would subsequently fail. | Source reading identifies the primary gate; runtime target execution was not performed. |
| **UNKNOWN** | The exact behavior of uninspected Go versions `<1.15` under Ghidra 12.1.4's version gate and snapshot loader. | Only versions in the context of the S003 range (`1.15-1.25`) and observed `1.26` were analyzed. |

---

## 5. Conclusion & Handoff to L1 / Integrator

- **C1 novelty is verified:** The proposed entry `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` covers ground not held by any existing entry in `corpus/README.md` or `corpus/knowledge/`.
- **Coverage-map question identified:** Resolves the root cause of the Go 1.26 symbol recovery collapse first recorded in `r4-10`, distinguishing the hard version gate (`GoRttiMapper.java:79`) and missing snapshot path (`GoApiSnapshot.java:115,124`) from binary layout incompatibility.
- **Verification checks:** No build, test, linter, or live REA target execution was run; all assertions are grounded in static source checks, file hashes, and text coordinates.
