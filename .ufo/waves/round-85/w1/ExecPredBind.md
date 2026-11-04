# ExecPredBind — R85-C1 predicate-bind counter (round 85, wave r85-w1)

Declaration rev measured: `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`. Lane untouched; all bytes under
`.ufo/waves/round-85/w1/ExecPredBind/`. No tool installs were needed (stock `python3` + `git`; nothing
added to PATH, no pacman).

## Files changed (candidate, not integrated)

- `candidate/tools/round-85/predicate-bind.py` — new counter, stdlib only, runs as `python3 -I -B`,
  modeled on `tools/round-84/freeze-precheck.py` (copied: `git_blob`, `strings`, `pins`, `SCRIPT_RE`,
  CLI shape `--root/--rev/--container/--expect/--control instruments-only/--selftest/--json-out`,
  receipt keys `containers/controls/control_fired/mismatches/refused_expected/accepted_expected/met/rev/schema`).
  Schema: `kaidoku-r85-predicate-bind-v1`.

## Rule as implemented (frozen predicate sentence)

Paths are read from each claim's `predicate` string only (`kill_rule` alone never satisfies). A path
counts when it is (a) a blob at `--rev`, (b) pinned in `instruments`/`loaded_by_counter`/
`producers_not_counters` at its blob digest, (c) in a sentence without a negation token. Sentences are
split on `.`/`;`/newline with path spans masked first (a path never straddles a boundary; tokens inside
a path never count). Negation tokens, word-boundary, case-sensitive lowercase: `not no never without
neither nor cannot` — `none` deliberately excluded (r84 predicates read "mismatches none"). Documented
decision: a claim is refused if ANY predicate path is negated (`PB_PREDICATE_NEGATED` once per claim);
otherwise one affirmative pinned blob-verified path carries it, but every defective affirmative path is
reported per path, so a good path never offsets a bad one — matching the claim's kill rule.

## Measured results (all at the frozen measure command, exit 0)

| check | result |
|---|---|
| F1 | FLAGGED, exactly `PB_NO_PREDICATE_PATH:R85-F1` |
| F2 | FLAGGED, exactly `PB_PREDICATE_NEGATED:R85-F2` |
| `.ufo/waves/round-84/claims.json` | CLEAN, findings [] |
| mismatches / refused_expected / accepted_expected | `[]` / 2 / 1 |
| control_fired (instruments-only accepts F1, F2) | true (`met: true`) |
| same run with `--control` omitted | identical verdicts, `met: true`, exit 0 |
| BASE comparison (`base-freeze-precheck.json`) | r84 gate at same rev: F1 CLEAN, F2 CLEAN, refused_expected 0 — the do-nothing control cannot reach the target |

`--selftest`: 21 fixture cases, 0 failures, exit 0 (`selftest.json`). Covers every finding exactly:
kill-rule-only path, negated same sentence, negated path in a second sentence (flags — that path shares
its sentence), negation in a second/semicolon/newline-separated sentence with the path in the first
(accepts), `none` not a negation, `cannot` negates, not-blob, unpinned, wrong digest, unparsable JSON,
no claims, multi-path one-unpinned, predicate-as-list, relative-path guard, second-claim naming, and the
cheap rule accepting a defective container while rejecting an empty `instruments` map.

## r83 / r84 negation confirmation (diagnostic run)

- `.ufo/waves/round-83/claims.json` (present at REV): FLAGGED with `PB_NO_PREDICATE_PATH:R83-C1` — its
  predicate says "attribution mismatches 0 across exactly eight frozen cases…" and names no script path
  (the counter `tools/round-83/attribution-audit.py` is pinned only at container top level). That is the
  exact gap round-84's gate docstring records; this counter closes it. Exit 1 here is the diagnostic
  mismatch line (no `--expect` passed), not a failure.
- `.ufo/waves/round-84/claims.json`: CLEAN — all three predicates name their counters affirmatively;
  `mismatches none` / `survivors none` correctly do not negate (`none` is not a token), and R84-C3's
  "REA 6.5.0" dots only fragment later, path-free sentences. No negation false positive.

## Limits (for the lesson)

This is a naming-and-negation lint, not semantics: a predicate that names the counter in an affirmative
but meaningless sentence still passes, and pin checks only see the three pin maps (a digest pinned under
`frozen_instruments`/`target_instruments` instead is "not pinned" here). The naive `.`-sentence split
cuts version numbers and abbreviations ("REA 6.5.0", "v4.a") into fragments, so a negation token after
such a dot is read into a different fragment than the path and will not negate it — conservative for
clean containers, but a real miss for a negation hiding after an abbreviation dot; likewise a negation
token anywhere in the path's sentence flips the claim even if it scopes a different clause ("cannot" is
a common word). Paths are masked before splitting, so tokens inside a path never self-negate, but a path
spelled without its `tools/`/`corpus/`/`.ufo/` prefix is invisible to SCRIPT_RE and reads as no path at
all. Finally, a container whose claims name a counter with an empty-string `id` falls back to
`<unnamed-claim>` labels, and the `--expect` key is the literal container path, so two containers with
identical paths cannot carry distinct expectations.

## Evidence files (this dir)

- `candidate/tools/round-85/predicate-bind.py` — the counter
- `after-predicate-bind.json` — frozen measure with control (met true, exit 0)
- `after-predicate-bind-nocontrol.json` — same without `--control` (met true, exit 0)
- `selftest.json` — 21 cases, failures []
- `r83-r84-predicate-check.json` — diagnostic run
- `base-freeze-precheck.json` — BASE do-nothing receipt copy (source: `.ufo/waves/round-85/pre/c1/`)
