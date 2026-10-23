# ExecPrefreezeR31 — round-31 freeze discipline as exit codes (round-30 gates on round 31)

Seat: `KaidokuR31.ExecPrefreezeR31` (leaf executor; no subagents spawned). Lane:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only. Sandbox:
`/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecPrefreezeR31/`.

Item: run the lane's three round-30 gates on round 31 in a sandbox clone at the freeze commit,
plus each gate's `--selftest`; explain every non-zero exit from the gate's own code; list the
exact files/columns/JSON keys round 31 must commit for each gate to pass.

**No claim counter ran, no REA process ran, no carrier or mutant was read, opened or executed.**
No frozen target line was executed in this seat, so the "control met its target line" question is
not applicable here.

## 0. Environment and provenance (observations)

- Lane HEAD at seat start and at every run below: `35ba7c522dba55f9be27eb161d4254eacaa24330`
  (observed via read-only `git rev-parse HEAD`; equal to the frozen claims rev). Lane base is
  `c369242fee9f559f895e3f7956b1242076c7b1be`, per `claims.json`.
- Freeze commit is `35ba7c52...` and its message is `round-31: freeze R31-C1/C2
  (inspect-sqlite-database) — instruments, 12 carriers, 23 predictions, before receipts`
  (observed: `git log -1 --format='%H %ct %s' 35ba7c52` → ct `1792728307`).
- Sandbox clone (the `<clone>` used in every command below), created exactly as the Contract
  prescribes:
  `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q <lane> clone && env -u GIT_DIR
  -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C clone checkout -q -B ctl 35ba7c522dba55f9be27eb161d4254eacaa24330`
  → `git -C clone rev-parse HEAD` printed `35ba7c522dba55f9be27eb161d4254eacaa24330`
  (observation, 2026-10-23T04:09Z). All six runs below used that clone at that rev; the
  axis-fit run's own output confirms `"rev": "35ba7c522dba55f9be27eb161d4254eacaa24330"`.
- Working directory for every command:
  `cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecPrefreezeR31` and `TMPDIR=$PWD/tmp`.
  `python3 -I -B` was used verbatim; each run was wrapped in `timeout 300`.
- UTC timestamps below are the `START`/`END` markers written into each captured log at run time
  (observations); for the supplementary probes, `START` was not written, so the file mtime is
  given (observation, labelled).

## 1. The six runs (command, stdout, exit, UTC)

### 1.1 prefreeze gate

Command (as executed):

```
TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/prefreeze-gate.py \
  --root clone --round 31 --rev HEAD
```

Window: `2026-10-23T04:10:11Z` → `2026-10-23T04:10:12Z`. Exit: **0** (observation).

Full stdout:

```
prefreeze round=round-31 freeze=35ba7c522dba55f9be27eb161d4254eacaa24330 rev=35ba7c522dba55f9be27eb161d4254eacaa24330 claims=.ufo/waves/round-31/claims.json
pins=5 present=5 unhashed=0 mismatch=0 data_before_freeze=0 tools_named=2 tools_unpinned=0 findings=0
verdict=CLEAN
```

Log: `out/prefreeze.log`, sha256 `895a129274ea76bd6555ad5937a62c669d80c3f9b7a941e2f7636dd16cdee1df`.

### 1.2 axis-fit gate

Command (as executed):

```
TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/axis-fit-gate.py \
  --root clone --round 31 --rev HEAD
```

Window: `2026-10-23T04:10:11Z` → `2026-10-23T04:10:12Z`. Exit: **1** (observation).

Full stdout (one JSON line, 887 bytes):

```
{"axis_claims": [{"axis": "coverage", "claim": "R31-C1", "surface": "ok", "unmoved_command": "ok"}, {"axis": "depth", "claim": "R31-C2", "surface": "ok", "unmoved_command": "ok"}], "claim": "R30-axis-fit-gate", "claims_file": ".ufo/waves/round-31/claims.json", "findings": [{"finding": "RECEIPTS_ABSENT", "path": ".ufo/waves/round-31/controls/receipts.tsv"}], "notes": [], "receipts": {"path": ".ufo/waves/round-31/controls/receipts.tsv", "present": false}, "required_controls": ["do-nothing", "junk-row (entry + PROVINCE/SKILL rows without envelopes)", "all-false (committed refusal envelopes for C1; all-accept for C2)", "no-reader (envelopes fabricated from the oracle or the predictions, never produced by REA)", "shortcut keyed on ids/labels (another carrier's or request's envelope under the id)"], "rev": "35ba7c522dba55f9be27eb161d4254eacaa24330", "round": 31, "verdict": "FAIL"}
```

