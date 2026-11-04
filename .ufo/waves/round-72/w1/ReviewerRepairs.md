# ReviewerRepairs — round-72 w1

Reviewer: ReviewerRepairs-4 (same-lane dispatched reviewer; not an outside promotion verifier). Read-only review of carried repairs and record shape. No production files edited; no admission or axis judgment issued.

Axes: evidence accuracy, complete repair accounting, append-only custody, promotion-verifier independence. Parallel reads and cheap data reductions were used; no runtime or scoring claims are inferred from record inspection.

## Findings by severity

### Medium — R72-G3: supersession needs replacement bytes and a re-taken before record

Evidence: `.ufo/waves/round-71/claims.json:44-76` has five `instrument_supersessions` entries containing only `commit`, `path`, `reason`; its `instruments` map preserves the freeze digests. Each entry omits the replacement `sha256`. Keeping the original freeze map is not itself a defect when a complete supersession records the measured replacement. A clean freeze-gate result is not proof that this stronger record contract is satisfied.

I independently hashed `git show 5cecf4c0f879f3e60884c5625226a0d68ced8458:<path>` bytes (read-only; no tool execution). Missing replacement hashes:

| Path | Replacement sha256 |
|---|---|
| tools/round-71/packed-elf.py | d8bd30b8b95cb57524e1045e9786d4b14837fb27b0a9f6842b0bff81545d7d7a |
| tools/round-71/seam-probe.py | 22b840e1427b24618ac33075169d29780887d2cffb5b7b989af8cc4bb6ee0ce2 |
| tools/round-71/forged-receipts.py | bd70af49ed4629ab965b83a814ec0a39ce5db4a86c2a76e42121bb9eabb2084a |
| tools/round-71/registry-census.py | b85b4d7922ab571af04f633e415a4fe91859e440c9a609d4182a46aec61bb380 |
| tools/round-71/controls.py | fc60093056692f4d8bc11d04508c3e32ea102439670e39a6827fdf6fd7b1858a |

Round-72 shape: preserve the top-level `instruments` object mapping each repository-relative path to its frozen 64-hex SHA-256, with the predicate sentences in `claims`. Any post-freeze replacement requires an appended `instrument_supersessions` object with `path` (same instrument path), `commit` (full replacement commit), `sha256` (actual replacement blob digest), and `reason` (specific defect/behavior change). Re-take the before record required by A1 against those replacement bytes, append it at a fresh receipt path, and cite that path and measured revision in the disclosure/report. A reason or commit alone is insufficient; silently updating the freeze map would lose custody. A genuinely new, explicitly identified container with new pins is the alternative named by the prior verifier, not an undisclosed rewrite.

Current round-72 container: `.ufo/waves/round-72/claims.json:35` explicitly requires the replacement sha and re-taken before record; lines 47-54 supply the six frozen pins. No supersession list is present in the inspected container, so this is a prospective requirement, not a claim that a round-72 supersession is already defective. Prior verifier evidence: `corpus/lessons/round-71-verifier-spotcheck.md:118`.

### Low — R72-G4: S274 still puts verdict prose in scope

Evidence: `corpus/SOURCES.md:191` has 11 logical cells. Cell 5 (`scope`, shell field `$6`) begins `REJECTED: the page grounds race-free creation...`; cell 7 (`teaches`, `$8`) already contains a rejection explanation and `flip:` but begins `REJECTED on name properties`, not the normative `REJECTED:` form. The reason is duplicated across scope and teaches; it is not missing altogether.

