# R31-C1 all-false control — CtlC1AllFalse

- Seat: `KaidokuR31.CtlC1AllFalse` (critic/control, leaf).
- Lane base `c369242fee9f559f895e3f7956b1242076c7b1be`; freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`.
- Sandbox clone `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/clone`, branch `ctl`, base commit `35ba7c5…`, control commit `bcec6566b4eaab17815e571ca0b967d8ab818a3c` (committed `2026-10-23T01:11:09-03:00` = `2026-10-23T04:11:09Z`).
- All commands below run with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset. Nothing was written inside the lane except this report; the lane was read only (`git show`, `git grep`, `sha256sum`).
- Counter under test is byte-identical to the lane's: `sha256(tools/round-31/c1-sqlite-positive.py) = 048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0` in both the lane and the clone (observed).

## Control built

At the clone HEAD (control commit), 14 paths added on top of the freeze commit, all listed by `git show --name-only`:

| Path | sha256 | Content |
|---|---|---|
| `PROVINCE.md` | `8de31d2908540a02ad2b0b8e5afa3fed6db5fb516d19c3f42f9b2714e1f18dfc` | appended `### Round-31 additions to Core` + one table row naming `inspect-sqlite-database` and the entry path |
| `corpus/knowledge/2026-10-23-r31-sqlite-positive.md` | `372789d6b123b39547e1a9f5e8a16a03e64f12a2870faf5adecc4e6ebf1ab7b5` | junk-row entry, cites `S096`, states that it commits no result and names no `evidence_id` |
| `corpus/evidence/round-31/c1/envelopes/<id>.json` × 12 | every file `f546ef05f4d7894ba9b189875a00f271ae675847dc91080381b1568320161a35` | the same REA refusal envelope copied under each of the 12 carrier ids from `carriers.tsv` |

The 12 ids (from `corpus/evidence/round-31/c1/carriers.tsv`, sha256 `46f180b837b77297cfba11f4cc805d9f849034e411c279bf5744fa6c21c19211`): `proj-341`, `proj-350`, `proj-361`, `proj-370`, `proj-371`, `chinook`, `chinook-autoinc`, `gpkg-curve`, `gpkg-curvepolygon`, `gpkg-line-zm`, `gpkg-multisurface`, `gpkg-test-gpkg-nulls`. `sha256sum envelopes/*.json | uniq -c -w64` → `12 f546ef05…`.

Refusal envelope (one run, copied 12×; 526 bytes, exit 1, captured `2026-10-23T04:11:02Z`):

```
{"ok":false,"error":{"code":"invalid_request","category":"invalid_input","message":"Analysis input is invalid. Check the arguments and try again.","retryable":true,"remediation":{"action":"Correct the listed arguments and retry."},"details":{"operation":"inspect_sqlite_database","issues":[{"path":["path"],"reason":"invalid_value","message":"Selected SQLite database does not exist: /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/nonexistent.sqlite"}]}},"meta":{"command":"inspect-sqlite-database","duration":"4ms"}}
```

Producing command (run at `2026-10-23T04:10:28Z` for the probe and again at `04:11:02Z` to capture the bytes; both exit 1):

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-sqlite-database /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/nonexistent.sqlite --format json --full-output
```

## Counter command 1 — baseline at the freeze commit (before the control commit)

Start ≈`2026-10-23T04:10:35Z`, end `2026-10-23T04:10:46Z` (10.6 s wall), exit **1**.

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/clone --rev 35ba7c522dba55f9be27eb161d4254eacaa24330
```

