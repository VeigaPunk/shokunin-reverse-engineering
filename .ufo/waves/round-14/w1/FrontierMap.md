# FrontierMap — Non-Obvious Move: Append-Only Mapping of Go Version-Gate Diagnosis without Citation Drift or Target Recovery Overclaim

- **Seat:** `KaidokuR14.FrontierMap` (role: `connector` / UFO-FSD connector)
- **Lane path:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Report path:** `.ufo/waves/round-14/w1/FrontierMap.md`
- **Round:** Kaidoku round 14 (wave `kaidoku-r14-w1`)
- **Baseline revision:** `767adafb97e2eef6980e2ad873d357e16721c467` (HEAD)
- **Access date:** 2026-10-20 (UTC)
- **Judged on axes:** `coverage`, `calibration` (under no-harm constraint on `depth`, `operability`, `freshness`, `adjacency`)
- **Tool directive record:** 0 tools installed or upgraded. Used pre-existing host tools (`git`, `python3`, `sha256sum`, `grep`) read-only.
- **Contract & Leaf Bounds:** Leaf member; no subagent dispatch; no builds, tests, linters, formatters, or live REA target runs mid-flight (L1 integrates and verifies). Source reading, cryptographic hashes, and exact text counts only.

---

## 1. Executive Summary & Named Axes

