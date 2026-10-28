# ScribeRowsC — third pass over failing registry verdict cells (R48-C1 clause 8)

Scope: the 16 registry verdict cells that fail `meaning_classes` under `--profile v3`.
For each: a proposed repair that keeps the tool's honest exit semantics AND satisfies the
frozen counter, or an argument that the counter vocabulary is wrong for that tool.
Measured against worktree `SKILL.md` at `ac02a79ff8` and the frozen counter at
`dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` (A2 bytes — the exit-0 guard is gone).

**Frozen counter status: not touched, not mutated. SKILL.md: not touched. All evidence is
in-memory scoring plus fixture-free `meaning_classes` calls (the exact function clause 8
delegates to, `tools/round-48/meanings.py:227-247`).**

## Bottom line

- 16 of 40 existing registry rows fail clause 8; the counter's clause-8 run on a synthetic
  landing reproduces `meaning_rows_failed 16`, `registry_missing [meanings.py, record2.py]`,
  `registry_extra []`, `registry_duplicates []`, `census_rederived_equal true`
  (receipt `score-clause8.json`).
- All 16 have honest repairs — a class prefix or one-word rewrite, never a semantics change.
  With all 16 repairs plus the 2 new census rows applied to a copy, clause 8 goes fully
  green: `meaning_rows_failed 0`, `registry_missing []`, `registry_rows 42` vs census 42
  (receipt `score-clause8-repaired.json`).
- One row needs a *word choice* argument rather than a plain class prefix: `gate.py`'s
  exit 1 is a usage refusal (unevaluable-class), and `refusal` happens to sit in the
  counter's NOTMET vocabulary. Details below.
- **Residual forgery finding (new):** clause 8 binds token shape, not meaning —
  `1=scored` and `1=covered` pass as the not-met segment because `NOTMET`'s `red` is an
  unanchored substring (`meanings.py:59`), and `no placeholder text` only excludes
  `banana|nope|whatever` (`meanings.py:62`, `:233-234`). A forged row
  `0=met and green; 1=scored; 2=usage error` scores `{0:success,1:not-met,2:unevaluable}`
  (receipt `forgery-probes.txt`, probe P2). Clause 8 as frozen is still lexically
  satisfiable by text carrying no meaning; only the battery forgeries are checked, and the
  battery does not mutate segment classes to non-vocabulary noise.
- The two missing census rows (`tools/round-48/meanings.py`, `tools/round-48/record2.py`)
  get drafted verdict cells below; both verified green through `meaning_classes`.

## The counter's class machinery (what the repairs target)

`meaning_classes` (`meanings.py:227-247`): `_segments` splits the cell on
`(?<![0-9])([012])\s*=` requiring exactly marks `0,1,2` in order; BANANA check; then
- seg0 must match `SUCCESS = \b(met|clean|ok|green|pass|passed|verified|succeeded|wrote)\b`
- seg1 must match `NOTMET = (not met|violation|red|fail|failed|no verdict|refusal|refused|unresolved)` — **unanchored alternation**
- seg2 must match `UNEVAL = (could-not-evaluate|unevaluable|could not evaluate|\busage\b|\berror\b|absent|unreadable|refus)`
- the three segment texts must be pairwise distinct (`:245`).

Asymmetric anchoring: SUCCESS tokens are word-bounded (`\bpass\b` misses `passes`,
`\bmet\b` misses `met_target`), while NOTMET's `red`/`fail`/`refus` and UNEVAL's `refus`
match inside words. `\berror\b` misses `errored`/`errors`.

## The 16 failing rows and the proposed repairs

Each repair is the minimal edit that (a) keeps the tool's real meaning and (b) gives each
segment its class token. Verified: `meaning_classes(repaired) == {0:success,1:not-met,
2:unevaluable}` for all 16 (receipt `proposed-cells.json`, `all_pass: true`).

