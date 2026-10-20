# WaveOutcomesTool — forward fix for R18-DEADSEAT-RECORD

Seat: `KaidokuR19.WaveOutcomesTool` (executor). Report is observation/inference labelled; every
command below is pasted with its exit code. Work was done only in `/tmp/kr19-WaveOutcomesTool`
(copy of LANE at the contract baseline); the LANE worktree received only this report and the patch.

## Delivered

| item | value |
|---|---|
| patch | `.ufo/waves/round-19/w1/patches/WaveOutcomesTool.patch` |
| patch sha256 | `a6485a80bf02c69fcdc70b5903d6881590046114b0043c8902edbc8beb7646a9` |
| file added | `.ufo/waves/round-19/tools/wave-outcomes.py` (new, 840 lines, mode 100755) |
| observed clone base | `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (`git -C /tmp/kr19-WaveOutcomesTool rev-parse HEAD`) |

`git -C /tmp/kr19-WaveOutcomesTool diff --cached --stat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`:

```
 .ufo/waves/round-19/tools/wave-outcomes.py | 840 +++++++++++++++++++++++++++++
 1 file changed, 840 insertions(+)
```

No `__pycache__`/`.pyc` in the patch: `grep -c "pycache\|\.pyc" .ufo/waves/round-19/w1/patches/
WaveOutcomesTool.patch` printed `0`, `GREP_EXIT=1` (zero matches).

## Contract implemented (path:line anchors, all in `.ufo/waves/round-19/tools/wave-outcomes.py`)

CLI: `--registration REG --report-dir DIR --causes CAUSES --out OUT [--selftest]`; missing flags are
a named refusal, not an argparse default (`main` :800-834). Record per seat is exactly
`{name, role, report_present, cause}` (:309-316), written to `--out` atomically (:352-369).

- **report rule** (:16-18, `_report_present` :166-172): `<report-dir>/<name>.md` must be a regular
  file with size > 0. Zero-byte files, directories and dangling symlinks are absence; files not named
  `<seat>.md` are ignored. Every printed count carries its rule text (`_print_summary` :371-381,
  `RULE` :73-78).
- **cause rule** (:19-20): `causes[<name>]` or `causes[<agentId>]`, non-empty after `.strip()`; a
  whitespace-only string is not a cause. `source` is retained separately (`cause_sources`, :346).
- **exit rule** (:21, :349): 1 iff any seat with `report_present=false` has `cause=null`; 0 otherwise;
  2 on unusable input. Refusals write nothing and name the finding on stderr as
  `REFUSED <finding>: <detail>` (:833).
- **registration** (:121-163): requires `members` object (model
  `.ufo/waves/round-18/wave2-registration.json:8-1087`), non-empty `role` string per seat (:146-149),
  unique `agentId` (:296-307), and seat names that are bare file names — `../escape` is refused as
  `seat_name_unsafe` (:114-118, :128-132) so a registration cannot read outside the report dir.
- **causes shapes** (:228-289): flat map (string or object value), wrapped `{"wave","causes":{...}}`,
  list of `{"name"|"seat"|"agentId", "cause"|"reason"|"error"|"text", "source"}` rows; registration
  metadata keys in a flat map are ignored and counted (`causes_ignored_meta`). Every key resolves
  against the registration, so a typo'd seat is `causes_unknown_seat` (exit 2) instead of silently
  marking someone dead (:202-212); two conflicting entries for one seat are `causes_ambiguous`
  (:213-226).
- **determinism** (:40-44, :326-348, :356-361): no timestamp, no absolute-path computation, seats in
  byte order of name, inputs bound by `registration_sha256` / `causes_sha256`, `indent=2`,
  `ensure_ascii=True`, trailing newline, `os.replace`. Identical inputs give identical bytes (measured
  below).

## Selftest (run once in the clone, exact last line)

```
$ cd /tmp/kr19-WaveOutcomesTool && python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py --selftest
SELFTEST: CLEAN cases=33
EXIT=0
```

33 cases, fixtures under `tempfile.mkdtemp()` only (`_selftest` :391-798). Coverage by case
(labels are the selftest check labels): all-present, seat-shape, record-binding, missing-uncaused-red,
missing-null-cause, red-reason, string-cause, object-cause-source, agentid-key, blank-cause-red,
empty-and-dir-absent, report-dir-missing, unknown-cause-seat, registration-malformed, members-empty,
member-no-role, seat-name-escape, causes-malformed, causes-missing, ambiguous-cause,
duplicate-identical, unneeded-cause, deterministic-bytes, list-causes, wrapped-causes, flat-meta, meta-key-seat,
duplicate-agentid, out-unwritable, cause-value-type, cause-field-type, nameless-row, argv-missing.

The same selftest was re-run against the *patch applied to a fresh baseline clone* (see below) —
`SELFTEST: CLEAN cases=33`, exit 0 — so the delivered artifact, not just my working copy, is clean.

## Acceptance run: round-18 wave 2 with an empty causes file

Empty causes file: `printf '{}\n' > /tmp/kr19wo-empty-causes.json` (exit 0).

```
$ cd /tmp/kr19-WaveOutcomesTool && python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py \
    --registration .ufo/waves/round-18/wave2-registration.json \
    --report-dir .ufo/waves/round-18/w2 \
    --causes /tmp/kr19wo-empty-causes.json --out /tmp/kr19wo-r18w2.json
