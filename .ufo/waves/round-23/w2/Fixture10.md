# Fixture10: R23 C1 `wrong_command` source review

Candidate `2838351450ff1ee4baa620c962a1153450d53311` (chain `aa1450b → a3c92eb → 2b40aec → 6615aea → 2838351`). Baseline B `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Scope: `frozen/expected-v2.json` case `wrong_command`; `frozen/fixture.json`; the `wrong_command` branch of `tools/counter-fixtures.py`.
Method: static source trace of candidate bytes (`git show` / `git archive`, sha256 pins). Nothing executed: no selftest, no counter run, no clone, no mutation.
Labels: [O] observed in bytes or command output; [I] inferred from source trace, not executed; [U] unknown. Line numbers are candidate-tree lines unless a path is given.

## Verdict

- The expected values `{exit 1, count 1, finding c1_incomplete}` are correct against the candidate trace [I]. No wrong expectation found in this case.
- Positive-preserving [I]: `wrong_command` differs from `positive` by one string, `counter-fixtures.py:55`. The envelope stays `ok:true` with data and operation intact, so only the meta-equality rule can fire.
- Distinguishes the direct fault (a foreign `meta.command` credited under the entry verb): yes, by count only (2 → 1). Exit and finding do not move.
- Does not distinguish "credited to the envelope's declared verb" [I]. The foreign value `identify-flutter-build` is the one verb the baseline always witnesses, so crediting it can never change k. Round 22 used a non-catalog value (`'other'`); round 23 changed it (F3).
- `meta.command` laxity (absent, containment, case/underscore, debugger alias) is not represented anywhere in the frozen suite [I] (F4). Reclassifying the bind result 1 vs 2 is output-invisible [O] (F5).

## Findings

**F1. Expectation matches the source trace [I]**
- Expected: `frozen/expected-v2.json:53–57` = `{exit 1, count 1, finding c1_incomplete}`. `expected.json` and `expected-v1.json` are byte-identical to each other (sha256 `ad1b4462…`) with the same values at lines 53–57.
- Trace: default selection `counter-fixtures.py:38` (`inspect-signal-decoders`). Mutation `:54–55` sets `meta.command='identify-flutter-build'`. Envelope written `:64–69`; entry line `:70` = `inspect-signal-decoders <ev_5555…> .ufo/waves/round-23/evidence/c1/inspect-signal-decoders.json`.
- Eligibility `tools/count-c1.py:104–110` passes: the injected S058 row is `A`/`mined`/`2026-10-21` with used-by = ENTRY. Baseline S-rows end at `corpus/SOURCES.md:63`, `## Paths` is at `:65`, and the injected row lands after the last S-row, so the `historical_sources_changed` prefix check in `measure` holds.
- Bind: `count-c1.py:119–123` → `bind_new` (`:42–56`). The refusal walk finds nothing; `:54` → `round-22/tools/count-c1.py:79–80` (`meta.get("command") != verb` → `return 1`). Not credited (`:123`).
- Historical: `count-c1.py:82–83` pins the baseline set to `['identify-flutter-build']`; `:92–93` and `:126–127` make `held == ['identify-flutter-build']`; `:128–130` finding `c1_incomplete`; `:166` exit 1. Matches.
- Positive (`cases.positive` = `{exit 1, count 2}`): same path, but `round-22 count-c1.py:96` → `round-21/tools/verb-coverage.py:99` returns 0, so the witness is credited and count = 2.

**F2. Positive-preserving isolation [O]**
- Each case deep-copies its documents (`counter-fixtures.py:37`), so the mutation cannot leak into other cases.
- The mutated record keeps `ok:true` (the refusal walk at `count-c1.py:52` does not fire), keeps `data.evidence_id`, and keeps `data.operation` (`round-21/tools/verb-coverage.py:88` matches). The count delta is therefore attributable only to the meta-equality rule.
- The builder imports stdlib only (`counter-fixtures.py:7–13`). Expectations come from `manifest['cases']` (`:33`) and are compared at `:111–112`; they are not computed in the builder.

