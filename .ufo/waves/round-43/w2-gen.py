#!/usr/bin/env python3
"""Generate the round-43 wave-2 falsification spec (32 distinct attacks)."""
import json
import os
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE = f"{LANE}/.ufo/waves/round-43"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r43"
FREEZE = "f3f8db389416d094b1ddeb1215ddcf914bfc0d1c"
PLAN = f"{LANE}/plans/round-43-claims.md"
GOD = open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")).read().strip()

context = f"""# Target
Kaidoku round 43 wave 2 = FALSIFY the integrated, frozen round-43 claims and their landed artifacts. Lane root: {LANE}. L1/integration owner: KaidokuR43. Round freeze: {FREEZE}; read the frozen plan FIRST ({PLAN}), then read the current lane tip and the committed C1/C2 score/control receipts. The base round has 32 settled wave-1 seats and >32 distinct attack findings; this 32-seat wave is the falsification wave required by the round-42 open defect R42-CL2. Do not re-open the claim design or change frozen predicates; attack whether the frozen claims, tools, receipts, data and landing meet those exact predicates. Record the full measured revision at which each attack is evaluated.

# Attacks
Every item names one independent attack surface. Run only the checks in its text and read-only reproduction against committed bytes. Attack C1 and C2 separately where assigned; do not infer a green from a summary field when the underlying bytes can be re-read. If the data run or a claim score is an honest stop, attack the stop evidence and report that outcome without manufacturing missing inputs. The lane owner will integrate; this wave is read-only.

# Reserved inputs
Never run REA, unblob, sasquatch or any extractor on a PUBLISHED third-party firmware image or anything carved from it. Allowed REA inputs are only the pinned MIT unblob 26.6.4 test fixtures under {LANE}/corpus/evidence/round-42/c2/fixtures/, round-42 generated carriers, and freshly generated local trees. No published firmware bytes are to be opened or copied.

# Bounds
Each seat writes ONLY its report and artifacts under {WAVE}/w2/ and scratch under {SCRATCH}/w2/<seat-name>/; every `Report:` trailer is relative to {LANE} and must be written under that absolute lane path. No lane production edits, no commits, no VCS mutation, no fleet/sibling/shokuknow writes, no agent://all, no subagents/background jobs. Check in your report the exact paths and hashes you read, commands, outputs, exit codes, and limitations; mark inference. Do not run formatters/tests/linters on the whole repo. Scratch must be removed before yield.

# Tooling and safety
The operator's installation policy is authorized: before any installation read /home/vgpnk/.omp/agent/RULES.md and record tool/version/channel/reason. No installation is expected. Pacman is paused host-wide; never run pacman. Check disk-guard status before a heavy probe; if ENOSPC occurs, report free space and do not rerun until green. Use git read-only on the lane and use `git -C <scratch clone>` for any fixture commits; verify the clone toplevel before the first commit. One wave, 32 members, no replacements.
"""

