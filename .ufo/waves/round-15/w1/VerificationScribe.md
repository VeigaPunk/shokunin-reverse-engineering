# KaidokuR15.VerificationScribe — L1 verification argv plan (round 15)

Scope: plan only. No gate, selftest, measure, census, probe, build, or test was executed by this seat. Nothing below is a claimed pass. Predictions are labelled `[PRECEDENT r14]` (observed in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/verification.json` at revision `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`) or `[INFERENCE]` (derived from gate docstrings or source reading, not run).

Inventory commands run by this seat (non-verdict): `git rev-parse`, `git status --porcelain`, `git diff --stat`/`-U0`, `git show <rev>:<path> | sha256sum`, `sha256sum` on pinned inputs, `ls`/`find`, `command -v`, `read` of gate source and fixtures, and a `read`/`unzip -p | cat -n | sed -n` of two installed Go source members for citation-range checks.

---

## 1. Observed state at inspection time (pre-execution; L1 must re-observe)

Repository `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

| Observable | Observed | Source |
|---|---|---|
| HEAD | `9719dd232687f5ee78a4ed323b37f8810e833d10` (= `claims.json` baseline); `@{u}..HEAD` count 0 | `git rev-parse HEAD`, `git rev-list --count` |
| Tracked worktree edits (uncommitted) | `M corpus/QUALITY.md` (+1, row 17 inserted after line 26); `M corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (+11, "Round-15 advisory-pointer correction"); `M corpus/lessons/round-14.md` (+17, "Round-15 correction — virtual-dispatch advisory") | `git diff --stat` |
| Untracked | `?? .ufo/waves/round-15/` (claims.json, spec.json, dispatch.json, task-result.json, dispatch.stderr.txt, w1/swarm-registry.json) | `git status` |
| `corpus/lessons/round-15.md` | **absent** (lessons dir lists `round-14.md`, `round-14-verifier-spotcheck.md`, no round-15 file) | directory listing |
| `corpus/SOURCES.md` | sha256 `25c19036312957087d384f8174c5e78e7f38d6decff5cf227b403b2c809e6cbb`, identical to `9719dd2` blob | `git show 9719dd2:corpus/SOURCES.md \| sha256sum` |
| Shared census script | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`; `kaidoku` lane present at `/home/vgpnk/Projects/shokunin/shokunin.conf:45` | sha256sum, grep-equivalent read |
| Fleet root `/home/vgpnk/Projects/shokunin` | dirty (`M .ufo/watchdog.log`, untracked `.ufo/state/*.report-baseline`). Not kaidoku; not touched by this seat. | `git -C` status |

Pinned inputs (current sha256 vs. pins; L1 must re-hash):

| File (under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/`) | Current sha256 | Pinned by | Match |
|---|---|---|---|
| `.ufo/waves/round-14/tools/quote-fidelity.py` | `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8` | `.ufo/waves/round-14/measurement-pins.json` | yes |
| `.ufo/waves/round-14/fixtures/expected.json` | `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf` | `measurement-pins.json`; `fixtures/PROVENANCE.md` table | yes (expected.json is not self-pinned) |
| `.ufo/waves/round-14/measure.py` | `ee546111cb19e70eae63634f0795325465d58d3f3d0e098cbafc1fdb0c4dd2ab` | `measurement-pins.json` | yes |
| `.ufo/waves/round-14/fixtures/manifest-corrected.json` | `7bb4deb5d333cac935237a4d798fe9de11187f9277cecc4a510d07b5972d00b6` | `expected.json` (manifest entry), `PROVENANCE.md` | yes |
| `.ufo/waves/round-14/fixtures/s017-view8-readme-usage-deterministic.html` | `b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9` | `manifest-corrected.json` sources; `expected.json` sources | yes |
| `.ufo/gates/citation-drift/pointer-table.json` | `7994eec7e764e8c3195dd79efb850b63d437aa610e6a9d96ed24484bb53789d1` | `.ufo/gates/citation-drift/expected.json` `pointer_table.sha256` | yes |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` | none (not pinned by any file) | n/a |
| `.ufo/gates/citation-drift/expected.json` | `05c251fb06d2c1537ee39231602bb7e8d73ea16a9caf7614f3104cc276aac52c` | none (self-declared not self-pinned) | n/a |
| `.ufo/waves/round-14/w1/ReviewGoInference.md` | `8a2657f963f1bc8c76226a165349edb1a3196af323397d668776d00164cdf8bd` | none | n/a |
| S003 `Base-src.zip` (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`) | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` | round-14 closure digest pin | yes |

Tools present (inventory only; no installs performed or needed): `/usr/bin/python3` (3.14.7), `/usr/bin/git`, `/usr/bin/gawk` (5.4.1), `/usr/bin/unzip`, `sha256sum`; `/var/tmp` writable. No tool was installed or upgraded by this seat.

---

## 2. Exact registry command paths (SKILL.md, section "Local round-evidence gate registry", lines 438–452)

Verbatim command forms from the registry rows:

- **quote-fidelity** (gate):
  - Entry: `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest .ufo/waves/round-14/fixtures/manifest-corrected.json` — 0 clean, 1 failed, 2 could-not-evaluate.
  - Frozen: `--frozen .ufo/waves/round-14/fixtures/expected.json` — mismatches 1, tampered snapshots 2.
  - Selftest: same script with `--selftest`.
  - Pinned: `.ufo/waves/round-14/fixtures/expected.json`. Limits stated in row: raw UTF-8 substring and Markdown/single-line HTML heading consistency only.
- **citation-drift** (probe):
  - `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`
  - Probe semantics: 0 reported (drift reported, not failed), 2 could-not-evaluate; `--strict` restores 0 clean / 1 failed / 2 CNE.
  - Frozen preflight: table sha256 must equal `expected.json` pin, else exit 2 (`pointer_table_tampered`).
  - Selftest: same command with `--selftest` (13 cases; case table is in `expected.json`).
- **custody-pair** (tool) and **interactive-r1-recovery** (gate): registered, but not implicated by round 15 (no operator config or custody path is touched, no interactive-r1 artifact is involved). Not in the L1 set.
- Not registered in SKILL: `.ufo/gates/c1-census-v10.py` (used by round-14 `verification.json` label `census`). See §4 exclusion.
- Shared (fleet) census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` modes `validate|census|overdue|shared|selftest`, used by round-14 with `--root /home/vgpnk/Projects/shokunin kaidoku`. Not in the SKILL registry table; fleet-owned.

Round-14 precedent argv (from `verification.json`, label → argv, exit):

- `measure` → `python3 .../round-14/measure.py 3e99fbd6…` → 0
- `quote-selftest` → `python3 -I .../round-14/tools/quote-fidelity.py --selftest` → 0
- `quote-frozen` → `python3 -I .../quote-fidelity.py --frozen .../round-14/fixtures/expected.json` → 0
- `s017-red` / `s018-red` → `--manifest manifest-s017-red.json` / `manifest-s018-red.json` → 1 each
- `s017-fixed` / `s018-fixed` / `quote-corrected` → `--manifest` fixed/corrected → 0 each
- `citation-strict` → `python3 .../.ufo/gates/citation-drift/citation-drift-probe.py --root .../kaidoku-shokunin --rev 3e99fbd6… --table … --expected … --strict` → 0
- `census` → `python3 .../.ufo/gates/c1-census-v10.py --root .../kaidoku-shokunin` → 0
- `sources-validate` → `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → 0 (stdout `kaidoku\tok\t…`)
- `sources-census` → `… census --root /home/vgpnk/Projects/shokunin kaidoku` → 0 (kaidoku rows 22, A20/B1/C1, mined 21, rejected 1)

These are precedents at an older revision. None of them is evidence about the round-15 commit.

---

## 3. Proposed L1 argv plan (ordered; run once after all seats finish)

Constants: `KR=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `REV=<committed round-15 commit>`, `FLEET=/home/vgpnk/Projects/shokunin`.

### Step 0 — Preconditions (L1 action, before any measurement)

0a. Commit the round-15 deliverables (QUALITY row 17, `corpus/lessons/round-15.md`, round-14.md and knowledge corrections, `.ufo/waves/round-15/` artifacts). Reason: `measure.py` and `citation-drift` read Git objects at a revision (`git show <rev>:…`, `git ls-tree`); uncommitted bytes are not measured. Record the resulting `REV`.

0b. Working tree must match `REV` for every gate input:
```json
["git","-C","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","status","--porcelain"]
```
Expected: empty (or only files the plan does not read). Any tracked diff under `.ufo/waves/round-14/` or `.ufo/gates/` = STOP (immutability broken).

0c. Re-hash the pinned inputs and compare with §1 values:
```json
["sha256sum",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/manifest-corrected.json",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/s017-view8-readme-usage-deterministic.html",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json",
 "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json"]
```
Also pin the digest of `expected.json` outside the run (the gate does not self-hash it; PROVENANCE says so) and record the digest of `citation-drift-probe.py` (currently unpinned).

0d. Git-object checks (inventory, to be run against `REV`):
- `git -C $KR show $REV:corpus/SOURCES.md | sha256sum` → must equal `25c19036…` (no new source rows; claims say none unless L1 opens them).
- `git -C $KR show $REV:corpus/lessons/round-15.md` → must exist (QUALITY row 17, the round-14 correction, and the knowledge correction all cite it; see Finding F2).
- `git -C $KR show $REV:.ufo/waves/round-14/tools/quote-fidelity.py | sha256sum` → must equal `0d939e23…` (instrument unchanged).

### Step 1 — Immutable measurement

1a. Existing instrument (round-14, presence counts only):
```json
["python3","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py","<REV>"]
```
Precedent (r14) keys: `C1_source_diagnosis_entries 1`, `C2_quote_gate_instruments 1`, `C2_grounded_quality_criteria 1`, `knowledge_files 92`, `mapped 92`, `missing []`, `dangling []`, `sources_rows 22`, tiers A20/B1/C1, statuses mined21/queued0/rejected1. [PRECEDENT r14]. Expected at REV: the same values, because round 15 adds no knowledge file and no source row. [INFERENCE]

1b. Round-15 C2/C1 duty checks are NOT covered by `measure.py` (it does not look at QUALITY row 17 or the correction sections). If MeasureDesign ships a round-15 measure script, L1 runs that instead, at REV, and pins its sha256. If none is delivered, L1 runs these committed-object presence checks and reports them as presence-only:
- `REV:corpus/QUALITY.md` contains exactly one line starting `| 17 |` and that line contains `Supersedes #16`; the row-16 line is unchanged.
- `REV:corpus/lessons/round-14.md` contains `## Round-15 correction — virtual-dispatch advisory`.
- `REV:corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` contains `## Round-15 advisory-pointer correction`.
- `REV:corpus/lessons/round-15.md` exists and names both routed defects.

### Step 2 — Quote instrument (existing; unchanged gate code)

2a. Selftest (existing, isolated `/var/tmp` fixtures):
```json
["python3","-I","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py","--selftest"]
```
[PRECEDENT r14] exit 0, 28/28 cases, each case line `CLEAN`.

2b. Frozen controls (existing):
```json
["python3","-I","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py","--frozen","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json"]
```
[PRECEDENT r14] exit 0, `manifests=7 findings=0`, seven `match` pin lines. Note: this reads the working tree; with Step 0b clean, it is also the REV bytes.

2c. Registry manifest (existing):
```json
["python3","-I","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py","--manifest","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/manifest-corrected.json"]
```
[PRECEDENT r14] exit 0, two quotes, zero findings.

Optional controls for the C2 "documented limit" (ad hoc, not committed; see §5 for the decision). Setup is an L1 action with `cp` and a JSON file written under `/var/tmp`:

```json
["mkdir","-p","/var/tmp/qf-r15-limit/src"]
["cp","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/s017-view8-readme-usage-deterministic.html","/var/tmp/qf-r15-limit/src/s017.html"]
```

Manifest `/var/tmp/qf-r15-limit/render.json` (rendered-text quote, markup-spanning in raw bytes):
```json
{"sources":{"S017":{"path":"src/s017.html","sha256":"b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9"}},
 "quotes":[{"id":"R15-RENDER","source":"S017","section":"Deterministic Function Names and Mapping CSV",
            "quote":"Use --normalize to replace address-derived function names with deterministic identifiers."}]}
```
Run: `["python3","-I",".../quote-fidelity.py","--manifest","/var/tmp/qf-r15-limit/render.json"]`
[INFERENCE from docstring: "quote absent from the whole source" → `quote_not_contiguous@R15-RENDER`, exit 1. Source line 14 reads `Use <code>--normalize</code> to replace …`, so the rendered string is not a raw substring.]

Manifest `/var/tmp/qf-r15-limit/raw-markup.json` (same source, raw bytes including the tags):
```json
{"sources":{"S017":{"path":"src/s017.html","sha256":"b5942047de0e7626d7edf72104afacfa1a5e1c8bb182ee271fb4adabdbb7d4d9"}},
 "quotes":[{"id":"R15-RAW","source":"S017","section":"Deterministic Function Names and Mapping CSV",
            "quote":"Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers."}]}
```
Run: `["python3","-I",".../quote-fidelity.py","--manifest","/var/tmp/qf-r15-limit/raw-markup.json"]`
[INFERENCE] exit 0 (raw substring, 10 words, section body from line 13 `<h3>` to line 16 `<h3>`). This control shows the gate accepts markup-literal bytes; see F4.

Cleanup of `/var/tmp/qf-r15-limit` is an L1 action after recording outputs.

### Step 3 — Citation no-harm (existing probe)

3a. Frozen-run probe at REV (strict map):
```json
["python3","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py","--root","/home/vgpnk/Projects/shokunin/kaidoku-shokunin","--rev","<REV>","--table","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json","--expected","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json","--strict"]
```
[PRECEDENT r14 at 3e99fbd6] exit 0, `CITATION_DRIFT_*` header lines. Expected at REV: exit 0 unless a pinned target moved. Pinned QUALITY targets are only lines 21, 24–25 (pointer-table lines 119, 316, 328). Row 17 is inserted at line 27, so those targets do not move. The `SKILL.md` extracted targets (lines 246–254) and the `corpus/README.md`, `SCORECARD.md`, `LOG.md` pins are unaffected unless their files are edited above the pinned lines. [INFERENCE from grep of pointer table; not executed.]

3b. Selftest of the probe (existing, 13 cases):
```json
["python3","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py","--selftest","--expected","/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json"]
```
Expected: each of the 13 selftest cases matches `expected.json` `selftest[]`. Exit code is not stated for the selftest in SKILL; L1 records the exact output.

### Step 4 — Census (existing shared validator)

4a. `["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh","validate","--root","/home/vgpnk/Projects/shokunin","kaidoku"]` → [PRECEDENT r14] stdout `kaidoku\tok\t/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, exit 0. Note: E11 (used-by path missing on disk) would catch any `used-by` that names `corpus/lessons/round-15.md` before it exists.

4b. `["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh","census","--root","/home/vgpnk/Projects/shokunin","kaidoku"]` → expected rows 22, tiers A20/B1/C1, status mined21/rejected1 (since SOURCES.md is byte-identical to r14). [INFERENCE; r14 precedent]

4c. `["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh","overdue","--root","/home/vgpnk/Projects/shokunin","--today","2026-10-20","kaidoku"]` → exit 1 if any row is overdue. Current result UNKNOWN (not run in r14). Report the exact lines; an overdue row is a finding, not a round-15 defect.

4d. Optional: `["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh","shared","--root","/home/vgpnk/Projects/shokunin"]` for cross-lane URL sharing. Informational only.

### Step 5 — Exclusions (explicitly not in the L1 set)

- `.ufo/gates/c1-census-v10.py`: its `CLIENTS` table (lines 243–245) reads `~/.config/devin/mcp_config.json`, `~/.omp/agent/mcp.json`, and `~/.kimi-code/config.toml` to re-derive "live anchors" (lines 333, 481–482, 514). The seat contract forbids client-config access, round 15 changes no REA pin, and the instrument is not in the SKILL registry. Round 14 ran it, but it is not required for any round-15 claim. Run it only with explicit operator approval.
- `custody-pair` and `interactive-r1-recovery`: no operator path, custody receipt, or interactive-r1 artifact is in scope.
- Fleet `sources-census.sh selftest`: fleet-owned; not a kaidoku check.
- Any command that writes `~/.omp/agent/*`, `~/.kimi-code/*`, or the custody paths.

---

## 4. Calibration: what each check can and cannot support

| Check | Supports | Does not support |
|---|---|---|
| measure.py (r14) | Presence/count of instrument files, knowledge mapping, SOURCES tiers at REV | Any correctness of the C1 diagnosis, the C2 criterion wording, or the QUALITY row 17 text |
| quote selftest/frozen/manifest | Gate code path behaves as its 28 selftest cases and 7 frozen controls say, on pinned bytes at REV | Upstream authenticity, completeness, semantic support, or any held REA capability (QUALITY #16/#17) |
| rendered/raw controls (ad hoc) | The gate reports `quote_not_contiguous` for the tag-stripped rendered wording and accepts the markup-literal raw bytes | That the gate "detects" rendered quotes as a class; exit 2 is not a manual-review classifier (QUALITY #17) |
| citation-drift --strict | Pointers in the table still resolve at REV, and the table is the pinned one | Any pointer not in the table; the probe itself is unpinned |
| sources-census validate/census | Registry is well-formed, used-by paths exist, counts unchanged | Source-row content accuracy, tier correctness, or source liveness |

Immutability caveats: every gate input is tracked and unchanged at the working-tree level (checked by sha256 above), but the sha256 pins are self-declared, not hashed by the gates. `expected.json` for quote-fidelity is not self-pinned. The `citation-drift` expected.json is not pinned by anything.

---

## 5. Findings (observed unless labelled)

**F1 — Measurement reads Git objects; the round-15 edits are uncommitted.** `git diff --stat` shows 29 insertions across three tracked files, and `.ufo/waves/round-15/` is untracked. `measure.py` and the citation probe both resolve `corpus/*` through `git show <rev>:` and `ls-tree`, so they cannot see these edits at HEAD `9719dd2`. Action: commit first (Step 0a). [O]

**F2 — `corpus/lessons/round-15.md` is cited but does not exist.** It is named by QUALITY row 17 (`corpus/QUALITY.md` row 17, "why" column), by the round-14 lesson correction (`corpus/lessons/round-14.md` lines 157–158, uncommitted), and by the knowledge correction (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, uncommitted). No existing check fails on a dangling lesson citation: QUALITY is not a pointer-table target at 27, `measure.py` does not scan lessons, and `census` does not read lessons. Action: L1 must create it before the commit in Step 0a, or the cited basis is missing. [O]

**F3 — Row insertion does not move any pinned QUALITY line.** The diff inserts row 17 after line 26 (`@@ -26,0 +27 @@`). Pointer-table entries that target `corpus/QUALITY.md` are at pointer-table lines 119, 316, 328, and they pin content at QUALITY lines 21, 24–25 (`content+params-keyed`, `content-addressed`, `parsed-and-empty`). All are above 26. The "Signals of weak material" heading shifts from 29 to 30 and no pin reads it. [O for the pins; I for the no-move conclusion, which L1 should confirm with the probe at REV]

**F4 — Calibration boundary: markup-literal quotes are accepted by the gate.** Row 17 says "rendered quotations spanning markup must not be submitted as machine-gradeable". The gate accepts a quote that copies the raw tags (control in Step 2, `raw-markup.json`, [INFERENCE] exit 0), because it is a raw UTF-8 substring. The criterion's wording permits raw substrings "heading-structured raw UTF-8", so the letter of row 17 allows machine grading of a tag-containing quote, while its intent forbids it. Recommend the integrator either narrow row 17 to tag-free raw substrings, or state explicitly that markup-literal raw bytes are "substring consistency only" and not rendered-evidence. This is a wording decision for the integrator; the gate code is unchanged. [O for the gate docstring and fixture; I for the exit 0 prediction]

**F5 — Round-14 quote results are not round-15 results.** The `quote-selftest` 28/28 and `--frozen` 7/7 results in `verification.json` were recorded at `3e99fbd`. The instrument (`0d939e23…`) and `expected.json` (`ef3714bb…`) are unchanged, so the same results are expected to reproduce, but they cannot be claimed for REV without L1's own run. [O for hashes; I for reproduction]

**F6 — Source-range citations in the uncommitted round-14 correction check out on the installed S003 archive.** Read of `Base-src.zip` members (digest `f00d29c2…`, matches the S003 pin):
- `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`: `SUPPORTED_VERSIONS` check with `Msg.error("Untested Go version …")` at 170–172 (the correction's "out-of-range branch logs and continues" is consistent with the closure's 170–176 range). `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)` at 353 inside a try whose catch at 356 branches on `apiSnapshot.isInvalid()` → `BootstrapInfoException` (356–361). `@Override public <T> T getType(String, Class<T>)` at 379–380, body calling `goTypes.findDataType(name)` at 382. [O]
- `GoTypeManager.java`: `findTypeRec` body starts with `if (result == null)` at 405; `apiSnapshot.getTypeDef(typeName)` at 449 inside `else if`. The correction's range `405-455` contains both; the closure's `448-449` also matches. [O]
- Not verified by this seat: that `registerStructures` (called from the mapper's init at 353) actually reaches the `getType` override at 380 through a call chain. The definition of `registerStructures` was not located in this read. The correction says it "reaches" the override; that reachability is UNKNOWN here. [U]

**F7 — The round-14 closure's description of the correction does not match the working tree.** The closure text (`corpus/lessons/round-14-verifier-spotcheck.md` lines 166–167 and 173) describes "a 17-line append-only correction" to "the previous historical entry". In the working tree, the 17-line insertion is in `corpus/lessons/round-14.md` and an 11-line insertion is in `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`. The historical knowledge entry is not modified (not in `git status`). The closure text and the working tree therefore disagree about where the correction lives. Action: integrator to state the single correction location in the round-15 lesson, and L1 to check it against the commit. [O]

**F8 — The round-14 `census` label ran an instrument that the SKILL registry does not register.** `c1-census-v10.py` is in `verification.json` but absent from the SKILL registry (rows at lines 447–450 list four gates; `c1-census` is not one of them). Its `CLIENTS` table reads client configs (see §3, Step 5). Action: keep it out of the round-15 L1 set. Registering it would be a SKILL change this round does not assign. [O]

**F9 — QUALITY row 17 supersedes row 16 but row 16 is not edited.** The diff adds row 17 only; row 16 still says "this local instrument does not grade them" for markup-spanning quotes, and row 17 says "supersedes". Per the QUALITY governance (never rewrite; a new row names the row it supersedes), that is the intended form. The "supersedes" column of row 17 reads `16`. [O]

**F10 — No SKILL.md change is needed for C2 and none was observed.** The quote-fidelity registry row already states "Raw UTF-8 substring and Markdown/single-line HTML heading consistency only: no upstream authenticity, full-document completeness, semantic support, or whole-registry verdict" (SKILL.md line 450). This matches row 17. Pointer-table entries that anchor SKILL.md (lines 109–110, 441–449) are content-anchored, not line-anchored, and the SKILL file is not modified. [O]

---

## 6. Recommended L1 order and stop conditions

1. Step 0a–0d (commit; re-hash; Git-object checks; create `corpus/lessons/round-15.md` before the commit). STOP if a pin mismatches or `round-15.md` is absent.
2. Step 1a (measure.py at REV) and 1b (presence checks). Record both verbatim.
3. Step 2a–2c (selftest, frozen, registry manifest). STOP-and-report on any exit other than 0/0/0.
4. Step 2 optional controls (render/raw), recorded as observed; if the integrator wants them pinned, that is a new `expected.json` entry and a re-pin of `expected.json` (changes the 0c pin). Decision required; do not pin silently.
5. Step 3a (citation probe `--strict` at REV) and 3b (probe selftest). STOP on exit 1/2.
6. Step 4a–4c (census validate, census, overdue). STOP on exit 1 from validate.
7. Record REV, every argv, exit code, and the stdout head for each run, plus the pre/post sha256 of §0c. Do not claim a pass from precedent values.

Installs/updates by this seat: none.
Files written by this seat: this report only.
