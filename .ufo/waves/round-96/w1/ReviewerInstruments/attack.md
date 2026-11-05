# ReviewerInstruments attack log — round-96 instruments at lane HEAD 3baac2ef4b9b2830d299125b8184ca06d9e6584d

Scope: surgical correctness review of `tools/round-96/*` (8 files, 1744 lines) at HEAD,
working tree confirmed byte-identical to HEAD for `tools/round-96` (`git diff HEAD --stat
-- tools/round-96` empty). All runs executed in the scratch clone
`/fast/scratch/hyaku/kaidoku-r96/ReviewerInstruments/clone` (git clone --shared of the lane,
HEAD = 3baac2ef). Lane tree never written. Python 3.14.8. No tools installed (none needed).

## Environment / preconditions verified

- A1 Pins vs HEAD bytes: sha256 over all 60 paths in `.ufo/waves/round-96/pins.sha256`
  computed from the clone → 0 mismatches.
- A2 `py_compile` all 8 `tools/round-96/*.py` → 8/8 ok.
- A3 Static mutant-table check: for each of M0-M10, `find` occurs exactly once in its
  target bytes and the replaced file compiles (`compile(...)`) → 11/11 ok.
- A4 Import-closure check for `build_copy` deps `[v3, round-92 battery, round-92
  battery-v2]`: v6 → v3 at module level (`v3` line 77 `_load(R92_BATTERY)`) → b92 →
  battery-v2 (`stop-boundary-repair-battery.py:62 _load(V2)`); R87/R88 loads are lazy
  (inside score, root-relative). Deps = exact transitive module-level closure. Complete.

## Selftests (the item's dynamic requirement)

- A5 `python3 -I -B tools/round-96/stop-boundary-repair-battery-v6.py --selftest --work
  $S/v6-st` → exit 0, `SELFTEST cases=13 failures=0`. All 13 cases assert what their names
  say (checked line by line); the usage case swaps `v3.score = fake` and restores
  `orig_score` in `finally` (v6:328-337).
- A6 `python3 -I -B tools/round-96/kill-rule-v2.py --selftest --work $S/kr-st` → exit 0,
  `SELFTEST cases=4 failures=0` (apply-once, double-find-refused, lying-probe-inconsistent,
  truthful-negative-consistent).
- No other round-96 instrument has a `--selftest` (grep: symlink-probe-v2, probe-writer-legs,
  r95-unbound-at-base, gen-forgery-fixtures, fresh-source2-check have none; legacy-kill-rule's
  "selftest" mentions are calls into the r95 instruments).

## Attacks on the v6 counter

- A7 (hit, HIGH) Tried to find an unbound receipt field beyond the frozen six. Constructed
  receipts with `met_target` absent and `met_target: null` (label/counts/pins/revision/head
  honest) and ran `verify_receipt` from the clone → both return `{'ok': True, 'reasons':
  []}`. The directional checks at v6:170-172 only test `is True` / `is False`, so a receipt
  asserting no met direction at all self-verifies green; `main` then prints `met None exit
  0` (v6:393) and exits 0. This is a seventh M95-g-class unbound field; no frozen fixture
  or mutant covers it. (The six frozen classes still refuse with exactly their intended
  single reason — verified in A10 — so the committed green receipts are unaffected.)
- A8 (no hit) Label arithmetic: recomputed `recompute_label(counts, 6)` against LABEL_RE and
  the met-directional bindings — the `intact` denominator comes from the caller's
  `--intact-total`, not the receipt; no lie available there.
- A9 (no hit, LOW noted) `counts` with `fresh_scored: null` reports
  `counts-missing-key:fresh_scored` (same string as a truly missing key); extra keys outside
  COUNT_KEYS are ignored. Typed refusal preserved both times.
- A10 (no hit) Forgery isolation: for all six committed fixtures verified revision ==
  e4d1f7de…, `head == revision` (except head-mismatch), pins equal pins.sha256 values
  (except the single violated pin in each pin fixture), unlabelled carries 8 of 9 count
  keys. Each violates exactly one binding → the exactly-one-reason requirement is sound.
- A11 (no hit) resolve_rev: `HEAD` → 3baac2ef…, `"HEAD "` → None, `nonexistent-x` → None,
  `HEAD~1` → e4d1f7de…; whitespace rejection at v6:124 fires before the git call; a leading
  `-` rev fails inside git → None (fail-closed).
- A12 (no hit) Receipt field order: `main` records verdict/counter/repair pins and `head`
  (v6:371-378) before `write_receipt` (383) and `verify_receipt` (384-386); fail-closed
  `code = 1` at 387-388. The committed red evidence honest-pos-red-head-not-bound.* is
  consistent with this gate firing on the pre-supersession bytes.
- A13 (no hit) Planted-tmp immunity exercised by the selftest (victim intact, target regular,
  complete JSON); unknown-type raise leaves no temp and no partial target (leftover scan in
  the selftest covers the run dir). Writer fsyncs the file (v6:94) but not the directory —
  contract "Complete JSON or absent" still holds (LOW-3).

## Attacks on kill-rule-v2

