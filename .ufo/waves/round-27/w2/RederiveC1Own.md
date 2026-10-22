# R27 wave 2 seat: RederiveC1Own — independent re-derivation of all 16 R27-C1 rows

Seat: KaidokuR27.RederiveC1Own. Lane base cd32264f, claims frozen a4f674b, lane main
attacked at 4084d897 (rev-parse at 2026-10-22T15:36:16Z). Leaf: no subagents, no jobs.
No lane file edited; no lane counter code executed; no tools installed.

## Method (independent, no lane counter)

Own script `/fast/scratch/hyaku/kaidoku-r27/seats/w2/RederiveC1Own/rederive-c1.mjs`
(sha256 497cace2d3cb8093cf009e3d07bdf6d30ad7b96fe8251f927b986b485f49eb99). It reads
only `git show main:<path>` bytes for corpus/evidence/round-27/c1/{runs.tsv,table.tsv,
envelopes/*.json} plus the frozen rules in `.ufo/waves/round-27/claims.json` at a4f674b
(carriers, argv templates, frozen package pin parsed from `invocation`: 6.5.0 /
a5003023...). It applies the frozen R27-C1 rules: frozen TSV headers, one table row and
one run per (carrier, verb, base|repeat|renamed), path, argv template, exit 0, utc_start
no earlier than the commit that added the pinned counter (a4f674b, committer
2026-10-22T14:51:23Z; envelope first-commit checked per file), pkg_version and
pkg_json_sha256 frozen, envelope sha256 equal to file bytes and globally distinct across
all 48 runs, ok envelope, meta.command equal to the verb, evidence_id equal across
envelope/runs.tsv/table.tsv and recomputing under the 6.5.0 rule, subject sha256 equal
to the carrier, own path present and the row's other path absent in the envelope bytes,
subject.name equal to the run file name, and the verdict derivation (base!=repeat
unstable, renamed==base content-keyed, else rename-sensitive). ID recompute uses the
6.5.0 package's own JS from /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6: `digestCanonicalValue`
imported from dist/domain/canonicalDigest.js and `semanticProjection` lifted verbatim
from dist/domain/evidence.js source text and evaluated (never retyped); the package's own
`parseEvidence` authenticate gate is a second, independent check per envelope. The
installed package.json hashed to the frozen a5003023... before any import.

## Result: 15 of 16 rows re-derive complete; exactly one fails, only on shared bytes

Run: `node rederive-c1.mjs` (cwd above), 2026-10-22T15:41:06Z, exit 1, stderr empty.
Output excerpt (rederive-c1.out, sha256 d0254368976796e4994b666cc2d0f5ff722b28f908c240c1f25a56c657462c3c):

```
COMPLETE jq analyze [rename-sensitive]
COMPLETE jq inspect [rename-sensitive]
COMPLETE jq decompile [content-keyed]
COMPLETE jq xrefs [content-keyed]
COMPLETE jq read-bytes [content-keyed]
COMPLETE jq function [content-keyed]
COMPLETE jq instructions [content-keyed]
COMPLETE jq inspect-binary-layout [rename-sensitive]
COMPLETE tinyxxd analyze [rename-sensitive]
COMPLETE tinyxxd inspect [rename-sensitive]
COMPLETE tinyxxd decompile [content-keyed]
COMPLETE tinyxxd xrefs [content-keyed]
COMPLETE tinyxxd read-bytes [content-keyed]
COMPLETE tinyxxd function [content-keyed]
COMPLETE tinyxxd instructions [content-keyed]
INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: envelope_sha256 shared with another run
entry: ok (sourced by S082)
rows_complete=15/16 entry_ok=1 rev=4084d8975b684a8837b1c858eea0008ce9ab49e0
```

Per row: 15 rows COMPLETE with zero reason strings (every frozen check passed, including
48/48 id recomputes and 48/48 parseEvidence accepts); 1 row INCOMPLETE with exactly two
reasons, both the distinct-envelope-sha256 rule, on the same (carrier, verb) pair.
All 16 derived verdicts match table.tsv cells (no "table verdict" or "table id cells"
reasons). Observation; exit code 1 observed, not assumed.

## The counterexample (shared bytes)

Command, 2026-10-22T15:42:01Z, exit 0:
`git -C <lane> show main:corpus/evidence/round-27/c1/envelopes/tinyxxd-inspect-binary-layout-{base,repeat,renamed}.json | sha256sum`

```
base    f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130
repeat  f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130
renamed bbfbc309da6016f5ab0ffc21a4f624db9cf74f5ab7cfe923e24b23c12f9e929c
```

The base and repeat envelopes are byte-identical (same git blob 7a34b312 in ls-tree;
both meta.duration "132ms"), so runs.tsv carries the same envelope_sha256 twice and the
frozen rule "distinct envelope sha256 equal to the file bytes" refuses both runs of that
one row. The ids still re-derive (ev_aeeab0db... twice, renamed ev_02e910c6...), the
verdict rename-sensitive is correctly recorded, and jq's inspect-binary-layout base and
repeat bytes differ — the collision is specific to this tinyxxd pair.

## Verdicts

- R27-C1 claim statement at main (16/16 complete rows): FAILS, with the counterexample
  above. Observation.
- L1 report fidelity (15 of 16, entry_ok 1, exit 1 at 97358f75-reported logic, single
  failure only on the shared-bytes rule): CONFIRMED by independent re-derivation at
  main 4084d897. Observation.
- Exactly-one-row-fails and only-on-shared-bytes: CONFIRMED. No other row has any
  failing reason; the failing row has no other failing reason. Observation.
- ID identity under the package's own rule: 48/48 envelopes recompute to their stored
  evidence_id via imported digestCanonicalValue + verbatim semanticProjection, and the
  package's parseEvidence accepts 48/48 records. Observation. The content-keyed vs
  rename-sensitive split (5 verbs content-keyed, analyze/inspect/inspect-binary-layout
  rename-sensitive, both carriers) re-derives exactly.
- entry_ok: entry source: line names the table and S082 (new since base, mined, opened
  2026-10-22, in ## Gate); S079 named but present at base, correctly not counted.
  Observation.

## Residual risk and verification gaps

- Canonical JSON and digest come from the package's own implementation; the only second
  gate used is the same package's parseEvidence. A from-scratch canonicalizer would add
  redundancy but the round-26 corpus already exercised this rule; unknown residual:
  none observed.
- Carrier bytes at /usr/bin/jq and /usr/bin/tinyxxd were not re-hashed live; subject
  digests match the frozen claims' carrier sha256 (corpus-internal consistency only).
- Envelope first-commit-after-counter was checked per file inside the script (all 48
  passed; a failure would have surfaced as a row reason).
- The verdict is a recommendation only; this seat judged, did not integrate.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/w2/RederiveC1Own/)

```
497cace2d3cb8093cf009e3d07bdf6d30ad7b96fe8251f927b986b485f49eb99  rederive-c1.mjs
d0254368976796e4994b666cc2d0f5ff722b28f908c240c1f25a56c657462c3c  rederive-c1.out
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  rederive-c1.err
```
