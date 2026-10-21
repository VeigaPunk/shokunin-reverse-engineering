# R22-C2 reviewer report — count-c2.py ok-field bool/int equality & error-path type coercion

**Seat:** KaidokuR22R.C2Types-6 (reviewer, leaf). **Target:** `.ufo/waves/round-22/tools/count-c2.py`
(file SHA tag 5EAE as read this session; claims frozen in `.ufo/waves/round-22/claims.json`,
baseline 7787fea4d6fd718726de92ed20759d11ce7b8b48). Working tree vs HEAD of the target file
differs only in docstring wording and one unused `import re` — **logic is identical**; findings
apply to both. **Scope:** bool/int equality and error-type coercion on the `observed` agreement
path; adjacent grammar/robustness only as reached. No production files touched. No tool installs
(RULES.md consulted; nothing needed). Environment: Python 3.14.8, git 2.56.0, Linux x86_64.

## Axes (godspeed)

- **coverage** — number of distinct type-coercion / error-path behaviors of the agreement code exercised with observed exits.
- **calibration** — precision of the defect/limit split: no declared limit claimed as flaw, no flaw downplayed to limit, every exit a real observation.

Frontier walk kept: bool/number conflation (dict+list nesting), non-finite overflow match, empty-code/empty-path grammar acceptance, non-UTF8 receipt misleveling, exact-duplicate heading. Dropped: probe-column aliasing (already controlled by the fixture set), path-traversal `..` (controlled), duplicate-member/literal-`Infinity` (controlled, corroborated below).

## Method

Private scratch repos in `/tmp` (no lane writes): `/tmp/r22c2-repo-oj8g3vmy` and `/tmp/r22c2-repo2-*`, one commit per case on a 14-verb baseline table (all rows `error:capability_unavailable` with matching envelopes, `meta.command == verb`; mirrors the frozen fixture baseline). Per-case argv, identical for every row below:

```
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py --root <scratch repo> --rev <case commit>
```

Observed summary lines are reproduced verbatim under each finding. Harness source retained at end.

## Findings

### F1 — HIGH: `ok-field` agreement uses Python `==`; JSON `true/false` match integer `1/0` (recursively through lists and dicts)

`check()` line 120: `dig(env.get("data"), dotted) == strict(literal)`. Python `==` on JSON-decoded values conflates bool and number: `True == 1`, `False == 0`, `True == 1.0`, `False == 0.0`, and this survives containers: `[1] == [True]`, `{"a": 0} == {"a": False}`. The receipt therefore never has to contain the claimed literal.

Observed (v0 = `inspect-packet-fields` in every case; all others unchanged and matched):

| case | row `observed` | receipt `data.<path>` | result |
|---|---|---|---|
| 01 positive control | `error:capability_unavailable` | — | `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}` |
| 02 | `ok-field:transport=0` | `false` (bool) | `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}` |
| 03 | `ok-field:enabled=true` | `1` (int) | `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}` |
| 04 | `ok-field:items=[1,false]` | `[true, 0]` | `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}` |
| 05 | `ok-field:m={"a":false}` | `{"a": 0}` | `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}` |
| 10 control (exact bool) | `ok-field:flag=false` | `false` | `{"exit": 0, ... "v0": "matched"}` |

Case 02 alone: a row claiming the receipt says `transport` is `0` is accepted when the receipt actually says `false`. That is exactly claims.json's falsifier shape — "a row whose receipt ... differs from its observed value is accepted" — realized on the ok-field branch. **Implementation flaw**, not a declared limit: the `limit` field declares only "receipt/row agreement at one revision; not provider availability over time" and cannot authorize type coercion; the docstring says the literal must be *equal*, and JSON `false` ≠ `0`. Note the codebase already knows the strict idiom: `ok` is checked with `is False`/`is True`, which correctly rejects `"ok": 0` (case 08: exit 1, `observed_mismatch`) — the strictness simply was not carried to field values.

