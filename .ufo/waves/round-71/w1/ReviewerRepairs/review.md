# ReviewerRepairs — round 71 / w1

Axes reviewed: append-only preservation, scope confinement, predicate identity, repair completeness, registry-cell integrity. This is a review recommendation, not admission.

## Findings (severity order)

### Medium — R70 routed defect 6 is not closed by R71-G4's stated disposition

`corpus/lessons/round-70-verifier-spotcheck.md` §Routed defects item 6 concerns the **round-70** claim “all 16 settled, none dead”: its result objects have no status/dead fields. `plans/round-71-claims.md` §Repairs carried instead promises “the round-71 wave-settlement receipt”; the introduction likewise says “for this wave.” A settlement receipt for round 71 cannot substantiate or qualify round 70's claim. The plan acknowledges the issue, but leaves the historical disposition unanswered. L1 should append a round-70 settlement disclosure citing the actual WAVE-DONE plus 16 result entries, explicitly distinguishing outputs from per-seat liveness/status evidence, or provide the requested round-70 receipt. Do not rewrite the filed report or invent status fields.

### Low — container misattributes declaration commit

Frozen `.ufo/waves/round-71/claims.json` `declaration_pointer` and `frozen_atoms.A0` call `46366cc5525f661b97d26a8c70ed3a53d0b4b916` the declaration containing tools/plan/census-start. Commit history and `git diff-tree --no-commit-id --name-only -r <commit>` show those files were added at **329208cf4a234aac391b7f02b50769c5920f1beb**. `46366cc…` is the subsequent pre-receipt/generator commit. Actual ordering and pins are correct; the descriptive provenance attribution is not. Append an erratum naming both fields and the correct identities; do not silently edit the frozen container or predicates.

## Seven routed inputs and intended disposition

Read the entire committed round-70 spot-check (including its rejection screen and closure note), not just the numbered list.

| R70 item | Intended R71 disposition | Review |
|---|---|---|
| 1. Three capability-table rows missing | R71-G1: append round-70 rows to SCORECARD Capabilities at record | Addressed in plan, not yet landed at freeze |
| 2. W04 “same 20” disagrees with receipt's 21 | R71-G2: append erratum to round-70 lesson and LOG; carry it in next report | Addressed; preserve original filed wording |
| 3. “Sixteen forgery shapes” unsupported by cited 10+2 receipt | R71-C2: six lying-field rows cut from landing material, relabelled FIRST-CUT, first_cut_rc 0 / superseded_rc 1; 18 rows total | Addressed as claim; execution owned by other seats |
| 4. Missing round-70 Search-log note and tempfile rejected row | R71-G5/frontier: append search note and S274 REJECTED row, reason and flip condition | Addressed in plan |
| 5. ca9817cf typo | R71-G3: appended erratum; actual supersession ca9817cdf9c73801569bff8a20aac6856647cbb2 / ca9817cd | Addressed; never rewrite historical report |
| 6. R70 settlement evidence shape | R71-G4 promises R71 settlement only | Historical issue unanswered; medium finding above |
| 7. Dead scratch provenance pointers | Introduction: identify as run pointers, not evidence; cite committed summaries | Addressed as observation, explicitly **not a defect** in spot-check |

Strictly, “Repairs carried” names G1–G5 only: item 3 is C2 and item 7 is covered by the introduction. Neither is omitted from the plan as a whole. The spot-check's phrase “count overstated” conflicts with its explicit 20→21 numbers; use the numeric erratum, not an inferred direction.

## Frozen diff and append-only discipline

