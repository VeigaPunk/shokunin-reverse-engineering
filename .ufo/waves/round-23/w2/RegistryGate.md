# RegistryGate — round-23 C1 registry fields (source review)

Seat: KaidokuR23.RegistryGate. Leaf reviewer, author-side; not an independent admission.
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` (baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`).

Method: every candidate byte was read with `git show <candidate>:PATH` into the ignored runtime directory and hashed. No counter, fixture, selftest or test was executed. Python was used only for static JSON/table parsing and `git cat-file -e` existence checks on extracted copies.

Process disclosures:
- Three early `/tmp` extraction copies I made were deleted before further work. All extractions now live under `.ufo/waves/round-23/runtime/RegistryGate/`.
- One LOOK-ONLY `_grep` ran against the live worktree `tools/count-c1.py` before I switched to candidate bytes. Live line numbers differ from the candidate: live `frozen = root / …` at :152 against candidate :137, and live `unevaluable` return at :186 against candidate :168. The worktree has moved. Nothing from the live file is cited below.
- One repo-wide `git grep -l selftest21` at the candidate (narrow token). Hits: `gen-wave2.py` and `LOG.md` only.

Labels: **observed** = read from candidate bytes at the cited line; **inferred** = reasoning from observed code, not executed; **unknown** = not determinable from source.

## Findings

### F1 (medium; observed, Python exit semantics inferred) — `--selftest` can exit 1 where the row promises 2
- `counter-fixtures.py:24-27`: `command()` raises `RuntimeError(p.stderr)` on any non-zero git exit. Calls at :31 (clone), :32 (checkout baseline), :35-36 (reset/clean), :100-104 (add/commit/rev-parse).
- `count-c1.py:136-146` `selftest()` has no handler. `count-c1.py:167-168` catches only `(OSError, ValueError, UnicodeError, RecursionError, KeyError)` → 2. `RuntimeError` is not in that tuple (`RecursionError` subclasses `RuntimeError`, not the reverse).
- Consequence (inferred): uncaught → interpreter exit 1, traceback on stderr, no JSON (`count-c1.py:169` skipped). Triggers: `--root` holding the pinned input bytes but no git repository (clone at :31 fails); lane lacking the baseline commit (checkout at :32 fails).
- Row contract `SKILL.md:735`: "2 could-not-evaluate including snapshot_tampered" for `--selftest`. Mismatch.

### F2 (medium; observed) — row says "Reads committed inputs only"; `--selftest` reads the live working tree
- `SKILL.md:735` "Reads committed inputs only".
- `count-c1.py:138` `(frozen/'expected-v2.json').read_bytes()`; `:143` `(root/rel).read_bytes()` per manifest input; `:145` `load(root/…counter-fixtures.py)` re-reads the file; `counter-fixtures.py:23` reads `fixture.json` from `root`.
- Only `measure()` (`count-c1.py:59-133`) reads Git objects at `--rev`.
- Hash checks (:143) and later execution reads (:145, fixtures:23) are separate reads. Verified bytes are not guaranteed to be the executed bytes under a concurrent writer. Severity low (inferred, threat-model dependent).

### F3 (medium; observed, survival inferred from ordering) — eligibility conjuncts have no distinguishing control; W1 ReviewRegistryHome F4(b) not implemented
- Predicate: `count-c1.py:102-103` (`source:` header), `:105-107` (`S[0-9]{3,}` id; `int(sid[1:]) >= 58`; `row[4] in ('A','B')`; `row[8]=='mined'`; `row[9]=='2026-10-21'`; `entry in used-by`).
- Every control row is the literal `counter-fixtures.py:83`: tier A, `mined`, `2026-10-21`. Tier, status, date and the S058+ floor never vary across the 21 cases.
- `old_source` (`counter-fixtures.py:77-78, 85-86`; expected exit 2 in `expected-v2.json`) stops at `count-c1.py:73` (`historical_sources_changed`), before the entry loop at :98+. The S058+ floor and the tier/status/date conjuncts can therefore be removed with all 21 cases unchanged (inferred from ordering).
- Only `wrong_usedby` (`counter-fixtures.py:82`) isolates a conjunct (used-by, :107).
- W1 F4(b) — "a round23 witness citing only a legacy-tier source does not count" — is not an isolated control. Its only legacy-tier case lands on a different reason.