OUTCOMES seats=98 reports=94 missing=4 uncaused=4 (rule: report=report_present=<report-dir>/<name>.md exists as a regular file with size>0; cause=cause=causes[<name>| <agentId>], non-empty after strip)
MISSING n=4 ["GatePRODUCERREV", "GateSUMSRUNLOG", "ShonenLines", "TruthREGISTRY"] (rule: seat has no report file)
CAUSES recorded=0 unneeded=0 ignored_meta=0 (rule: one non-empty cause per seat, from causes[<name>|<agentId>])
UNCAUSED n=4 ["GatePRODUCERREV", "GateSUMSRUNLOG", "ShonenLines", "TruthREGISTRY"] (rule: 1 iff any seat with report_present=false has cause null) -> exit 1
OUT /tmp/kr19wo-r18w2.json
EXIT=1
```

Missing set: **`GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines`, `TruthREGISTRY`** — 4, as expected.
Record counts: `seat_count=98`, `report_present_count=94`, `missing_count=4`; the four rows carry
`role=reviewer`, `report_present=false`, `cause=null` [O].

Same run at the pinned historical revision `a245bb00c581ae3423a10a055c77d4bc873918df` (fresh clone,
`git -C /tmp/kr19wo-a245 rev-parse HEAD` = `a245bb00c581ae3423a10a055c77d4bc873918df`): exit **1**, the
same four names, 98/94/4 [O]. So the record is revision-faithful, not an artefact of `main`.

Green path on real data (no fabricated causes): wave 1 registration vs `w1/` reports exits **0** with
`seats=89 reports=89 missing=0` [O]. That directory also holds `swarm-registry.json`, which the
`<name>.md` rule ignores — evidence that non-report files cannot inflate presence.

Caused path on the real four, shape-only demo file `/tmp/kr19wo-demo-causes.json` whose cause text is
literally `DEMO SHAPE ONLY - not evidence` (a fixture; **not** dead-seat evidence — the real cause text
belongs to the `DeadSeatHistoryR18` seat): exit **0**, `uncaused=0`, `causes_recorded=4`, and the
mixed key forms all resolved (`name`, `agentId`, bare `agentId`) with `cause_sources` populated [O].

Determinism [O]: rerunning the wave-2 empty-causes command to a second path exited 1 and produced a
byte-identical file —
`0858f59569ffa8452ef69a3303df8d1609398df77fb6138a1c9a5f32dfebeb52` for both
`/tmp/kr19wo-r18w2.json` and `/tmp/kr19wo-r18w2-rerun.json`.

## Patch consumption check

```
$ git -C /tmp/kr19wo-applycheck apply --check .../WaveOutcomesTool.patch   -> APPLY_CHECK_EXIT=0
$ git -C /tmp/kr19wo-applycheck apply .../WaveOutcomesTool.patch           -> APPLY_EXIT=0
$ git -C /tmp/kr19wo-applycheck status --porcelain
?? .ufo/waves/round-19/                                                    (the applied dir; exit 0)
$ python3 -I -B /tmp/kr19wo-applycheck/.ufo/waves/round-19/tools/wave-outcomes.py --selftest
SELFTEST: CLEAN cases=33
SELFTEST_EXIT=0
$ cd /tmp/kr19wo-applycheck && python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py \
    --registration .ufo/waves/round-18/wave2-registration.json \
    --report-dir .ufo/waves/round-18/w2 \
    --causes /tmp/kr19wo-empty-causes.json --out /tmp/kr19wo-applycheck-out.json