### F2 — MEDIUM: non-finite `inf` enters via overflow literals and satisfies `ok-field`, despite "non-finite refused"

`strict()` refuses the literal tokens `NaN`/`Infinity` via `parse_constant`, but `1e999`/`2e999` are syntactically valid JSON numbers that `float()` overflows to `inf`; nothing downstream rejects them. `float('inf') == float('inf')` is True, so a receipt value and a claimed literal that both overflow compare equal — and both are non-finite values the docstring promises to refuse.

Observed:

- Case 06 — row `ok-field:r=1e999`, receipt `data.r = 2e999` (distinct magnitudes by a factor of 2, both decoding to the same `inf`): `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}`.
- Case H control — row `ok-field:r=Infinity` (literal token) vs receipt `1e999`: exit 1, `observed_mismatch` — the refusal is asymmetric, token-only.

Convergent with sibling seat KaidokuR22R.C2Json-6 finding F1 (their commit 194d850); independently reproduced here with a distinct pair (`2e999` vs `1e999`). **Implementation flaw**: docstring line "duplicate members/non-finite refused" is violated by the decoded value.

### F3 — LOW: degenerate grammar values are accepted as matches

Two grammar slots accept empty/degenerate content and then agree with equally degenerate receipts:

- **F3a** — `observed: "error:"` (empty code). The `error:` branch takes `observed[len("error:"):] == ""` and matches a receipt `{"ok":false,"error":{"code":""},...}` — an error envelope whose error code is the empty string. Case 09: `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}`.
- **F3b** — `ok-field:=5` (empty dotted path). `"".split(".") == [""]`, so the "path" is the single key `""`; a receipt `{"ok":true,"data":{"":5},...}` matches. Case 11: `{"exit": 0, "accounted": 14, "mismatched": [], "v0": "matched"}`.

