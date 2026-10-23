# A2Capability27 — R32-C2 v3, statement round-27 `cross-pin evidence-ID attribution`

Seat: `KaidokuR32A2.A2Capability27` (reviewer, leaf, no subagents). Audit lane: attempt-2 pre-data controls, kaidoku round 32.
UTC window: 2026-10-23T06:47Z → 2026-10-23T06:57Z. Read-only on lane and fleet; every git call ran inside my unique sandbox clones with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset and `git -C <absolute>`.

- Sandbox: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability27` — `lane` clone HEAD `f382e3b7978e6091a19ca93277c15a75c0016b43`, `fleet` clone HEAD `575bcedac44943fae1cd43f9030aea7662ddb6be`; pin `cef00867` is ancestor of fleet HEAD (`merge-base --is-ancestor`, exit 0).
- Revisions: lane base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`; claims.json freeze `9a73680a`; claims-v3.json freeze `f382e3b7978e`; fleet pin `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- Tool installs: none (node v24.21.0, python3, jq already present). No lane/fleet/scorecard edits; no summary repair run.

## 1. Freeze and pin integrity (exercised)

- `claims-v3.json` blob at `f382e3b7:...` = `7d38b604313d7ff5a9f03bf446eb4eb1c5d9f0ad`; `git hash-object` of the working-tree file = identical → unchanged since freeze. `git log f382e3b7..HEAD -- claims-v3.json` = empty.
- `claims.json` blob at `9a73680a:...` = `59ff7d70012d728807ee2757b02d72300d46d7c1` = working-tree file → unchanged; log after freeze = empty.
- MANIFEST: `git show cef00867:MANIFEST.json` (1,242,275 B) re-hashed = `e6fc0394f5d5d49c665b8575500d3caff182a427` = pinned blob id.
- Counter instrument sha256 `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` equals the claims-v3 instruments pin.

## 2. Statement, anchors (exercised re-derivation)

MANIFEST round entry `lane=kaidoku round=27` (`type=closure`, `admitted=false`, `verdict=rejected-honest-stop`, `verification.reviewer` = "hyaku-closure (@m_opus session, non-author)", `closed_at` 2026-10-22T16:14:35Z). Its single `capabilities_added` item, verbatim:

> cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27)

Independent anchor computation (counter's own regexes re-implemented): MANIFEST item yields `{tools/round-27/xpin-attribute.mjs}`. The card at base holds 4 capability tables (`SCORECARD.md:617, 2134, 2206, 2373`); the three outside-`## Capabilities` rows (`:2135`, `:2207`, `:2374`) match keys 13/14/17, not key 27; the only other `cross-pin` line, `:3097` first cell "R27-C2 cross-pin attribution tool, capability row, S081", is a claims-table row and lacks "evidence-ID". So anchor set = `{tools/round-27/xpin-attribute.mjs}` — exactly `anchors_at_freeze["27"]`. No discrepancy.

## 3. Anchor re-opened: capability evidence, not existence alone

