# R79-C1 — independent re-derivation and falsification (ReviewerC1)

- Target claim: `R79-C1` (calibration), frozen in `.ufo/waves/round-79/claims.json` and
  `plans/round-79-claims.md:32-69`.
- Measured rev: `ed68cd0a6cc790cca342380a2d80d1927a668c8c` (base arm `29d2ca30…`,
  declaration `a1f9b81…`).
- Target blob: `tools/round-78/attack-gate.py` @ freeze, sha256
  `4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf`, 46214 bytes.
- Instrument: `tools/round-79/gate-mutation.py` @ freeze, sha256
  `682f1e7873dcc6ee47355c2cee3aa9359ef519ace6ef0eda5dd8f7135709c86c`.
- Seats run: fresh `--battery` at both revs, fresh `--control empty-set` at base, direct
  `--selftest` at base/declaration/freeze, hand-applied mutant kills, and 17 receipt forgeries
  through `--validate`. All scratch under `/fast/scratch/hyaku/kaidoku-r79/ReviewerC1/`,
  deleted before yield; no lane file outside this evidence dir was written.

**Verdict: no blocking defect.** Every numeric clause of R79-C1 re-derives from the committed
receipt's own mutant list, from a fresh battery run, and from a hand-applied re-run that bypasses
the instrument's judge. Two predicate conjuncts (`exit`, `validate`) are *not carried by the
receipt bytes* and were re-executed; both hold. The `--validate` subcommand is materially weaker
than the predicate's wording suggests: it admits five forgery shapes that contradict the
predicate, so it cannot be the sole admission gate for a future receipt. That is a guard gap in
the instrument, not a false claim here.

## Receipt