Both are fail-closed against honest data but admit nonsense pairs a calibration counter should bounce as `bad_observed_grammar`. **Implementation flaw** (the docstring's grammars — `error:<code>`, `data.<dotted.path>` — imply non-empty code and path).

### F4 — LOW: one non-UTF8 receipt flattens the whole run to exit 2 "revision cannot be read"

`git_show` decodes with `proc.stdout.decode("utf-8")`; `UnicodeError` is caught only in `main()` (with `OSError`/`ValueError`), so one byte-broken receipt aborts the audit: per-verb statuses for the other 13 clean verbs are lost and the finding is misleveled to revision-level unavailability.

Case A — receipt bytes `\xff\xfe{}` for v0: `{"exit": 2, "accounted": null, "mismatched": null, "v0": null, "finding": "unevaluable", "error": "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"}`.

Convergent with C2Json-6 F3 (their receipt embedded an invalid byte inside a JSON envelope; mine is a raw non-UTF-8 blob — same `decode` site). Fail-closed, so low; but the docstring reserves exit 2 for "the revision itself cannot be read".

### F5 — LOW: only the *first* `### Round-22 catalog dispositions` heading is read; exact-duplicate later sections are ignored

`section_rows` uses `next(i for ...)` over `line.startswith(HEADING)` — first match wins, and `startswith` admits suffixes. C2Json-6's F4 covers the *malformed-suffix* variant (decoy heading shadowing the real section). Distinct variant here: the heading repeated **verbatim**, first occurrence empty, real table in the second:

- Case D (first section empty, second has the full correct table): `{"exit": 1, "accounted": 0, "mismatched": [], "v0": "unaccounted"}` — fail-closed here.
- Case C (first section carries a stale row contradicting its receipt, second the correct table): exit 1 with v0 `observed_mismatch` from the stale section — the second section is never consulted either way.

Mostly fail-closed (the dangerous direction would need the *first* section to match while the integrator's real section is ignored), hence low; recorded for completeness of the heading-parsing contract.

### F6 — INSIGNIFICANT: `receipt_outside_prefix` status is also produced for in-prefix non-file receipts

Pointing the receipt cell at the directory `.ufo/waves/round-22/evidence/c2` (present at REV): `git show` emits a tree listing, `strict()` fails, and the row is reported `receipt_outside_prefix` (case J: exit 1, v0 `receipt_outside_prefix`) — a *presence/class* problem labeled as a *path-scope* problem. Correctly rejected; status taxonomy nit only.

## Error-path type safety — VERIFIED CLEAN (the "error coercion" half of the seat)

Adversarial probes aimed at coercing the `error:` branch all reject correctly:

| case | row | receipt | observed |
|---|---|---|---|
| 07 | `error:0` | `"code": 0` (int) | exit 1, `observed_mismatch` |
| 08 | `error:x` | `"ok": 0` (numeric, not `false`) | exit 1, `observed_mismatch` |
| F | `error:x` | `ok: true` with `error.code = "x"` | exit 1, `observed_mismatch` |
| G | `ok-field:m={"a":1,"a":1}` (duplicate member in the *literal*) | receipt `{"a":1}` | exit 1, `observed_mismatch` |
| I | `ok-field:n=9007199254740992` | `"n": 9007199254740993` | exit 1, `observed_mismatch` (no float precision leak — `int` path exact) |
| E | `ok-empty:sessions` | `"sessions": {}` | exit 1, `observed_mismatch` |

The `error:` comparison is `env["error"].get("code") == observed[len("error:"):]`, i.e. `==` against a **str**; Python never coerces bool/int to str, and the dict guard `isinstance(env.get("error"), dict)` plus `ok is False` (rejects `0`) close the remaining doors. Nested `KeyError` from `dig` (non-dict interior) is already funneled to `observed_mismatch`. A 1200-deep nested receipt parses and is decided normally (case B: exit 1, `observed_mismatch`) — no crash path found on the error side.

## Declared limits respected (not findings)

- `limit` "receipt/row agreement at one revision; not provider availability over time" — the counter indeed evaluates exactly one revision.
- `duplicate_rows` / `foreign_rows` gating and the `probe == verb` equality (fixture `probe_alias`) behave as declared.
- Receipt prefix confinement incl. `..` segments and symlink-free blob reads via `git show` — controlled.

## Narrow fix (author-side; lane untouched)

Two-point patch in `count-c2.py`, +14/−1 lines. `json_same` enforces: bool is its own class (`is`), numbers compare across int/float (JSON has one number type, so `1 == 1.0` stays a match — F1's demonstrated conflation `true≡1`, `false≡0` is killed), containers recurse element-wise, everything else requires exact type. The `parse_float` guard routes overflow-literal `inf` into the existing `ValueError` → `receipt_unevaluable` path, honoring the docstring's non-finite refusal symmetrically for receipts and literals:

```python
import math
# in strict():
def strict(text):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate_member: " + key)
            out[key] = value
        return out

    def constant(value):
        raise ValueError("nonfinite_number: " + value)

    def finite(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("nonfinite_number: " + value)
        return number
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant,
                      parse_float=finite)

def json_same(left, right):
    if isinstance(left, bool) or isinstance(right, bool):
        return left is right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(json_same(a, b) for a, b in zip(left, right))
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(json_same(left[k], right[k]) for k in left)
    return type(left) is type(right) and left == right

# in check(), ok-field branch:
        elif observed.startswith("ok-field:") and "=" in observed:
            dotted, literal = observed[len("ok-field:"):].split("=", 1)
            ok = env.get("ok") is True and json_same(dig(env.get("data"), dotted), strict(literal))
```

Semantics unit-verified before proposal (same interpreter): `json_same` keeps `1≡1.0`, exact bool/str/null, container-order sensitivity (`[1,2] != [2,1]`), dict key-set equality; rejects `False≡0`, `True≡1`, `[1]≡[True]`, `{"a":0}≡{"a":False}`, `0≡"0"`, `None≡0`, `[]≡{}`; `finite("1e999")` raises, `finite("1e10")` returns `10000000000.0`. Optional one-liners for F3 (`if not observed[len("error:"):]: return "bad_observed_grammar"` and a non-empty check on the `ok-field` dotted part) and F4 (`except UnicodeError: return "receipt_unevaluable"` around the `git_show` call in `check()`). F5/F6 need no change for the claim's verdicts; if touched at all, collect rows under every exact `HEADING` line (`==`, not `startswith`).

## Verification gaps / residual risk

- No execution of any REA binary or device contact anywhere (fixture envelopes are hand-authored JSON; consistent with the contract's unavailable-client posture).
- F1's practical exploitability inside this lane is low today: the retained `ok-field` rows claim `null` and `"local"` (string), neither of which coerces with a plausible alternative type — but the counter must not rely on that accident; the flaw stands on the frozen grammar.
- Per-case commit SHAs live only in the ephemeral scratch repos (tmpfs); the harness reproduces every row deterministically from the commands embedded above.
- Sibling-seat convergence: F2≈C2Json F1, F4≈C2Json F3, F5-variant≈C2Json F4 (independent reproduction, distinct case shapes). F1, F3a/b, F6 and the full error-path clean table are unique to this seat.

## Retained harness (author-side, for L1 integration if wanted)

```python
# /tmp/r22c2/harness.py + harness2.py (merged view); run with python3, no deps.
# Builds a scratch git repo with the 14-verb baseline table, one commit per case,
# and runs the frozen counter via: python3 -I -B <count-c2.py> --root <repo> --rev <commit>
# Case table (name -> row observed / receipt mutation):
#   01_clean_all14            control                                  -> exit 0, 14/14, matched
#   02_bool_field_vs_0        ok-field:transport=0 / data.transport=false   -> exit 0 (F1)
#   03_int_field_vs_true      ok-field:enabled=true / data.enabled=1        -> exit 0 (F1)
#   04_nested_list_coerce     ok-field:items=[1,false] / [true,0]           -> exit 0 (F1)
#   05_dict_coerce            ok-field:m={"a":false} / {"a":0}              -> exit 0 (F1)
#   06_inf_overflow_2e999_vs_1e999  ok-field:r=1e999 / data.r=2e999         -> exit 0 (F2)
#   07_error_code_int0        error:0 / error.code=0 (int)                  -> exit 1 (clean)
#   08_ok_numeric0            error:x / "ok":0                              -> exit 1 (clean)
#   09_empty_error_code       error: / error.code=""                        -> exit 0 (F3a)
#   10_exact_bool_match       ok-field:flag=false / false                   -> exit 0 (control)
#   11_empty_dotted_segment   ok-field:=5 / data {"":5}                     -> exit 0 (F3b)
#   A_non_utf8_receipt        receipt bytes b'\xff\xfe{}'                   -> exit 2 (F4)
#   B_deep_nesting_recursion  1200-deep receipt                             -> exit 1 (clean)
#   C_duplicate_section_first_wins  stale first heading                     -> exit 1 (F5)
#   D_duplicate_section_empty_first exact dup heading, first empty           -> exit 1, unaccounted (F5)
#   E_ok_empty_vs_dict        ok-empty:sessions / {}                        -> exit 1 (clean)
#   F_error_observed_but_ok_true  error:x / ok:true + error.code="x"        -> exit 1 (clean)
#   G_literal_duplicate_member  ok-field:m={"a":1,"a":1}                    -> exit 1 (clean)
#   H_literal_infinity_vs_receipt_inf  ok-field:r=Infinity / data.r=1e999    -> exit 1 (clean, asymmetry)
#   I_int_precision_exact     ok-field:n=9007199254740992 / 9007199254740993 -> exit 1 (clean)
#   J_receipt_is_directory    receipt cell = the c2 directory               -> exit 1, receipt_outside_prefix (F6)
```
