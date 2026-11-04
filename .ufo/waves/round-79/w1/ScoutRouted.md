# ScoutRouted — round-79 wave-1 recon

Scope: read-only inventory of the two round-79 instruments' CLI contracts from the
committed bytes at the freeze `ed68cd0a`, re-derivation of the round-78 wave
accounting, a numeric-clause/receipt-field map for both frozen claims, and the
round-79 freeze-gate entry. Nothing outside this evidence dir was written.

Bearer facts: freeze `ed68cd0a6cc790cca342380a2d80d1927a668c8c`, base
`29d2ca30b83a6a0d85b0aa979de0138fde1660e6`, declaration
`a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d`, HEAD at measurement
`da8e5d5e401c3567d87f0ff58ecee34726c1aecc`.

## 0. The one finding that matters

**R79-C2's frozen predicate and `counting_command` omit `--battery`, and the frozen
instrument exits 2 on exactly that argv and writes no receipt.**

```
$ python3 -I -B <frozen pointer-bind.py at ed68cd0a> \
    --root . --rev ed68cd0a... --json-out /fast/scratch/.../probe.json
usage: --battery --rev <rev> [--json-out <path>] [--control path-only]
EXIT=2   receipt_written=no
```

The same argv at base `29d2ca30` also exits 2. With `--battery` appended, the freeze
arm exits 0 (`checks_total 5, matched 5, mismatches 0, unparsed 0`) and the base arm
exits 1 (`matched 3, mismatches 2, omp-pin + kimi-pin`). Every number in the claim is
therefore true of *command plus flag* and untrue of *command as printed*.

Both frozen claims print the same shape — `claims.json` R79-C2 `counting_command` and
the `PREDICATE` string baked into `pointer-bind.py` — so the claim's own reproduction
recipe does not run. The C1 predicate does include `--battery` and does run as printed.

An uncommitted edit by another seat is in the worktree right now making `--rev` imply
`--battery` (`git status`: ` M tools/round-79/pointer-bind.py`, sha256 `3f07bd2a…` vs
pinned `91d23dad…`). HEAD and the freeze still carry the pinned bytes. This seat did
not touch it; landing it changes the instrument digest and therefore needs a
supersession entry.

Why the freeze gate could not see this: `auth_findings`
(`tools/round-78/attack-gate.py:534-551`) admits a claims receipt when the instrument
`{path, sha256}` re-derives at the receipt's rev. It never executes the predicate. A
CLEAN verdict means "the three instrument pins resolve", not "the claim runs".

## 1. CLI contract (committed bytes at `ed68cd0a`)

Digests at freeze / declaration / HEAD are identical for both instruments and equal to
the pins in `claims.json` (`682f1e78…`, `91d23dad…`); `attack-gate.py` is
`4e4baf00…`. Both round-79 instruments are absent at base (`git show 29d2ca30:…` →
exit 128), so the base arms necessarily run them from a later revision.

Mode precedence in both `main()`s: `--selftest` > `--validate` > `--battery`. A
`--validate` combined with `--battery` silently validates and never measures.

### `tools/round-79/gate-mutation.py` (417 lines)

| mode | argv | exit | writes |
|---|---|---|---|
| `--selftest` | `… --selftest` | 0 all cases pass / 1 otherwise | stdout only: `{case,got,want,pass}` lines + `SELFTEST cases=N failures=M`; no receipt file |
| `--validate` | `… --validate PATH` | 0 `defects==[]` / 1 defects or unreadable path | stdout only: `{defects,mutants,survivors}` |
| `--battery` | `… --root . --rev REV --work DIR --battery --json-out PATH` | 0 `ok` / 1 red / 2 no `--rev` or target absent at rev | receipt (fields below) |
| `--control empty-set` | same + `--control empty-set` | always 1 (`ok` requires `len(mutants)==len(MUTANTS)==8`) | receipt with `mutants_total 0, killed 0, survivors 0, hits 0, ok false` |
| no mode | `…` | 2 | stderr usage |

