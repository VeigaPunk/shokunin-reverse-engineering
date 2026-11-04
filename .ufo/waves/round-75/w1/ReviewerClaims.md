# ReviewerClaims — adversarial review of R75-C1 (round 75, wave r75-w1)

Reviewer: ReviewerClaims-3. Reviewed the frozen predicate (plans/round-75-claims.md,
.ufo/waves/round-75/claims.json) as a CLAIM, against the committed evidence. No lane files
edited. Lane worktree moved during review (HEAD `bfdf03dd` at start → `13d1498f` at end,
wave landing in flight); every derivation below is pinned to frozen revs. No LSP device is
mounted in this session; ground truth is `git show` + direct execution of the frozen blobs.

Verdict per assignment item; **no BLOCKING defect**. One non-blocking provenance finding (F1).

## Item 1 — sha re-derivation: AGREE

- `git show 8dff07b9:tools/round-75/seam-probe.py | sha256sum`
  → `1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d`. Identical at freeze
  `ec149dc4`, at tip `bfdf03dd`, in the worktree at review start, and equal to the
  claims.json `instruments` pin. The pin the battery was told to expect
  (c1-post-at-declaration.json `target_pin.expect`) is the same digest, and the receipt's
  `target_sha256` matches — the blob hashed, pinned, and scored is one blob.
- `git show 3c15a156:tools/round-74/seam-probe.py | sha256sum`
  → `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039` = claims.json
  `loaded_by_counter` pin = c1-base-arm.json `target_sha256`.
- The battery itself at the declaration hashes `ec089411…` (= claims.json pin). **But the
  worktree copy changed mid-review** to `d7757ae2…` (post-freeze commits `ad53c1e1`,
  `8d9ab100` — see F1).

## Item 2 — do-nothing paths to survivor_count 0: AGREE (none found)

Read of the frozen battery (`tools/round-75/probe-mutation.py` @ `8dff07b9`, ec089411):

- **Stale anchors**: `apply_patch` raises `Unevaluable` unless the anchor occurs exactly once
  → exit 2, and `--json-out` is written only on the scoring path → no receipt, no exit 0.
- **Crash/timeout-as-kill**: `run_detector` returns rc None/nonzero with empty `failed`;
  `classify` then yields `killed_wrong_case`, and `ok` requires `killed_wrong_case == []` →
  exit 1. A lying-or-broken harness cannot manufacture kills.
- **Pristine count lowered**: floor = patch-set default (25 / 20) because the frozen commands
  pass no `--min-pristine-cases`; `pristine_ok` requires `rc 0 ∧ failed [] ∧ cases ≥ floor` →
  exit 1 otherwise. Frozen receipts show 25 / 20.
- **Vacuous sole**: `sole = verdict=="killed" ∧ failed == [expect_case]` exactly; with
  `failed == []` the verdict is `killed_wrong_case`/`survived` and sole is False. Cannot be
  true vacuously.
- **Pin**: `check_pin` runs on the `git show rev:tool` blob BEFORE `score_text` writes or
  executes any copy; mismatch → exit 2, nothing executed. The scored text IS the hashed text
  (no TOCTOU). Note: `pinned_before_exec` is a constant `True` in the receipt — honest for
  this version, decorative as a field (see risks).
- **Renamed-cases do-nothing**: closed by the committed control arm `c1_no_declared_cases`
  (controls-at-declaration.json): renaming the closed case names yields `killed_wrong_case`
  for all seven and no kill — red selftest alone does not satisfy the claim.
- Residual (minor): the exit code never asserts the mutant-set size (15); a battery with
  fewer mutants could still exit 0. Closed for the frozen state because the battery content
  is sha-pinned in claims.json; would be a gap for future rounds.

## Item 3 — base-arm attack + patch-site uniqueness: AGREE

Programmatic count of every anchor against its target blob (29 classes total):

- r75probe (15 classes on the r75 blob): every `sites == 1`; no no-op replacement
  (replacement ≠ anchor for all). Two classes leave the anchor as a benign substring of the
  replacement (`b-first-sample-only` `[:1]` suffix, `c-skip-forged-subrun` early-return
  prefix) — residue, not ambiguity; `apply_patch` would exit 2 on any count ≠ 1 anyway.
- r75base (14 classes on the r74 blob, incl. the `a-any-forged-sample` anchor swap
  `forged_kernel.values()`): every `sites == 1`.

False survivors would require the mutated selftest to exit 0 while its own case fails; the
harness tail (`return 0 if all(cases.values()) else 1`) is not touched by any class in the
set, and the pristine harness is verified green at 20 cases. The four named survivors are
genuinely unbound at base: the r74 blob compares `home_under`/`tmpdir_under` with `is True`
against boolean fixtures (a `bool()` twin is invisible), keeps one sample per name by
construction, and `lie_clean` uses exact key-list equality that a superset passes; the
`a12-genuine-field-identity` case does not exist there. The converse (false killed) requires
rc ≠ 0 with the declared case in `failed` — genuine detection. The base cross-binding is
confirmed in the r74 source: its `a12-kernel-multiple-samples` conjunct
`any(s.get("canary_present") for s in samples)` makes `b-drop-canary-field` fail BOTH cases →
not sole (receipt: failed `[a12-kernel-multiple-samples, a12-kernel-canary-field]`). ✓

