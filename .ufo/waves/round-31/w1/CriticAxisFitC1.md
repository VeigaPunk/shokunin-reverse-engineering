# R31-C1 — axis-fit critique, before data

Seat: `KaidokuR31.CriticAxisFitC1` (critic, leaf). Base `c369242fee9f559f895e3f7956b1242076c7b1be`; freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`. Claim read from `.ufo/waves/round-31/claims.json`, sha256 `6b090a3363e57330582841c6a17659139ab2fb61b86f2ae59b3be448e0099e51` in the worktree and at the freeze commit (identical). I ran no REA, installed nothing, and made one lane write: this file. Sandbox clone and evidence log are under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticAxisFitC1/`.

## Verdict

**narrow-fit.**

Coverage is the right axis only for the artifact the claim actually changes: `PROVINCE.md` gains its first Core row for REA's SQLite reader (0 rows under any spelling at base and freeze), and the CLI verb `inspect-sqlite-database` is used for the first time. As written, however, the claim's surface sentence is false: the operation was already run and named at the base, and its knowledge entry was already the admitted coverage move of luna-round-7. Under the fleet lesson ("name the axis by the surface it changes; re-scoring a held rule on new inputs is quality work, not coverage"), the frozen sentence's novelty premise is depth/quality-class, not coverage. The claim survives as coverage only when read as "first PROVINCE Core row + first CLI use", not as "new verb".

Attack verdicts on the assigned sub-questions:

| Attacked premise | Verdict | Counterexample |
|---|---|---|
| "genuinely ungoverned ground … never run or named" | **fails** | `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:1,5,7,9` names and runs `inspect_sqlite_database` under `rea-agents@6.5.0` (Evidence `ev_7572e6…`); mapped in `corpus/README.md:65,163`; coverage-credited in `SCORECARD.md:503-521` / `LOG.md:811-821` |
| "no prior … Core row about REA's SQLite reader" / held under another name | **holds** (no prior row) | `PROVINCE.md` at base and freeze: 0 hits for `sqlite|database|.db|pnpm|package_index`; no `inspect_artifact`/Electron row claims `.db` reading |
| positive class is real published input, not author-built | **holds**, with a fixture caveat | 12/12 carrier bytes equal the member/asset inside the published container; 5 wheel sha256 and the sdist sha256 equal committed PyPI JSON digests |
| do-nothing or shortcut control could meet the counter | **do-nothing: fails**; **two shortcuts: fail the claim's own contract** | gates reject absence; `--write-evidence` prints the target line before committed envelopes exist; `entry_ok` accepts `S096` in prose |
| 12 carriers add coverage breadth | **fails as breadth, holds as evidence** | 3 upstream schema families (proj.db ×5, Chinook ×2, pyogrio fixtures ×5); the claim's own limits say proj.db may share one schema |

## Evidence

Times are UTC, 2026-10-23. Every command below is read-only on the lane; the command-A red ran in the sandbox clone.

