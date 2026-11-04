# Sibling Overlap & Instrument Cross-Reference Scan (Round 86)

**Seat:** ConnectorR86 (connector, leaf, read-only)  
**Lane:** `kaidoku-shokunin`  
**Round:** 86 (kaidoku)  
**Axes:** coverage, depth, calibration  
**Milestone:** R86-C1 record agreement (3 atoms) and R86-C2 gate registration (5 atoms); frontier S255/S305 and the round-86 lesson  

---

## 1. Inventory of Existing Lane Instruments in `SKILL.md`

Analysis of the five specified instrument-registry rows in `SKILL.md`:

| Tool | Population | What it checks (One-line summary) |
|---|---|---|
| `tools/round-46/registry.py` | `tools/round-46/census.json` (all tools from rounds 41–46 named in claim files that exist at `--rev`) | Scores marker-bound registry rows against the frozen census, enforcing cell-0 path equality, house header, bound verdict maps, file presence at `--rev`, and rejects seven forgery classes. |
| `tools/round-68/registry-conformance.py` | Dynamic plan census: own-round tools named in `plans/round-N-claims.md` for rounds N ≥ 41 that exist at `--rev` | Audits the whole registry table for structural conformance, reporting sets of unregistered tools, duplicate rows, missing blobs at `--rev`, and thin verdict cells lacking 0/1/2 exit bindings. |
| `tools/round-75/record-audit.py` | Round-74 non-author routed defects 1–7 across records (atoms D16–D23) | Validates eight record-calibration atoms against committed bytes with strict grammars for used-by lists, search notes, integer counts, rejected-row reasons, and census-bound errata with self-validating receipts. |
| `tools/round-76/record-audit.py` | Atoms D16–D23 plus all round sections claiming capability rows entered (atom D24) | Extends round 75's eight atoms by parsing round sections at paragraph granularity to verify each claimed capability row exists in SCORECARD `## Capabilities` with ≥8 words, resolvable evidence path, and matching first-working round. |
| `tools/round-84/freeze-precheck.py` | Claim objects in `claims*.json` containers (specifically round-83 and round-84 containers) | Validates prefreeze claim metadata requiring each claim object to declare a lane-relative counter path whose blob is pinned at the declaration revision, matching expected CLEAN/FLAGGED status. |

---

## 2. Verdict on `tools/round-86/gate-registry.py` vs Round-68 `registry-conformance.py`

### Verdict
**(c) A different surface (per-row behavioural re-derivation of one gate)**.

### Baseline Row Text Compared Against
From `SKILL.md` (line 1860):
```markdown
| `tools/round-68/registry-conformance.py` | gate — R68-C1 calibration: the instrument-registry conformance census over the registry's own regime (each plan's own-round tools for rounds 41 and later that exist at --rev, against the SKILL.md rows), reporting unregistered, duplicate, absent-at-rev and thin-verdict sets, legacy rounds out of regime, and an eleven-case selftest inventory | 0=clean, mismatches 0 with scope above 0; 1=a named mismatch set; 2=could-not-evaluate (unknown revision, absent or doubled registry markers, unreadable SKILL.md or plans, bad argv) | python3 -I -B tools/round-68/registry-conformance.py --selftest — 11 cases, exit 0 on 2026-11-03 | none — the regime constant (41) and the verdict grammar are in the source; SKILL.md is its subject, never a pin | --json-out receipt only; it reads git objects, never the worktree | kaidoku |
```

### Exact Differences & Evidence
1. **Scope and Cardinality:**
   - `tools/round-68/registry-conformance.py` is a macro-census over the entire registry regime (all plans for rounds N ≥ 41).
   - `tools/round-86/gate-registry.py` is a focused, deep micro-audit evaluating a single registered gate (`tools/round-85/predicate-bind.py`) across five specific atoms (G1–G5).