- **Axes Evaluated:**
  1. `coverage` (C1): Admitting one source-backed knowledge entry (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`) that resolves the uncovered causal question behind the Go 1.26 symbol recovery collapse.
  2. `calibration` (C2): Ensuring exact quote fidelity, truthful attribution (source diagnosis vs. target recovery), avoiding representation confusion, and preventing citation-drift regression.
  3. *No-harm guarantee:* Preserving `depth` (17/17 rules), `operability` (recheck grading), `freshness` (stable anchors), and `adjacency` (`PROVINCE.md` boundaries).

- **The Non-Obvious Move (Synthesis across Round 14 Proposals):**
  An apparent insoluble contradiction exists between the Recipe A index requirement and the frozen citation-drift gate:
  - *Requirement A (Recipe A Index):* Adding `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` requires its token stem `2026-10-20-r14-go-version-diagnosis` to appear within the `## Coverage map` section of `corpus/README.md` (lines 11–68) to prevent dropping the coverage proxy from 10.0 to 9.89 (`missing` list).
  - *Constraint B (Citation Drift Pinning):* Adding a new table row anywhere inside `## Coverage map` (lines 11–68) or `## Knowledge` (lines 70–155) increases the line count of `corpus/README.md` by $\ge 1$, which shifts line 138 (pinned by `sc72-readme-nitrow` in `SCORECARD.md:72`), line 175 (pinned by `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2`), and line 180 (pinned by `sc69-readme-177` in `SCORECARD.md:69`). Any such insertion causes the automated `citation-drift-probe.py` gate to FAIL with `citation_dead` or `citation_out_of_range`.
  - *The Compatible Synthesis:* **Append the new entry token in-place into line 32 of `corpus/README.md`** (the existing `knowledge/2026-10-13-r4-10-real-version-pair` row), following the multi-token convention established by lines 22, 36, 42, and 64. This maps the entry into `## Coverage map` for Recipe A, directly links the source diagnosis to the historical empirical observation it corrects, maintains total file line count at exactly 191, and causes **zero line displacement** for pinned lines 22, 138, 175, and 180.

---

## 2. Local Evidence & Surface Inspection

### A. Inspection of `PROVINCE.md`
- **Line 52 (`Core` table, `Cross-version compare` row):**
  > `... real-version pair op 2.34.1→2.40.0 (41–43MB Go ELF): Go toolchain bump go1.25.7→go1.26.8 collapses provider symbol recovery 33,060→11,595 procs (11,588 FUN_*) — symbol-keyed pairing unsafe across Go versions, pair by ELF role/address (r4-10) [r5-audit C1]; REA_GHIDRA_STARTUP_TIMEOUT_MS needed past ~40MB targets (r2-08) |`
- **Line 158 (`Round-4 frontier (post-unlock)`, `Cross-version residuals`):**
  > `- **Cross-version residuals** — compare-application-versions EXERCISED on all three input classes ... multi-version pacman pairs beyond expac exercised (r4-10: op 2.34.1→2.40.0, qpdf control) [r5-audit C1: merged from the pruned Frontier bullet — its compare_javascript_export_shapes item is now held (Core, r4-09)].`
- **Line 106 (`Adjacent`):**
  > `- **Source-available reconstruction of ordinary repositories** — REA's own anti-trigger (unowned).`
- **Provincial Boundary Finding:** `PROVINCE.md` does not claim Go 1.26 symbol recovery. It records the historical collapse on `op` 2.40.0 as an empirical hazard. Under shokunin doctrine, source-code analysis of Ghidra internals (`Base-src.zip`) is a *source diagnosis* explaining tool limitations; it does **not** constitute target recovery of Go 1.26 executables. `PROVINCE.md` must remain strictly unedited: promoting Go 1.26 recovery to `Core` would be false, while adding an unheld capability to `Frontier` would contradict the fact that operator engine upgrades are unheld.

### B. Inspection of `corpus/README.md` & Pinned Citation Analysis
1. **Recipe A Extraction Logic (`SCORECARD.md:90-125`):**
   ```python
   section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
   mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
   files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
   missing = sorted(files - mapped)
   coverage_score = round(10*len(files & mapped)/len(files), 2)
   ```
   Recipe A inspects exclusively the text block between `## Coverage map\n` and `\n## `. If the new file `2026-10-20-r14-go-version-diagnosis.md` is added to `corpus/knowledge/`, its stem `2026-10-20-r14-go-version-diagnosis` MUST be matched by regex inside that block.
2. **Pinned Line Invariants in `pointer-table.json`:**
   - **Line 22:** Citing line of `readme22-r7range` and `readme22-r8range`. Must match `r7: corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:(\d+)-(\d+)`.
   - **Line 138:** Target line of `sc72-readme-nitrow` (extracted from `SCORECARD.md:72`). Must match `4 nits: 2 fixes applied at integration`.
   - **Line 175:** Citing line of `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2`. Must match `SCORECARD.md:(\d+)` and `r7-pe-wall.md:(\d+)-(\d+)`.
   - **Line 180:** Target line of `sc69-readme-177` (extracted from `SCORECARD.md:69`). Must match `held, not frontier`.
3. **Second-Order Line Displacement Arithmetic:**
   - If a new row is inserted anywhere above line 138 (e.g. at the bottom of `## Coverage map`, line 69), line 138 shifts to 139, line 175 shifts to 176, and line 180 shifts to 181. `citation-drift-probe.py` fails on 5 distinct pointer entries.
   - If a new row is appended to `## Knowledge` (after line 154), line 138 is preserved, but lines 175 and 180 shift down, failing `readme175-*` and `sc69-readme-177`.
   - If a bullet is appended at the end of the file (after line 191), lines 22, 138, 175, and 180 do not shift, but the entry is outside `## Coverage map`, which breaks Recipe A (`missing: ['2026-10-20-r14-go-version-diagnosis']`).
   - **Conclusion:** Modifying an existing row within lines 23–68 without adding newline characters is the *only* mathematically viable placement that satisfies both Recipe A and the citation-drift gate.

### C. Inspection of `corpus/SOURCES.md` & Path 2
- **Path 2 (`corpus/SOURCES.md:32-33`):**
  > `Go ≥1.26 recovery and cross-version matching — S003 → S004 → S005 → S006: inspect the installed 12.1.4 gate, compare the exact upstream GP-6528 patch, bound the independent parser by its README, then study BSim's name-free similarity model. These sources do not establish a Go 1.26 recovery run or that BSim produced the lane's REA compare findings.`
- **Registry Rows S003–S006 (`corpus/SOURCES.md:9-12`):**
  All four rows are currently `mined`, citing `corpus/lessons/round-13.md` in the `used-by` column.
  - S003: Ghidra 12.1.4 `Base-src.zip` (SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`).
  - S004: Ghidra upstream GP-6528 commit `385e8cd923d09f10b1a7874108e71748875fa174`.
  - S005: Mandiant GoReSym commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`.
  - S006: Ghidra BSim Tutorial (`BSimTutorial_Intro.md`).
- **Census Check:** As demonstrated by `BaselineMeasures.md` and `ReviewRegistry.md`, `sources-census.sh` check E11 validates that every path in `used-by` exists on disk. Appending `, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` to rows S003–S006 is valid *only after* the knowledge file is physically written to disk.

---

## 3. Sources Opened & Quotes Verified

All sources below were opened and verified on 2026-10-20:

| id | Source Location | Contiguous Quote ($\le 25$ words) | Verified SHA-256 | Limits & Epistemic Boundaries |
|---|---|---|---|---|
| S003 | Installed Ghidra 12.1.4 `Base-src.zip`, `GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` | Declared range constant in installed source archive; code analysis only; no Ghidra target execution. |
| S003 | Same archive, `GoRttiMapper.java:170-171` | `if (!SUPPORTED_VERSIONS.contains(goVer) ) { Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer)); }` | Same | Version check is a logged warning; does not throw or abort execution. |
| S003 | Same archive, `GoRttiMapper.java:358-360` | `throw new BootstrapInfoException( "Missing Go bootstrap type info, unable to extract Go RTTI info." .formatted(goVer));` | Same | Hard abort when bootstrap snapshot is missing or invalid. |
| S003 | Same archive, `GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` | Same | Returned when no JSON snapshot matches requested version, causing `isInvalid() == true`. |
| S004 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 | “GP-6528 add support for golang 1.26” | Git commit `385e8cd9…` | Upstream master commit; not present in release 12.1.4. Demonstrates patch delta, not host capability. |
| S005 | https://github.com/mandiant/GoReSym/tree/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d, README `Version Support` | ``This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.`` | README SHA `d44dd94d…` | Pinned README; note backticks around `pclntab`. Caps layout support at 1.20; does not support Go 1.26. |
| S006 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md`, line 19 | “Certain attributes, such as values of constants, names of registers, and data types, are intentionally not incorporated into the features.” | `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e` | Installed tutorial; feature normalization omits data types and names; similarity is not semantic equivalence. |

---

## 4. Synthesis of Proposed Moves & Second-Order Contradictions

| Proposal / Finding | Surface Affected | Direct Claim | Contradiction / Second-Order Impact | Synthesis / Resolution |
|---|---|---|---|---|
| **C1 Candidate Entry** (`GoEntryDraft.candidate.md`) | `corpus/knowledge/` | Adds source diagnosis for Go 1.26 symbol loss. | If integrated as a new row in `corpus/README.md`, shifts line 138 and 180, breaking `citation-drift-probe.py`. | Map token into existing line 32 of `corpus/README.md`. Zero line shift. |
| **Novelty Critique** (`AttackNovelty.md`) | `SCORECARD.md` & `claims.json` | C1 risks duplicate coverage because `r4-10` already observed the collapse. | `r4-10:70-71` speculated moduledata/pclntab layout corruption without citing source. The causal mechanism was unheld and misattributed. | State explicit coverage question: root cause of symbol collapse (version-gate warning vs. missing bootstrap snapshot vs. layout parse). |
| **Version Gate Mechanism** (`InstalledGoGate.md`) | Ghidra 12.1.4 Java AST | `SUPPORTED_VERSIONS` (line 79) stops analysis. | `GoRttiMapper.java:170-171` only logs `Msg.error`! The hard stop is `GoApiSnapshot.java:115` returning `EMPTY`, triggering `BootstrapInfoException` at line 359. | Title and diagnose entry as *missing bootstrap snapshot and version-gate logging*, avoiding the false claim that line 79 aborts. |
| **GoReSym Bounds** (`GoReSymBounds.md`) | Cross-tool comparison | GoReSym can cross-check Go 1.26 layouts. | GoReSym code reveals `-v 1.26` falls through to Go 1.1 (`ver11`) parser, corrupting type reconstruction. | Cite S005 only as bounded layout evidence ($\le 1.20$), not as a Go 1.26 corroboration (Santos-Grueiro S011). |
| **BSim Bounds** (`BSimBounds.md`) | Name-free matching | BSim provides fallback cross-version matching. | BSim vectors discard constants, types, and register names; similarity score 1.0 is not semantic equivalence. | BSim cited strictly as candidate-generation heuristic for symbol recovery, not held REA capability. |
| **Quote Gate Interface** (`ReviewS017.md` & `ReviewS018.md`) | Calibration (C2) | Gate expects Markdown `#` headings. | Pinned `View8` README has zero `#` headings (uses HTML `<h2>`/`<h3>`). `Check Point` article line numbers were rendered, not raw. | Use raw HTML headings or captured markdown fixtures; quote verbatim with backticks for S005. |

---

## 5. The Proposed Move: Exact Placement Recommendations (Not Edits)

To satisfy the round assignment without mutating shared files during the leaf flight, the following exact recommendations are provided for L1 integration:

### Recommendation 1: In-Place Placement in `corpus/README.md` (Coverage Map)
Do **not** insert a new line into `## Coverage map` or `## Knowledge`.
Update line 32 of `corpus/README.md` in place to append the new knowledge token:

```startLine:32:endLine:32:corpus/README.md
| `knowledge/2026-10-13-r4-10-real-version-pair`, `knowledge/2026-10-20-r14-go-version-diagnosis` | full compare pipeline at 41-43MB (`op` 2.34.1→2.40.0, ~6-7min per verb — every verb re-imports fresh); CLI `rea compare` caps at `status:unknown` vs domain `compareBundles`+`record_pairs` → `status:changed`; Go bump (1.25.7→1.26.8) collapses symbol recovery 33,060→11,595 procs — pair by ELF role/address, not symbol name; Go 1.26 symbol loss root-caused to Ghidra 12.1.4 missing API type snapshot and version gate, disproving moduledata/pclntab layout corruption | `rea analyze`/`search`/`function`/`compare` + domain `compareBundles`/`compareFunctions`; source diagnosis `GoRttiMapper`/`GoApiSnapshot` |
```

- **Verification:**
  - Recipe A extracts `2026-10-20-r14-go-version-diagnosis` via `re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section)`.
  - `mapped` count increases from 91 to 92. `missing` is empty `[]`. `coverage_score` remains 10.0.
  - Line 22 remains line 22. Line 138 remains line 138. Line 175 remains line 175. Line 180 remains line 180.
  - Zero citation drift.

### Recommendation 2: Append Placement in `corpus/README.md` (Known Gaps Section)
If L1 wishes to record the residual gap for Go 1.26 target analysis, append to the very end of `corpus/README.md` (after line 191):

```markdown
- Go ≥1.26 symbol recovery remains unheld — source diagnosis (2026-10-20-r14-go-version-diagnosis) proves Ghidra 12.1.4 halts on missing bootstrap snapshot go1.26.0.json; recovery waits on a host engine upgrade carrying upstream GP-6528 (operator-owned).
```

- **Line arithmetic proof:** Line 191 is EOF at HEAD. Appending at line 192 shifts zero preceding lines. All line-pinned citations remain byte-exact.

### Recommendation 3: In-Place Placement in `corpus/SOURCES.md` (Registry Table)
In `corpus/SOURCES.md`, rows S003–S006 (lines 9–12), update the 11th cell (`used-by`) in place from:
`corpus/lessons/round-13.md`
to:
`corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`

- **Precondition:** Apply this edit *strictly after* `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` has been written to disk, preventing `sources-census.sh` check E11 (`missing used-by`) from failing.
- **Verification:** Row count remains 22. Tiers remain A=20, B=1, C=1. Statuses remain mined=21, rejected=1.

### Recommendation 4: Zero Edits to `PROVINCE.md`
Make **no edits** to `PROVINCE.md`.
- `PROVINCE.md:Core` represents host-verified operational capabilities. Ghidra 12.1.4 does not recover Go 1.26 symbols.
- `PROVINCE.md:Frontier` already records the Go bump collapse in `Cross-version residuals`.
- Adding Go 1.26 recovery would be an untruthful capability assertion. Retaining `PROVINCE.md` as-is preserves province boundary integrity and calibration.

---

## 6. Risks and Mitigations

| Risk | Severity | Root Cause | Exact Mitigation |
|---|---|---|---|
| **Citation Drift Failure** | HIGH (exit 1) | Integrator inserts a new row in `## Coverage map`, shifting line 138 or line 180. | Enforce in-place token mapping into existing line 32 of `corpus/README.md`. |
| **Capability Overclaim** | HIGH (adulteration) | Claiming that source inspection of Ghidra enables Go 1.26 analysis on the host. | Strictly classify C1 as *source diagnosis*. Do not edit `PROVINCE.md` Core. Label all target execution outcomes as UNKNOWN. |
| **Census E11 Breakage** | MEDIUM (exit 1) | Editing `corpus/SOURCES.md` before the C1 knowledge file exists on disk. | Sequence integration: write knowledge file first, verify existence with `test -e`, then update `SOURCES.md`. |
| **Quote Contiguity Failure** | MEDIUM (gate rejection) | Omitting backticks in S005 quote (`pclntab`). | In C1 entry and C2 manifest, preserve exact raw bytes: `` `pclntab` ``. |
| **Multi-Tool Corroboration Fallacy** | LOW (epistemic trap) | Concluding that GoReSym and Ghidra agree on Go 1.26 layout failure. | Document that GoReSym explicitly bounds pclntab layouts at 1.20 and defaults `-v 1.26` to Go 1.1; it does not evaluate Go 1.26. |

---

## 7. Verification Steps for L1 (Integrator)

Upon integration, L1 should run the following commands sequentially:

1. **Verify Recipe A (Knowledge & Coverage Integrity):**
   ```bash
   python3 - HEAD <<'PY'
   import json, pathlib, re, subprocess, sys
   rev = sys.argv[1]
   def get(path):
       return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
   paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'], text=True).splitlines()
   files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
   section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
   mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
   print(json.dumps({'knowledge_files': len(files), 'mapped': len(files & mapped), 'missing': sorted(files - mapped), 'coverage_score': round(10*len(files & mapped)/len(files), 2)}))
   PY
   ```
   *Expected Result:* `{"knowledge_files": 92, "mapped": 92, "missing": [], "coverage_score": 10.0}`.

2. **Verify Citation-Drift Gate:**
   ```bash
   python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
   ```
   *Expected Result:* Exit 0 clean; 0 findings.

3. **Verify Source Census:**
   ```bash
   bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
   ```
   *Expected Result:* `kaidoku	ok	.../corpus/SOURCES.md`, Exit 0.