Executed:

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 82c8e620c9222fb218aa0260570a3765da2afb44 b827a8b5d54f2885ec9be7786389f356c59226ce
```

Result: **14 files changed, 3894 insertions(+)**. Every changed path:

- `.ufo/waves/round-71/claims.json`
- `.ufo/waves/round-71/gen-claims.py`
- `.ufo/waves/round-71/l1/census-start.txt`
- `.ufo/waves/round-71/l1/pre/c1-at-base.json`
- `.ufo/waves/round-71/l1/pre/c2-do-nothing.json`
- `.ufo/waves/round-71/l1/pre/c3-at-base.json`
- `.ufo/waves/round-71/l1/pre/controls-at-declaration.json`
- `.ufo/waves/round-71/l1/pre/nonce-commitment.txt`
- `plans/round-71-claims.md`
- `tools/round-71/controls.py`
- `tools/round-71/forged-receipts.py`
- `tools/round-71/packed-elf.py`
- `tools/round-71/registry-census.py`
- `tools/round-71/seam-probe.py`

The complete path list comes from `git diff --name-only 82c8e620c9222fb218aa0260570a3765da2afb44 b827a8b5d54f2885ec9be7786389f356c59226ce`. No `LOG.md`, `SCORECARD.md`, `corpus/` path, `PROVINCE.md`, or `SKILL.md` changed. All freeze changes are additions scoped to the declaration, tools, container/generator and pre-receipts. Whole SKILL.md blobs are byte-identical (stronger than the requested row check).

Four round-69 eight-cell rows are byte-identical at base and freeze: packed-elf.py, mutation-check.py, contract-probe.py and controls.py. A fifth round-69 row, provenance-check.py, also exists but is not one of the four multicell rows; it was not miscounted as a fifth malformed row. No historical row repair was landed by this reviewer.

## Predicate identity and pin evidence

Reproducible comparison command (saved read-only analysis script; no target instrument execution):

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-71/w1/ReviewerRepairs/compare-frozen.py
```

The script loads **both files from the freeze commit** with `git show`, extracts the three `**Predicate (one sentence, frozen).**` paragraphs using a blank-line boundary, normalizes with `' '.join(text.split())`, asserts three predicates/claims, and compares them in order. Actual output:

```text
normalized_predicate_equal [True, True, True]
SKILL_whole_blob_equal True
```

All **5/5 `instruments` pins** and **6/6 `loaded_by_counter` pins** equal sha256 of their blobs at freeze; each comparison printed True. Exact expected/actual hashes, normalized-predicate hashes, complete original/replacement rows, history and diff stat are preserved in `evidence.json` beside this report. These are byte/structure checks, not semantic proof from text search.

## Pre-receipt ordering

Executed `git log --format='%H %P %s' b827a8b5d54f2885ec9be7786389f356c59226ce -- .ufo/waves/round-71/` and inspected declaration/pre commit changed-file lists with `git diff-tree`.

```text
82c8e620… base
  -> 329208cf… declaration: five tools + plan + census-start
  -> 46366cc… pre receipts + nonce commitment + generator
  -> b827a8b5… first claims.json container
```

All five declared pre artifacts are present in `46366cc…`, the direct parent of freeze; therefore the pre receipts **do precede** the first container commit. This proves commit order, not wall-clock execution or nonce secrecy. The wrong descriptive declaration hash does not invalidate the observed order.

## Exact SKILL.md replacements for L1 (draft only)

Each of the six old lines has exactly **six unescaped cells**, a real unescaped terminal delimiter and no internal bare pipe. Preserve that delimiter and append ` kaidoku |` (equivalently replace the terminal `|` with `| kaidoku |`). Do **not** concatenate another leading `|` after the existing delimiter: that would create an empty extra cell. No affected row has an escaped terminal pipe or an ambiguous boundary. Existing six cells remain unchanged; only the seventh owner cell is added. Under grammar v2 this restores original cell 5 as pinned and cell 6 as write scope; their prior misinterpretation as write/owner was the missing-column defect, not a new content change.

Replace only the matching complete lines with:

```text
| `tools/round-70/packed-elf.py` | gate — R70-C1/C2/C3: supersession of the round-69 packed-ELF route (kept byte-identical at its own round) — the provenance-bound `--check-receipt --root . --rev <rev>` (revision + instrument-hash binding, the frozen CARRIERS/DECLARED_ORIG/DECLARED_PACKED tables, ratio = round(ceiling/orig, 4), packed <= ceiling, format re-derived from `readelf -h`, arms/control/packer/runs/`before_ceilings` all read), the safe packer seam (hash before the first execution of `--upx`, the validated path threaded through pack/list/unpack/control, `build_child_env()` four-key allowlist, typed `broken_tool: node` and packer refusals, per-run mkdtemp scratch, 23-case selftest with the child-env cases), and the fourth carrier `static-exe` `/usr/bin/docker-init` | 0=met: carriers_matched 4 of 4, control_ok true, failing []; 1=not met: each false arm or failed clause named, the receipt still written; 2=could-not-evaluate (missing/broken node/git/readelf/upx, unusable `--work`, packer version/sha256 mismatch, unreadable packer, carrier pin drift, REA package pin drift, unknown revision, bad argv) | `--selftest` (23 cases incl. the three child-env cases and the case inventory) | `.ufo/waves/round-70/l1/scores/c3-check-at-landing.json` at the landing | write scope: carriers rebuilt under `--work`, receipts to `--json-out`; never the lane tree | kaidoku |
| `tools/round-70/mutation-check.py` | gate — R70-C1 battery: patch sets r68/r69/r70 (the five arm-false mutants), `--expect-target-sha256` (target pin enforced), `--min-pristine-cases` (pristine floor enforced), per-run mkdtemp `work_dir` recorded in the receipt | 0=expectation met incl. pin/floor; 1=missed, each survivor/wrong-case/pin/floor defect named; 2=could-not-evaluate (unknown revision, patch site absent or ambiguous, pristine selftest not green, refused `--work`, bad argv) | `mutation-check.py --validate <receipt>` (rejects mutants-absent, target/work_dir absent, kills with a green rc, survivors/failed inconsistencies) | `.ufo/waves/round-70/l1/scores/c1-at-landing.json` `battery_arms` | battery receipts name their `work_dir`; the battery never edits the frozen tools | kaidoku |
| `tools/round-70/contract-probe.py` | gate — R70-C1 corroboration and the R69-C2 probe, hardened: six arms (missing node, unwritable work, packer impostor, bumped pin, registry-bound A5 carrier records incl. counts/ratios/format, A6 host-packer pins + producer binding) with the harness HOME inside `--work` and per-run mkdtemp | 0=all six arms pass; 1=arms failed, each named with its observation; 2=could-not-evaluate (unknown revision, missing host tool, bad argv) | `contract-probe.py --validate <receipt>` (arm rows, observations, `arms_passed`/`failed`/`target` consistency) | `.ufo/waves/round-70/l1/scores/c1-at-landing.json` `genuine.probe_*` | A5/A6 read a receipt only through the producer binding | kaidoku |
| `tools/round-70/seam-probe.py` | gate — R70-C2: seven black-box arms (A1 hash-before-exec with an execution log, A2 threaded pinned-copy path from the producer-bound receipt, A3 committed child-env cases + green selftest at that count, A4 typed `broken_tool: node`, A5 typed exec-format refusal, A6 no-/tmp HOME fallback with the source literal check, A7 per-run distinct work dirs from two green battery runs invoked without `--pkg`) | 0=all seven arms pass; 1=arms failed, each named; 2=could-not-evaluate (unknown revision, missing host tool, bad argv) | `seam-probe.py --validate <receipt>` (arm rows, observations, `arms_passed`/`failed`/`target` consistency) | `.ufo/waves/round-70/l1/scores/c2-at-landing.json` (7/7) and `c2-at-base-recheck.json` (0/7) | A3/A6 rest on S272; A3's runtime capture and A7's concurrency coverage stay routed (M70-6) | kaidoku |
| `tools/round-70/forged-receipts.py` | gate — R70-C1 battery: ten frozen forged shapes (wrong-rev, wrong-instrument, relabelled-source, ratio-underived, inflated-orig, before-over-limit, rows-vs-matched, dropped-arm, unknown-carrier, absent-instrument) + landing-world probe shapes F3L/F9L, per-shape declared clause and declared probe arm, genuine-receipt pass, battery pin/floor/work-dir/constant arms | 0=every arm shows what it must; 1=failing arms named; 2=could-not-evaluate (unknown revision, unreadable material, bad argv) | `--selftest --root . --base-rev <base> --base-tool <r69 tool> --work <owned scratch>` (7 cases incl. the wrong-world control); `--validate <receipt>` | `.ufo/waves/round-70/l1/scores/c1-at-landing.json` | shapes are cut from the base-world receipt (QUALITY #115) | kaidoku |
| `tools/round-70/controls.py` | gate — the round's seven do-nothing/positive controls: base accepts a wrong-rev shape, constant battery rejected, base exec-format traceback, base impostor executes, new instrument refuses unrun, base three-carrier world, new checker rejects the old receipt on producer binding | 0=every control shows what it must; 1=any control misses, named; 2=bad argv or unreadable revision | `controls.py --validate <receipt>` (seven arms, ok/failures consistency) | `.ufo/waves/round-70/l1/pre/controls-at-declaration.json` and `scores/controls-at-landing.json` | arms name the defect's presence at the base, never the claim's target | kaidoku |
```

