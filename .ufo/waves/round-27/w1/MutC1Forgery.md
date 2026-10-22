# Round 27 wave 1 — MutC1Forgery (mutation tester)

Attacks: the pinned R27-C1 counter `tools/round-27/c1-rename-identity.py` for forged envelope
sets (round-26 lesson M26-5 class). Greenhouse: the counter's own `--selftest` green fixture
(`_build_green` reused verbatim), cloned per mutant inside the sandbox clone
`/fast/scratch/hyaku/kaidoku-r27/seats/MutC1Forgery/clone`. Every mutant is committed in its own
clone and the counter runs on that clone's HEAD with `--root <mutant repo> --rev HEAD --base <green base>`.
Baseline: pristine green exits 0 with `rows_complete=16/16 entry_ok=1` (verified).
Positive controls: m16 (whitespace inside a hashed field) killed by the recompute rule; m18
(envelopes first committed before the counter) killed by the envelope-commit-time gate.
Pristine green bytes unchanged after all runs (snapshot sha identical), counter file bytes untouched
(sha256 e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7).

Execution: `python3 -I -B mutate_c1.py` at 2026-10-22T15:09:39Z (and one earlier pass at
T15:03:06Z). All outputs archived under seats/MutC1Forgery (scripts `mutate_c1.py`
sha256 2187084c5b85ede302dfbda91caa5d31e8551742527d90bff6a674b21de1d6a2, `summary.json`
sha256 c17e557edf92aa92577d8842d8941a17ea6813749b6d7a091396ce5d614c6419; per-case
`counter-output.txt` under `clone/mutants/<case>/`).

## Table

| # | mutant | expected vote | counter verdict | exit | result |
|---|---|---|---|---|---|
| green | pristine fixture | — | `rows_complete=16/16 entry_ok=1` | 0 | baseline |
| m01 | jq envelope reused as tinyxxd base, sha resynced | refuse | `INCOMPLETE tinyxxd analyze: base: envelope_sha256 shared with another run; ... subject sha256 not the carrier; ... envelope does not contain its run path; ... subject.name 'jq' ...` | 1 | killed |
| m02 | jq renamed envelope taken from tinyxxd, sha resynced | refuse | `INCOMPLETE jq analyze: renamed: envelope_sha256 shared with another run; ... subject sha256 not the carrier; ... subject.name 'tinyxxd-r27-renamed.dat' ...` | 1 | killed |
| m03 | runs.tsv line duplicated with new seat name | refuse | `INCOMPLETE jq analyze: base: runs.tsv has 2 lines` | 1 | killed |
| m04 | envelope extra whitespace (trailing `\n\n   \n`), sha resynced | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m05 | envelope compressed as `.json.gz`, `.json` removed | refuse | `INCOMPLETE jq analyze: base: corpus/evidence/round-27/c1/envelopes/jq-analyze-base.json absent` | 1 | killed |
| m06 | table.tsv row duplicated | refuse | `INCOMPLETE jq analyze: table has 2 rows` | 1 | killed |
| m07 | extra table row for unknown verb `disassemble` | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m08 | hashed field (`authority`) edited, id recomputed, runs/table resynced | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m09 | `subject.name` removed | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m10 | recompute rule file `tools/round-26/recompute-ids.py` rewritten at REV, all ids forged consistently | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m11 | runs.tsv `utc_start` set to 2027-01-01 | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m12 | extra runs.tsv row for unknown verb `disassemble`, unique sha | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m13 | whole envelope set hand-written (fabricated), honest ids | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m14 | envelopes committed in the same commit as the counter | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m15 | extra runs.tsv row with run name `extra` for jq/analyze | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |
| m16 | whitespace inside a hashed field, id not recomputed | refuse | `INCOMPLETE jq analyze: base: evidence_id does not recompute under the 6.5.0 rule` | 1 | killed (control) |
| m17 | runs.tsv header column renamed | refuse | `input error: runs.tsv header differs from frozen header` | 2 | killed (error) |
| m18 | envelopes first committed before the counter commit | refuse | `INCOMPLETE ...: envelope first committed before the counter` | 1 | killed (control) |
| m19 | `data.operation` says `inspect`, row verb `analyze`, ids recomputed, resynced | refuse | `rows_complete=16/16 entry_ok=1` | 0 | **survived** |

## Survivors — do they make R27-C1 false?

