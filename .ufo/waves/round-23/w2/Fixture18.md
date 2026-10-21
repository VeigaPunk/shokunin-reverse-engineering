# Fixture18 — `absolute_citation` case review (R23-C1, candidate 2838351450ff1ee4baa620c962a1153450d53311)

Scope: `frozen/expected-v2.json` case `absolute_citation`, `frozen/fixture.json`, exact branch in
`tools/counter-fixtures.py`. Source review only; suite not executed (not a designated Run* seat).

## Verdict

The case **does distinguish the stated fault** at candidate, with one bounded weakness noted below.
Expected `{exit:1, count:1, finding:c1_incomplete}` is correct. Recommendation: admit; no defect.

## Mechanism (observed)

- `tools/counter-fixtures.py:65-66` mutates the positive entry's only evidence citation:
  `text = text.replace(PREFIX, '/tmp/not-the-lane/'+PREFIX)` where
  `PREFIX = '.ufo/waves/round-23/evidence/c1/'` (`:14`). `PREFIX` occurs exactly once in `text`
  (header at `:47` contains `source:`/`verified-at:`/`recheck:` only), so the mutation is a clean
  single-point change: the verb name and eid stay on the citation line and the envelope blob is
  still written and committed at `repo/.ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json`
  (`:62-63, :93-98`). Positive-preserving confirmed: eligibility (S058 A/mined/2026-10-21/used-by
  at `:84-87`), verb mention, blob existence, and eid all unchanged — only the citation is altered.
- Counter side (`tools/count-c1.py:96` at candidate):
  `cited_pattern = re.compile(r'(?<![/A-Za-z0-9_.-])'+re.escape(ROOTS[1])+r'[A-Za-z0-9._/-]+')`.
  In the mutated line `.ufo` is preceded by `/` (inside `/tmp/not-the-lane/`), which is in the
  lookbehind exclusion class → **zero citation matches** → the `evidence_path` loop never runs →
  `targets['inspect-signal-decoders']['new']` stays empty. Historical binding is
  `identify-flutter-build` only (`:80-83`), so `held=1` → `c1_incomplete`, `t1_exercised_count=1`,
  exit 1 (`main`, `:165-168`). Matches `expected-v2.json` `absolute_citation` exactly.

## Distinguishing power (observed)

A mutant counter without the path-start anchor (plain substring/`find` of the prefix) would extract
`.ufo/waves/...` out of the absolute path, then either (a) `git show` it relative to the rev — the
blob **does exist** at the revision because the fixture still writes it repo-relative →
`bind_new` succeeds (fixture envelope satisfies every `bind_cli` check: `ok:true`, `meta.command`
match, `data.evidence_id`/`operation` present, no refusal node) → count=2/exit0 → **caught**; or
(b) `git show` the literal absolute path → `git_input_unreadable` ValueError → exit2/unevaluable →
**caught**. The `count:1` (not `null`) expectation also distinguishes crash/unevaluable outcomes.
So the case catches both common fault directions for this class.

## Weakness (bounded, non-blocking)

- The rewritten path `/tmp/not-the-lane/.ufo/...` points at a non-existent host location. A counter
  mutant that resolves the citation against the **live filesystem** instead of the git revision
  would find nothing → no binding → count1 → passes. This bug class (out-of-root filesystem read)
  is not falsified. Mitigating factor: the contract forbids writes outside the lane runtime root,
  so no fixture could plant a file at that absolute path anyway; and the primary fault (prefix
  substring accepted inside an absolute path) is still killed because the repo-relative blob exists.

## Independence (observed)

- `counter-fixtures.py` imports stdlib only; it never imports, loads, or reuses counter logic —
  no `r20/r21/r22` helper import, no reuse of `cited_pattern`/`bind_cli` (docstring `:1-4`, imports
  `:5-12`). `PREFIX` is a hand-typed literal duplicate, not derived from `ROOTS[1]`.
- Expected values are hand-stated constants in `frozen/expected-v2.json`, itself SHA-pinned in
  `count-c1.py` (`SELFTEST_MANIFEST_SHA256`, `:25`) and whose `inputs` digests pin both
  `counter-fixtures.py` and `fixture.json`. Verified at candidate:
  - `tools/counter-fixtures.py` sha256 `f2990b35d1…a97f` — matches manifest pin.
  - `frozen/fixture.json` sha256 `a1f5aff8eb…ef4b` — matches manifest pin.
  - `frozen/expected-v2.json` sha256 `458b30d5a6…096f` — matches `SELFTEST_MANIFEST_SHA256`.
  Template is therefore an independent oracle, not decision-derived.

## Consistency notes (observed)

- Exit-1/not-counted treatment for an absolute citation is coherent with `mention_only` (verb
  mentioned, no path → 1). Asymmetry vs `..` traversal citations (explicit `ValueError
  'evidence_path_invalid'` → exit2 at `count-c1.py:103-104`) is a deliberate design choice
  documented at `:100` ("Git fails closed on missing/absolute/traversal citations") — absolute paths
  are silently un-extracted while `..` reaches extraction via regex and raises. Consistent within
  the manifest; no contradiction.
- v1→v2 change for this case is only an addition (`absolute_citation` absent from `expected-v1`);
  no prior stale expectation to reconcile.

## Produced files

- `.ufo/waves/round-23/w2/Fixture18.md` (this report).

## Installs

None (pacman paused; read-only wave).

## Open risks / gaps

- Live-filesystem-resolving mutant uncovered (above); contract prevents a stronger fixture.
- Not executed: expectations are traced through `count-c1.py` control flow at candidate, not
  observed output. RunSelftest seat holds execution.

Report: .ufo/waves/round-23/w2/Fixture18.md
