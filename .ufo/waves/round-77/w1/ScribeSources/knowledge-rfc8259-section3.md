source: own-work — `tools/round-77/verdict-bind.py`, with receipts `.ufo/waves/round-77/pre/c1-at-base.json` (rev `188562d4`, `mismatch_count 4`, 21 bound clauses, 9 in-scope rows) and its 15-case selftest `pre/selftest-c1.json`; S289 grounds the type-strict comparison; the outside population is `corpus/lessons/round-76-verifier-spotcheck.md` section 6 item 5
verified-at: 2026-11-04
recheck: `python3 -I -B tools/round-77/verdict-bind.py --root . --rev <rev> --json-out <receipt>` (`mismatch_count`, `population.bound_clauses`, `population.in_scope_rows`)

# A verdict beside a path is a claim, and the path does not answer it

Round 76's capability row said

> `.ufo/waves/round-76/l1/scores/c1-at-landing.json` (D24 true, mismatch_count 0)

and that receipt records `exit 1`, `mismatch_count 1`, `D24_capability_rows false`. The atom built to catch
record/table divergence, `D24_capability_rows`, was green: it reads the path, checks that it resolves at the
measured revision, and never parses the verdict written next to it. A pointer is not a claim; a verdict is, and
the pointer cannot stand for it.

## Gate

| field | value |
|---|---|
| row | S289 — RFC 8259 section 3 Values (JSON), `spec`, tier A, `mined` |
| URL | https://www.rfc-editor.org/rfc/rfc8259.txt |
| accessed | 2026-11-04 |
| snapshot | `.ufo/waves/round-77/l1/sources/rfc8259.txt`, 28 360 B, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| located quote | "A JSON value MUST be an object, array, number, or string, or one of" — section 3 Values (heading line 296), quote line 298, 14 words, contiguous plain text (not composite); the sentence continues to line 301 and the three literal names are at lines 301-303 |
| consumer | `tools/round-77/verdict-bind.py` line 187, `type(claimed) is type(actual) and claimed == actual` |

## What the grammar binds

`verdict-bind.py` reads a frozen record surface — the SCORECARD `## Capabilities` rows whose first-working-round
numeral is `>= 73`, plus the PROVINCE `- **Core — ` bullets — and parses every parenthesised annotation with a
closed vocabulary:

| form | binding | example |
|---|---|---|
| `field literal` | typed equality with a top-level receipt field | `mismatch_count 0` |
| `atom-id true/false` | the named atom's `ok`, by unique short id or full id | `D24 true` |
| `field N of M` | `field == N` and `field_total == M` (`arms_ok` → `arms_total`) | `arms_ok 3 of 3` |
| `N mismatches` | `mismatch_count == N` | `0 mismatches` |
| `N survivors` | `survivor_count == N` | `0 survivors` |
| `N\|word atoms` | `len(atoms) == N` | `nine atoms` |
| `pristine N [cases]` | `pristine.cases == N` | `pristine 25` |
| `validate defect-free` | `validate.defects == []` | `validate defect-free` |

A leading `<word>:` qualifier is stripped and retained. A clause the grammar cannot parse is recorded as
**unbound**, never guessed; a field the receipt lacks is unbound too — an absent field is not a pass. Prose
annotations that parse to nothing make no claim, and a cell with no JSON pointer cannot carry a bound clause at
all (`no_json_receipt`).

## Why the comparison is type-strict

`mismatch_count true` against a receipt field of `1` must fail. S289 (RFC 8259 section 3) fixes JSON's value
taxonomy: `false`, `null` and `true` are literal names, numbers are another value class. In Python
`True == 1`, so an `==` comparison would accept a boolean where the record holds an integer; the instrument
compares types (`type(claimed) is type(actual)`, line 187) so the annotation says what the receipt says.

## Limits

- The scope is the lane's own record layer, not the corpus: a knowledge entry's prose verdict is outside it.
- A clause is bound to the path nearest before its group; a cell that names two receipts and then writes one
  group binds the group to the nearer path. The bound path is printed in the receipt, so a mis-binding is visible.
- The instrument never edits the record. It reports; the lane corrects.

## Round-77 measurement

Base `188562d4`: `exit 1`, `mismatch_count 4` — the `capability-row binding` row and `PROVINCE.md` line 585, each
carrying the same two false clauses (`D24 true` vs `false`, `mismatch_count 0` vs `1`) — over 21 bound clauses and
9 in-scope rows. The landed record cites `c1-at-tip.json` (`D24 true`, `mismatch_count 0`, nine atoms) and
restates the landing receipt as "1 by construction".