ATTACKS = [
("R43W2C1Predicate", "reviewer", "Line-by-line P43-C1 predicate audit: for every frozen sentence, identify the implementing binding and receipt field at the final measured revision; compare plan, c1-counter, and receipt. Flag any missing/extra binding or contradiction; do not change the claim."),
("R43W2C1Predictor", "critic", "Adversarially search the frozen heldout-gen-v4r43 combo predictor against its committed tuple_check/REA envelopes. Focus on depth-limited extraction-output classification (including C05 residue-only, C02 v4 failure, wrap, two-chunk, dep, depth 3). Re-derive factors and compare all 24 combos; give exact tuple diffs or all-equal evidence."),
("R43W2C1Mutation", "mutation-tester", "Apply the R43MutGen 20 single-fault mutations to the frozen generator/counter in a scratch clone only. Confirm each intended red/green witness, including C02, all six one-field mismatches, order semantics, tuple_check self-certification, and no-manifest refusal. Report survivors and exact outputs."),
("R43W2C1Counter", "reviewer", "Review c1-counter-r43.py clause-by-clause against P43-C1 and final score JSON. Recompute one binding from committed envelope bytes, one freeze-drift binding from git objects, and the runjson digest binding; identify any value the receipt does not derive."),
("R43W2C1Merge", "critic", "Falsify freeze integrity with scratch git histories: evil merge changing a frozen blob, delete/re-add identical blob, merge touching SKILL status prose, and non-ancestor FREEZE. Confirm c1-counter exit 2 and named reason for each; ensure the fixture repo is isolated and clean."),
("R43W2C1C02", "scout", "Re-open committed round-42 C02 manifest and rea-full/envelope records plus round-43 CTL-C1-2 receipts. Independently compute declared vs observed tuple and verify the red is exit 3/no manifest and the green differs only by the correct observed declaration."),
("R43W2C1Regen", "reviewer", "Attack carrier/tree regeneration: compare all 78 carrier.sqsh and tree.json bytes to a --carriers-only regeneration at the frozen seed in a scratch clone; verify H43's seed-independent exception is not overclaimed and no manifest is needed."),
("R43W2C1CounterMut", "mutation-tester", "Mutate one declared_features field, one declared_extras value, one run.json handler list, and one subject digest in independent scratch copies. Confirm c1-counter flips the exact binding and does not read generator.tuple_check as observed truth."),
("R43W2C1Lookup", "critic", "Recompute combo_unseen_majority from the committed dev-arm named tuple union and the heldout observed tuples; separately score CTL-C2-7-lookup and prove it is reported, not bound. Attack the union source and any threshold/count discrepancy."),
("R43W2C1Controls", "reviewer", "Review final CTL-C1-0..4 and the reference witness receipts. Check argv/tool hashes/freeze, stale-manifest firing bindings, red/green tuple behavior, shortcut misses, and CTL-C1-4 envelope bytes unchanged; flag any control misclassified as a kill arm."),
("R43W2C1Set", "scout", "Independently enumerate the final heldout manifest and evidence tree: 27 named classes x2 plus 24 combos, all five files/carriers, IDs unique, subject digests, tuple_check coverage, effective_n/vacuous OOD IDs. Report exact counts and mismatches."),
("R43W2CrossClaims", "connector", "Cross-axis scan of the frozen C1/C2 claims, controls, and final receipts: look for a shared input or landing path that violates the separability claim, a score reused across claims, or a mutually dependent assertion. Give file/field evidence."),
("R43W2SentC1", "sentinel", "Security/provenance review of C1 generator and score receipt: look for path traversal, symlink-following, untrusted JSON, unsafe subprocess arguments, out-of-scratch writes, or fabricated subject digests. Only inspect code/receipts; do not execute REA on prohibited inputs."),
("R43W2C2Predicate", "reviewer", "Line-by-line audit of P43-C2 against the final c2-score-r43 receipt, gate JSON, copy-audit TSV, frozen paths and map. Confirm each clause has a measured field and actual committed evidence; flag missing checks."),
("R43W2C2Gate", "critic", "Attack the frozen local-source-gate on a clean clone at final REV: absent map, missing copy, wrong digest, stale --rev label, --sources/--map override, and worktree shadow. Verify the c2-score tool refuses to accept anything except the clean-clone invocation."),
("R43W2C2MapMut", "mutation-tester", "Mutation-test the final map/linter in isolated clones: duplicate JSON keys, duplicate copy alias, symlinked component, absolute/../ path, stub+matching digest, >5MiB file, and missing S126. Each must fail the correct structural/content binding."),
("R43W2C2Registry", "reviewer", "Recompute the base-to-final corpus/SOURCES.md delta and count rows. Check S135/S136/S137 are the only additions, their used-by entries exist, all base row bytes remain, and the frozen registry bytes are unchanged after FREEZE."),
("R43W2C2Pins", "critic", "Independently re-audit the 41 anchor digest slots over the 18 rows against the committed local copies and upstream substrates. Verify S048's 28 members and name the remaining structural slots; do not accept map sha alone."),
("R43W2C2Host", "scout", "Re-open the host sources and upstream fallback receipts for S035, S081, S048, S082. Verify absent-host classifications, Go-tag member identity, npm tarball pins, and no claim that absent objects are live-equal."),
("R43W2C2Linter", "reviewer", "Review verify-copies-r43.py and c2-score-r43.py. Re-derive `expect-source-frozen`, map digest, S126 preservation, row count, and linter check count from committed bytes; test whether a changed imported EXPECT table can escape."),
("R43W2C2MutPack", "mutation-tester", "Mutation-test the final pack with one-byte corruption in S048, a row-pinned member omission, a gzip payload mutation, and a changed S035 tar member. Confirm the content verifier fails even when map digest is adjusted to match a stub."),
("R43W2C2Worktree", "critic", "Attack the clean-clone and source-table guards: simulate uncommitted maps/copies and a SOURCES row rewrite/removal. Confirm the gate may green a dirty worktree but c2-score refuses the dirty clone and the frozen registry check catches post-freeze changes."),
("R43W2C2Score", "reviewer", "Check the final C2 score receipt's self-consistency: gate and copy-audit wrappers, resolved REV, tool digests, map/SOURCES hashes, numstat and S126. Re-run read-only derivations; explain any false binding such as extra formatting-only numstat."),
("R43W2CrossEvidence", "connector", "Cross-claim provenance scan: check shared S135, SOURCES.md, SKILL.md, and evidence paths are bound consistently across C1/C2; identify a path or digest cited by one claim but mutated by the other."),
("R43W2SentC2", "sentinel", "Adversarial path/security review of local-source gate, map parser, symlink handling, archive extraction and c2-score scratch clone. Look for traversal, archive bomb, unsafe links, or host-path leakage; report only concrete reachable cases."),
("R43W2AssimEntry", "reviewer", "Review the landed sasquatch release-matrix knowledge entry against S136/S137 and its retained fetch receipts. Check provenance trio order, tag/size/digest values, R36 falsification reversals, S107 overlap citation, and body-limit calibration."),
("R43W2AssimFlip", "critic", "Try to falsify the assimilation admission flip on fresh official API/page bytes: ninth release, changed asset set, body version-pair, changed digest-presence pattern. Use read-only network/source checks and preserve receipts under your w2 artifacts."),
("R43W2AssimCitations", "scout", "Re-open every source citation in the assimilation entry and independently verify the page-vs-API boundary, row anchors, recheck projection, and S136/S137 row schema. Do not fetch or write to shokuknow."),
("R43W2Skill", "reviewer", "Verify SKILL.md R42-V3 status paragraphs and v3/v4 region hashes at anchor/freeze/REV; check command A remains 21/21 and no citation or rule-block count shifted. Report exact hashes/counts."),
("R43W2Mistakes", "critic", "Adversarially review round-43 lesson M43 candidates and routed defects: ensure each adopted mistake has a captured-by QUALITY/prompt rule, evidence pointer, and a fix that is actually implemented; flag candidate duplication or unsupported closure."),
("R43W2Scorecard", "connector", "Audit the final SCORECARD/SHONEN/LOG/PROVINCE after L1 landing: verify before/after counts, axis/capability score deltas, planned next round, assertion citations, and no surface was silently narrowed."),
("R43W2Closure", "scribe", "Review the final round report against committed lane/fleet evidence: verify every hash, count, command, control verdict, round shape, C2/C1 status, tool install statement, and explicit residual risk. Return only factual corrections, not a second verdict."),
]

items = []
for name, role, task in ATTACKS:
    prompt = ("/skill:godspeed\n\n" + GOD + "\n\n" + task +
              f"\n\nReport: {WAVE}/w2/{name}.md and artifacts: {WAVE}/w2/artifacts/{name}/.")
    items.append({"name": name, "role": role, "prompt": prompt,
                  "axes": ["coverage", "calibration", "depth"]})

spec = {
    "wave": "r43-w2",
    "milestone": "Round 43 wave 2: falsify frozen C1/C2 claims, controls, landed evidence and assimilation",
    "reportDir": ".ufo/waves/round-43/w2",
    "context": context,
    "items": items,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1)
print(len(items), Counter(i["role"] for i in items))
