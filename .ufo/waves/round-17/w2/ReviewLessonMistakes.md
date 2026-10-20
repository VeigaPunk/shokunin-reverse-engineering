# ReviewLessonMistakes — falsify pass on round-17 `## Mistakes`

seat: KaidokuR17.ReviewLessonMistakes (author-side advisory; never an outside reviewer)
target: `corpus/lessons/round-17.md:69-89` at lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`
(baseline `b563c799d97774aae4351276fe43cb897311e349`; predictions frozen at `2711674`)
axes: calibration (primary), depth
mode: read-only. `git show`, round-17 tools against retained files, `python3 -B` selftests, `unzip`/`grep`
over the installed Ghidra source. No REA analyze/search/decompile, no Ghidra run, no carrier execution,
no pacman. Tool installs/updates: none.

Labels: **OBS** = observed command output; **INF** = inference from the cited artifacts.

## Verdict

The table is structurally sound: 9 rows, 4 cells each, and every class token is in the `CORPUS.md:174-176`
vocabulary. The `R16-PROVENANCE` corrections are line-exact, 4/4 resolved, and filed bytes are untouched.
But four fix claims do not hold at the reviewed revision, one fix's red state recurred after its own
commit, four `captured-by` cells are not a `QUALITY.md` criterion, a protocol rule, or `none`, three
claimed repairs name no red-before state required by `CORPUS.md:186-190`, and one stale premise survives
in the shared contract.

## Findings

### F1 — HIGH — row 2's fix state is false at `da64646`; C1's "every row" claim is falsified by the round's own audit

Anchors: `corpus/lessons/round-17.md:74` (row 2), `:12-14` (C1); `SKILL.md:448`, `:449`, `:532-541`.

**OBS** at HEAD:

```
$ python3 -B .ufo/waves/round-17/tools/invocation-audit.py --root . --rev da64646
counts: {'argv_records': 74, 'exercised_match': 6, 'labelled_unexercised': 0, 'receipt_files': 20,
         'receipt_glob_pathform_excluded': 71, 'rows': 17, 'unlabelled_variant': 11,
         'unreadable_receipt_paths': [], 'unreadable_receipts': 0}
unmatched: custody-pair, go-carrier-run, go-log-extract, go-route-predict, go-route-compare,
           receipt-validate, pins, temporal-sweep, invocation-audit, go-buildinfo-probe,
           round17-structural-controls
```

At baseline the row's red state is real (**OBS**): `--rev b563c799d97774aae4351276fe43cb897311e349`
returns `rows 7, exercised_match 5, unlabelled_variant 2` (citation-drift, custody-pair), exactly the
row's "2 of 7". But the fix column says "Both rows now advertise the exercised isolated absolute argv,
re-exercised this round with retained argv". At HEAD:

- `custody-pair` is still `unlabelled_variant`; no committed receipt matches its advertised command.
- `citation-drift` matches `.ufo/waves/round-16/verification.json` (r16), not a round-17 exercise. An
  untracked `w2/citation-drift-head.json` records a post-revision run of the advertised command (exit 0),
  but it stores a `command` string, not an `argv` array, and is not committed evidence at `da64646`.
- Both rows cite `.ufo/waves/round-17/verification.json` as the exercised-argv receipt:
  `ls .ufo/waves/round-17/verification.json` → `No such file or directory` (exit 2) (**OBS**).
- The ten new round-17 registry rows (`SKILL.md:532-541`) carry no `unexercised` label and no matching
  receipt. `w1/DraftSkillSection.md:8,50` says all seven drafted rows were labelled `unexercised` and
  "L1 must replace the label with the exercised argv once a receipt exists" — the labels were removed
  without receipts, the regression `w1/CriticNoHarm.md` F10 warned about (**OBS**, INF).

So C1's "Every SKILL registry row's command matches an exercised retained argv" is 6/17 true at the
reviewed revision, and the routed defect R16-INVOCATION is only half discharged (citation-drift aligned
in text, custody-pair neither exercised nor labelled).

Smallest fix (at the revision): retain `.ufo/waves/round-17/verification.json` with each invoked argv
and re-run the audit to `unlabelled_variant 0`; or, minimally, relabel custody-pair and the ten new rows
`unexercised` in `SKILL.md` (keeping one physical line per row) and rewrite C1 to the measured state,
e.g. "6 of 17 rows match a retained argv; 11 are labelled unexercised".

### F2 — MEDIUM — row 6's red state is real, but "retained in verification" does not resolve and no command is named

Anchor: `corpus/lessons/round-17.md:78`.

**OBS**, reproducing the two claims from the retained notesmd-cli artifacts (forced copy under `/tmp`):

```
$ python3 -B .ufo/waves/round-17/tools/compare.py \
    --prediction /tmp/forced-route.prediction.json \
    --observation .ufo/waves/round-17/runs/pro-notesmd-cli/observation.json