## Item 4 — semantic claim: AGREE, with one wording note

- Instrument meaning: `sole_detector[m]` = (m killed) ∧ (m.failed == [m.expect_case]) — the
  *mutant* direction ("this kill is attributable solely to the declared case"). The frozen
  predicate sentence states exactly this
  (`sole_detector["b-drop-canary-field"] true with failed == ["a12-kernel-canary-field"]`),
  so instrument and predicate agree. Wording note: the prose "SOLE detector of
  a12-kernel-canary-field" is the *case* direction (no other mutant detects that case); the
  battery does not compute it, but the receipt rows do, and I verified it: the only mutant
  whose failed list contains `a12-kernel-canary-field` is `b-drop-canary-field`, in both the
  committed receipt and my frozen re-run. Every other case's detector set is multiple only
  where the claim never asserts solehood (`a12-genuine-field-identity` ← both truthy twins;
  `a12-sample-name-merge` ← both merge directions; `a12-kernel-cases`,
  `a12-lie-clean-keys-exact` by design).
- Independence at source (r75 blob, lines ~1378-1393): `a12-kernel-multiple-samples` asserts
  only `len(samples) == 2`, pids `{10,11}`, basename set `{"git"}` — it never reads
  `canary_present` (the r74 conjunct was removed). The r74 blob's same case carries
  `and any(s.get("canary_present") for s in samples)` — the cross-binding the round removes.
  `b-first-sample-only` (`return list(seen.values())[:1]`) fails multiple-samples via
  `len == 2` and cannot touch `a12-sample-name-merge`, which feeds `_name_samples` a literal
  two-sample list. Dropping the witness key (line ~520) leaves len/pids/basename unchanged →
  multiple-samples green; only the isinstance-bool case fails. Semantics verified, matches
  the receipts.

## Item 5 — frozen commands re-run: AGREE

Run with the true frozen battery (extracted `git show 8dff07b9:tools/round-75/probe-mutation.py`
→ sha `ec089411…`, executed from scratch, `--root` = lane):

- Probe arm: `… --rev 8dff07b9… --tool tools/round-75/seam-probe.py --patch-set r75probe
  --expect-survivors 0 --expect-target-sha256 1fc1c8fc… --expect-sole b-drop-canary-field`
  → **exit 0**, `survivor_count 0`, `killed_wrong_case []`, pristine `{25, [], rc 0}`,
  pin matched, `sole_detector["b-drop-canary-field"]=True` with
  `failed == ["a12-kernel-canary-field"]`. Identical counts to
  c1-post-at-declaration.json on every field compared.
- Base arm: `… --rev 3c15a156… --tool tools/round-74/seam-probe.py --patch-set r75base
  --expect-survivors 4 --expect-survivor-names d-home-under-truthy,d-tmpdir-under-truthy,
  d-name-samples-last-wins,d-lie-clean-superset` → **exit 0**, exactly those four survivors,
  `b-drop-canary-field` not sole (failed both cases), pristine 20 green. Identical counts to
  c1-base-arm.json.
- `probe-mutation.py --validate` on both committed receipts: `defects []` (exit 0).
- My receipts: `.ufo/waves/round-75/w1/ReviewerClaims-3/{c1-post-frozen,c1-base-frozen,
  c1-post-verify,c1-base-verify}.json` (+ two selftest outputs; probe selftest 25/25, battery
  selftest 9/9).

## F1 — non-blocking provenance finding: the committed base receipt was not produced by the pinned battery

c1-base-arm.json (frozen at `ec149dc4`) records `runner.sha256 = d7757ae2…`. The frozen
battery (ec089411) computes the runner as `git show <rev>:tools/round-75/probe-mutation.py`;
at rev `3c15a156` that path does not exist (`git show` fails) → the frozen battery would
record `null`, not d7757ae2. So the committed base receipt was produced by a battery variant
whose content is d7757ae2 — the runner-binding change later committed as `ad53c1e1`
("round-75: the base receipt binds the runner that executed, not a revision that lacks it",
citing round-74 routed defect 5). `diff` of ec089411 vs d7757ae2 is a single hunk confined to
the runner-binding block; scoring logic (patch sets, classify, sole, pin order) is
byte-identical, and my independent run of the FROZEN blob reproduces every count of the
committed receipt. Consequence: the claims.json instrument pin (ec089411) does not describe
the exact bytes that produced c1-base-arm.json; the receipt's runner field is honest about
what executed. Claim unaffected (item 5), but the freeze's "pre receipts committed at the
freeze" story carries this one version skew. No action required for R75-C1; worth a line in
the record.

## BLOCKING defects

None. R75-C1's frozen predicate is verified end-to-end by independent re-derivation.

## Residual risks

- Mutant-set size (15/14) is pinned only via the battery content sha, not asserted by the
  exit code or `--validate`.
- `pinned_before_exec` is a constant in this battery version; it reflects verified code
  order, but the field itself cannot fail.
- The worktree moved during review (instruments `ec089411` → `d7757ae2`, HEAD
  `bfdf03dd` → `13d1498f`); conclusions rest only on frozen revs and scratch-extracted blobs.
- F1 above (base-receipt runner version skew) — cosmetic provenance, scoring-equivalent.