1. **Tool source** (`tools/round-27/xpin-attribute.mjs`, 267 lines, 10,887 B, sha256 `8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708` at base — equals the build seat's recorded artifact hash in `BuildXpinTool.md`). Header: "Neither pin's rule is retyped here." (:18); mechanism imports `digestCanonicalValue` and extracts `const semanticProjection` from each installed package's own `dist/domain/evidence.js` source, per pin — a bracket-scanner extraction, not a regex, per `BuildXpinTool.md` lines 24-36.
2. **Exercised re-derivation (this seat).** I extracted the 24 committed round-26 envelopes at base rev and ran the base tool:
   `argv=[node, ev/tools_round-27_xpin-attribute.mjs, --pkg65, /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents, --pkg67, /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents, <24 envelope paths>]`, `ulimit -v 4194304`, `timeout 900`. Exit 0; 24 TSV lines; sorted output sha256 `b3c152811440cb8dc951e0e53c651bb809287345a062e65a8cc61bd48b6a4bbc` — **byte-identical to committed `corpus/evidence/round-27/c2/r26-attribution.tsv`** (same sha256, diff empty). Counts: `6.5.0=21, both=3, 6.7.0=0, none=0`.
3. **Exercised checker (this seat).** `python3 -I -B tools_round-27_c2-xpin-check.py --root <sandbox lane clone> --rev 283aad7f` (sha256 `1c8259a8fe4f…636783` = post-round-29-revision instrument) → stdout `checker attribution of the round-26 envelopes: 6.5.0=21 6.7.0=0 both=3 none=0` / `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)`; **exit 0**. `red_ok=3/3` exercises the `6.7.0`/`none` attributions on checker-generated red envelopes.
4. **Committed receipts at base**: `after/c2-at-97358f75.txt` exit 0 (identical verdict line); `before/c2-at-cd32264f.txt` exit 1 ("FAIL tools/round-27/xpin-attribute.mjs absent at REV" — pre-data baseline); `before/c2-selftest.txt` 6/6 PASS.
5. **Non-author closure re-derivation** (MANIFEST `verification.rechecks`, quote ≤25 words): "re-running xpin-attribute.mjs from a git archive of the tip: output byte-identical to r26-attribution.tsv (21 6.5.0, 3 both; stored=6.5.0 id 24/24)"; red envelopes "attribute 6.7.0/none correctly". My run is a second independent re-derivation agreeing byte-for-byte.
6. **Rule-fit discrimination**: `keyless-default.tsv` (37 `both`) vs `keyless-parse.tsv` (6.7.0 rejects all 37) — default and `--parse` modes behave per package semantics, separating the capability from a stored-id echo. Consistent with claims limits: attribution is a rule fit, "not a 6.7.0 run".

## 4. Counter at base (exercised, sandbox clone)

`argv=[python3, -I, -B, tools/round-32/c2-capability-calibration-v3.py, --root, <lane clone>, --rev, 283aad7f, --fleet, <fleet clone>]` →
`round-27 P2-match row 5 anchor evidence tools/round-27/xpin-attribute.mjs; description words 16`; `statements=4 match=1 target=4 reverse_mismatch=0`; **exit 1** — reproduces `a2before/c2v3-base.txt` and the claim text exactly. `--selftest`: `cases=18 failures=0`, exit 0 (reproduces `a2before/c2v3-selftest.txt`).
Reverse domain note: `closed` = rounds 12..31 (MANIFEST entries carrying an `admitted` key; earlier duplicate entries for 13/14 lack it and carry no `capabilities_added`); the section's other last-cells (`luna-round-6`, `luna-round-8`, `arc2-loop1-round2`, `arc2-loop1-round7` → 6,8,2,7) are outside `closed`, so `reverse_mismatch=0` is structural, not coincidental.

## 5. Semantic vs lexical overlap limits

- The ≥5-word gate is purely lexical: distinct `[A-Za-z][A-Za-z-]{3,}`, case-folded, **no stemming** — `attributes` (row) vs `attribution` (MANIFEST) and `envelope`/`envelopes` never match. Of the row cell2's 17 qualifying words, 16 appear in the shared set; the MANIFEST item contributes only `saved` to that set (my replication, exact counter regex).
- **For statement 27 the gate is self-satisfying.** The anchored description = MANIFEST item ∪ cell2 of *every* base capability row matching the key — which includes the in-section row :623 itself. Any row matching key 27 with ≥5 words in cell2 passes, whatever the MANIFEST wording. For keys 13/14/17 (no matching inside-row) the union binds outside-row+MANIFEST words and is a real check.
- The evidence gate is equally lexical: a backticked span must be in the anchor set and resolve at REV (`ls-tree`). Row :623's cell3 has 4 ticked spans; only `tools/round-27/xpin-attribute.mjs` is an anchor (`corpus/evidence/round-27/c2/` is a directory and cannot match `REL_PATH_RE`; `c2-xpin-check.py`, `BuildXpinTool.md` resolve but are not anchors). Counter/claims limits quoted: "the evidence check is anchor-path presence and resolution, not that the path demonstrates the capability".
- My capability verdict therefore rests on the exercised re-derivation (§3.2–3.3), not on the lexical gates.

## 6. Faithfully copied summary row — draft only (evidence exists)

Verbatim from `SCORECARD.md@283aad7f:623`, the record the MANIFEST item itself cites:

`| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |`

Draft only; no lane edit made before controls land. If the identical row is committed post-controls, forward statement 27 stays satisfied (selftest case `do-nothing`: match=1, reverse=0).

## 7. Findings and residual risk

- **Verdict: not falsified.** The frozen anchor demonstrates a real, exercised capability: byte-identical re-derivation of the committed attribution receipt under both pins' installed code, checker exit 0 at the base, closure re-measurement agreeing.
- Residual (limits-class, lexical): description-overlap gate is vacuous for statement 27 (self-union, §5); a paraphrased row would still pass.
- Residual (limits-class, lexical): predicate binds only 1 of the row's 4 evidence pointers; the receipts dir and checker file are unverified by the counter (verified here by reading/running).
- Caveat (semantic scope): "Receipts hold no real `6.7.0` label yet" (`SCORECARD.md:3126` at base) — `6.7.0`/`none` verdicts exist only on generated red envelopes and one uncommitted wave-2 sweep; capability is rule-fit attribution, no live 6.7.0 REA run exists anywhere (round-27 claims.json `limits` agrees; tool source confirms).
- Caveat: `c2-xpin-check.py` "does not fail on a non-zero tool exit code" (`SCORECARD.md:3168` at base); checker-green alone does not imply tool exit 0 — supplied here by direct run, exit 0.
- `anchors_at_freeze["27"]` and the counter's anchor set agree byte-for-byte; selftest case `fake outside anchor row added at REV is ignored` keeps the set fixed at base.

## Trailer

- Report: `.ufo/waves/round-32/a2audit/A2Capability27.md` (under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`).
- Artifacts in scratch: extracted SCORECARD/MANIFEST at pinned revs; `ev/` = base-rev tool/checker/report/receipts/TSVs (filenames mirror source paths, incl. one `.py` evidence copy — an extracted file, not a marker); `env26/` = 24 envelope extractions (2.9 MB total, copies of committed blobs); `r26-myrun.tsv` byte-identical run output.
- UTC end: 2026-10-23T06:57Z. No processes left running; no installs.
