# ClaimSeparation — Causal Separability of C1 vs C2, Counting Recipes, and Score Inflation Defense

- **Seat:** `KaidokuR14.ClaimSeparation`
- **Role:** UFO-FSD Connector (leaf member; Godspeed-enabled; no subagent dispatch)
- **Round:** Kaidoku round 14 (wave `kaidoku-r14-w1`)
- **Lane path:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Report path:** `.ufo/waves/round-14/w1/ClaimSeparation.md`
- **Baseline commit:** `767adafb97e2eef6980e2ad873d357e16721c467` (HEAD)
- **Access date:** 2026-10-20
- **Tool directive record:** 0 tools installed or upgraded. Existing host tools (`git`, `python3`, `sha256sum`, `grep`, `awk`) used read-only.
- **Contract & bounds:** Leaf connector; only this report is written. No shared files, LOG, SCORECARD, corpus, fleet files, MANIFEST, or sibling files modified. No builds, tests, linters, gate executions, or live REA/target operations run.

---

## 1. Declared Axes (Godspeed Step 1)

1. **`coverage` (Primary for C1):** Discrete observable increment (0 → 1) representing the addition of one source-backed Go version-gate and bootstrap-snapshot differential diagnosis entry (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`) on uncovered source-diagnosis ground, without REA target execution.
2. **`calibration` (Primary for C2):** Discrete observable increment (0 → 1) representing an executable quote-location fidelity gate (`quote-fidelity.py`) plus a grounded `corpus/QUALITY.md` admission criterion that mechanically rejects the historical round-13 S017 splice and S018 mislocation while admitting corrected contiguous located quotes.
3. **No-Harm Invariant:** Unworked axes (`depth`, `operability`, `freshness`, `adjacency`) must remain strictly unharmed. Owned finite structural proxies in `SCORECARD.md` remain at saturation (10.0).

---

## 2. Sources Opened (Fresh Opens, 2026-10-20)

| id | Source location / identity | Contiguous quote (≤25 words) | Access date | Limitations |
|---|---|---|---|---|
| C1/C2 Claims | `.ufo/waves/round-14/claims.json:8-25` | `source-backed Go recovery version-gate diagnostic entry on uncovered source-diagnosis ground; literature/source analysis only, no new REA target execution` | 2026-10-20 | Pinned round specification; defines claim IDs, axes, before/after values, and limits. |
| Scorecard Saturation | `SCORECARD.md:2102-2104` | `All owned proxies sit at 10.0 and no capability row has entered since arc2-r8, so the AXES.md §stagnation nudge applies` | 2026-10-20 | Pinned scorecard baseline; establishes that owned proxy scores are saturated at 10.0. |
| Measurement Recipe A | `SCORECARD.md:88-90` | `This reads immutable Git objects, not a moving worktree, and never executes the inspected native library.` | 2026-10-20 | Normative counting recipe for knowledge mapping and rule citation resolution. |
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` (`GoRttiMapper.java:79`) | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | 2026-10-20 | Shipped source archive (SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`); Java code, not a live binary. |
| S003 | Same archive, `GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` | 2026-10-20 | Return path when base JSON is absent; causes `apiSnapshot.isInvalid() == true`. |
| S004 | GitHub commit `385e8cd923d09f10b1a7874108e71748875fa174` (2026-03-03) | `GP-6528 add support for golang 1.26` | 2026-10-20 | Upstream master commit; establishes master change scope, not host-held Ghidra 12.1.4 capability. |
| S005 | Mandiant GoReSym README at commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`, section `Version Support` | `This library current handles the pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.` | 2026-10-20 | Documented tool boundary; source text includes inline backticks; tool was not run against Go 1.26. |
| S006 | Ghidra BSim Tutorial (`BSimTutorial_Intro.md:19-20`) | `names of registers, and data types, are intentionally not incorporated into the features.` | 2026-10-20 | Installed doc; teaches feature abstraction; cosine similarity is candidate matching, not semantic proof. |
| S017 | Pinned View8 README (`ef39099b4f5076042173f9113382ebeb0630a56d:40`) | `Replace address-derived function identifiers with deterministic names based on parse order.` | 2026-10-20 | Raw README (SHA-256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b`); file uses HTML tags (`<h2>`, `<h3>`), zero `#` headings. |
| S018 | Check Point research article (`s018-raw.html:489`) | `The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.` | 2026-10-20 | Captured HTML (SHA-256 `31b8231560a20de10456e2911eaef007651d9029ba8e9754e1acb4434a74dd5e`); heading is `<h1 class="wp-block-heading">Introduction</h1>`. |
| Round 13 Errata | `corpus/lessons/round-13.md:63-66` | `These append-only corrections supersede the S017 quote and S018 location printed in the original Gate table.` | 2026-10-20 | Historical errata documenting S017 splice and S018 mislocation corrections. |
| Spotcheck Review | `corpus/lessons/round-13-verifier-spotcheck.md:13-14` | `Review found S017's spliced quotation and S018's mislocated exact quote.` | 2026-10-20 | Non-author spot-check establishing that L2 author seats cannot provide outside admission. |

---

## 3. Causal Separability Analysis: C1 Go Entry vs C2 Quotation Gate

Testing causal separability requires proving whether the success, failure, modification, or withdrawal of C1 affects C2, and vice versa. We trace five distinct interaction surfaces:

### A. Artifact Substrate & Filesystem Separation
- **C1 Artifacts:** Literature/source-backed knowledge entry at `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, four updated `used-by` table cells in `corpus/SOURCES.md` (rows S003–S006), one map row and one knowledge table row in `corpus/README.md`, and an addendum decision table in `SKILL.md`.
- **C2 Artifacts:** Standalone Python CLI script at `.ufo/waves/round-14/tools/quote-fidelity.py`, test fixture directory at `.ufo/waves/round-14/fixtures/` with manifests and captured source excerpts, and one appended criterion row (16) in `corpus/QUALITY.md`.
- **Finding:** C1 and C2 share **zero target files**. Their write sets are completely disjoint.

### B. Verification Surface Decoupling (The Firewall Invariant)
- **The Dependency Question:** Does verifying C1 require running C2's gate? Does verifying C2 require inspecting C1?
- **Analysis:**
  1. C2's gate contract (`spec.json`) requires input sources to be *UTF-8 Markdown excerpts* whose section is an *exact Markdown heading text including `#`*.
  2. C1 cites sources that are fundamentally heterogeneous:
     - S003 is Java code inside a zip archive (`Base-src.zip`). It has NO Markdown headings.
     - S004 is an upstream Git commit diff.
     - S005 is a Markdown README containing inline backticks around `pclntab`.
     - S006 is a tutorial document.
  3. If C2's quote-fidelity machine gate were run directly against C1's entry or C1's sources, it would immediately fail or throw `invalid_manifest` / `quote_location_mismatch`.
  4. C2 is designed and scoped strictly as an instrument to evaluate **local captured fixture excerpts in `.ufo/waves/round-14/fixtures/`** against frozen regression manifests (`manifest-red.json` and `manifest-corrected.json`).
  5. C1's source diagnosis is verified through Git tree inspection, source code line citation checks in `Base-src.zip`, and registry census checks (`sources-census.sh validate`).
- **Conclusion:** C1 and C2 are **strictly decoupled at the verification layer**. A failure or defect in C1's text cannot cause C2's gate to fail. A parser limitation in C2 cannot invalidate C1's source findings.

### C. Registry Surface Decoupling (`corpus/SOURCES.md`)
- C1 modifies rows 9–12 (`S003`, `S004`, `S005`, `S006`), appending `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` to their `used-by` cells. All four rows remain tier A, status `mined`.
- C2 involves `S017` (line 23) and `S018` (line 24). As established by `ReviewRegistry.md` and `ReviewS017.md`, S017 and S018 already have valid topic anchors and their `used-by` points to `corpus/lessons/round-13.md`. They require **zero edits** in `SOURCES.md`.
- **Finding:** Registry deltas operate on disjoint rows with zero merge conflict or cross-dependency.

### D. Normative Governance vs Machine Enforcement
- C2 appends criterion 16 to `corpus/QUALITY.md`:
  > "A quote-bearing claim is admitted only when the registered quote-fidelity gate exits 0 for the frozen manifest carrying it... Exit 1 rejects: quote_not_contiguous... quote_location_mismatch..."
- While QUALITY criterion 16 establishes the *normative human/author admission standard* that quotes must be contiguous and located inside their declared sections, its *automated machine enforcement* via `quote-fidelity.py` is bounded to manifest-declared Markdown excerpts.
- C1 complies with the normative standard of criterion 16 (verbatim quotes, exact line/member anchors, no splices), but its proof is rooted in the Java archive digest and file offsets, not a C2 manifest run.

### E. Index Integrity & Metric Decoupling
- Measurement Recipe A (`SCORECARD.md:86-125`) monitors `corpus/knowledge/*.md` vs `corpus/README.md:## Coverage map`.
- C1 adds one knowledge file; to maintain `coverage_score: 10.0`, C1 must be added to `corpus/README.md`.
- C2 adds tooling and fixtures under `.ufo/waves/round-14/` and edits `QUALITY.md`. It adds **zero files** to `corpus/knowledge/`.
- Thus, C2 has zero mathematical impact on Recipe A's knowledge file count, coverage proxy, or depth proxy.

---

## 4. Score Inflation Analysis & Defenses

### A. The Baseline State: Saturation of Finite Proxies
In `SCORECARD.md` at baseline `767adafb`:
- `coverage`: 10.0 (91/91 knowledge files mapped; Recipe A).
- `depth`: 10.0 (17/17 queue-drain rule blocks citation-resolved; Recipe A).
- `calibration`: 10.0 (historical finite proxy saturated; r13 post-review discernment improved, numeric score unchanged).

### B. Identified Vectors of Score Inflation
1. **Saturation Breach (Claiming Scores > 10.0):**
   - *Risk:* Claiming that adding C1 increases coverage from 10.0 to 11.0, or claiming C2 moves calibration to 11.0.
   - *Defense:* The 0–10 scale is a hard invariant. In `claims.json`, the claims are specified as discrete, observable units (`before: 0, after: 1`), while the global card note states: `"scores": "existing owned finite proxies all 10; no increase beyond saturation; C1 and C2 distinct independently verifiable finite observables"`.
2. **Cross-Axis Bleed (Claiming C1 Operability):**
   - *Risk:* Claiming that source-diagnosing Ghidra's Go version gate represents a held reverse-engineering capability or tool holding under `operability`.
   - *Defense:* C1 is literature/source analysis of Ghidra 12.1.4 Java code (`Base-src.zip`) and upstream commits. It ran NO live target and held NO new REA tool. It counts strictly under `coverage` (uncovered source diagnosis ground). Operability remains unchanged.
3. **Authority Inflation (Claiming C2 as Non-Author Calibration):**
   - *Risk:* Asserting that implementing and passing C2 represents an outside calibration check.
   - *Defense:* Dispatched seats (including this lane) are author-side and cannot provide non-author admission (`round-13-verifier-spotcheck.md:13-14`). C2 provides an *automated regression instrument* over local captured excerpts; it does not replace the orchestrator's fresh non-author spot-check.
4. **Denominator / Index Desynchronization:**
   - *Risk:* Adding `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` without registering it in `corpus/README.md` `## Coverage map`.
   - *Consequence:* Recipe A would report `knowledge_files: 92`, `mapped: 91`, `missing: ["2026-10-20-r14-go-version-diagnosis"]`, dropping `coverage_score` from 10.0 to 9.89 (`round(10 * 91 / 92, 2)`). This would be an unforced axis regression (self-harm).

---

## 5. Independently Reproducible Counting Recipes

To prevent score inflation and guarantee independent verification, the round's observables must be measured via exact, deterministic recipes executed against immutable Git objects.

### Recipe 1: Factual Baseline & Discrete Observable Counter (`measure.py`)
Run from repo root against any target commit `$REV`:
```bash
python3 .ufo/waves/round-14/measure.py "$REV"
```
**Expected Output on Pre-Round Baseline (`767adafb`):**
```json
{
  "C1_source_diagnosis_entries": 0,
  "C2_grounded_quality_criteria": 0,
  "C2_quote_gate_instruments": 0,
  "dangling": [],
  "knowledge_files": 91,
  "mapped": 91,
  "missing": [],
  "revision": "767adafb97e2eef6980e2ad873d357e16721c467",
  "sources_rows": 22,
  "statuses": { "mined": 21, "queued": 0, "rejected": 1 },
  "tiers": { "A": 20, "B": 1, "C": 1 }
}
```
**Expected Output on Integrated Target Commit:**
```json
{
  "C1_source_diagnosis_entries": 1,
  "C2_grounded_quality_criteria": 1,
  "C2_quote_gate_instruments": 1,
  "dangling": [],
  "knowledge_files": 92,
  "mapped": 92,
  "missing": [],
  "sources_rows": 22,
  "statuses": { "mined": 21, "queued": 0, "rejected": 1 },
  "tiers": { "A": 20, "B": 1, "C": 1 }
}
```

### Recipe 2: Structural Proxy Integrity (Recipe A Unmodified)
Run from repo root against `$REV`:
```bash
python3 - "$REV" <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev,
                                 '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
print(json.dumps({
    'revision': rev,
    'knowledge_files': len(files),
    'mapped': len(files & mapped),
    'missing': sorted(files - mapped),
    'dangling': sorted(mapped - files),
    'citation_resolved_rules': resolved,
    'rule_blocks': len(rules),
    'coverage_score': round(10 * len(files & mapped) / len(files), 2),
    'depth_score': round(10 * resolved / len(rules), 2)
}, sort_keys=True, indent=2))
PY
```
**Invariants:**
- `coverage_score` must remain exactly `10.0` (92/92 mapped; `missing` must be `[]`).
- `depth_score` must remain exactly `10.0` (17/17 citation-resolved).

### Recipe 3: C2 Quote Gate Execution & Falsifiability Recipe (L1 Verification Run)
Run by L1 once after integration (never mid-flight):
```bash
# 1. Selftest must exit 0 and report isolated finding passes
python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest
# Expected exit: 0

# 2. Red-before manifest must reject S017 splice and S018 mislocation
python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-red.json
# Expected exit: 1
# Expected findings:
# - S017: quote_not_contiguous
# - S018: quote_location_mismatch

# 3. Corrected manifest must admit contiguous located quotes
python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-corrected.json
# Expected exit: 0
```

### Recipe 4: Source Census Conformance
Run by L1 once after integration:
```bash
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku
```
**Invariants:**
- `validate` exits 0 with `kaidoku ok`.
- `census` reports: rows 22; tier A: 20, B: 1, C: 1; status mined: 21, rejected: 1; invalid tiers/statuses: 0; missing: 0.

---

## 6. Non-Obvious Move (Connector Synthesis across Proposals)

### A. Synthesis of Peer Evidence & Contradictions
1. **The HTML vs Markdown Contradiction in C2 (`ReviewS017`, `ReviewQuoteContract`, `AttackQuoteGate`):**
   - The pinned View8 README (`S017`) contains **zero** ATX `#` Markdown headings; all headings are HTML `<h2>` and `<h3>`.
   - The Check Point article (`S018`) is raw HTML whose headings are `<h1 class="wp-block-heading">`.
   - The C2 contract in `spec.json` states: "Source UTF-8 Markdown excerpt exact bytes; section is exact Markdown heading text including #".
   - *Contradiction:* Under the literal contract, the corrected S017 quote (`Replace address-derived function identifiers...`) cannot pass because `# Command-Line Arguments` does not exist in the raw file.
2. **The Layout Parsing vs Version Gate Contradiction in C1 (`CoverageGap`, `SourceChain`, `AttackNovelty`):**
   - Historical entry `2026-10-13-r4-10-real-version-pair.md:70–71` asserted that Ghidra 12.1.4 "cannot parse the Go 1.26 moduledata/pclntab layout".
   - Inspection of `Base-src.zip` (`GoRttiMapper.java` and `GoApiSnapshot.java`) proves this is **factually false**: Ghidra 12.1.4 never reaches moduledata or pclntab parsing for Go 1.26. It logs `Untested Go version`, fails to find `go1.26.0.json`, returns `GoApiSnapshot.EMPTY`, and aborts with `BootstrapInfoException("Missing Go bootstrap type info...")`.
   - Upstream commit GP-6528 (`S004`) changes no pclntab magic; it adds the snapshot JSON and updates header field mappings.
3. **The Multi-Media Source Gap (`ReviewRegistry`):**
   - S003 is Java inside a zip archive; S005 has backticks; S004 is a Git commit diff.
   - Any attempt to couple C1 directly to C2's gate would break C1, while ignoring C2's gate would leave quote verification ungrounded.

### B. The Non-Obvious Move: Strict Decoupling of Verification Surface from Substrate Grammar via Dual-Layer Observable Accounting

**Proposed Move:**
Integrate C1 and C2 as strictly separable, non-interfering observables through a **three-tier firewall**:

1. **Quarantine Machine Gate to Local Captured Fixtures:**
   - In `.ufo/waves/round-14/fixtures/`, the fixture producer produces *disclosed, digest-pinned Markdown excerpt files* for S017 and S018 (converting HTML headings to exact `#` ATX headings, or keeping the gate heading parser fence/HTML-aware).
   - In `expected.json`, pin both the excerpt's own SHA-256 and the upstream source raw SHA-256 (`191621cd...` for View8, `31b82315...` for Check Point).
   - Bounded strictly to `.ufo/waves/round-14/fixtures/`: `quote-fidelity.py` is NEVER called on `corpus/`, live archives, or outside files.
2. **Ground Normative Human Quality Separately from Machine Parsing:**
   - Append row 16 to `corpus/QUALITY.md` carrying the literal token `quote-fidelity` (satisfying `measure.py`), grounded in round-13 Mistakes 3 & 4.
   - The criterion establishes that *all* quotes must be verbatim contiguous substrings within their stated section/location, but recognizes that source locators vary by substrate (Markdown headings for doc excerpts; member/line numbers for Java archives like S003; commit diff hunks for S004).
3. **Falsify Historical Speculation and Bound Route-Arounds in C1:**
   - In `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, explicitly correct `r4-10`'s layout inference, proving the collapse is caused by the absent bootstrap snapshot in S003.
   - Restrict S005 and S006 to labeled study leads: S005 cannot claim Go 1.26 support, and S006 (BSim) is strictly bounded as name-free candidate matching, never semantic equivalence.

---

## 7. Risks and Second-Order Effects

1. **Risk of Fixture Conversion Drift:**
   - If converted fixtures in `fixtures/` diverge from upstream raw bytes, C2 could pass while the true upstream text is missing.
   - *Mitigation:* `expected.json` records the raw upstream commit/snapshot SHA-256 and the conversion command. The gate's limits are explicitly stated in `claims.json`: local captured source excerpts only.
2. **Risk of `sources-census.sh` E11 Failure:**
   - If L1 updates `used-by` in `corpus/SOURCES.md` before `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` is written to disk, check E11 will fail.
   - *Mitigation:* Strict write ordering: create the knowledge file first, verify its existence, then update `SOURCES.md`.
3. **Risk of Recipe A Regression:**
   - If the knowledge file is committed without updating `corpus/README.md:## Coverage map`, `coverage_score` falls to 9.89.
   - *Mitigation:* Update `corpus/README.md` and commit in the same atomic integration commit.

---

## 8. Verification Strategy for Integrator (L1)

L1 executes once after integrating candidate drafts (never run by leaf seats):

1. **Verify C1 Artifacts & Map:**
   ```bash
   test -f corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md
   grep -q "2026-10-20-r14-go-version-diagnosis" corpus/README.md
   ```
2. **Verify C2 Gate & Selftest:**
   ```bash
   python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest
   python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-red.json
   python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-corrected.json
   ```
3. **Verify QUALITY Criterion:**
   ```bash
   grep -q "quote-fidelity" corpus/QUALITY.md
   ```
4. **Execute Counting & Registry Census:**
   ```bash
   python3 .ufo/waves/round-14/measure.py HEAD
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku
   ```
5. **Execute Recipe A (Structural Proxy Invariant):**
   ```bash
   REV=$(git rev-parse HEAD)
   # Run Recipe A script from Section 5 -> coverage_score must be 10.0, depth_score 10.0.
   ```