OUTCOMES seats=98 reports=94 missing=4 uncaused=4 ...
UNCAUSED n=4 ["GatePRODUCERREV", "GateSUMSRUNLOG", "ShonenLines", "TruthREGISTRY"] (...) -> exit 1
R18RUN_EXIT=1
```

The applied patch therefore reproduces the acceptance result from a clean baseline checkout, not just
from my working copy [O]. A deliberately missing registration is refused by name:
`REFUSED registration_unreadable: /tmp/does-not-exist.json: no such file`, `MISSING_REG_EXIT=2` [O].

## Limits and risks (for the L1 to weigh)

- **Provenance of cause text is out of scope** [I]: the tool enforces presence/shape, not that the text
  came from an agent terminal. It preserves `source` so the caller's citation rides along, but it does
  not verify it. The dead-seat cause *content* is `DeadSeatHistoryR18`'s deliverable.
- **Unknown cause keys refuse (exit 2)** [O]: deliberate (a typo must not silently clear a dead seat),
  but it means one causes file cannot be reused across waves; the L1 must pass the per-wave map or a
  `{"causes": {...}}` wrapper for exactly this registration. If that proves inconvenient in practice,
  the smallest change is a `--allow-unknown-causes` demotion; I did not add an unrequested flag.
- **Registration schema is dict-members only** [O]: all six lane registrations round-16/17/18 use
  `{"members": {seat: {role: ...}}}` (observed with a `json.load` sweep over the six
  `.ufo/waves/round-1[678]/*registration*.json` files, all `dict` members carrying a role), so the
  strict refusal (`members_empty`, `member_invalid`) matches every existing input. A future list-shaped registry would be refused by name, not mis-parsed.
- **`--out` overwrites** [O]: atomic replace, identical bytes for identical inputs. If the L1 wants the
  r18 record retained as evidence, write it under `.ufo/waves/round-19/evidence/` on the first run; a
  rerun cannot silently change it unless an input changes (the input digests are in the record).
- **Reports are matched by name only** [I]: a seat whose report is nested (e.g. `w2/<seat>/report.md`)
  would count as dead. Round-18 w2 has no subdirectories (`find .ufo/waves/round-18/w2 -mindepth 1
  -type d | wc -l` printed `0`, `FIND_EXIT=0`), so this does not misreport the round-18 set.
- No tool installs or upgrades were performed for this seat (nothing was needed).

## Commands (all, with exits)

```
git clone -q --no-hardlinks LANE /tmp/kr19-WaveOutcomesTool                      -> 0
git -C /tmp/kr19-WaveOutcomesTool checkout -q --detach 8a8da7e...                -> 0
git -C /tmp/kr19-WaveOutcomesTool rev-parse HEAD                                 -> 0 (8a8da7e...)
python3 -c '<count missing at a245bb0 from git ls-tree>'                         -> 0 (4 missing)
python3 -I -B .../wave-outcomes.py --selftest                                    -> 0 (SELFTEST: CLEAN cases=33)
printf '{}\n' > /tmp/kr19wo-empty-causes.json                                    -> 0
... --registration .ufo/waves/round-18/wave2-registration.json --report-dir .ufo/waves/round-18/w2
    --causes /tmp/kr19wo-empty-causes.json --out /tmp/kr19wo-r18w2.json          -> 1
... same, --out /tmp/kr19wo-r18w2-rerun.json                                     -> 1
sha256sum /tmp/kr19wo-r18w2.json /tmp/kr19wo-r18w2-rerun.json                    -> 0 (equal)
git clone/checkout a245bb0 in /tmp/kr19wo-a245                                   -> 0
... (tool copy) --report-dir .ufo/waves/round-18/w2, empty causes                -> 1 (same 4)
... --registration .ufo/waves/round-18/wave1-registration.json --report-dir .../w1 -> 0 (89/89)
... --causes /tmp/kr19wo-demo-causes.json --out /tmp/kr19wo-r18w2-demo.json      -> 0 (demo shape)
cd /tmp/kr19-WaveOutcomesTool && git add -A && git diff --cached --binary 8a8da7e... > patch -> 0
git -C /tmp/kr19-WaveOutcomesTool diff --cached --stat 8a8da7e...                -> 0 (1 file, 840 +)
git -C /tmp/kr19wo-applycheck apply --check patch                                -> 0
git -C /tmp/kr19wo-applycheck apply patch                                        -> 0
python3 -I -B /tmp/kr19wo-applycheck/.../wave-outcomes.py --selftest             -> 0
python3 - <<'EOF' sweep of .ufo/waves/round-1[678]/*registration*.json
    (json.load; members dict + role per seat)                                    -> 0 (6/6 True)
find .ufo/waves/round-18/w2 -mindepth 1 -type d | wc -l                          -> 0 (printed 0)
grep -c "pycache\|\.pyc" .../WaveOutcomesTool.patch                              -> 1 (printed 0)
```