Log: `out/axisfit.log`, sha256 `d0f276e1ba18f605b3e7847f97369f44ee069c43c858f5985ffe2a676dfc020a`.

### 1.3 settle gate

Command (as executed):

```
TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/settle-gate.py \
  --root clone --round 31
```

Window: `2026-10-23T04:10:11Z` → `2026-10-23T04:10:12Z`. Exit: **2** (observation).

Full stdout:

```
settle: ERROR no swarm-registry.json under .ufo/waves/round-31
```

Log: `out/settle.log`, sha256 `3b63ec8175428a73d70330202354b80023f7c77c4f50a436947a59007527f83d`.

NOTE: `settle-gate.py` has no `--rev` option (its `main()` defines only `--root`, `--round`,
`--selftest`, lines 359-375); passing `--rev` would be an argparse usage error (exit 2). The
assignment's settle command (no `--rev`) is the only valid form.

### 1.4 prefreeze `--selftest`

Command (as executed):

```
TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/prefreeze-gate.py --selftest
```

Window: `2026-10-23T04:10:17Z` → `2026-10-23T04:10:18Z`. Exit: **0** (observation).

Full stdout:

```
ok clean got=code=0 codes=[]
ok round_arg_form got=code=0 codes=[]
ok round_invalid got=code=2 codes=[]
ok pin_absent got=code=1 codes=['PIN_ABSENT']
ok pin_mismatch got=code=1 codes=['PIN_MISMATCH']
ok r29_keys got=code=1 codes=['PIN_ABSENT']
ok r30_list got=code=0 codes=[]
ok r30_list_absent got=code=1 codes=['PIN_ABSENT']
ok envelope_at_freeze got=code=1 codes=['DATA_BEFORE_FREEZE']
ok runs_before_freeze got=code=1 codes=['DATA_BEFORE_FREEZE']
ok data_after_freeze got=code=0 codes=[]
ok other_round_data got=code=0 codes=[]
ok tool_unpinned got=code=1 codes=['TOOL_UNPINNED']
ok tool_pinned got=code=0 codes=[]
ok tool_superseded got=code=0 codes=[]
ok tool_supersession_no_reason got=code=1 codes=['TOOL_UNPINNED']
ok late_pin_not_counted got=code=1 codes=['TOOL_UNPINNED']
ok no_claims got=code=2 codes=[]
ok bad_json got=code=2 codes=[]
ok not_repo got=code=2 codes=[]
selftest cases=20 failures=0
```

Log: `out/prefreeze-selftest.log`, sha256 `e1f31c9d17e7d39899bcdfb20b5f6170c4486877a434d844bf26535e8ea5044d`.

### 1.5 axis-fit `--selftest`

Command (as executed):

```
TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/axis-fit-gate.py --selftest
```

Window: `2026-10-23T04:10:17Z` → `2026-10-23T04:10:18Z`. Exit: **0** (observation).

Full stdout:

```
ok green-basic exit=0 findings=-
ok green-pre-data-no-envelopes exit=0 findings=-
ok green-other-axis-only exit=0 findings=-
ok red-surface-missing exit=1 findings=SURFACE_MISSING
ok red-surface-blank exit=1 findings=SURFACE_EMPTY
ok red-unmoved-missing exit=1 findings=UNMOVED_COMMAND_MISSING
ok red-receipts-absent exit=1 findings=RECEIPTS_ABSENT
ok red-receipts-after-envelopes exit=1 findings=RECEIPTS_NOT_BEFORE_ENVELOPES
ok red-receipts-same-commit exit=1 findings=RECEIPTS_NOT_BEFORE_ENVELOPES
ok red-met-target-yes exit=1 findings=MET_TARGET_YES
ok red-control-missing exit=1 findings=CONTROL_MISSING
ok red-control-head-ambiguous exit=1 findings=CONTROL_MISSING
ok red-header-invalid exit=1 findings=CONTROL_MISSING,RECEIPTS_HEADER_INVALID
ok red-row-invalid exit=1 findings=RECEIPTS_ROW_INVALID
ok red-counter-exit-not-int exit=1 findings=RECEIPTS_ROW_INVALID
ok red-claims-absent exit=2 findings=-
ok red-claims-invalid-json exit=2 findings=-
ok red-not-a-repo exit=2 findings=-
selftest cases=18 failures=0
```

