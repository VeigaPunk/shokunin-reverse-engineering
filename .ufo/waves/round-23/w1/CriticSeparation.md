# R23-C1 critic — separation (coverage claim vs incidental depth/calibration; historical/new root union)

Seat: KaidokuR23.CriticSeparation (critic, read-only, author-side). Not verification.
Lane HEAD observed: `a3c92eb6bc70984e90ae5b895412de978840b2c5`; baseline B `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Working-tree state at review time (observed `git status --porcelain`): only untracked `.ufo/waves/round-23/{.gitignore,evidence/,frozen/,tools/,predictions.json,...}`; no corpus/README/PROVINCE/SKILL/SOURCES edits yet. Doc-preservation findings below are therefore prospective.

All commands were read-only `git show`/`git ls-tree`/`sha256sum`/inline `python3 -I -B` reads, exit 0. I did not run any REA probe, counter, selftest, build, or test.

## Findings

### F1 — HIGH: the historical root is an unpinned backdoor for new verbs (counterexample)
- Observation: `tools/count-c1.py:54-56` runs the legacy `measure` with `EVIDENCE_PREFIX=.ufo/waves/round-22/evidence/c1/`. Then `:78`/`:85` counts `historical = scans[0]...bound_evidence` with no further condition.
- Observation: legacy eligibility admits any row with id ≥51 that is A/B, `mined`, `2026-10-21`, and names the entry in used-by (`.ufo/waves/round-22/tools/count-c1.py:129-142`). The new R23 S058+ rows carry the same date (`claims.json` declared 2026-10-21), so they pass that filter.
- Counterexample (inference from code; not executed): add `.ufo/waves/round-22/evidence/c1/X.envelope.json`, a bound non-refused `inspect-signal-decoders` envelope. Add a new entry with `source: S058` that cites that path and evidence id, plus a matching S058 used-by. The legacy scan of the round-22 root binds it, and the wrapper counts it as `historical`. The new-witness rule (S058+, round-23 path) is never applied. This defeats claim text "new evidence only under round-23/evidence/c1".
- Observation: the selftest has no such case. `frozen/expected.json` cases are positive, all_six, same_verb, mention_only, missing_source, old_source, wrong_usedby, refused_parent, nested_refusal, wrong_command, wrong_operation, duplicate_member, helper_tamper, invalid_utf8. `tools/counter-fixtures.py:45,59` only ever writes under the round-23 prefix.
- Only external tripwire: the no-harm check "R22 C1=1/6 at final". The R22 counter would read 2/6 in this scenario. The R23 counting command alone does not catch it.
- Axes: coverage (false k), claim/no-harm separation.
- Smallest correction: pin the historical witness set as constants. Use the observed B set from `before-r22-c1.json`: `(identify-flutter-build, ev_6a84742a…b6, round-22/evidence/c1/identify-flutter-build-saber.envelope.json)` and `(identify-flutter-build, ev_3458b996…6b, round-22/evidence/c1/identify-godot.envelope.json)`. Compare the set of `(verb, eid, path)` from `scans[0]` against it: use set equality, not list equality, because new entries may legitimately re-cite historical envelopes and repeat pairs. On mismatch, exit 2 with finding `historical_root_changed`. Add a fixture case `historical_root_injection` (expected exit 2).

### F2 — HIGH: union-by-verb hides "inherited identify lost" (counterexample)
- Observation: `count-c1.py:85` sets `exercised = bool(historical or current)`. Finding and exit depend only on the count (`:87-88`, `:125`).
- Counterexample: the R23 work produces a new identify-flutter-build witness, and the R22 witness is lost (R22 entry edited or removed, or its S05x row altered). Count and exit stay exactly the same. Only the `targets.identify-flutter-build.historical == []` field shows the loss, and no predicate reads it. The claim lists "inherited identify lost" as a falsifier, but no fixture covers loss-with-replacement. `same_verb` only covers duplication.
- Axes: coverage, preservation.
- Smallest correction: the F1 pin covers this too. Missing historical pairs means `historical_root_changed`, exit 2. Add fixture `inherited_lost_replaced`: delete the R22 entries, add a new identify witness, expect exit 2.

### F3 — MEDIUM: "original-envelope" in the claim target is not measured by the counting command
- Observation: the claim target reads "cumulative sourced original-envelope bound held count" (`claims.json` R23-C1 `target`). The legacy docstring says "The original envelope is not compared with run.stdout by this counter" (`round-22/tools/count-c1.py:15-16`). The R23 wrapper adds no such comparison, but its `limit` string (`count-c1.py:92`) still says "local original-envelope/source linkage". R22 did this comparison in a separate final check (`round-22/verify.py:154-180`).
- Observation (fact check, read-only): the five present round-23 `*.envelope.json` files all have `run.stdout == envelope bytes`. Their verbs and run exits match the envelopes: `inventory` and `uart-help` are inspect-signal-decoders ok, `decode-uart-hi` and `decode-official-uart` are decode-signal-recording ok, `decode-invalid-decoder` is `ok:false execution_failure`, exit 1. Each records `env_overrides.REA_SIGROK_COMMAND=.ufo/waves/round-23/tools/sigrok-cli.sh`.
- Risk if L1 reuses the R22 pairing rule unchanged: `verify.py:155-157` maps every `*.run.json` under `/c1/` to `*.envelope.json`. `evidence/c1/generate-uart.run.json` has no envelope (it is a producer run, not REA), so that rule would report a spurious provenance failure. A rule that skips missing envelopes would hide real gaps.
- Axes: coverage (attribution of the qualifier), calibration (limit text overstates the measurement).
- Smallest correction: either compare `run.stdout` to the envelope inside the counter for every counted round-23 witness (and fail otherwise), or reword `limit` to "envelope/source linkage; original-envelope equality checked separately". L1's final check must then pair only REA runs, by `argv` containing `rea-agents@6.5.0`, not by filename.

### F4 — MEDIUM: incidental depth through SKILL.md and live fixed citations
- Observation: the depth scalar is computed by `.ufo/waves/round-21/controls.py:64-75`. It counts `- **` rule bullets in `SKILL.md` `## Queue-drain craft ` up to the next `\n## `, and checks that each rule's `corpus/knowledge/...:N-M` refs resolve. Read-only recomputation at B: 17 rules, depth 17/17. SCORECARD:24 still describes this proxy as "9/9" and `SKILL.md:77-191`, which is stale prose. R22 reported "citations17/17".
- Counterexample: R23 adds a rule bullet citing a new r23 entry anywhere in SKILL.md:81-318 (craft section ends before `## Config custody`, line 319). Depth goes 17/17→18/18. That is an undeclared depth move, even though the score stays 10.0. A bullet without a resolvable range drops depth below 10, and controls fails (`controls.py:86` requires `depth_score>=`).
- Live head citations that a mid-file SKILL insertion would shift (observed resolving at HEAD):
  - `corpus/lessons/round-17.md:82` cites `SKILL.md:448`/`:449`, which are currently the citation-drift and custody-pair rows.
  - `SHONEN.md:6` cites `SKILL.md:81-314`.
  - `corpus/README.md:140` cites `SKILL.md:81-195`.
  - `corpus/knowledge/2026-10-14-r14-02-final-sweep.md:47,106,165` cites `SKILL.md:77-191`, `:69`, and `:48`.