```json
{
  "review": "R79-C1",
  "reviewer": "ReviewerC1",
  "rev": "ed68cd0a6cc790cca342380a2d80d1927a668c8c",
  "base_rev": "29d2ca30b83a6a0d85b0aa979de0138fde1660e6",
  "landing_receipt": ".ufo/waves/round-79/l1/scores/c1-at-landing.json",
  "clauses": [
    {"name": "landing.exit", "claim": "0", "rederived": "0 (fresh --battery at ed68cd0a, process exit)", "ok": true, "in_receipt": false},
    {"name": "landing.mutants_total", "claim": "8", "rederived": "8 (8 entries, 8 unique ids)", "ok": true, "in_receipt": true},
    {"name": "landing.killed", "claim": "8", "rederived": "8 (sum of killed flags; all 8 declared cases flip to fail when the anchors are re-applied by this seat)", "ok": true, "in_receipt": true},
    {"name": "landing.survivors", "claim": "0", "rederived": "0 (survivor_ids [])", "ok": true, "in_receipt": true},
    {"name": "landing.survivor_ids", "claim": "[]", "rederived": "[]", "ok": true, "in_receipt": true},
    {"name": "landing.declared_case_hits", "claim": "8", "rederived": "8 (arithmetically identical to killed in this schema; see F5)", "ok": true, "in_receipt": true},
    {"name": "landing.target_pin.matched", "claim": "true", "rederived": "true (git show ed68cd0a:tools/round-78/attack-gate.py = 4e4baf00… = target_pin.expected = target_pin.actual = claims.loaded_by_counter)", "ok": true, "in_receipt": true},
    {"name": "landing.pristine.cases", "claim": "29", "rederived": "29 (direct --selftest at ed68cd0a prints SELFTEST cases=29 failures=0)", "ok": true, "in_receipt": true},
    {"name": "landing.pristine.failures", "claim": "0", "rederived": "0", "ok": true, "in_receipt": true},
    {"name": "landing.validate", "claim": "defect-free", "rederived": "{\"defects\": [], \"mutants\": 8, \"survivors\": 0}, exit 0", "ok": true, "in_receipt": false},
    {"name": "landing.each_declared_case_present_and_fails", "claim": "8/8", "rederived": "8/8 (each mutant re-applied by this seat; each copy printed 29 cases with 1-2 failures, its declared case among them)", "ok": true, "in_receipt": true},
    {"name": "landing.m03_m05_m08_sole_detector", "claim": "true", "rederived": "true (detector_count 1 and failing set == {declared} for each, in the committed receipt and in the independent rerun)", "ok": true, "in_receipt": true},
    {"name": "base.exit", "claim": "1", "rederived": "1 (fresh --battery at 29d2ca30; over-determined by the pin mismatch, see F7)", "ok": true, "in_receipt": false},
    {"name": "base.mutants_total", "claim": "8", "rederived": "8", "ok": true, "in_receipt": true},
    {"name": "base.killed", "claim": "5", "rederived": "5", "ok": true, "in_receipt": true},
    {"name": "base.survivors", "claim": "3", "rederived": "3", "ok": true, "in_receipt": true},
    {"name": "base.survivor_ids", "claim": "[m03-near-miss-re-dead, m05-atom-absent-bound, m08-validate-no-refusal-guard]", "rederived": "identical, same order", "ok": true, "in_receipt": true},
    {"name": "base.declared_case_hits", "claim": "5", "rederived": "5", "ok": true, "in_receipt": true},
    {"name": "base.survivor_mechanism_is_absence", "claim": "absent declared case is a survivor, never a pass", "rederived": "true: all eight anchors applied at base (applied true, exit 0, 26-case selftest), and the three declared cases are absent from that 26-case output; present and green at freeze", "ok": true, "in_receipt": true},
    {"name": "base.pristine.cases (supporting, not asserted)", "claim": "context only", "rederived": "26 (direct --selftest at 29d2ca30); 29 - 26 == the three added cases", "ok": true, "in_receipt": true}
  ],
  "digest_bind": {
    "tools/round-78/attack-gate.py@ed68cd0a": {
      "sha256": "4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf",
      "expected_sources": ["c1-at-landing.json target.sha256", "c1-at-landing.json target_pin.expected", "c1-at-landing.json target_pin.actual", "claims.json loaded_by_counter"],
      "ok": true
    },
    "tools/round-79/gate-mutation.py@ed68cd0a": {
      "sha256": "682f1e7873dcc6ee47355c2cee3aa9359ef519ace6ef0eda5dd8f7135709c86d",
      "expected_sources": ["claims.json instruments", "declaration a1f9b81", "worktree at HEAD"],
      "ok": true
    },
    "tools/round-79/pointer-bind.py@ed68cd0a": {
      "sha256": "91d23dade98d831f8a709e50b8b9925ccb8930f74956993e058c143f24e80a90",
      "expected_sources": ["claims.json instruments", "declaration a1f9b81", "worktree at HEAD"],
      "ok": true
    },
    "tools/round-78/attack-gate.py@29d2ca30": {
      "sha256": "961d5a23c1d38116f5b992434fa2295b5a90643b4a52233e205837ac73bf48c0",
      "expected_sources": ["pre/c1-at-base.json target.sha256"],
      "ok": true
    },
    "tools/round-78/attack-gate.py@a1f9b81": {
      "sha256": "4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf",
      "expected_sources": ["declaration state == freeze state"],
      "ok": true
    },
    "target.bytes": {"value": 46214, "rederived": "git cat-file -s ed68cd0a:tools/round-78/attack-gate.py", "ok": true},
    "declaration_to_freeze_diff": {"files": [".ufo/waves/round-79/claims.json"], "insertions": 42, "ok": true}
  },
  "forgeries": [
    {"id": "a", "shape": "m03 killed true with case_absent true and failed_cases []", "validate_exit": 1, "defects": ["m03-near-miss-re-dead: killed without its declared case failing", "declared_case_hits does not re-derive from the mutant list"], "admitted": false},
    {"id": "a2", "shape": "m03 killed true, failed_cases [red-something-else] (killed by another case)", "validate_exit": 1, "defects": ["m03-near-miss-re-dead: killed without its declared case failing", "declared_case_hits does not re-derive from the mutant list"], "admitted": false},
    {"id": "b", "shape": "mutants_total 8 with 7 entries", "validate_exit": 1, "defects": ["mutants_total does not re-derive from the mutant list", "killed does not re-derive from the mutant list", "declared_case_hits does not re-derive from the mutant list", "ok true but the frozen target is not met"], "admitted": false},
    {"id": "b2", "shape": "consistent shrink: 7 entries / total 7 / killed 7 / hits 7 / survivors 0 / ok true", "validate_exit": 1, "defects": ["ok true but the frozen target is not met"], "admitted": false},
    {"id": "c", "shape": "survivors 0 while survivor_ids names m03", "validate_exit": 1, "defects": ["survivor_ids do not re-derive from the mutant list"], "admitted": false},
    {"id": "c2", "shape": "survivors 0, ids [], one entry killed false", "validate_exit": 1, "defects": ["survivor_ids do not re-derive from the mutant list", "survivors does not re-derive from the mutant list", "ok true but the frozen target is not met"], "admitted": false},
    {"id": "d", "shape": "sole_detector true with detector_count 0 and two failed cases", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F3"},
    {"id": "e", "shape": "killed true with selftest exit 0", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F3"},
    {"id": "f", "shape": "pristine cases 26 (claim requires 29), failures 0, ok true", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F2"},
    {"id": "g", "shape": "target sha256 'b'*64 self-pinned, landed counters", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F1"},
    {"id": "g2", "shape": "target sha256 = base blob 961d5a… self-pinned, landed counters", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F1"},
    {"id": "h", "shape": "empty mutant set with ok true", "validate_exit": 1, "defects": ["ok true but the frozen target is not met"], "admitted": false},
    {"id": "i", "shape": "killed true and inconclusive true on the same mutant", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F4"},
    {"id": "j", "shape": "duplicate mutant id", "validate_exit": 1, "defects": ["duplicate mutant id"], "admitted": false},
    {"id": "k", "shape": "ok true with target_pin.matched false", "validate_exit": 1, "defects": ["ok true but the frozen target is not met"], "admitted": false},
    {"id": "l", "shape": "pristine cases 0, failures 0, ok true", "validate_exit": 0, "defects": [], "admitted": true, "gap": "F2"},
    {"id": "m", "shape": "anchor-miss entry (applied false, killed false) counted as a survivor, ok false", "validate_exit": 0, "defects": [], "admitted": true, "gap": "none: correct admit (a survivor is not a claim of success)"}
  ],
  "sole_detectors": [
    {"id": "m03-near-miss-re-dead", "declared_case": "red-near-miss-unparsed", "committed_receipt": {"detector_count": 1, "sole_detector": true, "failed_cases": ["red-near-miss-unparsed"]}, "independent_rerun": {"summary": [29, 1], "failing": ["red-near-miss-unparsed"], "sole": true}, "ok": true},
    {"id": "m05-atom-absent-bound", "declared_case": "red-atom-absent", "committed_receipt": {"detector_count": 1, "sole_detector": true, "failed_cases": ["red-atom-absent"]}, "independent_rerun": {"summary": [29, 1], "failing": ["red-atom-absent"], "sole": true}, "ok": true},
    {"id": "m08-validate-no-refusal-guard", "declared_case": "red-validate-refused-no-reason", "committed_receipt": {"detector_count": 1, "sole_detector": true, "failed_cases": ["red-validate-refused-no-reason"]}, "independent_rerun": {"summary": [29, 1], "failing": ["red-validate-refused-no-reason"], "sole": true}, "ok": true}
  ]
}
```