2. **Behavioral Child Execution vs Static Textual Parsing:**
   - Round 68 performs purely static lexical/regex parsing over Markdown text. As its docstring specifies, "it never runs git and never writes outside an optional --json-out". It never executes any instrument or self-test command.
   - Round 86 dynamically executes code in child processes:
     - **G2 (`exit-map-observed`):** Runs `run_selftest()` to invoke `python3 tools/round-85/predicate-bind.py --selftest` and verifies that the observed returncode equals the declared success exit 0.
     - **G3 (`self-invocation`):** Extracts the exact declared command string from cell 3 (`self-test command`), parses `want` exit code, tokenizes argv with `shlex.split`, executes it with `subprocess.run(..., shell=False)` under an isolated four-key child environment (`PATH`, `HOME`, `TMPDIR`, `LANG`), and asserts `observed_exit == declared_exit`.
3. **Multi-Cell Blob Resolution and Ownership Binding:**
   - **G4 (`pinned-blob`):** Parses `.ufo/waves/round-<N>/claims.json` tokens from cell 4 (`pinned-value path`) and asserts they resolve to valid git blobs at `--rev`. Round 68 does not inspect cell 4.
   - **G5 (`owner-round`):** Validates cell 6 (`owner`) format against directory round `tools/round-<N>/`. Round 68 does not validate owner cells.

Therefore, `tools/round-86/gate-registry.py` does not duplicate round 68 (it executes tools and audits cells 3, 4, and 6) nor is it a subset (round 68 lacks any capability to execute self-test commands or verify pin blobs). It constitutes an entirely distinct behavioural verification surface.

---

## 3. `tools/round-86/record-agreement.py` vs Round-75/76 `record-audit.py`

### Side-by-Side Atom Comparison

| Instrument | Atom ID | Target / Surface | Verification Logic |
|---|---|---|---|
| **Round 75/76** | `D16_validate_embedded` | `.ufo/waves/round-75/` C2 landing receipt | Checks embedded `validate` block is defect-free and referenced by committed receipt. |
| **Round 75/76** | `D17_s275_used_by_relog` | `corpus/lessons/round-75.md` | Asserts lesson re-logs S275 old and new `used-by` values and names round-74 wave file. |
| **Round 75/76** | `D18_canary_sole_detector` | Round-75 probe mutation receipt | Verifies landing battery's canary mutant was killed by declared case with zero survivors. |
| **Round 75/76** | `D19_critic_classes_bound` | Round-75 probe mutants | Checks home-under identity, sample last-wins, superset key in landing patch set. |
| **Round 75/76** | `D20_grammar_reds` | `corpus/SOURCES.md` (S277/S285) & notes | Enforces strengthened grammars reject red fixtures, live cells conform. |
| **Round 75/76** | `D21_binding_and_pins` | Round-75 receipts & claims | Asserts runner binding in base receipt, freeze pins match blobs, ledger restates debt. |
| **Round 75/76** | `D22_security_arms` | Round-75 selftest receipts | Checks redaction, sidecar source, pin-before-exec, and freeze-pin containment green. |
| **Round 75/76** | `D23_opened_convention` | `corpus/SOURCES.md` search notes | Verifies search log states row-opened convention and Gate row names opening round. |
| **Round 76 only**| `D24_capability_rows` | `SCORECARD.md` `## Capabilities` | Paragraph-level parse of sections claiming capabilities, checking description length (≥8 words), evidence path, and first-working-round. |
| **Round 86** | `A1-s303-supersede-count` | `corpus/SOURCES.md` newest row | Re-derives that newest row opening `supersedes S303` states exact count of other rows containing `rea-agents-6.5.0.tgz` and lists their exact IDs. |
| **Round 86** | `A2-docstring-status` | `tools/round-84/mutation-closure.py` | Re-derives that the single docstring sentence naming absent declared cases matches the status label in code branch `not case_present:` (`survived`), with no conflicting status words. |
| **Round 86** | `A3-receipt-pointer` | `SCORECARD.md` `\| coverage \|` row | Re-derives that coverage row round R is covered by a `.ufo/waves/round-M/l1/scores/*.json` receipt with M ≥ R, resolvable as a blob at `--rev` with a valid 40-hex `rev`. |