- `controls.py:80` checks byte preservation only for `round-20` waves, `corpus/knowledge/`, and `corpus/lessons/`. It does not cover `SKILL.md` or `PROVINCE.md`.
- Axes: depth (incidental), map/citation integrity.
- Smallest correction:
  - Put every R23 SKILL text and any counter-registry row after current EOF (706 lines), in a new `## … round 23` section, or append to the end of `### Round-22 measurement registry` (which is at EOF).
  - Add no `- **` bullets inside the craft section.
  - Check that final `SKILL.md` starts with the bytes of B's `SKILL.md`.
  - Report depth as 17/17→17/17.

### F5 — MEDIUM: incidental calibration through PROVINCE.md and the R22-C2 section
- Observation: R22-C2 parses only `### Round-22 catalog dispositions` up to the next `#` line (`round-22/tools/count-c2.py:40,102-121`). It reports any verb outside T2 as `foreign_rows` (`:206-208`), and R22 verify requires `not foreign_rows` (`round-22/verify.py:75`). The section is PROVINCE.md:173-204.
- Counterexamples:
  - Adding a "held" or "refused" row for `inspect-signal-decoders`, `decode-signal-recording`, or `decode-invalid-decoder` into that table makes C2 `dispositions_incomplete` (harm to "C2=14/14 at final").
  - Moving sigrok verbs into `## Core` (38-72), or titling the R23 section "additions to Core" (as R20 did at :164), is an undeclared capability/promotion claim. `not_claimed` and LOG forbid it.
  - Editing PROVINCE.md:216-217 ("The sigrok verbs remain unexercised…") rewrites a true historical R22 statement.