## Findings by severity

### High

None. Every measured number in R79-C1's landing and base clauses re-derives; the claim's two
capability statements (eight single-occurrence edits, absent case = survivor) hold against the
bytes.

### Low

**F1 — `--validate` does not re-derive the target pin from git; a self-consistent forged digest is
admitted.** `.ufo/waves/round-79/w1/ReviewerC1/forgeries/forge-g-forged-target-digest.json`
(target sha256 `b`×64, `target_pin.expected` set to the same value) and
`forge-g2-base-digest-self-pinned.json` (the *base* digest `961d5a…` pinned to itself with the
landed counters) both validate clean: `{"defects": [], "mutants": 8, "survivors": 0}`, exit 0.
Cause: `tools/round-79/gate-mutation.py:229-234` only checks `expected == target.sha256` and the
truthiness of `matched`; nothing compares the digest to `TARGET_SHA256` (`:42`) or to
`git show <rev>`. Consequence: the predicate's `target_pin.matched true` and "defect-free
`validate`" conjuncts do not together establish the pin, and claims.json's kill rule ("a receipt
admitted without re-deriving its own target pin") is enforced by the battery at `:297-298`, not by
`--validate`. The landing receipt is nonetheless true: I re-derived
`git show ed68cd0a:tools/round-78/attack-gate.py | sha256sum` = `4e4baf00…`, equal to
`target_pin.expected`, `target_pin.actual`, `target.sha256` and `claims.loaded_by_counter`.
Impact on the claim: none; impact on future admission: a receipt alone can no longer certify its
own target.