Full stdout (the final `EXIT=1` line is the seat's shell echo, not counter output):

```
proj-341	P1-fail	committed envelope absent
proj-350	P1-fail	committed envelope absent
proj-361	P1-fail	committed envelope absent
proj-370	P1-fail	committed envelope absent
proj-371	P1-fail	committed envelope absent
chinook	P1-fail	committed envelope absent
chinook-autoinc	P1-fail	committed envelope absent
gpkg-curve	P1-fail	committed envelope absent
gpkg-curvepolygon	P1-fail	committed envelope absent
gpkg-line-zm	P1-fail	committed envelope absent
gpkg-multisurface	P1-fail	committed envelope absent
gpkg-test-gpkg-nulls	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=0 (entry absent) province_ok=0 (no PROVINCE table row names the verb and the entry)
EXIT=1
```

Every row reached `P1-fail` only after `judge` returned `P1-pass` (the reason shown is the `committed_check` reason), i.e. the live run on all 12 immutable carriers is a positive match to the oracle and only the absent record blocks it.

## Counter command 2 — the all-false control at HEAD

Start `2026-10-23T04:11:11Z`, end `2026-10-23T04:11:25Z` (13.3 s wall), exit **1**.

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse && timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/clone/tools/round-31/c1-sqlite-positive.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/clone --rev HEAD
```

Full stdout (final `EXIT=1` line is the seat's shell echo):

```
proj-341	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-350	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-361	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-370	P1-fail	committed envelope differs from the live envelope (full comparison)
proj-371	P1-fail	committed envelope differs from the live envelope (full comparison)
chinook	P1-fail	committed envelope differs from the live envelope (full comparison)
chinook-autoinc	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-curve	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-curvepolygon	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-line-zm	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-multisurface	P1-fail	committed envelope differs from the live envelope (full comparison)
gpkg-test-gpkg-nulls	P1-fail	committed envelope differs from the live envelope (full comparison)
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
EXIT=1
```

**CONTROL CtlC1AllFalse: met=no score=0/12**

The control did not meet the target. The freezing clause is `committed_check`'s `strip_meta(committed) != strip_meta(live)` — the round-30 defect M30-3 repair. The live REA run on every immutable carrier is a genuine positive (`judge` returns `P1-pass`, oracle-exact), so the committed refusal bytes cannot stand in for it. A refusal-live variant would instead be stopped one gate earlier by `judge`'s `code != 0 or env.get("ok") is not True` clause; a refusal envelope therefore cannot pass on either path.

## Findings

### F1 — the control is caught by the full record comparison (attack verdict: the counter HOLDS)
Observation. Command 2 above, exit 1, `2026-10-23T04:11:11Z–04:11:25Z`, exact reason `committed envelope differs from the live envelope (full comparison)` on all 12 rows. Impacted axis: coverage (R31-C1). The all-false control cannot reach `pass=12` by any arrangement of committed refusal files, because the verdict is computed from a live run on the pinned carrier and the committed file must reproduce that live envelope field for field (meta excepted).

### F2 — the frozen target string is not literally produced by the counter (defect, procedural only)
Observation. `claims.json` freezes `target` as `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1, exit 0`; the counter prints `… entry_ok=1 (ok) province_ok=1 (ok)`. The parentheticals are inserted by `measure()` unconditionally (`print("carriers=%d pass=%d target=%d entry_ok=%d (%s) province_ok=%d (%s)" …)`), so the literal frozen substring `entry_ok=1 province_ok=1` never appears in any run, pass or fail. Evidence: control stdout line `carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)`, exit 1, and the pass-mode line `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)` from `write2.out` below. A literal-string acceptance check would therefore reject a genuine 12/12 pass. Impacted axis: measurement/quality, not the coverage claim itself. Correction is procedural because both the counter and the claims are frozen: accept C1 on `exit 0` plus parsed numeric fields `pass=12`, `entry_ok=1`, `province_ok=1`, never on the literal frozen substring.

### F3 — `--write-evidence` is a self-certifying mode that skips every record gate (defect, medium)
Observation. `measure(root, rev, write)` guards `committed_check` with `if verdict == LABEL and not write:`; with `--write-evidence` the committed-envelope equality and the entry-names-`evidence_id` clause are both bypassed, while the same target numbers are printed. Two independent runs at the control HEAD, with the junk entry and Core row in place and the committed envelopes still the 12 refusals:

```
cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse && timeout 900 python3 -I -B clone2/tools/round-31/c1-sqlite-positive.py --root $PWD/clone2 --rev HEAD --write-evidence
```
stdout ends `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)` / `EXIT2=0`, `2026-10-23T04:12:00Z`; and the same for `clone3` at `2026-10-23T04:12:17Z`, exit 0. After both runs `git -C clone2 status --porcelain` shows the envelopes as ` M …` (uncommitted) — so exit 0 with `pass=12` was produced with no committed record and with an entry that names no `evidence_id`. The pass count itself is real work (`judge` plus the oracle), not fabrication; what the flag drops is provenance. Impacted axes: provenance and record integrity. The frozen counter command in `claims.json` carries no flag, so this is not an active false pass, but any report quoting a `--write-evidence` run as the C1 gate would be claiming pass without the committed record.

### F4 — `entry_ok` and `province_ok` carry no evidentiary weight (observation, intended per `doc_gates`)
Observation. With zero carrier data, `entry_ok=1 (ok)` and `province_ok=1 (ok)` were reached by a 542-byte entry that cites `S096` and says it commits no result, plus one `PROVINCE.md` row that says `none yet`. Both are pure string checks (`CLAIM_ROW in text`; a `|` line containing the verb and `ENTRY` under a heading matching `Core` and not `Frontier|Adjacent|exclusion`). The frozen target therefore has two free fields; only `pass` discriminates. This is consistent with the frozen `doc_gates` wording, and the stronger record gate is `committed_check`'s `eid not in entry_text`, which is only reachable per passing carrier — so a real 12/12 pass does force the entry to name all 12 live `evidence_id`s. No correction requested.

### F5 — the full comparison is satisfiable: live envelopes are deterministic outside `meta` (observation, supports F1)
Observation. Two independent live runs over all 12 carriers (`clone2`, `clone3`, same commit, `--write-evidence`) produced envelope sets that are equal after removing top-level `meta` (`NONMETA_DIFFS: []`); the only varying field observed is `meta.duration` (`{…,"duration":"173ms"}` vs the other run). `data.evidence_id` is present and content-shaped (`ev_` + 64 hex) and equal across the two runs (`ev_fe9589c14b3445f946d1b213dd9915b44e67101a000ec14a92c5fb2fff303d52` for `chinook` in both). So `strip_meta(committed) != strip_meta(live)` is not an unsatisfiable gate, and `committed_check`'s `eid not in entry_text` lookup has a field to find. Impacted axis: coverage — this is what makes the M30-3 repair sound rather than a silent blocker.

### F6 — base absence holds (observation)
`git -C <lane> show 35ba7c5…:PROVINCE.md | grep -c inspect-sqlite-database` → `0`; `git -C <lane> grep -c inspect-sqlite-database 35ba7c5… -- PROVINCE.md SKILL.md corpus/knowledge` → no output, exit 1 (no hits). The verb is unclaimed at the freeze, as `claims.json` asserts. Counter selftest at the clone: `selftest cases=14 failures=0`, exit 0, `2026-10-23T04:13:56Z` (`selftest.out`, sha256 `86edbf914778623dcc762f0da984ac715ccc17b8cc7204ef9ce714dfeb698a9b`).

## Impacted axes
- Coverage (R31-C1): the all-false control adds no evidence and cannot produce `pass=12`; the counter's live-run plus committed-record pair is the sole gate, and it holds.
- Measurement/quality: F2 (target string vs printed line) and F4 (free doc-gate fields) affect how the claim is scored, not the claim's truth.
- Provenance: F3 (`--write-evidence` bypasses the record and `evidence_id` gates and still exits 0).

## Smallest safe correction
- Acceptance: score C1 on exit code plus the parsed fields (`pass=12`, `entry_ok=1`, `province_ok=1`), not on the literal frozen substring; and never quote a `--write-evidence` run as the C1 target (F2, F3). Both the counter and `claims.json` are frozen, so the fix is in the executor/L1 procedure; a round-32 counter change that prints the bare frozen line last is the durable version.
- No change to carriers, mutants, predictions, the oracle, or the claim is warranted by this control.

## Seat artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/CtlC1AllFalse/`)