- Observation: the `decode-invalid-decoder` refusal envelope is calibration-type material (a named gap). Using it as a disposition receipt or a calibration claim would be undeclared calibration work. It belongs only as a negative control inside the knowledge entry.
- Axes: calibration (incidental), capability/promotion.
- Smallest correction:
  - Append a new `### Round-23 …` heading after the current EOF (PROVINCE.md 218 lines).
  - Check that final PROVINCE.md starts with B's bytes.
  - Leave the R22 sections untouched, and do not add rows to the R22 disposition table.

### F6 — MEDIUM: coverage scalar vs claim numerator; mention denominators
- Observation: the coverage scalar is README Coverage-map integrity (`controls.py:59-63,75`; SCORECARD:23 "index integrity only"). Recomputed at B: 104 knowledge files, 104 mapped, 0 dangling. The mapping regex reads only `## Coverage map` (README:11 to `## Knowledge` at :72). A row added only to the `## Knowledge` table (as at :157-158) does not map the entry. Score becomes 104/105, which is harm, and controls fails.
- A Coverage-map row naming a candidate stem that has not landed (DraftSignalEntry is "candidate") makes the map dangling. R22 verify required no dangling entries (`verify.py:129-130`).
- Observation: lexical catalog mentions at B are `catalog_mentioned_count` 135/153 and `catalog_zero_count` 18 (`before-r22-c1.json` stdout). The ConnectCounters seat prompt (`wave1-spec.json`) uses "133/153", which was the R22 baseline (20 zero at 7787fea), so it is stale.
- Any R23 prose saying "debug-with-gdb/rizin remain Adjacent" lowers `catalog_zero` without holding anything. `count-c1.py:90-91` emits these fields with no lexical label.
- Axes: coverage (scalar vs claim confusion), calibration (stale denominator).
- Smallest correction:
  - Report three separate quantities: T1 held k/6 (claim), map N/N→N+n/N+n with scalar 10.0→10.0 (integrity), and catalog mentions 135/153 at B (lexical, not held).
  - Add `"catalog_fields": "lexical knowledge mentions, not holdings"` to the counter's `limit` string.
  - Map every landed r23 stem inside `## Coverage map`.

### F7 — LOW: the wrapper's attribution regex differs from the legacy citation regex (undercount only)
- `count-c1.py:82` paths regex has no `.rstrip('.')`. Legacy `cited_prefixes` strips the trailing dot (`round-20/tools/verb-coverage.py:127-129`).
- `count-c1.py:83` verb regex accepts only the hyphen form. Legacy `command_pattern` also accepts `_` (`verb-coverage.py:99-103`).
- An entry citing `…/inventory.envelope.json.` (sentence period, no backticks) or naming `decode_signal_recording` binds under legacy but is dropped as a new witness. This is the safe direction, but it can falsely report a verb as unheld.
- The 5-witness truncation (`round-22/tools/count-c1.py:168`) is already documented at `count-c1.py:5-7`.
- Correction: reuse legacy `r20.cited_prefixes` and `command_pattern` semantics, or wrap paths in backticks in entries.

