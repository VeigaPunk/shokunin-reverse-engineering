# R22-C2 reviewer report — count-c2.py duplicate-name / nonfinite envelope attack

**Seat:** KaidokuR22R.C2Json-6 (reviewer, leaf). **Target:** `.ufo/waves/round-22/tools/count-c2.py`
(baseline 7787fea4d6fd718726de92ed20759d11ce7b8b48; file SHA tag 5EAE as read this session).
**Scope:** duplicate JSON member names and non-finite numbers inside the REA CLI receipt envelope;
adjacent agreement semantics only as needed. No production files touched. Environment:
Python 3.14.8, git 2.56.0, Linux x86_64. Scratch repo only: `/tmp/r22c2-scratch-95whqdvx`
(13 commits, one per case, listed verbatim below). No tool installs; RULES.md read, no install needed.

## Verdict

Duplicate-member and literal `NaN`/`Infinity` handling is **correct** (positive controls below).
Two real acceptance flaws found in the same attack surface; both let the full counter run **exit 0**
on data the counter's own docstring or the frozen claim's "observed matches" contract forbids:

| ID | Severity | Flaw | Exit observed |
|----|----------|------|---------------|
| F1 | high | `strict()` refuses literal `NaN`/`Infinity` but not overflowing number literals (`1e999` → `inf`): nonfinite values enter the envelope and even satisfy `ok-field` claims | 0 (`matched`, 14/14) |
| F2 | medium | `ok-field` agreement uses Python `==`: `true`≡`1`, `1`≡`1.0` conflate distinct JSON types; receipt need not contain the claimed literal | 0 (`matched`, 14/14) |
| F3 | low | one non-UTF8 receipt aborts the whole run as `{"finding":"unevaluable"}` exit 2 ("revision cannot be read") instead of per-verb `receipt_unevaluable` exit 1 | 2 |
| F4 | low | `line.startswith(HEADING)` lets a malformed heading (`### Round-22 catalog dispositions decoy`) shadow the real section; decoy table counted | 0 |

## Mechanism and evidence

`strict()` (lines 46–57) installs `object_pairs_hook` (duplicate members → `ValueError`) and
`parse_constant` (`NaN`/`±Infinity` → `ValueError`). Unit probe (same process, module loaded via
importlib; `-I`-isolation semantics equivalent — no imports differ):

```
strict('{"a":1,"a":2}')                          -> ValueError: duplicate_member: a
strict('{"x":{"a":1,"a":2}}')                    -> ValueError: duplicate_member: a
strict('[{"a":1,"a":2}]')                        -> ValueError: duplicate_member: a
strict('NaN') / 'Infinity' / '-Infinity'/'{"n":NaN}' -> ValueError: nonfinite_number
strict('1e999')                                  -> inf            # BYPASS
strict('-1e999')                                 -> -inf           # BYPASS
strict('{"ok":true,"data":{"n":1e999}}')         -> {'ok': True, 'data': {'n': inf}}
strict('1e-999')                                 -> 0.0            # silent underflow
```

`parse_constant` only fires on the three literal tokens; `1e999` is a *syntactically valid* JSON
number that `float()` overflows to `inf`. Nothing downstream rejects nonfinite values.

### Full-run cases (exact argv, exits)

Each case committed on top of the same 14-verb baseline table (all
`error:capability_unavailable` error envelopes, meta.command == verb). Exact argv per case:
`python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py --root /tmp/r22c2-scratch-95whqdvx --rev <commit>`.

| commit | case | result |
|--------|------|--------|
| 2cc73e3 | clean_all (positive control) | exit 0, accounted_count 14, mismatched [], foreign [] |
| 194d850 | **F1**: receipt `{"ok":true,"data":{"n":1e999},...}` + row `ok-field:n=1e999` | **exit 0**, `inspect-packet-fields` status `matched`, accounted 14/14 |
| 236ca8a | **F1b**: `data.n=1e999` *unclaimed* (row still `error:capability_unavailable`) | **exit 0**, 14/14 — nonfinite payload sails through the decision path |
| 841d57d | **F2**: receipt `data.n=true` + row `ok-field:n=1` | **exit 0**, `matched` — `True == 1` |
| 44fd012 | **F2b**: receipt `data.n=1` + row `ok-field:n=1.0` | **exit 0**, `matched` — `1 == 1.0` |
| 83d5903 | underflow: receipt `data.n=1e-999` + row `ok-field:n=0` | exit 0, `matched` — `1e-999` silences to `0.0` |
| 2a0e7f1 | dup member `"ok":false,"ok":true` | exit 1, status `receipt_unevaluable` (positive) |
| bd89f6f | dup member nested inside `error` object | exit 1, `receipt_unevaluable` (positive) |
| 2bedcb6 | literal `NaN` in `data.n` | exit 1, `receipt_unevaluable` (positive) |
| 9689b75 | `NaN` inside a list `[NaN]` | exit 1, `receipt_unevaluable` (positive) |
| a3c9a46 | `ok-empty:sessions` claimed, value is dict | exit 1, `observed_mismatch` (positive) |
| 3198af7 | **F3**: receipt bytes `... "code":"\xff\xfe" ...` | **exit 2**, stdout `{"finding": "unevaluable", "error": "'utf-8' codec can't decode byte 0xff in position 29: invalid start byte"}`, stderr empty |
| 0577597 | **F4**: `### Round-22 catalog dispositions decoy` + full fake table before real heading (real section body empty) | **exit 0**, 14/14 from the decoy section |