**F2 — the pristine case count is not checked.** `--validate` checks only
`pristine.ok` and `pristine.failures == 0` (`:236-238`); `pristine.cases` is never compared with
the predicate's 29. Forgeries `f` (26 cases) and `l` (0 cases) validate clean. The landing value
29 is independently true: `python3 -I -B <blob@ed68cd0a> --selftest` prints
`SELFTEST cases=29 failures=0`, and the base blob prints `SELFTEST cases=26 failures=0`.

**F3 — `detector_count` / `sole_detector` / `exit` are not re-derived.** Forgery `d`
(`sole_detector true`, `detector_count 0`, two failed cases) and forgery `e` (`killed true` with
`exit 0`) both validate clean. The predicate's "each mutant's declared case is present and fails"
and "the three mutants … are detected by that one case alone" therefore rest on the receipt's own
flags. I re-derived both by hand for all eight mutants (see `independent-kills.txt`): every
mutated copy printed 29 cases, its declared case failed, and `m03`/`m05`/`m08` each had exactly
one failing case — the declared one.

**F4 — `killed` and `inconclusive` may both be true in an admitted receipt.** Forgery `i`
validates clean. The kill rule's "a copy without a `SELFTEST` summary counted as killed" is
enforced in the battery (`:277-284`: a missing summary sets `inconclusive` and the entry is
appended without `judge`), not in `--validate`. Not reachable from a battery-produced receipt,
but it means `--validate` cannot police that clause.

**F6 — plan prose conflates the file's current state with round 78's landed state.**
`plans/round-79-claims.md:34-35` reads "Round 78 landed a ten-class attack gate whose selftest
carries 29 cases". The blob at the claimed base `29d2ca30` carries **26** cases
(`SELFTEST cases=26 failures=0`); the 29 exists from declaration `a1f9b81` onward, and the exactly
three added cases are `red-near-miss-unparsed`, `red-atom-absent`,
`red-validate-refused-no-reason` — the declared cases of `m03`, `m05`, `m08` (no cases removed,
base order preserved). The receipts state the 26 → 29 contrast correctly, so this is narrative
imprecision only, with no effect on any predicate number.

### Informational

**F5 — three of the predicate's numbers are one measurement.** `judge` (`:184-197`) defines
`killed := declared present and failing`, and `killed_by_declared` is assigned `killed` verbatim
(`:190`) while `declared_case_hits` counts `killed and declared ∈ failed_cases` (`:294-296`), a
condition implied by `killed`. So `killed`, `killed_by_declared` and `declared_case_hits` are the
same boolean projected three ways; `hits == killed` identically. The landing values are true, but
the predicate's apparent independence is overstated. The falsifiable content is the per-mutant
`failed_cases`, `case_absent`, `applied` and `exit` fields, which I re-derived. Likewise, the kill
rule's "killed by a case other than its declared one counted in `declared_case_hits`" cannot be
produced by this battery (only by a forged receipt, and forgery `a2` shows `--validate` rejects
that form).

**F7 — the base arm's `exit 1` is over-determined.** The battery's `ok` requires
`target_pin.matched` (`:299-301`), and the pin is the freeze constant `4e4baf…`
(`:42`), so *any* run at base `29d2ca30` exits 1 regardless of survivors (base receipt:
`target_pin.matched false`, `actual 961d5a…`). The claim's base sentence also names the three
survivor ids, so nothing is misleading, but the exit code alone is not survivor evidence; the
`survivor_ids` and the absence of the three declared cases are (verified directly: the base
26-case selftest lacks all three names, and each of the three anchors applies at base with
`applied true`, `inconclusive false`, `exit 0`).

## Positive verifications (no defect found)

- The committed landing receipt is **byte-identical** to a fresh `--battery` run at
  `ed68cd0a` on every field except `measured_at` (`2026-11-04T10:03:14-03:00` committed vs
  `10:07:13-03:00` fresh), including all eight per-mutant objects.
- All eight anchors occur exactly once in the freeze blob *and* exactly once in the base blob,
  and no `replace` equals its `anchor` (no no-op mutant).
- Each of the eight mutated copies prints its own `SELFTEST` summary with 29 cases and 1–2
  failures, so no kill is an import error or a missing-summary artifact.
- The three declared cases are absent at base and present+green at freeze; the base→freeze case
  delta is exactly those three names.
- `--control empty-set` at base reproduces the plan's control line: `mutants_total 0`,
  `survivors 0`, `ok false`, exit 1, `pristine 26/0`; the committed
  `pre/controls/c1-empty-set.json` matches my fresh run field-for-field.
