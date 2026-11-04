# ExecC1Grammar — round-77 wave-1 seat report

Seat: ExecC1Grammar (leaf). Target: `tools/round-77/verdict-bind.py` (R77-C1
calibration instrument) — attack its annotation grammar with constructions a
token-presence predicate would accept, and show the parser/binder rejects each.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (no lane file edited;
  the instrument was imported in-process from a scratch copy).
- Instrument sha256 (worktree, matches the frozen pin in
  `.ufo/waves/round-77/claims.json`): `45280392ff6c59e4c96041544720f055952a11a088769e24cb04207db932a9e7`.
- Seat receipt: `.ufo/waves/round-77/w1/ExecC1Grammar/ExecC1Grammar.receipt.json`
  (fixtures + selftest + freeze_run + base_run).
- Counter receipts: `c1-at-freeze-6767a879.json`, `c1-at-base-188562d4.json`;
  `selftest.json`; both counter receipts pass `--validate` (exit 0).

## Verdict

20/20 attack fixtures reject: every false annotation is either bound and
defected (`value_mismatch`), explicitly unbound (`unknown_field`), out of the
declared scope floor, or reduced to "no claim" by the closed grammar. **No
fixture passed when it should not** — no blocking defect observed. The
selftest is green (15 cases, 0 failures). The freeze counter run reproduces
the frozen before-state exactly.

## Fixture results (id — token-presence predicate → this grammar)

1. `a-negation-with-false-claim` — cell
   `` `.ufo/x.json` (no defects, mismatch_count 0) `` vs a defective receipt.
   Token predicate sees `no defects` + `mismatch_count 0` and accepts.
   Grammar: `mismatch_count 0` binds (FIELD_RE) and defects
   (value_mismatch, claimed 0 actual 1); `no defects` matches no clause and
   is dropped from the parsed set — the negation escapes only as prose and
   the explicit false claim is caught. PASS.
2. `a2-negation-fused` — `(no mismatch_count 0)`. Token predicate accepts on
   the substring. Grammar: not `<field> <true|false|int>`, group scores as
   prose, makes no claim, never a pass. PASS.
3. `b-outside-group` — `` `.ufo/x.json` mismatch_count 0 `` (no parentheses).
   Token predicate accepts. Grammar: GROUP_RE finds no group; the cell binds
   nothing. PASS.
4. `b2-outside-group-hybrid` — `(D24 true) mismatch_count 0`. Grammar binds
   only the group (D24 true → value_mismatch on the defective receipt); the
   trailing clause is invisible. PASS.
5. `c-second-group-other-path` —
   `` `.ufo/good.json` (D24 true); also `.ufo/bad.json` (mismatch_count 0) ``.
   Token predicate keyed on the first path scores both clauses against
   good.json and accepts. Grammar: each group binds to the path immediately
   preceding it — group 2 binds bad.json, `mismatch_count 0` vs actual 1 →
   value_mismatch. PASS.
6. `d-contradictory-twins` — `(D24 true, D24 false)` vs a receipt with D24
   ok true. Token predicate accepts on the matching twin. Grammar: every
   bound clause must hold — the false twin defects (claimed False actual
   True). PASS.
7. `e-nested-parens-escaped-remainder` — `((D24 true), mismatch_count 0)` vs
   a receipt with mismatch_count 1. Token predicate accepts on both tokens.
   Grammar: GROUP_RE cannot nest; only `(D24 true)` is a group and binds ok;
   `mismatch_count 0` sits outside every group, makes no claim, and is not
   accepted as a verdict (bound clauses: 1, none on mismatch_count). PASS —
   rejected by reduction, not silently passed.
8. `e2-nested-parens-fully-wrapped` — `((mismatch_count 0))`. Grammar: the
   inner group still binds against .ufo/x.json and defects (0 vs 1) —
   nesting does not hide the clause. PASS.
9. `f-bare-path-after-backtick` —
   `` `.ufo/x.json` see .ufo/y.json (mismatch_count 0) `` (x defective, y
   clean). A path-token predicate can grab the flattering bare `.ufo/y.json`
   and accept. Grammar: `nearest_path` prefers backticked paths before the
   group → binds the defective `.ufo/x.json` → value_mismatch. PASS.
10. `f2-bare-path-before-backtick` — bare flattering path first, backticked
    defective path second: the backticked path still wins, order does not
    matter → value_mismatch. PASS.
11. `g-province-continuation-group-second-line` — PROVINCE bullet with the
    group on line 2 (`- **Core — row one** `.ufo/x.json`\n  (D24 true,
    mismatch_count 0)`). A first-line-only scanner sees pointer-only and
    accepts. Grammar: `province_bullets` appends continuation lines, both
    clauses bind to `.ufo/x.json` → two value_mismatch defects. PASS.
12. `g2-province-path-after-group` — group on line 2, path on line 3.
    Grammar: `nearest_path` falls back to the first path after the group →
    binds `.ufo/x.json` → D24 value_mismatch. Putting the path below the
    group does not escape. PASS.
