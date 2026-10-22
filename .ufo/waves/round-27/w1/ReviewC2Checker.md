# R27-C2 reviewer report — ReviewC2Checker (wave 1, 2026-10-22)

Attack target: tools/round-27/c2-xpin-check.py at lane HEAD a4f674b343d8564e21f7eb8984630a95089c82d6,
against R27-C2 in .ufo/waves/round-27/claims.json. Lane untouched except this report file.

## Checks and verdicts

1. Checker file identity — holds (observation).
   `sha256sum tools/round-27/c2-xpin-check.py` → d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3,
   equal to the claims.json instruments entry. Exit 0, 2026-10-22T14:58Z.

2. Frozen package sha256 values — holds (observation).
   `sha256sum` of the four FROZEN_FILES, exit 0, 2026-10-22T14:52Z:
   6.5.0 package.json a5003023…050a6c, 6.5.0 dist/domain/evidence.js f992d93e…78dcff,
   6.7.0 package.json 3f6c47fb…ebb570, 6.7.0 dist/domain/evidence.js a3fb9f02…29c0fb — all four
   match the checker's table exactly.

3. Checker 6.7.0 rule vs 6.7.0 package — holds (observation + inference).
   ids_for() builds `recompute.semantic_projection(data)` then sets
   `projection["relationship_coverage"] = data.get("relationship_coverage")` unconditionally.
   The 6.7.0 projection at dist/domain/evidence.js lines ~164-186 lists the same 15 fields with
   `relationship_coverage: evidence.relationship_coverage` unconditional. Field-for-field equal.
   Empirical closure: my Node recompute (packages' own digestCanonicalValue, projections
   transcribed from each evidence.js) gives checkerId67VsPackageId67Mismatches=[] over 24+3 fixtures.

4. Checker 6.5.0 rule vs tools/round-26/recompute-ids.py — holds by construction (observation):
   measure() does `recompute = load_module(show(root, rev, RECOMPUTE_PATH), ...)` at REV, and
   id65 = recompute.compute_evidence_id(data). recompute-ids.py's semantic_projection and
   canonical_json mirror the 6.5.0 evidence.js projection field-for-field (checked line by line).
   Empirical: all 24 stored round-26 ids re-derive under the 6.5.0 package code
   (storedMatchesPackageId65ForAll24=true), so the mirror is faithful on this corpus.

5. Attribution rule — holds (observation). attribution() checks `both` first, then 6.5.0, 6.7.0,
   else `none`; matches the statement's <6.5.0|6.7.0|both|none>. check_rows requires the tool's
   four printed cells to equal [stored, id65, id67, attribution] exactly.

6. Three red envelopes — holds (observation + inference).
   red_cases(): red-tampered (normalized_result replaced → none), red-minted-67 (id re-minted
   under the 6.7.0 rule → 6.7.0), red-coverage-set (coverage set, id re-minted under 6.5.0 → both),
   all derived from the first sorted envelope with null coverage (analyze-base.json). My Node
   script re-derived all three under the packages' own code: got none / 6.7.0 / both, and for
   red-minted-67 checkerMintEqualsPackageMint=true — the checker-minted id equals what the real
   6.7.0 package code produces.

7. Capability-row and source-row parsers — holds (observation).
   capability_row: a `|` row inside `## Capabilities` naming tools/round-27/xpin-attribute.mjs.
   source_row: S-id new since BASE, ≥11 cells, mark a1722018f28f9df2 in the source cell (row[1]),
   row[7]=="mined", row[8]=="2026-10-22", id listed in round-27 `## Gate`. Verified against the
   live SOURCES.md header (line 5: id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|
   used-by) — status is cell 7 and opened cell 8, so the indices are correct for the real table.
   The checker's own rows-fixture (5 cases) passed in the selftest.

8. Independent package-code recompute (Node, assignment script) — holds (observation).
   Command: `node recompute-r26.mjs` on the 24 envelopes extracted via `git show HEAD:…` (aggregate
   extraction hash 42ca185e260b736134103757e18e545202655a920313c494c198718408ead53f), exit 0,
   2026-10-22T14:57Z. Distribution under each package's own digestCanonicalValue:
   6.5.0=21, 6.7.0=0, both=3, none=0 — exactly the expected both=3 / 6.5.0=21, and identical to
   the checker's own printed distribution ("checker attribution of the round-26 envelopes:
   6.5.0=21 6.7.0=0 both=3 none=0", 2026-10-22T15:03Z run). digestCanonicalValue is
   byte-identical across pins (dist/domain/canonicalDigest.js, f46d6bd4…5be81d9 in both).