- A14 (hit, MED) Looked for the run-time enforcement of the declared table property "every
  replaced file still compiles": `build_copy` (kill-rule-v2:297-318) counts find (306) and
  replaces (310) but never compiles the result. A syntax-breaking replace would be "killed"
  by K-selftest rc≠0 — indistinguishable from a real gate-coverage kill. Current table is
  clean (A3), so the frozen count is not inflated today; the gap is enforcement only.
- A15 (hit, MED) Green-exit-vs-receipt binding for the kill rule itself: `--json-out` is
  optional (kill-rule-v2:494-497), the receipt is written but never re-read, and the printed
  label/met/exit are computed from `met` regardless. A v6-style `receipt-required` gate does
  not exist for the flagship calibration command. Write failure crashes (fail-closed), but a
  successful write is unverified and a missing write still exits 0.
- A16 (no hit) M10 kill mechanism: K-probe's honest leg runs the round-94 writer (v4), whose
  `write_receipt` uses the predictable `path + ".tmp"` + open + os.replace
  (round-94:60-67) — it follows the probe's planted `<target>.tmp` link, so truth is False
  on the honest leg and the hard-coded `verdict: "hardened", met: True` (M10) is
  inconsistent → killed. Consistency predicate at kill-rule-v2:290-291 is exactly the
  iff-form the claims freeze.
- A17 (no hit) c_dmain scenario wiring: per-scenario closure binding via default args, pos
  wants exit 0, shortrev/rewrite/notrecomp want non-zero, nojson wants 2, `v3.score`
  restored in finally (kill-rule-v2:245). Under M3 (forced ok) shortrev exits 0 → killed;
  under M4 (pass) shortrev exits 0 → killed; under M6 shortrev is caught by head-not-bound
  (the recorded head is computed by main, not claimable) → killed. Kill matrix closed for
  M1 (K-selftest planted-tmp), M2 (K-fsync), M5 (K-selftest not-frozen), M7-M9
  (K-agreement F3/F1/pos), M10 (K-probe).
- A18 (no hit) c_agreement_exact legs: forgeries at `--rev R95_WORLD_REV`
  (b5331db1…), honest leg at `--rev R95_INSTRUMENT_REV` (4bda1d1d…) against the committed
  round-95 honest receipt; expected exits 1/0 match the agreement instrument's semantics.
- A19 (no hit) Label arithmetic vs counts dict: 10/10/10/3/1/1 in the label string equals
  the counts dict (kill-rule-v2:479-489) and equals the committed green receipt
  c1-at-decl-worktree.json counts; identity mutant excluded from `killed` and required
  not-killed via `identity_not_killed` in `met`.
- A20 (no hit) c_selftest conventions: counter gets `--selftest --work d` (v6 convention),
  agreement gets `--selftest d` (agreement main:262-265 takes a value) — the supersession's
  convention split is correctly encoded (kill-rule-v2:122-131).

## Attacks on the smaller instruments

- A21 (no hit) symlink-probe-v2: own receipt through the hardened writer (mkstemp + fsync +
  os.replace, cleanup on raise); verdict/met derived from `ok = victim_intact and
  receipt_valid`; records tmp_left/tmp_is_symlink. TimeoutExpired uncaught (LOW-6,
  fail-closed direction preserved).
- A22 (no hit) legacy-kill-rule: faithful formalization of the r95 rule — checks (i)-(iii)
  run the mutated copies directly, (iv) runs the battery against `--root` (lane bytes), which
  reproduces the historical 5-of-10 survivor set exactly as committed in
  pre/c1-legacy-rule-at-base.json. `git init` inside its own scratch copy is the fixture-repo
  pattern the bounds allow. Its own receipt uses plain open() (LOW-7).
- A23 (no hit) r95-unbound-at-base: pins the v5 bytes via `git show` byte-compare; expects
  accepted 5 of 6 + 1 crash + nojson exit 0; matches the committed pre receipt. The nojson
  work dir is hardcoded from HYAKU_SCRATCH and `receipt_written: False` is asserted, not
  measured (LOW-4).
- A24 (no hit) probe-writer-legs: plants the symlink AT the probe's own `--json-out`;
  before leg (r95 probe open("w")) consumes the victim, after leg (v2) swaps the link.
  Docstring line 8 ("writer path that does not exist") contradicts run_leg line 48, which
  passes the existing identity_noop (LOW-5); the next sentence states the real mechanism.
- A25 (no hit) gen-forgery-fixtures: bakes honest pins + one violated field per fixture;
  regeneration at the supersession commit is coherent with the committed bytes (A10).
- A26 (no hit) fresh-source2-check: sha-pin gate (drift → exit 2 before any work), pack
  determinism, public-carrier collision check, intact identity, near/far arms with
  fail-closed denominators (`len(near) == len(DIRECTIONS)`, out-of-range cells excluded
  from both count and denominator pass). Plain-open receipt writer, `--rev` recorded raw
  (LOW-7 family; supplementary tool, not a claim counter).

## Findings index (full detail in the report)

- HIGH-1 v6 verify_receipt admits met_target absent/null (v6:170-172, surfaced at 393).
- MED-1 build_copy never compiles the replaced bytes (kill-rule-v2:297-318).
- MED-2 kill-rule-v2's own green exit is not bound to a verified receipt (494-497).
- LOW-1..8 as itemized in the report.