| File | sha256 |
|---|---|
| `refusal.json` (the one refusal envelope copied 12×) | `f546ef05f4d7894ba9b189875a00f271ae675847dc91080381b1568320161a35` |
| `refusal.err` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `baseline.out` (command 1 stdout + `EXIT=1`) | `2bebd74590d6fc9d539da458212f608b7a42e2847bcb67b3c0018632846a297c` |
| `baseline.err` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `control.out` (command 2 stdout + `EXIT=1`) | `0568435cf5638cd495f340d4dd1640120213d029814f88a22f3ed60f686d4da5` |
| `control.err` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `write2.out` (clone2 `--write-evidence`, exit 0) | `6ba72656e9c41ecf77e251904fb3d07421da08c71ce75125b2e416be1e8b3f03` |
| `write3.out` (clone3 `--write-evidence`, exit 0) | `c0c6a54ba706f187c3f0a38fb5c5a200cccb5eb5f7b2872b8e97bc68b2cab950` |
| `selftest.out` (counter selftest, 14 cases 0 failures, exit 0) | `86edbf914778623dcc762f0da984ac715ccc17b8cc7204ef9ce714dfeb698a9b` |
| `clone/` (branch `ctl`, HEAD `bcec6566b4eaab17815e571ca0b967d8ab818a3c`) | control tree; `PROVINCE.md` `8de31d29…`, entry `372789d6…`, envelopes `f546ef05…` ×12 |
| `clone2/`, `clone3/` (branch `ctl`, HEAD `bcec6566…`) | live-envelope determinism probes; clone2 working tree left dirty with the uncommitted live envelopes |
| `tmp/` | `TMPDIR` for every REA run |

No tool was installed or updated (`npx` used the existing `rea-agents@6.5.0` cache at `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, version checked `6.5.0`). No web source was opened, so no source table applies. REA was run only through the counter and for the one refusal envelope the item specifies; no carrier or mutant was run outside a counter. No process was left running by this seat (the REA PIDs visible at `04:12Z` belong to sibling seats).
