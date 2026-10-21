# ReviewRegistryHome — w1, round 23 — SKILL gate registry row fields and proposed cumulative gate entry

Scope attacked: (a) the inherited registry row for the R22 C1 counter (SKILL.md "Round-22 measurement registry") checked field-by-field against the actual gate code; (b) the declaration side — the proposed R23 cumulative gate entry (`count-c1.py`, claims.json R23-C1 + wave1-spec BuildCounter task) checked against the house registry-row conventions: codes 0/1/2, self-invocation, frozen input digest, scope/owner. Author-side review, not outside verification.

Labels: [O] observation (read/computed), [I] inference, [U] unknown.

## Registry row field conventions (inherited side)

[O] The canonical row shape is five columns — `Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope` — uniform across the top-level registry (SKILL.md:445), per-round sections (SKILL.md:681), with a section preamble scoping all rows away from REA correctness / outside review / canonical judgment / fleet acceptance (SKILL.md:440-443). Owner token is uniformly `gate / kaidoku` or `probe / kaidoku`.

[O] The direct ancestor row, SKILL.md:683 (round22-C1, gate / kaidoku), verifies against its code on every claimed field:

| Row claim | Evidence | Verdict |
|---|---|---|
| `0 c1_complete/all six, 1 c1_incomplete, 2 unevaluable` | count-c1.py:174-176 sets finding from 6-verb comparison; `main` returns 0 only when `t1_exercised_count == t1_total`, else 1; exceptions print `unevaluable` and return 2 | holds [O] |
| `--selftest` (optional `--root <LANE>` for a relocated executable); 0 clean / 1 failed / 2 snapshot_tampered/unevaluable | count-c1.py selftest branch: root defaults to parent-walk for the fixtures file, `--root` overrides; manifest/input digest mismatch → `snapshot_tampered`, 2 | holds [O] |
| `frozen/expected-v2.json` (manifest SHA constant in script) | `SELFTEST_MANIFEST_SHA256` = `1abdd9df3476…`; computed sha256 of `.ufo/waves/round-22/frozen/expected-v2.json` = `1abdd9df347610a77f01afbe157c7fdbfb4c90bc2e26b6b3ecebd08fbd930bb8` — equal | holds [O, computed] |
| fixture program and dependency hashes authenticated | `expected-v2.json` `inputs` includes `counter-fixtures.py` (`f90be315…`), both verb-coverage helpers, and one r20 verify artifact; the selftest digests each input before loading | holds [O] |
| reviewed helper hashes in `frozen/helper-hashes.json` | file's sha256 values for r20/r21 `verb-coverage.py` equal the script's `HELPER_SHA256` constants (cfbf1880…, 61536938…) | holds [O, computed] |
| No live-tree write; removed private Git fixtures only | counter-fixtures.py `run()` builds both fixture repos inside one `tempfile.TemporaryDirectory(prefix='kaidoku-r22-fixtures-')` with `git init`; helper bytes mutated then restored; directory removed on exit | holds [O] |
| aliases from S056 | `CLI_BIND_VERB` maps only the two debugger verbs to `gdb-console`/`rizin-debug-command` (count-c1.py:34-35); `meta.command` must equal the catalog verb exactly | holds [O] |

[O] Reading caveat the row does not spell out: `2 unevaluable` is run-level only. A malformed individual envelope is recorded in `targets[verb].unsupported_candidates` (count-c1.py:163-169) and leaves the exit at 0/1; only a measure-level `raise` produces 2. The R23 row should state this reading explicitly.

[O] Baseline consistency: `.ufo/waves/round-23/w1/.tmp-counter/out.json` (R22 counter run at rev `a3c92eb6bc70984e90ae5b895412de978840b2c5`) reports `t1_exercised_count` 1/6, `identify-flutter-build` only — exactly the `before: 1` frozen in claims.json:24. [O]

## Proposed cumulative gate entry (declaration side) — findings