### Overlap and Extension Analysis
- **Overlapping atoms:** **Zero (0)**. There is no overlap between D16–D24 and A1–A3. D20 inspected S277/S285 grammars, not S303 URL counts. D24 inspected SCORECARD capability rows, not the coverage row receipt pointer. Mutation-closure docstring alignment (A2) was never examined by prior instruments.
- **New atoms:** All three atoms (`A1-s303-supersede-count`, `A2-docstring-status`, `A3-receipt-pointer`) are entirely new, directly closing routed defects R85-3, R85-5, and R85-6 from `corpus/lessons/round-85-verifier-spotcheck.md` §8.
- **Should the new counter instead have extended the existing audit?**
  **No.** Creating the independent counter `tools/round-86/record-agreement.py` is the architecturally sound and compliant approach:
  1. *Historical Immutability:* `tools/round-75/record-audit.py` and `tools/round-76/record-audit.py` are frozen historical counters that serve as immutable witnesses for rounds 75 and 76. Modifying them post-closure violates audit freeze rules.
  2. *Strict Schema Binding:* Both round 75 and round 76 counters hardcode schema checks (`kaidoku-r75-record-audit-v1`) and strict atom counts (`len(ids) != len(ATOMS)` defect). Appending atoms to those files breaks their own internal self-tests and validation fixtures.
  3. *Heterogeneous Surface vs Uniform Round Closure:* Atoms A1–A3 re-derive internal agreement across three disparate repository surfaces (`SOURCES.md`, `mutation-closure.py`, `SCORECARD.md`) rather than auditing a single round's closeout receipts.
  4. *Target Failability & Control Discipline:* R86-C1 requires a specific cheap-rule control (`--control substring-only`) that accepts the defective BASE state to prove target failability. Bundling this into round 75/76 would corrupt the frozen control profiles.

---

## 4. Cross-Lane Pattern: "Registry Row Must Be Executable"

### Search Commands Executed
- Read-only search for registry-related tools across all sibling repositories in the fleet:
  ```sh
  find /home/vgpnk/Projects/shokunin -maxdepth 4 -path "*/tools/*" -name "*registry*"
  rg -l "subprocess\.run|subprocess\.Popen" /home/vgpnk/Projects/shokunin/*/tools/*registry*
  rg -l "re-derive.*running|re-derivable by running" /home/vgpnk/Projects/shokunin/*
  ```

### Sibling Lane Finding
1. **`tameshi-shokunin/tools/registry-check.py` (Round 17, R16-MON1):**
   - *Description:* Replays every active and superseded row of `tools/registry.json` by executing its declared `argv` directly via `subprocess.Popen(row["argv"], cwd=cwd, shell=False)` in a scrubbed environment (`GIT_*` removed, `PYTHONDONTWRITEBYTECODE=1`), asserting that `proc.returncode == expect["exit"]` and required stdout needles match.
2. **`tameshi-shokunin/tools/registry-figure-bind.py` (Round 80, defect 5):**
   - *Description:* Validates that `SKILL.md` markdown table rows and `tools/registry.json` match reality by running the instruments as subprocesses and verifying that the live figure printed to stdout matches the declared text in the markdown cell.
3. **`kama-shokunin/tools/round43-registry-audit.py` (Round 43, C1):**
   - *Description:* Asserts that `SKILL.md` documents `GATE_SELFTEST pass=P fail=0` by running the tool's `--selftest` in a clone repository at branch `master=TIP` and asserting exit code 0 and exact stdout agreement.
4. **Other sibling lanes (`mori-shokunin/tools/mori-gate-registry.py`, `tsukuroi-shokunin/tools/check-registry-coverage.py`):**
   - Carry static checks for self-test flags in AST/argparse keys or path existence via `git cat-file -e`, but do not execute the tool commands.

### What `kaidoku-shokunin` Would Cite
- **Cross-Lane Conceptual Ancestor:** `tameshi-shokunin/tools/registry-check.py` (round 17) for the principle that a registry row's entry command is an executable contract that must be verified by child execution with `shell=False` under a sanitized environment.
- **In-Lane Procedural Ancestor:** `kaidoku-shokunin`'s own `tools/round-76/plan-command.py` (round 76, R76-C2), which established parsing CLI command tokens from Markdown, stripping dangerous shell constructs, and executing via `subprocess.run` under the fixed four-key environment (`PATH`, `HOME`, `TMPDIR`, `LANG`).
- In round 86, `tools/round-86/gate-registry.py` synthesizes these two patterns into a gate that directly parses `SKILL.md` Markdown table cells and verifies them via execution.

