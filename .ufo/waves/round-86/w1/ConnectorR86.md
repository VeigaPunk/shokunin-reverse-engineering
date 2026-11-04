# ConnectorR86 — Sibling Overlap and Instrument Cross-Reference Findings

**Seat:** ConnectorR86 (connector, leaf, read-only)  
**Round:** 86 (kaidoku)  
**Milestone:** R86-C1 record agreement (3 atoms) and R86-C2 gate registration (5 atoms); frontier S255/S305 and the round-86 lesson  
**Detailed report:** `.ufo/waves/round-86/w1/ConnectorR86/overlap.md`  

---

## 1. Summary of Existing Instrument-Registry Rows in `SKILL.md`

| Tool | Population | Checked Invariant |
|---|---|---|
| `tools/round-46/registry.py` | `tools/round-46/census.json` (rounds 41–46 tools named in claim files at `--rev`) | Scores marker-bound registry rows against the frozen census, checking cell-0 path equality, house header, bound exit maps, file presence at `--rev`, and rejects seven forgery classes. |
| `tools/round-68/registry-conformance.py` | Dynamic own-round tools named in `plans/round-N-claims.md` (N ≥ 41) that exist at `--rev` | Audits whole registry table for structural conformance, reporting sets of unregistered tools, duplicate rows, missing blobs at `--rev`, and thin verdict cells lacking 0/1/2 exit bindings. |
| `tools/round-75/record-audit.py` | Round-74 non-author routed defects 1–7 (atoms D16–D23) | Validates eight record-calibration atoms against committed bytes with strict grammars for used-by lists, search notes, integer counts, rejected-row reasons, and census-bound errata with self-validating receipts. |
| `tools/round-76/record-audit.py` | Atoms D16–D23 plus round sections claiming capability rows entered (atom D24) | Extends round 75's eight atoms by parsing round sections at paragraph granularity to verify each claimed capability row exists in SCORECARD `## Capabilities` with ≥8 words, resolvable evidence path, and matching first-working round. |
| `tools/round-84/freeze-precheck.py` | Claim objects in `claims*.json` containers (round-83 and round-84 containers) | Validates prefreeze claim metadata requiring each claim object to declare a lane-relative counter path whose blob is pinned at the declaration revision, matching expected CLEAN/FLAGGED status. |

---

## 2. Verdict: `tools/round-86/gate-registry.py` vs Round-68 `registry-conformance.py`

**Verdict: (c) A different surface (per-row behavioural re-derivation of one gate).**

- **Compared against round-68 row text in `SKILL.md` (line 1860):**
  `| tools/round-68/registry-conformance.py | gate — R68-C1 calibration: the instrument-registry conformance census over the registry's own regime (each plan's own-round tools for rounds 41 and later that exist at --rev, against the SKILL.md rows), reporting unregistered, duplicate, absent-at-rev and thin-verdict sets, legacy rounds out of regime, and an eleven-case selftest inventory | 0=clean, mismatches 0 with scope above 0; 1=a named mismatch set; 2=could-not-evaluate (unknown revision, absent or doubled registry markers, unreadable SKILL.md or plans, bad argv) | python3 -I -B tools/round-68/registry-conformance.py --selftest — 11 cases, exit 0 on 2026-11-03 | none — the regime constant (41) and the verdict grammar are in the source; SKILL.md is its subject, never a pin | --json-out receipt only; it reads git objects, never the worktree | kaidoku |`
- **Exact differences:**
  1. *Scope:* Round 68 is a macro-census over all own-round tools across all plans from rounds N ≥ 41. Round 86 is a deep micro-audit of a single registered gate (`tools/round-85/predicate-bind.py`).
  2. *Behavioral Execution:* Round 68 performs purely static string and regex parsing over Markdown text, never executing any child process or tool. Round 86 actively executes child subprocesses: Atom G2 executes `tools/round-85/predicate-bind.py --selftest` and verifies returncode 0; Atom G3 tokenizes the declared self-test command from cell 3, executes it with `shell=False` under an isolated four-key child environment (`PATH`, `HOME`, `TMPDIR`, `LANG`), and asserts `observed_exit == declared_exit`.
  3. *Multi-Cell Invariants:* Atom G4 validates that cell 4 claims blobs exist in git at `--rev`; Atom G5 validates cell 6 owner directory format (`kaidoku-r<N>`). Round 68 does not inspect cells 4 or 6.