| row | error | proposed repair (the changed part) |
|---|---|---|
| round-41/c1-extra.py | exit 0 no success | seg0 → `0=met, all three bindings true, or a selftest in which every case passes` |
| round-41/c2-controls.py | exit 0 no success | seg0 → `0=green, no control reaches n/n so the kill rule does not fire`; seg1 → `1=not met, a control reaches n/n…` (seg1 also lacked a not-met token — masked behind seg0 because the counter returns on the first None class) |
| round-41/fetch-vendor.py | exit 0 no success | seg0 → `0=met, every external carrier materialised and every chain hash matched` |
| round-41/local-source-gate.py | exit 0 no success | seg0 → `0=green, every out-of-lane row resolved` |
| round-41/mk-l-carriers.py | exit 1 no not-met | seg1 → `1=not met, never a designed verdict: no explicit path returns it and only an uncaught exception does, e.g. a writer that exits 0 without writing the image raises FileNotFoundError at the sha256 read` |
| round-42/c1-run.sh | exit 1 no not-met | seg1 → `1=not met, no designed verdict: an unguarded command under set -e aborts with that command's status, which may be 1` |
| round-42/c2-controls.py | exit 0 no success | seg0 → `0=green, no control reaches full score, the kill rule stays silent` |
| round-42/heldout-gen-v4.py | exit 2 no unevaluable | seg2 → `2=could-not-evaluate, argparse rejected the argv, so nothing was evaluated` |
| round-42/indep-eval-v4.py | exit 0 no success | seg0 → `0=ok, one record printed or written for the single envelope, or the batch payload emitted for a directory` |
| round-42/sqfs3-oracle.py | exit 0 no success | seg0 → `0=met, producers agree and oracle.tsv plus nonregular.tsv are written` |
| round-42/unblob-logtee.sh | exit 0 no success | seg0 → `0=ok, the wrapped unblob returned 0, log copied when C1_LOG_COPY names an existing destination` |
| round-43/c1-counter.py | exit 0 no success | seg0 → `0=met, met_target true, every held-out pair matched and every binding true` (`met_target` misses `\bmet\b`) |
| round-43/c2-score-r43.py | exit 0 no success | seg0 → `0=met, all 13 checks true`; seg1 → `1=not met, at least one check false…` (second masked seg-1 failure) |
| round-44/c1-run.sh | exit 0 no success | seg0 → `0=met, every carrier ran and produced a receipt` |
| round-46/census.py | exit 0 no success | seg0 → `0=ok, census computed and printed, and written when --out is given`; seg1 → `1=not met, an unhandled exception such as an unwritable --out: a traceback, not a designed verdict` |
| round-46/gate.py | exit 1 no not-met | see the argument below |

Honesty notes on the three "not met" prefixes: for `mk-l-carriers` and `c1-run.sh`, exit 1
means the run's goal was not achieved (no second carrier pair / the arm aborted) — honest
not-met. For `census.py`, exit 1 is a crash on which the census was not computed — honest
not-met, kept with the "not a designed verdict" qualifier.

### tools/round-46/gate.py — the one arguable row