The script's own `--selftest` passes (exit 0, `counter_controls_clean`): all six declared
mutants behave — its `duplicate_json` control only exercises the top-level duplicate, which works.
The flaws above are outside the declared control set.

## Why each is an implementation flaw, not a declared limit

- **F1**: docstring line ~11–13 states receipts decode as "strict JSON (duplicate
  members/non-finite refused)". `1e999` is non-finite in the decoded envelope (it *is*
  `float('inf')`); the policy is stated about the decoded value, and an `ok-field` claim can name
  `1e999` and match — the receipt/row pair then certifies a value JSON cannot represent. The
  declared `limit` field ("receipt/row agreement at one revision") does not cover accepting
  non-JSON values.
- **F2**: claims.json falsifier set and `move` require "observed outcome matches the disposition
  row". `true`≠`1` and `1`≠`1.0` as JSON values; Python `==` treats them equal (also nested:
  `[1]`==`[1.0]`, `{"a":true}`==`{"a":1}`). The row/receipt pair is not in agreement even though
  `matched` is reported. (`error:` uses `==` too but on strings only; `ok` correctly uses `is`
  True/False — the codebase already knows the `is` idiom, just not for field values.)
- **F3**: docstring reserves exit 2 for "the revision itself cannot be read". A present, readable,
  non-UTF8 receipt file is a per-receipt defect; today `git_show`'s `proc.stdout.decode` raises
  UnicodeError, escapes `check()` (not caught there — only `ValueError` around `strict()` is),
  and flattens the run to `unevaluable`/2. Fail-closed, but misleveled: it converts one bad
  receipt into revision-level unavailability and loses all per-verb statuses.
- **F4**: the section contract names the heading exactly; `startswith` admits
  `### Round-22 catalog dispositions<anything>`. Combined with `next()` taking the *first* match,
  a malformed-duplicate heading earlier in PROVINCE.md fully supplies the table while the real
  section is ignored. Low likelihood in a human-edited PROVINCE, but it is precisely a
  coverage-attribution gap a counter exists to deny.

## Narrow fixes (author-side, all local to count-c2.py)

1. **F1** — in `strict()`, add
   `def real(v): r = float(v); ...` → replace `parse_float` with a wrapper raising
   `ValueError("nonfinite_number: "+v)` when `not math.isfinite(float(v))` (import `math`).
   Keeps `1e-999→0.0` if underflow is deemed acceptable; if underflow must also be refused,
   compare `float(v)` to the literal round-trip or bound the exponent instead.
   Alternative one-liner: post-decode walk for `isinstance(x,float) and not math.isfinite(x)`.
   `parse_int` needs no change (`int()` never overflows; absurd digit counts already raise
   ValueError → `receipt_unevaluable`).
2. **F2** — replace `dig(env.get("data"), dotted) == strict(literal)` with a recursive
   `json_equal(a,b)`: `type(a) is type(b)` after collapsing `(int,float)`-but-not-`bool` into one
   numeric class (or keep `int`/`float` separate for strictness), dicts/lists compared
   element-wise. ~10 lines. If int/float unification is intended, that also fixes `1`/`1.0`;
   either way `bool` must be its own class.
3. **F3** — in `check()`, wrap the `git_show` call: `except UnicodeError: return "receipt_unevaluable"`
   (or decode with `errors=` inside git_show and surface a sentinel). Per-verb status, exit 1.
4. **F4** — `line.startswith(HEADING)` → `line.rstrip() == HEADING` (and optionally
   `strip()` the candidate) so only the exact heading opens the section.

## Coverage notes / residual risk

- `parse_constant` covers every position (values in lists, nested objects, top level) — verified
  `NaN` inside a list is refused.
- Duplicate-member check covers every object including inside arrays — verified nested refuse.
- `error:`/`ok-empty:`/`ok-field:` all gate on the same `strict()` decode, so no observed-shape
  bypasses the JSON guards; the bypass is inside `strict()` itself.
- Not exercised (out of attack scope): `receipt` path grammar beyond the `..` segment check,
  `git` failure modes other than nonzero exit, `ok-field` literal grammar edge cases
  (`=` inside the literal is fine — `split("=",1)` — `ok-field:=...` is a grammar nit that
  still fails closed as `observed_mismatch`).
- Scratch repo retained at `/tmp/r22c2-scratch-95whqdvx` for re-run; counter itself was
  executed read-only from the lane path.

Verdict: two genuine acceptance bugs (F1 nonfinite overflow, F2 type-conflating equality),
both demonstrably reachable to exit 0; F3/F4 lower-severity robustness/attribution issues.
Duplicate-name and literal-nonfinite defenses are sound — the holes are the *number* channel,
not the token channel.