`/home/vgpnk/Projects/shokunin/CORPUS.md:86-118` requires scope to describe the claim/topic and teaches to carry `REJECTED: <reason>; flip: <what would change the verdict>`. The canonical census maps scope/teaches to `$6`/`$8` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:626-628`), requires NF=13 (11 cells), and only warns W02 when rejected teaches has length <8 (`:671-672`). Therefore a census pass would not establish this semantic column/prefix contract.

Do not rewrite S274. Append a correction with the next unused id, ordinary topic scope (e.g. mkdtemp creation safety versus directory-name distinctness), the same located source evidence, status `rejected` if that verdict is retained, and teaches beginning `supersedes S274 — REJECTED: <precise reason>; flip: <condition>`. The supersedes prefix implements append-only rule 2 while retaining the rejection reason/flip in the teaches cell. The new row also needs its own opened-in-round evidence and Gate URL/date/located quote. No source verdict was re-adjudicated here and no row was edited.

### Low — R72-G2: the historical pre receipt cannot support 12/18

Both the worktree read and `git show 56241b1c8baff95862730c008f1ae5132b03388e:.ufo/waves/round-71/l1/pre/c2-do-nothing.json` give exactly:

- `base_world_shapes: 10`, `landing_world_shapes: 2`, `forged_total: 10`, `lying_shapes: 0`, `target: 16`, `met: false`.
- `source: .ufo/waves/round-70/l1/scores/c1-at-landing.json`.

Do not silently normalize its inconsistent 10+2 versus forged_total 10. The next report must cite `.ufo/waves/round-71/l1/scores/controls-at-landing.json`, arm `c2-do-nothing` (`arms[2].observed`, lines 38-45): base 10 + landing 2, forged_total 12, lying_shapes 0, target 18, arm ok true. Preserve the historical pre receipt. Round-72 A10 names the intended citation repair; the final report still needs the actual pointer.

### Low — R72-G1: census correction must distinguish rounds and attack conventions

Own count of `.ufo/waves/round-72/r72-w1-spec.json` items (not a copied summary):

| Role | Count | Names |
|---|---:|---|
| executor | 5 | ExecC1, ExecC1Base, ExecC2, ExecC3, ExecSweep |
| reviewer | 2 | ReviewerGates, ReviewerRepairs |
| mutation-tester | 2 | MutProbe, MutReaders |
| critic | 1 | CriticClaims |
| sentinel | 1 | SentinelScope |
| scout | 1 | ScoutSource |
| connector | 1 | ConnectorCross |
| scribe | 3 | ScribeKnowledge, ScribeLesson, ScribeRecord |

Total 16. Round-72 report must state this exact census, attack roles reviewer/critic/mutation-tester = 5/16 = **31.25%** (31% rounded), with sentinel separate, and L1 holding the planner seat outside those 16 spec items. Spec roles do not prove delivered or settled seats; obtain those from the results/settlement records.

Historical correction must also explicitly state that round 71 had **6 executors and 2 scribes**, not carry round-72's 5/3 backward. The prior non-author verifier names all six historical executor seats at `corpus/lessons/round-71-verifier-spotcheck.md:116`; the prior report is not to be rewritten. Its 6/16 attack tally included sentinel; round-72's frozen convention excludes sentinel. State the convention instead of presenting the percentages as the same denominator membership.

### Low — additional declaration provenance wording defect

`.ufo/waves/round-72/claims.json:11` says "two pre-freeze declaration fixes", lists four and contains literal `{FIX2}`. A0 and errata at lines 20-24/34 supply the correct four commits, including `306cbb3fb11661fba6f364f73ad0b1eeb24a959f`. The record should append a field-specific erratum for `declaration_pointer` naming all four commits and the placeholder replacement; do not present the unresolved prose as an exact provenance citation or rewrite the frozen predicate sentences.

## SHONEN

`SHONEN.md:11-14` has all four boxes unchecked. `/home/vgpnk/Projects/shokunin/PROTOCOL.md:63-73` requires a named reviewer outside the authoring lane; its dispatched subagents are still the lane. **This seat can close none.** An actual fresh-lane/integrator non-author may close any of the four only after the corresponding evidence review; these are evidence candidates, not an issued promotion recommendation:

- [~] Box 1 — decision tables, error patterns, checklists, cited sources. Inspect `SKILL.md:42-80` (decision/error tables), `SKILL.md:792-800` (checklists), `SKILL.md:109-118` (sourced error-handling rationale), and the referenced corpus entries; verify each of the three required structures has a resolvable supporting citation. Merely counting headings is insufficient.
- [~] Box 2 — logged executed end-to-end task. Inspect `LOG.md:4244-4277` and `.ufo/waves/round-71/l1/scores/c1-at-landing.json`, `c1-check-at-landing.json`, retained `c1-env-at-landing.jsonl` and `c1-env-audit.json`; alternatively use a genuinely completed round-72 route/checker pair and its eventual LOG entry. Distinguish filed historical execution from a fresh run.
- [~] Box 3 — executable instructions without oral context. Inspect `SKILL.md` working contract/route table and pinned CLI registry, `plans/round-72-claims.md`, and the six declared instruments' exact argv/prerequisites/exit contracts. A named outside verifier must record a self-contained walkthrough and resolved pointers; this scoped metadata review is not that walkthrough.
- [~] Box 4 — no cross-domain bleed, accurate province. Inspect `PROVINCE.md:3-36,524-535`, round-72's eventual additions, and the connector's sibling-scan evidence plus the final scoped diff. Confirm pinned-carrier/checker Core boundaries do not become claims about every artifact or sibling-owned method. Pending final changes cannot be pre-certified.

Each actual close must be `[x] <outside-verifier-id>` plus its evidence pointer in the assessment; retain `[~]` for lane assertions or `[ ]` where evidence remains absent. The conditional four-box map above does not change SHONEN.md.

## Residual risk and verification gaps

- LSP unavailable: `read xd://lsp` returned "No such tool"; no semantic server/status/references/definition/diagnostics interface is mounted. Text searches are literal evidence only. This assignment reviews JSON/Markdown record contracts, not a semantic caller proof.
- Reviewed actual base→operative-freeze diff for claims container, SOURCES and SHONEN, plus named records and committed blob hashes. No tests, validators, carrier runs, installations, agent/runtime reroutes, admission gates or saturation measurements were executed. No claim is made about final landing/settlement or `resume_continuity_v1` (not changed or within this assignment).
- Remaining before-record/supersession proof belongs to the eventual measured landing; a policy sentence is not fulfillment. Standing r63/r58/r60/r64 debt is not waived by these scoped repairs.
- Tool installs/updates: none. Own scratch removed before terminal return.

Self-evaluation: accuracy 4/5 (static records, no final landing), completeness 4/5 (all five assigned areas; outside promotion verification intentionally absent), clarity 4/5 (precise paths but dense custody details), actionability 5/5 (exact counts, receipt selector and required shapes), conciseness 4/5 (full digest table retained for auditability), overall 4.2/5. No unsupported runtime success or promotion closure asserted.

Report: .ufo/waves/round-72/w1/ReviewerRepairs/Report.md