---

## 3. Comparison: `tools/round-86/record-agreement.py` vs Round-75/76 `record-audit.py`

- **Side-by-side atom comparison:**
  - Round-75/76 atoms D16–D24:
    - `D16_validate_embedded`: C2 landing receipt contains defect-free validate block.
    - `D17_s275_used_by_relog`: Lesson re-logs S275 old and new `used-by` values.
    - `D18_canary_sole_detector`: Probe canary mutant killed by declared case.
    - `D19_critic_classes_bound`: Patch set contains critic mutation classes.
    - `D20_grammar_reds`: Four grammars reject red fixtures, live cells conform.
    - `D21_binding_and_pins`: Base receipt runner binding, freeze pins match blobs.
    - `D22_security_arms`: Redaction, sidecar source, pin-before-exec green.
    - `D23_opened_convention`: Row-opened convention and retrospective opening round.
    - `D24_capability_rows` (round 76): Paragraph-level audit of capability claims in SCORECARD.
  - Round-86 atoms A1–A3:
    - `A1-s303-supersede-count`: `corpus/SOURCES.md` newest row opening `supersedes S303` states exact count of other rows containing `rea-agents-6.5.0.tgz` and lists their exact IDs.
    - `A2-docstring-status`: `tools/round-84/mutation-closure.py` module docstring sentence naming absent declared cases matches status assigned in code branch `not case_present:` (`survived`), with no conflicting status words.
    - `A3-receipt-pointer`: `SCORECARD.md` `| coverage |` row round R covered by `.ufo/waves/round-M/l1/scores/*.json` (M ≥ R) that is a blob at `--rev` with a valid 40-hex `rev`.
- **Overlap:** Zero (0) overlapping atoms. All three atoms (A1, A2, A3) are new, closing routed defects R85-3, R85-5, and R85-6.
- **Counter extension verdict:** Independent counter `tools/round-86/record-agreement.py` is the correct design. Extending round-75/76 would breach frozen contract immutability, break `tools/round-75/record-audit.py`'s hardcoded schema / atom count validator (`len(ids) != len(ATOMS)`), and compromise R86-C1's dedicated control pairing (`--control substring-only`).

---

## 4. Cross-Lane Pattern: "Registry Row Must Be Executable"

- **Search command:**
  `rg -l "subprocess\.run|subprocess\.Popen" /home/vgpnk/Projects/shokunin/*/tools/*registry*`
- **Findings:**
  - `tameshi-shokunin/tools/registry-check.py` (Round 17, R16-MON1): Replays every active and superseded row of `tools/registry.json` by directly executing its declared `argv` with `shell=False` under a scrubbed environment, asserting that `proc.returncode == expect["exit"]` and output matches expected needles.
  - `tameshi-shokunin/tools/registry-figure-bind.py` (Round 80, defect 5): Validates that Markdown table rows in `SKILL.md` (and `tools/registry.json`) match live reality by executing registered instruments as subprocesses and verifying that live stdout figures match declared Markdown cell values.
  - `kama-shokunin/tools/round43-registry-audit.py` (Round 43, C1): Validates that `SKILL.md` documents `GATE_SELFTEST pass=P fail=0` by executing `--selftest` in a clone repository at branch `master=TIP` and asserting exit 0 and exact stdout string match.