Receipt fields: `schema, round, predicate, measured_at,
target{path,rev,bytes,sha256}, target_pin{expected,actual,matched},
pristine{exit,cases,failures,ok,failed_cases}, mutants_total, killed, survivors,
survivor_ids, declared_case_hits, control, mutants[], ok`.
Per mutant: `id, edit, declared_case, applied, apply_note, exit, failed_cases,
case_absent, killed, killed_by_declared, detector_count, sole_detector, inconclusive`
(+ `stderr_tail` when inconclusive).

Measured: selftest 11/0 exit 0. Base arm exit 1 `8/5/3`, hits 5, `pin_matched false`,
pristine 26/0. Freeze arm exit 0 `8/8/0`, hits 8, `pin_matched true`, pristine 29/0.
Sole detectors at the freeze: `m02`, `m03`, `m04`, `m05`, `m08` (the claim names
`m03`, `m05`, `m08`; it does not claim exhaustiveness).

### `tools/round-79/pointer-bind.py` (344 lines)

| mode | argv | exit | writes |
|---|---|---|---|
| `--selftest` | `… --selftest` | 0 / 1 | stdout only; measured 16 cases, 0 failures |
| `--validate` | `… --validate PATH` | 0 `defects==[]` / 1 defects or unreadable path | stdout only: `{defects,checks,matched}` |
| `--battery` | `… --root . --rev REV --battery --json-out PATH` | 0 `ok` / 1 red / 2 missing `--rev`, missing `--battery` (frozen bytes), or `PROVINCE.md` absent at rev | receipt |
| `--control path-only` | same + `--control path-only` | 0 while all five paths exist | receipt with `line_start/line_end` null and `line_sha256` empty on every check |
| `--rev` without `--battery` | the printed predicate argv | 2, no receipt | stderr usage |

Receipt fields: `schema, round, predicate, checked_at, record{path,rev,sha256},
control, checks_total, matched, mismatches, unparsed, checks[], ok`.
Per check: `id, pointer, tokens, path, line_start, line_end, matched, unparsed,
reason, line_sha256`.

Measured: base exit 1 `5/3/2`, `unparsed 0`, `omp-pin` pointer `…/mcp.json:8`,
`kimi-pin` pointer `~/.kimi-code/config.toml:4126`. Freeze exit 0 `5/5/0/0` with the
same two pointers at `:12` and `:4722`. Control exit 0 `5/5/0/0`.

Both instruments' `--selftest` short-circuits before `--root`, `--validate` and
`--battery`, so `--selftest` can never be combined with a measurement.

### Exit-contract defect

`--validate` on an unreadable path is unguarded in both: `json.loads(open(path))`
raises `FileNotFoundError`, the process exits **1** — the same status as "the claim is
false". Both tools reserve 2 for could-not-evaluate, but never use it here.

## 2. Round-78 wave accounting

Source `.ufo/waves/round-78/r78-w1-results.json` (`seats: 12`, `results` length 12),
evidence root `.ufo/waves/round-78/w1/`.

| measure | value |
|---|---|
| seats | **12** |
| non-empty output | **11** |
| evidence dir exists | **10** |
| zero-byte output | 1 (`ExecSurfaceProbe`) |
| no evidence dir | 2 (`CriticClaims` 2133 B, `SentinelScope` 272 B) |

Report sentence (`SCORECARD.md:6107-6114`): "10 seats returned substantive evidence
(all files under `.ufo/waves/round-78/w1/`), 1 returned a progress note only
(`SentinelScope` …) and 1 returned a truncated final answer (`ExecSurfaceProbe` …)".

Verdict: the three counts and the 10/1/1 partition are numerically right, the
membership clause is off by one. The substantive bin must include `CriticClaims`,
which wrote nothing under that dir; `ExecSurfaceProbe`, which did write there, is the
truncated one. Two seats lack an evidence dir and the sentence names one of them. This
is the same class of defect the round-78 scout routed (`LOG.md:4601`), still present.

## 3. Claim clauses vs receipt fields

Full machine-readable map in `receipt.json → claim_fields`. Summary of the gaps:

**No receipt field at all**

- C1 and C2 "exits 0 / exits 1": process status only; the receipt carries `ok` and no
  `exit` field (the printed stdout summary has one, the file does not).