- m13, m08, m19: yes, in substance. R27-C1 is a learning claim: the table's 16 verdicts
  re-derive from three committed envelopes *produced by rea-agents 6.5.0 at the pin*. All three
  mutants hand-edit or fully fabricate the envelope data while keeping every counter rule satisfied
  (id recomputed under the honest rule, sha resynced, path present, subject digest = carrier sha,
  meta.command = verb). m19 additionally shows the hashed `data.operation` is never bound to the
  row's verb (real envelopes: `meta.command` = CLI verb, `data.operation` = provider operation,
  e.g. `analyze`→`binary_overview`), so the behavior "identify the verb" is only a word in the
  table. A green counter therefore cannot certify the envelopes are REA output; the claim's
  evidence identity is not established.
- m10: yes. The counter reads the id rule from `tools/round-26/recompute-ids.py` **at REV**
  (mutable), while only the counter file itself is sha256-pinned in claims.json. Rewriting the rule
  file at the data commit makes the recompute check vacuous (any id passes). Green then evidences
  nothing about the 6.5.0 rule.
- m14: partial. The envelope first-commit gate only rejects envelopes committed *before* the
  counter commit; same-commit (counter + data committed together) passes. It deforms the
  instruments-first freeze the claim relies on, though this round's real lane cannot hit it
  (counter frozen at a4f674b3 before any data).
- m07, m12, m15: no (literal statement "one complete row for each of 16 frozen pairs" still
  holds), but the corpus can carry unbacked rows/run records: an extra table row asserting a verdict
  for a verb with no envelopes, and extra runs.tsv rows describing runs that never happened. These
  are unsupported assertions committed into the evidence corpus.
- m04: no. Only byte-level formatting differs; parsed JSON and every derived fact identical. The
  counter cannot detect, but no claim content changes.
- m09: no. `subject.name` is not in the hashed projection (projection = subject digest/format/
  architecture), so removing it changes no id or verdict. Minor divergence: the counter's docstring
  checks name only "when present", while claims.json's rule list states "subject.name equal to the
  run's file name" unconditionally.
- m11: no, alone. `utc_start` is self-asserted text; the counter only enforces a lower bound (>= 
  counter commit). A future timestamp is nonsense but does not by itself change verdicts; it
  signals the timestamp gate is decorative for anti-backdating (the real anchor is the envelope
  first-commit git time, which works).

## Proposed gates

1. Pin `tools/round-26/recompute-ids.py` by sha256 inside the counter (constant, like
   `PKG_JSON_SHA256`) and refuse if the bytes at REV differ; or load the rule from the counter's own
   commit instead of REV. (kills m10)
2. Require `data.operation` to equal the VERBS key for the row (and optionally require
   `data.parameters.target/path` == the run path for the verbs whose real envelopes carry it).
   (kills m19; hardens m08/m13)
3. Require `subject.name` present and equal to the run's file name (drop the "when present"
   allowance). (kills m09)
4. Require table.tsv to contain exactly the 16 frozen (carrier,verb) rows (no extra rows), and
   runs.tsv exactly the 16×3 frozen triples (no unknown verb or extra run-name rows). (kills m07/
   m12/m15)
5. Require `utc_start` ≤ envelope first-commit time and ≤ now (upper bound), so the run timestamp
   cannot float into the future or detach from the commit record. Also require the counter commit to
   be strictly before each envelope's first-commit time (kills m14 by making equality fail).
6. Envelope authenticity (m13/m08) is not recoverable by any file-only structural counter. The only
   principled gate is re-execution: re-run the pinned 6.5.0 verb per pair at check time and compare
   the recomputed evidence id (round-26 shows base/repeat ids are reproducible), or seal a receipt
   at run time that an independent party verifies. Recommend an explicit claim-limits note that the
   counter certifies internal consistency + provenance-by-commit, not that the CLI was invoked.

## Bounds compliance

No lane files edited except this report. No git writes in the lane (mutations happen in the
sandbox clone and green copies). Read-only git used for the lane. No new tools installed.
Sources opened: lane files read locally (claims.json, counter, recompute-ids.py, round-26 lesson,
round-26 envelopes); installed 6.5.0 package read at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` (access 2026-10-22).
Quotes: counter docstring "each envelope's sha256 equals runs.tsv envelope_sha256, and all 48
differ"; round-26 lesson "The C1 counter accepts forged envelope sets (M26-5)"; real envelope
`{ "meta": {"command": "analyze"}, "data": {"operation": "binary_overview"} }`.