Log: `out/axisfit-selftest.log`, sha256 `b1b4f2b331ec049a8715b7d2da6647de2f1758042fb8dab3ff86059ac07bf2ff`.

### 1.6 settle `--selftest`

Command (as executed):

```
TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/settle-gate.py --selftest
```

Window: `2026-10-23T04:10:17Z` → `2026-10-23T04:10:17Z`. Exit: **0** (observation).

Full stdout:

```
ok green-clean got=0 want=0 code='settle: PASS'
ok red-missing-row got=1 want=1 code='MISSING_ROW w1/ScoutD'
ok red-returned-report-absent got=1 want=1 code='REPORT_ABSENT w1/ExecA'
ok red-r28-report-changed-after-filing got=1 want=1 code='REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix'
ok red-cancelled-report-without-note got=1 want=1 code='REPORT_WITHOUT_NOTE w1/CriticC'
ok green-cancelled-report-with-note got=0 want=0 code='settle: PASS'
ok red-no-ledger got=1 want=1 code='MISSING_LEDGER'
ok green-qualified-keys-two-waves got=0 want=0 code='settle: PASS'
ok error-ambiguous-bare-key got=2 want=2 code='is ambiguous'
ok error-bad-status got=2 want=2 code='status'
ok error-bad-sha got=2 want=2 code='not a sha256'
ok error-duplicate-row got=2 want=2 code='duplicate ledger row'
ok green-stray-row-warns got=0 want=0 code='WARN STRAY_ROW Ghost'
selftest cases=13 failures=0
```

Log: `out/settle-selftest.log`, sha256 `c5f2ab9e71429aa5df70316a716ecd3305639d4dcbe6878454cde716a4d858be`.

## 2. Why each non-zero exit happens, from the gate's own code

### 2.1 axis-fit exit 1 — `RECEIPTS_ABSENT`

Observation: only finding is `RECEIPTS_ABSENT` on `.ufo/waves/round-31/controls/receipts.tsv`;
`surface` and `unmoved_command` are both `ok` for R31-C1 and R31-C2.

Code path: `audit()` collects the coverage/depth claims (line 59 `AXIS`; 213-224), then, because
`axis_entries` is non-empty, demands the receipts blob at the measured rev
(`receipts_path = '.ufo/waves/round-%d/controls/receipts.tsv' % round_no`, line 235), reads it with
`show()` (line 236) and appends `RECEIPTS_ABSENT` when it is not a blob (lines 239-240). Exit 1 is
`return result, (0 if not findings else 1)` (line 296). This is exactly the "controls not yet
committed before data" state: no receipts exist at the freeze commit. The frozen controls are
already listed in `claims.json` and are echoed verbatim in `required_controls`.

Not failing, but worth knowing: the ordering clause is **vacuous** when no envelope path is
committed (`e_add is None → receipts['ordering'] = 'no-envelopes'`, note at 251-254). So the only
current axis-fit defect is the absent receipts file; the timing clause becomes live as soon as the
first `corpus/evidence/round-31/<one-seg>/envelopes/...` path is added.

### 2.2 settle exit 2 — no registry in the clone

Observation: stdout is exactly `settle: ERROR no swarm-registry.json under .ufo/waves/round-31`.

Code path: `check()` (line 168) calls `read_registries()` (line 173); that function globs
`.ufo/waves/round-<N>/*/swarm-registry.json` (line 93) and raises
`Unevaluable("no swarm-registry.json under %s")` when the list is empty (lines 111-112);
`check()` catches `Unevaluable` and returns 2 (lines 175-176). The clean clone at the freeze commit
has no such file, because the round-31 registry is **untracked** in the lane worktree (see §3.3).

The assignment's expectation ("settle expects `.ufo/waves/round-31/settle.tsv`") is the *next*
defect once a registry is visible; in the clone the gate stops one step earlier. Proven by probe
P3 in §4: with the lane's own untracked registry copied into the clone, the same command exits 1
with 44 `MISSING_ROW` findings (one per registry member) — i.e. the ledger is the next requirement.
[Inference from code lines 188-205, not observed: in the lane, where that registry already exists
and `settle.tsv` does not, the same gate will print `MISSING_LEDGER` **plus** one `MISSING_ROW` per
member — 45 findings for the current 44-member registry.]