- The target's `--selftest` is a pure in-memory case list (no fixtures, no git, no filesystem
  writes), so a kill is a deterministic function of the mutated blob; my runs could not and did
  not dirty the lane.
- Instrument bytes are identical at declaration `a1f9b81`, at freeze `ed68cd0a`, and in the
  worktree; `git diff --stat a1f9b81 ed68cd0a` touches only `claims.json` (42 insertions), so the
  freeze changed no instrument and added no test.
- The round-29 freeze gate's committed entry for round-79 reads `verdict CLEAN`, `findings []`,
  three instrument paths (read from
  `.ufo/waves/round-79/l1/scores/freeze-audit-at-freeze.json`; not re-executed here).
- Read-only git only; `git status --porcelain` shows pre-existing sibling edits
  (`SCORECARD.md`, `SKILL.md`, `corpus/*`) plus this seat's untracked evidence dir — none of them
  mine. No file outside `.ufo/waves/round-79/w1/ReviewerC1/` was written.

## Residual risk

- **Admission depends on the measurement path, not on `--validate`.** Because of F1–F4, a receipt
  that is internally self-consistent can be admitted while contradicting the pin, the pristine
  count, the sole-detector flags, or the killed/inconclusive separation. Any future round that
  treats `--validate` as the gate would over-admit. Re-running the battery or the digest bind is
  still required; I did both here.
- **One oracle.** The lethal judgment comes from the target's own selftest. My hand-applied
  rerun is a second *executor* but not a second oracle: a case that is sensitive to the mutant but
  asserts the wrong thing would still count as a kill. The mutants are textual by design and the
  claim scopes itself to those eight edits, so this is bounded, but it is not semantic mutation
  coverage.
- **`m05` is a two-token edit** (`False, "defect"` → `True, "bound"`). The kill proves the
  declared case keys on at least one of the two, not which; the claim does not assert more.
- **Base arm precision** (F7): a future base control should pin the base digest rather than the
  freeze digest if the intent is for the exit code to be survivor-derived.

## Verification gaps

- No `lsp` device is mounted in this seat (`xd://` exposes no `lsp` path and the harness tool list
  has none), so caller/definition checks on the Python instrument were done by direct read of
  `tools/round-79/gate-mutation.py` plus execution, not by a semantic index.
- I did not re-execute the round-29 freeze gate; its CLEAN verdict for round-79 is cited from the
  committed audit receipt, not re-derived.
- I did not re-run R79-C2 (`pointer-bind.py`) or any other wave seat's instrument; this review is
  scoped to C1.
- I did not mutate the instrument itself (the mutation seat's surface). My forgeries attack
  receipt shapes only; an instrument mutant plus a matching receipt is outside this evidence.
- Timing: the committed landing receipt was measured 8 s after the freeze commit
  (`10:03:14` vs `10:03:06`). It measures the freeze blob (digest verified), so the ordering is
  coherent, but it is not a pre-commit measurement.

## Artifacts

- `.ufo/waves/round-79/w1/ReviewerC1.md` — this report.
- `.ufo/waves/round-79/w1/ReviewerC1/c1-at-freeze-reviewer.json` — fresh battery, freeze rev.
- `.ufo/waves/round-79/w1/ReviewerC1/c1-at-base-reviewer.json` — fresh battery, base rev.
- `.ufo/waves/round-79/w1/ReviewerC1/c1-control-empty-set-reviewer.json` — fresh empty-set control.
- `.ufo/waves/round-79/w1/ReviewerC1/validate-log.txt` — `--validate` output for the committed
  receipts, my fresh receipts, and all 17 forgeries.
- `.ufo/waves/round-79/w1/ReviewerC1/independent-kills.txt` — anchor multiplicity, hand-applied
  mutants, direct pristine selftests, base-case-absence check.
- `.ufo/waves/round-79/w1/ReviewerC1/forgeries/forge-*.json` — 17 forged receipts.

## Reproduce

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=$(mktemp -d /fast/scratch/hyaku/kaidoku-r79/ReviewerC1/repro.XXXXXX)
TMPDIR=$S python3 -I -B tools/round-79/gate-mutation.py --root . \
  --rev ed68cd0a6cc790cca342380a2d80d1927a668c8c --work "$S/work" \
  --battery --json-out "$S/c1.json"; echo "exit=$?"
python3 -I -B tools/round-79/gate-mutation.py --validate "$S/c1.json"
rm -rf -- "$S"
```