The R23 entry had not landed at review time: `.ufo/waves/round-23/worktrees/` contains only `AppImageLibraries`; no BuildCounter output exists yet. Findings below are against the frozen spec (claims.json:26-38, wave1-spec.json BuildCounter item) and the inherited code the entry must reuse. Severity-ordered.

**F1 (high, design) — prefix-conditional source floor is not obtainable from two plain legacy `measure()` calls.** The R23 rule requires legacy-source eligibility (>=51) to be insufficient for NEW witnesses, i.e. round23-prefix witnesses must cite S058+ rows (wave1-spec BuildCounter; claims.json:28 "sourced"). But the legacy `measure()` hardcodes the floor inside `source_rows` construction — `int(cells[1][1:]) >= 51` (count-c1.py:129) — computes eligibility from it (count-c1.py:141-142), and emits witnesses only as `[evidence_id, path]` pairs without the citing entry text (count-c1.py:162). A wrapper that unions two verbatim runs therefore cannot tell which entry made a round23-prefix witness eligible and cannot enforce the >=58 floor; S051-S057 citations would wrongly count as new witnesses. The wrapper must re-derive eligibility per evidence prefix (per-claim policy code, distinct from the reused `bind_cli` binding policy) or parameterize the walk. Falsifiers at risk: "new source relevance or ownership unsupported", "source linkage absent" (claims.json:36-37). [I from O code+spec]

**F2 (medium) — hardcoded claim id in reused output.** Legacy `measure()` returns `"claim": "R22-C1"` (count-c1.py:174). A union that forwards this field would misattribute R23 measurements in the registered verdict output. The wrapper must rewrite to `R23-C1` and the registry row must name the emitted claim id. [O code; I consequence]

**F3 (medium) — unevaluable dominance for the union is unspecified.** Legacy single-run semantics map a raise to exit 2 (count-c1.py `main` try/except). With two roots, the row must declare: any root unevaluable → 2, even if the other root counted 6/6; a healthy root's exit 1 must not mask the other root's 2. Not stated in claims.json or the BuildCounter task text. [I from O]

**F4 (medium) — selftest control list has two gaps against the frozen falsifiers.** BuildCounter's declared controls: positive/new signal, mention-only, refusal, parent-copy, missing-source, same-verb-double-count, tampered-helper (wave1-spec). The falsifier list (claims.json:30-38) additionally names "inherited identify lost" and "new source relevance or ownership unsupported"; neither maps to a declared control. Required additions: (a) a fixture asserting a legacy-prefix witness still counts under the union (guards F1's opposite failure — the union invalidating R22's identify); (b) a fixture asserting a round23-prefix witness citing only a legacy-tier source (S051-S057 shape) does not count. [O spec diff; I recommendation]

**F5 (low) — predicate wording drift.** SKILL.md:692 states the R22 checklist with "this round's frozen k>=1 improvement predicate". R23's frozen predicate is k>=2 (claims.json:26). The R23 row must restate its own predicate and keep exit 0 = 6/6 only — a partial k>=2 remains exit 1 (wave1-spec BuildCounter: "exit0 only6/6,1 incomplete,2 unevaluable"; checklist pattern SKILL.md:690-692). Copying the R22 sentence verbatim into the R23 row would misstate the frozen claim. [O]

**F6 (low) — per-witness vs run-level 2 (see reading caveat above).** Row should keep `unsupported_candidates` out of the exit-code semantics, as R22 does. [O]

**F7 (low) — usage errors fold into code 2 via argparse** (`parser.error` when `--root`/`--rev` missing, count-c1.py `main`). Sibling convention names usage explicitly under 2 (e.g. receipt-validate row, SKILL.md:541: "2 unreadable, no arguments, …"). R23 row should do the same. [O]