### F4 (medium-low; observed) — selftest oracle compares only exit/count/finding; no snapshot-tamper control
- `counter-fixtures.py:111-112` compares only `exit`, `count`, `finding`. The six exit-2 cases (`helper_tamper`, `invalid_utf8`, `old_source`, `historical_root_injection`, `inherited_lost`, `catalog_changed`) pass for any run-level unevaluable reason.
- No case mutates `expected-v2.json`, `fixture.json` or `counter-fixtures.py`. Selftest guards `count-c1.py:139-140` and `:143-144` have no control.
- `LOG.md:2651` lists "frozen-input mutation exit2"; that is not among the 21 manifest cases. Its evidence source: unknown.

### F5 (medium-low; observed) — the counter under test is not pinned
- `frozen/expected-v2.json` (blob `7e4199d7…`) `inputs` has exactly two entries: `.ufo/waves/round-23/tools/counter-fixtures.py` = `f2990b35…` and `.ufo/waves/round-23/frozen/fixture.json` = `a1f5aff8…`. Both equal candidate bytes (computed).
- The executed counter is `Path(__file__)` (`count-c1.py:146`). No digest of `count-c1.py` appears in the manifest, in the constant (`count-c1.py:25` pins expected-v2 only), or in selftest output (`counter-fixtures.py:115-116` returns finding/passed/total/cases only).
- W1 CriticGate F7 (`CriticGate.md:138-147`) still valid.