# fields: snapshot_route predicted "info", observed "fallback", match false; exit 1

$ python3 -B .ufo/waves/round-17/tools/compare.py \
    --prediction /tmp/three-field.prediction.json \
    --observation .ufo/waves/round-17/runs/pro-notesmd-cli/observation.json
# fields: untested_version / snapshot_label / missing_bootstrap all match; exit 0
```

The discriminator is real and genuinely separates the route field from the three contract fields. The
problem is the evidence: `.ufo/waves/round-17/verification.json` is absent (F1), and no committed file
under `runs/` or `predictions/` contains `forced` (`grep -rni forced .ufo/waves/round-17/runs
.ufo/waves/round-17/predictions` returns nothing). "Retained in verification" is therefore a fix that
exists only as intent at this revision, and the cell gives no command.

Smallest fix: commit the two compare outputs plus exits (e.g. under
`.ufo/waves/round-17/runs/pro-notesmd-cli/compare-forced.json` / `.exit`) and cite them with both
commands in the cell; or add them to the round-17 `verification.json` F1 asks for.

### F3 — MEDIUM — row 1's fix claims retained mid-run pin maps that are never written

Anchors: `corpus/lessons/round-17.md:73`; same phrase in the Gate row `:26` ("pins equal pre/mid/post").

**OBS** on every retained receipt (all eight checked):

```
$ python3 -B -c "import json; d=json.load(open('.ufo/waves/round-17/runs/pro-notesmd-cli/receipt.json')); \
    print(sorted(d)); print(sorted(d['steps']['analyze']))"
top keys: ... pins_compare, pins_post, pins_pre ...   (no pins_mid, no mid timestamps)
steps.analyze: argv, cwd, ended_at_utc, evidence_id, exit, polls, retained_logs,
               started_at_utc, stderr_path, stderr_sha256, stdout_path, stdout_sha256