Code line: `gate.py:247` — `sys.exit("gate.py is a library; use attest.py or registry.py")`.
`sys.exit(str)` exits **code 1**, so gate.py's only exit-1 producer is a *usage refusal*:
"evaluates nothing, and no library entry point returns 1". Honest class: unevaluable, not
not-met. The frozen counter's fixed `cls["1"]=="not-met"` binding (`meanings.py:237,
241-243`) is wrong for this tool — no token makes an invocation refusal a not-met verdict
without bending the word.

Repair that stays honest AND satisfies the counter (the `refusal`/`refused` vocabulary is
in NOTMET, `meanings.py:59`):

```
1=refusal, not a verdict: running gate.py as a program exits 1 printing
"gate.py is a library" and evaluates nothing; no library entry point returns 1
```

Verified `{1:not-met}` via `refusal`. I flag, though: this works only because the counter
admits `refusal` as a not-met synonym while `refus` in UNEVAL is unanchored. If L1 prefers
the stricter reading, the alternative is to record in the round-48 report that gate.py's
exit-1 is a refusal class that the frozen digit→class table cannot name without the
vocabulary's own overlap; the proposed text above is the least-dishonest formulation —
it names the refusal and never calls a refusal a failed measurement.

## Two missing census rows (L1 must add; drafted and verified)

`registry_missing [tools/round-48/meanings.py, tools/round-48/record2.py]`. Proposed
verdict cells (full row shape in `proposed-cells.json.new_rows`):

- `tools/round-48/meanings.py`: `0=met with failing empty and the four-forgery battery on
  target; 1=not met, each false clause named in failing; 2=could-not-evaluate:
  frozen_path_changed, SKILL.md absent at rev, malformed claims file, craft section,
  registry or census, a battery error, a refused --json-out, an unknown revision, or an
  unhandled exception`
- `tools/round-48/record2.py`: `0=met with failing empty and the five-forgery battery on
  target; 1=not met, each false clause named in failing; 2=could-not-evaluate:
  frozen_path_changed, SCORECARD.md absent at rev, an oracle import or exec failure, a
  malformed card, a refused --json-out, an unknown revision, or an unhandled exception`

## Residual forgery surface (the valuable negative finding)

`meaning_classes` is a lexical classifier, and clause 8's "no placeholder text" names only
`banana|nope|whatever`. Demonstrated (`forgery-probes.txt`):

| probe cell | result |
|---|---|
| `0=met; 1=red; 2=usage` | green — pure token shorthand |
| `0=met and green; 1=scored; 2=usage error` | green — `scored` carries `red` inside it, has no not-met meaning |
| `0=met; 1=covered by the run; 2=could-not-evaluate` | green — `covered` likewise |
| `0=…declared…generated…` in seg0 | green — `decla(red)`, `gene(red)` also leak (harmless post-A2, proves the substring) |
| `0=met; 1=failed; 2=errors` | red — `errors` misses `\berror\b` (plural rejected) |

Consequence for the claim: R48-C1 clause 8 closes R46-CL7's `banana` cell only for the
three named mutations. A registry row written as `0=met and green; 1=scored; 2=usage
error` is a meaning-free forgery that the frozen counter scores clean. The kill rule
survives (it is battery-scoped), but clause 8's wording — "meanings carry the class their
digit claims" — overstates what the frozen bytes enforce. L1 may want a round-49 routing
note: anchor `red`/`fail`/`refus` to word boundaries, or grow the placeholder set; note
the tension — `gate.py`'s honest repair itself rides the unanchored `refus`/`refusal`
overlap.

## Pass notes for L1 (word-level pitfalls seen across all 42 rows)

- Two masked seg-1 failures surface only after seg0 is fixed (`c2-controls.py` round-41,
  `c2-score-r43.py`): the counter reports the FIRST missing class, so a green seg0 result
  does not mean segs 1-2 are clean. Re-run after each edit.
- `passes`/`passing` never satisfy `\bpass\b`; use `passed` or a `met|ok|green` prefix.
- `met_target` never satisfies `\bmet\b`.
- `written`/`emitted`/`printed` never satisfy SUCCESS; `wrote` does.
- `errored`/`errors` never satisfy `\berror\b`; use `usage error` or `could-not-evaluate`.
- `never a verdict`/`no designed verdict`/`not a verdict` do NOT contain `no verdict`
  (verbatim token); a refusal segment needs `refusal`/`refused`/`violation`/`failed`
  or an explicit `not met`.
- Existing seg-0 text containing `-red` suffixes (`generated`, `declared`, `produced`,
  `covered`) is harmless post-A2 — the exit-0 absence-of-not-met guard is gone — but it
  is the same substring the `1=scored` forgery rides.

## Receipts

| file | content | sha256 |
|---|---|---|
| receipts/analyze.json | registry_rows 40, census 42, 16 failing rows + missing/extra/dupes | 8810a2850e83… |
| receipts/segments.json | per-segment token truth table for all 16 failures | 8854576838e5… |
| receipts/proposed-cells.json | all 16 repairs + 2 new rows, `all_pass: true` | 03082595d62c… |
| receipts/score-clause8.json | real `score()` v3 clause-8 on synthetic landing: `meaning_rows_failed 16`, `registry_missing [2]` | e4dd04b3719d… |
| receipts/score-clause8-repaired.json | same run with repairs: `meaning_rows_failed 0`, `registry_rows 42`, clause 8 green | 011afc239932… |
| receipts/forgery-probes.txt | seven forged/boundary cells through `meaning_classes` | 8270574da433… |

Commands: `python3` driving `tools/round-48/meanings.py` `{registry_rows, _segments,
meaning_classes, score}` against worktree `SKILL.md` and committed `census2.json`;
exit 0; full heredoc sources preserved in receipt files' generation transcripts above
(`analyze.json`, `segments.json`, `proposed-cells.json`, `score-clause8.json`,
`score-clause8-repaired.json` were produced by `score()`/`meaning_classes` directly —
frozen interpreter executed read-only, no file mutated). UTC 2026-10-28T18:54Z.

Exit codes: analysis runs exited 0 (success of measurement); the clause-8 score runs
returned receipt exit 1 (not met) as designed — `score-clause8.json` carries `"exit": 1`
because the pre-repair artefact has 16 failing rows.

Installs: none (stdlib + frozen lane tools only). `pacman` untouched.

## Out of scope / not run

- Whole-counter `--selftest` and the 4-forgery battery: not run (needs clone fixtures;
  sibling C1 seats own the battery). My clause-8 evidence runs `score()` directly, which
  is what clause 8 executes, minus the battery.
- `record2.py`/C2: not in this seat's scope.