**F8 (info) — integration placement gates the selftest.** Frozen counting command is `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE> --rev <REV>` (claims.json:27). The selftest root-resolution (R22 pattern: parent-walk for the round's fixtures path, optional `--root`) must target the integrated layout — fixtures + frozen expected under `.ufo/waves/round-23/` — not the sandbox `worktrees/BuildCounter/output/` layout the author runs in. The registered row must use the frozen command path or record the equivalence; the R22 row used an absolute path. L1 owns this integration. [O spec + I]

**F9 (info) — one ambiguity to resolve in the row text.** "Historical identify remains 1; new same verb never raises count" (wave1-spec BuildCounter): boolean per-verb `exercised` (count-c1.py:167) makes the second clause structurally automatic, but whether a NEW identify-flutter-build witness could establish the verb absent any legacy witness is unspecified. The row should state which reading is implemented (recommend: identify counts only via the round22 prefix; other verbs count via the union). [I]

## Required fields for the R23 registry row proposal (conformance checklist)

Derived from the conventions above; each item traceable: [I from O]

1. `Name`: `round23-C1` (roundNN-claim pattern, SKILL.md:683); `Kind / owner`: `gate / kaidoku`.
2. `Entry / verdict map`: exact frozen counting_command (claims.json:27); 0 = all six / c1_complete only, 1 = incomplete (explicitly including a partial k>=2 that meets the frozen improvement predicate), 2 = unevaluable or usage error; union semantics: any root unevaluable → 2 (F3).
3. `Self-invocation`: `--selftest` map (0 `counter_controls_clean`, 1 `counter_controls_failed`, 2 `snapshot_tampered`/unevaluable), optional `--root` relocation, controls enumerated — must include the two F4 additions.
4. `Pinned values / write scope`: legacy counter's reviewed sha256 pin and where it lives; inherited helper hashes (r20/r21 verb-coverage pins, carried from count-c1.py:36-39 / frozen/helper-hashes.json); R23 frozen manifest path + the manifest-SHA constant location in the script; the two evidence prefixes (round22 + round23) and the per-prefix source floors (>=51 historical, >=58 new); GIT_* stripped and `GIT_NO_REPLACE_OBJECTS=1` (count-c1.py `main`; repeated in BuildCounter task); no live-tree write; removed private Git fixtures only; emitted claim id `R23-C1` (F2); scope limits: "Local association, not authentication" (inherited) plus claims.json:29 boundary — no debugger/Frida execution claims, offline signal work only, inspect-dart-aot static parsing only.

## Declaration-side linkage already grounded in the working tree

[O] `corpus/SOURCES.md` S058/S059/S060: tier A, `mined`, opened `2026-10-21`, used-by naming `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` — they satisfy the legacy eligibility cell check (count-c1.py:129) and clear the >=58 floor.
[O] That knowledge entry exists; first line is `source: S058 …; S059 …; S060 …` (proper `source:` header form), mentions both signal verbs, and cites exact envelope paths under `.ufo/waves/round-23/evidence/c1/` (inventory/decode-uart-hi/decode-official-uart/decode-invalid-decoder/uart-help .envelope.json).
[U] Whether these count at integration depends on the wrapper implementing F1 correctly and on everything being committed at the measured REV — the counter reads Git objects at REV, not the working tree.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewRegistryHome.md` — final-file sha256 recorded in this seat's closing report message (a sha256 printed inside the file it digests cannot match by construction)

## Installs

None.

## Open risks

- The proposed entry (`output/count-c1.py`) and its registry-row proposal did not exist at review time (only `AppImageLibraries` worktree present; BuildCounter still running). This report reviews spec + ancestor; the landed file/row must be re-checked at integration by L1 against F1-F4.
- All tree observations are working-tree state, not a REV; counters evaluate Git objects at `--rev`.
- `.ufo/waves/round-23/w1/.tmp-counter/` scratch observed read-only; not owned by this seat.

— ReviewRegistryHome (w1 reviewer), report trailer: `.ufo/waves/round-23/w1/ReviewRegistryHome.md`