- C1 and C2 "a defect-free `validate`": produced by a separate invocation and never
  recorded. It is also green on both red base receipts and on the C1 empty-set control,
  so the clause is non-discriminating.
- C2 "the pin at `:12`" and "the pin at `:4722`": the receipt records only the asserted
  line (8 / 4126) and the reason "token … is not on line 8". The true line is nowhere.
  It is recoverable only from the freeze receipt's pointer or a token grep.
- Both: `argv` and `--root`. No receipt can be tied to the printed counting command.

**Partial**

- C1 "eight exact single-occurrence edits": `applied: true` + `apply_note: "applied"`;
  the occurrence count, anchor and replacement are not in the receipt, so the
  "exactly 1" rule lives only in `apply_mutant`.

**Present and re-derivable**

- C1: `mutants_total`, `killed`, `survivors`, `survivor_ids`, `declared_case_hits`,
  `target_pin.matched`, `pristine.cases/.failures`, per-mutant `case_absent`,
  `failed_cases`, `sole_detector`, `detector_count`, `target.rev`.
- C2: `checks_total`, `matched`, `mismatches`, `unparsed`, per-check `pointer`,
  `line_start`, `line_end`, `line_sha256`, `matched`, `record.rev`; the control's
  `mismatches` lives in a separate receipt file and `claims.json` `counting_command`
  does not name the `--control path-only` invocation that produces it.

Cross-check: my base and freeze receipts reproduce the pre-stored ones field for field
(`pre/c1-at-base.json`, `pre/c2-at-base.json`, `pre/controls/c2-path-only.json`).

Minor: `killed_by_declared` is dead — `judge()` sets it equal to `killed`, which already
requires the declared case to fail.

## 4. Round-79 freeze-gate entry (verbatim, `.ufo/waves/round-79/l1/scores/freeze-audit-at-freeze.json`)

```json
{
 "claims_file": ".ufo/waves/round-79/claims.json",
 "findings": [],
 "freeze": "ed68cd0a6cc790cca342380a2d80d1927a668c8c",
 "instruments": [
  "tools/round-78/attack-gate.py",
  "tools/round-79/gate-mutation.py",
  "tools/round-79/pointer-bind.py"
 ],
 "verdict": "CLEAN"
}
```

Context: `claim "R29-freeze-gate"`, `rev ed68cd0a…`, `audited 54`, `clean 29`,
`required_clean ["round-79"]`, `required_failed []`, `summary
{INSTRUMENT_ABSENT 12, INSTRUMENT_NONE 7, INSTRUMENT_PIN_MISMATCH 3,
INSTRUMENT_REVISED 18, INSTRUMENT_UNPINNED 12, INSTRUMENT_UNRESOLVED 11}`,
`flagged` 25 entries, `round-79` not among them.

The three instrument paths match the task's "three instrument paths"; no findings;
verdict CLEAN. Under `auth_findings` this verdict is about pin resolution only, which
is why it is compatible with the unrunnable C2 command.

## 5. Files

- `receipt.json` — acceptance object (`cli`, `wave_accounting`, `claim_fields`,
  `freeze_gate`, `findings`, `evidence`, `risks`).
- `c1-at-base.json`, `c1-at-freeze.json`, `c2-at-base.json`, `c2-at-freeze.json`,
  `c2-control-base.json` — measured this session.
- `pred-argv-freeze.txt`, `pred-argv-base.txt` — the frozen C2 predicate argv, exit 2,
  no receipt written.
- `pb-selftest-frozen.txt` — 16/0 against the frozen bytes.

Worktree drift at yield: both round-79 instruments carry uncommitted edits by other
seats (`gate-mutation.py` `682f1e78…` → `75fbf1a7…`, `pointer-bind.py` `91d23dad…` →
`3f07bd2a…`); `attack-gate.py` is still `4e4baf00…`. Every measurement above was taken
against the pinned bytes, each instrument verified equal to its pin immediately before
its first arm. Landing either edit breaks the corresponding `claims.json` instrument pin
and needs a supersession entry rather than a silent re-pin.

No tools installed or upgraded; no pacman transaction; no git/jj writes; scratch under
`/fast/scratch/hyaku/kaidoku-r79/ScoutRouted/` removed before yield.