## 3. Exactly what round 31 must commit for each gate to pass

All line pointers are into `tools/round-30/<gate>.py` at the freeze commit. "Pass" means the gate's
own exit-0 condition.

### 3.1 prefreeze-gate.py — currently PASSES (exit 0, `verdict=CLEAN`)

Requirement (docstring lines 12-26; code 162-223):

1. **Freeze commit.** A commit reachable from `--rev` must add
   `.ufo/waves/round-31/claims.json` (line 167); the oldest such adding commit is the freeze
   (lines 178-183). Satisfied by `35ba7c52...` (observation). If the L1 never amends that commit,
   this stays the freeze.
2. **Pins.** The claims object at the **freeze commit** is scanned for the four pin keys
   `instruments`, `frozen_inputs`, `loaded_by_counter`, `producers_not_counters`
   (`PIN_KEYS`, line 51; extraction 95-124):
   - a **string** value is a sha256 pin: the path must be a blob at the freeze commit
     (else `PIN_ABSENT`, line 195) with exactly that digest (else `PIN_MISMATCH`, 200-202);
   - a **list** value records paths with no digest: each must be a blob at the freeze commit
     (presence only, counted `unhashed`, 198-199);
   - a **dict of list** values behaves like the list case per item (119-122).
   Round 31 currently pins 5 paths (`instruments`: 3 tools; `frozen_inputs`: `carriers.tsv`,
   `predictions.tsv`), all hashed and present (observation: `pins=5 present=5 unhashed=0
   mismatch=0`). **Every tool or frozen input round 31 relies on must be committed in or before
   the freeze commit with its sha256 in `instruments`/`frozen_inputs`.**
3. **No data before freeze.** No path under `corpus/evidence/round-31/` that has an `envelopes`
   directory segment or is named `runs.tsv` may be added at or before the freeze commit
   (docstring 19-21; `is_data_path` 124-131; `data_before_freeze` 127-140; finding 204-207).
   Currently 0 (observation). Consequence: **do not amend/rebase the freeze commit to include
   envelopes or `runs.tsv`**; commit data strictly after it. [Inference from lines 128-130: the
   walk is `git log ... <freeze>`, so data added after the freeze is invisible to this clause —
   re-running the gate at a later `--rev` stays clean for data, which the selftest
   `data_after_freeze` case (line ~364) also encodes.]
4. **Tool references in claim text.** Every string matching
   `tools/[A-Za-z0-9._/-]+\.(py|sh|mjs|js)` anywhere inside a **claim's** values must be
   digest-pinned in the claims file at the freeze commit, or named in
   `instrument_supersessions` as `{"path": ..., "reason": "<nonempty>"}` in the claims file at the
   freeze **or** at `--rev` (regex 52; claim strings 209; supersessions 143-159, 210-215).
   Note the asymmetry: a path pinned only in a **list** is `unhashed` and does **not** satisfy
   `TOOL_UNPINNED` — the set used is `{path for path, digest in pins.items() if digest is not
   None}` (line 211). Currently `tools_named=2`, `tools_unpinned=0` (observation). The two named
   tools are the C1 and C2 counters; `tools/round-31/sqlite_oracle.py` is pinned but not named in
   claim text, so it is not subject to this clause.
5. **Exit semantics.** 0 clean, 1 any finding, 2 unevaluable (root not a repository top, no freeze
   commit, unreadable claims, bad `--round`; docstring 32-34; `main` 466-475).

### 3.2 axis-fit-gate.py — currently FAILS on exactly one missing file

Requirement (docstring 12-26; code 193-296):

1. **Claims at `--rev`.** `.ufo/waves/round-31/claims.json` must exist and parse at the measured
   rev with a `claims` list (lines 198-208). Every claim whose `axis` matches
   `^(coverage|depth)\b` (line 59) must carry a **nonempty string** `surface` and a **nonempty
   string** `unmoved_command` (field_state 127-131; checks 221-224); `id` is the claim key used in
   receipts (214-216). Round 31 satisfies this for both R31-C1 (coverage) and R31-C2 (depth)
   (observation: both `ok`).
2. **Receipts file present at `--rev`.** `.ufo/waves/round-31/controls/receipts.tsv` must be a
   blob at the measured rev (235-240).