### F8 — LOW: measurement side effects and the instrument change between before and after
- `count-c1.py:46-48` creates `<root>/.ufo/waves/round-23/runtime` and sets the global `tempfile.tempdir`, so the counting command writes to the measured lane. `.gitignore` (`/runtime/`, `/worktrees/`) is still untracked. If it is not committed with the tools, `runtime/` could be committed.
- `before: 1` was measured with the R22 counter (`before-r22-c1.json`), not with the frozen R23 counting command, which was absent at `a3c92eb`. The R23 wrapper loads the legacy file from `--rev`. Its sha `c925918f…1879` is identical at B, at HEAD, and in the worktree (observed), so `--rev B` is evaluable.
- Correction: L1 records R23-counter output at B (expected 1/6, `new` empty) before the after-measurement, commits `.gitignore`, and states that the before/after instrument differs from R22.

### Preservation checks that hold or are neutral (observed)
- `round-22/tools/count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` is the same at B, HEAD, and the worktree, and matches `count-c1.py:23` `LEGACY_SHA256`.
- `controls.py` sha256 `1bcdb772…2ec0`; `count-c2.py` sha256 `ace81241…75b0`.
- S051–S057 used-by name only the two R22 knowledge entries and `corpus/lessons/round-22.md`, all present at B. While those rows stay byte-identical, a new entry can be eligible only through an S058+ row. Exception: the text-keyed `eligible` set (`round-22/tools/count-c1.py:142,161`) also admits a byte-identical copy of an R22 entry. That copy can only cite round-22 paths, so it is benign under F1's pin.
- Cross-verb leak: none. Legacy `bind` requires the record `operation` to equal the bound verb (`round-21/tools/verb-coverage.py:85-88`), so a mention like "debug-with-gdb remains Adjacent" next to a decode envelope cannot bind gdb-console.
- The R22 Dart refusal envelope has `ok:false` and no `data` record (observed), so it cannot be re-wrapped as a positive. `run.stdout` equals the envelope for both R22 Saber envelopes (observed).
- "102 reportless" in claims.json/LOG equals R22 W1 93 (causes unknown per child) plus W2 9 (named provider failures) (`round-22/final-wave-outcomes.json`). DraftMistake's "reportless93 W1" is scoped to W1 and is consistent. The claim must not merge the 9 known causes into "unknown".

## Impacted axes
- Coverage: F1, F2 (false or masked k), F3, F6, F7.
- Depth (incidental): F4.
- Calibration (incidental): F3 limit text, F5, F6 stale denominator.
- Preservation/no-harm: F1, F2, F4, F5, F8.

## Smallest safe correction set (for L1; not applied by this seat)
1. In the counter, pin the B historical `(verb, eid, path)` set and use set equality. On mismatch, exit 2 `historical_root_changed`. Add fixtures `historical_root_injection` and `inherited_lost_replaced`. Re-freeze `frozen/expected.json` and its digest pin (F1, F2).
2. Make the counter's `limit` text honest about the original-envelope comparison and catalog lexical fields. Pair REA runs by argv in the final check (F3, F6).
3. Run append-only prefix checks for `SKILL.md` and `PROVINCE.md` against B, alongside `round-21/controls.py --before B --after V`. Add no craft-section bullets and no rows to the R22 disposition table. Add r23 stems only to `## Coverage map` (F4, F5, F6).
4. Report k/6, map, depth 17/17, catalog mentions 135/153, R22-C1 `t1_exercised==['identify-flutter-build']`, and R22-C2 14/14 with `foreign_rows==[]` as separate quantities. For the R22-counter no-harm check, compare the count and `bound_evidence` only. `entries`/`catalog_*` will legitimately change with R23 mentions (F6).
5. Record R23-counter output at B and commit `.gitignore` (F8).

## Produced files
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CriticSeparation.md` (this report; its sha256 is reported in the seat's final message because a file cannot contain its own digest).

## Installs
None.

## Open risks
- F1/F2 are code-path inferences. I did not execute fixture clones for them; L1 must reproduce them with the proposed fixtures.
- The sigrok wrapper `tools/sigrok-cli.sh` sets `LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0`, a mixed bundle/host ABI. The decode envelopes depend on this environment. Whether that environment and ownership is in scope is for CriticScope/SentinelBoundary; I did not assess it.
- Source relevance and ownership of the S058+ rows is not reviewed here.
- The doc-preservation findings (F4–F6) are prospective; no corpus edits existed at review time.