| # | Finding | Command | Output excerpt | Exit | Time | Label |
|---|---|---|---|---|---|---|
| F1 | Base and freeze `PROVINCE.md` name neither spelling of the verb | `git grep -c --fixed-strings 'inspect-sqlite-database' c369242f -- PROVINCE.md SKILL.md corpus/knowledge` | (no output) | 1 | 04:15:49 | observation |
| F1b | Same, freeze | `git show 35ba7c52…:PROVINCE.md \| grep -c -i sqlite` | `0` | 1 | 04:15:49 | observation |
| F2 | Base `corpus/knowledge` names the operation with its tool-name spelling | `git grep -c --fixed-strings 'inspect_sqlite_database' c369242f -- PROVINCE.md SKILL.md corpus/knowledge` | `…l7-04-inspect-sqlite-database.md:3` ; `…l8-01-6p4-symmetry-battery.md:1` | 0 | 04:15:49 | observation |
| F3 | L7-04 records a real 6.5.0 run, not a catalog listing | `git show c369242f:corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md \| nl -ba` | `:1 # inspect_sqlite_database — offline SQLite schema inventory`; `:9 Carrier: /tmp/bb6-leg-6/sc4-index.db, SHA-256 3701a7e3…; … Call: inspect_sqlite_database({"path":…}); Evidence ID ev_7572e622…` | 0 | 04:15:49 | observation |
| F3b | The entry is indexed as an admitted knowledge file | `git show c369242f:corpus/README.md \| nl -ba \| sed -n '65p;163p'` | `65 \| knowledge/2026-10-16-l7-04-inspect-sqlite-database \| Path-only inspect_sqlite_database inventory …`; `163 \| 2026-10-16-l7-04-inspect-sqlite-database \| 6.5.0 SQLite path-only inventory …` | 0 | 04:14:31 | observation |
| F4 | Coverage credit for that entry was already banked | `git show c369242f:SCORECARD.md \| nl -ba \| sed -n '503,534p'`; `git show c369242f:LOG.md \| nl -ba \| sed -n '808,830p'` | `503 ## luna-round-7 — coverage: six 6.5.0-verb entries`; `521 \| coverage \| 10.0 → 10.0 … \| improved (six RESULT-class verbs became admitted, quality-gated knowledge) \|`; `811 ### luna-round-7 — coverage: six 6.5.0-verb knowledge entries (72 → 78)`; `820-821 entry 4 admits only lane-B's real-carrier SQLite result (lane A's synthetic fixture fails QUALITY-12)` | 0 | 04:14:31 | observation |
| F5 | No other Core row owns SQLite reading | `git grep -n -i -E 'sqlite\|database\|\.db\b\|pnpm\|package_index' c369242f -- PROVINCE.md` | (no output) | 1 | 04:15:49 | observation |
| F6 | Carriers are published input, byte-for-byte | `lsattr /fast/scratch/hyaku/kaidoku-r31/carriers/*`; python zip/tar member sha256 vs `carriers.tsv` | `12 ----i-----------------`; `carrier bytes == published container member/asset: 12/12` | 0 | 04:15:49 | observation |
| F6b | Container digests are the published PyPI digests | python: compare `corpus/evidence/round-31/c1/pypi-*.json` digests to `carriers.tsv` | `pypi-json sha256 hit: True` ×5; `pyogrio sdist sha256: e1441dc9c866f10d… frozen e1441dc9…: True` | 0 | 04:14:05 | observation |
| F7 | Counter selftest is green | `python3 -I -B tools/round-31/c1-sqlite-positive.py --selftest` | `selftest cases=14 failures=0` | 0 | 04:15:49 | observation |
| F8 | Do-nothing fails every gate | harness importing the frozen counter (no REA): `entry_ok(None)`, `province_ok(None)`, `committed_check('.', 'c369242f', 'proj-341', {}, 1, '')` | `entry_ok(None) -> (False, 'entry absent')`; `province_ok(None) -> (False, 'PROVINCE absent')`; `committed_check… -> (False, 'committed envelope absent')` | 0 | 04:15:49 | observation |
| F8b | `entry_ok` accepts a bare prose mention | same harness | `entry_ok("analysis note, cf. S096") -> (True, 'ok')` | 0 | 04:15:49 | observation |
| F9 | The lane's own source-linkage rules are stricter than the frozen gate | `grep -n -E '^\| (29\|45) \|' corpus/QUALITY.md` | `39:\| 29 \| A round-specific held-verb counter verifies its declared source linkage…`; `55:\| 45 \| … the row must be on the entry's \`source:\` line, new since the base, status mined, opened in the round and listed in the round lesson's \`## Gate\`…` | 0 | 04:14:31 | observation |
| F10 | The S-rows the claim cites do not exist yet | `grep -c -E '^\| S09[2-6] \|' corpus/SOURCES.md` | `0` | 1 | 04:15:49 | observation |
| F11 | A passing C1 can still lower the coverage proxy | sandbox clone, command A recipe from `SCORECARD.md:88-123`: base vs empty `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` + commit | base `{"coverage_score": 10.0, "knowledge_files": 116, "mapped": 116, "missing": []}`; after `{"coverage_score": 9.91, "knowledge_files": 117, "mapped": 116, "missing": ["2026-10-23-r31-sqlite-positive"]}` | 0 | 04:15:03 | observation (sandbox) |
| F12 | Instruments match the frozen hashes | `sha256sum tools/round-31/*.py` | `04802088…` c1; `aefd8639…` oracle; `d2394895…` c2 — all equal to `claims.json` | 0 | 04:15:49 | observation |

Supporting code reads, exact lines in `tools/round-31/c1-sqlite-positive.py`: `33 REA = ["npx", "-y", "rea-agents@6.5.0"]`; `89 argv = REA + ["inspect-sqlite-database", path, "--schema-scope", "database", …]`; `113 if strip_meta(committed) != strip_meta(live)`; `124 if CLAIM_ROW not in text`; `180 if verdict == LABEL and not write`; `201 return 0 if passed == TARGET and e_ok and p_ok else 1`.

## 1. Is `inspect_sqlite_database` ungoverned ground at the base?

Split answer, because the claim conflates two surfaces:

- **The operation is not new.** L7-04 (`corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`) was admitted 2026-10-16: it names `inspect_sqlite_database` three times, records a 6.5.0 call on a pinned pnpm v11 `index.db`, an Evidence ID and a carrier sha256, and its result (`rows:null`, one `package_index` table). `corpus/README.md:65,163` maps it. `LOG.md:811,820-821` records it as entry 4 of the six-verb coverage move, and `SCORECARD.md:521` records that round's coverage verdict as "improved (six RESULT-class verbs became admitted, quality-gated knowledge)". The operation was also named once more at `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:12` as a 6.4.0 refusal leg.
- **The PROVINCE row is new.** At base and at the freeze, `PROVINCE.md` has 0 hits for `sqlite` (F1, F1b), and no row under another name owns SQLite reading (F5): the `inspect_artifact`/`extract_artifact` archive row and the Electron/ASAR row do not cover `.db` schema inspection. So the lane's coverage artifact (AXES: "PROVINCE.md lists every surface") genuinely lacked this surface.

The claim's zero-count is a spelling artifact: the lane writes the tool name with underscores, the CLI command with hyphens. Counting `inspect-sqlite-database` returns 0 in `corpus/knowledge` (F1) while `inspect_sqlite_database` returns 3+1 (F2). A surface-keyed check would have returned 4, not 0. The frozen sentence "a verb the lane has never run or named" is therefore falsified by the base tree; "no PROVINCE Core row" is not.

## 2. Is the 12-carrier positive class real published input?

Yes, and it is not author-built:

- 5 `proj.db` are members of published pyproj wheels; each wheel's sha256 equals the committed PyPI JSON digest, and the extracted member's sha256 equals the frozen carrier sha256 (F6, F6b).
- 2 Chinook files are GitHub release assets of `lerocha/chinook-database` v1.4.5; the asset sha256 equals the carrier sha256 (F6).
- 5 `.gpkg` are members of the published pyogrio 0.11.1 sdist (sdist sha256 equals the committed PyPI digest); each member sha256 equals the frozen carrier sha256 (F6, F6b). They are upstream **test fixtures**, shipped in the sdist, not real-world databases — published, fixture-class.
- Independence caveat: this is 12 files in three upstream families. The claim's limits already say proj-341/350/361 may share one schema; in fact all five proj.db come from one PROJ database line and the two Chinook variants share one schema. The 12 runs are evidence depth over one surface, not 12 independent surfaces. The carrier count must not be presented as coverage breadth.

The pre-freeze probe (claims.json `pre_freeze_probe`) is an L1-built non-carrier, but that is a probe, not a carrier; no carrier or mutant was run before the freeze per that record. The lane's own QUALITY-12 admission rule (`l7-04:16`) excludes self-made fixtures from admitted entries, so the GeoPackage fixtures being upstream-published matters: they are admissible as published input even though fixture-class.

## 3. Could a do-nothing or shortcut control meet the counter?