13. `g3-province-bare-clause-continuation` — bare `mismatch_count 0` on the
    continuation line, no parentheses. Token predicate accepts on the line's
    tokens. Grammar: no group → no claim → not accepted. PASS.
14. `h-scope-floor-round-72` — fixture git repo (scratch) whose SCORECARD
    carries the false cell `` `.ufo/x.json` (mismatch_count 0) `` in a
    first-working-round **72** row plus a clean round-73 row. A token
    predicate without a scope floor scores it and accepts. Grammar:
    `capability_rows` finds the row but `audit()` filters to first_round >=
    73; the false annotation is never scored (capability_rows 2,
    in_scope_rows 1, mismatch_count 0). PASS.
15. `h2-same-cell-in-scope` — the identical cell in a round-73 row binds and
    defects (value_mismatch). The round-72 row avoided a defect only via the
    declared scope floor (SCOPE_MIN_ROUND=73, part of the frozen predicate),
    not because the grammar was fooled. PASS.
16. `i-unknown-field-survivor-1` — `(survivor 1)` vs a receipt with no
    `survivor` field. Token predicate accepts on the tokens. Grammar:
    SURVIVOR_RE needs `<N> survivors`; `survivor 1` falls through to
    FIELD_RE as field `survivor` = 1, the field is absent → unbound
    (`unknown_field`), never a guessed pass. PASS.
17. `i2-legitimate-look-alike` — `(0 survivors)` vs survivor_count 0 binds
    and passes. PASS.
18. `j-typed-true-vs-int-1` — `(mismatch_count true)` vs the integer 1. A
    coercing predicate equates true with 1. Grammar: literal True vs int 1,
    `typed_equal` is type-strict (bool is not int) → bound and defect
    value_mismatch (claimed True, actual 1). PASS.
19. `j2-legitimate-look-alikes` — `mismatch_count 1` vs int 1 and
    `mismatch_count true` vs bool true both bind clean. Typed equality is
    symmetric, not a blanket boolean refusal. PASS.
20. `r76-real-false-annotation-at-base` — the actual round-76 false
    annotation `` `.ufo/waves/round-76/l1/scores/c1-at-landing.json`
    (D24 true, mismatch_count 0) `` scored against the real receipt at base
    188562d4 (exit 1, mismatch_count 1, D24_capability_rows ok false — the
    exact routed defect 5). Token presence admitted it in round 76; this
    grammar re-derives both clauses from the named receipt → two
    value_mismatch defects. PASS.

Full inputs, synthetic receipt shapes, per-clause bindings (clause/status/
path/field/claimed/actual) and pass booleans: see the seat receipt JSON.

## Selftest (spec point 3)

`python3 -I -B tools/round-77/verdict-bind.py --selftest` → exit 0,
`cases: 15`, `failures: []` (copied verbatim to `selftest.json` in this
directory).

## Freeze counter run (spec point 4)

`python3 -I -B tools/round-77/verdict-bind.py --root <lane> --rev 6767a879c6a3f386a9c3fc9d332c794f2d9ea914 --json-out c1-at-freeze-6767a879.json`

- `mismatch_count`: **4**
- `population.bound_clauses`: **21**
- `population.in_scope_rows`: **9** (capability_rows 39, groups 18,
  unbound_clauses 3)
- `validate.defects`: **[]** (`--validate` exit 0)
- defect labels (exactly the frozen before-state):
  - `## Capabilities row 'capability-row binding' (first-working round 76)`,
    group `(D24 true, mismatch_count 0)`, path
    `.ufo/waves/round-76/l1/scores/c1-at-landing.json`: `D24` true vs
    false; `mismatch_count` 0 vs 1 (both value_mismatch).
  - `PROVINCE.md line 585`, same group/path: `D24` true vs false;
    `mismatch_count` 0 vs 1 (both value_mismatch).
- The three unbound clauses (never passes): `forged_detected true` (row
  'kernel-side environment witness bound by ancestry'), `sole true` (row
  'A12 case-independence closure'), `mismatch 1` (PROVINCE.md line 585) —
  each `unknown_field` against its named receipt.
- exit 1 (the freeze predates the landing repairs; identical numbers at base
  188562d4 — see `c1-at-base-188562d4.json`, the frozen before-state).

## Risks / notes

- Fixtures a2/b/e/g3 reject by "makes no claim" (closed grammar: a clause
  outside a parenthesised group is prose and binds nothing) rather than by a
  defect. That is the instrument's documented semantics and is not a pass;
  the landing predicate additionally floors `bound_clauses >= 18` so a
  record cannot reach green on prose alone.
- `nearest_path` prefers backticked paths and ignores bare ones whenever a
  backticked path exists in the cell (fixtures f/f2) — a deliberate,
  declared choice; a bare path alone (no backticks anywhere) would still
  resolve via JSON_ONLY_RE.
- Scope floor is load-bearing (fixture h): a false annotation in a
  first-working-round < 73 row is never scored; the predicate's surface
  definition makes this exclusion explicit, and in_scope_rows >= 11 guards
  the landing against scope-shrinking.
- No environment dumps anywhere; all probes run under the instrument's own
  code paths with synthetic receipts in scratch.