taken_at_utc occurrences in receipt: 4 (pre, post, compare pre, compare post)
```

Across all eight receipts (`for` loop over `runs/*/receipt.json`, printing keys containing `mid` and the
`taken_at_utc` count): every run reports `mid_keys=[]`, `taken_at=4` (**OBS**).

`carrier-run.py:422-432` builds `mid = pins.snapshot(pin_paths)`, compares it, and on inequality records
`pins_changed_during_run`; on equality the mid map is dropped. Receipts therefore carry pre and post maps
with UTC timestamps and `pins_compare.equal=true`, which satisfies QUALITY #19 — but not "pre, 30 s
mid-run and post maps with timestamps". A reader cannot tell from a receipt whether any mid snapshot ran,
let alone compare it (INF, from the code and absent fields). This is the same overstatement class the row
is correcting, one level down.

Smallest fix: reword to "pre and post maps with timestamps; mid-run checks are computed and only a
mismatch is recorded", or append each mid snapshot to the step record.

### F4 — MEDIUM — row 5's fix is contradicted at the code level, and the red state recurred after the commit

Anchor: `corpus/lessons/round-17.md:77`.

**OBS**:

```
$ git log -1 --format='%ci' da64646            → 2026-10-20 11:06:06 -0300
$ stat -c '%y %n' .ufo/waves/round-16/__pycache__/selection.cpython-314.pyc
  2026-10-20 11:08:56 ... selection.cpython-314.pyc
$ stat -c '%y %n' .ufo/waves/round-17/tools/__pycache__/pins.cpython-314.pyc
  2026-10-20 11:10:08 ... pins.cpython-314.pyc
$ grep -c 'dont_write_bytecode' .ufo/waves/round-17/tools/predict.py .ufo/waves/round-17/tools/carrier-run.py
predict.py:0
carrier-run.py:0
```

"Removed before commit" was true at 11:06 only: both pycs postdate the commit and are still present at
review time (untracked; `.gitignore:1` is `__pycache__/`). The second file is an r17 tool module imported
without `-B` after the fix landed. The row's "predict/carrier-run import with bytecode writes disabled" is
false as written: neither sets `sys.dont_write_bytecode`, the guard `w1/CriticNoHarm.md` F6 recommended;
only the `-B` flag in documented invocations protects, and the recurrence shows a seat invocation is not
covered (INF). Mechanism reproduced independently (**OBS**): an `importlib` `spec_from_file_location` +
`exec_module` under `python3 -I` creates `__pycache__/selection.cpython-314.pyc`; adding `-B` creates
nothing. (Plain `python3 -I -c "import selection"` fails with `ModuleNotFoundError`; the row's wording
should name the import-by-path form.)

Smallest fix: set `sys.dont_write_bytecode = True` in `predict.py` and `carrier-run.py` (and any other
importer), record the 11:08:56 / 11:10:08 recurrences in the row, and delete the two pycs. Attribution
of the creates to a specific process is inference; the timestamps and presence are observed.

### F5 — LOW/MEDIUM — row 4's stale premise is still live in the shared contract

Anchors: `corpus/lessons/round-17.md:76`; `.ufo/waves/round-17/contract.md:65`.

**OBS**:

```
$ grep -n 'fromVersionString' .ufo/waves/round-17/contract.md
65: Normalize exactly as Ghidra's `GoVer.parse`/`fromVersionString` would ...
$ unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
    ghidra/app/util/bin/format/golang/GoVer.java | grep -n 'static GoVer'
46 parse(String); 58 parseWildcardPatch(String); 89 fromProgramProperties(Program)
→ no fromVersionString
```

The fix itself is real: `predict.py:100-102,194-195` strips `go` before `GoVer.parse`, matching
`GoBuildInfo.java:488-489` (verified in the installed source). But the contract that every wave-1 executor
worked from still names the nonexistent method, and no correction line or amendment names
`contract.md:65`. A stale premise that survives in the shared contract is not discharged by fixing one
consumer.

Smallest fix: append one line naming `contract.md:65` and `GoVer.parse` (append-only; filed bytes need no
rewrite), or correct the contract line if lane-internal edits are permitted.

### F6 — LOW — four `captured-by` cells are not a criterion, protocol rule, or `none`

Anchors: `corpus/lessons/round-17.md:75` ("author-side critics this round"), `:76` ("author-side review"),
`:80` ("outside closure (route) vs this lane's search"), `:81` ("host job cap, not a lane gate").
`CORPUS.md:171-176` requires "the `QUALITY.md` criterion or protocol rule that should have caught it, or
`none`". These four name actors or explanations, not a rule; none of them is `none`.

Smallest fix: prefix rows 75/80/81 with `none — `; row 76 can cite `QUALITY #1` (a nonexistent method
name is not a resolvable source).

### F7 — LOW — row 9's "(job cap 100)" is not in the cited evidence

Anchor: `corpus/lessons/round-17.md:81`.

**OBS**: `.ufo/waves/round-17/wave1-dispatch-attempts.json` contains only `{try, at, refused}` with
`refused` 78, 78, 0; `wave1-result.txt` says "Spawned 78 background agents"; `git grep -nI 'job cap'
da64646 -- .ufo/waves/round-17` prints nothing (count 0), and no committed file names "100" as the cap.
The two refusals and the 78 spawned are supported; the cause and the number are not in the pointer. (An
uncommitted w2 draft, `.ufo/waves/round-17/w2/draft-scorecard.md:68`, says "host job cap (78 each)" — no
cap number — and is not evidence at the revision.)

Smallest fix: drop "(job cap 100)" or cite the dispatch error text that names the cap.

### F8 — LOW — three claimed repairs name no red-before state (CORPUS rule), though two exist

Anchors: `corpus/lessons/round-17.md:76` (row 4), `:79` (row 7), `:80` (row 8); rule at
`CORPUS.md:186-190` ("A fix is shown able to fail before it counts ... a claimed repair ships one
red-before state in which the same command exits non-clean for the named reason").

**OBS**: rows 4, 7 and 8 are claimed repairs but carry no "Able to fail" line. Two red-before states exist
but are not cited:

- row 4 (**OBS**): `python3 -B -c "import importlib.util; s=importlib.util.spec_from_file_location('p',
  '.ufo/waves/round-17/tools/predict.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m);
  print(m.gover_parse('go1.27.2',0), m.gover_parse('1.27.2',0))"` → `None (1, 27, 2)` — the strip is what
  makes input parse; `predict.py --selftest` does not assert the unstripped failure.
- row 8: `temporal-sweep.py --selftest` case 3 is exactly the deleted-site red state the row's fix
  depends on.
- row 7: no red-before exists — `carrier-run.py --selftest` has 2 cases (happy path; nonzero analyze),
  neither exercises a foreign/unbound session or the `len(bound) != expected` exit-2 path.

Smallest fix: append one line per row naming the command and observed output; add a carrier-run selftest
case with zero/foreign bound sessions for row 7.

## Red-state reproduction (acceptance item)

| row | claimed red state | command | observed | verdict |
|---|---|---|---|---|
| 1 | `pins.py --selftest` mutated file → compare exit 1 naming path | `python3 -B .ufo/waves/round-17/tools/pins.py --selftest` | `red case observed: compare exit 1 names /tmp/pins-selftest-*/a.txt`; `SELFTEST: CLEAN cases=7`, exit 0 | REAL |
| 2 | baseline run shows 2 variants | `python3 -B .../invocation-audit.py --root . --rev b563c79` | `rows 7, exercised_match 5, unlabelled_variant 2` | REAL at baseline; post-fix claim FALSE (F1) |
| 3 | selftest cases 2–3: path-only marker and deleted site stay unqualified | `python3 -B .../temporal-sweep.py --selftest` | `SELFTEST: CLEAN cases=6`; source cases 2 and 3 assert exactly that | REAL |
| 5 | `python3 -I` without `-B` recreates the pyc | copy r16 `selection.py` to `/tmp/pyc-test/`, then `python3 -I -c "import importlib.util; s=importlib.util.spec_from_file_location('s','/tmp/pyc-test/selection.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)"` | creates `/tmp/pyc-test/__pycache__/selection.cpython-314.pyc`; with `-B`: none | REAL (import-by-path form) |
| 6 | forced route → compare exit 1; three fields → exit 0 | see F2 commands | exit 1 / exit 0 | REAL mechanism; retention FALSE (F2) |

Rows 4, 7, 8, 9 make no "able to fail" claim (F8 covers the red-before gap for rows 4/7/8). Row 7's
verification claim is real (below).

## Bounded no-findings (what I checked and did not find broken)

- **Classes** (all 9 rows; extraction `sed -n '73,81p' ... | awk -F'|' '{print $2}'`): `vacuous`,
  `number-drift`, `survivor`, `reference-drift`, `scope`, `stale-premise`, `landing`, `attribution`,
  `provider` — every token is in `CORPUS.md:174-176`; the two compounds (`vacuous / number-drift`,
  `survivor / reference-drift`) are two vocabulary tokens, matching r16 precedent.
- **Evidence pointers** row by row (OBS):
  - row 1 `.ufo/waves/round-16/verification.json:419` is exactly `"pins_unchanged_during_run": true,`
    (the 20-entry map is lines 397-418); the three site lines exist at `LOG.md:2012`,
    `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`.
  - row 2 `SKILL.md:448` (citation-drift) and `:449` (custody-pair) exist at `b563c79` with the
    relative, non-`-I` commands described; audit classes both `unlabelled_variant`.
  - row 3 `contract.md:91-95` is the old site list + regex; reproduced count is exactly 2 of 4 (hits
    `corpus/lessons/round-16.md:154` and `.ufo/waves/round-16/verification.json:419`; misses
    `LOG.md:2012` "unchanged across execution" and the knowledge file).
  - row 4 `contract.md:65` exists and names `fromVersionString`; w1 `ReviewContract`, `ScoutGoVer`,
    `ScoutGoRttiMapper` exist.
  - row 6 `GoRttiMapper.java:179-180` is the requested-label echo (`Using Go API snapshot for version %s`,
    reached at 174-181 on both exact and fallback paths); w1 `CriticC2Novelty` V1 and
    `ConnRequestedLabel` exist; `GoApiSnapshot.java:148-166` is the WARN-vs-INFO choice.
  - row 7 `contract.md:36-39` is the new-dir poll; w1 `SentinelPollRace` F1 and `SentinelCarrierSafety` F1
    exist.
  - row 8 `round-16-verifier-spotcheck.md:183` names the scorecard; `git show b563c79:SCORECARD.md |
    grep -ciE '<site regex>'` → 0; the knowledge entry is not named there.
  - row 9 `wave1-dispatch-attempts.json` exists with 78/78/0 (see F7 for the unsupported cap).
  - row 5's pyc path exists but with mtime 11:08:56, not the row's 10:32 (F4); the durable pointer is the
    cited `w1/CriticNoHarm.md` F6, which does record 10:32:31.
- **Row 7 fix verified** (OBS): all 8 receipts have `bound_sessions` length 1, `unbound_sessions` `[]`,
  `pins_compare.equal true`, and `carrier-run.exit` 0; `bind_session` (`carrier-run.py:124-139`) checks
  both `Using log file: <dir>/ghidra.log` and `IMPORTING: file://<dir>/target-<sha256[:12]>.bin`.