---

## 5. Recommended Exact Cross-References for New `SKILL.md` Rows

To ensure clean traceability across both newly registered instruments and the round's counters, the following exact row entries and cross-reference lines are recommended:

### A. Recommended Row for `tools/round-85/predicate-bind.py` (R86-C2 Subject)
```markdown
| `tools/round-85/predicate-bind.py` | gate — R85-C1 calibration: binds a claim's counter to its `predicate` sentence — an affirmative, pinned, blob-verified path — and refuses a path named only in `kill_rule` or sharing a sentence with a negation token; the round's frozen list that also held `none` is recorded as the missed rule, and the landed counter deliberately omits it; registered in round 86 to close routed defect R85-2 (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), verified executable by `tools/round-86/gate-registry.py` | 0=every container's verdict equals its `--expect`, or is CLEAN without one; 1=a verdict mismatches or a container is FLAGGED without an expectation; 2=a container that cannot be read or parsed | `python3 -I -B tools/round-85/predicate-bind.py --selftest` — 21 cases, exit 0 on 2026-11-04 | `.ufo/waves/round-85/claims.json` (container pins) | none — read-only, `--json-out` receipt only | kaidoku-r85 |
```
*Key Cross-References:* Cites routed defect `R85-2` (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), links to its R86-C2 verifier `tools/round-86/gate-registry.py`, and pins container `.ufo/waves/round-85/claims.json`.

### B. Recommended Row for `tools/round-86/gate-registry.py` (R86-C2 Counter)
```markdown
| `tools/round-86/gate-registry.py` | gate — R86-C2 operability: behavioural re-derivation of registered gate rows in SKILL.md (G1 row presence, G2 complete exit map and observed selftest exit 0, G3 execution of declared self-test command under 4-key child env, G4 pinned claims blobs at rev, G5 owner round match); closes routed defect R85-2 (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), extends the `tameshi-shokunin/tools/registry-check.py` cross-lane execution contract and `tools/round-76/plan-command.py` child-env harness to markdown gate registries, distinct from the static macro-census of `tools/round-68/registry-conformance.py` | 0=met, mismatches empty; 1=not met, failing atom IDs listed; 2=could-not-evaluate (unreadable SKILL.md or tool at rev, bad argv) | `python3 -I -B tools/round-86/gate-registry.py --selftest` — 8 cases, exit 0 on 2026-11-04 | `.ufo/waves/round-86/claims.json` | `--json-out` receipt and isolated mkdtemp scratch under `--work` | kaidoku-r86 |
```
*Key Cross-References:* Cites routed defect `R85-2`, explicitly distinguishes itself from `tools/round-68/registry-conformance.py`, cites `tools/round-76/plan-command.py` child-environment harness, and notes the cross-lane precedent `tameshi-shokunin/tools/registry-check.py`.

### C. Recommended Row for `tools/round-86/record-agreement.py` (R86-C1 Counter)
```markdown
| `tools/round-86/record-agreement.py` | gate — R86-C1 calibration: re-derives three heterogeneous committed record cells against the bytes they describe (A1 SOURCES.md newest S303-supersession count and URL ID list, A2 mutation-closure.py docstring alignment with `not case_present` status branch, A3 SCORECARD.md coverage receipt pointer recency, blob and 40-hex rev); closes routed defects R85-3, R85-5 and R85-6 (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), distinct from the frozen round-75/76 record-audit population (D16–D24); cites S255 for committed git-show reading | 0=all three atoms agreed, mismatches empty; 1=any atom mismatch; 2=could-not-evaluate (unreadable git objects, bad argv) | `python3 -I -B tools/round-86/record-agreement.py --selftest` — 11 cases, exit 0 on 2026-11-04 | `corpus/SOURCES.md`, `tools/round-84/mutation-closure.py`, `SCORECARD.md` | `--json-out` receipt only (read-only git inspection) | kaidoku-r86 |
```
*Key Cross-References:* Cites routed defects `R85-3`, `R85-5`, and `R85-6`, cites `corpus/SOURCES.md:S255` (git-show committed-bytes convention), and records non-overlap with `tools/round-75/record-audit.py` / `tools/round-76/record-audit.py`.