3. **Receipts shape.** First line is exactly the 4 tab-separated columns, in this order:
   `claim`, `control`, `counter_exit`, `met_target` (`RECEIPTS_HEADER`, line 60; comparison 140;
   `RECEIPTS_HEADER_INVALID` on mismatch). Each following nonblank row must have exactly 4 cells,
   nonblank `claim` and `control`, and an **integer** `counter_exit`; otherwise
   `RECEIPTS_ROW_INVALID` (142-156). `met_target` must be `no` case-insensitively; `yes` gives
   `MET_TARGET_YES`, anything else `MET_TARGET_INVALID` (157-163). Blank lines skipped (145-146).
4. **Rows must cover every frozen control for every coverage/depth claim.**
   `controls_required_before_data` (claims.json) must be a list of nonblank strings
   (226-233); for **each** axis claim, each frozen control name must have a row whose `claim` cell
   equals the claim `id` (`controls_for`, 168-185; loop 283-291). A row satisfies a frozen name
   when its `control` cell equals the full frozen name, **or** equals the frozen name's text
   before the first ` (` (its short head) and that head names exactly one frozen control
   (`control_head` 133-134; head rule 176-181). For round 31 this means **10 rows**: the five
   frozen controls × `R31-C1` and `R31-C2`. The unique short heads are
   `do-nothing`, `junk-row`, `all-false`, `no-reader`, `shortcut keyed on ids/labels`; both the full
   name and the head are accepted (cf. round-30's committed receipts, which use the heads).
   Missing any → `CONTROL_MISSING` (289-291).
5. **Control commit is strictly before the first envelope commit.** When any
   `corpus/evidence/round-31/<exactly one directory segment>/envelopes/<...>` path is committed
   (102-125), the committer timestamp of the commit that first added `receipts.tsv`
   (`first_add`, 92-100, 246-249) must be strictly less than the committer timestamp of the
   oldest commit that added such an envelope path (250-275). Equal or later →
   `RECEIPTS_NOT_BEFORE_ENVELOPES` (268-271); same commit also fails (selftest
   `red-receipts-same-commit`). Ancestry is reported but only a note; the hard test is the
   committer timestamp (263-272). **Therefore: commit `controls/receipts.tsv` in its own commit,
   before the first envelope commit.** Envelopes placed at
   `corpus/evidence/round-31/envelopes/...` (zero intermediate segments) would be invisible to this
   clause but are still seen by prefreeze's data rule — use `round-31/c1/envelopes/...` and
   `round-31/c2/envelopes/...`.
6. **Exit semantics.** 0 pass, 1 any finding, 2 unevaluable (claims absent/unparsable, root not a
   repo top, receipts added by a commit not in the walked history; docstring 29-33; `main`
   471-489).

### 3.3 settle-gate.py — reads the worktree only; must be run last

Requirement (docstring 13-33; code 86-232):

1. **A wave registry.** `.ufo/waves/round-31/*/swarm-registry.json` — one directory level below
   the round dir (glob, line 93). At least one must exist or the gate exits 2 (111-112). The
   registry must be a JSON object whose `members` is an **object of member names** (97-99). Optional
   `reportDir` (string, root-relative, must not escape the root — 102-108) sets the report
   directory; when absent the registry's own directory is used. **Observation:** the lane worktree
   at `35ba7c52` already has `.ufo/waves/round-31/w1/swarm-registry.json` (44 members, e.g.
   `ExecPrefreezeR31`, `CtlC1AllFalse`, `MutC1Judge`, `ScribeQualityRows`, …; `reportDir` =
   `.ufo/waves/round-31/w1`), but it is **untracked** (`git ls-files --error-unmatch` → "did not
   match any file(s) known to git"), which is why a clean clone cannot evaluate this gate. The gate
   itself reads the worktree, so it is evaluable in the lane without committing the registry; if
   the L1 wants it evaluable from a clone, the registry must be committed.
2. **The ledger.** `.ufo/waves/round-31/settle.tsv` (line 119). Blank lines and lines starting
   with `#` are ignored (32, 121-124). A **header line is required** (129-130), tab-separated, and
   it must contain, by name, the columns `name`, `status`, `utc`, `report_sha256`
   (`REQUIRED`, line 68; check 131-133). Column order is free and unknown columns are ignored
   (docstring 21-23; read by name at 134). An optional `note` column is the documented 5th column
   (17-29).
3. **Rows.** One row per dispatched seat:
   `name<TAB>status<TAB>utc<TAB>report_sha256[<TAB>note]`.
   - `name`: nonempty and unique; else exit 2 (141-146). A row key is the bare member name, or
     `<wave>/<name>` where the wave is the registry's directory name (docstring 28-31). A bare key
     for a name that appears in more than one registry is refused with exit 2 (194-201). Round 31
     has one registry, so bare names work; `w1/<name>` also works.
   - `status`: exactly one of `returned`, `cancelled`, `dead` (`STATUSES`, line 67; 147-148);
     anything else exits 2.
   - `utc`: ISO-8601 Zulu matching `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$`
     (`UTC_RE`, line 70; 149-150), e.g. `2026-10-23T04:20:00Z`.
   - `report_sha256`: 64 hex chars, case-insensitive (lower-cased at 151; `SHA256_RE`, line 69;
     154-155). `-` or empty means "no report" and is legal **only** for `cancelled`/`dead`; a
     `returned` row must carry a sha256 (156-157).
   - `note`: optional; treated as present when nonempty and not `-` (158-160).
   - A row may not have more tab fields than the header (137-138, exit 2).
4. **Report bytes must agree with the ledger.** For every registry member the report is
   `<reportDir>/<name>.md` (docstring 15-16; 207). `status=returned` → the file must exist and its
   sha256 must equal `report_sha256` (`REPORT_ABSENT` 216/219; `REPORT_SHA_MISMATCH` 220-221).
   `status=cancelled|dead` → if a report exists, the row must carry a nonempty note
   (`REPORT_WITHOUT_NOTE`, 222-223). A row that settles no registry member prints
   `WARN STRAY_ROW` and does **not** fail (44, 224-225). A member with no row → `MISSING_ROW`
   (205); no ledger at all → `MISSING_LEDGER` (189).
5. **Exit semantics.** 0 all rows agree (`settle: PASS`, 231-232); 1 any finding
   (`settle: FAIL (N findings)`, 228-230); 2 unevaluable (root not a directory 169-171; round dir
   absent 88-90; no registry 111-112; unreadable/malformed registry 94-99; ledger header/row
   violations 129-157; ambiguous bare key 199-201). `main()` accepts `--round N` or `round-N`
   (364-376).
6. **Timing.** The gate reads the **worktree**, not Git, and compares against current report bytes,
   so it must be the last gate run before filing: a report rewritten after the ledger row is
   written produces `REPORT_SHA_MISMATCH` (docstring 49-51; round-28 shape, selftest 300-304).

### 3.4 One-line filing checklist for the L1 (derived from the above)

- [x] Freeze commit `35ba7c52...` adds `claims.json`, pins all 5 instruments/frozen inputs, no
      envelope or `runs.tsv` at or before it — prefreeze exit 0 (observed).
- [ ] Commit `.ufo/waves/round-31/controls/receipts.tsv` **first**, header
      `claim⇥control⇥counter_exit⇥met_target`, 10 rows = {`do-nothing`, `junk-row`, `all-false`,
      `no-reader`, `shortcut keyed on ids/labels`} × {`R31-C1`, `R31-C2`}, `counter_exit` integer,
      `met_target` `no`. Commit it **before** the first envelope commit (strictly earlier
      committer timestamp, separate commit).
- [ ] Add envelopes only under `corpus/evidence/round-31/c1/envelopes/...` and
      `corpus/evidence/round-31/c2/envelopes/...` after the receipts commit.
- [ ] Write `.ufo/waves/round-31/settle.tsv` with header `name⇥status⇥utc⇥report_sha256⇥note`
      (name-keyed columns; order free), one row per member of
      `.ufo/waves/round-31/w1/swarm-registry.json` (44 at the time of observation), `utc` ISO-8601
      Zulu, `report_sha256` 64 hex or `-` for cancelled/dead, `note` when a cancelled/dead seat
      left a report.
- [ ] Every member's `<reportDir>/<name>.md` exists and hashes to its row; run settle-gate last,
      immediately before the filing commit; do not rewrite a report afterwards.
- [ ] Re-run prefreeze at the final rev: data added after the freeze does not flag, and the pins
      stay freeze-scoped [inference from lines 128-130, 190-203].

## 4. Supplementary shape probes (sandbox only; not lane state, not claim evidence)

These are gate-shape experiments in my scratch clones. They are **not** round-31 evidence and not
control receipts; they only prove that the requirement lists in §3 are exact.

### P1 — axis-fit accepts a receipts-only tree (10 synthetic rows, no envelopes)

- Setup: in `clone` (at freeze), wrote a synthetic
  `.ufo/waves/round-31/controls/receipts.tsv` with header + 5 frozen controls × 2 claim ids, all
  `counter_exit=1`, `met_target=no`; committed (commit `77d4a865fd61f0cb53f34f1100e0c7a4742a99ab`).
- Command: `TMPDIR=$PWD/tmp timeout 300 python3 -I -B clone/tools/round-30/axis-fit-gate.py
  --root clone --round 31 --rev HEAD`
- Exit: **0** (observation; log mtime `2026-10-23T04:11:05Z`). Verdict `PASS`, `findings: []`,
  `receipts.rows = 10`, `receipts.ordering = "no-envelopes"`, note
  `no envelope path is committed yet: the ordering clause is vacuous`.
- Log: `out/probeA-axisfit.log`, sha256 `892817a3afac1d68beeef3ba49ec8af5c1ad339265672599bae7214e5da7bd9d`.
  Conclusion (observation): RECEIPTS_ABSENT is the **only** axis-fit defect; a 10-row receipts
  file of exactly that shape makes the gate pass at the freeze claims.

### P2 — axis-fit rejects receipts later than the first envelope

- Setup: `clone2` at freeze; first commit adds `corpus/evidence/round-31/c1/envelopes/probe.json`
  with `GIT_COMMITTER_DATE='2026-01-01T00:00:00 +0000'` (commit `aed13c50...`), second commit adds
  the same synthetic 10-row receipts with `GIT_COMMITTER_DATE='2026-01-01T00:01:00 +0000'`
  (commit `8f7e2bf3...`).
- Command: same axis-fit gate, `--root clone2 --round 31 --rev HEAD`.
- Exit: **1** (observation; log mtime `2026-10-23T04:11:21Z`). Finding
  `RECEIPTS_NOT_BEFORE_ENVELOPES`, `receipts.committer_ct = 1767225660`,
  `envelopes.committer_ct = 1767225600`, `ancestor_of_first_envelope: false`.
- Log: `out/probeB-ordering.log`, sha256 `ad64161edd939deb2d6a789c8f002fa9cc2e6ca60ef705afbcecf7b0605a6196`.
  Conclusion (observation): the ordering test is the strict committer-timestamp comparison, exactly
  as §3.2(5) says.

### P3 — settle passes on a well-formed registry+ledger, and the lane registry is the next step

- P3a: in `clone`, wrote `.ufo/waves/round-31/w1/swarm-registry.json` (one member `ProbeSeat`,
  `reportDir` `.ufo/waves/round-31/w1`), `.ufo/waves/round-31/w1/ProbeSeat.md`, and
  `.ufo/waves/round-31/settle.tsv` with header + one `returned` row whose sha256 equals the report.
  Command: `python3 -I -B clone/tools/round-30/settle-gate.py --root clone --round 31`. Exit **0**
  (observation; log mtime `2026-10-23T04:11:05Z`): `settle: round-31 ... registries=1 members=1
  ledger=.ufo/waves/round-31/settle.tsv rows=1` then `settle: PASS`.
  Log: `out/probe-settle.log`, sha256 `b5d68ee6290c13357a4686437cf59c158e751c3811e7e09394172550425f81b8`.
- P3b: copied the lane's untracked `.ufo/waves/round-31/w1/swarm-registry.json` (44 members) into
  `clone` and re-ran the same command. Exit **1** (observation; log mtime
  `2026-10-23T04:11:51Z`): `registries=1 members=44 ... rows=1`,
  `settle: WARN STRAY_ROW w1/ProbeSeat`, 44 × `settle: MISSING_ROW w1/<member>`,
  `settle: FAIL (44 findings)`.
  Log: `out/probe-settle-lane-registry.log`, sha256 `6f0638cce80a9596674b4aed23716bf5ca33bf52937d5f6981b46266e7273803`.
  Conclusion (observation): with the lane registry visible, the gate's next demand is one ledger row
  (+ a matching report) for each of the 44 members; and it reads the worktree, so the registry need
  not be committed for the lane run to be evaluable.

## 5. Verdicts on the three gates as round-31 controls

| Gate | Round-31 result in the clone | Verdict |
|---|---|---|
| prefreeze-gate | exit 0, `verdict=CLEAN`, `findings=0` | **holds** (freeze is pin-complete and data-free) |
| axis-fit-gate | exit 1, `RECEIPTS_ABSENT` only | **fails as predicted** (pre-data controls not yet committed); fixed by §3.2 |
| settle-gate | exit 2, `no swarm-registry.json` (clean clone) | **could-not-evaluate in the clone**; lane worktree has the untracked registry, so the lane run will report at least `MISSING_LEDGER` |

All three `--selftest` runs exit 0 with 20/18/13 cases and 0 failures (observation), so the gates
themselves are sound on this host.

## 6. Risks and blockers

- R1 (risk, observation): the round-31 registry is untracked at lane HEAD; a clone-based settle run
  can never see it. The gate reads the worktree, so the lane run is fine, but the L1 should either
  commit the registry or record that settle is worktree-scoped.
- R2 (risk, inference): axis-fit ordering is by committer timestamp. If receipts and the first
  envelope land in the same commit, or receipts land later (e.g. a rebase/amend reordering), the
  gate fails even though the content is correct. Commit receipts first, separately.
- R3 (risk, observation): the ledger needs a row for every registry member (44 at observation). A
  member added to the registry after the ledger is written becomes `MISSING_ROW`. Generate the
  ledger from the final registry.
- R4 (risk, inference): `counter_exit 0` with `met_target no` only produces a note (lines 259-260);
  the gate cannot detect a control that actually met the target line but was recorded as `no`.
  Record `no` only when the control genuinely misses the target line.
- R5 (risk, inference): do not amend/rebase the freeze commit to add data — prefreeze's data clause
  walks to the freeze and would then see the data at the freeze.
- R6 (risk, observation): settle-gate has no `--rev`; a `--rev` argument is an argparse error
  (exit 2) and would be misread as a gate failure.
- R7 (risk, observation): settle must run last; it hashes current report bytes (round-28 defect
  shape). Any post-gate report rewrite turns the pass red.
- Blockers: none.

## 7. Tooling, sources, REA

- Installs/updates: **none** (the three gates need only `python3` and `git`, both already present;
  `python3 -I -B` used as frozen).
- Primary sources opened: **none** (this seat reads only lane Git objects and its own sandbox
  clones; no HTTP fetch, no browser).
- REA: **not run** (no claim counter and no probe required it; no carrier or mutant was touched).
- Lane writes: only this report at `.ufo/waves/round-31/w1/ExecPrefreezeR31.md`. No git/jj write in
  the lane or the fleet repo; the only commits were made inside the scratch clones.

## 8. Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecPrefreezeR31/`)

| Artifact | sha256 / identity |
|---|---|
| `out/prefreeze.log` | `895a129274ea76bd6555ad5937a62c669d80c3f9b7a941e2f7636dd16cdee1df` |
| `out/axisfit.log` | `d0f276e1ba18f605b3e7847f97369f44ee069c43c858f5985ffe2a676dfc020a` |
| `out/settle.log` | `3b63ec8175428a73d70330202354b80023f7c77c4f50a436947a59007527f83d` |
| `out/prefreeze-selftest.log` | `e1f31c9d17e7d39899bcdfb20b5f6170c4486877a434d844bf26535e8ea5044d` |
| `out/axisfit-selftest.log` | `b1b4f2b331ec049a8715b7d2da6647de2f1758042fb8dab3ff86059ac07bf2ff` |
| `out/settle-selftest.log` | `c5f2ab9e71429aa5df70316a716ecd3305639d4dcbe6878454cde716a4d858be` |
| `out/probeA-axisfit.log` | `892817a3afac1d68beeef3ba49ec8af5c1ad339265672599bae7214e5da7bd9d` |
| `out/probeB-ordering.log` | `ad64161edd939deb2d6a789c8f002fa9cc2e6ca60ef705afbcecf7b0605a6196` |
| `out/probe-settle.log` | `b5d68ee6290c13357a4686437cf59c158e751c3811e7e09394172550425f81b8` |
| `out/probe-settle-lane-registry.log` | `6f0638cce80a9596674b4aed23716bf5ca33bf52937d5f6981b46266e7273803` |
| `clone/` (sandbox clone; HEAD after P1 probe) | commit `77d4a865fd61f0cb53f34f1100e0c7a4742a99ab` |
| `clone2/` (sandbox clone for P2) | commit `8f7e2bf3c238122d448edc0a104745bfb92e3d1d` |
| `tmp/` | scratch `TMPDIR` for the selftests |