- **Row 8's "not copied from a prose list"** verified: `temporal-sweep.py --sites-rev b563c79` reads sites
  at the baseline and its selftest case 3 hides a deleted site from the count.
- **Corrections append-only and line-exact** (OBS): `temporal-sweep.py --root . --rev da64646
  --sites-rev b563c79` → `sites 4, corrected 4, unqualified 0, new_unqualified_at_rev 0`, each corrected
  by `LOG.md:2059-2062`; `git diff --stat b563c79 da64646 -- corpus/lessons/round-16.md
  corpus/knowledge/2026-10-20-r16-go-selection-preview.md .ufo/waves/round-16/verification.json` is empty,
  and the LOG.md diff is a pure append.
- **Widened sweep behavior**: `find_sites` joins the hard-wrapped next line
  (`temporal-sweep.py:116-131`), matching the knowledge file's line 95/96 wrap; the correction match
  requires the exact `file:line` token plus `temporal stability not evidenced`
  (`temporal-sweep.py:164-171`), and selftest cases 2-3 cover the path-only and deleted-site red states.

## Residual risk and gaps

- Reviewed revision `da64646` only. `w2/citation-drift-head.json` and `w2/DraftLessonEvidence.md` are
  untracked, so they are not evidence at the revision; if wave 2 commits a `verification.json` with the
  missing argv, F1/F2 become revision-timing defects, but the lesson's past-tense claims remain false at
  `da64646`. The working tree has since diverged from the revision (`M .ufo/waves/round-17/run-carriers.sh`,
  new untracked `.ufo/waves/round-17/verify.py`), so F1/F2 must be re-judged at the integration commit.
- I did not run REA analyze/search/decompile, Ghidra, or any carrier, so the Go route/selection claims
  were not re-derived here; this seat judged only the Mistakes table's internal evidence and fix claims.
- Attribution of the two post-commit pyc creations to a particular process is inference (no audit trail);
  their presence, names, sizes, and mtimes are observed.
- No tool installs or updates were made; no pacman transaction was run.