9. Selftest — pass (observation).
   `python3 -I -B tools/round-27/c2-xpin-check.py --selftest`, exit 0, 2026-10-22T15:01Z:
   "PASS" on all four stub cases, tool-absent-at-base, and 5 rows-fixture cases;
   final line "selftest cases=6 failures=0".

## Findings by severity

F1 (medium, fails — counterexample): the tool's exit code never affects the verdict.
   check_rows appends a reason when run_tool's exit != 0, but measure() returns
   `0 if (r26_ok == R26_TOTAL and red_ok == 3 and cap == 1 and src == 1) else 1` — reasons are
   printed, never counted. Command 2026-10-22T15:03Z: c2-xpin-check.py --root <lane> --rev HEAD
   --tool-cmd "python3 -I -B …/exit1-stub.py …" where the stub prints all 27 correct rows then
   sys.exit(1). Output: "FAIL tool exit 1:" twice, yet "r26_rows_ok=24/24 red_ok=3/3
   capability_row=0 source_row=0", exit 1 only because the SCORECARD/SOURCES rows do not exist
   yet. At a REV where they exist, this claim passes (exit 0) while the statement's tool contract
   ("exit 0") is false. A tool that crashes after printing also lands here.

F2 (medium, fails — disclosed reviewer item): the checker cannot detect a retyped projection.
   claims.json limits admit this. Demonstrated: the selftest's own correct-stub and my exit1-stub
   import neither rea-agents package and still score 24/24 + 3/3; the statement's tool_contract
   ("ids must come from each package's own exported digestCanonicalValue and that package's own
   semanticProjection source text") is unenforceable by this checker. Mitigation from this review:
   the checker's recompute equals both packages' own code on all 27 fixtures today, so any tool
   passing today agrees with the packages on this corpus. Residual: FROZEN_FILES pins
   evidence.js and package.json but NOT dist/domain/canonicalDigest.js (the digest primitive a
   retyped tool could silently diverge from after a future re-pin).

F3 (minor, latent, dormant): absent-key divergence in the 6.7.0 patch. For a record where
   relationship_coverage is absent, ids_for sets explicit null while 6.7.0 code reads undefined,
   which emitCanonical drops (canonicalDigest.js: `if (Reflect.get(value, key) === undefined …)
   continue`). The checker would then demand an id the real 6.7.0 package cannot produce (false
   rejection of a correct tool) and attribute "6.5.0" where real-code attribution is "both".
   Dormant on this corpus: no projected field is absent in any of the 24 records (my script's
   projectedFieldsAbsentInStoredRecords is empty).

F4 (minor): the red selftest breaks once the claim goes green. selftest() takes
   `rev = git(lane, "rev-parse", "HEAD")` and requires `got == 1` for the four stub cases; after
   the build seat commits the SCORECARD/SOURCES rows, correct-stub exits 0, the case is recorded
   FAIL, and the committed selftest exits 1 on a passing claim. Valid only at the freeze commit.

## Inputs the checker accepts while the statement is false

- Any tool that prints the 27 correct rows but exits nonzero or crashes afterward (F1).
- Any tool whose ids come from a retyped projection or no package import at all, as long as they
  equal the checker's recompute (F2) — includes today's stubs.
- A tool printing extra stdout lines for paths outside the fixture set (run_tool ignores them;
  statement says one line per envelope) — cosmetic.

## Residual risk and verification gaps

- xpin-attribute.mjs is absent at HEAD (`git ls-tree HEAD tools/round-27/` lists only the two
  counters), so the real build-seat tool is unverified: unknown, not failed. My 24/24 agreement is
  checker-recompute vs package-code, not vs the actual tool.
- Float-formatting and lone-surrogate paths of canonical_json vs emitCanonical were not
  fuzz-tested; [INFERENCE] the corpus exercises none of them (all 24 stored ids re-derive).
- No external sources opened this round; all evidence is local (files and sha256s listed above),
  access date 2026-10-22. No tools installed (node v24.21.0 and python3 3.14.8 already present).

## Artifacts (under /fast/scratch/hyaku/kaidoku-r27/seats/ReviewC2Checker/)

- recompute-r26.mjs — 5e969f7fec2390bc873f0293fabd2a08873c2abb06f77881ed17b916e6f8b87d
- exit1-stub.py — efae4826432a727f74380520fd44e4854bd29aefb20a117239dc6675abe5f27b
- envelopes/ (24 files from git show HEAD) — aggregate sha256 42ca185e260b736134103757e18e545202655a920313c494c198718408ead53f
- tmp/ (empty, unused — no REA calls needed)

Overall: the checker's rules, red fixtures, parsers and frozen pins are sound and independently
confirmed against both packages' own code; fix F1 (count tool exit) and optionally F2/F4 before
the wave closes.