- **What this lane would cite:**
  `kaidoku-shokunin` would cite `tameshi-shokunin/tools/registry-check.py` for the foundational operational contract that registered tool commands must be re-derivable by subprocess execution with `shell=False` under a scrubbed environment, alongside its own prior in-lane instrument `tools/round-76/plan-command.py` (round 76, R76-C2) for four-key environment isolation (`PATH`, `HOME`, `TMPDIR`, `LANG`) and shell-injection guards.

---

## 5. Recommended Exact Cross-References for New `SKILL.md` Rows

### Row 1: `tools/round-85/predicate-bind.py` (R86-C2 Subject)
```markdown
| `tools/round-85/predicate-bind.py` | gate — R85-C1 calibration: binds a claim's counter to its `predicate` sentence — an affirmative, pinned, blob-verified path — and refuses a path named only in `kill_rule` or sharing a sentence with a negation token; the round's frozen list that also held `none` is recorded as the missed rule, and the landed counter deliberately omits it; registered in round 86 to close routed defect R85-2 (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), verified executable by `tools/round-86/gate-registry.py` | 0=every container's verdict equals its `--expect`, or is CLEAN without one; 1=a verdict mismatches or a container is FLAGGED without an expectation; 2=a container that cannot be read or parsed | `python3 -I -B tools/round-85/predicate-bind.py --selftest` — 21 cases, exit 0 on 2026-11-04 | `.ufo/waves/round-85/claims.json` (container pins) | none — read-only, `--json-out` receipt only | kaidoku-r85 |
```

### Row 2: `tools/round-86/gate-registry.py` (R86-C2 Counter)
```markdown
| `tools/round-86/gate-registry.py` | gate — R86-C2 operability: behavioural re-derivation of registered gate rows in SKILL.md (G1 row presence, G2 complete exit map and observed selftest exit 0, G3 execution of declared self-test command under 4-key child env, G4 pinned claims blobs at rev, G5 owner round match); closes routed defect R85-2 (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), extends the `tameshi-shokunin/tools/registry-check.py` cross-lane execution contract and `tools/round-76/plan-command.py` child-env harness to markdown gate registries, distinct from the static macro-census of `tools/round-68/registry-conformance.py` | 0=met, mismatches empty; 1=not met, failing atom IDs listed; 2=could-not-evaluate (unreadable SKILL.md or tool at rev, bad argv) | `python3 -I -B tools/round-86/gate-registry.py --selftest` — 8 cases, exit 0 on 2026-11-04 | `.ufo/waves/round-86/claims.json` | `--json-out` receipt and isolated mkdtemp scratch under `--work` | kaidoku-r86 |
```

### Row 3: `tools/round-86/record-agreement.py` (R86-C1 Counter)
```markdown
| `tools/round-86/record-agreement.py` | gate — R86-C1 calibration: re-derives three heterogeneous committed record cells against the bytes they describe (A1 SOURCES.md newest S303-supersession count and URL ID list, A2 mutation-closure.py docstring alignment with `not case_present` status branch, A3 SCORECARD.md coverage receipt pointer recency, blob and 40-hex rev); closes routed defects R85-3, R85-5 and R85-6 (`corpus/lessons/round-85-verifier-spotcheck.md:§8`), distinct from the frozen round-75/76 record-audit population (D16–D24); cites S255 for committed git-show reading | 0=all three atoms agreed, mismatches empty; 1=any atom mismatch; 2=could-not-evaluate (unreadable git objects, bad argv) | `python3 -I -B tools/round-86/record-agreement.py --selftest` — 11 cases, exit 0 on 2026-11-04 | `corpus/SOURCES.md`, `tools/round-84/mutation-closure.py`, `SCORECARD.md` | `--json-out` receipt only (read-only git inspection) | kaidoku-r86 |
```

---

## 6. Verification and Integrity Disclosures

- All analysis conducted strictly read-only against the BASE commit `2cf0b7ff93c698809bed321f7338276a22d6beb9`, working-tree artifacts, and sibling lane repositories.
- No production files were created, edited, or modified.
- No git / VCS mutations were executed.
- No package installs or system modifications performed.