### F6 (medium-low; observed) — "copy erases parent refusal" has no control
- claims.json falsifier "copy erases parent refusal" (`claims.json:30-38`).
- Detached-copy path: legacy `bind_cli` returns 2 when `ok`/`data` are absent (`round-22/tools/count-c1.py:74`); candidate silently drops it (`count-c1.py:123`, counts only `== 0`).
- Cross-file path: the per-path loop (`count-c1.py:119-124`) does not link a refused ancestor file to a separate copy file. A fresh full envelope with `ok:true` in another cited file counts (inferred; the counter cannot know the copy's ancestry).
- None of the 21 manifest case names covers either path.

### F7 (medium-low; observed) — round-23 registry row (`SKILL.md:735`) omits or misstates fields
- Count 21 is not stated in the row. `expected-v2.json` has 21 keys. `LOG.md:2651` claims `selftest21/21`; that is a run claim I did not verify.
- Per-witness codes 1 and 2 are silently dropped (`count-c1.py:123`). No `unsupported_candidates` field exists at candidate, so code 2 is run-level only. The row does not state this (W1 F6, `ReviewRegistryHome.md:41`, still open).
- Emitted tokens vs. row: snapshot tamper emits `finding:'unevaluable'` with `error:'snapshot_tampered: …'` (`count-c1.py:144,168`). Pass emits `c1_complete` (`count-c1.py:129`), not `c1_complete6/6`. Exit codes match.

### F8 (low; observed) — empty refusal containers are not refusals
- Round-21 helper `refused()` uses truthiness: `round-21/tools/verb-coverage.py:44-45` (`if node.get(key): return True`). `{"error": {}}` and `{"errors": []}` pass `refused()`. Candidate `bind_new` relies on it (`count-c1.py:51`); legacy `bind_cli` likewise (`round-22/tools/count-c1.py:76,79`).
- W1 CounterRefusals.md:224 (N7) still valid at candidate. No control.

### F9 (low; observed) — ambiguous retained v1 file
- `frozen/expected.json` and `frozen/expected-v1.json` are byte-identical (blob `8f1cff19…`, sha256 `ad1b4462…`). Neither is referenced by candidate code; only `expected-v2.json` is (`count-c1.py:137-138`).
- Row says "Old v1 proposals retained, not active" but does not name `expected.json`.

## Verified holding (observed / computed / static)
- code0 only 6/6: `count-c1.py:166` `code = 0 if result['t1_exercised_count'] == 6 else 1`. `t1_exercised_count = len(held)` (:127-130), `held` ⊆ the six legacy T1 verbs (round-22 counter `T1` tuple; set equals claims.json:16-23).
- code1 incomplete: any count ≠ 6 → 1 (:166); finding `c1_incomplete` (:129).
- Pins equal candidate bytes (sha256 computed): LEGACY `c925918f…` (`count-c1.py:23`); r20 helper `cfbf1880…` and r21 helper `61536938…` (legacy `HELPER_SHA256`); manifest `458b30d5…` (`count-c1.py:25`, file blob `7e4199d7…`); `counter-fixtures.py` `f2990b35…`; `fixture.json` `a1f5aff8…`.
- Historical pins identical to baseline: catalog blob `61fc4e66…` (both); `round-22/evidence/c1` tree `b83fc459…` (both).
- Temp write scope conforms: all writes under `<root>/.ufo/waves/round-23/runtime/`. Measure: `count-c1.py:74-76` (mkdir; `tempfile.tempdir` redirect). Selftest: `counter-fixtures.py:21-22, 29` (`TemporaryDirectory(prefix='fixture-', dir=runtime)`). Clone reset/clean (:35-36) acts only inside the disposable clone. `round-23/.gitignore` = `/runtime/` and `/worktrees/`.
- Source eligibility, static: S058–S061 (`corpus/SOURCES.md` blob `daf5ce02…`, rows at lines 64-67): tier A, status `mined`, date `2026-10-21`, used-by naming `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` (S058–S060) and `…r23-dart-legacy-layout-boundary.md` (S061). 61 unique IDs; no duplicates. Both entries begin with `source:`. All 8 cited round-23 `.json` paths exist at candidate (`git cat-file -e`).
- 21/21 expected tuples agree with my derivation from candidate source (inferred; not executed). Key points: duplicate_member → `verb-coverage.py:28` raise → `bind_new` returns 2, uncounted; nested/sibling refusal → `refused()` (:44, :50); wrong_operation → `bind()` operation mismatch; all_six → `CLI_BIND_VERB` mapping.

## Stale W1 proposal findings re-evaluated against candidate

| W1 finding | Candidate status |
|---|---|
| ReviewRegistryHome.md:15 (count-c1.py:174-176 refs) | STALE — moved to :128-130 and :166-168 |
| :16 selftest parent-walk default | STALE — `--root` required (`count-c1.py:155`) |
| :17 SELFTEST digest `1abdd9df…` (R22 manifest) | STALE for R23 — constant `458b30d5…` (:25) equals R23 `expected-v2.json` |
| :18 inputs include helpers and r20 artifact | STALE — inputs are 2 entries; helper pins are code constants checked at rev |
| :19 `frozen/helper-hashes.json` | N/A — absent in round-23 `frozen/`; not referenced |
| :20 `kaidoku-r22-fixtures-` under TMPDIR; helper mutation | STALE — `fixture-` in runtime (fixtures:29); mutation is of the legacy counter bytes in the clone (fixtures:88-90) |
| :23 and :41 `unsupported_candidates` | STALE field; substance OPEN (F7) |
| :33 F2 hardcoded R22-C1 claim id | RESOLVED — `'claim': 'R23-C1'` (`count-c1.py:128`) |
| :35 F3 union dominance | RESOLVED — any raise → 2; historical/catalog/source-prefix guards raise |
| :37 F4(a) legacy witness still counts | COVERED implicitly by `positive` (count 2 requires historical identify) |
| :37 F4(b) | OPEN (F3) |
| :39 F5 k>=2 wording | RESOLVED — `SKILL.md:735` states k>=2, not a completeness gate |
| :45 F8 selftest root resolution | RESOLVED — `--root` required; row uses `--root <LANE>` |
| :47 F9 identify new witness | RESOLVED structurally — identify historical is mandatory (`historical_baseline_changed` guard in `measure()`) |
| :55 self-invocation names `counter_controls_clean/failed` | RESOLVED to `selftest_clean`/`selftest_failed` (`counter-fixtures.py:115`; `SKILL.md:735`) |
| CriticGate.md:138-147 F7 | STILL VALID (F5) |
| CounterGitIsolation.md:4-6 writes under inherited TMPDIR | RESOLVED for R23 wrapper by `count-c1.py:76`; R22 `revision_helpers` unchanged |
| CounterRefusals.md:224 N7 | STILL VALID (F8) |
| CounterRefusals.md:230 N8 refused vs unparseable | CHANGED — `data.ok:false` now returns 1 via the `bind_new` walk (`count-c1.py:51`); still not reported (F7) |
| CounterRefusals.md:232 N10 reasons collapsed | STILL VALID — bare ints; no reason recorded |

## Produced files and hashes
- `kaidoku-shokunin/.ufo/waves/round-23/w2/RegistryGate.md` — this report. Final sha256 is in the delivery message (not embedded, to avoid self-reference).
- Ignored extractions under `kaidoku-shokunin/.ufo/waves/round-23/runtime/RegistryGate/`, candidate-pinned (blob id; sha256):
  - `count-c1.py` — blob `0f966a50018bba2fa5af3d6f9af1541f660c43c2`; sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` (8382 B)
  - `counter-fixtures.py` — blob `55356faade5c11165783fc551a8a7f5275e65a6f`; sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`
  - `frozen/expected-v2.json` — blob `7e4199d73d8dd0f8ef27e56cb04935d015eea93d`; sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`
  - `frozen/fixture.json` — blob `92c2f04ae7e01456cffd8b97aefcd63bcaaa55f5`; sha256 `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`
  - `frozen/expected-v1.json` = `frozen/expected.json` — blob `8f1cff19fff9c11945cc6f8fd0eb34d661397755`; sha256 `ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24`
  - `frozen/counter-fixtures-v1.py` — blob `a226fb25ee603188b65867099e368f8dae007817`; sha256 `96e65034bcf2206c0e9c6335da264695f4741ed91e9a357c56484e6cd35e2849`
  - round-22 counter (legacy) `tools/count-c1.py` — blob `2b97d43c709f51e2f11d5c61281f574cc3779f83`; sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`
  - helpers: r20 `verb-coverage.py` blob `988f8f6c8c29412c27b79e25cd82de7a0fb82f3c`, sha256 `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`; r21 `verb-coverage.py` blob `0756c0ecc534277178b9c7d6999504dea618c400`, sha256 `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`
  - catalog `round20/verb-coverage.json` — blob `61fc4e66a5842941547507cf7c8d3bf064a57c70`; sha256 `7c0d57d748720dcdaa69c2e481c62893b7185c663564a9f3e793dae0574fc515`
  - `corpus/SOURCES.md` — blob `daf5ce02b06390caf204f8b92fbb0288509f293a`; sha256 `736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525`
  - `SKILL.md` — blob `e21f0b113b3e9ab3356ed998652bef66fb8b5e84`; sha256 `be7d85f8bedb8748b73fcdfaaf627d73ffcf2578d9ab9d3bb9296b353d14cf9b`
  - `LOG.md` — blob `9966bfb7d5791d847f39a20f73896a6388b3684b`; sha256 `249553811d364458ddf3964446b97c181cb557db203423ff0b40f9d0032163ef`
  - knowledge `2026-10-21-r23-offline-signal-envelopes.md` — blob `6c14cce624550135d19b587358b820886f096bcc`; sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35`
  - knowledge `2026-10-21-r23-dart-legacy-layout-boundary.md` — blob `7d24fb83a4c081464486925dcafce668351b1587`
  - `gen-wave2.py` — blob `4c4f7fe7a6e1e62c7b010d502c384918d0eca8b6`; sha256 `da2962bc77d964c09a9ac3ff06c8ea760d4001164974e48135c3b6404d5d009a`
  - `.gitignore` (round-23) — blob `eb0cb12fe00ece8a5036179a8a3a96f5f64e6d25`; sha256 `a94bb09a7255bf2d97b003717ba0eb6f59eb5d72361ff9ca55be48f8e86532e9`
  - W1 copies (read): `ReviewRegistryHome.md` sha256 `d5bd2fa0801949c527b1f18414a3c9d5ab61721940e2d817ced9b16e09fb0d9d`; `CounterRefusals.md` sha256 `a899d270309dc32bdc887e0534f6da37097c1cf689c5a0b42610f705411b370d`; `CounterGitIsolation.md` sha256 `bfdab2f0cb3f310150987f24df4c13a3d16c185dbc86adf908dbfadd91747c29`; `CriticGate.md` sha256 `fe92e9e59786c40bdea7d903b2edc9e86f48c85e987270136eb13f5a50658ba8`
  - `w1/.tmp-counter/r23-out-final.json` extracted (sha256 `832167363438af7447422e2c33627a52808adbb6ad5ef6de330d7be6b7487399`), not analyzed (outside registry-field scope)
- Git objects read only; no lane, index, or sibling files written.

## Installs
None. Only `python3` stdlib (`-I -B`) for static parsing; no package installs, no updates.

## Open risks and unknowns
- Not executed: every control-outcome statement (F3, F4, F6, 21/21 agreement) and Python exit semantics for F1 (standard interpreter behavior, inferred). Run seats own execution.
- `LOG.md:2651` (`selftest21/21`) and "frozen-input mutation exit2" are run claims. Not reproduced here (unknown).
- The live worktree has moved relative to the candidate. Any run against `--root <LANE>` with a live worktree tests different counter bytes. The counter digest is not pinned anywhere (F5), so a revision or counter-digest binding is needed for the row to mean what it says.
- Real measured count k, and evidence binding for the four LOG-claimed verbs, were not computed here (Run seats).
- Author-side evidence only; not independent non-author admission.