- **Do-nothing: no.** Without an entry, `entry_ok` is 0; without a PROVINCE row, `province_ok` is 0; without committed envelopes, every carrier that matched the oracle is downgraded by `committed_check` to `P1-fail` ("committed envelope absent"). The target line requires pass=12, entry_ok=1, province_ok=1 (F8; code lines 121-143, 180-201). Junk-row (entry + doc rows, no envelopes) fails the same way in default mode. All-false and id-copy fail `judge` (ok/exit, operation, subject sha256, full report compare; code 64-85). The full-envelope rule of round 30 (M30-3) is present at line 113.
- **Shortcut 1 — `--write-evidence` skips half the predicate.** In write mode line 180 bypasses `committed_check` for every carrier, yet line 201 still returns exit 0 and prints `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1` once the live runs match the oracle and the doc gates pass. That receipt is pre-commit evidence, not the frozen target: the claim's predicate requires a committed envelope added after the freeze that equals live. The L1 must quote a default-mode run after commit; a write-mode receipt must never stand as `P1-pass`.
- **Shortcut 2 — `entry_ok` is a substring check.** `entry_ok("analysis note, cf. S096")` returns True (F8b). A junk entry that mentions `S096` in prose, with the `source:` line citing something else (or S096 not mined/opened/listed in the lesson's `## Gate`), passes the frozen gate while failing QUALITY #45 (`corpus/QUALITY.md:55`) and the source-linkage duty of QUALITY #29 (`:39`). Today no S092-S096 rows exist in `corpus/SOURCES.md` (F10); the source seats are still writing them, so a dangling S096 would not be caught by the counter.
- **Live-run authenticity.** `run_rea` resolves bare `npx` through PATH (line 33/89) and checks only the hardcoded package.json version/hash. A PATH-shadowed `npx` that emits oracle-derived envelopes would satisfy judge + committed equality with no REA run. This is intentional deception rather than a plausible self-control, so I record it as an attack surface, not a required correction; the controls do not include a PATH-shadow test.

## 4. New verb (coverage) or deeper reading of a held verb (depth)?

The operation is corpus-held and coverage-credited (l7-04 / luna-round-7); the CLI spelling and PROVINCE Core row are not. The frozen predicate (12 live envelopes equal to an independent oracle field-for-field) is depth/operability-class verification used as admission evidence, which is exactly the lane's own Core-promotion convention ("ground moves to Core only after an end-to-end probe lands a LOG entry citing its evidence_id and subject sha256", `PROVINCE.md` conventions paragraph). So the axis label is defensible only for the PROVINCE artifact. The sentence "a verb the lane has never run or named" is a depth-class novelty claim laid on a coverage claim; that is the misfit edge.

## Impacted axes

| Axis | Impact | Why |
|---|---|---|
| coverage | **narrow positive, with a measurable regression risk** | PROVINCE gains its first SQLite Core row (real), but the coverage proxy (command A) falls 10.0 → 9.91 if the new entry is not added to the README Coverage-map section; the frozen counter does not gate this (F11) |
| calibration | **at risk** | the frozen surface overstates novelty against l7-04; the SCORECARD coverage row also still cites 109/109 at `ebe2cb4a` while command A at base is 116/116 (F11) — pre-existing, not caused by C1, but the claim should not repeat a stale denominator |
| freshness | minor | the unmoved command is spelling-keyed; the intended zero is "no PROVINCE row", not "no name in corpus" |
| depth | supports, not claimed | 12 live oracle-equal envelopes are depth-class evidence; C2 owns the depth claim |
| operability | at risk | `entry_ok`/QUALITY #29/#45 gap; `--write-evidence` target line; S092-S096 not yet in SOURCES.md |

## Wording the L1 must use (lesson; `claims.json` stays frozen)

Do not amend `.ufo/waves/round-31/claims.json` or re-scale the target. Record the following in the round lesson (and in the LOG entry), and carry the corrected surface in the C1 entry and its PROVINCE row:

- Replace the frozen surface sentence's premise. The lesson statement must read, in substance: "REA SQLite reader (operation `inspect_sqlite_database`; CLI `inspect-sqlite-database`): named and run once at l7-04 (2026-10-16, `rea-agents@6.5.0`, Evidence `ev_7572e6…`), and that entry was the coverage move of luna-round-7; absent from `PROVINCE.md` at the base (0 rows under either spelling). Round 31 adds the first PROVINCE Core row for the surface and the first CLI-verb use, over 12 published files in three upstream families."
- The coverage increment this round is the **PROVINCE Core row + CLI verb**, not the verb's discovery. State that luna-round-7 already credited coverage for the entry so the same surface is not counted twice.
- Replace the unmoved command with a surface-keyed one: `git grep -c -iE 'inspect[_-]sqlite[_-]database' <REV> -- PROVINCE.md` (0 at base) plus "no Core row under another name" (`git grep -n -iE 'sqlite|database|\.db|package_index' <REV> -- PROVINCE.md` empty). Do not quote the hyphen-only count as evidence the lane never touched the verb.
- Record the carrier caveat: 12 files, 3 upstream schema families; 5 GeoPackages are published pyogrio test fixtures. Do not present 12 as breadth.

## Smallest safe correction

1. **Land the README map rows with the entry.** Add the Coverage-map row (and the Knowledge-table row, as luna-round-7 did) for `2026-10-23-r31-sqlite-positive`, then re-measure command A and record 117/117 (or the then-current 10.0) before claiming coverage. Without this, C1's counter can exit 0 while the coverage axis is harmed (F11). The frozen counter cannot be edited without a QUALITY #33 `instrument_supersessions` entry; the cheap safe path is an L1-verified doc gate recorded in the LOG, not a silent instrument edit.
2. **Bind the entry's source line to S096.** The entry's `source:` line must cite S096; S096 must be a new, mined `corpus/SOURCES.md` row opened this round and listed in the lesson's `## Gate` (QUALITY #45), and the counter's source linkage is not verified by `entry_ok` (QUALITY #29). If the L1 wants the counter to enforce this, use the QUALITY #33 supersession path with a re-taken before record and a red case ("source line cites another new row").
3. **Quote only a default-mode counter run** (no `--write-evidence`) after the 12 committed envelopes exist; a write-mode run is not the target.
4. Do not edit `claims.json`, the carriers, the predictions, the instruments, or the frozen target under this critique; the surface correction is lesson-only and the predicate is unaffected.

## Artifacts

- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticAxisFitC1/evidence.txt` — sha256 `4342cd8a3be8716011677d336a4b8bc49bdf0f200cc89279c8a88bfef83046b3` (timestamped evidence log; section G quotes the 04:15:03 command-A run verbatim).
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CriticAxisFitC1/clone/` — sandbox clone at `c369242f`, plus one control commit adding an empty `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` to measure the command-A drop (F11).
- No installs; no REA runs; no external sources opened by this seat; no lane, fleet, Git, or jj state mutated. The only lane write is this report.