**F3. Weak mutation: credit to the declared verb is masked [I; not executed]**
- `identify-flutter-build` is always held. `count-c1.py:82–83` forces the baseline set to exactly identify, and `:126` marks it exercised regardless of `new`. Any credit to identify leaves k = 1 and the finding unchanged.
- Mutant C_declared (drop the meta-equality check; bind against the entry verb; credit the envelope's declared verb): `wrong_command` still yields 1 and passes. Across the 21 cases, only `wrong_command` has declared ≠ entry verb with a successful entry-verb operation bind (`wrong_operation` fails that bind at `round-21/tools/verb-coverage.py:88,96`). C_declared is expected to survive the whole frozen suite.
- `wrong_operation` (`counter-fixtures.py:56–57`) uses the same held verb as its foreign operation, so a credit-by-operation mutant also survives it.
- Provenance [O]: round 22 used `record['meta']['command'] = 'other'` (`round-22/tools/counter-fixtures.py:119–120`). Round 23 `frozen/counter-fixtures-v1.py:54–55` changed it to `identify-flutter-build`; unchanged in `tools/counter-fixtures.py:54–55`. W1 `w1/ReviewEvidenceBinding.md:17` cites the round-22 lines as the existing wrong-command control without noting the change. A pattern search of `w1/` for "wrong command", "foreign", and "other" found no rationale for the identify value.
- Repair, not applied: use a non-held catalog verb such as `decode-signal-recording` (template at `frozen/fixture.json:71–72`). Expected stays `{1, 1, c1_incomplete}`; C_declared then counts 2 and is caught. `tools/counter-fixtures.py` (sha256 `f2990b35…`) and `expected-v2.json` (sha256 `458b30d5…`, pinned at `count-c1.py:25`) are hash-pinned, so this needs a re-frozen manifest, not an in-place edit.
- Related gap [I]: a bind-by-declared-verb mutant (binds against the declared verb, credits the entry verb) is not caught, because the wrong_command envelope is not self-consistent for its declared verb (operation stays `inspect_signal_decoders`). Catching it needs a second control: a self-consistent foreign envelope (declared verb and operation both non-held), cited under the entry. Correct result 1; mutant 2.

**F4. `meta.command` laxity survives the frozen suite [I]**
No case omits `meta.command` or varies it except the single foreign string at `counter-fixtures.py:55`. These mutants pass every case by trace:
- absent-default (`meta.get('command', verb) != verb`): no case omits `command`.
- containment or prefix (`verb in meta`, `startswith`): `'inspect-signal-decoders'` is not a substring of `'identify-flutter-build'`, so wrong_command rejects. The positive is exact, so it passes.
- case or underscore normalization: no variant case exists.
- debugger alias accepted (`gdb-console` or `rizin-debug-command` as `meta.command` for `debug-with-*`): no negative case; `all_six` uses catalog names only.
- Policy: exact hyphen equality (`w1/CounterSources.md:159`). The candidate's exact check (`round-22/tools/count-c1.py:79`) is policy-correct; the suite simply does not pin it. Whether debugger envelopes carry the catalog name or the alias is unobserved (`w1/ReviewEvidenceBinding.md:19`) [U].

**F5. 1 vs 2 bind classification is output-invisible [O]**
`count-c1.py:123` credits only on `== 0`. Refused (1, `round-22/tools/count-c1.py:80`) and unevaluable (2) look the same to the count. Exit stays 1 and the finding stays `c1_incomplete` either way, so a mutant that changes meta-mismatch from 1 to 2 passes `wrong_command`. This is W1 `w1/CounterRefusals.md:232` (N10), still open at the candidate.

**F6. Vacuity dependence [I]**
A build that never credits `inspect-signal-decoders` also yields 1 here. The case discriminates only together with `positive` (expects 2). That pairing is the correct design, not a wrong expectation.

**F7. Oracle independence [O]**
- Template: `frozen/fixture.json` (sha256 `a1f5aff8…`). The `inspect-signal-decoders` block is at `:56–60` (`meta.command` at `:59`), and `normalized_result.control` is marked synthetic.
- Expectations are frozen in `expected-v2.json`. `count-c1.py:138–139` checks its pin; `:142–144` checks the input pins for `counter-fixtures.py` and `fixture.json`.
- Round 22 computed expectations inline (`round-22/tools/counter-fixtures.py:152–153`); round 23 moved them to the frozen manifest. This is an improvement.
- No generator for `expected-v2.json` was found. I searched `gen-wave1.py`, `gen-wave2.py`, `verify.py`, and `predictions.json`; predictions cover signal decoding only. A full-tree search was not performed [U].

**F8. W1 items re-evaluated at 2838351**
- `w1/CounterRefusals.md:103` (meta.command mismatch → 1): holds (`round-22/tools/count-c1.py:79–80`, `count-c1.py:54`).
- `w1/CounterRefusals.md:232` (N10, reasons collapse): still open (`count-c1.py:123`).
- `w1/CounterRefusals.md:244` (N17, hyphen-only command token): resolved; `count-c1.py:120` uses `r20.command_pattern`.
- `w1/CriticSeparation.md:15` ("counter-fixtures writes only under the round-23 prefix"): stale. Round-23 v2 writes `.ufo/waves/round-22/…` and `round-20/…` paths inside the disposable clone (`counter-fixtures.py:88–99`, git add list `:100–102`).
- `w1/ReviewEvidenceBinding.md:19` (debugger meta form unknown): still unknown at the candidate.

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture10.md` (this report).
- Candidate pins (observed via `git show <rev>:<path> | sha256sum`):
  - `tools/count-c1.py` `f4b8d16a…`; `tools/counter-fixtures.py` `f2990b35…` (manifest input); `frozen/fixture.json` `a1f5aff8…` (manifest input); `frozen/expected-v2.json` `458b30d5…` (equals `count-c1.py:25`).
  - `frozen/expected.json` = `frozen/expected-v1.json` `ad1b4462…`; `frozen/counter-fixtures-v1.py` `96e65034…`.
  - `round-22/tools/count-c1.py` `c925918f…` (equals `LEGACY_SHA256`); `round-22/tools/counter-fixtures.py` `f90be315…`.
  - `round-21/tools/verb-coverage.py` `61536938…`; `round-20/tools/verb-coverage.py` `cfbf1880…` (equal the round-22 helper pins).
  - `corpus/SOURCES.md` blob: `aa1450b` `d80ed12d…` vs `2838351` `daf5ce02…`; `git diff --stat` shows 6 insertions across `a3c92eb..2838351` (S058–S061 rows and one search-log line). The fixture base `aa1450b` excludes them.
- Private extracts under `.ufo/waves/round-23/runtime/Fixture10/` (ignored) were removed after review.

## Installs or none

None. Read-only git only (`cat-file`, `show`, `archive`, `rev-parse`, `diff`, `ls-tree`), `tar` into my ignored runtime directory, `sha256sum`, and one read-only `python3 -c` key listing of the candidate manifest. No pacman, uv, npm, or cargo activity. No git writes.

## Open risks

- Harness exit ambiguity: `counter-fixtures.py:26–27` raises `RuntimeError` on any git failure. `count-c1.py:167` does not catch it, so the run prints a traceback and exits 1 with no JSON. Exit 1 alone cannot separate a failed case from a crash.
- Repairing F3 requires re-freezing (new `counter-fixtures.py`, a new manifest, and a new pin at `count-c1.py:25`). Decision for L1: re-freeze before the verdict, or record F3 and F4 as open.
- The candidate SOURCES chain adds real S058–S061 rows. This case is isolated by `frozen/fixture.json:2` (base `aa1450b`). Production counts at the candidate read those rows; that is outside this item.
- F3–F5 are source-trace inferences. A mutation seat would be needed to confirm survival.
