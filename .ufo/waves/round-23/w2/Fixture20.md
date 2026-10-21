# Fixture20 — R23-C1 `inherited_lost` case source review (godspeed)

Scope: frozen `expected-v2.json` case `inherited_lost`, `frozen/fixture.json`, the exact
`tools/counter-fixtures.py` branch, against candidate commit
`2838351450ff1ee4baa620c962a1153450d53311` (B=`aa1450b82f9ede35aada63efe8a34e01c6e02f72`).
All candidate bytes read via `git show <rev>:PATH`. Suite NOT executed (leaf, non-Run seat).

## Verdict

**Case is sound: it distinguishes the stated fault at candidate source.** No wrong
expectation found; no weak mutation in the kill-the-mutant sense. Findings below.

## Fault model and mechanism

- Mutation (counter-fixtures.py:95-96, branch `if name == 'inherited_lost'`):
  `(repo/'.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json').unlink()` — after
  `reset --hard`/`clean -fd` (lines 35-36), so the deletion lands in the per-case commit;
  staged by `git add -- ... '.ufo/waves/round-22/evidence/c1'` (line 100-102), which stages
  removals. Clone is disposable under the lane runtime and removed by TemporaryDirectory.
- Stated fault ("inherited identify lost", claims.json falsifier list line 34): a counter
  that still credits the inherited `identify-flutter-build` witness after the candidate
  erased it. Candidate counter guards this at count-c1.py:66-68: old-root tree equality
  `git rev-parse rev:round-22/evidence/c1` vs `BASELINE:` → `ValueError('historical_evidence_changed')`
  → main() line 168 → `{'finding':'unevaluable'}`, exit 2, no `t1_exercised_count` key.
- Expected template (expected-v2.json:103-107): `{"exit": 2, "count": null, "finding": "unevaluable"}`.
  Observed-shaping in fixtures run(): lines 106-114 read `out.get('t1_exercised_count')` →
  `None` on the error path; all three fields match. Consistent.

## Mutation specificity (deleted file is a real witness, not dead weight)

- OBSERVED baseline bytes (`git show aa1450b8:.../identify-godot.envelope.json`):
  top-level `ok:true`, `meta.command == "identify-flutter-build"`, `data.operation ==
  "identify_flutter_build"`, has `data.evidence_id`, `normalized_result.flutter_detected: false`.
- r21.refused (round-21/tools/verb-coverage.py:39-55, sha256
  `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b` — matches R22 counter
  pin HELPER_SHA256, verified at B) checks only error/errors/code/status/completion_status/
  exit_code fields; `flutter_detected:false` is not a refusal. So the envelope binds at
  baseline: deleting it is precisely "the inherited identify witness is lost".
- Distinguishing power: a counter lacking the tree guard measures historical at BASELINE
  (count-c1.py:81) where the envelope still exists → identify held, plus new synthetic
  `inspect-signal-decoders` → observed {exit 1, count 2, c1_incomplete} ≠ expected → killed.
  Even the stronger mutant (no guard AND re-measuring historical at candidate rev) dies:
  the sibling `identify-flutter-build-saber.envelope.json` still binds, and if it did not,
  count-c1.py:83 `historical_baseline_changed` still forces exit 2.

## Positive-preserving / independence checks

- Positive preservation: the case writes a valid new witness (envelope + ENTRY + S058 row,
  used-by ENTRY) before the R22 unlink; the tree check fires before any counting in
  `measure()` (line 67 precedes the knowledge scan), so expected {2,null,unevaluable} is
  unaffected by new-evidence counting. Positive counting itself is covered by the `positive`
  case; suite-level isolation is adequate.
- Independent template: expected-v2.json is hash-pinned inside the counter
  (SELFTEST_MANIFEST_SHA256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`
  == actual sha256, OBSERVED at candidate and working copy); its `inputs` digests match
  actual bytes of counter-fixtures.py (`f2990b35…`) and fixture.json (`a1f5aff8…`) at
  candidate and on disk. counter-fixtures.py imports only stdlib (lines 7-13) — no
  validator/decision import; expected values are frozen literals consistent with the
  published exit taxonomy (count-c1.py docstring: "0=clean6/6;1=failed/incomplete;
  2=could-not-evaluate"), not observed runs.
- Frozen-variant history: expected.json/expected-v1.json (14 cases each) lack
  `inherited_lost` and `historical_root_injection` entirely; v2 (21 cases) adds both.
  Stale W1/v1-era findings of "no inherited-loss coverage" are obsolete at candidate.
- Git semantics dependency OBSERVED: `git rev-parse <rev>:<dir>` returns the tree OID;
  candidate and baseline old-root trees are both `b83fc459dca64a8356480b1ebc8309b4de65de71`
  (candidate preserves inheritance), so any deletion/addition/content change flips it.
  CATALOG path exists at baseline (cat-file -e OK), so fixtures `git add` pathspecs all resolve.

## Minor findings (no action required)

1. Attribution breadth (by design): the guard is root-level, so deleting ANY file under
   round-22/evidence/c1 yields identical observables; the template does not pin the error
   string (`historical_evidence_changed` lands in `result['error']`, unchecked). Which guard
   fired is unverified by this case. Acceptable: an indiscriminate always-unevaluable mutant
   is killed by positive/all_six, and `historical_root_injection` + `inherited_lost`
   jointly pin bidirectional root integrity (deletion and addition directions).
2. Same-error collapse: `inherited_lost`, `historical_root_injection`, `old_source`,
   `helper_tamper`, `invalid_utf8`, `catalog_changed` all share observables
   {2,null,unevaluable}; the case set, not the single case, discriminates fault classes.
   In-scope conclusion: `inherited_lost` itself is neither wrong nor weak.
3. Execution unobserved: this review is static + observed hashes/tree-IDs; the one-shot
   suite run belongs to the designated Run seat.

## Produced files

- `.ufo/waves/round-23/w2/Fixture20.md` — this report
  (sha256 recorded by lane tooling; `sha256sum .ufo/waves/round-23/w2/Fixture20.md` to confirm).

## Installs

None.

## Open risks

- `r21.refused` semantics verified at baseline-pinned helper bytes; if a future wave re-pins
  round-21 helpers with changed refusal semantics, "witness" status of the godot envelope
  could change — the case outcome would not (tree guard precedes binding).
- Tree-equality inheritance holds only while `--shared` clones see baseline objects; fixture
  already relies on lane history containing B (it does at candidate).