### Paste-ready LOG disclosure (append as a new round-71 entry)

Round-71 registry repair disclosure (R71-C3): the following six round-70 SKILL.md registry rows omitted their owner cell. For each, old→new is the exact filed six-cell line → the same six cells with a seventh `kaidoku` owner cell appended: `tools/round-70/packed-elf.py`, `tools/round-70/mutation-check.py`, `tools/round-70/contract-probe.py`, `tools/round-70/seam-probe.py`, `tools/round-70/forged-receipts.py`, and `tools/round-70/controls.py`. No prior content cell is edited, no other SKILL.md line changes, and the four round-69 eight-cell rows remain byte-identical and are read by grammar v2's pinned-cell join rule. The historical omission remains disclosed; this is an intentional repair of the live registry, not a rewrite of filed round-70 LOG/report/lesson bytes. Exact old and new lines are recorded in ReviewerRepairs/evidence.json and the replacements in ReviewerRepairs/review.md.

## Residual risk / verification gaps

- Frozen state is intentionally before record repairs: this review confirms the intended replacement bytes and disclosures, not a future landing. L1 must check its final SKILL diff contains only these six owner additions and must not claim the routed dispositions have already landed.
- Runtime C1/C2/C3 outcomes, saturation scores, full counter caller semantics, nonce confidentiality, canonical-runtime routing and resume_continuity_v1 are not exercised by this document/registry assignment. No such runtime/resume code is changed in this review; do not infer broader guarantees from these results.
- LSP device unavailable: `read xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics service could be invoked. Used frozen Git bytes and literal parsing instead; no grep result is presented as semantic proof.
- No installs, package changes, commits, pushes, instrument edits, sibling edits or fleet-root writes. Scratch contained no fixtures and was removed before handoff. Only seat report/evidence/comparison artifacts were authored.

Self-evaluation: accuracy 4 (byte checks observed; future dispositions deliberately unverified), completeness 4 (all requested frozen checks/drafts covered; LSP unavailable), clarity 4 (long exact rows necessary for paste-ready repair), actionability 4 (exact replacements and two concrete errata), conciseness 4 (full evidence retained separately). Overall 4.0/5. Highest-impact integration action: close the historical R70 settlement gap without manufacturing per-seat statuses; then append the declaration-hash erratum. User-agreement self-check: report separates observed passes, defects and unexecuted future work.

VERDICT: defect named — frozen predicates/pins/scope/row preservation met; round-70 settlement disposition unanswered and declaration hash misattributed.
